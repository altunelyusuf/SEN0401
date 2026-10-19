# Chapter 13 page assets - the wheel (v1.3.0)

Adds to ASSETS_PROVENANCE_v1_0_0.md, v1_1_0.md and v1_2_0.md (the story pictures: unchanged, licences there) the one new asset of the chapter 13 page.

## sen0401_ch13_lib-1.1.0-py3-none-any.whl

- sha256 `7a74931ffdad8160485833a3f4f7de89222a482c09f762989346b1d1f793e3d4`, 364954 bytes; written by `08-tooling/ch13-page/pywheels_make_v1_1_0.py` (reproducible: zip dates fixed).
- Holds `sen0401_ch13_lib_v1_0_0.py`, `sen0401_ch10_p2p_v1_0_0.py` (copied byte for byte from 08-tooling) and, in `ch13-evidence`, 36 saved files copied byte for byte. The files are those the worked examples really open (found by running every example once with open() logged, not guessed from the text) AND whose terms clearly allow redistribution.
- 51 of the chapter's 62 worked examples run in the browser over them; 11 are shown as 'Recorded, not run on this page' because they read a file that is NOT in the wheel (below).

| File shipped | Bytes | Licence status |
|---|---|---|
| bip-0032.mediawiki | 28032 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0039.mediawiki | 6842 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0067.mediawiki | 8686 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0093.mediawiki | 45041 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0112.mediawiki | 16727 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0143.mediawiki | 57755 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0174.mediawiki | 136028 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bip-0324.mediawiki | 67644 | the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain) |
| bitcoind_help_31.1.txt | 60324 | MIT (Bitcoin Core) |
| bitcoinwiki_brainwallet.txt | 8696 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_casascius.txt | 8797 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_hardware_wallet.txt | 35826 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_mt_gox.txt | 19173 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_paper_wallet.txt | 11841 | CC BY 3.0 (Bitcoin Wiki) |
| bitcoinwiki_trezor.txt | 9966 | CC BY 3.0 (Bitcoin Wiki) |
| book_ch05_wallets.adoc | 81728 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| book_ch10_network.adoc | 67355 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| book_ch13_security.adoc | 17471 | CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition) |
| core_contrib_guix_README.md | 15290 | MIT (Bitcoin Core) |
| core_doc_descriptors.md | 28143 | MIT (Bitcoin Core) |
| core_doc_external-signer.md | 6448 | MIT (Bitcoin Core) |
| core_doc_managing-wallets.md | 10727 | MIT (Bitcoin Core) |
| core_doc_psbt.md | 5653 | MIT (Bitcoin Core) |
| core_relnotes_26.0.md | 15000 | MIT (Bitcoin Core) |
| core_relnotes_27.0.md | 7034 | MIT (Bitcoin Core) |
| core_src_kernel_chainparams.cpp | 37441 | MIT (Bitcoin Core) |
| core_src_script_descriptor.cpp | 129871 | MIT (Bitcoin Core) |
| core_src_script_interpreter.cpp | 91214 | MIT (Bitcoin Core) |
| core_src_wallet_crypter.h | 4078 | MIT (Bitcoin Core) |
| core_src_wallet_rpc_backup.cpp | 31515 | MIT (Bitcoin Core) |
| core_src_wallet_rpc_encrypt.cpp | 13456 | MIT (Bitcoin Core) |
| core_src_wallet_rpc_wallet.cpp | 42835 | MIT (Bitcoin Core) |
| regtest_run_v1_0_0.json | 12544 | this course's own run record |
| wikipedia_air_gap.txt | 17598 | CC BY-SA (Wikipedia) |
| wikipedia_bitfinex.txt | 29977 | CC BY-SA (Wikipedia) |
| wikipedia_mt_gox.txt | 38345 | CC BY-SA (Wikipedia) |

## Left out of the wheel (terms of redistribution not clear), and the examples that are recorded instead

- `(other)`: 1 example (LostSevenThousand).
- `bip-0068.mediawiki`: 1 example (OlderSixtyFiveThousand).
- `bip39_english.txt`: 1 example (BrainwalletCrackTime).
- `bip39_trezor_vectors.json`: 2 examples (Bip39MnemonicChecksum, Bip39SeedFromWords).
- `bitcoincore_31.1_SHA256SUMS.asc.txt`: 1 example (SignatureNeedsKeys).
- `bitcoincore_31.1_SHA256SUMS.txt`: 1 example (TarballHashMatches).
- `mempool_block_0.json`: 1 example (GenesisHashHardCoded).
- `mempool_block_938343.json`: 1 example (AssumeValidShortcut).
- `shamir_1979_how_to_share_a_secret.txt`: 2 examples (OneShareRevealsNothing, ShamirTwoOfThree).

- Note: the recorded examples are the ones counted by the page's standin record (`08-tooling/ch13-page/standin_v1_1_0.json`). Data from mempool.space and Blockchain.com carries no stated licence; papers, web pages, wallet vendors' pages and any BIP whose header has no License line are not carried because their redistribution terms are not clear to this author; code listings of the book repository (`book_code_*`) are not carried because they have no separately clear licence.
