#!/usr/bin/env python3
"""sen0401_lineage_res08 v1_0_0 - change route (G104, G125, G127, G129, G133, G136) for the gap the control of the template 9.52.3 found: its executor edited the committed template file three times (element 5 of AC9_Template not met). A ChangeRequest ex:CR3_TemplateRedo with its ImpactAssessment, then a StageRevision from the Scope stage that ADMITS one story, ST_Template_9524 (the verified bytes as a new file), into the NEW Iteration 34 (planned, not started), and re-points the page items of Iterations 25 to 28 to the new template. Same route as sen0401_lineage_res06. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_retro24_v1_0_0 as RT
R = RT.R; lit = G.lit
CR = "ex:CR3_TemplateRedo"; REV = "ex:Revision_Lineage3_Scope18"
ACTIVE = ["ex:Out3_ScopeR18", "ex:Out3_GoalR18", "ex:Out3_ObjectiveR18", "ex:Out3_BacklogR20"]; NEWB = "ex:Out3_BacklogR21"; R.NEWB = NEWB
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders; nothing is waived)"
FACT = ("MEASURED 2026-10-25 by the lineage agent in the control of the template task (register v0.394.0, tool sen0401_template_control_check_v1_0_0.py): the committed file 08-tooling/course_page_template_v9_52_3.html was EDITED by its executor three times after its first commit (fb1d9f8, 36eeb95, 8a1922f; revisions 2, 3, 4), each after a failed check, instead of being made as new versions, and the log of its first failed batch was deleted before it was saved; the executor disclosed this. "
        "The rule is that a committed file is never edited, and element (5) of the criterion AC9_Template says so; it is NOT MET, as the control of the page 9.82.0 of chapter 5 named an appended log not met. The other four elements are met by the content of the final file (SHA-256 44bcb3e7...564d): 9.52.2 unchanged, the diff limited to the story rules, the story layout probe PASS on the scratch pages of chapters 5 to 8, the regression on the scratch pages of chapters 5, 1 and 10 at or above the stored results. "
        "Nothing is waived: the template task is Suspended, and the template is delivered again as a NEW file that is never edited.")
TXT_TP = ("Make the NEW file 08-tooling/course_page_template_v9_52_4.html as a byte-identical copy of the committed 08-tooling/course_page_template_v9_52_3.html (final content, SHA-256 44bcb3e7b29a4917b8673c5cf08e79bd516a66ad3e21e4985a3884918f98564d), in ONE commit, and never edit it afterwards (the files 9.52.2 and 9.52.3 stay byte-identical: SHA-256 before and after). "
          "No content change is made or wanted: the bytes that were verified are the bytes that ship, under a name whose history shows no in-place edit. PROOF kept as logs, each written once after its run is complete: SHA-256 of 9.52.2, 9.52.3 and 9.52.4 before and after (9.52.4 equal to 9.52.3); scratch pages of chapters 1, 5, 6, 7, 8 and 10 built from 9.52.4 and from 9.52.3 with the page builder v4_15_0 (PAGE_TEMPLATE, PAGE_SCRATCH, the newest page version of each chapter) are byte-identical in pairs (SHA-256 of each); the story layout probe v1_0_0 on the scratch pages of chapters 5 to 8 built from 9.52.4 (under flock /tmp/page_test.lock) prints RESULT PASS; nochange (the commit only adds one file). "
          "DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES. A committed file is never edited: every output is a new file with a new version number. STOP and report if the task cannot be satisfied without editing a committed file. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. The machine has 2 cores: browser tests run one at a time under the lock.")
STS = [("ST_Template_9524", "The page template 9.52.4: the verified bytes of 9.52.3 as a new file that is never edited", ["AC9_Template9524"], ["TK_Template_9524_Build", "TK_Template_9524_Verify"], "SEN0401-I34-template9524", TXT_TP, "Compare the SHA-256 of the three templates; build the scratch pages of chapters 1, 5, 6, 7, 8, 10 from both and compare; run the story layout probe on chapters 5 to 8; nochange (one file added, never modified).", [], 14, 2, 1.5)]
ITER = ("Iter_34", "Iteration 34: the page template 9.52.4, a new file for the verified bytes of 9.52.3 (planned, not started)", "2026-11-06T12:00:00", "2026-11-07T12:00:00", "The page template 9.52.4 exists as a new file, equal to the verified 9.52.3, and the page items name it.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    return {"AC9_Template9524": ("The page template 9.52.4 is the verified content of 9.52.3 as a new file, never edited", base + "Given the templates 9.52.2 and 9.52.3 (both unchanged), when the NEW template 9.52.4 is made, then ALL of: (1) 9.52.2 and 9.52.3 are byte-identical (SHA-256 before and after: 9089403f...73db and 44bcb3e7...564d); (2) 9.52.4 is added in one commit, is byte-identical to 9.52.3, and no later commit modifies it (git log --diff-filter=M over it is empty); (3) scratch pages of chapters 1, 5, 6, 7, 8 and 10 built with the page builder v4_15_0 from 9.52.4 are byte-identical to those built from 9.52.3, so the regression results of the control of 9.52.3 hold for the same bytes, and the story layout probe v1_0_0 on the scratch pages of chapters 5 to 8 gives RESULT PASS; (4) no committed file is edited; results as printed; if any element fails the template is named failing. " + FACT, "ex:TS_PageBuilder415, ex:TS_StoryLayoutProbe", "page template 9.52.4; page builder v4_15_0; story layout probe v1_0_0")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Repair of the in-place edits of the page template 9.52.3, as a new template file"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the story into Iteration 34."))
    ia = ('\nex:IA3_TemplateRedo a backlog:ImpactAssessment ;\n    rdfs:label "What the template repair costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: a new template file and the page items that name the template. NOT AFFECTED: the controlled criteria of the decks (they stay met), the content of the template (unchanged), the old templates, every committed file. ESTIMATE (G120): 1.5 h executor plus 0.5 h verification. The page items of Iterations 25 to 28 name the template and its Verify task: they are re-pointed to 9.52.4 in the rebuilt Backlog (their text only; no criterion is edited in meaning, none has evidence)."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the in-place edits of the page template 9.52.3 of the control of the template task (v0.394.0)."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the repair of the in-place edits of the page template 9.52.3); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the repair of the in-place edits of the page template 9.52.3"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_TemplateRedo ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the repair of the in-place edits of the page template 9.52.3: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The page template 9.52.4, the verified bytes of 9.52.3 as a new file"
    tx = "New file: the page template 9.52.4. " + FACT
    L = ('\nex:Del3_TemplateRedo a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_TemplateRedo ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the in-place edits of the page template 9.52.3). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR19", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the in-place edits of the page template 9.52.3: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR19", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_TemplateRedo a backlog:Goal ;
    rdfs:label "The page template is delivered as a new file that is never edited"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR19 .
ex:G3_TemplateRedo rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_TemplateRedo; the intent origin is therefore Derived."@en .
ex:Spec3I_TemplateRedo a backlog:Specification ;
    rdfs:label "What it is for the template repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_TemplateRedo ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR19 .
ex:Spec3I_TemplateRedo_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_TemplateRedo ; backlog:hasScenarioText %s .
ex:Spec3I_TemplateRedo_Fail a backlog:TestScenario ; rdfs:label "A repair that loses a refusal, leaves a folder or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_TemplateRedo ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new files, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a tool version that loses a refusal or an exit code, or leaves a folder, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR19", "Out3_ScopeR19"), "third lineage, Goal stage rebuilt for the in-place edits of the page template 9.52.3: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR19", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_TemplateRedo a backlog:Objective ; rdfs:label "The template repair met on verified evidence: from 0 to 1"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_TemplateRedo ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_TemplateRedo ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "1"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_TemplateRedo ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR19 .
ex:Met3_TemplateRedo a backlog:Metric ; rdfs:label "template repair whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_TemplateRedo a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair story is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criterion." ; backlog:expectedValue "1"^^xsd:decimal .
ex:ObsR26_TemplateRedo_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_TemplateRedo ; backlog:observationFor ex:Obj3_TemplateRedo ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_TemplateRedo rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_TemplateRedo; the intent origin is therefore Derived."@en .
''' % (lit("Count of the repair story (ST_Template_9524) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the template task on 2026-10-25: the new template file does not exist, so 0 of 1."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR19", "Out3_GoalR19"), "third lineage, Objective stage rebuilt for the in-place edits of the page template 9.52.3: one objective (0 to 1) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR19", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR20"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    cnt = 0; extra = []
    for m in sorted(set(re.findall(r"\nex:(\w+) a backlog:(?:Story|ExecutionTask|AcceptanceCriterion)\b", t))):
        if m in ("ST_Template_9523", "TK_Template_9523_Build", "TK_Template_9523_Verify", "AC9_Template") or m.startswith("ST_Remedy") or m.startswith("TK_Remedy"): continue
        i, j = T.blk(t, m); b = t[i:j]
        if not re.search(r"9\.52\.3|9_52_3|Template_9523", b): continue
        stt = re.findall(r"hasState backlog:(\w+)", b)
        if stt and stt[0] in ("Done", "Cancelled", "InProgress"): continue
        t = t[:i] + b.replace("9.52.3", "9.52.4").replace("9_52_3", "9_52_4").replace("Template_9523", "Template_9524") + t[j:]; cnt += 1
        extra.append("ex:%s backlog:hasAuditNote %s .\n" % (m, lit("Template reference corrected " + M.now()[:10] + ": the template 9.52.3 was delivered with in-place edits of a committed file (see ex:CR3_TemplateRedo); this item names the new template 9.52.4 (byte-identical content) and the Verify task of its story instead. Text only; the unit has no evidence yet and no criterion is changed in meaning.")))
    assert cnt >= 30, cnt
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_TemplateRedo and the control of the template task (v0.394.0)."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_TemplateRedo").replace("ex:Data3S_TC9_", "ex:Data3S_TC9G_").replace("ex:TC9_", "ex:TC9G_"))
    L = [x.replace("ex:TC9_", "ex:TC9G_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_TemplateRedo", "Obj3_TemplateRedo", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 34 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_TemplateRedo, ex:Spec3I_TemplateRedo_Pass, ex:Spec3I_TemplateRedo_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_TemplateRedo backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_TemplateRedo a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the repair of the in-place edits of the page template 9.52.3"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by one story; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_TemplateRedo and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L) + "".join(extra)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR21", "Out3_ObjectiveR19"), "third lineage, Backlog stage rebuilt: the template repair admitted into the planned Iteration 34 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
