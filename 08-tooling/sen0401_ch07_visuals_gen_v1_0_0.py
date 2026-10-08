#!/usr/bin/env python3
"""Writes the chapter-visualisation file of SEN0401 chapter 7, 08-tooling/ch07-page/visuals_v1_0_0.json, which the page data step reads as
its newest visuals_v*.json and the page draws under each concept's "Visualise" button.

Adapted from sen0401_ch06_visuals_gen_v1_0_0.py for this chapter only; the discipline is the same. Nothing here is drawn by hand: every
figure in a visual is a Python expression that this script executes under the interpreter named on the command line (the course's own
CPython 3.14 by default), and the result written into the file is the interpreter's own repr of what the expression gave. Every expression
uses the standard library only, so the same lines run in the page's own interpreter. Only the template's `facts` kind (a table of
expressions and what they gave) is used: this chapter has no sampling experiment for which a histogram would be honest.

Usage: python3 sen0401_ch07_visuals_gen_v1_0_0.py [/path/to/python3.14]"""
__version__ = "1.0.0"
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = next((a for a in sys.argv[1:] if "/" in a or a.endswith("python3.14")), "/root/.local/bin/python3.14")

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


V = {
 "_version": __version__,
 "_note": "Built by 08-tooling/sen0401_ch07_visuals_gen_v1_0_0.py. Every result in a `facts` table was produced by executing the expression beside it under the interpreter named on that run's command line; the generator refuses to write a result it did not execute.",
 "MastVersusAst": facts(
   "How many 32-byte commitments a spend needs: one for each level between the script and the root, plus the root. Doubling the number of scripts costs one commitment more.",
   [("Commitments for 3 scripts, and the bytes they take", "(lambda n: (n, 32 * n))((3 - 1).bit_length() + 1)"),
    ("Commitments for 4 scripts: the same as for 3", "(4 - 1).bit_length() + 1"),
    ("Commitments for 8 scripts: one more", "(8 - 1).bit_length() + 1"),
    ("Commitments for 1,024 scripts", "(1024 - 1).bit_length() + 1"),
    ("Commitments for 32,768 scripts, and the bytes they take", "(lambda n: (n, 32 * n))((32768 - 1).bit_length() + 1)"),
    ("Commitments for 2 to the 127 scripts, the book's 'more than all computers could create'", "(2 ** 127 - 1).bit_length() + 1"),
    ("The same scripts in one legacy script of at most 10,000 bytes, at 34 bytes a branch", "10000 // 34")]),
 "ControlBlock": facts(
   "The control block of a taproot script path spend: one byte for the leaf version and the parity, 32 bytes for the internal key, and 32 bytes for each level of the tree.",
   [("Depth 0: a tree of one leaf, like the inscription in block 775,072", "33 + 32 * 0"),
    ("Depth 1: two leaves", "33 + 32 * 1"),
    ("Depth 2: three or four leaves", "33 + 32 * 2"),
    ("Depth 7: up to 128 leaves", "33 + 32 * 7"),
    ("Depth 128, the largest the rules allow", "33 + 32 * 128"),
    ("The first byte 0xc1: its leaf version and its parity bit", "(0xc1 & 0xfe, 0xc1 & 1)"),
    ("A length that is not 33 plus a multiple of 32 is refused", "[(n - 33) % 32 == 0 for n in (33, 65, 97, 98)]")]),
 "MultisigLimits": facts(
   "The size of an m-of-n multisignature script with compressed keys is 34 bytes for each key plus 3: the count of signatures, the count of keys and the opcode.",
   [("2-of-3: the script in the book", "34 * 3 + 3"),
    ("2-of-5: Mohammed's company", "34 * 5 + 3"),
    ("15 keys, the most that fits a script hash", "34 * 15 + 3"),
    ("16 keys, one too many: over the 520-byte limit of a redeem script", "34 * 16 + 3"),
    ("Is the 15-key script within 520 bytes, and the 16-key one?", "(34 * 15 + 3 <= 520, 34 * 16 + 3 <= 520)"),
    ("20 keys, the consensus limit for a witness script", "34 * 20 + 3"),
    ("The same 2-of-3 written for tapscript with OP_CHECKSIGADD", "34 * 3 + 2")]),
 "SignatureHash": facts(
   "The six hash types of a signature and their byte values: the low bits choose the outputs the signature covers and the high bit decides whether the other inputs are covered.",
   [("SIGHASH_ALL", "hex(0x01)"),
    ("SIGHASH_NONE", "hex(0x02)"),
    ("SIGHASH_SINGLE", "hex(0x03)"),
    ("ALL with ANYONECANPAY", "hex(0x01 | 0x80)"),
    ("NONE with ANYONECANPAY", "hex(0x02 | 0x80)"),
    ("SINGLE with ANYONECANPAY", "hex(0x03 | 0x80)"),
    ("Taproot's default type, a signature of 64 bytes without the type byte", "(64, 64 + 1)")]),
 "OpSuccess": facts(
   "The opcode values that make a tapscript succeed at once, from BIP342's list: 87 of the 256 possible byte values.",
   [("Single values: 80 and 98", "[80, 98]"),
    ("The range 126 to 129", "list(range(126, 130))"),
    ("The range 131 to 134", "list(range(131, 135))"),
    ("The values 137, 138, 141 and 142", "[137, 138, 141, 142]"),
    ("The range 149 to 153: contains OP_LSHIFT, number 152, disabled in 2010", "list(range(149, 154))"),
    ("The range 187 to 254", "(187, 254, 254 - 187 + 1)"),
    ("How many values in all", "2 + 4 + 4 + 4 + 5 + (254 - 187 + 1)")]),
 "TapscriptChanges": facts(
   "The same policy written for the old and for the new language: m of n keys. The tapscript form is one byte shorter for every n: each key takes 34 bytes in both forms, and the legacy script needs one more byte for the count of keys.",
   [("Legacy 2-of-3, bytes", "34 * 3 + 3"),
    ("Tapscript 2-of-3, bytes", "33 * 3 + 3 + 1 + 1"),
    ("Legacy 3-of-5, bytes", "34 * 5 + 3"),
    ("Tapscript 3-of-5, bytes", "33 * 5 + 5 + 1 + 1"),
    ("Legacy 11-of-15, bytes: the count 11 is still one byte", "34 * 15 + 3"),
    ("Tapscript 11-of-15, bytes", "33 * 15 + 15 + 1 + 1"),
    ("Signature checks needed with OP_CHECKSIGADD for a 2-of-3 spend: the empty value costs nothing", "2")]),
}
out = os.path.join(HERE, "ch07-page", "visuals_v1_0_0.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
J = json.dumps
checks = {"MastVersusAst": ("(3, 96)", 0), "ControlBlock": ("97", 2), "MultisigLimits": ("513", 2), "TapscriptChanges": ("104", 1), "OpSuccess": ("87", 6)}
for k, (want, i) in checks.items():
    got = V[k]["facts"][i]["result"]
    assert got == want, (k, i, got, want)
json.dump(V, open(out, "w"), indent=1)
print("wrote", out, "-", len([k for k in V if not k.startswith("_")]), "visuals under", PY)
