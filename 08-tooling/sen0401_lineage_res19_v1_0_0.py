#!/usr/bin/env python3
"""sen0401_lineage_res19 v1_0_0 - the owner's correction of 2026-10-29 on the exam mission: the exam work is a change of the THIRD lineage, not a fourth lineage.
Route (c) of the routing test (G104): the mission statement is amended -> ex:Mission_V2 supersedes ex:Mission (owner-decided), with a chapter-agnostic wording;
the chapter facts are owner statements (CR3_ExamMission, IA3_ExamMission, the origin of Mission_V2), not mission text. The exam chain of the fourth lineage is
re-admitted in the third lineage by a StageRevision from the Scope stage (G127), the same route as sen0401_lineage_res18; the fourth lineage is set down with an
as-is assessment and a closure report marked cancelled (G162).
Usage: change | abandon4 | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import glob, importlib.util, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_open4_v1_0_0 as O4
lit = G.lit


def _pv_newest():
    fw = X.FW; vk = lambda q: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", q)[0]]
    spec = importlib.util.spec_from_file_location("pv", sorted(glob.glob(fw + "/03-tooling/backlog_pipeline_verify_v*.py"), key=vk)[-1])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.STAGE_TYPES = m._load_stage_types(sorted(glob.glob(fw + "/01-ontologies/backlog_tbox_v*.ttl"), key=vk)[-1], table="v4")
    return m
X._pv = _pv_newest

REV = "ex:Revision_Lineage3_Scope30"
ACTIVE = ["ex:Out3_ScopeR29", "ex:Out3_GoalR29", "ex:Out3_ObjectiveR29", "ex:Out3_BacklogR31"]
OLDB = "ex:Out3_BacklogR31"; NEWB = "ex:Out3_BacklogR32"
CR = "ex:CR3_ExamMission"; IA = "ex:IA3_ExamMission"; SC = "ex:SC3_Exam"
WHEN = "Thursday 2026-10-29, the owner's words relayed by the coordinator (mission input 15:08 Istanbul; the owner's correction of the chapter scope and of the route the same day)"
CH = "the exam chapters (the instructor fixes the list before each sitting)"
OWNER_QUOTE = ("The exact chapter content will be cleared tomorrow after the completion of the lectures. For SEN0401, we will be able to cover chapter 6 and all other chapters are in the scope of the exam. "
               "Possibly, we will not be able to finish Chapter 7.")
READING = ("The coordinator's reading of that word (a reading, not the owner's text): the chapter list is NOT fixed to chapters 1 to 8; chapters 1 to 6 are in the exam scope; chapter 7 is doubtful; the final list is due 2026-10-30, "
           "after the lectures. The lineage agent builds every chapter-specific item against a chapter list that is a PARAMETER of the engine, fixed by the instructor before each sitting.")
OLD_STATEMENT = ("Every SEN0401 lecture teaches what the third edition of Mastering Bitcoin teaches, chapter by chapter, with a deck, the research behind it and an interactive page - renewed from the book and researched evidence, "
                 "within the term theme of semantic technologies.")
EXAM_CLAUSE = ("the course assesses what it teaches: for the chapters the instructor fixes before each sitting, two printed exams (the midterm and a make-up exam, a 60-minute sitting each) built from the course's own material "
               "by one general exam engine, with a reliable method to grade each student's paper")
STATEMENT_V2 = OLD_STATEMENT[:-1] + ", and " + EXAM_CLAUSE + "."
OLD_OUTCOME = "A student in SEN0401 finds, for each chapter, a deck, an interactive page and the sources behind them, grounded in the edition they can read for free."
OUTCOME_V2 = (OLD_OUTCOME + " The instructor also holds, for each sitting, a print-ready paper with its answer key, made by one general engine from the chapters he fixes, and a method and a tool that read, assess and grade a student's paper.")
MIDTERM_INPUT = O4.OWNER.replace("Chapters 1 to 8, physical paper, midterm next week; the budget is this week's usage limit.", "Physical paper; the midterm is next week; the budget is this week's usage limit.")
COST = ("THE COST OF THE FOURTH LINEAGE (disclosed): the lineage agent advanced the fourth lineage (ex:Lineage4, mission ex:Mission_Midterm) from LS_Opened to LS_Backlogged in the versions 0.618.0 to 0.623.0 BEFORE the owner answered the route question "
        "(his rule: one lineage at a time, a different mission waits at Opened; he had asked whether the mission and scope already match the exam scope). That was a process slip. What it cost: (1) five register versions and six commits (9f8d8dc, dbf2ace, a55608b, a860120, e049103, 655adfc) that carry two active lineages with no link between them, "
        "which the shape UnconnectedActiveLineagesShape would report as a Violation; the full validator was not run on them; (2) a Mission, Scope, four goals, an objective, seven Proposed stories with criteria, tasks and planning events, and two planned iterations that have to be set down (lineage 4) and re-admitted (lineage 3); "
        "(3) the work of recomputing five digests with the digest table v5, which the third lineage does not use. Nothing was started, no urgent interruption was declared, no executor was briefed, and no committed file was edited; the forks stay in git as history.")


def fixch(s):
    return s.replace("chapters 1 to 8", CH).replace("Chapters 1 to 8", CH[0].upper() + CH[1:])


# ------------------------------------------------------------------ change
def ev_change(t):
    m = ('\nex:Mission_V2 a backlog:Mission ;\n    rdfs:label "Teach SEN0401 from the edition students can now read for free, and assess what it teaches"@en ;\n'
         '    backlog:supersedesMission ex:Mission ;\n    backlog:missionFor ex:Backlog ;\n    backlog:hasMissionStatement %s ;\n    backlog:hasMissionOrigin %s ;\n    backlog:hasMissionOutcome %s ;\n'
         '    backlog:outcomeRationale %s ;\n    backlog:decidedBy backlog:Owner ;\n    backlog:missionSource %s .\n') % (
        lit(STATEMENT_V2),
        lit("Route (c) of the routing test (a mission-statement change: the same lineage under a better statement), decided by the owner on " + WHEN + ". The owner's words: " + OWNER_QUOTE.replace('"', "'") + " " + READING.replace('"', "'")
            + " The wording of the mission names no chapter on purpose: the chapter facts are recorded as owner statements in ex:CR3_ExamMission and ex:IA3_ExamMission, not in the mission text. The first part of the statement is the old statement, unchanged. The mission input of the owner was: " + MIDTERM_INPUT.replace('"', "'")),
        lit(OUTCOME_V2),
        lit("The old statement stays in the register as ex:Mission (superseded, kept as history; the lineages 1 to 3 were opened under it). The old mission does not mention the exam, and the owner asked that the exam scope be covered by amending the mission and updating the lineage, not by a separate lineage."),
        lit("The owner's words of 2026-10-29 (the mission input at 15:08 Istanbul, the route answer, and the correction of the chapter scope), relayed by the coordinator; the register's rulings G104 (routing test) and G127 (a deliverable added to a closed scope)."))
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The course also assesses what it teaches: two printed exams (midterm and make-up) for the chapters the instructor fixes, from one general engine, with a reliable grading method"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso %s, ex:Mission_V2 ;\n'
          '    backlog:hasChangeRequestRationale %s .\n') % (CR, IA, lit(
        "Owner's words, " + WHEN + ". MISSION INPUT: " + MIDTERM_INPUT + " THE OWNER'S ANSWER ON THE ROUTE: does the mission and scope match the exam scope? If so, updating the lineage and the prioritisation of the exam is enough; otherwise the mission can be enhanced to cover the exam work and the lineage updated. "
        "No separate lineage and no pre-chain urgent item unless the rulings leave no other way. MEASURED: the mission of the third lineage (ex:Mission) and its scope (ex:Scope3) say nothing about an exam: the scope's IN list is the link passes and the carried open work, and its OUT list does not name an exam; the exam work therefore does not match the mission as stated, so the mission was not set for it. "
        "The routing test (G104, narrative item 4) gives route (c): a mission-statement change, the same lineage under a better statement, decided by the owner. "
        "THE OWNER'S STATEMENTS ABOUT THE CHAPTERS (recorded here, not in the mission text): the owner's own words: " + OWNER_QUOTE.replace('"', "'") + " " + READING.replace('"', "'")
        + " THE EXAMS: two, the midterm and a make-up exam over the same chapters, each a 60-minute sitting on physical printed paper. THE TIME BOX: chapter work restarts on Sunday 2026-11-01, after the weekly usage limit resets; until then only the exam scope is worked; when it restarts, the pages of chapters 1 to 6 are measured and completed first, chapters 7 and 8 only if time remains; chapter 11 and chapters 9 and above stay paused (nothing of them is started, so no urgent interruption is declared)."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What amending the mission and moving the exam chain into the third lineage costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3, ex:Lineage4 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(
        "AFFECTED: the mission (a NEW statement ex:Mission_V2 that supersedes ex:Mission; ex:Mission stays as history and stays the mission the third lineage's recorded Mission output was computed for); the third lineage's Scope, Goal, Objective and Backlog stages (a revision from the Scope stage, G127: four outputs retracted and rebuilt, the Mission output stays); "
        "the fourth lineage (set down: as-is assessment, closure report marked cancelled, status Abandoned). NOT AFFECTED: every Done item, the executors, the decks and pages, every committed file, the evidence. "
        "MEASURED BEFORE THE ROUTE WAS CHOSEN: the mission digest of the third lineage changes when the new mission belongs to the lineage or when the lineage's mission pointer moves (0d854051ea52ba05 becomes 52f0291f178728b1) and stays when ex:Mission_V2 is a free-standing superseding statement; "
        "a revision from the Mission stage is refused by the framework (StageRevisionShape: rebuilding from the mission is a LineageRestart). The route therefore keeps ex:Lineage3 pointing at ex:Mission, and the goals of the exam contribute to ex:Mission_V2 (the statement the exam work serves). "
        "COST OF THE ROUTE: seven register versions and commits for the revision, one for the closure of the fourth lineage, and the loss of the pointer purity (the lineage's mission pointer names the superseded statement; the owner may ask for a LineageRestart or a pointer move with a full rebuild of all five outputs). "
        + COST))
    return t + m + cr + ia, "Route (c): the owner-decided mission amendment ex:Mission_V2 (supersedes ex:Mission; chapter-agnostic wording), the change request ex:CR3_ExamMission with the owner's statements about the chapters, and the impact assessment ex:IA3_ExamMission with the disclosure of the fourth lineage's early advance and its cost. No stage changes in this version."


# ------------------------------------------------------------------ abandon4
def ev_abandon4(t):
    t0 = M.newest()
    d = tempfile.mkdtemp(prefix="res19_", dir="/tmp/claude-0/s"); p = os.path.join(d, "r.ttl"); open(p, "w", encoding="utf-8").write(t)
    tool = sorted(glob.glob(X.FW + "/03-tooling/backlog_lineage_steps_v*.py"), key=lambda q: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", q)[0]])[-1]
    LIN = "http://example.org/sen0401-slides-lineage#Lineage4"
    fit = ("AS-IS (2026-10-29): the fourth lineage was taken from LS_Opened to LS_Backlogged (Mission, Scope, Goal, Objective and Backlog stages) before the owner's answer to the route question. It holds seven Proposed stories with their tasks, criteria and planning events in two planned iterations; nothing was started. "
           "FIT: the exam scope (the critical points, the general engine, the items, the paper rules, the papers, the grading method) is what the owner asked for. GAP: the lineage is a separate lineage for the same course; the owner's rule is one lineage at a time and his answer was that the exam scope belongs to the mission of the course, amended, and the lineage updated. "
           "The owner's correction (the chapter list is not fixed to 1 to 8) also makes its wording wrong. Its content is re-admitted in the third lineage (ex:Mission_V2, a stage revision from the Scope stage) in the versions that follow this one.")
    imp = ("IMPACT: no item was started; the seven stories, the fourteen tasks, the criteria and the planning events of the fourth lineage are due and are not carried: the same items are admitted again, renamed, in the third lineage. Nothing is lost that was built, because nothing was built. "
           "The cost of the early advance is in ex:IA3_ExamMission. The lineage and its mission ex:Mission_Midterm stay in the register as history.")
    r = subprocess.run([sys.executable, tool, "assess", p, "--lineage", LIN, "--fit-gap", fit, "--impact", imp], capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip()[-300:])
    assert r.returncode == 0, r.stderr
    t = open(p, encoding="utf-8").read(); shutil.rmtree(d, ignore_errors=True)
    n = len(re.findall(r"^ex:Closure_\d+|a backlog:ClosureReport", t, re.M)) + 1
    ass = re.findall(r"^<(http://example.org/sen0401-slides-lineage#AsIs_\d+)> a backlog:AsIsAssessment", t, re.M)[-1]
    ts = M.now()
    rat = ("Cancelled on 2026-10-29. The owner answered the route question: the exam scope is covered by amending the mission of the course and updating its lineage, not by a separate lineage, and he corrected the chapter scope. "
           "The fourth lineage was advanced to LS_Backlogged before that answer (a disclosed slip; see ex:IA3_ExamMission). Its exam chain is re-admitted in the third lineage under ex:Mission_V2. The mission ex:Mission_Midterm is kept as history.")
    cl = ('\n<http://example.org/sen0401-slides-lineage#Closure_%d> a backlog:ClosureReport ; backlog:belongsToLineage ex:Lineage4 ; backlog:closesForMission ex:Mission_Midterm ; backlog:reportGeneratedAt "%s"^^xsd:dateTime ;\n    backlog:reportsOnObjective ex:Obj4_Midterm ;\n'
          '    backlog:hasClosureMark backlog:Cm_Cancelled ; backlog:citesAssessment <%s> ; backlog:hasClosureSummary %s .\n') % (n, ts, ass, lit(rat))
    t += cl
    i, j = T.blk(t, "Mission_Midterm"); b = t[i:j]
    old = re.search(r'backlog:hasMissionOutcome ("(?:[^"\\]|\\.)*")', b)
    assert old
    b = b.replace(old.group(0), "backlog:hasMissionOutcome backlog:Out_Abandoned", 1)
    b = re.sub(r'backlog:outcomeRationale "(?:[^"\\]|\\.)*"', lambda m_: "backlog:outcomeRationale " + lit(rat + " The outcome statement it carried before: " + old.group(1)[1:-1].replace('"', "'")), b, count=1)
    t = t[:i] + b + t[j:]
    t = O4.set_status(t, "LS_Abandoned")
    t += ('\nex:Lineage4 rdfs:comment %s@en .\n') % lit("Set down on 2026-10-29 by the closure report ex:Closure_%d (marked cancelled) after the as-is assessment %s. " % (n, ass.split("#")[-1]) + COST)
    return t, "Fourth lineage set down: as-is assessment, closure report marked cancelled, mission outcome Abandoned, lineage status Abandoned; the early advance is disclosed with its cost."


# ------------------------------------------------------------------ retract
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds the exam deliverables and the page measurement of chapters 1 to 8 to a lineage whose Backlog stage is closed; a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). "
              "The Mission stage is NOT revised: the amendment of the mission is route (c) and the superseding statement ex:Mission_V2 is not owned by the lineage, so the Mission output still reproduces. This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; "
              "the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission under the new Backlog output.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the exam work under the amended mission, and the page measurement of the chapters in the order the owner gave"@en ;\n'
         '    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (
        REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the exam work under the amended mission and the page measurements: the four outputs are retracted; nothing is rebuilt in this version."


def out_new(t, stage, name, consumes):
    return ('\nex:%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the third lineage, rebuilt by the stage revision for the exam work under the amended mission"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;\n    backlog:consumesOutput ex:%s ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (name, stage, stage, consumes, X.digest(t, stage))


# ------------------------------------------------------------------ scope
AREAS = [("Sources", "The critical points of the exam chapters and their sources", "03-materials (decks, speaker notes, pages), 02-textbook and the course corpus, the stories; the list is a new file in 08-tooling/exam", "critical points listed with at least one source each, and points no source carries listed for the owner: none today"),
         ("Engine", "The general exam engine and the items of the two exams", "08-tooling/exam: the engine as new files, the item files of the two exams; the chapter banks are read, never edited", "exams built by the engine from items of several chapters, constraints checked: 0 of 2 today"),
         ("Paper", "The printed paper: types and styles, page reduction, answering methods", "08-tooling/exam: the paper rules as SHACL, the renderer, the two papers and keys as print-ready files", "papers print-ready with page count and answering aids measured: 0 of 2 today"),
         ("Grading", "Reading, assessing and grading a student's paper", "08-tooling/exam: the reading and grading method and tool, shown on synthetic papers", "paper read and graded with measured accuracy on synthetic papers: none today"),
         ("PageMeasure", "The interactive pages measured with the page tests 9.34.2, 9.35.2 and 9.37.0, chapters 1 to 6 first", "03-materials/chNN/page: read, never changed; the stored results of the runs", "pages measured: 0 of 8 today (chapter 11 is a separate, paused story)")]
DELIVS = [(k, a, fixch(lab), fixch(txt)) for k, a, lab, txt in O4.DELIVS]
DELIVS = [("Exam" + k, "Engine" if a == "Exams" else a, lab, txt) for k, a, lab, txt in DELIVS]
DELIVS = [(k if k != "ExamGrading" else "ExamGrading", a, lab, txt) for k, a, lab, txt in DELIVS]
DELIVS.append(("PagesMeasured", "PageMeasure", "The interactive pages of chapters 1 to 8 measured with the page tests 9.34.2, 9.35.2 and 9.37.0, chapters 1 to 6 first, and the results recorded as printed",
               "For each chapter 1 to 8 the page in 03-materials/chNN/page (the newest version) is run, unchanged, with the page tests 9.34.2, 9.35.2 and 9.37.0, serially, each under flock /tmp/page_test.lock, through the page test run wrapper; the results are kept as new files as printed. The order is the owner's: chapters 1 to 6 first, chapters 7 and 8 only if time remains. A page that fails or skips is reported as printed and not repaired in the measurement; repairs are separate changes."))
EXCL = [("NoDelivery", "In-browser or screen delivery, CATS or QTI export, and any change to the interactive pages", "The owner's word is a physical printed paper. The pages' exam modes stay as they are.", "Owner's words of 2026-10-29: physical printed paper."),
        ("LaterChapters", "Chapters the instructor does not fix for a sitting, the page and deck work of chapter 11 and of chapters 9 and above", "Chapter work restarts on Sunday 2026-11-01 and is ordered: pages of chapters 1 to 6 first; chapter 11 and chapters 9 and above stay paused.", "Owner's words of 2026-10-29."),
        ("StudentData", "Any real student's name, number, paper or score", "The exam and the grading method are shown on synthetic stand-ins only.", "The exam convention: no personal data of students."),
        ("OwnerDecisions", "Deciding for the owner what only he knows: the final chapter list, the critical points no source carries, the number of items, the weights per chapter, the paper size, the sitting", "Where no rule or fact settles a question it is put to the owner plainly, never decided by the agent.", "Owner's words of 2026-10-29.")]
ENT = O4.ENT
CLAUSE = "the course assesses what it teaches: for the chapters the instructor fixes before each sitting, two printed exams"


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    i, j = T.blk(t, "Scope3"); b = t[i:j]; assert "backlog:scopeForMission ex:Mission ;" in b
    t = t[:i] + b.replace("backlog:scopeForMission ex:Mission ;", "backlog:scopeForMission ex:Mission_V2 ;", 1) + t[j:]
    L = []
    for k, lab, loc, meas in AREAS:
        L.append('ex:Area3_%s a backlog:ScopeArea ;\n    rdfs:label %s@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n    backlog:areaLocation %s ;\n    backlog:areaMeasure %s ;\n    backlog:hasScopeLayer backlog:Layer_Work .\n' % (k if k == "PageMeasure" else "Exam" + k, lit(lab), lit(loc), lit(meas)))
    for k, a, lab, txt in DELIVS:
        ar = "PageMeasure" if k == "PagesMeasured" else "Exam" + a
        cl = "an interactive page" if k == "PagesMeasured" else CLAUSE
        L.append('ex:Del3_%s a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause %s^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_%s ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n' % (k, lit(lab), lit(cl), lit(txt), ar))
    for k, what, why, src in EXCL:
        L.append('ex:Excl3_Exam%s a backlog:ScopeExclusion ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:excludesConcern %s ;\n    backlog:hasExclusionRationale %s ;\n    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .\n' % (k, lit(what[:110]), lit(what), lit(why + " Source: " + src)))
    L.append('ex:Blueprint3Exam a backlog:Blueprint ;\n    rdfs:label "What the exams, their items, answer sheets and papers are about"@en ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:blueprintFor ex:Scope3 ;\n    backlog:hasDomainEntity %s .\n' % ", ".join("ex:DE3_" + e[0] for e in ENT))
    for k, lab in ENT: L.append('ex:DE3_%s a backlog:DomainEntity ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 .\n' % (k, lit(lab)))
    gaps = [(e[0], s) for e in ENT for s in ("SuspensionException", "Termination")] + [("Exam", "ActiveUse"), ("StudentPaper", "Creation")]
    why = {"SuspensionException": "No suspension or exception work is planned for this entity in this lineage; it is matured in a later box if the owner needs it.", "Termination": "No termination work is planned: the exams are made once for the sittings and nothing is retired by this lineage.",
           "ActiveUse": "The exam is sat by students on the owner's day; sitting is the owner's act and outside this lineage.", "Creation": "A student fills in the paper at the sitting, outside this lineage; here only synthetic stand-ins are made, for the grading method."}
    names = {"SuspensionException": "suspension or exception", "Termination": "termination", "ActiveUse": "active use", "Creation": "creation"}
    for e, s in gaps:
        L.append('ex:Gap3_%s_%s a backlog:BlueprintGap ; rdfs:label "No coverage yet for the %s at the %s stage"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:gapForEntity ex:DE3_%s ; backlog:gapForStage backlog:Stage_%s ; backlog:hasGapReason %s .\n' % (e, s, dict(ENT)[e].split(" - ")[0], names[s], e, s, lit(why[s])))
    L.append("ex:Scope3 backlog:coversArea %s ; backlog:hasScopeExclusion %s ; backlog:requiresDeliverable %s ; rdfs:seeAlso %s, ex:Mission_V2 .\n" % (
        ", ".join("ex:Area3_" + (a[0] if a[0] == "PageMeasure" else "Exam" + a[0]) for a in AREAS), ", ".join("ex:Excl3_Exam" + e[0] for e in EXCL), ", ".join("ex:Del3_" + d[0] for d in DELIVS), CR))
    L.append("ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-29 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires %d deliverables: six for the exam work, derived from the clause of the amended mission ex:Mission_V2 (\"%s\"), and one for the page measurement. "
                                                       "The exclusions now include the owner's order of the chapter work and the decisions that stay his. Owner statements about the chapters: %s %s" % (REV, CR, WHEN, len(DELIVS), CLAUSE, OWNER_QUOTE.replace('"', "'"), READING.replace('"', "'"))))
    t += "\n" + "".join(L)
    return t + out_new(t, "Scope", "Out3_ScopeR30", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision: five areas, seven deliverables (six for the exam work, one for the page measurement), four exclusions, and a blueprint of four entities with their ten recorded gaps; status LS_Scoped."


# ------------------------------------------------------------------ goal
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR30", prev); t = X.set_status(t, "LS_Goaled")
    goals = [("Exams", "Two exams for the chapters the instructor fixes are made by one general engine from grounded items", "Facing_Mission", "ExamEngine", None),
             ("Paper", "The exams are fit for a physical printed paper and a student's mistakes in giving answers are reduced", "Facing_Scope", "ExamPaper", None),
             ("Grading", "Each student's paper is read, assessed and graded by a method that can be trusted", "Facing_Containment", "ExamGrading", None),
             ("Bounds", "Nothing outside the exam work is built and no decision of the owner is taken for him", "Facing_Exclusion", "ExamSources", "ex:Excl3_ExamNoDelivery, ex:Excl3_ExamLaterChapters, ex:Excl3_ExamStudentData, ex:Excl3_ExamOwnerDecisions")]
    L = []
    for k, lab, fc, area, guard in goals:
        L.append('ex:G3_Exam%s a backlog:Goal ;\n    rdfs:label %s@en ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_%s ;\n    backlog:contributesToMission ex:Mission_V2 ; backlog:hasGoalFacing backlog:%s ; backlog:hasGoalOrigin backlog:GoalOrigin_New ; backlog:hasGoalPriority backlog:Priority_Must ;\n%s    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;\n    backlog:hasGoalRationale %s ;\n    backlog:producedByStage ex:Out3_GoalR30 .\n' % (
            k, lit(lab), area, fc, ("    backlog:guardsExclusion %s ;\n" % guard) if guard else "", lit("Derived from the exam clause of the amended mission ex:Mission_V2 and the scope ex:Scope3 as revised, from the verified gaps G1 to G7 (ex:CR3_ExamMission) and the owner's words of 2026-10-29.")))
    L.append('ex:G3_PageMeasure a backlog:Goal ;\n    rdfs:label "The interactive pages are measured with the new page tests, chapters 1 to 6 first, so that what is wrong with them is known before it is repaired"@en ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_PageMeasure ;\n    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Scope ; backlog:hasGoalOrigin backlog:GoalOrigin_New ; backlog:hasGoalPriority backlog:Priority_Should ;\n    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;\n    backlog:hasGoalRationale %s ;\n    backlog:producedByStage ex:Out3_GoalR30 .\n' % lit("The owner's order of 2026-10-29: when chapter work restarts on Sunday 2026-11-01 the pages of chapters 1 to 6 are measured and completed first, chapters 7 and 8 after only if time remains, chapter 11 and chapters 9 and above stay paused."))
    L.append('ex:Spec3I_Exam a backlog:Specification ;\n    rdfs:label "What it is for the exams to be ready"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_ExamExams ;\n    backlog:hasSpecificationText %s ;\n    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR30 .\n' % lit(
        "Two exams (the midterm and a make-up exam, a 60-minute sitting each) for the chapters the instructor fixes exist as print-ready papers with keys, built by one general engine, with a grading method shown on synthetic papers; every item names its source; every convention is checked by a gate whose answer is known on fixtures; the chapter list is a parameter of the engine."))
    L.append('ex:Spec3I_Exam_Pass a backlog:TestScenario ; rdfs:label "The exams and the grading method pass their checks"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Exam ; backlog:hasScenarioText %s .\n' % lit("Given the new files, when the checks of each criterion run on the evidence bridge, then every element passes."))
    L.append('ex:Spec3I_Exam_Fail a backlog:TestScenario ; rdfs:label "A broken convention, an unsourced item or a misread paper is refused"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Exam ; backlog:hasScenarioText %s .\n' % lit("Given an exam that breaks a convention, an item with no source or a paper with a doubtful mark, when the checks run, then the named check fails and nothing is claimed."))
    L.append('ex:Spec3I_PageMeasure a backlog:Specification ;\n    rdfs:label "What it is for a page to be measured"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_PageMeasure ;\n    backlog:hasSpecificationText %s ;\n    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR30 .\n' % lit("The page of the chapter is run, unchanged, with the page tests 9.34.2, 9.35.2 and 9.37.0, serially under the lock, and every result is kept as printed in new files; a page that fails or skips is reported, not repaired."))
    L.append('ex:Spec3I_PageMeasure_Pass a backlog:TestScenario ; rdfs:label "The measurement is complete and as printed"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_PageMeasure ; backlog:hasScenarioText %s .\n' % lit("Given the page and the three tests, when each is run under the lock, then the results are kept as printed and the page is byte-identical."))
    L.append('ex:Spec3I_PageMeasure_Fail a backlog:TestScenario ; rdfs:label "A repaired page or an edited test is not a measurement"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_PageMeasure ; backlog:hasScenarioText %s .\n' % lit("Given a page changed during the run or a test edited, when the checks run, then the nochange check fails and no measurement is claimed."))
    t += "\n" + "".join(L)
    return t + out_new(t, "Goal", "Out3_GoalR30", "Out3_ScopeR30"), "third lineage, Goal stage rebuilt: five goals (four for the exam work under ex:Mission_V2, one for the page measurement) with two specifications and four scenarios; status LS_Goaled."


# ------------------------------------------------------------------ objective
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR30", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Exam a backlog:Objective ; rdfs:label "The six exam deliverables met on verified evidence: from 0 to 6"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_ExamExams, ex:G3_ExamPaper, ex:G3_ExamGrading, ex:G3_ExamBounds ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Exam ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "6"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3_Exam ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR30 .
ex:Met3_Exam a backlog:Metric ; rdfs:label "exam deliverables whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3_Exam a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the exam stories are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria." ; backlog:expectedValue "6"^^xsd:decimal .
ex:ObsR36_Exam_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Exam ; backlog:observationFor ex:Obj3_Exam ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_PageMeasure a backlog:Objective ; rdfs:label "The pages of chapters 1 to 8 measured with the new page tests: from 0 to 8"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_PageMeasure ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_PageMeasure ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "8"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3_PageMeasure ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR30 .
ex:Met3_PageMeasure a backlog:Metric ; rdfs:label "chapter pages measured, story Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3_PageMeasure a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the chapters 1 to 6 are measured"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria of chapters 1 to 6." ; backlog:expectedValue "6"^^xsd:decimal .
ex:ObsR36_PageMeasure_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_PageMeasure ; backlog:observationFor ex:Obj3_PageMeasure ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
''' % (lit("Count of the six deliverables Del3_ExamCriticalPoints, Del3_ExamEngine, Del3_ExamItems, Del3_ExamPaperRules, Del3_ExamPapers and Del3_ExamGrading whose story is Done on bridge-verified evidence."), now,
       lit("Baseline on 2026-10-29: none of the six exists, so 0 of 6 (gaps G1 to G7)."),
       lit("Count of the stories ST_Ch01_PageMeasure to ST_Ch08_PageMeasure whose story is Done on bridge-verified evidence."), now,
       lit("Baseline on 2026-10-29: no page is measured with the page tests 9.34.2, 9.35.2 and 9.37.0 (they exist since 2026-10-29), so 0 of 8."))
    t += o
    return t + out_new(t, "Objective", "Out3_ObjectiveR30", "Out3_GoalR30"), "third lineage, Objective stage rebuilt: two objectives (exam 0 to 6, page measurement 0 to 8) with metrics, checkpoints and baseline readings; status LS_Objectived."


# ------------------------------------------------------------------ backlog
ITERS = {47: ("Iter_47", "Iteration 47: the critical points, the paper rules and the general exam engine (planned, not started)", "2026-10-29T16:00:00", "2026-10-30T20:00:00", "Revive the critical points, write the paper rules and build the general exam engine."),
         48: ("Iter_48", "Iteration 48: the answering methods, the items, the papers and the grading method (planned, not started)", "2026-10-30T20:00:00", "2026-11-01T12:00:00", "Make the answering methods, the items of the two exams, the two papers and the grading method."),
         49: ("Iter_49", "Iteration 49: the pages of chapters 1 to 8 measured with the new page tests (planned, not started)", "2026-11-01T12:00:00", "2026-11-04T12:00:00", "Measure the pages of chapters 1 to 6 first, chapters 7 and 8 only if time remains.")}
ITMAP = {45: 47, 46: 48}
STS = []
for sid, title, dl, area, sess, cov, hrs, btxt, vtxt, deps, itn in O4.STS:
    k = sid[3:].replace("Mid_", "")
    STS.append(("ST_Exam_" + k, fixch(title), "Exam" + dl, "Exam" + area, sess.replace("I45", "I47").replace("I46", "I48"), cov, hrs, fixch(btxt), fixch(vtxt), [d.replace("TK_Mid_", "TK_Exam_") for d in deps], ITMAP[itn]))
MEAS = [(n, "ST_Ch%02d_PageMeasure" % n) for n in range(1, 9)]
MEAS_TXT = ("MEASURE the page of chapter %d (the newest page in 03-materials/ch%02d/page; if no page exists, report that and stop) with the page tests 9.34.2, 9.35.2 and 9.37.0 (story ST_PageTest_Click is Done), serially, each under flock /tmp/page_test.lock, through sen0401_lineage_page_test_run_v1_2_0.py, "
            "keeping every run as a new log. THIS IS A MEASUREMENT: the page is NOT changed. If a test fails or skips on the page, report it as printed and STOP; do not repair the page and do not edit any test, gate or threshold. "
            "DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES. Free disk is about 2 GB: tell the coordinator at once if it falls under 0.9 GB. One page build at a time; avoid heavy parallel load.")
MEAS_V = "Re-run the three tests on the page under the lock, one at a time; compare the printed results with the executor's logs and the stored results; check no FAIL and no SKIP line (or name each as printed); confirm the page file and every committed file are byte-identical."


def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR30", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLDB[3:] if False else "backlog:admittedByOutput %s ;" % OLDB); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLDB, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; mem = {47: [], 48: [], 49: []}; allids = []
    note = "Admitted by the change request " + CR + " (" + WHEN + "), under the amended mission ex:Mission_V2. One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). The chapter list of the exam is a parameter fixed by the instructor."
    def crit_blocks(k, label, gh, scen_pass, scen_fail, nm):
        return ('\nex:AC3%s_%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS_ChapterCheck ;\n    backlog:measuredWithVersion "checks written by the executor as new files, run by the control on the evidence bridge" ;\n'
                '    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3%s_%s_Passes, ex:TC3%s_%s_NotClaimed .\n'
                'ex:TC3%s_%s_Passes a backlog:TestCase ; rdfs:label "Run the checks of the criterion"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:exercisesCriterion ex:AC3%s_%s ; backlog:coversScenario %s ; backlog:runsOnData ex:Data3%s_%s_Passing ;\n    backlog:hasCaseText "Run the checks of the criterion; they report no failure and exit 0." .\n'
                'ex:TC3%s_%s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on a broken case and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:exercisesCriterion ex:AC3%s_%s ; backlog:coversScenario %s ; backlog:runsOnData ex:Data3%s_%s_Failing ;\n    backlog:hasCaseText %s .\n'
                'ex:Data3%s_%s_Passing a backlog:TestData ; rdfs:label "The new files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasFixtureState "The new files of the task, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .\n'
                'ex:Data3%s_%s_Failing a backlog:TestData ; rdfs:label "The broken case that fails the checks"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasFixtureState %s .\n') % (
            nm, k, lit(label), lit(gh), nm, k, nm, k, nm, k, nm, k, scen_pass, nm, k, nm, k, nm, k, scen_fail, nm, k,
            lit("Run the checks on a fixture that breaks a convention, an item without a source, a paper with a doubtful mark, a changed page or an edited test, and require that nothing is claimed for it."), nm, k, nm, k,
            lit("A fixture that breaks one convention of the criterion, or a page changed during the run, for which the named check must fail."))
    def story_task_blocks(sid, bt, vt, title, dl, ac, obj, it, cov, deps, sess, hrs, btxt, vtxt, itn, role_so):
        cv = "".join("    backlog:coversEntity ex:DE3_%s ; backlog:coversStage backlog:Stage_%s ;\n" % c for c in cov)
        out = ('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
               '    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability %s ; backlog:soThat %s ;\n    backlog:satisfiesDeliverable ex:Del3_%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:%s ;\n%s'
               '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible %s ;\n    backlog:decomposesInto ex:%s, ex:%s ;\n    backlog:hasState backlog:Proposed ;\n'
               '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored by the ranking step of the same change route." ;\n    backlog:hasAuditNote %s .\n') % (
            sid, lit(title), sid, lit(title), it, NEWB, lit(title[0].lower() + title[1:]), lit(role_so), dl, obj, ac, cv, G.EXEC, bt, vt, lit(note))
        for tid, tt, ttype, dp in ((bt, "Build: " + title, "Build", deps), (vt, "Verify: " + title, "Verify", [bt])):
            full = (btxt if ttype == "Build" else vtxt) + " Planned session %s (an estimate, G120: the real start is recorded at work begun); about %.1f hours." % (sess if ttype == "Build" else "builder", hrs if ttype == "Build" else 1.0)
            out += ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ; backlog:responsible %s ;\n'
                    '    backlog:hasInvestmentCategory backlog:Cat_%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Proposed ;\n%s'
                    '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n') % (
                tid, lit(tt), tid, lit(tt), it, NEWB, G.EXEC, "NewCapability" if ttype == "Build" else "Compliance", ttype, ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + d for d in dp)) if dp else "", lit(full))
        return out
    for sid, title, dl, area, sess, cov, hrs, btxt, vtxt, deps, itn in STS:
        k = sid[3:]; bt = "TK_" + k + "_Build"; vt = "TK_" + k + "_Verify"; it = "ex:" + ITERS[itn][0]; mem[itn] += [sid, bt, vt]; allids.append(sid)
        gh = ("Given the new files made for %s when the checks of this criterion are run on the evidence bridge then ALL of: (1) every file is new and no committed file is edited; (2) %s (3) results as printed; if any element fails the work is named failing. Source: the verified gaps G1 to G7 (ex:CR3_ExamMission) and the owner's words of 2026-10-29." % (dl, vtxt))
        L.append(crit_blocks(k, "Criterion of " + title, gh, "ex:Spec3I_Exam_Pass", "ex:Spec3I_Exam_Fail", "E"))
        L.append(story_task_blocks(sid, bt, vt, title, dl, "AC3E_" + k, "Obj3_Exam", it, cov, deps, sess, hrs, btxt, vtxt, itn, "the instructor holds two printed exams and can grade the papers"))
        L.append('ex:Plan3E_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration %d (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:%s, ex:%s ;\n    backlog:refinementProduces ex:Spec3I_Exam, ex:Spec3I_Exam_Pass, ex:Spec3I_Exam_Fail .\n' % (sid, sid, itn, now, it, sid, bt, vt))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    for n, sid in MEAS:
        k = sid[3:]; bt = "TK_" + k + "_Build"; vt = "TK_" + k + "_Verify"; it = "ex:Iter_49"; mem[49] += [sid, bt, vt]; allids.append(sid)
        title = "The page of chapter %d measured with the page tests 9.34.2, 9.35.2 and 9.37.0" % n
        gh = ("Given the page of chapter %d (unchanged) and the page tests 9.34.2, 9.35.2 and 9.37.0 when each is run on it serially under flock /tmp/page_test.lock then ALL of: (1) each run is kept as a new log and the results are recorded as printed; (2) the page file and every committed file are byte-identical (SHA-256 before and after); (3) no test, gate or threshold is edited; "
              "(4) a FAIL or SKIP line is reported as printed, not repaired. Source: the owner's order of 2026-10-29 (chapters 1 to 6 first, 7 and 8 only if time remains)." % n)
        L.append(crit_blocks(k, "Criterion of " + title, gh, "ex:Spec3I_PageMeasure_Pass", "ex:Spec3I_PageMeasure_Fail", "M"))
        L.append(story_task_blocks(sid, bt, vt, title, "PagesMeasured", "AC3M_" + k, "Obj3_PageMeasure", it, [], [], "SEN0401-I49-page%02d" % n, 3.0, MEAS_TXT % (n, n), MEAS_V, 49, "the instructor knows how the page of the chapter stands before it is repaired"))
        L.append('ex:Plan3M_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 49 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:%s, ex:%s ;\n    backlog:refinementProduces ex:Spec3I_PageMeasure, ex:Spec3I_PageMeasure_Pass, ex:Spec3I_PageMeasure_Fail .\n' % (sid, sid, now, it, sid, bt, vt))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    for n, (itid, lab, st, en, goal) in ITERS.items():
        dur = "Planned by the lineage agent on 2026-10-29, NOT started: the start and the end are planned instants (%s to %s UTC), bounded by the tasks and by the owner's order (exam work first; chapter work restarts on Sunday 2026-11-01), not by a calendar; the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
        L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started."), ", ".join("ex:" + x for x in mem[n])))
    L.append("ex:Obj3_Exam backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append("ex:Obj3_PageMeasure backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s for _, s in MEAS))
    L.append('%s a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the exam work under the amended mission and the page measurements in the owner\'s order"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        SC, CR, ", ".join("ex:" + s for s in allids), lit("Decided by the owner in his explicit words of 2026-10-29 (" + WHEN + "): the exam scope is covered by amending the mission and updating the lineage; the chapter work is ordered (pages of chapters 1 to 6 measured first). Applied by the lineage agent. The boundary moved outward by %d stories; new files only." % len(allids))))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange %s and the stories it admits, on the owner\'s explicit word of 2026-10-29; it was Pending before."@en .\n' % (CR, now[:10], SC))
    t += "\n" + "".join(L)
    return t + out_new(t, "Backlog", NEWB[3:], "Out3_ObjectiveR30"), "third lineage, Backlog stage rebuilt: %d stories admitted (seven for the exam work in the planned Iterations 47 and 48, eight page measurements in the planned Iteration 49) with criteria, tasks, planning events and the ScopeChange; the change request is Accepted." % len(allids)


def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete and no work is begun." % (NEWB, prev)


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "abandon4": lambda: ev_abandon4(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]),
          "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
