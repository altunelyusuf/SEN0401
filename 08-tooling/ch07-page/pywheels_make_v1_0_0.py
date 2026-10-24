#!/usr/bin/env python3
"""pywheels_make v1_0_0 (SEN0401 chapter 7 page 9.84.0). Writes (1) the wheel 03-materials/ch07/assets/sen0401_ch07_lib-1.0.0-py3-none-any.whl: the two modules of the chapter library
named by the deck's chapter-code manifest (sen0401_ch07_script_lib_v1_0_0.py and sen0401_ch07_deck_lib_v1_0_0.py, copied byte for byte, hashes checked against the manifest; they import hashlib,
hmac and struct only, so they run in the page's Pyodide as they are); the zip entries carry a fixed date; (2) pywheels_v1_0_0.json: the wheel with its SHA-256 and the boot snippet, which runs the
setup code of the manifest once and makes every name it imports (L, K and the helpers) ready in every program. The setup code is read from the newest chapter-code manifest, not typed here.
The boot snippet is executed here, in a scratch folder that holds ONLY the two modules, under the browser's Python (python3.13 by default; the page's Pyodide is CPython 3.13.2).
Usage: pywheels_make_v1_0_0.py [PYTHON_FOR_THE_BROWSER_VERSION]"""
__version__ = "1.0.0"
import ast, base64, glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
PYB = sys.argv[1] if len(sys.argv) > 1 else "/root/.local/bin/python3.13"
WH = "sen0401_ch07_lib-1.0.0-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch07", "assets")
mf = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch07", "page", "chapter_code_ch07_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", p)[0]])[-1]
man = json.load(open(mf)); setup = man["setup"]["code"]
mods = [man["library"]] + man["library"]["data_files"]
files = {}
for m in mods:
    b = open(os.path.join(REPO, m["file"]), "rb").read()
    assert hashlib.sha256(b).hexdigest() == m["sha256"], "hash mismatch " + m["file"]
    files[os.path.basename(m["file"])] = b
def entry(z, name, data):
    zi = zipfile.ZipInfo(name, (2026, 10, 24, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, data)
files["sen0401_ch07_lib-1.0.0.dist-info/METADATA"] = b"Metadata-Version: 2.1\nName: sen0401-ch07-lib\nVersion: 1.0.0\nSummary: The chapter 7 (Authorization and Authentication) library of the SEN0401 course: the Script interpreter and the worked-example helpers (standard library only).\n"
files["sen0401_ch07_lib-1.0.0.dist-info/WHEEL"] = b"Wheel-Version: 1.0\nGenerator: pywheels_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
rec = []; path = os.path.join(AS, WH)
with zipfile.ZipFile(path, "w") as z:
    for n, b in files.items():
        entry(z, n, b); rec.append("%s,sha256=%s,%d" % (n, base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode(), len(b)))
    entry(z, "sen0401_ch07_lib-1.0.0.dist-info/RECORD", ("\n".join(rec) + "\nsen0401_ch07_lib-1.0.0.dist-info/RECORD,,\n").encode())
sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
names = []
for nd in ast.parse(setup).body:
    if isinstance(nd, ast.Import): names += [a.asname or a.name.split(".")[0] for a in nd.names]
    if isinstance(nd, ast.ImportFrom): names += [a.asname or a.name for a in nd.names]
names = [n for n in dict.fromkeys(names) if not n.startswith("sen0401")]
boot = "import builtins\n" + setup + "\nfor _n in %r: setattr(builtins, _n, globals()[_n])\n" % (tuple(names),)
sd = tempfile.mkdtemp(prefix="sen0401_wheel_boot_")
try:
    for n, b in files.items():
        if n.endswith(".py"): open(os.path.join(sd, n), "wb").write(b)
    open(os.path.join(sd, "boot_check.py"), "w").write(boot + "import builtins\nprint(sorted(n for n in %r if hasattr(builtins, n)))\n" % (tuple(names),))
    r = subprocess.run([PYB, "-I", "-c", "import sys; sys.path.insert(0, %r); exec(open(%r).read())" % (sd, os.path.join(sd, "boot_check.py"))], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    print("boot snippet ran under", subprocess.run([PYB, "--version"], capture_output=True, text=True).stdout.strip(), "->", r.stdout.strip())
finally:
    shutil.rmtree(sd)
json.dump({"_version": "1.0.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the two modules of the chapter 7 library (standard library only), copied unchanged from 08-tooling and checked against the hashes of the deck's chapter-code manifest %s. The boot snippet runs the manifest's setup once and makes L, K and the helper names ready in every program." % os.path.basename(mf)},
          open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
print("wheel", WH, sha[:16], os.path.getsize(path), "bytes; manifest", os.path.basename(mf))
