#!/usr/bin/env python3
"""chapter_code_make v1.3.0 (SEN0401 chapter 5): writes 03-materials/ch05/page/chapter_code_ch05_v1_3_0.json beside the committed v1_2_0 (which stays unchanged).
The 27 examples are the code of the code slides of the deck 3.8.0 (read from the deck, boxes in reading order, joined by line breaks) and must equal the code of 1.2.0 (the deck re-cut its boxes at statement
boundaries and changed no code); the library is the chapter library 1.2.0 (no lambda, Bitcoin Core references in its docstring). Usage: python3 chapter_code_make_v1_3_0.py"""
__version__ = "1.3.0"
import hashlib, json, os, re
from pptx import Presentation
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H)); PG = os.path.join(REPO, "03-materials", "ch05", "page")
DECK = os.path.join(REPO, "03-materials", "ch05", "SEN0401_Ch05_WalletRecovery_3e_v3_8_0.pptx")
LIB = os.path.join(REPO, "08-tooling", "sen0401_ch05_wallet_lib_v1_2_0.py")
OLD = json.load(open(os.path.join(PG, "chapter_code_ch05_v1_2_0.json"))); DST = os.path.join(PG, "chapter_code_ch05_v1_3_0.json")
assert not os.path.exists(DST)
p = Presentation(DECK); code = {}
for i, s in enumerate(p.slides, 1):
    bx = sorted([x for x in s.shapes if x.has_text_frame and x.name.startswith("code ")], key=lambda x: (x.top, x.left))
    if bx: code[i] = "\n".join(x.text_frame.text for x in bx)
new = json.loads(json.dumps(OLD))
for e in new["examples"]:
    assert code[e["slide"]].strip() == e["code"].strip(), ("the code of the slide differs from 1.2.0", e["slide"])
assert len(new["examples"]) == len(code) == 27
new["version"] = "1.3.0"; new["deck"] = "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_8_0.pptx"
new["executed_with"]["library"] = "sen0401_ch05_wallet_lib_v1_2_0"
new["library"]["file"] = "08-tooling/sen0401_ch05_wallet_lib_v1_2_0.py"; new["library"]["sha256"] = hashlib.sha256(open(LIB, "rb").read()).hexdigest()
new["about"] = ("The code examples of the chapter 5 deck v3.8.0, in the order of the code slides (order = slide order): the code of an example is the code of its slide, unchanged (no prompt, no probe line, no lambda). "
                "The page's chapter-code tab ('Run slide code') lists them by NAME in this order; the code runs in the page with the chapter library 1.2.0 and the prelude defined first; the expected result is what the run printed. "
                "1.3.0 changes only the deck and the library: the deck cut its code boxes at statement boundaries, and the library has no lambda and points to Bitcoin Core in its docstring.")
json.dump(new, open(DST, "w"), indent=1, ensure_ascii=False)
print("written", DST, new["library"]["sha256"][:16])
