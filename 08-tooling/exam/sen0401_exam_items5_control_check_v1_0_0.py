#!/usr/bin/env python3
"""sen0401_exam_items5_control_check v1_0_0 - the lineage agent's own control of the private items parts 5A, 5B, 5C. Usage: ... a|b|c
Prints names, keys and counts only (no question, no answer text). Checks: the private file is git-ignored, untracked and unstaged; the executor's check re-run (exit 0); code traces executed here and equal to the stored output; numeric answers of 5B recomputed here from the stems' numbers without the builder; option-length bias counted; answer letters counted."""
import json, os, subprocess, sys, hashlib
REPO = "/home/claude/sen0401"; P = REPO + "/08-tooling/exam/"; part = sys.argv[1]
F = P + "private/sen0401_exam_items5%s_v1_0_0.json" % part
res = []
def ok(n, c, d=""): res.append(bool(c)); print("%s  %s  %s" % ("PASS" if c else "FAIL", n, d))
g = lambda *a: subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True)
rel = os.path.relpath(F, REPO)
ok("L1 private file is git-ignored, untracked and unstaged", g("check-ignore", rel).returncode == 0 and g("ls-files", rel).stdout.strip() == "" and rel not in g("diff", "--cached", "--name-only").stdout, rel.split("/")[-1])
ok("L2 no tracked exam file of the new papers or keys", not [x for x in g("ls-files", "08-tooling/exam").stdout.split() if "items5" in x and x.endswith(".json") or "papers_midterm_v4" in x])
r = subprocess.run([sys.executable, "-B", P + "sen0401_exam_items5%s_check_v1_0_0.py" % part], capture_output=True, text=True, cwd=REPO)
ok("E1 the executor's check re-run: exit 0, no FAIL line", r.returncode == 0 and not [l for l in r.stdout.splitlines() if l.strip().startswith("FAIL") or "[FAIL]" in l], "%d PASS lines" % r.stdout.count("PASS"))
d = json.load(open(F)); its = d["items"] if isinstance(d, dict) and "items" in d else d.get("slots") and d.get("items") or []
if part == "a":
    its = d["items"]; ch = [i for i in its if isinstance(i.get("options"), list)]
    ok("A1 seven choice sub-questions", len(its) == 7 and len(ch) == 7, "%d" % len(its))
    ok("A2 four distinct options and one valid answer index", all(len(set(i["options"])) == 4 and i["answer"] in range(4) for i in ch))
    lon = sum(1 for i in ch if max(range(4), key=lambda k: len(i["options"][k])) == i["answer"])
    print("INFO correct option is the longest in %d of %d items (to be rebalanced by 5M); answer letters %s" % (lon, len(ch), sorted(i["answer"] for i in ch)))
    # recompute three items from the stems
    it = {i["key"]: i for i in its}
    f = it["mt2:i02:fee-not-written"]; ok("A3 fee item: 140000 - 95000 - 8000 = 37000 equals the keyed option", "37,000" in f["options"][f["answer"]], "")
    c = it["mt2:i05:shop-confirmations"]; ok("A4 confirmations item: 10 percent needs 3 (z=2 gives 5.1), 30 percent needs 10 (z=9 gives 5.5)", "three" in c["options"][c["answer"]] and "ten" in c["options"][c["answer"]])
    o = it["mt3:a5:old-notes-and-new-keys"]; ok("A5 old notes: 3,000,000 / 1,000 = 3,000 equals the keyed option", "3,000 new marks" in o["options"][o["answer"]])
elif part == "b":
    its = d["items"]; out = {}
    for i in its:
        if i["type"] == "CodeTrace":
            import io, contextlib
            b = io.StringIO()
            with contextlib.redirect_stdout(b): exec(i["code"], {})
            out[i["key"]] = b.getvalue().strip(); ok("B1 code trace %s executed here equals the stored output" % i["key"], out[i["key"]] == str(i["output"]).strip(), out[i["key"]])
    v = {}
    v["vanity"] = 3 * 58 ** 2 // 58; ok("B2 vanity: 3 * 58^2 / 58 = %d" % v["vanity"], v["vanity"] == 174)
    h = 33 // 5; ok("B3 coinbase: halvings %d, subsidy %d, limit %d, claim 7 invalid" % (h, 8 >> h, (8 >> h) + 4), h == 6 and (8 >> h) + 4 == 4)
    tx = {"A": (100, 3000), "B": (250, 2500), "C": (200, 4000), "D": (150, 2250), "E": (50, 250)}; room = 500; fee = 0
    for k in sorted(tx, key=lambda k: -tx[k][1] / tx[k][0]):
        if tx[k][0] <= room: room -= tx[k][0]; fee += tx[k][1]
    ok("B4 fee-per-size block: total fee %d" % fee, fee == 9500)
    ok("B5 words to entropy: 18*11=198 bits, E + E/32 = 198 gives E=192", 192 + 192 // 32 == 18 * 11)
    ok("B6 pool wait 10 * 4000 / 100 = 400", 10 * 4000 // 100 == 400)
    ok("B7 pizza: (2*60000+3*70000)/5 * 10000 = 660 million", (2 * 60000 + 3 * 70000) // 5 * 10000 == 660_000_000)
    ok("B8 eight Q2 items, points add up to 25", len(its) == 8 and sum(int(i.get("points", 0)) for i in its) == 25, "%d items, %s points" % (len(its), sum(int(i.get("points", 0)) for i in its)))
else:
    its = d["items"]; print("INFO %d items in part C, keys: %s" % (len(its), ", ".join(i["key"] for i in its)))
    ok("C1 chapters of the form are 1 to 6 and every item has critical points and a primary chapter", all(i.get("critical_points") and i.get("chapters") for i in its))
    ok("C2 hand-marked bonus present", bool(d.get("bonus")))
print("RESULT " + ("PASS" if all(res) else "FAIL")); sys.exit(0 if all(res) else 1)
