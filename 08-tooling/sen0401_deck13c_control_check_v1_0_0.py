#!/usr/bin/env python3
"""sen0401_deck13c_control_check v1.0.0 - the control's OWN checks of the chapter 13 deck v2_3_0 and the manifest v1_2_0 (story ST_Deck13_Charts). A NEW tool; it edits nothing.
Usage: sen0401_deck13c_control_check_v1_0_0.py KIND [COMMITS]
  sha       the deck v2_1_0 and the manifest v1_0_0 have the same SHA-256 in the commit before the executor's work (git, parent of the first commit) as now
  parts     the zip parts of the deck v2_1_0 and v2_2_0 differ only in docProps/core.xml, ppt/slides/slide24.xml and the notes part of slide 24 (same part list)
  textdiff  the text of every shape and table and the notes of every slide: only slide 24 differs, and the differing lines name example 12 (printed in full)
  links     the set of hyperlink addresses of v2_1_0 equals that of v2_2_0 (printed with the count)
  codeeq    for every manifest v1_1_0 example the code lines equal the '>>> ' / '... ' rows of its slide in v2_2_0 (strict where v1_0_0 against v2_1_0 is equal as well; the baseline count is printed)
  run28     (Python 3.14 of venv314) all examples of the manifest run on the wheel's stored run, one fresh namespace each after the setup: every show expression repr equals its expected text
  dcheck    the deck check v1_1_0 under venv314 on v2_2_0 (an extra reading: it is not an element of the criterion AC9_Deck13_Ex12)
  noerr     (same run) no result text of any example carries 'Error:', 'Traceback' or 'NameError' in its first 160 characters (the page test 9.37.0's rule)
Exit 0 only when the kind holds."""
__version__ = "1.0.0"
import difflib, hashlib, json, os, re, subprocess, sys, zipfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(R, "03-materials/ch13")
OLD = os.path.join(D, "SEN0401_Ch13_BitcoinSecurity_3e_v2_2_0.pptx"); NEW = os.path.join(D, "SEN0401_Ch13_BitcoinSecurity_3e_v2_3_0.pptx")
MO = os.path.join(D, "page/chapter_code_ch13_v1_1_0.json"); MN = os.path.join(D, "page/chapter_code_ch13_v1_2_0.json")
PARENT = "0f037d5"
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*a): return subprocess.run(["git", "-C", R] + list(a), capture_output=True).stdout
def done(ok, msg): print(msg); print("RESULT " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
def texts(path):
    from pptx import Presentation
    out = []
    for s in Presentation(path).slides:
        l = []
        for sh in s.shapes:
            if sh.has_text_frame: l += [p.text for p in sh.text_frame.paragraphs]
            if sh.has_table: l += [" | ".join(c.text for c in r.cells) for r in sh.table.rows]
        out.append((l, s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""))
    return out
def links(p):
    z = zipfile.ZipFile(p); o = set()
    for n in z.namelist():
        if re.match(r"ppt/slides/_rels/slide\d+\.xml\.rels$", n):
            for m in re.finditer(r"<Relationship [^>]*>", z.read(n).decode()):
                if "/hyperlink" in m.group(0): o.add(re.search(r'Target="([^"]+)"', m.group(0)).group(1))
    return o
def rows(deck, slide):
    from pptx import Presentation
    s = Presentation(deck).slides[slide - 1]; o = []
    for sh in s.shapes:
        if sh.has_text_frame: o += [p.text for p in sh.text_frame.paragraphs if p.text.startswith((">>> ", "... "))]
    return [x[4:] for x in o]
def kind_sha():
    ok = True
    for rel in ("03-materials/ch13/SEN0401_Ch13_BitcoinSecurity_3e_v2_2_0.pptx", "03-materials/ch13/page/chapter_code_ch13_v1_1_0.json"):
        b = git("show", "%s:%s" % (PARENT, rel)); n = open(os.path.join(R, rel), "rb").read(); k = sha(b) == sha(n) and len(b) > 0; ok &= k
        print("%s before(%s) %s after %s %s" % (rel, PARENT, sha(b), sha(n), "equal" if k else "DIFFERENT"))
    ch = git("log", "--format=%h", "%s..HEAD" % PARENT, "--", "03-materials/ch13/SEN0401_Ch13_BitcoinSecurity_3e_v2_2_0.pptx", "03-materials/ch13/page/chapter_code_ch13_v1_1_0.json").split()
    print("commits since touching either file: %s" % ch); done(ok and not ch, "sha")
def kind_parts():
    a, b = zipfile.ZipFile(OLD), zipfile.ZipFile(NEW); na, nb = sorted(a.namelist()), sorted(b.namelist()); diff = [n for n in na if n in nb and a.read(n) != b.read(n)]
    rel = zipfile.ZipFile(NEW).read("ppt/slides/_rels/slide24.xml.rels").decode(); notes = re.findall(r"notesSlides/(notesSlide\d+\.xml)", rel)
    allowed = {"docProps/core.xml", "ppt/slides/slide24.xml", "ppt/charts/chart2.xml"} | {"ppt/notesSlides/" + x for x in notes}
    print("part lists equal: %s (%d parts); differing parts: %s; allowed: %s" % (na == nb, len(na), diff, sorted(allowed))); done(na == nb and set(diff) <= allowed and "ppt/charts/chart2.xml" in diff, "parts")
def kind_textdiff():
    a, b = texts(OLD), texts(NEW); ch = [i + 1 for i in range(min(len(a), len(b))) if a[i] != b[i]]
    print("slides %d and %d; slides whose text or notes differ: %s" % (len(a), len(b), ch))
    if ch == [24]:
        for l in difflib.unified_diff(a[23][0], b[23][0], "v2_2_0", "v2_3_0", lineterm="", n=0): print(l)
        print("notes %s" % ("same" if a[23][1] == b[23][1] else "differ"))
        if a[23][1] != b[23][1]:
            for l in difflib.unified_diff(a[23][1].splitlines(), b[23][1].splitlines(), "n2_2_0", "n2_3_0", lineterm="", n=0): print(l)
        gone = [l for l in a[23][0] if l not in b[23][0]]; new = [l for l in b[23][0] if l not in a[23][0]]
        key = re.compile(r"Sending is refused|wrong passphrase|incorrect|Error|msg|spend|shown|wrong|wallet|balance_visible|removeprefix|passphrase|1\.0|b4_|left|u = |l = ")
        bad = [l for l in gone + new if not key.search(l)]; print("changed lines not naming example 12 terms: %s" % bad); done(not bad, "textdiff")
    done(False, "textdiff")
def kind_links():
    a, b = links(OLD), links(NEW); print("distinct addresses v2_2_0: %d, v2_3_0: %d; only in old: %s; only in new: %s" % (len(a), len(b), sorted(a - b), sorted(b - a))); done(a == b and len(b) == 14, "links")
def kind_codeeq():
    def chk(man, deck):
        bad = []; n = 0
        for e in json.load(open(man))["examples"]:
            code = [l for l in e["code"].splitlines()]; r = rows(deck, e["slide"]); n += 1
            if [l.rstrip() for l in code if l.strip()] != [l.rstrip() for l in r if l.strip()]: bad.append((e["order"], e["slide"], e["name"]))
        return n, bad
    n0, b0 = chk(MO, OLD); n1, b1 = chk(MN, NEW)
    print("baseline v1_0_0 against v2_1_0: %d examples, %d unequal %s" % (n0, len(b0), b0)); print("v1_1_0 against v2_2_0: %d examples, %d unequal %s" % (n1, len(b1), b1))
    for e in json.load(open(MN))["examples"]:
        if e["order"] == 12: print("manifest ex12 code:\n" + e["code"]); print("deck slide 24 rows:\n" + "\n".join(rows(NEW, 24)))
    done(n1 == 28 and set(b1) <= set(b0) and not [x for x in b1 if x[0] == 12], "codeeq")
def kind_run(noerr):
    v = "/home/claude/venv314/bin/python"
    if os.path.realpath(sys.executable) != os.path.realpath(v) and not os.environ.get("D13_INNER"):
        r = subprocess.run([v, "-B", os.path.abspath(__file__), "noerr" if noerr else "run28"], env=dict(os.environ, D13_INNER="1")); sys.exit(r.returncode)
    import tempfile, shutil, platform
    m = json.load(open(MN)); tmp = tempfile.mkdtemp(prefix="sen0401_d13ctl_", dir=os.environ.get("TMPDIR")); bad = []; res = []
    try:
        zipfile.ZipFile(os.path.join(R, m["library"]["file"])).extractall(tmp); sys.path.insert(0, tmp); os.chdir(tmp)
        for e in m["examples"]:
            ns = {}; exec(m["setup"]["code"], ns); exec(e["code"], ns)
            for s in e["show"]:
                got = repr(eval(s["expression"], ns)); res.append((e["order"], got))
                if noerr:
                    if re.search(r"Traceback|NameError|Error:", got[:160]): bad.append((e["order"], got[:70]))
                elif got != s["expected"]: bad.append((e["order"], s["expression"], got[:70], s["expected"][:70]))
    finally:
        os.chdir(R); shutil.rmtree(tmp, ignore_errors=True)
    print("python %s; %d examples, %d result texts; defects: %s" % (platform.python_version(), len(m["examples"]), len(res), bad)); done(not bad and len(m["examples"]) == 28, "noerr" if noerr else "run28")

def kind_chart():
    import re as _re
    a, b = zipfile.ZipFile(OLD).read("ppt/charts/chart2.xml").decode(), zipfile.ZipFile(NEW).read("ppt/charts/chart2.xml").decode()
    vals = lambda x: _re.findall(r"<c:v>([^<]*)</c:v>", x); typ = lambda x: sorted(set(_re.findall(r"<c:(\w+Chart)>", x)))
    lab = lambda x: len(_re.findall(r"<c:dLbls>", x)); shown = "<c:showVal val=\"1\"/>" in b
    print("chart2 values equal: %s (%d values); chart types old %s new %s; dLbls blocks old %d new %d; showVal=1 in new: %s" % (vals(a) == vals(b), len(vals(b)), typ(a), typ(b), lab(a), lab(b), shown))
    n1 = lambda x: x.count('<c:showVal val="1"/>'); n0 = lambda x: x.count('<c:showVal val="0"/>'); print("showVal=1 old %d new %d; showVal=0 old %d new %d" % (n1(a), n1(b), n0(a), n0(b)))
    ok = vals(a) == vals(b) and typ(a) == typ(b) and n1(b) > n1(a) and n0(b) == 0 and shown
    z = zipfile.ZipFile(NEW); nolab = [n for n in z.namelist() if _re.match(r"ppt/charts/chart\d+\.xml$", n) and "<c:dLbls>" not in z.read(n).decode()]
    print("chart parts without data labels in v2_3_0: %s" % nolab); done(ok and not nolab, "chart")
def kind_mfields():
    a, b = json.load(open(MO)), json.load(open(MN)); diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    print("manifest keys that differ: %s; manifest=%s deck=%s deck_version=%s" % (diff, b["manifest"], b["deck"], b["deck_version"]))
    done(diff == ["deck", "deck_version", "manifest"] and b["deck"].endswith("v2_3_0.pptx") and b["deck_version"] == "2.3.0" and b["manifest"] == "chapter_code_ch13_v1_2_0", "mfields")
def kind_dcheck_old():
    r = subprocess.run(["/home/claude/venv314/bin/python", "-B", os.path.join(R, "08-tooling/sen0401_deck_check_v1_1_0.py"), "13", OLD], capture_output=True, text=True); print((r.stdout + r.stderr).strip()[-300:]); print("exit %d (the comparison reading: v2_2_0 is expected to be refused)" % r.returncode); done(r.returncode == 1, "dcheck_old")
def kind_dcheck():
    r = subprocess.run(["/home/claude/venv314/bin/python", "-B", os.path.join(R, "08-tooling/sen0401_deck_check_v1_1_0.py"), "13", NEW], capture_output=True, text=True); print((r.stdout + r.stderr).strip()); print("exit %d" % r.returncode); done(r.returncode == 0, "dcheck")
if __name__ == "__main__":
    k = sys.argv[1]; {"sha": kind_sha, "parts": kind_parts, "textdiff": kind_textdiff, "links": kind_links, "codeeq": kind_codeeq, "run28": lambda: kind_run(False), "noerr": lambda: kind_run(True), "dcheck": kind_dcheck, "chart": kind_chart, "mfields": kind_mfields, "dcheck_old": kind_dcheck_old}[k]()
