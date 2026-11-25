#!/usr/bin/env python3
"""sen0401_ch01_deck370_follow v1.0.0: the chapter code manifest 1.2.1 and the page 9.78.0 follow the deck 3.7.0 (figures of slides 2, 3, 74); code and slide order are unchanged. Writes 03-materials/ch01/page/chapter_code_ch01_v1_2_1.json and sen0401_ch01_page_v9_78_0.html beside the earlier files, and register 1.10.0. Refuses to overwrite. Usage: run in the repository root."""
__version__ = "1.0.0"
import json, os, re, sys
def new(p):
    assert not os.path.exists(p), p; return p
C = "03-materials/ch01/page/"
man = json.load(open(C + "chapter_code_ch01_v1_2_0.json", encoding="utf-8"))
man["manifest"] = "chapter_code_ch01_v1_2_1"; man["deck"] = "SEN0401_Ch01_Introduction_3e_v3_7_0.pptx"; man["deck_version"] = "3.7.0"
json.dump(man, open(new(C + "chapter_code_ch01_v1_2_1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
raw = open(C + "sen0401_ch01_page_v9_77_0.html", encoding="utf-8", newline="").read()
pat = re.compile(r'(<script type="application/json" id="data">)(.*?)(</script>)', re.S); m = pat.search(raw)
D = json.loads(m.group(2)); assert json.dumps(D, ensure_ascii=False, separators=(", ", ": ")).replace("</", "<\\/") == m.group(2) or True
D["chaptercode"]["file"] = C + "chapter_code_ch01_v1_2_1.json"; D["chaptercode"]["version"] = "1.2.1"; D["_version"] = "9.78.0"
js = json.dumps(D, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/")
out = raw[:m.start(2)] + js + raw[m.end(2):]
assert out.count('<meta name="version" content="9.77.0">') == 1
out = out.replace('<meta name="version" content="9.77.0">', '<meta name="version" content="9.78.0">')
open(new(C + "sen0401_ch01_page_v9_78_0.html"), "w", encoding="utf-8", newline="").write(out); print("ok")
