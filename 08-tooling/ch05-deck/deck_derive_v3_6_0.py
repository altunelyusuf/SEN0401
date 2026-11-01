#!/usr/bin/env python3
"""Chapter 5 deck v3.6.0 and deck plan v3.6.0 (NEW files; the deck v3.5.0 and the plan v3.5.0 are read, never written). The teaching enhancement of the owner's Friday standard, in this order:
(1) the three true stories (slides 5, 20, 56) are told as sentences with real names, dates and places: the six label rows (WHO, WHAT, ...) are replaced by three story cards ('story 1..3'); picture, credit and live link stay;
(2) the two slides whose code used the word lambda (11, 45) say the same with def (the rule is a function, body on its own indented line); the code of slides 11 and 60 called sha256_hex, a helper only the page defines, so it calls hashlib.sha256(...).hexdigest() (the chapter prelude of the deck check has no sha256_hex);
(3) slide 54: the one-line compound statement 'for r in rows: print(...)' becomes two lines (same code, indented body); the boxes below move down by that one line;
(4) the 19 code slides that had no reading of their result get a one-line reading ('reading') on the row of the result label; the 8 that had one keep it;
(5) every slide gets short speaker notes with clues (deck_notes_v3_6_0.py);
(6) every result line reads 'EXPRESSION  →  VALUE' (the marker of sen0401_code_marker_v1_0_0.py: the expression is re-run by the deck check and must equal the value); (7) slide 2: the counter label names real names, dates and places instead of the label words.
Slides are not added or removed, so every slide number stays. Code boxes, shape names 'code N' and 'result line N', results, charts, tables, pictures, links stay. docProps/core.xml names v3.6.0. Usage: deck_derive_v3_6_0.py"""
__version__ = "3.6.0"
import os, re, json, zipfile, copy, sys
sys.dont_write_bytecode = True
from lxml import etree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_notes_v3_6_0 as NT
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_5_0.pptx")
DST = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_6_0.pptx")
PSRC = os.path.join(HERE, "deck_plan_v3_5_0.json")
PDST = os.path.join(HERE, "deck_plan_v3_6_0.json")
NSMAP = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main", "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
A = "{%s}" % NSMAP["a"]
ACC, INK, CARD = "2F6D62", "2B2622", "F2ECE1"

STORIES = {
    5: {"sub": "A true story, with real names, dates and places",
        "cards": ["In 2011 **Stefan Thomas**, a programmer and former Ripple technology chief, was paid **7,002 bitcoin** and kept the keys on an IronKey USB drive in a safe.",
                  "He lost the paper with the password. On **12 January 2021** reporter **Nathaniel Popper** told the story in the New York Times: eight of ten guesses were already used.",
                  "The drive locks forever after ten wrong guesses, and memory was his only backup. A recovery code, tested in advance, is the alternative."]},
    20: {"sub": "A true story, with real names, dates and places",
         "cards": ["**Marek Palatinus** and **Pavol Rusnak** of SatoshiLabs, the makers of Trezor, saw that nobody transcribes 128 raw bits correctly. **Aaron Voisine** and **Sean Bowe** joined them.",
                   "On **10 September 2013** they published **BIP 39** in the public bips repository on GitHub: a way to write entropy as ordinary words.",
                   "The recipe is 2,048 words of eleven bits each, a checksum folded in, and key stretching from the words to the seed."]},
    56: {"sub": "A true story, with real names, dates and places",
         "cards": ["On **21 March 2014**, three weeks after the bankruptcy filing, **Mark Karpeles**, chief executive of Mt. Gox, said the exchange had found about **200,000 BTC**.",
                   "**Simon Sharwood** of The Register reported it. The coins sat in an old-format wallet file that the company believed was empty and had never checked.",
                   "A file made by software two generations older still held spendable keys. Wallet files hold keys forever."]},
}
READING = {11: "Same seed, same three keys: one backup is enough.",
           17: "codex32 checks by checksum, Electrum by an HMAC prefix.",
           18: "Any three shares give True; two shares give False.",
           25: "Right code: checksum True. One word changed: False.",
           26: "Both spellings give one seed after normalising.",
           27: "Rounds or salt change, and the result is unrelated.",
           28: "Two passphrases give two different wallet addresses.",
           34: "Each index gives its own key and its own chain code.",
           35: "Index 2147483648 is hardened and gives a different key.",
           37: "Both routes end at the same public key: True.",
           38: "Both keys are 111 characters; xprv spends, xpub watches.",
           45: "Four purposes give a 1, 3, bc1q and bc1p address.",
           46: "Our address equals the published one: True.",
           47: "The tweak changes the key; the address shows the new one.",
           49: "The checksum and the key origin are computed from the text.",
           54: "One JSON line per label: an address and a transaction.",
           58: "Three customers get three different addresses.",
           60: "Verification is True for the signed message only.",
           62: "A single wrong word gives a different wallet: False."}
VERSION_EXPR = '__import__("sys").version_info[:2]'
STAT_OLD, STAT_NEW = "true stories, told as who, what, when, where, why, how", "true stories with real names, dates and places"
SUB_OLD = "A true story, told as who, what, when, where, why and how"

def q(tag): p, t = tag.split(":"); return "{%s}%s" % (NSMAP[p], t)
def byname(root, name): return [sp for sp in root.iter(q("p:sp")) if sp.find("p:nvSpPr/p:cNvPr", NSMAP).get("name") == name]
def xfrm(sp): return sp.find("p:spPr/a:xfrm/a:off", NSMAP), sp.find("p:spPr/a:xfrm/a:ext", NSMAP)
def settext(sp, new, old=None):
    ts = list(sp.iter(A + "t")); assert len(ts) == 1, [t.text for t in ts]
    if old is not None: assert ts[0].text == old, ts[0].text
    ts[0].text = new
def maxid(root): return max(int(e.get("id")) for e in root.iter() if e.tag == q("p:cNvPr"))

def run(text, bold=False, color=INK, size=1250, italic=False):
    return ('<a:r><a:rPr lang="en-US" sz="%d" b="%d" i="%d"><a:solidFill><a:srgbClr val="%s"/></a:solidFill><a:latin typeface="Calibri"/></a:rPr><a:t>%s</a:t></a:r>'
            % (size, bold, italic, color, text.replace("&", "&amp;").replace("<", "&lt;")))

def story_card(i, k, text, x, y, w, h):
    parts = text.split("**"); runs = "".join(run(t, bold=(n % 2 == 1), color=ACC if n % 2 == 1 else INK) for n, t in enumerate(parts) if t)
    xml = ('<p:sp xmlns:p="%s" xmlns:a="%s"><p:nvSpPr><p:cNvPr id="%d" name="story %d"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
           '<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 8000"/></a:avLst></a:prstGeom><a:solidFill><a:srgbClr val="%s"/></a:solidFill><a:ln><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln></p:spPr>'
           '<p:txBody><a:bodyPr rtlCol="0" anchor="ctr" wrap="square" lIns="118872" rIns="118872" tIns="45720" bIns="45720"/><a:lstStyle/><a:p><a:pPr algn="l"/>%s</a:p></p:txBody></p:sp>'
           % (NSMAP["p"], NSMAP["a"], i, k, x, y, w, h, CARD, CARD, runs))
    return etree.fromstring(xml)

def do_story(root, n):
    st = STORIES[n]; rows = byname(root, "5N1K row"); labs = byname(root, "5N1K label"); txs = byname(root, "5N1K text")
    assert len(rows) == len(labs) == len(txs) == 6
    off0, ext0 = xfrm(rows[0]); x, w, y0 = int(off0.get("x")), int(ext0.get("cx")), int(off0.get("y"))
    first = rows[0]; parent = first.getparent(); pos = list(parent).index(first)
    for sp in rows + labs + txs: parent.remove(sp)
    h, gap = 914400, 91440; nid = maxid(root)
    for k, text in enumerate(st["cards"], 1):
        nid += 1; parent.insert(pos + k - 1, story_card(nid, k, text, x, y0 + (k - 1) * (h + gap), w, h))
    subs = byname(root, "subtitle"); assert len(subs) == 1; settext(subs[0], st["sub"], SUB_OLD)

DEF = "FFA657"; DFLT = "E6EDF3"; NUM = "79C0FF"
def code_run(t, color=DFLT):
    return etree.fromstring('<a:r xmlns:a="%s"><a:rPr sz="1050" b="0" i="0"><a:solidFill><a:srgbClr val="%s"/></a:solidFill><a:latin typeface="Courier New"/></a:rPr><a:t xml:space="preserve">%s</a:t></a:r>' % (NSMAP["a"], color, t))
def code_para(parts):
    p = etree.fromstring('<a:p xmlns:a="%s"><a:pPr algn="l"/></a:p>' % NSMAP["a"])
    for t, c in parts: p.append(code_run(t, c))
    return p
def children_top(el):
    for path in ("p:spPr/a:xfrm/a:off", "p:xfrm/a:off", "p:grpSpPr/a:xfrm/a:off"):
        o = el.find(path, NSMAP)
        if o is not None: return o
def grow_below(root, boxname, d, keep=("takeaway", "source", "slide number", "chip", "subtitle")):
    """the code box 'boxname' (and its explanation beside it) grows by d; every shape below it moves down by d; the takeaway moves down only as far as needed"""
    tree = root.find(".//p:cSld/p:spTree", NSMAP); box = byname(root, boxname)[0]; off, ext = xfrm(box); top, h = int(off.get("y")), int(ext.get("cy"))
    ext.set("cy", str(h + d)); lowest = 0
    for el in tree:
        if el.tag == q("p:nvGrpSpPr") or el.tag == q("p:grpSpPr") or el is box: continue
        o = children_top(el)
        if o is None: continue
        nm = el.find(".//p:cNvPr", NSMAP).get("name", "")
        y = int(o.get("y"))
        if nm == "explanation" and y == top:
            e = el.find("p:spPr/a:xfrm/a:ext", NSMAP); e.set("cy", str(int(e.get("cy")) + d)); continue
        if nm in keep or nm == "Title 1" or y <= top: continue
        o.set("y", str(y + d))
        e = el.find("p:spPr/a:xfrm/a:ext", NSMAP)
        if e is None: e = el.find("p:xfrm/a:ext", NSMAP)
        if e is None: e = el.find("p:grpSpPr/a:xfrm/a:ext", NSMAP)
        if nm not in ("result label", "reading"): lowest = max(lowest, y + d + int(e.get("cy")))
    tk = byname(root, "takeaway")[0]; to, te = xfrm(tk)
    need = lowest + 18288 - int(to.get("y"))
    if need > 0: to.set("y", str(int(to.get("y")) + min(need, 137160)))
    return lowest

DEFS = {11: ("code 1", 1, [[("def", DEF), (" key(i):", DFLT)], [("    ", DFLT), ("return", DEF), (" hashlib.sha256(seed + bytes([i])).hexdigest()", DFLT)]]),
        45: ("code 1", 0, [[("def", DEF), (" pub(p):", DFLT)], [("    ", DFLT), ("return", DEF), (" ser_p(ec_mul(keys_at(B84, p)[", DFLT), ("0", NUM), ("]))", DFLT)]])}
def do_def(root, n):
    nm, idx, new = DEFS[n]; sp = byname(root, nm)[0]; paras = sp.findall("p:txBody/a:p", NSMAP); old = paras[idx]
    assert "lambda" in "".join(t.text for t in old.iter(A + "t"))
    for k, np_ in enumerate(new): old.addprevious(code_para(np_))
    sp.find("p:txBody", NSMAP).remove(old)
    h = int(xfrm(sp)[1].get("cy")); d = int(round((h - 2 * 36576) / len(paras)))
    return grow_below(root, nm, d)

def do_sha60(root):
    n = 0
    for sp in byname(root, "code 2") + byname(root, "code 3"):
        for par in sp.findall("p:txBody/a:p", NSMAP):
            rs = par.findall("a:r", NSMAP); tx = [r.find("a:t", NSMAP) for r in rs]
            if "sha256_hex" in [t.text for t in tx]:
                i = [t.text for t in tx].index("sha256_hex"); tx[i].text = "hashlib.sha256"
                j = next(k for k in range(i + 1, len(tx)) if tx[k].text == ")"); tx[j].text = ").hexdigest()"; n += 1
    assert n == 2, n
    return n

def do_reading(root, n):
    lab = byname(root, "result label"); assert len(lab) == 1 and not byname(root, "reading")
    off, ext = xfrm(lab[0]); y, h = int(off.get("y")), int(ext.get("cy")); nid = maxid(root) + 1
    xml = ('<p:sp xmlns:p="%s" xmlns:a="%s"><p:nvSpPr><p:cNvPr id="%d" name="reading"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="4526280" y="%d"/><a:ext cx="4297680" cy="%d"/></a:xfrm>'
           '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" anchor="t" lIns="45720" rIns="45720" tIns="36576" bIns="36576"><a:spAutoFit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/>%s</a:p></p:txBody></p:sp>'
           % (NSMAP["p"], NSMAP["a"], nid, y, h, run(READING[n], color=INK, size=1100, italic=True)))
    lab[0].addnext(etree.fromstring(xml))

def do_split54(root):
    code2 = [s for s in byname(root, "code 2")]; assert len(code2) == 1; sp = code2[0]
    paras = sp.findall("p:txBody/a:p", NSMAP); tgt = [p for p in paras if "".join(t.text for t in p.iter(A + "t")) == "for r in rows: print(json.dumps(r))"]; assert len(tgt) == 1; p1 = tgt[0]
    p2 = copy.deepcopy(p1); runs1 = p1.findall("a:r", NSMAP); texts = [r.find("a:t", NSMAP).text for r in runs1]
    ci = texts.index(":"); assert texts[ci + 1] == " " and texts[ci + 2] == "print"
    for r in runs1[ci + 1:]: p1.remove(r)
    runs2 = p2.findall("a:r", NSMAP)
    for r in runs2[:ci + 2]: p2.remove(r)
    ind = copy.deepcopy(runs1[ci]); ind.find("a:t", NSMAP).text = "    "
    p2.insert(1, ind); p1.addnext(p2)
    off, ext = xfrm(sp); h = int(ext.get("cy")); total = len(paras) - 1  # code lines after the move are one more: line height from the old box
    pl = (h - 2 * 36576) / len(paras); d = int(round(pl))
    ext.set("cy", str(h + d))
    for nm in ("result line 2", "result label", "result table"):
        for e in byname(root, nm) or [g for g in root.iter(q("p:graphicFrame")) if g.find("p:nvGraphicFramePr/p:cNvPr", NSMAP).get("name") == nm]:
            o = e.find("p:spPr/a:xfrm/a:off", NSMAP) if e.tag == q("p:sp") else e.find("p:xfrm/a:off", NSMAP)
            o.set("y", str(int(o.get("y")) + d))
    for e in byname(root, "explanation"):
        o, x = xfrm(e)
        if int(o.get("y")) == int(off.get("y")): x.set("cy", str(int(x.get("cy")) + d))
    return d

def transform(name, xml):
    n = int(re.search(r"slide(\d+)\.xml", name).group(1)); root = etree.fromstring(xml); did = []
    if n in STORIES: do_story(root, n); did.append("story")
    if n in DEFS: do_def(root, n); did.append("def")
    if n == 60: do_sha60(root); did.append("sha60")
    if n == 54: did.append("split+%d" % do_split54(root))
    if n in READING: do_reading(root, n); did.append("reading")
    for sp in [e for e in root.iter(q("p:sp")) if e.find("p:nvSpPr/p:cNvPr", NSMAP).get("name", "").startswith("result line ")]:
        settext(sp, VERSION_EXPR + "  \u2192  (3, 14)", "(3, 14)"); did.append("result")
    if n == 2:
        for sp in byname(root, "stat label"):
            if "".join(t.text for t in sp.iter(A + "t")) == STAT_OLD: settext(sp, STAT_NEW); did.append("stat")
    return (etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True) if did else xml), did

def notes_for(z):
    out = {}
    for n in range(1, 69):
        rel = z.read("ppt/slides/_rels/slide%d.xml.rels" % n).decode()
        m = re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', rel); out["ppt/notesSlides/" + m.group(1)] = n
    return out

if __name__ == "__main__":
    zi = zipfile.ZipFile(SRC); nmap = notes_for(zi); log = {}
    with zipfile.ZipFile(DST, "w") as zo:
        for it in zi.infolist():
            data = zi.read(it.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", it.filename):
                data, did = transform(it.filename, data)
                if did: log[it.filename] = did
            elif it.filename in nmap:
                root = etree.fromstring(data); ts = []
                for sp in root.iter(q("p:sp")):
                    ph = sp.find("p:nvSpPr/p:nvPr/p:ph", NSMAP)
                    if ph is not None and ph.get("type") == "body": ts = list(sp.iter(A + "t"))
                assert len(ts) == 1; ts[0].text = NT.NOTES[nmap[it.filename]]
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            elif it.filename == "docProps/core.xml":
                s = data.decode("utf-8"); assert "deck v3.5.0" in s; data = s.replace("deck v3.5.0", "deck v3.6.0").encode("utf-8")
            zo.writestr(it, data, compress_type=it.compress_type)
    p = json.load(open(PSRC, encoding="utf-8")); p["meta"]["version"] = "3.6.0"
    for i, s in enumerate(p["slides"], 1):
        s["notes"] = NT.NOTES[i]
        if i in STORIES:
            s["sub"] = STORIES[i]["sub"]
            s["items"] = [({**it, "render": "story cards (sentences, no label words)", "cards": [c.replace("**", "") for c in STORIES[i]["cards"]]} if it.get("t") == "factrow" else it) for it in s["items"]]
        if i in READING: s["items"].append({"t": "reading", "text": READING[i]})
    json.dump(p, open(PDST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k in sorted(log, key=lambda s: int(re.search(r"(\d+)", s).group(1))): print(k, log[k])
    print("notes written for %d slides" % len(nmap)); print("written", DST); print("written", PDST)
