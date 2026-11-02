#!/usr/bin/env python3
"""sen0401_lineage_res47 v1_0_0 - (the exam move to CME, copy of res45) (was: copy of res38 for the repair of the chapter 3 page v9_74_0: a defect found by the lineage agent in the quiet window of 2026-11-01) change route (G125 route 2, G133, G147) for the owner's words of 2026-11-01 13:04 Istanbul on the exam: the IKU cover page as page 1, five question formats (4 x 25 points, the 5th 10 points bonus), no memorising items, tips for terms, abbreviations spelled out, 4 pages (else 6). Adds the stories of the cover renderer, items v1.2.0, papers/key/sheet v3, the honesty-check successor and the Ch05 Teach repair task. Usage: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog24"; OLD = "ex:Out3_BacklogR51"; NEWB = "ex:Out3_BacklogR52"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamMoveCME"; IA = "ex:IA3_ExamMoveCME"
WHEN = "Monday 2026-11-02, on the owner's decision of 10:27 Istanbul, relayed by the coordinator"
WORDS = ("OWNER DECISION (2026-11-02, 10:27 Istanbul, relayed by the coordinator): move the exams to the CME repository, which is private. Background measured by the lineage agent: the SEN0401 repository is PUBLIC and its history already holds exam papers, keys and items with answers (papers_midterm_v1, v2 and v3, items v1.1.0 to v1.3.0). A copy executor started at 2026-11-02T07:28:00Z and copies the exam material (08-tooling/exam including private/, the papers, the items, and the backup folder) to the CME repository; it deletes nothing. THE ORDER, in the owner's words 'move': after the copy is verified by hash, the answer-bearing tracked exam files are removed from the working tree of the public SEN0401 repository by a new commit. Committed history stays: a history rewrite is NOT decided and NOT ordered. From now on every NEW exam artefact (the items merge, the papers, keys, sheets) is written to the CME location that the copy executor reports and not to the SEN0401 repository; private/ stays only as scratch until then. The guard in .gitignore stays. ")
SPEC = {"ST_Exam_Move_Copy": ("The exam material is copied to the private CME repository and the copy is verified by hash", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I68-examcopy", 1.0, 0.5, "examcopy", []),
 "ST_Exam_Move_Remove": ("The answer-bearing tracked exam files are removed from the public SEN0401 working tree after the verified copy", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I69-examremove", 0.5, 0.5, "examremove", ["TK_Exam_Move_Copy_Build"])}
TK = {"ST_Exam_Move_Copy": "Exam_Move_Copy", "ST_Exam_Move_Remove": "Exam_Move_Remove"}
BRIEFS = {"examcopy": WORDS + "ITEM (stated first): THE COPY. This task is already running (copy executor, start 2026-11-02T07:28:00Z, registered afterwards on the owner's order and disclosed as such). WHAT TO DO: copy 08-tooling/exam (all tracked files and private/), the papers and items folders, and /home/claude/exam_private_backup to the CME repository (private) into one new folder, keeping the relative layout; delete NOTHING; print for every file the SHA-256 at the source and at the copy and a table of equal and different; write a manifest (file, size, hash) into the CME folder; commit in CME only (never in SEN0401 beyond your own script), by path, under flock /tmp/sen0401_git.lock for SEN0401 and the git rules of CME; confirm that the CME repository is private (gh repo view, printed); report the CME location and every number as printed, a missing or unequal file included. Nothing is committed to SEN0401 that holds a question or an answer.",
 "examremove": WORDS + "ITEM (stated first): THE REMOVAL. Do not start until the lineage agent has controlled the hash-verified copy (its Verify task is Done). WHAT TO DO: list the tracked files of the SEN0401 repository that hold answers (papers_midterm_v*/ keys, papers, items json from v1.1.0, the *_key.* files, answer-bearing check logs), show for each that its copy in CME has the same SHA-256, then remove exactly those files from the working tree with git rm in ONE new commit (message names the owner's decision of 2026-11-02 10:27 and that history stays); do NOT rewrite history, do NOT remove tools, scripts, structure files, topics or analysis that hold no answers unless the listing shows an answer in them; the .gitignore guard stays and is extended only by a new line if the listing shows a path it does not cover; after the commit print git ls-files for 08-tooling/exam and prove with grep that no key or items file remains tracked. Report the commit id and every count as printed."}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {"ST_Exam_Move_Copy": ("AC9_Exam_Move_Copy", "Every exam file of the SEN0401 repository, its private folder and the backup has a copy in the private CME repository with the same SHA-256, and nothing was deleted", "Owner decision (" + CR + ", " + WHEN + "). Given the source files, when the copy is made, then ALL of: (1) every source file has a copy with an equal SHA-256 (the control recomputes the hashes itself); (2) the CME repository is private (printed); (3) nothing is deleted at the source; (4) a manifest is in the CME folder; (5) nothing that holds a question or an answer is committed to SEN0401."),
 "ST_Exam_Move_Remove": ("AC9_Exam_Move_Remove", "No answer-bearing exam file remains tracked in the public SEN0401 working tree, history is not rewritten, and the guard stays", "Owner decision (" + CR + ", " + WHEN + "). Given the verified copy, when the files are removed, then ALL of: (1) one new commit removes exactly the listed answer-bearing files and each has an equal-hash copy in CME; (2) git ls-files shows no key and no items file with answers; (3) no history rewrite; (4) tools and files without answers stay; (5) the .gitignore guard stays.")}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The exams are moved to the private CME repository"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the exam move to CME costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: one new story with two tasks (about 4 agent-hours); no existing task depends on it, but every later exam artefact is written to the CME location; the open items are re-ranked (G147)."))
    return t + cr + ia, "Change request with impact assessment: the owner's decision to move the exams; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the exam move to CME"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the exam move to CME; nothing is rebuilt here." % OLD.replace("ex:", "")
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
    L.append('ex:SC3_ExamMoveCME a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the exam move to CME story"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamMoveCME; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR52 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the exam move to CME"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: one story with two tasks (exam move to CME) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
