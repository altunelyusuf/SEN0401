# Chapter 10 page assets - the wheel (v1.2.0)

Adds to ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md (the five story pictures: unchanged, licences there) the one new asset of the chapter 10 page.

## sen0401_ch10_lib-1.0.0-py3-none-any.whl

- sha256 `8f9aaf7ee9915157e94a21271215a3e6fc43464929c5a8a890f299c048364d99`, 350329 bytes; written by `08-tooling/ch10-page/pywheels_make_v1_0_0.py` (reproducible: zip dates fixed).
- Holds `sen0401_ch10_lib_v1_0_0.py` and `sen0401_ch10_p2p_v1_0_0.py` (copied byte for byte from 08-tooling) and, in `ch10-evidence`, 36 saved files copied byte for byte. The files are those the worked examples really open (found by running every example once with open() logged, not guessed from the text) AND whose terms clearly allow redistribution.
- 49 of the chapter's 62 worked examples run in the browser over them; 13 are shown as 'Recorded, not run on this page' because they read a file that is NOT in the wheel (below).

| File shipped | Bytes | Licence status |
|---|---|---|
| bip-0130.mediawiki | 2683 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0144.mediawiki | 5204 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0151.mediawiki | 10331 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0152.mediawiki | 31006 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0155.mediawiki | 9740 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0157.mediawiki | 21050 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0158.mediawiki | 16770 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0158_testnet-19.json | 17816 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0159.mediawiki | 3361 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0324.mediawiki | 67644 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bip-0339.mediawiki | 3087 | the open licence each BIP states (BSD-2-Clause or public domain) |
| bitcoind_help_31.1.txt | 60324 | MIT (Bitcoin Core) |
| book_ch10_network.adoc | 67355 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| core_doc_bips.md | 17450 | MIT (Bitcoin Core) |
| core_doc_tor.md | 11120 | MIT (Bitcoin Core) |
| core_relnotes_22.0.md | 79585 | MIT (Bitcoin Core) |
| core_relnotes_23.0.md | 12654 | MIT (Bitcoin Core) |
| core_relnotes_26.0.md | 15000 | MIT (Bitcoin Core) |
| core_relnotes_27.0.md | 7034 | MIT (Bitcoin Core) |
| core_relnotes_28.0.md | 14573 | MIT (Bitcoin Core) |
| core_relnotes_29.0.md | 12277 | MIT (Bitcoin Core) |
| core_relnotes_30.0.md | 17197 | MIT (Bitcoin Core) |
| core_relnotes_31.0.txt | 390335 | MIT (Bitcoin Core) |
| core_src_blockencodings.h | 5028 | MIT (Bitcoin Core) |
| core_src_common_bloom.h | 4838 | MIT (Bitcoin Core) |
| core_src_headerssync.h | 11658 | MIT (Bitcoin Core) |
| core_src_kernel_chainparams.cpp | 37441 | MIT (Bitcoin Core) |
| core_src_net.h | 77942 | MIT (Bitcoin Core) |
| core_src_net_processing.cpp | 297492 | MIT (Bitcoin Core) |
| core_src_net_processing.h | 8012 | MIT (Bitcoin Core) |
| core_src_node_protocol_version.h | 1366 | MIT (Bitcoin Core) |
| core_src_node_txorphanage.h | 7035 | MIT (Bitcoin Core) |
| core_src_test_bloom_tests.cpp | 47491 | MIT (Bitcoin Core) |
| nakamoto_2008_bitcoin.txt | 25643 | MIT, as published on bitcoin.org |
| optech_topic_eclipse_attacks.txt | 4382 | CC BY 4.0 (Bitcoin Optech) |
| regtest_run_v1_0_0.json | 38747 | this course's own run record |

## Left out of the wheel (terms of redistribution not clear), and the examples that are recorded instead

- `bitnodes_snapshot_latest.json` (2.7 MB, the Bitnodes census of reachable nodes, 2026-10-15; no terms stated for copying the data): 8 examples (BloomDisabledByDefault, FiltersOverP2P, I2pAndCjdns, ReachableNodesToday, ServiceBitsOfNetwork, SoftwareShare, TorHiddenService, V2DefaultHistory).
- `blockchaincom_blocks_size.json` and `mempool_tip_height.txt` (data of Blockchain.com and mempool.space; no terms stated): HeaderChainSize.
- `heilman_2015_eclipse` (USENIX Security 2015 paper, copyright of the authors/USENIX): EclipseAttack. `apostolaki_2017_hijacking` (IEEE S&P 2017 paper): RoutingAttack.
- `ml_bfd_2016-05_committed_bloom` (a mailing-list post): FilterIdeaPost2016. `bitcoinfibre_org` (a web page): RelayNetworkHistory.
- Note: the 13 recorded examples are the ones counted by the page's standin record (`08-tooling/ch10-page/standin_v1_0_0.json`); the count is 62 - 49. The `bip-0158_testnet-19.json` vectors are shipped (BIP 158's licence is BSD-2-Clause).
