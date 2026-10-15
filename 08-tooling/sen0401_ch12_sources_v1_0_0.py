#!/usr/bin/env python3
"""SEN0401 chapter 12 (Mining and Consensus): the source table. One row per source opened: (id, author-year, label, url, saved file, role).
The saved copies live in ch12-evidence (fetched by sen0401_ch12_fetch_v1_0_0.py, which writes sources_index_v1_0_0.json with the HTTP status, size and sha256 of each);
the passages used from each are re-read from the saved copy by sen0401_ch12_quotes_v1_0_0.QUOTES, which the chapter's claims execute."""
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
H210000 = "000000000000048b95347e83192f69cf0366076336c639f9b7228e9ba171342e"
H420000 = "000000000000000002cce816c0ab2c5c269cb081896b7dcb34b8422d6b74ffa1"
H630000 = "000000000000000000024bead8df69990852c202db0e0097c1a12ea637d7e96d"
H840000 = "0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5"
H225430 = "00000000000001c108384350f74090433e7fcf79a606b8e797f065b130575932"
H709632 = "0000000000000000000687bca986194dc2c1f949318629b44bb54ec0a94d8244"
H277316 = "0000000000000001b6b9a13b095e96db41c4a928b97ef2d944a9b31b2cc7bdc4"
H838656 = "00000000000000000001f2fa38c036edc385487c0226fbffc8bfe72c5a655899"
H840671 = "00000000000000000002bf1e60049e942ac34b728911adda77d704cc8401e84b"
H840672 = "00000000000000000001d2cbad2209f51143679b6797aef393a45e82eb88a9ae"
S = [
 ("P01", AH, "Mastering Bitcoin, 3rd edition - Chapter 12, Mining and Consensus (Antonopoulos and Harding, 2023; O'Reilly; CC BY-SA 4.0; commit 275c4eb8, equal to tag third_edition_print1)", book("ch12_mining.adoc"), "book_ch12_mining.adoc", "primary"),
 ("P02", AH, "Mastering Bitcoin, 3rd edition - Chapter 11, The Blockchain: the header, the nonce and the test chains that this chapter builds on (Antonopoulos and Harding, 2023)", book("ch11_blockchain.adoc"), "book_ch11_blockchain.adoc", "secondary"),
 ("P03", AH, "Mastering Bitcoin, 3rd edition - Chapter 9, Fees: fee rates and ancestor fee rate mining (Antonopoulos and Harding, 2023)", book("ch09_fees.adoc"), "book_ch09_fees.adoc", "secondary"),
 ("P04", AH, "Mastering Bitcoin, 3rd edition - Chapter 10, The Bitcoin Network: how a new block spreads (Antonopoulos and Harding, 2023)", book("ch10_network.adoc"), "book_ch10_network.adoc", "secondary"),
 ("P05", AH, "Mastering Bitcoin, 3rd edition - Chapter 7, Authorization and Authentication: timelocks, CLTV and CSV (Antonopoulos and Harding, 2023)", book("ch07_authorization-authentication.adoc"), "book_ch07_authorization-authentication.adoc", "secondary"),
 ("P06", AH, "Mastering Bitcoin, 3rd edition - Chapter 6, Transactions: the inputs and outputs a block carries (Antonopoulos and Harding, 2023)", book("ch06_transactions.adoc"), "book_ch06_transactions.adoc", "secondary"),
 ("P07", AH, "Mastering Bitcoin, 3rd edition - Glossary (Antonopoulos and Harding, 2023)", book("glossary.asciidoc"), "book_glossary.asciidoc", "secondary"),
 ("P08", AH, "Mastering Bitcoin, 3rd edition - Appendix C, the list of BIPs (Antonopoulos and Harding, 2023)", book("appc_bips.adoc"), "book_appc_bips.adoc", "secondary"),
 ("P09", AH, "Mastering Bitcoin, 3rd edition - code/max_money.py, the script printed in the chapter (Antonopoulos and Harding, 2023)", book("code/max_money.py"), "book_code_max_money.py", "secondary"),
 ("P10", "Wuille et al., 2015", "BIP 9, Version bits with timeout and delay (Pieter Wuille, Peter Todd, Greg Maxwell and Rusty Russell, assigned 2015-10-04, status Deployed) (Wuille et al., 2015)", bip(9), "bip-0009.mediawiki", "secondary"),
 ("P11", "Fry and Dashjr, 2017", "BIP 8, Version bits with lock-in by height (Shaolin Fry and Luke Dashjr) (Fry and Dashjr, 2017)", bip(8), "bip-0008.mediawiki", "secondary"),
 ("P12", "Andresen, 2012", "BIP 34, Block v2, Height in Coinbase (Gavin Andresen, assigned 2012-07-06, status Deployed) (Andresen, 2012)", bip(34), "bip-0034.mediawiki", "secondary"),
 ("P13", "Todd, 2014", "BIP 65, OP_CHECKLOCKTIMEVERIFY (Peter Todd, status Deployed) (Todd, 2014)", bip(65), "bip-0065.mediawiki", "secondary"),
 ("P14", "Wuille, 2015", "BIP 66, Strict DER signatures (Pieter Wuille, status Deployed) (Wuille, 2015)", bip(66), "bip-0066.mediawiki", "secondary"),
 ("P15", "Kerin and Friedenbach, 2015", "BIP 113, Median time-past as endpoint for lock-time calculations (Thomas Kerin and Mark Friedenbach, status Deployed) (Kerin and Friedenbach, 2015)", bip(113), "bip-0113.mediawiki", "secondary"),
 ("P16", "Lombrozo et al., 2015", "BIP 141, Segregated Witness (Consensus layer): the witness commitment in the coinbase (Eric Lombrozo, Johnson Lau and Pieter Wuille) (Lombrozo et al., 2015)", bip(141), "bip-0141.mediawiki", "secondary"),
 ("P17", "Shaolinfry, 2017", "BIP 148, Mandatory activation of segwit deployment (Shaolinfry, a pseudonym) (Shaolinfry, 2017)", bip(148), "bip-0148.mediawiki", "secondary"),
 ("P18", "Hilliard, 2017", "BIP 91, Reduced threshold Segwit MASF (James Hilliard) (Hilliard, 2017)", bip(91), "bip-0091.mediawiki", "secondary"),
 ("P19", "BtcDrak, 2018", "BIP 320, nVersion bits for general purpose use (BtcDrak, status Draft) (BtcDrak, 2018)", bip(320), "bip-0320.mediawiki", "secondary"),
 ("P20", "Poinsot and Corallo, 2025", "BIP 54, Consensus Cleanup (Antoine Poinsot and Matt Corallo) (Poinsot and Corallo, 2025)", bip(54, "md"), "bip-0054.md", "secondary"),
 ("P21", "Jahr, 2024", "BIP 94, Testnet 4: the difficulty rules that fix the timewarp and the minimum-difficulty storms (Fabian Jahr) (Jahr, 2024)", bip(94), "bip-0094.mediawiki", "secondary"),
 ("P22", "Andresen, 2013", "BIP 50, March 2013 Chain Fork Post-Mortem (Gavin Andresen) (Andresen, 2013)", bip(50), "bip-0050.mediawiki", "secondary"),
 ("P23", "Wuille et al., 2020", "BIP 341, Taproot: SegWit version 1 spending rules, with its deployment section (Pieter Wuille, Jonas Nick and Anthony Towns) (Wuille et al., 2020)", bip(341), "bip-0341.mediawiki", "secondary"),
 ("P24", "Dashjr, 2012", "BIP 22, getblocktemplate - Fundamentals (Luke Dashjr) (Dashjr, 2012)", bip(22), "bip-0022.mediawiki", "secondary"),
 ("P25", "Palatinus et al., 2017", "BIP 310, Stratum V1 protocol extensions, including version rolling (Marek Palatinus and others) (Palatinus et al., 2017)", bip(310), "bip-0310.mediawiki", "secondary"),
 ("P26", BC, "Bitcoin Core at v31.1 (commit 9be056a): src/pow.cpp, the difficulty adjustment and the proof-of-work check (Bitcoin Core, 2026)", core("src/pow.cpp"), "core_src_pow.cpp", "secondary"),
 ("P27", BC, "Bitcoin Core at v31.1: src/arith_uint256.cpp, the compact encoding of the target (Bitcoin Core, 2026)", core("src/arith_uint256.cpp"), "core_src_arith_uint256.cpp", "secondary"),
 ("P28", BC, "Bitcoin Core at v31.1: src/validation.cpp, GetBlockSubsidy, CheckBlock and the contextual block checks (Bitcoin Core, 2026)", core("src/validation.cpp"), "core_src_validation.cpp", "secondary"),
 ("P29", BC, "Bitcoin Core at v31.1: src/consensus/tx_check.cpp, the context-free checks of a transaction (Bitcoin Core, 2026)", core("src/consensus/tx_check.cpp"), "core_src_consensus_tx_check.cpp", "secondary"),
 ("P30", BC, "Bitcoin Core at v31.1: src/consensus/tx_verify.cpp, the input checks of a transaction (Bitcoin Core, 2026)", core("src/consensus/tx_verify.cpp"), "core_src_consensus_tx_verify.cpp", "secondary"),
 ("P31", BC, "Bitcoin Core at v31.1: src/consensus/consensus.h, the block weight limit, the coinbase maturity and the signature operation limit (Bitcoin Core, 2026)", core("src/consensus/consensus.h"), "core_src_consensus_consensus.h", "secondary"),
 ("P32", BC, "Bitcoin Core at v31.1: src/consensus/params.h, the consensus parameters of a chain, including the difficulty adjustment interval (Bitcoin Core, 2026)", core("src/consensus/params.h"), "core_src_consensus_params.h", "secondary"),
 ("P33", BC, "Bitcoin Core at v31.1: src/kernel/chainparams.cpp, the parameters of mainnet, testnet4, signet and regtest (Bitcoin Core, 2026)", core("src/kernel/chainparams.cpp"), "core_src_kernel_chainparams.cpp", "secondary"),
 ("P34", BC, "Bitcoin Core at v31.1: src/node/miner.cpp, how a block template is assembled (Bitcoin Core, 2026)", core("src/node/miner.cpp"), "core_src_node_miner.cpp", "secondary"),
 ("P35", BC, "Bitcoin Core at v31.1: src/node/miner.h, the block assembler options (Bitcoin Core, 2026)", core("src/node/miner.h"), "core_src_node_miner.h", "secondary"),
 ("P36", BC, "Bitcoin Core at v31.1: src/rpc/mining.cpp, getblocktemplate, generatetoaddress, generateblock and submitblock (Bitcoin Core, 2026)", core("src/rpc/mining.cpp"), "core_src_rpc_mining.cpp", "secondary"),
 ("P37", BC, "Bitcoin Core at v31.1: src/versionbits.cpp, the state machine of a deployment (Bitcoin Core, 2026)", core("src/versionbits.cpp"), "core_src_versionbits.cpp", "secondary"),
 ("P38", BC, "Bitcoin Core at v31.1: src/deploymentinfo.cpp, the names of the deployments (Bitcoin Core, 2026)", core("src/deploymentinfo.cpp"), "core_src_deploymentinfo.cpp", "secondary"),
 ("P39", BC, "Bitcoin Core at v31.1: src/policy/policy.h, the default block reserved weight and the standardness limits (Bitcoin Core, 2026)", core("src/policy/policy.h"), "core_src_policy_policy.h", "secondary"),
 ("P40", BC, "Bitcoin Core at v31.1: src/chain.h, the median time past (Bitcoin Core, 2026)", core("src/chain.h"), "core_src_chain.h", "secondary"),
 ("P41", BC, "Bitcoin Core at v31.1: src/consensus/validation.h, the rejection reasons of consensus (Bitcoin Core, 2026)", core("src/consensus/validation.h"), "core_src_consensus_validation.h", "secondary"),
 ("P42", BC, "Bitcoin Core at v31.1: doc/bips.md, the BIPs the node implements and since which version (Bitcoin Core, 2026)", core("doc/bips.md"), "core_doc_bips.md", "secondary"),
 ("P43", BCD + ", 2021", "Bitcoin Core release notes 0.21.1: the activation of taproot by speedy trial (Bitcoin Core developers, 2021)", rn("0.21.1"), "core_relnotes_0.21.1.md", "secondary"),
 ("P44", BCD + ", 2025", "Bitcoin Core release notes 29.0: the timewarp rule in block templates and the reserved block weight (Bitcoin Core developers, 2025)", rn("29.0"), "core_relnotes_29.0.md", "secondary"),
 ("P45", BCD + ", 2025", "Bitcoin Core release notes 30.0: the mining interface for external template providers (Bitcoin Core developers, 2025)", rn("30.0"), "core_relnotes_30.0.md", "secondary"),
 ("P46", BCD + ", 2026", "Bitcoin Core 31.1 command line help, bitcoind -help and -help-debug, run on the binary (Bitcoin Core developers, 2026)", "local:bitcoind-help", "bitcoind_help_31.1.txt", "secondary"),
 ("P47", "Nakamoto, 2008", "Satoshi Nakamoto, Bitcoin: A Peer-to-Peer Electronic Cash System, 2008 (Nakamoto, 2008)", "https://bitcoin.org/bitcoin.pdf", "nakamoto_2008_bitcoin.pdf", "secondary"),
 ("P48", "Back, 2002", "Adam Back, Hashcash - A Denial of Service Counter-Measure, 2002 (Back, 2002)", "http://www.hashcash.org/papers/hashcash.pdf", "back_2002_hashcash.pdf", "secondary"),
 ("P49", "Dwork and Naor, 1992", "Cynthia Dwork and Moni Naor, Pricing via Processing or Combatting Junk Mail, CRYPTO 1992 (Dwork and Naor, 1992)", "https://www.wisdom.weizmann.ac.il/~naor/PAPERS/pvp.pdf", "dwork_naor_1992_pricing.pdf", "secondary"),
 ("P50", "Eyal and Sirer, 2013", "Ittay Eyal and Emin Gun Sirer, Majority is not Enough: Bitcoin Mining is Vulnerable, arXiv 1311.0243 (Eyal and Sirer, 2013)", "https://arxiv.org/pdf/1311.0243", "eyal_sirer_2013_selfish_mining.pdf", "secondary"),
 ("P51", "Rosenfeld, 2014", "Meni Rosenfeld, Analysis of Hashrate-Based Double Spending, arXiv 1402.2009 (Rosenfeld, 2014)", "https://arxiv.org/pdf/1402.2009", "rosenfeld_2014_double_spending.pdf", "secondary"),
 ("P52", OT, "Bitcoin Optech topic: Time warp attack (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/time-warp/", "optech_topic_time_warp.html", "secondary"),
 ("P53", OT, "Bitcoin Optech topic: Soft fork activation (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/soft-fork-activation/", "optech_topic_soft_fork_activation.html", "secondary"),
 ("P54", OT, "Bitcoin Optech topic: Selfish mining (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/selfish-mining/", "optech_topic_selfish_mining.html", "secondary"),
 ("P55", OT, "Bitcoin Optech topic: ASICBoost (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/asicboost/", "optech_topic_asicboost.html", "secondary"),
 ("P56", OT, "Bitcoin Optech topic: Block withholding attacks (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/block-withholding/", "optech_topic_block_withholding.html", "secondary"),
 ("P57", OT, "Bitcoin Optech topic: Taproot (Bitcoin Optech, 2026)", "https://bitcoinops.org/en/topics/taproot/", "optech_topic_taproot.html", "secondary"),
 ("P58", BW, "Bitcoin Wiki, Difficulty (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Difficulty", "bitcoinwiki_difficulty.html", "secondary"),
 ("P59", BW, "Bitcoin Wiki, Controlled supply (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Controlled_supply", "bitcoinwiki_controlled_supply.html", "secondary"),
 ("P60", BW, "Bitcoin Wiki, Mining (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Mining", "bitcoinwiki_mining.html", "secondary"),
 ("P61", BW, "Bitcoin Wiki, Stratum mining protocol (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Stratum_mining_protocol", "bitcoinwiki_stratum_mining_protocol.html", "secondary"),
 ("P62", BW, "Bitcoin Wiki, Hashcash (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Hashcash", "bitcoinwiki_hashcash.html", "secondary"),
 ("P63", BW, "Bitcoin Wiki, Majority attack (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Majority_attack", "bitcoinwiki_majority_attack.html", "secondary"),
 ("P64", BW, "Bitcoin Wiki, Proof of work (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Proof_of_work", "bitcoinwiki_proof_of_work.html", "secondary"),
 ("P65", BW, "Bitcoin Wiki, Comparison of mining pools (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/wiki/Comparison_of_mining_pools", "bitcoinwiki_comparison_of_mining_pools.html", "secondary"),
 ("P66", "Stratum contributors, 2026", "Stratum V2 specification, the Stratum Reference Implementation project (Stratum contributors, 2026)", "https://stratumprotocol.org/specification/", "stratum_v2_specification.html", "secondary"),
 ("P67", WP, "Wikipedia, Adam Back (Wikipedia contributors, 2026)", wp("Adam_Back"), "wikipedia_adam_back.html", "secondary"),
 ("P68", WP, "Wikipedia, Hashcash (Wikipedia contributors, 2026)", wp("Hashcash"), "wikipedia_hashcash.html", "secondary"),
 ("P69", WP, "Wikipedia, Berkeley DB, the database behind the chain split of March 2013 (Wikipedia contributors, 2026)", wp("Berkeley_DB"), "wikipedia_berkeley_db.html", "secondary"),
 ("P70", WP, "Wikipedia, SegWit (Wikipedia contributors, 2026)", wp("SegWit"), "wikipedia_segwit.html", "secondary"),
 ("P71", WP, "Wikipedia, Bitcoin Cash, the hard fork of 2017 (Wikipedia contributors, 2026)", wp("Bitcoin_Cash"), "wikipedia_bitcoin_cash.html", "secondary"),
 ("P72", MS, "mempool.space, block 277,316, the block of the book's example, JSON with extras (Mempool Space, 2026)", msp("api/v1/block/" + H277316), "mempool_block_277316.json", "secondary"),
 ("P73", MS, "mempool.space, the header of block 277,316 (Mempool Space, 2026)", msp("api/block/" + H277316 + "/header"), "mempool_header_277316.txt", "secondary"),
 ("P74", MS, "mempool.space, block 840,000, the fourth halving, JSON with extras (Mempool Space, 2026)", msp("api/v1/block/" + H840000), "mempool_block_840000.json", "secondary"),
 ("P75", MS, "mempool.space, block 210,000, the first halving, JSON (Mempool Space, 2026)", msp("api/v1/block/" + H210000), "mempool_block_210000.json", "secondary"),
 ("P76", MS, "mempool.space, block 420,000, the second halving, JSON (Mempool Space, 2026)", msp("api/v1/block/" + H420000), "mempool_block_420000.json", "secondary"),
 ("P77", MS, "mempool.space, block 630,000, the third halving, JSON (Mempool Space, 2026)", msp("api/v1/block/" + H630000), "mempool_block_630000.json", "secondary"),
 ("P78", MS, "mempool.space, block 225,430, the block that split the chain in March 2013, JSON (Mempool Space, 2026)", msp("api/v1/block/" + H225430), "mempool_block_225430.json", "secondary"),
 ("P79", MS, "mempool.space, block 709,632, the first block under taproot rules, JSON (Mempool Space, 2026)", msp("api/v1/block/" + H709632), "mempool_block_709632.json", "secondary"),
 ("P80", MS, "mempool.space, the header of block 838,656, the first block of a difficulty period (Mempool Space, 2026)", msp("api/block/" + H838656 + "/header"), "mempool_header_838656.txt", "secondary"),
 ("P81", MS, "mempool.space, the header of block 840,671, the last block of that period (Mempool Space, 2026)", msp("api/block/" + H840671 + "/header"), "mempool_header_840671.txt", "secondary"),
 ("P82", MS, "mempool.space, the header of block 840,672, the first block after the adjustment (Mempool Space, 2026)", msp("api/block/" + H840672 + "/header"), "mempool_header_840672.txt", "secondary"),
 ("P83", MS, "mempool.space, the difficulty adjustment under way, fetched 2026-10-15 (Mempool Space, 2026)", msp("api/v1/difficulty-adjustment"), "mempool_difficulty_adjustment.json", "secondary"),
 ("P84", MS, "mempool.space, the difficulty adjustments of the last two years (Mempool Space, 2026)", msp("api/v1/mining/difficulty-adjustments/2y"), "mempool_difficulty_adjustments_2y.json", "secondary"),
 ("P85", MS, "mempool.space, the mining pools by blocks found in the last year (Mempool Space, 2026)", msp("api/v1/mining/pools/1y"), "mempool_pools_1y.json", "secondary"),
 ("P86", MS, "mempool.space, the hash rate of the last three months (Mempool Space, 2026)", msp("api/v1/mining/hashrate/3m"), "mempool_hashrate_3m.json", "secondary"),
 ("P87", MS, "mempool.space, the height of the mainnet tip, fetched 2026-10-15 (Mempool Space, 2026)", msp("api/blocks/tip/height"), "mempool_tip_height.txt", "secondary"),
 ("P88", "Blockchain Charts, 2026", "Blockchain.com charts, the hash rate of the network over all time, API (Blockchain Charts, 2026)", "https://api.blockchain.info/charts/hash-rate?timespan=all&format=json&cors=true", "blockchaincom_hash_rate.json", "secondary"),
 ("P89", "Buterin, 2013", "Vitalik Buterin, Bitcoin Network Shaken by Blockchain Fork, Bitcoin Magazine, 13 March 2013 (Buterin, 2013)", "https://bitcoinmagazine.com/technical/bitcoin-network-shaken-by-blockchain-fork-1363144448", "bitcoinmagazine_2013_chain_fork.html", "secondary"),
 ("P90", MS, "mempool.space, block 225,429, the last block before the split of March 2013, JSON (Mempool Space, 2026)", msp("api/v1/block/0000000000000366ce98ca28338900094e8cbf445776253181749f782546d006"), "mempool_block_225429.json", "secondary"),
 ("P91", MS, "mempool.space, block 225,454, the block at which the split of March 2013 ended, JSON (Mempool Space, 2026)", msp("api/v1/block/00000000000001976860e9e35b20b8ebe22c35f813a40962c25ead9fbd89510b"), "mempool_block_225454.json", "secondary"),
]
