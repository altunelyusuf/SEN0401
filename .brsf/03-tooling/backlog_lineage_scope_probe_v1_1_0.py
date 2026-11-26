#!/usr/bin/env python3
"""backlog_lineage_scope_probe v1.1.0 (Lineage 33, box 66; v1.1.0 after review r1: faults on checkpoints, observations and gaps, on the records the box tool writes, and a pyshacl that fails): a step checked against a lineage's own records (the box tool's `--scope lineage`) still refuses what the whole-register check refuses on that lineage, and is fast.
Usage: probe REGISTER [--lineage L_SimplifiedProfile]. Cases, each on a scratch copy of the register: the register as it is holds no violation on the lineage; each planted fault (an objective with no checkpoint, a story with no responsible executor, a stage output that consumes nothing) is named by the lineage-scope check; a lineage-scope check ends within 180 seconds; the generated chain's fingerprints reproduce; the box tool refuses a scope that is neither `lineage` nor `register`; the box tool reads the validator's lineage output. Exit 0 when every case holds."""
import os, re, sys, glob, time, shutil, subprocess, tempfile, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
def newest(stem):
    return sorted(glob.glob(os.path.join(HERE, stem + "_v*.py")), key=lambda f: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", f)[0]])[-1]
if sys.argv[1:] == ["--deps"]:
    for s in ("backlog_validate", "backlog_box_step", "backlog_pipeline_verify"): print(newest(s))
    print(os.path.abspath(__file__)); sys.exit(0)
REG = sys.argv[1]; LIN = sys.argv[sys.argv.index("--lineage") + 1] if "--lineage" in sys.argv else "L_SimplifiedProfile"
VAL, BOX, PV = newest("backlog_validate"), newest("backlog_box_step"), newest("backlog_pipeline_verify")
FAILS = []; N = [0]
def expect(what, ok, extra=""):
    N[0] += 1
    if not ok: FAILS.append(what); print("FAIL ", what, extra)
def lineage_check(path):
    t0 = time.time(); r = subprocess.run([sys.executable, "-B", VAL, path, "--validate-lineage", LIN], capture_output=True, text=True)
    return r.stdout, time.time() - t0
text = open(REG, encoding="utf-8").read()
def planted(old, new):
    assert text.count(old) >= 1, old
    d = tempfile.mkdtemp(); p = os.path.join(d, "register.ttl"); open(p, "w", encoding="utf-8").write(text.replace(old, new, 1)); return p
out, secs = lineage_check(REG)
expect("the register as it is holds no violation on the lineage", "0 Violation" in out, out[-300:])
expect("a lineage-scope check ends within 180 seconds", secs < 180, "%.0f s" % secs)
faults = [("an objective with no checkpoint is named", "backlog:hasCheckpoint fw:CP_SPR_Mission ;", "", "Obj_SPR_Mission"),
          ("a story with no responsible executor is named", "    backlog:responsible fw:Run_SPR_0_Builder ;\n    backlog:hasReach 5.0", "    backlog:hasReach 5.0", "ST_SPR_Seed"),
          ("a stage output that consumes nothing is named", "backlog:consumesOutput fw:Out_Mission_SimplifiedProfile ;", "", "Out_Scope_SimplifiedProfile")]
for what, old, new, focus in faults:
    p = planted(old, new); o, _ = lineage_check(p); shutil.rmtree(os.path.dirname(p))
    expect(what, "1 Violation" in o and focus in o, o[-300:])
more = [("a checkpoint with no date is named", "backlog:checkpointDate \"2026-11-27T00:00:00Z\"^^xsd:dateTime .", ".", "CP_SPR_Mission"),
        ("an observation with no value is named", "backlog:hasObservedValue 250.0 ;", "", "Obs_SPR_Mission"),
        ("a plan baseline written by the box tool with no time is named", "backlog:baselinedAt \"2026-11-24T16:16:46Z\"^^xsd:dateTime ;", "", "PB_SPR_66"),
        ("a gap with no reason is named", "backlog:hasGapReason \"Not yet in use: the template tool is built in this lineage and used live only after its proof.\" .", ".", "Gap_SPR_ActiveUse")]
for what, old2, new2, focus in more:
    p = planted(old2, new2) if text.count(old2) else None
    if p is None:
        expect(what + " (the planted text exists)", False, old2[:60]); continue
    o, _ = lineage_check(p); shutil.rmtree(os.path.dirname(p))
    expect(what, "1 Violation" in o and focus in o, o[-300:])
d = tempfile.mkdtemp(); os.makedirs(os.path.join(d, "pyshacl")); open(os.path.join(d, "pyshacl", "__init__.py"), "w").write("")
open(os.path.join(d, "pyshacl", "__main__.py"), "w").write("import sys; sys.exit(1)\n")
env = dict(os.environ, PYTHONPATH=d + os.pathsep + os.environ.get("PYTHONPATH", ""))
r = subprocess.run([sys.executable, "-B", VAL, REG, "--validate-lineage", LIN], capture_output=True, text=True, env=env); shutil.rmtree(d)
expect("a pyshacl that fails is not read as a clean report", r.returncode == 2 and "safe profile source" not in r.stdout, r.stdout[-200:])
r = subprocess.run([sys.executable, "-B", PV, REG, "--lineage", LIN], capture_output=True, text=True)
expect("the fingerprints of the generated chain reproduce", "VERDICT     : PASS" in r.stdout, r.stdout[-300:])
sp = importlib.util.spec_from_file_location("boxstep", BOX); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
sample = "VALIDATE-LINEAGE: X\ncounts      : 1 Violation, 0 Warning, 0 Info\n  - Violation http://example.org/x#A: L1: a thing.\nVERDICT     : NOT a safe profile source\n"
expect("the box tool reads the validator's lineage output", m.parse_lineage_violations(sample) == {("http://example.org/x#A", "L1: a thing.")}, str(m.parse_lineage_violations(sample)))
r = subprocess.run([sys.executable, "-B", BOX, REG, "--scope", "everything", "owes", "LS_InProgress"], capture_output=True, text=True)
expect("the box tool refuses a scope that is neither lineage nor register", "REFUSED" in r.stdout, r.stdout[-200:])
print("VERDICT: %s -- %d expectations %s" % ("PASS" if not FAILS else "FAIL", N[0], "hold" if not FAILS else "(%d failed)" % len(FAILS)))
sys.exit(1 if FAILS else 0)
