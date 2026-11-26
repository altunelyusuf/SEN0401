#!/usr/bin/env python3
"""backlog_work_guard_probe v1.6.0 -- proof that the work guard discriminates and cannot pass over nothing (L-95).

Builds a real throwaway git repository, installs the guard with backlog_guard_install, and drives REAL git commits and
the REAL Claude hook script against fixtures/fixture_execution_ready_negative (cite by stem, L-123), where the lineage
Lin_Ready is fully built with one groomed item and Lin_Waiting has no Backlog stage. Every case states the outcome it
must produce, both halves: what must pass AND what must be refused. Exit 0 when every expectation holds, 1 otherwise.
"""
import glob, json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sv = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", p)[0]]
fx = sorted(glob.glob(os.path.join(HERE, "fixtures", "fixture_execution_ready_negative_v*.ttl")), key=sv)[-1]
TOOLS = ["backlog_work_guard", "backlog_session_brief", "backlog_execution_ready", "backlog_guard_claude_hook", "backlog_guard_install"]
bad = []


def sh(cwd, *cmd, inp=None, env=None):
    e = dict(os.environ); e.update(env or {})
    return subprocess.run(list(cmd), cwd=cwd, capture_output=True, text=True, input=inp, env=e)


def expect(name, ok):
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok: bad.append(name)


def fresh(lineage="Lin_Ready", work=("app/**",)):
    d = tempfile.mkdtemp(prefix="guardprobe_")
    sh(d, "git", "init", "-q"); sh(d, "git", "config", "user.email", "p@x"); sh(d, "git", "config", "user.name", "p")
    os.makedirs(os.path.join(d, "tools")); os.makedirs(os.path.join(d, "app")); os.makedirs(os.path.join(d, "docs"))
    for t in TOOLS:
        src = sorted(glob.glob(os.path.join(HERE, t + "_v*.py")), key=sv)[-1]
        shutil.copy(src, os.path.join(d, "tools"))
    shutil.copy(fx, os.path.join(d, "register.ttl"))
    open(os.path.join(d, "app", "main.py"), "w").write("print(1)\n"); open(os.path.join(d, "docs", "a.md"), "w").write("a\n")
    sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "-m", "baseline before the guard")
    args = [sys.executable, os.path.join(d, "tools", "backlog_guard_install_v1_2_0.py"), d, "--tooling-dir", "tools",
            "--register", "register.ttl", "--lineage", lineage]
    for w in work: args += ["--work-path", w]
    r = subprocess.run(args, capture_output=True, text=True)
    return d, r


def commit(d, msg, path="app/main.py", extra=(), noverify=False):
    open(os.path.join(d, path), "a").write("x\n")
    sh(d, "git", "add", "-A")
    return sh(d, "git", "commit", "-q", *(["--no-verify"] if noverify else []), "-m", msg, *extra)


if sys.argv[1:] == ["--deps"]:
    print(os.path.abspath(__file__)); print(fx)
    for t in TOOLS:
        print(sorted(glob.glob(os.path.join(HERE, t + "_v*.py")), key=sv)[-1])
    sys.exit(0)


d, r = fresh()
expect("installer runs and reports the layers", r.returncode == 0 and "installed:" in r.stdout)
s = json.load(open(os.path.join(d, ".claude", "settings.json")))
expect("Claude hooks registered for SessionStart and PreToolUse",
       "SessionStart" in s["hooks"] and "PreToolUse" in s["hooks"])
expect("CI workflow written", os.path.isfile(os.path.join(d, ".github", "workflows", "backlog-work-guard.yml")))
r = commit(d, "work without any item")
expect("REFUSED: a work commit with no Work-Item trailer", r.returncode != 0 and "names no `Work-Item" in r.stdout + r.stderr)
r = commit(d, "work on a missing item\n\nWork-Item: S_Missing")
expect("REFUSED: a Work-Item that is not in the register", r.returncode != 0 and "not found in the register" in r.stdout + r.stderr)
r = commit(d, "work on an ungroomed item\n\nWork-Item: S_NoCriterion")
expect("REFUSED: a Work-Item with no acceptance criterion", r.returncode != 0 and "acceptance criterion" in r.stdout + r.stderr)
r = commit(d, "work on a proposed item\n\nWork-Item: S_Proposed")
expect("REFUSED: a Work-Item that is not Ready or InProgress", r.returncode != 0 and "Ready or InProgress" in r.stdout + r.stderr)
r = commit(d, "work on a groomed item\n\nWork-Item: S_Groomed")
expect("ACCEPTED: a work commit naming a groomed, planned item", r.returncode == 0)
r = commit(d, "docs only, no item needed", path="docs/a.md")
expect("ACCEPTED: a commit that touches no governed work needs no item", r.returncode == 0)
r = commit(d, "skipped the hook", noverify=True)
expect("a --no-verify commit gets in locally (the hook alone can be skipped)", r.returncode == 0)
g = os.path.join(d, "tools", "backlog_work_guard_v1_5_0.py")
r = sh(d, sys.executable, g, "range", "HEAD~2..HEAD")
expect("REFUSED by the CI layer: the range check names the skipped commit",
       r.returncode == 2 and "names no Work-Item" in r.stdout and "examined" in r.stdout)
r = sh(d, sys.executable, g, "range", "HEAD~2..HEAD~1")
expect("ACCEPTED by the CI layer: a range holding only compliant commits", r.returncode == 0 and "VERDICT: PASS" in r.stdout)
hook = os.path.join(d, "tools", "backlog_guard_claude_hook_v1_1_0.py")
ev = lambda **k: json.dumps(dict({"cwd": d, "hook_event_name": "PreToolUse"}, **k))
r = sh(d, sys.executable, hook, inp=ev(tool_name="Edit", tool_input={"file_path": os.path.join(d, "app", "main.py")}))
expect("ACCEPTED at edit time: lineage ready", r.returncode == 0)
r = sh(d, sys.executable, hook, inp=ev(tool_name="Bash", tool_input={"command": "echo hi"}))
expect("ACCEPTED: a Bash command that writes nothing governed", r.returncode == 0)

sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "commit the installed guard files")
d5 = tempfile.mkdtemp(prefix="guardclone_"); shutil.rmtree(d5); sh(os.path.dirname(d), "git", "clone", "-q", d, d5)
sh(d5, "git", "config", "user.email", "p@x"); sh(d5, "git", "config", "user.name", "p")
r = commit(d5, "work in a fresh clone, hooks not armed yet")
expect("a fresh clone has no git hooks (they do not travel): the commit gets in", r.returncode == 0)
sh(d5, "git", "reset", "-q", "--hard", "HEAD~1")
r = sh(d5, sys.executable, os.path.join(d5, "tools", "backlog_guard_claude_hook_v1_1_0.py"), inp=json.dumps({"cwd": d5, "hook_event_name": "SessionStart"}))
expect("SessionStart re-arms the git hooks in the clone", r.returncode == 0 and "re-armed" in r.stdout)
r = commit(d5, "work in a fresh clone after the session start")
expect("REFUSED in the fresh clone once the session start has re-armed the hooks", r.returncode != 0 and "names no `Work-Item" in r.stdout + r.stderr)
shutil.rmtree(d5, ignore_errors=True)

bare = tempfile.mkdtemp(prefix="guardbare_"); sh(bare, "git", "init", "-q", "--bare")
sh(d, "git", "remote", "add", "origin", bare)
r = sh(d, "git", "push", "-q", "origin", "HEAD:refs/heads/work")
expect("REFUSED at push: the range holds the commit that skipped the commit hook", r.returncode != 0 and "names no Work-Item" in r.stdout + r.stderr)
d4, r = fresh()
bare4 = tempfile.mkdtemp(prefix="guardbare_"); sh(bare4, "git", "init", "-q", "--bare"); sh(d4, "git", "remote", "add", "origin", bare4)
commit(d4, "groomed work\n\nWork-Item: S_Groomed")
r = sh(d4, "git", "push", "-q", "origin", "HEAD:refs/heads/work")
expect("ACCEPTED at push: a range of compliant commits", r.returncode == 0)
shutil.rmtree(bare, ignore_errors=True); shutil.rmtree(bare4, ignore_errors=True); shutil.rmtree(d4, ignore_errors=True)

d2, r = fresh("Lin_Waiting")
hook2 = os.path.join(d2, "tools", "backlog_guard_claude_hook_v1_1_0.py")
ev2 = lambda **k: json.dumps(dict({"cwd": d2, "hook_event_name": "PreToolUse"}, **k))
r = sh(d2, sys.executable, hook2, inp=ev2(tool_name="Write", tool_input={"file_path": os.path.join(d2, "app", "new.py")}))
expect("REFUSED at edit time: lineage has no Backlog stage (the Lineage_2 state)",
       r.returncode == 2 and "Stage_Backlog" in r.stderr and "NEXT REQUIRED ACT" in r.stderr)
r = sh(d2, sys.executable, hook2, inp=ev2(tool_name="Bash", tool_input={"command": "sed -i s/1/2/ app/main.py"}))
expect("REFUSED at edit time: a Bash write to a governed path", r.returncode == 2)
r = sh(d2, sys.executable, hook2, inp=ev2(tool_name="Write", tool_input={"file_path": os.path.join(d2, "docs", "n.md")}))
expect("ACCEPTED at edit time: a non-governed path stays writable on the same lineage", r.returncode == 0)
r = sh(d2, sys.executable, hook2, inp=json.dumps({"cwd": d2, "hook_event_name": "SessionStart"}))
expect("SessionStart puts NOT READY and the next required act into the session",
       r.returncode == 0 and "NOT READY" in r.stdout and "build the Backlog stage" in r.stdout)
d3, r = fresh("Lin_Ready", work=("nowhere/**",))
r = commit(d3, "work", path="docs/a.md")
expect("REFUSED: a work path that matches no tracked file (a guard over nothing)",
       r.returncode != 0 and "matches no tracked file" in r.stdout + r.stderr)
r = subprocess.run([sys.executable, os.path.join(d, "tools", "backlog_guard_install_v1_2_0.py"), d, "--tooling-dir", "tools",
                    "--register", "register.ttl", "--lineage", "Lin_Ready", "--work-path", "app/**"], capture_output=True, text=True)
s2 = json.load(open(os.path.join(d, ".claude", "settings.json")))
expect("installer is idempotent: hooks are not duplicated", len(s2["hooks"]["PreToolUse"]) == 1 and r.returncode == 0)
for x in (d, d2, d3): shutil.rmtree(x, ignore_errors=True)

# ---- v1.2.0 (G119): the range is judged by the configuration and the register that were in force before it ----
def committed():
    """A fresh repository whose installed guard files are committed (the state a consumer is in once it adopted the guard)."""
    d, r = fresh()
    sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "commit the installed guard files")
    return d
gv = lambda d: os.path.join(d, "tools", "backlog_work_guard_v1_5_0.py")
head = lambda d: sh(d, "git", "rev-parse", "HEAD").stdout.strip()

d6 = committed(); base = head(d6)
cfgp = os.path.join(d6, ".backlog-guard.json"); c = json.load(open(cfgp)); c["exempt_paths"] = ["app/**"]; json.dump(c, open(cfgp, "w"), indent=2)
sh(d6, "git", "add", "-A"); r = sh(d6, "git", "commit", "-q", "-m", "loosen the guard\n\nWork-Item: S_Groomed")
expect("a configuration change with a ready Work-Item gets in (the configuration is governed, not frozen)", r.returncode == 0)
r = commit(d6, "work after the loosening, no item", noverify=True)
r = sh(d6, sys.executable, gv(d6), "range", base + "..HEAD")
expect("REFUSED by the range check: a configuration loosened inside the range does not release the later commit",
       r.returncode == 2 and "names no Work-Item" in r.stdout and "read at" in r.stdout)
r = sh(d6, sys.executable, gv(d6), "range", "HEAD~1..HEAD")
expect("the same commit is exempt in the NEXT range (the loosening is in force at its base)", r.returncode == 0 and "VERDICT: PASS" in r.stdout)

d7 = committed()
c0 = json.load(open(os.path.join(d7, ".backlog-guard.json"))); c0["note"] = "edited"; json.dump(c0, open(os.path.join(d7, ".backlog-guard.json"), "w"), indent=2)
sh(d7, "git", "add", "-A"); r = sh(d7, "git", "commit", "-q", "-m", "edit the guard configuration, no item")
expect("REFUSED: the guard configuration is governed work (protected path)", r.returncode != 0 and "names no `Work-Item" in r.stdout + r.stderr)
c = json.load(open(os.path.join(d7, ".backlog-guard.json"))); sh(d7, "git", "checkout", "--", ".backlog-guard.json")
c["exempt_paths"] = [".githooks/**", ".backlog-guard.json", "tools/**"]; json.dump(c, open(os.path.join(d7, ".backlog-guard.json"), "w"), indent=2)
sh(d7, "git", "add", "-A"); sh(d7, "git", "commit", "-q", "--no-verify", "-m", "exempt the guard files")
r = commit(d7, "edit a hook, no item", path=".githooks/commit-msg")
expect("REFUSED: no exempt path releases the guard's own files", r.returncode != 0 and "names no `Work-Item" in r.stdout + r.stderr)
r = commit(d7, "edit the vendored guard, no item", path="tools/backlog_work_guard_v1_5_0.py")
expect("REFUSED: the vendored tooling directory is governed work", r.returncode != 0 and "names no `Work-Item" in r.stdout + r.stderr)

d8 = committed(); base8 = head(d8)
reg = os.path.join(d8, "register.ttl"); t = open(reg).read()
commit(d8, "work on a proposed item, hook skipped\n\nWork-Item: S_Proposed", noverify=True)
open(reg, "w").write(t.replace("ex:S_Proposed a backlog:Story ; backlog:hasIdentifier \"S_Proposed\" ; backlog:hasState backlog:Proposed", "ex:S_Proposed a backlog:Story ; backlog:hasIdentifier \"S_Proposed\" ; backlog:hasState backlog:Ready"))
sh(d8, "git", "add", "-A"); sh(d8, "git", "commit", "-q", "-m", "ready the item afterwards (register edit)")
r = sh(d8, sys.executable, gv(d8), "range", base8 + "..HEAD")
expect("REFUSED: work committed BEFORE its item was ready is not rescued by a later register edit (the register is read at the commit's parent)",
       r.returncode == 2 and "Ready or InProgress" in r.stdout)

d9 = committed(); base9 = head(d9)
reg = os.path.join(d9, "register.ttl"); t = open(reg).read()
open(reg, "w").write(t.replace("ex:S_Proposed a backlog:Story ; backlog:hasIdentifier \"S_Proposed\" ; backlog:hasState backlog:Proposed", "ex:S_Proposed a backlog:Story ; backlog:hasIdentifier \"S_Proposed\" ; backlog:hasState backlog:Ready"))
sh(d9, "git", "add", "-A"); sh(d9, "git", "commit", "-q", "-m", "ready the item (register edit)")
r = commit(d9, "work on the item readied one commit earlier\n\nWork-Item: S_Proposed")
expect("ACCEPTED locally: ready before the commit is what the commit hook asks", r.returncode == 0)
r = sh(d9, sys.executable, gv(d9), "range", base9 + "..HEAD")
expect("ACCEPTED by the range check, and the item readied inside the range is reported",
       r.returncode == 0 and "NOTE" in r.stdout and "became ready inside this range" in r.stdout)
r = sh(d9, sys.executable, gv(d9), "range", "--strict-base", base9 + "..HEAD")
expect("REFUSED under --strict-base: readiness must be established before the range began",
       r.returncode == 2 and "was not ready before the range began" in r.stdout)
r = sh(d9, sys.executable, gv(d9), "range", "HEAD~1..HEAD")
expect("ACCEPTED under the ordinary range once the item was ready at its base", r.returncode == 0 and "NOTE" not in r.stdout)
wf = open(os.path.join(d9, ".github", "workflows", "backlog-work-guard.yml")).read()
expect("the CI file runs the guard as it was BEFORE the range (git archive of the base), so a commit cannot edit the judge",
       "git archive" in wf and "--config .backlog-guard.json" in wf)
for x in (d6, d7, d8, d9): shutil.rmtree(x, ignore_errors=True)

# G122: the session-start status carries the brief, and does not stop speaking when the brief is absent
dB, _ = fresh()
r = sh(dB, sys.executable, os.path.join(dB, "tools", "backlog_work_guard_v1_5_0.py"), "--config", ".backlog-guard.json", "status")
expect("the status prints the brief (focus, items in progress, checkpoints due, what a close needs)",
       r.returncode == 0 and all(k in r.stdout for k in ("FOCUS", "IN PROGRESS", "DUE", "TO CLOSE")) and "NEXT REQUIRED ACT" in r.stdout)
os.remove(os.path.join(dB, "tools", "backlog_session_brief_v1_0_0.py"))
r = sh(dB, sys.executable, os.path.join(dB, "tools", "backlog_work_guard_v1_5_0.py"), "--config", ".backlog-guard.json", "status")
expect("without the brief tool the status still speaks and says what is missing",
       r.returncode == 0 and "NEXT REQUIRED ACT" in r.stdout and "BRIEF" in r.stdout and "not shown" in r.stdout)
shutil.rmtree(dB, ignore_errors=True)


# ---- v1.3.0 (G123): register by pattern, the guard-install commit, no rdflib needed to decide, the Bash write test ----
dP, _ = fresh("Lin_Waiting")
os.makedirs(os.path.join(dP, "registers"))
sh(dP, "git", "mv", "register.ttl", "registers/r_v1_0_0.ttl") if False else shutil.move(os.path.join(dP, "register.ttl"), os.path.join(dP, "registers", "r_v1_0_0.ttl"))
cp_ = os.path.join(dP, ".backlog-guard.json"); c = json.load(open(cp_)); c["register"] = ["registers/r_v*.ttl"]; json.dump(c, open(cp_, "w"), indent=2)
sh(dP, "git", "add", "-A"); sh(dP, "git", "commit", "-q", "--no-verify", "-m", "setup: the register cited by pattern and the guard committed")
gP = os.path.join(dP, "tools", "backlog_work_guard_v1_5_0.py")
r = sh(dP, sys.executable, gP, "status")
expect("a register cited by pattern is read (the lineage state is reported)", r.returncode == 0 and "NOT READY" in r.stdout)
shutil.move(os.path.join(dP, "registers", "r_v1_0_0.ttl"), os.path.join(dP, "registers", "r_v1_1_0.ttl"))
sh(dP, "git", "add", "-A"); r = sh(dP, "git", "commit", "-q", "-m", "BP-D7: the register gets a new version, the configuration is untouched")
expect("ACCEPTED while NOT READY: renaming a register cited by pattern touches only the register", r.returncode == 0)
r = sh(dP, sys.executable, gP, "status")
expect("the renamed register is the one read", r.returncode == 0 and "NOT READY" in r.stdout)
r = sh(dP, sys.executable, gP, "range", "HEAD~1..HEAD")
expect("the range check resolves the register at each revision", r.returncode == 0 and "VERDICT: PASS" in r.stdout)

# the guard-install commit
tf = os.path.join(dP, "tools", "backlog_work_guard_v1_5_0.py")
open(tf, "a").write("# re-vendored\n"); sh(dP, "git", "add", "-A")
r = sh(dP, "git", "commit", "-q", "-m", "re-vendor the guard, no marker")
expect("REFUSED while NOT READY: guard files changed with neither a Work-Item nor Guard-Install", r.returncode != 0 and "names no `Work-Item" in r.stdout + r.stderr)
r = sh(dP, "git", "commit", "-q", "-m", "re-vendor the guard\n\nGuard-Install: v1.3.0 vendored")
expect("ACCEPTED while NOT READY: a commit of only the guard's own files that states Guard-Install", r.returncode == 0)
open(tf, "a").write("# again\n"); open(os.path.join(dP, "app", "main.py"), "a").write("x\n"); sh(dP, "git", "add", "-A")
r = sh(dP, "git", "commit", "-q", "-m", "guard files with work mixed in\n\nGuard-Install: sneaked")
expect("REFUSED: Guard-Install does not release governed work committed beside the guard files", r.returncode != 0)
sh(dP, "git", "reset", "-q", "--hard", "HEAD")
open(os.path.join(dP, ".backlog-guard.json"), "a").write("\n"); sh(dP, "git", "add", "-A")
r = sh(dP, "git", "commit", "-q", "-m", "configuration under the install marker\n\nGuard-Install: sneaked")
expect("REFUSED: Guard-Install does not cover the configuration", r.returncode != 0)
sh(dP, "git", "reset", "-q", "--hard", "HEAD")
r = sh(dP, sys.executable, gP, "range", "HEAD~2..HEAD")
expect("the range check lists the guard-install commit without judging it by readiness", r.returncode == 0 and "guard-install commit" in r.stdout)

# no rdflib: python3 -S sees no site-packages
hP = os.path.join(dP, "tools", "backlog_guard_claude_hook_v1_1_0.py")
evP = lambda **k: json.dumps(dict({"cwd": dP, "hook_event_name": "PreToolUse"}, **k))
bash = lambda c: sh(dP, sys.executable, "-S", hP, inp=evP(tool_name="Bash", tool_input={"command": c}))
r = bash("python3 -m pip install rdflib pyshacl")
expect("ACCEPTED without rdflib: the command that installs rdflib", r.returncode == 0)
r = sh(dP, sys.executable, "-S", hP, inp=evP(tool_name="Write", tool_input={"file_path": os.path.join(dP, "app", "n.py")}))
expect("REFUSED without rdflib: a governed edit, and the reason names rdflib", r.returncode == 2 and "rdflib" in r.stderr)
r = sh(dP, sys.executable, "-S", hP, inp=json.dumps({"cwd": dP, "hook_event_name": "SessionStart"}))
expect("the session starts without rdflib and says the lineage state is not shown", r.returncode == 0 and "not shown" in r.stdout)

# the Bash write test
r = bash("grep -rn foo app > /tmp/guardprobe_out")
expect("ACCEPTED: a read of a governed directory whose redirect writes elsewhere", r.returncode == 0)
r = bash("echo x > app/new.py")
expect("REFUSED: a redirect into a governed path", r.returncode == 2)
r = bash("cp app/main.py /tmp/guardprobe_copy")
expect("ACCEPTED: copying a governed file OUT of the governed paths", r.returncode == 0)
r = bash("cp /tmp/guardprobe_copy app/main.py")
expect("REFUSED: copying INTO a governed path", r.returncode == 2)
r = bash("sed -i s/1/2/ app/main.py")
expect("REFUSED: sed -i on a governed file", r.returncode == 2)
shutil.rmtree(dP, ignore_errors=True)

# v1.4.0 (G161): a renamed register, and the configuration change that narrows an exact register path to its pattern
dV, r = fresh(lineage="Lin_Waiting")
shutil.move(os.path.join(dV, "register.ttl"), os.path.join(dV, "register_v1_0_0.ttl"))
cfgp = os.path.join(dV, ".backlog-guard.json"); cfg = json.load(open(cfgp)); cfg["register"] = ["register_v1_0_0.ttl"]; json.dump(cfg, open(cfgp, "w"))
sh(dV, "git", "add", "-A"); sh(dV, "git", "commit", "-q", "--no-verify", "-m", "version the register")
gV = os.path.join(dV, "tools", "backlog_work_guard_v1_5_0.py")
sh(dV, "git", "mv", "register_v1_0_0.ttl", "register_v1_1_0.ttl"); sh(dV, "git", "commit", "-q", "--no-verify", "-m", "rename the register")
r = sh(dV, sys.executable, gV, "status")
expect("a register renamed to a later version is still read through its exact path (G161)", "cannot read the register" not in r.stdout + r.stderr and r.returncode in (0, 2))
cfg = json.load(open(cfgp)); cfg["register"] = ["register_v*.ttl"]; json.dump(cfg, open(cfgp, "w"))
sh(dV, "git", "add", ".backlog-guard.json")
r = sh(dV, "git", "commit", "-q", "-m", "narrow the register path\n\nGuard-Install: pattern of the same stem")
expect("ACCEPTED while NOT READY: the configuration only replaces the exact register path by its pattern, Guard-Install stated (G161)", r.returncode == 0)
cfg["exempt_paths"] = ["app/**"]; json.dump(cfg, open(cfgp, "w"))
sh(dV, "git", "add", ".backlog-guard.json")
r = sh(dV, "git", "commit", "-q", "-m", "loosen\n\nGuard-Install: sneaked")
expect("REFUSED: a configuration change that does more than narrow the register path, even with Guard-Install", r.returncode != 0)
sh(dV, "git", "reset", "-q", "--hard", "HEAD")
shutil.rmtree(dV, ignore_errors=True)

# ---- v1.6.0 (box 63, G248): arming never blocks the lineage it arms, and no state of a lineage is without a permitted act ----
import importlib.util
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
BL = "http://example.org/backlog#"; EXN = "http://example.org/fixture#"
guard_src = sorted(glob.glob(os.path.join(HERE, "backlog_work_guard_v*.py")), key=sv)[-1]
spec = importlib.util.spec_from_file_location("wg", guard_src); WG = importlib.util.module_from_spec(spec); spec.loader.exec_module(WG)
regs_dir = tempfile.mkdtemp(prefix="guardstates_")
def state_register(state):
    """A copy of the fixture register in which the lineage Lin_Ready is in the named guard state (installed: the lineage is absent)."""
    g = Graph(); g.parse(fx, format="turtle")
    ns = None
    for s in g.subjects(RDF.type, URIRef(BL + "Lineage")):
        if str(s).endswith("Lin_Ready"): ns = str(s)[:-len("Lin_Ready")]
    L = URIRef(ns + "Lin_Ready")
    stages = ["Stage_Mission", "Stage_Scope", "Stage_Goal", "Stage_Objective", "Stage_Backlog"]
    if state == "installed":
        lin = "Lin_Absent"
    else:
        lin = "Lin_Ready"
        cut = {"mission": 0, "scope": 1, "goal": 2, "objective": 3, "backlog": 4}.get(state)
        if cut is not None:
            for o in list(g.subjects(RDF.type, URIRef(BL + "StageOutput"))):
                if (o, URIRef(BL + "belongsToLineage"), L) in g and any((o, URIRef(BL + "outputOfStage"), URIRef(BL + st)) in g for st in stages[cut:]):
                    for p_, o_ in list(g.predicate_objects(o)): g.remove((o, p_, o_))
        if state == "inbox":
            it = URIRef(ns + "It_Open_Probe")
            g.add((it, RDF.type, URIRef(BL + "Iteration"))); g.add((it, URIRef(BL + "belongsToLineage"), L)); g.add((it, URIRef(BL + "hasState"), URIRef(BL + "InProgress")))
    path = os.path.join(regs_dir, state + ".ttl"); g.serialize(path, format="turtle")
    return path, lin
def clone_in_state(state):
    path, lin = state_register(state)
    d = tempfile.mkdtemp(prefix="guardstate_")
    sh(d, "git", "init", "-q"); sh(d, "git", "config", "user.email", "p@x"); sh(d, "git", "config", "user.name", "p")
    os.makedirs(os.path.join(d, "tools")); os.makedirs(os.path.join(d, "app")); os.makedirs(os.path.join(d, "docs"))
    for tname in TOOLS:
        shutil.copy(sorted(glob.glob(os.path.join(HERE, tname + "_v*.py")), key=sv)[-1], os.path.join(d, "tools"))
    shutil.copy(path, os.path.join(d, "register.ttl"))
    open(os.path.join(d, "app", "main.py"), "w").write("print(1)\n"); open(os.path.join(d, "docs", "a.md"), "w").write("a\n")
    sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "-m", "baseline before the guard")
    inst = sorted(glob.glob(os.path.join(HERE, "backlog_guard_install_v*.py")), key=sv)[-1]
    r = subprocess.run([sys.executable, inst, d, "--tooling-dir", "tools", "--register", "register.ttl", "--lineage", lin, "--work-path", "app/**", "--work-path", "register.ttl"], capture_output=True, text=True)
    return d, r
no_act = 0
ARM = ["add", ".backlog-guard.json", ".githooks", ".claude", ".github", "tools"]
for state in ("installed", "mission", "scope", "goal", "objective", "backlog", "ready", "inbox"):
    d, r = clone_in_state(state)
    sh(d, "git", *ARM)
    r = sh(d, "git", "commit", "-q", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
    expect("[%s] ACCEPTED: the commit that arms the clone, with the configuration, needs no Work-Item" % state, r.returncode == 0)
    open(os.path.join(d, "register.ttl"), "a").write("# a record of the chain\n"); sh(d, "git", "add", "register.ttl")
    r = sh(d, "git", "commit", "-q", "-m", "record the chain")
    expect("[%s] ACCEPTED: a commit that changes only the register needs no Work-Item" % state, r.returncode == 0)
    open(os.path.join(d, "tools", "note.txt"), "w").write("x\n"); sh(d, "git", "add", "tools/note.txt")
    r = sh(d, "git", "commit", "-q", "-m", "guard files", "-m", "Guard-Install: a note")
    expect("[%s] ACCEPTED: a commit of the guard's own files that states Guard-Install needs no Work-Item" % state, r.returncode == 0)
    open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "app/main.py")
    r = sh(d, "git", "commit", "-q", "-m", "work with no item")
    out = r.stdout + r.stderr
    acts = WG.STATE_ACTS[state] + list(WG.COMMON_ACTS.values())
    expect("[%s] REFUSED, and the refusal names every permitted act of the state" % state, r.returncode != 0 and ("PERMITTED in this state (%s)" % state) in out and all(a in out for a in acts))
    if not acts: no_act += 1
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    shutil.rmtree(d, ignore_errors=True)
expect("no state of the lineage is without a permitted act (the count of such states is 0)", no_act == 0)
# the three dead ends of 2026-11-21, one by one
d, r = clone_in_state("backlog")
r2 = subprocess.run([sys.executable, sorted(glob.glob(os.path.join(HERE, "backlog_guard_install_v*.py")), key=sv)[-1], d, "--tooling-dir", "tools", "--register", "register.ttl", "--lineage", "Lin_Waiting", "--work-path", "nowhere/**"], capture_output=True, text=True)
sh(d, "git", *ARM); r = sh(d, "git", "commit", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
expect("dead end 1: ACCEPTED, with a warning, the arming commit whose work path matches no tracked file while the lineage is not ready", r.returncode == 0 and "matches no tracked file" in r.stdout + r.stderr and "warning" in r.stdout + r.stderr)
shutil.rmtree(d, ignore_errors=True)
d, r = clone_in_state("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
cfgp = os.path.join(d, ".backlog-guard.json"); cfg = json.load(open(cfgp)); cfg["work_paths"] = ["nowhere/**"]; json.dump(cfg, open(cfgp, "w")); sh(d, "git", "add", ".backlog-guard.json")
r = sh(d, "git", "commit", "-q", "-m", "retarget", "-m", "Guard-Install: sneaked")
expect("REFUSED: a configuration change after arming is governed work, even with Guard-Install (the first-install exception is not a way round)", r.returncode != 0)
sh(d, "git", "reset", "-q", "--hard", "HEAD")
open(os.path.join(d, "app", "main.py"), "a").write("x\n"); open(os.path.join(d, "tools", "note.txt"), "w").write("x\n"); sh(d, "git", "add", "-A")
r = sh(d, "git", "commit", "-q", "-m", "guard file and work together", "-m", "Guard-Install: mixed")
expect("REFUSED: a Guard-Install commit that also changes governed work", r.returncode != 0)
sh(d, "git", "reset", "-q", "--hard", "HEAD")
dd, r = clone_in_state("ready")
sh(dd, "git", "add", "-A")
r = sh(dd, "git", "commit", "-q", "-m", "Install the work guard", "-m", "Guard-Install: first installation", "--allow-empty")
expect("ACCEPTED: the first installation also in a lineage that is ready and whose work path matches a tracked file", r.returncode == 0)
shutil.rmtree(dd, ignore_errors=True)
# a lineage that is ready and has a work path matching nothing is still refused (a guard over nothing proves nothing once work may start)
cfg = json.load(open(cfgp)); cfg["work_paths"] = ["nowhere/**"]; json.dump(cfg, open(cfgp, "w"))
r = sh(d, sys.executable, os.path.join(d, "tools", os.path.basename(guard_src)), "status")
expect("the status of a ready lineage with a work path that matches nothing reports a guard error, not a warning", "GUARD CONFIG: work path" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# ---- repair round 1 of box 63: every commit kind in every state, the range layer, the refusals that name the acts ----
STATES = ("installed", "mission", "scope", "goal", "objective", "backlog", "ready", "inbox")
def armed_clone(state, extra_work=(), reg=None, untracked=(), regname="register.ttl"):
    path, lin = state_register(state)
    if reg: path = reg
    d = tempfile.mkdtemp(prefix="guardstate_")
    sh(d, "git", "init", "-q"); sh(d, "git", "config", "user.email", "p@x"); sh(d, "git", "config", "user.name", "p")
    os.makedirs(os.path.join(d, "tools")); os.makedirs(os.path.join(d, "app")); os.makedirs(os.path.join(d, "docs"))
    for tname in TOOLS:
        shutil.copy(sorted(glob.glob(os.path.join(HERE, tname + "_v*.py")), key=sv)[-1], os.path.join(d, "tools"))
    shutil.copy(path, os.path.join(d, regname))
    open(os.path.join(d, "app", "main.py"), "w").write("print(1)\n"); open(os.path.join(d, "docs", "a.md"), "w").write("a\n")
    sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "-m", "baseline before the guard")
    base = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
    for u in untracked:
        os.makedirs(os.path.dirname(os.path.join(d, u)), exist_ok=True); open(os.path.join(d, u), "w").write("x\n")
    inst = sorted(glob.glob(os.path.join(HERE, "backlog_guard_install_v*.py")), key=sv)[-1]
    args = [sys.executable, inst, d, "--tooling-dir", "tools", "--register", regname, "--lineage", lin, "--work-path", "app/**", "--work-path", regname]
    for w in extra_work: args += ["--work-path", w]
    ir = subprocess.run(args, capture_output=True, text=True)
    return d, base, ir
for state in STATES:
    d, base, ir = armed_clone(state)
    expect("[%s] the installer prints the arming command with the Guard-Install trailer" % state, "Guard-Install: first installation" in ir.stdout and "git commit" in ir.stdout)
    addline = [l for l in ir.stdout.splitlines() if "git add" in l]
    expect("[%s] the installer's printed git add lists the configuration, the hooks, the session settings, the workflow and the tooling directory" % state, bool(addline) and all(x in addline[0] for x in (".backlog-guard.json", ".githooks", ".claude/settings.json", ".github/workflows/backlog-work-guard.yml", "tools")))
    na = sorted(glob.glob(os.path.join(HERE, "backlog_next_act_v*.py")), key=sv)[-1]
    sh(d, "git", *ARM)
    r = sh(d, sys.executable, na, "armed", "--root", d)
    expect("[%s] armed refuses arming that is staged but not committed (HEAD is tested, not the index)" % state, r.returncode == 2 and "NOT ARMED" in r.stdout)
    sh(d, "git", "reset", "-q")
    # the first installation must carry nothing but the guard's files and the configuration, and must state Guard-Install
    sh(d, "git", *ARM); open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "app/main.py")
    r = sh(d, "git", "commit", "-q", "-m", "arm and work", "-m", "Guard-Install: first installation")
    expect("[%s] REFUSED: the first installation that also changes governed work" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "app/main.py"); sh(d, "git", "checkout", "-q", "--", "app/main.py")
    r = sh(d, "git", "commit", "-q", "-m", "Install the work guard")
    expect("[%s] REFUSED: the first installation without the Guard-Install trailer" % state, r.returncode != 0)
    open(os.path.join(d, "docs", "a.md"), "a").write("x\n"); sh(d, "git", "add", "docs/a.md")
    r = sh(d, "git", "commit", "-q", "-m", "arm and docs", "-m", "Guard-Install: first installation")
    expect("[%s] REFUSED: the first installation that also changes a file that is not the guard's" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "docs/a.md"); sh(d, "git", "checkout", "-q", "--", "docs/a.md")
    r = sh(d, "git", "commit", "-q", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
    expect("[%s] ACCEPTED: the arming commit once it carries only the guard's files and the configuration" % state, r.returncode == 0)
    # mixed commits
    open(os.path.join(d, "register.ttl"), "a").write("# r\n"); open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A")
    r = sh(d, "git", "commit", "-q", "-m", "register and work with no item")
    expect("[%s] REFUSED: a commit of the register together with governed work and no Work-Item, naming the acts" % state, r.returncode != 0 and "PERMITTED in this state" in r.stdout + r.stderr)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    open(os.path.join(d, "register.ttl"), "a").write("# r\n"); open(os.path.join(d, "tools", "note.txt"), "w").write("x\n"); sh(d, "git", "add", "-A")
    r = sh(d, "git", "commit", "-q", "-m", "register and guard file", "-m", "Guard-Install: mixed")
    expect("[%s] REFUSED: a commit of the register together with a guard file" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    open(os.path.join(d, "tools", "note.txt"), "w").write("x\n"); open(os.path.join(d, "docs", "a.md"), "a").write("x\n"); sh(d, "git", "add", "-A")
    r = sh(d, "git", "commit", "-q", "-m", "guard file and docs", "-m", "Guard-Install: mixed")
    expect("[%s] REFUSED: a Guard-Install commit that also changes a file that is not the guard's" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    # work with an item: judged by the item's own lineage (ready only in installed [the configured lineage is absent], ready and inbox)
    open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "app/main.py")
    r = sh(d, "git", "commit", "-q", "-m", "work on a groomed item", "-m", "Work-Item: S_Groomed")
    want = state in ("installed", "ready", "inbox")
    expect("[%s] work naming S_Groomed is %s" % (state, "ACCEPTED" if want else "REFUSED, naming the acts"), (r.returncode == 0) if want else (r.returncode != 0 and "PERMITTED in this state (%s)" % state in r.stdout + r.stderr))
    sh(d, "git", "reset", "-q", "--hard", "HEAD~1") if want else sh(d, "git", "reset", "-q", "--hard", "HEAD")
    open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "app/main.py")
    r = sh(d, "git", "commit", "-q", "-m", "work on a proposed item", "-m", "Work-Item: S_Proposed")
    expect("[%s] REFUSED: work naming an item that is not ready, and the refusal names the acts" % state, r.returncode != 0 and "PERMITTED in this state (%s)" % state in r.stdout + r.stderr)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    # a configuration change after arming
    cfgp = os.path.join(d, ".backlog-guard.json"); cfg = json.load(open(cfgp)); cfg["exempt_paths"] = ["app/**"]; json.dump(cfg, open(cfgp, "w")); sh(d, "git", "add", ".backlog-guard.json")
    r = sh(d, "git", "commit", "-q", "-m", "loosen", "-m", "Guard-Install: sneaked")
    expect("[%s] REFUSED: a configuration change after arming, with Guard-Install" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    # review 2 D1/D8: the commit that changes the configuration cannot make the configuration or app work the register, nor retarget the register
    gt = os.path.join(d, "tools", os.path.basename(guard_src))
    cfg = json.load(open(cfgp)); cfg["register"] = ["register.ttl", ".backlog-guard.json"]; cfg["exempt_paths"] = ["app/**"]; json.dump(cfg, open(cfgp, "w")); sh(d, "git", "add", ".backlog-guard.json")
    r = sh(d, "git", "commit", "-q", "-m", "make the configuration the register")
    expect("[%s] REFUSED: a commit that names the configuration as the register and loosens the guard (no Work-Item)" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    cfg = json.load(open(cfgp)); cfg["register"] = ["register.ttl", "app/main.py"]; json.dump(cfg, open(cfgp, "w")); open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A")
    r = sh(d, "git", "commit", "-q", "-m", "make app work the register")
    expect("[%s] REFUSED: a commit that names app work as the register and changes it (no Work-Item)" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    cfg = json.load(open(cfgp)); cfg["register"] = ["docs/a.md"]; json.dump(cfg, open(cfgp, "w")); sh(d, "git", "add", ".backlog-guard.json")
    r = sh(d, "git", "commit", "-q", "-m", "retarget the register", "-m", "Guard-Install: retarget")
    expect("[%s] REFUSED: retargeting the register key with Guard-Install" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    # review 5: deletions, the CI workflow and the session settings are protected, the edit hook on the guard's own files, a mid-sentence trailer
    sh(d, "git", "rm", "-q", "app/main.py")
    r = sh(d, "git", "commit", "-q", "-m", "delete governed work with no item")
    expect("[%s] REFUSED: a commit that deletes governed work with no Work-Item" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    gfile = os.path.join("tools", os.path.basename(guard_src))
    sh(d, "git", "rm", "-q", gfile)
    r = sh(d, "git", "commit", "-q", "-m", "delete the vendored guard")
    expect("[%s] REFUSED: a commit that deletes the vendored guard with no Guard-Install" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    for pth in (".github/workflows/backlog-work-guard.yml", ".claude/settings.json"):
        open(os.path.join(d, pth), "a").write("\n")
        sh(d, "git", "add", pth)
        r = sh(d, "git", "commit", "-q", "-m", "edit " + pth)
        expect("[%s] REFUSED: an edit of %s with no Work-Item and no Guard-Install" % (state, pth), r.returncode != 0)
        sh(d, "git", "reset", "-q", "--hard", "HEAD")
    sh(d, "git", "clean", "-fdq")
    open(os.path.join(d, "tools", "note.txt"), "w").write("y\n"); sh(d, "git", "add", "tools/note.txt")
    r = sh(d, "git", "commit", "-q", "-m", "we mention Guard-Install: sneaked in a sentence")
    expect("[%s] REFUSED: a Guard-Install that is not at the start of a line is not a trailer" % state, r.returncode != 0)
    r2 = sh(d, "git", "commit", "-q", "-m", "guard note", "-m", "Guard-Install: a note")
    expect("[%s] ACCEPTED: the same guard file with Guard-Install at the start of a line" % state, r2.returncode == 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD~1")
    if state not in ("installed", "ready", "inbox"):
        r = sh(d, sys.executable, gt, "edit", gfile)
        expect("[%s] the edit hook lets a guard file be edited while not ready, pointing to Guard-Install" % state, r.returncode == 0 and "guard's own files" in r.stdout + r.stderr and "BLOCKS" not in r.stdout + r.stderr)
    # review 6: a rename into governed work, a Work-Item mentioned mid-line, a register-only commit with a stray Work-Item
    sh(d, "git", "mv", "docs/a.md", "app/b.py")
    r = sh(d, "git", "commit", "-q", "-m", "rename an ungoverned file into governed work")
    expect("[%s] REFUSED: a commit that renames an ungoverned file into governed work with no Work-Item" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "app/main.py")
    r = sh(d, "git", "commit", "-q", "-m", "we are not naming it, see Work-Item: S_Groomed")
    expect("[%s] REFUSED: a Work-Item that is not at the start of a line is not a trailer" % state, r.returncode != 0)
    sh(d, "git", "commit", "-q", "--no-verify", "-m", "we are not naming it, see Work-Item: S_Groomed")
    r = sh(d, sys.executable, gt, "range", base + "..HEAD")
    expect("[%s] the range check refuses a Work-Item mentioned mid-line" % state, r.returncode == 2 and "names no Work-Item" in r.stdout)
    # review 13 D1: names that merely contain pyc or cache are governed work; only interpreter bytecode is not
    mid = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
    for nm in ("app/pycfg.py", "app/mypyc_data.txt", "app/pyc/x.py", "app/gen_x.py"):
        os.makedirs(os.path.dirname(os.path.join(d, nm)), exist_ok=True); open(os.path.join(d, nm), "w").write("x\n"); sh(d, "git", "add", nm)
        r = sh(d, "git", "commit", "-q", "-m", "a governed file whose name holds pyc, no item")
        expect("[%s] REFUSED at the commit hook: %s with no Work-Item" % (state, nm), r.returncode != 0)
        sh(d, "git", "commit", "-q", "--no-verify", "-m", "a governed file whose name holds pyc, no item")
        r = sh(d, sys.executable, gt, "range", mid + "..HEAD")
        expect("[%s] REFUSED by the range check: %s with no Work-Item" % (state, nm), r.returncode == 2 and nm in r.stdout)
        sh(d, "git", "reset", "-q", "--hard", mid)
    os.makedirs(os.path.join(d, "app", "__pycache__"), exist_ok=True); open(os.path.join(d, "app", "__pycache__", "x.pyc"), "w").write("b\n"); sh(d, "git", "add", "-f", "app/__pycache__/x.pyc")
    r = sh(d, "git", "commit", "-q", "-m", "interpreter bytecode is not work")
    expect("[%s] ACCEPTED: app/__pycache__/x.pyc is bytecode, not governed work" % state, r.returncode == 0)
    sh(d, "git", "reset", "-q", "--hard", mid)
    if state not in ("installed", "ready", "inbox"):
        open(os.path.join(d, "app", "gen_x.py"), "w").write("x\n")
        r = sh(d, sys.executable, gt, "edit", "app/gen_x.py")
        expect("[%s] the edit hook blocks app/gen_x.py while the lineage is not ready" % state, "BLOCKS" in r.stdout + r.stderr)
        os.remove(os.path.join(d, "app", "gen_x.py"))
    sh(d, "git", "reset", "-q", "--hard", "HEAD~1")
    open(os.path.join(d, "register.ttl"), "a").write("# r\n"); sh(d, "git", "add", "register.ttl")
    r = sh(d, "git", "commit", "-q", "-m", "record the chain", "-m", "Work-Item: S_Proposed")
    expect("[%s] ACCEPTED: a register-only commit is a record commit even with a stray Work-Item trailer" % state, r.returncode == 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD~1" if r.returncode == 0 else "HEAD")
    # review 9: nested and oddly named governed files, deletions seen by the range check
    os.makedirs(os.path.join(d, "app", "sub", "deep"), exist_ok=True)
    for nm in ("app/sub/deep/x.py", "app/my_cache.py"):
        open(os.path.join(d, nm), "w").write("x\n"); sh(d, "git", "add", nm)
        r = sh(d, "git", "commit", "-q", "-m", "work on " + nm)
        expect("[%s] REFUSED: %s is governed work and the commit names no Work-Item" % (state, nm), r.returncode != 0)
        sh(d, "git", "reset", "-q", "--hard", "HEAD"); sh(d, "git", "clean", "-fdq")
    open(os.path.join(d, "app", "keep.py"), "w").write("x\n"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "keep a governed file", "-m", "Guard-Install: x")
    kept = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
    sh(d, "git", "rm", "-q", "app/main.py"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "delete governed work")
    r = sh(d, sys.executable, gt, "range", kept + "..HEAD")
    expect("[%s] the range check refuses a commit that only deletes governed work and names no Work-Item" % state, r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
    sh(d, "git", "reset", "-q", "--hard", "HEAD~2")
    # D3: a file that looks like a register but is not
    open(os.path.join(d, "app", "data.ttl"), "w").write("# d\n"); sh(d, "git", "add", "-A")
    r = sh(d, "git", "commit", "-q", "-m", "a turtle file that is app work")
    expect("[%s] REFUSED: an app *.ttl that is not the register, with no Work-Item" % state, r.returncode != 0)
    sh(d, "git", "reset", "-q", "--hard", "HEAD")
    # D4: the edit-time hook and the status, in this state
    r = sh(d, sys.executable, gt, "edit", "register.ttl")
    expect("[%s] the edit hook lets the register be edited in this state" % state, r.returncode == 0 and "BLOCKS" not in r.stdout + r.stderr)
    if state not in ("installed", "ready", "inbox"):
        r = sh(d, sys.executable, gt, "edit", "app/main.py")
        expect("[%s] the edit hook refuses app work while the lineage is not ready and names the permitted acts" % state, "BLOCKS" in r.stdout + r.stderr and "PERMITTED in this state (%s)" % state in r.stdout + r.stderr)
    if state not in ("installed", "ready", "inbox"):
        open(os.path.join(d, "app", "data.ttl"), "w").write("# d\n")
        r = sh(d, sys.executable, gt, "edit", "app/data.ttl")
        expect("[%s] the edit hook refuses an app *.ttl while the lineage is not ready" % state, "BLOCKS" in r.stdout + r.stderr)
        os.remove(os.path.join(d, "app", "data.ttl"))
    r = sh(d, sys.executable, gt, "status")
    expect("[%s] the status names the permitted acts of the state" % state, "PERMITTED in this state (%s)" % state in r.stdout)
    # D2: the range layer over a Guard-Install commit that changes app work, and over a mixed register and work commit
    open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "app work claiming install", "-m", "Guard-Install: sneaked")
    r = sh(d, sys.executable, gt, "range", base + "..HEAD")
    expect("[%s] the range check refuses a Guard-Install commit that changes governed app work" % state, r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
    sh(d, "git", "reset", "-q", "--hard", "HEAD~1")
    open(os.path.join(d, "register.ttl"), "a").write("# r\n"); open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "register and app work")
    r = sh(d, sys.executable, gt, "range", base + "..HEAD")
    expect("[%s] the range check refuses a mixed register and app work commit with no item" % state, r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
    sh(d, "git", "reset", "-q", "--hard", "HEAD~1")
    # the range layer over the arming, a record commit and a guard commit, then over a work commit with no item
    open(os.path.join(d, "register.ttl"), "a").write("# r\n"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "-m", "record the chain")
    open(os.path.join(d, "tools", "note.txt"), "w").write("x\n"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "-m", "guard files", "-m", "Guard-Install: a note")
    g = os.path.join(d, "tools", os.path.basename(guard_src))
    r = sh(d, sys.executable, g, "range", base + "..HEAD")
    expect("[%s] the range check passes the arming, a record commit and a guard commit and lists each" % state, r.returncode == 0 and "VERDICT: PASS" in r.stdout and "record commit" in r.stdout and "guard-install commit" in r.stdout and r.stdout.count("NOTE") >= 3)
    open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "work with no item")
    r = sh(d, sys.executable, g, "range", base + "..HEAD")
    expect("[%s] the range check refuses a work commit with no item and names the permitted acts" % state, r.returncode == 2 and "PERMITTED in this state (%s)" % state in r.stdout and r.stdout.rstrip().splitlines()[-1].startswith("VERDICT: FAIL"))
    shutil.rmtree(d, ignore_errors=True)
    # a work path that matches nothing: a warning before the lineage is ready, an error after
    d, base, ir = armed_clone(state, extra_work=("nowhere/**",))
    expect("[%s] the installer warns of a work path that matches no tracked file" % state, "warning" in ir.stdout and "nowhere/**" in ir.stdout)
    sh(d, "git", *ARM); r = sh(d, "git", "commit", "-q", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
    o = r.stdout + r.stderr
    if state in ("ready", "inbox"):
        expect("[%s] REFUSED: the arming of a ready lineage whose work path matches nothing, naming the acts" % state, r.returncode != 0 and "GUARD BLOCKS" in o and "PERMITTED in this state (%s)" % state in o)
    else:
        expect("[%s] ACCEPTED with a warning: the arming whose work path matches nothing while the lineage is not ready" % state, r.returncode == 0 and "warning" in o and "matches no tracked file" in o)
    shutil.rmtree(d, ignore_errors=True)

# review 2 D5: a box open in ANOTHER lineage does not make this lineage's state "inbox"
rp, _ = state_register("ready")
og = Graph(); og.parse(rp, format="turtle")
nsx = [str(x)[:-len("Lin_Ready")] for x in og.subjects(RDF.type, URIRef(BL + "Lineage")) if str(x).endswith("Lin_Ready")][0]
og.add((URIRef(nsx + "It_Other"), RDF.type, URIRef(BL + "Iteration"))); og.add((URIRef(nsx + "It_Other"), URIRef(BL + "belongsToLineage"), URIRef(nsx + "Lin_Other"))); og.add((URIRef(nsx + "It_Other"), URIRef(BL + "hasState"), URIRef(BL + "InProgress")))
op = os.path.join(regs_dir, "other.ttl"); og.serialize(op, format="turtle")
d, base, ir = armed_clone("ready", reg=op)
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, os.path.join(d, "tools", os.path.basename(guard_src)), "status")
expect("a box open in another lineage leaves this lineage's state ready, not inbox", "PERMITTED in this state (ready)" in r.stdout and "(inbox)" not in r.stdout)
shutil.rmtree(d, ignore_errors=True)

# review 3: configuration narrowing, range over an unmatched work path, configuration change inside a range, status warning, installer single star
expect("narrowing a register path to its pattern alone is a narrowing", WG.narrowing_only({"register": ["r_v1_0_0.ttl"], "exempt_paths": []}, {"register": ["r_v*.ttl"], "exempt_paths": []}))
expect("narrowing a register path and changing another key is not a narrowing", not WG.narrowing_only({"register": ["r_v1_0_0.ttl"], "exempt_paths": []}, {"register": ["r_v*.ttl"], "exempt_paths": ["app/**"]}))
d, base, ir = armed_clone("ready", extra_work=("nowhere/**",))
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, os.path.join(d, "tools", os.path.basename(guard_src)), "range", base + "..HEAD")
expect("the range check over a ready lineage with a work path matching nothing fails", r.returncode == 2 and "matches no tracked file" in r.stdout and "PERMITTED in this state (ready)" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
arm_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
cfgp = os.path.join(d, ".backlog-guard.json"); cfg = json.load(open(cfgp)); cfg["register"] = ["register.ttl", "app/main.py"]; json.dump(cfg, open(cfgp, "w"))
sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "config names app work as register", "-m", "Work-Item: S_Groomed")
open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "app work claiming to be the register")
r = sh(d, sys.executable, os.path.join(d, "tools", os.path.basename(guard_src)), "range", arm_commit + "..HEAD")
expect("the range check judges a later commit by the configuration in force before the range, not by a change inside it", r.returncode == 2 and "names no Work-Item" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
d, base, ir = armed_clone("mission", extra_work=("nowhere/**",))
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, os.path.join(d, "tools", os.path.basename(guard_src)), "status")
expect("the status warns of a work path matching nothing while the lineage is not ready", "(warning)" in r.stdout and "matches no tracked file" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
d, base, ir = armed_clone("ready", extra_work=("*.py",))
expect("the installer warns of a single-star work path that matches no file in the directory it names", "warning" in ir.stdout and "*.py" in ir.stdout)
shutil.rmtree(d, ignore_errors=True)

# review 4: the backlog state with every stage built, a finished iteration, an untracked work path, fail-closed configurations, installer re-run, empty reason
GP = lambda d: os.path.join(d, "tools", os.path.basename(guard_src))
rp, _ = state_register("ready")
bg = Graph(); bg.parse(rp, format="turtle")
from rdflib import Literal
bg.add((URIRef(nsx + "Lin_Ready"), URIRef(BL + "lineageFrozen"), Literal(True)))
bp = os.path.join(regs_dir, "backlogfull.ttl"); bg.serialize(bp, format="turtle")
d, base, ir = armed_clone("ready", reg=bp)
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, GP(d), "status")
expect("every stage built with a readiness fact missing (frozen by an unanswered finding) is the state backlog", "PERMITTED in this state (backlog)" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
dg = Graph(); dg.parse(rp, format="turtle")
dg.add((URIRef(nsx + "It_Done"), RDF.type, URIRef(BL + "Iteration"))); dg.add((URIRef(nsx + "It_Done"), URIRef(BL + "belongsToLineage"), URIRef(nsx + "Lin_Ready"))); dg.add((URIRef(nsx + "It_Done"), URIRef(BL + "hasState"), URIRef(BL + "Done")))
dp = os.path.join(regs_dir, "done.ttl"); dg.serialize(dp, format="turtle")
d, base, ir = armed_clone("ready", reg=dp)
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, GP(d), "status")
expect("an iteration of the lineage that is done leaves the state ready", "PERMITTED in this state (ready)" in r.stdout and "(inbox)" not in r.stdout)
shutil.rmtree(d, ignore_errors=True)
d, base, ir = armed_clone("ready", extra_work=("extra/**",), untracked=("extra/x.py",))
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, GP(d), "status")
expect("a work path matched only by an untracked file matches no tracked file", "matches no tracked file" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# fail-closed configurations
for what in ("work_paths", "register", "emptyreg", "lineage"):
    d, base, ir = armed_clone("ready")
    sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
    cfgp = os.path.join(d, ".backlog-guard.json"); cfg = json.load(open(cfgp))
    if what == "work_paths": cfg["work_paths"] = []; json.dump(cfg, open(cfgp, "w"))
    elif what == "register": cfg["register"] = []; json.dump(cfg, open(cfgp, "w"))
    elif what == "lineage": del cfg["active_lineage"]; json.dump(cfg, open(cfgp, "w"))
    else:
        open(os.path.join(d, "register.ttl"), "w").write(""); sh(d, "git", "add", "register.ttl"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "empty the register")
    open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "app/main.py")
    r = sh(d, "git", "commit", "-q", "-m", "work on a groomed item", "-m", "Work-Item: S_Groomed")
    expect("REFUSED, closed: " + {"work_paths": "an empty work_paths list", "register": "no register configured", "emptyreg": "an empty register", "lineage": "no active_lineage"}[what], r.returncode != 0 and "PERMITTED in this state" in r.stdout + r.stderr)
    shutil.rmtree(d, ignore_errors=True)
# installer re-run keeps governed_from and exempt_paths
d, base, ir = armed_clone("ready")
cfgp = os.path.join(d, ".backlog-guard.json"); first = json.load(open(cfgp)); first["exempt_paths"] = ["docs/**"]; json.dump(first, open(cfgp, "w"))
sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "move on")
instp = sorted(glob.glob(os.path.join(HERE, "backlog_guard_install_v*.py")), key=sv)[-1]
subprocess.run([sys.executable, instp, d, "--tooling-dir", "tools", "--register", "register.ttl", "--lineage", "Lin_Ready", "--work-path", "app/**", "--work-path", "register.ttl"], capture_output=True, text=True)
again = json.load(open(cfgp))
expect("an installer re-run keeps governed_from and exempt_paths", again.get("governed_from") == first.get("governed_from") and again.get("exempt_paths") == ["docs/**"])
shutil.rmtree(d, ignore_errors=True)
# a Guard-Install trailer with no reason is not a trailer
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); r = sh(d, "git", "commit", "-q", "-m", "Install the work guard", "-m", "Guard-Install:")
expect("REFUSED: the arming whose Guard-Install trailer states no reason", r.returncode != 0)
shutil.rmtree(d, ignore_errors=True)

# review 5: withdrawn output, planned iteration, installer glob agreement and untracked files, narrowing needs the trailer
wg = Graph(); wg.parse(rp, format="turtle")
for o_ in list(wg.subjects(URIRef(BL + "outputOfStage"), URIRef(BL + "Stage_Mission"))):
    if (o_, URIRef(BL + "belongsToLineage"), URIRef(nsx + "Lin_Ready")) in wg: wg.add((o_, URIRef(BL + "outputRetracted"), Literal(True)))
wp = os.path.join(regs_dir, "withdrawn.ttl"); wg.serialize(wp, format="turtle")
d, base, ir = armed_clone("ready", reg=wp)
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, GP(d), "status")
expect("a withdrawn stage output does not count: the lineage is back at the mission", "PERMITTED in this state (mission)" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
pg = Graph(); pg.parse(rp, format="turtle")
pg.add((URIRef(nsx + "It_Plan"), RDF.type, URIRef(BL + "Iteration"))); pg.add((URIRef(nsx + "It_Plan"), URIRef(BL + "belongsToLineage"), URIRef(nsx + "Lin_Ready"))); pg.add((URIRef(nsx + "It_Plan"), URIRef(BL + "hasState"), URIRef(BL + "Proposed")))
pp = os.path.join(regs_dir, "planned.ttl"); pg.serialize(pp, format="turtle")
d, base, ir = armed_clone("ready", reg=pp)
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, GP(d), "status")
expect("an iteration that is only planned leaves the state ready", "PERMITTED in this state (ready)" in r.stdout and "(inbox)" not in r.stdout)
shutil.rmtree(d, ignore_errors=True)
d, base, ir = armed_clone("ready", extra_work=("app/ma?n.py", "**/register.ttl"))
expect("the installer reads a ? and a leading **/ as the guard does and warns of neither", "warning" not in ir.stdout)
shutil.rmtree(d, ignore_errors=True)
d, base, ir = armed_clone("ready", extra_work=("extra/**",), untracked=("extra/x.py",))
expect("the installer counts only tracked files: a path matched only by an untracked file draws the warning", "warning" in ir.stdout and "extra/**" in ir.stdout)
shutil.rmtree(d, ignore_errors=True)
for trailer, want in (("Guard-Install: narrowing", True), (None, False)):
    d, base, ir = armed_clone("ready", regname="register_v1_0_0.ttl")
    sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
    cfgp = os.path.join(d, ".backlog-guard.json"); cfg = json.load(open(cfgp)); cfg["register"] = ["register_v*.ttl"]; json.dump(cfg, open(cfgp, "w")); sh(d, "git", "add", ".backlog-guard.json")
    args = ["git", "commit", "-q", "-m", "narrow the register path"] + (["-m", trailer] if trailer else [])
    r = sh(d, *args)
    expect("a narrowing of the register path to its pattern is %s" % ("ACCEPTED with Guard-Install" if want else "REFUSED without Guard-Install"), (r.returncode == 0) == want)
    if not want:
        sh(d, "git", "commit", "-q", "--no-verify", "-m", "narrow the register path")
        r = sh(d, sys.executable, GP(d), "range", base + "..HEAD")
        expect("the range check refuses a narrowing with no Guard-Install", r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
    shutil.rmtree(d, ignore_errors=True)

# review 6: a file elsewhere that carries the register's versioned name is not the register
d, base, ir = armed_clone("ready", regname="register_v1_0_0.ttl")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
open(os.path.join(d, "app", "register_v1_9_0.ttl"), "w").write("# not the register\n"); sh(d, "git", "add", "-A")
r = sh(d, "git", "commit", "-q", "-m", "app work named like the register")
expect("REFUSED: a file in another directory with the register's versioned name, no Work-Item", r.returncode != 0)
sh(d, "git", "commit", "-q", "--no-verify", "-m", "app work named like the register")
r = sh(d, sys.executable, GP(d), "range", base + "..HEAD")
expect("the range check refuses it too", r.returncode == 2 and "names no Work-Item" in r.stdout)
open(os.path.join(d, "register_v1_1_0.ttl"), "w").write("# next version\n"); sh(d, "git", "rm", "-q", "register_v1_0_0.ttl"); sh(d, "git", "add", "-A")
r = sh(d, "git", "commit", "-q", "-m", "the register renamed to its next version")
expect("ACCEPTED: the register renamed to its next version in the same directory", r.returncode == 0)
shutil.rmtree(d, ignore_errors=True)

# review 8: a register changed by the same commit that relies on it is judged by the range check on the register of the commit's parent
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
arm_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
rg = Graph(); rg.parse(os.path.join(d, "register.ttl"), format="turtle")
sp = URIRef(nsx + "S_Proposed")
rg.remove((sp, URIRef(BL + "hasState"), URIRef(BL + "Proposed"))); rg.add((sp, URIRef(BL + "hasState"), URIRef(BL + "Ready")))
rg.serialize(os.path.join(d, "register.ttl"), format="turtle")
open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A")
sh(d, "git", "commit", "-q", "--no-verify", "-m", "ready the item and work on it in one commit", "-m", "Work-Item: S_Proposed")
r = sh(d, sys.executable, GP(d), "range", arm_commit + "..HEAD")
expect("the range check judges a Work-Item by the register of the commit's parent: readying the item and using it in one commit is refused", r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 10 D1: the range layer over a commit that changes a guard file AND governed app work with Guard-Install and no item
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
arm_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
open(GP(d), "a").write("# note\n"); open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A")
sh(d, "git", "commit", "-q", "--no-verify", "-m", "a guard file and app work claiming install", "-m", "Guard-Install: sneaked")
r = sh(d, sys.executable, GP(d), "range", arm_commit + "..HEAD")
expect("the range check refuses a Guard-Install commit that changes a guard file together with governed app work", r.returncode == 2 and "VERDICT: FAIL" in r.stdout and "guard-install commit" not in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 10 D2: one item named by two commits, a register edit between them making it not ready: the second is judged on its own parent's register
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
rg = Graph(); rg.parse(os.path.join(d, "register.ttl"), format="turtle")
sp = URIRef(nsx + "S_Proposed")
rg.remove((sp, URIRef(BL + "hasState"), URIRef(BL + "Proposed"))); rg.add((sp, URIRef(BL + "hasState"), URIRef(BL + "Ready")))
rg.serialize(os.path.join(d, "register.ttl"), format="turtle"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "ready the item")
ready_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A")
sh(d, "git", "commit", "-q", "--no-verify", "-m", "work on the ready item", "-m", "Work-Item: S_Proposed")
r = sh(d, sys.executable, GP(d), "range", ready_commit + "..HEAD")
expect("the range check accepts the work on an item that is ready at its parent", r.returncode == 0 and "VERDICT: PASS" in r.stdout)
rg = Graph(); rg.parse(os.path.join(d, "register.ttl"), format="turtle")
rg.remove((sp, URIRef(BL + "hasState"), URIRef(BL + "Ready"))); rg.add((sp, URIRef(BL + "hasState"), URIRef(BL + "Proposed")))
rg.serialize(os.path.join(d, "register.ttl"), format="turtle"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "--no-verify", "-m", "the item is no longer ready")
open(os.path.join(d, "app", "main.py"), "a").write("y\n"); sh(d, "git", "add", "-A")
sh(d, "git", "commit", "-q", "--no-verify", "-m", "work on the item again", "-m", "Work-Item: S_Proposed")
r = sh(d, sys.executable, GP(d), "range", ready_commit + "..HEAD")
expect("the range check refuses the second commit naming an item that is no longer ready at its own parent (the first verdict is not reused)", r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 11 D2: the range layer over a Guard-Install commit that changes the configuration and governed app work
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
arm_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
cfgp = os.path.join(d, ".backlog-guard.json"); cfg = json.load(open(cfgp)); cfg["exempt_paths"] = ["app/**"]; json.dump(cfg, open(cfgp, "w"))
open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A")
sh(d, "git", "commit", "-q", "--no-verify", "-m", "loosen the configuration and edit app work", "-m", "Guard-Install: sneaked")
r = sh(d, sys.executable, GP(d), "range", arm_commit + "..HEAD")
expect("the range check refuses a Guard-Install commit that changes the configuration together with governed app work", r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 11 D3: a register retargeted to a pattern of another stem, or with an extra entry, is not a narrowing
for what, newreg, wantword in (("a register path retargeted to a pattern of another stem", ["app/x_v*.py"], None), ("an extra register entry appended", ["register_v1_0_0.ttl", "extra_v1_0_0.ttl"], None), ("an exact path replaced by a pattern of another stem beside the old pattern", ["register_v*.ttl", "app/y_v*.py"], None)):
    d, base, ir = armed_clone("ready", regname="register_v1_0_0.ttl")
    sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
    arm_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
    cfgp = os.path.join(d, ".backlog-guard.json"); cfg = json.load(open(cfgp)); cfg["register"] = newreg; json.dump(cfg, open(cfgp, "w")); sh(d, "git", "add", ".backlog-guard.json")
    r = sh(d, "git", "commit", "-q", "-m", "change the register entry", "-m", "Guard-Install: narrowing")
    expect("REFUSED at the commit hook: %s" % what, r.returncode != 0)
    sh(d, "git", "commit", "-q", "--no-verify", "-m", "change the register entry", "-m", "Guard-Install: narrowing")
    r = sh(d, sys.executable, GP(d), "range", arm_commit + "..HEAD")
    expect("REFUSED by the range check: %s" % what, r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
    shutil.rmtree(d, ignore_errors=True)
# review 11 D4: a governed file whose name has a non-ASCII letter is governed work
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
arm_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
open(os.path.join(d, "app", "\u00e9.py"), "w").write("x\n"); sh(d, "git", "add", "-A")
r = sh(d, "git", "commit", "-q", "-m", "a non-ASCII governed file, no item")
expect("REFUSED at the commit hook: app/\u00e9.py with no Work-Item", r.returncode != 0)
sh(d, "git", "commit", "-q", "--no-verify", "-m", "a non-ASCII governed file, no item")
r = sh(d, sys.executable, GP(d), "range", arm_commit + "..HEAD")
expect("REFUSED by the range check: app/\u00e9.py with no Work-Item", r.returncode == 2 and "names no Work-Item" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 12 D2: a nested file of the tooling directory is guard work
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
os.makedirs(os.path.join(d, "tools", "sub"), exist_ok=True); open(os.path.join(d, "tools", "sub", "x.py"), "w").write("x = 1\n"); sh(d, "git", "add", "-A")
r = sh(d, "git", "commit", "-q", "-m", "a nested vendored tool, no item")
expect("REFUSED at the commit hook: tools/sub/x.py is a guard file and the commit names no item", r.returncode != 0)
shutil.rmtree(d, ignore_errors=True)
# review 12 D3: the register, app work and a Guard-Install trailer in one commit is not a record commit
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
arm_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
open(os.path.join(d, "register.ttl"), "a").write("# r\n"); open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A")
sh(d, "git", "commit", "-q", "--no-verify", "-m", "register and app work claiming install", "-m", "Guard-Install: sneaked")
r = sh(d, sys.executable, GP(d), "range", arm_commit + "..HEAD")
expect("the range check refuses the register plus app work plus a Guard-Install trailer", r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 12 D5: a Guard-Install line with no reason is not a trailer, even when another paragraph follows
d, base, ir = armed_clone("ready")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
arm_commit = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
for msg in (["-m", "x", "-m", "Guard-Install:", "-m", "Signed-off-by: x"], ["-m", "x", "-m", "Guard-Install:\nSigned-off-by: x"]):
    open(os.path.join(d, "tools", "note.txt"), "a").write("n\n"); sh(d, "git", "add", "-A")
    r = sh(d, "git", "commit", "-q", *msg)
    expect("REFUSED at the commit hook: a Guard-Install line with no reason followed by another line, on a guard file", r.returncode != 0)
    sh(d, "git", "commit", "-q", "--no-verify", *msg)
r = sh(d, sys.executable, GP(d), "range", arm_commit + "..HEAD")
expect("REFUSED by the range check: a Guard-Install line with no reason followed by another line", r.returncode == 2 and "VERDICT: FAIL" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 12 F-h: a register pattern at the repository root is read at a revision
d, base, ir = armed_clone("ready", regname="register_v1_0_0.ttl")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
cfgp = os.path.join(d, ".backlog-guard.json"); cfg = json.load(open(cfgp)); cfg["register"] = ["register_v*.ttl"]; json.dump(cfg, open(cfgp, "w")); sh(d, "git", "add", ".backlog-guard.json")
sh(d, "git", "commit", "-q", "-m", "narrow the register path", "-m", "Guard-Install: narrowing")
narrow = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
open(os.path.join(d, "register_v1_0_0.ttl"), "a").write("# r\n"); sh(d, "git", "add", "-A")
r = sh(d, "git", "commit", "-q", "-m", "record the chain")
expect("ACCEPTED at the commit hook: a record commit with the register pattern at the repository root", r.returncode == 0)
r = sh(d, sys.executable, GP(d), "range", narrow + "..HEAD")
expect("ACCEPTED by the range check: a record commit with the register pattern at the repository root", r.returncode == 0 and "VERDICT: PASS" in r.stdout)
rg = Graph(); rg.parse(os.path.join(d, "register_v1_0_0.ttl"), format="turtle"); sp = URIRef(nsx + "S_Proposed")
rg.remove((sp, URIRef(BL + "hasState"), URIRef(BL + "Proposed"))); rg.add((sp, URIRef(BL + "hasState"), URIRef(BL + "Ready")))
rg.serialize(os.path.join(d, "register_v1_0_0.ttl"), format="turtle"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "-m", "ready the item")
open(os.path.join(d, "app", "main.py"), "a").write("x\n"); sh(d, "git", "add", "-A")
r = sh(d, "git", "commit", "-q", "-m", "work on the ready item", "-m", "Work-Item: S_Proposed")
expect("ACCEPTED at the commit hook: work on a ready item with the register pattern at the repository root", r.returncode == 0)
r = sh(d, sys.executable, GP(d), "range", narrow + "..HEAD")
expect("ACCEPTED by the range check: work on a ready item, the register read at its parent through a pattern at the repository root", r.returncode == 0 and "VERDICT: PASS" in r.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 14 D5: the installer reads tracked file names as the guard does, a non-ASCII name included
d, base, ir = armed_clone("ready")
os.makedirs(os.path.join(d, "zz")); open(os.path.join(d, "zz", "\u00e9.py"), "w").write("x\n"); sh(d, "git", "add", "-A"); sh(d, "git", "commit", "-q", "-m", "a non-ASCII file")
path_, lin_ = state_register("ready")
inst_ = sorted(glob.glob(os.path.join(HERE, "backlog_guard_install_v*.py")), key=sv)[-1]
ir = subprocess.run([sys.executable, inst_, d, "--tooling-dir", "tools", "--register", "register.ttl", "--lineage", lin_, "--work-path", "app/**", "--work-path", "register.ttl", "--work-path", "zz/**"], capture_output=True, text=True)
expect("the installer finds the tracked file zz/\u00e9.py for the work path zz/** and warns of nothing", ir.returncode == 0 and "warning" not in ir.stdout)
shutil.rmtree(d, ignore_errors=True)
# review 8 F3: a ? in a work path does not match a slash
d, base, ir = armed_clone("ready", extra_work=("app?main.py",))
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
r = sh(d, sys.executable, GP(d), "status")
expect("a ? in a work path does not match a slash: app?main.py matches no tracked file", "matches no tracked file" in r.stdout)
shutil.rmtree(d, ignore_errors=True)

# review 9: an unreadable register still gets the permitted acts from the status and the edit hook
d, base, ir = armed_clone("mission")
sh(d, "git", *ARM); sh(d, "git", "commit", "-q", "--no-verify", "-m", "Install the work guard", "-m", "Guard-Install: first installation")
open(os.path.join(d, "register.ttl"), "w").write("this is not turtle {{{\n")
r = sh(d, sys.executable, GP(d), "status")
expect("the status with an unreadable register says so and prints the permitted acts", r.returncode == 1 and "cannot read the register" in r.stdout and "PERMITTED in this state" in r.stdout)
r = sh(d, sys.executable, GP(d), "edit", "app/main.py")
expect("the edit hook with an unreadable register says so and prints the permitted acts", r.returncode == 2 and "cannot read the register" in r.stdout + r.stderr and "PERMITTED in this state" in r.stdout + r.stderr)
shutil.rmtree(d, ignore_errors=True)

# the acts of the tool are the acts of the register
rg = Graph(); rg.parse(sorted(glob.glob(os.path.join(HERE, "..", "01-ontologies", "backlog_abox_v*.ttl")), key=sv)[-1], format="turtle")
name_of = {"installed": "Installed", "mission": "Mission", "scope": "Scope", "goal": "Goal", "objective": "Objective", "backlog": "Backlog", "ready": "Ready", "inbox": "InBox"}
agree = True
for k, nm in name_of.items():
    gs = [s for s in rg.subjects(RDF.type, URIRef(BL + "GuardState")) if str(s).endswith("GS_IK_" + nm)]
    if len(gs) != 1: agree = False; continue
    got = {str(rg.value(a, URIRef(BL + "hasActStatement"))) for a in rg.objects(gs[0], URIRef(BL + "hasPermittedAct"))}
    if got != set(WG.STATE_ACTS[k]) | set(WG.COMMON_ACTS.values()): agree = False
expect("the permitted acts of every state in the guard are exactly the acts the register records for that state", agree)
shutil.rmtree(regs_dir, ignore_errors=True)

print("VERDICT   :", "PASS" if not bad else "FAIL"); [print("  ", b) for b in bad]
sys.exit(1 if bad else 0)
