#!/usr/bin/env python3
"""sen0401_lineage_open_iter v1_1_0 - opens a planned iteration at its REAL start by a planning ceremony (the open_iter25 tool made general; the coordinator's order of 2026-10-25: the owner wants progress). THE RULE (lineage discipline v119, G70 and G136 Q2(b)): the dates of an iteration that has a PlanBaseline move only by a Rebaseline;
an iteration planned without a ceremony has NO PlanBaseline, so the ceremony sets its start to the instant it is held and records the baseline; no Rebaseline, no owner decision. Makes the named stories and tasks Ready (refinement events). The end stays as planned.
Usage: sen0401_lineage_open_iter_v1_0_0.py ITER STORY,STORY.. TASK,TASK..   (one new register version)"""
__version__ = "1.3.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; IT = sys.argv[1]; N = IT[5:]; RS = sys.argv[2].split(","); RT = sys.argv[3].split(",")
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
assert ("ex:PC3_%s a " % IT) not in t and ("ex:PB3S_%s a " % IT) not in t, "already opened"
i, j = T.blk(t, IT); b = t[i:j]; mem = re.findall(r"ex:((?:ST|TK)_\w+)", re.search(r"backlog:hasMember ([^.]*)\.", b, re.S).group(1))
old = re.search(r'iterationStart "([^"]*)"', b).group(1); end = re.search(r'iterationEnd "([^"]*)"', b).group(1); assert old > now, (old, now)
lab = re.search(r'rdfs:label "([^"]*)"@en', b).group(1).replace(" (planned, not started)", "")
nb = b.replace('iterationStart "%s"' % old, 'iterationStart "%s"' % now, 1)
nb = re.sub(r'rdfs:label "[^"]*"@en', 'rdfs:label %s@en' % lit(lab), nb, count=1)
nb = re.sub(r'backlog:hasDurationSource "(?:[^"\\]|\\.)*"', "backlog:hasDurationSource " + lit("Opened by the lineage agent on %s UTC by the planning ceremony ex:PC3_%s: the start is the instant of the ceremony (planned for %s UTC without a ceremony and without a PlanBaseline, so no Rebaseline applies); the end stays %s UTC. Estimates, not measurements: deck 1.5 h build plus 0.5 h verification, page 1.5 h plus 1.0 h; pages wait for the verified template 9.52.3; browser runs serial under the lock." % (now, IT, old, end)), nb, count=1)
nb = nb.replace("PLANNED, not started: no ceremony is held, no executor is briefed.", "Frozen at the planning ceremony ex:PC3_%s." % IT)
t = t[:i] + nb + t[j:]
for x in RS + RT:
    assert x in mem, x
    i, j = T.blk(t, x); bb = t[i:j]; assert "backlog:hasState backlog:Proposed" in bb, x
    t = t[:i] + bb.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    L.append('ex:Refine%s_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:%s ;\n    backlog:hasRefinementOutcome %s .\n' % (N, x, x, x, now, IT, lit("Refined by the lineage agent when %s was opened: no dependency is open, the brief is generated from the register; startable." % IT)))
evs = [re.search(r"^ex:(Plan3[A-Z]_%s) a backlog:PlanningEvent" % s, t, re.M).group(1) for s in mem if s.startswith("ST_")]
for e in evs: assert ("ex:%s a backlog:PlanningEvent" % e) in t, e
L.append('ex:PB3S_%s a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration %s when it was planned"@en ; backlog:baselineFor ex:%s ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (IT, N, IT, now, now, end))
L.append('ex:PC3_%s a backlog:SprintPlanningCeremony ; rdfs:label %s@en ; backlog:ceremonyFor ex:%s ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (IT, lit("Planning of " + lab.lower()), IT, now, ", ".join("ex:" + e for e in evs), lit("Held %s UTC by the lineage agent, ahead of the date planned (%s UTC), because the owner wants progress and slots are free: the discipline moves a baselined iteration only by a Rebaseline; this iteration had no baseline, so the ceremony sets its start (G70, G136 Q2(b)). No executor has started in it; work begun is recorded at the real start of each session." % (now, old))))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "%s opened by its planning ceremony at the real start %s (no baseline existed, so no Rebaseline); %d stories and %d tasks made Ready." % (IT, now, len(RS), len(RT)))))
