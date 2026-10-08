#!/usr/bin/env python3
"""Verify the chapter 7 Bitcoin Script library (sen0401_ch07_script_lib_v1_0_0.py) against evidence it did not write.

Run with python 3.14 and the standard library only:  python3.14 sen0401_ch07_verify_v1_0_0.py
It reads Bitcoin Core's own test data from the commit this course pins (05bc2f5, through git in /home/claude/src/bitcoin) and the
transactions saved in ch07-evidence, runs every check, prints one line per check with the measured count, and exits 1 if any
check fails. The checks, in order:
  1. RIPEMD-160 written in python equals the C implementation in hashlib for 131 inputs of 0 to 130 bytes.
  2. BIP 340 test vectors: every verification result and every signing vector of the saved CSV.
  3. Bitcoin Core src/test/data/script_tests.json: every test that carries a script pair (the file also holds comment rows).
  4. Bitcoin Core src/test/data/sighash.json: the legacy signature hash of every vector.
  5. Bitcoin Core src/test/data/bip341_wallet_vectors.json: the seven output keys, addresses and control blocks, and the seven
     key path signatures (hash, tweaked key and signature).
  6. Three landmark mainnet transactions (block 170, the pizza payment, Alice's taproot payment).
  7. The first 599 non-coinbase transactions of block 775,072: every input is checked against the output it spends.
  8. Tampering: one flipped bit in a signature, or in the amount of a segwit input, must make a real input fail."""
__version__ = "1.0.0"
import sys, os, json, csv, hashlib, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch07_script_lib_v1_0_0 as L
EV = os.path.join(HERE, "ch07-evidence")
CORE, COMMIT = "/home/claude/src/bitcoin", "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
ERRNAME = {"SIG_NULLFAIL": "NULLFAIL"}   # Core's own table maps this one enum name to a shorter word in the json files
RESULTS = []

def git(path): return subprocess.run(["git", "-C", CORE, "show", COMMIT + ":" + path], capture_output=True, text=True, check=True).stdout
def report(name, ok, total, extra=""):
    RESULTS.append((name, ok, total))
    print("%-4s %-58s %5d / %-5d %s" % ("PASS" if ok == total else "FAIL", name, ok, total, extra))

def check_ripemd():
    ok = 0
    for n in range(131):
        d = hashlib.sha256(b"x%d" % n).digest() * 5; d = d[:n]
        ok += L.ripemd160_pure(d) == hashlib.new("ripemd160", d).digest()
    report("RIPEMD-160 (python) equals hashlib", ok, 131)

def check_bip340():
    rows = list(csv.DictReader(open(os.path.join(EV, "bip-0340_test-vectors.csv"))))
    ok = signs = nsign = 0
    for r in rows:
        try: v = L.schnorr_verify(bytes.fromhex(r["public key"]), bytes.fromhex(r["message"]), bytes.fromhex(r["signature"]))
        except Exception: v = False
        ok += v == (r["verification result"] == "TRUE")
        if r["secret key"]:
            nsign += 1; s = int(r["secret key"], 16)
            signs += (L.schnorr_pubkey(s).hex().upper() == r["public key"] and
                      L.schnorr_sign(s, bytes.fromhex(r["message"]), bytes.fromhex(r["aux_rand"])).hex().upper() == r["signature"])
    report("BIP 340 vectors: verification results", ok, len(rows)); report("BIP 340 vectors: public key and signature produced", signs, nsign)

def parse_witness_item(x, st):
    if x.startswith("#SCRIPT#"): st["leaf"] = L.assemble(x[8:].strip()); return st["leaf"]
    if x == "#CONTROLBLOCK#":
        gx = L.G[0].to_bytes(32, "big"); par, q = L.taproot_tweak_pubkey(gx, L.tap_leaf_hash(0xc0, st["leaf"]))
        st["out"] = q; return bytes([0xc0 | par]) + gx
    return bytes.fromhex(x)

def check_script_tests():
    data = json.loads(git("src/test/data/script_tests.json"))
    n = ok = wit_n = wit_ok = tap_n = tap_ok = 0; bad = []
    for e in data:
        i, wit, amount, st = 0, [], 0, {}
        if e and isinstance(e[0], list):
            wit = [parse_witness_item(x, st) for x in e[0][:-1]]; amount = int(round(e[0][-1] * 1e8)); i = 1
        if len(e) < i + 4: continue
        ss, spk, fl, exp = e[i:i + 4]
        if spk == "0x51 0x20 #TAPROOTOUTPUT#": spk = "0x51 0x20 0x" + st["out"].hex()
        flags = [f for f in fl.split(",") if f and f != "NONE"]
        try: got = L.run(ss, spk, flags, wit, amount=amount)
        except Exception as ex: got = "EXCEPTION " + type(ex).__name__
        got = ERRNAME.get(got, got)
        good = got == exp
        n += 1; ok += good
        if i: wit_n += 1; wit_ok += good
        if "TAPROOT" in flags and i: tap_n += 1; tap_ok += good
        if not good: bad.append((exp, got, ss[:40], spk[:40]))
    report("Core script_tests.json: all script tests", ok, n, "(file has %d rows incl. comments)" % len(data))
    report("  of which with a witness", wit_ok, wit_n); report("  of which tapscript auto-generated outputs", tap_ok, tap_n)
    for b in bad[:5]: print("     ", b)
    return n

def check_sighash():
    d = json.loads(git("src/test/data/sighash.json")); n = ok = 0
    for e in d:
        if len(e) != 5: continue
        n += 1
        h = L.sighash_legacy(bytes.fromhex(e[1]), L.parse_tx(e[0]), e[2], e[3] & 0xffffffff)
        ok += h[::-1].hex() == e[4]
    report("Core sighash.json: legacy signature hashes", ok, n)

def _walk(t):
    if isinstance(t, dict): return L.tap_leaf_hash(t["leafVersion"], bytes.fromhex(t["script"])), [(t["id"], [], t["leafVersion"])]
    a, la = _walk(t[0]); b, lb = _walk(t[1])
    return L.tap_branch_hash(a, b), [(i, p + [b], v) for i, p, v in la] + [(i, p + [a], v) for i, p, v in lb]

def check_bip341():
    d = json.loads(git("src/test/data/bip341_wallet_vectors.json")); good = 0
    for v in d["scriptPubKey"]:
        g = v["given"]; ip = bytes.fromhex(g["internalPubkey"])
        root, paths = (b"", []) if g["scriptTree"] is None else _walk(g["scriptTree"])
        par, q = L.taproot_tweak_pubkey(ip, root); spk = L.p2tr_script(q)
        cbs = sorted(bytes([ver | par]) + ip + b"".join(p) for _, p, ver in paths)
        good += (spk.hex() == v["expected"]["scriptPubKey"] and L.script_to_address(spk) == v["expected"]["bip350Address"]
                 and sorted(bytes.fromhex(x) for x in v["expected"].get("scriptPathControlBlocks", [])) == cbs)
    report("BIP 341 vectors: output key, address, control blocks", good, len(d["scriptPubKey"]))
    k = d["keyPathSpending"][0]; tx = L.parse_tx(k["given"]["rawUnsignedTx"])
    spent = [(u["amountSats"], bytes.fromhex(u["scriptPubKey"])) for u in k["given"]["utxosSpent"]]
    hs = sg = 0
    for i in k["inputSpending"]:
        g = i["given"]; h = L.sighash_taproot(tx, g["txinIndex"], g["hashType"], spent); hs += h.hex() == i["intermediary"]["sigHash"]
        tw = L.taproot_tweak_seckey(int(g["internalPrivkey"], 16), bytes.fromhex(g["merkleRoot"]) if g["merkleRoot"] else b"")
        sig = L.schnorr_sign(tw, h, b"\0" * 32) + (bytes([g["hashType"]]) if g["hashType"] else b"")
        sg += sig.hex() == i["expected"]["witness"][0]
    report("BIP 341 vectors: signature hash", hs, len(k["inputSpending"])); report("BIP 341 vectors: key path signature produced", sg, len(k["inputSpending"]))

def load_records(name): return json.load(open(os.path.join(EV, name)))["transactions"]
def inputs_of(rec):
    tx = L.parse_tx(rec["hex"]); spent = [(a, bytes.fromhex(s)) for a, s in rec["spent"]]
    return tx, spent

def check_landmarks():
    ok = n = 0
    for r in load_records("mainnet_landmarks_v1_0_0.json"):
        tx, spent = inputs_of(r)
        for i in range(len(tx.vin)):
            n += 1; ok += tx.txid() == r["txid"] and L.verify_input(tx, i, spent, L.MAINNET_FLAGS) == "OK"
    report("landmark mainnet transactions: inputs accepted", ok, n)

def check_census():
    recs = load_records("mainnet_block775072_census_v1_0_0.json"); kinds = collections.Counter(); ok = n = idok = std_ok = 0
    for r in recs:
        tx, spent = inputs_of(r); idok += tx.txid() == r["txid"]
        for i in range(len(tx.vin)):
            n += 1; k = L.classify(spent[i][1])[0]; res = L.verify_input(tx, i, spent, L.MAINNET_FLAGS)
            kinds[k] += res == "OK"; ok += res == "OK"
            std_ok += L.verify_input(tx, i, spent, L.STANDARD_FLAGS) == "OK"
    report("block 775,072: transaction ids recomputed", idok, len(recs))
    report("block 775,072: inputs accepted under today's consensus rules", ok, n, dict(kinds))
    report("block 775,072: inputs also accepted under every policy flag the library implements", std_ok, n)

def check_tamper():
    ok = n = 0; seen = set(); results = {}
    for r in load_records("mainnet_block775072_census_v1_0_0.json"):
        tx, spent = inputs_of(r)
        for i in range(len(tx.vin)):
            k = L.classify(spent[i][1])[0]
            if k in seen or k not in ("pubkeyhash", "witness_v0_keyhash", "witness_v0_scripthash", "witness_v1_taproot", "scripthash"): continue
            seen.add(k); n += 1
            # flip one bit of the signature: the first push of the scriptSig (legacy) or the first witness item (segwit)
            if tx.witness[i]:
                w = list(tx.witness[i]); w0 = bytearray(w[0 if k != "witness_v0_scripthash" else 1]); w0[5] ^= 1
                w[0 if k != "witness_v0_scripthash" else 1] = bytes(w0); tx.witness[i] = w
            else:
                ss = bytearray(tx.vin[i][2]); ss[8] ^= 1; tx.vin[i] = (tx.vin[i][0], tx.vin[i][1], bytes(ss), tx.vin[i][3])
            res = L.verify_input(tx, i, spent, L.MAINNET_FLAGS); results[k] = res; ok += res != "OK"
    # a segwit input whose amount is changed: the BIP 143 and BIP 341 hashes commit to the amount
    for r in load_records("mainnet_block775072_census_v1_0_0.json"):
        tx, spent = inputs_of(r)
        if L.classify(spent[0][1])[0] == "witness_v0_keyhash":
            s2 = list(spent); s2[0] = (spent[0][0] + 1, spent[0][1]); res = L.verify_input(tx, 0, s2, L.MAINNET_FLAGS)
            n += 1; ok += res != "OK"; results["amount+1 sat (p2wpkh)"] = res; break
    report("tampered inputs are rejected", ok, n, results)

if __name__ == "__main__":
    for f in (check_ripemd, check_bip340, check_script_tests, check_sighash, check_bip341, check_landmarks, check_census, check_tamper): f()
    bad = [r for r in RESULTS if r[1] != r[2]]
    print("\n%d checks, %d failed" % (len(RESULTS), len(bad)))
    sys.exit(1 if bad else 0)
