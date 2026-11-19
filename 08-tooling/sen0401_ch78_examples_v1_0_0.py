#!/usr/bin/env python3
"""sen0401_ch78_examples v1.0.0 - the corrected worked examples of chapters 7 and 8 (owner's material rulings of 2026-11-19, urgency).
One list per chapter. Each example gives its code as chunks: one chunk is one code box on the slide, and the chunks joined by a newline are
the code of the page's chapter code tab, so slide and page always show the same text. No lambda, no prompt markers, a comment line above each idea.
'show' lists the expressions the page checks after the run: (expression, expected value as printed). 'say' None keeps the slide's old sentence."""

EX7 = [
 dict(slide=7, chunks=[
  "# Run the unlocking data '2 3' against the locking script\npassing = L.run('2 3', 'OP_ADD 5 OP_EQUAL')",
  "# The same script with a six instead of a five must fail\nfailing = L.run('2 3', 'OP_ADD 6 OP_EQUAL')",
  "# Turn the five words of the script into bytes, shown as hex\nscript_hex = L.assemble('2 3 OP_ADD 5 OP_EQUAL').hex()\nresults = [passing, failing, script_hex]\nprint(results)"],
  show=[("results", "['OK', 'EVAL_FALSE', '5253935587']")]),
 dict(slide=9, chunks=[
  "# The software of 2010 joined both scripts into one program\njoined_old = old_joined('OP_1 OP_RETURN', LOCK)",
  "# Today the two scripts run apart, so the same pair fails\nrun_now = L.run('OP_1 OP_RETURN', LOCK, flags=())",
  "# The owner's real key still opens the lock\nowner_key = '0x06' + b'secret'.hex()\nowner_run = L.run(owner_key, LOCK, flags=())\nresults = [joined_old, run_now, owner_run]\nprint(results)"],
  show=[("results", "['OK', 'OP_RETURN', 'OK']")]),
 dict(slide=15, chunks=[
  "# Build the 25-byte lock from the hash of public key number 1\nlock = L.p2pkh_script(L.hash160(K.pub(1)))\nlock_facts = (len(lock), L.classify(lock)[0])",
  "# Spend with the right key, another key, and a changed amount\nright_key = p2pkh()\nwrong_key = p2pkh(signer=2)\nchanged_amount = p2pkh(amount_after=99999)\nresults = (right_key, wrong_key, changed_amount)\nprint(results)"],
  show=[("lock_facts", "(25, 'pubkeyhash')"), ("results", "('OK', 'EVAL_FALSE', 'EVAL_FALSE')")]),
 dict(slide=17, chunks=[
  "# Sign the message 'pay Bob' with secret key number 1\nsignature = L.ecdsa_sign(K.secret(1), L.sha256(b'pay Bob'))",
  "# Append the hash-type byte and look at the result\nsig_full = signature + b'\\x01'\nfacts = [len(sig_full), sig_full[0], L.is_low_s(sig_full)]",
  "# Without the strict rule a padded signature passes; with it, not\nno_strict_rule = L.MAINNET_FLAGS - {'DERSIG'}\nloose_old = p2pkh(loose=True, flags=no_strict_rule)\nloose_now = p2pkh(loose=True)\nresults = [loose_old, loose_now]\nprint(results)"],
  show=[("facts", "[72, 48, True]"), ("results", "['OK', 'SIG_DER']")]),
 dict(slide=21, chunks=[
  "# Two of three keys sign: in key order, swapped, and only one\nin_order = K.ms_spend(2, 3, [0, 2])\nswapped = K.ms_spend(2, 3, [2, 0])\ntoo_few = K.ms_spend(2, 3, [1])",
  "# The extra element in front of the signatures must be empty\nbad_dummy = K.ms_spend(2, 3, [0, 1], dummy=b'\\x01')",
  "# Collect the three verdicts\nresults = [in_order, swapped, too_few]\nprint(results)"],
  show=[("results", "['OK', 'EVAL_FALSE', 'INVALID_STACK_OPERATION']"), ("bad_dummy", "'SIG_NULLDUMMY'"), ("len(RED)", "105")]),
 dict(slide=25, chunks=[
  "# The 23-byte lock holds only the hash of the redeem script\nlock = L.p2sh_script(L.hash160(RED))\naddress = L.script_to_address(lock)",
  "# Reveal the true script, then a script that hashes differently\nrevealed = K.ms_spend(2, 3, [0, 1], wrap='p2sh')\nwrong_script = K.p2sh_spend(RED, hashed=RED + b'\\x00')",
  "# The address starts with 3; the lock is 23 bytes\nresults = [address[:6], len(lock), revealed, wrong_script]\nprint(results)"],
  show=[("results", "['3BuKam', 23, 'OK', 'EVAL_FALSE']")]),
 dict(slide=29, chunks=[
  "# A sequence below 0xffffffff keeps the lock time switched on\nnot_final = 0xfffffffe\non_time = K.key_spend(CLTV, locktime=800000,\n                      sequence=not_final)",
  "# One block too early fails\ntoo_early = K.key_spend(CLTV, locktime=799999,\n                        sequence=not_final)",
  "# A final sequence makes nodes ignore the lock time, so it fails\nfinal_sequence = K.key_spend(CLTV, locktime=800000)\nresults = [on_time, too_early, final_sequence]\nprint(results)"],
  show=[("results", "['OK', 'UNSATISFIED_LOCKTIME', 'UNSATISFIED_LOCKTIME']")]),
 dict(slide=31, chunks=[
  "# Version 2 and a sequence of 4,320 blocks: about thirty days\nwaited = K.key_spend(CSV, version=2, sequence=4320)",
  "# One block short, and the same wait with transaction version 1\ntoo_early = K.key_spend(CSV, version=2, sequence=4319)\nversion_one = K.key_spend(CSV, version=1, sequence=4320)",
  "# Setting bit 31 of the sequence switches the relative lock off\ndisabled_bit = 0x80000000 | 4320\nbit_set = K.key_spend(CSV, version=2, sequence=disabled_bit)\nprint(bit_set)"],
  show=[("waited", "'OK'"), ("too_early", "'UNSATISFIED_LOCKTIME'"), ("version_one", "'UNSATISFIED_LOCKTIME'"), ("bit_set", "'UNSATISFIED_LOCKTIME'")]),
 dict(slide=35, chunks=[
  "# The script of Mohammed's capital account, and path one\nscript_size = len(K.moh_script())\npath_one = K.moh_spend(1)",
  "# Path two: lawyer and a partner, 4,320 blocks, then one less\nwaits = (4320, 4319)\npath_two = [K.moh_spend(2, sequence=w) for w in waits]",
  "# Path three: the lawyer alone, 12,960 blocks, then 4,320\nwaits = (12960, 4320)\npath_three = [K.moh_spend(3, sequence=w) for w in waits]\nprint(path_three)"],
  show=[("script_size", "192"), ("path_one", "'OK'"), ("path_two", "['OK', 'UNSATISFIED_LOCKTIME']"), ("path_three", "['OK', 'UNSATISFIED_LOCKTIME']")]),
 dict(slide=39, chunks=[
  "# Spend a witness key-hash output directly and wrapped in P2SH\nworks = [K.wpkh_spend(), K.wpkh_spend(nested=True)]",
  "# Change the signed amount: the signature no longer matches\nwrong_amount = K.wpkh_spend(signed_amount=99999)",
  "# The 22-byte witness program and its bech32 address\nprogram = L.p2wpkh_script(L.hash160(K.pub(1)))\naddress = L.script_to_address(program)\nprint(address)"],
  show=[("works", "['OK', 'OK']"), ("wrong_amount", "'EVAL_FALSE'"), ("address", "'bc1qm5gqhe7e46jhyy2ca00x66slmrlljwa33n9fts'")]),
 dict(slide=47, chunks=[
  "# Length of the proof for each leaf of Mohammed's script tree\nproof_lengths = [len(p) for p in K.tap_tree(MOH_LEAVES)[1]]",
  "# Tree depth for 3, 8, 1,024 and about a million scripts\nleaf_counts = (3, 8, 1024, 2**20)\ndepths = [(n - 1).bit_length() for n in leaf_counts]\nprint(depths)"],
  show=[("proof_lengths", "[2, 2, 1]"), ("leaf_counts", "(3, 8, 1024, 1048576)"), ("depths", "[2, 3, 10, 20]")]),
 dict(slide=52, chunks=[
  "# Tweak key 1 with an empty script tree: the taproot output key\nparity, output_key = L.taproot_tweak_pubkey(K.xpub(1), b'')\naddress = L.script_to_address(L.p2tr_script(output_key))\nlock_facts = (address[:6], len(output_key))",
  "# Key path spend: one 64-byte signature; untweaked key fails\nverdict, witness, weight = K.tr_keypath(1)\nuntweaked = K.tr_keypath(1, MOH_LEAVES, tamper='untweaked')[0]\nresults = (verdict, len(witness[0]), weight, untweaked)\nprint(results)"],
  show=[("lock_facts", "('bc1pwd', 32)"), ("results", "('OK', 64, 308, 'SCHNORR_SIG')")]),
 dict(slide=55, chunks=[
  "# Spend each of the three leaves of the script tree\nverdicts = [moh_tap(i)[0] for i in range(3)]\ntap_weights = [moh_tap(i)[2] for i in range(3)]",
  "# The same three paths inside an ordinary witness script hash\nwsh_weights = [moh_wsh(path) for path in (1, 2, 3)]\nprint(verdicts)"],
  show=[("verdicts", "['OK', 'OK', 'OK']"), ("tap_weights", "[577, 617, 414]"), ("wsh_weights", "[585, 584, 509]")]),
 dict(slide=57, chunks=[
  "# A 2-of-3 lock written with OP_CHECKSIGADD\nscript = K.csa_script([0, 1, 2], 2)\nsizes = (len(script), len(RED))",
  "# Two signatures and one empty slot pass; one signature fails\ntwo_sigs = [b'', ('sig', 1), ('sig', 0)]\npassing = K.tr_spend([script], 0, two_sigs)[0]\none_sig = K.tr_spend([script], 0, [b'', b'', ('sig', 0)])[0]\nresults = [passing, one_sig]\nprint(results)"],
  show=[("sizes", "(104, 105)"), ("results", "['OK', 'EVAL_FALSE']")]),
 dict(slide=58, chunks=[
  "# Count the opcodes kept free for future upgrades\nreserved = sum(1 for op in range(256) if L.is_op_success(op))",
  "# In tapscript an upgrade opcode makes the script succeed\ntapscript = K.tr_spend([bytes([0x51, 152])], 0, [])[0]\n# In an old script the same opcode is disabled and fails\nold_script = L.run('OP_1 OP_LSHIFT', 'OP_1', flags=())\nresults = [reserved, tapscript, old_script]\nprint(results)"],
  show=[("results", "[87, 'OK', 'DISABLED_OPCODE']")]),
]

EX8 = [
 dict(slide=7, chunks=[
  "# One secret key, one message, and the public key that follows\nsecret_key, message = K.SK, K.MSG\npublic_key = L.pubkey_create(secret_key)\nsignature = L.ecdsa_sign(secret_key, message)",
  "# Two altered inputs: one flipped bit, and a different key\nflipped = bytes([message[0] ^ 1]) + message[1:]\nother_key = L.pubkey_create(secret_key + 1)",
  "def accepts(key, text):\n    return L.ecdsa_verify(key, text, signature)\n\nverdicts = [accepts(public_key, message),\n            accepts(public_key, flipped),\n            accepts(other_key, message)]\nprint(verdicts)"],
  show=[("verdicts", "[True, False, False]"), ("len(signature)", "70")]),
 dict(slide=9, chunks=[
  "# A remainder keeps a number inside a fixed range\nremainder = 5 % 3",
  "# Reduce the response s modulo n and modulo p, then compare\nby_n, by_p, differ = C.modulus_check()",
  "# The two moduli are different 256-bit numbers\ngap_bits = (L.P - L.N).bit_length()\nprint((by_n, by_p, differ))"],
  show=[("remainder", "2"), ("(by_n, by_p, differ)", "(True, False, True)"), ("gap_bits", "129")]),
 dict(slide=10, chunks=[
  "# Two identical transactions; then change one output amount\ntx_a, tx_b = C.make_tx(2, 2), C.make_tx(2, 2)\ntx_b.vout[1] = (1001, tx_b.vout[1][1])",
  "def digest_of(tx):\n    # the first 12 hex characters of the digest that is signed\n    return L.sighash_legacy(b'\\x51', tx, 0, 1).hex()[:12]",
  "# Same transaction, same digest; changed amount, new digest\ndigests = [digest_of(tx_a), digest_of(tx_a), digest_of(tx_b)]\nprint(digests)"],
  show=[("digests", "['18bdeda48b41', '18bdeda48b41', 'ff64b81fb946']")]),
 dict(slide=13, chunks=[
  "# The three base flags, each a single byte\nbase_flags = [L.SIGHASH_ALL, L.SIGHASH_NONE, L.SIGHASH_SINGLE]",
  "# ANYONECANPAY is one more bit added on top of a base flag\nanyone_can_pay = L.SIGHASH_ANYONECANPAY",
  "combined = [flag | anyone_can_pay for flag in base_flags]\nprint(combined)"],
  show=[("base_flags + [anyone_can_pay]", "[1, 2, 3, 128]"), ("combined", "[129, 130, 131]")]),
 dict(slide=15, chunks=[
  "# The six flags, with and without ANYONECANPAY\nflags = (1, 2, 3, 0x81, 0x82, 0x83)",
  "# For each flag, which of the five transaction parts it commits to\ncommits = {f: C.sighash_commitments(f) for f in flags}",
  "count = {hex(f): sum(commits[f].values()) for f in flags}\ncounts = list(count.values())\nprint(counts)"],
  show=[("count", "{'0x1': 5, '0x2': 2, '0x3': 3, '0x81': 3, '0x82': 1, '0x83': 2}"), ("counts", "[5, 2, 3, 3, 1, 2]"), ("[''.join('Y' if x else '.' for x in commits[f].values()) for f in flags]", "['YYYYY', 'Y...Y', 'Y.Y.Y', '..YYY', '....Y', '..Y.Y']")]),
 dict(slide=16, chunks=[
  "# A transaction with three inputs and only one output\ntx = C.make_tx(3, 1)",
  "def digest_of_input(i):\n    return L.sighash_legacy(b'\\x51', tx, i, 3).hex()\n\ndigests = [digest_of_input(i)[:8] for i in range(3)]",
  "# Inputs 1 and 2 have no matching output: the digest is just 1\nis_the_bug = [d == '01000000' for d in digests]\nprint(is_the_bug)"],
  show=[("digests", "['11a21de8', '01000000', '01000000']"), ("is_the_bug", "[False, True, True]")]),
 dict(slide=19, chunks=[
  "# A toy run with small whole numbers: secret 3, generator 5\ntoy = C.toy_protocol(x=3, G_=5, k=7, e=11)",
  "# The response, and the check that the verifier performs\nresponse, holds = toy['s'], toy['holds']",
  "# Dividing the public number by the generator leaks the secret\nleaked_key = toy['xG'] // 5\nprint(leaked_key)"],
  show=[("toy", "{'xG': 15, 'kG': 35, 's': 40, 'sG': 200, 'exG': 165, 'holds': True, 'd"), ("(response, holds)", "(40, True)"), ("leaked_key", "3")]),
 dict(slide=21, chunks=[
  "# Secret x, nonce k and challenge e (toy values) and their points\nx, k, e = 1234567, 7654321, 99999\npoint_mul, point_add = L.point_mul, L.point_add\nX, R = point_mul(x), point_mul(k)",
  "# Response s = k + e*x; the verifier checks s*G == R + e*X\ns = (k + e * x) % L.N\n\ndef holds(t):\n    return point_mul(t) == point_add(R, point_mul(e, X))\n\nproof = [holds(s), holds(s + 1)]",
  "# Fiat-Shamir: the message replaces the verifier's challenge\nsig = C.fs_sign(x, b'A', k)\nsigs = [C.fs_verify(X, m, sig) for m in (b'A', b'B')]\nprint(sigs)"],
  show=[("proof", "[True, False]"), ("sigs", "[True, False]")]),
 dict(slide=24, chunks=[
  "# A secret key and a message\nsk = 0x3b78ce563f89a0ed9414f5aa28ad0d96d6795f9c63\nmessage = L.sha256(b'ch08')",
  "# BIP340: an x-only public key and a 64-byte signature\nx_only_key = L.schnorr_pubkey(sk)\nschnorr_sig = L.schnorr_sign(sk, message)\n# The ECDSA equivalents, for comparison\ncompressed_key = L.pubkey_create(sk)\necdsa_sig = L.ecdsa_sign(sk, message)",
  "valid = L.schnorr_verify(x_only_key, message, schnorr_sig)\nsizes = [len(compressed_key), len(x_only_key),\n         len(ecdsa_sig), len(schnorr_sig)]\nprint(sizes)"],
  show=[("sizes", "[33, 32, 71, 64]"), ("valid", "True")]),
 dict(slide=26, chunks=[
  "# An attacker picks a key that cancels the victims' keys\nnaive_result = C.key_cancellation(5, 7, 3, b'pay')",
  "# The same attempt against MuSig2\nmusig_result = C.musig2_cancellation_attempt()\nprint((naive_result, musig_result))"],
  show=[("naive_result", "(True, True)"), ("musig_result", "False"), ("(naive_result, musig_result)", "((True, True), False)")]),
 dict(slide=27, chunks=[
  "from itertools import combinations\n\n# Split the secret 31337 into three shares; any two recover it\nshares = C.shamir_split(31337, 2, [1, 2, 3], [77])",
  "# Combine every pair of shares\npairs = combinations(shares, 2)\nrecovered = [C.shamir_combine(pair) for pair in pairs]",
  "# One share alone tells nothing about the secret\nalone = C.shamir_combine(shares[:1])\nprint(recovered)"],
  show=[("shares", "[(1, 31414), (2, 31491), (3, 31568)]"), ("recovered", "[31337, 31337, 31337]"), ("alone", "31414")]),
 dict(slide=30, chunks=[
  "# A toy key x, a message hash h and a nonce k\nx, h, k = 0x1234, 0x5678, 0x9abc\nR, s = C.ecdsa_sign_k(x, h, k)\nX = L.point_mul(x)",
  "def verifies(t):\n    return C.ecdsa_verify_K(X, h, R, t)",
  "# Both s and n - s verify; only the low one is standard\nboth = [verifies(s), verifies(L.N - s)]\nlowform = s <= L.N - s\nprint(both)"],
  show=[("both", "[True, True]"), ("lowform", "False"), ("hex(s)[:14]", "'0xd312ba095ee4'"), ("hex(L.N - s)[:14]", "'0x2ced45f6a11b'")]),
 dict(slide=32, chunks=[
  "# A real signature with its hash-type byte\nsignature = L.ecdsa_sign(K.SK, K.MSG) + b'\\x01'",
  "# Cut it into its DER fields and count the bytes of each\nfields = C.der_fields(signature)\nrows = [(name, len(value) // 2) for name, value in fields]",
  "total = sum(size for name, size in rows)\nprint(total)"],
  show=[("[size for name, size in rows]", "[1, 1, 1, 1, 32, 1, 1, 32, 1]"), ("total", "71"), ("C.der_strict_ok(signature)", "True")]),
 dict(slide=34, chunks=[
  "# A signature and its twin with s replaced by n - s\nsignature = L.ecdsa_sign(K.SK, K.MSG)\nr, s = L.der_parse_lax(signature)[:2]\ntwin = L.der_encode(r, L.N - s)",
  "pk = L.pubkey_create(K.SK)\n\ndef is_valid(sig):\n    return L.ecdsa_verify(pk, K.MSG, sig)\n\ndef is_low_s(sig):\n    return L.is_low_s(sig + b'\\x01')",
  "# Both are valid; only the low-s form passes the relay policy\nverdict = [(is_valid(g), is_low_s(g)) for g in (signature, twin)]\nprint(verdict)"],
  show=[("verdict", "[(True, True), (True, False)]")]),
 dict(slide=38, chunks=[
  "# Two different messages signed with the same nonce k\nx, k, h1, h2 = 1234567, 7654321, 111, 222\nr, s1 = C.ecdsa_sign_k(x, h1, k)\nr2, s2 = C.ecdsa_sign_k(x, h2, k)",
  "# Anyone can solve the two equations for the private key\ngot, k2 = C.recover_key_from_reused_nonce(r, s1, h1, s2, h2)",
  "# A fresh nonce gives a different r\nfresh = C.ecdsa_sign_k(x, h2, k + 1)[0] != r\nprint(got == x)"],
  show=[("r == r2", "True"), ("got == x", "True"), ("k2 == k", "True"), ("fresh", "True")]),
 dict(slide=40, chunks=[
  "# RFC 6979 derives the nonce from the key and the message\nh = L.sha256(b'sample')\nk1 = C.rfc6979_k(L.N, K.SK, h)",
  "# Another message gives another nonce\nk2 = C.rfc6979_k(L.N, K.SK, L.sha256(b'other'))",
  "# Repeating the derivation repeats the nonce and the signature\nagain = C.rfc6979_k(L.N, K.SK, h) == k1\nsame = L.ecdsa_sign(K.SK, h) == L.ecdsa_sign(K.SK, h)\nprint(again)"],
  show=[("again", "True"), ("k1 != k2", "True"), ("same", "True"), ("hex(k1)[:14]", "'0x1f8bce02bda8'"), ("hex(k2)[:14]", "'0x80fb94370ee8'")]),
 dict(slide=41, chunks=[
  "from collections import Counter\n\n# Sign 200 different messages with one key\nmessages = [L.sha256(b'm%d' % i) for i in range(200)]",
  "# Collect the length of every signature\nlengths = [len(L.ecdsa_sign(K.SK, m)) for m in messages]",
  "# Half are 70 bytes, half are 71 bytes\ncounts = dict(sorted(Counter(lengths).items()))\nprint(counts)"],
  show=[("counts", "{70: 100, 71: 100}")]),
 dict(slide=44, chunks=[
  "# Transactions with 1, 10, 100 and 1,000 inputs\nns = [1, 10, 100, 1000]\ntxs = [C.make_tx(n, 1) for n in ns]",
  "# Bytes hashed by the old and by the BIP143 method\nold = [C.legacy_bytes_hashed(t) for t in txs]\nnew = [C.bip143_bytes_hashed(t) for t in txs]",
  "# How many times more the old method hashes\nratio = [round(a / b, 1) for a, b in zip(old, new)]\nprint(ratio)"],
  show=[("ns", "[1, 10, 100, 1000]"), ("old", "[146, 5150, 420500, 41107000]"), ("new", "[384, 2670, 25530, 254130]"), ("ratio", "[0.4, 1.9, 16.5, 161.8]")]),
 dict(slide=45, chunks=[
  "# One input and a key-hash script that stays the same\ntx = C.make_tx(1, 1)\nscript = b'\\x76\\xa9\\x14' + b'\\x22' * 20 + b'\\x88\\xac'",
  "def digest_for_amount(amount):\n    return L.sighash_v0(script, tx, 0, 1, amount).hex()[:12]",
  "# The amount is part of the digest: 5001 gives a new digest\nds = [digest_for_amount(5000), digest_for_amount(5000),\n      digest_for_amount(5001)]\nlegacy = L.sighash_legacy(script, tx, 0, 1).hex()[:12]\nprint(ds)"],
  show=[("ds", "['3d02f61132ca', '3d02f61132ca', '89c355aa699d']"), ("legacy", "'0d29c866d5f0'")]),
 dict(slide=47, chunks=[
  "from datetime import date\n\n# Schnorr's patent: filed in 1990, granted in 1991\nfiled, grant = date(1990, 2, 23), date(1991, 2, 19)",
  "# The term: the longer of 17 years from grant, 20 from filing\nt17 = grant.replace(year=grant.year + 17)\nt20 = filed.replace(year=filed.year + 20)\nterm_end = max(t17, t20)",
  "# Days from Bitcoin's first block to the taproot activation\ndays = (date(2021, 11, 14) - date(2009, 1, 3)).days\nprint(term_end)"],
  show=[("str(t17)", "'2008-02-19'"), ("str(t20)", "'2010-02-23'"), ("str(term_end)", "'2010-02-23'"), ("term_end", "datetime.date(2010, 2, 23)"), ("days", "4698")]),
]

# Explanations under the code boxes where the number of boxes changed against the old slide (all others keep the old sentence of the same box).
SAYS = {
 (7, 52): ["The output key is the internal key plus a tweak; here there is no script. The address begins with bc1p.",
           "One 64-byte signature spends it; an untweaked key is refused."],
 (7, 55): ["Each of the three leaves of the account script can be spent; the weight of each spend is counted.",
           "The same three paths as an ordinary witness script hash spend, for comparison."],
 (7, 57): ["The same 2-of-3 rule written with CHECKSIGADD is a byte shorter.",
           "Two valid signatures and one empty slot satisfy it; with only one, the count stays below two and the script fails."],
 (7, 58): ["In tapscript, 87 opcode values succeed on sight.",
           "A tapscript with opcode 152 succeeds at once; the same word, a disabled shift, fails in an old script."],
 (8, 13): ["Bitcoin knows three base flags, each a small number.",
           "The modifier is a single high bit, so it combines with any base flag.",
           "Adding the modifier to each base flag gives 129, 130 and 131."],
 (8, 26): ["Bob waits for Alice's public key, then publishes his own key minus hers; against the naive sum he alone signs for both.",
           "MuSig2 weights every key by a hash of all keys, and the same attack fails."],
}
