#!/usr/bin/env python3
"""Builds 03-materials/ch02/assets/sen0401_ch02_lib-1.1.0-py3-none-any.whl from 08-tooling/sen0401_ch02_tx_lib_v1_1_0.py (the committed 1.0.0 wheel stays) and
the chapter-code manifest 1.2.0 from 1.1.0 (deck 3.3.0, library 1.1.0 with its wheel and hash). Standard library only."""
__version__ = "1.0.0"
import base64, hashlib, json, os, zipfile
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
MOD = "sen0401_ch02_tx_lib_v1_1_0.py"; WH = "sen0401_ch02_lib-1.1.0-py3-none-any.whl"
src = open(os.path.join(H, MOD), "rb").read()
meta = b"Metadata-Version: 2.1\nName: sen0401-ch02-lib\nVersion: 1.1.0\nSummary: The chapter 2 (How Bitcoin Works) library of the SEN0401 course (standard library only).\n"
whl = b"Wheel-Version: 1.0\nGenerator: sen0401_ch02_wheel_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
di = "sen0401_ch02_lib-1.1.0.dist-info/"
def rec(n, b): return "%s,sha256=%s,%d" % (n, base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode(), len(b))
record = "\n".join([rec(MOD, src), rec(di + "METADATA", meta), rec(di + "WHEEL", whl), di + "RECORD,,"]) + "\n"
out = os.path.join(R, "03-materials", "ch02", "assets", WH)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for n, b in ((MOD, src), (di + "METADATA", meta), (di + "WHEEL", whl), (di + "RECORD", record.encode())):
        zi = zipfile.ZipInfo(n, (2026, 11, 25, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; z.writestr(zi, b)
sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
P = os.path.join(R, "03-materials", "ch02", "page")
c = json.load(open(os.path.join(P, "chapter_code_ch02_v1_1_0.json")))
c["manifest"] = "chapter_code_ch02_v1_2_0"; c["deck"] = "SEN0401_Ch02_HowBitcoinWorks_3e_v3_3_0.pptx"; c["deck_version"] = "3.3.0"
c["library"] = {"module": "sen0401_ch02_tx_lib_v1_1_0", "file": "03-materials/ch02/assets/" + WH, "sha256": sha, "modules": ["sen0401_ch02_tx_lib_v1_1_0"],
                "import": "import sen0401_ch02_tx_lib_v1_1_0 as T", "requires": "Python standard library only (hashlib, math, struct, urllib.parse)",
                "bitcoin_core": "pointers in the module docstring, read on the master branch of github.com/bitcoin/bitcoin, commit 079437c"}
c["setup"]["code"] = c["setup"]["code"].replace("sen0401_ch02_tx_lib_v1_0_0", "sen0401_ch02_tx_lib_v1_1_0")
json.dump(c, open(os.path.join(P, "chapter_code_ch02_v1_2_0.json"), "w"), indent=1, ensure_ascii=False)
print(WH, sha[:16], os.path.getsize(out), "bytes; manifest 1.2.0 written;", len(c["examples"]), "examples")
