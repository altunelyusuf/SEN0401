#!/usr/bin/env python3
"""sen0401_lineage_readings24 v1_0_0 - records the readings of the objectives Obj3_Repair20 and Obj3_Repair21 at the reviews RC3S_Iter_22 and RC3S_Iter_23 (the validator's L3 asks for a MetricObservation dated at or after the finish of each story closed Done in v0.280.0;
the rank and settle tools before this one recorded none). New file over v0.281.0 or later; one event. Values are read from the register: the count of the stories of each objective that are Done on bridge-verified evidence."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); time.sleep(1.1); now = M.now(); L = []
R = [("Obj3_Repair20", "Met3_Repair20", "RC3S_Iter_22", ["ST_Ch07_Deck_Reissue", "ST_PageTest_937", "ST_Section_Links_Ch11"], "the deck of chapter 7 re-issued (controlled MET in v0.257.0) and the page test 9.37.0 (controlled MET in v0.258.0) are Done; the section-link remainder (ST_Section_Links_Ch11) is withdrawn by the change route of CR3_Retro24 and its work is carried by the page of chapter 11 in Iteration 27"),
     ("Obj3_Repair21", "Met3_Repair21", "RC3S_Iter_23", ["ST_Ch07_Page_R", "ST_Ch08_Page_R", "ST_Remedy_Regress_R"], "the page of chapter 7 (controlled MET in v0.269.0) and the page 9.85.0 of chapter 8 (controlled MET in v0.270.0) are Done; the regression story (ST_Remedy_Regress_R) is withdrawn by the change route of CR3_Retro24 and its criterion is carried as element (4) of AC9_Template")]
for obj, met, rc, sts, why in R:
    n = 0
    for s in sts:
        i, j = T.blk(t, s); n += 1 if "backlog:hasState backlog:Done" in t[i:j] else 0
    L.append('ex:ObsR24_%s a backlog:MetricObservation ; rdfs:label %s@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony ex:%s ;\n    backlog:hasObservationMethod %s .\n' % (
        obj, lit("Reading at the review %s" % rc), met, obj, n, now, rc, lit("Read %s UTC in this run from the register: the count of the stories %s that are Done: %d of %d; %s." % (now, ", ".join(sts), n, len(sts), why))))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Readings of the objectives Obj3_Repair20 and Obj3_Repair21 at the reviews of Iterations 22 and 23 (MetricObservations dated after the finish of the closed stories).")))
