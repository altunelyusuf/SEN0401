#!/usr/bin/env python3
"""sen0401_ch12_page_fix v1.0.0 - writes the next chapter 12 page beside the newest one: no everyday comparison (also in the embedded turtle copies and the lecture), no lambda,
lecture text and titles from the notes of the new deck, the chapter-code examples of the new manifest, "Run slide code" as a top menu item. Never edits an existing version. Chapter 12 only.
Usage: python3 sen0401_ch12_page_fix_v1_0_0.py"""
__version__ = "1.0.0"
import glob, importlib.util, json, os, re
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); TOOL = os.path.join(REPO, "08-tooling"); PD = os.path.join(REPO, "03-materials", "ch12", "page")
sp = importlib.util.spec_from_file_location("nt", os.path.join(TOOL, "sen0401_ch12_notes_v1_0_0.py")); NT = importlib.util.module_from_spec(sp); sp.loader.exec_module(NT)
def vkey(p, ext): return tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.%s$" % ext, p).groups())
src = sorted(glob.glob(os.path.join(PD, "sen0401_ch12_page_v*.html")), key=lambda p: vkey(p, "html"))[-1]; v = vkey(src, "html")
ver = "%d.%d.0" % (v[0], v[1] + 1); dst = os.path.join(PD, "sen0401_ch12_page_v%d_%d_0.html" % (v[0], v[1] + 1)); assert not os.path.exists(dst)
man_p = sorted(glob.glob(os.path.join(PD, "chapter_code_ch12_v*.json")), key=lambda p: vkey(p, "json"))[-1]; man = json.load(open(man_p, encoding="utf-8"))
ddir = os.path.join(TOOL, "ch12-page"); dst_data = os.path.join(ddir, "page_data_v%d_%d_0.json" % (v[0], v[1] + 1)); assert not os.path.exists(dst_data)
H = open(src, encoding="utf-8").read()
tag = '<script type="application/json" id="data">'; a = H.index(tag) + len(tag); b = H.index("</script>", a); data = json.loads(H[a:b]); old_ver = data["_version"]
def ttl(x): return x.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("'", "\\'")   # the form of code inside the embedded turtle copies

# ---- code without lambda: node examples, boot setup
OLD_RATE = "[(k, round(v['fee'] * 1e8 / v['vsize'], 1)) for k, v in sorted(m.items(), key=lambda kv: -float(kv[0]))]"
NEW_RATE = "[(k, round(m[k]['fee'] * 1e8 / m[k]['vsize'], 1)) for k in sorted(m, key=float, reverse=True)]"
DEF_F = "def f(n, w='w'):\n    return hashlib.sha256(('Hello, %sorld! %d' % (w, n) + chr(10)).encode()).hexdigest()\n\n"
n_rate = n_f = 0
for n in data["nodes"]:
    io = n.get("io")
    if not io: continue
    c = io["code"]
    if OLD_RATE in c: io["code"] = c.replace(OLD_RATE, NEW_RATE); n_rate += 1
    elif c.startswith("f = lambda n, w='w': "):
        body = c[len("f = lambda n, w='w': "):]; head, rest = body.split("; (", 1)
        io["code"] = DEF_F + "(" + rest; assert head.startswith("hashlib.sha256(") and head.endswith(".hexdigest()"); assert DEF_F.split("return ")[1].split("\n")[0] == head, head; n_f += 1
assert n_rate == 1 and n_f == 1, (n_rate, n_f)
old_boot = "hw = lambda n, w='w': hashlib.sha256(('Hello, ' + w + 'orld! ' + str(n) + chr(10)).encode()).hexdigest()\n"
new_boot = "def hw(n, w='w'):\n    return hashlib.sha256(('Hello, ' + w + 'orld! ' + str(n) + chr(10)).encode()).hexdigest()\n\n"
assert old_boot in data["py_boot"]; data["py_boot"] = data["py_boot"].replace(old_boot, new_boot)
cc = data["chaptercode"]; assert len(cc["examples"]) == len(man["examples"])
for e, me in zip(cc["examples"], man["examples"]): assert e["slide"] == me["slide"]; e["code"] = me["code"]
cc["file"] = "03-materials/ch12/page/" + os.path.basename(man_p); cc["version"] = man["manifest"].split("_v", 1)[1].replace("_", ".")
# ---- lecture: say and title from the notes of the deck, takeaway without the comparison
for L_ in data["lecture"]:
    k = L_["n"]; L_["say"] = NT.NOTES[k]
    if k in NT.TITLES: L_["title"] = NT.TITLES[k]
    if L_.get("takeaway", "").startswith("Say each idea twice"): L_["takeaway"] = NT.BOT_NEW
data["_version"] = ver
raw = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
H2 = H[:a] + raw + H[b:]
H2 = H2.replace('<meta name="version" content="%s">' % old_ver, '<meta name="version" content="%s">' % ver)

# ---- turtle copies of the node examples
H2 = H2.replace(ttl(OLD_RATE), ttl(NEW_RATE)).replace(OLD_RATE, NEW_RATE)
def seg(pat_start, fn):
    global H2
    out = []; pos = 0
    for m in re.finditer(pat_start, H2):
        if m.start() < pos: continue
        e = H2.index('"', m.start()); out.append((m.start(), e)); pos = e
    for s_, e_ in reversed(out): H2 = H2[:s_] + fn(H2[s_:e_]) + H2[e_:]
    return len(out)
def cb(s):
    s = s.replace("f = lambda n: bytes.fromhex(", "cb = {n: bytes.fromhex(", 1).replace("['coinbaseRaw']);", "['coinbaseRaw']) for n in (277316, 709632, 840000)};".replace("[", "\\[") if False else "['coinbaseRaw']) for n in (277316, 709632, 840000)};")
    s = s.replace("[\\'coinbaseRaw\\']);", "[\\'coinbaseRaw\\']) for n in (277316, 709632, 840000)};")
    for t_ in ("840000", "709632", "277316"): s = s.replace("f(%s)" % t_, "cb[%s]" % t_)
    return s.replace("len(f(n))", "len(cb[n])")
n1 = seg(r"f = lambda n: bytes\.fromhex\(", cb)
def th(s): return s.replace("th = lambda g: (1 - g) / (3 - 2 * g); ", "").replace("round(th(g), 4)", "round((1 - g) / (3 - 2 * g), 4)")
n2 = seg(r"th = lambda g: \(1 - g\)", lambda s: s)
H2 = H2.replace("th = lambda g: (1 - g) / (3 - 2 * g); ", "").replace("round(th(g), 4)", "round((1 - g) / (3 - 2 * g), 4)")
pat_f = re.compile(r"f = lambda n, w=(\\?')w(\\?'): (hashlib\.sha256\(.*?\.hexdigest\(\)); ")
H2, n3 = pat_f.subn(lambda m: "def f(n, w=%sw%s): return %s\\n" % (m.group(1), m.group(2), m.group(3)), H2)
# ---- tutorial text of the page
for old, new in (("lambda  lambda x: …", "lambda  an unnamed one-line function"),
                 ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
                 ('key=lambda x: len(x))', 'key=len)')):
    assert old in H2, old; H2 = H2.replace(old, new)
# ---- everyday comparisons
H2, n_like = re.subn(r" ?It is like [^\"\\]*?\.(?= [A-Z]|[\"\\]|$)", "", H2)
pairs = [(", a key-analogy slide maps house and car keys onto bitcoin keys, and program code", ", and program code"),
         ("Say each idea twice: once as the meaning, once as the everyday comparison", NT.BOT_NEW),
         ("Dice analogy", "Dice model of hashing")]
for old, new in pairs: print(H2.count(old), old[:50]); H2 = H2.replace(old, new)
# ---- the top menu item "Run slide code"
v1 = "['learn','📚 Learn'],['maps'"; v2 = "['learn','📚 Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),['maps'"
g1 = "...(CC.length?[['chaptercode','💻 Chapter code']]:[]),"
assert v1 in H2 and g1 in H2; H2 = H2.replace(v1, v2, 1).replace(g1, "", 1)
open(dst, "w", encoding="utf-8").write(H2); json.dump(data, open(dst_data, "w", encoding="utf-8"), ensure_ascii=False)
print(os.path.basename(dst), os.path.basename(dst_data), "coinbase", n1, "selfish", n2, "hello", n3, "it-is-like removed", n_like)
