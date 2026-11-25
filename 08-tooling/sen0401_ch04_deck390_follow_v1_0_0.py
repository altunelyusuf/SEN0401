#!/usr/bin/env python3
"""sen0401_ch04_deck390_follow v1.0.0: the chapter code manifest 1.2.1 and the page 9.78.0 follow the deck 3.9.0 (code slides in the step-balloon layout); code and slide order unchanged. The page 9.77.0 carried the meta version 9.75.0 beside the data version 9.77.0: 9.78.0 carries 9.78.0 in both. Refuses to overwrite. Usage: run in the repository root."""
__version__ = "1.0.0"
import json, os
C = "03-materials/ch04/page/"
def new(p):
    assert not os.path.exists(p), p; return p
man = json.load(open(C + "chapter_code_ch04_v1_2_0.json", encoding="utf-8"))
man["manifest"] = "chapter_code_ch04_v1_2_1"; man["deck"] = "SEN0401_Ch04_KeysAndAddresses_3e_v3_9_0.pptx"; man["deck_version"] = "3.9.0"
json.dump(man, open(new(C + "chapter_code_ch04_v1_2_1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
h = open(C + "sen0401_ch04_page_v9_77_0.html", encoding="utf-8", newline="").read()
for old, nw in (('chapter_code_ch04_v1_2_0.json", "version": "1.2.0"', 'chapter_code_ch04_v1_2_1.json", "version": "1.2.1"'),
                ('"_version": "9.77.0"', '"_version": "9.78.0"'), ('<meta name="version" content="9.75.0">', '<meta name="version" content="9.78.0">')):
    assert h.count(old) == 1, old; h = h.replace(old, nw)
open(new(C + "sen0401_ch04_page_v9_78_0.html"), "w", encoding="utf-8", newline="").write(h); print("ok")
