#!/usr/bin/env python3
"""Chapter 10 (The Bitcoin Network) deck content, 26 slides, for the SEN0401 deck engine (sen0401_deck_engine_v1_0_0.py). Writes deck_plan_v1_1_0.json.

Every '>>>' row comes from examples_out_v1_0_0.json (executed by examples_v1_0_0.py under Python 3.14.6) and is re-run off the finished file by the deck check.
Every chart is built from those executed rows (parsed here and asserted), never typed. Rows that read the records of Bitcoin Core 31.1 on regtest are on slides that say Recorded;
what the research marks NOT EXECUTED carries that label; the pictures that show a topic and not the event are labelled stand-in. Speaker notes are short reader's prose
(2-4 sentences, at most 100 words, no presenter labels).
"""
import ast, datetime, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_1_0 as E
import sen0401_links_v1_0_0 as LK

E.init(10, HERE, assets=("photo_total_solar_eclipse_2017.png", "photo_optical_fibre.png", "photo_bloom_filter_diagram.png", "photo_solomon_golomb.png", "photo_enigma_machine.png"))
C, G, LABEL, STORY = E.C, E.G, E.LABEL, E.STORY
D = C.D
NPUB, NFIND, NCLAIM = len(D.PUBS), len(D.FINDINGS), len(D.TAX) + len(D.CLAIMS)
assert (NPUB, NFIND, NCLAIM) == (85, 24, 67), (NPUB, NFIND, NCLAIM)
OUT = lambda grp, i: ast.literal_eval(G[grp][i][1])
REC = "Recorded"
KEEP = {}          # key -> title, to find the slide numbers once the agenda has been inserted


def con(grp, x, y, w, h, label, fs=10, rows=None):
    return dict(E.code(grp, x, y, w, h, fs=fs, rows=rows), label=label)


def beats(x, y, w, h, items, fs=10.5):
    return {"t": "beats", "x": x, "y": y, "w": w, "h": h, "fs": fs, "items": items}


def foot(x, y, w, h, body, fs=11.5):
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body}


def chips(x, y, w, h, items, fs=10):
    return {"t": "chips", "x": x, "y": y, "w": w, "h": h, "fs": fs, "items": items}


def flow(x, y, w, h, steps, fs=11):
    return {"t": "flow", "x": x, "y": y, "w": w, "h": h, "fs": fs, "steps": steps}


def page(key, title, sub, items, notes, take, lede=None):
    KEEP[key] = title
    E.content(title, sub, items, notes, take=take, lede=lede)


def rows_of(grp, idx):
    return [G[grp][i] for i in idx]


def story(key, sid, photo, standin, beats_, grp, idx, label, notes, title=None):
    st = STORY[sid]
    rr = rows_of(grp, idx)
    E.story_slide(sid, photo, (0.5, 1.4, 2.9, 2.45), beats_, grp, rr, label, "", (3.6, 3.0, 5.9, 1.38), (3.6, 1.4, 5.9, 1.2), title=title)
    s = E.S[-1]
    s["notes"] = notes
    dt = datetime.date.fromisoformat(st["when"])
    s["sub"] = "The story of %d %s %d: who, where, when and what to read next" % (dt.day, dt.strftime("%B"), dt.year)
    for it in s["items"]:
        if it.get("t") == "factrow":
            it["x"], it["w"], it["y"] = 0.5, 9.0, 4.62
        if it.get("t") == "beats":
            it["fs"] = 10.5
    if standin:
        s["items"].append(foot(0.5, 4.22, 2.9, 0.36, standin, fs=9))
    KEEP[key] = s["title"]


# ---------------------------------------------------------------------------------------------- 1-3 opening
E.slide("title", "Chapter 10: The Bitcoin Network", "How nodes find each other, pass blocks and payments, and what moved since print. Bitcoin Core 31.1 results are Recorded.", [],
        "This deck explains the Bitcoin network: who the nodes are, how they find each other and shake hands, how blocks and transactions travel, and how light clients and encryption changed since the book went to print. Every example runs under Python 3.14.6 on the chapter's own library, and Bitcoin Core 31.1 was run on a test network, so its answers are Recorded and only read back here. The research package for chapter 10 holds the sources and the claims.")

page("questions", "The questions this chapter answers", "Its own competency questions, and the numbers behind the answers",
     [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 1.7, "fs": 13, "items": list(C.CQS)},
      {"t": "stat", "x": 0.5, "y": 3.3, "w": 9.0, "h": 1.6, "items": [
          {"n": str(NPUB), "label": "sources, opened and read on %s" % D.DATE},
          {"n": str(NCLAIM), "label": "claims, each recomputed by running code"},
          {"n": str(NFIND), "label": "findings, several of them corrections of the book"}]}],
     "The chapter asks two questions that this deck answers by computation: which of its statements can be checked, and what has changed since print. The three numbers are counted from the research package, which holds %d sources, %d findings and %d executed claims. Each slide that follows shows the computation behind one claim." % (NPUB, NFIND, NCLAIM),
     "")
E.S[-1].pop("take", None)

# ---------------------------------------------------------------------------------------------- part A
MARKET = "Like a village market with no manager: every stall only talks to its neighbours"
E.section("Who is on the network", MARKET,
          [{"label": "Nodes counted today"}, {"label": "The handshake"}],
          "This part asks who is on the network and how two nodes meet. The village market on the slide is the picture to keep: no manager, and every stall deals with its neighbours. The census of the real network is saved, and the handshake was run on a test node of Bitcoin Core 31.1.")
KEEP["secA"] = "Who is on the network"

page("census", "Who is on the network today", MARKET,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 1: 25,361 reachable nodes, of which 12,488 are onion services; only 8,664 are on the clearnet (row 2), not the book's 10,000",
                                   "Row 3: 99.67 percent report a /Satoshi: agent; plain Bitcoin Core is 83.57 percent, and 31.1.0 is the most common",
                                   "Row 4: the service bits show what a node offers: 22,402 keep the whole chain, 25,322 at least the last 288 blocks"], fs=10.5),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Reachable nodes by network, saved census", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": [k for k, v in sorted(OUT("Census", 0)[1], key=lambda kv: -kv[1])], "series": [{"name": "nodes", "data": [v for k, v in sorted(OUT("Census", 0)[1], key=lambda kv: -kv[1])]}]},
      con("Census", 0.5, 3.42, 9.0, 1.38, "executed on the saved Bitnodes snapshot of %s" % D.DATE, fs=10)],
     "A census of the reachable network shows a flat peer-to-peer system of equals, as the book says, but its numbers have moved. The saved snapshot lists 25,361 reachable nodes, and nearly half of them are onion services, so only 8,664 can be reached over the ordinary internet. More than 99 percent run code derived from Bitcoin Core, and the service bits tell a client which nodes keep the whole chain and which keep only the last 288 blocks.",
     "The network is flat and open, and nearly half of its nodes sit behind Tor")

HAND = "Like two people meeting: each says who they are, then they agree on a language"
page("handshake", "The handshake: version, verack, services", HAND,
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "version", "sub": "who I am: 70016"}, {"label": "wtxidrelay, sendaddrv2", "sub": "options"}, {"label": "verack", "sub": "agreed", "hot": True}, {"label": "sendcmpct, getheaders", "sub": "first requests"}], fs=10.5),
      con("Handshake", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest; the mainnet magic bytes are saved in the source", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 2: magic, command, length, checksum make 24 bytes for verack; mainnet magic f9beb4d9, test chain fabfb5da",
                                  "Rows 3 and 5: the node sent protocol version 70016 and /Satoshi:31.1.0/; the book's listing shows 70002",
                                  "Rows 4 and 6: version, options, verack, then requests; an archival node offers NETWORK, a pruned one only NETWORK_LIMITED"], fs=10)],
     "Two nodes meet by exchanging a version message, a few option messages and a verack, each framed with four magic bytes, a command, a length and a checksum. A script that knew only the wire format introduced itself to a test node of Bitcoin Core 31.1 and was answered as an equal with protocol version 70016, not the 70002 of the book. The services field says what a node offers: a pruned node does not set NETWORK but only NETWORK_LIMITED.",
     "Two nodes meet as equals: version, options, verack, then requests")

# ---------------------------------------------------------------------------------------------- part B
E.section("Peers, blocks and transactions", "Finding peers, choosing connections, and passing blocks and payments along.",
          [{"label": "Finding peers"}, {"label": "Compact blocks"}, {"label": "Headers first"}, {"label": "Relay and orphans"}],
          "This part follows a node from its first start to the data it relays. It finds peers through DNS seeds and gossip, keeps a few outbound connections of different kinds, and learns about blocks and transactions from them. A story about an attack on those connections and a story about compact blocks sit in the middle.")
KEEP["secB"] = "Peers, blocks and transactions"

DIR = "Like asking the phone directory for a few numbers, then your friends for more"
page("discovery", "Finding peers: DNS seeds and addr", DIR,
     [chips(0.5, 1.27, 9.0, 0.38, ["8 DNS seeds", "182 distinct addresses", "port 8333"], fs=9.5),
      con("Discovery", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest, with the DNS answers saved", fs=10),
      beats(0.5, 4.3, 9.0, 0.45, ["Rows 2 and 3: 8 DNS seeds answered with 20 to 29 addresses each, 182 in all, on port 8333; our probe did not connect",
                                  "Rows 4 to 6: a node sends up to 23 percent of its table as addr; with addrv2 it also names Tor, I2P and CJDNS peers"], fs=10),
      foot(0.5, 4.78, 9.0, 0.24, "NOT EXECUTED: connections to mainnet peers; row 3 shows the probe did not connect.", fs=10)],
     "A new node asks the DNS seeds named in its code for a few addresses, connects to some of them, and then asks those peers for more with addr messages. In the run the eight seeds answered with 20 to 29 addresses each, 182 different ones, but the test node could not connect to any mainnet peer, so that step was not run. The newer addrv2 message can carry the long addresses of Tor, I2P and CJDNS, which the old four-byte format could not.",
     "Peers are found by DNS seeds first, then by gossip")

page("conn", "Who connects to whom: connection types", "Eight full-relay links, two block-relay-only links, and at most 125 connections in all",
     [flow(0.5, 1.38, 9.0, 0.55, [{"label": "Outbound full relay", "sub": "8: blocks, payments, addr"}, {"label": "Block-relay-only", "sub": "2: blocks only"},
                                  {"label": "Feeler, addr-fetch", "sub": "short, to test or learn"}, {"label": "Inbound", "sub": "the rest of 125", "hot": True}], fs=10.5),
      con("ConnTypes", 0.5, 2.22, 9.0, 1.85, "Recorded: Core 31.1 regtest, three connection types", fs=9),
      beats(0.5, 4.3, 9.0, 0.68, ["Row 1: each entry is type, relays payments, relays addr, transport; the block-relay-only link relays neither and spoke v1",
                                  "Row 3: the code sets 8 outbound full-relay links, 2 block-relay-only links and 125 connections in all",
                                  "Rows 4 and 5: a peer that said it wants no payments was sent none of the 2 announced, a normal peer was sent both"], fs=10)],
     "A node does not treat all its peers alike. It keeps eight outbound links that carry everything and two that carry only blocks, so that an attacker who sees its payment traffic still cannot see those two. Short feeler and address-fetch links test and learn addresses, and up to 125 connections are allowed in all. On the test network a peer that said it wanted no payments received none.",
     "Two of a node's links carry blocks only, and hide from payment traffic")

story("eclipse", "EclipseAtUsenix", "photo_total_solar_eclipse_2017.png", "Stand-in picture: an eclipse, not the paper.",
      ["On 12 August 2015 Ethan Heilman and colleagues present the eclipse attack at USENIX Security in Washington, D.C.",
       "With enough addresses an attacker could own all of a node's connections; Core now keeps 2 block-relay-only links (row 1)",
       "NOT EXECUTED: the attack itself; the papers' claims are found in the saved copies (rows 2 and 3)"],
      "Eclipse", [0, 1, 2], "executed on saved sources; NOT EXECUTED: the attack",
      "On 12 August 2015 Ethan Heilman and his colleagues presented the eclipse attack at the USENIX Security Symposium in Washington, D.C. An adversary that controls enough addresses can take over all of a node's connections and then feed it a false view of the chain. Bitcoin Core now keeps anchor connections and two block-relay-only links. The attack and the routing attack of 2017 were not run here; the passages were found in the saved papers.")

CMP = "Like telling a friend the page numbers of a book they already own"
page("compact", "Compact blocks: send only what is missing", CMP,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: a block of 13 transactions was sent as 12 short ids of 6 bytes, and all 12 matched the receiver's own list",
                                   "Row 3: the coinbase is always sent in full; the receiver lacked 2 transactions, asked for them and got exactly those",
                                   "Row 4: 332 bytes instead of 3,062, about a ninth of the block"], fs=10.5),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Recorded: bytes to send one block of 13 transactions", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": ["compact block", "full block"], "series": [{"name": "bytes", "data": [OUT("Compact", 3)[0], OUT("Compact", 3)[1]]}]},
      con("Compact", 0.5, 3.42, 9.0, 1.38, "Recorded: Core 31.1 regtest", fs=10)],
     "A node already holds most transactions of a new block in its mempool, so the block can travel as a header, a six-byte short id for each transaction, and the few transactions the receiver cannot have, always including the coinbase. In the run a block of 13 transactions took 332 bytes instead of 3,062, and the receiver asked for the two transactions it lacked. A node sends compact blocks unasked to at most three high-bandwidth peers.",
     "A compact block is a header and short ids: a ninth of the bytes")

story("cbr", "CompactBlockRelay", "photo_optical_fibre.png", "Stand-in picture: optical fibre, not the BIP.",
      ["On 27 April 2016 BIP 152 is assigned to Matt Corallo; Bitcoin Core 0.13.0 ships Suhas Daftuar's code",
       "The book says 2015 (row 1); Core's own list says 0.13.0 (row 2), so the book is a year early",
       "Relay networks go further: a lost piece of 4 is rebuilt from one parity piece (row 4); FIBRE is NOT EXECUTED"],
      "CompactStory", [0, 1, 2, 3], "executed on saved sources and a demo; NOT EXECUTED: FIBRE",
      "On 27 April 2016 the number 152 was assigned to the proposal for compact block relay by Matt Corallo, and Bitcoin Core 0.13.0 lists the code of Suhas Daftuar. The book dates the feature to 2015, which is a year too early. Corallo had earlier built a relay network for miners, and its successor FIBRE adds forward error correction, so that a lost packet can be rebuilt. The demonstration rebuilds one lost piece of four; FIBRE itself was not run.")

page("headers", "Syncing: headers first, then blocks", "Like reading the contents page before asking for the chapters",
     [chips(0.5, 1.27, 9.0, 0.38, ["2,000 headers per message", "80 bytes each", "window of 1,024 blocks"], fs=9.5),
      con("Headers", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest, a second node syncing from the first", fs=9),
      beats(0.5, 4.3, 9.0, 0.68, ["Rows 2 and 3: 2,000 headers came first, then 101, so 2,101 blocks; each header is 80 bytes and links to the one before it",
                                  "Row 4: without sendheaders a new block is announced by inv, with it by the header itself",
                                  "Row 5: blocks are fetched inside a window of 1,024, at most 16 in flight per peer; the second node ended on the same chain"], fs=10)],
     "A node that is catching up first asks for headers, at most 2,000 in one reply, and checks that each links to the one before. Only then does it fetch blocks, inside a window of 1,024 and at most 16 in flight from one peer. In the run a second node synced 2,105 blocks from the first and ended on the same chain. A peer that sent sendheaders is told of new blocks by their headers instead of an inv message.",
     "Headers come first, then blocks, so a liar is caught cheaply")

MEMPOOL = "Like each shop keeping its own waiting list, while the town ledger is shared"
page("relay", "Relaying payments, and orphans", MEMPOOL,
     [con("Relay", 0.5, 1.65, 9.0, 2.1, "Recorded: Core 31.1 regtest", fs=9),
      beats(0.5, 4.0, 9.0, 0.62, ["Rows 2 and 3: wtxid announcements (type 5); a peer with feefilter 5 sat/vB heard of 20.0 sat/vB, not 2.0",
                                  "Row 4: one node held 6 payments, its blocks-only neighbour 0, yet both held the same 107 outputs after a block",
                                  "Row 5: the orphan child is refused (False), the node asks for its parent (0x40000001), then both are in"], fs=10),
      foot(0.5, 4.7, 9.0, 0.3, "NOT EXECUTED: Erlay; row 6 shows that BIP 330 is off by default, so announcements are still flooded.", fs=10)],
     "Transactions are announced by their wtxid, and a peer's feefilter keeps cheaper ones from being announced to it. The mempool is local to each node whereas the set of unspent outputs is shared, and the run shows a node with six waiting payments next to a neighbour with none that nevertheless holds the same 107 outputs. A child that arrives before its parent waits in the orphan pool, and the node asks its peers for the parent.",
     "The mempool is local; the set of unspent outputs is shared")

# ---------------------------------------------------------------------------------------------- part C
E.section("Light clients, privacy, transport", "How a phone checks a payment without the chain, what it leaked, and how the wire became private.",
          [{"label": "Merkle proof"}, {"label": "Bloom and block filters"}, {"label": "Encrypted transport"}, {"label": "Onion, I2P and CJDNS"}],
          "This part is about the nodes that do not keep the chain. A light client checks a payment with headers and a short proof, asks a full node for what concerns it, and has to hide what it asks. Two stories show how the first answer, the Bloom filter, leaked and how the second turned the question around, and a third shows how the wire itself was encrypted.")
KEEP["secC"] = "Light clients, privacy, transport"

PHONE = "Like proving a name is in a phone book by showing only the headings on its path"
page("spv", "A light client verifies with headers", PHONE,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: at height 971,499 the headers are 77.7 MB and the chain 775,272 MB: 9,975 times smaller, as the book says",
                                   "Row 3: a path of 3 hashes proves one of 5 payments in a block: 215 bytes against a block of 4,448",
                                   "Row 4: an attacker with 10 percent of the power has a 0.0002428 chance after 6 blocks, one with 30 percent 0.1321"], fs=10.5),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Recorded: bytes to prove one payment", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": ["Merkle proof", "whole block"], "series": [{"name": "bytes", "data": [OUT("Spv", 2)[3], OUT("Spv", 2)[4]]}]},
      con("Spv", 0.5, 3.42, 9.0, 1.38, "Recorded: Core 31.1 regtest; the sizes come from saved data", fs=10)],
     "A light client keeps only the 80-byte block headers, which are about ten thousand times smaller than the chain. To check one payment it asks a full node for the Merkle path from that payment to the root in the header, and the test run needed three hashes for a block of five payments, 215 bytes against a block of 4,448. Nakamoto's formula gives the odds that an attacker catches up after six blocks: 0.0002428 for a tenth of the power.",
     "Headers and a short Merkle path are enough to check one payment")

BLOOM = "Like a guest list that admits a few strangers by mistake but never a listed friend"
page("bloom", "Bloom filters: a fuzzy guest list", BLOOM,
     [chips(0.5, 1.27, 9.0, 0.38, ["6 bits set", "5.3 percent false hits", "BLOOM bit off by default"], fs=9.5),
      con("Bloom", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; the BIP 37 vector is published", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Rows 2 and 3: a toy filter with 6 bits set missed nothing and gave 0.053 false hits; BIP 37's published vector matches ours",
                                  "Row 4: one wallet payment came back as a 215-byte merkleblock instead of a block of 4,448",
                                  "Row 5: a default node sets no BLOOM bit and hung up on a peer that sent filterload"], fs=10)],
     "A Bloom filter is a short row of bits that answers either definitely not or probably yes, so a light client can send a full node a filter of its addresses and receive only matching payments. The toy filter of the chapter missed nothing and gave a few false hits, and the encoding of BIP 37 matches its published vector. The test node sent one matching payment as a 215-byte merkleblock, but a default node no longer offers the service.",
     "A Bloom filter says definitely not or probably yes, and it leaked")

story("bloomstory", "BloomFiltersLeak", "photo_bloom_filter_diagram.png", None,
      ["On 24 October 2012 BIP 37 is assigned to Mike Hearn and Matt Corallo: a phone sends a Bloom filter of its addresses",
       "In 2014 Arthur Gervais and colleagues at ETH Zurich show that the filters leak the user's addresses (row 1)",
       "Core 0.19.0.1 turned the service off: a default node hangs up on it (row 2), but 4,308 of 25,361 nodes still offer it (row 3)"],
      "BloomStory", [0, 1, 2], "executed on saved sources and the Core 31.1 record (Recorded)",
      "On 24 October 2012 BIP 37 was assigned to Mike Hearn and Matt Corallo: a light client would send a Bloom filter of its addresses to a full node. In 2014 Arthur Gervais and his colleagues at ETH Zurich showed that the reliance on Bloom filters leaks considerable information about the addresses of the user. Bitcoin Core 0.19.0.1 switched the service off by default, and the test node hung up on a peer that sent filterload.")

GOLOMB = "Like a library posting each day's index, so you look yourself up without asking"
page("filters", "Block filters turn the question around", GOLOMB,
     [chips(0.5, 1.27, 9.0, 0.38, ["M = 784,931 and P = 19", "21 bits per element", "OP_RETURN left out"], fs=9.5),
      con("Filters", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest; the BIP 158 vectors are published", fs=9.5),
      beats(0.5, 4.3, 9.0, 0.68, ["Rows 2 and 3: the gaps 379, 97, 177, 196, 51 fit in 8 bits, not 10; Rice coding stores the five numbers in 44 bits, not 50",
                                  "Rows 4 and 5: all 10 published vectors pass; our filter equals the node's, at 21.15 bits per element, not 64",
                                  "Row 6: the 2 OP_RETURN outputs of the block are not in the filter"], fs=10)],
     "A block filter reverses the Bloom filter: the full node builds one small filter for every block, and the light client downloads it and tests its own scripts locally, so it never reveals them. The filter stores the sorted differences with Golomb-Rice coding, about 21 bits for each element, not the 64 bits of the book. The chapter's own code reproduced all ten published vectors of BIP 158, and the filter and header of the test node.",
     "A block filter is tested on the client, so nothing is revealed")

story("filterstory", "FilterIdeaPost", "photo_solomon_golomb.png", "Stand-in picture: Solomon Golomb, namesake of the coding.",
      ["On 9 May 2016 a developer writing as bfd posts the idea to the bitcoin-dev list: one small filter for each block (row 1)",
       "Olaoluwa Osuntokun and Alex Akselrod write it as BIP 157 and 158; Lightning Labs builds Neutrino on it",
       "A Core 31.1 node served 3 filters on request, one without the option hung up (row 2); 7,905 nodes offer them (row 3)"],
      "FilterStory", [0, 1, 2], "executed on saved sources and the Core 31.1 record (Recorded)",
      "On 9 May 2016 a developer writing as bfd posted to the bitcoin-dev list the idea of committed Bloom filters, one small filter for each block, so that the client tests its own addresses and reveals nothing. Olaoluwa Osuntokun and Alex Akselrod wrote it as BIP 157 and 158, and Lightning Labs built the light client Neutrino on it. A node of Bitcoin Core 31.1 served three filters on request, and one started without the option hung up.")

V2 = "Like moving from a postcard that anyone can read to a sealed envelope"
page("v2", "Transport v2: from postcard to envelope", V2,
     [chips(0.5, 1.27, 9.0, 0.38, ["v1 shows its magic bytes", "v2 shows nothing", "85.8 percent offer v2"], fs=9.5),
      con("Transport", 0.5, 2.12, 9.0, 1.85, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 4.3, 9.0, 0.68, ["Rows 2 and 3: the v1 stream shows the magic bytes and the word version; v2 shows neither, at 7.953 bits of 8 per byte",
                                  "Rows 4 and 5: both ends derive the same 64-character session id; v2 is the default since Core 27.0, offered by 85.8 percent",
                                  "Row 6: BIP 324 calls v1 unencrypted and unauthenticated, and names the man in the middle that v2 does not stop"], fs=10)],
     "In the old transport every message began with the same four magic bytes and the command name, so anyone on the path could read the traffic. The version 2 transport of BIP 324 hides all of that: in the run its stream showed neither the magic bytes nor the word version and looked like random bytes, and both ends derived the same session id. It encrypts but does not authenticate, so an active man in the middle remains possible.",
     "The book says the wire is plain, but v2 has been the default since 27.0")

story("encstory", "EncryptionAtLast", "photo_enigma_machine.png", "Stand-in picture: an Enigma machine, not the protocol.",
      ["Jonas Schnelli proposes encrypted connections in BIP 151 in 2016; it is closed after mixed comments (row 2)",
       "On 8 March 2019 BIP 324 is assigned to Mehta, Ruffing, Schnelli and Wuille; Core 26.0 offers it and 27.0 makes it the default (row 1)",
       "On the 31.1 test node a v2 stream showed no magic bytes (row 3); 21,768 of 25,361 census nodes offer it"],
      "EncStory", [0, 1, 2], "executed on saved sources and the Core 31.1 record (Recorded)",
      "Jonas Schnelli proposed encrypting peer connections in BIP 151 in 2016, and the proposal was closed after mixed comments. On 8 March 2019 BIP 324 was assigned to Dhruv Mehta, Tim Ruffing, Jonas Schnelli and Pieter Wuille, and it replaces BIP 151. Bitcoin Core 26.0 added it as an option and 27.0 made it the default, so that 21,768 of the 25,361 nodes of the census now offer it.",
      title="From a closed proposal to the default")

TOR = "Like passing a note through several friends so none knows both sender and reader"
page("anon", "Hiding who you are: Tor, I2P, CJDNS", TOR,
     [con("Anon", 0.5, 1.65, 9.0, 2.05, "Recorded: Core 31.1 regtest, and counts from the saved census", fs=8.4),
      beats(0.5, 3.98, 9.0, 0.66, ["Rows 1 and 2: five networks are known; with a proxy setting onion was marked reachable (nothing ran)",
                                  "Row 3: the census holds 12,488 onion nodes, 4,208 I2P nodes and 1 on CJDNS; the book knows only Tor",
                                  "Rows 4 and 5: I2P came with Core 22.0 and CJDNS with 23.0; Core creates a Tor onion service by default"], fs=10.5),
      foot(0.5, 4.68, 9.0, 0.34, "NOT EXECUTED: Tor, I2P and CJDNS routers; the proxy setting only marks a network reachable, and no traffic ran through it.", fs=10.5)],
     "Bitcoin Core can run over five networks, and the book knows only Tor. Tor version 3 and addrv2 came with release 0.21.0, I2P with 22.0 and CJDNS with 23.0, and the saved census shows 12,488 onion nodes, 4,208 I2P nodes and a single CJDNS node. The test node marked onion as reachable when given a proxy setting, but no Tor, I2P or CJDNS router was run, so no traffic was sent through them.",
     "Onion nodes are about half of the network, I2P a sixth, CJDNS one node")

page("summary", "The chapter in five lines", "One line per part, each one provable from its slides",
     [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5, "items": [
         "The network is flat and open: 25,361 reachable nodes, 99.67 percent on Bitcoin Core code, nearly half of them behind Tor",
         "Peers meet through DNS seeds and addr, shake hands on version 70016, and keep 8 full-relay and 2 block-relay-only links",
         "Blocks travel as headers and compact blocks, payments as wtxid announcements, and the mempool stays local",
         "A light client needs headers and a Merkle path; Bloom filters leaked and are off, block filters turn the question around",
         "Since print the wire is encrypted by default, I2P and CJDNS join Tor, and the orphan and mempool rules have moved"]}],
     "These five lines are the deck in miniature. Each can be traced to a part of the route on slide 2 and to computations that ran on its slides. A line that feels unproven should send the reader back to that part's consoles.",
     "If a line feels unproven, its part's consoles carry the receipt")

page("resources", "Where to go from here", "Opened on %s; every entry is a live link in this file" % D.DATE,
     [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
         {"head": "Read", "rows": [
             ["Optech topic, compact block relay", "https://bitcoinops.org/en/topics/compact-block-relay/"],
             ["Optech topic, v2 P2P transport", "https://bitcoinops.org/en/topics/v2-p2p-transport/"],
             ["Bitnodes, the live node census", "https://bitnodes.io/"]]},
         {"head": "Standards and papers", "rows": [
             ["BIP 152, compact block relay", "https://bips.dev/152/"],
             ["BIP 324, v2 encrypted transport", "https://bips.dev/324/"],
             ["Heilman et al., eclipse attacks", "https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/heilman"]]},
         {"head": "Watch", "rows": [
             ["USENIX talk: eclipse attacks (video)", "https://www.youtube.com/embed/b-qGTj2Vvns"],
             ["Neutrino light client (video)", "https://www.youtube.com/embed/7FWKc8lM4Ek"]]},
         {"head": "Community", "rows": [
             ["Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/"],
             ["Delving Bitcoin, research forum", "https://delvingbitcoin.org/"],
             ["The bitcoin-dev group", "https://groups.google.com/g/bitcoindev"]]}]}],
     "Everything here is free to read or watch, and every link was opened on %s. A good start is the USENIX talk on eclipse attacks, then the Optech topic on compact block relay next to the chapter. The research package for chapter 10 lists all %d sources with the passages used." % (D.DATE, NPUB),
     "Watch the eclipse talk, then read the Optech topic beside the chapter")

E.slide("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "Who is on the network, and how two nodes meet",
            "How blocks and payments travel, and what a node keeps",
            "How a light client checks a payment without the chain",
            "What stays hidden now: v2 transport, filters, Tor, I2P"]}],
        "Four claims, each carried by computations that ran on slides of this deck. A reader who can say them and point to the slide that proves them has the chapter. The research package for chapter 10 holds the sources and the test records behind them.", bg="dark")

# ---------------------------------------------------------------------------------------------- agenda and plan meta
LK.patch(E.S, 10)   # v1.1.0: every resources row names its resource, goes straight to it and says what the reader finds there
E.agenda(["The chapter's questions", "Who is on the network", "Peers, blocks and transactions", "Light clients, privacy and transport"],
         "The route has three parts after the questions: who is on the network and how two nodes meet, how peers, blocks and payments are found and relayed, and finally light clients, privacy and the encrypted wire. Each part carries a true story or a correction of the book that a reader can check on the slide. The numbers in the list let a reader jump straight to a part.",
         "Three parts, five true stories, and a list of what was not run")
E.finish("Chapter 10: The Bitcoin Network", "1.1.0", "2026-10-15, first deck from the committed research package (commit a7b47b2), to the CME look and feel; notes are short reader's prose; v1.1.0: every READ card and resources link names its resource and goes straight to it (link_register_v1_0_0.json)")

planp = os.path.join(HERE, "deck_plan_v1_1_0.json")
plan = json.load(open(planp))
num = {k: [i + 1 for i, s in enumerate(plan["slides"]) if s["title"] == t][0] for k, t in KEEP.items()}
plan["meta"]["notes"] = "short reader's prose: 2-4 sentences, at most 100 words"
plan["meta"]["honesty"] = {
    "title": ["Bitcoin Core 31.1", REC],
    "recorded": [1, num["handshake"], num["discovery"], num["conn"], num["compact"], num["headers"], num["relay"], num["spv"], num["bloom"], num["bloomstory"], num["filters"], num["filterstory"], num["v2"], num["encstory"], num["anon"]],
    "notExecuted": [num["discovery"], num["eclipse"], num["cbr"], num["relay"], num["anon"]],
    "standin": {str(num["eclipse"]): ["Stand-in picture"], str(num["cbr"]): ["Stand-in picture"], str(num["filterstory"]): ["Stand-in picture"], str(num["encstory"]): ["Stand-in picture"]},
    "vectors": [num["census"], num["handshake"], num["discovery"], num["bloom"], num["filters"], num["eclipse"], num["cbr"], num["bloomstory"], num["filterstory"], num["encstory"]],
}
plan["meta"]["analogies"] = [
    {"concept": "flat peer-to-peer network", "analogy": MARKET, "slide": num["secA"]},
    {"concept": "handshake", "analogy": HAND, "slide": num["handshake"]},
    {"concept": "DNS seed", "analogy": DIR, "slide": num["discovery"]},
    {"concept": "compact block", "analogy": CMP, "slide": num["compact"]},
    {"concept": "mempool", "analogy": MEMPOOL, "slide": num["relay"]},
    {"concept": "Merkle proof", "analogy": PHONE, "slide": num["spv"]},
    {"concept": "Bloom filter", "analogy": BLOOM, "slide": num["bloom"]},
    {"concept": "block filter", "analogy": GOLOMB, "slide": num["filters"]},
    {"concept": "encrypted transport", "analogy": V2, "slide": num["v2"]},
    {"concept": "Tor", "analogy": TOR, "slide": num["anon"]},
]
json.dump(plan, open(planp, "w"), indent=1)
print("meta: honesty and %d analogies written; slide numbers %s" % (len(plan["meta"]["analogies"]), num))
