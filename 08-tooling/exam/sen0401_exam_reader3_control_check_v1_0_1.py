#!/usr/bin/env python3
# NEW VERSION of sen0401_exam_reader3_control_check_v1_0_0.py (task TK_Exam_Move_Repoint_Build): the only change is that the exam files removed from the public tree are read from the CME clone (CMEX); no check, bound or rule is changed.
"""sen0401_exam_reader3_control_check v1_0_0 - the lineage agent's own run of the reader of record (v1.2.0, through the measure copy v3_0_0) on 40 synthetic sheets of EACH printed form of papers v3 with seed blocks of the control's own (58000 for form A, 58100 for form B; the executor used 57000 and 57100): with the reader's methods 0 silent wrong, 0 missed, 0 empty not flagged, no registration failure, and at most 25 percent of rows held. Usage: reader3_control_check"""
__version__ = "1.0.0"
import json, os, subprocess, sys
import os as _o, sys as _s
CMEX = '/home/claude/CME/exams/SEN0401/08-tooling/exam'   # the private CME clone: the exam files removed from this public tree are read here
if not _o.path.isdir(CMEX):
    print('NOT_RUN  the CME clone is missing: ' + CMEX + ' (a gate that cannot run is not a pass)'); _s.exit(3)
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(CMEX, "papers_midterm_v3"); ok = True
for F, seed in (("A", 58000), ("B", 58100)):
    b = os.path.join(D, "sen0401_exam_midterm_v3_0_0_form%s_sheet" % F)
    r = subprocess.run([sys.executable, "-B", os.path.join(H, "sen0401_exam_answersheet_measure_v3_0_0.py"), b + ".pdf", b + "_layout.json", "--sheets", "40", "--seed-base", str(seed)], capture_output=True, text=True, timeout=290)
    d = json.loads(r.stdout[r.stdout.index("{"):r.stdout.rindex("}") + 1]); w = d["with_methods"]; n = d["rows_scored"]
    good = d["registration_failures"] == 0 and not any(w.get(k, 0) for k in ("silent_wrong", "missed", "empty_not_flagged")) and w.get("held", 0) <= 0.25 * n
    ok &= good; print("PASS " if good else "FAIL ", "form %s code %s seeds %d-%d: %d rows, with methods %s, registration failures %d, held share %.1f percent" % (F, d["form_code"], seed, seed + 39, n, w, d["registration_failures"], 100.0 * w.get("held", 0) / n))
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
