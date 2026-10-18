"""Chapter 2 deck 2.3.0: every story slide shows its licence-clear picture with the credit and the ISO date of the story; the resources slide gets a seminal-papers group and the video as an embed URL (owner's coordinator, 2026-10-19)."""
import os, sys, glob, re, importlib.util
T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, T)
from sen0401_deck_story_v1_1_0 import set_pic, set_fact, move, items, slide, swap_row, drop_row, add_group, find_row, groups
def stories():
    p = sorted(glob.glob(os.path.join(T, "sen0401_ch02_stories_v*.py")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    sp = importlib.util.spec_from_file_location("st", p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return {s["id"]: s for s in m.STORIES}
def patch(plan):
    S = stories(); C = "02"
    for n, k in ((6, "WhitepaperMath"), (12, "FirstFaucet"), (21, "ValueOverflow")):
        set_fact(plan, n, when=S[k]["when"], link=S[k]["link"], linkText=S[k]["linkLabel"], x=0.5, y=4.42, w=9.0)
    # 6 the white paper: the news clipping, the quote and the beats make room for the bust of its author's name-sake in a third column
    slide(plan, 6)["sub"] = "Posted to a cryptography mailing list on 31 October 2008"
    move(plan, 6, "news", w=2.6, h=2.45)
    move(plan, 6, "text", x=3.35, w=4.0); move(plan, 6, "beats", x=3.35, w=4.0)
    set_pic(plan, 6, C, "photo_satoshi_bust_budapest.jpg", S["WhitepaperMath"]["credit"], 7.55, 1.45, 1.95, 2.2)
    # 12 the faucet
    set_pic(plan, 12, C, "photo_gavin_andresen.jpg", S["FirstFaucet"]["credit"], 0.5, 1.45, 2.6, 2.55)
    # 21 the value overflow
    move(plan, 21, "claims", w=6.9)
    set_pic(plan, 21, C, "photo_bitcoin_logo.png", S["ValueOverflow"]["credit"], 7.55, 2.95, 1.95, 0.95)
    # 29 resources
    slide(plan, 29)["sub"] = "Checked 2026-10-19; every entry is a live link in this file"
    swap_row(plan, 29, "youtube.com/watch?v=bBC-nXj3Ng4", url="https://www.youtube.com/embed/bBC-nXj3Ng4")
    g, r = find_row(plan, 29, "bitcoin.org/bitcoin.pdf"); g["rows"].remove(r)
    add_group(plan, 29, "Seminal papers", [r, ["Back: Hashcash, a DoS counter-measure (PDF)", "https://cdn.nakamotoinstitute.org/docs/hashcash.pdf", "Adam Back's proof-of-work paper; Nakamoto Institute copy"]], at=1)
