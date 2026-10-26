#!/usr/bin/env python3
"""pywheels_make v1_1_0 (SEN0401 chapter 11 page 9.79.0 or above). The chapter library wheel 03-materials/ch11/assets/sen0401_ch11_lib-1.0.0-py3-none-any.whl was committed earlier and is NOT rewritten here:
it is verified (its SHA-256 equals the chapter-code manifest's, its modules equal the library files of 08-tooling, byte for byte). Writes pywheels_v1_1_0.json only: the wheel with its SHA-256 and the boot snippet,
which runs the setup of the deck's chapter-code manifest (read from the newest manifest, not typed here) and makes its names (L, R, hashlib) ready in every program. The boot snippet is executed here with the wheel's files on the path before anything is written."""
__version__ = "1.1.0"
import glob, hashlib, json, os, re, shutil, sys, tempfile, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
WH = "sen0401_ch11_lib-1.0.0-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch11", "assets")
mf = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch11", "page", "chapter_code_ch11_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", p)[0]])[-1]
man = json.load(open(mf)); setup = man["setup"]["code"]
sha = hashlib.sha256(open(os.path.join(AS, WH), "rb").read()).hexdigest()
assert sha == man["library"]["sha256"], "the wheel differs from the manifest's hash"
assert man["library"]["file"].endswith(WH)
with zipfile.ZipFile(os.path.join(AS, WH)) as z:
    for _m in ("sen0401_ch11_lib_v1_0_0.py", "sen0401_ch10_p2p_v1_0_0.py"):
        assert z.read(_m) == open(os.path.join(T, _m), "rb").read(), "the wheel's module %s differs from the library file" % _m
    tmp = tempfile.mkdtemp(prefix="pywheels_ch11_"); z.extractall(tmp)
boot = "import builtins\n" + setup + "\nfor _n in [k for k in list(globals()) if not k.startswith('_') and k != 'builtins']: setattr(builtins, _n, globals()[_n])\n"
sys.path.insert(0, tmp); ns = {}; exec(boot, ns); shutil.rmtree(tmp, ignore_errors=True)
json.dump({"_version": "1.1.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the chapter 11 library and the protocol module (standard library only) and, in the folder ch11-evidence beside them, the saved files the worked examples read, as committed earlier. The boot snippet runs the setup of the deck's chapter-code manifest %s once (L = the library, R = the recorded run of Bitcoin Core 31.1, hashlib) and makes those names ready in every program." % os.path.basename(mf)},
          open(os.path.join(H, "pywheels_v1_1_0.json"), "w"), indent=1)
print("wheel", WH, sha[:16], os.path.getsize(os.path.join(AS, WH)), "bytes verified; manifest", os.path.basename(mf))
