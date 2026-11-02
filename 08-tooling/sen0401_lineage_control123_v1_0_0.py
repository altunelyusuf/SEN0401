#!/usr/bin/env python3
"""sen0401_lineage_control123 v1_0_0 - (copy of control122 with the case papers6: TK_Exam_V6_Papers_Build, AC9_Exam_V6_Papers) (copy of control121 with the case ch03rep2: TK_Repair_Ch03_Page2_Build, AC9_Repair_Ch03_Page2; the executor reported NOT ACHIEVED, so the record takes the NOT MET path: the task is Suspended, nothing waived) (copy of control120 with the case items6: TK_Exam_V6_Items_Build, AC9_Exam_V6_Items) (copy of control119 with the case sheet6: TK_Exam_V6_Sheet_Build, AC9_Exam_V6_Sheet) (copy of control118 with the case read6: TK_Exam_V6_Read_Build, AC9_Exam_V6_Read) (copy of control112 with the case items4: TK_Exam_Items4_Build, AC9_Exam_Items4) (copy of control111 with the case deck04teach: TK_Ch04_DeckTeach_Build, AC9_Ch04_DeckTeach, Build Done and Verify open because D5 is NOT_MEASURED) (copy of control110 with the case papers3: TK_Exam_Papers3_Build, AC9_Exam_Papers3, Build and Verify closed) (copy of control109 with the case ch06size: TK_Repair_Ch06_DeckSize_Build, criterion AC9_Repair_Ch06_DeckLayout, the size control check) (copy of control107 with the case deck03teach: TK_Ch03_DeckTeach_Build, AC9_Ch03_DeckTeach, own check teach1 v1_2_0) (copy of control106 with the case deck02teach: TK_Ch02_DeckTeach_Build, AC9_Ch02_DeckTeach, Build Done and Verify open because D5 is NOT_MEASURED) (copy of control105 with the case deck01teach: TK_Ch01_DeckTeach_Build, AC9_Ch01_DeckTeach, Build Done and Verify open because D5 is NOT_MEASURED) (copy of control104 with the case deck03code: TK_Ch03_DeckCode_Build, AC9_Ch03_DeckCode; the own check is sen0401_deck_code_control_check_v1_1_0.py, which does not count monospaced diagram boxes of the old deck as code boxes) (copy of control103 with the case deck02code: TK_Ch02_DeckCode_Build, AC9_Ch02_DeckCode; the executor proof is deck_code_proof_v1_0_0.py with the old and new deck) control of the midterm-scope BUILD tasks (copied from control101). CASE deck05code: TK_Ch05_DeckCode_Build (criterion AC9_Ch05_DeckCode). PARTIAL: the successor checks (element 4) cannot run until the code gate has landed, so the Build is recorded Done on the elements that were run and the Verify task stays open. Usage: prepare CASE COMMITS | record CASE SESSION COMMITS"""
import glob, os, re, subprocess, sys, datetime, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_control54_v1_0_0 as K
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit; TL = "08-tooling/"
GATE = '/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py'; git = K.git; utc = K.utc; sha256 = K.sha256; PRE = K.PRE
CCC = TL + "sen0401_urgent_control_check_v1_0_0.py"; DKC = TL + "sen0401_ch06_deck_control_check_v1_0_0.py"; MAT = TL + "sen0401_deck_page_code_match_v1_0_0.py"; PNL = TL + "sen0401_page_panels_test_v1_0_0.py"
M3 = "03-materials/ch06/"; CTL = REPO + "/" + TL + "verify/iter53/ctl/ctl_sen0401_page_test_v9_"
def deck(pre):
    return dict(crit="AC9_Urgent_Ch06_Deck", tk="TK_Urgent_Ch06_Deck_Build", vt="TK_Urgent_Ch06_Deck_Verify", brief="iter53", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", DKC, M3 + "SEN0401_Ch06_Transactions_3e_v2_3_0.pptx " + M3 + "SEN0401_Ch06_Transactions_3e_v2_2_0.pptx " + M3 + "page/chapter_code_ch06_v1_1_0.json"), ("match", MAT, "06")],
   label={"nochange": "the executor's commits leave every earlier committed file with the same content at the last commit (net; a file changed and restored counts as unchanged)",
          "own": "the control's own script on the deck v2_3_0 and the old deck v2_2_0: prompts, indentation, lambda, label shapes, 52 result rows re-run, code differences listed, the old deck byte-identical",
          "match": "the code match of the newest deck and page: every code line of the chapter-code manifest is on the deck and in the page"},
   elem=[("(1) no committed file is edited and the old deck is unchanged", ["nochange"]), ("(2) to (4) 0 prompts, 0 lambda, 0 label shapes, 0 unindented bodies, every result re-run equal, and the deck's code is the page's Chapter code examples", ["own", "match"])])
def page(pre):
    pt = lambda v, n: ("pt" + v, CCC, "logcheck " + v + " " + n)
    return dict(crit="AC9_Urgent_Ch06_Page", tk="TK_Urgent_Ch06_Page_Build", vt="TK_Urgent_Ch06_Page_Verify", brief="iter53", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("match", MAT, "06"), ("panels", CCC, "logcheck panels 100"), pt("38_0", "300"), pt("34_3", "300"), pt("35_3", "300"), pt("37_0", "300"), pt("34_2", "300")],
   label={"nochange": "the executor's commits leave every earlier committed file with the same content at the last commit (net)",
          "match": "the code match of the newest deck and page: 0 slide code lines found nowhere in the page",
          "panels": "the panel test run by the control on the page v9.89.0 (full screen and reader-set size): no FAIL line",
          "pt38_0": "the control's own run of the page test copy 9.38.0 on the page v9.89.0 (log read: no traceback, no FAIL, all widgets passed, at least 300 features)",
          "pt34_3": "the control's own run of the page test copy 9.34.3 on the page v9.89.0 (same reading)",
          "pt35_3": "the control's own run of the page test copy 9.35.3 on the page v9.89.0 (same reading)",
          "pt37_0": "the control's own run of the COMMITTED page test 9.37.0 on the page v9.89.0 (same reading)",
          "pt34_2": "the control's own run of the COMMITTED page test 9.34.2 on the page v9.89.0 (same reading)"},
   elem=[("(1)(6) no committed file is edited", ["nochange"]), ("(2) full screen and reader-set size in every panel kind", ["panels"]), ("(3)(4) slide examples first in the Playground, 0 slide code lines found nowhere", ["match"]),
         ("(5a) the page test copies 9.34.3, 9.35.3 and 9.38.0 give widgets and features, none failing", ["pt38_0", "pt34_3", "pt35_3"]), ("(5b) the committed page tests 9.34.2 and 9.37.0 named by the criterion give widgets, features and gates not below the old page's", ["pt37_0", "pt34_2"])])
def nocopy(pre):
    return dict(crit="AC3E_Exam_NoCopy", tk="TK_Exam_NoCopy_Build", vt="TK_Exam_NoCopy_Verify", brief="iter51", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("rerun", CCC, "samelines"), ("own", "08-tooling/exam/sen0401_exam_nocopy_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's five commits leave every earlier committed file with the same content (net); all exam files are new",
          "rerun": "the executor's check v1.1.1 re-run by the control (16 of 16 PASS) gives the same PASS and FAIL lines as the executor's log",
          "own": "the control's own check: own pairs with an own ground truth (difflib), the engine's command line, a static read for bank calls, and the byte identity of the 43 v1.0.0 files"},
   elem=[("(1) the engine v1.1.0 is new files and no committed file is edited", ["nochange"]), ("(2)(3) EN11 refuses a page copy with thresholds stated before the run, and the fixture of known answer gives the expected answer", ["rerun", "own"]), ("(4)(5) authored items only, and all rules of v1.0.0 and the owner's decisions still hold", ["rerun", "own"])])
def items(pre):
    return dict(crit="AC3E_Exam_Items", tk="TK_Exam_Items_Build", vt="TK_Exam_Items_Verify", brief="iter54b", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("rerun", CCC, "samelines items"), ("own", "08-tooling/exam/sen0401_exam_items_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's commit adds only new files and edits no earlier committed file",
          "rerun": "the executor's check re-run by the control (all lines PASS, RESULT PASS) gives the same result lines as its committed log",
          "own": "the control's own check: units and chapters, seed keys and point ids resolved by my own loader, trace listings re-run (my own cs_encode supplied for one), the five number keys computed again from the stems, my own similarity of every component against 1236 page items (highest 0.560 on short ordering steps), letters, levels, report counts"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2) 24 units, authored, none a near copy by the engine rule EN11 and by the control's own method (and the nearest pairs read by a person)", ["rerun", "own"]), ("(3) every item names seeds or says none, enhancements, points, chapters, level, type and source, all resolving", ["rerun", "own"]), ("(4) computed keys re-run equal", ["rerun", "own"]), ("(5) terms found, conventions hold, the engine v1.1.0 accepts the midterm", ["rerun"]), ("(6) the report names the points tested and not tested", ["own"])])
def papers(pre):
    return dict(crit="AC3E_Exam_Papers", tk="TK_Exam_Papers_Build", vt="TK_Exam_Papers_Verify", brief="iter54d", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("rerun", CCC, "samelines papers"), ("own", "08-tooling/exam/sen0401_exam_papers_control_check_v1_0_0.py", REPO + "/08-tooling/verify/iter54/ctl/papers_rebuilt")],
   label={"nochange": "the executor's commit adds only new files and edits no earlier committed file",
          "rerun": "the executor's papers check re-run by the control on the control's own rebuild (17 of 17 PASS) gives the same result lines as its committed log",
          "own": "the control's own check: the builder run again gives the same key, graph, layout and measurement files; the key agrees with the items for every keyed entry by my own reading of the graph and the printed steps; page counts by pdfinfo; no image and no colour in the rendered pages; the reader v1.1.0 on 40 synthetic sheets of each of the paper's own layouts"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2) the rendered pages were opened and read by the control, pages counted (7 in chapter order, 6 grouped by type), print safety, key and paper agree", ["rerun", "own"])])
def grading(pre):
    return dict(crit="AC3E_Exam_Grading", tk="TK_Exam_Grading_Build", vt="TK_Exam_Grading_Verify", brief="iter54f", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("rerun", CCC, "samelines grading"), ("own", "08-tooling/exam/sen0401_exam_grading_control_check_v1_0_0.py", "101")],
   label={"nochange": "the executor's commit adds only new files and edits no earlier committed file",
          "rerun": "the executor's check re-run by the control (32 of 32 PASS) gives the same result lines as its committed log",
          "own": "the control's own check: pair check refusals, my own true score from the synthetic students' intended answers and the key, 100 held-out sheets of each order (seeds 63000-63099) and the 40-sheet reader-gap block 41000: bounds contain my true score, no accepted place differs from what the student meant, never FINAL while a written place awaits entry"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2) the tool re-run on synthetic papers with known answers: grades and doubtful lists compared", ["rerun", "own"])])
def deckcode(pre, nn, name, old, new, brief, tk, crit, extra):
    CC = TL + "sen0401_deck_code_control_check_v1_0_0.py"; M3 = "03-materials/ch0%s/" % nn
    return dict(crit=crit, tk=tk, vt=tk.replace("_Build", "_Verify"), brief="iter56", bp="08-tooling/briefs/iter56/BRIEF_SEN0401-I52-%s.md" % brief, pre=pre, ei="EI" + pre, n="00", partial=extra,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", CC, "%s %s%s %s%s HEAD" % (nn, M3, old, M3, new)), ("proof", TL + "ch0%s-deck/deck_proof_v%s.py" % (nn, new.split("_v")[-1].replace(".pptx", "")), "run")],
   label={"nochange": "the executor's commits add new files only; every file that existed before the first commit has the same content at the last (net)",
          "own": "the control's own check on the old and the new deck: slide count, old deck equals its committed blob, 0 prompt lines, code boxes named code N and equal in number, every old code line in order, every old result row on its slide, other text, notes and hyperlinks unchanged, layout check clean, notes check PASS (lambdas reported as INFO)",
          "proof": "the executor's proof script re-run by the control (its RESULT line)"},
   elem=[("(1)(6) the old deck is byte-identical and no committed file is edited", ["nochange"]), ("(2)(3)(5) the code lines in order without prompts, the result rows under their code boxes, everything else unchanged", ["own", "proof"])])
CASES = {"paper2": None, "deck05code": deckcode("Ev102ka", "5", "Ch05", "SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx", "SEN0401_Ch05_WalletRecovery_3e_v3_5_0.pptx", "deck05", "TK_Ch05_DeckCode_Build", "AC9_Ch05_DeckCode",
   "RESULT: elements (1), (2), (3), (5) and (6) MET; element (4) NOT RUN: the successor checks of the code gate are not in the repository yet (the executor logged CANNOT_RUN), the arc check v1_3_0 and the hyperlink count are in the executor's logs and the hyperlink count was re-checked by the control; the criterion is NOT satisfied until the Verify task has run element (4) after the code gate landed. The Build task is Done for the file it delivered; the Verify task and the story stay open. Disclosed risk: the Teach build continues from this deck; if the successor checks fail on it, the deck is repaired as a new version and the Teach build is redone.")}

def paper2(pre):
    EX = TL + "exam/"
    return dict(crit="AC3E_Repair_PaperFormCode", tk="TK_Repair_Exam_Paper_Build", vt="TK_Repair_Exam_Paper_Verify", brief="iter55b", bp="08-tooling/briefs/iter55b/BRIEF_TK_Repair_Exam_Paper_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", EX + "sen0401_exam_paper_v2_control_check_v1_0_0.py", "run"), ("rerun", EX + "sen0401_exam_papers_control_check_v2_0_0.py", EX + "papers_midterm_v2 --no-rebuild")],
   label={"nochange": "the executor's commits leave every earlier committed file with the same content at the last commit (net)",
          "own": "the control's own check: paper and key .docx exported again by LibreOffice here (3 and 1 pages), sheets 1 page, form codes distinct and printed, the key against the items by my own reading of the .docx and my own runs (choice letters, numbers, code traces with a real cs_encode, ordering, matching, fill-in bank) for both forms, the only changed item is the cs_encode item",
          "rerun": "the executor's control script v2.0.0 re-run by the control on the delivered files (31 PASS lines, no FAIL; the rebuild element J is run by the control's own earlier run)"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2)(3)(4)(5)(7)(8) pages, Word files, forms with distinct codes, one item changed, code boxes, key against the items", ["own", "rerun"]), ("(6) the sheet PDF read by the reader of record (v1.1.0; v1.2.0 not yet committed) on synthetic sheets: 0 silent wrong", ["rerun"])])
CASES["paper2"] = paper2("Ev102kb")

def reader2(pre):
    EX = TL + "exam/"
    return dict(crit="AC3E_Repair_ReaderGap", tk="TK_Repair_Exam_Reader_Build", vt="TK_Repair_Exam_Reader_Verify", brief="iter55", bp="08-tooling/briefs/iter55/BRIEF_TK_Repair_Exam_Reader_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", EX + "sen0401_exam_reader_v12_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's commit adds only new files and edits no earlier committed file (net)",
          "own": "the control's own check on seed blocks the executor did not name: the earlier reader, measurement and gap-control files equal their blobs before the commit; the gap control v1.1.0 with reader 1.2.0 on seeds 95000-95059 and 96000-96059 over the three layouts (0 BAD rows, 0 registration failures, held share at most 25 percent); the reader's own measurement on the default layout, 100 sheets, seeds 17000.., against v1.1.0 (no silent wrong, no missed, no unflagged empty; ok rows at least 99 percent)"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2)(3)(4) the reader alone gives 0 missed, 0 silent wrong and 0 empty-not-flagged on every layout, held share at most 25 percent, every sheet registers, the default-layout measurement not worse (on blocks the control chose)", ["own"])])
CASES["reader2"] = reader2("Ev102kc")

def teach5(pre):
    return dict(crit="AC9_Ch05_DeckTeach", tk="TK_Ch05_DeckTeach_Build", vt="TK_Ch05_DeckTeach_Verify", brief="iter56", bp="08-tooling/briefs/iter56/BRIEF_SEN0401-I52-deck05.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the repaired deck v3_7_0 (the first Teach deck v3_6_0 was NOT Done: 54 occurrences of the version probe __import__(sys).version_info, repaired in commit 85f0608). The deck standard check v1_3_1 reports D5 NOT_MEASURED (no story slide detected by label words); that is not a pass and is covered by the control's own reading until a D5 successor exists; the slides 11, 37, 45 and 54 were read as text, not rendered. The Verify task and the story stay open.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "sen0401_deck_teach_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's commits add new files only (net)", "own": "the control's own check of v3_7_0 against v3_6_0: the only difference is the removed version probe, no probe left, 0 prompts, 0 lambdas, 0 label shapes, notes of all 68 slides unchanged"},
   elem=[("(1) no committed file is edited", ["nochange"]), ("(2) the repaired deck differs from v3_6_0 only by the probe and meets the code rules", ["own"])])
def gate(pre):
    return dict(crit="AC9_Code_Gate", tk="TK_Code_Gate_Build", vt="TK_Code_Gate_Verify", brief="iter56", bp="08-tooling/briefs/iter56/BRIEF_SEN0401-I52-codegate.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("fx", TL + "sen0401_code_gate_fixtures_v1_0_1.py", "run")],
   label={"nochange": "the executor's commits add new files only (net)", "fx": "the code gate fixtures v1_0_1 re-run by the control (RESULT PASS)"},
   elem=[("(1) the four old tools are unchanged and the successors are new files", ["nochange"]), ("(2) the code gate fixtures give the expected answers", ["fx"])])
def dchk(pre):
    return dict(crit="AC9_Deck_Checks", tk="TK_Deck_Checks_Build", vt="TK_Deck_Checks_Verify", brief="iter56", bp="08-tooling/briefs/iter56/BRIEF_SEN0401-I52-codegate.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("fx", TL + "sen0401_deck_checks_fixtures_v1_0_1.py", "run"), ("own", TL + "sen0401_deck_checks_control_check_v1_0_0.py", "run"), ("impact", TL + "sen0401_code_gate_impact_v1_0_1.py", "1 2 3 4 5 6")],
   label={"nochange": "the executor's commits add new files only (net)", "fx": "the deck checks fixtures v1_0_1 re-run by the control (27 of 27)", "own": "the control's own counts of prompts, lambda lines and label shapes on the old decks of chapters 1 to 6 equal the successor checks' counts (Ch04 lambda: 3 lines; the control's first count of 4 counted occurrences, two on one line)", "impact": "the impact proof re-run by the control: 0 comparisons not equal on decks with prompts"},
   elem=[("(1) old checks unchanged", ["nochange"]), ("(2) successors give the expected answers on fixtures", ["fx"]), ("(3) successor counts equal the control's counts on the old decks", ["own"]), ("(4) on decks with prompts the old and the new checks agree", ["impact"])])
CASES["deck05teach"] = teach5("Ev103ka"); CASES["gate"] = gate("Ev103kb"); CASES["dchk"] = dchk("Ev103kc")
def honesty(pre):
    return dict(crit="AC9_Code_Honesty", tk="TK_Code_Honesty_Build", vt="TK_Code_Honesty_Verify", brief="iter57", bp="08-tooling/briefs/iter57/BRIEF_TK_Code_Honesty_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "sen0401_deck_honesty_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's commit adds new files only (net)", "own": "the control's own check: v1_1_0 equals v1_0_0 on three decks with prompts, accepts Chapter 1 v3_3_0 and Chapter 5 v3_7_0, refuses a stale caption the control made, and the executor's fixtures end with every stale fixture refused"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2)(3)(4) the successor equals the old check on decks with prompts, accepts the captions of the prompt-free decks and refuses a stale caption", ["own"])])
CASES["honesty"] = honesty("Ev103kd")
def chk6(pre):
    return dict(crit="AC9_Chapter_Check6", tk="TK_Chapter_Check6_Build", vt="TK_Chapter_Check6_Verify", brief="iter57", bp="08-tooling/briefs/iter57/BRIEF_TK_Chapter_Check6_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "sen0401_chapter_check_control_v1_0_0.py", "run")],
   label={"nochange": "the executor's commit adds new files only (net)", "own": "the control's own check: v1_5_0 equals its blob, the only code change is the fixtures call, Deck/Ch01 passes with v1_6_0 and fails with v1_5_0, Deck/Ch04 gives the same lines with both"},
   elem=[("(1)(2) a new file that differs from v1_5_0 only in the fixtures call", ["nochange", "own"]), ("(3)(4) Deck/Ch01 passes, a deck with prompts gives identical lines", ["own"])])
def d01(pre):
    d = deckcode(pre, "1", "Ch01", "SEN0401_Ch01_Introduction_3e_v3_2_0.pptx", "SEN0401_Ch01_Introduction_3e_v3_3_0.pptx", "deck01", "TK_Ch01_DeckCode_Build", "AC9_Ch01_DeckCode", None)
    d["partial"] = None; d["bp"] = "08-tooling/briefs/iter56/BRIEF_SEN0401-I52-deck01.md"; k0 = d["kinds"]
    d["kinds"] = lambda c: [x if x[0] != "proof" else ("proof", TL + "ch01-deck/deck_code_proof_v3_3_0.py", "03-materials/ch01/SEN0401_Ch01_Introduction_3e_v3_2_0.pptx 03-materials/ch01/SEN0401_Ch01_Introduction_3e_v3_3_0.pptx") for x in k0(c)] + [("chk", TL + "sen0401_lineage_chapter_check_v1_6_0.py", "Deck/Ch01")]
    d["label"] = dict(d["label"], chk="the chapter check v1_6_0 (successor checks of the code gate) Deck/Ch01 on the newest deck: exit 0")
    d["elem"] = d["elem"] + [("(4) the successor checks run on the new deck", ["chk"])]
    return d
CASES["chk6"] = chk6("Ev103ke"); CASES["deck01code"] = d01("Ev103kf")
def d02(pre):
    d = deckcode(pre, "2", "Ch02", "SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx", "SEN0401_Ch02_HowBitcoinWorks_3e_v3_1_0.pptx", "deck02", "TK_Ch02_DeckCode_Build", "AC9_Ch02_DeckCode", None)
    d["partial"] = None; d["bp"] = "08-tooling/briefs/iter58/BRIEF_TK_Ch02_DeckCode_Build.md"; k0 = d["kinds"]
    d["kinds"] = lambda c: [x if x[0] != "proof" else ("proof", TL + "ch02-deck/deck_code_proof_v1_0_0.py", "03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx 03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_1_0.pptx") for x in k0(c)] + [("chk", TL + "sen0401_lineage_chapter_check_v1_6_0.py", "Deck/Ch02")]
    d["label"] = dict(d["label"], chk="the chapter check v1_6_0 (successor checks of the code gate) Deck/Ch02 on the newest deck: exit 0")
    d["elem"] = d["elem"] + [("(4) the successor checks run on the new deck", ["chk"])]
    return d
def d03(pre):
    d = deckcode(pre, "3", "Ch03", "SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx", "SEN0401_Ch03_BitcoinCore_3e_v3_1_0.pptx", "deck03", "TK_Ch03_DeckCode_Build", "AC9_Ch03_DeckCode", None)
    d["partial"] = None; d["bp"] = "08-tooling/briefs/iter58/BRIEF_TK_Ch03_DeckCode_Build.md"; k0 = d["kinds"]
    def kinds(c):
        r = []
        for x in k0(c):
            if x[0] == "proof": x = ("proof", TL + "ch03-deck/deck_proof_v3_1_0.py", "03-materials/ch03/SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx 03-materials/ch03/SEN0401_Ch03_BitcoinCore_3e_v3_1_0.pptx")
            if x[0] == "own": x = ("own", TL + "sen0401_deck_code_control_check_v1_1_0.py", x[2])
            r.append(x)
        return r + [("chk", TL + "sen0401_lineage_chapter_check_v1_6_0.py", "Deck/Ch03")]
    d["kinds"] = kinds
    d["label"] = dict(d["label"], chk="the chapter check v1_6_0 (successor checks of the code gate) Deck/Ch03 on the newest deck: exit 0")
    d["elem"] = d["elem"] + [("(4) the successor checks run on the new deck", ["chk"])]
    return d
CASES["deck03code"] = d03("Ev105ka")
def t01(pre):
    P = "03-materials/ch01/SEN0401_Ch01_Introduction_3e_"
    return dict(crit="AC9_Ch01_DeckTeach", tk="TK_Ch01_DeckTeach_Build", vt="TK_Ch01_DeckTeach_Verify", brief="iter58", bp="08-tooling/briefs/iter58/BRIEF_TK_Ch01_DeckTeach_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the deck v3_5_0 (v3_4_0 was not Done: 30 text runs below 9 pt; repaired in commit 67beff8). The deck standard check v1_3_1 reports D5 NOT_MEASURED (no story slide detected by label words); that is not a pass and is covered by the control's own reading of the five story slides (picture and live link on each; sentences, no label words) until a D5 successor exists. The story layout probe, the page link check and the deck match were not run by the executor and belong to the page tasks. The Verify task and the story stay open.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("size", TL + "sen0401_deck_size_control_check_v1_0_0.py", P + "v3_4_0.pptx " + P + "v3_5_0.pptx 67beff8~1"), ("own", TL + "sen0401_deck_teach1_control_check_v1_0_0.py", P + "v3_3_0.pptx " + P + "v3_5_0.pptx 08-tooling/ch01-deck/deck_v3_4_0_logs/concept_table_v3_4_0.json"), ("chk", TL + "sen0401_lineage_chapter_check_v1_7_0.py", "Deck/Ch01")],
   label={"nochange": "the executor's commits add new files only; every file that existed before the first commit has the same content at the last (net)",
          "size": "the control's own check of v3_5_0 against v3_4_0: v3_4_0 equals its committed blob, slide count, every slide's text, shape names, notes and hyperlinks equal, no text run below 9 pt, layout check clean, notes check PASS",
          "own": "the control's own check of the Teach criterion: code and result shapes of the code deck kept, 0 prompts, 0 lambdas, 0 label words, notes 1 to 80 words on every slide, the five story slides with a picture and a live link, the concept table of 117 concepts with none missing",
          "chk": "the chapter check v1_7_0 (successor checks: deck check v1.2.0 under Python 3.14.6, honesty v1_2_0, fixtures, layout, notes) Deck/Ch01 on the newest deck: exit 0"},
   elem=[("(1) the earlier deck is byte-identical and no committed file is edited", ["nochange"]), ("(2)(3)(6)(8) code and results unchanged, 0 label words, prompts and lambdas, notes short with clues, stories as sentences with a picture and a live link, no text below 9 pt", ["size", "own"]), ("(7) layout, notes and deck checks pass (the deck standard D5 is NOT_MEASURED and is disclosed)", ["chk"])])
CASES["deck01teach"] = t01("Ev106ka")
def t02(pre):
    P = "03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_"
    return dict(crit="AC9_Ch02_DeckTeach", tk="TK_Ch02_DeckTeach_Build", vt="TK_Ch02_DeckTeach_Verify", brief="iter58", bp="08-tooling/briefs/iter58/BRIEF_TK_Ch02_DeckTeach_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the deck v3_2_0. The deck standard check v1_3_1 reports D5 NOT_MEASURED (no story slide detected by label words); that is not a pass and is covered by the control's own reading of the three story slides (picture and live link on each; sentences, no label words) until a D5 successor exists. Three code boxes (slides 25 and 30 of the code deck) had a lambda rewritten as def with the same result (the deck check re-runs all 14 examples, 0 mismatches): that is the lambda rule of the criterion; the page Chapter Examples must follow the deck (task TK_Ch02_PageCode_Build). The Verify task and the story stay open.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("size", TL + "sen0401_deck_minfont_check_v1_0_0.py", P + "v3_2_0.pptx"), ("own", TL + "sen0401_deck_teach1_control_check_v1_1_0.py", P + "v3_1_0.pptx " + P + "v3_2_0.pptx 08-tooling/ch02-deck/deck_teach_v3_2_0_logs/concept_table.json 7,45,51 101"), ("chk", TL + "sen0401_lineage_chapter_check_v1_7_0.py", "Deck/Ch02")],
   label={"nochange": "the executor's commit adds new files only; every file that existed before the first commit has the same content at the last (net)",
          "size": "the control's own check: no text run of the new deck below 9 pt, the smallest size printed",
          "own": "the control's own check of the Teach criterion: code boxes of the code deck kept (the lambda boxes rewritten), result shapes kept, 0 prompts, 0 lambdas, 0 label words, notes 1 to 80 words on every slide, the three story slides with a picture and a live link, the concept table of 101 concepts with none missing",
          "chk": "the chapter check v1_7_0 (deck check v1.2.0 under Python 3.14.6, honesty v1_2_0, fixtures, layout, notes) Deck/Ch02 on the newest deck: exit 0"},
   elem=[("(1) the earlier deck is byte-identical and no committed file is edited", ["nochange"]), ("(2)(3)(6)(8) code and results kept, 0 label words, prompts and lambdas, notes short, stories as sentences with a picture and a live link, no text below 9 pt", ["size", "own"]), ("(7) layout, notes and deck checks pass (the deck standard D5 is NOT_MEASURED and is disclosed)", ["chk"])])
CASES["deck02teach"] = t02("Ev107ka")
def t03(pre):
    P = "03-materials/ch03/SEN0401_Ch03_BitcoinCore_3e_"
    return dict(crit="AC9_Ch03_DeckTeach", tk="TK_Ch03_DeckTeach_Build", vt="TK_Ch03_DeckTeach_Verify", brief="iter58", bp="08-tooling/briefs/iter58/BRIEF_TK_Ch03_DeckTeach_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the deck v3_2_0 (61 slides, commit 42b1891). The deck standard check v1_3_1 reports D5 NOT_MEASURED (no story slide detected by label words); that is not a pass and is covered by the control's own reading of the three story slides (6, 16, 28) (picture and live link on each; sentences, no label words) until a D5 successor exists. Three code boxes (slides 25 and 30 of the code deck) had a lambda rewritten as def with the same result (the deck check re-runs all 14 examples, 0 mismatches): that is the lambda rule of the criterion; the page Chapter Examples must follow the deck (task TK_Ch03_PageCode_Build). The Verify task and the story stay open.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("size", TL + "sen0401_deck_minfont_check_v1_0_0.py", P + "v3_2_0.pptx"), ("own", TL + "sen0401_deck_teach1_control_check_v1_2_0.py", P + "v3_1_0.pptx " + P + "v3_2_0.pptx 08-tooling/ch03-deck/deck_v3_2_0_logs/concept_table_v3_2_0.json 6,16,28 115 39"), ("chk", TL + "sen0401_lineage_chapter_check_v1_7_0.py", "Deck/Ch03")],
   label={"nochange": "the executor's commit adds new files only; every file that existed before the first commit has the same content at the last (net)",
          "size": "the control's own check: no text run of the new deck below 9 pt, the smallest size printed",
          "own": "the control's own check of the Teach criterion: code boxes of the code deck kept (the lambda boxes rewritten), result shapes kept, 0 prompts, 0 lambdas, 0 label words, notes 1 to 80 words on every slide, the three story slides (6, 16, 28) with a picture and a live link, the concept table of 115 concepts with none missing",
          "chk": "the chapter check v1_7_0 (deck check v1.2.0 under Python 3.14.6, honesty v1_2_0, fixtures, layout, notes) Deck/Ch03 on the newest deck: exit 0"},
   elem=[("(1) the earlier deck is byte-identical and no committed file is edited", ["nochange"]), ("(2)(3)(6)(8) code and results kept, 0 label words, prompts and lambdas, notes short, stories as sentences with a picture and a live link, no text below 9 pt", ["size", "own"]), ("(7) layout, notes and deck checks pass (the deck standard D5 is NOT_MEASURED and is disclosed)", ["chk"])])
CASES["deck03teach"] = t03("Ev109ka")
def c6(pre):
    P = "03-materials/ch06/SEN0401_Ch06_Transactions_3e_"
    return dict(crit="AC9_Repair_Ch06_DeckLayout", tk="TK_Repair_Ch06_DeckSize_Build", vt="TK_Repair_Ch06_DeckSize_Verify", brief="iter58", bp="08-tooling/briefs/iter58/BRIEF_TK_Repair_Ch06_DeckSize_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the deck v2_4_3 (commit c421380): the only change is the type size. The deck standard check v1_3_1 reports D5 NOT_MEASURED as on v2_4_2 (not a pass; covered by the earlier control of the Ch06 stories). The page Lecture tab and the deck-page code match were not run by the executor and belong to the page task. The criterion of this story (the layout check clean on the deck) holds on v2_4_3; the Verify task of the story and the story stay open.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("size", TL + "sen0401_deck_size_control_check_v1_0_0.py", P + "v2_4_2.pptx " + P + "v2_4_3.pptx c421380~1"), ("min", TL + "sen0401_deck_minfont_check_v1_0_0.py", P + "v2_4_3.pptx"), ("chk", TL + "sen0401_lineage_chapter_check_v1_7_0.py", "Deck/Ch06")],
   label={"nochange": "the executor's commit adds new files only; every file that existed before the first commit has the same content at the last (net)",
          "size": "the control's own check of v2_4_3 against v2_4_2: v2_4_2 equals its committed blob, slide count, every slide's text, shape names, notes and hyperlinks equal, no text run below 9 pt, layout check clean, notes check PASS",
          "min": "the control's own minimum size check: no text run of v2_4_3 below 9 pt, the smallest size printed",
          "chk": "the chapter check v1_7_0 (deck check v1.2.0 under Python 3.14.6, honesty v1_2_0, fixtures, layout, notes) Deck/Ch06 on the newest deck: exit 0"},
   elem=[("(1) the earlier deck is byte-identical and no committed file is edited", ["nochange"]), ("(2) only the type size changed and no text run is below 9 pt", ["size", "min"]), ("(3) layout, notes and deck checks pass on the new deck", ["chk"])])
CASES["ch06size"] = c6("Ev110ka")
def p3(pre):
    EXD = "08-tooling/exam/"
    return dict(crit="AC9_Exam_Papers3", tk="TK_Exam_Papers3_Build", vt="TK_Exam_Papers3_Verify", brief="iter57", bp="08-tooling/briefs/iter57/BRIEF_TK_Exam_Papers3_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "exam/sen0401_exam_papers3_control_check_v1_0_0.py", "/tmp/sen0401_p3ctl"), ("items", TL + "exam/sen0401_exam_items3_control_check_v1_0_0.py", "run"), ("reader", TL + "exam/sen0401_exam_reader3_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's commit adds new files only; no earlier committed file is edited (net)",
          "own": "the control's own check of the papers: paper, key and sheet exported or read again here (paper 5 pages, key 2, sheet 1 per form), question-page fonts, cover fields and form codes, points 25, 25, 25, 25 and 10 bonus from the key, abbreviations expanded at first use, the Q2 programs run here against the key, the same items in both forms",
          "items": "the control's own check of items v1.2.0 re-run (21 items, numeric answers recomputed, abbreviations and tips, structure 25/25/25/25 and 10 bonus, v1.1.0 equals its blob, the executor's check)",
          "reader": "the reader of record v1.2.0 on 40 synthetic sheets of each form with the control's own seed blocks: 0 silent wrong, 0 missed, 0 empty not flagged, held share at most 25 percent"},
   elem=[("(1)(4) every file is new; Word paper and key, PDF sheet", ["nochange", "own"]), ("(2)(3) page 1 is the cover page; 6 pages in all (4 measured impossible), the choice reported", ["own"]), ("(5) the reader of record reads synthetic sheets of both forms with 0 silent wrong and 0 missed", ["reader"]), ("(6) the papers control passes, and the items are still tested", ["own", "items"])])
CASES["papers3"] = p3("Ev111ka")
def t04(pre):
    P = "03-materials/ch04/SEN0401_Ch04_KeysAndAddresses_3e_"
    return dict(crit="AC9_Ch04_DeckTeach", tk="TK_Ch04_DeckTeach_Build", vt="TK_Ch04_DeckTeach_Verify", brief="iter58b", bp="08-tooling/briefs/iter58b/BRIEF_TK_Ch04_DeckTeach_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the deck v3_7_0 (79 slides, commit 04fae7e; v3_6_0, commit 69c8a1d, was not Done: slide 13 carried a shape named code head and two untested code lines, both repaired). The deck standard check v1_3_1 reports D5 NOT_MEASURED (no story slide detected by label words); that is not a pass and is covered by the control's own reading of the three story slides (picture and live link on each; sentences, no label words) until a D5 successor exists. Lambdas stay on slides 11, 46 and 54 and slide 10 says what a lambda is. Executor disclosures accepted: split text boxes have a second part without a bullet mark; the new visuals are shapes and 5 recorded chart objects remain. The Verify task and the story stay open.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("size", TL + "sen0401_deck_minfont_check_v1_0_0.py", P + "v3_7_0.pptx"), ("own", TL + "sen0401_deck_teach1_control_check_v1_2_0.py", P + "v3_5_0.pptx " + P + "v3_7_0.pptx 08-tooling/ch04-deck/deck_v3_6_0_logs/concept_table_v3_6_0.json 8,35,72 87 11,46,54"), ("chk", TL + "sen0401_lineage_chapter_check_v1_7_0.py", "Deck/Ch04")],
   label={"nochange": "the executor's commits add new files only; every file that existed before the first commit has the same content at the last (net)",
          "size": "the control's own check: no text run of the new deck below 9 pt, the smallest size printed",
          "own": "the control's own check of the Teach criterion: the 45 code boxes and 21 result shapes of the code deck v3_5_0 kept, 0 prompts, lambdas only where a slide says what a lambda is, 0 label words, notes 1 to 80 words on every slide, the three story slides with a picture and a live link, the concept table of 87 concepts with none missing",
          "chk": "the chapter check v1_7_0 (deck check v1.2.0 under Python 3.14.6, honesty v1_2_0, fixtures, layout, notes) Deck/Ch04 on the newest deck: exit 0"},
   elem=[("(1) the earlier deck is byte-identical and no committed file is edited", ["nochange"]), ("(2)(3)(6)(8) code and results kept, 0 label words, prompts, lambdas only where taught, notes short, stories as sentences with a picture and a live link, no text below 9 pt", ["size", "own"]), ("(7) layout, notes and deck checks pass (the deck standard D5 is NOT_MEASURED and is disclosed)", ["chk"])])
CASES["deck04teach"] = t04("Ev112ka")
def i4(pre):
    return dict(crit="AC9_Exam_Items4", tk="TK_Exam_Items4_Build", vt="TK_Exam_Items4_Verify", brief="iter59", bp="08-tooling/briefs/iter59/BRIEF_TK_Exam_Items4_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for items v1.3.0 (commits d23f7d2, d6b5017, 9ffc577). The three owner cases are items (C1 spending order replaces i06, C2 mined or not replaces i07, C3 change and fee replaces i02) and point B reworks i03; i05 and i23 are byte-equal. The topic map is reported and NOT hidden: of the owner's nine topics T4 is covered, T6, T7 and T8 are partial, T1, T2, T3, T5 and T9 are GAP; of the six added points A, B and C are covered and D, E and F are GAP. The owner is asked how to fill the GAPs (replace the least central items or keep); a fill is a new items version. DISCLOSED: the printed instruction of Q3.a (from the unchanged structure) says five steps of one payment while C1 is five transactions; the critical points CP2.03, CP2.04, CP2.10 and CP6.09 are held only by weak links; the column fit of the longer C3 and C2 texts is not measured here (the papers task measures it); in C2 the facts leave D and E undecided, which is the careful reading of the spending references and is put to the owner as one question; point B does not ask the end of halving at one satoshi or that the names satoshi and bitcoin are not on chain. The Verify task and the story stay open.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "exam/sen0401_exam_items4_control_check_v1_0_0.py", "run"), ("items", TL + "exam/sen0401_exam_items_midterm_check_v1_3_0.py", ""), ("owner", TL + "exam/sen0401_exam_items_midterm_owner_input_check_v1_3_0.py", "")],
   label={"nochange": "the executor's commits add new files only; no earlier committed file is edited (net)",
          "own": "the control's own check: 17 of 21 items equal v1.2.0, only i02, i03, i06 and i07 differ, i05 and i23 equal; answer types equal the structure; C1 order, C2 mined set, C3 change and fee and the point B subsidy recomputed here without the builder and equal to the stored answers; all 15 owner points carry a verdict COVERED, PARTIAL or GAP",
          "items": "the executor's items check v1_3_0 re-run by the control (exit 0, with the critical-points tool inside)",
          "owner": "the executor's owner-input check re-run (the newest owner topics file, T1-T9 and A-F each an item key or GAP)"},
   elem=[("(1) every file is new, nothing committed is edited", ["nochange"]), ("(2)(3) the three cases and point B recomputed, i05 and i23 kept", ["own"]), ("(4)(7) tips, abbreviations, critical points and the item checks pass", ["items"]), ("(5) the topic map of all nine topics and A to F is reported as item key, partial or GAP", ["own", "owner"]), ("(6) the structure and the answer block types are unchanged", ["own"])])
CASES["items4"] = i4("Ev113ka")
def items3(pre):
    EX = TL + "exam/"
    return dict(crit="AC9_Exam_Items3", tk="TK_Exam_Items3_Build", vt="TK_Exam_Items3_Verify", brief="iter57", bp="08-tooling/briefs/iter57/BRIEF_TK_Exam_Items3_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", EX + "sen0401_exam_items3_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's commits add new files only (net)", "own": "the control's own check: 21 items, four numeric answers recomputed (3900, 65000, 3364, 192), abbreviations expanded and tips present except the two items with the rule inside the question, audit of 23 rows, structure 4 x 25 plus 10 bonus, v1.1.0 equals its blob, the executor's check re-run"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2)(3)(4)(5)(6) audit, tips and abbreviations, structure and checks", ["own"])])
def cover(pre):
    EX = TL + "exam/"
    return dict(crit="AC9_Exam_Cover", tk="TK_Exam_Cover_Build", vt="TK_Exam_Cover_Verify", brief="iter57", bp="08-tooling/briefs/iter57/BRIEF_TK_Exam_Cover_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", EX + "sen0401_exam_cover_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's commit adds new files only (net)", "own": "the control's own check: both demo covers are one page on the control's LibreOffice export, required fields present, no other-course code, a missing template path fails with an error, the template is not tracked (Word is not available: what Word shifts is not measured)"},
   elem=[("(1) every file is new", ["nochange"]), ("(2)(3)(4) one page, the fields, abbreviations spelled out", ["own"])])
CASES["items3"] = items3("Ev103kg"); CASES["items3b"] = items3("Ev103ki"); CASES["cover"] = cover("Ev103kh")
def i5(part, pre, partial):
    P = part.upper()
    return dict(crit="AC9_Exam_Items5" + P, tk="TK_Exam_Items5%s_Build" % P, vt="TK_Exam_Items5%s_Verify" % P, brief="iter62", bp="08-tooling/briefs/iter62/BRIEF_TK_Exam_Items5%s_Build.md" % P, pre=pre, ei="EI" + pre, n="00", partial=partial,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "exam/sen0401_exam_items5_control_check_v1_0_0.py", part)],
   label={"nochange": "the executor's commits add new files only; no earlier committed file is edited (net)",
          "own": "the control's own check of the private part %s: file git-ignored, untracked and unstaged; the executor's check re-run (exit 0, no FAIL line); the answers recomputed here without the builder (code traces executed, numbers recomputed from the stems); counts of option lengths and answer letters; names and counts only are printed" % P},
   elem=[("(1) every committed file is new and no committed file is edited", ["nochange"]), ("(2) the private items file is not tracked and not staged, the check passes, the answers are recomputed here", ["own"])])
PART_A = "RESULT: Build Done for part A (commit 8ad1b4c; private file sha256 cb815c37...). Verify stays open until the merge control. DISCLOSED: in 4 of the 7 choice items the correct option is the longest (5M must rebalance); point L is provisional (invented country); the words 51 percent are not in the book chapters 1 to 6 (the executor used a majority, 60 of 100); the chapter lists of the five new slots differ from structure v1.0.0; 5 items dropped and 11 critical points lost their sole holder (56 to 51 held). NOT_MEASURED: Word and print fit."
PART_B = "RESULT: Build Done for part B (commit 9901387; private file sha256 a929e44a...). Verify stays open until the merge control. DISCLOSED: the engine caps NumericAnswer at Bloom 3, so Q2.d and Q2.g are Bloom 3 and the Analyze-or-higher units of the combined paper fall from 8 to 6, exactly the minimum; the engine refuses equal chapter weights on the combined paper (EN01, EN07), the weights 4,5,3,4,3,5 are declared; not covered by any source: rising hash rate and hardware (I), steady interval against forking risk (F), the soft fork numeric form; sole holders lost: CP6.21, CP6.10, CP6.02, CP3.03, CP5.20. NOT_MEASURED: Word and print fit."
PART_C = "RESULT: Build Done for part C (commit ba5da5a; private file sha256 853edbfd...). Verify stays open until the merge control. DISCLOSED: F partial (no soft fork wording in i23), I partial, O only hand-marked, P a GAP in the machine-read part (the words 51 percent are in the Ch12 pages and in the owner's point P); C2 kept in both readings, provisional; N and Q5.b part 3 provisional; sole holders lost: CP3.14, CP3.16, CP3.17, CP3.18, CP4.07. NOT_MEASURED: Word and print fit, reader and answer sheet behaviour."
CASES["items5a"] = i5("a", "Ev114ka", PART_A); CASES["items5b"] = i5("b", "Ev114kb", PART_B); CASES["items5c"] = i5("c", "Ev114kc", PART_C)
def mv(pre):
    return dict(crit="AC9_Exam_Move_Copy", tk="TK_Exam_Move_Copy_Build", vt="TK_Exam_Move_Copy_Verify", brief="iter65", bp="08-tooling/briefs/iter65/BRIEF_TK_Exam_Move_Copy_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("own", TL + "exam/sen0401_exam_move_control_check_v1_0_0.py", "copy")],
   label={"own": "the control's own check: every file of 08-tooling/exam of the SEN0401 repository (230 files, incl. private/) has an equal-hash copy in the CME clone (own walk, SHA-256), the item backup folder (22 files) is complete in CME, the CME repository is private on the remote (REST API), nothing under exams/ is uncommitted in CME. The copy commits are in CME (709e55e, a7e7361, 4e78db3), not in this repository; the commit given to this record is the control script's commit in this repository"},
   elem=[("(1)-(5) equal hashes for all files, private repository, nothing deleted, nothing with answers committed to SEN0401 by the copy", ["own"])])
def m5(pre):
    return dict(crit="AC9_Exam_Items5M", tk="TK_Exam_Items5M_Build", vt="TK_Exam_Items5M_Verify", brief="iter62", bp="08-tooling/briefs/iter62/BRIEF_TK_Exam_Items5M_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the merged items v1.4.0 (one form; commit c7662f9 for the check script, CME commit a7e7361 for the private files). Verify stays open until Papers5 shows that the form builds, prints and fits. DISCLOSED: 21 items = 24 machine-read units, 4 per chapter, no weight declared; Analyze-or-higher units 7 (minimum 6); 19 critical points lost their only holder and 10 were gained (named in the check log); topic map of 28 points: 20 COVERED, 8 PARTIAL (T7, T8, B, F, G, H, I, O) with reasons; P built as Q1.f with the words 51 percent only in a tip (the engine rule EN08 refuses them as a term); PROVISIONAL: Q4.a and Q4.b (C2, T7), Q1.g (L), Q4.c and Q4.d (N), Q5.b part 3. The control READ by eye the ordering Q3.a (order G E H B J unique), the matching Q3.b and the fill-in Q4.a/Q4.b (K and L mined, N and P not shown) and found them right; that reading is not a script. NOT_RUN: the part check scripts of 5A, 5B, 5C on the merged file; no Word or PDF built yet.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "exam/sen0401_exam_move_control_check_v1_0_0.py", "items5m")],
   label={"nochange": "the executor's commit adds only a new check script; no earlier committed file is edited (net)",
          "own": "the control's own check: the executor's items check v1.4.0 re-run (exit 0, RESULT PASS, 97 PASS lines), the items, the structure and the topic map equal their copies in CME, only the check script is tracked in this repository, nothing staged, the three code traces executed here equal their stored outputs, 21 positions once each"},
   elem=[("(1) every committed file is new and no committed file is edited", ["nochange"]), ("(2) the private files are not tracked, equal in CME, the check passes, the traces recomputed", ["own"])])
CASES["examcopy"] = mv("Ev115ka"); CASES["items5m"] = m5("Ev115kb")
def rm(pre):
    return dict(crit="AC9_Exam_Move_Remove", tk="TK_Exam_Move_Remove_Build", vt="TK_Exam_Move_Remove_Verify", brief="iter65", bp="08-tooling/briefs/iter65/BRIEF_TK_Exam_Move_Remove_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the removal commit cd9706c (41 files, tracked 10276 to 10235). Verify stays open: the criterion element (2) 'no key and no items file with answers is tracked' is NOT yet met, because 4 key files remain tracked in 08-tooling/verify/iter54/ctl/papers_rebuilt/ (chapter and type keys, json and pdf) with the rebuilt papers of the first form beside them, and some bridge and check logs may print answers (not yet inspected). A follow-up task copies those to CME and removes them. Also tracked control scripts that read the removed paths fail until repointed (a follow-up). History is not rewritten.",
   kinds=lambda c: [("own", TL + "exam/sen0401_exam_move_control_check_v1_1_0.py", "remove")],
   label={"own": "the control's own check of the removal commit: it only deletes (41 of 41), every deleted file has an equal-hash copy in CME (own walk), the tracked count fell by exactly 41, the .gitignore is unchanged, the commit is in the remote history with the earlier head as its ancestor, no key, paper, Word file or items file of the removed kinds is tracked in 08-tooling/exam"},
   elem=[("(1) one commit removes exactly the listed files and each has an equal-hash copy", ["own"]), ("(3)(5) no history rewrite, the guard stays", ["own"])])
CASES["examremove"] = rm("Ev116ka")
def fw(pre):
    return dict(crit="AC9_Exam_Move_Followup", tk="TK_Exam_Move_Followup_Build", vt="TK_Exam_Move_Followup_Verify", brief="iter66", bp="08-tooling/briefs/iter66/BRIEF_TK_Exam_Move_Followup_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("own", TL + "exam/sen0401_exam_move_control_check_v1_2_1.py", "remove 664b0b3 cc8d986"), ("scan", TL + "exam/sen0401_exam_move_control_check_v1_2_1.py", "leakscan")],
   label={"own": "the control's own check of the removal commit 664b0b3: it only deletes (42 of 42), every deleted file has an equal-hash copy in CME (own walk), the tracked count fell by exactly 42, the .gitignore is unchanged, the commit is in the remote history, no key, paper, Word file or items file of the removed kinds is tracked",
          "scan": "the control's own search: 522 strings of 40 to 200 characters taken from the private items and key files in CME are searched with git grep in the tracked files of 08-tooling/exam, verify and briefs; the allow-list holds course-fact files (critical points, analysis, fixtures, seed report, structure, owner topics, topic maps, engine logs, the first items report); the result of this line is read as printed"},
   elem=[("(1)-(5) the decisions were printed, the copies are equal, one removal commit, no history rewrite", ["own"]), ("(4) no answer-bearing file of the decided kinds remains tracked (search by answer strings)", ["scan"])])
def rp(pre):
    return dict(crit="AC9_Exam_Move_Repoint", tk="TK_Exam_Move_Repoint_Build", vt="TK_Exam_Move_Repoint_Verify", brief="iter66", bp="08-tooling/briefs/iter66/BRIEF_TK_Exam_Move_Repoint_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for three new control scripts that read the CME copies (papers control v1_0_1, grading control v1_0_1, reader control v1_0_1; commit 3d36f75). The control diffed each against its v1_0_0 (only the path lines and the NOT_RUN guard differ), ran the guard with a missing CME folder (NOT_RUN, exit 3), re-ran the grading control (101: CONTROL PASS, no differing line against the last committed log) and the reader control (RESULT PASS). Verify stays open: NOT_RUN or held back by the executor, stated plainly: the items, items3, items4, papers3 and paper_v2 controls (answer text in the code; kept outside the repository, now in CME, 0 differing lines when re-run); the papers control v2_0_1 (2 differences from later changes); the items-midterm check v1_3_1 (4 differences from later changes); the owner-input check v1_3_1 (1 difference, a newer topics file); the items-midterm checks v1_0_1 and v1_2_1, the builds v1_0_1, v1_2_1 and v1_3_1 and the papers builds v1_0_1 and v2_0_1 (NOT_RUN). Older checks not repointed: items5a, 5b, 5c checks, the v1_4_0 items check (reads v1_3_0), answersheet check v3_0_0, reader gap control v1_1_0, grading measure, analysis build, papers check v1_0_0. A no-deletion gate fails by design after the removal. The 43 historic one-shot lineage scripts are history and stay. The control did NOT re-run the papers control v1_0_1 (it needs a rebuild folder).",
   kinds=lambda c: [("nochange", CCC, "nochange " + c)],
   label={"nochange": "the executor's commit adds only new files; no earlier committed file is edited (net)"},
   elem=[("(2) every file is new and no committed file is edited", ["nochange"])])
CASES["examfollow"] = fw("Ev117ka"); CASES["exampoint"] = rp("Ev117kb")
def pp(pre):
    return dict(crit="AC9_Exam_Papers5", tk="TK_Exam_Papers5_Build", vt="TK_Exam_Papers5_Verify", brief="iter62", bp="08-tooling/briefs/iter62/BRIEF_TK_Exam_Papers5_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the midterm paper v5 (one form; private files in the CME clone, CME commit 50228be; five scripts in this repository, commit 88c765b). Verify stays open. NOT MET: the 4-page target; the paper is 6 pages on the control's own LibreOffice export (cover plus 5 question pages), the key 3, the sheet 1, which is the owner's fallback (six pages with readability). NOT_MEASURED: the page count in Microsoft Word itself (only the LibreOffice export is measured; the warning box on the cover sits near the page bottom). DISCLOSED: provisional readings Q4.a and Q4.b (case C2, T7), Q1.g (L), Q4.c and Q4.d (N), Q5.b part 3; the words 51 percent only in a tip of Q1.f; 8 topic-map points PARTIAL; 18 critical points lost their only holder and 10 were gained (an earlier note said 19; the 18 named lines of the items check are the count); Analyze-or-higher units 7 against a minimum of 6; the printed order of sub-questions is a mixed draw. The control read every page image of the paper, the key and the sheet, checked every key letter, the matching, the ordering and the fill-in keys against the items and the printed text by eye, and found them right. The control also found that the papers control script printed the numbers of question 2 in its code; it was removed from the public tree (commit 756308d) and is in CME.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "exam/sen0401_exam_papers5_move_control_v1_0_0.py", "")],
   label={"nochange": "the executor's commit adds only new files; no earlier committed file is edited (net)",
          "own": "the control's own check: the three files have the reported hashes, my own LibreOffice export gives paper 6, key 3, sheet 1 pages, the executor's papers control (all PASS) and sheet check (10 of 10 PASS) re-run from the CME clone, every choice letter of the key equals the printed letter of the correct option by my own docx read, and the leak search of the public tree passes"},
   elem=[("(1) every committed file is new", ["nochange"]), ("(2)-(5) pages, hashes, key against the printed paper, the sheet read by the reader of record, no question or answer in the public tree", ["own"])])
CASES["papers5"] = pp("Ev118ka")
def rd6(pre):
    return dict(crit="AC9_Exam_V6_Read", tk="TK_Exam_V6_Read_Build", vt="TK_Exam_V6_Read_Verify", brief="iter67", bp="08-tooling/briefs/iter67/BRIEF_TK_Exam_V6_Read_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "exam/sen0401_exam_readability_control_check_v1_0_0.py", "")],
   label={"nochange": "the executor's commit adds only new files; no earlier committed file is edited (net)",
          "own": "the control's own check: SHA-256 of the four public files and the two baseline files in CME as reported; the fixtures re-run (22 stems, 5 directions, RESULT PASS, table rows equal the committed log); one expectation changed in a copy gives RESULT FAIL; the baseline of the v5 paper and items re-run equals the CME text (exit 1 by design: v5 fails R1 to R5); my own word count of the stems above 60 words agrees; no 40-character sentence of the private items in the fixtures; the public leak search passes. DISCLOSED: the R2 glossary test is mechanical; paper tables and footers are not read; Word pagination is NOT_MEASURED; R6 abbreviations need a person's confirmation"},
   elem=[("(1) new tool and rule data, no question or answer inside; (5) no committed file edited", ["nochange", "own"]), ("(2)(3)(4) at least ten fixtures answered as expected, a wrong answer reported, report by key and label, the v5 baseline printed", ["own"])])
CASES["read6"] = rd6("Ev119ka")
def sh6(pre):
    return dict(crit="AC9_Exam_V6_Sheet", tk="TK_Exam_V6_Sheet_Build", vt="TK_Exam_V6_Sheet_Verify", brief="iter67", bp="08-tooling/briefs/iter67/BRIEF_TK_Exam_V6_Sheet_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the scoring rule and module, the sheet v6 (two A4 pages) and the reader v1.3.0 (public commit 63ce497; private files in CME commit 43fb636). Verify stays open until Papers6 shows the sheet in the paper set. NOT_MEASURED: Word pagination (the sheet is a PDF). DISCLOSED: the 5a and 5b lines on the sheet are 4 lines against 6 on the question pages; the paper builder must supply tips as label and text pairs; the reader does not read digits; the page-2 note is longer than one sentence. OWNER POINTS (to confirm, defaults implemented): the penalty fraction p/(1-p), 1/3 for choice of four, is derived from the zero-gain principle, with the table of alternatives; the negligible limit p below 0.005 (numbers of three or more digits cost nothing extra); no floor at 0; two marks in one place count as no answer. The control did not independently recompute the four sheet-versus-page fixture scores; it relies on the executor's hand computations and the check's own pass.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "exam/sen0401_exam_sheet6_control_check_v1_0_0.py", "")],
   label={"nochange": "the executor's commit adds only new files; no earlier committed file is edited (net)",
          "own": "the control's own check: SHA-256 of the 8 public and 4 CME files as reported; my own exact derivation of every penalty p/(1-p) (zero expected blind gain) and the rule file states them; the scoring check re-run (13 of 13 PASS) and the sheet check re-run (22 of 22 PASS, reader v1.3.0 on 80 synthetic sheets, 0 silent wrong, 0 missed); pdfinfo gives 2 A4 pages; I viewed both page images; the leak search of the public tree passes"},
   elem=[("(1)(2) scoring rule file and module, blind guess near zero, penalty derived", ["own"]), ("(3)(4) sheet of two pages, lines for 5a and 5b, tips page, reader v1.3.0", ["own"]), ("(5) every file is new and no committed file is edited", ["nochange"])])
CASES["sheet6"] = sh6("Ev120ka")
def it6(pre):
    return dict(crit="AC9_Exam_V6_Items", tk="TK_Exam_V6_Items_Build", vt="TK_Exam_V6_Items_Verify", brief="iter67", bp="08-tooling/briefs/iter67/BRIEF_TK_Exam_V6_Items_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for items v1.5.0, structure v1.2.0 and topic map v1.5.0 (private files in CME commits d336c59 and 5523476; check script in this repository, commit 6c1c984). Verify stays open until Papers6 builds and prints the form. DISCLOSED: the executor's own check ends RESULT FAIL on hygiene lines only (git status of files of another session); after that session's files were committed (e134bc7) the control re-ran the critical-points tool and the engine check on the tree; the executor's own check script was NOT re-run by the control (it expects the private folder inside the public repository and cannot run from the CME clone as it stands). Whether the shortened stems keep their meaning is a human reader's judgment. CP4.12 (the vanity point) lost its only holder by the owner's order; the committed critical-points list and older committed files still mention it. RECONCILED: the penalty for numbers: the structure gives 0 for all number and trace places (p = 1/100000 for five boxes) while the scoring module takes p from the digits of the key with a bound of 0.005 (1/99 for a two-digit key, 1/9 for a one-digit key, 0 from three digits); the scoring module governs, because it is what the tips page prints and what the scoring check simulates, and it protects the worst-case guesser who knows the size of the answer; the structure fields for numbers are informational and the paper builder takes penalties from the scoring module. The limit itself is an owner point already raised with the sheet. The Q2.a item answer 32 seconds is a new key.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", TL + "exam/sen0401_exam_items6_control_check_v1_0_0.py", ""), ("cp", TL + "exam/sen0401_exam_critical_points_check_v1_0_0.py", ""), ("eng", TL + "exam/sen0401_exam_engine_check_v1_1_1.py", "")],
   label={"nochange": "the executor's commit adds only new files; no earlier committed file is edited (net)",
          "own": "the control's own check: SHA-256 of the seven files as reported; v1.4.0 equals its CME blob; the other 20 items have the same type, answer, options, computed, points and key value as v1.4.0; the removed item is the vanity item; the new item's key (2 to the 12 divided by 16 divided by 8 = 32 seconds) recomputed by my own program; stems 60 words or fewer and how_to_answer 25 words or fewer by my own count; no vanity trace in the new files; every penalty p/(1-p) as exact fractions; the leak search of the public tree passes",
          "cp": "the critical-points tool re-run by the control on the committed tree (8 of 8 checks)",
          "eng": "the engine check v1.1.1 re-run by the control on the committed tree (16 checks)"},
   elem=[("(1)-(6) items, structure, topic map, penalties, stems and directions", ["own"]), ("(7) the critical-points tool and the engine check pass on a committed tree", ["cp", "eng"]), ("(8) every file is new and no committed file is edited", ["nochange"])])
CASES["items6"] = it6("Ev121ka")
def r2(pre):
    CK = TL + "sen0401_ch03page2_control_check_v1_0_0.py"
    return dict(crit="AC9_Repair_Ch03_Page2", tk="TK_Repair_Ch03_Page2_Build", vt="TK_Repair_Ch03_Page2_Verify", brief="iter64", bp="08-tooling/briefs/iter63/BRIEF_TK_Repair_Ch03_Page2_Build.md", pre=pre, ei="EI" + pre, n="00", partial=None,
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("cause", CK, "cause"), ("page", CK, "page")],
   label={"nochange": "the executor's commits add only new files (diagnostic copies of the page test and hold scripts and logs); no earlier committed file is edited (net)",
          "cause": "the control's own count of the diagnostic runner files: v9_75_0 10 runs, 2 with a main-thread budget [FAIL]; v9_73_0 1 run, 0 budget [FAIL]; no 2063 ms task in any log; DOM probe 98 editors on both pages (8443 and 9109 elements). NOT in the executor's report: the endless-program feature failed in one v9_75_0 busy run and in the one v9_73_0 busy run, so the shipped page v9_73_0 also failed one of its one busy runs",
          "page": "element (3)-(5): a new page v9_76_0 exists and the page test passed on it five times in a row: no such page was built, no proof step was run (NOT_RUN)"},
   elem=[("(1) every file is new and v9_74_0 and v9_73_0 are byte-identical", ["nochange"]), ("(2) the cause is found from a trace and reported with the numbers of every run", ["cause"]), ("(3)-(5) a new page passes 9.38.0 five times in a row, 9.34.3, the panel test, the chapter check and the code match", ["page"])])
CASES["ch03rep2"] = r2("Ev122ka")
def pp6(pre):
    CK = TL + "exam/sen0401_exam_papers6_control_check_v1_0_0.py"; SK = TL + "exam/sen0401_exam_answersheet_check_v6_1_0.py"; D = "/home/claude/CME/exams/SEN0401/08-tooling/exam/papers_midterm_v6"
    return dict(crit="AC9_Exam_V6_Papers", tk="TK_Exam_V6_Papers_Build", vt="TK_Exam_V6_Papers_Verify", brief="iter67", bp="08-tooling/briefs/iter67/BRIEF_TK_Exam_V6_Papers_Build.md", pre=pre, ei="EI" + pre, n="00",
   partial="RESULT: Build Done for the midterm paper, key and sheet v6 (form code 60012; private files in the CME clone, commit e8efedb; scripts in this repository, commit 4a09097). Verify stays open. The control READ every page image (paper 6, key 3, sheet 3). READY TO PRINT WITH STATED LIMITS (the owner received the files on 2026-11-02 after the urgent word of 15:43 Istanbul). NOT MET as the owner wished: the sheet is 3 pages, not 2, because the 94 tips do not fit one page at 10.5 pt (tips on pages 2 and 3, only page 1 is read by the reader; accepted by the control, nothing cut); the paper is 6 pages (the owner's fallback 'four pages or else six'). NOT_MEASURED: Word pagination and the look of the bordered boxes in Word. DISCLOSED: the readability tool reports R2 on three entries (paper 1b the clause 'Case one: ...', 1e the table 'With 10 percent of the hash power: z=2: ...', 4d the clause 'A block is filled by weight: ...'), read by the control as mechanical false positives; R3 fails as run on the paper alone because the tool has no tip lists (the executor's second run with the tips supplied passes); the executor edited its own committed library v6.0.0 (2a48072) in this task, disclosed; the sheet has 4 answer lines for 5a and 5b against 6 on the question pages; provisional readings 5a part 3 and Q4.e/Q4.f. A floor at 0 on the paper total (owner ruling 16:52) is handled by ST_Exam_V6_Floor: the key of this build still says the total is not raised to 0.",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", CK, "a0551543 c7ae981d e3de7bba"), ("sheet", SK, D + " --tag sen0401_exam_midterm_v6_0_0_sheet --key " + D + "/sen0401_exam_midterm_v6_0_0_key.json --log /tmp/sen0401_ctl123_sheet61.txt")],
   label={"nochange": "the executor's public commit adds only new scripts; no earlier committed file is edited (net)",
          "own": "the control's own check: the three files have the reported hashes (paper a0551543, key c7ae981d, sheet e3de7bba), my own LibreOffice export gives paper 6, key 3, sheet 3 pages, every choice letter of the key equals the printed letter of the correct option, the readability tool as it stands (R1, R4, R5, R6 pass, R2 fails 3 of 23, R3 as read), the cover prints the penalty and two-answers sentences, the leak search of the public tree passes",
          "sheet": "the executor's sheet check v6.1.0 re-run by the control on the CME sheet (22 checks, reader v1.3.0 on 40 synthetic sheets at each of two seed bases)"},
   elem=[("(1) every public file is new and no committed file is edited", ["nochange"]), ("(2)-(5) the paper, key and sheet v6 measured, key against the printed paper, the sheet checked", ["own", "sheet"])])
CASES["papers6"] = pp6("Ev123ka")
def setup(case):
    global CS, LOG, WORK, kinds, LABEL, ELEM
    CS = CASES[case]; LOG = os.path.join(REPO, TL, "verify/iter56/bridge_" + case); WORK = "/tmp/sen0401_ctl102_" + case; kinds = CS["kinds"]; LABEL = CS["label"]; ELEM = CS["elem"]
def prepare(case, c):
    setup(case)
    os.makedirs(LOG, exist_ok=True); os.makedirs(WORK, exist_ok=True); draft = [PRE]
    for kind, spec, tid in kinds(c): draft.append('ex:Ev55_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, lit(LABEL[kind]), tid, spec))
    d = WORK + "/draft.ttl"; open(d, "w").write("".join(draft)); cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{spec}_{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-100).log 2>&1' % LOG
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", WORK + "/bridge.ttl"], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(r.stdout[-300:])
def last(tid):
    tid = tid[0] + "_" + tid[1]
    p = os.path.join(LOG, "bridge_%s.log" % re.sub(r"[^A-Za-z0-9\n]", "_", tid)[:100]); ls = [l for l in open(p, errors="replace").read().splitlines() if l.strip()] if os.path.exists(p) else []
    return " ".join(ls)[:300] if ls else "(log missing)"
def record(case, sess, c):
    setup(case)
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; TK = CS["tk"]; VT = CS["vt"]; CRIT = CS["crit"]
    v = S.verdicts(WORK + "/bridge.ttl"); K_ = kinds(c); V = {k: v["Ev55_" + k] for k, _, _ in K_}; OUT = {k: last((sp, i)) for k, sp, i in K_}
    began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); cm = c.split(","); end = utc(cm[-1])
    files = sorted({f for x in cm for f in git("show", "--name-only", "--format=", x).splitlines() if f}); logs = sorted(os.path.relpath(os.path.join(dp, f), REPO) for dp, _, fs in os.walk(LOG) for f in fs)
    allf = sorted(set(files) | set(logs) | {TL + "sen0401_lineage_control101_v1_0_0.py", TL + "sen0401_lineage_work_begun_v1_17_0.py", TL + "sen0401_urgent_control_check_v1_0_0.py"}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values())
    L.append('ex:EI55 a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion "brief of the register as generated" ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (lit("Executor session " + sess), began, end, lit("Started at the recorded work begun (%s UTC, as reported by the coordinator); retired at its commit %s (%s UTC)." % (began, c, end))))
    bp = CS["bp"]
    L.append('ex:Brief55 a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI55 ;\n    rdfs:comment %s .\n' % (lit("Brief of " + TK), TK, CRIT, lit("File %s, SHA-256 %s." % (bp, sha256(bp)))))
    for kind, spec, tid in K_:
        ok, at, how = V[kind]
        L.append('ex:Ev55_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (kind, lit(LABEL[kind]), CRIT, tid, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, _) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), now))
    lines = []; bad = []
    for name, ks in ELEM:
        okk = all(V[k][0] for k in ks); bad += [] if okk else [name]; lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s -> %s" % ("verified" if V[k][0] else "NOT verified", OUT[k][:200]) for k in ks)))
    ex = ["Ev55_" + k for k, _, _ in K_]; evs = ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files)
    DEV = os.environ.get("CTL_EXTRA", "")
    if not bad:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. %s %s" % (now[:10], nxt, " | ".join(lines), CS.get("partial") or "RESULT: MET.", DEV))))
        i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
        L.append(C.transition("Done55T_" + TK, TK, "T_Complete", end, "Done on the executor's commit %s (%s UTC), recorded in v%s on %s once the control run gave it bridge-verified evidence." % (c, end, nxt, now), TK + " completed"))
        L.append('ex:Harness55_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, evs, lit("Done, recorded %s: delivered by the executor session %s (commit %s). Results are those of the evidence nodes and the note of %s. %s" % (now[:10], sess, c, CRIT, DEV))))
        if not CS.get("partial"):
            i, j = T.blk(t, VT); b = t[i:j]; assert ("backlog:hasState backlog:Proposed" in b or "backlog:hasState backlog:Ready" in b) and "startedAt" not in b, VT
            wasprop = "backlog:hasState backlog:Proposed" in b
            tmp = (t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]) if wasprop else t; ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
            r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp"); assert "VERDICT     : READY" in r.stdout, r.stdout[-300:]
            time.sleep(1.1); start = M.now(); time.sleep(1.1); fin = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
            t = t[:i] + b.replace("backlog:hasState backlog:Proposed" if wasprop else "backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (start, fin, fin), 1) + t[j:]
            if wasprop: L.append(C.transition("Ready55T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the start gate said READY." % (ready, TK, nxt), VT + " ready"))
            L.append(C.transition("Begin55T_" + VT, VT, "T_Start", start, "Verification begun %s UTC by the lineage agent after the start gate said READY, inside the started sprint ex:%s." % (start, it), VT + " started"))
            L.append(C.transition("Done55T_" + VT, VT, "T_Complete", fin, "Verification finished %s UTC: the checks ran on the bridge and are verified; recorded as printed." % fin, VT + " completed"))
            L.append('ex:Harness55_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
            L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, CRIT, evs, lit("Done, recorded %s: the elements are those of the control of %s in the same version." % (now[:10], TK))))
    else:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s): %s. RESULT: NOT MET: %s. %s" % (now[:10], nxt, " | ".join(lines), "; ".join(bad), DEV))))
        why = "Paused %s UTC, not Done: elements not met: %s (nothing waived, the criterion is not edited)." % (now, "; ".join(bad))
        i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
        L.append(C.transition("Susp55T_" + TK, TK, "T_Suspend", now, why, TK + " suspended")); L.append('ex:%s backlog:hasEvidence %s .\n' % (TK, evs))
    RN = lambda x: re.sub(r"(Ev|EI|Brief|Harness|Done|Begin|Ready|Susp)55", lambda m: m.group(1) + "102" + {"deck05code": "ka", "paper2": "kb", "reader2": "kc", "deck05teach": "ta", "gate": "tb", "dchk": "tc", "honesty": "td", "chk6": "te", "deck01code": "tf", "items3": "tg", "cover": "th", "items3b": "ti", "deck02code": "tj", "deck03code": "tk", "deck01teach": "tl", "deck02teach": "tm", "deck03teach": "to", "ch06size": "tp", "papers3": "tq", "deck04teach": "tr", "items4": "ts", "items5a": "ua", "items5b": "ub", "items5c": "uc", "examcopy": "ud", "items5m": "ue", "examremove": "uf", "examfollow": "ug", "exampoint": "uh", "papers5": "ui", "read6": "uj", "sheet6": "uk", "items6": "ul", "ch03rep2": "um", "papers6": "un"}[case], x)
    print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + RN("".join(L)), "LS_InProgress"), nxt, cur, "Control of the midterm-scope work (%s, %s): %s." % (TK, sess, ("MET, Build Done, Verify open" if CS.get("partial") else "MET, Build and Verify Done") if not bad else "NOT MET: " + "; ".join(bad))))); print(bad)
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]](*sys.argv[2:])
