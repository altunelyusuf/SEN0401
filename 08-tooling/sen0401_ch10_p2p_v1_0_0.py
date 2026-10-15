#!/usr/bin/env python3
"""SEN0401 chapter 10 (The Bitcoin Network): an independent implementation of the pieces of the Bitcoin peer-to-peer protocol that the chapter describes, in the
standard library only. It does not use Bitcoin Core code. The regtest run (sen0401_ch10_regtest_v1_0_0.py) uses it as a probe against Bitcoin Core 31.1; the
chapter's claims (sen0401_ch10_leaves_v1_0_0.py) use its pure functions to recompute from the recorded bytes what the node answered.
Contents: message framing; the version message; headers, inv, getdata; compact blocks (BIP 152: SipHash-2-4 short identifiers); bloom filters (BIP 37: MurmurHash3,
filterload, merkleblock and the partial merkle tree); compact block filters (BIP 158: Golomb-coded sets, filter headers of BIP 157); addrv2 (BIP 155)."""
__version__ = "1.0.0"
import hashlib, math, os, socket, struct, threading, time

MAGIC = {"regtest": bytes.fromhex("fabfb5da"), "main": bytes.fromhex("f9beb4d9")}
PROTOCOL_VERSION = 70016
SERVICE_BITS = {1: "NETWORK", 4: "BLOOM", 8: "WITNESS", 64: "COMPACT_FILTERS", 1024: "NETWORK_LIMITED", 2048: "P2P_V2"}
MSG = {"TX": 1, "BLOCK": 2, "FILTERED_BLOCK": 3, "CMPCT_BLOCK": 4, "WTX": 5, "WITNESS_FLAG": 1 << 30}


def sha256d(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


# ----------------------------------------------------------------------------------------------------------------- compact size and framing
def cs_dec(b, i):
    n = b[i]
    if n < 253:
        return n, i + 1
    if n == 253:
        return int.from_bytes(b[i + 1:i + 3], "little"), i + 3
    if n == 254:
        return int.from_bytes(b[i + 1:i + 5], "little"), i + 5
    return int.from_bytes(b[i + 1:i + 9], "little"), i + 9


def cs_enc(n):
    if n < 253:
        return bytes([n])
    if n < 65536:
        return b"\xfd" + n.to_bytes(2, "little")
    if n < 2 ** 32:
        return b"\xfe" + n.to_bytes(4, "little")
    return b"\xff" + n.to_bytes(8, "little")


def frame(cmd, payload, net="regtest"):
    return MAGIC[net] + cmd.encode().ljust(12, b"\0") + struct.pack("<I", len(payload)) + sha256d(payload)[:4] + payload


def deframe(buf, net="regtest"):
    """One message from the front of buf: (cmd, payload, rest) or None when incomplete."""
    if len(buf) < 24:
        return None
    if buf[:4] != MAGIC[net]:
        raise ValueError("bad magic %s" % buf[:4].hex())
    cmd = buf[4:16].rstrip(b"\0").decode("ascii", "replace")
    n = struct.unpack("<I", buf[16:20])[0]
    if len(buf) < 24 + n:
        return None
    payload = buf[24:24 + n]
    if sha256d(payload)[:4] != buf[20:24]:
        raise ValueError("bad checksum")
    return cmd, payload, buf[24 + n:]


def netaddr(services, ip="127.0.0.1", port=0):
    return struct.pack("<Q", services) + b"\0" * 10 + b"\xff\xff" + socket.inet_aton(ip) + struct.pack(">H", port)


def version_payload(services=1032, relay=True, start_height=0, ua="/sen0401-ch10-probe:1.0/", version=PROTOCOL_VERSION, nonce=None, ts=None):
    nonce = nonce if nonce is not None else int.from_bytes(os.urandom(8), "little")
    ts = ts if ts is not None else int(time.time())
    return (struct.pack("<iQq", version, services, ts) + netaddr(1, "127.0.0.1", 0) + netaddr(services, "127.0.0.1", 0) + struct.pack("<Q", nonce)
            + cs_enc(len(ua)) + ua.encode() + struct.pack("<i", start_height) + (b"\x01" if relay else b"\x00"))


def parse_version(p):
    version, services, ts = struct.unpack("<iQq", p[:20])
    i = 20
    recv = (struct.unpack("<Q", p[i:i + 8])[0], socket.inet_ntoa(p[i + 8 + 12:i + 8 + 16]), struct.unpack(">H", p[i + 24:i + 26])[0]); i += 26
    frm = (struct.unpack("<Q", p[i:i + 8])[0], socket.inet_ntoa(p[i + 8 + 12:i + 8 + 16]), struct.unpack(">H", p[i + 24:i + 26])[0]); i += 26
    nonce = struct.unpack("<Q", p[i:i + 8])[0]; i += 8
    n, i = cs_dec(p, i)
    ua = p[i:i + n].decode("ascii", "replace"); i += n
    h = struct.unpack("<i", p[i:i + 4])[0]; i += 4
    relay = bool(p[i]) if i < len(p) else None
    return {"version": version, "services": services, "services_names": service_names(services), "timestamp": ts, "addr_recv": recv, "addr_from": frm, "nonce": nonce,
            "user_agent": ua, "start_height": h, "relay": relay, "payload_bytes": len(p)}


def service_names(s):
    return [n for b, n in sorted(SERVICE_BITS.items()) if s & b]


# ----------------------------------------------------------------------------------------------------------------- a probe peer
class Peer:
    """A TCP connection that speaks version 1 of the transport (plaintext). A reader thread keeps every message with the time it arrived."""

    def __init__(self, port, host="127.0.0.1", net="regtest"):
        self.net, self.msgs, self.buf, self.closed, self.lock = net, [], b"", False, threading.Lock()
        self.s = socket.create_connection((host, port), timeout=10)
        self.s.settimeout(0.5)
        self.t0 = time.time()
        self.th = threading.Thread(target=self._read, daemon=True)
        self.th.start()

    def _read(self):
        while not self.closed:
            try:
                d = self.s.recv(1 << 20)
            except socket.timeout:
                continue
            except OSError:
                self.closed = True
                break
            if not d:
                self.closed = True
                break
            self.buf += d
            while True:
                try:
                    r = deframe(self.buf, self.net)
                except ValueError:
                    self.closed = True
                    return
                if not r:
                    break
                cmd, payload, self.buf = r
                with self.lock:
                    self.msgs.append((round(time.time() - self.t0, 3), cmd, payload))
                if cmd == "ping":
                    try:
                        self.send("pong", payload)
                    except OSError:
                        pass

    def send(self, cmd, payload=b""):
        self.s.sendall(frame(cmd, payload, self.net))

    def wait(self, cmd, timeout=15, start=0):
        """The first message named cmd at or after index start (index, time, payload) or None."""
        end = time.time() + timeout
        while time.time() < end:
            with self.lock:
                for k in range(start, len(self.msgs)):
                    if self.msgs[k][1] == cmd:
                        return k, self.msgs[k][0], self.msgs[k][2]
            if self.closed:
                break
            time.sleep(0.05)
        return None

    def commands(self, start=0):
        with self.lock:
            return [(t, c, len(p)) for t, c, p in self.msgs[start:]]

    def handshake(self, services=1032, relay=True, pre_verack=(), start_height=0, ua="/sen0401-ch10-probe:1.0/"):
        """version out; version in; the messages of pre_verack [(cmd, payload)] between; verack out. Returns the parsed version of the node."""
        self.send("version", version_payload(services, relay, start_height, ua))
        r = self.wait("version", 10)
        v = parse_version(r[2])
        for c, p in pre_verack:
            self.send(c, p)
        self.send("verack")
        self.wait("verack", 10)
        return v

    def sync_to_tip(self, tip_hash_display):
        """Asks for the headers after the tip. The node then knows this peer has every header, which it needs to announce a new block by headers or compact block."""
        k = len(self.msgs)
        self.send("getheaders", getheaders_payload([bytes.fromhex(tip_hash_display)[::-1]]))
        return self.wait("headers", 10, start=k)

    def close(self):
        self.closed = True
        try:
            self.s.close()
        except OSError:
            pass


# ----------------------------------------------------------------------------------------------------------------- headers, inv, getdata, locators
def getheaders_payload(locator_hashes_internal, stop=b"\0" * 32, version=PROTOCOL_VERSION):
    return struct.pack("<I", version) + cs_enc(len(locator_hashes_internal)) + b"".join(locator_hashes_internal) + stop


def parse_headers(p):
    n, i = cs_dec(p, 0)
    out = []
    for _ in range(n):
        out.append(p[i:i + 80]); i += 80
        c, i = cs_dec(p, i)
        assert c == 0
    assert i == len(p)
    return out


def header_hash(h80):
    return sha256d(h80)[::-1].hex()


def inv_payload(items):
    return cs_enc(len(items)) + b"".join(struct.pack("<I", t) + bytes(h) for t, h in items)


def parse_inv(p):
    n, i = cs_dec(p, 0)
    out = []
    for _ in range(n):
        out.append((struct.unpack("<I", p[i:i + 4])[0], p[i + 4:i + 36][::-1].hex())); i += 36
    return out


# ----------------------------------------------------------------------------------------------------------------- transactions and blocks
def parse_tx_bytes(b, i=0):
    """(tx dict, next index). Keeps the raw serialization and the txid and wtxid (display order)."""
    s = i
    ver = int.from_bytes(b[i:i + 4], "little", signed=True); i += 4
    segwit = b[i] == 0 and b[i + 1] == 1
    if segwit:
        i += 2
    n, i = cs_dec(b, i)
    vin = []
    for _ in range(n):
        txid = b[i:i + 32]; vout = int.from_bytes(b[i + 32:i + 36], "little"); i += 36
        sl, i = cs_dec(b, i); ss = b[i:i + sl]; i += sl
        seq = int.from_bytes(b[i:i + 4], "little"); i += 4
        vin.append({"txid": txid[::-1].hex(), "vout": vout, "scriptSig": ss, "sequence": seq, "witness": []})
    n, i = cs_dec(b, i)
    vout = []
    for _ in range(n):
        v = int.from_bytes(b[i:i + 8], "little"); i += 8
        sl, i = cs_dec(b, i); vout.append({"value": v, "spk": b[i:i + sl]}); i += sl
    if segwit:
        for k in range(len(vin)):
            c, i = cs_dec(b, i)
            for _ in range(c):
                l, i = cs_dec(b, i); vin[k]["witness"].append(b[i:i + l]); i += l
    lock = int.from_bytes(b[i:i + 4], "little"); i += 4
    raw = b[s:i]
    base = raw[:4] + (raw[6:] if segwit else raw[4:])
    if segwit:   # strip the witness: rebuild the non-witness serialization
        base = ver.to_bytes(4, "little", signed=True) + cs_enc(len(vin))
        for x in vin:
            base += bytes.fromhex(x["txid"])[::-1] + x["vout"].to_bytes(4, "little") + cs_enc(len(x["scriptSig"])) + x["scriptSig"] + x["sequence"].to_bytes(4, "little")
        base += cs_enc(len(vout))
        for o in vout:
            base += o["value"].to_bytes(8, "little") + cs_enc(len(o["spk"])) + o["spk"]
        base += lock.to_bytes(4, "little")
    else:
        base = raw
    return {"version": ver, "vin": vin, "vout": vout, "locktime": lock, "raw": raw, "txid": sha256d(base)[::-1].hex(), "wtxid": sha256d(raw)[::-1].hex(),
            "size": len(raw), "base_size": len(base), "weight": len(base) * 3 + len(raw)}, i


def parse_block(b):
    hdr = b[:80]
    n, i = cs_dec(b, 80)
    txs = []
    for _ in range(n):
        t, i = parse_tx_bytes(b, i)
        txs.append(t)
    assert i == len(b)
    return {"header": hdr, "hash": header_hash(hdr), "merkle_root": hdr[36:68][::-1].hex(), "txs": txs}


def merkle_root(txids_display):
    """The merkle root (display order) of a list of txids (display order): pairs hashed with double SHA-256, the last one duplicated on odd levels."""
    lvl = [bytes.fromhex(t)[::-1] for t in txids_display]
    while len(lvl) > 1:
        if len(lvl) % 2:
            lvl.append(lvl[-1])
        lvl = [sha256d(lvl[k] + lvl[k + 1]) for k in range(0, len(lvl), 2)]
    return lvl[0][::-1].hex()


def merkle_branch(txids_display, index):
    """The merkle path of the transaction at `index`: the sibling hashes (display order) from the leaf up to the root, and the root reached by following them."""
    lvl = [bytes.fromhex(t)[::-1] for t in txids_display]
    idx, path = index, []
    while len(lvl) > 1:
        if len(lvl) % 2:
            lvl.append(lvl[-1])
        path.append(lvl[idx ^ 1][::-1].hex())
        lvl = [sha256d(lvl[k] + lvl[k + 1]) for k in range(0, len(lvl), 2)]
        idx //= 2
    return path, lvl[0][::-1].hex()


def follow_branch(txid_display, index, path_display):
    h = bytes.fromhex(txid_display)[::-1]
    for sib in path_display:
        s = bytes.fromhex(sib)[::-1]
        h = sha256d(h + s) if index % 2 == 0 else sha256d(s + h)
        index //= 2
    return h[::-1].hex()


def parse_merkleblock(p):
    """(header80, total_transactions, hashes (display), flag bits) of a merkleblock message or of the hex of gettxoutproof."""
    hdr = p[:80]
    total = struct.unpack("<I", p[80:84])[0]
    n, i = cs_dec(p, 84)
    hashes = [p[i + 32 * k:i + 32 * k + 32][::-1].hex() for k in range(n)]; i += 32 * n
    fl, i = cs_dec(p, i)
    flags = p[i:i + fl]
    bits = [(flags[k // 8] >> (k % 8)) & 1 for k in range(fl * 8)]
    return hdr, total, hashes, bits


def partial_merkle_tree(total, hashes, bits):
    """Walks the partial merkle tree of BIP 37: returns (root (display), matched txids (display), bits consumed, hashes consumed)."""
    height = 0
    while (1 << height) < total:
        height += 1
    pos = {"bit": 0, "hash": 0}
    matched = []

    def width(h):
        return (total + (1 << h) - 1) >> h

    def rec(h, p):
        flag = bits[pos["bit"]]; pos["bit"] += 1
        if h == 0 or not flag:
            x = hashes[pos["hash"]]; pos["hash"] += 1
            if h == 0 and flag:
                matched.append(x)
            return bytes.fromhex(x)[::-1]
        left = rec(h - 1, p * 2)
        right = rec(h - 1, p * 2 + 1) if p * 2 + 1 < width(h - 1) else left
        return sha256d(left + right)

    root = rec(height, 0)
    return root[::-1].hex(), matched, pos["bit"], pos["hash"]


# ----------------------------------------------------------------------------------------------------------------- SipHash-2-4 (BIP 152 short ids, BIP 158 filters)
M64 = (1 << 64) - 1


def siphash24(k0, k1, data):
    v0 = k0 ^ 0x736f6d6570736575
    v1 = k1 ^ 0x646f72616e646f6d
    v2 = k0 ^ 0x6c7967656e657261
    v3 = k1 ^ 0x7465646279746573
    rotl = lambda x, b: ((x << b) | (x >> (64 - b))) & M64

    def rnd():
        nonlocal v0, v1, v2, v3
        v0 = (v0 + v1) & M64; v1 = rotl(v1, 13); v1 ^= v0; v0 = rotl(v0, 32)
        v2 = (v2 + v3) & M64; v3 = rotl(v3, 16); v3 ^= v2
        v0 = (v0 + v3) & M64; v3 = rotl(v3, 21); v3 ^= v0
        v2 = (v2 + v1) & M64; v1 = rotl(v1, 17); v1 ^= v2; v2 = rotl(v2, 32)

    n = len(data)
    for k in range(0, n - n % 8, 8):
        m = int.from_bytes(data[k:k + 8], "little")
        v3 ^= m; rnd(); rnd(); v0 ^= m
    last = (n & 0xff) << 56 | int.from_bytes(data[n - n % 8:], "little")
    v3 ^= last; rnd(); rnd(); v0 ^= last
    v2 ^= 0xff
    for _ in range(4):
        rnd()
    return (v0 ^ v1 ^ v2 ^ v3) & M64


def siphash_test_vector():
    """The reference test vector of the SipHash paper: key 00..0f, message 00..0e (15 bytes) gives a129ca6149be45e5."""
    k = bytes(range(16))
    return "%016x" % siphash24(int.from_bytes(k[:8], "little"), int.from_bytes(k[8:], "little"), bytes(range(15)))


# ----------------------------------------------------------------------------------------------------------------- compact blocks (BIP 152)
def parse_cmpctblock(p):
    hdr = p[:80]
    nonce = p[80:88]
    n, i = cs_dec(p, 88)
    ids = [int.from_bytes(p[i + 6 * k:i + 6 * k + 6], "little") for k in range(n)]; i += 6 * n
    m, i = cs_dec(p, i)
    pre = []
    last = -1
    for _ in range(m):
        d, i = cs_dec(p, i)
        t, i = parse_tx_bytes(p, i)
        last = last + d + 1
        pre.append((last, t))
    assert i == len(p)
    return {"header": hdr, "nonce": nonce, "short_ids": ids, "prefilled": pre, "bytes": len(p)}


def short_id_key(header80, nonce8):
    k = hashlib.sha256(header80 + nonce8).digest()
    return int.from_bytes(k[:8], "little"), int.from_bytes(k[8:16], "little")


def short_id(header80, nonce8, wtxid_display):
    k0, k1 = short_id_key(header80, nonce8)
    return siphash24(k0, k1, bytes.fromhex(wtxid_display)[::-1]) & 0xffffffffffff


def sendcmpct(announce, version=2):
    return (b"\x01" if announce else b"\x00") + struct.pack("<Q", version)


# ----------------------------------------------------------------------------------------------------------------- bloom filters (BIP 37)
def murmur3_32(seed, data):
    c1, c2 = 0xcc9e2d51, 0x1b873593
    h = seed & 0xffffffff
    n = len(data)
    for k in range(0, n - n % 4, 4):
        k1 = int.from_bytes(data[k:k + 4], "little")
        k1 = (k1 * c1) & 0xffffffff; k1 = ((k1 << 15) | (k1 >> 17)) & 0xffffffff; k1 = (k1 * c2) & 0xffffffff
        h ^= k1; h = ((h << 13) | (h >> 19)) & 0xffffffff; h = (h * 5 + 0xe6546b64) & 0xffffffff
    tail = data[n - n % 4:]
    k1 = 0
    for j in range(len(tail) - 1, -1, -1):
        k1 = (k1 << 8) | tail[j]
    if tail:
        k1 = (k1 * c1) & 0xffffffff; k1 = ((k1 << 15) | (k1 >> 17)) & 0xffffffff; k1 = (k1 * c2) & 0xffffffff; h ^= k1
    h ^= n
    h ^= h >> 16; h = (h * 0x85ebca6b) & 0xffffffff; h ^= h >> 13; h = (h * 0xc2b2ae35) & 0xffffffff; h ^= h >> 16
    return h


class Bloom:
    """The bloom filter of BIP 37, sized as Bitcoin Core sizes it from the number of elements and the false positive rate."""

    def __init__(self, n_elements, fp_rate, tweak=0, flags=0, max_size=36000, max_hash=50):
        self.size = int(min(-1 / (math.log(2) ** 2) * n_elements * math.log(fp_rate), max_size * 8)) // 8 or 1
        self.data = bytearray(self.size)
        self.k = int(min(self.size * 8 / n_elements * math.log(2), max_hash)) if n_elements else 1
        self.k = max(self.k, 1)
        self.tweak, self.flags = tweak, flags

    def _h(self, i, data):
        return murmur3_32((i * 0xFBA4C795 + self.tweak) & 0xffffffff, data) % (self.size * 8)

    def insert(self, data):
        for i in range(self.k):
            b = self._h(i, data)
            self.data[b >> 3] |= 1 << (b & 7)

    def contains(self, data):
        return all(self.data[(b := self._h(i, data)) >> 3] & (1 << (b & 7)) for i in range(self.k))

    def payload(self):
        return cs_enc(len(self.data)) + bytes(self.data) + struct.pack("<II", self.k, self.tweak) + bytes([self.flags])


class ToyBloom:
    """The book's teaching filter: N bits and M hash functions (here SHA-256 with the function number as a prefix), to count false positives."""

    def __init__(self, n_bits, m_funcs):
        self.n, self.m, self.bits = n_bits, m_funcs, [0] * n_bits

    def positions(self, pattern):
        return [int.from_bytes(hashlib.sha256(bytes([i]) + pattern.encode()).digest()[:8], "big") % self.n for i in range(self.m)]

    def add(self, pattern):
        for p in self.positions(pattern):
            self.bits[p] = 1

    def test(self, pattern):
        return all(self.bits[p] for p in self.positions(pattern))


# ----------------------------------------------------------------------------------------------------------------- compact block filters (BIP 157/158)
GCS_P, GCS_M = 19, 784931


def _fastrange(h, f):
    return (h * f) >> 64


def gcs_hashed_set(k0, k1, elements, m=GCS_M):
    elems = sorted(set(elements))
    f = len(elems) * m
    return sorted(_fastrange(siphash24(k0, k1, e), f) for e in elems), len(elems)


def golomb_encode(values_sorted, p=GCS_P):
    bits = []
    last = 0
    for v in values_sorted:
        d = v - last; last = v
        q, r = d >> p, d & ((1 << p) - 1)
        bits += [1] * q + [0] + [(r >> (p - 1 - j)) & 1 for j in range(p)]
    while len(bits) % 8:
        bits.append(0)
    return bytes(int("".join(map(str, bits[k:k + 8])), 2) for k in range(0, len(bits), 8))


def golomb_decode(data, n, p=GCS_P):
    bits = "".join(format(x, "08b") for x in data)
    i, last, out = 0, 0, []
    for _ in range(n):
        q = 0
        while bits[i] == "1":
            q += 1; i += 1
        i += 1
        r = int(bits[i:i + p], 2); i += p
        last += (q << p) + r
        out.append(last)
    return out


def block_filter_elements(block, prev_scripts):
    """The elements of the basic filter: the output scripts of the block (not empty, not OP_RETURN) and the scripts of the outputs it spends. prev_scripts: list of bytes."""
    els = []
    for t in block["txs"]:
        for o in t["vout"]:
            if o["spk"] and o["spk"][0] != 0x6a:
                els.append(o["spk"])
    els += [s for s in prev_scripts if s]
    return els


def basic_filter(block_hash_display, elements):
    """The serialized basic filter of BIP 158: a compact size for N, then the Golomb-Rice coded deltas of the SipHash values (key = first 16 bytes of the block hash)."""
    hb = bytes.fromhex(block_hash_display)[::-1]
    k0, k1 = int.from_bytes(hb[:8], "little"), int.from_bytes(hb[8:16], "little")
    vals, n = gcs_hashed_set(k0, k1, elements)
    return cs_enc(n) + golomb_encode(vals), n


def filter_match(filter_bytes, block_hash_display, script):
    hb = bytes.fromhex(block_hash_display)[::-1]
    k0, k1 = int.from_bytes(hb[:8], "little"), int.from_bytes(hb[8:16], "little")
    n, i = cs_dec(filter_bytes, 0)
    vals = set(golomb_decode(filter_bytes[i:], n))
    return _fastrange(siphash24(k0, k1, script), n * GCS_M) in vals


def filter_header(filter_bytes, prev_header_display):
    """BIP 157: header = double SHA-256 of (double SHA-256 of the filter, then the previous header), all in internal byte order; returns display order."""
    return sha256d(sha256d(filter_bytes) + bytes.fromhex(prev_header_display)[::-1])[::-1].hex()


def getcfilters_payload(start, stop_hash_display, ftype=0):
    return bytes([ftype]) + struct.pack("<I", start) + bytes.fromhex(stop_hash_display)[::-1]


def parse_cfilter_msg(p):
    n, i = cs_dec(p, 33)
    return {"type": p[0], "block_hash": p[1:33][::-1].hex(), "filter": p[i:i + n]}


# ----------------------------------------------------------------------------------------------------------------- addrv2 (BIP 155)
def parse_addrv2(p):
    n, i = cs_dec(p, 0)
    out = []
    for _ in range(n):
        t = struct.unpack("<I", p[i:i + 4])[0]; i += 4
        svc, i = cs_dec(p, i)
        net = p[i]; i += 1
        l, i = cs_dec(p, i)
        a = p[i:i + l]; i += l
        port = struct.unpack(">H", p[i:i + 2])[0]; i += 2
        out.append({"time": t, "services": svc, "network": net, "addr_len": l, "addr": a.hex(), "port": port})
    assert i == len(p)
    return out


def parse_addr_v1(p):
    n, i = cs_dec(p, 0)
    out = []
    for _ in range(n):
        t = struct.unpack("<I", p[i:i + 4])[0]
        out.append({"time": t, "services": struct.unpack("<Q", p[i + 4:i + 12])[0], "addr": p[i + 12:i + 28].hex(), "port": struct.unpack(">H", p[i + 28:i + 30])[0]}); i += 30
    return out


# ----------------------------------------------------------------------------------------------------------------- numbers
def entropy_bits_per_byte(b):
    if not b:
        return 0.0
    c = [0] * 256
    for x in b:
        c[x] += 1
    return -sum(v / len(b) * math.log2(v / len(b)) for v in c if v)


# ----------------------------------------------------------------------------------------------------------------- a segwit v0 address from a 20-byte hash (BIP 173), to pay a light client's key in the test
_B32 = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if (b >> i) & 1 else 0
    return chk


def p2wpkh_address(hash20, hrp="bcrt"):
    data = [0] + [x for x in _convert8to5(hash20)]
    pm = _polymod([ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp] + data + [0] * 6) ^ 1
    chk = [(pm >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + "1" + "".join(_B32[d] for d in data + chk)


def _convert8to5(b):
    acc, bits, out = 0, 0, []
    for v in b:
        acc = (acc << 8) | v
        bits += 8
        while bits >= 5:
            bits -= 5
            out.append((acc >> bits) & 31)
    if bits:
        out.append((acc << (5 - bits)) & 31)
    return out
