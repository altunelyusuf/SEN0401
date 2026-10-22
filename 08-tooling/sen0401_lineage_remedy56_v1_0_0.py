#!/usr/bin/env python3
"""sen0401_lineage_remedy56 v1_0_0 - change route (rulings G125, G127, G133) for the owner's direction of 2026-10-22 17:27 and 17:30 Istanbul on the chapter 5 and chapter 6 decks and pages.
This file records the FIRST event only: the ChangeRequest (Pending) and the ImpactAssessment with the measured facts, the written teaching-material standard, the plan (stories, tasks, order), the iteration proposal and the duration.
The StageRevision events (retract, scope, goal, objective, backlog, begin) follow as separate versions. No brief is generated before the facts are in the register. Times from the clock (UTC).
Usage: sen0401_lineage_remedy56_v1_0_0.py change"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

lit = lambda s: '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
Q1 = ('"I need the chapter 5 and 6 urgently. The HTML file Playground code list is crazily extends outside of the page space. You put the code there not the name of the code. Chapter code is not listed as far as I see. '
      'I need a specific tab just to run the chapter code matching with the same order of the ppt. Additionally, multiple concepts are presented on the same page with downward flow. You can add one more step to the hierarchy and build the details in lower level panels. '
      'Repeating the same menu items on the tab and left hierarchical menu is not good when the tabs are not fitting on a single line. PPT is very poor in content and just listing codes with sub shapes and concept names. '
      'They cannot be presented nor understandable. They are certainly not matches with any standards of teaching materials."')
Q2 = '"I want you to remedy the weaknesses and provide me Chapter 5 and 6 PPT and Interactive pages ready to use."'
OWNER_ACT = ("Owner's messages of Thursday 2026-10-22, relayed by the course coordinator and recorded by the builder session. 17:27 Istanbul (14:27 UTC), quoted: %s 17:30 Istanbul (14:30 UTC), quoted: %s "
             "The 17:30 message authorises the scope: remedy the weaknesses and deliver the chapter 5 and chapter 6 decks and interactive pages ready to use. Under the standing rule that work following the owner's direction is recorded as owner-directed, it is not listed as an open owner confirmation. "
             "The end of the iteration is still the owner's." % (Q1, Q2))
FACTS = ("MEASURED FACTS (fact-finding agent of the coordinator, read-only, tools Playwright 1.56.0 and python-pptx 1.0.2, date 2026-10-22; the builder session did not re-measure them and states so). "
         "PAGE. The Playground is one select with 97 options (chapter 5) and 106 (chapter 6); its width is 4861 px and 5836 px, and it is still that wide at 390 px in a container 242 px wide. "
         "83 of 97 and 92 of 106 option labels read 'Name: code', so the whole label is the code (longest 840 and 828 characters); the chapter items are 76 and 85. Of the page items 4 of 76 (chapter 5) and 0 of 85 (chapter 6) appear in the deck. "
         "The deck code blocks are 18 (9 slides) and 21 (13 slides); they call chapter-library functions (master, ckd_priv, parse_tx, weight, block_subsidy, WORDS, TV, ALICE and others) that the page does not define, so a deck REPL line cannot be pasted into the Playground; the Playground items follow concept order, not slide order. "
         "The Learn tab bar has a second row of 8 folder tabs that repeats the 8 left-tree folders (8 of 8 the same label); the Learn sub-tab bar has 10 tabs, wraps to 3 rows (chapter 5) and 2 rows (chapter 6) at 1366 px and scrolls sideways at 390 px. "
         "The group panes stack 2 to 7 h4 concepts and are 3751 to 10754 px (chapter 5) and 2544 to 7530 px (chapter 6) tall; the Lecture pane has 23 and 26 cards and is 4107 and 4875 px tall; the Stories are 4.1 and 6.4 screens. "
         "DECK. Chapter 5 has 23 slides (average 74 words, longest box 39 words); chapter 6 has 26 (average 81, longest box 56). Of the code slides 9 and 13 are two REPL transcripts plus 3 caption pills; the executed result is REPL text, not a visual. "
         "Native charts: 1 and 3. Stories with 5N1K and a picture: 3 and 4. Analogies: 0 in both decks. The dividers (4 and 5) hold concept names only. Speaker notes are 31 to 98 words. A resources slide and slide numbers are present. "
         "Ranked page defects: (1) Playground select width and raw code; (2) no slide-ordered chapter-code tab, and the slide code needs the chapter library the page lacks; (3) the tab bar repeats the tree; (4) group panes stack concepts with no panel level below the group; (5) Lecture and Stories flow over 4 to 7 screens. "
         "Ranked deck defects: (1) code slides are transcripts plus captions with no visual result; (2) no analogies; (3) thin coverage of the 111 concepts; (4) dividers are names only; (5) charts are sparse; (6) page and deck code do not correspond.")
STD = ("WRITTEN STANDARD (the owner's standing teaching-material rules, from his recorded preferences; each element is measurable and none is a taste). "
       "DECK: (D1) every slide is numbered; (D2) no long paragraph: no text box over 30 words, full sentences allowed (python-pptx 1.0.2 count); (D3) every code slide carries an explanation beside the code (each line group has a plain-language note) and the executed result as a visualization, not REPL text (100 percent of code slides); "
       "(D4) every key concept has an everyday analogy (100 percent of the chapter's key concepts, listed in the research); (D5) every story follows 5N1K (who, what, when, where, why, how) with real names, a real picture and a live further-reading link; (D6) every chart is a native chart object, never a picture; "
       "(D7) speaker notes are short (at most 60 words per slide); (D8) a resources slide with links (community, corpus, seminal works, tutorials, videos); (D9) one consistent background scheme, no switching between dark and light mid-deck; (D10) each divider names its concepts with one line of meaning and one visual; "
       "(D11) the deck covers the chapter's concepts of the research (coverage counted against the research's concept list, and the result stated); (D12) the code blocks do not wrap. "
       "PAGE: (P1) no horizontal overflow at 390 px and at 1366 px (Playwright 1.56.0 measures scrollWidth); (P2) the chapter-code tab lists the deck's code examples by NAME, in the deck's slide order, each one runnable in the page with the chapter library defined in the page, and the code in the editor not in the list; "
       "(P3) the tab bar and the left tree are synchronised and their label sets are disjoint, or the tab bar is a single row; (P4) no third level of tabs; one more level of panels in the hierarchy so that one panel holds one concept; (P5) a panel fits the screen without scrolling (height at most 1.0 screen at 1366x768, stated measure); "
       "(P6) no duplicated list on a screen; (P7) every diagram has zoom; (P8) the menu is uncrowded; (P9) text size control and adaptive layout on phone, tablet and large screens; (P10) executed code results are visualized; (P11) the page and the deck carry the same code and the same look. "
       "The existing page tests 9.34.1 and 9.35.1, the deck match check, the Stage 4 gates and the chapter checks still pass on the rebuilt page; no existing gate, test, template or threshold is edited or weakened.")
PLAN = ("PLAN. Route: the deliverable (rebuilt decks and pages of chapters 5 and 6, a chapter-code tab, a panel level) is new content on units that are Done (ST_Deck_Ch05, ST_Deck_Ch06, ST_Page_Ch05, ST_Page_Ch06 stay Done and are not edited, G125 and G133); the lineage is in its InProgress state after the closure of the Backlog stage, so new deliverables on a closed scope are a StageRevision from the Scope stage (G127), the same route as ex:CR3_Pages (seven versions: change, retraction, four stages, work begun; about two hours of builder time). "
        "Stories (one acceptance criterion per unit, G133; each criterion names the tool and its version, G136): ST_Remedy_Template (a new page template version and new page-test versions as NEW files for the panel level, the single tab row or disjoint tabs, the chapter-code tab with its runnable chapter library, and the Playground by name; old files kept byte-identical; measured against the stored results of the shipped pages as in ex:ST_Page_Gates); "
        "ST_Remedy_Deck_Ch05, ST_Remedy_Deck_Ch06 (decks rebuilt as new files against D1 to D12), ST_Remedy_Page_Ch05, ST_Remedy_Page_Ch06 (pages rebuilt as new files against P1 to P11). Tasks with dependencies: template and test (T1) in parallel with deck ch5 (T2); deck ch6 (T3) after T2 starts; page ch5 (T4) needs T1 and T2 Done; page ch6 (T5) needs T1 and T3; a Verify task per deliverable on the evidence bridge (serially, about 10 minutes per page-test run). "
        "The deck rebuild comes before the page's chapter-code tab, which must match the deck's code order. Chapters 5 first, then 6. No executor brief is generated before the revision has closed its stages and the facts above are in the register. "
        "Iteration: a new iteration (Iter_17; the goal of Iter_16 is frozen and is not edited). Realistic duration (estimate, not a measurement): template and tests 4 to 5 hours, deck ch5 3 to 4 hours (parallel), page ch5 2 to 3 hours with two serial page-test runs, control about 1 hour per chapter; chapter 5 ready about 9 to 10 hours after the executors start, chapter 6 about 4 hours later; the machine has 2 cores, so browser tests run one at a time and builds do not run beside them, and the chapter 10 control shares that machine. "
        "Proposed end: Friday 2026-10-23 12:00 Istanbul (09:00 UTC), with chapter 5 delivered first; the end is the owner's, and the one thing the rules do not settle is the hour of tomorrow's class. "
        "Not in the plan: any change of content outside chapters 5 and 6, the Mission outcome and the Achieved status (the owner's act), the ch10 and ch11 section-link work (it continues in Iter_14 and Iter_16 and yields the machine to this work where they collide).")


def main():
    if sys.argv[1:] != ["change"]:
        raise SystemExit(__doc__)
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    cr = ('\nex:CR3_Remedy56 a backlog:ChangeRequest ;\n    rdfs:label "Remedy the weaknesses of the chapter 5 and chapter 6 decks and interactive pages, and deliver both ready to use"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR_SEN0401, ex:CR3_Pages ;\n'
          '    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % lit(
        OWNER_ACT + " The change grows the scope: the third lineage's scope names a deck and a page for every chapter, and the owner finds the delivered ones of chapters 5 and 6 below the standards of teaching material; "
        "the work is new deliverables beside the Done ones. Pending until the ScopeChange that admits the stories is recorded in the Backlog version.")
    ia = ('\nex:IA3_Remedy56 a backlog:ImpactAssessment ;\n    rdfs:label "What remedying the chapter 5 and chapter 6 decks and pages costs, with the facts measured before it is started"@en ;\n'
          '    backlog:analyzesRequest ex:CR3_Remedy56 ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_Pages, ex:IA3_PageGates ;\n    backlog:hasImpactStatement %s .\n') % lit(
        FACTS + " " + STD + " " + PLAN + " What moves: the digests of the Scope, Goal, Objective and Backlog stages of the third lineage move once, when the stages are closed again; no Done story is re-dated or re-opened; the first and second lineages are not touched. "
        "Risks: the page template change touches the shared template, so every shipped page is compared with its stored result again by the regression pattern of ex:AC3P_Regression (the new files only; the old ones stay); the deck of chapter 5 or 6 may not reach full concept coverage in the time, in which case the coverage is stated as measured and not claimed. "
        "A criterion that fails is named failing and its story is not Done; nothing is waived.")
    nt = t + cr + ia
    print(os.path.basename(M.write_new(src, nt, nxt, cur, "ChangeRequest ex:CR3_Remedy56 (Pending) and ImpactAssessment ex:IA3_Remedy56 for the owner's messages of 2026-10-22 17:27 and 17:30 Istanbul on the chapter 5 and 6 decks and pages: measured facts, written standard, plan; no stage changed in this version.")))


main()
