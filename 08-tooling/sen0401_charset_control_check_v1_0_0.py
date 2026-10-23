#!/usr/bin/env python3
"""sen0401_charset_control_check v1.0.0 - the control's own checks of TK_Charset_Check (criterion AC6R_Check): the builder re-runs the proofs with its OWN fixtures, written fresh into a scratch folder. A NEW tool; it edits no committed file.
Usage: sen0401_charset_control_check_v1_0_0.py KIND
  nochange:SHAS   every file of the commits (comma list) has git status A
  stdlib          the tool imports only standard-library modules (ast) and opens no file for writing (ast: no open mode with w, a, x, + ; no write/unlink calls)
  shipped         the tool exits non-zero on the pages 9.82.0 of chapters 5 and 6 and on template 9.52.1, prints the start of the tag (13578 for the pages), and the files' SHA-256 are the same before and after
  passfx          exit 0 on fresh fixtures: tag at byte 0; tag at byte 1000 (ends within 1024); tag at byte 0 with a 3-byte UTF-8 character cut by byte 1024 in a longer file
  failfx          exit non-zero on fresh fixtures: tag at byte 1100; tag at byte 10 with an invalid byte 0xFF before byte 1024; no tag; a missing file
  mixed           given one passing and one failing file the exit code is non-zero; given two passing files it is zero
Exit 0 only when the check holds."""
__version__ = "1.0.0"
import ast, hashlib, os, subprocess, sys, tempfile
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); TOOL = os.path.join(H, "sen0401_page_charset_check_v1_0_0.py")
def sh(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, **k)
def say(ok, msg): print("%s %s" % ("PASS" if ok else "FAIL", msg)); sys.exit(0 if ok else 1)
def run(*files): r = subprocess.run([sys.executable, "-B", TOOL] + list(files), capture_output=True, text=True); return r.returncode, r.stdout + r.stderr
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
TAG = b'<meta charset="utf-8">'
def fx(d):
    f = {}
    def w(n, b): p = os.path.join(d, n); open(p, "wb").write(b); f[n] = p
    w("tag0.html", TAG + b"<title>t</title>" + b" " * 200)
    w("tag1000.html", b"<!-- " + b"x" * 973 + b" -->" + TAG[:0] + TAG + b"<p>rest</p>" * 20)   # tag starts at 982? padded below
    pad = b"<!--" + b"x" * (1000 - 4 - 3) + b"-->"; w("tag1000.html", pad + TAG + b"<p>rest</p>" * 20)   # tag starts at byte 1000
    head = TAG + b"y" * (1022 - len(TAG)) + "€".encode() + b"z" * 300   # euro sign (3 bytes) occupies bytes 1022..1024: cut by the window
    w("cut.html", head)
    w("tag1100.html", b"<!--" + b"x" * 1096 + b"-->" + TAG + b"<p>x</p>")
    w("invalid.html", b"<p>" + b"\xff" + b"</p>" + b" " * 3 + TAG[:0] + b" " * 0)
    w("invalid.html", b"      " + TAG + b" \xff " + b"a" * 1200)
    w("notag.html", b"<html><body>" + b"a" * 2000)
    return f
def main():
    k = sys.argv[1].split(":")
    if k[0] == "nochange":
        st = []
        for c in k[1].split(","): st += [(c, l) for l in sh("git", "show", "--name-status", "--format=", c, cwd=R).stdout.splitlines() if l.strip()]
        bad = [c + " " + l for c, l in st if not l.startswith("A\t")]; say(not bad, "commits %s: %d file(s) added, %d modified or removed %s" % (k[1], len(st) - len(bad), len(bad), bad[:5]))
    if k[0] == "stdlib":
        tree = ast.parse(open(TOOL, encoding="utf-8").read()); mods = sorted({(n.names[0].name if isinstance(n, ast.Import) else n.module).split(".")[0] for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))})
        std = set(sys.stdlib_module_names); nonstd = [m for m in mods if m not in std]; badw = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open":
                mode = n.args[1].value if len(n.args) > 1 and isinstance(n.args[1], ast.Constant) else next((kw.value.value for kw in n.keywords if kw.arg == "mode" and isinstance(kw.value, ast.Constant)), "r")
                if any(c in str(mode) for c in "wax+"): badw.append(mode)
            if isinstance(n, ast.Attribute) and n.attr in ("write", "write_text", "write_bytes", "unlink", "remove", "rename", "truncate"): badw.append(n.attr)
        say(not nonstd and not badw, "imports %s (non-standard: %s); write-capable calls or modes: %s" % (mods, nonstd, badw))
    if k[0] == "shipped":
        fs = [os.path.join(R, "03-materials", "ch05", "page", "sen0401_ch05_page_v9_82_0.html"), os.path.join(R, "03-materials", "ch06", "page", "sen0401_ch06_page_v9_82_0.html"), os.path.join(H, "course_page_template_v9_52_1.html")]
        before = [sha(f) for f in fs]; res = []; ok = True
        for f in fs:
            c, o = run(f); res.append((os.path.basename(f), c, "13578" in o)); ok &= c != 0
        ok &= all(r[2] for r in res[:2]) and before == [sha(f) for f in fs]
        say(ok, "exit codes and tag offset 13578 printed %s; SHA-256 of the three files unchanged: %s" % (res, before == [sha(f) for f in fs]))
    with tempfile.TemporaryDirectory(prefix="sen0401_cs_") as d:
        f = fx(d)
        if k[0] == "passfx":
            res = {n: run(f[n])[0] for n in ("tag0.html", "tag1000.html", "cut.html")}; say(all(v == 0 for v in res.values()), "exit codes on fresh fixtures (tag at 0, tag at 1000, character cut by byte 1024): %s" % res)
        if k[0] == "failfx":
            res = {n: run(f[n])[0] for n in ("tag1100.html", "invalid.html", "notag.html")}; res["missing"] = run(os.path.join(d, "nope.html"))[0]; say(all(v != 0 for v in res.values()), "exit codes on fresh failing fixtures (tag at 1100, invalid byte, no tag, missing file): %s" % res)
        if k[0] == "mixed":
            a = run(f["tag0.html"], f["tag1100.html"])[0]; b = run(f["tag0.html"], f["tag1000.html"])[0]; say(a != 0 and b == 0, "one passing + one failing file: exit %d (non-zero wanted); two passing files: exit %d (zero wanted)" % (a, b))
    raise SystemExit(__doc__)
main()
