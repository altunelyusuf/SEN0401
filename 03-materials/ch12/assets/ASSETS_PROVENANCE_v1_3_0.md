# Chapter 12 page assets - the wheel (v1.3.0)

Adds to ASSETS_PROVENANCE_v1_0_0.md, v1_1_0.md and v1_2_0.md (the story pictures: unchanged, licences there) the one new asset of the chapter 12 page.

## sen0401_ch12_lib-1.0.1-py3-none-any.whl

- sha256 `17be534353bab3e4d423abe1db91fb0d43ae54d53c1e108cd02d7bb302c21054`, 319524 bytes; written by `08-tooling/ch12-page/pywheels_make_v1_0_1.py` (reproducible: zip dates fixed).
- Holds `sen0401_ch12_lib_v1_0_0.py`, `sen0401_ch10_p2p_v1_0_0.py` (copied byte for byte from 08-tooling) and, in `ch12-evidence`, 40 saved files copied byte for byte. The files are those the worked examples really open (found by running every example once with open() logged, not guessed from the text) AND whose terms clearly allow redistribution.
- 41 of the chapter's 65 worked examples run in the browser over them; 24 are shown as 'Recorded, not run on this page' because they read a file that is NOT in the wheel (below).

| File shipped | Bytes | Licence status |
|---|---|---|
| bip-0008.mediawiki | 18814 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0009.mediawiki | 14058 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0022.mediawiki | 12552 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0050.mediawiki | 6716 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0054.md | 19163 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0091.mediawiki | 6634 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0094.mediawiki | 10706 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0113.mediawiki | 4656 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0141.mediawiki | 26314 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0148.mediawiki | 4224 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0310.mediawiki | 12090 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0320.mediawiki | 3588 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bitcoinwiki_difficulty.txt | 12116 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_majority_attack.txt | 3954 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_proof_of_work.txt | 6226 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_stratum_mining_protocol.txt | 11019 | CC BY 3.0 (Bitcoin Wiki) |
| book_ch12_mining.adoc | 119091 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| core_relnotes_0.21.1.md | 8939 | MIT (Bitcoin Core) |
| core_relnotes_29.0.md | 12277 | MIT (Bitcoin Core) |
| core_relnotes_30.0.md | 17197 | MIT (Bitcoin Core) |
| core_src_arith_uint256.cpp | 6476 | MIT (Bitcoin Core) |
| core_src_chain.h | 16656 | MIT (Bitcoin Core) |
| core_src_consensus_consensus.h | 1734 | MIT (Bitcoin Core) |
| core_src_consensus_validation.h | 7307 | MIT (Bitcoin Core) |
| core_src_deploymentinfo.cpp | 1692 | MIT (Bitcoin Core) |
| core_src_kernel_chainparams.cpp | 37441 | MIT (Bitcoin Core) |
| core_src_node_miner.cpp | 22056 | MIT (Bitcoin Core) |
| core_src_pow.cpp | 6549 | MIT (Bitcoin Core) |
| core_src_rpc_mining.cpp | 51920 | MIT (Bitcoin Core) |
| core_src_validation.cpp | 313611 | MIT (Bitcoin Core) |
| nakamoto_2008_bitcoin.txt | 25643 | MIT, as published on bitcoin.org |
| optech_topic_asicboost.txt | 2491 | CC BY 4.0 (Bitcoin Optech) |
| optech_topic_block_withholding.txt | 3576 | CC BY 4.0 (Bitcoin Optech) |
| optech_topic_selfish_mining.txt | 3333 | CC BY 4.0 (Bitcoin Optech) |
| optech_topic_soft_fork_activation.txt | 27817 | CC BY 4.0 (Bitcoin Optech) |
| optech_topic_time_warp.txt | 7862 | CC BY 4.0 (Bitcoin Optech) |
| regtest_run_v1_0_0.json | 25853 | this course's own run record |
| wikipedia_berkeley_db.txt | 15271 | CC BY-SA (Wikipedia) |
| wikipedia_bitcoin_cash.txt | 34648 | CC BY-SA (Wikipedia) |
| wikipedia_segwit.txt | 11668 | CC BY-SA (Wikipedia) |

## Left out of the wheel (terms of redistribution not clear), and the examples that are recorded instead

- `bip-0034.mediawiki`: 2 examples (Bip34Activation, Bip34HeightPush).
- `book_code_max_money.py`: 1 example (BookScriptFloatErratum).
- `eyal_sirer_2013_selfish_mining.txt`: 1 example (SelfishMiningThreshold).
- `mempool_block_210000.json`: 1 example (HalvingEvery210000).
- `mempool_block_225430.json`: 1 example (ChainSplitMarch2013).
- `mempool_block_277316.json`: 4 examples (DifficultyFromTarget, MedianTimePast, RewardIsSubsidyPlusFees, VersionHistory).
- `mempool_block_709632.json`: 1 example (SpeedyTrialTaproot).
- `mempool_block_840000.json`: 3 examples (CoinbaseDataAndTags, CompactBits, FeesOfBlock840000).
- `mempool_difficulty_adjustment.json`: 1 example (NextAdjustmentToday).
- `mempool_difficulty_adjustments_2y.json`: 2 examples (HashrateFromDifficulty, RecentAdjustments).
- `mempool_hashrate_3m.json`: 1 example (NonceSpaceIsTiny).
- `mempool_header_277316.txt`: 2 examples (HashBelowTarget, HeaderOfBlock277316).
- `mempool_header_838656.txt`: 1 example (RetargetFormulaOnRealEpoch).
- `mempool_pools_1y.json`: 2 examples (PoolConcentration, TopPoolVersusThresholds).
- `stratum_v2_specification.txt`: 1 example (StratumProtocols).

- Note: the recorded examples are the ones counted by the page's standin record (`08-tooling/ch12-page/standin_v1_0_1.json`). Data from mempool.space and Blockchain.com carries no stated licence; the papers (Eyal and Sirer 2013, Back 2002, Dwork and Naor 1992, Rosenfeld 2014), the Bitcoin Magazine article and the Stratum V2 specification are not carried because their redistribution terms are not clear to this author; a BIP whose header has no License line (BIP 34) is withheld although the other BIPs state an open licence. `book_code_max_money.py`, a short code listing of the book repository, was carried by the wheel of v1_2_0 (page 9.47.0) and is no longer carried: its licence is not separately clear, so the example that reads it is Recorded.
