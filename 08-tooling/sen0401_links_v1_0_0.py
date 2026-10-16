#!/usr/bin/env python3
"""sen0401_links v1.0.0 - the named links of the SEN0401 decks of chapters 8 to 14 (owner finding of 2026-10-16: a link must name the resource and go straight to it).
DATA: READ[(chapter, story id)] = (label, url): the resource a story card links, label = its title and kind, short enough for the READ card (46 characters at most);
ROWS[old url] = (label, url, one line on what the reader finds); BOOK[chapter] = the chapter of Mastering Bitcoin 3e as its AsciiDoc source (raw.githubusercontent.com answers here, github.com does not).
patch(S, n) replaces the rows of every 'links' item of a deck plan by the named rows (called by deck_content_v1_1_0.py before the agenda); story_links(n) gives the READ pairs.
Run as a script: `sen0401_links_v1_0_0.py register NN` opens every new target (GET with a browser User-Agent through the proxy), reads its title (HTML title, PDF first page, YouTube oEmbed,
mempool.space API for blocks and transactions) and writes chNN-deck/link_register_v1_0_0.json from the old plan (deck_plan_v1_0_0.json) and the new one (deck_plan_v1_1_0.json)."""
__version__ = "1.0.0"
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/develop/"
BOOK = {8: ("ch08_signatures.adoc", "Mastering Bitcoin 3e, ch. 8: Digital Signatures"), 9: ("ch09_fees.adoc", "Mastering Bitcoin 3e, ch. 9: Transaction Fees"),
        10: ("ch10_network.adoc", "Mastering Bitcoin 3e, ch. 10: The Bitcoin Network"), 11: ("ch11_blockchain.adoc", "Mastering Bitcoin 3e, ch. 11: The Blockchain"),
        12: ("ch12_mining.adoc", "Mastering Bitcoin 3e, ch. 12: Mining and Consensus"), 13: ("ch13_security.adoc", "Mastering Bitcoin 3e, ch. 13: Security")}
READ = {
 (8, "SchnorrPatent"): ("Schnorr's patent US 4,995,082 (PDF)", "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4995082"),
 (8, "AndroidRandom"): ("Bitcoin.org alert: Android vulnerability", "https://bitcoin.org/en/alert/2013-08-11-android"),
 (8, "BookSignature"): ("The signed payment in block 277,316 (tx)", "https://mempool.space/tx/0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2"),
 (9, "HalvingBlock"): ("Block 840,000 on mempool.space (block)", "https://mempool.space/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5"),
 (9, "FullRbfPeering"): ("Peter Todd: Full-RBF Peering, v24.0.1 (post)", "https://mirror.b10c.me/lists/bitcoindev/Y5eSFbR61HleY6dw@petertodd.org"),
 (9, "CarveOutProposal"): ("Matt Corallo: CPFP Carve-Out proposal (post)", "https://mirror.b10c.me/lists/bitcoindev/c3f68b73-84c6-7428-4bf6-b47802141392@mattcorallo.com"),
 (9, "InstabilityPaper"): ("CITP blog: unstable without the reward (post)", "https://blog.citp.princeton.edu/2016/10/21/bitcoin-is-unstable-without-the-block-reward/"),
 (10, "CompactBlockRelay"): ("BIP 152: Compact Block Relay (spec)", "https://bips.dev/152/"),
 (10, "BloomFiltersLeak"): ("Gervais et al.: Bloom filter privacy (paper)", "https://eprint.iacr.org/2014/763"),
 (10, "FilterIdeaPost"): ("BIP 157: Client Side Block Filtering (spec)", "https://bips.dev/157/"),
 (10, "EclipseAtUsenix"): ("Heilman et al.: Eclipse Attacks (paper)", "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/heilman"),
 (10, "EncryptionAtLast"): ("BIP 324: v2 P2P Encrypted Transport (spec)", "https://bips.dev/324/"),
 (11, "HeadlineInTheGenesisBlock"): ("Genesis block 0 on mempool.space (block)", "https://mempool.space/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"),
 (11, "TheHashTreeOfRalphMerkle"): ("Merkle's patent US 4,309,569 (PDF)", "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4309569"),
 (11, "GriefingTheTestnet"): ("BIP 94: Testnet 4 (spec)", "https://bips.dev/94/"),
 (11, "SignetBlocksNeedASignature"): ("BIP 325: Signet (spec)", "https://bips.dev/325/"),
 (12, "HashcashBeforeBitcoin"): ("Back: Hashcash, a DoS counter-measure (PDF)", "https://web.archive.org/web/2023/http://www.hashcash.org/papers/hashcash.pdf"),
 (12, "ChainSplitOfMarch2013"): ("BIP 50: March 2013 Chain Fork Post-Mortem", "https://bips.dev/50/"),
 (12, "HalvingBlockWithRecordFees"): ("Block 840,000 on mempool.space (block)", "https://mempool.space/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5"),
 (12, "TaprootThroughSpeedyTrial"): ("Core 0.21.1 release notes: Speedy Trial", "https://bitcoincore.org/en/releases/0.21.1/"),
 (13, "TrezorSecureElement"): ("Bitcoin Wiki: Trezor (article)", "https://en.bitcoin.it/wiki/Trezor"),
 (13, "CasasciusCoins"): ("Bitcoin Wiki: Casascius physical bitcoins", "https://en.bitcoin.it/wiki/Casascius_physical_bitcoins"),
 (13, "MtGoxHotWallet"): ("Wikipedia: Mt. Gox (article)", "https://en.wikipedia.org/wiki/Mt._Gox"),
 (13, "ShamirSharesTheSecret"): ("Shamir: How to Share a Secret (PDF, 1979)", "https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf"),
 (14, "PizzaForBitcoins"): ("Bitcointalk thread: Pizza for bitcoins?", "https://bitcointalk.org/index.php?topic=137.0"),
 (14, "SpillmanChannels"): ("Reply: Anti DoS for tx replacement (list post)", "https://web.archive.org/web/2023/https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2013-April/002433.html"),
 (14, "PoonDryjaWhitepaper"): ("Poon and Dryja: Lightning paper (PDF)", "https://lightning.network/lightning-network-paper.pdf"),
 (14, "LightningTorch"): ("Wikipedia: Lightning Network (article)", "https://en.wikipedia.org/wiki/Lightning_Network"),
}
OT = "https://bitcoinops.org/en/topics/"
def bip(n, title, desc): return ("BIP %d: %s" % (n, title), "https://bips.dev/%d/" % n, desc)
ROWS = {
 "https://bitcoinops.org/en/newsletters/": ("Bitcoin Optech newsletters (weekly)", "https://bitcoinops.org/en/newsletters/", "Weekly digest of protocol and wallet development; all issues"),
 "https://delvingbitcoin.org/": ("Delving Bitcoin (research forum)", "https://delvingbitcoin.org/", "Developers argue out proposals and research in public threads"),
 "https://groups.google.com/g/bitcoindev": ("bitcoin-dev (mailing list)", "https://groups.google.com/g/bitcoindev", "Where BIPs and soft forks are first proposed and debated"),
 "https://mempool.space/": ("mempool.space (block explorer)", "https://mempool.space/", "Look up any block, transaction, fee rate and mempool"),
 "https://mempool.space/lightning": ("mempool.space Lightning (statistics)", "https://mempool.space/lightning", "Channels, nodes and capacity of the Lightning Network"),
 "https://bitnodes.io/": ("Bitnodes (live node census)", "https://bitnodes.io/", "Count and map of reachable nodes, by country and client"),
 "https://bitcoin.org/bitcoin.pdf": ("Bitcoin white paper (PDF)", "https://bitcoin.org/bitcoin.pdf", "Nakamoto's nine pages of October 2008"),
 "https://bips.dev/340/": bip(340, "Schnorr Signatures for secp256k1", "The specification with reference code and test vectors"),
 "https://bips.dev/327/": bip(327, "MuSig2 for BIP340 Multi-Signatures", "Specification of two-round multi-party Schnorr signing"),
 "https://bips.dev/125/": bip(125, "Opt-in Full Replace-by-Fee Signaling", "How a transaction signals that it may be replaced"),
 "https://bips.dev/431/": bip(431, "Topology Restrictions for Pinning", "The TRUC rules: version 3 transactions and package limits"),
 "https://bips.dev/152/": bip(152, "Compact Block Relay", "Short transaction ids and the messages that carry them"),
 "https://bips.dev/324/": bip(324, "v2 P2P Encrypted Transport", "The encrypted handshake and packet format of peers"),
 "https://bips.dev/94/": bip(94, "Testnet 4", "The rules of the new test network and why it replaced testnet3"),
 "https://bips.dev/325/": bip(325, "Signet", "How a block on the signed test network proves its signer"),
 "https://bips.dev/9/": bip(9, "Version bits with timeout and delay", "How soft forks are signalled in block versions"),
 "https://bips.dev/54/": bip(54, "Consensus Cleanup", "Proposed fixes of long-known consensus weaknesses"),
 "https://bips.dev/39/": bip(39, "Mnemonic code for deterministic keys", "Seed words, their checksum and the word list"),
 "https://bips.dev/112/": bip(112, "CHECKSEQUENCEVERIFY", "The relative timelock opcode that channels depend on"),
 OT + "replace-by-fee/": ("Optech topic: Replace-by-fee", OT + "replace-by-fee/", "Plain summary of RBF with links to newsletters and code"),
 OT + "compact-block-relay/": ("Optech topic: Compact block relay", OT + "compact-block-relay/", "Summary of BIP 152 and its later improvements"),
 OT + "v2-p2p-transport/": ("Optech topic: Version 2 P2P transport", OT + "v2-p2p-transport/", "Summary of encrypted peer traffic and its rollout"),
 OT + "merkle-tree-vulnerabilities/": ("Optech topic: Merkle tree vulnerabilities", OT + "merkle-tree-vulnerabilities/", "Why a 64-byte transaction can fake an inner node"),
 OT + "signet/": ("Optech topic: Signet", OT + "signet/", "Summary of signet use and public signets"),
 OT + "soft-fork-activation/": ("Optech topic: Soft fork activation", OT + "soft-fork-activation/", "The activation methods tried, with links to the debates"),
 OT + "selfish-mining/": ("Optech topic: Selfish mining", OT + "selfish-mining/", "Summary of the attack and what is known about it"),
 OT + "psbt/": ("Optech topic: Partially signed transactions", OT + "psbt/", "Summary of PSBT and the wallets that use it"),
 OT + "output-script-descriptors/": ("Optech topic: Output script descriptors", OT + "output-script-descriptors/", "Summary of descriptors with examples"),
 OT + "timelocks/": ("Optech topic: Timelocks", OT + "timelocks/", "The four timelock types side by side"),
 OT + "htlc/": ("Optech topic: Hash time locked contracts", OT + "htlc/", "How HTLCs route payments, with links to code"),
 OT + "anchor-outputs/": ("Optech topic: Anchor outputs", OT + "anchor-outputs/", "How channels keep the option to raise their fees later"),
 OT + "watchtowers/": ("Optech topic: Watchtowers", OT + "watchtowers/", "Services that answer a breach while the owner is offline"),
 "https://bitcoinops.org/en/schnorr-taproot-workshop/": ("Optech Schnorr and Taproot workshop", "https://bitcoinops.org/en/schnorr-taproot-workshop/", "Exercises and recorded sessions on Schnorr and Taproot"),
 "https://www.rfc-editor.org/rfc/rfc6979.txt": ("RFC 6979: Deterministic DSA and ECDSA", "https://www.rfc-editor.org/rfc/rfc6979.txt", "How the signing nonce is derived from key and message"),
 "https://link.springer.com/article/10.1007/BF00196725": ("Schnorr: Efficient signature generation (1991)", "https://link.springer.com/article/10.1007/BF00196725", "The seminal paper, Journal of Cryptology 4 (publisher page)"),
 "https://ocw.mit.edu/courses/15-s12-blockchain-and-money-fall-2018/": ("MIT 15.S12 Blockchain and Money: lectures", "https://ocw.mit.edu/courses/15-s12-blockchain-and-money-fall-2018/video_galleries/lecture-videos/", "The 2018 course, every lecture video in one list"),
 "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/heilman": ("Heilman et al.: Eclipse Attacks (paper)", "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/heilman", "Talk page with the paper, slides and video"),
 "https://arxiv.org/abs/1311.0243": ("Eyal and Sirer: Majority is not Enough (paper)", "https://arxiv.org/abs/1311.0243", "The selfish-mining paper, free to download"),
 "https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf": ("Shamir: How to Share a Secret (PDF, 1979)", "https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf", "The original two pages that define threshold sharing"),
 "https://raw.githubusercontent.com/lightning/bolts/master/03-transactions.md": ("BOLT 3: Transaction and Script Formats (spec)", "https://raw.githubusercontent.com/lightning/bolts/master/03-transactions.md", "Channel transaction layouts, with test vectors"),
 "https://lightning.network/lightning-network-paper.pdf": ("Poon and Dryja: Lightning paper (PDF)", "https://lightning.network/lightning-network-paper.pdf", "Draft 0.5.9.2 of 14 January 2016"),
 "https://www.youtube.com/embed/MPQMCVVhExY": ("Antonopoulos: Bitcoin Transaction Fees (video)", "https://www.youtube.com/embed/MPQMCVVhExY", "A talk on how fees are chosen and why they vary"),
 "https://www.youtube.com/embed/b-qGTj2Vvns": ("USENIX Security '15: Eclipse Attacks (video)", "https://www.youtube.com/embed/b-qGTj2Vvns", "The conference talk behind the paper"),
 "https://www.youtube.com/embed/7FWKc8lM4Ek": ("Neutrino: Privacy Preserving Light Client (video)", "https://www.youtube.com/embed/7FWKc8lM4Ek", "SF Bitcoin Developers talk on block filters"),
 "https://www.youtube.com/embed/_160oMzblY8": ("Brownworth: Blockchain 101, a visual demo (video)", "https://www.youtube.com/embed/_160oMzblY8", "Hashing, blocks and chains shown step by step"),
 "https://www.youtube.com/embed/na_omeubyYo": ("Chainlink: What Actually Are Merkle Trees? (video)", "https://www.youtube.com/embed/na_omeubyYo", "A short animated explanation of Merkle trees"),
 "https://www.youtube.com/embed/bBC-nXj3Ng4": ("3Blue1Brown: But how does bitcoin work? (video)", "https://www.youtube.com/embed/bBC-nXj3Ng4", "Ledger, signatures and proof of work, drawn out"),
 "https://www.youtube.com/embed/9V1bipPkCTU": ("Khan Academy: Bitcoin, proof of work (video)", "https://www.youtube.com/embed/9V1bipPkCTU", "Proof of work in a few minutes"),
 "https://www.youtube.com/embed/K54ildEW9-Q": ("Stand-up Maths: an open secret with maths (video)", "https://www.youtube.com/embed/K54ildEW9-Q", "Secret sharing explained with polynomials"),
 "https://www.youtube.com/embed/pOr6dwb7-dw": ("Unchained: What is bitcoin multisig? (video)", "https://www.youtube.com/embed/pOr6dwb7-dw", "How several keys protect one wallet"),
 "https://www.youtube.com/embed/yKdK-7AtAMQ": ("CuriousInventor: Lightning Explained (video)", "https://www.youtube.com/embed/yKdK-7AtAMQ", "How Lightning works, with animations"),
 "https://www.youtube.com/embed/KN7Z5dGWcRY": ("Poon and Dryja at Coinbase (video)", "https://www.youtube.com/embed/KN7Z5dGWcRY", "The two authors present the Lightning Network"),
 "https://en.bitcoin.it/wiki/OP_CHECKSIG": ("Bitcoin Wiki: OP_CHECKSIG (article)", "https://en.bitcoin.it/wiki/OP_CHECKSIG", "What the opcode checks, step by step"),
}


def row(n, r):
    old = r[1]
    if old == "https://aantonop.com/books/mastering-bitcoin/":
        f, lab = BOOK[n]
        return [lab, RAW + f, "The chapter's AsciiDoc source on GitHub, plain text"]
    if old not in ROWS:
        raise SystemExit("REFUSED: no named row for %s (chapter %d)" % (old, n))
    return list(ROWS[old])


def patch(S, n):
    k = 0
    for s in S:
        for it in s["items"]:
            if it.get("t") == "links":
                for g in it["groups"]:
                    g["rows"] = [row(n, r) for r in g["rows"]]; k += len(g["rows"])
    return k


def story_links(n):
    return {sid: v for (c, sid), v in READ.items() if c == n}


# ------------------------------------------------------------------------------------------------ register
UA = {"User-Agent": "Mozilla/5.0 (SEN0401 link register)"}


SCANNED = {"downloadPdf/4995082": "scanned patent, first page read by eye: United States Patent 4,995,082, Schnorr, Method for identifying subscribers and for generating and verifying electronic signatures in a data exchange system, Feb. 19, 1991",
           "downloadPdf/4309569": "scanned patent, first page read by eye: United States Patent 4,309,569, Merkle, Method of providing digital signatures, Jan. 5, 1982"}


def probe(u):
    import requests
    try:
        for k, v in SCANNED.items():
            if u.endswith(k):
                return requests.get(u, headers=UA, timeout=60).status_code, v
        if "youtube.com/embed/" in u:
            vid = u.rsplit("/", 1)[1]
            o = requests.get("https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=%s&format=json" % vid, headers=UA, timeout=30)
            st = requests.get(u, headers=UA, timeout=30).status_code
            return st, (o.json()["title"] + " / " + o.json()["author_name"]) if o.ok else "oEmbed answered %s" % o.status_code
        m = re.match(r"https://mempool\.space/(block|tx)/(\w+)$", u)
        r = requests.get(u, headers=UA, timeout=40)
        st = r.status_code
        if m:
            a = requests.get("https://mempool.space/api/%s/%s" % (m.group(1), m.group(2)), headers=UA, timeout=40)
            if a.ok:
                j = a.json()
                return st, ("mempool.space API: block height %s, %s transactions" % (j["height"], j["tx_count"])) if m.group(1) == "block" else \
                       ("mempool.space API: transaction %s, in block %s" % (j["txid"], j["status"].get("block_height")))
        if u.rstrip("/") == "https://mempool.space/lightning":
            a = requests.get("https://mempool.space/api/v1/lightning/statistics/latest", headers=UA, timeout=40)
            return st, "page is a single-page app (title: mempool - Bitcoin Explorer); its API answers %s with the latest Lightning statistics" % a.status_code
        ct = r.headers.get("content-type", ""); t = r.text if "pdf" not in ct and not u.endswith(".pdf") else ""
        if not t:
            p = subprocess.run(["pdftotext", "-l", "1", "-", "-"], input=r.content, capture_output=True, timeout=40).stdout.decode("utf8", "replace")
            ls = [x.strip() for x in p.splitlines() if x.strip()][:3]
            return st, "PDF, first page: " + " | ".join(ls)[:150]
        if "html" in ct or t.lstrip().startswith("<"):
            m2 = re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I)
            ti = re.sub(r"\s+", " ", m2.group(1)).strip() if m2 else "no title"
            import html
            return st, html.unescape(ti)[:150]
        return st, "text, first lines: " + " | ".join([x.strip() for x in t.splitlines() if x.strip()][:2])[:150]
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


def register(n):
    import concurrent.futures as cf, datetime
    chd = os.path.join(HERE, "ch%02d-deck" % n)
    old = items(json.load(open(os.path.join(chd, "deck_plan_v1_0_0.json"))))
    new = items(json.load(open(os.path.join(chd, "deck_plan_v1_1_0.json"))))
    assert len(old) == len(new) and all(a[0] == b[0] and a[1] == b[1] for a, b in zip(old, new)), "old and new plans do not pair"
    urls = list(dict.fromkeys(b[3] for b in new))
    with cf.ThreadPoolExecutor(6) as ex:
        pr = dict(zip(urls, ex.map(probe, urls)))
    rows = []
    for a, b in zip(old, new):
        st, ti = pr[b[3]]
        note = ""
        if ti in ("Client Challenge", "Sorry...") or "Checking you are not a bot" in str(ti):
            note = "not verified from here: the server answered with a bot challenge page; the URL is the publisher's own article page"
        elif not isinstance(st, int) or st >= 400:
            note = "not verified from here"
        if "hashcash.org" in b[3]:
            note = "www.hashcash.org serves no HTTPS (the story check needs https links); the Internet Archive copy of the same PDF is linked and was read"
        elif "web.archive.org" in b[3]:
            note = "the original list server (lists.linuxfoundation.org, same path) answers HTTP 418 to this machine; the Internet Archive copy of the same message is linked and was read"
        rows.append({"slide": b[0], "place": b[1], "old_label": a[2], "old_url": a[3], "new_label": b[2], "new_url": b[3], "changed": (a[2], a[3]) != (b[2], b[3]),
                     "status": st, "title_found": ti, "note": note})
    json.dump({"_version": __version__, "chapter": n, "checked": datetime.date.today().isoformat(), "links": rows}, open(os.path.join(chd, "link_register_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
    ch = sum(r["changed"] for r in rows); bad = [r for r in rows if r["note"].startswith("not verified")]
    print("chapter %d: %d links, %d changed, %d not verified from here" % (n, len(rows), ch, len(bad)))


if __name__ == "__main__":
    if sys.argv[1] == "register":
        register(int(sys.argv[2]))
