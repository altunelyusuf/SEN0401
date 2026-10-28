"""[v3.1.0: a NEW file; the 15 examples are byte-for-byte those of examples_v3_0_0.py (which stays unchanged); the chart expressions are recorded by examples_run_v3_1_0.py.]
Every code listing of the SEN0401 chapter 1 deck 3.0.0 (Introduction; a NEW file, the earlier examples_v1_*.py stay unchanged) and the source of the chapter-code manifest
chapter_code_ch01_v1_0_0.json that the page's chapter-code tab reads. One entry per code slide, in SLIDE ORDER. A listing is a list of GROUPS; a group is a few single-line statements
and the plain-language note that explains them (the deck standard asks for an explanation beside every code box). Every statement is ONE line. The last row of a listing is an expression
(`final`, which is also in `show`): the slide prints its value under it, the only REPL text of the slide; the full result of the example is drawn as a chart or a table beside the listing
from the recorded `show` values (examples_run_v3_0_0.py), never typed. A statement is at most 56 characters, so that a code line never wraps (deck standard D12).
Every example uses only the chapter library sen0401_ch01_lib_v1_0_0 and the standard library; none reads a file or the network, so each runs in the browser as it runs here.
No example prints an error first; no example teaches an error."""
__version__ = "3.1.0"

PRELUDE = "import hashlib\nfrom decimal import Decimal\nfrom sen0401_ch01_lib_v1_0_0 import *\n"
G = lambda note, *lines: {"lines": list(lines), "note": note}

EXAMPLES = [
  {"id": "ex01", "name": "Read the headline in block zero", "branch": "Origins", "final": "sizes",
   "groups": [G("The first block keeps a short script, and the headline sits at its end.", "raw = bytes.fromhex(COINBASE_HEX)", "head, text = raw[:8], raw[8:].decode()"),
              G("Eight bytes of pushes come first; the rest is the newspaper headline.", "sizes = [len(head), len(text)]", "sizes")],
   "show": ["sizes", "head.hex()", "text", "len(raw)"]},
  {"id": "ex02", "name": "One bitcoin counted in satoshis", "branch": "Money", "final": "units",
   "groups": [G("A bitcoin is counted in whole satoshis, one hundred million to the coin.", "from decimal import Decimal", "sats = int(Decimal('0.001') * COIN)"),
              G("Three common amounts, each written as a count of satoshis.", "units = [COIN, COIN // 1000, 1]", "units")],
   "show": ["sats", "units"]},
  {"id": "ex03", "name": "The subsidy at five block heights", "branch": "Money", "final": "subs",
   "groups": [G("The subsidy starts at fifty bitcoin and halves every 210,000 blocks.", "heights = [0, 210000, 420000, 630000, 840000]", "subs = [subsidy(h) for h in heights]"),
              G("Each era pays exactly half of the era before it.", "ratios = [a / b for a, b in zip(subs, subs[1:])]", "subs")],
   "show": ["subs", "ratios"]},
  {"id": "ex04", "name": "The 21 million cap is a sum of eras", "branch": "Money", "final": "cap",
   "groups": [G("Each era issues its subsidy for 210,000 blocks, then the subsidy halves.", "eras = [(50 * COIN >> k) * HALVING for k in range(33)]"),
              G("Adding every era gives the cap, just under 21 million bitcoin.", "cap = sum(eras) / COIN", "cap")],
   "show": ["cap", "[sum(eras[:k + 1]) // COIN for k in range(8)]"]},
  {"id": "ex05", "name": "No one sets the price: trades do", "branch": "Money", "final": "avg",
   "groups": [G("Three illustrative trades: bitcoin bought, and the dollars paid for it.", "trades = [(0.5, 31000), (0.2, 12600), (1.0, 63100)]", "prices = [round(u / b, 2) for b, u in trades]"),
              G("The day's single figure weights each price by its volume.", "avg = round(vwap([(b, u / b) for b, u in trades]), 2)", "avg")],
   "show": ["trades", "prices", "avg"]},
  {"id": "ex06", "name": "The Pizza Day coins, repriced", "branch": "Money", "final": "list(val.values())",
   "groups": [G("Ten thousand bitcoin, priced at six documented moments.", "coins = 10000", "val = {d: int(coins * p) for d, p in PIZZA.items()}"),
              G("The dollar value of the same coins at each moment, from 2010 to 2026.", "list(val.values())")],
   "show": ["list(val.keys())", "list(val.values())", "round(val['2026-10'] / val['2010-05'])"]},
  {"id": "ex07", "name": "Work that is hard to find and easy to check", "branch": "Network", "final": "tries",
   "groups": [G("Search for a number that gives a hash starting with zeros.", "data = b'alice pays bob 1'", "tries = [mine(data, z)[0] + 1 for z in (1, 2, 3, 4)]"),
              G("Anyone checks the winner with one hash instead of a long search.", "n, d = mine(data, 4)", "check = hashlib.sha256(data + b'%d' % n).hexdigest()"),
              G("The last line shows how many guesses each difficulty took.", "tries")],
   "show": ["tries", "check == d", "d[:12]"]},
  {"id": "ex08", "name": "A double spend is refused", "branch": "Network", "final": "book.owner",
   "groups": [G("A shared ledger remembers which coins are spent.", "book = Ledger({'c1': 'alice'})", "first = book.pay('c1', 'bob')"),
              G("Alice offers the same coin again; the rule says no, with no referee.", "second = book.pay('c1', 'carol')", "book.owner")],
   "show": ["first", "second", "book.owner"]},
  {"id": "ex09", "name": "A chain that notices tampering", "branch": "Network", "final": "after",
   "groups": [G("Three blocks, each hashing its own text together with the block before.", "blocks = chain(['pay A', 'pay B', 'pay C'])", "before = verify(blocks)"),
              G("Change one word in block two; the check stops there.", "blocks[1]['text'] = 'pay Z'", "after = verify(blocks)", "after")],
   "show": ["before", "after", "[verify(blocks[:k]) == k for k in (1, 2, 3)]"]},
  {"id": "ex10", "name": "What the outputs leave over is the fee", "branch": "Network", "final": "fee",
   "groups": [G("One coin of 100,000 satoshis pays Bob and sends the change back.", "inputs = [100000]", "outputs = [20000, 75000]"),
              G("Whatever the outputs do not take goes to the miner as the fee.", "fee = sum(inputs) - sum(outputs)", "share = round(100 * fee / sum(inputs), 1)", "fee")],
   "show": ["fee", "share", "sum(inputs)", "outputs"]},
  {"id": "ex11", "name": "A recovery phrase stretched into a seed", "branch": "Wallets", "final": "seeds",
   "groups": [G("The test phrase of BIP 39: eleven times abandon, then about.", "words = TEST_PHRASE.split()", "rounds = (1, 10, 2048)"),
              G("Stretching repeats the hash; the wallet uses 2048 rounds.", "seeds = [stretch(TEST_PHRASE, n)[:8] for n in rounds]", "seeds")],
   "show": ["len(words)", "rounds", "seeds"]},
  {"id": "ex12", "name": "An address is a hash with a checksum", "branch": "First use", "final": "address",
   "groups": [G("Block 0 pays to a 20-byte hash of a public key, behind a version byte.", "version = bytes([0])", "payload = version + bytes.fromhex(GENESIS_HASH160)"),
              G("The checksum is the first four bytes of a double hash of the payload.", "check = dsha(payload)[:4]", "address = base58(payload + check)", "address")],
   "show": ["address", "check.hex()", "len(payload + check)", "payload[1:].hex()"]},
  {"id": "ex13", "name": "An invoice is a link with an amount", "branch": "First use", "final": "sats",
   "groups": [G("A payment request packs address, amount and label into one line of text.", "req = parse_uri(BIP21_URI)"),
              G("The fields come back by name, and the amount converts to satoshis.", "sats = int(Decimal(req['amount']) * COIN)", "sats")],
   "show": ["req", "sats"]},
  {"id": "ex14", "name": "Sending: coins in, payment and change out", "branch": "First use", "final": "change",
   "groups": [G("The wallet holds three unspent coins; it owes sixty thousand and a fee.", "coins = [50000, 30000, 80000]", "pay, fee = 60000, 1500"),
              G("It picks the smallest coin that covers both, and the rest comes back.", "pick = min(c for c in coins if c >= pay + fee)", "change = pick - pay - fee", "change")],
   "show": ["pick", "pay", "fee", "change"]},
  {"id": "ex15", "name": "A channel needs two transactions, not one per payment", "branch": "Foundations", "final": "saved",
   "groups": [G("Paid on the chain, every payment is one transaction.", "payments = [1, 10, 100, 1000]", "onchain = payments"),
              G("A channel records two transactions, one to open and one to close.", "saved = [n - 2 for n in payments]", "saved")],
   "show": ["onchain", "saved"]},
]
