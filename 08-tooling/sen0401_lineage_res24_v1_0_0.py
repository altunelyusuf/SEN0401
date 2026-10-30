#!/usr/bin/env python3
"""sen0401_lineage_res24 v1_0_0 - change route (G113, G125 route 2, G133, G134, G147) for (a) the two defects found in the delivered urgent chapter 6 work (the Lecture tab of the page v9.89.0 still lists the 62 slides of the old deck; the deck v2_3_0 fails the deck layout check with 49 items where v2_2_0 was clean) and (b) the owner's decision of 2026-10-30 07:45 Istanbul: build the MIDTERM first, the make-up papers can wait (limited token budget).
A StageRevision from the Backlog stage. Events, one new file each: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog9"; OLD = "ex:Out3_BacklogR36"; NEWB = "ex:Out3_BacklogR37"; R.NEWB = NEWB; ITER = "Iter_54"
CRS = ["ex:CR3_Ch06Repairs", "ex:CR3_MidtermFirst"]; IAS = ["ex:IA3_Ch06Repairs", "ex:IA3_MidtermFirst"]
WHEN = "Friday 2026-10-30 07:45 Istanbul, on the owner's word relayed by the coordinator, and the control of the urgent chapter 6 work by the lineage agent"
F_REP = ("MEASURED 2026-10-30 by the lineage agent on the delivered urgent work (deck v2_3_0, page v9.89.0, template 9.52.9). (1) THE LECTURE TAB: the page's data holds a lecture list of 62 entries, the manifest lecture_v1_3_1.json of the OLD 62-slide deck; the delivered deck v2_3_0 has 71 slides, so the Lecture tab does not show the deck the owner teaches from (the page executor reported it, my count agrees). "
         "(2) THE DECK LAYOUT: the deck layout check v1_0_0 prints 49 items to look at on v2_3_0 (for example slides 63, 65 and 67: 'needs 10.4 pt in 8.6 pt' for the RESULT line, 'needs 24.4 pt in 21.6 pt' for a caption) where v2_2_0 printed 'clean'; the new result lines and captions do not fit their boxes at the size the standard asks. The deck's code, results (52 of 52 re-run equal), prompts, lambda and label words are not in question. "
         "(3) PAGE TESTS: the executor reports that the committed page tests 9.34.2, 9.35.2 and 9.37.0 crash with StopIteration on the new page (the Playground now lists the slide examples first) while the copies 9.34.3, 9.35.3 and 9.38.0 pass; the lineage agent's own runs are recorded in the control note; whether the copies are accepted as the page tests is the owner's ruling and is asked through the coordinator. "
         "(4) NOT MEASURED, as printed: the deck standard check elements D3, D5 and D12 and the deck check example re-run read the '>>>' prompts and cannot read a prompt-free deck; the owner has allowed new reader files beside the old checks (old ones unchanged): this is the existing planned story ST_Code_Gate, which no longer waits for a further word. "
         "(5) RECONCILIATION NEEDED, not hidden: the urgent deck delivered most of what the planned stories ST_Ch06_DeckCode and ST_Ch06_DeckTeach and ST_Template_Panels were to deliver (code corrected, concepts told, panels and Playground); they are not started and their text, versions and dependencies no longer match what exists; they are closed or reduced by a fit-gap and closure step of their own.")
F_MID = ("THE OWNER'S WORD (2026-10-30 07:45 Istanbul): return to the exams; the make-up papers can wait because the token budget is limited; build the MIDTERM first, the make-up later. THE EFFECT ON THE PLAN: the Items story now asks for the 24 items of the MIDTERM only (the make-up items, which must share none with them, become the new story ST_Exam_Items_Makeup, ranked behind, not dropped); the Papers story renders the midterm paper, its key and its answer sheet (the make-up paper becomes ST_Exam_Papers_Makeup); the grading story is unchanged (it reads any sheet). The engine keeps its rule that a make-up never repeats a midterm item, so the make-up items will be written against the finished midterm items. Nothing already measured changes.")
FACT = F_REP + " " + F_MID
COMMON = ("DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES. A committed file is never edited: every output is a new file with a new version number. STOP and report if the task cannot be satisfied without editing a committed file, or if a gate, a test or a threshold would have to change. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. The machine has 2 cores and about 1.8 GB free disk (stop at 0.9): one build or browser run at a time (browser runs only under flock /tmp/page_test.lock). Commit ONLY your own files to main (git add by path, pull --rebase before push); commit each verified step at once.")
def _items_mid(s): 
    s = s.replace("WRITE THE ITEMS OF THE TWO EXAMS (24 for the midterm, 24 for the make-up, the make-up sharing none with the midterm)", "WRITE THE 24 ITEMS OF THE MIDTERM EXAM ONLY (the make-up items are the later story ST_Exam_Items_Makeup, deferred by the owner on 2026-10-30)")
    s = s.replace("REPORT per paper:", "REPORT for the midterm:").replace("(4 items per chapter per paper, chapters 1 to 6;", "(4 items per chapter on the midterm, chapters 1 to 6;")
    s = s.replace("Several sessions may be needed: write what you can in verified steps and report what is left.", "Several sessions may be needed: write what you can in verified steps and report what is left. EVERY ITEM CARRIES ITS SEED LINKS (item keys of the page questions it was built from, or 'none: written from the source of the point') AND ITS CRITICAL-POINT LINKS (point ids of list A), so that the control can follow each item to its origin.")
    return s
def _verify_mid(s): return s.replace("the two papers share no item, and both pass the engine v1.1.0", "the midterm passes the engine v1.1.0")
def _items_makeup(s):
    s = s.replace("WRITE THE ITEMS OF THE TWO EXAMS (24 for the midterm, 24 for the make-up, the make-up sharing none with the midterm)", "WRITE THE 24 ITEMS OF THE MAKE-UP EXAM, sharing NONE with the 24 midterm items (read the midterm items file written by the story ST_Exam_Items; never edit it; the engine refuses a repeat)")
    return s.replace("REPORT per paper:", "REPORT for the make-up:").replace("(4 items per chapter per paper", "(4 items per chapter on the make-up")
def _papers_mid(s): return s.replace("Render the two exams with the engine", "Render the MIDTERM exam with the engine (the make-up paper is the later story ST_Exam_Papers_Makeup, deferred by the owner on 2026-10-30)").replace("with an answer key each and the answer sheet", "with its answer key and its answer sheet")
GATE_NOTE = "The owner allowed new reader files beside the old deck checks, old ones unchanged (relayed by the coordinator 2026-10-30): the word this story waited for is given; it may start when ranked first."
TXT_LEC = ("Make the NEW chapter 6 page (03-materials/ch06/page, the next version number after v9_89_0, never edited, SHA-256 before and after) in which the Lecture tab is built from the manifest of the CURRENT deck v2_3_0 (71 slides; the manifest derived from that deck, for example lecture_v1_4_0.json made by a new builder step as a NEW file, the old lecture_v1_3_1.json is not edited): every slide of the deck has its entry in order with its number and title, and the Lecture tab's count equals the deck's slide count. Use the newest template (9.52.9, not edited) and builders; change nothing else: panels, Playground order, chapter code, concept texts and exam modes stay as in v9.89.0. "
           "PROOF kept as logs: SHA-256 of the old page before and after; the deck's slide count and titles against the page's lecture list, equal; the deck-page code match script (0 slide code lines found nowhere); the page tests that gate a release run serially under flock /tmp/page_test.lock: 9.34.3, 9.35.3 and 9.38.0 (the copies the page executor made) and, as printed, the committed 9.34.2, 9.35.2 and 9.37.0 (they crash with StopIteration on v9.89.0: report that as CANNOT_RUN, never edit them); the panel test; the chapter checks. " + COMMON)
TXT_LAY = ("Make the NEW chapter 6 deck v2_3_1 (03-materials/ch06; v2_3_0 is never edited, SHA-256 before and after) in which the deck layout check v1_0_0 prints 'clean' (it prints 49 items on v2_3_0, e.g. slides 63, 65 and 67: the RESULT line needs 10.4 pt in 8.6 pt; a caption needs 24.4 pt in 21.6 pt): make each text fit its box at the size the standard asks by changing the box (height, position), the text length or the line breaks, never by shrinking type below the deck's standard size and never by lowering the check. Everything else stays: code, result values, notes, pictures, links, numbering. "
           "PROOF kept as logs: SHA-256 of v2_3_0 before and after; the layout check on v2_3_1: clean; my measure script sen0401_deck_teach_measure_v1_0_0.py: 0 prompts, 0 lambda, 0 label shapes; the own control script sen0401_ch06_deck_control_check_v1_0_0.py run with 52 of 52 equal result rows; the overlap and arc checks; the hyperlink count; renders of five changed slides before and after. " + COMMON)
VT_LEC = "Compare the SHA-256 of v9_89_0; compare the lecture list with the deck's slides; run the code match script; run the page tests under the lock and name each CANNOT_RUN; nochange."
VT_LAY = "Compare the SHA-256 of v2_3_0; run the layout check; run the measure and control scripts; run overlap and arc checks; render five slides; nochange."
def crit_rep():
    base = "Owner-directed repair (" + ", ".join(CRS) + ", " + WHEN + "). "
    return {"AC9_Repair_Ch06_Lecture": ("The chapter 6 page lists the 71 slides of the current deck in its Lecture tab",
              base + "Given the page v9.89.0 and the deck v2_3_0 (unchanged) when the NEW page is made, then ALL of: (1) the old page is byte-identical; (2) the Lecture tab lists every slide of the deck v2_3_0 in order with its number and title and the count equals the deck's slide count (71); (3) the code match shows 0 slide code lines found nowhere; (4) the page tests 9.34.3, 9.35.3 and 9.38.0 pass, and the committed 9.34.2, 9.35.2 and 9.37.0 are reported as printed; (5) no committed file is edited. Results as printed; if any element fails the work is named failing. " + FACT, "page test 9.34.3, 9.35.3 and 9.38.0; page test run v1_2_0 under flock; code findings measure"),
            "AC9_Repair_Ch06_DeckLayout": ("The chapter 6 deck v2_3_1 passes the deck layout check clean",
              base + "Given the deck v2_3_0 (unchanged) when the NEW deck v2_3_1 is made, then ALL of: (1) v2_3_0 is byte-identical; (2) the deck layout check v1_0_0 prints clean (49 items on v2_3_0); (3) the code, the 52 result rows (re-run equal), the notes, the pictures and the links are as in v2_3_0, with 0 prompts, 0 lambda and 0 label shapes; (4) the overlap and arc checks give no less; (5) no committed file is edited. Results as printed; if any element fails the work is named failing. " + FACT, "deck layout check v1_0_0; own control script; measure script")}
STS = [("ST_Repair_Ch06_DeckLayout", "REPAIR: the chapter 6 deck v2_3_1 passes the deck layout check clean", ["AC9_Repair_Ch06_DeckLayout"], ["TK_Repair_Ch06_DeckLayout_Build", "TK_Repair_Ch06_DeckLayout_Verify"], "SEN0401-I54-decklayout", TXT_LAY, VT_LAY, 2.0, [], 1.0, "Del3_Ch06Teach", "Obj3_Ch06Teach"),
       ("ST_Repair_Ch06_Lecture", "REPAIR: the chapter 6 page lists the 71 slides of the current deck in its Lecture tab", ["AC9_Repair_Ch06_Lecture"], ["TK_Repair_Ch06_Lecture_Build", "TK_Repair_Ch06_Lecture_Verify"], "SEN0401-I54-lecture", TXT_LEC, VT_LEC, 2.5, ["TK_Repair_Ch06_DeckLayout_Verify"], 1.0, "Del3_PanelView", "Obj3_Ch06Teach")]
def ev_change(t):
    cr1 = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Two defects of the delivered urgent chapter 6 work: the Lecture tab lists the old deck, the new deck fails the layout check"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso %s, ex:CR3_Ch06Teach ;\n    backlog:hasChangeRequestRationale %s .\n') % (CRS[0], IAS[0], lit("Repair items found by the page executor and confirmed by the lineage agent's own control, " + WHEN + ". " + F_REP))
    cr2 = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Build the midterm exam first; the make-up papers can wait"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Shrink ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso %s, ex:CR3_ExamMission ;\n    backlog:hasChangeRequestRationale %s .\n') % (CRS[1], IAS[1], lit("The owner, " + WHEN + ". " + F_MID))
    ia1 = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the two chapter 6 repairs cost and touch"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IAS[0], CRS[0], lit(F_REP + " AFFECTED: two new repair stories (a deck v2_3_1 and a page after v9_89_0, new files); the planned stories ST_Ch06_DeckCode, ST_Ch06_DeckTeach, ST_Template_Panels and ST_Ch06_PageCode need reconciliation with what the urgent work delivered. NOT AFFECTED: every committed file, the exam work. ORDER: the owner said the exams come first; the repairs are ranked below the exam stories, not dropped. ESTIMATE (G120): layout 2 h, Lecture 2.5 h, verification 1 h each."))
    ia2 = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What building the midterm first costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IAS[1], CRS[1], lit(F_MID + " AFFECTED: the Items story and its tasks (not started; midterm only, seed links and critical-point links on every item), the Papers story and its Build task (midterm paper), two new stories ST_Exam_Items_Makeup and ST_Exam_Papers_Makeup (ranked behind). NOT AFFECTED: the engine, the answer sheet, the grading story, every committed file. The plan: the engine v1.1.0 is controlled first, then the 24 midterm items, then the midterm paper; the make-up follows when the owner's budget allows. ESTIMATE (G120): the midterm items 6 h (unchanged), make-up items 6 h and make-up paper 1.5 h moved behind."))
    return t + cr1 + cr2 + ia1 + ia2, "Two change requests with impact assessments: the two defects of the delivered chapter 6 work (Lecture tab on the old deck manifest, deck layout 49 items) and the owner's decision to build the midterm first and the make-up later; no stage changed."
def ev_retract(t):
    reason = ("The change requests " + ", ".join(CRS) + " (" + WHEN + ") add four stories and rewrite the not-started Items and Papers stories' text and criterion; a new criterion is counted by the Backlog digest, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit; the items already in the register, Done ones included, re-enter by admission, not re-dated.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: two chapter 6 repairs and the midterm first"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, ", ".join(CRS), ", ".join(IAS), lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the chapter 6 repairs and the midterm-first decision; nothing is rebuilt here." % OLD.replace("ex:", "")
def _swap(t, bid, fn):
    i, j = T.blk(t, bid); return t[:i] + fn(t[i:j]) + t[j:]
def _lit_of(b, prop):
    m = re.search(r'backlog:%s "((?:[^"\\]|\\.)*)"' % prop, b); assert m, prop
    return m, m.group(1).replace('\\"', '"').replace("\\\\", "\\").replace("\\n", "\n")
def _rewrite(t, bid, prop, fn):
    def f(b):
        m, txt = _lit_of(b, prop); new = fn(txt); assert new != txt, (bid, prop)
        return b.replace(m.group(0), "backlog:%s %s" % (prop, lit(new)), 1)
    return _swap(t, bid, f)
def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEWB)
    # --- rewrites of not-started items (G133)
    for tk in ("TK_Exam_Items_Build", "TK_Exam_Items_Verify", "TK_Exam_Papers_Build"):
        i, j = T.blk(t, tk); assert "startedAt" not in t[i:j], tk
    t = _rewrite(t, "TK_Exam_Items_Build", "hasAuditNote", _items_mid)
    t = _rewrite(t, "TK_Exam_Items_Verify", "hasAuditNote", _verify_mid)
    t = _rewrite(t, "TK_Exam_Papers_Build", "hasAuditNote", _papers_mid)
    def gh(s):
        s = s.replace("24 items per paper, the make-up sharing none with the midterm,", "24 items for the MIDTERM (the make-up items are the later story ST_Exam_Items_Makeup, deferred by the owner on 2026-10-30),")
        s = s.replace("both papers pass the engine v1.1.0", "the midterm passes the engine v1.1.0").replace("the report names, per paper,", "the report names, for the midterm,")
        return s
    t = _rewrite(t, "AC3E_Exam_Items", "hasGherkinText", gh)
    t = _rewrite(t, "AC9_Code_Gate", "hasGherkinText", lambda s: s.replace("THE OWNER'S EXPLICIT WORD for this gate change is required before the task starts.", "THE OWNER'S WORD for this change is given (new reader files beside the old checks, old ones unchanged; relayed by the coordinator on 2026-10-30)."))
    t = _rewrite(t, "TK_Code_Gate_Build", "hasAuditNote", lambda s: s.replace("THE OWNER'S EXPLICIT WORD for this gate change must be recorded in the register before this task starts.", "THE OWNER'S WORD for this change is given (relayed by the coordinator on 2026-10-30)."))
    L = []
    note = "Admitted " + WHEN + " (" + ", ".join(CRS) + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). " + GATE_NOTE
    # --- criteria and cases of the new stories
    crits = {k: ((v[0], v[1], 'ex:TS_ChapterCheck, ex:TS_DeckMatch', v[2]) if len(v) == 3 else v) for k, v in crit_rep().items()}
    mk_items = ("The 24 make-up items are authored, share none with the midterm items and pass the engine", "Given the 24 midterm items (the story ST_Exam_Items Done) and the owner's ruling that page questions are seeds when the 24 items of the make-up exam are authored as new files, then ALL of: (1) every file is new and no committed file is edited; (2) 24 items, sharing none with the midterm items (by id and by the engine's make-up rule and the control's own method), every item authored, none a near copy of a page item (EN11 and the control's method); (3) every item names its seed link(s) or says it has none, the enhancement, the critical point(s) (list A), chapter(s), level, type and source; (4) computed keys re-run equal; terms in the corpus; the conventions hold; (5) the make-up passes the engine v1.1.0 (EN01 to EN11, R01 to R22); results as printed; if any element fails the work is named failing.", "ex:TS_ChapterCheck", "checks written by the executor as new files, run by the control; engine v1.1.0")
    mk_pap = ("The make-up paper is rendered print-ready with its key and answer sheet", "Given the make-up items (ST_Exam_Items_Makeup Done) when the make-up exam is rendered with the engine v1.1.0 as new files, then ALL of: (1) every file is new and no committed file is edited; (2) the paper is white, line-based and large type with its key and answer sheet, the pages counted (sheet included) and within the limit; (3) key and paper agree; (4) results as printed; if any element fails the work is named failing.", "ex:TS_ChapterCheck", "engine v1.1.0 renderer; control's own reading of the PDF")
    crits["AC3E_Exam_ItemsMakeup"] = (mk_items[0], "Owner-directed work (" + CRS[1] + ", " + WHEN + "). " + mk_items[1], mk_items[2], mk_items[3])
    crits["AC3E_Exam_PapersMakeup"] = (mk_pap[0], "Owner-directed work (" + CRS[1] + ", " + WHEN + "). " + mk_pap[1], mk_pap[2], mk_pap[3])
    for aid, (label, g_, tl, ver) in crits.items():
        k = aid[4:]
        L.append(RT.ac_block(aid, label, g_, tl, ver, k).replace("ex:TC9_", "ex:TC9R_"))
        L.append(RT.case_blocks(k, aid).replace("Spec3I_Retro24", "Spec3I_Ch06Teach").replace("ex:Data3S_TC9_", "ex:Data3S_TC9R_").replace("ex:TC9_", "ex:TC9R_")
            .replace("Run the checks on the item as measured in the baseline of 2026-10-25 (an overlap, a manifest example that starts with an error name, a story whose text lies below the first screen, a committed file with status M) and require that nothing is claimed for it.", "Run the checks on the item as it stands before the work and require that nothing is claimed for it.")
            .replace("The finding as measured in the baseline of 2026-10-25 (ex:IA3_Retro24).", "The finding as measured on 2026-10-30 (ex:IA3_Ch06Repairs)."))
    MK = [("ST_Exam_Items_Makeup", "The 24 items of the make-up exam, authored from seeds, sharing none with the midterm", "AC3E_Exam_ItemsMakeup", "Del3_ExamItems", "Obj3_Exam", ["TK_Exam_Items_Verify"], _items_makeup(__import__("sen0401_lineage_res21_v1_0_0").ITEMS_BUILD) if False else None, 6.0, "SEN0401-I54-itemsmakeup"),
          ("ST_Exam_Papers_Makeup", "The make-up exam rendered as a print-ready paper with key and answer sheet", "AC3E_Exam_PapersMakeup", "Del3_ExamPapers", "Obj3_Exam", ["TK_Exam_Papers_Verify", "TK_Exam_Items_Makeup_Verify"], None, 1.5, "SEN0401-I54-papersmakeup")]
    _i, _j = T.blk(t, "TK_Exam_Items_Build"); mi, items_txt = _lit_of(t[_i:_j], "hasAuditNote")
    _i, _j = T.blk(t, "TK_Exam_Papers_Build"); mp, pap_txt = _lit_of(t[_i:_j], "hasAuditNote")
    items_mk = items_txt.replace("WRITE THE 24 ITEMS OF THE MIDTERM EXAM ONLY (the make-up items are the later story ST_Exam_Items_Makeup, deferred by the owner on 2026-10-30)", "WRITE THE 24 ITEMS OF THE MAKE-UP EXAM, sharing NONE with the 24 midterm items (read the midterm items file written by the story ST_Exam_Items, never edit it; the engine refuses a repeat)").replace("REPORT for the midterm:", "REPORT for the make-up:"); assert items_mk != items_txt
    pap_mk = pap_txt.replace("Render the MIDTERM exam with the engine (the make-up paper is the later story ST_Exam_Papers_Makeup, deferred by the owner on 2026-10-30)", "Render the MAKE-UP exam with the engine").replace("its answer key and its answer sheet", "its answer key and its answer sheet"); assert pap_mk != pap_txt
    texts = {"ST_Exam_Items_Makeup": (items_mk, "Check every item against the seed report and the banks with the control's own similarity method, that the make-up shares no item with the midterm, that every seed and critical-point link exists, computed keys re-run equal, and that the make-up passes the engine v1.1.0 (EN01 to EN11, R01 to R22)."),
             "ST_Exam_Papers_Makeup": (pap_mk, "Open the rendered pages, count pages, check print safety and that key and paper agree.")}
    itid = ITER; mem = []
    for (sid, title, crit_id, dl, ob, deps, _x, hrs, sess) in MK:
        bt = "TK_" + sid[3:] + "_Build"; vt = "TK_" + sid[3:] + "_Verify"; mem += [sid, bt, vt]
        btx, vtx = texts[sid]
        L.append(R.story_block(sid, title, dl, ob, [crit_id], [bt, vt], note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(bt, "Build: " + title, "Build", deps if sid != "ST_Exam_Papers_Makeup" else ["TK_Exam_Papers_Verify", "TK_Exam_Items_Makeup_Verify"], sess, "S", hrs, btx, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(vt, "Verify: " + title, "Verify", [bt], "builder", "S+%.1fh" % hrs, 1.0, vtx, "ex:" + itid, "Proposed", True))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    for (sid, title, crits_, tks, sess, txt, vtxt, hrs, deps, vh, dl, ob) in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, dl, ob, crits_, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, vh, vtxt, "ex:" + itid, "Proposed", True))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    L.append('ex:%s a backlog:Iteration ; rdfs:label "Iteration 54: the two chapter 6 repairs and the make-up exam (planned, not started)"@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "2026-11-02T08:00:00"^^xsd:dateTime ; backlog:iterationEnd "2026-11-06T20:00:00"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (
        itid, itid, lit("Planned by the lineage agent on 2026-10-30, NOT started: planned instants, the ceremony is held when the iteration starts. Estimates, not measurements (G120)."),
        lit("The chapter 6 deck layout and Lecture tab are repaired and the make-up items and paper exist, after the midterm. PLANNED, not started."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Exam backlog:metricMovableBy ex:ST_Exam_Items_Makeup, ex:ST_Exam_Papers_Makeup .\nex:Obj3_Ch06Teach backlog:metricMovableBy ex:ST_Repair_Ch06_DeckLayout, ex:ST_Repair_Ch06_Lecture .\n")
    admits = ["ST_Exam_Items_Makeup", "ST_Exam_Papers_Makeup"] + [s[0] for s in STS]
    L.append('ex:SC3_Ch06Repairs a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by two repairs and the make-up split"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (", ".join(CRS), ", ".join("ex:" + a for a in admits), lit("Decided by the owner (the midterm first, 2026-10-30 07:45 Istanbul) and required by the repairs found in the delivered work; applied by the lineage agent. " + FACT)))
    for c in CRS:
        t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(c), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1, c
        L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Ch06Repairs; it was Pending before."@en .\n' % (c, now[:10]))
    L.append("ex:ST_Code_Gate rdfs:comment %s@en .\n" % lit("2026-10-30: " + GATE_NOTE))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR37 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the chapter 6 repairs and the midterm first"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: two repair stories, the make-up items and papers split behind the midterm (Items and Papers rewritten, not started), the gate story's owner word recorded, both change requests Accepted; %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
