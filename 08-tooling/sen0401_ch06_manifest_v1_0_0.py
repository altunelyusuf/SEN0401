#!/usr/bin/env python3
"""Writes chapter_code_ch06_v1_4_0.json from v1_3_0 (never edited): the deck is v2_5_0, the library is sen0401_ch06_tx_lib_v1_1_0 (wheel 1.1.0, Bitcoin Core references). The 18 examples keep their code and expected results;
every one is executed here, setup + listing, under this interpreter and each 'show' expression must give its stated value. Usage: python3 sen0401_ch06_manifest_v1_0_0.py"""
__version__ = "1.0.0"
import hashlib, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H); PG = os.path.join(REPO, "03-materials", "ch06", "page")
sys.path.insert(0, H)
d = json.load(open(os.path.join(PG, "chapter_code_ch06_v1_3_0.json"), encoding="utf-8"))
wh = os.path.join(REPO, "03-materials", "ch06", "assets", "sen0401_ch06_lib-1.1.0-py3-none-any.whl")
d["manifest"] = "chapter_code_ch06_v1_4_0"; d["deck"] = "SEN0401_Ch06_Transactions_3e_v2_5_0.pptx"; d["deck_version"] = "2.5.0"
d["library"] = {"module": "sen0401_ch06_tx_lib_v1_1_0", "file": "03-materials/ch06/assets/sen0401_ch06_lib-1.1.0-py3-none-any.whl", "sha256": hashlib.sha256(open(wh, "rb").read()).hexdigest(),
                "modules": ["sen0401_ch06_tx_lib_v1_1_0"], "import": "from sen0401_ch06_tx_lib_v1_1_0 import *"}
for e in d["examples"]: e["library"] = "sen0401_ch06_tx_lib_v1_1_0"
import sen0401_ch06_tx_lib_v1_1_0 as L
bad = 0
for e in d["examples"]:
    g = {k: getattr(L, k) for k in dir(L) if not k.startswith("_")}
    exec(d["setup"]["code"], g); exec(e["code"], g)
    for s in e.get("show", []):
        v = repr(eval(s["expression"], g))
        if v != s["expected"]: print("MISMATCH", e["order"], s["expression"], v[:60], s["expected"][:60]); bad += 1
assert not bad
out = os.path.join(PG, "chapter_code_ch06_v1_4_0.json"); assert not os.path.exists(out)
json.dump(d, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("wrote", out, len(d["examples"]), "examples, all expected values reproduced")
