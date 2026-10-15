#!/usr/bin/env python3
"""sen0401_lineage_migrate_digests v1_0_0 - the stated migration to RS_DigestTable_v4 that the framework's ruling G117 prescribes (response to this register's handover on planning after
the Backlog stage closed). In a NEW register version it (1) declares on the register root that the register adopts RS_DigestTable_v4 (the v3 table without ExecutionTask; the Backlog digest
also covers the pre-lineage items the lineage's own Backlog output admitted), and (2) re-records the stage digests of BOTH lineages with backlog_pipeline_verify's own state_digest under
that table. Each re-recorded output carries a note with the value it replaces. A re-recorded digest witnesses the state of the register at THIS version, not the state at the original close;
the migration says so. No committed version is rewritten. Run backlog_pipeline_verify before and after.

Usage: sen0401_lineage_migrate_digests_v1_0_0.py
"""
__version__ = "1.0.0"
import glob, importlib.util, os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

FW = "/home/claude/Ontologies/backlog-roadmap-framework"
B = M.B


def main():
    spec = importlib.util.spec_from_file_location("pv", sorted(glob.glob(FW + "/03-tooling/backlog_pipeline_verify_v*.py"), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[0]])[-1])
    pv = importlib.util.module_from_spec(spec); spec.loader.exec_module(pv)
    tb = sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"))[-1]
    pv.STAGE_TYPES = pv._load_stage_types(tb, table="v4")
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); now = M.now()
    assert "RS_DigestTable_v4" not in t, "already adopted"
    root = re.search(r"(ex:Backlog a backlog:Backlog ;.*?)( \.)\n", t, re.S)
    t = t[:root.start(2)] + (" ;\n    backlog:adoptsRuleSet backlog:RS_DigestTable_v4 ; backlog:ruleSetAdoptedAt \"%s\"^^xsd:dateTime" % now) + t[root.start(2):]
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    changed = []
    for lin, pfx in (("Lineage", "Out_"), ("Lineage2", "Out2_")):
        luri = rdflib.URIRef(M.BASE + "#" + lin)
        for stage in ("Mission", "Scope", "Goal", "Objective", "Backlog"):
            new = pv.state_digest(g, "Stage_" + stage, luri, admitted=True)
            m = re.search(r'(ex:%s%s a backlog:StageOutput ;.*?backlog:hasStateDigest )"([0-9a-f]+)"' % (pfx, stage), t, re.S)
            assert m, pfx + stage
            old = m.group(2)
            note = ('ex:%s%s rdfs:comment "Digest re-recorded at register version %s (%s) under RS_DigestTable_v4, the stated migration of ruling G117. It witnesses the state of the register at that version, not the state at the original close of this stage. Value replaced: %s%s."@en .\n'
                    % (pfx, stage, nxt, now[:10], old, " (unchanged)" if old == new else ""))
            t = t[:m.start(2)] + new + t[m.end(2):]
            changed.append((lin, stage, old[:12], new[:12])); t += note
    out = M.write_new(src, t, nxt, cur, "Stated migration to the stage digest table v4 (ruling G117): the register adopts it and re-records the stage digests of both lineages; they witness the state at this version, not the original close.")
    for c in changed:
        print(*c)
    print(os.path.basename(out))


main()
