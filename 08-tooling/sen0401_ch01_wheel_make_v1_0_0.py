#!/usr/bin/env python3
"""sen0401_ch01_wheel_make v1.0.0 - builds the chapter 1 library wheel 1.1.0 (03-materials/ch01/assets/sen0401_ch01_lib-1.1.0-py3-none-any.whl) beside the committed 1.0.0 wheel, which stays unchanged.
The new wheel holds the library module of version 1.1.0 (no lambda, Bitcoin Core references in the module docstring; the code of the functions is the code of 1.0.0)."""
__version__ = "1.0.0"
import base64, hashlib, os, zipfile
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H); AS = os.path.join(REPO, "03-materials", "ch01", "assets")
NEW = os.path.join(AS, "sen0401_ch01_lib-1.1.0-py3-none-any.whl")
assert not os.path.exists(NEW), NEW
files = [("sen0401_ch01_lib_v1_1_0.py", open(os.path.join(H, "sen0401_ch01_lib_v1_1_0.py"), "rb").read())]
dist = "sen0401_ch01_lib-1.1.0.dist-info/"
files.append((dist + "METADATA", b"Metadata-Version: 2.1\nName: sen0401-ch01-lib\nVersion: 1.1.0\nSummary: The chapter 1 (Introduction) library of the SEN0401 course (standard library only).\n"))
files.append((dist + "WHEEL", b"Wheel-Version: 1.0\nGenerator: sen0401_ch01_wheel_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"))
h = lambda b: "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode()
record = "".join("%s,%s,%d\n" % (n, h(b), len(b)) for n, b in files) + dist + "RECORD,,\n"
files.append((dist + "RECORD", record.encode()))
with zipfile.ZipFile(NEW, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in files:
        zi = zipfile.ZipInfo(n, (2026, 11, 25, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, b)
print("written", NEW, os.path.getsize(NEW), "bytes", hashlib.sha256(open(NEW, "rb").read()).hexdigest())
