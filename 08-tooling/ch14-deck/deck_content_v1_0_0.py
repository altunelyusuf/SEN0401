#!/usr/bin/env python3
"""Chapter 14 (Second-Layer Applications) deck content, 26 slides, for the SEN0401 deck engine (sen0401_deck_engine_v1_0_0.py). Writes deck_plan_v1_0_0.json.

Every '>>>' row comes from examples_out_v1_0_0.json (executed by examples_v1_0_0.py under Python 3.14.6) and is re-run off the finished file by the deck check.
Every chart is built from those executed rows (parsed here and asserted), never typed. Rows that read the records of Bitcoin Core 31.1 and lnd 0.21.3-beta on regtest are on slides that say Recorded;
what the research marks NOT EXECUTED carries that label; the pictures that show a topic and not the event are labelled stand-in. Speaker notes are short reader's prose
(2-4 sentences, at most 100 words, no presenter labels).
"""
import ast, datetime, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_0_0 as E

E.init(14, HERE, assets=("papa_johns_jacksonville.png", "micropayment_channel_construction.png", "lightning_cut_nodes.png", "jack_dorsey_2009.png"))
C, G, LABEL, STORY = E.C, E.G, E.LABEL, E.STORY
D = C.D
NPUB, NFIND, NCLAIM = len(D.PUBS), len(D.FINDINGS), len(D.TAX) + len(D.CLAIMS)
assert (NPUB, NFIND, NCLAIM) == (83, 27, 55), (NPUB, NFIND, NCLAIM)
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
E.slide("title", "Chapter 14: Second-Layer Apps", "What the chain guarantees, how a payment channel is built and how Lightning routes payments. Bitcoin Core 31.1 and lnd 0.21.3-beta results are Recorded.", [],
        "This deck explains what is built on top of Bitcoin: the guarantees of the chain, colored coins, payment channels and the Lightning Network. Every example runs under Python 3.14.6 on the chapter's own library, and Bitcoin Core 31.1 and five lnd 0.21.3-beta nodes were run on private test chains, so their answers are Recorded and only read back here. The research package for chapter 14 holds the sources, the claims and the list of what was not run.")

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
E.section("What the chain guarantees", "No double spend, proofs, pledges and colored coins.",
          [{"label": "Pizza for bitcoins"}, {"label": "No double spend"}, {"label": "Proof and pledge"}, {"label": "Single-use seals"}],
          "This part asks what the base chain gives to anything built on it. A spent output stays spent, a hash in a transaction proves that a document existed, pledges can be pooled into one payment, and a spent output can serve as a seal for colored coins. The story is the first purchase made with bitcoin.")
KEEP["secA"] = "What the chain guarantees"

story("pizza", "PizzaForBitcoins", "papa_johns_jacksonville.png", "Stand-in picture: a Papa Johns shop in Florida, not the 2010 order.",
      ["On 18 May 2010 by the forum clock (17 May on the Wiki) Laszlo Hanyecz offers 10,000 bitcoins for pizzas",
       "On 22 May 2010 Jeremy Sturdivant, 19, orders two pizzas to Jacksonville and receives the coins",
       "Rows 2 and 3: today 32,518 channels, 3,753.7 BTC, fee 100 ppm. NOT EXECUTED: gossip on mainnet"],
      "PizzaStory", [0, 1, 2], "executed on the mempool.space statistics, saved on 2026-10-15",
      "On 22 May 2010 a 19-year-old in California ordered two pizzas for Laszlo Hanyecz in Jacksonville and received 10,000 bitcoins, the first notable retail purchase with bitcoin. That payment settled on the chain, as every payment then did. The Lightning Network now holds 32,518 channels with 3,753.7 bitcoin on a public statistics page, but only the page was read here and no gossip was observed.",
      title="Two pizzas for 10,000 bitcoins")

CHEQUE = "Like a cheque cashed once: the bank refuses a second copy"
page("double", "No double spend, no expiry", CHEQUE,
     [con("Double", 0.5, 1.7, 9.0, 1.8, "Recorded: Core 31.1 regtest; the release notes are saved", fs=10),
      beats(0.5, 3.85, 9.0, 0.7, ["Row 2: a second spend with a lower fee is refused as an insufficient fee; the first spend was accepted (True)",
                                  "Row 3: with a higher fee it replaces the first; after a block the loser is refused",
                                  "Rows 4 and 5: more out than in is refused; a payment kept 150 blocks still passes; full RBF is default"], fs=10)],
     "Bitcoin's most basic guarantee is that an output is spent once. On the test chain a second spend with a lower fee was refused, one with a higher fee replaced the first in the memory pool, and once a block had confirmed one of them the other was refused. A payment that spent more than it held was refused, and a payment signed at height 301 was still accepted at 451. Since release 28.0 full replace-by-fee is the default.",
     "A spent output stays spent, and a signed payment never expires")

PLEDGE = "Like a street collection that pays out only when the whole target is raised"
page("pledge", "Proof of existence and a crowdfund", PLEDGE,
     [con("Pledge", 0.5, 1.7, 9.0, 1.5, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 3.6, 9.0, 0.7, ["Row 2: a 32-byte SHA-256 sits in an OP_RETURN output of value zero, so the document existed by that block",
                                 "Row 3: two pledges minus the fee reach the goal; one pledge alone is refused (bad-txns-in-belowout)",
                                 "Row 4: both pledges pass (True); a changed output fails; signing everything first fails (False)"], fs=10)],
     "A document can be timestamped by writing only its hash: a 32-byte SHA-256 in an output of value zero was confirmed in a block, so the document existed no later than that block. A crowdfunding transaction in the style of Lighthouse joins two pledges, each signed only for its own input and the one fixed output. With one pledge the node refused it for lack of value, with both it accepted it, and a changed output broke the signatures.",
     "A hash proves existence; pledges join only when the goal is met")

TICKET = "Like a ticket torn once: the contract printed on it stays in your pocket"
page("seals", "Single-use seals and client validation", TICKET,
     [con("Seals", 0.5, 1.7, 9.0, 1.8, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 3.85, 9.0, 0.62, ["Row 2: three seals are three different outpoints; each earlier output was spent by the next transaction",
                                   "Rows 3 and 4: a key tweaked by a contract hash is a new address (False); only the tweaked key spends it",
                                   "Row 5: the history validates, a forged contract does not, and no token shows on the chain (False)"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: Taproot Assets and RGB; only the seal, the tweak and the validation were built by hand.", fs=10)],
     "A single-use seal is something that can be closed once, and an unspent output is exactly that. In the test a chain of three seals was three different outpoints, each spent by the next transaction. A public key tweaked by the hash of a contract made a new address, only the tweaked key could spend from it, and the contract itself never appeared on the chain. A forged contract failed the check, so the validation stays between the parties.",
     "A spent output can seal a contract that never touches the chain")

# ---------------------------------------------------------------------------------------------- part B
E.section("Payment channels", "A shared output, signed refunds and a promise that punishes cheating.",
          [{"label": "First channels"}, {"label": "Emma and Fabian"}, {"label": "Falling lock times"}, {"label": "Penalty"}, {"label": "HTLC"}],
          "This part builds a payment channel. Two parties fund a shared output and exchange signed transactions, refunds carry falling lock times so the newest wins, the commitment of one side can be punished if an old one is published, and a hash-locked contract lets a payment pass through a third party. The story is where channels were first proposed.")
KEEP["secB"] = "Payment channels"

story("spillman", "SpillmanChannels", "micropayment_channel_construction.png", "Stand-in picture: a 2018 diagram of a channel, not the 2013 thread.",
      ["On 17 April 2013 Mike Hearn posts Anti DoS for tx replacement; on 20 April Jeremy Spillman replies (row 2)",
       "The Wiki traces the idea to an open transaction replaced until its lock time (row 3)",
       "The one-way channel needs a refund signed before the funding, as in the Emma and Fabian test"],
      "SpillmanStory", [0, 1, 2], "executed on the Bitcoin Wiki page on channels, saved on 2026-10-15",
      "The Bitcoin Wiki traces payment channels to the first Bitcoin code, where an unrecorded open transaction could keep being replaced until its lock time. On 17 April 2013 Mike Hearn posted Anti DoS for tx replacement to the bitcoin-development list, and on 20 April Jeremy Spillman replied with the one-way design that the book calls Spillman-style. The refund had to be signed before the funding was sent.",
      title="The first payment channels")

TAB = "Like a tab at a cafe: you settle the running total at the end, not each cup"
page("emma", "Emma and Fabian: a channel in numbers", TAB,
     [con("Emma", 0.5, 1.7, 9.0, 1.5, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 3.6, 9.0, 0.7, ["Row 2: at 1,000 satoshis a second an hour uses all 3,600,000; after 600 seconds Emma keeps 3,000,000 (True)",
                                 "Row 3: Emma alone cannot spend the funding output (script verify failed); both can; 165 virtual bytes",
                                 "Row 4: the funding script starts 52 (2) and ends 52ae (2, CHECKMULTISIG), 71 bytes long"], fs=10)],
     "In the book Emma pays Fabian one thousand satoshis for each second of video, from a channel funded with 3,600,000 satoshis, enough for one hour. The funding output needs two keys: on the test chain Emma's signature alone was refused and both signatures were accepted. The 71-byte script starts with 2 and ends with 2 and CHECKMULTISIG, and the recorded settlement paid Fabian for 6 seconds.",
     "A channel is a two-key output and a running total of signed settlements")

DATED = "Like cheques dated one day earlier each time: the newest is the first to cash"
page("ladder", "Refunds with falling lock times", DATED,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: six refunds carry lock heights 488 down to 483; all six are non-final at the start",
                                   "Row 3: refund 6, the lowest lock, is refused until its block, then accepted (non-final, True)",
                                   "Row 4: once refund 6 is mined the funding output is spent; the rest end as missing-inputs"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Lock height of each refund", "dataLabels": True, "dlFmt": "0", "dlFs": 9,
       "labels": ["refund %d" % (i + 1) for i in range(6)], "series": [{"name": "height", "data": OUT("Ladder", 1)[0]}]},
      con("Ladder", 0.5, 3.42, 9.0, 1.38, "Recorded: Core 31.1 regtest", fs=10)],
     "To let a channel be replaced, each new refund carries an earlier lock time than the one before, so the newest refund can be mined first. On the test chain six refunds carried the lock heights 488 down to 483 and all six were refused at the start. The refund with the lowest lock was accepted at its height, and once it spent the funding output the older refunds failed with missing inputs.",
     "The newest refund has the earliest lock and wins the race")

PENALTY = "Like a contract that hands the whole safe to the other party if you cheat"
page("commit", "A commitment that punishes cheating", PENALTY,
     [con("Commit", 0.5, 1.7, 9.0, 2.1, "Recorded: lnd 0.21.3-beta and Core 31.1 regtest", fs=10),
      beats(0.5, 4.15, 9.0, 0.7, ["Rows 2 and 3: pay-to-self waits 1000 blocks (CSV): refused at 999 confirmations, accepted at 1000",
                                  "Rows 4 and 5: the revocation key needs both halves of its secret; with both, the penalty spend confirms",
                                  "Row 6: 1000 blocks is the book's teaching value; lnd 0.21.3-beta used 2016 (14 days)"], fs=10)],
     "Each side holds a commitment whose own output waits a number of blocks, while the other side can take it at once with a revocation key. On the test chain a spend after 999 confirmations was refused and after 1000 was accepted. The revocation key needed both halves of its secret, and with both the penalty spend confirmed. The book's 1000 blocks is a teaching value, since lnd 0.21.3-beta set 2016.",
     "A published old state can be taken whole by the other side")

LOCKER = "Like a locker: the code opens it today, and the owner reclaims it tomorrow"
page("htlc", "HTLC: a secret opens it, time reclaims it", LOCKER,
     [con("Htlc", 0.5, 1.7, 9.0, 1.5, "Recorded: Core 31.1 regtest", fs=10),
      beats(0.5, 3.6, 9.0, 0.7, ["Row 2: the secret opens the output (True); a wrong secret fails OP_EQUALVERIFY; the payer's key alone fails",
                                 "Row 3: before the timeout the refund is non-final, one block early too; at the locked height it passes",
                                 "Row 4: the refund came 19 blocks after funding; HASH160 is RIPEMD160 of SHA256; the secret has 32 bytes"], fs=10),
      foot(0.5, 4.4, 9.0, 0.28, "NOT EXECUTED: an HTLC left to time out on the chain in lnd; the timeout ran in the hand-built contract only.", fs=10)],
     "A hash-time-locked contract has two ways out. Whoever knows the secret behind the hash can claim the output, and a wrong secret or the payer's key alone failed. After the lock height the payer can take it back, and the refund was refused one block early. The book writes HASH160 for the hash, which is the RIPEMD160 of the SHA256, while the Lightning payment hash itself is a plain 32-byte SHA256.",
     "A secret opens it before the deadline, the refund after it")

# ---------------------------------------------------------------------------------------------- part C
E.section("The Lightning Network", "Routing, fees, invoices, the wire formats and the chain side.",
          [{"label": "A paper, a torch"}, {"label": "Five-node payment"}, {"label": "Hold invoice"}, {"label": "Wire formats"}, {"label": "Breach and fees"}],
          "This part runs the network. Five lnd nodes pass one payment of one bitcoin along a line with fees and falling timelocks, a hold invoice keeps it in flight, the handshake and the onion packet are checked against the published vectors, and the channel's own transactions show how cheating is punished and fees are bumped. The stories are the paper that proposed the network and the torch that passed along it.")
KEEP["secC"] = "The Lightning Network"

RELAY = "Like parcel relays: each courier takes a fee and has less time than the last"
page("five", "Five nodes, one payment of 1 BTC", RELAY,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: each hop forwards less: 200,000, 100,000, 0 and 0 satoshis above 1 BTC; the fee is 300,000",
                                   "Row 4: each hop's expiry steps down by 80 blocks, as set by lnd; the final delta is 80 too",
                                   "The total of 300,000 satoshis is 0.3% of 1 BTC, the book's fee",
                                   "NOT EXECUTED: a payment on the public network; its fees and failures are not shown"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "Satoshis above 1 BTC in the HTLC at each node", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 8,
       "labels": ["Bob", "Carol", "Diana", "Eric"], "series": [{"name": "satoshi", "data": OUT("Five", 1)[0]}]},
      con("Five", 0.5, 3.42, 9.0, 1.38, "Recorded: lnd 0.21.3-beta, five nodes on regtest", fs=10)],
     "Alice paid one bitcoin to Eric through Bob, Carol and Diana on five lnd nodes. Each hop forwarded a little less than it received, keeping a fee, so 300,000 satoshis went to the three middle nodes, which is 0.3 percent. The expiry of the payment fell by 80 blocks at each hop, so a node always has time to claim from the one before it. Nothing was paid on the public network.",
     "Each hop keeps a fee and gets less time than the hop before")

COURIER = "Like a courier who waits at the door until the recipient signs for the parcel"
page("hold", "A hold invoice keeps a payment in flight", COURIER,
     [beats(0.5, 1.38, 4.6, 1.75, ["Row 2: while held, the HTLCs along the line carried 10,000,000 to 10,300,000 satoshis",
                                   "Row 3: cancelling left every balance as before (True); pending HTLCs per node were 1, 2, 2, 2, 1",
                                   "Row 4: after the secret was released the payment status was SUCCEEDED",
                                   "NOT EXECUTED: multipath, trampoline routing and BOLT 12 offers; the line has one path"], fs=10),
      {"t": "chart", "x": 5.3, "y": 1.38, "w": 4.2, "h": 1.75, "ctype": "bar", "title": "HTLCs pending at each node while held", "dataLabels": True, "dlFmt": "0", "dlFs": 9,
       "labels": ["Alice", "Bob", "Carol", "Diana", "Eric"], "series": [{"name": "pending", "data": OUT("Hold", 2)[1]}]},
      con("Hold", 0.5, 3.42, 9.0, 1.38, "Recorded: lnd 0.21.3-beta, five nodes on regtest", fs=10)],
     "A hold invoice lets the receiver delay the release of the secret. While the invoice was held every node on the line kept the payment in flight, the end nodes with one pending payment and the middle ones with two. Cancelling the invoice returned every balance to what it was, and releasing the secret settled the payment. Only one path existed, so multipath payments were not tried.",
     "A payment can wait in flight, and then settle or unwind")

LAYERS = "Like a parcel wrapped in layers: each relay peels one and cannot see the rest"
page("wire", "Handshake and onion, checked on vectors", LAYERS,
     [con("Wire", 0.5, 1.7, 9.0, 1.8, "executed on the BOLT 8 and BOLT 4 vectors, saved on 2026-10-15", fs=10),
      beats(0.5, 3.85, 9.0, 0.7, ["Row 2: the BOLT 8 acts and the session key match the published vector (True, True, True)",
                                  "Rows 3 and 4: acts of 50 and 66 bytes; the onion matches the vector, 1,366 bytes for 1, 2 or 5 hops",
                                  "Row 5: the HMAC of the onion holds (True); a flipped bit breaks it (False, False)"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: the handshake between two lnd nodes on the wire; the vector was recomputed in Python.", fs=10)],
     "Two published test vectors were recomputed in Python. The BOLT 8 handshake gave the expected first and third acts, of 50 and 66 bytes, and the same session key. The BOLT 4 onion packet for five hops matched the vector at 1,366 bytes, and the size stays the same for one, two or five hops so that a relay cannot tell its place on the path. Flipping a single bit of the onion made its HMAC fail.",
     "A relay sees only its own layer, and every onion has one size")

BILL = "Like a bill with the payer reference printed on it: amount, hash and expiry"
page("invoice", "An invoice carries the payment hash", BILL,
     [con("Invoice", 0.5, 1.7, 9.0, 1.8, "Recorded: lnd 0.21.3-beta regtest; the BOLT 11 example is computed", fs=10),
      beats(0.5, 3.85, 9.0, 0.7, ["Row 2: lnd's invoice is for the regtest network (lnbcrt1), 100,000,000,000 msat, final delta 80",
                                  "Row 3: the SHA-256 of the payment secret equals the payment hash in the invoice (True)",
                                  "Row 5: the BOLT 11 example (lnbc2500u) asks 250,000 satoshis, stamped 2017-06-01 10:57:38, 65-byte signature"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: other implementations; Core Lightning, Eclair and LDK were read, not run.", fs=10)],
     "A Lightning invoice is a bech32 string that holds the network, the amount, the payment hash, an expiry and a signature. The invoice made by lnd named the regtest network, asked for one bitcoin in millisatoshis and set a final delta of 80 blocks. Hashing the secret gave the payment hash printed in it, and the BOLT 11 example decoded to 250,000 satoshis. Only lnd was run.",
     "An invoice is a signed promise that names the hash to be paid")

JOINT = "Like a joint account: both signatures to open it, one closing letter"
page("chain", "Channel transactions on the chain", JOINT,
     [con("Chain", 0.5, 1.7, 9.0, 1.8, "Recorded: lnd 0.21.3-beta regtest; the BOLT 3 vector is computed", fs=10),
      beats(0.5, 3.85, 9.0, 0.7, ["Row 2: the funding output is a script hash for a 2-of-2 multisig script and holds 4.0 BTC",
                                  "Row 3: the state number hides in locktime (0x20) and sequence (0x80); four outputs, 279 virtual bytes",
                                  "Rows 4 and 5: a close is one transaction, 2 in the channel's life; the BOLT 3 key vectors match"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: the lnd manifest signature (file not served, HTTP 404); only the archive hash was compared.", fs=10)],
     "On the chain a channel is two transactions, the funding output that needs both keys and a cooperative close. The commitment transaction hides a 48-bit state number in its lock time and sequence fields, which lets both sides number their states. A cooperative close was one transaction with lock time zero, so the channel's whole life used two on-chain transactions. The BOLT 3 key derivation vectors matched.",
     "A channel's whole life can be two transactions on the chain")

LEDGER = "Like a clerk who spots an old cheque and gives the whole account to its victim"
page("breach", "Breach, justice and fee bumping", LEDGER,
     [con("Breach", 0.5, 1.7, 9.0, 1.8, "Recorded: lnd 0.21.3-beta and Core 31.1 regtest", fs=10),
      beats(0.5, 3.85, 9.0, 0.7, ["Row 2: in the newest state Hitesh held 700,000,000 satoshis, Irene 299,996,530; Irene broadcast an older one",
                                  "Row 3: the justice transaction spends 2 outputs and pays Hitesh 999,990,380 satoshis",
                                  "Rows 4 and 5: a zero-fee parent is refused alone but accepted with its child, at 10.9 sat/vB"], fs=10),
      foot(0.5, 4.58, 9.0, 0.28, "NOT EXECUTED: a watchtower, and a close with HTLCs pending; the victim's own node answered the breach.", fs=10)],
     "When Irene broadcast an old state, Hitesh's node saw the revoked commitment and spent both of its outputs in a justice transaction. He received 999,990,380 satoshis of the 1,000,000,000 in the channel, and the rest went to the fee. A second test showed fee bumping: a zero-fee parent was refused alone and accepted as a package with a child that paid for both, at 10.9 satoshis per virtual byte.",
     "Cheating with an old state loses the whole channel")

story("paper", "PoonDryjaWhitepaper", "lightning_cut_nodes.png", "Stand-in picture: a chart of cut nodes, not the authors.",
      ["Joseph Poon and Thaddeus Dryja publish a white paper in February 2015; a copy was archived on 28 February 2015 (row 1)",
       "The draft kept at lightning.network is version 0.5.9.2 of 14 January 2016, 320 days later (row 2)",
       "The book still calls the network proposed; Lightning Labs launched it in 2018 (row 3)"],
      "PaperStory", [0, 1, 2], "executed on the Wikipedia page and the book, saved on 2026-10-15",
      "Joseph Poon and Thaddeus Dryja published a Lightning Network white paper in February 2015, and Wikipedia cites a copy archived on 28 February 2015. The draft that lightning.network keeps is version 0.5.9.2 of 14 January 2016, 320 days later. Lightning Labs launched the network in 2018, so the book's word proposed no longer holds, while its date for the first description, February 2015, does.",
      title="A paper that became a network")

story("torch", "LightningTorch", "jack_dorsey_2009.png", None,
      ["On 19 January 2019 hodlonaut starts the torch with 100,000 satoshis; each holder adds 10,000 (row 3)",
       "Well-known people such as Jack Dorsey and Elizabeth Stark pass it on",
       "Rows 1 and 2: three hops of fees; 1,000 satoshis delivered cost the sender 1,003"],
      "TorchStory", [0, 1, 2], "executed on the fee code and the Wikipedia page, saved on 2026-10-15",
      "On 19 January 2019 the pseudonymous Twitter user hodlonaut began a promotional test of the Lightning Network by sending 100,000 satoshis to a trusted recipient. Each recipient added 10,000 satoshis and sent the sum on, so it reached well-known people such as Jack Dorsey and Elizabeth Stark. Each hand-over was an ordinary Lightning payment, and the fee arithmetic of the book predicts what stays after each hop.",
      title="Satoshis passed from hand to hand")

# ---------------------------------------------------------------------------------------------- summary, resources, closing
page("summary", "The chapter in five lines", "One line per idea, each one provable from its slides",
     [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5, "items": [
         "A spent output stays spent, a signed payment never expires, and a hash proves a document existed",
         "Single-use seals and tweaked keys let colored coins keep their contract off the chain",
         "A channel is a two-key output, refunds with falling locks and a commitment that can be punished",
         "A hash-locked contract moves a payment through a line of nodes, each keeping a fee and less time",
         "The wire formats are fixed-size and checked by vectors; cheating with an old state loses the channel"]}],
     "These five lines are the deck in miniature. Each can be traced to a part of the route on slide 2 and to computations that ran on its slides. A line that feels unproven should send the reader back to that part's consoles.",
     "If a line feels unproven, its part's consoles carry the receipt")

page("resources", "Where to go from here", "Opened on %s; every entry is a live link in this file" % D.DATE,
     [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
         {"head": "Read", "rows": [
             ["Optech topic, hash time locked contracts", "https://bitcoinops.org/en/topics/htlc/"],
             ["Optech topic, anchor outputs", "https://bitcoinops.org/en/topics/anchor-outputs/"],
             ["Optech topic, watchtowers", "https://bitcoinops.org/en/topics/watchtowers/"]]},
         {"head": "Standards and papers", "rows": [
             ["BOLT 3, transaction and script formats", "https://raw.githubusercontent.com/lightning/bolts/master/03-transactions.md"],
             ["BIP 112, CHECKSEQUENCEVERIFY", "https://bips.dev/112/"],
             ["Poon and Dryja, the Lightning paper (draft 0.5.9.2)", "https://lightning.network/lightning-network-paper.pdf"]]},
         {"head": "Watch", "rows": [
             ["CuriousInventor: how Lightning works (video)", "https://www.youtube.com/embed/yKdK-7AtAMQ"],
             ["Poon and Dryja at Coinbase (video)", "https://www.youtube.com/embed/KN7Z5dGWcRY"]]},
         {"head": "Community", "rows": [
             ["mempool.space, the Lightning explorer", "https://mempool.space/lightning"],
             ["Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/"],
             ["Delving Bitcoin, research forum", "https://delvingbitcoin.org/"]]}]}],
     "Everything here is free to read or watch, and every link was opened on %s. A good start is the CuriousInventor video, then the Optech topic on hash time locked contracts next to the chapter. The research package for chapter 14 lists all %d sources with the passages used." % (D.DATE, NPUB),
     "Watch the first video, then read the Optech topic beside the chapter")

E.slide("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "What the chain guarantees, and what colored coins add",
            "How a payment channel is funded, refunded and punished",
            "How a payment crosses five nodes with fees and timelocks",
            "Why cheating with an old state loses the channel"]}],
        "Four claims, each carried by computations that ran on slides of this deck. A reader who can say them and point to the slide that proves them has the chapter. The research package for chapter 14 holds the sources and the test records behind them.", bg="dark")

# ---------------------------------------------------------------------------------------------- agenda and plan meta
E.agenda(["The chapter's questions", "What the chain guarantees", "Payment channels", "The Lightning Network"],
         "The route has three parts after the questions: what the chain guarantees, with the first bitcoin purchase, no double spend, proofs, pledges and colored coins; payment channels, with the first channels, Emma and Fabian, falling lock times, the penalty and the hash-locked contract; and the Lightning Network, with a five-node payment, hold invoices, the wire formats, the chain side and two stories. Each part carries true stories and corrections of the book that a reader can check on the slide.",
         "Three parts, four true stories, and a list of what was not run")
E.finish("Chapter 14: Second-Layer Apps", "1.0.0", "2026-10-16, first deck from the committed research package (commit f255770), to the CME look and feel; notes are short reader's prose")

planp = os.path.join(HERE, "deck_plan_v1_0_0.json")
plan = json.load(open(planp))
num = {k: [i + 1 for i, s in enumerate(plan["slides"]) if s["title"] == t][0] for k, t in KEEP.items()}
plan["meta"]["notes"] = "short reader's prose: 2-4 sentences, at most 100 words"
plan["meta"]["honesty"] = {
    "title": ["Bitcoin Core 31.1", REC],
    "recorded": [1] + [num[k] for k in ("double", "pledge", "seals", "emma", "ladder", "commit", "htlc", "five", "hold", "invoice", "chain", "breach")],
    "notExecuted": [num[k] for k in ("pizza", "seals", "htlc", "five", "hold", "wire", "invoice", "chain", "breach")],
    "standin": {str(num["pizza"]): ["Stand-in picture"], str(num["spillman"]): ["Stand-in picture"], str(num["paper"]): ["Stand-in picture"]},
    "vectors": [num[k] for k in ("pizza", "double", "spillman", "wire", "paper", "torch")],
}
plan["meta"]["analogies"] = [
    {"concept": "double spend", "analogy": CHEQUE, "slide": num["double"]},
    {"concept": "proof of existence and crowdfund", "analogy": PLEDGE, "slide": num["pledge"]},
    {"concept": "single-use seal", "analogy": TICKET, "slide": num["seals"]},
    {"concept": "payment channel", "analogy": TAB, "slide": num["emma"]},
    {"concept": "refund timelock ladder", "analogy": DATED, "slide": num["ladder"]},
    {"concept": "revocable commitment", "analogy": PENALTY, "slide": num["commit"]},
    {"concept": "hash time locked contract", "analogy": LOCKER, "slide": num["htlc"]},
    {"concept": "multi-hop payment", "analogy": RELAY, "slide": num["five"]},
    {"concept": "hold invoice", "analogy": COURIER, "slide": num["hold"]},
    {"concept": "onion packet", "analogy": LAYERS, "slide": num["wire"]},
    {"concept": "invoice", "analogy": BILL, "slide": num["invoice"]},
    {"concept": "channel transactions", "analogy": JOINT, "slide": num["chain"]},
    {"concept": "justice transaction", "analogy": LEDGER, "slide": num["breach"]},
]
json.dump(plan, open(planp, "w"), indent=1)
print("meta: honesty and %d analogies written; slide numbers %s" % (len(plan["meta"]["analogies"]), num))
