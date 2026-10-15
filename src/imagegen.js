// Photoreal image generation through the official Codex CLI ($imagegen skill, gpt-image), on the ChatGPT plan login.
// CI restores ~/.codex/auth.json from the CODEX_AUTH_JSON secret (see the workflow).
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn } = require("child_process");

// Fixed house style, appended to every scene so the look never drifts.
const STYLE = `Create a photorealistic image: a real photograph taken on a real camera, the kind of frame a cinematographer would light for a quiet film scene.
Shot on 35mm film with a 35mm or 50mm lens at eye level or slightly low, shallow depth of field, subtle natural film grain, natural colour balance.
Motivated practical lighting with a clear direction (a single lamp, a window, a narrow beam through dust); deep natural shadows; exactly one small vivid lime-green (#D7FF3C) light as the accent, everything else in cool blue-grey and warm shadow.
Real materials with honest imperfections: dust, fingerprints, scuffs, worn edges, uneven surfaces. The image should feel honest and unposed, like a captured moment, not a render.
No CGI or 3D-render look, no glossy perfection, no studio polish, no glamorization, no heavy retouching.
Absolutely no text, letters, numbers, signs, logos, labels, watermarks, captions, UI or screens with writing anywhere in the image.
No humanoid robots, no glowing brains, no people's faces, no cartoon, illustration, vector or concept-art styles.
Landscape 3:2 (1536x1024), high quality, PNG.`;

function generatedDir() {
  return path.join(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"), "generated_images");
}

function newestPng(dir, since) {
  let best = null;
  const walk = (d) => {
    for (const e of fs.existsSync(d) ? fs.readdirSync(d, { withFileTypes: true }) : []) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (/\.(png|jpe?g|webp)$/i.test(e.name)) {
        const m = fs.statSync(p).mtimeMs;
        if (m >= since && (!best || m > best.m)) best = { p, m };
      }
    }
  };
  walk(dir);
  return best && best.p;
}

// refPath: optional style reference (only "style-input" entries from design/references, i.e. our own posters)
async function generateImage(scene, outPath, { timeoutMs = 8 * 60000, refPath = null, style = STYLE, refNote = null } = {}) {
  const started = Date.now() - 1000;
  const prompt = `Use the $imagegen skill to generate exactly ONE image, then stop. Do not run any shell commands and do not edit files.

${refPath ? (refNote || "Use the attached image ONLY as a STYLE reference: match its poster grammar, finish and typography treatment. Do NOT copy its subject, colours or words.") + "\n\n" : ""}Scene: ${scene}

${style}`;
  let log = "";
  await new Promise((resolve, reject) => {
    const args = ["exec", "--skip-git-repo-check", "-s", "read-only"];
    if (refPath) args.push("--image", refPath, "--"); // "--" stops --image from swallowing the stdin marker
    args.push("-");
    const child = spawn("codex", args, {
      cwd: os.tmpdir(), stdio: ["pipe", "pipe", "pipe"],
    });
    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      reject(new Error("codex image generation timed out"));
    }, timeoutMs);
    child.stdout.on("data", (d) => (log += d));
    child.stderr.on("data", (d) => (log += d));
    child.on("error", (e) => {
      clearTimeout(timer);
      reject(new Error(`could not start codex CLI: ${e.message}`));
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      if (code !== 0) return reject(new Error(`codex exited ${code}: ${log.slice(-400)}`));
      resolve();
    });
    child.stdin.end(prompt);
  });
  // read the image from THIS run's session folder (parallel runs must not grab each other's files)
  const sid = (log.match(/session id:\s*([0-9a-f-]{36})/i) || [])[1];
  const file = sid ? newestPng(path.join(generatedDir(), sid), 0) : newestPng(generatedDir(), started);
  if (!file) throw new Error("codex finished but no image was generated (is the ChatGPT login valid?)");
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.copyFileSync(file, outPath);
  return outPath;
}

module.exports = { generateImage, STYLE };
