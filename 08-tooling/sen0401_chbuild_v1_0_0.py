#!/usr/bin/env python3
"""sen0401_chbuild v1.0.0 - one driver for building a SEN0401 chapter (8-14) the way SEN0414's newest chapters are built.
Usage: sen0401_chbuild_v1_0_0.py <command> NN [options]      Environment: SEN0401_ROOT (default: the parent of this file's folder), TMPDIR.
  scaffold NN [--demo]   write the chapter's authoring files (never overwrites): data module, corpus bridge, stories, examples, deck content, page inputs
                         --demo fills them with a tiny valid chapter, only to prove the pipeline (use chapter 99)
  research NN            build the five RDODI artefacts from the data module (sen0401_rdodi_build_v1_1_0.py)
  checks NN [python]     execute the claims and behaviours and compare with the artefacts (sen0401_rdodi_checks_v1_0_0.py)
  gates NN [eco] [AV]    RDODI pipeline validator on the pinned ecosystem (sen0401_rdodi_gates_v1_2_0.py)
  examples NN [python]   run chNN-deck/examples_v1_0_0.py, write examples_out_v1_0_0.json
  plan NN                run chNN-deck/deck_content_v1_0_0.py through the engine -> deck_plan_v1_0_0.json
  render NN              plan -> pptx (shared renderer deck_render_v1_0_0.js) -> ooxml fix -> office stamp
  deckchecks NN          deck_check, structure, fit, picture, links(--no-write), honesty, story, arc, lookfeel  (+ fixtures with --fixtures)
  pagetest NN            key-substituted page test (sen0401_page_test_run_v1_0_0.py)
Each command prints its own verdict and exits non-zero on a failure; 'deckchecks' runs all and reports each."""
__version__ = "1.0.0"
import glob, os, re, subprocess, sys, textwrap

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
T = os.path.join(ROOT, "08-tooling")
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def newest(pat):
    fs = sorted(glob.glob(pat), key=vkey)
    if not fs:
        sys.exit("REFUSED: nothing matches " + pat)
    return fs[-1]


def sh(cmd, cwd=None, env=None):
    e = dict(os.environ, SEN0401_ROOT=ROOT, **(env or {}))
    return subprocess.run(cmd, cwd=cwd or T, env=e).returncode


# ------------------------------------------------------------------ scaffolds
DATA = '''"""SEN0401 chapter {n} ({title}) for the RDODI build (generic builder sen0401_rdodi_build_v1_1_0.py).
{status}"""
__version__ = "1.0.0"
CH = {n}
DATE = "{date}"          # the day every source was opened and every claim executed
PYVER = "3.14.6"
VERSION = "1_0_0"
TITLE = "{title}"
QUESTION = "{question}"
CQS = ("Which claims of the chapter can be checked by computation, and what does the computation give?",
       "What in the chapter has changed since the book went to print, and on what source?")
LABELS = {{}}      # explicit labels for acronyms and hyphenated terms (the camel-case rule mangles them)
S = "Antonopoulos and Harding, 2023"
PUBS = [   # (id, label, url, primary?)  P01 is the book chapter at tag third_edition_print1
{pubs}]
CONCEPTS = [   # (kind, label): the chapter's section headings as "Section", its named ideas as "Concept"
{concepts}]
FINDINGS = [   # (id, section, text, cites)  sections: Background, Contemporary developments, Comparative analysis, Conclusion
{findings}]
TAX = [   # (top, mid, leaf, example, definition, io)  io = (expression, repr of its value) or None; every expression is executed by the checks
{tax}]
BODY = {{   # one cited sentence or more for every class named in TAX
{body}}}
CLAIMS = [   # (expression, repr of its value)
{claims}]
BEH = [   # (what, code printing the value, the value printed)
{beh}]
'''

DEMO = dict(
    title="Demonstration chapter for the pipeline proof", question="Does the sen0401 chapter pipeline run end to end on a tiny chapter?",
    pubs=' ("P01", "Mastering Bitcoin, 3rd edition - Chapter 8 (Antonopoulos and Harding, O\'Reilly, 2023; CC BY-SA 4.0; tag third_edition_print1)", "https://github.com/bitcoinbook/bitcoinbook/blob/third_edition_print1/ch08_signatures.adoc", True),\n ("P02", "BIP 340: Schnorr signatures for secp256k1 (Wuille et al., 2020)", "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki", False),\n',
    concepts=' ("Section", "Digital signatures"), ("Concept", "hash"), ("Concept", "signature"),\n',
    findings=' ("F1", "Background", "The chapter introduces hashes and signatures as the proof of authorization (%s)." % S, ["P01"]),\n ("F2", "Contemporary developments", "Schnorr signatures are specified by BIP 340 (Wuille et al., 2020).", ["P02"]),\n ("F3", "Comparative analysis", "A SHA-256 digest has 32 bytes whatever the input (%s)." % S, ["P01"]),\n ("F4", "Conclusion", "Signatures bind a spend to a key (%s)." % S, ["P01"]),\n',
    tax=' ("Primitive", "Hashing", "Digest", "a SHA-256 digest", "A SHA-256 digest has 32 bytes whatever the input.", ("__import__(\'hashlib\').sha256(b\'\').digest().hex()[:8]", "\'e3b0c442\'")),\n ("Primitive", "Hashing", "Length", "the digest length", "The digest length is fixed.", ("len(__import__(\'hashlib\').sha256(b\'abc\').digest())", "32")),\n ("Scheme", "Signing", "Schnorr", "BIP 340", "BIP 340 signatures are 64 bytes.", ("64", "64")),\n',
    body=' "Primitive": "Primitives are the building blocks (%s)." % S,\n "Hashing": "Hashing maps data to a fixed size (%s)." % S,\n "Digest": "A digest is the output of a hash function (%s)." % S,\n "Length": "The length of a digest does not depend on the input (%s)." % S,\n "Scheme": "A scheme combines primitives (%s)." % S,\n "Signing": "Signing proves control of a key (%s)." % S,\n "Schnorr": "Schnorr signatures are specified by BIP 340 (Wuille et al., 2020)." ,\n',
    claims=' ("sum(range(5))", "10"),\n',
    beh=' ("a SHA-256 digest of nothing starts with e3b0c442", "import hashlib; print(hashlib.sha256(b\'\').hexdigest()[:8])", "e3b0c442"),\n')

BLANK = dict(
    title="TODO title", question="TODO the research question of the chapter",
    pubs=' ("P01", "Mastering Bitcoin, 3rd edition - Chapter NN, TODO (Antonopoulos and Harding, O\'Reilly, 2023; CC BY-SA 4.0; tag third_edition_print1)", "TODO https://github.com/bitcoinbook/bitcoinbook/blob/third_edition_print1/chNN_TODO.adoc", True),\n',
    concepts=' ("Section", "TODO"),\n', findings=' ("F1", "Background", "TODO (%s)." % S, ["P01"]),\n',
    tax=' # ("Top", "Mid", "Leaf", "example", "definition", ("expr", "repr")),\n', body=' # "Top": "TODO (%s)." % S,\n', claims='', beh='')

CORPUS = '''"""SEN0401 chapter {n} corpus bridge: NODES and CQS for the deck engine, derived from the chapter's RDODI data module
(sen0401_ch{n}_rdodi_data_v1_0_0.py) so that research and deck cannot drift apart. A node is (name, label, level, parent, example, paragraphs)."""
__version__ = "1.0.0"
import importlib
D = importlib.import_module("sen0401_ch{n}_rdodi_data_v1_0_0")
LAB = lambda c: D.LABELS.get(c) or (lambda t: t[0].upper() + t[1:])("".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip())
NODES, _seen = [], set()
for top, mid, leaf, ex, d, io in D.TAX:
    for c, lv, par in ((top, 1, None), (mid, 2, top), (leaf, 3, mid)):
        if c in _seen:
            continue
        _seen.add(c)
        NODES.append([c, LAB(c), lv, par, (ex, d, io) if lv == 3 else None, [("What it is", D.BODY[c])]])
CQS = list(D.CQS)
'''

STORIES = '''"""SEN0401 chapter {n} - the story companion (5N1K): real, dated, sourced stories, one live link and one free picture each.
Fill every field; run_checks() refuses any TODO, a date that is not ISO, a link that is not https, a missing credit or picture file."""
__version__ = "1.0.0"
import os, re
STORIES = [
{stories}]
MONEY_PICTURES = []   # historical money pictures (coin, note, ledger page...) as dicts with file/credit/licence/source: the owner's rule; warned when empty
FIELDS = ("id", "title", "when", "who", "where", "link", "concepts", "story", "lesson", "source", "credit", "photo")


def run_checks():
    bad = []
    for s in STORIES:
        for f in FIELDS:
            v = s.get(f)
            if not v or "TODO" in str(v):
                bad.append("%s: field %s empty or TODO" % (s.get("id"), f))
        if len(str(s.get("lesson", "")).split()) > 14:
            bad.append("%s: lesson over 14 words" % s.get("id"))
        if not (2 <= str(s.get("story", "")).count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % s.get("id"))
        if not re.match(r"^\\d{{4}}-\\d{{2}}-\\d{{2}}$", str(s.get("when", ""))):
            bad.append("%s: when is not an ISO date" % s.get("id"))
        if not str(s.get("link", "")).startswith("https://"):
            bad.append("%s: link is not https" % s.get("id"))
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "03-materials", "ch{n}", "assets", str(s.get("photo", "")))
        if s.get("photo") and "TODO" not in str(s["photo"]) and not os.path.exists(p):
            bad.append("%s: picture file %s missing" % (s.get("id"), s.get("photo")))
    if len(STORIES) < 3:
        bad.append("fewer than three stories")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print("\\n".join(b) or "stories ok")
    raise SystemExit(1 if b else 0)
'''
STORY_DEMO = '''    {"id": "Demo%d", "title": "Demo story %d", "when": "2009-01-03", "who": "A demonstration person", "where": "A demonstration place", "link": "https://en.bitcoin.it/wiki/Genesis_block",
     "concepts": ["Digest"], "story": "On 3 January 2009 the first block was mined. This sentence is demonstration text.", "lesson": "A demonstration lesson", "source": "https://en.bitcoin.it/wiki/Genesis_block",
     "credit": "Demonstration picture, public domain", "photo": "demo.png"},
'''
STORY_BLANK = '''    {"id": "TODO%d", "title": "TODO", "when": "TODO", "who": "TODO", "where": "TODO", "link": "TODO", "concepts": [], "story": "TODO", "lesson": "TODO",
     "source": "TODO", "credit": "TODO", "photo": "TODO"},
'''

EXAMPLES = '''"""Every computation the SEN0401 chapter {n} lecture deck shows; the outputs come from executing these statements (examples_run), never from typing them.
PRELUDE is run first in each group's namespace; deck_check re-runs every '>>>' row of the finished deck in the same namespace. A statement must be ONE line."""
__version__ = "1.0.0"
PRELUDE = "import hashlib, json"
EX = {{
{ex}}}
'''
EXAMPLES_RUN = '''#!/usr/bin/env python3
"""sen0401_deck_examples_run v1.0.0 - executes every statement of chNN-deck/examples_v1_0_0.py (one namespace per group after PRELUDE) and writes
examples_out_v1_0_0.json, as ch07-deck/examples_run_v1_0_0.py does. Usage: sen0401_deck_examples_run_v1_0_0.py NN <python> <out.json>"""
import importlib.util, json, os, subprocess, sys
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n, PY, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("ex", os.path.join(ROOT, "08-tooling", "ch%s-deck" % n, "examples_v1_0_0.py")); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
RUNNER = ("import json, sys\\nns = {}\\nexec(sys.argv[1], ns)\\nout = []\\nfor st in json.loads(sys.argv[2]):\\n    try:\\n        try:\\n            out.append(repr(eval(st, ns)))\\n"
          "        except SyntaxError:\\n            exec(st, ns); out.append('')\\n    except Exception as e:\\n        out.append('%s: %s' % (type(e).__name__, e))\\nprint(json.dumps(out))\\n")
ver = subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True)
out = {"_version": "1.0.0", "_python": ver.stdout.strip()}
for k, rows in m.EX.items():
    if any("\\n" in r for r in rows): sys.exit("REFUSED: group %s has a multi-line statement" % k)
    r = subprocess.run([PY, "-c", RUNNER, m.PRELUDE, json.dumps(rows)], capture_output=True, text=True)
    if r.returncode: sys.exit("group %s failed: %s" % (k, r.stderr[-400:]))
    out[k] = [[s, o] for s, o in zip(rows, json.loads(r.stdout))]
json.dump(out, open(OUT, "w"), indent=1); print("written", OUT, "under Python", out["_python"], "-", len(m.EX), "groups")
'''

DECK_BLANK = '''#!/usr/bin/env python3
"""Chapter {n} deck content (26 slides) for the SEN0401 engine. REFUSES to build until every TODO is replaced by the chapter's own slides.
Pattern (see ch07-deck/deck_build_v1_0_0.py for a finished chapter): title; [agenda inserted as slide 2]; questions; a map; then 5 sections each with
content slides (console rows from examples_out via E.code(group,...)), 3+ story slides (E.story_slide), a summary, ONE resources slide last.
Owner rules: short sentences on slides, notes as reader's prose, 5N1K stories with real names/dates/places/free pictures/live links, every
chart a native PPT chart, diagrams as native shapes, the CME look and feel (tokens in CME_MaterialsLookAndFeel_v1_0_0.md)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_0_0 as E
E.init({nn}, HERE, assets=())
raise SystemExit("REFUSED: chapter {n} deck content is not written yet (scaffold skeleton) - write the slides, then remove this line")
'''

DECK_DEMO = '''#!/usr/bin/env python3
"""Chapter {n} DEMO deck content: a generated 26-slide deck over the demo corpus, only to prove that engine -> renderer -> checks run. Not teaching content."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_0_0 as E
E.init({nn}, HERE, assets=("demo.png",))
C, G, LABEL = E.C, E.G, E.LABEL
names = [n[0] for n in C.NODES if n[2] == 3]
E.slide("title", "Chapter {nn}: Demonstration", "A generated deck that proves the pipeline", [], "This deck is generated from the demonstration data module. It proves that the engine, the renderer and the checks run; it teaches nothing. The full text is on the course page.")
E.content("The questions this chapter answers", "Its own competency questions", [{{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.6, "fs": 11, "items": list(C.CQS)}}], E.notes(names[0], look="The questions are the chapter's own"))
E.content("The chapter map", "One slide for the whole chapter", [{{"t": "boxes", "x": 0.5, "y": 1.7, "w": 9.0, "h": 2.9, "cols": 3, "fs": 12, "subfs": 10, "accent": [], "items": [{{"label": LABEL[n]}} for n in names]}}], E.notes(names[0], look="The boxes name the leaves"), lede="Every box is a concept of the chapter.", take="The map of the chapter")
for i in range(5):
    E.section("Part %d" % (i + 1), "Generated section", [{{"label": LABEL[names[j % len(names)]]}} for j in range(3)], E.notes(names[0], look="A section slide"))
    for k in range(3 if i < 4 else 2):
        grp = sorted(G)[0]
        E.content("Slide %d.%d" % (i + 1, k + 1), "Generated", [E.code(grp, 0.5, 1.9, 9.0, 2.4, fs=10)], E.notes(names[0], look="The console is run by the deck check"), lede="One console row group, executed by the checker.", take="Executed, not typed")
for i, sid in enumerate(sorted(E.STORY)):
    g = sorted(G)[0]
    E.story_slide(sid, "demo.png", (0.5, 1.6, 3.0, 1.9), ["Who and where", "What happened", "The lesson"], g, G[g][:2], "executed", "The picture is a generated stand-in", (3.8, 1.6, 5.7, 1.6), (3.8, 3.3, 5.7, 1.2))
E.agenda(["Questions and map"] + ["Part %d" % (i + 1) for i in range(5)], "The route has five generated parts. Nothing here teaches; it proves the pipeline.", "Five generated parts")
E.finish("Chapter {nn}: Demonstration", "1.0.0", "demo")
'''
DEMO_EX = ' "Demo": ["d = hashlib.sha256(b\'abc\').hexdigest()", "d[:8]", "len(d) if d else 0"],\n'


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        print("kept   ", os.path.relpath(path, ROOT))
        return
    open(path, "w").write(text)
    print("written", os.path.relpath(path, ROOT))


def scaffold(nn, demo):
    n = "%02d" % nn
    d = dict(DEMO if demo else BLANK)
    d["n"] = nn
    d["date"] = "2026-10-14"
    d["status"] = "DEMONSTRATION data, only to prove the pipeline." if demo else "SKELETON: replace every TODO; the build refuses a TODO."
    w(os.path.join(T, "sen0401_ch%s_rdodi_data_v1_0_0.py" % n), DATA.format(**d).replace("chNN_TODO", "ch%s_TODO" % n).replace("Chapter NN", "Chapter %d" % nn))
    w(os.path.join(T, "sen0401_ch%s_corpus_v1_0_0.py" % n), CORPUS.format(n=n))
    w(os.path.join(T, "sen0401_ch%s_stories_v1_0_0.py" % n), STORIES.format(n=n, stories="".join((STORY_DEMO if demo else STORY_BLANK) % ((i, i) if demo else i) for i in range(1, 4))))
    if demo:
        from PIL import Image
        pth = os.path.join(ROOT, "03-materials", "ch%s" % n, "assets", "demo.png")
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        Image.new("RGB", (320, 200), (217, 122, 20)).save(pth)
    ex = DEMO_EX if demo else ' # "Group": ["one-line statement", "..."],\n'
    w(os.path.join(T, "ch%s-deck" % n, "examples_v1_0_0.py" % () if False else "examples_v1_0_0.py"), EXAMPLES.format(n=nn, ex=ex))
    w(os.path.join(T, "ch%s-deck" % n, "deck_content_v1_0_0.py"), (DECK_DEMO if demo else DECK_BLANK).format(n=n, nn=nn))
    if not os.path.exists(os.path.join(T, "sen0401_deck_examples_run_v1_0_0.py")):
        w(os.path.join(T, "sen0401_deck_examples_run_v1_0_0.py"), EXAMPLES_RUN)
    if demo:
        w(os.path.join(T, "ch%s-deck" % n, ".demo"), "generated demonstration chapter; delete the folder and the sen0401_ch%s_* files\n" % n)


def data_module(n):
    return "sen0401_ch%s_rdodi_data_v1_0_0" % n


def cmd(argv):
    c, nn = argv[0], int(argv[1]); n = "%02d" % nn; opts = argv[2:]
    py = "/home/claude/venv314/bin/python" if os.path.exists("/home/claude/venv314/bin/python") else sys.executable
    if "--python" in opts:
        py = opts[opts.index("--python") + 1]       # the interpreter the recording was made under (deck_check refuses any other)
    deck = os.path.join(T, "ch%s-deck" % n)
    out = os.path.join(deck, "sen0401_ch%s_deck_v1_0_0.pptx" % n)
    if c == "scaffold":
        return scaffold(nn, "--demo" in opts) or 0
    if c == "research":
        src = open(os.path.join(T, data_module(n) + ".py")).read()
        if "TODO" in src:
            sys.exit("REFUSED: the data module still has TODO")
        return sh([sys.executable, "sen0401_rdodi_build_v1_1_0.py", data_module(n), "2026-10-14T00:00:00Z"] if False else
                  [sys.executable, "sen0401_rdodi_build_v1_1_0.py", data_module(n), __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")], env={"PYTHONPATH": T})
    if c == "checks":
        return sh([sys.executable, "sen0401_rdodi_checks_v1_0_0.py", data_module(n), opts[0] if opts else py], env={"PYTHONPATH": T})
    if c == "gates":
        return sh([sys.executable, "sen0401_rdodi_gates_v1_2_0.py", n] + opts)
    if c == "examples":
        return sh([sys.executable, "sen0401_deck_examples_run_v1_0_0.py", n, opts[0] if opts else py, os.path.join(deck, "examples_out_v1_0_0.json")])
    if c == "plan":
        return sh([sys.executable, "deck_content_v1_0_0.py"], cwd=deck)
    if c == "render":
        raw = os.path.join(os.environ.get("TMPDIR", "/tmp"), "sen0401_ch%s_raw.pptx" % n)
        node = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        for step in ([["node", os.path.join(T, "sen0401_deck_render_v1_0_0.js"), "deck_plan_v1_0_0.json", raw]],
                     [[sys.executable, os.path.join(T, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]],
                     [[sys.executable, os.path.join(T, "office_stamp_v1_0_0.py"), out, "1.0.0", "SEN0401 Chapter %d" % nn]]):
            r = sh(step[0], cwd=deck, env={"NODE_PATH": node})
            if r:
                return r
        return 0
    if c == "deckchecks":
        env = {"SEN0401_DECK": out}
        steps = [("deck_check", [py, "sen0401_deck_check_v1_0_0.py", n, out]),
                 ("structure", [sys.executable, "sen0401_deck_structure_check_v1_0_0.py", out]),
                 ("fit", [sys.executable, "sen0401_deck_fit_check_v1_0_0.py", out]),
                 ("picture", [sys.executable, "sen0401_deck_picture_check_v1_0_0.py", n]),
                 ("links", [sys.executable, "sen0401_deck_links_check_v1_0_0.py", n, "--no-write"]),
                 ("honesty", [sys.executable, "sen0401_deck_honesty_check_v1_0_0.py", n]),
                 ("story", [sys.executable, "sen0401_story_check_v1_0_0.py", n]),
                 ("arc", [sys.executable, "sen0401_deck_arc_check_v1_0_0.py", n]),
                 ("lookfeel", [sys.executable, "sen0401_deck_lookfeel_check_v1_0_0.py", n])]
        if "--fixtures" in opts:
            steps.append(("fixtures", [sys.executable, "sen0401_deck_fixtures_v1_0_0.py", n, "--run"]))
        res = [(name, sh(c_, env=env)) for name, c_ in steps]
        print("\n".join("%-10s %s" % (a, "PASS" if not b else "FAIL(%d)" % b) for a, b in res))
        return 1 if any(b for _, b in res) else 0
    if c == "pagetest":
        return sh([sys.executable, "sen0401_page_test_run_v1_0_0.py", n] + opts)
    sys.exit(__doc__)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sys.exit(cmd(sys.argv[1:]))
