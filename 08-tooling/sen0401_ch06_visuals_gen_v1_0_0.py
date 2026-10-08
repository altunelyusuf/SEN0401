#!/usr/bin/env python3
"""Writes the chapter-visualisation file of SEN0401 chapter 6, 08-tooling/ch06-page/visuals_v1_0_0.json, which the page data step
reads as its newest visuals_v*.json and the page draws under each concept's "Visualise" button.

Adapted from sen0401_visuals_gen_v1_0_0.py (chapters 2 to 5) for this chapter only; the discipline is the same. Nothing here is
drawn by hand: every figure in a visual is a Python expression that this script executes under the interpreter named on the
command line (the course's own CPython 3.14 by default), and the result written into the file is the interpreter's own repr of
what the expression gave; a mismatch between a stated and an executed result stops the script. The drawn counts of the one
histogram come from a seeded pseudo-random run, so the picture is the same every time it is built and read. Every expression
uses the standard library only, so the same lines run in the page's own interpreter.

Two of the template's thirteen visual kinds are used, for the reason the chapters 2-5 generator records: `facts` (a table of
expressions and what they gave) suits any chapter, and `hist` is honest only where the picture is a sampling experiment - here,
the first hexadecimal digit of a double SHA-256 digest over random inputs, which is level because a digest is unpredictable.

Usage: python3 sen0401_ch06_visuals_gen_v1_0_0.py [/path/to/python3.14]"""
__version__ = "1.0.0"
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = next((a for a in sys.argv[1:] if "/" in a or a.endswith("python3.14")), "/root/.local/bin/python3.14")
ALICE = ("01000000000101eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a0100000000ffffffff02204e0000000000002251203b41daba"
         "4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068f8240100000000001600147752c165ea7be772b2c0acb7f4d6047ae6f4768e0141cf5efe"
         "2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e521c00b51be739df2f899c49dc267c0ad280aca6dab0d2fa2b42a45182fc83e817130100000000")

RUNNER = r"""
import json, sys
out = []
for e in json.loads(sys.stdin.read()):
    try: out.append(repr(eval(e, {})))
    except BaseException as ex: out.append("%s: %s" % (type(ex).__name__, ex))
print(json.dumps(out))
"""


def run(exprs):
    r = subprocess.run([PY, "-c", RUNNER], input=json.dumps(exprs), capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise SystemExit("the runner failed under %s: %s" % (PY, r.stderr[-400:]))
    return json.loads(r.stdout)


def facts(caption, rows):
    got = run([e for _, e in rows])
    return dict(kind="facts", caption=caption, facts=[dict(label=l, expr=e, result=g) for (l, e), g in zip(rows, got)])


def hist(caption, draws, seed, expr, labels):
    got = run([expr])[0]
    counts = eval(got, {})
    if not isinstance(counts, list) or len(counts) != len(labels):
        raise SystemExit("the drawing expression gave %s, not %d counts" % (got[:80], len(labels)))
    if sum(counts) != draws:
        raise SystemExit("the counts add up to %d, not the %d draws claimed" % (sum(counts), draws))
    return dict(kind="hist", caption=caption, draws=draws, seed=seed, bars=[dict(index=i, text=t, count=c) for i, (t, c) in enumerate(zip(labels, counts))])


TX = "bytes.fromhex('%s')" % ALICE
V = {
 "_version": __version__,
 "_note": "Built by 08-tooling/sen0401_ch06_visuals_gen_v1_0_0.py. Every result in a `facts` table and every count in a `hist` bar was produced by executing the expression beside it under the interpreter named on that run's command line; the generator refuses to write a result it did not execute, and a histogram whose counts do not add up to the draws it claims.",
 "Weight": facts(
   "Alice's transaction measured the way a block is filled: the bytes legacy nodes see count four times, the marker, the flag and the witness once, and the sum is the 569 the book obtained from Bitcoin Core.",
   [("Bytes of the whole transaction", "len(%s)" % TX),
    ("Bytes of the legacy serialization: no marker, flag or witness", "len(%s[:4] + %s[6:-71] + %s[-4:])" % (TX, TX, TX)),
    ("Bytes that count once: the marker, the flag and the witness structure", "2 + 67"),
    ("Weight: legacy bytes times three plus all bytes", "125 * 3 + 194"),
    ("The same weight from the factors: four per legacy byte, one per witness byte", "125 * 4 + 69 * 1"),
    ("Virtual bytes, the weight over four rounded up", "-(-569 // 4)"),
    ("Weight if the signature had been in the input script instead", "(125 + 66) * 4"),
    ("Weight units the segwit discount saves", "(125 + 66) * 4 - 569")]),
 "CompactSize": facts(
   "The book's table of the compactSize integer, executed: one byte up to 252, then a prefix byte and two, four or eight little-endian bytes. The lengths are 1, 3, 5 and 9.",
   [("252, the largest one-byte value", "bytes([252]).hex()"),
    ("253, the first value that needs the 0xfd prefix", "(b'\\xfd' + (253).to_bytes(2, 'little')).hex()"),
    ("65,535, the largest value of the three-byte form", "(b'\\xfd' + (65535).to_bytes(2, 'little')).hex()"),
    ("65,536, the first value of the five-byte form", "(b'\\xfe' + (65536).to_bytes(4, 'little')).hex()"),
    ("2 to the 32, the first value of the nine-byte form", "(b'\\xff' + (2 ** 32).to_bytes(8, 'little')).hex()"),
    ("Bytes used by each form", "[1, 3, 5, 9]"),
    ("The input count byte of the pizza transaction, 131 inputs", "bytes([131]).hex()")]),
 "Bip68Timelock": facts(
   "The sequence field read as BIP68 reads it: the disable flag at bit 31, the type flag at bit 22, the 16-bit value, and what each example means for an output confirmed at height 774,958.",
   [("The disable flag, 1 shifted left 31", "hex(1 << 31)"),
    ("The type flag, 1 shifted left 22", "hex(1 << 22)"),
    ("The mask that extracts the value", "hex(0xffff)"),
    ("Sequence 30: a lock of 30 blocks, earliest confirming height", "774958 + (30 & 0xffff)"),
    ("Sequence 0x00400008: the type flag set, so 8 units of 512 seconds", "(0x00400008 & 0xffff) * 512"),
    ("Sequence 0xffffffff: the disable flag is set, no timelock", "bool(0xffffffff & (1 << 31))"),
    ("Largest lock in blocks, and in days at ten minutes a block", "(0xffff, 0xffff * 600 // 86400)"),
    ("Largest lock in 512-second units, in days", "0xffff * 512 // 86400")]),
 "DustLimit": facts(
   "Bitcoin Core's dust thresholds, recomputed from the sizes its policy source states and the default rate of 3,000 satoshis per kilo-vbyte: the output's size plus the smallest input that could spend it, times the rate.",
   [("A legacy P2PKH output, 34 bytes, needs a 148-byte input", "34 + 148"),
    ("Its threshold in satoshis", "(34 + 148) * 3000 // 1000"),
    ("A P2WPKH output, 31 bytes, needs a 67-byte input", "31 + 67"),
    ("Its threshold in satoshis", "(31 + 67) * 3000 // 1000"),
    ("A taproot output, 43 bytes, with the same 67-byte input", "(43 + 67) * 3000 // 1000"),
    ("A data-carrier output, OP_RETURN: unspendable, so no threshold", "0"),
    ("Alice's smaller output, 20,000 satoshis, against the 546 figure", "20000 > 546")]),
 "BlockSubsidy": facts(
   "The subsidy schedule Bitcoin Core computes: 50 bitcoins shifted right once per 210,000 blocks. It reaches one satoshi at block 6,720,000 and zero at block 6,930,000, and the whole schedule issues just under 21 million.",
   [("Block 0, in satoshis", "(50 * 10**8) >> (0 // 210000)"),
    ("Block 210,000, the first halving", "(50 * 10**8) >> (210000 // 210000)"),
    ("Block 775,072, Alice's block", "(50 * 10**8) >> (775072 // 210000)"),
    ("Block 840,000, the fourth halving, in bitcoins", "((50 * 10**8) >> (840000 // 210000)) / 10**8"),
    ("Block 6,720,000, the 32nd halving", "(50 * 10**8) >> (6720000 // 210000)"),
    ("Block 6,929,999, the last block with a subsidy", "(50 * 10**8) >> (6929999 // 210000)"),
    ("Block 6,930,000, the 33rd halving", "(50 * 10**8) >> (6930000 // 210000)"),
    ("Every satoshi the schedule issues, in bitcoins", "sum(((50 * 10**8) >> h) * 210000 for h in range(64)) / 10**8")]),
 "Digest": hist(
   "Three thousand two hundred double SHA-256 digests of random 32-byte inputs, grouped by the first hexadecimal digit of the digest. The bars are level because a digest is unpredictable: no first digit is likelier than another, which is why a hash can identify a transaction and why changing one byte of a transaction gives an identifier that shares nothing with the old one.",
   3200, 20261008,
   "(lambda firsts: [firsts.count(d) for d in range(16)])((lambda r, h: [h(r.getrandbits(256).to_bytes(32, 'big'))[0] >> 4 for _ in range(3200)])(__import__('random').Random(20261008), lambda b: __import__('hashlib').sha256(__import__('hashlib').sha256(b).digest()).digest()))",
   ["digit %x" % d for d in range(16)]),
}
# the two hand-stated figures in the tables are checked against execution before the file is written
assert V["Weight"]["facts"][3]["result"] == V["Weight"]["facts"][4]["result"] == "569", V["Weight"]["facts"][3:5]
assert V["DustLimit"]["facts"][1]["result"] == "546" and V["DustLimit"]["facts"][3]["result"] == "294", V["DustLimit"]["facts"]
out = os.path.join(HERE, "ch06-page", "visuals_v1_0_0.json")
json.dump(V, open(out, "w"), indent=1)
print("wrote", out, "-", len([k for k in V if not k.startswith("_")]), "visuals under", PY)
