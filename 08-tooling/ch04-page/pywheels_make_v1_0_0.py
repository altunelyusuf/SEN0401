#!/usr/bin/env python3
"""pywheels_make v1_0_0 (SEN0401 chapter 4 page 9.74.0). The chapter library wheel 03-materials/ch04/assets/sen0401_ch04_lib-1.0.0-py3-none-any.whl was committed with the deck 3.4.0 and is NOT rewritten here:
it is verified (its SHA-256 equals the chapter-code manifest's, its module equals the library file of 08-tooling, byte for byte). Writes pywheels_v1_0_0.json only: the wheel with its SHA-256 and the boot snippet,
which runs the setup of the deck's chapter-code manifest (read from the newest manifest, not typed here) and makes its names ready in every program. The boot snippet is executed here with the library on the path before anything is written."""
__version__ = "1.0.0"
import glob, hashlib, json, os, re, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
LIB = "sen0401_ch04_lib_v1_0_0.py"; WH = "sen0401_ch04_lib-1.0.0-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch04", "assets")
mf = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch04", "page", "chapter_code_ch04_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", p)[0]])[-1]
man = json.load(open(mf)); setup = man["setup"]["code"]
assert hashlib.sha256(open(os.path.join(T, LIB), "rb").read()).hexdigest() == man["library"]["source_sha256"], "the library differs from the manifest's hash"
sha = hashlib.sha256(open(os.path.join(AS, WH), "rb").read()).hexdigest()
assert sha == man["library"]["sha256"], "the wheel differs from the manifest's hash"
with zipfile.ZipFile(os.path.join(AS, WH)) as z: assert z.read(LIB) == open(os.path.join(T, LIB), "rb").read(), "the wheel's module differs from the library file"
boot = "import builtins\n" + setup + "\nfor _n in [k for k in list(globals()) if not k.startswith('_') and k != 'builtins']: setattr(builtins, _n, globals()[_n])\n"
import sys
sys.path.insert(0, T); ns = {}; exec(boot, ns)
json.dump({"_version": "1.0.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the chapter 4 library (standard library only, with a pure-Python RIPEMD-160), as committed with the deck 3.4.0. The boot snippet runs the setup of the deck's chapter-code manifest %s once (hashlib, math and K = the chapter 4 library) and makes those names ready in every program." % os.path.basename(mf)},
          open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
print("wheel", WH, sha[:16], os.path.getsize(os.path.join(AS, WH)), "bytes verified; manifest", os.path.basename(mf))
