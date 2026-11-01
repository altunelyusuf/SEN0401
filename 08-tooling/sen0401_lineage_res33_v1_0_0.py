#!/usr/bin/env python3
"""sen0401_lineage_res33 v1_0_0 - change route (G113, G125 route 2, G133, G147) for the owner's instruction of 2026-11-01 12:13 Istanbul: the files delivered for the midterm scope (SEN0401 chapters 1 to 6) are not ready to share; the code on the slides must match the page's Chapter Examples, and the decks and pages are brought to the quality level of the Friday chapter 6 files. A StageRevision from the Backlog stage: five new stories (the Teach deck of chapters 1 to 5), the not-started PageCode tasks of chapters 1 to 6 and the Lecture repair of chapter 6 are made to wait for the final deck. Events: change | retract | backlog PREV | fill PREV"""
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
REV = "ex:Revision_Lineage3_Backlog13"; OLD = "ex:Out3_BacklogR40"; NEWB = "ex:Out3_BacklogR41"; R.NEWB = NEWB; ITER = "Iter_54"
CR = "ex:CR3_MidtermQuality"; IA = "ex:IA3_MidtermQuality"
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
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The delivered files of the midterm scope (chapters 1 to 6) are brought to the chapter 6 Friday standard before they are shared"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Pending ; rdfs:seeAlso %s, ex:CR3_ExamMission ;\n    backlog:hasChangeRequestRationale %s .\n') % (CR, IA, lit("Raised " + WHEN + ". " + FACT))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the midterm-scope quality work costs and touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(FACT + " ROUTE: a change request in the running lineage, not an urgency ceremony: the exam executors that run (the reader and the paper) are not paused, the owner's exam-first rule of 2026-10-30 stays for them, and nothing is suspended; the work of chapters 1 to 6 is already planned as stories (the code-only deck, the page rebuild, the page measure, the deck checks, the code gate, the page templates) and this change adds what the Friday standard has that they lack: a Teach story for each of chapters 1 to 5 (slides that teach alone, storytelling, results as visuals, clean layout), the Lecture tab and the full-screen and resizable panels as criteria of the page rebuild, and the order. AFFECTED: five new stories ST_Ch01_DeckTeach to ST_Ch05_DeckTeach; the PageCode Build tasks of chapters 1 to 6 wait for the final deck of their chapter (and the chapter 6 Lecture repair waits for the chapter 6 Teach deck, since the slide count may change). NOT AFFECTED: every committed file, the exam stories. ESTIMATE (G120), agent hours per chapter: foundations (deck checks 4, code gate 4, code template 6, panels template 7) = 21; chapter 1: code deck 2.5 + Teach 8.5 + page 3 + measure 3 = 17; chapter 2: 2.5 + 5 + 3 + 3 = 13.5; chapter 3: 3 + 6 + 3 + 3 = 15; chapter 4: 3 + 6.5 + 3 + 3 = 15.5; chapter 5: 5 + 9.5 + 4 + 3 = 21.5; chapter 6: code deck 4 + Teach 10 + page 3 + measure 3 + Lecture and layout repairs (see their records) in addition. Total about 103 agent hours beyond the chapter 6 repairs. OPEN FOR THE OWNER (one question): which chapter he teaches next, to order the chapters."))
    return t + cr + ia, "Change request with impact assessment: the owner's instruction of 2026-11-01 12:13 to bring the midterm scope (chapters 1 to 6) to the chapter 6 Friday standard before sharing, with the as-is fit-gap measured per chapter; no stage changed."
def ev_retract(t):
    reason = ("The change request " + CR + " (" + WHEN + ") adds five stories with their own criteria and changes the dependencies of not-started tasks; a new criterion is counted by the Backlog digest, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the midterm scope brought to the Friday standard"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return X.set_status(t, "LS_Objectived") + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the owner's instruction on the midterm scope; nothing is rebuilt here." % OLD.replace("ex:", "")
def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125)."
    mem = []
    for c in range(1, 6):
        aid, label, g_ = crit(c); k = aid[4:]
        L.append(RT.ac_block(aid, label, g_, 'ex:TS_ChapterCheck, ex:TS_DeckMatch', "the prompt, lambda, indent and label-word checks; layout, notes, deck standard, arc, overlap and deck checks", k).replace("ex:TC9_", "ex:TC9T_"))
        L.append(RT.case_blocks(k, aid).replace("Spec3I_Retro24", "Spec3I_Ch06Teach").replace("ex:Data3S_TC9_", "ex:Data3S_TC9T_").replace("ex:TC9_", "ex:TC9T_")
            .replace("Run the checks on the item as measured in the baseline of 2026-10-25 (an overlap, a manifest example that starts with an error name, a story whose text lies below the first screen, a committed file with status M) and require that nothing is claimed for it.", "Run the checks on the item as it stands before the work and require that nothing is claimed for it.")
            .replace("The finding as measured in the baseline of 2026-10-25 (ex:IA3_Retro24).", "The finding as measured on 2026-11-01 (ex:IA3_MidtermQuality)."))
        sid = "ST_Ch0%d_DeckTeach" % c; tks = ["TK_Ch0%d_DeckTeach_Build" % c, "TK_Ch0%d_DeckTeach_Verify" % c]; mem += [sid] + tks
        L.append(R.story_block(sid, title(c), "Del3_ChapterCode", "Obj3_ChapterCode", [aid], tks, note, "ex:" + ITER, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title(c), "Build", ["TK_Ch0%d_DeckCode_Verify" % c, "TK_Deck_Checks_Verify"], EFF[c][1], "S", EFF[c][0], txt_build(c), "ex:" + ITER, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title(c), "Verify", [tks[0]], "builder", "S+%.1fh" % EFF[c][0], 3.0, txt_verify(c), "ex:" + ITER, "Proposed", True))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
        L.append("ex:Obj3_ChapterCode backlog:metricMovableBy ex:%s .\n" % sid)
    # the PageCode tasks wait for the final deck; clause on the Lecture tab and the panels
    CL = " ADDED 2026-11-01 (" + CR.replace("ex:", "ex:") + "): the page is built from the FINAL deck of the chapter (the Teach deck); its Lecture tab lists every slide of that deck in order, the count equal to the deck's, each with its note; the code of each slide equals the Chapter Examples of the page text for text in slide order; every diagram has zoom in and out, a full-screen view and a resizable panel (template 9.52.7); the layout is clean. Measure these and report each as printed."
    for c in range(1, 7):
        bid = "TK_Ch0%d_PageCode_Build" % c; i, j = T.blk(t, bid); b = t[i:j]
        m = re.search(r"(backlog:dependsOn )([^;]*?)( ;)", b); assert m, bid
        b = b.replace(m.group(0), m.group(1) + m.group(2).rstrip() + ", ex:TK_Ch0%d_DeckTeach_Verify" % c + m.group(3), 1)
        m = re.search(r'(backlog:hasAuditNote ")((?:[^"\\]|\\.)*)"', b); s_ = m.group(2); k_ = s_.find(" Planned session"); assert k_ > 0, bid
        b = b[:m.start()] + m.group(1) + s_[:k_] + CL.replace('"', '\\"') + s_[k_:] + '"' + b[m.end():]
        t = t[:i] + b + t[j:]
    i, j = T.blk(t, "TK_Repair_Ch06_Lecture_Build"); b = t[i:j]; m = re.search(r"backlog:dependsOn ([^;]*?) ;", b)
    b = (b.replace(m.group(0), "backlog:dependsOn " + m.group(1).rstrip() + ", ex:TK_Ch06_DeckTeach_Verify ;", 1) if m else b.replace("backlog:hasState backlog:Proposed ;", "backlog:hasState backlog:Proposed ;\n    backlog:dependsOn ex:TK_Ch06_DeckTeach_Verify ;", 1))
    t = t[:i] + b + t[j:]
    i, j = T.blk(t, ITER); b = t[i:j]; m = re.search(r"backlog:hasMember ([^;.]*?)( ;| \.|\.\n)", b, re.S); assert m
    t = t[:i] + b.replace(m.group(0), "backlog:hasMember " + m.group(1).rstrip() + ", " + ", ".join("ex:" + x for x in mem) + m.group(2), 1) + t[j:]
    L.append('ex:SC3_MidtermQuality a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the Teach decks of chapters 1 to 5 and the final-deck order of the pages"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:ST_Ch0%d_DeckTeach" % c for c in range(1, 6)), lit("The owner's instruction of 2026-11-01 12:13; the rule that a change re-ranks the open items. " + FACT)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_MidtermQuality; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + ('\nex:Out3_BacklogR41 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt for the midterm scope quality work"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR32 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % X.digest(t, "Backlog"), \
        "third lineage, Backlog stage rebuilt: five Teach stories for chapters 1 to 5, the PageCode tasks of chapters 1 to 6 wait for the final deck (change request Accepted); %d items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s)." % (NEWB.replace("ex:", ""), prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
