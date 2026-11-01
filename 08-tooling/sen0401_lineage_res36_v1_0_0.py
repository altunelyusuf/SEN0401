#!/usr/bin/env python3
"""sen0401_lineage_res36 v1_0_0 - change route (G125 route 2, G133, G147) for the owner's words of 2026-11-01 13:04 Istanbul on the exam: the IKU cover page as page 1, five question formats (4 x 25 points, the 5th 10 points bonus), no memorising items, tips for terms, abbreviations spelled out, 4 pages (else 6). Adds the stories of the cover renderer, items v1.2.0, papers/key/sheet v3, the honesty-check successor and the Ch05 Teach repair task. Usage: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog16"; OLD = "ex:Out3_BacklogR43"; NEWB = "ex:Out3_BacklogR44"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamNewRules"; IA = "ex:IA3_ExamNewRules"
WHEN = "Sunday 2026-11-01, on the owner's words of 13:04 Istanbul time relayed by the coordinator"
BD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "briefs", "iter57")
def bodyof(n):
    t_ = open(os.path.join(BD, "BRIEF_%s.md" % n), encoding="utf-8").read(); return t_[t_.index("## The task") + len("## The task"):].strip()
WORDS = ("THE OWNER'S WORDS (relayed, 2026-11-01 13:04): 'Use the attached page and fill the generic parts appropriately for each of the exams. Categorize the exam into 5 question format with possible number of sub-questions. If possible 4 questions 25 points and 5th Question is 10 points and bonus. If you can fit overall exam in 4 pages it is fine, otherwise, fit with 6 pages but better formatting and readability. The abbreviations should be used in full form in their first usage. Never ask memorizing questions and dont force the students to remember a specific terminology. You should support the students with provide tips to remember, if you use a specific term in the exam. What SegWit scripts, P2PKH, ... are is not important, their usage and the importance for the Bitcoin the reason they exist is more important.' The attached page is the cover page of another IKU course (copy: /home/claude/exam_cover_template/IKU_exam_cover_page_template_source.docx). "
          "AUDIT (heuristic, by names only, 23 items of items v1.1.0): terms or abbreviations without expansion or tip appear in at least items i12, i14, i15, i19, i20; the full audit is the first element of the items task. HOW THE PAPER STORIES ARE REOPENED: ST_Repair_Exam_Paper and ST_Repair_Exam_Reader stay Done and are not edited (G125); the new stories make NEW items (v1.2.0), a cover renderer, papers, key and sheet v3 as new files; the reader is unchanged while the sheet's block types are unchanged. This supersedes the earlier target of 3 paper pages plus 1 sheet page, and the wait for the owner's question styles.")
SPEC = {  # sid: (title, deliv, obj, tasks(build, verify), session, hrs build, hrs verify, brief, deps of build)
 "ST_Exam_Cover": ("The exam cover page: the IKU template page filled for SEN0401 and SEN0414 by a renderer", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I57-cover", 3.0, 1.0, "SEN0401-I57-cover", []),
 "ST_Exam_Items3": ("The midterm items v1.2.0: understanding, tips, abbreviations spelled out, five question formats", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I57-items", 6.0, 1.5, "SEN0401-I57-items", []),
 "ST_Exam_Papers3": ("The midterm papers, key and answer sheet v3: cover page, five questions, four pages or else six", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I57-papers", 6.0, 2.0, "SEN0401-I57-papers", ["TK_Exam_Cover_Build", "TK_Exam_Items3_Build"]),
 "ST_Code_Honesty": ("The honesty check and its fixtures read prompt-free decks: successor files", "Del3_ChapterCode", "Obj3_ChapterCode", "SEN0401-I57-honesty", 3.0, 1.0, "SEN0401-I57-honesty", []),
}
TK = {"ST_Exam_Cover": "Exam_Cover", "ST_Exam_Items3": "Exam_Items3", "ST_Exam_Papers3": "Exam_Papers3", "ST_Code_Honesty": "Code_Honesty"}
CRIT = {
 "ST_Exam_Cover": ("AC9_Exam_Cover", "A renderer fills the IKU cover page for our exams and the page renders as one page", "Owner-directed work (" + CR + ", " + WHEN + "). Given the cover template of the owner, when the NEW renderer and its demo are made, then ALL of: (1) every file is new; (2) the demo cover is exactly one page on the LibreOffice render with every table inside the margins; (3) it carries the course, Midterm Exam, Academic Year 2026-2027, Fall, 60 minutes, the instructor, a marked date and time fill-in, the question table Q1 to Q4 of 25 and Q5 of 10 bonus, our own outcome rows and the cheating warning; (4) every abbreviation is spelled out at first use."),
 "ST_Exam_Items3": ("AC9_Exam_Items3", "The items v1.2.0 ask about use, importance and reason, never recall, with tips and spelled-out abbreviations, in five question formats", "Owner-directed work (" + CR + ", " + WHEN + "). Given the 23 items v1.1.0 (unchanged), when items v1.2.0 and the structure are made, then ALL of: (1) every file is new; (2) a full audit table of the 23 items is reported with counts by chapter; (3) no item requires recalling a term, every term carries a tip, every abbreviation is spelled out at first use; (4) the critical points of the chapters stay covered; (5) the structure has 4 questions of 25 points and a 5th of 10 points (bonus), each with sub-questions; (6) the existing item checks pass on the new file."),
 "ST_Exam_Papers3": ("AC9_Exam_Papers3", "The papers, key and answer sheet v3 carry the cover page and five questions in four pages or else six, and the reader of record reads the sheet", "Owner-directed work (" + CR + ", " + WHEN + "). Given the cover renderer and items v1.2.0, when papers v3, key v3 and sheet v3 are made, then ALL of: (1) every file is new; (2) page 1 is the cover page; (3) the paper is 4 pages in all or else 6, the choice reported; (4) Word paper and key, PDF sheet; (5) the reader of record reads synthetic sheets of both forms with 0 silent wrong and 0 missed; (6) the papers control passes."),
 "ST_Code_Honesty": ("AC9_Code_Honesty", "The honesty check and the fixtures successor refuse a stale caption on prompt-free decks and equal the old check on old decks", "Owner-directed work (" + CR + ", the owner's earlier answer 'New check beside the old', 2026-11-01). Given the committed honesty check v1_0_0 and fixtures (unchanged), when the successor files are made, then ALL of: (1) every file is new; (2) the stale_caption fixture is refused by the successor; (3) the successor equals the old check on a deck with prompts; (4) the report explains why Chapter 6 does not meet the problem."),
}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
CH5 = "TK_Repair_Ch05_DeckTeach_Build"
CH5TXT = ("REPAIR of the chapter 5 Teach deck v3_6_0 (commit 880a966): my control found 54 occurrences of __import__(\"sys\").version_info[:2] in code boxes and result shapes, which the Friday chapter 6 deck v2_3_0 does not have; the label 'What the run printed (python 3.14.6)' already states the version. Make the NEW deck v3_7_0 (v3_6_0 never edited, SHA-256 before and after): remove those stamp lines and their result rows, change nothing else, rebuild the notes and charts unchanged, then run the code, indent, lambda, label-word, prompt and layout checks and the deck standard, and report each as printed. Reported by the coordinator as sent to the deck05 executor with work begun about 2026-11-01T10:13:00Z (reported, not witnessed by the register; disclosed). Planned session SEN0401-I52-deck05.")
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The exams get the IKU cover page, five question formats, no memorising items, tips and spelled-out abbreviations, in four pages or else six"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the new exam rules cost and touch"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: four new stories (cover, items, papers, honesty successor) with eight tasks, one repair task of the chapter 5 Teach deck, an estimate of about 20 agent-hours; the Done exam stories are not reopened in place. The Paper control and the reader stay as recorded."))
    return t + cr + ia, "Change request with impact assessment: the owner's 13:04 exam rules (IKU cover page, five question formats, no memorising, tips, abbreviations, 4 pages or else 6); no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the exam rules of 13:04 and the honesty successor"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the owner's 13:04 exam rules; nothing is rebuilt here." % OLD.replace("ex:", "")
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
        L.append(RT.ac_block(aid, label, g_, 'ex:TS_ChapterCheck, ex:TS_DeckMatch', "the checks of the task, run again by the lineage agent; papers control; LibreOffice render; reader on the sheet PDF", k).replace("ex:TC9_", "ex:TC9X_"))
        L.append(RT.case_blocks(k, aid).replace("Spec3I_Retro24", "Spec3I_Ch06Teach").replace("ex:Data3S_TC9_", "ex:Data3S_TC9X_").replace("ex:TC9_", "ex:TC9X_")
            .replace("Run the checks on the item as measured in the baseline of 2026-10-25 (an overlap, a manifest example that starts with an error name, a story whose text lies below the first screen, a committed file with status M) and require that nothing is claimed for it.", "Run the checks on the item as it stands before the work and require that nothing is claimed for it.")
            .replace("The finding as measured in the baseline of 2026-10-25 (ex:IA3_Retro24).", "The finding as measured on 2026-11-01 (" + IA + ")."))
        tb, tv = "TK_%s_Build" % TK[sid], "TK_%s_Verify" % TK[sid]; mem += [sid, tb, tv]
        L.append(R.story_block(sid, title_, deliv, obj, [aid], [tb, tv], NOTE, "ex:" + ITER, "Proposed"))
        note_b = bodyof(brief) + " REUSE: use the existing tools and files named in the task and never edit a committed file. ONE EXECUTOR SESSION: " + sess + "."
        L.append(R.task_block(tb, "Build: " + title_, "Build", deps, sess, "S", hb, note_b, "ex:" + ITER, "Proposed", True))
        L.append(R.task_block(tv, "Verify: " + title_, "Verify", [tb], "builder", "S+%.1fh" % hb, hv, "Run the checks of the criterion again myself, with my own control scripts and the existing tools, on the new files; open every produced file; read the report of the executor against the files; register Done only on files I have re-run.", "ex:" + ITER, "Proposed", True))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
        L.append("ex:Obj3_%s backlog:metricMovableBy ex:%s .\n" % ("Exam" if obj.endswith("Exam") else "ChapterCode", sid))
    # Ch05 repair task
    L.append(R.task_block(CH5, "Repair: the chapter 5 Teach deck v3_7_0 without the version probe", "Build", [], "SEN0401-I52-deck05", "S", 1.0, CH5TXT, "ex:" + ITER, "Proposed", True))
    mem.append(CH5)
    i, j = T.blk(t, "ST_Ch05_DeckTeach"); b = t[i:j]; m = re.search(r"backlog:decomposesInto ([^;]*?) ;", b); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:decomposesInto " + m.group(1).rstrip() + ", ex:" + CH5 + " ;", 1) + t[j:]
    t = setdeps(t, "TK_Ch05_DeckTeach_Verify", [CH5])
    i, j = T.blk(t, ITER); b = t[i:j]; m = re.search(r"backlog:hasMember ([^;.]*?)( ;| \.|\.\n)", b, re.S); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:hasMember " + m.group(1).rstrip() + ", " + ", ".join("ex:" + x for x in mem) + m.group(2), 1) + t[j:]
    L.append('ex:SC3_ExamNewRules a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the cover, items, papers and honesty-successor stories and the Chapter 5 Teach repair"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamNewRules; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR44 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the exam rules of 13:04 and the honesty successor"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: four stories with eight tasks (exam cover, items v1.2.0, papers v3, honesty successor) and the Chapter 5 Teach repair task (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
