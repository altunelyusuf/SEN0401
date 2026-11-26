#!/usr/bin/env python3
"""sen0401_ch11_story_replace v1.0.0 - chapter 11: the genesis-headline story is told in chapter 1 (slide 7), so chapter 11 tells a different one
(owner ruling 2026-11-26, answer "Replace in chapter 11"). One run writes, beside the released files (which stay untouched):

  deck  03-materials/ch11/SEN0401_Ch11_TheBlockchain_3e_v2_6_0.pptx   over v2_5_0: slide 14 = the two coinbases that were mined twice, blocks 91722-91880 (picture, three balloons, lesson, READ link, notes);
                                                                       the notes of slides 12, 13, 19 and 38 rewritten (19 explains z, 38 explains challenge script, multisig and magic bytes)
  page  03-materials/ch11/page/sen0401_ch11_page_v9_100_0.html        over v9_99_0: the story record, the lecture entries of slides 12-14, 19 and 38, the references
  data  08-tooling/ch11-page/page_data_v9_100_0.json                  the page's data, byte-equal to the data block inside the page
  more  08-tooling/ch11-page/stories_img_v1_1_0.json, 08-tooling/ch11-deck/link_register_v1_1_0.json, 03-materials/ch11/assets/ASSETS_PROVENANCE_v1_4_0.md

Every anchor must be found exactly once and every output must be new, or the script stops. The story itself is 08-tooling/sen0401_ch11_stories_v1_4_0.py (self-checked
against the saved sources in ch11-evidence)."""
__version__ = "1.0.0"
import base64, copy, hashlib, json, os, re, sys, importlib.util
from pptx import Presentation
from pptx.util import Emu

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
T = os.path.join(R, "08-tooling"); M = os.path.join(R, "03-materials", "ch11")
OLD_DECK = os.path.join(M, "SEN0401_Ch11_TheBlockchain_3e_v2_5_0.pptx"); NEW_DECK = os.path.join(M, "SEN0401_Ch11_TheBlockchain_3e_v2_6_0.pptx")
OLD_PAGE = os.path.join(M, "page", "sen0401_ch11_page_v9_99_0.html"); NEW_PAGE = os.path.join(M, "page", "sen0401_ch11_page_v9_100_0.html")
OLD_DATA = os.path.join(T, "ch11-page", "page_data_v9_99_0.json"); NEW_DATA = os.path.join(T, "ch11-page", "page_data_v9_100_0.json")
PIC = os.path.join(M, "assets", "photo_bitcoinqt_0_5_2_screenshot.png")
for f in (NEW_DECK, NEW_PAGE, NEW_DATA):
    if os.path.exists(f):
        sys.exit("refuse: %s exists" % f)

spec = importlib.util.spec_from_file_location("stories", os.path.join(T, "sen0401_ch11_stories_v1_4_0.py")); st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)
bad = st.run_checks()
if bad:
    sys.exit("stories not ok: %s" % bad)
STORY = st.STORIES[0]
assert STORY["id"] == "TwoCoinbasesThatRepeated"

# ---- the texts ----------------------------------------------------------------------------------------------------
SL14_TITLE = "Two blocks with one coinbase"
SL14_TEXT = ["On 14 November 2010 block 91842 repeated the coinbase of block 91812, down to its identifier d5d27987.",
             "Blocks 91722 and 91880 did the same with e3bf3d07; Bitcoin Core still knows these four blocks by their hashes.",
             "BIP 30 (2012) forbids repeated identifiers; BIP 34 puts the height first in every coinbase, so none can repeat."]
SL14_LESSON = STORY["lesson"] + "."
SL14_CAPTION = "Bitcoin-qt 0.5.2 - the Bitcoin developers, MIT, Wikimedia Commons"
SL14_STANDIN = "Stand-in picture: the client of February 2012"
SL14_READ = (STORY["linkLabel"], STORY["link"], "bips.dev")
N14 = ("On 14 November 2010 block 91812 paid its 50 coins in a coinbase transaction named d5d27987, and block 91842, mined about three hours later, carried a coinbase with the same bytes and therefore the same name; blocks 91722 and 91880 did the same with the name e3bf3d07. "
       "A transaction is named by the hash of its bytes, so two equal coinbases cannot be told apart. "
       "Bitcoin Core lists the earlier two blocks as unspendable and lets the later two through by their hashes. "
       "BIP 30 of 2012 forbids a block to repeat the name of an earlier transaction that is not fully spent, and BIP 34 puts the height first in every coinbase script. "
       "Connect this with slide 17, where the height is read back from the script; the BIP 30 page on the slide gives the rule.")
N19 = ("Two blocks mined on the same parent at height 511 form a fork, and the branch with more work becomes the active chain, so one more block on the first child decided it. "
       "The last lines evaluate the catch-up formula of the white paper for an attacker who holds ten percent of the mining power, where z is the number of blocks by which the attacker's branch is behind the honest one. "
       "With z equal to 0 the chance is 1.0, because the branches are level; for one, two and six blocks behind it is 0.2045873, 0.0509779 and 0.0002428. "
       "The chance falls fast as z grows, which is why waiting for more confirmations makes a payment safer. "
       "This is example 8; connect the fork with the child blocks on slide 10.")
N38 = ("On 20 March 2019 Karl-Johan Alm and Anthony Towns wrote BIP 325, which defines signet, a test network in which a signature replaces mining. "
       "Every signet has a challenge, which is a locking script, and a block is valid only if it carries a solution to that script, so only the holders of the matching keys can make blocks. "
       "The default signet's challenge is a one-of-two multisig, a script that a signature from either of two keys unlocks. "
       "Its four magic bytes, 0a03cf40, are the first four bytes of the double SHA-256 hash of that script, and they open every message on this network. "
       "Nobody can flood such a network, so it stays calm, at the price of open participation. "
       "Core 0.21.0 added signet, and on 15 October 2026 its tip was at height 326,440.")
for nm, tx in (("14", N14), ("19", N19), ("38", N38)):
    w = len(tx.split())
    if not 60 <= w <= 140:
        sys.exit("note %s has %d words (60-140 wanted)" % (nm, w))
    if re.search(r"think of|you will|click|point at|ask the", tx, re.I):
        sys.exit("note %s has a presenter direction" % nm)


def sub1(s, old, new, name):
    if s.count(old) != 1:
        sys.exit('anchor "%s" found %d times (need 1)' % (name, s.count(old)))
    return s.replace(old, new, 1)


def first2(note):
    m = list(re.finditer(r"(?<=[a-z0-9\)])\. (?=[A-Z])", note))
    return note[:m[1].start() + 1] if len(m) >= 2 else note


# ---- the deck -----------------------------------------------------------------------------------------------------
prs = Presentation(OLD_DECK)
S = list(prs.slides)
old12 = S[11].notes_slide.notes_text_frame.text; old13 = S[12].notes_slide.notes_text_frame.text
N12 = sub1(old12, "mined the first block, whose story follows on slide 14.", "mined the first block.", "n12")
N13 = sub1(old13, "This is example 4, and the next slide tells the story of the headline.", "This is example 4; the next slide tells the story of two blocks that repeated a coinbase.", "n13")
S[11].notes_slide.notes_text_frame.text = N12
S[12].notes_slide.notes_text_frame.text = N13
S[18].notes_slide.notes_text_frame.text = N19
S[37].notes_slide.notes_text_frame.text = N38

s14 = S[13]
by = {sh.name: sh for sh in s14.shapes}
def settext(sh, text):
    runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
    if len(runs) != 1:
        sys.exit("shape %s has %d runs (need 1)" % (sh.name, len(runs)))
    runs[0].text = text
settext(by["Text 2"], SL14_TITLE)
settext(by["Text 3"], STORY["title"])
for k, tx in zip(("Story Text 1", "Story Text 2", "Story Text 3"), SL14_TEXT):
    settext(by[k], tx)
settext(by["Text 12"], SL14_LESSON)
settext(by["Text 4"], SL14_CAPTION)
settext(by["Text 13"], SL14_STANDIN)
# READ card: the first paragraph holds "READ  " and the hyperlink run; the second holds the host name
card = by["Text 21"]
paras = card.text_frame.paragraphs
hl = [r for p in paras for r in p.runs if r.hyperlink.address]
if len(hl) != 1:
    sys.exit("READ card: %d hyperlink runs" % len(hl))
old_rid = hl[0]._r.xpath(".//a:hlinkClick/@r:id")[0]
hl[0].text = SL14_READ[0]; hl[0].hyperlink.address = SL14_READ[1]
host = [r for p in paras[1:] for r in p.runs]
if len(host) != 1:
    sys.exit("READ card: %d host runs" % len(host))
host[0].text = SL14_READ[2]
new_rid = hl[0]._r.xpath(".//a:hlinkClick/@r:id")[0]
if new_rid != old_rid:
    s14.part.drop_rel(old_rid)
# the picture: same place and layer, new file, width kept, height from its own proportions
old = by["Image 0"]; w = Emu(old.width); h = int(w * 473 / 773); top = old.top + (old.height - h) // 2
rid_old = old._element.xpath(".//a:blip/@r:embed")[0]
newpic = s14.shapes.add_picture(PIC, old.left, top, w, h)
old._element.addprevious(newpic._element)
newpic.name = "Image 0"
newpic._element.nvPicPr.cNvPr.set("descr", "../../03-materials/ch11/assets/photo_bitcoinqt_0_5_2_screenshot.png")
old._element.getparent().remove(old._element)
s14.part.drop_rel(rid_old)
s14.notes_slide.notes_text_frame.text = N14
prs.core_properties.version = "2.6.0"
prs.save(NEW_DECK)

# ---- the page data --------------------------------------------------------------------------------------------------
raw_page = open(OLD_PAGE, encoding="utf-8").read()
a0 = raw_page.index('<script type="application/json" id="data">') + len('<script type="application/json" id="data">'); a1 = raw_page.index("</script>", a0)
raw = raw_page[a0:a1]
D = json.loads(raw)
if json.dumps(D, ensure_ascii=False).replace("</", "<\\/") != raw:
    sys.exit("the data block does not round-trip")
if json.dumps(D, ensure_ascii=False) != open(OLD_DATA, encoding="utf-8").read():
    sys.exit("page_data_v9_99_0.json is not the data block of the page")
D["_version"] = "9.100.0"
img = base64.b64encode(open(PIC, "rb").read()).decode()
D["stories"][0] = {"id": STORY["id"], "title": STORY["title"], "when": STORY["when"], "who": STORY["who"], "where": STORY["where"], "link": STORY["link"], "story": STORY["story"],
                   "lesson": STORY["lesson"], "source": STORY["source"], "linkLabel": STORY["linkLabel"], "concepts": STORY["concepts"],
                   "imgs": [{"data": "data:image/png;base64," + img, "w": 773, "h": 473, "credit": STORY["credit"], "file": STORY["photo"]}]}
byid = {n["id"]: n for n in D["nodes"]}
for c in STORY["concepts"]:
    if c not in byid:
        sys.exit("story concept %s is not a node of the page" % c)
L = {x["n"]: x for x in D["lecture"]}
L[12]["say"] = first2(N12); L[13]["say"] = first2(N13)
L[14].update({"title": SL14_TITLE, "say": first2(N14), "read": {"label": SL14_READ[0], "url": SL14_READ[1]}, "takeaway": STORY["title"], "concept": "Bip34HeightInCoinbase"})
L[19]["say"] = first2(N19); L[38]["say"] = first2(N38)
NEWREFS = [
    ["mempool.space, block 91722, one of the four blocks of the repeated coinbases, JSON (Mempool Space, 2026)", "https://mempool.space/api/block/00000000000271a2dc26e7667f8419f2e15416dc6955e5a6c6cdf3f2574dd08e"],
    ["mempool.space, block 91812, one of the four blocks of the repeated coinbases, JSON (Mempool Space, 2026)", "https://mempool.space/api/block/00000000000af0aed4792b1acee3d966af36cf5def14935db8de83d6f9306f2f"],
    ["mempool.space, block 91842, one of the four blocks of the repeated coinbases, JSON (Mempool Space, 2026)", "https://mempool.space/api/block/00000000000a4d0a398161ffc163c503763b1f4360639393e0e4c8e300e0caec"],
    ["mempool.space, block 91880, one of the four blocks of the repeated coinbases, JSON (Mempool Space, 2026)", "https://mempool.space/api/block/00000000000743f190a18c5577a3c2d2a1f610ae9601ac046a38084ccb7cd721"],
    ["mempool.space, the transaction ids of block 91842, whose coinbase repeats that of block 91812 (Mempool Space, 2026)", "https://mempool.space/api/block/00000000000a4d0a398161ffc163c503763b1f4360639393e0e4c8e300e0caec/txids"],
    ["mempool.space, the transaction ids of block 91880, whose coinbase repeats that of block 91722 (Mempool Space, 2026)", "https://mempool.space/api/block/00000000000743f190a18c5577a3c2d2a1f610ae9601ac046a38084ccb7cd721/txids"],
    ["mempool.space, the coinbase transaction d5d27987 that blocks 91812 and 91842 share (Mempool Space, 2026)", "https://mempool.space/api/tx/d5d27987d2a3dfc724e359870c6644b40e497bdc0589a033220fe15429d88599"],
    ["Wikimedia Commons, Screenshot of Bitcoin-qt 0.5.2, MIT licence, the picture of the story on the repeated coinbases (Wikimedia Commons, 2012)", "https://commons.wikimedia.org/wiki/File:Screenshot_of_Bitcoin-qt-0.5.2.png"]]
was_sorted = D["refs"] == sorted(D["refs"], key=lambda x: x[0])
D["refs"] = D["refs"] + NEWREFS
if was_sorted:
    D["refs"] = sorted(D["refs"], key=lambda x: x[0])
new_json = json.dumps(D, ensure_ascii=False)
open(NEW_DATA, "w", encoding="utf-8").write(new_json)
page = raw_page[:a0] + new_json.replace("</", "<\\/") + raw_page[a1:]
page = sub1(page, "<!-- page 9.99.0 over 9.98.0", "<!-- page 9.100.0 over 9.99.0 (owner ruling 2026-11-26): the genesis-headline story is told in chapter 1, so the story of this chapter is now the two coinbases that were mined twice, blocks 91722 to 91880 of 14 and 15 November 2010; the notes of slides 12, 13, 19 and 38 are rewritten. Nothing else changed. --><!-- page 9.99.0 over 9.98.0", "head comment")
open(NEW_PAGE, "w", encoding="utf-8").write(page)

# ---- the records beside --------------------------------------------------------------------------------------------
si = json.load(open(os.path.join(T, "ch11-page", "stories_img_v1_0_0.json")))
si["_version"] = "1.1.0"; si["_note"] = si["_note"] + " v1.1.0: the first story is now TwoCoinbasesThatRepeated (the genesis-headline story is told in chapter 1)."
si.pop("HeadlineInTheGenesisBlock")
si = {"_version": si["_version"], "_note": si["_note"], "TwoCoinbasesThatRepeated": [{"file": STORY["photo"], "credit": STORY["credit"]}], **{k: v for k, v in si.items() if k not in ("_version", "_note")}}
json.dump(si, open(os.path.join(T, "ch11-page", "stories_img_v1_1_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
lr = json.load(open(os.path.join(T, "ch11-deck", "link_register_v1_0_0.json")))
lr["_version"] = "1.1.0"; lr["checked"] = "2026-11-26"
lr["links"].append({"slide": 14, "place": "READ card", "old_label": "Genesis block 0 on mempool.space (block)", "old_url": "https://mempool.space/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
                    "new_label": SL14_READ[0], "new_url": SL14_READ[1], "changed": True, "status": None, "title_found": None, "note": "deck 2.6.0: the story of slide 14 is the two coinbases that were mined twice; status and title are read by the link check of the box run (see ch11-evidence/ev_links.log)"})
json.dump(lr, open(os.path.join(T, "ch11-deck", "link_register_v1_1_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
sha = hashlib.sha256(open(PIC, "rb").read()).hexdigest()
open(os.path.join(M, "assets", "ASSETS_PROVENANCE_v1_4_0.md"), "w", encoding="utf-8").write(
    "# Chapter 11 assets - provenance (v1.4.0)\n\nAdds to v1_0_0.md to v1_3_0.md (unchanged) the one new asset of the deck 2.6.0.\n\n| File | Origin | Licence | Credit |\n|---|---|---|---|\n"
    "| photo_bitcoinqt_0_5_2_screenshot.png | File:Screenshot of Bitcoin-qt-0.5.2.png, https://commons.wikimedia.org/wiki/File:Screenshot_of_Bitcoin-qt-0.5.2.png, taken 2026-11-26 from https://upload.wikimedia.org/wikipedia/commons/5/59/Screenshot_of_Bitcoin-qt-0.5.2.png (773 x 473, sha256 %s); recorded 2012-02-21 on Windows 7 | MIT licence (the licence of the software shown), as stated on the Commons page | "
    "Screenshot of Bitcoin-qt 0.5.2 - the Bitcoin developers (Satoshi Nakamoto, Gavin Andresen, Jeff Garzik and others), MIT licence, Wikimedia Commons |\n\n"
    "It is a stand-in picture and says so on its slide: it shows the client of February 2012, the month in which BIP 30 was written, more than a year after the blocks of November 2010. photo_satoshi_bust_budapest.png stays in the folder for the released deck 2.5.0 and page 9.99.0.\n" % sha)
print("deck", NEW_DECK); print("page", NEW_PAGE); print("data", NEW_DATA)
print("notes words: 14=%d 19=%d 38=%d 12=%d 13=%d" % (len(N14.split()), len(N19.split()), len(N38.split()), len(N12.split()), len(N13.split())))
