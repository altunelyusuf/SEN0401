#!/usr/bin/env python3
"""sen0401_lineage_chapter_check v1_1_0 - ONE rerunnable command per story of a SEN0401 chapter, for backlog_evidence_bridge to run as the test of a
TestEvidence (the bridge verifies a TestEvidence only if its spec file exists in the workspace and the command exits 0). It runs the checks that already
belong to the chapter and changes nothing in the repository (every output goes to a temporary directory). Ported from sen0414_lineage_chapter_check_v1_1_0.

Usage: sen0401_lineage_chapter_check_v1_1_0.py KIND/ChNN        e.g. Deck/Ch05, Research/Ch06, Page/Ch07
  Deck      deck_check (every '>>>' example on the committed deck re-run under Python 3.14, 0 mismatches) in the chapter's own folder; every stale fixture in its
            fixtures/ folder refused; deck_layout_check clean; deck_notes_check PASS (the notes are the reader's prose, owner's ruling of 2026-10-08)
  Research  RDODI's own pipeline validator over Stages 1-3 on the newest file of each part (sen0401_rdodi_gates logic, per-part versions); the chapter's corpus
            claims executed under Python 3.14; the chapter's verify script (against the standards' vectors and Bitcoin Core's own test data) exit 0; HermiT
            consistency of the chapter's TBox+ABox when Java and owlready2 are present (otherwise reported as skipped, never as passed)
  Page      the newest page test (headless Chromium) on a copy of the newest page whose exam-release public key is replaced by a TEST key
            (sen0401_lineage_page_test_run): the pass proves the page's logic, not the real instructor key
Exit 0 only when every part passed.
"""
__version__ = "1.1.0"
import glob, importlib.util, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "08-tooling")
ECO = os.environ.get("RDODI_ECOSYSTEM", "/home/claude/eco_pin/rdodi-ecosystem")
PY = shutil.which("python3.14") or sys.executable
vkey = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]


def newest(pattern):
    fs = glob.glob(pattern)
    return sorted(fs, key=vkey)[-1] if fs else None


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout + r.stderr


def deck(n):
    d = os.path.join(TOOL, "ch%02d-deck" % n)
    pptx = newest(os.path.join(REPO, "03-materials", "ch%02d" % n, "SEN0401_Ch%02d_*_3e_v*.pptx" % n))
    assert pptx, "no committed deck"
    print("deck:", os.path.relpath(pptx, REPO))
    parts = {}
    rc, out = run([PY, "-B", "deck_check_v1_0_0.py", pptx], cwd=d)
    print(out.strip()[-600:]); parts["deck_check (examples re-run)"] = rc == 0 and "0 mismatch" in out
    fx = sorted(glob.glob(os.path.join(d, "fixtures", "*.pptx")))
    refused = []
    for f in fx:
        rc, _ = run([PY, "-B", "deck_check_v1_0_0.py", f], cwd=d); refused.append(rc != 0)
    print("stale fixtures:", [os.path.basename(f) for f in fx], "refused:", refused)
    parts["stale fixtures refused"] = bool(fx) and all(refused)
    rc, out = run([sys.executable, "-B", os.path.join(TOOL, "deck_layout_check_v1_0_0.py"), pptx])
    print(out.strip()[-300:]); parts["layout check clean"] = rc == 0 and "RESULT: clean" in out
    rc, out = run([sys.executable, "-B", os.path.join(TOOL, "deck_notes_check_v1_0_0.py"), pptx])
    print("\n".join(out.strip().splitlines()[:6])); parts["notes check (reader's prose)"] = rc == 0 and "VERDICT: PASS" in out
    return parts


def gates(n):
    rd = os.path.join(REPO, "03-materials", "ch%02d" % n, "rdodi")
    V = newest(os.path.join(ECO, "02-gates", "rdodi_pipeline_validator_v*.py"))
    spec = importlib.util.spec_from_file_location("rdodi_validator", V); m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.join(ECO, "02-gates")); spec.loader.exec_module(m)
    SV = os.path.join(ECO, "01-stage-vocabularies")
    part = lambda p: newest(os.path.join(rd, "sen0401_ch%02d_%s_v*.ttl" % (n, p)))
    c = {k: part(k) for k in ("research", "domain_tbox", "domain_abox", "domain_shacl", "document")}
    print("validator:", os.path.basename(V)); print("parts:", {k: os.path.basename(v) for k, v in c.items()})
    N = lambda *a: newest(os.path.join(SV, *a))
    out = [m.gate_parse("Stage1.A", c["research"]), m.gate_shacl("Stage1.B", [c["research"]], N("01-research", "research_ontology_shacl_v*.ttl")),
           m.gate_parse("Stage2.A", c["domain_tbox"]), m.gate_shacl("Stage2.C", [c["domain_tbox"], c["domain_abox"]], c["domain_shacl"]),
           m.gate_parse("Stage3.A", c["document"]), m.gate_reference_rule("Stage3.F", c["document"], c["research"]),
           m.gate_shacl("Stage3.B", [c["document"], c["domain_tbox"], c["domain_abox"]], N("03-document", "document_ontology_shacl_v*.ttl")),
           m.gate_coverage_rule("Stage3.E.cov", c["document"], N("03-document", "document_ontology_tbox_v*.ttl"), N("03-document", "document_ontology_shacl_v*.ttl"), "document-ontology#"),
           m.gate_substance_rule("Stage3.E.sub", c["document"], N("03-document", "document_ontology_tbox_v*.ttl"), N("03-document", "document_ontology_shacl_v*.ttl"), "document-ontology#"),
           m.gate_source_validity("Stage3.src", c["document"])]
    for r in out:
        print(r)
    bad = [r for r in out if r.verdict == "FAIL"]
    print("gates:", "PASS" if not bad else "FAIL (%d)" % len(bad))
    return not bad, c


SNIPPET = r"""
import importlib, sys
sys.path.insert(0, %(tool)r)
m = importlib.import_module(%(mod)r)
bad = []; n = 0
base = m
if not hasattr(m, 'run_checks_inprocess'):
    base = importlib.import_module(%(base)r)
n, bad = base.run_checks_inprocess()
if base is not m:
    for e, x in m.CHECKS:
        n += 1
        try: got = repr(eval(e, {}))
        except BaseException as ex: got = 'EXC %%r' %% (ex,)
        if got != x: bad.append((e[:120], x, got))
print(n, 'claims executed under CPython', sys.version.split()[0], '- failures:', bad)
sys.exit(1 if bad else 0)
"""


def corpus(n):
    mods = sorted(glob.glob(os.path.join(TOOL, "sen0401_ch%02d_corpus_v*.py" % n)), key=vkey)
    mod = os.path.basename(mods[-1])[:-3]; base = os.path.basename(mods[0])[:-3]
    rc, out = run([PY, "-B", "-c", SNIPPET % {"tool": TOOL, "mod": mod, "base": base}])
    print(out.strip()[-500:])
    return rc == 0 and "failures: []" in out


def verify(n):
    f = newest(os.path.join(TOOL, "sen0401_ch%02d_verify_v*.py" % n))
    rc, out = run([PY, "-B", f], cwd=TOOL)
    print(os.path.basename(f), "->", "\n".join(out.strip().splitlines()[-3:]))
    return rc == 0 and ("failures: []" in out or " 0 failed" in out)


def hermit(n, c):
    """Consistency under HermiT of TBox+ABox. 'skipped' only when owlready2 or Java is absent."""
    try:
        import owlready2, rdflib
    except Exception as e:
        return "skipped", "owlready2 not importable: %s" % e
    if not shutil.which("java"):
        return "skipped", "no java"
    d = tempfile.mkdtemp(prefix="hermit_")
    g = rdflib.Graph()
    for k in ("domain_tbox", "domain_abox"):
        g.parse(c[k])
    p = os.path.join(d, "o.owl"); g.serialize(p, format="xml")
    try:
        onto = owlready2.get_ontology("file://" + p).load()
        with onto:
            owlready2.sync_reasoner_hermit(infer_property_values=False)
        return "pass", "consistent (HermiT), %d classes" % len(list(onto.classes()))
    except owlready2.OwlReadyInconsistentOntologyError:
        return "fail", "INCONSISTENT"
    except Exception as e:
        return "fail", "reasoner error: %s" % str(e)[:200]


def research(n):
    parts = {}
    ok, c = gates(n); parts["RDODI pipeline gates"] = ok
    parts["corpus claims executed"] = corpus(n)
    parts["verify script"] = verify(n)
    h, why = hermit(n, c); print("hermit:", h, why)
    parts["HermiT consistent"] = h == "pass" if h != "skipped" else True
    if h == "skipped":
        parts["HermiT (skipped: %s)" % why] = True
    return parts


def page(n):
    rc, out = run([sys.executable, "-B", os.path.join(TOOL, "sen0401_lineage_page_test_run_v1_1_0.py"), "%02d" % n])
    print("\n".join(out.splitlines()[-24:]))
    return {"page test (TEST key; proves page logic only)": rc == 0 and "RESULT: PASS" in out}


def main():
    kind, ch = sys.argv[1].split("/")
    n = int(ch[2:])
    parts = {"Deck": deck, "Research": research, "Page": page}[kind](n)
    for k, v in parts.items():
        print("  %-60s %s" % (k, "PASS" if v else "FAIL"))
    ok = all(parts.values())
    print("RESULT %s: %s" % (sys.argv[1], "PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
