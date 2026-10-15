#!/usr/bin/env python3
"""inputs_make v1_0_0 (SEN0401 chapter 8 page). Writes the page's authored inputs (objectives, quiz, question_bank, discussion, resources, stories_img, test_config, all v1_0_0) from the chapter's page data
(page_data_v*.json, the concepts exactly as the research states them) and from the deck's own links. Nothing here adds or rewords research prose: a question's right answer is the FIRST SENTENCE of the concept's
own explanation, its wrong answers are first sentences of other concepts, and its rationale names the concept the wrong answer belongs to. Run after sen0401_page_data_v2_12_0.py has written page_data.
Usage: inputs_make_v1_0_0.py PAGEVER   (e.g. 9_42_0)"""
__version__ = "1.0.0"
import hashlib, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); PV = sys.argv[1]
d = json.load(open(os.path.join(H, "page_data_v%s.json" % PV))); nodes = d["nodes"]; by = {n["id"]: n for n in nodes}
def top(n):
    while n["parent"]: n = by[n["parent"]]
    return n["id"]
def first(n):
    t = (n["paras"][0]["text"] if n["paras"] else n["body"]).strip()
    m = re.search(r"(?<=[a-z0-9\)])\. (?=[A-Z])", t)
    s = t[:m.start() + 1] if m else t
    return s if len(s) <= 230 else s[:s.rfind(" ", 0, 227)] + " ..."
J = lambda name, obj: json.dump(obj, open(os.path.join(H, name), "w"), indent=1, ensure_ascii=False)
# ---- objectives -----------------------------------------------------------------------------------------------
CO = {"CO1": ["Sign and verify a message with the ECDSA equations on the chapter's curve, say which three inputs verification needs, and explain why exponents are reduced modulo n while coordinates are reduced modulo p", "Apply"],
      "CO2": ["Decide, for each signature hash flag with and without ANYONECANPAY, which parts of a transaction a signature commits to, and explain the SIGHASH_SINGLE bug and how Bitcoin Core refuses it", "Analyze"],
      "CO3": ["Follow the step from an identity proof to a Fiat-Shamir signature and check a BIP340 signature: 64 bytes, an x-only key, a tagged hash and a default nonce", "Apply"],
      "CO4": ["Explain why naive key aggregation fails (the key cancellation attack), what MuSig2 changes, and how Shamir secret sharing gives any two of three shares the secret and one share nothing", "Analyze"],
      "CO5": ["Judge the safety of a signing nonce: reuse, deterministic nonces by RFC 6979, low-R grinding and the size of a DER signature, with the Android random-number failure as the case", "Evaluate"],
      "CO6": ["Separate what consensus requires of a signature from what relay policy requires (strict DER, low S, taproot hash types), and name what has changed in the standards and in Bitcoin Core since the book went to print", "Understand"]}
J("objectives_v1_0_0.json", dict({"_version": "1.0.0"}, **CO, _serves="These six outcomes are chapter 8's: what a signature is and what it commits to (CO1, CO2), schnorr signatures and their aggregation (CO3, CO4), the safety of the nonce and the size of a signature (CO5), and how a node judges a signature and what has moved since print (CO6). The chapter serves LO-6 of the course (reading and constructing transactions, scripts and signatures and explaining how a node decides whether one is valid); CO2 and CO6 also touch LO-5 and LO-8 through the policy and security questions they raise."))
# ---- question bank: one item per concept ---------------------------------------------------------------------
OBJ = {"SignatureFoundations": "CO1", "SighashFlags": "CO2", "SchnorrSignatures": "CO3", "EcdsaSignatures": "CO1", "Randomness": "CO5", "SegwitSigning": "CO2", "SinceTheBook": "CO6"}
OBJ_G = {"Aggregation": "CO4", "ThresholdSharing": "CO4", "ConsensusAndPolicy": "CO6"}
def obj(n):
    k = n
    while k:
        if k["id"] in OBJ_G: return OBJ_G[k["id"]]
        k = by[k["parent"]] if k["parent"] else None
    return OBJ[top(n)]
bank = []; pool = sorted(nodes, key=lambda n: hashlib.sha256(n["id"].encode()).hexdigest())
for n in nodes:
    right = first(n); others = []
    for m in pool:
        if m["id"] == n["id"] or top(m) == top(n) and len(others) < 1: continue
        s = first(m)
        if s != right and all(first(o) != s for o in others): others.append(m)
        if len(others) == 3: break
    opts = [(right, None)] + [(first(m), m) for m in others]
    order = sorted(range(4), key=lambda i: hashlib.sha256((n["id"] + str(i)).encode()).hexdigest())
    options = [opts[i][0] for i in order]; ans = order.index(0)
    lv = "Remember"
    why = "That sentence opens the chapter's explanation of '%s'. The others open the explanations of %s." % (n["label"], ", ".join("'%s'" % m["label"] for _, m in sorted([o for o in opts if o[1]], key=lambda o: o[1]["label"])))
    bank.append({"concept": n["id"], "level": lv, "q": "Which of these sentences opens the explanation of '%s' in this chapter?" % n["label"], "options": options, "answer": ans, "why": why})
J("question_bank_v1_0_0.json", bank)
# ---- quiz: twelve of those items, spread over the branches ----------------------------------------------------
pick = []
for t in [x["id"] for x in nodes if x["level"] == 1]:
    ls = [b for b in bank if top(by[b["concept"]]) == t and by[b["concept"]]["level"] >= 3]
    pick += ls[:2] if t in ("SighashFlags", "SchnorrSignatures", "EcdsaSignatures", "Randomness", "SegwitSigning") else ls[:1]
items = []
for b in pick:
    n = by[b["concept"]]; wrong = [o for i, o in enumerate(b["options"]) if i != b["answer"]]
    items.append({"q": b["q"], "options": b["options"], "answer": b["answer"], "level": "Remember", "objective": obj(n), "rationales": ["This sentence opens the explanation of another concept of the chapter." for _ in wrong]})
J("quiz_v1_0_0.json", {"_version": "1.0.0", "items": items})
J("discussion_v1_0_0.json", {"_version": "1.0.0", "items": [["Noticeable issues", "What stood out in this chapter, and what surprised you about what a Bitcoin signature does and does not commit to?"],
  ["Interesting details", "Which of the chapter's attacks or failures (key cancellation, nonce reuse, the Android random numbers, the SIGHASH_SINGLE bug) would you test first in a new wallet library, and how?"],
  ["Unclarified issues", "Which points need further explanation? Select one critical issue from the chapter and explain it."]]})
# ---- resources -----------------------------------------------------------------------------------------------
L = lambda kind, title, url, source, why, concept: {"kind": kind, "title": title, "url": url, "source": source, "why": why, "concept": concept}
links = [
 L("standard", "BIP 340: Schnorr Signatures for secp256k1", "https://bips.dev/340/", "bips.dev", "The format of the 64-byte signatures and x-only keys that the chapter's checks run against its 19 published test vectors.", "Bip340Format"),
 L("standard", "BIP 327: MuSig2 for BIP340-compatible Multi-Signatures", "https://bips.dev/327/", "bips.dev", "The key aggregation that blocks the key cancellation attack.", "MuSigKeyAgg"),
 L("standard", "RFC 6979: Deterministic Usage of DSA and ECDSA", "https://www.rfc-editor.org/rfc/rfc6979.txt", "rfc-editor.org", "The deterministic nonce whose published test vector the chapter reproduces.", "Rfc6979Vector"),
 L("seminal", "Schnorr, C. P.: Efficient signature generation by smart cards (Journal of Cryptology, 1991)", "https://link.springer.com/article/10.1007/BF00196725", "Springer Nature Link", "The paper behind the patent story and the signature scheme itself.", "FiatShamirSignature"),
 L("corpus", "Mastering Bitcoin, the book (Antonopoulos)", "https://aantonop.com/books/mastering-bitcoin/", "aantonop.com", "The chapter this page re-reads, free to read, CC BY-SA 4.0.", "SignatureFoundations"),
 L("documentation", "OP_CHECKSIG - Bitcoin Wiki", "https://en.bitcoin.it/wiki/OP_CHECKSIG", "en.bitcoin.it", "How the script operation that checks a signature builds the signed digest.", "DigestCommitment"),
 L("video", "Blockchain and Money (MIT OpenCourseWare 15.S12)", "https://ocw.mit.edu/courses/15-s12-blockchain-and-money-fall-2018/", "MIT OpenCourseWare", "Lectures on digital signatures and Bitcoin, free to watch.", "SignatureRoles"),
 L("video", "Bitcoin Optech Schnorr Taproot Workshop", "https://bitcoinops.org/en/schnorr-taproot-workshop/", "bitcoinops.org", "Workshop videos on schnorr signatures, MuSig and taproot; the deck's suggested start.", "SchnorrSignatures"),
 L("community", "Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/", "bitcoinops.org", "Where changes to standards and to Bitcoin Core are reported week by week, after the book went to print.", "SinceTheBook"),
 L("community", "Delving Bitcoin", "https://delvingbitcoin.org/", "delvingbitcoin.org", "A research forum where proposals such as threshold signatures are discussed.", "ThresholdBipGap"),
 L("community", "The bitcoin-dev mailing list", "https://groups.google.com/g/bitcoindev", "Google Groups", "The list on which BIP 66 and the schnorr proposal were announced.", "StrictDerConsensus")]
J("resources_v1_0_0.json", {"_version": "1.0.0", "checked": "2026-10-15", "links": links, "_note": "The eleven links are the links of the chapter 8 deck's resources slide. Each was fetched over HTTPS on 2026-10-15 from this session and answered 200 (a ranged request answered 206); the title is the page's own title line. YouTube answered 429 from this machine, so no YouTube link is listed: a link that was not opened is not listed."})
J("stories_img_v1_0_0.json", {"_version": "1.0.0", "_note": "Story pictures for the chapter 8 page's Stories tab, from the stories module sen0401_ch08_stories_v1_1_0.py (the photo field of each story); licences in 03-materials/ch08/assets/ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md. The picture of BookSignature is a stand-in (the Bitcoin logo, public domain), as the deck's slide 17 says; AndroidRandom's is the platform, not the incident (slide 19).",
  "SchnorrPatent": [{"file": "ch08_schnorr.png", "credit": "Claus-Peter Schnorr, Oberwolfach, 1986 - Konrad Jacobs, MFO, CC BY-SA 2.0 de, Wikimedia Commons"}],
  "AndroidRandom": [{"file": "ch08_android.png", "credit": "The Android robot - Google Inc., designed by Irina Blok, CC BY 3.0, Wikimedia Commons (stand-in picture: the platform, not the incident)"}],
  "BookSignature": [{"file": "ch08_bitcoinlogo.png", "credit": "Bitcoin logo - Grayliptrot, public domain, Wikimedia Commons (stand-in picture: the logo, not the sender or the transaction)"}]})
print("bank %d, quiz %d, resources %d" % (len(bank), len(items), len(links)))
