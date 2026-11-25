#!/usr/bin/env python3
"""Builds the chapter 6 library wheel 1.1.0 (03-materials/ch06/assets/sen0401_ch06_lib-1.1.0-py3-none-any.whl) from sen0401_ch06_tx_lib_v1_1_0.py (Bitcoin Core references; behaviour unchanged). Never overwrites a wheel."""
__version__ = "1.0.0"
import base64, hashlib, os, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H); AS = os.path.join(REPO, "03-materials", "ch06", "assets")
NEW = os.path.join(AS, "sen0401_ch06_lib-1.1.0-py3-none-any.whl"); assert not os.path.exists(NEW)
M = "sen0401_ch06_tx_lib_v1_1_0.py"; files = [(M, open(os.path.join(H, M), "rb").read())]
dist = "sen0401_ch06_lib-1.1.0.dist-info/"
files.append((dist + "METADATA", b"Metadata-Version: 2.1\nName: sen0401-ch06-lib\nVersion: 1.1.0\nSummary: The chapter 6 (Transactions) library of the SEN0401 course, with Bitcoin Core references\n"))
files.append((dist + "WHEEL", b"Wheel-Version: 1.0\nGenerator: sen0401_ch06_wheel_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"))
h = lambda b: "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode()
record = "".join("%s,%s,%d\n" % (n, h(b), len(b)) for n, b in files) + dist + "RECORD,,\n"
files.append((dist + "RECORD", record.encode()))
with zipfile.ZipFile(NEW, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in files:
        zi = zipfile.ZipInfo(n, (2026, 11, 25, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, b)
print("written", NEW, os.path.getsize(NEW), hashlib.sha256(open(NEW, "rb").read()).hexdigest())
