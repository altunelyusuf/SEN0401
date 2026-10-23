#!/usr/bin/env python3
"""sen0401_lineage_charset_rev v1_0_0 - change route (rulings G125, G127, G133, G136) for the late character-set declaration found by the owner on the delivered chapter 5 and 6 pages (`<meta charset="utf-8">` at byte 13584, behind the first 1024 bytes). Events, one new file each: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV.
The StageRevision from the Scope stage is the same route as ex:CR3_ChipScroll (sen0401_lineage_repair_rev_v1_0_0) and ex:CR3_Remedy56. New items: template 9.52.2 (a new file) and a new check tool, and the rebuild of the chapter 5 and 6 pages on them (new files). The other pages are tracked by ex:CR3_CharsetOtherPages and a closure caveat, not rebuilt.
Work begun is recorded at the real start of each executor session, in later versions made by the work-begun tool."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_remedy56_rev_v1_0_0 as RV
lit, esc = G.lit, M.esc
ITER = "ex:Iter_19"; REV = "ex:Revision_Lineage3_Scope7"; CR = "ex:CR3_Charset"; IA = "ex:IA3_Charset"
ACTIVE = ["ex:Out3_ScopeR7", "ex:Out3_GoalR7", "ex:Out3_ObjectiveR7", "ex:Out3_BacklogR9"]; NEWB = "ex:Out3_BacklogR10"; OLDB = "ex:Out3_BacklogR9"
RV.ITER = ITER; RV.NEWB = NEWB
WHEN = "Friday 2026-10-23 09:32 Istanbul, relayed by the course coordinator (the owner's defect report on the delivered chapter 5 and 6 pages)"
FACT = ("MEASURED FACTS. The owner reports that the delivered chapter 5 and 6 pages show the label '▸\U0001f4c1Wallet keys' as 'â–¸ðŸ“\u0081Wallet keys' (UTF-8 bytes read as Windows-1252). The coordinator measured the cause: in template 9.52.1, in 9.52.0 and in all older pages built from the 9.24 line, `<meta charset=\"utf-8\">` sits at byte 13587 of the file, behind a long header comment and other meta tags; a viewer that prescans only the first 1024 bytes for a charset does not find it and guesses Windows-1252. "
        "In the pages 9.82.0 of chapter 5 and chapter 6 the tag sits at byte 13584. The other delivered pages (chapters 1 to 14 in the owner's archive) have the same defect.")
STD1 = ("PAGE FEATURE (new, measured by the new check): the file declares its character set so that a viewer which looks only at the first 1024 bytes finds it: the string `<meta charset=\"utf-8\">` occurs at a byte offset below 1024, and the first 1024 bytes decode as UTF-8 (a multibyte sequence cut by the end of the window is not an error; any other invalid byte is).")
VER = ("page template 9.52.2 (new file over 9.52.1, which stays byte-identical, as do 9.52.0 and every older template); page charset check v1_0_0 (a new tool, Python 3.13 standard library only); page builder v4_15_0 and page-data builder v2_24_0 (unchanged; the template is passed by PAGE_TEMPLATE, a builder v4_16_0 only if the builder puts anything before the template's first bytes); "
       "page test 9.36.0 (Playwright 1.56.0); page tests 9.34.1 and 9.35.1; Stage 4 gate runner v1_1_0 reading the CURRENT RDODI validator v1.13.0; chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; deck match check v1_0_0; page check wrapper v1_4_1; Playwright 1.56.0")
COMMON = RV.COMMON
NOEDIT = ("DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES: write each log once, after its run is complete, and commit it once (the control of the page 9.82.0 of chapter 5 found a log file of the executor appended in a later commit, which fails the element 'no committed file is edited').")
STORIES = [("ST_Charset_Template", "The page template 9.52.2 declares its character set within the first 1024 bytes, as a new file", "Del3_CharsetTemplate", "Obj3_Charset", ["AC6R_Template"], ["TK_Charset_Template", "TK_Charset_Template_Verify"]),
           ("ST_Charset_Check", "A check fails every page whose character set is not found within the first 1024 bytes", "Del3_CharsetTemplate", "Obj3_Charset", ["AC6R_Check"], ["TK_Charset_Check", "TK_Charset_Check_Verify"]),
           ("ST_Charset_Page_Ch05", "The page of chapter 5 is rebuilt on template 9.52.2 and declares its character set within the first 1024 bytes", "Del3_CharsetPages", "Obj3_Charset", ["AC6R_Page_Ch05"], ["TK_Charset_Page_Ch05_Build", "TK_Charset_Page_Ch05_Verify"]),
           ("ST_Charset_Page_Ch06", "The page of chapter 6 is rebuilt on template 9.52.2 and declares its character set within the first 1024 bytes", "Del3_CharsetPages", "Obj3_Charset", ["AC6R_Page_Ch06"], ["TK_Charset_Page_Ch06_Build", "TK_Charset_Page_Ch06_Verify"])]
def pagenote(nn):
    ch = nn.lstrip("0"); old = {"05": "9.82.0 (delivered; its control found one log file of the executor appended)", "06": "9.82.0 (delivered; controlled MET)"}[nn]
    return ("Build the page of chapter %s again as a NEW file with the NEW page version 9.83.0 (higher than the page %s) on the template 9.52.2 (course_page_template_v9_52_2.html, built by TK_Charset_Template; pass it with PAGE_TEMPLATE) with the page builder v4_15_0 and the page-data builder v2_24_0, from the same inputs as the page 9.82.0 "
            "(the deck's lecture export and stories, the chapter-code manifest chapter_code_ch%s_v1_1_0.json, the pywheels file where the chapter has one). Everything of the earlier build stays valid; the change is the template. " % (ch, old, nn) +
            "Run the new check on the page (python3 08-tooling/sen0401_page_charset_check_v1_0_0.py PAGEFILE; it must pass), run the page tests 9.36.0, 9.34.1 and 9.35.1 (the runner with PAGE_TEST), serially, store the result as a new test_results file, and build the Stage 4 page ABox with the Stage 4 builder. " + NOEDIT + " " + FACT + " " + RV.STD_P + " " + RV.DOMC + " " + COMMON)
TASKS = [("TK_Charset_Template", "Make page template 9.52.2: the character set is declared first, within the first 1024 bytes", "Build", [], "SEN0401-I19-template", "T0", 0.5,
          "Write the NEW file 08-tooling/course_page_template_v9_52_2.html from course_page_template_v9_52_1.html (which stays byte-identical, as do 9.52.0 and every older template). " + FACT + " "
          "THE CHANGE: `<meta charset=\"utf-8\">` becomes the very first element of the file (the first bytes), and the template's header comments, which are long, move after it, so that the declaration lies within the first 1024 bytes; the version marker comment names 9.52.2. Change nothing else: every id, hook, behaviour and the DOM contract of 9.52.1 stay; the unified diff against 9.52.1 shows only the moved charset tag and the moved comments (same lines, new order) and the version marker. "
          "The tag must stay exactly once in the file. Then build one scratch page of chapter 5 on 9.52.2 outside the repository folders (builders v4_15_0 and v2_24_0, PAGE_TEMPLATE, PAGE_SCRATCH / PAGE_DATA_OUT) and show that the byte offset of the tag in the built page is below 1024: if the page builder puts anything before the template's first bytes and the offset is not below 1024, write sen0401_page_build_v4_16_0.py as a new file over v4_15_0 and say so. "
          "PROOF to deliver and keep as logs: (1) the unified diff; (2) SHA-256 of 9.52.0, 9.52.1 and 9.52.2 before and after; (3) the byte offset of the tag in the template and in the scratch page; (4) the page test 9.36.0 on the scratch page of chapter 5 reports no failure. " + NOEDIT + " " + STD1 + " " + COMMON),
         ("TK_Charset_Template_Verify", "Verify page template 9.52.2 on the evidence bridge", "Verify", ["TK_Charset_Template"], "builder", "T0+0.7h", 0.5,
          "Re-run on the bridge: the old templates byte-identical, the diff of 9.52.2 over 9.52.1 limited to the moved charset tag, the moved comments and the version marker, every id and hook present, the tag once at an offset below 1024, a scratch page of chapter 5 built by the builder session on 9.52.2 with the tag below 1024 and the page test 9.36.0 passing; record every result as printed."),
         ("TK_Charset_Check", "Make the page charset check: fail unless the character set is declared within the first 1024 bytes and they decode as UTF-8", "Build", [], "SEN0401-I19-check", "T0", 0.5,
          "Write the NEW tool 08-tooling/sen0401_page_charset_check_v1_0_0.py (Python 3.13, standard library only): usage `python3 -B sen0401_page_charset_check_v1_0_0.py FILE...`; for each file it prints PASS or FAIL with the byte offset found, and the exit code is 0 only when EVERY file passes. A file passes only when BOTH hold: (1) the case-insensitive pattern of a meta charset declaration for utf-8 (`<meta charset=\"utf-8\">`, any quoting, spacing and case) is found within the first 1024 bytes, and (2) the first 1024 bytes decode as UTF-8; a multibyte sequence that is merely cut by the end of the 1024-byte window is NOT an error, any other invalid byte is. A missing file or no tag is FAIL, never skipped. "
          + FACT + " PROOF to deliver and keep as logs: (a) the tool FAILS (exit non-zero, offset 13584 printed) on the shipped pages 03-materials/ch05/page/sen0401_ch05_page_v9_82_0.html and 03-materials/ch06/page/sen0401_ch06_page_v9_82_0.html and on the template 9.52.1; (b) it PASSES on three small fixture files you write beside the logs (a tag at byte 0, a tag at byte 1000, and a tag at byte 0 with a UTF-8 character cut by byte 1024); (c) it FAILS on a fixture with the tag at byte 1100, on a fixture with the tag at byte 10 and an invalid byte (0xFF) before byte 1024, and on a missing file; (d) the tool does not change any file. "
          + NOEDIT + " " + STD1 + " " + COMMON),
         ("TK_Charset_Check_Verify", "Verify the page charset check on the evidence bridge", "Verify", ["TK_Charset_Check"], "builder", "T0+0.7h", 0.5,
          "Re-run on the bridge: the tool exits non-zero on the pages 9.82.0 of chapters 5 and 6 and on template 9.52.1, exits zero on the passing fixtures, exits non-zero on the failing fixtures, changes no file; record every result as printed."),
         ("TK_Charset_Page_Ch05_Build", "Rebuild the page of chapter 5 on template 9.52.2", "Build", ["TK_Charset_Template", "TK_Charset_Template_Verify", "TK_Charset_Check", "TK_Charset_Check_Verify"], "SEN0401-I19-page-ch05", "T0+1.2h", 1.5, pagenote("05")),
         ("TK_Charset_Page_Ch05_Verify", "Verify the rebuilt page of chapter 5", "Verify", ["TK_Charset_Page_Ch05_Build"], "builder", "T0+2.7h", 1.0,
          "Re-run serially the charset check and the page tests 9.36.0, 9.34.1 and 9.35.1, the Stage 4 gate runner v1_1_0, the Research, Deck and Page chapter checks, the deck match check and the manifest equality; record every result as printed."),
         ("TK_Charset_Page_Ch06_Build", "Rebuild the page of chapter 6 on template 9.52.2", "Build", ["TK_Charset_Template", "TK_Charset_Template_Verify", "TK_Charset_Check", "TK_Charset_Check_Verify"], "SEN0401-I19-page-ch06", "T0+1.2h", 1.5, pagenote("06")),
         ("TK_Charset_Page_Ch06_Verify", "Verify the rebuilt page of chapter 6", "Verify", ["TK_Charset_Page_Ch06_Build"], "builder", "T0+3.2h", 1.0,
          "Re-run serially the charset check and the page tests 9.36.0, 9.34.1 and 9.35.1, the Stage 4 gate runner v1_1_0, the Research, Deck and Page chapter checks, the deck match check and the manifest equality; record every result as printed.")]
LAB = {"AC6R_Template": "The page template 9.52.2 is a new file that declares its character set first and changes nothing else", "AC6R_Check": "The page charset check fails every page without a UTF-8 charset declaration in its first 1024 bytes and passes every page with one",
       "AC6R_Page_Ch05": "The page of chapter 5 rebuilt on template 9.52.2 declares its character set within the first 1024 bytes and passes all three page tests", "AC6R_Page_Ch06": "The page of chapter 6 rebuilt on template 9.52.2 declares its character set within the first 1024 bytes and passes all three page tests"}
def gh(c):
    if c == "AC6R_Template":
        return ("Owner-directed work (ex:CR3_Charset). Given the template 9.52.1 (byte-identical after the task) and the defect measured on the pages 9.82.0, when the NEW file course_page_template_v9_52_2.html is written, then ALL of: (1) the file is new and the templates 9.52.0 and 9.52.1 and every older template are byte-identical; (2) `<meta charset=\"utf-8\">` occurs exactly once, at a byte offset below 1024, and the first 1024 bytes decode as UTF-8; "
                "(3) the unified diff of 9.52.2 over 9.52.1 shows only the moved tag, the moved header comments (the same lines in a new order) and the version marker, and every id and hook of 9.52.1 and the DOM contract are present; (4) a scratch page of chapter 5 built on 9.52.2 with the builders v4_15_0 and v2_24_0 (PAGE_TEMPLATE) has the tag below byte 1024 and passes the page test 9.36.0 with no failure; "
                "(5) no committed file is edited, no gate, test or threshold changed; results as printed; if any element fails the template is named failing. " + FACT + " " + STD1)
    if c == "AC6R_Check":
        return ("Owner-directed work (ex:CR3_Charset). Given the pages 9.82.0 of chapters 5 and 6 (known bad) and the template 9.52.1, when the NEW tool sen0401_page_charset_check_v1_0_0.py is written, then ALL of: (1) the tool is a new file using the standard library only and changes no file; (2) it exits non-zero and prints the offset 13584 on the pages 9.82.0 of chapters 5 and 6 and prints a failure on template 9.52.1; "
                "(3) it exits zero on a fixture with the tag at byte 0, on one with the tag at byte 1000 and on one whose UTF-8 character is cut by byte 1024; (4) it exits non-zero on a fixture with the tag at byte 1100, on one with the tag at byte 10 and an invalid byte before byte 1024, and on a missing file; (5) it exits zero only when every file given passes; no committed file is edited; results as printed; if any element fails the tool is named failing. " + FACT + " " + STD1)
    nn = c[-2:]; ch = nn.lstrip("0")
    return ("Owner-directed work (ex:CR3_Charset). Given the page of chapter %s (the page 9.82.0 and its deck), when the page is rebuilt as a new file with the new page version 9.83.0 on the template 9.52.2 with the builders v4_15_0 and v2_24_0, then ALL of: (1) the charset check exits 0 on the page (the tag below byte 1024, the first 1024 bytes decode as UTF-8); "
            "(2) the page test 9.36.0 runs all its added features with no skip and passes them (P1, P2, P3, P4, P5, P6, P8, P9, P11) and every other feature, exit 0, and the page tests 9.34.1 and 9.35.1 report no failure and widgets, features and gates not below the stored result of the page 9.74.0 (chapter 5) or 9.75.0 (chapter 6), skipped not more; "
            "(3) the chapter-code tab equals the deck's chapter-code manifest in names and order and each example runs in the page and shows its result; (4) the Stage 4 gate runner v1_1_0 for %s exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, the Research, Deck and Page chapter checks pass, the deck match check reports 0 not carried; "
            "(5) no committed file is edited (an executor's own log is written once), no gate, test or threshold changed; the Stage 4 page ABox and the stored page-test result are new files; results as printed; if any element fails the page is named failing and this criterion has no passing result. " % (ch, ch) + FACT + " " + RV.STD_P)
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The delivered chapter 5 and 6 pages show their labels with garbled characters: may a template 9.52.2 declare the character set first, with a check, and the two pages be rebuilt on it?"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR3_ChipScroll, ex:AC5R_Page_Ch05, ex:AC5R_Page_Ch06 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit("Requested " + WHEN + ". " + FACT + " The change grows the scope: a new template version, a new check tool, and new rebuilds of two pages that were delivered. Pending until the ScopeChange that admits the stories is recorded in the Backlog version."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What declaring the character set first costs, measured before it is started"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_ChipScroll ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACT + " AFFECTED: the pages 9.82.0 of chapters 5 and 6 (delivered; replaced by new files 9.83.0, the old files stay); the Build task of the chapter 5 page of Iter_18 (Suspended, not edited, G125) and the Done tasks of the chapter 6 page and of the template 9.52.1 (not edited; the template 9.52.1 stays byte-identical). "
        "NOT AFFECTED: the decks, the page tests, the builders (unless the builder puts bytes before the template, then one new builder file), the pywheels files, the chapter-code manifests, every other chapter, the Mission outcome and the Achieved status. "
        "OTHER PAGES: the pages of chapters 1 to 14 in the owner's archive have the same defect (the tag at byte 13584 or later). They are NOT rebuilt by this request: the decision is tracked by the change request ex:CR3_CharsetOtherPages (Pending) and the closure caveat ex:Cav_CharsetOtherPages. "
        "PLAN (route as ex:CR3_ChipScroll, G127): a StageRevision from the Scope stage, seven versions; new iteration Iter_19 with four stories and eight tasks: the template 9.52.2 and the check (two executors, about 0.5 h each, in parallel) and their verification (builder, about 0.5 h each); then the pages of chapters 5 and 6 rebuilt in parallel (executors, about 1.5 h each) and their verification (builder, about 1 h each, serial browser tests). "
        "Estimated from T0 (both tool executors start at once): tools verified about T0+1.2 h, pages about T0+2.7 h and T0+3.2 h; the machine has 2 cores, so browser tests queue. The proposed end is today Friday 2026-10-23 11:00 UTC (14:00 Istanbul), the owner's to decide. "
        "COST: new files only (one template, one tool); old files byte-identical; no gate, test or threshold changes. A criterion that fails is named failing and its story is not Done; nothing is waived."))
    cr2 = ('\nex:CR3_CharsetOtherPages a backlog:ChangeRequest ;\n    rdfs:label "The pages of chapters 1 to 14 in the owner\'s archive declare their character set late: may they be rebuilt on template 9.52.2?"@en ;\n'
           '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso %s ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit("Found " + WHEN + ". " + FACT + " Only the pages of chapters 5 and 6 are rebuilt now (the owner uses them first). The other pages carry the same defect and stay as delivered until the owner decides whether to rebuild them: the decision is the disposition of this request. Pending."))
    ia2 = ('\nex:IA3_CharsetOtherPages a backlog:ImpactAssessment ;\n    rdfs:label "What rebuilding the other pages on template 9.52.2 would cost, measured before any decision"@en ;\n    backlog:analyzesRequest ex:CR3_CharsetOtherPages ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso %s ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, lit("Affected if yes: the pages of the other twelve chapters (new files, one rebuild and three serial page-test runs each, about 1.5 h of executor time and 1 h of control each, on 2 cores), a Scope-stage revision (G127). Not affected if no: nothing changes; those pages keep the defect and show garbled characters in viewers that prescan only the first 1024 bytes. The charset check of this iteration measures any page, so the extent can be counted at once."))
    cav = ('\nex:Cav_CharsetOtherPages a backlog:ClosureCaveat ;\n    rdfs:label "The pages of the chapters other than 5 and 6 declare their character set late and can show garbled characters"@en ;\n    backlog:caveatTrackedBy ex:CR3_CharsetOtherPages ;\n    rdfs:comment %s@en .\n') % lit(
        "Disclosed " + WHEN + ": the pages of chapters 1 to 14 other than the rebuilt chapters 5 and 6 have `<meta charset=\"utf-8\">` at byte 13584 or later. Tracked by the change request ex:CR3_CharsetOtherPages, whose disposition is the owner's decision.")
    return t + cr + ia + cr2 + ia2 + cav, "ChangeRequest %s (Pending) and ImpactAssessment %s for the late character-set declaration of the delivered pages, with the change request ex:CR3_CharsetOtherPages, its assessment and the closure caveat that track the other pages (decision pending)." % (CR, IA)
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds deliverables (a new template version and two page rebuilds, as new files); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). "
              "The request and its impact assessment " + IA + " were recorded first. This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated. "
              "The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). Recorded as decided by the builder role.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the character set declared first (template 9.52.2, a check, and the chapter 5 and 6 pages)"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the character set repair: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    L = ['''
ex:Del3_CharsetTemplate a backlog:ScopeDeliverable ;
    rdfs:label "A page template 9.52.2 that declares its character set within the first 1024 bytes, and a check that measures it, as new files with the older templates kept"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%(cl)s"^^xsd:string ;
    backlog:hasDeliverableText %(tp)s ;
    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del3_CharsetPages a backlog:ScopeDeliverable ;
    rdfs:label "The pages of chapters 5 and 6 rebuilt on template 9.52.2 so that their character set is declared within the first 1024 bytes"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%(cl)s"^^xsd:string ;
    backlog:hasDeliverableText %(pg)s ;
    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Scope3 backlog:requiresDeliverable ex:Del3_CharsetTemplate, ex:Del3_CharsetPages ; rdfs:seeAlso %(cr)s, %(ia)s .
ex:Scope3 rdfs:comment %(sc)s@en .
''' % dict(cl=T.CLAUSE, cr=CR, ia=IA, tp=lit("The page template 9.52.2, a new file over 9.52.1 (which stays unchanged, as do the older templates), whose first bytes are the character set declaration `<meta charset=\"utf-8\">` with the header comments after it, and a new check tool that measures the declaration; every id, hook and behaviour of 9.52.1 stays. " + FACT + " " + STD1),
                  pg=lit("The pages of chapter 5 and chapter 6 rebuilt as new files on template 9.52.2 with the builders v4_15_0 and v2_24_0, passing the charset check, the page test 9.36.0 and the page tests 9.34.1 and 9.35.1 with no failure, the Stage 4 gate runner and the chapter checks. " + RV.STD_P),
                  sc=lit("Revised 2026-10-23 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires ex:Del3_CharsetTemplate and ex:Del3_CharsetPages in the area ex:Area3_Remedy56. No exclusion changes: the new template is a new file named in the deliverable and the exclusion of changes to gates, tests and thresholds still holds." % (REV, CR, WHEN)))]
    t += "".join(L); return t + SL.out_new(t, "Scope", "Out3_ScopeR8", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the character set repair: two deliverables (template 9.52.2 with its check; the pages of chapters 5 and 6 rebuilt on it) in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR8", prev); t = X.set_status(t, "LS_Goaled")
    L = ['''
ex:G3_Charset a backlog:Goal ;
    rdfs:label "The chapter 5 and 6 pages declare their character set where every viewer finds it"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Must ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %(r)s ;
    backlog:producedByStage ex:Out3_GoalR8 .
ex:G3_Charset rdfs:comment "Drafted by the builder session on 2026-10-23 from the change request %(cr)s; the intent origin is therefore Derived."@en .
ex:Spec3H_P a backlog:Specification ;
    rdfs:label "What it is for a page to declare its character set in time"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Charset ;
    backlog:hasSpecificationText %(s)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR8 .
ex:Scen3H_Passes a backlog:TestScenario ; rdfs:label "A page on template 9.52.2 declares its character set within the first 1024 bytes"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3H_P ;
    backlog:hasScenarioText "Given a page of chapter 5 or 6 built on template 9.52.2, when the charset check and the page tests are run, then the check passes (the tag lies below byte 1024 and the first 1024 bytes decode as UTF-8) and nothing else fails." .
ex:Scen3H_NotClaimed a backlog:TestScenario ; rdfs:label "A page whose character set is declared late is named failing and not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3H_P ;
    backlog:hasScenarioText "Given the chapter 5 page 9.82.0 on template 9.52.1 (the tag at byte 13584, measured 2026-10-23), when the charset check is run, then it fails and the page carries no passing result." .
''' % dict(cr=CR, r=lit("Derived from the revised scope and from the change request %s: the owner uses the pages in class; garbled characters in the labels are a defect of the teaching material. %s" % (CR, FACT)), s=lit(STD1 + " " + FACT))]
    t += "".join(L); return t + SL.out_new(t, "Goal", "Out3_GoalR8", "Out3_ScopeR8"), "third lineage, Goal stage rebuilt for the character set repair: one goal with its specification and a nominal and a rejection scenario."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR8", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    L = ['''
ex:Obj3_Charset a backlog:Objective ; rdfs:label "Pages of chapters 5 and 6 whose character set is declared within the first 1024 bytes: from 0 to 2"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Charset ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Charset ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of the pages of chapters 5 and 6 on which the charset check exits 0 and the page tests 9.36.0, 9.35.1 and 9.34.1 report no failure, read from the runs after the evidence bridge has run them on the newest pages." ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "2"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3H_Charset ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR8 .
ex:Met3_Charset a backlog:Metric ; rdfs:label "pages of chapters 5 and 6 with the character set declared below byte 1024"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3H_Charset a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the rebuilt pages are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria on the rebuilt pages, so the count is read from verified runs." ; backlog:expectedValue "2"^^xsd:decimal .
ex:Obs44_Charset a backlog:MetricObservation ; rdfs:label "Baseline, before the repair"@en ;
    backlog:observesMetric ex:Met3_Charset ; backlog:observationFor ex:Obj3_Charset ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Baseline from the coordinator's measurement of 2026-10-23: the tag lies at byte 13584 in both pages 9.82.0, so 0 of 2." .
ex:Obj3_Charset rdfs:comment "Drafted by the builder session on 2026-10-23 from the change request %s; the intent origin is therefore Derived."@en .
''' % (now, CR)]
    t += "".join(L); return t + SL.out_new(t, "Objective", "Out3_ObjectiveR8", "Out3_GoalR8"), "third lineage, Objective stage rebuilt for the character set repair: one objective (pages with the character set declared below byte 1024, 0 to 2) with its metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR8", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLDB); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLDB, "backlog:admittedByOutput %s ;" % NEWB)
    L = ['ex:TS_PageTemplateE a backlog:ToolScript ; rdfs:label "page template 9.52.2 (new file over 9.52.1: the character set is declared first)"@en ; backlog:scriptFileName "course_page_template_v9_52_2.html" ; backlog:acceptsGraphPath false .\n', 'ex:TS_PageCharsetCheck a backlog:ToolScript ; rdfs:label "page charset check v1_0_0 (new tool: the character set declared within the first 1024 bytes)"@en ; backlog:scriptFileName "sen0401_page_charset_check_v1_0_0.py" ; backlog:acceptsGraphPath false .\n']
    tools_of = {"AC6R_Template": ["TS_PageTemplateE", "TS_PageCharsetCheck", "TS_PageTest36", "TS_PageBuilder415", "TS_PageData224"], "AC6R_Check": ["TS_PageCharsetCheck"], "AC6R_Page_Ch05": ["TS_PageTemplateE", "TS_PageCharsetCheck", "TS_PageBuilder415", "TS_PageData224", "TS_PageTest36"] + RV.BASE, "AC6R_Page_Ch06": ["TS_PageTemplateE", "TS_PageCharsetCheck", "TS_PageBuilder415", "TS_PageData224", "TS_PageTest36"] + RV.BASE}
    for c, lab in LAB.items():
        k = "TC3H_T" if c == "AC6R_Template" else ("TC3H_K" if c == "AC6R_Check" else "TC3H_P")
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs and the diffs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:%s_Passes, ex:%s_NotClaimed .\n' % (c, lit(lab), lit(gh(c)), ", ".join("ex:" + x for x in tools_of[c]), lit(VER), k, k))
    for tid, title, ttype, deps, sess, est, hrs, note in TASKS: L.append(RV.task_block(tid, title, ttype, deps, sess, est, hrs, note))
    for sid, title, deliv, obj, crits, tks in STORIES: L.append(RV.story_block(sid, title, deliv, obj, crits, tks, "Requested " + WHEN + " (" + CR + "). One criterion per unit (G133). The Done stories and tasks stay Done and are not edited (G125); the chapter 5 page task of Iter_18 stays Suspended. " + FACT))
    for k in ("T", "K", "P"):
        L.append('''
ex:TC3H_%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the checks of the criteria on the new files and require no failure and no skip"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3H_Passes ; backlog:runsOnData ex:Data3H_%(k)s_Passing ;
    backlog:hasCaseText "Run the checks of the criterion over the newest files; they report no failure and exit 0 (the bridge runs recorded in this register are these runs)." .
ex:TC3H_%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on the existing page that fails and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3H_NotClaimed ; backlog:runsOnData ex:Data3H_%(k)s_Failing ;
    backlog:hasCaseText "Run the charset check over the chapter 5 page 9.82.0 and the template 9.52.1 (measured 2026-10-23); it fails and they carry no passing result." .
ex:Data3H_%(k)s_Passing a backlog:TestData ; rdfs:label "The rebuilt files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest rebuilt files, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3H_%(k)s_Failing a backlog:TestData ; rdfs:label "The chapter 5 page 9.82.0 whose character set is declared late"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The page sen0401_ch05_page_v9_82_0.html on template 9.52.1 with the tag at byte 13584 (ex:IA3_Charset)." .
''' % dict(k=k, cr=", ".join("ex:" + c for c in ({"T": ["AC6R_Template"], "K": ["AC6R_Check"], "P": ["AC6R_Page_Ch05", "AC6R_Page_Ch06"]}[k]))))
    sid_all = [s[0] for s in STORIES]; tk_all = [x[0] for x in TASKS]
    for x in sid_all + tk_all:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, ITER, lit("Refined by the builder session from the change request %s and the measured facts of %s: acceptance criterion with tool and version, dependencies, estimated start, and a brief to be generated; startable when its dependencies are Done." % (CR, IA))))
    for sid, title, deliv, obj, crits, tks in STORIES:
        L.append('ex:Plan3H_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 19"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3H_P, ex:Scen3H_Passes, ex:Scen3H_NotClaimed .\n' % (sid, sid, now, ITER, sid, ", ".join("ex:" + x for x in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    L.append("ex:Obj3_Charset backlog:metricMovableBy ex:ST_Charset_Template, ex:ST_Charset_Check, ex:ST_Charset_Page_Ch05, ex:ST_Charset_Page_Ch06 .\n")
    END = "2026-10-23T11:00:00"
    SG = ("The character set of the chapter 5 and 6 pages is declared within the first 1024 bytes on a new template 9.52.2, measured by a new check, and both pages are rebuilt on it and pass the check and the three page tests, verified by the evidence bridge; the new template and the rebuilt pages are new files and nothing existing is edited. Frozen at the planning ceremony.")
    DS = ("Proposed by the builder session on 2026-10-23: the start is the instant of the planning ceremony ex:PC3_Iter_19; the proposed end is Friday 2026-10-23 11:00 UTC (14:00 Istanbul); the owner decides the end. Justification (estimates, not measurements): the template change is one moved tag (about 0.5 h with a scratch proof run) and the check is a small tool (about 0.5 h), in parallel, each verified in about 0.5 h; "
          "the two page rebuilds follow in parallel (about 1.5 h each with three serial page-test runs each, on 2 cores), their verification about 1 h each, serial. Critical path: 0.5 h + 0.5 h verification + 1.5 h + 1.0 h = about 3.5 h after the tool executors start; chapter 6 about 0.5 h later. The page of chapter 6 can be declined without blocking chapter 5.")
    L.append('ex:Iter_19 a backlog:Iteration ; rdfs:label "Iteration 19: the character set declared first, template 9.52.2, a check and the chapter 5 and 6 pages rebuilt"@en ; backlog:hasIdentifier "Iter_19" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (now, END, lit(DS), lit(SG), ", ".join("ex:" + x for x in sid_all + tk_all)))
    L.append('ex:PB3H_Iter_19 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 19 when it was planned"@en ; backlog:baselineFor ex:Iter_19 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (now, now, END))
    L.append('ex:PC3_Iter_19 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 19: the character set declared first"@en ; backlog:ceremonyFor ex:Iter_19 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (now, ", ".join("ex:Plan3H_" + s for s in sid_all), lit("Held %s by the builder session after the change request %s: four stories and eight tasks are committed to this iteration, whose goal is frozen at its start. No executor has started in it; work begun is recorded at the real start of each executor session, with its brief." % (now, CR))))
    L.append('ex:SC3_Charset a backlog:ScopeChange ;\n    rdfs:label "Scope grown by the character set repair: template 9.52.2, a check and the chapter 5 and 6 pages rebuilt on it"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in sid_all), lit("Requested " + WHEN + ". The boundary moved outward by four stories; new files only; nothing existing is edited or weakened.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Charset and the four stories it admits; it was Pending before. The direction is the owner\'s standing direction of 2026-10-22 17:30 Istanbul as relayed by the course coordinator on 2026-10-23; the end of the iteration is still the owner\'s."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR10", "Out3_ObjectiveR8"), "third lineage, Backlog stage rebuilt for the character set repair: four stories (template; check; pages of chapters 5 and 6) with eight tasks and dependencies, three criteria with tools and versions, refinement and planning events, the new iteration Iter_19, and the ScopeChange that admits the stories; the change request is Accepted; the %d carried items are re-admitted, not re-dated." % n
def ev_fill(t, prev):
    return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete and no work is begun." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
