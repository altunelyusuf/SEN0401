#!/usr/bin/env python3
"""sen0401_lineage_singular v1_0_0 - change route (rulings G113, G125 route 2, G133, G134, G136) for the finding of the control of the two research tasks of Iter_14 (register v0.163):
the chapter 10 research states one property per class pair (26 properties for 28 links, the same meaning stated more than once) and its links carry no sentence; the owner's standing rule of 2026-10-21 (OE v2.27.0 BP-D61, v2.28.0 duplicate detector, rule S6) is that
real equals are ONE property with several labels. The delivered task TK_SecLinks_Ch10_Research stays Done (G125: a Done item stays Done); the repair is a NEW task and a NEW criterion on the open story ST_Section_Links.
An acceptance criterion is counted by the Backlog digest, so the route is a StageRevision from the Backlog stage (G125 route 2, as for chapter 5). The new task goes into a NEW iteration, ex:Iter_15: the goal of ex:Iter_14 is frozen at its start and
work added later goes to a new iteration or to the owner's rebaseline (the owner's rule of 2026-10-21).
Events, one new file each: change | retract | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL

lit, esc = G.lit, M.esc
REV = "ex:Revision_Lineage3_Backlog6"; OLD = "ex:Out3_BacklogR5"; NEW = "ex:Out3_BacklogR6"; ITER = "ex:Iter_15"
CR = "ex:CR3_Singular"; IA = "ex:IA3_Singular"
WHEN = "Thursday 2026-10-22 (after 03:04 Istanbul, the last commit of the chapter 11 research session), as relayed by the course coordinator"
RULE = ("the owner's standing rule of 2026-10-21, as relayed by the coordinator on 2026-10-22: real equals (terms with the same meaning) are ONE property with several labels, not parallel properties (consolidate; OE v2.27.0 BP-D61 'one meaning, one term', "
        "v2.28.0 duplicate detector, rule S6)")
FOUND = ("Found by the control run of 2026-10-22 (register v0.163; logs in 08-tooling/verify/iter14/ch10): the chapter 10 research v1.1.0 (commit d4dda4c) states its 28 links with 26 properties, one per class pair, and the same meaning is stated more than once: "
         "five 'precedes' variants (precedesCompactBlockMode, precedesFeefilter, precedesHeadersRequest, precedesWtxidAnnouncement, relayNetworkPrecedesCompactBlocks), six requirement variants (buildsOn x3, requiresAddressExchange, requiresProtocolVersion, plaintextFramedBy), "
         "five comparison variants ('in the way of', 'differs in privacy from', 'shares its hash function with') and two 'defend against an attack' variants among four causal ones. The check 'singular' of sen0401_lineage_research_check v1_0_0 (a floor: no two properties share a category and a super-property, no two share a label) fails with groups of 4, 2, 5, 6 and 5; chapter 11 passes it with 6 general properties for 32 links. "
         "The OE link discovery passes chapter 10 because its duplicate family compares definitions word for word and finds no identical one. Second finding: the chapter 10 links carry no sentence that states them (0 of 28; chapter 11: 32 of 32, check 'annotated'). "
         "Cause on the builder side: the brief generated for the research task (sen0401_lineage_brief v1_1_0) did not carry BP-D61 or the singularity rule, and the criterion AC3L_Ch10 did not ask for the sentence.")


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Chapter 10 research: one property per meaning and a sentence on every link, found by the control of the research task"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_PageErd, ex:IA3_PageErd ;\n'
          '    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(
        "Raised " + WHEN + ". " + FOUND + " The rule applied is " + RULE + ". The delivered task stays Done (G125); the repair is a new Build task, ex:TK_SecLinks_Ch10_Consolidate, with its own criterion (G133: one criterion per unit; the criterion AC3L_Ch10 is not rewritten while the work under it runs), "
        "in a new story of its own, ex:ST_Ch10_Consolidate (a story is planned into one iteration only). The deliverable ex:Del3_SectionLinks is unchanged: its text asks that the relationships be stated as links discovered with the taxonomy; one meaning one property is how the taxonomy and BP-D61 ask them to be stated. "
        "A new criterion is counted by the Backlog digest, so the route is a revision from the Backlog stage (G125 route 2), not from the Scope stage. Pending until the ScopeChange that admits the new criterion and task is recorded."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the consolidation of the chapter 10 research costs, measured before it is started"@en ;\n'
          '    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_PageErd ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(
        FOUND + " What moves: the Backlog digest of the third lineage once, when the stage is closed again (one more criterion, one more task); Scope, Goal and Objective digests do not move. "
        "New items: the criterion AC3L_Ch10_Singular, the Build task TK_SecLinks_Ch10_Consolidate (a new research version v1.2.0 as new files: one property per meaning with several labels, the same 28 link meanings kept, 17 of 17 sections covered, every link annotated with its sentence, the T-Box notes on standard relations such as BFO precedes and dcterms corrected where they are still true, all gates unchanged) "
        "planned into a NEW iteration ex:Iter_15 (the goal of ex:Iter_14 is frozen at its start; work added later goes to a new iteration or to the owner's rebaseline, which is not asked). Dependencies corrected: TK_SecLinks_PageData waited only for the chapter 10 research; it now waits for the consolidation and the chapter 11 research, because it reads the links of both and is tested on the consolidated chapter 10; "
        "TK_SecLinks_Ch10_Page now also waits for the consolidation. No page work has begun, so nothing is wasted; the chapter 10 page would otherwise have been built on 26 properties and rebuilt. Chapter 11 passes the same floor check and the sentence check and is not touched; "
        "its 'is followed by' (direct succession) and 'is earlier than' (order) differ in category and are kept as two meanings. The start of the ST_Section_Links story and the lineage status stay InProgress; the Done research tasks are re-admitted by admission, not re-dated. "
        "Interim: while the Backlog output is retracted the register shows the declared interim violations (G129). Nothing is waived and no gate, test, threshold or criterion is changed. Cost of waiting: pages built on parallel properties, a rule of the owner broken in the delivery. Cost of acting: four versions and one executor session of about ten minutes (the first research session took nine)."))
    return t + cr + ia, "ChangeRequest ex:CR3_Singular (Pending) and ImpactAssessment ex:IA3_Singular: the chapter 10 research states one property per class pair and its links carry no sentence (found by the control); the owner's rule one meaning one property applies; no stage changed."


def ev_retract(t):
    t = X.set_status(t, "LS_Objectived")
    reason = (FOUND + " The new acceptance criterion of the open story ex:ST_Section_Links is counted by the Backlog digest, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output %s and rebuilds nothing; "
              "the next version rebuilds it, re-admitting the same items by admission, not re-dated. The change request %s and the impact assessment %s are in the previous version. The interim version is the declared transition (G129). "
              "Recorded as decided by the builder role: the owner's rule is the origin; the revision is the route that the rule needs." % (OLD.replace("ex:", ""), CR.replace("ex:", ""), IA.replace("ex:", "")))
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: one meaning one property in the chapter 10 research"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the consolidation of the chapter 10 research; nothing is rebuilt here." % OLD.replace("ex:", "")


NOTE_TASK = ("Write the chapter 10 research as a NEW version v1.2.0 (new files only; research v1.1.0, commit d4dda4c, and its generator are not edited) in which the same relationships are stated once per meaning: "
             "(1) ONE PROPERTY PER MEANING (%s): read the definitions of the 26 properties of v1.1.0 and the sentence that states each of the 28 links, group them by meaning (for example the five 'precedes' variants, the six requirement variants, the five comparison variants, the 'defend against an attack' variants), "
             "and state each meaning as one general object property with its relationship category, one label and, where an earlier wording adds information, a further label (skos:altLabel); the class pair belongs to the link and to the sentence that states it, not to a new property; chapter 11 is the model "
             "(hasComponent, refersTo, hasConsequence, isComparedWith, isFollowedBy, isEarlierThan: 6 properties for 32 links). A meaning that really differs (a different category or a different standard super-property) stays a separate property, with its definition saying how it differs; "
             "(2) THE SAME 28 LINK MEANINGS: every link of v1.1.0 is still stated between the same two individuals (check samepairs:10); a pair you cannot keep is reported by name, not dropped; "
             "(3) every one of the 17 sections is related to at least one other (check seclinks:10); "
             "(4) EVERY LINK CARRIES THE SENTENCE THAT STATES IT, as chapter 11 does (owl:Axiom with rdfs:comment; see the chapter 11 A-Box v1.1.0 and check annotated:10); "
             "(5) STANDARD RELATIONS: where a retained property reuses a standard relation (BFO precedes, dcterms or RDODI properties such as requires, replaces, isPartOf) the T-Box says which and why, and an evidence note that stops being true after merging is corrected or removed; the reuse stays only where it is true (a process 'precedes' a process); "
             "(6) CHECKS, all as printed: sen0401_lineage_research_check singular:10, samepairs:10, seclinks:10, annotated:10, linkdisc:10 (0 beyond the baseline), kindrule:10 (0 violations; declare class kinds where the kind rule needs them), the Stage 4 gate runner for 10 (current validator v1.13.0) and the Research chapter check (pinned v1.6.0). "
             "A committed file is never edited; no gate, test, threshold or criterion is changed. STOP and report if a merge would change what a link says, or a check would have to change. " % RULE)


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged")
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEW)
    now = M.now(); c = "AC3L_Ch10_Singular"; k = "TK_SecLinks_Ch10_Consolidate"; sess = "SEN0401-I15-consolidate-ch10"; L = []
    # tools as data
    for ts, fn, what in [("TS_ResearchCheck", "sen0401_lineage_research_check_v1_0_0.py", "research check v1_0_0 (singular, samepairs, annotated, seclinks, linkdisc, kindrule wrapper for the bridge)"),
                         ("TS_SeclinksCheck", "sen0401_ch_seclinks_check_v1_0_0.py", "section links check v1_0_0"), ("TS_KindRuleCheck", "oe_kind_rule_check_v1_1_0.py", "OE kind rule check v1_1_0 (repo-tooling v1.77.0)")]:
        L.append('ex:%s a backlog:ToolScript ; rdfs:label %s@en ; backlog:scriptFileName "%s" ; backlog:acceptsGraphPath false .\n' % (ts, lit(what), fn))
    tools = ["TS_Stage4Gates", "TS_ChapterCheck", "TS_LinkDiscovery", "TS_KindRuleCheck", "TS_SeclinksCheck", "TS_ResearchCheck", "TS_RdodiValidatorCurrent", "TS_RdodiValidatorPinned"]
    gh = ("Given the chapter 10 research v1.1.0 (commit d4dda4c: 26 properties for 28 links, the same meaning stated more than once; no link carries its sentence) and %s, when a new research version v1.2.0 states the relationships once per meaning, then ALL of: "
          "(1) singular: the check singular:10 reports PASS (no two properties share a label, none share both a relationship category and a super-property) and each retained property's definition says what it means that no other retained property means, chapter 11 being the model (6 properties for 32 links); "
          "(2) the same 28 link meanings: the check samepairs:10 reports PASS (every link of v1.1.0 is still stated between the same two individuals); "
          "(3) every one of the 17 sections is an end of at least one link (seclinks:10 PASS); (4) every link carries the sentence that states it (annotated:10 PASS); "
          "(5) gates: the Stage 4 gate runner v1_1_0 for chapter 10 (reading the current validator v1.13.0) exits 0, the Research chapter check v1_3_0 (reading the pinned validator v1.6.0) passes, the OE link discovery v1_1_0 reports 0 beyond the baseline and the OE kind rule check v1_1_0 reports 0 violations; "
          "(6) no committed file is edited, no gate, test, threshold or criterion is changed; results are reported as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); if any element fails the research is named failing and this criterion has no passing result." % RULE)
    L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
             '    backlog:satisfiedByArtifact "the new chapter 10 research files cited by SHA-256, and the runs of the research checks, the Stage 4 gate runner, the chapter check, the link discovery and the kind rule check, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3L_L_Passes, ex:TC3L_L_NotClaimed .\n' % (
        c, lit("The chapter 10 research states each relationship meaning once, keeps its 28 links and gives each link its sentence"), lit(gh), ", ".join("ex:" + x for x in tools),
        lit("research check v1_0_0 (singular, samepairs, annotated, seclinks); Stage 4 gate runner v1_1_0 reading the CURRENT RDODI validator v1.13.0; chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; OE link discovery v1_1_0 and OE kind rule check v1_1_0 (repo-tooling v1.77.0, OE v2.32.0); section links check v1_0_0")))
    L.append(G.task_block(k, "Consolidate the chapter 10 section links: one property per meaning, a sentence on every link, research v1.2.0", "Build", NOTE_TASK + "Satisfies the criterion ex:%s." % c, ("TK_SecLinks_Ch10_Research",)).replace("ex:Out3_BacklogR2", NEW).replace(G.ITER, ITER, 1))
    sid = "ST_Ch10_Consolidate"
    L.append(G.story_block(sid, "The chapter 10 section links are stated once per meaning, each with its sentence", "the chapter 10 research to state each relationship meaning once, keep its 28 links and give each link its sentence",
                            "the page of chapter 10 is built on a research that follows the owner's rule one meaning one term, and its ERD labels say what each link means", "Del3_SectionLinks", "Obj3_SectionsLinked", "Cat_NewCapability", [c], [k],
                            "Created by the change route %s after the control of the research task (v0.163): %s Planned into the new iteration ex:Iter_15 as a story of its own, because a story is planned into one iteration only (L4) and the goal of ex:Iter_14 is frozen. " % (CR.replace("ex:", ""), FOUND) + "The tasks of ex:ST_Section_Links for chapter 10 depend on its task.").replace(G.ITER, ITER, 1).replace("ex:Out3_BacklogR2", NEW).replace("Not scored: the owner decided on 2026-10-20 10:42 Istanbul that the gaps are closed first, so there is no ranking left to compute.", "Not scored: a repair raised by the control under the owner's rule, so there is no ranking left to compute."))
    L.append("ex:%s backlog:standsAlone true .\n" % sid)
    for x in (sid,):
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome "Refined by the builder session from the finding of the control (ex:IA3_Singular) and the rule of the owner." .\n' % (x, x, x, now, ITER))
    L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome "Refined by the builder session from the finding of the control (ex:IA3_Singular) and the rule of the owner; the criterion and the task text name the checks and what a passing result is." .\n' % (k, k, k, now, ITER))
    L.append('ex:Plan3L_ST_Ch10_Consolidate a backlog:PlanningEvent ; rdfs:label "Planning of ST_Ch10_Consolidate into iteration 15"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:%s ;\n    backlog:refinementProduces ex:Spec3L_L .\n' % (now, ITER, sid, k))
    # story, dependencies, verify
    for tk, old, new in (("TK_SecLinks_PageData", "backlog:dependsOn ex:TK_SecLinks_Ch10_Research ;", "backlog:dependsOn ex:TK_SecLinks_Ch10_Research, ex:%s, ex:TK_SecLinks_Ch11_Research ;" % k),
                         ("TK_SecLinks_Ch10_Page", "backlog:dependsOn ex:TK_SecLinks_Ch10_Research, ex:TK_SecLinks_PageData ;", "backlog:dependsOn ex:TK_SecLinks_Ch10_Research, ex:%s, ex:TK_SecLinks_PageData ;" % k)):
        i, j = T.blk(t, tk); b = t[i:j]; assert old in b, tk
        t = t[:i] + b.replace(old, new, 1) + t[j:]
    L.append('ex:TK_SecLinks_PageData backlog:hasAuditNote %s .\nex:TK_SecLinks_Ch10_Page backlog:hasAuditNote %s .\n' % (
        lit("Dependency corrected %s (ex:IA3_Singular): this task read the links of both chapters but waited only for the chapter 10 research; it now waits for the consolidated chapter 10 research (ex:%s) and the chapter 11 research. Where the links carry a sentence, the relation's evidence in the page data is that sentence." % (now[:10], k)),
        lit("Dependency corrected %s (ex:IA3_Singular): the page is built on the consolidated chapter 10 research v1.2.0 (task ex:%s), not on v1.1.0." % (now[:10], k))))
    L.append("ex:TK_SecLinks_Ch10_Verify backlog:hasAcceptanceCriterion ex:%s .\nex:%s backlog:standsAlone true .\n" % (c, k) if False else "ex:TK_SecLinks_Ch10_Verify backlog:hasAcceptanceCriterion ex:%s .\n" % c)
    L.append('ex:AC3L_Ch10 backlog:hasAuditNote %s .\nex:TK_SecLinks_Ch10_Research backlog:hasAuditNote %s .\n' % (
        lit("Note %s: the rule one meaning one property and the sentence on every link were not elements of this criterion; the criterion is not rewritten while the work under it runs (G133); they are the elements of its sibling ex:%s, measured by the same Verify task." % (now[:10], c)),
        lit("Note %s: Done on the elements of its text (links declared, between sections, every section covered, gates, discovery, kinds); the control found that the delivery states one property per class pair and no sentence per link (ex:IA3_Singular); the repair is the new task ex:%s, and this task is not re-opened (G125)." % (now[:10], k))))
    # iteration 15
    L.append('ex:Iter_15 a backlog:Iteration ; rdfs:label "Iteration 15: consolidate the chapter 10 section links, one property per meaning"@en ; backlog:hasIdentifier "Iter_15" ; backlog:belongsToLineage ex:Lineage3 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-23T06:00:00"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember ex:ST_Ch10_Consolidate, ex:%s .\n' % (
        now, lit("Proposed by the builder session on 2026-10-22: the start is the instant of the planning ceremony ex:PC3_Iter_15; the proposed end is Friday 2026-10-23 06:00 UTC (09:00 Istanbul), the end of ex:Iter_13; one research task of about ten minutes. The end is the owner's to decide. "
                    "Why a new iteration: the goal of ex:Iter_14 is frozen at its start and work added later goes to a new iteration or to the owner's rebaseline. The remaining tasks of ex:Iter_14 for chapter 10 wait for this one (dependsOn), so the two iterations run one after the other in effect."),
        lit("The chapter 10 research states each relationship meaning once (one property per meaning with several labels, the class pair and the sentence carried by the link), keeps its 28 links and covers all 17 sections, on the gates as they stand, so that the section links of ex:Iter_14 are built on it; each check that fails is named. Frozen at the iteration's start."), k))
    L.append('ex:PB3L_Iter_15 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 15 when it was planned"@en ; backlog:baselineFor ex:Iter_15 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "2026-10-23T06:00:00"^^xsd:dateTime .\n' % (now, now))
    L.append('ex:PC3_Iter_15 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 15: the chapter 10 consolidation"@en ; backlog:ceremonyFor ex:Iter_15 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent ex:Plan3L_ST_Ch10_Consolidate ;\n    rdfs:comment %s@en .\n' % (
        now, lit("Held %s by the builder session after the control of the research tasks (v0.163): the task %s is committed to this iteration, whose goal is frozen at its start. No executor has started; work begun is recorded at the real start of the session %s with its brief." % (now, k, sess))))
    L.append('ex:SC3_Singular a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the consolidation of the chapter 10 section links"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:ST_Ch10_Consolidate ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, lit("The rule applied is " + RULE + ". The criterion %s and the task %s are admitted with the new story ex:ST_Ch10_Consolidate. " % (c, k) + FOUND)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Singular and the items it admits; it was Pending before. The owner\'s rule of 2026-10-21 is the decision."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt by the stage revision from the Backlog stage for the consolidation of the chapter 10 section links"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR4 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEW, X.digest(t, "Backlog")), \
        "third lineage, Backlog stage rebuilt for the chapter 10 consolidation: criterion %s, task %s planned into the new iteration Iter_15, dependencies of the page-data builder and the chapter 10 page corrected, scope change SC3_Singular, change request Accepted; %d items re-admitted, not re-dated." % (c, k, n)


def ev_fill(t, prev):
    t = G.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the consolidation is planned, no work begun." % (NEW.replace("ex:", ""), prev)


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
