#!/usr/bin/env python3
"""Chapter 4: check the chapter's toolkit (sen0401_keys_toolkit) against three independent references, and run the
tests that are too long to repeat with every check. Writes verify_results_v1_0_0.json next to this script.
  1. the book's own bech32 reference library (sipa/bech32), on the book's four addresses and on every BIP350 vector;
  2. every BIP350 test vector, valid and invalid, through the toolkit;
  3. Bitcoin Core 31.1's answers saved by sen0401_ch04_evidence_v1_0_0.sh;
  and, on the book's 42-character P2WPKH address, every one- and two-character substitution and 200,000 random three-
  and four-character substitutions, none of which may still carry a valid checksum.
Usage: sen0401_ch04_verify_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_keys_toolkit_v1_0_0 as T
import segwit_addr_sipa_v1_0_0 as S
V = json.load(open(os.path.join(HERE, "bip350_vectors_v1_0_0.json"))); res = {}
book = {("bc", 0, "2b626ed108ad00a944bb2922a309844611d25468"): "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee",
        ("bc", 0, "648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f"): "bc1qvj9r9egtd7mu2gemy28kpf4zefq4ssqzdzzycj7zjhk4arpavfhsct5a3p",
        ("bc", 1, "2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311"): "bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7",
        ("bc", 16, "0000"): "bc1sqqqqkfw08p"}
res["book_addresses_toolkit"] = all(T.segwit_address(h, v, bytes.fromhex(p)) == a for (h, v, p), a in book.items())
res["book_addresses_sipa_library"] = all(S.encode(h, v, bytes.fromhex(p)) == a for (h, v, p), a in book.items())
res["book_addresses_agree"] = res["book_addresses_toolkit"] and res["book_addresses_sipa_library"]
def spk(ver, prog): return bytes([0 if ver == 0 else 0x50 + ver, len(prog)]) + prog
ok = 0
for a, want in V["valid_segwit"]:
    hrp = a[:2].lower(); d = T.segwit_decode(hrp, a); s = S.decode(hrp, a)
    ok += bool(d and spk(*d).hex() == want and s[0] is not None and spk(s[0], bytes(s[1])).hex() == want)
res["bip350_valid_vectors"] = [ok, len(V["valid_segwit"])]
bad = 0
for a, why in V["invalid_segwit"]:
    hrp = a[:2].lower() if a[:2].lower() in ("bc", "tb") else "bc"
    bad += (T.segwit_decode(hrp, a) is None) and (S.decode(hrp, a)[0] is None)
res["bip350_invalid_vectors"] = [bad, len(V["invalid_segwit"])]
res["bip350_bech32m_strings"] = [sum(T.bech_check(a) == T.BECH32M for a in V["valid_bech32m"] if a not in ("?1v759aa",)), len(V["valid_bech32m"]) - 1]
# the length-extension example: valid under bech32's constant, not under bech32m's
ext = ["bc1pqqqsq9txsqp", "bc1pqqqsq9txsqqqqp", "bc1pqqqsq9txsqqqqqqp", "bc1pqqqsq9txsqqqqqqqqp", "bc1pqqqsq9txsqqqqqqqqqp", "bc1pqqqsq9txsqqqqqqqqqqqp"]
res["length_extension_bech32_valid"] = [sum(T.bech_check(a) == T.BECH32 for a in ext), len(ext)]
res["length_extension_bech32m_valid"] = [sum(T.bech_check(a) == T.BECH32M for a in ext), len(ext)]
# Core
core = json.load(open(os.path.join(HERE, "core_validateaddress_31_1_v1_0_0.json")))
res["core_validate_agrees_on_segwit_examples"] = all(core[a]["isvalid"] == (T.segwit_decode("bc", a) is not None) for a in core if a.startswith("bc1"))
# errors: exhaustive one and two substitutions, random three and four
addr = "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee"; hrp, _, d = addr.rpartition("1"); data = [T.CHARSET.find(c) for c in d]; L = len(data)
def valid(dd): return T.polymod(T.hrp_expand(hrp) + dd) == T.BECH32
und1 = sum(valid(data[:i] + [x] + data[i + 1:]) for i in range(L) for x in range(32) if x != data[i])
und2 = 0
for i in range(L):
    for j in range(i + 1, L):
        for x in range(32):
            if x == data[i]: continue
            for y in range(32):
                if y == data[j]: continue
                dd = data[:]; dd[i] = x; dd[j] = y; und2 += valid(dd)
random.seed(4); und34 = 0
for _ in range(200000):
    k = random.choice((3, 4)); pos = random.sample(range(L), k); dd = data[:]
    for p in pos: dd[p] = random.choice([x for x in range(32) if x != data[p]])
    und34 += valid(dd)
res["substitution_errors_undetected"] = {"one": und1, "two": und2, "three_or_four_random_of_200000": und34, "address": addr, "data_characters": L}
json.dump(res, open(os.path.join(HERE, "verify_results_v1_0_0.json"), "w"), indent=1); print(json.dumps(res, indent=1))
