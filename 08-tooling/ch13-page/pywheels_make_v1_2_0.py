#!/usr/bin/env python3
"""pywheels_make v1_2_0 (SEN0401 chapter 13 page 9.81.0 or above). The chapter library wheel 03-materials/ch13/assets/sen0401_ch13_lib-1.1.0-py3-none-any.whl was committed earlier and is NOT rewritten here:
it is verified (its SHA-256 equals the chapter-code manifest's, its modules equal the library files of 08-tooling, byte for byte). Writes pywheels_v1_2_0.json only: the wheel with its SHA-256 and the boot snippet,
which first registers a pure-Python PBKDF2-HMAC where the runtime lacks it (Pyodide 0.28.2: the preflight of example 17 failed without it), then runs the setup of the deck's chapter-code manifest (read from the newest manifest, not typed here) and makes its names (L, R, hashlib) ready in every program. The boot snippet is executed here with the wheel's files on the path before anything is written."""
__version__ = "1.2.0"
import glob, hashlib, json, os, re, shutil, sys, tempfile, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
WH = "sen0401_ch13_lib-1.1.0-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch13", "assets")
mf = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch13", "page", "chapter_code_ch13_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", p)[0]])[-1]
man = json.load(open(mf)); setup = man["setup"]["code"]
sha = hashlib.sha256(open(os.path.join(AS, WH), "rb").read()).hexdigest()
assert sha == man["library"]["sha256"], "the wheel differs from the manifest's hash"
assert man["library"]["file"].endswith(WH)
with zipfile.ZipFile(os.path.join(AS, WH)) as z:
    for _m in ("sen0401_ch13_lib_v1_0_0.py", "sen0401_ch10_p2p_v1_0_0.py"):
        assert z.read(_m) == open(os.path.join(T, _m), "rb").read(), "the wheel's module %s differs from the library file" % _m
    tmp = tempfile.mkdtemp(prefix="pywheels_ch13_"); z.extractall(tmp)
PBK = (
    "import hashlib, hmac, struct\n"
    "# PBKDF2-HMAC in pure Python, registered only where the runtime lacks it (Pyodide 0.28.2 has no hashlib.pbkdf2_hmac; the library's bip39_seed calls it)\n"
    "def _pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None):\n"
    "    password = bytes(password); salt = bytes(salt); base = hmac.new(password, digestmod=hash_name); size = base.digest_size\n"
    "    dklen = size if dklen is None else dklen; out = b''; block = 1\n"
    "    while len(out) < dklen:\n"
    "        c = base.copy(); c.update(salt + struct.pack('>I', block)); u = c.digest(); acc = int.from_bytes(u, 'big')\n"
    "        for _ in range(iterations - 1):\n"
    "            c = base.copy(); c.update(u); u = c.digest(); acc ^= int.from_bytes(u, 'big')\n"
    "        out += acc.to_bytes(size, 'big'); block += 1\n"
    "    return out[:dklen]\n"
    "if not hasattr(hashlib, 'pbkdf2_hmac'): hashlib.pbkdf2_hmac = _pbkdf2_hmac\n")
boot = "import builtins\n" + PBK + setup + "\nfor _n in [k for k in list(globals()) if not k.startswith('_') and k != 'builtins']: setattr(builtins, _n, globals()[_n])\n"
sys.path.insert(0, tmp); ns = {}; exec(boot, ns); shutil.rmtree(tmp, ignore_errors=True)
json.dump({"_version": "1.2.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the chapter 13 library and the protocol module (standard library only) and, in the folder ch13-evidence beside them, the 36 saved files the worked examples read, as committed earlier. The boot snippet runs the setup of the deck's chapter-code manifest %s once (L = the library, R = the recorded run of Bitcoin Core 31.1, seen = the search of a saved source, hashlib, math) and makes those names ready in every program." % os.path.basename(mf)},
          open(os.path.join(H, "pywheels_v1_2_0.json"), "w"), indent=1)
print("wheel", WH, sha[:16], os.path.getsize(os.path.join(AS, WH)), "bytes verified; manifest", os.path.basename(mf))
