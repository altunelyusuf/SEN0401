"""Chapter 4 deck 3.3.0: story slides 6, 12 and 17 show a licence-clear picture with credit and the ISO date of the story in a full-width fact row; the resources slide gets the watch group and a reachable replacement for the blocked link (owner's coordinator, 2026-10-19)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sen0401_deck_geom_v1_0_0 import gap_pass
from sen0401_deck_story_v1_1_0 import set_pic, set_fact, move, items, slide, swap_row, add_group
import glob, importlib.util, re
T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def stories():
    p = sorted(glob.glob(os.path.join(T, "sen0401_ch04_stories_v*.py")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    sp = importlib.util.spec_from_file_location("st", p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return {s["id"]: s for s in m.STORIES}
def patch(plan):
    St = stories(); C = "04"
    for n, k in ((6, "NewDirections1976"), (12, "Base58Design"), (17, "BitcoinEater")):
        set_fact(plan, n, when=St[k]["when"], link=St[k]["link"], linkText=St[k]["linkLabel"], x=0.5, y=4.42, w=9.0)
    set_pic(plan, 6, C, "photo_whitfield_diffie_2017.jpg", St["NewDirections1976"]["credit"], 0.5, 1.45, 1.7, 2.55, drop=("photo_diffie_hellman.jpg",))
    slide(plan, 12)["sub"] = "Written into the first source file, 2009"
    move(plan, 12, "prog", w=6.4)
    set_pic(plan, 12, C, "photo_satoshi_bust_budapest.jpg", St["Base58Design"]["credit"], 7.1, 1.5, 2.4, 2.3)
    move(plan, 17, "beats", w=6.9)
    set_pic(plan, 17, C, "photo_bitcoin_logo.png", St["BitcoinEater"]["credit"], 7.6, 2.95, 1.9, 1.1)
    slide(plan, 24)["sub"] = "Checked 2026-10-19; every entry is a live link in this file"
    swap_row(plan, 24, "learnmeabitcoin.com/technical/keys", label="Bitcoin Wiki: address background (guide)", url="https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses", desc="Keys to addresses, step by step, on the wiki")
    add_group(plan, 24, "Watch", [["Elliptic Curves - Computerphile (video)", "https://www.youtube.com/embed/NF1pwjL9-DE", "The curve behind every public key, explained on screen"]])
    gap_pass(plan)
    move(plan, 22, "code", nth=0, y=3.32); move(plan, 22, "code", nth=1, y=4.4, h=0.62)
