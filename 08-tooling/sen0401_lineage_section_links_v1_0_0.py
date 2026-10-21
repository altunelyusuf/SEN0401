#!/usr/bin/env python3
"""sen0401_lineage_section_links v1_0_0 - change route (rulings G113, G125, G127, G133, G134, G136) for the owner's answer of 2026-10-22 about the ERD of the pages of chapters 10 and 11, quoted in OWNER_ACT.
The owner chose option (b) of the open change request ex:CR3_PageErd, widened: the relationships between the sections of a chapter are discovered with the OEE relationship taxonomy and STATED IN THE CHAPTER RESEARCH AS LINKS
(object properties between the sections' individuals or classes), not as text. The deliverable is new (the scope excluded research changes other than chapter 8), the third lineage is in its closed Backlog stage, so the route is a
StageRevision from the Scope stage (G127). The work is planned into a NEW iteration, ex:Iter_14, because the goal of ex:Iter_13 is frozen at its start and an iteration is not extended (the owner's rule of 2026-10-21 10:14 Istanbul).
One call = one new file = one event; the caller validates, checks and commits each alone. Events, in order:
  change | retract | scope PREV | goal PREV | objective PREV | backlog PREV
The Disposition of ex:CR3_PageErd becomes Accepted in the backlog version, with the ScopeChange. Nothing is waived, no criterion is changed, and no recorded digest is rewritten."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T

lit, esc = G.lit, M.esc
EXEC = G.EXEC
ITER = "ex:Iter_14"
REV = "ex:Revision_Lineage3_Scope3"
WHEN = "Thursday 2026-10-22 01:24 Istanbul (2026-10-21T22:24:00 UTC), as relayed by the course coordinator; the time at which the owner wrote it is not known to the builder session"
QUOTE = ('"Sections are linked with each other at least by menu, possibly by semantic, syntactic, temporal, concepts, content or other relationships. You need to discover it by using the OEE relationship taxonomy '
         'and if necessary class categorization in a similar manner."')
OWNER_ACT = ("Owner's answer of %s to the question of ex:CR3_PageErd, relayed by the course coordinator and recorded by the builder session, quoted: %s This is option (b) of the question, widened: the relationships between sections are discovered and stated in the chapter research "
             "as links (object properties), not text. Under the standing rule that work following the owner's direction is recorded as owner-directed, it is not listed as an open owner confirmation." % (WHEN, QUOTE))
ACTIVE = ["ex:Out3_ScopeR3", "ex:Out3_GoalR3", "ex:Out3_ObjectiveR3", "ex:Out3_BacklogR4"]
NEWB = "ex:Out3_BacklogR5"
CH = [("Ch10", "chapter 10", "10", 17, "Bitcoin network"), ("Ch11", "chapter 11", "11", 16, "")]

FACTS = ("Measured 2026-10-22 by the builder session from the newest page of each chapter (the relations the page test sees: page data relations between two different sections, counted by the same section map the page test 9.35.0 uses): "
         "chapter 10 has 17 sections and 0 relations between two sections; chapter 11 has 16 sections and 0; chapter 13 has 16 and 0; chapter 8 has 23 sections and 4 (16 sections with none); chapter 9 has 20 and 3 (14 with none); chapter 12 has 15 and 2 (12 with none); "
         "chapter 14 has 13 and 2 (10 with none); chapters 1 to 7 have every section linked (93, 50, 59, 39, 83, 110 and 52 section pairs). In chapters 1 to 7 the section relationship is NOT authored as a link between sections: it is the page-data builder's text co-mention "
         "('mentions', evidence: the document's section on X names Y; 1,644 of the 1,683 cross-section relations of those chapters) plus a few 'operates on' relations that come from the domain link chx:hasOwner (a subproperty of RDODI's hasOwningConcept) between concept individuals of different sections (11, 4, 2, 3, 11, 4 and 4). "
         "The research of chapters 10 and 11 states no relationship between two sections: their domain T-Box holds subclass links inside sections and disjointness, their domain A-Box holds only the I/O examples (type, label, definition, source, input, output, hasIOExample); the OEE link discovery (oe_link_discovery) found only the syntactic pair input/output. "
         "The text co-mention does not arise in chapters 10 and 11 because their document text names no concept of another section.")
OEE = ("The OEE relationship taxonomy is oe-method/04-documentation/RELATIONSHIP_TAXONOMY_RESEARCH_v1_11_0.md (categories as kb:RelationshipCategory_* in oe-method/09-governance/oegov_abox_v1_36_0.ttl, properties kb:hasRelationshipCategory and kb:hasClassKind in oegov_tbox_v1_15_0.ttl); "
       "construction method BP-D58 (choose the relation: which category, is there a standard relation that says it, which pattern, what to declare), class kinds BP-D59, missing-link discovery BP-D57 (tool repo-tooling/oe_link_discovery_v1_1_0.py: syntactic, semantic, temporal families; file set = a T-Box and A-Box pair), kind rule check repo-tooling/oe_kind_rule_check_v1_1_0.py. "
       "OE v2.31.0 and v2.32.0 (ceremony of 2026-10-22: PROCEED, repo-tooling v1.77.0) add kind rules and two class kinds: they bind the ontology files and any research that declares a category or a kind; they do not bind the A-Box versions of this register.")
DIRECTION_NOTE = "Direction: Shrink in the question (option (a)), Grow in the decision (option (b) widened, a deliverable is added)."

TOOLS = [("TS_Stage4Gates", "sen0401_stage4_gates_v1_1_0.py", "Stage 4 gate runner v1_1_0, reading the CURRENT RDODI pipeline validator v1.13.0"),
         ("TS_ChapterCheck", "sen0401_lineage_chapter_check_v1_3_0.py", "chapter check v1_3_0, reading the PINNED RDODI pipeline validator v1.6.0 (/home/claude/eco_pin/rdodi-ecosystem)"),
         ("TS_PageTest35", "sen0401_page_test_v9_35_0.py", "page test 9.35.0"),
         ("TS_PageTest34", "sen0401_page_test_v9_34_0.py", "page test 9.34.0"),
         ("TS_DeckMatch", "pages_deck_match_verify_v1_0_0.py", "deck match check v1_0_0"),
         ("TS_PageCheck", "sen0401_lineage_page_check_v1_0_0.py", "page check wrapper v1_0_0 (template markers and page test run for the bridge)")]
MEASURED_VERSION = ("page test 9.35.0 and 9.34.0 (unchanged); Stage 4 gate runner v1_1_0 reading the CURRENT RDODI validator v1.13.0; chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; deck match check v1_0_0; page check wrapper v1_0_0; "
                    "relationship discovery: oe_link_discovery v1_1_0 (repo-tooling v1.77.0, OE v2.32.0)")


def out_new(t, stage, name, consumes):
    return ('\nex:%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the third lineage, rebuilt by the stage revision for the relationships between sections"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;\n    backlog:consumesOutput ex:%s ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (name, stage, stage, consumes, X.digest(t, stage))


INTENT = ('ex:%s rdfs:comment "Drafted by the builder session on 2026-10-22 from the owner\'s answer of ' + WHEN + ' (quoted in the change request ex:CR3_PageErd); the intent origin is therefore Derived. '
          'The owner gave the direction; he did not review the wording of this element."@en .\n')


def ev_change(t):
    # the owner's answer on the existing change request and impact assessment (one request, one assessment)
    i, j = T.blk(t, "CR3_PageErd")
    b = t[i:j]
    assert "backlog:Direction_Shrink" in b
    b = b.replace("backlog:Direction_Shrink", "backlog:Direction_Grow", 1)
    b = b.rstrip().rstrip(".") + (' ;\n    rdfs:comment %s@en .\n' % lit(
        "Owner's answer recorded 2026-10-22: " + OWNER_ACT + " The question assumed option (a), a Shrink of the written standard; the decision is option (b) widened, which adds a deliverable to the scope, so the direction is Grow (" + DIRECTION_NOTE + ") "
        "No criterion is changed or waived: AC3T_Ch10 and AC3T_Ch11 stay as written and are met when the new page passes element 3. Disposition stays Pending until the ScopeChange that admits the story is recorded in the Backlog version (G127 route)."))
    t = t[:i] + b + t[j:]
    i, j = T.blk(t, "IA3_PageErd")
    b = t[i:j]
    b = b.rstrip().rstrip(".") + (' ;\n    rdfs:comment %s@en .\n' % lit(
        "Impact assessment after the owner's answer (2026-10-22). " + FACTS + " Route: the scope of the third lineage excludes a change of the research other than chapter 8 (ex:Excl3_NoConceptGates), so a new deliverable is added: a StageRevision from the Scope stage (G127), 7 versions "
        "(this one, retraction, four stages, and the iteration with the backlog in one) against the 'closed lineage and successor' alternative of about ten plus the owner's closure act. "
        "Work (planned, not begun): one story, one criterion per chapter (G133), seven tasks - for each of chapters 10 and 11 a research task (new research version whose section relationships are links, discovered with the OEE relationship taxonomy), a page task (the page-data builder reads the links as relations, the page is rebuilt as a new page version, the Stage 4 page ABox is rebuilt), a verify task - "
        "and one builder task that is shared (a new page-data builder version). Each page rebuild runs the page tests, about nine minutes per run. "
        "Iteration: ex:Iter_14, new, because the goal of ex:Iter_13 is frozen at its start and may not be extended; ex:Iter_13 stays open with ST_Page_Template only, its members unchanged, and closes when AC3T_Ch10 and AC3T_Ch11 are met by the verify tasks of the new iteration, or the owner rebaselines or recommits; closing it earlier would need a Rebaseline decided by the owner, which is not asked. "
        "Affected: AC3T_Ch10 and AC3T_Ch11 (met by the new pages), ST_Page_Template (closes after them), the Mission outcome, closureCommittedAt and the Achieved status of the third lineage are not touched. "
        "Risks: a section for which no relationship can be stated with a standard or declared relation is reported by name and not forced; the template draws every relation type that is not 'mentions' as 'operates on' and it is not changed; chapters 8, 9, 12, 13 and 14 have sections with no relationship and are not in this deliverable (an owner question). "
        "Not changed: any gate, test, threshold, criterion or template."))
    t = t[:i] + b + t[j:]
    return t, "The owner's answer of 2026-10-22 recorded on the change request ex:CR3_PageErd (direction now Grow, still Pending) and its impact assessment ex:IA3_PageErd; no stage changed in this version."


def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = (OWNER_ACT + " The work adds a deliverable to the scope of the third lineage (relationships between sections stated in the research of chapters 10 and 11, and the pages rebuilt from them); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). "
              "The change request ex:CR3_PageErd and its impact assessment ex:IA3_PageErd were completed first, in the previous version. This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; they are rebuilt one stage and one commit at a time; "
              "the goals, objectives, stories and tasks already in the register, Done ones included, re-enter by admission and are not re-dated. The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). "
              "The revision is recorded as decided by the builder role: the route is what the owner's direction needs; the stage revision itself he did not decide.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the relationships between the sections of chapters 10 and 11 are stated in the research as links"@en ;\n'
         '    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n    rdfs:seeAlso ex:CR3_PageErd, ex:IA3_PageErd ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the relationships between sections: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Scoped")
    L = ['''
ex:Area3_SectionLinks a backlog:ScopeArea ;
    rdfs:label "The relationships between the sections of the chapters whose research states none"@en ;
    backlog:belongsToLineage ex:Lineage3 ;
    backlog:areaLocation "03-materials: the research folders (rdodi) and page folders of chapters 10 and 11; the page-data builder, the page builder and the Stage 4 builder in 08-tooling" ;
    backlog:areaMeasure "sections of chapters 10 and 11 with no relationship to another section: 33 of 33 today; after the work 0" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del3_SectionLinks a backlog:ScopeDeliverable ;
    rdfs:label "The research of chapters 10 and 11 states how their sections relate, as links, and their pages show the relationships"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area3_SectionLinks ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Scope3 backlog:requiresDeliverable ex:Del3_SectionLinks ;
    backlog:coversArea ex:Area3_SectionLinks ;
    rdfs:seeAlso ex:CR3_PageErd, ex:IA3_PageErd .
ex:Scope3 rdfs:comment %s@en .
ex:Excl3_NoConceptGates rdfs:comment %s@en .
''' % (T.CLAUSE,
       lit("A new version of the research of chapters 10 and 11 (the domain T-Box, A-Box and SHACL as the chapter's package requires, the document and the research file) in which the relationships between the sections are STATED AS LINKS (object properties between the sections' individuals or classes; ruling G134: links, not text), "
           "discovered with the OEE relationship taxonomy (categories such as semantic, syntactic, temporal, containment, ordering and succession; class kinds where the kind rule needs them), each property declared in the domain T-Box with domain, range, label and kb:hasRelationshipCategory, a standard relation reused where one says it; "
           "every section of the chapter related to at least one other section; the page-data builder reads the links as page relations, the page is rebuilt as a new page version and its Stage 4 page ABox as a new file; the page test 9.35.0 runs its ERD labels feature and passes it with no skip. "
           + OEE + " " + FACTS),
       lit("Revised 2026-10-22 by the stage revision %s on the owner's answer of %s (quoted in the change request ex:CR3_PageErd). The statement above is unchanged (L-112). It now also requires ex:Del3_SectionLinks and covers the area ex:Area3_SectionLinks. The exclusion ex:Excl3_NoConceptGates (owner-decided) stands for every gate, test and threshold. Not in the deliverable and not changed: the page template, a page test, a criterion, a relation type the template cannot draw (it draws every type other than 'mentions' as 'operates on'), forcing a relationship that no taxonomy relation states, and the section relationships of chapters 8, 9, 12, 13 and 14 (reported as facts; extending to them is the owner's to decide)." % (REV.replace("ex:", ""), WHEN)),
       lit("Note 2026-10-22: the concern 'a change of content, decks or research other than the chapter 8 examples' is lifted for the research of chapters 10 and 11 by the owner's answer of %s, as ex:Del3_SectionLinks; the exclusion stands for every other change of content, decks or research and for every gate, test and threshold." % WHEN))]
    t += "".join(L)
    return t + out_new(t, "Scope", "Out3_ScopeR4", "Out3_Mission"), \
        "third lineage, Scope stage rebuilt by the stage revision for the relationships between sections: a deliverable (the research of chapters 10 and 11 states section relationships as links; the pages show them), its area, and its area; the exclusion ex:Excl3_NoConceptGates stands for every gate, test and threshold."


def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR4", prev); t = X.set_status(t, "LS_Goaled")
    L = ['\nex:G3_SectionsRelated a backlog:Goal ;\n    rdfs:label "The sections of a chapter are related to each other as the research states, so the ERD of its page shows how they connect"@en ;\n'
         '    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_SectionLinks ;\n'
         '    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalOrigin backlog:GoalOrigin_New ;\n'
         '    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;\n'
         '    backlog:hasGoalRationale %s ;\n    backlog:producedByStage ex:Out3_GoalR4 .\n' % lit(
             "Derived from the revised scope of the third lineage (ex:Del3_SectionLinks) and from the owner's answer of %s, quoted: %s" % (WHEN, QUOTE))]
    L.append(INTENT % "G3_SectionsRelated")
    L.append('''
ex:Spec3L_L a backlog:Specification ;
    rdfs:label "What it is for the research to state how the sections of a chapter relate"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_SectionsRelated ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR4 .
ex:Scen3L_L_Passes a backlog:TestScenario ; rdfs:label "A chapter whose research links its sections shows labelled relationships on its ERD"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3L_L ;
    backlog:hasScenarioText "Given the new research version of a chapter, when the section relationships it states as links are read by the page-data builder and the page is rebuilt, then the page test 9.35.0 runs the two ERD label features without a skip and passes them, and every section has a relationship to at least one other section." .
ex:Scen3L_L_NotClaimed a backlog:TestScenario ; rdfs:label "A chapter whose ERD feature is skipped is not claimed as measured"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3L_L ;
    backlog:hasScenarioText "Given a page for which the test 9.35.0 skips the ERD label features because the research states no relationship between two sections, when the story is to be recorded Done, then the criterion of that chapter has no passing result and the chapter is named." .
''' % lit("The research of a chapter states, as links between the sections' individuals or classes, how the sections relate: every section is related to at least one other section by a relation of the OEE taxonomy (semantic, syntactic, temporal, containment, ordering or another), "
       "declared in the domain T-Box with a relationship category, and the page of the chapter draws them so that the existing ERD features of the page test 9.35.0 can run. " + OEE))
    t += "".join(L)
    return t + out_new(t, "Goal", "Out3_GoalR4", "Out3_ScopeR4"), "third lineage, Goal stage rebuilt for the relationships between sections: one goal (the sections of a chapter are related as the research states) with a specification and a nominal and a rejection scenario."


OBJS = [("Obj3_SectionsLinked", "Met3_SectionsLinked", "sections of chapters 10 and 11 with no relationship to another section", 33, 0, "Dir_Decrease",
         "Baseline measured 2026-10-22 from the newest page of each chapter (page data relations between two different sections, the section map of the page test 9.35.0): chapter 10 has 17 sections and 0 such relations, chapter 11 has 16 and 0: 33 of 33 sections without a relationship to another section."),
        ("Obj3_ErdLabelsRun", "Met3_ErdLabelsRun", "pages among chapters 10 and 11 whose ERD label features of the page test 9.35.0 run and pass without a skip", 0, 2, "Dir_Increase",
         "Baseline measured by the control run of 2026-10-21 (v0.154): the page test 9.35.0 skips the two ERD label features on both pages (the skip lines are quoted in ex:CR3_PageErd): 0 of 2.")]


def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR4", prev); t = X.set_status(t, "LS_Objectived")
    now = M.now(); L = []
    for i, m, what, b, tg, d, basis in OBJS:
        L.append('''
ex:%(i)s a backlog:Objective ; rdfs:label "%(Wh)s: from %(b)d to %(tg)d"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_SectionsRelated ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:%(m)s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %(what)s, read from the newest pages and the research of the chapters after the evidence bridge has run the checks." ;
    backlog:hasBaselineValue "%(b)d"^^xsd:decimal ; backlog:hasTargetValue "%(tg)d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%(d)s ;
    backlog:hasCheckpoint ex:CP3L_%(i)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR4 .
ex:%(m)s a backlog:Metric ; rdfs:label "%(what)s"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3L_%(i)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the section-links story is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria of chapters 10 and 11, so the count is read from verified runs." ;
    backlog:expectedValue "%(tg)d"^^xsd:decimal .
ex:Obs40_%(i)s a backlog:MetricObservation ; rdfs:label "Baseline, before any work on the section links"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(i)s ; backlog:hasObservedValue "%(b)d"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ;
    backlog:hasObservationMethod "%(basis)s" .
''' % dict(i=i, m=m, what=esc(what), Wh=esc(what[0].upper() + what[1:]), b=b, tg=tg, d=d, now=now, basis=esc(basis)))
    L.append("".join(INTENT % i for i, *_ in OBJS))
    t += "".join(L)
    return t + out_new(t, "Objective", "Out3_ObjectiveR4", "Out3_GoalR4"), "third lineage, Objective stage rebuilt for the relationships between sections: objectives (sections with no relationship 33 to 0; pages whose ERD label features run 0 to 2) with metric, checkpoint and a baseline reading of 2026-10-22."


def gh(label, num, nsec, other):
    return ("Owner's answer of %s: \"Sections are linked with each other at least by menu, possibly by semantic, syntactic, temporal, concepts, content or other relationships. You need to discover it by using the OEE relationship taxonomy and if necessary class categorization in a similar manner.\" "
            "Given the research of %s (%d sections, none related to another section, ruling G134: links, not text) and its page (page 9.77.0), when a new version of the research states the relationships between sections as object-property links discovered with the OEE relationship taxonomy "
            "(each property declared in the domain T-Box with domain, range, label and a relationship category; a standard relation reused where one says it; class kinds where the kind rule needs them) and the page is rebuilt from it as a new page version, then ALL of: "
            "(1) links: every one of the %d sections is related to at least one other section by a stated link, and no relationship is stated as text only; "
            "(2) ERD: the page test 9.35.0 runs its ERD label features (the filled ERD overlap and labels-over-entity reading, and the on-choice labels mode) with no skip and passes them, labels shown after Untangle at least 95 percent of the grid's; "
            "(3) gates: the Stage 4 gate runner v1_1_0 for %s (reading the current validator v1.13.0) exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, and the Research, Deck and Page chapter checks v1_3_0 (reading the pinned validator v1.6.0) pass; "
            "(4) the five elements of the criterion AC3T_Ch%s are measured again on the new page and all pass: the template markers, pages_deck_match_verify with 0 not carried, the page tests 9.34.0 and 9.35.0 unchanged with counts equal to or better than the stored result, the Stage 4 page ABox rebuilt as a new file; "
            "(5) no gate, test, threshold, criterion or template is changed and no committed file is edited; results are reported as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN) and a skip is not a pass; "
            "if any element fails the chapter is named failing and this criterion has no passing result." % (WHEN, label, nsec, nsec, num, num))


def task_block(tid, title, ttype, note, deps=(), state="Proposed"):
    s = G.task_block(tid, title, ttype, note, deps).replace("ex:Out3_BacklogR2", NEWB).replace(G.ITER, ITER, 1)
    if state == "Proposed":
        s = s.replace("backlog:hasState backlog:Ready", "backlog:hasState backlog:Proposed", 1)
    return s


def story_block(*a):
    return G.story_block(*a).replace("ex:Out3_BacklogR2", NEWB).replace(G.ITER, ITER, 1).replace(
        "Not scored: the owner decided on 2026-10-20 10:42 Istanbul that the gaps are closed first, so there is no ranking left to compute.", "Not scored: the owner directed this work on 2026-10-22, so there is no ranking left to compute.")


def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR4", prev); t = X.set_status(t, "LS_Backlogged")
    now = M.now()
    n = t.count("backlog:admittedByOutput ex:Out3_BacklogR4 ;")
    assert n >= 40, n
    t = t.replace("backlog:admittedByOutput ex:Out3_BacklogR4 ;", "backlog:admittedByOutput %s ;" % NEWB)
    L = []
    # tools as data (G136) and the criteria measured with them
    for ts, fn, what in TOOLS:
        L.append('ex:%s a backlog:ToolScript ; rdfs:label %s@en ; backlog:scriptFileName "%s" ; backlog:acceptsGraphPath false .\n' % (ts, lit(what), fn))
    L.append('ex:TS_RdodiValidatorCurrent a backlog:ToolScript ; rdfs:label "RDODI pipeline validator v1.13.0 (the newest in the Ontologies checkout), read by the Stage 4 gate runner"@en ; backlog:scriptFileName "rdodi_pipeline_validator_v1_13_0.py" ; backlog:acceptsGraphPath false .\n')
    L.append('ex:TS_RdodiValidatorPinned a backlog:ToolScript ; rdfs:label "RDODI pipeline validator v1.6.0 (the pinned ecosystem checkout), read by the chapter check"@en ; backlog:scriptFileName "rdodi_pipeline_validator_v1_6_0.py" ; backlog:acceptsGraphPath false .\n')
    L.append('ex:TS_LinkDiscovery a backlog:ToolScript ; rdfs:label "OEE missing-link discovery v1_1_0 (repo-tooling v1.77.0)"@en ; backlog:scriptFileName "oe_link_discovery_v1_1_0.py" ; backlog:acceptsGraphPath false .\n')
    allts = [x[0] for x in TOOLS] + ["TS_RdodiValidatorCurrent", "TS_RdodiValidatorPinned", "TS_LinkDiscovery"]
    crit = []; tk = []
    for nm, label, num, nsec, _ in CH:
        c = "AC3L_" + nm; crit.append(c)
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
                 '    backlog:satisfiedByArtifact "the new research version, the page, its Stage 4 page ABox and the stored page-test results as new files cited by SHA-256, and the runs of the template markers, the deck match check, the page tests, the Stage 4 gate runner and the chapter checks, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3L_L_Passes, ex:TC3L_L_NotClaimed .\n'
                 % (c, lit("The research of %s states how its sections relate as links, and its page shows them with the ERD labels measured" % label), lit(gh(label, num, nsec, "")),
                    ", ".join("ex:" + x for x in allts), lit(MEASURED_VERSION)))
    R10, R11, BLD = "TK_SecLinks_Ch10_Research", "TK_SecLinks_Ch11_Research", "TK_SecLinks_PageData"
    spec = {"Ch10": (R10, "TK_SecLinks_Ch10_Page", "TK_SecLinks_Ch10_Verify"), "Ch11": (R11, "TK_SecLinks_Ch11_Page", "TK_SecLinks_Ch11_Verify")}
    COMMON = ("A committed file is never edited: every output is a new file with a new version number. No gate, test, threshold, criterion or page template is changed; STOP and report if any would be needed (including a relation type the template cannot draw). "
              + OEE)
    for nm, label, num, nsec, _ in CH:
        r, p, v = spec[nm]; c = "AC3L_" + nm
        L.append(task_block(r, "State the relationships between the sections of %s as links in a new research version" % label, "Build",
                            "Discover the relationships between the %d sections of %s with the OEE relationship taxonomy (read the research, the domain T-Box and A-Box, the document; run oe_link_discovery on the T-Box and A-Box pair; classify by category: semantic, syntactic, temporal, containment, ordering and succession, and by class kind where needed) "
                            "and state them in a NEW research version as object-property links between the sections' individuals (the X_ individuals the page-data builder maps to sections) or classes, in the domain A-Box, with every property declared in the domain T-Box with domain, range, label and kb:hasRelationshipCategory, reusing a standard relation where one says it (as chapters 1 to 7 reuse rd:hasOwningConcept through chx:hasOwner); "
                            "every section related to at least one other; no relationship stated only as text (ruling G134). Produce the new T-Box, A-Box, SHACL, document and research files as the chapter's package needs, run the Stage 3.F and Stage 4 gates and the Research chapter check on them. %s Satisfies the criterion ex:%s." % (nsec, label, COMMON, c), (), "Ready"))
    L.append(task_block(BLD, "Give the page-data builder a new version that reads the section links as page relations", "Build",
                        "Write a new version of the page-data builder (08-tooling/sen0401_page_data_v2_22_0.py reads chx:hasOwner only) that reads the section-relationship links of the new research versions as page relations of type 'operates on' (the template draws every type other than 'mentions' that way), "
                        "with the relation's evidence naming the property and its category, and that gives the same output as before for chapters whose research has no such links; check it on chapter 10 first and on chapters 1 to 7 to show no relation changes there. A new file; the builder v2_22_0 is not edited. %s Satisfies the criteria ex:AC3L_Ch10 and ex:AC3L_Ch11." % COMMON,
                        (R10,), "Proposed"))
    for nm, label, num, nsec, _ in CH:
        r, p, v = spec[nm]; c = "AC3L_" + nm
        L.append(task_block(p, "Rebuild the page of %s from the research with section links, and its Stage 4 page ABox" % label, "Build",
                            "From the new research version of %s and the new page-data builder, build the page as a new file with a new page version on the page template 9.51.0 with the page builder v4_14_0, run the page tests 9.34.0 and 9.35.0 unchanged (the ERD label features must run, not skip) and store the result; build the Stage 4 page ABox from the new page with the Stage 4 builder (a new file). %s Satisfies the criterion ex:%s."
                            % (label, COMMON, c), (r, BLD), "Proposed"))
        L.append(task_block(v, "Verify the section links and the page of %s" % label, "Verify",
                            "Run, one after the other and as printed: the Stage 4 gate runner v1_1_0 for %s (current validator v1.13.0); the Research, Deck and Page chapter checks v1_3_0 (pinned validator v1.6.0); the page tests 9.34.0 and 9.35.0 (the ERD label features run without a skip); the template markers; pages_deck_match_verify; the link count (every section related to another); "
                            "and the five elements of the criterion ex:AC3T_%s on the new page, so that ST_Page_Template can close. Record every result as reported (PASS, FAIL, NOT_MEASURED, CANNOT_RUN). Criteria ex:%s and ex:AC3T_%s." % (num, nm, c, nm), (p,)))
        tk += [r, p, v]
    tk.insert(2, BLD)
    sid = "ST_Section_Links"
    L.append(story_block(sid, "The research of chapters 10 and 11 states how their sections relate, as links, and their pages show the relationships",
                         "the relationships between the sections of chapters 10 and 11 stated in the research as links and shown on the ERD of their pages",
                         "a student sees how the sections of a chapter connect, the ERD labels can be measured, and the research, not the page builder, is where the relationships are stated",
                         "Del3_SectionLinks", "Obj3_SectionsLinked", "Cat_NewCapability", crit, tk,
                         OWNER_ACT + " One criterion per chapter (G133). " + FACTS))
    L.append("ex:%s backlog:standsAlone true .\nex:Obj3_ErdLabelsRun backlog:metricMovableBy ex:%s .\nex:Obj3_SectionsLinked backlog:metricMovableBy ex:%s .\n" % (sid, sid, sid))
    L.append('''
ex:TC3L_L_Passes a backlog:TestCase ; rdfs:label "Run the section-link checks on a chapter whose files pass and require no failure and no skip"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3L_L_Passes ; backlog:runsOnData ex:Data3L_L_Passing ;
    backlog:hasCaseText "Run the checks of the criterion over the newest files of a chapter; they report no failure, the ERD label features run and pass, and the run exits 0 (the bridge runs recorded in this register are these runs)." .
ex:TC3L_L_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on a chapter whose ERD feature is skipped and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3L_L_NotClaimed ; backlog:runsOnData ex:Data3L_L_Failing ;
    backlog:hasCaseText "Run the page test 9.35.0 over a page whose research states no relationship between two sections (the pages of chapters 10 and 11 as measured 2026-10-21); the ERD features are skipped, the chapter carries no verified test evidence for the criterion and the story names it failing." .
ex:Data3L_L_Passing a backlog:TestData ; rdfs:label "A chapter whose section links are stated and whose ERD features run when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest research and page files of a chapter for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3L_L_Failing a backlog:TestData ; rdfs:label "A chapter whose research states no relationship between two sections"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The research and page files of chapters 10 and 11 as they stood on 2026-10-21 (page 9.77.0): the page test 9.35.0 skips the ERD label features." .
''' % dict(cr=", ".join("ex:" + c for c in crit)))
    for x in [sid] + tk:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome "Refined by the builder session from the owner\'s answer of %s (quoted in ex:CR3_PageErd) and the facts in ex:IA3_PageErd; the criterion and the task text name the checks, the files and what a passing result is." .\n'
                 % (x, x, x, now, ITER, WHEN))
    L.append('ex:Plan3L_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 14"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3L_L, ex:Scen3L_L_Passes, ex:Scen3L_L_NotClaimed .\n'
             % (sid, sid, now, ITER, sid, ", ".join("ex:" + x for x in tk)))
    # the iteration: new, start = the planning ceremony; the end is proposed
    L.append('ex:Iter_14 a backlog:Iteration ; rdfs:label "Iteration 14: state the relationships between the sections of chapters 10 and 11 as links in the research and rebuild their pages"@en ; backlog:hasIdentifier "Iter_14" ; backlog:belongsToLineage ex:Lineage3 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-24T06:00:00"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n'
             % (now, lit("Proposed by the builder session on 2026-10-22: the start is the instant of the planning ceremony ex:PC3_Iter_14; the proposed end is Saturday 2026-10-24 06:00 UTC (09:00 Istanbul), a day after the end of ex:Iter_13, for two chapters of research, one builder version and two page rebuilds at about nine minutes per page test run. The end is the owner's to decide: the plan stands whatever end he gives, and a story still open at the end shows as spillover (L4) until he rebaselines or recommits. "
                                       "Why a new iteration: the goal of ex:Iter_13 is frozen at its start and adding work to it is the mid-sprint extension the owner ruled out on 2026-10-21 10:14 Istanbul; closing ex:Iter_13 early would need a Rebaseline decided by the owner. ex:Iter_13 stays open with ST_Page_Template only (members unchanged) until AC3T_Ch10 and AC3T_Ch11 are met by the verify tasks here."),
                lit("The research of chapters 10 and 11 states the relationships between their sections as links discovered with the OEE relationship taxonomy, the page-data builder reads them, and the two pages are rebuilt so that the ERD label features of the page test 9.35.0 run and pass with no skip, on the gates as they stand, each unit that fails named; then the owner records the Mission outcome. Frozen at the iteration's start: work added later goes to a new iteration or to the owner's rebaseline."),
                ", ".join("ex:" + x for x in [sid] + tk)))
    L.append('ex:PB3L_Iter_14 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 14 when it was planned"@en ; backlog:baselineFor ex:Iter_14 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "2026-10-24T06:00:00"^^xsd:dateTime .\n' % (now, now))
    L.append('ex:PC3_Iter_14 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 14: the section links of chapters 10 and 11"@en ; backlog:ceremonyFor ex:Iter_14 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent ex:Plan3L_%s ;\n    rdfs:comment %s@en .\n'
             % (now, sid, lit("Held %s by the builder session, after the owner's answer of %s (quoted in ex:CR3_PageErd): the story %s and its %d tasks are committed to this iteration, whose goal is frozen at its start. No executor has started; work begun is recorded at the real start of each executor session, with its brief." % (now, WHEN, sid, len(tk)))))
    L.append('ex:SC3_SectionLinks a backlog:ScopeChange ;\n    rdfs:label "Scope grown by the section relationships of chapters 10 and 11 stated in the research"@en ;\n    backlog:fulfillsRequest ex:CR3_PageErd ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n'
             % (sid, lit(OWNER_ACT + " The boundary moved outward by one story because the owner chose to have the relationships stated in the research. It is paid for by a new iteration, new files beside the old ones, and no change to any gate, test, threshold, criterion or the template.")))
    t, k = re.subn(r'(ex:CR3_PageErd a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR3_PageErd rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_SectionLinks and the story it admits; it was Pending before. Accepted in the sense of option (b), widened by the owner\'s answer of %s."@en .\n' % (now[:10], WHEN))
    t += "\n" + "".join(L)
    return t + out_new(t, "Backlog", "Out3_BacklogR5", "Out3_ObjectiveR4"), ("third lineage, Backlog stage rebuilt for the relationships between sections: one story with a criterion per chapter (10, 11) measured with named tools and versions, seven tasks, refinement and planning events, tools as data, "
                                                                           "the new iteration Iter_14 with its sprint goal, plan baseline and planning ceremony, test cases, the ScopeChange that admits the story; the change request CR3_PageErd is Accepted; the %d carried items are re-admitted by the rebuilt output, not re-dated." % n)


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]),
          "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2])}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
