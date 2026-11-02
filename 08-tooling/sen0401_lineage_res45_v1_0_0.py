#!/usr/bin/env python3
"""sen0401_lineage_res45 v1_0_0 - (the combined page-test run proof, copy of res44) (was: copy of res38 for the repair of the chapter 3 page v9_74_0: a defect found by the lineage agent in the quiet window of 2026-11-01) change route (G125 route 2, G133, G147) for the owner's words of 2026-11-01 13:04 Istanbul on the exam: the IKU cover page as page 1, five question formats (4 x 25 points, the 5th 10 points bonus), no memorising items, tips for terms, abbreviations spelled out, 4 pages (else 6). Adds the stories of the cover renderer, items v1.2.0, papers/key/sheet v3, the honesty-check successor and the Ch05 Teach repair task. Usage: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog23"; OLD = "ex:Out3_BacklogR50"; NEWB = "ex:Out3_BacklogR51"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_CombinedRunProof"; IA = "ex:IA3_CombinedRunProof"
WHEN = "Monday 2026-11-02, on the lineage agent's measurement of the page-test cost, approved by the coordinator"
WORDS = ("FINDING (lineage agent, 2026-11-02): the page-test stage costs about 13 minutes of the shared browser lock per run, and every page is run with several test versions (9.38.0, 9.34.3 and the older ones). By feature NAME, 9.38.0 contains every feature of 9.34.3 and 9.35.3 on chapter 2 (187, 187 and 199 names, 0 outside); 9.38.0 differs from 9.34.3 in 13 source lines and from 9.35.3 in 7 (diff counts of the committed files). A name match is NOT a proof that the check is the same, so no combined run may be relied on yet. The aim is one combined 9.38.0 run per page instead of two, saving about 13 minutes of lock time per page, WITHOUT weakening any gate. ")
SPEC = {"ST_Test_Combined_Run_Proof": ("The combined 9.38.0 page-test run is proven to cover the older tests, by a source-diff tool proven on fixtures", "Del3_ChapterCode", "Obj3_ChapterCode", "SEN0401-I64-combproof", 2.0, 0.5, "combproof", [])}
TK = {"ST_Test_Combined_Run_Proof": "Test_Combined_Run_Proof"}
BRIEFS = {"combproof": (WORDS + "ITEM (stated first, the owner's rule: a gate that cannot run is not a pass; a tool that refuses is not thereby correct): build a NEW tool and report; change nothing else. WHAT TO DO: (1) Write a new versioned tool (sen0401_test_superset_proof_v1_0_0.py in 08-tooling) that reads the committed page tests 9.34.3, 9.35.3 and 9.38.0 (never edits them) and, for every feature each of the two older tests records (the feat(...) calls with their label), finds the same label in 9.38.0 and compares the CHECK ITSELF: the Python syntax tree of the code that computes the verdict (the statements between the previous and this feat call that the verdict depends on, the helper functions it calls, the page data it reads, and any numeric bound or text it compares with), normalised for whitespace and comments only. It must print for every feature one of: IDENTICAL, CHANGED (with both texts), MISSING. Do not decide by label alone. (2) Prove the tool with FIXTURES OF KNOWN ANSWER before using it: at least five scratch copies of 9.38.0 in a scratch folder, each altered in one known way (a feature removed; a bound loosened from 200 to 400; a comparison inverted; a label renamed with the check unchanged; a comment-only change), and require that the tool reports exactly the known answer for each (MISSING, CHANGED, CHANGED, IDENTICAL under a new label reported as renamed, IDENTICAL). Print the table of expected against reported. If any fixture is answered wrongly the tool is wrong, not the fixture; fix the tool and report the failed first attempt. (3) Run it for 9.34.3 against 9.38.0 and for 9.35.3 against 9.38.0, and report the numbers: features total, IDENTICAL, CHANGED, MISSING, renamed. (4) Also state, from the sources, whether a feature of an older test depends on state left by an earlier feature in its own run (the order of features, a page opened once and reused, a clicked state), because a combined run runs the features in 9.38.0's order and such a dependency would change the result; list every such dependency found. (5) The RULE you may write is only this: a combined run replaces the older run when EVERY older feature is IDENTICAL (or a pure rename) and no order dependency is found; otherwise list exactly which features are not covered, and then the older run stays required for those; do not write the rule if the proof fails. (6) NEVER retune or relax a gate, a bound or a test, and never edit a committed test. The check on the pages themselves is NOT part of this task and needs no browser, no lock and no page; it must not take the page-test lock. (7) Commit your own files by path under `flock /tmp/sen0401_git.lock`; report the commit ids and every result verbatim, including a failure; delete scratch folders you created (disk stop at 0.9 GB free)."),}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {"ST_Test_Combined_Run_Proof": ("AC9_Test_Combined_Run_Proof", "A source-diff tool proves, on fixtures of known answer, which features of the older page tests 9.34.3 and 9.35.3 the test 9.38.0 covers with an identical check", "Owner-directed work (" + CR + ", " + WHEN + "). Given the committed tests 9.34.3, 9.35.3 and 9.38.0 (unchanged), when the tool is made, then ALL of: (1) the tool is a new file and no committed test is edited; (2) at least five fixtures altered in one known way are answered exactly as expected, and a wrong first answer is reported; (3) the tool reports for every feature of 9.34.3 and 9.35.3 IDENTICAL, CHANGED, MISSING or renamed, with totals; (4) every order or state dependency between features is listed; (5) the combined-run rule is written only if every older feature is covered and no dependency is found, otherwise the uncovered features are listed and the older run stays required; (6) no gate, bound or test is retuned and the page-test lock is not taken.")}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The combined page-test run is proven by a source-diff tool"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the combined-run proof costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: one new story with two tasks (about 4 agent-hours); no existing task depends on it; the open items are re-ranked (G147)."))
    return t + cr + ia, "Change request with impact assessment: the cost of the page-test stage; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the combined-run proof"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the combined-run proof; nothing is rebuilt here." % OLD.replace("ex:", "")
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
    i, j = T.blk(t, ITER); b = t[i:j]; m = re.search(r"backlog:hasMember ([^;.]*?)( ;| \.|\.\n)", b, re.S); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:hasMember " + m.group(1).rstrip() + ", " + ", ".join("ex:" + x for x in mem) + m.group(2), 1) + t[j:]
    L.append('ex:SC3_CombinedRunProof a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the combined-run proof story"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_CombinedRunProof; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR50 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the combined-run proof"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: one story with two tasks (combined-run proof) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
