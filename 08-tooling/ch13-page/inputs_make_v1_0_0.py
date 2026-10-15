#!/usr/bin/env python3
"""inputs_make v1_0_0 (SEN0401 chapter 13 page). Writes the page's authored inputs (objectives, quiz, question_bank, discussion, resources, stories_img, test_config, all v1_0_0) from the chapter's page data
(page_data_v*.json, the concepts exactly as the research states them) and from the deck's own links. Nothing here adds or rewords research prose: a question's right answer is the FIRST SENTENCE of the concept's
own explanation, its wrong answers are first sentences of other concepts, and its rationale names the concept the wrong answer belongs to. Run after sen0401_page_data_v2_18_0.py has written page_data.
Usage: inputs_make_v1_0_0.py PAGEVER   (e.g. 9_48_0)"""
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
CO = {"CO1": ["Explain what the security model of Bitcoin protects (a signed transaction can be published, the transport can be encrypted) and how a user checks the software and the root of trust", "Understand"],
      "CO2": ["Compare cold storage, wallet encryption, signing devices and paper or memory as ways to protect keys, and judge what each one does and does not defend against", "Analyze"],
      "CO3": ["Explain how seed words and wallet backups keep access to coins, including the BIP 39 checksum, the descriptor in a backup and the risk of a stale backup", "Apply"],
      "CO4": ["Compute the odds of loss and theft of a single key against a 2-of-3 multisignature wallet, and explain how Shamir's scheme shares a secret so that one piece reveals nothing", "Analyze"],
      "CO5": ["Learn from the custody failures of Mt. Gox and Bitfinex and from physical coins what a custodian can and cannot be trusted with", "Evaluate"],
      "CO6": ["Design a delayed path for an heir with a timelock and state the limits of the chapter's experiments, what was not executed", "Apply"]}
J("objectives_v1_0_0.json", dict({"_version": "1.0.0"}, **CO, _serves="These six outcomes are chapter 13's: the security model (CO1), protecting keys (CO2), keeping access (CO3), sharing control (CO4), custody history (CO5) and survivability (CO6). The chapter serves LO-6 of the course (reading and constructing transactions, scripts and signatures and explaining how a node decides whether one is valid). Each outcome is worded with one level of Bloom's taxonomy (Understand, Apply, Analyze or Evaluate here). Written by the page author from the chapter's own subjects; the research states no learning outcomes of its own."))
# ---- question bank: one item per concept ---------------------------------------------------------------------
OBJ = {"SecurityModel": "CO1", "ProtectingKeys": "CO2", "KeepingAccess": "CO3", "SharingControl": "CO4", "CustodyHistory": "CO5", "Survivability": "CO6"}
OBJ_G = {}
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
    pick += ls[:2] if t in ("SecurityModel", "ProtectingKeys", "KeepingAccess", "SharingControl") else ls[:1]
items = []
for b in pick:
    n = by[b["concept"]]; wrong = [o for i, o in enumerate(b["options"]) if i != b["answer"]]
    items.append({"q": b["q"], "options": b["options"], "answer": b["answer"], "level": "Remember", "objective": obj(n), "rationales": ["This sentence opens the explanation of another concept of the chapter." for _ in wrong]})
J("quiz_v1_0_0.json", {"_version": "1.0.0", "items": items})
J("discussion_v1_0_0.json", {"_version": "1.0.0", "items": [["Noticeable issues", "What stood out in this chapter, and what surprised you about how much a signed transaction can safely reveal, or how a locked wallet still shows its balance?"],
  ["Interesting details", "Which of the chapter's cases (the lost seven thousand bitcoin, the heir who must wait ten blocks, the Mt. Gox hot wallet) would you test first on a regtest chain of your own, and how?"],
  ["Unclarified issues", "Which points need further explanation? Select one critical issue from the chapter and explain it."]]})
# ---- resources -----------------------------------------------------------------------------------------------
L = lambda kind, title, url, source, why, concept: {"kind": kind, "title": title, "url": url, "source": source, "why": why, "concept": concept}
links = [
 L("documentation", "Optech topic: Partially signed bitcoin transactions", "https://bitcoinops.org/en/topics/psbt/", "bitcoinops.org", "The newsletter topic page on PSBTs, the format that carries a transaction between a hot and a cold wallet.", "PsbtThroughColdNode"),
 L("documentation", "Optech topic: Output script descriptors", "https://bitcoinops.org/en/topics/output-script-descriptors/", "bitcoinops.org", "The newsletter topic page on descriptors, the part of a backup that says what the keys control.", "DescriptorIsPartOfBackup"),
 L("documentation", "Optech topic: Timelocks", "https://bitcoinops.org/en/topics/timelocks/", "bitcoinops.org", "The newsletter topic page on timelocks, the tool behind the heir's delayed path.", "HeirWaitsTenBlocks"),
 L("standard", "BIP 324: Version 2 P2P Encrypted Transport Protocol", "https://bips.dev/324/", "bips.dev", "The specification of the encrypted transport that is on by default since release 27.0.", "V2SessionOnBothSides"),
 L("standard", "BIP 39: Mnemonic code for generating deterministic keys", "https://bips.dev/39/", "bips.dev", "The specification of seed words and their checksum.", "Bip39MnemonicChecksum"),
 L("seminal", "Shamir: How to Share a Secret (1979)", "https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf", "web.mit.edu", "The paper behind the chapter's two-of-three sharing of a secret.", "ShamirTwoOfThree"),
 L("video", "Stand-up Maths: how to keep an open secret (video)", "https://www.youtube.com/embed/K54ildEW9-Q", "youtube.com", "A talk on sharing a secret in pieces; the deck's suggested start.", "OneShareRevealsNothing"),
 L("video", "Unchained: what is bitcoin multisig (video)", "https://www.youtube.com/embed/pOr6dwb7-dw", "youtube.com", "A short lesson on multisignature wallets.", "TwoOfThreeSigning"),
 L("community", "Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/", "bitcoinops.org", "Where changes to wallets, signing devices and security practice are reported week by week, after the book went to print.", "ExternalSignerSupport"),
 L("community", "Delving Bitcoin", "https://delvingbitcoin.org/", "delvingbitcoin.org", "A research forum where wallet security and key management are discussed.", "ColdStorage"),
 L("community", "The bitcoin-dev mailing list", "https://groups.google.com/g/bitcoindev", "Google Groups", "The list on which wallet and security proposals are argued.", "Codex32AndSlip39")]
J("resources_v1_0_0.json", {"_version": "1.0.0", "checked": "2026-10-15", "links": links, "_note": "The eleven links are the links of the chapter 13 deck's last slide (Where to go from here), which states that every link was opened on 2026-10-15; this page author did not fetch them again. The YouTube links are the embed addresses the deck gives."})
J("stories_img_v1_0_0.json", {"_version": "1.0.0", "_note": "Story pictures for the chapter 13 page's Stories tab, from the deck's own placements (08-tooling/ch13-deck/deck_content_v1_0_0.py); licences in 03-materials/ch13/assets/ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md. Three pictures are stand-ins and say so, as the deck's slides 15, 16 and 22 do; the portrait of Adi Shamir (slide 23) is the real thing.",
  "TrezorSecureElement": [{"file": "trezor_model_t.png", "credit": "Trezor Model T - FlippyFlink, CC0 1.0, Wikimedia Commons (stand-in picture: a Trezor Model T, not the Safe 5)"}],
  "CasasciusCoins": [{"file": "casascius_hologram.png", "credit": "Casascius hologram close-up - BTC Keychain, CC BY 2.0, Flickr (stand-in picture: a hologram close-up, not the coin)"}],
  "MtGoxHotWallet": [{"file": "mtgox_letter.png", "credit": "Letter regarding Mt.Gox - NetSPI, CC BY 2.0, Flickr (stand-in picture: a letter about the bankruptcy, not the theft)"}],
  "ShamirSharesTheSecret": [{"file": "adi_shamir.png", "credit": "Adi Shamir Royal Society - Duncan Hull, CC BY-SA 4.0, Wikimedia Commons"}]})
print("bank %d, quiz %d, resources %d" % (len(bank), len(items), len(links)))
