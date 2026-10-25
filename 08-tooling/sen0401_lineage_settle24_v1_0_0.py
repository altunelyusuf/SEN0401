#!/usr/bin/env python3
"""sen0401_lineage_settle24 v1_0_0 - closes the reviews of Iterations 22 and 23 (the stories whose every task is Done on bridge-verified evidence are recorded Done, T_Complete; SprintReviewCeremonies close both iterations), after the change route of ex:CR3_Retro24 withdrew
the carried regression story ST_Remedy_Regress_R (its criterion is restated as element (4) of AC9_Template, not waived). Ported from sen0401_lineage_settle21 (ST_Remedy_Tools closure and the review ceremonies); the tool evidence_of is imported from it.
Closed: ST_Ch07_Deck_Reissue and ST_PageTest_937 (Iteration 22, review RC3S_Iter_22); ST_Ch07_Page_R and ST_Ch08_Page_R (Iteration 23, review RC3S_Iter_23). Usage: no arguments; writes one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdflib
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_settle21_v1_0_0 as S21
lit = C.lit; CR = "ex:CR3_Retro24"
RULE = "the owner's standing orders (a lineage never waits on questions unrelated to its work; repairs re-rank the open items; work the lineage enforces but the actual work misses must be dealt with)"
CLOSE = [(22, "RC3S_Iter_22", [("ST_Ch07_Deck_Reissue", "AC7R_Deck_Ch07", "v0.257.0"), ("ST_PageTest_937", "AC7R_PageTest937", "v0.258.0")]),
         (23, "RC3S_Iter_23", [("ST_Ch07_Page_R", "AC8R_Page_Ch07", "v0.269.0"), ("ST_Ch08_Page_R", "AC8R_Page_Ch08", "v0.270.0")])]
def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
    g = rdflib.Graph(); g.parse(src, format="turtle")
    for n, rc, stories in CLOSE:
        for sid, crit, ver in stories:
            i, j = T.blk(t, sid); b = t[i:j]; assert "backlog:hasState backlog:InProgress" in b, sid
            tks = re.findall(r"ex:(TK_\w+)", re.search(r"backlog:decomposesInto ([^;]*);", b).group(1))
            for k in tks: assert "backlog:hasState backlog:Done" in t[T.blk(t, k)[0]:T.blk(t, k)[1]], (sid, k)
            ev = S21.evidence_of(g, tks); assert ev, sid
            fin = max(re.findall(r'finishedAt "([^"]*)"', "".join(t[T.blk(t, k)[0]:T.blk(t, k)[1]] for k in tks)))
            m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, sid
            time.sleep(1.1); at = M.now()
            nb = b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, at), 1)
            t = t[:i] + nb + t[j:]
            L.append(C.transition("Done24T_" + sid, sid, "T_Complete", at, "Done at the review ex:%s on %s UTC: its tasks %s are Done on bridge-verified evidence and the criterion ex:%s was controlled MET in the register %s (evidence bridge, the builder's own re-runs)." % (rc, at, ", ".join(tks), crit, ver), sid + " completed"))
            L.append('ex:Harness24_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (sid, lit("Checks run for " + sid), sid, ", ".join("ex:" + e for e in ev)))
            L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (sid, ", ".join("ex:" + e for e in ev), lit("Closed %s UTC at the review ex:%s by the lineage under %s: the criterion ex:%s is met on the bridge-verified evidence recorded in the tasks' audit notes (control in %s)." % (at, rc, RULE, crit, ver))))
    t2 = t + "\n" + "".join(L)
    for n, rc, stories in CLOSE:
        time.sleep(1.1); at = M.now(); I = "Iter_%d" % n; i, j = T.blk(t2, I); blk = t2[i:j]
        mem = re.findall(r"ex:((?:ST|TK)_\w+)", re.search(r"backlog:hasMember ([^.]*)\.", blk, re.S).group(1))
        bad = [x for x in mem if not re.search(r"hasState backlog:(Done|Cancelled)", t2[T.blk(t2, x)[0]:T.blk(t2, x)[1]])]
        assert not bad, (n, bad)
        flag = [x for x in mem if x.startswith("ST_") and "backlog:hasState backlog:Cancelled" in t2[T.blk(t2, x)[0]:T.blk(t2, x)[1]]]
        t2 += ('\nex:%s a backlog:SprintReviewCeremony ; rdfs:label %s@en ; backlog:ceremonyFor ex:%s ; backlog:reviewsCeremony ex:PC3_Iter_%d ; backlog:closesIteration ex:%s ; backlog:closesStory %s ;%s backlog:heldAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
            rc, lit("Review of iteration %d: the stories whose tasks are Done on verified evidence are closed, the iteration is closed" % n), I, n, I, ", ".join("ex:" + s[0] for s in stories),
            (" backlog:flagsForCarryOver " + ", ".join("ex:" + s for s in flag) + " ;") if flag else "", at,
            lit("Held %s UTC by the lineage agent under %s: every member of the iteration is Done or withdrawn (Cancelled) by the change route %s; the stories %s are recorded Done at this review. %s The readings of the objectives are those of the earlier review of the iteration." % (
                at, RULE, CR, ", ".join(s[0] for s in stories), ("The withdrawn story %s is flagged for carry-over: its criterion ex:AC8R_Regress is carried, not waived, as element (4) of ex:AC9_Template." % ", ".join(flag)) if flag else "Nothing is carried over."))))
    t3 = X.set_status(t2, "LS_InProgress")
    print(os.path.basename(M.write_new(src, t3, nxt, cur, "Reviews of Iterations 22 and 23 held: four stories recorded Done on bridge-verified evidence (the controls of v0.257.0, v0.258.0, v0.269.0, v0.270.0), both iterations closed; the carried regression story is withdrawn by the change route of %s." % CR)))
if __name__ == "__main__": main()
