#!/usr/bin/env python3
"""sen0401_ch11_rulings_fix v1.0.0 - corrects the chapter 11 deck to the owner's material rulings of 2026-11-14 (urgent lineage 7, story ST7_Ch11_Deck).
Reads the newest chapter 11 deck, writes the next version beside it. Changes: four short titles lengthened; presenter notes extended so each teaches its slide
(60-140 words); connectors added to slides without a visual (they show how the cards or steps relate); prompt markers removed from code frames; two lambdas
replaced by def. Nothing else is touched. Usage: python3 sen0401_ch11_rulings_fix_v1_0_0.py"""
import copy, glob, os, re, sys
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE_TYPE as T
from pptx.dml.color import RGBColor
from lxml import etree

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(REPO, "03-materials", "ch11")
def ver(p): return tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.pptx$", p).groups())
src = sorted(glob.glob(os.path.join(D, "SEN0401_Ch11_TheBlockchain_3e_v*.pptx")), key=ver)[-1]
v = ver(src); dst = os.path.join(D, "SEN0401_Ch11_TheBlockchain_3e_v%d_%d_0.pptx" % (v[0], v[1] + 1))
assert not os.path.exists(dst), dst

TITLES = {2: "Today's route through the chapter", 20: "Merkle trees: one root for many", 22: "Pair, hash and repeat upward", 28: "Test blockchains and their constants"}

EXT = {
 2: "Use this slide to promise the shape of the lesson. Point at the four boxes in order, then at the three numbers on the right: forty-three slides, four true stories and seventeen examples. Tell students that every example has a twin on the course page, so they can run the code themselves after class.",
 3: "Read the seven questions aloud and ask students to guess one answer before moving on, but do not answer yet. The point is to give the lesson a target. Each question is answered on a named slide, and we tick them off in the summary so that students can see their own progress.",
 4: "The map shows how much of the chapter each part carries: seventeen key concepts for the block and the chain, seven for merkle trees and seventeen for test blockchains. The arrows join the parts in teaching order. The concept cards between them are short revision stops, and the code slides are where the ideas get their proof.",
 5: "Open the part with the train picture: each carriage is coupled to the one in front, and that coupling is the whole idea of a chain. The three columns preview the part: the anatomy of a block, the name and position of a block, and then links and forks. Ask students to say what they expect to find inside a carriage.",
 6: "Read each card, then give its everyday picture: the parcel, the cover page of a report, the fingerprint with a seat number, the first page of a diary. Ask a student to retell one card in their own words before you show the code slide. The arrows show the order in which the ideas build on each other, from the whole block down to the very first one.",
 7: "Walk the three numbered boxes in order. First the genesis transaction is rebuilt from constants in the source code. Then the block size is the header, one count byte and that transaction. Last, the size is read from Bitcoin Core. Two equal numbers from two independent sources are the proof. Ask students to predict the size before you show it.",
 8: "Link these cards to the train picture from the divider: each header holds its parent's hash, so a carriage cannot be swapped without breaking the coupling. The glacier gives a second way to remember that old layers carry the new ones. Ask students which of the two pictures they prefer, and why.",
 9: "Show the cut points on the line: zero, four, thirty-six, sixty-eight, seventy-two, seventy-six and eighty. The differences between neighbours are the field widths, which the code prints as four, thirty-two, thirty-two, four, four and four. Students should be able to name the six fields in order and say where each one ends.",
 10: "Child blocks matter because they prepare the fork slide later in this part. One parent may have several children, but only one of them continues the family line, and that line is the active chain. Ask students what happens to the other child, and keep their answer for the fork example.",
 11: "Take the three numbers one by one: a clock counted in seconds, a median of eleven clocks that no single liar can move, and a compact target from which the difficulty is computed. Ask students why a median is safer than the latest timestamp. Then show that the bit length of the target tells how hard the work is.",
 12: "Height is counted like the floors of a building from the ground, so the genesis block sits at height zero. Bitcoin Core is the program whose results we compare our own code with, so in this chapter it plays the referee. Satoshi Nakamoto is the name behind the first block that we meet on the next slides.",
 13: "The code reads the message the creator wrote and counts the zeros at the start of the block's name. Ask students why zeros matter: a name that starts with ten zero digits means a great many tries were needed, so the block took real work to produce. The headline also dates the block, and the next slide tells that story.",
 14: "Ask students what else could prove the age of a document, and compare their answers with the newspaper trick. A date quoted inside a block proves the block is not older than that day. Point to the source line on the slide, so that they see the claim can be checked rather than believed.",
 15: "The wax seal is the picture to keep: each block presses its seal over the seal of the previous letter, so rewriting history means redoing every seal after it. BIP 34 is the page number written into the first message of each block. Ask students why a page number helps a reader check the order.",
 16: "Run the comparison in two lines: hash once, then hash twice. The single hash starts with 6dd6c5716cc8 and does not match the block's name; the double hash does. Stress that every node recomputes the name instead of trusting it, which is why a block's name cannot be faked without doing the work.",
 17: "Two ideas share this slide. BIP 34 puts the height inside the first message of each block, and the code reads it back from eight real scripts. The second box shows maturity: a reward is refused after ninety-nine confirmations and accepted after one hundred. Ask why a waiting time protects against a block that is later replaced.",
 18: "This is the most important code slide of the part. Count the links that hold in ten headers, then flip one bit and count again. One link breaks, and seven headers have to be mined again. Ask students what that costs an attacker, because that cost is what protects old blocks.",
 19: "Two children of the same parent form a fork, and the branch that gets another block becomes the active chain. The last lines compute the odds that an attacker with ten percent of the power catches up from zero, one, two and six blocks behind. Let students read the falling numbers and say what that means for waiting before accepting a payment.",
 20: "Open the part with the knockout draw: pairs meet, winners meet again, and one winner is left. A merkle tree plays the same game with hashes. The three columns preview the part: how the tree is built, how a short proof shows that one transaction is inside, and the weakness that comes from repeating the last hash.",
 21: "Use the knockout tournament: teams are paired, winners meet, and at the end one name remains. A merkle tree does the same with hashes, and the single remaining hash, the root, goes into the block header. A light client keeps only headers, so it relies on short proofs instead of whole blocks.",
 22: "Build the tree by hand on the board: four ids, hashed in pairs to give two, hashed again to give the root. The code does exactly this and compares the root with the one in the block header. For three ids the last id is repeated, which is the detail that causes the weakness two slides later.",
 23: "The receipts picture explains the proof: to show that one subtotal belongs in the grand total you hand over only the receipts that sit next to it on the way to the top. That is the authentication path. Say that merkle path is simply another name for it, so that students do not think there are two ideas.",
 24: "To prove one of sixteen transactions you hand over four sibling hashes, 128 bytes in all, and the verifier hashes upward to the root. Show the three sizes for a thousand, four thousand and sixteen thousand transactions: the proof grows by one hash each time the block doubles. That slow growth is what makes light clients possible.",
 25: "Ask students why a patent about digital signatures became the base of a block header. The answer is that one small root can vouch for a long list, and a header only has room for one hash. Then point to the source line, which names the patent number and the date, so that the story can be checked.",
 26: "The test shows two different lists with the same root: repeating the last two ids changes the list but not the root. A block could therefore be altered without changing its header. Core's rule rejects such a block as a duplicate, which is why the story ends well. Ask students how a defender can spot the copy.",
 27: "A light client downloads very little: the header, a count of transactions, five hashes and some flag bits, 248 bytes in all for a block of sixteen. Compare that with downloading the whole block, and ask students to estimate the saving for a block of thousands. Core confirmed that the proof names exactly the transaction we asked about.",
 28: "Open the part with the rehearsal room: same stage, no real audience. Developers need somewhere to break things, so Bitcoin has several chains that follow the same rules with different constants. The three columns preview what follows: the five chains, testnet and its flooding problem, then signet and regtest.",
 29: "Start from the three pictures: the flight simulator, the training pitch and the match, with the same rules but different stakes. Test chains follow Bitcoin's rules with worthless coins so that developers can break things safely. The problems with testnet are the reason testnet4 exists, which the story slide shows.",
 30: "Read the ports as five names for one program: 8333 for mainnet, 18333 for the old testnet, 48333 for testnet4, 38333 for signet and 18444 for regtest. The expected data size is the other difference between them. Ask students which chain they could start on a laptop in seconds.",
 31: "Signet is the club with a doorman: only blocks signed by a trusted signer are accepted, so the chain stays calm. Regtest goes further and runs on your own computer with trivial difficulty. Ask students which of the test chains they would use to try a wallet feature on their laptop, and why.",
 32: "The flags show which chains allow a block at minimum difficulty: testnet, testnet4 and regtest say yes, mainnet and signet say no. That freedom keeps a quiet test chain moving, but it also let miners flood testnet3. Core's help text now calls testnet3 deprecated, and testnet4 starts from its own genesis block.",
 33: "Retell the lesson as cause and effect: a rule meant to keep a small test chain moving became an invitation to vandals, because test coins cost nothing. The fix, testnet4 with BIP 94, writes rules against abuse into the chain itself. Ask students which other free systems face the same problem.",
 34: "This recap uses new pictures: the model railway with the same signals as the real one, and the sandpit. Ask students to say, without looking, what is the same and what is different between a test chain and mainnet. The answer is that the rules are the same, while the constants and the value of the coins differ.",
 35: "Look at the three prefixes: bc for mainnet, tb for the test chains and bcrt for regtest, and the legacy version bytes 0 and 111. A wallet can reject an address from the wrong chain at a glance, which protects students from sending real money to a test address. Ask which prefix they would expect on signet.",
 36: "The village green is the public signet that most developers share, and the members' club is a signet with your own guest list. The guest list is the challenge script, which the next code slide opens up. Connect the two pictures to the script, so that the code does not feel abstract.",
 37: "The challenge is a short script of seventy-one bytes that asks for a signature from one of two keys. Hashing it gives the four magic bytes, 0a03cf40, that identify the chain. A challenge of 51, which means anyone can sign, gives another magic. Show that changing the script changes the network.",
 38: "Retell it as a design choice: instead of paying for blocks with work, a doorman signs them, so a test network stays calm. Two people wrote the proposal, BIP 325, in 2019. Ask students what is traded away when a trusted signer replaces mining, and answer that the chain gives up open participation for stability.",
 39: "Close the concepts with three anchors: regtest as the rehearsal room, BIP 325 as the club's written rules, and mainnet as the real match. Ask students to place a given activity, such as trying a script or paying real money, on the right chain. The arrows show how the three relate.",
 40: "Regtest halves the reward every 150 blocks, so a whole schedule fits into a few seconds of mining. The code feeds that number to the library's rule and compares the result with the values Core recorded at six heights; all of them agree. Ask students what the reward is at heights 1, 150 and 450.",
 41: "Read each line slowly and ask which slide proved it. Line one points to the genesis and header slides, line two to the broken chain and the fork, line three to the merkle path, line four to the weakness slide and line five to the test chain slides. Students who cannot find the proof should go back to that code.",
 42: "Tell students which entry to open first, depending on what they need: the Brownworth demo for the picture of a chain, the Optech topics for the weaknesses and the test chains, and mempool.space to look at real blocks. The community entries are where questions get answered after the course ends.",
}

PROMPT = re.compile(r'^(>>>|\.\.\.|>>)\s?')
LAMBDA18 = ("    link = lambda x, y: y['prev'] == x['hash']", "    link")
def has_code(sh):
    return sh.has_text_frame and sh.name != 'chip' and any(r.font.name == 'Courier New' for pa in sh.text_frame.paragraphs for r in pa.runs)

def set_para_text(par, text):
    runs = par.runs
    runs[0].text = text
    for r in runs[1:]: r._r.getparent().remove(r._r)

def fix_code(sh, slide_no):
    paras = sh.text_frame.paragraphs
    for par in paras:
        t = "".join(r.text for r in par.runs)
        n = PROMPT.sub("", t, count=1)
        if n != t and par.runs: set_para_text(par, n)
    # lambdas -> def (slides 18 and 19)
    for par in sh.text_frame.paragraphs:
        t = "".join(r.text for r in par.runs)
        m = re.match(r"^(\s*)(\w+) = lambda (\w+(?:, \w+)*): (.*)$", t)
        if m and par.runs:
            ind, name, args, body = m.groups()
            set_para_text(par, "%sdef %s(%s): return %s" % (ind, name, args, body))

def accent_rgb(slide):
    for sh in slide.shapes:
        if sh.shape_type == T.AUTO_SHAPE and sh.width < 914400 * 0.2 and sh.height > 914400 * 0.5:
            try: return sh.fill.fore_color.rgb
            except Exception: pass
    return RGBColor(0x5B, 0x6C, 0x8F)

def add_arrow(slide, x1, y1, x2, y2, rgb, name):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(int(x1)), Emu(int(y1)), Emu(int(x2)), Emu(int(y2)))
    c.name = "Connector " + name
    c.line.color.rgb = rgb; c.line.width = Pt(2)
    ln = c.line._get_or_add_ln()
    te = etree.SubElement(ln, "{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd"); te.set("type", "triangle")
    return c

def boxes(slide, minw, minh):
    out = [sh for sh in slide.shapes if sh.shape_type == T.AUTO_SHAPE and sh.width >= minw and sh.height >= minh and sh.top > 914400 * 1.2 and sh.top < 914400 * 4.9]
    return sorted(out, key=lambda s: (round(s.top / 914400, 1), s.left))

def add_flow(slide, ch_slide_no):
    rgb = accent_rgb(slide)
    E = 914400
    cards = boxes(slide, 2.3 * E, 0.9 * E)
    if len(cards) >= 2:
        for a, b in zip(cards, cards[1:]):
            if abs(a.top - b.top) < 0.1 * E:      # same row: right edge to left edge
                add_arrow(slide, a.left + a.width - 0.02 * E, a.top + a.height / 2, b.left + 0.02 * E, b.top + b.height / 2, rgb, "relation")
        for a in cards:                            # same column, next row: straight down
            for b in cards:
                if abs(a.left - b.left) < 0.1 * E and 0 < b.top - a.top < 2.0 * E:
                    add_arrow(slide, a.left + a.width / 2, a.top + a.height - 0.02 * E, b.left + b.width / 2, b.top + 0.02 * E, rgb, "relation")
        return True
    dots = sorted([sh for sh in slide.shapes if sh.shape_type == T.AUTO_SHAPE and abs(sh.width - 0.44 * E) < 0.03 * E and abs(sh.height - 0.44 * E) < 0.03 * E], key=lambda s: s.top)
    if len(dots) >= 2:
        for a, b in zip(dots, dots[1:]):
            add_arrow(slide, a.left + a.width / 2, a.top + a.height - 0.01 * E, b.left + b.width / 2, b.top + 0.01 * E, rgb, "step")
        return True
    dots = sorted([sh for sh in slide.shapes if sh.shape_type == T.AUTO_SHAPE and abs(sh.width - 0.09 * E) < 0.02 * E], key=lambda s: (round(s.left / E), s.top))
    if len(dots) >= 2:
        for a, b in zip(dots, dots[1:]):
            if abs(a.left - b.left) < 0.05 * E and b.top - a.top < 0.6 * E:
                add_arrow(slide, a.left + a.width / 2, a.top + a.height, b.left + b.width / 2, b.top, rgb, "reading-order")
        return True
    return False

def has_visual(slide):
    for sh in slide.shapes:
        if sh.shape_type in (T.PICTURE, T.CHART, T.TABLE, T.GROUP): return True
        if has_code(sh): return True
    return sum(1 for sh in slide.shapes if sh.shape_type == T.LINE or 'Connector' in sh.name) >= 2

prs = Presentation(src); n = len(prs.slides)
for i, s in enumerate(prs.slides, 1):
    if i in TITLES:
        for sh in s.shapes:
            if sh.has_text_frame and sh.name == "Text 2" or (sh.has_text_frame and sh.top < 914400 * 1.3 and sh.text_frame.text.strip() == {2: "Today's route", 20: "Merkle trees", 22: "Pair, hash, repeat", 28: "Test blockchains"}[i]):
                old = sh.text_frame.text.strip()
                if old in ("Today's route", "Merkle trees", "Pair, hash, repeat", "Test blockchains"):
                    set_para_text(sh.text_frame.paragraphs[0], TITLES[i]); break
        else:
            raise SystemExit("title not found on slide %d" % i)
    for sh in s.shapes:
        if has_code(sh): fix_code(sh, i)
    if i not in (1, n) and not has_visual(s):
        assert add_flow(s, i), "no flow placed on slide %d" % i
    if i in EXT:
        tf = s.notes_slide.notes_text_frame
        old = tf.text.strip()
        new = old + " " + EXT[i]
        nw = len(new.split())
        assert 60 <= nw <= 140, (i, nw)
        tf.text = new
prs.save(dst)
print(os.path.basename(dst))
