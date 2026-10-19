# Chapter 09 page assets - the wheel (v1.5.0)

Adds to ASSETS_PROVENANCE_v1_0_0.md, v1_1_0.md and v1_2_0.md (the story pictures, unchanged, licences there) the new wheel of the chapter 09 page, which replaces wheel 1.0.1 of v1_3_0 and v1_4_0 (the mempool.space census, which states no licence, is no longer shipped; the page built on wheel 1.0.1 is superseded) and carries only texts whose redistribution is clear.

## sen0401_ch09_lib-1.0.2-py3-none-any.whl

- sha256 `dd31ef4d639d622d862cc8ca7ea2a50d3dffdf405e72bd9765037d63f53390fe`, 497092 bytes; written by `08-tooling/ch09-page/pywheels_make_v1_0_2.py` (reproducible: zip dates fixed).
- Holds `sen0401_ch09_lib_v1_0_1.py` (copied byte for byte from 08-tooling) and, in `ch09-evidence`, 35 saved files copied byte for byte. The files are those the worked examples really open (found by running every example once with open() logged, not guessed from the text) AND whose terms clearly allow redistribution.
- 64 of the chapter's 69 worked examples run in the browser over them; 5 are shown as 'Recorded, not run on this page' because they read a file that is NOT in the wheel (below).

| File shipped | Bytes | Licence status |
|---|---|---|
| bip-0125.mediawiki | 9569 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0133.mediawiki | 3985 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0326.mediawiki | 8577 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0433.mediawiki | 4038 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bolt03_transactions.md | 194359 | CC BY 4.0 (BOLT 3; the file itself states it) |
| book_ch09_fees.adoc | 38795 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| book_ch10_network.adoc | 67355 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| core_doc_policy_mempool-design.md | 5351 | MIT (Bitcoin Core) |
| core_doc_policy_mempool-replacements.md | 3623 | MIT (Bitcoin Core) |
| core_doc_policy_packages.md | 7464 | MIT (Bitcoin Core) |
| core_relnotes_0.13.0.md | 45375 | MIT (Bitcoin Core) |
| core_relnotes_0.19.0.1.md | 56136 | MIT (Bitcoin Core) |
| core_relnotes_28.0.md | 14573 | MIT (Bitcoin Core) |
| core_relnotes_29.0.md | 12277 | MIT (Bitcoin Core) |
| core_relnotes_31.0.txt | 390335 | MIT (Bitcoin Core) |
| core_src_consensus_consensus.h | 1734 | MIT (Bitcoin Core) |
| core_src_kernel_mempool_options.h | 2634 | MIT (Bitcoin Core) |
| core_src_node_transaction.h | 3492 | MIT (Bitcoin Core) |
| core_src_policy_fees_block_policy_estimator.cpp | 46350 | MIT (Bitcoin Core) |
| core_src_policy_fees_block_policy_estimator.h | 15765 | MIT (Bitcoin Core) |
| core_src_policy_policy.h | 11046 | MIT (Bitcoin Core) |
| core_src_policy_rbf.cpp | 5909 | MIT (Bitcoin Core) |
| core_src_policy_truc_policy.h | 5437 | MIT (Bitcoin Core) |
| core_src_rpc_fees.cpp | 12526 | MIT (Bitcoin Core) |
| core_src_validation.cpp | 313611 | MIT (Bitcoin Core) |
| core_src_wallet_feebumper.cpp | 17824 | MIT (Bitcoin Core) |
| core_src_wallet_spend.cpp | 78840 | MIT (Bitcoin Core) |
| core_src_wallet_wallet.h | 54747 | MIT (Bitcoin Core) |
| mainnet_fee_census_v2_0_0.json | 269550 | CC BY 4.0 (the course's own census: facts of the block chain collected from mempool.space and blockstream.info and cross-checked, statistics computed by sen0401_ch09_census_collect_v1_0_0.py; licence statement in the file) |
| nakamoto_2008_bitcoin.txt | 25643 | MIT, as published on bitcoin.org |
| optech_newsletter_2023-10-25.txt | 29297 | CC BY 4.0 (Bitcoin Optech) |
| optech_topic_anchor_outputs.txt | 6908 | CC BY 4.0 (Bitcoin Optech) |
| optech_topic_replacement_cycling.txt | 4678 | CC BY 4.0 (Bitcoin Optech) |
| regtest2_run_v1_0_0.json | 11997 | this course's own run record |
| regtest_run_v1_0_0.json | 229357 | this course's own run record |

## Left out of the wheel (terms of redistribution not clear), and the examples that are recorded instead

- `carlsten_2016_instability.txt`: 2 examples (FeeOnlyFuture, UndercuttingAttack).
- `mempool_fees_recommended.json`: 1 example (RecommendedFeesToday).
- `ml_corallo_2018-12_carveout.txt`: 1 example (CarveOutRule).
- `moeser_boehme_2015_fees.txt`: 1 example (RevealedFeeBehaviour).

- Note: the recorded examples are the ones counted by the page's standin record (`08-tooling/ch09-page/standin_v1_0_2.json`). Left out for unclear terms: the full text of two academic papers (Carlsten et al., ACM CCS 2016; Moeser and Boehme, 2015) and of one mailing-list post (Corallo, 2018), which the wheel of v1_2_0 carried and this wheel does not; and the two saved market files fetched from the public mempool.space interface (`mempool_blocks_fees_1y.json`, `mempool_fees_recommended.json`; no licence stated by the service), which this wheel no longer carries either, as in the chapter 11 page. The mainnet census of the earlier wheel (`mainnet_fee_census_v1_0_0.json`, two blocks fetched from mempool.space, no licence stated) is no longer carried: this wheel carries the course's own census `mainnet_fee_census_v2_0_0.json` (20 blocks, CC BY 4.0, collected by `08-tooling/sen0401_ch09_census_collect_v1_0_0.py`, both services named and cross-checked inside the file).
