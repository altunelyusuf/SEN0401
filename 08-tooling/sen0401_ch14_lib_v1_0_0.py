#!/usr/bin/env python3
"""SEN0401 chapter 14 (Second-Layer Applications): the library the chapter's executed claims call. Standard library only (plus sen0401_ch10_p2p_v1_0_0 for sha256d).
* text(), has(), const(): read a saved source (08-tooling/ch14-evidence) and test that a passage or a constant is in it (whitespace collapsed).
* run(): the recorded regtest run (sen0401_ch14_regtest_v1_0_0.py, Bitcoin Core 31.1 nodes on private chains); every value read from it is a SINGLE-RUN value.
* the arithmetic and the cryptography of the chapter as functions: the route fee and timelock arithmetic of the book's Lightning example, the pure-Python BOLT 8 handshake, BOLT 4 onion packet,
  BOLT 3 shachain and revocation keys and BOLT 11 invoice parse, each recomputed from the published test vectors in the saved BOLT files (sen0401_ch14_crypto_v1_0_0).
* quotes_report(), index_report(): the passages used from every source, and the fetch record of every source."""
__version__ = "1.0.0"
import datetime, hashlib, html, json, math, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P
import sen0401_ch14_crypto_v1_0_0 as C
EV = os.path.join(HERE, "ch14-evidence")
sha256d = P.sha256d
_T = {}
_J = {}


def text(fname):
    """The saved source as one string, whitespace collapsed; html and pdf copies are read through their .txt conversion."""
    if fname not in _T:
        p = os.path.join(EV, fname)
        if fname.endswith(".html") or fname.endswith(".pdf"):
            p = os.path.splitext(p)[0] + ".txt"
        s = open(p, errors="replace").read()
        if fname.endswith(".html"):
            s = html.unescape(s)
        _T[fname] = re.sub(r"\s+", " ", s)
    return _T[fname]


def has(fname, *frags):
    t = text(fname)
    return all(re.sub(r"\s+", " ", f) in t for f in frags)


def const(fname, name):
    """The value of a C++ constant or a markdown definition: `name = ...;` or `name{...}` in a saved source (first match), as written."""
    t = text(fname)
    m = re.search(re.escape(name) + r"\s*(?:\{|=)\s*([^;}\s,]+)", t)
    return m.group(1) if m else None


def jload(name):
    if name not in _J:
        _J[name] = json.load(open(os.path.join(EV, name)))
    return _J[name]


def run():
    return jload("regtest_run_v1_0_0.json")


def raw(fname):
    return open(os.path.join(EV, fname)).read().strip()


def iso(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _hx(x):
    return bytes.fromhex(x[2:] if x.startswith("0x") else x)


def _vec(name, fname="bolt08_transport.md", nth=0):
    """the nth value written as name: 0x... in a saved BOLT file"""
    return re.findall(re.escape(name) + r"[:=]\s*(0x[0-9a-f]+)", text(fname))[nth]


# ------------------------------------------------------------------------------------------------ the arithmetic of the book's Lightning example
def route_fees(amount, base_fees):
    """Forwarding from the last hop backwards: every intermediary adds its fee on top of what the next hop must receive; returns (amounts that each hop sends, total sent)."""
    sends, a = [], amount
    for f in reversed(base_fees):
        a += f
        sends.append(a)
    return list(reversed(sends)), a


def timelocks(final_cltv, deltas):
    """The expiry of the HTLC on each hop, from the receiver backwards: each hop must have more time than the next one by its delta."""
    out, t = [], final_cltv
    for d in reversed(deltas):
        t += d
        out.append(t)
    return list(reversed(out))


def channel_balances(capacity, moves):
    """A list of (from_a, amount): the balance (a, b) after each move, refusing a move that would overdraw the sender."""
    a, b, hist = capacity, 0, [(capacity, 0)]
    for dirn, amt in moves:
        if dirn == "ab":
            assert a >= amt
            a, b = a - amt, b + amt
        else:
            assert b >= amt
            a, b = a + amt, b - amt
        hist.append((a, b))
    return hist


# ------------------------------------------------------------------------------------------------ the cryptography of the specification, recomputed from the vectors
def bolt8():
    """The initiator of the BOLT 8 handshake with the fixed keys of the vector, run on the vector's act two: returns the three outputs and the two keys, as hex."""
    r = C.noise_initiator(_hx(_vec("ls.priv")), _hx(_vec("e.priv")), _hx(_vec("rs.pub")), _hx(_vec("input", nth=0)))
    return {"act1": "0x" + r["act1"].hex(), "act3": "0x" + r["act3"].hex(), "sk": "0x" + r["sk"].hex(), "ck_len": len(r["ck"]),
            "want_act1": _vec("output", nth=0), "want_act3": _vec("output", nth=1), "want_sk": re.findall(r"sk,rk=(0x[0-9a-f]+),(0x[0-9a-f]+)", text("bolt08_transport.md"))[0][0]}


def bolt8_hello():
    """The first transport message of the vector: the 5 bytes hello under the sending key, as hex."""
    sk = _hx(re.findall(r"sk,rk=(0x[0-9a-f]+),(0x[0-9a-f]+)", text("bolt08_transport.md"))[0][0])
    out, sk2, ck2, n = C.transport_message(sk, b"\0" * 32, 0, b"hello")
    return "0x" + out.hex(), len(out)


def onion():
    """The BOLT 4 onion packet of the five-hop vector, rebuilt from the session key, the hops and the associated data, against the packet of the file."""
    v = jload("bolt04_onion_test.json")
    g = v["generate"]
    hops = [(bytes.fromhex(h["pubkey"]), bytes.fromhex(h["payload"])) for h in g["hops"]]
    pkt = C.sphinx_packet(bytes.fromhex(g["session_key"]), hops, bytes.fromhex(g["associated_data"]))
    return pkt.hex(), v["onion"], len(g["hops"])


def onion_hmac_ok(packet_hex, flip_bit=None):
    """What the first hop does with the packet: the shared secret from its own private key and the ephemeral key in the packet, the key mu, and the HMAC over the 1300 routing bytes and the associated data compared with the HMAC in the packet. flip_bit changes one bit of the routing bytes first."""
    v = jload("bolt04_onion_test.json")
    pkt = bytes.fromhex(packet_hex)
    if flip_bit is not None:
        pkt = pkt[:34] + C.flip_bit(pkt[34:1334], flip_bit) + pkt[1334:]
    ss = C.ecdh(bytes.fromhex(v["decode"][0]), pkt[1:34])
    mu = C.hmac256(b"mu", ss)
    return C.hmac256(mu, pkt[34:1334] + bytes.fromhex(v["generate"]["associated_data"])) == pkt[1334:1366]


def onion_size(n_hops):
    """The length of the packet built from the first n hops of the vector (the payloads are the vector's)."""
    g = jload("bolt04_onion_test.json")["generate"]
    hops = [(bytes.fromhex(h["pubkey"]), bytes.fromhex(h["payload"])) for h in g["hops"][:n_hops]]
    return len(C.sphinx_packet(bytes.fromhex(g["session_key"]), hops, bytes.fromhex(g["associated_data"])))


def shachain_vector(seed_hex, index):
    return C.shachain(bytes.fromhex(seed_hex), index).hex()


def bolt3_keys():
    """The key derivations of BOLT 3 appendix E, recomputed with the base secret and the per-commitment secret of the vector; returns (localpubkey ok, revocationpubkey ok, revocationprivkey ok, localprivkey as the secret plus the hash)."""
    bs, pcs = _hx(_vec("base_secret", "bolt03_transactions.md")), _hx(_vec("per_commitment_secret", "bolt03_transactions.md"))
    bp, pcp = C.pub(bs), C.pub(pcs)
    lp = C.pubkey_from_basepoint(bp, pcp)
    rp = C.revocation_pubkey(bp, pcp)
    rk = C.revocation_privkey(bs, pcs)
    return ("0x" + lp.hex() == _vec("localpubkey", "bolt03_transactions.md"), "0x" + rp.hex() == _vec("revocationpubkey", "bolt03_transactions.md"),
            "0x" + rk.hex() == _vec("revocationprivkey", "bolt03_transactions.md"), "0x" + bp.hex() == _vec("base_point", "bolt03_transactions.md"))


def invoice(which="coffee"):
    """Parse the invoice of the BOLT 11 examples that starts with lnbc2500u1 and asks for a cup of coffee."""
    t = text("bolt11_payment_encoding.md")
    m = re.search(r"(lnbc2500u1[a-z0-9]+)", t)
    return C.bolt11(m.group(1))


def count_sources_with(phrase):
    """In how many saved sources of the table does the phrase occur (whitespace collapsed)?"""
    import sen0401_ch14_sources_v1_0_0 as S
    n = 0
    for r in S.S:
        try:
            if re.sub(r"\s+", " ", phrase) in text(r[4]):
                n += 1
        except FileNotFoundError:
            pass
    return n


# ------------------------------------------------------------------------------------------------ the quotes of the sources
def quotes_report():
    """Every source's used passages re-read from the saved copy: returns (n_sources, n_fragments, failures[(id, fragment)], sources without a quote)."""
    import sen0401_ch14_quotes_v1_0_0 as Q
    import sen0401_ch14_sources_v1_0_0 as S
    files = {r[0]: r[4] for r in S.S}
    bad, n = [], 0
    for sid, frags in Q.QUOTES.items():
        for f in frags:
            n += 1
            if not has(files[sid], f):
                bad.append((sid, f[:70]))
    missing = [sid for sid in files if sid not in Q.QUOTES]
    return len(Q.QUOTES), n, bad, missing


def index_report():
    idx = json.load(open(os.path.join(EV, "sources_index_v1_0_0.json")))
    import sen0401_ch14_sources_v1_0_0 as S
    ok = []
    for sid, r in idx.items():
        if r.get("http") == 200 and r.get("sha256"):
            b = open(os.path.join(EV, r["file"]), "rb").read()
            if hashlib.sha256(b).hexdigest() == r["sha256"]:
                ok.append(sid)
    return len(S.S), len(ok), sorted(set(r[0] for r in S.S) - set(ok))
