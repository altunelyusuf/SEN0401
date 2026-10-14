"""sen0401_lineage_successor_stages v1_0_0 - the five stage events of the successor lineage ex:Lineage2 (Mission, Scope, Goal, Objective, Backlog), called by
sen0401_lineage_succession. One stage per call, one commit per call. A stage output carries the digest the FRAMEWORK'S OWN tool computes
(backlog_pipeline_verify.state_digest, scoped to Lineage2) and closedAtCommit "PENDING" until a later file replaces it with the real hash of the commit that
closed the stage (passed in by the caller after it has committed - never guessed). Ported from sen0414_lineage_outscope_stages_v1_1_0 / _backlog_v1_1_0.

The successor takes in 30 out-scoped stories: chapters 5-7 (9 stories, built before they were planned) by admission, Done only when the evidence bridge verified
the exit-0 chapter check and every cited file's SHA-256 (and every story they depend on is Done); chapters 8-14 (21 stories, not built) by admission as open
pre-lineage items, to be planned in the ordinary way. The three epics and the initiative are admitted open.
"""
__version__ = "1.0.0"
import glob, importlib.util, json, os, re
import rdflib

FW = "/home/claude/Ontologies/backlog-roadmap-framework"
B = rdflib.Namespace("http://example.org/backlog#")
BASE = "http://example.org/sen0401-slides-lineage"
EXN = rdflib.Namespace(BASE + "#")
STAGES = ["Mission", "Scope", "Goal", "Objective", "Backlog"]
GAP = "ex:Gap_OutScope_Ch05_14"
CLAUSE = "Every SEN0401 lecture teaches what the third edition of Mastering Bitcoin teaches"
CHECK = "08-tooling/sen0401_lineage_chapter_check_v1_0_0.py"
KINDNAME = {"Deck": "deck", "Research": "research run", "Page": "page"}


def _pv():
    spec = importlib.util.spec_from_file_location("pv", FW + "/03-tooling/backlog_pipeline_verify_v1_8_0.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    tb = sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"))[-1]
    m.STAGE_TYPES = m._load_stage_types(tb, table="v1")
    return m


def digest(text, stage):
    pv = _pv()
    g = rdflib.Graph(); g.parse(data=text, format="turtle")
    return pv.state_digest(g, "Stage_" + stage, rdflib.URIRef(BASE + "#Lineage2"))


def output(text, stage, prev_commit):
    d = digest(text, stage)
    i = STAGES.index(stage)
    consumes = ("\n    backlog:consumesOutput ex:Out2_%s ;" % STAGES[i - 1]) if i else ""
    return ('\nex:Out2_%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the second lineage"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;%s\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, d)


def fill_previous(text, stage, commit):
    pat = re.compile(r'(ex:Out2_%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % stage, re.S)
    assert pat.search(text), "no PENDING on Out2_" + stage
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, text, count=1)


def set_status(text, status):
    pat = re.compile(r'(ex:Lineage2 a backlog:Lineage ;.*?)(backlog:hasLineageStatus backlog:\w+ ;\s*)?(backlog:adoptsObligationSet)', re.S)
    m = pat.search(text); assert m
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:%s ;\n    " % status + m.group(3) + text[m.end():]


def _dels(kind, chs):
    return ", ".join("ex:Del_%s_Ch%02d" % (kind, n) for n in chs)


# ---------------------------------------------------------------- stage content
def scope_block(M):
    L = ['''
ex:Area2_Admission a backlog:ScopeArea ;
    rdfs:label "The finished chapters 5 to 7 admitted into the register"@en ;
    backlog:belongsToLineage ex:Lineage2 ;
    backlog:areaLocation "07-lineage (this register); the finished files are in 03-materials and 08-tooling, chapters 5 to 7" ;
    backlog:areaMeasure "3 chapters, each with a deck, a research run and a page, recorded Done with their real finish dates and verified evidence" ;
    backlog:hasScopeLayer backlog:Layer_Work .
''']
    for k, plural in (("Decks", "decks"), ("Research", "research runs"), ("Pages", "pages")):
        L.append('''
ex:Del2_%s a backlog:ScopeDeliverable ;
    rdfs:label "The %s of chapters 5 to 7 recorded Done"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText "The three %s (chapters 5 to 7) are recorded Done, each with its real finish date from git and evidence that was run again and verified against the course repository; one whose check fails stays open and is carried in unfinished." ;
    backlog:deliverableForArea ex:Area2_Admission ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
''' % (k, plural, CLAUSE, plural))
    L.append('''
ex:Excl2_NoRebuild a backlog:ScopeExclusion ;
    rdfs:label "The admission builds and rebuilds nothing"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:excludesConcern "Any change to the decks, research runs or pages of chapters 5 to 7 made in order to admit them: they enter this register exactly as they stand in the course repository. An admitted item whose check fails stays open; repairing it is separate work, planned like any other." ;
    backlog:hasExclusionRationale "These chapters were built before they were planned. The admission records them; it does not redo them, and a record that changed its subject would not be evidence of it." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .

ex:Scope2 a backlog:ScopeStatement ;
    rdfs:label "Admit the finished chapters 5 to 7; build chapters 8 to 14 in the ordinary way"@en ;
    backlog:belongsToLineage ex:Lineage2 ; backlog:scopeForMission ex:Mission ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:scopeCompletionState backlog:Proposed ;
    backlog:hasScopeStatementText "IN: (1) the admission of chapters 5 to 7 of Mastering Bitcoin's 3rd edition (9 stories: deck, research and page of each), built and committed before they were planned, recorded as finished with their real finish dates from git and evidence run again against the course repository - an item whose check fails is not recorded Done and is carried in unfinished; (2) what remains of the mission: the deck, the RDODI research and the interactive page of each of chapters 8 to 14 (21 stories), not yet built, planned and built one chapter at a time. Carried in unchanged, not worked here: the three epics and the initiative that group the stories. OUT: building or rebuilding chapters 5 to 7 in order to admit them; decks following the 2nd edition's structure. Nothing else of the first lineage is open: chapters 1 to 4 and the supplementary Numbers page are Done there with their own evidence." ;
    backlog:coversArea ex:Area2_Admission, ex:Area_Deck, ex:Area_Research, ex:Area_Page ;
    backlog:hasScopeExclusion ex:Excl2_NoRebuild, ex:Excl_OldStructure ;
    backlog:producedByStage ex:Out2_Scope ;
    backlog:requiresDeliverable ex:Del2_Decks, ex:Del2_Research, ex:Del2_Pages, %s, %s, %s .

ex:Blueprint2 a backlog:Blueprint ;
    rdfs:label "What the admission and the remaining chapters are about"@en ;
    backlog:belongsToLineage ex:Lineage2 ; backlog:blueprintFor ex:Scope2 ;
    backlog:hasDomainEntity ex:DE2_Deck, ex:DE2_ResearchRun, ex:DE2_InteractivePage .
ex:DE2_Deck a backlog:DomainEntity ; rdfs:label "Deck - a chapter's lecture slides"@en ; backlog:belongsToLineage ex:Lineage2 .
ex:DE2_ResearchRun a backlog:DomainEntity ; rdfs:label "Research run - an RDODI run on a chapter's subject"@en ; backlog:belongsToLineage ex:Lineage2 .
ex:DE2_InteractivePage a backlog:DomainEntity ; rdfs:label "Interactive page - a chapter's companion page"@en ; backlog:belongsToLineage ex:Lineage2 .
''' % (_dels("Deck", M.REMAIN), _dels("Research", M.REMAIN), _dels("Page", M.REMAIN)))
    L.extend(
        'ex:Gap2_%s_%s a backlog:BlueprintGap ; rdfs:label "No coverage yet for the %s at the %s stage"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:gapForEntity ex:DE2_%s ; backlog:gapForStage backlog:Stage_%s ; backlog:hasGapReason "The entity is covered by the first lineage and by the admission of its finished chapters; chapters 8 to 14 arrive at the Backlog stage." .\n'
        % (e, st, h, human, e, st)
        for e, h in (("Deck", "Deck"), ("ResearchRun", "Research run"), ("InteractivePage", "Interactive page"))
        for st, human in (("Creation", "creation"), ("ActiveUse", "active use"), ("SuspensionException", "suspension or exception"), ("Termination", "termination")))
    return "".join(L)


GOALS = [("G2_FinishedAdmitted", "The chapters built before they were planned are in the register as finished", "Facing_Mission", "", "GoalOrigin_Carried", "Area2_Admission"),
         ("G2_EveryAdmittedChapterProven", "Every admitted chapter is recorded Done with evidence that was run again", "Facing_Scope", "", "GoalOrigin_Carried", "Area2_Admission"),
         ("G2_DatesAreGitsDates", "No finish date of an admitted chapter is typed ahead of git", "Facing_Containment", "", "GoalOrigin_New", "Area2_Admission"),
         ("G2_NothingRebuilt", "No admitted chapter is rebuilt to fit its record", "Facing_Exclusion", "\n    backlog:guardsExclusion ex:Excl2_NoRebuild ;", "GoalOrigin_New", "Area2_Admission"),
         ("G2_RemainingChaptersTeachTheBook", "Chapters 8 to 14 are renewed, researched and given a page, so every chapter teaches what the 3rd edition teaches", "Facing_Mission", "", "GoalOrigin_Carried", "Area_Deck")]


def goal_block(M):
    L = []
    for i, label, f, g, origin, area in GOALS:
        gap = ("\n    backlog:goalAnswersGap %s ;" % GAP) if origin == "GoalOrigin_Carried" else ""
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label "%s"@en ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:derivesFromScope ex:Scope2 ; backlog:goalCoversArea ex:%s ;%s\n'
                 '    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:%s ; backlog:hasGoalOrigin backlog:%s ;%s\n'
                 '    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;\n'
                 '    backlog:hasGoalRationale "Derived from the scope of the second lineage and from the owner\'s rule of 2026-10-12: work finished before it was planned is out-scoped, the finished lineage closes, and a successor takes it in with its real dates and builds what remains." ;\n'
                 '    backlog:producedByStage ex:Out2_Goal .\n' % (i, label, area, gap, f, origin, g))
    L.append('''
ex:Spec2 a backlog:Specification ;
    rdfs:label "What an admitted chapter is"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:specifiesGoal ex:G2_FinishedAdmitted ;
    backlog:hasSpecificationText "A chapter is admitted as finished when each of its three stories (deck, research, page) is Done with a finish date that equals the last git commit of the files cited for it, an acceptance criterion, a test harness, a last-audit date, an execution modality and evidence that backlog_evidence_bridge verified against the course repository: a rerunnable chapter check that exits 0, and the built files cited by SHA-256. A story whose files cannot be verified is not Done." ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out2_Goal .
ex:Scen2_Verified a backlog:TestScenario ; rdfs:label "An admitted chapter's check passes and its files match their hashes"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec2 ;
    backlog:hasScenarioText "Given a finished chapter's deck, research and page in the course repository, when the chapter check is run and each cited file is hashed, then the check exits 0 and every hash equals the recorded one." .
ex:Scen2_ChangedFileRefused a backlog:TestScenario ; rdfs:label "A cited file that changed after it was recorded is refused"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec2 ;
    backlog:hasScenarioText "Given a cited file whose bytes differ from the recorded SHA-256, when the evidence bridge is run, then the evidence is not verified and the story cannot be Done." .
ex:Model2_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the admission of the finished chapters"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The owner reads the register to learn which chapters are finished and on what evidence; the course session records each finished chapter with its git date and runs its check; the evidence bridge verifies the check and the file hashes; the framework's order check reads the chain and the admissions." ;
    backlog:describesItem ex:G2_FinishedAdmitted .
''')
    return "".join(L)


# (id, goal, metric, what, baseline, target, direction, movers kind, resolves gap)
OBJS = [("Obj2_AdmittedDone", "G2_FinishedAdmitted", "Met2_AdmittedDone", "admitted stories of chapters 5 to 7 recorded Done", 0, 9, "Dir_Increase", True),
        ("Obj2_EvidenceVerified", "G2_EveryAdmittedChapterProven", "Met2_EvidenceVerified", "admitted stories whose evidence the evidence bridge verified", 0, 9, "Dir_Increase", True),
        ("Obj2_DatesFromGit", "G2_DatesAreGitsDates", "Met2_DatesFromGit", "admitted stories whose finish date equals the last git commit of their cited files", 0, 9, "Dir_Increase", True),
        ("Obj2_NothingRebuilt", "G2_NothingRebuilt", "Met2_Rebuilt", "files of chapters 5 to 7 changed by this lineage", 0, 0, "Dir_Hold", False),
        ("Obj2_DecksRemaining", "G2_RemainingChaptersTeachTheBook", "Met2_DecksRemaining", "renewed decks of chapters 8 to 14 passing the chapter check", 0, 7, "Dir_Increase", True),
        ("Obj2_ResearchRemaining", "G2_RemainingChaptersTeachTheBook", "Met2_ResearchRemaining", "chapters among 8 to 14 with a completed RDODI run", 0, 7, "Dir_Increase", True),
        ("Obj2_PagesRemaining", "G2_RemainingChaptersTeachTheBook", "Met2_PagesRemaining", "chapters among 8 to 14 with an interactive page carrying their research", 0, 7, "Dir_Increase", True)]


def objective_block(now_iso):
    L = []
    for i, g, m, what, b, t, d, movers in OBJS:
        gap = "\n    backlog:resolvesPartialScope %s ;" % GAP if i in ("Obj2_AdmittedDone", "Obj2_DecksRemaining", "Obj2_ResearchRemaining", "Obj2_PagesRemaining") else ""
        L.append('''
ex:%s a backlog:Objective ; rdfs:label "%s: from %d to %d"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:contributesToGoal ex:%s ; backlog:fillsScope ex:Scope2 ; backlog:hasSuccessMetric ex:%s ;%s
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %s, read from this register after the evidence bridge has run against the course repository." ;
    backlog:hasBaselineValue "%d"^^xsd:decimal ; backlog:hasTargetValue "%d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%s ;
    backlog:hasCheckpoint ex:CP2_%s ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out2_Objective .
ex:%s a backlog:Metric ; rdfs:label "%s"@en ; backlog:belongsToLineage ex:Lineage2 .
ex:CP2_%s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the admission is recorded"@en ;
    backlog:checkpointCondition "Taken after the Backlog stage output of this lineage is closed and the evidence bridge has run, so the count is read from verified facts." ;
    backlog:expectedValue "%d"^^xsd:decimal .
ex:Obs20_%s a backlog:MetricObservation ; rdfs:label "Baseline, before any admission or build"@en ;
    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Read from this register at the Objective stage of the second lineage: no story has been admitted as finished yet; the thirty stories of chapters 5 to 14 still read Proposed." .
''' % (i, what.capitalize(), b, t, g, m, gap, what, b, t, d, i, m, what, i, t, i, m, i, b, now_iso))
    L.append('''
ex:Model2_Activity a backlog:ModelArtifact ; rdfs:label "How one finished chapter is admitted"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_ActivityDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "Per story, in order: read from git the files that carry the story and the commit that last changed them; hash each file; run the chapter check - BRANCH: a check that fails leaves the story out of Done and it is carried in unfinished; run the evidence bridge over the evidence; record the story Done with the git finish date, the criterion, the harness, the audit date and the modality; the Backlog output of this lineage admits it. Chapters 8 to 14 are admitted open and then planned and built one chapter at a time." ;
    backlog:describesItem ex:Obj2_AdmittedDone .
ex:Model2_Sequence a backlog:ModelArtifact ; rdfs:label "Who asks whom when an admitted chapter is verified"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_SequenceDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The session asks git for the finish commit of each cited file and hashes the files; the evidence bridge runs the chapter check and compares each hash; the register records the bridge's verdict; the order check and the validator read the register." ;
    backlog:describesItem ex:Obj2_AdmittedDone .
''')
    return "".join(L)


# ---------------------------------------------------------------- the Backlog stage
def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def ev_ids(sid, k):
    return "Ev2_%s" % sid[3:], ["Ev2_%s_File%d" % (sid[3:], i + 1) for i in range(k)]


def evidence_draft(facts, stories):
    """Evidence nodes as they stand BEFORE the bridge: no evidenceVerified. One TestEvidence (the rerunnable chapter check) and one ArtifactEvidence per cited file."""
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <%s#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n" % BASE]
    for sid in stories:
        f = facts["stories"][sid]
        kind, ch = sid.split("_")[1], sid.split("_")[2]
        te, files = ev_ids(sid, len(f["artifacts"]))
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for %s %s"@en ; backlog:attestsCriterion ex:AC_Chapter ;\n'
                 '    backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s" ;\n'
                 '    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s/%s" .\n' % (te, kind, ch, kind, ch, CHECK, CHECK, kind, ch))
        for i, a in enumerate(f["artifacts"]):
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:attestsCriterion ex:AC_Chapter ;\n'
                     '    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"]))
    return "".join(L)


def verdicts(bridge_ttl):
    g = rdflib.Graph(); g.parse(bridge_ttl, format="turtle")
    out = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        out[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), str(g.value(ev, B.verifiedAt)), str(g.value(ev, B.hasVerificationMethod)))
    return out


def story_block(t, sid):
    m = re.search(r"^ex:%s a backlog:[A-Za-z]+.*?\n\n" % re.escape(sid), t, re.S | re.M)
    assert m, sid
    return m


def admit_block(blk, sid):
    n = blk.replace("backlog:admittedByOutput ex:Out_Backlog ;", "backlog:preLineageItem true ; backlog:admittedByOutput ex:Out2_Backlog ;", 1)
    assert n != blk, sid
    return n


ADMISSION_BLOCK = '''
ex:AC2_Admission a backlog:AcceptanceCriterion ; rdfs:label "An out-scoped chapter item is recorded Done only when its check passes and its files match their hashes"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasGherkinText "Given a chapter item that the first lineage out-scoped, when the evidence bridge runs the chapter check against the course repository and compares each cited file's SHA-256, and every item it depends on is also Done, then the item is recorded Done with its finish date from git - and when the check exits non-zero, a hash differs, or a dependency is not Done, the item stays Proposed." ;
    backlog:satisfiedByArtifact "the evidence bridge's verdict on the chapter check and on each cited file, recorded in this register" ; backlog:coveredByCase ex:TC2_NotDoneUnlessVerified .
ex:TC2_NotDoneUnlessVerified a backlog:TestCase ; rdfs:label "Admit an item whose check does not exit 0 and require it to stay Proposed"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:AC2_Admission ; backlog:coversScenario ex:Scen2_ChangedFileRefused ; backlog:runsOnData ex:Data2_FailingCheck ;
    backlog:hasCaseText "Run the bridge over an item whose chapter check exits 1; the item must not be recorded Done and must carry no verified test evidence." .
ex:Data2_FailingCheck a backlog:TestData ; rdfs:label "A chapter item whose check fails when run"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "An admitted item whose chapter check exits non-zero when the bridge runs it, or whose cited file's bytes no longer equal the recorded SHA-256." .
ex:Model2_Class a backlog:ModelArtifact ; rdfs:label "How an admitted chapter item and its evidence are stored"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "A Story (deck, research or page of one chapter) is admitted by the Backlog output of this lineage as a pre-lineage item. A Done story has a start and a finish from git, one TestHarness, one TestEvidence (the chapter check, with the bridge's verdict and time) and one ArtifactEvidence per cited file (path and SHA-256). A story that depends on another may be Done only if that one is. A story of chapters 8 to 14 is admitted open and planned later." ;
    backlog:describesItem ex:Obj2_AdmittedDone .
'''


def lineage1_readings(g, done_now, now_iso, tag):
    """An objective of the FIRST lineage that a newly Done story can move (metricMovableBy) and that has no reading dated at or after that story's finish gets one,
    its value the number of Done stories among its movers, counted from the register (the story's own metric, no new claim)."""
    blk = ""
    for obj in sorted(set(g.subjects(B.metricMovableBy, None)), key=str):
        if (obj, B.belongsToLineage, EXN.Lineage) not in g:
            continue
        movers = set(g.objects(obj, B.metricMovableBy)); hit = [x for x in done_now if EXN[x] in movers]
        if not hit:
            continue
        on = str(obj).split("#")[-1]; mid = str(g.value(obj, B.hasSuccessMetric)).split("#")[-1]
        n = sum(1 for m in movers if (m, B.hasState, B.Done) in g)
        blk += ('ex:Obs%s_%s a backlog:MetricObservation ; rdfs:label "Reading after stories of this objective were recorded Done in the second lineage"@en ;\n'
                '    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
                '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n'
                '    backlog:hasObservationMethod "Counted the stories that can move this objective and read Done in this register version: %d of %d. The stories recorded Done in this version are %s; the others were counted from their existing Done records and were not re-run here." .\n') % (tag, on, mid, on, n, now_iso, n, len(movers), ", ".join(hit))
    return blk


def backlog_stage(t, args, M, now_iso):
    prev, facts_p, bridge_p = args[0], args[1], args[2]
    facts = json.load(open(facts_p)); vd = verdicts(bridge_p)
    t = fill_previous(t, "Objective", prev)
    t = set_status(t, "LS_Backlogged")
    done, kept, add = [], [], []
    verified = {}
    for sid in M.ADMIT_STORIES:
        f = facts["stories"][sid]
        te, files = ev_ids(sid, len(f["artifacts"]))
        verified[sid] = te in vd and vd[te][0] and all(x in vd and vd[x][0] for x in files)
    deps = {sid: re.findall(r"backlog:dependsOn ex:(\w+)", story_block(t, sid).group(0)) for sid in M.ADMIT_STORIES}
    changed = True
    while changed:                   # a Done item may not depend on work that is not Done
        changed = False
        for sid in M.ADMIT_STORIES:
            if verified[sid] and any(d in verified and not verified[d] for d in deps[sid]):
                verified[sid] = False; changed = True
    for sid in M.ADMIT_STORIES:
        f = facts["stories"][sid]
        te, files = ev_ids(sid, len(f["artifacts"]))
        m = story_block(t, sid)
        blk = admit_block(m.group(0), sid)
        if verified[sid]:
            nb = blk.replace("backlog:hasState backlog:Proposed ;", "backlog:hasState backlog:Done ;", 1)
            nb = nb.replace('backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." .',
                            'backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Admitted as finished: this story was never planned, so it is not scored." .', 1)
            assert "Done" in nb and "never planned" in nb, sid
            blk = nb
            done.append(sid)
            aud = vd[te][1]
            kind, ch = sid.split("_")[1], sid.split("_")[2]
            add.append('ex:%s backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n    backlog:hasEvidence %s .\n'
                       % (sid, f["started"], f["finished"], aud, ", ".join("ex:" + x for x in [te] + files)))
            add.append('ex:Harness2_%s a backlog:TestHarness ; rdfs:label "Chapter check for %s %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:%s .\n' % (sid[3:], kind, ch, sid, te))
            add.append('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for %s %s"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                       '    backlog:evidenceVerified true ; backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                       % (te, kind, ch, kind, ch, CHECK, esc(vd[te][2]) + (" (the page test ran against a copy of the page carrying a TEST release key: it proves the page logic, not the instructor's real key)" if kind == "Page" else ""),
                          "backlog_evidence_bridge_v1_1_0 with the course repository as workspace", aud))
            for i, a in enumerate(f["artifacts"]):
                add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                           '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                           % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"], esc(vd[files[i]][2]), vd[files[i]][1]))
        else:
            kept.append(sid)
        t = t.replace(m.group(0), blk)
    for sid in M.REMAIN_STORIES + M.CONTAINERS:      # admitted open: not built (8-14) or containers
        m = story_block(t, sid)
        t = t.replace(m.group(0), admit_block(m.group(0), sid))
    t += "\n" + "".join(add) + ADMISSION_BLOCK
    t += "".join("ex:%s backlog:hasAcceptanceCriterion ex:AC2_Admission .\n" % x for x in M.ADMIT_STORIES + M.CONTAINERS)
    t += "".join("ex:%s backlog:satisfiesDeliverable ex:Del2_%s .\n" % (x, {"Deck": "Decks", "Research": "Research", "Page": "Pages"}[x.split("_")[1]]) for x in M.ADMIT_STORIES)
    for o in ("Obj2_AdmittedDone", "Obj2_EvidenceVerified", "Obj2_DatesFromGit", "Obj2_NothingRebuilt"):
        t += "ex:%s backlog:metricMovableBy %s .\n" % (o, ", ".join("ex:" + s for s in M.ADMIT_STORIES))
    for k, o in (("Deck", "Obj2_DecksRemaining"), ("Research", "Obj2_ResearchRemaining"), ("Page", "Obj2_PagesRemaining")):
        ss = ["ST_%s_Ch%02d" % (k, n) for n in M.REMAIN]
        t += "ex:%s backlog:metricMovableBy %s .\n" % (o, ", ".join("ex:" + s for s in ss))
        t += "".join("ex:%s backlog:pursuesObjective ex:%s .\n" % (s, o) for s in ss)
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    # the lineage-1 objectives need a reading dated at or after each newly Done story's finish: counted from this version
    t += lineage1_readings(g, done, now_iso, "21")
    json.dump({"done": done, "kept_open": kept}, open(os.environ.get("SEN0401_BACKLOG_OUTCOME", "/tmp/sen0401_backlog_outcome.json"), "w"))
    return t + output(t, "Backlog", prev), ("second lineage, Backlog stage closed: the first lineage's out-scoped work is admitted (%d admitted stories of chapters 5-7 recorded Done with bridge-verified evidence%s; "
                                           "chapters 8-14 admitted open, to be planned; the three epics and the initiative carried unchanged)." % (len(done), ("; admitted still open: " + ", ".join(kept)) if kept else ""))


def run(ev, t, args, M):
    now_iso = M.now()
    if ev == "mission":
        t = set_status(t, "LS_Opened")
        return t + output(t, "Mission", None), "second lineage opened under the same Mission (Mission stage closed; the Mission is continued unchanged - its re-affirmation is the owner's act, G14, not performed here)."
    if ev == "fill":
        return fill_previous(t, args[0], args[1]), "closedAtCommit of the %s stage output of the second lineage set to the commit that closed it." % args[0]
    prev = args[0]
    if ev == "scope":
        t = fill_previous(t, "Mission", prev)
        t = set_status(t, "LS_Scoped")
        t += scope_block(M)
        return t + output(t, "Scope", prev), "second lineage, Scope stage closed (admit the finished chapters 5-7; build chapters 8-14)."
    if ev == "goal":
        t = fill_previous(t, "Scope", prev)
        t = set_status(t, "LS_Goaled")
        t += goal_block(M)
        return t + output(t, "Goal", prev), "second lineage, Goal stage closed."
    if ev == "objective":
        t = fill_previous(t, "Goal", prev)
        t = set_status(t, "LS_Objectived")
        t += objective_block(now_iso)
        return t + output(t, "Objective", prev), "second lineage, Objective stage closed."
    if ev == "backlog":
        return backlog_stage(t, args, M, now_iso)
    raise SystemExit("unknown event " + ev)
