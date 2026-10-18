"""Chapter 3 deck 2.3.0: every story slide shows its licence-clear picture with the credit and the ISO date of the story; the resources slide gets standards, community and watch groups and the blocked link of the maintainer story is replaced (owner's coordinator, 2026-10-19)."""
import os, sys, glob, re, importlib.util
T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, T)
from sen0401_deck_story_v1_1_0 import set_pic, set_fact, move, items, slide, swap_row, drop_row, add_group, find_row, groups
def stories():
    p = sorted(glob.glob(os.path.join(T, "sen0401_ch03_stories_v*.py")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    sp = importlib.util.spec_from_file_location("st", p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return {s["id"]: s for s in m.STORIES}
def patch(plan):
    S = stories(); C = "03"
    for n, k in ((6, "FirstRelease"), (10, "ReproducibleBuilds"), (14, "MaintainerHandoffs")):
        set_fact(plan, n, when=S[k]["when"], link=S[k]["link"], linkText=S[k]["linkLabel"], x=0.5, y=4.42, w=9.0)
    # 6 version 0.1: clipping, beats and the screenshot make room for the bust
    slide(plan, 6)["sub"] = "Announced on the cryptography list, 8 January 2009"
    move(plan, 6, "news", w=2.6, h=2.45)
    move(plan, 6, "beats", x=3.4, w=4.05); move(plan, 6, "img", x=3.4)
    set_pic(plan, 6, C, "photo_satoshi_bust_budapest.jpg", S["FirstRelease"]["credit"], 7.65, 1.45, 1.85, 2.1)
    # 10 reproducible builds: the Guix logo instead of the project's own icon
    set_pic(plan, 10, C, "photo_guix_logo.png", S["ReproducibleBuilds"]["credit"], 0.5, 1.75, 1.85, 0.6, drop=("core_logo_128.png",))
    # 14 maintainers: the faucet builder of chapter 2, in a column at the right
    move(plan, 14, "flow", y=1.5, h=1.05)
    move(plan, 14, "beats", y=2.7, w=6.8, h=1.5)
    set_pic(plan, 14, C, "photo_gavin_andresen.jpg", S["MaintainerHandoffs"]["credit"], 7.55, 2.65, 1.95, 1.3)
    # 22 resources: five groups (the history rows join Read, the RPC reference joins Verify and build)
    slide(plan, 22)["sub"] = "Checked 2026-10-19; every entry is a live link in this file"
    G = {g["head"]: g for g in groups(plan, 22)}
    rpc = [r for r in G["Talk to a node"]["rows"] if "developer.bitcoin.org" in r[1]][0]; se = [r for r in G["Talk to a node"]["rows"] if "stackexchange" in r[1]][0]
    G["Verify & build"]["rows"].append(rpc); G["Read"]["rows"] += G["History"]["rows"]
    groups(plan, 22)[:] = [G["Read"], G["Verify & build"]]
    add_group(plan, 22, "Standards and papers", [["BIP 1: what a BIP is (spec)", "https://bips.dev/1/", "How a change to Bitcoin is proposed, reviewed and numbered"], ["Bitcoin white paper (PDF)", "https://bitcoin.org/bitcoin.pdf", "Nakamoto's nine pages of 31 October 2008"]])
    add_group(plan, 22, "Community", [["Bitcoin Core PR Review Club (meetings)", "https://bitcoincore.reviews/", "Weekly sessions that read one Core pull request together"], ["Delving Bitcoin (forum)", "https://delvingbitcoin.org/", "Developers discuss protocol and Core changes in the open"], ["bitcoin-dev (mailing list)", "https://groups.google.com/g/bitcoindev", "The development mailing list; read its archive"], se])
    add_group(plan, 22, "Watch", [["Tracing Bitcoin Core v23.0 (talk video)", "https://www.youtube.com/embed/XuRnL393pSk", "A developer shows Core's tracepoints watching a running node"]])
    move(plan, 22, "links", y=1.4, h=3.6)
