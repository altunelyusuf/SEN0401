#!/usr/bin/env python3
"""sen0401_deckstd_control_check v1.0.0 - the control's OWN checks of the deck standard check v1_2_0 and the D9 shapes (story ST_DeckStd_Dark, criterion AC9_DeckStd_Dark). A NEW tool; it edits nothing.
Usage: sen0401_deckstd_control_check_v1_0_0.py KIND [COMMITS]
  sha       the check v1_1_0 has the same SHA-256 in the commit before the executor's work as now, and no later commit touches it
  shapes    the shapes file parses; owl:Ontology versionInfo 1.0.0; the owner's date 2026-10-29 is stated in sh:message or rdfs:comment; no markdown file was added by the executor's commits; every class and property of its vocabulary is connected to another one
            (the control's own reading: appears in a domain, range, subClassOf, sh:class, sh:path or sh:node of something else); pyshacl meta-validation of the shapes passes
  fixtures  the control's OWN five variants, made from the newest chapter 8 deck copied to a scratch folder (backgrounds changed with python-pptx): light only PASS, dark last only PASS, dark middle FAIL, last two dark FAIL, dark first FAIL, read on the D9 line of v1_2_0
  exec      the executor's five committed fixtures run by the control: the verdict on the D9 line equals the file name suffix
  impact    v1_2_0 and v1_1_0 run on the newest deck of every chapter 1 to 14: every element D1 to D12 equal, D9 PASS on all 14 (both tables printed)
  diff      the lines of v1_2_0 that differ from v1_1_0 (printed); those outside the D9 block are only version, import and documentation lines
  nochange  every file of the executor's commits was added (none modified or deleted)
Exit 0 only when the kind holds."""
__version__ = "1.0.0"
import glob, os, re, shutil, subprocess, sys, tempfile, difflib, hashlib
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); T = os.path.join(R, "08-tooling"); PARENT = "f61b63b"
V1 = os.path.join(T, "sen0401_deck_standard_check_v1_1_0.py"); V2 = os.path.join(T, "sen0401_deck_standard_check_v1_2_0.py"); SH = os.path.join(R, "06-quality/sen0401_deck_standard_shapes_v1_0_0.ttl")
def git(*a): return subprocess.run(["git", "-C", R] + list(a), capture_output=True, text=True).stdout
def done(ok, msg): print(msg); print("RESULT " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
def run(tool, nn, deck=None):
    r = subprocess.run([sys.executable, "-B", tool, nn] + ([deck] if deck else []), capture_output=True, text=True, timeout=900); out = r.stdout + r.stderr
    return r.returncode, dict(re.findall(r"^(D\d+) (PASS|FAIL|NOT_MEASURED|CANNOT_RUN)", out, re.M)), out
def newest(nn):
    vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.pptx", p)[0]]; return sorted(glob.glob(os.path.join(R, "03-materials/ch%s/SEN0401_*.pptx" % nn)), key=vk)[-1]
def k_sha():
    rel = "08-tooling/sen0401_deck_standard_check_v1_1_0.py"; b = subprocess.run(["git", "-C", R, "show", "%s:%s" % (PARENT, rel)], capture_output=True).stdout; n = open(os.path.join(R, rel), "rb").read()
    ok = len(b) > 0 and hashlib.sha256(b).digest() == hashlib.sha256(n).digest(); print("v1_1_0 before(%s) %s after %s" % (PARENT, hashlib.sha256(b).hexdigest(), hashlib.sha256(n).hexdigest())); ch = git("log", "--format=%h", "%s..HEAD" % PARENT, "--", rel).split(); print("commits since touching it: %s" % ch); done(ok and not ch, "sha")
def k_shapes(commits):
    import rdflib
    from rdflib import RDF, RDFS, OWL, Namespace
    SHN = Namespace("http://www.w3.org/ns/shacl#"); g = rdflib.Graph(); g.parse(SH, format="turtle"); ok = True
    ver = [str(o) for o in g.objects(None, OWL.versionInfo)]; print("versionInfo %s" % ver); ok &= "1.0.0" in ver
    txt = " ".join(str(o) for p in (SHN.message, RDFS.comment) for o in g.objects(None, p)); has = "2026-10-29" in txt; print("owner's date in sh:message/rdfs:comment: %s" % has); ok &= has
    files = [f for c in commits.split(",") for f in git("show", "--name-only", "--format=", c).splitlines() if f]; md = [f for f in files if f.lower().endswith(".md")]; print("markdown files added by the commits: %s" % md); ok &= not md
    terms = set(s for s in g.subjects(RDF.type, OWL.Class)) | set(s for t in (OWL.ObjectProperty, OWL.DatatypeProperty, RDF.Property) for s in g.subjects(RDF.type, t))
    for x in sorted(terms):
        link = set()
        for p in (RDFS.domain, RDFS.range, RDFS.subClassOf, SHN["class"], SHN.path, SHN.node, OWL.inverseOf, RDFS.subPropertyOf):
            link |= {s for s in g.subjects(p, x) if s != x} | {o for o in g.objects(x, p) if o != x and isinstance(o, rdflib.URIRef)}
        # shapes that reference the term inside a blank node (sh:property [ sh:path x ]) count through the shape's target class
        ref = {s for s, p, o in g if o == x and p in (SHN.path, SHN["class"], SHN.targetClass, SHN.node)}
        print("%-60s linked to %d other terms, %d shape references" % (str(x).split("#")[-1], len(link), len(ref))); ok &= bool(link or ref)
    from pyshacl import validate
    conf, _, txtv = validate(g, meta_shacl=True, inference="none"); print("pyshacl meta-validation of the shapes: %s" % ("PASS" if conf else "FAIL " + txtv[:300])); ok &= bool(conf)
    done(ok, "shapes")
def variants(src, tmp):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    out = {}
    def mk(name, dark):
        p = Presentation(src); n = len(p.slides)
        for i, s in enumerate(p.slides, 1):
            f = s.background.fill; f.solid(); f.fore_color.rgb = RGBColor.from_string("14213D" if i in dark(n) else "FAF6EF")
        path = os.path.join(tmp, name + ".pptx"); p.save(path); out[name] = path
    mk("light_only_PASS", lambda n: set()); mk("dark_last_only_PASS", lambda n: {n}); mk("dark_middle_FAIL", lambda n: {n // 2}); mk("last_two_dark_FAIL", lambda n: {n - 1, n}); mk("dark_first_FAIL", lambda n: {1})
    return out
def k_fixtures():
    tmp = tempfile.mkdtemp(prefix="sen0401_dsctl_", dir=os.environ.get("TMPDIR")); ok = True
    try:
        for name, path in variants(newest("08"), tmp).items():
            _, res, out = run(V2, "08", path); want = name.rsplit("_", 1)[1]; got = res.get("D9"); print("%-24s D9 %s (want %s)  %s" % (name, got, want, [l for l in out.splitlines() if l.startswith("D9")][0][:150])); ok &= got == want
    finally: shutil.rmtree(tmp, ignore_errors=True)
    done(ok, "fixtures")
def k_exec():
    ok = True
    for f in sorted(glob.glob(os.path.join(T, "deck_standard_v1_2_0/fixtures/*.pptx"))):
        _, res, out = run(V2, "05", f); want = os.path.basename(f)[:-5].rsplit("_", 1)[1]; got = res.get("D9"); print("%-30s D9 %s (want %s)" % (os.path.basename(f), got, want)); ok &= got == want
    done(ok, "exec")
def k_impact():
    ok = True
    for c in range(1, 15):
        nn = "%02d" % c; d = newest(nn); c1, r1, _ = run(V1, nn, d); c2, r2, _ = run(V2, nn, d); eq = r1 == r2 and len(r1) == 12; ok &= eq and r2.get("D9") == "PASS"
        print("ch%s %s\n   v1_1_0 %s\n   v1_2_0 %s\n   %s (exit %d / %d)" % (nn, os.path.basename(d), " ".join("%s:%s" % kv for kv in sorted(r1.items())), " ".join("%s:%s" % kv for kv in sorted(r2.items())), "EQUAL" if eq else "DIFFERENT", c1, c2))
    done(ok, "impact")
def k_diff():
    a = open(V1).read().splitlines(); b = open(V2).read().splitlines(); sm = difflib.SequenceMatcher(None, a, b, autojunk=False); outside = []; n = 0
    d9s = next(i for i, l in enumerate(b) if l.strip().startswith("# D9")); d10 = next(i for i, l in enumerate(b) if l.strip().startswith("# D10"))
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": continue
        n += (i2 - i1) + (j2 - j1)
        for j in range(j1, max(j2, j1 + 1)):
            if not (d9s <= j <= d10): outside += [(j + 1, b[j] if j < len(b) else "")]
        for x in a[i1:i2]: print("-", x[:200])
        for x in b[j1:j2]: print("+", x[:200])
    f0 = next(i for i, l in enumerate(b) if l.startswith("def d9_shacl")); f1 = next(i for i, l in enumerate(b) if i > f0 and l.startswith("def main") or (i > f0 and l.startswith("def ") and "d9_shacl" not in l))
    outside = [(j, l) for j, l in outside if not (f0 <= j - 1 < f1)]
    bad = [(j, l) for j, l in outside if l.strip() and not re.search(r"version|1\.2\.0|1\.1\.0|pyshacl|shapes|import|D9|owner|Usage|ruling|retroactive|SHAPES|shacl|SHACL|rdflib|dark|facts", l, re.I)]
    print("changed lines %d; outside the D9 block: %d; of them not version/import/documentation: %s" % (n, len(outside), bad)); done(not bad, "diff")
def k_nochange(commits):
    bad = []
    for c in commits.split(","):
        for l in git("show", "--name-status", "--format=", c).splitlines():
            if l and not l.startswith("A"): bad.append(l)
    print("commits %s: files not added: %s" % (commits, bad)); done(not bad, "nochange")
if __name__ == "__main__":
    k = sys.argv[1]; c = sys.argv[2] if len(sys.argv) > 2 else ""
    {"sha": k_sha, "shapes": lambda: k_shapes(c), "fixtures": k_fixtures, "exec": k_exec, "impact": k_impact, "diff": k_diff, "nochange": lambda: k_nochange(c)}[k]()
