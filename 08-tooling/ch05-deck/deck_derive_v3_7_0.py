#!/usr/bin/env python3
"""Chapter 5 deck v3.7.0 and deck plan v3.7.0 (NEW files; the deck v3.6.0 and the plan v3.6.0 are read, never written). ONE kind of change, the owner's Friday standard as in the Ch06 deck: the version probe
'__import__("sys").version_info[:2]' (54 occurrences: 27 code lines and 27 result rows) is removed. Each result line now shows a real expression of the example and its value, 'EXPRESSION  ->  VALUE' (the marker of
sen0401_code_marker_v1_0_0.py); the value is what Python answers: it is computed here by running the slide's listing in the chapter prelude (the way the deck check does) and the deck check re-runs it again.
The Python version stays stated by the caption 'What the run printed (python 3.14.6)'; the deck check still refuses any interpreter other than the recording's 3.14.6, so no probe is needed (the Ch06 approach).
Each code box that held the probe is one line shorter, everything below moves up by that line (the growth of v3.6.0 on slides 11, 45 and 54 is undone where the probe took it back); every other shape, text, note, chart,
picture and link stays. Usage: deck_derive_v3_7_0.py   (python3; the values are verified by the deck check under Python 3.14.6)"""
__version__ = "3.7.0"
import os, re, json, zipfile, sys, importlib.util
from xml.dom import minidom
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, ".."))
import deck_derive_v3_6_0 as D6
import sen0401_code_marker_v1_0_0 as MARK
from lxml import etree
ROOT = D6.ROOT
SRC = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_6_0.pptx")
DST = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_7_0.pptx")
PSRC = os.path.join(HERE, "deck_plan_v3_6_0.json"); PDST = os.path.join(HERE, "deck_plan_v3_7_0.json")
PROBE = '__import__("sys").version_info[:2]'
ARROW = "  →  "
EXPR = {11: "keys == again", 17: "n", 18: "shamir_combine(shares[:2]) == secret", 22: 'bin(diff).count("1")', 23: "(bits, n)", 24: 'format(idx[0], "011b")', 25: "mnemonic_to_entropy(bad)[1]",
        26: "mnemonic_to_seed(s) == mnemonic_to_seed(n)", 27: 'stretch(b"mnemonic", 2048)', 28: "addr(PASSPHRASE)[:14]", 33: 'k == int.from_bytes(left, "big")', 34: "(i, ci.hex()[:12])",
        35: "normal == hard", 36: "back == k", 37: "ec_mul(k5) == K5", 38: 'parse_extended(xpub)["depth"]', 39: "len(range(HARD, 2 * HARD))", 44: "sum(i >= HARD for i in idx)",
        45: "(a44[0], a86[:4])", 46: "addr == published", 47: "Q.hex()[:12]", 49: "descsum_create(multi)[-8:]", 54: "len(rows)", 58: "p2wpkh_address(ser_p(Ki))[:12]",
        59: "len(found)", 60: "ecdsa_verify(pub, z2, sig)", 62: 'first(B84.replace("about", "above")) == noted'}

def prelude():
    f = os.path.join(HERE, "examples_v1_2_0.py"); sys.path.insert(0, HERE)
    spec = importlib.util.spec_from_file_location("sen0401_examples", f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.PRELUDE

def values(z, PRE):
    out = {}
    for n in range(1, 69):
        d = minidom.parseString(z.read("ppt/slides/slide%d.xml" % n)); listing, rows = MARK.form2(MARK.xml_shapes(d))
        if not rows: continue
        ns = {}; exec(PRE, ns); exec(listing, ns); out[n] = repr(eval(EXPR[n], ns))
    assert sorted(out) == sorted(EXPR), (sorted(out), sorted(EXPR))
    return out

def transform(n, xml, val):
    root = etree.fromstring(xml); A = D6.A; NS = D6.NSMAP; boxes = [e for e in root.iter(D6.q("p:sp")) if e.find("p:nvSpPr/p:cNvPr", NS).get("name", "").startswith("code ")]
    hit = []
    for sp in boxes:
        for p in sp.findall("p:txBody/a:p", NS):
            if "".join(t.text for t in p.iter(A + "t")) == PROBE: hit.append((sp, p))
    assert len(hit) == 1, (n, len(hit)); sp, p = hit[0]
    paras = sp.findall("p:txBody/a:p", NS); assert len(paras) >= 2 and paras[-1] is p
    off, ext = D6.xfrm(sp); h = int(ext.get("cy")); pl = int(round((h - 2 * 36576) / len(paras)))
    sp.find("p:txBody", NS).remove(p); name = sp.find("p:nvSpPr/p:cNvPr", NS).get("name")
    res = D6.byname(root, "result line " + name.split()[-1]); assert len(res) == 1
    D6.settext(res[0], EXPR[n] + ARROW + val, PROBE + ARROW + "(3, 14)")
    top = int(off.get("y")); d_eff = pl
    for e in D6.byname(root, "explanation"):
        eo, ee = D6.xfrm(e)
        if int(eo.get("y")) == top:   # the explanation beside the box keeps the height its text needs (estimate: 0.095 in per character, 0.2 in per line, 0.1 in of insets)
            txt = "".join(t.text for t in e.iter(A + "t")); cpl = max(1, int((int(ee.get("cx")) / 914400 - 0.16) / 0.095)); need = int((-(-len(txt) // cpl) * 0.2 + 0.1) * 914400)
            d_eff = max(0, min(pl, int(ee.get("cy")) - need))
    lowest = D6.grow_below(root, name, -d_eff); ext.set("cy", str(h - pl))
    # the result shape stands directly under the shortened box
    roff = D6.xfrm(res[0])[0]; roff.set("y", str(top + h - pl))
    tk = D6.byname(root, "takeaway")[0]; tko = D6.xfrm(tk)[0]
    if lowest + 18288 <= 4517136: tko.set("y", "4517136")
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True), len(EXPR[n] + ARROW + val)

if __name__ == "__main__":
    zi = zipfile.ZipFile(SRC); vals = values(zi, prelude()); longest = 0
    with zipfile.ZipFile(DST, "w") as zo:
        for it in zi.infolist():
            data = zi.read(it.filename); m = re.fullmatch(r"ppt/slides/slide(\d+)\.xml", it.filename)
            if m and int(m.group(1)) in EXPR:
                n = int(m.group(1)); data, w = transform(n, data, vals[n]); longest = max(longest, w); print("slide %d  %s%s%s" % (n, EXPR[n], ARROW, vals[n]))
            elif it.filename == "docProps/core.xml":
                s = data.decode("utf-8"); assert "deck v3.6.0" in s; data = s.replace("deck v3.6.0", "deck v3.7.0").encode("utf-8")
            zo.writestr(it, data, compress_type=it.compress_type)
    p = json.load(open(PSRC, encoding="utf-8")); p["meta"]["version"] = "3.7.0"
    json.dump(p, open(PDST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("longest result line: %d characters" % longest); print("written", DST); print("written", PDST)
