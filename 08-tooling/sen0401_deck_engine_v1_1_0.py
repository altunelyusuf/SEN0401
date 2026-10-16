#!/usr/bin/env python3
"""Generic deck-plan engine for a SEN0401 chapter: the helpers of ch07-deck/deck_build_v1_0_0.py (notes, story_notes, code, factrow, img,
content, section, story_slide) taken out of the chapter file and parametrised by the chapter number, plus finish(), which holds every
refusal the ch07 builder holds (notes present, no directive labels, takeaway length, 20-26 slides, agenda ranges) and writes
deck_plan_v1_1_0.json. A chapter's content file (made by sen0401_chbuild_v1_0_0.py scaffold) does:
    import sen0401_deck_engine_v1_0_0 as E
    E.init(8, HERE, assets=[...])
    E.slide('title', ...); E.content(...); ...; E.finish(...)
Behaviour on chapter 7 is the same as deck_build_v1_0_0.py's (checked: sen0401_chbuild_v1_0_0.py proof, plan sections of the README)."""
__version__ = "1.1.0"  # plan file deck_plan_v1_1_0.json; the READ card shows the story's linkLabel (the resource's title and kind) when the stories file has one
import glob, importlib.util, json, os, re, sys

TOOLING = os.path.dirname(os.path.abspath(__file__))
S = []
C = ST = G = STORY = BYNAME = LABEL = None
NN = HERE = ASSETS = CAP = PYV = None
BOOKCAP = "Mastering Bitcoin 3e, CC BY-SA"
STORY_TITLES = set()   # titles of slides made by story_slide (a story slide needs no takeaway clue)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _newest(pattern):
    fs = sorted(glob.glob(os.path.join(TOOLING, pattern)), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.py$", p)[0]])
    if not fs:
        raise SystemExit("REFUSED: no file matches %s" % pattern)
    return fs[-1]


def init(nn, here, assets=(), root=None, deck_assets_rel=None):
    """nn: chapter number; here: the chapter's deck folder; assets: file names that must exist in 03-materials/chNN/assets."""
    global C, ST, G, STORY, BYNAME, LABEL, NN, HERE, ASSETS, CAP, PYV
    NN, HERE = "%02d" % nn, here
    C = _load("corpus" + NN, _newest("sen0401_ch%s_corpus_v*.py" % NN))
    ST = _load("stories" + NN, _newest("sen0401_ch%s_stories_v*.py" % NN))
    if ST.run_checks():
        raise SystemExit("REFUSED: the story companion fails its own checks")
    STORY = {x["id"]: x for x in ST.STORIES}
    ASSETS = deck_assets_rel or "../../03-materials/ch%s/assets/" % NN
    for f in assets:
        if not os.path.exists(os.path.join(here, ASSETS, f)):
            raise SystemExit("REFUSED: missing asset %s" % f)
    EX = json.load(open(os.path.join(here, "examples_out_v1_0_0.json")))
    PYV = EX["_python"]
    CAP = "run under Python %s" % PYV
    G = {k: v for k, v in EX.items() if not k.startswith("_")}
    BYNAME = {n[0]: n for n in C.NODES}
    LABEL = {n[0]: (n[1] or n[0]) for n in C.NODES}
    S.clear()
    STORY_TITLES.clear()


def _sentences(text, k=2):
    return " ".join(re.split(r"(?<=[.!?]) +", text)[:k])


def _section_of(name):
    n = BYNAME[name]
    while n[2] > 2:
        n = BYNAME[n[3]]
    return LABEL[n[0]]


def notes(*names, look=None, think=None):
    for nm in names:
        if nm not in BYNAME:
            raise SystemExit("REFUSED: no corpus concept named %r" % nm)
    lead = BYNAME[names[0]][5][0][1]
    out = _sentences(lead, 2)
    if len(out) > 520:
        out = _sentences(lead, 1)
    if look:
        out += " " + look.rstrip(".") + "."
    if think:
        out += " A question to think about is this: " + think.rstrip(".?") + "?"
    secs = sorted({_section_of(nm) for nm in names})
    out += " The full explanation is on the course page, chapter %d, under " % int(NN) + " and ".join(secs) + \
           (", in the concept" if len(names) == 1 else ", in the concepts") + " " + ", ".join(LABEL[nm] for nm in names) + "."
    return out


def story_notes(sid, look=None):
    st = STORY[sid]
    out = "This is a true story, dated %s. %s" % (st["when"], st["story"])
    if look:
        out += " " + look.rstrip(".") + "."
    return out + " The lesson the slide carries is that %s. The sources are these. %s" % (st["lesson"][0].lower() + st["lesson"][1:], st["source"])


def children(name, level=None):
    out = [n for n in C.NODES if n[3] == name]
    if level is not None:
        out = [n for n in out if n[2] == level]
    return [n[0] for n in out]


def code(group, x, y, w, h, fs=11, rows=None):
    rr = rows if rows is not None else G[group]
    for st, out in rr:
        if "\n" in st:
            raise SystemExit("REFUSED: console %s has a newline in a source row (lesson L3 of the SEN0414 deposit); re-run line by line" % group)
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    nlines = sum(1 + (1 if out.strip() else 0) for _, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * 0.00842), 1), round((h - 0.30) * 72.0 / (nlines * 1.3), 1))
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1fx%.1fin (needs %.1f pt)" % (group, w, h, fs))
    return {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs, "cap": CAP}


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    cut = lambda s: s[:150].rsplit(",", 1)[0] if len(s) > 150 else s
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": cut(st["who"]), "where": cut(st["where"]), "when": st["when"],
            "link": st["link"], "linkText": st.get("linkLabel") or host}


def img(f, x, y, w, h, cap=None):
    it = {"t": "img", "path": ASSETS + f, "x": x, "y": y, "w": w, "h": h}
    if cap:
        it["cap"] = cap
    return it


def slide(kind, title, sub, items, notes_text, bg="light"):
    S.append({"kind": kind, "title": title, "sub": sub, "items": items, "notes": notes_text, "bg": bg})


def content(title, sub, items, notes_text, take=None, lede=None):
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes_text, "bg": "light"}
    if lede:
        if len(lede.split()) > 34:
            raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
        for it in items:
            top = it["y"] - (0.3 if it.get("t") == "code" and it.get("label") else 0)
            if top < 1.68:
                raise SystemExit("REFUSED: %r starts at %.2f in under the lede of %r" % (it.get("label") or it.get("t"), top, title))
        sl["lede"] = lede
    if take:
        sl["take"] = take
    S.append(sl)


def section(title, sub, boxes, notes_text, image=None):
    items = [{"t": "boxes", "x": 0.85, "y": 2.95, "w": 5.3 if image else 8.6, "h": 1.9, "cols": 2 if image else min(4, len(boxes)),
              "fs": 14, "subfs": 11, "accent": [], "items": boxes}]
    if image:
        items.append(image)
    slide("section", title, sub, items, notes_text)


def story_slide(sid, photo, photo_box, beats, grp, rows, label, lookstr, code_box, beats_box, title=None):
    st = STORY[sid]
    items = [img(photo, *photo_box, cap=st["credit"]),
             {"t": "beats", "x": beats_box[0], "y": beats_box[1], "w": beats_box[2], "h": beats_box[3], "fs": 12, "items": beats},
             dict(code(grp, *code_box, fs=9, rows=rows), label=label),
             factrow(sid, x=beats_box[0] if code_box[0] > 1 else 0.5, y=4.62, w=9.5 - (beats_box[0] if code_box[0] > 1 else 0.5))]
    STORY_TITLES.add(title or st["title"])
    content(title or st["title"], st["when"], items, story_notes(sid, look=lookstr))


def agenda(route, route_notes, take):
    """Insert the agenda as slide 2. route: list of (title, first_slide_or_None, last_slide_or_None); None means 'derive from section slides':
    row 0 is 'questions and map' (slides 3..first section), then one row per section, the last running to the end."""
    S.insert(1, {"kind": "content", "title": "Today's route", "sub": "The questions, then %s parts; every number is a slide you can jump to" % ("", "one", "two", "three", "four", "five", "six", "seven", "eight")[len(route) - 1],
                 "items": [], "notes": "", "take": take, "bg": "light"})
    sec = [i for i, s in enumerate(S) if s["kind"] == "section"]
    if len(sec) != len(route) - 1:
        raise SystemExit("REFUSED: %d section slides but the route names %d parts" % (len(sec), len(route) - 1))
    bounds = [(3, sec[0])] + [(sec[i] + 1, sec[i + 1] if i + 1 < len(sec) else len(S)) for i in range(len(sec))]
    rows = [(t, a, b) for t, (a, b) in zip(route, bounds)]
    for t, a, b in rows:
        if not 2 < a <= b <= len(S):
            raise SystemExit("REFUSED: agenda range %r (%d-%d) out of order" % (t, a, b))
    S[1]["items"] = [{"t": "numlist", "x": 0.5, "y": 1.5, "w": 6.3, "h": 3.4, "fs": 12.0, "items": ["%s  (slides %d-%d)" % r for r in rows]},
                     {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
                         {"n": str(len(S)), "label": "slides, numbered bottom-right"},
                         {"n": str(len(ST.STORIES)), "label": "true stories, each with WHO / WHERE / WHEN / READ"},
                         {"n": str(sum(1 for s in S for i in s["items"] if i.get("t") == "code")), "label": "live-run consoles, each shown with its result"}]}]
    S[1]["notes"] = route_notes


def finish(title, version=__version__, redesign=""):
    for s in S:
        if not str(s.get("notes", "")).strip():
            raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
        for line in str(s["notes"]).splitlines():
            if re.match(r"^\s*(?:[A-Z][A-Z \-/&()0-9]{1,24}|say|ask|tell|show|story|cue|demo|note|full text|read|point|click|pause|transition|timing)\s*(?:\([^)]*\))?\s*:", line):
                raise SystemExit("REFUSED: slide %r carries a directive label in its notes: %r" % (s["title"], line[:60]))
        if s["kind"] == "content" and s.get("take") and len(s["take"].split()) > 24:
            raise SystemExit("REFUSED: takeaway %r runs past the gate" % s["take"])
    story_titles = {STORY[k]["title"] for k in STORY} | STORY_TITLES
    missing = [s["title"] for s in S if s["kind"] == "content" and "take" not in s and s["title"] not in story_titles
               and not s["title"].startswith("The questions")]
    if missing:
        raise SystemExit("REFUSED: content slides without a takeaway clue: %r" % missing)
    if len(S) != 26:
        raise SystemExit("REFUSED: %d slides (the lecture standard is 26)" % len(S))
    plan = {"meta": {"title": title, "sub": "SEN0401, third-edition redesign", "version": version, "python": PYV, "total": 0, "redesign": redesign},
            "slides": S}
    out = os.path.join(HERE, "deck_plan_v1_1_0.json")
    json.dump(plan, open(out, "w"), indent=1)
    print("written", out, "-", len(S), "slides")
