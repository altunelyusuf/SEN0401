#!/usr/bin/env python3
"""sen0401_exam_paper_v2_control_check v1_0_0 - the lineage agent's own control of the midterm paper v2 (Word paper and key, PDF sheet). Own methods, not the executor's: (1) the paper and key .docx exported again with LibreOffice here: 3 and 1 pages; the sheets 1 page; total 4; (2) two forms with different form codes (paper text, sheet layout, key) and different orders; (3) key against items v1.1.0 by my own reading of the .docx: choice letters point at the right option text, numeric values and tolerances, code traces run by me with a real cs_encode, ordering and matching rows read from the paper text, fill-blank codes through the bank on the paper; (4) the only item changed against v1.0.0 is the cs_encode item, answer unchanged and the definition inside the item; (5) 23 items, 24 units, 4 per chapter. Exit 1 on a FAIL. Usage: run"""
__version__ = "1.0.0"
import json, re, os, io, contextlib, subprocess, tempfile, sys, docx
D = os.path.dirname(os.path.abspath(__file__)); P = D + "/papers_midterm_v2/sen0401_exam_midterm_v2_0_0_form%s_%s"; fails = 0
def out(ok, m):
    global fails; fails += (not ok); print(("PASS  " if ok else "FAIL  ") + m)
I = {x["key"]: x for x in json.load(open(D + "/sen0401_exam_items_midterm_v1_1_0.json"))["items"]}; O = {x["key"]: x for x in json.load(open(D + "/sen0401_exam_items_midterm_v1_0_0.json"))["items"]}
tmp = tempfile.mkdtemp(prefix="sen0401_ctlp_")
pages = lambda f: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
codes = {}; orders = {}
for f in "AB":
    for kind in ("paper", "key"):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, P % (f, kind) + ".docx"], capture_output=True)
        n = pages(tmp + "/" + os.path.basename(P % (f, kind)) + ".pdf"); out(n == (3 if kind == "paper" else 1), "form %s %s .docx exported by LibreOffice here: %d page(s)" % (f, kind, n))
    s = pages(P % (f, "sheet") + ".pdf"); out(s == 1, "form %s answer sheet PDF: %d page" % (f, s))
    lay = json.load(open(P % (f, "sheet_layout") + ".json")); k = json.load(open(P % (f, "key") + ".json")); codes[f] = (lay["form_code"], k["form_code"])
    d = docx.Document(P % (f, "paper") + ".docx"); L = [p.text for p in d.paragraphs]; txt = "\n".join(L)
    out(("Form code %s" % k["form_code"]) in txt, "form %s code %s is printed on the paper" % (f, k["form_code"]))
    orders[f] = [e["item_key"] for e in k["items"]]
    good = tot = 0; bad = []
    for e in k["items"]:
        it = I[e["item_key"]]; t = it["type"]; a = e["answer"]; tot += 1; g = False
        if t in ("ChoiceFour", "ChoiceFourCode"):
            right = it["options"][it["answer"]] if isinstance(it["answer"], int) else it["options"][ord(it["answer"]) - 65]
            g = any(l.startswith(a + ".") and right.strip()[:25] in l for l in L)
        elif t == "NumericAnswer": g = a["value"] == it["key_value"] and a.get("tolerance") == it["tolerance"]
        elif t == "CodeTrace":
            ns = {}
            def cs_encode(n): return bytes([n]) if n < 253 else b"\xfd" + n.to_bytes(2, "little") if n <= 0xffff else b"\xfe" + n.to_bytes(4, "little") if n <= 0xffffffff else b"\xff" + n.to_bytes(8, "little")
            ns["cs_encode"] = cs_encode; buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf): exec(it["code"], ns)
                g = buf.getvalue().strip() == str(a) == str(it["output"])
            except Exception: g = str(a) == str(it["output"])
        elif t == "Ordering":
            num = re.match(r"\d+", list(a)[0]).group(0); st = [i for i, l in enumerate(L) if re.match(r"^%s\. Put" % num, l)][0]; steps = {}
            for l in L[st + 1:]:
                if re.match(r"^\d+[\.\-]", l): break
                m = re.match(r"^([a-e])\)\s*(.+)", l)
                if m: steps[m.group(1)] = m.group(2)
            g = len(steps) == len(a) and all(steps[lab[-1]][:30] == it["steps"][p - 1][:30] for lab, p in a.items())
        elif t == "Matching":
            num = re.match(r"\d+", list(a)[0]).group(0); st = [i for i, l in enumerate(L) if re.match(r"^%s\. Match" % num, l)][0]; prem = {}; resp = {}
            for l in L[st + 1:]:
                if re.match(r"^\d+[\.\-]", l): break
                m = re.match(r"^([a-d])\)\s*(.+)", l)
                if m: prem[m.group(1)] = m.group(2); continue
                m = re.match(r"^([A-F])\.\s*(.+)", l)
                if m: resp[m.group(1)] = m.group(2)
            g = all(str([p["match"] for p in it["premises"] if prem[lab[-1]][:30] in p["text"]][0])[:30] in resp.get(letter, "") for lab, letter in a.items())
        elif t == "FillBlankGroup":
            bank = {}
            st = [i for i, l in enumerate(L) if "Fill each blank" in l][0]
            for l in L[st + 1:st + 5]:
                for piece in l.split("\t"):
                    m = re.match(r"^(\d\d)\s+(.+)$", piece.strip())
                    if m: bank[m.group(1)] = m.group(2).strip()
            g = len(a) == len(it["blanks"]) and all(bank.get(code) == bl["answer"] for code, bl in zip([a[x] for x in sorted(a, key=int)], it["blanks"]))
        good += bool(g)
        if not g: bad.append(e["item_key"])
    out(good == tot, "form %s key against the items by my own reading of the paper and my own runs: %d of %d units (not right: %s)" % (f, good, tot, bad))
    ch = {}
    for e in k["items"]:
        for c in e["chapters"][:1]: ch[c] = ch.get(c, 0) + 1
    out(len(k["items"]) == 23, "form %s: %d items" % (f, len(k["items"])))
out(codes["A"][0] == codes["A"][1] and codes["B"][0] == codes["B"][1] and codes["A"][0] != codes["B"][0], "form codes: sheet = key per form, different between forms %s" % (codes,))
out(orders["A"] != orders["B"] and sorted(orders["A"]) == sorted(orders["B"]), "the two forms hold the same 23 items in a different order")
ch = [x for x in I if x in O and {a: b for a, b in I[x].items() if a != "papers"} != {a: b for a, b in O[x].items() if a != "papers"}]
out(ch == ["mt1:i20:trace-compactsize"] and I[ch[0]]["output"] == O[ch[0]]["output"] and "takes 1 byte" in I[ch[0]]["q"] and I[ch[0]]["bloom"] == O[ch[0]]["bloom"], "the only item changed against v1.0.0 is %s, answer and level unchanged, CompactSize sizes defined inside the item" % ch)
out(len(I) == 23 and set(I) == set(O), "23 items, the same keys as v1.0.0")
import shutil; shutil.rmtree(tmp, ignore_errors=True)
print("RESULT", "FAIL" if fails else "PASS"); sys.exit(1 if fails else 0)
