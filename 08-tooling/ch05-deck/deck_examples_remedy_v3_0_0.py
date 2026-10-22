#!/usr/bin/env python3
"""Chapter 5 deck v3.0.0 - the code examples, in slide order, as ONE source of truth.

Each example is a list of line groups; a group is (code lines, a plain-language note). The deck shows the groups with the
note beside each, the page tab lists the same examples by NAME in the same order, and the result shown on a slide is what
this file's runner PRINTS when the example is executed (python3.14, the chapter library sen0401_ch05_wallet_lib_v1_1_0.py
plus the PRELUDE below). Nothing on a slide's result is typed: it is read from the run.

Usage: deck_examples_remedy_v3_0_0.py   (runs every example, prints the output, exits 1 on any error or line over 56 characters)"""
__version__ = "3.0.0"
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))
LIB = "sen0401_ch05_wallet_lib_v1_1_0"
PY = os.environ.get("PY314", "/root/.local/bin/python3.14")
MAXLINE = 56

# The sample data every example may use (the chapter's own worked example and BIP32 / BIP84 test data). The page defines these names too.
PRELUDE = '''import json
sha256_hex = lambda b: hashlib.sha256(b).hexdigest()
ENT = "0c1e24e5917779d297e14d45f14e1a1a"
WORDS = "army van defense carry jealous true garbage claim echo media make crunch"
PASSPHRASE = "SuperDuperSecret"
TV = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
B84 = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
DESC = ("wpkh([73c5da0a/84h/0h/0h]xpub6CatWdiZiodmUeTDp8LT5or8nmbKNcuyvz7WyksVFkKB4RHwCD3Xyuv"
        "PEbvqAQY3rAPshWcMLoP2fMFMKHPJ4ZeZXYVUhLv1VMrjPC7PW6V/0/*)")
C32 = "ms10testsxxxxxxxxxxxxxxxxxxxxxxxxxx4nzvca9cmczlw"
BOOK_XPUB = ("xpub67xpozcx8pe95XVuZLHXZeG6XWXHpGq6Qv5cmNfi7cS5mtjJ2tgypeQbB"
             "s2UAR6KECeeMVKZBPLrtJunSDMstweyLXhRgPxdp14sk9tJPW9")
'''

EXAMPLES = [
    dict(id="loose_vs_seed", name="Loose keys versus one seed", concepts=["independent key generation", "deterministic key generation", "seed"],
         groups=[
             (['seed = b"my seed"', 'key = lambda i: sha256_hex(seed + bytes([i]))'],
              "One secret, and a rule that turns it into key number i."),
             (['keys = [key(i)[:8] for i in range(3)]', 'print(keys)'],
              "Ask the rule for keys 0, 1 and 2; show the first eight characters of each."),
             (['again = [key(i)[:8] for i in range(3)]', 'print(keys == again)'],
              "Run it again. The same seed gives the same keys, so one backup is enough."),
         ]),
    dict(id="hash_avalanche", name="A hash function changes half its bits", concepts=["hash function", "SHA-256 and SHA-512"],
         groups=[
             (['a = hashlib.sha256(b"seed A").digest()', 'b = hashlib.sha256(b"seed B").digest()'],
              "Hash two inputs that differ by one letter with SHA-256."),
             (['diff = int(a.hex(), 16) ^ int(b.hex(), 16)', 'print(len(a) * 8, bin(diff).count("1"))'],
              "XOR the results and count the bits that differ: about half of the 256 change."),
         ]),
    dict(id="entropy_sizes", name="How many words for how much entropy", concepts=["entropy", "code length", "security strength"],
         groups=[
             (['for bits in (128, 160, 192, 224, 256):', '    ent = bytes(bits // 8)'],
              "Five allowed entropy sizes, from 128 to 256 bits."),
             (['    n = len(entropy_to_mnemonic(ent).split())', '    print(bits, n)'],
              "Turn each into a recovery code and count its words: 12, 15, 18, 21 and 24."),
         ]),
    dict(id="entropy_to_words", name="From entropy to twelve words", concepts=["word list", "eleven-bit segment", "entropy"],
         groups=[
             (['words = entropy_to_mnemonic(bytes.fromhex(ENT))', 'print(words == WORDS)'],
              "The chapter's 128 bits of entropy become its twelve words."),
             (['idx = [wordlist().index(w) for w in words.split()]', 'print(idx)'],
              "Each word is a position, 0 to 2047, in the BIP39 list: eleven bits each."),
             (['print(format(idx[0], "011b"), words.split()[0])'],
              "Position 96 is the eleven bits 00001100000, the word army."),
         ]),
    dict(id="checksum", name="The checksum catches a wrong word", concepts=["checksum", "BIP39 checksum"],
         groups=[
             (['ent, ok = mnemonic_to_entropy(WORDS)', 'print(ent.hex(), ok)'],
              "Decode the code back to entropy and check the last four bits."),
             (['bad = WORDS.replace("crunch", "army")', 'print(mnemonic_to_entropy(bad)[1])'],
              "Change the last word. The recomputed checksum no longer matches."),
         ]),
    dict(id="normalisation", name="Text is normalised before stretching", concepts=["text normalisation"],
         groups=[
             (['s = "caf\\u00e9"', 'n = unicodedata.normalize("NFKD", s)'],
              "The same word can be one character or two: e-acute, or e plus an accent."),
             (['print(len(s), len(n))', 'print(mnemonic_to_seed(s) == mnemonic_to_seed(n))'],
              "Normalising makes both spellings give the same seed on every device."),
         ]),
    dict(id="pbkdf2_salt", name="PBKDF2 stretches the words with a salt", concepts=["key-stretching function", "PBKDF2", "salt", "root seed"],
         groups=[
             (['def stretch(salt, rounds):', '    d = hashlib.pbkdf2_hmac(', '        "sha512", WORDS.encode(), salt, rounds)', '    return d.hex()[:12]'],
              "PBKDF2 with HMAC-SHA512 repeats the work many times on the words."),
             (['print(stretch(b"mnemonic", 1))', 'print(stretch(b"mnemonic", 2048))', 'print(stretch(b"mnemonic1", 2048))'],
              "One round, 2048 rounds, and another salt: three unrelated results. BIP39 uses 2048 rounds."),
         ]),
    dict(id="passphrase_wallets", name="A passphrase opens a different wallet", concepts=["recovery code passphrase", "optional passphrase in BIP39", "plausible deniability", "duress wallet"],
         groups=[
             (['path = "m/84h/0h/0h/0/0"', 'def addr(pp):'],
              "Pick one key path and define a helper that returns its address."),
             (['    k, c = keys_at(WORDS, path, pp)', '    return p2wpkh_address(ser_p(ec_mul(k)))'],
              "The helper derives the key from the words plus the passphrase."),
             (['print(addr(""))', 'print(addr(PASSPHRASE))'],
              "Same twelve words, two passphrases, two different addresses."),
         ]),
    dict(id="master_key", name="HMAC-SHA512 makes the master key", concepts=["HMAC-SHA512", "master private key", "master chain code", "root seed"],
         groups=[
             (['h = hmac.new(b"Bitcoin seed", TV, hashlib.sha512)', 'I = h.digest()', 'left, right = I[:32], I[32:]'],
              "One HMAC-SHA512 of the seed gives 64 bytes, split into two halves."),
             (['print(len(I), len(left), len(right))', 'k, c = master(TV)'],
              "The library function master() does the same in one call."),
             (['print(k == int.from_bytes(left, "big"), c == right)', 'print("%064x" % k)'],
              "Left half is the master private key, right half the master chain code."),
         ]),
    dict(id="child_keys", name="Child keys from a parent and an index", concepts=["child key derivation", "chain code", "index number", "private child key derivation"],
         groups=[
             (['k, c = master(TV)', 'for i in range(3):'],
              "Start at the master pair and ask for children 0, 1 and 2."),
             (['    ki, ci = ckd_priv(k, c, i)', '    print(i, "%064x" % ki, ci.hex())'],
              "Each child gets its own key and its own chain code, so the tree can keep growing."),
         ]),
    dict(id="hardened", name="Hardened and normal children differ", concepts=["hardened derivation", "hardened child key derivation", "index numbers for normal and hardened derivation"],
         groups=[
             (['k, c = master(TV)', 'normal, _ = ckd_priv(k, c, 0)'],
              "Child number 0 is in the normal range, below 2 to the 31."),
             (['hard, _ = ckd_priv(k, c, HARD)', 'print(HARD, normal == hard)'],
              "Child number 2147483648 is the first hardened one: a different key."),
             (['print(path_indices("m/0h") == [HARD])'],
              "In a path, the letter h adds 2 to the power 31 to the index."),
         ]),
    dict(id="xpub_leak", name="Why hardened steps protect the parent", concepts=["child key independence", "extended public key", "using derived child keys"],
         groups=[
             (['k, c = master(TV)', 'K = ec_mul(k)'],
              "Take a parent key and its public key K."),
             (['kid, _ = ckd_priv(k, c, 5)', 'back = leak_parent_private_key(K, c, 5, kid)'],
              "With the extended public key and ONE normal child private key, subtract the hash value."),
             (['print(back == k)'],
              "The parent private key falls out. A hardened step cannot be undone this way."),
         ]),
    dict(id="public_derivation", name="Public keys derived without private keys", concepts=["public child key derivation", "extended public key deployment"],
         groups=[
             (['k, c = master(TV)', 'K = ec_mul(k)'],
              "The parent private key and its public key."),
             (['k5, _ = ckd_priv(k, c, 5)', 'K5, _ = ckd_pub(K, c, 5)'],
              "Route one: derive the private child, then its public key. Route two: use only K."),
             (['print(ec_mul(k5) == K5)'],
              "Both routes give the same public key, so a shop can make addresses without any private key."),
         ]),
    dict(id="extended_keys", name="Extended keys: xprv, xpub and a fingerprint", concepts=["extended key", "extended private key", "extended public key", "extended key encoding", "key fingerprint"],
         groups=[
             (['k, c = master(TV)', 'xprv = serialize_xprv(k, c)'],
              "A key plus its chain code, written in Base58Check."),
             (['xpub = serialize_xpub(ec_mul(k), c)', 'print(xprv[:4], len(xprv), xpub[:4], len(xpub))'],
              "The same for the public key: xprv and xpub, both 111 characters long."),
             (['print(fingerprint(ec_mul(k)).hex())', 'print(parse_extended(xpub)["depth"])'],
              "Four bytes identify the key; the depth says how far down the tree we are."),
         ]),
    dict(id="key_path", name="Reading a key path level by level", concepts=["HD wallet path", "purpose level (BIP43)", "BIP44 structure", "account branch", "change branch", "address index"],
         groups=[
             (['path = "m/84h/0h/0h/1/7"', 'idx = path_indices(path)'],
              "A path is a list of child numbers below the master key m."),
             (['names = "purpose coin account change index".split()', 'for n, i in zip(names, idx):'],
              "Five levels, as BIP43 and BIP44 define them."),
             (['    print(n, i, i >= HARD)'],
              "Print each number and whether it is hardened: the first three are."),
         ]),
    dict(id="standard_paths", name="Four standard paths, four address types", concepts=["BIP44 path for legacy scripts", "BIP49 path for nested segwit", "BIP84 path for native segwit", "BIP86 path for single-key taproot", "implicit path", "output script"],
         groups=[
             (['pub = lambda p: ser_p(ec_mul(keys_at(B84, p)[0]))', 'a44 = p2pkh(pub("m/44h/0h/0h/0/0"))'],
              "Purpose 44 gives a legacy pay-to-public-key-hash address, and it starts with 1."),
             (['s = b"\\x00\\x14" + hash160(pub("m/49h/0h/0h/0/0"))', 'a49 = b58check(b"\\x05" + hash160(s))'],
              "Purpose 49 wraps a segwit script inside a script hash."),
             (['a84 = p2wpkh_address(pub("m/84h/0h/0h/0/0"))', 'q = taproot_output_key(pub("m/86h/0h/0h/0/0"))', 'a86 = p2tr_address(q)', 'print(a44, a49, a84, a86, sep="\\n")'],
              "Purposes 84 and 86 give native segwit and taproot addresses. Print all four."),
         ]),
    dict(id="bip84_vector", name="Our address equals the standard's own", concepts=["explicit path", "BIP44"],
         groups=[
             (['k, c = keys_at(B84, "m/84h/0h/0h/0/0")', 'addr = p2wpkh_address(ser_p(ec_mul(k)))'],
              "Derive the first address of the BIP84 test recovery code."),
             (['published = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"', 'print(addr == published)'],
              "Compare it with the address printed in BIP84 and derived by Bitcoin Core."),
         ]),
    dict(id="descriptor", name="A descriptor with its checksum and key origin", concepts=["output script descriptor", "descriptor checksum", "key origin", "multipath descriptor"],
         groups=[
             (['print(descsum_create(DESC)[-8:])'],
              "The eight-character checksum that BIP380 appends after the hash sign."),
             (['fp, steps = parse_origin(DESC)', 'print(fp, [s >= HARD for s in steps])'],
              "The bracket at the start names the parent fingerprint and the hardened path."),
             (['multi = "wsh(multi(2,A,B,C))"', 'print(descsum_create(multi))'],
              "A two-of-three multisignature descriptor gets its own checksum."),
         ]),
    dict(id="gap_limit", name="The gap limit decides how far a scan looks", concepts=["gap limit"],
         groups=[
             (['used = {0, 3, 25}', 'for gap in (5, 10, 20, 30):'],
              "A wallet received payments on keys 0, 3 and 25."),
             (['    found = scan_with_gap(used, gap)', '    print(gap, len(found))'],
              "Scan, stopping after gap unused keys in a row. Gaps below 22 miss key 25."),
         ]),
    dict(id="xpub_shop", name="A web shop that holds no private key", concepts=["payment processor", "wallet with public keys only", "extended public key deployment"],
         groups=[
             (['acct = parse_extended(BOOK_XPUB)', 'K = decompress(acct["key"])'],
              "The shop is given only an extended public key."),
             (['for i in range(3):', '    Ki, _ = ckd_pub(K, acct["chain"], i)'],
              "For each customer it derives the next public key."),
             (['    print(i, p2wpkh_address(ser_p(Ki)))'],
              "A fresh address per customer, and no private key anywhere on the server."),
         ]),
    dict(id="shamir", name="Three of five shares recover the secret", concepts=["secret sharing", "SLIP39 share set"],
         groups=[
             (['secret = 0x1337c0de', 'shares = shamir_split(secret, 3, 5, [11, 22])'],
              "Split a secret into five shares; any three can rebuild it."),
             (['print(shamir_combine(shares[:3]) == secret)', 'print(shamir_combine(shares[1:4]) == secret)'],
              "Two different groups of three both recover the secret."),
             (['print(shamir_combine(shares[:2]) == secret)'],
              "Two shares give a wrong answer and reveal nothing."),
         ]),
    dict(id="other_schemes", name="Other recovery codes check themselves differently", concepts=["codex32", "Electrum v2", "BIP39", "Aezeed", "Muun"],
         groups=[
             (['print(codex32_check(C32))'],
              "codex32 carries a long checksum that can be checked by hand."),
             (['n = next(i for i in range(99999)', '         if electrum_has_version("seed %d" % i, "100"))'],
              "Electrum marks a seed by the first digits of an HMAC. Search for one marked 100."),
             (['print(n, electrum_hash("seed %d" % n)[:3])'],
              "The search stops at the first match and shows the marker."),
         ]),
    dict(id="key_tweak", name="A key tweak makes the taproot key", concepts=["key tweak"],
         groups=[
             (['k, c = keys_at(B84, "m/86h/0h/0h/0/0")', 'P = ser_p(ec_mul(k))'],
              "This is the internal key of the BIP86 path, before the tweak."),
             (['Q = taproot_output_key(P)', 'print(P[1:].hex()[:12], Q.hex()[:12])'],
              "Add a hash-derived number times the generator point: a tweaked output key."),
             (['print(p2tr_address(Q))'],
              "The address encodes the tweaked key, not the internal one."),
         ]),
    dict(id="labels", name="Labels exported in the BIP329 format", concepts=["label", "address label", "transaction label", "BIP329", "label export format (BIP329)"],
         groups=[
             (['a = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"', 'rows = [dict(type="addr", ref=a, label="rent"),'],
              "A label names an address or a transaction."),
             (['        dict(type="tx", ref="ab" * 32, label="pay")]', 'for r in rows: print(json.dumps(r))'],
              "BIP329 writes one JSON object per line, so any program can read the backup."),
         ]),
    dict(id="signature", name="A digital signature fails if the message changes", concepts=["digital signature"],
         groups=[
             (['d = 0x1337', 'pub = ec_mul(d)'],
              "A toy private key and its public key."),
             (['z = int(sha256_hex(b"pay 1"), 16)', 'sig = ecdsa_sign(d, z, 4242)'],
              "Sign the hash of a message (never choose the nonce yourself in real life)."),
             (['z2 = int(sha256_hex(b"pay 2"), 16)', 'print(ecdsa_verify(pub, z, sig))', 'print(ecdsa_verify(pub, z2, sig))'],
              "The signature verifies for the signed message and fails for any other."),
         ]),
    dict(id="index_space", name="2 to the 31 children, normal and hardened", concepts=["index number"],
         groups=[
             (['print(2**31, HARD, 2**31 - 1)'],
              "The book writes 2,147,483,647 for the count; BIP32 counts 2 to the 31 for each kind."),
             (['print(len(range(0, HARD)), len(range(HARD, 2 * HARD)))'],
              "Indexes 0 to 2^31 - 1 are normal, 2^31 to 2^32 - 1 hardened: equal counts."),
         ]),
    dict(id="restore_drill", name="The restore drill: a typo opens another wallet", concepts=["testing a backup", "written backup", "data loss"],
         groups=[
             (['def first(words):', '    k, c = keys_at(words, "m/84h/0h/0h/0/0")'],
              "A helper that derives the first address from a recovery code."),
             (['    return p2wpkh_address(ser_p(ec_mul(k)))', 'noted = first(B84)'],
              "Write down this address when the wallet is created."),
             (['print(first(B84) == noted)', 'print(first(B84.replace("about", "above")) == noted)'],
              "Restore from the right code: match. One wrong word: a different, empty wallet."),
         ]),
]


# slide order of the code slides (the manifest and the page tab keep this order)
ORDER = ["loose_vs_seed", "other_schemes", "shamir", "hash_avalanche", "entropy_sizes", "entropy_to_words", "checksum", "normalisation",
         "pbkdf2_salt", "passphrase_wallets", "master_key", "child_keys", "hardened", "xpub_leak", "public_derivation", "extended_keys",
         "index_space", "key_path", "standard_paths", "bip84_vector", "key_tweak", "descriptor", "labels", "xpub_shop", "gap_limit",
         "signature", "restore_drill"]
assert sorted(ORDER) == sorted(e["id"] for e in EXAMPLES)
EXAMPLES.sort(key=lambda e: ORDER.index(e["id"]))
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_text(ex):
    return "\n".join(l for g, _ in ex["groups"] for l in g)


RUNNER = r'''
import sys, io, contextlib
sys.path.insert(0, %(tool)r)
from %(lib)s import *
ns = dict(globals())
exec(%(prelude)r, ns)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(%(code)r, ns)
sys.stdout.write(buf.getvalue())
'''


def run(ex, timeout=120):
    src = RUNNER % dict(tool=TOOLING, lib=LIB, prelude=PRELUDE, code=code_text(ex))
    r = subprocess.run([PY, "-B", "-c", src], capture_output=True, text=True, timeout=timeout, cwd=TOOLING)
    if r.returncode:
        raise SystemExit("EXAMPLE %s FAILED: %s" % (ex["id"], r.stderr.strip()[-500:]))
    return r.stdout


def run_all():
    return {ex["id"]: run(ex) for ex in EXAMPLES}


if __name__ == "__main__":
    bad = 0
    for ex in EXAMPLES:
        for g, _ in ex["groups"]:
            for l in g:
                if len(l) > MAXLINE:
                    print("LONG LINE (%d) in %s: %s" % (len(l), ex["id"], l)); bad += 1
        print("==", ex["id"]); print(run(ex)[:700], end="")
    sys.exit(1 if bad else 0)
