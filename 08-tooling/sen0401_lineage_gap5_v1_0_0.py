#!/usr/bin/env python3
"""sen0401_lineage_gap5 v1_0_0 - change route (G125 route 2, G133) for a gap found by measurement after the owner's direction of 2026-10-20 10:42 Istanbul ("No, fill the gaps first."):
the Stage 3 document of chapter 5 fails Stage 3.F (15 dangling citations) under the current RDODI validator that the Stage 4 gate runner uses; the lineage chapter check passes it because it reads the
PINNED validator. The new criterion is a criterion of the open story ex:ST_Gap_Stage3F; an acceptance criterion is counted by the Backlog digest, so the route is a StageRevision from the Backlog stage.
Events (one new file each): change | retract | backlog PREV | begin PREV   (begin = fills the rebuilt output's commit and records work begun on the new Build task after the start gate says READY)"""
__version__ = "1.0.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G

lit, esc = G.lit, M.esc
REV = "ex:Revision_Lineage3_Backlog5"
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
FOUND = ("Found by measurement later, not hidden: on 2026-10-20 (after the work on the other units had begun) the coordinator ran the Stage 4 gate runner for chapter 5 and Stage3.F reported 15 dangling citations; the lineage chapter check "
         "(08-tooling/sen0401_lineage_chapter_check_v1_3_0.py) passes the same document because it reads the pinned validator of the ecosystem checkout (v1.6.0), while the Stage 4 runner reads the current validator (rdodi_pipeline_validator_v1_13_0). "
         "My earlier statement that Stage 3.F passes for chapters 2 to 14 was measured with the pinned validator. Re-measured with the current validator on 2026-10-20: chapters 1 to 4, 6 to 14 and Bitcoin in numbers pass (chapter 1 and Bitcoin in numbers after their repair); chapter 5 fails.")
OWNER = G.OWNER_ACT.split(" The question")[0] + " His direction, quoted: %s, covers every gap in the Stage 3.F and Stage 4 table; this gap was not in the table because it was found by measurement afterwards." % G.QUOTE
NOTE5 = "Chapter 5: the Stage 3 document of chapter 5 fails Stage 3.F with 15 dangling citations under the current validator."


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1
    j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


def ev_change(t):
    cr = ('\nex:CR3_Gaps5 a backlog:ChangeRequest ;\n    rdfs:label "Close the Stage 3.F gap of chapter 5, found by measurement after the gaps were planned"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_Gaps, ex:SC3_Gaps ;\n'
          '    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % lit(
        OWNER + " " + FOUND + " The deliverable ex:Del3_Stage3FRepair is the Stage 3 documents that fail Stage 3.F passing it; its text names the two units measured then, so chapter 5 widens it by one unit. A ScopeDeliverable's subject is the same, "
        "so the Scope digest does not move; the new acceptance criterion is counted by the Backlog digest, so the route is a revision from the Backlog stage (G125 route 2), not from the Scope stage. Pending until the ScopeChange that admits the story's new criterion and tasks is recorded.")
    ia = ('\nex:IA3_Gaps5 a backlog:ImpactAssessment ;\n    rdfs:label "What closing the Stage 3.F gap of chapter 5 costs, measured before it is started"@en ;\n'
          '    backlog:analyzesRequest ex:CR3_Gaps5 ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:CR3_Gaps ;\n    backlog:hasImpactStatement %s .\n') % lit(
        "Measured 2026-10-20: " + FOUND + " What moves: the Backlog digest of the third lineage, once, when the stage is closed again by a revision from the Backlog stage (one more criterion, AC3G_3F_Ch05); the Scope, Goal and Objective digests do not move. "
        "New items: one criterion on the open story ex:ST_Gap_Stage3F, a Build and a Verify task for chapter 5 (planned into the same iteration, ex:Iter_12, ending 2026-10-23T06:00 UTC, the owner's own confirmed end date). The target of the objective ex:Obj3_Stage3FPass moves from 2 to 3 documents "
        "(a state, not a stage element; disclosed on it). No Done story is re-dated; the 10 started Build tasks and their stories keep their states and start times; the carried items are re-admitted by admission. "
        "Interim: while the Backlog output is retracted the register shows the declared interim violations (G129). Nothing is waived, no gate, test or threshold is changed (the validator difference is disclosed, not repaired). "
        "Cost of waiting: the Mission outcome stays unrecorded and a document that fails the gate the runner uses stays unrepaired. Cost of acting: three commits and about half an hour; enforcement value forgone: none.")
    return t + cr + ia, "ChangeRequest ex:CR3_Gaps5 (Pending) and ImpactAssessment ex:IA3_Gaps5: chapter 5 fails Stage 3.F under the current validator (found by measurement); the owner's direction of 2026-10-20 10:42 Istanbul covers it; no stage changed."


def ev_retract(t):
    t = X.set_status(t, "LS_Objectived")
    reason = (OWNER + " " + FOUND + " The new acceptance criterion of the open story ex:ST_Gap_Stage3F is counted by the Backlog digest, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output ex:Out3_BacklogR2 and rebuilds nothing; "
              "the next version rebuilds it, re-admitting the same items by admission, not re-dated. The change request ex:CR3_Gaps5 and the impact assessment ex:IA3_Gaps5 are in the previous version. The interim version is the declared transition (G129). "
              "Recorded as decided by the builder role: the owner decided that every gap is filled first; the revision is the route that needs.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the Stage 3.F gap of chapter 5"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso ex:CR3_Gaps5, ex:IA3_Gaps5 ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput ex:Out3_BacklogR2 ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\nex:Out3_BacklogR2 backlog:outputRetracted true .\n') % (REV, lit(reason))
    return t + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output ex:Out3_BacklogR2 is retracted for the Stage 3.F gap of chapter 5; nothing is rebuilt here."


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged")
    n = t.count("backlog:admittedByOutput ex:Out3_BacklogR2 ;")
    assert n >= 22, n
    t = t.replace("backlog:admittedByOutput ex:Out3_BacklogR2 ;", "backlog:admittedByOutput ex:Out3_BacklogR3 ;")
    now = M.now()
    # objective target 2 -> 3 (a state, disclosed)
    i, j = blk(t, "Obj3_Stage3FPass"); b = t[i:j]
    b2 = b.replace('hasTargetValue "2"^^xsd:decimal', 'hasTargetValue "3"^^xsd:decimal').replace("from 0 to 2", "from 0 to 3"); assert b2 != b
    t = t[:i] + b2 + t[j:]
    i, j = blk(t, "CP3G_Obj3_Stage3FPass"); b = t[i:j]; b2 = b.replace('expectedValue "2"', 'expectedValue "3"'); assert b2 != b
    t = t[:i] + b2 + t[j:]
    c = "AC3G_3F_Ch05"; bt, vt = "TK_Gap3F_Ch05_Build", "TK_Gap3F_Ch05_Verify"
    L = ['\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:satisfiedByArtifact "the Stage3.F line of the Stage 4 gate runner (current validator) and of the chapter check, verified by the evidence bridge, and the new research and document data cited by SHA-256" ;\n    backlog:coveredByCase ex:TC3G_3F_Passes, ex:TC3G_3F_NotClaimed .\n'
         % (c, lit("Stage 3.F passes for the Stage 3 document of chapter 5"), lit(G.gherkin_3f("chapter 5", "Ch05", "FAIL, 15 dangling citations under the current validator that the Stage 4 gate runner uses; the chapter check, which reads the pinned validator, passes")))]
    L.append("ex:TC3G_3F_Passes backlog:exercisesCriterion ex:%s .\nex:TC3G_3F_NotClaimed backlog:exercisesCriterion ex:%s .\n" % (c, c))
    L.append(G.task_block(bt, "Repair Stage 3.F of the Stage 3 document of chapter 5", "Build",
                          "Resolve the 15 dangling citations that Stage 3.F reports for the Stage 3 document of chapter 5 under the current validator (the one the Stage 4 gate runner uses): each citation must point to a source of the research data, missing sources being added with their record, in new versions of the research and document data; a citation or a claim is not removed only to pass. A committed file is not edited. No gate, test or threshold is changed. Satisfies the criterion ex:%s." % c))
    L.append(G.task_block(vt, "Verify Stage 3.F for the Stage 3 document of chapter 5", "Verify",
                          "Run the Stage 4 gate runner v1_1_0 for 05 and Research/Ch05 with the chapter check v1_3_0, record what they report (Stage3.F and the rest, as measured; the two validators differ and both are reported), and confirm the Research, Deck and Page chapter checks of the unit still pass. Criterion ex:%s." % c, (bt,)))
    for x in (c, bt, vt):
        pass
    for x in (bt, vt):
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_12 ;\n    backlog:hasRefinementOutcome "Refined by the builder session from the owner\'s direction of %s and the measurement in ex:IA3_Gaps5." .\n' % (x, x, x, now, G.OWNER_WHEN))
    L.append('ex:Plan3G_ST_Gap_Stage3F_Ch05 a backlog:PlanningEvent ; rdfs:label "Planning of the chapter 5 tasks of ST_Gap_Stage3F into iteration 12"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_12 ;\n    backlog:plansItem ex:ST_Gap_Stage3F ; backlog:producesTask ex:%s, ex:%s ;\n    backlog:refinementProduces ex:Spec3G_3F, ex:Scen3G_3F_Passes, ex:Scen3G_3F_NotClaimed .\n' % (now, bt, vt))
    L.append("ex:ST_Gap_Stage3F backlog:hasAcceptanceCriterion ex:%s ; backlog:decomposesInto ex:%s, ex:%s .\nex:Iter_12 backlog:hasMember ex:%s, ex:%s .\n" % (c, bt, vt, bt, vt))
    L.append('ex:SC3_Gaps5 a backlog:ScopeChange ;\n    rdfs:label "Scope widened by the Stage 3.F repair of chapter 5"@en ;\n    backlog:fulfillsRequest ex:CR3_Gaps5 ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:ST_Gap_Stage3F ;\n    backlog:hasScopeChangeRationale %s .\n' % lit(OWNER + " The criterion %s and the tasks %s and %s are admitted on the open story ex:ST_Gap_Stage3F." % (c, bt, vt)))
    t, k = re.subn(r'(ex:CR3_Gaps5 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR3_Gaps5 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Gaps5 and the items it admits; it was Pending before. The owner\'s direction of %s is the decision."@en .\n' % (now[:10], G.OWNER_WHEN))
    L.append('ex:Obj3_Stage3FPass rdfs:comment %s@en .\nex:Del3_Stage3FRepair rdfs:comment %s@en .\nex:Obs35_Obj3_Stage3FPass rdfs:comment %s@en .\n' % (
        lit("Target changed from 2 to 3 documents on %s by the stage revision ex:Revision_Lineage3_Backlog5: chapter 5 fails Stage 3.F under the current validator. The label, the checkpoint and the target carry the new value; the baseline reading of 0 stands (chapter 5 failed, so 0 of 3 passed)." % now[:10]),
        lit("Widened on %s by one unit, chapter 5 (change request ex:CR3_Gaps5, scope change ex:SC3_Gaps5): the Stage 3 document of chapter 5 passes Stage 3.F under the current validator. The text above names the two units measured at the time (L-112)." % now[:10]),
        lit("Read at the Objective stage with a gate run that missed chapter 5: under the current validator the units failing were chapter 1 (1 uncited), Bitcoin in numbers (19 dangling) and chapter 5 (15 dangling); the count of passing among the three was 0.")))
    t += "\n" + "".join(L).replace("backlog:admittedByOutput ex:Out3_BacklogR2 ;", "backlog:admittedByOutput ex:Out3_BacklogR3 ;")
    return t + ('\nex:Out3_BacklogR3 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt by the stage revision from the Backlog stage"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR2 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt for chapter 5: criterion AC3G_3F_Ch05, tasks %s and %s, scope change SC3_Gaps5, change request Accepted; objective target 2 -> 3; %d items re-admitted, not re-dated." % (bt, vt, n)


def ev_begin(t, prev):
    t = G.fill_re(t, "ex:Out3_BacklogR3", prev)
    src = M.newest()
    k = "TK_Gap3F_Ch05_Build"
    # start gate on the register as it will stand
    tmp = src + ".gate.tmp"; open(tmp, "w").write(t)
    try:
        r = subprocess.run([sys.executable, GATE, tmp, "--lineage", "Lineage3", "--item", k], capture_output=True, text=True)
    finally:
        os.remove(tmp)
    assert "VERDICT     : READY" in r.stdout, r.stdout[-400:]
    now = M.now()
    i, j = blk(t, k); b = t[i:j]; assert "hasState backlog:Ready" in b
    t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
    t = X.set_status(t, "LS_InProgress")
    print("STARTED", now)
    return t, "closedAtCommit of the rebuilt Backlog output ex:Out3_BacklogR3 filled; work begun on TK_Gap3F_Ch05_Build at %s UTC (start gate READY); the lineage is InProgress." % now


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "begin": lambda: ev_begin(t, sys.argv[2])}
    nt, comment = fn[ev]()
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
