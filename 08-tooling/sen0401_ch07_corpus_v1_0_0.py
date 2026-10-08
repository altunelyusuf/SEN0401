#!/usr/bin/env python3
"""SEN0401 chapter 7 corpus, version 1.0.0: Authorization and Authentication (chapter 7 of Mastering Bitcoin, 3rd edition), each concept
explained in four to six paragraphs of continuous prose (what it is, why it matters, where it is seen, how it works, what to watch for)
and each group and branch in three to six, plus the concepts the explanations rely on, so that no term is used unexplained. The facet
name at the start of a paragraph is only the author's writing guide and is never printed.

Used by sen0401_chapter_build_v1_0_1.py (TBox/ABox/document). This is the chapter's first ontology. The text is assembled from
sen0401_ch07_text_a..i_v1_0_0.py and the shared parts in sen0401_ch07_common_v1_0_0.py; the executed claims use
sen0401_ch07_checklib_v1_0_0.py (source readers and spend builders) and sen0401_ch07_script_lib_v1_0_0.py (a Bitcoin Script
interpreter in the standard library, checked against Bitcoin Core's own test data by sen0401_ch07_verify_v1_0_0.py).

Sources actually read for this version, in this session, and saved in 08-tooling/ch07-evidence (every saved copy is re-read by a
CHECKS entry): the chapter's source (ch07_authorization-authentication.adoc of the bitcoinbook working copy at commit 275c4eb8, the
commit the textbook ontology pins) and, in the same book, chapters 4, 6, 8 and 9 and the glossary; BIPs 11, 13, 16, 32, 65, 66, 68, 86,
112, 114, 116, 141, 143, 146, 147, 173, 327, 340, 341, 342, 350 and 379 (bitcoin/bips); Bitcoin Core's sources at commit 05bc2f5
(interpreter.cpp and .h, script.cpp and .h, script_error.h, solver.cpp, sign.cpp, descriptor.cpp, policy.cpp and .h, consensus.h,
params.h, tx_verify.cpp, transaction.h, pubkey.cpp, chainparams.cpp), its doc/bips.md and its test data (script_tests.json,
sighash.json, bip341_wallet_vectors.json); the sources of Bitcoin 0.3.0 and 0.3.7; the Bitcoin Wiki entry for CVE-2010-5141; and,
because no Bitcoin Core node is available in this environment, the raw bytes and explorer records of the first 599 non-coinbase
transactions of block 775,072 and of three landmark transactions, and the six activation blocks, all from mempool.space fetched on
2026-10-08. Every number, identifier, encoding or error quoted is executed in CHECKS or in a worked example by the chapter builder
(python 3.14), the spends by the chapter's own interpreter; quotations are re-read from the saved copies by a CHECKS entry.
"""
__version__ = "1.0.0"
import sen0401_ch07_text_a_v1_0_0 as A
import sen0401_ch07_text_b_v1_0_0 as B
import sen0401_ch07_text_c_v1_0_0 as C
import sen0401_ch07_text_d_v1_0_0 as D
import sen0401_ch07_text_e_v1_0_0 as E
import sen0401_ch07_text_f_v1_0_0 as F
import sen0401_ch07_text_g_v1_0_0 as G
import sen0401_ch07_text_h_v1_0_0 as H
import sen0401_ch07_text_i_v1_0_0 as I
from sen0401_ch07_common_v1_0_0 import PROG, _SL, X, Qb, Qe

SL = _SL

CHAPTER = "07"
NODES = A.NODES_A + B.NODES_B + C.NODES_C + D.NODES_D + E.NODES_E + F.NODES_F + G.NODES_G + H.NODES_H + I.NODES_I
# the facts of the three stories (sen0401_ch07_stories_v1_0_0.py), re-read from the saved sources
CHECKS_S = [
 X("(lambda t: [k in t for k in ('950 of the last 1,000', 'roughly half the network hash rate was mining without fully validating blocks (called SPV mining)', '4 July @ 02:10 03:50 6 0', '5 July @ 21:50 23:40 3', 'wait an additional 30 confirmations', 'Bitcoin Core 0.9.5 or later users are unaffected')])(C.html_text('bitcoinorg_alert_2015_07_04_spv_mining_v1_0_0.html'))", [True] * 6),
 Qe('bitcoinwiki_common_vulnerabilities_v1_0_0.txt', 'CVE-2010-5141 2010-07-28 wxBitcoin and bitcoind Theft [ 4 ] Easy OP_RETURN could be used to spend any output.', 'One exploited a bug in the transaction handling code and allowed an attacker to spend coins that they did not own. This was never exploited on the main network, and was fixed by Bitcoin version 0.3.5.', 'many currently-unused script words were disabled for safety'),
 X("(L.OP['OP_LSHIFT'], L.is_op_success(L.OP['OP_LSHIFT']))", (152, True)),
 Qb('ch08_signatures.adoc', 'Claus Schnorr patented the algorithm he discovered and', 'prevented its use in open standards and open source software for almost two decades.', 'until the activation of the', 'taproot soft fork in 2021.'),
 X("[(b['height'], b['tx_count'], __import__('datetime').datetime.fromtimestamp(b['timestamp'], __import__('datetime').UTC).strftime('%Y-%m-%d %H:%M:%S')) for b in C.ev_json('mainnet_activation_blocks_v1_0_0.json')['blocks'] if b['height'] in (363725, 709632)]", [(363725, 1, "2015-07-04 01:54:32"), (709632, 2043, "2021-11-14 05:15:27")]),
]
CHECKS = (A.CHECKS_A + B.CHECKS_B + C.CHECKS_C + D.CHECKS_D + E.CHECKS_E + F.CHECKS_F + G.CHECKS_G + H.CHECKS_H + I.CHECKS_I + CHECKS_S)

# claims that something fails (executed by the chapter builder)
RAISES = [
 ("bytes.fromhex('5g')", "ValueError"),
 ("int('', 16)", "ValueError"),
 ("pow(0, -1, 7)", "ValueError"),
 ("(lambda L: L.assemble('OP_BOGUS'))(%s)" % SL(), "ValueError"),
 ("(lambda L: L.cs_encode(2 ** 64))(%s)" % SL(), "AssertionError"),
 ("(lambda L: L.multisig_script(21, [b'\\x02' * 33] * 21))(%s)" % SL(), "AssertionError"),
 ("(lambda L: L.multisig_script(3, [b'\\x02' * 33] * 2))(%s)" % SL(), "AssertionError"),
 ("(lambda L: L.parse_tx('00'))(%s)" % SL(), "error"),
 ("(lambda L: L.tap_leaf_hash(0xc0, b'')[40])(%s)" % SL(), "IndexError"),
 ("'qpzry9x8gf2tvdw0s3jn54khce6mua7l'.index('b')", "ValueError"),
 ("(2 ** 63).to_bytes(8, 'little', signed=True)", "OverflowError"),
 ("bytes(32)[32]", "IndexError"),
]

# a concept that is part of, or operates on, another concept of this chapter
OWNERS = [("PublicKeyHash", "PayToPublicKeyHash"), ("OpChecksig", "PayToPublicKey"), ("SignatureEncoding", "OpChecksig"),
          ("SignatureHash", "OpChecksig"), ("CheckmultisigDummy", "ScriptedMultisignature"), ("SignatureCheckCount", "ScriptedMultisignature"),
          ("MultisigLimits", "ScriptedMultisignature"), ("RedeemScript", "PayToScriptHashOutput"), ("P2shAddress", "PayToScriptHashOutput"),
          ("P2shRules", "PayToScriptHashOutput"), ("DataCarrierPolicy", "OpReturnOutput"), ("LockTimeLimits", "CheckLockTimeVerify"),
          ("RelativeTimelock", "CheckSequenceVerify"), ("VerifyGuard", "ConditionalClauses"), ("MultiPathScript", "ConditionalClauses"),
          ("P2wpkh", "WitnessProgram"), ("P2wsh", "WitnessProgram"), ("SegwitAddress", "WitnessProgram"), ("WitnessSighash", "BackwardCompatibleUpgrade"),
          ("NestedSegwit", "BackwardCompatibleUpgrade"), ("MastVersusAst", "Mast"), ("ThresholdSignature", "ScriptlessMultisignature"),
          ("KeyPathSpending", "Taproot"), ("ScriptPathSpending", "Taproot"), ("ControlBlock", "ScriptPathSpending"),
          ("ChecksigAdd", "TapscriptChanges"), ("OpSuccess", "TapscriptChanges"), ("StackExecution", "Script"), ("ScriptLimits", "Script"),
          ("InputScript", "SeparateExecution"), ("OutputScript", "SeparateExecution")]

# an error condition of a concept: the expression, the error class and the start of its message, all executed. The page offers these
# programs as repair exercises in the reader's browser, so each one is self-contained: standard library only, no file access and no
# local module.
_E_LIM = PROG("script = bytes(10001)\n"
              "assert len(script) <= 10000, 'a script is at most 10,000 bytes'\n"
              "result = len(script)")
_E_DER = PROG("sig = bytes.fromhex('3145022100aa0220bb01')\n"
              "assert sig[0] == 0x30, 'a DER signature starts with the byte 0x30'\n"
              "result = sig[0]")
_E_KH = PROG("import hashlib\n"
             "key_hash = hashlib.sha256(b'a public key').digest()          # 32 bytes: SHA-256 alone, not HASH160\n"
             "assert len(key_hash) == 20, 'a public key hash is 20 bytes'\n"
             "result = key_hash.hex()")
_E_MS = PROG("keys = 21\n"
             "assert 1 <= keys <= 20, 'a multisignature holds at most 20 keys'\n"
             "result = keys")
_E_CLTV = PROG("lock = -5\n"
               "assert lock >= 0, 'a lock time is not negative'\n"
               "result = lock")
_E_CSV = PROG("blocks = 65536\n"
              "assert blocks <= 0xffff, 'a relative timelock holds at most 65535 blocks'\n"
              "result = blocks & 0xffff")
_E_P2SH = PROG("redeem_script = bytes(521)\n"
               "assert len(redeem_script) <= 520, 'a redeem script is one push of at most 520 bytes'\n"
               "result = len(redeem_script)")
_E_WP = PROG("program = bytes(19)\n"
             "assert len(program) in (20, 32), 'a version 0 witness program is 20 or 32 bytes'\n"
             "result = len(program)")
_E_TR = PROG("internal_key = bytes(33)          # a compressed key still has its prefix byte\n"
             "assert len(internal_key) == 32, 'an internal key is 32 bytes, the x coordinate only'\n"
             "result = internal_key.hex()")
_E_CB = PROG("control = bytes(34)\n"
             "assert 33 <= len(control) <= 4129 and (len(control) - 33) % 32 == 0, 'a control block is 33 bytes plus 32 for each level'\n"
             "result = len(control)")
_E_KP = PROG("witness = [bytes(63)]\n"
             "assert len(witness) == 1 and len(witness[0]) in (64, 65), 'a key path witness is one signature of 64 or 65 bytes'\n"
             "result = len(witness[0])")
_E_MAST = PROG("proof = [bytes(32)] * 129\n"
               "assert len(proof) <= 128, 'a script path has at most 128 hashes'\n"
               "result = len(proof)")
ERRORS = [("Script", "bytes.fromhex('5g') raises ValueError: non-hexadecimal number found in fromhex() arg"),
          ("ScriptLimits", _E_LIM + " raises AssertionError: a script is at most 10,000 bytes"),
          ("SignatureEncoding", _E_DER + " raises AssertionError: a DER signature starts with the byte 0x30"),
          ("PublicKeyHash", _E_KH + " raises AssertionError: a public key hash is 20 bytes"),
          ("MultisigLimits", _E_MS + " raises AssertionError: a multisignature holds at most 20 keys"),
          ("CheckLockTimeVerify", _E_CLTV + " raises AssertionError: a lock time is not negative"),
          ("RelativeTimelock", _E_CSV + " raises AssertionError: a relative timelock holds at most 65535 blocks"),
          ("RedeemScript", _E_P2SH + " raises AssertionError: a redeem script is one push of at most 520 bytes"),
          ("WitnessProgram", _E_WP + " raises AssertionError: a version 0 witness program is 20 or 32 bytes"),
          ("SegwitAddress", "'qpzry9x8gf2tvdw0s3jn54khce6mua7l'.index('b') raises ValueError: substring not found"),
          ("Taproot", _E_TR + " raises AssertionError: an internal key is 32 bytes, the x coordinate only"),
          ("ControlBlock", _E_CB + " raises AssertionError: a control block is 33 bytes plus 32 for each level"),
          ("KeyPathSpending", _E_KP + " raises AssertionError: a key path witness is one signature of 64 or 65 bytes"),
          ("Mast", _E_MAST + " raises AssertionError: a script path has at most 128 hashes"),
          ("ThresholdSignature", "pow(0, -1, 7) raises ValueError: base is not invertible for the given modulus")]

CQS = ["What does a Bitcoin output ask of its spender, and how do the input script and the output script together decide whether a spend is authorized?",
       "How does a script run on a stack, why is the language deliberately not Turing complete, and why can every node verify a spend without knowing anything but the transaction and the outputs it spends?",
       "How do pay to public key hash, scripted multisignatures and pay to script hash move the cost of a complicated condition from the payer to the spender, and what does the signature check count?",
       "How do lock time, OP_CHECKLOCKTIMEVERIFY, the sequence field and OP_CHECKSEQUENCEVERIFY make a spend wait, and where do the book and Bitcoin Core's rules differ by one block?",
       "How does segregated witness fix signature malleability and add a version byte for later upgrades, and what do P2WPKH, P2WSH and the nested forms look like on the chain?",
       "How do a script tree, a tweaked key and a scriptless multisignature combine into taproot, and what does a key path spend or a script path spend reveal?",
       "What does tapscript change in the language, and which statements of the book differ from the BIPs and from Bitcoin Core's sources?"]

PROVENANCE = ("Concepts are corpus-derived from the 3rd edition's chapter 7 through the Stage 1 research record: the chapter's own sections and named terms "
              "first, then the standards it cites (BIP11, BIP13, BIP16, BIP65, BIP66, BIP68, BIP86, BIP112, BIP114, BIP116, BIP141, BIP143, BIP146, BIP147, BIP173, "
              "BIP327, BIP340, BIP341, BIP342, BIP350 and BIP379), Bitcoin Core's script, policy and consensus sources at commit 05bc2f5 with its list of "
              "implemented proposals and its script and signature-hash test data, the first interpreter of Bitcoin 0.3.0 and its repair, and the raw bytes "
              "and explorer records of 599 transactions of block 775,072 fetched from mempool.space on 2026-10-08; the supporting concepts (the stack, the "
              "truth of a script, the key hash, the DER encoding, the signature check count and the witness program) were added because an audit of the "
              "explanations found them used without a concept of their own.")
TOOLING = "CPython 3.14.6"
DOC_TITLE = "Authorization and authentication: chapter 7 of the 3rd edition run through a Bitcoin Script interpreter and checked against the standards and Bitcoin Core's tests"
DOC_ABOUT = "This document renews chapter 7 of the 3rd edition by running every script, signature check, timelock, multisignature, segregated witness and taproot spend it describes through a Bitcoin Script interpreter written with the standard library, validated against Bitcoin Core's own test data and against 1,022 inputs of a mainnet block, and by comparing the chapter's statements with the BIPs and with Bitcoin Core's sources at a pinned commit."
CHANGE = ("1.0.0 is the first ontology of chapter 7: %d concepts in nine branches, each level 3 concept explained in four to six paragraphs of continuous prose and "
          "each level 1 or 2 group in three or four, with the terms the explanations rely on added as concepts of their own so that nothing is used unexplained; "
          "every quoted number, identifier, encoding, spend and error is executed by the chapter builder, and every quotation is re-read from a saved copy of its "
          "source by an executed claim.") % len(NODES)


def run_checks_inprocess():
    bad = []
    n = 0

    def ev(e):
        return repr(eval(e, {}))
    for e, x in CHECKS:
        n += 1
        try:
            got = ev(e)
        except BaseException as ex:
            got = "EXC %r" % (ex,)
        if got != x:
            bad.append((e[:160], x, got))
    for nd in NODES:
        if nd[4] and nd[4][2]:
            n += 1
            e, x = nd[4][2]
            try:
                got = ev(e)
            except BaseException as ex:
                got = "EXC %r" % (ex,)
            if got != x:
                bad.append((nd[0], x, got))
    for e, typ in RAISES:
        n += 1
        try:
            eval(e, {})
            bad.append((e[:120], typ, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != typ:
                bad.append((e[:120], typ, type(ex).__name__))
    for leaf, text in ERRORS:
        n += 1
        e, rest = text.split(" raises ", 1)
        et, msg = rest.split(": ", 1) if ": " in rest else (rest, "")
        try:
            eval(e, {})
            bad.append((leaf, et, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != et or not str(ex).startswith(msg):
                bad.append((leaf, rest, "%s: %s" % (type(ex).__name__, ex)))
    return n, bad


if __name__ == "__main__":
    import sys
    n, bad = run_checks_inprocess()
    print(n, "claims executed under CPython", sys.version.split()[0], "- failures:", bad)
    ids = [x[0] for x in NODES]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    byid = {x[0]: x for x in NODES}
    for x in NODES:
        assert x[3] is None or x[3] in byid, x[0]
        assert (x[2] == 3) == (x[4] is not None), x[0]
        if x[3]:
            assert byid[x[3]][2] == x[2] - 1 and ids.index(x[3]) < ids.index(x[0]), x[0]
        assert (x[2] == 3 and 4 <= len(x[5]) <= 6) or (x[2] < 3 and 3 <= len(x[5]) <= 6), (x[0], len(x[5]))
        for f, t in x[5]:
            assert "[" not in t or "[" in t.replace("[0]", ""), (x[0], t[:80])
    for leaf, owner in OWNERS:
        assert leaf in byid and owner in byid and byid[leaf][2] == 3 and byid[owner][2] == 3, (leaf, owner)
    for leaf, t in ERRORS:
        assert leaf in byid and byid[leaf][2] == 3, leaf
    tops = [x[0] for x in NODES if x[2] == 1]
    assert 6 <= len(tops) <= 9, tops
    print(len(NODES), "concepts;", len(tops), "branches;", sum(1 for x in NODES if x[2] == 2), "groups;",
          sum(1 for x in NODES if x[2] == 3), "concept sections;", sum(len(x[5]) for x in NODES), "paragraphs;",
          sum(len(t.split()) for x in NODES for f, t in x[5]), "words;", len(CHECKS) + len(RAISES) + len(ERRORS), "checks;",
          sum(1 for x in NODES if x[4] and x[4][2]), "worked examples")
    print("branches:", ", ".join(tops))
