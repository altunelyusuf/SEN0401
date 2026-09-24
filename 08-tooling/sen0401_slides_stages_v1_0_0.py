"""Scope, Goal, Objective and Backlog stages of the SEN0401 slide-renewal lineage, forked from SEN0414's.
Chapters come from Mastering Bitcoin 3rd edition's own BOOK.md at tag third_edition_print1."""
import json, os

CHAPTERS = [(n, "Mastering Bitcoin 3rd edition, chapter %d: %s" % (n, t)) for n, t in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chapters.json")))]
KIND = [("Deck", "Deck", "the renewed lecture deck, restyled with PowerPoint's capabilities and rewritten to the edition it rests on"),
        ("Research", "Research", "an RDODI four-stage research run on the chapter's subject, with its pedagogy stage and Courseware profile"),
        ("Page", "Page", "an interactive page for the chapter, enriched with the research results")]


def cid(n):
    return "Ch%02d" % n if n != "T" else "Threads"


def scope_block():
    L = []
    for k, label, what in KIND:
        L.append('\nex:Area_%s a backlog:ScopeArea ;\n    rdfs:label "%s for every taught chapter"@en ;\n    backlog:areaLocation "03-materials/, one per taught chapter" ;\n    backlog:areaMeasure "%d chapters, each with %s" ;\n    backlog:hasScopeLayer backlog:Layer_Product .\n' % (k, label, len(CHAPTERS), what))
    dels = []
    for n, src in CHAPTERS:
        for k, label, what in KIND:
            i = "Del_%s_%s" % (k, cid(n)); dels.append(i)
            L.append('\nex:%s a backlog:ScopeDeliverable ;\n    rdfs:label "%s for %s"@en ;\n    backlog:derivesFromMissionClause "every SEN0401 lecture deck teaches what the textbook teaches"^^xsd:string ;\n    backlog:hasDeliverableText "%s, grounded in %s." ;\n    backlog:deliverableForArea ex:Area_%s ;\n    backlog:hasScopeLayer backlog:Layer_Product ;\n    backlog:hasProductScopeKind backlog:Kind_Functional .\n' % (i, label, src.split(":")[0], what[0].upper() + what[1:], src, k))
    L.append('''
ex:Excl_OldStructure a backlog:ScopeExclusion ;
    rdfs:label "No deck follows the 2nd edition's chapter structure"@en ;
    backlog:excludesConcern "Decks organised by the 2nd edition's twelve chapters, including its Advanced Transactions and Scripting chapter as such." ;
    backlog:hasExclusionRationale "Owner ruling, 2026-09-24: the outline follows the 3rd edition's fourteen chapters; the course teaches the edition students can read for free." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Product .

ex:Scope a backlog:ScopeStatement ;
    rdfs:label "Renew what is taught, deck by deck, on research"@en ;
    backlog:scopeForMission ex:Mission ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:scopeCompletionState backlog:Proposed ;
    backlog:hasScopeStatementText "IN: for each of the fourteen chapters of Mastering Bitcoin's 3rd edition, a deck, the RDODI research behind it, and an interactive page. OUT: decks following the 2nd edition's structure." ;
    backlog:coversArea ex:Area_Deck, ex:Area_Research, ex:Area_Page ;
    backlog:hasScopeExclusion ex:Excl_OldStructure ;
    backlog:producedByStage ex:Out_Scope ;
    backlog:requiresDeliverable %s .

ex:Blueprint a backlog:Blueprint ;
    rdfs:label "What the slide renewal is about"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:blueprintFor ex:Scope, ex:Backlog ;
    backlog:hasDomainEntity ex:DE_Deck, ex:DE_ResearchRun, ex:DE_InteractivePage .
ex:DE_Deck a backlog:DomainEntity ; rdfs:label "Deck - a chapter's lecture slides"@en ; backlog:belongsToLineage ex:Lineage .
ex:DE_ResearchRun a backlog:DomainEntity ; rdfs:label "Research run - an RDODI run on a chapter's subject"@en ; backlog:belongsToLineage ex:Lineage .
ex:DE_InteractivePage a backlog:DomainEntity ; rdfs:label "Interactive page - a chapter's companion page"@en ; backlog:belongsToLineage ex:Lineage .
''' % ", ".join("ex:" + d for d in dels))
    for e in ("Deck", "ResearchRun", "InteractivePage"):
        for st, human in (("Creation", "creation"), ("ActiveUse", "active use"), ("SuspensionException", "suspension or exception"), ("Termination", "termination")):
            L.append('ex:Gap_%s_%s a backlog:BlueprintGap ; rdfs:label "No coverage yet for the %s at the %s stage"@en ; backlog:gapForEntity ex:DE_%s ; backlog:gapForStage backlog:Stage_%s ; backlog:hasGapReason "Admitted work that covers it arrives at the Backlog stage." .\n' % (e, st, e, human, e, st))
    return "".join(L)


GOALS = [("G_DecksTeachTheBook", "Every deck teaches what the 3rd edition teaches", "Area_Deck", "Facing_Mission", ""),
         ("G_ResearchBehindEveryDeck", "Every renewed deck rests on a recorded research run", "Area_Research", "Facing_Scope", ""),
         ("G_PageForEveryDeck", "Every renewed deck has its interactive page", "Area_Page", "Facing_Containment", ""),
         ("G_NothingUntaughtRenewed", "No deck follows the superseded structure", "Area_Deck", "Facing_Exclusion", "\n    backlog:guardsExclusion ex:Excl_OldStructure ;")]


def goal_block():
    L = []
    for i, l, a, f, g in GOALS:
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label "%s"@en ;\n    backlog:belongsToLineage ex:Lineage ; backlog:derivesFromScope ex:Scope ; backlog:goalCoversArea ex:%s ;%s\n    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:%s ;\n    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;\n    backlog:hasGoalRationale "Derived from the scope\'s %s area, and from the owner\'s request of 2026-09-24 for renewed decks, research and interactive pages together." ;\n    backlog:producedByStage ex:Out_Goal .\n' % (i, l, a, g, f, a.split("_")[1].lower()))
    L.append('''
ex:Spec a backlog:Specification ;
    rdfs:label "What a renewed chapter is"@en ; backlog:belongsToLineage ex:Lineage ; backlog:specifiesGoal ex:G_DecksTeachTheBook ;
    backlog:hasSpecificationText "A chapter is renewed when: its deck uses the edition's own terms, order and code, every command or code example on it is reproduced from the book or run and checked; every claim beyond the book traces to a source recorded by the chapter's RDODI run; it is described as a teaching material aligned to the course outcomes it serves; and its interactive page carries the research results." ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out_Goal .
ex:Scen_Renewed a backlog:TestScenario ; rdfs:label "A renewed chapter's examples match the book"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec ;
    backlog:hasScenarioText "Given a renewed deck, when every example on it is checked against the book at tag third_edition_print1 and every executable one is run, then each matches what its slide shows." .
ex:Scen_StaleCodeRefused a backlog:TestScenario ; rdfs:label "A deck carrying superseded content is refused"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec ;
    backlog:hasScenarioText "Given a deck carrying a claim or example taken from the 2nd edition that the 3rd edition changed, when the deck is checked, then it is refused and the item named." .
ex:Model_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the renewed chapters"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The instructor presents a deck in class and uses its research notes; a student reads the deck and works through the interactive page before and after class; the CME session builds each chapter's research, deck and page and checks them before they are taught." ;
    backlog:describesItem ex:G_DecksTeachTheBook .
''')
    return "".join(L)


OBJS = [("Obj_DecksRenewed", "G_DecksTeachTheBook", "Met_DecksRenewed", "renewed decks passing the chapter check", 0, 16, "Dir_Increase"),
        ("Obj_ResearchRecorded", "G_ResearchBehindEveryDeck", "Met_ResearchRecorded", "chapters with a completed RDODI run", 0, 16, "Dir_Increase"),
        ("Obj_PagesBuilt", "G_PageForEveryDeck", "Met_PagesBuilt", "chapters with an interactive page carrying their research", 0, 16, "Dir_Increase"),
        ("Obj_NoUntaughtWork", "G_NothingUntaughtRenewed", "Met_UntaughtWork", "renewal items following the superseded structure", 0, 0, "Dir_Hold")]
MOVERS = {"Obj_DecksRenewed": "Deck", "Obj_ResearchRecorded": "Research", "Obj_PagesBuilt": "Page"}
BASE_AT = "__BASE_AT__"


def objective_block(with_movers):
    L = []
    for i, g, m, what, b, t, d in OBJS:
        mv = ""
        if with_movers and i in MOVERS:
            mv = "\n    backlog:metricMovableBy %s ;" % ", ".join("ex:ST_%s_%s" % (MOVERS[i], cid(n)) for n, _ in CHAPTERS)
        elif with_movers:
            mv = "\n    backlog:metricMovableBy ex:ST_Deck_Ch01 ;"
        L.append('''
ex:%s a backlog:Objective ; rdfs:label "%s: from %d to %d"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:contributesToGoal ex:%s ; backlog:fillsScope ex:Scope ; backlog:hasSuccessMetric ex:%s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %s, read from the course repository's materials part." ;
    backlog:hasBaselineValue "%d"^^xsd:decimal ; backlog:hasTargetValue "%d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%s ;
    backlog:hasCheckpoint ex:CP_%s ;%s
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out_Objective .
ex:%s a backlog:Metric ; rdfs:label "%s"@en ; backlog:belongsToLineage ex:Lineage .
ex:CP_%s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after chapter 1 is taught"@en ;
    backlog:checkpointCondition "Taken after chapter 1 is presented on 2026-09-25, so the remaining chapters are planned on what the first one measured." ;
    backlog:expectedValue "%d"^^xsd:decimal .
ex:Obs0_%s a backlog:MetricObservation ; rdfs:label "Baseline, before any work"@en ;
    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Read from the SEN0401 repository, created empty on 2026-09-24 and holding only this lineage: no deck, no research run, no interactive page." .
''' % (i, what.capitalize(), b, t, g, m, what, b, t, d, i, mv, m, what, i, (1 if t else 0), i, m, i, b, BASE_AT, ))
    L.append('''
ex:Model_Activity a backlog:ModelArtifact ; rdfs:label "How one chapter is renewed"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasModelKind backlog:Kind_ActivityDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "Per chapter, in order: run RDODI's four stages on the subject, with the pedagogy stage and Courseware profile; rewrite the deck from the edition and the research; check every example against the book and, where executable, run it - BRANCH: a mismatch returns to the rewrite; restyle the deck; build the interactive page from the research; describe both as teaching materials; publish through the governed publisher; then the owner presents it." ;
    backlog:describesItem ex:Obj_DecksRenewed .
ex:Model_Sequence a backlog:ModelArtifact ; rdfs:label "Who asks whom when a chapter is checked"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasModelKind backlog:Kind_SequenceDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The session extracts every example from the deck, checks it against the book's source and runs what is executable, reads the chapter's research record for every claim beyond the book, and only then asks the publisher to release the chapter." ;
    backlog:describesItem ex:Obj_DecksRenewed .
''')
    return "".join(L)
