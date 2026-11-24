#!/usr/bin/env python3
"""page_build v9.98.0 (chapter 14): builds sen0401_ch14_page_v9_98_0.html from v9_97_0 (which stays as it is).
Changes (rulings of 2026-11-14 and 2026-11-24): no everyday analogy in the page data; the lecture (slide notes) is read from deck plan 2.2.0;
the chapter code is read from chapter_code_ch14_v1_1_0.json (no prompts, no lambdas, comment-led groups); 'Run slide code' is its own top menu item.
Usage: python3 page_build_v9_98_0.py"""
import re, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PG = os.path.join(ROOT, "03-materials", "ch14", "page")
old = open(os.path.join(PG, "sen0401_ch14_page_v9_97_0.html"), encoding="utf-8").read()
m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', old, re.S)
D = json.loads(m.group(2))
plan = json.load(open(os.path.join(ROOT, "08-tooling", "ch14-deck", "deck_plan_v2_2_0.json")))["slides"]
man = json.load(open(os.path.join(PG, "chapter_code_ch14_v1_1_0.json")))

# 1 analogy sentences out
SENT = re.compile(r"\s*It is like.*?(?<![0-9A-Z])\.(?=\s|$)", re.S)
REPL = [("like the tamper-evident seal on a parcel, and", "and"), ("Each pairs a short meaning with something from everyday life, so that the idea can be retold in your own words. ", "Each gives a literal meaning, so that the idea can be retold in your own words. "),
        ("Each pairs a short meaning with something from everyday life. ", "Each gives a literal meaning. "), ("concept cards with everyday comparisons", "concept cards with literal meanings")]
removed = [0]
def clean(x):
    if isinstance(x, str):
        y = x
        if "It is like" in y:
            removed[0] += len(SENT.findall(y)); y = SENT.sub("", y)
        for a, b in REPL: y = y.replace(a, b)
        return y
    if isinstance(x, dict): return {k: (v if k == "py_wheels" else clean(v)) for k, v in x.items()}
    if isinstance(x, list): return [clean(v) for v in x]
    return x
D = clean(D)

# 2 lecture from the plan (notes are the reader-facing text)
lec = []
for i, s in enumerate(plan, 1):
    e = {"n": i, "kind": s["kind"], "title": s["title"], "say": s["notes"], "takeaway": s.get("take") or s.get("sub") or ""}
    lec.append(e)
assert len(lec) == len(D["lecture"]) == 47
D["lecture"] = lec

# 3 chapter code
D["chaptercode"] = {"file": "03-materials/ch14/page/chapter_code_ch14_v1_1_0.json", "version": "1.1.0",
                    "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in man["examples"]]}

js = json.dumps(D, ensure_ascii=False, separators=(", ", ": ")).replace("</", "<\\/")
new = old[:m.start(2)] + js + old[m.end(2):]

# 3b embedded ontology files: new versions beside the old (document 1.1.0: no analogy sentence; domain abox 1.1.0: the fee example without a lambda)
import hashlib
RD = os.path.join(ROOT, "03-materials", "ch14", "rdodi")
def newver(name, edit):
    src = open(os.path.join(RD, name + "_v1_0_0.ttl"), encoding="utf-8").read()
    out = edit(src)
    open(os.path.join(RD, name + "_v1_1_0.ttl"), "w", encoding="utf-8").write(out)
    return src, out
def ed_doc(t):
    n = len(SENT.findall(t)); t = SENT.sub("", t); print("document ttl: sentences removed", n); return t
HOP = "hop = lambda amt: s['med_base_fee_mtokens'] / 1000 + amt * s['med_fee_rate'] / 1_000_000; "
def ed_abox(t):
    n = t.count(HOP)
    t = t.replace(HOP, "fee = s['med_base_fee_mtokens'] / 1000 + 100_000_000 * s['med_fee_rate'] / 1_000_000; ")
    t = t.replace("3 * hop(100_000_000)", "3 * fee"); print("abox ttl: hop lambdas replaced", n); return t
for name, ed in (("sen0401_ch14_document", ed_doc), ("sen0401_ch14_domain_abox", ed_abox)):
    src, out = newver(name, ed)
    pat = re.compile(r'(<script type="text/turtle" data-kind="chapter" data-name=")' + name + r'_v1_0_0\.ttl(" data-sha256=")\w+(">)(.*?)(</script>)', re.S)
    mm = pat.search(new); assert mm and mm.group(4) == src, name + " embedded copy differs from the file"
    new = new[:mm.start()] + mm.group(1) + name + "_v1_1_0.ttl" + mm.group(2) + hashlib.sha256(out.encode()).hexdigest()[:16] + mm.group(3) + out + mm.group(5) + new[mm.end():]
    new = new.replace(name + "_v1_0_0", name + "_v1_1_0")
# the shared materials file stays as it is in the repository; the embedded copy of one sentence is reworded (precedent: Ch8 page)
new = new.replace("a key-analogy slide maps house and car keys onto bitcoin keys, and ", "")
new = new.replace("the idea of the seal is described", "the single-use seal idea is described")
# generic playground text of the page without a lambda
new = new.replace("lambda:'lambda  lambda x: …'", "lambda:'lambda  an unnamed one-line function'")
new = new.replace('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"')
new = new.replace("key=lambda x: len(x))", "key=len)")
# 4 menu item (Ch8 precedent): 'Run slide code' is its own top menu item, no longer inside Learn
a = "...(CC.length?[['chaptercode','💻 Chapter code']]:[])"
assert new.count(a) == 1
new = new.replace(a, "")
b = "const VIEWS=[['learn','📚 Learn'],"; b2 = "const VIEWS=[['learn','📚 Learn'],"
c = "const VIEWS=[['learn','📚 Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),"
if b in new: new = new.replace(b, c, 1)
else:
    b = "const VIEWS=[['learn','📚 Learn'],".replace("'", "\\'")
    assert new.count(b) == 1, "VIEWS not found"
    new = new.replace(b, c.replace("'", "\\'"), 1)
# 5 lambdas in page text (course playground examples) become def
new = new.replace("a = lambda k: h[k]['allowed']", "def a(k): return h[k]['allowed']")
open(os.path.join(PG, "sen0401_ch14_page_v9_98_0.html"), "w", encoding="utf-8").write(new)
json.dump({"analogy_sentences_removed": removed[0]}, open("/tmp/c14/page_build.json", "w"))
print("removed analogy sentences:", removed[0], "| wrote v9_98_0")
