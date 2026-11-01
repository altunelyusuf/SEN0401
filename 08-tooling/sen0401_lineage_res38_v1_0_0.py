#!/usr/bin/env python3
"""sen0401_lineage_res38 v1_0_0 - (copy of res37 for the owner's exam content direction of 2026-11-01 21:09 Istanbul: items v1.3.0 and papers v4) change route (G125 route 2, G133, G147) for the owner's words of 2026-11-01 13:04 Istanbul on the exam: the IKU cover page as page 1, five question formats (4 x 25 points, the 5th 10 points bonus), no memorising items, tips for terms, abbreviations spelled out, 4 pages (else 6). Adds the stories of the cover renderer, items v1.2.0, papers/key/sheet v3, the honesty-check successor and the Ch05 Teach repair task. Usage: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog18"; OLD = "ex:Out3_BacklogR45"; NEWB = "ex:Out3_BacklogR46"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_ExamCases"; IA = "ex:IA3_ExamCases"
WHEN = "Sunday 2026-11-01, on the owner's words of 21:09 Istanbul time relayed by the coordinator"
WORDS = ("THE OWNER'S WORDS (relayed, 2026-11-01 21:09 Istanbul, from his class sessions): three cases to turn into items, used as seeds with original wording and numbers, simple arithmetic without a calculator, no memorisation, a tip whenever a term is used. (1) ORDERING: a chain of successively spent transaction outputs; ask the order of the transactions; a spending transaction always comes after the transaction whose output it spends, traceable back to the coinbase transaction. (2) MINED OR NOT: a set of transactions with spending references; a transaction that receives a spending reference means the referenced transaction was already mined; ask which are mined and which are not (in the same question as 1 or separately). (3) FULL SPENDING: if no change output is added, the unspent difference is the fee and the miner collects it; ask the change amount (or the fee) of a transaction with several inputs and several outputs, with simple numbers. His earlier topic list, also relevant: serverless peer-to-peer; distributed trust; double-spending prevention; independent confirmations; approval without private keys (what a signature proves); telling a genuine from a fake transaction; timing differences in spending; why seed words replaced hand-managed random keys; the borderless nature of Bitcoin. He has not yet chosen between a topic map and his per-topic notes, so more notes may follow and the items task accepts additions. "
         "MAPPING AGAINST ITEMS v1.2.0 (reading the items in full): KEPT: i05 shop confirmations (independent confirmations and double-spending prevention), i23 fill txid and weight (chapter 6, no overlap with the three cases). REWORKED: i02 fee not written becomes case 3 (several inputs and outputs, the change amount or the fee, same four-choice answer block); i07 fill fee rate and set becomes case 2 (mined or not by spending references, and the unspent outputs that form the set, same fill-in answer block). REPLACED: i06 order wallet to block becomes case 1 (order of a spending chain back to the coinbase transaction, same ordering answer block). The other items stay unless the topic list shows a gap, which the executor reports and fills only by replacing, never by adding (the structure stays 25/25/25/25 + 10, one unit per sub-question). Done exam stories and tasks are not edited (G125).")
SPEC = {
 "ST_Exam_Items4": ("The midterm items v1.3.0: three owner cases (spending order, mined or not, full spending) and the owner's topic list", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I59-items4", 2.5, 1.0, "items4", []),
 "ST_Exam_Papers4": ("The midterm papers, key and answer sheet v4 from items v1.3.0, forms A and B", "Del3_ExamPapers", "Obj3_Exam", "SEN0401-I59-papers4", 2.0, 1.5, "papers4", ["TK_Exam_Items4_Build"]),
}
TK = {"ST_Exam_Items4": "Exam_Items4", "ST_Exam_Papers4": "Exam_Papers4"}
BRIEFS = {
 "items4": ("Make the NEW items v1.3.0 of the midterm as new files (items JSON, structure file v1.1.0 only if the numbering or the points change, build script, check script as a new copy of the v1.2.0 check, check log, computed-values log, report). Input: `08-tooling/exam/sen0401_exam_items_midterm_v1_2_0.json` (unchanged), `08-tooling/exam/sen0401_exam_structure_v1_0_0.json` (unchanged), and the owner's input file `08-tooling/exam/sen0401_exam_owner_topics_v1_0_0.json` (the three cases and the nine topics; if newer files of the pattern `sen0401_exam_owner_topics_v*.json` exist, read the newest and say which). " + WORDS + "WHAT TO DO: (1) Keep i05 and i23 as they are (re-run their checks). (2) Rework i02 into case 3: a transaction with several inputs and several outputs and no change output; the student finds the change amount (or the fee) by simple addition and subtraction on round numbers, no calculator; four choices, one correct, the wrong ones from the usual slips (forgetting an input, counting the fee as change); the tip says what a fee is and who collects it. (3) Rework i07 into case 2: five or six transactions with spending references drawn as plain statements (transaction X spends the first output of transaction Y); the student marks which are already mined (every transaction that receives a spending reference) and which may still be waiting; keep the fill-in block type of the position and recompute its computed fields. (4) Replace i06 by case 1: a chain of at least four transactions, each spending an output of the one before and the first spending a coinbase output; the student puts them in order (the Ordering block type of the position); the tip says what a coinbase transaction is. (5) Original wording and numbers; the three cases are seeds, not copies of the owner's examples. No question asks the student to recall a term; every term used carries a tip; every abbreviation is spelled out at first use. (6) Report the TOPIC MAP: for each of the nine topics of the owner, the item key that covers it (kept, reworked or replaced) or the word GAP; fill a GAP only by replacing the weakest-fitting item of the same answer block type and say which; never add a sub-question. (7) Keep the critical points covered (re-run the critical-points tool) and keep seeds and answers consistent. (8) Keep the sub-question positions, answer block types and units of the structure so the answer sheet and the reader need no change; if one cannot be kept, STOP and report. (9) Report every result verbatim. Output NEW files in `08-tooling/exam/`; never edit a committed file. The task accepts additions: the coordinator may add further owner notes as a newer owner-topics file before the session starts; read the newest."),
 "papers4": ("Make the NEW papers, key and answer sheet v4 from items v1.3.0 (the output of TK_Exam_Items4_Build, committed) as new files in `08-tooling/exam/papers_midterm_v4/`: forms A and B as in papers v3 (mixed order, different codes), the cover page, the structure 25/25/25/25 + 10 with one unit per sub-question, the Word paper and key, the PDF answer sheet. Start from the builder and library of papers v3 (copy to v4 names; v3 stays unchanged). The answer sheet and the reader of record stay unchanged while the block types stay unchanged; if the new items need a change, STOP and report. Never shorten an item to fit the pages; report the page count of the paper (6 pages were measured for v3) and why. Run the papers control, the sheet checks as new copies, and the reader measure on 40 synthetic sheets per form: 0 silent wrong and 0 missed. Report every result verbatim."),
}
def bodyof(n): return BRIEFS[n][0]
CRIT = {
 "ST_Exam_Items4": ("AC9_Exam_Items4", "The items v1.3.0 turn the owner's three cases into items and map his topic list, with the same structure", "Owner-directed work (" + CR + ", " + WHEN + "). Given the items v1.2.0 and the structure v1.0.0 (unchanged), when items v1.3.0 are made, then ALL of: (1) every file is new; (2) i05 and i23 are kept and i02, i07 and i06 are reworked or replaced into the three cases with original wording and numbers; (3) the arithmetic of the cases is simple and the answers recompute; (4) no item requires recall of a term, every term has a tip, every abbreviation is spelled out at first use; (5) a topic map of the owner's nine topics is reported with each as item key or GAP; (6) the structure is unchanged (25/25/25/25 + 10, one unit per sub-question, same answer block types); (7) the item checks and the critical-points tool pass on the new file."),
 "ST_Exam_Papers4": ("AC9_Exam_Papers4", "The papers, key and answer sheet v4 carry items v1.3.0 in forms A and B and the reader of record reads the sheet", "Owner-directed work (" + CR + ", " + WHEN + "). Given items v1.3.0 and the papers v3 tools (unchanged), when papers v4, key v4 and sheet v4 are made, then ALL of: (1) every file is new; (2) page 1 is the cover page and the structure is 25/25/25/25 + 10; (3) forms A and B in mixed order with different codes; (4) Word paper and key, PDF sheet; (5) the reader of record reads synthetic sheets of both forms with 0 silent wrong and 0 missed; (6) the papers control passes."),
}
NOTE = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The exam items and papers take the owner\'s three cases and topic list from his class sessions"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso ex:CR3_MidtermSimplify ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, lit(WORDS))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the exam cases of the owner cost and touch"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(WORDS + " AFFECTED: two new stories with four tasks (about 7 agent-hours); the Done exam stories are not reopened (G125); the reader and the sheet stay unchanged while the block types stay."))
    return t + cr + ia, "Change request with impact assessment: the owner's 21:09 exam cases (spending order, mined or not, full spending, topic list); no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds stories, tasks and criteria, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the exam cases of 21:09"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the owner's 21:09 exam cases; nothing is rebuilt here." % OLD.replace("ex:", "")
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
    L.append('ex:SC3_ExamCases a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the items v1.3.0 and papers v4 stories"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in SPEC), lit(WORDS)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ExamCases; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR45 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the exam cases of 21:09"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: two stories with four tasks (items v1.3.0, papers v4) (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
