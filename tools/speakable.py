"""Turn on-screen text into what a human narrator would SAY. Strict: the result may contain only letters, spaces and
basic punctuation — any digit or symbol left over is an error (the voice must never read "₹", "%", "/", ".gov" or
"1930" the way a machine does). Usage: python3 tools/speakable.py "text" ...   (prints the spoken form)

Rules (also in brand/BRAND.md → Voiceover):
  helplines & phone numbers   digit by digit, grouped:  1930 → "one nine three zero"; 1-800-555-0142 → "one, eight hundred, ..."
  money                        ₹4,80,000 → "four lakh eighty thousand rupees" (Indian grouping for ₹: lakh, crore)
                               $1.6B → "one point six billion dollars"; £55.5M → "fifty-five point five million pounds"
  percentages                  44% → "forty-four percent"; −60% → "down sixty percent"
  years                        2025 → "twenty twenty-five"; 2000–2009 → "two thousand and five"
  counts                       6,833 → "six thousand, eight hundred and thirty-three"; 3 → "three"
  ranges / slashes / &          9–5 → "nine to five"; a/b → "a or b"; & → "and"; + → "plus"
  web addresses                cybercrime.gov.in → "cybercrime dot gov dot in"; reportfraud.ftc.gov → "report fraud dot F T C dot gov"
  acronyms                     spelled letter by letter when people say them that way (OTP → "O T P", UPI, SIM stays "sim")
  times                        9:41 → "nine forty-one"; ordinals 1st → "first"
  never spoken                 emoji, hashtags, brackets, ellipses, defanged links (example[.]top → "a fake link")."""
import re, sys

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
DIG = {str(i): ONES[i] for i in range(10)}
ACRONYMS = {"OTP": "O T P", "UPI": "U P I", "FBI": "F B I", "FTC": "F T C", "IC3": "I C three", "I4C": "I four C", "RBI": "R B I",
            "SEBI": "sebi", "ID": "I D", "PIN": "pin", "SMS": "S M S", "CVV": "C V V", "KYC": "K Y C", "APK": "A P K", "QR": "Q R",
            "AI": "A I", "URL": "U R L", "UK": "U K", "US": "U S", "USA": "U S A", "ATM": "A T M", "PDF": "P D F", "CBI": "C B I",
            "ED": "E D", "GPS": "G P S", "IRS": "I R S", "HMRC": "H M R C", "DMV": "D M V", "USPS": "U S P S", "NPCI": "N P C I",
            "CERT-In": "cert in", "SIM": "sim", "OK": "okay", "eSIM": "e-sim", "DOJ": "D O J"}
# words an English voice mispronounces: spelled the way they should SOUND (shown text keeps the real spelling).
# Amma is "UM-mah" (short first vowel, doubled m); read as written it comes out "AA-MAA".
PRONOUNCE = {"Amma": "Umma", "amma": "umma", "Appa": "Uppa", "appa": "uppa", "Paytm": "pay T M", "Aadhaar": "Aadhar", "rupee": "rupee",
             "lakh": "lakh", "crore": "crore", "Bengaluru": "Bengga-luru", "WhatsApp": "WhatsApp"}
ORD = {"1st": "first", "2nd": "second", "3rd": "third", "4th": "fourth", "5th": "fifth", "6th": "sixth", "7th": "seventh", "8th": "eighth", "9th": "ninth", "10th": "tenth"}


def under1000(n):
    w = []
    if n >= 100: w.append(ONES[n // 100] + " hundred"); n %= 100; w.append("and") if n else None
    if n >= 20: w.append(TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else ""))
    elif n or not w: w.append(ONES[n])
    return " ".join(x for x in w if x)


def words(n, indian=False):
    n = int(n)
    if n == 0: return "zero"
    parts = []
    scales = [(10**7, "crore"), (10**5, "lakh"), (1000, "thousand")] if indian else [(10**9, "billion"), (10**6, "million"), (1000, "thousand")]
    for v, name in scales:
        if n >= v: parts.append(f"{words(n // v, indian) if indian and n // v >= 1000 else under1000(n // v)} {name}"); n %= v
    if n: parts.append(("and " if parts and n < 100 else "") + under1000(n))
    return ", ".join(parts) if not indian else " ".join(parts)


def decimal(s, indian=False):
    a, _, b = s.partition(".")
    return words(int(a.replace(",", "") or 0), indian) + (" point " + " ".join(DIG[d] for d in b) if b else "")


def year(y):
    y = int(y)
    if 2000 <= y <= 2009: return "two thousand" + (" and " + ONES[y - 2000] if y > 2000 else "")
    return under1000(y // 100).replace(" and", "") + " " + (under1000(y % 100) if y % 100 >= 10 else ("oh " + ONES[y % 100] if y % 100 else "hundred"))


SCALE = {"k": "thousand", "K": "thousand", "m": "million", "M": "million", "b": "billion", "B": "billion", "bn": "billion", "cr": "crore", "L": "lakh"}
CUR = {"$": "dollars", "₹": "rupees", "£": "pounds", "€": "euros", "A$": "Australian dollars", "C$": "Canadian dollars"}


def speak(text, lang="en"):
    t = text
    if lang == "hi": t = t.replace("।", ".").replace("॥", ".")   # Hindi danda → full stop (Fish reads Devanagari natively; Latin loanwords stay Latin)
    t = re.sub(r"\[([^\]]*)\]", r"\1", t).replace("<br>", " ")          # highlight brackets / line breaks
    t = re.sub(r"\{([^}]*)\}", r"\1", t)                                 # tell markers
    t = re.sub(r"[\w-]+\[\.\][\w./-]+", "a fake link", t)                # defanged links are never read out
    t = re.sub(r"#\w+", "", t)
    t = re.sub(r"[\U0001F300-\U0001FAFF☀-➿]", "", t)
    t = t.replace("…", ".").replace("...", ".").replace("“", '"').replace("”", '"').replace("’", "'")
    t = re.sub(r"\(([^)]*)\)", r", \1,", t)
    # web addresses
    def url(m):
        u = m.group(0).lower().replace("https://", "").replace("http://", "").replace("www.", "")
        out = []
        for part in re.split(r"([./])", u):
            if part == ".": out.append("dot")
            elif part == "/": out.append("slash")
            elif part: out.append(ACRONYMS.get(part.upper(), part) if part.upper() in ("FTC", "FBI", "IC3") else part.replace("reportfraud", "report fraud"))
        return " ".join(out)
    t = re.sub(r"\b(?:https?://)?(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:gov|com|org|net|in|uk|au|ca|io|co|police)(?:\.[a-z]{2})?(?:/[\w/-]*)?\b", url, t, flags=re.I)
    # helplines, short codes and phone numbers: digit by digit
    t = re.sub(r"\b1930\b", "one nine three zero", t)
    t = re.sub(r"\b(text|dial|call|ring|forward(?: it)? to|sms)\s+(\d{3,6})\b", lambda m: m.group(1) + " " + " ".join(DIG[c] for c in m.group(2)), t, flags=re.I)
    t = re.sub(r"\b(\d{3,6})\s+(helpline|hotline|short code)\b", lambda m: " ".join(DIG[c] for c in m.group(1)) + " " + m.group(2), t, flags=re.I)
    t = re.sub(r"\bH([12])\b", lambda m: "the " + ("first" if m.group(1) == "1" else "second") + " half of", t)
    t = re.sub(r"\bQ([1-4])\b", lambda m: "the " + ["first", "second", "third", "fourth"][int(m.group(1)) - 1] + " quarter of", t)
    t = re.sub(r"\b1-(\d{3})-([A-Z0-9-]+)\b", lambda m: "one, " + " ".join(DIG.get(c, c) for c in m.group(1)) + ", " + m.group(2).replace("-", " "), t)
    t = re.sub(r"\+?\b\d[\d -]{6,}\d\b", lambda m: ", ".join(" ".join(DIG[c] for c in g) for g in re.split(r"[ -]+", m.group(0).lstrip("+"))), t)
    # money with scale: $1.6B, ₹10,178 cr, £55.5M, A$837.7M
    t = re.sub(r"(A\$|C\$|[$₹£€])\s?(\d[\d,]*(?:\.\d+)?)\s?(bn|cr|[kKmMbBL])\b",
               lambda m: f"{decimal(m.group(2).replace(',', ''), m.group(1) == '₹')} {SCALE[m.group(3)]} {CUR[m.group(1)]}", t)
    t = re.sub(r"(A\$|C\$|[$₹£€])\s?(\d[\d,]*(?:\.\d+)?)", lambda m: f"{decimal(m.group(2).replace(',', ''), m.group(1) == '₹')} {CUR[m.group(1)]}", t)
    # percentages, signed
    t = re.sub(r"\b(fell|dropped|down|cut|lost|fall|drop|decreased|declined)\s+(?:by\s+)?[−-](\d+(?:\.\d+)?)%", lambda m: f"{m.group(1)} {decimal(m.group(2))} percent", t)
    t = re.sub(r"[−-](\d+(?:\.\d+)?)%", lambda m: f"down {decimal(m.group(1))} percent", t)
    t = re.sub(r"\+(\d+(?:\.\d+)?)%", lambda m: f"up {decimal(m.group(1))} percent", t)
    t = re.sub(r"(\d+(?:\.\d+)?)\s?%", lambda m: f"{decimal(m.group(1))} percent", t)
    # times, ordinals, years, ranges
    t = re.sub(r"\b(\d{1,2}):(\d{2})\b", lambda m: f"{words(m.group(1))} {'o\'clock' if m.group(2) == '00' else ('oh ' + ONES[int(m.group(2))] if int(m.group(2)) < 10 else words(m.group(2)))}", t)
    t = re.sub(r"\b(\d{1,2})(st|nd|rd|th)\b", lambda m: ORD.get(m.group(0), words(m.group(1)) + "th"), t)
    t = re.sub(r"\b(19[5-9]\d|20[0-4]\d)\b(?!,\d|\d)", lambda m: year(m.group(1)), t)
    t = re.sub(r"(\d+)\s?[–-]\s?(\d+)", r"\1 to \2", t)
    # remaining numbers (with scale words like 2.1M, 5x)
    t = re.sub(r"\b(\d[\d,]*(?:\.\d+)?)\s?(bn|[kKmMbB])\b", lambda m: f"{decimal(m.group(1).replace(',', ''))} {SCALE[m.group(2)]}", t)
    t = re.sub(r"\b(\d+)x\b", lambda m: f"{words(m.group(1))} times", t)
    t = re.sub(r"\b\d[\d,]*(?:\.\d+)?\b", lambda m: decimal(m.group(0).replace(",", "")), t)
    # symbols and acronyms
    t = t.replace("&", " and ").replace("+", " plus ").replace("/", " or ").replace("=", " equals ").replace("@", " at ").replace("→", ", then ")
    t = t.replace("—", ", ").replace("–", ", ").replace(";", ",").replace(":", ",").replace('"', "")
    for k, v in sorted(ACRONYMS.items(), key=lambda x: -len(x[0])):
        t = re.sub(rf"(?<![\w-]){re.escape(k)}(?![\w-])", v, t)
    t = re.sub(r"\b[A-Z]{3,}\b", lambda m: m.group(0).lower() if m.group(0) not in ACRONYMS.values() else m.group(0), t)   # SHOUTING words → normal
    for k, v in PRONOUNCE.items():
        if k != v: t = re.sub(rf"\b{re.escape(k)}\b", v, t)
    t = re.sub(r"\s+,", ",", re.sub(r",\s*,", ",", re.sub(r"\s+", " ", t))).strip(" ,")
    return t


def check(spoken, lang="en"):
    """Strict gate: a spoken line may hold only letters, spaces and . , ? ! ' -  (lang "hi": plus Devanagari U+0900-U+097F and the danda)"""
    bad = re.findall(r"[^A-Za-z\u0900-\u097F\u0964\u0965 .,?!'\-]" if lang == "hi" else r"[^A-Za-z .,?!'\-]", spoken)
    return sorted(set(bad))


if __name__ == "__main__":
    for a in sys.argv[1:]:
        s = speak(a); b = check(s)
        print(f"{a}\n  → {s}" + (f"\n  ✗ leftover: {''.join(b)}" if b else ""))
