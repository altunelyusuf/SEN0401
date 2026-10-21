"""SEN0401 chapter 8 (Mastering Bitcoin 3rd edition, Digital Signatures) for the RDODI build, version 1.2.0: the version 1.0.0 research (sources, concepts, 45 executed leaves, 20 findings) plus eighteen
worked examples with changeable whole numbers (sen0401_ch08_leaves_v1_2_0.py), their 18 concept paragraphs, six claims that the passages they rely on are in the saved sources, and two findings.
Over 1.1.0 (a hand-patched copy of 1.0.0 whose publication labels carry the author-year string of the Stage 3 document): this module applies the same label additions to PUBS, so a rebuild keeps them.
Every source was opened on 2026-10-15 and is unchanged (its SHA-256 is checked by K.sources_resaved()); the eighteen examples were executed on 2026-10-21."""
__version__ = "1.2.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_rdodi_noquote_v1_0_0 as NQ
import sen0401_ch08_rdodi_data_v1_0_0 as D0
import sen0401_ch08_leaves_v1_2_0 as LV

CH = 8
DATE = "2026-10-21"          # the day of the last execution: the sources were opened on 2026-10-15, the eighteen worked examples of version 1.2.0 were executed on 2026-10-21
PYVER = "3.14.6"
VERSION = "1_2_0"
TITLE = D0.TITLE
QUESTION = D0.QUESTION
CQS = D0.CQS
_NEW_LABELS = {
    "ModularRemainder": "Remainder of a division", "ToyEcdsaCheck": "ECDSA with small numbers", "OtherValidS": "The other valid S", "DerPadding": "The padding zero of DER", "FlagByte": "The flag byte by hand",
    "SingleBugIndexes": "Inputs without an output", "HashedBytesGrowth": "Bytes hashed grow with inputs", "SlowSigops": "Twenty-five seconds for 5,569 operations", "SigopCapInputs": "Inputs under the operation cap",
    "LowRTries": "Chance of a low R", "SchnorrSavings": "Bytes saved by schnorr", "FiatShamirIntegers": "An identity round with small numbers", "KeyCancellationToy": "Key cancellation with small numbers",
    "ShamirModulus": "Shamir sharing modulo 101", "NonceReuseRecovery": "Recovering a key from a reused nonce", "PatentTermYears": "The patent term in years", "RetargetBoundary": "Activation on a retarget boundary",
    "TaggedPrefixBlock": "The tag prefix fills a block"}
LABELS = dict(D0.LABELS, **_NEW_LABELS)
# the author-year strings that the Stage 3 document cites, added to the labels of these publications in research 1.1.0 (each checked against the saved copy; see sen0401_research_cite_fix_ch8_v1_0_0.py)
_ADD = {"P03": "(Wuille et al., 2020)", "P04": "(Wuille et al., 2020)", "P05": "(Wuille et al., 2020)", "P06": "(Wuille et al., 2020)", "P07": "(Nick et al., 2022)",
        "P09": "(Lau and Wuille, 2016)", "P10": "(Lau and Wuille, 2016)", "P11": "(Decker and Towns, 2017)", "P12": "(Wuille, 2012)", "P13": "(Chow, 2017)", "P14": "(Chow, 2024)",
        "P15": "(Poinsot and Corallo, 2025)", "P16": "(Gilligan, 2026)", "P18": "(Chow, 2024)", "P36": "(SECG, 2010)", "P38": "(Schnorr, 1990)",
        "P39": "(Fiat and Shamir, 1986; CRYPTO 1986, proceedings volume dated 1987)", "P44": "(Komlo and Goldberg, 2021)", "P47": "(USPTO, 1991)",
        "P48": "(Cornell Legal Information Institute, 2026)", "P61": "(Lightning BOLTs, 2026)", "P65": "(Mempool Space, 2026)", "P66": "(Mempool Space, 2026)"}
PUBS = [(i, (l + " " + _ADD[i]) if i in _ADD else l, u, p) for i, l, u, p in D0.PUBS]
CONCEPTS = D0.CONCEPTS
_F = [
 ("F21", "Comparative analysis", "The numbers of the chapter's equations can be recomputed from whole numbers that a reader may change, and eighteen worked examples do so: the ECDSA equations and the identity proof hold line for line in the integers modulo 101 (Antonopoulos and Harding, 2023); a first byte of 136 gives the padding zero that makes the book's signature 71 bytes before the hash type (Antonopoulos and Harding, 2023); a flag byte of 131 is SINGLE with ANYONECANPAY (Bitcoin Core, 2026); 5,569 signature operations took 25 seconds, 4.5 milliseconds each (Lau and Wuille, 2016); the cap of 2,500 allows 1,250 inputs of 2 operations each (Bitcoin Core, 2026); a low R is found within 8 attempts with a chance of 0.9961 (Bitcoin Core, 2026); schnorr saves 9 bytes of witness for each input (Wuille et al., 2020); two signatures with one nonce give away the key (Antonopoulos and Harding, 2023); and the patent of 1990 ran to 2010 (Cornell Legal Information Institute, 2026).", ["P01", "P09", "P10", "P20", "P21", "P23", "P03", "P48", "P47"]),
 ("F22", "Conclusion", "The worked examples of version 1.2.0 carry their limits with them: the toy examples use the integers modulo 101 in place of curve points, so they show the algebra and not the secrecy, because division is possible there and impossible on secp256k1 (Antonopoulos and Harding, 2023); the sizes of the hashing model, 148 bytes for each input and 100 fixed bytes, and the 2 operations for each input under the cap are assumptions chosen for the arithmetic and not measurements; the 25 seconds were measured by the authors of BIP143 on the computer of 2015 and say nothing about today (Lau and Wuille, 2016); and the first taproot spend is the one in the saved mainnet record (Mempool Space, 2026).", ["P01", "P09", "P66"]),
]
FINDINGS = list(D0.FINDINGS) + _F
KP = D0.KP
_NEWTAX = [(t, m, l, ex, d, (NQ.noquote(c), r)) for t, m, l, ex, d, c, r, b in LV.NEW]
TAX = list(D0.TAX) + _NEWTAX
BODY = dict(D0.BODY)
for t, m, l, ex, d, c, r, b in LV.NEW:
    BODY[l] = b.replace('"', "'").replace("\n", " ")
_P = "import sys; sys.path.insert(0, '08-tooling'); import sen0401_ch08_sig_lib_v1_0_0 as C; "
CLAIMS = list(D0.CLAIMS) + [
 (_P + "(C.has('book_ch08_signatures.adoc', 'if it was 3 and the result of an operation was 5, the actual number we would use is 2', 's = k^{-1} (Hash(m) + x \\\\times R)', 'The +ANYONECANPAY+ has the value +0x80+ and is applied by bitwise OR', 'then the signing _private key_ can be calculated by anyone', 'People have had funds stolen because of inadvertent reuse of a _k_ value', 'roughly quadratically', 'Bob generates his public key using _zG_ – _yG_'), C.has('book_ch08_signatures.adoc', '+0x45+, the length of the sequence (69 bytes)', '+0x21+, the length of the integer (33 bytes)', 'producing exactly 64 bytes'))", "(True, True)"),
 (_P + "(C.has('core_src_script_interpreter.h', 'SIGHASH_ALL = 1', 'SIGHASH_NONE = 2', 'SIGHASH_SINGLE = 3', 'SIGHASH_ANYONECANPAY = 0x80'), C.has('core_src_script_interpreter.cpp', 'if (nIn >= txTo.vout.size())', 'return uint256::ONE'), C.has('core_src_key.cpp', 'return compact_sig[0] < 0x80', '// Grind for low R'), C.has('core_release_30.0_notes.txt', 'limited to 2500'))", "(True, True, True, True)"),
 (_P + "(C.has('bip-0143.mediawiki', '1 MB block would normally take 2 seconds to verify with an average computer in 2015, a 1MB transaction with 5569 sigops may take 25 seconds to verify', 'the time complexity becomes O(n)'), C.has('bip-0146.mediawiki', 'We require that the S value inside ECDSA signatures is at most the curve order divided by 2'))", "(True, True)"),
 (_P + "(C.has('bip-0340.mediawiki', 'ECDSA signatures are inherently malleable', 'This would result in 33-byte public keys and 65-byte signatures', 'resulting in 32-byte public keys and 64-byte signatures', 'this is a 64-byte long context-specific constant'), C.has('bip-0341.mediawiki', 'the min_activation_height is block 709632', 'The deployment did activate at height 709632 on Bitcoin mainnet'), C.has('bip-0327.mediawiki', 'key aggregation coefficient'))", "(True, True, True)"),
 (_P + "(C.has('shamir_1979_how_to_share_a_secret.txt', 'pick a prime p which is bigger than both D and n', 'leaves D completely undetermined'), C.has('google_patent_US4995082.txt', '1990-02-23', '1991-02-19'), C.has('cornell_35usc154.txt', 'ending 20 years from the date on which the application for the patent was filed', 'the greater of the 20-year term as provided in subsection (a), or 17 years from grant'), C.has('wikipedia_schnorr_signature.txt', 'expired in February 2010'))", "(True, True, True, True)"),
 (_P + "import json; j = json.load(open(C.ev('mainnet_tx_33e794d0.json'))); (j['status']['block_height'], C.has('bip-0066.mediawiki', 'strict'))", "(709635, True)"),
]
EXTRA = D0.EXTRA
BEH = D0.BEH
