#!/usr/bin/env python3
"""sen0401_lineage_res54 v1_0_0 - (the exam v7 redesign, five stories, copy of res51) (the exam v6 corrections: the floor at 0, copy of res50) change route (G125 route 2) for the owner ruling of Monday 2026-11-02 16:52 Istanbul (relayed by the coordinator): the total of the whole paper is floored at 0 for both exams, no floor inside a question. Adds one story with one Build task and one Verify task: the scoring rule file and module as new versions with the floor, the instructor key text updated, the blind-mean figures recomputed. Usage: change | retract | backlog PREV | fill PREV."""
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
REV = "ex:Revision_Lineage3_Backlog30"; OLD = "ex:Out3_BacklogR57"; NEWB = "ex:Out3_BacklogR58"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamV7Split"; IA = "ex:IA3_ExamV7Split"
WHEN = "Monday 2026-11-02, on the owner's urgency order of 19:07 Istanbul, relayed by the coordinator"
WORDS = ("OWNER REDESIGN (2026-11-02, 18:20 Istanbul, relayed by the coordinator), urgent, supersedes the floor and penalty work. The owner: the deduction calculations are too complicated and impossible by hand; each question's deduction is different, which confuses and stresses students; simplify, students may get advantages; the answer sheet with tips is 3 pages and the exam 6, total 9, but the standard is 4 pages and the maximum 6; shorten the tips and put them on the question; 'remove the deductions and remove the bonus question, but increase the options from 4 to 5, so students get 20 points if they answer totally blindly'; and: how are hand-written answers graded? RULINGS for SEN0401 as a new version v7 (new versioned files only, no gate weakened, no committed file edited): (1) no deductions of any kind: a right answer scores its points, a wrong or blank answer 0, no floor needed, one rule for every question; (2) the bonus question is removed, the total is 100 points; (3) every closed-answer unit has 5 alternatives so a blind guess is worth 1/5: choice 5 options, matching 5 responses per premise, ordering a place from 1 to 5 over 5 steps, fill-in banks of 5 entries; number and code-trace answers stay hand-written (blind chance about 0, so the blind total is slightly under 20: report the exact figure); the fifth option, entry or step is added per item as a new item version, answers unchanged unless a fifth alternative forces otherwise, every key recomputed by running the code; (4) tips: no tips pages; a short tip (target 12 words or fewer) printed on the question itself under the stem; the readability rules (stem 60 words, direction 25 words) stay and its tip rule is updated as a new version; (5) pages: paper plus sheet at most 6, aim 4 or 5 (cover 1, questions 2 to 3, sheet 1); the sheet is one page with choice-type answers only, the reader reads page 1; (6) grading: a plain one-page grading procedure in the instructor key: closed answers by the sheet or the question pages, numbers and traces hand-written on the question page compared with the key value (the exact value gives full points, else 0, no partial credit), the question pages are the legal copy, no arithmetic beyond adding points; (7) cover and directions: every penalty sentence and the two-answers deduction wording removed; the legal-copy sentence and the rule 'two answers in one place count as no answer' stay. The deliverable set carries ONE version: sen0401_exam_midterm_v7_0_0_paper.docx and .pdf, _key.docx and .pdf, _sheet.pdf, and SHA256.txt.")
COMMON = " COMMON RULES: write every file that holds a question, an answer, a key or a sheet into /home/claude/CME/exams/SEN0401/08-tooling/exam/ (same relative layout) and commit it in CME yourself (git -C /home/claude/CME pull --rebase --autostash first, add by path, commit, push); commit to SEN0401 only scripts and data files that hold no question and no answer (the lineage agent's leak search is run on your commit); all new files are new versions, never edit a committed file, never weaken a gate; report every result as the tool prints it (NOT_MEASURED and NOT_RUN are not passes); Word pagination is NOT_MEASURED (LibreOffice export only). THIS IS URGENT: the owner prints today."
SPEC = {
"ST_Exam_V7_PapersTool": ("The paper tooling v7 on a synthetic items file: key renderer, one-page grading procedure, paper layout, SHA256 tooling", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I83-examv7papertool", 2.0, 1.0, "v7papertool", []),
}
TK = {k: k[3:] for k in SPEC}
BRIEFS = {
"v7papertool": WORDS + " ITEM (stated first): the paper TOOLING v7, split from the papers task by the owner's urgency order of 2026-11-02 19:07 Istanbul so the exam is finished earlier. It does NOT wait for the items executor. Build, against a SYNTHETIC v7 items file and structure that you write yourself (same field names as the items v1.5.0 file, five alternatives per closed unit, 'tip' string and 'needs_tip', whole-number row points, no bonus, 100 points; use invented placeholder wording such as 'Synthetic question 1', never a real question; disclose in every output and log that the input is synthetic), NEW files only (never edit a committed file): (1) the papers builder v2_0_0 pieces that render paper (cover without any penalty sentence but with the legal-copy sentence and the sentence 'two answers in one place count as no answer', questions with one 'Tip:' line of at most 12 words under the stem, no tips page, answer-format lines) and key (the key with the answers and a ONE-PAGE 'How to grade' section: numbers and traces exact value is full points else 0, no partial credit, question pages are the legal copy, nothing to compute beyond adding points) as .docx and .pdf (LibreOffice); the existing sen0401_exam_papers_build_v2_0_0.py and paper_lib_v2_0_0.py may be read and copied into new v3_0_0 files; (2) a SHA256 writer for the set sen0401_exam_midterm_v7_0_0_{paper,key}.{docx,pdf}, _sheet.pdf and SHA256.txt; (3) a one-command render script that takes the real items v1.6.0 and structure v1.3.0 from CME private/ when they exist and renders the real files with the sheet module v7_0_0 (units_from_list) and a real form code; (4) run readability check v1.1.0 and the scoring module v2.0.0 on the synthetic render and print page counts (paper plus sheet at most 6; aim 4 to 5). Write synthetic outputs into /home/claude/CME/exams/SEN0401/08-tooling/exam/papers_v7_synthetic/ (clearly named synthetic, never delivered). The scripts hold no question and no answer. Do not run Libreoffice more than one at a time (page-test lock: flock /tmp/page_test.lock). Machine has 2 CPUs: run heavy checks at nice 10. ",
}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {
"ST_Exam_V7_PapersTool": ("AC9_Exam_V7_PapersTool", "The paper tooling v7 renders paper, key with a one-page grading procedure, and the SHA256 file from a synthetic items file, and renders the real set in one command once the real items exist", "Owner urgency order (" + CR + ", " + WHEN + "). Given the split of the papers task, when the tooling is run on a synthetic items file, then the paper, the key and the SHA256 list are produced, the readability check v1.1.0 and the scoring module v2.0.0 run on them, the page count of paper plus sheet is printed, and no file holds a real question or answer."),
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
    t = setdeps(t, "TK_Exam_V7_Papers_Build", ["TK_Exam_V7_PapersTool_Build"])
    i, j = T.blk(t, ITER); b = t[i:j]; m = re.search(r"backlog:hasMember ([^;.]*?)( ;| \.|\.\n)", b, re.S); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:hasMember " + m.group(1).rstrip() + ", " + ", ".join("ex:" + x for x in mem) + m.group(2), 1) + t[j:]
    L.append('ex:SC3_ExamV7Split a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the exam v7 stories"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamV7Split; it was Pending before."@en .\n' % (CR, now[:10]))
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
