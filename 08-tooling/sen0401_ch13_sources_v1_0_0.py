#!/usr/bin/env python3
"""SEN0401 chapter 13 (Bitcoin Security): the source table. One row per source opened: (id, author-year, label, url, saved file, role).
The saved copies live in ch13-evidence (fetched by sen0401_ch13_fetch_v1_0_0.py, which writes sources_index_v1_0_0.json with the HTTP status, size and sha256 of each);
the passages used from each are re-read from the saved copy by sen0401_ch13_quotes_v1_0_0.QUOTES, which the chapter's claims execute."""
__version__ = "1.0.0"
GH = "https://raw.githubusercontent.com/"
BOOK_C = "275c4eb8eab8800c6adc39f8def8e8f8fa356a57"      # the commit the textbook ontology pins; its chapter files equal tag third_edition_print1 (6d1c26e1)
CORE_C = "9be056a8a72b624dae9623b2f7bded92c2a21c91"      # tag v31.1 of bitcoin/bitcoin
AH, BC = "Antonopoulos and Harding, 2023", "Bitcoin Core, 2026"
BCD = "Bitcoin Core developers"
OT = "Bitcoin Optech, 2026"
WP = "Wikipedia contributors, 2026"
BW = "Bitcoin Wiki, 2026"
MS = "Mempool Space, 2026"
book = lambda f: GH + "bitcoinbook/bitcoinbook/" + BOOK_C + "/" + f
core = lambda f: GH + "bitcoin/bitcoin/" + CORE_C + "/" + f
bip = lambda n, ext="mediawiki": GH + "bitcoin/bips/master/bip-%04d.%s" % (n, ext)
rn = lambda v: core("doc/release-notes/release-notes-%s.md" % v)
wp = lambda t: "https://en.wikipedia.org/api/rest_v1/page/html/" + t
msp = lambda p: "https://mempool.space/" + p

H0 = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
D = "https://bitcoincore.org/bin/bitcoin-core-31.1/"
wb = lambda t: "https://en.bitcoin.it/wiki/" + t
OTP = lambda t: "https://bitcoinops.org/en/topics/%s/" % t
S = [
 ("P01", AH, "Mastering Bitcoin, 3rd edition - Chapter 13, Bitcoin Security (Antonopoulos and Harding, 2023; O'Reilly; CC BY-SA 4.0; commit 275c4eb8, equal to tag third_edition_print1)", book("ch13_security.adoc"), "book_ch13_security.adoc", "primary"),
 ("P02", AH, "Mastering Bitcoin, 3rd edition - Chapter 5, Wallets: seeds, recovery codes and descriptors (Antonopoulos and Harding, 2023)", book("ch05_wallets.adoc"), "book_ch05_wallets.adoc", "secondary"),
 ("P03", AH, "Mastering Bitcoin, 3rd edition - Chapter 4, Keys and Addresses (Antonopoulos and Harding, 2023)", book("ch04_keys.adoc"), "book_ch04_keys.adoc", "secondary"),
 ("P04", AH, "Mastering Bitcoin, 3rd edition - Chapter 7, Authorization and Authentication: multisignature and timelocks (Antonopoulos and Harding, 2023)", book("ch07_authorization-authentication.adoc"), "book_ch07_authorization-authentication.adoc", "secondary"),
 ("P05", AH, "Mastering Bitcoin, 3rd edition - Chapter 6, Transactions (Antonopoulos and Harding, 2023)", book("ch06_transactions.adoc"), "book_ch06_transactions.adoc", "secondary"),
 ("P06", AH, "Mastering Bitcoin, 3rd edition - Chapter 8, Digital Signatures: what a signature commits to (Antonopoulos and Harding, 2023)", book("ch08_signatures.adoc"), "book_ch08_signatures.adoc", "secondary"),
 ("P07", AH, "Mastering Bitcoin, 3rd edition - Chapter 3, Bitcoin Core: Reference Implementation (Antonopoulos and Harding, 2023)", book("ch03_bitcoin-core.adoc"), "book_ch03_bitcoin-core.adoc", "secondary"),
 ("P08", AH, "Mastering Bitcoin, 3rd edition - Chapter 10, The Bitcoin Network: encrypted transport (Antonopoulos and Harding, 2023)", book("ch10_network.adoc"), "book_ch10_network.adoc", "secondary"),
 ("P09", AH, "Mastering Bitcoin, 3rd edition - Glossary (Antonopoulos and Harding, 2023)", book("glossary.asciidoc"), "book_glossary.asciidoc", "secondary"),
 ("P10", AH, "Mastering Bitcoin, 3rd edition - Appendix C, the list of BIPs (Antonopoulos and Harding, 2023)", book("appc_bips.adoc"), "book_appc_bips.adoc", "secondary"),
 ("P11", AH, "Mastering Bitcoin, 3rd edition - Appendix B, the errata of the book (Antonopoulos and Harding, 2023)", book("appb_errata.adoc"), "book_appb_errata.adoc", "secondary"),
 ("P12", "Palatinus et al., 2013", "BIP 39, Mnemonic code for generating deterministic keys (Marek Palatinus, Pavol Rusnak, Aaron Voisine and Sean Bowe, status Proposed) (Palatinus et al., 2013)", bip(39), "bip-0039.mediawiki", "secondary"),
 ("P13", "Wuille, 2012", "BIP 32, Hierarchical Deterministic Wallets, with its test vectors (Pieter Wuille, status Final) (Wuille, 2012)", bip(32), "bip-0032.mediawiki", "secondary"),
 ("P14", "Caldwell and Voisine, 2012", "BIP 38, Passphrase-protected private key (Mike Caldwell and Aaron Voisine, assigned 2012-11-20) (Caldwell and Voisine, 2012)", bip(38), "bip-0038.mediawiki", "secondary"),
 ("P15", "Kerin et al., 2015", "BIP 67, Deterministic Pay-to-script-hash multi-signature addresses through public key sorting (Thomas Kerin, Jean-Pierre Rupp and Ruben de Vries, assigned 2015-02-08) (Kerin et al., 2015)", bip(67), "bip-0067.mediawiki", "secondary"),
 ("P16", "Friedenbach et al., 2015", "BIP 68, Relative lock-time using consensus-enforced sequence numbers (Mark Friedenbach, BtcDrak, Nicolas Dorier and kinoshitajona) (Friedenbach et al., 2015)", bip(68), "bip-0068.mediawiki", "secondary"),
 ("P17", "BtcDrak et al., 2015", "BIP 112, CHECKSEQUENCEVERIFY (BtcDrak, Mark Friedenbach and Eric Lombrozo) (BtcDrak et al., 2015)", bip(112), "bip-0112.mediawiki", "secondary"),
 ("P18", "Lau and Wuille, 2016", "BIP 143, Transaction Signature Verification for Version 0 Witness Program (Johnson Lau and Pieter Wuille, status Deployed) (Lau and Wuille, 2016)", bip(143), "bip-0143.mediawiki", "secondary"),
 ("P19", "Chow, 2017", "BIP 174, Partially Signed Bitcoin Transaction Format (Ava Chow, assigned 2017-07-12, status Deployed) (Chow, 2017)", bip(174), "bip-0174.mediawiki", "secondary"),
 ("P20", "Chow, 2021", "BIP 370, PSBT Version 2 (Andrew Chow) (Chow, 2021)", bip(370), "bip-0370.mediawiki", "secondary"),
 ("P21", "Wuille and Chow, 2021", "BIP 380, Output Script Descriptors General Operation (Pieter Wuille and Ava Chow, assigned 2021-06-27) (Wuille and Chow, 2021)", bip(380), "bip-0380.mediawiki", "secondary"),
 ("P22", "Wuille and Chow, 2021", "BIP 382, Segwit Output Script Descriptors (Pieter Wuille and Ava Chow, assigned 2021-06-27) (Wuille and Chow, 2021)", bip(382), "bip-0382.mediawiki", "secondary"),
 ("P23", "Wuille and Chow, 2024", "BIP 387, Tapscript Output Script Descriptors (Pieter Wuille and Ava Chow, assigned 2024-04-17) (Wuille and Chow, 2024)", bip(387), "bip-0387.mediawiki", "secondary"),
 ("P24", "Ingala, 2023", "BIP 388, Wallet Policies for Descriptor Wallets (Salvatore Ingala, assigned 2023-12-26) (Ingala, 2023)", bip(388), "bip-0388.mediawiki", "secondary"),
 ("P25", "Olsson Curr et al., 2023", "BIP 93, codex32: Checksummed SSS-enabled BIP32 seeds (Leon Olsson Curr, Pearlwort Sneed and Andrew Poelstra, assigned 2023-02-13, status Draft) (Olsson Curr et al., 2023)", bip(93), "bip-0093.mediawiki", "secondary"),
 ("P26", "Mehta et al., 2019", "BIP 324, Version 2 P2P Encrypted Transport Protocol (Dhruv Mehta, Tim Ruffing, Jonas Schnelli and Pieter Wuille, assigned 2019-03-08) (Mehta et al., 2019)", bip(324), "bip-0324.mediawiki", "secondary"),
 ("P27", "Palatinus et al., 2013", "BIP 39 English word list, 2048 words (Palatinus et al., 2013)", GH + "bitcoin/bips/master/bip-0039/english.txt", "bip39_english.txt", "secondary"),
 ("P28", "Trezor developers, 2026", "python-mnemonic test vectors for BIP 39 (SatoshiLabs; Trezor developers, 2026)", GH + "trezor/python-mnemonic/master/vectors.json", "bip39_trezor_vectors.json", "secondary"),
 ("P29", BC, "Bitcoin Core at v31.1 (commit 9be056a): src/wallet/crypter.cpp, the key stretching and the encryption of wallet keys (Bitcoin Core, 2026)", core("src/wallet/crypter.cpp"), "core_src_wallet_crypter.cpp", "secondary"),
 ("P30", BC, "Bitcoin Core at v31.1: src/wallet/crypter.h, the sizes of key, salt and rounds (Bitcoin Core, 2026)", core("src/wallet/crypter.h"), "core_src_wallet_crypter.h", "secondary"),
 ("P31", BC, "Bitcoin Core at v31.1: src/wallet/rpc/encrypt.cpp, encryptwallet, walletpassphrase and walletlock (Bitcoin Core, 2026)", core("src/wallet/rpc/encrypt.cpp"), "core_src_wallet_rpc_encrypt.cpp", "secondary"),
 ("P32", BC, "Bitcoin Core at v31.1: src/wallet/rpc/backup.cpp, backupwallet, restorewallet and importdescriptors (Bitcoin Core, 2026)", core("src/wallet/rpc/backup.cpp"), "core_src_wallet_rpc_backup.cpp", "secondary"),
 ("P33", BC, "Bitcoin Core at v31.1: src/wallet/rpc/wallet.cpp, createwallet and its options (Bitcoin Core, 2026)", core("src/wallet/rpc/wallet.cpp"), "core_src_wallet_rpc_wallet.cpp", "secondary"),
 ("P34", BC, "Bitcoin Core at v31.1: src/rpc/rawtransaction.cpp, testmempoolaccept and the PSBT RPCs (Bitcoin Core, 2026)", core("src/rpc/rawtransaction.cpp"), "core_src_rpc_rawtransaction.cpp", "secondary"),
 ("P35", BC, "Bitcoin Core at v31.1: src/kernel/chainparams.cpp, the genesis block and the assumed-valid block (Bitcoin Core, 2026)", core("src/kernel/chainparams.cpp"), "core_src_kernel_chainparams.cpp", "secondary"),
 ("P36", BC, "Bitcoin Core at v31.1: src/script/descriptor.cpp, output script descriptors and miniscript in them (Bitcoin Core, 2026)", core("src/script/descriptor.cpp"), "core_src_script_descriptor.cpp", "secondary"),
 ("P37", BC, "Bitcoin Core at v31.1: doc/psbt.md, how Bitcoin Core handles partially signed transactions (Bitcoin Core, 2026)", core("doc/psbt.md"), "core_doc_psbt.md", "secondary"),
 ("P38", BC, "Bitcoin Core at v31.1: doc/descriptors.md (Bitcoin Core, 2026)", core("doc/descriptors.md"), "core_doc_descriptors.md", "secondary"),
 ("P39", BC, "Bitcoin Core at v31.1: doc/managing-wallets.md, backup and restore of wallets (Bitcoin Core, 2026)", core("doc/managing-wallets.md"), "core_doc_managing-wallets.md", "secondary"),
 ("P40", BC, "Bitcoin Core at v31.1: doc/external-signer.md, hardware signing devices through an external signer (Bitcoin Core, 2026)", core("doc/external-signer.md"), "core_doc_external-signer.md", "secondary"),
 ("P41", BC, "Bitcoin Core at v31.1: contrib/guix/README.md, reproducible builds (Bitcoin Core, 2026)", core("contrib/guix/README.md"), "core_contrib_guix_README.md", "secondary"),
 ("P42", BCD + ", 2018", "Bitcoin Core release notes 0.17.0: PSBT RPCs and the wallet in the node (Bitcoin Core developers, 2018)", rn("0.17.0"), "core_relnotes_0.17.0.md", "secondary"),
 ("P43", BCD + ", 2022", "Bitcoin Core release notes 23.0: descriptor wallets by default (Bitcoin Core developers, 2022)", rn("23.0"), "core_relnotes_23.0.md", "secondary"),
 ("P44", BCD + ", 2023", "Bitcoin Core release notes 26.0: encrypted transport of BIP 324 (Bitcoin Core developers, 2023)", rn("26.0"), "core_relnotes_26.0.md", "secondary"),
 ("P45", BCD + ", 2025", "Bitcoin Core release notes 30.0: legacy wallets and the Berkeley DB wallet (Bitcoin Core developers, 2025)", rn("30.0"), "core_relnotes_30.0.md", "secondary"),
 ("P46", BCD + ", 2026", "Bitcoin Core release notes 31.0 (Bitcoin Core developers, 2026)", "https://bitcoincore.org/en/releases/31.0/", "core_relnotes_31.0.html", "secondary"),
 ("P47", BCD + ", 2026", "Bitcoin Core 31.1 command line help, bitcoind -help and -help-debug, run on the binary (Bitcoin Core developers, 2026)", "local:bitcoind-help", "bitcoind_help_31.1.txt", "secondary"),
 ("P48", BC, "Bitcoin Core at v31.1: src/script/interpreter.cpp, the signature hash types (Bitcoin Core, 2026)", core("src/script/interpreter.cpp"), "core_src_script_interpreter.cpp", "secondary"),
 ("P49", "Bitcoin Core release signers, 2026", "Bitcoin Core 31.1 SHA256SUMS, the list of hashes of the release files (Bitcoin Core release signers, 2026)", D + "SHA256SUMS", "bitcoincore_31.1_SHA256SUMS.txt", "secondary"),
 ("P50", "Bitcoin Core release signers, 2026", "Bitcoin Core 31.1 SHA256SUMS.asc, the signatures of the builders over that list (Bitcoin Core release signers, 2026)", D + "SHA256SUMS.asc", "bitcoincore_31.1_SHA256SUMS.asc.txt", "secondary"),
 ("P51", "Nakamoto, 2008", "Satoshi Nakamoto, Bitcoin: A Peer-to-Peer Electronic Cash System, 2008, with its section on privacy (Nakamoto, 2008)", "https://bitcoin.org/bitcoin.pdf", "nakamoto_2008_bitcoin.pdf", "secondary"),
 ("P52", "Shamir, 1979", "Adi Shamir, How to Share a Secret, Communications of the ACM 22(11), 1979 (Shamir, 1979)", "https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf", "shamir_1979_how_to_share_a_secret.pdf", "secondary"),
 ("P53", "Moriarty et al., 2017", "RFC 8018, PKCS #5: Password-Based Cryptography Specification Version 2.1, the PBKDF2 used by BIP 39 (Moriarty et al., 2017)", "https://www.rfc-editor.org/rfc/rfc8018.txt", "rfc8018_pbkdf2.txt", "secondary"),
 ("P54", OT, "Bitcoin Optech topic: Partially signed bitcoin transactions (Bitcoin Optech, 2026)", OTP("psbt"), "optech_topic_psbt.html", "secondary"),
 ("P55", OT, "Bitcoin Optech topic: Miniscript (Bitcoin Optech, 2026)", OTP("miniscript"), "optech_topic_miniscript.html", "secondary"),
 ("P56", OT, "Bitcoin Optech topic: Output script descriptors (Bitcoin Optech, 2026)", OTP("output-script-descriptors"), "optech_topic_output_script_descriptors.html", "secondary"),
 ("P57", OT, "Bitcoin Optech topic: Multisignature (Bitcoin Optech, 2026)", OTP("multisignature"), "optech_topic_multisignature.html", "secondary"),
 ("P58", OT, "Bitcoin Optech topic: Timelocks (Bitcoin Optech, 2026)", OTP("timelocks"), "optech_topic_timelocks.html", "secondary"),
 ("P59", BW, "Bitcoin Wiki, Securing your wallet (Bitcoin Wiki, 2026)", wb("Securing_your_wallet"), "bitcoinwiki_securing_your_wallet.html", "secondary"),
 ("P60", BW, "Bitcoin Wiki, Hardware wallet (Bitcoin Wiki, 2026)", wb("Hardware_wallet"), "bitcoinwiki_hardware_wallet.html", "secondary"),
 ("P61", BW, "Bitcoin Wiki, Paper wallet (Bitcoin Wiki, 2026)", wb("Paper_wallet"), "bitcoinwiki_paper_wallet.html", "secondary"),
 ("P62", BW, "Bitcoin Wiki, Casascius physical bitcoins (Bitcoin Wiki, 2026)", wb("Casascius_physical_bitcoins"), "bitcoinwiki_casascius.html", "secondary"),
 ("P63", BW, "Bitcoin Wiki, Mt. Gox (Bitcoin Wiki, 2026)", wb("Mt._Gox"), "bitcoinwiki_mt_gox.html", "secondary"),
 ("P64", BW, "Bitcoin Wiki, Trezor (Bitcoin Wiki, 2026)", wb("Trezor"), "bitcoinwiki_trezor.html", "secondary"),
 ("P65", BW, "Bitcoin Wiki, Brainwallet (Bitcoin Wiki, 2026)", wb("Brainwallet"), "bitcoinwiki_brainwallet.html", "secondary"),
 ("P66", BW, "Bitcoin Wiki, Multisignature (Bitcoin Wiki, 2026)", wb("Multisignature"), "bitcoinwiki_multisignature.html", "secondary"),
 ("P67", WP, "Wikipedia, Mt. Gox (Wikipedia contributors, 2026)", wp("Mt._Gox"), "wikipedia_mt_gox.html", "secondary"),
 ("P68", WP, "Wikipedia, Cryptocurrency wallet (Wikipedia contributors, 2026)", wp("Cryptocurrency_wallet"), "wikipedia_cryptocurrency_wallet.html", "secondary"),
 ("P69", WP, "Wikipedia, Shamir's secret sharing (Wikipedia contributors, 2026)", wp("Shamir%27s_secret_sharing"), "wikipedia_shamir_secret_sharing.html", "secondary"),
 ("P70", WP, "Wikipedia, Adi Shamir (Wikipedia contributors, 2026)", wp("Adi_Shamir"), "wikipedia_adi_shamir.html", "secondary"),
 ("P71", WP, "Wikipedia, Bitfinex, with the hack of 2016 (Wikipedia contributors, 2026)", wp("Bitfinex"), "wikipedia_bitfinex.html", "secondary"),
 ("P72", WP, "Wikipedia, Air gap (networking) (Wikipedia contributors, 2026)", wp("Air_gap_(networking)"), "wikipedia_air_gap.html", "secondary"),
 ("P73", MS, "mempool.space, the genesis block, JSON (Mempool Space, 2026)", msp("api/v1/block/" + H0), "mempool_block_0.json", "secondary"),
 ("P74", MS, "mempool.space, the height of the mainnet tip, fetched 2026-10-15 (Mempool Space, 2026)", msp("api/blocks/tip/height"), "mempool_tip_height.txt", "secondary"),
 ("P76", MS, "mempool.space, block 938,343, the assumed-valid block of Bitcoin Core 31.1, JSON (Mempool Space, 2026)", msp("api/v1/block/00000000000000000000ccebd6d74d9194d8dcdc1d177c478e094bfad51ba5ac"), "mempool_block_938343.json", "secondary"),
 ("P75", "Bitcoin.org, 2026", "Bitcoin.org, Secure your wallet (Bitcoin.org, 2026)", "https://bitcoin.org/en/secure-your-wallet", "bitcoinorg_secure_your_wallet.html", "secondary"),
 ("P77", BCD + ", 2024", "Bitcoin Core release notes 27.0: encrypted transport on by default (Bitcoin Core developers, 2024)", rn("27.0"), "core_relnotes_27.0.md", "secondary"),
]
