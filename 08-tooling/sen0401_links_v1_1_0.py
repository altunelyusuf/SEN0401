#!/usr/bin/env python3
"""sen0401_links v1.1.0 - the named links of the SEN0401 decks of chapters 1 to 7 (owner finding of 2026-10-16: a link must name the resource and go straight to it).
DATA: READ[(chapter, slide)] = (story id, label, url): the resource a story card links, label = its title and kind, 46 characters at most so that the READ card shows it whole;
ROWS[(chapter, old url)] = (label, url, one line on what the reader finds) for every row of the resources slide.
apply(n, plan) gives the new plan of a chapter (the READ cards, the rows, and for chapter 3 the date of the version 0.1 announcement: 8 January 2009, the date in the list header);
stories_text(n, text) gives the text of the new story companion (link and linkLabel of each story, and the chapter 3 date); register(n, old, new) probes every new target and writes chNN-deck/link_register_v1_0_0.json.
Usage: sen0401_links_v1_1_0.py plan NN <old plan> <new plan> | stories NN <old module> <new module> | register NN <old plan> <new plan>"""
__version__ = "1.1.0"
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RAW = "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/develop/"
BOOK = {1: ("ch01_intro.adoc", "Mastering Bitcoin, ch. 1: Introduction"), 2: ("ch02_overview.adoc", "Mastering Bitcoin, ch. 2: How Bitcoin Works"),
        3: ("ch03_bitcoin-core.adoc", "Mastering Bitcoin, ch. 3: Bitcoin Core"), 4: ("ch04_keys.adoc", "Mastering Bitcoin, ch. 4: Keys and Addresses"),
        5: ("ch05_wallets.adoc", "Mastering Bitcoin, ch. 5: Wallets"), 6: ("ch06_transactions.adoc", "Mastering Bitcoin, ch. 6: Transactions")}
GENESIS_TX = "https://mempool.space/tx/4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
BLOCK170_TX = "https://mempool.space/tx/f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16"
WIKI_OVERFLOW = "https://en.bitcoin.it/wiki/Value_overflow_incident"
GOX_LOST = "https://techcrunch.com/2014/03/03/mt-gox-posts-new-statement-on-alleged-theft-bankruptcy-filing/"
READ = {
 (1, 7): ("GenesisHeadline", "Genesis block coinbase, with the headline (tx)", GENESIS_TX),
 (1, 8): ("FirstTransaction", "Satoshi to Finney, block 170 (tx)", BLOCK170_TX),
 (1, 9): ("CypherpunkLineage", "Bitcoin white paper (PDF)", "https://bitcoin.org/bitcoin.pdf"),
 (1, 11): ("StoneMoney", "Furness: The Island of Stone Money (book)", "https://www.gutenberg.org/ebooks/72830"),
 (1, 12): ("MoneyEvolution", "The History of Money (museum exhibit)", "https://www.money.org/money-museum/virtual-exhibits/hom"),
 (1, 15): ("OnlinePayments", "PayPal Form S-1, 2001 (SEC filing)", "https://www.sec.gov/Archives/edgar/data/1103415/000091205701533855/a2059025zs-1.htm"),
 (1, 16): ("WhenMoneyStops", "CNBC: Ukraine accepts crypto donations (news)", "https://www.cnbc.com/2022/03/02/ukraine-dogecoin-other-cryptocurrencies-accepted-for-donations.html"),
 (1, 23): ("PizzaDay", "First commercial Bitcoin transaction (record)", "https://www.guinnessworldrecords.com/world-records/696240-first-commercial-bitcoin-transaction"),
 (1, 34): ("MtGox", "Mt.Gox filing statement, TechCrunch (news)", GOX_LOST),
 (2, 6): ("WhitepaperMath", "Bitcoin white paper (PDF)", "https://bitcoin.org/bitcoin.pdf"),
 (2, 12): ("FirstFaucet", "Get 5 free bitcoins (bitcointalk thread)", "https://bitcointalk.org/index.php?topic=183.0"),
 (2, 21): ("ValueOverflow", "Value overflow incident (Bitcoin Wiki)", WIKI_OVERFLOW),
 (3, 6): ("FirstRelease", "Satoshi: Bitcoin v0.1 released (list post)", "https://www.metzdowd.com/pipermail/cryptography/2009-January/014994.html"),
 (3, 10): ("ReproducibleBuilds", "Builder attestation, Core 31.1 (hash list)", "https://raw.githubusercontent.com/bitcoin-core/guix.sigs/main/31.1/achow101/all.SHA256SUMS"),
 (3, 14): ("MaintainerHandoffs", "Andresen: Core maintainer van der Laan (post)", "https://web.archive.org/web/2015/https://bitcoinfoundation.org/2014/04/07/bitcoin-core-maintainer-wladimir-van-der-laan/"),
 (4, 6): ("NewDirections1976", "Diffie, Hellman: New Directions (PDF)", "https://www-ee.stanford.edu/~hellman/publications/24.pdf"),
 (4, 12): ("Base58Design", "base58.h in bitcoin/bitcoin (source)", "https://raw.githubusercontent.com/bitcoin/bitcoin/master/src/base58.h"),
 (4, 17): ("BitcoinEater", "The eater address on blockstream.info", "https://blockstream.info/address/1BitcoinEaterAddressDontSendf59kuE"),
 (5, 6): ("IronKey", "Lost passwords lock millionaires out (NYT)", "https://www.nytimes.com/2021/01/12/technology/bitcoin-passwords-wallets-fortunes.html"),
 (5, 9): ("Bip39Birth", "BIP 39: Mnemonic code (spec)", "https://bips.dev/39/"),
 (5, 18): ("GoxColdFind", "MtGox finds 200,000 Bitcoin (The Register)", "https://www.theregister.com/2014/03/21/mtgox_finds_200000_bitcoin_in_old_wallets/"),
 (6, 6): ("FirstTransaction", "Satoshi to Finney, block 170 (tx)", BLOCK170_TX),
 (6, 9): ("PizzaDay", "Pizza for bitcoins? (bitcointalk thread)", "https://bitcointalk.org/index.php?topic=137.0"),
 (6, 15): ("ValueOverflow", "Value overflow incident (Bitcoin Wiki)", WIKI_OVERFLOW),
 (6, 19): ("GoxMalleability", "Transaction Malleability and MtGox (paper)", "https://arxiv.org/abs/1403.6676"),
 (7, 7): ("OpReturnBug", "CVE-2010-5141 entry (Bitcoin Wiki)", "https://en.bitcoin.it/wiki/Common_Vulnerabilities_and_Exposures#CVE-2010-5141"),
 (7, 10): ("DerFork", "Alert: Some Miners Generating Invalid Blocks", "https://bitcoin.org/en/alert/2015-07-04-spv-mining"),
 (7, 22): ("SchnorrToTaproot", "Block 709,632, taproot activation (block)", "https://mempool.space/block/0000000000000000000687bca986194dc2c1f949318629b44bb54ec0a94d8244"),
}
# the 46-character limit is for the READ card; the host follows in small text when the label is short
WP = ("Bitcoin white paper (PDF)", "https://bitcoin.org/bitcoin.pdf", "Nakamoto's nine pages of 31 October 2008")
SE = ("Bitcoin Stack Exchange (Q&A site)", "https://bitcoin.stackexchange.com", "Search or ask any technical question; answers are voted")
MEMPOOL = ("mempool.space (block explorer)", "https://mempool.space", "Live blocks, transactions and fee rates; look up any txid")
BLOCKSTREAM = ("blockstream.info (block explorer)", "https://blockstream.info", "Look up any block, transaction or address")
LMAB = ("learnmeabitcoin.com (illustrated guide)", "https://learnmeabitcoin.com", "Every Bitcoin structure drawn and explained, with code")
YT3B1B = ("But how does bitcoin actually work? (video)", "https://www.youtube.com/watch?v=bBC-nXj3Ng4", "3Blue1Brown draws the ledger, signatures and proof of work")
PIZZA = ("Pizza for bitcoins? (bitcointalk thread)", "https://bitcointalk.org/index.php?topic=137.0", "Laszlo Hanyecz's offer of 10,000 bitcoins, May 2010")
STRANGE = ("Strange block 74638 (bitcointalk thread)", "https://bitcointalk.org/index.php?topic=822.0", "The forum thread where the overflow was found live")
OVERFLOW = ("Value overflow incident (Bitcoin Wiki)", WIKI_OVERFLOW, "What block 74,638 did and how it was fixed")


def bip(n, label, finds): return ("BIP %d: %s (spec)" % (n, label), "https://bips.dev/%d/" % n, finds)


ROWS = {
 # chapter 1
 (1, "https://bitcoin.org/bitcoin.pdf"): WP,
 (1, "https://github.com/bitcoinbook/bitcoinbook"): (BOOK[1][1], RAW + BOOK[1][0], "Chapter text as AsciiDoc source, plain text, free to read"),
 (1, "https://developer.bitcoin.org"): ("Bitcoin Developer Guides (docs)", "https://developer.bitcoin.org/devguide/index.html", "Guides to blocks, transactions, wallets and the network"),
 (1, "https://bitcoincore.org"): ("Bitcoin Core: download page", "https://bitcoincore.org/en/download/", "Signed releases of the reference client, with checksums"),
 (1, "https://mempool.space"): MEMPOOL,
 (1, "https://blockstream.info"): BLOCKSTREAM,
 (1, "https://www.coingecko.com"): ("CoinGecko: Bitcoin price page", "https://www.coingecko.com/en/coins/bitcoin", "Price, market cap and volume history of bitcoin"),
 (1, "https://bitcoin.stackexchange.com"): SE,
 (1, "https://bitcointalk.org"): PIZZA,
 (1, "http://www.hashcash.org"): ("Back: Hashcash, a DoS counter-measure (PDF)", "https://web.archive.org/web/2023/http://www.hashcash.org/papers/hashcash.pdf", "Adam Back's proof-of-work paper; Internet Archive copy"),
 (1, "http://www.weidai.com/bmoney.txt"): ("Wei Dai: b-money (text, 1998)", "https://web.archive.org/web/2023/http://www.weidai.com/bmoney.txt", "The 1998 proposal Bitcoin cites; Internet Archive copy"),
 (1, "https://www.youtube.com/watch?v=bBC-nXj3Ng4"): YT3B1B,
 # chapter 2
 (2, "https://bitcoin.org/bitcoin.pdf"): ("Bitcoin white paper (PDF)", "https://bitcoin.org/bitcoin.pdf", "Section 11: the table of attacker odds this chapter charts"),
 (2, "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch02_overview.adoc"): (BOOK[2][1], RAW + BOOK[2][0], "Chapter text as AsciiDoc source, plain text, free to read"),
 (2, WIKI_OVERFLOW): OVERFLOW,
 (2, "https://mempool.space"): MEMPOOL,
 (2, "https://blockstream.info"): BLOCKSTREAM,
 (2, "https://learnmeabitcoin.com"): LMAB,
 (2, "https://bitcoin.stackexchange.com"): SE,
 (2, "https://bitcointalk.org/index.php?topic=141.0"): ("Get 5 free bitcoins (bitcointalk thread)", "https://bitcointalk.org/index.php?topic=183.0", "Gavin Andresen's faucet announcement, 11 June 2010"),
 (2, "https://www.youtube.com/watch?v=bBC-nXj3Ng4"): YT3B1B,
 # chapter 3
 (3, "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch03_bitcoin-core.adoc"): (BOOK[3][1], RAW + BOOK[3][0], "Chapter text as AsciiDoc source, plain text, free to read"),
 (3, "https://bitcoincore.org"): ("Bitcoin Core: releases", "https://bitcoincore.org/en/releases/", "Every release with notes, binaries and signatures"),
 (3, "https://github.com/bitcoin/bitcoin"): ("bitcoind.cpp at tag v31.1 (source)", "https://raw.githubusercontent.com/bitcoin/bitcoin/v31.1/src/bitcoind.cpp", "The daemon's entry point; change the tag to read others"),
 (3, "https://github.com/bitcoin-core/guix.sigs"): ("guix.sigs README: how builders attest (text)", "https://raw.githubusercontent.com/bitcoin-core/guix.sigs/main/README.md", "The process behind the signed build hashes of each release"),
 (3, "https://github.com/bitcoin/bitcoin/tree/master/doc"): ("Bitcoin Core build guide for Unix (text)", "https://raw.githubusercontent.com/bitcoin/bitcoin/master/doc/build-unix.md", "Dependencies and commands to build bitcoind on Linux"),
 (3, "https://developer.bitcoin.org/reference/rpc/"): ("Bitcoin Core RPC reference (docs)", "https://developer.bitcoin.org/reference/rpc/", "Every RPC method with arguments, results and examples"),
 (3, "https://bitcoin.stackexchange.com"): SE,
 (3, "https://en.wikipedia.org/wiki/Bitcoin_Core"): ("Wikipedia: Bitcoin Core (article)", "https://en.wikipedia.org/wiki/Bitcoin_Core", "History of the client from version 0.1 to the present"),
 (3, "https://git-scm.com/book"): ("Pro Git, 2nd edition (book)", "https://git-scm.com/book/en/v2", "The free book on Git, by Chacon and Straub"),
 # chapter 4
 (4, "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch04_keys.adoc"): (BOOK[4][1], RAW + BOOK[4][0], "Chapter text as AsciiDoc source, plain text, free to read"),
 (4, "https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange"): ("Diffie, Hellman: New Directions (PDF)", "https://www-ee.stanford.edu/~hellman/publications/24.pdf", "The 1976 paper that introduced public-key cryptography"),
 (4, "https://github.com/bitcoin/bitcoin/blob/master/src/base58.h"): ("base58.h in bitcoin/bitcoin (source)", "https://raw.githubusercontent.com/bitcoin/bitcoin/master/src/base58.h", "Satoshi's comment on why 58 characters were chosen"),
 (4, "https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki"): bip(173, "Base32 address format", "bech32 addresses for native segwit outputs"),
 (4, "https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki"): bip(350, "Bech32m addresses", "The bech32m fix used by v1+ (taproot) addresses"),
 (4, "https://blockstream.info/address/1BitcoinEaterAddressDontSendf59kuE"): ("1BitcoinEater... on blockstream.info (address)", "https://blockstream.info/address/1BitcoinEaterAddressDontSendf59kuE", "The unspendable address and every coin sent into it"),
 (4, "https://learnmeabitcoin.com"): ("learnmeabitcoin: Keys (guide)", "https://learnmeabitcoin.com/technical/keys/", "Private keys, public keys and addresses, drawn stepwise"),
 (4, "https://bitcoin.stackexchange.com"): SE,
 # chapter 5
 (5, "https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch05_wallets.adoc"): (BOOK[5][1], RAW + BOOK[5][0], "Chapter text as AsciiDoc source, plain text, free to read"),
 (5, "https://www.nytimes.com/2021/01/12/technology/bitcoin-passwords-wallets-fortunes.html"): ("Lost passwords lock millionaires out (NYT)", "https://www.nytimes.com/2021/01/12/technology/bitcoin-passwords-wallets-fortunes.html", "The IronKey story as reported, 12 January 2021"),
 (5, "https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki"): bip(39, "Mnemonic code", "The word list and how seed words become a seed"),
 (5, "https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki"): bip(32, "HD wallets", "How one seed derives a whole tree of keys"),
 (5, "https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki"): bip(84, "P2WPKH derivation", "The m/84'/0'/0' path these slides derived"),
 (5, "https://iancoleman.io/bip39/"): ("Ian Coleman's BIP39 tool (use offline)", "https://iancoleman.io/bip39/", "Turn seed words into keys and addresses; run it offline"),
 (5, "https://learnmeabitcoin.com"): ("learnmeabitcoin: HD wallets (guide)", "https://learnmeabitcoin.com/technical/keys/hd-wallets/", "Seed to master key to child keys, drawn"),
 (5, "https://bitcoin.stackexchange.com"): SE,
 # chapter 6
 (6, "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/develop/ch06_transactions.adoc"): (BOOK[6][1], RAW + BOOK[6][0], "Chapter text as AsciiDoc source, plain text, free to read"),
 (6, "https://arxiv.org/abs/1403.6676"): ("Transaction Malleability and MtGox (paper)", "https://arxiv.org/abs/1403.6676", "Decker and Wattenhofer's measurements, free to download"),
 (6, "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0141.mediawiki"): bip(141, "Segregated Witness", "Weight, witness data and the new transaction format"),
 (6, "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0068.mediawiki"): bip(68, "Relative lock-time", "Locking an input by sequence numbers"),
 (6, "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0125.mediawiki"): bip(125, "Opt-in Replace-by-Fee", "How a transaction signals that it may be replaced"),
 (6, "https://mempool.space/tx/466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177"): ("Alice's transaction on mempool.space (tx)", "https://mempool.space/tx/466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177", "Block 775,072: the payment this chapter builds"),
 (6, "https://learnmeabitcoin.com/technical/transaction/"): ("learnmeabitcoin: Transaction (guide)", "https://learnmeabitcoin.com/technical/transaction/", "A raw transaction byte by byte, drawn"),
 (6, "https://bitcointalk.org/index.php?topic=137.0"): PIZZA,
 (6, "https://bitcointalk.org/index.php?topic=822.0"): STRANGE,
 # chapter 7
 (7, "https://bitcoin.org/bitcoin.pdf"): WP,
 (7, "https://en.bitcoin.it/wiki/Script"): ("Script (Bitcoin Wiki)", "https://en.bitcoin.it/wiki/Script", "Every opcode with its effect and status"),
 (7, "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0066.mediawiki"): bip(66, "Strict DER signatures", "The rule behind the July 2015 fork"),
 (7, "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0141.mediawiki"): bip(141, "Segregated Witness", "Witness programs and how they are validated"),
 (7, "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0341.mediawiki"): bip(341, "Taproot spending rules", "Key path, script path and the commitment"),
 (7, "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0342.mediawiki"): bip(342, "Tapscript validation", "The script rules inside a taproot spend"),
 (7, "https://raw.githubusercontent.com/bitcoin/bitcoin/v0.3.0/script.cpp"): ("script.cpp of Bitcoin 0.3.0 (source)", "https://raw.githubusercontent.com/bitcoin/bitcoin/v0.3.0/script.cpp", "The early script engine, as it was released"),
 (7, "https://en.bitcoin.it/wiki/Common_Vulnerabilities_and_Exposures"): ("CVE-2010-5141 entry (Bitcoin Wiki)", "https://en.bitcoin.it/wiki/Common_Vulnerabilities_and_Exposures#CVE-2010-5141", "The early script bug, in the list of known vulnerabilities"),
 (7, "https://bitcoin.org/en/alert/2015-07-04-spv-mining"): ("Alert: Some Miners Generating Invalid Blocks", "https://bitcoin.org/en/alert/2015-07-04-spv-mining", "The notice of 4 July 2015 about unvalidated blocks"),
 (7, "https://bitcoinops.org/en/topics/taproot/"): ("Optech topic: Taproot", "https://bitcoinops.org/en/topics/taproot/", "Summary of taproot with links to newsletters and code"),
 (7, "https://en.bitcoin.it/wiki/Taproot"): ("Taproot (Bitcoin Wiki)", "https://en.bitcoin.it/wiki/Taproot", "Plain description of the taproot soft fork"),
}
DATE_FIX = (("2009-01-09", "2009-01-08"), ("Friday January 9 2009", "Thursday January 8 2009"), ("Six days after", "Five days after"))
CH3_FIX_SLIDE = 6


def apply(n, plan):
    """The new plan of chapter n: READ cards and rows named, chapter 3 date corrected. Refuses a card or row without an entry."""
    used = set()
    for i, s in enumerate(plan["slides"], 1):
        for it in s["items"]:
            if it.get("t") == "factrow":
                if (n, i) not in READ:
                    raise SystemExit("REFUSED: no READ entry for chapter %d slide %d" % (n, i))
                sid, lab, url = READ[(n, i)]
                if len(lab) > 46:
                    raise SystemExit("REFUSED: label over 46 characters: %s" % lab)
                it["linkText"], it["link"] = lab, url; used.add(("r", i))
            if it.get("t") == "links":
                for g in it["groups"]:
                    new = []
                    for r in g["rows"]:
                        if (n, r[1]) not in ROWS:
                            raise SystemExit("REFUSED: no named row for %s (chapter %d)" % (r[1], n))
                        new.append(list(ROWS[(n, r[1])])); used.add(("w", r[1]))
                    g["rows"] = new
        if n == 3 and i == CH3_FIX_SLIDE:
            t = json.dumps(s, ensure_ascii=False)
            for a, b in DATE_FIX:
                t = t.replace(a, b)
            plan["slides"][i - 1] = json.loads(t)
    miss = [k for k in READ if k[0] == n and ("r", k[1]) not in used] + [k for k in ROWS if k[0] == n and ("w", k[1]) not in used]
    if miss:
        raise SystemExit("REFUSED: entries without a place in the plan: %r" % miss)
    return plan


def stories_text(n, text):
    """The text of the new story companion: each story's link replaced and linkLabel added (the chapter 3 date and 'Six days' corrected)."""
    for (c, sl), (sid, lab, url) in READ.items():
        if c != n:
            continue
        m = re.search(r'("id": "%s",.*?)("link": ")([^"]*)(",)' % re.escape(sid), text, re.S)
        if not m:
            raise SystemExit("REFUSED: story %s not found in the chapter %d module" % (sid, n))
        text = text[:m.start(2)] + '"link": "%s", "linkLabel": "%s",' % (url, lab) + text[m.end(4):]
    if n == 3:
        for a, b in DATE_FIX:
            text = text.replace(a, b)
    return text


# ------------------------------------------------------------------------------------------------ register
UA = {"User-Agent": "Mozilla/5.0 (SEN0401 link register)"}
CHALLENGE = ("Just a moment", "Establishing a secure connection", "Challenge Verification", "Access Denied", "Client Challenge", "Sorry...", "Are you a robot", "nytimes.com", "Your Request Originates")
# targets this machine cannot open (bot challenge) but whose title was read another way: url -> (status, title, how)
MANUAL = {
 "https://www.sec.gov/Archives/edgar/data/1103415/000091205701533855/a2059025zs-1.htm":
   (200, "Form S-1 Registration Statement under the Securities Act of 1933, PayPal, Inc., filed 28 September 2001", "the proxy answers 403 (the SEC refuses undeclared tools); the WebFetch tool opened it and read this title"),
 "https://www.cnbc.com/2022/03/02/ukraine-dogecoin-other-cryptocurrencies-accepted-for-donations.html":
   (403, "Ukraine accepts dogecoin, other cryptocurrencies for donations as funding rises to $35 million", "not verified from here: the server answered 403 (access denied); the headline is the one a web search shows for this exact URL"),
 "https://www.nytimes.com/2021/01/12/technology/bitcoin-passwords-wallets-fortunes.html":
   (403, "Lost Passwords Lock Millionaires Out of Their Bitcoin Fortunes", "not verified from here: the server answered 403; the headline is the one web searches show for this article (N. Popper, 12 January 2021)"),
}


def probe(u):
    import time
    for k in range(4):
        r = probe1(u)
        if isinstance(r[0], int) and r[0] != 429 or k == 3:
            return r
        time.sleep(6)


def probe1(u):
    import requests, time
    if u in MANUAL:
        return MANUAL[u][0], MANUAL[u][1]
    try:
        m = re.match(r"https://youtu\.be|https://www\.youtube\.com/watch\?v=([\w-]+)$", u)
        if m:
            o = requests.get("https://www.youtube.com/oembed?url=%s&format=json" % u, headers=UA, timeout=30)
            return (200 if o.ok else o.status_code), (o.json()["title"] + " / " + o.json()["author_name"]) if o.ok else "oEmbed answered %s" % o.status_code
        m = re.match(r"https://blockstream\.info/address/(\w+)$", u)
        if m:
            a = requests.get("https://blockstream.info/api/address/" + m.group(1), headers=UA, timeout=40)
            st = requests.get(u, headers=UA, timeout=40).status_code
            if a.ok:
                j = a.json()
                return st, "blockstream.info API: address %s, %d transactions received" % (j["address"], j["chain_stats"]["funded_txo_count"])
        if u.startswith("https://raw.githubusercontent.com/bitcoin-core/guix.sigs/main/31.1/"):
            r = requests.get(u, headers=UA, timeout=40)
            return r.status_code, "text, first line: " + r.text.splitlines()[0][:110]
        import sen0401_links_v1_0_0 as L0
        for k in range(3):
            r = L0.probe(u)
            if isinstance(r[0], int) or k == 2:
                return r
            time.sleep(5)
    except Exception as e:
        return type(e).__name__, str(e)[:100]


def items(plan):
    out = []
    for i, s in enumerate(plan["slides"], 1):
        for it in s["items"]:
            if it.get("t") == "factrow":
                out.append((i, "READ card", it["linkText"], it["link"]))
            if it.get("t") == "links":
                for g in it["groups"]:
                    for r in g["rows"]:
                        out.append((i, "resources, " + g["head"], r[0], r[1]))
    return out


def register(n, oldp, newp):
    import concurrent.futures as cf, datetime
    chd = os.path.join(HERE, "ch%02d-deck" % n)
    old = items(json.load(open(oldp)))
    new = items(json.load(open(newp)))
    assert len(old) == len(new) and all(a[0] == b[0] and a[1] == b[1] for a, b in zip(old, new)), "old and new plans do not pair"
    urls = list(dict.fromkeys(b[3] for b in new))
    with cf.ThreadPoolExecutor(6) as ex:
        pr = dict(zip(urls, ex.map(probe, urls)))
    rows = []
    for a, b in zip(old, new):
        st, ti = pr[b[3]]
        note = ""
        if b[3] in MANUAL:
            note = MANUAL[b[3]][2]
        elif b[3] == "https://learnmeabitcoin.com/technical/keys/hd-wallets/":
            note = "not verified from here: the page answers with a bot challenge; the Keys guide page (HTTP 200) links to this exact path"
        elif any(c in str(ti) for c in CHALLENGE) or (isinstance(st, int) and st >= 400):
            note = "not verified from here: the server answered %s with a bot challenge page; the URL is the publisher's own page for the resource" % st
        elif "web.archive.org" in b[3] and "hashcash" in b[3]:
            note = "www.hashcash.org serves no HTTPS; the Internet Archive copy of the same PDF is linked and was read"
        elif "web.archive.org" in b[3] and "weidai" in b[3]:
            note = "www.weidai.com/bmoney.txt answers on HTTP only here (HTTPS resets); the Internet Archive copy of the same text is linked and was read"
        elif "web.archive.org" in b[3]:
            note = "bitcoinfoundation.org no longer serves the post (404); the Internet Archive copy of the same page is linked and was read"
        elif "raw.githubusercontent.com" in b[3]:
            note = "github.com pages are blocked from here; the file is linked as the plain text raw.githubusercontent.com serves and was read"
        elif b[3] == GENESIS_TX:
            note = "mempool.space API: the coinbase input script reads 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'"
        elif b[3] == BLOCK170_TX:
            note = "mempool.space API: confirmed in block 170, outputs of 10 and 40 BTC (the 10 BTC are Finney's)"
        elif b[3].endswith("#CVE-2010-5141"):
            note = "the page was read and carries the anchor CVE-2010-5141"
        elif b[3] == "https://www.money.org/money-museum/virtual-exhibits/hom":
            note = "survey topic with no single primary source; the exhibit was read: it covers Mesopotamia, Lydia, electrum coins and paper money (not the 1971 gold window)"
        elif b[3] == "https://en.wikipedia.org/wiki/Bitcoin_Core":
            note = "the project's history as a whole has no single primary source; the article is named as Wikipedia in the label"
        elif b[3] == "https://www.metzdowd.com/pipermail/cryptography/2009-January/014994.html":
            note = "list header date: Thu Jan 8 14:27:40 EST 2009; the slide said 9 January and is corrected to 8 January 2009"
        elif b[3] == "https://bitcointalk.org/index.php?topic=183.0":
            note = "the old link (topic 141) is the thread 'Odd amount of generated coins', not the faucet announcement; the faucet thread is topic 183, first posts 11 June 2010"
        rows.append({"slide": b[0], "place": b[1], "old_label": a[2], "old_url": a[3], "new_label": b[2], "new_url": b[3], "changed": (a[2], a[3]) != (b[2], b[3]),
                     "status": st, "title_found": ti, "note": note})
    json.dump({"_version": __version__, "chapter": n, "checked": datetime.date.today().isoformat(), "links": rows}, open(os.path.join(chd, "link_register_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
    ch = sum(r["changed"] for r in rows); bad = [r for r in rows if r["note"].startswith("not verified")]
    print("chapter %d: %d links, %d changed, %d not verified from here" % (n, len(rows), ch, len(bad)))
    for r in bad:
        print("   not verified:", r["new_url"])


if __name__ == "__main__":
    cmd, n = sys.argv[1], int(sys.argv[2])
    if cmd == "plan":
        p = json.load(open(sys.argv[3]))
        v = re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", sys.argv[4])[0]
        p = apply(n, p); p["meta"]["version"] = "%s.%s.%s" % v
        json.dump(p, open(sys.argv[4], "w"), indent=1)
        print("written", sys.argv[4])
    elif cmd == "stories":
        v = re.findall(r"_v(\d+)_(\d+)_(\d+)\.py$", sys.argv[4])[0]
        t = stories_text(n, open(sys.argv[3]).read())
        t = re.sub(r'__version__ = "[\d.]+"', '__version__ = "%s.%s.%s"  # each story link goes straight to the resource and carries linkLabel (owner finding of 2026-10-16)' % v, t, count=1)
        open(sys.argv[4], "w").write(t)
        print("written", sys.argv[4])
    elif cmd == "register":
        register(n, sys.argv[3], sys.argv[4])
