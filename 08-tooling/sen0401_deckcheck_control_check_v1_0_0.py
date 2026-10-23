#!/usr/bin/env python3
"""sen0401_deckcheck_control_check v1.0.0 - the builder's own checks of TK_Ch78_DeckCheck (criterion AC7_DeckCheck): the builder runs both versions of the deck standard check itself and counts the research concepts with its OWN reader (rdflib). A NEW tool; it edits no committed file.
Usage: sen0401_deckcheck_control_check_v1_0_0.py KIND
  nochange:SHAS  every file of the commits (comma list) has git status A (element 1: the file is new, nothing committed earlier is edited)
  sha100         v1_0_0 equals its committed blob (git hash-object against the commit that added it) and the executor's SHA logs show the same value before and after (element 1)
  diffclass      v1_1_0 equals v1_0_0 once the version words are mapped back and the reading of the class sen0414:PrimarySourceConcept is removed (element 2)
  same567        chapters 5, 6 and 7: v1_0_0 and v1_1_0 print the same lines (apart from the version words) and the same exit code (element 3)
  measured       chapters 8 to 14: v1_1_0 prints PASS or FAIL for D4 and D11 (never NOT_MEASURED) and v1_0_0 printed NOT_MEASURED for them (element 4)
  counts         chapters 8 to 14: the builder counts the declarations of the class in the newest research file (rdflib) and the de-duplicated labels (the check's own definition, normalised label); the declarations equal 46,38,62,43,43,29,69 and the de-duplicated number equals the number v1_1_0 prints in D4 (element 4)
Exit 0 only when the check holds."""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
V0 = os.path.join(H, "sen0401_deck_standard_check_v1_0_0.py"); V1 = os.path.join(H, "sen0401_deck_standard_check_v1_1_0.py")
RAW = {"08": 46, "09": 38, "10": 62, "11": 43, "12": 43, "13": 29, "14": 69}
def sh(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, **k)
def say(ok, msg): print("%s %s" % ("PASS" if ok else "FAIL", msg)); sys.exit(0 if ok else 1)
def run(tool, ch): r = sh(sys.executable, "-B", tool, ch, cwd=R); return r.returncode, r.stdout
def norm(s):
    s = re.sub(r"\([^)]*\)", " ", s.lower()); s = re.sub(r"[^a-z0-9]+", " ", s).strip(); return " ".join(w[:-1] if w.endswith("s") and len(w) > 1 else w for w in s.split())
def ver(p): return tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups())
def main():
    k = sys.argv[1].split(":")
    if k[0] == "nochange":
        st = []
        for c in k[1].split(","): st += [(c, l) for l in sh("git", "show", "--name-status", "--format=", c, cwd=R).stdout.splitlines() if l.strip()]
        bad = [c + " " + l for c, l in st if not l.startswith("A\t")]; say(bool(st) and not bad, "commits %s: %d file(s) added, %d modified or removed %s" % (k[1], len(st) - len(bad), len(bad), bad[:5]))
    if k[0] == "sha100":
        rel = "08-tooling/sen0401_deck_standard_check_v1_0_0.py"; blob = sh("git", "rev-parse", "271ce28:" + rel, cwd=R).stdout.strip(); now = sh("git", "hash-object", V0, cwd=R).stdout.strip()
        d = os.path.join(H, "deckcheck_v1_1_0_logs"); b = open(os.path.join(d, "sha_v1_0_0_before.log")).read().split(); a = open(os.path.join(d, "sha_v1_0_0_after.log")).read().split()
        h = hashlib.sha256(open(V0, "rb").read()).hexdigest(); say(blob == now and h in b and h in a, "working file equals the committed blob %s (%s); SHA-256 %s appears in the executor's before log %s and after log %s" % (blob[:10], blob == now, h[:12], h in b, h in a))
    t0 = open(V0, encoding="utf-8").read(); t1 = open(V1, encoding="utf-8").read()
    if k[0] == "diffclass":
        back = t1.replace("1.1.0", "1.0.0").replace("1_1_0", "1_0_0").replace(" or sen0414:PrimarySourceConcept", "").replace("sen04(?:01|14):", "sen0401:")
        import difflib; dl = [l for l in difflib.unified_diff(t0.splitlines(), back.splitlines(), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
        n = sum(1 for a, b in zip(t0.splitlines(), t1.splitlines()) if a != b); say(not dl, "after mapping the version words and the class reading back, %d differing lines remain %s; %d lines differ in all" % (len(dl), dl[:4], n))
    def strip(o): return o.replace("1.1.0", "1.0.0").replace("1_1_0", "1_0_0")
    if k[0] == "same567":
        res = {}
        for ch in ("05", "06", "07"):
            c0, o0 = run(V0, ch); c1, o1 = run(V1, ch); res[ch] = (c0 == c1 and strip(o1) == o0, c0, c1, len(o0.splitlines()))
        say(all(v[0] for v in res.values()), "chapter: (same lines and exit code, exit v1_0_0, exit v1_1_0, lines) %s" % res)
    if k[0] in ("measured", "counts"):
        out = {}
        for ch in RAW:
            c1, o1 = run(V1, ch); c0, o0 = run(V0, ch); out[ch] = (o0, o1)
        if k[0] == "measured":
            res = {}
            for ch, (o0, o1) in out.items():
                d4 = [l for l in o1.splitlines() if l.startswith("D4 ")]; d11 = [l for l in o1.splitlines() if l.startswith("D11 ")]; z4 = [l for l in o0.splitlines() if l.startswith("D4 ")]; z11 = [l for l in o0.splitlines() if l.startswith("D11 ")]
                res[ch] = (bool(d4 and d11 and d4[0].split()[1] in ("PASS", "FAIL") and d11[0].split()[1] in ("PASS", "FAIL") and z4 and z11 and "NOT_MEASURED" in z4[0] and "NOT_MEASURED" in z11[0]), d4[0].split()[1] if d4 else None, d11[0].split()[1] if d11 else None)
            say(all(v[0] for v in res.values()), "chapter: (v1_1_0 measured and v1_0_0 NOT_MEASURED, D4, D11) %s" % res)
        import rdflib
        res = {}; ok = True
        for ch in RAW:
            f = sorted(glob.glob(os.path.join(R, "03-materials", "ch" + ch, "rdodi", "sen0401_ch%s_research_v*.ttl" % ch)), key=ver)[-1]; g = rdflib.Graph(); g.parse(f, format="turtle")
            subs = [s for s, o in g.subject_objects(rdflib.RDF.type) if str(o).endswith("#PrimarySourceConcept") or str(o).endswith("/PrimarySourceConcept")]
            labs = [str(g.value(s, rdflib.RDFS.label)) for s in subs if g.value(s, rdflib.RDFS.label) is not None]; dd = len({norm(l) for l in labs})
            m = re.search(r"of (\d+) key concepts", [l for l in out[ch][1].splitlines() if l.startswith("D4 ")][0]); pr = int(m.group(1)) if m else -1
            res[ch] = (len(subs), RAW[ch], dd, pr); ok &= len(subs) == RAW[ch] and dd == pr
        say(ok, "chapter: (declarations counted by rdflib, wanted, de-duplicated by the builder, printed by v1_1_0 in D4) %s" % res)
    raise SystemExit(__doc__)
main()
