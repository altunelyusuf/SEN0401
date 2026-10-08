#!/usr/bin/env python3
"""Writes ch07-page/question_bank_v1_0_0.json, the question bank of SEN0401 chapter 7: at least one item for every node of the chapter
(branch, group and concept), at least two for every concept with a worked example, one of those two an Apply item whose program prints
the marked option. Follows chapter 6's sen0401_ch06_bank_gen_v1_0_0.py: the items are kept here as tuples (concept, level, question,
options with the RIGHT one first, why, code or None); the right option of an Apply item is never typed - it is what the item's program
printed when this script ran it under CPython 3.14 - and the script rotates the right option to a position that cycles 0, 1, 2, 3
through the bank, so each position carries a quarter of the items.
Every program uses the standard library only and no file access, because the page runs it in the reader's browser (Pyodide, an older
CPython), and the checker re-runs each one under every older interpreter on this machine.
Run: python3 sen0401_ch07_bank_gen_v1_0_0.py        then: python3 question_bank_check_v1_2_0.py 07"""
__version__ = "1.0.0"
import json, os, re, subprocess, sys

PY = "/root/.local/bin/python3.14"
I = []     # (concept, level, q, [right, wrong, wrong, wrong], why, code)


def q(concept, level, question, options, why):
    I.append((concept, level, question, options, why, None))


def a(concept, question, code, wrongs, why):
    """an Apply item: the right option is whatever the program prints, filled in when the bank is built"""
    I.append((concept, "Apply", question, [None] + list(wrongs), why, code))


# ---- shared program text (a program is one string; these are prefixes) ----
B58 = """import hashlib
A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58check(version, payload):
    d = bytes([version]) + payload
    d += hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]
    n, s = int.from_bytes(d, 'big'), ''
    while n:
        n, r = divmod(n, 58)
        s = A[r] + s
    return '1' * (len(d) - len(d.lstrip(b'\\0'))) + s
"""
EC = """import hashlib
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
def add(a, b):
    if a is None or b is None:
        return a or b
    if a[0] == b[0] and (a[1] + b[1]) % P == 0:
        return None
    m = (3 * a[0] * a[0] * pow(2 * a[1], -1, P) if a == b else (b[1] - a[1]) * pow(b[0] - a[0], -1, P)) % P
    x = (m * m - a[0] - b[0]) % P
    return x, (m * (a[0] - x) - a[1]) % P
def mul(k, p):
    r = None
    while k:
        if k & 1:
            r = add(r, p)
        p, k = add(p, p), k >> 1
    return r
"""
TAG = """def tagged(tag, data):
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + data).digest()
def leaf(script): return tagged('TapLeaf', bytes([0xc0, len(script)]) + script)
def branch(x, y): return tagged('TapBranch', min(x, y) + max(x, y))
"""
SCH = EC + TAG + """def lift_x(x):
    y = pow((pow(x, 3, P) + 7) % P, (P + 1) // 4, P)
    return None if pow(y, 2, P) != (x ** 3 + 7) % P else (x, y if y % 2 == 0 else P - y)
def sign(d, msg, k):
    pt = mul(d, G)
    d = d if pt[1] % 2 == 0 else N - d
    r_pt = mul(k, G)
    k = k if r_pt[1] % 2 == 0 else N - k
    e = int.from_bytes(tagged('BIP0340/challenge', r_pt[0].to_bytes(32, 'big') + pt[0].to_bytes(32, 'big') + msg), 'big') % N
    return r_pt[0].to_bytes(32, 'big') + ((k + e * d) % N).to_bytes(32, 'big')
def verify(pub32, msg, sig):
    pt, r, s = lift_x(int.from_bytes(pub32, 'big')), int.from_bytes(sig[:32], 'big'), int.from_bytes(sig[32:], 'big')
    e = int.from_bytes(tagged('BIP0340/challenge', sig[:32] + pub32 + msg), 'big') % N
    r_pt = add(mul(s, G), mul(N - e, pt))
    return r_pt is not None and r_pt[1] % 2 == 0 and r_pt[0] == r
"""
RUN = """def run(ops, st):
    ex = [True]
    for w in ops:
        if w == 'IF':
            c = st.pop() if ex[-1] else 0
            ex.append(ex[-1] and bool(c))
        elif w == 'ELSE':
            ex[-1] = all(ex[:-1]) and not ex[-1]
        elif w == 'ENDIF':
            ex.pop()
        elif all(ex):
            st.append(int(w))
    return st
"""

# ============================== 1 TRANSACTION SCRIPTS AND THE SCRIPT LANGUAGE ==============================
q("ScriptLanguage", "Understand", "What question does the idea of an authorization script answer when you receive bitcoins?",
  ["Who may spend them later, and how that person must prove it", "Which exchange holds them for you", "How many confirmations the payment needs", "What the next block reward will be"],
  "An output carries the conditions for spending it, and a later spend carries the proof that the conditions are met.")
q("ScriptModel", "Remember", "Which two things does Script describe, according to the definition of the language?",
  ["The conditions for spending an output and the proof that they are met", "The price of a coin and the fee for a spend", "The blocks of a chain and their order", "The wallets of two parties and their balance"],
  "Script is the stack-based language in which both the conditions and the proof are written.")
q("Script", "Remember", "What kind of language is Script?",
  ["A Forth-like, stack-based language", "A compiled object-oriented language", "A markup language like HTML", "A query language like SQL"],
  "Script reads left to right, pushes data and lets each operator pop its inputs and push its result.")
a("Script", "A script is '2 3 ADD 5 EQUAL'. A tiny interpreter runs it. What does the stack hold at the end?",
  "st = []\nfor w in '2 3 ADD 5 EQUAL'.split():\n    if w == 'ADD':\n        b, a = st.pop(), st.pop()\n        st.append(a + b)\n    elif w == 'EQUAL':\n        b, a = st.pop(), st.pop()\n        st.append(int(a == b))\n    else:\n        st.append(int(w))\nprint(st)",
  ["[5]", "[2, 3, 5]", "[]"], "ADD leaves 5, EQUAL compares it with the pushed 5 and leaves a true value, written 1.")
q("StackExecution", "Remember", "What happens to the operands of an operator such as ADD?",
  ["It pops them and pushes the result", "It reads them from a file and keeps them", "It leaves them and pushes a copy of the result below", "It pushes them again in reverse order"],
  "Each operator pops its inputs and pushes its result.")
a("StackExecution", "A stack holds [1, 2]. The script runs SWAP and then DUP. What does the stack hold?",
  "st = [1, 2]\nst[-2:] = st[-1], st[-2]\nst.append(st[-1])\nprint(st)", ["[1, 2, 2]", "[2, 1]", "[2, 2, 1]"],
  "SWAP exchanges the top two items, giving [2, 1], and DUP copies the top, giving [2, 1, 1].")
q("TuringIncompleteness", "Understand", "Why is it an advantage that Script has no loops?",
  ["Every script ends, so its running time is predictable", "Scripts become shorter than any loop", "Nodes may skip checking the script", "Signatures no longer need to be valid"],
  "A loop-free language cannot run forever, which protects every node from a script that never ends.")
a("TuringIncompleteness", "A script of four opcodes has no loops. At most how many opcodes does a node execute for it?",
  "ops = ['DUP', 'HASH160', 'EQUALVERIFY', 'CHECKSIG']\nsteps = 0\nfor op in ops:\n    steps += 1\nprint(steps)", ["Unbounded", "16", "8"],
  "Without loops each opcode runs at most once, so the work is bounded by the length of the script.")
q("StatelessVerification", "Understand", "What does stateless verification mean for a script?",
  ["Nothing is kept before or after it runs, so every node gets the same verdict", "The script cannot read the stack", "Only one node may verify each script", "The script may depend on the time of the node's clock"],
  "The only inputs are the transaction and the scripts, so the result is the same on any system.")
a("StatelessVerification", "A verifier takes only its inputs and keeps nothing. Do two runs on the same inputs give the same verdict?",
  "def verdict(script):\n    return sum(script) == 5\nprint(verdict([2, 3]) == verdict([2, 3]))", ["False", "None", "5"],
  "A function of its inputs alone gives the same answer every time.")
q("ScriptLimits", "Remember", "What is the consensus limit on the size of an item that a script pushes?",
  ["520 bytes", "80 bytes", "10,000 bytes", "32 bytes"],
  "Elements are limited to 520 bytes, which also bounds a redeem script.")
a("ScriptLimits", "A script may be 10,000 bytes long. How many pushes of 520 bytes (each takes a 3-byte header) fit in it?",
  "print(10000 // (520 + 3))", ["20", "19.2", "24"], "Each push costs 523 bytes, and 19 of them take 9,937.")

q("ScriptExecution", "Understand", "How does a spend reach its verdict?",
  ["The input script and the output script are run, and the result must be true", "A miner votes on the script", "The wallet signs a receipt for the node", "The fee decides the verdict"],
  "A spend is valid when both scripts run without error and leave true on top of the stack.")
q("OutputScript", "Remember", "What is the name of the output script in Bitcoin Core's code?",
  ["scriptPubKey", "scriptSig", "witnessScript", "redeemScript"], "The output script states the conditions and is called scriptPubKey in the code.")
a("OutputScript", "A pay to public key hash output script is 76a914<20 bytes>88ac. How long is it, what is its first byte and what is its last byte?",
  "spk = bytes.fromhex('76a914ab68025513c3dbd2f7b92a94e0581f5d50f654e788ac')\nprint(len(spk), spk[0], spk[-1])", ["23 169 135", "25 169 172", "24 118 172"],
  "It is 25 bytes: OP_DUP (118), OP_HASH160, a 20-byte push, OP_EQUALVERIFY and OP_CHECKSIG (172).")
q("InputScript", "Remember", "What does a legacy input script usually hold?",
  ["A signature and a public key", "The whole previous transaction", "The recipient's name", "A proof of work"], "The input script satisfies the output script; for a key hash it supplies the signature and the key.")
a("InputScript", "An input script is a 71-byte push followed by a 33-byte push. What are the lengths of its pushes?",
  "ss = bytes([71]) + bytes(71) + bytes([33]) + bytes(33)\nitems, i = [], 0\nwhile i < len(ss):\n    n = ss[i]\n    items.append(n)\n    i += 1 + n\nprint(items)", ["[72, 34]", "[71]", "[104]"],
  "The loop reads a length byte, skips that many bytes and repeats.")
q("ScriptTruth", "Remember", "Which of these values makes a script fail when it is left on top of the stack?",
  ["Negative zero, written 0x80", "The number 1", "The number 16", "A 20-byte hash"], "Zero, negative zero, an empty item and an empty stack are false.")
a("ScriptTruth", "Which of the items 00, 80, 01 and the empty item count as true?",
  "def true(b):\n    for i, x in enumerate(b):\n        if x != 0:\n            return not (i == len(b) - 1 and x == 0x80)\n    return False\nprint([true(b'\\x00'), true(b'\\x80'), true(b'\\x01'), true(b'')])", ["[True, False, True, False]", "[False, True, True, False]", "[False, False, True, True]"],
  "Only the item 01 has a non-zero byte that is not a lone negative-zero marker.")
q("SeparateExecution", "Understand", "How are the input script and the output script run since 2010?",
  ["One after the other, with the stack passed from the first to the second", "Joined into a single script", "In parallel on two stacks", "Only the output script is run"],
  "Joining the two scripts allowed the OP_RETURN bug, so they are run separately.")
a("SeparateExecution", "The input script pushes 1. The output script is '1 ADD 2 EQUAL'. The scripts run one after the other on one stack. What does the stack hold at the end?",
  "st = [1]\nst.append(1)\nb, a = st.pop(), st.pop()\nst.append(a + b)\nst.append(2)\nb, a = st.pop(), st.pop()\nst.append(int(a == b))\nprint(st)", ["[2]", "[1, 1]", "[]"],
  "The output script starts with the input script's 1 on the stack: 1 plus 1 is 2, and EQUAL against 2 leaves a true value.")
q("OpReturnBug", "Understand", "Why could anyone spend any output in the first release?",
  ["OP_RETURN jumped to the end of the joined scripts, so a true value before it made the spend succeed", "The signatures were never checked at all", "The output script was missing", "Miners could rewrite every script"],
  "An input script of a true value and OP_RETURN skipped the output script.")
a("OpReturnBug", "In a joined script OP_RETURN jumps to the end. In separate execution OP_RETURN fails the script. For input '1 RETURN' and output '0', what do the two models give?",
  "def joined(ins, outs):\n    st = []\n    for w in ins + outs:\n        if w == 'RETURN':\n            break\n        st.append(int(w))\n    return bool(st and st[-1])\ndef separate(ins, outs):\n    return 'RETURN' not in ins and 'RETURN' not in outs\nprint(joined(['1', 'RETURN'], ['0']), separate(['1', 'RETURN'], ['0']))", ["False False", "True True", "False True"],
  "The joined model stops with a true 1 on top; the separate model fails the script at once.")

# ============================== 2 LOCKING TO A KEY ==============================
q("KeyLocking", "Understand", "What do the three ways of locking to a key in this branch have in common?",
  ["Each conditions the spend on a signature from a key, they differ in what the output reveals", "Each needs no signature", "Each needs three signatures", "Each hides the key from the spender forever"],
  "Pay to public key, to its hash and the check of the signature all authenticate the spender with a key.")
q("PayToKey", "Understand", "How does pay to public key hash differ from pay to public key?",
  ["The output holds a hash of the key, not the key", "The output holds the private key", "The output needs no signature", "The output holds the signature"],
  "The key is shown only when the output is spent.")
q("PayToPublicKey", "Remember", "How long is a pay to public key output script with an uncompressed key?",
  ["67 bytes", "25 bytes", "35 bytes", "22 bytes"], "A 65-byte key, its push byte and OP_CHECKSIG make 67 bytes.")
a("PayToPublicKey", "A pay to public key script pushes a 65-byte key and ends with OP_CHECKSIG (0xac). What are its length and last byte?",
  "spk = bytes([65]) + bytes(65) + bytes([0xac])\nprint(len(spk), hex(spk[-1]))", ["25 0xac", "66 0xac", "67 0x88"], "One length byte, 65 key bytes and one opcode.")
q("PublicKeyHash", "Remember", "Which two hash functions make a public key hash?",
  ["SHA-256 and then RIPEMD-160", "SHA-1 and MD5", "Two rounds of SHA-512", "Keccak-256 and then SHA-1"], "The result is 20 bytes.")
a("PublicKeyHash", "A legacy address is the Base58Check form of a 20-byte key hash with version 0. What is the first character of the address and the length of the hash?",
  B58 + "h = bytes.fromhex('ab68025513c3dbd2f7b92a94e0581f5d50f654e7')\nprint(b58check(0, h)[0], len(h))", ["3 20", "1 32", "b 20"], "Version 0 gives a leading 1; the hash is 20 bytes.")
q("PayToPublicKeyHash", "Understand", "What must the spender of a pay to public key hash output present?",
  ["A public key that matches the hash and a signature from its private key", "Only the hash", "Only a signature", "Two public keys"], "The script checks the hash and then the signature.")
a("PayToPublicKeyHash", "Name the operations in the output script 76 a9 14<hash> 88 ac in order.",
  "spk = bytes.fromhex('76a914ab68025513c3dbd2f7b92a94e0581f5d50f654e788ac')\nnames = {0x76: 'DUP', 0xa9: 'HASH160', 0x88: 'EQUALVERIFY', 0xac: 'CHECKSIG'}\nprint([names.get(b, 'PUSH') for b in (spk[0], spk[1], spk[2], spk[23], spk[24])])",
  ["['DUP', 'SHA256', 'PUSH', 'EQUAL', 'CHECKSIG']", "['PUSH', 'DUP', 'HASH160', 'EQUALVERIFY', 'CHECKSIG']", "['HASH160', 'PUSH', 'EQUAL']"], "The script duplicates the key, hashes it, compares the hashes and checks the signature.")

q("SignatureChecking", "Understand", "What does a node need to check a signature?",
  ["The public key, the signature and a hash of the spending transaction", "The private key", "The recipient's address book", "The miner's approval"], "The check needs no secret.")
q("OpChecksig", "Remember", "What does OP_CHECKSIG push when the signature is invalid?",
  ["False", "Nothing, the script fails at once", "The public key", "The transaction hash"], "OP_CHECKSIG pushes true or false.")
a("OpChecksig", "A toy ECDSA signature is made with private key 7, nonce 11 and a message hash. Does it verify, and does it verify for a different message hash?",
  EC + """def sign(d, z, k):
    r = mul(k, G)[0] % N
    return r, pow(k, -1, N) * (z + r * d) % N
def verify(q, z, r, s):
    w = pow(s, -1, N)
    pt = add(mul(z * w % N, G), mul(r * w % N, q))
    return pt is not None and pt[0] % N == r
q = mul(7, G)
r, s = sign(7, 12345, 11)
print(verify(q, 12345, r, s), verify(q, 12346, r, s))""", ["True True", "False False", "False True"], "The signature commits to the hash it was made for.")
q("SignatureHash", "Understand", "What does the hash type appended to a signature say?",
  ["Which parts of the transaction the signature commits to", "Which hash function the node must use", "How many signatures follow", "Which block the signature belongs to"], "ALL, NONE and SINGLE can be combined with ANYONECANPAY.")
a("SignatureHash", "ANYONECANPAY is 0x80 and SINGLE is 3. What is the hash type byte SINGLE|ANYONECANPAY?",
  "print(hex(3 | 0x80))", ["0x81", "0x03", "0x82"], "The two values are combined by setting bit 7 on top of 3.")
q("SignatureEncoding", "Remember", "Which encoding does Bitcoin use for an ECDSA signature?",
  ["DER, followed by a hash-type byte", "Base64", "Plain 64-byte concatenation of r and s", "ASCII hexadecimal"], "Strict DER is a consensus rule, and policy asks for the low s.")
a("SignatureEncoding", "r = 2**255 + 5 and s = 1 are written in DER with the hash-type byte appended. How many bytes is the result?",
  "def num(x):\n    b = x.to_bytes((x.bit_length() + 7) // 8, 'big')\n    return b'\\x00' + b if b[0] & 0x80 else b\ndef der(r, s):\n    body = b'\\x02' + bytes([len(num(r))]) + num(r) + b'\\x02' + bytes([len(num(s))]) + num(s)\n    return b'\\x30' + bytes([len(body)]) + body\nprint(len(der(2**255 + 5, 1)) + 1)", ["38", "72", "40"],
  "r needs a 0x00 prefix because its top bit is set, so it takes 33 bytes; with the headers, s and the hash type the total is 41.")

# ============================== 3 SCRIPTED MULTISIGNATURES ==============================
q("ScriptedMultisig", "Understand", "What is the main idea of a scripted multisignature?",
  ["An output names several keys and needs a number of valid signatures from them", "An output needs the same key to sign several times", "An output is split among several blocks", "An output needs several miners"], "The output lists k keys and requires t signatures.")
q("MultisigForm", "Understand", "What are t and k in a t-of-k multisignature script?",
  ["t is the number of signatures required, k the number of keys listed", "t is the lock time, k the key hash", "t is the fee, k the size", "t is the version, k the sequence"], "A 2-of-3 script lists three keys and needs two signatures.")
q("ScriptedMultisignature", "Understand", "In what order must the signatures be given?",
  ["The same order as their keys in the script", "Any order", "Sorted by size", "Newest first"], "The opcode walks the keys and signatures together and cannot go back.")
a("ScriptedMultisignature", "Keys are A, B, C. Are the signature lists [A, C] and [C, A] accepted by an ordered scan?",
  "def ok(sigs, keys):\n    i = 0\n    for s in sigs:\n        while i < len(keys) and keys[i] != s:\n            i += 1\n        if i == len(keys):\n            return False\n        i += 1\n    return True\nprint(ok(['A', 'C'], ['A', 'B', 'C']), ok(['C', 'A'], ['A', 'B', 'C']))", ["False False", "True True", "False True"], "The second list needs a key that the scan already passed.")
q("MultisigLimits", "Remember", "How many keys can a script hash multisignature list?",
  ["15", "3", "20", "16"], "The 520-byte limit on a script element caps it at 15 compressed keys.")
a("MultisigLimits", "A t-of-k script with compressed keys takes 3 + 34k bytes. What is the largest k whose script fits in 520 bytes?",
  "print(max(k for k in range(1, 40) if 3 + 34 * k <= 520))", ["16", "20", "14"], "The 15-key script takes 513 bytes and the 16-key script takes 547.")
q("MultisigOddity", "Understand", "Which two quirks does this group describe?",
  ["The extra stack element and the number of signature checks", "The lock time and the sequence", "The hash type and the encoding", "The version and the marker"], "Both are consequences of how OP_CHECKMULTISIG was written.")
q("CheckmultisigDummy", "Remember", "What must the dummy element be since BIP147?",
  ["An empty byte array", "The number 1", "The hash of the script", "A signature"], "A non-empty dummy is rejected so that nobody can change it to alter the transaction identifier.")
a("CheckmultisigDummy", "Which item does OP_CHECKMULTISIG pop last from ['', sigB, sigC, 2, pkA, pkB, pkC, 3]?",
  "st = ['', 'sigB', 'sigC', '2', 'pkA', 'pkB', 'pkC', '3']\nn = int(st.pop())\nkeys = [st.pop() for _ in range(n)]\nm = int(st.pop())\nsigs = [st.pop() for _ in range(m)]\ndummy = st.pop()\nprint(repr(dummy), st)", ["'sigB' []", "'3' ['']", "'pkA' []"], "The extra item at the bottom is the dummy element.")
q("SignatureCheckCount", "Understand", "Why can one signature cost many checks?",
  ["Each failed comparison against a key is another signature check", "The signature is hashed many times", "The block must be rescanned", "The key is derived again"], "A matching key far from the start of the scan comes after many failures.")
a("SignatureCheckCount", "The keys are k0 to k4 and the scan starts at the last key. How many checks does a signature from k0 take, and one from k4?",
  "keys = ['k0', 'k1', 'k2', 'k3', 'k4']\ndef checks(signer):\n    n = 0\n    for k in reversed(keys):\n        n += 1\n        if k == signer:\n            return n\nprint(checks('k0'), checks('k4'))", ["1 5", "5 5", "2 4"], "The first key tried is the one at the top of the stack.")

# ============================== 4 PAY TO SCRIPT HASH ==============================
q("PayToScriptHash", "Understand", "What problem does pay to script hash solve?",
  ["Long scripts burden the payer, so the output holds only a hash and the spender supplies the script", "Miners need to read the script", "Signatures were too small", "Addresses were not unique"], "The payer pays to a short address and the later spender stores the script.")
q("P2shMechanism", "Understand", "Where is the script revealed in a pay to script hash payment?",
  ["In the input of the spend", "In the output that is created", "On a public website", "In the block header"], "The output holds only a hash; the spender reveals the script.")
q("PayToScriptHashOutput", "Remember", "How long is a pay to script hash output script?",
  ["23 bytes", "25 bytes", "34 bytes", "20 bytes"], "OP_HASH160, a 20-byte push and OP_EQUAL make 23 bytes.")
a("PayToScriptHashOutput", "The output script is OP_HASH160 (0xa9), a 20-byte push and OP_EQUAL (0x87). How many bytes is it?",
  "spk = bytes([0xa9, 20]) + bytes(20) + bytes([0x87])\nprint(len(spk))", ["22", "25", "34"], "One opcode, one length byte, 20 bytes and one opcode.")
q("RedeemScript", "Understand", "Where does the redeem script appear in the input script?",
  ["As its last item", "As its first item", "Nowhere, it is in the output", "In the witness only"], "The node hashes the last item and compares it with the hash in the output.")
a("RedeemScript", "An input script pushes an empty item, a 72-byte signature and a 105-byte script with PUSHDATA1. How long is the last item?",
  "ss = bytes([0]) + bytes([72]) + bytes(72) + bytes([0x4c, 105]) + bytes(105)\nitems, i = [], 0\nwhile i < len(ss):\n    op = ss[i]\n    i += 1\n    if op == 0:\n        items.append(b'')\n        continue\n    if op == 0x4c:\n        op = ss[i]\n        i += 1\n    items.append(ss[i:i + op])\n    i += op\nprint(len(items[-1]))", ["72", "0", "107"], "The parser reads three pushes; the last is the redeem script.")
q("P2shAddress", "Remember", "With which character does a P2SH address begin?",
  ["3", "1", "bc1", "m"], "Version byte 5 gives a leading 3.")
a("P2shAddress", "Encode a 20-byte script hash with version 5 in Base58Check. What are the first character and the length of the address?",
  B58 + "h = bytes.fromhex('54c557e07dde5bb6cb791c7a540e0a4796f5e97e')\nad = b58check(5, h)\nprint(ad[0], len(ad))", ["1 34", "3 20", "5 33"], "Version 5 gives an address of 34 characters starting with 3 for this hash.")
q("P2shConsequences", "Understand", "Who gains and who pays more with pay to script hash?",
  ["The payer gains a short address; the spender carries the long script", "The payer carries the long script", "The miner pays the fee", "Nobody changes"], "The storage and the fee move to the spender.")
q("P2shBenefits", "Understand", "Why does the payer of a P2SH output not need to know the script?",
  ["The payer pays to the hash, which looks like any other address", "The script is kept secret forever", "The script is empty", "The miner provides it"], "A complex payment becomes as easy as an ordinary one for the payer.")
a("P2shBenefits", "A bare 3-of-5 multisignature output with compressed keys takes 3 + 34 * 5 bytes. How many bytes does a P2SH output of 23 bytes save in the payer's output?",
  "print((3 + 34 * 5) - 23)", ["170", "126", "23"], "The 173-byte script becomes a 23-byte output; the 150 bytes move to the spender.")
q("P2shRules", "Understand", "Which rule applies to the input script of a P2SH spend?",
  ["It may only push data", "It may contain any opcode", "It must be empty", "It must contain OP_RETURN"], "Otherwise the script could change the redeem script's meaning.")
a("P2shRules", "A 2-of-3 redeem script has its signature operations counted. How many does accurate counting give, and how many does the legacy count of 20 give?",
  "def sigops(words, accurate):\n    n, prev = 0, None\n    for w in words:\n        if w in ('CHECKSIG', 'CHECKSIGVERIFY'):\n            n += 1\n        elif w in ('CHECKMULTISIG', 'CHECKMULTISIGVERIFY'):\n            n += int(prev) if accurate and prev and prev.isdigit() and 1 <= int(prev) <= 16 else 20\n        prev = w\n    return n\nw = ['2', 'pkA', 'pkB', 'pkC', '3', 'CHECKMULTISIG']\nprint(sigops(w, True), sigops(w, False))", ["2 20", "20 3", "3 3"], "With an OP_n before the operator the count is n, otherwise 20.")

# ============================== 5 DATA OUTPUT AND TIMELOCKS ==============================
q("DataAndTime", "Understand", "Which two subjects does this branch combine?",
  ["Recording data in an output and locking a spend in time", "Mining and fees", "Wallets and seeds", "Addresses and QR codes"], "OP_RETURN outputs and the absolute and relative timelocks.")
q("DataOutput", "Understand", "Why is data placed in an OP_RETURN output rather than a spendable one?",
  ["Nodes need not keep it in the set of unspent outputs", "It is encrypted there", "It is free of fees", "Miners refuse other outputs"], "It can never be spent, so it is not added to the UTXO set.")
q("OpReturnOutput", "Remember", "What can be spent from an OP_RETURN output?",
  ["Nothing, it can never be spent", "Everything after one block", "Only the data", "Only half of it"], "The output script fails whatever the input provides.")
a("OpReturnOutput", "An OP_RETURN output carries the 5 bytes 'hello' after a length byte. How many bytes is the whole output with its 8-byte amount and 1-byte script length?",
  "data = b'hello'\nspk = bytes([0x6a, len(data)]) + data\nprint(8 + 1 + len(spk))", ["14", "17", "13"], "The script is 7 bytes; with the amount and its length byte the output is 16.")
q("DataCarrierPolicy", "Remember", "Is the data carrier limit a consensus rule?",
  ["No, it is a relay policy that a node can change", "Yes, every block checks it", "Yes, but only for the first block", "No, it is a legal limit"], "A policy decides what a node relays, not what is valid.")
a("DataCarrierPolicy", "A standard transaction weighs at most 400,000 weight units. How many virtual bytes is that?",
  "print(400000 // 4)", ["400000", "1000000", "50000"], "Four weight units make one virtual byte.")
q("AbsoluteTimelocks", "Understand", "What does an absolute timelock fix?",
  ["A block height or a time before which a spend is not valid", "The age of an output", "The size of a signature", "The number of keys"], "The lock time field and OP_CHECKLOCKTIMEVERIFY work with a point in time.")
q("LockTimeLimits", "Understand", "What does the lock time field of a transaction not prevent?",
  ["The signer spending the same inputs in another transaction without a lock time", "Inclusion before the lock time", "A change of the amount", "A signature"], "Only the locked transaction is held back, so it is a promise that can be cancelled by spending the output elsewhere.")
a("LockTimeLimits", "A transaction has lock time 800000. Is it final in a block of height 800000, and in a block of height 800001?",
  "def final(lock, height):\n    return lock == 0 or lock < height\nprint(final(800000, 800000), final(800000, 800001))", ["True True", "False False", "True False"], "Core's rule is that the lock time must be less than the block height.")
q("CheckLockTimeVerify", "Understand", "Which condition makes OP_CHECKLOCKTIMEVERIFY fail?",
  ["The input's sequence is final (0xffffffff)", "The transaction has two outputs", "The key is compressed", "The output is small"], "A final input would make the lock time ineffective.")
a("CheckLockTimeVerify", "OP_CHECKLOCKTIMEVERIFY with operand 800000: what does it give for lock time 800000 and sequence 0xfffffffe, 799999 and the same sequence, and 800000 with sequence 0xffffffff?",
  "def cltv(n, lock, seq):\n    if seq == 0xffffffff or (n < 500_000_000) != (lock < 500_000_000) or n > lock:\n        return False\n    return True\nprint(cltv(800000, 800000, 0xfffffffe), cltv(800000, 799999, 0xfffffffe), cltv(800000, 800000, 0xffffffff))", ["True True False", "True False True", "False False False"], "Only the first call has an effective lock time of the same kind that is large enough.")
q("RelativeTimelocks", "Understand", "What does a relative timelock count from?",
  ["The block in which the spent output was confirmed", "The first block of the chain", "The time of the signature", "The moment the node starts"], "It measures the age of the output.")
q("RelativeTimelock", "Remember", "In which field of an input is a relative timelock encoded?",
  ["The sequence field", "The previous output index", "The witness", "The version"], "BIP68 gives the sequence field this meaning for version 2 transactions.")
a("RelativeTimelock", "Decode the sequences 144 and 0x00400064 as BIP68 locks.",
  "def decode(seq):\n    if seq & (1 << 31):\n        return 'no relative lock'\n    n = seq & 0xffff\n    return str(n * 512) + ' seconds' if seq & (1 << 22) else str(n) + ' blocks'\nprint(decode(144), '|', decode(0x00400064))", ["144 seconds | 100 blocks", "144 blocks | 100 seconds", "no relative lock | 51200 seconds"], "Bit 22 selects 512-second units, so 100 units are 51,200 seconds.")
q("CheckSequenceVerify", "Understand", "What is the minimum transaction version for OP_CHECKSEQUENCEVERIFY?",
  ["2", "1", "3", "0"], "Version 1 transactions do not enforce relative locks.")
a("CheckSequenceVerify", "OP_CHECKSEQUENCEVERIFY needs version 2, a relative lock of the same kind and an operand no larger than the sequence. Which of (4320, 4320, v2), (4320, 4319, v2), (4320, 4320, v1) pass?",
  "def csv(n, seq, version):\n    return version >= 2 and not seq & (1 << 31) and (n & (1 << 22)) == (seq & (1 << 22)) and (n & 0xffff) <= (seq & 0xffff)\nprint([csv(4320, 4320, 2), csv(4320, 4319, 2), csv(4320, 4320, 1)])", ["[True, True, False]", "[False, False, False]", "[True, False, True]"], "Only the first passes: the second is too young and the third has version 1.")

# ============================== 6 FLOW CONTROL AND COMPLEX SCRIPTS ==============================
q("FlowControl", "Understand", "What can a script do with flow control that a simple key lock cannot?",
  ["Offer several ways to spend, chosen by the spender", "Run loops without end", "Change the amount of the output", "Skip the signature check"], "Conditionals let one output have several redemption paths.")
q("Conditionals", "Understand", "Which two ideas does this group combine?",
  ["Conditional clauses that choose a path and VERIFY opcodes that guard one", "Loops and recursion", "Hashes and keys", "Fees and weights"], "Both control whether the script continues.")
q("ConditionalClauses", "Remember", "What does OP_IF read to choose its path?",
  ["The value on top of the stack", "The next opcode", "The block height", "The sequence of the input"], "The input script pushes the value.")
a("ConditionalClauses", "Run 'IF 2 ELSE 3 ENDIF' once with a stack [1] and once with [0]. What does the stack hold afterward?",
  RUN + "print(run('IF 2 ELSE 3 ENDIF'.split(), [1]), run('IF 2 ELSE 3 ENDIF'.split(), [0]))", ["[3] [2]", "[2] [2]", "[1, 2] [0, 3]"], "A true value runs the first path, a false one the ELSE path.")
q("VerifyGuard", "Understand", "What does EQUALVERIFY do that EQUAL does not?",
  ["It fails the script unless the items are equal and leaves nothing on the stack", "It pushes the larger of the two items", "It always succeeds", "It pushes the hash of the items"], "VERIFY variants are guard clauses.")
a("VerifyGuard", "Compare EQUAL and EQUALVERIFY on a stack [5, 5]. What is left on the stack by each?",
  "def equal(st):\n    b, a = st.pop(), st.pop()\n    st.append(int(a == b))\n    return st\ndef equalverify(st):\n    b, a = st.pop(), st.pop()\n    if a != b:\n        raise ValueError('fails')\n    return st\nprint(equal([5, 5]), equalverify([5, 5]))", ["[] [1]", "[1] [1]", "[5] []"], "EQUAL leaves a result; EQUALVERIFY leaves nothing and continues.")
q("MultiPathScript", "Understand", "How does the input script choose a path of a nested script?",
  ["By pushing a true or false value for each clause", "By signing with a special key", "By setting the lock time", "By naming the path in the output"], "Each IF consumes one of the pushed values.")
a("MultiPathScript", "A script is 'IF 10 ELSE IF 20 ELSE 30 ENDIF ENDIF'. What is left for the stacks [1], [1, 0] and [0, 0]?",
  RUN + "s = 'IF 10 ELSE IF 20 ELSE 30 ENDIF ENDIF'.split()\nprint(run(s, [1]), run(s, [1, 0]), run(s, [0, 0]))", ["[20] [10] [30]", "[10] [30] [20]", "[10] [10] [20]"], "The top value picks the outer clause and the next one picks the inner clause.")
q("ComplexScripts", "Understand", "What does the capital account example combine?",
  ["Several signers with timelocks and several paths", "Only one key", "A hash of a preimage", "A proof of work"], "It shows how script features compose.")
q("MohammedScript", "Understand", "Who can spend the capital account output after 90 days?",
  ["The lawyer alone", "Any one partner", "Nobody", "Two partners only"], "The third path unlocks after 90 days for the lawyer.")
a("MohammedScript", "Test the three paths: ages 0, 10, 30, 89 and 90 days with signers {A,B}, {L,A}, {L,A}, {L}, {L}.",
  "def can(age, signers):\n    partners = len(signers & {'A', 'B', 'C'})\n    return partners >= 2 or ('L' in signers and partners >= 1 and age >= 30) or ('L' in signers and age >= 90)\nprint([can(0, {'A', 'B'}), can(10, {'L', 'A'}), can(30, {'L', 'A'}), can(89, {'L'}), can(90, {'L'})])",
  ["[True, True, True, False, True]", "[False, False, True, False, True]", "[True, False, True, True, True]"], "The lawyer needs a partner until day 90.")
q("Miniscript", "Understand", "What does Miniscript make possible that arbitrary Script does not?",
  ["A program can analyse the result and construct witnesses", "Loops in scripts", "Unlimited script size", "Skipping signatures"], "Fragments with known behaviour are composed by rules.")
a("Miniscript", "Compile or_i(pk(A), and_v(v:pk(B), older(144))) with the fragment rules used here.",
  "def script(m):\n    k = m[0]\n    if k == 'pk':\n        return [m[1], 'CHECKSIG']\n    if k == 'older':\n        return [str(m[1]), 'CHECKSEQUENCEVERIFY']\n    if k == 'v':\n        s = script(m[1])\n        ver = {'CHECKSIG': 'CHECKSIGVERIFY', 'EQUAL': 'EQUALVERIFY'}.get(s[-1])\n        return s[:-1] + [ver] if ver else s + ['VERIFY']\n    if k == 'and_v':\n        return script(m[1]) + script(m[2])\n    if k == 'or_i':\n        return ['IF'] + script(m[1]) + ['ELSE'] + script(m[2]) + ['ENDIF']\nprint(' '.join(script(('or_i', ('pk', 'A'), ('and_v', ('v', ('pk', 'B')), ('older', 144))))))",
  ["A CHECKSIG IF B CHECKSIG 144 CHECKSEQUENCEVERIFY ENDIF", "IF A CHECKSIG ELSE B CHECKSIG 144 CHECKSEQUENCEVERIFY ENDIF", "IF A CHECKSIGVERIFY ELSE B CHECKSIG ENDIF"], "The v wrapper turns CHECKSIG into CHECKSIGVERIFY.")

# ============================== 7 SEGREGATED WITNESS SCRIPTS ==============================
q("SegwitScripts", "Understand", "What did segregated witness change about where the proof of a spend is kept?",
  ["It moved the proof into a separate witness structure", "It deleted the proof", "It put the proof in the block header", "It made the proof optional"], "The scripts' inputs live in the witness.")
q("WitnessPrograms", "Understand", "Which two things does this group describe?",
  ["The witness program format and the address that encodes it", "Fees and weights", "Lock times and sequences", "Seeds and keys"], "Program, P2WPKH, P2WSH and the bech32 address.")
q("WitnessProgram", "Remember", "Which version byte starts a taproot witness program?",
  ["OP_1", "OP_0", "OP_16", "OP_2"], "Version 0 is P2WPKH and P2WSH; version 1 is taproot.")
a("WitnessProgram", "Classify the output scripts 0014<20 bytes> and 5120<32 bytes> by version and length.",
  "def kind(spk):\n    ver = 0 if spk[0] == 0 else spk[0] - 80\n    prog = spk[2:]\n    if ver == 0 and len(prog) == 20:\n        return 'P2WPKH'\n    if ver == 0 and len(prog) == 32:\n        return 'P2WSH'\n    return 'P2TR' if ver == 1 and len(prog) == 32 else 'other'\nprint(kind(bytes([0, 20]) + bytes(20)), kind(bytes([0x51, 32]) + bytes(32)))", ["P2WSH P2TR", "P2WPKH P2WSH", "P2TR P2WPKH"], "Version 0 with 20 bytes is a key hash; version 1 with 32 bytes is taproot.")
q("P2wpkh", "Remember", "What does the witness of a P2WPKH spend contain?",
  ["A signature and a public key", "A script and a signature", "Only a signature", "A 32-byte hash"], "The input script is empty.")
a("P2wpkh", "How many bytes shorter is a P2WPKH output script (0014 plus 20 bytes) than a P2PKH one (25 bytes)?",
  "print(25 - len(bytes([0, 20]) + bytes(20)))", ["5", "1", "25"], "A P2WPKH output is 22 bytes.")
q("P2wsh", "Remember", "Which hash does a P2WSH output hold?",
  ["The 32-byte SHA-256 of the script", "The 20-byte HASH160 of the script", "The 32-byte SHA-256 of the key", "The double SHA-256 of the output"], "One SHA-256 gives 32 bytes.")
a("P2wsh", "The script OP_TRUE is the single byte 0x51. What is the length of its SHA-256 witness program and what are the first 8 hex digits?",
  "import hashlib\nh = hashlib.sha256(bytes([0x51])).digest()\nprint(len(h), h.hex()[:8])", ["20 4bf5122f", "32 e3b0c442", "32 00000000"], "SHA-256 outputs 32 bytes.")
q("SegwitAddress", "Remember", "Which encoding does a version 1 witness address use?",
  ["bech32m", "Base58Check", "bech32 with a different prefix", "Base64"], "Version 0 uses bech32; later versions use bech32m with a different checksum constant.")
a("SegwitAddress", "Build a mainnet address for the key hash of version 0 and for a 32-byte program of version 1. What are the first four characters of each?",
  """CH = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
def polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if (top >> i) & 1 else 0
    return chk
def address(hrp, version, program):
    const = 1 if version == 0 else 0x2bc830a3
    data, acc, bits = [version], 0, 0
    for byte in program:
        acc = (acc << 8) | byte
        bits += 8
        while bits >= 5:
            bits -= 5
            data.append((acc >> bits) & 31)
    if bits:
        data.append((acc << (5 - bits)) & 31)
    values = [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp] + data
    mod = polymod(values + [0] * 6) ^ const
    checksum = [(mod >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + '1' + ''.join(CH[d] for d in data + checksum)
print(address('bc', 0, bytes(20))[:4], address('bc', 1, bytes(32))[:4])""", ["bc1p bc1q", "bc1q bc1q", "bc1p bc1p"], "The data character after the separator is the version: q is 0 and p is 1.")
q("SegwitUpgrade", "Understand", "What are the two ways of putting segregated witness outputs to use?",
  ["Native witness outputs and nested ones inside a script hash", "Hard fork and rollback", "Mining and relaying", "Seeds and passwords"], "Nested outputs let old wallets pay a new kind of script.")
q("BackwardCompatibleUpgrade", "Understand", "How does an old node see a witness output?",
  ["As two pushes that anyone can spend", "As an invalid script", "As an OP_RETURN", "As a coinbase"], "That is why a soft fork works.")
a("BackwardCompatibleUpgrade", "An old node sees a version 0 witness program as two pushes: an empty item, then 20 bytes of non-zero data. Does the old node count the top item as true?",
  "stack = [b'', bytes([17]) * 20]\ntop = stack[-1]\nprint(any(top))", ["False", "None", "20"], "A non-empty item with a non-zero byte is true.")
q("NestedSegwit", "Understand", "What is the redeem script of a nested segwit output?",
  ["A witness program", "A public key", "An OP_RETURN script", "A multisignature script only"], "Old wallets pay to the 3 address and the receiver spends it with a witness.")
a("NestedSegwit", "A nested P2WPKH redeem script is 0014 plus a 20-byte hash. How many bytes does the input script take when it pushes it, and what character does the address start with?",
  B58 + "redeem = bytes([0, 20]) + bytes(20)\nprint(len(redeem) + 1, b58check(5, bytes(20))[0])", ["22 1", "22 3", "34 3"], "One length byte plus 22 bytes, and a leading 3 for version 5.")
q("WitnessSighash", "Understand", "Why does BIP143 make the signature hash cheaper for large transactions?",
  ["It reuses three hashes for all inputs", "It drops the signature", "It skips the outputs", "It hashes only one byte"], "The work grows with the size of the transaction and not with its square.")
a("WitnessSighash", "BIP143 hashes the value of the output being spent. Do two hashes of the same data with values 100000 and 100001 differ?",
  "import hashlib, struct\ndef h256(b):\n    return hashlib.sha256(hashlib.sha256(b).digest()).digest()\nprint(h256(b'tx' + struct.pack('<q', 100000)) != h256(b'tx' + struct.pack('<q', 100001)))", ["False", "None", "1"], "Committing to the amount means a wrong amount breaks the signature.")

# ============================== 8 SCRIPT TREES AND KEY TWEAKS ==============================
q("TreesAndTweaks", "Understand", "What do script trees and key tweaks have in common?",
  ["Both commit to more than a key with a hash", "Both use loops", "Both need a miner's key", "Both are only policy"], "A Merkle root or a tweak is hidden inside what looks like a key or hash.")
q("ScriptTrees", "Understand", "What is the benefit of putting alternative scripts in a Merkle tree?",
  ["Only the used script and a short proof are revealed", "All scripts are revealed", "The scripts are shortened", "No script is run"], "The cost grows with the depth of the tree.")
q("Mast", "Understand", "What does a spender reveal from a Merklized alternative script tree?",
  ["The used script and the hashes that connect it to the root", "Every script of the tree", "The private key", "The tree's depth only"], "One 32-byte hash per level.")
a("Mast", "How many sibling hashes does a proof need for balanced trees of 3, 4, 8 and 1,024 scripts?",
  "print([(n - 1).bit_length() for n in (3, 4, 8, 1024)])", ["[1, 2, 3, 10]", "[2, 2, 3, 1024]", "[2, 4, 8, 10]"], "The proof length is the depth of the tree.")
q("MastVersusAst", "Analyze", "Which statement about the two meanings of MAST is correct?",
  ["The alternative script tree commits to complete scripts and needs one hash per level", "The abstract syntax tree is the one used in taproot", "Both commit to every part of a program", "Neither uses a Merkle root"], "Taproot uses the alternative script tree.")
a("MastVersusAst", "A path to one of 1,000 alternative scripts shows the siblings plus the root. How many commitments is that?",
  "def commitments(n):\n    return (n - 1).bit_length() + 1\nprint(commitments(1000))", ["10", "1000", "12"], "Ten siblings and the root.")
q("KeyTweaks", "Understand", "What does a key tweak add to a public key?",
  ["A number derived from a commitment, times the generator", "A second signature", "A timestamp", "A checksum"], "The tweaked key still looks like a key.")
q("PayToContract", "Understand", "What does the payee need to spend a pay-to-contract output?",
  ["The private key plus the same number as the tweak", "Only the description", "Only the public key", "A new address"], "Adding the tweak to the private key matches adding it to the public key.")
a("PayToContract", "Pay to a key tweaked with the hash of 'one'. Is the key the same for the same description, and for the description 'two'?",
  EC + "def key(d):\n    return add(mul(11, G), mul(int.from_bytes(hashlib.sha256(d).digest(), 'big') % N, G))\nprint(key(b'one') == key(b'one'), key(b'one') == key(b'two'))", ["True True", "False False", "False True"], "The tweak commits to the description.")
q("ScriptlessMultisignature", "Understand", "What disappears in a scriptless multisignature?",
  ["The script that counts keys and signatures", "The signature", "The public key", "The transaction"], "The result looks like a single signer.")
a("ScriptlessMultisignature", "Two participants have private keys 5 and 6. Is the sum of their public keys the public key of 11?",
  EC + "print(add(mul(5, G), mul(6, G)) == mul(11, G))", ["False", "None", "11"], "Scalar multiplication distributes over addition of points.")
q("ThresholdSignature", "Analyze", "What is a drawback of a threshold signature for accountability?",
  ["It does not show which participants signed", "It needs more bytes", "It cannot be verified", "It reveals all keys"], "The signature looks ordinary.")
a("ThresholdSignature", "A line f(x) = 777 + 4242x gives shares at x = 1, 2, 3. Interpolating at 0 from the shares at 2 and 3 gives what?",
  "N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141\nsecret, a1 = 777, 4242\nshares = {x: (secret + a1 * x) % N for x in (1, 2, 3)}\ni, j = 2, 3\nprint((j * pow(j - i, -1, N) * shares[i] + (-i) * pow(j - i, -1, N) * shares[j]) % N)", ["4242", "0", "5019"], "Any two points of a line fix its value at x = 0.")

# ============================== 9 TAPROOT AND TAPSCRIPT ==============================
q("TaprootBranch", "Understand", "What are the two spending paths of a taproot output?",
  ["Key path and script path", "Hash path and time path", "Native path and nested path", "Fast path and slow path"], "The branch ends with tapscript, the language of the script path.")
q("TaprootOutputs", "Understand", "What does paying to a taproot output key also commit to?",
  ["The scripts of the tree", "The amount", "The fee", "The sender"], "The output key is the internal key tweaked by the tree's root.")
q("Taproot", "Remember", "How many bytes is the program of a taproot output?",
  ["32", "20", "33", "64"], "It is the x coordinate of the output key.")
a("Taproot", "Tweak the generator's x coordinate with no script tree. Is the output key different from the internal key?",
  SCH + "internal = G[0].to_bytes(32, 'big')\nt = int.from_bytes(tagged('TapTweak', internal), 'big')\nq = add(lift_x(G[0]), mul(t, G))\nprint(q[0].to_bytes(32, 'big') != internal)", ["False", "None", "32"], "Even with no scripts, BIP341 tweaks the key.")
q("KeyPathSpending", "Understand", "What does a key path spend reveal about the scripts?",
  ["Nothing", "All of them", "The first one", "Their hashes"], "A single signature is all that appears.")
a("KeyPathSpending", "Sign a message with a BIP340 signature and verify it. What do verification of the message and of another message give, and how long is the signature?",
  SCH + "d = 3\npub = mul(d, G)[0].to_bytes(32, 'big')\nmsg = hashlib.sha256(b'pay Bob').digest()\nsig = sign(d, msg, 5)\nprint(verify(pub, msg, sig), verify(pub, hashlib.sha256(b'pay Eve').digest(), sig), len(sig))", ["True True 64", "False False 64", "True False 65"], "A BIP340 signature is 64 bytes and commits to its message.")
q("ScriptPathSpending", "Understand", "What does a script path spend reveal?",
  ["One script, the control block and the data that satisfies it", "The whole tree", "The private key", "All the sibling scripts"], "Other scripts remain private.")
a("ScriptPathSpending", "A tree of four scripts: fold the first leaf with its proof. Does it match the root, and how long is the control block?",
  SCH + "l = [leaf(bytes([0x51 + i])) for i in range(4)]\nroot = branch(branch(l[0], l[1]), branch(l[2], l[3]))\nproof = [l[1], branch(l[2], l[3])]\nh = l[0]\nfor s in proof:\n    h = branch(h, s)\ncontrol = bytes([0xc0]) + bytes(32) + b''.join(proof)\nprint(h == root, len(control))", ["True 65", "False 97", "True 129"], "Two siblings make a control block of 33 + 64 bytes.")
q("ControlBlock", "Remember", "What does the first byte of the control block hold?",
  ["The leaf version and the parity of the output key", "The number of scripts", "The length of the proof", "The hash type"], "The remaining bytes are the internal key and the sibling hashes.")
a("ControlBlock", "Read the first byte 0xc1 of a control block with a 33-byte base and two hashes: version, parity and depth.",
  "control = bytes([0xc1]) + bytes(32) + bytes(64)\nprint(control[0] & 0xfe, control[0] & 1, (len(control) - 33) // 32)", ["193 0 2", "192 1 64", "194 1 2"], "The low bit is the parity and the other bits are the version, 0xc0.")
q("Tapscript", "Understand", "Which kind of script runs in a script path spend?",
  ["Tapscript", "Legacy Script", "Miniscript only", "A Forth interpreter"], "Tapscript is the version 0xc0 script language.")
q("TapscriptChanges", "Remember", "Which signature scheme does every signature check use in tapscript?",
  ["BIP340 Schnorr signatures", "ECDSA", "RSA", "Lamport signatures"], "OP_CHECKMULTISIG is disabled too.")
a("TapscriptChanges", "A 2-of-5 script is 3 + 34 * 5 bytes in legacy Script. In tapscript it is five 33-byte key pushes, one CHECKSIG, four CHECKSIGADD, OP_2 and NUMEQUAL. What are the two sizes?",
  "legacy = 3 + 34 * 5\ntap = 5 * 33 + 1 + 4 + 1 + 1\nprint(legacy, tap)", ["173 173", "172 173", "173 171"], "One byte is saved by dropping the legacy opcode.")
q("ChecksigAdd", "Understand", "What does OP_CHECKSIGADD do with an empty signature?",
  ["It leaves the number unchanged", "It fails the script", "It adds one", "It pushes the key"], "Only a non-empty invalid signature fails.")
a("ChecksigAdd", "Three signatures, the second empty and the others valid, are checked in a 2-of-3 chain. What is the final count?",
  "count = 0\nfor s in (b'a', b'', b'c'):\n    if s:\n        count += 1\nprint(count)", ["3", "1", "0"], "The empty signature counts nothing.")
q("OpSuccess", "Understand", "What happens when a tapscript contains an OP_SUCCESS opcode?",
  ["The script succeeds unconditionally", "The script fails", "The opcode is skipped", "The script is slow"], "This lets a soft fork give the opcode a meaning later.")
a("OpSuccess", "The OP_SUCCESS values include 80, 98, 126 to 129 and others. Is 0xac (OP_CHECKSIG) among them, and what is the smallest?",
  "success = {80, 98, *range(126, 130), *range(131, 135), 137, 138, 141, 142, *range(149, 154), *range(187, 255)}\nprint(0xac in success, min(success))", ["True 80", "False 126", "True 187"], "OP_CHECKSIG is a real opcode, and 80 is the smallest.")

# ============================== the file ==============================
_XMETA = re.compile(r"\b(chapter|section|the book|the author|the authors|this text)\b", re.I)
for k, it in enumerate(I):
    concept, level, question, options, why, code = it
    if code:
        r = subprocess.run([PY, "-c", code], capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            raise SystemExit("item %d (%s) failed: %s" % (k, concept, r.stderr[-300:]))
        out = r.stdout.strip()
        if not out:
            raise SystemExit("item %d (%s) printed nothing" % (k, concept))
        if out in options[1:]:
            raise SystemExit("item %d (%s): a distractor equals the real output %r" % (k, concept, out))
        options = [out] + options[1:]
        I[k] = (concept, level, question, options, why, code)
    assert len(options) == 4 and len(set(options)) == 4, (concept, options)
    assert not _XMETA.search(question) and not _XMETA.search(options[0]), (concept, question)
items = []
for k, (concept, level, question, options, why, code) in enumerate(I):
    pos = k % 4
    opts = options[1:1 + pos] + [options[0]] + options[1 + pos:]
    assert opts[pos] == options[0] and sorted(opts) == sorted(options), (concept, question)
    it = {"concept": concept, "level": level, "q": question, "options": opts, "answer": pos, "why": why}
    if code:
        it = {"concept": concept, "level": level, "q": question, "code": code, "options": opts, "answer": pos, "why": why}
    items.append(it)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch07-page", "question_bank_v1_0_0.json")
json.dump(items, open(out, "w"), indent=1)
import collections
print("wrote %s: %d items, %d concepts covered, %d with code" % (os.path.basename(out), len(items), len({i['concept'] for i in items}), sum(1 for i in items if 'code' in i)))
print("positions:", dict(sorted(collections.Counter(i["answer"] for i in items).items())))
