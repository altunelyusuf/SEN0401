#!/usr/bin/env python3
"""inputs_make v1_0_0 (SEN0401 chapter 9 page). Writes the page's authored inputs (objectives, quiz, question_bank, discussion, resources, stories_img, test_config, all v1_0_0) from the chapter's page data
(page_data_v*.json, the concepts exactly as the research states them) and from the deck's own links. Nothing here adds or rewords research prose: a question's right answer is the FIRST SENTENCE of the concept's
own explanation, its wrong answers are first sentences of other concepts, and its rationale names the concept the wrong answer belongs to. Run after sen0401_page_data_v2_13_0.py has written page_data.
Usage: inputs_make_v1_0_0.py PAGEVER   (e.g. 9_43_0)"""
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
CO = {"CO1": ["Show that a fee is the gap between what a transaction's inputs hold and its outputs hold, say why only the spender's signature can commit to it, and describe what a miner chooses", "Understand"],
      "CO2": ["Compute the virtual size and the fee rate of a transaction from its weight, convert between the units a node uses, and state the minimum rates and the dust limits a node applies", "Apply"],
      "CO3": ["Explain how a node estimates the fee rate for a target number of blocks from the past, what it needs before it answers, and read the fee market of two mainnet blocks", "Analyze"],
      "CO4": ["State what a replacement transaction must pay, how the opt-in signal differs from full replacement, and judge the hazards that replacement brings", "Apply"],
      "CO5": ["Work out the package fee rate that lifts a cheap parent, explain package relay and the cluster mempool, and say how a large child pins a parent and what version 3 and anchors change", "Analyze"],
      "CO6": ["Explain fee sniping and the lock time defence, and judge how much the defence matters when fees are a small or a large part of a miner's income", "Evaluate"]}
J("objectives_v1_0_0.json", dict({"_version": "1.0.0"}, **CO, _serves="These six outcomes are chapter 9's: who pays a fee and what it is (CO1), how it is priced (CO2), how it is estimated (CO3), how a payment is replaced (CO4), how a cheap parent is lifted and how that can be blocked (CO5), and why the lock time matters (CO6). The chapter serves LO-6 of the course (reading and constructing transactions, scripts and signatures and explaining how a node decides whether one is valid). Each outcome is worded with one level of Bloom's taxonomy (Understand, Apply, Analyze or Evaluate here). Written by the page author from the chapter's own subjects; the research states no learning outcomes of its own."))
# ---- question bank: one item per concept ---------------------------------------------------------------------
OBJ = {"WhoPaysTheFee": "CO1", "FeesAndFeeRates": "CO2", "FeeEstimation": "CO3", "ReplaceByFee": "CO4", "ChildPaysForParent": "CO5", "PinningAndAnchors": "CO5", "FeeSnipingAndIncentives": "CO6"}
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
    pick += ls[:2] if t in ("ReplaceByFee", "ChildPaysForParent", "FeesAndFeeRates", "PinningAndAnchors", "FeeEstimation", "FeeSnipingAndIncentives") else ls[:1]
items = []
for b in pick:
    n = by[b["concept"]]; wrong = [o for i, o in enumerate(b["options"]) if i != b["answer"]]
    items.append({"q": b["q"], "options": b["options"], "answer": b["answer"], "level": "Remember", "objective": obj(n), "rationales": ["This sentence opens the explanation of another concept of the chapter." for _ in wrong]})
J("quiz_v1_0_0.json", {"_version": "1.0.0", "items": items})
J("discussion_v1_0_0.json", {"_version": "1.0.0", "items": [["Noticeable issues", "What stood out in this chapter, and what surprised you about who pays a fee and how a node decides which payment to keep?"],
  ["Interesting details", "Which of the chapter's cases (the replacement a node would not relay, the pinned parent, the carve out that was removed, the block where fees were nearly the reward) would you test first in a new wallet, and how?"],
  ["Unclarified issues", "Which points need further explanation? Select one critical issue from the chapter and explain it."]]})
# ---- resources -----------------------------------------------------------------------------------------------
L = lambda kind, title, url, source, why, concept: {"kind": kind, "title": title, "url": url, "source": source, "why": why, "concept": concept}
links = [
 L("documentation", "Optech topic: Replace by fee", "https://bitcoinops.org/en/topics/replace-by-fee/", "bitcoinops.org", "The newsletter topic page that follows replacement rules and their changes after the book went to print.", "ReplacementRules"),
 L("corpus", "Mastering Bitcoin, the book (Antonopoulos)", "https://aantonop.com/books/mastering-bitcoin/", "aantonop.com", "The chapter this page re-reads, free to read, CC BY-SA 4.0.", "FeeAsDifference"),
 L("community", "mempool.space, the explorer", "https://mempool.space/", "mempool.space", "A live view of the fee market the chapter's census measures on two saved blocks.", "FeeMarketOnMainnet"),
 L("standard", "BIP 125: Opt-in Full Replace-by-Fee Signaling", "https://bips.dev/125/", "bips.dev", "The signal of replaceability that the chapter's replacement examples read from the sequence number.", "ReplaceableSignal"),
 L("standard", "BIP 431: Topologically Restricted Until Confirmation (version 3) Transactions", "https://bips.dev/431/", "bips.dev", "The version-3 policy that caps a child and so ends pinning of the parent.", "TrucPolicy"),
 L("seminal", "Nakamoto, S.: Bitcoin: A Peer-to-Peer Electronic Cash System (2008)", "https://bitcoin.org/bitcoin.pdf", "bitcoin.org", "The paper whose incentive section the chapter's fee sniping story starts from.", "BlockRewardMix"),
 L("video", "Antonopoulos on transaction fees (video)", "https://www.youtube.com/embed/MPQMCVVhExY", "youtube.com", "A talk on fees by the book's author; the deck's suggested start.", "WhoPaysTheFee"),
 L("video", "Blockchain and Money (MIT OpenCourseWare 15.S12)", "https://ocw.mit.edu/courses/15-s12-blockchain-and-money-fall-2018/", "MIT OpenCourseWare", "Lectures on money and Bitcoin, free to watch.", "FeesAndFeeRates"),
 L("community", "Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/", "bitcoinops.org", "Where changes to fee policy and to Bitcoin Core are reported week by week, after the book went to print.", "ClusterMempool"),
 L("community", "Delving Bitcoin", "https://delvingbitcoin.org/", "delvingbitcoin.org", "A research forum where the cluster mempool and package relay were discussed.", "PackageRelay"),
 L("community", "The bitcoin-dev mailing list", "https://groups.google.com/g/bitcoindev", "Google Groups", "The list on which the carve out and full replacement were argued.", "CarveOut")]
J("resources_v1_0_0.json", {"_version": "1.0.0", "checked": "2026-10-15", "links": links, "_note": "The eleven links are the links of the chapter 9 deck's last slide (Where to go from here). Each was fetched over HTTPS on 2026-10-15 from this session and answered 200 (a ranged request answered 206); the YouTube link is the embed address the deck gives, which answered 200."})
J("stories_img_v1_0_0.json", {"_version": "1.0.0", "_note": "Story pictures for the chapter 9 page's Stories tab, from the stories module sen0401_ch09_stories_v1_1_0.py (the photo field of each story); licences in 03-materials/ch09/assets/ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md. Three pictures are stand-ins and say so, as the deck's slides 11, 14 and 20 do; Nassau Hall (slide 23) is the authors' own university.",
  "FullRbfPeering": [{"file": "photo_bitcoin_namecoin_accepted_here_sign.png", "credit": "Bitcoin and Namecoin Accepted Here sign - ninjarobot, CC0, Wikimedia Commons, 2013-06-19 (stand-in picture: a shop sign, not a node)"}],
  "CarveOutProposal": [{"file": "photo_lightning_network_logo.png", "credit": "Lightning Network logo - Ole Henrik Skogstrom, CC BY-SA 4.0, Wikimedia Commons, 2020-04-24 (stand-in picture: the Lightning logo, not the proposal)"}],
  "HalvingBlock": [{"file": "photo_bitcoin_mining_farm.png", "credit": "Bitcoin mining farm - Marko Ahtisaari, CC BY 2.0, Wikimedia Commons, 2014-06-14 (stand-in picture: a mining farm, not this block)"}],
  "InstabilityPaper": [{"file": "photo_nassau_hall_princeton.png", "credit": "Nassau Hall, Princeton University - Smallbones, CC0, Wikimedia Commons, 2012-02-18"}]})
print("bank %d, quiz %d, resources %d" % (len(bank), len(items), len(links)))
