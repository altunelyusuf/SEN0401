"""SEN0401 chapter 13 (Bitcoin Security) - the story companion (5N1K): real, dated, sourced stories, one live link and one free picture each,
and the further-reading list. run_checks() refuses an empty field, a date that is not ISO, a link that is not https, a missing credit or picture file,
and re-reads the key facts of each story from the saved sources in ch13-evidence."""
__version__ = "1.3.0"  # (v1.3.0: concepts extended with the executed examples of research v1_0_2 that sit on the story slides)  each story's link goes straight to the resource and carries linkLabel, its title and kind (owner finding of 2026-10-16)
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STORIES = [
    {"id": "MtGoxHotWallet", "bio": 'Mark Karpeles, CEO of Mt. Gox from March 2011, was later found guilty by the Tokyo District Court of falsifying data; Jed McCaleb founded the exchange', "title": "The exchange that held the keys of everyone",
     "when": "2014-02-24",
     "who": "Mark Karpeles, who bought the site in March 2011 and ran it as CEO, Jed McCaleb, who founded it, and the customers whose coins were kept in the exchange's wallets",
     "where": "the exchange Mt. Gox in Shibuya, Tokyo, Japan, and its website mtgox.com",
     "link": "https://en.wikipedia.org/wiki/Mt._Gox", "linkLabel": "Wikipedia: Mt. Gox (article)",
     "concepts": ["MtGoxLoss", "BitfinexSegregatedWallets", "GenesisHashHardCoded", "AssumeValidShortcut", "MtGoxShare", "BitfinexHaircut"],
     "story": ("Mt. Gox, based in Shibuya, was launched in 2010 and was handling over 70% of all bitcoin transactions worldwide by early 2014. "
               "On 7 February 2014 it halted all withdrawals, and on 24 February it suspended all trading and its website went to a blank page. "
               "A leaked document claimed that it had lost 744,408 bitcoins in a theft that went undetected for years, and the Tokyo District Court later found Karpeles guilty of falsifying data to inflate the exchange's assets. "
               "The book's warning, that early exchanges put all user funds in a single hot wallet on one server, describes the design in which customers hold a claim on the exchange and not the keys."),
     "lesson": "Not your keys, not your coins: custody is trust",
     "source": "wikipedia_mt_gox.html (P67), bitcoinwiki_mt_gox.html (P63), book_ch13_security.adoc (P01); the MtGoxLoss leaf",
     "credit": "Letter regarding Mt.Gox - NetSPI, CC BY 2.0, Flickr",
     "photo": "mtgox_letter.png"},
    {"id": "CasasciusCoins", "bio": 'Mike Caldwell, maker of the Casascius coins in Sandy, Utah, suspended sales on 26 November 2013 after FinCEN called him a money transmitter', "title": "A coin with a private key under a sticker",
     "when": "2013-11-26",
     "who": "Mike Caldwell, the maker of the Casascius coins, and FinCEN, the Treasury bureau that told him that minting physical bitcoins made him a money transmitter",
     "where": "Sandy, Utah, USA, and the Bitcoin community that bought the coins",
     "link": "https://en.bitcoin.it/wiki/Casascius_physical_bitcoins", "linkLabel": "Bitcoin Wiki: Casascius physical bitcoins",
     "concepts": ["CasasciusHologram", "PaperWalletsAreObsolete", "BrainwalletCrackTime", "ExternalSignerSupport"],
     "story": ("Mike Caldwell first imagined a private key on a piece of paper inside a washer with a tamper-evident hologram on each side, and found it more economical to make a real coin. "
               "The coins, sold in 1, 10, 25, 100 and 1000 BTC sizes, had the key under a hologram that shows a honeycomb pattern when peeled, so that the holder could see whether anyone had looked. "
               "FinCEN had told him that minting physical bitcoins qualified him as a money transmitter business that must register, and he suspended sales on 26 November 2013. "
               "The book's physical storage, the seed on paper or metal, is the same idea without the maker."),
     "lesson": "A tamper seal tells you someone looked, not who",
     "source": "bitcoinwiki_casascius.html (P62), book_ch13_security.adoc (P01); the CasasciusHologram leaf",
     "credit": "Casascius hologram close-up - BTC Keychain, CC BY 2.0, Flickr",
     "photo": "casascius_hologram.png"},
    {"id": "ShamirSharesTheSecret", "bio": 'Adi Shamir, cryptographer at MIT in 1979 and co-inventor of RSA, published How to Share a Secret in the Communications of the ACM, volume 22, number 11', "title": "Three pieces of a key, any two will do",
     "when": "1979-11-01",
     "who": "Adi Shamir, then at the Massachusetts Institute of Technology and co-inventor of RSA, and the editor Rivest of the Communications of the ACM",
     "where": "the Communications of the ACM, volume 22, number 11, November 1979, pages 612 and 613",
     "link": "https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf", "linkLabel": "Shamir: How to Share a Secret (PDF, 1979)",
     "concepts": ["ShamirTwoOfThree", "OneShareRevealsNothing", "Codex32AndSlip39", "KeyLossTolerance", "SmallShamirByHand", "OneShareFitsEverySecret", "ShareGroups"],
     "story": ("Adi Shamir's two-page paper How to Share a Secret divides data D into n pieces so that D is easily computable from any k pieces and knowledge of any k minus 1 pieces leaves D completely undetermined. "
               "The scheme is based on polynomial interpolation: k points in the plane determine one and only one polynomial of degree k minus 1, and the secret is its value at zero. "
               "He noted that with n = 2k - 1 the key is recovered even when k - 1 pieces are lost or betrayed, which is the idea behind codex32 and SLIP39. "
               "In this chapter a degree-1 polynomial over a 127-bit prime gave three shares of which any two returned the secret 123456789."),
     "lesson": "Split the secret so that loss and theft both need several failures",
     "source": "shamir_1979_how_to_share_a_secret.pdf (P52), wikipedia_shamir_secret_sharing.html (P69), wikipedia_adi_shamir.html (P70), bip-0093.mediawiki (P25); the ShamirTwoOfThree leaf",
     "credit": "Adi Shamir Royal Society - Duncan Hull, CC BY-SA 4.0, Wikimedia Commons",
     "photo": "adi_shamir.png"},
    {"id": "TrezorSecureElement", "bio": 'SatoshiLabs, maker of the Trezor hardware wallets, announced the Trezor Safe 5 on 14 June 2024 at BTC Prague', "title": "The little box that learned to wait",
     "when": "2024-06-14",
     "who": "SatoshiLabs, the company behind the Trezor hardware wallets, and the people at BTC Prague where the Trezor Safe 5 was announced",
     "where": "BTC Prague, and the Bitcoin Wiki page on Trezor",
     "link": "https://en.bitcoin.it/wiki/Trezor", "linkLabel": "Bitcoin Wiki: Trezor (article)",
     "concepts": ["TrezorPinWait", "HardwareDoesNotCheckTheAddress", "ExternalSignerSupport", "PsbtThroughColdNode", "PinWaitByAttempts"],
     "story": ("A Trezor holds the keys and makes the signatures, and defends itself against a thief with a PIN whose waits double, 1 second after the first wrong try, 2 after the second, 4 after the third, and a wipe after 16 failed attempts. "
               "SatoshiLabs announced the Trezor Safe 5 on 14 June 2024 at BTC Prague, with a colour touchscreen with haptic feedback and an EAL 6+ secure element, and the Trezor Safe 7 on 21 October 2025 with a transparent, auditable secure element based on the TROPIC01 chip. "
               "The Bitcoin Wiki still warns that malware on the computer could swap the recipient's address, so the person must read the address on the device's own screen. "
               "In this chapter the waits before the sixteenth attempt added up to 32,767 seconds, 9.1 hours."),
     "lesson": "A signing box protects the key, you protect the intent",
     "source": "bitcoinwiki_trezor.html (P64), bitcoinwiki_hardware_wallet.html (P60), core_doc_external-signer.md (P40); the TrezorPinWait leaf",
     "credit": "Trezor Model T - FlippyFlink, CC0 1.0, Wikimedia Commons",
     "photo": "trezor_model_t.png"},
]
RESOURCES = [   # (kind, title, url): each opened on 2026-10-15
    ("video", "But how does bitcoin actually work? (3Blue1Brown, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=bBC-nXj3Ng4"),
    ("video", "Where Did The Bitcoin Go? The Mystery of Mt. Gox (CoinGecko, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=sBkWIK8Ld9c"),
    ("video", "Mt. Gox: Solving the Mystery of Bitcoin's Biggest Disaster (Fortune Magazine, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=SfiiF1zHWU4"),
    ("video", "MultiSig is NOT the best option for most people to store their bitcoin, June 2023 (aantonop, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=sjS5qF65Yos"),
    ("video", "What is bitcoin multisig? (Unchained, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=pOr6dwb7-dw"),
    ("video", "How to keep an open secret with mathematics (Stand-up Maths, YouTube; title read through YouTube oEmbed)", "https://www.youtube.com/watch?v=K54ildEW9-Q"),
    ("topic", "Bitcoin Optech topic: Partially signed bitcoin transactions", "https://bitcoinops.org/en/topics/psbt/"),
    ("topic", "Bitcoin Optech topic: Output script descriptors", "https://bitcoinops.org/en/topics/output-script-descriptors/"),
    ("topic", "Bitcoin Optech topic: Miniscript", "https://bitcoinops.org/en/topics/miniscript/"),
    ("topic", "Bitcoin Optech topic: Timelocks", "https://bitcoinops.org/en/topics/timelocks/"),
    ("explorer", "mempool.space, the block explorer that supplied the genesis block and the assumed-valid block of this chapter", "https://mempool.space/"),
    ("book", "Mastering Bitcoin, the book site (Antonopoulos and Harding)", "https://bitcoinbook.info/"),
    ("documentation", "BIP 324: version 2 P2P encrypted transport protocol", "https://bips.dev/324/"),
    ("documentation", "BIP 39: mnemonic code for generating deterministic keys", "https://bips.dev/39/"),
    ("documentation", "BIP 174: partially signed bitcoin transaction format", "https://bips.dev/174/"),
    ("documentation", "Bitcoin Core 27.0 release notes (the encrypted transport turned on by default)", "https://bitcoincore.org/en/releases/27.0/"),
    ("paper", "How to Share a Secret (Shamir, 1979, Communications of the ACM; the copy kept by MIT course 6.857)", "https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf"),
]
FIELDS = ("id", "bio", "title", "when", "who", "where", "link", "concepts", "story", "lesson", "source", "credit", "photo")
FACTS = {   # story id -> (saved file, fragments that must be found in it)
    "MtGoxHotWallet": ("wikipedia_mt_gox.txt", ["handling over 70% of all bitcoin transactions worldwide by early 2014", "On 7 February 2014, Mt. Gox halted all bitcoin withdrawals", "On 24 February 2014, Mt. Gox suspended all trading", "lost 744,408 bitcoins in a theft which went undetected for years", "found Karpel"]),
    "MtGoxHotWallet2": ("bitcoinwiki_mt_gox.txt", ["Jed McCaleb", "Shibuya, Tokyo, Japan", "after losing 640 thousand bitcoins"]),
    "MtGoxHotWallet3": ("book_ch13_security.adoc", ["many early Bitcoin exchanges concentrated all user funds in"]),
    "CasasciusCoins": ("bitcoinwiki_casascius.txt", ["Mike Caldwell, Sandy, Utah, USA", "sold until Nov 26, 2013", "Casascius coins are available in 1, 10, 25, 100, and 1000 BTC increments", "Originally, Mike Caldwell imagined placing a private key on a piece of paper inside a washer with a tamper-evident hologram on each side", "honeycomb-like tamper-evidence pattern when peeled", "minting physical bitcoins qualifies him as a money transmitter business"]),
    "ShamirSharesTheSecret": ("shamir_1979_how_to_share_a_secret.txt", ["leaves D completely undetermined", "Such a scheme is called a (k, n) threshold scheme", "Communications November 1979 of Volume 22 the ACM Number 11", "Adi Shamir"]),
    "ShamirSharesTheSecret2": ("wikipedia_shamir_secret_sharing.txt", ["first developed by Adi Shamir in 1979"]),
    "ShamirSharesTheSecret3": ("bip-0093.mediawiki", ["split into up to 31 shares"]),
    "TrezorSecureElement": ("bitcoinwiki_trezor.txt", ["Trezor Safe 5 was announced by SatoshiLabs on 14 June 2024 at the BTC Prague period", "EAL 6+ secure element", "Trezor Safe 7 was announced on 21 October 2025", "TROPIC01", "The device automatically wipe itself after 16 failed PIN entry attempts", "1 second after the first attempt, 2 seconds after the second attempt, and 4 seconds after the third attempt"]),
    "TrezorSecureElement2": ("bitcoinwiki_hardware_wallet.txt", ["malware on a PC could monitor for high value transactions and then swap out the recipient"]),
}


def run_checks():
    bad = []
    ev = os.path.join(HERE, "ch13-evidence")
    for s in STORIES:
        for f in FIELDS:
            v = s.get(f)
            if not v or "TODO" in str(v) or "CREDIT_" in str(v):
                bad.append("%s: field %s empty or TODO" % (s.get("id"), f))
        if len(str(s.get("lesson", "")).split()) > 14:
            bad.append("%s: lesson over 14 words" % s.get("id"))
        if not (2 <= str(s.get("story", "")).count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % s.get("id"))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(s.get("when", ""))):
            bad.append("%s: when is not an ISO date" % s.get("id"))
        if not str(s.get("link", "")).startswith("https://"):
            bad.append("%s: link is not https" % s.get("id"))
        p = os.path.join(HERE, "..", "03-materials", "ch13", "assets", str(s.get("photo", "")))
        if not os.path.exists(p) or os.path.getsize(p) < 10000 or open(p, "rb").read(5) in (b"<!DOC", b"<html"):
            bad.append("%s: picture file %s missing or not a picture" % (s.get("id"), s.get("photo")))
        for k in [s["id"]] + [s["id"] + str(i) for i in range(2, 7)]:
            if k not in FACTS:
                continue
            fn, frs = FACTS[k]
            t = re.sub(r"\s+", " ", open(os.path.join(ev, fn), encoding="utf-8", errors="replace").read())
            for fr in frs:
                if re.sub(r"\s+", " ", fr) not in t:
                    bad.append("%s: fact %r not in %s" % (s["id"], fr, fn))
    if len(STORIES) < 4:
        bad.append("fewer than four stories")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print("\n".join(b) or "stories ok")
    raise SystemExit(1 if b else 0)
