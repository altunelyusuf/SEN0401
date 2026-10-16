#!/usr/bin/env python3
"""sen0401_lineage_followup v1_0_0 - plans the follow-up of the open parts of the SEN0401 slide lineage as ExecutionTasks under existing admitted items (the open epics for follow-up of Done stories)
(ruling G117: planning an ExecutionTask under an admitted story needs no change request; no story is added, so the Lineage2 Backlog digest does not move),
in a NEW version of the register; each task has an Executor. Nothing is started or Done here.
Usage: sen0401_lineage_followup_v1_0_0.py plan "end of iteration UTC (Friday 06:00)"
"""
__version__ = "1.0.0"
import os, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

TASKS = []
for n, why in ((1, "deck_check_v1_0_0.py is missing in the deck folder, the examples re-run and the stale-fixture check fail, notes carry SAY/ASK/STORY labels"),
               (2, "deck_check_v1_0_0.py is missing in the deck folder, stale fixtures are not refused, notes carry SAY/ASK/STORY labels"),
               (3, "the old deck_check hits a NameError and merkle_root refusals (it also failed on the old deck), notes carry SAY/ASK/STORY labels"),
               (4, "the old deck_check hits NameError and merkle_root refusals (it also failed on the old deck), notes carry SAY/ASK/STORY labels")):
    TASKS.append(("TK_Deck_Ch%02d_CheckFix" % n, "ST_Deck_Ch%02d" % n, "Fix the deck-check failures of Deck Ch%02d" % n, "Deck/Ch%02d fails the lineage deck check: %s." % (n, why)))
TASKS.append(("TK_Deck_Ch14_StaleFixtures", "ST_Deck_Ch14", "Add the stale_credit and stale_date fixtures to Deck Ch14", "Deck Ch14 has no stale proof for the credit and date gates; the fixtures are missing."))
TASKS += [("TK_Licence_Mempool_Ch09", "ST_Page_Ch09", "Settle the mempool.space licence question of the chapter 9 wheel", "Open licence question: the mempool.space census shown in the chapter 9 wheel. Needs a licence decision."),
          ("TK_Licence_Texts_Ch09", "ST_Page_Ch09", "Settle the licence of the three third-party texts of page 9", "Open licence question: three third-party texts on page 9. Needs a licence decision."),
          ("TK_Licence_BOLT_Ch09", "ST_Page_Ch09", "Correct the BOLT provenance contradiction of page 9", "Open: the BOLT text is recorded both as CC0 and as CC BY 4.0; the provenance must be corrected from the source.")]
for n in range(8, 15):
    TASKS.append(("TK_Research_Ch%02d_Stage4" % n, "ST_Research_Ch%02d" % n, "Build the stage-4 courseware artefact of chapter %d" % n, "The stage-4 courseware artefact of chapter %d is not built." % n))
for n in (2, 3, 4):
    TASKS.append(("TK_Research_Ch%02d_Stage3F" % n, "ST_Research_Ch%02d" % n, "Clear the Stage3.F failures of the chapter %d research" % n, "The research of chapter %d fails Stage3.F." % n))


# A Done story cannot have an open task (shapes L1, L2) nor be planned into a second iteration (L4), so a follow-up of finished work hangs under the open epic of its kind.
EPIC = {"Deck": "EP_Deck", "Page": "EP_Page", "Research": "EP_Research"}
TASKS = [(a, EPIC[b.split("_")[1]], c, d + " (Follows the Done story %s; the open task hangs under the epic because a Done story may not carry an open task.)" % b) for a, b, c, d in TASKS]


def main():
    end = sys.argv[2]
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); now = M.now()
    g = rdflib.Graph(); g.parse(src)
    assert (M.EX.Iter_11, None, None) not in g
    L = []; by_story = {}
    for tid, st, title, note in TASKS:
        assert (M.EX[st], None, None) in g and (M.EX[tid], None, None) not in g, tid
        L.append('ex:%s a backlog:ExecutionTask ; rdfs:label "%s"@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle "%s" ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_11 ; backlog:admittedByOutput ex:Out2_Backlog ; backlog:hasState backlog:Ready ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
                 '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Build ; backlog:effectiveDefinitionOfDone ex:DoD ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s score; scoring both would double-count." ;\n    backlog:hasAuditNote "%s" .\n'
                 % (tid, M.esc(title), tid, M.esc(title), M.esc(note)))
        L.append("ex:%s backlog:decomposesInto ex:%s .\n" % (st, tid))
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n'
                 '    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_11 ; backlog:hasRefinementOutcome "%s" .\n' % (tid[3:], tid, tid, now, M.esc(note)))
        by_story.setdefault(st, []).append(tid)
    for st, tids in by_story.items():
        L.append('ex:Plan_%s_Followup a backlog:PlanningEvent ; rdfs:label "Planning of the follow-up of %s into iteration 11"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Owner ; backlog:plannedInto ex:Iter_11 ;\n'
                 '    backlog:plansItem ex:%s ; backlog:producesTask %s .\n' % (st[3:], st, now, st, ", ".join("ex:" + x for x in tids)))
    L.append('ex:Iter_11 a backlog:Iteration ; rdfs:label "Iteration 11: follow-up of the open parts of chapters 1 to 14"@en ; backlog:hasIdentifier "Iter_11" ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n'
             '    backlog:hasDurationSource "Proposed: one week from the planning, ending at a class (Friday 09:00 Istanbul); the owner may move it." ;\n    backlog:hasSprintGoal "The open parts after the link pass are tracked as tasks under existing admitted items (the open epics for follow-up of Done stories): deck-check failures of chapters 1 to 4, the page link pass, the licence questions, the stage-4 and Stage3.F gaps." ;\n    backlog:hasMember %s .\n' % (now, end, ", ".join("ex:" + x[0] for x in TASKS)))
    body = t + "\n" + "".join(L); rdflib.Graph().parse(data=body, format="turtle")
    out = M.write_new(src, body, nxt, cur, "The follow-up of the open parts planned as %d ExecutionTasks under existing admitted stories in Iter_11 (ruling G117: no story added); nothing started or Done." % len(TASKS))
    print(os.path.basename(out))


main()
