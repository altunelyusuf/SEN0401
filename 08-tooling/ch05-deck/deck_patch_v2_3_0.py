"""Chapter 5 deck 2.3.0: geometry corrections (labels short enough to share their row with the caption, frames that overlapped); every story slide shows its licence-clear picture with the credit and the ISO date of the story; the resources slide gets the watch group and reachable replacements for the blocked links (owner's coordinator, 2026-10-19)."""
import glob, importlib.util, os, re, sys
T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, T)
from sen0401_deck_geom_v1_0_0 import gap_pass
from sen0401_deck_story_v1_1_0 import set_pic, set_fact, move, items, slide, swap_row, add_group
def item(plan, slide_n, t, nth=0):
    return [it for it in plan["slides"][slide_n - 1]["items"] if it["t"] == t][nth]
LABELS = {(7, 1): "loose keys: unrelated", (7, 2): "same seed, same keys", (10, 1): "the word list", (10, 2): "a vector, decoded", (11, 1): "the seed: 512 bits", (11, 2): "new passphrase, new wallet", (13, 1): "the master pair, range-checked"}
def stories():
    p = sorted(glob.glob(os.path.join(T, "sen0401_ch05_stories_v*.py")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    sp = importlib.util.spec_from_file_location("st", p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return {s["id"]: s for s in m.STORIES}
def patch(plan):
    S = stories(); C = "05"
    for (s, k), t in LABELS.items(): plan["slides"][s - 1]["items"][k]["label"] = t
    item(plan, 17, "numlist").update(t="beats", y=1.45, h=0.8)
    for n, k in ((6, "IronKey"), (9, "Bip39Birth"), (18, "GoxColdFind")):
        set_fact(plan, n, when=S[k]["when"], link=S[k]["link"], linkText=S[k]["linkLabel"], x=0.5, y=4.42, w=9.0)
    # 6 the lost password: the photograph gives up height so the fact row can run the full width
    set_pic(plan, 6, C, "photo_stefan_thomas.jpg", S["IronKey"]["credit"], 0.5, 1.45, 2.4, 2.55)
    move(plan, 6, "beats", h=2.3)
    items(plan, 6, "beats")[0]["items"][0] = "2011: paid 7,002 BTC for a bitcoin explainer video"
    # 9 BIP 39
    slide(plan, 9)["sub"] = "BIP 39 was created on 10 September 2013"
    set_pic(plan, 9, C, "photo_trezor_pair.jpg", S["Bip39Birth"]["credit"], 0.5, 1.5, 3.3, 2.1)
    # 18 the forgotten wallet file
    move(plan, 18, "beats", w=6.2)
    set_pic(plan, 18, C, "photo_mtgox_logo.png", S["GoxColdFind"]["credit"], 6.95, 3.0, 2.55, 1.0)
    # 22 resources
    slide(plan, 22)["sub"] = "Checked 2026-10-19; every entry is a live link in this file"
    swap_row(plan, 22, "nytimes.com", label=S["IronKey"]["linkLabel"], url=S["IronKey"]["link"], desc="Popper's report of 12 Jan 2021, republished")
    swap_row(plan, 22, "learnmeabitcoin.com/technical/keys/hd-wallets", label="Bitcoin Wiki: HD wallets (guide)", url="https://en.bitcoin.it/wiki/Deterministic_wallet", desc="Why one seed can give a whole tree of keys, explained on the wiki")
    add_group(plan, 22, "Watch", [["BIP-39 mnemonic words (tutorial video)", "https://www.youtube.com/embed/hRXcY_tIlrw", "Mobilefish.com walks through how twelve words encode a seed"]])
    gap_pass(plan)
