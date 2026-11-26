#!/usr/bin/env python3
"""backlog_box_close_links_probe v1.0.0 -- pins what the box tool 3.10.0 close reads by link (Lineage 29, box 66, story CloseByRegister).

It runs the function the close itself calls (`check_opening_names`, which finds the box's iteration by its link, reads which stories were groomed in advance, and refuses a name changed by hand) and `find_task_record`, on small registers whose expected names are WRITTEN OUT HERE, not taken from the tool; then it plants faults in copies of the tool and requires each to be caught.
Registers: box 1 of lineage ex (prefix G), two stories GN_A and GN_B (GN_B's tasks Design and Build), box 10 beside it so that It_G_1 and It_G_10 are different names.
  A. Planned in advance (iteration It_G1, both stories groomed before the box started, no tool-named refinement): the close finds nothing missing.
  B. Opened from nothing (It_G_1, tool-named refinements): nothing missing.
  C. Each name removed by hand in turn (every name of the written list, in both registers) is refused and named; a name missing only because another name starts with it (It_G_1 and It_G_10) is not mistaken for present.
  D. A refinement added by hand after the box started, grooming it, does not stand in for the tool's own refinement; grooming of another story or another box does not count.
  E. A task record is found whole when it is plain, when it carries a pause rationale, when preceded by other text and by a longer name; not taken when it ends otherwise.
  F. The task pattern is anchored at a line start and takes the rationale only.
Usage: backlog_box_close_links_probe.py
"""
import importlib.util, os, re, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(here, "backlog_box_step_v3_10_0.py"), encoding="utf-8").read()

def load(src, tag):
    d = tempfile.mkdtemp(); p = os.path.join(d, "bs_%s.py" % tag)
    open(p, "w", encoding="utf-8").write(src)
    sp = importlib.util.spec_from_file_location("bs_" + tag, p)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m

PRE = ("@prefix backlog: <http://example.org/backlog#> .\n@prefix fw: <http://example.org/backlog-framework-register#> .\n"
       "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
TASKS = {"GN_A": ["Build"], "GN_B": ["Design", "Build"]}
# the names the opening writes for box 1, written out (the part that does not depend on the iteration's name)
COMMON = ["Ceremony_G_Planning1", "DPlan_G_1", "Act_G_1_Validate",
  "Chk_G_1_GN_A", "Plan_G_1_GN_A", "Ev1_ST_G_GN_A_T_Refine", "Ev1_ST_G_GN_A_T_Start", "K_G_1_GN_A_AC", "K_G_1_GN_A_Size", "K_G_1_GN_A_Dep", "K_G_1_GN_A_Input",
  "T_G_GN_A_Build", "Chk_G_1_T_GN_A", "K_G_1_T_GN_A_AC", "K_G_1_T_GN_A_Size", "K_G_1_T_GN_A_Dep", "K_G_1_T_GN_A_Input",
  "Ev1_T_G_GN_A_Build_T_Decompose", "Ev1_T_G_GN_A_Build_T_RefinedToReady", "Ev1_T_G_GN_A_Build_T_Start",
  "Chk_G_1_GN_B", "Plan_G_1_GN_B", "Ev1_ST_G_GN_B_T_Refine", "Ev1_ST_G_GN_B_T_Start", "K_G_1_GN_B_AC", "K_G_1_GN_B_Size", "K_G_1_GN_B_Dep", "K_G_1_GN_B_Input",
  "T_G_GN_B_Design", "Chk_G_1_T_GN_B_Design", "K_G_1_T_GN_B_Design_AC", "K_G_1_T_GN_B_Design_Size", "K_G_1_T_GN_B_Design_Dep", "K_G_1_T_GN_B_Design_Input",
  "Ev1_T_G_GN_B_Design_T_Decompose", "Ev1_T_G_GN_B_Design_T_RefinedToReady", "Ev1_T_G_GN_B_Design_T_Start",
  "T_G_GN_B_Build", "Chk_G_1_T_GN_B", "K_G_1_T_GN_B_AC", "K_G_1_T_GN_B_Size", "K_G_1_T_GN_B_Dep", "K_G_1_T_GN_B_Input",
  "Ev1_T_G_GN_B_Build_T_Decompose", "Ev1_T_G_GN_B_Build_T_RefinedToReady", "Ev1_T_G_GN_B_Build_T_Start"]
REFS = ["Ref_G_1_GN_A", "Ref_G_1_GN_B"]

def iteration(name, n, start):
    return ('fw:%s a backlog:Iteration ; backlog:hasIdentifier "G-BOX-%d" ; backlog:belongsToLineage fw:L_X ;\n    backlog:iterationStart "%s"^^xsd:dateTime .\n' % (name, n, start))

def register(planned, extra=""):
    """A register text holding every name of box 1 (and a box 10 beside it)."""
    t = "# some leading text\n" + PRE + "fw:GN_A a backlog:Story .\nfw:GN_B a backlog:Story .\n"
    t += iteration("It_G_10", 10, "2026-11-25T09:00:00Z")
    if planned:
        t += iteration("It_G1", 1, "2026-11-25T10:00:00Z")
        for st, r in (("GN_A", "Own_A"), ("GN_B", "Own_B")):
            t += "fw:%s a backlog:RefinementEvent ; backlog:refines fw:%s ; backlog:groomsForIteration fw:It_G1 ; backlog:refinedAt \"2026-11-24T10:00:00Z\"^^xsd:dateTime .\n" % (r, st)
    else:
        t += iteration("It_G_1", 1, "2026-11-25T10:00:00Z")
        t += "".join("fw:%s a backlog:RefinementEvent ; backlog:refines fw:%s ; backlog:refinedAt \"2026-11-25T10:00:01Z\"^^xsd:dateTime .\n" % (r, "GN_" + r.split("_")[-1]) for r in REFS)
    t += "".join("fw:%s a backlog:Thing .\n" % i for i in COMMON)
    return t + extra

def refused(bs, text):
    try:
        bs.check_opening_names(text, "G", 1, ["GN_A", "GN_B"], TASKS, "fw:L_X", {"GN_A": "GN_A", "GN_B": "GN_B"})
        return None
    except SystemExit as e:
        return str(e)

def drop(text, name):
    """The record NAME removed from the register text altogether."""
    out, skip = [], False
    for line in text.split("\n"):
        if line.startswith("fw:%s " % name): skip = True
        elif skip and not line.startswith("    "): skip = False
        if not skip: out.append(line)
    return "\n".join(out)

def run_cases(bs):
    o = {}
    pl, op = register(True), register(False)
    o["A planned in advance: nothing missing"] = refused(bs, pl) is None
    o["B opened from nothing: nothing missing"] = refused(bs, op) is None
    for nm in COMMON:
        for tag, reg in (("planned", pl), ("opened", op)):
            msg = refused(bs, drop(reg, nm))
            o["C %s: %s removed by hand is named" % (tag, nm)] = bool(msg) and nm in msg or bool(msg) and nm in (msg or "")
    # the planned iteration and the tool's own names
    o["C planned: the planned iteration removed is refused"] = refused(bs, drop(pl, "It_G1")) is not None
    o["C opened: the iteration removed is refused (It_G_10 does not stand in for It_G_1)"] = refused(bs, drop(op, "It_G_1")) is not None
    for r in REFS:
        o["C opened: %s removed is named" % r] = (refused(bs, drop(op, r)) or "").find(r) >= 0
    # D
    late = op.replace("fw:Ref_G_1_GN_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ;", "fw:Late_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ; backlog:groomsForIteration fw:It_G_1 ;")
    o["D a grooming refinement made after the box started does not stand in for the tool's own"] = (refused(bs, late) or "").find("Ref_G_1_GN_A") >= 0
    other_story = op.replace("fw:Ref_G_1_GN_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ;", "fw:Late_A a backlog:RefinementEvent ; backlog:refines fw:GN_B ; backlog:groomsForIteration fw:It_G_1 ; backlog:refinedAt \"2026-11-24T10:00:00Z\"^^xsd:dateTime ;")
    o["D grooming of another story does not count for this one"] = (refused(bs, other_story) or "").find("Ref_G_1_GN_A") >= 0
    other_box = op.replace("fw:Ref_G_1_GN_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ;", "fw:Late_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ; backlog:groomsForIteration fw:It_G_10 ; backlog:refinedAt \"2026-11-24T10:00:00Z\"^^xsd:dateTime ;")
    o["D grooming for another box does not count"] = (refused(bs, other_box) or "").find("Ref_G_1_GN_A") >= 0
    # E, F
    plain = 'fw:T_X a backlog:ExecutionTask ; backlog:hasIdentifier "T-1.0" ; backlog:hasState backlog:InProgress ;\n    backlog:startedAt "2026-11-20T14:56:50Z"^^xsd:dateTime .\nfw:Z a backlog:Thing .\n'
    paused = 'fw:T_X a backlog:ExecutionTask ; backlog:hasState backlog:InProgress ;\n    backlog:startedAt "2026-11-20T14:56:50Z"^^xsd:dateTime ;\n    backlog:hasRationale "paused by \\"u\\": a. b" .\nfw:Z a backlog:Thing .\n'
    other = 'fw:T_X a backlog:ExecutionTask ; backlog:startedAt "2026-11-20T14:56:50Z"^^xsd:dateTime ; backlog:hasEvidence fw:E .\n'
    mp, mq, mo = bs.find_task_record(plain, "T_X"), bs.find_task_record(paused, "T_X"), bs.find_task_record(other, "T_X")
    o["E a plain task record is found whole"] = bool(mp) and mp.group(0).rstrip().endswith("xsd:dateTime .") and "fw:Z" not in mp.group(0)
    o["E a paused task record is found whole, with its rationale"] = bool(mq) and "a. b" in mq.group(0) and mq.group(0).rstrip().endswith('b" .') and "fw:Z" not in mq.group(0)
    o["E a record with another tail is not taken"] = mo is None
    twice = paused.replace('b" .', 'b" ;\n    backlog:hasRationale "paused again by \\"v\\": c" .')
    mt = bs.find_task_record(twice, "T_X")
    o["E a task held by two pauses (two rationales) is found whole"] = bool(mt) and "paused again" in mt.group(0) and "fw:Z" not in mt.group(0)
    undated = op.replace("fw:Ref_G_1_GN_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ; backlog:refinedAt \"2026-11-25T10:00:01Z\"^^xsd:dateTime .", "fw:Late_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ; backlog:groomsForIteration fw:It_G_1 .")
    tie = op.replace("fw:Ref_G_1_GN_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ; backlog:refinedAt \"2026-11-25T10:00:01Z\"^^xsd:dateTime .", "fw:Late_A a backlog:RefinementEvent ; backlog:refines fw:GN_A ; backlog:groomsForIteration fw:It_G_1 ; backlog:refinedAt \"2026-11-25T10:00:00Z\"^^xsd:dateTime .")
    o["D a grooming made at the moment the box started is not in advance"] = (refused(bs, tie) or "").find("Ref_G_1_GN_A") >= 0
    o["D an undated refinement grooming the box does not stand in for the tool's own"] = (refused(bs, undated) or "").find("Ref_G_1_GN_A") >= 0
    lead = "fw:Other a backlog:ExecutionTask ; backlog:startedAt \"2026-11-20T14:00:00Z\"^^xsd:dateTime .\n" + paused
    ml = bs.find_task_record(lead, "T_X")
    o["E a record after another is found alone"] = bool(ml) and "fw:Other" not in ml.group(0)
    mid = 'fw:Pre a backlog:Thing ; rdfs:comment "x fw:T_X a backlog:ExecutionTask ; backlog:startedAt "2026-11-20T14:56:50Z"^^xsd:dateTime ." .\n'
    o["F the task pattern is anchored at a line start"] = bs.find_task_record(mid, "T_X") is None
    longer = plain.replace("fw:T_X ", "fw:T_XY ")
    o["F a longer name is not taken for a shorter one"] = bs.find_task_record(longer, "T_X") is None
    return o

MUT = [
 ("an undated refinement counts as grooming", 'return False   # a refinement with no time', 'return True   # a refinement with no time'),
 ("grooming at the very start counts", 'return a < b', 'return a <= b'),
 ("a second rationale not allowed", '\\.)*\\")* \\."', '\\.)*\\")? \\."'),
 ("close ignores the found iteration", 'it = resolve_it_id(type("Text", (), {"s": text})(), P, n, L)', 'it = "It_%s_%d" % (P, n)'),
 ("grooming never read", 'return {k for k, sid in story_of.items()\n            if any(', 'return set() if True else {k for k, sid in story_of.items()\n            if any('),
 ("every story read as groomed", 'groomed = groomed_stories(text, it, story_of)', 'groomed = set(story_of)'),
 ("grooming not tied to the box", '(r, BB.groomsForIteration, N[it]) in g and before(r)', '(r, BB.groomsForIteration, None) in g and before(r)'),
 ("grooming after the start counts", 'return a < b', 'return True'),
 ("grooming of any story counts", 'for r in g.subjects(BB.refines, N[sid]))}', 'for r in g.subjects(BB.refines, None))}'),
 ("old task pattern", '(?: ;\\s*backlog:hasRationale \\"(?:[^\\"\\\\]|\\\\.)*\\")* \\."', ' \\."'),
 ("widened task pattern", '(?: ;\\s*backlog:hasRationale \\"(?:[^\\"\\\\]|\\\\.)*\\")* \\."', '(?: ;[^\\n]*)? \\."'),
 ("task pattern without line anchor", 'TASK_RECORD = r"^fw:%s a', 'TASK_RECORD = r"fw:%s a'),
 ("task record cut at the first full stop", 'TASK_RECORD = r"^fw:%s a backlog:ExecutionTask .*?', 'TASK_RECORD = r"^fw:%s a backlog:ExecutionTask [^.]*?'),
 ("by-hand refusal disabled", '    if gone:\n        raise SystemExit("REFUSED: %d identifier(s) written at the opening of box %d are gone, so a name was changed by hand: %s" % (len(gone), n, ", ".join(gone[:3])))\n\n\ndef whole', '    if False:\n        raise SystemExit("x")\n\n\ndef whole'),
 ("readiness check dropped from the names", '+ ["Chk_%s_%d_%s" % (P, n, k), "Plan_%s_%d_%s" % (P, n, k),', '+ ["Plan_%s_%d_%s" % (P, n, k),'),
 ("planning event dropped from the names", ', "Plan_%s_%d_%s" % (P, n, k),', ','),
 ("name match without a word end", 'if not re.search(r"^fw:%s\\s" % re.escape(i), text, re.M)]', 'if not re.search(r"^fw:%s" % re.escape(i), text, re.M)]'),
 ("story looked up by another name", 'g.subjects(BB.refines, N[sid])', 'g.subjects(BB.refines, N["ST_" + sid])'),
 ("deployment plan dropped from the names", 'out = [it or ids["it"], ids["plan"], ids["dplan"], ids["act"]]', 'out = [it or ids["it"], ids["plan"], ids["act"]]'),
]
bad = 0
def check(name, ok):
    global bad
    print(("PASS " if ok else "FAIL ") + name); bad += (not ok)
res = run_cases(load(SRC, "base"))
fails = [k for k, v in res.items() if not v]
for k in fails: check(k, False)
print("%d expectations on the tool as it is: %d hold" % (len(res), len(res) - len(fails))); bad += len(fails)
for name, old, new in MUT:
    if old not in SRC: check("mutant '%s' could be planted" % name, False); continue
    try: caught = not all(run_cases(load(SRC.replace(old, new, 1), "m")).values())
    except Exception: caught = True
    check("mutant '%s' is caught" % name, caught)
sys.exit(1 if bad else 0)
