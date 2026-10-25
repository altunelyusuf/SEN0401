#!/usr/bin/env python3
"""sen0401_lineage_open_iter25 v1_0_0 - opens Iteration 25 at its REAL start by a planning ceremony (the coordinator's order of 2026-10-25: the owner has said not to wait). THE RULE (read in the lineage discipline v119, G70 and G136 Q2(b)): the date of an iteration that has a PlanBaseline may be moved only by a Rebaseline;
Iter_25 was planned without a ceremony and has NO PlanBaseline, so its proposed start is not a baselined date: the planning ceremony sets the start to the instant it is held and records the baseline (PB3S_Iter_25); no Rebaseline is needed and none is recorded; no owner decision is involved (the order of the iteration is the lineage's, by the owner's standing orders).
A task that records a start must be a member of an iteration whose iterationStart is at or before it (G136 Q2(b)): this version comes before any start in Iteration 25. It also readies the items of Iteration 25 whose dependencies are Done (stories and tasks with refinement events) and records the Pending ChangeRequest of the arc-check repair (an out-of-criterion tool defect, planned for Iteration 27, not now).
Usage: no arguments; writes one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
READY_S = ["ST_Ch04_Deck_R24", "ST_Ch01_VerifyScript"]; READY_T = ["TK_Ch04_Deck_Build_R24", "TK_Ch01_VerifyScript_Build"]
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
i, j = T.blk(t, "Iter_25"); b = t[i:j]; mem = re.findall(r"ex:((?:ST|TK)_\w+)", re.search(r"backlog:hasMember ([^.]*)\.", b, re.S).group(1))
old = re.search(r'iterationStart "([^"]*)"', b).group(1); assert "Iter_25" in b and old > now, (old, now)
nb = b.replace('iterationStart "%s"' % old, 'iterationStart "%s"' % now, 1)
nb = re.sub(r'rdfs:label "([^"]*) \(planned, not started\)"@en', r'rdfs:label "\1"@en', nb, count=1)
nb = re.sub(r'backlog:hasDurationSource "(?:[^"\\]|\\.)*"', "backlog:hasDurationSource " + lit("Opened by the lineage agent on %s UTC by the planning ceremony ex:PC3_Iter_25: the start is the instant of the ceremony (it was planned for %s UTC without a ceremony and without a PlanBaseline, so no Rebaseline applies); the end stays 2026-10-27T12:00 UTC. Estimates, not measurements: deck 1.5 h build plus 0.5 h verification, verify script 1.0 h plus 0.5 h, page repair 1.5 h plus 1.0 h; the page repairs wait for the verified template 9.52.3; browser runs serial under the lock." % (now, old)), nb, count=1)
nb = nb.replace("PLANNED, not started: no ceremony is held, no executor is briefed.", "Frozen at the planning ceremony ex:PC3_Iter_25.")
t = t[:i] + nb + t[j:]
for x in READY_S + READY_T:
    i, j = T.blk(t, x); bb = t[i:j]; assert "backlog:hasState backlog:Proposed" in bb, x
    t = t[:i] + bb.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    L.append('ex:Refine25_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_25 ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, lit("Refined by the lineage agent when Iteration 25 was opened: no dependency is open, the brief is generated from the register; startable.")))
evs = ["Plan3L_" + s for s in mem if s.startswith("ST_")]
for e in evs: assert ("ex:%s a backlog:PlanningEvent" % e) in t, e
L.append('ex:PB3S_Iter_25 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 25 when it was planned"@en ; backlog:baselineFor ex:Iter_25 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "2026-10-27T12:00:00"^^xsd:dateTime .\n' % (now, now))
L.append('ex:PC3_Iter_25 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 25: the story-layout repair of the pages of chapters 5 to 8, the deck of chapter 4, the chapter 1 verify script"@en ; backlog:ceremonyFor ex:Iter_25 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (now, ", ".join("ex:" + e for e in evs), lit("Held %s UTC by the lineage agent, ahead of the date planned (%s UTC), because the owner has said not to wait and a slot is free: the discipline moves a baselined iteration only by a Rebaseline; Iteration 25 had no baseline, so the ceremony sets its start (G70, G136 Q2(b)). No executor has started in it; work begun is recorded at the real start of each session." % (now, old))))
L.append('ex:CR3_ArcCheck a backlog:ChangeRequest ;\n    rdfs:label "Repair of the deck arc check as a new tool version: it demands a 26-slide standard and refuses the decks of chapters 1 and 8"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n' % lit("Found 2026-10-25 by the executor of the chapter 1 deck and confirmed on the deck of chapter 8: sen0401_deck_arc_check_v1_1_0.py refuses a deck of another length than 26 slides. It is not an element of any criterion of Iterations 24 to 28, so it blocks nothing; it is a tool defect to be repaired as a NEW file (a version above v1_1_0; the old file stays), planned for Iteration 27 and admitted by the ScopeChange of that iteration's planning. Pending: nothing is built now (the coordinator's order of 2026-10-25)."))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
print(os.path.basename(M.write_new(src, t2, nxt, cur, "Iteration 25 opened by its planning ceremony at the real start %s (no baseline existed, so no Rebaseline); the deck of chapter 4 and the chapter 1 verify script made Ready; ChangeRequest ex:CR3_ArcCheck (Pending) records the arc-check repair planned for Iteration 27." % now)))
