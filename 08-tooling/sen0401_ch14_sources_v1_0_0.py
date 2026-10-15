#!/usr/bin/env python3
"""SEN0401 chapter 14 (Second-Layer Applications): the source table. One row per source opened: (id, author-year, label, url, saved file, role).
The saved copies live in ch14-evidence (fetched by sen0401_ch14_fetch_v1_0_0.py, which writes sources_index_v1_0_0.json with the HTTP status, size and sha256 of each);
the passages used from each are re-read from the saved copy by sen0401_ch14_quotes_v1_0_0.QUOTES, which the chapter's claims execute."""
__version__ = "1.0.0"
GH = "https://raw.githubusercontent.com/"
BOOK_C = "275c4eb8eab8800c6adc39f8def8e8f8fa356a57"      # the commit the textbook ontology pins; its chapter files equal tag third_edition_print1 (6d1c26e1)
CORE_C = "9be056a8a72b624dae9623b2f7bded92c2a21c91"      # tag v31.1 of bitcoin/bitcoin
LND_T = "v0.21.3-beta"
AH, BC = "Antonopoulos and Harding, 2023", "Bitcoin Core, 2026"
BCD = "Bitcoin Core developers"
LD = "Lightning developers, 2026"
LL = "Lightning Labs, 2026"
OT = "Bitcoin Optech, 2026"
WP = "Wikipedia contributors, 2026"
BW = "Bitcoin Wiki, 2026"
MS = "Mempool Space, 2026"
book = lambda f: GH + "bitcoinbook/bitcoinbook/" + BOOK_C + "/" + f
core = lambda f: GH + "bitcoin/bitcoin/" + CORE_C + "/" + f
bip = lambda n, ext="mediawiki": GH + "bitcoin/bips/master/bip-%04d.%s" % (n, ext)
bolt = lambda f: GH + "lightning/bolts/master/" + f
lnd = lambda f: GH + "lightningnetwork/lnd/" + LND_T + "/" + f
wp = lambda t: "https://en.wikipedia.org/w/index.php?title=%s&action=render" % t
wb = lambda t: "https://en.bitcoin.it/wiki/" + t
OTP = lambda t: "https://bitcoinops.org/en/topics/%s/" % t
S = [
 ("P01", AH, "Mastering Bitcoin, 3rd edition - Chapter 14, Second-Layer Applications (Antonopoulos and Harding, 2023; O'Reilly; CC BY-SA 4.0; commit 275c4eb8, equal to tag third_edition_print1)", book("ch14_applications.adoc"), "book_ch14_applications.adoc", "primary"),
 ("P02", AH, "Mastering Bitcoin, 3rd edition - Chapter 6, Transactions: timelocks and the sequence field (Antonopoulos and Harding, 2023)", book("ch06_transactions.adoc"), "book_ch06_transactions.adoc", "secondary"),
 ("P03", AH, "Mastering Bitcoin, 3rd edition - Chapter 7, Authorization and Authentication: scripts, multisignature, CLTV, CSV and pay to contract (Antonopoulos and Harding, 2023)", book("ch07_authorization-authentication.adoc"), "book_ch07_authorization-authentication.adoc", "secondary"),
 ("P04", AH, "Mastering Bitcoin, 3rd edition - Chapter 8, Digital Signatures: SIGHASH types (Antonopoulos and Harding, 2023)", book("ch08_signatures.adoc"), "book_ch08_signatures.adoc", "secondary"),
 ("P05", AH, "Mastering Bitcoin, 3rd edition - Chapter 9, Fees (Antonopoulos and Harding, 2023)", book("ch09_fees.adoc"), "book_ch09_fees.adoc", "secondary"),
 ("P06", AH, "Mastering Bitcoin, 3rd edition - Chapter 10, The Bitcoin Network (Antonopoulos and Harding, 2023)", book("ch10_network.adoc"), "book_ch10_network.adoc", "secondary"),
 ("P07", AH, "Mastering Bitcoin, 3rd edition - Appendix B, the errata of the book (Antonopoulos and Harding, 2023)", book("appb_errata.adoc"), "book_appb_errata.adoc", "secondary"),
 ("P08", AH, "Mastering Bitcoin, 3rd edition - Glossary (Antonopoulos and Harding, 2023)", book("glossary.asciidoc"), "book_glossary.asciidoc", "secondary"),
 ("P09", AH, "Mastering Bitcoin, 3rd edition - Chapter 12, Mining and Consensus, whose source file begins with the anchor [[mining]] (Antonopoulos and Harding, 2023)", book("ch12_mining.adoc"), "book_ch12_mining.adoc", "secondary"),
 ("P10", LD, "BOLT 0, Introduction and Index of the Lightning specification (Lightning developers, 2026)", bolt("00-introduction.md"), "bolt00_introduction.md", "secondary"),
 ("P11", LD, "BOLT 1, Base Protocol: messages and the TLV format (Lightning developers, 2026)", bolt("01-messaging.md"), "bolt01_messaging.md", "secondary"),
 ("P12", LD, "BOLT 2, Peer Protocol for Channel Management: opening, updating and closing a channel (Lightning developers, 2026)", bolt("02-peer-protocol.md"), "bolt02_peer_protocol.md", "secondary"),
 ("P13", LD, "BOLT 3, Bitcoin Transaction and Script Formats: funding, commitment and HTLC transactions, with test vectors (Lightning developers, 2026)", bolt("03-transactions.md"), "bolt03_transactions.md", "secondary"),
 ("P14", LD, "BOLT 4, Onion Routing Protocol (Lightning developers, 2026)", bolt("04-onion-routing.md"), "bolt04_onion_routing.md", "secondary"),
 ("P15", LD, "BOLT 4 test vector onion-test.json, the packet for a five-hop route with a variable-length payload (Lightning developers, 2026)", bolt("bolt04/onion-test.json"), "bolt04_onion_test.json", "secondary"),
 ("P16", LD, "BOLT 5, Recommendations for On-chain Transaction Handling: what a node does when a channel closes unilaterally (Lightning developers, 2026)", bolt("05-onchain.md"), "bolt05_onchain.md", "secondary"),
 ("P17", LD, "BOLT 7, P2P Node and Channel Discovery: gossip (Lightning developers, 2026)", bolt("07-routing-gossip.md"), "bolt07_routing_gossip.md", "secondary"),
 ("P18", LD, "BOLT 8, Encrypted and Authenticated Transport, with test vectors (Lightning developers, 2026)", bolt("08-transport.md"), "bolt08_transport.md", "secondary"),
 ("P19", LD, "BOLT 9, Assigned Feature Flags (Lightning developers, 2026)", bolt("09-features.md"), "bolt09_features.md", "secondary"),
 ("P20", LD, "BOLT 11, Invoice Protocol for Lightning Payments, with test vectors (Lightning developers, 2026)", bolt("11-payment-encoding.md"), "bolt11_payment_encoding.md", "secondary"),
 ("P21", LD, "BOLT 12, Flexible Protocol for Lightning Payments (offers) (Lightning developers, 2026)", bolt("12-offer-encoding.md"), "bolt12_offer_encoding.md", "secondary"),
 ("P22", LD, "README of the BOLT repository: who maintains the Lightning specification (Lightning developers, 2026)", bolt("README.md"), "bolt_readme.md", "secondary"),
 ("P23", "Poon and Dryja, 2016", "Joseph Poon and Thaddeus Dryja, The Bitcoin Lightning Network: Scalable Off-Chain Instant Payments, draft version 0.5.9.2, 14 January 2016 (Poon and Dryja, 2016)", "https://lightning.network/lightning-network-paper.pdf", "poon_dryja_lightning_paper.pdf", "secondary"),
 ("P24", "Poon and Dryja, 2015", "Joseph Poon and Thaddeus Dryja, Lightning Network summary slides, the PDF at lightning.network (Poon and Dryja, 2015)", "https://lightning.network/lightning-network-summary.pdf", "poon_dryja_lightning_summary.pdf", "secondary"),
 ("P25", "Danezis and Goldberg, 2009", "George Danezis and Ian Goldberg, Sphinx: A Compact and Provably Secure Mix Format, IEEE Symposium on Security and Privacy, 2009 (Danezis and Goldberg, 2009)", "https://www.cypherpunks.ca/~iang/pubs/Sphinx_Oakland09.pdf", "danezis_goldberg_sphinx_2009.pdf", "secondary"),
 ("P26", "Decker and Wattenhofer, 2015", "Christian Decker and Roger Wattenhofer, A Fast and Scalable Payment Network with Bitcoin Duplex Micropayment Channels, SSS 2015 (Decker and Wattenhofer, 2015)", "https://www.tik.ee.ethz.ch/file/716b955c130e6c703fac336ea17b1670/duplex-micropayment-channels.pdf", "decker_wattenhofer_duplex_2015.pdf", "secondary"),
 ("P27", "Rosenfeld, 2012", "Meni Rosenfeld, Overview of Colored Coins, 4 December 2012 (Rosenfeld, 2012)", "https://bitcoil.co.il/BitcoinX.pdf", "rosenfeld_colored_coins_2012.pdf", "secondary"),
 ("P28", "Todd, 2017", "Peter Todd, Scalable Single-Use-Seal Asset Transfer, 2017 (Todd, 2017)", "https://petertodd.org/2017/scalable-single-use-seal-asset-transfer", "todd_single_use_seals_2017.html", "secondary"),
 ("P29", "Todd, 2014", "BIP 65, OP_CHECKLOCKTIMEVERIFY (Peter Todd, status Final) (Todd, 2014)", bip(65), "bip-0065.mediawiki", "secondary"),
 ("P30", "Friedenbach et al., 2015", "BIP 68, Relative lock-time using consensus-enforced sequence numbers (Friedenbach et al., 2015)", bip(68), "bip-0068.mediawiki", "secondary"),
 ("P31", "BtcDrak et al., 2015", "BIP 112, CHECKSEQUENCEVERIFY (BtcDrak et al., 2015)", bip(112), "bip-0112.mediawiki", "secondary"),
 ("P32", "Lau and Wuille, 2016", "BIP 143, Transaction Signature Verification for Version 0 Witness Program (Lau and Wuille, 2016)", bip(143), "bip-0143.mediawiki", "secondary"),
 ("P33", "Wuille et al., 2020", "BIP 341, Taproot: SegWit version 1 spending rules (Wuille et al., 2020)", bip(341), "bip-0341.mediawiki", "secondary"),
 ("P34", "Wuille et al., 2020", "BIP 341 wallet test vectors, wallet-test-vectors.json (Wuille et al., 2020)", GH + "bitcoin/bips/master/bip-0341/wallet-test-vectors.json", "bip341_wallet_test_vectors.json", "secondary"),
 ("P35", "Decker and Towns, 2017", "BIP 118, SIGHASH_ANYPREVOUT for Taproot Scripts (draft) (Decker and Towns, 2017)", bip(118), "bip-0118.mediawiki", "secondary"),
 ("P36", "Rubin, 2020", "BIP 119, CHECKTEMPLATEVERIFY (draft) (Rubin, 2020)", bip(119), "bip-0119.mediawiki", "secondary"),
 ("P37", "Harding and Todd, 2015", "BIP 125, Opt-in Full Replace-by-Fee Signaling (Harding and Todd, 2015)", bip(125), "bip-0125.mediawiki", "secondary"),
 ("P38", "Zhao, 2024", "BIP 431, Topology Restrictions for Pinning, the TRUC (version 3) transaction rules (Zhao, 2024)", bip(431), "bip-0431.mediawiki", "secondary"),
 ("P39", "Sanders, 2025", "BIP 433, Pay to Anchor (P2A) (Sanders, 2025)", bip(433), "bip-0433.mediawiki", "secondary"),
 ("P40", "Wuille and Maxwell, 2017", "BIP 173, Base32 address format for native v0-16 witness outputs (bech32), the encoding of Lightning invoices (Wuille and Maxwell, 2017)", bip(173), "bip-0173.mediawiki", "secondary"),
 ("P41", OT, "Bitcoin Optech topic: HTLC (Bitcoin Optech, 2026)", OTP("htlc"), "optech_topic_htlc.html", "secondary"),
 ("P42", OT, "Bitcoin Optech topic: Anchor outputs (Bitcoin Optech, 2026)", OTP("anchor-outputs"), "optech_topic_anchor_outputs.html", "secondary"),
 ("P43", OT, "Bitcoin Optech topic: Channel factories (Bitcoin Optech, 2026)", OTP("channel-factories"), "optech_topic_channel_factories.html", "secondary"),
 ("P44", OT, "Bitcoin Optech topic: Multipath payments (Bitcoin Optech, 2026)", OTP("multipath-payments"), "optech_topic_multipath_payments.html", "secondary"),
 ("P45", OT, "Bitcoin Optech topic: Watchtowers (Bitcoin Optech, 2026)", OTP("watchtowers"), "optech_topic_watchtowers.html", "secondary"),
 ("P46", OT, "Bitcoin Optech topic: Splicing (Bitcoin Optech, 2026)", OTP("splicing"), "optech_topic_splicing.html", "secondary"),
 ("P47", OT, "Bitcoin Optech topic: Trampoline payments (Bitcoin Optech, 2026)", OTP("trampoline-payments"), "optech_topic_trampoline_payments.html", "secondary"),
 ("P48", OT, "Bitcoin Optech topic: Offers, BOLT 12 (Bitcoin Optech, 2026)", OTP("offers"), "optech_topic_offers.html", "secondary"),
 ("P49", OT, "Bitcoin Optech topic: PTLCs, point time locked contracts (Bitcoin Optech, 2026)", OTP("ptlc"), "optech_topic_ptlc.html", "secondary"),
 ("P50", OT, "Bitcoin Optech topic: Simple taproot channels (Bitcoin Optech, 2026)", OTP("simple-taproot-channels"), "optech_topic_simple_taproot_channels.html", "secondary"),
 ("P51", OT, "Bitcoin Optech topic: Channel jamming attacks (Bitcoin Optech, 2026)", OTP("channel-jamming-attacks"), "optech_topic_channel_jamming_attacks.html", "secondary"),
 ("P52", OT, "Bitcoin Optech topic: Eltoo / LN-Symmetry (Bitcoin Optech, 2026)", OTP("eltoo"), "optech_topic_eltoo.html", "secondary"),
 ("P53", OT, "Bitcoin Optech topic: Client-side validation (Bitcoin Optech, 2026)", OTP("client-side-validation"), "optech_topic_client_side_validation.html", "secondary"),
 ("P54", OT, "Bitcoin Optech topic: Ephemeral anchors (Bitcoin Optech, 2026)", OTP("ephemeral-anchors"), "optech_topic_ephemeral_anchors.html", "secondary"),
 ("P55", OT, "Bitcoin Optech topic: Dual funding (Bitcoin Optech, 2026)", OTP("dual-funding"), "optech_topic_dual_funding.html", "secondary"),
 ("P56", BW, "Bitcoin Wiki, Payment channels (Bitcoin Wiki, 2026)", wb("Payment_channels"), "bitcoinwiki_payment_channels.html", "secondary"),
 ("P57", BW, "Bitcoin Wiki, Contract, with the rapidly-adjusted payments of Mike Hearn and Jeremy Spilman (Bitcoin Wiki, 2026)", wb("Contract"), "bitcoinwiki_contract.html", "secondary"),
 ("P58", BW, "Bitcoin Wiki, Colored Coins (Bitcoin Wiki, 2026)", wb("Colored_Coins"), "bitcoinwiki_colored_coins.html", "secondary"),
 ("P59", BW, "Bitcoin Wiki, Lightning Network (Bitcoin Wiki, 2026)", wb("Lightning_Network"), "bitcoinwiki_lightning_network.html", "secondary"),
 ("P60", BW, "Bitcoin Wiki, Hashed Timelock Contracts (Bitcoin Wiki, 2026)", wb("Hashed_Timelock_Contracts"), "bitcoinwiki_htlc.html", "secondary"),
 ("P61", BW, "Bitcoin Wiki, Laszlo Hanyecz (Bitcoin Wiki, 2026)", wb("Laszlo_Hanyecz"), "bitcoinwiki_laszlo_hanyecz.html", "secondary"),
 ("P62", BW, "Bitcoin Wiki, Timelock (Bitcoin Wiki, 2026)", wb("Timelock"), "bitcoinwiki_timelock.html", "secondary"),
 ("P63", "Hanyecz, 2010", "Laszlo Hanyecz, Pizza for bitcoins?, thread 137 of the Bitcoin Forum, 18 May 2010 (Hanyecz, 2010)", "https://bitcointalk.org/index.php?topic=137.0", "bitcointalk_pizza_137.html", "secondary"),
 ("P64", "Nolan, 2013", "Tier Nolan, Alt chains and atomic transfers, Bitcoin Forum thread 193281, 2013 (Nolan, 2013)", "https://bitcointalk.org/index.php?topic=193281.msg2224949", "bitcointalk_atomic_193281.html", "secondary"),
 ("P65", WP, "Wikipedia, Lightning Network (Wikipedia contributors, 2026)", wp("Lightning_Network"), "wikipedia_lightning_network.html", "secondary"),
 ("P66", WP, "Wikipedia, Onion routing (Wikipedia contributors, 2026)", wp("Onion_routing"), "wikipedia_onion_routing.html", "secondary"),
 ("P67", WP, "Wikipedia, Cryptocurrency, the page to which Atomic swap redirects, with its passage on atomic swaps (Wikipedia contributors, 2026)", wp("Atomic_swap"), "wikipedia_atomic_swap.html", "secondary"),
 ("P68", WP, "Wikipedia, Bitcoin, with the passage on the first retail purchase of goods for bitcoin on 22 May 2010 (Wikipedia contributors, 2026)", wp("Bitcoin_Pizza_Day"), "wikipedia_history_of_bitcoin.html", "secondary"),
 ("P69", WP, "Wikipedia, Micropayment (Wikipedia contributors, 2026)", wp("Micropayment"), "wikipedia_micropayment.html", "secondary"),
 ("P70", WP, "Wikipedia, Noise Protocol Framework (Wikipedia contributors, 2026)", wp("Noise_Protocol_Framework"), "wikipedia_noise_protocol.html", "secondary"),
 ("P71", LL, "lnd " + LND_T + ", release notes of 0.21.0 (Lightning Labs, 2026)", lnd("docs/release-notes/release-notes-0.21.0.md"), "lnd_relnotes_0.21.0.md", "secondary"),
 ("P72", LL, "lnd " + LND_T + ", sample-lnd.conf: the default values of the node (Lightning Labs, 2026)", lnd("sample-lnd.conf"), "lnd_sample_lnd.conf.txt", "secondary"),
 ("P73", LL, "lnd " + LND_T + ", release manifest with the sha256 of the linux-amd64 archive (Lightning Labs, 2026)", "https://github.com/lightningnetwork/lnd/releases/download/" + LND_T + "/manifest-" + LND_T + ".txt", "lnd_manifest.txt", "secondary"),
 ("P74", LL, "Lightning Labs documentation: Taproot Assets (Lightning Labs, 2026)", "https://docs.lightning.engineering/the-lightning-network/taproot-assets", "lightning_engineering_taproot_assets.html", "secondary"),
 ("P75", "RGB developers, 2026", "RGB, smart contracts for Bitcoin and Lightning, rgb.tech (RGB developers, 2026)", "https://rgb.tech/", "rgb_tech.html", "secondary"),
 ("P76", BC, "Bitcoin Core at v31.1: doc/policy/packages.md, package relay and package RBF (Bitcoin Core, 2026)", core("doc/policy/packages.md"), "core_doc_policy_packages.md", "secondary"),
 ("P77", BCD + ", 2024", "Bitcoin Core release notes 28.0: TRUC (v3) transactions, pay to anchor, package relay (Bitcoin Core developers, 2024)", core("doc/release-notes/release-notes-28.0.md"), "core_relnotes_28.0.md", "secondary"),
 ("P78", BCD + ", 2026", "Bitcoin Core 31.1 command line help, bitcoind -help and -help-debug, run on the binary (Bitcoin Core developers, 2026)", "local:bitcoind-help", "bitcoind_help_31.1.txt", "secondary"),
 ("P79", MS, "mempool.space, Lightning Network statistics, JSON, fetched 2026-10-15 (Mempool Space, 2026)", "https://mempool.space/api/v1/lightning/statistics/latest", "mempool_lightning_statistics.json", "secondary"),
 ("P80", MS, "mempool.space, the height of the mainnet tip, fetched 2026-10-15 (Mempool Space, 2026)", "https://mempool.space/api/blocks/tip/height", "mempool_tip_height.txt", "secondary"),
 ("P81", "Core Lightning developers, 2026", "Core Lightning README, the Blockstream implementation (Core Lightning developers, 2026)", GH + "ElementsProject/lightning/master/README.md", "cln_readme.md", "secondary"),
 ("P82", "ACINQ, 2026", "Eclair README, the ACINQ implementation (ACINQ, 2026)", GH + "ACINQ/eclair/master/README.md", "eclair_readme.md", "secondary"),
 ("P83", "Spiral, 2026", "Lightning Development Kit (rust-lightning) README (Spiral, 2026)", GH + "lightningdevkit/rust-lightning/main/README.md", "ldk_readme.md", "secondary"),
]
