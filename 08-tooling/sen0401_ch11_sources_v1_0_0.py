#!/usr/bin/env python3
"""SEN0401 chapter 11 (The Blockchain): the source table. One row per source opened: (id, author-year, label, url, saved file, role).
The saved copies live in ch11-evidence (fetched by sen0401_ch11_fetch_v1_0_0.py, which writes sources_index_v1_0_0.json with the HTTP status, size and sha256 of each);
the passages used from each are re-read from the saved copy by sen0401_ch11_quotes_v1_0_0.QUOTES, which the chapter's claims execute."""
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
G277314 = "00000000000000027e7ba6fe7bad39faf3b5a83daed765f05f7d1b71a1632249"
G277315 = "0000000000000002a7bbd25a417c0374cc55261021e8a9ca74442b01284f0569"
G0 = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
G840000 = "0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5"
S = [
 ("P01", AH, "Mastering Bitcoin, 3rd edition - Chapter 11, The Blockchain (Antonopoulos and Harding, 2023; O'Reilly; CC BY-SA 4.0; commit 275c4eb8, equal to tag third_edition_print1)", book("ch11_blockchain.adoc"), "book_ch11_blockchain.adoc", "primary"),
 ("P02", AH, "Mastering Bitcoin, 3rd edition - Chapter 12, Mining and Consensus: the nonce, the target and the forks the blockchain chapter points to (Antonopoulos and Harding, 2023)", book("ch12_mining.adoc"), "book_ch12_mining.adoc", "secondary"),
 ("P03", AH, "Mastering Bitcoin, 3rd edition - Chapter 10, The Bitcoin Network: headers, merkleblock and light clients (Antonopoulos and Harding, 2023)", book("ch10_network.adoc"), "book_ch10_network.adoc", "secondary"),
 ("P04", AH, "Mastering Bitcoin, 3rd edition - Chapter 3, Bitcoin Core: running the node, regtest and the command line (Antonopoulos and Harding, 2023)", book("ch03_bitcoin-core.adoc"), "book_ch03_bitcoin-core.adoc", "secondary"),
 ("P05", AH, "Mastering Bitcoin, 3rd edition - Chapter 4, Keys: the address prefixes of the networks (Antonopoulos and Harding, 2023)", book("ch04_keys.adoc"), "book_ch04_keys.adoc", "secondary"),
 ("P06", AH, "Mastering Bitcoin, 3rd edition - Glossary (Antonopoulos and Harding, 2023)", book("glossary.asciidoc"), "book_glossary.asciidoc", "secondary"),
 ("P07", "Wuille et al., 2015", "BIP 9, Version bits with timeout and delay (Pieter Wuille, Peter Todd, Greg Maxwell and Rusty Russell, assigned 2015-10-04, status Deployed): the version field of the block header (Wuille et al., 2015)", bip(9), "bip-0009.mediawiki", "secondary"),
 ("P08", "Wuille, 2012", "BIP 30, Duplicate transactions (Pieter Wuille, assigned 2012-02-22, status Deployed): a block may not contain a transaction that repeats an unspent one (Wuille, 2012)", bip(30), "bip-0030.mediawiki", "secondary"),
 ("P09", "Andresen, 2012", "BIP 34, Block v2, Height in Coinbase (Gavin Andresen, assigned 2012-07-06, status Deployed): the height in the coinbase (Andresen, 2012)", bip(34), "bip-0034.mediawiki", "secondary"),
 ("P10", "Kerin and Friedenbach, 2015", "BIP 113, Median time-past as endpoint for lock-time calculations (Thomas Kerin and Mark Friedenbach, assigned 2015-08-10, status Deployed): the median of the last 11 timestamps (Kerin and Friedenbach, 2015)", bip(113), "bip-0113.mediawiki", "secondary"),
 ("P11", "Alm and Towns, 2019", "BIP 325, Signet (Karl-Johan Alm and Anthony Towns, assigned 2019-03-20, status Complete): a test network whose blocks are signed by a challenge script (Alm and Towns, 2019)", bip(325), "bip-0325.mediawiki", "secondary"),
 ("P12", "Jahr, 2024", "BIP 94, Testnet 4 (Fabian Jahr, assigned 2024-05-27, status Deployed): the replacement of testnet3 (Jahr, 2024)", bip(94), "bip-0094.mediawiki", "secondary"),
 ("P13", "BtcDrak, 2018", "BIP 320, nVersion bits for general purpose use (BtcDrak, assigned 2018-03-01, status Draft): 16 bits of the version field as extra nonce space (BtcDrak, 2018)", bip(320), "bip-0320.mediawiki", "secondary"),
 ("P14", "Poinsot and Corallo, 2025", "BIP 54, Consensus Cleanup (Antoine Poinsot and Matt Corallo, assigned 2025-04-11, status Complete): the timewarp fix and the ban on 64-byte transactions (Poinsot and Corallo, 2025)", bip(54, "md"), "bip-0054.md", "secondary"),
 ("P15", BC, "Bitcoin Core at v31.1 (commit 9be056a): src/primitives/block.h, the CBlockHeader and CBlock classes (Bitcoin Core, 2026)", core("src/primitives/block.h"), "core_src_primitives_block.h", "secondary"),
 ("P16", BC, "Bitcoin Core at v31.1: src/primitives/block.cpp, the block hash as the hash of the header (Bitcoin Core, 2026)", core("src/primitives/block.cpp"), "core_src_primitives_block.cpp", "secondary"),
 ("P17", BC, "Bitcoin Core at v31.1: src/consensus/merkle.cpp, the merkle root and the CVE-2012-2459 comment (Bitcoin Core, 2026)", core("src/consensus/merkle.cpp"), "core_src_consensus_merkle.cpp", "secondary"),
 ("P18", BC, "Bitcoin Core at v31.1: src/consensus/consensus.h, the block weight limit and the coinbase maturity (Bitcoin Core, 2026)", core("src/consensus/consensus.h"), "core_src_consensus_consensus.h", "secondary"),
 ("P19", BC, "Bitcoin Core at v31.1: src/consensus/params.h, the consensus parameters of a chain (Bitcoin Core, 2026)", core("src/consensus/params.h"), "core_src_consensus_params.h", "secondary"),
 ("P20", BC, "Bitcoin Core at v31.1: src/kernel/chainparams.cpp, the genesis block, the testnet4 and signet parameters (Bitcoin Core, 2026)", core("src/kernel/chainparams.cpp"), "core_src_kernel_chainparams.cpp", "secondary"),
 ("P21", BC, "Bitcoin Core at v31.1: src/chainparamsbase.cpp, the data directory of each chain (Bitcoin Core, 2026)", core("src/chainparamsbase.cpp"), "core_src_chainparamsbase.cpp", "secondary"),
 ("P22", BC, "Bitcoin Core at v31.1: src/pow.cpp, the difficulty adjustment and the testnet minimum difficulty rule (Bitcoin Core, 2026)", core("src/pow.cpp"), "core_src_pow.cpp", "secondary"),
 ("P23", BC, "Bitcoin Core at v31.1: src/chain.h, the median time past and the block index (Bitcoin Core, 2026)", core("src/chain.h"), "core_src_chain.h", "secondary"),
 ("P24", BC, "Bitcoin Core at v31.1: src/validation.cpp, the block checks (Bitcoin Core, 2026)", core("src/validation.cpp"), "core_src_validation.cpp", "secondary"),
 ("P25", BC, "Bitcoin Core at v31.1: src/signet.cpp, the check of a signet block solution (Bitcoin Core, 2026)", core("src/signet.cpp"), "core_src_signet.cpp", "secondary"),
 ("P26", BC, "Bitcoin Core at v31.1: src/node/blockstorage.cpp, the layout of the blk files (Bitcoin Core, 2026)", core("src/node/blockstorage.cpp"), "core_src_node_blockstorage.cpp", "secondary"),
 ("P27", BC, "Bitcoin Core at v31.1: src/rpc/blockchain.cpp, getblock, getblockheader and getchaintips (Bitcoin Core, 2026)", core("src/rpc/blockchain.cpp"), "core_src_rpc_blockchain.cpp", "secondary"),
 ("P28", BC, "Bitcoin Core at v31.1: src/rpc/mining.cpp, generatetoaddress and generateblock (Bitcoin Core, 2026)", core("src/rpc/mining.cpp"), "core_src_rpc_mining.cpp", "secondary"),
 ("P29", BC, "Bitcoin Core at v31.1: doc/bips.md, the BIPs the node implements and since which version (Bitcoin Core, 2026)", core("doc/bips.md"), "core_doc_bips.md", "secondary"),
 ("P30", BC, "Bitcoin Core at v31.1: doc/files.md, the data directory layout (Bitcoin Core, 2026)", core("doc/files.md"), "core_doc_files.md", "secondary"),
 ("P31", BC, "Bitcoin Core at v31.1: src/util/chaintype.cpp, the chain names (Bitcoin Core, 2026)", core("src/util/chaintype.cpp"), "core_src_util_chaintype.cpp", "secondary"),
 ("P32", BCD + ", 2021", "Bitcoin Core release notes 0.21.0, 2021-01: signet support (Bitcoin Core developers, 2021)", rn("0.21.0"), "core_relnotes_0.21.0.md", "secondary"),
 ("P33", BCD + ", 2024", "Bitcoin Core release notes 28.0, 2024-10: testnet4 (Bitcoin Core developers, 2024)", rn("28.0"), "core_relnotes_28.0.md", "secondary"),
 ("P34", BCD + ", 2025", "Bitcoin Core release notes 29.0, 2025-04: the target field of getblock, the timewarp rule in block templates and the reserved block weight (Bitcoin Core developers, 2025)", rn("29.0"), "core_relnotes_29.0.md", "secondary"),
 ("P35", BCD + ", 2025", "Bitcoin Core release notes 30.0, 2025-10: the limit on legacy signature operations prepared for BIP 54 (Bitcoin Core developers, 2025)", rn("30.0"), "core_relnotes_30.0.md", "secondary"),
 ("P36", BCD + ", 2026", "Bitcoin Core release notes 31.0, 2026: the coinbase_tx object of getblock (Bitcoin Core developers, 2026)", "https://bitcoincore.org/en/releases/31.0/", "core_relnotes_31.0.html", "secondary"),
 ("P37", OT, "Bitcoin Optech topic: Time warp attack (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/time-warp/", "optech_topic_time_warp.html", "secondary"),
 ("P38", BCD + ", 2026", "Bitcoin Core 31.1 command line help, bitcoind -help and -help-debug, run on the binary (Bitcoin Core developers, 2026)", "local:bitcoind-help", "bitcoind_help_31.1.txt", "secondary"),
 ("P39", "Nakamoto, 2008", "Satoshi Nakamoto, Bitcoin: A Peer-to-Peer Electronic Cash System, 2008 (Nakamoto, 2008)", "https://bitcoin.org/bitcoin.pdf", "nakamoto_2008_bitcoin.pdf", "secondary"),
 ("P40", "Haber and Stornetta, 1991", "Stuart Haber and W. Scott Stornetta, How to Time-Stamp a Digital Document, Journal of Cryptology, 1991 (Haber and Stornetta, 1991)", "https://www.gwern.net/doc/bitcoin/1991-haber.pdf", "haber_stornetta_1991_timestamp.pdf", "secondary"),
 ("P41", "Merkle, 1980", "Ralph C. Merkle, Protocols for Public Key Cryptosystems, 1980 (Merkle, 1980)", "https://www.ralphmerkle.com/papers/Protocols.pdf", "merkle_1980_protocols.pdf", "secondary"),
 ("P42", OT, "Bitcoin Optech topic: Merkle tree vulnerabilities (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/merkle-tree-vulnerabilities/", "optech_topic_merkle_tree_vulnerabilities.html", "secondary"),
 ("P43", OT, "Bitcoin Optech topic: Testnet (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/testnet/", "optech_topic_testnet.html", "secondary"),
 ("P44", OT, "Bitcoin Optech topic: Signet (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/signet/", "optech_topic_signet.html", "secondary"),
 ("P45", OT, "Bitcoin Optech topic: Consensus cleanup soft fork (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/consensus-cleanup-soft-fork/", "optech_topic_consensus_cleanup.html", "secondary"),
 ("P46", BW, "Bitcoin Wiki, Genesis block (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Genesis_block", "bitcoinwiki_genesis_block.html", "secondary"),
 ("P47", BW, "Bitcoin Wiki, Block hashing algorithm (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Block_hashing_algorithm", "bitcoinwiki_block_hashing_algorithm.html", "secondary"),
 ("P48", BW, "Bitcoin Wiki, Testnet (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Testnet", "bitcoinwiki_testnet.html", "secondary"),
 ("P49", BW, "Bitcoin Wiki, Block timestamp (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Block_timestamp", "bitcoinwiki_block_timestamp.html", "secondary"),
 ("P50", BW, "Bitcoin Wiki, Protocol documentation: the block message and the compact size integer (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Protocol_documentation", "bitcoinwiki_protocol_documentation.html", "secondary"),
 ("P51", BW, "Bitcoin Wiki, Target: the compact encoding of the proof-of-work target (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Target", "bitcoinwiki_target.html", "secondary"),
 ("P52", WP, "Wikipedia, Merkle tree (Wikipedia contributors, 2026)", wp("Merkle_tree"), "wikipedia_merkle_tree.html", "secondary"),
 ("P53", WP, "Wikipedia, Ralph Merkle (Wikipedia contributors, 2026)", wp("Ralph_Merkle"), "wikipedia_ralph_merkle.html", "secondary"),
 ("P54", WP, "Wikipedia, Unix time: the 32-bit counter and the year 2106 (Wikipedia contributors, 2026)", wp("Unix_time"), "wikipedia_unix_time.html", "secondary"),
 ("P55", WP, "Wikipedia, Alistair Darling, the Chancellor of the Exchequer of the headline in the genesis block (Wikipedia contributors, 2026)", wp("Alistair_Darling"), "wikipedia_alistair_darling.html", "secondary"),
 ("P56", WP, "Wikipedia, The Times (Wikipedia contributors, 2026)", wp("The_Times"), "wikipedia_the_times.html", "secondary"),
 ("P57", WP, "Wikipedia, Cryptographic hash function (Wikipedia contributors, 2026)", wp("Cryptographic_hash_function"), "wikipedia_cryptographic_hash_function.html", "secondary"),
 ("P58", WP, "Wikipedia, Ice core: the layers of a glacier that the book compares the blockchain with (Wikipedia contributors, 2026)", wp("Ice_core"), "wikipedia_ice_core.html", "secondary"),
 ("P59", MS, "mempool.space, the genesis block (block 0), JSON (Mempool Space, 2026)", msp("api/block/" + G0), "mempool_block_0.json", "secondary"),
 ("P60", MS, "mempool.space, the 80-byte header of the genesis block in hexadecimal (Mempool Space, 2026)", msp("api/block/" + G0 + "/header"), "mempool_header_0.txt", "secondary"),
 ("P61", MS, "mempool.space, block 277,314, JSON (Mempool Space, 2026)", msp("api/block/" + G277314), "mempool_block_277314.json", "secondary"),
 ("P62", MS, "mempool.space, the header of block 277,314 (Mempool Space, 2026)", msp("api/block/" + G277314 + "/header"), "mempool_header_277314.txt", "secondary"),
 ("P63", MS, "mempool.space, block 277,315, JSON (Mempool Space, 2026)", msp("api/block/" + G277315), "mempool_block_277315.json", "secondary"),
 ("P64", MS, "mempool.space, the header of block 277,315 (Mempool Space, 2026)", msp("api/block/" + G277315 + "/header"), "mempool_header_277315.txt", "secondary"),
 ("P65", MS, "mempool.space, the transaction ids of block 277,315 (Mempool Space, 2026)", msp("api/block/" + G277315 + "/txids"), "mempool_txids_277315.json", "secondary"),
 ("P66", MS, "mempool.space, block 840,000, JSON (Mempool Space, 2026)", msp("api/block/" + G840000), "mempool_block_840000.json", "secondary"),
 ("P67", MS, "mempool.space, the height of the mainnet tip, fetched 2026-10-15 (Mempool Space, 2026)", msp("api/blocks/tip/height"), "mempool_tip_height.txt", "secondary"),
 ("P68", MS, "mempool.space, the height of the signet tip (Mempool Space, 2026)", msp("signet/api/blocks/tip/height"), "mempool_signet_tip_height.txt", "secondary"),
 ("P69", MS, "mempool.space, the height of the testnet4 tip (Mempool Space, 2026)", msp("testnet4/api/blocks/tip/height"), "mempool_testnet4_tip_height.txt", "secondary"),
 ("P70", MS, "mempool.space, the height of the testnet3 tip (Mempool Space, 2026)", msp("testnet/api/blocks/tip/height"), "mempool_testnet3_tip_height.txt", "secondary"),
 ("P71", "Blockchain Charts, 2026", "Blockchain.com charts, total size of the block chain in megabytes, API (Blockchain Charts, 2026)", "https://api.blockchain.info/charts/blocks-size?timespan=all&format=json&cors=true", "blockchaincom_blocks_size.json", "secondary"),
 ("P72", "Bitcoin Project, 2026", "Bitcoin.org Developer Guide: block chain (Bitcoin Project, 2026)", "https://developer.bitcoin.org/devguide/block_chain.html", "devguide_block_chain.html", "secondary"),
 ("P73", "Bitcoin Project, 2026", "Bitcoin.org Developer Reference: block headers (Bitcoin Project, 2026)", "https://developer.bitcoin.org/reference/block_chain.html", "devref_block_chain.html", "secondary"),
]
