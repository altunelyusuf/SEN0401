#!/usr/bin/env python3
"""sen0401_lineage_revision v1_0_0 - records, in NEW versions of the SEN0401 slides lineage register, a StageRevision of the third lineage from its Objective stage (never the Mission): its reason, the retraction of the
Objective and Backlog outputs in a commit of its own, then the rebuilt Objective output (now carrying the class model the Backlog stage owes) and the rebuilt Backlog output, which re-admits the same items; the
waiver of the earlier Backlog output is not repeated because the obligation is now met. One call = one new file = one event; the caller validates and commits each alone. Nothing is re-dated or re-recorded: the digests
are computed by the framework's own state_digest for the rebuilt outputs, the retracted outputs and their digests stay in the register as history.
Usage: sen0401_lineage_revision_v1_0_0.py retract | objective PREV_COMMIT | backlog PREV_COMMIT | fill COMMIT
"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X

REV = "ex:Revision_Lineage3_Objective"
REASON = ("The Backlog stage of the third lineage owes a class model of the domain at the analysis level, and that obligation was closed on the record with a waiver (register version 0.101) because the model had not been produced at the Objective stage, "
          "where the stage digest table v4 counts a model artifact. This revision pays the debt: the Objective stage is rebuilt with the model (the Mission, Scope and Goal outputs stand), and the Backlog stage is rebuilt after it, re-admitting the same "
          "items by admission and not re-dating them. The waiver was the course session's omission, not a ruling that no model is owed. The revision was asked for through the course coordinator; the owner's own confirmation of it is listed as open in the register's notes, so it is recorded as decided by the builder role and not by the owner.")
CLASS = '''
ex:Model3_Class a backlog:ModelArtifact ; rdfs:label "How a link-pass story and its evidence are stored"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "A Story (the deck link pass or the page link pass) is admitted by the Backlog output of this lineage as a pre-lineage item. It has a start and a finish from git, one TestHarness, one TestEvidence per chapter whose check passed and one ArtifactEvidence per cited file (path and SHA-256). A chapter whose check fails has the hash of its files only and is named in the story. The open tasks of the second lineage are admitted open, each with an executor." ;
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
               'ex:Out3_Objective backlog:outputRetracted true .\nex:Out3_Backlog backlog:outputRetracted true .\n') % (REV, M.esc(REASON))
        return t + blk, "StageRevision of the third lineage from the Objective stage: the Objective and Backlog outputs are retracted (the class model owed by the Backlog stage is to be paid); nothing is rebuilt in this version."
    if ev == "objective":
        t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % args[0], t, count=1, flags=re.S)
        t = X.set_status(t, "LS_Objectived"); t += CLASS
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
