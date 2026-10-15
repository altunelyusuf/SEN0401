#!/usr/bin/env python3
"""inputs_make v1_0_0 (SEN0401 chapter 10 page). Writes the page's authored inputs (objectives, quiz, question_bank, discussion, resources, stories_img, test_config, all v1_0_0) from the chapter's page data
(page_data_v*.json, the concepts exactly as the research states them) and from the deck's own links. Nothing here adds or rewords research prose: a question's right answer is the FIRST SENTENCE of the concept's
own explanation, its wrong answers are first sentences of other concepts, and its rationale names the concept the wrong answer belongs to. Run after sen0401_page_data_v2_14_0.py has written page_data.
Usage: inputs_make_v1_0_0.py PAGEVER   (e.g. 9_44_0)"""
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
CO = {"CO1": ["Describe the Bitcoin network as a flat peer-to-peer network of equal nodes, name the services nodes differ in, and read what a census of reachable nodes shows", "Understand"],
      "CO2": ["Follow how a node joins: DNS seeds, the version handshake and its services, address exchange, and the kinds of connection a node keeps", "Apply"],
      "CO3": ["Explain how a block travels (announcement, compact blocks, private relay) and how a node syncs headers first and blocks after, and judge why speed matters for rival blocks", "Analyze"],
      "CO4": ["Compare a light client that checks headers and Merkle paths, the Bloom filters of BIP 37 that leaked privacy, and the block filters of BIPs 157 and 158 that replaced them", "Analyze"],
      "CO5": ["Explain what the encrypted v2 transport and the Tor, I2P and CJDNS networks hide, and judge the eclipse and routing attacks on the network", "Evaluate"],
      "CO6": ["Explain how transactions are announced and filtered, why every mempool is local, and what a node does with a child that arrives before its parent", "Understand"]}
J("objectives_v1_0_0.json", dict({"_version": "1.0.0"}, **CO, _serves="These six outcomes are chapter 10's: the network and its nodes (CO1), joining it (CO2), moving blocks (CO3, with syncing), light clients (CO4), privacy and attacks (CO5) and the mempool with orphans (CO6). The chapter serves LO-6 of the course (reading and constructing transactions, scripts and signatures and explaining how a node decides whether one is valid). Each outcome is worded with one level of Bloom's taxonomy (Understand, Apply, Analyze or Evaluate here). Written by the page author from the chapter's own subjects; the research states no learning outcomes of its own."))
# ---- question bank: one item per concept ---------------------------------------------------------------------
OBJ = {"NetworkAndNodes": "CO1", "PeersAndDiscovery": "CO2", "BlockRelay": "CO3", "Syncing": "CO3", "LightClients": "CO4", "PrivacyAndTransport": "CO5", "MempoolAndOrphans": "CO6"}
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
    pick += ls[:2] if t in ("PeersAndDiscovery", "BlockRelay", "LightClients", "PrivacyAndTransport", "NetworkAndNodes") else ls[:1]
items = []
for b in pick:
    n = by[b["concept"]]; wrong = [o for i, o in enumerate(b["options"]) if i != b["answer"]]
    items.append({"q": b["q"], "options": b["options"], "answer": b["answer"], "level": "Remember", "objective": obj(n), "rationales": ["This sentence opens the explanation of another concept of the chapter." for _ in wrong]})
J("quiz_v1_0_0.json", {"_version": "1.0.0", "items": items})
J("discussion_v1_0_0.json", {"_version": "1.0.0", "items": [["Noticeable issues", "What stood out in this chapter, and what surprised you about how equal the nodes are and how a block reaches all of them?"],
  ["Interesting details", "Which of the chapter's cases (the Bloom filter that told on the wallet, the eclipse attack, the encryption that arrived years after the proposal) would you test first on a node of your own, and how?"],
  ["Unclarified issues", "Which points need further explanation? Select one critical issue from the chapter and explain it."]]})
# ---- resources -----------------------------------------------------------------------------------------------
L = lambda kind, title, url, source, why, concept: {"kind": kind, "title": title, "url": url, "source": source, "why": why, "concept": concept}
links = [
 L("documentation", "Optech topic: Compact block relay", "https://bitcoinops.org/en/topics/compact-block-relay/", "bitcoinops.org", "The newsletter topic page on compact blocks (BIP 152) and the changes since the book.", "CompactBlocks"),
 L("documentation", "Optech topic: v2 P2P transport", "https://bitcoinops.org/en/topics/v2-p2p-transport/", "bitcoinops.org", "The newsletter topic page on the encrypted transport of BIP 324.", "EncryptedTransport"),
 L("community", "Bitnodes, the live node census", "https://bitnodes.io/", "bitnodes.io", "The live census of reachable nodes that the chapter's node counts come from.", "NodeKinds"),
 L("standard", "BIP 152: Compact Block Relay", "https://bips.dev/152/", "bips.dev", "The protocol of compact blocks that the chapter's examples recompute.", "CompactBlocks"),
 L("standard", "BIP 324: Version 2 P2P Encrypted Transport Protocol", "https://bips.dev/324/", "bips.dev", "The specification of the encrypted v2 transport, the largest change since the book.", "EncryptedTransport"),
 L("seminal", "Heilman et al.: Eclipse Attacks on Bitcoin's Peer-to-Peer Network (USENIX Security 2015)", "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/heilman", "usenix.org", "The paper behind the chapter's eclipse attack story.", "NetworkAttacks"),
 L("video", "USENIX talk: eclipse attacks (video)", "https://www.youtube.com/embed/b-qGTj2Vvns", "youtube.com", "The authors present the eclipse attack; the deck's suggested start.", "NetworkAttacks"),
 L("video", "Neutrino light client (video)", "https://www.youtube.com/embed/7FWKc8lM4Ek", "youtube.com", "A talk on the light client that uses the block filters of BIPs 157 and 158.", "BlockFilters"),
 L("community", "Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/", "bitcoinops.org", "Where changes to the peer-to-peer network and to Bitcoin Core are reported week by week, after the book went to print.", "FlatNetwork"),
 L("community", "Delving Bitcoin", "https://delvingbitcoin.org/", "delvingbitcoin.org", "A research forum where relay, orphan handling and transport are discussed.", "OrphanPool"),
 L("community", "The bitcoin-dev mailing list", "https://groups.google.com/g/bitcoindev", "Google Groups", "The list on which the filter idea of 2016 was first posted.", "BlockFilters")]
J("resources_v1_0_0.json", {"_version": "1.0.0", "checked": "2026-10-15", "links": links, "_note": "The eleven links are the links of the chapter 10 deck's last slide (Where to go from here). Each was fetched over HTTPS on 2026-10-15 from this session and answered 200 (a ranged request answered 206); the YouTube links are the embed addresses the deck gives, which answered 200."})
J("stories_img_v1_0_0.json", {"_version": "1.0.0", "_note": "Story pictures for the chapter 10 page's Stories tab, from the stories module sen0401_ch10_stories_v1_1_0.py (the photo field of each story); licences in 03-materials/ch10/assets/ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md. Four pictures are stand-ins and say so, as the deck's slides 10, 12, 20 and 22 do; the Bloom filter diagram (slide 18) is the real thing.",
  "CompactBlockRelay": [{"file": "photo_optical_fibre.png", "credit": "Optical fibre - BigRiz, CC BY-SA 3.0, Wikimedia Commons (stand-in picture: a fibre, not the relay network)"}],
  "BloomFiltersLeak": [{"file": "photo_bloom_filter_diagram.png", "credit": "Bloom filter diagram - David Eppstein, public domain, Wikimedia Commons"}],
  "FilterIdeaPost": [{"file": "photo_solomon_golomb.png", "credit": "Solomon Golomb - National Science Foundation, public domain, Wikimedia Commons (stand-in picture: the inventor of the codes the filter uses, not the poster)"}],
  "EclipseAtUsenix": [{"file": "photo_total_solar_eclipse_2017.png", "credit": "Total solar eclipse 2017 - NASA / Aubrey Gemignani, public domain, Wikimedia Commons (stand-in picture: an eclipse of the sun, not the attack)"}],
  "EncryptionAtLast": [{"file": "photo_enigma_machine.png", "credit": "Enigma machine - Rama, CC BY-SA 2.0 FR, Wikimedia Commons (stand-in picture: a cipher machine, not the protocol)"}]})
print("bank %d, quiz %d, resources %d" % (len(bank), len(items), len(links)))
