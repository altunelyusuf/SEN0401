#!/usr/bin/env python3
"""inputs_make v1_0_0 (SEN0401 chapter 14 page). Writes the page's authored inputs (objectives, quiz, question_bank, discussion, resources, stories_img, test_config, all v1_0_0) from the chapter's page data
(page_data_v*.json, the concepts exactly as the research states them) and from the deck's own links. Nothing here adds or rewords research prose: a question's right answer is the FIRST SENTENCE of the concept's
own explanation, its wrong answers are first sentences of other concepts, and its rationale names the concept the wrong answer belongs to. Run after sen0401_page_data_v2_19_0.py has written page_data.
Usage: inputs_make_v1_0_0.py PAGEVER   (e.g. 9_50_0)"""
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
CO = {"CO1": ["Explain what the chain guarantees to an application (no double spend, outputs cannot exceed inputs, no expiry) and how applications such as proof of existence and crowdfunding are composed from these building blocks", "Understand"],
      "CO2": ["Explain how an output works as a single-use seal, how a contract stays off the chain, and how colored coins and later asset protocols use this", "Analyze"],
      "CO3": ["Work through a payment channel in satoshis: funding by both keys, refunds with falling lock times, revocable commitments with a penalty, and the HTLC with its secret and timeout branches", "Apply"],
      "CO4": ["Follow a routed payment across the Lightning Network: the fee arithmetic, the timelock staircase, the balances afterwards, and the structure of an invoice", "Apply"],
      "CO5": ["Check the Noise handshake, the transport messages and the onion packet against test vectors, and read a channel on the chain: the funding output, the commitment transaction, a cooperative close and a justice transaction", "Analyze"],
      "CO6": ["Judge what changed since the print (errata, TRUC and anchors, full RBF, other implementations) and the limits of the chapter's experiments", "Evaluate"]}
J("objectives_v1_0_0.json", dict({"_version": "1.0.0"}, **CO, _serves="These six outcomes are chapter 14's: platform guarantees (CO1), colored coins (CO2), payment channels (CO3), the Lightning Network (CO4), the channel on the chain and the packets that carry it (CO5) and what changed since the print (CO6). The chapter serves LO-6 of the course (reading and constructing transactions, scripts and signatures and explaining how a node decides whether one is valid). Each outcome is worded with one level of Bloom's taxonomy (Understand, Apply, Analyze or Evaluate here). Written by the page author from the chapter's own subjects; the research states no learning outcomes of its own."))
# ---- question bank: one item per concept ---------------------------------------------------------------------
OBJ = {"PlatformGuarantees": "CO1", "ColoredCoins": "CO2", "PaymentChannels": "CO3", "LightningNetwork": "CO4", "SinceThePrint": "CO6"}
OBJ_G = {"TransportAndOnion": "CO5", "ChannelOnChain": "CO5"}
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
    pick += ls[:2] if t in ("PlatformGuarantees", "PaymentChannels", "LightningNetwork", "SinceThePrint") else ls[:1]
items = []
for b in pick:
    n = by[b["concept"]]; wrong = [o for i, o in enumerate(b["options"]) if i != b["answer"]]
    items.append({"q": b["q"], "options": b["options"], "answer": b["answer"], "level": "Remember", "objective": obj(n), "rationales": ["This sentence opens the explanation of another concept of the chapter." for _ in wrong]})
J("quiz_v1_0_0.json", {"_version": "1.0.0", "items": items})
J("discussion_v1_0_0.json", {"_version": "1.0.0", "items": [["Noticeable issues", "What stood out in this chapter, and what surprised you about how a channel keeps its promises with only locks, hashes and a penalty?"],
  ["Interesting details", "Which of the chapter's cases (the two pizzas for 10,000 bitcoins, the refund ladder with falling lock times, the hold invoice that keeps a payment in flight) would you test first on a regtest chain of your own, and how?"],
  ["Unclarified issues", "Which points need further explanation? Select one critical issue from the chapter and explain it."]]})
# ---- resources -----------------------------------------------------------------------------------------------
L = lambda kind, title, url, source, why, concept: {"kind": kind, "title": title, "url": url, "source": source, "why": why, "concept": concept}
links = [
 L("documentation", "Optech topic: Hash time locked contracts", "https://bitcoinops.org/en/topics/htlc/", "bitcoinops.org", "The newsletter topic page on HTLCs, the contract that routes a payment.", "HtlcSecretBranch"),
 L("documentation", "Optech topic: Anchor outputs", "https://bitcoinops.org/en/topics/anchor-outputs/", "bitcoinops.org", "The newsletter topic page on anchor outputs, the fee-bumping machinery that came after the book.", "TrucAndAnchors"),
 L("documentation", "Optech topic: Watchtowers", "https://bitcoinops.org/en/topics/watchtowers/", "bitcoinops.org", "The newsletter topic page on watchtowers, which punish a breach while the owner is offline.", "BreachJusticeTransaction"),
 L("standard", "BOLT 3: Bitcoin transaction and script formats", "https://raw.githubusercontent.com/lightning/bolts/master/03-transactions.md", "github.com", "The specification of the commitment and HTLC transactions the chapter reads on the chain.", "CommitmentTransactionShape"),
 L("standard", "BIP 112: CHECKSEQUENCEVERIFY", "https://bips.dev/112/", "bips.dev", "The relative timelock behind the revocable commitments.", "CsvDelayThousandVersus2016"),
 L("seminal", "Poon and Dryja: The Bitcoin Lightning Network (draft 0.5.9.2)", "https://lightning.network/lightning-network-paper.pdf", "lightning.network", "The paper that started the Lightning Network.", "WhitepaperDate"),
 L("video", "CuriousInventor: how Lightning works (video)", "https://www.youtube.com/embed/yKdK-7AtAMQ", "youtube.com", "A visual explanation of channels and routed payments; the deck's suggested start.", "RoutedPayment"),
 L("video", "Poon and Dryja at Coinbase (video)", "https://www.youtube.com/embed/KN7Z5dGWcRY", "youtube.com", "The authors present the Lightning Network.", "PoonDryja" if False else "WhitepaperDate"),
 L("community", "mempool.space, the Lightning explorer", "https://mempool.space/lightning", "mempool.space", "A live view of the public Lightning graph whose size the chapter measures.", "MainnetGraphSize"),
 L("community", "Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/", "bitcoinops.org", "Where changes to Lightning and to the base layer are reported week by week, after the book went to print.", "NewMachinery"),
 L("community", "Delving Bitcoin", "https://delvingbitcoin.org/", "delvingbitcoin.org", "A research forum where Lightning and channel designs are discussed.", "ProposalsStillDrafts")]
J("resources_v1_0_0.json", {"_version": "1.0.0", "checked": "2026-10-15", "links": links, "_note": "The eleven links are the links of the chapter 14 deck's last slide (Where to go from here), which states that every link was opened on 2026-10-15; this page author did not fetch them again. The YouTube links are the embed addresses the deck gives."})
J("stories_img_v1_0_0.json", {"_version": "1.0.0", "_note": "Story pictures for the chapter 14 page's Stories tab, from the deck's own placements (08-tooling/ch14-deck/deck_content_v1_0_0.py); licences in 03-materials/ch14/assets/ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md. Three pictures are stand-ins and say so, as the deck's slides 5, 10 and 22 do; the portrait of Jack Dorsey (slide 23) is the real thing.",
  "PizzaForBitcoins": [{"file": "papa_johns_jacksonville.png", "credit": "Papa Johns Jacksonville - Sanjev Rajaram, CC0 1.0, Wikimedia Commons (stand-in picture: a Papa Johns shop in Florida, not the 2010 order)"}],
  "SpillmanChannels": [{"file": "micropayment_channel_construction.png", "credit": "Construction of a micropayment channel - Burchert, Decker, Wattenhofer, CC BY 4.0, Wikimedia Commons (stand-in picture: a 2018 diagram of a channel, not the 2013 thread)"}],
  "PoonDryjaWhitepaper": [{"file": "lightning_cut_nodes.png", "credit": "Lightning Network cut nodes - FrankAndProust, CC0 1.0, Wikimedia Commons (stand-in picture: a chart of cut nodes, not the authors)"}],
  "LightningTorch": [{"file": "jack_dorsey_2009.png", "credit": "Jack Dorsey 2009 - Brian Solis, CC BY 2.0, Wikimedia Commons"}]})
print("bank %d, quiz %d, resources %d" % (len(bank), len(items), len(links)))
