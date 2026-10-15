"""One shared, human-readable activity log for the production board (owner 10-14: "I want to see what is going on").
from activity import log; log("Recording voice · Just ask · line 3 of 10")   →   logs/activity.log"""
import os, time
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/activity.log")
def log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f: f.write(time.strftime("%H:%M:%S") + "  " + msg + "\n")
