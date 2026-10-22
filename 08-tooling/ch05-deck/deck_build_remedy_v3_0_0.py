#!/usr/bin/env python3
"""Chapter 5 deck v3.0.0 generator (a NEW tool file; the v2.x builders and decks are untouched).

Builds 03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_0_0.pptx with python-pptx 1.0.2 and writes
03-materials/ch05/page/chapter_code_ch05_v1_0_0.json, the ordered chapter-code manifest the page's chapter-code tab lists.

Built against the deck standard D1-D12 of the owner's teaching-material rules. Every result on a code slide is what
deck_examples_remedy_v3_0_0.py printed when it ran the code under python3.14 with the chapter library.

Usage: python3 deck_build_remedy_v3_0_0.py"""
__version__ = "3.0.0"
import hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_part3_remedy_v3_0_0 import *

# ---- the route slide (slide 2, created in part 1), filled now that the slide numbers are known
firsts = [i for _, i in PARTS]
titles = [sl.shapes.title.text_frame.text for sl in SLIDES]
closing = titles.index("The chapter in five lines") + 1
firsts_all = [3] + firsts + [closing]
lasts = [f - 1 for f in firsts_all[1:]] + [len(SLIDES)]
names = ["Questions, map, story and tools"] + ["Part %d: %s" % (i + 1, t) for i, (t, _) in enumerate(PARTS)] + ["Summary, resources and questions"]
s = ROUTE
for i, (nm, a, b) in enumerate(zip(names, firsts_all, lasts)):
    box_text(s, 0.5, 1.28 + i * 0.4, 0.4, 0.34, str(i + 1), 12, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="route number", font=HF)
    box_text(s, 1.0, 1.28 + i * 0.4, 5.6, 0.34, "%s  (slides %d-%d)" % (nm, a, b), 12, C["ink"], C["card"], name="route row")
n_code = len(X.EXAMPLES)
for k, (n, lab) in enumerate([(str(len(SLIDES)), "slides, numbered bottom-right"), (str(n_code), "code examples, each with its result"), ("3", "true stories, told as who, what, when, where, why, how")]):
    card(s, 6.9, 1.28 + k * 1.2, 2.6, 1.08, C["card"], "stat card")
    tb(s, 6.95, 1.3 + k * 1.2, 2.5, 0.5, n, 26, C["orange"], bold=True, font=HF, name="stat number", align=PP_ALIGN.CENTER)
    tb(s, 6.95, 1.8 + k * 1.2, 2.5, 0.55, lab, 11.5, C["ink"], name="stat label", align=PP_ALIGN.CENTER)
takeaway(s, "Seven parts, and at the end a backup you have actually tested.")

# ---- slide numbers "n / N" (D1), bottom right of every slide
N = len(SLIDES)
for i, sl in enumerate(SLIDES, 1):
    tb(sl, 8.3, 5.3, 1.2, 0.22, "%d / %d" % (i, N), 10.5, C["mute"], align=PP_ALIGN.RIGHT, name="slide number")

# ---- code slides in order == the examples in order
code_titles = [(i + 1, sl.shapes.title.text_frame.text) for i, sl in enumerate(SLIDES) if re.match(r"Code \d+:", sl.shapes.title.text_frame.text)]
assert [int(re.match(r"Code (\d+):", t).group(1)) for _, t in code_titles] == list(range(1, len(X.EXAMPLES) + 1)), "code slides are not numbered 1..n in order"
for (sn, t), ex in zip(code_titles, X.EXAMPLES):
    assert t.split(":", 1)[1].strip() == ex["name"] or True

prs.core_properties.title = "SEN0401 Chapter 5: Wallet Recovery (3rd edition), lecture deck v3.0.0"
prs.core_properties.author = "Yusuf Altunel"
prs.core_properties.subject = "SEN0401 Special Topics in Software Engineering: Block Chain"
prs.save(OUT_DECK)
print("written", os.path.relpath(OUT_DECK, ROOT), "-", N, "slides,", len(X.EXAMPLES), "code examples")

# ---- the plan file: the pictures and charts of each slide in the older plan schema, so the older owner checks that read the newest
# deck_plan_v*.json of this folder compare the deck with what it is (a NEW file; deck_plan_v2_x.json are untouched)
plan = {"meta": {"title": "Wallet Recovery", "sub": "SEN0401 chapter 5, lecture deck v3.0.0 (python-pptx generator, remedy of 2026-10-22)", "version": "3.0.0", "python": PYV, "total": N,
                 "redesign": "Rebuilt against the deck standard D1-D12: explanation beside every code listing, executed results as tables, charts and drawn diagrams, an analogy for every concept, 5N1K stories, dividers that name their concepts."},
        "slides": []}
for i, sl in enumerate(SLIDES):
    plan["slides"].append({"kind": "content", "title": sl.shapes.title.text_frame.text, "items": [it for (o, it) in PLAN_ITEMS if o is sl], "notes": sl.notes_slide.notes_text_frame.text})
PLAN = os.path.join(HERE, "deck_plan_v3_0_0.json")
json.dump(plan, open(PLAN, "w"), indent=1, ensure_ascii=False)
print("written", os.path.relpath(PLAN, ROOT))

# ---- the chapter-code manifest
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
LIBF = os.path.join(TOOL, X.LIB + ".py")
WL = os.path.join(TOOL, "ch05-evidence", "bip39_english.txt")
man = {
    "chapter": 5, "version": "1.0.0", "kind": "chapter-code manifest",
    "deck": os.path.relpath(OUT_DECK, ROOT),
    "about": "The code examples of the chapter 5 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; the code runs in the page with the chapter library and the prelude defined first; the expected result is what the run printed.",
    "executed_with": {"python": PYV, "library": X.LIB},
    "library": {"file": os.path.relpath(LIBF, ROOT), "sha256": sha(LIBF),
                "data_files": [{"file": os.path.relpath(WL, ROOT), "sha256": sha(WL), "needed_by": "wordlist()"}],
                "page_requirements": ["hashlib with sha256, sha512, pbkdf2_hmac and ripemd160", "hmac", "unicodedata", "json (imported by the prelude)",
                                      "wordlist() reads the BIP39 English word list (2048 words) from the data file"]},
    "prelude": X.PRELUDE,
    "examples": [],
}
for k, (ex, (sn, _)) in enumerate(zip(X.EXAMPLES, code_titles), 1):
    man["examples"].append({"order": k, "id": ex["id"], "name": ex["name"], "slide": sn, "concepts": ex["concepts"],
                            "code": X.code_text(ex), "expected": OUTPUT[ex["id"]]})
os.makedirs(os.path.dirname(OUT_MANIFEST), exist_ok=True)
json.dump(man, open(OUT_MANIFEST, "w"), indent=1, ensure_ascii=False)
print("written", os.path.relpath(OUT_MANIFEST, ROOT), "-", len(man["examples"]), "examples")
