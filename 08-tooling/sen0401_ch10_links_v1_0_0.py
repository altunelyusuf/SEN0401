#!/usr/bin/env python3
"""SEN0401 chapter 10: opens every story link and every further-reading link (curl, through the sandbox proxy) and records the HTTP status; a YouTube link is checked through oEmbed
(the title it returns is recorded). Writes ch10-evidence/links_checked_v1_0_0.json and exits 1 if any link is not 200."""
__version__ = "1.0.0"
import json, os, subprocess, sys, time, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_ch10_stories_v1_0_0 as ST
UA = "sen0401-research/1.0 (altunel.yusuf@gmail.com)"
def get(u):
    for i in range(4):
        r = subprocess.run(["curl", "-s", "-L", "-m", "40", "-A", UA, "-w", "\n%{http_code}", u], capture_output=True, text=True)
        body, _, code = r.stdout.rpartition("\n")
        if code == "200":
            return code, body
        time.sleep(10)
    return code, body
out, bad = {}, []
for u in [s["link"] for s in ST.STORIES] + [r[2] for r in ST.RESOURCES]:
    if "youtube.com/watch" in u:
        code, body = get("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(u, safe=""))
        out[u] = {"http": code, "oembed_title": json.loads(body)["title"] if code == "200" else None}
    else:
        code, body = get(u)
        out[u] = {"http": code}
    if code != "200":
        bad.append(u)
    print(out[u]["http"], u)
json.dump(out, open(os.path.join(HERE, "ch10-evidence", "links_checked_v1_0_0.json"), "w"), indent=1)
print("not ok:", bad)
sys.exit(1 if bad else 0)
