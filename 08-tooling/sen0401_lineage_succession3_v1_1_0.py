#!/usr/bin/env python3
"""sen0401_lineage_succession3 v1_1_0 - (1.1.0: no Backlog container and no design concern on the link-pass stories; the Backlog output records the waiver of the class-model obligation) records, in NEW versions of the SEN0401 slides lineage register, the second succession (ruling G125, route "out-scope, close, succeed"; the
owner decided it on 2026-10-18): the second lineage out-scopes its unfinished work, closes complete on what it finished, and a successor (the third lineage) under the same mission
takes the out-scoped work in and admits the two link passes as finished work with their real dates from git. One call = one new file = one event; the caller validates and commits it
alone. Written beside sen0401_lineage_succession v1_1_0 (first succession), whose helpers it uses; that file is not edited.

Usage: sen0401_lineage_succession3_v1_1_0.py EVENT [ARGS]
EVENT: declare | close | mission | scope PREV_COMMIT | goal PREV_COMMIT | objective PREV_COMMIT | backlog PREV_COMMIT FACTS.json BRIDGE.ttl[,BRIDGE2.ttl] | fill STAGE COMMIT
Digests come from the framework's own backlog_pipeline_verify (state_digest, table v4, scoped to Lineage3), times from the clock (UTC), commits from git; a stage output carries
closedAtCommit "PENDING" until the next event, given the real commit, fills it. Nothing is placed that was not computed or read here.
"""
__version__ = "1.1.0"
import datetime, glob, importlib.util, json, os, re, subprocess, sys
import rdflib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S

B, BASE, FW = M.B, M.BASE, M.FW
EXN = rdflib.Namespace(BASE + "#")
STAGES = ["Mission", "Scope", "Goal", "Objective", "Backlog"]
GAP = "ex:Gap_OutScope_Lineage2"
CLAUSE = S.CLAUSE
REPO = M.REPO
CHECK = "08-tooling/sen0401_lineage_chapter_check_v1_1_0.py"
EXEC = "ex:Executor_ClaudeCodeSession"
DECK_SHAS = "63f135e 6df5c90 895cf99 3d5e489 2e5c3bd 7bef4cf 1093656 1be22b9 0f432f8 b4369a8 d9de650 74f559b c918ccc 09c008c".split()
PAGE_SHAS = "20f2ea2 740cf3f c3a12d1 12f5941 c161485 126215a b13ad1f 600c337 b09e22d a401f89 330d09a a534ba3 58b1a30 8c02ca6".split()
DECK_FAIL = [1, 2, 3, 4]       # decks admitted but failing the lineage deck check
PAGE_FAIL = [13]               # page failing its one check


def _pv():
    spec = importlib.util.spec_from_file_location("pv", FW + "/03-tooling/backlog_pipeline_verify_v1_9_0.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    tb = sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"))[-1]
    m.STAGE_TYPES = m._load_stage_types(tb, table="v4")
    return m


def digest(text, stage):
    g = rdflib.Graph(); g.parse(data=text, format="turtle")
    return _pv().state_digest(g, "Stage_" + stage, rdflib.URIRef(BASE + "#Lineage3"), admitted=True)


def output(text, stage, waiver=None):
    i = STAGES.index(stage)
    consumes = ("\n    backlog:consumesOutput ex:Out3_%s ;" % STAGES[i - 1]) if i else ""
    return ('\nex:Out3_%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the third lineage"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;%s\n    backlog:hasStateDigest "%s" ;%s\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, digest(text, stage), waiver or "")


def fill_previous(text, stage, commit):
    pat = re.compile(r'(ex:Out3_%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % stage, re.S)
    assert pat.search(text), "no PENDING on Out3_" + stage
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, text, count=1)


def set_status(text, status, lin="Lineage3"):
    pat = re.compile(r'(ex:%s a backlog:Lineage ;.*?)(backlog:hasLineageStatus backlog:\w+ ;\s*)?(backlog:adoptsObligationSet)' % lin, re.S)
    m = pat.search(text); assert m, lin
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:%s ;\n    " % status + m.group(3) + text[m.end():]


def git_times(shas):
    out = []
    for s in shas:
        r = subprocess.run(["git", "-C", REPO, "show", "-s", "--format=%aI", s], capture_output=True, text=True, check=True).stdout.strip()
        out.append(datetime.datetime.fromisoformat(r).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"))
    return min(out), max(out)


def open_tasks(t, lineage="Lineage2"):
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    return sorted(str(s).split("#")[-1] for s in g.subjects(rdflib.RDF.type, B.ExecutionTask)
                  if (s, B.belongsToLineage, EXN[lineage]) in g and (s, B.hasState, B.Done) not in g and (s, B.hasState, B.Cancelled) not in g)


OPEN_L1 = ["EP_Deck", "EP_Page", "EP_Research", "Init_Slides", "ST_Page_Ch06", "ST_Page_Ch13"]


# ---------------------------------------------------------------- closure events
def ev_declare(t):
    tasks = open_tasks(t); out = tasks   # a lineage can only out-scope its own work (shape, v1.135.0): the open items of the first lineage were out-scoped by the first declaration and stay carried by the second lineage's Backlog output
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    for x in OPEN_L1:     # read, not assumed
        assert (EXN[x], B.hasState, B.Done) not in g, x
    blk = ('\n%s a backlog:PartialScopeDeclaration ;\n'
           '    rdfs:label "Out-scoping of the work of the second lineage that is not finished"@en ;\n'
           '    backlog:declaresGapFor ex:Lineage2 ; backlog:decidedBy backlog:Owner ;\n'
           '    backlog:outScopes %s ;\n'
           '    backlog:describesUncoveredScope "Not Done in this register at the time of this declaration and created during the second lineage: %d tasks (the deck-check fixes of chapters 1 to 4, the stale-fixture work of the deck of chapter 14, the three licence questions of page 9, the stage-4 courseware artefacts of chapters 8 to 14, the Stage3.F failures of the research of chapters 2 to 4, and the build and verify tasks of the page of chapter 13, held open on purpose with the page of chapter 6: their load-time budget and test-design ruling are owner decisions). The open stories, epics and initiative of the first lineage (the pages of chapters 6 and 13, three epics, one initiative) belong to the first lineage, were out-scoped by its own declaration and stay carried by the Backlog output of the second lineage. Two link passes (decks and pages of chapters 1 to 14) were done after their stories were Done; ruling G125 says a link pass is a story of its own, so they are not added to this lineage, whose Backlog stage is closed and digest-verified. All of this leaves the second lineage unchanged and unfinished so that it closes with no unfinished work inside it; the successor lineage under the same mission takes the open work in and admits the two link passes as finished work with their real dates from git. The route is the owner decision of 2026-10-18 for the route \\"out-scope, close, succeed\\" of ruling G125 (G105): the owner confirms it by accepting this record." .\n'
           ) % (GAP, ", ".join("ex:" + x for x in out), len(tasks))
    return t + blk, "the second lineage's unfinished work is out-scoped by an owner-decided PartialScopeDeclaration (%d tasks); nothing else changes." % len(tasks)


def ev_close(t):
    a = re.search(r'ex:Lineage2 a backlog:Lineage ;.*?backlog:hasLineageStatus backlog:LS_Backlogged', t, re.S)
    assert a, "the second lineage is not Backlogged"
    t = set_status(t, "LS_Achieved", "Lineage2")
    blk = ('\nex:Lineage3 a backlog:Lineage ;\n    rdfs:label "Third lineage run for the SEN0401 decks: the link passes done after the second lineage planned its stories, and the work still open"@en ;\n'
           '    backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 3 ; backlog:lineageArchived false ;\n'
           '    backlog:adoptsObligationSet backlog:OS_SDLC_v2 ; backlog:adoptionRecordedAtOpen true .\n'
           '\nex:Succession_Lineage2_3 a backlog:LineageSuccession ;\n    rdfs:label "Succession that takes in the open work of the second lineage and the two link passes"@en ;\n'
           '    backlog:succeedsLineage ex:Lineage2 ; backlog:successorLineage ex:Lineage3 ;\n    backlog:resolvesGap %s ;\n'
           '    backlog:decidedBy backlog:Owner ;\n'
           '    backlog:successionRationale "After the Backlog stage of the second lineage was closed and digest-verified, the decks and pages of chapters 1 to 14 were rebuilt so that every link names its resource and goes straight to it. That work has its own criterion, so it is two stories (ruling G125); a story the closed Backlog stage did not admit moves its digest, so it cannot be added to the second lineage, and a task cannot carry it. The second lineage was therefore left unchanged: its unfinished work was out-scoped in the previous event, it closes complete on what it finished, and a successor under the same mission opens with the Scope of admitting the two link passes as finished work (real dates from git, evidence run through the evidence bridge) and of carrying the open follow-up work. The Mission is continued unchanged; its re-affirmation is the owner\'s act (G14). Cost of waiting: the register cannot state the link passes or start the follow-up of the open parts without breaking the digest; cost of acting: one succession and five stage commits; enforcement value forgone: none, the chains of the first two lineages stay untouched." .\n') % GAP
    return t + blk, "the second lineage is Achieved on its finished scope; the succession ex:Succession_Lineage2_3 under the same mission opens the third lineage ex:Lineage3 and resolves the out-scoping declaration."


# ---------------------------------------------------------------- stage content
def scope_block(t):
    n = len(open_tasks(t))
    L = ['''
ex:Area3_LinkPass a backlog:ScopeArea ;
    rdfs:label "The link passes over the decks and pages of chapters 1 to 14 admitted into the register"@en ;
    backlog:belongsToLineage ex:Lineage3 ;
    backlog:areaLocation "07-lineage (this register); the rebuilt files are in 03-materials and the link registers in 08-tooling, chapters 1 to 14" ;
    backlog:areaMeasure "2 stories (a deck link pass and a page link pass), each recorded Done with its real dates from git and evidence verified by the evidence bridge" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del3_DeckLinkPass a backlog:ScopeDeliverable ;
    rdfs:label "The deck link pass recorded Done"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText "The decks of chapters 1 to 14 rebuilt so that every READ card and resources link names its resource and goes straight to it, each deck with a link register, recorded Done with its real dates from git and evidence that was verified against the course repository; the decks of chapters 1 to 4 fail the lineage deck check and are admitted failing, with the reasons." ;
    backlog:deliverableForArea ex:Area3_LinkPass ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del3_PageLinkPass a backlog:ScopeDeliverable ;
    rdfs:label "The page link pass recorded Done"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText "The interactive pages of chapters 1 to 14 rebuilt with the deck link labels, recorded Done with their real dates from git and evidence that was verified against the course repository; the page of chapter 13 fails its one check and is admitted failing, and the page tests ran with a test release key." ;
    backlog:deliverableForArea ex:Area3_LinkPass ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del3_OpenWorkCarried a backlog:ScopeDeliverable ;
    rdfs:label "The open work of the second lineage carried"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText "The %d open tasks of the second lineage are admitted open, each with an executor, to be finished or ruled on; the page of chapter 6, the page of chapter 13, the three epics and the initiative that the first succession carried stay as they are." ;
    backlog:deliverableForArea ex:Area3_LinkPass ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Excl3_NoRebuild a backlog:ScopeExclusion ;
    rdfs:label "The admission rebuilds nothing and decides nothing for the owner"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:excludesConcern "Any change to the decks or pages of chapters 1 to 14 made in order to admit them: they enter this register exactly as they stand in the course repository, and a deck or page that fails its check is admitted failing. Also the owner decisions the open items wait for (the licence questions, the load-time budget of the page of chapter 6, the test-design ruling of the page of chapter 13)." ;
    backlog:hasExclusionRationale "The link passes were done before their stories existed. The admission records them; it does not redo them, and a record that changed its subject would not be evidence of it. The rulings belong to the owner." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .

ex:Scope3 a backlog:ScopeStatement ;
    rdfs:label "Admit the deck link pass and the page link pass as finished; carry the open work"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:scopeForMission ex:Mission ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:scopeCompletionState backlog:Proposed ;
    backlog:hasScopeStatementText "IN: (1) the admission of the deck link pass and the page link pass over chapters 1 to 14 of Mastering Bitcoin's 3rd edition, done after the stories of those decks and pages were Done and recorded as finished with their real dates from git and evidence run through the evidence bridge - a deck or page that fails its check is admitted failing and named, not Done; (2) the open work of the second lineage, carried in unchanged and with an executor: %d tasks. OUT: rebuilding any deck or page in order to admit it; the owner's decisions (the licence questions, the page of chapter 6 and the page of chapter 13). Nothing else of the first two lineages is open." ;
    backlog:coversArea ex:Area3_LinkPass, ex:Area_Deck, ex:Area_Research, ex:Area_Page ;
    backlog:hasScopeExclusion ex:Excl3_NoRebuild, ex:Excl_OldStructure ;
    backlog:producedByStage ex:Out3_Scope ;
    backlog:requiresDeliverable ex:Del3_DeckLinkPass, ex:Del3_PageLinkPass, ex:Del3_OpenWorkCarried .

ex:Blueprint3 a backlog:Blueprint ;
    rdfs:label "What the link passes and the open work are about"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:blueprintFor ex:Scope3 ;
    backlog:hasDomainEntity ex:DE3_Deck, ex:DE3_ResearchRun, ex:DE3_InteractivePage .
ex:DE3_Deck a backlog:DomainEntity ; rdfs:label "Deck - a chapter's lecture slides"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:DE3_ResearchRun a backlog:DomainEntity ; rdfs:label "Research run - an RDODI run on a chapter's subject"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:DE3_InteractivePage a backlog:DomainEntity ; rdfs:label "Interactive page - a chapter's companion page"@en ; backlog:belongsToLineage ex:Lineage3 .
''' % (CLAUSE, CLAUSE, CLAUSE, n, n)]
    L.extend('ex:Gap3_%s_%s a backlog:BlueprintGap ; rdfs:label "No coverage yet for the %s at the %s stage"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:gapForEntity ex:DE3_%s ; backlog:gapForStage backlog:Stage_%s ; backlog:hasGapReason "The entity is covered by the first two lineages; this lineage admits the link passes over it and carries its open work." .\n'
             % (e, st, h, human, e, st)
             for e, h in (("Deck", "Deck"), ("ResearchRun", "Research run"), ("InteractivePage", "Interactive page"))
             for st, human in (("Creation", "creation"), ("ActiveUse", "active use"), ("SuspensionException", "suspension or exception"), ("Termination", "termination")))
    return "".join(L)


GOALS = [("G3_LinksNameTheirResource", "Every link of a deck or page names its resource and goes straight to it", "Facing_Mission", "", "GoalOrigin_New", "Area3_LinkPass"),
         ("G3_LinkPassesProven", "Both link passes are recorded Done with evidence that was run again", "Facing_Scope", "", "GoalOrigin_New", "Area3_LinkPass"),
         ("G3_FailuresStayVisible", "A deck or page that fails its check is admitted as failing, never as Done", "Facing_Containment", "", "GoalOrigin_New", "Area3_LinkPass"),
         ("G3_NothingRebuilt", "No deck or page is rebuilt to fit its record", "Facing_Exclusion", "\n    backlog:guardsExclusion ex:Excl3_NoRebuild ;", "GoalOrigin_New", "Area3_LinkPass"),
         ("G3_OpenWorkCarried", "The open work of the second lineage is carried, with an executor, until it is finished or ruled on", "Facing_Mission", "", "GoalOrigin_Carried", "Area_Deck")]


def goal_block(t):
    L = []
    for i, label, f, g, origin, area in GOALS:
        gap = ("\n    backlog:goalAnswersGap %s ;" % GAP) if origin == "GoalOrigin_Carried" else ""
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label "%s"@en ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:%s ;%s\n'
                 '    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:%s ; backlog:hasGoalOrigin backlog:%s ;%s\n'
                 '    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;\n'
                 '    backlog:hasGoalRationale "Derived from the scope of the third lineage and from ruling G125: work done after its story was Done is a story of its own; the lineage whose Backlog stage is closed out-scopes the open work, closes, and a successor takes it in with its real dates." ;\n'
                 '    backlog:producedByStage ex:Out3_Goal .\n' % (i, label, area, gap, f, origin, g))
    L.append('''
ex:Spec3 a backlog:Specification ;
    rdfs:label "What an admitted link pass is"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_LinkPassesProven ;
    backlog:hasSpecificationText "A link pass is admitted as finished when its story is Done with dates that equal the first and last git commit of the rebuilt files, an acceptance criterion, a test harness, a last-audit date, an execution modality and evidence that backlog_evidence_bridge verified against the course repository: a rerunnable chapter check that exits 0 for each chapter that passes, and the rebuilt files (and the link registers) cited by SHA-256. A chapter whose check fails is named in the story and is not claimed as passing." ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_Goal .
ex:Scen3_Verified a backlog:TestScenario ; rdfs:label "A rebuilt chapter's check passes and its files match their hashes"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3 ;
    backlog:hasScenarioText "Given a rebuilt deck or page of a chapter in the course repository, when the chapter check is run and each cited file is hashed, then the check exits 0 and every hash equals the recorded one." .
ex:Scen3_ChangedFileRefused a backlog:TestScenario ; rdfs:label "A cited file that changed after it was recorded is refused"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3 ;
    backlog:hasScenarioText "Given a cited file whose bytes differ from the recorded SHA-256, when the evidence bridge is run, then the evidence is not verified and the story cannot be Done." .
ex:Model3_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the admission of the link passes"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The owner reads the register to learn which decks and pages carry the link pass and on what evidence; the course session records the pass with its git dates and runs the chapter checks; the evidence bridge verifies the checks and the file hashes; the framework's order check and digest verifier read the chain." ;
    backlog:describesItem ex:G3_LinkPassesProven .
''')
    return "".join(L)


OBJS = [("Obj3_LinkPassesDone", "G3_LinksNameTheirResource", "Met3_LinkPassesDone", "link-pass stories (deck, page) recorded Done", 0, 2, "Dir_Increase", True),
        ("Obj3_EvidenceVerified", "G3_LinkPassesProven", "Met3_EvidenceVerified", "link-pass stories whose evidence the evidence bridge verified", 0, 2, "Dir_Increase", True),
        ("Obj3_DatesFromGit", "G3_LinkPassesProven", "Met3_DatesFromGit", "link-pass stories whose dates equal the first and last git commit of their rebuilt files", 0, 2, "Dir_Increase", True),
        ("Obj3_FailuresNamed", "G3_FailuresStayVisible", "Met3_FailuresNamed", "failing decks and pages named in the story that admits them", 0, 5, "Dir_Increase", True),
        ("Obj3_NothingRebuilt", "G3_NothingRebuilt", "Met3_Rebuilt", "decks and pages changed by this lineage", 0, 0, "Dir_Hold", False)]


def objective_block(t, now_iso):
    n = len(open_tasks(t))
    objs = OBJS + [("Obj3_OpenWorkFinished", "G3_OpenWorkCarried", "Met3_OpenWorkFinished", "carried follow-up tasks recorded Done", 0, n, "Dir_Increase", True)]
    L = []
    for i, g, m, what, b, tg, d, movers in objs:
        gap = "\n    backlog:resolvesPartialScope %s ;" % GAP if i == "Obj3_OpenWorkFinished" else ""
        L.append('''
ex:%s a backlog:Objective ; rdfs:label "%s: from %d to %d"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:%s ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:%s ;%s
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %s, read from this register after the evidence bridge has run against the course repository." ;
    backlog:hasBaselineValue "%d"^^xsd:decimal ; backlog:hasTargetValue "%d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%s ;
    backlog:hasCheckpoint ex:CP3_%s ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_Objective .
ex:%s a backlog:Metric ; rdfs:label "%s"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3_%s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the admission is recorded"@en ;
    backlog:checkpointCondition "Taken after the Backlog stage output of this lineage is closed and the evidence bridge has run, so the count is read from verified facts." ;
    backlog:expectedValue "%d"^^xsd:decimal .
ex:Obs30_%s a backlog:MetricObservation ; rdfs:label "Baseline, before any admission"@en ;
    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Read from this register at the Objective stage of the third lineage: no link pass has been admitted yet and none of the carried tasks is recorded by this lineage." .
''' % (i, what.capitalize(), b, tg, g, m, gap, what, b, tg, d, i, m, what, i, tg, i, m, i, b, now_iso))
    L.append('''
ex:Model3_Activity a backlog:ModelArtifact ; rdfs:label "How one link pass is admitted"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ActivityDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "Per link pass, in order: read from git the commits that rebuilt the files and the files they changed; hash each file; run the chapter check of each chapter through the evidence bridge - BRANCH: a check that fails leaves that chapter out of the evidence and it is named as failing in the story; record the story Done with the first and last git time, the criterion, the harness, the audit date and the modality; the Backlog output of this lineage admits it." ;
    backlog:describesItem ex:Obj3_LinkPassesDone .
ex:Model3_Sequence a backlog:ModelArtifact ; rdfs:label "Who asks whom when a link pass is verified"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_SequenceDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The session asks git for the commits and hashes the files; the evidence bridge runs each chapter check and compares each hash; the register records the bridge's verdict; the order check, the digest verifier and the validator read the register." ;
    backlog:describesItem ex:Obj3_LinkPassesDone .
''')
    return "".join(L)


# ---------------------------------------------------------------- the Backlog stage
DISC_COMMON = ("Agent-reported, not verified from here: 403 or a bot challenge for the CNBC and CoinGecko links (chapter 1), the NYT and learnmeabitcoin HD-wallets links (chapter 5), the learnmeabitcoin Transaction link (chapter 6) and the Schnorr 1991 article (chapter 8), so those links were not verifiable by the builders; "
               "archive.org copies were used for hashcash, b-money, the bitcoinfoundation 2014 post and the Spilman reply, and raw.githubusercontent.com for GitHub files; Wikipedia stays for the Mt. Gox card (chapter 13) and the Lightning Network, Trezor and Casascius wiki cards (chapter 14); "
               "the agent that rebuilt chapters 8 to 14 edited the committed sen0401_links_v1_0_0.py (the Hashcash entry) after its commit, which breaks the no-edit rule; corrected on the way: the chapter 2 slide 12 linked bitcointalk topic 141 (wrong) and now links topic 183, and the chapter 3 slide 6 date changed from 9 January to 8 January 2009 after Satoshi's post header (Thu Jan 8 14:27:40 EST 2009), \"Six days\" became \"Five days\"; the older chapter 3 pages and the materials register sen0401_materials_v1_4_* still say 9 January (open).")
DISC_DECK = ("The decks of chapters 1 to 4 are admitted but FAIL the lineage deck check: deck_check_v1_0_0.py is missing in the deck folder of chapters 1 and 2, the stale fixtures of chapter 2 are not refused, the notes of chapters 1 to 4 carry SAY/ASK/STORY labels, and the old deck_check hits a NameError and merkle_root refusals on chapters 3 and 4 (it also failed on the old decks); their evidence here is the hash of the deck and its link register only. "
             "The decks of chapters 5 to 14 pass the check through the evidence bridge. " + DISC_COMMON)
DISC_PAGE = ("All page checks ran against a copy of the page carrying a TEST release key: they prove the page logic, not the instructor's real key. The page of chapter 13 FAILS its one check (as before) and is admitted failing, with its file hash only. "
             "The page of chapter 8 fails page test 9.34.0 (a crash after the question-type check; no honest fix found, agent-reported) and passes the newest test, 9.35.0, with 3 skips, which is the test the recorded check runs. The page of chapter 3 is v9.66.0 on template 9.50.0 and supersedes two earlier commits; the first bridge run of chapter 1 failed the load-time budget while other checks ran in parallel and passed when run alone. " + DISC_COMMON)

TPL_TEST = ('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for %s %s, link pass"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n'
            '    backlog:evidenceVerified true ; backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n')
TPL_FILE = ('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n'
            '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n')


def artifact_only_draft(facts, sids, tag, out):
    """Evidence draft for files whose chapter check FAILS: only the SHA-256 of the files is claimed (no test evidence)."""
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <%s#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n" % BASE]
    for sid in sids:
        for i, a in enumerate(facts["stories"][sid]["artifacts"]):
            L.append('ex:Ev3%s_%s_File%d a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:attestsCriterion ex:AC3_X ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n'
                     % (tag, sid[3:], i + 1, os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"]))
    open(out, "w").write("".join(L))


def story_text(kind, ssha, start, fin, aud, ev, harness_ev, deps):
    nm = {"Deck": "deck", "Page": "page"}[kind]
    own = ("every READ card and resources link of the lecture decks names its resource and goes straight to it" if kind == "Deck" else "the interactive pages carry the new deck link labels")
    return ('\nex:ST_%(k)s_LinkPass a backlog:Story ; rdfs:label "%(k)s link pass: chapters 1 to 14"@en ; backlog:hasIdentifier "ST_%(k)s_LinkPass" ; backlog:hasTitle "%(k)s link pass over chapters 1 to 14" ;\n'
            '    backlog:belongsToLineage ex:Lineage3 ; backlog:preLineageItem true ; backlog:admittedByOutput ex:Out3_Backlog ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
            '    backlog:asRole "SEN0401 student and instructor" ; backlog:wantsCapability "%(own)s" ; backlog:soThat "a reader reaches the source a slide cites in one step, from the %(nm)s" ;\n'
            '    backlog:satisfiesDeliverable ex:Del3_%(k)sLinkPass ; backlog:pursuesObjective ex:Obj3_LinkPassesDone ; backlog:hasAcceptanceCriterion ex:AC3_%(k)sLinkPass ;\n'
            '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:responsible %(ex)s ;\n%(deps)s'
            '    backlog:hasState backlog:Done ; backlog:startedAt "%(s)s"^^xsd:dateTime ; backlog:finishedAt "%(f)s"^^xsd:dateTime ; backlog:lastAuditedAt "%(a)s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n'
            '    backlog:hasEvidence %(ev)s ;\n'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Admitted as finished: this story was never planned, so it is not scored." ;\n'
            '    backlog:hasAuditNote "%(note)s" .\n'
            'ex:Harness3_%(k)sLinkPass a backlog:TestHarness ; rdfs:label "Chapter checks for the %(nm)s link pass"@en ; backlog:harnessFor ex:ST_%(k)s_LinkPass ; backlog:hasHarnessEvidence %(hev)s .\n'
            ) % dict(k=kind, nm=nm, own=own, ex=EXEC, deps=deps, s=start, f=fin, a=aud, ev=", ".join("ex:" + x for x in ev), hev=", ".join("ex:" + x for x in harness_ev),
                     note=M.esc((DISC_DECK if kind == "Deck" else DISC_PAGE) + " Dates: first and last git commit of the listed rebuild commits (%s); the commits are %s." % (kind.lower() + " rebuilds", ", ".join(ssha))))


AC_BLOCK = '''
ex:AC3_DeckLinkPass a backlog:AcceptanceCriterion ; rdfs:label "A deck link pass is accepted when the rebuilt decks of the chapters that pass carry a link register and pass the chapter check, and every cited file matches its hash"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasGherkinText "Given a deck that was rebuilt so its READ cards and resources links name their resource and go straight to it, when the evidence bridge runs the chapter check of that chapter against the course repository and compares the SHA-256 of the deck and of its link register, then the chapter is evidenced - and a deck whose check exits non-zero is admitted failing and named, and is not claimed as passing; the decks of chapters 1 to 4 are admitted failing." ;
    backlog:satisfiedByArtifact "the evidence bridge's verdict on each chapter check and on each cited file, recorded in this register" ; backlog:coveredByCase ex:TC3_NotDoneUnlessVerified .
ex:AC3_PageLinkPass a backlog:AcceptanceCriterion ; rdfs:label "A page link pass is accepted when the rebuilt pages of the chapters that pass pass the chapter check and every cited file matches its hash"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasGherkinText "Given a page that was rebuilt with the deck link labels, when the evidence bridge runs the chapter check of that chapter (the page test, with a test release key) and compares the SHA-256 of the page, then the chapter is evidenced - and a page whose check fails is admitted failing and named; the page of chapter 13 is admitted failing." ;
    backlog:satisfiedByArtifact "the evidence bridge's verdict on each chapter check and on each cited file, recorded in this register" ; backlog:coveredByCase ex:TC3_NotDoneUnlessVerified .
ex:TC3_NotDoneUnlessVerified a backlog:TestCase ; rdfs:label "Admit a chapter whose check does not exit 0 and require it to carry no verified test evidence"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:AC3_DeckLinkPass, ex:AC3_PageLinkPass ; backlog:coversScenario ex:Scen3_ChangedFileRefused ; backlog:runsOnData ex:Data3_FailingCheck ;
    backlog:hasCaseText "Run the bridge over a chapter whose check exits 1; the chapter must carry no verified test evidence and the story must name it as failing." .
ex:Data3_FailingCheck a backlog:TestData ; rdfs:label "A chapter whose check fails when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "A chapter whose check exits non-zero when the bridge runs it, or whose cited file's bytes no longer equal the recorded SHA-256." .
'''


WAIVER = ('\n    backlog:obligationWaivedBy backlog:Ob_Backlog_ClassDiagram ;\n    backlog:obligationWaiverReason "%s" ;' % M.esc(
    "The Backlog stage owes a class model of the domain at the analysis level in the lineage. It was not produced at the Objective stage, where the stage digest table v4 counts a model artifact; the Objective output of this lineage was already committed and pushed without it, a committed file is not edited (L-112) and adding the model afterwards would move the recorded Objective digest. "
    "This is the course session's omission, not a decision that no model is owed: the debt stays on the record as an advisory and is paid by a stage revision from the Objective stage if the owner asks for one. The two link-pass stories declare no design concern."))


def readings(g, lineage, now_iso, tag):
    """An objective of the lineage that newly Done stories move gets a reading dated at or after their finish: the count of Done movers, counted from the register."""
    blk = ""
    for obj in sorted(set(g.subjects(B.metricMovableBy, None)), key=str):
        if (obj, B.belongsToLineage, EXN[lineage]) not in g:
            continue
        movers = set(g.objects(obj, B.metricMovableBy)); n = sum(1 for m in movers if (m, B.hasState, B.Done) in g)
        if not n:
            continue
        on = str(obj).split("#")[-1]; mid = str(g.value(obj, B.hasSuccessMetric)).split("#")[-1]
        blk += ('ex:Obs%s_%s a backlog:MetricObservation ; rdfs:label "Reading after the link-pass stories were recorded Done"@en ;\n'
                '    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
                '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n'
                '    backlog:hasObservationMethod "Counted the stories that can move this objective and read Done in this register version: %d of %d." .\n') % (tag, on, mid, on, n, now_iso, n, len(movers))
    return blk


def backlog_stage(t, args, now_iso):
    prev, facts_p, bridge_p = args[0], args[1], args[2]
    facts = json.load(open(facts_p)); vd = {}
    for bp in bridge_p.split(","):
        vd.update(S.verdicts(bp))
    t = fill_previous(t, "Objective", prev); t = set_status(t, "LS_Backlogged")
    tasks = open_tasks(t)
    # (a) the open tasks of the second lineage are admitted by this lineage's Backlog output (tasks are outside the table-v4 digest; the second lineage's digest does not move)
    for tk in tasks:
        i = t.index("ex:%s a backlog:ExecutionTask" % tk); j = t.index("backlog:admittedByOutput ex:Out2_Backlog", i)
        assert j - i < 1500 and "\nex:" not in t[i + 5:j], tk
        t = t[:j] + "backlog:preLineageItem true ; backlog:admittedByOutput ex:Out3_Backlog" + t[j + len("backlog:admittedByOutput ex:Out2_Backlog"):]
    # (b) the two link-pass stories
    add = [AC_BLOCK]
    ds, df = git_times(DECK_SHAS); ps, pf = git_times(PAGE_SHAS)
    audits = []; cover = {}
    for kind, shas, fail, (st_, fi_) in (("Deck", DECK_SHAS, DECK_FAIL, (ds, df)), ("Page", PAGE_SHAS, PAGE_FAIL, (ps, pf))):
        ev, hev = [], []
        for n in range(1, 15):
            sid = "ST_%s_Ch%02d" % (kind, n); f = facts["stories"][sid]
            te = "Ev3LK_%s_Ch%02d" % (kind, n); files = ["%s_File%d" % (te, i + 1) for i in range(len(f["artifacts"]))]
            crit = "AC3_%sLinkPass" % kind
            if n in fail:
                assert not (te in vd and vd[te][0]), sid + " is expected to fail but the bridge verified it"
                assert all(x in vd and vd[x][0] for x in files), sid + ": the file hashes were not verified"
                for i, a in enumerate(f["artifacts"]):
                    add.append(TPL_FILE % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], crit, a["path"], a["sha256"], M.esc(vd[files[i]][2]), vd[files[i]][1]))
                    audits.append(vd[files[i]][1]); ev.append(files[i])
                continue
            assert te in vd and vd[te][0] and all(x in vd and vd[x][0] for x in files), sid + ": the bridge did not verify the chapter check or a file"
            add.append(TPL_TEST % (te, kind, "Ch%02d" % n, crit, kind, "Ch%02d" % n, CHECK, M.esc(vd[te][2]), vd[te][1]))
            for i, a in enumerate(f["artifacts"]):
                add.append(TPL_FILE % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], crit, a["path"], a["sha256"], M.esc(vd[files[i]][2]), vd[files[i]][1]))
            audits.append(vd[te][1]); ev += [te] + files; hev.append(te)
        cover[kind] = (ev, hev, shas, st_, fi_)
    for kind in ("Deck", "Page"):
        ev, hev, shas, st_, fi_ = cover[kind]
        aud = max(vd[x][1] for x in ev)
        deps = "    backlog:dependsOn ex:ST_Deck_LinkPass ;\n" if kind == "Page" else ""
        add.append(story_text(kind, shas, st_, fi_, aud, ev, hev, deps))
    t += "\n" + "".join(add)
    for o in ("Obj3_LinkPassesDone", "Obj3_EvidenceVerified", "Obj3_DatesFromGit", "Obj3_FailuresNamed", "Obj3_NothingRebuilt"):
        t += "ex:%s backlog:metricMovableBy ex:ST_Deck_LinkPass, ex:ST_Page_LinkPass .\n" % o
    t += "ex:Obj3_OpenWorkFinished backlog:metricMovableBy %s .\n" % ", ".join("ex:" + x for x in tasks)
    # (c) every open item carried names an executor (L2)
    t += "".join("ex:%s backlog:responsible %s .\n" % (x, EXEC) for x in M_OPEN_L1_NO_EXEC(t))
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    t += readings(g, "Lineage3", now_iso, "31")
    # (d) an open item's score may not predate a completion in the register (L3): re-run, same components and value, dated now
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    lastfin = max(str(x) for x in g.objects(None, B.finishedAt)); rescored = []
    for sc in sorted(set(g.subjects(rdflib.RDF.type, B.PriorityScore)), key=str):
        items = list(g.subjects(B.hasPriorityScore, sc))
        if not items or any((i, B.hasState, B.Done) in g or (i, B.hasState, B.Cancelled) in g for i in items) or str(g.value(sc, B.scoredAt)) >= lastfin:
            continue
        sid = str(sc).split("#")[-1]
        t, n = re.subn(r'(ex:%s a backlog:PriorityScore[^\n]*\n[^\n]*backlog:scoredAt )"[^"]*"' % re.escape(sid), r'\g<1>"%s"' % now_iso, t, count=1)
        assert n == 1, sid
        t += 'ex:%s rdfs:comment "Re-run %s: the components and the value are unchanged; it had to be dated after the completions recorded in this version."@en .\n' % (sid, now_iso[:10]); rescored.append(sid)
    json.dump({"tasks_admitted": tasks, "rescored": rescored}, open(os.environ.get("SEN0401_BACKLOG_OUTCOME3", "/tmp/sen0401_backlog_outcome3.json"), "w"))
    return t + output(t, "Backlog", WAIVER), ("third lineage, Backlog stage closed: the %d open tasks of the second lineage are admitted open with an executor; the deck link pass and the page link pass are admitted as finished stories with their git dates, "
                                      "criterion, harness, audit date, modality and bridge-verified evidence (decks of chapters 1-4 and the page of chapter 13 admitted failing, with file hashes only). The first-lineage items the first succession carried (the pages of chapters 6 and 13, three epics, the initiative) stay admitted by the second lineage's Backlog output: moving them would move its digest." % len(tasks))


def M_OPEN_L1_NO_EXEC(t):
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    return [x for x in OPEN_L1 if (EXN[x], B.responsible, None) not in g]


def run(ev, t, args, now_iso):
    if ev == "mission":
        t = set_status(t, "LS_Opened")
        return t + output(t, "Mission"), "third lineage opened under the same Mission (Mission stage closed; the Mission is continued unchanged - its re-affirmation is the owner's act, G14, not performed here)."
    if ev == "fill":
        return fill_previous(t, args[0], args[1]), "closedAtCommit of the %s stage output of the third lineage set to the commit that closed it." % args[0]
    if ev == "scope":
        t = fill_previous(t, "Mission", args[0]); t = set_status(t, "LS_Scoped"); t += scope_block(t)
        return t + output(t, "Scope"), "third lineage, Scope stage closed (admit the deck link pass and the page link pass; carry the open work)."
    if ev == "goal":
        t = fill_previous(t, "Scope", args[0]); t = set_status(t, "LS_Goaled"); t += goal_block(t)
        return t + output(t, "Goal"), "third lineage, Goal stage closed."
    if ev == "objective":
        t = fill_previous(t, "Goal", args[0]); t = set_status(t, "LS_Objectived"); t += objective_block(t, now_iso)
        return t + output(t, "Objective"), "third lineage, Objective stage closed."
    if ev == "backlog":
        return backlog_stage(t, args, now_iso)
    raise SystemExit("unknown event " + ev)


EVENTS = {"declare": ev_declare, "close": ev_close}


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    if ev in EVENTS:
        nt, comment = EVENTS[ev](t)
    else:
        nt, comment = run(ev, t, sys.argv[2:], M.now())
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
