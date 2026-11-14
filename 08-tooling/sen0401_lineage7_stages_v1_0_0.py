#!/usr/bin/env python3
"""sen0401_lineage7_stages v1.0.0 - stage events (Mission, Scope, Goal, Objective) of ex:Lineage7, the urgent lineage that corrects the chapter 11 deck and page to the owner's rulings of 2026-11-14. Parented to the sixth lineage so both may be active (G104); opens under Profile_Standard from backlog_open_lineage. Usage: python3 sen0401_lineage7_stages_v1_0_0.py mission|scope|goal|objective [PREV_COMMIT]"""
import datetime, glob, importlib.util, os, re, subprocess, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = REPO
FRAMEWORK = os.environ.get('BRSF_ROOT', '/home/claude/altunelyusuf/backlog-roadmap-framework')
LIN = os.path.join(REPO, "07-lineage")
FW = "/home/claude/Ontologies/backlog-roadmap-framework"
BASE = "http://example.org/sen0401-slides-lineage"
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace(BASE + "#")
STAGES = ["Mission", "Scope", "Goal", "Objective", "Backlog"]
CLAUSE = "Every SEN0401 lecture teaches what the third edition of Mastering Bitcoin teaches"


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]


def newest():
    return sorted(glob.glob(os.path.join(LIN, "sen0401_slides_lineage_v*.ttl")), key=ver)[-1]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def next_version(src):
    v = ver(src)
    return "%d.%d.0" % (v[0], v[1] + 1), "%d.%d.%d" % tuple(v)


def header_version(text):
    m = re.search(r'owl:versionInfo "([\d.]+)" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;', text)
    assert m, "no owl:versionInfo header found"
    return m.group(1)


def write_new(src, text, nxt, cur, comment):
    hv = header_version(text)
    assert hv == cur, "header (%s) and filename (%s) disagree - resync first" % (hv, cur)
    pat = re.compile(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(hv))
    repl = 'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, BASE, nxt, BASE, cur)
    t, n = pat.subn(repl, text, count=1)
    assert n == 1, "header not found"
    ident = 'dcterms:identifier "sen0401_slides_lineage"'
    cm = 'rdfs:comment "%s (%s): %s"@en' % (nxt, now()[:10], esc(comment))
    if ident + " ;" in t:
        t2 = t.replace(ident + " ;", ident + " ;\n    " + cm + " ;", 1)
    else:
        t2 = t.replace(ident + " .", ident + " ;\n    " + cm + " .", 1)
    assert t2 != t, "header comment not placed"
    out = os.path.join(LIN, "sen0401_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    assert not os.path.exists(out), out
    rdflib.Graph().parse(data=t2, format="turtle")
    open(out, "w", encoding="utf-8").write(t2)
    return out


def _pv():
    spec = importlib.util.spec_from_file_location("pv", FW + "/03-tooling/backlog_pipeline_verify_v1_15_0.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    tb = sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"))[-1]
    m.STAGE_TYPES = m._load_stage_types(tb, table="v5")
    return m


def digest(text, stage):
    g = rdflib.Graph(); g.parse(data=text, format="turtle")
    return _pv().state_digest(g, "Stage_" + stage, EX.Lineage7)


def output(text, stage):
    i = STAGES.index(stage)
    consumes = ("\n    backlog:consumesOutput ex:Out7_%s ;" % STAGES[i - 1]) if i else ""
    return ('\nex:Out7_%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the seventh lineage"@en ;\n    backlog:belongsToLineage ex:Lineage7 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;%s\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, digest(text, stage))


def fill_previous(text, stage, commit):
    pat = re.compile(r'(ex:Out7_%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % stage, re.S)
    assert pat.search(text), "no PENDING on Out7_" + stage
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, text, count=1)


def set_lineage_status(text, lin, status):
    m = re.search(r"(ex:%s a backlog:Lineage ;.*?)backlog:hasLineageStatus backlog:\w+" % lin, text, re.S)
    assert m
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:" + status + text[m.end():]


def set_status(text, status):
    pat = re.compile(r'(ex:Lineage7 a backlog:Lineage ;.*?)(backlog:hasLineageStatus backlog:\w+ ;\s*)?(backlog:adoptsObligationSet)', re.S)
    m = pat.search(text); assert m
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:%s ;\n    " % status + m.group(3) + text[m.end():]



CLAUSE7 = "Every SEN0401 lecture teaches what the third edition of Mastering Bitcoin teaches"
COMMIT_URG = None


def opening_block():
    import subprocess
    tool = FW + "/03-tooling/backlog_open_lineage_v1_3_0.py"
    out = subprocess.run([sys.executable, tool, "--profile", "Profile_Standard", "--lineage", "Lineage7", "--prefix", "ex"], capture_output=True, text=True, check=True).stdout
    assert "RS_ConcurrentLineages" in out
    return "\n" + out


def lineage_header():
    return ('\nex:Lineage7 a backlog:Lineage ;\n'
            '    rdfs:label "Seventh lineage: the chapter 11 deck and page corrected to the owner\'s rulings of 2026-11-14 (urgent)"@en ;\n'
            '    backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 7 ; backlog:lineageArchived false ;\n'
            '    backlog:parentLineage ex:Lineage6 ;\n'
            '    backlog:adoptsObligationSet backlog:OS_SDLC_v2 .\n') + opening_block()


def mission_block():
    return '\nex:Lineage7 backlog:lineageForMission ex:Mission .\n'


def scope_block():
    return '''
ex:Area7_Ch11 a backlog:ScopeArea ; rdfs:label "The chapter 11 deck and its page, corrected to the deck and page rulings of 2026-11-14"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:areaLocation "03-materials/ch11 (the deck) and 03-materials/ch11/page (the page); the correction script in 08-tooling" ;
    backlog:areaMeasure "1 deck and 1 page, each passing the CME material check (title words, visual per slide, notes of 60-140 words, no prompt markers, code that parses, no untaught lambda, slide code on the page)" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del7_Ch11 a backlog:ScopeDeliverable ; rdfs:label "The chapter 11 deck and page that pass the material rulings"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:derivesFromMissionClause "%(c)s"^^xsd:string ;
    backlog:hasDeliverableText "A new version of the chapter 11 deck and of its page. Every slide title has at least four words; every content slide carries a visual; every presenter note is 60 to 140 words (30 to 140 on the opening, closing and divider slides) and teaches the slide; no code frame carries a prompt marker and every frame parses as shown; no lambda appears in slide code or page code; every slide code frame is on the page; the page has the Slide code tab. The CME material check passes on both, run fresh." ;
    backlog:deliverableForArea ex:Area7_Ch11 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Excl7_Rest a backlog:ScopeExclusion ; rdfs:label "Chapters 12-14 and the older chapters are not corrected here"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:excludesConcern "The decks and pages of chapters 12, 13 and 14, and of chapters 1-10 including 7 and 8. They fail the same rulings and are corrected by later lineages, one lineage per round of chapters." ;
    backlog:hasExclusionRationale "The owner ruled on 2026-11-14 that the corrections come first and that the older files are processed by the next lineages, not all in one lineage, if that causes complications. This lineage keeps the smallest closeable slice: one chapter, one deck and one page." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .
ex:Scope7 a backlog:ScopeStatement ; rdfs:label "Correct the chapter 11 deck and page to the owner's rulings, as an urgent lineage"@en ;
    backlog:belongsToLineage ex:Lineage7 ; backlog:scopeForMission ex:Mission ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:scopeCompletionState backlog:Proposed ;
    backlog:hasScopeStatementText "IN: a corrected chapter 11 deck and page that pass the CME material check. OUT: every other chapter (see the exclusion). The sixth lineage, which admits the finished chapter 11-14 files, is paused by the urgency ceremony while this lineage works and resumes when it is done." ;
    backlog:coversArea ex:Area7_Ch11 ;
    backlog:hasScopeExclusion ex:Excl7_Rest ;
    backlog:producedByStage ex:Out7_Scope ;
    backlog:requiresDeliverable ex:Del7_Ch11 .
ex:Blueprint7 a backlog:Blueprint ; rdfs:label "What the chapter 11 correction is about"@en ;
    backlog:belongsToLineage ex:Lineage7 ; backlog:blueprintFor ex:Scope7 ; backlog:hasDomainEntity ex:DE3_Deck, ex:DE3_InteractivePage .
''' % {"c": CLAUSE7}


def goal_block():
    return '''
ex:G7_Ch11Meets a backlog:Goal ; rdfs:label "The chapter 11 deck and page meet the written material rulings when the check is run fresh"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:derivesFromScope ex:Scope7 ; backlog:goalCoversArea ex:Area7_Ch11 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalOrigin backlog:GoalOrigin_New ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale "Derived from the scope of the seventh lineage: the chapter 11 files fail the owner's rulings of 2026-11-14 on a measured run of the CME material check, and the owner ordered the corrections first, in an urgent lineage." ;
    backlog:producedByStage ex:Out7_Goal .
'''


def objective_block(now_iso):
    return '''
ex:Obj7_Ch11Pass a backlog:Objective ; rdfs:label "Material-check conditions passing on the chapter 11 deck and page: from 2 to 16"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:contributesToGoal ex:G7_Ch11Meets ; backlog:fillsScope ex:Scope7 ; backlog:hasSuccessMetric ex:Met7_Ch11Pass ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of the 16 conditions (8 checks on the deck, 8 on the deck with its page) reported PASS by cme_material_check on the newest chapter 11 deck and page." ;
    backlog:hasBaselineValue "2"^^xsd:decimal ; backlog:hasTargetValue "16"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP7_Ch11Pass ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out7_Objective .
ex:Met7_Ch11Pass a backlog:Metric ; rdfs:label "Material-check conditions passing on the chapter 11 deck and page"@en ; backlog:belongsToLineage ex:Lineage7 .
ex:CP7_Ch11Pass a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the Backlog stage output of this lineage is closed"@en ;
    backlog:checkpointCondition "Taken after the Backlog stage output of this lineage is closed." ; backlog:expectedValue "16"^^xsd:decimal .
ex:Obs70_Ch11Pass a backlog:MetricObservation ; rdfs:label "Baseline measured on 2026-11-14 on deck v2.1.0 and page 9.94.0"@en ;
    backlog:observesMetric ex:Met7_Ch11Pass ; backlog:observationFor ex:Obj7_Ch11Pass ; backlog:hasObservedValue "2"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "cme_material_check_v1_0_0.py run on SEN0401_Ch11_TheBlockchain_3e_v2_1_0.pptx and sen0401_ch11_page_v9_94_0.html: the notes-labels and code-in-page conditions pass, the other conditions fail." .
''' % now_iso


EXEC7 = "ex:Executor_ClaudeCodeSession"
ARTIFACTS7 = '''
ex:DE7_Deck a backlog:DomainEntity ; rdfs:label "Deck - a chapter's lecture slides, corrected to the rulings"@en ; backlog:belongsToLineage ex:Lineage7 .
ex:DE7_InteractivePage a backlog:DomainEntity ; rdfs:label "Interactive page - a chapter's companion page, corrected to the rulings"@en ; backlog:belongsToLineage ex:Lineage7 .
ex:Blueprint7 backlog:hasDomainEntity ex:DE7_Deck, ex:DE7_InteractivePage .
ex:Gap7_Deck_ActiveUse a backlog:BlueprintGap ; rdfs:label "No coverage yet for the deck at the active use stage"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:gapForEntity ex:DE7_Deck ; backlog:gapForStage backlog:Stage_ActiveUse ; backlog:hasGapReason "This urgent lineage corrects one chapter's files at their creation stage; nothing in it plans this later life-cycle stage of the entity, so it is written down as a gap." .\nex:Gap7_Deck_SuspensionException a backlog:BlueprintGap ; rdfs:label "No coverage yet for the deck at the suspension or exception stage"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:gapForEntity ex:DE7_Deck ; backlog:gapForStage backlog:Stage_SuspensionException ; backlog:hasGapReason "This urgent lineage corrects one chapter's files at their creation stage; nothing in it plans this later life-cycle stage of the entity, so it is written down as a gap." .\nex:Gap7_Deck_Termination a backlog:BlueprintGap ; rdfs:label "No coverage yet for the deck at the termination stage"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:gapForEntity ex:DE7_Deck ; backlog:gapForStage backlog:Stage_Termination ; backlog:hasGapReason "This urgent lineage corrects one chapter's files at their creation stage; nothing in it plans this later life-cycle stage of the entity, so it is written down as a gap." .\nex:Gap7_InteractivePage_ActiveUse a backlog:BlueprintGap ; rdfs:label "No coverage yet for the interactive page at the active use stage"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:gapForEntity ex:DE7_InteractivePage ; backlog:gapForStage backlog:Stage_ActiveUse ; backlog:hasGapReason "This urgent lineage corrects one chapter's files at their creation stage; nothing in it plans this later life-cycle stage of the entity, so it is written down as a gap." .\nex:Gap7_InteractivePage_SuspensionException a backlog:BlueprintGap ; rdfs:label "No coverage yet for the interactive page at the suspension or exception stage"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:gapForEntity ex:DE7_InteractivePage ; backlog:gapForStage backlog:Stage_SuspensionException ; backlog:hasGapReason "This urgent lineage corrects one chapter's files at their creation stage; nothing in it plans this later life-cycle stage of the entity, so it is written down as a gap." .\nex:Gap7_InteractivePage_Termination a backlog:BlueprintGap ; rdfs:label "No coverage yet for the interactive page at the termination stage"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:gapForEntity ex:DE7_InteractivePage ; backlog:gapForStage backlog:Stage_Termination ; backlog:hasGapReason "This urgent lineage corrects one chapter's files at their creation stage; nothing in it plans this later life-cycle stage of the entity, so it is written down as a gap." .\nex:Spec7 a backlog:Specification ; rdfs:label "What a chapter deck and page must be under the rulings of 2026-11-14"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:specifiesGoal ex:G7_Ch11Meets ;
    backlog:hasSpecificationText "Deck: every non-divider slide title has at least four words; every non-divider slide carries a visual (picture, native chart, table, group of shapes, or a code frame); every presenter note is 60 to 140 words (30 to 140 on the first, last and divider slides) and teaches its slide without a label prefix; no code frame shows a prompt marker, every code frame parses as shown, no lambda appears unless taught. Page: every slide code frame appears on the page, no prompt marker and no lambda in the page's code, and a Slide code tab lists the slide code in slide order." ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out7_Goal .
ex:Scen7_Nominal a backlog:TestScenario ; rdfs:label "A corrected deck and page pass the material check"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec7 ;
    backlog:hasScenarioText "Given the corrected chapter 11 deck and page, when cme_material_check is run fresh on them, then every condition reports PASS." .
ex:Scen7_Rejection a backlog:TestScenario ; rdfs:label "A deck with a thin note, a bare slide or a prompt marker is refused"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec7 ;
    backlog:hasScenarioText "Given a deck with a note under 60 words, a content slide with no visual, a code frame starting with a prompt marker or a lambda that was not taught, when the check is run, then the matching condition reports FAIL and the story is not Done." .
ex:Model7_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the corrected chapter 11 material"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The instructor teaches from the deck with the notes as the script; the student works the same code on the page; the material check and the three reviewing roles read both." ;
    backlog:describesItem ex:G7_Ch11Meets .
ex:Model7_Activity a backlog:ModelArtifact ; rdfs:label "How the chapter 11 deck and page are corrected"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:hasModelKind backlog:Kind_ActivityDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "Measure the current files with the check; correct titles, notes, visuals, code frames and lambdas in the deck and the page; run the check again - BRANCH: any condition failing sends the work back to the correction step; the three reviewing roles read the result; the new files are versioned and recorded." ;
    backlog:describesItem ex:Obj7_Ch11Pass .
ex:Model7_Sequence a backlog:ModelArtifact ; rdfs:label "Who asks whom when the corrected files are verified"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:hasModelKind backlog:Kind_SequenceDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The correction script rewrites the deck and the page; the session runs the material check and the deck and page tests; the register records the verdicts; the validator reads the register." ;
    backlog:describesItem ex:Obj7_Ch11Pass .
ex:Model7_Class a backlog:ModelArtifact ; rdfs:label "How the chapter 11 correction stories are stored"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "Two Stories (deck, page), each decomposed into four typed Tasks (design, implement, verify, validate), each Story with an acceptance criterion, the lineage's own Definition of Done and its evidence." ;
    backlog:describesItem ex:Obj7_Ch11Pass .
ex:AC7_Ch11 a backlog:AcceptanceCriterion ; rdfs:label "The corrected chapter 11 deck or page passes every condition of the material check on a fresh run"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:hasGherkinText "Given the corrected chapter 11 deck and page, when cme_material_check is run on them, then all conditions report PASS, and when a note is cut below 60 words the notes condition reports FAIL (the check keeps its ability to refuse)." ;
    backlog:satisfiedByArtifact "the material check output on the new deck and page" .
ex:DoD7 a backlog:DefinitionOfDone ; rdfs:label "What finished means for the chapter 11 correction"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:hasDoDCriterion ex:DoD7_CheckPasses, ex:DoD7_NotesTeach, ex:DoD7_CodeRuns, ex:DoD7_StoryNotRepeated .
ex:DoD7_CheckPasses a backlog:DoDCriterion ; rdfs:label "The material check passes on the new deck and page"@en ;
    backlog:hasCheckQuery "python3 08-tooling/cme_material_check_v1_0_0.py DECK PAGE, run fresh." ; backlog:hasExpectedResult "Every condition PASS; the same run on a deck with a planted thin note fails the notes condition." .
ex:DoD7_NotesTeach a backlog:DoDCriterion ; rdfs:label "Every presenter note teaches its slide in the instructor's own words"@en ;
    backlog:hasCheckQuery "The academician and the undergraduate reader each read ten notes drawn at random and answer: could I teach this slide from the note alone?" ; backlog:hasExpectedResult "Both answer yes on all ten; a no is a defect item." .
ex:DoD7_CodeRuns a backlog:DoDCriterion ; rdfs:label "Every code example runs as the slide shows and its page twin runs"@en ;
    backlog:hasCheckQuery "Extract every code frame, run it under the current Python, compare with the slide's shown result; run the page's example tests." ; backlog:hasExpectedResult "Each frame runs and prints what its slide shows; a stale one is named and refused." .
ex:DoD7_StoryNotRepeated a backlog:DoDCriterion ; rdfs:label "No story told in this chapter is told again in another chapter or course without the owner's confirmation"@en ;
    backlog:hasCheckQuery "Compare the chapter's stories with the stories of the other chapters' decks and pages." ; backlog:hasExpectedResult "No story appears twice; a repeat is replaced or confirmed by the owner." .
'''


def _task7(sid, kind, ttype, text, produces=""):
    tid = "TK7_%s_%s" % (sid, kind)
    return tid, (
        'ex:%(tid)s a backlog:ExecutionTask ; rdfs:label "%(kind)s: %(text)s"@en ; backlog:hasIdentifier "%(tid)s" ; backlog:hasTitle "%(kind)s: %(text)s" ;\n'
        '    backlog:belongsToLineage ex:Lineage7 ; backlog:hasTaskType backlog:%(tt)s ; backlog:hasInvestmentCategory backlog:Cat_Compliance ;\n'
        '    backlog:responsible %(ex)s ; backlog:effectiveDefinitionOfDone ex:DoD7 ; backlog:hasState backlog:Proposed ;\n'
        '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story; scoring both would double-count." .\n') % dict(tid=tid, kind=kind, tt=ttype, text=text, ex=EXEC7)


def _story7(kind, what):
    sid = "Ch11_%s" % kind
    st = "ST7_%s" % sid
    tasks = [_task7(sid, "Design", "Task_DesignDefinition", "list what fails and plan the correction of the chapter 11 %s" % what),
             _task7(sid, "Implement", "Task_Implementation", "correct the chapter 11 %s to the rulings" % what),
             _task7(sid, "Verify", "Task_Verification", "run the material check and the code on the corrected %s" % what),
             _task7(sid, "Validate", "Task_Validation", "the three reading roles judge the corrected %s" % what)]
    t = ('ex:%(st)s a backlog:Story ; rdfs:label "Correct the chapter 11 %(what)s to the rulings of 2026-11-14"@en ;\n'
         '    backlog:hasIdentifier "%(st)s" ; backlog:hasTitle "Correct the chapter 11 %(what)s to the rulings of 2026-11-14" ;\n'
         '    backlog:belongsToLineage ex:Lineage7 ; backlog:hasInvestmentCategory backlog:Cat_Compliance ;\n'
         '    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability "the chapter 11 %(what)s to pass the written material rulings" ;\n'
         '    backlog:soThat "the chapter can be taught from notes that teach, slides that show something and code that runs, as the owner ruled on 2026-11-14" ;\n'
         '    backlog:coversEntity ex:%(de)s ; backlog:coversStage backlog:Stage_Creation ;\n'
         '    backlog:satisfiesDeliverable ex:Del7_Ch11 ; backlog:pursuesObjective ex:Obj7_Ch11Pass ; backlog:hasAcceptanceCriterion ex:AC7_Ch11 ;\n'
         '    backlog:effectiveDefinitionOfDone ex:DoD7 ; backlog:responsible %(ex)s ; backlog:hasState backlog:Proposed ;\n'
         '    backlog:standsAlone true ; backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked in the planning step that follows the backlog stage, by BRSF\'s own method." ;\n'
         '    backlog:hasAuditNote "Groomed at the Backlog stage. Its tasks (design, implement, verify, validate) are created at the planning ceremony that puts it into an iteration, because a task needs a planning event in the register." .\n') % dict(st=st, what=what, de=("DE7_Deck" if kind == "Deck" else "DE7_InteractivePage"), ex=EXEC7)
    return st, t


def backlog_stage(t, prev_commit):
    t = fill_previous(t, "Objective", prev_commit)
    t = set_status(t, "LS_Backlogged")
    add = [ARTIFACTS7]; sids = []
    for kind, what in (("Deck", "deck"), ("Page", "page")):
        st, txt = _story7(kind, what); add.append(txt); sids.append("ex:" + st)
    t += "".join(add)
    t += "ex:Obj7_Ch11Pass backlog:metricMovableBy %s .\n" % ", ".join(sids)
    t += output(t, "Backlog")
    return t, "seventh lineage, Backlog stage closed: two groomed correction stories (chapter 11 deck and page), each with an acceptance criterion and the lineage's own Definition of Done; the stage artifacts the obligations name are carried."


def main():
    ev = sys.argv[1]; prev = sys.argv[2] if len(sys.argv) > 2 else None
    src = newest(); t = open(src, encoding="utf-8").read(); nxt, cur = next_version(src)
    now_iso = now()
    if ev == "mission":
        t2 = set_status(t + lineage_header() + mission_block(), "LS_Opened")
        t = t2 + output(t2, "Mission")
        comment = "seventh lineage opened as an urgent lineage parented to the sixth (Profile_Standard from backlog_open_lineage), Mission stage closed; the sixth lineage is untouched."
    elif ev == "scope":
        t = fill_previous(t, "Mission", prev); t = set_status(t, "LS_Scoped"); t2 = t + scope_block()
        t = t2 + output(t2, "Scope"); comment = "seventh lineage, Scope stage closed (chapter 11 deck and page only)."
    elif ev == "goal":
        t = fill_previous(t, "Scope", prev); t = set_status(t, "LS_Goaled"); t2 = t + goal_block()
        t = t2 + output(t2, "Goal"); comment = "seventh lineage, Goal stage closed."
    elif ev == "objective":
        t = fill_previous(t, "Goal", prev); t = set_status(t, "LS_Objectived"); t2 = t + objective_block(now_iso)
        t = t2 + output(t2, "Objective"); comment = "seventh lineage, Objective stage closed."
    elif ev == "backlog":
        t, comment = backlog_stage(t, prev)
    else:
        raise SystemExit("unknown event " + ev)
    out = write_new(src, t, nxt, cur, comment)
    print(os.path.basename(out))


if __name__ == "__main__":
    main()
