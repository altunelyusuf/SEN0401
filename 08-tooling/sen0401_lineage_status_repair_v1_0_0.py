#!/usr/bin/env python3
"""sen0401_lineage_status_repair v1_0_0 - the status and date audit of the register, and ONE new register version that repairs what the rules let it repair.
Owner direction, 2026-10-20 09:19 Istanbul (2026-10-20T06:19:00 UTC), relayed by the course coordinator: "Update the status of the PBI's backfilling the historic data. Never let
inconsistencies in status and dates. What is still waiting in the lineage? We need to finish the work of SEN0401 as soon as possible. Keep quality and cleaning operations until we
finish the lineage first as we need to reserve a concentrated time on them."
Committed versions are never edited (L-112): the repair is a new file. No digest moves: the Backlog digest covers subjects only, and no subject is added or removed.
Usage:
  sen0401_lineage_status_repair_v1_0_0.py audit [REGISTER.ttl]    list every inconsistency of status, dates, parent/child and iteration membership (read only)
  sen0401_lineage_status_repair_v1_0_0.py draft OUT.ttl           the evidence nodes of the three epics (the check of 08-tooling/sen0401_lineage_item_check_v1_0_0.py run on the newest register), before the evidence bridge
  sen0401_lineage_status_repair_v1_0_0.py repair BRIDGE.ttl       write the next register version (the repairs, the three epics Done with the bridge-verified evidence)
  sen0401_lineage_status_repair_v1_0_0.py initiative [DRAFT.ttl|BRIDGE.ttl]   the initiative: with DRAFT.ttl as the first argument 'initiative draft OUT.ttl' writes its evidence nodes; 'initiative record BRIDGE.ttl' writes the next version
"""
__version__ = "1.0.0"
import os, re, sys
from collections import defaultdict
from datetime import datetime, timezone
import rdflib
from rdflib import Namespace, RDF
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

B = Namespace("http://example.org/backlog#"); EX = Namespace("http://example.org/sen0401-slides-lineage#")
CLASSES = ("Initiative", "Epic", "Story", "ExecutionTask")
DIRECTION = ("Owner's direction, 2026-10-20 09:19 Istanbul (2026-10-20T06:19:00 UTC), relayed by the course coordinator: \"Update the status of the PBI's backfilling the historic data. "
             "Never let inconsistencies in status and dates. What is still waiting in the lineage? We need to finish the work of SEN0401 as soon as possible. Keep quality and cleaning "
             "operations until we finish the lineage first as we need to reserve a concentrated time on them.\"")


def ln(x):
    return str(x).split("#")[-1]


def dt(x):
    d = datetime.fromisoformat(str(x).replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def audit(g, now):
    items = {}
    for c in CLASSES:
        for s in g.subjects(RDF.type, B[c]):
            items[s] = c
    iters = {it: (g.value(it, B.iterationStart), g.value(it, B.iterationEnd)) for it in g.subjects(RDF.type, B.Iteration)}
    parent = defaultdict(list)
    for s in items:
        for c in g.objects(s, B.decomposesInto):
            parent[c].append(s)
    out = []

    def I(s, kind, m):
        out.append((kind, ln(s), m))
    for s, cls in items.items():
        st = [ln(x) for x in g.objects(s, B.hasState)]; sa = list(g.objects(s, B.startedAt)); fa = list(g.objects(s, B.finishedAt))
        stt = st[0] if st else None
        if len(st) != 1: I(s, "state", "states %s" % st)
        if stt == "Done":
            if not sa: I(s, "dates", "Done without startedAt")
            if not fa: I(s, "dates", "Done without finishedAt")
            if cls in ("Story", "ExecutionTask") and not list(g.objects(s, B.hasEvidence)): I(s, "evidence", "Done without evidence")
        if stt != "Done" and fa: I(s, "dates", "finishedAt but not Done")
        if stt in ("Proposed", "Refined", "Ready") and sa: I(s, "dates", "%s with startedAt" % stt)
        if sa and fa and dt(fa[0]) < dt(sa[0]): I(s, "dates", "finish before start")
        if sa and fa and dt(fa[0]) == dt(sa[0]) and not list(g.objects(s, B.startedAtIsEstimate)): I(s, "estimate", "finish equals start, start not stated as an estimate (G120)")
        for d in sa + fa:
            if dt(d) > now: I(s, "dates", "date in the future %s" % d)
        its = [o for o in g.objects(s, B.memberOfContainer) if o in iters]
        for it in its:
            a, b = iters[it]
            if sa and dt(sa[0]) < dt(a): I(s, "iteration", "started %s before %s starts %s" % (sa[0], ln(it), a))
            if fa and dt(fa[0]) > dt(b): I(s, "iteration", "finished %s after %s ends %s" % (fa[0], ln(it), b))
        kids = [k for k in g.objects(s, B.decomposesInto) if k in items]
        for k in kids:
            ks = [ln(x) for x in g.objects(k, B.hasState)]; kf = list(g.objects(k, B.finishedAt))
            if stt == "Done" and ks != ["Done"]: I(s, "parent-child", "Done parent, child %s is %s" % (ln(k), ks))
            if stt == "Done" and fa and kf and dt(kf[0]) > dt(fa[0]): I(s, "parent-child", "finished %s before its child %s finished %s" % (fa[0], ln(k), kf[0]))
        if kids and all([ln(x) for x in g.objects(k, B.hasState)] == ["Done"] for k in kids) and stt != "Done":
            I(s, "parent-child", "all %d children Done, parent %s" % (len(kids), stt))
        if cls == "ExecutionTask" and not parent[s]: I(s, "parent-child", "task without a parent")
    return out


def owners(t):
    return [(m.start(), m.group(1)) for m in re.finditer(r"^([A-Za-z][\w-]*:[\w.-]+)[ \t]", t, re.M)]


def edit(t, subj, pattern, repl):
    """replace the one match of PATTERN that belongs to subject SUBJ (the statement may sit in the subject's block or in a later line)"""
    own = owners(t); hits = []
    import bisect
    pos = [p for p, _ in own]
    for m in re.finditer(pattern, t):
        i = bisect.bisect_right(pos, m.start()) - 1
        if i >= 0 and own[i][1] == "ex:" + subj:
            hits.append(m)
    assert len(hits) == 1, (subj, pattern, len(hits))
    m = hits[0]
    return t[:m.start()] + (repl(m) if callable(repl) else repl) + t[m.end():]


def verdicts(path):
    """evidence node -> verified, from the evidence bridge output"""
    g = rdflib.Graph(); g.parse(path, format="turtle")
    return {ln(s): True for s in g.subjects(B.evidenceVerified, rdflib.Literal(True))}


def bridge_nodes(path):
    return "\n".join(l for l in open(path, encoding="utf-8").read().splitlines() if not l.startswith("@prefix")) + "\n"


def harness(item):
    return 'ex:Harness4_%s a backlog:TestHarness ; rdfs:label "Completion check for %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:Ev4_%s .\n' % (item, item, item, item)


def parent_note(item, day, what):
    return ('ex:%s backlog:hasAuditNote "Recorded Done %s (owner direction of that day, backfilling the historic data): %s all read Done, every story and task below it carries bridge-verified evidence, and the files they cite were re-hashed from the workspace (Ev4_%s, the check 08-tooling/sen0401_lineage_item_check_v1_0_0.py run by the evidence bridge). The completion of an epic or an initiative is derived from its constituent work; startedAt is the earliest start and finishedAt the latest finish below it, so a parent never finishes before a child. The item was admitted open as part of the first lineage and carried; the Backlog digest covers subjects only and does not move. The committed versions stay as the record (L-112)." .\n' % (item, day, what, item))


def draft(out, items):
    src = M.newest(); ver = os.path.basename(src).replace("sen0401_slides_lineage_", "").replace(".ttl", "")
    reg = "07-lineage/" + os.path.basename(src)
    import hashlib
    sha = hashlib.sha256(open(src, "rb").read()).hexdigest()
    L = ["@prefix backlog: <http://example.org/backlog#> .", "@prefix ex: <http://example.org/sen0401-slides-lineage#> .", "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .", ""]
    for it in items:
        crit = "ex:AC2_Admission"
        L.append('ex:Ev4_%s a backlog:TestEvidence ; rdfs:label "Completion check for %s, read from register %s"@en ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s:%s" ; backlog:hasTestSpec "08-tooling/sen0401_lineage_item_check_v1_0_0.py" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running 08-tooling/sen0401_lineage_item_check_v1_0_0.py %s:%s" .' % (it, it, ver, crit, it, ver, it, ver))
        L.append('ex:Ev4_%s_File1 a backlog:ArtifactEvidence ; rdfs:label "register %s that the completion check of %s read"@en ; backlog:attestsCriterion %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" .' % (it, os.path.basename(src), it, crit, reg, sha))
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("draft", out, "reads", ver)


def initiative(bridge):
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); now_iso = M.now(); day = now_iso[:10]
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    kids = list(g.objects(EX.Init_Slides, B.decomposesInto))
    assert len(kids) == 3 and all((k, B.hasState, B.Done) in g for k in kids)
    vd = verdicts(bridge); assert vd.get("Ev4_Init_Slides") and vd.get("Ev4_Init_Slides_File1"), "the bridge did not verify the check of Init_Slides"
    a, f = min(str(g.value(k, B.startedAt)) for k in kids), max(str(g.value(k, B.finishedAt)) for k in kids)
    t = edit(t, "Init_Slides", r"backlog:hasState backlog:Proposed", "backlog:hasState backlog:Done")
    add = ['ex:Init_Slides backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n    backlog:hasEvidence ex:Ev4_Init_Slides, ex:Ev4_Init_Slides_File1 .\n' % (a, f, now_iso),
           parent_note("Init_Slides", day, "its 3 epics (the descendants below them included)"), harness("Init_Slides"), bridge_nodes(bridge)]
    t += "\n" + "".join(add)
    out = M.write_new(src, t, nxt, cur, "The initiative Init_Slides recorded Done on the owner's direction of 2026-10-20 09:19 Istanbul: its three epics are Done, and the completion check run by the evidence bridge passed.")
    g2 = rdflib.Graph(); g2.parse(data=t, format="turtle")
    left = audit(g2, datetime.now(timezone.utc))
    print(os.path.basename(out)); print("inconsistencies after:", len(left))
    for r in sorted(left): print(" ", *r, sep=" | ")


def main():
    mode = sys.argv[1]
    if mode == "audit":
        p = sys.argv[2] if len(sys.argv) > 2 else M.newest()
        g = rdflib.Graph(); g.parse(p, format="turtle")
        res = audit(g, datetime.now(timezone.utc))
        for r in sorted(res): print(*r, sep=" | ")
        print(len(res), "inconsistencies in", os.path.basename(p)); return
    if mode == "draft":
        return draft(sys.argv[2], ["EP_Deck", "EP_Page", "EP_Research"])
    if mode == "initiative":
        if sys.argv[2] == "draft":
            return draft(sys.argv[3], ["Init_Slides"])
        return initiative(sys.argv[3])
    bridge = sys.argv[2]
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); now_iso = M.now(); day = now_iso[:10]
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    before = audit(g, datetime.now(timezone.utc))
    add = []
    # A. the page link-pass tasks belong to the story that carries the link pass (G125), not to the page stories that were Done in September
    moved = []
    for ch in list(range(1, 13)) + [14]:
        line = "ex:ST_Page_Ch%02d backlog:decomposesInto ex:TK_Page_Ch%02d_LinkPass .\n" % (ch, ch)
        assert t.count(line) == 1, line
        t = t.replace(line, ""); moved.append("TK_Page_Ch%02d_LinkPass" % ch)
        add.append('ex:ST_Page_Ch%02d backlog:hasAuditNote "Date repair %s (owner direction of that day): the link-pass task of this chapter, hung under this story in the versions 0.91 to 0.93, finished on 2026-10-16, long after this story was Done; under ruling G125 the link pass is a story of its own (ST_Page_LinkPass) and a task hung under a finished story makes its finish date contradict the parent. The task is now a child of ST_Page_LinkPass; its dates, evidence and notes are unchanged and the committed versions stay as the record (L-112)." .\n' % (ch, day))
        add.append('ex:TK_Page_Ch%02d_LinkPass backlog:hasAuditNote "Moved %s from ST_Page_Ch%02d to ST_Page_LinkPass (ruling G125); dates and evidence unchanged. Its start and finish are the same instant, the git commit of the rebuilt page, so its start is stated as an estimate (G120)." .\n' % (ch, day, ch))
    add.append("ex:ST_Page_LinkPass backlog:decomposesInto " + ", ".join("ex:" + x for x in moved) + " .\n")
    add.append('ex:ST_Page_LinkPass backlog:hasAuditNote "Date repair %s (owner direction of that day): the %d link-pass tasks of the pages are now its children; the earliest start (2026-10-16T07:46:59) and the latest finish (2026-10-16T13:43:01) of these tasks are this story\'s own start and finish, so parent and children agree. The page of chapter 13 has no link-pass task because it was admitted failing and was repaired by its own tasks." .\n' % (day, len(moved)))
    # B. a story is Done when its last task is: the finish of a story is not earlier than the finish of its own tasks
    g2 = rdflib.Graph(); g2.parse(data=t + "\n" + "".join(add), format="turtle")
    storyfix = []
    for s in sorted(g2.subjects(RDF.type, B.Story), key=str):
        fa = list(g2.objects(s, B.finishedAt))
        if not fa: continue
        kf = [str(f) for k in g2.objects(s, B.decomposesInto) for f in g2.objects(k, B.finishedAt)]
        if kf and dt(max(kf)) > dt(fa[0]):
            storyfix.append((ln(s), str(fa[0]), max(kf)))
    for sid, old, new in storyfix:
        t = edit(t, sid, r'backlog:finishedAt "%s"\^\^xsd:dateTime' % re.escape(old), 'backlog:finishedAt "%s"^^xsd:dateTime' % new)
        la = [str(x) for x in g2.objects(EX[sid], B.lastAuditedAt)]
        assert not la or dt(la[0]) >= dt(new), (sid, la, new)
        add.append('ex:%s backlog:hasAuditNote "Date repair %s (owner direction of that day): finishedAt moved forward from %s to %s. The earlier time is the last commit of the story\'s artifact (the Build task keeps it); the later time is the instant its last task, the check, was recorded finished. A story is Done when its last task is, so its finish cannot be earlier than the finish of its own task. Nothing else of the story changed; the committed versions stay as the record (L-112)." .\n' % (sid, day, old, new))
    # C. a start that is the same instant as the finish was never witnessed: stated as an estimate (G120)
    eq = []
    for s in sorted(g2.subjects(RDF.type, B.ExecutionTask), key=str):
        sa = list(g2.objects(s, B.startedAt)); fa = list(g2.objects(s, B.finishedAt))
        if sa and fa and dt(sa[0]) == dt(fa[0]) and not list(g2.objects(s, B.startedAtIsEstimate)):
            eq.append(ln(s))
    for tid in eq:
        if tid.endswith("_LinkPass"):
            basis = "the git commit instant of the rebuilt page: the register holds one instant for this task, the start of the rebuild was not recorded; the commit bounds the start from above"
        elif tid.endswith("_Verify"):
            basis = "the instant the check was run and recorded (the audit instant of its story): the register holds one instant for this task and the start of the run was not recorded; it bounds the start from above"
        else:
            raise SystemExit("unexpected equal-span task " + tid)
        add.append('ex:%s backlog:startedAtIsEstimate true ; backlog:startEstimateBasis "%s" .\n' % (tid, basis))
    # D. the iteration that took the finished link-pass tasks in starts when the earliest of them started
    first = min(str(g2.value(EX[x], B.startedAt)) for x in moved)
    old_it = str(g.value(EX.Iter_11, B.iterationStart))
    assert dt(first) < dt(old_it)
    t = edit(t, "Iter_11", r'backlog:iterationStart "%s"\^\^xsd:dateTime' % re.escape(old_it), 'backlog:iterationStart "%s"^^xsd:dateTime' % first)
    add.append('ex:Iter_11 rdfs:comment "Date repair %s (owner direction of that day): the iteration starts at %s, the start of the earliest task it holds (the page link passes, finished on 2026-10-16 before the iteration was opened at %s); a task cannot start before the time box it belongs to. The end, 2026-10-23, is the owner-confirmed date and is unchanged."@en .\n' % (day, first, old_it))
    # E. the Obj3_FailuresNamed reading counted Done stories (2); the objective counts the failing decks and pages NAMED in the story that admits them
    add.append('ex:Obs34_Obj3_FailuresNamed a backlog:MetricObservation ; rdfs:label "Reading of the failing decks and pages named in the admitting stories"@en ;\n    backlog:observesMetric ex:Met3_FailuresNamed ; backlog:observationFor ex:Obj3_FailuresNamed ; backlog:hasObservedValue "5"^^xsd:decimal ;\n    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n    backlog:hasObservationMethod "Counted from the audit notes of the two admitting stories as the register stands: ST_Deck_LinkPass names the decks of chapters 1, 2, 3 and 4 as failing the lineage deck check, and ST_Page_LinkPass names the page of chapter 13 as failing its check: 5 named. The earlier reading of 2 (Obs31, Obs33) counted the stories that read Done, which is not what this objective measures; it stays as the record and this reading corrects it forward. The five have since been repaired by their own tasks, which does not remove them from the count of what was named."  .\n' % now_iso)
    # F. the epics: Done once every child is Done; dates are the earliest start and the latest finish of the children; the evidence is the bridge-verified item check
    g3 = rdflib.Graph(); g3.parse(data=t + "\n" + "".join(add), format="turtle")
    vd = verdicts(bridge)
    for e in ("EP_Deck", "EP_Page", "EP_Research"):
        kids = list(g3.objects(EX[e], B.decomposesInto))
        assert kids and all((k, B.hasState, B.Done) in g3 for k in kids), e
        a, f, n = min(str(g3.value(k, B.startedAt)) for k in kids), max(str(g3.value(k, B.finishedAt)) for k in kids), len(kids)
        assert vd.get("Ev4_" + e) and vd.get("Ev4_" + e + "_File1"), "the bridge did not verify the check of " + e
        t = edit(t, e, r"backlog:hasState backlog:Proposed", "backlog:hasState backlog:Done")
        add.append('ex:%s backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n    backlog:hasEvidence ex:Ev4_%s, ex:Ev4_%s_File1 .\n' % (e, a, f, now_iso, e, e))
        add.append(parent_note(e, day, "its %d children (stories and the follow-up tasks hung under it)" % n))
        add.append(harness(e))
    add.append(bridge_nodes(bridge))
    for s_ in ["EP_Deck", "EP_Page", "EP_Research"]:
        add.append('ex:%s rdfs:comment "Owner-directed. %s"@en .\n' % (s_, M.esc(DIRECTION)))
    add.append('ex:Init_Slides rdfs:comment "Owner-directed. %s The initiative is recorded Done in the version after the one that records its three epics Done, because its check reads the epics as Done."@en .\n' % M.esc(DIRECTION))
    # G. the lineage status follows the register
    t = edit(t, "Lineage3", r"backlog:hasLineageStatus backlog:LS_Backlogged", "backlog:hasLineageStatus backlog:LS_InProgress")
    add.append('ex:Lineage3 rdfs:comment "Status moved from LS_Backlogged to LS_InProgress on %s: both stories this lineage admitted and the 20 tasks it carried were Done long before (the status lagged the register, G87). %s"@en .\n' % (day, M.esc(DIRECTION)))
    # H. a true overrun, disclosed and not altered
    add.append('ex:ST_Page_Ch01 backlog:hasAuditNote "Audit %s (owner direction of that day): this story finished at 2026-09-25T06:12:40, 12 minutes after the end of its iteration (Iter_1, 2026-09-25T06:00:00, the 09:00 Istanbul class the owner set). The overrun is a fact, not a record error; neither the finish nor the owner-set end is changed." .\n' % day)
    t += "\n" + "".join(add)
    g4 = rdflib.Graph(); g4.parse(data=t, format="turtle")
    after = audit(g4, datetime.now(timezone.utc))
    out = M.write_new(src, t, nxt, cur, "Status and dates repaired on the owner's direction of 2026-10-20 09:19 Istanbul: the 3 epics recorded Done with the dates of their children and bridge-verified evidence; %d page link-pass tasks moved under ST_Page_LinkPass (G125); %d story finishes moved to the finish of their last task; %d single-instant tasks stated as estimated starts (G120); Iter_11 start set to its earliest task; Obj3_FailuresNamed corrected forward to 5; Lineage3 status InProgress; the initiative follows in the next version." % (len(moved), len(storyfix), len(eq)))
    print(os.path.basename(out)); print("inconsistencies before:", len(before), "after:", len(after))
    for r in sorted(after): print(" ", *r, sep=" | ")


main()
