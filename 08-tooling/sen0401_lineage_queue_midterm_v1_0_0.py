#!/usr/bin/env python3
"""sen0401_lineage_queue_midterm v1_0_0 - two events, one new register version each (owner's direction of 2026-10-28 14:21 Istanbul, relayed by the coordinator).
  gaps  : two ChangeRequests for the verified gaps of chapters 1 to 8 found by the lineage agent's own re-runs of the deck check v1_1_0 (chapter work comes first).
  queue : the midterm exam of chapters 1 to 8 is a DIFFERENT mission (G104, G159): it waits as a lineage at LS_Opened (ex:Lineage4) under the adaptive opening profile of the
          framework (opening block printed by backlog_open_lineage v1_1_0 from the data file, not typed); ex:Lineage3 keeps running; nothing of the exam is started.
Usage: gaps | queue"""
__version__ = "1.0.0"
import glob, importlib.util, os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_gap_revision_v1_0_0 as G
lit = G.lit; B, BASE, FW = M.B, M.BASE, M.FW

def _load(path, name):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def ev_gaps(t):
    base = ("MEASURED 2026-10-28 by the lineage agent on its own re-run (python 3.14.6, sen0401_deck_check_v1_1_0.py NN with the delivered deck of 03-materials, logs kept by the run): ")
    tail = (" This is not an element of the criterion the deck was controlled on, so that criterion stays met; it is a gap against the mission clause that a lecture is renewed from the book and researched evidence with code-derived charts and re-run examples, said openly and not waived. "
            "The midterm exam of chapters 1 to 8 (queued, ex:Lineage4) draws on these decks, so chapter work comes first (the coordinator's order of 2026-10-28). Filled through change management in the active lineage: a new deck version as new files, then a control.")
    c1 = ('\nex:CR3_Ch01DeckCheck a backlog:ChangeRequest ;\n    rdfs:label "The chapter 1 deck v3_1_0 is refused by the deck check v1_1_0: 8 plotted chart values are in no executed output"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Accepted .\n'
          ) % lit(base + "chapter 1, deck v3_1_0 (62 slides): 15 examples re-run, 5 charts, 8 mismatches, all of one kind: the plotted values 10.5, 15.75, 18.375, 19.6875, 20.3438, 20.6719, 20.8359 and 20.918 (the supply-by-halving chart) are in no executed output (provenance). The arc check v1_3_0 accepts the deck." + tail)
    c5 = ('\nex:CR3_Ch05DeckCheck a backlog:ChangeRequest ;\n    rdfs:label "The chapter 5 deck v3_2_0 is refused by the deck check v1_1_0: 27 example rows are not recorded rows and the charts do not match the plan"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_GateArcDark ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Accepted .\n'
          ) % lit(base + "chapter 5, deck v3_2_0 (68 slides): 106 examples re-run, 32 mismatches: 27 example rows (among them the row of the interpreter version on slides 11, 17, 18, 22 and 23) are 'not a recorded row with this result' (the recording of the chapter in 08-tooling/ch05-deck is that of the older deck v2_3_0), and 5 chart mismatches (the plan has 5 chart items, the file 1 chart part). The arc check v1_3_0 refuses the same deck for the dark closing slide (the pending change request ex:CR3_GateArcDark, the owner's word is awaited, not touched here)." + tail)
    return t + c1 + c5, "Two ChangeRequests for the verified deck gaps of chapters 1 and 5 found by the lineage agent's re-run of the deck check v1_1_0 (the decks of chapters 2 to 4 and 6 to 8 pass it; chapters 1 to 8 pages and research not changed)."

MISSION = '''
ex:Mission_Midterm a backlog:Mission ;
    rdfs:label "A SEN0401 student sits a midterm exam on chapters 1 to 8, built from the course's own verified material"@en ;
    backlog:missionFor ex:Backlog ;
    backlog:hasMissionStatement "The SEN0401 midterm exam covers chapters 1 to 8 of Mastering Bitcoin's third edition as the course teaches them: items that need course knowledge, mostly at the higher Bloom levels, delivered as printed paper with an answer key and as a CATS/QTI export, following the Exam Studio conventions." ;
    backlog:hasMissionOrigin "Owner direction of Wednesday 2026-10-28 14:21 Istanbul, relayed by the coordinator: the midterm is built after the current chapters are completed and is held next week; the owner's answers: coverage chapters 1 to 8; delivery without a stated preference (default printed paper plus answer key, with CATS/QTI export); Exam Studio conventions (multiple-choice letters evenly distributed, fill-in option banks randomised, print-safe, no fabricated terms, items need course knowledge, higher Bloom levels in the majority). VERIFIED GAP it is set from: the assessment ontology 04-assessment/sen0401_assessment_v1_0_0.ttl holds the Midterm component (30 percent) and states that no exam items are held yet; nothing else of the exam exists." ;
    backlog:hasMissionOutcome "A student sits the midterm on chapters 1 to 8, and the instructor holds a printed paper, its answer key and a CATS/QTI export that were built from the course's verified decks, pages and research." ;
    backlog:outcomeRationale "The mission is immature on purpose (adaptive profile): the exam structure, the number of items and the weights per chapter are not decided and are matured stage by stage and box by box. It waits at LS_Opened because the running lineage ex:Lineage3 has not been confirmed accomplished (G104, G159, the owner's rule of 2026-10-26)." ;
    backlog:decidedBy backlog:Owner ;
    backlog:producedByStage ex:Out4_Mission ;
    backlog:missionSource "The owner's direction quoted above; the verified gaps of chapters 1 to 8 are the change requests ex:CR3_Ch01DeckCheck and ex:CR3_Ch05DeckCheck and the pending ex:CR3_GateArcDark, ex:CR3_DeckCh06Slide51 (they come first)." .
'''

def digest(text):
    pv = _load(sorted(glob.glob(FW + "/03-tooling/backlog_pipeline_verify_v*.py"), key=lambda q: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", q)[0]])[-1], "pv")
    pv.STAGE_TYPES = pv._load_stage_types(sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"))[-1], table="v4")
    g = rdflib.Graph(); g.parse(data=text, format="turtle")
    return pv.state_digest(g, "Stage_Mission", rdflib.URIRef(BASE + "#Lineage4"), admitted=True)

def ev_queue(t):
    ol = _load(FW + "/03-tooling/backlog_open_lineage_v1_1_0.py", "ol")
    ab = sorted(glob.glob(FW + "/01-ontologies/backlog_abox_v*.ttl"), key=ol.sv)[-1]
    g = rdflib.Graph(); g.parse(ab, format="turtle"); P = ol.profiles(g)
    blk = ol.block("Profile_Adaptive", "Lineage4", "ex", P["Profile_Adaptive"], ol.latest_revision(g))
    lin = ('\nex:Lineage4 a backlog:Lineage ;\n    rdfs:label "Fourth lineage for SEN0401: the midterm exam of chapters 1 to 8 (queued, not started)"@en ;\n'
           '    backlog:lineageForMission ex:Mission_Midterm ; backlog:lineageOrdinal 4 ; backlog:lineageArchived false ;\n    backlog:hasLineageStatus backlog:LS_Opened .\n' + blk)
    t2 = t + lin + MISSION
    out = ('\nex:Out4_Mission a backlog:StageOutput ;\n    rdfs:label "Closure of the Mission stage of the fourth lineage"@en ;\n    backlog:belongsToLineage ex:Lineage4 ;\n'
           '    backlog:outputOfStage backlog:Stage_Mission ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % digest(t2)
    return t2 + out, "The midterm exam of chapters 1 to 8 is queued as the fourth lineage at LS_Opened under the adaptive opening profile (a different mission waits, G104 and G159); the third lineage keeps running; no exam work is started."

def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    nt, comment = {"gaps": ev_gaps, "queue": ev_queue}[ev](t)
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__":
    main()
