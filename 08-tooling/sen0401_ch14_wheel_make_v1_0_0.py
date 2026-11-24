#!/usr/bin/env python3
"""sen0401_ch14_wheel_make v1.0.0 - builds the chapter 14 library wheel 1.1.0 (03-materials/ch14/assets/sen0401_ch14_lib-1.1.0-py3-none-any.whl) beside the committed 1.0.0 wheel, which stays unchanged.
The new wheel holds the two library modules of version 1.1.0 (Bitcoin Core references in the module docstrings; the p2p module is the unchanged 1.0.0 of chapter 10) and every saved file of the 1.0.0 wheel byte for byte (ch14-evidence)."""
__version__ = "1.0.0"
import base64, hashlib, os, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H); AS = os.path.join(REPO, "03-materials", "ch14", "assets")
OLD = os.path.join(AS, "sen0401_ch14_lib-1.0.0-py3-none-any.whl"); NEW = os.path.join(AS, "sen0401_ch14_lib-1.1.0-py3-none-any.whl")
MODS = ["sen0401_ch14_lib_v1_1_0.py", "sen0401_ch10_p2p_v1_0_0.py", "sen0401_ch14_crypto_v1_1_0.py"]
files = [(m, open(os.path.join(H, m), "rb").read()) for m in MODS]
with zipfile.ZipFile(OLD) as z:
    for n in z.namelist():
        if n.startswith("ch14-evidence/"): files.append((n, z.read(n)))
dist = "sen0401_ch14_lib-1.1.0.dist-info/"
files.append((dist + "METADATA", b"Metadata-Version: 2.1\nName: sen0401-ch14-lib\nVersion: 1.1.0\nSummary: The chapter 14 (Second-Layer Applications) library of the SEN0401 course with the saved files its worked examples read.\n"))
files.append((dist + "WHEEL", b"Wheel-Version: 1.0\nGenerator: sen0401_ch14_wheel_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"))
h = lambda b: "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode()
record = "".join("%s,%s,%d\n" % (n, h(b), len(b)) for n, b in files) + dist + "RECORD,,\n"
files.append((dist + "RECORD", record.encode()))
with zipfile.ZipFile(NEW, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in files:
        zi = zipfile.ZipInfo(n, (2026, 11, 24, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, b)
print("written", NEW, os.path.getsize(NEW), "bytes", hashlib.sha256(open(NEW, "rb").read()).hexdigest())
