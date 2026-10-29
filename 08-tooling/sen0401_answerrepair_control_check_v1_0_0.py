#!/usr/bin/env python3
"""sen0401_answerrepair_control_check v1_0_0 - the lineage agent's OWN control of TK_Exam_AnswerMethods_Repair_Build.
Usage: KIND [COMMIT]   KIND: rerun | blocks | nochange COMMIT. Exit 0 only when met.
`blocks` draws THREE seed blocks of 200 sheets at control time (random, printed in the log), none overlapping the calibration seeds 1000-1099 and 2000-2199, the executor's evaluation seeds 9000-9199 and 31000-31199,
or the control's earlier blocks (30000-30199, 40000-40199, 50000-50199), applies the executor's criteria of check v1.1.0 (the C6 criteria of v1.0.0 unchanged, plus zero marks read as empty without a flag) to the v1.1.0 reader,
and reports the v1.0.0 reader on the same blocks for comparison (information, not a criterion)."""
import json, os, random, re, secrets, subprocess, sys
R = "/home/claude/sen0401/"; X = R + "08-tooling/exam/"; sys.path.insert(0, X); sys.dont_write_bytecode = True
USED = [(1000, 100), (2000, 200), (9000, 200), (31000, 200), (30000, 200), (40000, 200), (50000, 200)]
def rerun():
    r = subprocess.run([sys.executable, "-B", X + "sen0401_exam_answersheet_check_v1_1_0.py"], capture_output=True, text=True, cwd=R); out = r.stdout
    log = open(X + "sen0401_exam_answersheet_check_log_v1_1_0.txt").read(); keys = lambda s: [re.sub(r"\s+", " ", l) for l in s.splitlines() if l.startswith(("PASS", "FAIL", "SUMMARY"))]
    same = keys(out) == keys(log); print("executor's check v1.1.0 re-run by the control: exit %d, %s; PASS/FAIL lines equal the committed log: %s" % (r.returncode, [l for l in out.splitlines() if l.startswith("SUMMARY")], same))
    return r.returncode == 0 and same
def pick():
    rng = secrets.SystemRandom(); out = []
    while len(out) < 3:
        b = rng.randrange(100000, 900000)
        if all(b + 200 <= u or u + n <= b for u, n in USED) and all(abs(b - o) >= 200 for o in out): out.append(b)
    return out
def blocks():
    import sen0401_exam_answersheet_measure_v1_0_0 as M0, sen0401_exam_answersheet_measure_v1_1_0 as M1
    ok = True; bl = pick(); print("control's seed blocks drawn at control time (200 sheets each): %s" % bl)
    for b in bl:
        e = M1.run(200, b); o = M0.run(200, b, samples=None)
        wm, nv, pk = e["with_methods"], e["naive_reader"], e["per_kind_with_methods"]; share = e["recoverable_rows_held_by_a_flag"] / e["recoverable_rows"]; slip = pk.get("code_slip", {}); swap = pk.get("code_swap", {})
        c = {"registration failures 0": e["registration_failures"] == 0, "silent wrong 0": wm.get("silent_wrong", 0) == 0, "missed 0": wm.get("missed", 0) == 0, "every slip detected": slip.get("detected", 0) == sum(slip.values()),
             "every swap detected": swap.get("detected", 0) == sum(swap.values()), "reader without methods fails at least once": nv.get("silent_wrong", 0) + nv.get("missed", 0) > 0, "held share <= 25%": share <= 0.25, "unflagged empty reads 0": wm.get("empty_not_flagged", 0) == 0}
        bad = [k for k, v in c.items() if not v]; ok &= not bad; ow = o["with_methods"]; osh = o["recoverable_rows_held_by_a_flag"] / o["recoverable_rows"]
        print("block %d: v1.1.0 silent wrong %d, missed %d, unflagged empty %d, held %.1f%% (%d of %d recoverable rows), registration failures %d; criteria not met: %s | v1.0.0 reader on the same block: silent wrong %d, missed %d, unflagged empty %d, held %.1f%%" % (
            b, wm.get("silent_wrong", 0), wm.get("missed", 0), wm.get("empty_not_flagged", 0), 100 * share, e["recoverable_rows_held_by_a_flag"], e["recoverable_rows"], e["registration_failures"], bad,
            ow.get("silent_wrong", 0), ow.get("missed", 0), ow.get("empty_not_flagged", 0), 100 * osh))
        print("   held rows by flag kind (v1.1.0) %s; thresholds %s" % (e["recoverable_rows_held_by_flag_kind"], e["thresholds"]))
    return ok
def nochange(c):
    st = [l for l in subprocess.run(["git", "-C", R, "show", "--name-status", "--format=", c], capture_output=True, text=True).stdout.split("\n") if l]
    notnew = [l for l in st if not l.startswith("A\t")]; out = [l for l in st if not l.split("\t")[1].startswith("08-tooling/exam/")]
    print("commit %s: %d files, all added: %s; all under 08-tooling/exam/: %s" % (c, len(st), not notnew, not out)); return bool(st) and not notnew and not out
k = sys.argv[1]; ok = {"rerun": rerun, "blocks": blocks, "nochange": lambda: nochange(sys.argv[2])}[k]()
print("RESULT", "MET" if ok else "NOT MET"); sys.exit(0 if ok else 1)
