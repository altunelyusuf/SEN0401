#!/usr/bin/env python3
"""sen0401_template_check2 v1.0.0 - the control's own checks of TK_Charset_Template (page template 9.52.2; criterion AC6R_Template). A NEW tool; it edits no committed file; the page tests are run by the builder, not taken from the executor's logs.
Usage: sen0401_template_check2_v1_0_0.py run | KIND
  run         builds the data and the page of chapter 5 on template 9.52.2 (PAGE_TEMPLATE) into a scratch folder with builders v4_15_0 and v2_24_0, then runs page test 9.36.0 (logs in 08-tooling/verify/iter19/template)
  ident       element (1): 9.52.0 and 9.52.1 and every older template are clean against HEAD; 9.52.0 and 9.52.1 have the recorded SHA-256 (executor's before/after file) and one commit each; 9.52.2 is committed once, as a new file
  offset      element (2): the page charset check v1_0_0 exits 0 on 9.52.2 and prints the tag offset; the tag occurs exactly once; offset below 1024; the first 1024 bytes decode as UTF-8
  diff        element (3): after removing from both files (a) every comment, (b) the tag, the rest must be identical but for whitespace (printed); every comment of 9.52.1 is in 9.52.2 and the only new comment is the 9.52.2 version marker; every id and data- hook of 9.52.1 is in 9.52.2. Any other difference (printed) fails.
  scratch     element (4): the scratch page of chapter 5 embeds 9.52.2, has the tag exactly once below byte 1024 (charset check exit 0) and page test 9.36.0 exits 0 with no [FAIL] line, all widgets passed
  nochange:SHAS   element (5): every file of the commits (comma list) has git status A
Exit 0 only when the check holds. Results are printed."""
__version__ = "1.0.0"
import hashlib, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); T = "/tmp/claude-0/s/tp19"; LOG = os.path.join(H, "verify", "iter19", "template"); VENV = "/home/claude/venv314/bin/python"; PV = "9_92_0"; NN = "05"; TPL = "course_page_template_v9_52_2.html"
P = lambda n: os.path.join(H, "course_page_template_v%s.html" % n); CHK = os.path.join(H, "sen0401_page_charset_check_v1_0_0.py"); TAG = b'<meta charset="utf-8">'
def sh(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, **k)
def say(ok, msg): print("%s %s" % ("PASS" if ok else "FAIL", msg)); sys.exit(0 if ok else 1)
def chk(p): r = subprocess.run([sys.executable, "-B", CHK, p], capture_output=True, text=True); return r.returncode, (r.stdout + r.stderr).strip()
def scratch():
    out = os.path.join(T, "out" + NN); os.makedirs(out, exist_ok=True); os.makedirs(LOG, exist_ok=True)
    env = dict(os.environ, PAGE_VER=PV, PAGE_DATA_OUT=out, PAGE_DATA_DIR=out, PAGE_SCRATCH=out, PAGE_TEMPLATE=TPL)
    for a in ([VENV, "sen0401_page_data_v2_24_0.py", NN, VENV], [VENV, "sen0401_page_build_v4_15_0.py", NN]):
        r = subprocess.run(a, capture_output=True, text=True, env=env, cwd=H, timeout=900); open(os.path.join(LOG, "build_%s_%s.log" % (NN, a[1][-14:-3])), "w").write(r.stdout + r.stderr)
        if r.returncode: print("build failed", a[1], r.stderr[-400:]); sys.exit(2)
    mk = os.path.join(T, "mkscratch.sh"); open(mk, "w").write(open("/tmp/claude-0/s17/mkscratch.sh").read().replace("S=/tmp/claude-0/s17/repo$NN", "S=%s/repo$NN" % T))
    r = subprocess.run(["sh", mk, NN, PV, out], capture_output=True, text=True); print(r.stdout.strip()[-200:], r.stderr[-200:]); return r.stdout.strip().splitlines()[-1]
def main():
    a = sys.argv[1]; k = a.split(":")
    if a == "run":
        sc = scratch(); full = os.path.join(LOG, "sc05_9_36_0.full.log"); runner = os.path.join(LOG, "sc05_9_36_0.runner.txt")
        r = subprocess.run([sys.executable, "-B", os.path.join(sc, "08-tooling", "sen0401_lineage_page_test_run_v1_2_0.py"), NN, PV], capture_output=True, text=True, env=dict(os.environ, PAGE_TEST="sen0401_page_test_v9_36_0.py", FULL_LOG=full), cwd=sc)
        open(runner, "w").write(r.stdout + r.stderr); print("page test 9.36.0: exit", r.returncode); return
    if k[0] == "ident":
        rec = dict(reversed(l.split()) for l in open(os.path.join(H, "template952_logs", "I19", "sha256_before_after.txt")) if re.match(r"^[0-9a-f]{64}\s", l))
        old = [p for p in sorted(os.listdir(H)) if re.match(r"course_page_template_v.*\.html$", p) and p != TPL]; dirty = [p for p in old if sh("git", "diff", "--quiet", "HEAD", "--", os.path.join(H, p), cwd=R).returncode or sh("git", "ls-files", "--error-unmatch", os.path.join(H, p), cwd=R).returncode]
        h = lambda n: hashlib.sha256(open(P(n), "rb").read()).hexdigest(); c = lambda n: sh("git", "log", "--format=%h", "--", P(n), cwd=R).stdout.split()
        st = sh("git", "log", "--format=%h", "--name-status", "--diff-filter=A", "--", P("9_52_2"), cwd=R).stdout
        ok = not dirty and h("9_52_0") == rec.get("course_page_template_v9_52_0.html") and h("9_52_1") == rec.get("course_page_template_v9_52_1.html") and len(c("9_52_0")) == 1 and len(c("9_52_1")) == 1 and len(c("9_52_2")) == 1 and "A\t" in st and h("9_52_2") == rec.get("course_page_template_v9_52_2.html")
        say(ok, "%d older templates, %d not clean against HEAD %s; 9.52.0 SHA-256 %s and 9.52.1 SHA-256 %s equal the recorded; commits of 9.52.0/9.52.1/9.52.2: %d/%d/%d; 9.52.2 SHA-256 %s equals the recorded and was added as a new file" % (len(old), len(dirty), dirty[:3], h("9_52_0")[:12], h("9_52_1")[:12], len(c("9_52_0")), len(c("9_52_1")), len(c("9_52_2")), h("9_52_2")[:12]))
    if k[0] == "offset":
        b = open(P("9_52_2"), "rb").read(); code, out = chk(P("9_52_2")); n = b.count(TAG); off = b.find(TAG); n2 = len(re.findall(rb"<meta charset", b))
        try: b[:1024].decode("utf-8"); dec = True
        except UnicodeDecodeError as e: dec = e.start >= 1022
        say(code == 0 and n == 1 and n2 == 1 and 0 <= off < 1024 and dec, "check tool exit %d: '%s'; the tag occurs %d time(s) (%d '<meta charset'), at byte %d; first 1024 bytes decode as UTF-8: %s" % (code, out, n, n2, off, dec))
    if k[0] == "diff":
        A = open(P("9_52_1"), encoding="utf-8").read(); B = open(P("9_52_2"), encoding="utf-8").read(); cm = re.compile(r"<!--.*?-->", re.S)
        ca = cm.findall(A); cb = cm.findall(B); miss = [x[:60] for x in ca if x not in cb]; new = [x[:80] for x in cb if x not in ca]
        strip = lambda s: cm.sub("", s).replace(TAG.decode(), "")
        sa, sb = strip(A), strip(B)
        res = []; ws = "none"
        if sa != sb:
            i = 0; n = min(len(sa), len(sb))
            while i < n and sa[i] == sb[i]: i += 1
            j = 0
            while j < n - i and sa[-1 - j] == sb[-1 - j]: j += 1
            res = [("residual", sa[i:len(sa) - j][:80], sb[i:len(sb) - j][:80])]
            if re.sub(r"\s", "", sa) == re.sub(r"\s", "", sb): res = []; ws = "line-break difference only (%d vs %d characters of whitespace after removing comments and the tag)" % (len(re.findall(r"\s", sa)), len(re.findall(r"\s", sb)))
        ids = lambda s: set(re.findall(r'\bid="([^"]+)"', s)) | set(re.findall(r"\b(data-[a-z0-9-]+)", s)); mi = sorted(ids(A) - ids(B))
        okc = not miss and len(new) == 1 and "version 9.52.2" in new[0]
        say(okc and not res and not mi, "comments of 9.52.1 missing in 9.52.2: %d; new comments: %d %s; after removing all comments and the tag, residual differences: %d %s (whitespace: %s); ids and data- hooks of 9.52.1 missing in 9.52.2: %d" % (len(miss), len(new), [x[:40] for x in new], len(res), res[:4], ws, len(mi)))
    if k[0] == "scratch":
        pg = os.path.join(T, "out" + NN, "sen0401_ch%s_page_v%s.html" % (NN, PV)); b = open(pg, "rb").read(); code, out = chk(pg); n = b.count(TAG); off = b.find(TAG)
        full = open(os.path.join(LOG, "sc05_9_36_0.full.log"), encoding="utf-8", errors="replace").read(); rn = open(os.path.join(LOG, "sc05_9_36_0.runner.txt"), encoding="utf-8", errors="replace").read()
        m = re.findall(r"exit (\d+)", " ".join(l for l in rn.splitlines() if l.startswith("page "))); w = re.search(r"widgets: (\d+) tested, (\d+) passed", full); fails = [l.strip()[:150] for l in full.splitlines() if l.strip().startswith("[FAIL]")]
        emb = b"course_page_template version 9.52.2" in b
        say(code == 0 and n == 1 and off < 1024 and emb and m and m[-1] == "0" and w and w.group(1) == w.group(2) and not fails, "scratch page of chapter 5 on 9.52.2: embeds 9.52.2 %s; check exit %d: '%s'; tag %d time(s) at byte %d; page test 9.36.0 exit %s, widgets %s, %d failed feature line(s)" % (emb, code, out, n, off, m[-1:] , w.groups() if w else None, len(fails)))
    if k[0] == "nochange":
        cs = k[1].split(","); st = []
        for c in cs: st += [(c, l) for l in sh("git", "show", "--name-status", "--format=", c, cwd=R).stdout.splitlines() if l.strip()]
        bad = [c + " " + l for c, l in st if not l.startswith("A\t")]; say(not bad, "commits %s: %d file(s) added, %d modified or removed %s" % (",".join(cs), len(st) - len(bad), len(bad), bad[:5]))
    raise SystemExit(__doc__)
main()
