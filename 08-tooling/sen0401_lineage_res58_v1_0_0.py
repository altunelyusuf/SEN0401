#!/usr/bin/env python3
"""sen0401_lineage_res58 v1_0_0 - (the exam v7 redesign, five stories, copy of res51) (the exam v6 corrections: the floor at 0, copy of res50) change route (G125 route 2) for the owner ruling of Monday 2026-11-02 16:52 Istanbul (relayed by the coordinator): the total of the whole paper is floored at 0 for both exams, no floor inside a question. Adds one story with one Build task and one Verify task: the scoring rule file and module as new versions with the floor, the instructor key text updated, the blind-mean figures recomputed. Usage: change | retract | backlog PREV | fill PREV."""
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
REV = "ex:Revision_Lineage3_Backlog34"; OLD = "ex:Out3_BacklogR61"; NEWB = "ex:Out3_BacklogR62"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamV72P"; IA = "ex:IA3_ExamV72P"
WHEN = "Monday 2026-11-02, on the owner's decision of the evening of 2026-11-02 (accept 7 pages), relayed by the coordinator"
WORDS = "OWNER DECISION (2026-11-02, evening, relayed by the coordinator, answer to the coordinator's one question): 'Accept 7 pages.' The Papers executor of the v7.2 set (session SEN0401-I93-examv72papers, started 2026-11-02T19:19:32Z) STOPPED and delivered nothing: the merged items v1.8.0 need 7.43 columns at the smallest allowed layout setting, paper plus sheet is 7 pages (cover, five question pages, sheet) against the limit of 6, refused even at a 0.5 percent planning margin. The owner's decision: for the set v7_2_0 ONLY the page limit is 7 pages (paper 6 plus sheet 1), nothing is shortened; this is an owner decision against the 6-page rule, recorded, not a waiver for other sets. Everything else of the owner's orders (21:03 the sheet holds the Question 2 answers, 21:06 no code questions, 21:24 plain language with intention and worked solutions in the key) stays. Public commit ec28d45a already holds the new tooling files sen0401_exam_paper_lib_v7_2_0.py, sen0401_exam_papers_build_v7_2_0.py and sen0401_exam_render_v7_2_0.py (no exam text)."
COMMON = " COMMON RULES: write every file that holds a question, an answer, a key or a sheet into /home/claude/CME/exams/SEN0401/08-tooling/exam/ (same relative layout) and commit it in CME yourself (git -C /home/claude/CME pull --rebase --autostash first, add by path, commit, push); commit to SEN0401 only scripts and data files that hold no question and no answer (the lineage agent's leak search is run on your commit); all new files are new versions, never edit a committed file, never weaken a gate; report every result as the tool prints it (NOT_MEASURED and NOT_RUN are not passes); Word pagination is NOT_MEASURED (LibreOffice export only). THIS IS URGENT: the owner prints today."
SPEC = {
"ST_Exam_V72_Papers2": ("The midterm set v7.2 rendered with the 7-page limit and structure v1.5.1: paper, key with worked solutions, sheet, SHA256.txt", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I94-examv72papers2", 2.0, 0.5, "v72papers2", []),
}
TK = {k: k[3:] for k in SPEC}
BRIEFS = {'v72papers2': "OWNER DECISION (2026-11-02, evening, relayed by the coordinator, answer to the coordinator's one question): 'Accept 7 pages.' The Papers executor of the v7.2 set (session SEN0401-I93-examv72papers, started 2026-11-02T19:19:32Z) STOPPED and delivered nothing: the merged items v1.8.0 need 7.43 columns at the smallest allowed layout setting, paper plus sheet is 7 pages (cover, five question pages, sheet) against the limit of 6, refused even at a 0.5 percent planning margin. The owner's decision: for the set v7_2_0 ONLY the page limit is 7 pages (paper 6 plus sheet 1), nothing is shortened; this is an owner decision against the 6-page rule, recorded, not a waiver for other sets. Everything else of the owner's orders (21:03 the sheet holds the Question 2 answers, 21:06 no code questions, 21:24 plain language with intention and worked solutions in the key) stays. Public commit ec28d45a already holds the new tooling files sen0401_exam_paper_lib_v7_2_0.py, sen0401_exam_papers_build_v7_2_0.py and sen0401_exam_render_v7_2_0.py (no exam text). ITEM (stated first): the PAPERS v7.2, second run. Steps in this order. (1) NEW structure v1.5.1 in CME private/ (structure v1.5.0 stays untouched): copy v1.5.0 and correct the Question 2 heading, which still says 'Work out each number, by calculation or by following the program', to: Work out each number by calculation. No Question 2 item has a program. Search every item, structure and key file you will use for the same sentence and report where else it appears (committed files are not edited: new versions only). (2) NEW builder copy with the page limit raised to 7 pages (paper 6 plus sheet 1 = 7 total; new file, e.g. sen0401_exam_papers_build_v7_2_1.py; never edit a committed file; the limit applies to this set only and is stated in the log as the owner's decision), then the real render with V7_PLAN_FREE=0.005 V7_MIN_FREE=0.005 using the render script (copy it as a new file if it must name the new builder), items v1.8.0 and structure v1.5.1 from CME private/, the sheet from sen0401_exam_answersheet_v7_build_v1_1_0.py (sheet v7.1: bubbles plus digit boxes for the Question 2 places; the paper prints five boxes per Question 2 place and the sheet the same five, so the box count does not reveal the answer length), a real form code, into /home/claude/CME/exams/SEN0401/08-tooling/exam/papers_midterm_v7_2/ named sen0401_exam_midterm_v7_2_0_{paper.docx,paper.pdf,key.docx,key.pdf,sheet.pdf} and SHA256.txt. No question shortened, no option cut, no stem or tip changed. (3) The paper prints q only (never the old instruction field) with one Tip line under each stem; the key keeps the one-page 'How to grade' whole on key page 1 (steps 1, 2, 4 and 8: the hand-written value is read from the question page, the sheet box is for fast reading, the exact value scores the full points else 0, no partial credit; the numbers are copied to the sheet; two answers in one place count as no answer) and then for EVERY item the answer and its worked solution from sen0401_exam_key_solutions_v1_8_0.json (steps with intermediate numbers; why right and why each other option or row is wrong), and the PROVISIONAL flags Q4.a/b, Q4.c/d and Q1.g (point L is the author's reading); the key is not counted in the pages. Cover direction: Write each number in the boxes on the question page and copy it into the boxes of the answer sheet; the question pages count if they differ (sentences at most 25 words; the legal-copy sentence and 'Two answers in one place count as no answer' stay; no deduction sentence). (4) Checks, reported as printed: readability v1.1.0 R1 to R6, the clarity check in paper mode on the new paper (C1, C2, C5 measured on the paper; C3 and C4 on the items), the tooling check (the spurious R01 'code text must be 8 point or larger' that the draft logged although the paper has no code is disclosed, not hidden), the scoring check (exact blind 77033/5000), the reader on 40 synthetic sheets at two seed bases, pdfinfo page counts (paper at most 6 pages, sheet 1 page, total at most 7), my own-style recomputation of the eight hand calculations by running code, the leak search (sen0401_exam_move_control_check_v1_2_6.py leakscan), sha256sum -c. List the delivered hashes and every NOT_MEASURED (Word pagination). Machine has 2 CPUs: nice 10 for heavy runs. Commit CME and the public scripts (no question, no answer) with trailers and verify with git fetch that the pushes landed."}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {
"ST_Exam_V72_Papers2": ("AC9_Exam_V72_Papers2", "The paper, key and sheet v7.2 are delivered as one version with worked solutions in the key, at most 7 pages with the sheet by owner decision, and structure v1.5.1", "Owner decision (" + CR + ", " + WHEN + "). Given the merged items, when the set is rendered, then the paper shows each intention, the key shows the worked solution of every item with the one-page grading procedure and the provisional flags, paper (at most 6 pages) plus sheet (1 page) is at most 7 pages, the Question 2 heading is corrected in structure v1.5.1, and the set has one version name with SHA256.txt."),
}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The exam v7: no deductions, no bonus, five alternatives, short tips, one-page sheet"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the exam v7 redesign costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: one new story with two tasks (about 4 agent-hours); no existing task depends on it, but every later exam artefact is written to the CME location; the open items are re-ranked (G147)."))
    return t + cr + ia, "Change request with impact assessment: the corrected exam: items, sheet, reader, readability tool and papers; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the the exam v7 redesign"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the exam v7 redesign; nothing is rebuilt here." % OLD.replace("ex:", "")
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
    L.append('ex:SC3_ExamV72P a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the exam v7 stories"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamV72P; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the exam v7 redesign"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEWB, X.digest(t, "Backlog")), \
        "third lineage, Backlog stage rebuilt: one story with two tasks (the exam v7 redesign) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
