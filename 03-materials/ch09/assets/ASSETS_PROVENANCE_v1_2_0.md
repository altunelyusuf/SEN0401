# Chapter 9 page assets - the wheel (v1.2.0)

Adds to ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md (the four story pictures: unchanged, licences there) the one new asset of the chapter 9 page.

## sen0401_ch09_lib-1.0.0-py3-none-any.whl

- sha256 `a1d820c842ea2f805af18299ed56d6c0201601e55067ea4b5c8d2053112c2d19`, 576741 bytes; written by `08-tooling/ch09-page/pywheels_make_v1_0_0.py` (reproducible: zip dates fixed).
- Holds `sen0401_ch09_lib_v1_0_0.py` (the chapter library, copied byte for byte from 08-tooling) and, in the folder `ch09-evidence`, 40 saved files copied byte for byte from `08-tooling/ch09-evidence` (a .pdf or .html source is shipped as the .txt conversion the library reads). They are exactly the files the chapter's worked examples read, found by the tool from the examples' text.
- The page unpacks it into the Python worker (Pyodide) at start, so 67 of the chapter's 69 worked examples run in the browser over the recorded data; the other two are recorded (their text in the ontology is not valid Python).

| File shipped | Bytes |
|---|---|
| bip-0125.mediawiki | 9569 |
| bip-0133.mediawiki | 3985 |
| bip-0326.mediawiki | 8577 |
| bip-0433.mediawiki | 4038 |
| bolt03_transactions.md | 194359 |
| book_ch09_fees.adoc | 38795 |
| book_ch10_network.adoc | 67355 |
| carlsten_2016_instability.txt | 157324 |
| core_doc_policy_mempool-design.md | 5351 |
| core_doc_policy_mempool-replacements.md | 3623 |
| core_doc_policy_packages.md | 7464 |
| core_relnotes_0.13.0.md | 45375 |
| core_relnotes_0.19.0.1.md | 56136 |
| core_relnotes_28.0.md | 14573 |
| core_relnotes_29.0.md | 12277 |
| core_relnotes_31.0.txt | 390335 |
| core_src_consensus_consensus.h | 1734 |
| core_src_kernel_mempool_options.h | 2634 |
| core_src_node_transaction.h | 3492 |
| core_src_policy_fees_block_policy_estimator.cpp | 46350 |
| core_src_policy_fees_block_policy_estimator.h | 15765 |
| core_src_policy_policy.h | 11046 |
| core_src_policy_rbf.cpp | 5909 |
| core_src_policy_truc_policy.h | 5437 |
| core_src_rpc_fees.cpp | 12526 |
| core_src_validation.cpp | 313611 |
| core_src_wallet_feebumper.cpp | 17824 |
| core_src_wallet_spend.cpp | 78840 |
| core_src_wallet_wallet.h | 54747 |
| mainnet_fee_census_v1_0_0.json | 286134 |
| mempool_blocks_fees_1y.json | 81181 |
| mempool_fees_recommended.json | 74 |
| ml_corallo_2018-12_carveout.txt | 8399 |
| moeser_boehme_2015_fees.txt | 41965 |
| nakamoto_2008_bitcoin.txt | 25643 |
| optech_newsletter_2023-10-25.txt | 29297 |
| optech_topic_anchor_outputs.txt | 6908 |
| optech_topic_replacement_cycling.txt | 4678 |
| regtest2_run_v1_0_0.json | 11997 |
| regtest_run_v1_0_0.json | 229357 |

## Licence questions (for the instructor to decide)

The page is meant for the course's students and carries copies of saved sources as data. Licences, as far as the sources state them:

- Mastering Bitcoin 3rd edition chapters (`book_ch09_fees.adoc`, `book_ch10_network.adoc`): CC BY-SA 4.0 (attribution and share-alike; the page names the book).
- Bitcoin Core files (`core_src_*`, `core_doc_*`, `core_relnotes_*`): MIT licence. BIPs (`bip-*.mediawiki`): the licence each BIP states (BSD-2-Clause or public domain). BOLT 3 (`bolt03_transactions.md`): CC0. Bitcoin Optech pages (`optech_*`): CC BY 4.0. Satoshi Nakamoto's paper (`nakamoto_2008_bitcoin.txt`): MIT licence as published on bitcoin.org.
- UNCLEAR, a decision is needed: the full text of two academic papers (`carlsten_2016_instability.txt`, Carlsten, Kalodner, Weinberg and Narayanan, ACM CCS 2016, and `moeser_boehme_2015_fees.txt`, Moeser and Boehme, 2015) and of one mailing-list post (`ml_corallo_2018-12_carveout.txt`). They are in the course repository already (as the research package's saved sources) and the page now carries them again inside the wheel. If redistribution of the papers' full text is not allowed, the two files can be left out of the wheel; the examples that read them then become 'Recorded, not run on this page' and the page loses those runs, nothing else.
- Market data (`mempool_blocks_fees_1y.json`, `mempool_fees_recommended.json`, `mainnet_fee_census_v1_0_0.json`): numbers fetched from the public mempool.space interface and from block data on 2026-10-15; no licence is stated by the service.
