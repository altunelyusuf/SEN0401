#!/usr/bin/env python3
"""backlog_release_preflight_probe v1.2.0 -- proof that the release tool's preflight sees a handover that arrived on origin, before the gate (G151)."""
import glob, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sv = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", p)[0]]
tool = sorted(glob.glob(os.path.join(HERE, "backlog_release_tool_v*.py")), key=sv)[-1]
if sys.argv[1:] == ["--deps"]:
    print(os.path.abspath(__file__)); print(tool); sys.exit(0)
bad = []
def expect(n, ok):
    print(("PASS  " if ok else "FAIL  ") + n)
    if not ok: bad.append(n)
def git(d, *a): return subprocess.run(["git", "-c", "user.email=p@p", "-c", "user.name=p", *a], cwd=d, capture_output=True, text=True, check=True).stdout
with tempfile.TemporaryDirectory() as t:
    git(t, "init", "-q", "--bare", "origin.git")
    for who in ("a", "b"):
        git(t, "clone", "-q", "origin.git", who)
    a, b = os.path.join(t, "a"), os.path.join(t, "b")
    pkg = os.path.join(a, "backlog-roadmap-framework")
    os.makedirs(pkg + "/03-tooling"); os.makedirs(pkg + "/07-handover-inbox/pending"); os.makedirs(pkg + "/04-documentation")
    shutil.copy(tool, pkg + "/03-tooling/" + os.path.basename(tool))
    open(pkg + "/07-handover-inbox/pending/README.md", "w").write("r\n"); open(pkg + "/VERSION.txt", "w").write("1.0.0\n"); open(pkg + "/03-tooling/thing_v1_0_0.py", "w").write("a\n")
    open(pkg + "/04-documentation/CHANGELOG_v1_1_0.md", "w").write("## v1.0.1 — x\n")
    git(a, "add", "-A"); git(a, "commit", "-q", "-m", "base"); git(a, "push", "-q", "origin", "HEAD:main")
    run = lambda: subprocess.run([sys.executable, "-B", pkg + "/03-tooling/" + os.path.basename(tool), "preflight", "1.0.1"], capture_output=True, text=True, cwd=pkg).stdout
    out = run()
    expect("no arrival: preflight does not name a handover", "handover(s) on origin" not in out)
    git(b, "pull", "-q", "origin", "main"); os.makedirs(b + "/backlog-roadmap-framework/07-handover-inbox/pending", exist_ok=True)
    open(b + "/backlog-roadmap-framework/07-handover-inbox/pending/HANDOVER_x_to_y_z_v1_0_0.md", "w").write("q\n")
    git(b, "add", "-A"); git(b, "commit", "-q", "-m", "arrives"); git(b, "push", "-q", "origin", "HEAD:main")
    out = run()
    expect("a handover pushed to origin is named, and preflight stops", "HANDOVER_x_to_y_z_v1_0_0.md" in out and "STOP" in out)
    git(a, "pull", "-q", "origin", "main")
    expect("once pulled into the working tree it is no longer an arrival", "HANDOVER_x_to_y_z" not in run().split("preflight")[0])
    os.makedirs(a + "/backlog-roadmap-framework/07-handover-inbox/accepted", exist_ok=True)
    git(a, "mv", "backlog-roadmap-framework/07-handover-inbox/pending/HANDOVER_x_to_y_z_v1_0_0.md", "backlog-roadmap-framework/07-handover-inbox/accepted/HANDOVER_x_to_y_z_v1_0_0.md")
    expect("a handover dispositioned here (moved to accepted/, not yet pushed) is not an arrival", "HANDOVER_x_to_y_z" not in run().split("preflight")[0])
    open(pkg + "/03-tooling/thing_v1_0_0.py", "w").write("changed\n")
    expect("a published versioned file changed under its own name is refused before the gate (BP-D7)", "thing_v1_0_0.py" in run() and "keeps its versioned name" in run())
# the vocabulary probe (Lineage 29): a failing one stops the preflight, a passing one is silent, and the planted faults of the tool are caught
VOC = lambda code: "import sys\nprint('vocabulary probe: ' + ('PASS' if %d == 0 else 'FAIL'))\nsys.exit(%d)\n" % (code, code)
def has_onts(pk): os.makedirs(pk + "/01-ontologies", exist_ok=True)
def voc_run(toolpath, code):
    with tempfile.TemporaryDirectory() as t2:
        git(t2, "init", "-q", "--bare", "origin.git"); git(t2, "clone", "-q", "origin.git", "a"); a2 = os.path.join(t2, "a"); pk = os.path.join(a2, "backlog-roadmap-framework")
        os.makedirs(pk + "/03-tooling"); os.makedirs(pk + "/04-documentation"); shutil.copy(toolpath, pk + "/03-tooling/" + os.path.basename(toolpath))
        open(pk + "/VERSION.txt", "w").write("1.0.0\n"); open(pk + "/04-documentation/CHANGELOG_v1_1_0.md", "w").write("## v1.0.1 — x\n")
        open(pk + "/03-tooling/backlog_vocabulary_probe_v1_0_0.py", "w").write(VOC(code)); has_onts(pk)
        git(a2, "add", "-A"); git(a2, "commit", "-q", "-m", "base"); git(a2, "push", "-q", "origin", "HEAD:main")
        return subprocess.run([sys.executable, "-B", pk + "/03-tooling/" + os.path.basename(toolpath), "preflight", "1.0.1"], capture_output=True, text=True, cwd=pk).stdout
def voc_cases(toolpath):
    o3 = voc_run(toolpath, 3)
    return ("vocabulary probe fails" in o3 and "exit 3" in o3 and "vocabulary probe: FAIL" in o3, "vocabulary probe fails" not in voc_run(toolpath, 0), "vocabulary probe fails" in voc_run(toolpath, 1))
f, ok, crash = voc_cases(tool)
expect("a failing vocabulary probe stops the preflight and names it", f)
expect("a passing vocabulary probe is silent", ok)
expect("a failing vocabulary probe is named with its exit code and its last line, and a crash (exit 1) stops the preflight too", crash)
for what, old, new in (("the vocabulary probe is not run", "vp = newest(os.path.join(HERE, \"backlog_vocabulary_probe_v*.py\"))", "vp = None"), ("its failure is not reported", "bad.append(\"the vocabulary probe fails", "(lambda *a: None)(\"the vocabulary probe fails"), ("only exit code 3 is reported", "if r.returncode != 0:\n            tail", "if r.returncode == 3:\n            tail"), ("the last line is dropped from the message", "(exit %d; it takes about 6 s here and would refuse after the long gate): %s\" % (r.returncode, tail)", "(exit %d; it takes about 6 s here and would refuse after the long gate)\" % r.returncode")):
    src = open(tool, encoding="utf-8").read()
    if old not in src:
        expect("mutant text found: " + what, False); continue
    with tempfile.TemporaryDirectory() as md:
        mp = os.path.join(md, os.path.basename(tool)); open(mp, "w", encoding="utf-8").write(src.replace(old, new, 1))
        mf, _, mc = voc_cases(mp)
    expect("mutant caught: " + what, not (mf and mc))
# the gate's number-origin and doc-coverage sections (Lineage 29, box 62). Both checkers are put through the SAME cases, so no fault can hide on one side:
# a failing exit (1, 2, 3, 7) is named with its code and verdict line; a pass is silent; a hang is a refusal naming the checker that hung; the newest version is chosen by number
# (not by text, not by file time, not the oldest); the arguments are exactly the gate's; both failing names both; no ontologies folder runs neither.
KINDS = (("number origin", "backlog_number_origin", ["--strict"]), ("doc coverage", "backlog_doc_coverage_gate", []))
VARIANTS = {
    "stderr": lambda args: "import sys\nif sys.argv[1:] == %r:\n    sys.stderr.write('FATAL: planted on stderr\\n')\n    sys.exit(1)\n" % (args,),
    "passfail": lambda args: "import sys\nprint('no FAIL here, all FAIL checks pass')\nsys.exit(0)\n",
    "verdictmix": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('FAIL early detail')\n    print('VERDICT: FAIL - final')\n    print('note: done')\n    sys.exit(1)\n" % (args,),
    "bothchannels": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('VERDICT: FAIL - on stdout', flush=True)\n    sys.stderr.write('VERDICT: FAIL - on stderr\\n')\n    sys.exit(1)\n" % (args,),
    "failtail": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('VERDICT: FAIL - first')\n    print('FAIL: detail last')\n    sys.exit(1)\n" % (args,),
    "verdicttail": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('FAIL early detail')\n    print('VERDICT: REFUSED')\n    sys.exit(1)\n" % (args,),
    "nofail": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('alpha')\n    print('beta')\n    sys.exit(1)\n" % (args,),
    "lowercase": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('VERDICT: FAIL - real')\n    print('the failing detail in lower case')\n    sys.exit(1)\n" % (args,),
    "passstderr": lambda args: "import sys\nsys.stderr.write('a warning on stderr\\n')\nsys.exit(0)\n",
    "blankboth": lambda args: "import sys\nif sys.argv[1:] == %r:\n    sys.stderr.write('  \\n\\n')\n    sys.exit(1)\n" % (args,),
    "blank": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('   ')\n    sys.stderr.write('VERDICT: FAIL - on stderr\\n')\n    sys.exit(1)\n" % (args,),
    "bothnofail": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('alpha')\n    sys.stderr.write('VERDICT: FAIL - on stderr\\n')\n    sys.exit(1)\n" % (args,),
    "midline": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('ok one')\n    print('note mid FAIL here')\n    print('ok last')\n    sys.exit(1)\n" % (args,),
    "passverdict": lambda args: "import sys\nif sys.argv[1:] == %r:\n    print('VERDICT: PASS')\n    sys.exit(1)\n" % (args,),
    "slow3": lambda args: "import sys, time\ntime.sleep(3)\nsys.exit(0)\n",
    "slow2": lambda args: "import sys, time\ntime.sleep(1.85)\nsys.exit(0)\n",
    "slow6": lambda args: "import sys, time\ntime.sleep(6)\nsys.exit(0)\n",
    "slow": lambda args: "import sys, time\ntime.sleep(0.6)\nsys.exit(0)\n",
    "slow08": lambda args: "import sys, time\ntime.sleep(0.8)\nsys.exit(0)\n",
    "slow13": lambda args: "import sys, time\ntime.sleep(1.3)\nsys.exit(0)\n",
    "slow18": lambda args: "import sys, time\ntime.sleep(1.8)\nsys.exit(0)\n",
    "slow24": lambda args: "import sys, time\ntime.sleep(2.4)\nsys.exit(0)\n",
}
def stub(args, code, hang=False, silent=False):
    if hang: return "import time\ntime.sleep(400)\n"
    if silent: return "import sys\nsys.exit(%d if sys.argv[1:] == %r else 0)\n" % (code, args)
    return "import sys\nc = %d if sys.argv[1:] == %r else 0\nprint('VERDICT: ' + ('PASS' if c == 0 else 'FAIL - planted'))\nsys.exit(c)\n" % (code, args)
UNRELATED = ("vocab", "many", "ric", "gatek", "kind", "register", "fixture", "link", "archive", "pipeline")
MARKS = {"ric": "release-item accounting", "versioned": "keeps its versioned name", "noentry": "changelog", "vocab": "vocabulary probe fails", "gatek": "Gate K:", "kind": "the kind and category probe fails", "register": "the register does not validate", "fixture": "the positive fixture does not validate", "link": "the link-control probe fails", "archive": "archive integrity", "pipeline": "stage digests of"}
def ENV(tl):
    e = dict(os.environ); e.pop("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", None)
    if tl is not None: e["BACKLOG_PREFLIGHT_SECTION_TIMEOUT"] = tl
    return e
def files_hang_default(s):
    return {"backlog_number_origin_v1_2_0.py": (stub(["--strict"], 0, hang=True), None), "backlog_doc_coverage_gate_v1_2_0.py": (stub([], 0), None)}
class Scratch:
    def __init__(s, toolpath, arrival=False):
        s.t = tempfile.mkdtemp(); git(s.t, "init", "-q", "--bare", "origin.git"); git(s.t, "clone", "-q", "origin.git", "a"); s.a = os.path.join(s.t, "a"); s.pk = os.path.join(s.a, "backlog-roadmap-framework")
        os.makedirs(s.pk + "/03-tooling"); os.makedirs(s.pk + "/04-documentation"); s.tool = s.pk + "/03-tooling/" + os.path.basename(toolpath); shutil.copy(toolpath, s.tool)
        open(s.pk + "/VERSION.txt", "w").write("1.0.0\n"); open(s.pk + "/04-documentation/CHANGELOG_v1_1_0.md", "w").write("## v1.0.1 — x\n")
        s.base = set(os.listdir(s.pk + "/03-tooling")); has_onts(s.pk); git(s.a, "add", "-A"); git(s.a, "commit", "-q", "-m", "base"); git(s.a, "push", "-q", "origin", "HEAD:main")
        for tg in ("v0.0.1", "v0.0.2", "v0.0.10", "v1.0.1"): git(s.a, "tag", "backlog-roadmap-framework-" + tg)
        if arrival:
            git(s.t, "clone", "-q", "origin.git", "b"); git(s.t + "/b", "pull", "-q", "origin", "main"); os.makedirs(s.t + "/b/backlog-roadmap-framework/07-handover-inbox/pending", exist_ok=True)
            open(s.t + "/b/backlog-roadmap-framework/07-handover-inbox/pending/HANDOVER_x_to_y_z_v1_0_0.md", "w").write("q\n"); git(s.t + "/b", "add", "-A"); git(s.t + "/b", "commit", "-q", "-m", "arrives"); git(s.t + "/b", "push", "-q", "origin", "HEAD:main")
    def run(s, files, onts=True, limit=60, other_refusal=None, tl="1"):
        om = set(other_refusal) if isinstance(other_refusal, (tuple, list)) else {other_refusal}; cl_mode = [m for m in ("versioned", "noentry", "many") if m in om][:1]; cl_mode = cl_mode[0] if cl_mode else None
        open(s.pk + "/04-documentation/CHANGELOG_v1_1_0.md", "w").write({"versioned": "## v1.0.1 — x\nchanged under its own name\n", "noentry": "## v0.0.1 — x\n", "many": "## v0.0.1 — x\n"}.get(cl_mode, "## v1.0.1 — x\n"))
        for f in os.listdir(s.pk + "/03-tooling"):
            if f not in s.base:
                q = s.pk + "/03-tooling/" + f
                shutil.rmtree(q) if os.path.isdir(q) else os.remove(q)
        for f in glob.glob(s.pk + "/01-ontologies/backlog_abox_v*.ttl"): os.remove(f)
        for nm, (body, mt) in files.items():
            p = s.pk + "/03-tooling/" + nm; os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(body)
            if mt is not None: os.utime(p, (mt, mt))
        for other_refusal in [m for m in sorted(om, key=str) if m in UNRELATED]:
            td = s.pk + "/03-tooling/"; fx = "import sys\nprint('%s planted')\nsys.exit(1)\n"
            if other_refusal == "ric":
                open(td + "backlog_release_item_check_v1_0_0.py", "w").write("import sys\nprint('ric planted')\nsys.exit(1)\n")
                if not git(s.a, "tag", "--list", "backlog-roadmap-framework-v*").strip(): git(s.a, "tag", "backlog-roadmap-framework-v1.0.0")
            if other_refusal == "gatek": open(td + "backlog_validate_v1_0_0.py", "w").write("import sys\nif '--gate-k' in sys.argv:\n    print('gate k planted')\n    sys.exit(1)\n")
            if other_refusal == "kind": open(td + "backlog_kind_category_probe_v1_0_0.py", "w").write("import sys\nprint('FAIL kind planted')\nsys.exit(1)\n")
            if other_refusal in ("kind", "register", "fixture", "link", "archive", "pipeline"):
                open(s.pk + "/01-ontologies/backlog_abox_v1_0_0.ttl", "w").write("fw:L_X a backlog:Lineage .\n")
                open(td + "backlog_validate_v1_0_0.py", "w").write("import sys\nbad = %r\nsys.exit(1 if bad and (bad != 'fixture' or 'fixture' in ' '.join(sys.argv)) and '--gate-k' not in sys.argv and (bad in ('register', 'fixture')) else 0)\n" % other_refusal)
                if other_refusal == "fixture": os.makedirs(td + "fixtures", exist_ok=True); open(td + "fixtures/fixture_positive_v1_0_0.ttl", "w").write("@prefix : <http://example.org/x#> .\n")
                if other_refusal == "link": open(td + "backlog_link_control_probe_v1_0_0.py", "w").write(fx % "link")
                if other_refusal == "archive": open(td + "backlog_archive_integrity_v1_0_0.py", "w").write(fx % "archive")
                if other_refusal == "pipeline": open(td + "backlog_pipeline_verify_v1_0_0.py", "w").write(fx % "pipeline")
        if om & {"vocab", "many"}: open(s.pk + "/03-tooling/backlog_vocabulary_probe_v1_0_0.py", "w").write("import sys\nprint('vocabulary probe: FAIL')\nsys.exit(3)\n")
        od = s.pk + "/01-ontologies"
        if not onts and os.path.isdir(od): os.rename(od, s.t + "/onts_away")
        if onts and not os.path.isdir(od): os.rename(s.t + "/onts_away", od)
        try:
            return subprocess.run([sys.executable, "-B", s.tool, "preflight", "1.0.1"], capture_output=True, text=True, cwd=s.pk, env=ENV(tl), timeout=limit).stdout
        except subprocess.TimeoutExpired:
            return "PROBE-TIMEOUT"
    def close(s): shutil.rmtree(s.t, ignore_errors=True)
class RealScratch:
    """The checkers and the files they read, copied from this package into a scratch git clone with a tag, a register file and the fixtures: the setting the preflight meets in a release."""
    def __init__(s, toolpath):
        pkg0 = os.path.dirname(HERE); nw = lambda pat: sorted(glob.glob(pat), key=sv)[-1]
        s.t = tempfile.mkdtemp(); git(s.t, "init", "-q", "--bare", "origin.git"); git(s.t, "clone", "-q", "origin.git", "a"); s.a = os.path.join(s.t, "a"); s.pk = os.path.join(s.a, "backlog-roadmap-framework")
        for d in ("03-tooling", "01-ontologies", "02-shacl-safeguards", "04-documentation", "06-package-provenance", "03-tooling/fixtures"): os.makedirs(s.pk + "/" + d, exist_ok=True)
        s.tool = s.pk + "/03-tooling/" + os.path.basename(toolpath); shutil.copy(toolpath, s.tool)
        for pat in ("03-tooling/backlog_number_origin_v*.py", "03-tooling/backlog_doc_coverage_gate_v*.py", "01-ontologies/backlog_tbox_v*.ttl", "02-shacl-safeguards/backlog_shacl_v*.ttl", "04-documentation/BACKLOG_ROADMAP_FRAMEWORK_STANDARD_v*.md", "06-package-provenance/LIGHT_RELEASES.txt"):
            src = nw(os.path.join(pkg0, pat)) if "*" in pat else os.path.join(pkg0, pat)
            shutil.copy(src, s.pk + "/" + os.path.dirname(pat) + "/" + os.path.basename(src))
        shutil.copy(nw(os.path.join(pkg0, "03-tooling/fixtures/fixture_positive_v*.ttl")), s.pk + "/03-tooling/fixtures/")
        open(s.pk + "/01-ontologies/backlog_abox_v1_0_0.ttl", "w").write("@prefix : <http://example.org/x#> .\n")
        open(s.pk + "/VERSION.txt", "w").write("9.9.8\n"); open(s.pk + "/04-documentation/CHANGELOG_v1_1_0.md", "w").write("## v9.9.9 — x\n")
        s.tbox = nw(s.pk + "/01-ontologies/backlog_tbox_v*.ttl"); s.std = nw(s.pk + "/04-documentation/BACKLOG_ROADMAP_FRAMEWORK_STANDARD_v*.md")
        s.tbox_text = open(s.tbox, encoding="utf-8").read(); s.std_text = open(s.std, encoding="utf-8").read()
        git(s.a, "add", "-A"); git(s.a, "commit", "-q", "-m", "base"); git(s.a, "tag", "backlog-roadmap-framework-v9.9.8"); git(s.a, "push", "-q", "origin", "HEAD:main")
    def run(s, plant=None):
        open(s.tbox, "w", encoding="utf-8").write(s.tbox_text + ("\n<http://example.org/backlog#PlantedNumber> a <http://www.w3.org/2002/07/owl#DatatypeProperty> ; <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2001/XMLSchema#decimal> .\n" if plant == "number" else ""))
        open(s.std, "w", encoding="utf-8").write(re.sub(r"\bRuleRepair\b", "RuleRepa1r", s.std_text) if plant == "class" else s.std_text)
        try:
            return subprocess.run([sys.executable, "-B", s.tool, "preflight", "9.9.9"], capture_output=True, text=True, cwd=s.pk, env=dict(os.environ, BACKLOG_PREFLIGHT_SECTION_TIMEOUT="30"), timeout=300).stdout
        except subprocess.TimeoutExpired:
            return "PROBE-TIMEOUT"
    def close(s): shutil.rmtree(s.t, ignore_errors=True)

# A reference model of gate_section_failures, run against the function over a grid of checker states (so no single fault the reviewers might think of hides): both checkers cross a wide set of states
# (exit codes over every range, every output kind, hang, slow then fail, slow pass, passing with stderr, missing, an older version beside a newer one) and the exact refusals are compared with the model's.
import importlib.util, itertools, concurrent.futures as _cf
GRID_MISMATCH = []
OUTK = {"verdict": ("VERDICT: FAIL - v\n", ""), "silent": ("", ""), "stderr": ("", "VERDICT: FAIL - e\n"), "nofail": ("alpha\nbeta\n", ""),
        "mixed": ("FAIL early\nVERDICT: FAIL - final\ntail\n", ""), "blank": ("   \n", "VERDICT: FAIL - on stderr\n"), "bothnofail": ("alpha\n", "VERDICT: FAIL - on stderr\n"),
        "midline": ("ok one\nnote mid FAIL here\nok last\n", ""), "passverdict": ("VERDICT: PASS\n", ""), "failtail": ("VERDICT: FAIL - first\nFAIL: detail last\n", ""),
        "verdicttail": ("FAIL early detail\nVERDICT: REFUSED\n", ""), "lower": ("VERDICT: FAIL - real\nthe failing detail in lower case\n", ""), "long": ("VERDICT: FAIL - " + "x" * 300 + "\n", ""),
        "twochan": ("VERDICT: FAIL - out\n", "VERDICT: FAIL - err\n"), "blankerr": ("VERDICT: FAIL - out\n", "   \n")}
def _body(spec, args):
    k = spec[0]
    if k == "pass": return "import sys\nsys.exit(0)\n"
    if k == "passfailtext": return "import sys\nprint('VERDICT: FAIL - but exit 0')\nsys.exit(0)\n"
    if k == "passfailerr": return "import sys\nsys.stderr.write('FAIL on stderr\\n')\nsys.exit(0)\n"
    if k == "passerr": return "import sys\nsys.stderr.write('warning\\n')\nsys.exit(0)\n"
    if k == "slowpass": return "import sys, time\ntime.sleep(%s)\nsys.exit(0)\n" % (spec[1] if len(spec) > 1 else 1.5)
    if k == "hang": return "import time\ntime.sleep(400)\n"
    code, kind = spec[1], spec[2]
    pre = "import sys, time\nif sys.argv[1:] != %r:\n    sys.exit(0)\n" % (args,) + ("time.sleep(%s)\n" % (spec[3] if len(spec) > 3 else 1.5) if k == "slowfail" else "")
    so, se = OUTK[kind]
    return pre + "sys.stdout.write(%r)\nsys.stdout.flush()\nsys.stderr.write(%r)\nsys.exit(%d)\n" % (so, se, code)
def _stdout_of(spec):
    k = spec[0]
    if k not in ("fail", "slowfail"): return "", ""
    return OUTK[spec[2]]
def _expect(what, newest_name, spec):
    k = spec[0]
    if k in ("missing", "pass", "passerr", "slowpass", "passfailtext", "passfailerr"): return None
    if k == "hang": return "the gate's %s section did not answer in time (it takes under one second here): %s" % (what, newest_name)
    so, se = _stdout_of(spec)
    lines = so.strip().splitlines() or se.strip().splitlines() or ["no output"]
    hit = [l.strip() for l in lines if "FAIL" in l or "VERDICT" in l] or lines[-1:]
    return "the gate's %s section refuses (exit %d): %s" % (what, spec[1], hit[-1][:240])
SIBLINGS = ("backlog_coverage_gate_v9_9_9.py", "backlog_number_origin_probe_v9_9_9.py", "backlog_number_origin_check_v9_9_9.py", "backlog_doc_coverage_v9_9_9.py")
def _build(root, spec_a, spec_b):
    here = os.path.join(root, "03-tooling"); pkg = os.path.join(root, "pkg"); os.makedirs(here); os.makedirs(pkg)
    exp = []
    DEC = "import sys\nprint('VERDICT: FAIL - sibling')\nsys.exit(1)\n"
    for sib in SIBLINGS: open(os.path.join(here, sib), "w").write(DEC)
    for (what, base, args) in KINDS:
        for dn in (base + "_v9_0_0.txt", "old_" + base + "_v9_0_0.py", "x" + base + "_v9_0_0.py", base + "_v9_0_0.py.bak", base + "_probe_v9_0_0.py"): open(os.path.join(here, dn), "w").write(DEC)
        os.makedirs(os.path.join(here, "sub"), exist_ok=True); open(os.path.join(here, "sub", base + "_v9_0_0.py"), "w").write(DEC)
        os.makedirs(os.path.join(here, "fixtures"), exist_ok=True); open(os.path.join(here, "fixtures", base + "_v9_0_0.py"), "w").write(DEC)
    for (what, base, args), spec in zip(KINDS, (spec_a, spec_b)):
        if spec[0] == "missing": exp.append(None); continue
        if spec[0] == "older":
            open(os.path.join(here, base + "_v1_1_0.py"), "w").write(_body(spec[1], args)); cur = spec[2]
        else: cur = spec
        ver = "1_2_0"
        if cur[0] == "ver": ver, cur = cur[1], cur[2]
        nm = base + "_v" + ver + ".py"; open(os.path.join(here, nm), "w").write(_body(cur, args)); exp.append(_expect(what, nm, cur))
    return here, pkg, [e for e in exp if e]
def grid_matrix(toolpath):
    with tempfile.TemporaryDirectory() as td:
        spec = importlib.util.spec_from_file_location("tm_" + str(abs(hash(toolpath))), toolpath); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        S9 = [("pass",), ("fail", 1, "verdict"), ("fail", 7, "verdict"), ("fail", 100, "silent"), ("hang",), ("fail", 130, "stderr"), ("slowfail", 1, "verdict"), ("slowpass",), ("missing",)]
        W = [("passerr",)] + [("fail", c, "verdict") for c in (2, 3, 6, 8, 63, 64, 65, 99, 101, 125, 126, 127, 128, 129, 131, 254, 255)]
        W += [("fail", c, kd) for c in (1, 100) for kd in ("silent", "stderr", "nofail", "mixed")]
        W += [("ver", v, sp) for v in ("2_0_0", "1_10_0", "0_0_1") for sp in (("hang",), ("fail", 7, "verdict"), ("fail", 100, "silent"))]
        W += [("older", ("fail", 1, "verdict"), ("hang",)), ("older", ("fail", 1, "verdict"), ("pass",)), ("older", ("fail", 1, "verdict"), ("fail", 7, "verdict")), ("older", ("hang",), ("pass",)), ("older", ("pass",), ("fail", 3, "stderr"))]
        W2 = [("pass",), ("passerr",), ("passfailtext",), ("passfailerr",), ("hang",), ("slowfail", 1, "verdict"), ("fail", 1, "verdict"), ("fail", 3, "verdict"), ("fail", 4, "verdict"), ("fail", 8, "verdict"), ("fail", 9, "verdict"), ("fail", 62, "verdict"), ("fail", 126, "verdict"), ("fail", 127, "verdict"), ("fail", 255, "stderr"), ("older", ("fail", 1, "verdict"), ("pass",)), ("older", ("fail", 1, "verdict"), ("fail", 7, "verdict")), ("missing",)]
        allc = [(("fail", c, "verdict"), ("pass",)) for c in range(1, 256)] + [(("pass",), ("fail", c, "verdict")) for c in range(1, 256)] + [(("fail", c, "verdict"), ("fail", 1, "verdict")) for c in range(1, 256)] + [(("fail", 1, "verdict"), ("fail", c, "verdict")) for c in range(2, 256)]
        allk = [(("fail", c, kd), ("pass",)) for c in range(1, 256) for kd in OUTK] + [(("pass",), ("fail", c, kd)) for c in range(1, 256) for kd in OUTK]
        sc = list(dict.fromkeys(allc + allk + [(a, b) for a in S9 for b in S9] + [(a, b) for a in W2 for b in W2] + [(w, ("pass",)) for w in W] + [(("pass",), w) for w in W]))
        def one(i):
            a, b = sc[i]; root = os.path.join(td, str(i)); here, pkg, exp = _build(root, a, b)
            try: got = m.gate_section_failures(here, pkg)
            except Exception as e: got = ["raised " + type(e).__name__]
            return None if got == exp else (a, b, got, exp)
        os.environ["BACKLOG_PREFLIGHT_SECTION_TIMEOUT"] = "2"
        with _cf.ThreadPoolExecutor(max_workers=8) as ex: res = [r for r in ex.map(one, range(len(sc))) if r]
        os.environ.pop("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", None)
        if res: GRID_MISMATCH.append(res[:3])
        return not res

import random
def _rspec(r):
    x = r.random()
    if x < .27: return ("pass",)
    if x < .31: return ("passerr",)
    if x < .34: return ("passfailtext",)
    if x < .37: return ("passfailerr",)
    if x < .40: return ("hang",)
    if x < .43: return ("slowpass", 1.2)
    if x < .47: return ("slowfail", r.randint(1, 255), r.choice(list(OUTK)), 1.2)
    if x < .50: return ("missing",)
    code = r.choice([r.randint(1, 255), r.randint(1, 9), r.randint(10, 61), r.randint(62, 100), r.randint(101, 255), 126, 127, 130, 255, 100, 42, 63])
    return ("fail", code, r.choice(list(OUTK)))
def _rfull(r):
    cur = _rspec(r)
    if cur[0] == "missing": return cur
    y = r.random()
    if y < .15: return ("ver", r.choice(("1_10_0", "2_0_0", "0_0_1")), cur)
    if y < .30:
        old = _rspec(r)
        if old[0] != "missing": return ("older", old, ("ver", r.choice(("1_10_0", "2_0_0")), cur) if r.random() < .5 else cur)
    return cur
def fuzz_function(toolpath, n=1100, seed=20261122):
    r = random.Random(seed); sc = [(_rfull(r), _rfull(r)) for _ in range(n)]
    with tempfile.TemporaryDirectory() as td:
        spec = importlib.util.spec_from_file_location("tf_" + str(abs(hash(toolpath))), toolpath); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        def one(i):
            a, b = sc[i]; here, pkg, exp = _build(os.path.join(td, str(i)), a, b)
            try: got = m.gate_section_failures(here, pkg)
            except Exception as e: got = ["raised " + type(e).__name__]
            return None if got == exp else (a, b, got, exp)
        os.environ["BACKLOG_PREFLIGHT_SECTION_TIMEOUT"] = "2"
        with _cf.ThreadPoolExecutor(max_workers=8) as ex: res = [x for x in ex.map(one, range(len(sc))) if x]
        os.environ.pop("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", None)
        if res: GRID_MISMATCH.append(res[:2])
        return not res
def fuzz_preflight(s, n=60, seed=20261123, arrival=False):
    r = random.Random(seed); ok = True; bad_cases = []
    for i in range(n):
        modes = tuple(m for m in ("versioned", "noentry", "vocab", "ric", "gatek") if r.random() < .4)
        specs = []
        for _ in KINDS:
            x = r.random(); specs.append(("pass",) if x < .35 else ("hang",) if x < .45 else ("fail", r.choice([r.randint(1, 255), 1, 2, 3, 5, 7, 100, 126, 127, 255]), r.choice(list(OUTK))))
        files = {}; exp = []
        for (what, base, args), sp in zip(KINDS, specs):
            nm = base + "_v1_2_0.py"; files[nm] = (_body(sp, args), None); e = _expect(what, nm, sp)
            if e: exp.append(e)
        onts = r.random() > .15
        if r.random() < .5: files["backlog_validate_v1_0_0.py"] = ("import sys\nsys.exit(1 if '--gate-k' in sys.argv and %r else 0)\n" % ("gatek" in modes,), None)
        if r.random() < .5: files["fixtures/fixture_positive_v1_0_0.ttl"] = ("x\n", None)
        for d in ("02-shacl-safeguards", "04-documentation"):
            os.makedirs(os.path.join(s.pk, d), exist_ok=True)
        if r.random() < .5: open(s.pk + "/02-shacl-safeguards/backlog_shacl_v1_0_0.ttl", "w").write("x\n")
        elif os.path.exists(s.pk + "/02-shacl-safeguards/backlog_shacl_v1_0_0.ttl"): os.remove(s.pk + "/02-shacl-safeguards/backlog_shacl_v1_0_0.ttl")
        if r.random() < .5: open(s.pk + "/04-documentation/BACKLOG_ROADMAP_FRAMEWORK_STANDARD_v1_0_0.md", "w").write("x\n")
        elif os.path.exists(s.pk + "/04-documentation/BACKLOG_ROADMAP_FRAMEWORK_STANDARD_v1_0_0.md"): os.remove(s.pk + "/04-documentation/BACKLOG_ROADMAP_FRAMEWORK_STANDARD_v1_0_0.md")
        if not os.path.isdir(s.pk + "/01-ontologies") and os.path.isdir(s.t + "/onts_away"): os.rename(s.t + "/onts_away", s.pk + "/01-ontologies")
        tb = s.pk + "/01-ontologies/backlog_tbox_v1_0_0.ttl"
        if onts and r.random() < .5: open(tb, "w").write("x\n")
        elif os.path.exists(tb): os.remove(tb)
        for tg in git(s.a, "tag", "--list", "backlog-roadmap-framework-v*").split(): git(s.a, "tag", "-d", tg)
        for tg in ("v0.0.1", "v0.0.2", "v0.0.10", "v1.0.1"):
            if "ric" in modes and tg == "v0.0.1" or r.random() < .5: git(s.a, "tag", "backlog-roadmap-framework-" + tg)
        o = s.run(files, onts=onts, other_refusal=modes if modes else None, limit=60)
        if not onts: exp = []
        got = [l for l in o.splitlines() if "the gate's" in l]
        good = len(got) == len(exp) and all(any(e in l for l in got) for e in exp)
        for m in modes:
            if m == "noentry" and "versioned" in modes: continue
            if m == "vocab" and not onts: continue
            if m == "ric" and not git(s.a, "tag", "--list", "backlog-roadmap-framework-v*").strip(): continue
            good = good and MARKS[m] in o
        if not modes and not exp: good = good and "GO" in o
        if arrival: good = good and "handover(s) on origin" in o
        if not good: ok = False; bad_cases.append((modes, specs, onts, o[-300:]))
    if bad_cases: GRID_MISMATCH.append(bad_cases[:1])
    return ok
def sec_fuzz(toolpath):
    R = {}
    R["the grid of checker states: every refusal equals the reference model's, exactly"] = grid_matrix(toolpath)
    R["random states over every dimension (%d cases, seeded): every refusal equals the reference model's, exactly" % 1100] = fuzz_function(toolpath)
    s = Scratch(toolpath)
    try: R["random settings, tags, refusals and outcomes at the preflight (60 cases, seeded): each section named exactly when it refuses"] = fuzz_preflight(s)
    finally: s.close()
    s = Scratch(toolpath, arrival=True)
    try: R["random preflight cases beside a handover arrival (25 cases, seeded)"] = fuzz_preflight(s, n=25, seed=20261124, arrival=True)
    finally: s.close()
    return R
CROSS2 = ((0, ("fail", 100)), (1, ("hang",)))
CROSS = ((0, ("fail", 5)), (0, ("fail", 255)), (1, ("fail", 5)), (1, ("fail", 255)), (0, ("fail", 126)), (1, ("fail", 9)), (0, ("fail", 2)), (0, ("fail", 100)), (1, ("fail", 3)), (1, ("fail", 7)), (0, ("hang",)), (1, ("hang",)), (0, ("fail", 42)), (1, ("fail", 63)))
def cross_cases(s, modes, label, cases=None):
    out = {}
    for mode in modes:
        for ki, sp in (cases or CROSS):
            what, base, args = KINDS[ki]
            body = stub(args, 0, hang=True) if sp[0] == "hang" else stub(args, sp[1])
            fl = {b + "_v1_2_0.py": (stub(a, 0), None) for _, b, a in KINDS}; fl[base + "_v1_2_0.py"] = (body, None)
            o = s.run(fl, other_refusal=mode, limit=60)
            want = "the gate's %s section did not answer in time" % what if sp[0] == "hang" else "the gate's %s section refuses (exit %d): VERDICT: FAIL - planted" % (what, sp[1])
            out["%s %s: %s with %s is named beside it" % (label, mode or "arrival", what, "a hang" if sp[0] == "hang" else "exit %d" % sp[1])] = (want in o)
    return out
def sec_extra(toolpath, cross=True):
    """Review 17 additions: the time limit between its edges, the handover arrival crossed with every unrelated refusal, the real-release setting."""
    R = {}
    def files(over=None, hang=None, extra=None):
        f = {}
        for k, base, args in KINDS:
            f[base + "_v1_2_0.py"] = (stub(args, 0), None)
        for k, base, args in KINDS:
            if hang == k: f[base + "_v1_2_0.py"] = (stub(args, 0, hang=True), None)
        for sib in SIBLINGS: f[sib] = ("import sys\nprint('VERDICT: FAIL - sibling')\nsys.exit(1)\n", None)
        for nm, v in (over or {}).items(): f[nm] = v
        f.update(extra or {})
        return f
    s = Scratch(toolpath)
    try:
        for k, base, args in KINDS:
            for vn, tlv, hangs in (("slow08", "1", False), ("slow13", "1", True), ("slow18", "2", False), ("slow24", "2", True)):
                o = s.run(files({base + "_v1_2_0.py": (VARIANTS[vn](args), None)}), tl=tlv)
                R["%s: a checker taking %s s under a %s s limit %s (the limit is exactly the one stated)" % (k, vn[4] + "." + vn[5], tlv, "is a hang" if hangs else "passes")] = (("the gate's %s section did not answer in time" % k in o) == hangs and ("section refuses" not in o))
    finally:
        s.close()
    s = Scratch(toolpath, arrival=True)
    try:
        if cross:
            R.update(cross_cases(s, ("versioned", "noentry", "vocab", "ric", "gatek"), "unrelated refusal beside an arrival"))
            R.update(cross_cases(s, [sb for n in (2, 3, 4, 5) for sb in itertools.combinations(("versioned", "noentry", "vocab", "ric", "gatek"), n)], "unrelated refusals together beside an arrival", CROSS))
    finally:
        s.close()
    s = Scratch(toolpath, arrival=True)
    try:
        for t_ in git(s.a, "tag", "--list").split(): git(s.a, "tag", "-d", t_)
        R["no release tag beside an arrival: the scratch holds no tag"] = (git(s.a, "tag", "--list").strip() == "")
        if cross:
            R.update(cross_cases(s, (None, "versioned", "noentry", "vocab", "ric", "gatek"), "no release tag, unrelated refusal beside an arrival"))
            R.update(cross_cases(s, [sb for n in (2, 3, 4, 5) for sb in itertools.combinations(("versioned", "noentry", "vocab", "ric", "gatek"), n)], "no release tag, unrelated refusals together beside an arrival", CROSS))
    finally:
        s.close()
    s = Scratch(toolpath)
    try:
        os.makedirs(s.pk + "/02-shacl-safeguards", exist_ok=True); os.makedirs(s.pk + "/03-tooling/fixtures", exist_ok=True); os.makedirs(s.pk + "/04-documentation", exist_ok=True)
        open(s.pk + "/04-documentation/BACKLOG_ROADMAP_FRAMEWORK_STANDARD_v1_0_0.md", "w").write("x\n"); open(s.pk + "/02-shacl-safeguards/backlog_shacl_v1_0_0.ttl", "w").write("x\n")
        open(s.pk + "/01-ontologies/backlog_tbox_v1_0_0.ttl", "w").write("x\n"); open(s.pk + "/01-ontologies/backlog_abox_v1_0_0.ttl", "w").write("x\n")
        if not git(s.a, "tag", "--list", "backlog-roadmap-framework-v*").strip(): git(s.a, "tag", "backlog-roadmap-framework-v1.0.0")
        for k, base, args in KINDS:
            other = [x for x, _, _ in KINDS if x != k][0]
            fl = files({b + "_v1_2_0.py": (stub(a, 0), None) for _, b, a in KINDS}); fl[base + "_v1_2_0.py"] = (stub(args, 1), None); fl["backlog_validate_v1_0_0.py"] = ("import sys\nsys.exit(0)\n", None); fl["fixtures/fixture_positive_v1_0_0.ttl"] = ("x\n", None)
            o = s.run(fl)
            R["all of shapes, standard, fixtures, validator, register and T-box present, %s failing: it is named and the other is not" % k] = ("the gate's %s section refuses" % k in o and other + " section" not in o)
        fl = files({b + "_v1_2_0.py": (stub(a, 0), None) for _, b, a in KINDS}); fl["backlog_validate_v1_0_0.py"] = ("import sys\nsys.exit(0)\n", None); fl["fixtures/fixture_positive_v1_0_0.ttl"] = ("x\n", None)
        o = s.run(fl)
        R["all of shapes, standard, fixtures, validator, register and T-box present, both passing: silent about both"] = ("section refuses" not in o and "did not answer" not in o)
    finally:
        s.close()
    return R
def sec_matrix(toolpath, deep=False, grid=True, cross=True, fuzz=True):
    """Returns a dict name -> bool of every expectation about the two sections, for the tool at toolpath."""
    s = Scratch(toolpath); R = {}; names = {k: k for k, _, _ in KINDS}
    def files(over=None, hang=None, extra=None):
        f = {}
        for k, base, args in KINDS:
            f[base + "_v1_2_0.py"] = (stub(args, 0), None)
        for k, base, args in KINDS:
            if hang == k: f[base + "_v1_2_0.py"] = (stub(args, 0, hang=True), None)
        for sib in SIBLINGS: f[sib] = ("import sys\nprint('VERDICT: FAIL - sibling')\nsys.exit(1)\n", None)
        for nm, v in (over or {}).items(): f[nm] = v
        f.update(extra or {})
        return f
    try:
        _o = s.run(files()); R["silent when both pass: no refusal, no checker output"] = ("section" not in _o and "VERDICT" not in _o and "GO" in _o)
        for k, base, args in KINDS:
            other = [x for x, _, _ in KINDS if x != k][0]
            for code in (1, 2, 3, 4, 5, 7, 64, 100, 126, 127, 130, 255):
                o = s.run(files({base + "_v1_2_0.py": (stub(args, code), None)}))
                R["%s: exit %d is a refusal naming it, with the code and the verdict line, and not the other" % (k, code)] = ("the gate's %s section refuses (exit %d): VERDICT: FAIL - planted" % (k, code) in o and other + " section" not in o and "STOP (1)" in o)
            o = s.run(files({base + "_v1_2_0.py": (stub(args, 1, silent=True), None)}))
            R["%s: a failing checker that prints nothing is still refused and named" % k] = ("the gate's %s section refuses (exit 1): no output" % k in o and other + " section" not in o)
            o = s.run(files(hang=k), limit=60)
            R["%s: a hang is a refusal naming that checker only" % k] = ("the gate's %s section did not answer in time" % k in o and "STOP (1)" in o and ("the gate's %s section" % other) not in o)
            fail, ok = (base + "_v1_9_0.py", base + "_v1_10_0.py")
            for label, mts in (("written in order", (1000, 2000)), ("written in reverse order", (2000, 1000))):
                o = s.run(files(extra={fail: (stub(args, 1), mts[0]), ok: (stub(args, 0), mts[1])}))
                R["%s: failing 1_9_0 beside passing 1_10_0 (%s) is silent: the version is a number, not text, not file time" % (k, label)] = ("section refuses" not in o)
                o = s.run(files(extra={ok: (stub(args, 1), mts[0]), fail: (stub(args, 0), mts[1])}))
                R["%s: failing 1_10_0 beside passing 1_9_0 (%s) is refused" % (k, label)] = ("the gate's %s section refuses" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["stderr"](args), None)}))
            R["%s: a checker that fails with output on stderr only is refused and its line is named" % k] = ("the gate's %s section refuses (exit 1): FATAL: planted on stderr" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["passfail"](args), None)}))
            R["%s: a passing checker whose output mentions FAIL is silent" % k] = ("section refuses" not in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["verdictmix"](args), None)}))
            R["%s: the verdict line named is the last FAIL or VERDICT line" % k] = ("the gate's %s section refuses (exit 1): VERDICT: FAIL - final" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["bothchannels"](args), None)}))
            R["%s: when both channels carry a verdict line, the one on stdout is named" % k] = ("the gate's %s section refuses (exit 1): VERDICT: FAIL - on stdout" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["failtail"](args), None)}))
            R["%s: a FAIL line after the verdict line is the line named (the last of either kind)" % k] = ("the gate's %s section refuses (exit 1): FAIL: detail last" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["verdicttail"](args), None)}))
            R["%s: a verdict line that does not say FAIL is the line named" % k] = ("the gate's %s section refuses (exit 1): VERDICT: REFUSED" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["slow2"](args), None)}), tl="2")
            R["%s: a checker taking 1.85 s passes under a 2 s limit (not scaled, not reduced)" % k] = ("section refuses" not in o and "did not answer" not in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["slow6"](args), None)}), tl=None, limit=120)
            R["%s: with the limit unset a checker taking 6 s passes (the default is run, not read)" % k] = ("section refuses" not in o and "did not answer" not in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["nofail"](args), None)}))
            R["%s: with no FAIL or VERDICT line the last line is named" % k] = ("the gate's %s section refuses (exit 1): beta" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["lowercase"](args), None)}))
            R["%s: FAIL is matched in capitals only" % k] = ("the gate's %s section refuses (exit 1): VERDICT: FAIL - real" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["passstderr"](args), None)}))
            R["%s: a passing checker that writes to stderr is silent" % k] = ("section refuses" not in o and "did not answer" not in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["slow3"](args), None)}), tl="1")
            R["%s: a checker taking 3 s under a 1 s limit is a hang (the limit is not enlarged or floored)" % k] = ("the gate's %s section did not answer in time" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["blank"](args), None)}))
            R["%s: a blank stdout is read as empty and stderr is named" % k] = ("the gate's %s section refuses (exit 1): VERDICT: FAIL - on stderr" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["blankboth"](args), None)}))
            R["%s: blank stdout and blank stderr read as no output" % k] = ("the gate's %s section refuses (exit 1): no output" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["bothnofail"](args), None)}))
            R["%s: with text on both channels and no FAIL line on stdout the last stdout line is named" % k] = ("the gate's %s section refuses (exit 1): alpha" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["midline"](args), None)}))
            R["%s: FAIL in the middle of a line counts" % k] = ("the gate's %s section refuses (exit 1): note mid FAIL here" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["passverdict"](args), None)}))
            R["%s: a non-zero exit that prints a PASS verdict is still refused" % k] = ("the gate's %s section refuses (exit 1): VERDICT: PASS" % k in o)
            for code in (100, 127, 255):
                o = s.run(files({base + "_v1_2_0.py": ("import sys\nif sys.argv[1:] == %r:\n    print('FAIL early detail')\n    print('VERDICT: FAIL - final')\n    sys.exit(%d)\n" % (args, code), None)}))
                R["%s: exit %d with several FAIL lines names the last" % (k, code)] = ("the gate's %s section refuses (exit %d): VERDICT: FAIL - final" % (k, code) in o)
            o = s.run(files(extra={base + "_v9_0_0.txt": (stub(args, 1), None), "old_" + base + "_v9_0_0.py": (stub(args, 1), None)}))
            R["%s: a .txt file or a file with a prefix is not the checker" % k] = ("section refuses" not in o)
            for mode in ("versioned", "noentry", "vocab", "ric", "gatek"):
                o = s.run(files(), other_refusal=mode)
                R["%s: both sections passing, the unrelated refusal (%s) is still reported" % (k, mode)] = (MARKS[mode] in o and "STOP (" in o and "the gate's" not in o)
            o = s.run(files(extra={base + "_vX.py": (stub(args, 1), None)}))
            R["%s: a file with an unversioned name does not outrank the versioned checker" % k] = ("section refuses" not in o)
            o = s.run(files(extra={"sub/" + base + "_v9_0_0.py": (stub(args, 1), None)}))
            R["%s: a checker in a sub-folder of the tooling folder is not the checker" % k] = ("section refuses" not in o)
            o = s.run(files({base + "_v1_2_0.py": (VARIANTS["slow"](args), None)}))
            R["%s: a checker slower than a half of the time limit still passes (the limit is not scaled down)" % k] = ("section refuses" not in o and "did not answer" not in o)
            o = s.run(files(extra={base + "_probe_v9_0_0.py": (stub(args, 1), None), base + "_v9_0_0.py.bak": (stub(args, 1), None)}))
            R["%s: files with a similar name are not the checker" % k] = ("section refuses" not in o)
            for mode in ("versioned", "noentry", "vocab"):
                o = s.run(files(hang=k), other_refusal=mode, limit=60)
                R["%s: a hang is named with an unrelated refusal (%s) present" % (k, mode)] = ("the gate's %s section did not answer in time" % k in o)
                o = s.run(files({base + "_v1_2_0.py": (stub(args, 7), None)}), other_refusal=mode)
                R["%s: exit 7 is named with an unrelated refusal (%s) present" % (k, mode)] = ("the gate's %s section refuses (exit 7)" % k in o)
            o = s.run(files({base + "_v1_2_0.py": (stub(["--x"] + args, 1), None)}))
            R["%s: called with exactly the gate's arguments, no more" % k] = ("section refuses" not in o)
            o = s.run(files({base + "_v1_2_0.py": ("import sys\nsys.exit(1 if sys.argv[1:] != %r else 0)\n" % (args,), None)}))
            R["%s: called with exactly the gate's arguments, no fewer" % k] = ("section refuses" not in o)
        if cross:
            for mode in ("ric", "gatek", "versioned"):
                fl = {b + "_v1_2_0.py": (stub(a, 0, hang=True), None) for _, b, a in KINDS}
                o = s.run(fl, other_refusal=mode, limit=60)
                R["both sections hang beside an unrelated refusal (%s): both are named" % mode] = (o.count("section did not answer in time") == 2)
        if cross: R.update(cross_cases(s, ("versioned", "noentry", "vocab", "ric", "gatek"), "unrelated refusal")); R.update(cross_cases(s, [sb for n in range(2, 6) for sb in itertools.combinations(("versioned", "noentry", "vocab", "ric", "gatek"), n)], "unrelated refusals together", CROSS))
        for k, base, args in KINDS:
            for ver in ("2_0_0", "1_10_0", "0_0_1"):
                o = s.run(files(extra={base + "_v" + ver + ".py": (stub(args, 0, hang=True), None)}) if ver != "0_0_1" else files({base + "_v1_2_0.py": (stub(args, 0), None)}, extra={base + "_v" + ver + ".py": (stub(args, 0, hang=True), None)}), limit=60)
                R["%s: a hang of a checker named _v%s is named (%s)" % (k, ver, "newest" if ver != "0_0_1" else "oldest is not run")] = (("the gate's %s section did not answer in time" % k in o) == (ver != "0_0_1"))
        states = ("pass", "fail", "hang", "missing")
        def sf(k, base, args, st):
            return {"pass": {base + "_v1_2_0.py": (stub(args, 0), None)}, "fail": {base + "_v1_2_0.py": (stub(args, 1), None)}, "hang": {base + "_v1_2_0.py": (stub(args, 0, hang=True), None)}, "missing": {}}[st]
        for s1 in states:
            for s2 in states:
                f = {}; f.update(sf("number origin", KINDS[0][1], KINDS[0][2], s1)); f.update(sf("doc coverage", KINDS[1][1], KINDS[1][2], s2))
                o = s.run(f, limit=60)
                want = lambda st: st in ("fail", "hang")
                n1 = ("the gate's number origin section" in o); n2 = ("the gate's doc coverage section" in o)
                R["states crossed, number origin %s with doc coverage %s: each is named exactly when it fails or hangs, and the count is right" % (s1, s2)] = ("VERDICT: PASS" not in o and n1 == want(s1) and n2 == want(s2) and ("STOP (%d)" % (want(s1) + want(s2)) in o if want(s1) or want(s2) else "STOP" not in o))
        dn = "import sys\nif sys.argv[1:] == %r:\n    print('VERDICT: FAIL - %s')\n    sys.exit(%d)\n"
        o = s.run(files({KINDS[0][1] + "_v1_2_0.py": (dn % (KINDS[0][2], "NO", 3), None), KINDS[1][1] + "_v1_2_0.py": (dn % (KINDS[1][2], "DC", 5), None)}))
        R["both fail with different codes and lines: each is named with its own code and line"] = ("number origin section refuses (exit 3): VERDICT: FAIL - NO" in o.replace("the gate's ", "") and "doc coverage section refuses (exit 5): VERDICT: FAIL - DC" in o.replace("the gate's ", ""))
        o = s.run(files({KINDS[0][1] + "_v1_2_0.py": (stub(KINDS[0][2], 3), None), KINDS[1][1] + "_v1_2_0.py": (stub(KINDS[1][2], 1), None)}))
        R["number origin exits 3 and doc coverage fails: both are named (an exit above 1 does not stop the next)"] = ("number origin section refuses (exit 3)" in o.replace("the gate's ", "") and "doc coverage section refuses (exit 1)" in o.replace("the gate's ", ""))
        for k, base, args in KINDS:
            for lo, hi in (("1_2_9", "1_2_10"), ("1_9_0", "2_0_0"), ("1_9_9", "1_10_0")):
                o = s.run(files(extra={base + "_v" + lo + ".py": (stub(args, 1), 1000), base + "_v" + hi + ".py": (stub(args, 0), 2000)}))
                R["%s: failing %s beside passing %s is silent (every component of the version counts, the length of the name does not)" % (k, lo, hi)] = ("section refuses" not in o)
                o = s.run(files(extra={base + "_v" + hi + ".py": (stub(args, 1), 1000), base + "_v" + lo + ".py": (stub(args, 0), 2000)}))
                R["%s: failing %s beside passing %s is refused" % (k, hi, lo)] = ("the gate's %s section refuses" % k in o)
        bothfail = files({b + "_v1_2_0.py": (stub(a, 1), None) for _, b, a in KINDS})
        for mode, mark in ((m, MARKS[m]) for m in ("versioned", "noentry", "vocab", "ric", "gatek", "kind", "register", "fixture", "link", "archive", "pipeline")):
            o = s.run(bothfail, other_refusal=mode)
            R["an unrelated refusal (%s) present: both sections are still run and named beside it" % mode] = ("number origin section refuses" in o and "doc coverage section refuses" in o and mark in o)
    finally:
        s.close()
    s = Scratch(toolpath, arrival=True)
    try:
        if cross: R.update(cross_cases(s, (None,), "unrelated refusal")); R.update(cross_cases(s, (("gatek",), ("ric", "vocab", "gatek")), "unrelated refusals with an arrival"))
        for mode, mark, cnt in ((None, "handover(s) on origin", 3), ("many", "handover(s) on origin", 6)):
            o = s.run(bothfail, other_refusal=mode)
            R["an unrelated refusal (%s) present: both sections are still run and named beside it" % (mode or "a handover arrival")] = ("number origin section refuses" in o and "doc coverage section refuses" in o and mark in o and "STOP (%d)" % cnt in o)
    finally:
        s.close()
    s = Scratch(toolpath)
    try:
        o = s.run(files({b + "_v1_2_0.py": (stub(a, 1), None) for _, b, a in KINDS}), onts=False)
        R["no ontologies folder: neither runs"] = ("section refuses" not in o)
        os.makedirs(s.pk + "/02-shacl-safeguards", exist_ok=True); os.makedirs(s.pk + "/03-tooling/fixtures", exist_ok=True)
        open(s.pk + "/04-documentation/BACKLOG_ROADMAP_FRAMEWORK_STANDARD_v1_0_0.md", "w").write("x\n"); open(s.pk + "/02-shacl-safeguards/backlog_shacl_v1_0_0.ttl", "w").write("x\n")
        if not git(s.a, "tag", "--list", "backlog-roadmap-framework-v*").strip(): git(s.a, "tag", "backlog-roadmap-framework-v1.0.0")
        fl = files({b + "_v1_2_0.py": (stub(a, 1), None) for _, b, a in KINDS}); fl["backlog_validate_v1_0_0.py"] = ("import sys\nsys.exit(0)\n", None); fl["fixtures/fixture_positive_v1_0_0.ttl"] = ("x\n", None)
        o = s.run(fl, onts=False)
        R["no ontologies folder, with shapes, standard, fixtures, validator and a release tag present: neither runs"] = ("section refuses" not in o)
    finally:
        s.close()
    rs = RealScratch(toolpath)
    try:
        o = rs.run()
        R["real package copy (T-box, shapes, standard, changelog, tag, register file, fixtures): silent about both sections"] = ("section refuses" not in o and "did not answer" not in o)
        o = rs.run(plant="number")
        R["real package copy: a numeric property with no origin is named as number origin only"] = ("number origin section refuses" in o and "doc coverage section refuses" not in o)
        o = rs.run(plant="class")
        R["real package copy: a class the standard does not name is named as doc coverage only"] = ("doc coverage section refuses" in o and "number origin section refuses" not in o)
    finally:
        rs.close()
    R.update(sec_extra(toolpath, cross))
    if fuzz: R.update(sec_fuzz(toolpath))
    elif grid: R["the grid of checker states: every refusal equals the reference model's, exactly"] = grid_matrix(toolpath)
    if deep:
        s = Scratch(toolpath)
        try:
            o = s.run(files_hang_default(s), tl=None, limit=200)
            R["with the limit unset a hanging checker is a refusal after a finite default (the default is a limit)"] = ("the gate's number origin section did not answer in time" in o)
        finally:
            s.close()
    R["the default time limit is 120 seconds"] = bool(re.search(r'BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"\)', open(toolpath, encoding="utf-8").read()))
    return R
SEC_MUTANTS_EXTRA = (
    ("review 19 A06: a doc coverage exit 3 is dropped when a versioned-name and a Gate K refusal stand", "        bad += gate_section_failures(HERE, PKG)", "        bad += [x for x in gate_section_failures(HERE, PKG) if not (\"doc coverage\" in x and \"(exit 3)\" in x and any(\"BP-D7\" in b for b in bad) and any(b.startswith(\"Gate K\") for b in bad))]"),
    ("the time limit is enlarged by a factor of 1.4", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=1.4 * int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))'),
    ("the time limit is enlarged by 0.5 s", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")) + 0.5'),
    ("the time limit is enlarged by 0.8 s", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")) + 0.8'),
    ("the time limit is reduced by a factor of 0.7", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=0.7 * int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))'),

    ("review 18 P01: the sections are skipped when exactly four refusals stand", "        bad += gate_section_failures(HERE, PKG)", "        bad += [] if len(bad) == 4 else gate_section_failures(HERE, PKG)"),
    ("review 18 P08: the sections are skipped when an arrival stands and the repository has no release tag", "        bad += gate_section_failures(HERE, PKG)", "        bad += [] if (arr and not tag) else gate_section_failures(HERE, PKG)"),
    ("review 18 P12: a checker exiting 200 is not refused", "        if r.returncode != 0:\n            lines = (r.stdout", "        if r.returncode not in (0, 200):\n            lines = (r.stdout"),
    ("review 18 P15: a checker exiting 250 with no output is not refused", "        if r.returncode != 0:\n            lines = (r.stdout", "        if r.returncode not in (0,) and not (r.returncode == 250 and not r.stdout.strip() and not r.stderr.strip()):\n            lines = (r.stdout"),
    ("review 18 P13: exit 33 with text on both channels names the stderr line first", "lines = (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or [\"no output\"])\n            hit", "lines = ((r.stderr.strip().splitlines() or r.stdout.strip().splitlines()) if r.returncode == 33 else (r.stdout.strip().splitlines() or r.stderr.strip().splitlines()) or [\"no output\"])\n            hit"),
)
if sys.argv[1:2] == ["--matrix"]:
    for n, ok in sec_matrix(tool).items(): expect(n, ok)
    print("VERDICT   :", "PASS" if not bad else "FAIL"); sys.exit(1 if bad else 0)
if sys.argv[1:2] == ["--grid"]:
    grid_matrix(tool)
    expect("the grid of checker states (every exit code with every output kind, both ways): every refusal equals the reference model's", not GRID_MISMATCH)
    print("VERDICT   :", "PASS" if not bad else "FAIL"); sys.exit(1 if bad else 0)
if sys.argv[1:2] == ["--extra"]:
    for n, ok in sec_extra(tool).items(): expect(n, ok)
    for what, old, nw in (m for m in SEC_MUTANTS_EXTRA):
        src0 = open(tool, encoding="utf-8").read()
        with tempfile.TemporaryDirectory() as md:
            mp = os.path.join(md, os.path.basename(tool)); open(mp, "w", encoding="utf-8").write(src0.replace(old, nw, 1))
            caught = not all(sec_extra(mp).values())
            if not caught:
                del GRID_MISMATCH[:]; grid_matrix(mp); caught = bool(GRID_MISMATCH); del GRID_MISMATCH[:]
            expect("mutant caught: " + what, caught)
    print("VERDICT   :", "PASS" if not bad else "FAIL"); sys.exit(1 if bad else 0)
base_R = sec_matrix(tool, deep=True)
for n, ok in base_R.items(): expect(n, ok)
SEC_MUTANTS = (
    ("the time limit is enlarged by a factor of 1.4", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=1.4 * int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))'),
    ("the time limit is enlarged by 0.5 s", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")) + 0.5'),
    ("the time limit is enlarged by 0.8 s", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")) + 0.8'),
    ("the time limit is reduced by a factor of 0.7", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=0.7 * int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))'),
    ("the number-origin check is not run", '("backlog_number_origin_v*.py", ["--strict"], "number origin")', '("backlog_none_v*.py", ["--strict"], "number origin")'),
    ("the doc-coverage check is not run", '("backlog_doc_coverage_gate_v*.py", [], "doc coverage")', '("backlog_none_v*.py", [], "doc coverage")'),
    ("number origin runs without --strict", '["--strict"], "number origin"', '[], "number origin"'),
    ("number origin runs with an extra argument", '["--strict"], "number origin"', '["--strict", "--x"], "number origin"'),
    ("doc coverage runs with --strict", '("backlog_doc_coverage_gate_v*.py", [], "doc coverage")', '("backlog_doc_coverage_gate_v*.py", ["--strict"], "doc coverage")'),
    ("a failure is not reported", 'out.append("the gate\'s %s section refuses', '(lambda *a: None)("the gate\'s %s section refuses'),
    ("only the first failing section is reported", 'out.append("the gate\'s %s section refuses (exit %d): %s" % (what, r.returncode, hit[-1][:240]))', 'out[:] = ["the gate\'s %s section refuses (exit %d): %s" % (what, r.returncode, hit[-1][:240])]'),
    ("the verdict line is dropped", '(exit %d): %s" % (what, r.returncode, hit[-1][:240])', '(exit %d)" % (what, r.returncode)'),
    ("the exit code is dropped", '(exit %d): %s" % (what, r.returncode, hit[-1][:240])', '(): %s" % hit[-1][:240]'),
    ("only exit 1 is a refusal", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode == 1:\n            lines = (r.stdout'),
    ("only exit 1 or 2 is a refusal", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode in (1, 2):\n            lines = (r.stdout'),
    ("the oldest checker version is chosen", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, pat)), key=semver_key) or [None])[0]'),
    ("the checker version is sorted as text", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, pat))) or [None])[-1]'),
    ("the checker is chosen by file time", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, pat)), key=os.path.getmtime) or [None])[-1]'),
    ("the checker is chosen by file time, oldest", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, pat)), key=os.path.getmtime) or [None])[0]'),
    ("no time limit", ', timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")))', ')'),
    ("no time limit on number origin", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=(None if what == "number origin" else int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")))'),
    ("no time limit on doc coverage", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=(None if what == "doc coverage" else int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")))'),
    ("a hang is reported under the other section's name", 'out.append("the gate\'s %s section did not answer in time (it takes under one second here): %s" % (what, os.path.basename(t)))', 'out.append("the gate\'s %s section did not answer in time (it takes under one second here): %s" % ("doc coverage" if what == "number origin" else "number origin", os.path.basename(t)))'),
    ("a hang is not a refusal", 'out.append("the gate\'s %s section did not answer in time', '(lambda *a: None)("the gate\'s %s section did not answer in time'),
    ("the loop stops at the first checker", '        if r.returncode != 0:\n            lines = (r.stdout', '        if r.returncode != 0 and not out:\n            lines = (r.stdout'),
    ("a hang stops the loop", 'continue\n        if r.returncode', 'break\n        if r.returncode'),
    ("a missing checker stops the loop", 'if not t:\n            continue', 'if not t:\n            break'),
    ("the sections run only when nothing else has refused", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not bad:               # v1.17.0'),
    ("the version key ignores the patch number", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, pat)), key=lambda p: tuple(semver_key(p))[:2]) or [None])[-1]'),
    ("the version key ignores the major number", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, pat)), key=lambda p: tuple(semver_key(p))[1:]) or [None])[-1]'),
    ("the checker is chosen by the length of its name", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, pat)), key=len) or [None])[-1]'),
    ("exit codes above 7 are not refusals", 'if r.returncode != 0:\n            lines = (r.stdout', 'if 0 < r.returncode < 8:\n            lines = (r.stdout'),
    ("a failing checker with no output is not refused", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode != 0 and r.stdout.strip():\n            lines = (r.stdout'),
    ("the output of a passing checker is printed", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode == 0 and r.stdout.strip(): out.append("note " + r.stdout.strip().splitlines()[-1])\n        if r.returncode != 0:\n            lines = (r.stdout'),
    ("the sections are skipped when a handover has arrived", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not any("handover" in b for b in bad):               # v1.17.0'),
    ("the sections are skipped when the vocabulary probe refused", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not any("vocabulary" in b for b in bad):               # v1.17.0'),
    ("the sections are skipped when the changelog entry is missing", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not any("changelog" in b.lower() for b in bad):               # v1.17.0'),
    ("the sections are skipped when three or more refusals stand", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and len(bad) < 3:               # v1.17.0'),
    ("stderr is not read", '(r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ["no output"])', '(r.stdout.strip().splitlines() or ["no output"])'),
    ("the first FAIL line is named, not the last", 'hit[-1][:240]', 'hit[0][:240]'),
    ("a passing checker that mentions FAIL is refused", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode != 0 or "FAIL" in r.stdout:\n            lines = (r.stdout'),
    ("a similarly named number-origin file is taken as the checker", '"backlog_number_origin_v*.py"', '"backlog_number_origin*v*.py"'),
    ("a similarly named doc-coverage file is taken as the checker", '"backlog_doc_coverage_gate_v*.py"', '"backlog_doc_coverage_gate*v*.py"'),
    ("the time limit is scaled down", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=0.3 * int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))'),
    ("the sections are skipped when a register file exists", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not newest(os.path.join(PKG, "01-ontologies", "backlog_abox_v*.ttl")):               # v1.17.0'),
    ("the sections are skipped when a T-box exists", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not newest(os.path.join(PKG, "01-ontologies", "backlog_tbox_v*.ttl")):               # v1.17.0'),
    ("the sections are skipped when a release tag exists", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not subprocess.run(["git", "tag", "--list"], cwd=REPO, capture_output=True, text=True).stdout.strip():               # v1.17.0'),
    ("the sections are skipped when a fixtures folder exists", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not os.path.isdir(os.path.join(HERE, "fixtures")):               # v1.17.0'),
    ("the sections are run in a package with no ontologies folder", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if True:               # v1.17.0'),
    ("exit codes 4, 5, 100, 126, 127 and 130 are not refusals", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode not in (0, 4, 5, 100, 126, 127, 130):\n            lines = (r.stdout'),
    ("stderr is read before stdout", '(r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ["no output"])', '(r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ["no output"])'),
    ("stdout and stderr are merged", '(r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ["no output"])', '((r.stdout + r.stderr).strip().splitlines() or ["no output"])'),
    ("only VERDICT lines are chosen", 'if "FAIL" in l or "VERDICT" in l]', 'if "VERDICT" in l]'),
    ("only FAIL lines are chosen", 'if "FAIL" in l or "VERDICT" in l]', 'if "FAIL" in l]'),
    ("the checker is searched for in sub-folders too", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, "**", pat), recursive=True), key=semver_key) or [None])[-1]'),
    ("the time limit is scaled to 0.8", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=0.8 * int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))'),
    ("the time limit is reduced by 0.3 s", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")) - 0.3'),
    ("the default time limit is 5 s while its text is kept", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=(int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")) if "BACKLOG_PREFLIGHT_SECTION_TIMEOUT" in os.environ else 5)'),
    ("the sections are skipped when Gate K refused", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not any("Gate K" in b for b in bad):               # v1.17.0'),
    ("the sections are skipped when the release-item accounting refused", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not any("release-item" in b for b in bad):               # v1.17.0'),
    ("with no output the first line is named", '["no output"])\n            hit', '["no output"])[::-1]\n            hit'),
    ("FAIL is matched in any case", 'if "FAIL" in l or "VERDICT" in l]', 'if "fail" in l.lower() or "VERDICT" in l]'),
    ("a passing checker that writes to stderr is refused", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode != 0 or r.stderr.strip():\n            lines = (r.stdout'),
    ("the second section is named with the first one's code and line", 'out.append("the gate\'s %s section refuses (exit %d): %s" % (what, r.returncode, hit[-1][:240]))', 'out.append("the gate\'s %s section refuses (exit %d): %s" % (what, (r.returncode if not out else int(out[0].split("exit ")[1].split(")")[0])), (hit[-1][:240] if not out else out[0].split("): ", 1)[1])))'),
    ("an exit code above 1 stops the next section", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode > 1: out.append("the gate\'s %s section refuses (exit %d): x" % (what, r.returncode)); break\n        if r.returncode != 0:\n            lines = (r.stdout'),
    ("the time limit is enlarged by 5 s", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")) + 5'),
    ("the time limit is floored at 4 s", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=max(4, int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120")))'),
    ("an unset time limit means no limit", 'timeout=int(os.environ.get("BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"))', 'timeout=(int(os.environ["BACKLOG_PREFLIGHT_SECTION_TIMEOUT"]) if "BACKLOG_PREFLIGHT_SECTION_TIMEOUT" in os.environ else None)'),
    ("the sections run when a shapes folder exists without an ontologies folder", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) or os.path.isdir(os.path.join(PKG, "02-shacl-safeguards")):               # v1.17.0'),
    ("the sections run when a release tag exists without an ontologies folder", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) or subprocess.run(["git", "tag", "--list"], cwd=REPO, capture_output=True, text=True).stdout.strip():               # v1.17.0'),
    ("a file with an unversioned name ranks first", 't = newest(os.path.join(here, pat))', 't = (sorted(glob.glob(os.path.join(here, pat)), key=lambda p: (9999, 0, 0) if not re.search(r"_v(\\d+)_(\\d+)_(\\d+)\\.[a-z]+$", p) else semver_key(p)) or [None])[-1]'),
    ("the unrelated refusals are dropped when the sections run", 'bad += gate_section_failures(HERE, PKG)', 'bad = gate_section_failures(HERE, PKG)'),
    ("a .txt file is taken as the number-origin checker", '"backlog_number_origin_v*.py"', '"backlog_number_origin_v*"'),
    ("a .txt file is taken as the doc-coverage checker", '"backlog_doc_coverage_gate_v*.py"', '"backlog_doc_coverage_gate_v*"'),
    ("a prefixed file is taken as the number-origin checker", '"backlog_number_origin_v*.py"', '"*backlog_number_origin_v*.py"'),
    ("a prefixed file is taken as the doc-coverage checker", '"backlog_doc_coverage_gate_v*.py"', '"*backlog_doc_coverage_gate_v*.py"'),
    ("stdout is not stripped before it is read", '(r.stdout.strip().splitlines() or r.stderr.strip().splitlines()', '(r.stdout.splitlines() or r.stderr.strip().splitlines()'),
    ("the fallback line comes from stderr when there is any", 'or lines[-1:]', 'or (r.stderr.strip().splitlines() or lines)[-1:]'),
    ("FAIL counts only at the start of a line", 'if "FAIL" in l or "VERDICT" in l]', 'if l.strip().startswith(("FAIL", "VERDICT"))]'),
    ("the first verdict line is named for an exit of 100 or more", 'hit[-1][:240]', '(hit[0] if r.returncode >= 100 else hit[-1])[:240]'),
    ("a non-zero exit that prints a PASS verdict is not refused", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode != 0 and "VERDICT: PASS" not in r.stdout:\n            lines = (r.stdout'),
    ("exit 10 is not a refusal", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode not in (0, 10):\n            lines = (r.stdout'),
    ("exit 42 is not a refusal", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode not in (0, 42):\n            lines = (r.stdout'),
    ("exits 66 to 98 are not refusals", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode != 0 and not 66 <= r.returncode <= 98:\n            lines = (r.stdout'),
    ("exits 132 to 253 are not refusals", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode != 0 and not 132 <= r.returncode <= 253:\n            lines = (r.stdout'),
    ("a multiple of 19 is not a refusal", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode != 0 and r.returncode % 19:\n            lines = (r.stdout'),
    ("exit 42 stops the loop", 'if r.returncode != 0:\n            lines = (r.stdout', 'if r.returncode == 42: break\n        if r.returncode != 0:\n            lines = (r.stdout'),
    ("exits 10 to 61 name the other section", '(what, r.returncode, hit[-1][:240])', '("doc coverage" if what == "number origin" and 10 <= r.returncode <= 61 else what, r.returncode, hit[-1][:240])'),
    ("the sections are skipped when exactly five refusals stand", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and len(bad) != 5:               # v1.17.0'),
    ("the sections are skipped when versioned name, vocabulary probe and Gate K refuse", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not (any("versioned" in b for b in bad) and any("vocabulary" in b for b in bad) and any("Gate K" in b for b in bad)):               # v1.17.0'),
    ("the sections are skipped when two release tags exist", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and len(subprocess.run(["git", "tag", "--list"], cwd=REPO, capture_output=True, text=True).stdout.split()) < 2:               # v1.17.0'),
    ("the doc-coverage glob is widened to any coverage gate", '"backlog_doc_coverage_gate_v*.py"', '"backlog_*coverage_gate_v*.py"'),
    ("the number-origin glob is widened to any number-origin file", '"backlog_number_origin_v*.py"', '"backlog_number_origin_*v*.py"'),
    ("an exit 5 section refusal is dropped when an unrelated refusal stands", 'bad += gate_section_failures(HERE, PKG)', 'bad += [x for x in gate_section_failures(HERE, PKG) if not (bad and "(exit 5)" in x)]'),
    ("an exit 255 section refusal is dropped beside a handover arrival", 'bad += gate_section_failures(HERE, PKG)', 'bad += [x for x in gate_section_failures(HERE, PKG) if not (any("handover" in b for b in bad) and "(exit 255)" in x)]'),
    ("a hang is not reported when the newest checker is not named 1_2_0", 'except subprocess.TimeoutExpired:\n            out.append(', 'except subprocess.TimeoutExpired:\n            if "_v1_2_0" not in t: continue\n            out.append('),
    ("the sections are skipped when the tag of the version already exists", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not subprocess.run(["git", "tag", "--list", PKGNAME + "-v" + v], cwd=REPO, capture_output=True, text=True).stdout.strip():               # v1.17.0'),
    ("the second section is dropped when both exit with the same code between 10 and 61", 'out.append("the gate\'s %s section refuses (exit %d): %s" % (what, r.returncode, hit[-1][:240]))', 'out.append("the gate\'s %s section refuses (exit %d): %s" % (what, r.returncode, hit[-1][:240])) if not (10 <= r.returncode <= 61 and out and ("(exit %d)" % r.returncode) in out[0]) else None'),
    ("exit 42 with output on stderr only is named as no output", '(r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ["no output"])', '(r.stdout.strip().splitlines() or ([] if r.returncode == 42 else r.stderr.strip().splitlines()) or ["no output"])'),
    ("blank stderr with empty stdout is named as an empty line", '(r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ["no output"])', '(r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ([""] if r.stderr else ["no output"]))'),
    ("two hangs are dropped beside an unrelated refusal", 'bad += gate_section_failures(HERE, PKG)', 'bad += (lambda g: [] if bad and sum("did not answer" in x for x in g) == 2 else g)(gate_section_failures(HERE, PKG))'),
    ("exits 42 and 63 are dropped beside a handover arrival", 'bad += gate_section_failures(HERE, PKG)', 'bad += [x for x in gate_section_failures(HERE, PKG) if not (any("handover" in b for b in bad) and ("(exit 42)" in x or "(exit 63)" in x))]'),
    ("the sections are skipped when no release tag exists", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and subprocess.run(["git", "tag", "--list"], cwd=REPO, capture_output=True, text=True).stdout.strip():               # v1.17.0'),
    ("the sections are skipped when a T-box exists without a register", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not (newest(os.path.join(PKG, "01-ontologies", "backlog_tbox_v*.ttl")) and not newest(os.path.join(PKG, "01-ontologies", "backlog_abox_v*.ttl"))):               # v1.17.0'),
    ("the sections are skipped when shapes and standard exist without a T-box", 'if os.path.isdir(os.path.join(PKG, "01-ontologies")):               # v1.17.0', 'if os.path.isdir(os.path.join(PKG, "01-ontologies")) and not (os.path.exists(os.path.join(PKG, "02-shacl-safeguards", "backlog_shacl_v1_0_0.ttl")) and os.path.exists(os.path.join(PKG, "04-documentation", "BACKLOG_ROADMAP_FRAMEWORK_STANDARD_v1_0_0.md")) and not newest(os.path.join(PKG, "01-ontologies", "backlog_tbox_v*.ttl"))):               # v1.17.0'),
    ("a checker in a sub-folder is preferred", 't = newest(os.path.join(here, pat))', 't = newest(os.path.join(here, "*", pat)) or newest(os.path.join(here, pat))'),
    ("the default time limit is very long", '"BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "120"', '"BACKLOG_PREFLIGHT_SECTION_TIMEOUT", "99999"'),
)
src = open(tool, encoding="utf-8").read()
import concurrent.futures
def run_mutant(m):
    what, old, new = m
    if old not in src: return (what, None)
    with tempfile.TemporaryDirectory() as md:
        mp = os.path.join(md, os.path.basename(tool)); open(mp, "w", encoding="utf-8").write(src.replace(old, new, 1))
        callsite = ("bad" in old) or ("01-ontologies" in old)
        R1 = sec_fuzz(mp)
        if not all(R1.values()): return (what, R1)
        return (what, sec_matrix(mp, deep=("time limit" in what), grid=False, cross=callsite, fuzz=False))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    mres = list(ex.map(run_mutant, SEC_MUTANTS))
for what, mR in mres:
    if mR is None: expect("mutant text found: " + what, False)
    else: expect("mutant caught: " + what, not all(mR.values()))
for g in GRID_MISMATCH: print("GRID MISMATCH (first three):", g)
print("VERDICT   :", "PASS" if not bad else "FAIL"); sys.exit(1 if bad else 0)
