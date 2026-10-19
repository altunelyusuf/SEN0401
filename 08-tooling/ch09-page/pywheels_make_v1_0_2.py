#!/usr/bin/env python3
"""pywheels_make v1_0_2 (SEN0401 chapter 9 page). Writes, from the chapter's committed library and evidence, (1) the wheel 03-materials/ch09/assets/sen0401_ch09_lib-1.0.2-py3-none-any.whl: the chapter library and
library (sen0401_ch09_lib_v1_0_0.py, copied byte for byte) and, in a folder ch09-evidence beside them, the saved files the worked examples read AND whose terms clearly allow
redistribution (Bitcoin Core files, the BIPs, Mastering Bitcoin, Bitcoin Optech, the Bitcoin paper, and this course's own run record); academic papers, mailing-list posts, web pages and third-party service data are left
out and the examples that read them are recorded; the zip entries carry a fixed date; (2) pywheels_v1_0_2.json (the wheel with its SHA-256 and the boot snippet); (3) standin_v1_0_2.json: every worked example is run
in a scratch folder that holds ONLY what the wheel holds, under the browser's Python version (python3.13 by default); one that raises an error for a missing file is listed under "recorded". Nothing is typed by hand
about which example runs. Usage: pywheels_make_v1_0_2.py [PYTHON_FOR_THE_BROWSER_VERSION]   (default /root/.local/bin/python3.13)"""
__version__ = "1.0.2"
import base64, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
import rdflib
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling"); EV = os.path.join(T, "ch09-evidence")
PYB = sys.argv[1] if len(sys.argv) > 1 else "/root/.local/bin/python3.13"
LIB = "sen0401_ch09_lib_v1_0_1.py"; WH = "sen0401_ch09_lib-1.0.2-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch09", "assets"); os.makedirs(AS, exist_ok=True)
PRE = "import sys; sys.path.insert(0, '08-tooling'); import sen0401_ch09_lib_v1_0_0 as L; R = L.run(); R2 = L.run2(); C = L.census(); "
import glob
_ab = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch09", "rdodi", "sen0401_ch09_domain_abox_v*.ttl")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]   # the newest ABox (v1_0_2)
A = rdflib.Graph().parse(_ab)
CH = rdflib.Namespace("http://example.org/sen0401/ch09#"); RDN = rdflib.Namespace("http://example.org/rdodi/domain-ontology#")
ex = {}
for x in sorted(A.subjects(RDN.hasIOExample, None)):
    e = str(A.value(A.value(x, RDN.hasIOExample), CH.input))
    if not e.startswith(PRE): raise SystemExit("an example in a form this tool does not know: %r" % e[:120])
    ex[re.sub(r"^X_", "", str(x).split("#")[-1])] = e[len(PRE):]
# 1.0.2 (over the chapter 9 maker v1_0_0 that shipped in 2b43edc): only files whose terms clearly allow redistribution are shipped: Bitcoin Core files (MIT), the BIPs (each states an open licence), Mastering Bitcoin (CC BY-SA 4.0), Bitcoin Optech (CC BY 4.0), the Bitcoin paper
# (MIT, as on bitcoin.org) and this course's own run record. Academic papers, mailing-list posts, web pages and the data of third-party services (Bitnodes, Blockchain.com, mempool.space) have no clear terms and are left out:
# an example that reads one of them is shown as recorded.
OK_PREFIX = ("core_", "book_", "bip-", "bolt03_", "optech_", "nakamoto_2008_bitcoin", "regtest_run_", "regtest2_run_", "bitcoinwiki_", "mainnet_fee_census_")
# Withheld because they fall outside OK_PREFIX: Carlsten et al. 2016, Moeser and Boehme 2015, the Corallo post of 2018, and the mempool.space market files (mempool_blocks_fees_1y.json, mempool_fees_recommended.json).
# KEPT although it came from the mempool.space interface: mainnet_fee_census_v1_0_0.json (two mainnet blocks with their transactions: public chain data). The chapter library loads it at start (L.census()) in the first line of
# EVERY worked example, so without it no example could run at all; the licence question for it is open and is stated in the provenance file.
NOT_CLEAR = ("mainnet_fee_census_v1_0_0.json",)   # 1.0.2: the file fetched from mempool.space (no stated licence) is not shipped; the course's own census mainnet_fee_census_v2_0_0.json (CC BY 4.0) is
def clear(f): return f.startswith(OK_PREFIX) and f not in NOT_CLEAR
# which files do the examples open? Every example is run once in a folder that holds ALL the saved evidence, with open() logging the files it opens; nothing is guessed from the text of the examples.
T_ = tempfile.mkdtemp(prefix="ch09_trace_"); shutil.copy(os.path.join(T, LIB), T_); shutil.copytree(EV, os.path.join(T_, "ch09-evidence"))
LOG = os.path.join(T_, "opened.log")
trace = "import builtins, os\n_o = builtins.open\ndef _open(f, *a, **k):\n    if 'ch09-evidence' in str(f): _o(%r, 'a').write(os.path.basename(str(f)) + '\\n')\n    return _o(f, *a, **k)\nbuiltins.open = _open\n" % LOG
drv0 = "import sen0401_ch09_lib_v1_0_1 as L\nR = L.run(); R2 = L.run2(); C = L.census()\nG = {'L': L, 'R': R, 'R2': R2, 'C': C}\nimport sys, ast\nsrc = sys.stdin.read()\nt = ast.parse(src)\nlast = ast.Expression(t.body.pop().value)\nexec(compile(t, 'x', 'exec'), G)\nprint(repr(eval(compile(last, 'x', 'eval'), G)))\n"
for cid, body in sorted(ex.items()):
    p = subprocess.run([PYB, "-c", trace + drv0], input=body, capture_output=True, text=True, cwd=T_, timeout=300)
    if p.returncode != 0: raise SystemExit("%s fails even with all the evidence present: %s" % (cid, p.stderr.strip().splitlines()[-1]))
opened = sorted(set(open(LOG).read().split())); shutil.rmtree(T_)
withheld = [f for f in opened if not clear(f)]; ship = [f for f in opened if clear(f)]
def entry(z, name, data):
    zi = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, data)
rec = []; path = os.path.join(AS, WH)
with zipfile.ZipFile(path, "w") as z:
    fl = {LIB: open(os.path.join(T, LIB), "rb").read()}
    for f in ship: fl["ch09-evidence/" + f] = open(os.path.join(EV, f), "rb").read()
    fl["sen0401_ch09_lib-1.0.2.dist-info/METADATA"] = b"Metadata-Version: 2.1\nName: sen0401-ch09-lib\nVersion: 1.0.2\nSummary: The chapter 9 (Transaction Fees) library of the SEN0401 course with the saved files its worked examples read.\n"
    fl["sen0401_ch09_lib-1.0.2.dist-info/WHEEL"] = b"Wheel-Version: 1.0\nGenerator: pywheels_make_v1_0_2\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    for n, b in fl.items():
        entry(z, n, b); rec.append("%s,sha256=%s,%d" % (n, base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode(), len(b)))
    entry(z, "sen0401_ch09_lib-1.0.2.dist-info/RECORD", ("\n".join(rec) + "\nsen0401_ch09_lib-1.0.2.dist-info/RECORD,,\n").encode())
sha = hashlib.sha256(open(path, "rb").read()).hexdigest(); size = os.path.getsize(path)
boot = "import builtins\nimport sen0401_ch09_lib_v1_0_1 as L\nR = L.run(); R2 = L.run2(); C = L.census()\nbuiltins.L, builtins.R, builtins.R2, builtins.C = L, R, R2, C\n"
json.dump({"_version": "1.0.2", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the chapter library (standard library only) and, in the folder ch09-evidence beside it, the %d saved files the worked examples read, copied unchanged from 08-tooling/ch09-evidence. The boot snippet loads the two recorded runs of Bitcoin Core 31.1.0 once and makes L (the library), R and R2 (the runs) and C (the census) available to every program, as in the research record's examples." % len(ship)},
          open(os.path.join(H, "pywheels_v1_0_2.json"), "w"), indent=1)
# ---- which worked examples run with nothing but the wheel ------------------------------------------------------
sb = tempfile.mkdtemp(prefix="ch09_sandbox_"); shutil.copy(os.path.join(T, LIB), sb); os.makedirs(os.path.join(sb, "ch09-evidence"))
for f in ship: shutil.copy(os.path.join(EV, f), os.path.join(sb, "ch09-evidence", f))
drv = "import builtins, sen0401_ch09_lib_v1_0_1 as L\nR = L.run(); R2 = L.run2(); C = L.census()\nG = {'L': L, 'R': R, 'R2': R2, 'C': C}\nimport sys, ast\nsrc = sys.stdin.read()\nt = ast.parse(src)\nlast = ast.Expression(t.body.pop().value)\nexec(compile(t, 'x', 'exec'), G)\nprint(repr(eval(compile(last, 'x', 'eval'), G)))\n"
recorded = {}; ran = []; outs = {}
for cid, body in sorted(ex.items()):
    p = subprocess.run([PYB, "-c", drv], input=body, capture_output=True, text=True, cwd=sb, timeout=300)
    if p.returncode == 0: ran.append(cid); outs[cid] = p.stdout.strip(); continue
    last = p.stderr.strip().splitlines()[-1]
    if last.startswith("SyntaxError"):
        recorded[cid] = "The text of this example in the chapter's ontology is not valid Python (the research package wrote a double quote inside the code as a single quote: %s), so it cannot be run here; the research executed the original, and this is its recorded output." % last; continue
    if "FileNotFoundError" not in last: raise SystemExit("%s failed in the sandbox for a reason other than a missing file: %s" % (cid, last))
    f = re.search(r"/([^/']+)'$", last).group(1)
    recorded[cid] = "This example reads %s, a file saved with the chapter's evidence that the page does not carry, a file whose terms of redistribution are not clear and which the page therefore does not carry." % f
outA = {re.sub(r"^X_", "", str(x).split("#")[-1]): str(A.value(A.value(x, RDN.hasIOExample), CH.output)) for x in A.subjects(RDN.hasIOExample, None)}
diff = [c for c in ran if outs[c] != outA[c]]
print("sandbox output (Python 3.13) differs from the ontology's recorded output for %d of %d examples: %s" % (len(diff), len(ran), diff))
bpy = subprocess.run([PYB, "--version"], capture_output=True, text=True).stdout.strip()
json.dump({"_version": "1.0.2", "markers": [], "note": "",
  "notice": "Python and data on this page: %d of the %d worked examples run in your browser (Pyodide, Python 3.13.2) on the chapter's own library and on the saved files it reads, which travel inside this page in a wheel (%d files: the two recorded runs of Bitcoin Core 31.1.0 on a test network and the saved sources the examples quote); the names L, R, R2 and C are ready in every program (C is the course's own census of 20 mainnet blocks, CC BY 4.0, collected from mempool.space and blockstream.info and cross-checked). What such an example computes is the recorded run read back and measured again, not a new run of Bitcoin Core: a node was not started for this page. Each result equals what the research recorded under Python 3.14.6. %s" % (len(ran), len(ran) + len(recorded), len(ship), ("The other %d cannot run here (each reads a saved file whose terms of redistribution are not clear, so the page does not carry it): each is shown with its recorded output and the file it needs, under 'Recorded, not run on this page'." % len(recorded)) if recorded else "No example is left out."),
  "recorded": recorded, "_note": "Written by pywheels_make_v1_0_2.py from a run of every example under %s in a folder holding only the wheel's files; not edited by hand." % bpy}, open(os.path.join(H, "standin_v1_0_2.json"), "w"), indent=1, ensure_ascii=False)
shutil.rmtree(sb)
print("withheld (terms of redistribution not clear):", withheld)
print("wheel", WH, sha[:16], "%d bytes" % size, "| files shipped: %d | examples that run with the wheel alone: %d; recorded: %d" % (len(ship), len(ran), len(recorded)))
for k, v in recorded.items(): print("  recorded", k, v)
