#!/usr/bin/env python3
"""sen0401_exam_items_control_check v1_0_0 - the lineage agent's OWN control of the midterm items (task TK_Exam_Items_Build). Not the executor's tools: own loader, own seed resolution, own similarity (difflib on whole stems and option sets, token overlap), own re-computation of the number and trace keys, own count of units, chapters, types, levels and letters.
Prints PASS / FAIL lines and, with 'pairs', the nearest item-seed pairs for reading by a person. Exit 1 when a FAIL line is printed. Usage: control.py [pairs]"""
import difflib, glob, json, os, re, subprocess, sys, collections
T = "/home/claude/sen0401/08-tooling/"; F = T + "exam/sen0401_exam_items_midterm_v1_0_0.json"
D = json.load(open(F)); IT = D["items"]; fails = []
def rep(n, ok, d=""): print("%s  %s  %s" % ("PASS" if ok else "FAIL", n, d)); (None if ok else fails.append(n))
def units(i): return len(i["blanks"]) if i["type"] == "FillBlankGroup" else 1
def comps(i):
    c = []
    if i.get("q"): c.append(i["q"])
    c += [b["text"] for b in i.get("blanks", [])] + [p["text"] for p in i.get("premises", [])] + i.get("steps", [])
    return c
def opts(i): return list(i.get("options", []))
# page items
PAGE = {}
for fp in sorted(glob.glob(T + "ch0[1-6]-page/question_bank_v*.json") + glob.glob(T + "ch0[1-6]-page/quiz_v*.json")):
    ch = int(re.search(r"ch0(\d)-page", fp).group(1)); name = os.path.basename(fp); data = json.load(open(fp))
    if isinstance(data, dict): data = data.get("items") or data.get("questions") or list(data.values())[0]
    for k, x in enumerate(data): PAGE[("ch%02d/%s#%d" % (ch, name, k))] = x
def ptext(x): return (x.get("q") or x.get("question") or x.get("stem") or "", [str(o) for o in (x.get("options") or [])])
rep("A1 units: fill-in blanks count as one each", sum(units(i) for i in IT) == 24, "items %d, units %d" % (len(IT), sum(units(i) for i in IT)))
byc = collections.Counter(); [byc.update({i["chapters"][0]: units(i)}) for i in IT]; rep("A2 four units per chapter 1 to 6 by the first chapter of an item", all(byc[c] == 4 for c in range(1, 7)), dict(sorted(byc.items())))
rep("A3 papers field says midterm only", all(i["papers"] == ["midterm"] for i in IT))
rep("A4 no item key or text equals a page item", not any(ptext(x)[0].strip() == i.get("q", "#").strip() for x in PAGE.values() for i in IT))
miss = [s for i in IT for s in i["seeds"] if s not in PAGE]; rep("B1 every seed key resolves to a page item", not miss, "missing %s; pages read %d items" % (miss, len(PAGE)))
cp = json.load(open(T + "exam/sen0401_exam_critical_points_v1_0_0.json")); txt = json.dumps(cp); ids = set(re.findall(r"CP\d\.\d\d", txt)); bad = [c for i in IT for c in i["critical_points"] if c not in ids]
rep("B2 every critical point id exists in the list", not bad, "ids in list %d, unknown %s" % (len(ids), bad))
noseed = [i["key"] for i in IT if not i["seeds"]]; rep("B3 an item without seed gives its reason", all(i["no_seed_reason"] for i in IT if not i["seeds"]), "without seed: %s" % noseed)
rep("B4 every source file exists", all(os.path.exists("/home/claude/sen0401/" + i["source"]["file"]) for i in IT if i.get("source")), "")
# trace
ok = True
for i in IT:
    if i["type"] == "CodeTrace":
        pre = "def cs_encode(n):\n    if n < 253: return bytes([n])\n    if n <= 0xffff: return b\"\\xfd\" + n.to_bytes(2, \"little\")\n    if n <= 0xffffffff: return b\"\\xfe\" + n.to_bytes(4, \"little\")\n    return b\"\\xff\" + n.to_bytes(8, \"little\")\n" if "cs_encode" in i["code"] and "def cs_encode" not in i["code"] else ""
        r = subprocess.run([sys.executable, "-I", "-c", pre + i["code"]], capture_output=True, text=True, timeout=20); got = r.stdout.strip(); good = got == str(i["output"]).strip(); ok &= good; print("   trace", i["key"], "(my own cs_encode supplied; the listing on the paper does not define it)" if pre else "", "prints", got, "key", i["output"], "OK" if good else "DIFFERENT")
rep("C1 trace listings re-run here print the key", ok)
import math
own = {"mt1:i02:toy-chain-supply": sum(50 * (40 >> k) for k in range(10)), "mt1:i03:vwap-third-trade": 63250 * 4 - 62000 - 2 * 63000, "mt1:i05:change-after-fee-rate": 200000 - 120000 - 18 * math.ceil(1126 / 4), "mt1:i13:vanity-factor": 58 ** 2, "mt1:i16:words-to-entropy": next(e for e in range(128, 257, 32) if e + e // 32 == 18 * 11)}
nums = {i["key"]: i["key_value"] for i in IT if i["type"] == "NumericAnswer"}; rep("C2 number keys equal my own computation from the stem", all(own.get(k) == v for k, v in nums.items()) and set(own) == set(nums), "keys %s own %s" % (nums, own))
ch = [i for i in IT if i["type"] in ("ChoiceFour", "ChoiceFourCode")]; rep("D1 choice answers are valid and options distinct", all(0 <= i["answer"] < 4 and len(set(i["options"])) == 4 for i in ch), "letters " + str(collections.Counter("ABCD"[i["answer"]] for i in ch)))
rep("D2 no option refers to another option", not any(re.search(r"\b(all|none) of the above|both [ab]\b|option [a-d]\b", o, re.I) for i in ch for o in i["options"]))
rep("D3 code lines at most 45 characters", all(len(l) <= 45 for i in IT for l in i.get("code", "").split("\n")), "longest %d" % max(len(l) for i in IT for l in i.get("code", "").split("\n")))
lv = collections.Counter(units(i) and i["bloom"] for i in IT); ap = sum(units(i) for i in IT if i["bloom"] >= 3); an = sum(units(i) for i in IT if i["bloom"] >= 4)
rep("D4 the executor's labels: Apply or above at least 13 units, Analyze or above at least 6 units (the labels are the executor's own; a person confirms)", ap >= 13 and an >= 6, "Apply+ %d, Analyze+ %d, items by level %s" % (ap, an, dict(lv)))
# own similarity
R = lambda a, b: difflib.SequenceMatcher(None, a, b).ratio()
rows = []
for i in IT:
    for c in comps(i):
        for k, x in PAGE.items():
            q, o = ptext(x)
            if not q: continue
            r = R(c.lower(), q.lower()) if abs(len(c) - len(q)) < 0.5 * max(len(c), len(q)) else 0.0
            if r > 0.3: rows.append((r, i["key"], k, c, q))
    if opts(i):
        so = set(o.lower() for o in opts(i))
        for k, x in PAGE.items():
            po = set(o.lower() for o in ptext(x)[1])
            if po and so:
                j = len(so & po) / len(so | po)
                if j > 0.3: rows.append((j, i["key"], k, "OPTIONS", "OPTIONS"))
rows.sort(key=lambda r: -r[0]); mx = rows[0][0] if rows else 0
rep("E1 own similarity: no component of any item has a whole-stem ratio or option overlap of 0.6 or more with a page item", mx < 0.6, "highest %.3f over %d pairs above 0.3" % (mx, len(rows)))
R_ = json.load(open(T + "exam/sen0401_exam_items_midterm_report_v1_0_0.json")); tested = {c for i in IT for c in i["critical_points"] if c.startswith("CP") and 1 <= int(c[2]) <= 6}
pt = R_["points_tested"]; pn = R_["points_not_tested"]; npt = len(pt) if hasattr(pt, "__len__") else pt; npn = len(pn) if hasattr(pn, "__len__") else pn
rep("F1 the report names the points tested and not tested, and its tested count equals my own count from the items", npt == len(tested) and npt + npn == 101, "mine %d tested; report %s tested and %s not tested of 101" % (len(tested), npt, npn))
if "pairs" in sys.argv:
    seen = set(); n = 0
    for r, k, pk, c, q in rows:
        if (k, pk) in seen: continue
        seen.add((k, pk)); n += 1; print("\n[%d] %.3f ITEM %s  vs PAGE %s\n   ITEM: %s\n   PAGE: %s" % (n, r, k, pk, c[:330], q[:330]))
        if n >= 20: break
print("CONTROL:", "FAIL " + str(fails) if fails else "PASS (the nearest pairs above need reading by a person)"); sys.exit(1 if fails else 0)
