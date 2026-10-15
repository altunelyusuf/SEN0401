#!/usr/bin/env python3
"""Chapter 13 (Bitcoin Security) deck content, 26 slides, for the SEN0401 deck engine (sen0401_deck_engine_v1_0_0.py). Writes deck_plan_v1_0_0.json.

Every '>>>' row comes from examples_out_v1_0_0.json (executed by examples_v1_0_0.py under Python 3.14.6) and is re-run off the finished file by the deck check.
Every chart is built from those executed rows (parsed here and asserted), never typed. Rows that read the records of Bitcoin Core 31.1 on regtest are on slides that say Recorded;
what the research marks NOT EXECUTED carries that label; the pictures that show a topic and not the event are labelled stand-in. Speaker notes are short reader's prose
(2-4 sentences, at most 100 words, no presenter labels).
"""
import ast, datetime, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_0_0 as E

E.init(13, HERE, assets=("adi_shamir.png", "trezor_model_t.png", "casascius_hologram.png", "mtgox_letter.png"))
C, G, LABEL, STORY = E.C, E.G, E.LABEL, E.STORY
D = C.D
NPUB, NFIND, NCLAIM = len(D.PUBS), len(D.FINDINGS), len(D.TAX) + len(D.CLAIMS)
assert (NPUB, NFIND, NCLAIM) == (77, 25, 50), (NPUB, NFIND, NCLAIM)
OUT = lambda grp, i: ast.literal_eval(G[grp][i][1])
REC = "Recorded"
KEEP = {}          # key -> title, to find the slide numbers once the agenda has been inserted


def con(grp, x, y, w, h, label, fs=10, rows=None):
    return dict(E.code(grp, x, y, w, h, fs=fs, rows=rows), label=label)


def beats(x, y, w, h, items, fs=10.5):
    return {"t": "beats", "x": x, "y": y, "w": w, "h": h, "fs": fs, "items": items}


def foot(x, y, w, h, body, fs=11.5):
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body}


def chips(x, y, w, h, items, fs=10):
    return {"t": "chips", "x": x, "y": y, "w": w, "h": h, "fs": fs, "items": items}


def flow(x, y, w, h, steps, fs=11):
    return {"t": "flow", "x": x, "y": y, "w": w, "h": h, "fs": fs, "steps": steps}


def page(key, title, sub, items, notes, take, lede=None):
    KEEP[key] = title
    E.content(title, sub, items, notes, take=take, lede=lede)


def rows_of(grp, idx):
    return [G[grp][i] for i in idx]


def story(key, sid, photo, standin, beats_, grp, idx, label, notes, title=None):
    st = STORY[sid]
    rr = rows_of(grp, idx)
    E.story_slide(sid, photo, (0.5, 1.4, 2.9, 2.45), beats_, grp, rr, label, "", (3.6, 3.0, 5.9, 1.38), (3.6, 1.4, 5.9, 1.2), title=title)
    s = E.S[-1]
    s["notes"] = notes
    dt = datetime.date.fromisoformat(st["when"])
    s["sub"] = "The story of %d %s %d: who, where, when and what to read next" % (dt.day, dt.strftime("%B"), dt.year)
    for it in s["items"]:
        if it.get("t") == "factrow":
            it["x"], it["w"], it["y"] = 0.5, 9.0, 4.62
        if it.get("t") == "beats":
            it["fs"] = 10.5
    if standin:
        s["items"].append(foot(0.5, 4.22, 2.9, 0.36, standin, fs=9))
    KEEP[key] = s["title"]


# ---------------------------------------------------------------------------------------------- 1-3 opening
E.slide("title", "Chapter 13: Bitcoin Security", "What a signature protects, how keys are kept and backed up, and how several keys survive loss and theft. Bitcoin Core 31.1 results are Recorded.", [],
        "This deck explains Bitcoin security: what a signature protects, how traffic and the chain's first block are trusted, how a download is checked, and how keys are kept offline, on a device, behind a passphrase and in a backup. It ends with several keys, a delayed heir and Shamir's shared secrets. Every example runs under Python 3.14.6 on the chapter's own library, and Bitcoin Core 31.1 was run on a test network, so its answers are Recorded and only read back here. The research package for chapter 13 holds the sources and the claims.")

page("questions", "The questions this chapter answers", "Its own competency questions, and the numbers behind the answers",
     [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 1.7, "fs": 13, "items": list(C.CQS)},
      {"t": "stat", "x": 0.5, "y": 3.3, "w": 9.0, "h": 1.6, "items": [
          {"n": str(NPUB), "label": "sources, opened and read on %s" % D.DATE},
          {"n": str(NCLAIM), "label": "claims, each recomputed by running code"},
          {"n": str(NFIND), "label": "findings, several of them corrections of the book"}]}],
     "The chapter asks two questions that this deck answers by computation: which of its statements can be checked, and what has changed since print. The three numbers are counted from the research package, which holds %d sources, %d findings and %d executed claims. Each slide that follows shows the computation behind one claim." % (NPUB, NFIND, NCLAIM),
     "")
E.S[-1].pop("take", None)

# ---------------------------------------------------------------------------------------------- part A
E.section("Trusting the network and the software", "What a signature protects, and what a node or a download is trusted for.",
          [{"label": "A signed payment"}, {"label": "Encrypted traffic"}, {"label": "The first block"}, {"label": "Checking a download"}],
          "This part asks what Bitcoin protects and what it asks you to trust. A signed payment cannot be altered or replayed, node traffic is now encrypted by default, the chain starts from one typed-in block and a shortcut called assumed-valid, and a downloaded program can be checked against a list of hashes, but only so far as the signers' keys are known.")
KEEP["secA"] = "Trusting the network and the software"

CHEQUE = "Like a cheque with amount and payee inked in: change either and the signature fails"
page("payment", "A signature protects value and recipient", CHEQUE,
     [con("Payment", 0.5, 1.7, 9.0, 1.8, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 3.85, 9.0, 0.62, ["Row 2: the 222-byte payment holds a 71-byte signature and the 33-byte public key, no private key and no WIF",
                                   "Row 3: a valid payment is accepted; a swapped recipient or a changed amount breaks the signature",
                                   "Rows 4 and 5: the sighash byte 01 signs all outputs; a replay pays nothing, the outputs are already known"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: real money on mainnet; every payment here was made on regtest.", fs=10)],
     "A Bitcoin payment authorizes a specific value to a specific recipient. On a Bitcoin Core 31.1 test node, a signed payment of 222 bytes held a signature of 71 bytes and the public key of 33 bytes, and neither the private key nor its WIF text. The same payment with a swapped recipient or a changed amount was refused, because the signature covers the outputs, and sending it again paid nothing. No mainnet funds were used.",
     "A signature covers value and recipient, and never contains the key")

ENV = "Like sealing the envelope: strangers on the road cannot read it, only the two peers can"
page("transport", "Encrypted by default since release 27.0", ENV,
     [con("Transport", 0.5, 1.7, 9.0, 1.8, "Recorded: Core 31.1 regtest; the book and the release notes are saved", fs=9.5),
      beats(0.5, 3.85, 9.0, 0.62, ["Row 2: two Core 31.1 nodes spoke v2 and agreed on one session id; the services list P2P_V2",
                                   "Row 3: a peer that offers no v2 is served over v1, with no session id, and is still connected",
                                   "Rows 4 and 5: the book says no encryption is required; release 27.0 turned BIP 324 on by default"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: BIP 324 on the wire; the session ids matched, but no packets were captured.", fs=10)],
     "The book says that no encryption is required for Bitcoin traffic, and chapter 10 says Bitcoin Core talks in the clear. That is out of date: BIP 324 defines an encrypted version 2 transport, release 26.0 added it switched off, and release 27.0 turned it on by default. Two test nodes of Core 31.1 spoke v2 and agreed on one session id, while a peer without v2 was still served over v1. No traffic was captured on the wire.",
     "Since release 27.0 peers encrypt their traffic by default")

ROOT = "Like tracing a family tree to its founder, but trusting a recent page to save time"
page("root", "The root of trust: one typed-in block", ROOT,
     [con("Root", 0.5, 1.7, 9.0, 1.8, "executed on blocks saved from mempool.space and on the saved chainparams.cpp", fs=10),
      beats(0.5, 3.85, 9.0, 0.7, ["Row 2: the hash of the first block is typed into chainparams.cpp, and the code asserts it (True)",
                                  "Rows 3 and 4: Core 31.1 also ships an assumed-valid block, 938,343, and may skip script checks for blocks before it",
                                  "Row 5: that block is 33,237 blocks behind the tip, so 'trust only a validated chain' has a shortcut"], fs=10)],
     "The book says that the genesis block is the root of trust and that the only thing to be explicitly trusted is a fully validated blockchain. The genesis hash is indeed typed into chainparams.cpp and asserted. But Bitcoin Core 31.1 also ships an assumed-valid block, 938,343, and its help says a node may assume that block and its ancestors are valid and skip their script verification. Trust is therefore in the release you installed as well.",
     "The chain starts from one typed-in block, plus an assumed-valid shortcut")

SEAL = "Like a seal on a medicine box: it shows the box is the listed one, not who sealed it"
page("release", "Does the download match the list?", SEAL,
     [con("Release", 0.5, 1.7, 9.0, 1.5, "Recorded: Core 31.1 regtest; the list and the Guix text are saved", fs=10),
      beats(0.5, 3.6, 9.0, 0.7, ["Row 2: the SHA-256 of the 90,293,352-byte tarball equals its line among the 28 in SHA256SUMS (True)",
                                 "Row 3: gpg checked none of the 11 signatures with an empty keyring: exit 2, no good signature",
                                 "So the hash shows the file is the listed one, not who listed it; Guix builds avoid blind trust (row 4)"], fs=10),
      foot(0.5, 4.4, 9.0, 0.28, "NOT EXECUTED: a good gpg verification; it needs the builders' public keys, which were not imported.", fs=10)],
     "The tarball of Bitcoin Core 31.1 has 90,293,352 bytes and its SHA-256 equals its line in the list of 28 hashes, so it is the file that the list names. But the list itself is signed with 11 signatures, and with an empty keyring gpg could call none of them good: the hash proves only that the file is the listed one. The project's Guix builds exist so that users need not trust binary downloads blindly.",
     "A matching hash proves the file is the listed one, not who listed it")

# ---------------------------------------------------------------------------------------------- part B
E.section("Keeping the keys safe", "Cold storage, devices, passphrases, backups and seed words.",
          [{"label": "Cold storage"}, {"label": "Hardware wallets"}, {"label": "Passphrase and backup"}, {"label": "Seed words"}, {"label": "Trezor and Casascius"}],
          "This part is about keeping keys. A watch-only wallet and a partially signed transaction keep the keys on another machine, a hardware wallet makes the signature and defends itself with waiting, a passphrase locks the wallet file, and a backup must hold the descriptor and be recent. Seed words are checksummed arithmetic. The stories are the Trezor and the Casascius coin.")
KEEP["secB"] = "Keeping the keys safe"

CASH = "Like a cashier who writes cheques and a manager in another building who only signs them"
page("cold", "Cold storage: watch, sign elsewhere, send", CASH,
     [con("Cold", 0.5, 1.7, 9.0, 1.8, "Recorded: Core 31.1 regtest, three nodes", fs=10),
      beats(0.5, 3.85, 9.0, 0.62, ["Row 2: the hot wallet has private keys disabled and cannot sign (complete False, no signatures)",
                                   "Row 3: asked for its private descriptors, a watch-only wallet refuses: it holds none",
                                   "Rows 4 and 5: a node with 0 blocks and 0 connections signed the 528-character PSBT; the hot node sent it"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: a true air gap; the cold node was a second regtest node, not a separate machine.", fs=10)],
     "In cold storage the node that is online holds only public keys. On test nodes the hot wallet had private keys disabled and could not sign, and when asked for its private descriptors it answered with error minus four. A second node with no blocks and no connections signed the partially signed transaction of 528 characters, and the hot node finalized and broadcast it. A second node on the same machine is not a true air gap.",
     "The online wallet only watches; the signing happens somewhere else")

SAFE = "Like a safe that makes you wait longer after each wrong code, and then empties itself"
page("hardware", "Hardware wallets wait and wipe", SAFE,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: a Trezor waits 1, 2, 4 ... 16,384 seconds after wrong PINs: 32,767 seconds, 9.1 hours in all",
                                   "Row 3: after 16 failed PIN entries the device wipes itself (True)",
                                   "Row 4: Core 31.1 can use a device with -signer, but malware could still swap the recipient shown",
                                   "NOT EXECUTED: a hardware signing device"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Seconds of waiting after the nth wrong PIN", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 7,
       "labels": [str(i + 1) for i in range(15)], "series": [{"name": "seconds", "data": OUT("Hardware", 1)[0]}]},
      con("Hardware", 0.5, 3.42, 9.0, 1.38, "executed on the Bitcoin Wiki and the Core documentation, saved on 2026-10-15", fs=10)],
     "A hardware wallet holds the keys and makes the signatures, and it defends itself against a thief with a PIN whose waits double after every wrong try. The waits before the sixteenth attempt add up to 32,767 seconds, 9.1 hours, and then the device wipes itself. Bitcoin Core can drive such a device with the option -signer. The Bitcoin Wiki warns that malware could swap the recipient's address, so the person must read it on the device's screen; no device was run.",
     "The device protects the key; you must still read the address on its screen")

DRAWER = "Like a locked cash drawer in a shop window: customers see the money, only you can open it"
page("encryption", "A passphrase locks the keys, not the balance", DRAWER,
     [con("Encryption", 0.5, 1.7, 9.0, 2.1, "Recorded: Core 31.1 regtest; the constants are read from the saved crypter.h", fs=10),
      beats(0.5, 4.15, 9.0, 0.62, ["Rows 2, 3: a locked wallet shows its balance (1.0) but cannot send (-13); a wrong passphrase gives -14",
                                   "Row 4: an unlock for 3 seconds ended exactly then: the key is dropped and sending fails again",
                                   "Rows 5, 6: 32-byte key, 8-byte salt, 25000 rounds; encrypting also makes a new seed, so old backups miss new coins"], fs=10)],
     "Encrypting the wallet locks the private keys and nothing else. A locked wallet on the test node still showed its balance and gave new addresses, but refused to send with error minus 13, and a wrong passphrase gave minus 14. A three-second unlock ended on time. The key is AES-256 with a salt of 8 bytes and 25000 rounds, and encryptwallet also makes a new seed, so a backup made before encryption cannot recover the coins received after it.",
     "Encryption hides the keys, and it starts a new seed: back up again")

SPARE = "Like a spare key cut before the locksmith adds new locks: it opens only the old ones"
page("backups", "A backup is a descriptor and a date", SPARE,
     [con("Backups", 0.5, 1.7, 9.0, 1.8, "Recorded: Core 31.1 regtest; the help text is saved", fs=10),
      beats(0.5, 3.85, 9.0, 0.62, ["Row 2: a wallet restored from a fresh backup holds all 3.0 coins and derives the same next addresses",
                                   "Row 3: with a keypool of 3 a stale backup held 1.0 of 3.0: coins went to the tenth address, outside 0 to 2",
                                   "Row 4: one key does not know the multisig address; the descriptor finds the 2.0 coins, a wrong key order 0.0"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: paper and metal backups; only file backups of regtest wallets were restored.", fs=10)],
     "The book speaks of a wallet as keys that can be backed up like any file. In Bitcoin Core 31.1 a wallet is a set of descriptors, and a backup is only good while it is recent: on a node with a keypool of 3, a stale backup held only 1.0 of 3.0 coins because 2.0 went to the tenth address. For a multisignature wallet the descriptor must be saved as well, since one key alone knew nothing of the address and the same keys in another order found nothing.",
     "A backup needs the descriptor and a recent date")

RECIPE = "Like a recipe card: twelve words are enough to cook the same keys again"
page("seeds", "Seed words and their arithmetic", RECIPE,
     [con("Seeds", 0.5, 1.7, 9.0, 1.8, "executed on the published BIP 39 test vector, saved on 2026-10-15; the Core files are saved", fs=10),
      beats(0.5, 3.85, 9.0, 0.62, ["Rows 2, 3: 16 bytes make 12 words and 4 bits of checksum, so swapping the last word is caught",
                                   "Row 4: 2048 rounds with the passphrase TREZOR give the published seed (True); with none the seed starts 5eb00bbd",
                                   "Row 5: no mention of a mnemonic in Core's descriptors document or help: Core keeps descriptors, not words"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: recovery of a BIP 39 phrase in Bitcoin Core; Core has no such import.", fs=10)],
     "A seed phrase is a number written in words with a checksum. Sixteen bytes of entropy make twelve words from a list of 2048, and the last four bits are a checksum, so a changed last word is caught. The seed is made with 2048 rounds of PBKDF2 over the words and an optional passphrase, and it equals the published Trezor vector. Printing a single key on paper was a method of 2011 to 2016 that the Bitcoin Wiki now calls obsolete, and a brainwallet of four words is found in hours.",
     "Twelve words with a checksum rebuild every key; Core itself keeps descriptors")

story("trezor", "TrezorSecureElement", "trezor_model_t.png", "Stand-in picture: a Trezor Model T, not the Safe 5.",
      ["On 14 June 2024 SatoshiLabs announces the Trezor Safe 5 at BTC Prague, with an EAL 6+ secure element (row 3)",
       "A wrong PIN costs more waiting each time: 1, 2, 4 ... seconds, 32,767 in all (row 2)",
       "After 16 wrong PINs the device wipes itself; the Wiki lists the Trezor first among commercial hardware wallets"],
      "TrezorStory", [0, 1, 2], "executed on the Bitcoin Wiki page on the Trezor, saved on 2026-10-15",
      "A Trezor holds the keys and makes the signatures, and it defends itself against a thief with a PIN whose waits double, with a wipe after 16 failed attempts. SatoshiLabs announced the Trezor Safe 5 on 14 June 2024 at BTC Prague, with a colour touchscreen and an EAL 6+ secure element. The Bitcoin Wiki still warns that malware could swap the recipient's address, so the person must read the address on the device's own screen.",
      title="The little box that learned to wait")

story("casascius", "CasasciusCoins", "casascius_hologram.png", "Stand-in picture: a hologram close-up, not the coin.",
      ["Mike Caldwell of Sandy, Utah, sold Casascius coins with a private key under a hologram, until 26 November 2013 (row 2)",
       "They came in 1, 10, 25, 100 and 1000 BTC; the hologram shows if anyone peeled it, not who (row 2)",
       "FinCEN told him that minting physical bitcoins made him a money transmitter (row 3)"],
      "CasasciusStory", [0, 1, 2], "executed on the Bitcoin Wiki page on Casascius, saved on 2026-10-15",
      "Mike Caldwell of Sandy, Utah, made physical bitcoins: a coin with a private key under a tamper-evident hologram, sold in sizes from 1 to 1000 BTC. FinCEN had told him that minting physical bitcoins qualified him as a money transmitter that must register, and he suspended sales on 26 November 2013. The book's physical storage, the seed on paper or metal, is the same idea without the maker.",
      title="A coin with a private key under a sticker")

# ---------------------------------------------------------------------------------------------- part C
E.section("Surviving loss and theft", "Several keys, a delayed heir and shared secrets, and what custody costs.",
          [{"label": "Two of three keys"}, {"label": "The odds"}, {"label": "An heir who waits"}, {"label": "Shared secrets"}, {"label": "Two true stories"}],
          "This part is about the two ways to lose coins, losing the key and having it stolen. Several keys, a path for an heir that opens after a wait, and Shamir's shared secrets each trade one risk for another, and the odds depend on what is feared. The stories are the exchange that held everyone's keys and the paper that began secret sharing.")
KEEP["secC"] = "Surviving loss and theft"

BOX = "Like a safe deposit box that needs two of three keyholders: one lost key is no disaster"
page("multisig", "Two of three keys sign", BOX,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: one signature left the spend incomplete, two made it complete, 146 virtual bytes",
                                   "Row 3: losing one key leaves the funds spendable (True); losing two does not (False)",
                                   "Row 4: one key cost 110 virtual bytes, 2-of-3 costs 146; sortedmulti keeps one address (True), multi does not"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Virtual bytes of one spend", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": ["one key", "2-of-3 multisig"], "series": [{"name": "vbytes", "data": [OUT("Multisig", 3)[0], OUT("Multisig", 3)[1]]}]},
      con("Multisig", 0.5, 3.42, 9.0, 1.38, "Recorded: Core 31.1 regtest", fs=10)],
     "A two-of-three wallet needs two signatures: on the test chain one signature left the payment incomplete and two made it complete, in 146 virtual bytes against 110 for a single key. The loss of one key left the funds spendable, the loss of two did not. With sortedmulti the address is the same for any order of the keys, while with plain multi a different order gave a different address, which is why the descriptor belongs in the backup.",
     "Two of three keys survive one loss, and cost 36 more virtual bytes")

LOCKS = "Like extra locks on a door: fewer break-ins, but more ways to lock yourself out"
page("odds", "Odds of losing or being robbed", LOCKS,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 1: with each key lost at 0.1, a 2-of-3 setup is stuck at 0.028 and a 1-of-3 at 0.001, a single key at 0.1",
                                   "Row 2: with each key stolen at 0.05, 2-of-3 is robbed at 0.00725, but 1-of-3 at 0.14263",
                                   "Row 3: at a loss chance of 0.5 the 2-of-3 is no better than one key (0.5); keys are assumed independent"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 2.1, "h": 1.75, "ctype": "bar", "title": "Stuck", "dataLabels": True, "dlFmt": "0.###", "dlFs": 8,
       "labels": ["1 key", "2-of-3", "1-of-3"], "series": [{"name": "stuck", "data": OUT("Odds", 0)}]},
      {"t": "chart", "x": 7.4, "y": 1.38, "w": 2.1, "h": 1.75, "ctype": "bar", "title": "Robbed", "dataLabels": True, "dlFmt": "0.#####", "dlFs": 8,
       "labels": ["1 key", "2-of-3", "1-of-3"], "series": [{"name": "robbed", "data": OUT("Odds", 1)}]},
      con("Odds", 0.5, 3.42, 9.0, 1.38, "executed on the chapter's own formulas; the chances are assumptions", fs=10)],
     "The odds depend on what is feared. If each key is lost with chance 0.1 and stolen with chance 0.05, independently, which is an assumption, a two-of-three setup is stuck with chance 0.028 and robbed with chance 0.00725, against 0.1 and 0.05 for one key. A one-of-three setup is almost never stuck, 0.001, but is robbed with chance 0.14263. At a loss chance of 0.5 the two-of-three is no better than a single key.",
     "More keys trade the risk of loss against the risk of theft")

WILL = "Like a will with a waiting period: the heir can claim only after the owner stays silent"
page("heir", "An heir who must wait ten blocks", WILL,
     [con("Heir", 0.5, 1.7, 9.0, 1.8, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 3.85, 9.0, 0.62, ["Rows 2, 3: the owner spends at once; the heir is refused at 1 and 9 confirmations and accepted at 10",
                                   "Row 4: older(65536) was accepted by Core 31.1, but BIP 68 reads 16 bits: the heir could spend after 1 block",
                                   "Row 5: the longest honest wait is 65,535 blocks, 455.1 days, or 65,535 units of 512 seconds, 388.4 days"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: estate planning with a lawyer; only the script rule was tested, on regtest.", fs=10)],
     "A wallet can give an heir a path that opens only after a delay: the policy was or(owner, and(heir, older 10)). On the test chain the owner could spend at once and the heir was refused at one and at nine confirmations and accepted at ten. There is a trap: BIP 68 reads only 16 bits of the sequence, and Bitcoin Core 31.1 accepted older(65536), with which the heir could spend after one block. The longest honest wait is 65,535 blocks, about 455 days.",
     "An heir path waits for confirmations, and a value over 65,535 wraps around")

PAPER = "Like a map torn in three: any two pieces show the spot, one shows nothing"
page("shamir", "Shamir: three pieces, any two open it", PAPER,
     [con("Shamir", 0.5, 1.7, 9.0, 1.5, "executed on the chapter's own Shamir library over a prime field", fs=10),
      beats(0.5, 3.6, 9.0, 0.7, ["Rows 2, 3: a secret is split in three shares; any two recover it, one share alone does not (False)",
                                 "Row 4: over the field 257, one share fits all 257 possible secrets: it leaves the secret undetermined",
                                 "The chapter does not mention Shamir; BIP 93 (codex32, a draft) and SLIP 39 use the idea for seed words"], fs=10),
      foot(0.5, 4.4, 9.0, 0.28, "NOT EXECUTED: Shamir sharing inside a wallet; the shares were made by the chapter's own library.", fs=10)],
     "Shamir's scheme splits a secret into n pieces so that any k of them recover it and fewer reveal nothing. In the chapter's library a secret was split into three shares, and any two returned it while one share did not. Over a small field of 257 values, one share fitted all 257 possible secrets, which is what undetermined means. The book does not mention the scheme, but BIP 93, a draft, and SLIP 39 use it for seed words.",
     "Any two of three shares recover the secret, and one share reveals nothing")

story("mtgox", "MtGoxHotWallet", "mtgox_letter.png", "Stand-in picture: a letter about the bankruptcy, not the theft.",
      ["On 24 February 2014 Mt. Gox of Shibuya, Tokyo, suspended all trading, after halting withdrawals on 7 February",
       "A leaked document claimed 744,408 bitcoins stolen unseen for years; it had over 70% of all trades (row 2)",
       "Counts differ: 850,000 less the 199,999.99 found gives 650,000.01 (row 3). NOT EXECUTED: an exchange breach"],
      "MtGoxStory", [0, 1, 2], "executed on the Wikipedia page on Mt. Gox, saved on 2026-10-15",
      "Mt. Gox of Shibuya, Tokyo, launched in 2010, handled over 70 percent of bitcoin transactions by early 2014, halted withdrawals on 7 February 2014 and suspended all trading on 24 February. A leaked document claimed a loss of 744,408 bitcoins in a theft undetected for years, and the Tokyo District Court later found its CEO Mark Karpeles guilty of falsifying data. The figures differ by source and are quoted with theirs. Customers held a claim on the exchange and not the keys.",
      title="The exchange that held the keys of everyone")

story("shamirpaper", "ShamirSharesTheSecret", "adi_shamir.png", None,
      ["In November 1979 Adi Shamir, then at MIT, publishes How to Share a Secret in the Communications of the ACM",
       "Any k pieces recover the secret; k minus 1 pieces leave it completely undetermined (row 3)",
       "Here two of three shares gave back 123456789 (row 2); codex32 and SLIP 39 use the same idea"],
      "ShamirStory", [0, 1, 2], "executed on the saved 1979 paper and the chapter's Shamir library",
      "Adi Shamir's two-page paper How to Share a Secret, in the Communications of the ACM of November 1979, divides data into n pieces so that any k pieces compute it easily and knowledge of any k minus 1 pieces leaves it completely undetermined. The scheme rests on polynomial interpolation: k points determine one polynomial of degree k minus 1, and the secret is its value at zero. In this chapter two of three shares returned the secret 123456789.",
      title="Three pieces of a key, any two will do")

# ---------------------------------------------------------------------------------------------- summary, resources, closing
page("summary", "The chapter in five lines", "One line per idea, each one provable from its slides",
     [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5, "items": [
         "A signature covers value and recipient, and traffic between nodes is encrypted by default",
         "The chain starts from one typed-in block, and a matching hash proves only that a file is the listed one",
         "Keys are safer offline or on a device, behind a passphrase, and backed up with their descriptor",
         "Seed words are checksummed arithmetic; paper wallets and brainwallets are weak",
         "Several keys, a delayed heir or shared secrets trade the risk of loss against the risk of theft"]}],
     "These five lines are the deck in miniature. Each can be traced to a part of the route on slide 2 and to computations that ran on its slides. A line that feels unproven should send the reader back to that part's consoles.",
     "If a line feels unproven, its part's consoles carry the receipt")

page("resources", "Where to go from here", "Opened on %s; every entry is a live link in this file" % D.DATE,
     [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
         {"head": "Read", "rows": [
             ["Optech topic, partially signed transactions", "https://bitcoinops.org/en/topics/psbt/"],
             ["Optech topic, output script descriptors", "https://bitcoinops.org/en/topics/output-script-descriptors/"],
             ["Optech topic, timelocks", "https://bitcoinops.org/en/topics/timelocks/"]]},
         {"head": "Standards and papers", "rows": [
             ["BIP 324, encrypted transport", "https://bips.dev/324/"],
             ["BIP 39, mnemonic code", "https://bips.dev/39/"],
             ["Shamir, How to Share a Secret (1979)", "https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf"]]},
         {"head": "Watch", "rows": [
             ["Stand-up Maths: how to keep an open secret (video)", "https://www.youtube.com/embed/K54ildEW9-Q"],
             ["Unchained: what is bitcoin multisig (video)", "https://www.youtube.com/embed/pOr6dwb7-dw"]]},
         {"head": "Community", "rows": [
             ["Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/"],
             ["Delving Bitcoin, research forum", "https://delvingbitcoin.org/"],
             ["The bitcoin-dev group", "https://groups.google.com/g/bitcoindev"]]}]}],
     "Everything here is free to read or watch, and every link was opened on %s. A good start is the Stand-up Maths video on secret sharing, then the Optech topic on partially signed transactions next to the chapter. The research package for chapter 13 lists all %d sources with the passages used." % (D.DATE, NPUB),
     "Watch the secret-sharing video, then read the Optech topic beside the chapter")

E.slide("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "What a signature protects, and what a node or a download is trusted for",
            "How keys are kept offline, on a device, behind a passphrase and in a backup",
            "How seed words, several keys and shared secrets are made",
            "Why custody is trust, and what each safeguard costs"]}],
        "Four claims, each carried by computations that ran on slides of this deck. A reader who can say them and point to the slide that proves them has the chapter. The research package for chapter 13 holds the sources and the test records behind them.", bg="dark")

# ---------------------------------------------------------------------------------------------- agenda and plan meta
E.agenda(["The chapter's questions", "Trusting the network and the software", "Keeping the keys safe", "Surviving loss and theft"],
         "The route has three parts after the questions: trusting the network and the software, with the signed payment, encrypted traffic, the first block and the download check; keeping the keys safe, with cold storage, devices, passphrases, backups and seed words; and surviving loss and theft, with several keys, an heir, shared secrets and custody. Each part carries true stories and corrections of the book that a reader can check on the slide. The numbers in the list let a reader jump straight to a part.",
         "Three parts, four true stories, and a list of what was not run")
E.finish("Chapter 13: Bitcoin Security", "1.0.0", "2026-10-15, first deck from the committed research package (commit 600f845, v1_0_1 files), to the CME look and feel; notes are short reader's prose")

planp = os.path.join(HERE, "deck_plan_v1_0_0.json")
plan = json.load(open(planp))
num = {k: [i + 1 for i, s in enumerate(plan["slides"]) if s["title"] == t][0] for k, t in KEEP.items()}
plan["meta"]["notes"] = "short reader's prose: 2-4 sentences, at most 100 words"
plan["meta"]["honesty"] = {
    "title": ["Bitcoin Core 31.1", REC],
    "recorded": [1, num["payment"], num["transport"], num["release"], num["cold"], num["encryption"], num["backups"], num["multisig"], num["heir"]],
    "notExecuted": [num["payment"], num["transport"], num["release"], num["cold"], num["hardware"], num["backups"], num["seeds"], num["heir"], num["shamir"], num["mtgox"]],
    "standin": {str(num["trezor"]): ["Stand-in picture"], str(num["casascius"]): ["Stand-in picture"], str(num["mtgox"]): ["Stand-in picture"]},
    "vectors": [num["transport"], num["root"], num["release"], num["hardware"], num["encryption"], num["backups"], num["seeds"], num["trezor"], num["casascius"], num["mtgox"], num["shamirpaper"]],
}
plan["meta"]["analogies"] = [
    {"concept": "transaction signature", "analogy": CHEQUE, "slide": num["payment"]},
    {"concept": "encrypted transport", "analogy": ENV, "slide": num["transport"]},
    {"concept": "root of trust", "analogy": ROOT, "slide": num["root"]},
    {"concept": "release checking", "analogy": SEAL, "slide": num["release"]},
    {"concept": "cold storage", "analogy": CASH, "slide": num["cold"]},
    {"concept": "hardware wallet", "analogy": SAFE, "slide": num["hardware"]},
    {"concept": "wallet encryption", "analogy": DRAWER, "slide": num["encryption"]},
    {"concept": "backup", "analogy": SPARE, "slide": num["backups"]},
    {"concept": "seed phrase", "analogy": RECIPE, "slide": num["seeds"]},
    {"concept": "multisignature", "analogy": BOX, "slide": num["multisig"]},
    {"concept": "loss and theft odds", "analogy": LOCKS, "slide": num["odds"]},
    {"concept": "timelocked heir", "analogy": WILL, "slide": num["heir"]},
    {"concept": "secret sharing", "analogy": PAPER, "slide": num["shamir"]},
]
json.dump(plan, open(planp, "w"), indent=1)
print("meta: honesty and %d analogies written; slide numbers %s" % (len(plan["meta"]["analogies"]), num))
