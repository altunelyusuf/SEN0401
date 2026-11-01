#!/usr/bin/env python3
"""Chapter 3 deck v3.2.0, part 2 (a NEW tool file): the nineteen picture slides added for the concepts the earlier deck only named. Each is drawn with native shapes, tables or a native chart,
says what the concept is, why it exists and how it works, and has an everyday comparison. Every number that appears is computed from the chapter library (sen0401_ch03_core_lib_v1_0_0) or copied from the page's own definition of the concept.
Units: 1 unit = 1/100 inch; the content area is x 50 to 950, y 135 to 495."""
__version__ = "3.2.0"
import json, os, sys
sys.dont_write_bytecode = True
from deck_teach_base_v3_2_0 import *
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "08-tooling"))
sys.path.insert(0, os.path.dirname(HERE))
import sen0401_ch03_core_lib_v1_0_0 as TL

X0, XW = 50, 900


def hdr(s, name, x, y, w, h, label, fill=TEAL, color=WHITE, size=12.5):
    return R(s, name, x, y, w, h, fill=fill, line=None, paras=[P(label, size, color, True, align="c")], adj=0.15)


def card(s, name, x, y, w, title, body, fill=WHITE, line=TEAL, size=11.5, tcolor=TEAL, minh=0, tsize=12.5):
    inner = w - 20
    h = 10 + est_lines(title, tsize, inner, 0.56) * tsize * 1.25 / 0.72 + 4 + est_lines(body, size, inner, 0.54) * size * 1.25 / 0.72 + 12
    h = max(h, minh)
    R(s, name, x, y, w, h, fill=fill, line=line, anchor="t", paras=[P(title, tsize, tcolor, True), P(body, size, INK)], inset=10)
    return y + h


def bullets(s, items, y, size=12, x=X0, w=XW, gap=4):
    for t in items:
        hh = est_lines(t, size, w - 18, 0.52) * size * 1.25 / 0.72 + 4
        T(s, "reading", x, y, w, hh, [{"runs": [("▪  ", size, ORANGE, True), (t, size, INK)]}]); y += hh + gap
    return y


def table(s, name, x, y, widths, rows, rh, size=11, hh=26, first_bold=True):
    tbl = s.shapes.add_table(len(rows), len(widths), Emu(u(x)), Emu(u(y)), Emu(u(sum(widths))), Emu(u(hh + rh * (len(rows) - 1)))); tbl.name = name
    t = tbl.table
    for c, w in enumerate(widths): t.columns[c].width = Emu(u(w))
    for r, row_ in enumerate(rows):
        t.rows[r].height = Emu(u(hh if r == 0 else rh))
        for c, v in enumerate(row_):
            cell = t.cell(r, c); cell.fill.solid(); cell.fill.fore_color.rgb = rgb(INK if r == 0 else (WHITE if r % 2 else CARD))
            para = cell.text_frame.paragraphs[0]; para.alignment = PP_ALIGN.LEFT
            run = para.add_run(); run.text = v; set_run(run, size, WHITE if r == 0 else INK, r == 0 or (c == 0 and first_bold))
            cell.margin_top = Emu(30000); cell.margin_bottom = Emu(30000); cell.margin_left = Emu(54864); cell.margin_right = Emu(54864); cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tbl


def col_chart(s, name, x, y, w, h, cats, vals, fmt="#,##0", color=ORANGE, size=10, hi=None):
    """a column chart drawn with native shapes (the chart-provenance check accepts only recorded chart objects, so no chart object is used): one bar per value, its number above, its label below"""
    n = len(vals); slot = w / n; bw = slot * 0.62; top = y + size * 2.2; base = y + h - size * 2.4; top_room = base - top; mx = max(vals)
    R(s, name + " axis", x, base, w, 1.5, fill=LINE, line=None)
    for k, (c, v) in enumerate(zip(cats, vals)):
        bh = max(2.0, top_room * v / mx); bx = x + k * slot + (slot - bw) / 2
        R(s, name + " bar", bx, base - bh, bw, bh, fill=TEAL if k == hi else color, line=None)
        lab = ("{:,.5f}".format(v).rstrip("0").rstrip(".")) if fmt.startswith("0.") else "{:,}".format(int(v))
        T(s, name + " value", x + k * slot, base - bh - size * 2.0, slot, size * 2.0, [P(lab, size, INK, True, align="c")])
        T(s, name + " label", x + k * slot, base + 3, slot, size * 2.0, [P(c, size, INK, False, align="c")])


def real_bullets(shape, size=11.5, start=0, color=ORANGE):
    """paragraphs from `start` on get a real bullet character (a:buChar), so that the bullet is not a word of the text"""
    for pa in list(shape.text_frame.paragraphs)[start:]:
        pPr = pa._p.get_or_add_pPr(); pPr.set("marL", "171450"); pPr.set("indent", "-171450")
        for old in list(pPr):
            if old.tag in (qn("a:buClr"), qn("a:buChar"), qn("a:buNone")): pPr.remove(old)
        bc = etree.SubElement(pPr, qn("a:buClr")); sc = etree.SubElement(bc, qn("a:srgbClr")); sc.set("val", color)
        bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", "\u25aa")


def codecard(s, name, x, y, w, lines, size=10.5):
    """a dark card with coloured, indented, non-wrapping Python or text; named so that it is never read as a chapter code box"""
    h = 14 + len(lines) * size * 1.25 / 0.72 + 4
    R(s, name, x, y, w, h, fill=CODEBG, line=None, adj=0.06)
    text(s, name + " text", x + 14, y + 8, w - 28, h - 12, code_paras(lines, size), anchor="t", wrap=False)
    return y + h


def flow(s, y, items, w=None, gap=14, h=100, size=11, accent_last=False, head=12.5):
    n = len(items); w = w or (900 - gap * (n - 1)) / n
    for i, (title, body) in enumerate(items):
        x = X0 + i * (w + gap); last = accent_last and i == n - 1
        R(s, "step %d" % (i + 1), x, y, w, h, fill=SOFT if last else CARD, line=TEAL if last else LINE, anchor="t", paras=[P(title, head, TEAL if last else ORANGE, True), P(body, size, INK)], inset=9)
        if i < n - 1: A(s, "arrow %d" % (i + 1), x + w + 1, y + h / 2, x + w + gap - 1, y + h / 2, ORANGE, 2.0)


# ------------------------------------------------------------------------------------------------------------------------------------------------
def new_slide(prs, src, title, sub, take):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    for sh in list(s.shapes): delete(sh)
    bg = src._element.cSld.find(qn("p:bg"))
    if bg is not None: s._element.cSld.insert(0, copy.deepcopy(bg))
    for sh in src.shapes:
        if sh.top / U < 120 or sh.top / U >= 500: s.shapes._spTree.append(copy.deepcopy(sh._element))
    for sh in s.shapes:
        L, Tp = round(sh.left / U), round(sh.top / U)
        if L == 125 and Tp == 26: settext(sh, title)
        elif L == 125 and Tp == 88: settext(sh, sub)
        elif L == 72 and Tp == 503: settext(sh, take)
        elif L == 860 and Tp == 508: sh.name = "number"
    # the title shrinks like the existing slides: 28 pt up to 32 characters, 24 pt up to 46, 21 pt beyond
    for sh in s.shapes:
        if round(sh.left / U) == 125 and round(sh.top / U) == 26:
            for r in sh.text_frame.paragraphs[0].runs: r.font.size = Pt(28 if len(title) <= 32 else (24 if len(title) <= 46 else 21))
    return s


# ---- L0 lambda -------------------------------------------------------------------------------------------------------------------------------
def L0(s):
    tiles = [("lambda", 170, ORANGE, WHITE, "makes a function that has no name"), ("v", 150, TEAL, WHITE, "the one input it takes"), (":", 110, INK, WHITE, "ends the inputs"),
             ("round(v * 10**8)", 380, SOFT, INK, "the value it hands back")]
    x = X0
    for t, w, f, c, lab in tiles:
        R(s, "tile " + t, x, 140, w, 44, fill=f, line=TEAL if f == SOFT else None, paras=[{"runs": [(t, 14, c, True, False, "Courier New")], "align": "c"}], adj=0.12)
        T(s, "tile label", x, 190, w, 40, [P(lab, 11, MUTE, False, True, align="c")]); x += w + 14
    sat = lambda v: round(v * 10 ** 8)
    outs = json.loads(TL.ALICE_DECODED)["vout"]
    rows = [("v, in bitcoin", "sat(v), in satoshis")] + [("%s" % o["value"], "{:,}".format(sat(o["value"]))) for o in outs]
    T(s, "table head", X0, 236, 420, 24, [P("Alice's two outputs run through it", 12, TEAL, True)])
    table(s, "lambda table", X0, 264, (210, 210), rows, 28, size=12, hh=26)
    T(s, "def head", 500, 236, 450, 24, [P("The same helper with a name, written with def", 12, TEAL, True)])
    codecard(s, "def card", 500, 264, 450, ["def sat(v):", "    return round(v * 10**8)"], size=11.5)
    bullets(s, ["A lambda is a function with no name: written on one line, right where it is needed, it hands back the value after the colon.",
                "Here sat turns bitcoin into satoshis; the def form beside it does the same job, and sat is just a variable that holds the function.",
                "Use a lambda for a tiny job done once, a named def for anything reused. Think of a sticky note with a formula."], 354, size=12)


# ---- N1 full node ----------------------------------------------------------------------------------------------------------------------------
def N1(s):
    flow(s, 140, [("1  Start", "The node starts and looks for other nodes."),
                  ("2  Peer and connection", "A peer is another node it keeps a connection with, up to a limit."),
                  ("3  Initial download", "Fetches and checks the whole chain before it processes transactions."),
                  ("4  Full node", "Checks every block and every transaction against every rule itself."),
                  ("5  Stay in sync", "Accepts and passes on what is valid, so others can check it too.")], h=134, gap=12, size=11, head=12)
    T(s, "chart head", X0, 274, 440, 24, [P("Megabytes to fetch after being offline", 12, TEAL, True)])
    days = [1, 5, 10, 20]
    col_chart(s, "catch up chart", X0, 302, 440, 122, ["%d day%s" % (d, "" if d == 1 else "s") for d in days], [400 * d for d in days], size=10, hi=2)
    card(s, "why check", 520, 282, 430, "Why every node checks", "A full node's report is authoritative because it verified the data itself; a node that only trusted others is only as good as they are.", size=11.5, minh=136)
    bullets(s, ["A node off for ten days fetches about four gigabytes, at 400 megabytes a day. Think of an accountant reading the whole ledger before touching the till."], 432, size=12)


# ---- N2 open source and forks ----------------------------------------------------------------------------------------------------------------
def N2(s):
    R(s, "old rules", X0, 140, 440, 250, fill=WHITE, line=ORANGE, lw=2.0, adj=0.05)
    T(s, "old label", X0 + 14, 146, 410, 26, [P("Blocks the old rules accept", 12.5, ORANGE, True)])
    R(s, "new rules", X0 + 60, 190, 320, 120, fill=SOFT, line=TEAL, lw=2.0, adj=0.08, anchor="m", paras=[P("Blocks the new rules accept", 12.5, TEAL, True, align="c"), P("a smaller set, inside the old one", 11, INK, align="c")], inset=8)
    T(s, "old note", X0 + 14, 326, 410, 56, [P("A soft fork tightens the rules like this: every block the new rules accept is still valid for old nodes, so they keep following the chain.", 11, MUTE, False, True)])
    y = card(s, "open source card", 520, 140, 430, "Open-source software", "Its source code is published under a licence that lets anyone use, change and distribute it; Bitcoin Core uses the MIT license.", size=11)
    y = card(s, "fork card", 520, y + 8, 430, "Fork", "A split of the chain into two branches: by accident, or for good when rules change incompatibly.", size=11)
    y = card(s, "soft fork card", 520, y + 8, 430, "Soft fork", "A backward-compatible tightening of the consensus rules; BIP 9 lets several be deployed at once by signalling in the block version.", size=11, fill=SOFT)
    assert y < 492, y
    bullets(s, ["Think of a club's rulebook: tightening a rule keeps every old game legal, while an incompatible change splits the club in two."], 404, size=12, w=440)


# ---- N3 source to bitcoind -------------------------------------------------------------------------------------------------------------------
def N3(s):
    flow(s, 140, [("Git repository", "git clone copies the repository with its whole history."),
                  ("Build prerequisite", "Libraries and tools that must be present before compiling."),
                  ("Package manager", "Installs the software and the libraries it depends on."),
                  ("Configure", "Choose the options, with the Autotools build or the CMake build."),
                  ("Compilation", "Turns source files into programs; up to an hour, then unit tests.")], h=124, gap=12, size=11, head=12)
    rows = [("", "Autotools build (older books)", "CMake build (current)"),
            ("Configure", "./autogen.sh, then ./configure", "cmake -B build"),
            ("Compile", "make", "cmake --build build"),
            ("Options", "--disable-wallet, --with-gui=no", "-DENABLE_WALLET=OFF, -DBUILD_GUI=ON")]
    table(s, "build table", X0, 284, (140, 380, 380), rows, 30, size=11.5, hh=28)
    bullets(s, ["The bitcoin command is a front door to the node and its tools; its -m option runs the multiprocess programs instead of the monolithic ones.",
                "Think of a kitchen: shopping list (prerequisites), recipe card (configure), oven (compilation)."], 414, size=12)


# ---- N4 trust a download ---------------------------------------------------------------------------------------------------------------------
def N4(s):
    cols = [("Checksum", "A short fixed-size value computed from a file by a hash function; any change to the file changes it.", "It shows your file equals the one that was published."),
            ("OpenPGP signature", "A digital signature in the OpenPGP format, made with a secret key and checked with the matching public key.", "It shows the list of checksums comes from the key holder."),
            ("Reproducible build", "A build that gives bit-for-bit identical files from the same source, so several builders can attest to the same checksums.", "It shows many independent builders reached the same file.")]
    for i, (h, what, shows) in enumerate(cols):
        x = X0 + 306 * i
        hdr(s, "trust title %d" % i, x, 140, 288, 30, h)
        R(s, "trust what %d" % i, x, 174, 288, 100, fill=WHITE, line=LINE, anchor="t", paras=[P(what, 11.5, INK)], inset=10)
        R(s, "trust shows %d" % i, x, 280, 288, 62, fill=SOFT, line=TEAL, anchor="m", paras=[P(shows, 11.5, INK, True)], inset=10)
    R(s, "release verification", X0, 352, 900, 60, fill=CARD, line=ORANGE, lw=1.5, anchor="m",
      paras=[P("Release verification means these checks together: the file matches the published record, which does not prove the signers deserve trust.", 12, INK, True, align="c")], inset=10)
    bullets(s, ["Think of a parcel: the weight on the label is the checksum, the wax seal the signature, and many packers reporting one weight the reproducible build."], 426, size=12)


# ---- N5 options and the start-up log ---------------------------------------------------------------------------------------------------------
def N5(s):
    T(s, "ladder head", X0, 136, 430, 26, [P("Configuration option: a name and a value", 12.5, TEAL, True)])
    for i, (t, f, c, sub) in enumerate((("Command line", ORANGE, WHITE, "wins when it sets the option"), ("Dynamic settings file", CARD, INK, "the node's own file of changes"), ("Configuration file", CARD, INK, "the defaults you keep"))):
        R(s, "source %d" % i, X0, 166 + 66 * i, 430, 54, fill=f, line=LINE if f == CARD else None, anchor="m", paras=[P(t, 12.5, c, True, align="c"), P(sub, 11, c, align="c")], inset=6)
    A(s, "wins arrow", 500, 340, 500, 170, ORANGE, 2.0)
    T(s, "wins label", 506, 240, 80, 40, [P("overrides", 11, ORANGE, True)])
    card(s, "log card", 590, 138, 360, "Start-up log", "While starting, the node prints its version, the settings it read, its connection limits, the interface it opens, the wallet database and the cache sizes.", size=11.5, minh=120)
    card(s, "alert card", 590, 276, 360, "Alert notification (alertnotify)", "Runs a command you choose when the node raises an alert; %s stands for the message, which the node first cleans and puts in single quotes.", size=11.5, fill=SOFT, minh=130)
    bullets(s, ["Read the log after every change: it is the receipt of what the node really did. Think of the slip a machine prints after setup."], 414, size=12)


# ---- N6 wallets and descriptors --------------------------------------------------------------------------------------------------------------
def N6(s):
    rows = [("Wallet", "Stored in", "Status"), ("Descriptor wallet", "SQLite", "The current default"),
            ("Legacy wallet", "A Berkeley DB file, described by its keys", "Since Bitcoin Core 30.0 it can only be migrated, no longer created or loaded")]
    table(s, "wallet kinds", X0, 140, (170, 290, 440), rows, 42, size=11.5, hh=26)
    rows2 = [("Output type", "Address starts with"), ("P2PKH", "1"), ("P2SH-P2WPKH", "3"), ("P2WPKH", "bc1q"), ("P2TR", "bc1p")]
    table(s, "output types", X0, 262, (200, 220), rows2, 28, size=11.5, hh=26)
    y = card(s, "descriptor card", 500, 262, 450, "Output descriptor", "A short text that describes a set of output scripts, optionally followed by an 8-character checksum that catches typing and copying errors.", size=11.5)
    y = card(s, "type card", 500, y + 8, 450, "Output type", "The form of locking an output uses; a descriptor wallet keeps one descriptor for each output type it supports.", size=11.5, fill=SOFT)
    bullets(s, ["Think of a recipe card: one card rebuilds every dish, while a shelf of cooked meals holds only what was made."], 414, size=12, w=440)


# ---- N7 API menu ------------------------------------------------------------------------------------------------------------------------------
def N7(s):
    items = [("Your program", "asks a question"), ("Application programming interface", "the requests the node offers"),
             ("JSON-RPC interface over an HTTP request", "a POST to 127.0.0.1, port 8332"), ("JSON data format", "the answer: objects, arrays, strings, numbers")]
    for i, (t, b) in enumerate(items):
        y = 140 + 68 * i
        R(s, "layer %d" % i, X0, y, 430, 54, fill=SOFT if i == 1 else CARD, line=TEAL if i == 1 else LINE, anchor="m", paras=[P(t, 12, TEAL if i == 1 else ORANGE, True, align="c"), P(b, 11, INK, align="c")], inset=6)
        if i < 3: A(s, "layer arrow %d" % i, X0 + 215, y + 55, X0 + 215, y + 67, ORANGE, 2.0)
    body = json.loads(TL.rpc_body("getblockchaininfo"))
    T(s, "json head", 520, 138, 430, 20, [P("The call as a JSON object", 12, TEAL, True)])
    lines = ["{"] + ['  "%s": %s%s' % (k, json.dumps(v), "," if i < len(body) - 1 else "") for i, (k, v) in enumerate(body.items())] + ["}"]
    y = codecard(s, "json card", 520, 162, 430, lines, size=11)
    T(s, "json read", 520, y + 6, 430, 60, [P("Curly brackets hold an object of name and value pairs; square brackets hold a list, here an empty one.", 11, MUTE, False, True)])
    bullets(s, ["bitcoin-cli, the command-line client, sends the same calls the API offers, so it is the way to experiment; its help command lists them.",
                "Think of a restaurant menu: you may order only what is on it, and every answer arrives on the same kind of plate."], 420, size=12)


# ---- N8 two status calls ----------------------------------------------------------------------------------------------------------------------
def N8(s):
    def listcard(x, title, call, items, fill):
        R(s, "call card " + call, x, 140, 435, 214, fill=fill, line=TEAL)
        T(s, "call title", x + 12, 148, 410, 24, [P(title, 12.5, TEAL, True)])
        T(s, "call name", x + 12, 172, 410, 20, [P("bitcoin-cli " + call, 11, MUTE, False, True, "Courier New")])
        lst = T(s, "call list", x + 12, 198, 410, 150, [{"runs": [(t, 11.5, INK)], "space": 3} for t in items]); real_bullets(lst)
    listcard(X0, "Blockchain information", "getblockchaininfo", ["the chain's name", "the number of blocks and headers", "the best block", "its difficulty and chain work", "whether it is still in its initial download", "whether it is pruned"], WHITE)
    listcard(515, "Network information", "getnetworkinfo", ["the node's own version", "the protocol version", "the services it offers", "its connections and reachable networks", "the fee rates it uses to accept transactions"], SOFT)
    R(s, "read only", X0, 366, 900, 34, fill=CARD, line=LINE, anchor="m", paras=[P("Both are questions, not commands: asking changes nothing in the node.", 12, INK, True, align="c")], inset=6)
    bullets(s, ["Think of a car dashboard with two gauges: one for the road, the chain, and one for the engine's own connections."], 414, size=12)


# ---- N9 cookie or hashed credentials ----------------------------------------------------------------------------------------------------------
def N9(s):
    rows = [("", "Cookie authentication", "Hashed credentials (rpcauth)"),
            ("The secret", "A random value the node writes to the .cookie file at every start", "A fixed user name, a random salt and the HMAC-SHA256 of the password"),
            ("What leaks", "A program that can read the data directory can call the node", "A leaked file shows only the hash, never the password"),
            ("Best for", "Programs that can read the cookie file", "Programs that cannot read the cookie")]
    table(s, "auth table", X0, 140, (130, 385, 385), rows, 54, size=11.5, hh=28)
    items = [("password", "what you type"), ("salt, %d characters" % len(TL.SALT), "random, stored"), ("HMAC-SHA256", "a keyed hash"), ("stored hash", "64 characters, no way back")]
    for i, (t, b) in enumerate(items):
        x = X0 + 230 * i
        R(s, "hash step %d" % i, x, 340, 200, 60, fill=SOFT if i == 3 else CARD, line=TEAL if i == 3 else LINE, anchor="m", paras=[P(t, 11.5, TEAL if i == 3 else ORANGE, True, align="c"), P(b, 11, INK, align="c")], inset=4)
        if i < 3: A(s, "hash arrow %d" % i, x + 202, 370, x + 228, 370, ORANGE, 2.0)
    bullets(s, ["The cookie is recoded at every start, like a hotel key card; rpcauth stays fixed but keeps only a check value, like a bank that never stores your PIN."], 412, size=12)


# ---- N10 bytes to fields ---------------------------------------------------------------------------------------------------------------------
def alice_fields():
    raw = bytes.fromhex(TL.ALICE_HEX); base, wit = TL.split_witness(raw)
    assert len(raw) == 194 and len(base) == 125 and len(wit) == 69
    tx = json.loads(TL.ALICE_DECODED)
    nin, nout = len(tx["vin"]), len(tx["vout"])
    # parse the extended serialization: version 4, marker+flag 2, input count 1, input 32+4+1+4, output count 1, outputs, witness, lock time 4
    pos = 4 + 2; assert raw[4] == 0 and raw[5] == 1
    cnt = raw[pos]; assert cnt == 1; pos += 1; ins = 32 + 4 + 1 + raw[pos + 36] + 4; pos += ins
    out_start = pos; ocnt = raw[pos]; assert ocnt == 2; pos += 1
    for _ in range(ocnt):
        pos += 8; ln = raw[pos]; pos += 1 + ln
    outs = pos - out_start; wit_len = len(raw) - 4 - pos
    fields = [("version", 4), ("marker and flag", 2), ("inputs", 1 + ins), ("outputs", outs), ("witness", wit_len), ("lock time", 4)]
    assert sum(b for _, b in fields) == 194, fields
    return fields


def N10(s):
    fields = alice_fields(); cols = {"version": TEAL, "marker and flag": ORANGE, "inputs": INK, "outputs": "5F8F86", "witness": "B5651D", "lock time": MUTE}
    sc = 900 / 194.0; x = X0
    for nm, nb in fields:
        w = nb * sc
        R(s, "field " + nm, x, 146, w, 44, fill=cols[nm], line=WHITE, adj=0.0, shape=MSO_SHAPE.RECTANGLE, paras=[P("%d B" % nb, 11, WHITE, True, align="c")] if w > 60 else None)
        x += w
    rows = [("Field", "Bytes", "What it holds")] + [(nm, str(nb), t) for (nm, nb), t in zip(fields, [
        "the format edition, written little-endian", "tell a node that a witness follows", "the one coin Alice spends, named by an earlier txid and an index",
        "20,000 and 75,000 satoshis, each with its locking script", "the signature data, kept apart from the txid", "when the transaction may first be mined"])]
    t = table(s, "field table", X0, 202, (170, 70, 660), rows, 28, size=11, hh=26)
    for r in range(1, 7):
        c = t.table.cell(r, 0); c.fill.solid(); c.fill.fore_color.rgb = rgb(cols[fields[r - 1][0]])
        for pa in c.text_frame.paragraphs:
            for rr in pa.runs: rr.font.color.rgb = rgb(WHITE)
    bullets(s, ["Transaction serialization writes the transaction as a sequence of bytes, shown in hexadecimal; a marker and a flag stand before the inputs when a witness follows.",
                "A decoded transaction shows the same 194 bytes as labelled fields, as decoderawtransaction does. Think of an X-ray label: nothing new, only names on the same bones."], 400, size=12)


# ---- N11 segregated witness ------------------------------------------------------------------------------------------------------------------
def N11(s):
    raw = bytes.fromhex(TL.ALICE_HEX); base, wit = TL.split_witness(raw); weight = 4 * len(base) + len(wit); plain = 4 * len(raw)
    sc = 520.0 / plain
    T(s, "bars head", X0, 138, 540, 20, [P("Weight units of Alice's transaction", 12, TEAL, True)])
    R(s, "bar plain", X0, 162, plain * sc, 34, fill=MUTE, line=None, adj=0.0, shape=MSO_SHAPE.RECTANGLE, paras=[P("%d bytes x 4 = %d, if nothing were discounted" % (len(raw), plain), 11, WHITE, True)], inset=6)
    R(s, "bar base", X0, 204, 4 * len(base) * sc, 34, fill=TEAL, line=None, adj=0.0, shape=MSO_SHAPE.RECTANGLE, paras=[P("%d base bytes x 4 = %d" % (len(base), 4 * len(base)), 11, WHITE, True)], inset=6)
    R(s, "bar witness", X0 + 4 * len(base) * sc, 204, len(wit) * sc, 34, fill=ORANGE, line=None, adj=0.0, shape=MSO_SHAPE.RECTANGLE)
    T(s, "witness label", X0 + 569 * sc + 8, 204, 150, 34, [P("witness %d x 1 = %d" % (len(wit), len(wit)), 11, ORANGE, True)])
    T(s, "weight label", X0, 250, 540, 40, [P("Transaction weight = %d units: non-witness bytes count four times, witness bytes once; the virtual size is %d / 4, rounded up = %d." % (weight, weight, -(-weight // 4)), 11.5, INK, True)])
    rows = [("Identifier", "Hashes", "First 16 characters"), ("txid", "the %d base bytes, no witness" % len(base), TL.txid(raw)[:16]), ("wtxid", "all %d bytes, with the witness" % len(raw), TL.wtxid(raw)[:16])]
    table(s, "identifier table", X0, 312, (100, 280, 160), rows, 28, size=11, hh=26)
    y = card(s, "segwit card", 620, 138, 330, "Segregated witness", "Moves signature data out of the part the identifier covers, into a witness that counts less toward the size limit.", size=11.5)
    y = card(s, "txid card", 620, y + 8, 330, "Transaction identifier", "The txid leaves out the witness and the wtxid includes it; before confirmation a txid is not final, because a transaction can be modified.", size=11.5, fill=SOFT)
    assert y < 440, y
    bullets(s, ["A third party can no longer change the txid by re-encoding a signature, because the signature is not in it.",
                "Think of a tracking number printed before anyone signs, and of freight priced by volume: compact data costs less."], 412, size=12)


# ---- N12 block weight and subsidy ------------------------------------------------------------------------------------------------------------
def N12(s):
    eras = list(range(7)); subsidy = [(50 * 10 ** 8 >> n) / 10 ** 8 for n in eras]
    T(s, "chart head", X0, 136, 480, 24, [P("Block subsidy in bitcoins, after each halving", 12, TEAL, True)])
    col_chart(s, "subsidy chart", X0, 160, 480, 200, ["%s" % "{:,}".format(210000 * n) for n in eras], subsidy, fmt="0.#####", size=10, hi=3)
    T(s, "chart foot", X0, 362, 480, 40, [P("Height of the first block of each era; block 775,072 lies in the fourth era, which pays %.2f bitcoins." % ((50 * 10 ** 8 >> (775072 // 210000)) / 10 ** 8), 11, MUTE, False, True)])
    y = card(s, "weight card", 560, 138, 390, "Block weight", "A block without witness data weighs four times its size in weight units; getblock shows size, strippedsize and weight. The limit is 4,000,000.", size=11.5)
    card(s, "subsidy card", 560, y + 10, 390, "Block subsidy", "The newly created coins a miner may claim: it starts at 50 bitcoins and is shifted right once for every 210,000 blocks.", size=11.5, fill=SOFT)
    bullets(s, ["Weight limits what a block holds; the subsidy limits how many coins ever exist. Think of a van with a load limit and a press that slows each cycle."], 420, size=12)


# ---- N13 bits, difficulty, chain work --------------------------------------------------------------------------------------------------------
def N13(s):
    bits = 0x1a6a93b3; ln = bits >> 24; digits = bits & 0xffffff; target = digits << (8 * (ln - 3)); work = 2 ** 256 // (target + 1)
    diff = round(0xffff * 256 ** (0x1d - 3) / (digits * 256 ** (ln - 3)), 1)
    flow(s, 140, [("Compact target (bits)", "The four bytes 0x1a6a93b3 stored in the block header."),
                  ("Length and digits", "The first byte, 0x%02x, is the length: %d bytes; the next three are the digits %06x." % (ln, ln, digits)),
                  ("The target", "Digits shifted left by %d - 3 = %d bytes; a block hash must not exceed it." % (ln, ln - 3)),
                  ("Chain work", "2^256 / (target + 1) hashes expected for this block: the chain work adds them up.")], h=118, size=11, head=12, accent_last=True)
    R(s, "target card", X0, 270, 900, 40, fill=CODEBG, line=None, adj=0.1)
    T(s, "target text", X0 + 14, 278, 880, 24, [[("target  ", 10.5, "F2A860", True, False, "Courier New"), ("%064x" % target, 10.5, CODE_COL["plain"], False, False, "Courier New")]], wrap=False)
    y1 = card(s, "difficulty card", X0, 322, 440, "Difficulty", "How much harder this target is than the easiest one: %s times harder for this block." % "{:,}".format(diff), size=11.5, minh=70)
    y2 = card(s, "work card", 510, 322, 440, "Chain work", "For this block about %.1f x 10^14 hashes are expected; the chain with the most work is the best chain." % (work / 1e14), size=11.5, fill=SOFT, minh=70)
    bullets(s, ["Think of a lock whose gap narrows: a smaller target means more tries on average before a key fits."], max(y1, y2) + 12, size=12)


# ---- N14 fork, best chain, reorganization ----------------------------------------------------------------------------------------------------
def N14(s):
    def blk(name, x, y, label, fill, tc=WHITE):
        R(s, name, x, y, 58, 36, fill=fill, line=None, anchor="m", paras=[P(label, 10.5, tc, True, align="c")], adj=0.15)
    for i, lb in enumerate(("n-2", "n-1", "n")):
        blk("trunk %d" % i, X0 + 70 * i, 232, lb, MUTE)
        if i < 2: A(s, "trunk arrow %d" % i, X0 + 70 * i + 58, 250, X0 + 70 * i + 70, 250, INK, 1.5)
    A(s, "to A", X0 + 3 * 70 - 12 + 0, 244, X0 + 214, 190, ORANGE, 1.5); A(s, "to B", X0 + 3 * 70 - 12, 256, X0 + 214, 312, TEAL, 1.5)
    for i in range(2):
        blk("A %d" % (i + 1), X0 + 214 + 70 * i, 172, "A%d" % (i + 1), ORANGE)
        if i: A(s, "A arrow", X0 + 214 + 58, 190, X0 + 214 + 70, 190, ORANGE, 1.5)
    for i in range(3):
        blk("B %d" % (i + 1), X0 + 214 + 70 * i, 294, "B%d" % (i + 1), TEAL)
        if i: A(s, "B arrow %d" % i, X0 + 214 + 70 * (i - 1) + 58, 312, X0 + 214 + 70 * i, 312, TEAL, 1.5)
    T(s, "A note", X0 + 214, 212, 230, 40, [P("Branch A: less work", 11, ORANGE, True)])
    T(s, "B note", X0 + 214, 334, 260, 40, [P("Branch B: more work, the best chain", 11, TEAL, True)])
    T(s, "fork label", X0, 150, 200, 44, [P("A fork: two blocks found at about the same time", 11, MUTE, False, True)])
    y = card(s, "fork card", 520, 140, 430, "Fork", "A split of the chain into two branches, accidental or permanent.", size=11.5)
    y = card(s, "best card", 520, y + 8, 430, "Best chain", "The valid chain with the most cumulative proof of work, which is not always the one with the most blocks.", size=11.5, fill=SOFT)
    y = card(s, "reorg card", 520, y + 8, 430, "Chain reorganization", "A node switches to the chain with more work: blocks leave the best chain, their transactions return to the mempool unless the new chain holds them.", size=11.5)
    assert y < 492, y
    bullets(s, ["Think of two roads from one crossing: travellers move to the one with more paving, and cargo on the other is sent again."], 390, size=12, w=450)


# ---- N15 libraries, wrappers, registries -----------------------------------------------------------------------------------------------------
def N15(s):
    items = [("Your program", "p.getblockchaininfo()"), ("Wrapper library", "RawProxy hides the HTTP call"), ("JSON-RPC over HTTP", "the request the library builds"), ("bitcoind", "answers; the library decodes it")]
    for i, (t, b) in enumerate(items):
        x = X0 + 228 * i
        R(s, "wrap %d" % i, x, 140, 200, 70, fill=SOFT if i == 1 else CARD, line=TEAL if i == 1 else LINE, anchor="m", paras=[P(t, 12, TEAL if i == 1 else ORANGE, True, align="c"), P(b, 11, INK, align="c")], inset=6)
        if i < 3: A(s, "wrap arrow %d" % i, x + 202, 175, x + 226, 175, ORANGE, 2.0)
    y = card(s, "library card", X0, 232, 290, "Software library", "A collection of code written to be used by other programs, which saves them from writing it again.", size=11.5)
    card(s, "wrapper card", 357, 232, 290, "Wrapper library", "Turns p.getblockchaininfo() into the JSON-RPC request and returns the decoded answer.", size=11.5, fill=SOFT)
    card(s, "registry card", 664, 232, 286, "Package registry", "A public index of the libraries published for a language, with their versions and release dates.", size=11.5)
    bullets(s, ["A registry lets you check how fresh a library is before you rely on it; the next slides do exactly that for nine toolkits.",
                "Think of a phrasebook that turns your sentence into the node's language, and of the date on the newest delivery in a shop window."], 380, size=12)


# ---- N16 verified and linked data ------------------------------------------------------------------------------------------------------------
def N16(s):
    info = json.loads(TL.GETBLOCKCHAININFO)
    T(s, "json head", X0, 136, 230, 26, [P("JSON from your own node", 12, TEAL, True)])
    codecard(s, "plain json", X0, 162, 220, ["{", '  "chain": "%s",' % info["chain"], '  "blocks": %d' % info["blocks"], "}"], size=11)
    A(s, "ctx arrow 1", 276, 205, 308, 205, ORANGE, 2.0)
    T(s, "ctx head", 314, 136, 380, 26, [P("JSON-LD context: keys become names", 12, TEAL, True)])
    codecard(s, "context json", 314, 162, 390, ['"@context": {', '  "chain": "https://example.org/chain",', '  "blocks": "https://example.org/blocks"', "}"], size=10.5)
    A(s, "ctx arrow 2", 708, 205, 736, 205, ORANGE, 2.0)
    T(s, "iri head", 742, 136, 208, 26, [P("IRI: a global name", 12, TEAL, True)])
    R(s, "iri box", 742, 162, 208, 92, fill=SOFT, line=TEAL, anchor="m", paras=[P("https://example.org/chain", 10.5, INK, True, align="c"), P("names one concept for every program; example.org is a placeholder", 10.5, MUTE, False, True, align="c")], inset=8)
    y = card(s, "verified card", X0, 270, 440, "Verified data", "Data from your own node is authoritative because the node verified it itself: the kind of fact a provenance record states about any dataset.", size=11.5)
    card(s, "iri card", 510, 270, 440, "IRI and JSON-LD context", "An internationalized resource identifier is a global name for a thing; a context maps each JSON key to one, making the JSON linked data.", size=11.5, fill=SOFT)
    bullets(s, ["Think of a name tag with a full address: the word chain alone is ambiguous, the address says which chain is meant."], 410, size=12)


# ---- N17a/b computing words ------------------------------------------------------------------------------------------------------------------
def N17a(s):
    rows = [("Word", "What it is", "Where it appears here", "Think of"),
            ("Bit and byte", "A bit is a binary digit; a byte is eight bits, one of 256 values, written with two hexadecimal digits.", "The 32 bytes of the cookie are 64 hexadecimal characters.", "A row of eight light switches"),
            ("Bit shift", "Moves the bits of an integer left or right: a multiplication or a division by a power of two.", "v >> 29 in the version; the subsidy is shifted right once per halving.", "Sliding beads on an abacus rod"),
            ("Unix time", "The seconds counted since 1 January 1970 at 00:00 UTC.", "The time in a block header; the median time 1,305,197,900.", "A stopwatch started at New Year 1970"),
            ("Random number", "A value nobody can predict, drawn from the computer's secure sources of randomness.", "The cookie and the salt of rpcauth.", "A fresh shuffle of a deck")]
    table(s, "computing a", X0, 140, (130, 320, 280, 170), rows, 66, size=11, hh=28)


def N17b(s):
    rows = [("Word", "What it is", "Where it appears here", "Think of"),
            ("File and directory", "A file holds data under a name; a directory holds files and other directories.", "The data directory and the .cookie file", "A filing cabinet"),
            ("Process and thread", "A running program with its own memory; a thread is a flow of execution inside it.", "bitcoind and bitcoin-cli run as separate processes", "A kitchen with several cooks"),
            ("Software library", "Code written to be used by other programs.", "python-bitcoinlib and the chapter library T", "A box of ready-made parts"),
            ("Platform", "The processor family and operating system a program is built for.", "One release archive for each platform", "Plug shapes by country"),
            ("Network protocol", "An agreed format and order of messages between programs.", "HTTP between bitcoin-cli and bitcoind, port 8332", "The etiquette of a phone call"),
            ("Software testing", "Running a program on chosen inputs and comparing with the expected result.", "Unit tests after compilation; a change merges only if they pass", "A test drive before delivery"),
            ("Programming language", "A notation for instructing a computer.", "C++ for the node; Python for tests, helpers and examples", "Languages for one recipe")]
    table(s, "computing b", X0, 138, (150, 310, 300, 140), rows, 44, size=10.5, hh=26)


SPECS = [  # (after old slide, key, title, subtitle, takeaway, function)
    (7, "N1", "What a full node does all day", "Peers, the initial download and checking every rule", "A full node trusts nobody: it checks every rule itself", N1),
    (8, "N2", "Open source and the forks of Bitcoin", "Anyone may read the code; a soft fork tightens the rules", "A soft fork only tightens the rules, so old nodes still follow the chain", N2),
    (10, "N3", "From a git clone to bitcoind", "The tools between the source code and the programs", "Clone, install the prerequisites, configure, compile", N3),
    (14, "N4", "Three checks before you trust a download", "Checksum, signature and reproducible build", "Each check closes one gap; none proves the signers deserve trust", N4),
    (16, "N5", "Options and the start-up log", "One option can come from three places; the log shows the result", "The command line wins; the log tells you what the node did", N5),
    (21, "N6", "Wallets inside the node: descriptors", "How a node describes the scripts it can spend", "A descriptor says in one line what a wallet can watch and spend", N6),
    (23, "N7", "An API is a menu of questions", "From your program to the node and back, in JSON", "You may ask only what the menu offers, and the answer is JSON", N7),
    (26, "N9", "Cookie or hashed credentials?", "Two ways for a program to prove it may call the node", "The cookie changes at every start; rpcauth is fixed but keeps no password", N9),
    (27, "N8", "Two status calls, side by side", "getblockchaininfo and getnetworkinfo", "One call reports the chain, the other the node's own network", N8),
    (28, "L0", "A lambda is a function without a name", "The one-line helper that the next code uses", "A lambda is a tiny function written where it is needed", L0),
    (29, "N10", "From bytes to fields", "Serialization and decoding of Alice's 194 bytes", "Decoding only reads the same bytes in labelled groups", N10),
    (31, "N11", "Segregated witness and the two identifiers", "Why the txid ignores signatures and how weight counts them", "Moving the signature out gives a stable txid and cheaper block space", N11),
    (36, "N12", "Block weight and the block subsidy", "How full a block may be, and what its miner may claim", "Weight limits the block; halving limits the new coins", N12),
    (36, "N13", "From the bits field to chain work", "How a compact number becomes a target and a count of hashes", "A smaller target means more work, and the most work wins", N13),
    (36, "N14", "Forks, the best chain and reorganization", "What a node does when two branches compete", "The chain with the most work is the best chain", N14),
    (38, "N15", "Libraries, wrappers and registries", "Where toolkits live and how they reach the node", "A wrapper hides the HTTP call; a registry shows how fresh a library is", N15),
    (39, "N16", "Facts with a name: verified and linked data", "Your own node's answers, and how JSON becomes linked data", "A context turns plain JSON keys into global names", N16),
    (39, "N17a", "Computing words, part one: numbers", "Four small ideas under the numbers of this chapter", "Plain computing ideas carry the numbers", N17a),
    (39, "N17b", "Computing words, part two: systems", "Seven words from computing and where they appear", "The words of computing name the parts of a node", N17b),
]
