"""Backlog stage of the SEN0401 slide lineage: admission only. Every item Proposed; no task yet -
tasks are produced by planning, and only for what is planned into an iteration."""
from sen0401_slides_stages_v1_0_0 import CHAPTERS, KIND, cid

# Planning of 2026-09-24, approved by the owner: chapters 1 and 2 in the first iteration, until
# SEN0401's class at 09:00 Istanbul (06:00 UTC) on 2026-09-25. WSJF components are
# (business value, time criticality, risk reduction, job size). Chapter 1's were proposed and
# approved; chapter 2 was added by the owner at approval and takes the same components, since it is
# taught in the same class.
PLANNED_AT = "2026-09-24T22:23:59"
WSJF = {"Research": (13, 20, 13, 3), "Page": (13, 20, 5, 3), "Deck": (20, 20, 8, 5)}
PLANNED = {1}
# Started items, at the clock time each began. The kick-off was declared by the owner.
STARTED = {("Research", 1): "2026-09-24T22:23:59", ("Deck", 1): "2026-09-24T22:32:36", ("Page", 1): "2026-09-24T22:28:51"}
# Re-scoring after the latest completion (BP-D11), at the clock time it was done; components unchanged.
RESCORED_AT = "2026-09-24T22:34:30"

# Finished items and the evidence each closed on. Times from the clock or from commits only.
DONE = {("Research", 1): {"finished": "2026-09-24T22:28:23", "closed": "2026-09-24T22:28:51", "release": "sen0401-v0.7.0 (a69f51d)",
    "spec": "RDODI procedure v1.6.0, Stages 1-3 for Mastering Bitcoin's chapter 1, built by 08-tooling/sen0401_rdodi_build_v1_0_0.py from sen0401_ch01_rdodi_data_v1_0_0.py. All gates PASS after two fixes: RDODI's citation detector could not read W3C as an author (a digit in the name), so W3C is cited as World Wide Web Consortium; and one of the chapter's sections was not named in the document. Stage1.A-B, Stage2.A, C and H, Stage3.A, B, F, E.cov, E.sub and src with RDODI's validator functions; Stage1.C-E, Stage2.B (HermiT consistent), D-G, Stage3.C-E (coverage 25/25), G and H as direct checks."},
    ("Deck", 1): {"finished": "2026-09-24T22:34:12", "closed": "2026-09-24T22:34:30", "release": "the release carrying 03-materials/ch01/SEN0401_Ch01_Introduction_3e.pptx",
    "spec": "08-tooling/ch01-deck/deck_check.py re-ran every computation shown on the deck under Python 3.14.4 - the toy proof of work and the supply schedule - with 0 mismatches; the fixture fixture_stale_deck.pptx, showing 21000000.0 for the supply, was refused naming slide 6. Every other slide's content traces to the book's chapter 1 or the research record, cited in its speaker notes. Rendered and inspected; three faults fixed before closing: an over-long title, chart labels naming halving years not read from any source, and data labels rounding 12.5 to 13."}}

REFINED = {
    "Research": "Settled: RDODI's four-stage procedure v1.6.0 on the chapter's subject, with its Pedagogy and Professional Standards stage and the Courseware profile; the research record lists every source a later claim rests on.",
    "Deck": "Settled: rewritten from the 3rd edition's chapter and the research record, restyled with PowerPoint's own capabilities, every code example run under current Python before it is shown, and the deck described as a teaching material aligned to the outcomes it serves.",
    "Page": "Settled: one interactive page for the chapter, carrying the research results; published as a page students can open, and described as a teaching material.",
}

OBJ = {"Deck": "Obj_DecksRenewed", "Research": "Obj_ResearchRecorded", "Page": "Obj_PagesBuilt"}


def planned_tail(k, n):
    if n not in PLANNED:
        return 'backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned."'
    if (k, n) in DONE:
        d = DONE[(k, n)]
        state = ('Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ;\n'
                 '    backlog:hasEvidence ex:Ev_%s_%s ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (STARTED[(k, n)], d["finished"], d["closed"], k, cid(n)))
    else:
        state = ('InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % STARTED[(k, n)]) if (k, n) in STARTED else 'Ready'
    return ('backlog:hasState backlog:' + state + ' ; backlog:memberOfContainer ex:Iter_1 ;\n    backlog:hasPriorityScore ex:Score_%s_%s ;\n'
            '    backlog:decomposesInto ex:TK_%s_%s_Build, ex:TK_%s_%s_Verify' % (k, cid(n), k, cid(n), k, cid(n)))


def start_block(k, n):
    if (k, n) not in STARTED or (k, n) == ("Research", 1): return ""  # chapter 1's research started at the kick-off, recorded there
    return '''
ex:Start_%s_%s a backlog:TransitionEvent ; rdfs:label "%s %s started"@en ; backlog:transitionedItem ex:ST_%s_%s ;
    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "%s" .
''' % (k, cid(n), k, cid(n), k, cid(n), STARTED[(k, n)], (
        "Started once its dependency, the chapter's research, was Done. Time read from the clock." if (k, n) != ("Page", 1) else
        "The start was not recorded when the work began. This is its provable lower bound: the commit time of sen0414-v2.9.1, the last release before any page work - bounded, not composed."))


REFINE2_TAIL = """
    backlog:refines ex:ST_Page_%(c)s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%(cl)s"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_1 ;
    backlog:hasRefinementOutcome "RDODI's Pedagogy and Professional Standards stage runs its gates over an interactive page's ABox and HTML (its README: --page, --html), so it belongs to the page story, not the research story where the first refinement put it." """


def closure_block(k, n):
    if (k, n) not in DONE: return ""
    d = DONE[(k, n)]; c = cid(n)
    return '''
ex:Ev_%(k)s_%(c)s a backlog:TestEvidence ; rdfs:label "Checks for %(k)s %(c)s"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:attestsCriterion ex:AC_Chapter ; backlog:evidenceVerified true ; backlog:hasTestId "%(k)s/%(c)s" ;
    backlog:hasTestSpec "%(spec)s" ; backlog:hasVerificationMethod "Gates run over the artefacts as published in %(rel)s." ;
    backlog:verifiedByTool "%(tool)s" ; backlog:verifiedAt "%(fin)s"^^xsd:dateTime .
ex:Harness_%(k)s_%(c)s a backlog:TestHarness ; rdfs:label "Checks for %(k)s %(c)s"@en ;
    backlog:harnessFor ex:ST_%(k)s_%(c)s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:Ev_%(k)s_%(c)s .
ex:Obs1_%(k)s_%(c)s a backlog:MetricObservation ; rdfs:label "%(k)s count read after %(c)s closed"@en ;
    backlog:observesMetric ex:%(met)s ; backlog:observationFor ex:%(obj)s ;
    backlog:hasObservedValue "%(count)d"^^xsd:decimal ; backlog:observedAt "%(cl)s"^^xsd:dateTime ;
    backlog:hasObservationMethod "%(obsnote)s" .
ex:Complete_%(k)s_%(c)s a backlog:TransitionEvent ; rdfs:label "%(k)s %(c)s completed"@en ;
    backlog:transitionedItem ex:ST_%(k)s_%(c)s ; backlog:viaTransition backlog:T_Complete ;
    backlog:transitionedAt "%(cl)s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "%(tnote)s" .
%(extra)s
''' % dict(k=k, c=c, spec=d["spec"], rel=d["release"], fin=d["finished"], cl=d["closed"],
                met={"Research": "Met_ResearchRecorded", "Deck": "Met_DecksRenewed", "Page": "Met_PagesBuilt"}[k], obj=OBJ[k],
                obsnote=("Counted chapters whose Stages 1-3 artefacts are published and pass their gates: %s." % ", ".join("chapter %d" % m for (kk, m) in DONE if kk == "Research" and m <= n) if k == "Research" else "Counted renewed decks passing the chapter check: %s." % ", ".join("chapter %d" % m for (kk, m) in DONE if kk == "Deck" and m <= n)),
                count=len([1 for (kk, m) in DONE if kk == k and m <= n]),
                tool=("rdodi-ecosystem/02-gates/rdodi_pipeline_validator_v1_6_0.py, pyshacl, owlready2 HermiT" if k == "Research" else "08-tooling/ch01-deck/deck_check.py under Python 3.14.4"),
                tnote=("Closed on Stages 1-3 of the RDODI procedure. The pedagogy stage, which this story's refinement placed here, runs over a page artefact - its gates take the page's ABox and HTML - so it moves to the chapter's page story; recorded in Refine2_Research_%s rather than claimed here." % c) if k == "Research" else "Closed on the deck check and its refused fixture. Times read from the clock.",
                extra=(("ex:Obs1_Untaught_%s a backlog:MetricObservation ; rdfs:label \"No renewal item following the superseded structure, read after the %s deck closed\"@en ; backlog:observesMetric ex:Met_UntaughtWork ; backlog:observationFor ex:Obj_NoUntaughtWork ; backlog:hasObservedValue \"0\"^^xsd:decimal ; backlog:observedAt \"%s\"^^xsd:dateTime ; backlog:hasObservationMethod \"Counted renewal items for chapters outside the scope - command-line programs, untaught chapters, the GUI decks: none.\" ." % (c, c, d["closed"])) if k == "Deck" else "") + ((("ex:Refine2_Research_%s a backlog:RefinementEvent ; rdfs:label \"Pedagogy stage moved to the page story\"@en ;" % c) + REFINE2_TAIL.replace("%(c)s", c).replace("%(cl)s", d["closed"]) + " .") if k == "Research" else ""))


def planned_block(k, n):
    bv, tc, rr, js = WSJF[k]; c = cid(n)
    return '''
ex:Score_%(k)s_%(c)s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;
    backlog:hasScoreValue "%(v).2f"^^xsd:decimal ; backlog:scoredAt "%(t)s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;
    backlog:hasScoreRationale "WSJF = (business value %(bv)d + time criticality %(tc)d + risk reduction %(rr)d) / job size %(js)d, approved by the owner. Time criticality is set by the class at 09:00 Istanbul on 2026-09-25." .
ex:Plan_%(k)s_%(c)s a backlog:PlanningEvent ; rdfs:label "Planning of %(k)s for %(c)s into the first iteration"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:plannedAt "%(t)s"^^xsd:dateTime ; backlog:plannedBy backlog:Owner ; backlog:plannedInto ex:Iter_1 ;
    backlog:plansItem ex:ST_%(k)s_%(c)s ; backlog:producesTask ex:TK_%(k)s_%(c)s_Build, ex:TK_%(k)s_%(c)s_Verify .
ex:Refine_%(k)s_%(c)s a backlog:RefinementEvent ; rdfs:label "Refinement that made %(k)s for %(c)s ready"@en ;
    backlog:refines ex:ST_%(k)s_%(c)s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%(t)s"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_1 ; backlog:hasRefinementOutcome "%(o)s" .
ex:TK_%(k)s_%(c)s_Build a backlog:ExecutionTask ; rdfs:label "%(k)s for %(c)s: build"@en ; backlog:hasIdentifier "TK_%(k)s_%(c)s_Build" ; backlog:hasTitle "Build %(k)s %(c)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:%(tstate)s ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Build ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; scoring both would double-count." ;%(dep)s
    backlog:hasAuditNote "Build it." .
ex:TK_%(k)s_%(c)s_Verify a backlog:ExecutionTask ; rdfs:label "%(k)s for %(c)s: verify"@en ; backlog:hasIdentifier "TK_%(k)s_%(c)s_Verify" ; backlog:hasTitle "Verify %(k)s %(c)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:%(tstate)s ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Verify ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; scoring both would double-count." ;%(dep)s
    backlog:hasAuditNote "Run the chapter check and require the stale fixture refused." .
''' % dict(k=k, c=c, bv=bv, tc=tc, rr=rr, js=js, v=(bv + tc + rr) / js, t=(RESCORED_AT if (RESCORED_AT and (k, n) not in DONE) else PLANNED_AT), o=REFINED[k],
          tstate=(('Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence ex:Ev_%s_%s' % (STARTED[(k, n)], DONE[(k, n)]["finished"], k, c)) if (k, n) in DONE else 'Proposed'),
          dep=("" if k == "Research" else "\n    backlog:dependsOn ex:ST_Research_%s ;" % c))


ITER = '''
ex:Iter_1 a backlog:Iteration ; rdfs:label "First iteration: chapter 1, before the 09:00 class of 25 September"@en ;
    backlog:hasIdentifier "Iter_1" ; backlog:belongsToLineage ex:Lineage ;
    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-09-25T06:00:00"^^xsd:dateTime ;
    backlog:hasDurationSource "Owner, 2026-09-25: chapter 1 first and most urgent, ready for SEN0401's class at 09:00 Istanbul (06:00 UTC) on 2026-09-25." ;
    backlog:hasSprintGoal "Chapter 1 researched, its deck built and its interactive page built, ready to present at 09:00." ;
    backlog:hasMember %s .
'''


FEEDBACK = ""


def backlog_block():
    L = ['''
ex:Backlog a backlog:Backlog ; rdfs:label "Work admitted for renewing SEN0401's chapters"@en ;
    backlog:hasIdentifier "Backlog_SEN0401_Slides" ; backlog:belongsToLineage ex:Lineage ; backlog:isRegisterRoot true ;
    backlog:hasState backlog:InProgress ; backlog:producedByStage ex:Out_Backlog ;
    backlog:appliesDefinitionOfDone ex:DoD ; backlog:hasCommitment ex:Commit ; backlog:hasMember ex:Init_Slides .
ex:DoD a backlog:DefinitionOfDone ; rdfs:label "What finished means for a renewed chapter"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasDoDCriterion ex:DoD_CodeRuns, ex:DoD_Sourced, ex:DoD_TruthfulDates .
ex:DoD_CodeRuns a backlog:DoDCriterion ; rdfs:label "Every code example runs as the slide shows"@en ;
    backlog:hasCheckQuery "Extract every code example from the deck and run it under current Python." ;
    backlog:hasExpectedResult "Each prints what its slide shows; a stale example is named and refused." ; backlog:hasCriterionStatus backlog:NotYetEnforceable .
ex:DoD_Sourced a backlog:DoDCriterion ; rdfs:label "Every claim beyond the book has a recorded source"@en ;
    backlog:hasCheckQuery "Compare the deck's and page's claims against the chapter's RDODI research record." ;
    backlog:hasExpectedResult "No claim beyond the edition without a source in the research record." ; backlog:hasCriterionStatus backlog:NotYetEnforceable .
ex:DoD_TruthfulDates a backlog:DoDCriterion ; rdfs:label "Every recorded time is read, never composed"@en ;
    backlog:hasCheckQuery "Compare every start, finish, planning, refinement, scoring and observation time with the clock records and commits." ;
    backlog:hasExpectedResult "None post-dates the commit that carried it; none was written instead of read." ; backlog:hasCriterionStatus backlog:NotYetEnforceable .
ex:Commit a backlog:Commitment ; rdfs:label "This register commits to chapters that teach the book students read"@en ;
    backlog:commitsToGoal ex:G_DecksTeachTheBook ; backlog:commitsToObjective ex:Obj_DecksRenewed ; backlog:commitsToDefinitionOfDone ex:DoD .
ex:Session_Opening a backlog:RegisterSession ; rdfs:label "The session that built this register"@en ;
    backlog:sessionFor ex:Backlog ; backlog:sessionConductedBy "cme-session" ;
    backlog:sessionStartedAt "2026-09-24T22:19:17"^^xsd:dateTime ; backlog:sessionEndedAt "2026-09-24T22:20:36"^^xsd:dateTime ;
    backlog:stateVerifiedAtStart true ;
    backlog:hasSessionScopeNote "Built on 2026-09-25 when the owner made SEN0401's chapter 1 the most urgent work, for its 09:00 class; SEN0401 is not yet registered with CME." ;
    backlog:changedItem ex:Init_Slides .
ex:Kickoff a backlog:TransitionEvent ; rdfs:label "Kick-off: the owner declared execution begun"@en ;
    backlog:transitionedItem ex:ST_Research_Ch01 ; backlog:viaTransition backlog:T_Start ;
    backlog:transitionedAt "2026-09-24T22:23:59"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "Declared by the owner in the words 'Approve and kick off', approving the proposed plan in the same message: chapter 1's three stories scored as SEN0414's were, an iteration ending at the 09:00 class, research first. Planning and kick-off are recorded at the same clock time because the owner gave them in one reply." .
ex:Init_Slides a backlog:Initiative ; rdfs:label "Renew SEN0401's taught chapters"@en ; backlog:hasIdentifier "Init_Slides" ; backlog:hasTitle "Renew SEN0401's chapters" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:Proposed ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasInitiativeKind backlog:InitKind_Development ;
    backlog:producesIncrement "sen0401 0.6.0 onward - one published increment per renewed chapter" ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:appliesDefinitionOfDone ex:DoD ; backlog:coversEntity ex:DE_Deck ;
    backlog:pursuesObjective ex:Obj_DecksRenewed ; backlog:hasApplicableConcern backlog:Concern_Data ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored at planning, through its stories." ;
    backlog:decomposesInto ex:EP_Deck, ex:EP_Research, ex:EP_Page .
ex:AC_Chapter a backlog:AcceptanceCriterion ; rdfs:label "A chapter item is accepted when its check passes and a stale fixture is refused"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasGherkinText "Given a chapter's published deck, research record and page, when every code example is run under current Python and every claim beyond the book is traced to the research record, then all pass - and a deck carrying one stale example is refused, naming it." ;
    backlog:satisfiedByArtifact "the chapter check, run against the release that carried the chapter" ; backlog:coveredByCase ex:TC_StaleExample .
ex:TC_StaleExample a backlog:TestCase ; rdfs:label "Put a stale example on a deck and require it refused"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:exercisesCriterion ex:AC_Chapter ; backlog:coversScenario ex:Scen_StaleCodeRefused ; backlog:runsOnData ex:Data_Stale ;
    backlog:hasCaseText "Insert an example whose output under current Python differs from the slide, run the chapter check, expect refusal naming it." .
ex:Data_Stale a backlog:TestData ; rdfs:label "One example taken from an earlier edition whose output has changed"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasFixtureState "A single code example with the output its slide shows, chosen so current Python prints something else." .
ex:Model_Class a backlog:ModelArtifact ; rdfs:label "How a renewed chapter is stored"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Design ;
    backlog:declaresState "A chapter has one ResearchRun, one Deck and one InteractivePage. The Deck and the Page each derive from the ResearchRun. The Deck and the Page are teaching materials in 03-materials, each described by learning-object metadata and aligned to the outcomes it serves. A Deck carries CodeExamples, each with the output its slide shows." ;
    backlog:describesItem ex:Init_Slides .
ex:Model_Component a backlog:ModelArtifact ; rdfs:label "What produces a renewed chapter"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasModelKind backlog:Kind_ComponentDiagram ; backlog:hasModelLevel backlog:Level_Design ;
    backlog:declaresState "RDODI's four-stage procedure produces the ResearchRun; the textbook ontology and edition supply the content; the deck builder produces the Deck from both; the page builder produces the InteractivePage from the ResearchRun; the chapter check runs examples under current Python and gates publication; the governed publisher releases into the course repository." ;
    backlog:describesItem ex:Init_Slides .
''']
    for k, label, what in KIND:
        L.append('''
ex:EP_%s a backlog:Epic ; rdfs:label "%s for every taught chapter"@en ; backlog:hasIdentifier "EP_%s" ; backlog:hasTitle "%s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:Proposed ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:appliesDefinitionOfDone ex:DoD ;
    backlog:coversEntity ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasApplicableConcern backlog:Concern_Data ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked through its stories' scores at planning." ;
    backlog:decomposesInto %s .
''' % (k, label, k, label, {"Deck": "DE_Deck", "Research": "DE_ResearchRun", "Page": "DE_InteractivePage"}[k], OBJ[k],
       ", ".join("ex:ST_%s_%s" % (k, cid(n)) for n, _ in CHAPTERS)))
        for n, src in CHAPTERS:
            dep = "" if k == "Research" else "\n    backlog:dependsOn ex:ST_Research_%s ;" % cid(n)
            L.append('''
ex:ST_%s_%s a backlog:Story ; rdfs:label "%s: %s"@en ; backlog:hasIdentifier "ST_%s_%s" ; backlog:hasTitle "%s for %s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;
    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability "%s" ; backlog:soThat "students are taught from the edition they read, on researched ground" ;
    backlog:satisfiesDeliverable ex:Del_%s_%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:AC_Chapter ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;%s
    %s .
''' % (k, cid(n), label, src, k, cid(n), label, src.split(":")[0], what, k, cid(n), OBJ[k], dep, planned_tail(k, n)))
            if n in PLANNED:
                L.append(planned_block(k, n))
                L.append(closure_block(k, n))
                L.append(start_block(k, n))
    L.append(FEEDBACK)
    if PLANNED: L.append(ITER % (PLANNED_AT, ", ".join("ex:ST_%s_%s" % (k, cid(n)) for k, _, _ in KIND for n in sorted(PLANNED))))
    return "".join(L)
