#!/usr/bin/env python3
"""sen0401_ch13_gap_fix v1.0.0 - closes the remaining gaps of the chapter 13 set; writes new versions beside the committed ones, edits nothing that exists:
  library 1.2.0 (module sen0401_ch13_lib_v1_2_0, wheel 1.3.0) with Bitcoin Core references checked against the real files of github.com/bitcoin/bitcoin (saved in ch13-evidence),
  manifest chapter_code_ch13_v1_4_0.json, domain ABox 1.1.1 (recorded inputs re-run with the new library and compared with the recorded outputs), document ontology 1.1.1,
  diagrams ABox 1.0.0 written as a repository file, page 9.98.0 whose embedded Turtle blocks are byte-identical copies of repository files.
Run from the repository root:  python3 08-tooling/sen0401_ch13_gap_fix_v1_0_0.py"""
__version__ = "1.0.0"
import base64, hashlib, io, json, os, re, sys, zipfile
REPO = os.getcwd(); T = os.path.join(REPO, "08-tooling"); EV = os.path.join(T, "ch13-evidence")
M = os.path.join(REPO, "03-materials", "ch13"); PG = os.path.join(M, "page"); AS = os.path.join(M, "assets"); RD = os.path.join(M, "rdodi")
sys.path.insert(0, T)
rd = lambda p: open(p, encoding="utf-8").read()
def wr(p, s):
    assert not os.path.exists(p), p
    open(p, "w", encoding="utf-8").write(s)

# 1 -------------------------------------------------------------------------- Core references, each one an anchor in a saved real file
ANCH = [("core_src_base58.cpp", "EncodeBase58Check"), ("core_src_base58.cpp", "pszBase58 = \"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz\""),
        ("core_src_base58.cpp", "str.assign(zeroes, '1')"), ("core_src_base58.cpp", "vch.insert(vch.end(), hash.data(), hash.data() + 4)"),
        ("core_src_hash.h", "class CHash256"), ("core_src_hash.h", "sha.Reset().Write(buf, CSHA256::OUTPUT_SIZE).Finalize(output.data())"),
        ("core_src_key.cpp", "static const unsigned char hashkey[] = {'B','i','t','c','o','i','n',' ','s','e','e','d'}"), ("core_src_key.cpp", "CHMAC_SHA512{hashkey, sizeof(hashkey)}"),
        ("core_src_key.cpp", "memcpy(chaincode.begin(), vout.data() + 32, 32)"), ("core_src_kernel_chainparams.cpp", "base58Prefixes[EXT_SECRET_KEY] = {0x04, 0x88, 0xAD, 0xE4}")]
for f, frag in ANCH:
    assert re.sub(r"\s+", " ", frag) in re.sub(r"\s+", " ", open(os.path.join(EV, f), errors="replace").read()), (f, frag)
print("Core anchors found in the saved real files:", len(ANCH))
OLD, NEW = "sen0401_ch13_lib_v1_1_0", "sen0401_ch13_lib_v1_2_0"
src = rd(os.path.join(T, OLD + ".py"))
a = src.index("References (version 1.1.0"); b = src.index('"""', a)
refs = src[a:b].replace("References (version 1.1.0;", "References (version 1.2.0;")
refs = refs.rstrip() + """
* b58check(): Base58Check as Bitcoin Core writes it, EncodeBase58Check in src/base58.cpp (core_src_base58.cpp): Hash(vch) gives the double SHA-256 of src/hash.h (class CHash256, core_src_hash.h), its first 4 bytes are appended, and EncodeBase58 writes every leading zero byte as '1' with the alphabet pszBase58.
* bip32_master(): CExtKey::SetSeed in src/key.cpp (core_src_key.cpp): CHMAC_SHA512 keyed with the twelve characters 'Bitcoin seed', the first 32 bytes are the key, the last 32 the chain code; the version bytes 0x0488ADE4 of the xprv are base58Prefixes[EXT_SECRET_KEY] of the main chain in src/kernel/chainparams.cpp (core_src_kernel_chainparams.cpp)."""
src2 = src[:a] + refs + src[b:]
src2 = src2.replace('__version__ = "1.1.0"', '__version__ = "1.2.0"')
src2 = src2.replace('def b58check(payload):\n', 'def b58check(payload):\n    """Base58Check: the payload, then the first 4 bytes of its double SHA-256 as a check, written in base 58; the same steps as EncodeBase58Check in Bitcoin Core src/base58.cpp."""\n', 1)
assert src2.count("EncodeBase58Check in Bitcoin Core") == 1 and "__version__ = \"1.2.0\"" in src2
wr(os.path.join(T, NEW + ".py"), src2)
# wheel 1.3.0: the modules of wheel 1.2.0 with the new library module
WO = os.path.join(AS, "sen0401_ch13_lib-1.2.0-py3-none-any.whl"); WN = os.path.join(AS, "sen0401_ch13_lib-1.3.0-py3-none-any.whl")
files = [(NEW + ".py", src2.encode())]
with zipfile.ZipFile(WO) as z:
    for n in z.namelist():
        if n.endswith(OLD + ".py") or ".dist-info/" in n: continue
        files.append((n, z.read(n)))
dist = "sen0401_ch13_lib-1.3.0.dist-info/"
files.append((dist + "METADATA", b"Metadata-Version: 2.1\nName: sen0401-ch13-lib\nVersion: 1.3.0\nSummary: The chapter 13 (Bitcoin Security) library of the SEN0401 course with the saved files its worked examples read.\n"))
files.append((dist + "WHEEL", b"Wheel-Version: 1.0\nGenerator: sen0401_ch13_gap_fix_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"))
h64 = lambda x: "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(x).digest()).rstrip(b"=").decode()
files.append((dist + "RECORD", ("".join("%s,%s,%d\n" % (n, h64(x), len(x)) for n, x in files) + dist + "RECORD,,\n").encode()))
assert not os.path.exists(WN)
with zipfile.ZipFile(WN, "w", zipfile.ZIP_DEFLATED) as z:
    for n, x in files:
        zi = zipfile.ZipInfo(n, (2026, 11, 24, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, x)
WB = open(WN, "rb").read(); WSHA = hashlib.sha256(WB).hexdigest(); print("wheel", os.path.basename(WN), len(WB), WSHA[:16])

# 2 -------------------------------------------------------------------------- manifest 1.4.0, all examples run with the new library
import importlib
L = importlib.import_module(NEW); R = L.run(); seen = L.has
man = json.load(open(os.path.join(PG, "chapter_code_ch13_v1_3_0.json"), encoding="utf-8"))
man["manifest"] = "chapter_code_ch13_v1_4_0"
man["library"] = {"module": "sen0401_ch13_lib", "file": "03-materials/ch13/assets/sen0401_ch13_lib-1.3.0-py3-none-any.whl", "sha256": WSHA, "modules": [NEW, "sen0401_ch10_p2p_v1_0_0"],
                  "import": "import %s as L; R = L.run(); seen = L.has" % NEW}
man["setup"]["code"] = man["setup"]["code"].replace(OLD, NEW)
bad = []
for e in man["examples"]:
    ns = {"L": L, "R": R, "seen": seen, "hashlib": hashlib, "math": __import__("math")}
    exec(e["code"], ns)
    for sh in e["show"]:
        got = repr(eval(sh["expression"], ns))
        if got != sh["expected"]: bad.append((e["id"], sh["expression"], got, sh["expected"]))
assert not bad, bad
print("manifest examples run with the new library:", len(man["examples"]), "all expected values equal")
json.dump(man, open(os.path.join(PG, "chapter_code_ch13_v1_4_0.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1) if not os.path.exists(os.path.join(PG, "chapter_code_ch13_v1_4_0.json")) else sys.exit("manifest exists")

# 3 -------------------------------------------------------------------------- Turtle files
ab = rd(os.path.join(RD, "sen0401_ch13_domain_abox_v1_1_0.ttl"))
import rdflib
g = rdflib.Graph(); g.parse(data=ab, format="turtle")
CHX = rdflib.Namespace("http://example.org/sen0401/ch13#")
n_io, bad = 0, []
os.chdir(REPO)
for s in g.subjects(CHX.input, None):
    inp = str(g.value(s, CHX.input)); out = str(g.value(s, CHX.output))
    import ast
    code = inp.replace("sen0401_ch13_lib_v1_0_0", NEW); tree = ast.parse(code); ns = {}
    last = tree.body.pop(); exec(compile(tree, "io", "exec"), ns); got = repr(eval(compile(ast.Expression(last.value), "io", "eval"), ns)); n_io += 1
    if got != out: bad.append((str(s), got[:80], out[:80]))
print("recorded inputs re-run:", n_io, "differences:", len(bad)); assert not bad, bad
ab2 = ab.replace("sen0401_ch13_lib_v1_0_0", NEW)
ab2 = ab2.replace('owl:versionInfo "1.1.0"', 'owl:versionInfo "1.1.1"', 1).replace("ch13/abox/1.1.0>", "ch13/abox/1.1.1>", 1).replace('"sen0401_ch13_abox_v1_1_0"', '"sen0401_ch13_abox_v1_1_1"', 1)
ab2 = ab2.replace('dcterms:modified "2026-10-27"', 'dcterms:modified "2026-11-24"', 1)
assert 'versionInfo "1.1.1"' in ab2 and "lib_v1_0_0" not in ab2
wr(os.path.join(RD, "sen0401_ch13_domain_abox_v1_1_1.ttl"), ab2)
dc = rd("/tmp/doc_embedded.ttl")
dc2 = dc.replace('owl:versionInfo "1.1.0"', 'owl:versionInfo "1.1.1"', 1).replace("ch13/document/1.1.0>", "ch13/document/1.1.1>", 1).replace('"sen0401_ch13_document_v1_1_0"', '"sen0401_ch13_document_v1_1_1"', 1)
assert 'versionInfo "1.1.1"' in dc2
wr(os.path.join(RD, "sen0401_ch13_document_v1_1_1.ttl"), dc2)
# the diagrams ABox is generated by the page build; its embedded text becomes a repository file
H = rd(os.path.join(PG, "sen0401_ch13_page_v9_97_0.html"))
def block(name):
    m = re.search(r'<script type="text/turtle" [^>]*data-name="%s"[^>]*>(.*?)</script>' % re.escape(name), H, re.S); return m.group(1)
wr(os.path.join(RD, "sen0401_ch13_diagrams_abox_v1_0_0.ttl"), block("sen0401_ch13_diagrams_abox_v1_0_0.ttl"))

# 4 -------------------------------------------------------------------------- page 9.98.0
tag = '<script type="application/json" id="data">'; a0 = H.index(tag) + len(tag); b0 = H.index("</script>", a0); data = json.loads(H[a0:b0])
assert data["_version"] == "9.97.0"
cc = data["chaptercode"]; assert len(cc["examples"]) == len(man["examples"])
cc["file"] = "03-materials/ch13/page/chapter_code_ch13_v1_4_0.json"; cc["version"] = "1.4.0"
assert OLD in data["py_boot"]; data["py_boot"] = data["py_boot"].replace(OLD, NEW)
data["py_wheels"] = [{"name": "sen0401_ch13_lib-1.3.0-py3-none-any.whl", "hex": WB.hex()}]
data["_version"] = "9.98.0"
H2 = H[:a0] + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + H[b0:]
H2 = H2.replace('<meta name="version" content="9.97.0">', '<meta name="version" content="9.98.0">')
for o, n in (("sen0401_ch13_domain_abox_v1_1_0", "sen0401_ch13_domain_abox_v1_1_1"), ("sen0401_ch13_document_v1_1_0", "sen0401_ch13_document_v1_1_1"), ("sen0401_materials_v1_4_14", "sen0401_materials_v1_4_15"),
             ("chapter_code_ch13_v1_3_0", "chapter_code_ch13_v1_4_0"), ("sen0401_ch13_lib-1.2.0", "sen0401_ch13_lib-1.3.0")):
    print("  rename x%d: %s" % (H2.count(o), o)); H2 = H2.replace(o, n)
FILES = {"sen0401_materials_v1_4_15.ttl": os.path.join(REPO, "03-materials", "sen0401_materials_v1_4_15.ttl"),
         "sen0401_ch13_domain_abox_v1_1_1.ttl": os.path.join(RD, "sen0401_ch13_domain_abox_v1_1_1.ttl"), "sen0401_ch13_document_v1_1_1.ttl": os.path.join(RD, "sen0401_ch13_document_v1_1_1.ttl")}
def rebuild(m):
    name = re.search(r'data-name="([^"]*)"', m.group(1)).group(1)
    if name in FILES: body = rd(FILES[name])
    else: body = m.group(3)
    return '<script type="text/turtle"%sdata-sha256="%s">%s</script>' % (re.sub(r'data-name="[^"]*"', 'data-name="%s"' % name, m.group(1)), hashlib.sha256(body.encode()).hexdigest()[:16], body)
H2, nb = re.subn(r'<script type="text/turtle"([^>]*)data-sha256="([0-9a-f]+)">(.*?)</script>', rebuild, H2, flags=re.S)
wr(os.path.join(PG, "sen0401_ch13_page_v9_98_0.html"), H2)
dd = os.path.join(T, "ch13-page", "page_data_v9_98_0.json"); assert not os.path.exists(dd); json.dump(data, open(dd, "w", encoding="utf-8"), ensure_ascii=False)
print("page v9_98_0 written, turtle blocks", nb)
