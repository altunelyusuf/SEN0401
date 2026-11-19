#!/usr/bin/env python3
"""Apply the reader-facing notes (sen0401_ch78_readernotes_v1_0_0.py) to the newest deck and page of chapter 7 or 8.
Usage: python3 sen0401_ch78_readernotes_apply_v1_0_0.py 7|8   (writes the next deck, page, manifest and page_data versions; never overwrites)."""
import sys, os, re, glob, json, shutil, importlib.util
from pptx import Presentation
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); TOOL = os.path.join(REPO, "08-tooling")
sp = importlib.util.spec_from_file_location("rn", os.path.join(TOOL, "sen0401_ch78_readernotes_v1_0_0.py")); RN = importlib.util.module_from_spec(sp); sp.loader.exec_module(RN)
ch = int(sys.argv[1]); NOTES = {7: RN.RN7, 8: RN.RN8}[ch]; PAGE_MINOR = {7: 99, 8: 100}[ch]
D = os.path.join(REPO, "03-materials", "ch0%d" % ch); PD = os.path.join(D, "page"); DD = os.path.join(TOOL, "ch0%d-page" % ch)
def vk(p, ext): return tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.%s$" % ext, p).groups())
def newest(pat, ext): return sorted(glob.glob(pat), key=lambda p: vk(p, ext))[-1]
deck = newest(os.path.join(D, "SEN0401_Ch0%d_*_3e_v*.pptx" % ch), "pptx"); page = newest(os.path.join(PD, "sen0401_ch0%d_page_v*.html" % ch), "html")
man = newest(os.path.join(PD, "chapter_code_ch0%d_v*.json" % ch), "json")
dv, pv, mv = vk(deck, "pptx"), vk(page, "html"), vk(man, "json")
deck2 = re.sub(r"_v\d+_\d+_\d+\.pptx$", "_v%d_%d_0.pptx" % (dv[0], dv[1] + 1), deck)
page2 = re.sub(r"_v\d+_\d+_\d+\.html$", "_v9_%d_0.html" % PAGE_MINOR, page)
man2 = re.sub(r"_v\d+_\d+_\d+\.json$", "_v%d_%d_0.json" % (mv[0], mv[1] + 1), man)
data2 = os.path.join(DD, "page_data_v9_%d_0.json" % PAGE_MINOR)
for f in (deck2, page2, man2, data2): assert not os.path.exists(f), f
M = json.load(open(man)); ex_of = {e["slide"]: i + 1 for i, e in enumerate(M["examples"])}
def final(n):
    t = NOTES[n]
    if "{EX}" in t:
        assert n in ex_of, (n, "no example on this slide"); t = t.replace("{EX}", str(ex_of[n]))
    return t.strip()
P = Presentation(deck); assert len(P.slides) == len(NOTES), (len(P.slides), len(NOTES))
for i, s in enumerate(P.slides, 1): s.notes_slide.notes_text_frame.text = final(i)
P.save(deck2)
M["deck"] = os.path.basename(deck2); M["deck_version"] = "%d.%d.0" % (dv[0], dv[1] + 1); M["manifest"] = os.path.basename(man2)[:-5]
json.dump(M, open(man2, "w"), indent=1, ensure_ascii=False)
H = open(page, encoding="utf-8").read(); tag = '<script type="application/json" id="data">'; a = H.index(tag) + len(tag); b = H.index("</script>", a)
data = json.loads(H[a:b]); old_ver = data["_version"]; new_ver = "9.%d.0" % PAGE_MINOR
for L in data["lecture"]: L["say"] = final(L["n"])
data["_version"] = new_ver; data["chaptercode"]["file"] = "03-materials/ch0%d/page/%s" % (ch, os.path.basename(man2)); data["chaptercode"]["version"] = "%d.%d.0" % (mv[0], mv[1] + 1)
H2 = H[:a] + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + H[b:]
H2 = H2.replace('<meta name="version" content="%s">' % old_ver, '<meta name="version" content="%s">' % new_ver)
old = "<p>'+esc(s.say)+'</p>"; assert H2.count(old) == 1
H2 = H2.replace(old, "'+esc(s.say).split(/\\n\\n+/).map(function(t){return '<p>'+t+'</p>'}).join('')+'")   # one paragraph per blank-line block of a note
open(page2, "w", encoding="utf-8").write(H2); json.dump(data, open(data2, "w"), ensure_ascii=False)
print(os.path.basename(deck2), os.path.basename(page2), os.path.basename(man2), os.path.basename(data2))
