#!/usr/bin/env python3
"""sen0401_lineage_rank v1_6_0 - RE-RANKS the open stories after completions (BP-D11: a score that predates the most recent completion must be re-run; the validator's L3 on v0.288.0). New dated RICE+DepFactor records (TAG from the environment RANK_TAG, default 42) for every open story that has a live PriorityScore:
Reach, Impact, Confidence and Effort are taken unchanged from its live record (no new judgement), the DepFactor is RECOMPUTED from the register (1 when every dependency of every task of the story is Done, 0.5 otherwise, the method's stipulation), and the earlier link is replaced by the link to the new record (the earlier record stays). A NEW file over v1_5_0.
Usage: sen0401_lineage_rank_v1_6_0.py"""
__version__ = "1.6.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdflib
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit; TAG = os.environ.get("RANK_TAG", "42")
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#")
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); g = rdflib.Graph(); g.parse(src, format="turtle"); L = []; rows = []
state = lambda x: str(g.value(x, B.hasState)).split("#")[-1]
for s in sorted(g.subjects(rdflib.RDF.type, B.Story), key=str):
    if state(s) in ("Done", "Cancelled"): continue
    live = list(g.objects(s, B.hasPriorityScore))
    if not live: continue
    sc = max(live, key=lambda x: str(g.value(x, B.scoredAt))); sid = str(s).split("#")[-1]
    R, I, Cf, Ef = (float(g.value(sc, p)) for p in (B.hasReach, B.hasImpact, B.hasConfidence, B.hasEffort)); old = float(g.value(sc, B.hasDepFactor) or 1)
    deps = {d for tk in g.objects(s, B.decomposesInto) for d in g.objects(tk, B.dependsOn)} - set(g.objects(s, B.decomposesInto))
    D = 1.0 if all(state(d) == "Done" for d in deps) else 0.5
    v = round(R * I * Cf / Ef, 2); key = round(v * D, 2); rows.append((key, sid))
    L.append('ex:Rank%s_%s a backlog:RICEScore ; rdfs:label %s@en ; backlog:scoredByMethod backlog:Method_RICE_DepFactor ;\n    backlog:hasReach "%s"^^xsd:decimal ; backlog:hasImpact "%s"^^xsd:decimal ; backlog:hasConfidence "%s"^^xsd:decimal ; backlog:hasEffort "%s"^^xsd:decimal ; backlog:hasDepFactor "%s"^^xsd:decimal ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
        TAG, sid, lit("Re-ranking of %s, %s" % (sid, now[:10])), R, I, Cf, Ef, D, v, now, lit("Re-run after completions (BP-D11): Reach, Impact, Confidence and Effort are those of the live record %s (unchanged, no new judgement); the dependency factor is recomputed from the register: %s (it was %s). Score = %s x %s x %s / %s = %.2f; ordering key = score x dependency factor = %.2f. A new dated record, no earlier record edited." % (str(sc).split("#")[-1], "1 (every dependency Done)" if D == 1 else "0.5 (a dependency is not Done; the method's stipulation)", old, R, I, Cf, Ef, v, key))))
    t, k = re.subn(r"^ex:%s backlog:hasPriorityScore ex:%s \.\n" % (sid, str(sc).split("#")[-1]), "", t, flags=re.M); assert k >= 1, sid
    L.append("ex:%s backlog:hasPriorityScore ex:Rank%s_%s .\n" % (sid, TAG, sid))
rows.sort(reverse=True); order = "; ".join("%d. %s (%.2f)" % (k + 1, r[1], r[0]) for k, r in enumerate(rows[:12]))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Open stories re-ranked after the completions of the decks of chapters 1 to 4 and the chapter 1 verify script (BP-D11; RICE+DepFactor, dependency factors recomputed); first of the order: " + order)))
for r in rows: print("%.2f %s" % r)
