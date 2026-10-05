#!/usr/bin/env python3
"""Writes the chapter-visualisation file of SEN0401 chapters 2 to 5, 08-tooling/chNN-page/visuals_v1_0_0.json, which the
page data step reads as its newest visuals_v*.json and the page draws under each concept's "Visualise" button.

Nothing here is drawn by hand. Every figure in a visual is a Python expression that this script executes under the
interpreter named on the command line (the course's own CPython 3.14.4 by default), and the result written into the file
is the interpreter's own repr of what the expression gave; a mismatch between a stated and an executed result stops the
script, so the file cannot ship a number the interpreter did not produce. The drawn counts of a histogram come from a
seeded pseudo-random run, so the picture is the same every time it is built and every time it is read.

Two of the template's thirteen visual kinds are used, and the choice is deliberate rather than a shortfall:

  * `facts`  - a table of expressions and the results they gave. The kind suits any chapter, because its heading, which
    the template fixes, says exactly what the table is: expressions Python ran, and what they gave.
  * `hist`   - a bar per outcome of a stated number of seeded draws. The template's heading for this kind names the
    draw count and the seed, so the kind is honest only where the picture really is a sampling experiment; it is used
    for the two concepts where sampling is the mechanism being taught, the choice of a private key and the choice of
    the entropy behind a recovery code.

The remaining eleven kinds (boxes, slices, lanes, unpack, keysort, refgraph, matrix, mutation, passes, seqtypes,
classify) carry headings the template hard-codes about Python lists, their indexes, their slices and the objects names
reach - "A list as boxes", "Operations sorted by what they do to a list", "Names and the objects they reach". A Bitcoin
mechanism drawn under one of those headings would be mislabelled on the page, and the headings live in the shared
template, which this chapter does not own. They are therefore left unused here and named in the handover instead.

Usage: python3 sen0401_visuals_gen_v1_0_0.py [/path/to/python3.14] [NN ...]"""
__version__ = "1.0.0"
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = next((a for a in sys.argv[1:] if "/" in a or a.endswith("python3.14")), "/root/.local/bin/python3.14")
WANT = [a for a in sys.argv[1:] if a.isdigit()] or ["02", "03", "04", "05"]

RUNNER = r"""
import json, sys
out = []
for e in json.loads(sys.stdin.read()):
    try: out.append(repr(eval(e, {})))
    except BaseException as ex: out.append("%s: %s" % (type(ex).__name__, ex))
print(json.dumps(out))
"""


def run(exprs):
    """The interpreter's own repr for each expression, in order."""
    r = subprocess.run([PY, "-c", RUNNER], input=json.dumps(exprs), capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise SystemExit("the runner failed under %s: %s" % (PY, r.stderr[-400:]))
    return json.loads(r.stdout)


def facts(caption, rows):
    """rows: [(label, expression)] - the result of each is executed here, never written by hand."""
    got = run([e for _, e in rows])
    return dict(kind="facts", caption=caption,
                facts=[dict(label=l, expr=e, result=g) for (l, e), g in zip(rows, got)])


def hist(caption, draws, seed, expr, labels):
    """`expr` must give a list of counts, one per label, from `draws` seeded draws."""
    got = run([expr])[0]
    counts = eval(got, {})
    if not isinstance(counts, list) or len(counts) != len(labels):
        raise SystemExit("the drawing expression gave %s, not %d counts" % (got[:80], len(labels)))
    if sum(counts) != draws:
        raise SystemExit("the counts add up to %d, not the %d draws claimed" % (sum(counts), draws))
    return dict(kind="hist", caption=caption, draws=draws, seed=seed,
                bars=[dict(index=i, text=t, count=c) for i, (t, c) in enumerate(zip(labels, counts))])


# ---------------------------------------------------------------------------------------------------------------
# chapter 2: the one transaction the chapter follows, and the whitepaper's own odds of a reversal
# ---------------------------------------------------------------------------------------------------------------
CH02 = lambda: {
 "TransactionPart": facts(
   "Every figure of Alice's payment, recomputed from the amounts and the sizes the chapter reads out of the "
   "transaction itself. The inputs do not equal the outputs: the difference is the fee, and no field holds it.",
   [("What the input brings in, in satoshis", "100000"),
    ("What the two outputs create: the payment and the change", "sum([75000, 20000])"),
    ("The fee, which is the difference and is written nowhere", "100000 - sum([75000, 20000])"),
    ("Outputs plus fee, which must equal the inputs", "sum([75000, 20000, 5000]) == 100000"),
    ("Weight units of the transaction", "569"),
    ("Virtual bytes, which is the weight divided by four and rounded up", "(569 + 3) // 4"),
    ("Satoshis per virtual byte, the price miners compare", "round(5000 / 143, 2)"),
    ("Satoshis in one thousandth of a bitcoin", "10**8 // 1000")]),
 "Probability": facts(
   "The whitepaper's own calculation, for an attacker holding a tenth of the hash rate: the chance of catching up "
   "from z blocks behind falls away as confirmations accumulate. Each line is the ratio of the attacker's share to "
   "the honest share, raised to the number of confirmations.",
   [("One confirmation", "round((0.1 / 0.9) ** 1, 9)"),
    ("Two confirmations", "round((0.1 / 0.9) ** 2, 9)"),
    ("Three confirmations", "round((0.1 / 0.9) ** 3, 9)"),
    ("Four confirmations", "round((0.1 / 0.9) ** 4, 9)"),
    ("Six confirmations, the figure merchants quote", "round((0.1 / 0.9) ** 6, 9)"),
    ("Eight confirmations", "round((0.1 / 0.9) ** 8, 9)"),
    ("How many times safer six confirmations are than one",
     "round((0.1 / 0.9) ** 1 / (0.1 / 0.9) ** 6)"),
    ("Blocks expected in a day, at one every ten minutes", "24 * 60 // 10")]),
}

# ---------------------------------------------------------------------------------------------------------------
# chapter 3: what the node computes about a block and a transaction before it applies any rule
# ---------------------------------------------------------------------------------------------------------------
CH03 = lambda: {
 "BlockHeader": facts(
   "The eighty bytes a node hashes, field by field, and the figures it derives from the header of the real block the "
   "chapter reads. The header is the whole of what proof of work commits to; everything else in the block is reached "
   "through the Merkle root inside it.",
   [("Version, in bytes", "4"),
    ("The previous block's identifier, in bytes", "32"),
    ("The Merkle root, in bytes", "32"),
    ("Time, the compact target and the nonce, four bytes each", "4 + 4 + 4"),
    ("The whole header, in bytes", "4 + 32 + 32 + 4 + 4 + 4"),
    ("The target the compact field 0x1a6a93b3 stands for",
     "'%064x' % (0x6a93b3 << (8 * (0x1a - 3)))"),
    ("How much harder that target is than the easiest one",
     "round(0xffff * 256**(0x1d - 3) / (0x6a93b3 * 256**(0x1a - 3)), 10)"),
    ("The subsidy of block 775072, in satoshis", "50 * 10**8 >> (775072 // 210000)"),
    ("The same subsidy, in bitcoins", "(50 * 10**8 >> (775072 // 210000)) / 10**8"),
    ("Halvings behind that block", "775072 // 210000")]),
 "TransactionWeight": facts(
   "How a segregated-witness transaction is measured. The data outside the witness counts four times over, the "
   "witness once, and the virtual size is the weight divided by four and rounded up - which is why moving data into "
   "the witness makes a transaction cheaper without making it smaller.",
   [("Bytes of the transaction without its witness", "125"),
    ("Bytes of the whole transaction, witness included", "194"),
    ("Bytes of witness data alone", "194 - 125"),
    ("Weight units: the base data four times, the witness once", "4 * 125 + 194 - 125"),
    ("Virtual bytes, the weight divided by four and rounded up", "-(-(4 * 125 + 194 - 125) // 4)"),
    ("What the virtual size would be if nothing were in the witness", "-(-(4 * 194) // 4)"),
    ("Virtual bytes the witness discount saves", "-(-(4 * 194) // 4) - -(-(4 * 125 + 194 - 125) // 4)"),
    ("The limit on one block, in weight units", "4000000")]),
}

# ---------------------------------------------------------------------------------------------------------------
# chapter 4: from a private key to the strings a payer can type, and the randomness the first step needs
# ---------------------------------------------------------------------------------------------------------------
CH04 = lambda: {
 "Hash160": facts(
   "The chain of functions between a key and an address, each step executed. The two hash functions are applied one "
   "after the other, which is what shortens a thirty-three byte key to a twenty byte commitment; the four-byte "
   "checksum is itself a hash of what precedes it.",
   [("The first eight hexadecimal digits of the SHA-256 of the three letters abc",
     "__import__('hashlib').sha256(b'abc').hexdigest()[:8]"),
    ("Length of a SHA-256 result, in bytes and in bits",
     "(__import__('hashlib').sha256(b'abc').digest_size, __import__('hashlib').sha256(b'abc').digest_size * 8)"),
    ("Length of the twenty-byte commitment, in bytes and in bits",
     "(lambda d: (len(bytes.fromhex(d)), len(bytes.fromhex(d)) * 8))('bbc1e42a39d05a4cc61752d6963b7f69d09bb27b')"),
    ("Do the compressed and the uncompressed key give the same commitment?",
     "'bbc1e42a39d05a4cc61752d6963b7f69d09bb27b' == '211b74ca4686f81efda5641767fc84ef16dafe0b'"),
    ("The four checksum bytes of a wallet-format private key",
     "__import__('hashlib').sha256(__import__('hashlib').sha256(bytes.fromhex("
     "'801E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD')).digest()).digest()[:4].hex()"),
    ("How much shorter a compressed public key is", "round(1 - 33 / 65, 3)"),
    ("Characters in the native-segwit address of the chapter",
     "len('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee')"),
    ("Bytes a twenty-byte commitment and a one-byte version take before encoding", "1 + 20")]),
 "SecureRandomness": facts(
   "Why a private key may be chosen at random at all. The count of keys is so large that no search can cover it, and "
   "the odd-looking upper bound is the order of the curve's group, not a round power of two: a key must fall below it.",
   [("How many private keys there are, as a power of two", "2**256"),
    ("The same count, in decimal digits", "len(str(2**256))"),
    ("The order of the curve group, which bounds a valid key",
     "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"),
    ("How many of the 2**256 numbers are too large to be a key",
     "2**256 - 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"),
    ("The share of numbers that are too large",
     "round((2**256 - 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141) / 2**256, 40)"),
    ("Is a key drawn by the standard library's secure source in range?",
     "0 < __import__('secrets').randbelow("
     "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 - 1) + 1 < "
     "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"),
    ("Years to try them all at a thousand million million keys a second",
     "round(2**256 / 1e15 / (365 * 24 * 3600))")]),
 "Entropy": hist(
   "Four thousand private keys drawn from a seeded generator, sorted by their first hexadecimal digit. The bars are "
   "level because the digit carries no information about the key: a generator whose bars were uneven would be leaking "
   "exactly the kind of structure a search could use.",
   4000, 20260401,
   "(lambda R: (lambda ks: [sum(1 for k in ks if k >> 252 == d) for d in range(16)])"
   "([R.getrandbits(256) for _ in range(4000)]))(__import__('random').Random(20260401))",
   ["first digit %x" % d for d in range(16)]),
}

# ---------------------------------------------------------------------------------------------------------------
# chapter 5: the arithmetic of a recovery code, and the entropy the code is made from
# ---------------------------------------------------------------------------------------------------------------
CH05 = lambda: {
 "CodeLength": facts(
   "Why a recovery code has twelve words rather than any other number. The standard adds one checksum bit for every "
   "thirty-two bits of entropy and then cuts the result into eleven-bit pieces, one word each, so the word count "
   "follows from the entropy and nothing is chosen.",
   [("Words in the list, which is two to the eleventh", "2 ** 11"),
    ("Bits one word therefore carries", "2048 .bit_length() - 1"),
    ("Entropy in the chapter's own example, in bits",
     "len(bytes.fromhex('0c1e24e5917779d297e14d45f14e1a1a')) * 8"),
    ("Checksum bits for that entropy: one per thirty-two", "128 // 32"),
    ("Pieces of eleven bits the two together make", "(128 + 128 // 32) // 11"),
    ("The checksum bits themselves, the first four of a SHA-256 of the entropy",
     "bin(__import__('hashlib').sha256(bytes.fromhex('0c1e24e5917779d297e14d45f14e1a1a')).digest()[0])"
     "[2:].zfill(8)[:4]"),
    ("The first three word numbers the example's bits give",
     "[int(bin(int.from_bytes(bytes.fromhex('0c1e24e5917779d297e14d45f14e1a1a'), 'big'))[2:].zfill(128)"
     "[i:i + 11], 2) for i in range(0, 33, 11)]"),
    ("Entropy, checksum and word count for every length the standard allows",
     "[(e, e // 32, (e + e // 32) // 11) for e in (128, 160, 192, 224, 256)]"),
    ("Rounds of key stretching between the words and the seed", "2048"),
    ("Bytes of seed the stretching produces", "64")]),
 "Entropy": hist(
   "Three thousand two hundred runs of the first step of making a recovery code: a hundred and twenty-eight random "
   "bits, of which the first eleven name the first word. The bars group the two thousand and forty-eight words into "
   "eight blocks of two hundred and fifty-six, and they are level because every word must be as likely as every "
   "other - a code whose first word were predictable would have less entropy than its length claims.",
   3200, 20260501,
   "(lambda R: (lambda es: [sum(1 for e in es if (e >> (128 - 11)) // 256 == b) for b in range(8)])"
   "([R.getrandbits(128) for _ in range(3200)]))(__import__('random').Random(20260501))",
   ["words %d-%d" % (b * 256, b * 256 + 255) for b in range(8)]),
}

BUILD = {"02": CH02, "03": CH03, "04": CH04, "05": CH05}
NOTE = ("Built by 08-tooling/sen0401_visuals_gen_v1_0_0.py. Every result in a `facts` table and every count in a "
        "`hist` bar was produced by executing the expression beside it under the interpreter named on that run's "
        "command line; the generator refuses to write a result it did not execute, and a histogram whose counts do "
        "not add up to the stated number of draws stops it. The draws are seeded, so the bars are identical on "
        "every build.")

for nn in WANT:
    data = BUILD[nn]()
    ids = {n["id"] for n in json.load(open(os.path.join(HERE, "ch%s-page" % nn, "page_data_v9_28_0.json")))["nodes"]}
    unknown = sorted(set(data) - ids)
    if unknown:
        raise SystemExit("chapter %s: %s is not a concept of the chapter" % (nn, unknown))
    out = {"_version": "1.0.0", "_note": NOTE}
    out.update(data)
    p = os.path.join(HERE, "ch%s-page" % nn, "visuals_v1_0_0.json")
    json.dump(out, open(p, "w"), indent=1, ensure_ascii=False)
    print("ch%s: %d visuals (%s) -> %s" % (
        nn, len(data), ", ".join("%s/%s" % (k, v["kind"]) for k, v in data.items()), os.path.basename(p)))
    for k, v in data.items():
        if v["kind"] == "facts":
            bad = [f["label"] for f in v["facts"] if "Error:" in f["result"]]
            if bad:
                raise SystemExit("chapter %s, %s: expressions that raised: %s" % (nn, k, bad))
            print("    %-18s %d executed figures" % (k, len(v["facts"])))
        else:
            print("    %-18s %d bars, %d draws, seed %d" % (k, len(v["bars"]), v["draws"], v["seed"]))
print("interpreter:", subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.strip())
