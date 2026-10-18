"""Chapter 7 deck 1.3.0: geometry corrections (labels short enough to share their row with the caption, frames that overlapped); every story slide keeps its picture with the credit and shows the ISO date of the story in a full-width fact row that prints the read link's host; the resources slide gets community and watch groups (owner's coordinator, 2026-10-19)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sen0401_deck_geom_v1_0_0 import gap_pass
from sen0401_deck_story_v1_1_0 import set_pic, set_fact, move, items, slide, add_group
import glob, importlib.util, re
T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def stories():
    p = sorted(glob.glob(os.path.join(T, "sen0401_ch07_stories_v*.py")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    sp = importlib.util.spec_from_file_location("st", p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return {s["id"]: s for s in m.STORIES}
def item(plan, slide, t, nth=0):
    return [it for it in plan["slides"][slide - 1]["items"] if it["t"] == t][nth]
LABELS = {(6, 1): '2 3 ADD 5 EQUAL, and bytes', (6, 2): 'a real spend, two broken ones', (7, 2): "2010 accepts it; today's engine refuses", (9, 0): 'a 72-byte strict low-s signature; the padded copy fails only under DERSIG', (10, 2): 'the padded signature: accepted, then SIG_DER', (11, 0): '2 of 3: right order, wrong order, one short, extra element', (12, 1): 'the 2-of-3 output: its address, a real spend, a wrong script', (14, 0): 'wait until height 800,000: lock time at least that, input not final', (15, 1): 'the 192-byte script through each path; too young an age fails', (17, 1): 'native and nested spends', (18, 1): 'tree proofs, larger trees', (20, 1): 'output key, address, 64-byte key path spend of 308 units; untweaked fails', (21, 1): 'per-leaf weights and proofs', (22, 2): 'a key path spend: one 64-byte signature, 308 units', (23, 0): '2 of 3 with OP_CHECKSIGADD: 104 bytes, one empty signature; one signature fails', (23, 1): '87 opcode values are OP_SUCCESS; OP_LSHIFT succeeds, the legacy engine refuses'}
def patch(plan):
    for (s, k), t in LABELS.items():
        it = plan["slides"][s - 1]["items"][k]
        capw = min(it["w"] * 0.62, max(1.8, len(it["cap"]) * 0.062 + 0.15)); mx = int((it["w"] - capw - 0.1) / 0.085)
        assert len(t) <= mx, (s, k, len(t), mx, t)
        it["label"] = t
    S = plan["slides"]
    S[11]["title"] = "P2SH: the payer sees only a hash"
    S[22]["title"] = "Tapscript: three small changes"
    item(plan, 1, "img").update(h=0.95)
    item(plan, 7, "beats").update(fs=11, h=1.35); item(plan, 7, "code").update(y=3.3)
    item(plan, 10, "beats").update(fs=11, h=1.6); item(plan, 10, "code").update(y=3.5)
    item(plan, 11, "chips").update(y=3.62); item(plan, 11, "beats").update(y=4.3, h=0.6)
    St = stories(); C = "07"
    for n, k in ((7, "OpReturnBug"), (10, "DerFork"), (22, "SchnorrToTaproot")):
        set_fact(plan, n, when=St[k]["when"], link=St[k]["link"], linkText=St[k]["linkLabel"], x=0.5, y=4.42, w=9.0)
    # 7 the script that ended true: picture, beats and code re-spaced above the full-width row
    slide(plan, 7)["sub"] = "Found on 28 July 2010, fixed in version 0.3.5"
    set_pic(plan, 7, C, "photo_satoshi_bust_budapest.jpg", St["OpReturnBug"]["credit"], 0.5, 1.45, 2.3, 2.5)
    move(plan, 7, "beats", y=1.4, h=1.15); move(plan, 7, "code", y=2.95)
    # 10 half the miners
    set_pic(plan, 10, C, "photo_bitcoin_mining_farm.jpg", St["DerFork"]["credit"], 0.5, 1.45, 3.0, 1.69)
    move(plan, 10, "beats", y=1.4, h=1.45); move(plan, 10, "code", y=3.42)
    # 22 Schnorr
    set_pic(plan, 22, C, "photo_claus_schnorr_1986.jpg", St["SchnorrToTaproot"]["credit"], 0.5, 1.45, 2.4, 2.2)
    # 25 resources
    slide(plan, 25)["sub"] = "Checked 2026-10-19; every entry is a live link in this file"
    G = {g["head"]: g for g in items(plan, 25, "links")[0]["groups"]}
    G["Read"]["rows"] += G["Tools"]["rows"]; G["Read"]["head"] = "Read and explore"; items(plan, 25, "links")[0]["groups"].remove(G["Tools"])
    move(plan, 25, "links", y=1.4, h=3.6)
    add_group(plan, 25, "Community", [["Bitcoin Stack Exchange (Q&A site)", "https://bitcoin.stackexchange.com", "Search or ask any technical question; answers are voted"], ["Delving Bitcoin (forum)", "https://delvingbitcoin.org/", "Developers discuss script and consensus changes in the open"]])
    add_group(plan, 25, "Watch", [["Schnorr: Optech workshop 1.1 (video)", "https://www.youtube.com/embed/wybiVFdknhg", "Bitcoin Optech's workshop on the signature scheme of chapter 7"], ["Tapscript: Optech workshop 2.3 (video)", "https://www.youtube.com/embed/nXGe9_M5pjk", "Bitcoin Optech on the three small changes of tapscript"]])
    gap_pass(plan)
