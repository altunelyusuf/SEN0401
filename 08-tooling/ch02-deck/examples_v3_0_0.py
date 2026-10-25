"""Chapter 2 examples, version 3.0.0 - the fourteen code examples of the chapter 2 deck 3.0.0 (new file; examples_v1_x are the earlier decks' and stay as they are).
Each example is a listing of single-line statements, the last one an expression whose repr the deck prints under the listing; `show` lists the expressions whose values the
result picture of the slide is drawn from (the first is the printed one). The listings run after the PRELUDE, one fresh namespace each, and call the chapter library
sen0401_ch02_tx_lib_v1_0_0 as T. Nothing here records an answer: examples_run_v3_0_0.py runs every listing and writes examples_out_v3_0_0.json; the deck is drawn from that file."""
__version__ = "3.0.0"
PRELUDE = "import hashlib\nimport urllib.parse\nimport sen0401_ch02_tx_lib_v1_0_0 as T\n"
LIB = "sen0401_ch02_tx_lib_v1_0_0"

P1, P2, P3, P4, P5, P6 = ("Buying from an Online Store", "Bitcoin Transactions", "Coin Selection", "Constructing a Transaction",
                          "Adding the Transaction to the Blockchain", "Spending the Transaction")

G = lambda lines, note: {"lines": lines, "note": note}
EXAMPLES = [
 {"id": "ex01", "name": "Satoshis are whole numbers", "branch": P1, "picture": "table",
  "groups": [G(["btc = '0.01577764'"], "The invoice amount, written the way people write it."),
             G(["sats = T.to_sats(btc)", "back = T.to_btc(sats)", "(sats, back)"], "Whole numbers in, whole satoshis out, and the same text comes back.")],
  "show": ["(sats, back)", "T.to_sats('0.00075')", "T.to_sats('1')"]},
 {"id": "ex02", "name": "Reading Bob's invoice", "branch": P1, "picture": "table",
  "groups": [G(["u = urllib.parse.urlsplit(T.INVOICE)", "q = urllib.parse.parse_qs(u.query)"], "Split the link into the part before the question mark and the query."),
             G(["[u.scheme, q['amount'][0], q['label'][0]]"], "The scheme tells a wallet to open; the query holds the amount and the label.")],
  "show": ["[u.scheme, q['amount'][0], q['label'][0]]", "u.path[:12]", "T.to_sats(q['amount'][0])"]},
 {"id": "ex03", "name": "Inputs equal outputs plus the fee", "branch": P2, "picture": "native chart",
  "groups": [G(["ins, outs = T.ALICE_IN, T.ALICE_OUT"], "Alice's one input and her two outputs, in satoshis."),
             G(["fee = sum(ins) - sum(outs)", "(sum(ins), sum(outs), fee)"], "Inputs minus outputs is the fee; nobody writes it down anywhere.")],
  "show": ["(sum(ins), sum(outs), fee)", "outs"]},
 {"id": "ex04", "name": "The txid is shown backwards", "branch": P2, "picture": "table",
  "groups": [G(["raw = bytes.fromhex(T.PREV_RAW)"], "The 32 bytes of the earlier transaction's identifier, as an input stores them."),
             G(["shown = raw[::-1].hex()", "(raw.hex()[:8], shown[:8])"], "Reverse the bytes to get the order in which block explorers display it.")],
  "show": ["(raw.hex()[:8], shown[:8])", "(raw.hex()[-8:], shown[-8:])", "len(raw)"]},
 {"id": "ex05", "name": "Size in virtual bytes and the fee rate", "branch": P2, "picture": "table",
  "groups": [G(["weight = 569"], "Alice's transaction weighs 569 weight units, as Bitcoin Core reports."),
             G(["vbytes = -(-weight // 4)", "rate = round(5000 / vbytes, 2)", "(vbytes, rate)"], "Four units make a virtual byte, rounded up; fee divided by size is the rate.")],
  "show": ["(vbytes, rate)", "weight / 4"]},
 {"id": "ex06", "name": "Which outputs are still unspent", "branch": P2, "picture": "table",
  "groups": [G(["C = T.CHAIN", "used = {i for a, b in C.values() for i in a}"], "The chain of figure 2-3, and the set of outputs that some input spends."),
             G(["val = {o: v for _, b in C.values() for o, v in b.items()}"], "Every output of the chain with its value in satoshis."),
             G(["free = [o for o in val if o not in used]", "free"], "Outputs that nobody has spent are the coins that still exist.")],
  "show": ["free", "val", "sorted(used)", "[sum(val[i] for i in C[t][0]) - sum(C[t][1].values()) for t in ('Tx2', 'Tx3')]"]},
 {"id": "ex07", "name": "Coin selection: pick, pay, change back", "branch": P3, "picture": "native chart",
  "groups": [G(["vals, need = [60000, 30000, 25000], 80000"], "Three coins in the wallet, and a payment of 80,000 satoshis to make."),
             G(["pick, change = T.select(vals, need)", "(pick, change)"], "Take whole coins in order until they cover the payment; the surplus is change.")],
  "show": ["(pick, change)", "sum(pick)"]},
 {"id": "ex08", "name": "Three common shapes of a transaction", "branch": P3, "picture": "table",
  "groups": [G(["F = T.FORMS", "shape = {k: (len(a), len(b)) for k, (a, b) in F.items()}"], "Three forms, each a list of input values and a list of output values."),
             G(["fee = {k: sum(a) - sum(b) for k, (a, b) in F.items()}", "fee"], "The fee of each shape is again inputs minus outputs.")],
  "show": ["fee", "shape"]},
 {"id": "ex09", "name": "A higher fee rate leaves less change", "branch": P4, "picture": "native chart",
  "groups": [G(["vb = 143", "rates = [10, 20, 35, 100]"], "The size of Alice's transaction, and four fee rates in satoshis per virtual byte."),
             G(["change = [100000 - 75000 - r * vb for r in rates]", "change"], "Coin minus payment minus fee: what is left comes back as change.")],
  "show": ["change", "[r * vb for r in rates]"]},
 {"id": "ex10", "name": "One more zero, many more tries", "branch": P5, "picture": "native chart",
  "groups": [G(["data = 'Hello, world! '", "ok = lambda n, z: T.sha(data + str(n)).startswith('0' * z)"], "A text, and a test: does the hash of text plus counter start with z zeros?"),
             G(["find = lambda z: next(n for n in range(10**7) if ok(n, z))", "[find(z) for z in (1, 2, 3, 4)]"], "Count up from zero until the test passes, for one to four zeros.")],
  "show": ["[find(z) for z in (1, 2, 3, 4)]", "T.sha(data + str(find(4)))[:12]"]},
 {"id": "ex11", "name": "The first block header is 80 bytes", "branch": P5, "picture": "table",
  "groups": [G(["hdr = T.genesis_header()"], "Pack the six fields of Bitcoin's first block header into 80 bytes."),
             G(["h = T.block_hash(hdr)", "(len(hdr), h[:20])"], "Hash twice and reverse the bytes: the name of the first block starts with ten zeros.")],
  "show": ["(len(hdr), h[:20])", "h", "[len(hdr[a:b]) for a, b in ((0, 4), (4, 36), (36, 68), (68, 72), (72, 76), (76, 80))]"]},
 {"id": "ex12", "name": "Nakamoto's catch-up table, recomputed", "branch": P5, "picture": "native chart",
  "groups": [G(["q10 = [round(T.catch_up(0.1, z), 7) for z in range(7)]"], "The white paper's formula for an attacker with 10 percent of the hash power."),
             G(["q30 = [round(T.catch_up(0.3, z), 7) for z in range(7)]", "(q10[1], q10[6])"], "The same for 30 percent; the printed pair is the chance at one and at six blocks.")],
  "show": ["(q10[1], q10[6])", "q10", "q30"]},
 {"id": "ex13", "name": "The reward halves every 210,000 blocks", "branch": P6, "picture": "native chart",
  "groups": [G(["era = T.HALVING_INTERVAL", "reward = lambda h: 50 * T.COIN >> h // era"], "Fifty bitcoin, shifted right by one bit for every completed era of 210,000 blocks."),
             G(["[reward(h * era) / T.COIN for h in range(6)]"], "The reward at the first block of each of the first six eras, in bitcoin.")],
  "show": ["[reward(h * era) / T.COIN for h in range(6)]", "era"]},
 {"id": "ex14", "name": "Two outputs that wrapped around", "branch": P6, "picture": "table",
  "groups": [G(["big = 9223372036854277039", "total = big + big"], "Each of the two outputs of block 74,638 held this many satoshis."),
             G(["stored = T.wrap64(total)", "(stored, stored < 0)"], "A signed 64-bit number wraps around, so the sum turns negative.")],
  "show": ["(stored, stored < 0)", "total", "big"]},
]
for _e in EXAMPLES:
    _e["lines"] = [l for g in _e["groups"] for l in g["lines"]]
