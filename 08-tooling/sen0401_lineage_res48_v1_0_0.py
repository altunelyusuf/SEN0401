#!/usr/bin/env python3
"""sen0401_lineage_res48 v1_0_0 - (the exam move follow-up, copy of res47) (was: copy of res38 for the repair of the chapter 3 page v9_74_0: a defect found by the lineage agent in the quiet window of 2026-11-01) change route (G125 route 2, G133, G147) for the owner's words of 2026-11-01 13:04 Istanbul on the exam: the IKU cover page as page 1, five question formats (4 x 25 points, the 5th 10 points bonus), no memorising items, tips for terms, abbreviations spelled out, 4 pages (else 6). Adds the stories of the cover renderer, items v1.2.0, papers/key/sheet v3, the honesty-check successor and the Ch05 Teach repair task. Usage: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog25"; OLD = "ex:Out3_BacklogR52"; NEWB = "ex:Out3_BacklogR53"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamMoveFollow"; IA = "ex:IA3_ExamMoveFollow"
WHEN = "Monday 2026-11-02, on the lineage agent's control of the removal, with the coordinator's ruling of 2026-11-02"
WORDS = ("FINDING (lineage agent, 2026-11-02, control of the removal commit cd9706c, which passed my own check: 41 files deleted, each with an equal-hash copy in CME): the owner's order is 'move the exams to the private CME repository' (10:27). Answer-bearing files still tracked in the PUBLIC SEN0401 tree: the rebuilt first-form papers in 08-tooling/verify/iter54/ctl/papers_rebuilt/ (chapter and type papers, their keys as json and pdf, paper.ttl, measure and layout files; CME has no copy at that path), and possibly bridge and check logs under 08-tooling/verify/ and 08-tooling/exam/ that print answer values (not yet inspected; the generic words answer or expected in 61 candidate logs are not proof). Also tracked control scripts of the lineage read paths that were removed (for example papers_midterm_v1/..., items_midterm v1_0_0 to v1_3_0, the rebuilt papers): they fail until they read the copies in CME (the private CME clone at /home/claude/CME/exams/SEN0401/). Committed history stays; a history rewrite is not decided and not ordered. ")
SPEC = {"ST_Exam_Move_Followup": ("The remaining answer-bearing tracked files are copied to CME with equal hashes and removed from the public tree", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I70-examfollow", 1.0, 0.5, "examfollow", []),
 "ST_Exam_Move_Repoint": ("The control scripts that read the removed exam paths are repointed to the CME copies as new versioned files", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I71-exampoint", 1.5, 0.5, "exampoint", [])}
TK = {"ST_Exam_Move_Followup": "Exam_Move_Followup", "ST_Exam_Move_Repoint": "Exam_Move_Repoint"}
BRIEFS = {"examfollow": WORDS + "ITEM (stated first): INSPECT FIRST, THEN COPY, THEN REMOVE. WHAT TO DO: (1) List the tracked files under 08-tooling/verify/ and 08-tooling/exam/ whose names or contents belong to the exam (papers, keys, items, check and bridge logs of exam checks, topic maps, reports); for every file decide by reading it whether it prints an answer value, a key, an option text, or a question or paper text; print the table (file, decision, the first matching line with the answer part cut to its first 12 characters). Files that print only counts, names or PASS and FAIL lines stay. The 4 key files and the rebuilt first-form papers in 08-tooling/verify/iter54/ctl/papers_rebuilt/ are in. (2) Copy every file you decided to remove into /home/claude/CME/exams/SEN0401/ at the same relative path, print the SHA-256 of source and copy side by side, require equal, commit in CME yourself (git pull --rebase --autostash first). (3) Only then remove exactly those files from the SEN0401 working tree in ONE new commit with git rm (message names the owner's decision of 2026-11-02 10:27; history stays; no force push; the guard stays; extend the guard by a new line only if a path is not covered). (4) Print git ls-files for the checked folders afterwards. Report the commit ids and all counts as printed.",
 "exampoint": WORDS + "ITEM (stated first): NEW VERSIONED FILES ONLY. WHAT TO DO: find, with grep over the tracked scripts of 08-tooling/ (python and shell), every control, check or build script that opens a path that cd9706c removed (list: git diff --name-status cd9706c^ cd9706c) or that will be removed by the follow-up commit of the story ST_Exam_Move_Followup; print the table (script, the removed path it reads, how it reads it). For each such script that is still needed by the lineage, write a NEW file with the next version number whose only change is that the exam paths are read from the CME clone (/home/claude/CME/exams/SEN0401/<same relative path>) and, if the CME clone is missing, it prints NOT_RUN and exits non-zero (a gate that cannot run is not a pass); never edit a committed file; no gate, bound or rule is weakened; the new script must not hold a question or an answer. Prove each new script by running it: the result must equal the result it gave before the removal (compare with its last committed log, line by line, and print differences). Scripts that cannot be proved are listed as NOT_RUN with the reason. Commit your new files by path under flock /tmp/sen0401_git.lock; report the commit ids and every result as printed."}
def bodyof(n): b = BRIEFS[n]; return b if isinstance(b, str) else b[0]
CRIT = {"ST_Exam_Move_Followup": ("AC9_Exam_Move_Followup", "No answer-bearing exam file remains tracked in the public SEN0401 tree outside the removed 41, each removed file has an equal-hash copy in CME, history is not rewritten", "Owner decision (" + CR + ", " + WHEN + "). Given the findings, when the follow-up is done, then ALL of: (1) every tracked exam file was inspected and the decision is printed; (2) every file removed has an equal-hash copy in CME (the control recomputes); (3) one new commit removes exactly the decided files; (4) the 4 keys and the rebuilt papers of verify/iter54/ctl/papers_rebuilt are no longer tracked; (5) no history rewrite and the guard stays."),
 "ST_Exam_Move_Repoint": ("AC9_Exam_Move_Repoint", "Each control script that read a removed exam path has a new versioned copy that reads the CME copy, is proven by running, and no gate is weakened", "Owner decision (" + CR + ", " + WHEN + "). Given the removal, when the scripts are repointed, then ALL of: (1) the table of scripts that read removed paths is printed; (2) every new script is a new file and no committed script is edited; (3) each runs against the CME copies and gives the lines it gave before, or is listed NOT_RUN with the reason; (4) a missing CME clone gives NOT_RUN and a non-zero exit; (5) no question and no answer is in the new files.")}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The exam move to CME is completed and the scripts are repointed"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the exam move follow-up costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: one new story with two tasks (about 4 agent-hours); no existing task depends on it, but every later exam artefact is written to the CME location; the open items are re-ranked (G147)."))
    return t + cr + ia, "Change request with impact assessment: the remaining answer-bearing files and the scripts that read removed paths; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the exam move follow-up"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the exam move follow-up; nothing is rebuilt here." % OLD.replace("ex:", "")
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
    L.append('ex:SC3_ExamMoveFollow a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the exam move follow-up story"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamMoveFollow; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR53 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the exam move follow-up"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: one story with two tasks (exam move follow-up) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
