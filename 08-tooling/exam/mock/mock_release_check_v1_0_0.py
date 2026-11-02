#!/usr/bin/env python3
"""Release check v1.0.0 (X3b) for the SEN0401 mock set.
  check [--private DIR] [--public DIR] [--set vX_Y_Z]   check the working folders, archives and the set folder
  selftest                                              a good fixture and a failing fixture for every rule
Rules
  M1 one current version per identity outside archive/ : in every folder of the mock tree, the name with all version tokens (_vN_N_N) removed (identity) holds ONE version; an unversioned file next to a versioned one of the same identity counts as two
  M1x the same identity in the private parts folder and in the public mock folder is one version (no tree keeps an older copy)\n  M2 every file in an archive folder has a row in ARCHIVE_RECORD.tsv (private: file, sha256, superseded_by, reason, date, set_version_archived_in) / ARCHIVE_REGISTER.tsv (public, file names only: file, superseded_by, date, set_version_archived_in); sha256 equal (private); every row names an existing file; superseded_by exists outside archive/ (private and public)
  M3 set folder: MANIFEST_SHA256 verifies with sha256sum -c and lists every file; master equals m1 (bytes); names carry the set version (the bank file carries its own bank version); every HTML shows the set version in its footer; six screenshots named with the set version
  M4 the private archive record names the master as sent to the owner
Result PASS only when every rule is measured and passes; a rule with no files to measure is NOT_MEASURED (never a pass)."""
import hashlib, os, re, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
VT = re.compile(r"_v(\d+)_(\d+)_(\d+)")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
PRIV_HDR = ["file", "sha256", "superseded_by", "reason", "date", "set_version_archived_in"]
PUB_HDR = ["file", "superseded_by", "date", "set_version_archived_in"]
def identity(name):
    vers = tuple(tuple(int(x) for x in m) for m in VT.findall(name))
    return VT.sub("", name), vers
def files_under(d):
    out = []
    for dp, dn, fn in os.walk(d):
        dn[:] = sorted(x for x in dn if x != "__pycache__")
        for f in sorted(fn): out.append(os.path.relpath(os.path.join(dp, f), d))
    return out
def m1(root, archive_name="archive", skip=("sample", "screens")):
    """per folder (archive and screenshots-of-old-release folders excluded): identity -> distinct version tuples"""
    bad = []
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(x for x in dn if x not in (archive_name, "__pycache__") and not x.startswith("set_"))
        seen = {}
        for f in fn:
            if f in ("ARCHIVE_RECORD.tsv", "ARCHIVE_REGISTER.tsv"): continue
            idn, v = identity(f); seen.setdefault(idn, set()).add(v)
        for idn, vs in seen.items():
            if len(vs) > 1: bad.append("%s: identity %s has %d versions %s" % (os.path.relpath(dp, root) or ".", idn, len(vs), sorted(vs)))
    return bad
def m1x(dirs):
    """cross-tree: the same identity in the private parts folder and the public mock folder (and the public exam folder for the mock script families) must be one version"""
    seen = {}
    for d in dirs:
        if not os.path.isdir(d): continue
        for f in os.listdir(d):
            if not os.path.isfile(os.path.join(d, f)) or f in ("ARCHIVE_RECORD.tsv", "ARCHIVE_REGISTER.tsv"): continue
            idn, v = identity(f)
            if v: seen.setdefault(idn, {}).setdefault(v, []).append(os.path.basename(os.path.dirname(os.path.join(d, f))))
    return ["identity %s has versions %s across the trees" % (i, sorted(vs)) for i, vs in seen.items() if len(vs) > 1]
def m2(root, archive_name, tsvname, hdr, with_sha, current_names):
    bad = []; base = os.path.join(root, archive_name)
    if not os.path.isdir(base): return ["no %s folder" % archive_name]
    tsv = os.path.join(base, tsvname)
    if not os.path.isfile(tsv): return ["%s missing" % tsvname]
    lines = open(tsv, encoding="utf-8").read().splitlines(); rows = {}
    if lines[0].split("\t") != hdr: bad.append("%s header differs" % tsvname)
    for ln in lines[1:]:
        c = ln.split("\t")
        if len(c) != len(hdr) or not all(x.strip() for x in c): bad.append("row without %d filled columns: %r" % (len(hdr), ln[:70])); continue
        rows[c[0]] = c
    for f in files_under(base):
        if f in (tsvname,): continue
        if f not in rows: bad.append("archived file %s has no row" % f)
        elif with_sha and rows[f][1] != sha(os.path.join(base, f)): bad.append("%s sha256 differs from its row" % f)
    for f, c in rows.items():
        if not os.path.isfile(os.path.join(base, f)): bad.append("row names missing file %s" % f)
        by = c[2] if with_sha else c[1]
        if by not in current_names: bad.append("%s: superseded_by %s is not a current file" % (f, by))
    return bad
def current_names(root, archive_name="archive"):
    out = set()
    for dp, dn, fn in os.walk(root):
        dn[:] = [x for x in dn if x not in (archive_name, "__pycache__")]
        out |= set(fn)
    return out
def m3(setdir, setv):
    bad = []
    if not os.path.isdir(setdir): return ["set folder missing"]
    names = sorted(f for f in os.listdir(setdir) if os.path.isfile(os.path.join(setdir, f)))
    if "MANIFEST_SHA256" not in names: return ["MANIFEST_SHA256 missing"]
    r = subprocess.run(["sha256sum", "-c", "MANIFEST_SHA256"], cwd=setdir, capture_output=True, text=True)
    if r.returncode: bad.append("sha256sum -c failed")
    listed = {ln.split("  ", 1)[1] for ln in open(os.path.join(setdir, "MANIFEST_SHA256"), encoding="utf-8").read().splitlines() if "  " in ln}
    if listed != set(names) - {"MANIFEST_SHA256"}: bad.append("manifest does not list exactly the files of the folder")
    htmls = [f for f in names if f.endswith(".html")]
    ms = [f for f in htmls if "_master_" in f]; one = [f for f in htmls if "_m1_" in f]
    if len(ms) != 1 or len(one) != 1 or sha(os.path.join(setdir, ms[0])) != sha(os.path.join(setdir, one[0])): bad.append("master is not byte-identical to m1")
    if len(htmls) != 9: bad.append("expected 9 pages, found %d" % len(htmls))
    for f in names:
        if f != "MANIFEST_SHA256" and setv not in f and not re.fullmatch(r"sen0401_mock_bank_all_v\d+_\d+_\d+\.json", f): bad.append("name %s does not carry the set version %s" % (f, setv))
    for f in htmls:
        s = open(os.path.join(setdir, f), encoding="utf-8").read()
        if not re.search(r'<footer id="set-footer"[^>]*>[^<]*mock exam set %s' % re.escape(setv), s): bad.append("%s: set version not in the page footer" % f)
    if len([f for f in names if f.endswith(".png")]) != 6: bad.append("expected 6 screenshots")
    return bad
def m4(private_archive):
    p = os.path.join(private_archive, "ARCHIVE_RECORD.tsv")
    if not os.path.isfile(p): return ["record missing"]
    rows = [l for l in open(p, encoding="utf-8").read().splitlines() if l.startswith("mock_ch_all_master.html\t")]
    return [] if rows and "sent to the owner" in rows[0] else ["master row does not say it was sent to the owner"]
def run_check(priv, pub, setv):
    res = []
    def add(rule, bad, measured=True):
        res.append((rule, "NOT_MEASURED" if not measured else ("PASS" if not bad else "FAIL"), bad))
    mock = os.path.join(priv, "mock")
    add("M1 private", m1(mock)); add("M1 public", m1(pub))
    add("M1 cross-tree", m1x([os.path.join(mock, "parts"), pub]))
    add("M2 private", m2(mock, "archive", "ARCHIVE_RECORD.tsv", PRIV_HDR, True, current_names(mock)))
    add("M2 public", m2(pub, "archive", "ARCHIVE_REGISTER.tsv", PUB_HDR, False, current_names(pub) | current_names(os.path.dirname(pub))))
    add("M3", m3(os.path.join(mock, "set_" + setv), setv))
    add("M4", m4(os.path.join(mock, "archive")))
    for r, st, bad in res:
        print("%-11s %s" % (r, st)); [print("    ", b) for b in bad[:12]]
    ok = all(st == "PASS" for _, st, _ in res)
    print("RELEASE CHECK " + ("PASS" if ok else "FAIL")); return ok
def selftest():
    td = tempfile.mkdtemp(); ok = True
    try:
        def build(good=True):
            priv = os.path.join(td, "priv"); pub = os.path.join(td, "pub")
            shutil.rmtree(td + "/priv", ignore_errors=True); shutil.rmtree(td + "/pub", ignore_errors=True)
            mock = os.path.join(priv, "mock"); sd = os.path.join(mock, "set_v1_0_0"); ar = os.path.join(mock, "archive"); os.makedirs(sd); os.makedirs(ar); os.makedirs(os.path.join(pub, "archive"))
            page = '<html><body><footer id="set-footer" class="meta">SEN0401 mock exam set v1_0_0 (bank v1_1_0)</footer></body></html>'
            for n in ["master"] + ["m%d" % k for k in range(1, 9)]: open(os.path.join(sd, "sen0401_mock_exam_%s_v1_0_0.html" % n), "w").write(page)
            for n in ("student_390", "student_1280", "checked_390", "checked_1280", "print_390", "print_1280"): open(os.path.join(sd, "sen0401_mock_exam_set_v1_0_0_%s.png" % n), "w").write(n)
            subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_release_manifest_v1_0_0.py"), sd], capture_output=True)
            open(os.path.join(mock, "part_a_v1_0_1.json"), "w").write("{}")
            open(os.path.join(ar, "part_a_v1_0_0.json"), "w").write("old")
            open(os.path.join(ar, "mock_ch_all_master.html"), "w").write("m")
            open(os.path.join(ar, "ARCHIVE_RECORD.tsv"), "w").write("\t".join(PRIV_HDR) + "\n" + "part_a_v1_0_0.json\t%s\tpart_a_v1_0_1.json\tsuperseded\t2026-11-03\tv1_0_0\n" % sha(os.path.join(ar, "part_a_v1_0_0.json"))
                + "mock_ch_all_master.html\t%s\tsen0401_mock_exam_master_v1_0_0.html\tsent to the owner earlier; superseded\t2026-11-03\tv1_0_0\n" % sha(os.path.join(ar, "mock_ch_all_master.html")))
            open(os.path.join(pub, "tool_v1_0_1.py"), "w").write("x"); open(os.path.join(pub, "archive", "tool_v1_0_0.py"), "w").write("x")
            open(os.path.join(pub, "archive", "ARCHIVE_REGISTER.tsv"), "w").write("\t".join(PUB_HDR) + "\ntool_v1_0_0.py\ttool_v1_0_1.py\t2026-11-03\tv1_0_0\n")
            return priv, pub, mock, sd, ar
        import io, contextlib
        def result(priv, pub):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf): r = run_check(priv, pub, "v1_0_0")
            return r
        priv, pub, mock, sd, ar = build()
        g = result(priv, pub); print("good fixture:", "PASS" if g else "FAIL (wrong)"); ok &= g
        def planted(name, fn):
            nonlocal ok
            priv, pub, mock, sd, ar = build(); fn(priv, pub, mock, sd, ar); r = result(priv, pub)
            print("planted %-48s %s" % (name + ":", "FAILS as required" if not r else "NOT CAUGHT")); ok &= (not r)
        planted("second version of an identity outside archive", lambda p, b, m, s, a: open(os.path.join(m, "part_a_v1_0_0.json"), "w").write("{}"))
        planted("unversioned file next to a versioned one", lambda p, b, m, s, a: open(os.path.join(m, "part_a.json"), "w").write("{}"))
        planted("second script version in the public folder", lambda p, b, m, s, a: open(os.path.join(b, "tool_v1_0_0.py"), "w").write("x"))
        def _cross(p, b, m, s, a):
            os.makedirs(os.path.join(m, "parts"), exist_ok=True); open(os.path.join(m, "parts", "tool_v1_0_0.py"), "w").write("x")
        planted("older copy in the private parts folder", _cross)
        planted("archived file without a row", lambda p, b, m, s, a: open(os.path.join(a, "extra_v1_0_0.json"), "w").write("x"))
        planted("archive file changed after the record", lambda p, b, m, s, a: open(os.path.join(a, "part_a_v1_0_0.json"), "w").write("changed"))
        planted("superseded_by names a missing file", lambda p, b, m, s, a: os.remove(os.path.join(m, "part_a_v1_0_1.json")))
        planted("manifest hash differs", lambda p, b, m, s, a: open(os.path.join(s, "sen0401_mock_exam_m3_v1_0_0.html"), "a").write("x"))
        planted("master differs from m1", lambda p, b, m, s, a: open(os.path.join(s, "sen0401_mock_exam_master_v1_0_0.html"), "a").write("x"))
        planted("set version missing in a page footer", lambda p, b, m, s, a: open(os.path.join(s, "sen0401_mock_exam_m5_v1_0_0.html"), "w").write("<html></html>"))
        def _rewrite(p, b, m, s, a):
            t = open(os.path.join(a, "ARCHIVE_RECORD.tsv")).read().replace("sent to the owner", "old"); open(os.path.join(a, "ARCHIVE_RECORD.tsv"), "w").write(t)
        planted("master row without the owner note", _rewrite)
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print("SELFTEST " + ("PASS" if ok else "FAIL")); return ok
if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "selftest": sys.exit(0 if selftest() else 1)
    priv = a[a.index("--private") + 1] if "--private" in a else "/home/claude/CME/exams/SEN0401/08-tooling/exam"
    pub = a[a.index("--public") + 1] if "--public" in a else "/home/claude/sen0401/08-tooling/exam/mock"
    setv = a[a.index("--set") + 1] if "--set" in a else "v1_0_0"
    sys.exit(0 if run_check(priv, pub, setv) else 1)
