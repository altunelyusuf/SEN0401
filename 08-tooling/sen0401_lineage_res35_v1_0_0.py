#!/usr/bin/env python3
"""sen0401_lineage_res35 v1_0_0 - change route (G125 route 2, G133, G147) for the owner's words of 2026-11-01 12:26 Istanbul: 'Simplify the tasks of the agents to concentrate on the issues we have solved on friday, and pass the useless effort spent to remeasure the allready succeeded parts.' The not-started midterm-scope tasks are rewritten: the Friday tools and templates are reused (template 9.52.9, builder 4.19.0, the chapter 6 deck builders), the existing gates are run once at the end of a chapter and what passed on unchanged bytes is not re-run (a cache, not a weakened gate), one session per chapter does the deck and page tasks in order, and the estimates are lowered. The two template stories are cancelled afterwards by a separate version (res36). Events: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog15"; OLD = "ex:Out3_BacklogR42"; NEWB = "ex:Out3_BacklogR43"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_MidtermSimplify"; IA = "ex:IA3_MidtermSimplify"
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
PACE = ("THE OWNER'S WORDS (relayed, 2026-11-01 12:26 Istanbul): 'Simplify the tasks of the agents to concentrate on the issues we have solved on friday, and pass the useless effort spent to remeasure the allready succeeded parts.' The coordinator's reading: the work per chapter is exactly the Friday fixes (no '>>>' prompts, no untaught lambdas, indented code, slides that teach alone, 5N1K as storytelling, the slide code equal to the page's Chapter Examples in slide order, on the page full screen, a resizable panel and the Lecture tab), reusing the chapter 6 tools and templates; what passed is not measured again; the existing gates run ONCE at the end of a chapter; the foundation stories are dropped or merged unless reuse is impossible; one brief per chapter (deck and page together). THE FACTS (read by the lineage agent in the repository, 2026-11-01): the page template 9.52.9 (full screen and reader-set size for every diagram panel, slide examples first in the Playground, no prompt in the card), the page builder 4.19.0 and the panel test v1_0_0 were made on Friday and passed on the chapter 6 page v9.89.0 (page tests 9.34.3, 9.35.3, 9.38.0 PASS); so the stories ST_Code_Template (page template 9.52.6) and ST_Template_Panels (9.52.7) are satisfied by files that already exist and are CANCELLED by the next version with the fit-gap and a closure report, not rebuilt. The code gate and the four deck checks (indentation, lambda, label words, prompts) are NOT available as tools for chapters 1 to 5 (the committed deck checks find code by the prompts), so they stay, merged into one small session of 3 hours each. The chapter 6 deck v2_3_0 already has no prompts and no lambdas, so its DeckCode task is only a verification of 0.5 hours. NOT WEAKENED: every gate and every criterion stays; a gate that passed on unchanged bytes is not re-run (the cache of the method, R9), and each chapter's existing gates run once at its end (the PageMeasure task, about 1 hour). RISK named: the agents reuse the Friday builders; if a builder does not fit a chapter the executor stops and reports.")
HRS = {"TK_Code_Gate_Build": 3.0, "TK_Deck_Checks_Build": 3.0}
for c, (dc, th, pg) in {1: (2.5, 5.0, 2.0), 2: (2.5, 3.0, 2.0), 3: (3.0, 3.5, 2.0), 4: (3.0, 4.0, 2.0), 5: (5.0, 6.0, 3.0), 6: (0.5, 6.0, 2.0)}.items():
    HRS["TK_Ch0%d_DeckCode_Build" % c] = dc; HRS["TK_Ch0%d_DeckTeach_Build" % c] = th; HRS["TK_Ch0%d_PageCode_Build" % c] = pg; HRS["TK_Ch0%d_PageMeasure_Build" % c] = 1.0
HRS["TK_Repair_Ch06_Lecture_Build"] = 0.5
REUSE = " REUSE AND NO RE-MEASURING (owner 2026-11-01 12:26, ex:CR3_MidtermSimplify): apply the Friday fixes with the Friday tools: the page template 9.52.9, the page builder 4.19.0 and the panel test (08-tooling), the chapter 6 deck builders in 08-tooling/ch06-deck (deck_lib, deck_enhance, deck_notes, deck_concepts, deck_derive) and the chapter 6 page steps in 08-tooling/ch06-page, as the starting point; do not rebuild them. Do not measure again what passed on unchanged bytes; run the existing gates ONCE at the end of the chapter. If a Friday tool does not fit your chapter, STOP and report why."
DEPS = {"TK_Code_Template_Build": [], "TK_Template_Panels_Build": []}
for c in range(1, 7):
    DEPS["TK_Ch0%d_PageCode_Build" % c] = ["TK_Ch0%d_DeckTeach_Build" % c]
SESS = {"TK_Deck_Checks_Build": "SEN0401-I52-codegate", "TK_Repair_Ch06_Lecture_Build": "SEN0401-I52-deck06", "TK_Repair_Ch06_DeckLayout_Build": "SEN0401-I52-deck06"}
for c in range(1, 7):
    for k in ("DeckTeach", "PageCode", "PageMeasure"):
        SESS["TK_Ch0%d_%s_Build" % (c, k)] = "SEN0401-I52-deck0%d" % c
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The midterm-scope tasks are simplified to the Friday fixes: reuse, no re-measuring, one session per chapter"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso %s, ex:CR3_MidtermQuality, ex:CR3_MidtermToday ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, IA, lit("Raised " + WHEN + ". " + PACE))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the simplification costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(PACE + " AFFECTED: the text, estimate and session of %d not-started Build tasks and the dependencies of the page tasks; the two template stories are cancelled by the next version. ESTIMATE (G120), agent hours: code gate 3 and deck checks 3 (one session); chapter 1 = 2.5 + 5 + 2 + 1 = 10.5; chapter 2 = 8.5; chapter 3 = 9.5; chapter 4 = 10; chapter 5 = 15; chapter 6 = 0.5 + 6 + 2 + 1 + 2 (layout repair) + 0.5 (Lecture) = 12; total about 76 (was 136). NOT AFFECTED: every criterion, every committed file, the exam stories that run. RISK: the Friday builders may not fit a chapter (the executor stops and reports)." % len(HRS)))
    return t + cr + ia, "Change request with impact assessment: the not-started midterm-scope tasks are simplified to the Friday fixes (reuse, no re-measuring, one session per chapter, lower estimates), at the owner's order; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") changes the dependencies of not-started tasks, which the Backlog digest counts, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: midterm scope simplified to the Friday fixes"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
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
    for tid, sess in SESS.items():
        i, j = T.blk(t, tid); b = t[i:j]; b2, k = re.subn(r"Planned session SEN0401-[A-Za-z0-9-]+", "Planned session " + sess, b); assert k >= 1, tid
        t = t[:i] + b2 + t[j:]
    for tid, h in HRS.items():
        i, j = T.blk(t, tid); b = t[i:j]; b2, k = re.subn(r"about [\d.]+ hours", "about %.1f hours" % h, b); assert k >= 1, tid
        b2 = re.sub(r'(backlog:hasAuditNote ")((?:[^"\\]|\\.)*)"', lambda m: m.group(1) + m.group(2) + REUSE.replace('"', '\\"') + '"', b2, count=1)
        t = t[:i] + b2 + t[j:]
    for c in range(1, 7):
        i, j = T.blk(t, "TK_Ch0%d_PageCode_Build" % c); b = t[i:j]; b2, k = re.subn(r"the template 9\.52\.7 of the story ST_Template_Panels", "the template 9.52.9 (made on Friday; the page template of the chapter 6 page v9.89.0)", b)
        t = t[:i] + b2 + t[j:]
    L = ['ex:SC3_MidtermSimplify a backlog:ScopeChange ;\n    rdfs:label "Midterm-scope tasks simplified to the Friday fixes"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem ex:ST_Ch06_DeckCode ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, lit(PACE))]
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_MidtermSimplify; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR43 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt with the simplified midterm-scope tasks"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: the midterm-scope tasks simplified to the Friday fixes (reuse, no re-measuring, one session per chapter), %d tasks rewritten (change request Accepted); %d items re-admitted." % (len(HRS), n)
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
