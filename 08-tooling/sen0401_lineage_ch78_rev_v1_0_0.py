#!/usr/bin/env python3
"""sen0401_lineage_ch78_rev v1_0_0 - change route (rulings G113, G120, G125, G127, G129, G133, G136) for the owner's decision of Friday 2026-10-23 16:06 Istanbul (relayed by the course coordinator): chapters 6, 7 and 8 are urgent;
chapters 7 and 8 need a deck, a chapter-code manifest and a page on the current standard (template 9.52.2, character set first); after these the chapters 1 to 14 are retrofitted in order (manifest, deck match, page with chapter-code tab and panels, character set), planned now, not started.
Same route as ex:CR3_Charset (sen0401_lineage_charset_rev): a ChangeRequest with an ImpactAssessment, a StageRevision from the Scope stage (G127), the Scope, Goal, Objective and Backlog outputs rebuilt one per version, a last version fills the last commit.
New items: Iteration 20 (urgent: chapters 7 and 8; a new deck standard check version; five stories, ten tasks) and Iteration 21 (planned retrofit of chapters 1 to 4 and 9 to 14; twenty stories, forty tasks, Proposed, no executor briefed).
Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV    (one call = one new file = one event; the caller validates and commits each alone)"""
__version__ = "1.0.0"
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_remedy56_rev_v1_0_0 as RV
lit, esc = G.lit, M.esc
IT1 = "ex:Iter_20"; IT2 = "ex:Iter_21"; REV = "ex:Revision_Lineage3_Scope8"; CR = "ex:CR3_Ch78"; IA = "ex:IA3_Ch78"; CRR = "ex:CR3_Retrofit"; IAR = "ex:IA3_Retrofit"
ACTIVE = ["ex:Out3_ScopeR8", "ex:Out3_GoalR8", "ex:Out3_ObjectiveR8", "ex:Out3_BacklogR10"]; NEWB = "ex:Out3_BacklogR11"
WHEN = "Friday 2026-10-23 16:06 Istanbul, relayed by the course coordinator (the owner's decision)"
END1 = "2026-10-24T09:00:00"; START2 = "2026-10-24T09:00:00"; END2 = "2026-10-26T09:00:00"
URGENT = ["07", "08"]; RETRO = ["01", "02", "03", "04", "09", "10", "11", "12", "13", "14"]
COMMON, STD_D, STD_P, DOMC = RV.COMMON, RV.STD_D, RV.STD_P, RV.DOMC
NOEDIT = ("DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES: write each log once, after its run is complete, and commit it once (the control of the page 9.82.0 of chapter 5 found a log file of the executor appended in a later commit and named that element not met).")
FACT = ("MEASURED FACTS (2026-10-23, by the builder session with the committed tools). Decks: the deck standard check v1_0_0 on the newest decks gives PASS=12 for chapters 5 and 6 and FAIL for every other chapter: chapters 1 to 4 fail D1, D2, D3, D4, D5, D7, D10, D11 (PASS=4); chapter 7 (26 slides, 14 code slides) fails the same eight (D1 25 of 26 numbered, D2 longest box 45 words, D3 3 of 14 code slides complete, D4 0 of 87 key concepts with an analogy, D5 0 of 3 stories complete, D7 longest note 100 words, D10 0 of 5 dividers complete, D11 32 of 87 research concepts shown = 36.8 percent); "
        "chapter 8 (26 slides, 16 code slides) and chapters 9 to 14 fail D1, D2, D3, D5, D7, D10 and the check returns NOT_MEASURED for D4 and D11 because their research files declare the key concepts as sen0414:PrimarySourceConcept while the check reads sen0401:PrimarySourceConcept (a skip is not a pass). "
        "Manifests: only chapters 5 and 6 have a chapter-code manifest. Pages: the charset check v1_0_0 passes the newest pages of chapters 5 and 6 (tag at byte 37) and fails the newest page of every other chapter (tag at byte 11172, or 11888 for chapter 10); the pages of chapters 7 and 8 (9.76.0, 9.77.0) are built on template 9.51.0 and have no chapter-code tab. Research, a deck and a page exist for all fourteen chapters; no chapter is unbuilt.")

def ch(nn): return nn.lstrip("0")
def vkey(p): return [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
def newest(pat):
    fs = sorted(glob.glob(os.path.join(M.REPO, pat)), key=vkey); return os.path.relpath(fs[-1], M.REPO) if fs else None
def deckfile(nn): return newest("03-materials/ch%s/*.pptx" % nn)
def pagefile(nn): return newest("03-materials/ch%s/page/sen0401_ch%s_page_v*.html" % (nn, nn))
def pagever(nn): return re.search(r"_v(\d+_\d+_\d+)\.html", pagefile(nn)).group(1)
def vdot(v): return v.replace("_", ".")
DECKV = {"07": "v2_0_0", "08": "v2_0_0"}                       # the new deck version of the urgent chapters (the old ones: 1.3.0 and 1.1.0)
PAGEV = {"07": "9_84_0", "08": "9_85_0"}                       # the new page version of the urgent chapters
def checkver(nn): return "v1_1_0" if nn in ("08", "09", "10", "11", "12", "13", "14") else "v1_0_0"
def checkdesc(nn): return ("the deck standard check v1_1_0 (a new tool made by TK_Ch78_DeckCheck: it reads the key concepts of the research whichever way they are declared)" if checkver(nn) == "v1_1_0" else "the deck standard check v1_0_0")
VER_D = ("deck standard check v1_0_0 (python-pptx 1.0.2) and, for chapters 8 to 14, its new version v1_1_0; Deck chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; deck match check v1_0_0; deck control check v1_1_0 (the manifest equals the deck's code slides); python-pptx 1.0.2")
VER_P = ("page template 9.52.2 (course_page_template_v9_52_2.html, built and controlled in Iteration 19); page charset check v1_0_0; page builder v4_15_0 and page-data builder v2_24_0 (unchanged; the template is passed by PAGE_TEMPLATE); page test 9.36.0 (Playwright 1.56.0); page tests 9.34.1 and 9.35.1; "
         "Stage 4 gate runner v1_1_0 reading the CURRENT RDODI validator v1.13.0; chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; deck match check v1_0_0; page check wrapper v1_5_0; Playwright 1.56.0")

# ---------------------------------------------------------------- the items
def deck_note(nn, planned):
    c = ch(nn); old = deckfile(nn); new = ("sen0401 chapter %s deck, new version (see the criterion)" % c)
    nv = DECKV.get(nn, "a new version above the newest")
    return ("Rebuild the deck of chapter %s as a NEW file (the newest deck is %s; it stays unchanged) with a new version number (%s) from the chapter research 03-materials/ch%s/rdodi and the earlier deck's assets, to the deck standard. " % (c, old, nv, nn) + FACT[:0] +
            "The owner's words on the chapter 5 and 6 decks (quoted in ex:CR3_Remedy56) apply: a deck must be presentable and understandable. " + STD_D + " "
            "Rules from the owner's standing teaching-material preferences: full sentences are fine but no long paragraphs; explanation beside every code listing; the executed result shown as a visualization (native chart, table or drawn diagram) next to each listing; an everyday analogy for each key concept; 5N1K stories with real names, a real picture and a live link; native charts only; numbered slides; a resources slide with links for further reading and watching; short speaker notes; a smooth colour scheme. "
            "Follow the way the decks of chapters 5 and 6 were built (their generator files in 08-tooling/ch05-deck and ch06-deck are the pattern; write your own generator as a NEW tool file). "
            "ALSO write the chapter-code manifest 03-materials/ch%s/page/chapter_code_ch%s_v1_0_0.json in the form of chapter_code_ch06_v1_1_0.json: the ordered list of the deck's code examples (order number = slide order, a short NAME, the code that runs in the page with the chapter library it needs, the expected result), because the page tab must list the same examples in the same order. "
            "The checker is the independent %s, not you: run it when it exists and report every element as printed. " % (nn, nn, checkdesc(nn)) + NOEDIT + " " + COMMON)
def page_note(nn):
    c = ch(nn); pv = PAGEV.get(nn)
    return ("Build the page of chapter %s again as a NEW file with the new page version %s on the template 9.52.2 (course_page_template_v9_52_2.html, pass it with PAGE_TEMPLATE) with the page builder v4_15_0 and the page-data builder v2_24_0, from the chapter research, the deck's lecture export and stories, and the deck's NEW chapter-code manifest chapter_code_ch%s_v1_0_0.json "
            "(state how you passed the template and how the lecture export and stories were made; the pages of chapters 5 and 6 are the pattern: their build logs are in 08-tooling/ch05-page and ch06-page). Run the page charset check on the page (it must pass), run the page tests 9.36.0, 9.34.1 and 9.35.1 (the runner with PAGE_TEST), serially, store the result as a new test_results file, and build the Stage 4 page ABox with the Stage 4 builder. " % (c, vdot(pv) if pv else "above the newest page " + vdot(pagever(nn)), nn) +
            STD_P + " " + DOMC + " " + NOEDIT + " " + COMMON)
def mk_tasks():
    T_ = []
    T_.append(("TK_Ch78_DeckCheck", "Make the deck standard check v1_1_0: read the research key concepts of chapters 8 to 14", "Build", [], "SEN0401-I20-deckcheck", "T0", 0.5,
        "Write the NEW file 08-tooling/sen0401_deck_standard_check_v1_1_0.py from sen0401_deck_standard_check_v1_0_0.py (which stays byte-identical): the only change is that the key concepts of the chapter research are read both when they are declared as sen0401:PrimarySourceConcept and when they are declared as sen0414:PrimarySourceConcept (the research files of chapters 8 to 14 use the second); every other element, threshold and message is unchanged. "
        "THE DEFECT, measured 2026-10-23: the v1_0_0 check returns NOT_MEASURED for D4 (analogy per key concept) and D11 (coverage) on chapters 8 to 14 with 'no research concept list found', because it matches the class sen0401:PrimarySourceConcept and finds none in those files (chapter 8: 46 concepts under sen0414:, chapter 9: 38, 10: 62, 11: 43, 12: 43, 13: 29, 14: 69). A skip is not a pass, so no deck of those chapters can be shown to meet the standard without this change. "
        "PROOF to deliver and keep as logs: (a) the unified diff against v1_0_0; (b) SHA-256 of v1_0_0 before and after; (c) v1_1_0 gives, on chapters 5, 6 and 7, the same PASS/FAIL and the same measured numbers as v1_0_0 for every element; (d) on chapters 8 to 14 D4 and D11 are now measured (a number, PASS or FAIL) instead of NOT_MEASURED, with the concept count per chapter as stated above. " + NOEDIT + " " + COMMON))
    T_.append(("TK_Ch78_DeckCheck_Verify", "Verify the deck standard check v1_1_0 on the evidence bridge", "Verify", ["TK_Ch78_DeckCheck"], "builder", "T0+0.7h", 0.5,
        "Re-run on the bridge: v1_0_0 byte-identical; the diff limited to the reading of the concept class; the same results as v1_0_0 on chapters 5, 6 and 7; D4 and D11 measured on chapters 8 to 14 with the concept counts stated; no file edited."))
    for nn in URGENT:
        c = ch(nn); dv = "T0+2.0h" if nn == "07" else "T0+2.5h"
        T_.append(("TK_Ch%s_Deck_Build" % nn, "Rebuild the deck of chapter %s to the deck standard with its chapter-code manifest" % c, "Build", [], "SEN0401-I20-deck-ch%s" % nn, "T0", 1.5, deck_note(nn, False)))
        T_.append(("TK_Ch%s_Deck_Verify" % nn, "Verify the deck of chapter %s against the deck standard" % c, "Verify", ["TK_Ch%s_Deck_Build" % nn] + (["TK_Ch78_DeckCheck_Verify"] if checkver(nn) == "v1_1_0" else []), "builder", "T0+1.5h" if nn == "07" else "T0+2.0h", 0.5,
            "Run %s for chapter %s, the Deck chapter check v1_3_0 for Deck/Ch%s, the deck match check and the manifest equality; read the deck slide by slide (the reading by the three roles of the owner's preference - teaching academician, reviewing faculty specialist, student - is recorded as a reading, not as a tool result); record every result as printed." % (checkdesc(nn), c, nn)))
        T_.append(("TK_Ch%s_Page_Build" % nn, "Rebuild the page of chapter %s on template 9.52.2 with the chapter-code tab" % c, "Build", ["TK_Ch%s_Deck_Verify" % nn, "TK_Charset_Template_Verify", "TK_Charset_Check_Verify"], "SEN0401-I20-page-ch%s" % nn, dv, 1.5, page_note(nn)))
        T_.append(("TK_Ch%s_Page_Verify" % nn, "Verify the rebuilt page of chapter %s" % c, "Verify", ["TK_Ch%s_Page_Build" % nn], "builder", "T0+3.5h" if nn == "07" else "T0+4.5h", 1.0,
            "Re-run serially the charset check and the page tests 9.36.0, 9.34.1 and 9.35.1, the Stage 4 gate runner v1_1_0, the Research, Deck and Page chapter checks, the deck match check and the manifest equality (the chapter-code tab equals the deck's code order); record every result as printed."))
    return T_
def mk_retro_tasks():
    T_ = []
    for k, nn in enumerate(RETRO):
        c = ch(nn); h = 2.0 * k
        T_.append(("TK_Ch%s_Deck_Build" % nn, "Rebuild the deck of chapter %s to the deck standard with its chapter-code manifest" % c, "Build", ["TK_Ch78_DeckCheck_Verify"] if checkver(nn) == "v1_1_0" else [], "SEN0401-I21-deck-ch%s" % nn, "S+%.1fh" % h, 1.5, deck_note(nn, True)))
        T_.append(("TK_Ch%s_Deck_Verify" % nn, "Verify the deck of chapter %s against the deck standard" % c, "Verify", ["TK_Ch%s_Deck_Build" % nn], "builder", "S+%.1fh" % (h + 1.5), 0.5,
            "Run %s for chapter %s, the Deck chapter check v1_3_0 for Deck/Ch%s, the deck match check and the manifest equality; read the deck slide by slide (the three roles; recorded as a reading); record every result as printed." % (checkdesc(nn), c, nn)))
        T_.append(("TK_Ch%s_Page_Build" % nn, "Rebuild the page of chapter %s on template 9.52.2 with the chapter-code tab" % c, "Build", ["TK_Ch%s_Deck_Verify" % nn, "TK_Charset_Template_Verify", "TK_Charset_Check_Verify"], "SEN0401-I21-page-ch%s" % nn, "S+%.1fh" % (h + 2.0), 1.5, page_note(nn)))
        T_.append(("TK_Ch%s_Page_Verify" % nn, "Verify the rebuilt page of chapter %s" % c, "Verify", ["TK_Ch%s_Page_Build" % nn], "builder", "S+%.1fh" % (h + 3.5), 1.0,
            "Re-run serially the charset check and the page tests 9.36.0, 9.34.1 and 9.35.1, the Stage 4 gate runner v1_1_0, the Research, Deck and Page chapter checks, the deck match check and the manifest equality; record every result as printed."))
    return T_
def stories(chs, plan_it):
    S = []
    for nn in chs:
        c = ch(nn)
        S.append(("ST_Ch%s_Deck" % nn, "The deck of chapter %s meets the deck standard and carries its chapter-code manifest" % c, "Del3_%sDecks" % plan_it, "Obj3_%s" % plan_it, ["AC7_Deck_Ch%s" % nn], ["TK_Ch%s_Deck_Build" % nn, "TK_Ch%s_Deck_Verify" % nn]))
        S.append(("ST_Ch%s_Page" % nn, "The page of chapter %s is rebuilt on template 9.52.2 and meets the page standard with the character set first" % c, "Del3_%sPages" % plan_it, "Obj3_%s" % plan_it, ["AC7_Page_Ch%s" % nn], ["TK_Ch%s_Page_Build" % nn, "TK_Ch%s_Page_Verify" % nn]))
    return S
STORIES1 = [("ST_Ch78_DeckCheck", "A deck standard check that measures the key concepts of every chapter's research, as a new file", "Del3_Ch78Decks", "Obj3_Ch78", ["AC7_DeckCheck"], ["TK_Ch78_DeckCheck", "TK_Ch78_DeckCheck_Verify"])] + stories(URGENT, "Ch78")
STORIES2 = stories(RETRO, "Retrofit")
TASKS1 = mk_tasks(); TASKS2 = mk_retro_tasks()

def gh_deckcheck():
    return ("Owner-directed work (" + CR + "). Given the deck standard check v1_0_0 (byte-identical after the task) and the research files of chapters 5 to 14, when the NEW file sen0401_deck_standard_check_v1_1_0.py is written, then ALL of: (1) the file is new and v1_0_0 is byte-identical (SHA-256 before and after); "
            "(2) the diff against v1_0_0 is limited to the reading of the key-concept class (sen0401:PrimarySourceConcept and sen0414:PrimarySourceConcept); (3) on chapters 5, 6 and 7 every element gives the same result and the same measured numbers as v1_0_0; (4) on chapters 8 to 14 the elements D4 and D11 give a measured number and PASS or FAIL instead of NOT_MEASURED, and the concept counts are chapter 8: 46, 9: 38, 10: 62, 11: 43, 12: 43, 13: 29, 14: 69; "
            "(5) no committed file is edited, no gate, test or threshold changed; the logs are kept; results as printed; if any element fails the file is named failing. MEASURED FACT. The v1_0_0 check returns NOT_MEASURED for D4 and D11 on chapters 8 to 14 ('no research concept list found'); a skip is not a pass. " + STD_D)
def gh_deck(nn):
    c = ch(nn); dv = DECKV.get(nn, "the new version")
    return ("Owner-directed work (" + (CR if nn in URGENT else CRR) + ", " + WHEN + "). Given the newest deck of chapter %s (%s, unchanged) and its research, when the deck is rebuilt as a new file (version %s) with its chapter-code manifest chapter_code_ch%s_v1_0_0.json, then ALL of: "
            "(1) %s for chapter %s reports every element D1 to D12 met and exits 0 (no NOT_MEASURED); (2) the Deck chapter check v1_3_0 for Deck/Ch%s passes and the deck match check reports 0 not carried; "
            "(3) the manifest lists the deck's code examples in slide order, by name, and the order equals the order of the code slides (measured by the deck control check v1_1_0); (4) no committed file is edited, including the executor's own logs (written once); results as printed; if any element fails the deck is named failing and this criterion has no passing result. " % (c, deckfile(nn), dv.replace("_", "."), nn, checkdesc(nn), c, nn) + (FACT + " " if nn in URGENT else "MEASURED FACTS: see ex:IA3_Ch78. ") + STD_D)
def gh_page(nn):
    c = ch(nn); pv = vdot(PAGEV[nn]) if nn in PAGEV else "above the newest page " + vdot(pagever(nn))
    return ("Owner-directed work (" + (CR if nn in URGENT else CRR) + ", " + WHEN + "). Given the rebuilt deck of chapter %s with its manifest and the newest page of chapter %s (%s), when the page is rebuilt as a new file with the page version %s on the template 9.52.2 with the builders v4_15_0 and v2_24_0, then ALL of: "
            "(1) the charset check exits 0 on the page (the tag below byte 1024, the first 1024 bytes decode as UTF-8); (2) the page test 9.36.0 runs all its added features with no skip and passes them (P1, P2, P3, P4, P5, P6, P8, P9, P11) and every other feature, exit 0, and the page tests 9.34.1 and 9.35.1 report no failure and widgets, features and gates not below the stored result of the page %s, skipped not more; "
            "(3) the chapter-code tab equals the deck's chapter-code manifest in names and order and each example runs in the page and shows its result; (4) the Stage 4 gate runner v1_1_0 for %s exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, the Research, Deck and Page chapter checks pass, the deck match check reports 0 not carried; "
            "(5) no committed file is edited (an executor's own log is written once), no gate, test or threshold changed; the Stage 4 page ABox and the stored page-test result are new files; results as printed; if any element fails the page is named failing and this criterion has no passing result. " % (c, c, pagefile(nn), pv, vdot(pagever(nn)), c) + (FACT + " " if nn in URGENT else "MEASURED FACTS: see ex:IA3_Ch78. ") + STD_P)
CRIT = {"AC7_DeckCheck": ("The deck standard check v1_1_0 measures the key concepts of every chapter's research and changes nothing else", gh_deckcheck)}
for _nn in URGENT + RETRO:
    CRIT["AC7_Deck_Ch%s" % _nn] = ("The deck of chapter %s meets the deck standard D1 to D12 and carries its chapter-code manifest" % ch(_nn), (lambda n=_nn: gh_deck(n)))
    CRIT["AC7_Page_Ch%s" % _nn] = ("The page of chapter %s rebuilt on template 9.52.2 declares its character set within the first 1024 bytes and passes all three page tests" % ch(_nn), (lambda n=_nn: gh_page(n)))

def task_block(tid, title, ttype, deps, sess, est, hrs, note, it, state, base):
    full = note + " Planned session %s; estimated start %s (%s), about %s hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)." % (sess, est, "T0 = the first executor start of the iteration" if it == IT1 else "S = the start of the iteration, planned and not yet held", hrs)
    return ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ; backlog:responsible %s ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:%s ;\n%s'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n'
            '    backlog:hasAuditNote %s .\n') % (tid, lit(title), tid, lit(title), it, NEWB, G.EXEC, "NewCapability" if ttype == "Build" else "Compliance", ttype, state,
                                                 ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + d for d in deps)) if deps else "", lit(full))
def story_block(sid, title, deliv, obj, crits, tks, note, it, state):
    return ('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
            '    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability %s ; backlog:soThat %s ;\n'
            '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion %s ;\n'
            '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible %s ;\n'
            '    backlog:decomposesInto %s ;\n    backlog:hasState backlog:%s ;\n'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored by the ranking step of the same change route." ;\n'
            '    backlog:hasAuditNote %s .\n') % (sid, lit(title), sid, lit(title), it, NEWB, lit(title[0].lower() + title[1:]), lit("the instructor can teach the chapter from a deck and a page that meet the written standard"), deliv, obj,
                                                 ", ".join("ex:" + c for c in crits), G.EXEC, ", ".join("ex:" + x for x in tks), state, lit(note))

# ---------------------------------------------------------------- events
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Chapters 7 and 8 are urgent: may they get a deck, a chapter-code manifest and a page on the current standard, with a deck check that measures their research?"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR3_Charset, ex:CR3_Remedy56 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit("Requested " + WHEN + ": chapters 6, 7 and 8 are urgent; chapter 6 is rebuilt already (Iteration 19). Chapters 7 and 8 need a deck, a chapter-code manifest and a page on the current standard (template 9.52.2, character set first). " + FACT +
                " The change grows the scope: two decks and two pages rebuilt as new files, and a new version of the deck check, because the present check cannot measure two of its twelve elements on chapter 8. Pending until the ScopeChange that admits the stories is recorded in the Backlog version."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What bringing chapters 7 and 8 to the current standard costs, measured before it is started"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_Charset ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACT + " AFFECTED: the decks of chapters 7 (1.3.0) and 8 (1.1.0) and the pages 9.76.0 and 9.77.0 are replaced by new files (the old files stay); the deck check gets a new file v1_1_0 (v1_0_0 stays). NOT AFFECTED: the template 9.52.2, the page builders and tests, the pages and decks of every other chapter, the Mission outcome and the Achieved status. "
                    "PLAN (route as ex:CR3_Charset, G127): a StageRevision from the Scope stage, seven versions; new iteration Iter_20 with five stories and ten tasks: the deck check v1_1_0 (an executor, about 0.5 h, verified about 0.5 h by the builder); the decks of chapters 7 and 8 (two executors in parallel, about 1.5 h each, verified about 0.5 h each by the builder); then the pages of chapters 7 and 8 (two executors, about 1.5 h each with three serial page-test runs each, verified about 1 h each by the builder with three serial runs). "
                    "Measured from the chapters 5 and 6 work of 2026-10-22 and 23: the deck executor of chapter 6 needed 35 minutes, the page executor 62 minutes on an idle machine, a control run of one page test about 10 minutes. The machine has 2 cores shared with other sessions; browser tests run one at a time. "
                    "Estimated from T0 (the executors of the deck check and of both decks start at once): decks verified about T0+2.0 h and T0+2.5 h; page of chapter 7 about T0+3.5 h, page of chapter 8 about T0+4.5 h, all on an idle machine; with the present machine load of other sessions the browser tests may take twice as long, so up to about T0+8 h. The proposed end is Saturday 2026-10-24 09:00 UTC, the owner's to decide. "
                    "COST: new files only; old files byte-identical; no gate, test or threshold changes. A criterion that fails is named failing and its story is not Done; nothing is waived."))
    cr2 = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "After chapters 7 and 8: bring chapters 1 to 4 and 9 to 14 to the same standard, in order"@en ;\n'
           '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso %s ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CRR, CR, lit("Requested " + WHEN + ": after chapters 6, 7 and 8, return to all chapters starting with chapter 1 (retrofit: manifest, deck match, page with chapter-code tab and panels, character set) and after that build the remaining chapters. " + FACT +
                     " Planned now, NOT started: Iteration 21 holds the ten chapters 1 to 4 and 9 to 14 in order (chapters 5 to 8 are done by Iterations 19 and 20), each as a deck story and a page story with its own criterion. Nothing is unbuilt in the fourteen chapters, so 'the remaining chapters' has no content beyond this retrofit; the owner's materials folder 'numbers' is the only other material and is not a chapter. Pending until the ScopeChange that admits the stories is recorded in the Backlog version."))
    ia2 = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the retrofit of chapters 1 to 4 and 9 to 14 costs, estimated before it is planned into an iteration"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso %s ;\n    backlog:hasImpactStatement %s .\n') % (
        IAR, CRR, IA, lit(FACT + " ESTIMATE per chapter (executor and builder hours): deck 1.5 h build plus 0.5 h verification, page 1.5 h build plus 1.0 h verification = 4.5 h; ten chapters = 45 hours of work, of which the browser tests (three runs by the executor, three by the builder, about 10 minutes each on an idle machine = about 1 h per page) are serial: about 10 hours of browser time. "
                       "With three executors in parallel and the machine as it is today the retrofit is about 2 days of wall-clock (planned Sunday 2026-10-25 to Monday 2026-10-26, from the end of Iteration 20); the estimates are not measurements. ORDER: chapters 1, 2, 3, 4, then 9, 10, 11, 12, 13, 14 (chapters 5 and 6 are done, 7 and 8 are in Iteration 20). "
                       "NOT STARTED: no executor is briefed, no work begun is recorded; the stories are Proposed. COST: new files only."))
    return t + cr + ia + cr2 + ia2, "ChangeRequests %s and %s (Pending) with their ImpactAssessments for the owner's decision of 2026-10-23 16:06: chapters 7 and 8 urgent, then the retrofit of chapters 1 to 4 and 9 to 14 in order." % (CR, CRR)
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change requests " + CR + " and " + CRR + " (" + WHEN + ") add deliverables (decks and pages of chapters 7 and 8 and a new deck check version, and the planned retrofit of ten more chapters, all as new files); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). "
              "The requests and their impact assessments " + IA + " and " + IAR + " were recorded first. This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated. "
              "The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). Recorded as decided by the builder role.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: chapters 7 and 8 urgent, then the retrofit of chapters 1 to 14"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, %s, %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, IA, CRR, IAR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for chapters 7 and 8 and the retrofit: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    D = [("Del3_Ch78Decks", "The decks of chapters 7 and 8 rebuilt to the deck standard with their chapter-code manifests, and a deck check that measures the key concepts of every chapter's research, as new files",
          "The decks of chapter 7 and chapter 8 as new files with new version numbers meeting the deck standard D1 to D12 with a chapter-code manifest each, and a new deck standard check v1_1_0 (v1_0_0 stays) that reads the key concepts of the research whichever class declares them. " + FACT + " " + STD_D),
         ("Del3_Ch78Pages", "The pages of chapters 7 and 8 rebuilt on template 9.52.2 with the chapter-code tab and the character set first",
          "The pages of chapter 7 and chapter 8 as new files on template 9.52.2 with the builders v4_15_0 and v2_24_0, passing the charset check, the page test 9.36.0 and the page tests 9.34.1 and 9.35.1 with no failure, the Stage 4 gate runner and the chapter checks. " + STD_P),
         ("Del3_RetrofitDecks", "The decks of chapters 1 to 4 and 9 to 14 rebuilt to the deck standard with their chapter-code manifests (planned, not started)",
          "The decks of chapters 1, 2, 3, 4, 9, 10, 11, 12, 13 and 14 as new files meeting the deck standard D1 to D12 with a chapter-code manifest each, in this order. Planned in Iteration 21; no executor is briefed. " + FACT),
         ("Del3_RetrofitPages", "The pages of chapters 1 to 4 and 9 to 14 rebuilt on template 9.52.2 with the chapter-code tab and the character set first (planned, not started)",
          "The pages of chapters 1, 2, 3, 4, 9, 10, 11, 12, 13 and 14 as new files on template 9.52.2 passing the charset check, the page tests and the chapter checks, in this order. Planned in Iteration 21; no executor is briefed. " + STD_P)]
    L = "".join('''
ex:%s a backlog:ScopeDeliverable ;
    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
''' % (i, lit(lb), T.CLAUSE, lit(tx)) for i, lb, tx in D)
    L += "ex:Scope3 backlog:requiresDeliverable %s ; rdfs:seeAlso %s, %s, %s, %s .\n" % (", ".join("ex:" + d[0] for d in D), CR, IA, CRR, IAR)
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-23 by the stage revision %s on the change requests %s and %s (%s). The statement above is unchanged (L-112). It now also requires four deliverables in the area ex:Area3_Remedy56 (the decks and pages of chapters 7 and 8 with a new deck check version; the planned retrofit of the decks and pages of ten more chapters). No exclusion changes: new files only, and the exclusion of changes to gates, tests and thresholds still holds." % (REV, CR, CRR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR9", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for chapters 7 and 8 and the retrofit: four deliverables in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR9", prev); t = X.set_status(t, "LS_Goaled")
    def goal(g, lab, cr, ratio, spec_id, spec_t, scen1, scen2):
        return '''
ex:%(g)s a backlog:Goal ;
    rdfs:label %(lab)s@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Must ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %(r)s ;
    backlog:producedByStage ex:Out3_GoalR9 .
ex:%(g)s rdfs:comment "Drafted by the builder session on 2026-10-23 from the change request %(cr)s; the intent origin is therefore Derived."@en .
ex:%(sp)s a backlog:Specification ;
    rdfs:label %(spl)s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:%(g)s ;
    backlog:hasSpecificationText %(st)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR9 .
ex:%(sp)s_Pass a backlog:TestScenario ; rdfs:label %(s1l)s@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:%(sp)s ; backlog:hasScenarioText %(s1)s .
ex:%(sp)s_Fail a backlog:TestScenario ; rdfs:label %(s2l)s@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:%(sp)s ; backlog:hasScenarioText %(s2)s .
''' % dict(g=g, lab=lit(lab), cr=cr.replace("ex:", "ex:"), r=lit(ratio), sp=spec_id, spl=lit("What it is for a chapter to meet the deck and page standard"), st=lit(spec_t), s1l=lit(scen1[0]), s1=lit(scen1[1]), s2l=lit(scen2[0]), s2=lit(scen2[1]))
    t += goal("G3_Ch78", "The decks and pages of chapters 7 and 8 meet the written teaching-material standard", CR, "Derived from the revised scope and the change request " + CR + ": chapters 6, 7 and 8 are urgent for the owner's teaching. " + FACT,
              "Spec3I_Ch78", "A chapter meets the standard when its deck passes the deck standard check (D1 to D12, none NOT_MEASURED) and carries a chapter-code manifest, and its page is built on template 9.52.2, passes the charset check and the three page tests, and lists the deck's code examples in the same order. " + STD_D + " " + STD_P,
              ("A deck and page of chapter 7 or 8 meet the standard", "Given the rebuilt deck and page of chapter 7 or 8, when the deck standard check, the charset check and the page tests are run, then every element passes and the chapter-code tab equals the manifest."),
              ("The existing deck 1.3.0 of chapter 7 does not meet the standard", "Given the deck of chapter 7 version 1.3.0 (26 slides), when the deck standard check v1_0_0 is run, then it fails D1, D2, D3, D4, D5, D7, D10 and D11 (measured 2026-10-23) and the deck carries no passing result."))
    t += goal("G3_Retrofit", "The decks and pages of chapters 1 to 4 and 9 to 14 meet the same standard (planned)", CRR, "Derived from the revised scope and the change request " + CRR + ": after chapters 6, 7 and 8 all chapters follow in order. " + FACT,
              "Spec3I_Retrofit", "The same standard as for chapters 7 and 8, chapter by chapter in the order 1, 2, 3, 4, 9, 10, 11, 12, 13, 14. " + STD_D + " " + STD_P,
              ("A retrofitted chapter meets the standard", "Given a retrofitted chapter, when the checks are run, then every element passes as for chapters 7 and 8."),
              ("A chapter whose page declares the character set late is not claimed", "Given the page of chapter 1 (version 9.70.0, tag at byte 11172), when the charset check is run, then it fails and the chapter carries no passing result."))
    return t + SL.out_new(t, "Goal", "Out3_GoalR9", "Out3_ScopeR9"), "third lineage, Goal stage rebuilt for chapters 7 and 8 and the retrofit: two goals with a specification and scenarios each."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR9", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    def obj(o, m, lab, mlab, goal, query, base, target, cp, cond, obsid, obsm):
        return '''
ex:%(o)s a backlog:Objective ; rdfs:label %(lab)s@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:%(g)s ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:%(m)s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %(q)s ;
    backlog:hasBaselineValue "%(b)s"^^xsd:decimal ; backlog:hasTargetValue "%(tv)s"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:%(cp)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR9 .
ex:%(m)s a backlog:Metric ; rdfs:label %(ml)s@en ; backlog:belongsToLineage ex:Lineage3 .
ex:%(cp)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the rebuilt chapters are controlled"@en ;
    backlog:checkpointCondition %(cc)s ; backlog:expectedValue "%(tv)s"^^xsd:decimal .
ex:%(ob)s a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(o)s ; backlog:hasObservedValue "%(b)s"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %(om)s .
ex:%(o)s rdfs:comment "Drafted by the builder session on 2026-10-23 from the change requests %(crs)s; the intent origin is therefore Derived."@en .
''' % dict(o=o, m=m, lab=lit(lab), ml=lit(mlab), g=goal, q=lit(query), b=base, tv=target, cp=cp, cc=lit(cond), ob=obsid, now=now, om=lit(obsm), crs=CR + " and " + CRR)
    Q = "Count of the chapters (of the fourteen) for which the deck standard check exits 0 on the newest deck with no NOT_MEASURED, a chapter-code manifest exists, and the charset check passes on the newest page, read from the runs after the evidence bridge has run them."
    t += obj("Obj3_Ch78", "Met3_Ch78", "Chapters 7 and 8 meeting the deck and page standard: from 0 to 2", "chapters of 7 and 8 whose deck, manifest and page meet the standard", "G3_Ch78", Q + " Restricted to chapters 7 and 8.", 0, 2, "CP3I_Ch78", "Taken after the evidence bridge has run the checks of the criteria on the rebuilt decks and pages, so the count is read from verified runs.", "Obs45_Ch78",
             "Baseline from the builder's measurement of 2026-10-23: the deck standard check fails both decks, no manifest exists, the charset check fails both pages, so 0 of 2.")
    t += obj("Obj3_Retrofit", "Met3_Retrofit", "Chapters of the fourteen meeting the deck and page standard: from 2 to 14", "chapters of 14 whose deck, manifest and page meet the standard", "G3_Retrofit", Q, 2, 14, "CP3I_Retrofit", "Taken after the evidence bridge has run the checks of the criteria on the rebuilt decks and pages of the chapters, so the count is read from verified runs.", "Obs45_Retrofit",
             "Baseline from the builder's measurement of 2026-10-23: chapters 5 and 6 pass the deck standard check (PASS=12), carry a manifest and have a page that passes the charset check; the other twelve fail, so 2 of 14.")
    return t + SL.out_new(t, "Objective", "Out3_ObjectiveR9", "Out3_GoalR9"), "third lineage, Objective stage rebuilt for chapters 7 and 8 and the retrofit: two objectives (chapters 7 and 8 meeting the standard, 0 to 2; all chapters, 2 to 14) with metrics, checkpoints and baseline readings."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR9", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR10"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = ['ex:TS_DeckStdCheck11 a backlog:ToolScript ; rdfs:label "deck standard check v1_1_0 (new tool: reads the key concepts of the research whichever class declares them)"@en ; backlog:scriptFileName "sen0401_deck_standard_check_v1_1_0.py" ; backlog:acceptsGraphPath false .\n']
    deck_tools = lambda nn: ["TS_DeckStdCheck11" if checkver(nn) == "v1_1_0" else "TS_DeckStdCheck", "TS_ChapterCheck", "TS_DeckMatch", "TS_RdodiValidatorPinned"]
    page_tools = ["TS_PageTemplateE", "TS_PageCharsetCheck", "TS_PageBuilder415", "TS_PageData224", "TS_PageTest36"] + RV.BASE
    cases = {}
    for c, (lab, fn) in CRIT.items():
        nn = c[-2:]
        tools = ["TS_DeckStdCheck11", "TS_DeckStdCheck"] if c == "AC7_DeckCheck" else (deck_tools(nn) if "_Deck_" in c else page_tools)
        k = "TC3I_K" if c == "AC7_DeckCheck" else ("TC3I_D" if "_Deck_" in c else "TC3I_P"); cases.setdefault(k, []).append(c)
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs and the diffs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:%s_Passes, ex:%s_NotClaimed .\n' % (
            c, lit(lab), lit(fn()), ", ".join("ex:" + x for x in tools), lit(VER_D if k != "TC3I_P" else VER_P), k, k))
    sc = {"TC3I_K": ("Spec3I_Ch78", "The deck check v1_1_0 gives the same results as v1_0_0 on chapters 5 to 7 and measures D4 and D11 on chapters 8 to 14", "Run v1_0_0 and v1_1_0 on the chapters and compare; they agree on chapters 5, 6, 7 and v1_1_0 gives a measured D4 and D11 on 8 to 14.", "The v1_0_0 check on chapter 8 returns NOT_MEASURED for D4 and D11 (measured 2026-10-23) and no deck of chapters 8 to 14 can pass the standard with it."),
          "TC3I_D": ("Spec3I_Ch78", "Run the deck standard check, the chapter checks and the manifest check on the rebuilt deck", "Run the checks of the criterion over the newest deck; they report no failure and no NOT_MEASURED and exit 0.", "Run the deck standard check on the existing deck of chapter 7 (1.3.0); it fails D1, D2, D3, D4, D5, D7, D10 and D11 and the deck carries no passing result."),
          "TC3I_P": ("Spec3I_Ch78", "Run the charset check and the page tests on the rebuilt page", "Run the checks of the criterion over the newest page; they report no failure and no skip and exit 0.", "Run the charset check on the existing page 9.76.0 of chapter 7 (tag at byte 11172); it fails and the page carries no passing result.")}
    for k, crs in cases.items():
        spec, lab, pas, fl = sc[k]
        L.append('''
ex:%(k)s_Passes a backlog:TestCase ; rdfs:label %(l1)s@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Spec3I_Ch78_Pass, ex:Spec3I_Retrofit_Pass ; backlog:runsOnData ex:Data3I_%(k)s_Passing ;
    backlog:hasCaseText %(pas)s .
ex:%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on the existing file that fails and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Spec3I_Ch78_Fail, ex:Spec3I_Retrofit_Fail ; backlog:runsOnData ex:Data3I_%(k)s_Failing ;
    backlog:hasCaseText %(fl)s .
ex:Data3I_%(k)s_Passing a backlog:TestData ; rdfs:label "The rebuilt files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest rebuilt files, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3I_%(k)s_Failing a backlog:TestData ; rdfs:label "The existing file that fails the checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The existing deck or page of the chapter as measured on 2026-10-23 (ex:IA3_Ch78)." .
''' % dict(k=k, l1=lit(lab), cr=", ".join("ex:" + c for c in crs), sp=spec if True else "", pas=lit(pas), fl=lit(fl)))
    # the scenarios of the retrofit goal are named Spec3I_Retrofit_*, used by the retrofit criteria: reuse the nominal and rejection scenario of the urgent goal for the cases (one spec per goal is not required by a case)
    def items(S, TKS, it, state, base):
        for sid, title, deliv, obj, crits, tks in S:
            L.append(story_block(sid, title, deliv, obj, crits, tks, "Requested " + WHEN + " (" + (CR if it == IT1 else CRR) + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment " + (IA if it == IT1 else IAR) + ".", it, state))
        for tid, title, ttype, deps, sess, est, hrs, note in TKS:
            L.append(task_block(tid, title, ttype, deps, sess, est, hrs, note, it, "Ready" if (state == "Ready" and ttype == "Build") else "Proposed", base))
    DONE = {"TK_Charset_Template_Verify", "TK_Charset_Check_Verify"}
    items(STORIES1, TASKS1, IT1, "Ready", True)
    items(STORIES2, TASKS2, IT2, "Proposed", False)
    sid1 = [s[0] for s in STORIES1]; tk1 = [x[0] for x in TASKS1]; sid2 = [s[0] for s in STORIES2]; tk2 = [x[0] for x in TASKS2]
    for x in sid1 + tk1:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, IT1, lit("Refined by the builder session from the change request %s and the measured facts of %s: acceptance criterion with tool and version, dependencies, estimated start, and a brief to be generated; startable when its dependencies are Done." % (CR, IA))))
    for sid, title, deliv, obj, crits, tks in STORIES1:
        L.append('ex:Plan3I_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 20"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Ch78, ex:Spec3I_Ch78_Pass, ex:Spec3I_Ch78_Fail .\n' % (sid, sid, now, IT1, sid, ", ".join("ex:" + x for x in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    for sid in sid2: L.append("ex:%s backlog:standsAlone true .\n" % sid)
    L.append("ex:Obj3_Ch78 backlog:metricMovableBy %s .\nex:Obj3_Retrofit backlog:metricMovableBy %s .\n" % (", ".join("ex:" + s for s in sid1), ", ".join("ex:" + s for s in sid2)))
    SG1 = "The decks and pages of chapters 7 and 8 meet the written standard on template 9.52.2, measured by the deck check (a new version that reads their research), the charset check and the page tests, verified by the evidence bridge; everything is a new file and nothing existing is edited. Frozen at the planning ceremony."
    DS1 = ("Proposed by the builder session on 2026-10-23: the start is the instant of the planning ceremony ex:PC3_Iter_20; the proposed end is Saturday 2026-10-24 09:00 UTC; the owner decides the end. Justification (estimates, not measurements; measured analogues: the deck executor of chapter 6 needed 35 minutes, the page executor 62 minutes, a control run of one page test about 10 minutes, on an idle machine): "
           "the deck check v1_1_0 about 0.5 h and its verification 0.5 h; the two decks in parallel about 1.5 h each, verified about 0.5 h each; the two pages follow, about 1.5 h each with three serial page-test runs each, verified about 1 h each, serial. Critical path on an idle machine: 1.5 h + 0.5 h + 1.5 h + 1.0 h = about 4.5 h for chapter 7 and about 1 h later for chapter 8; the machine has 2 cores shared with other sessions and the browser tests queue, so the window allows about 18 hours. Chapter 8 can be declined without blocking chapter 7.")
    L.append('%s a backlog:Iteration ; rdfs:label "Iteration 20: chapters 7 and 8 on the current standard"@en ; backlog:hasIdentifier "Iter_20" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (IT1, now, END1, lit(DS1), lit(SG1), ", ".join("ex:" + x for x in sid1 + tk1)))
    L.append('ex:PB3I_Iter_20 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 20 when it was planned"@en ; backlog:baselineFor %s ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (IT1, now, now, END1))
    L.append('ex:PC3_Iter_20 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 20: chapters 7 and 8"@en ; backlog:ceremonyFor %s ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (IT1, now, ", ".join("ex:Plan3I_" + s for s in sid1), lit("Held %s by the builder session after the change request %s: five stories and ten tasks are committed to this iteration, whose goal is frozen at its start. No executor has started in it; work begun is recorded at the real start of each executor session, with its brief." % (now, CR))))
    SG2 = "The decks and pages of chapters 1 to 4 and 9 to 14 meet the written standard in this order. PLANNED, not started: no ceremony is held, no executor is briefed."
    DS2 = ("Planned by the builder session on 2026-10-23 on the owner's decision of 16:06 Istanbul; not started. Estimates, not measurements: per chapter deck 1.5 h build + 0.5 h verification, page 1.5 h build + 1.0 h verification (4.5 h), ten chapters 45 h of work, about 10 h of serial browser time; with three executors in parallel about two days, from the end of Iteration 20 (Saturday 2026-10-24 09:00 UTC) to Monday 2026-10-26 09:00 UTC. The start and the end are the owner's to confirm when the iteration is planned; the planning ceremony is held then.")
    L.append('%s a backlog:Iteration ; rdfs:label "Iteration 21: the retrofit of chapters 1 to 4 and 9 to 14 (planned, not started)"@en ; backlog:hasIdentifier "Iter_21" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (IT2, START2, END2, lit(DS2), lit(SG2), ", ".join("ex:" + x for x in sid2 + tk2)))
    L.append('ex:SC3_Ch78 a backlog:ScopeChange ;\n    rdfs:label "Scope grown: chapters 7 and 8 urgent, then the retrofit of ten more chapters"@en ;\n    backlog:fulfillsRequest %s, %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, CRR, ", ".join("ex:" + s for s in sid1 + sid2), lit("Requested " + WHEN + ". The boundary moved outward by twenty-five stories; new files only; nothing existing is edited or weakened.")))
    for crx in (CR, CRR):
        t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(crx), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
        L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Ch78 and the stories it admits; it was Pending before. The direction is the owner\'s decision of 2026-10-23 16:06 Istanbul as relayed by the course coordinator; the end of the iterations is still the owner\'s."@en .\n' % (crx, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR11", "Out3_ObjectiveR9"), "third lineage, Backlog stage rebuilt for chapters 7 and 8 and the retrofit: Iteration 20 (five stories, ten tasks, planned) and Iteration 21 (twenty stories, forty tasks, planned and not started), criteria with tools and versions, the ScopeChange; both change requests Accepted; the %d carried items are re-admitted, not re-dated." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete and no work is begun." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
