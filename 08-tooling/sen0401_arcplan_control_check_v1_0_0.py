#!/usr/bin/env python3
"""sen0401_arcplan_control_check v1_0_0 - the lineage agent's OWN check of the chapter 5 plan file (criterion AC9_Ch05ArcPlan). Usage: sen0401_arcplan_control_check_v1_0_0.py slides | kinds | nochange
slides: the newest plan deck_plan_v*.json of 08-tooling/ch05-deck has as many slides as the newest deck .pptx of 03-materials/ch05, and in the same order (every plan title occurs in the text of the deck slide of the same number); the last slide's plan bg equals the deck's real background (light/dark by its fill).
kinds: the arc check v1_3_0 on chapter 5 refuses nothing for a missing kind or section; ALL its refusals are printed (each carries its rule); exit 0 when none concerns a missing kind or section.
nochange: the deck, the old plan v3_1_0 and the arc check v1_3_0 have the SHA-256 values of the earlier read and git status of tracked files is empty."""
import glob, hashlib, json, os, re, subprocess, sys
from pptx import Presentation
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T); vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
deck = sorted(glob.glob(R + "/03-materials/ch05/*.pptx"), key=vk)[-1]; plan = sorted(glob.glob(T + "/ch05-deck/deck_plan_v*.json"), key=vk)[-1]
def slides():
    P = json.load(open(plan))["slides"]; D = list(Presentation(deck).slides); print(os.path.basename(plan), len(P), "slides;", os.path.basename(deck), len(D), "slides"); bad = []
    norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
    for i, (p, d) in enumerate(zip(P, D), 1):
        tx = norm(" ".join(sh.text_frame.text for sh in d.shapes if sh.has_text_frame))
        if norm(p["title"]) not in tx: bad.append(i)
    print("plan titles not found on the deck slide of the same number:", bad)
    s = D[-1]; fill = s.background.fill; rgb = str(fill.fore_color.rgb) if fill.type is not None else "(none)"; print("last slide real background:", rgb, "| plan bg of the last slide:", P[-1].get("bg"))
    lum = lambda h: sum(int(h[k:k + 2], 16) for k in (0, 2, 4)) / 3 if re.fullmatch(r"[0-9A-Fa-f]{6}", h) else None
    l = lum(rgb); same = l is not None and (("dark" if l < 128 else "light") == P[-1].get("bg"))
    print("plan bg equals the deck's real background:", same); return len(P) == len(D) and not bad and same
def kinds():
    r = subprocess.run([sys.executable, "-B", T + "/sen0401_deck_arc_check_v1_3_0.py", "05"], capture_output=True, text=True); print(r.stdout.strip()); print("arc check exit", r.returncode)
    return not [l for l in r.stdout.splitlines() if l.strip().startswith("REFUSED") and re.search(r"kind|section", l) and re.search(r"missing|no kind|no section|has no", l)]
def nochange():
    want = {"03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_1_0.pptx": "a01711a90797902ff6d186f4beedb9e64d55d5c3245e527b2dcf117599b989af", "08-tooling/ch05-deck/deck_plan_v3_1_0.json": "cff27d1fd7c8af9589690e13d1c4959c4aba3cdeea7e62f8a18034a7a4cb44cf", "08-tooling/sen0401_deck_arc_check_v1_3_0.py": "b04a4449d01361f19b1ab4de58b085d6e990f415670f3693d878d099c4fbb92f"}; ok = True
    for f, h in want.items(): g = hashlib.sha256(open(os.path.join(R, f), "rb").read()).hexdigest(); print(f, g == h); ok &= g == h
    mods = subprocess.run(["git", "diff", "--name-status", "--diff-filter=MD", "a3014ad", "HEAD", "--", "03-materials/ch05", "08-tooling/ch05-deck", "08-tooling/sen0401_deck_arc_check_v1_3_0.py"], cwd=R, capture_output=True, text=True).stdout.strip(); print("files modified or deleted since the register commit a3014ad in the chapter 5 deck/plan folders:", mods or "none"); return ok and not mods
a = sys.argv[1]; ok = {"slides": slides, "kinds": kinds, "nochange": nochange}[a](); print("RESULT %s: %s" % (a, "PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
