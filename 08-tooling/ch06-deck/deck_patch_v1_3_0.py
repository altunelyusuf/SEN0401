"""Chapter 6 deck 1.3.0: geometry corrections (labels short enough to share their row with the caption, frames that overlapped); every story slide shows its licence-clear picture with the credit and the ISO date of the story, with a full-width fact row; the resources slide gets the watch group and a reachable replacement for the blocked link (owner's coordinator, 2026-10-19)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sen0401_deck_geom_v1_0_0 import gap_pass
from sen0401_deck_story_v1_1_0 import set_pic, set_fact, move, items, slide, swap_row, add_group
import glob, importlib.util, re
T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def stories():
    p = sorted(glob.glob(os.path.join(T, "sen0401_ch06_stories_v*.py")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    sp = importlib.util.spec_from_file_location("st", p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return {s["id"]: s for s in m.STORIES}
def item(plan, slide, t, nth=0):
    return [it for it in plan["slides"][slide - 1]["items"] if it["t"] == t][nth]
LABELS = {(7, 0): 'size, version, marker and flag, counts, lock time', (8, 0): 'the outpoint: identifier in internal order, index 1, 100,000 sat in block 774,958', (8, 1): "the fold-tac pipeline: reversed bytes equal the library's identifier", (9, 2): 'the pizza transaction: inputs, output, fee, id', (12, 1): "Alice's lock time is 0; her funding transaction used 774,957", (12, 2): 'eleven block times, their median, and its lag: 600 seconds', (14, 1): "each output's script: 34 bytes of taproot, 22 bytes of version 0", (15, 2): "the overflow, refused by Core's range check", (16, 1): 'four thresholds, two sizes', (18, 1): 'the txid hashes the 125 legacy bytes; a new witness changes only the wtxid', (20, 1): "Alice's outputs are witness programs v1 and v0; empty input script", (22, 1): '6,720,000 against 6,930,000', (22, 2): 'block 170 spends block 9', (23, 1): '569 bytes, 143 vbytes', (23, 2): 'which spans weigh one per byte'}
def patch(plan):
    for (s, k), t in LABELS.items():
        it = plan["slides"][s - 1]["items"][k]
        capw = min(it["w"] * 0.62, max(1.8, len(it["cap"]) * 0.062 + 0.15)); mx = int((it["w"] - capw - 0.1) / 0.085)
        assert len(t) <= mx, (s, k, len(t), mx, t)
        it["label"] = t
    S = plan["slides"]
    item(plan, 20, "code").update(y=3.52, h=0.9); item(plan, 20, "chips").update(y=4.52, h=0.4)
    S[11]["title"] = "Lock time, and the clock it uses"
    S[17]["title"] = "Malleability: one spend, four identifiers"
    S[22]["sub"] = "The book's table, recomputed from the bytes"
    St = stories(); C = "06"
    for n, k in ((6, "FirstTransaction"), (9, "PizzaDay"), (15, "ValueOverflow"), (19, "GoxMalleability")):
        set_fact(plan, n, when=St[k]["when"], link=St[k]["link"], linkText=St[k]["linkLabel"], x=0.5, y=4.42, w=9.0)
    set_pic(plan, 6, C, "photo_hal_finney_1972.jpg", St["FirstTransaction"]["credit"], 0.5, 1.45, 2.6, 2.5)
    set_pic(plan, 9, C, "photo_papa_johns_jacksonville.jpg", St["PizzaDay"]["credit"], 0.5, 1.45, 2.4, 2.5)
    slide(plan, 15)["sub"] = "A signed amount that wrapped, on 15 August 2010"
    set_pic(plan, 15, C, "photo_satoshi_bust_budapest.jpg", St["ValueOverflow"]["credit"], 0.5, 1.45, 2.2, 2.5, drop=("photo_gavin_andresen_2014.jpg",))
    move(plan, 19, "beats", w=6.2)
    set_pic(plan, 19, C, "photo_mtgox_logo.png", St["GoxMalleability"]["credit"], 6.95, 3.0, 2.55, 1.0)
    slide(plan, 25)["sub"] = "Checked 2026-10-19; every entry is a live link in this file"
    swap_row(plan, 25, "learnmeabitcoin.com/technical/transaction", label="Bitcoin Wiki: Transaction (guide)", url="https://en.bitcoin.it/wiki/Transaction", desc="Fields of a transaction, explained on the wiki")
    add_group(plan, 25, "Watch", [["Bitcoin transaction (tutorial video)", "https://www.youtube.com/embed/PrcJD4rznyA", "Mobilefish.com walks through inputs, outputs and signatures"]])
    gap_pass(plan)
