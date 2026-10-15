#!/usr/bin/env python3
"""sen0401_ch08_core_record v1.0.0 - runs the signature behaviours of chapter 8 against a real Bitcoin Core node on regtest and writes
ch08-evidence/core_regtest_record_v1_0_0.json, which sen0401_ch08_verify_v1_0_0.py re-checks OFFLINE (no node needed to re-run the gates).

The node is the official release binary bitcoin-31.1-x86_64-linux-gnu.tar.gz (SHA256 b80d9c3e04da78fb6f0569685673418cf686fadba9042d926d13fb87ff503f9e, matched
against the project's SHA256SUMS), started on regtest with -listen=0 -connect=0 -dnsseed=0 -acceptnonstdtxn=0 (policy on, no peer, no network). Nothing here
touches mainnet. Usage: sen0401_ch08_core_record_v1_0_0.py <bitcoind-bin-dir> <datadir> <rpcport> (the node must already be running with rpcuser u, rpcpassword p)."""
__version__ = "1.0.0"
import base64, collections, hashlib, json, os, struct, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch07_script_lib_v1_0_0 as L
import sen0401_ch08_sig_lib_v1_0_0 as C

PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 18702
OUT = os.path.join(HERE, "ch08-evidence", "core_regtest_record_v1_0_0.json")
AUTH = "Basic " + base64.b64encode(b"u:p").decode()
_id = [0]


def rpc(method, *params, wallet="w"):
    _id[0] += 1
    req = urllib.request.Request("http://127.0.0.1:%d/%s" % (PORT, ("wallet/" + wallet) if wallet else ""), json.dumps(
        {"jsonrpc": "1.0", "id": _id[0], "method": method, "params": list(params)}).encode(), {"Authorization": AUTH, "Content-Type": "text/plain"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=300).read())
    except urllib.error.HTTPError as e:
        r = json.loads(e.read())
    if r.get("error"):
        raise RuntimeError("%s: %s" % (method, r["error"]))
    return r["result"]


def try_rpc(method, *params, wallet="w"):
    try:
        return True, rpc(method, *params, wallet=wallet)
    except RuntimeError as e:
        return False, str(e)


def sat(btc):
    return int(round(float(btc) * 1e8))


REC = {"tool": "sen0401_ch08_core_record", "version": __version__}
REC["node"] = {k: rpc("getnetworkinfo", wallet=None)[k] for k in ("version", "subversion")}
REC["node"]["chain"] = rpc("getblockchaininfo", wallet=None)["chain"]
rpc("createwallet", "w", wallet=None)
mine = rpc("getnewaddress", "", "bech32")
rpc("generatetoaddress", 110, mine)

# ---- 1. one funded set of three outputs per address type ----------------------------------------------------------
TYPES = ["legacy", "p2sh-segwit", "bech32", "bech32m"]
addrs = {t: [rpc("getnewaddress", "", t) for _ in range(3)] for t in TYPES}
rpc("sendmany", "", {a: 1.0 for t in TYPES for a in addrs[t]})
rpc("generatetoaddress", 1, mine)
unspent = rpc("listunspent", 1, 9999, [a for t in TYPES for a in addrs[t]])
by_type = {t: [u for u in unspent if u["address"] in addrs[t]] for t in TYPES}
outs = [rpc("getnewaddress", "", "bech32") for _ in range(3)]

FLAGS = ["ALL", "NONE", "SINGLE", "ALL|ANYONECANPAY", "NONE|ANYONECANPAY", "SINGLE|ANYONECANPAY"]
REC["flags"] = []
for t in TYPES:
    utx = by_type[t]
    raw = rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]} for u in utx], [{outs[0]: 0.5}, {outs[1]: 0.6}, {outs[2]: 0.7}])
    prev = [{"amount_sat": sat(u["amount"]), "spk": u["scriptPubKey"]} for u in utx]
    for f in FLAGS + (["DEFAULT"] if t == "bech32m" else []):
        s = rpc("signrawtransactionwithwallet", raw, [], f)
        REC["flags"].append({"type": t, "sighashtype": f, "complete": s["complete"], "raw_unsigned": raw, "hex": s["hex"], "prevouts": prev})

# ---- 2. the same transaction signed twice: ECDSA and Schnorr determinism ---------------------------------------------
REC["twice"] = {}
for t in ("bech32", "bech32m"):
    utx = by_type[t]
    raw = rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]} for u in utx], [{outs[0]: 0.5}])
    a = rpc("signrawtransactionwithwallet", raw)["hex"]; b = rpc("signrawtransactionwithwallet", raw)["hex"]
    REC["twice"][t] = {"first": a, "second": b, "equal": a == b}

# ---- 3. the length of 300 signatures made by Core (low-R grinding) ---------------------------------------------------
many = [rpc("getnewaddress", "", "bech32") for _ in range(300)]
rpc("sendmany", "", {a: 0.01 for a in many})
rpc("generatetoaddress", 1, mine)
us = rpc("listunspent", 1, 9999, many)
raw = rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]} for u in us], [{outs[0]: 2.9}])
s = rpc("signrawtransactionwithwallet", raw)
tx = L.parse_tx(s["hex"])
lens = [len(w[0]) for w in tx.witness]
REC["lengths"] = {"inputs": len(us), "complete": s["complete"], "sig_lengths": dict(collections.Counter(lens)), "hex": s["hex"],
                  "prevouts": [{"amount_sat": sat(u["amount"]), "spk": u["scriptPubKey"]} for u in us]}

# ---- 4. SIGHASH_SINGLE on an input that has no output of the same index (the legacy quirk) --------------------------
utx = by_type["legacy"][:2]
raw = rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]} for u in utx], [{outs[0]: 1.5}])
ok, res = try_rpc("signrawtransactionwithwallet", raw, [], "SINGLE")
REC["single_bug"] = {"raw_unsigned": raw, "prevouts": [{"amount_sat": sat(u["amount"]), "spk": u["scriptPubKey"]} for u in utx],
                     "result": res if not ok else {"complete": res["complete"], "hex": res["hex"], "errors": res.get("errors")}}
ok2, res2 = try_rpc("signrawtransactionwithwallet", raw, [], "ALL")
REC["single_bug"]["all_complete"] = res2["complete"] if ok2 else str(res2)

# ---- 5. signatures Core did not make: our own keys, our own signatures, Core's verdict --------------------------------
sk = 0x1b1d3a5f9c0e7d62a4b8c1d2e3f40516273849a5b6c7d8e9f0a1b2c3d4e5f607 % L.N
pub = L.pubkey_create(sk)
h160 = L.hash160(pub)
p2pkh_spk = L.p2pkh_script(h160)
p2pkh_addr = L.b58check_encode(111, h160)
xonly = L.schnorr_pubkey(sk)
par, Q = L.taproot_tweak_pubkey(xonly)
p2tr_spk = L.p2tr_script(Q)
p2tr_addr = L.segwit_address("bcrt", 1, Q)
t1 = rpc("sendtoaddress", p2pkh_addr, 1.0); t2 = rpc("sendtoaddress", p2tr_addr, 1.0)
rpc("generatetoaddress", 1, mine)
t3 = rpc("sendtoaddress", p2pkh_addr, 1.0)       # third and fourth funding outputs, kept for the two block tests
t4 = rpc("sendtoaddress", p2pkh_addr, 1.0)
rpc("generatetoaddress", 1, mine)


def find(txid, spk):
    d = rpc("getrawtransaction", txid, True, wallet=None)
    for v in d["vout"]:
        if v["scriptPubKey"]["hex"] == spk.hex():
            return bytes.fromhex(txid)[::-1], v["n"], sat(v["value"])
    raise SystemExit("output not found")


h_a, n_a, amt_a = find(t1, p2pkh_spk); h_b, n_b, amt_b = find(t2, p2tr_spk); h_c, n_c, amt_c = find(t3, p2pkh_spk); h_d, n_d, amt_d = find(t4, p2pkh_spk)
dest = L.p2wpkh_script(L.hash160(L.pubkey_create(7)))


def spend(h, n, amt, sig_script_fn=None, witness=None):
    return L.Tx(2, [(h, n, b"", 0xfffffffd)], [(amt - 10000, dest)], 0, [witness or []])


def der_pad_r(r, s):
    """a DER signature whose R has a needless leading zero byte: valid for the old lax parser, forbidden since BIP66"""
    rb = r.to_bytes((r.bit_length() + 7) // 8, "big"); rb = (b"\x00" if rb[0] < 0x80 else b"\x00\x00") + rb      # one zero byte too many
    sb = s.to_bytes((s.bit_length() + 7) // 8, "big")
    if sb[0] & 0x80: sb = b"\x00" + sb
    body = b"\x02" + bytes([len(rb)]) + rb + b"\x02" + bytes([len(sb)]) + sb
    return b"\x30" + bytes([len(body)]) + body


def legacy_variants(h, n, amt):
    t = spend(h, n, amt)
    digest = L.sighash_legacy(p2pkh_spk, t, 0, 1)
    der = L.ecdsa_sign(sk, digest)
    r, s = L.der_parse_lax(der)
    variants = {}
    def with_sig(sig):
        tt = spend(h, n, amt); tt.vin[0] = (h, n, L.push_data(sig + b"\x01") + L.push_data(pub), 0xfffffffd); return tt.serialize().hex()
    variants["valid_low_s"] = with_sig(der)
    variants["high_s"] = with_sig(L.der_encode(r, L.N - s))
    variants["non_minimal_der"] = with_sig(der_pad_r(r, s))
    variants["signed_other_message"] = with_sig(L.ecdsa_sign(sk, hashlib.sha256(b"another message").digest()))
    return variants, digest.hex(), (r, s)


leg, dg, (r_, s_) = legacy_variants(h_a, n_a, amt_a)
REC["own_ecdsa"] = {"address": p2pkh_addr, "pubkey": pub.hex(), "spk": p2pkh_spk.hex(), "digest": dg, "r": hex(r_), "s": hex(s_), "variants": {}}
for name, hx in leg.items():
    okk, res = try_rpc("testmempoolaccept", [hx], wallet=None)
    REC["own_ecdsa"]["variants"][name] = {"hex": hx, "allowed": res[0]["allowed"] if okk else False, "reject_reason": (res[0].get("reject-reason") if okk else res)}

# consensus acceptance of high-S (policy rejects it, a block may contain it) and refusal of non-DER
hs = legacy_variants(h_c, n_c, amt_c)[0]
okb, resb = try_rpc("generateblock", mine, [hs["high_s"]], wallet=None)
REC["own_ecdsa"]["high_s_in_block"] = {"accepted": okb, "result": resb if okb else str(resb)}
nd = legacy_variants(h_d, n_d, amt_d)[0]["non_minimal_der"]
okn, resn = try_rpc("generateblock", mine, [nd], wallet=None)
REC["own_ecdsa"]["non_der_in_block"] = {"accepted": okn, "result": resn if okn else str(resn)}

# taproot key path: 64 bytes, 65 with 0x01, 65 with 0x00, 63 bytes, flipped bit, signed with hash type 0 but labelled 0x01
spent = [(amt_b, p2tr_spk)]
tp = spend(h_b, n_b, amt_b)
d0 = L.sighash_taproot(tp, 0, 0, spent); d1 = L.sighash_taproot(tp, 0, 1, spent)
tw = L.taproot_tweak_seckey(sk)
sig0 = L.schnorr_sign(tw, d0); sig1 = L.schnorr_sign(tw, d1)
flip = bytearray(sig0); flip[40] ^= 1
tvars = {"default_64": sig0, "explicit_all_65": sig1 + b"\x01", "explicit_zero_65": sig0 + b"\x00", "short_63": sig0[:63],
         "flipped_bit": bytes(flip), "hash_type_mismatch": sig0 + b"\x01"}
REC["own_schnorr"] = {"address": p2tr_addr, "output_key": Q.hex(), "digest_default": d0.hex(), "digest_all": d1.hex(), "variants": {}}
for name, sg in tvars.items():
    t = spend(h_b, n_b, amt_b, witness=[sg]); hx = t.serialize().hex()
    okk, res = try_rpc("testmempoolaccept", [hx], wallet=None)
    REC["own_schnorr"]["variants"][name] = {"sig_hex": sg.hex(), "hex": hx, "allowed": res[0]["allowed"] if okk else False, "reject_reason": (res[0].get("reject-reason") if okk else res)}

# ---- 6. what the node says about itself ----------------------------------------------------------------------------
REC["blocks"] = rpc("getblockcount", wallet=None)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(REC, open(OUT, "w"), indent=1)
print("written", OUT, "flags:", len(REC["flags"]), "sig lengths:", REC["lengths"]["sig_lengths"], "node", REC["node"])
