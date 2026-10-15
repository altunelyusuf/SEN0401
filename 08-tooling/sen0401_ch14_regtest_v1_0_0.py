#!/usr/bin/env python3
"""SEN0401 chapter 14 (Second-Layer Applications): the regtest run. One private chain of Bitcoin Core 31.1 (the release binary of bitcoincore.org) and, for the Lightning part, nodes of lnd 0.21.3-beta
(the release binary of Lightning Labs, sha256 compared with its manifest) in temporary data directories. Everything is recorded in ch14-evidence/regtest_run_v1_0_0.json.
Phases (script level, with the Python toolkit sen0401_ch14_tx and the node as judge):
  c1 the building blocks: double spend, accounting, non-expiration, proof of existence in OP_RETURN, a Lighthouse pledge with SIGHASH_ALL|ANYONECANPAY
  c2 pay to contract and a two-step colored coin whose history a third party validates on the client side
  c3 the one-way channel of Emma and Fabian: funding, refund, commitments with decreasing timelocks, the cheat that fails
  c4 the asymmetric revocable commitment of Hitesh and Irene: delayed output after 1,000 blocks, revocation key, half of a key
  c5 the hash time lock contract of the book: preimage, wrong preimage, refund before and after the timeout, redemption by anyone
  c6 an anchor-based commitment: a version 3 parent without fee and a pay-to-anchor output, paid for by a child in a package
  l1..l6 five lnd nodes in a line (Alice, Bob, Carol, Diana, Eric) with the fees of the book, a payment of 1 bitcoin, hold invoices, a cooperative close; and two nodes (Hitesh, Irene)
  where Irene broadcasts a revoked state and Hitesh takes the whole channel
  b  the release archive of lnd against its manifest
Nothing here touches the public network; -connect=0 for the chain, 127.0.0.1 for the Lightning nodes. One run, one record: hashes, keys and timings differ on a rerun.
Usage: sen0401_ch14_regtest_v1_0_0.py [out.json] [--only c1,c2] [--keep]   Environment: BITCOIN_BIN, LND_DIR, TMPDIR."""
__version__ = "1.0.0"
import hashlib, json, os, shutil, subprocess, sys, tempfile, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch14_crypto_v1_0_0 as C
import sen0401_ch14_tx_v1_0_0 as T

BIN = os.environ.get("BITCOIN_BIN", "/home/claude/core31/bitcoin-31.1/bin")
LNDD = os.environ.get("LND_DIR", "/home/claude/ln21/lnd-linux-amd64-v0.21.3-beta")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = [a for a in args if a.endswith(".json")]
OUT = OUT[0] if OUT else os.path.join(HERE, "ch14-evidence", "regtest_run_v1_0_0.json")
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
TMP = tempfile.mkdtemp(prefix="ch14_regtest_", dir=os.environ.get("TMPDIR"))
R = {"_version": __version__, "phase": {}, "errors": {}}
T0 = time.time()
BTC_RPC, BTC_PORT, ZMQB, ZMQT = 18700, 18701, 28332, 28333


def sh(c, **k):
    return subprocess.run(c, capture_output=True, text=True, **k)


class RPCError(Exception):
    pass


class BTC:
    def __init__(self):
        self.dd = os.path.join(TMP, "btc")
        os.makedirs(self.dd)
        open(os.path.join(self.dd, "bitcoin.conf"), "w").write(
            "regtest=1\n[regtest]\nrpcuser=u\nrpcpassword=p\nrpcport=%d\nport=%d\nserver=1\nzmqpubrawblock=tcp://127.0.0.1:%d\nzmqpubrawtx=tcp://127.0.0.1:%d\nfallbackfee=0.0002\n"
            "dnsseed=0\nlisten=0\ntxindex=1\ndiscover=0\nconnect=0\n" % (BTC_RPC, BTC_PORT, ZMQB, ZMQT))
        r = sh([BIN + "/bitcoind", "-datadir=" + self.dd, "-daemon"])
        assert r.returncode == 0, r.stdout + r.stderr
        for _ in range(200):
            try:
                self.rpc("getblockcount")
                break
            except RPCError:
                time.sleep(0.3)
        self.addr = None

    def rpc(self, method, *a, wallet=None):
        c = [BIN + "/bitcoin-cli", "-datadir=" + self.dd, "-rpcclienttimeout=900", "-stdin"] + (["-rpcwallet=" + wallet] if wallet else []) + [method]
        r = sh(c, input="\n".join(x if isinstance(x, str) else json.dumps(x) for x in a))
        if r.returncode:
            raise RPCError(" ".join((r.stdout + r.stderr).split()))
        o = r.stdout.strip()
        try:
            return json.loads(o)
        except Exception:
            return o

    def attempt(self, method, *a, **kw):
        try:
            return {"ok": self.rpc(method, *a, **kw)}
        except RPCError as e:
            return {"error": str(e)}

    def stop(self):
        try:
            self.rpc("stop")
        except RPCError:
            pass
        time.sleep(3)

    # ---- helpers on the wallet "miner"
    def mine(self, n=1):
        out = []
        while n > 0:
            k = min(n, 500)
            out += self.rpc("generatetoaddress", k, self.addr)
            n -= k
        return out

    def height(self):
        return self.rpc("getblockcount")

    def fund(self, spk, sat):
        """pays sat to the script spk from the wallet, returns (txid, vout)"""
        addr = T.segwit_addr(spk[2:]) if len(spk) in (22, 34) and spk[0] == 0 else None
        txid = self.rpc("sendtoaddress", addr, "%.8f" % (sat / 1e8), wallet="miner")
        tx = self.rpc("getrawtransaction", txid, True)
        for o in tx["vout"]:
            if o["scriptPubKey"]["hex"] == spk.hex():
                return txid, o["n"]
        raise RuntimeError("output not found")

    def verdict(self, tx):
        r = self.rpc("testmempoolaccept", [tx.hex()])[0]
        return {"allowed": r["allowed"], "reason": r.get("reject-reason")}

    def send(self, tx):
        return self.rpc("sendrawtransaction", tx.hex(), 0)


B = None
sk = lambda label: int.from_bytes(C.sha256(label.encode()), "big") % C.N
BTCF = lambda sat: "%.8f" % (sat / 1e8)


def phase(name):
    def deco(f):
        def run():
            if ONLY and name not in ONLY:
                return
            t = time.time()
            try:
                R[name] = f()
            except BaseException as e:
                R["errors"][name] = "".join(traceback.format_exception_only(type(e), e)).strip()[:600]
                traceback.print_exc()
            R["phase"][name] = round(time.time() - t, 1)
            print("phase", name, R["phase"][name], "s", "ERROR" if name in R["errors"] else "ok", flush=True)
            save()
        run.phase = name
        return run
    return deco


def save():
    R["wall_s"] = round(time.time() - T0, 1)
    json.dump(R, open(OUT, "w"), indent=1, sort_keys=True, default=str)


# ================================================================================================ c1 the building blocks
@phase("c1")
def c1():
    o = {}
    w = "miner"
    unspent = [u for u in B.rpc("listunspent", 1, 9999999, [], True, wallet=w) if u["amount"] >= 1 and u["spendable"]]
    u = unspent[0]
    a1, a2 = B.rpc("getnewaddress", wallet=w), B.rpc("getnewaddress", wallet=w)
    mk = lambda addr, amt: B.rpc("signrawtransactionwithwallet", B.rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]}], {addr: amt}), wallet=w)["hex"]
    t1, t2lo, t2hi = mk(a1, round(float(u["amount"]) - 0.001, 8)), mk(a2, round(float(u["amount"]) - 0.0005, 8)), mk(a2, round(float(u["amount"]) - 0.002, 8))
    id1 = B.rpc("sendrawtransaction", t1)
    lo = B.attempt("sendrawtransaction", t2lo)
    hi = B.attempt("sendrawtransaction", t2hi)
    first_still = "ok" in B.attempt("getmempoolentry", id1)
    B.mine(1)
    again = B.attempt("sendrawtransaction", t1)
    o["double_spend"] = {"first_accepted": True, "second_lower_fee": lo.get("error", "accepted"), "second_higher_fee": "replaced the first" if ("ok" in hi and not first_still) else hi.get("error", "accepted beside the first"),
                         "first_still_in_mempool": first_still, "first_after_block": again.get("error", "accepted"), "fee_first_sat": 100000, "fee_lower_sat": 50000, "fee_higher_sat": 200000}
    # accounting: outputs larger than inputs
    u2 = unspent[1]
    big = B.rpc("signrawtransactionwithwallet", B.rpc("createrawtransaction", [{"txid": u2["txid"], "vout": u2["vout"]}], {a1: round(float(u2["amount"]) + 1, 8)}), wallet=w)["hex"]
    o["outputs_exceed_inputs"] = B.rpc("testmempoolaccept", [big])[0].get("reject-reason")
    # non-expiration: sign now, wait 150 blocks, then submit
    u3 = unspent[2]
    held = B.rpc("signrawtransactionwithwallet", B.rpc("createrawtransaction", [{"txid": u3["txid"], "vout": u3["vout"]}], {a2: round(float(u3["amount"]) - 0.001, 8)}), wallet=w)["hex"]
    h0 = B.height()
    B.mine(150)
    r = B.rpc("testmempoolaccept", [held])[0]
    o["non_expiration"] = {"signed_at_height": h0, "tested_at_height": B.height(), "allowed": r["allowed"]}
    # proof of existence: the hash of a document in an OP_RETURN output
    doc = b"SEN0401 Special Topics: Blockchain, chapter 14, proof of existence"
    dig = hashlib.sha256(doc).hexdigest()
    raw = B.rpc("createrawtransaction", [], [{"data": dig}])
    fr = B.rpc("fundrawtransaction", raw, wallet=w)
    sg = B.rpc("signrawtransactionwithwallet", fr["hex"], wallet=w)["hex"]
    pid = B.rpc("sendrawtransaction", sg)
    bh = B.mine(1)[0]
    blk = B.rpc("getblock", bh)
    tx = B.rpc("getrawtransaction", pid, True)
    nd = [x for x in tx["vout"] if x["scriptPubKey"]["type"] == "nulldata"][0]
    o["proof_of_existence"] = {"sha256": dig, "txid": pid, "block_height": blk["height"], "block_time": blk["time"], "nulldata_asm": nd["scriptPubKey"]["asm"], "value": nd["value"],
                              "contains_hash": dig in nd["scriptPubKey"]["hex"]}
    # Lighthouse: two pledges, each signed SIGHASH_ALL|ANYONECANPAY over a fixed 2-bitcoin output
    pa, pb = sk("lighthouse-pledger-a"), sk("lighthouse-pledger-b")
    va, vb = 100_050_000, 100_000_000
    ta, ia = B.fund(T.p2wpkh(C.pub(pa)), va)
    tb, ib = B.fund(T.p2wpkh(C.pub(pb)), vb)
    B.mine(1)
    goal = T.p2wpkh(C.pub(sk("lighthouse-project")))

    def build(inputs, out_sat=200_000_000, htype=T.SIGHASH_ALL | T.ANYONECANPAY, order=None):
        tx = T.Tx(2)
        for t_, i_, v_, s_ in inputs:
            tx.add_in(t_, i_)
        tx.add_out(out_sat, goal)
        return tx
    full = build([(ta, ia, va, pa), (tb, ib, vb, pb)])
    full.sign_p2wpkh(0, pa, va, T.SIGHASH_ALL | T.ANYONECANPAY)
    full.sign_p2wpkh(1, pb, vb, T.SIGHASH_ALL | T.ANYONECANPAY)
    only_a = build([(ta, ia, va, pa)])
    only_a.sign_p2wpkh(0, pa, va, T.SIGHASH_ALL | T.ANYONECANPAY)
    # the same pledge of A but signed SIGHASH_ALL: B's input cannot be added afterwards
    plain = build([(ta, ia, va, pa)])
    plain.sign_p2wpkh(0, pa, va, T.SIGHASH_ALL)
    plain.add_in(tb, ib)
    plain.sign_p2wpkh(1, pb, vb, T.SIGHASH_ALL)
    # tamper: the recipient changed after the pledges were signed
    tam = build([(ta, ia, va, pa), (tb, ib, vb, pb)])
    tam.sign_p2wpkh(0, pa, va, T.SIGHASH_ALL | T.ANYONECANPAY)
    tam.sign_p2wpkh(1, pb, vb, T.SIGHASH_ALL | T.ANYONECANPAY)
    tam.vout[0][1] = T.p2wpkh(C.pub(sk("thief")))
    o["lighthouse"] = {"pledge_a_sat": va, "pledge_b_sat": vb, "goal_sat": 200_000_000, "only_a": B.verdict(only_a), "both": B.verdict(full), "a_signed_all_then_b_added": B.verdict(plain), "output_changed": B.verdict(tam)}
    txid = B.send(full)
    B.mine(1)
    o["lighthouse"]["confirmed_txid"] = txid
    o["lighthouse"]["fee_sat"] = va + vb - 200_000_000
    return o


# ================================================================================================ c2 pay to contract and client-side validation
def p2c_tweak(pubkey, contract):
    return int.from_bytes(C.sha256(pubkey + contract), "big") % C.N


def p2c_key(secret, contract):
    """the tweaked key: (secret + t) with t = SHA256(P || contract); and its public key Q = P + tG"""
    P_ = C.pub(secret)
    t = p2c_tweak(P_, contract)
    return (secret + t) % C.N, C.ser(C.padd(C.parse(P_), C.pmul(t)))


@phase("c2")
def c2():
    o = {}
    contract = b"Bob sells Alice 10 shares of ACME for 1 coin; delivery within 30 days"
    a = sk("p2c-alice")
    tw_secret, Q = p2c_key(a, contract)
    spk = T.p2wpkh(Q)
    txid, vout = B.fund(spk, 1_000_000)
    B.mine(1)
    dest = T.p2wpkh(C.pub(sk("p2c-dest")))

    def spend(secret, pubkey):
        tx = T.Tx(2)
        tx.add_in(txid, vout)
        tx.add_out(1_000_000 - 1000, dest)
        sc = b"\x76\xa9\x14" + C.hash160(pubkey) + b"\x88\xac"
        tx.vin[0][3] = [tx.sig(0, secret, sc, 1_000_000), pubkey]
        return tx
    o["p2c"] = {"contract_len": len(contract), "plain_pubkey": C.pub(a).hex(), "tweaked_pubkey": Q.hex(), "tweak_hex": "%064x" % p2c_tweak(C.pub(a), contract),
                "output_script_hex": spk.hex(), "same_as_plain_p2wpkh": spk == T.p2wpkh(C.pub(a)),
                "spend_with_plain_key": B.verdict(spend(a, C.pub(a))), "spend_with_tweaked_key": B.verdict(spend(tw_secret, Q)),
                "reveal_check": C.hash160(C.ser(C.padd(C.parse(C.pub(a)), C.pmul(p2c_tweak(C.pub(a), contract))))) == spk[2:],
                "reveal_wrong_contract": C.hash160(C.ser(C.padd(C.parse(C.pub(a)), C.pmul(p2c_tweak(C.pub(a), b"another contract"))))) == spk[2:]}
    # a two-step colored coin: the seal of Bob is a UTXO whose key commits to the contract c0; Bob spends it into the key of Alice committing to c1, Alice spends into the key of Dan committing to c2
    bob, alice, dan = sk("cv-bob"), sk("cv-alice"), sk("cv-dan")
    c0 = b"issue: 100 tokens of ACME, owned by the holder of the seal tx0:0"
    c1 = b"transfer: 50 tokens to the seal of the next output; 50 tokens to a seal that Alice never sees"
    c2 = b"transfer: 50 tokens to the seal of the next output"
    ks0, Q0 = p2c_key(bob, c0)
    ks1, Q1 = p2c_key(alice, c1)
    ks2, Q2 = p2c_key(dan, c2)
    v0 = 500_000
    t0, i0 = B.fund(T.p2wpkh(Q0), v0)
    B.mine(1)
    tx1 = T.Tx(2); tx1.add_in(t0, i0); tx1.add_out(v0 - 1000, T.p2wpkh(Q1))
    tx1.sign_p2wpkh(0, ks0, v0)
    id1 = B.send(tx1)
    B.mine(1)
    tx2 = T.Tx(2); tx2.add_in(id1, 0); tx2.add_out(v0 - 2000, T.p2wpkh(Q2))
    tx2.sign_p2wpkh(0, ks1, v0 - 1000)
    id2 = B.send(tx2)
    B.mine(1)
    # what Dan receives from Alice: the public keys, the contracts and the outpoints, not the private keys
    hist = [{"pubkey": C.pub(bob).hex(), "contract": c0.decode(), "outpoint": "%s:%d" % (t0, i0)}, {"pubkey": C.pub(alice).hex(), "contract": c1.decode(), "outpoint": "%s:0" % id1},
            {"pubkey": C.pub(dan).hex(), "contract": c2.decode(), "outpoint": "%s:0" % id2}]
    # Dan validates with the node: each outpoint's script equals P2WPKH(P + t*G), and each is spent by the next transaction
    chk = []
    for k, h in enumerate(hist):
        t_, n_ = h["outpoint"].split(":")
        out = B.rpc("getrawtransaction", t_, True)["vout"][int(n_)]["scriptPubKey"]["hex"]
        P_ = bytes.fromhex(h["pubkey"])
        q = C.ser(C.padd(C.parse(P_), C.pmul(p2c_tweak(P_, h["contract"].encode()))))
        chk.append(T.p2wpkh(q).hex() == out)
    spent_by = [B.rpc("getrawtransaction", id1, True)["vin"][0]["txid"] == t0, B.rpc("getrawtransaction", id2, True)["vin"][0]["txid"] == id1]
    forged = hist[1].copy(); forged["contract"] = "transfer: 100 tokens to the seal of the next output"
    P_ = bytes.fromhex(forged["pubkey"])
    forged_ok = T.p2wpkh(C.ser(C.padd(C.parse(P_), C.pmul(p2c_tweak(P_, forged["contract"].encode()))))).hex() == B.rpc("getrawtransaction", id1, True)["vout"][0]["scriptPubKey"]["hex"]
    o["client_side_validation"] = {"history": hist, "commitments_match": chk, "spent_by_next": spent_by, "forged_contract_matches": forged_ok,
                                   "on_chain_script_types": [B.rpc("getrawtransaction", x, True)["vout"][0]["scriptPubKey"]["type"] for x in (id1, id2)],
                                   "tx_ids": [id1, id2], "tokens_visible_in_chain": any(b"ACME" in bytes.fromhex(B.rpc("getrawtransaction", x)) for x in (id1, id2))}
    return o


# ================================================================================================ c3 Emma and Fabian
@phase("c3")
def c3():
    o = {}
    E, F = sk("emma"), sk("fabian")
    Ep, Fp = C.pub(E), C.pub(F)
    ws = T.multisig2(Ep, Fp)
    order = sorted([(Ep, E), (Fp, F)])
    spk = T.p2wsh(ws)
    cap = 3_600_000                                  # 36 millibits = 0.036 bitcoin
    fee = 1000
    # Emma builds the funding transaction, signs it and does not transmit it
    addr = T.segwit_addr(spk[2:])
    raw = B.rpc("createrawtransaction", [], {addr: BTCF(cap)})
    fr = B.rpc("fundrawtransaction", raw, wallet="miner")
    fund_hex = B.rpc("signrawtransactionwithwallet", fr["hex"], wallet="miner")["hex"]
    dec = B.rpc("decoderawtransaction", fund_hex)
    ftxid = dec["txid"]
    fvout = [x["n"] for x in dec["vout"] if x["scriptPubKey"]["hex"] == spk.hex()][0]
    # the refund (commitment 1) is signed by both before the funding is transmitted
    h0 = B.height()
    L = h0 + 30                                      # the scaled form of the 4,320 blocks (30 days) of the book

    def commit(k, locktime=None, sigs=2):
        tx = T.Tx(2, (L - (k - 1)) if locktime is None else locktime)
        tx.add_in(ftxid, fvout, 0xfffffffe)
        tx.add_out(k * 1000, T.p2wpkh(Fp))           # k seconds of video at 1,000 satoshi (0.01 millibit) per second
        tx.add_out(cap - fee - k * 1000, T.p2wpkh(Ep))
        s = {pk: tx.sig(0, sec, ws, cap) for pk, sec in order}
        tx.vin[0][3] = [b"", s[order[0][0]], s[order[1][0]], ws] if sigs == 2 else [b"", s[Ep], b"", ws]
        return tx
    commits = [commit(k) for k in range(1, 7)]
    o["capacity_sat"] = cap
    o["funding_vsize"] = dec["vsize"]
    o["locktimes"] = [c.locktime for c in commits]
    o["start_height"] = h0
    before_funding = B.rpc("testmempoolaccept", [commits[0].hex()])[0].get("reject-reason")
    B.rpc("sendrawtransaction", fund_hex)
    B.mine(1)
    o["refund_before_funding_confirmed"] = before_funding
    h1 = B.height()
    o["at_start"] = [B.verdict(c)["reason"] for c in commits]
    B.mine(L - 6 - h1)                               # tip = L - 6: commitment 6 (locktime L - 5) is still not final
    o["tip_l_minus_6"] = {"height": B.height(), "c6": B.verdict(commits[5]), "c5": B.verdict(commits[4])}
    B.mine(1)                                         # tip = L - 5
    o["tip_l_minus_5"] = {"height": B.height(), "c6": B.verdict(commits[5]), "c5": B.verdict(commits[4]), "c1": B.verdict(commits[0])}
    B.rpc("sendrawtransaction", commits[5].hex())
    B.mine(1)
    o["after_c6_mined"] = {"height": B.height(), "c1_to_c5": [B.verdict(c)["reason"] for c in commits[:5]]}
    B.mine(L - B.height() + 1)
    o["after_all_timelocks"] = {"height": B.height(), "c1": B.verdict(commits[0])["reason"]}
    o["settlement_outputs_sat"] = [x[0] for x in commits[5].vout]
    # a cheat and a missing signature: Emma alone cannot move the funds (a second, identical channel, no timelock)
    t2, v2 = B.fund(spk, cap)
    B.mine(1)
    tx = T.Tx(2, 0); tx.add_in(t2, v2); tx.add_out(cap - fee, T.p2wpkh(Ep))
    tx.vin[0][3] = [b"", tx.sig(0, E, ws, cap), b"", ws]
    both = T.Tx(2, 0); both.add_in(t2, v2); both.add_out(cap - fee, T.p2wpkh(Ep))
    ss = {pk: both.sig(0, sec, ws, cap) for pk, sec in order}
    both.vin[0][3] = [b"", ss[order[0][0]], ss[order[1][0]], ws]
    o["emma_alone"] = B.verdict(tx)
    o["both_sign"] = B.verdict(both)
    o["witness_script_hex"] = ws.hex()
    o["witness_script_len"] = len(ws)
    return o


# ================================================================================================ c4 the revocable commitment of Hitesh and Irene
@phase("c4")
def c4():
    o = {}
    Hs, Is = sk("hitesh"), sk("irene")
    Hp, Ip = C.pub(Hs), C.pub(Is)
    ws = T.multisig2(Hp, Ip)
    order = sorted([(Hp, Hs), (Ip, Is)])
    spk = T.p2wsh(ws)
    cap = 1_000_000_000                              # 10 bitcoin, 5 from each
    fee = 10_000
    a_half, b_half = sk("hitesh-revocation-half"), sk("irene-revocation-half")   # each channel party generates one half of the revocation secret
    RP = C.ser(C.padd(C.pmul(a_half), C.pmul(b_half)))
    full = (a_half + b_half) % C.N
    delay = 1000

    def channel():
        t_, v_ = B.fund(spk, cap)
        B.mine(1)
        # the commitment held by Hitesh, signed by Irene and completed by Hitesh: Irene is paid at once, Hitesh after the delay or Irene with the revocation key
        rscript = T.script("IF", RP, "ELSE", delay, "CSV", "DROP", Hp, "ENDIF", "CHECKSIG")
        tx = T.Tx(2, 0)
        tx.add_in(t_, v_, 0xfffffffe)
        tx.add_out(500_000_000, T.p2wpkh(Ip))
        tx.add_out(500_000_000 - fee, T.p2wsh(rscript))
        ss = {pk: tx.sig(0, sec, ws, cap) for pk, sec in order}
        tx.vin[0][3] = [b"", ss[order[0][0]], ss[order[1][0]], ws]
        return tx, rscript

    def spend(ctx, rscript, secret, branch, seq=0xfffffffe):
        tx = T.Tx(2, 0)
        tx.add_in(ctx.txid(), 1, seq)
        tx.add_out(500_000_000 - fee - 10_000, T.p2wpkh(C.pub(sk("sweep-" + branch))))
        sg = tx.sig(0, secret, rscript, 500_000_000 - fee)
        tx.vin[0][3] = [sg, b"\x01", rscript] if branch == "revoke" else [sg, b"", rscript]
        return tx
    # (i) the delayed path: the holder waits for 1,000 blocks
    ctx, rscript = channel()
    o["commitment_vsize"] = ctx.vsize()
    o["to_local_script_hex"] = rscript.hex()
    o["to_local_script_asm"] = B.rpc("decodescript", rscript.hex())["asm"]
    B.rpc("sendrawtransaction", ctx.hex())
    B.mine(1)
    hc = B.height()
    d = spend(ctx, rscript, Hs, "delay", delay)
    early = B.verdict(spend(ctx, rscript, Hs, "delay", 0xfffffffe))
    o["delay_no_sequence"] = early
    B.mine(delay - 2)                                 # the commitment has delay - 1 confirmations
    o["delay_at_999_confirmations"] = {"confirmations": B.height() - hc + 1, **B.verdict(d)}
    B.mine(1)
    o["delay_at_1000_confirmations"] = {"confirmations": B.height() - hc + 1, **B.verdict(d)}
    B.send(d)
    o["delay_spent"] = True
    # the same output, claimed by the other party through the revocation branch
    ctx2, rscript2 = channel()
    B.rpc("sendrawtransaction", ctx2.hex())
    B.mine(1)
    o["revoke_with_one_half"] = B.verdict(spend(ctx2, rscript2, b_half, "revoke"))
    o["revoke_with_both_halves"] = B.verdict(spend(ctx2, rscript2, full, "revoke"))
    rv = spend(ctx2, rscript2, full, "revoke")
    B.send(rv)
    B.mine(1)
    o["revoke_confirmed"] = True
    o["revoke_witness_items"] = [len(x) for x in rv.vin[0][3]]
    o["revocation_pubkey"] = RP.hex()
    o["delay_blocks"] = delay
    return o


# ================================================================================================ c5 the hash time lock contract of the book
@phase("c5")
def c5():
    o = {}
    pay, rcv = sk("htlc-payer"), sk("htlc-receiver")
    Pp, Rp = C.pub(pay), C.pub(rcv)
    secret_r = C.sha256(b"the secret R of the receiver")
    Hh = C.hash160(secret_r)
    o["secret_len"] = len(secret_r)
    o["hash160_hex"] = Hh.hex()
    o["sha256_payment_hash"] = C.sha256(secret_r).hex()
    o["hash160_is_ripemd160_of_sha256"] = Hh == C.ripemd160(C.sha256(secret_r))
    lock = B.height() + 20
    amt = 100_000
    fee = 1000

    def contract(variant):
        if variant == "book":
            return T.script("IF", "HASH160", Hh, "EQUALVERIFY", Rp, "CHECKSIG", "ELSE", lock, "CLTV", "DROP", Pp, "CHECKSIG", "ENDIF")
        return T.script("IF", "HASH160", Hh, "EQUAL", "ELSE", lock, "CLTV", "DROP", Pp, "CHECKSIG", "ENDIF")

    def fresh(variant):
        ws = contract(variant)
        t_, v_ = B.fund(T.p2wsh(ws), amt)
        return ws, t_, v_

    def spend(ws, t_, v_, branch, preimage=None, locktime=0, dest="x", signer=None):
        tx = T.Tx(2, locktime)
        tx.add_in(t_, v_, 0xfffffffe)
        tx.add_out(amt - fee, T.p2wpkh(C.pub(sk("htlc-" + dest))))
        if branch == "hash":
            items = [preimage, b"\x01", ws]
            if signer is not None:
                items = [tx.sig(0, signer, ws, amt)] + items
        else:
            items = [tx.sig(0, signer, ws, amt), b"", ws]
        tx.vin[0][3] = items
        return tx
    wsb, tb, vb = fresh("book")
    ws0, t0, v0 = fresh("book")
    ws1, t1, v1 = fresh("book")
    wsa, ta, va = fresh("anyone")
    B.mine(1)
    o["lock_height"] = lock
    o["height_at_funding"] = B.height()
    o["script_asm"] = B.rpc("decodescript", wsb.hex())["asm"]
    o["claim_with_secret"] = B.verdict(spend(wsb, tb, vb, "hash", secret_r, 0, "rcv", rcv))
    o["claim_with_wrong_secret"] = B.verdict(spend(ws0, t0, v0, "hash", C.sha256(b"a guess"), 0, "rcv", rcv))
    o["claim_with_secret_but_payer_key"] = B.verdict(spend(ws0, t0, v0, "hash", secret_r, 0, "rcv", pay))
    o["refund_before_timeout"] = B.verdict(spend(ws1, t1, v1, "refund", None, lock, "pay", pay))
    anyone = spend(wsa, ta, va, "hash", secret_r, 0, "thief")
    o["anyone_with_secret"] = B.verdict(anyone)
    B.mine(lock - 1 - B.height())                   # tip = lock - 1: a transaction with locktime = lock is still not final
    o["refund_at_tip_lock_minus_1"] = {"height": B.height(), **B.verdict(spend(ws1, t1, v1, "refund", None, lock, "pay", pay))}
    o["refund_with_low_locktime_final"] = {"height": B.height(), **B.verdict(spend(ws1, t1, v1, "refund", None, lock - 5, "pay", pay))}
    B.mine(1)
    o["refund_at_tip_lock"] = {"height": B.height(), **B.verdict(spend(ws1, t1, v1, "refund", None, lock, "pay", pay))}
    o["claim_after_timeout"] = B.verdict(spend(ws0, t0, v0, "hash", secret_r, 0, "rcv", rcv))
    o["wsh_len_book"] = len(wsb)
    return o


# ================================================================================================ c6 anchors: version 3 parent, pay to anchor, child in a package
@phase("c6")
def c6():
    o = {}
    u = [x for x in B.rpc("listunspent", 1, 9999999, [], True, wallet="miner") if x["amount"] >= 1][0]
    ch = B.rpc("getnewaddress", wallet="miner")
    p2a = bytes.fromhex("51024e73")
    amt = int(round(float(u["amount"]) * 1e8))
    parent = T.Tx(3, 0)
    parent.add_in(u["txid"], u["vout"], 0xfffffffd)
    parent.add_out(0, p2a)
    chspk = bytes.fromhex(B.rpc("getaddressinfo", ch, wallet="miner")["scriptPubKey"])
    parent.add_out(amt, chspk)                       # a parent that pays no fee at all
    sp = B.rpc("signrawtransactionwithwallet", parent.hex(), wallet="miner")["hex"]
    o["parent_alone"] = B.rpc("testmempoolaccept", [sp])[0]
    ptx = B.rpc("decoderawtransaction", sp)
    child = T.Tx(3, 0)
    child.add_in(ptx["txid"], 0, 0xfffffffd)         # the anchor: anyone can spend it, no witness needed
    child.add_in(ptx["txid"], 1, 0xfffffffd)
    caddr = B.rpc("getnewaddress", wallet="miner")
    cspk = bytes.fromhex(B.rpc("getaddressinfo", caddr, wallet="miner")["scriptPubKey"])
    child.add_out(amt - 3000, cspk)
    prev = [{"txid": ptx["txid"], "vout": 0, "scriptPubKey": p2a.hex(), "amount": 0}, {"txid": ptx["txid"], "vout": 1, "scriptPubKey": chspk.hex(), "amount": amt / 1e8}]
    sc = B.rpc("signrawtransactionwithwallet", child.hex(), prev, wallet="miner")
    o["child_signed_complete"] = sc["complete"]
    o["package"] = B.attempt("submitpackage", [sp, sc["hex"]])
    if "ok" in o["package"]:
        pk = o["package"]["ok"]
        o["package_msg"] = pk.get("package_msg")
        o["parent_vsize"], o["child_vsize"] = ptx["vsize"], B.rpc("decoderawtransaction", sc["hex"])["vsize"]
        o["anchor_witness_len"] = len(B.rpc("decoderawtransaction", sc["hex"])["vin"][0].get("txinwitness", []))
        B.mine(1)
        o["both_confirmed"] = B.rpc("getrawtransaction", ptx["txid"], True).get("confirmations", 0) >= 1
    return o


# ================================================================================================ Lightning with lnd
LN_BASE = 9731
class LND:
    def __init__(self, name, idx, extra=()):
        self.name, self.idx, self.extra = name, idx, list(extra)
        self.dir = os.path.join(TMP, name)
        self.rpc, self.port, self.rest = 10001 + idx, LN_BASE + idx, 8081 + idx
        self.proc = None
        self.pk = None

    def start(self):
        os.makedirs(self.dir, exist_ok=True)
        self.proc = subprocess.Popen([LNDD + "/lnd", "--lnddir=" + self.dir, "--bitcoin.regtest", "--bitcoin.node=bitcoind", "--bitcoind.rpchost=127.0.0.1:%d" % BTC_RPC, "--bitcoind.rpcuser=u",
                                      "--bitcoind.rpcpass=p", "--bitcoind.zmqpubrawblock=tcp://127.0.0.1:%d" % ZMQB, "--bitcoind.zmqpubrawtx=tcp://127.0.0.1:%d" % ZMQT, "--noseedbackup",
                                      "--listen=127.0.0.1:%d" % self.port, "--rpclisten=127.0.0.1:%d" % self.rpc, "--restlisten=127.0.0.1:%d" % self.rest, "--protocol.wumbo-channels",
                                      "--alias=" + self.name] + self.extra, stdout=open(os.path.join(self.dir, "out.log"), "a"), stderr=subprocess.STDOUT, start_new_session=True)
        for _ in range(180):
            try:
                i = self.cli("getinfo")
                if i.get("synced_to_chain"):
                    self.pk = i["identity_pubkey"]
                    return i
            except Exception:
                pass
            time.sleep(1)
        raise RuntimeError("lnd %s did not start" % self.name)

    def cmd(self):
        return [LNDD + "/lncli", "--lnddir=" + self.dir, "--rpcserver=127.0.0.1:%d" % self.rpc, "--network=regtest"]

    def cli(self, *a, timeout=120):
        r = sh(self.cmd() + [str(x) for x in a], timeout=timeout)
        if r.returncode:
            raise RuntimeError(" ".join((r.stdout + r.stderr).split())[:500])
        try:
            return json.loads(r.stdout)
        except Exception:
            return r.stdout.strip()

    def attempt(self, *a):
        try:
            return {"ok": self.cli(*a)}
        except Exception as e:
            return {"error": str(e)}

    def stop(self):
        try:
            self.cli("stop")
        except Exception:
            pass
        for _ in range(60):
            if self.proc is not None and self.proc.poll() is not None:
                break
            time.sleep(0.5)
        if self.proc is not None and self.proc.poll() is None:
            self.proc.kill()
        time.sleep(1)


def wait(cond, secs=120, step=1.0):
    t = time.time()
    while time.time() - t < secs:
        try:
            v = cond()
            if v:
                return v
        except Exception:
            pass
        time.sleep(step)
    return None


LNN = {}


def pay(src, invoice, extra=()):
    r = sh(src.cmd() + ["payinvoice", "--pay_req", invoice, "--force", "--json"] + list(extra), timeout=300)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"status": "ERROR", "text": " ".join((r.stdout + r.stderr).split())[:300]}


def chans(n):
    return [{"channel_point": c["channel_point"], "chan_id": c["chan_id"], "capacity": int(c["capacity"]), "local": int(c["local_balance"]), "remote": int(c["remote_balance"]), "active": c["active"],
             "csv_delay": c["csv_delay"], "reserve_local": int(c["local_chan_reserve_sat"]), "reserve_remote": int(c["remote_chan_reserve_sat"]), "commit_fee": int(c["commit_fee"]),
             "commitment_type": c["commitment_type"], "num_updates": int(c["num_updates"]), "initiator": c["initiator"], "pending": [{"incoming": h["incoming"], "amount": int(h["amount"]), "expiration_height": h["expiration_height"], "hash_lock": h["hash_lock"]} for h in c.get("pending_htlcs", [])],
             "remote_pubkey": c["remote_pubkey"]} for c in n.cli("listchannels")["channels"]]


@phase("l1")
def l1():
    o = {}
    names = ["alice", "bob", "carol", "diana", "eric"]
    # the book's example has a fee of 0.001 per hop: the three intermediaries are started with that base fee, no proportional fee and a timelock delta of 80 blocks (lnd's default)
    fee = ["--bitcoin.basefee=100000000", "--bitcoin.feerate=0", "--bitcoin.timelockdelta=80"]
    nodes = [LND(n, i, fee if n in ("bob", "carol", "diana") else ()) for i, n in enumerate(names)]
    LNN.update({n.name: n for n in nodes})
    infos = {}
    for n in nodes:
        infos[n.name] = n.start()
    o["version"] = infos["alice"]["version"]
    o["features"] = sorted({f["name"] for f in infos["alice"]["features"].values() if f.get("name")})
    o["chain"] = infos["alice"]["chains"][0]
    for n in nodes[:4]:
        a = n.cli("newaddress", "p2wkh")["address"]
        B.rpc("sendtoaddress", a, "4.5", wallet="miner")
    B.mine(6)
    wait(lambda: all(int(n.cli("walletbalance")["confirmed_balance"]) > 0 for n in nodes[:4]), 60)
    opens = []
    for a, b in zip(nodes, nodes[1:]):
        a.cli("connect", b.pk + "@127.0.0.1:%d" % b.port)
        r = a.cli("openchannel", "--node_key", b.pk, "--local_amt", 400_000_000, "--push_amt", 200_000_000)
        opens.append(r["funding_txid"])
        B.mine(1)
        time.sleep(1)
    B.mine(6)
    wait(lambda: all(len(chans(n)) >= 1 and all(c["active"] for c in chans(n)) for n in nodes), 120)
    o["funding_txids"] = opens
    def graph_ready():
        g = nodes[0].cli("describegraph")
        if len(g["edges"]) != 4:
            return False
        have = sum(1 for e in g["edges"] for k in ("node1_policy", "node2_policy") if e[k] and e[k]["fee_base_msat"] == "100000000")
        return have >= 3
    def gr_mine():
        B.mine(1)
        return graph_ready()
    o["graph_ready"] = bool(wait(gr_mine, 300, 20))
    o["channels"] = {n.name: chans(n) for n in nodes}
    g = nodes[0].cli("describegraph")
    o["graph"] = {"nodes": len(g["nodes"]), "edges": len(g["edges"])}
    ni = nodes[0].cli("getnetworkinfo")
    o["networkinfo"] = {k: ni[k] for k in ("graph_diameter", "num_nodes", "num_channels", "total_network_capacity", "avg_out_degree", "max_out_degree")}
    o["funding_output"] = []
    for t_ in opens:
        tx = B.rpc("getrawtransaction", t_, True)
        o["funding_output"].append([{"value": x["value"], "type": x["scriptPubKey"]["type"]} for x in tx["vout"]])
    return o


@phase("l2")
def l2():
    o = {}
    a, e = LNN["alice"], LNN["eric"]
    inv = e.cli("addinvoice", "--amt", 100_000_000)
    d = a.cli("decodepayreq", inv["payment_request"])
    o["invoice"] = {"payment_request": inv["payment_request"], "payment_hash": d["payment_hash"], "num_satoshis": d["num_satoshis"], "cltv_expiry": d["cltv_expiry"], "expiry": d["expiry"],
                    "payment_addr": d["payment_addr"], "destination": d["destination"], "features": sorted(v["name"] for v in d["features"].values())}
    h0 = B.height()
    before = {n: chans(LNN[n]) for n in LNN}
    res = pay(a, inv["payment_request"])
    o["height_at_payment"] = h0
    o["status"] = res.get("status")
    o["preimage"] = res.get("payment_preimage")
    o["preimage_hashes_to_payment_hash"] = hashlib.sha256(bytes.fromhex(res["payment_preimage"])).hexdigest() == d["payment_hash"] if res.get("payment_preimage") else False
    o["fee_sat"] = res.get("fee_sat")
    o["htlcs"] = [{"status": h["status"], "total_time_lock": h["route"]["total_time_lock"], "total_fees_msat": h["route"]["total_fees_msat"], "total_amt_msat": h["route"]["total_amt_msat"],
                   "hops": [{"pub_key": x["pub_key"], "chan_id": x["chan_id"], "amt_to_forward_msat": x["amt_to_forward_msat"], "fee_msat": x["fee_msat"], "expiry": x["expiry"]} for x in h["route"]["hops"]]} for h in res.get("htlcs", [])]
    o["names_by_pubkey"] = {LNN[n].pk: n for n in LNN}
    time.sleep(2)
    o["channels_before"] = before
    o["channels_after"] = {n: chans(LNN[n]) for n in LNN}
    return o


@phase("l3")
def l3():
    o = {}
    a, e = LNN["alice"], LNN["eric"]

    def inflight(pre):
        pre_b = bytes.fromhex(pre)
        h = hashlib.sha256(pre_b).hexdigest()
        inv = e.cli("addholdinvoice", h, 10_000_000)
        log = os.path.join(TMP, "pay_%s.json" % h[:8])
        p = subprocess.Popen(a.cmd() + ["payinvoice", "--pay_req", inv["payment_request"], "--force", "--json"], stdout=open(log, "w"), stderr=subprocess.STDOUT)
        def all_pending():
            return all(any(c["pending"] for c in chans(LNN[n])) for n in ("alice", "bob", "carol", "diana", "eric"))
        wait(all_pending, 60, 0.5)
        snap = {}
        for n in ("alice", "bob", "carol", "diana", "eric"):
            snap[n] = [{"remote": next((LNN[x].name for x in LNN if LNN[x].pk == c["remote_pubkey"]), "?"), "local": c["local"], "remote_bal": c["remote"], "pending": c["pending"]} for c in chans(LNN[n]) if c["pending"]]
        return h, p, log, snap
    pre1 = hashlib.sha256(b"the secret R of the Lightning example").hexdigest()
    h1, p1, log1, snap1 = inflight(pre1)
    o["inflight"] = snap1
    o["height_inflight"] = B.height()
    o["hash"] = h1
    e.cli("settleinvoice", pre1)
    p1.wait(timeout=120)
    try:
        r1 = json.load(open(log1))
    except Exception:
        r1 = {}
    o["settled_status"] = r1.get("status")
    o["settled_preimage"] = r1.get("payment_preimage")
    time.sleep(2)
    o["after_settle"] = {n: [(c["local"], c["remote"]) for c in chans(LNN[n])] for n in LNN}
    # the second one is cancelled by the receiver: the HTLCs fail back and every balance returns
    bal_before = {n: [(c["local"], c["remote"]) for c in chans(LNN[n])] for n in LNN}
    pre2 = hashlib.sha256(b"a second secret that is never revealed").hexdigest()
    h2, p2, log2, snap2 = inflight(pre2)
    e.cli("cancelinvoice", h2)
    p2.wait(timeout=120)
    try:
        r2 = json.load(open(log2))
    except Exception:
        r2 = {}
    time.sleep(2)
    o["cancel"] = {"status": r2.get("status"), "failure_reason": r2.get("failure_reason"), "balances_before": bal_before, "balances_after": {n: [(c["local"], c["remote"]) for c in chans(LNN[n])] for n in LNN},
                   "pending_during": {n: sum(len(x["pending"]) for x in snap2[n]) for n in snap2}}
    return o


@phase("l4")
def l4():
    o = {}
    b, c = LNN["bob"], LNN["carol"]
    ch = [x for x in chans(b) if x["remote_pubkey"] == c.pk][0]
    txid, idx = ch["channel_point"].split(":")
    o["state_before"] = {"num_updates": ch["num_updates"], "local": ch["local"], "remote": ch["remote"]}
    r = b.attempt("closechannel", txid, idx)
    time.sleep(2)
    mp = B.rpc("getrawmempool")
    B.mine(1)
    ct = None
    for tid in mp:
        t = B.rpc("getrawtransaction", tid, True)
        if any(i["txid"] == txid for i in t["vin"]):
            ct = t
    if ct is None:
        raise RuntimeError("closing transaction not found: %s" % r)
    o["close"] = {"txid": ct["txid"], "vsize": ct["vsize"], "outputs": [{"value": x["value"], "type": x["scriptPubKey"]["type"]} for x in ct["vout"]], "locktime": ct["locktime"],
                  "witness_items": [len(w) // 2 for w in ct["vin"][0]["txinwitness"]], "sequence": ct["vin"][0]["sequence"], "witness_script_asm": B.rpc("decodescript", ct["vin"][0]["txinwitness"][-1])["asm"],
                  "witness_script_hex": ct["vin"][0]["txinwitness"][-1], "version": ct["version"]}
    o["onchain_transactions_in_lifetime"] = 2
    ft = B.rpc("getrawtransaction", txid, True)
    o["funding"] = {"txid": txid, "vsize": ft["vsize"], "value": ft["vout"][int(idx)]["value"], "type": ft["vout"][int(idx)]["scriptPubKey"]["type"]}
    time.sleep(2)
    o["closed"] = [{"close_type": x["close_type"], "settled_balance": x["settled_balance"]} for x in b.cli("closedchannels")["channels"]]
    return o


@phase("l5")
def l5():
    o = {}
    hn, irn = LND("hitesh", 5), LND("irene", 6)
    LNN.update({"hitesh": hn, "irene": irn})
    hn.start(); irn.start()
    irn_addr = irn.cli("newaddress", "p2wkh")["address"]
    B.rpc("sendtoaddress", irn_addr, "11", wallet="miner")
    B.mine(6)
    wait(lambda: int(irn.cli("walletbalance")["confirmed_balance"]) >= 1_100_000_000, 60)
    irn.cli("connect", hn.pk + "@127.0.0.1:%d" % hn.port)
    irn.cli("openchannel", "--node_key", hn.pk, "--local_amt", 1_000_000_000, "--push_amt", 500_000_000)
    B.mine(6)
    wait(lambda: chans(irn) and chans(irn)[0]["active"], 90)
    def edge_ready():
        g = irn.cli("describegraph")
        return len(g["edges"]) == 1 and g["edges"][0]["node1_policy"] and g["edges"][0]["node2_policy"]
    wait(edge_ready, 200, 5)
    c0 = chans(irn)[0]
    o["state1"] = {"irene": c0["local"], "hitesh": c0["remote"], "num_updates": c0["num_updates"], "csv_delay": c0["csv_delay"], "capacity": c0["capacity"], "commitment_type": c0["commitment_type"]}
    cp = c0["channel_point"]
    ftxid, fidx = cp.split(":")
    # the snapshot of Irene's data at state 1 (a stopped node, a copy of its directory)
    irn.stop()
    snap = os.path.join(TMP, "irene_snap")
    shutil.copytree(irn.dir, snap)
    irn.start()
    wait(lambda: any(x["remote_pubkey"] == hn.pk and x["active"] for x in chans(irn)), 60)
    inv = hn.cli("addinvoice", "--amt", 200_000_000)
    res = pay(irn, inv["payment_request"])
    o["payment_status"] = res.get("status")
    if res.get("status") != "SUCCEEDED":
        raise RuntimeError("the payment that moves the channel to state 2 did not succeed: %s" % (res.get("failure_reason") or res.get("text")))
    time.sleep(2)
    c1 = chans(irn)[0]
    h1 = chans(hn)[0]
    o["state2"] = {"irene": c1["local"], "hitesh": c1["remote"], "num_updates": c1["num_updates"], "hitesh_view": [h1["local"], h1["remote"]]}
    hbal_before = int(hn.cli("walletbalance")["confirmed_balance"])
    # Irene goes back to the old state: Hitesh is offline, so no node tells her that she is behind
    hn.stop(); irn.stop()
    shutil.move(irn.dir, irn.dir + "_current")
    shutil.copytree(snap, irn.dir)
    irn.start()
    old = chans(irn)[0]
    o["irene_restored_state"] = {"irene": old["local"], "hitesh": old["remote"], "num_updates": old["num_updates"]}
    r = irn.attempt("closechannel", "--force", ftxid, fidx)
    o["force_close_command"] = "ok" if "ok" in r else r["error"]
    time.sleep(3)
    mp = B.rpc("getrawmempool")
    rev = None
    for tid in mp:
        t = B.rpc("getrawtransaction", tid, True)
        if any(i["txid"] == ftxid for i in t["vin"]):
            rev = t
    if rev is None:
        raise RuntimeError("revoked commitment not in the mempool: %s" % mp)
    o["revoked_commitment"] = {"txid": rev["txid"], "locktime": rev["locktime"], "sequence": rev["vin"][0]["sequence"], "version": rev["version"], "vsize": rev["vsize"],
                               "outputs": [{"value": x["value"], "type": x["scriptPubKey"]["type"], "hex": x["scriptPubKey"]["hex"]} for x in rev["vout"]],
                               "witness_script_asm": B.rpc("decodescript", rev["vin"][0]["txinwitness"][-1])["asm"], "witness_script_hex": rev["vin"][0]["txinwitness"][-1],
                               "witness_items": [len(w) // 2 for w in rev["vin"][0]["txinwitness"]]}
    B.mine(1)
    irn.stop()
    hn.start()
    jt = None
    # lnd waits for several confirmations of a spend of a large channel before it acts: mine them (the justice window is 2016 blocks)
    B.mine(6)
    o["blocks_mined_before_justice"] = 7
    def find_justice():
        for tid in B.rpc("getrawmempool"):
            t = B.rpc("getrawtransaction", tid, True)
            if any(i["txid"] == rev["txid"] for i in t["vin"]):
                return t
        return None
    jt = wait(find_justice, 120, 2)
    if jt is None:
        raise RuntimeError("no justice transaction")
    o["justice"] = {"txid": jt["txid"], "inputs": [{"vout": i["vout"], "witness_items": [len(w) // 2 for w in i["txinwitness"]], "script_asm": B.rpc("decodescript", i["txinwitness"][-1])["asm"] if len(i["txinwitness"][-1]) > 0 else "", "first_item_empty_or_one": i["txinwitness"][-2] if len(i["txinwitness"]) >= 2 else None} for i in jt["vin"]],
                    "outputs": [{"value": x["value"], "type": x["scriptPubKey"]["type"]} for x in jt["vout"]], "vsize": jt["vsize"], "blocks_after_revoked": 7}
    B.mine(1)
    time.sleep(3)
    o["hitesh_wallet_before_sat"] = hbal_before
    o["hitesh_wallet_after_sat"] = int(hn.cli("walletbalance")["confirmed_balance"])
    cl = hn.attempt("closedchannels")
    o["hitesh_closed"] = [{"close_type": x["close_type"], "settled_balance": x["settled_balance"]} for x in cl["ok"]["channels"]] if "ok" in cl else cl
    o["total_channel_sat"] = 1_000_000_000
    return o


@phase("b")
def bphase():
    o = {}
    man = open(os.path.join(HERE, "ch14-evidence", "lnd_manifest.txt")).read()
    ln = [l for l in man.splitlines() if "lnd-linux-amd64" in l and l.endswith(".tar.gz")][0].split()
    tgz = "/home/claude/ln21/lnd.tgz"
    h = hashlib.sha256(open(tgz, "rb").read()).hexdigest()
    o["archive_hash"] = h
    o["manifest_hash"] = ln[0]
    o["match"] = h == ln[0]
    o["lnd_binary_sha256"] = hashlib.sha256(open(LNDD + "/lnd", "rb").read()).hexdigest()
    o["manifest_lists_binary"] = o["lnd_binary_sha256"] in man
    o["manifest_signature_file"] = "https://github.com/lightningnetwork/lnd/releases/download/v0.21.3-beta/manifest-roasbeef-v0.21.3-beta.txt.sig -> HTTP 404 (Not Found)"
    return o


R["not_executed"] = [
    {"item": "lightning_on_mainnet", "reason": "no mainnet funds; the Lightning nodes ran on a private regtest chain, so fees, liquidity and routing failures of the public network are not shown"},
    {"item": "other_implementations", "reason": "only lnd 0.21.3 was installed; Core Lightning, Eclair and LDK are read from their README files, and interoperability between implementations is not tested"},
    {"item": "taproot_assets_and_rgb", "reason": "no Taproot Assets or RGB software was installed; only the building blocks (single-use seal, pay to contract, client-side validation) were built by hand"},
    {"item": "watchtower", "reason": "no watchtower service was run; the breach was answered by the online counterparty itself"},
    {"item": "htlc_timeout_on_chain", "reason": "no HTLC was left to expire on chain in the lnd run; the timeout branch was run only in the hand-built contract of phase c5"},
    {"item": "multipath_and_trampoline", "reason": "the 5-node line has one path; multipath payments, trampoline routing and BOLT 12 offers were not run"},
    {"item": "gossip_on_mainnet", "reason": "the gossip of five private nodes only; the size and the behaviour of the public graph are taken from a statistics page"},
    {"item": "bolt8_between_lnd_nodes_on_the_wire", "reason": "the handshake was recomputed from the BOLT 8 test vectors in Python; the traffic between the lnd nodes was not captured"},
    {"item": "gpg_signature_of_lnd_manifest", "reason": "the detached signature file named manifest-roasbeef is not served under that name for this release (HTTP 404), so only the sha256 of the archive was compared with the manifest"},
    {"item": "unilateral_close_with_htlcs_pending", "reason": "no commitment with HTLC outputs was broadcast; the HTLC-timeout and HTLC-success transactions of BOLT 3 were not produced"},
]


# ================================================================================================ main
PHASES = [c1, c2, c3, c4, c5, c6, l1, l2, l3, l4, l5, bphase]


def main():
    global B
    B = BTC()
    try:
        B.rpc("createwallet", "miner")
        B.addr = B.rpc("getnewaddress", wallet="miner")
        B.mine(300)
        R["binary"] = {"bitcoind_version": B.rpc("getnetworkinfo")["subversion"], "bitcoind_sha256": hashlib.sha256(open(BIN + "/bitcoind", "rb").read()).hexdigest(),
                       "version_line": sh([BIN + "/bitcoind", "--version"]).stdout.splitlines()[0]}
        for p in PHASES:
            p()
    finally:
        for n in list(LNN.values()):
            n.stop()
        save()
        B.stop()
        if "--keep" not in sys.argv:
            shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    main()
