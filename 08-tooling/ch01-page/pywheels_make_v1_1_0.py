#!/usr/bin/env python3
"""pywheels_make v1_1_0 (SEN0401 chapter 1 page 9.72.0). Over v1_0_0 (kept, unchanged): the page test 9.37.0 on the page 9.71.0 found that example 11 (stretch, hashlib.pbkdf2_hmac)
raises AttributeError in the page's Pyodide, whose hashlib has no pbkdf2_hmac. The chapter library, the manifest and the wheel stay byte for byte as they are; the boot snippet gets
a prefix that defines hashlib.pbkdf2_hmac in pure Python (hmac + hashlib) ONLY when hashlib lacks it, so the deck's code runs unchanged in the page. The shim is executed here and compared
with the real hashlib.pbkdf2_hmac before anything is written. Writes pywheels_v1_1_0.json only (the wheel of v1_0_0 is verified, not rewritten)."""
__version__ = "1.1.0"
import glob, hashlib, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
LIB = "sen0401_ch01_lib_v1_0_0.py"; WH = "sen0401_ch01_lib-1.0.0-py3-none-any.whl"; AS = os.path.join(REPO, "03-materials", "ch01", "assets")
mf = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch01", "page", "chapter_code_ch01_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", p)[0]])[-1]
man = json.load(open(mf)); setup = man["setup"]["code"]
assert hashlib.sha256(open(os.path.join(T, LIB), "rb").read()).hexdigest() == man["library"]["sha256"], "the library differs from the manifest's hash"
old = json.load(open(os.path.join(H, "pywheels_v1_0_0.json")))
sha = hashlib.sha256(open(os.path.join(AS, WH), "rb").read()).hexdigest()
assert old["wheels"] == [{"file": WH, "sha256": sha}], "the wheel differs from pywheels_v1_0_0.json"
SHIM = '''# shim: this page's Python (Pyodide) has no hashlib.pbkdf2_hmac; define it with hmac only when it is missing (same result as the real function)
import hashlib
if not hasattr(hashlib, 'pbkdf2_hmac'):
    def _pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None):
        import hmac, struct
        prf = hmac.new(bytes(password), digestmod=hash_name); size = prf.digest_size; dklen = dklen or size; dk = b''; i = 1
        while len(dk) < dklen:
            h = prf.copy(); h.update(bytes(salt) + struct.pack('>I', i)); u = h.digest(); r = int.from_bytes(u, 'big')
            for _ in range(iterations - 1):
                h = prf.copy(); h.update(u); u = h.digest(); r ^= int.from_bytes(u, 'big')
            dk += r.to_bytes(size, 'big'); i += 1
        return dk[:dklen]
    hashlib.pbkdf2_hmac = _pbkdf2_hmac
'''
# the shim, run on its own as if pbkdf2_hmac were missing, equals the real function
real = hashlib.pbkdf2_hmac; ns = {}
exec(SHIM.replace("if not hasattr(hashlib, 'pbkdf2_hmac'):", "if True:"), ns)
mine = hashlib.pbkdf2_hmac; hashlib.pbkdf2_hmac = real
for hn, pw, sl, it, dl in (("sha512", b"abc def", b"mnemonic", 1, None), ("sha512", b"abc def", b"mnemonic", 10, None), ("sha512", b"abc def", b"mnemonic", 2048, None), ("sha256", b"p", b"s", 3, 70)):
    assert mine(hn, pw, sl, it, dl) == real(hn, pw, sl, it, dl), (hn, it)
boot = "import builtins\n" + SHIM + setup + "\nfor _n in [k for k in list(globals()) if not k.startswith('_') and k != 'builtins']: setattr(builtins, _n, globals()[_n])\n"
import sys
sys.path.insert(0, T); ns = {}; exec(boot, ns)
json.dump({"_version": "1.1.0", "wheels": old["wheels"], "pyodide_packages": [], "boot_python": boot,
           "_note": "As pywheels_v1_0_0.json (same wheel, same manifest setup %s), plus a boot prefix that defines hashlib.pbkdf2_hmac in pure Python when the page's Pyodide lacks it (the page test 9.37.0 found example 11 failing without it)." % os.path.basename(mf)},
          open(os.path.join(H, "pywheels_v1_1_0.json"), "w"), indent=1)
print("pywheels_v1_1_0.json written; wheel", WH, sha[:16], "verified; shim equals hashlib.pbkdf2_hmac on 4 cases; manifest", os.path.basename(mf))
