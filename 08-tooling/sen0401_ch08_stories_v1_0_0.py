"""SEN0401 chapter 8 - the story companion (5N1K): real, dated, sourced stories, one live further-reading link and one licence-clear picture each.
Fill every field; run_checks() refuses any TODO, a date that is not ISO, a link that is not https, a missing credit or picture file.

Chapter 7 already told the script bug of 2010, the BIP66 fork of 2015 and the taproot activation of 2021, so this chapter tells three others, each tied to a
computation the chapter runs:
* SchnorrPatent - 19 February 1991: the United States grant of the Schnorr signature patent, which is why Bitcoin started with ECDSA (the dates are computed).
* AndroidRandom - 11 August 2013: the alert that Android's secure random number generator was weak, and the nonce-reuse key recovery the chapter executes.
* BookSignature - 27 December 2013: the signature printed in the book's DER example is a real signature in block 277,316 and is verified in the chapter.
"""
__version__ = "1.0.0"
import os, re

STORIES = [
    {
        "id": "SchnorrPatent",
        "title": "The signature that was patented for two decades",
        "when": "1991-02-19",
        "who": "Claus-Peter Schnorr, the cryptographer who invented the signature; the company Public Key Partners, which the patent database lists as its later holder",
        "where": "the United States patent office for United States patent 4,995,082, applied for on 23 February 1990 with a priority date of 24 February 1989, and the Crypto '89 conference whose proceedings published his scheme",
        "link": "https://en.wikipedia.org/wiki/Schnorr_signature",
        "concepts": ["PatentDates", "SchnorrToTaprootYears", "Bip340Vectors"],
        "story": ("Claus-Peter Schnorr published an efficient identification and signature scheme for smart cards in the proceedings of the Crypto '89 conference, and "
                  "the United States published his patent 4,995,082 on 19 February 1991, filed on 23 February 1990 and claiming priority from 24 February 1989. "
                  "A patent kept the algorithm out of open standards, so cryptographers of the early 1990s who wanted a free alternative designed the Digital "
                  "Signature Algorithm and its elliptic curve version, ECDSA, and ECDSA was the only signature Bitcoin supported from its first release until the taproot "
                  "soft fork of 2021. The statute gave such a patent the greater of 17 years from grant, 19 February 2008, and 20 years from filing, 23 February 2010; the chapter computes both, "
                  "and Wikipedia states that the patent expired in February 2010, which fits the book's 'almost two decades'. The BIP340 signature that Bitcoin uses today "
                  "is Schnorr's scheme in a form made for its curve, and the chapter checks it against the 19 official test vectors."),
        "lesson": "A patent decided which signature Bitcoin started with",
        "source": ("The patent record US4995082A (inventor Claus P. Schnorr; filing date 1990-02-23; publication date 1991-02-19; priority 1989-02-24; the status 'Expired - Lifetime' "
                   "is marked by the site as an assumption), 35 U.S. Code section 154 (the greater of the 20-year term and 17 years from grant for applications filed before mid-1995), Wikipedia's article on the Schnorr signature (expired in February 2010), "
                   "Schnorr's Crypto '89 paper in LNCS 435 (1990) and his 1991 Journal of Cryptology paper, the book's chapter 8 section on ECDSA, and BIP340. All saved in "
                   "08-tooling/ch08-evidence. Photo: Claus-Peter Schnorr at Oberwolfach, 1986 - Konrad Jacobs (Mathematisches Forschungsinstitut Oberwolfach), CC BY-SA 2.0 de, "
                   "Wikimedia Commons File:Claus-Peter Schnorr.jpg."),
        "photo": "ch08_schnorr.jpg",
        "credit": "Claus-Peter Schnorr, Oberwolfach, 1986 - Konrad Jacobs, MFO, CC BY-SA 2.0 de, Wikimedia Commons",
    },
    {
        "id": "AndroidRandom",
        "title": "When the phone's random numbers were not random",
        "when": "2013-08-11",
        "who": "Alex Klyubin, the Android security engineer who explained the cause; the Bitcoin Wallet, blockchain.info, BitcoinSpinner and Mycelium Wallet teams that released updates; Soo Hyeon Kim, Daewan Han and Dong Hoon Lee, who reported the flaw to Google",
        "where": "Android phones worldwide, and the Bitcoin.org network alert; Android Developers Blog, 14 August 2013",
        "link": "https://bitcoin.org/en/alert/2013-08-11-android",
        "concepts": ["NonceReuse", "DeterministicSigning", "Rfc6979Vector"],
        "story": ("On 11 August 2013 Bitcoin.org published an alert that the Android component that generates secure random numbers contained critical weaknesses, "
                  "which made every wallet generated on Android vulnerable to theft, and named Bitcoin Wallet, blockchain.info, BitcoinSpinner and Mycelium Wallet; "
                  "Bitcoin Wallet 3.15 rotated keys automatically. On 14 August the Android security engineer Alex Klyubin wrote that the cause was an improper initialization of "
                  "the underlying pseudo-random number generator, that the investigation had begun with the compromise of one bitcoin transaction, and that developers should seed "
                  "it from /dev/urandom. The sources do not say which flaw the thief used; the chapter shows why such a weakness is fatal for signatures: when two ECDSA signatures from "
                  "one key share a nonce, the private key follows from a few modular subtractions and divisions, and the chapter's script recovers a test key that way. This is why the book "
                  "asks for the deterministic nonce of RFC 6979 and why Bitcoin Core now derives its nonces from the key and the message."),
        "lesson": "Weak randomness at signing time gives away the private key",
        "source": ("The Bitcoin.org alert 'Android Security Vulnerability' of 11 August 2013 (critical weaknesses in the component that generates secure random numbers; the four named wallets; "
                   "Bitcoin Wallet update 3.15), the Android Developers Blog post 'Some SecureRandom Thoughts' of 14 August 2013 by Alex Klyubin (improper initialization of the underlying PRNG; "
                   "the three reporters), the book's section on the importance of randomness, and RFC 6979, all saved in 08-tooling/ch08-evidence; the nonce-reuse recovery is executed in "
                   "sen0401_ch08_claims_v1_0_0.py. Picture: the Android robot, designed by Irina Blok for Google Inc., CC BY 3.0, Wikimedia Commons File:Android robot.svg; it shows "
                   "the platform, not the incident."),
        "photo": "ch08_android.png",
        "credit": "The Android robot - Google Inc., designed by Irina Blok, CC BY 3.0, Wikimedia Commons",
    },
    {
        "id": "BookSignature",
        "title": "The signature on the page is a real payment",
        "when": "2013-12-27",
        "who": "the unnamed sender of a transaction mined in block 277,316 on 27 December 2013; Andreas M. Antonopoulos and David A. Harding, who printed its signature in Mastering Bitcoin",
        "where": "block 277,316 of the Bitcoin main chain; the signature appears in the DER section of chapter 8 of the 3rd edition",
        "link": "https://mempool.space/tx/0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2",
        "concepts": ["DerLayout", "BookSampleOnChain", "BookSampleVerifies"],
        "story": ("The long hexadecimal string that chapter 8 of Mastering Bitcoin uses to explain the DER layout, beginning 3045022100884d142d, is not an invented example: "
                  "it is the signature in the input of transaction 0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2, mined in block 277,316 at 23:11:54 UTC on 27 December 2013. "
                  "The chapter's script splits it into the nine DER elements (a 72-byte signature with the SIGHASH_ALL byte 01 at the end), finds that Bitcoin Core's strict-encoding rule accepts it, "
                  "and recomputes the legacy signature hash of the transaction to show that the signature really verifies against the 65-byte uncompressed public key in the same input. "
                  "Changing the flag byte to NONE makes it fail. The signature is also an example of the older ECDSA style: its R value begins with 0x88, so a padding zero makes it 72 bytes, "
                  "which a modern Bitcoin Core avoids by grinding for a small R."),
        "lesson": "Even a textbook example can be checked against the chain",
        "source": ("The mempool.space record of transaction 0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2 (block height 277,316; block time 1388185914, that is 2013-12-27 23:11:54 UTC; "
                   "the scriptsig with the signature, saved in 08-tooling/ch08-evidence), the book's chapter 8 DER section, and Bitcoin Core's interpreter.cpp (IsValidSignatureEncoding); verified by "
                   "K.book_sample_in_mainnet_tx and K.book_sample_verifies in sen0401_ch08_claims_v1_0_0.py. Picture: a screenshot of Bitcoin-qt 0.5.2 on Windows 7 taken on 21 February 2012 by "
                   "JimNelin, MIT licence, Wikimedia Commons File:Screenshot of Bitcoin-qt-0.5.2.png; it is a wallet of the same era, not the sender's wallet."),
        "photo": "ch08_bitcoinqt.png",
        "credit": "Screenshot of Bitcoin-qt 0.5.2 - JimNelin, MIT licence, Wikimedia Commons",
    },
]


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for s in STORIES:
        for f in ("id", "title", "when", "who", "where", "link", "concepts", "story", "lesson", "source", "credit", "photo"):
            v = s.get(f)
            if not v or "TODO" in str(v):
                bad.append("%s: field %s empty or TODO" % (s.get("id"), f))
        if len(str(s.get("lesson", "")).split()) > 14:
            bad.append("%s: lesson over 14 words" % s.get("id"))
        if not (2 <= str(s.get("story", "")).count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % s.get("id"))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(s.get("when", ""))):
            bad.append("%s: when is not an ISO date" % s.get("id"))
        if not str(s.get("link", "")).startswith("https://"):
            bad.append("%s: link is not https" % s.get("id"))
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "03-materials", "ch08", "assets", str(s.get("photo", "")))
        if s.get("photo") and not os.path.exists(p):
            bad.append("%s: picture file %s missing" % (s.get("id"), s.get("photo")))
    if len(STORIES) < 3:
        bad.append("fewer than three stories")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print("\n".join(b) or "stories ok")
    raise SystemExit(1 if b else 0)
