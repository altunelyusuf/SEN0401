#!/usr/bin/env python3
"""sen0401_lineage_settle25 v1_0_0 - records Done the stories whose every task is Done on bridge-verified evidence (the framework's StoryReadyToCloseShape proposes exactly this; a story is closed by T_Complete on its evidence, a review ceremony being needed only to close an iteration, which closes
with a disposition for every story still in it, IterationNotCleanedShape). No iteration is closed here: Iterations 24, 25, 27 and 28 still hold open stories. Then one MetricObservation per objective whose movable stories were closed (L3: a reading dated at or after the finish of a closed story).
Ported from sen0401_lineage_settle24 (evidence_of from settle21). Usage: no arguments; writes one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdflib
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_settle21_v1_0_0 as S21
lit = C.lit
RULE = "the owner's standing orders (a lineage never waits on questions unrelated to its work; work the lineage enforces but the actual work misses must be dealt with) and the framework's StoryReadyToCloseShape (a story whose tasks are all Done is proposed for closing)"
OBJ = {"Obj3_Retro24": "Met3_Retro24", "Obj3_Res01": "Met3_Res01"}
def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); g = rdflib.Graph(); g.parse(src, format="turtle"); L = []; closed = []
    for s in sorted(set(re.findall(r"^ex:(ST_\w+) a backlog:Story", t, re.M))):
        i, j = T.blk(t, s); b = t[i:j]
        if "backlog:hasState backlog:InProgress" not in b: continue
        m0 = re.search(r"backlog:decomposesInto ([^;]*);", b)
        if not m0: continue
        tks = re.findall(r"ex:(TK_\w+)", m0.group(1))
        if not tks or any("backlog:hasState backlog:Done" not in t[T.blk(t, k)[0]:T.blk(t, k)[1]] for k in tks): continue
        ev = S21.evidence_of(g, tks)
        if not ev: print("no bridge evidence, not closed:", s); continue
        crit = re.search(r"backlog:hasAcceptanceCriterion ex:(\w+)", b).group(1)
        fin = max(re.findall(r'finishedAt "([^"]*)"', "".join(t[T.blk(t, k)[0]:T.blk(t, k)[1]] for k in tks)))
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, s
        time.sleep(1.1); at = M.now()
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, at), 1) + t[j:]
        L.append(C.transition("Done25T_" + s, s, "T_Complete", at, "Done on %s UTC: its tasks %s are Done on bridge-verified evidence and the criterion ex:%s was controlled MET (the audit note of the criterion names the version of the control); closed by the lineage under %s." % (at, ", ".join(tks), crit, RULE), s + " completed"))
        L.append('ex:Harness25_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (s, lit("Checks run for " + s), s, ", ".join("ex:" + e for e in ev)))
        L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (s, ", ".join("ex:" + e for e in ev), lit("Closed %s UTC by the lineage under %s: the criterion ex:%s is met on the bridge-verified evidence recorded in the tasks' audit notes. No iteration review is held: the iteration still holds open stories." % (at, RULE, crit))))
        closed.append(s)
    t2 = t + "\n" + "".join(L); R = []
    time.sleep(1.1); now = M.now()
    for obj, met in OBJ.items():
        i, j = T.blk(t2, obj); b = t2[i:j]; mem = re.findall(r"ex:(ST_\w+)", (re.search(r"backlog:metricMovableBy ([^.]*)\.", t2) and "" or ""))
    for obj, met in OBJ.items():
        mm = re.search(r"ex:%s backlog:metricMovableBy ([^.]*)\." % obj, t2); sts = re.findall(r"ex:(ST_\w+)", mm.group(1)) if mm else []
        n = sum(1 for s in sts if "backlog:hasState backlog:Done" in t2[T.blk(t2, s)[0]:T.blk(t2, s)[1]])
        R.append('ex:ObsR25_%s a backlog:MetricObservation ; rdfs:label %s@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n    backlog:observedAt "%s"^^xsd:dateTime ;\n    backlog:hasObservationMethod %s .\n' % (
            obj, lit("Reading after the closing of stories, %s" % now[:10]), met, obj, n, now, lit("Read %s UTC in this run from the register: the count of the stories of the objective that are Done: %d of %d (%s). No review ceremony links it: none is held." % (now, n, len(sts), ", ".join(s for s in sts if "backlog:hasState backlog:Done" in t2[T.blk(t2, s)[0]:T.blk(t2, s)[1]])))))
    print(os.path.basename(M.write_new(src, X.set_status(t2 + "\n" + "".join(R), "LS_InProgress"), nxt, cur, "Stories recorded Done on bridge-verified evidence (%s); readings of the objectives Obj3_Retro24 and Obj3_Res01 taken after them." % ", ".join(closed)))); print(closed)
if __name__ == "__main__": main()
