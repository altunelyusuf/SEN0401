#!/usr/bin/env python3
"""sen0401_lineage_revision v1_1_0 - (1.1.0: the reason names the error of the course session and the owner's instruction; the design-level class model and the data concern of the two stories are restored) records, in NEW versions of the SEN0401 slides lineage register, a StageRevision of the third lineage from its Objective stage (never the Mission): its reason, the retraction of the
Objective and Backlog outputs in a commit of its own, then the rebuilt Objective output (now carrying the class model the Backlog stage owes) and the rebuilt Backlog output, which re-admits the same items; the
waiver of the earlier Backlog output is not repeated because the obligation is now met. One call = one new file = one event; the caller validates and commits each alone. Nothing is re-dated or re-recorded: the digests
are computed by the framework's own state_digest for the rebuilt outputs, the retracted outputs and their digests stay in the register as history.
Usage: sen0401_lineage_revision_v1_1_0.py retract | objective PREV_COMMIT | backlog PREV_COMMIT | fill COMMIT
"""
__version__ = "1.1.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X

REV = "ex:Revision_Lineage3_Objective"
REASON = ("The Backlog stage of the third lineage owes a class model of the domain at the analysis level (Ob_Backlog_ClassDiagram, required). The course session closed that stage on 2026-10-18 (register version 0.101) with a waiver of the obligation instead of meeting it, "
          "and dropped the data concern from the two link-pass stories because that concern in turn owes a design-level class model. That was an ERROR of the course session, not a gap of the framework: a requirement of the lineage was bypassed, and it should have been met in the stage that owes it, in the same commit. "
          "The owner's instruction of 2026-10-19: \"If there is a requirement in the lineage you should never bypass it. This is a drift and breaking the rules. You should never do such a thing. And you should do this in time not after the completion of the work.\" "
          "This revision pays the debt: the Objective stage is rebuilt with the analysis-level class model and the design-level class model (the Mission, Scope and Goal outputs stand), the data concern is restored on the two stories, and the Backlog stage is rebuilt after it, re-admitting the same items by admission and not re-dating them, with no waiver. "
          "The earlier outputs and the waiver stay in the register, readable as the dated record of the error. The revision is recorded as decided by the builder role: the owner gave the instruction above, but did not himself decide this revision, and his confirmation of it is listed as open.")
NOTE = ("ERROR of the course session, recorded 2026-10-19: this output was closed on 2026-10-18 with a waiver of the required class-model obligation of the Backlog stage. A requirement of the lineage was bypassed; it should have been met in time. "
        "This output and the Objective output are retracted by the stage revision %s and rebuilt with the model; the waiver on this output stays as the dated record of the error and is not relied on by the rebuilt output." % REV)
CLASS = '''
ex:Model3_Class a backlog:ModelArtifact ; rdfs:label "How a link-pass story and its evidence are stored"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "A Story (the deck link pass or the page link pass) is admitted by the Backlog output of this lineage as a pre-lineage item. It has a start and a finish from git, one TestHarness, one TestEvidence per chapter whose check passed and one ArtifactEvidence per cited file (path and SHA-256). A chapter whose check fails has the hash of its files only and is named in the story. The open tasks of the second lineage are admitted open, each with an executor." ;
    backlog:describesItem ex:Obj3_LinkPassesDone .
'''

CLASS_DESIGN = '''
ex:Model3_ClassDesign a backlog:ModelArtifact ; rdfs:label "Design of the stored link-pass story, its harness and its evidence"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Design ;
    backlog:declaresState "Classes: Story (identifier, title, state, startedAt, finishedAt, lastAuditedAt, executionModality, preLineageItem, admittedByOutput) with associations to AcceptanceCriterion (exactly the criterion of the pass), TestHarness (harnessFor the story, hasHarnessEvidence), TestEvidence (hasTestId, hasTestSpec, hasVerificationMethod, evidenceVerified, verifiedAt) and ArtifactEvidence (hasArtifactPath, hasArtifactSHA256, evidenceVerified, verifiedAt); a StageOutput (hasStateDigest, closedAtCommit) admits the story. A chapter whose check fails has ArtifactEvidence only." ;
    backlog:describesItem ex:Obj3_LinkPassesDone .
'''


def out_r(text, stage, consumes):
    return ('\nex:Out3_%sR a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the third lineage, rebuilt by the stage revision"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;\n    backlog:consumesOutput ex:%s ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, X.digest(text, stage))


def run(ev, t, args):
    if ev == "retract":
        t = X.set_status(t, "LS_Goaled")
        blk = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Objective stage: the class model is paid"@en ;\n'
               '    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Objective ;\n    backlog:revisionReason "%s" ;\n'
               '    backlog:retractsOutput ex:Out3_Objective, ex:Out3_Backlog ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n'
               'ex:Out3_Objective backlog:outputRetracted true .\nex:Out3_Backlog backlog:outputRetracted true .\nex:Out3_Backlog rdfs:comment "%s"@en .\n') % (REV, M.esc(REASON), M.esc(NOTE))
        return t + blk, "StageRevision of the third lineage from the Objective stage: the Objective and Backlog outputs are retracted (the class model owed by the Backlog stage is to be paid); nothing is rebuilt in this version."
    if ev == "objective":
        t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % args[0], t, count=1, flags=re.S)
        t = X.set_status(t, "LS_Objectived"); t += CLASS + CLASS_DESIGN
        t += "".join("ex:%s backlog:hasApplicableConcern backlog:Concern_Data .\n" % x for x in ("ST_Deck_LinkPass", "ST_Page_LinkPass"))
        return t + out_r(t, "Objective", "Out3_Goal"), "third lineage, Objective stage rebuilt by the stage revision: the class model is now part of the stage; the output consumes the Goal output, which stands."
    if ev == "backlog":
        t = re.sub(r'(ex:Out3_ObjectiveR a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"', lambda m: m.group(1) + '"%s"' % args[0], t, count=1, flags=re.S)
        t = X.set_status(t, "LS_Backlogged")
        n = t.count("admittedByOutput ex:Out3_Backlog ;")
        t = t.replace("backlog:admittedByOutput ex:Out3_Backlog ;", "backlog:admittedByOutput ex:Out3_BacklogR ;")
        assert n == 22, n        # 20 open tasks and the 2 link-pass stories, read from the register
        return t + out_r(t, "Backlog", "Out3_ObjectiveR"), "third lineage, Backlog stage rebuilt by the stage revision: the same %d items (20 open tasks, the deck link pass and the page link pass) are re-admitted by the rebuilt output, not re-dated; the class model obligation is met, so no waiver is recorded." % n
    if ev == "fill":
        t = re.sub(r'(ex:Out3_BacklogR a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"', lambda m: m.group(1) + '"%s"' % args[0], t, count=1, flags=re.S)
        return t, "closedAtCommit of the rebuilt Backlog output of the third lineage set to the commit that closed it."
    raise SystemExit("unknown event " + ev)


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    nt, comment = run(sys.argv[1], t, sys.argv[2:])
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


main()
