# Chapter 11 page assets - the wheel (v1.2.0)

Adds to ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md (the story pictures: unchanged, licences there) the one new asset of the chapter 11 page.

## sen0401_ch11_lib-1.0.0-py3-none-any.whl

- sha256 `6946a8f136bd777a3d6175514539902e23b2ee605028b13eb0d1d532c5db7477`, 371510 bytes; written by `08-tooling/ch11-page/pywheels_make_v1_0_0.py` (reproducible: zip dates fixed).
- Holds `sen0401_ch11_lib_v1_0_0.py`, `sen0401_ch10_p2p_v1_0_0.py` (copied byte for byte from 08-tooling) and, in `ch11-evidence`, 31 saved files copied byte for byte. The files are those the worked examples really open (found by running every example once with open() logged, not guessed from the text) AND whose terms clearly allow redistribution.
- 44 of the chapter's 69 worked examples run in the browser over them; 25 are shown as 'Recorded, not run on this page' because they read a file that is NOT in the wheel (below).

| File shipped | Bytes | Licence status |
|---|---|---|
| bip-0009.mediawiki | 14058 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0054.md | 19163 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0094.mediawiki | 10706 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0113.mediawiki | 4656 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0320.mediawiki | 3588 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0325.mediawiki | 8754 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bitcoind_help_31.1.txt | 60324 | MIT (Bitcoin Core) |
| bitcoinwiki_genesis_block.txt | 9095 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_target.txt | 3733 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_testnet.txt | 8226 | CC BY 3.0 (Bitcoin Wiki) |
| book_ch11_blockchain.adoc | 38691 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| book_ch12_mining.adoc | 119091 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| core_relnotes_28.0.md | 14573 | MIT (Bitcoin Core) |
| core_relnotes_29.0.md | 12277 | MIT (Bitcoin Core) |
| core_relnotes_31.0.txt | 390335 | MIT (Bitcoin Core) |
| core_src_chain.h | 16656 | MIT (Bitcoin Core) |
| core_src_consensus_consensus.h | 1734 | MIT (Bitcoin Core) |
| core_src_consensus_merkle.cpp | 7251 | MIT (Bitcoin Core) |
| core_src_kernel_chainparams.cpp | 37441 | MIT (Bitcoin Core) |
| core_src_pow.cpp | 6549 | MIT (Bitcoin Core) |
| core_src_primitives_block.cpp | 927 | MIT (Bitcoin Core) |
| core_src_validation.cpp | 313611 | MIT (Bitcoin Core) |
| nakamoto_2008_bitcoin.txt | 25643 | MIT, as published on bitcoin.org |
| optech_topic_merkle_tree_vulnerabilities.txt | 9923 | CC BY 4.0 (Bitcoin Optech) |
| regtest_run_v1_0_0.json | 26987 | this course's own run record |
| wikipedia_alistair_darling.txt | 53450 | CC BY-SA (Wikipedia) |
| wikipedia_ice_core.txt | 86753 | CC BY-SA (Wikipedia) |
| wikipedia_merkle_tree.txt | 17113 | CC BY-SA (Wikipedia) |
| wikipedia_ralph_merkle.txt | 15158 | CC BY-SA (Wikipedia) |
| wikipedia_the_times.txt | 98077 | CC BY-SA (Wikipedia) |
| wikipedia_unix_time.txt | 46183 | CC BY-SA (Wikipedia) |

## Left out of the wheel (terms of redistribution not clear), and the examples that are recorded instead

- `bip-0034.mediawiki`: 1 example (Bip34HeightInCoinbase).
- `haber_stornetta_1991_timestamp.txt`: 1 example (HashChainedTimestamps).
- `mempool_block_0.json`: 2 examples (GenesisListingMatchesBook, RootIsAlways32Bytes).
- `mempool_block_277315.json`: 3 examples (MedianTimePast, NonceAndExtraNonce, TargetCompactEncoding).
- `mempool_block_840000.json`: 4 examples (BlockReservedWeight, BlockWeightLimit, TimestampField, VersionBitsField).
- `mempool_header_0.txt`: 3 examples (BlockHashIsDoubleSha256, HashLeadingZeros, HeaderIs80Bytes).
- `mempool_header_277315.txt`: 2 examples (Block277315Links, FieldOrderAndEndianness).
- `mempool_signet_tip_height.txt`: 1 example (SignetSizeToday).
- `mempool_testnet3_tip_height.txt`: 2 examples (Testnet3StillThere, TestnetBlockStorms).
- `mempool_testnet4_tip_height.txt`: 1 example (Testnet4Replaces).
- `mempool_tip_height.txt`: 1 example (HeightFromGenesis).
- `mempool_txids_277315.json`: 3 examples (PathLengthLogarithm, RealBlockRoot, TreeDepth).
- `merkle_1980_protocols.txt`: 1 example (HashTreeHistory).

- Note: the recorded examples are the ones counted by the page's standin record (`08-tooling/ch11-page/standin_v1_0_0.json`). Data from mempool.space carries no stated licence; the papers (Haber and Stornetta 1991, Merkle 1980) are copyright of their publishers or authors; `bip-0034.mediawiki` carries no licence line in its header and is withheld although the other BIPs state an open licence.
