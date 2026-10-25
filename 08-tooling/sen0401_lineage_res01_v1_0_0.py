#!/usr/bin/env python3
"""sen0401_lineage_res01 v1_0_0 - change route (G104, G125, G127, G129, G133, G136) that ADMITS the two Pending change requests ex:CR3_Ch01Research (the two structural gaps of the chapter 1 research set) and ex:CR3_ArcCheck (the deck arc check demands a 26-slide standard and refuses a closing summary part)
as work: a StageRevision from the Scope stage (a deliverable is added), the Scope, Goal, Objective and Backlog outputs rebuilt one per version, a last version fills the last commit. Same route as sen0401_lineage_retro24 (whose helpers it uses).
New stories: ST_Ch01_Research_R24 (Iteration 26, with the chapter 1 page) and ST_ArcCheck_Repair (Iteration 28), each with a Build task (executor) and a Verify task (lineage agent), a criterion and two test cases; planning events for both.
The requests exist already (v0.294.0 and v0.288.0), so there is no change step. Usage: retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_retro24_v1_0_0 as RT
R = RT.R; lit = G.lit
CRS = ["ex:CR3_Ch01Research", "ex:CR3_ArcCheck"]; REV = "ex:Revision_Lineage3_Scope12"
ACTIVE = ["ex:Out3_ScopeR12", "ex:Out3_GoalR12", "ex:Out3_ObjectiveR12", "ex:Out3_BacklogR14"]; NEWB = "ex:Out3_BacklogR15"; R.NEWB = NEWB; R.IT1 = "ex:Iter_26"
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route under the owner's standing orders (gaps found are filled through change management; repairs re-rank; a lineage never waits)"
FACT = ("MEASURED 2026-10-25. Research set of chapter 1: the form of the chapter 2 verify script (library sen0401_research_verify_lib_v1_0_0.py) fails on it with ('publication never cited', 'P23', 'RFC 3986') and ('counts', 30, 7): 7 findings against the minimum of 8 (executor of TK_Ch01_VerifyScript_Build, commit 7ac4a31; control v0.293.0). "
        "Arc check: sen0401_deck_arc_check_v1_1_0.py demands a 26-slide deck (--slides N is a flag, not read from the plan) and refuses a deck whose agenda ends with a summary-and-resources part that starts at a slide that is not a section slide; it refuses the decks of chapters 1 and 8 and, with the right length, the deck of chapter 4 (agenda range 45-47). It is not an element of any criterion of Iterations 24 to 28.")
TXT_RES = ("Repair the research set of chapter 1 as NEW files (the research files of 03-materials/ch01/rdodi stay unchanged; new versions above the newest): (1) cite the publication P23 (RFC 3986) where the research uses it, or drop it with a stated reason; (2) reach the findings minimum of 8 (the library's) with findings that are true and sourced, not padding; "
           "(3) after the repair the form of the chapter 2 verify script (the shared library sen0401_research_verify_lib_v1_0_0.py, not edited) passes on the chapter 1 research, so a NEW version of the chapter 1 verify script above v1_0_0 adopts that form and keeps the quotation, number and example checks; "
           "(4) the Research chapter check v1_3_0 for Research/Ch01 exits 0 and the Stage 4 gate runner v1_1_0 for 01 exits 0; the validators (CURRENT v1.13.0 for Stage 4, PINNED v1.6.0 for the chapter check) pass on the new research; (5) the research is consistent (HermiT) and nothing else in the repository is edited. " + R.NOEDIT + " " + R.COMMON)
TXT_ARC = ("Make the NEW file 08-tooling/sen0401_deck_arc_check_v1_2_0.py from v1_1_0 (which stays byte-identical, SHA-256 before and after): (1) the number of slides is read from the deck (or the plan) unless --slides is given, so a deck of any length is checked against the rest of the rule; (2) a closing part of the agenda (summary, resources, closing) may start at the summary slide that precedes the resources slide, not only at a section slide; "
           "every other rule and message is unchanged. PROOF to keep as logs: the unified diff; SHA-256 of v1_1_0 before and after; v1_2_0 on the decks of chapters 1, 4 and 8 (and 5, 6, 7 for comparison): the refusals of the 26-slide demand and of the closing-part agenda range are gone, and every refusal that remains is one the check's own rule gives (listed); on a fixture deck with a wrong agenda range (a range starting inside a section) v1_2_0 still refuses. " + R.NOEDIT + " " + R.COMMON)
ST = [("ST_Ch01_Research_R24", "The research set of chapter 1 meets the research standard: the two structural findings are repaired as new files", ["AC9_Ch01Research"], ["TK_Ch01_Research_Build_R24", "TK_Ch01_Research_Verify_R24"], "Iter_26", "SEN0401-I26-research-ch01", TXT_RES, "Run, as printed: the Research chapter check v1_3_0 for Research/Ch01 (venv314), the form of the ch02 verify script on the new research, the Stage 4 gate runner v1_1_0 for 01, nochange on the executor's commits; read the new findings against their sources."),
      ("ST_ArcCheck_Repair", "The deck arc check reads the length of the deck and accepts a closing summary part, as a new tool version", ["AC9_ArcCheck"], ["TK_ArcCheck_Build", "TK_ArcCheck_Verify"], "Iter_28", "SEN0401-I28-arccheck", TXT_ARC, "Run v1_2_0 on the decks of chapters 1, 4, 5, 6, 7, 8 and the fixtures, byte-compare v1_1_0, nochange; record every result as printed.")]
def crit():
    return {"AC9_Ch01Research": ("The research set of chapter 1 passes the form of the chapter 2 verify script and the Research chapter check, as new files", "Owner-directed work (" + CRS[0] + ", " + WHEN + "). Given the research of chapter 1 and the chapter 1 verify script v1_0_0 (unchanged), when the research is repaired as new files, then ALL of: (1) P23 is cited or dropped with a stated reason; (2) the findings reach the library minimum of 8; (3) the form of the chapter 2 verify script (shared library, unedited) passes on the new research and a NEW verify script version adopts it; (4) the Research chapter check for Research/Ch01 and the Stage 4 gate runner for 01 exit 0; (5) no committed file is edited; results as printed; if any element fails the research is named failing. " + FACT, "ex:TS_ResearchCheck, ex:TS_ChapterCheck, ex:TS_Stage4Gates, ex:TS_RdodiValidatorCurrent, ex:TS_RdodiValidatorPinned", "Research chapter check v1_3_0 (venv314) reading the PINNED RDODI validator v1.6.0; Stage 4 gate runner v1_1_0 reading the CURRENT validator v1.13.0; shared verify library sen0401_research_verify_lib_v1_0_0.py"),
            "AC9_ArcCheck": ("The deck arc check v1_2_0 reads the deck length and accepts a closing part and changes nothing else", "Owner-directed work (" + CRS[1] + ", " + WHEN + "). Given the arc check v1_1_0 (unchanged), when the NEW file v1_2_0 is made, then ALL of: (1) v1_1_0 is byte-identical (SHA-256 before and after); (2) the diff is limited to the reading of the deck length and the closing-part agenda range; (3) on the decks of chapters 1, 4 and 8 the two refusals are gone and the remaining refusals are listed with their rule; (4) a fixture with a wrong agenda range is still refused; (5) no committed file is edited; results as printed. " + FACT, "ex:TS_DeckStdCheck11", "arc check v1_2_0 (python-pptx 1.0.2); v1_1_0 byte-identical")}
def blocks_new():
    return [(sid, title, crits, tks, it, sess, txt, vtxt) for sid, title, crits, tks, it, sess, txt, vtxt in ST]
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change requests " + ", ".join(CRS) + " (" + WHEN + ") add a deliverable (the repair of the chapter 1 research set and of the arc check); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The requests and their assessments were recorded first (v0.288.0, v0.294.0). "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the repair of the chapter 1 research set and of the deck arc check"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_Ch01Research ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, ", ".join(CRS), lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the repair of the chapter 1 research set and of the deck arc check: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The research set of chapter 1 repaired and the deck arc check repaired, each as new files"
    tx = "The research of chapter 1 as new files citing or dropping P23 and reaching the findings minimum, with a verify script version that adopts the shared form; the deck arc check v1_2_0 as a new file that reads the deck length and accepts a closing part. " + FACT
    L = ('\nex:Del3_Res01 a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Res01 ; rdfs:seeAlso %s .\n" % ", ".join(CRS)
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change requests %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the research repair and the arc-check repair). No exclusion changes: new files only." % (REV, ", ".join(CRS), WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR13", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the research and arc-check repairs: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR13", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Res01 a backlog:Goal ;
    rdfs:label "The chapter 1 research set and the deck arc check meet the standard that their own checks state"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR13 .
ex:G3_Res01 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change requests ex:CR3_Ch01Research and ex:CR3_ArcCheck; the intent origin is therefore Derived."@en .
ex:Spec3I_Res01 a backlog:Specification ;
    rdfs:label "What it is for the research repair and the arc-check repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Res01 ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR13 .
ex:Spec3I_Res01_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Res01 ; backlog:hasScenarioText %s .
ex:Spec3I_Res01_Fail a backlog:TestScenario ; rdfs:label "A repair that pads the findings, edits a committed file, or leaves a refusal unexplained is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Res01 ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change requests: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new research files or the new arc check version, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a research repair that adds an uncited finding or edits a committed file, or an arc check that loses a refusal it should keep, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR13", "Out3_ScopeR13"), "third lineage, Goal stage rebuilt for the research and arc-check repairs: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR13", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Res01 a backlog:Objective ; rdfs:label "The two repairs met on verified evidence: from 0 to 2"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Res01 ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Res01 ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "2"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Res01 ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR13 .
ex:Met3_Res01 a backlog:Metric ; rdfs:label "repairs (chapter 1 research set, deck arc check) whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Res01 a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair stories are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the two criteria." ; backlog:expectedValue "2"^^xsd:decimal .
ex:ObsR24_Res01_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Res01 ; backlog:observationFor ex:Obj3_Res01 ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Res01 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change requests ex:CR3_Ch01Research and ex:CR3_ArcCheck; the intent origin is therefore Derived."@en .
''' % (lit("Count of the two repair stories (ST_Ch01_Research_R24, ST_ArcCheck_Repair) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the measurements of 2026-10-25 (v0.293.0 and v0.292.0): neither repair exists, so 0 of 2."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR13", "Out3_GoalR13"), "third lineage, Objective stage rebuilt for the research and arc-check repairs: one objective (0 to 2) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR13", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR14"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + ", ".join(CRS) + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_Ch01Research and the control of v0.293.0."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Res01").replace("ex:Data3S_TC9_", "ex:Data3S_TC9R_").replace("ex:TC9_", "ex:TC9R_"))
    L = [x.replace("ex:TC9_", "ex:TC9R_") for x in L]
    for sid, title, crits, tks, it, sess, txt, vtxt in ST:
        L.append(R.story_block(sid, title, "Del3_Res01", "Obj3_Res01", crits, tks, note, "ex:" + it, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", [], sess, "S", 2.0 if "Research" in sid else 1.5, txt, "ex:" + it, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+2.0h", 1.0, vtxt, "ex:" + it, "Proposed", True))
        L.append('ex:Plan3L_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration %s (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Res01, ex:Spec3I_Res01_Pass, ex:Spec3I_Res01_Fail .\n' % (sid, sid, it[5:], now, it, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
        i, j = T.blk(t, it); b = t[i:j]; assert "backlog:hasMember" in b
        nb = re.sub(r"(backlog:hasMember [^.]*?)\s*\.\s*$", lambda m: m.group(1) + ", ex:" + ", ex:".join([sid] + tks) + " .\n", b.rstrip() + "\n", count=1, flags=re.S); assert nb != b
        t = t[:i] + nb + t[j:]
    L.append("ex:Obj3_Res01 backlog:metricMovableBy ex:ST_Ch01_Research_R24, ex:ST_ArcCheck_Repair .\n")
    L.append('ex:SC3_Res01 a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the repair of the chapter 1 research set and of the deck arc check"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:ST_Ch01_Research_R24, ex:ST_ArcCheck_Repair ;\n    backlog:hasScopeChangeRationale %s .\n' % (", ".join(CRS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), which the lineage agent applied (" + WHEN + "). The boundary moved outward by two stories; new files only.")))
    for c in CRS:
        t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(c), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1, c
        L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Res01 and the stories it admits; it was Pending before."@en .\n' % (c, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR15", "Out3_ObjectiveR13"), "third lineage, Backlog stage rebuilt: the research repair of chapter 1 (Iteration 26) and the arc-check repair (Iteration 28) admitted with criteria, tasks, planning events and the ScopeChange; both change requests Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
