#!/usr/bin/env python3
"""sen0401_lineage_res41 v1_0_0 - (copy of res40 for the page-test gates 9.37.0 and 9.34.2 that cannot run on the new Playground: a gate that cannot run is not a pass) change route (G125 route 2, G133, G147) for the owner's words of 2026-11-01 13:04 Istanbul on the exam: the IKU cover page as page 1, five question formats (4 x 25 points, the 5th 10 points bonus), no memorising items, tips for terms, abbreviations spelled out, 4 pages (else 6). Adds the stories of the cover renderer, items v1.2.0, papers/key/sheet v3, the honesty-check successor and the Ch05 Teach repair task. Usage: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog20"; OLD = "ex:Out3_BacklogR47"; NEWB = "ex:Out3_BacklogR48"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_PlaygroundTests"; IA = "ex:IA3_PlaygroundTests"
WHEN = "Sunday 2026-11-01, on the coordinator's ruling that a gate that cannot run is not a pass, after the lineage agent's quiet-window runs"
BODY = ("FINDING (lineage agent, quiet window, 2026-11-01/02): the committed page tests 9.37.0 and 9.34.2 crash (StopIteration in the Playground step, after 27 features passed and 0 failed) on every page whose Playground lists the chapter's slide examples (the option values 'cc:N'), for example Ch02 v9_73_0. A gate that cannot run is not a pass. The versioned copies already exist and differ from the old tests by ONE line each: 9.34.3 over 9.34.2 and 9.38.0 over 9.37.0 (the expected code of an option whose value starts with 'cc:' is read from the page's chapter-code examples). WHAT TO DO (new files only; no gate is weakened, loosened or retuned; the committed tests are never edited): (1) Show by diff, as printed, that 9.34.3 and 9.38.0 differ from 9.34.2 and 9.37.0 only in that line, and that every other check is identical. (2) Build FIXTURES OF KNOWN ANSWER for that Playground step: a page copy in which the code of one 'cc:' option is altered (the step must FAIL, naming the option), a page copy with a 'cc:' value out of range (must FAIL, not crash), and the true page (must PASS); run 9.34.3 and 9.38.0 on each and report each result as printed. If a fixture shows that the step cannot fail when it should, report it as a defect and make a new versioned test (9.34.4 and 9.38.1, new files) that fails correctly. (3) Run 9.34.3 on the Ch01 v9_74_0, Ch02 v9_73_0 and Ch04 v9_75_0 pages, one at a time, each under flock /tmp/page_test.lock (the lineage agent has run 9.38.0 on them, not 9.34.3). (4) Run nothing else on the lock; delete scratch copies and temporary folders you create (disk stop at 0.9 GB free). (5) Report every result verbatim, including a failure, and the commit ids.")
SPEC = {"ST_Test_Playground_Fixtures": ("The page tests that match the Playground of the new pages are proven with fixtures of known answer", "Del3_ChapterCode", "Obj3_ChapterCode", "SEN0401-I61-testfix", 2.0, 0.5, "testfix", [])}
TK = {"ST_Test_Playground_Fixtures": "Test_Playground_Fixtures"}
BRIEFS = {"testfix": [BODY]}
assert len(BODY) > 800
def bodyof(n): return BRIEFS[n][0]
CRIT = {"ST_Test_Playground_Fixtures": ("AC9_Test_Playground_Fixtures", "The page tests 9.34.3 and 9.38.0 are shown to differ from 9.34.2 and 9.37.0 only in the Playground line and to fail on fixtures of known wrong answer", "Owner-directed work (" + CR + ", " + WHEN + "). Given the committed tests 9.34.2, 9.34.3, 9.37.0 and 9.38.0 (unchanged), when the fixtures are made, then ALL of: (1) every file is new and no committed test is edited; (2) the diffs show one changed line each; (3) a page copy with a wrong example code makes the Playground step FAIL and the true page makes it PASS, for 9.34.3 and 9.38.0; (4) a 'cc:' value out of range fails and does not crash; (5) 9.34.3 is run on Ch01, Ch02 and Ch04 and the results are reported as printed.")}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). A gate that cannot run is not a pass. Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The page tests are proven on the Playground of the new pages"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the page-test fixtures cost and touch"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: one new story with two tasks (about 2.5 agent-hours); the Verify tasks of the Ch01 to Ch04 PageCode stories depend on it (a gate that cannot run is not a pass); the open items are re-ranked (G147)."))
    return t + cr + ia, "Change request with impact assessment: the page tests that cannot run on the new Playground; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the page-test fixtures"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the page-test fixtures; nothing is rebuilt here." % OLD.replace("ex:", "")
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
    for _c in ("Ch01", "Ch02", "Ch03", "Ch04"): t = setdeps(t, "TK_%s_PageCode_Verify" % _c, ["TK_Test_Playground_Fixtures_Build"])
    i, j = T.blk(t, ITER); b = t[i:j]; m = re.search(r"backlog:hasMember ([^;.]*?)( ;| \.|\.\n)", b, re.S); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:hasMember " + m.group(1).rstrip() + ", " + ", ".join("ex:" + x for x in mem) + m.group(2), 1) + t[j:]
    L.append('ex:SC3_PlaygroundTests a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the page-test fixtures story"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_PlaygroundTests; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR48 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the page-test fixtures"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: one story with two tasks (page-test fixtures) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
