#!/usr/bin/env python3
"""sen0401_ch03_core_pointers v1.0.0: Chapter 3 gets its pointers to Bitcoin Core, as new files beside the released ones (nothing is edited in place).
Each pointer was read in the source tree of Bitcoin Core, commit 079437c. Behaviour of the library is unchanged.
Writes: library sen0401_ch03_core_lib_v1_1_0.py and its wheel (assets, 1.1.0); deck v3_3_1 (the five code slides import the new module name);
chapter code v1_2_1; page v9_78_0. Refuses to overwrite. Usage: python3 sen0401_ch03_core_pointers_v1_0_0.py"""
import os, re, json, zipfile, hashlib
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); CH = os.path.join(R, "03-materials", "ch03")
OLD, NEW = "sen0401_ch03_core_lib_v1_0_0", "sen0401_ch03_core_lib_v1_1_0"
def new_file(p):
    assert not os.path.exists(p), "exists: " + p
    return p
# ---- library and wheel
old = open(os.path.join(H, OLD + ".py"), encoding="utf-8").read()
m = re.match(r'"""(.*?)"""\n__version__ = "1.0.0"\n', old, re.S); assert m
doc = m.group(1).replace("sen0401_ch03_core_lib v1.0.0", "sen0401_ch03_core_lib v1.1.0", 1)
doc += """

Relation to Bitcoin Core (v1.1.0; each pointer was read in the source tree of Bitcoin Core, commit 079437c; behaviour of this file is unchanged from v1.0.0):
* parse_conf(): ArgsManager::ReadConfigStream in src/common/config.cpp reads the lines of bitcoin.conf.
* cache_split(): the struct CacheSizes in src/kernel/caches.h gives an eighth of the total (at most MAX_BLOCK_DB_CACHE, 2 MiB) to the block index database, half of the rest (at most MAX_COINS_DB_CACHE, 8 MiB) to the chain state database, and the remainder to the coins cache.
* check_options(): the refusal 'Prune mode is incompatible with -txindex.' is raised in src/init.cpp; MIN_DISK_SPACE_FOR_BLOCK_FILES, 550 MiB, the least automatic pruning target, is in src/validation.h.
* clean(), alert_command(): SanitizeString with SAFE_CHARS_DEFAULT in src/util/strencodings.cpp keeps the characters of SAFE; the alert text is cleaned that way before the -alertnotify command runs, in AlertNotify in src/node/kernel_notifications.cpp.
* the -maxmempool default of MAXMEMPOOL_MB is DEFAULT_MAX_MEMPOOL_SIZE_MB in src/kernel/mempool_options.h; the 5 MB of blocks-only mode is stated in doc/reduce-memory.md.
* rpc_body(): JSONRPCRequestObj in src/rpc/request.cpp builds the request object.
* rpcauth(): the helper share/rpcauth/rpcauth.py writes the salted HMAC-SHA256; the server checks it with CHMAC_SHA256 and TimingResistantEqual in CheckUserAuthorized, src/httprpc.cpp.
* hash256(): Hash() in src/hash.h is the double SHA256.
* split_witness(), txid(), wtxid(): CTransaction::ComputeHash and CTransaction::ComputeWitnessHash in src/primitives/transaction.cpp hash the serialisation without and with the witness.
* header(), header_fields(): CBlockHeader in src/primitives/block.h (80 bytes); its hash is CBlockHeader::GetHash in src/primitives/block.cpp.
* merkle(): ComputeMerkleRoot in src/consensus/merkle.cpp.
* version_key(), age_days() and the registry data (TOOLKITS) have no counterpart in Bitcoin Core; they serve the chapter's tables."""
new = '"""' + doc + '"""\n__version__ = "1.1.0"\n' + old[m.end():]
f = new_file(os.path.join(H, NEW + ".py")); open(f, "w", encoding="utf-8").write(new)
w = new_file(os.path.join(CH, "assets", "sen0401_ch03_lib-1.1.0-py3-none-any.whl"))
with zipfile.ZipFile(w, "w", zipfile.ZIP_DEFLATED) as z:
    def put(n, b):
        zi = zipfile.ZipInfo(n, (2026, 11, 25, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; z.writestr(zi, b)
    put(NEW + ".py", new.encode("utf-8"))
    put("sen0401_ch03_lib-1.1.0.dist-info/METADATA", b"Metadata-Version: 2.1\nName: sen0401-ch03-lib\nVersion: 1.1.0\nSummary: The chapter 3 (Bitcoin Core) library of the SEN0401 course.\n")
    put("sen0401_ch03_lib-1.1.0.dist-info/WHEEL", b"Wheel-Version: 1.0\nGenerator: sen0401_ch03_core_pointers_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
# ---- deck v3_3_1: only the module name in the five code slides changes
src = os.path.join(CH, "SEN0401_Ch03_BitcoinCore_3e_v3_3_0.pptx"); dst = new_file(os.path.join(CH, "SEN0401_Ch03_BitcoinCore_3e_v3_3_1.pptx"))
zin = zipfile.ZipFile(src); n = 0
with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zin.infolist():
        b = zin.read(it.filename)
        if it.filename.endswith(".xml") and OLD.encode() in b:
            n += b.count(OLD.encode()); b = b.replace(OLD.encode(), NEW.encode())
        zo.writestr(it, b)
assert n == 5, n
# ---- chapter code v1_2_1
man = json.load(open(os.path.join(CH, "page", "chapter_code_ch03_v1_2_0.json"), encoding="utf-8"))
s = json.dumps(man, ensure_ascii=False).replace(OLD, NEW); man = json.loads(s)
man["manifest"] = "chapter_code_ch03_v1_2_1"; man["deck"] = "SEN0401_Ch03_BitcoinCore_3e_v3_3_1.pptx"; man["deck_version"] = "3.3.1"
man["library"]["file"] = "08-tooling/" + NEW + ".py"; man["library"]["sha256"] = hashlib.sha256(new.encode("utf-8")).hexdigest()
mf = new_file(os.path.join(CH, "page", "chapter_code_ch03_v1_2_1.json")); json.dump(man, open(mf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---- page v9_78_0
raw = open(os.path.join(CH, "page", "sen0401_ch03_page_v9_77_0.html"), encoding="utf-8", newline="").read()
DATA = re.compile(r'(<script type="application/json" id="data">)(.*?)(</script>)', re.S); mm = DATA.search(raw); D = json.loads(mm.group(2))
D["py_wheels"] = [{"name": os.path.basename(w), "hex": open(w, "rb").read().hex()}]
D["chaptercode"] = {"file": "03-materials/ch03/page/chapter_code_ch03_v1_2_1.json", "version": "1.2.1",
                    "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in man["examples"]]}
D["_version"] = "9.78.0"
js = json.dumps(D, ensure_ascii=False, separators=(", ", ": ")).replace("</", "<\\/")
out = raw[:mm.start(2)] + js + raw[mm.end(2):]
out = out.replace(OLD, NEW)
pf = new_file(os.path.join(CH, "page", "sen0401_ch03_page_v9_78_0.html")); open(pf, "w", encoding="utf-8", newline="").write(out)
print("wrote", f, w, dst, mf, pf, "| module occurrences left in page:", out.count(OLD))
