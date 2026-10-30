#!/usr/bin/env python3
"""sen0401_exam_papers_control_check v1_0_0 - the lineage agent's OWN control of the midterm paper (task TK_Exam_Papers_Build). Own key check from the items file and the paper graph, own page counts (pdfinfo), own print-safety reading (pdfimages, pixels of the rendered pages), and the answer sheet reader v1.1.0 run on synthetic sheets of the paper's OWN layout (synthetic students of the v1.0.0 stress model; no real data).
Usage: control.py REBUILT_DIR   (a folder made by the builder run again by the control)"""
import glob, json, os, re, random, subprocess, sys, tempfile, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rdflib
W = sys.argv[1]; COM = os.path.join(HERE, "papers_midterm_v1"); fails = []
def rep(n, ok, d=""): print("%s  %s  %s" % ("PASS" if ok else "FAIL", n, d)); (None if ok else fails.append(n))
P = "http://example.org/sen0401/engine/paper#"; PR = "http://example.org/sen0401/paperrules#"
items = {i["key"]: i for i in json.load(open(os.path.join(HERE, "sen0401_exam_items_midterm_v1_0_0.json")))["items"]}
def O(g, s, p):
    return next((str(o) for o in g.objects(s, rdflib.URIRef(PR + p))), None)
for order in ("chapter", "type"):
    base = "sen0401_exam_midterm_%s_v1_0_0" % order
    for f in ("_key.json", "_paper.ttl", "_sheet_layout.json", "_measure.json"):
        a = open(os.path.join(W, base + f), "rb").read(); b = open(os.path.join(COM, base + f), "rb").read()
        rep("A rebuilt %s equals the committed file" % (base + f)[-44:], a == b if not f.endswith("ttl") else re.sub(rb"[^\n]*(createdAt|generatedAt)[^\n]*\n", b"", a) == re.sub(rb"[^\n]*(createdAt|generatedAt)[^\n]*\n", b"", b))
    key = json.load(open(os.path.join(COM, base + "_key.json"))); g = rdflib.Graph(); g.parse(os.path.join(COM, base + "_paper.ttl"))
    pos = {}
    for s in g.subjects(rdflib.URIRef(PR + "position"), None):
        if str(s).startswith(P + "midterm_v1_item") and re.fullmatch(r"midterm_v1_item\d+", str(s)[len(P):]): pos[int(O(g, s, "position"))] = s
    bad = []; n = 0
    for ki in key["items"]:
        s = pos[ki["position"]]; ik = O(g, s, "itemKey").split("#")[0]; it = items[ik]; ans = ki["answer"]; t = ki["type"]; n += 1
        if t in ("ChoiceFour", "ChoiceFourCode"):
            texts = {O(g, o, "letter"): O(g, o, "text") for o in g.objects(s, rdflib.URIRef(PR + "option"))}
            if texts.get(ans) != it["options"][it["answer"]]: bad.append((ki["position"], "choice letter " + ans))
            if len(set(texts.values())) != 4 or sorted(texts) != list("ABCD"): bad.append((ki["position"], "options"))
        elif t == "Matching":
            prem = {O(g, p, "text"): O(g, next(g.objects(p, rdflib.URIRef(PR + "matchesTo"))), "letter") for p in g.objects(s, rdflib.URIRef(PR + "hasPremise"))}
            resp = {O(g, r, "text"): O(g, r, "letter") for r in g.objects(s, rdflib.URIRef(PR + "hasResponse"))}
            exp = {p["text"]: resp[p["match"]] for p in it["premises"]}
            if exp != prem: bad.append((ki["position"], "matching graph"))
            ptxt = {int(str(x).rsplit("prem", 1)[1]): O(g, x, "text") for x in g.objects(s, rdflib.URIRef(PR + "hasPremise"))}
            if any(ans["%d%s" % (ki["position"], "abcdefgh"[k])] != exp[ptxt[k]] for k in ptxt): bad.append((ki["position"], "matching key letters"))
        elif t == "Ordering":
            raw = subprocess.run(["pdftotext", os.path.join(COM, base + ".pdf"), "-"], capture_output=True, text=True).stdout
            seg = raw[raw.index("rows %da to" % ki["position"]):]; seg = seg[:seg.index("\n\n\n") if "\n\n\n" in seg else 1500]
            shown = {}; cur = None
            for ln in seg.splitlines()[1:]:
                m = re.match(r"([a-e])\) (.*)", ln)
                if m and m.group(1) in shown: break
                if m: cur = m.group(1); shown[cur] = m.group(2)
                elif not ln.strip() and len(shown) == len(it["steps"]): break
                elif cur and ln.strip() and not re.match(r"\d+[\.-]", ln): shown[cur] += " " + ln.strip()
            norm = lambda x: re.sub(r"\W", "", x.lower())[:30]
            ok = len(shown) == len(it["steps"]) and all(ans["%d%s" % (ki["position"], c)] == [norm(x) for x in it["steps"]].index(norm(v)) + 1 for c, v in shown.items())
            if not ok: bad.append((ki["position"], "ordering key against the printed steps", shown))
        elif t == "FillBlankGroup":
            e = next(g.objects(s, rdflib.URIRef(PR + "answerEntry")), None)
            ent = {O(g, x, "text"): O(g, x, "label") for x in g.objects(next(g.objects(s, rdflib.URIRef(PR + "bank"))), rdflib.URIRef(PR + "entry"))}
            blank_no = int(O(g, s, "blankNo")); 
        elif t == "NumericAnswer":
            if ans["value"] != it["key_value"]: bad.append((ki["position"], "number"))
        elif t == "CodeTrace":
            if str(ans) != str(it["output"]): bad.append((ki["position"], "trace"))
    # fill-in blanks through the bank
    for s in [pos[p] for p in pos if str(O(g, pos[p], "itemType")).endswith("FillBlank")]:
        ik = O(g, s, "itemKey"); base_k, bn = ik.split("#"); want = items[base_k]["blanks"][int(bn) - 1]["answer"]
        ent = {O(g, x, "text"): O(g, x, "label") for x in g.objects(next(g.objects(s, rdflib.URIRef(PR + "bank"))), rdflib.URIRef(PR + "entry"))}
        code = ent[want]; kv = [v for ki in key["items"] if ki["type"] == "FillBlankGroup" for v in [ki["answer"]]][0]
        if code not in kv.values(): bad.append((O(g, s, "position"), "fill code"))
    rep("B %s: key agrees with the items for all %d keyed entries (choice letter text, matching, ordering, fill-in bank codes, numbers, traces)" % (order, n), not bad, bad)
    letters = collections.Counter(ki["answer"] for ki in key["items"] if ki["type"] in ("ChoiceFour", "ChoiceFourCode")); rep("B %s letters spread" % order, max(letters.values()) - min(letters.values()) <= 1, dict(letters))
    pdf = os.path.join(COM, base + ".pdf"); sh = os.path.join(COM, base + "_sheet.pdf"); ky = os.path.join(COM, base + "_key.pdf")
    pg = lambda f: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
    rep("C %s pages: paper %d + sheet %d, key %d" % (order, pg(pdf), pg(sh), pg(ky)), (pg(pdf), pg(sh), pg(ky)) == ((5, 2, 1) if order == "chapter" else (5, 1, 1)))
    img = subprocess.run(["pdfimages", "-list", pdf], capture_output=True, text=True).stdout.strip().splitlines(); rep("D %s no image in the paper PDF" % order, len(img) <= 2)
    d = tempfile.mkdtemp(); subprocess.run(["pdftoppm", "-r", "60", "-png", pdf, d + "/p"]); from PIL import Image; import numpy as np
    col = 0
    for f in glob.glob(d + "/p*.png"):
        a = np.array(Image.open(f).convert("RGB")).astype(int); col += int((abs(a[..., 0] - a[..., 1]) + abs(a[..., 1] - a[..., 2]) > 12).sum())
    rep("D %s no colour in the rendered pages" % order, col == 0, "coloured pixels %d" % col)
# reader on the paper's own sheet layouts
import numpy as np
from PIL import Image
import sen0401_exam_answersheet_v1_1_0 as A
import sen0401_exam_answersheet_measure_v1_0_0 as MS
for order in ("chapter", "type"):
    base = "sen0401_exam_midterm_%s_v1_0_0" % order; lay = json.load(open(os.path.join(COM, base + "_sheet_layout.json")))
    work = tempfile.mkdtemp(); pngs = A.rasterise(os.path.join(COM, base + "_sheet.pdf"), os.path.join(work, "b")); blank = [np.array(Image.open(p).convert("L")) for p in pngs]
    tot = collections.Counter(); regf = 0; rows = 0
    for i in range(40):
        rng = random.Random(77000 + i); ims, truth = MS.student(lay, blank, rng); reg = [A.register(im, lay, p) for p, im in enumerate(ims)]
        if any(r is None for r in reg): regf += 1; continue
        out, bst, held = A.read_sheet(reg, lay); o, p = MS.score(out, truth); tot.update(o); rows += len(truth)
    print("   %s: 40 synthetic sheets, registration failures %d, rows %d, score %s" % (order, regf, rows, dict(tot)))
    bad_keys = [k for k in tot if re.search(r"silent|wrong|missed|unflagged", k, re.I) and tot[k]]
    rep("E reader v1.1.0 on the %s sheet layout: registration on every sheet and no silent wrong, missed or unflagged-empty count" % order, regf == 0 and not bad_keys, "non-zero bad counters %s" % {k: tot[k] for k in bad_keys})
print("CONTROL:", "FAIL " + str(fails) if fails else "PASS"); sys.exit(1 if fails else 0)
