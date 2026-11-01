#!/usr/bin/env python3
"""sen0401_lineage_res31 v1_0_0 - change route (G113, G125 route 2, G133, G147) for the owner's words of 2026-11-01 11:52 Istanbul on the midterm paper: 4 pages in total printed on 2 sheets, mixed order of questions, paper, key and ANSWER SHEET as MS Word (.docx), item styles to follow from his class sessions. A StageRevision from the Backlog stage; the not-started story ST_Repair_Exam_Paper and its two tasks and criterion are REWRITTEN (nothing is started), no committed file is edited. Events: change | retract | backlog PREV | fill PREV"""
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

REV = "ex:Revision_Lineage3_Backlog11"; OLD = "ex:Out3_BacklogR38"; NEWB = "ex:Out3_BacklogR39"; R.NEWB = NEWB
CR = "ex:CR3_PaperWordFourPages"; IA = "ex:IA3_PaperWordFourPages"; SID = "ST_Repair_Exam_Paper"
WHEN = "Sunday 2026-11-01, on the owner's words of 11:52 Istanbul time relayed by the coordinator"
WORDS = ("THE OWNER'S WORDS (relayed, 2026-11-01 and the day before): 'I need the PPT slides and interactive HTML files for both courses. Midterm scope: SEN0401: Chapters 1-6 ... the MS Word midterm exams, answer sheets. I will give you some details about the exam questions, as I made some interactive sessions during the class and ask them questions to understand if the students are reached to a certain level. The examinations should be developed to fit into 4 pages in total, to print in 2 pages, easy to read and assess, but using various techniques, including calculations, ordering, etc, that can be helpful to replace hand writing answers.' Earlier: '4 Pages to fit into 2 pages double side print. Mixed order mixed questions.' and 'Not PDF, MS Explorer for edit option'.")
MEAS = ("MEASURED 2026-11-01 by the lineage agent on the committed items (23 items, 24 units) and renderer v1.2.0: the paper alone fills 4.2 to 4.4 content pages at the committed settings; with every layout lever together (margin 10 mm, leading 1.12, code 8 pt, item gap 1.0 mm, column gap 6 mm; text stays at 10 pt) it still fills 3.31 (chapter order) and 3.47 (grouped by type) content pages, i.e. 4 pages. So 3 content pages plus 1 answer-sheet page is NOT reachable by layout alone: the items must be shorter or fewer (about 10 to 15 percent less text), or the answer sheet must share a page with the last paper page. The paper rules (R01 text at least 10 pt, code at least 8 pt; R17 columns; R10 code capacity) are not changed.")
FACT = WORDS + " " + MEAS
TITLE = "REPAIR: the midterm paper v2 - 4 pages in total on 2 sheets, seeded mixed order, paper, key and answer sheet in MS Word (.docx), a form code per form, a code box wide enough"
AC_LABEL = "The midterm paper v2 is 4 pages in total (paper plus answer sheet), mixed order, in MS Word, with a form code per form and a code box wide enough"
TXT_B = ("Make the NEW midterm paper v2 as new files (08-tooling/exam; v1.0.0 files, the renderers v1.1/v1.2 and the items v1.0.0 are never edited, SHA-256 before and after). INPUTS: " + WORDS + " THE ITEMS STAY SEEDS: the owner will send the question styles of his class sessions through the coordinator; until the lineage agent passes them to you, build with the items v1.0.0 as they are (and STOP and report instead of inventing an item style); a changed or shorter item is a NEW items version (never an edit). "
         "(1) FOUR PAGES IN TOTAL = the paper plus the answer sheet, printed double sided on 2 sheets. " + MEAS + " Reach 4 pages by the lever you can justify: a new items version with shorter listings and option texts (every item keeps its chapter, Bloom level and answer; the key is rebuilt and checked against the items), or the answer sheet on the last page of the paper if the reader tolerances still hold; report both measured, choose none silently, and do not lower a paper rule. If 4 pages are not reached within the rules, STOP and report the measurements. "
         "(2) MIXED ORDER: the 24 units in a seeded mixed order (chapters and question types mixed), one rule: a permutation drawn from a recorded seed, with the stated constraints (no two consecutive units of the same item; first unit of low difficulty); the number of forms is a PARAMETER with the default 2 (forms A and B with different seeds, to deter copying), a default and NOT the owner's decision; each form has its own form code (a stated rule, valid for the sheet's check digit if there is one), printed on its paper, sheet, layout and key, and the grading tool's pair check refuses a mismatch. "
         "(3) MS WORD: the paper, the key and the ANSWER SHEET are .docx files that open and edit in Word (not PDF only); you can run LibreOffice here, not Word, so the sheet must not depend on Word's own layout choices: fixed table layout, exact row heights, exact column widths, fiducials and the code boxes as absolutely positioned objects, one named font with a metric-compatible fallback, no automatic spacing, no page-break dependence on text flow; say in your report what Word may still shift (fonts, line breaks, cell padding, anchoring, printer scaling). Also give a PDF export of each file for printing. "
         "(4) THE SHEET LAYOUT JSON for the reader is MEASURED on the render of the .docx (LibreOffice to PDF to 300 dpi), never copied from the intended positions; VERIFY: the page count of every file equals its expected count, each bubble centre and fiducial is within 0.5 mm of the layout JSON, and the reader v1.1.0 (v1.2.0 when committed) reads the synthetic sheets of the sheet layout with the registration tolerance: apply to the rendered sheet a shift of up to 3 mm, a scale of up to 1.5 percent and a rotation of up to 0.5 degree (the printed-scan tolerance) and report the result per setting as printed. "
         "(5) CODE BOX at least as wide as the longest allowed line (45 characters) at the printed size, in a NEW renderer version, every code box measured. "
         "(6) The FINAL build of the paper and sheet waits for the reader v1.2.0 (task TK_Repair_Exam_Reader_Build): check git log for it before the last step; the renderer, the .docx writer and the page budget work do not wait. If it is not committed, deliver the build with the reader v1.1.0 named as the reader of record, and say so. "
         "Run the control's own scripts (sen0401_exam_papers_control_check_v1_0_0.py, adapted as a new file). DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES. Commit ONLY your own files to main (git add by path, pull --rebase before push); commit each verified step at once. Report every result as printed. Planned session SEN0401-I54-paperfix; about 5.0 hours (an estimate, G120; it was 2.0 before the owner's words).")
TXT_V = "Open each .docx and PDF and read every page; count the pages (paper plus sheet = 4); render the sheet .docx myself with LibreOffice and measure the bubble and fiducial positions against the layout JSON; apply my own shifts, scales and rotations to the render and read it with the reader of record; run the papers control script; compare the form codes of the forms and the pair check of the grading tool; nochange (SHA-256 of every earlier file)."
AC_G = ("Owner-directed work (" + CR + ", " + WHEN + "). Given the committed items v1.0.0, renderer v1.2.0 and the owner's words, when the NEW paper v2 is made, then ALL of: (1) every file is new and no committed file is edited; (2) paper plus answer sheet are exactly 4 pages, printable double sided on 2 sheets, with text at least 10 pt and code at least 8 pt, measured on the render; (3) the 24 units are in a seeded mixed order by a stated rule, the number of forms is a parameter (default 2, not the owner's decision), each form has a distinct form code carried by its paper, sheet, layout and key; (4) the paper, the key and the answer sheet are .docx files, and the layout JSON of the sheet is measured on the LibreOffice render of the .docx: page count as expected, every bubble and fiducial within 0.5 mm of the layout, and the reader of record reads the sheet under a shift of 3 mm, a scale of 1.5 percent and a rotation of 0.5 degree with 0 silent wrong; (5) no line of a code box is wider than its box, measured for every item; (6) the papers control script passes (key against the items). The items stay seeds until the owner's question styles are passed; no item is invented. Results as printed; if any element fails the work is named failing, and a rule is never changed to pass. " + FACT)
def sub_attr(b, pred, val):
    pat = re.compile(r'(%s )"(?:[^"\\]|\\.)*"(@en)?' % re.escape(pred)); m = pat.search(b); assert m, pred
    return b[:m.start()] + m.group(1) + lit(val) + (m.group(2) or "") + b[m.end():]
def edit_blk(t, sid, fn):
    i, j = T.blk(t, sid); return t[:i] + fn(t[i:j]) + t[j:]
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The midterm paper is 4 pages in total, mixed order, and the paper, key and answer sheet are MS Word files"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso %s, ex:CR3_ExamMission, ex:CR3_PaperFormCode ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, IA, lit("Raised " + WHEN + ". " + FACT))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the four-page, mixed-order, Word paper costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(FACT + " AFFECTED: the not-started story ST_Repair_Exam_Paper and its two tasks and criterion are rewritten (G133: nothing is started); the Done Papers story and its files are kept as the record. A .docx answer sheet cannot be proven to print in Word the way LibreOffice renders it: the sheet is built with fixed geometry, its layout is measured on the render, and the reader gets a stated scan tolerance. The items stay seeds until the owner passes the question styles of his class sessions; the reader repair (ST_Repair_Exam_Reader, unchanged) must be committed before the final build of the paper. NOT AFFECTED: every committed file, the grading tool, the reader story. OPEN FOR THE OWNER: whether the answer sheet may share a page with the paper, whether a second form with another mix is wanted, the cs_encode definition, the 24 items, the default of 6 at Analyze+, and the question styles. ESTIMATE (G120): 5 h build (was 2 h), 1.5 h verification."))
    return t + cr + ia, "Change request with impact assessment: the owner's words of 2026-11-01 on the midterm paper (4 pages in total, mixed order, paper, key and answer sheet in MS Word, question styles to follow); no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") rewrites the criterion, the story and the two tasks of ST_Repair_Exam_Paper, none of them started; a changed criterion is counted by the Backlog digest, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the midterm paper in four pages, mixed order, MS Word"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the owner's words on the midterm paper; nothing is rebuilt here." % OLD.replace("ex:", "")
def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEWB)
    # rewrite the not-started items (G133); states are checked
    for x in (SID, "TK_Repair_Exam_Paper_Build", "TK_Repair_Exam_Paper_Verify", "AC3E_Repair_PaperFormCode"):
        i, j = T.blk(t, x); assert "backlog:Proposed" in t[i:j] or x.startswith("AC3E"), x
    def f_story(b):
        b = sub_attr(b, "rdfs:label", TITLE); b = sub_attr(b, "backlog:hasTitle", TITLE)
        b = sub_attr(b, "backlog:wantsCapability", TITLE)
        b = sub_attr(b, "backlog:hasAuditNote", "Admitted Friday 2026-10-30 and REWRITTEN " + WHEN + " (" + CR + ", ex:CR3_PaperFormCode); nothing was started (G133). One criterion per unit.")
        return b
    t = edit_blk(t, SID, f_story)
    t = edit_blk(t, "TK_Repair_Exam_Paper_Build", lambda b: sub_attr(sub_attr(sub_attr(b, "rdfs:label", "Build: " + TITLE), "backlog:hasTitle", "Build: " + TITLE), "backlog:hasAuditNote", TXT_B))
    t = edit_blk(t, "TK_Repair_Exam_Paper_Verify", lambda b: sub_attr(sub_attr(sub_attr(b, "rdfs:label", "Verify: " + TITLE), "backlog:hasTitle", "Verify: " + TITLE), "backlog:hasAuditNote", TXT_V))
    def f_ac(b):
        b = sub_attr(b, "rdfs:label", AC_LABEL); b = sub_attr(b, "backlog:hasGherkinText", AC_G)
        return sub_attr(b, "backlog:measuredWithVersion", "papers control script (adapted new file); LibreOffice render of the .docx; own position and tolerance measurement")
    t = edit_blk(t, "AC3E_Repair_PaperFormCode", f_ac)
    L = []
    mem = []
    L.append('ex:SC3_ExamWord a backlog:ScopeChange ;\n    rdfs:label "Backlog rewritten for the four-page, mixed-order, Word midterm paper"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, SID, lit("The owner's words of 2026-11-01; the story, its criterion and its two tasks are rewritten while not started (G133); the rule that a change re-ranks the open items. " + FACT)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamWord; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR39 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the four-page Word midterm paper"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: ST_Repair_Exam_Paper rewritten for the owner's four-page, mixed-order, Word paper (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
