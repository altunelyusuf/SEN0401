#!/usr/bin/env python3
"""deck_build v3.0.0 (chapter 3, Bitcoin Core) - the generator of the chapter 3 deck 3.0.0 (task TK_Ch03_Deck_Build_R24, Iteration 24), a NEW file; the deck 2.3.0 stays as it is.
It writes (1) 03-materials/ch03/SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, (2) the chapter-code manifest 03-materials/ch03/page/chapter_code_ch03_v1_0_0.json (the examples in the order
of the deck's code slides: the manifest IS the deck's code boxes, drawn from the same list), (3) deck_plan_v3_0_0.json.
It reads the chapter research (the 42 key concepts of sen0401_ch03_research_v1_3_0.ttl), the story module sen0401_ch03_stories_v1_2_0.py (three stories with pictures and links), the
examples examples_v3_0_0.py and their recorded executions examples_out_v3_0_0.json (made by examples_run_v3_0_0.py under Python 3.14). Every number on a result picture is parsed from the
recorded output, never typed. The deck standard (D1-D12) is held as refusals in deck_kit_v3_0_0.py BEFORE the file is drawn; the independent checks measure the result afterwards.
Usage: python3 -B deck_build_v3_0_0.py"""
__version__ = "3.0.0"
import ast, hashlib, importlib.util, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v3_0_0 as X
from deck_kit_v3_0_0 import *

DECK_NAME = "SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx"
OUT = json.load(open(os.path.join(HERE, "examples_out_v3_0_0.json")))
PY = OUT["_python"]
EX = {e["id"]: e for e in X.EXAMPLES}
ASSETS = os.path.join(ROOT, "03-materials", "ch03", "assets")
asset = lambda f: os.path.join(ASSETS, f)
fmt = lambda v: "{:,}".format(v)


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


ST = load(os.path.join(TOOL, "sen0401_ch03_stories_v1_2_0.py"), "stories03")
STORY = {s["id"]: s for s in ST.STORIES}


def val(ex, i=0):
    return ast.literal_eval(OUT[ex][i][1])


def chart_rec(key):
    c = OUT["_charts"][key]
    return c["labels"], [int(v) if float(v).is_integer() else v for v in c["values"]]


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the parts of the deck; every divider names its concepts with one line of meaning and an everyday analogy (D10, D4); the headings of the book's sections stand in titles and subtitles
# ------------------------------------------------------------------------------------------------------------------------------------------------
PARTS = [(X.P1, "Core"), (X.P2, "Source"), (X.P3, "Node"), (X.P4, "API"), (X.P5, "Transactions"), (X.P6, "Blocks"), (X.P7, "Toolkits")]
DIV = {  # title -> (subtitle, notes, [(concept, meaning, analogy)])
 X.P1: ("Bitcoin Core: The Reference Implementation",
   "Part 1 asks what Bitcoin Core is. It began as the program Satoshi Nakamoto released in 2009, and it checks every rule itself as a full verification node. Changes reach it through numbered Bitcoin Improvement Proposals.",
   [("reference implementation", "The program against which other programs are measured.", "Think of the standard metre bar that every ruler was checked against."),
    ("full verification node", "A node that downloads every block and checks every rule itself.", "Think of an auditor who recounts every receipt instead of trusting a summary."),
    ("Bitcoin Improvement Proposal", "A numbered public document that proposes a change to Bitcoin.", "Think of a numbered bylaw proposed in a club's rulebook.")]),
 X.P2: ("Compiling Bitcoin Core from the Source Code",
   "Part 2 turns the source code into programs you can run. A release tag fixes which version you build, and release candidates are tried before a final tag exists. The build produces bitcoind, the node itself.",
   [("release tag", "A name that fixes one exact version of the source, such as v31.1.", "Think of a bookmark that always opens the same page."),
    ("release candidate", "A tagged version offered for testing before it becomes final.", "Think of a dress rehearsal before the opening night."),
    ("bitcoind", "The node program, which runs in the background.", "Think of the engine of a car, working while you do other things.")]),
 X.P3: ("Configuring the Bitcoin Core Node",
   "Part 3 starts the node and sets it up. A configuration file and the command line decide what the node does, and the data directory is where it keeps everything. Pruning, the transaction index and the memory limits trade disk, memory and features.",
   [("configuration file", "A text file of settings that the node reads when it starts.", "Think of the settings card taped to a coffee machine."),
    ("data directory", "The folder in which the node keeps blocks, state, logs and settings.", "Think of the node's filing cabinet."),
    ("prune", "An option that deletes old block files after the node has checked them.", "Think of an accountant who audits old invoices, keeps the totals and shreds the paper.")]),
 X.P4: ("Getting Information on Bitcoin Core's Status",
   "Part 4 talks to the running node. The command-line client bitcoin-cli sends JSON-RPC calls, and the node checks who is asking before it answers. The cookie is the default way in, and rpcauth is the fixed alternative.",
   [("bitcoin-cli", "A command-line tool that calls the node's interface.", "Think of a remote control for the node."),
    ("JSON-RPC", "A way to call a program's functions with small JSON messages.", "Think of an order slip handed over a counter."),
    ("cookie authentication", "A secret that the node writes to a file at every start.", "Think of a hotel key card coded anew for each guest."),
    ("rpcauth", "A stored user name with a salted hash of the password.", "Think of a bank that keeps a check value, not your PIN.")]),
 X.P5: ("Reading a transaction the way the node reports it",
   "Part 5 reads a transaction the way the node reports it. Each transaction has an identifier, a weight and a witness. We decode Alice's payment from chapter 2 and look at each part.",
   [("transaction ID", "The hash that names a transaction.", "Think of the tracking number on a parcel."),
    ("transaction malleability", "Changing a transaction's id without changing what it does.", "Think of a receipt whose number changes when the clerk re-signs it."),
    ("weight units", "The measure by which a block is filled.", "Think of postage by volume, where compact data costs less.")]),
 X.P6: ("Height, hash, merkle root and time",
   "Part 6 reads blocks. A block has a height, a hash made from its header, a merkle root of its transactions and a time. We rebuild each one ourselves with a few lines of Python.",
   [("block height", "A block's place in the chain, counted from zero.", "Think of a page number in a very long book."),
    ("block hash", "The name of a block, made by hashing its header.", "Think of a fingerprint taken from the page's header."),
    ("median time", "The middle timestamp of the last eleven blocks.", "Think of a median price that one odd sale cannot move.")]),
 X.P7: ("Using Bitcoin Core's Programmatic Interface",
   "Part 7 looks beyond Bitcoin Core. Libraries such as python-bitcoinlib call the node from your own programs, and other clients follow the same rules in other languages. We end with how fresh each toolkit is.",
   [("python-bitcoinlib", "A Python library that calls the node and builds transactions.", "Think of a phrasebook that turns your Python into the node's language."),
    ("alternative client", "Another program that follows Bitcoin's rules.", "Think of another airline flying the same routes under the same safety rules.")]),
}
# the divider's title is the book's section heading where the section has one; the parts' own names (route and strip) are in PARTS
DIV_TITLE = {X.P5: "Exploring and Decoding Transactions", X.P6: "Exploring Blocks", X.P4: "Bitcoin Core API", X.P3: "Running a Bitcoin Core Node", X.P7: "Alternative Clients, Libraries, and Toolkits",
             X.P2: "Bitcoin Development Environment", X.P1: "From Bitcoin to Bitcoin Core"}

# ------------------------------------------------------------------------------------------------------------------------------------------------
# the code slides: title, subtitle, takeaway (an everyday analogy for the concepts on the slide), notes; and the executed result as a picture
# ------------------------------------------------------------------------------------------------------------------------------------------------
TEXT = {
 "ex01": ("A version number that carries a vote", "A Bitcoin Improvement Proposal signals through bit flags",
          "Think of a ballot with 29 tick boxes, one for each proposal",
          "A block's version field is not a counter. Its top three bits mark the BIP 9 scheme, and every lower bit is a vote for one proposal. Here only bit 1 is set."),
 "ex02": ("Release tags sort by number, not by letters", "A release tag names the version; a release candidate carries rc",
          "Think of edition numbers: the tenth edition follows the ninth",
          "These are real tags of the Bitcoin repository. Sorted as text, v0.10.0 lands before v0.9.5, which is wrong. A release candidate is a tag with rc in it, so we leave those out first."),
 "ex03": ("What a release folder holds", "bitcoind is the node; bitcoin-cli is the client that calls it",
          "Think of bitcoind as the engine and bitcoin-cli as the steering wheel",
          "A release unpacks into seven programs and three helper parts. The one to know is bitcoind, the node. You steer it from the command line with bitcoin-cli."),
 "ex04": ("A download must match its published hash", "Checking a release against SHA256SUMS",
          "Think of the safety seal on a medicine bottle: break it and you can tell",
          "Each release ships a list of hashes. You hash your download and compare. If the two texts match, the file is the one that the builders signed for."),
 "ex05": ("The command line wins over the file", "The configuration file sets defaults; an option on the command line overrides them",
          "Think of a recipe card that you may override with a note on the fridge",
          "A configuration file holds the settings of a node. When the same option is also given on the command line, the command line wins. A script can therefore change one value for one run."),
 "ex06": ("How the database cache is shared out", "The dbcache setting is divided before it is used",
          "Think of a desk: two small drawers and one very large tabletop",
          "The dbcache option sizes the cache for the unspent outputs. Bitcoin Core first gives two small databases their share. Everything else goes to the cache of coins."),
 "ex07": ("Pruning and the transaction index do not mix", "prune deletes old blocks; txindex needs every block",
          "Think of a library that shreds old books and so cannot catalogue them all",
          "Pruning keeps only recent blocks. The transaction index must find any block that holds a transaction. The node therefore refuses both at once, and release 31.1 printed exactly that."),
 "ex08": ("An alert text is cleaned before it runs", "The alertnotify option runs your command when the node raises an alert",
          "Think of a mail room that removes anything dangerous before a letter reaches you",
          "The node can run a script of yours when something is wrong. The message goes into the command, so the node cleans it first. The hostile quotes vanish and the rest stays inside one word."),
 "ex09": ("One JSON-RPC call and its reply", "JSON-RPC is how every client talks to the node",
          "Think of an order slip: the same fields every time, and an answer on the same slip",
          "A call is a small JSON text with a method and parameters. The reply carries a result, an error and the id of the call. The sample reply is the one the book prints for the curl example."),
 "ex10": ("The cookie is a fresh password", "Cookie authentication needs no password to invent or store",
          "Think of a hotel key card that is recoded for every guest",
          "At every start bitcoind writes a new random secret to the .cookie file. A client that can read the file can call the node. The secret is 32 bytes, shown as 64 hexadecimal characters."),
 "ex11": ("rpcauth stores a salted hash, not the password", "A fixed credential for programs that cannot read the cookie",
          "Think of a bank that keeps a check value and never your PIN",
          "The rpcauth line holds a user, a random salt and a keyed hash of the password. Even a leaked configuration file does not reveal the password. A wrong password gives a different hash."),
 "ex12": ("Reading getblockchaininfo", "Getting Information on Bitcoin Core's Status",
          "Think of a car dashboard: it reports, and you do not touch the engine",
          "This is the answer of a real node of release 31.1 that had only the first block. It says which chain it is on, how many blocks it has verified and how hard the work is."),
 "ex13": ("Decoding Alice's transaction", "Exploring and Decoding Transactions",
          "Think of an X-ray: the same body, shown layer by layer",
          "The node's own decoder turns Alice's bytes into readable fields. Every output has a number, a value and a type. Two outputs, 20,000 and 75,000 satoshis, plus the 5,000 fee make her 100,000."),
 "ex14": ("The txid leaves the witness out", "The transaction ID and transaction malleability",
          "Think of a tracking number printed before anyone adds a signature",
          "The txid is a hash of the transaction without its witness. A third party can no longer change the txid by re-encoding a signature. That change is called transaction malleability, and segregated witness ended it."),
 "ex15": ("Weight units and virtual bytes", "How much of a block a transaction fills",
          "Think of postage by volume: compact, light data costs less",
          "Blocks are filled by weight units. Base bytes count four units each and witness bytes one. Alice's 194 bytes weigh 569 units, which is 143 virtual bytes."),
 "ex16": ("A block's name is the hash of its header", "The block hash and the block height of block 123,456",
          "Think of a fingerprint taken from the page's header line",
          "The header has six fields in 80 bytes. Hashing it twice and reversing the bytes gives the block hash, which starts with many zeros. The block's height, 123,456, counts the blocks before it."),
 "ex17": ("Rebuilding the merkle root", "One hash that commits to every transaction of the block",
          "Think of a tournament bracket: pairs play, winners meet, one champion remains",
          "Block 123,456 holds 13 transactions. Hashing neighbours in pairs gives 7, 4, 2 and finally 1 hash. That last hash is the merkle root stored in the header, and one changed transaction would change it."),
 "ex18": ("Median time of the last eleven blocks", "Block timestamps are guesses; the median time is not",
          "Think of a median price that one odd sale cannot move",
          "Miners write the time into every header, and it can be a little off. Bitcoin Core therefore uses the median of the last eleven times. We recompute the saved median of block 123,456."),
 "ex19": ("How fresh are the alternative toolkits", "python-bitcoinlib and its neighbours, by days since the latest release",
          "Think of the date on the newest delivery in a shop window",
          "Libraries for other languages and other clients exist, but they age. This is the number of days between each toolkit's latest release and the day we asked the registries. A library can be useful and still be old."),
}
RESULT_CAP = {"ex01": "Result: the 32 bits of the version", "ex02": "Result: the oldest tags, in two orders", "ex03": "Result: the programs of release 31.1",
              "ex04": "Result: the listed hash against the computed one", "ex05": "Result: which source wins for each option", "ex06": "Result: MiB of cache for each use",
              "ex07": "Result: the verdict for each option set", "ex08": "Result: the alert text, before and after", "ex09": "Result: the call and the reply",
              "ex10": "Result: the pieces of the cookie login", "ex11": "Result: the three parts of the rpcauth line", "ex12": "Result: what the node reports",
              "ex13": "Result: the outputs in satoshis", "ex14": "Result: two hashes of one transaction", "ex15": "Result: weight units of the transaction (log scale not needed)",
              "ex16": "Result: the six fields of the header", "ex17": "Result: hashes left on each level", "ex18": "Result: minutes since the first of the eleven blocks",
              "ex19": "Result: days since the latest release (log scale)"}
RESULT_CAP["ex15"] = "Result: weight units of the transaction"


def visual(s, ex, x, y, w):
    """draws the executed result of one example from its recorded values; returns (height used, reading line)"""
    if ex == "ex01":
        v, top, bits = val(ex, 0); b32 = val(ex, 1)
        groups = [b32[i:i + 4] for i in range(0, 32, 4)]; heads = ["%d-%d" % (31 - i * 4, 28 - i * 4) for i in range(8)]
        gf = table(s, x, y, w, [w / 8.0] * 8, [heads, groups], size=8.5, rowh=0.3, align=["c"] * 8)
        c = gf.table.cell(1, 0); c.fill.solid(); c.fill.fore_color.rgb = rgb(ORANGE)
        for r in c.text_frame.paragraphs[0].runs: r.font.color.rgb = rgb(WHITE); r.font.bold = True
        c = gf.table.cell(1, 7); c.fill.solid(); c.fill.fore_color.rgb = rgb(TEAL)
        for r in c.text_frame.paragraphs[0].runs: r.font.color.rgb = rgb(WHITE); r.font.bold = True
        table(s, x, y + 0.6 + 0.2, w, [1.6, 1.5], [["Part", "Value"], ["Version", v], ["Top three bits", "%s = BIP 9" % format(top, "03b")], ["Bits set below", ", ".join(str(b) for b in bits)]], rowh=0.3)
        return 0.6 + 0.2 + 4 * 0.3, "Orange cell: the BIP 9 marker. Teal cell: bit %s, the vote." % ", ".join(str(b) for b in bits)
    if ex == "ex02":
        t4, n4 = val(ex, 1), val(ex, 2)
        table(s, x, y, w, [0.6, 1.25, 1.25], [["Rank", "As text", "By number"]] + [[i + 1, t4[i], n4[i]] for i in range(4)], rowh=0.32, align=["c", "l", "l"])
        return 5 * 0.32, "As text, v0.10.0 comes first; by number the oldest tag, %s, does." % val(ex, 0)[1]
    if ex == "ex03":
        n, nl, ok = val(ex, 0); roles = val(ex, 1); libs = val(ex, 2)
        table(s, x, y, w, [1.15, 1.95], [["Program", "What it does"]] + [[a, b] for a, b in roles], size=9.5, rowh=0.285)
        return (len(roles) + 1) * 0.285, "Beside bin, libexec holds %d parts: %s." % (nl, ", ".join(libs))
    if ex == "ex04":
        eq, short = val(ex, 0); n = val(ex, 1)
        text(s, x, y, w, 0.62, [[("SHA256SUMS lists", {"bold": True, "size": 10})], [(short + "...", {"font": MONO, "size": 10})]], size=10, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.08, anchor="m", align="c", radius=0.15)
        arrow(s, x + w / 2, y + 0.62, x + w / 2, y + 0.92, color=ORANGE)
        text(s, x, y + 0.92, w, 0.62, [[("Your download hashes to", {"bold": True, "size": 10})], [(val(ex, 2) + "...", {"font": MONO, "size": 10})]], size=10, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.08, anchor="m", align="c", radius=0.15)
        arrow(s, x + w / 2, y + 1.54, x + w / 2, y + 1.84, color=ORANGE)
        text(s, x, y + 1.84, w, 0.62, [[("Equal: %s" % eq, {"bold": True, "size": 12, "color": WHITE})], [("all %d characters" % n, {"size": 10, "color": WHITE})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL, pad=0.08, anchor="m", align="c", radius=0.15)
        return 2.46, "Only the first 12 of %d characters are shown here." % n
    if ex == "ex05":
        used, conf, cli = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Option", "File", "Command", "Used"]] + [[k, conf.get(k, "-"), cli.get(k, "-"), used[k]] for k in sorted(used)]
        table(s, x, y, w, [0.95, 0.6, 0.9, 0.65], rows, rowh=0.34, hot={i for i, k in enumerate(sorted(used)) if k in cli}, align=["l", "c", "c", "c"])
        return len(rows) * 0.34, "dbcache is set in both places, so the command line's %s is used; txindex comes from the file." % cli["dbcache"]
    if ex == "ex06":
        lab, vals = chart_rec("ex06")
        chart(s, x, y, w, 2.25, "bar", lab, [("MiB", vals)], pointcolors=[MUTED, MUTED, TEAL])
        return 2.25, "Of %s MiB, %s serve the coins cache; the block index gets %s and the chain state %s." % (fmt(sum(vals)), fmt(vals[2]), vals[0], vals[1])
    if ex == "ex07":
        verdict, why, sets = val(ex, 0), val(ex, 1), val(ex, 2)
        rows = [["Options", "Verdict", "Why"]] + [[" + ".join("%s %s" % kv for kv in o.items()), v, w_] for o, v, w_ in zip(sets, verdict, why)]
        table(s, x, y, w, [1.1, 0.7, 1.3], rows, size=9, rowh=0.5, hot={2})
        return len(rows) * 0.5, "Recorded on release 31.1: the node refuses to start with both options."
    if ex == "ex08":
        cl, n = val(ex, 0); cmd = val(ex, 1); msg = val(ex, 2)
        table(s, x, y, w, [1.0, 2.1], [["Step", "Text"], ["Hostile alert", msg], ["After cleaning", cl], ["Command that runs", cmd]], size=9.5, rowh=0.5, hot={2})
        return 4 * 0.5, "%d characters were stripped, so no quote can end the word early." % n
    if ex == "ex09":
        meth, blocks, err = val(ex, 0); rid = val(ex, 1)
        text(s, x, y, w, 0.62, [[("Client sends", {"bold": True, "size": 10})], [("method %s" % meth, {"font": MONO, "size": 9.5})]], size=10, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.08, anchor="m", align="c", radius=0.15)
        arrow(s, x + w / 2, y + 0.62, x + w / 2, y + 0.92, color=ORANGE)
        text(s, x, y + 0.92, w, 0.62, [[("bitcoind", {"bold": True, "size": 12, "color": WHITE})], [("checks the caller, runs the method", {"size": 10, "color": WHITE})]], size=10, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL, pad=0.08, anchor="m", align="c", radius=0.15)
        arrow(s, x + w / 2, y + 1.54, x + w / 2, y + 1.84, color=ORANGE)
        text(s, x, y + 1.84, w, 0.62, [[("Reply", {"bold": True, "size": 10})], [("blocks %s, error %s, id %s" % (fmt(blocks), "null" if err is None else err, rid), {"font": MONO, "size": 9})]], size=10, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.08, anchor="m", align="c", radius=0.15)
        return 2.46, "An empty error means the call worked."
    if ex == "ex10":
        a, b, tok = val(ex, 0); user = val(ex, 1)[:-1]
        table(s, x, y, w, [1.65, 1.45], [["Piece", "Value"], ["User name", user], ["Secret, characters", a], ["Secret, bytes", b], ["Header sent", "Basic %s..." % tok]], size=9.5, rowh=0.34)
        return 5 * 0.34, "The header holds user:secret in Base64, so it starts with %s." % tok
    if ex == "ex11":
        lens = val(ex, 0); parts = val(ex, 1); same = val(ex, 2)
        user, salt = parts[0].split(":"); h = parts[1]
        table(s, x, y, w, [0.65, 1.8, 0.65], [["Part", "Starts with", "Length"], ["user", user, lens[0]], ["salt", salt[:12] + "...", lens[1]], ["hash", h[:12] + "...", lens[2]]], size=9.5, rowh=0.34, align=["l", "l", "c"])
        return 4 * 0.34, "The same salt with a wrong password gives a different hash: equal is %s." % same
    if ex == "ex12":
        chain, nb, ibd = val(ex, 0); best = val(ex, 1); cw = val(ex, 2); dif = val(ex, 3); prog = val(ex, 4)
        rows = [["Field", "Value"], ["chain", chain], ["blocks", nb], ["bestblockhash", best[:14] + "..."], ["difficulty", dif], ["chainwork", fmt(cw)], ["still downloading", ibd], ["verification", "%.1e" % prog]]
        table(s, x, y, w, [1.35, 1.75], rows, size=9.5, rowh=0.3)
        return len(rows) * 0.3, "The best block is the first one: its hash starts with %s." % best[:12]
    if ex == "ex13":
        lab, vals = chart_rec("ex13"); types = val(ex, 1); vs = val(ex, 2)
        chart(s, x, y, w, 2.25, "bar", lab, [("satoshis", vals)], pointcolors=[TEAL, ORANGE])
        return 2.25, "Output 0 is a %s output, output 1 a %s output; size %d virtual bytes." % (types[0], types[1], vs)
    if ex == "ex14":
        a, b = val(ex, 0); m1, m2 = val(ex, 1), val(ex, 2)
        table(s, x, y, w, [0.8, 1.0, 1.3], [["Hash", "Covers", "Starts with"], ["txid", "no witness", a], ["second hash", "everything", b]], size=9, rowh=0.42)
        table(s, x, y + 1.26 + 0.15, w, [2.1, 1.0], [["Same as Bitcoin Core says", "Equal"], ["txid", m1], ["hash", m2]], size=9, rowh=0.3)
        return 1.26 + 0.15 + 0.9, "The witness holds the signature, so only the second hash changes with it."
    if ex == "ex15":
        lab, vals = chart_rec("ex15"); wt, vb = val(ex, 0); sizes = val(ex, 1); core = val(ex, 2)
        chart(s, x, y, w, 2.25, "bar", lab, [("units", vals)], pointcolors=[TEAL, ORANGE, MUTED])
        return 2.25, "%d bytes in all: %d base and %d witness. Core says %d units; %d / 4 rounded up is %d." % (sizes[0], sizes[1], sizes[2], core, wt, vb)
    if ex == "ex16":
        n, ok, name = val(ex, 0); fields = val(ex, 1); h = val(ex, 2)
        rows = [["Field", "Bytes", "Starts with"]] + [[a, b, c] for a, b, c in fields]
        table(s, x, y, w, [1.3, 0.6, 1.2], rows, size=9.5, rowh=0.28, align=["l", "c", "l"])
        return len(rows) * 0.28, "Hashed twice and reversed: %s... equals the saved id: %s." % (h[:18], ok)
    if ex == "ex17":
        lab, vals = chart_rec("ex17"); eq = val(ex, 1)
        chart(s, x, y, w, 2.25, "bar", lab, [("hashes", vals)], pointcolors=[TEAL, ORANGE, ORANGE, ORANGE, TEAL])
        return 2.25, "The single hash at the top equals the root saved in the block: %s." % eq
    if ex == "ex18":
        lab, vals = chart_rec("ex18"); med, ok = val(ex, 0)
        chart(s, x, y, w, 2.25, "bar", lab, [("minutes", vals)], pointcolors=[ORANGE] * 5 + [TEAL] + [ORANGE] * 5, size=8)
        return 2.25, "Teal: the sixth value of the sorted times, %s, the same as the saved median time: %s." % (fmt(med), ok)
    if ex == "ex19":
        lab, vals = chart_rec("ex19")
        chart(s, x, y, w, 2.45, "bar", lab, [("days", vals)], log=True, size=7, pointcolors=[ORANGE] * len(lab))
        return 2.45, "python-bitcoinlib is %s days old, bitcoinjs-lib %s days (log scale)." % (fmt(dict(zip(lab, vals))["python-bitcoinlib"]), dict(zip(lab, vals))["bitcoinjs-lib"])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# slide builders: each draws one slide and returns its entry of the plan (kind, title, items, take, bg) for the owner checks that read deck_plan_v3_0_0.json
# ------------------------------------------------------------------------------------------------------------------------------------------------
ANALOGIES = []
RECORDED = []
relp = lambda f: os.path.relpath(asset(f), HERE)


def s_title(d, k, n):
    s = d.new("Chapter 2 followed one payment through the network. Chapter 3 opens the program that checks every rule, Bitcoin Core, and shows how to build it, run it and ask it questions. Every result in this deck was computed by the chapter library from saved data.")
    for i in range(3):
        text(s, 0.6 + i * 0.95, 0.75, 0.75, 0.75, ["₿"] if i == 2 else [""], size=26, bold=True, color=WHITE if i == 2 else INK, align="c", anchor="m",
             shape=MSO_SHAPE.OVAL, fill=ORANGE if i == 2 else None, line=ORANGE)
        if i < 2: arrow(s, 1.35 + i * 0.95, 1.12, 1.55 + i * 0.95, 1.12, color=ORANGE)
    text(s, 0.6, 1.9, 5.0, 1.2, ["Chapter 3: Bitcoin Core"], size=30, font=SERIF, anchor="m")
    text(s, 0.6, 3.2, 5.0, 0.7, ["The reference implementation: build it, run it, ask it questions"], size=15, italic=True, color=MUTED)
    text(s, 0.6, 4.2, 8.8, 0.3, ["Python %s; every number is computed by the chapter library from saved data; no Bitcoin Core node was run." % PY], size=11, color=MUTED)
    text(s, 0.6, 4.62, 8.0, 0.45, ["SEN0401 Special Topics in Software Engineering: Block Chain · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University"], size=11, color=MUTED)
    picture(s, asset("c3_cointocode.png"), 5.85, 0.7, 3.65, 2.41, "A bitcoin coin dissolving into lines of code", mode="fit")
    text(s, 5.85, 3.15, 3.65, 0.5, ["A coin that turns into code - from the course's 2025 deck"], size=9, color=MUTED)
    number(s, k, n)
    return dict(kind="title", title="Chapter 3: Bitcoin Core", items=[{"t": "img", "path": relp("c3_cointocode.png")}, {"t": "foot"}], bg="light")


def s_route(d, k, n, ranges):
    s = d.new("The route has seven parts that follow the program from its source code to the toolkits around it. Three true stories and nineteen code examples are spread across them. Every example has a picture of its result.")
    frame(d, s, k, n, "Today's route", "Seven parts around one program; every range is a slide you can jump to", "Seven parts, three true stories, nineteen examples")
    names = ["1. Questions and the chapter map"] + ["%d. %s" % (i + 2, PARTS[i][0]) for i in range(7)] + ["9. Summary, resources, closing"]
    for i, a in enumerate(names):
        cx, cy = 0.5 + (i % 3) * 2.15, 1.4 + (i // 3) * 1.15
        text(s, cx, cy, 2.0, 1.05, [[(a, {"bold": True, "font": SERIF, "size": 11})], [("(slides %d-%d)" % ranges[i], {"size": 10.5, "color": MUTED})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD,
             line=LINE, pad=0.1, anchor="m", radius=0.1)
    stats = [(str(n), "slides, numbered bottom-right"), ("3", "true stories, each told by 5N1K"), ("19", "code examples, each with a picture of its result")]
    for i, (a, b) in enumerate(stats):
        y = 1.4 + i * 1.15
        rect(s, 6.95, y, 2.55, 1.05, CARD, line=LINE)
        text(s, 7.1, y + 0.05, 2.25, 0.42, [a], size=22, font=SERIF, color=ORANGE, anchor="m")
        text(s, 7.1, y + 0.5, 2.25, 0.5, [b], size=10.5, color=MUTED)
    return dict(kind="content", title="Today's route", items=[{"t": "boxes"}, {"t": "stat"}], take="Seven parts, three true stories, nineteen examples")


def s_questions(d, k, n):
    s = d.new("The six questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all six has understood the chapter.")
    frame(d, s, k, n, "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary")
    qs = ["What makes Bitcoin Core the reference implementation of Bitcoin?", "How do I choose a release, check it and build it from source?",
          "Which settings decide what a node stores, remembers and trusts?", "How do I ask a running node questions, and who may ask?",
          "How do I decode a transaction and tell its txid from its weight?", "How can I check a block myself, and what else can talk to a node?"]
    for i, q in enumerate(qs):
        y = 1.4 + i * 0.58
        text(s, 0.5, y, 0.44, 0.44, [str(i + 1)], size=14, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.OVAL, fill=TEAL)
        text(s, 1.12, y, 8.38, 0.44, [q], size=13, anchor="m")
    return dict(kind="content", title="The questions this chapter answers", items=[{"t": "numlist", "items": qs}])


def s_map(d, k, n):
    s = d.new("Six steps carry us from the source code to the data of the chain. We read the code and pick a release, build it, run it, ask it questions and read what it says. The last step looks at other programs that speak to a node.")
    frame(d, s, k, n, "The chapter in one picture", "One program, six steps; the parts of the deck follow them", "Six steps from the source code to the data of the chain")
    steps = [("1 Source", "Read the code; pick a release."), ("2 Build", "Compile it and check the files."), ("3 Run", "Start the node and set it up."),
             ("4 Ask", "Call its interface with JSON-RPC."), ("5 Read", "Decode transactions and blocks."), ("6 Extend", "Libraries and other clients.")]
    w, gap = 1.38, 0.144
    for i, (a, b) in enumerate(steps):
        x = 0.5 + i * (w + gap)
        text(s, x, 1.7, w, 0.5, [a], size=12, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL if i < 5 else ORANGE, radius=0.2)
        text(s, x, 2.4, w, 0.9, [b], size=11)
        if i < 5: arrow(s, x + w + 0.01, 1.95, x + w + gap - 0.01, 1.95, color=ORANGE)
    text(s, 0.5, 3.6, 9.0, 0.9, ["Nineteen code examples run along this path. Each prints its result under the listing and shows it as a picture beside it."], size=14, color=MUTED, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
         fill=CARD, line=LINE, pad=0.15, anchor="m", radius=0.1)
    return dict(kind="content", title="The chapter in one picture", items=[{"t": "flow", "steps": [a for a, _ in steps]}, {"t": "text"}], take="Six steps from the source code to the data of the chain")


def s_divider(d, k, n, part, idx):
    sub, notes, items = DIV[part]; title = DIV_TITLE[part]
    s = d.new(notes)
    text(s, 0.6, 0.45, 8.8, 0.8, [title], size=28 if len(title) <= 34 else 26, font=SERIF, anchor="m")
    text(s, 0.6, 1.28, 8.8, 0.4, [sub], size=15, italic=True, color=MUTED, anchor="m")
    m = len(items); cw = (8.8 - (m - 1) * 0.2) / m
    for i, (pill, mean, ana) in enumerate(items):
        x = 0.6 + i * (cw + 0.2)
        if len(pill.split()) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words (D10)" % pill)
        if len(ana.split()) < 5 or len(mean.split()) < 5: raise SystemExit("REFUSED: divider meaning or analogy of %r under 5 words (D10)" % pill)
        text(s, x, 1.95, cw, 0.42, [pill], size=12, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL, pad=0.06, radius=0.3)
        text(s, x, 2.48, cw, 0.8, [mean], size=11.5)
        text(s, x, 3.34, cw, 0.8, [ana], size=11.5, italic=True, color=ORANGE)
        ANALOGIES.append({"concept": pill, "analogy": ana, "slide": k})
    gf = table(s, 0.6, 4.4, 8.8, [8.8 / 7.0] * 7, [[p[1] for p in PARTS]], size=10, rowh=0.4, head=False, align=["c"] * 7)
    for j in range(7):
        c = gf.table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = rgb(ORANGE if j == idx else CARD)
        for r in c.text_frame.paragraphs[0].runs: r.font.color.rgb = rgb(WHITE if j == idx else MUTED); r.font.bold = (j == idx)
    number(s, k, n)
    return dict(kind="section", title=title, sub=sub, items=[{"t": "groups", "items": [{"pill": a, "meaning": b, "analogy": c} for a, b, c in items]}, {"t": "striptable"}], bg="light")


def s_architecture(d, k, n):
    s = d.new("Bitcoin Core is one program with several parts. Peers and the connection manager bring in blocks and transactions, the validation engine checks them, and the storage engine keeps headers, blocks and coins. The interface at the right lets your own programs ask questions.")
    frame(d, s, k, n, "Inside the program", "The parts of Bitcoin Core, from the course textbook", "One program: it listens, checks, stores and answers")
    picture(s, asset("mbc3_0301.png"), 0.5, 1.35, 3.6, 3.37, "Diagram of Bitcoin Core: peer discovery, connection manager, mempool, validation engine, storage engine, wallet and RPC", mode="fit")
    text(s, 0.5, 4.72, 3.6, 0.3, ["Antonopoulos and Harding, Mastering Bitcoin 3e, CC BY-SA 4.0"], size=8, color=MUTED)
    cards = [("Connection manager", "Talks to the peers and passes on blocks and transactions."), ("Validation engine", "Checks every block and every transaction against the rules."),
             ("Storage engine", "Keeps the headers, the blocks and the set of coins."), ("RPC", "Lets your own programs ask the node questions.")]
    for i, (a, b) in enumerate(cards):
        text(s, 4.4, 1.4 + i * 0.9, 5.1, 0.8, [[(a, {"bold": True, "font": SERIF, "size": 12.5})], [(b, {"size": 11})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.12, anchor="m", radius=0.1)
    return dict(kind="content", title="Inside the program", items=[{"t": "img", "path": relp("mbc3_0301.png")}, {"t": "cards"}], take="One program: it listens, checks, stores and answers")


def s_builds(d, k, n):
    s = d.new("A build has three decisions. You select a release tag, you configure which features to build, and you build the executables. Each step has a single command, and a clean tag makes the result repeatable.")
    frame(d, s, k, n, "Three steps from source to executables", "The three headings of the book's building section", "Select, configure, build: three steps, one set of programs")
    cards = [("Selecting a Bitcoin Core Release", "Check out the tag of a final release, not of a candidate.", "Think of choosing the printed edition, not the draft."),
             ("Configuring the Bitcoin Core Build", "Choose options, such as whether to build the wallet or the window.", "Think of ticking the options on a car order form."),
             ("Building the Bitcoin Core Executables", "The compiler turns the source into the programs of the bin folder.", "Think of an oven that turns dough into bread.")]
    w, gap = 2.8, 0.3
    for i, (a, b, c) in enumerate(cards):
        x = 0.5 + i * (w + gap)
        text(s, x, 1.45, w, 0.62, [a], size=12, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL if i < 2 else ORANGE, pad=0.08, radius=0.15)
        text(s, x, 2.3, w, 1.0, [b], size=12)
        text(s, x, 3.45, w, 0.9, [c], size=12, italic=True, color=ORANGE)
        ANALOGIES.append({"concept": a, "analogy": c, "slide": k})
        if i < 2: arrow(s, x + w + 0.03, 1.76, x + w + gap - 0.03, 1.76, color=ORANGE)
    return dict(kind="content", title="Three steps from source to executables", items=[{"t": "flow", "steps": [a for a, _, _ in cards]}, {"t": "text"}], take="Select, configure, build: three steps, one set of programs")


DATADIR = {"blocks": "the block files and their index", "chainstate": "the set of unspent outputs", "debug.log": "the node's diary, line by line", "bitcoin.conf": "your configuration file",
           "peers.dat": "addresses of the peers it knows", "mempool.dat": "waiting transactions, saved at shutdown", "fee_estimates.dat": "what the node learned about fees",
           "banlist.json": "peers it refuses to talk to", "settings.json": "settings changed while running", "bitcoind.pid": "the number of the running process", "demo": "the folder of the demo wallet"}


def s_datadir(d, k, n):
    entries = [l.split(": ", 1)[1] for l in open(os.path.join(TOOL, "ch03-evidence", "datadir_entries_31_1_v1_0_0.txt")).read().splitlines() if l.startswith("data dir entry")]
    assert sorted(entries) == sorted(DATADIR), (sorted(entries), sorted(DATADIR))
    s = d.new("Everything the node knows lives in its data directory. Blocks and the chain state are the big parts, the log is the node's diary, and the configuration file holds your settings. The cookie file appears while the node runs.")
    frame(d, s, k, n, "Inside the data directory", "What the offline node of release 31.1 had written", "The data directory is the whole memory of the node")
    rows = [["Entry", "What it holds"]] + [[e, DATADIR[e]] for e in entries]
    table(s, 0.5, 1.4, 5.7, [1.7, 4.0], rows, size=9.5, rowh=0.285)
    text(s, 6.45, 1.4, 3.05, 1.25, ["Think of the data directory as the node's filing cabinet: long drawers for the blocks, a small box for the state of the chain, the diary on top."], size=12, italic=True, color=ORANGE,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.12, anchor="m", radius=0.08)
    ANALOGIES.append({"concept": "data directory", "analogy": "Think of the data directory as the node's filing cabinet: long drawers for the blocks, a small box for the state of the chain, the diary on top.", "slide": k})
    text(s, 6.45, 2.85, 3.05, 1.3, ["The .cookie file with the node's temporary password is also written here while the node runs, and removed when it stops."], size=11.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.12, anchor="m", radius=0.08)
    text(s, 6.45, 4.3, 3.05, 0.5, ["Recorded: the listing of the offline node of release 31.1."], size=9.5, color=MUTED)
    RECORDED.append(k)
    return dict(kind="content", title="Inside the data directory", sub="What the offline node of release 31.1 had written", items=[{"t": "table"}, {"t": "cards"}], take="The data directory is the whole memory of the node")


def s_memory(d, k, n):
    lab, vals = chart_rec("mempool")
    s = d.new("Two settings reduce what a node asks of its machine. Blocks-only mode stops it from collecting loose transactions, and the mempool limit caps the waiting room. The default limit is 300 megabytes, and blocks-only mode needs only 5.")
    frame(d, s, k, n, "Two ways to spend less memory", "The blocksonly and maxmempool options", "A node can trade features for memory, and keep verifying everything")
    text(s, 0.5, 1.4, 4.2, 0.32, ["Mempool limit in megabytes"], size=11, bold=True, color=TEAL)
    chart(s, 0.5, 1.8, 4.2, 2.4, "bar", lab, [("megabytes", vals)], pointcolors=[ORANGE, TEAL])
    text(s, 0.5, 4.3, 4.2, 0.6, ["300 MB are %.1f MiB; blocks-only mode needs %d times less." % (vals[0] * 10**6 / 2**20, vals[0] // vals[1])], size=11, color=MUTED)
    cards = [("blocksonly", "The node takes blocks from its peers but no loose transactions.", "Think of reading only the daily paper, not every rumour."),
             ("maxmempool", "A cap, in megabytes, on the waiting room of unconfirmed transactions.", "Think of a clinic's waiting room: it has only so many chairs.")]
    for i, (a, b, c) in enumerate(cards):
        y = 1.4 + i * 1.75
        rect(s, 5.0, y, 4.5, 1.6, CARD, line=LINE, radius=0.06); rect(s, 5.05, y + 0.12, 0.07, 1.36, ORANGE, rounded=False)
        text(s, 5.27, y + 0.08, 4.1, 0.85, [[(a, {"bold": True, "font": SERIF, "size": 14})], [(b, {"size": 11.5})]], size=11.5)
        text(s, 5.27, y + 1.0, 4.1, 0.5, [c], size=11.5, italic=True, color=ORANGE)
        ANALOGIES.append({"concept": a, "analogy": c, "slide": k})
    return dict(kind="content", title="Two ways to spend less memory", sub="The blocksonly and maxmempool options", items=[{"t": "chart", "ex": "mempool"}, {"t": "cards"}], take="A node can trade features for memory, and keep verifying everything")


def s_heights(d, k, n):
    h, tip = 123456, 123461
    s = d.new("A block's height counts the blocks before it, so the first block has height zero. Each block built on top adds a confirmation. The numbers in the picture are an example, not a live chain.")
    frame(d, s, k, n, "Height, depth and confirmations", "Example numbers: block 123,456 with five blocks on top", "A confirmation is one more block on top of yours")
    w, gap = 1.3, 0.34
    for i in range(6):
        x = 0.5 + i * (w + gap)
        text(s, x, 1.5, w, 0.55, [fmt(h + i)], size=13, font=SERIF, bold=True, color=WHITE if i in (0, 5) else INK, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE,
             fill=ORANGE if i == 0 else (TEAL if i == 5 else CARD), line=LINE, radius=0.15)
        text(s, x, 2.12, w, 0.3, ["%d confirmation%s" % (tip - h - i + 1, "" if tip - h - i + 1 == 1 else "s")], size=9.5, color=MUTED, align="c")
        if i < 5: arrow(s, x + w + gap - 0.03, 1.775, x + w + 0.03, 1.775, color=ORANGE)
    text(s, 0.5, 2.5, 9.0, 0.3, ["Each block points back to the one before it. The tip, %s, has one confirmation: itself." % fmt(tip)], size=10.5, color=MUTED)
    cards = [("block height", "The place of a block in the chain, counted from zero at the first block.", "Think of a page number in a very long book."),
             ("confirmations", "The number of blocks from yours to the tip, yours included.", "Think of witnesses who sign a contract one after another.")]
    for i, (a, b, c) in enumerate(cards):
        x = 0.5 + i * 4.6
        rect(s, x, 3.0, 4.4, 1.9, CARD, line=LINE, radius=0.06); rect(s, x + 0.05, 3.12, 0.07, 1.66, ORANGE, rounded=False)
        text(s, x + 0.27, 3.08, 4.0, 1.0, [[(a.capitalize(), {"bold": True, "font": SERIF, "size": 14})], [(b, {"size": 11.5})]], size=11.5)
        text(s, x + 0.27, 4.2, 4.0, 0.6, [c], size=11.5, italic=True, color=ORANGE)
        ANALOGIES.append({"concept": a, "analogy": c, "slide": k})
    return dict(kind="content", title="Height, depth and confirmations", sub="Example numbers: block 123,456 with five blocks on top", items=[{"t": "flow", "steps": [fmt(h + i) for i in range(6)]}, {"t": "cards"}], take="A confirmation is one more block on top of yours")


def s_prog(d, k, n):
    s = d.new("A library can speak to the node for you. python-bitcoinlib builds the JSON-RPC call, sends it over HTTP and returns the result as a Python value. On the offline node of release 31.1 a call for the block count returned zero.")
    frame(d, s, k, n, "Using Bitcoin Core's Programmatic Interface", "python-bitcoinlib calls the node for you", "Your code can ask the node anything the command line can")
    steps = [("Your Python script", "asks for the block count"), ("python-bitcoinlib", "builds the JSON-RPC call"), ("HTTP", "carries it to the node"), ("bitcoind", "answers with the result")]
    w, gap = 1.95, 0.4
    for i, (a, b) in enumerate(steps):
        x = 0.5 + i * (w + gap)
        text(s, x, 1.5, w, 1.0, [[(a, {"bold": True, "font": SERIF, "size": 12, "color": WHITE})], [(b, {"size": 10.5, "color": WHITE})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL if i < 3 else ORANGE,
             pad=0.08, anchor="m", align="c", radius=0.12)
        if i < 3: arrow(s, x + w + 0.03, 2.0, x + w + gap - 0.03, 2.0, color=ORANGE)
    text(s, 0.5, 2.9, 4.4, 1.3, ["Think of a waiter who carries your order to the kitchen and brings the dish back to your table."], size=12.5, italic=True, color=ORANGE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.15, anchor="m", radius=0.08)
    ANALOGIES.append({"concept": "python-bitcoinlib", "analogy": "Think of a waiter who carries your order to the kitchen and brings the dish back to your table.", "slide": k})
    text(s, 5.1, 2.9, 4.4, 1.3, ["Recorded on the offline node of release 31.1: the call getblockcount returned 0, and python-bitcoinlib imported under Python 3.14.4."], size=11.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.15, anchor="m", radius=0.08)
    RECORDED.append(k)
    return dict(kind="content", title="Using Bitcoin Core's Programmatic Interface", sub="python-bitcoinlib calls the node for you", items=[{"t": "flow", "steps": [a for a, _ in steps]}, {"t": "text"}], take="Your code can ask the node anything the command line can")


def s_code(d, k, n, ex):
    e = EX[ex]; title, sub, take, notes = TEXT[ex]
    s = d.new(notes); frame(d, s, k, n, title, sub, take)
    ANALOGIES.append({"concept": title, "analogy": take, "slide": k})
    out = OUT[ex][0][1]
    if len(out) > 62: raise SystemExit("REFUSED %s: output line over 62 characters (D12)" % ex)
    y = 1.4; lay = []
    for gi, g in enumerate(e["groups"]):
        for l in g["lines"]:
            if len(l) + 4 > 62: raise SystemExit("REFUSED %s: code line over 62 characters with its prompt (D12): %s" % (ex, l))
        rows = [code_runs(l) for l in g["lines"]]
        if gi == len(e["groups"]) - 1: rows.append([(out, {"color": CODE_OUT})])
        th = est(rows, 5.4, 10, mono=True) + 0.02; nh = est([g["note"]], 5.7, 11) + 0.04
        lay.append((y, rows, th, g["note"], nh)); y += th + 0.2 + 0.06 + nh + 0.12
    for (y0, rows, th, note, nh) in lay:      # all listings first, so that the executed rows of the slide follow one another (the deck check reads them in shape order)
        rect(s, 0.5, y0, 5.7, th + 0.2, CODE, radius=0.06)
    for (y0, rows, th, note, nh) in lay:
        text(s, 0.66, y0 + 0.1, 5.4, th, rows, size=10, font=MONO)
    for (y0, rows, th, note, nh) in lay:      # then the plain-language note beside each listing
        text(s, 0.5, y0 + th + 0.2 + 0.06, 5.7, nh, [note], size=11)
    if y > 4.9: raise SystemExit("REFUSED %s: the listings need %.2f in (limit 4.9)" % (ex, y))
    stamp = "run under Python %s - T is the chapter library of the page (%s)" % (PY, X.LIB)
    if e["rec"]:
        stamp = "run under Python %s - Recorded data: %s - T is the chapter library" % (PY, e["rec"]); RECORDED.append(k)
    text(s, 0.5, y - 0.04, 5.7, 0.32, [stamp], size=9, color=MUTED)
    text(s, 6.4, 1.4, 3.1, 0.4, [RESULT_CAP[ex]], size=11, bold=True, color=TEAL)
    used, reading = visual(s, ex, 6.4, 1.85, 3.1)
    text(s, 6.4, 1.85 + used + 0.12, 3.1, 0.75, [reading], size=11)
    kind = {"native chart": "chart", "table": "table", "diagram": "diagram"}[e["picture"]]
    return dict(kind="content", title=title, sub=sub, items=[{"t": "codeblocks", "ex": ex}, {"t": kind, "ex": ex}], take=take)


def s_story(d, k, n, sid, a):
    st = STORY[sid]; s = d.new(a["notes"])
    frame(d, s, k, n, a["title"], a["sub"], a["take"])
    credit = "Picture: " + st["credit"] + a["credit_tail"]
    host = re.sub(r"^https?://(www\.)?", "", st["link"]).split("/")[0]
    def n5box(x, y, w, h, lab, body):
        parts = [(lab + " ", {"bold": True, "color": ORANGE, "size": 10.5})] + ([(body, {"size": 10.5})] if isinstance(body, str) else [(b, dict(o, size=10.5)) for b, o in body])
        text(s, x, y, w, h, [parts], size=10.5)
    def readbox(x, y, w):
        text(s, x, y, w, 0.3, [[("READ ", {"bold": True, "color": ORANGE, "size": 10.5}), (st["linkLabel"], {"size": 10.5, "color": TEAL, "link": st["link"]}), (("" if len(st["linkLabel"]) > 24 else " - " + host), {"size": 10.5, "color": MUTED})]], size=10.5)
    if a.get("wide"):
        picture(s, asset(st["photo"]), 0.5, 1.35, 4.3, 1.31, a["alt"], mode="fit")
        text(s, 0.5, 2.7, 4.3, 0.4, [credit], size=8.5, color=MUTED)
        for i in range(3): n5box(0.5, 3.15 + i * 0.6, 4.3, 0.56, *a["n5"][i])
        for i in range(3): n5box(5.05, 1.4 + i * 0.95, 4.45, 0.9, *a["n5"][3 + i])
        readbox(5.05, 4.4, 4.45)
    else:
        if a["pic_w"] == 3.0: picture(s, asset(st["photo"]), 0.5, 1.35, 3.0, 2.45, a["alt"], focus=a.get("focus", 0.3))
        else: picture(s, asset(st["photo"]), 0.5 + (3.0 - a["pic_w"]) / 2, 1.35, a["pic_w"], 2.45, a["alt"], mode="fit")
        text(s, 0.5, 3.88, 3.0, 0.62, [credit], size=8.5, color=MUTED)
        for i, (lab, body) in enumerate(a["n5"]): n5box(3.75, 1.33 + i * 0.52, 5.75, 0.48, lab, body)
        readbox(3.75, 4.5, 5.75)
    return dict(kind="content", title=a["title"], sub=a["sub"], items=[{"t": "img", "path": relp(st["photo"]), "cap": credit}, {"t": "beats", "items": ["%s %s" % (l, b if isinstance(b, str) else "".join(x for x, _ in b)) for l, b in a["n5"]]},
                {"t": "factrow", "who": st["who"], "where": st["where"], "when": st["when"], "link": st["link"], "linkText": st["linkLabel"]}], take=a["take"])


def s_summary(d, k, n):
    s = d.new("Each row answers one of the six opening questions in a line. If you can say each answer in your own words, using the everyday pictures of this chapter, you have the chapter.")
    frame(d, s, k, n, "Summary: the six answers", "The questions of slide 3, answered", "Reference, release, settings, interface, transaction, block")
    rows = [["Question", "Answer in one line"],
            ["1 What makes Core the reference?", "It came first, it defines the rules by running them, and it is built in the open."],
            ["2 How do I get a release I trust?", "Check out a final tag, build it, and compare its hash with the published one."],
            ["3 What do the settings decide?", "What is stored, how much memory is used, and which alerts run."],
            ["4 How do I ask a node, and who may?", "JSON-RPC calls; the cookie or an rpcauth credential lets you in."],
            ["5 How do I read a transaction?", "Decode it; the txid ignores the witness, and weight counts it."],
            ["6 How do I check a block?", "Hash the 80-byte header and rebuild the merkle root yourself."]]
    table(s, 0.5, 1.4, 9.0, [3.1, 5.9], rows, size=11, rowh=0.45)
    return dict(kind="content", title="Summary: the six answers", items=[{"t": "table"}], take="Reference, release, settings, interface, transaction, block")


RES = [("Read", "Mastering Bitcoin, chapter 3 (source text)", "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/develop/ch03_bitcoin-core.adoc", "The chapter this deck follows."),
       ("Read", "Bitcoin Core releases", "https://bitcoincore.org/en/releases/", "Every release, with notes and signatures."),
       ("Read", "Bitcoin Core RPC reference", "https://developer.bitcoin.org/reference/rpc/", "Every call with its arguments and results."),
       ("Standards and papers", "BIP 1: what a BIP is", "https://bips.dev/1/", "How a change to Bitcoin is proposed and numbered."),
       ("Standards and papers", "Bitcoin white paper", "https://bitcoin.org/bitcoin.pdf", "Nakamoto's nine pages of 31 October 2008."),
       ("Verify and build", "Build guide for Unix", "https://raw.githubusercontent.com/bitcoin/bitcoin/master/doc/build-unix.md", "Dependencies and commands for bitcoind."),
       ("Community", "Bitcoin Core PR Review Club", "https://bitcoincore.reviews/", "Weekly sessions that read one change together."),
       ("Community", "Delving Bitcoin", "https://delvingbitcoin.org/", "Developers discuss protocol and Core in the open."),
       ("Community", "Bitcoin Stack Exchange", "https://bitcoin.stackexchange.com/", "Ask a question, read the voted answers."),
       ("Watch", "Tracing Bitcoin Core v23.0 (talk video)", "https://www.youtube.com/embed/XuRnL393pSk", "A developer watches a running node with tracepoints.")]


def s_resources(d, k, n):
    s = d.new("These links are all open and free. Start with the chapter source and the release page, try the RPC reference against your own node, and watch the talk on tracing a running node. The community links are where questions get answered.")
    frame(d, s, k, n, "Resources: read, try, watch, ask", "Every link was opened on 25 October 2026; free to use", "Build a release, run it offline, and ask it getblockchaininfo")
    for i, (kind, lab, url, why) in enumerate(RES):
        col, row = i // 5, i % 5
        x, y = 0.5 + col * 4.6, 1.4 + row * 0.72
        text(s, x, y, 4.4, 0.64, [[(kind + "  ", {"bold": True, "color": ORANGE, "size": 9}), (lab, {"size": 11.5, "bold": True, "color": TEAL, "link": url})], [(why, {"size": 10, "color": MUTED})]], size=11)
    groups = []
    for head in ("Read", "Standards and papers", "Verify and build", "Community", "Watch"):
        groups.append({"head": head, "rows": [[lab, url, why] for kd, lab, url, why in RES if kd == head]})
    return dict(kind="content", title="Resources: read, try, watch, ask", items=[{"t": "links", "groups": groups}], take="Build a release, run it offline, and ask it getblockchaininfo")


def s_closing(d, k, n):
    s = d.new("That is Bitcoin Core from source to answers. Chapter 4 turns to keys and addresses, which the node's wallet depends on. Bring your questions.")
    rect(s, 0.5, 0.9, 9.0, 3.7, CODE, radius=0.04)
    text(s, 0.9, 1.3, 8.2, 1.1, ["Questions?"], size=44, font=SERIF, color=WHITE, anchor="m")
    text(s, 0.9, 2.5, 8.2, 0.5, ["From the source code to a node you can ask"], size=18, italic=True, color=C_NUM)
    text(s, 0.9, 3.3, 8.2, 0.45, ["Next: chapter 4, Keys and Addresses"], size=15, font=SERIF, color=CODE_OR)
    text(s, 0.9, 4.0, 8.2, 0.4, ["Python %s; every result in this deck was computed by the chapter library, not typed" % PY], size=11, color=CODE_TXT)
    number(s, k, n)
    return dict(kind="closing", title="Questions?", items=[{"t": "bullets", "items": ["Next: chapter 4, Keys and Addresses"]}], bg="dark")


def when_runs(iso, long):
    return [(iso, {}), (" (%s)" % long, {})]


STORIES = {
 "FirstRelease": dict(title="Version 0.1, set in stone", sub="8 January 2009 · the first release of Bitcoin", take="The program came first: the reference implementation defines the rules", pic_w=3.0, focus=0.3,
    alt="Bronze bust of Satoshi Nakamoto in Budapest", credit_tail=", Wikimedia Commons",
    n5=[("WHO", "Satoshi Nakamoto, the pseudonymous author of the white paper and of the first program."), ("WHAT", "Version 0.1 of Bitcoin, a Windows program that anyone could download and run."),
        ("WHEN", when_runs("2009-01-08", "8 January 2009")), ("WHERE", "Announced on the metzdowd.com cryptography mailing list; the download sat on SourceForge."),
        ("WHY", "Only running software could start the network. Later he wrote that, once 0.1 was out, the core design was set in stone."),
        ("HOW", "A short post with the download link, five days after the first block had been mined.")],
    notes="In January 2009 Satoshi Nakamoto published version 0.1 of the Bitcoin program. A year and a half later he wrote that its core design was set in stone. That is why Bitcoin Core is called the reference implementation: the software came first, and the rules are what it does."),
 "MaintainerHandoffs": dict(title="The project that outlives its keyholders", sub="7 April 2014 · Andresen hands over to van der Laan", take="The reference implementation is an institution, not a person", pic_w=3.0, focus=0.2,
    alt="Gavin Andresen at Web Summit 2014", credit_tail=", Wikimedia Commons",
    n5=[("WHO", "Gavin Andresen, who led the software after Satoshi Nakamoto, and Wladimir van der Laan, his successor."), ("WHAT", "Andresen passed the lead-maintainer role of Bitcoin Core to van der Laan."),
        ("WHEN", when_runs("2014-04-07", "7 April 2014")), ("WHERE", "The public bitcoin/bitcoin repository on GitHub, where every change is reviewed in the open."),
        ("WHY", "Andresen wanted to focus on protocol work, and a reference cannot wait for one person."), ("HOW", "He named van der Laan, who led until 2022; Satoshi had handed the project to Andresen in 2011.")],
    notes="Bitcoin Core outlived its first author. Satoshi Nakamoto handed the project to Gavin Andresen in 2011, and on 7 April 2014 Andresen passed the lead to Wladimir van der Laan. A reference implementation needs a team and public review, not one keyholder."),
 "ReproducibleBuilds": dict(title="Dozens of builders, one identical binary", sub="13 September 2021 · Bitcoin Core 22.0 moves to Guix", take="Verify, don't trust: the project applies its own rule to itself", wide=True,
    alt="The GNU Guix logo", credit_tail=", Wikimedia Commons",
    n5=[("WHO", "Carl Dong, who wrote the Guix build system, and the independent builders who sign its results."), ("WHAT", "Release 22.0 was the first built with Guix, so anyone can rebuild the binary bit for bit."),
        ("WHEN", when_runs("2021-09-13", "13 September 2021")), ("WHERE", "The guix.sigs repository, beside bitcoin/bitcoin on GitHub."),
        ("WHY", "A downloaded program asks for trust; here several builders compare hashes instead of taking one person's word."),
        ("HOW", "Each builder compiles the tagged source and signs the hashes. Release 31.1 shows 11 good signatures on its SHA256SUMS.")],
    notes="Anyone can ask whether a downloaded binary really matches the source. Since release 22.0 Bitcoin Core builds with Guix, so independent builders get identical files and sign their hashes. For release 31.1 the checksum file carries eleven good signatures."),
}

# ------------------------------------------------------------------------------------------------------------------------------------------------
# the order of the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
SEQ = [("title",), ("route",), ("questions",), ("map",),
       ("div", X.P1, 0), ("story", "FirstRelease"), ("arch",), ("code", "ex01"),
       ("div", X.P2, 1), ("builds",), ("code", "ex02"), ("code", "ex03"), ("story", "ReproducibleBuilds"), ("code", "ex04"),
       ("div", X.P3, 2), ("code", "ex05"), ("datadir",), ("code", "ex06"), ("code", "ex07"), ("memory",), ("code", "ex08"), ("story", "MaintainerHandoffs"),
       ("div", X.P4, 3), ("code", "ex09"), ("code", "ex10"), ("code", "ex11"), ("code", "ex12"),
       ("div", X.P5, 4), ("code", "ex13"), ("code", "ex14"), ("code", "ex15"),
       ("div", X.P6, 5), ("heights",), ("code", "ex16"), ("code", "ex17"), ("code", "ex18"),
       ("div", X.P7, 6), ("prog",), ("code", "ex19"),
       ("summary",), ("resources",), ("closing",)]


def main():
    n = len(SEQ)
    pos = [i + 1 for i, q in enumerate(SEQ) if q[0] == "div"]; summ = [j + 1 for j, q in enumerate(SEQ) if q[0] == "summary"][0]
    ranges = [(3, pos[0] - 1)] + [(pos[i], (pos[i + 1] - 1) if i + 1 < len(pos) else summ - 1) for i in range(7)] + [(summ, n)]
    d = Deck(); code_slides = {}; plan = []
    for k, q in enumerate(SEQ, 1):
        kind = q[0]
        if kind == "title": e = s_title(d, k, n)
        elif kind == "route": e = s_route(d, k, n, ranges)
        elif kind == "questions": e = s_questions(d, k, n)
        elif kind == "map": e = s_map(d, k, n)
        elif kind == "div": e = s_divider(d, k, n, q[1], q[2])
        elif kind == "story": e = s_story(d, k, n, q[1], STORIES[q[1]])
        elif kind == "code": e = s_code(d, k, n, q[1]); code_slides[q[1]] = k
        elif kind == "arch": e = s_architecture(d, k, n)
        elif kind == "builds": e = s_builds(d, k, n)
        elif kind == "datadir": e = s_datadir(d, k, n)
        elif kind == "memory": e = s_memory(d, k, n)
        elif kind == "heights": e = s_heights(d, k, n)
        elif kind == "prog": e = s_prog(d, k, n)
        elif kind == "summary": e = s_summary(d, k, n)
        elif kind == "resources": e = s_resources(d, k, n)
        elif kind == "closing": e = s_closing(d, k, n)
        e["n"] = k; e["notes"] = d.last_notes; e.setdefault("bg", "light"); e.setdefault("sub", ""); plan.append(e)
    deck_path = os.path.join(ROOT, "03-materials", "ch03", DECK_NAME)
    d.prs.save(deck_path)
    # the chapter-code manifest: the examples in the order of the deck's code slides, drawn from the same list
    lib_path = os.path.join(TOOL, "sen0401_ch03_core_lib_v1_0_0.py")
    setup = "# setup: the chapter library of the page (T = the chapter 3 library); the page runs this before every example\n" + X.PRELUDE.rstrip("\n")
    exs = []
    for o, q in enumerate([q for q in SEQ if q[0] == "code"], 1):
        e = EX[q[1]]
        exs.append({"order": o, "id": e["id"], "name": e["name"], "slide": code_slides[e["id"]], "branch": e["branch"], "library": X.LIB, "needs": ["setup"],
                    "code": "\n".join(e["lines"]), "show": [{"expression": x, "expected": r} for x, r in OUT[e["id"]]], "result_picture": e["picture"]})
    man = {"manifest": "chapter_code_ch03_v1_0_0", "chapter": 3, "deck": DECK_NAME, "deck_version": "3.0.0", "python_of_expected_values": PY,
           "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the chapter library defined in the page; the manifest equals the deck's code boxes",
           "library": {"module": X.LIB, "file": "08-tooling/sen0401_ch03_core_lib_v1_0_0.py", "sha256": hashlib.sha256(open(lib_path, "rb").read()).hexdigest(),
                       "import": "import sen0401_ch03_core_lib_v1_0_0 as T", "requires": "Python standard library only (hashlib, hmac, json, struct, datetime; base64 is imported by the setup)"},
           "setup": {"code": setup, "data": {}}, "examples": exs}
    json.dump(man, open(os.path.join(ROOT, "03-materials", "ch03", "page", "chapter_code_ch03_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
    meta = {"title": "Chapter 3: Bitcoin Core", "sub": "SEN0401, third-edition deck 3.0.0", "version": "3.0.0", "python": PY, "total": n,
            "redesign": "2026-10-25, task TK_Ch03_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
            "notes": "short reader's prose: 2-4 sentences, at most 60 words", "analogies": ANALOGIES,
            "honesty": {"title": ["no Bitcoin Core node"], "no_node": True, "notExecuted": [], "recorded": sorted(RECORDED), "standin": {}, "vectors": []}}
    json.dump({"meta": meta, "slides": plan}, open(os.path.join(HERE, "deck_plan_v3_0_0.json"), "w"), indent=1, ensure_ascii=False)
    print("wrote %s (%d slides, %d code slides) and chapter_code_ch03_v1_0_0.json (%d examples)" % (DECK_NAME, n, len(code_slides), len(exs)))


if __name__ == "__main__":
    main()
