#!/usr/bin/env python3
"""inputs_make v1_0_0 (SEN0401 chapter 12 page). Writes the page's authored inputs (objectives, quiz, question_bank, discussion, resources, stories_img, test_config, all v1_0_0) from the chapter's page data
(page_data_v*.json, the concepts exactly as the research states them) and from the deck's own links. Nothing here adds or rewords research prose: a question's right answer is the FIRST SENTENCE of the concept's
own explanation, its wrong answers are first sentences of other concepts, and its rationale names the concept the wrong answer belongs to. Run after sen0401_page_data_v2_17_0.py has written page_data.
Usage: inputs_make_v1_0_0.py PAGEVER   (e.g. 9_47_0)"""
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
CO = {"CO1": ["Compute the block subsidy at any height from the halving every 210,000 blocks, show why the total supply stays below 21 million, and say what a miner may claim as reward (subsidy plus fees)", "Apply"],
      "CO2": ["Describe the checklists every node applies to a transaction and to a block, and explain why the chain with the most work, not the longest, is the best chain", "Understand"],
      "CO3": ["Build a candidate block: choose transactions from the template by fee rate, write the coinbase transaction and its fields, and fill in the header", "Apply"],
      "CO4": ["Explain proof of work as a lottery of hashes below a target, convert between target, bits, difficulty and hash rate, and apply the retargeting formula every 2,016 blocks", "Analyze"],
      "CO5": ["Judge the competition among miners: the nonce and extra nonce space, the pools and their shares, and the limits of selfish-mining and majority attacks", "Evaluate"],
      "CO6": ["Compare hard forks and soft forks, follow a deployment through the BIP 9 state machine, and explain how taproot was activated", "Analyze"]}
J("objectives_v1_0_0.json", dict({"_version": "1.0.0"}, **CO, _serves="These six outcomes are chapter 12's: money creation (CO1), decentralized consensus (CO2), building the candidate block (CO3), proof of work (CO4), mining competition (CO5) and changing consensus rules (CO6). The chapter serves LO-6 of the course (reading and constructing transactions, scripts and signatures and explaining how a node decides whether one is valid). Each outcome is worded with one level of Bloom's taxonomy (Understand, Apply, Analyze or Evaluate here). Written by the page author from the chapter's own subjects; the research states no learning outcomes of its own."))
# ---- question bank: one item per concept ---------------------------------------------------------------------
OBJ = {"MoneyCreation": "CO1", "DecentralizedConsensus": "CO2", "BuildingTheCandidateBlock": "CO3", "ProofOfWork": "CO4", "MiningCompetition": "CO5", "ChangingConsensusRules": "CO6"}
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
    pick += ls[:2] if t in ("MoneyCreation", "ProofOfWork", "MiningCompetition", "ChangingConsensusRules") else ls[:1]
items = []
for b in pick:
    n = by[b["concept"]]; wrong = [o for i, o in enumerate(b["options"]) if i != b["answer"]]
    items.append({"q": b["q"], "options": b["options"], "answer": b["answer"], "level": "Remember", "objective": obj(n), "rationales": ["This sentence opens the explanation of another concept of the chapter." for _ in wrong]})
J("quiz_v1_0_0.json", {"_version": "1.0.0", "items": items})
J("discussion_v1_0_0.json", {"_version": "1.0.0", "items": [["Noticeable issues", "What stood out in this chapter, and what surprised you about how the reward halves, how a hash lottery needs no trust, or how little a block's check costs against its search?"],
  ["Interesting details", "Which of the chapter's cases (block 840,000 where the tips beat the subsidy, the chain split of March 2013, the activation of taproot) would you test first on a regtest chain of your own, and how?"],
  ["Unclarified issues", "Which points need further explanation? Select one critical issue from the chapter and explain it."]]})
# ---- resources -----------------------------------------------------------------------------------------------
L = lambda kind, title, url, source, why, concept: {"kind": kind, "title": title, "url": url, "source": source, "why": why, "concept": concept}
links = [
 L("documentation", "Optech topic: Soft fork activation", "https://bitcoinops.org/en/topics/soft-fork-activation/", "bitcoinops.org", "The newsletter topic page on how soft forks are activated, from BIP 9 to Speedy Trial.", "Bip9StateMachine"),
 L("documentation", "Optech topic: Selfish mining", "https://bitcoinops.org/en/topics/selfish-mining/", "bitcoinops.org", "The newsletter topic page on the selfish-mining attack.", "SelfishMiningThreshold"),
 L("community", "mempool.space, the block explorer", "https://mempool.space/", "mempool.space", "A block explorer where the blocks, difficulty adjustments and pools the chapter reads can be looked up live.", "RecentAdjustments"),
 L("standard", "BIP 9: Version bits with timeout and delay", "https://bips.dev/9/", "bips.dev", "The specification of the state machine the chapter runs on regtest.", "Bip9StateMachine"),
 L("standard", "BIP 54: Consensus cleanup", "https://bips.dev/54/", "bips.dev", "The proposal that closes the time-warp and related weaknesses of the retargeting rule.", "Bip54ConsensusCleanup"),
 L("seminal", "Eyal and Sirer: Majority is not enough (arXiv)", "https://arxiv.org/abs/1311.0243", "arxiv.org", "The paper behind the selfish-mining threshold of the chapter.", "SelfishMiningThreshold"),
 L("video", "3Blue1Brown: how does bitcoin actually work (video)", "https://www.youtube.com/embed/bBC-nXj3Ng4", "youtube.com", "A visual explanation of the proof-of-work lottery; the deck's suggested start.", "HelloWorldNonce"),
 L("video", "Khan Academy: Bitcoin, proof of work (video)", "https://www.youtube.com/embed/9V1bipPkCTU", "youtube.com", "A short lesson on proof of work and why it is costly to produce and cheap to check.", "ProofIsCheapToCheck"),
 L("community", "Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/", "bitcoinops.org", "Where changes to mining, Stratum and consensus rules are reported week by week, after the book went to print.", "StratumProtocols"),
 L("community", "Delving Bitcoin", "https://delvingbitcoin.org/", "delvingbitcoin.org", "A research forum where mining, block templates and consensus changes are discussed.", "BlockTemplate"),
 L("community", "The bitcoin-dev mailing list", "https://groups.google.com/g/bitcoindev", "Google Groups", "The list on which soft fork activation methods were argued.", "SpeedyTrialTaproot")]
J("resources_v1_0_0.json", {"_version": "1.0.0", "checked": "2026-10-15", "links": links, "_note": "The eleven links are the links of the chapter 12 deck's last slide (Where to go from here), which states that every link was opened on 2026-10-15; this page author did not fetch them again. The YouTube links are the embed addresses the deck gives."})
J("stories_img_v1_0_0.json", {"_version": "1.0.0", "_note": "Story pictures for the chapter 12 page's Stories tab, from the deck's own placements (08-tooling/ch12-deck/deck_content_v1_0_0.py); licences in 03-materials/ch12/assets/ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md. Three pictures are stand-ins and say so, as the deck's slides 7, 22 and 23 do; the portrait of Adam Back (slide 16) is the real thing.",
  "HalvingBlockWithRecordFees": [{"file": "photo_asic_miner.png", "credit": "Antminer ASIC Miner - Steve Rainwater, CC BY-SA 2.0, Wikimedia Commons (stand-in picture: a miner of the kind, not the one)"}],
  "HashcashBeforeBitcoin": [{"file": "photo_adam_back.png", "credit": "Adam Back - Joi Ito, CC BY 2.0, Wikimedia Commons"}],
  "ChainSplitOfMarch2013": [{"file": "photo_fork_in_the_road.png", "credit": "Fork in the road - Ian Sane, CC BY 2.0, Flickr (stand-in picture: a fork in a road, not the split)"}],
  "TaprootThroughSpeedyTrial": [{"file": "photo_taproot_profile.png", "credit": "Taproot profile - Forest and Kim Starr, CC BY 3.0, Wikimedia Commons (stand-in picture: a tree's taproot, not the soft fork)"}]})
print("bank %d, quiz %d, resources %d" % (len(bank), len(items), len(links)))
