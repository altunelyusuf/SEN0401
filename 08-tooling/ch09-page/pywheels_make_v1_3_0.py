#!/usr/bin/env python3
"""pywheels_make v1_3_0 (SEN0401 chapter 9 page 9.82.0 or above). The chapter library wheel 03-materials/ch09/assets/sen0401_ch09_lib-1.0.2-py3-none-any.whl was committed earlier and is NOT rewritten here:
it is verified (its SHA-256 equals the chapter-code manifest's, its module equals the library file of 08-tooling, byte for byte). Writes pywheels_v1_3_0.json only: the wheel with its SHA-256 and the boot snippet,
which runs the setup of the deck's chapter-code manifest (read from the newest manifest, not typed here) and makes its names (L, R, R2, C, B) ready in every program. The boot snippet is executed here with the wheel's files on the path before anything is written."""
__version__ = "1.3.0"
import glob, hashlib, json, os, re, shutil, sys, tempfile, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
LIB = "sen0401_ch09_lib_v1_0_1.py"; WH = "sen0401_ch09_lib-1.0.2-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch09", "assets")
mf = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch09", "page", "chapter_code_ch09_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", p)[0]])[-1]
man = json.load(open(mf)); setup = man["setup"]["code"]
sha = hashlib.sha256(open(os.path.join(AS, WH), "rb").read()).hexdigest()
assert sha == man["library"]["sha256"], "the wheel differs from the manifest's hash"
assert man["library"]["file"].endswith(WH)
with zipfile.ZipFile(os.path.join(AS, WH)) as z:
    assert z.read(LIB) == open(os.path.join(T, LIB), "rb").read(), "the wheel's module differs from the library file"
    tmp = tempfile.mkdtemp(prefix="pywheels_ch09_"); z.extractall(tmp)
boot = "import builtins\n" + setup + "\nfor _n in [k for k in list(globals()) if not k.startswith('_') and k != 'builtins']: setattr(builtins, _n, globals()[_n])\n"
sys.path.insert(0, tmp); ns = {}; exec(boot, ns); shutil.rmtree(tmp, ignore_errors=True)
json.dump({"_version": "1.3.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the chapter 9 library (standard library only) and, in the folder ch09-evidence beside it, the saved files the worked examples read, as committed earlier. The boot snippet runs the setup of the deck's chapter-code manifest %s once (L = the library, R and R2 = the recorded runs of Bitcoin Core 31.1, C = the census of two blocks, B = its blocks) and makes those names ready in every program." % os.path.basename(mf)},
          open(os.path.join(H, "pywheels_v1_3_0.json"), "w"), indent=1)
print("wheel", WH, sha[:16], os.path.getsize(os.path.join(AS, WH)), "bytes verified; manifest", os.path.basename(mf))
