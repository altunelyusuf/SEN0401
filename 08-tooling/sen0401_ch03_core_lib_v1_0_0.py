"""sen0401_ch03_core_lib v1.0.0 - the chapter library of the chapter 3 deck (Bitcoin Core, the reference implementation) and of its page tab 'chapter code'.
Standard library only (hashlib, hmac, json, struct, base64 through the caller), so it runs unchanged in the page's Python. Every constant below is read from a file saved with the
chapter: the evidence of the offline run of Bitcoin Core 31.1 (08-tooling/ch03-evidence: getblockchaininfo, Alice's transaction decoded, the release checksums, the registry query),
the public data of block 123,456 (saved from the Blockstream API on 2026-09-28) and the book's own examples (the curl reply, the cookie, the rpcauth helper). The deck shows short
listings; the helper functions here keep every listing within one line. Nothing here is typed from memory: where a value came from a saved file, its name stands in the comment."""
__version__ = "1.0.0"
import hashlib, hmac, json, struct

COIN = 100_000_000            # satoshis in one bitcoin
SAFE = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,;-_/:?@()"   # the characters Bitcoin Core lets through into an alert command (the set the chapter corpus read from Bitcoin Core's source)

# ---- releases and tags: an excerpt of the 369 tags that `git ls-remote --tags` listed on 2026-10-04 (git_ls_remote_tags_bitcoin_v1_2_0.txt)
TAGS = 'v0.9.5 v0.10.0 v0.10.0rc1 v0.21.2 v22.0 v22.0rc1 v29.0 v30.0 v31.0 v31.0rc4 v31.1 v31.1rc1 v32.0rc1'.split()
LAYOUT = {"bin": ["bitcoin", "bitcoin-cli", "bitcoin-qt", "bitcoin-tx", "bitcoin-util", "bitcoin-wallet", "bitcoind"],      # release_layout_31_1_v1_0_0.txt
          "libexec": ["bitcoin-gui", "bitcoin-node", "test_bitcoin"]}
ROLE = {"bitcoin": "starts the other programs", "bitcoin-cli": "calls the node by name", "bitcoin-qt": "node with a window",
        "bitcoin-tx": "builds and edits transactions", "bitcoin-util": "small helper commands", "bitcoin-wallet": "works on wallet files",
        "bitcoind": "the node, as a daemon"}
SUMS = {"bitcoin-31.1-x86_64-linux-gnu.tar.gz": "b80d9c3e04da78fb6f0569685673418cf686fadba9042d926d13fb87ff503f9e",     # SHA256SUMS of release 31.1 (release_SHA256SUMS_31_1_v1_1_0.txt)
        "bitcoin-31.1-arm64-apple-darwin.tar.gz": "16a097c09fbd7eb78b240ce1dae123663ea2e5e377cfd6a951e71e227e23cf2f"}
RECOMPUTED = "b80d9c3e04da78fb6f0569685673418cf686fadba9042d926d13fb87ff503f9e"      # sha256 of the downloaded x86_64 archive, recomputed on 2026-10-02 (release_recheck_31_1_v1_1_0.txt)

# ---- configuration
CONF_TEXT = "# a bitcoin.conf like the book's samples\ndbcache=450\ntxindex=1\n"
MAXMEMPOOL_MB, BLOCKSONLY_MB = 300, 5      # defaults of -maxmempool and of blocks-only mode (Bitcoin Core 31.1 help and doc/reduce-memory.md)

# ---- the node's interface
GETBLOCKCHAININFO = '{\n  "chain": "main",\n  "blocks": 0,\n  "headers": 0,\n  "bestblockhash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",\n  "bits": "1d00ffff",\n  "target": "00000000ffff0000000000000000000000000000000000000000000000000000",\n  "difficulty": 1,\n  "time": 1231006505,\n  "mediantime": 1231006505,\n  "verificationprogress": 7.061365181330129e-10,\n  "initialblockdownload": true,\n  "chainwork": "0000000000000000000000000000000000000000000000000000000100010001",\n  "size_on_disk": 293,\n  "pruned": false,\n  "warnings": [\n  ]\n}'      # the answer of bitcoin-cli getblockchaininfo on the offline node of release 31.1, 2026-09-28
REPLY = '{"result":{"chain":"main","blocks":799278,"headers":799278,"bestblockhash":"000000000000000000018387c50988ec705a95d6f765b206b6629971e6978879","difficulty":53911173001054.59,"time":1689703111,"mediantime":1689701260,"verificationprogress":0.9999979206082515,"initialblockdownload":false,"chainwork":"00000000000000000000000000000000000000004f3e111bf32bcb47f9dfad5b","size_on_disk":563894577967,"pruned":false,"warnings":""},"error":null,"id":"curltest"}'      # the reply printed by the book's curl example (Mastering Bitcoin 3e, chapter 3)
COOKIE = "17c9b71cef21b893e1a019f4bc071950c7942f49796ed061b274031b17b19cd0"      # the book's example .cookie secret: 32 random bytes as 64 hexadecimal characters
SALT = "00112233445566778899aabbccddeeff"      # a 16-byte salt written as 32 hexadecimal characters, as share/rpcauth/rpcauth.py prints one

# ---- transactions and blocks
ALICE_HEX = '01000000000101eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a0100000000ffffffff02204e0000000000002251203b41daba4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068f8240100000000001600147752c165ea7be772b2c0acb7f4d6047ae6f4768e0141cf5efe2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e521c00b51be739df2f899c49dc267c0ad280aca6dab0d2fa2b42a45182fc83e817130100000000'      # Alice's transaction as the book prints it (segregated witness serialisation)
ALICE_DECODED = '{\n  "txid": "466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177",\n  "hash": "f7cdbc7cf8b910d35cc69962e791138624e4eae7901010a6da4c02e7d238cdac",\n  "version": 1,\n  "size": 194,\n  "vsize": 143,\n  "weight": 569,\n  "locktime": 0,\n  "vin": [\n    {\n      "txid": "4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19278fe33aeb",\n      "vout": 1,\n      "scriptSig": {\n        "asm": "",\n        "hex": ""\n      },\n      "txinwitness": [\n        "cf5efe2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e521c00b51be739df2f899c49dc267c0ad280aca6dab0d2fa2b42a45182fc83e8171301"\n      ],\n      "sequence": 4294967295\n    }\n  ],\n  "vout": [\n    {\n      "value": 0.00020000,\n      "n": 0,\n      "scriptPubKey": {\n        "asm": "1 3b41daba4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068",\n        "desc": "rawtr(3b41daba4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068)#38d6v6ev",\n        "hex": "51203b41daba4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068",\n        "address": "bc1p8dqa4wjvnt890qmfws83te0v3qxzsfu7ul63kp7u56w8qc0qwp5qv995qn",\n        "type": "witness_v1_taproot"\n      }\n    },\n    {\n      "value": 0.00075000,\n      "n": 1,\n      "scriptPubKey": {\n        "asm": "0 7752c165ea7be772b2c0acb7f4d6047ae6f4768e",\n        "desc": "addr(bc1qwafvze0200nh9vkq4jmlf4sy0tn0ga5w0zpkpg)#qq404gts",\n        "hex": "00147752c165ea7be772b2c0acb7f4d6047ae6f4768e",\n        "address": "bc1qwafvze0200nh9vkq4jmlf4sy0tn0ga5w0zpkpg",\n        "type": "witness_v0_keyhash"\n      }\n    }\n  ]\n}'      # the same transaction decoded by Bitcoin Core 31.1 (decoderawtransaction), 2026-09-28
BLOCK_123456 = {'id': '0000000000002917ed80650c6174aac8dfc46f5fe36480aaef682ff6cd83c3ca', 'height': 123456, 'version': 1, 'timestamp': 1305200806, 'merkle_root': '0e60651a9934e8f0decd1c5fde39309e48fca0cd1c84a21ddfde95033762d86c', 'previousblockhash': '0000000000000b60bc96a44724fd72daf9b92cf8ad00510b5224c6253ac40095', 'mediantime': 1305197900, 'nonce': 2436437219, 'bits': 443192243}      # block 123,456 as the Blockstream API reported it on 2026-09-28
TXIDS_123456 = ['5b75086dafeede555fc8f9a810d8b10df57c46f9f176ccc3dd8d2fa20edd685b', 'e3d0425ab346dd5b76f44c222a4bb5d16640a4247050ef82462ab17e229c83b4', '137d247eca8b99dee58e1e9232014183a5c5a9e338001a0109df32794cdcc92e', '5fd167f7b8c417e59106ef5acfe181b09d71b8353a61a55a2f01aa266af5412d', '60925f1948b71f429d514ead7ae7391e0edf965bf5a60331398dae24c6964774', 'd4d5fc1529487527e9873256934dfb1e4cdcb39f4c0509577ca19bfad6c5d28f', '7b29d65e5018c56a33652085dbb13f2df39a1a9942bfe1f7e78e97919a6bdea2', '0b89e120efd0a4674c127a76ff5f7590ca304e6a064fbc51adffbd7ce3a3deef', '603f2044da9656084174cfb5812feaf510f862d3addcf70cacce3dc55dab446e', '9a4ed892b43a4df916a7a1213b78e83cd83f5695f635d535c94b2b65ffb144d3', 'dda726e3dad9504dce5098dfab5064ecd4a7650bfe854bb2606da3152b60e427', 'e46ea8b4d68719b65ead930f07f1f3804cb3701014f8e6d76c4bdbc390893b94', '864a102aeedf53dd9b2baab4eeb898c5083fde6141113e0606b664c41fe15e1f']      # the 13 transaction ids of block 123,456, in block order
BLOCK_TIMES = {123445: 1305191152, 123446: 1305191688, 123447: 1305193319, 123448: 1305194571, 123449: 1305194986, 123450: 1305195947, 123451: 1305197900, 123452: 1305199436, 123453: 1305200301, 123454: 1305200460, 123455: 1305200584, 123456: 1305200806}      # the timestamps of blocks 123,445 to 123,456

# ---- alternative toolkits: registry, latest release, its date (queried 2026-10-02, registry_toolkits_v1_1_0.json)
QUERIED = "2026-10-02"
TOOLKITS = {'bcoin': ('npm', '1.0.2', '2018-07-13'), 'bitcore-lib': ('npm', '10.10.7', '2025-07-21'), 'bitcoinjs-lib': ('npm', '7.0.2', '2026-09-07'), 'python-bitcoinlib': ('PyPI', '0.12.2', '2023-06-03'), 'pycoin': ('PyPI', '0.92718.20260405', '2026-04-05'), 'btcd': ('Go module proxy', 'v0.26.2', '2026-07-24'), 'rust-bitcoin': ('crates.io', '0.32.102', '2026-07-22'), 'bitcoinj': ('Maven Central', '0.17', '2025-02-21'), 'bitcoin-s': ('Maven Central', '1.9.10', '2025-01-25')}


def version_key(tag):
    """'v0.21.2' -> (0, 21, 2): the numbers of a release tag, so that tags sort by number and not by letters"""
    return tuple(int(x) for x in tag.lstrip("v").split("rc")[0].split("."))


def parse_conf(text):
    """name=value lines of a configuration file -> dict; blank lines and # comments are skipped"""
    return dict(l.split("=", 1) for l in text.splitlines() if l.strip() and not l.startswith("#"))


def cache_split(total_mib):
    """how Bitcoin Core divides -dbcache: block index database (at most 2 MiB, an eighth of the total), chain state database (at most 8 MiB, half of the rest), the rest for the coins cache"""
    a = min(total_mib // 8, 2); rest = total_mib - a
    b = min(rest // 2, 8)
    return (a, b, rest - b)


def check_options(opts):
    """a plain verdict on a set of node options: ('ok', why) or ('refused', why); the txindex rule was recorded on release 31.1 (prune_txindex_31_1_v1_0_0.txt)"""
    p, t = opts.get("prune", 0), opts.get("txindex", 0)
    if p and t:
        return ("refused", "prune mode is incompatible with txindex")
    if p > 1 and p < 550:
        return ("refused", "automatic pruning needs a target of at least 550 MiB")
    return ("ok", "no conflict")


def clean(msg):
    """the alert text after Bitcoin Core has removed every character that is not in SAFE"""
    return "".join(c for c in msg if c in SAFE)


def alert_command(template, msg):
    """-alertnotify: the cleaned message in single quotes replaces %s in the command"""
    return template.replace("%s", "'" + clean(msg) + "'")


def rpc_body(method, *params):
    """the JSON text of a JSON-RPC call, as the book's curl example sends it"""
    return json.dumps({"jsonrpc": "1.0", "id": "curltest", "method": method, "params": list(params)})


def rpcauth(user, password, salt):
    """the line for rpcauth= in bitcoin.conf: user:salt$HMAC-SHA256(salt, password)"""
    return "%s:%s$%s" % (user, salt, hmac.new(salt.encode(), password.encode(), "sha256").hexdigest())


def hash256(b):
    """SHA-256 applied twice, the hash of Bitcoin's transactions and block headers"""
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def _varint(b, i):
    n = b[i]
    if n < 253:
        return n, i + 1
    w = {253: 2, 254: 4, 255: 8}[n]
    return int.from_bytes(b[i + 1:i + 1 + w], "little"), i + 1 + w


def split_witness(raw):
    """a segwit transaction (bytes) -> (the bytes without marker, flag and witness, the marker, flag and witness bytes)"""
    i = 6; n, i = _varint(raw, i)
    for _ in range(n):
        i += 36; s, i = _varint(raw, i); i += s + 4
    m, i = _varint(raw, i)
    for _ in range(m):
        i += 8; s, i = _varint(raw, i); i += s
    body_end = i; w0 = i
    for _ in range(n):
        k, i = _varint(raw, i)
        for _ in range(k):
            s, i = _varint(raw, i); i += s
    base = raw[:4] + raw[6:body_end] + raw[-4:]
    return base, raw[4:6] + raw[w0:-4]


def txid(raw):
    """the transaction id: the double hash of the transaction without its witness, shown in reverse byte order"""
    return hash256(split_witness(raw)[0])[::-1].hex()


def wtxid(raw):
    """the hash of the whole transaction with its witness (the 'hash' field of decoderawtransaction)"""
    return hash256(raw)[::-1].hex()


def header(b):
    """the 80 bytes of a block header from a block record: version, previous block, merkle root, time, bits, nonce"""
    return (struct.pack("<I", b["version"]) + bytes.fromhex(b["previousblockhash"])[::-1] + bytes.fromhex(b["merkle_root"])[::-1]
            + struct.pack("<III", b["timestamp"], b["bits"], b["nonce"]))


def header_fields(b):
    """the six fields of the header with their byte counts and the first hexadecimal digits of each"""
    h = header(b); cut = [(0, 4), (4, 36), (36, 68), (68, 72), (72, 76), (76, 80)]
    names = ["version", "previous block", "merkle root", "time", "bits", "nonce"]
    return [(n, e - s, h[s:e].hex()[:8]) for n, (s, e) in zip(names, cut)]


def merkle(txids):
    """the merkle root of a list of transaction ids (hex, display order) and the number of hashes on each level"""
    lvl = [bytes.fromhex(t)[::-1] for t in txids]; sizes = [len(lvl)]
    while len(lvl) > 1:
        if len(lvl) % 2:
            lvl.append(lvl[-1])
        lvl = [hash256(lvl[i] + lvl[i + 1]) for i in range(0, len(lvl), 2)]; sizes.append(len(lvl))
    return lvl[0][::-1].hex(), sizes


def age_days(queried):
    """days between each toolkit's latest release and the day the registries were queried"""
    y, m, d = (int(x) for x in queried.split("-"))
    import datetime
    q = datetime.date(y, m, d)
    return {n: (q - datetime.date.fromisoformat(v[2])).days for n, v in TOOLKITS.items()}
