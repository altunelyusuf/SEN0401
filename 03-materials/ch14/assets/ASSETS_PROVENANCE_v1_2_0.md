# Chapter 14 page assets - the wheel (v1.2.0)

Adds to ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md (the story pictures: unchanged, licences there) the one new asset of the chapter 14 page.

## sen0401_ch14_lib-1.0.0-py3-none-any.whl

- sha256 `e47f07c297fd098cebcaaee96795d02a55f21449e69b50cf3d34d789dd5990f2`, 325392 bytes; written by `08-tooling/ch14-page/pywheels_make_v1_0_0.py` (reproducible: zip dates fixed).
- Holds `sen0401_ch14_lib_v1_0_0.py`, `sen0401_ch10_p2p_v1_0_0.py`, `sen0401_ch14_crypto_v1_0_0.py` (copied byte for byte from 08-tooling) and, in `ch14-evidence`, 22 saved files copied byte for byte. The files are those the worked examples really open (found by running every example once with open() logged, not guessed from the text) AND whose terms clearly allow redistribution.
- 40 of the chapter's 50 worked examples run in the browser over them; 10 are shown as 'Recorded, not run on this page' because they read a file that is NOT in the wheel (below).

| File shipped | Bytes | Licence status |
|---|---|---|
| bip-0118.mediawiki | 20418 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0119.mediawiki | 36474 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0125.mediawiki | 9569 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0431.mediawiki | 27577 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0433.mediawiki | 4038 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bitcoind_help_31.1.txt | 60324 | MIT (Bitcoin Core) |
| bitcoinwiki_colored_coins.txt | 14530 | CC BY 3.0 (Bitcoin Wiki) |
| bolt03_transactions.md | 194359 | CC BY 4.0 (stated in the BOLT file itself) |
| bolt04_onion_routing.md | 155433 | CC BY 4.0 (stated in the BOLT file itself) |
| bolt08_transport.md | 43682 | CC BY 4.0 (stated in the BOLT file itself) |
| bolt11_payment_encoding.md | 52334 | CC BY 4.0 (stated in the BOLT file itself) |
| book_appb_errata.adoc | 11582 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| book_ch12_mining.adoc | 119091 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| book_ch14_applications.adoc | 71554 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| core_relnotes_28.0.md | 14573 | MIT (Bitcoin Core) |
| lnd_sample_lnd.conf.txt | 82839 | MIT (lnd) |
| optech_topic_client_side_validation.txt | 4768 | CC BY 4.0 (Bitcoin Optech) |
| optech_topic_eltoo.txt | 3815 | CC BY 4.0 (Bitcoin Optech) |
| optech_topic_ptlc.txt | 4539 | CC BY 4.0 (Bitcoin Optech) |
| regtest_run_v1_0_0.json | 39802 | this course's own run record |
| wikipedia_lightning_network.txt | 17381 | CC BY-SA (Wikipedia) |
| wikipedia_noise_protocol.txt | 57152 | CC BY-SA (Wikipedia) |

## Left out of the wheel (terms of redistribution not clear), and the examples that are recorded instead

- `bolt04_onion_test.json`: 3 examples (OnionFixedSize, OnionIntegrityByHmac, OnionPacketVector).
- `cln_readme.md`: 1 example (OtherImplementations).
- `mempool_lightning_statistics.json`: 3 examples (BookFeeVersusNetworkFee, LightningNoLongerProposed, MainnetGraphSize).
- `poon_dryja_lightning_paper.txt`: 1 example (WhitepaperDate).
- `rgb_tech.txt`: 1 example (RgbAndTaprootAssets).
- `rosenfeld_colored_coins_2012.txt`: 1 example (ColoredCoinsHistory).

- Note: the recorded examples are the ones counted by the page's standin record (`08-tooling/ch14-page/standin_v1_0_0.json`). Left out because their terms of redistribution are not clear to this author: mempool.space data, papers (Danezis and Goldberg 2009, Decker and Wattenhofer 2015), forum posts (bitcointalk), web pages (Lightning Engineering), the lnd release manifest, the BIP 341 and BOLT 4 test-vector files (no licence statement in the file itself), the README files of other implementations, any BIP whose header has no License line, and any code listing of the book (`book_code_*`). The wheel also carries the chapter's two helper modules (`sen0401_ch14_crypto_v1_0_0.py`, `sen0401_ch10_p2p_v1_0_0.py`), copied byte for byte from 08-tooling.
