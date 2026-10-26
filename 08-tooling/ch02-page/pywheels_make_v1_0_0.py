#!/usr/bin/env python3
"""pywheels_make v1_0_0 (SEN0401 chapter 2 page 9.72.0). Writes (1) the wheel 03-materials/ch02/assets/sen0401_ch02_lib-1.0.0-py3-none-any.whl: the chapter library
sen0401_ch02_tx_lib_v1_0_0.py copied byte for byte (hashlib, math, struct and urllib.parse only, so it runs in the page's Pyodide as it is); the zip entries carry a fixed date;
(2) pywheels_v1_0_0.json: the wheel with its SHA-256 and the boot snippet, which runs the setup of the deck's chapter-code manifest (read from the newest manifest, not typed here)
and makes its names (hashlib, urllib, T) ready in every program. The boot snippet is executed here with the library on the path before anything is written."""
__version__ = "1.0.0"
import base64, glob, hashlib, json, os, re, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
LIB = "sen0401_ch02_tx_lib_v1_0_0.py"; WH = "sen0401_ch02_lib-1.0.0-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch02", "assets")
mf = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch02", "page", "chapter_code_ch02_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", p)[0]])[-1]
man = json.load(open(mf)); setup = man["setup"]["code"]
assert man["library"]["module"] == "sen0401_ch02_tx_lib_v1_0_0"
assert hashlib.sha256(open(os.path.join(T, LIB), "rb").read()).hexdigest() == man["library"]["sha256"], "the library differs from the manifest's hash"
def entry(z, name, data):
    zi = zipfile.ZipInfo(name, (2026, 10, 26, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, data)
rec = []; path = os.path.join(AS, WH)
with zipfile.ZipFile(path, "w") as z:
    fl = {LIB: open(os.path.join(T, LIB), "rb").read(),
          "sen0401_ch02_lib-1.0.0.dist-info/METADATA": b"Metadata-Version: 2.1\nName: sen0401-ch02-lib\nVersion: 1.0.0\nSummary: The chapter 2 (How Bitcoin Works) library of the SEN0401 course (standard library only).\n",
          "sen0401_ch02_lib-1.0.0.dist-info/WHEEL": b"Wheel-Version: 1.0\nGenerator: pywheels_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"}
    for n, b in fl.items():
        entry(z, n, b); rec.append("%s,sha256=%s,%d" % (n, base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode(), len(b)))
    entry(z, "sen0401_ch02_lib-1.0.0.dist-info/RECORD", ("\n".join(rec) + "\nsen0401_ch02_lib-1.0.0.dist-info/RECORD,,\n").encode())
sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
boot = "import builtins\n" + setup + "\nfor _n in ('hashlib', 'urllib', 'T'): setattr(builtins, _n, globals()[_n])\n"
import sys
sys.path.insert(0, T); ns = {}; exec(boot, ns)
json.dump({"_version": "1.0.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the chapter 2 library (standard library only), copied unchanged from 08-tooling. The boot snippet runs the setup of the deck's chapter-code manifest %s once (hashlib, urllib.parse and T = the chapter 2 library) and makes those names ready in every program." % os.path.basename(mf)},
          open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
print("wheel", WH, sha[:16], os.path.getsize(path), "bytes; manifest", os.path.basename(mf))
