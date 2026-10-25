#!/usr/bin/env python3
"""sen0401_manifest_errfirst_scan v1_0_0 - exit 0 only when no example of the newest chapter-code manifest of chapter NN has a first output line (in show[].expected, expected or result text) that starts with an error name (the page test 9.37.0 reads it as a failed run).
Usage: sen0401_manifest_errfirst_scan_v1_0_0.py NN"""
import glob, json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); nn = sys.argv[1]
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
f = sorted(glob.glob(os.path.join(R, "03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (nn, nn))), key=vk)[-1]
ERR = re.compile(r"^(\w*Error|Traceback|Stopped after)"); bad = []
for e in json.load(open(f))["examples"]:
    vals = [str(s.get("expected", "")) for s in (e.get("show") or [])] + [e["expected"]] if isinstance(e.get("expected"), str) else [str(s.get("expected", "")) for s in (e.get("show") or [])]
    for v in vals:
        l = v.strip().splitlines()[:1]
        if l and ERR.match(l[0]): bad.append((e.get("order"), e.get("name"), l[0][:60]))
print("manifest %s | %d examples | error-first examples: %s" % (os.path.basename(f), len(json.load(open(f))["examples"]), bad)); print("RESULT %s" % ("FAIL" if bad else "PASS")); sys.exit(1 if bad else 0)
