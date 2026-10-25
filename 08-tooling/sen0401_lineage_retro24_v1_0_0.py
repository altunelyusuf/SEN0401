#!/usr/bin/env python3
"""sen0401_lineage_retro24 v1_0_0 - change route (rulings G104, G125, G127, G129, G133, G136, G147; the owner's standing orders) for the retrofit of all chapters, planned on the MEASURED state of 2026-10-25.
The owner's order: after the urgent chapters 5 to 8, return to ALL chapters starting with chapter 1 and bring each (deck, page, research set and page ABox) to the course standard; build what remains.
Same route as sen0401_lineage_rep21: a ChangeRequest with an ImpactAssessment, a StageRevision from the Scope stage (a deliverable is added to the closed scope, G127), the Scope, Goal, Objective and Backlog
outputs rebuilt one per version, a last version fills the last commit. The Backlog version RESTATES the criteria of the open retrofit stories on the current standard (the old Iteration 21 items are withdrawn by the next tool,
after their replacements exist), adds the story-layout repair of the pages of chapters 5 to 8, the template 9.52.3, the chapter 1 verify script, and plans Iterations 24 (held) and 25 to 28 (planned).
New files only: the register versions here; nothing committed earlier is edited.
Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_ch78_rev_v1_0_0 as R
lit = G.lit
CR = "ex:CR3_Retro24"; IA = "ex:IA3_Retro24"; REV = "ex:Revision_Lineage3_Scope11"
ACTIVE = ["ex:Out3_ScopeR11", "ex:Out3_GoalR11", "ex:Out3_ObjectiveR11", "ex:Out3_BacklogR13"]; NEWB = "ex:Out3_BacklogR14"; R.NEWB = NEWB
R.IT1 = "ex:Iter_24"
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route under the owner's standing orders (retrofit all chapters starting with chapter 1; repairs re-rank the open items; a lineage never waits on unrelated questions)"
DECKS = ["01", "02", "03", "04", "09", "10", "11", "12", "13", "14"]; URGENT = ["05", "06", "07", "08"]
ITERS = {  # id: (label, start, end, goal)
    "Iter_24": ("Iteration 24: the decks of chapters 1 to 3 and the template 9.52.3", None, "2026-10-26T12:00:00", "The decks of chapters 1, 2 and 3 meet the deck standard with overlap-free slides and a manifest without error-first examples, and the template 9.52.3 shows every story's text on the first screen; verified by the evidence bridge."),
    "Iter_25": ("Iteration 25: the story-layout repair of the pages of chapters 5 to 8, the deck of chapter 4 and the chapter 1 verify script (planned, not started)", "2026-10-26T12:00:00", "2026-10-27T12:00:00", "The pages of chapters 5 to 8 are rebuilt on the template 9.52.3 and pass the story layout at three viewports; the deck of chapter 4 meets the deck standard; the chapter 1 research has a verify script."),
    "Iter_26": ("Iteration 26: the pages of chapters 1 to 4 (planned, not started)", "2026-10-27T12:00:00", "2026-10-28T12:00:00", "The pages of chapters 1 to 4 are rebuilt on the template 9.52.3 with the chapter-code tab and meet the page standard."),
    "Iter_27": ("Iteration 27: the decks and pages of chapters 9 to 11 (planned, not started)", "2026-10-28T12:00:00", "2026-10-30T12:00:00", "The decks and pages of chapters 9, 10 and 11 meet the written standard."),
    "Iter_28": ("Iteration 28: the decks and pages of chapters 12 to 14 (planned, not started)", "2026-10-30T12:00:00", "2026-11-01T12:00:00", "The decks and pages of chapters 12, 13 and 14 meet the written standard."),
}
DECK_IT = {"01": "Iter_24", "02": "Iter_24", "03": "Iter_24", "04": "Iter_25", "09": "Iter_27", "10": "Iter_27", "11": "Iter_27", "12": "Iter_28", "13": "Iter_28", "14": "Iter_28"}
PAGE_IT = {"01": "Iter_26", "02": "Iter_26", "03": "Iter_26", "04": "Iter_26", "05": "Iter_25", "06": "Iter_25", "07": "Iter_25", "08": "Iter_25", "09": "Iter_27", "10": "Iter_27", "11": "Iter_27", "12": "Iter_28", "13": "Iter_28", "14": "Iter_28"}
F_BASE = ("MEASURED (the lineage agent's baseline, 2026-10-25, tool sen0401_lineage_baseline_v1_0_0.py, one log per run in 08-tooling/verify/iter24/baseline, committed before this change): "
          "DECKS: the deck standard check v1_1_0 gives 12 of 12 elements PASS for chapters 5 to 8 and 4 PASS, 8 FAIL (D1, D2, D3, D4, D5, D7, D10, D11) for every one of chapters 1 to 4 and 9 to 14; the deck overlap check v1_0_0 is clean on the decks of chapters 5 to 14 and reports overlaps (text over a picture, a table over text) on chapters 1 to 4. "
          "MANIFESTS: a chapter-code manifest exists for chapters 5 to 8 only (27, 18, 15 and 20 examples; the control check manifest:NN exits 0; no example's first output line starts with an error name) and for no other chapter. "
          "PAGES: the newest pages of chapters 5 to 8 declare the standard 9.52, have the chapter-code tab and pass the charset check; the newest pages of the other ten chapters have no chapter-code tab, no standard declaration and fail the charset check (tag behind byte 1024). "
          "STORY LAYOUT (the owner's rule, new tool sen0401_story_layout_probe_v1_0_0.py, 1366x768, 1400x900 and 390x844, logs in 08-tooling/verify/iter24/storylayout): the pages of chapters 5, 6, 7 and 8 FAIL it (a photograph as tall as the screen pushes the narrative below the first screen: 4 of 9, 3 of 12, 2 of 9 and 3 of 9 stories); the cause is the template 9.52.2 (.simgrow img with width 100 percent and height auto, no height cap). "
          "GATES: the Stage 4 gate runner v1_1_0 gives OVERALL PASS for all fourteen chapters; the Research chapter check v1_3_0 exits 0 for chapters 2 to 14 and CRASHES for chapter 1 (no file sen0401_ch01_verify_v*.py exists; the check names the verify script as a part). "
          "NOT MEASURED here: the page test 9.37.0 on the old pages (they lack the chapter-code tab, so P2 and P11 cannot pass) - the page test is run on every rebuilt page.")
STD_DECK = ("(1) the deck standard check v1_1_0 for chapter {c} reports every element D1 to D12 met, no NOT_MEASURED, exit 0; (2) the deck overlap check v1_0_0 exits 0 on the deck (no text over a picture, table or other text, none beyond the slide edge); "
            "(3) the chapter-code manifest 03-materials/ch{nn}/page/chapter_code_ch{nn}_v1_0_0.json exists, lists the deck's code examples in slide order by name, the deck control check v1_1_0 (manifest:{nn}) exits 0, and NO example's first output line starts with an error name (such as TypeError, ValueError, KeyError, Traceback): an example that teaches an error shows a first line that names what it does, then the error, because the page test 9.37.0 reads a first line that starts with an error name as a failed run; "
            "(4) the Deck chapter check v1_3_0 for Deck/Ch{nn} passes and the deck match check reports 0 not carried; (5) no committed file is edited, including the executor's own logs (each written once); results as printed; if any element fails the deck is named failing and this criterion has no passing result.")
STD_PAGE = ("(1) the charset check v1_0_0 exits 0 on the page (the tag below byte 1024, the first 1024 bytes decode as UTF-8); (2) the page test 9.37.0 runs all its features with no skip and passes them (exit 0), and the page tests 9.34.1 and 9.35.1 report no failure and widgets, features and gates not below the stored result of the page {old}, skipped not more; "
            "(3) the STORY LAYOUT probe sen0401_story_layout_probe_v1_0_0.py prints RESULT PASS: for EVERY story of the Stories tab, at 1366x768, 1400x900 and 390x844, the tallest photograph is shorter than the viewport and the story's narrative paragraph begins within the first screen; "
            "(4) the chapter-code tab equals the deck's chapter-code manifest in names and order and each example runs in the page and shows its result; (5) the Stage 4 gate runner v1_1_0 for {nn} exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, the Research, Deck and Page chapter checks pass, the deck match check reports 0 not carried; "
            "(6) the Stage 4 page ABox and the stored page-test result are new files; (7) no committed file is edited (an executor's own log is written once), no gate, test or threshold changed; results as printed; if any element fails the page is named failing and this criterion has no passing result.")
VER_D24 = ("deck standard check v1_1_0 (python-pptx 1.0.2); deck overlap check v1_0_0; deck control check v1_1_0 (manifest:NN); Deck chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; deck match check v1_0_0; baseline tool v1_0_0 (error-first scan of the manifest)")
VER_P24 = ("page template 9.52.3 (course_page_template_v9_52_3.html, built by ex:ST_Template_9523); page charset check v1_0_0; page builder v4_15_0 and page-data builder v2_24_0 (the template passed by PAGE_TEMPLATE); page tests 9.37.0, 9.34.1 and 9.35.1 (Playwright 1.56.0, serial, each under flock /tmp/page_test.lock); "
           "story layout probe v1_0_0; Stage 4 gate runner v1_1_0 reading the CURRENT RDODI validator v1.13.0; chapter check v1_3_0 reading the PINNED validator v1.6.0; deck match check v1_0_0; page ABox builder v2_1_0")
TOOLS_D = "ex:TS_DeckStdCheck11, ex:TS_DeckOverlapCheck, ex:TS_ChapterCheck, ex:TS_DeckMatch, ex:TS_RdodiValidatorPinned, ex:TS_Baseline24"
TOOLS_P = "ex:TS_PageTemplateF, ex:TS_PageCharsetCheck, ex:TS_PageBuilder415, ex:TS_PageData224, ex:TS_PageTest37, ex:TS_PageTest34b, ex:TS_PageTest35b, ex:TS_StoryLayoutProbe, ex:TS_Stage4Gates, ex:TS_ChapterCheck, ex:TS_DeckMatch, ex:TS_RdodiValidatorCurrent, ex:TS_RdodiValidatorPinned"
STORYRULE = ("STORY RULE (the owner's): the text of a story is visible without scrolling past a full-height photograph; check EVERY story at 1366x768, 1400x900 and 390x844 with the narrative starting within the first screen. "
             "The template 9.52.2 has no height cap on story photographs (.simgrow img{width:100%;height:auto}); the template 9.52.3 caps them.")


def ch(nn): return nn.lstrip("0")


def newdeck_note(nn):
    c = ch(nn); old = R.deckfile(nn)
    return ("Rebuild the deck of chapter %s as a NEW file (the newest deck is %s; it stays unchanged) with a new version number above the newest, from the chapter research 03-materials/ch%s/rdodi and the earlier deck's assets, to the deck standard. " % (c, old, nn)
            + "MEASURED today (baseline, 2026-10-25): the deck fails D1, D2, D3, D4, D5, D7, D10 and D11 of the deck standard check v1_1_0" + (" and the overlap check reports overlaps" if nn in ("01", "02", "03", "04") else "") + "; there is no chapter-code manifest. "
            + "The owner's words on the chapter 5 and 6 decks (quoted in ex:CR3_Remedy56) apply: a deck must be presentable and understandable. " + R.STD_D + " "
            + "Rules from the owner's standing teaching-material preferences: numbered slides, short sentences, explanation beside every code listing, the executed result shown as a visualization (native chart, table or drawn diagram) next to each listing, an everyday analogy for each key concept, 5N1K stories with real names, a real picture and a live link, native charts only, a resources slide with links, short speaker notes, one smooth colour scheme (the matching look of the page). "
            + "Follow the way the decks of chapters 5 to 8 were built (their generator files in 08-tooling/ch05-deck to ch08-deck are the pattern; write your own generator as a NEW tool file). "
            + "ALSO write the chapter-code manifest 03-materials/ch%s/page/chapter_code_ch%s_v1_0_0.json in the form of chapter_code_ch08_v1_0_0.json: the ordered list of the deck's code examples (order number = slide order, a short NAME, the code that runs in the page with the chapter library it needs, the expected result). Slide code is exactly one chapter-code page tab: the manifest equals the deck's code boxes. " % (nn, nn)
            + "NO example may have a first output line that starts with an error name (TypeError, ValueError, KeyError, Traceback ...): an example that teaches an error first prints a plain line, then the error is caught and printed after it. Run `python3 -B 08-tooling/sen0401_deck_control_check_v1_1_0.py manifest:%s`, the deck standard check v1_1_0 and the deck overlap check v1_0_0 on your deck and fix until they pass. " % nn
            + "The checker is the independent tools, not you: report every element as printed. " + R.NOEDIT + " " + R.COMMON)


def newpage_note(nn):
    c = ch(nn); old = R.pagefile(nn)
    kind = "relayout" if nn in URGENT else "retrofit"
    s = ("Build the page of chapter %s again as a NEW file with a page version above the newest page (%s) on the template 9.52.3 (course_page_template_v9_52_3.html, pass it with PAGE_TEMPLATE) with the page builder v4_15_0 and the page-data builder v2_24_0, " % (c, old)
         + ("from the chapter research, the deck's lecture export and stories (the deck stays as it is: it already meets the deck standard), and the deck's chapter-code manifest (state which file). " if nn in URGENT else
            "from the chapter research, the deck's lecture export and stories, and the deck's NEW chapter-code manifest chapter_code_ch%s_v1_0_0.json. " % nn)
         + "State how you passed the template and how the lecture export and stories were made (the pages of chapters 5 to 8 are the pattern: their build logs are in 08-tooling/ch05-page to ch08-page). "
         + "Run the page charset check (it must pass), the page tests 9.37.0, 9.34.1 and 9.35.1 (the runner with PAGE_TEST, serially, each under `flock /tmp/page_test.lock`), and the story layout probe `flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_story_layout_probe_v1_0_0.py %s <page version> <log>`; store the page-test result as a new test_results file, and build the Stage 4 page ABox with the page ABox builder v2_1_0. " % nn
         + STORYRULE + " " + R.STD_P + " " + R.DOMC + " ")
    if nn == "11": s += "ALSO keep the section-link ERD of the page of chapter 11 (the research relates every one of 16 sections to another; the ERD labels must run without a skip in the page tests 9.34.1 and 9.35.1; carried from the withdrawn story ST_Section_Links_Ch11). "
    if nn == "01": s += "The Research chapter check for Research/Ch01 crashes today because the file sen0401_ch01_verify_v*.py does not exist: that file is made by the task TK_Ch01_VerifyScript_Build, which this task depends on; run the Research chapter check once it exists. "
    return s + R.NOEDIT + " " + R.COMMON


def verify_deck_note(nn):
    return ("Run, from the evidence bridge and as printed: the deck standard check v1_1_0 for chapter %s, the deck overlap check v1_0_0, `sen0401_deck_control_check_v1_1_0.py manifest:%s`, the scan of the manifest for an example whose first output line starts with an error name (sen0401_lineage_baseline_v1_0_0.py %s), "
            "the Deck chapter check v1_3_0 for Deck/Ch%s, the deck match check, and `nochange` (no committed file edited); read the deck slide by slide (the three roles of the owner's preference: teaching academician, reviewing faculty specialist, student; recorded as a reading, not as a tool result)." % (ch(nn), nn, "<outdir> " + nn, nn))


def verify_page_note(nn):
    return ("Re-run serially, each browser run under `flock /tmp/page_test.lock`: the charset check, the page tests 9.37.0, 9.34.1 and 9.35.1, the story layout probe v1_0_0 at 1366x768, 1400x900 and 390x844 on EVERY story, the Stage 4 gate runner v1_1_0 for %s, the Research, Deck and Page chapter checks, the deck match check and the manifest equality (the chapter-code tab equals the deck's code order); "
            "check that the stored result and the Stage 4 ABox are new files and that no committed file is edited; record every result as printed." % nn)


TXT_TEMPLATE = ("Make the NEW file course_page_template_v9_52_3.html (the folder of course_page_template_v9_52_2.html, which stays byte-identical: SHA-256 before and after) from the template 9.52.2. The ONLY change is the layout of the Stories tab: a story photograph is capped in height so that the story's narrative begins within the first screen at every viewport (for example max-height as a share of the viewport height with object-fit cover, narrower photographs side by side or beside the text on wide screens, a smaller cap on phones); zoom of a photograph and its caption stay. "
                "Every other rule, class, attribute, DOM contract entry and the text-size control are unchanged. " + STORYRULE + " "
                "PROOF to deliver and keep as logs: (a) the unified diff against 9.52.2, limited to the story rules; (b) SHA-256 of 9.52.2 before and after; (c) scratch pages of chapters 5, 6, 7 and 8 built from their present data with the page builder v4_15_0 and PAGE_TEMPLATE=9.52.3 into a scratch folder (not shipped, not committed) and the story layout probe on each: `flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_story_layout_probe_v1_0_0.py NN <page version> <log>` prints RESULT PASS for every story at all three viewports; "
                "(d) REGRESSION (carried from the withdrawn criterion AC8R_Regress, restated on 9.52.3, not waived): the page tests 9.37.0, 9.34.1 and 9.35.1 on the scratch page of chapter 5, and the page tests 9.34.1 and 9.35.1 on scratch pages of chapters 1 and 10 built from the same template, each give the stored result of the shipped page of that chapter or better (serial, under the lock, every run kept as a log; the scratch pages are not shipped); (e) no committed file is edited. " + R.NOEDIT + " " + R.COMMON)
TXT_TEMPLATE_V = ("Re-run on the bridge, serially under the lock: SHA-256 of 9.52.2 unchanged; the diff limited to the story rules; the story layout probe on the scratch pages of chapters 5 to 8 (the builder builds them again from the committed template and data); the page tests on the scratch page of chapter 5; nochange; record every result as printed.")
TXT_VERIFY_SCRIPT = ("Make the NEW file 08-tooling/sen0401_ch01_verify_v1_0_0.py, the verify script of the chapter 1 research, in the form of sen0401_ch02_verify_v1_0_0.py: the Research chapter check v1_3_0 names it as a part ('verify script') and CRASHES for chapter 1 today with TypeError: expected str, bytes or os.PathLike object, not NoneType, because no file sen0401_ch01_verify_v*.py exists (the chapter check is NOT edited). "
                     "The script checks the claims of the chapter 1 research that can be executed (the numbers and examples of the chapter's rdodi claims) and exits 0 when they hold. PROOF: `venv314/bin/python -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Research/Ch01` exits 0 with the verify part PASS; the Research chapter checks of chapters 2 to 14 give the same results as before. " + R.NOEDIT + " " + R.COMMON)


def ac_deck(nn):
    c = ch(nn)
    return ("Owner-directed work (" + CR + ", " + WHEN + "). Given the newest deck of chapter %s (%s, unchanged) and its research, when the deck is rebuilt as a new file (a version above the newest) with its chapter-code manifest, then ALL of: " % (c, R.deckfile(nn))
            + STD_DECK.format(c=c, nn=nn) + " " + F_BASE + " " + R.STD_D)


def ac_page(nn):
    c = ch(nn); old = R.pagefile(nn); ov = R.vdot(R.pagever(nn))
    return ("Owner-directed work (" + CR + ", " + WHEN + "). Given the deck of chapter %s with its chapter-code manifest and the newest page of chapter %s (%s, unchanged), when the page is rebuilt as a new file with a page version above %s on the template 9.52.3 with the builders v4_15_0 and v2_24_0, then ALL of: " % (c, c, old, ov)
            + STD_PAGE.format(old=ov, nn=nn) + " " + F_BASE + " " + STORYRULE + " " + R.STD_P)


AC_TEMPLATE = ("Owner-directed work (" + CR + ", " + WHEN + "). Given the template 9.52.2 and the pages of chapters 5 to 8, when the NEW template 9.52.3 is made, then ALL of: (1) 9.52.2 is byte-identical (SHA-256 before and after); (2) the diff against 9.52.2 is limited to the rules of the Stories tab; (3) scratch pages of chapters 5, 6, 7 and 8 built from the present page data with the page builder v4_15_0 and PAGE_TEMPLATE=9.52.3 pass the story layout probe v1_0_0 (RESULT PASS, every story at 1366x768, 1400x900 and 390x844); "
               "(4) REGRESSION (carried from the withdrawn criterion AC8R_Regress of ST_Remedy_Regress_R, restated on 9.52.3, not waived): the page tests 9.37.0, 9.34.1 and 9.35.1 on the scratch page of chapter 5, and the page tests 9.34.1 and 9.35.1 on scratch pages of chapters 1 and 10 built from 9.52.3, each give the stored result of the shipped page of that chapter or better (equal or beat, as the regression criterion required); (5) no committed file is edited; results as printed; if any element fails the template is named failing. " + F_BASE + " " + STORYRULE)
AC_VSCRIPT = ("Owner-directed work (" + CR + ", " + WHEN + "). Given the Research chapter check v1_3_0 (unchanged), when the NEW file sen0401_ch01_verify_v1_0_0.py is made, then ALL of: (1) the Research chapter check for Research/Ch01 exits 0 with its verify-script part PASS (it crashes today); (2) the chapter checks Research/Ch02 to Ch14 give the same results as in the baseline; (3) no committed file is edited. " + F_BASE)


def txt_tasks():
    """(task id, title, type, deps, session, est, hours, note, iteration)"""
    L = []
    for nn in ["01", "02", "03", "04", "09", "10", "11", "12", "13", "14"]:
        c = ch(nn); it = DECK_IT[nn]; sess = "SEN0401-%s-deck-ch%s" % (it.replace("Iter_", "I"), nn)
        L.append(("TK_Ch%s_Deck_Build_R24" % nn, "Rebuild the deck of chapter %s to the deck standard with its chapter-code manifest" % c, "Build", [], sess, "S", 1.5, newdeck_note(nn), it))
        L.append(("TK_Ch%s_Deck_Verify_R24" % nn, "Verify the deck of chapter %s against the deck standard" % c, "Verify", ["TK_Ch%s_Deck_Build_R24" % nn], "builder", "S+1.5h", 0.5, verify_deck_note(nn), it))
    L.append(("TK_Template_9523_Build", "Make the page template 9.52.3 with the story photographs capped", "Build", [], "SEN0401-I24-template", "S", 1.5, TXT_TEMPLATE, "Iter_24"))
    L.append(("TK_Template_9523_Verify", "Verify the page template 9.52.3 on the bridge", "Verify", ["TK_Template_9523_Build"], "builder", "S+1.5h", 1.0, TXT_TEMPLATE_V, "Iter_24"))
    L.append(("TK_Ch01_VerifyScript_Build", "Make the verify script of the chapter 1 research", "Build", [], "SEN0401-I25-verify-ch01", "S", 1.0, TXT_VERIFY_SCRIPT, "Iter_25"))
    L.append(("TK_Ch01_VerifyScript_Verify", "Verify the chapter 1 verify script and the Research chapter check", "Verify", ["TK_Ch01_VerifyScript_Build"], "builder", "S+1.0h", 0.5, "Run the Research chapter check v1_3_0 for Research/Ch01 and for chapters 2 to 14 (venv314) and compare with the baseline; nochange; record every result as printed.", "Iter_25"))
    for nn in URGENT + DECKS:
        c = ch(nn); it = PAGE_IT[nn]; sess = "SEN0401-%s-page-ch%s" % (it.replace("Iter_", "I"), nn)
        deps = ["TK_Template_9523_Verify"] + (["TK_Ch%s_Deck_Verify_R24" % nn] if nn in DECKS else [])
        if nn == "01": deps.append("TK_Ch01_VerifyScript_Verify")
        L.append(("TK_Ch%s_Page_Build_R24" % nn, ("Rebuild the page of chapter %s on template 9.52.3 with the story layout repaired" if nn in URGENT else "Rebuild the page of chapter %s on template 9.52.3 with the chapter-code tab") % c, "Build", deps, sess, "S", 1.5, newpage_note(nn), it))
        L.append(("TK_Ch%s_Page_Verify_R24" % nn, "Verify the rebuilt page of chapter %s" % c, "Verify", ["TK_Ch%s_Page_Build_R24" % nn], "builder", "S+1.5h", 1.0, verify_page_note(nn), it))
    return L


def stories():
    S = []   # (sid, title, deliverable, objective, criteria, tasks, iteration)
    for nn in DECKS:
        c = ch(nn)
        S.append(("ST_Ch%s_Deck_R24" % nn, "The deck of chapter %s meets the deck standard and carries its chapter-code manifest" % c, "Del3_Retro24", "Obj3_Retro24", ["AC9_Deck_Ch%s" % nn], ["TK_Ch%s_Deck_Build_R24" % nn, "TK_Ch%s_Deck_Verify_R24" % nn], DECK_IT[nn]))
    S.append(("ST_Template_9523", "The page template 9.52.3 shows every story's text on the first screen", "Del3_Retro24", "Obj3_Retro24", ["AC9_Template"], ["TK_Template_9523_Build", "TK_Template_9523_Verify"], "Iter_24"))
    S.append(("ST_Ch01_VerifyScript", "The chapter 1 research has a verify script and its Research chapter check runs", "Del3_Retro24", "Obj3_Retro24", ["AC9_VerifyScript"], ["TK_Ch01_VerifyScript_Build", "TK_Ch01_VerifyScript_Verify"], "Iter_25"))
    for nn in URGENT + DECKS:
        c = ch(nn)
        S.append(("ST_Ch%s_Page_R24" % nn, ("The page of chapter %s shows every story's text on the first screen on the template 9.52.3" if nn in URGENT else "The page of chapter %s is rebuilt on template 9.52.3 and meets the page standard with the story layout") % c, "Del3_Retro24", "Obj3_Retro24", ["AC9_Page_Ch%s" % nn], ["TK_Ch%s_Page_Build_R24" % nn, "TK_Ch%s_Page_Verify_R24" % nn], PAGE_IT[nn]))
    return S


def criteria():
    C = {}
    for nn in DECKS:
        C["AC9_Deck_Ch%s" % nn] = ("The deck of chapter %s meets the deck standard D1 to D12, overlap-free, with a chapter-code manifest without error-first examples" % ch(nn), ac_deck(nn), TOOLS_D, VER_D24)
    for nn in URGENT + DECKS:
        C["AC9_Page_Ch%s" % nn] = ("The page of chapter %s on template 9.52.3 passes the page tests 9.37.0, 9.34.1 and 9.35.1 and the story layout at three viewports, with its character set first" % ch(nn), ac_page(nn), TOOLS_P, VER_P24)
    C["AC9_Template"] = ("The template 9.52.3 passes the story layout probe on the pages of chapters 5 to 8 and changes nothing else", AC_TEMPLATE, "ex:TS_PageBuilder415, ex:TS_PageData224, ex:TS_PageTest37, ex:TS_PageTest34b, ex:TS_PageTest35b, ex:TS_StoryLayoutProbe", VER_P24)
    C["AC9_VerifyScript"] = ("The chapter 1 research has a verify script and the Research chapter check for chapter 1 exits 0", AC_VSCRIPT, "ex:TS_ChapterCheck, ex:TS_RdodiValidatorPinned", "Research chapter check v1_3_0 (venv314) reading the PINNED RDODI validator v1.6.0")
    return C


def ac_block(aid, label, gh, tools, ver, k):
    return ('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
            '    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC9_%s_Passes, ex:TC9_%s_NotClaimed .\n') % (aid, lit(label), lit(gh), tools, lit(ver), k, k)


def case_blocks(k, aid):
    return '''ex:TC9_%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the checks of the criterion"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Spec3I_Retro24_Pass ; backlog:runsOnData ex:Data3S_TC9_%(k)s_Passing ;
    backlog:hasCaseText "Run the checks of the criterion; they report no failure and exit 0." .
ex:TC9_%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on the finding that fails and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Spec3I_Retro24_Fail ; backlog:runsOnData ex:Data3S_TC9_%(k)s_Failing ;
    backlog:hasCaseText "Run the checks on the item as measured in the baseline of 2026-10-25 (an overlap, a manifest example that starts with an error name, a story whose text lies below the first screen, a committed file with status M) and require that nothing is claimed for it." .
ex:Data3S_TC9_%(k)s_Passing a backlog:TestData ; rdfs:label "The new files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The new files of the task, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3S_TC9_%(k)s_Failing a backlog:TestData ; rdfs:label "The finding that fails the checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The finding as measured in the baseline of 2026-10-25 (ex:IA3_Retro24)." .
''' % dict(k=k, a=aid)


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Retrofit of all chapters on the measured state: restated criteria, the story-layout repair of chapters 5 to 8, the template 9.52.3, the chapter 1 verify script, planned in five iterations"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR3_Retrofit, ex:CR3_Repair21 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit("Requested " + WHEN + ". " + F_BASE + " The criteria of the retrofit stories of Iteration 21 (ex:AC7_Deck_ChNN, ex:AC7_Page_ChNN) name the page test 9.36.0 and the template 9.52.2 and lack the rules the owner added since: no text overlap in a deck, no manifest example that starts with an error name, the story text on the first screen at three viewports, the page ABox as a new file. "
                "A rule added after a story is written does not reach into it (G133), so the repair is new work by the change route. The change grows the scope by one deliverable (the restated criteria, the template 9.52.3, the story-layout repair of the pages of chapters 5 to 8, the chapter 1 verify script); nothing existing is edited. Pending until the ScopeChange that admits the stories is recorded in the Backlog version."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the retrofit costs on the measured state, and in what order it runs"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_Retrofit ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(F_BASE + " AFFECTED: the 20 retrofit stories and 40 tasks of Iteration 21 and ST_Section_Links_Ch11 with its Verify task (withdrawn in the version after the replacements exist; none started, none Done); the Done pages of chapters 5 to 8 stay Done and are not edited (G125): their story-layout defect is repaired by new stories on new page files. NOT AFFECTED: every committed file; the tools; the Mission outcome. "
                    "PLAN (route as ex:CR3_Repair21, G127): a StageRevision from the Scope stage, seven versions; one version for the withdrawals, one for the ranking (BP-D10), one for work begun. ORDER (the owner's: chapter 1 first; repairs re-rank, G147): the template 9.52.3 gates every page, so it runs first with the decks of chapters 1 to 3 (three executors at once): "
                    "Iter_24 decks 1, 2, 3 and the template; Iter_25 the story-layout repair of the pages 5 to 8, the deck of chapter 4 and the chapter 1 verify script; Iter_26 the pages 1 to 4; Iter_27 chapters 9 to 11; Iter_28 chapters 12 to 14. Iterations 25 to 28 are planned, not started (their ceremonies are held when each starts). "
                    "ESTIMATES (not measurements, G120): deck 1.5 h build plus 0.5 h verify, page 1.5 h plus 1.0 h, template 1.5 h plus 1.0 h, verify script 1.0 h plus 0.5 h; browser runs about 9 minutes each, serial under the lock on two cores; at most three executors at once. COST: new files only; a failing criterion is named failing; nothing is waived."))
    return t + cr + ia, "ChangeRequest %s (Pending) with its ImpactAssessment: the retrofit of all chapters planned on the measured state of 2026-10-25 (restated criteria, story-layout repair, template 9.52.3, chapter 1 verify script)." % CR


def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable; the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its impact assessment " + IA + " were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated. The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the retrofit of all chapters on the measured state"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the retrofit of all chapters: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The decks and pages of the fourteen chapters restated on the measured standard, the template 9.52.3 with the story layout, the story-layout repair of the pages of chapters 5 to 8, and the chapter 1 verify script"
    tx = ("The decks of chapters 1 to 4 and 9 to 14 as new files meeting the deck standard with no overlap and a manifest without error-first examples; the pages of all fourteen chapters as new files on the template 9.52.3 (a new file; 9.52.2 stays) meeting the page standard with the story layout at three viewports; the verify script of the chapter 1 research. " + F_BASE)
    L = ('\nex:Del3_Retro24 a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n'
         '    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Retro24 ; rdfs:seeAlso %s, %s .\n" % (CR, IA)
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the retrofit on the measured standard). No exclusion changes: new files only; the exclusion of changes to gates, tests and thresholds still holds (9.52.3 and the probe are new files)." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR12", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the retrofit of all chapters: one deliverable in the existing area."


def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR12", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Retro24 a backlog:Goal ;
    rdfs:label "Every chapter's deck and page meet the written teaching-material standard, including the story layout, on verified evidence"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Must ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR12 .
ex:G3_Retro24 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request %s; the intent origin is therefore Derived."@en .
ex:Spec3I_Retro24 a backlog:Specification ;
    rdfs:label "What it is for a retrofitted chapter to meet the standard"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Retro24 ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR12 .
ex:Spec3I_Retro24_Pass a backlog:TestScenario ; rdfs:label "A deck or page built as new files passes its criterion"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Retro24 ; backlog:hasScenarioText %s .
ex:Spec3I_Retro24_Fail a backlog:TestScenario ; rdfs:label "A deck with an overlap, a manifest example that starts with an error name, a page whose story text lies below the first screen, or a committed file edited is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Retro24 ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request " + CR + ": the owner ordered a return to all chapters from chapter 1. " + F_BASE),
       CR, lit("A chapter meets the standard when every element of the criteria of its deck and its page is measured on the evidence bridge as met, the output files are new, and no committed file is edited. " + STORYRULE),
       lit("Given the deck or the page of a chapter built as new files, when the checks of its criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a deck whose slides overlap, a manifest whose example starts with an error name, a page whose story narrative begins below the first screen, or a task that edits a committed file, when the checks are run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR12", "Out3_ScopeR12"), "third lineage, Goal stage rebuilt for the retrofit of all chapters: one goal with a specification and two scenarios."


def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR12", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Retro24 a backlog:Objective ; rdfs:label "Chapters of the fourteen whose deck and page meet the standard including the story layout: from 0 to 14"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Retro24 ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Retro24 ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "14"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Retro24 ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR12 .
ex:Met3_Retro24 a backlog:Metric ; rdfs:label "chapters whose deck story and page story are Done on bridge-verified evidence under the restated criteria"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Retro24 a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after each iteration is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria of the iteration, so the count is read from verified runs." ; backlog:expectedValue "14"^^xsd:decimal .
ex:ObsR24_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Retro24 ; backlog:observationFor ex:Obj3_Retro24 ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Retro24 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request %s; the intent origin is therefore Derived."@en .
''' % (lit("Count of the chapters (of the fourteen) whose deck story and page story under the restated criteria are Done on bridge-verified evidence: deck standard check D1-D12, overlap check, manifest, page tests 9.37.0/9.34.1/9.35.1, story layout probe, Stage 4 gates, chapter checks."), now,
       lit("Baseline from the measurement of 2026-10-25 (08-tooling/verify/iter24/baseline and storylayout): no chapter meets all elements - chapters 5 to 8 fail the story layout, the other ten fail the deck standard and the page standard - so 0 of 14."), CR)
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR12", "Out3_GoalR12"), "third lineage, Objective stage rebuilt for the retrofit: one objective (0 to 14) with metric, checkpoint and baseline reading."


def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR12", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR13"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []
    tools = ('\nex:TS_DeckOverlapCheck a backlog:ToolScript ; rdfs:label "deck overlap check v1_0_0 (text over a picture, table or other text; spill beyond the slide edge)"@en ; backlog:scriptFileName "deck_overlap_check_v1_0_0.py" ; backlog:acceptsGraphPath false .\n'
             'ex:TS_StoryLayoutProbe a backlog:ToolScript ; rdfs:label "story layout probe v1_0_0 (every story at 1366x768, 1400x900 and 390x844: the tallest photograph shorter than the viewport, the narrative begins in the first screen)"@en ; backlog:scriptFileName "sen0401_story_layout_probe_v1_0_0.py" ; backlog:acceptsGraphPath false .\n'
             'ex:TS_Baseline24 a backlog:ToolScript ; rdfs:label "baseline measurement v1_0_0 (the committed checks per chapter 1 to 14 and the scan of the manifests for error-first examples)"@en ; backlog:scriptFileName "sen0401_lineage_baseline_v1_0_0.py" ; backlog:acceptsGraphPath false .\n'
             'ex:TS_PageTemplateF a backlog:ToolScript ; rdfs:label "page template 9.52.3 (new file over 9.52.2: the story photographs capped; made by ST_Template_9523)"@en ; backlog:scriptFileName "course_page_template_v9_52_3.html" ; backlog:acceptsGraphPath false .\n')
    L.append(tools)
    C = criteria()
    for aid, (label, gh, tl, ver) in C.items():
        L.append(ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(case_blocks(aid[4:], aid))
    ST = stories(); TS = txt_tasks()
    note = "Restated " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment " + IA + "."
    state_of = {}
    for sid, title, deliv, obj, crits, tks, it in ST:
        L.append(R.story_block(sid, title, deliv, obj, crits, tks, note, "ex:" + it, "Ready" if it == "Iter_24" else "Proposed")); state_of[sid] = it
    for tid, title, ttype, deps, sess, est, hrs, nt, it in TS:
        ready = (it == "Iter_24" and ttype == "Build" and not deps)
        L.append(R.task_block(tid, title, ttype, deps, sess, est, hrs, nt, "ex:" + it, "Ready" if ready else "Proposed", True))
    L.append("ex:ST_Template_9523 backlog:standsAlone true .\n")
    refine = [s[0] for s in ST if s[6] == "Iter_24"] + [x[0] for x in TS if x[8] == "Iter_24"]
    for x in refine:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_24 ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, lit("Refined by the lineage agent from the change request %s and the measured facts of %s: acceptance criterion with tools and versions, dependencies, estimated start, and a brief to be generated; startable when its dependencies are Done." % (CR, IA))))
    for sid, title, deliv, obj, crits, tks, it in ST:
        if it != "Iter_24": continue
        L.append('ex:Plan3S_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 24"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_24 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Retro24, ex:Spec3I_Retro24_Pass, ex:Spec3I_Retro24_Fail .\n' % (sid, sid, now, sid, ", ".join("ex:" + x for x in tks)))
    L.append("ex:Obj3_Retro24 backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in ST))
    for itid, (lab, st, en, goal) in ITERS.items():
        mem = [s[0] for s in ST if s[6] == itid] + [x[0] for x in TS if x[8] == itid]
        start = now if st is None else st
        dur = ("Proposed by the lineage agent on 2026-10-25: the start is the instant of the planning ceremony ex:PC3_Iter_24; the proposed end is %s UTC. Estimates, not measurements: deck 1.5 h build plus 0.5 h verification, template 1.5 h plus 1.0 h; three executors at once; every browser run serialised by the lock." % en) if st is None else \
              ("Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (start, en))
        sg = goal + (" Frozen at the planning ceremony." if st is None else " PLANNED, not started: no ceremony is held, no executor is briefed.")
        L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, start, en, lit(dur), lit(sg), ", ".join("ex:" + x for x in mem)))
    L.append('ex:PB3S_Iter_24 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 24 when it was planned"@en ; backlog:baselineFor ex:Iter_24 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (now, now, ITERS["Iter_24"][2]))
    i24 = [s[0] for s in ST if s[6] == "Iter_24"]
    L.append('ex:PC3_Iter_24 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 24: the decks of chapters 1 to 3 and the template 9.52.3"@en ; backlog:ceremonyFor ex:Iter_24 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (now, ", ".join("ex:Plan3S_" + s for s in i24), lit("Held %s by the lineage agent after the change request %s: four stories and eight tasks are committed to this iteration, whose goal is frozen at its start. No executor has started in it; work begun is recorded at the real start of each executor session, with its brief. Iterations 25 to 28 are planned, not started." % (now, CR))))
    L.append('ex:SC3_Retro24 a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the retrofit of all chapters on the measured standard"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in ST), lit("Decided by the owner through his standing orders (retrofit all chapters starting with chapter 1; repairs re-rank; never wait on unrelated questions), which the lineage agent applied (" + WHEN + "). The decider recorded is the Owner because the orders are his decision; the lineage agent did the recording. The boundary moved outward by %d stories; new files only; nothing existing is edited or weakened." % len(ST))))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Retro24 and the stories it admits; it was Pending before. Decided by the lineage under the owner standing orders; the coordinator tells the owner afterwards."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR14", "Out3_ObjectiveR12"), "third lineage, Backlog stage rebuilt for the retrofit of all chapters: Iteration 24 (4 stories, 8 tasks, planned) and Iterations 25 to 28 (planned, not started), %d stories with restated criteria, the ScopeChange; the change request Accepted; the %d carried items are re-admitted, not re-dated." % (len(ST), n)


def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete and no work is begun." % (NEWB, prev)


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__": main()
