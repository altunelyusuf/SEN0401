"""SEN0401 chapter 11: the teaching paragraphs of the leaves of subject 6 (the test blockchains) and the introductions of the subjects and the six sections. One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run or recomputed, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
D = {}

D["SeveralChainsExist"] = (
 "There is not one Bitcoin blockchain but several: the main chain created on 3 January 2009 is called mainnet, and the book names three more that exist for testing, testnet, signet and regtest (Antonopoulos and Harding, 2023). "
 "Bitcoin Core 31.1 lists the chains main, test, testnet4, signet and regtest in the help of the option -chain, and the nodes of this chapter started on each of them reported genesis hashes that equal the ones the code rebuilt from chainparams.cpp: 000000000933ea01... for testnet3, 00000000da84f2ba... for testnet4, 00000008819873e9... for signet and 0f9188f1... for regtest (Bitcoin Core, 2026); (Bitcoin Core developers, 2026). "
 "Each chain has its own genesis block, its own message-start bytes on the network and its own data directory, so the chains cannot be mixed up. "
 "It is like the different currencies in a board game: the notes look alike, but the ones from the box of one game are not accepted in the box of another.")

D["AddressPrefixes"] = (
 "The test chains use other address prefixes than mainnet so that nobody sends real coins to a test address by mistake (Antonopoulos and Harding, 2023). "
 "In the source the base58 prefixes are 0 and 5 on mainnet (addresses starting with 1 and 3) and 111 and 196 on the test chains (starting with m or n, and with 2), while the bech32 prefix is bc on mainnet, tb on testnet3, testnet4 and signet, and bcrt on regtest (Bitcoin Core, 2026). "
 "The nodes of this chapter produced exactly these: legacy addresses beginning with m, script addresses with 2, tb1q for segwit and tb1p for taproot on testnet4 and signet, and bcrt1q and bcrt1p on regtest. "
 "The book's tip lists m, n and tb1 and so leaves out the prefix 2 of script addresses and the bcrt1 of regtest, which its own regtest listing uses a few pages later (Antonopoulos and Harding, 2023). "
 "The prefix is like the country code of a telephone number: you know at once that the number is not for a local call.")

D["DataDirectories"] = (
 "Bitcoin Core keeps each chain apart in its own subdirectory of the data directory, so that a developer can run mainnet and a test chain on one machine: regtest, testnet3, testnet4 and signet, with the main chain in the directory itself (Bitcoin Core, 2026). "
 "The nodes of the run reported the data directories regtest, testnet4, signet and testnet3, matching the book's examples for testnet3 and regtest, and each chain has its own default port: 8333 for mainnet, 18333 for testnet3, 48333 for testnet4, 38333 for signet and 18444 for regtest (Antonopoulos and Harding, 2023); (Bitcoin Core developers, 2026). "
 "Separate directories and ports mean that a mistake with one chain cannot damage another. "
 "It is like having a separate drawer in the kitchen for each kind of cutlery: the knives are all in the house, but you do not reach for them when you want a spoon.")

D["AssumedChainSizes"] = (
 "The book says that testnet3 was a large blockchain, in excess of 30 GB in 2023, and that the default signet was about a gigabyte in size, with a listing showing size_on_disk 769,525,915 bytes (Antonopoulos and Harding, 2023). "
 "Bitcoin Core keeps an estimate of each chain's size for the warning about free disk space, and in the release 31.1 source the estimates are 856 GB for mainnet, 245 GB for testnet3, 31 GB for testnet4 and 24 GB for the default signet (Bitcoin Core, 2026). "
 "These figures are approximate, but they show that testnet3 is about eight times larger than the book's lower bound and that the signet has grown to about 31 times the size in the book's listing, as one would expect from the chain having more than doubled in blocks. "
 "A test chain called light can therefore need a lot of disk space, and the cheapest test environment remains regtest, which starts at zero. "
 "It is like a spare room that was meant to hold a few boxes and now holds the stock of a shop.")

D["Testnet3StillThere"] = (
 "The book says that the current testnet is testnet3, restarted in February 2011 to reset the difficulty (Antonopoulos and Harding, 2023). "
 "Bitcoin Core 31.1 still starts it with the option -testnet, reporting the chain name test and the data directory testnet3, and the chain created on 2011-02-02 stood on 2026-10-15 at height 5,189,394, but the help text of the option says that support for testnet3 is deprecated and will be removed in an upcoming release, and recommends testnet4 (Bitcoin Core developers, 2026); (Mempool Space, 2026). "
 "Release 28.0 had already announced the intention to phase testnet3 out (Bitcoin Core developers, 2024). "
 "So the book's sentence is still true of the code but no longer of the advice. "
 "It is like an old road that is still on the map and drivable, with a sign at the entrance telling you to take the new bypass.")

D["Testnet4Replaces"] = (
 "Testnet4 is the replacement for testnet3, specified in BIP 94 by Fabian Jahr, assigned on 2024-05-27 and now Deployed, and supported in Bitcoin Core since release 28.0 with the option -testnet4 (Jahr, 2024); (Bitcoin Core developers, 2024). "
 "Its genesis block carries the message 03/May/2024 followed by a 64-digit hexadecimal number in the form of a block hash, has the hash 00000000da84f2ba..., the time 2024-05-03 23:11:00 UTC, and the chain stood on 2026-10-15 at height 156,618, where testnet3 had 5,189,394 (Bitcoin Core, 2026); (Mempool Space, 2026). "
 "Optech reports that the testnet is a testing network included with Bitcoin Core and supported by many other programs, with testnet4 a recently started replacement (Bitcoin Optech, 2026). "
 "A new test chain is like a new notebook after the old one has been scribbled all over: the same pen, a clean page.")

D["TestnetMinimumDifficulty"] = (
 "The book says that testnet's minimum difficulty is half that of Bitcoin and that a block may be mined at the minimum difficulty if its timestamp is more than 20 minutes after the previous one (Antonopoulos and Harding, 2023). "
 "The second half is right in the code: in pow.cpp a testnet block whose time is later than the previous block's time plus 2 x nPowTargetSpacing, 2 x 10 minutes, must use the minimum difficulty, and the flag is true for testnet3, testnet4 and regtest and false for mainnet and signet (Bitcoin Core, 2026). "
 "The first half does not show in chainparams.cpp, where mainnet and testnet3 have the same powLimit 00000000ffff...; the sentence matches the Bitcoin Wiki, which says that the minimum difficulty of 1.0 on testnet equals 0.5 on mainnet, but the code gives no support for such a factor (Bitcoin Wiki, 2026). "
 "It is a small imprecision that the book has taken over from a secondary source. "
 "The 20-minute exception is like a quiet night rule at a pool: when nobody has swum for a while, anyone may get in the water without the usual test.")

D["TestnetBlockStorms"] = (
 "The book describes disruptive miners who create many blocks in a row on testnet without transactions and make it unusable (Antonopoulos and Harding, 2023). "
 "The numbers show the damage: testnet3 had 5,189,394 blocks on 2026-10-15, 6.3 times the 825,696 that one block in ten minutes since 2011-02-02 would have given, and more than 5 times the 971,537 blocks of mainnet; BIP 94 says that three years' worth of blocks were mined in a few weeks and the network was practically unusable (Mempool Space, 2026); (Jahr, 2024). "
 "The Bitcoin Wiki dates the blog post of Jameson Lopp, Griefing Bitcoin's Testnet, to 4 May 2024 and calls it the catalyst for testnet4 (Bitcoin Wiki, 2026). "
 "A block storm is like a faucet that someone has left open in a rented flat: the minimum-difficulty rule is meant for a trickle, and the tenant upstairs turns it into a flood.")

D["Bip94Rules"] = (
 "BIP 94 changes two rules for testnet4 and keeps the 20-minute exception for CPU mining: the difficulty adjustment takes its base from the first block of the previous period instead of the last, which stops a minimum-difficulty block at the end of a period from resetting the whole next period, and the first block of each period of 2016 blocks may not have a time more than 600 seconds before its parent's (Jahr, 2024). "
 "Bitcoin Core switches the rule on by the parameter enforce_BIP94, which only testnet4 sets, and the code of pow.cpp starts the retarget from pindexFirst->nBits when it is set (Bitcoin Core, 2026). "
 "Release 29.0 made the timewarp rule inactive on regtest and made block templates respect it on all networks, so miners are ready if mainnet adopts a timewarp fix (Bitcoin Core developers, 2025). "
 "The timewarp rule comes from the consensus cleanup proposal that Optech describes (Bitcoin Optech, 2026). "
 "It is like a speed limit that is first tried on a quiet side road, and written into the main road code later if it works.")

D["SignetChallengeIsMultisig"] = (
 "A signet is a test network in which every block must carry a solution to a challenge script, a normal Bitcoin script, so that only the holder of the keys can make blocks, which is why the book calls it fully permissioned (Antonopoulos and Harding, 2023); (Alm and Towns, 2019). "
 "The challenge of the default signet in Bitcoin Core 31.1 is 71 bytes long and disassembles to OP_1, two public keys of 33 bytes, OP_2 and OP_CHECKMULTISIG, a 1-of-2 multisig: either of the two operators can sign, as the book says that two contributors operate the default signet (Bitcoin Core, 2026). "
 "The custom signet of the run used the challenge 51, a single OP_1, which anyone can satisfy, so it is a signet in name only. "
 "The Optech topic explains that signed blocks give the creator complete control over the test network (Bitcoin Optech, 2026). "
 "It is like a theatre where only people with a ticket stub from one of two box offices can walk on the stage, however many people want to try.")

D["SignetMagicFromChallenge"] = (
 "Peers must not mistake one signet for another, so the four message-start bytes of a signet are not fixed in the source but computed: they are the first four bytes of the double SHA-256 of the challenge script with its length in front (Bitcoin Core, 2026). "
 "The code of this chapter reproduced the rule on three challenges: 0a03cf40 for the default signet, 54d26fbd for the one-byte challenge 51, and 7ec653a5 for the example given in BIP 325, the very value the BIP lists as the message start (Alm and Towns, 2019). "
 "A custom signet therefore needs no registry of magic numbers: choosing a new challenge chooses a new network. "
 "It is like a secret handshake derived from the club's password: change the password and all the hands change.")

D["SignetGenesisShared"] = (
 "All signets start from the same genesis block, whatever their challenge: the default signet and the custom signet with the challenge 51 in the run both reported the hash 000000088198..., the time 2020-09-01 00:00:00 UTC and the bits 1e0377ae, because the genesis block does not contain the challenge (Bitcoin Core, 2026). "
 "What separates one signet from another is therefore the challenge and the blocks that follow it, and the message-start bytes derived from it. "
 "BIP 325 was assigned to Karl-Johan Alm and Anthony Towns on 2019-03-20, and Bitcoin Core 0.21.0 added the support, with one public signet maintained and personal signets possible (Alm and Towns, 2019); (Bitcoin Core developers, 2021). "
 "It is like a set of identical blank forms from one printer: the forms are the same, and it is the stamp that makes each club's version its own.")

D["SignetSizeToday"] = (
 "The book says that the default signet has about 150,000 blocks and gives a listing with 143,619 blocks and 769 megabytes (Antonopoulos and Harding, 2023). "
 "On 2026-10-15 the tip of the default signet was at height 326,440, 2.27 times as many, close to the 321,840 that one block in ten minutes since the genesis of 2020-09-01 would give, so the signet keeps its target pace (Mempool Space, 2026). "
 "The book adds that the default signet is used to test proposed upgrades through the Bitcoin Inquisition project, and a signet can show a demonstration, as Optech notes for the slow blocks of BIP 54 (Bitcoin Optech, 2026). "
 "The book's figures are therefore a snapshot of 2023, not a property of the network. "
 "A number like this is a photograph of a growing child: true on the day it was taken.")

D["RegtestStartState"] = (
 "Regtest, short for regression testing, is a chain that exists only on your own machine: you launch it from scratch, with no other node unless you add one (Antonopoulos and Harding, 2023). "
 "A fresh Bitcoin Core 31.1 node on regtest reported the chain regtest, 0 blocks, 0 headers, the difficulty 4.656542373906925e-10, the median time 1296688602 and the best block hash 0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206, exactly the values in the book's listing, including the chainwork ending in 02 (Bitcoin Core, 2026). "
 "The difficulty is so low because the target 7fff... lets about every second hash win. "
 "It is like a driving school's empty car park: the rules of the road are the same, but you can practise a hundred times without meeting anybody.")

D["RegtestHalvesEvery150"] = (
 "On mainnet the block reward halves every 210,000 blocks, about four years; on regtest the interval is only 150, so that a developer can see several halvings within a few minutes (Bitcoin Core, 2026). "
 "The test chain showed the reward through getblockstats: 50 coins at heights 1 and 149, 25 at 150 and 299, 12.5 at 300 and 449, and 6.25 at 450 and 500, the same values as the code's subsidy rule with the interval 150 (Bitcoin Core, 2026). "
 "The book does not mention the interval, but it leads to the balance in the next listing. "
 "It is like a kitchen timer that is set to seconds instead of hours so that a lesson on 'cooking times' fits in a class.")

D["RegtestBalanceAfter500"] = (
 "The book mines 500 blocks on regtest and finds a balance of 12,462.5 coins, because the rewards must be 100 blocks deep to be spent (Antonopoulos and Harding, 2023). "
 "The sums agree: the rewards of blocks 1 to 400 add up to 149 x 50 + 150 x 25 + 101 x 12.5 = 12,462.5, the 100 blocks 401 to 500 gave 931.25 coins that the wallet still showed as immature, and mining the 500 blocks took 2.27 seconds on the shared machine of this run (Bitcoin Core, 2026). "
 "The book's number is correct, and it is correct only because of the interval of 150. "
 "It is like a pay slip with a month's wages held back: the full amount is on the paper, but only the older part can be drawn.")

D["NoDefaultWallet"] = (
 "The book's regtest session begins with the command createwallet with an empty name, to make a default wallet, but a Bitcoin Core 31.1 node refuses it: the command printed the error 'Wallet name cannot be empty' and exited with code 8 (Antonopoulos and Harding, 2023); (Bitcoin Core, 2026). "
 "A fresh node has no wallet at all, listwallets returned an empty list and getnewaddress answered that no wallet is loaded, so a reader who types the commands of the book gets an error at the first step and has to give the wallet a name, for example createwallet test. "
 "Release 31.0 mentions the empty wallet name in a different place, the Restore Wallet dialog of the graphical interface, which shows an error if the name is empty (Bitcoin Core developers, 2026). "
 "It is like a recipe that tells you to use the cupboard with no label: the shop no longer sells cupboards without labels.")

D["PipelineOrder"] = (
 "The book recommends a development pipeline: test the code on regtest, then on signet or testnet, and finally put it into production on mainnet (Antonopoulos and Harding, 2023). "
 "The source shows how the stages differ in how public they are: regtest has one dummy seed and no peers, signet has 2 DNS seeds and a block rule that needs a signature, testnet3 has 5 seeds and the minimum-difficulty rule, and mainnet has 8 seeds and no such rule (Bitcoin Core, 2026). "
 "A developer meets more and more of the real world at each step, other software, other people's transactions and network delays. "
 "It is like learning to drive: first the empty car park, then a quiet road with an instructor, and then the motorway.")

TOP = {}
TOP["BlockStructure"] = ("The first section of the chapter opens the block: a header of six fields and a list of transactions, with the sizes, the version flags, the time and the target that the header carries (Antonopoulos and Harding, 2023). "
 "Each statement was checked against a real block, the genesis block, block 277,315 or block 840,000, or against a block of the test chain (Bitcoin Core, 2026).")
TOP["BlockIdentifiers"] = ("The second section teaches the two names of a block, the hash that is computed from the header and the height that counts the blocks, and why the first is unique and the second is not (Antonopoulos and Harding, 2023). "
 "It also covers the coinbase rules that depend on height: the height written in the coinbase and the 100 blocks of maturity (Andresen, 2012).")
TOP["GenesisBlock"] = ("The third section is about the first block, which is written into the program, carries the headline of The Times of 3 January 2009 and can be rebuilt from a few numbers (Antonopoulos and Harding, 2023). "
 "The section also shows what is peculiar about it: its reward can never be spent (Bitcoin Wiki, 2026).")
TOP["LinkingBlocks"] = ("The fourth section is about the chain itself: how each block commits to its parent, why changing an old block means mining all that follow it, what a fork is and how the odds of a reorganization fall with depth (Antonopoulos and Harding, 2023). "
 "The ice core of the book's comparison is checked here as well (Wikipedia contributors, 2026).")
TOP["MerkleTrees"] = ("The fifth section teaches the merkle tree that summarizes the transactions of a block in 32 bytes: how it is built, its two known weaknesses and how a short path proves that one transaction is in a block (Antonopoulos and Harding, 2023). "
 "It has the most executed leaves of the chapter, because every statement about hashes can be recomputed (Bitcoin Core, 2026).")
TOP["TestBlockchains"] = ("The sixth section is about the chains on which Bitcoin software can be tried without risk: testnet, signet and regtest, with their genesis blocks, addresses, difficulty rules and sizes, and the pipeline from one to the next (Antonopoulos and Harding, 2023). "
 "It is the section where the book is most out of date, because testnet4 and the end of testnet3 came after it (Bitcoin Core developers, 2024).")

MID = {}
MID["BlockContainer"] = ("This subject asks what a block is as a container: the header, the counter and the transactions, the size field that belongs to the file on disk, the weight limit and the fields that getblock prints today (Antonopoulos and Harding, 2023).")
MID["HeaderFields"] = ("This subject asks what is in the 80 bytes: the version bits, the field order and byte order, the timestamp and the median of eleven, the compact target and the nonce that is too small for the work (Bitcoin Wiki, 2026).")
MID["HashIdentity"] = ("This subject asks what the block hash is: a double SHA-256 of the header, which is not stored inside the block and whose zeros are a consequence of the target (Bitcoin Wiki, 2026).")
MID["HeightAndMaturity"] = ("This subject asks what the height is: a count from the genesis block that can be shared by competing blocks, that BIP 34 writes into the coinbase and that decides when a reward may be spent (Andresen, 2012).")
MID["GenesisConstants"] = ("This subject asks what the genesis block is made of: the constants in chainparams.cpp, the message, the listing in the book and the transaction shared by most chains (Bitcoin Core, 2026).")
MID["GenesisQuirks"] = ("This subject asks what is odd about the genesis block: the reward that cannot be spent, and the headline that dates it to the term of Chancellor Alistair Darling (Wikipedia contributors, 2026).")
MID["BackLinks"] = ("This subject asks how blocks are linked backward and why that makes history hard to change: the previous-hash field, a real example, the effect of tampering, accumulated work, the old idea of linked time-stamps and the picture of the ice core (Haber and Stornetta, 1991).")
MID["ForksAndReorgs"] = ("This subject asks what happens when two blocks compete: the fork, the switch to the heavier branch and the fall of the odds of a reorganization with depth (Nakamoto, 2008).")
MID["TreeConstruction"] = ("This subject asks how a merkle tree is built: pairs, the duplicated odd hash, a 32-byte root whatever the size, the depth, a real block and the history of the idea (Merkle, 1980).")
MID["TreeFlaws"] = ("This subject asks where the construction is weak: the duplicated hash that lets two lists have one root, the defence in the code, the run that shows it, and the 64-byte transaction that looks like an inner node (Bitcoin Optech, 2026).")
MID["MerkleProofs"] = ("This subject asks how inclusion is proved with a short path: the path of the 11th of 16 transactions, its logarithmic length, the size compared with a block, the merkleblock message and the importance of left and right (Antonopoulos and Harding, 2023).")
MID["ChainsAndAddresses"] = ("This subject asks which chains exist and how they are kept apart: genesis blocks, address prefixes, data directories and the sizes of the chains (Bitcoin Core, 2026).")
MID["Testnet"] = ("This subject asks about the public proof-of-work test network: testnet3, which is deprecated, testnet4 that replaces it, the minimum-difficulty rule, the block storms and the two rules of BIP 94 (Jahr, 2024).")
MID["Signet"] = ("This subject asks about the signed test network: the challenge script, the message start derived from it, the shared genesis block and the growth of the default signet (Alm and Towns, 2019).")
MID["Regtest"] = ("This subject asks about the private test chain that the reader can run: its start state, the halving every 150 blocks, the balance after 500 blocks and the wallet command of the book that no longer works (Bitcoin Core, 2026).")
MID["DevelopmentPipeline"] = ("This subject asks how the test chains are used together: from regtest to signet or testnet and then to mainnet (Antonopoulos and Harding, 2023).")
