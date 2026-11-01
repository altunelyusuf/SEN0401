#!/usr/bin/env python3
"""sen0401_lineage_res34 v1_0_0 - change route (G125 route 2, G133, G147) for the owner's pacing answer of 2026-11-01 12:2x Istanbul ('Today we should finish both the Midterms and midterm scope work'): the dependencies of the not-started midterm-scope tasks are restructured so that independent work starts at once. A dependency on a Verify task was an ORDERING of the lineage agent (control before the next step); the REAL dependency is on the produced files, i.e. on the Build task. The Verify tasks keep the control and gate the Done state. Events: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog14"; OLD = "ex:Out3_BacklogR41"; NEWB = "ex:Out3_BacklogR42"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_MidtermToday"; IA = "ex:IA3_MidtermToday"
WHEN = "Sunday 2026-11-01, on the owner's words of 12:13 Istanbul time relayed by the coordinator"
WORDS = ("THE OWNER'S WORDS (relayed, 2026-11-01 12:13): 'Do you think the files you provided are ready to share? The source codes in the slides should match with the interactive page of that chapter's Chapter Examples in the Lab. You need to bring the files to the quality level of the files we have generated in our last Friday work and adapt all Midterm scope to this level before sharing them.' The coordinator's answer to him: NO. Midterm scope: SEN0401 chapters 1 to 6, to the chapter 6 Friday standard: prompt-free code, no untaught lambda, indented code, slides that teach alone, 5N1K as storytelling, the code on the slides equal to the page's Chapter Examples in slide order, on the page zoom, full screen and a resizable panel for every diagram, a Lecture tab matching the deck, a clean layout. The exam executors already running (reader, paper) continue.")
FG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0401_midterm_fitgap_2026_11_01.json")))
def fg_text():
    L = ["AS-IS FIT-GAP, MEASURED 2026-11-01 by the lineage agent on the newest deck and page of each chapter (prompts = '>>>' and '...' lines in slide text; deck layout check v1_0_0; page 'chaptercode' examples against the code-font slides in order, prompts ignored; Lecture tab = number of slides listed; 'full' = occurrences of fullscreen in the page):"]
    for c in sorted(FG):
        d = FG[c]; L.append("Ch%s: deck %s (%s slides), prompt lines %s, lambdas on slides %s, label-word shapes %s, notes average %s words; layout check %s; page %s: examples %s of %s code slides matched in order; examples with a lambda %s; Lecture tab %s of %s slides; full screen %s." % (c, d["deck"], d["slides"], d["prompts"], d["lambda"], d["labels"], d["notes_avg"], d["layout"], d["page"], d["match"], d["codeslides"], d["page_lambda"], d["lecture"], d["slides"], d["fullscreen"]))
    L.append("FIT: the notes of every deck pass the notes check; the Lecture tab of chapters 1 to 5 equals the deck; the examples of chapters 1 to 5 are the slide code without prompts (15, 14, 19, 21 and 27 examples, all matched). GAP: prompts and lambdas on the slides of chapters 1 to 5 (so the slide code is not the page's Chapter Examples text); chapter 1 has label-word shapes; the notes are short but say little (the standard asks for clues); no page of chapters 1 to 5 offers full screen; chapter 6: the page is built from an older deck (18 examples and a Lecture tab of 62 slides against a deck of 71 slides and 20 code slides: only 2 examples match in order) and the deck has 49 layout items to look at.")
    return " ".join(L)
FACT = WORDS + " " + fg_text()
EFF = {1: (8.5, "SEN0401-I55-deckteach-ch01"), 2: (5.0, "SEN0401-I55-deckteach-ch02"), 3: (6.0, "SEN0401-I55-deckteach-ch03"), 4: (6.5, "SEN0401-I55-deckteach-ch04"), 5: (9.5, "SEN0401-I55-deckteach-ch05")}
NAME = {1: "Introduction", 2: "How Bitcoin Works", 3: "Bitcoin Core", 4: "Keys and Addresses", 5: "Wallet Recovery"}
DECK = {1: ("SEN0401_Ch01_Introduction_3e", "v3_2_0"), 2: ("SEN0401_Ch02_HowBitcoinWorks_3e", "v3_0_0"), 3: ("SEN0401_Ch03_BitcoinCore_3e", "v3_0_0"), 4: ("SEN0401_Ch04_KeysAndAddresses_3e", "v3_4_0"), 5: ("SEN0401_Ch05_WalletRecovery_3e", "v3_4_0")}
def title(c): return "The chapter %d deck: every concept understandable from the slides, human storytelling, results as visuals, notes that carry the clues, layout clean" % c
def txt_build(c):
    f = FG[str(c)]
    return ("Make the NEW chapter %d deck (03-materials/ch0%d) as the version AFTER the deck of the story ST_Ch0%d_DeckCode (the code-only deck; never edited, SHA-256 before and after) so that a reader who has only the slides and the notes understands each concept of the chapter, to the standard of the chapter 6 Friday deck (read its builder and its checks first). The deck's code, its shape names and its results do not change (the code checks must still PASS). MEASURED today on %s: %s slides, label-word shapes %s, notes averaging %s words (maximum %s), layout check %s. THE WORK: (1) for every concept of the chapter (the list from the page's concept nodes and the ontology of the chapter, one entry each in your log) the slides say what it is, why it exists, how it works and show it with a picture, diagram, table or small simulation made as native objects (charts are native PowerPoint chart objects, never pictures of charts), the way the page does with its visualisations; (2) human storytelling instead of labels: no text shape begins with WHAT/WHO/WHEN/WHERE/WHY/HOW and a colon or dash; the who, what, when, where, why and how of each story are told as sentences with real names, dates and places, a REAL picture or a free-source picture, and a live source link on the slide; (3) each example's executed result is a visualisation beside or under the code with a one-line reading; no '>>>' prompt, no lambda that the chapter has not taught, code indented; (4) the notes stay SHORT (a few sentences) but carry the clues: what to say, what to point at, the question to ask, the common mistake; (5) slides numbered, one light colouring (the closing slide may be dark as the deck standard allows), a resources slide with links, no long paragraphs, the layout check CLEAN (0 items to look at). PROOF kept as logs: SHA-256 before and after; a table concept by concept (slides, visual, page visualisation); the label-word, lambda, indent and prompt checks, the deck standard, arc, overlap, layout, notes and deck checks all PASS; the hyperlink count not fewer; renders of ten changed slides kept as pictures; a reading by the three roles of the owner's rule (teaching academician, expert reviewer, undergraduate student) as a short table; nochange. DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES. A committed file is never edited: every output is a new file with a new version number. STOP and report if a gate, a test or a threshold would have to change. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN). The machine has 2 cores and little disk (about 1 GB free, stop at 0.9): one build or browser run at a time (browser runs only under flock /tmp/page_test.lock), remove only your own temporary folders. Commit ONLY your own files to main (git add by path, pull --rebase before push). Planned session %s; about %.1f hours (an estimate, G120: the real start is recorded at work begun)." % (c, c, c, f["deck"], f["slides"], f["labels"], f["notes_avg"], f["notes_max"], f["layout"], EFF[c][1], EFF[c][0]))
def txt_verify(c): return "Compare the SHA-256 of the earlier deck; read the concept table and spot-check six concepts against the slides; run the prompt, lambda, indent and label-word checks and the deck standard, arc, overlap, layout, notes and deck checks myself; count the hyperlinks; render ten slides and read ten notes; read the code of five slides against the page's Chapter Examples; nochange."
def crit(c):
    return ("AC9_Ch0%d_DeckTeach" % c, "The chapter %d deck is a new file in which every concept is understandable from the slides and the notes, with no label words, no prompts and a clean layout" % c,
            "Owner-directed work (" + CR + ", " + WHEN + "). Given the chapter %d deck of the story ST_Ch0%d_DeckCode (unchanged) when the NEW deck is made, then ALL of: (1) the earlier deck is byte-identical; (2) the code, shape names and results are unchanged and the code checks PASS; (3) the label-word, lambda, indent and prompt checks find 0; (4) a concept table lists every concept of the chapter with its slides, its visual and the page visualisation it matches, none missing; (5) each example's result is a visual with a one-line reading; (6) the notes are short (none over 80 words) and carry clues on every slide; (7) the layout check reports 0 items to look at and the deck standard, arc, overlap, notes and deck checks PASS; (8) the stories are told as sentences with real names, a real picture and a live link. Results as printed; if any element fails the work is named failing. " % (c, c) + FACT)
def sub_attr(b, pred, val):
    pat = re.compile(r'(%s )"(?:[^"\\]|\\.)*"(@en)?' % re.escape(pred)); m = pat.search(b); assert m, pred
    return b[:m.start()] + m.group(1) + lit(val) + (m.group(2) or "") + b[m.end():]
PACE = ("THE OWNER'S WORDS (relayed, 2026-11-01 12:2x Istanbul): 'Today we should finish both the Midterms and midterm scope work.' The target is today for the exams and chapters 1 to 6 at the Friday standard. The lineage agent cannot prove that about 136 agent hours fit in a day (the estimates are in ex:CR3_MidtermQuality); the work is therefore restructured for the most safe parallelism. REAL VS ORDERING: (1) the deck builds of chapters 1 to 6 need only the marker convention stated in the code-gate task (code boxes and result lines named by prefix), not the finished checks: the dependency on the code gate and the deck checks is moved from the Build to the Verify; (2) the Teach build of a chapter continues the deck of its DeckCode build in the same executor session (the same file lineage), so it depends on the DeckCode Build, not on its Verify; (3) the page of a chapter needs the final deck file and the panels template file, not their controls: it depends on the Teach Build and the Panels Build; (4) the page template 9.52.6 does not need the gate; the panels template 9.52.7 really extends 9.52.6 (a real dependency, on the Build). A Verify task is still required for every Done: if the control finds a defect after a dependent was built on the file, the defect is repaired as a new version and the dependent is rebuilt; that risk is accepted and named here.")
DEPS = {}
for c in range(1, 7):
    DEPS["TK_Ch0%d_DeckCode_Build" % c] = []
    DEPS["TK_Ch0%d_DeckCode_Verify" % c] = ["TK_Ch0%d_DeckCode_Build" % c, "TK_Code_Gate_Verify"] + (["TK_Deck_Checks_Verify"] if c == 6 else [])
    DEPS["TK_Ch0%d_DeckTeach_Build" % c] = ["TK_Ch0%d_DeckCode_Build" % c]
    DEPS["TK_Ch0%d_DeckTeach_Verify" % c] = ["TK_Ch0%d_DeckTeach_Build" % c, "TK_Deck_Checks_Verify"]
    DEPS["TK_Ch0%d_PageCode_Build" % c] = ["TK_Ch0%d_DeckTeach_Build" % c, "TK_Template_Panels_Build"]
DEPS["TK_Code_Template_Build"] = []
DEPS["TK_Template_Panels_Build"] = ["TK_Code_Template_Build"]
DEPS["TK_Repair_Ch06_Lecture_Build"] = ["TK_Repair_Ch06_DeckLayout_Verify", "TK_Ch06_DeckTeach_Build"]
SESS_SAME = {"TK_Ch0%d_DeckTeach_Build" % c: "SEN0401-I52-deck0%d" % c for c in range(1, 7)}
SESS_SAME["TK_Template_Panels_Build"] = "SEN0401-I52-template"
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The midterm scope is restructured to start at once: dependencies on controls become dependencies on built files"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso %s, ex:CR3_MidtermQuality ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, IA, lit("Raised " + WHEN + ". " + PACE))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the restructure costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(PACE + " AFFECTED: the dependencies of %d not-started tasks and the planned session of the Teach and panels Build tasks (set to the session of the build they continue). NOT AFFECTED: every criterion, every committed file, the exam stories that run. RISK: a defect found by a Verify after a dependent was built is repaired as a new version and the dependent rebuilt." % len(DEPS)))
    return t + cr + ia, "Change request with impact assessment: the dependencies of the not-started midterm-scope tasks move from the controls to the built files so that independent work starts at once (the owner's wish to finish the midterm scope today); no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") changes the dependencies of not-started tasks, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: midterm-scope dependencies on built files"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the owner's pacing answer on the midterm scope; nothing is rebuilt here." % OLD.replace("ex:", "")
def setdeps(t, tid, deps):
    i, j = T.blk(t, tid); b = t[i:j]
    b = re.sub(r"\n?[ \t]*backlog:dependsOn [^;]*;", "", b, count=1)
    if deps:
        m = re.search(r"backlog:hasState backlog:\w+ ;", b); assert m, tid
        b = b[:m.end()] + "\n    backlog:dependsOn " + ", ".join("ex:" + d for d in deps) + " ;" + b[m.end():]
    return t[:i] + b + t[j:]
def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEWB)
    for tid, deps in DEPS.items():
        i, j = T.blk(t, tid); assert "backlog:Proposed" in t[i:j] or "backlog:Ready" in t[i:j], tid
        t = setdeps(t, tid, deps)
    for tid, sess in SESS_SAME.items():
        i, j = T.blk(t, tid); b = t[i:j]; b2, k = re.subn(r"Planned session SEN0401-[A-Za-z0-9-]+", "Planned session " + sess, b); assert k == 1, tid
        t = t[:i] + b2 + t[j:]
    L = ['ex:SC3_MidtermToday a backlog:ScopeChange ;\n    rdfs:label "Dependencies of the midterm-scope tasks moved from the controls to the built files"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem ex:ST_Ch06_DeckCode ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, lit(PACE))]
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_MidtermToday; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR42 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt with the midterm-scope dependencies on built files"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: the dependencies of %d midterm-scope tasks moved from controls to built files (change request Accepted); %d items re-admitted." % (len(DEPS), n)
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
