#!/usr/bin/env python3
"""sen0401_notes_rewrite v1.0.0 - rewrites the speaker notes of a deck PLAN into short reader's prose and changes nothing else (same slides, items, titles).
Owner's two rules reconciled (decided from the files, 2026-10-15): notes are SHORT (preference) and reader's prose with no presenter labels (ruling of 2026-10-08):
2 to 4 full sentences, at most 100 words, one paragraph, no directive label. Input styles handled:
  labelled  'SAY: ...\\nASK: ...\\nFULL TEXT: course page, chapter N - A, B.'   ->  the SAY sentences, 'A question to think about is this: ...', 'The full explanation is on the course page, chapter N, in A and B.'
            'STORY (date): ...\\nSOURCE: ...'                                  ->  'This is a true story, dated D.' + the first two sentences of the story + 'The source is ...'
  prose     already reader's prose (ch06/07 style): kept when within the limit; otherwise cut to the leading sentences, keeping the closing pointer to the course page, and for a story the date, the first story sentence and the lesson.
Usage: sen0401_notes_rewrite_v1_0_0.py <plan_in.json> <plan_out.json> [--max-words 100] [--max-sentences 4]      Prints one line per changed slide (words before -> after)."""
__version__ = "1.0.0"
import json, re, sys
a = sys.argv[1:]
if len(a) < 2:
    sys.exit(__doc__)
MW = int(a[a.index("--max-words") + 1]) if "--max-words" in a else 100
MS = int(a[a.index("--max-sentences") + 1]) if "--max-sentences" in a else 4
def sents(t):
    t = re.sub(r"\b(Mt|Dr|St|Mr|Mrs|vs|No|approx)\.\s", lambda m: m.group(1) + ".\x00", t.strip())
    return [s.replace("\x00", " ") for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9'\"(])", t) if s]


LAB = {}
if "--corpus" in a:     # a chapter corpus module (NODES: name, label, ...) gives the human labels of the concepts the notes point to
    import importlib.util
    _sp = importlib.util.spec_from_file_location("corp", a[a.index("--corpus") + 1]); _m = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_m)
    LAB = {n[0]: (n[1] or n[0]) for n in _m.NODES}


def human(x):
    if x in LAB:
        return LAB[x]
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", x).replace("  ", " ").lower().capitalize() if re.fullmatch(r"[A-Za-z0-9]+", x) and re.search(r"[a-z][A-Z]", x) else x
join = lambda ss: " ".join(s if re.search(r"[.!?][\"')]*$", s) else s + "." for s in ss)


def cap(ss):
    ss = list(ss)
    tail = ss[-1] if ss and re.match(r"(The full explanation|The full text|The source)", ss[-1]) else None
    while len(ss) > MS or (len(" ".join(ss).split()) > MW and len(ss) > 2):
        if tail and len(ss) > 2:
            del ss[-2]
        else:
            ss.pop()
    return ss


def labelled(n):
    f = {}
    for k, v in re.findall(r"^(SAY|ASK|FULL TEXT|STORY \([^)]*\)|SOURCE):\s*(.*?)(?=^\w[\w ]*(?: \([^)]*\))?:|\Z)", n + "\n", re.S | re.M):
        f[k.split(" (")[0]] = (v.strip(), re.findall(r"\(([^)]*)\)", k)[:1])
    out = []
    if "STORY" in f:
        when = f["STORY"][1][0] if f["STORY"][1] else ""
        st = sents(f["STORY"][0])
        out += ["This is a true story, dated %s." % when] + st[:2]
        if "SOURCE" in f:
            src = re.split(r"\s+Photo:", f["SOURCE"][0])[0]
            out.append("The source is " + (src[0].lower() + src[1:] if re.match(r"(The|A|An) ", src) else src).rstrip(".") + ".")
        return out
    say = sents(f["SAY"][0]) if "SAY" in f else []
    out += say[:2]
    if "ASK" in f:
        q = re.split(r"\s+-\s+", f["ASK"][0].strip())[0]
        asked = "?" in q
        q = (q[:q.index("?") + 1] if asked else q).rstrip(".?!")
        q = q[0].lower() + q[1:] if len(q) > 1 and not q[1].isupper() else q
        if re.match(r"(what|why|which|where|when|how|who|does|do|is|are|can|could|would|should|will)\b", q):
            out.append("A question to think about is this: %s?" % q)
        else:
            out.append("Think about this case: %s%s" % (q, "?" if asked else "."))
    if "FULL TEXT" in f:
        m = re.match(r"course page, (chapter \d+)(?:\s*-\s*(.*))?$", f["FULL TEXT"][0].rstrip("."))
        if m:
            parts = [human(x.strip()) for x in (m.group(2) or "").split(",") if x.strip()]
            where = (" in " + (parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1])) if parts else ""
            out.append("The full explanation is on the course page, %s,%s." % (m.group(1), where) if where else "The full explanation is on the course page, %s." % m.group(1))
        else:
            out.append("The full explanation is on the course page.")
    return out


def prose(n):
    ss = sents(n)
    if ss and ss[0].startswith("This is a true story"):
        les = [s for s in ss if s.startswith("The lesson the slide carries")]
        les = ["The lesson is this: " + (lambda t: t[0].upper() + t[1:])(re.sub(r"^The lesson the slide carries is that ", "", l).rstrip(".")) + "." for l in les[:1]]
        return ss[:3] + les
    return ss


plan = json.load(open(a[0]))
for i, s in enumerate(plan["slides"], 1):
    n = s.get("notes", "") or ""
    before = len(n.split())
    if re.match(r"^\s*(SAY|STORY)\b", n):
        ss = labelled(n)
    else:
        ss = prose(n)
        if len(ss) <= MS and before <= MW and ss and not ss[0].startswith("This is a true story"):
            continue
    ss = cap(ss)
    new = join(ss)
    if new != n:
        s["notes"] = new
        print("slide %2d: %3d -> %3d words, %d sentences" % (i, before, len(new.split()), len(ss)))
if "meta" in plan:
    plan["meta"]["notes"] = "short reader's prose (sen0401_notes_rewrite_v1_0_0.py): 2-4 sentences, at most %d words" % MW
json.dump(plan, open(a[1], "w"), indent=1)
