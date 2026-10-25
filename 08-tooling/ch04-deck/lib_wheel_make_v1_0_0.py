#!/usr/bin/env python3
"""lib_wheel_make v1.0.0 (SEN0401 chapter 4 deck 3.4.0). Writes 03-materials/ch04/assets/sen0401_ch04_lib-1.0.0-py3-none-any.whl: the chapter library 08-tooling/sen0401_ch04_lib_v1_0_0.py copied byte
for byte, with a dist-info folder; zip entries carry a fixed date, so the file (and its SHA-256) is the same on every run. It then runs the wheel, unzipped into a scratch folder that holds ONLY the wheel's
files, under the browser's Python (python3.13 by default) with the native RIPEMD-160 switched off (as in the page's Pyodide), against the recorded expected values of every example of examples_out_v3_4_0.json,
and prints the verdict. Usage: lib_wheel_make_v1_0_0.py [PYTHON_FOR_THE_BROWSER_VERSION]   (default /root/.local/bin/python3.13)"""
__version__ = "1.0.0"
import json, os, subprocess, sys, tempfile, zipfile, shutil, hashlib
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); ROOT = os.path.dirname(T)
PYB = sys.argv[1] if len(sys.argv) > 1 else "/root/.local/bin/python3.13"
LIB = "sen0401_ch04_lib_v1_0_0.py"; WH = "sen0401_ch04_lib-1.0.0-py3-none-any.whl"
AS = os.path.join(ROOT, "03-materials", "ch04", "assets"); path = os.path.join(AS, WH)
def entry(z, name, data):
    zi = zipfile.ZipInfo(name, (2026, 10, 25, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, data)
with zipfile.ZipFile(path, "w") as z:
    entry(z, LIB, open(os.path.join(T, LIB), "rb").read())
    entry(z, "sen0401_ch04_lib-1.0.0.dist-info/METADATA", b"Metadata-Version: 2.1\nName: sen0401-ch04-lib\nVersion: 1.0.0\nSummary: The chapter 4 (Keys and Addresses) library of the SEN0401 course.\n")
    entry(z, "sen0401_ch04_lib-1.0.0.dist-info/WHEEL", b"Wheel-Version: 1.0\nGenerator: lib_wheel_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
print("wrote", os.path.relpath(path, ROOT), "sha256", hashlib.sha256(open(path, "rb").read()).hexdigest())
# the wheel, alone, under the browser's Python and without a native RIPEMD-160
sys.path.insert(0, H)
import examples_v3_4_0 as X
rec = json.load(open(os.path.join(H, "examples_out_v3_4_0.json")))
scratch = tempfile.mkdtemp(prefix="ch04_wheel_"); zipfile.ZipFile(path).extractall(scratch)
drv = "import hashlib, sys, json\nsys.path.insert(0, %r)\n" % scratch + "_n = hashlib.new\ndef _no(name, data=b'', **k):\n    if str(name).lower().replace('-', '') == 'ripemd160': raise ValueError('unsupported hash type ripemd160')\n    return _n(name, data, **k)\nhashlib.new = _no\n" \
      "import sen0401_ch04_lib_v1_0_0 as _L\nassert _L.ripemd160.__name__ == '<lambda>', 'the pure RIPEMD-160 is not in use'\n" \
      "src = json.loads(sys.stdin.read()); ns = {}\nexec(src['pre'], ns); exec(src['code'], ns)\nprint(json.dumps([[x, repr(eval(x, ns))] for x in src['show']]))\n"
bad = 0
for e in X.EXAMPLES:
    p = subprocess.run([PYB, "-c", drv], input=json.dumps({"pre": X.PRELUDE, "code": "\n".join(e["lines"]), "show": e["show"]}), capture_output=True, text=True, cwd=tempfile.gettempdir(), timeout=120)
    got = json.loads(p.stdout) if p.returncode == 0 else None
    ok = got == rec[e["id"]]
    bad += (not ok)
    print(e["id"], "PASS" if ok else "FAIL %s" % (p.stderr.strip().splitlines()[-1:] or got))
shutil.rmtree(scratch)
print("wheel check under %s without native RIPEMD-160: %d of %d examples differ" % (PYB, bad, len(X.EXAMPLES)))
sys.exit(1 if bad else 0)
