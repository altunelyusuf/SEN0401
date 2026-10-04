#!/usr/bin/env python3
"""Shared parts of the SEN0401 chapter 5 corpus (version 1.0.0): the writing-guide facets, the citation markers, the source list (one entry per source
read; the research record is generated from it) and the builders of the executed claims. Used by sen0401_ch05_text_*_v1_0_0.py and
sen0401_ch05_corpus_v1_0_0.py. Python standard library only."""
__version__ = "1.0.0"
import os
HERE = os.path.dirname(os.path.abspath(__file__))
W, Y, E, H, K = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out"

GH = "https://raw.githubusercontent.com/"
CORE_C = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
# (marker, author-year string, label of the publication, url, role, local file under ch05-evidence / description, one cites per marker)
# the research record gets one publication per source file read; markers of the same author-year share the string.
SOURCES = [
 ("AH", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Chapter 5, Wallet Recovery (Antonopoulos and Harding, 2023; O'Reilly; CC BY-SA 4.0; tag third_edition_print1)", GH + "bitcoinbook/bitcoinbook/third_edition_print1/ch05_wallets.adoc", "primary", "book:ch05_wallets.adoc"),
 ("AH14", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Chapter 14, Bitcoin Applications, the section on routed payment channels (Antonopoulos and Harding, 2023)", GH + "bitcoinbook/bitcoinbook/third_edition_print1/ch14_applications.adoc", "secondary", "book:ch14_applications.adoc"),
 ("AH7", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Chapter 7, Authorization and Authentication, the section on multisignature (Antonopoulos and Harding, 2023)", GH + "bitcoinbook/bitcoinbook/third_edition_print1/ch07_authorization-authentication.adoc", "secondary", "book:ch07_authorization-authentication.adoc"),
 ("AHG", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Glossary (Antonopoulos and Harding, 2023)", GH + "bitcoinbook/bitcoinbook/third_edition_print1/glossary.asciidoc", "secondary", "book:glossary.asciidoc"),
 ("B32", "Wuille, 2012", "BIP32, Hierarchical Deterministic Wallets, the BIPs repository (Wuille, 2012), status Deployed", GH + "bitcoin/bips/master/bip-0032.mediawiki", "secondary", "ev:bip-0032.mediawiki"),
 ("B39", "Palatinus et al., 2013", "BIP39, Mnemonic code for generating deterministic keys, and its English word list, the BIPs repository (Palatinus et al., 2013), status Deployed", GH + "bitcoin/bips/master/bip-0039.mediawiki", "secondary", "ev:bip-0039.mediawiki"),
 ("B43", "Palatinus and Rusnak, 2014a", "BIP43, Purpose Field for Deterministic Wallets, the BIPs repository (Palatinus and Rusnak, 2014a), status Deployed", GH + "bitcoin/bips/master/bip-0043.mediawiki", "secondary", "ev:bip-0043.mediawiki"),
 ("B44", "Palatinus and Rusnak, 2014b", "BIP44, Multi-Account Hierarchy for Deterministic Wallets, the BIPs repository (Palatinus and Rusnak, 2014b), status Deployed", GH + "bitcoin/bips/master/bip-0044.mediawiki", "secondary", "ev:bip-0044.mediawiki"),
 ("B49", "Weigl, 2016", "BIP49, Derivation scheme for P2WPKH-nested-in-P2SH based accounts, the BIPs repository (Weigl, 2016), status Deployed", GH + "bitcoin/bips/master/bip-0049.mediawiki", "secondary", "ev:bip-0049.mediawiki"),
 ("B84", "Rusnak, 2017", "BIP84, Derivation scheme for P2WPKH based accounts, the BIPs repository (Rusnak, 2017), status Deployed", GH + "bitcoin/bips/master/bip-0084.mediawiki", "secondary", "ev:bip-0084.mediawiki"),
 ("B86", "Chow, 2021", "BIP86, Key Derivation for Single Key P2TR Outputs, the BIPs repository (Chow, 2021), status Deployed", GH + "bitcoin/bips/master/bip-0086.mediawiki", "secondary", "ev:bip-0086.mediawiki"),
 ("B93", "Olsson Curr et al., 2023", "BIP93, codex32: Checksummed SSSS-aware BIP32 seeds, the BIPs repository (Olsson Curr et al., 2023), status Draft", GH + "bitcoin/bips/master/bip-0093.mediawiki", "secondary", "ev:bip-0093.mediawiki"),
 ("B329", "Raw, 2022", "BIP329, Wallet Labels Export Format, the BIPs repository (Raw, 2022), status Draft", GH + "bitcoin/bips/master/bip-0329.mediawiki", "secondary", "ev:bip-0329.mediawiki"),
 ("B380", "Wuille and Chow, 2021", "BIP380 to BIP386, Output Script Descriptors: general operation and the script expressions, the BIPs repository (Wuille and Chow, 2021), status Deployed", GH + "bitcoin/bips/master/bip-0380.mediawiki", "secondary", "ev:bip-0380.mediawiki"),
 ("B389", "Chow, 2022", "BIP389, Multipath Descriptor Key Expressions, the BIPs repository (Chow, 2022), status Draft", GH + "bitcoin/bips/master/bip-0389.mediawiki", "secondary", "ev:bip-0389.mediawiki"),
 ("B379", "Wuille et al., 2023", "BIP379, Miniscript, the BIPs repository (Wuille et al., 2023), status Draft", GH + "bitcoin/bips/master/bip-0379.md", "secondary", "ev:bip-0379.md"),
 ("S39", "Rusnak et al., 2017", "SLIP-0039, Shamir's Secret-Sharing for Mnemonic Codes, SatoshiLabs Improvement Proposals (Rusnak et al., 2017), status Final", GH + "satoshilabs/slips/master/slip-0039.md", "secondary", "ev:slip-0039.md"),
 ("S44", "Rusnak and Palatinus, 2014", "SLIP-0044, Registered coin types for BIP-0044, SatoshiLabs Improvement Proposals (Rusnak and Palatinus, 2014)", GH + "satoshilabs/slips/master/slip-0044.md", "secondary", "ev:slip-0044.md"),
 ("EL", "Electrum Technologies, 2026", "Electrum documentation: the Seed Version System of Electrum 2.0 and higher (Electrum Technologies, 2026)", GH + "spesmilo/electrum-docs/master/seedphrase.rst", "secondary", "ev:electrum_seeds.rst"),
 ("AZ", "Lightning Labs, 2026a", "lnd: the aezeed cipher seed scheme, aezeed/README.md (Lightning Labs, 2026a)", GH + "lightningnetwork/lnd/master/aezeed/README.md", "secondary", "ev:aezeed_README.md"),
 ("LR", "Lightning Labs, 2026b", "lnd: Recovering Funds From lnd, docs/recovery.md (Lightning Labs, 2026b)", GH + "lightningnetwork/lnd/master/docs/recovery.md", "secondary", "ev:lnd_recovery.md"),
 ("MU", "Muun, 2026", "Muun recovery tool, README.md (Muun, 2026)", GH + "muun/recovery/master/README.md", "secondary", "ev:muun_recovery_README.md"),
 ("LO", "Lopp, 2026", "Known Physical Bitcoin Attacks, README.md of the list kept by Jameson Lopp (Lopp, 2026)", GH + "jlopp/physical-bitcoin-attacks/master/README.md", "secondary", "ev:lopp_attacks.md"),
 ("TZ", "Trezor, 2026", "python-mnemonic: the BIP39 test vectors, vectors.json (Trezor, 2026)", GH + "trezor/python-mnemonic/master/vectors.json", "secondary", "ev:trezor_vectors.json"),
 ("BP", "BTCPay Server contributors, 2026", "BTCPay Server, README.md (BTCPay Server contributors, 2026)", GH + "btcpayserver/btcpayserver/master/README.md", "secondary", "ev:btcpayserver_README.md"),
 ("R2104", "Krawczyk et al., 1997", "RFC 2104, HMAC: Keyed-Hashing for Message Authentication (Krawczyk et al., 1997)", "https://www.rfc-editor.org/rfc/rfc2104", "secondary", "ev:rfc2104.txt"),
 ("R8018", "Moriarty et al., 2017", "RFC 8018, PKCS #5: Password-Based Cryptography Specification Version 2.1 (Moriarty et al., 2017)", "https://www.rfc-editor.org/rfc/rfc8018", "secondary", "ev:rfc8018.txt"),
 ("R7914", "Percival and Josefsson, 2016", "RFC 7914, The scrypt Password-Based Key Derivation Function (Percival and Josefsson, 2016)", "https://www.rfc-editor.org/rfc/rfc7914", "secondary", "ev:rfc7914.txt"),
 ("AHB", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Appendix C, Bitcoin Improvement Proposals (Antonopoulos and Harding, 2023)", GH + "bitcoinbook/bitcoinbook/third_edition_print1/appc_bips.adoc", "secondary", "book:appc_bips.adoc"),
 ("PY", "Python Software Foundation, 2026", "Python 3.14.4 documentation source: the hashlib module, Doc/library/hashlib.rst at the tag v3.14.4 (Python Software Foundation, 2026)", GH + "python/cpython/v3.14.4/Doc/library/hashlib.rst", "secondary", "ev:python_hashlib.rst"),
 ("BC", "Bitcoin Core, 2026", "Bitcoin Core documentation: doc/bips.md and doc/descriptors.md at commit 05bc2f5 (Bitcoin Core, 2026)", GH + "bitcoin/bitcoin/" + CORE_C + "/doc/bips.md", "secondary", "ev:core_doc_bips.md"),
 ("BCD", "Bitcoin Core, 2026", "Bitcoin Core documentation: doc/descriptors.md at commit 05bc2f5 (Bitcoin Core, 2026)", GH + "bitcoin/bitcoin/" + CORE_C + "/doc/descriptors.md", "secondary", "ev:core_doc_descriptors.md"),
 ("BCW", "Bitcoin Core, 2026", "Bitcoin Core wallet source at commit 05bc2f5: src/wallet/wallet.h, src/wallet/walletutil.h and src/wallet/scriptpubkeyman.h (Bitcoin Core, 2026)", GH + "bitcoin/bitcoin/" + CORE_C + "/src/wallet/wallet.h", "secondary", "ev:core_src_wallet_wallet.h"),
 ("B31", "Bitcoin Core, 2026", "Bitcoin Core 31.1 release, downloaded, checked against SHA256SUMS and run as an offline node: descriptors, a fresh wallet, the BIP84 test vector and the RPC and option help (Bitcoin Core, 2026); evidence in 08-tooling/ch05-evidence", "https://bitcoincore.org/bin/bitcoin-core-31.1/", "secondary", "ev:core_version_31_1_v1_0_0.txt"),
 ("AL", "Altunel, 2021", "Course notes: Chapter_5_Wallets.pptx, SEN0401 (then CSE0469) Blockchain, Yusuf Altunel, 2021 - based on Mastering Bitcoin 2nd edition; the owner's file in 03-materials/owner-legacy-2025 (sha256 8f0d4ca26a81c514)", "urn:sen0401:course-notes:Chapter_5_Wallets.pptx:8f0d4ca26a81c514", "secondary", "file:../03-materials/owner-legacy-2025/slides-2025/Chapter_5_Wallets_v1_0_0.pptx"),
]
CITE = {s[0]: s[1] for s in SOURCES}
# markers used in the text: " [B32]" is replaced by " (Wuille, 2012)"
_MARK = dict(CITE); _MARK.update({"AH14": CITE["AH"], "AH7": CITE["AH"], "AHG": CITE["AH"], "AHB": CITE["AH"]})
def c(t):
    for k in sorted(_MARK, key=len, reverse=True): t = t.replace(" [" + k + "]", " (" + _MARK[k] + ")")
    assert "[" not in t.replace("[0]", "") or True
    import re
    bad = re.findall(r" \[[A-Z0-9]{2,5}\]", t)
    assert not bad, (bad, t[:120])
    return t
def P(*items):
    """paragraph list: items are (facet, text) pairs; markers are resolved"""
    return [(f, c(t)) for f, t in items]

# ---- builders of the executed claims (each result is an expression the chapter builder evaluates alone in a fresh interpreter) ----
_LIBS = "__import__('sys').path.insert(0, %r)" % HERE
def _CL(): return "(%s or __import__('sen0401_ch05_checklib_v1_0_0'))" % _LIBS
def _WL(): return "(%s or __import__('sen0401_ch05_wallet_lib_v1_1_0'))" % _LIBS
def Qb(name, *phrases): return ("%s.has_book(%r%s)" % (_CL(), name, "".join(", %r" % p for p in phrases)), "True")      # phrases in a chapter of the book
def Qe(name, *phrases): return ("%s.has_ev(%r%s)" % (_CL(), name, "".join(", %r" % p for p in phrases)), "True")        # phrases in a source saved in ch05-evidence
def Qs(chdir, name, *phrases): return ("%s.has_src(%r, %r%s)" % (_CL(), chdir, name, "".join(", %r" % p for p in phrases)), "True")   # in a source saved for another chapter
def Qc(path, *phrases): return ("%s.has_core(%r%s)" % (_CL(), path, "".join(", %r" % p for p in phrases)), "True")        # in a file of Bitcoin Core at the pinned commit
def X(expr_in_W, expected):
    """an executed claim: expr_in_W is evaluated with W = the chapter 5 wallet library (sen0401_ch05_wallet_lib_v1_1_0) and C = the check library"""
    return ("(lambda W, C: %s)(%s, %s)" % (expr_in_W, _WL(), _CL()), expected if isinstance(expected, str) else repr(expected))
CL, WL = _CL, _WL     # public aliases, so a text module can build its own claim expressions
def PROG(code, var="result"):
    """a small program (several statements) as one expression: its variable `result`. The page runs a worked example in the reader's
    browser, so such a program uses the standard library only and reads no files."""
    return "(lambda g: (exec(%r, g), g[%r])[1])({})" % (code, var)
# PBKDF2 written out with hmac and hashlib.sha512, because the Python of the course's browser pages has no hashlib.pbkdf2_hmac
# (that function needs OpenSSL, which Pyodide's build does not provide); a CHECKS entry compares it with hashlib's own.
PBKDF2 = ("import hashlib, hmac\n"
          "def seed(words, salt, rounds=2048):\n"
          "    u = hmac.new(words, salt + b'\\x00\\x00\\x00\\x01', hashlib.sha512).digest()\n"
          "    out = bytearray(u)\n"
          "    for _ in range(rounds - 1):\n"
          "        u = hmac.new(words, u, hashlib.sha512).digest()\n"
          "        out = bytearray(a ^ b for a, b in zip(out, u))\n"
          "    return bytes(out)\n")
def Pp(name, *phrases): return ("%s.has_pptx(%r%s)" % (_CL(), "../03-materials/owner-legacy-2025/slides-2025/" + name, "".join(", %r" % p for p in phrases)), "True")   # the owner's 2021 slides
