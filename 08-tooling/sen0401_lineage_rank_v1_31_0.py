#!/usr/bin/env python3
"""sen0401_lineage_rank v1_31_0 - the first dated RICE+DepFactor PriorityScore records (BP-D10, G147) for the 15 stories admitted by the stage revision for the exam work (seven exam stories, eight page measurements), and a new dated record for ST_Ch11_PageMeasure that puts it behind chapters 1 to 8 as the owner ordered on 2026-10-29. A NEW tool file over v1_30_0 (unchanged).
Scales (the method's): Impact 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal; Confidence 1 / 0.8 / 0.5; Effort in hours (the tasks' estimates); DepFactor 1 when every prerequisite is Done, 0.5 when one is not (0.5 is a stipulation).
The ordering key is the score times the DepFactor; ties break in the owner's chapter order (1, 2, 3, 4, 9 to 14). Usage: sen0401_lineage_rank_v1_5_0.py   (writes one new register version and prints the ranking)"""
__version__ = "1.31.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit
TAG = "75"
FACTS = ("FACTS: the stories were admitted on 2026-10-29 by the stage revision ex:Revision_Lineage3_Scope30 on the owner's word. The owner's order: the exam scope is worked first (the midterm is next week); chapter work restarts on Sunday 2026-11-01; then the pages of chapters 1 to 6 are measured and completed first, chapters 7 and 8 only if time remains, chapter 11 and chapters 9 and above stay paused. Nothing is started; no urgent interruption is declared because no started item is held. Reach is 1 for each (one instructor, one course); the Impact levels are the method's scale and are stipulations; Effort is the hours of the Build task.")
ITEMS = [("ST_Exam_CriticalPoints", "the critical points of the exam chapters", 1, 3, 0.8, 3.0, 1, "Impact 3 (massive): every item of the exams is grounded in them. No prerequisite, so the dependency factor is 1."),
         ("ST_Exam_PaperRules", "the paper rules for the printed exam", 1, 3, 0.8, 3.0, 1, "Impact 3 (massive): the engine, the answering methods and the papers follow these rules. No prerequisite, so the dependency factor is 1."),
         ("ST_Exam_Engine", "the general exam engine", 1, 3, 0.8, 4.0, 0.5, "Impact 3 (massive). Its prerequisite TK_Exam_PaperRules_Build is not Done, so the dependency factor is 0.5 (a stipulation of the method)."),
         ("ST_Exam_AnswerMethods", "the answer sheet and the answering methods", 1, 3, 0.8, 3.0, 0.5, "Impact 3 (massive): the printed paper cannot be sat without it. Its prerequisite TK_Exam_PaperRules_Build is not Done, so the dependency factor is 0.5."),
         ("ST_Exam_Items", "the items of the two exams", 1, 3, 0.8, 4.0, 0.5, "Impact 3 (massive). Its prerequisites TK_Exam_CriticalPoints_Build and TK_Exam_Engine_Build are not Done, so the dependency factor is 0.5."),
         ("ST_Exam_Papers", "the two printed papers with keys", 1, 3, 0.8, 3.0, 0.5, "Impact 3 (massive). Its prerequisites are not Done, so the dependency factor is 0.5."),
         ("ST_Exam_Grading", "the grading method and tool", 1, 3, 0.8, 4.0, 0.5, "Impact 3 (massive): the exam cannot be graded without it. Its prerequisite TK_Exam_AnswerMethods_Build is not Done, so the dependency factor is 0.5.")]
for n in range(1, 9):
    items_i = 1 if n <= 6 else 0.5
    ITEMS.append(("ST_Ch%02d_PageMeasure" % n, "the measurement of the page of chapter %d" % n, 1, items_i, 0.8, 3.0, 1, "Impact %s (%s): the owner ordered chapters 1 to 6 first, chapters 7 and 8 only if time remains. ST_PageTest_Click is Done, so the dependency factor is 1." % (items_i, "medium" if n <= 6 else "low")))
ORDER = ["01", "02", "03", "04", "05", "06", "07", "08", "11"]
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []; rows = []
def chapter_rank(sid):
    m = re.search(r"Ch(\d\d)", sid); return ORDER.index(m.group(1)) if m and m.group(1) in ORDER else -1
for sid, lab, R, I, Cf, E, D, basis in ITEMS:
    assert ("ex:%s a backlog:Story" % sid) in t, sid
    v = round(R * I * Cf / E, 2); key = round(v * D, 2); rows.append((key, -chapter_rank(sid), sid, lab))
    i, j = T.blk(t, sid); b = t[i:j]; b2 = re.sub(r'\n?\s*backlog:notYetScoreable true ; backlog:hasScoreabilityReason "(?:[^"\\]|\\.)*" ;', '', b, count=1); assert b2 != b, sid
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
print(os.path.basename(M.write_new(src, t2, nxt, cur, "First dated RICE+DepFactor PriorityScore records for the 15 stories admitted for the exam work and the page measurements, and a new record for ST_Ch11_PageMeasure behind chapters 1 to 8 (G147); no earlier record edited; ranking: " + order)))
for r in rows: print("%.2f  %s" % (r[0], r[3]))
