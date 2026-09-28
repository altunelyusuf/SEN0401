"""SEN0401 chapter 3 (Mastering Bitcoin 3rd edition, Bitcoin Core: The Reference Implementation) for the RDODI build.
Every claim read on 2026-09-29 from the source it cites; every computation executed under Python 3.14.4; the book's
own commands run on the real Bitcoin Core 31.1 release, downloaded, checked against its published checksums and
signatures, and run as an offline node (08-tooling/ch03-evidence/)."""
__version__ = "1.0.0"
CH = 3
DATE = "2026-09-29"
PYVER = "3.14.4"
TITLE = "Bitcoin Core: the reference implementation, run and checked against the book"
QUESTION = "How does chapter 3 of Mastering Bitcoin's 3rd edition take a reader from Bitcoin Core's source to a running full node and its programmatic interface, which of its steps, defaults and printed results still hold on the current release, and what does running the real software show that the book cannot?"
VERSION = "1_0_0"
CQS = ("Which commands, figures and printed results of the chapter can be reproduced by execution on the current release, and what does the execution give?",
       "What in the chapter has changed in Bitcoin Core since the book went to print, and on what source?")
LABELS = {'CMakeBuild': 'CMake build', 'AutotoolsBuild': 'Autotools build', 'JsonRpc': 'JSON-RPC interface',
          'RpcInterface': 'RPC interface', 'BitcoinCommand': 'The bitcoin command', 'ImprovementProposal': 'Bitcoin Improvement Proposal',
          'DatabaseCache': 'Database cache (dbcache)', 'TransactionIndex': 'Transaction index (txindex)',
          'CommandLineClient': 'Command-line client (bitcoin-cli)', 'WrapperLibrary': 'Wrapper library',
          'MerkleRoot': 'Merkle root', 'JsonLdContext': 'JSON-LD context', 'FullNode': 'Full node',
          'ReferenceImplementation': 'Reference implementation', 'ReleaseTag': 'Release tag', 'CookieAuthentication': 'Cookie authentication',
          'DescriptorWallet': 'Descriptor wallet', 'ConfigurationFile': 'Configuration file', 'BlockSubsidy': 'Block subsidy',
          'ReleaseVerification': 'Release verification', 'NodeResources': 'Node resources', 'AlternativeToolkit': 'Alternative toolkit'}
P = "%s"
PUBS = [
 ("P01", "Mastering Bitcoin, 3rd edition - Chapter 3, Bitcoin Core: The Reference Implementation (Antonopoulos and Harding, O'Reilly, 2023; CC BY-SA 4.0; tag third_edition_print1)", "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch03_bitcoin-core.adoc", True),
 ("P02", "Bitcoin Core documentation: doc/build-unix.md at commit 05bc2f5 (Bitcoin Core, 2026)", "https://raw.githubusercontent.com/bitcoin/bitcoin/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940/doc/build-unix.md", False),
 ("P03", "Bitcoin Core 29.0 release notes: the build system migrated from Autotools to CMake (Bitcoin Core, 2026)", "https://raw.githubusercontent.com/bitcoin/bitcoin/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940/doc/release-notes/release-notes-29.0.md", False),
 ("P04", "Bitcoin Core 30.0 release notes: legacy BerkeleyDB wallets removed, the bitcoin command, install layout (Bitcoin Core, 2026)", "https://raw.githubusercontent.com/bitcoin/bitcoin/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940/doc/release-notes/release-notes-30.0.md", False),
 ("P05", "Bitcoin Core 31.0 release notes: the -dbcache default raised to 1024 MiB (Bitcoin Core, 2026)", "https://raw.githubusercontent.com/bitcoin/bitcoin/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940/doc/release-notes/release-notes-31.0.md", False),
 ("P06", "Bitcoin Core 28.0 release notes: the warnings field returned as an array (Bitcoin Core, 2026)", "https://raw.githubusercontent.com/bitcoin/bitcoin/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940/doc/release-notes/release-notes-28.0.md", False),
 ("P07", "Bitcoin Core documentation: doc/files.md, doc/init.md and doc/multiprocess.md at commit 05bc2f5 (Bitcoin Core, 2026)", "https://raw.githubusercontent.com/bitcoin/bitcoin/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940/doc/files.md", False),
 ("P08", "Bitcoin Core source: GetBlockSubsidy in src/validation.cpp at commit 05bc2f5 (Bitcoin Core, 2026)", "https://raw.githubusercontent.com/bitcoin/bitcoin/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940/src/validation.cpp", False),
 ("P09", "Bitcoin Core 31.1 release files, checksums and signatures (Bitcoin Core, 2026), downloaded, verified and run; evidence in 08-tooling/ch03-evidence", "https://bitcoincore.org/bin/bitcoin-core-31.1/", False),
 ("P10", "Bitcoin Core download page and releases page (Bitcoin Core, 2026)", "https://bitcoincore.org/en/download/", False),
 ("P11", "Running a full node, minimum requirements (Bitcoin.org, 2026), the page the owner's notes link", "https://bitcoin.org/en/full-node", False),
 ("P12", "Blockstream Esplora API: blocks 123456 and 775072 and Alice's transaction (Blockstream, 2026), a third party's index of the chain", "https://blockstream.info/api/block/000000000000000000027d39da52dd790d98f85895b02e764611cb7acf552e90", False),
 ("P13", "python-bitcoinlib 0.12.2 on PyPI, released 2023-06-03 (Todd, 2023)", "https://pypi.org/project/python-bitcoinlib/0.12.2/", False),
 ("P14", "Package-registry release data for the toolkits the book lists: npm, PyPI, Go module proxy, crates.io, Maven Central (queried 2026-09-29)", "https://registry.npmjs.org/bcoin", False),
 ("P15", "Bitcoin Core builder signing keys and release signatures, bitcoin-core/guix.sigs (Bitcoin Core, 2026)", "https://github.com/bitcoin-core/guix.sigs", False),
 ("P16", "JSON-LD 1.1, W3C Recommendation, 16 July 2020 (World Wide Web Consortium, 2020)", "https://www.w3.org/TR/json-ld11/", False),
 ("P_NOTES", "Course notes: Chapter_3_BitcoinCore_TheReferenceImplementation.pptx, SEN0401 (then CSE0469) Blockchain, Yusuf Altunel, 2021 - based on Mastering Bitcoin 2nd edition; the owner's file in 03-materials/owner-legacy-2025 (sha256 2264cacbb0c8252c)", "urn:sen0401:course-notes:Chapter_3_BitcoinCore_TheReferenceImplementation.pptx:2264cacbb0c8252c", False),
]
SEC = ("Bitcoin Core: The Reference Implementation", "From Bitcoin to Bitcoin Core", "Bitcoin Development Environment",
       "Compiling Bitcoin Core from the Source Code", "Selecting a Bitcoin Core Release", "Configuring the Bitcoin Core Build",
       "Building the Bitcoin Core Executables", "Running a Bitcoin Core Node", "Configuring the Bitcoin Core Node",
       "Bitcoin Core API", "Getting Information on Bitcoin Core's Status", "Exploring and Decoding Transactions",
       "Exploring Blocks", "Using Bitcoin Core's Programmatic Interface", "Alternative Clients, Libraries, and Toolkits")
CONCEPTS = [("Section", x) for x in SEC] + [("Concept", x) for x in (
    "full verification node", "reference implementation", "Bitcoin Improvement Proposal", "release tag", "release candidate", "bitcoind",
    "bitcoin-cli", "configuration file", "data directory", "prune", "txindex", "dbcache", "blocksonly", "maxmempool", "alertnotify",
    "JSON-RPC", "cookie authentication", "rpcauth", "python-bitcoinlib", "transaction ID", "transaction malleability", "block height",
    "block hash", "confirmations", "median time", "merkle root", "weight units")]
FINDINGS = [
 ("F1", "Background", "Chapter 3 presents Bitcoin Core as the reference implementation and leads a reader from its source to a running full node: selecting a release tag, building bitcoind with autogen.sh, configure and make, running and configuring the node, exploring status, transactions and blocks with bitcoin-cli, and calling the JSON-RPC interface from Python with python-bitcoinlib, before listing alternative libraries.", ["P01"]),
 ("F2", "Contemporary developments", "The build steps the chapter prints have been replaced: Bitcoin Core 29.0 migrated the build from Autotools to CMake, so a current build is cmake -B build, cmake --build build and cmake --install build; the book's --disable-wallet corresponds to -DENABLE_WALLET=OFF, and the graphical client is now opt-in for a source build with -DBUILD_GUI=ON; since 30.0 a bitcoin command starts the node and tools and with -m runs the multiprocess binaries bitcoin-node and bitcoin-gui; the newest release is 31.1.", ["P03", "P02", "P04", "P07", "P10"]),
 ("F3", "Contemporary developments", "Several defaults and outputs the chapter prints have moved: the database cache default rose from 450 to 1024 MiB in 31.0 on machines with at least 4096 MiB of memory; legacy BerkeleyDB wallets can no longer be created or loaded since 30.0, and starting the 31.1 release logs SQLite where the book's log shows Berkeley DB 4.8.30; the 31.1 help gives 300 megabytes as the default mempool limit where the chapter's constrained example sets 150; automatic pruning needs a target of at least 550 MiB and cannot be combined with txindex; the warnings field is an array, not the string the book prints.", ["P05", "P04", "P09", "P06", "P01"]),
 ("F4", "Comparative analysis", "The chapter's examples reproduce on the real 31.1 release: decoding Alice's serialized transaction gives the book's txid, hash, size 194, vsize 143 and weight 569, both outputs and, on a mainnet node, the same two addresses and descriptor checksums; Python over the same hex gives the same txid and wtxid; block 123456's 13 transaction identifiers hash to the Merkle root the book shows, its header hashes to the block hash the book prints and its difficulty follows from its bits; and python-bitcoinlib 0.12.2 on Python 3.14.4 runs the book's rpc_example.py against 31.1 unchanged.", ["P09", "P01", "P12", "P13"]),
 ("F5", "Comparative analysis", "One printed result does not match its script: rpc_block.py reads block 775072, where Core's schedule gives a subsidy of 6.25 bitcoins, yet the text reports 10,322.07722534 BTC including a 25 BTC reward and 0.0909 BTC of fees; the explorer's data for that block's 1,966 transactions sum to 5,863.00566521 BTC, with a coinbase of 6.33799108 that is the 6.25 subsidy plus 0.08799108 in fees, so the printed figure belongs to another block. The chapter's own suggestion to compare with a block explorer would expose it.", ["P01", "P08", "P12"]),
 ("F6", "Comparative analysis", "Resource figures differ by source and year: the chapter says over 500 GB at first and about 400 MB a day in 2023, which is about 12 GB a month; the download page now says about 600 GB plus 5 to 10 GB a month and pruning to as little as 10 GB; the bitcoin.org page the owner's notes link lists about 740 GB for the first start and about 20 GB a month, so the figures are orders of magnitude to be re-read where the software is downloaded.", ["P01", "P10", "P11", "P_NOTES"]),
 ("F7", "Comparative analysis", "The chapter's toolkit list has aged unevenly: registries show releases in 2026 for bitcoinjs-lib, btcd, the Rust bitcoin crate, pycoin and bitcoinj; python-bitcoinlib's latest release 0.12.2 dates from June 2023 and its documentation says its RPC interface should work with Bitcoin Core 24.0 or later, which the run above confirms for 31.1; the bcoin package's latest release on npm is from July 2018.", ["P14", "P13"]),
 ("F8", "Comparative analysis", "A download of the current release can be checked before it is run: the Linux tarball's SHA-256 equals the value in the release's SHA256SUMS, and that file carries 11 good PGP signatures from builder keys held in the guix.sigs repository; this shows the download matches the published record, and it does not establish trust in the keys, which the check took from the same repository.", ["P09", "P15"]),
 ("F9", "Course notes", "The owner's course notes for this chapter (2021, after the 2nd edition; mostly slide titles over screenshots of the book) add three topics beyond the book's flow, each checked here: the wallet in Bitcoin Core, which the 3rd edition defers to chapter 5 and which the current release keeps in SQLite as a descriptor wallet; the graphical client and the Windows instructions, which the 31.1 release still ships as bitcoin-qt and a win64 installer; and the minimum-requirements page, whose figures now differ from the book's (see the resource finding).", ["P_NOTES", "P09", "P11", "P01"]),
 ("F10", "Conclusion", "For the course theme, a full node's answers are authoritative because the node verified them, the property that provenance records try to describe, and the JSON that Bitcoin Core returns can be given a meaning as linked data: JSON-LD 1.1 is the W3C's JSON-based format to serialize Linked Data, designed to integrate with systems that already use JSON.", ["P01", "P16"]),
]
TAX = [
 ("Node", "Verification", "FullNode", "a node that verifies every rule", "A full verification node checks every confirmed transaction against every rule of the system, so that what it reports is authoritative because it was independently verified.", None),
 ("Node", "Verification", "ReferenceImplementation", "Bitcoin Core", "Bitcoin Core is the reference implementation: it provides a reference for how each part of the technology should be implemented.", None),
 ("Node", "Verification", "ImprovementProposal", "BIP9", "Most major parts of the system since 2011 are documented in Bitcoin Improvement Proposals, referred to by number.", None),
 ("Node", "NodeResources", "InitialDownload", "the first synchronization", "A new node downloads and validates the whole chain before it can process transactions, and a node that was off for ten days downloads about four gigabytes at 400 megabytes a day.", ("400 * 10 / 1000", "4.0")),
 ("Node", "NodeResources", "PrunedNode", "a node that deletes old blocks", "A pruned node deletes old blocks to reduce disk use while still downloading and verifying the whole chain; automatic pruning needs a target of at least 550 MiB.", None),
 ("Build", "Source", "ReleaseTag", "git checkout v24.0.1", "A release tag marks a snapshot of the source by version number; release candidates carry the suffix rc and stable releases none.", None),
 ("Build", "Toolchain", "AutotoolsBuild", "autogen.sh, configure and make", "The book builds bitcoind with autogen.sh, configure and make, options such as --disable-wallet and --with-gui=no shaping the build; Bitcoin Core replaced this with CMake.", None),
 ("Build", "Toolchain", "CMakeBuild", "cmake -B build", "A current build is cmake -B build, cmake --build build and cmake --install build, with options such as -DENABLE_WALLET=OFF and -DBUILD_GUI=ON.", None),
 ("Build", "Toolchain", "BitcoinCommand", "bitcoin -m node", "The bitcoin command is a front door to the node and tools, and its -m option runs the multiprocess binaries instead of the monolithic ones.", None),
 ("Operation", "Configuration", "ConfigurationFile", "bitcoin.conf in the data directory", "Bitcoin Core reads bitcoin.conf from its data directory at every start; options can also be given on the command line, and bitcoind -printtoconsole shows where the file is.", None),
 ("Operation", "Configuration", "DatabaseCache", "dbcache", "The dbcache option sizes the cache of the unspent-output set: 450 MiB by default in the book, 1024 MiB by default from Bitcoin Core 31.0 on machines with enough memory.", None),
 ("Operation", "Configuration", "TransactionIndex", "txindex=1", "The txindex option builds an index of every transaction so that getrawtransaction can find any of them; it cannot be combined with pruning.", None),
 ("Operation", "Wallet", "DescriptorWallet", "the SQLite wallet", "The current default wallet is a descriptor wallet stored in SQLite; legacy BerkeleyDB wallets can no longer be created or loaded and can only be migrated.", None),
 ("Interface", "RpcInterface", "JsonRpc", "a getblockchaininfo call over HTTP", "Bitcoin Core's API is JSON-RPC over HTTP, by default to 127.0.0.1 on port 8332, so any program that can make an HTTP request can call it.", None),
 ("Interface", "RpcInterface", "CookieAuthentication", "the .cookie file", "By default Bitcoin Core creates a random credential on each start and stores it in the data directory as .cookie, which bitcoin-cli reads; rpcauth.py makes a static credential instead.", None),
 ("Interface", "Client", "CommandLineClient", "bitcoin-cli getblockchaininfo", "The bitcoin-cli helper sends the same calls the API offers, which makes it the way to experiment interactively; its help command lists the available RPC commands.", None),
 ("Interface", "Client", "WrapperLibrary", "python-bitcoinlib's RawProxy", "A wrapper library hides the HTTP call: python-bitcoinlib's RawProxy turns p.getblockchaininfo() into the JSON-RPC request and returns the decoded answer.", None),
 ("Data", "Transaction", "DecodedTransaction", "decoderawtransaction on Alice's transaction", "Decoding the serialized hexadecimal of Alice's payment shows its one input, two outputs, addresses and script types, exactly as the chain holds them.", None),
 ("Data", "Transaction", "TransactionWeight", "569 weight units, 143 virtual bytes", "A transaction's weight counts its non-witness bytes four times and its witness bytes once, and its virtual size is the weight divided by four, rounded up.", ("-(-(4 * 125 + 194 - 125) // 4)", "143")),
 ("Data", "Transaction", "TransactionIdentifier", "txid and hash", "The txid hashes the transaction without its witness and the hash includes it; a txid is not authoritative before confirmation because a transaction can be modified.", None),
 ("Data", "Block", "BlockHeight", "getblockhash 123456", "A block is found by its height, how many blocks precede it, or by its header hash; its confirmations count the blocks built on top, itself included.", ("123456 + 651742 - 1", "775197")),
 ("Data", "Block", "BlockWeight", "weight 16716 for size 4179", "A block without witness data weighs four times its size in weight units, which the getblock result shows as size, strippedsize and weight.", ("4 * 4179", "16716")),
 ("Data", "Block", "MerkleRoot", "the Merkle root of the block's transactions", "The Merkle root in a block header commits to every transaction of the block, and hashing the block's transaction identifiers pairwise up to one value reproduces it.", None),
 ("Data", "Block", "BlockSubsidy", "6.25 bitcoins at height 775072", "The subsidy starts at 50 bitcoins and is shifted right once for every 210,000 blocks, so it is 6.25 bitcoins at height 775072.", ("50 * 10**8 >> (775072 // 210000)", "625000000")),
 ("Data", "Block", "Difficulty", "difficulty from bits 1a6a93b3", "A block's difficulty follows from its bits, the compact form of its target, as the ratio of the easiest target to this block's target.", ("round(0xffff * 256**(0x1d - 3) / (0x6a93b3 * 256**(0x1a - 3)), 10)", "157416.4018436489")),
 ("Ecosystem", "Assurance", "ReleaseVerification", "SHA256SUMS and its signatures", "A downloaded release can be checked against the SHA-256 checksums the project publishes and the signatures on them, which shows the file matches the published record.", None),
 ("Ecosystem", "Assurance", "AlternativeToolkit", "python-bitcoinlib, btcd, bitcoinj", "Libraries, toolkits and full nodes in many languages give native access to Bitcoin, and their upkeep varies, so a listed toolkit's latest release is worth checking.", None),
 ("Semantics", "LinkedData", "VerifiedData", "a node's own verified answer", "Data from your own node is authoritative because the node verified it, the property a provenance record is meant to describe.", None),
 ("Semantics", "LinkedData", "JsonLdContext", "a context that maps JSON keys to IRIs", "JSON-LD is a JSON-based format to serialize Linked Data, so the JSON a node returns can be given a meaning as linked data.", None),
]
S = "Antonopoulos and Harding, 2023"; C = "Bitcoin Core, 2026"; A = "Altunel, 2021"; T = "Todd, 2023"; W = "World Wide Web Consortium, 2020"; X = "Blockstream, 2026"; B = "Bitcoin.org, 2026"
BODY = {
 "Node": "Bitcoin Core: The Reference Implementation begins from the idea that software on your own computer can verify Bitcoin itself, without a third party (%s)." % S,
 "Verification": "From Bitcoin to Bitcoin Core explains what a verifying node is and why Bitcoin Core is the reference for it (%s)." % S,
 "FullNode": "A full verification node verifies every confirmed transaction against every rule, so the data it gives you is authoritative not because a powerful entity designated it so but because your node independently verified it (%s)." % S,
 "ReferenceImplementation": "Bitcoin Core grew out of the first Bitcoin software and is the reference implementation: it provides a reference for how each part of the technology should be implemented, and it implements wallets, validation, block construction and the peer-to-peer protocol (%s)." % S,
 "ImprovementProposal": "The chapter refers to Bitcoin Improvement Proposals by number, for example BIP9 for the mechanism used for several major upgrades, and Bitcoin Core's documentation lists which BIPs it implements and since which version (%s)." % S,
 "NodeResources": "Running a Bitcoin Core Node states what a node costs in disk, bandwidth and time (%s)." % S,
 "InitialDownload": "The book puts the first download at over 500 GB and the growth at about 400 MB a day, so ten days offline means about 4 GB to catch up; the download page now says about 600 GB plus 5 to 10 GB a month (%s)." % C,
 "PrunedNode": "Pruning keeps a node within a disk budget by deleting old blocks, and the current help says automatic pruning needs a target of at least 550 MiB and is incompatible with txindex, where the book's constrained example uses 5000 (%s)." % C,
 "Build": "Compiling Bitcoin Core from the Source Code takes a reader from the repository to installed executables (%s)." % S,
 "Source": "The reader clones the repository and then selects a release rather than building the newest, possibly unstable, code (%s)." % S,
 "ReleaseTag": "The book checks out the tag v24.0.1, then the highest release; the releases page now lists 31.1 as the newest (%s)." % C,
 "Toolchain": "Configuring the Bitcoin Core Build and Building the Bitcoin Core Executables give the commands that turn the source into bitcoind (%s)." % S,
 "AutotoolsBuild": "The book generates the build scripts with autogen.sh, runs configure with options such as --disable-wallet, --with-gui=no and --with-incompatible-bdb, and then make, make check and make install (%s)." % S,
 "CMakeBuild": "Bitcoin Core 29.0 migrated its build system from Autotools to CMake, so the build is cmake -B build, cmake --build build and cmake --install build, with -DENABLE_WALLET=OFF for no wallet and -DBUILD_GUI=ON for the graphical client (%s)." % C,
 "BitcoinCommand": "Since 30.0 a bitcoin command starts the node with bitcoin node, calls RPC with bitcoin rpc and, with -m, runs the multiprocess binaries bitcoin-node and bitcoin-gui instead of bitcoind and bitcoin-qt (%s)." % C,
 "Operation": "Configuring the Bitcoin Core Node covers the settings that decide how a node behaves and what it stores (%s)." % S,
 "Configuration": "The configuration file and its options, of which the book says there are more than 100, shape the node; the 31.1 help lists 139 in its default listing (%s)." % C,
 "ConfigurationFile": "Bitcoin Core looks for bitcoin.conf in its data directory on every start, and running bitcoind -printtoconsole shows the path on its first lines, as the 31.1 startup log does (%s)." % C,
 "DatabaseCache": "The book gives the dbcache default as 450 MiB; Bitcoin Core 31.0 raised it to 1024 MiB on systems where at least 4096 MiB of memory is detected, and dbcache=450 restores the old behaviour (%s)." % C,
 "TransactionIndex": "By default a node indexes only the transactions of its own wallet; setting txindex=1 builds a complete index so that getrawtransaction can find any transaction (%s)." % S,
 "Wallet": "The chapter's startup log shows the wallet database in use, which is where the current release differs (%s)." % S,
 "DescriptorWallet": "Legacy BerkeleyDB wallets can no longer be created or loaded since Bitcoin Core 30.0 and can be migrated with the migratewallet RPC, and the 31.1 release creates a descriptor wallet whose format is sqlite (%s)." % C,
 "Interface": "Bitcoin Core API introduces the programmatic interface that the rest of the book uses (%s)." % S,
 "RpcInterface": "Using Bitcoin Core's Programmatic Interface explains what the API is and how a program reaches it (%s)." % S,
 "JsonRpc": "The API is JSON-RPC over HTTP: curl posts a jsonrpc request for a method such as getblockchaininfo to 127.0.0.1 on the default port 8332 (%s)." % S,
 "CookieAuthentication": "Bitcoin Core creates a random credential at each start and stores it as .cookie in the data directory, deleted on shutdown, and the rpcauth.py script in the source's share directory makes a static credential (%s)." % C,
 "Client": "The bitcoin-cli helper and a wrapper library are the two ways the chapter calls the API (%s)." % S,
 "CommandLineClient": "The bitcoin-cli help command lists the RPC commands, and getblockchaininfo, getmempoolinfo, getnetworkinfo and getwalletinfo report the node's status (%s)." % S,
 "WrapperLibrary": "The book uses python-bitcoinlib, which is not part of Bitcoin Core, to call the API from Python, and its documentation says the RPC interface should work with Bitcoin Core 24.0 or later (%s)." % T,
 "Data": "Exploring and Decoding Transactions and Exploring Blocks read the chain through the API (%s)." % S,
 "Transaction": "The chapter retrieves Alice's payment from chapter 2 by its transaction ID and decodes it (%s)." % S,
 "DecodedTransaction": "The getrawtransaction command returns the serialized transaction in hexadecimal and decoderawtransaction shows its parts: one input and two outputs, the payment to Bob and the change back to Alice (%s)." % S,
 "TransactionWeight": "The decoded transaction reports size 194, vsize 143 and weight 569, and 143 is 569 divided by four rounded up (%s)." % S,
 "TransactionIdentifier": "A tip in the chapter warns that a txid is not authoritative because a transaction can be modified before confirmation, and the decoded result gives both the txid and the hash that includes the witness (%s)." % S,
 "Block": "Exploring Blocks finds a block by its height or its hash and reads its fields (%s)." % S,
 "BlockHeight": "getblockhash 123456 returns the header hash of block 123456, and getblock reports 651742 confirmations, the depth of the block and so the difficulty of changing anything in it (%s)." % S,
 "BlockWeight": "The getblock result gives a block's stripped size, its size and its weight, which for block 123456 is 4179, 4179 and 16716 (%s)." % S,
 "MerkleRoot": "The getblock result shows the block's merkle root beside nonce, bits, difficulty and chainwork as the fields used for security and proof of work (%s)." % S,
 "BlockSubsidy": "The chapter says its block total includes a 25 BTC reward, while its script reads block 775072, where Bitcoin Core's own schedule gives 6.25 bitcoins (%s)." % C,
 "Difficulty": "The difficulty of block 123456 is 157416.4018436489, which follows from its bits value 1a6a93b3 (%s)." % S,
 "Ecosystem": "Alternative Clients, Libraries, and Toolkits lists other ways to reach Bitcoin, and running the real release shows what has been checked (%s)." % S,
 "Assurance": "Trust in a download can be tested before the software is run (%s)." % C,
 "ReleaseVerification": "The 31.1 Linux tarball's SHA-256 equals the value in the release's SHA256SUMS, and that file carries 11 good signatures from builder keys held in the guix.sigs repository, which does not itself establish trust in those keys (%s)." % C,
 "AlternativeToolkit": "The book lists toolkits by language, from bcoin, Bitcore and BitcoinJS to btcd, rust-bitcoin, bitcoin-s and NBitcoin, and registry data show that their upkeep varies, with the bcoin package's latest npm release dating from 2018 (%s)." % S,
 "Semantics": "The course theme of semantic technologies meets the chapter in the authority of a node's own data and in the format it returns (%s)." % W,
 "LinkedData": "A node's answers are JSON, and the W3C's JSON-LD 1.1 turns JSON into Linked Data (%s)." % W,
 "VerifiedData": "Data that your own node verified is authoritative for a reason that can be stated, which is what a provenance record does for any dataset (%s)." % S,
 "JsonLdContext": "JSON-LD 1.1 is a JSON-based format to serialize Linked Data whose syntax is designed to integrate into systems that already use JSON, such as the answers of getblock (%s)." % W,
}
# long computations, executed by the checks against the evidence files; the expected value is the repr under Python 3.14.4
_HEX = "open('08-tooling/ch03-evidence/alice_tx_hex_book_v1_0_0.txt').read().strip()"
_DEC = "__import__('json').load(open('08-tooling/ch03-evidence/alice_decoded_31_1_v1_0_0.json'))"
_DSHA = "lambda b: __import__('hashlib').sha256(__import__('hashlib').sha256(b).digest()).digest()"
_BLK = "__import__('json').load(open('08-tooling/ch03-evidence/block_775072_outputs_v1_0_0.json'))"
_HDR = "__import__('json').load(open('08-tooling/ch03-evidence/block_123456_header_v1_0_0.json'))"
_TXIDS = ("5b75086dafeede555fc8f9a810d8b10df57c46f9f176ccc3dd8d2fa20edd685b e3d0425ab346dd5b76f44c222a4bb5d16640a4247050ef82462ab17e229c83b4 "
          "137d247eca8b99dee58e1e9232014183a5c5a9e338001a0109df32794cdcc92e 5fd167f7b8c417e59106ef5acfe181b09d71b8353a61a55a2f01aa266af5412d "
          "60925f1948b71f429d514ead7ae7391e0edf965bf5a60331398dae24c6964774 d4d5fc1529487527e9873256934dfb1e4cdcb39f4c0509577ca19bfad6c5d28f "
          "7b29d65e5018c56a33652085dbb13f2df39a1a9942bfe1f7e78e97919a6bdea2 0b89e120efd0a4674c127a76ff5f7590ca304e6a064fbc51adffbd7ce3a3deef "
          "603f2044da9656084174cfb5812feaf510f862d3addcf70cacce3dc55dab446e 9a4ed892b43a4df916a7a1213b78e83cd83f5695f635d535c94b2b65ffb144d3 "
          "dda726e3dad9504dce5098dfab5064ecd4a7650bfe854bb2606da3152b60e427 e46ea8b4d68719b65ead930f07f1f3804cb3701014f8e6d76c4bdbc390893b94 "
          "864a102aeedf53dd9b2baab4eeb898c5083fde6141113e0606b664c41fe15e1f")
_MERKLE = ("import hashlib\nd = lambda b: hashlib.sha256(hashlib.sha256(b).digest()).digest()\n"
           "level = [bytes.fromhex(t)[::-1] for t in %r.split()]\n"
           "while len(level) > 1:\n    if len(level) %% 2: level.append(level[-1])\n    level = [d(level[i] + level[i + 1]) for i in range(0, len(level), 2)]\n"
           "level[0][::-1].hex()" % _TXIDS)
_HEADER = ("import hashlib, json, struct\nb = json.load(open('08-tooling/ch03-evidence/block_123456_header_v1_0_0.json'))\n"
           "h = struct.pack('<I', b['version']) + bytes.fromhex(b['previousblockhash'])[::-1] + bytes.fromhex(b['merkle_root'])[::-1] + struct.pack('<III', b['timestamp'], b['bits'], b['nonce'])\n"
           "hashlib.sha256(hashlib.sha256(h).digest()).digest()[::-1].hex() == b['id'], len(h), b['id']")
_TEXT = lambda f: "open('08-tooling/ch03-evidence/%s').read()" % f
CLAIMS = [
 ("(lambda h, r: h(r[:4] + r[6:-71] + r[-4:])[::-1].hex())(%s, bytes.fromhex(%s))" % (_DSHA, _HEX), "'466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177'"),
 ("(lambda h, r: h(r)[::-1].hex())(%s, bytes.fromhex(%s))" % (_DSHA, _HEX), "'f7cdbc7cf8b910d35cc69962e791138624e4eae7901010a6da4c02e7d238cdac'"),
 ("(lambda d: [d['txid'][:8], d['hash'][:8], d['size'], d['vsize'], d['weight']])(%s)" % _DEC, "['46620030', 'f7cdbc7c', 194, 143, 569]"),
 ("(lambda d: [o['scriptPubKey']['address'] for o in d['vout']])(%s)" % _DEC, "['bc1p8dqa4wjvnt890qmfws83te0v3qxzsfu7ul63kp7u56w8qc0qwp5qv995qn', 'bc1qwafvze0200nh9vkq4jmlf4sy0tn0ga5w0zpkpg']"),
 ("(lambda d: [o['scriptPubKey']['desc'][-9:] for o in d['vout']])(%s)" % _DEC, "['#38d6v6ev', '#qq404gts']"),
 ("(lambda d: [o['value'] for o in d['vout']])(%s)" % _DEC, "[0.0002, 0.00075]"),
 (_MERKLE, "'0e60651a9934e8f0decd1c5fde39309e48fca0cd1c84a21ddfde95033762d86c'"),
 (_HEADER, "(True, 80, '0000000000002917ed80650c6174aac8dfc46f5fe36480aaef682ff6cd83c3ca')"),
 ("0x1a6a93b3 == %s['bits']" % _HDR, "True"),
 ("%s['previousblockhash'].endswith('60bc96a44724fd72daf9b92cf8ad00510b5224c6253ac40095')" % _HDR, "True"),
 ("sum(sum(t['out_sat']) for t in %s['txs']) / 10**8" % _BLK, "5863.00566521"),
 ("sum((%s)['txs'][0]['out_sat'])" % _BLK, "633799108"),
 ("sum(t['fee_sat'] or 0 for t in (%s)['txs'][1:])" % _BLK, "8799108"),
 ("50 * 10**8 >> (775072 // 210000)", "625000000"),
 ("sum((%s)['txs'][0]['out_sat']) == (50 * 10**8 >> (775072 // 210000)) + sum(t['fee_sat'] or 0 for t in (%s)['txs'][1:])" % (_BLK, _BLK), "True"),
 ("len((%s)['txs'])" % _BLK, "1966"),
 ("%s['bestblockhash'].endswith('19d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')" % "__import__('json').load(open('08-tooling/ch03-evidence/getblockchaininfo_31_1_v1_0_0.json'))", "True"),
 ("(lambda d: (type(d['warnings']).__name__, d['chain']))(__import__('json').load(open('08-tooling/ch03-evidence/getblockchaininfo_31_1_v1_0_0.json')))", "('list', 'main')"),
 ("(lambda d: (d['version'], d['subversion'], d['protocolversion'], 'P2P_V2' in d['localservicesnames']))(__import__('json').load(open('08-tooling/ch03-evidence/getnetworkinfo_31_1_v1_0_0.json')))", "(310100, '/Satoshi:31.1.0/', 70016, True)"),
 ("__import__('re').search(r'-dbcache=<n>\\s+Maximum database cache size <n> MiB \\(minimum 4, default: (\\d+)\\)', %s).group(1)" % _TEXT("help_bitcoind_31_1_v1_0_0.txt"), "'1024'"),
 ("__import__('re').search(r'-maxmempool=<n>\\s+Keep the transaction memory pool below <n> megabytes \\(default: (\\d+)\\)', %s).group(1)" % _TEXT("help_bitcoind_31_1_v1_0_0.txt"), "'300'"),
 ("'>=550 =' in ' '.join(%s.split())" % _TEXT("help_bitcoind_31_1_v1_0_0.txt"), "True"),
 ("'incompatible with -txindex' in ' '.join(%s.split())" % _TEXT("help_bitcoind_31_1_v1_0_0.txt"), "True"),
 ("sum(1 for l in %s.splitlines() if l.startswith('  -'))" % _TEXT("help_bitcoind_31_1_v1_0_0.txt"), "139"),
 ("(lambda t: ('SQLite' in t, 'Berkeley' in t))(%s)" % _TEXT("startup_31_1_v1_0_0.log"), "(True, False)"),
 ("__import__('json').load(open('08-tooling/ch03-evidence/getwalletinfo_31_1_v1_0_0.json'))['format']", "'sqlite'"),
 ("'no longer possible to create a legacy wallet' in %s" % _TEXT("createwallet_legacy_31_1_v1_0_0.txt"), "True"),
 ("%s.splitlines()[0]" % _TEXT("rpc_example_output_31_1_v1_0_0.txt"), "'0'"),
 ("(lambda L: L[0] == L[1])([l.split()[0] for l in %s.splitlines() if l.strip().endswith('.tar.gz')])" % _TEXT("release_check_31_1_v1_0_0.txt"), "True"),
 ("'good signatures on SHA256SUMS: 11' in %s" % _TEXT("release_check_31_1_v1_0_0.txt"), "True"),
 ("'Prune mode is incompatible with -txindex' in %s" % _TEXT("prune_txindex_31_1_v1_0_0.txt"), "True"),
 ("400 * 30 / 1000", "12.0"),
]
BEH = [
 ("the virtual size is the weight divided by four, rounded up", "print(-(-569 // 4), 569 / 4)", "143 142.25"),
 ("a Merkle level with an odd number of hashes pairs the last one with itself", "L = [1, 2, 3]\nif len(L) % 2: L.append(L[-1])\nprint([(L[i], L[i + 1]) for i in range(0, len(L), 2)])", "[(1, 2), (3, 3)]"),
]
