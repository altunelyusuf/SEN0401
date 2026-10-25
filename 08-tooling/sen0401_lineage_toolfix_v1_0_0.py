#!/usr/bin/env python3
"""sen0401_lineage_toolfix v1_0_0 - corrects an error of the lineage agent made on 2026-10-25: four new control tools were written under the file names sen0401_lineage_control32_v1_0_0.py to control35_v1_0_0.py, names that earlier committed tools of the lineage already carried, so the committed files were EDITED (the rule is that a committed file is never edited; every change is a new file).
Found by the lineage agent itself when writing control36 (git showed the old control36 committed; git log --diff-filter=M listed the four overwrites). Repair, done in the commit of this version: the four old files are restored byte for byte from their last commits before the overwrite (768000a, 1b4f86b, 3e91130, e90c604); the four new tools are committed under
control50, control51, control52, control53 (same content, own names inside); the earlier register records (v0.312.0, v0.314.0, v0.343.0, v0.354.0) hashed the overwritten paths, so this version records NEW ArtifactEvidence for the new paths (bridge-verified), and states the error on the four criteria.
The generated briefs briefs/iter30 and briefs/iter31 were also regenerated over their committed first forms (after the iteration opening); that is stated here too. Usage: no arguments; one new register version."""
__version__ = "1.0.0"
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; REPO = M.REPO
MAP = [("AC9_Ch01Research", "control32", "control50", "v0.312.0", "768000a"), ("AC9_ArcCheck", "control33", "control51", "v0.314.0", "1b4f86b"), ("AC9_ArcLookup", "control34", "control52", "v0.343.0", "3e91130"), ("AC9_Ch12Research", "control35", "control53", "v0.354.0", "e90c604")]
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); files = ["08-tooling/sen0401_lineage_%s_v1_0_0.py" % n for _, _, n, _, _ in MAP]
ver = C.bridge_files(files, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"; L = []
for (crit, old, new, rv, prev), f in zip(MAP, files):
    eid = ver[f][0]; sha = hashlib.sha256(open(os.path.join(REPO, f), "rb").read()).hexdigest()
    L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), crit, f, sha, now))
    note = ("CORRECTION %s UTC by the lineage agent: the control of this criterion (%s) was run with a tool written under the file name sen0401_lineage_%s_v1_0_0.py, a name an earlier committed tool already carried, so that committed file was overwritten (the rule is that a committed file is never edited). "
            "Repaired in the commit of the register version %s: the earlier tool is restored byte for byte from its last commit %s, and the tool that was actually run is committed unchanged as sen0401_lineage_%s_v1_0_0.py, recorded above as new bridge-verified evidence. The results of the control are those printed in %s and stand; only the file name of the tool is corrected. Cause: no check that a new tool name is free; the rule of the lineage agent is now to list the existing files before naming a tool." % (now, rv, old, nxt, prev, new, rv))
    L.append("ex:%s backlog:hasAuditNote %s .\n" % (crit, lit(note)))
L.append('ex:Lineage3 rdfs:comment %s@en .\n' % lit("Error found and repaired %s UTC by the lineage agent: four control tools (control32 to control35) overwrote earlier committed files of the same name; restored and re-homed as control50 to control53 (see the audit notes of ex:AC9_Ch01Research, ex:AC9_ArcCheck, ex:AC9_ArcLookup, ex:AC9_Ch12Research). The generated briefs of Iterations 30 and 31 were regenerated over their first committed forms after the iterations opened; the content differs only in the state of the register they were generated from." % now))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Correction of the overwritten control tools (control32 to control35 restored, control50 to control53 recorded as evidence) stated on the four criteria.")))
