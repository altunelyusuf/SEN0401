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
PLANNED = {1, 2}
# Chapter 2 planned on 2026-09-25 by the owner's instruction "proceed with chapter 2 for both courses", into Iter_2,
# which ends at SEN0401's next class - the course meets on Fridays at 09:00 Istanbul, per its outline.
PLANNED_AT_2 = "2026-09-25T00:24:54"
ITER_OF = {1: "Iter_1", 2: "Iter_2"}
# Started items, at the clock time each began. The kick-off was declared by the owner.
STARTED = {("Research", 1): "2026-09-24T22:23:59", ("Deck", 1): "2026-09-24T22:32:36", ("Page", 1): "2026-09-24T22:28:51", ("Research", 2): "2026-09-25T00:24:54", ("Page", 2): "2026-09-25T00:28:01", ("Deck", 2): "2026-09-25T00:30:58"}
# Re-scoring after the latest completion (BP-D11), at the clock time it was done; components unchanged.
RESCORED_AT = "2026-09-25T06:13:08"

# Finished items and the evidence each closed on. Times from the clock or from commits only.
DONE = {("Research", 1): {"finished": "2026-09-24T22:28:23", "closed": "2026-09-24T22:28:51", "release": "sen0401-v0.7.0 (a69f51d)",
    "spec": "RDODI procedure v1.6.0, Stages 1-3 for Mastering Bitcoin's chapter 1, built by 08-tooling/sen0401_rdodi_build_v1_0_0.py from sen0401_ch01_rdodi_data_v1_0_0.py. All gates PASS after two fixes: RDODI's citation detector could not read W3C as an author (a digit in the name), so W3C is cited as World Wide Web Consortium; and one of the chapter's sections was not named in the document. Stage1.A-B, Stage2.A, C and H, Stage3.A, B, F, E.cov, E.sub and src with RDODI's validator functions; Stage1.C-E, Stage2.B (HermiT consistent), D-G, Stage3.C-E (coverage 25/25), G and H as direct checks."},
    ("Deck", 1): {"finished": "2026-09-24T22:34:12", "closed": "2026-09-24T22:34:30", "release": "the release carrying 03-materials/ch01/SEN0401_Ch01_Introduction_3e.pptx",
    "spec": "08-tooling/ch01-deck/deck_check.py re-ran every computation shown on the deck under Python 3.14.4 - the toy proof of work and the supply schedule - with 0 mismatches; the fixture fixture_stale_deck.pptx, showing 21000000.0 for the supply, was refused naming slide 6. Every other slide's content traces to the book's chapter 1 or the research record, cited in its speaker notes. Rendered and inspected; three faults fixed before closing: an over-long title, chart labels naming halving years not read from any source, and data labels rounding 12.5 to 13."},
    ("Research", 2): {"finished": "2026-09-25T00:27:49", "closed": "2026-09-25T00:28:01", "release": "sen0401-v0.11.0 (934b9c1)",
    "spec": "RDODI procedure v1.6.0, Stages 1-3 for Mastering Bitcoin's chapter 2 by 08-tooling/sen0401_rdodi_build_v1_0_0.py from sen0401_ch02_rdodi_data_v1_0_0.py: all gates PASS, coverage 25/25. Its central quantitative claim was reproduced: a Python transcription of the whitepaper's section 11 procedure gives the paper's own table - 0.2045873 at one confirmation, 0.0002428 at six - to seven decimal places."},
    ("Deck", 2): {"finished": "2026-09-25T00:32:02", "closed": "2026-09-25T00:32:12", "release": "the release carrying 03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e.pptx",
    "spec": "08-tooling/ch02-deck/deck_check.py re-ran the six computations shown on the deck under Python 3.14.4 - satoshi units, the toy fee, change, and the whitepaper's attacker-success procedure - with 0 mismatches; the fixture fixture_stale_deck.pptx, showing 0.0024 for six confirmations, was refused naming slide 9. The PROV-O terms on slide 12 were checked against the W3C Recommendation's text before use."},
    ("Page", 1): {"finished": "2026-09-25T06:12:40", "closed": "2026-09-25T06:13:08", "release": "the release carrying the chapter 1 page",
    "spec": "08-tooling/sen0401_page_test_v2_0_0.py exercised every widget and feature of the chapter 1 page in headless Chromium at 2026-09-25T06:12:40 - every widget passed, every executable example printed via Pyodide exactly what the build interpreter printed, 0 console errors, 0 WCAG 2 AA violations - and a fixture with one stored value altered was refused. RDODI Stage 4 and every automated pedagogy gate pass. The Courseware profile's pedagogical-soundness attestation is the owner's, is not part of this story's definition of done, and is recorded as pending, not claimed."},
    ("Page", 2): {"finished": "2026-09-25T06:12:40", "closed": "2026-09-25T06:13:08", "release": "the release carrying the chapter 2 page",
    "spec": "08-tooling/sen0401_page_test_v2_0_0.py exercised every widget and feature of the chapter 2 page in headless Chromium at 2026-09-25T06:12:40 - every widget passed, every executable example printed via Pyodide exactly what the build interpreter printed, 0 console errors, 0 WCAG 2 AA violations - and a fixture with one stored value altered was refused. RDODI Stage 4 and every automated pedagogy gate pass. The Courseware profile's pedagogical-soundness attestation is the owner's, is not part of this story's definition of done, and is recorded as pending, not claimed."}}

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
    return ('backlog:hasState backlog:' + state + ' ; backlog:memberOfContainer ex:' + ITER_OF[n] + ' ;\n    backlog:hasPriorityScore ex:Score_%s_%s ;\n'
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
                obsnote=("Counted chapters whose Stages 1-3 artefacts are published and pass their gates: %s." % ", ".join("chapter %d" % m for (kk, m) in DONE if kk == "Research" and m <= n) if k == "Research" else ("Counted renewed decks passing the chapter check: %s." % ", ".join("chapter %d" % m for (kk, m) in DONE if kk == "Deck" and m <= n)) if k == "Deck" else ("Counted interactive pages passing their browser tests and Stage 4 gates: %s." % ", ".join("chapter %d" % m for (kk, m) in DONE if kk == "Page" and m <= n))),
                count=len([1 for (kk, m) in DONE if kk == k and m <= n]),
                tool=("rdodi-ecosystem/02-gates/rdodi_pipeline_validator_v1_6_0.py, pyshacl, owlready2 HermiT" if k == "Research" else ("08-tooling/ch%02d-deck/deck_check.py under Python 3.14.4" % n) if k == "Deck" else "08-tooling/sen0401_page_test_v2_0_0.py in headless Chromium, RDODI Stage 4 and pedagogy gates"),
                tnote=("Closed on Stages 1-3 of the RDODI procedure. The pedagogy stage, which this story's refinement placed here, runs over a page artefact - its gates take the page's ABox and HTML - so it moves to the chapter's page story; recorded in Refine2_Research_%s rather than claimed here." % c) if k == "Research" else ("Closed on the deck check and its refused fixture. Times read from the clock." if k == "Deck" else "Closed on the page's browser tests, its refused fixture and its Stage 4 gates. The Courseware attestation, the owner's, is pending and not claimed. Times read from the clock."),
                extra=(("ex:Obs1_Untaught_%s a backlog:MetricObservation ; rdfs:label \"No renewal item following the superseded structure, read after the %s deck closed\"@en ; backlog:observesMetric ex:Met_UntaughtWork ; backlog:observationFor ex:Obj_NoUntaughtWork ; backlog:hasObservedValue \"0\"^^xsd:decimal ; backlog:observedAt \"%s\"^^xsd:dateTime ; backlog:hasObservationMethod \"Counted renewal items following the 2nd edition's superseded chapter structure: none.\" ." % (c, c, d["closed"])) if k == "Deck" else "") + ((("ex:Refine2_Research_%s a backlog:RefinementEvent ; rdfs:label \"Pedagogy stage moved to the page story\"@en ;" % c) + REFINE2_TAIL.replace("%(c)s", c).replace("%(cl)s", d["closed"]) + " .") if k == "Research" else ""))


def planned_block(k, n):
    bv, tc, rr, js = WSJF[k]; c = cid(n)
    return '''
ex:Score_%(k)s_%(c)s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;
    backlog:hasScoreValue "%(v).2f"^^xsd:decimal ; backlog:scoredAt "%(t)s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;
    backlog:hasScoreRationale "WSJF = (business value %(bv)d + time criticality %(tc)d + risk reduction %(rr)d) / job size %(js)d, approved by the owner. Time criticality is set by the class at 09:00 Istanbul on 2026-09-25." .
ex:Plan_%(k)s_%(c)s a backlog:PlanningEvent ; rdfs:label "Planning of %(k)s for %(c)s into the first iteration"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:plannedAt "%(pt)s"^^xsd:dateTime ; backlog:plannedBy backlog:Owner ; backlog:plannedInto ex:%(it)s ;
    backlog:plansItem ex:ST_%(k)s_%(c)s ; backlog:producesTask ex:TK_%(k)s_%(c)s_Build, ex:TK_%(k)s_%(c)s_Verify .
ex:Refine_%(k)s_%(c)s a backlog:RefinementEvent ; rdfs:label "Refinement that made %(k)s for %(c)s ready"@en ;
    backlog:refines ex:ST_%(k)s_%(c)s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%(pt)s"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:%(it)s ; backlog:hasRefinementOutcome "%(o)s" .
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
''' % dict(k=k, c=c, bv=bv, tc=tc, rr=rr, js=js, v=(bv + tc + rr) / js, t=(RESCORED_AT if (RESCORED_AT and (k, n) not in DONE) else (PLANNED_AT_2 if n == 2 else PLANNED_AT)), pt=(PLANNED_AT_2 if n == 2 else PLANNED_AT), it=ITER_OF[n], o=REFINED[k],
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


FEEDBACK = """
ex:Finding_PagesV3OwnerRules a backlog:RetrospectiveFinding ;
    rdfs:label "All three SEN0401 pages rebuilt to the owner's page rules"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch01, ex:ST_Page_Ch02, ex:ST_Page_Numbers ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's review of the Bitcoin in numbers page found four faults and made them rules for every course page: code on the page must really run - the published version showed stored results, so edits changed nothing; agents must answer from their own slice of the ontology and corpus - they gave near-identical answers; a menu click must change the main area first, with the detail card only on explicit request; and the tab row must be the sub-menu of the selected top-level item, not mixed with it. The chapter 1 and 2 pages shared the same design and the same faults." ;
    backlog:hasRemedy "All three pages rebuilt as version 3 from course_page_template_v3_0_0.html, byte-identical to SEN0414's, with SEN0401's own text in course_page_config.json - so the two courses no longer fork their page template. Python runs in Brython, which loads as plain scripts and so also works when published; agents receive only their own concepts, relations, computed results and the research findings; clicks move the main area and details open only on request; one top menu with each subject's tabs as its sub-menu. At 2026-09-25T11:05:41 every rule check in 08-tooling/sen0401_page_test_v3_0_0.py passed on all three pages, every widget included (52, 36 and 23, the nine charts among them), with 0 console errors and 0 WCAG 2 AA violations; a stale-value fixture was refused on each. Two tooling faults surfaced and were fixed: the record script built its folder path before normalising the unit name, and the ABox builder read the objectives' explanatory note as an objective." .

ex:G_ChaptersSeenInData a backlog:Goal ;
    rdfs:label "Chapters 1 and 2 are seen in the network's real data"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:derivesFromScope ex:Scope ; backlog:goalCoversArea ex:Area_Page ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Containment ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale "Added with scope change SC_Numbers, not by the Goal stage: the owner asked for his Bitcoin numbers dashboard to become a course page. It serves the mission's grounding - students see chapter 1's supply schedule and chapter 2's security by computation in Blockchain.com's data." .
ex:Obj_Supplements backlog:contributesToGoal ex:G_ChaptersSeenInData ; backlog:hasCheckpoint ex:CP_Obj_Supplements .
ex:CP_Obj_Supplements a backlog:ObjectiveCheckpoint ; rdfs:label "Reading when the supplementary page closes"@en ;
    backlog:checkpointCondition "Taken when the Bitcoin in numbers page closes, since it is the only item this objective counts." ;
    backlog:expectedValue "1"^^xsd:decimal .

ex:Obj_Supplements a backlog:Objective ; rdfs:label "Owner-requested supplementary pages built: from 0 to 1"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:fillsScope ex:Scope ; backlog:hasSuccessMetric ex:Met_Supplements ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of supplementary pages the owner requested that are published in the course repository and pass their gates and browser tests." ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "1"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:metricMovableBy ex:ST_Page_Numbers ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner .
ex:Met_Supplements a backlog:Metric ; rdfs:label "owner-requested supplementary pages built"@en ; backlog:belongsToLineage ex:Lineage .
ex:Obs0_Supplements a backlog:MetricObservation ; rdfs:label "Baseline, when the request was taken up"@en ;
    backlog:observesMetric ex:Met_Supplements ; backlog:observationFor ex:Obj_Supplements ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "2026-09-25T08:52:21"^^xsd:dateTime ; backlog:hasObservationMethod "Read from the repository: no supplementary page existed." .
ex:Obs1_Supplements a backlog:MetricObservation ; rdfs:label "Supplementary pages read after the Bitcoin in numbers page closed"@en ;
    backlog:observesMetric ex:Met_Supplements ; backlog:observationFor ex:Obj_Supplements ; backlog:hasObservedValue "1"^^xsd:decimal ;
    backlog:observedAt "2026-09-25T09:01:03"^^xsd:dateTime ; backlog:hasObservationMethod "Counted supplementary pages passing their gates and browser tests: Bitcoin in numbers." .
ex:ST_Page_Numbers backlog:pursuesObjective ex:Obj_Supplements .
ex:Finding_ForkedObjectiveTargets a backlog:RetrospectiveFinding ;
    rdfs:label "SEN0401's objectives carried SEN0414's target of 16"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Numbers ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Tying the new page to an objective meant reading SEN0401's objectives closely: all three counting objectives - decks, research runs, pages - had a target of 16, SEN0414's number of taught subjects, carried over when SEN0414's lineage builder was forked on 2026-09-25. SEN0401 has fourteen chapters. Every earlier validation passed because nothing checks a target against the scope it measures." ;
    backlog:hasRemedy "The stage builder now takes the target from the number of chapters, so the three objectives read 14; this finding records that published releases sen0401-v0.4.0 to v0.15.0 stated 16. The lesson reaches past this lineage: the fork is the root cause, which is why consolidating both courses' builders into one CME-held builder is already on the record." .

ex:CR_Numbers a backlog:ChangeRequest ;
    rdfs:label "Turn the owner's Bitcoin numbers dashboard into an interactive course page"@en ;
    backlog:requestsChangeTo ex:Scope ; backlog:hasChangeDirection backlog:Direction_Grow ;
    backlog:hasChangeRequestRationale "The owner asked for a dashboard built by another session - Bitcoin: price, supply and mining power v1.1.0, a claude.ai artifact of 25 September 2026 drawn from Blockchain.com's public charts - to be converted into an interactive page like the chapter pages. The scope covers the fourteen chapters' decks, research and pages; a supplementary page is outside it, so the boundary has to move." ;
    backlog:hasDisposition backlog:Disp_Accepted .

ex:IA_Numbers a backlog:ImpactAssessment ;
    rdfs:label "What the supplementary page costs, measured before building it"@en ;
    backlog:analyzesRequest ex:CR_Numbers ; backlog:identifiesAffectedLineage ex:Lineage ;
    backlog:hasImpactStatement "Measured before the work: the dashboard holds nine charts over one data snapshot (1,471 price samples, 1,500 supply samples, 1,615 hash-rate samples). The chapter tooling assumed numbered chapters throughout - builder, page data, page build, tests, ABox, gate runner - so it had to be generalised to named units, and that generalisation had to be shown to rebuild chapters 1 and 2 unchanged. No chapter story is displaced; chapter 2's iteration keeps its goal." .

ex:SC_Numbers a backlog:ScopeChange ;
    rdfs:label "Scope grown by one supplementary page: Bitcoin in numbers"@en ;
    backlog:fulfillsRequest ex:CR_Numbers ; backlog:changesScope ex:Scope ; backlog:decidedBy backlog:Owner ;
    backlog:admitsItem ex:ST_Page_Numbers ;
    backlog:hasScopeChangeRationale "The boundary moved outward by one page because the owner asked for it. Paid for by generalising the tooling rather than forking it again - the generalised builder and page tooling were shown to regenerate chapters 1 and 2 identically - and by verifying the dashboard's data against its stated source before teaching from it." .

ex:Del_Page_Numbers a backlog:ScopeDeliverable ;
    rdfs:label "Page: Bitcoin in numbers, supplement to chapters 1 and 2"@en ;
    backlog:derivesFromMissionClause "every SEN0401 lecture deck teaches what the textbook teaches"^^xsd:string ;
    backlog:hasDeliverableText "An interactive page with the chapter pages' tools, carrying the owner's dashboard's nine charts over its Blockchain.com snapshot, grounded in verified sources and connected to chapters 1 and 2." ;
    backlog:deliverableForArea ex:Area_Page ; backlog:hasScopeLayer backlog:Layer_Product ; backlog:hasProductScopeKind backlog:Kind_Functional .

ex:ST_Page_Numbers a backlog:Story ; rdfs:label "Page: Bitcoin in numbers"@en ; backlog:hasIdentifier "ST_Page_Numbers" ; backlog:hasTitle "Supplementary page: Bitcoin in numbers" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;
    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability "the Bitcoin numbers dashboard as an interactive page like the chapter pages" ; backlog:soThat "students see chapter 1's supply schedule and chapter 2's security by computation in real data" ;
    backlog:satisfiesDeliverable ex:Del_Page_Numbers ; backlog:hasAcceptanceCriterion ex:AC_Chapter ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;
    backlog:hasState backlog:Done ; backlog:startedAt "2026-09-25T08:52:21"^^xsd:dateTime ; backlog:finishedAt "2026-09-25T09:00:01"^^xsd:dateTime ; backlog:lastAuditedAt "2026-09-25T09:01:03"^^xsd:dateTime ;
    backlog:hasEvidence ex:Ev_Page_Numbers ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:memberOfContainer ex:Iter_2 ;
    backlog:hasPriorityScore ex:Score_Page_Numbers ;
    backlog:decomposesInto ex:TK_Page_Numbers_Build, ex:TK_Page_Numbers_Verify .
ex:Score_Page_Numbers a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;
    backlog:hasScoreValue "12.67"^^xsd:decimal ; backlog:scoredAt "2026-09-25T08:52:21"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;
    backlog:hasScoreRationale "WSJF = (business value 13 + time criticality 20 + risk reduction 5) / job size 3: the page components the owner approved for this lineage's pages, applied unchanged; the owner's request put it first." .
ex:Plan_Page_Numbers a backlog:PlanningEvent ; rdfs:label "Planning of the Bitcoin in numbers page into the second iteration"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:plannedAt "2026-09-25T08:52:21"^^xsd:dateTime ; backlog:plannedBy backlog:Owner ; backlog:plannedInto ex:Iter_2 ;
    backlog:plansItem ex:ST_Page_Numbers ; backlog:producesTask ex:TK_Page_Numbers_Build, ex:TK_Page_Numbers_Verify .
ex:Refine_Page_Numbers a backlog:RefinementEvent ; rdfs:label "Refinement that made the Bitcoin in numbers page ready"@en ;
    backlog:refines ex:ST_Page_Numbers ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "2026-09-25T08:52:21"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_2 ;
    backlog:hasRefinementOutcome "Settled from the owner's request: convert the dashboard into an interactive page similar to the chapter pages, keeping its charts; its data verified against Blockchain.com before use." .
ex:TK_Page_Numbers_Build a backlog:ExecutionTask ; rdfs:label "Bitcoin in numbers page: build"@en ; backlog:hasIdentifier "TK_Page_Numbers_Build" ; backlog:hasTitle "Build the Bitcoin in numbers page" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:hasState backlog:Done ; backlog:startedAt "2026-09-25T08:52:21"^^xsd:dateTime ; backlog:finishedAt "2026-09-25T09:00:01"^^xsd:dateTime ; backlog:hasEvidence ex:Ev_Page_Numbers ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Build ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; a task is not scored on its own." .
ex:TK_Page_Numbers_Verify a backlog:ExecutionTask ; rdfs:label "Bitcoin in numbers page: verify"@en ; backlog:hasIdentifier "TK_Page_Numbers_Verify" ; backlog:hasTitle "Verify the Bitcoin in numbers page" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:hasState backlog:Done ; backlog:startedAt "2026-09-25T08:52:21"^^xsd:dateTime ; backlog:finishedAt "2026-09-25T09:00:01"^^xsd:dateTime ; backlog:hasEvidence ex:Ev_Page_Numbers ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Verify ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; a task is not scored on its own." .
ex:Ev_Page_Numbers a backlog:TestEvidence ; rdfs:label "Checks for the Bitcoin in numbers page"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:attestsCriterion ex:AC_Chapter ; backlog:evidenceVerified true ; backlog:hasTestId "Page/Numbers" ;
    backlog:hasTestSpec "Data: the snapshot spot-checked against the Blockchain.com API - market price and hash rate equal at shared dates. RDODI Stages 1-3 for the unit, all gates PASS, coverage 12 of 12 of the dashboard's own sections. Page: 08-tooling/sen0401_page_test_v2_0_0.py in headless Chromium at 2026-09-25T09:00:01 - all 23 widgets passed, including all nine charts drawn by Chart.js with their data and all three computations printed by Pyodide exactly as the build interpreter printed them; 0 console errors; 0 WCAG 2 AA violations; a fixture with one stored value altered refused. RDODI Stage 4 and every automated pedagogy gate pass; the owner's pedagogical-soundness attestation is pending, not claimed." ;
    backlog:hasVerificationMethod "Gates and browser tests run over the artefacts as published." ;
    backlog:verifiedByTool "08-tooling/sen0401_page_test_v2_0_0.py, rdodi-ecosystem gates, pyshacl, owlready2 HermiT" ; backlog:verifiedAt "2026-09-25T09:00:01"^^xsd:dateTime .
ex:Harness_Page_Numbers a backlog:TestHarness ; rdfs:label "Checks for the Bitcoin in numbers page"@en ;
    backlog:harnessFor ex:ST_Page_Numbers ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:Ev_Page_Numbers .
ex:Start_Page_Numbers a backlog:TransitionEvent ; rdfs:label "Bitcoin in numbers page started"@en ; backlog:transitionedItem ex:ST_Page_Numbers ;
    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "2026-09-25T08:52:21"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "Started when the owner's request was taken up; planning, refinement and start share this clock time because the request carried all three." .
ex:Complete_Page_Numbers a backlog:TransitionEvent ; rdfs:label "Bitcoin in numbers page completed"@en ;
    backlog:transitionedItem ex:ST_Page_Numbers ; backlog:viaTransition backlog:T_Complete ;
    backlog:transitionedAt "2026-09-25T09:01:03"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "Closed on its data check, its gates, its browser tests and its refused fixture. Times read from the clock." .

ex:Finding_ChapterAboxTestName a backlog:RetrospectiveFinding ;
    rdfs:label "The chapter pages' ABoxes named a test script that does not exist"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch01, ex:ST_Page_Ch02 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Regression-checking the generalised tooling against the published chapter pages showed each widget's design test attributed to 08-tooling/sen0401_page_test_v1_0_0.py - a name inherited from SEN0414's first page builder. The script that ran every one of those tests is sen0401_page_test_v2_0_0.py." ;
    backlog:hasRemedy "The page ABox builder now names the real script; both chapter pages' ABoxes re-issued as v2.1.1 with nothing else changed. The pages themselves were not touched." .

ex:Finding_PagesRevisedFromCourseNotes a backlog:RetrospectiveFinding ;
    rdfs:label "The chapter 1 and 2 pages were revised to carry what the decks gained from the course notes"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch01, ex:ST_Page_Ch02 ;
    backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner asked for the interactive pages to be updated as well. The pages are generated from each chapter's domain ontology and document, so the notes' topics were added there rather than to the pages directly: chapter 1 gained a Nature subject (four characteristics, three architectural parts), an Issuance sub-subject (central-bank replacement; deflation, with issuance ending around 2140 computed as about 2140.8 at ten minutes a block) and an Acquisition sub-subject (four ways to get bitcoin); chapter 2 gained the BIP21 payment request with its URI parsed by Python, unconfirmed transactions, small-payment acceptance, the sudoku analogy and the Blockchain Demo. Both pages gained a Discussion tab with the notes' prompts. Doing so exposed labels the camel-case rule had mangled - Bitcoin a t m, Bip21 uri - fixed with explicit labels at their source." ;
    backlog:hasRemedy "Domain ontologies, documents and research records re-published as v1.1.0 with all RDODI gates passing; pages re-published as v2.1.0 with every widget passing in the browser at 2026-09-25T07:55:36 (52 on chapter 1, 36 on chapter 2), 0 console errors, 0 WCAG 2 AA violations, a stale-value fixture refused on each, and every Stage 4 and automated pedagogy gate passing. The owner's pedagogical-soundness attestation remains pending." .

ex:Finding_DecksRevisedFromCourseNotes a backlog:RetrospectiveFinding ;
    rdfs:label "The delivered chapter 1 and 2 decks were revised from the owner's course notes"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Deck_Ch01, ex:ST_Deck_Ch02 ;
    backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "After both decks were closed, the owner supplied his course notes (2021, after the 2nd edition) to fill gaps. Compared slide by slide, they surfaced topics the renewed decks lacked: for chapter 1, what makes Bitcoin different, its four parts behind the scenes, mining replacing a central bank, and the ways to get a first bitcoin; for chapter 2, the invoice as a BIP21 URI, why ten minutes is an average, the sudoku analogy for mining, and an interactive blockchain demo; for both, the owner's discussion prompts. Every topic was checked against the 3rd edition before it was used, and kept in the 3rd edition's words; two items were left out - a 2021 price-prediction source and classified-ad sellers the 3rd edition no longer lists." ;
    backlog:hasRemedy "Revisions recorded here rather than by reopening closed stories: the decks' content grew, their acceptance - every computation re-run, fixtures refused - was re-run on the revised decks at 2026-09-25T06:07:08 and 2026-09-25T06:07:08 with 0 mismatches, and both chapters' research records were re-published as v1.0.1 naming the notes, chapter 12 and the demo as sources, all RDODI gates passing again." .
"""


ITER2 = '''
ex:Iter_2 a backlog:Iteration ; rdfs:label "Second iteration: chapter 2, before the class of 2 October"@en ;
    backlog:hasIdentifier "Iter_2" ; backlog:belongsToLineage ex:Lineage ;
    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-02T06:00:00"^^xsd:dateTime ;
    backlog:hasDurationSource "Owner, 2026-09-25: proceed with chapter 2 for both courses. The end is SEN0401's next class, Friday 2 October at 09:00 Istanbul, from the weekly schedule in the course outline." ;
    backlog:hasSprintGoal "Chapter 2 researched, its deck built and its interactive page built." ;
    backlog:hasMember %s .
'''


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
    if PLANNED: L.append(ITER % (PLANNED_AT, ", ".join("ex:ST_%s_%s" % (k, cid(n)) for k, _, _ in KIND for n in (1,))))
    if 2 in PLANNED: L.append(ITER2 % (PLANNED_AT_2, ", ".join("ex:ST_%s_%s" % (k, cid(2)) for k, _, _ in KIND)))
    return "".join(L)
