#!/usr/bin/env python3
"""pywheels_make v1_0_0 (SEN0401 chapter 5 page, task TK_Remedy_Page_Ch05_Build).
Writes, from the chapter 5 library and the BIP39 word list (both copied byte for byte), (1) the wheel 03-materials/ch05/assets/sen0401_ch05_lib-1.1.0-py3-none-any.whl
(the library sen0401_ch05_wallet_lib_v1_1_0.py and, beside it, ch05-evidence/bip39_english.txt, the file wordlist() opens; the zip entries carry a fixed date) and
(2) pywheels_v1_0_0.json: the wheel with its SHA-256, and the boot snippet. The boot snippet is pure Python. It (a) registers a RIPEMD-160 and a PBKDF2-HMAC (built on hmac)
when the page's Pyodide 0.28.2 lacks them (RUNTIME_FACTS: hashlib.new('ripemd160') raises ValueError, hashlib.pbkdf2_hmac raises AttributeError), BEFORE the library is
imported, (b) imports the library and makes its public names, and the names of the deck's prelude (read from the newest chapter-code manifest), ready in every program
(builtins), exactly as the deck's examples were run (`from library import *`, then the prelude).
It then checks the wheel: the shims against the standard test vectors and against the native hashlib, and every example of the manifest, run in a scratch folder that holds
ONLY the wheel's files under the browser's Python (python3.13), with the native RIPEMD-160 and PBKDF2 switched off, against the manifest's expected result.
Usage: pywheels_make_v1_0_0.py [PYTHON_FOR_THE_BROWSER_VERSION]   (default /root/.local/bin/python3.13)"""
__version__ = "1.0.0"
import base64, glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling")
PYB = sys.argv[1] if len(sys.argv) > 1 else "/root/.local/bin/python3.13"
LIB = "sen0401_ch05_wallet_lib_v1_1_0"; WORDS = os.path.join(T, "ch05-evidence", "bip39_english.txt"); WH = "sen0401_ch05_lib-1.1.0-py3-none-any.whl"
AS = os.path.join(REPO, "03-materials", "ch05", "assets")
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
MAN = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch05", "page", "chapter_code_ch05_v*.json")), key=vk)[-1]
man = json.load(open(MAN))
want_sha = man["library"]["sha256"]; got_sha = hashlib.sha256(open(os.path.join(T, LIB + ".py"), "rb").read()).hexdigest()
if want_sha != got_sha: raise SystemExit("the library differs from the one the manifest was made with: %s vs %s" % (got_sha, want_sha))
if man["library"]["data_files"][0]["sha256"] != hashlib.sha256(open(WORDS, "rb").read()).hexdigest(): raise SystemExit("the word list differs from the manifest's")

SHIMS = r'''import builtins, hashlib, hmac, struct
# ---- RIPEMD-160 and PBKDF2-HMAC in pure Python, registered only where the runtime lacks them (Pyodide 0.28.2 has neither) ----
_M = 0xFFFFFFFF
_RL = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8, 3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12, 1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2, 4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13)
_RR = (5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12, 6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2, 15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13, 8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14, 12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11)
_SL = (11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8, 7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12, 11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5, 11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12, 9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6)
_SR = (8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6, 9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11, 9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5, 15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8, 8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11)
_KL = (0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E)
_KR = (0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000)
def _rol(x, n): return ((x << n) | (x >> (32 - n))) & _M
def _f(j, x, y, z):
    if j < 16: return x ^ y ^ z
    if j < 32: return (x & y) | (~x & _M & z)
    if j < 48: return (x | (~y & _M)) ^ z
    if j < 64: return (x & z) | (y & (~z & _M))
    return x ^ (y | (~z & _M))
def _r160_block(h, block):
    x = struct.unpack("<16I", block)
    al, bl, cl, dl, el = h; ar, br, cr, dr, er = h
    for j in range(80):
        t = (_rol((al + _f(j, bl, cl, dl) + x[_RL[j]] + _KL[j // 16]) & _M, _SL[j]) + el) & _M
        al, el, dl, cl, bl = el, dl, _rol(cl, 10), bl, t
        t = (_rol((ar + _f(79 - j, br, cr, dr) + x[_RR[j]] + _KR[j // 16]) & _M, _SR[j]) + er) & _M
        ar, er, dr, cr, br = er, dr, _rol(cr, 10), br, t
    t = (h[1] + cl + dr) & _M
    return [t, (h[2] + dl + er) & _M, (h[3] + el + ar) & _M, (h[4] + al + br) & _M, (h[0] + bl + cr) & _M]
class _RIPEMD160:
    name = "ripemd160"; digest_size = 20; block_size = 64
    def __init__(self, data=b""):
        self._h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]; self._buf = b""; self._len = 0
        if data: self.update(data)
    def update(self, data):
        data = bytes(data); self._len += len(data); b = self._buf + data
        n = len(b) - len(b) % 64
        for i in range(0, n, 64): self._h = _r160_block(self._h, b[i:i + 64])
        self._buf = b[n:]; return None
    def copy(self):
        c = _RIPEMD160(); c._h = list(self._h); c._buf = self._buf; c._len = self._len; return c
    def digest(self):
        c = self.copy(); pad = b"\x80" + b"\0" * ((55 - c._len) % 64) + struct.pack("<Q", (c._len * 8) & 0xFFFFFFFFFFFFFFFF)
        c.update(pad); return struct.pack("<5I", *c._h)
    def hexdigest(self): return self.digest().hex()
_native_new = hashlib.new
def _new(name, data=b"", **kw):
    if str(name).lower().replace("-", "") == "ripemd160": return _RIPEMD160(data)
    return _native_new(name, data, **kw)
try: _native_new("ripemd160", b"")
except Exception: hashlib.new = _new
def _pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None):
    password = bytes(password); salt = bytes(salt); base = hmac.new(password, digestmod=hash_name); size = base.digest_size
    dklen = size if dklen is None else dklen; out = b""; block = 1
    while len(out) < dklen:
        c = base.copy(); c.update(salt + struct.pack(">I", block)); u = c.digest(); acc = int.from_bytes(u, "big")
        for _ in range(iterations - 1):
            c = base.copy(); c.update(u); u = c.digest(); acc ^= int.from_bytes(u, "big")
        out += acc.to_bytes(size, "big"); block += 1
    return out[:dklen]
if not hasattr(hashlib, "pbkdf2_hmac"): hashlib.pbkdf2_hmac = _pbkdf2_hmac
# ---- the chapter library, imported after the two registrations; its public names are ready in every program, as in the deck's runs ----
import importlib
_lib = importlib.import_module("''' + LIB + r'''")
_ns = {k: v for k, v in vars(_lib).items() if not k.startswith("_")}
exec(PRELUDE_TEXT, _ns)
for _k, _v in _ns.items():
    if not _k.startswith("_") and not hasattr(builtins, _k): setattr(builtins, _k, _v)
'''
BOOT = SHIMS.replace("PRELUDE_TEXT", repr(man["prelude"]))

def entry(z, name, data):
    zi = zipfile.ZipInfo(name, (2026, 10, 23, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, data)
os.makedirs(AS, exist_ok=True); path = os.path.join(AS, WH); rec = []
with zipfile.ZipFile(path, "w") as z:
    fl = {LIB + ".py": open(os.path.join(T, LIB + ".py"), "rb").read(), "ch05-evidence/bip39_english.txt": open(WORDS, "rb").read(),
          "sen0401_ch05_lib-1.1.0.dist-info/METADATA": b"Metadata-Version: 2.1\nName: sen0401-ch05-lib\nVersion: 1.1.0\nSummary: The chapter 5 (Wallet Recovery) library of the SEN0401 course with the BIP39 English word list it reads.\n",
          "sen0401_ch05_lib-1.1.0.dist-info/WHEEL": b"Wheel-Version: 1.0\nGenerator: pywheels_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"}
    for n, b in fl.items():
        entry(z, n, b); rec.append("%s,sha256=%s,%d" % (n, base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode(), len(b)))
    entry(z, "sen0401_ch05_lib-1.1.0.dist-info/RECORD", ("\n".join(rec) + "\nsen0401_ch05_lib-1.1.0.dist-info/RECORD,,\n").encode())
sha = hashlib.sha256(open(path, "rb").read()).hexdigest(); size = os.path.getsize(path)
json.dump({"_version": "1.0.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": BOOT,
           "_note": "The wheel holds the chapter 5 library (standard library only) and, in the folder ch05-evidence beside it, the BIP39 English word list (2048 words) that wordlist() opens. The boot snippet is pure Python: it registers a RIPEMD-160 and a PBKDF2-HMAC (on hmac) where the runtime lacks them, imports the library, and makes the library's names and the deck's prelude names ready in every program. Made by pywheels_make_v1_0_0.py from the manifest %s." % os.path.basename(MAN)},
          open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)

# ---- checks, with the tools the page runs on: the standard vectors, then every example in a folder that holds only the wheel's files ----
sb = tempfile.mkdtemp(prefix="ch05_sandbox_")
with zipfile.ZipFile(path) as z: z.extractall(sb)
vec = r'''
import hashlib, hmac, os
%s
# RIPEMD-160 test vectors (Dobbertin, Bosselaers, Preneel 1996) and the native digest on random lengths
for msg, h in [(b"", "9c1185a5c5e9fc54612808977ee8f548b2258d31"), (b"a", "0bdc9d2d256b3ee9daae347be6f4dc835a467ffe"), (b"abc", "8eb208f7e05d987a9b044a8e98c6b087f15a0bfc"),
               (b"message digest", "5d0689ef49d2fae572b881b123a85ffa21595f36"), (b"a" * 1000000, "52783243c1697bdbe16d37f97f68f08325dc1528")]:
    assert hashlib.new("ripemd160", msg).hexdigest() == h, msg[:20]
for n in range(0, 300, 7):
    d = os.urandom(n); assert _RIPEMD160(d).digest() == _native_new("ripemd160", d).digest() if _have_native else True
# PBKDF2-HMAC-SHA512 against the vector of RFC 6070 style (SHA-1) and a BIP39 seed
assert hashlib.pbkdf2_hmac("sha1", b"password", b"salt", 2, 20).hex() == "ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957"
assert hashlib.pbkdf2_hmac("sha256", b"password", b"salt", 4096, 32).hex() == "c5e478d59288c841aa530db6845c4c8d962893a001ce4e11a4963873aa98134a"
seed = hashlib.pbkdf2_hmac("sha512", b"abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about", b"mnemonicTREZOR", 2048)
assert seed.hex().startswith("c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e5349553"), seed.hex()[:64]
print("shims ok")
''' % ("\n".join(l for l in BOOT.split("\n") if not l.startswith("import importlib") and "_lib" not in l and "_ns" not in l and not l.startswith("exec(") and not l.startswith("for _k") and not l.startswith("    if not _k")).replace("try: _native_new(\"ripemd160\", b\"\")\nexcept Exception: hashlib.new = _new", "hashlib.new = _new").replace("if not hasattr(hashlib, \"pbkdf2_hmac\"): hashlib.pbkdf2_hmac = _pbkdf2_hmac", "hashlib.pbkdf2_hmac = _pbkdf2_hmac"))
vec = "_have_native = True\n" + vec
p = subprocess.run([PYB, "-I", "-c", vec], capture_output=True, text=True, cwd=sb)
print("shim check under", PYB, "->", (p.stdout + p.stderr).strip()[-400:])
if p.returncode: raise SystemExit("the shims fail their vectors")
# every example, native ripemd160/pbkdf2 switched off BEFORE the boot snippet runs (what Pyodide does), the library found only in the wheel's folder
drv = r'''
import sys, io, ast, json, hashlib, contextlib
_o = hashlib.new
def _no(name, *a, **k):
    if str(name).lower().startswith("ripemd"): raise ValueError("unsupported hash type ripemd160")
    return _o(name, *a, **k)
hashlib.new = _no
del hashlib.pbkdf2_hmac
exec(%r)
import builtins
man = json.load(open(%r))
bad = 0
for e in man["examples"]:
    ns = {"__name__": "__main__"}; buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
    try:
        t = ast.parse(e["code"])
        if t.body and isinstance(t.body[-1], ast.Expr):
            last = ast.Expression(t.body.pop().value); exec(compile(t, "<c>", "exec"), ns); v = eval(compile(last, "<c>", "eval"), ns)
            if v is not None: print(repr(v))
        else: exec(compile(t, "<c>", "exec"), ns)
    except Exception as ex: print(type(ex).__name__ + ": " + str(ex))
    finally: sys.stdout = old
    got = buf.getvalue().rstrip(); ok = " ".join(got.split()) == " ".join(e["expected"].split())
    bad += (not ok); print("%%2d %%-55s %%s" %% (e["order"], e["name"], "same" if ok else "DIFFERENT: " + got[:200]))
print("examples run with the wheel alone and the pure-Python shims: %%d of %%d same as the manifest" %% (len(man["examples"]) - bad, len(man["examples"])))
sys.exit(1 if bad else 0)
''' % (BOOT, MAN)
p = subprocess.run([PYB, "-I", "-c", "import sys; sys.path.insert(0, %r)\n" % sb + drv], capture_output=True, text=True, cwd=sb, timeout=900)
print(p.stdout + p.stderr[-800:])
shutil.rmtree(sb)
print("wheel", WH, sha[:16], "%d bytes" % size)
sys.exit(p.returncode)
