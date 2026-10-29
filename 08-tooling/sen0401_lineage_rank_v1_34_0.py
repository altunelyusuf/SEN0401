#!/usr/bin/env python3
"""sen0401_lineage_rank v1_34_0 - after TK_Exam_PaperRules_Build and its story were controlled Done (v1_32_0, unchanged, did the same after the critical points) (G147: a completion re-ranks the open items): a new dated RICE+DepFactor record for every open exam and page-measurement story, Reach, Impact, Confidence and Effort unchanged from the live record, the dependency factor recomputed from the register. A NEW tool over v1_31_0 (unchanged); its docstring: the first dated RICE+DepFactor PriorityScore records (BP-D10, G147) for the 15 stories admitted by the stage revision for the exam work (seven exam stories, eight page measurements), and a new dated record for ST_Ch11_PageMeasure that puts it behind chapters 1 to 8 as the owner ordered on 2026-10-29. A NEW tool file over v1_30_0 (unchanged).
Scales (the method's): Impact 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal; Confidence 1 / 0.8 / 0.5; Effort in hours (the tasks' estimates); DepFactor 1 when every prerequisite is Done, 0.5 when one is not (0.5 is a stipulation).
The ordering key is the score times the DepFactor; ties break in the owner's chapter order (1, 2, 3, 4, 9 to 14). Usage: sen0401_lineage_rank_v1_5_0.py   (writes one new register version and prints the ranking)"""
__version__ = "1.34.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit
TAG = "78"
FACTS = ("FACTS (v1_34_0): TK_Exam_Engine_Build and ST_Exam_Engine are Done on the control of the lineage agent (v0.649.0, v0.650.0). The control of TK_Exam_AnswerMethods_Build gave NOT MET on the executor's own check C6 (v0.647.0); the repair is registered (ex:CR3_AnswerRepair, ex:Revision_Lineage3_Backlog7, v0.651.0 to v0.654.0) as the new story ex:ST_Exam_AnswerMethods_Repair, ranked first because the papers and the grading wait for it and it blocks the closing of the answering-methods story (G147: a repair re-ranks the open items). Earlier facts: "
         "FACTS: TK_Exam_CriticalPoints_Build, ST_Exam_CriticalPoints, TK_Exam_PaperRules_Build and ST_Exam_PaperRules are Done on the control of the lineage agent (register v0.637.0 to v0.641.0). The stories were admitted on 2026-10-29 by the stage revision ex:Revision_Lineage3_Scope30 on the owner's word. The owner's order: the exam scope is worked first (the midterm is next week); chapter work restarts on Sunday 2026-11-01; then the pages of chapters 1 to 6 are measured and completed first, chapters 7 and 8 only if time remains, chapter 11 and chapters 9 and above stay paused. Nothing is started; no urgent interruption is declared because no started item is held. Reach is 1 for each (one instructor, one course); the Impact levels are the method's scale and are stipulations; Effort is the hours of the Build task.")
ORDER = ["01", "02", "03", "04", "05", "06", "07", "08", "11"]
src0 = M.newest(); t0 = open(src0, encoding="utf-8").read()
import rdflib as _rdf
_g = _rdf.Graph(); _g.parse(data=t0, format="turtle"); _B = _rdf.Namespace("http://example.org/backlog#"); _E = _rdf.Namespace("http://example.org/sen0401-slides-lineage#")
def _st(x): return str(_g.value(x, _B.hasState)).split("#")[-1]
ITEMS = []
for _s in sorted(_g.subjects(_rdf.RDF.type, _B.Story), key=str):
    sid = str(_s).split("#")[-1]
    if not (sid.startswith("ST_Exam_") or sid.endswith("_PageMeasure")) or sid == "ST_Ch11_PageMeasure" or sid.endswith("_Repair") or _st(_s) not in ("Proposed", "Ready", "InProgress"): continue
    _rec = sorted(re.findall(r"^ex:Rank(\d+)_%s a " % sid, t0, re.M), key=int)[-1]
    _blk = re.search(r"^ex:Rank%s_%s a .*?(?=^ex:\w+ a |\Z)" % (_rec, sid), t0, re.S | re.M).group(0)
    _g2 = lambda kk: re.search(r'backlog:has%s "([\d.]+)"' % kk, _blk).group(1)
    _bt = "TK_" + sid[3:] + "_Build"; _deps = [d for d in _g.objects(_E[_bt], _B.dependsOn)]; _open = [str(d).split("#")[-1] for d in _deps if _st(d) != "Done"]
    _D = 0.5 if _open else 1
    ITEMS.append((sid, "the story " + sid, float(_g2("Reach")), float(_g2("Impact")), float(_g2("Confidence")), float(_g2("Effort")), _D,
                  "Reach, Impact, Confidence and Effort are those of the live record Rank%s_%s (unchanged, no new judgement). The prerequisites of its Build task not Done: %s, so the dependency factor is %s (0.5 is a stipulation of the method)." % (_rec, sid, ", ".join(_open) or "none", _D)))
_rb = "ST_Exam_AnswerMethods_Repair"
ITEMS = [(a, b, c, d, e, f, (0.5 if a == "ST_Exam_AnswerMethods" else g), (h + " ST_Exam_AnswerMethods can be Done only through the repair, so its dependency factor is 0.5 (a stipulation).") if a == "ST_Exam_AnswerMethods" else h) for a, b, c, d, e, f, g, h in ITEMS]
ITEMS.append((_rb, "the story " + _rb, 1.0, 3.0, 0.8, 3.0, 1, "New story, no earlier record. Reach 1.0, Impact 3 and Confidence 0.8 are those of the story it repairs (ST_Exam_AnswerMethods, Rank77), Effort 3 hours is the Build task's estimate; no prerequisite is open (the paper rules task is Done), so the dependency factor is 1. The scale values are stipulations of the method's scale."))
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []; rows = []
def chapter_rank(sid):
    m = re.search(r"Ch(\d\d)", sid); return ORDER.index(m.group(1)) if m and m.group(1) in ORDER else -1
for sid, lab, R, I, Cf, E, D, basis in ITEMS:
    assert ("ex:%s a backlog:Story" % sid) in t, sid
    v = round(R * I * Cf / E, 2); key = round(v * D, 2); rows.append((key, -chapter_rank(sid), sid, lab))
    i, j = T.blk(t, sid); b = t[i:j]; b2 = re.sub(r'\n?\s*backlog:notYetScoreable true ; backlog:hasScoreabilityReason "(?:[^"\\]|\\.)*" ;', '', b, count=1); pass
    t = t[:i] + b2 + t[j:]
    L.append('ex:Rank%s_%s a backlog:RICEScore ; rdfs:label %s@en ; backlog:scoredByMethod backlog:Method_RICE_DepFactor ;\n    backlog:hasReach "%s"^^xsd:decimal ; backlog:hasImpact "%s"^^xsd:decimal ; backlog:hasConfidence "%s"^^xsd:decimal ; backlog:hasEffort "%s"^^xsd:decimal ; backlog:hasDepFactor "%s"^^xsd:decimal ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
        TAG, sid, lit("Ranking of " + lab + ", " + now[:10]), R, I, Cf, E, D, v, now, lit("RICE with dependency factor (BP-D10): score = Reach x Impact x Confidence / Effort = %s x %s x %s / %s = %.2f; the dependency factor %s is recorded beside it and the ORDERING KEY is the score times the dependency factor = %.2f (ties break in chapter order of the list ORDER). %s %s A repair re-ranks the open items (G147); a new dated record, no earlier score is edited." % (R, I, Cf, E, v, D, key, basis, FACTS))))
    L.append("ex:%s backlog:hasPriorityScore ex:Rank%s_%s .\n" % (sid, TAG, sid))
for sid in ("ST_Ch11_PageMeasure",):
    recs = re.findall(r"^ex:Rank(\d+)_%s a " % sid, t, re.M); tag0 = max(int(x) for x in recs)
    blk = re.search(r"^ex:Rank%d_%s a .*?(?=^ex:\w+ a |\Z)" % (tag0, sid), t, re.S | re.M).group(0)
    g = lambda k: re.search(r'backlog:has%s "([\d.]+)"' % k, blk).group(1)
    R_, I_, C_, E_ = g("Reach"), "0.25", g("Confidence"), g("Effort"); v = round(float(R_) * float(I_) * float(C_) / float(E_), 2); D_ = 1
    L.append('ex:Rank%s_%s a backlog:RICEScore ; rdfs:label %s@en ; backlog:scoredByMethod backlog:Method_RICE_DepFactor ;\n    backlog:hasReach "%s"^^xsd:decimal ; backlog:hasImpact "%s"^^xsd:decimal ; backlog:hasConfidence "%s"^^xsd:decimal ; backlog:hasEffort "%s"^^xsd:decimal ; backlog:hasDepFactor "%s"^^xsd:decimal ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (TAG, sid, lit("Re-ranking of " + sid + ", " + now[:10]), R_, I_, C_, E_, D_, v, now, lit("Re-ranked (G147) because the stage revision for the exam work admitted new stories: Reach, Confidence and Effort are those of the live record Rank%d_%s; Impact is set to 0.25 (minimal, the method's scale, a stipulation) because the owner ordered chapter 11 behind chapters 1 to 8 and paused; the dependency factor is %s (no prerequisite open). Score = %s x %s x %s / %s = %.2f; ordering key = %.2f. %s" % (tag0, sid, D_, R_, I_, C_, E_, v, round(v * D_, 2), FACTS))))
    L.append("ex:%s backlog:hasPriorityScore ex:Rank%s_%s .\n" % (sid, TAG, sid))
rows.sort(reverse=True)
allrows = []
for m in re.finditer(r"^ex:(ST_\w+) a backlog:Story.*?(?=^ex:\w+ a )", t, re.S | re.M):
    sid = m.group(1); st = re.search(r"hasState backlog:(\w+)", m.group(0))
    if not st or st.group(1) not in ("Proposed", "Ready", "InProgress"): continue
    recs = re.findall(r"^ex:%s backlog:hasPriorityScore ex:Rank(\d+)_" % re.escape(sid), t + "".join(L), re.M)
    if not recs: continue
    tag = max(int(x) for x in recs); blk = re.search(r"^ex:Rank%d_%s a .*?(?=^ex:\w+ a |\Z)" % (tag, re.escape(sid)), t + "".join(L), re.S | re.M)
    if not blk: continue
    sv = re.search(r'hasScoreValue "([\d.]+)"', blk.group(0)); df = re.search(r'hasDepFactor "([\d.]+)"', blk.group(0))
    if sv and df: allrows.append((round(float(sv.group(1)) * float(df.group(1)), 2), sid))
allrows.sort(key=lambda x: (-x[0], x[1]))
order = "; ".join("%d. %s (%.2f)" % (k + 1, r[1], r[0]) for k, r in enumerate(allrows))
L.append("ex:Iter_47 rdfs:comment %s@en .\n" % lit("Ranking of %s (BP-D10, RICE with dependency factor; the scores are the newest records of each open story, ex:Rank%s_* for this one; ties break in chapter order, which these keys do not apply across kinds): %s. The scale values (impact levels, the dependency factor 0.5) are stipulations of the method's scale and are disclosed as such." % (now, TAG, order)))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
print(os.path.basename(M.write_new(src, t2, nxt, cur, "Dated RICE+DepFactor records (tag 78) after the engine was controlled Done and the answer sheet repair was registered: the repair story ranked, the open exam and page-measurement stories re-scored from the register (G147); no earlier record edited; ranking: " + order)))
for r in rows: print("%.2f  %s" % (r[0], r[3]))
