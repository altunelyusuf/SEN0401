#!/usr/bin/env python3
"""Planted v8 copy must FAIL (X3b). Reads the CURRENT v8 item files in memory, plants verbatim and lightly changed copies as units of a temporary copy of the mock bank,
runs gate v1.0.1 on that bank and on a HTML built from it (temporary, never kept); the clean bank must PASS and every planted unit must FAIL.
Usage: mock_test_planted_v8_v1_0_0.py BANK.json [--log F]. Prints ids and counts only (no item text)."""
import json, sys, os, re, tempfile, importlib
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import mock_exclusion_gate_v1_0_1 as G
import importlib.util
spec = importlib.util.spec_from_file_location("mb", os.path.join(H, "mock_build_v1_0_2.py")); src = open(os.path.join(H, "mock_build_v1_0_2.py")).read().replace("\nmain()\n", "\n")
mb = type(sys)("mb"); mb.__dict__["__file__"] = os.path.join(H, "mock_build_v1_0_2.py"); exec(compile(src, "mock_build_v1_0_2.py", "exec"), mb.__dict__)
lines = []
def log(x): print(x); lines.append(x)
V8 = G.EXAM + "/v8/items/"
bank = json.load(open(sys.argv[1]))
def newest(idn):
    fs = [x for x in os.listdir(V8) if re.fullmatch(re.escape(idn) + r"_v\d+_\d+_\d+\.json", x)]
    return max(fs, key=lambda n: tuple(int(y) for y in re.findall(r"\d+", n[len(idn):])))
a2 = json.load(open(V8 + newest("v8_2a_target_after_adjustment"))); e2 = json.load(open(V8 + newest("sen0401_v8_item_2e")))
h2 = json.load(open(V8 + newest("sen0401_v8_item_2h"))); x2 = json.load(open(V8 + newest("sen0401_exam_x2_items")))
def numunit(i, st, kv, un): return {"id": i, "type": "numeric", "chapter": 1, "points": 3, "unit": un, "tip": "x", "can_be_4": False, "instances": [{"stem": st, "key_value": kv}]}
planted = [
  numunit("pl_2a", a2["stem"], a2["key_value"], a2["unit"]),
  numunit("pl_2e_numbers", G.bump_numbers(e2["stem"]), e2["key_value"] + 3, e2["unit"]),
  numunit("pl_2h_words", G.change_two_words(h2["stem"]), h2["key_value"], h2["unit"]),
  {"id": "pl_1c", "type": "choice", "chapter": 2, "points": 3, "stem": x2[0]["q"], "options": x2[0]["options"], "answer": 0},
  {"id": "pl_3c", "type": "ordering", "chapter": 2, "intro": x2[1]["q"], "steps": x2[1]["steps"], "answer": [2, 1, 3, 4, 5]},
]
gate = G.Gate(); ok = True
def run(items, label):
    msgs = []; n, f = G.run_items(gate, items, lambda x: msgs.append(x), label=label)
    failed = sorted({m.split()[1].split("#")[0] for m in msgs if " FAIL" in m and "units checked" not in m})
    return n, f, failed
n, f, failed = run(bank["items"], "clean")
log("clean bank: %d units, failed %d -> %s" % (n, f, "PASS" if f == 0 else "FAIL")); ok &= (f == 0)
bad = json.loads(json.dumps(bank)); bad["items"] += planted
n, f, failed = run(bad["items"], "planted")
want = sorted(p["id"] for p in planted)
log("planted bank: %d units, failed %d, failing ids %s, expected exactly %s -> %s" % (n, f, failed, want, "FAIL AS REQUIRED" if failed == want else "WRONG")); ok &= (failed == want)
with tempfile.TemporaryDirectory() as td:
    bp = os.path.join(td, "planted_bank.json"); json.dump(bad, open(bp, "w"))
    html = mb.build(bad, {"k": 1}, "planted test page")
    items = G.load_html_bank_text(html) if hasattr(G, "load_html_bank_text") else json.loads(re.search(r'<script id="mock-bank" type="application/json">(.*?)</script>', html, re.S).group(1).replace("<\\/", "</"))["items"]
    n, f, failed2 = run(items, "planted-html")
    log("planted page (temporary): %d units, failed %d, failing ids %s -> %s" % (n, f, failed2, "FAIL AS REQUIRED" if failed2 == want else "WRONG")); ok &= (failed2 == want)
log("PLANTED V8 TEST " + ("PASS" if ok else "FAIL"))
if "--log" in sys.argv: open(sys.argv[sys.argv.index("--log") + 1], "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
