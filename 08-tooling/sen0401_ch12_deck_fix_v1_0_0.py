#!/usr/bin/env python3
"""sen0401_ch12_deck_fix v1.0.0 - brings the chapter 12 deck to the course standard (deck standard v3.1.0, CME material check v1.2.0): no everyday comparison on a slide or in a note,
reader-facing notes of 60-140 words, code slides rebuilt from the chapter-code examples (comment-led boxes, no prompts, no lambda, an explanation under every box), titles of at least four words,
a visual on every slide. Reads the newest chapter 12 deck and manifest, writes the next version of each beside them (never edits a version that exists). Chapter 12 only.
Usage: python3 sen0401_ch12_deck_fix_v1_0_0.py"""
__version__ = "1.0.0"
import copy, glob, importlib.util, io, json, math, os, re, sys, tokenize
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE_TYPE as T
from lxml import etree

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "08-tooling"); E = 914400
D = os.path.join(REPO, "03-materials", "ch12"); PD = os.path.join(D, "page")
def load(name):
    sp = importlib.util.spec_from_file_location(name, os.path.join(TOOL, name + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
NT = load("sen0401_ch12_notes_v1_0_0")

# the shared helpers of the chapter 7/8 fix (layout of a code slide, cards, connectors) are used as they are
_src = open(os.path.join(TOOL, "sen0401_ch78_rulings_fix_v1_0_0.py"), encoding="utf-8").read()
_a = _src.index("# ---------------------------------------------------------------- deck helpers"); _b = _src.index("def wc(s)")
exec(compile(_src[_a:_b], "ch78_helpers", "exec"), globals())
def wc(s): return len(s.split())
def vkey(p, ext): return tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.%s$" % ext, p).groups())

COMMENTS = {
7: ["# Five heights, one for each period", "# The reward in coins at each height", "# The last non-zero reward"],
8: ["# Add up all rewards in whole satoshis", "# How far the total falls below 21 million coins", "# The book's script as it is printed"],
9: ["# Core's block template on a private chain", "# The reward is subsidy plus fees", "# A claim of one satoshi less, and one satoshi more"],
13: ["# Ask Core about spoiled transactions", "# Add the young coinbase, then read each reason", "# The same spend with 100 confirmations"],
14: ["# Fourteen test blocks and their verdicts", "# The valid block is accepted", "# Count the rules and show the verdict"],
15: ["# The chain before and after the switch", "# Chain work of each tip as a number", "# Which tip wins, and by how much"],
18: ["# The block template and its weight limit", "# The coinbase of a Core block", "# Limit, height and the pushed height"],
20: ["# Take the 80-byte header apart", "# Is the hash within the target?", "# Leading zero bits and the summary"],
21: ["# Two builds of the same block", "# Coinbase ids and merkle roots of both", "# Header nonces and the three comparisons"],
24: ["# The hash of Hello, world! with a counter", "# Tries until z zero digits", "# Tries for one to four zero digits"],
27: ["# The target from the bits of block 277,316", "# The difficulty from the same bits", "# The zero bits a valid hash needs"],
28: ["# Hashes per block at that difficulty", "# Days and blocks for one terahash a second", "# The network hash rate from a later difficulty"],
29: ["# Times and bits of the period", "# Apply the retarget rule of Core", "# The bias of counting 2,016 for 2,015"],
30: ["# The target of a typical period", "# Ratio of new to old target for a duration", "# Too fast, on time and too slow"],
31: ["# Constants of three chains: no retargeting", "# Constants for the BIP 94 branch", "# The flags of regtest and testnet4"],
34: ["# Hashes a second on 15 October 2026", "# Times a second the nonce is emptied", "# Free bits: nonce and version rolling"],
36: ["# Shares of the network hash rate", "# Expected days for one block", "# The result"],
38: ["# Catch-up odds for three attacker shares", "# Selfish-mining thresholds by honest follow share", "# Both results"],
41: ["# One block seen by a loose and a strict node", "# The two chains that followed", "# The verdicts and whether the tips agree"],
44: ["# Shares of the hash rate left on a branch", "# Days for 2,016 blocks at each share", "# The result"],
46: ["# The states of a test deployment", "# Thresholds for 95 and 90 percent", "# The final state and the thresholds"],
48: ["# Fork names and the pattern of their heights", "# Read each height from chainparams.cpp", "# The result"],
}
REWRITE = {   # lambdas become named functions (a lambda is not taught in this course)
24: {"ok = lambda n, z: hw(n).startswith('0' * z)": "def ok(n, z): return hw(n).startswith('0' * z)",
     "f = lambda z: next(n for n in ns if ok(n, z))": "def f(z): return next(n for n in ns if ok(n, z))"},
30: {"rt = lambda s: L.retarget(0, s, '17034219')": "def rt(s): return L.retarget(0, s, '17034219')",
     "tg = lambda s: L.bits_to_target(rt(s)) / t0": "def tg(s): return L.bits_to_target(rt(s)) / t0"},
}
SETUP_OLD = "hw = lambda n, w='w': hashlib.sha256(('Hello, ' + w + 'orld! ' + str(n) + chr(10)).encode()).hexdigest()"
SETUP_NEW = "def hw(n, w='w'):\n    return hashlib.sha256(('Hello, ' + w + 'orld! ' + str(n) + chr(10)).encode()).hexdigest()"

src = sorted(glob.glob(os.path.join(D, "SEN0401_Ch12_MiningAndConsensus_3e_v*.pptx")), key=lambda p: vkey(p, "pptx"))[-1]
v = vkey(src, "pptx"); dst = os.path.join(D, "SEN0401_Ch12_MiningAndConsensus_3e_v%d_%d_0.pptx" % (v[0], v[1] + 1)); assert not os.path.exists(dst), dst
src_man = sorted(glob.glob(os.path.join(PD, "chapter_code_ch12_v*.json")), key=lambda p: vkey(p, "json"))[-1]
mv = vkey(src_man, "json"); dst_man = os.path.join(PD, "chapter_code_ch12_v%d_%d_0.json" % (mv[0], mv[1] + 1)); assert not os.path.exists(dst_man), dst_man
man = json.load(open(src_man, encoding="utf-8"))
prs = Presentation(src); N = len(prs.slides)

# ---- the examples: the old boxes of each slide (lines without prompts) with a comment line in front, and the old explanations
EX = {}
for e in man["examples"]:
    s = prs.slides[e["slide"] - 1]
    frames = [sh for sh in sorted(s.shapes, key=lambda x: (x.top, x.left)) if is_code(sh)]
    says = [sh.text_frame.text.strip() for sh in s.shapes if sh.has_text_frame and not is_code(sh) and sh.width > 4 * E and 0.7 * E < sh.left < 1.0 * E and 1.3 * E < sh.top < 4.99 * E and "run under" not in sh.text_frame.text]
    chunks = []
    for f in frames:
        lines = [pa.text[4:] for pa in f.text_frame.paragraphs if pa.text.startswith((">>> ", "... "))]
        lines = [REWRITE.get(e["slide"], {}).get(l, l) for l in lines]
        chunks.append(lines)
    assert "\n".join("\n".join(c) for c in chunks).replace("lambda", "") != "" and len(chunks) == len(COMMENTS[e["slide"]]) == len(says), (e["slide"], len(chunks), len(says))
    EX[e["slide"]] = dict(chunks=["\n".join([c] + l) for c, l in zip(COMMENTS[e["slide"]], chunks)], says=says, show=e["show"])
    for ch_ in EX[e["slide"]]["chunks"]:
        compile(ch_, "<chunk>", "exec")
        assert wc(ch_) <= 30, (e["slide"], ch_)
    for sy in says: assert wc(sy) >= 8, (e["slide"], sy)

# ---- the deck
SUB_OLD = "Each card: the meaning in a few words, then something you already know"
BOT_OLD = "Say each idea twice: once as the meaning, once as the everyday comparison"
report = []
for i, s in enumerate(prs.slides, 1):
    shapes = list(s.shapes)
    th = [(k, sh) for k, sh in enumerate(shapes) if sh.has_text_frame and THINK.match(sh.text_frame.text)]
    if i in NT.DIVIDER_LINES:
        for (k, sh), new in zip(th, NT.DIVIDER_LINES[i]): set_text(sh.text_frame.paragraphs[0], new)
        assert len(th) == len(NT.DIVIDER_LINES[i]), (i, len(th))
        hd = next(x for x in shapes if x.has_text_frame and x.name == "Text 3"); set_text(hd.text_frame.paragraphs[0], NT.HEADLINE[i])
    else:
        cards = []; rem = []
        for k, sh in th:
            prev = next((p for p in reversed(shapes[:k]) if p.has_text_frame and p.text_frame.text.strip() and len(p.text_frame.paragraphs) >= 2), None)
            rem.append((sh, prev))
        for sh, prev in rem:
            if prev is not None:
                for bg in s.shapes:
                    if bg.shape_type == T.AUTO_SHAPE and not bg.text_frame.text.strip() and bg.left <= prev.left <= bg.left + bg.width and bg.top <= prev.top <= bg.top + bg.height and bg.width > 1.5 * E:
                        bg.height = Emu(int(prev.top + prev.height - bg.top + 0.10 * E))
                        for bar in s.shapes:
                            if bar.shape_type == T.AUTO_SHAPE and bar.width < 0.2 * E and bg.left <= bar.left <= bg.left + bg.width and bg.top <= bar.top <= bg.top + bg.height + 0.5 * E and bar.height > bg.height:
                                bar.height = Emu(int(bg.height - 0.28 * E))
                        break
            sh._element.getparent().remove(sh._element)
        if rem: scale_cards(s, [p for _, p in rem if p is not None])
    for sh in s.shapes:
        if sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                t = "".join(r.text for r in pa.runs)
                if t.strip() == SUB_OLD and pa.runs: set_text(pa, NT.SUB_NEW)
                if t.strip() == BOT_OLD and pa.runs: set_text(pa, NT.BOT_NEW)
    if i == 42:   # the hard fork and soft fork boxes: the closing "Like ..." sentence goes
        for sh in s.shapes:
            if sh.has_text_frame:
                for pa in list(sh.text_frame.paragraphs):
                    if "".join(r.text for r in pa.runs).startswith("Like "): pa._p.getparent().remove(pa._p)
    # code slide
    if i in EX:
        foot = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame and "run under" in sh.text_frame.text][0]
        layout_code_slide(s, EX[i]["chunks"], EX[i]["says"], foot)
        for sh in s.shapes:
            if sh.name.startswith("Code ") and not sh.name.startswith("Code box"): sh.name = "code " + sh.name[5:]
    # title, notes, visual
    if i in NT.TITLES:
        tsh = title_shape(s); set_text(tsh.text_frame.paragraphs[0], NT.TITLES[i])
    if i not in (1, N) and not has_visual(s):
        if not add_flow(s): report.append(("no visual placed", i))
    n_ = wc(NT.NOTES[i])
    if not 60 <= n_ <= 140: report.append(("notes words", i, n_))
    s.notes_slide.notes_text_frame.text = NT.NOTES[i]
prs.core_properties.version = "%d.%d.0" % (v[0], v[1] + 1)
prs.save(dst); print(os.path.basename(dst)); print("report:", report)

# ---- the manifest: the same code as the slides, setup without a lambda
for me in man["examples"]:
    ne = EX[me["slide"]]; me["code"] = "\n".join(ne["chunks"])
man["setup"]["code"] = man["setup"]["code"].replace(SETUP_OLD, SETUP_NEW); assert "lambda" not in man["setup"]["code"]
man["manifest"] = "chapter_code_ch12_v%d_%d_0" % (mv[0], mv[1] + 1); man["deck"] = os.path.basename(dst); man["deck_version"] = "%d.%d.0" % (v[0], v[1] + 1)
json.dump(man, open(dst_man, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print(os.path.basename(dst_man))
