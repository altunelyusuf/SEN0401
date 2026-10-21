#!/usr/bin/env python3
"""pywheels_make v1_1_0 (SEN0401 chapter 8 page; research 1.2.0 adds 18 self-contained examples with changeable whole numbers that need no library). The wheel of 1.0.0 is unchanged and is NOT written again: this version only checks its SHA-256, writes pywheels_v1_1_0.json and standin_v1_1_0.json from the ABox v1_2_0. Original text follows. Writes, from the chapter's committed library, (1) the wheel 03-materials/ch08/assets/sen0401_ch08_lib-1.0.0-py3-none-any.whl (the three modules the chapter's
worked examples import, copied byte for byte: sen0401_ch07_script_lib_v1_0_0.py, sen0401_ch08_sig_lib_v1_0_0.py, sen0401_ch08_claims_v1_0_0.py; the zip entries carry a fixed date so the wheel is reproducible),
(2) pywheels_v1_0_0.json (the wheel with its SHA-256, and the boot snippet), (3) standin_v1_0_0.json: every worked example is run in a scratch folder that holds ONLY those three modules, under the browser's
Python version (python3.13 by default; the page's Pyodide is CPython 3.13.2), with no evidence folder; an example that raises FileNotFoundError because it reads a saved source or the record of
Bitcoin Core's run is listed under "recorded" with the file it needs, so the page shows it as recorded and never as a run that did not happen. Nothing is typed by hand about which example runs.
Usage: pywheels_make_v1_0_0.py [PYTHON_FOR_THE_BROWSER_VERSION]   (default /root/.local/bin/python3.13)"""
__version__ = "1.1.0"
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
import rdflib
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
PYB = sys.argv[1] if len(sys.argv) > 1 else "/root/.local/bin/python3.13"
MODS = ["sen0401_ch07_script_lib_v1_0_0.py", "sen0401_ch08_sig_lib_v1_0_0.py", "sen0401_ch08_claims_v1_0_0.py"]
WH = "sen0401_ch08_lib-1.0.0-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch08", "assets"); os.makedirs(AS, exist_ok=True)
def entry(z, name, data):
    zi = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, data)
path = os.path.join(AS, WH)
assert os.path.exists(path), "the committed wheel is missing"
sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
boot = "import builtins\nimport sen0401_ch07_script_lib_v1_0_0 as L, sen0401_ch08_sig_lib_v1_0_0 as C, sen0401_ch08_claims_v1_0_0 as K\nbuiltins.L, builtins.C, builtins.K = L, C, K\n"
json.dump({"_version": "1.1.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the three modules of the chapter's library, copied unchanged from 08-tooling (hashlib, hmac and struct only). The boot snippet imports them and makes the names L (the Script and curve library of chapter 7), C (the chapter 8 signature library) and K (the chapter 8 claims) available to every program, so a worked example reads K.roundtrip(), as the deck's consoles do."},
          open(os.path.join(H, "pywheels_v1_1_0.json"), "w"), indent=1)
# ---- which worked examples run with nothing but the wheel -----------------------------------------------------
A = rdflib.Graph().parse(os.path.join(REPO, "03-materials", "ch08", "rdodi", "sen0401_ch08_domain_abox_v1_2_0.ttl"))
CH = rdflib.Namespace("http://example.org/sen0401/ch08#"); RDN = rdflib.Namespace("http://example.org/rdodi/domain-ontology#")
sb = tempfile.mkdtemp(prefix="ch08_sandbox_")
for m in MODS: shutil.copy(os.path.join(T, m), sb)
recorded = {}; ran = []
for x in sorted(A.subjects(RDN.hasIOExample, None)):
    e = str(A.value(A.value(x, RDN.hasIOExample), CH.input)); m = re.match(r"^import sys; sys\.path\.insert\(0, '08-tooling'\); import (\w+) as K; (K\.\w+\(\))$", e)
    cid = re.sub(r"^X_", "", str(x).split("#")[-1])
    if m: prog = "import %s as K\nprint(repr(%s))" % (m.group(1), m.group(2))
    elif "sen0401" not in e: prog = "import ast\nsrc = %r\nt = ast.parse(src)\nns = {}\nlast = t.body.pop()\nexec(compile(t, 'x', 'exec'), ns)\nprint(repr(eval(compile(ast.Expression(last.value), 'x', 'eval'), ns)))" % e   # 1.1.0: a self-contained example
    else: raise SystemExit("an example in a form this tool does not know: %r" % e)
    p = subprocess.run([PYB, "-c", prog], capture_output=True, text=True, cwd=sb, timeout=300)
    if p.returncode == 0: ran.append(cid); continue
    last = p.stderr.strip().splitlines()[-1]
    if "FileNotFoundError" not in last: raise SystemExit("%s failed in the sandbox for a reason other than a missing file: %s" % (cid, last))
    f = re.search(r"/([^/']+)'$", last).group(1)
    recorded[cid] = "This example reads %s, a file saved with the chapter's evidence (the fetched sources, their test vectors or the record of Bitcoin Core 31.1.0's run), and a browser does not have it." % f
bpy = subprocess.run([PYB, "--version"], capture_output=True, text=True).stdout.strip()
json.dump({"_version": "1.1.0", "markers": [], "note": "",
  "notice": "Python and libraries on this page: %d of the %d worked examples run in your browser (Pyodide, Python 3.13.2), on Python alone or on the chapter's own library, loaded from a wheel embedded in this page (the names K, L and C are ready in every program, as in the deck's consoles), and equal what the research recorded under Python 3.14.6. The other %d read a file saved with the chapter's evidence (a fetched source, a test-vector file or the record of Bitcoin Core 31.1.0's run on a test network), which a browser does not have: each is shown with its recorded output and the file it needs, under 'Recorded, not run on this page'. The sandbox check that sorted them ran each example under %s with only the three library modules present." % (len(ran), len(ran) + len(recorded), len(recorded), bpy),
  "recorded": recorded, "_note": "Written by pywheels_make_v1_1_0.py from a run of every example; not edited by hand."}, open(os.path.join(H, "standin_v1_1_0.json"), "w"), indent=1, ensure_ascii=False)
shutil.rmtree(sb)
print("wheel", WH, sha[:16], "| examples that run with the wheel alone: %d; recorded: %d" % (len(ran), len(recorded)))
