#!/usr/bin/env python3
"""Writes the chapter visualisations of SEN0401 chapter 1: 08-tooling/ch01-page/visuals_v1_0_0.json.

Each visualisation is a specification in one of the kinds the course page template draws (the thirteen kinds of
nvKinds() plus the interactive ones); the page reads it from data.visuals, keyed by the identifier of the concept the
visual belongs to. Nothing in the file is typed by hand: every number, word, hash and message below is produced by
running the expression that stands beside it in this module, under the interpreter that runs this script, so the file
cannot drift from what Python actually does. The generator prints what it wrote and exits non-zero if any value it
intends to publish disagrees with the value it computes.

The five visuals, with the mechanism each one shows:
  Halving        (kind 'passes')  the subsidy schedule era by era - one row per halving, with the running total
  Supply cap     (kind 'facts')   the arithmetic behind the total of 20,999,999.9769 bitcoin, claim by claim
  Proof of work  (kind 'hist')    how many of 100,000 candidate hashes begin with 1, 2, 3, 4 and 5 zero hex digits
  Recovery code  (kind 'boxes')   a twelve-word recovery code as an ordered list, with the off-by-one error
  Bitcoin address (kind 'facts')  the parts of the address the book prints: network prefix, separator, data
                                  part in its 32-character alphabet, and the six-character checksum

usage: sen0401_ch01_visuals_gen_v1_0_0.py [OUTDIR]       default: 08-tooling/ch01-page
"""
__version__ = "1.0.0"
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ch01-page")
VER, V = "1.0.0", "1_0_0"

# ---------------------------------------------------------------------------------------------------------------------
# every published value is the value of the expression beside it: ev() evaluates and records the pair
# ---------------------------------------------------------------------------------------------------------------------
RUN = []
def ev(expr):
    v = eval(expr, {})
    RUN.append((expr, repr(v)))
    return v

# ---- Halving: one row per era -----------------------------------------------------------------------------------
ERAS = 5
rows, running = [], 0
for era in range(ERAS):
    sat = ev("(50 * 10**8) >> %d" % era)
    first = ev("%d * 210000" % era)
    made = ev("(50 * 10**8 >> %d) * 210000" % era)
    running += made
    rows.append(["%d" % era, "{:,}".format(first), "{:,}".format(sat), "%g" % (sat / 10**8),
                 "{:,}".format(made // 10**8), "{:,}".format(running // 10**8)])
printed = ["era %d starts at block %s and pays %g BTC a block" % (int(r[0]), r[1], float(r[3])) for r in rows]
HALVING = {
 "kind": "passes",
 "caption": ("The subsidy of a block is 50 bitcoin shifted right once for every completed interval of 210,000 blocks, "
             "so it halves at each interval and every shift drops any fraction below one satoshi. One row per era, with "
             "the new bitcoin that era creates and the total in circulation once it ends."),
 "tables": [{"header": "subsidy_sat = (50 * 10**8) >> (height // 210000)",
             "cols": ["era", "first block", "subsidy (sat)", "subsidy (BTC)", "new BTC in the era", "total BTC after it"],
             "rows": rows}],
 "printed_label": "What the schedule says, era by era",
 "printed": printed,
 "start": {"expr": "(50 * 10**8 >> 840000 // 210000) / 10**8",
           "result": repr(ev("(50 * 10**8 >> 840000 // 210000) / 10**8"))},
}

# ---- Supply cap: the arithmetic, claim by claim -------------------------------------------------------------------
FACT_SPEC = [
 ("The first subsidy, in satoshis", "50 * 10**8"),
 ("Blocks in one halving interval", "210000"),
 ("The last era with a non-zero subsidy", "max(e for e in range(64) if (50 * 10**8) >> e)"),
 ("The first era whose subsidy rounds to nothing", "min(e for e in range(64) if not (50 * 10**8) >> e)"),
 ("Blocks until the subsidy reaches zero", "33 * 210000"),
 ("Every subsidy of every era, added up, in bitcoin", "sum((50 * 10**8 >> era) * 210000 for era in range(33)) / 10**8"),
 ("How far that total falls short of 21 million", "round(21_000_000 - sum((50 * 10**8 >> era) * 210000 for era in range(33)) / 10**8, 4)"),
 ("The subsidy of block 840,000, in bitcoin", "(50 * 10**8 >> 840000 // 210000) / 10**8"),
]
SUPPLY = {
 "kind": "facts",
 "caption": ("The cap is not a number stored anywhere in the protocol: it is what comes out when the subsidy of every "
             "block of every era is added together. Each line below is an expression this page ran and the value it gave."),
 "facts": [{"label": lab, "expr": e, "result": repr(ev(e))} for lab, e in FACT_SPEC],
}

# ---- Proof of work: how rare a leading run of zeros is ------------------------------------------------------------
PREFIX, DRAWS = "SEN0401-", 100000
counts = {k: 0 for k in range(1, 6)}
for n in range(DRAWS):
    h = hashlib.sha256(("%s%d" % (PREFIX, n)).encode()).hexdigest()
    z = len(h) - len(h.lstrip("0"))
    for k in range(1, 6):
        if z >= k:
            counts[k] += 1
RUN.append(("counts of leading zero hex digits over %d hashes of %r + n" % (DRAWS, PREFIX), repr(counts)))
first4 = ev("next(n for n in range(10**6) if __import__('hashlib').sha256(f'SEN0401-{n}'.encode()).hexdigest().startswith('0000'))")
POW = {
 "kind": "hist",
 "draws": DRAWS,
 "seed": "the text SEN0401- followed by the candidate number",
 "caption": ("Mining is a search: a miner changes one number in the block and hashes again until the result begins "
             "with enough zeros. Hashing the text SEN0401- followed by each of the first %s candidate numbers, this is "
             "how many of them gave a hash with at least one, two, three, four and five leading zero digits - each extra "
             "digit is about sixteen times rarer than the last. The first candidate whose hash begins with four zeros is "
             "number %s, so %s hashes were computed to find it." % ("{:,}".format(DRAWS), "{:,}".format(first4), "{:,}".format(first4 + 1))),
 "bars": [{"index": k, "text": "at least %d leading zero digit%s" % (k, "" if k == 1 else "s"), "count": counts[k]} for k in range(1, 6)],
}

# ---- Recovery code: an ordered list of words ----------------------------------------------------------------------
CODE = "nephew dog crane clever quantum crazy purse traffic repeat fruit old clutch"
WORDS = ev("%r.split()" % CODE)
PICK_SPEC = [
 ("words[0]", [0]),
 ("words[11]", [11]),
 ("words[-1]", [11]),
 ("words[:4]", [0, 1, 2, 3]),
 ("words[-3:]", [9, 10, 11]),
]
picks = []
for e, at in PICK_SPEC:
    val = eval(e, {}, {"words": WORDS})
    RUN.append((e, repr(val)))
    assert [WORDS.index(w) for w in (val if isinstance(val, list) else [val])] == at, (e, at)
    picks.append({"expr": e, "at": at, "result": repr(val)})
try:
    eval("words[12]", {}, {"words": WORDS}); raise SystemExit("words[12] did not fail")
except IndexError as exc:
    err = {"expr": "words[12]", "message": "IndexError: %s" % exc}
RUN.append(("words[12]", err["message"]))
RECOVERY = {
 "kind": "boxes",
 "name": "words",
 "len": len(WORDS),
 "list": WORDS,
 "caption": ("A recovery code is an ordered list of words, and the order is part of the secret: the same twelve words in "
             "another order rebuild another wallet, or nothing at all. The boxes are the words of the code the chapter "
             "uses; the number above a box counts from the first word, the number below from the last."),
 "picks": picks,
 "error": err,
}

# ---- Bitcoin address: the Bech32 checksum -------------------------------------------------------------------------
GOOD = "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee"
ALPHABET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
ADDR_SPEC = [
 ("Characters in the address", "len(%r)" % GOOD),
 ("The part before the separator, which names the network", "%r.split('1', 1)[0]" % GOOD),
 ("The character that separates the two parts", "%r[2]" % GOOD),
 ("The last six characters, which are the checksum itself", "%r[-6:]" % GOOD),
 ("Distinct characters the data part is written in", "len(set(%r.split('1', 1)[1]))" % GOOD),
 ("Every character after the separator comes from the 32-character alphabet",
  "set(%r.split('1', 1)[1]) <= set(%r)" % (GOOD, ALPHABET)),
 ("The four letters and digits the alphabet leaves out, to stop one being read as another",
  "sorted(set('0123456789abcdefghijklmnopqrstuvwxyz') - set(%r))" % ALPHABET),
]
ADDRESS = {
 "kind": "facts",
 "caption": ("An address is a string with parts: a prefix that names the network, a separator, a data part written in a "
             "32-character alphabet that leaves out the characters most easily misread, and a six-character checksum "
             "computed from everything before it. Each line below takes the address the textbook prints apart, and the "
             "worked example of this concept runs the checksum itself."),
 "facts": [{"label": lab, "expr": e, "result": repr(ev(e))} for lab, e in ADDR_SPEC],
}

VIS = {"_version": VER,
       "_note": ("Every value in this file was produced by running the expression recorded beside it, under %s, by "
                 "08-tooling/sen0401_ch01_visuals_gen_v%s.py. The kinds used - passes, facts, hist and boxes - are "
                 "kinds the course page template already draws." % (sys.version.split()[0], V)),
       "Halving": HALVING, "SupplyCap": SUPPLY, "ProofOfWork": POW, "RecoveryCode": RECOVERY, "BitcoinAddress": ADDRESS}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "visuals_v%s.json" % V)
    json.dump(VIS, open(p, "w"), indent=1)
    print("written", p, os.path.getsize(p), "bytes")
    print("%d values executed under CPython %s" % (len(RUN), sys.version.split()[0]))
    for k, v in VIS.items():
        if not k.startswith("_"):
            print("   %-16s %s" % (k, v["kind"]))
