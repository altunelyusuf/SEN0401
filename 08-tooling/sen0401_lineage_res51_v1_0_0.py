#!/usr/bin/env python3
"""sen0401_lineage_res51 v1_0_0 - (the exam v6 corrections: the floor at 0, copy of res50) change route (G125 route 2) for the owner ruling of Monday 2026-11-02 16:52 Istanbul (relayed by the coordinator): the total of the whole paper is floored at 0 for both exams, no floor inside a question. Adds one story with one Build task and one Verify task: the scoring rule file and module as new versions with the floor, the instructor key text updated, the blind-mean figures recomputed. Usage: change | retract | backlog PREV | fill PREV."""
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
REV = "ex:Revision_Lineage3_Backlog27"; OLD = "ex:Out3_BacklogR54"; NEWB = "ex:Out3_BacklogR55"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamV6Floor"; IA = "ex:IA3_ExamV6Floor"
WHEN = "Monday 2026-11-02, on the owner ruling of 16:52 Istanbul, relayed by the coordinator"
WORDS = ("OWNER RULING (2026-11-02, 16:52 Istanbul, relayed by the coordinator), the answer to the floor point raised with the sheet and scoring work of the exam v6: the total of the whole paper is floored at 0 for both exams (SEN0401 and SEN0414); there is no floor inside a question. For SEN0401 the printed paper, cover and sheet need no change if they do not state a floor (the lineage agent checked: the cover says a wrong answer can cost part of its points and a blank costs nothing; sheet page 2 says a blank answer costs nothing; neither states a total or a floor), but the instructor key and the scoring module's floor setting must say so. The measured figures before the ruling (lineage agent, 20000 blind sheets that mark every place, the v6 key of 100 points): mean of the raw total -0.05, mean of the floored total +3.65, 53 percent of the blind sheets fall below 0 and are floored; the owner's SEN0414 figure is about +4.3 of 110.")
COMMON = " COMMON RULES: write every file that holds a question, an answer, a key or a sheet into /home/claude/CME/exams/SEN0401/08-tooling/exam/ (same relative layout) and commit it in CME yourself (git -C /home/claude/CME pull --rebase --autostash first, add by path, commit, push); commit to SEN0401 only scripts and data files that hold no question and no answer (the lineage agent's leak search is run on your commit)."
SPEC = {"ST_Exam_V6_Floor": ("The scoring rule file and module have the floor of the paper total at 0, the instructor key says so, and the blind-mean figures are recomputed", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I76-examv6floor", 1.0, 0.5, "v6floor", [])}
TK = {"ST_Exam_V6_Floor": "Exam_V6_Floor"}
BRIEFS = {
"v6floor": WORDS + " ITEM: new versions only, never edit a committed file. (1) The scoring module sen0401_exam_scoring_v1_0_0.py and its rule file become v1_1_0 files (copies): the field total_floor reads 'DECIDED by the owner on 2026-11-02 16:52 Istanbul: the total of the whole paper is not below 0 (floor at 0 on the paper total, none inside a question)', score() applies the floor to the total by default (the bonus is added after and is not a penalty), and every printed or generated sentence that says the total is not raised to 0 is changed. (2) The scoring check is a new version that proves the floor: a sheet whose raw total is below 0 gives total 0 and its per-question points keep their signs, a sheet above 0 is unchanged, a perfect sheet gives 100, a blank sheet 0; the blind simulation (at least 20000 blind sheets that mark every place, on the v6 key) reports the mean of the raw total, the mean of the floored total, the share of blind sheets floored and the 95th percentile, printed as they are (the lineage agent measured raw -0.05, floored +3.65, 53 percent floored: say whether yours agree). The mean of the floored total is above 0 by construction; state it plainly as the owner's ruling and give the number for a student who answers only the places a guesser would and for the all-blank sheet. (3) The instructor key of the v6 paper (the key.docx and key.pdf, and the key.json scoring note) is rebuilt as a new version of the key only: the lines that say the total is not raised to 0 or that a floor would give a blind guesser a gain are replaced by the ruling and the measured figures; the paper docx and the sheet are NOT changed, and their SHA-256 must be equal to those of commit e8efedb (print them). (4) Check the printed paper, cover and sheet page 2 for any sentence that contradicts a floor at 0 and report the result (the lineage agent found none). Leak search on the public commit. Report with the numbers as printed." + COMMON,
}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {
"ST_Exam_V6_Floor": ("AC9_Exam_V6_Floor", "The scoring rule and module floor the paper total at 0, the instructor key says so and the blind-mean figures are recomputed, with the paper and the sheet unchanged", "Owner ruling (" + CR + ", " + WHEN + "). Given the ruling that the paper total is floored at 0 for both exams and no floor inside a question, when the correction is made, then ALL of: (1) the scoring rule file and module are new versions with the floor on the paper total, no committed file is edited; (2) the scoring check proves the floor on a sheet below 0, a sheet above 0, a perfect sheet and a blank sheet; (3) the blind-mean figures (raw, floored, share floored) are recomputed on at least 20000 blind sheets of the v6 key and printed; (4) the instructor key says so and no longer says the total is not raised to 0; (5) the paper and the sheet are byte-identical to commit e8efedb; (6) the leak search of the public tree passes."),
}

NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The paper total of both exams is floored at 0 (owner ruling)"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the floor at 0 costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: one new story with two tasks (about 4 agent-hours); no existing task depends on it, but every later exam artefact is written to the CME location; the open items are re-ranked (G147)."))
    return t + cr + ia, "Change request with impact assessment: the corrected exam: items, sheet, reader, readability tool and papers; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the the floor at 0 correction"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the floor at 0 correction; nothing is rebuilt here." % OLD.replace("ex:", "")
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
    i, j = T.blk(t, ITER); b = t[i:j]; m = re.search(r"backlog:hasMember ([^;.]*?)( ;| \.|\.\n)", b, re.S); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:hasMember " + m.group(1).rstrip() + ", " + ", ".join("ex:" + x for x in mem) + m.group(2), 1) + t[j:]
    L.append('ex:SC3_ExamV6Floor a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the floor-at-0 correction story"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamV6Floor; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the floor at 0 correction"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEWB, X.digest(t, "Backlog")), \
        "third lineage, Backlog stage rebuilt: one story with two tasks (the floor at 0 correction) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
