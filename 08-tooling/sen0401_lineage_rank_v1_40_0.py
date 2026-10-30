#!/usr/bin/env python3
"""sen0401_lineage_rank v1_40_0 - re-rank of the open items (G147) after the exam Papers story was Done: a new dated record (tag 84) for every open story, same RICE + DepFactor rule as v1_37_0 (copied from it, with no new story). Usage: no arguments; writes one new register version."""
__version__ = "1.37.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit
TAG = "84"
FACTS = ("FACTS (v1_40_0): the urgent chapter 6 deck and page were delivered and controlled by the lineage agent; two defects of that work are the repairs ST_Repair_Ch06_DeckLayout and ST_Repair_Ch06_Lecture (ex:CR3_Ch06Repairs, ex:Revision_Lineage3_Backlog9, v0.690.0 to v0.694.0); the owner decided on 2026-10-30 07:45 Istanbul to return to the exams, the midterm first and the make-up later (ex:CR3_MidtermFirst): the make-up items and paper are the new stories ST_Exam_Items_Makeup and ST_Exam_Papers_Makeup, ranked behind with Impact 0.25 (minimal, a stipulation of the method's scale, as chapter 11 was), not dropped; the repairs have Impact 1 (medium) because the owner said the exams come first (a stipulation). A repair or a change re-ranks the open items (G147).")
ORDER = ["01", "02", "03", "04", "05", "06", "07", "08", "11"]
src0 = M.newest(); t0 = open(src0, encoding="utf-8").read()
import rdflib as _rdf
_g = _rdf.Graph(); _g.parse(data=t0, format="turtle"); _B = _rdf.Namespace("http://example.org/backlog#"); _E = _rdf.Namespace("http://example.org/sen0401-slides-lineage#")
def _st(x): return str(_g.value(x, _B.hasState)).split("#")[-1]
ITEMS = []
NEW = {}
for _s in sorted(_g.subjects(_rdf.RDF.type, _B.Story), key=str):
    sid = str(_s).split("#")[-1]
    if _st(_s) not in ("Proposed", "Ready", "InProgress", "Suspended"): continue
    _bt = "TK_" + sid[3:] + "_Build"; _deps = [d for d in _g.objects(_E[_bt], _B.dependsOn)]; _open = [str(d).split("#")[-1] for d in _deps if _st(d) != "Done"]; _D = 0.5 if _open else 1
    if sid in NEW:
        R_, I_, C_, E_ = NEW[sid]
        ITEMS.append((sid, "the story " + sid, R_, I_, C_, E_, _D, "New story, no earlier record. Reach %s, Impact %s and Confidence %s are stipulations of the method's scale; Effort %s hours is the Build task's estimate. The prerequisites of its Build task not Done: %s, so the dependency factor is %s (0.5 is a stipulation)." % (R_, I_, C_, E_, ", ".join(_open) or "none", _D))); continue
    _recs = sorted(re.findall(r"^ex:Rank(\d+)_%s a " % sid, t0, re.M), key=int)
    if not _recs: continue
    _rec = _recs[-1]; _blk = re.search(r"^ex:Rank%s_%s a .*?(?=^ex:\w+ a |\Z)" % (_rec, sid), t0, re.S | re.M).group(0)
    _g2 = lambda kk: re.search(r'backlog:has%s "([\d.]+)"' % kk, _blk).group(1)
    ITEMS.append((sid, "the story " + sid, float(_g2("Reach")), float(_g2("Impact")), float(_g2("Confidence")), float(_g2("Effort")), _D,
                  "Reach, Impact, Confidence and Effort are those of the live record Rank%s_%s (unchanged, no new judgement). The prerequisites of its Build task not Done: %s, so the dependency factor is %s (0.5 is a stipulation of the method)." % (_rec, sid, ", ".join(_open) or "none", _D)))
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
L.append("ex:Iter_54 rdfs:comment %s@en .\n" % lit("Ranking of %s (BP-D10, RICE with dependency factor; the scores are the newest records of each open story, ex:Rank%s_* for this one; ties break in chapter order, which these keys do not apply across kinds): %s. The scale values (impact levels, the dependency factor 0.5) are stipulations of the method's scale and are disclosed as such." % (now, TAG, order)))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
print(os.path.basename(M.write_new(src, t2, nxt, cur, "Dated RICE+DepFactor records (tag 84) after the Papers story was Done" + order)))
for r in rows: print("%.2f  %s" % (r[0], r[3]))
