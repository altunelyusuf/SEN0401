#!/usr/bin/env python3
"""sen0401_ch13_standard_fix v1.0.0 - writes the next Chapter 13 set beside the committed one (nothing existing is edited):
  library 1.1.0 wheel (03-materials/ch13/assets), manifest chapter_code_ch13_v1_3_0.json, deck v2_5_0, page v9_97_0 (+ page data json).
Rules applied (owner rulings up to 2026-11-24): code frames without prompts, results in the visual not in the frame, no lambda, code frame and page code identical, notes of 60 to 140 reader-facing words,
titles of at least four words, something to look at on every slide, no everyday comparison anywhere, "Run slide code" as a top menu item, lab library with Bitcoin Core and BIP references.
Usage: python3 sen0401_ch13_standard_fix_v1_0_0.py   (then: group step, office_stamp, checks - see the run script lines at the end of the file)"""
__version__ = "1.0.0"
import base64, copy, glob, hashlib, io, json, os, re, sys, zipfile
from lxml import etree
from pptx import Presentation
from pptx.util import Emu, Pt

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
M = os.path.join(REPO, "03-materials", "ch13"); PG = os.path.join(M, "page"); AS = os.path.join(M, "assets")
sys.path.insert(0, HERE)
import sen0401_ch13_notes_v1_0_0 as N
E = 914400
TMP = sys.argv[1] if len(sys.argv) > 1 else "/tmp/c13/stage1.pptx"

# ------------------------------------------------------------------ 1. library: the references are passages of the saved sources
EV = os.path.join(HERE, "ch13-evidence")
ANCHORS = [("bip-0032.mediawiki", 'Key = "Bitcoin seed"'), ("bip-0039.mediawiki", "PBKDF2"), ("bip-0039.mediawiki", "2048"), ("bip-0093.mediawiki", "Shamir"),
           ("core_src_wallet_crypter.h", "DEFAULT_DERIVE_ITERATIONS = 25000"), ("core_src_kernel_chainparams.cpp", "CreateGenesisBlock"), ("core_src_kernel_chainparams.cpp", "defaultAssumeValid"),
           ("bip-0068.mediawiki", "0x0000ffff"), ("core_src_script_interpreter.cpp", "nLockTimeMask"), ("core_src_script_interpreter.cpp", "CheckSequence"), ("bitcoind_help_31.1.txt", "-assumevalid")]
for f, frag in ANCHORS:
    assert re.sub(r"\s+", " ", frag) in re.sub(r"\s+", " ", open(os.path.join(EV, f), errors="replace").read()), (f, frag)
print("library references checked against the saved sources:", len(ANCHORS))
LIB = "sen0401_ch13_lib_v1_1_0"; OLDLIB = "sen0401_ch13_lib_v1_0_0"
WHL_OLD = os.path.join(AS, "sen0401_ch13_lib-1.1.0-py3-none-any.whl"); WHL = os.path.join(AS, "sen0401_ch13_lib-1.2.0-py3-none-any.whl")
files = [(LIB + ".py", open(os.path.join(HERE, LIB + ".py"), "rb").read())]
with zipfile.ZipFile(WHL_OLD) as z:
    for n in z.namelist():
        if n.endswith(OLDLIB + ".py") or n.endswith(".dist-info/METADATA") or n.endswith(".dist-info/WHEEL") or n.endswith(".dist-info/RECORD"): continue
        files.append((n, z.read(n)))
dist = "sen0401_ch13_lib-1.2.0.dist-info/"
files.append((dist + "METADATA", b"Metadata-Version: 2.1\nName: sen0401-ch13-lib\nVersion: 1.2.0\nSummary: The chapter 13 (Bitcoin Security) library of the SEN0401 course with the saved files its worked examples read.\n"))
files.append((dist + "WHEEL", b"Wheel-Version: 1.0\nGenerator: sen0401_ch13_standard_fix_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"))
h64 = lambda b: "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode()
rec = "".join("%s,%s,%d\n" % (n, h64(b), len(b)) for n, b in files) + dist + "RECORD,,\n"
files.append((dist + "RECORD", rec.encode()))
if os.path.exists(WHL): os.remove(WHL)
with zipfile.ZipFile(WHL, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in files:
        zi = zipfile.ZipInfo(n, (2026, 11, 24, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, b)
WHL_BYTES = open(WHL, "rb").read(); WHL_SHA = hashlib.sha256(WHL_BYTES).hexdigest()
print("wheel", os.path.basename(WHL), len(WHL_BYTES), WHL_SHA[:16])

# ------------------------------------------------------------------ 2. manifest 1.3.0
man = json.load(open(os.path.join(PG, "chapter_code_ch13_v1_2_0.json"), encoding="utf-8"))
NEW5 = ("mr = '4a5e1e4baab89f3a32518a88c31bc87f'\nmr += '618f76673e2cc77ab2127b7afdeda33b'\ndef le(n):\n    return n.to_bytes(4, 'little')\n"
        "hdr = le(1) + bytes(32) + bytes.fromhex(mr)[::-1]\nhdr += le(1231006505) + le(0x1d00ffff) + le(2083236893)\n"
        "first = hashlib.sha256(hdr).digest()\nh = hashlib.sha256(first).digest()[::-1].hex()\nfound = seen('core_src_kernel_chainparams.cpp', h)\n(len(hdr), h[:20], found)")
NEW20 = ("schemes = ((1, 1), (2, 3), (1, 3))\ndef lose(m, n):\n    return round(L.p_lose(0.1, m, n), 4)\nstuck = [lose(m, n) for m, n in schemes]\n"
         "def rob(m, n):\n    return round(L.p_theft(0.05, m, n), 5)\nrobbed = [rob(m, n) for m, n in schemes]\n(stuck, robbed)")
GROUPS_NEW = {12: [2, 4, 4], 36: [1, 3, 4]}        # lines per code frame of the two rebuilt slides
for e in man["examples"]:
    if e["slide"] == 12: e["code"] = NEW5
    if e["slide"] == 36: e["code"] = NEW20
man["manifest"] = "chapter_code_ch13_v1_3_0"; man["deck"] = "SEN0401_Ch13_BitcoinSecurity_3e_v2_5_0.pptx"; man["deck_version"] = "2.5.0"
man["library"] = {"module": "sen0401_ch13_lib", "file": "03-materials/ch13/assets/sen0401_ch13_lib-1.2.0-py3-none-any.whl", "sha256": WHL_SHA,
                  "modules": [LIB, "sen0401_ch10_p2p_v1_0_0"], "import": "import %s as L; R = L.run(); seen = L.has" % LIB}
man["setup"]["code"] = man["setup"]["code"].replace(OLDLIB, LIB)
# every example is executed here, with the new library, and must give its recorded expected values
import importlib
L = importlib.import_module(LIB); R = L.run(); seen = L.has
bad = []
for e in man["examples"]:
    ns = {"L": L, "R": R, "seen": seen, "hashlib": hashlib, "math": __import__("math")}
    exec(e["code"], ns)
    for sh in e["show"]:
        got = repr(eval(sh["expression"], ns))
        if got != sh["expected"]: bad.append((e["id"], sh["expression"], got, sh["expected"]))
assert not bad, bad
print("manifest examples executed with the new library:", len(man["examples"]), "all expected values equal")
man_p = os.path.join(PG, "chapter_code_ch13_v1_3_0.json")
json.dump(man, open(man_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ 3. deck
SRC = os.path.join(M, "SEN0401_Ch13_BitcoinSecurity_3e_v2_4_0.pptx")
prs = Presentation(SRC)
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
def courier(sh): return sh.has_text_frame and any(r.font.name == "Courier New" for p in sh.text_frame.paragraphs for r in p.runs)
def W(t): return len(t.split())
KW = {"def", "return", "for", "in", "if", "else", "import", "from", "as", "not", "and", "or", "True", "False", "None"}
TOK = re.compile(r"(?P<str>'[^']*'|\"[^\"]*\")|(?P<num>\b0x[0-9a-fA-F]+\b|\b\d+(?:\.\d+)?\b)|(?P<kw>\b[A-Za-z_]+\b)|(?P<cm>#.*)")
COL = {"txt": "E6EDF3", "str": "9ECBFF", "kw": "F2A860", "num": "FFD28A", "cm": "8FB996"}
def set_code(sh, lines):
    """write the lines of one code frame with the palette of the course (text E6EDF3, strings 9ECBFF, keywords F2A860 bold, numbers FFD28A)"""
    tf = sh.text_frame; ps = tf.paragraphs
    tmpl = copy.deepcopy([r for r in ps[0].runs if r.font.name == "Courier New"][-1]._r)
    body = tf._txBody
    for p in list(body.findall(A + "p")): body.remove(p)
    for line in lines:
        p = etree.SubElement(body, A + "p"); ppr = etree.SubElement(p, A + "pPr"); ppr.set("indent", "0"); ppr.set("marL", "0"); etree.SubElement(ppr, A + "buNone")
        pos = 0; parts = []
        for m in TOK.finditer(line):
            if m.start() > pos: parts.append((line[pos:m.start()], "txt"))
            g = m.lastgroup; tx = m.group(0)
            parts.append((tx, "kw" if g == "kw" and tx in KW else ("txt" if g == "kw" else g))); pos = m.end()
        if pos < len(line): parts.append((line[pos:], "txt"))
        merged = []
        for tx, k in parts:
            if merged and merged[-1][1] == k: merged[-1] = (merged[-1][0] + tx, k)
            else: merged.append((tx, k))
        for tx, k in merged:
            r = copy.deepcopy(tmpl); r.find(A + "t").text = tx
            rpr = r.find(A + "rPr")
            rpr.find(A + "solidFill").find(A + "srgbClr").set("val", COL[k])
            if k == "kw": rpr.set("b", "1")
            elif "b" in rpr.attrib: del rpr.attrib["b"]
            p.append(r)

code_slides = sorted({e["slide"] for e in man["examples"]})
codes = {e["slide"]: [l for l in e["code"].split("\n")] for e in man["examples"]}
for sn in code_slides:
    s = prs.slides[sn - 1]; sh_ = list(s.shapes)
    frames = sorted([x for x in sh_ if courier(x)], key=lambda x: x.top)
    rects = sorted([x for x in sh_ if x.shape_type == 1 and x.has_text_frame is not None and x.fill.type == 1 and str(x.fill.fore_color.rgb) == "23272E"], key=lambda x: x.top)
    dots = sorted([x for x in sh_ if x.shape_type == 1 and str(x.fill.fore_color.rgb) == "D97A14" and abs(x.width - 237744) < 5000], key=lambda x: x.top) if False else []
    dots = sorted([x for x in sh_ if x.shape_type == 1 and x.fill.type == 1 and str(x.fill.fore_color.rgb) == "D97A14" and abs(x.width - 237744) < 5000], key=lambda x: x.top)
    nums = sorted([x for x in sh_ if x.has_text_frame and abs(x.width - 237744) < 5000 and x.text_frame.text.strip().isdigit()], key=lambda x: x.top)
    balloons = sorted([x for x in sh_ if x.has_text_frame and not courier(x) and abs(x.left - 731520) < 20000 and abs(x.width - 4800600) < 20000], key=lambda x: x.top)
    notes_ = [x for x in sh_ if x.has_text_frame and x.text_frame.text.startswith("run under")]
    n = len(frames); assert n == len(rects) == len(dots) == len(nums) == len(balloons) and len(notes_) == 1, (sn, n, len(rects), len(dots), len(nums), len(balloons))
    # the lines of every frame: no prompt, no output line
    want = codes[sn]; got = []; per = []
    for fr in frames:
        keep = []
        for p in fr.text_frame.paragraphs:
            t = p.text
            if t.startswith(">>> "): keep.append(t[4:])
        per.append(keep); got += keep
    if sn in GROUPS_NEW:
        assert sum(GROUPS_NEW[sn]) == len(want) and len(GROUPS_NEW[sn]) == n, sn
        i0 = 0; per = []
        for k in GROUPS_NEW[sn]: per.append(want[i0:i0 + k]); i0 += k
        for fr, ln in zip(frames, per): set_code(fr, ln)
    else:
        assert got == want, (sn, got, want)
        for fr, ln in zip(frames, per):
            ps = fr.text_frame.paragraphs; k = 0
            for p in list(ps):
                if p.text.startswith(">>> "):
                    r0 = p.runs[0]; assert r0.text == ">>> ", (sn, r0.text); p._p.remove(r0._r)
                else: fr.text_frame._txBody.remove(p._p)
    # the new layout: box height 0.16 + 0.18 per line, the explanation 0.03 below its box, 0.09 between the explanation and the next box
    y = rects[0].top
    for k in range(n):
        nl = len(per[k]); h = int(round((0.16 + 0.18 * nl) * E))
        rects[k].top = y; rects[k].height = h; frames[k].top = y + int(0.08 * E); frames[k].height = h - int(0.14 * E)
        dots[k].top = y - int(0.08 * E); nums[k].top = y - int(0.08 * E)
        balloons[k].top = y + h + int(0.03 * E); y = balloons[k].top + balloons[k].height + int(0.09 * E)
        frames[k].name = "code %d" % (k + 1); rects[k].name = "Code box %d" % (k + 1)
    notes_[0].top = balloons[n - 1].top + balloons[n - 1].height + int(0.05 * E)
    assert notes_[0].top + notes_[0].height < int(5.0 * E), (sn, notes_[0].top / E)

# ---- text: titles, the cards, the dividers, no everyday comparison
def set_text(sh, text, para=None):
    ps = sh.text_frame.paragraphs; p = ps[0] if para is None else ps[para]
    rs = p.runs; rs[0].text = text
    for r in rs[1:]: p._p.remove(r._r)
NEWSUB = N.SUB_NEW; BOT = N.BOT_NEW
def S(i): return prs.slides[i - 1]
def by(i, name): return [x for x in S(i).shapes if x.name == name][0]
CARD = {  # (slide, shape name) -> the line that names the slide which shows the idea
    (6, "Text 7"): "Slides 7 to 10 show what a signature protects.", (6, "Text 11"): "Slides 12 to 14 show checks that start from typed-in values.",
    (6, "Text 15"): "Slide 14 shows a hash and a signature that check a download.", (6, "Text 19"): "Slide 12 shows a block hash typed into the software.",
    (8, "Text 7"): "Slide 12 shows a block hash typed into the software.", (8, "Text 11"): "Slides 12 and 13 show that every node starts from the same typed-in hash.",
    (8, "Text 15"): "Slide 13 shows the shortcut that skips old signature checks.", (8, "Text 19"): "Slide 12 rebuilds its hash from the 80-byte header.",
    (16, "Text 7"): "Slides 17 to 25 show the practices as recorded runs.", (16, "Text 11"): "Slides 28 and 29 show why backups are repeated.",
    (16, "Text 15"): "Slides 21 and 22 show a device that keeps the key inside.",
    (18, "Text 7"): "Slides 21 and 22 show a device that makes a thief wait.", (18, "Text 11"): "Slides 17 and 19 show an offline signer and an online watcher.",
    (18, "Text 15"): "Slides 30 and 31 turn the seed words into a seed.",
    (27, "Text 7"): "Slides 28 and 29 show what a stale backup misses.", (27, "Text 11"): "Slide 28 compares an early and a late backup.",
    (27, "Text 15"): "Slide 30 builds twelve words from random bytes.", (27, "Text 19"): "Slides 31 and 32 turn words into a seed and a master key.",
    (34, "Text 7"): "Slide 36 compares the chances of loss and theft.", (34, "Text 11"): "Slide 36 computes the chances for 1-of-1, 2-of-3 and 1-of-3.",
    (34, "Text 15"): "Slide 35 shows a recorded 2-of-3 spend.", (34, "Text 19"): "Slide 37 compares the size of the spends in bytes.",
    (43, "Text 7"): "Slide 20 compares a hot wallet with cold storage.",
    (49, "Text 7"): "Slides 50 and 51 show a timelock that lets an heir spend later.", (49, "Text 11"): "Slide 50 shows the owner spending at once and the heir after ten blocks.",
}
DIV = {
    (5, "Text 3"): "A node trusts only what it can check by itself: signatures, hashes and rules.", (5, "Text 7"): "Slide 7 shows the 222 recorded bytes of a payment.",
    (5, "Text 11"): "Slide 11 shows two peers with one session identifier.", (5, "Text 15"): "Slide 12 rebuilds the first block's hash from its header.",
    (5, "Text 19"): "Slide 14 compares a hash with a published list.",
    (15, "Text 3"): "Keys are kept where thieves cannot reach them: offline, locked or in a device.", (15, "Text 7"): "Slide 19 passes one file between two machines.",
    (15, "Text 11"): "Slides 24 and 25 show what a lock stops.", (15, "Text 15"): "Slide 21 shows waits that double after each wrong PIN.", (15, "Text 19"): "Slide 23 times the guessing of a few words.",
    (26, "Text 3"): "Access survives loss through a backup that is repeated after changes.", (26, "Text 7"): "Slides 30 to 32 turn twelve words into a master key.",
    (26, "Text 11"): "Slides 28 and 29 show what an early backup misses.",
    (33, "Text 3"): "Control is shared among several keys or among pieces of one secret.", (33, "Text 7"): "Slides 35 to 37 show a 2-of-3 spend, its risks and its size.",
    (33, "Text 11"): "Slides 38 to 41 split a secret into shares that rebuild it.",
    (42, "Text 3"): "Handing coins to someone else is trust, not safety.", (42, "Text 7"): "Slides 44 and 45 recompute figures of the Mt. Gox story.",
    (42, "Text 10"): "A coin can hide a key under a hologram that shows if it was peeled.", (42, "Text 11"): "Slides 46 and 47 check facts in saved sources.",
    (48, "Text 3"): "Funds should outlive their owner: a timelock makes the heir wait.", (48, "Text 7"): "Slides 50 and 51 test a ten-block wait on a recorded node.",
    (48, "Text 11"): "Slide 52 lists what the runs did not cover.",
}
for (i, nm), tx in {**CARD, **DIV}.items():
    sh = by(i, nm); old = sh.text_frame.text
    assert old.startswith("Think of") or i in (5, 15, 26, 33, 42, 48) , (i, nm, old)
    set_text(sh, tx)
set_text(by(20, "Text 6"), "Suits a small balance for daily spending.", 2); set_text(by(20, "Text 9"), "Suits the larger part of the savings.", 2)
assert by(20, "Text 6").text_frame.paragraphs[2].text.startswith("Suits") and by(20, "Text 9").text_frame.paragraphs[2].text.startswith("Suits")
for s in prs.slides:
    for x in s.shapes:
        if not x.has_text_frame: continue
        t = x.text_frame.text
        if t == "Each card: the meaning in a few words, then something you already know": set_text(x, NEWSUB)
        elif t == "Say each idea twice: once as the meaning, once as the everyday comparison": set_text(x, BOT)
for i, t in N.TITLES.items():
    sh = by(i, "Text 2"); set_text(sh, t)
    if i in (5, 15, 26, 33, 42, 48): sh.text_frame.paragraphs[0].runs[0].font.size = Pt(28)

# ---- cards behind the rows of slides 3 and 53 and the two panels of slide 54 (so that each of them is one picture the eye can hold)
ref = by(2, "Shape 4")._element
def add_card(slide, l, t, w, h):
    el = copy.deepcopy(ref); slide.shapes._spTree.append(el)
    ids = [int(x) for x in slide._element.xpath("//p:cNvPr/@id")]; el.xpath(".//p:cNvPr")[0].set("id", str(max(ids) + 1)); el.xpath(".//p:cNvPr")[0].set("name", "Card")
    off = el.find(".//" + A + "off"); ext = el.find(".//" + A + "ext")
    off.set("x", str(int(l * E))); off.set("y", str(int(t * E))); ext.set("cx", str(int(w * E))); ext.set("cy", str(int(h * E)))
    return el
for k in range(7): add_card(S(3), 0.48, 1.395 + 0.5 * k, 8.98, 0.47)
for k in range(5): add_card(S(53), 0.48, 1.50 + 0.66 * k, 8.98, 0.62)
add_card(S(54), 0.45, 1.42, 4.50, 3.50); add_card(S(54), 5.12, 1.42, 4.43, 3.00)

# ---- notes: reader-facing, 60 to 140 words, one per slide
for i, s in enumerate(prs.slides, 1):
    s.notes_slide.notes_text_frame.text = N.NOTES[i]
prs.core_properties.version = "2.5.0"
prs.save(TMP); print("stage 1 written", TMP)

# ------------------------------------------------------------------ 4. page 9.97.0
H = open(os.path.join(PG, "sen0401_ch13_page_v9_96_0.html"), encoding="utf-8").read()
tag = '<script type="application/json" id="data">'; a = H.index(tag) + len(tag); b = H.index("</script>", a); data = json.loads(H[a:b]); old_ver = data["_version"]
assert old_ver == "9.96.0"
ver = "9.97.0"
cc = data["chaptercode"]; assert len(cc["examples"]) == len(man["examples"])
for e, me in zip(cc["examples"], man["examples"]): assert e["slide"] == me["slide"]; e["code"] = me["code"]
cc["file"] = "03-materials/ch13/page/chapter_code_ch13_v1_3_0.json"; cc["version"] = "1.3.0"
assert OLDLIB in data["py_boot"]; data["py_boot"] = data["py_boot"].replace(OLDLIB, LIB)
data["py_wheels"] = [{"name": "sen0401_ch13_lib-1.2.0-py3-none-any.whl", "hex": WHL_BYTES.hex()}]
for L_ in data["lecture"]:
    k = L_["n"]; L_["say"] = N.NOTES[k]
    if k in N.TITLES: L_["title"] = N.TITLES[k]
    if L_.get("takeaway", "").startswith("Say each idea twice"): L_["takeaway"] = BOT
data["_version"] = ver
raw = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
H2 = H[:a] + raw + H[b:]
H2 = H2.replace('<meta name="version" content="%s">' % old_ver, '<meta name="version" content="%s">' % ver)
# everyday comparisons: the sentences "It is like ..." and the named images
SENT = re.compile(r' ?It is like (?:[^"\\.]|\\.|\.(?=\d))*?\.(?= [A-Z]|"|\\n|\\")')
H2, n_like = SENT.subn("", H2)
pairs = [(", a key-analogy slide maps house and car keys onto bitcoin keys, and program code", ", and program code"),
         ("Say each idea twice: once as the meaning, once as the everyday comparison", BOT),
         (" Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words.", " Each gives a short meaning and the slide that shows it, so that the idea can be retold in your own words."),
         (" A signature is not a bearer cheque that can be cashed twice.", ""),
         ("A signature is not a stamp on a blank page but a seal over the exact content, so changing the content breaks it", "A signature covers the exact content of a payment, so changing the content breaks it"),
         ("when a shop or a seal replaces your own key", "when a company or a coin package replaces your own key"),
         ("Handing coins to someone else is trust, like leaving cash with a stranger", "Handing coins to someone else is trust, not safety"),
         ("; it is like a postcard that cannot be altered but can be read, now sent in an envelope by default.", ".")]
for old, new in pairs:
    print("  replace x%d: %s" % (H2.count(old), old[:60])); H2 = H2.replace(old, new)
# lambda: the tutorial text of the page
for old, new in (("lambda  lambda x: …", "lambda  an unnamed one-line function"),
                 ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
                 ('key=lambda x: len(x))', 'key=len)')):
    print("  replace x%d: %s" % (H2.count(old), old[:60])); assert old in H2, old; H2 = H2.replace(old, new)
# the top menu item "Run slide code"
v1 = "['learn','📚 Learn'],['maps'"; v2 = "['learn','📚 Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),['maps'"
g1 = "...(CC.length?[['chaptercode','💻 Chapter code']]:[]),"
assert v1 in H2 and g1 in H2; H2 = H2.replace(v1, v2, 1).replace(g1, "", 1)
# the embedded turtle blocks show the hash of their text: recomputed where the text changed
def reha(m):
    body = m.group(3); h = hashlib.sha256(body.encode()).hexdigest()[:16]
    return '<script type="text/turtle"%sdata-sha256="%s">%s</script>' % (m.group(1), h, body)
H2, n_blocks = re.subn(r'<script type="text/turtle"([^>]*)data-sha256="([0-9a-f]+)">(.*?)</script>', reha, H2, flags=re.S)
dst = os.path.join(PG, "sen0401_ch13_page_v9_97_0.html"); assert not os.path.exists(dst)
open(dst, "w", encoding="utf-8").write(H2)
ddir = os.path.join(HERE, "ch13-page"); dd = os.path.join(ddir, "page_data_v9_97_0.json"); assert not os.path.exists(dd)
json.dump(data, open(dd, "w", encoding="utf-8"), ensure_ascii=False)
print("page", os.path.basename(dst), "it-is-like removed", n_like, "turtle blocks", n_blocks)
