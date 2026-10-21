#!/usr/bin/env python3
"""sen0401_lineage_gap_ch05 v1_0_0 - ONE new register version that records the chapter 5 Stage 3.F repair (research v1.1.1, commit 76d6083) of the third lineage: TK_Gap3F_Ch05_Build Done, TK_Gap3F_Ch05_Verify and
TK_GapS4_Ch05_Verify Done, each ONLY if the evidence bridge verified the evidence it rests on (Stage 4 gate runner v1_1_0 for 05; chapter checks Research/Deck/Page Ch05 v1_3_0; SHA-256 of the files of the repair commits);
then the stories ST_Gap_Stage3F and ST_Gap_Stage4 Done ONLY if every task of each is Done (every criterion then has a passing, bridge-verified run); the title of ST_Gap_Stage3F names chapter 5; dated notes on the Done
epics and the initiative (G125: a Done item stays Done; the gap stories are stories of their own in the third lineage and hang under no epic).
Usage: draft OUT.ttl | record BRIDGE.ttl T0 T1"""
__version__ = "1.0.0"
import hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN = "08-tooling/sen0401_stage4_gates_v1_1_0.py"
CHK = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"
COMMITS = ["76d6083", "7382c65"]
CR = "ex:AC3G_3F_Ch05, ex:AC3G_S4_Ch05"


def sh(*a):
    return subprocess.check_output(a, cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).strip()


def when(c):
    return sh("git", "log", "-1", "--format=%cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", c)


def files():
    out = []
    for c in COMMITS:
        out += [f for f in sh("git", "show", "--name-only", "--format=", c).splitlines() if f and not f.endswith("stage4_status.md")]
    return out


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
    emit("Ev3GE_Gates_Ch05", "T", 'ex:Ev3GE_Gates_Ch05 a backlog:TestEvidence ; rdfs:label "Stage 4 gate run (runner v1_1_0) for Ch05 after research v1.1.1"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "05" ; backlog:hasTestSpec "%s"' % (CR, RUN))
    for k in ("Research", "Deck", "Page"):
        emit("Ev3GE_%s_Ch05" % k, "T", 'ex:Ev3GE_%s_Ch05 a backlog:TestEvidence ; rdfs:label "Chapter check v1_3_0 for %s/Ch05 after research v1.1.1"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s/Ch05" ; backlog:hasTestSpec "%s"' % (k, k, CR, k, CHK))
    for i, f in enumerate(files(), 1):
        h = hashlib.sha256(open(os.path.join(REPO, f), "rb").read()).hexdigest()
        emit("Ev3GE_File_Ch05_%d" % i, "A", 'ex:Ev3GE_File_Ch05_%d a backlog:ArtifactEvidence ; rdfs:label "%s, committed in the chapter 5 Stage 3.F repair"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (i, os.path.basename(f), CR, f, h))
    return out


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1
    j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


ROOT = ("Root cause of the Stage 3.F failure of chapter 5 under the current validator (v1.13.0): the citations are written 'Lightning Labs, 2026a' and 'Lightning Labs, 2026b'; the validator's resolver reads a standalone four-digit year from a source label, "
        "and '2026a' is not one, so 15 citations of sources that WERE in the research data (P20, P21) did not resolve. The pinned validator (v1.6.0) reads it, which is why the chapter check passed while the runner failed. Repair (research v1.1.1, commit 76d6083): "
        "the two labels now end ', retrieved 2026-10-04' (the sources' own verifiedAt); no source was added or invented, no citation or claim removed, no gate, test or threshold changed; the sources were re-fetched and their SHA-256 equal the saved copies.")


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read()
    if sys.argv[1] == "draft":
        pre = "".join(l + "\n" for l in t.splitlines() if l.startswith("@prefix") or l.startswith("PREFIX"))
        open(sys.argv[2], "w", encoding="utf-8").write(pre + "\n" + nodes()); print("draft", sys.argv[2]); return
    vd = S.verdicts(sys.argv[2]); T0, T1 = sys.argv[3], sys.argv[4]
    nxt, cur = M.next_version(src); now = M.now()
    add = nodes(vd)
    tev = [n for n in ["Ev3GE_Gates_Ch05", "Ev3GE_Research_Ch05", "Ev3GE_Deck_Ch05", "Ev3GE_Page_Ch05"] if n in vd and vd[n][0]]
    aev = [n for n in vd if n.startswith("Ev3GE_File_Ch05_") and vd[n][0]]
    nfiles = len(files())
    if "Ev3GE_Gates_Ch05" not in tev or len(tev) < 4 or len(aev) != nfiles:
        sys.exit("bridge did not verify everything: %s %d/%d" % (tev, len(aev), nfiles))
    fin = when("76d6083")
    # Build task
    i, j = blk(t, "TK_Gap3F_Ch05_Build"); b = t[i:j]
    m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
    t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, now), 1) + t[j:]
    ev = ", ".join("ex:" + x for x in tev + aev)
    add += 'ex:Harness3GE_TK_Gap3F_Ch05_Build a backlog:TestHarness ; rdfs:label "Gate and chapter checks for TK_Gap3F_Ch05_Build"@en ; backlog:harnessFor ex:TK_Gap3F_Ch05_Build ; backlog:hasHarnessEvidence %s .\n' % ", ".join("ex:" + x for x in tev)
    add += ('ex:TK_Gap3F_Ch05_Build backlog:hasAcceptanceCriterion ex:AC3G_3F_Ch05 ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote "Done, recorded %s: the repair commit is 76d6083 (%s UTC), research v1.1.1, written by the chapter 5 work agent. %s The evidence bridge ran from %s to %s UTC the Stage 4 gate runner for 05 and the chapter checks Research, Deck and Page of Ch05 (all exit 0) and verified the SHA-256 of the %d files of the repair commits." .\n'
            % (ev, now[:10], fin, ROOT, T0, T1, nfiles))
    # Verify tasks
    for vid, ac in (("TK_Gap3F_Ch05_Verify", "AC3G_3F_Ch05"), ("TK_GapS4_Ch05_Verify", "AC3G_S4_Ch05")):
        i, j = blk(t, vid); b = t[i:j]
        assert "backlog:hasState backlog:Proposed" in b, vid
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (T0, T1, now), 1) + t[j:]
        add += 'ex:Harness3GE_%s a backlog:TestHarness ; rdfs:label "Gate and chapter checks for %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (vid, vid, vid, ", ".join("ex:" + x for x in tev))
        add += ('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote "Done, recorded %s: the evidence bridge ran from %s to %s UTC, after research v1.1.1, the Stage 4 gate runner v1_1_0 for 05 (exit 0: Stage3.F with 36 citations verified, Stage4.A, B, cov, sub and src as the runner reports them; NOT_MEASURED and CANNOT_RUN gates are reported by the runner and are not claimed) and the chapter checks Research/Ch05, Deck/Ch05 and Page/Ch05 (exit 0; the page tests use a TEST release key and prove page logic only). Both validators now pass: the current one (runner) and the pinned one (chapter check). The criterion has a passing run." .\n'
                % (vid, ac, ", ".join("ex:" + x for x in tev + aev), now[:10], T0, T1))
    # stories
    def fin_of(b):
        return re.search(r'backlog:finishedAt "([^"]*)"', b).group(1)
    for sid, tsk_pat in (("ST_Gap_Stage3F", "TK_Gap3F_"), ("ST_Gap_Stage4", "TK_GapS4_")):
        i, j = blk(t, sid); b = t[i:j]
        tasks = re.search(r'backlog:decomposesInto ([^;]*?)(?:;|\n)', b).group(1).replace(" ", "").split(",")
        tasks = [x.replace("ex:", "") for x in tasks]
        fins = []
        for tk in tasks:
            a, z = blk(t, tk)
            assert "backlog:hasState backlog:Done" in t[a:z], "not Done: " + tk
            fins.append(fin_of(t[a:z]))
        last = max(fins)
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
        b2 = b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), last, now), 1)
        if sid == "ST_Gap_Stage3F":
            b2 = b2.replace("of chapter 1 and Bitcoin in numbers", "of chapters 1 and 5 and Bitcoin in numbers").replace("of chapter 1 and of Bitcoin in numbers", "of chapters 1 and 5 and of Bitcoin in numbers")
            units = ["Ch01", "Numbers", "Ch05"]
        else:
            units = ["Ch01", "Ch02", "Ch03", "Ch04", "Ch05", "Ch06", "Ch07", "Numbers"]
        t = t[:i] + b2 + t[j:]
        gev = ["Ev3GD_Gates_" + u for u in units if "ex:Ev3GD_Gates_%s a " % u in t] + ["Ev3GE_Gates_Ch05"]
        add += 'ex:Harness3GE_%s a backlog:TestHarness ; rdfs:label "Gate runs for %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (sid, sid, sid, ", ".join("ex:" + x for x in gev))
        add += ('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote "Done, recorded %s, G125 (a story is Done when every criterion of it is satisfied): all %d tasks are Done and the Verify task of each criterion has a passing, bridge-verified run (the last task finished %s UTC). The story finishes at its last task. Gates the runner reports NOT_MEASURED or CANNOT_RUN are not claimed; the page tests use a TEST release key. The Mission outcome, the closure report and the achievement of the lineage are the owner\'s and are not recorded here." .\n'
                % (sid, ", ".join("ex:" + x for x in gev), now[:10], len(tasks), last))
        add = add.replace(" ", " ")
    for obj, met, val, what in (("Obj3_Stage3FPass", "Met3_Stage3FPass", "3", "Stage 3.F passes for chapter 1 (30 citations verified), Bitcoin in numbers (6) and chapter 5 (36) under the Stage 4 gate runner (current validator): 3 of 3"),
                                ("Obj3_Stage4Pass", "Met3_Stage4Pass", "8", "the Stage 4 gate run of chapters 1 to 7 and Bitcoin in numbers exits 0 with no failing gate: 8 of 8")):
        add += ('ex:Obs38_%s a backlog:MetricObservation ; rdfs:label "Reading after the chapter 5 repair, from the bridge-verified runs"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%s"^^xsd:decimal ;\n    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;\n    backlog:hasObservationMethod "Read %s from the evidence-bridge runs of v0.134 and v0.136: %s." .\n' % (obj, met, obj, val, now, now[:10], what))
    add += ('ex:Init_Slides backlog:hasAuditNote "Note %s: the stage revisions of the third lineage added stories (ST_Gap_Stage3F, ST_Gap_Stage4) to the third lineage, not to this initiative or its epics; they hang under no epic. G125: a Done item stays Done and the record of what it was is not edited; work after it is a story of its own. This item therefore stays Done and has no open child." .\n' % now[:10])
    for e in ("EP_Deck", "EP_Research", "EP_Page"):
        add += 'ex:%s backlog:hasAuditNote "Note %s: the gap stories of the third lineage (ST_Gap_Stage3F, ST_Gap_Stage4) are stories of their own and are not children of this epic. G125: a Done item stays Done; it has no open child." .\n' % (e, now[:10])
    out = M.write_new(src, t + "\n" + add, nxt, cur, "Chapter 5 Stage 3.F repair recorded on bridge-verified evidence: TK_Gap3F_Ch05_Build, TK_Gap3F_Ch05_Verify, TK_GapS4_Ch05_Verify Done; ST_Gap_Stage3F and ST_Gap_Stage4 Done (all criteria verified); notes on the Done epics and initiative.")
    print(os.path.basename(out))


main()
