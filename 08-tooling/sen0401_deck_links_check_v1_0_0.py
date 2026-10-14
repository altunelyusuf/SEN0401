#!/usr/bin/env python3
"""sen0401_deck_links_check v1.0.0 - opens every link of the chapter deck and writes the status each answered to chNN-deck/links_out_v1_0_0.json (port of SEN0414's links_check; SEN0401 had
no such step, its review notes record a manual run). The links are read from the plan: every 'links' item (the resources slide) and every story fact row. A status of 400 or more, or no
answer, refuses the deck, because the resources slide says that every link was opened on the day. A GET with a browser-like User-Agent through the build machine's proxy (HTTPS_PROXY).
GitHub's HTML pages are not reachable from the build machine, so the decks link raw.githubusercontent.com (the output says which links are raw).
Usage: sen0401_deck_links_check_v1_0_0.py NN [--no-write]       Environment: SEN0401_ROOT (needs requests).  Exit 0 when every link answered below 400."""
__version__ = "1.0.0"
import datetime, glob, json, os, re, sys
import requests

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
n = sys.argv[1]; chd = os.path.join(TOOL, "ch%s-deck" % n)
plan = json.load(open(sorted(glob.glob(os.path.join(chd, "deck_plan_v*.json")), key=vkey)[-1]))
links = []
for sl in plan["slides"]:
    for it in sl["items"]:
        if it.get("t") == "links":
            links += [r[1] for g in it["groups"] for r in g["rows"]]
        if it.get("t") == "factrow":
            links.append(it["link"])
links = list(dict.fromkeys(links))
rows, bad = [], 0
for u in links:
    try:
        r = requests.get(u, timeout=30, headers={"User-Agent": "Mozilla/5.0 (SEN0401 deck link check)"}, stream=True); st = r.status_code; r.close()
    except Exception as e:
        st = type(e).__name__
    rows.append([u, st])
    if not isinstance(st, int) or st >= 400: bad += 1
    print("  %s  %s" % (st, u))
if "--no-write" not in sys.argv:
    json.dump({"_version": __version__, "checked": datetime.date.today().isoformat(), "links": rows}, open(os.path.join(chd, "links_out_v1_0_0.json"), "w"), indent=1)
print("sen0401_deck_links_check %s (chapter %s): %d link(s) opened, %d not answered with a status below 400" % (__version__, n, len(rows), bad))
sys.exit(1 if bad else 0)
