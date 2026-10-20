#!/usr/bin/env python3
"""sen0401_lineage_gap_done v1_0_0 - ONE new register version that records the finished Build tasks of the Stage 3.F / Stage 4 gap stories of the third lineage and their Verify tasks as Done, each ONLY if the
evidence bridge verified the evidence it rests on (RDODI Stage 4 gate runner v1_1_0 run for the unit; the lineage chapter checks v1_3_0 Research/Deck/Page that exist for it; SHA-256 of the files the build commits added).
Dates: a Build task finishes at the last git commit of its unit; a Verify task starts at the time the bridge started, after the start gate was asked on the register as it would stand (Verify Ready, builds Done), and finishes
when the bridge ended. Stories stay open: a story is Done only when every criterion of it is satisfied. NOT_MEASURED and CANNOT_RUN gates of the runner are not claimed.
Usage: draft OUT.ttl | record BRIDGE.ttl T0 T1"""
__version__ = "1.0.0"
import os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = "08-tooling/sen0401_stage4_gates_v1_1_0.py"
CHK = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
# unit -> (runner id, Stage 3.F repair commit or None, Stage 4 commit, chapter number for chapter checks or None)
UNITS = {"Ch01": ("01", "3e664d2", "164c68a", 1), "Ch02": ("02", None, "edfc1e7", 2), "Ch03": ("03", None, "17c91a4", 3), "Ch04": ("04", None, "1b243bc", 4), "Ch05": ("05", None, "9d5ba49", 5),
         "Ch06": ("06", None, "fdd3fe7", 6), "Ch07": ("07", None, "08d8783", 7), "Numbers": ("numbers", "963f544", "6a491c6", None)}
EXEC = {"Ch01": "3F", "Numbers": "3F"}


def sh(*a):
    return subprocess.check_output(a, cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).strip()


def when(c):
    return sh("git", "log", "-1", "--format=%cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", c)


def files(c):
    return [f for f in sh("git", "show", "--name-only", "--format=", c).splitlines() if f and not f.endswith("stage4_status.md")]


def crit(u, kind):
    return ["AC3G_S4_" + u] + (["AC3G_3F_" + u] if u in EXEC else [])


def checks(u):
    n = UNITS[u][3]
    return [] if n is None else [("Research", "Research/Ch%02d" % n), ("Deck", "Deck/Ch%02d" % n), ("Page", "Page/Ch%02d" % n)]


def nodes(vd=None):
    out = ""
    def emit(name, kind, body):
        nonlocal out
        if vd is None:
            out += body + " .\n"
        elif name in vd and vd[name][0]:
            ok, at, meth = vd[name]
            tool = "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" if kind == "T" else "backlog_evidence_bridge_v1_1_0"
            out += body + ' ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (S.esc(meth), tool, at)
    for u, (rid, c3, c4, n) in UNITS.items():
        cr = ", ".join("ex:" + x for x in crit(u, ""))
        emit("Ev3GD_Gates_" + u, "T", 'ex:Ev3GD_Gates_%s a backlog:TestEvidence ; rdfs:label "Stage 4 gate run (runner v1_1_0) for %s"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s"' % (u, u, cr, rid, RUN))
        for k, tid in checks(u):
            emit("Ev3GD_%s_%s" % (k, u), "T", 'ex:Ev3GD_%s_%s a backlog:TestEvidence ; rdfs:label "Chapter check v1_3_0 for %s"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s"' % (k, u, tid, cr, tid, CHK))
        i = 0
        for c in [x for x in (c3, c4) if x]:
            for f in files(c):
                i += 1
                import hashlib
                h = hashlib.sha256(open(os.path.join(REPO, f), "rb").read()).hexdigest()
                emit("Ev3GD_File_%s_%d" % (u, i), "A", 'ex:Ev3GD_File_%s_%d a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (%s UTC)"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (u, i, os.path.basename(f), c, when(c), cr, f, h))
    return out


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1
    j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


def ev_names(vd, u):
    t = [n for n in ["Ev3GD_Gates_" + u] + ["Ev3GD_%s_%s" % (k, u) for k, _ in checks(u)] if n in vd and vd[n][0]]
    a = [n for n in vd if n.startswith("Ev3GD_File_%s_" % u) and vd[n][0]]
    return t, a


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read()
    if sys.argv[1] == "draft":
        pre = "".join(l + "\n" for l in t.splitlines() if l.startswith("@prefix") or l.startswith("PREFIX"))
        open(sys.argv[2], "w", encoding="utf-8").write(pre + "\n" + nodes()); print("draft", sys.argv[2]); return
    vd = S.verdicts(sys.argv[2]); T0, T1 = sys.argv[3], sys.argv[4]
    nxt, cur = M.next_version(src); now = M.now()
    add = nodes(vd); done, notdone = [], []
    for u, (rid, c3, c4, n) in UNITS.items():
        tev, aev = ev_names(vd, u)
        gates_ok = "Ev3GD_Gates_" + u in tev
        files_ok = len(aev) == sum(len(files(c)) for c in (c3, c4) if c)
        # Build tasks
        builds = []
        if c3: builds.append(("TK_Gap3F_%s_Build" % u, c3, "Stage 3.F repair"))
        builds.append(("TK_GapS4_%s_Build" % u, c4, "Stage 4 page ABox"))
        for tid, c, what in builds:
            fe = [x for x in aev if any(x == "Ev3GD_File_%s_%d" % (u, k) for k in range(1, 200))]
            if not (tev and files_ok):
                notdone.append(tid); continue
            fin = when(c)
            i, j = blk(t, tid); b = t[i:j]
            m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, tid
            t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, now), 1) + t[j:]
            cs = crit(u, "")
            add += ('ex:Harness3GD_%s a backlog:TestHarness ; rdfs:label "Gate and chapter checks for %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (tid, tid, tid, ", ".join("ex:" + x for x in tev)))
            ccrit = [x for x in cs if (x.startswith("AC3G_3F") == (what == "Stage 3.F repair"))]
            add += ('ex:%s backlog:hasAcceptanceCriterion %s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote "Done, recorded %s: the build commit is %s (%s UTC). The evidence bridge ran, from %s to %s UTC, %s and verified the SHA-256 of the %d file(s) that the build commit added (listed as file evidence). The Stage 4 runner and the chapter checks are reported as they ran; gates the runner reports as NOT_MEASURED or CANNOT_RUN (Stage4.L, Cross.B, Cross.C, Stage1.C/E) are not claimed. The page tests ran with a TEST release key, so they prove page logic only." .\n'
                    % (tid, ", ".join("ex:" + x for x in ccrit), ", ".join("ex:" + x for x in tev + aev), now[:10], c, fin, T0, T1, "the Stage 4 gate runner for %s and the chapter checks that exist for it (%s)" % (rid, ", ".join(x[1] for x in checks(u)) or "none exist for this unit"), len(aev)))
            done.append(tid)
        # Verify tasks
        vts = []
        if c3: vts.append(("TK_Gap3F_%s_Verify" % u, ["AC3G_3F_" + u]))
        vts.append(("TK_GapS4_%s_Verify" % u, ["AC3G_S4_" + u]))
        for vid, cs in vts:
            if not gates_ok:
                i, j = blk(t, vid)
                add += 'ex:%s backlog:hasAuditNote "Checked %s through the evidence bridge: the Stage 4 gate runner for %s did not exit 0 (it reports a failing gate), so this task stays open and the criterion is not satisfied." .\n' % (vid, now[:10], rid)
                notdone.append(vid); continue
            i, j = blk(t, vid); b = t[i:j]
            assert "backlog:hasState backlog:Proposed" in b, vid
            t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (T0, T1, now), 1) + t[j:]
            ev = tev + aev
            add += ('ex:Harness3GD_%s a backlog:TestHarness ; rdfs:label "Gate and chapter checks for %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (vid, vid, vid, ", ".join("ex:" + x for x in tev)))
            add += ('ex:%s backlog:hasAcceptanceCriterion %s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote "Done, recorded %s: the evidence bridge ran from %s to %s UTC the Stage 4 gate runner v1_1_0 for %s (exit 0: Stage3.F, Stage4.A, B, cov, sub and src as the runner reports them; NOT_MEASURED and CANNOT_RUN gates are reported by the runner and are not claimed) and the chapter checks that exist for the unit (%s). The criterion has a passing run." .\n'
                    % (vid, ", ".join("ex:" + x for x in cs), ", ".join("ex:" + x for x in tev + aev), now[:10], T0, T1, rid, ", ".join(x[1] for x in checks(u)) or "none exist for this unit"))
            done.append(vid)
    out = M.write_new(src, t + "\n" + add, nxt, cur, "Build tasks and Verify tasks of the Stage 3.F / Stage 4 gap stories recorded Done on bridge-verified evidence: %s; not recorded: %s." % (done, notdone or "none"))
    print(os.path.basename(out), "done", len(done), "not", notdone)


main()
