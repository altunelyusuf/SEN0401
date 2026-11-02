#!/usr/bin/env python3
"""sen0401_lineage_res55 v1_0_0 - (the exam v7 redesign, five stories, copy of res51) (the exam v6 corrections: the floor at 0, copy of res50) change route (G125 route 2) for the owner ruling of Monday 2026-11-02 16:52 Istanbul (relayed by the coordinator): the total of the whole paper is floored at 0 for both exams, no floor inside a question. Adds one story with one Build task and one Verify task: the scoring rule file and module as new versions with the floor, the instructor key text updated, the blind-mean figures recomputed. Usage: change | retract | backlog PREV | fill PREV."""
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
REV = "ex:Revision_Lineage3_Backlog31"; OLD = "ex:Out3_BacklogR58"; NEWB = "ex:Out3_BacklogR59"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamV71"; IA = "ex:IA3_ExamV71"
WHEN = "Monday 2026-11-02, on the owner's order of 21:03 Istanbul, relayed by the coordinator"
WORDS = ("OWNER ORDER (2026-11-02, 21:03 Istanbul, relayed by the coordinator), under the running urgency: 'Design the answer sheet to hold the answers for the question 2. You already provide boxes to fill in.' The owner then answered that the hand-written answers of Question 2 are written ON BOTH the question page and the sheet: the student writes on the question page and copies each into the boxes of the sheet; if they differ the question page counts; the legal-copy rule stays. This makes a new version of the whole set: sen0401_exam_midterm_v7_1_0 (paper, key, sheet, SHA256.txt) as ONE version. Rules: (1) the sheet v7.1 is still ONE A4 page, the same bubbles for the closed answers, plus digit boxes for every hand-written place of Question 2 (2a to 2h as in the structure: numbers and code results), the number of boxes of a place equal to the number of boxes printed on the question page for that place; reuse the number-box design of the v6 sheet module (sen0401_exam_answersheet_v6_1_0.py); the reader v1.4.0 keeps reading bubbles only and treats the boxes as hand-read, and the sheet and the key say so plainly; (2) the printed sentence 5 of the sheet becomes: Write numbers and code results on the question pages and copy each into its boxes here. (at most 25 words); the legal-copy sentences stay and 'Two filled bubbles in one place count as no answer' stays; (3) the paper cover line that says the sheet holds the choice answers only changes to match (the numbers are copied to the sheet, the question pages count); (4) the key 'How to grade': the hand-written step reads the value from the question page, the sheet box is for fast reading; the exact value scores the full points, anything else 0, no partial credit; still one page; (5) pages: paper 5 plus sheet 1 = 6 at most (aim 6 or fewer, measured); the items, the structure and the scoring module are NOT changed (v1.6.1, v1.3.1, v2.0.0). No deduction, no bonus, no floor.")
COMMON = " COMMON RULES: write every file that holds a question, an answer, a key or a sheet into /home/claude/CME/exams/SEN0401/08-tooling/exam/ (same relative layout) and commit it in CME yourself (git -C /home/claude/CME pull --rebase --autostash first, add by path, commit, push); commit to SEN0401 only scripts and data files that hold no question and no answer (the lineage agent's leak search is run on your commit); all new files are new versions, never edit a committed file, never weaken a gate; report every result as the tool prints it (NOT_MEASURED and NOT_RUN are not passes); Word pagination is NOT_MEASURED (LibreOffice export only). THIS IS URGENT: the owner prints today."
SPEC = {
"ST_Exam_V71_Sheet": ("The answer sheet v7.1: one page, bubbles for the closed answers and digit boxes for the hand-written answers of Question 2", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I85-examv71sheet", 1.5, 0.5, "v71sheet", []),
"ST_Exam_V71_Papers": ("The midterm set v7.1: paper, key and sheet as one version with the copy rule and SHA256.txt", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I86-examv71papers", 1.5, 0.5, "v71papers", ["TK_Exam_V71_Sheet_Build"]),
}
TK = {k: k[3:] for k in SPEC}
BRIEFS = {
"v71sheet": WORDS + " ITEM (stated first): the SHEET v7.1. Make NEW files only (never edit a committed file): sen0401_exam_answersheet_v7_1_0.py (a copy of v7_0_0 that adds the number boxes of Question 2 reusing the box design of sen0401_exam_answersheet_v6_1_0.py and units_from_list() for the papers builder), its build script, a check v7_1_0 and, only if the reader v1_4_0 cannot ignore the boxes, a reader copy v1_5_0 (otherwise state that v1_4_0 is used unchanged). The page: A4, four corner marks, the same 26 bubble rows, plus a block of boxes for 2a to 2h (label, then the boxes; the box count of each place equals the count printed on the question page for that place; read the count from the paper/layout, not from the key digits), all on ONE page; the printed sentences: line 5 is exactly the owner's sentence 'Write numbers and code results on the question pages and copy each into its boxes here.' (at most 25 words), the legal-copy sentences and 'Two filled bubbles in one place count as no answer.' stay; no word about points taken away, bonus or tips; type at least 10 pt. The check must prove: one page; every Question 2 place has its boxes; box counts equal the paper's; the page fits (overflow refused, never clipped); the reader v1_4_0 (or v1_5_0) on 40 synthetic sheets at each of two seed bases, now WITH digits drawn in the boxes at random, gives 0 registration failures, 0 silent wrong, 0 missed, 0 empty-not-flagged, held share at most 25 percent; the boxes are NOT read by the reader (hand-read, stated plainly in the check log and on the sheet by the sentence above); the older checks of v7_0_0 still pass on the bubble part. Machine has 2 CPUs: run heavy checks at nice 10. Report page measurements and the proof sheet in CME exams/SEN0401/08-tooling/exam/sheet_v71/.",
"v71papers": WORDS + " ITEM (stated first): the papers v7.1. Do NOT start until TK_Exam_V71_Sheet_Build is Done (the coordinator tells you). Then render the set with the existing one-command tooling (render_v7_0_1 and papers_build_v7_0_1, paper_lib_v7_0_1 in 08-tooling/exam; make new v7_1_0 copies, never edit a committed file) from the real items v1.6.1 and structure v1.3.1 in CME private/, with the sheet module v7_1_0 and a real form code: output into /home/claude/CME/exams/SEN0401/08-tooling/exam/papers_midterm_v7_1/ named sen0401_exam_midterm_v7_1_0_{paper.docx,paper.pdf,key.docx,key.pdf,sheet.pdf} and SHA256.txt. Changes against v7_0_0: the cover direction that says the sheet holds the choice answers only becomes: Write each number or code result in the boxes on the question page and copy it into the boxes of the answer sheet; the question pages count if they differ (at most 25 words per sentence, the legal-copy sentence and 'Two answers in one place count as no answer' stay); the key 'How to grade' steps 1, 2, 4 and 8 read: the hand-written value is read from the question page, the sheet box is for fast reading, the exact value scores the full points else 0, no partial credit, still ONE page and whole on key page 1; the sheet is the v7.1 sheet. Items, structure, scoring module, readability rules unchanged: run the readability check v1.1.0 (report R1 to R6 as printed; R6 is known to fail for the SegWit tip of 4e/4f in v7.0.0 and the owner decided to print it; report it again, do not reword items), the tooling check, the scoring check, the reader on 40 synthetic sheets, pages by pdfinfo: paper plus sheet at most 6 (paper 5 + sheet 1 expected; if more, STOP and report the exact count and the longest items); the planning margin may stay at the 0.5 percent used for v7.0.0, stated plainly, Word pagination NOT_MEASURED. Recompute the code traces by running code; list the delivered hashes.",
}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {
"ST_Exam_V71_Sheet": ("AC9_Exam_V71_Sheet", "The sheet v7.1 is one page with the bubbles and the digit boxes of Question 2, and the reader still reads only the bubbles", "Owner order (" + CR + ", " + WHEN + "). Given the order that the sheet holds the Question 2 answers, when the sheet is made, then it is one page, every hand-written place of Question 2 has boxes equal in number to the question page, the printed copy sentence is the owner's, the reader reads the bubbles with 0 registration failures, 0 silent wrong, 0 missed on 40 synthetic sheets at each of two seed bases with digits drawn in the boxes, and the boxes are stated as hand-read."),
"ST_Exam_V71_Papers": ("AC9_Exam_V71_Papers", "The paper, key and sheet v7.1 are delivered as one version with the copy rule, at most 6 pages with the sheet", "Owner order (" + CR + ", " + WHEN + "). Given the order, when the set is rendered, then the paper, key and sheet carry one version name with SHA256.txt, the cover and the key state that the question page counts and the sheet box is for fast reading, paper plus sheet is at most 6 pages, the key's grading procedure is whole on page 1, and no deduction sentence is printed."),
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
    L.append('ex:SC3_ExamV71 a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the exam v7 stories"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamV71; it was Pending before."@en .\n' % (CR, now[:10]))
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
