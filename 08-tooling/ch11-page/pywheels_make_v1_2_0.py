#!/usr/bin/env python3
"""pywheels_make v1_2_0 (SEN0401 chapter 11). Writes the wheel 03-materials/ch11/assets/sen0401_ch11_lib-1.1.0-py3-none-any.whl (the committed 1.0.0 wheel is not touched) and pywheels_v1_2_0.json.
The wheel holds the library sen0401_ch11_lib_v1_1_0.py (Bitcoin Core references of the verified list) and the protocol module sen0401_ch10_p2p_v1_1_0.py, copied byte for byte from 08-tooling; the saved files of the 1.0.0 wheel
(read from it, unchanged) and three more Bitcoin Core files (MIT) that the library's Core references name: core_src_primitives_block.h, core_src_rpc_blockchain.cpp, core_src_signet.cpp, copied from 08-tooling/ch11-evidence.
The boot snippet runs the setup of the newest chapter-code manifest (v1_2_0) and is executed here before anything is written. Usage: pywheels_make_v1_2_0.py"""
__version__ = "1.2.0"
import base64, hashlib, json, os, shutil, sys, tempfile, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); T = os.path.join(REPO, "08-tooling"); AS = os.path.join(REPO, "03-materials", "ch11", "assets")
OLD = os.path.join(AS, "sen0401_ch11_lib-1.0.0-py3-none-any.whl"); WH = "sen0401_ch11_lib-1.1.0-py3-none-any.whl"; LIB = "sen0401_ch11_lib_v1_1_0.py"; P2P = "sen0401_ch10_p2p_v1_1_0.py"
EXTRA = ["core_src_primitives_block.h", "core_src_rpc_blockchain.cpp", "core_src_signet.cpp"]
MF = os.path.join(REPO, "03-materials", "ch11", "page", "chapter_code_ch11_v1_2_0.json"); man = json.load(open(MF)); setup = man["setup"]["code"]
fl = {LIB: open(os.path.join(T, LIB), "rb").read(), P2P: open(os.path.join(T, P2P), "rb").read()}
with zipfile.ZipFile(OLD) as z:
    for n in z.namelist():
        if n.startswith("ch11-evidence/"): fl[n] = z.read(n)
for f in EXTRA: fl["ch11-evidence/" + f] = open(os.path.join(T, "ch11-evidence", f), "rb").read()
fl["sen0401_ch11_lib-1.1.0.dist-info/METADATA"] = b"Metadata-Version: 2.1\nName: sen0401-ch11-lib\nVersion: 1.1.0\nSummary: The chapter 11 (The Blockchain) library of the SEN0401 course with the saved files its worked examples read.\n"
fl["sen0401_ch11_lib-1.1.0.dist-info/WHEEL"] = b"Wheel-Version: 1.0\nGenerator: pywheels_make_v1_2_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
def entry(z, name, data):
    zi = zipfile.ZipInfo(name, (2026, 11, 24, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, data)
rec = []; path = os.path.join(AS, WH)
with zipfile.ZipFile(path, "w") as z:
    for n, b in fl.items():
        entry(z, n, b); rec.append("%s,sha256=%s,%d" % (n, base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode(), len(b)))
    entry(z, "sen0401_ch11_lib-1.1.0.dist-info/RECORD", ("\n".join(rec) + "\nsen0401_ch11_lib-1.1.0.dist-info/RECORD,,\n").encode())
sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
boot = "import builtins\n" + setup + "\nfor _n in [k for k in list(globals()) if not k.startswith('_') and k != 'builtins']: setattr(builtins, _n, globals()[_n])\n"
tmp = tempfile.mkdtemp(prefix="pywheels_ch11_")
with zipfile.ZipFile(path) as z: z.extractall(tmp)
sys.path.insert(0, tmp); ns = {}; exec(boot, ns); shutil.rmtree(tmp, ignore_errors=True)
json.dump({"_version": "1.2.0", "wheels": [{"file": WH, "sha256": sha}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the chapter 11 library and the protocol module (standard library only) and, in the folder ch11-evidence beside them, the saved files the worked examples read and the Bitcoin Core files the library names (%d files). The boot snippet runs the setup of the chapter-code manifest %s once (L = the library, R = the recorded run of Bitcoin Core 31.1, hashlib) and makes those names ready in every program." % (len([n for n in fl if n.startswith("ch11-evidence/")]), os.path.basename(MF))},
          open(os.path.join(H, "pywheels_v1_2_0.json"), "w"), indent=1)
print("wheel", WH, sha, os.path.getsize(path), "bytes")
