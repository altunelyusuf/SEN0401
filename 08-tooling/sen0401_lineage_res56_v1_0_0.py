#!/usr/bin/env python3
"""sen0401_lineage_res56 v1_0_0 - (the exam v7 redesign, five stories, copy of res51) (the exam v6 corrections: the floor at 0, copy of res50) change route (G125 route 2) for the owner ruling of Monday 2026-11-02 16:52 Istanbul (relayed by the coordinator): the total of the whole paper is floored at 0 for both exams, no floor inside a question. Adds one story with one Build task and one Verify task: the scoring rule file and module as new versions with the floor, the instructor key text updated, the blind-mean figures recomputed. Usage: change | retract | backlog PREV | fill PREV."""
__version__ = "1.0.0"
import os, re, sys, glob, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_retro24_v1_0_0 as RT
R = RT.R; lit = G.lit
def _pv_newest():
    fw = X.FW; vk = lambda q: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", q)[0]]
    spec = importlib.util.spec_from_file_location("pv", sorted(glob.glob(fw + "/03-tooling/backlog_pipeline_verify_v*.py"), key=vk)[-1])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.STAGE_TYPES = m._load_stage_types(sorted(glob.glob(fw + "/01-ontologies/backlog_tbox_v*.ttl"), key=vk)[-1], table="v4")
    return m
X._pv = _pv_newest



import json
REV = "ex:Revision_Lineage3_Backlog32"; OLD = "ex:Out3_BacklogR59"; NEWB = "ex:Out3_BacklogR60"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamV71I"; IA = "ex:IA3_ExamV71I"
WHEN = "Monday 2026-11-02, on the owner's order of 21:06 Istanbul, relayed by the coordinator"
WORDS = ("OWNER ORDER (2026-11-02, 21:06 Istanbul, relayed by the coordinator), under the running urgency: 'Code questions are crazy. We need to replace them.' The owner then answered: SEN0401 code traces only (SEN0414 stays as delivered); replace them with hand calculations (short number problems from taught material such as fees, halving, hash counts and sizes, answered by a number in the boxes; no code reading). The three Question 2 items whose answer is the output of a program listing are 2a (mt4b:ef1:tries-after-adjustment, critical point CP2.12), 2d (mt2:i11:trace-release-tags, CP3.03) and 2f (mt2:i19:trace-gap-limit, CP5.20), 3, 3 and 4 points. The final set sen0401_exam_midterm_v7_1_0 is rendered on the NEW structure, so the sheet boxes follow the new digit counts. Rules: items v1.7.0 and structure v1.4.0 are NEW files (v1.6.1 and v1.3.1 stay); each replaced item keeps its position, its whole points and holds the same critical point, so no critical point loses its holder (CP3.03 and CP5.20 are held by no other item); taught material only; each answer is a number with an exact value, recomputed by RUNNING code (the calculation is done in code and never shown to students); one Tip of at most 12 words under the stem; stem at most 60 words; NO code listing in any Question 2 item; the R6 repair: the tip of the txid and weight fill-in (4e/4f) is reworded so that SegWit is spelled out at first use (Segregated witness) and the tip keeps at most 12 words; options, answers and points of the other items do not change; no deduction, no bonus, no floor.")
COMMON = " COMMON RULES: write every file that holds a question, an answer, a key or a sheet into /home/claude/CME/exams/SEN0401/08-tooling/exam/ (same relative layout) and commit it in CME yourself (git -C /home/claude/CME pull --rebase --autostash first, add by path, commit, push); commit to SEN0401 only scripts and data files that hold no question and no answer (the lineage agent's leak search is run on your commit); all new files are new versions, never edit a committed file, never weaken a gate; report every result as the tool prints it (NOT_MEASURED and NOT_RUN are not passes); Word pagination is NOT_MEASURED (LibreOffice export only). THIS IS URGENT: the owner prints today."
SPEC = {
"ST_Exam_V71_Items": ("Items v1.7.0 and structure v1.4.0: the three code traces replaced by hand calculations, the SegWit tip repaired", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I87-examv71items", 2.0, 0.5, "v71items", []),
}
TK = {k: k[3:] for k in SPEC}
BRIEFS = {
"v71items": WORDS + " ITEM (stated first): items v1.7.0 and structure v1.4.0. Resume the Items fixer session. Make NEW files (never edit a committed file) in CME private/: items v1.7.0, structure v1.4.0, builder and check v1.7.0, starting from items v1.6.1 and structure v1.3.1. (a) Replace 2a, 2d and 2f (exactly those three) by three hand-calculation items of type NumericAnswer in the same positions with the same points (3, 3, 4), holding CP2.12, CP3.03 and CP5.20; use only taught material of the chapters of the replaced item (chapters 1,2; 3; 5), numbers chosen so that no calculator is needed beyond one or two short steps and the exact answer is a whole number of at most 5 digits; no two numbers shared with an existing item; the key value recomputed by running your own code, and a second independent route (a different formula) must give the same value; the new items need the fields of a NumericAnswer item of v1.6.1 (copy one), computed, understanding, abbreviations, tip. (b) No Question 2 item has a code listing or the words 'program prints'; the answer-format line says: Write the number in the boxes, one digit in each box, starting from the right (with the unit in words when it has one). (c) Repair R6: reword the tip of the txid and weight fill-in (mt2:i23) so SegWit is spelled out at first use as Segregated witness, at most 12 words after 'Tip:'. (d) Check v1.7.0: everything the v1.6.1 check proves (21 items, five alternatives, tips of at most 12 words, stems of at most 60 words, whole-number rows, total 100, keys recomputed by running code, critical points: every point that had a holder still has one, the three critical points named above held by the new items), plus: no code listing in Question 2, the three old keys are not reused, the answer hashes of the 18 other items equal v1.6.1, the scoring check v2_0_0 on a shape built from the new structure (structure_to_shape tool) gives 21 of 21 with the exact blind figure printed as a fraction (about 15.7 expected; report the exact value), the engine check v1_2_0 on the new items (16 of 16), and the readability check v1.1.0 on the items source (R1 to R4 and R6 PASS; R5 is NOT_MEASURED without a cover) with R6 reported as printed. (e) A table of changes: the three old item keys, the three new keys, the critical points, the digit counts of the new answers (the digit counts decide the sheet boxes). Machine has 2 CPUs: run heavy checks at nice 10. Commit to CME and the check and builder scripts (no question, no answer) to SEN0401 yourself with trailers.",
}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {
"ST_Exam_V71_Items": ("AC9_Exam_V71_Items", "Items v1.7.0 and structure v1.4.0 have hand calculations in place of the three code traces and the SegWit tip is repaired", "Owner order (" + CR + ", " + WHEN + "). Given the order that code questions are replaced by hand calculations, when the items are made, then 2a, 2d and 2f are number problems from taught material with the same points and the same critical points, no Question 2 item has a code listing, each key is recomputed by running code by two routes, the other 18 items are unchanged, the scoring check gives 21 of 21 with the exact blind figure, the readability check passes R1 to R4 and R6, and the digit counts are tabled."),
}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The exam v7: no deductions, no bonus, five alternatives, short tips, one-page sheet"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the exam v7 redesign costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: one new story with two tasks (about 4 agent-hours); no existing task depends on it, but every later exam artefact is written to the CME location; the open items are re-ranked (G147)."))
    return t + cr + ia, "Change request with impact assessment: the corrected exam: items, sheet, reader, readability tool and papers; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the the exam v7 redesign"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the exam v7 redesign; nothing is rebuilt here." % OLD.replace("ex:", "")
def setdeps(t, tid, deps):
    i, j = T.blk(t, tid); b = t[i:j]
    m = re.search(r"backlog:dependsOn ([^;]*?) ;", b)
    if m: b = b.replace(m.group(0), "backlog:dependsOn " + m.group(1).rstrip() + ", " + ", ".join("ex:" + d for d in deps) + " ;", 1)
    else:
        m = re.search(r"backlog:hasState backlog:\w+ ;", b); b = b[:m.end()] + "\n    backlog:dependsOn " + ", ".join("ex:" + d for d in deps) + " ;" + b[m.end():]
    return t[:i] + b + t[j:]
def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; mem = []
    for sid, (title_, deliv, obj, sess, hb, hv, brief, deps) in SPEC.items():
        aid, label, g_ = CRIT[sid]; k = aid[4:]
        L.append(RT.ac_block(aid, label, g_, 'ex:TS_ChapterCheck, ex:TS_DeckMatch', "the checks of the task, run again by the lineage agent; papers control; LibreOffice render; reader on the sheet PDF", k).replace("ex:TC9_", "ex:TC9Z_"))
        L.append(RT.case_blocks(k, aid).replace("Spec3I_Retro24", "Spec3I_Ch06Teach").replace("ex:Data3S_TC9_", "ex:Data3S_TC9Z_").replace("ex:TC9_", "ex:TC9Z_")
            .replace("Run the checks on the item as measured in the baseline of 2026-10-25 (an overlap, a manifest example that starts with an error name, a story whose text lies below the first screen, a committed file with status M) and require that nothing is claimed for it.", "Run the checks on the item as it stands before the work and require that nothing is claimed for it.")
            .replace("The finding as measured in the baseline of 2026-10-25 (ex:IA3_Retro24).", "The finding as measured on 2026-11-01 (" + IA + ")."))
        tb, tv = "TK_%s_Build" % TK[sid], "TK_%s_Verify" % TK[sid]; mem += [sid, tb, tv]
        L.append(R.story_block(sid, title_, deliv, obj, [aid], [tb, tv], NOTE, "ex:" + ITER, "Proposed"))
        note_b = bodyof(brief) + " REUSE: use the existing tools and files named in the task and never edit a committed file. ONE EXECUTOR SESSION: " + sess + "."
        L.append(R.task_block(tb, "Build: " + title_, "Build", deps, sess, "S", hb, note_b, "ex:" + ITER, "Proposed", True))
        L.append(R.task_block(tv, "Verify: " + title_, "Verify", [tb], "builder", "S+%.1fh" % hb, hv, "Run the checks of the criterion again myself, with my own control scripts and the existing tools, on the new files; open every produced file; read the report of the executor against the files; register Done only on files I have re-run.", "ex:" + ITER, "Proposed", True))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
        L.append("ex:Obj3_%s backlog:metricMovableBy ex:%s .\n" % ("Exam" if obj.endswith("Exam") else "ChapterCode", sid))
    t = setdeps(t, "TK_Exam_V71_Papers_Build", ["TK_Exam_V71_Items_Build"])
    ia_, ja_ = T.blk(t, "TK_Exam_V71_Papers_Build"); bb_ = t[ia_:ja_]
    assert "real items v1.6.1 and structure v1.3.1" in bb_
    bb_ = bb_.replace("real items v1.6.1 and structure v1.3.1", "NEW items v1.7.0 and structure v1.4.0 (three code traces replaced by hand calculations, SegWit tip repaired; the render regenerates the sheet and its Question 2 boxes from the NEW structure, so the box counts follow the new answers; the sheet tooling of the V71 Sheet task was built on v1.3.1 and must be re-run on v1.4.0)")
    bb_ = bb_.replace("Do NOT start until TK_Exam_V71_Sheet_Build is Done", "Do NOT start until TK_Exam_V71_Sheet_Build AND TK_Exam_V71_Items_Build are Done").replace("R6 is known to fail for the SegWit tip of 4e/4f in v7.0.0 and the owner decided to print it; report it again, do not reword items", "R6 is repaired in items v1.7.0 and must PASS; report it as printed; the code traces are replaced by hand calculations")
    t = t[:ia_] + bb_ + t[ja_:]
    i, j = T.blk(t, ITER); b = t[i:j]; m = re.search(r"backlog:hasMember ([^;.]*?)( ;| \.|\.\n)", b, re.S); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:hasMember " + m.group(1).rstrip() + ", " + ", ".join("ex:" + x for x in mem) + m.group(2), 1) + t[j:]
    L.append('ex:SC3_ExamV71I a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the exam v7 stories"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamV71I; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the exam v7 redesign"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEWB, X.digest(t, "Backlog")), \
        "third lineage, Backlog stage rebuilt: one story with two tasks (the exam v7 redesign) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
