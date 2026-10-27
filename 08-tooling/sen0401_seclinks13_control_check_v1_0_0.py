#!/usr/bin/env python3
"""sen0401_seclinks13_control_check v1.0.0 - the control's OWN checks of the chapter 13 research v1_1_0 (story ST_SecLinks_Ch13). A NEW tool; it edits nothing.
Usage: sen0401_seclinks13_control_check_v1_0_0.py KIND
  sha    every v1_0_x file of 03-materials/ch13/rdodi has the same SHA-256 in the parent of the executor's first commit (6f169be) as now, and no later commit touches one
  props  (rdflib) every property of the v1_1_0 domain T-Box that carries a relationship category has a label, a domain and a range; the v1_1_0 A-Box states at least 16 links with such properties between named individuals (printed by property)
  build  the page-data builder v2_24_0 builds a scratch page data on the newest research (output in the folder TMPDIR, deleted afterwards); counted here: relations whose two ends lie in two different sections (level-2 ancestors), the sections with none, the types; exit 0 only when no section is without a link and every type is one the template draws on other chapters
  Exit 0 only when the kind holds."""
__version__ = "1.0.0"
import collections, glob, hashlib, json, os, shutil, subprocess, sys, tempfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RD = "03-materials/ch13/rdodi"; FIRST = "6f169be"
def git(*a): return subprocess.run(["git", "-C", R] + list(a), capture_output=True).stdout
def done(ok, msg): print(msg); print("RESULT " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
def sha():
    ok = True; n = 0
    for f in sorted(glob.glob(os.path.join(R, RD, "sen0401_ch13_*_v1_0_[0-9].ttl"))):
        rel = os.path.relpath(f, R); b = git("show", "%s^:%s" % (FIRST, rel)); k = len(b) > 0 and hashlib.sha256(b).hexdigest() == hashlib.sha256(open(f, "rb").read()).hexdigest(); n += 1; ok &= k
        if not k: print("DIFFERENT or missing before:", rel)
    ch = git("log", "--format=%h", "%s^..HEAD" % FIRST, "--diff-filter=MD", "--", RD).split()
    print("%d v1_0_x files compared with the parent of %s; commits since that modified or deleted a file of %s: %s" % (n, FIRST, RD, ch)); done(ok and n == 15 and not ch, "sha")
def props():
    from rdflib import Graph, RDFS, RDF, OWL, URIRef
    tb, ab = Graph(), Graph(); tb.parse(os.path.join(R, RD, "sen0401_ch13_domain_tbox_v1_1_0.ttl")); ab.parse(os.path.join(R, RD, "sen0401_ch13_domain_abox_v1_1_0.ttl"))
    cat = [p for p in set(tb.predicates()) if str(p).endswith("hasRelationshipCategory")]; ps = sorted({s for p in cat for s, o in tb.subject_objects(p)}, key=str)
    bad = [str(p) for p in ps if not (list(tb.objects(p, RDFS.label)) and list(tb.objects(p, RDFS.domain)) and list(tb.objects(p, RDFS.range)))]
    use = collections.Counter(); named = lambda x: isinstance(x, URIRef)
    for p in ps:
        for s, o in ab.subject_objects(p):
            if named(s) and named(o): use[str(p).split("#")[-1].split("/")[-1]] += 1
    print("properties with a relationship category: %d; without label/domain/range: %s; A-Box links between named individuals by property: %s (total %d)" % (len(ps), bad, dict(use), sum(use.values()))); done(len(ps) >= 1 and not bad and sum(use.values()) >= 16, "props")
def build():
    tmp = tempfile.mkdtemp(prefix="sen0401_sl13ctl_", dir=os.environ.get("TMPDIR")); out = os.path.join(tmp, "pd"); os.makedirs(out)
    try:
        r = subprocess.run(["python3", "-B", os.path.join(R, "08-tooling/sen0401_page_data_v2_24_0.py"), "13", "/home/claude/venv314/bin/python"], capture_output=True, text=True, env=dict(os.environ, PAGE_DATA_OUT=out, PAGE_VER="9_99_0"), cwd=R)
        print((r.stdout.strip().splitlines() or [""])[-1][:200]); fs = glob.glob(os.path.join(out, "page_data_v9_99_0.json"))
        if r.returncode or not fs: print(r.stderr[-400:]); done(False, "build failed")
        d = json.load(open(fs[0]))
    finally: shutil.rmtree(tmp, ignore_errors=True)
    ns = {n["id"]: n for n in d["nodes"]}
    def sec(i):
        n = ns.get(i)
        while n and n["level"] > 2: n = ns.get(n["parent"])
        return n["id"] if n and n["level"] == 2 else None
    secs = sorted(n["id"] for n in d["nodes"] if n["level"] == 2); cross = []
    for x in d["relations"]:
        a, b = sec(x["source"]), sec(x["target"])
        if x["type"] != "is a kind of" and a and b and a != b: cross.append((a, b, x["type"]))
    cnt = {s: 0 for s in secs}
    for a, b, _ in cross: cnt[a] += 1; cnt[b] += 1
    types = collections.Counter(t for _, _, t in cross); none = [s for s, c in cnt.items() if c == 0]
    seen = set()
    for f in glob.glob(os.path.join(R, "08-tooling/ch*-page/page_data_v9_*.json")):
        if "ch13" in f: continue
        try: seen |= {x["type"] for x in json.load(open(f))["relations"]}
        except Exception: pass
    print("research %s; sections %d; relations in all %d; between two different sections %d, types %s, pairs %d; sections with none: %s; types not seen on other chapters' pages: %s" % (d["research_file"], len(secs), len(d["relations"]), len(cross), dict(types), len({frozenset(c[:2]) for c in cross}), none, sorted(set(types) - seen)))
    done(len(secs) == 16 and cross and not none and not (set(types) - seen), "build")
if __name__ == "__main__": {"sha": sha, "props": props, "build": build}[sys.argv[1]]()
