#!/usr/bin/env python3
"""sen0401_lineage_remedy56_rev v1_0_0 - the StageRevision from the Scope stage (ruling G127) for the change request ex:CR3_Remedy56 (the owner's messages of 2026-10-22 17:27 and 17:30 Istanbul on the chapter 5 and 6 decks and pages),
after sen0401_lineage_remedy56 v1_0_0 recorded the request and its impact assessment. Rulings G113, G120, G125, G127, G129, G133, G134, G136. One call = one new file = one event; the caller validates and commits each alone.
Events, in order: retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV. Nothing is begun here: work begun is recorded at the real start of each executor session."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import types
R = types.ModuleType("remedy56_constants"); R.__file__ = os.path.abspath(__file__)      # the constants of v1_0_0 (that file runs its event at import, so it is read up to its main())
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0401_lineage_remedy56_v1_0_0.py"), encoding="utf-8").read().split("def main():")[0], "remedy56_v1", "exec"), dict(R.__dict__, __file__=__file__) if False else R.__dict__)

lit, esc = G.lit, M.esc
ITER = "ex:Iter_17"; REV = "ex:Revision_Lineage3_Scope5"; CR = "ex:CR3_Remedy56"; IA = "ex:IA3_Remedy56"
ACTIVE = ["ex:Out3_ScopeR5", "ex:Out3_GoalR5", "ex:Out3_ObjectiveR5", "ex:Out3_BacklogR7"]; NEWB = "ex:Out3_BacklogR8"
WHEN = "Thursday 2026-10-22 17:27 and 17:30 Istanbul (14:27 and 14:30 UTC), as relayed by the course coordinator"
OWNER_ACT = R.OWNER_ACT
END = "2026-10-23T09:00:00"        # proposed end: Friday 12:00 Istanbul (the owner's to decide)
VER = ("deck standard check v1_0_0 (python-pptx 1.0.2); page test 9.36.0 (Playwright 1.56.0, new file over 9.35.1: the features of 9.35.1 unchanged, new features added); page tests 9.34.1 and 9.35.1; page template 9.52.0 (new file over 9.51.1); page builder v4_15_0 and page-data builder v2_24_0 (new files); "
       "Stage 4 gate runner v1_1_0 reading the CURRENT RDODI validator v1.13.0; chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; deck match check v1_0_0; page check wrapper v1_3_0; Playwright 1.56.0")
COMMON = ("A committed file is never edited: every output is a new file with a new version number. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. "
          "The machine has 2 cores: browser tests run one at a time and no build runs beside them.")
DOMC = ("DOM CONTRACT shared by the template, the page test and the page tasks (so the independent test can find what the template builds): the chapter-code tab is the tab with attribute data-pane=\"chaptercode\"; its list items have data-cc-item, the NAME of the example in data-cc-name and the deck's order number in data-cc-order; "
        "an item opens the example in the editor element data-cc-editor with a run button data-cc-run and a result element data-cc-result; the left tree items have role=treeitem and the tabs role=tab; one concept panel is an element with data-panel; the playground list items have data-pg-item and show names only; "
        "a page that follows the standard declares <meta name=\"page-standard\" content=\"9.52\">.")
STD_D = ("DECK STANDARD (checked by the deck standard check, python-pptx 1.0.2, one named result per element): D1 every slide is numbered; D2 no text box over 30 words; D3 every code slide has a plain-language explanation beside the code and the executed result as a visual (a native chart, a table or a drawn diagram), not REPL text; "
         "D4 every key concept of the chapter has an everyday analogy slide or box (the key concepts are listed in the chapter research); D5 every story has who, what, when, where, why and how, a real picture and a live link; D6 every chart is a native chart object, no chart picture; D7 speaker notes at most 60 words per slide; "
         "D8 a resources slide with links; D9 one background scheme, no dark/light switching mid-deck; D10 every divider names its concepts with one line of meaning and one visual; D11 coverage: the share of the chapter research concepts that appear on a slide, stated as measured, not below 90 percent; D12 no code line wraps.")
STD_P = ("PAGE STANDARD (checked by the new page test 9.36.0, Playwright 1.56.0): P1 no horizontal overflow at 390 px and at 1366 px; P2 the chapter-code tab lists the deck's examples by NAME in the deck's slide order, each runnable in the page with the chapter library defined in the page and its result visualised, "
         "and the code lives in the editor, not in the list; P3 tabs and left tree are synchronised and their label sets are disjoint or the tab bar is one row; P4 no third level of tabs, and one more level of panels so that one panel holds one concept; P5 a panel is at most 1.0 screen high at 1366x768; "
         "P6 no list repeated on one screen; P7 every diagram has zoom; P8 the top-level menu is uncrowded (at most 8 top-level tabs); P9 a text-size control and an adaptive layout at 390, 768 and 1366 px; P10 executed code results are visualised; P11 the page declares the standard and the examples equal the deck's code manifest.")
FACT_SHORT = R.FACTS
TOOLS = [("TS_DeckStdCheck", "sen0401_deck_standard_check_v1_0_0.py", "deck standard check v1_0_0 (python-pptx 1.0.2; the elements D1 to D12 of the deck standard, one named result each)"),
         ("TS_PageTest36", "sen0401_page_test_v9_36_0.py", "page test 9.36.0 (Playwright 1.56.0; new file over 9.35.1: all features of 9.35.1 unchanged, plus the features P1 to P6, P8, P9, P11 of the page standard)"),
         ("TS_PageTemplateC", "course_page_template_v9_52_0.html", "page template 9.52.0 (new file over 9.51.1: panel level, tab/tree rule, chapter-code tab, playground by name)"),
         ("TS_PageBuilder415", "sen0401_page_build_v4_15_0.py", "page builder v4_15_0 (new file over v4_14_0)"),
         ("TS_PageData224", "sen0401_page_data_v2_24_0.py", "page-data builder v2_24_0 (new file over v2_23_0: the chapter-code manifest and the panel data)"),
         ("TS_PageCheck3", "sen0401_lineage_page_check_v1_3_0.py", "page check wrapper v1_3_0 (written by the builder session for the control, never run by an executor)")]
BASE = ["TS_Stage4Gates", "TS_ChapterCheck", "TS_DeckMatch", "TS_RdodiValidatorCurrent", "TS_RdodiValidatorPinned", "TS_PageTest34b", "TS_PageTest35b"]
NEW = [x[0] for x in TOOLS]

# task: id, title, type, deps, session, estimated start (hours after the executors start, T0), estimated hours, note
TASKS = [
 ("TK_Remedy_DeckCheck", "Write the deck standard check and measure the two existing decks with it", "Build", [], "SEN0401-I17-deckcheck", "T0", 1.5,
  "Write the NEW file 08-tooling/sen0401_deck_standard_check_v1_0_0.py (python-pptx 1.0.2): one named, exit-coded result per element D1 to D12 of the deck standard, for a deck given by chapter number, printing the measured number for each. " + STD_D + " "
  "Define each element's measure in the file header (words per text box, what counts as a code slide, an analogy marker, a native chart, a story with 5N1K, coverage against the chapter research concept list 03-materials/chNN/rdodi). Prove it by running it on the two existing decks (chapters 5 and 6, newest files): it must reproduce the measured facts "
  "(chapter 5: 23 slides, 9 code slides, 1 native chart, 0 analogies, longest box 39 words; chapter 6: 26 slides, 13 code slides, 3 native charts, 0 analogies, longest box 56 words) and report the failing elements, which is the baseline. Keep the logs. Do not judge your own deck: you do not build a deck in this iteration. " + COMMON),
 ("TK_Remedy_PageTest", "Write page test 9.36.0 with the page-standard features and measure the two existing pages with it", "Build", [], "SEN0401-I17-pagetest", "T0", 3.0,
  "Write the NEW file 08-tooling/sen0401_page_test_v9_36_0.py from sen0401_page_test_v9_35_1.py (which stays byte-identical): every feature of 9.35.1 stays textually identical; add the features P1, P2, P3, P4, P5, P6, P8, P9 and P11 of the page standard, which apply to a page that declares the standard (meta page-standard 9.52) and are reported as SKIP with the reason 'page does not declare the standard' otherwise; "
  "an environment switch FORCE_STANDARD=1 applies them to any page. " + STD_P + " " + DOMC + " Show: a unified diff against 9.35.1, and the proof that the set of old feature texts is equal. Baseline: run it with FORCE_STANDARD=1 on the two existing pages (chapters 5 and 6, newest files; the key-substituted TEST copy by the runner sen0401_lineage_page_test_run_v1_2_0.py) "
  "and keep the logs: the failing features must name the measured defects (the playground select wider than its container: 4861 px and 5836 px; no chapter-code tab; 8 of 8 tab labels repeating the tree labels; panels taller than a screen). " + COMMON),
 ("TK_Remedy_Template", "Make page template 9.52.0 with the panel level, the tab and tree rule, the chapter-code tab and the playground by name", "Build", [], "SEN0401-I17-template", "T0", 4.5,
  "Write the NEW files course_page_template_v9_52_0.html (from v9_51_1, which stays byte-identical), sen0401_page_build_v4_15_0.py (from v4_14_0) and sen0401_page_data_v2_24_0.py (from v2_23_0). The owner's defects (quoted in ex:CR3_Remedy56): the playground list extends outside the page and shows code, not names; chapter code is not listed; multiple concepts stack on one page; the tab bar repeats the left tree and wraps. "
  "The template must: (1) show the playground as a list of NAMES that fits its container at 390 and 1366 px, the code opening in the editor; (2) add the chapter-code tab fed by the chapter-code manifest of the page data (an ordered list of named examples, each runnable with the chapter library defined in the page; FIRST establish as a fact how the page runs code today and what runtime the chapter library needs, and report it); "
  "(3) add one more level to the hierarchy: a group holds panels, one concept per panel, the panel at most one screen high; (4) tabs show only the sub-menus of the selected tree item, never the tree's own folder labels again, and never a third tab level (a breadcrumb instead); (5) keep every existing behaviour, id and test hook of 9.51.1 and add the DOM contract. " + DOMC + " "
  "The page-data builder reads the manifest file 03-materials/chNN/page/chapter_code_chNN_v*.json (written by the deck task of that chapter; if it is absent the page has no chapter-code tab) and the panel structure from the research. Build scratch copies of chapters 1 and 10 on the new template with the new builders outside the repository and show they build. "
  "Do NOT write the page test or judge your own work: the independent test is the task TK_Remedy_PageTest. " + COMMON),
 ("TK_Remedy_Regress", "Measure the new template against the old tests on a control set of pages built from it", "Verify", ["TK_Remedy_Template", "TK_Remedy_PageTest"], "builder", "T0+4.5h", 1.0,
  "After the template (TK_Remedy_Template) and the page test 9.36.0 (TK_Remedy_PageTest) are Done: build the pages of chapters 1 and 10 into a scratch folder on the template 9.52.0 with the new builders and run the page tests 9.34.1 and 9.35.1 on each (serially, a run is about nine minutes, every run kept): each result must equal or beat the stored result of the shipped page; "
  "and run 9.36.0 with FORCE_STANDARD=1 on them. Justification of the control set: the new template is a new file used only by pages built from it; the shipped pages stay on their files and are not rebuilt, so their results cannot move; the set shows the new template keeps the behaviour the old tests measure on a page with mentions (chapter 1) and a page with section links (chapter 10). " + COMMON),
]
for nn, nm in (("05", "Ch05"), ("06", "Ch06")):
    ch = nn.lstrip("0")
    TASKS += [
     ("TK_Remedy_Deck_%s_Build" % nm, "Rebuild the deck of chapter %s against the deck standard and give it its chapter-code manifest" % ch, "Build", [], "SEN0401-I17-deck-ch%s" % nn, "T0", 5.0 if nn == "05" else 5.5,
      "Build the deck of chapter %s as a NEW file with a new version number from the chapter research and the earlier deck's assets, to the deck standard. The owner's words (quoted in ex:CR3_Remedy56): the deck is very poor in content, only lists codes with sub shapes and concept names, cannot be presented nor understood. " % ch + STD_D + " "
      "Rules from the owner's standing teaching-material preferences: full sentences are fine but no long paragraphs; explanation beside every code listing; the executed result shown as a visualization (native chart, table or drawn diagram) next to each listing; an everyday analogy for each key concept; 5N1K stories with real names, a real picture and a live link; native charts only; numbered slides; a resources slide; short speaker notes; a smooth colour scheme. "
      "ALSO write the chapter-code manifest 03-materials/ch%s/page/chapter_code_ch%s_v1_0_0.json: the ordered list of the deck's code examples (order number = slide order, a short NAME, the code that runs in the page with the chapter library it needs, the expected result), because the page tab must list the same examples in the same order. The deck generator is a NEW tool file; the checker is the independent TK_Remedy_DeckCheck (not yours): run it when it exists and report every element as printed. " % (nn, nn) + COMMON),
     ("TK_Remedy_Deck_%s_Verify" % nm, "Verify the deck of chapter %s against the deck standard" % ch, "Verify", ["TK_Remedy_Deck_%s_Build" % nm, "TK_Remedy_DeckCheck"], "builder", "T0+%sh" % ("5.0" if nn == "05" else "5.5"), 0.5,
      "Run the deck standard check v1_0_0 for chapter %s, the Deck chapter check v1_3_0, the deck match check, and read the deck slide by slide (the reading by the three roles of the owner's preference - teaching academician, reviewing faculty specialist, student - is recorded as a reading, not as a tool result); record every result as printed. " % ch),
    ]
for nn, nm in (("05", "Ch05"), ("06", "Ch06")):
    ch = nn.lstrip("0")
    TASKS += [
     ("TK_Remedy_Page_%s_Build" % nm, "Rebuild the page of chapter %s on the new template with the chapter-code tab" % ch, "Build",
      ["TK_Remedy_Template", "TK_Remedy_PageTest", "TK_Remedy_Deck_%s_Verify" % nm], "SEN0401-I17-page-ch%s" % nn, "T0+%sh" % ("5.5" if nn == "05" else "6.0"), 3.0,
      "Build the page of chapter %s as a NEW file with a new page version on the template 9.52.0 with the page builder v4_15_0 and the page-data builder v2_24_0 (state how you passed the template), from the chapter research, the deck's lecture export and stories, and the deck's chapter-code manifest. "
      "Run the page tests 9.36.0, 9.34.1 and 9.35.1 (the runner with PAGE_TEST), serially, store the result as a new test_results file, and build the Stage 4 page ABox with the Stage 4 builder. " % ch + STD_P + " " + DOMC + " " + COMMON),
     ("TK_Remedy_Page_%s_Verify" % nm, "Verify the page of chapter %s against the page standard" % ch, "Verify", ["TK_Remedy_Page_%s_Build" % nm], "builder", "T0+%sh" % ("8.5" if nn == "05" else "9.0"), 1.0,
      "Re-run serially the page tests 9.36.0, 9.34.1 and 9.35.1, the Stage 4 gate runner v1_1_0, the Research, Deck and Page chapter checks, the deck match check, the link check and the manifest equality (the chapter-code tab equals the deck's code order); record every result as printed."),
    ]
IDS = {t[0]: t for t in TASKS}
STORIES = [
 ("ST_Remedy_Tools", "The page standard and the deck standard are measured by new tools and a new page template, as new files, without moving any existing gate", "Del3_Remedy56Tools", "Obj3_Remedy56Pages",
  ["AC4R_DeckCheck", "AC4R_PageTest", "AC4R_Template", "AC4R_Regress"], ["TK_Remedy_DeckCheck", "TK_Remedy_PageTest", "TK_Remedy_Template", "TK_Remedy_Regress"]),
 ("ST_Remedy_Deck_Ch05", "The deck of chapter 5 meets the deck standard and is ready to teach", "Del3_Remedy56Decks", "Obj3_Remedy56Decks", ["AC4R_Deck_Ch05"], ["TK_Remedy_Deck_Ch05_Build", "TK_Remedy_Deck_Ch05_Verify"]),
 ("ST_Remedy_Page_Ch05", "The page of chapter 5 meets the page standard and is ready to use", "Del3_Remedy56Pages", "Obj3_Remedy56Pages", ["AC4R_Page_Ch05"], ["TK_Remedy_Page_Ch05_Build", "TK_Remedy_Page_Ch05_Verify"]),
 ("ST_Remedy_Deck_Ch06", "The deck of chapter 6 meets the deck standard and is ready to teach", "Del3_Remedy56Decks", "Obj3_Remedy56Decks", ["AC4R_Deck_Ch06"], ["TK_Remedy_Deck_Ch06_Build", "TK_Remedy_Deck_Ch06_Verify"]),
 ("ST_Remedy_Page_Ch06", "The page of chapter 6 meets the page standard and is ready to use", "Del3_Remedy56Pages", "Obj3_Remedy56Pages", ["AC4R_Page_Ch06"], ["TK_Remedy_Page_Ch06_Build", "TK_Remedy_Page_Ch06_Verify"]),
]


def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = (OWNER_ACT + " The work adds deliverables (rebuilt decks and pages of chapters 5 and 6, a new page template, a new page test and a deck check, all as new files); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). "
              "The change request ex:CR3_Remedy56 and the impact assessment ex:IA3_Remedy56 were recorded first (v0.186). This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; "
              "the goals, objectives, stories and tasks already in the register, Done ones included, re-enter by admission and are not re-dated. The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). "
              "Recorded as decided by the builder role: the route is what the owner's direction needs; the stage revision itself he did not decide.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the chapter 5 and chapter 6 decks and pages are remedied"@en ;\n'
         '    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (
        REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the chapter 5 and 6 remedy: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Scoped")
    L = ['''
ex:Area3_Remedy56 a backlog:ScopeArea ;
    rdfs:label "The decks and interactive pages of chapters 5 and 6, and the tools that measure the teaching-material standard"@en ;
    backlog:belongsToLineage ex:Lineage3 ;
    backlog:areaLocation "03-materials: the deck and page folders of chapters 5 and 6; 08-tooling: the new template, builders, page test and deck check as new files" ;
    backlog:areaMeasure "chapters of 14 whose deck and page meet the written teaching-material standard: 0 of 2 (chapters 5 and 6) today; after the work 2" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del3_Remedy56Tools a backlog:ScopeDeliverable ;
    rdfs:label "A deck standard check, a page test with the page-standard features, and a page template 9.52.0 with its builders, as new files with the old ones kept"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%(cl)s"^^xsd:string ;
    backlog:hasDeliverableText %(tools)s ;
    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del3_Remedy56Decks a backlog:ScopeDeliverable ;
    rdfs:label "The decks of chapters 5 and 6 rebuilt to the deck standard, each with its chapter-code manifest"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%(cl)s"^^xsd:string ;
    backlog:hasDeliverableText %(decks)s ;
    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del3_Remedy56Pages a backlog:ScopeDeliverable ;
    rdfs:label "The pages of chapters 5 and 6 rebuilt to the page standard, with the chapter-code tab in the deck's order"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%(cl)s"^^xsd:string ;
    backlog:hasDeliverableText %(pages)s ;
    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Scope3 backlog:requiresDeliverable ex:Del3_Remedy56Tools, ex:Del3_Remedy56Decks, ex:Del3_Remedy56Pages ;
    backlog:coversArea ex:Area3_Remedy56 ;
    rdfs:seeAlso ex:CR3_Remedy56, ex:IA3_Remedy56 .
ex:Scope3 rdfs:comment %(sc)s@en .
ex:Excl3_NoGateChange rdfs:comment %(ex1)s@en .
ex:Excl3_NoConceptGates rdfs:comment %(ex2)s@en .
''' % dict(cl=T.CLAUSE,
           tools=lit("(1) the deck standard check v1_0_0 (a new file, python-pptx 1.0.2) that measures the elements D1 to D12 and reproduces the measured facts on the two existing decks; (2) the page test 9.36.0 (a new file over 9.35.1, which stays unchanged; every old feature identical, new features for the page standard) that fails the two existing pages on the measured defects; "
                     "(3) the page template 9.52.0, the page builder v4_15_0 and the page-data builder v2_24_0 (new files over 9.51.1, v4_14_0 and v2_23_0, which stay unchanged); (4) a control set of pages built from the new template that gives the old tests their stored result. " + R.STD),
           decks=lit("The decks of chapter 5 and chapter 6 rebuilt as new files that pass every element D1 to D12 of the deck standard, each with the chapter-code manifest of its code examples in slide order. " + STD_D + " " + R.FACTS),
           pages=lit("The pages of chapter 5 and chapter 6 rebuilt as new files on the template 9.52.0 that pass the page test 9.36.0 and the page tests 9.34.1 and 9.35.1, the Stage 4 gate runner and the chapter checks, with the chapter-code tab in the deck's order. " + STD_P),
           sc=lit("Revised 2026-10-22 by the stage revision %s on the owner's messages of %s (quoted in the change request ex:CR3_Remedy56). The statement above is unchanged (L-112). It now also requires ex:Del3_Remedy56Tools, ex:Del3_Remedy56Decks and ex:Del3_Remedy56Pages and covers the area ex:Area3_Remedy56." % (REV.replace("ex:", ""), WHEN)),
           ex1=lit("Note 2026-10-22: the exclusion of any change to a gate, a test or a threshold is lifted for exactly the new files named in ex:Del3_Remedy56Tools (a new page template, new builders, a new page test that only ADDS features and keeps every feature of 9.35.1, and a new deck check), by the owner's words of %s naming the defects they measure (ex:CR3_Remedy56). No existing file, gate, test, threshold or criterion is edited or weakened; the old files stay as comparison. The exclusion stands for everything else." % WHEN),
           ex2=lit("Note 2026-10-22: stands unchanged for the concept-inventory gates; the deck standard element D11 (coverage) is a new measure of its own and does not change them.")),
    ]
    t += "".join(L)
    return t + SL.out_new(t, "Scope", "Out3_ScopeR6", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the chapter 5 and 6 remedy: three deliverables (tools; decks; pages), their area, and the exclusion of gate changes lifted for the named new files only."


def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR6", prev); t = X.set_status(t, "LS_Goaled")
    intent = ('ex:%s rdfs:comment "Drafted by the builder session on 2026-10-22 from the owner\'s messages of ' + WHEN + ' (quoted in the change request ex:CR3_Remedy56); the intent origin is therefore Derived."@en .\n')
    GL = [("G3_Remedy56Decks", "The decks of chapters 5 and 6 are rich, presentable and understandable, to the written deck standard", "Del3_Remedy56Decks"),
          ("G3_Remedy56Pages", "The pages of chapters 5 and 6 are usable in class: the code lists by name in the deck's order, one concept per panel, no duplicated menu, no overflow", "Del3_Remedy56Pages")]
    L = []
    for gid, label, dl in GL:
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label %s@en ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;\n    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalOrigin backlog:GoalOrigin_New ;\n'
                 '    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;\n    backlog:hasGoalRationale %s ;\n    backlog:producedByStage ex:Out3_GoalR6 .\n' % (gid, lit(label), lit("Derived from the revised scope (ex:%s) and from the owner's messages of %s, quoted in ex:CR3_Remedy56: \"I want you to remedy the weaknesses and provide me Chapter 5 and 6 PPT and Interactive pages ready to use.\"" % (dl, WHEN))))
        L.append(intent % gid)
    for k, gid, what, text in (("D", "G3_Remedy56Decks", "a deck meets the teaching standard", STD_D), ("P", "G3_Remedy56Pages", "a page meets the teaching standard", STD_P)):
        L.append('''
ex:Spec3R_%(k)s a backlog:Specification ;
    rdfs:label "What it is for %(w)s"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:%(g)s ;
    backlog:hasSpecificationText %(tx)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR6 .
ex:Scen3R_%(k)s_Passes a backlog:TestScenario ; rdfs:label "A rebuilt chapter %(w2)s passes every element of the standard when measured"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3R_%(k)s ;
    backlog:hasScenarioText "Given the rebuilt file of chapter 5 or 6, when the check of the standard is run, then every element is met, nothing is skipped, and the run exits 0." .
ex:Scen3R_%(k)s_NotClaimed a backlog:TestScenario ; rdfs:label "An existing chapter %(w2)s that fails an element is named failing and not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3R_%(k)s ;
    backlog:hasScenarioText "Given the existing chapter 5 or 6 file (measured 2026-10-22), when the check of the standard is run on it, then the failing elements are named and the story carries no passing result for it." .
''' % dict(k=k, g=gid, w=what, w2="deck" if k == "D" else "page", tx=lit(text)))
    L.append('''
ex:Model3R_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the rebuilt chapter 5 and 6 materials"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The instructor presents the deck of the chapter in class and opens the page of the chapter on the same code, in the same order, with the same look; a student runs each deck example from the chapter-code tab on a phone or a laptop, changes it and sees the result visualised, and finds one concept per panel without scrolling through a stack of concepts; independent checks (the deck standard check, the page test 9.36.0) measure the standard; the evidence bridge verifies the runs; the owner reads the register to see which chapter materials are ready." ;
    backlog:describesItem ex:G3_Remedy56Pages .
''')
    t += "".join(L)
    return t + SL.out_new(t, "Goal", "Out3_GoalR6", "Out3_ScopeR6"), "third lineage, Goal stage rebuilt for the chapter 5 and 6 remedy: a goal for the decks and a goal for the pages, each with a specification (the standard) and a nominal and a rejection scenario; the use case model."


def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR6", prev); t = X.set_status(t, "LS_Objectived"); now = M.now(); L = []
    for oid, gid, mid, what, b, tg in (("Obj3_Remedy56Decks", "G3_Remedy56Decks", "Met3_Remedy56Decks", "decks of chapters 5 and 6 that pass every element of the deck standard check", 0, 2),
                                       ("Obj3_Remedy56Pages", "G3_Remedy56Pages", "Met3_Remedy56Pages", "pages of chapters 5 and 6 that pass the page test 9.36.0 and the page tests 9.34.1 and 9.35.1", 0, 2)):
        L.append('''
ex:%(i)s a backlog:Objective ; rdfs:label "%(Wh)s: from 0 to 2"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:%(g)s ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:%(m)s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %(w)s, read from the runs of the checks on the newest files after the evidence bridge has run them." ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "2"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3R_%(i)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR6 .
ex:%(m)s a backlog:Metric ; rdfs:label "%(w)s"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3R_%(i)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the chapter 5 and 6 materials are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria of chapters 5 and 6 on the rebuilt files, so the count is read from verified runs." ;
    backlog:expectedValue "2"^^xsd:decimal .
ex:Obs43_%(i)s a backlog:MetricObservation ; rdfs:label "Baseline, before any work on the remedy"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(i)s ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Baseline from the measured facts of 2026-10-22 recorded in ex:IA3_Remedy56 (Playwright 1.56.0, python-pptx 1.0.2): the existing decks and pages of chapters 5 and 6 fail the standard (code as playground labels, no chapter-code tab, 8 of 8 duplicate tab labels, 0 analogies, REPL transcripts as results): 0 of 2 pass." .
ex:%(i)s rdfs:comment "Drafted by the builder session on 2026-10-22 from the owner's messages of %(wh)s (ex:CR3_Remedy56); the intent origin is therefore Derived."@en .
''' % dict(i=oid, g=gid, m=mid, w=esc(what), Wh=esc(what[0].upper() + what[1:]), now=now, wh=WHEN))
    t += "".join(L)
    return t + SL.out_new(t, "Objective", "Out3_ObjectiveR6", "Out3_GoalR6"), "third lineage, Objective stage rebuilt for the chapter 5 and 6 remedy: two objectives (decks and pages that pass the standard, 0 to 2) with metrics, checkpoints and a baseline reading of 2026-10-22."


def gh_tool(c):
    if c == "AC4R_DeckCheck":
        return ("Owner-directed work (ex:CR3_Remedy56). Given the existing decks of chapters 5 and 6, when the NEW file sen0401_deck_standard_check_v1_0_0.py is written and run on them, then ALL of: (1) the file is new and no committed file is edited; (2) it reports one named exit-coded result for each element D1 to D12 of the deck standard and prints the measured number; "
                "(3) on the existing decks it reproduces the measured facts - chapter 5: 23 slides, 9 code slides, 1 native chart, 0 analogies, longest text box 39 words; chapter 6: 26 slides, 13 code slides, 3 native charts, 0 analogies, longest box 56 words - and names the failing elements (D3, D4, D10 and D11 at least), exit non-zero; "
                "(4) the header defines each measure (what is a code slide, an analogy, a story with 5N1K, coverage against the research concept list); (5) the logs of the runs are kept; results as printed; if any element fails the file is named failing. " + STD_D)
    if c == "AC4R_PageTest":
        return ("Owner-directed work (ex:CR3_Remedy56). Given the page test 9.35.1 (SHA-256 recorded by the executor) and the existing pages of chapters 5 and 6, when the NEW file sen0401_page_test_v9_36_0.py is written, then ALL of: (1) the file is new and 9.35.1 is byte-identical; (2) every feature text of 9.35.1 is present unchanged (the set of feat/skip texts of 9.35.1 is a subset of 9.36.0; a diff shows only added code and the version line and comments); "
                "(3) the added features P1, P2, P3, P4, P5, P6, P8, P9, P11 apply to a page that declares the standard and are reported SKIP with the reason otherwise; FORCE_STANDARD=1 applies them to any page; "
                "(4) with FORCE_STANDARD=1 on the existing pages of chapters 5 and 6 the run fails the features that name the measured defects (playground select 4861 px and 5836 px wide; no chapter-code tab; 8 of 8 repeated tab labels; panels over one screen high) and ends without a crash; (5) the logs are kept; results as printed. " + STD_P + " " + DOMC)
    if c == "AC4R_Template":
        return ("Owner-directed work (ex:CR3_Remedy56). Given the page template 9.51.1, the page builder v4_14_0 and the page-data builder v2_23_0 (all byte-identical after the task), when the NEW files course_page_template_v9_52_0.html, sen0401_page_build_v4_15_0.py and sen0401_page_data_v2_24_0.py are made, then ALL of: (1) the files are new, the old ones byte-identical; "
                "(2) the template implements the DOM contract and keeps every id and hook of 9.51.1; the report states as a fact how the page runs code today and what runtime the chapter-library examples need; (3) a scratch page of chapter 1 and of chapter 10 built on 9.52.0 declares the page standard and the page test 9.36.0 passes P1, P3, P4, P5, P6, P8, P9 on them (the chapter-code tab features apply when a manifest exists); "
                "(4) no gate, test or threshold is changed; results as printed. " + DOMC)
    if c == "AC4R_Regress":
        return ("Owner-directed work (ex:CR3_Remedy56). Given the template 9.52.0, the builders v4_15_0 and v2_24_0 and the page tests, when the pages of chapters 1 and 10 are built into a scratch folder on the new template and the page tests 9.34.1 and 9.35.1 are run on each, serially, then ALL of: "
                "(1) each of the 4 runs ends exit 0 with RESULT PASS, no [FAIL], and widgets, features and gates not below the stored result of the shipped page, skipped features not more and each of them one the stored result skips; (2) every run is kept as a log; (3) no committed file is edited, the scratch pages are not shipped; results as printed. "
                "Control set justified: the new template is a new file used only by pages built from it; the shipped pages stay on their files, so their results cannot move.")
    raise KeyError(c)


def gh_deck(nn):
    ch = nn.lstrip("0")
    return ("Owner-directed work (ex:CR3_Remedy56): the owner's 17:27 message says the deck is very poor in content and cannot be presented nor understood. Given the existing deck of chapter %s and its research, when the deck is rebuilt as a new file with a new version number and its chapter-code manifest written, then ALL of: "
            "(1) the deck standard check v1_0_0 for chapter %s reports every element D1 to D12 met and exits 0; (2) the Deck chapter check v1_3_0 for Deck/Ch%s passes and the deck match check reports 0 not carried; (3) the chapter-code manifest chapter_code_ch%s_v1_0_0.json lists the deck's code examples in slide order, by name, and the order equals the order of the code slides (measured by the deck check); "
            "(4) no committed file is edited; results as printed; if any element fails the deck is named failing and this criterion has no passing result. " % (ch, ch, nn, nn) + STD_D)


def gh_page(nn):
    ch = nn.lstrip("0")
    return ("Owner-directed work (ex:CR3_Remedy56): the owner's 17:27 message names the page defects. Given the existing page of chapter %s and the rebuilt deck of chapter %s, when the page is rebuilt as a new file with a new page version on the template 9.52.0 with the builders v4_15_0 and v2_24_0, then ALL of: "
            "(1) the page test 9.36.0 runs all its added features with no skip and passes them (P1, P2, P3, P4, P5, P6, P8, P9, P11), exit 0; (2) the page tests 9.34.1 and 9.35.1 report no failure and widgets, features and gates not below the stored result of the existing page, skipped not more; "
            "(3) the chapter-code tab equals the deck's chapter-code manifest in names and order and each example runs in the page and shows its result (measured by the page test); (4) the Stage 4 gate runner v1_1_0 for %s exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, and the Research, Deck and Page chapter checks pass; the deck match check reports 0 not carried; "
            "(5) no committed file is edited, no gate, test or threshold changed beyond the new files; the Stage 4 page ABox and the stored page-test result are new files; results as printed; if any element fails the page is named failing and this criterion has no passing result. " % (ch, ch, ch) + STD_P)


def task_block(tid, title, ttype, deps, sess, est, hrs, note):
    full = note + " Planned session %s; estimated start %s after the executors begin, about %s hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)." % (sess, est, hrs)
    return ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ; backlog:responsible %s ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:%s ;\n%s'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n'
            '    backlog:hasAuditNote %s .\n') % (tid, lit(title), tid, lit(title), ITER, NEWB, G.EXEC, "NewCapability" if ttype == "Build" else "Compliance", ttype, "Ready" if ttype == "Build" else "Proposed",
                                                 ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + d for d in deps)) if deps else "", lit(full))


def story_block(sid, title, deliv, obj, crits, tasks, note):
    return ('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
            '    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability %s ; backlog:soThat %s ;\n'
            '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion %s ;\n'
            '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible %s ;\n'
            '    backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Not scored: the owner directed this work on 2026-10-22 and uses it tomorrow, so there is no ranking left to compute." ;\n'
            '    backlog:hasAuditNote %s .\n') % (sid, lit(title), sid, lit(title), ITER, NEWB, lit(title[0].lower() + title[1:]), lit("the instructor can teach chapter 5 and 6 tomorrow from a deck and a page that meet the written standard"), deliv, obj,
                                                 ", ".join("ex:" + c for c in crits), G.EXEC, ", ".join("ex:" + x for x in tasks), lit(note))


def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR6", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput ex:Out3_BacklogR7 ;"); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput ex:Out3_BacklogR7 ;", "backlog:admittedByOutput %s ;" % NEWB)
    L = []
    for ts, fn, what in TOOLS:
        L.append('ex:%s a backlog:ToolScript ; rdfs:label %s@en ; backlog:scriptFileName "%s" ; backlog:acceptsGraphPath false .\n' % (ts, lit(what), fn))
    labels = {"AC4R_DeckCheck": "The deck standard check is a new file that reproduces the measured facts of the two existing decks and measures D1 to D12",
              "AC4R_PageTest": "The page test 9.36.0 is a new file that keeps every feature of 9.35.1 and fails the existing pages of chapters 5 and 6 on the measured defects",
              "AC4R_Template": "The page template 9.52.0 and its two builders are new files that implement the panel level, the tab and tree rule, the chapter-code tab and the playground by name",
              "AC4R_Regress": "The new template gives the old page tests the stored result on a control set of pages built from it",
              "AC4R_Deck_Ch05": "The deck of chapter 5 meets every element of the deck standard", "AC4R_Deck_Ch06": "The deck of chapter 6 meets every element of the deck standard",
              "AC4R_Page_Ch05": "The page of chapter 5 meets the page standard with the chapter-code tab in the deck's order", "AC4R_Page_Ch06": "The page of chapter 6 meets the page standard with the chapter-code tab in the deck's order"}
    tools_of = {"AC4R_DeckCheck": ["TS_DeckStdCheck"], "AC4R_PageTest": ["TS_PageTest36", "TS_PageTest35b"], "AC4R_Template": ["TS_PageTemplateC", "TS_PageBuilder415", "TS_PageData224", "TS_PageTest36"],
                "AC4R_Regress": ["TS_PageTemplateC", "TS_PageTest34b", "TS_PageTest35b"], "AC4R_Deck_Ch05": ["TS_DeckStdCheck", "TS_ChapterCheck", "TS_DeckMatch"], "AC4R_Deck_Ch06": ["TS_DeckStdCheck", "TS_ChapterCheck", "TS_DeckMatch"],
                "AC4R_Page_Ch05": NEW + BASE, "AC4R_Page_Ch06": NEW + BASE}
    cases = {"AC4R_DeckCheck": "TC3R_Tool", "AC4R_PageTest": "TC3R_Tool", "AC4R_Template": "TC3R_Tool", "AC4R_Regress": "TC3R_Tool", "AC4R_Deck_Ch05": "TC3R_D", "AC4R_Deck_Ch06": "TC3R_D", "AC4R_Page_Ch05": "TC3R_P", "AC4R_Page_Ch06": "TC3R_P"}
    for c, lab in labels.items():
        gt = gh_tool(c) if c in ("AC4R_DeckCheck", "AC4R_PageTest", "AC4R_Template", "AC4R_Regress") else (gh_deck(c[-2:]) if "_Deck_" in c else gh_page(c[-2:]))
        k = cases[c]
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
                 '    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs and the diffs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:%s_Passes, ex:%s_NotClaimed .\n'
                 % (c, lit(lab), lit(gt), ", ".join("ex:" + x for x in tools_of[c]), lit(VER), k, k))
    for tid, title, ttype, deps, sess, est, hrs, note in TASKS:
        L.append(task_block(tid, title, ttype, deps, sess, est, hrs, note))
    for sid, title, deliv, obj, crits, tks in STORIES:
        L.append(story_block(sid, title, deliv, obj, crits, tks, OWNER_ACT + " One criterion per unit (G133). The Done stories of chapters 5 and 6 (ST_Deck_Ch05, ST_Deck_Ch06, ST_Page_Ch05, ST_Page_Ch06) stay Done and are not edited (G125). " + R.FACTS))
    for k, ac in (("Tool", [c for c in labels if "_Deck_" not in c and "_Page_" not in c]), ("D", ["AC4R_Deck_Ch05", "AC4R_Deck_Ch06"]), ("P", ["AC4R_Page_Ch05", "AC4R_Page_Ch06"])):
        L.append('''
ex:TC3R_%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the checks of the criteria on the new files and require no failure and no skip"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3R_%(s)s_Passes ; backlog:runsOnData ex:Data3R_%(k)s_Passing ;
    backlog:hasCaseText "Run the checks of the criterion over the newest files; they report no failure and exit 0 (the bridge runs recorded in this register are these runs)." .
ex:TC3R_%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on an existing file that fails and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3R_%(s)s_NotClaimed ; backlog:runsOnData ex:Data3R_%(k)s_Failing ;
    backlog:hasCaseText "Run the checks over the existing deck or page of chapter 5 or 6 (measured 2026-10-22); the failing elements are named and the file carries no passing result." .
ex:Data3R_%(k)s_Passing a backlog:TestData ; rdfs:label "The rebuilt files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest rebuilt files, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3R_%(k)s_Failing a backlog:TestData ; rdfs:label "The existing chapter 5 and 6 files whose checks fail when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The decks and pages of chapters 5 and 6 as they stood on 2026-10-22 (page v9_74_0 and v9_75_0, the newest decks) with the measured defects of ex:IA3_Remedy56." .
''' % dict(k=k, s="D" if k in ("Tool", "D") else "P", cr=", ".join("ex:" + c for c in ac)))
    sid_all = [s[0] for s in STORIES]; tk_all = [x[0] for x in TASKS]
    for x in sid_all + tk_all:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, now, ITER, lit("Refined by the builder session from the owner's messages of %s (ex:CR3_Remedy56) and the measured facts of ex:IA3_Remedy56: acceptance criteria with tools and versions, dependencies, estimated start, and a brief to be generated; startable when its dependencies are Done." % WHEN)))
    for sid, title, deliv, obj, crits, tks in STORIES:
        L.append('ex:Plan3R_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 17"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3R_%s, ex:Scen3R_%s_Passes, ex:Scen3R_%s_NotClaimed .\n'
                 % (sid, sid, now, ITER, sid, ", ".join("ex:" + x for x in tks), "P" if "Page" in sid else "D", "P" if "Page" in sid else "D", "P" if "Page" in sid else "D"))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    L.append("ex:Obj3_Remedy56Decks backlog:metricMovableBy ex:ST_Remedy_Deck_Ch05, ex:ST_Remedy_Deck_Ch06 .\nex:Obj3_Remedy56Pages backlog:metricMovableBy ex:ST_Remedy_Page_Ch05, ex:ST_Remedy_Page_Ch06, ex:ST_Remedy_Tools .\n")
    SG = ("The decks and the interactive pages of chapters 5 and 6 are rebuilt as new files that meet the written teaching-material standard (the deck standard D1 to D12 and the page standard P1 to P11), measured by an independent deck check and the page test 9.36.0 and verified by the evidence bridge, chapter 5 first; "
          "each unit that fails is named failing and is not Done. No existing file, gate, test or threshold is edited. Frozen at the planning ceremony.")
    DS = ("Proposed by the builder session on 2026-10-22: the start is the instant of the planning ceremony ex:PC3_Iter_17; the proposed end is Friday 2026-10-23 09:00 UTC (12:00 Istanbul); the owner decides the end and the hour of tomorrow's class is not known to the builder. "
          "Justification (estimates, not measurements). Parallel on the 2 cores at the start (T0): the deck check (about 1.5 h), the page test (about 3 h), the template and builders (about 4.5 h), the deck of chapter 5 (about 5 h) and the deck of chapter 6 (about 5.5 h) are independent builds with python-pptx and light rendering. "
          "The heavy part is the browser tests, which run one at a time: baseline runs of the page test (2), the control set (4 runs), the page tests per page (3 each), and the builder's control runs (3 per page); about 3 hours of serial test time in all. "
          "CRITICAL PATH: deck of chapter 5 (5 h) -> its verification (0.5 h) -> page of chapter 5 (about 3 h, also needs the template and the page test) -> its verification (about 1 h) = about 9.5 h after T0 for the page of chapter 5; chapter 6 follows the same path half an hour later and its tests queue behind those of chapter 5: about 11 h. "
          "Estimated from T0 (executors start, expected about 18:15 UTC = 21:15 Istanbul if they begin at once): deck chapter 5 ready about T0+5.5 h (23:45 UTC), deck chapter 6 about T0+6 h (00:15 UTC), page chapter 5 about T0+9.5 h (03:45 UTC = 06:45 Istanbul), page chapter 6 about T0+11 h (05:15 UTC = 08:15 Istanbul) if nothing fails. "
          "The margin to the proposed end (09:00 UTC) is about 3.75 h, enough for one repeat of a page task (about 3 h) but not for two; chapter 5 is delivered about 1.5 h before chapter 6 on purpose. Whether the end serves the class is the owner's to say.")
    L.append('ex:Iter_17 a backlog:Iteration ; rdfs:label "Iteration 17: the chapter 5 and 6 decks and interactive pages remedied to the written standard"@en ; backlog:hasIdentifier "Iter_17" ; backlog:belongsToLineage ex:Lineage3 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (
        now, END, lit(DS), lit(SG), ", ".join("ex:" + x for x in sid_all + tk_all)))
    L.append('ex:PB3R_Iter_17 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 17 when it was planned"@en ; backlog:baselineFor ex:Iter_17 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (now, now, END))
    L.append('ex:PC3_Iter_17 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 17: the chapter 5 and 6 remedy"@en ; backlog:ceremonyFor ex:Iter_17 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (
        now, ", ".join("ex:Plan3R_" + s for s in sid_all), lit("Held %s by the builder session, after the owner's messages of %s (ex:CR3_Remedy56): the five stories and their 12 tasks are committed to this iteration, whose goal is frozen at its start. No executor has started; work begun is recorded at the real start of each executor session, with its brief." % (now, WHEN))))
    L.append('ex:SC3_Remedy56 a backlog:ScopeChange ;\n    rdfs:label "Scope grown by the chapter 5 and 6 decks and pages remedied, and the tools that measure the standard"@en ;\n    backlog:fulfillsRequest ex:CR3_Remedy56 ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        ", ".join("ex:" + s for s in sid_all), lit(OWNER_ACT + " The boundary moved outward by five stories; the exclusion of any change to a gate or a test is lifted only for the new files named in ex:Del3_Remedy56Tools; nothing existing is edited or weakened.")))
    t, kk = re.subn(r'(ex:CR3_Remedy56 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('ex:CR3_Remedy56 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Remedy56 and the five stories it admits; it was Pending before. The owner\'s message of %s is the direction and authorises the scope; the end of the iteration is still his."@en .\n' % (now[:10], WHEN))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR8", "Out3_ObjectiveR6"), ("third lineage, Backlog stage rebuilt for the chapter 5 and 6 remedy: five stories (tools; deck and page of chapters 5 and 6) with 12 tasks and dependencies, eight criteria with tools and versions, refinement and planning events, "
                                                                          "the new iteration Iter_17 with sprint goal, plan baseline and ceremony, and the ScopeChange that admits the stories; the change request is Accepted; the %d carried items are re-admitted by the rebuilt output, not re-dated." % n)


def ev_fill(t, prev):
    t = G.fill_re(t, NEWB, prev)
    return t, "closedAtCommit of the rebuilt Backlog output ex:Out3_BacklogR8 set to the commit that closed it (%s); the revision is complete and no work is begun." % prev


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
