#!/usr/bin/env python3
"""inputs_make v1_0_0 (SEN0401 chapter 11 page). Writes the page's authored inputs (objectives, quiz, question_bank, discussion, resources, stories_img, test_config, all v1_0_0) from the chapter's page data
(page_data_v*.json, the concepts exactly as the research states them) and from the deck's own links. Nothing here adds or rewords research prose: a question's right answer is the FIRST SENTENCE of the concept's
own explanation, its wrong answers are first sentences of other concepts, and its rationale names the concept the wrong answer belongs to. Run after sen0401_page_data_v2_15_0.py has written page_data.
Usage: inputs_make_v1_0_0.py PAGEVER   (e.g. 9_45_0)"""
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
CO = {"CO1": ["Describe what a block holds (a header of six fields in 80 bytes, a transaction count and the transactions), and why the block size field is file storage and the limit is weight", "Understand"],
      "CO2": ["Compute a block's name as the double SHA-256 of its header, and tell a block's hash, its height and its depth apart, including the coinbase maturity of 100 blocks", "Apply"],
      "CO3": ["Recompute the genesis block's hash from its constants and explain what is special about the first block, its message and its coinbase output", "Apply"],
      "CO4": ["Explain how back-links chain blocks, why changing an old block means mining it and every later block again, and how a fork is settled by more work", "Analyze"],
      "CO5": ["Build a merkle root and a merkle path by hand, and judge the two weaknesses of the tree (CVE-2012-2459 duplicates and 64-byte confusion) and how a node defends against them", "Analyze"],
      "CO6": ["Compare mainnet, testnet3 and testnet4, signet and regtest by purpose and rules, and choose the right test chain for a development step", "Evaluate"]}
J("objectives_v1_0_0.json", dict({"_version": "1.0.0"}, **CO, _serves="These six outcomes are chapter 11's: the block and its header (CO1), block names and numbers (CO2), the genesis block (CO3), linking blocks and forks (CO4), merkle trees and proofs (CO5) and the test blockchains (CO6). The chapter serves LO-6 of the course (reading and constructing transactions, scripts and signatures and explaining how a node decides whether one is valid). Each outcome is worded with one level of Bloom's taxonomy (Understand, Apply, Analyze or Evaluate here). Written by the page author from the chapter's own subjects; the research states no learning outcomes of its own."))
# ---- question bank: one item per concept ---------------------------------------------------------------------
OBJ = {"BlockStructure": "CO1", "BlockIdentifiers": "CO2", "GenesisBlock": "CO3", "LinkingBlocks": "CO4", "MerkleTrees": "CO5", "TestBlockchains": "CO6"}
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
    pick += ls[:2] if t in ("BlockStructure", "LinkingBlocks", "MerkleTrees", "TestBlockchains") else ls[:1]
items = []
for b in pick:
    n = by[b["concept"]]; wrong = [o for i, o in enumerate(b["options"]) if i != b["answer"]]
    items.append({"q": b["q"], "options": b["options"], "answer": b["answer"], "level": "Remember", "objective": obj(n), "rationales": ["This sentence opens the explanation of another concept of the chapter." for _ in wrong]})
J("quiz_v1_0_0.json", {"_version": "1.0.0", "items": items})
J("discussion_v1_0_0.json", {"_version": "1.0.0", "items": [["Noticeable issues", "What stood out in this chapter, and what surprised you about how little a block's name says (it is computed, never stored) or how short a proof of a transaction is?"],
  ["Interesting details", "Which of the chapter's cases (the headline in the genesis block, the merkle tree that could be fooled by a duplicated leaf, the testnet that was flooded) would you test first on a regtest chain of your own, and how?"],
  ["Unclarified issues", "Which points need further explanation? Select one critical issue from the chapter and explain it."]]})
# ---- resources -----------------------------------------------------------------------------------------------
L = lambda kind, title, url, source, why, concept: {"kind": kind, "title": title, "url": url, "source": source, "why": why, "concept": concept}
links = [
 L("documentation", "Optech topic: Merkle tree vulnerabilities", "https://bitcoinops.org/en/topics/merkle-tree-vulnerabilities/", "bitcoinops.org", "The newsletter topic page on the duplicate-leaf mutation and the 64-byte weakness of the tree.", "Cve20122459Trees"),
 L("documentation", "Optech topic: Signet", "https://bitcoinops.org/en/topics/signet/", "bitcoinops.org", "The newsletter topic page on signet and its signed blocks.", "Signet"),
 L("community", "mempool.space, the block explorer", "https://mempool.space/", "mempool.space", "A block explorer where the blocks the chapter reads (heights, hashes, roots) can be looked up live.", "RealBlockRoot"),
 L("standard", "BIP 94: Testnet 4", "https://bips.dev/94/", "bips.dev", "The rules of testnet4 that answer the flooding of testnet3.", "Bip94Rules"),
 L("standard", "BIP 325: Signet", "https://bips.dev/325/", "bips.dev", "The specification of signet, whose blocks need a signature.", "SignetChallengeIsMultisig"),
 L("seminal", "Nakamoto: Bitcoin, a peer-to-peer electronic cash system", "https://bitcoin.org/bitcoin.pdf", "bitcoin.org", "The paper that introduces the chain of blocks and the merkle tree of transactions.", "HashChainedTimestamps"),
 L("video", "Brownworth: Blockchain 101 (video)", "https://www.youtube.com/embed/_160oMzblY8", "youtube.com", "The visual blockchain demo; the deck's suggested start.", "TamperingBreaksDescendants"),
 L("video", "Chainlink: what are Merkle trees (video)", "https://www.youtube.com/embed/na_omeubyYo", "youtube.com", "A short talk on how a merkle tree and a merkle proof work.", "TreeConstruction"),
 L("community", "Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/", "bitcoinops.org", "Where changes to Bitcoin Core and to the test chains are reported week by week, after the book went to print.", "Testnet4Replaces"),
 L("community", "Delving Bitcoin", "https://delvingbitcoin.org/", "delvingbitcoin.org", "A research forum where block validation and the test chains are discussed.", "NodeRejectsMutatedBlock"),
 L("community", "The bitcoin-dev mailing list", "https://groups.google.com/g/bitcoindev", "Google Groups", "The list on which the testnet4 and merkle-tree proposals were discussed.", "Bip94Rules")]
J("resources_v1_0_0.json", {"_version": "1.0.0", "checked": "2026-10-15", "links": links, "_note": "The eleven links are the links of the chapter 11 deck's last slide (Where to go from here), which states that every link was opened on 2026-10-15; this page author did not fetch them again. The YouTube links are the embed addresses the deck gives."})
J("stories_img_v1_0_0.json", {"_version": "1.0.0", "_note": "Story pictures for the chapter 11 page's Stories tab, from the deck's own placements (08-tooling/ch11-deck/deck_content_v1_0_0.py); licences in 03-materials/ch11/assets/ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md. Three pictures are stand-ins and say so, as the deck's slides 8, 21 and 23 do; the portrait of Ralph Merkle (slide 17) is the real thing.",
  "HeadlineInTheGenesisBlock": [{"file": "photo_satoshi_bust_budapest.png", "credit": "Bust of Satoshi Nakamoto, Budapest - Fekist, CC BY-SA 4.0, Wikimedia Commons (stand-in picture: a sculpture, not Satoshi's face)"}],
  "TheHashTreeOfRalphMerkle": [{"file": "photo_ralph_merkle.png", "credit": "Ralph Merkle - david.orban (Flickr), CC BY 2.0, Wikimedia Commons"}],
  "GriefingTheTestnet": [{"file": "photo_children_sandpit.png", "credit": "Children in a sandpit - Shixart1985, CC BY 2.0, Wikimedia Commons (stand-in picture: a sandpit, not the testnet)"}],
  "SignetBlocksNeedASignature": [{"file": "photo_signet_ring.png", "credit": "Signet ring of Ramesses II - akhenatenator, CC0 1.0, Flickr (stand-in picture: a signet ring, not the BIP)"}]})
print("bank %d, quiz %d, resources %d" % (len(bank), len(items), len(links)))
