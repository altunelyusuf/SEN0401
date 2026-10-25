"""Chapter 1 deck link check, version 3.0.0 (NEW file). Reads every external hyperlink of the finished deck (python-pptx), asks each address once with curl through the agent proxy (follows redirects,
browser user agent, 30 seconds) and prints one line per address with the status code. Exit 0 when every address answers 200 to 399. With a second argument it writes the register (checked date, address,
status, slides that carry it) to that path ONCE (the file is written, never appended).
Usage: deck_links_check_v3_0_0.py <deck.pptx> [register.json]"""
__version__ = "3.0.0"
import datetime, json, subprocess, sys
from pptx import Presentation

deck = sys.argv[1]
links = {}
for i, s in enumerate(Presentation(deck).slides, 1):
    for r in s.part.rels.values():
        if r.is_external and r.target_ref.lower().startswith("http"):
            links.setdefault(r.target_ref, []).append(i)
rows, bad = [], 0
for url, sl in links.items():
    r = subprocess.run(["curl", "-sS", "-L", "-o", "/dev/null", "-A", "Mozilla/5.0 (X11; Linux x86_64)", "--max-time", "30", "-w", "%{http_code}", url], capture_output=True, text=True)
    code = int(r.stdout.strip() or 0) if r.stdout.strip().isdigit() else 0
    ok = 200 <= code < 400
    bad += not ok
    rows.append({"url": url, "status": code, "slides": sl, "ok": ok})
    print("%s %3d slides %s %s" % ("OK  " if ok else "FAIL", code, sl, url))
print("%d addresses, %d not answering 200-399" % (len(rows), bad))
if len(sys.argv) > 2:
    json.dump({"_version": __version__, "deck": deck.split("/")[-1], "checked": datetime.date.today().isoformat(), "links": rows}, open(sys.argv[2], "w"), indent=1)
sys.exit(1 if bad else 0)
