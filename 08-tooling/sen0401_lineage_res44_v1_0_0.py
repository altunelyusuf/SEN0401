#!/usr/bin/env python3
"""sen0401_lineage_res44 v1_0_0 - (second repair of the chapter 3 page, copy of res40; the first repair v9_75_0 failed the lineage agent control run of 2026-11-02) (was: copy of res38 for the repair of the chapter 3 page v9_74_0: a defect found by the lineage agent in the quiet window of 2026-11-01) change route (G125 route 2, G133, G147) for the owner's words of 2026-11-01 13:04 Istanbul on the exam: the IKU cover page as page 1, five question formats (4 x 25 points, the 5th 10 points bonus), no memorising items, tips for terms, abbreviations spelled out, 4 pages (else 6). Adds the stories of the cover renderer, items v1.2.0, papers/key/sheet v3, the honesty-check successor and the Ch05 Teach repair task. Usage: change | retract | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys, glob, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_retro24_v1_0_0 as RT
R = RT.R; lit = G.lit
def _pv_newest():
    fw = X.FW; vk = lambda q: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", q)[0]]
    spec = importlib.util.spec_from_file_location("pv", sorted(glob.glob(fw + "/03-tooling/backlog_pipeline_verify_v*.py"), key=vk)[-1])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.STAGE_TYPES = m._load_stage_types(sorted(glob.glob(fw + "/01-ontologies/backlog_tbox_v*.ttl"), key=vk)[-1], table="v4")
    return m
X._pv = _pv_newest



import json
REV = "ex:Revision_Lineage3_Backlog22"; OLD = "ex:Out3_BacklogR49"; NEWB = "ex:Out3_BacklogR50"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_Ch03PageRepair2"; IA = "ex:IA3_Ch03PageRepair2"
WHEN = "Monday 2026-11-02, on the lineage agent's own control run of the first repair, relayed by the coordinator"
WORDS = ("DEFECT (measured by the lineage agent, 2026-11-02, control of the repair page v9_75_0, test 9.38.0 unchanged, under one lock hold with the shipped v9_73_0 run straight after it, machine load average 6.4 at the start of the first run and 3.3 at the second): chapter 3 page v9_75_0 (the first repair) FAILS the main-thread budget feature: 396 passed 2 failed, load task median 145 ms of [131, 141, 145, 214] (bound 227, passes), but after load ONE main-thread task of 2063 ms (the printed 'after load' value is the longest task after 5000 ms; 28 long tasks in all). The shipped v9_73_0 in the next hold: 398 passed 0 failed, longest 143 ms. The executor's own two runs of v9_75_0 passed (after load 68 ms over 2 long tasks and 78 ms over 5), so the failure is intermittent or load dependent, and the first repair is not Done. KNOWN FROM THE FIRST REPAIR (its bisect logs in 08-tooling/ch03-page/page_9_75_0_logs/bisect/RESULTS.txt): on v9_74_0 the long tasks after load came from filling the 87 examples of the Playground loop (one pg.fill of TransactionSerialization = 1 beforeinput plus 99 input events, EventDispatch 450 ms, Layout 134 ms), the undoing of the plain-code data removed them (variants v1b, v5, v6 passed, v1 to v4 failed), and the final template cut one fill from about 440 ms to about 60 ms. HYPOTHESES to test, not to assume: (H1) the post-load work is still proportional to the CPU available, so a contended machine turns a 60 ms step into a very long one (a margin problem: the page does the work in one task instead of in slices); (H2) the 2063 ms task is a separate once-only step after 5000 ms (for example the first run of the embedded Python runtime, a layout of the ontology graph, the syntax highlighting of all listings, or garbage collection) that the first repair did not touch. ")
SPEC = {"ST_Repair_Ch03_Page2": ("REPAIR 2: the chapter 3 page without the 2-second task after load, as a new page version", "Del3_ChapterCode", "Obj3_ChapterCode", "SEN0401-I63-ch03page2", 3.0, 1.0, "ch03page2", [])}
TK = {"ST_Repair_Ch03_Page2": "Repair_Ch03_Page2"}
BRIEFS = {"ch03page2": (WORDS + "ITEM (stated first, the owner's rule and the coordinator's): chapter 3 STAYS on the shipped page v9_73_0 until a repair passes the lineage agent's own runs; v9_73_0, v9_74_0 and v9_75_0 are never edited. WHAT TO DO: (1) FIND THE CAUSE FIRST, from a trace, not from a guess: on a copy of v9_75_0 (a diagnostic copy of test 9.38.0 that stamps every long task after load with the step that runs it is allowed; it is not a gate and is never used as one) run the session at least 5 times and print for every run the longest task after load and which step it belongs to (the long-task attribution entries, a performance trace, or markers around the page steps); then run it again with the machine under moderate CPU load (for example two busy loops of python3 started in the background and removed after) because the failing run was made at load 3 to 6; report each run as printed, also the ones that pass. Decide between H1 and H2 on those numbers. (2) Build a NEW versioned page (v9_76_0 or higher; same template and builder unless the cause is there) that keeps everything v9_75_0 gives and removes the cause: whatever step produces the longest task after load is done in slices (idle callbacks or time-boxed chunks of at most 40 ms, with the same visible result), not made faster by dropping content. (3) NEVER retune or relax a gate, a bound or a test; a failing result is reported as printed. (4) Proof: 9.38.0 on the new page FIVE times back to back plus once on v9_73_0, all under ONE hold of `flock /tmp/page_test.lock`, at the lowest load you can get; ALL five must pass; then 9.34.3 on the new page and on v9_73_0 in one hold; then 9.37.0 and 9.34.2 are NOT to be run (they crash on this Playground, use 9.34.3 and 9.38.0 only), the panel test (sen0401_page_panels_test_v1_0_0.py) and the Page/Ch03 chapter check v1_7_0 on the new page, each under the lock. (5) The deck-page code match, the old pages byte-identical and the Deck and Research chapter checks as before. (6) Commit your own files by path under `flock /tmp/sen0401_git.lock`; report the commit ids and every result verbatim, including a failure; delete scratch variants and temporary folders you created (disk stop at 0.9 GB free)."),}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {"ST_Repair_Ch03_Page2": ("AC9_Repair_Ch03_Page2", "A new chapter 3 page passes the main-thread budget feature on a quiet machine, as the shipped page does, with the same content as v9_75_0", "Owner-directed work (" + CR + ", " + WHEN + "). Given the pages v9_75_0 and v9_74_0 (unchanged) and the shipped v9_73_0, when the new page is made, then ALL of: (1) every file is new and v9_74_0 and v9_73_0 are byte-identical; (2) the cause is found from a trace and reported with the numbers of every run, also under CPU load; (3) 9.38.0 passes on the new page FIVE times in a row under one lock hold, and 9.34.3 passes, with no gate retuned; (4) the panel test and the Page/Ch03 chapter check pass; (5) the slide code equals the Chapter Examples tab in slide order, 0 lambdas except the taught slide, the Lecture tab equals the deck.")}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). A repair re-ranks the open items (G147). Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The chapter 3 page v9_74_0 is repaired as a new page"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the chapter 3 page repair costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: one new story with two tasks (about 4 agent-hours); the Ch03 PageCode Verify task depends on the repair; the open items are re-ranked (G147)."))
    return t + cr + ia, "Change request with impact assessment: the defect of the chapter 3 page v9_74_0; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the chapter 3 page repair"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the chapter 3 page repair; nothing is rebuilt here." % OLD.replace("ex:", "")
def setdeps(t, tid, deps):
    i, j = T.blk(t, tid); b = t[i:j]
    m = re.search(r"backlog:dependsOn ([^;]*?) ;", b)
    if m: b = b.replace(m.group(0), "backlog:dependsOn " + m.group(1).rstrip() + ", " + ", ".join("ex:" + d for d in deps) + " ;", 1)
    else:
        m = re.search(r"backlog:hasState backlog:\w+ ;", b); b = b[:m.end()] + "\n    backlog:dependsOn " + ", ".join("ex:" + d for d in deps) + " ;" + b[m.end():]
    return t[:i] + b + t[j:]
def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; mem = []
    for sid, (title_, deliv, obj, sess, hb, hv, brief, deps) in SPEC.items():
        aid, label, g_ = CRIT[sid]; k = aid[4:]
        L.append(RT.ac_block(aid, label, g_, 'ex:TS_ChapterCheck, ex:TS_DeckMatch', "the checks of the task, run again by the lineage agent; papers control; LibreOffice render; reader on the sheet PDF", k).replace("ex:TC9_", "ex:TC9Z_"))
        L.append(RT.case_blocks(k, aid).replace("Spec3I_Retro24", "Spec3I_Ch06Teach").replace("ex:Data3S_TC9_", "ex:Data3S_TC9Z_").replace("ex:TC9_", "ex:TC9Z_")
            .replace("Run the checks on the item as measured in the baseline of 2026-10-25 (an overlap, a manifest example that starts with an error name, a story whose text lies below the first screen, a committed file with status M) and require that nothing is claimed for it.", "Run the checks on the item as it stands before the work and require that nothing is claimed for it.")
            .replace("The finding as measured in the baseline of 2026-10-25 (ex:IA3_Retro24).", "The finding as measured on 2026-11-01 (" + IA + ")."))
        tb, tv = "TK_%s_Build" % TK[sid], "TK_%s_Verify" % TK[sid]; mem += [sid, tb, tv]
        L.append(R.story_block(sid, title_, deliv, obj, [aid], [tb, tv], NOTE, "ex:" + ITER, "Proposed"))
        note_b = bodyof(brief) + " REUSE: use the existing tools and files named in the task and never edit a committed file. ONE EXECUTOR SESSION: " + sess + "."
        L.append(R.task_block(tb, "Build: " + title_, "Build", deps, sess, "S", hb, note_b, "ex:" + ITER, "Proposed", True))
        L.append(R.task_block(tv, "Verify: " + title_, "Verify", [tb], "builder", "S+%.1fh" % hb, hv, "Run the checks of the criterion again myself, with my own control scripts and the existing tools, on the new files; open every produced file; read the report of the executor against the files; register Done only on files I have re-run.", "ex:" + ITER, "Proposed", True))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
        L.append("ex:Obj3_%s backlog:metricMovableBy ex:%s .\n" % ("Exam" if obj.endswith("Exam") else "ChapterCode", sid))
    t = setdeps(t, "TK_Ch03_PageCode_Verify", ["TK_Repair_Ch03_Page2_Build"])
    i, j = T.blk(t, ITER); b = t[i:j]; m = re.search(r"backlog:hasMember ([^;.]*?)( ;| \.|\.\n)", b, re.S); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:hasMember " + m.group(1).rstrip() + ", " + ", ".join("ex:" + x for x in mem) + m.group(2), 1) + t[j:]
    L.append('ex:SC3_Ch03PageRepair2 a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the chapter 3 page repair story"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Ch03PageRepair2; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR50 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the chapter 3 page repair"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: one story with two tasks (chapter 3 page repair) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
