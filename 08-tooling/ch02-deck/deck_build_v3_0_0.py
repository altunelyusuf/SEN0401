#!/usr/bin/env python3
"""deck_build v3.0.0 (chapter 2, How Bitcoin Works) - the generator of the chapter 2 deck 3.0.0 (task TK_Ch02_Deck_Build_R24, Iteration 24), a NEW file; the deck 2.3.0 stays as it is.
It writes (1) 03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, (2) the chapter-code manifest 03-materials/ch02/page/chapter_code_ch02_v1_0_0.json (the examples in the order
of the deck's code slides: the manifest IS the deck's code boxes, drawn from the same list), (3) deck_plan_v3_0_0.json.
It reads the chapter research (the 25 key concepts of sen0401_ch02_research_v1_4_0.ttl), the story module sen0401_ch02_stories_v1_2_0.py (three stories with pictures and links), the examples
examples_v3_0_0.py and their recorded executions examples_out_v3_0_0.json (made by examples_run_v3_0_0.py under Python 3.14). Every number on a result picture is parsed from the recorded
output, never typed. The deck standard (D1-D12) is held as refusals in deck_kit_v3_0_0.py BEFORE the file is drawn; the independent checks measure the result afterwards.
Usage: python3 -B deck_build_v3_0_0.py"""
__version__ = "3.0.0"
import ast, hashlib, importlib.util, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, HERE); sys.path.insert(0, TOOL)
import examples_v3_0_0 as X
from deck_kit_v3_0_0 import *
import sen0401_ch02_tx_lib_v1_0_0 as T

DECK_NAME = "SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx"
OUT = json.load(open(os.path.join(HERE, "examples_out_v3_0_0.json")))
PY = OUT["_python"]
EX = {e["id"]: e for e in X.EXAMPLES}
ASSETS = os.path.join(ROOT, "03-materials", "ch02", "assets")
asset = lambda f: os.path.join(ASSETS, f)
fmt = lambda v: "{:,}".format(v)


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


ST = load(os.path.join(TOOL, "sen0401_ch02_stories_v1_2_0.py"), "stories02")
STORY = {s["id"]: s for s in ST.STORIES}


def val(ex, i=0):
    return ast.literal_eval(OUT[ex][i][1])


# ------------------------------------------------------------------------------------------------------------------------------------------------
# the research concepts: the 25 key concepts must each stand on a slide with an everyday analogy (D4) and on a slide at all (D11)
# ------------------------------------------------------------------------------------------------------------------------------------------------
PARTS = [("Buying from an Online Store", "Store"), ("Bitcoin Transactions", "Transactions"), ("Coin Selection", "Coin selection"),
         ("Constructing a Transaction", "Construction"), ("Adding the Transaction to the Blockchain", "Blockchain"), ("Spending the Transaction", "Spending")]
DIV = {  # title -> (subtitle, notes, [(concept, meaning, analogy)])
 "Buying from an Online Store": ("Alice pays Bob's Store: one real payment, followed all the way",
   "Part 1 starts where Alice does: with an invoice from an online store. We meet the whole system first, then the smallest unit of money and the link that carries the invoice.",
   [("How Bitcoin Works", "One payment is followed from the shop's invoice to the blockchain.", "Think of tracking a parcel from the shop to your door."),
    ("Bitcoin Overview", "Users, wallets, nodes and miners share one record that nobody owns.", "Think of a town where every shop keeps an identical ledger."),
    ("satoshi", "The smallest unit: one hundred-millionth of a bitcoin.", "Think of the cent, only a million times smaller.")]),
 "Bitcoin Transactions": ("Inputs, outputs, chains and change",
   "Part 2 opens the payment itself. A transaction is a ledger entry: it spends earlier outputs and creates new ones, and the difference is the fee.",
   [("Transaction Inputs and Outputs", "Inputs spend earlier outputs; outputs lock new amounts to new owners.", "Think of handing over banknotes and receiving new ones."),
    ("Transaction Chains", "Each input points to an earlier output, back to where the coins began.", "Think of a trail of signed receipts, each naming the one before."),
    ("Making Change", "Part of a spent coin returns to you as a new output.", "Think of paying with a 20 note for a 15 item and getting 5 back.")]),
 "Coin Selection": ("Which coins to spend, and what shape the payment takes",
   "Part 3 asks how a wallet chooses what to spend. Coins are spent whole, so the choice decides the change, and the same rule produces payments, consolidations and batches.",
   [("Common Transaction Forms", "Payment, consolidation and batching are shapes of inputs and outputs.", "Think of a single cheque, a deposit of coins and a payroll run."),
    ("consolidation transaction", "Many small inputs are merged into one output.", "Think of swapping a jar of small coins for one banknote."),
    ("change address", "A fresh address of your own that receives the change.", "Think of a new envelope addressed to yourself.")]),
 "Constructing a Transaction": ("The wallet assembles, prices and signs the payment",
   "Part 4 builds Alice's transaction step by step. The wallet finds inputs, writes the outputs, leaves a fee and signs, and the fee rate decides how much change comes back.",
   [("Getting the Right Inputs", "Find unspent outputs that together cover the payment and the fee.", "Think of counting coins onto the counter before paying."),
    ("Creating the Outputs", "Write down who receives how much, and where the change goes.", "Think of filling in the payee and the amount on a cheque."),
    ("transaction fee", "Inputs minus outputs: the difference that the miner keeps.", "Think of the postage stamp that pays the post office.")]),
 "Adding the Transaction to the Blockchain": ("From a node's inbox to a block that others build on",
   "Part 5 follows the signed transaction to a block. Miners search for a lucky number, the block is added, and every block on top makes the payment harder to reverse.",
   [("Bitcoin Mining", "Miners search for a number that makes a block of transactions valid.", "Think of rolling dice until a very rare number turns up."),
    ("confirmation", "Every block built on top makes the payment harder to reverse.", "Think of more witnesses signing a contract."),
    ("genesis block", "The first block of the chain, fixed in the software of every node.", "Think of page one of a ledger, printed into the binding.")]),
 "Spending the Transaction": ("When Bob may spend, and what every node checks first",
   "Part 6 closes the loop. Bob can spend his new output, and every node checks the same rules, so that a block which breaks one is refused.",
   [("consensus rules", "Rules that every node checks the same way; a block that breaks one is refused.", "Think of the rules of chess that every player and referee enforce."),
    ("block explorer", "A website where anyone can look up blocks, transactions and addresses.", "Think of a parcel tracker for money.")]),
}
CARDS = [("input", "A reference to an earlier output being spent, with a signature that proves ownership.", "Think of a banknote you hand over to the cashier."),
         ("output", "An amount of bitcoin locked to a new owner until it is spent.", "Think of a banknote you receive in return.")]

# ------------------------------------------------------------------------------------------------------------------------------------------------
# the code slides: title, subtitle, explanation beside the listing, takeaway, notes; and the executed result as a picture
# ------------------------------------------------------------------------------------------------------------------------------------------------
TEXT = {
 "ex01": ("Satoshis are whole numbers", "Converting the invoice amount without decimals",
          "The invoice writes 0.01577764 bitcoin. The library turns it into whole satoshis and back again, and no digit is lost on the way.",
          "Inside the network every amount is a whole number of satoshis",
          "Bitcoin counts in satoshis, one hundred-millionth of a bitcoin. Decimals are only for people. Converting with whole numbers keeps every digit, which floating point would not."),
 "ex02": ("Reading Bob's invoice", "A payment link is a small, readable address",
          "The invoice is a link. The part before the question mark names the address; the part after it holds the amount and a label for the wallet to show.",
          "One link carries the address, the amount and the label",
          "BIP 21 defines the bitcoin link that wallets and QR codes use. We split it into its parts with the standard library. The wallet then knows whom to pay, how much, and what to call the payee."),
 "ex03": ("Inputs equal outputs plus the fee", "Alice's payment as double-entry bookkeeping",
          "Alice spends one 100,000-satoshi output. Bob's Store gets 75,000, 20,000 comes back to her, and the 5,000 left over is the fee.",
          "Whatever the outputs do not claim becomes the miner's fee",
          "A transaction balances like a ledger. The inputs add up to 100,000 satoshis and the outputs to 95,000. The difference of 5,000 is written nowhere; it is implied, and the miner collects it."),
 "ex04": ("The txid is shown backwards", "The same 32 bytes in two orders",
          "An input names the earlier transaction by its identifier. The bytes are stored in one order and displayed in the reverse order, so we flip them.",
          "Explorers show the identifier in reverse byte order",
          "The identifier of Alice's earlier transaction is a 32-byte hash. Inside a transaction it is stored one way, and block explorers print it the other way round. Reversing the bytes converts between them."),
 "ex05": ("Size in virtual bytes and the fee rate", "How a miner compares transactions",
          "Proof data counts for less weight. Four weight units make one virtual byte, rounded up. The fee divided by that size is the rate miners rank by.",
          "Miners rank transactions by fee per virtual byte",
          "Alice's transaction weighs 569 units, which is 143 virtual bytes. Her fee of 5,000 satoshis divided by 143 gives about 35 satoshis per virtual byte. Blocks have limited room, so miners pick the best rates first."),
 "ex06": ("Which outputs are still unspent", "Walking the chain of figure 2-3",
          "Collect every output that some input has spent. The outputs left over are unspent: those are the coins that can still be used.",
          "Unspent outputs are the coins that exist right now",
          "Each transaction in the chain spends an earlier output and creates new ones. Collecting what was spent leaves the unspent outputs. Wallets and nodes keep exactly this set, because only these coins can be spent."),
 "ex07": ("Coin selection: pick, pay, change back", "A wallet chooses coins to cover a payment",
          "The wallet holds three coins and must pay 80,000. It takes coins in order until they cover the payment; the surplus becomes change.",
          "Coins are taken whole, so the surplus returns as change",
          "A wallet cannot cut a coin in two. It takes whole coins until the payment is covered, then sends the surplus back to itself as change. Real wallets use smarter rules, but this is the idea."),
 "ex08": ("Three common shapes of a transaction", "Counting inputs, outputs and the fee",
          "A payment has one input and two outputs. A consolidation merges three coins into one. Batching pays four people from one coin and needs no change.",
          "The same ledger rule fits every shape",
          "Three forms cover most transactions. A payment spends a coin and returns change. A consolidation merges many small coins into one, and batching pays many people at once. In every case inputs minus outputs is the fee."),
 "ex09": ("A higher fee rate leaves less change", "Pricing the payment before signing",
          "The size is 143 virtual bytes. Each rate turns that size into a fee, and whatever the fee takes is missing from the change.",
          "The wallet decides the fee; the change is what remains",
          "When the wallet builds the outputs it chooses a fee rate. The fee is the rate times the size. The change output is what is left after paying Bob and the fee, so a higher rate means smaller change."),
 "ex10": ("One more zero, many more tries", "Mining as a search for a lucky number",
          "We hash a text plus a counter until the result starts with zeros. Each extra zero makes success about sixteen times rarer, so the search takes longer.",
          "Mining is a search; more zeros means more work",
          "A miner changes a number, the nonce, and hashes again until the result starts with enough zeros. Nobody can shortcut the search, but anyone can check the answer with one hash. The network sets how many zeros are needed."),
 "ex11": ("The first block header is 80 bytes", "Hashing the genesis block's header",
          "A header holds six fields. Hashing these 80 bytes twice and reversing the bytes gives the name of the first block, which starts with many zeros.",
          "A block's name is the hash of its 80-byte header",
          "The genesis block was mined on 3 January 2009. Its header packs a version, the previous block, a summary of the transactions, a time, a difficulty and a nonce. Hashing it twice gives the famous name that starts with ten zeros."),
 "ex12": ("Nakamoto's catch-up table, recomputed", "Section 11 of the white paper, run again",
          "This is the paper's own formula. For an attacker with 10 percent of the hash power the chance falls from 20.5 percent at one block to 0.02 percent at six.",
          "Every confirmation makes a reversal much less likely",
          "Section 11 of the white paper computes how likely an attacker is to catch up. We reran the formula and obtained the paper's table to seven places. The chance drops fast with every block, which is why six confirmations became a habit."),
 "ex13": ("The reward halves every 210,000 blocks", "One of the consensus rules, in one line",
          "The reward starts at 50 bitcoin and is shifted right by one bit every 210,000 blocks. Each era pays half of the one before it.",
          "Halving is a rule every node enforces, not a promise",
          "The block reward is a consensus rule. Every node computes it the same way and refuses a block that claims more. Halving every 210,000 blocks, about four years, is what limits the total number of bitcoin."),
 "ex14": ("Two outputs that wrapped around", "Block 74,638 and the value overflow of 2010",
          "Each output held about 92 billion bitcoin. Added in a signed 64-bit number the sum wraps around and turns negative, which slipped past the old check.",
          "One overflow created 184 billion bitcoin; one new rule ended it",
          "In August 2010 a block paid out two huge outputs. Their sum overflowed a 64-bit integer, so the software thought the outputs were small. A new rule was shipped within hours, and the honest chain, without the forged coins, won."),
}
RESULT_CAP = {"ex01": "Result: one amount, written two ways", "ex02": "Result: the parts of the invoice link", "ex03": "Result: where Alice's 100,000 satoshis go",
              "ex04": "Result: the same identifier, two byte orders", "ex05": "Result: weight, size, fee and rate", "ex06": "Result: the five outputs of the chain",
              "ex07": "Result: payment, coins picked, change", "ex08": "Result: inputs, outputs and fee of each shape", "ex09": "Result: change left at four fee rates",
              "ex10": "Result: tries needed for 1 to 4 zeros (log scale)", "ex11": "Result: the six fields of the header", "ex12": "Result: the attacker's chance per block",
              "ex13": "Result: the block reward of each era, in bitcoin", "ex14": "Result: the overflow, number by number"}


def visual(s, ex, x, y, w):
    """draws the executed result of one example from its recorded values; returns (height used, reading line)"""
    if ex == "ex01":
        sats, back = val(ex, 0); one, small = val(ex, 2), val(ex, 1)
        table(s, x, y, w, [1.55, 1.55], [["Written as", "Whole satoshis"], ["1 bitcoin", fmt(one)], [back, fmt(sats)], ["0.00075", fmt(small)]], rowh=0.34)
        return 4 * 0.34, "No decimals are needed inside Bitcoin; the amount is a whole number of satoshis."
    if ex == "ex02":
        sch, amt, lab = val(ex, 0); adr = val(ex, 1)
        table(s, x, y, w, [0.9, 2.2], [["Part", "Value"], ["scheme", sch], ["address", adr + "..."], ["amount", amt + " bitcoin"], ["label", lab]], rowh=0.34)
        return 5 * 0.34, "The wallet reads these four parts and fills in the payment for Alice."
    if ex == "ex03":
        a, b, fee = val(ex, 0); outs = val(ex, 1)
        chart(s, x, y, w, 2.25, "bar", ["Input", "To Bob", "Change", "Fee"], [("satoshis", [a, outs[0], outs[1], fee])], pointcolors=[TEAL, ORANGE, CODE_OR, MUTED])
        return 2.25, "%s in = %s out + %s fee: the ledger balances." % (fmt(a), fmt(b), fmt(fee))
    if ex == "ex04":
        (r8, s8), (r8e, s8e), n = val(ex, 0), val(ex, 1), val(ex, 2)
        table(s, x, y, w, [1.3, 0.9, 0.9], [["Order", "First 8", "Last 8"], ["Stored", r8, r8e], ["Shown", s8, s8e]], rowh=0.34)
        return 3 * 0.34, "The same %d bytes, read in opposite directions." % n
    if ex == "ex05":
        vb, rate = val(ex, 0); wu = 569
        table(s, x, y, w, [1.35, 1.75], [["Measure", "Value"], ["Weight", "%d units" % wu], ["Size", "%d virtual bytes" % vb], ["Fee", "5,000 satoshis"], ["Fee rate", "%s sat/vB" % rate]], rowh=0.34)
        return 5 * 0.34, "569 / 4 = %s, rounded up to %d." % (val(ex, 1), vb)
    if ex == "ex06":
        free = val(ex, 0); v = val(ex, 1); spent = val(ex, 2); fees = val(ex, 3)
        rows = [["Output", "Satoshis", "State"]] + [[o, fmt(n), "unspent" if o in free else "spent"] for o, n in v.items()]
        table(s, x, y, w, [0.95, 1.05, 1.1], rows, rowh=0.3, hot={i for i, (o, _) in enumerate(v.items()) if o in free})
        return len(rows) * 0.3, "Fees: Tx2 paid %s, Tx3 paid %s satoshis." % (fmt(fees[0]), fmt(fees[1]))
    if ex == "ex07":
        pick, change = val(ex, 0); tot = val(ex, 1)
        chart(s, x, y, w, 2.25, "bar", ["Payment", "Coins picked", "Change back"], [("satoshis", [80000, tot, change])], pointcolors=[TEAL, ORANGE, CODE_OR])
        return 2.25, "Coins %s are taken, 80,000 is paid, %s goes back." % (" + ".join(fmt(c) for c in pick), fmt(change))
    if ex == "ex08":
        fee = val(ex, 0); shape = val(ex, 1)
        rows = [["Form", "In", "Out", "Fee"]] + [[k.capitalize(), shape[k][0], shape[k][1], fmt(fee[k])] for k in fee]
        table(s, x, y, w, [1.4, 0.45, 0.5, 0.75], rows, rowh=0.36, align=["l", "c", "c", "r"])
        return 4 * 0.36, "Consolidation merges coins; batching pays many people at once."
    if ex == "ex09":
        ch_, fees = val(ex, 0), val(ex, 1)
        chart(s, x, y, w, 2.25, "bar", ["10 sat/vB", "20 sat/vB", "35 sat/vB", "100 sat/vB"], [("change", ch_)], pointcolors=[ORANGE, ORANGE, ORANGE, MUTED])
        return 2.25, "At 100 sat/vB the fee takes %s; only %s returns as change." % (fmt(fees[3]), fmt(ch_[3]))
    if ex == "ex10":
        tries = val(ex, 0)
        chart(s, x, y, w, 2.25, "bar", ["1 zero", "2 zeros", "3 zeros", "4 zeros"], [("tries", tries)], log=True, pointcolors=[ORANGE, ORANGE, ORANGE, TEAL])
        return 2.25, "Each extra zero needs about 16 times more tries on average."
    if ex == "ex11":
        h = val(ex, 1); ln = val(ex, 2); g = T.GENESIS
        rows = [["Field", "Bytes", "Value"], ["Version", ln[0], g["version"]], ["Previous block", ln[1], "all zeros"], ["Merkle root", ln[2], g["merkle"][:8] + "..."],
                ["Time", ln[3], g["time"]], ["Bits", ln[4], "%x" % g["bits"]], ["Nonce", ln[5], g["nonce"]]]
        table(s, x, y, w, [1.15, 0.55, 1.4], rows, rowh=0.27, size=9.5, align=["l", "c", "l"])
        return 7 * 0.27, "Hashed twice: %s..." % h[:16]
    if ex == "ex12":
        q10, q30 = val(ex, 1), val(ex, 2)
        chart(s, x, y, w, 2.3, "line", [str(i) for i in range(7)], [("attacker 10%", q10), ("attacker 30%", q30)], fmt="0.0000", size=8, legend=True)
        return 2.3, "A 30 percent attacker still has %.0f percent after six blocks." % (100 * q30[6])
    if ex == "ex13":
        eras = val(ex, 0)
        chart(s, x, y, w, 2.25, "bar", ["2009", "2012", "2016", "2020", "2024", "2028"], [("reward", eras)], fmt="0.####", pointcolors=[ORANGE] * 5 + [MUTED])
        return 2.25, "The reward halved in 2012, 2016, 2020 and 2024; 2028 is the next halving due."
    if ex == "ex14":
        st, neg = val(ex, 0); total = val(ex, 1); big = val(ex, 2)
        table(s, x, y, w, [1.2, 1.9], [["Step", "Satoshis"], ["Each output", fmt(big)], ["True sum", fmt(total)], ["Stored in 64 bits", fmt(st)]], rowh=0.42, size=9.5, hot={2})
        return 4 * 0.42, "The stored sum is negative, so it sits below any input and the old check passed."


# ------------------------------------------------------------------------------------------------------------------------------------------------
# slide builders: each draws one slide and returns its entry of the plan (kind, title, items, take, bg) for the owner checks that read deck_plan_v3_0_0.json
# ------------------------------------------------------------------------------------------------------------------------------------------------
ANALOGIES = []
relp = lambda f: os.path.relpath(asset(f), HERE)


def s_title(d, k, n):
    s = d.new("Chapter 1 asked what Bitcoin is. Chapter 2 follows one payment, Alice paying Bob's Store, from the invoice to the blockchain. Every number in this deck was computed with the chapter's own Python library.")
    for i in range(3):
        text(s, 0.6 + i * 0.95, 0.75, 0.75, 0.75, ["₿"] if i == 2 else [""], size=26, bold=True, color=WHITE if i == 2 else INK, align="c", anchor="m",
             shape=MSO_SHAPE.OVAL, fill=ORANGE if i == 2 else None, line=ORANGE)
        if i < 2: arrow(s, 1.35 + i * 0.95, 1.12, 1.55 + i * 0.95, 1.12, color=ORANGE)
    text(s, 0.6, 1.9, 5.0, 1.2, ["Chapter 2: How Bitcoin Works"], size=30, font=SERIF, anchor="m")
    text(s, 0.6, 3.2, 5.0, 0.7, ["One payment, followed from the shop's invoice to the blockchain"], size=15, italic=True, color=MUTED)
    text(s, 0.6, 4.2, 8.8, 0.3, ["Python %s; every result is computed by the chapter library; no Bitcoin Core node was run." % PY], size=11, color=MUTED)
    text(s, 0.6, 4.62, 8.0, 0.45, ["SEN0401 Special Topics in Software Engineering: Block Chain · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University"], size=11, color=MUTED)
    picture(s, asset("shot_bitcoinqt_0_5_2.png"), 5.85, 0.7, 3.65, 2.23, "Screen of the Bitcoin-Qt wallet, version 0.5.2, with balance and recent transactions", mode="fit")
    text(s, 5.85, 3.0, 3.65, 0.5, ["Bitcoin-Qt 0.5.2, a wallet of 2012 - the Bitcoin developers, MIT licence, Wikimedia Commons"], size=9, color=MUTED)
    number(s, k, n)
    return dict(kind="title", title="Chapter 2: How Bitcoin Works", items=[{"t": "img", "path": relp("shot_bitcoinqt_0_5_2.png")}, {"t": "foot"}], bg="light")


def s_route(d, k, n, ranges):
    s = d.new("The route has six parts that follow one payment from the invoice to the spending. Three true stories and fourteen code examples are spread across them, and every example has a picture of its result.")
    frame(d, s, k, n, "Today's route", "Six parts around one payment; every range is a slide you can jump to", "Six parts, three true stories, fourteen examples")
    names = ["1. Questions and the chapter map"] + ["%d. %s" % (i + 2, PARTS[i][0]) for i in range(6)] + ["8. Summary, resources, closing"]
    for i, a in enumerate(names):
        cx, cy = 0.5 + (i % 3) * 2.15, 1.4 + (i // 3) * 1.12
        text(s, cx, cy, 2.0, 1.0, [[(a, {"bold": True, "font": SERIF, "size": 11.5})], [("(slides %d-%d)" % ranges[i], {"size": 10.5, "color": MUTED})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD,
             line=LINE, pad=0.1, anchor="m", radius=0.1)
    stats = [(str(n), "slides, numbered bottom-right"), ("3", "true stories, each told by 5N1K"), ("14", "code examples, each with a picture of its result")]
    for i, (a, b) in enumerate(stats):
        y = 1.4 + i * 1.12
        rect(s, 6.95, y, 2.55, 1.0, CARD, line=LINE)
        text(s, 7.1, y + 0.05, 2.25, 0.42, [a], size=22, font=SERIF, color=ORANGE, anchor="m")
        text(s, 7.1, y + 0.5, 2.25, 0.45, [b], size=10.5, color=MUTED)
    return dict(kind="content", title="Today's route", items=[{"t": "boxes"}, {"t": "stat"}], take="Six parts, three true stories, fourteen examples")


def s_questions(d, k, n):
    s = d.new("The six questions are the chapter's own, rewritten so that each has an answer on a slide. We return to them in the summary. A reader who can answer all six has understood the chapter.")
    frame(d, s, k, n, "The questions this chapter answers", "Each has an answer on a slide; we return to them in the summary")
    qs = ["What do Alice's payment and Bob's invoice contain?", "Why must inputs equal outputs plus a fee, and where does change come from?",
          "How does a wallet choose coins and build the outputs?", "How does a payment travel to a miner and into a block?",
          "What makes a payment harder to reverse with each confirmation?", "Which rules does every node check, and what if a block breaks one?"]
    for i, q in enumerate(qs):
        y = 1.4 + i * 0.58
        text(s, 0.5, y, 0.44, 0.44, [str(i + 1)], size=14, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.OVAL, fill=TEAL)
        text(s, 1.12, y, 8.38, 0.44, [q], size=13, anchor="m")
    return dict(kind="content", title="The questions this chapter answers", items=[{"t": "numlist", "items": qs}])


def s_map(d, k, n):
    s = d.new("Six steps carry one payment. Alice reads an invoice, a transaction is formed, coins are chosen, the wallet builds and signs it, a miner puts it in a block, and Bob can spend it. The parts of this deck follow the same path.")
    frame(d, s, k, n, "The chapter in one picture", "One payment, six steps; the parts of the deck follow them", "Six steps, one payment: from invoice to a spendable coin")
    steps = [("1 Invoice", "Alice learns what to pay."), ("2 Transaction", "Inputs, outputs and a fee."), ("3 Coins", "Pick them; change returns."),
             ("4 Build", "Price and sign the payment."), ("5 Block", "Miners add it; confirmations grow."), ("6 Spend", "Every node checks the rules.")]
    w, gap = 1.38, 0.144
    for i, (a, b) in enumerate(steps):
        x = 0.5 + i * (w + gap)
        text(s, x, 1.7, w, 0.5, [a], size=12, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL if i < 5 else ORANGE, radius=0.2)
        text(s, x, 2.4, w, 0.9, [b], size=11)
        if i < 5: arrow(s, x + w + 0.01, 1.95, x + w + gap - 0.01, 1.95, color=ORANGE)
    text(s, 0.5, 3.6, 9.0, 0.9, ["Fourteen code examples run along this path. Each prints its result under the listing and shows it as a picture beside it."], size=14, color=MUTED, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
         fill=CARD, line=LINE, pad=0.15, anchor="m", radius=0.1)
    return dict(kind="content", title="The chapter in one picture", items=[{"t": "flow", "steps": [a for a, _ in steps]}, {"t": "text"}], take="Six steps, one payment: from invoice to a spendable coin")


def s_divider(d, k, n, title, idx):
    sub, notes, items = DIV[title]
    s = d.new(notes)
    text(s, 0.6, 0.45, 8.8, 0.8, [title], size=28 if len(title) <= 34 else 26, font=SERIF, anchor="m")
    text(s, 0.6, 1.28, 8.8, 0.4, [sub], size=15, italic=True, color=MUTED, anchor="m")
    m = len(items); cw = (8.8 - (m - 1) * 0.2) / m
    for i, (pill, mean, ana) in enumerate(items):
        x = 0.6 + i * (cw + 0.2)
        if len(pill.split()) > 4: raise SystemExit("REFUSED: divider pill %r has over 4 words (D10)" % pill)
        text(s, x, 1.95, cw, 0.42, [pill], size=12, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL, pad=0.06, radius=0.3)
        text(s, x, 2.48, cw, 0.8, [mean], size=11.5)
        text(s, x, 3.34, cw, 0.62, [ana], size=11.5, italic=True, color=ORANGE)
        ANALOGIES.append({"concept": pill, "analogy": ana, "slide": k})
    gf = table(s, 0.6, 4.3, 8.8, [8.8 / 6.0] * 6, [[p[1] for p in PARTS]], size=10, rowh=0.4, head=False, align=["c"] * 6)
    for j in range(6):
        c = gf.table.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = rgb(ORANGE if j == idx else CARD)
        for r in c.text_frame.paragraphs[0].runs: r.font.color.rgb = rgb(WHITE if j == idx else MUTED); r.font.bold = (j == idx)
    number(s, k, n)
    return dict(kind="section", title=title, sub=sub, items=[{"t": "groups", "items": [{"pill": a, "meaning": b, "analogy": c} for a, b, c in items]}, {"t": "striptable"}], bg="light")


def s_overview(d, k, n):
    s = d.new("Four roles share the work. Users hold wallets that sign payments, nodes check the rules and pass transactions on, and miners bundle waiting transactions into blocks that everyone copies. Nobody owns the record.")
    frame(d, s, k, n, "Four roles, one network", "Who does what when Alice pays Bob", "No single owner: wallets sign, nodes check, miners bundle")
    picture(s, asset("c2s04_overview.png"), 0.5, 1.4, 4.6, 2.79, "Diagram of users, wallets, nodes and miners passing payments and blocks", mode="fit")
    text(s, 0.5, 4.3, 4.6, 0.4, ["Users, wallets, nodes and miners - from the course's 2025 deck"], size=9, color=MUTED)
    roles = [("Users and wallets", "A wallet holds keys and signs payments for its user."), ("Nodes", "Check every rule and pass valid transactions on."),
             ("Miners", "Bundle waiting transactions into the next block."), ("The blockchain", "The shared record of blocks that every node keeps.")]
    for i, (a, b) in enumerate(roles):
        text(s, 5.4, 1.4 + i * 0.86, 4.1, 0.76, [[(a, {"bold": True, "font": SERIF, "size": 12.5})], [(b, {"size": 11})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE,
             pad=0.12, anchor="m", radius=0.1)
    return dict(kind="content", title="Four roles, one network", items=[{"t": "img", "path": relp("c2s04_overview.png")}, {"t": "cards"}], take="No single owner: wallets sign, nodes check, miners bundle")


def s_story(d, k, n, sid, a):
    st = STORY[sid]; s = d.new(a["notes"])
    frame(d, s, k, n, a["title"], a["sub"])
    if a["pic_w"] == 3.0: picture(s, asset(st["photo"]), 0.5, 1.35, 3.0, 2.45, a["alt"], focus=a.get("focus", 0.3))
    else: picture(s, asset(st["photo"]), 0.5 + (3.0 - a["pic_w"]) / 2, 1.35, a["pic_w"], 2.45, a["alt"], mode="fit")
    credit = "Picture: " + st["credit"] + a["credit_tail"]
    text(s, 0.5, 3.88, 3.0, 0.62, [credit], size=8.5, color=MUTED)
    for i, (lab, body) in enumerate(a["n5"]):
        parts = [(lab + " ", {"bold": True, "color": ORANGE, "size": 10.5})] + ([(body, {"size": 10.5})] if isinstance(body, str) else [(b, dict(o, size=10.5)) for b, o in body])
        text(s, 3.75, 1.33 + i * 0.52, 5.75, 0.48, [parts], size=10.5)
    host = re.sub(r"^https?://(www\.)?", "", st["link"]).split("/")[0]
    text(s, 3.75, 4.5, 5.75, 0.3, [[("READ ", {"bold": True, "color": ORANGE, "size": 10.5}), (st["linkLabel"], {"size": 10.5, "color": TEAL, "link": st["link"]}), (" - " + host, {"size": 10.5, "color": MUTED})]], size=10.5)
    return dict(kind="content", title=a["title"], sub=a["sub"], items=[{"t": "img", "path": relp(st["photo"]), "cap": credit}, {"t": "beats", "items": ["%s %s" % (l, b if isinstance(b, str) else "".join(x for x, _ in b)) for l, b in a["n5"]]},
                {"t": "factrow", "who": st["who"], "where": st["where"], "when": st["when"], "link": st["link"], "linkText": st["linkLabel"]}], take=a["take"])


def s_code(d, k, n, ex):
    e = EX[ex]; title, sub, _expl, take, notes = TEXT[ex]
    s = d.new(notes); frame(d, s, k, n, title, sub, take)
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
    if y > 4.95: raise SystemExit("REFUSED %s: the listings need %.2f in (limit 4.95)" % (ex, y))
    text(s, 0.5, y - 0.04, 5.7, 0.2, ["run under Python %s - T is the chapter library of the page (%s)" % (PY, X.LIB)], size=9, color=MUTED)
    items = [{"t": "codeblocks", "ex": ex}]
    if ex == "ex01":
        picture(s, asset("c2s07_fractions.jpg"), 0.5, 3.75, 1.8, 1.19, "Table of satoshis and bitcoin from one satoshi to one bitcoin", mode="fit")
        text(s, 2.45, 3.95, 3.75, 0.5, ["The satoshi table of the course's 2025 deck: from one satoshi to one bitcoin"], size=9, color=MUTED)
        items.append({"t": "img", "path": relp("c2s07_fractions.jpg")})
    text(s, 6.4, 1.4, 3.1, 0.4, [RESULT_CAP[ex]], size=11, bold=True, color=TEAL)
    used, reading = visual(s, ex, 6.4, 1.85, 3.1)
    text(s, 6.4, 1.85 + used + 0.12, 3.1, 0.7, [reading], size=11)
    items.append({"t": EX[ex]["picture"] == "native chart" and "chart" or "table", "ex": ex})
    return dict(kind="content", title=title, sub=sub, items=items, take=take)


def s_cards_fig(d, k, n):
    s = d.new("A transaction is double-entry bookkeeping: the inputs on the left, the outputs on the right, and the difference is the fee. An input spends an earlier output; an output locks an amount to a new owner.")
    frame(d, s, k, n, "Inputs and outputs", "The ledger of figure 2-2, and the two words it is made of", "An input spends an earlier output; an output creates a new one")
    picture(s, asset("mbc3_0202.png"), 0.5, 1.4, 4.4, 3.05, "Figure 2-2: a transaction as double-entry bookkeeping", mode="fit")
    text(s, 0.5, 4.5, 4.4, 0.4, ["Figure 2-2, Mastering Bitcoin 3rd edition, Antonopoulos and Harding, CC BY-SA 4.0"], size=8.5, color=MUTED)
    for i, (lab, mean, ana) in enumerate(CARDS):
        y = 1.4 + i * 1.7
        rect(s, 5.15, y, 4.35, 1.55, CARD, line=LINE, radius=0.06); rect(s, 5.2, y + 0.12, 0.07, 1.31, ORANGE, rounded=False)
        text(s, 5.42, y + 0.1, 3.95, 0.85, [[(lab, {"bold": True, "font": SERIF, "size": 14})], [(mean, {"size": 11.5})]], size=11.5)
        text(s, 5.42, y + 1.0, 3.95, 0.45, [ana], size=11.5, italic=True, color=ORANGE)
        ANALOGIES.append({"concept": lab, "analogy": ana, "slide": k})
    return dict(kind="content", title="Inputs and outputs", items=[{"t": "img", "path": relp("mbc3_0202.png")}, {"t": "cards"}], take="An input spends an earlier output; an output creates a new one")


def s_chain_fig(d, k, n):
    s = d.new("Figure 2-3 shows three linked transactions. Each input names an earlier output, so the coins can be traced back; an output that nobody has spent yet is a coin that still exists.")
    frame(d, s, k, n, "A chain of transactions", "Outputs become inputs, and the chain leads back in time", "Follow the arrows backwards to find where a coin came from")
    picture(s, asset("mbc3_0203.png"), 1.1, 1.35, 7.8, 2.57, "Figure 2-3: Tx1, Tx2 and Tx3 linked by arrows from inputs to outputs", mode="fit")
    text(s, 1.1, 3.95, 7.8, 0.22, ["Figure 2-3, Mastering Bitcoin 3rd edition, Antonopoulos and Harding, CC BY-SA 4.0"], size=8.5, color=MUTED)
    for i, t in enumerate(["Each input names an earlier output, such as Tx1:0.", "A spent output can never be spent a second time.", "Outputs nobody has spent are the coins in a wallet."]):
        text(s, 0.5 + i * 3.1, 4.3, 2.9, 0.62, [t], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.1, anchor="m", radius=0.1)
    return dict(kind="content", title="A chain of transactions", items=[{"t": "img", "path": relp("mbc3_0203.png")}, {"t": "cards"}], take="Follow the arrows backwards to find where a coin came from")


def s_flow(d, k, n):
    s = d.new("The wallet builds Alice's transaction in five steps. It finds the inputs, writes the outputs, leaves the fee, signs every input and broadcasts the result to a node, which passes it on.")
    frame(d, s, k, n, "From coins to a signed transaction", "The five steps a wallet takes for Alice's payment", "The wallet only decides inputs, outputs and fee; the rules do the rest")
    steps = [("1 Inputs", "Find unspent outputs that cover payment and fee.", "Tx1:0 = 100,000"), ("2 Outputs", "One output for Bob's Store, one for the change.", "75,000 and 20,000"),
             ("3 Fee", "Leave the difference for the miner.", "100,000 - 95,000 = 5,000"), ("4 Sign", "Prove ownership of every input.", "one signature per input"),
             ("5 Send", "Pass the transaction to a node.", "the node relays it on")]
    w, gap, x0 = 1.64, 0.25, 0.4
    for i, (a, b, c) in enumerate(steps):
        x = x0 + i * (w + gap)
        text(s, x, 1.5, w, 0.5, [a], size=13, font=SERIF, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=TEAL if i != 4 else ORANGE, radius=0.2)
        text(s, x, 2.15, w, 1.0, [b], size=11.5)
        text(s, x, 3.3, w, 0.62, [c], size=10.5, color=ORANGE, bold=True, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE, pad=0.08, anchor="m", align="c", radius=0.15)
        if i < 4: arrow(s, x + w + 0.02, 1.75, x + w + gap - 0.02, 1.75, color=ORANGE)
    text(s, 0.5, 4.2, 9.0, 0.6, ["Steps 1 to 3 are the arithmetic of the ledger; step 4 is the signature, treated in chapter 8; step 5 hands the transaction to the network."], size=12, color=MUTED)
    return dict(kind="content", title="From coins to a signed transaction", items=[{"t": "flow", "steps": [a for a, _, _ in steps]}, {"t": "text"}], take="The wallet only decides inputs, outputs and fee; the rules do the rest")


def s_block_fig(d, k, n):
    s = d.new("Alice's transaction sits in block 277,316. A block's height counts from the genesis block, and its depth counts the blocks on top. Each block on top is one more confirmation, and a block explorer shows all of it.")
    frame(d, s, k, n, "Height, depth and confirmations", "Where Alice's transaction sits in the chain", "More blocks on top means a payment that is harder to reverse")
    picture(s, asset("mbc3_0207.png"), 0.5, 1.4, 2.62, 3.2, "Figure 2-7: Alice's transaction in block 277316 with blocks on top", mode="fit")
    text(s, 0.5, 4.65, 2.8, 0.34, ["Figure 2-7, Mastering Bitcoin 3rd edition, CC BY-SA 4.0"], size=8, color=MUTED)
    items = [("Block height", "The position of a block, counted from the genesis block. Alice's block is 277,316."), ("Block depth", "How many blocks lie on top of a block."),
             ("Confirmation", "Alice's block is the first confirmation; each block on top adds one more."), ("Block explorer", "Paste a transaction id into an explorer to see its block, depth and fee.")]
    for i, (a, b) in enumerate(items):
        text(s, 3.5, 1.4 + i * 0.86, 6.0, 0.76, [[(a, {"bold": True, "font": SERIF, "size": 12.5})], [(b, {"size": 11})]], size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=CARD, line=LINE,
             pad=0.12, anchor="m", radius=0.1)
    return dict(kind="content", title="Height, depth and confirmations", items=[{"t": "img", "path": relp("mbc3_0207.png")}, {"t": "cards"}], take="More blocks on top means a payment that is harder to reverse")


def s_summary(d, k, n):
    s = d.new("Each row answers one of the six opening questions in a line. If you can say each answer in your own words, using the everyday pictures of this chapter, you have the chapter.")
    frame(d, s, k, n, "Summary: the six answers", "The questions of slide 3, answered", "Inputs, outputs, fee, mining, confirmations, rules")
    rows = [["Question", "Answer in one line"],
            ["1 What does a payment contain?", "Inputs that spend earlier outputs, outputs for Bob and the change, a fee."],
            ["2 Why inputs = outputs + fee?", "The ledger must balance; the rest, 5,000 satoshis, is the miner's fee."],
            ["3 How is it built?", "Pick coins, write the outputs, leave the fee, sign."],
            ["4 How does it reach a block?", "A node relays it; a miner finds a valid nonce and adds a block."],
            ["5 Why confirmations?", "A 10 percent attacker's chance falls from 20.5 to 0.02 percent."],
            ["6 Which rules?", "Consensus rules, checked by every node; block 74,638 broke one."]]
    table(s, 0.5, 1.4, 9.0, [3.1, 5.9], rows, size=11, rowh=0.45)
    return dict(kind="content", title="Summary: the six answers", items=[{"t": "table"}], take="Inputs, outputs, fee, mining, confirmations, rules")


RES = [("Read", "Mastering Bitcoin, chapter 2 (source text)", "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch02_overview.adoc", "The chapter this deck follows."),
       ("Read", "Developer guide: transactions", "https://developer.bitcoin.org/devguide/transactions.html", "Inputs, outputs and fees in detail."),
       ("Standards and papers", "Bitcoin white paper", "https://bitcoin.org/bitcoin.pdf", "Nine pages; section 11 holds the catch-up table."),
       ("Standards and papers", "BIP 21: payment links", "https://bips.dev/21/", "The standard behind Bob's invoice link."),
       ("Standards and papers", "Bitcoin Core releases", "https://bitcoincore.org/en/releases/", "The software that checks every rule."),
       ("Try", "mempool.space block explorer", "https://mempool.space/", "Look up any transaction, block or fee."),
       ("Try", "Anders Brownworth's blockchain demo", "https://andersbrownworth.com/blockchain/hash", "Hash, block and mine in the browser."),
       ("Watch", "MIT 15.S12 Blockchain and Money", "https://ocw.mit.edu/courses/15-s12-blockchain-and-money-fall-2018/", "A full university course, free."),
       ("Community", "Bitcoin Optech topics", "https://bitcoinops.org/en/topics/", "Short explainers on how the technology works."),
       ("Community", "Bitcoin Stack Exchange", "https://bitcoin.stackexchange.com/", "Ask a question, read the answers.")]


def s_resources(d, k, n):
    s = d.new("These links are all open and free. Start with the chapter source and the white paper, try the block explorer on a real payment, and use the MIT course for the wider story of blockchain and money.")
    frame(d, s, k, n, "Resources: read, try, watch, ask", "Every link was opened on 25 October 2026; free to use", "Look up a real transaction in a block explorer today")
    for i, (kind, lab, url, why) in enumerate(RES):
        col, row = i // 5, i % 5
        x, y = 0.5 + col * 4.6, 1.4 + row * 0.72
        text(s, x, y, 4.4, 0.64, [[(kind + "  ", {"bold": True, "color": ORANGE, "size": 9}), (lab, {"size": 11.5, "bold": True, "color": TEAL, "link": url})], [(why, {"size": 10, "color": MUTED})]], size=11)
    groups = []
    for head in ("Read", "Standards and papers", "Try", "Watch", "Community"):
        groups.append({"head": head, "rows": [[lab, url, why] for kd, lab, url, why in RES if kd == head]})
    return dict(kind="content", title="Resources: read, try, watch, ask", items=[{"t": "links", "groups": groups}], take="Look up a real transaction in a block explorer today")


def s_closing(d, k, n):
    s = d.new("That is the whole path of one payment. Chapter 3 opens the software that checks every rule, Bitcoin Core, and shows how to run it yourself. Bring your questions.")
    rect(s, 0.5, 0.9, 9.0, 3.7, CODE, radius=0.04)
    text(s, 0.9, 1.3, 8.2, 1.1, ["Questions?"], size=44, font=SERIF, color=WHITE, anchor="m")
    text(s, 0.9, 2.5, 8.2, 0.5, ["One payment, from the invoice to the blockchain"], size=18, italic=True, color=C_NUM)
    text(s, 0.9, 3.3, 8.2, 0.45, ["Next: chapter 3, Bitcoin Core, the reference implementation"], size=15, font=SERIF, color=CODE_OR)
    text(s, 0.9, 4.0, 8.2, 0.4, ["Python %s; every result in this deck was computed by the chapter library, not typed" % PY], size=11, color=CODE_TXT)
    number(s, k, n)
    return dict(kind="closing", title="Questions?", items=[{"t": "bullets", "items": ["Next: chapter 3, Bitcoin Core, the reference implementation"]}], bg="dark")


def when_runs(iso, long):
    return [(iso, {}), (" (%s)" % long, {})]


STORIES = {
 "FirstFaucet": dict(title="Five free bitcoins for every visitor", sub="11 June 2010 · how a first coin reached its owner", take="Before exchanges, distribution itself had to be invented", pic_w=3.0, focus=0.2,
    alt="Gavin Andresen speaking at Web Summit 2014", credit_tail=", Wikimedia Commons",
    n5=[("WHO", "Gavin Andresen, a software developer who later led the Bitcoin software after Satoshi Nakamoto left."), ("WHAT", "A website that gave five bitcoins to every visitor who solved a CAPTCHA."),
        ("WHEN", when_runs("2010-06-11", "11 June 2010")), ("WHERE", "A website announced on the bitcointalk forum; Andresen worked from Massachusetts."),
        ("WHY", "Almost nowhere sold bitcoin in 2010, so he gave coins away to seed the first users."), ("HOW", "He stocked the site with 1,100 of his own bitcoins and paid five to each request.")],
    notes="Alice needs bitcoin before she can pay Bob. In 2010 there was almost nowhere to buy it, so Gavin Andresen gave five coins to every visitor of his website. Thousands of people got their first bitcoin this way."),
 "WhitepaperMath": dict(title="Nine pages, one table of probabilities", sub="31 October 2008 · section 11 of the white paper", take="A confirmation is a probability statement, and you can compute it", pic_w=3.0, focus=0.3,
    alt="Bronze bust of Satoshi Nakamoto in Budapest", credit_tail=", Wikimedia Commons",
    n5=[("WHO", "Satoshi Nakamoto, the pseudonymous author, writing to a cryptography mailing list."), ("WHAT", "A nine-page paper whose section 11 tabulates an attacker's chance of catching up."),
        ("WHEN", when_runs("2008-10-31", "31 October 2008")), ("WHERE", "The metzdowd.com cryptography mailing list; the PDF now sits on bitcoin.org."),
        ("WHY", "To show with numbers that waiting for confirmations makes a double spend unlikely."), ("HOW", "A random walk models the race of an honest chain against a secret one; the next slide reruns it.")],
    notes="The white paper reached its readers on 31 October 2008. Its section 11 does something rare for a systems paper: it computes the attacker's odds. The next slide reruns that computation."),
 "ValueOverflow": dict(title="The day someone printed 184 billion bitcoin", sub="15 August 2010 · block 74,638", take="Validation by every node is the immune system - and it worked", pic_w=2.45,
    alt="The Bitcoin logo, a stand-in picture", credit_tail=", Wikimedia Commons - a stand-in, since no free picture of the event exists",
    n5=[("WHO", "An unknown attacker; Jeff Garzik, who spotted the block; Satoshi Nakamoto, who patched the software."), ("WHAT", "A block paid out about 184 billion bitcoin, thousands of times the 21 million limit."),
        ("WHEN", when_runs("2010-08-15", "15 August 2010")), ("WHERE", "Block 74,638 of the Bitcoin chain, discussed live on the bitcointalk forum."),
        ("WHY", "Two outputs were so large that their sum overflowed and passed the checks; no rule limited the amounts."),
        ("HOW", "Garzik flagged the block within the hour; Satoshi shipped version 0.3.10 about five hours later and the honest chain overtook it.")],
    notes="On 15 August 2010 block 74,638 created about 184 billion bitcoin out of an overflow. Every node checks every rule, and this one rule was missing. Within hours the software was fixed and the honest chain, without the forged coins, won."),
}

# ------------------------------------------------------------------------------------------------------------------------------------------------
# the order of the deck
# ------------------------------------------------------------------------------------------------------------------------------------------------
SEQ = [("title",), ("route",), ("questions",), ("map",),
       ("div", "Buying from an Online Store", 0), ("overview",), ("story", "FirstFaucet"), ("code", "ex01"), ("code", "ex02"),
       ("div", "Bitcoin Transactions", 1), ("cardsfig",), ("code", "ex03"), ("code", "ex04"), ("code", "ex05"), ("chainfig",), ("code", "ex06"),
       ("div", "Coin Selection", 2), ("code", "ex07"), ("code", "ex08"),
       ("div", "Constructing a Transaction", 3), ("flow",), ("code", "ex09"),
       ("div", "Adding the Transaction to the Blockchain", 4), ("blockfig",), ("code", "ex10"), ("code", "ex11"), ("story", "WhitepaperMath"), ("code", "ex12"),
       ("div", "Spending the Transaction", 5), ("code", "ex13"), ("story", "ValueOverflow"), ("code", "ex14"),
       ("summary",), ("resources",), ("closing",)]


def main():
    n = len(SEQ)
    pos = [i + 1 for i, q in enumerate(SEQ) if q[0] == "div"]; summ = [j + 1 for j, q in enumerate(SEQ) if q[0] == "summary"][0]
    ranges = [(3, pos[0] - 1)] + [(pos[i], (pos[i + 1] - 1) if i + 1 < len(pos) else summ - 1) for i in range(6)] + [(summ, n)]
    d = Deck(); code_slides = {}; plan = []
    for k, q in enumerate(SEQ, 1):
        kind = q[0]
        if kind == "title": e = s_title(d, k, n)
        elif kind == "route": e = s_route(d, k, n, ranges)
        elif kind == "questions": e = s_questions(d, k, n)
        elif kind == "map": e = s_map(d, k, n)
        elif kind == "div": e = s_divider(d, k, n, q[1], q[2])
        elif kind == "overview": e = s_overview(d, k, n)
        elif kind == "story": e = s_story(d, k, n, q[1], STORIES[q[1]])
        elif kind == "code": e = s_code(d, k, n, q[1]); code_slides[q[1]] = k
        elif kind == "cardsfig": e = s_cards_fig(d, k, n)
        elif kind == "chainfig": e = s_chain_fig(d, k, n)
        elif kind == "flow": e = s_flow(d, k, n)
        elif kind == "blockfig": e = s_block_fig(d, k, n)
        elif kind == "summary": e = s_summary(d, k, n)
        elif kind == "resources": e = s_resources(d, k, n)
        elif kind == "closing": e = s_closing(d, k, n)
        e["n"] = k; e["notes"] = d.last_notes; e.setdefault("bg", "light"); e.setdefault("sub", ""); plan.append(e)
    deck_path = os.path.join(ROOT, "03-materials", "ch02", DECK_NAME)
    d.prs.save(deck_path)
    # the chapter-code manifest: the examples in the order of the deck's code slides, drawn from the same list
    lib_path = os.path.join(TOOL, "sen0401_ch02_tx_lib_v1_0_0.py")
    setup = "# setup: the chapter library of the page (T = the chapter 2 library); the page runs this before every example\n" + X.PRELUDE.rstrip("\n")
    exs = []
    for o, q in enumerate([q for q in SEQ if q[0] == "code"], 1):
        e = EX[q[1]]
        exs.append({"order": o, "id": e["id"], "name": e["name"], "slide": code_slides[e["id"]], "branch": e["branch"], "library": X.LIB, "needs": ["setup"],
                    "code": "\n".join(e["lines"]), "show": [{"expression": x, "expected": r} for x, r in OUT[e["id"]]], "result_picture": e["picture"]})
    man = {"manifest": "chapter_code_ch02_v1_0_0", "chapter": 2, "deck": DECK_NAME, "deck_version": "3.0.0", "python_of_expected_values": PY,
           "rule": "order = the order of the code slides of the deck; the page tab lists the examples by name in this order; each runs as setup + listing, with the chapter library defined in the page; the manifest equals the deck's code boxes",
           "library": {"module": X.LIB, "file": "08-tooling/sen0401_ch02_tx_lib_v1_0_0.py", "sha256": hashlib.sha256(open(lib_path, "rb").read()).hexdigest(),
                       "import": "import sen0401_ch02_tx_lib_v1_0_0 as T", "requires": "Python standard library only (hashlib, math, struct, urllib.parse)"},
           "setup": {"code": setup, "data": {}}, "examples": exs}
    json.dump(man, open(os.path.join(ROOT, "03-materials", "ch02", "page", "chapter_code_ch02_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
    standin = [str(e["n"]) for e in plan if any("stand-in" in (it.get("cap") or "") for it in e["items"])]
    meta = {"title": "Chapter 2: How Bitcoin Works", "sub": "SEN0401, third-edition deck 3.0.0", "version": "3.0.0", "python": PY, "total": n,
            "redesign": "2026-10-25, task TK_Ch02_Deck_Build_R24: content, analogies, code with explanation beside it and the result as a picture, dividers with meanings, deck standard D1-D12",
            "notes": "short reader's prose: 2-4 sentences, at most 60 words", "analogies": ANALOGIES,
            "honesty": {"title": ["no Bitcoin Core node"], "no_node": True, "notExecuted": [], "recorded": [], "standin": {s_: ["stand-in"] for s_ in standin}, "vectors": []}}
    json.dump({"meta": meta, "slides": plan}, open(os.path.join(HERE, "deck_plan_v3_0_0.json"), "w"), indent=1, ensure_ascii=False)
    print("wrote %s (%d slides, %d code slides) and chapter_code_ch02_v1_0_0.json (%d examples)" % (DECK_NAME, n, len(code_slides), len(exs)))


if __name__ == "__main__":
    main()
