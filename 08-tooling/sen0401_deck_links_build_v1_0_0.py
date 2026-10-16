#!/usr/bin/env python3
"""sen0401_deck_links_build v1.0.0 - rebuilds the deck of chapter 1 to 7 as a new version with named, direct links (owner finding of 2026-10-16).
For the chapter: new plan from the newest plan (sen0401_links_v1_1_0.py plan), the new story companion (stories), the deck drawn by the chapter's own pipeline
(chapters 1 to 4: the shared renderer as before, here through sen0401_deck_render_v1_2_0.js with SEN_LITE=1, raw output; chapters 5 to 7: the wrapper without SEN_LITE,
then sen0401_deck_ooxml_fix_v1_0_0.py and office_stamp_v1_0_0.py), the pptx saved to 03-materials/chNN and to the deck folder, the lecture export.
Usage: sen0401_deck_links_build_v1_0_0.py NN   (the register is written by sen0401_links_v1_1_0.py register, after the build)"""
__version__ = "1.0.0"
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# chapter: (old plan, new plan, old stories, new stories, old pptx name, new pptx name, pipeline, stamp title)
CFG = {
 1: ("deck_plan_v2_8_0.json", "deck_plan_v2_9_0.json", "sen0401_ch01_stories_v1_4_0.py", "sen0401_ch01_stories_v1_5_0.py", "SEN0401_Ch01_Introduction_3e_v2_8_0.pptx", "SEN0401_Ch01_Introduction_3e_v2_9_0.pptx", "lite", None),
 2: ("deck_plan_v2_0_0.json", "deck_plan_v2_1_0.json", "sen0401_ch02_stories_v1_0_0.py", "sen0401_ch02_stories_v1_1_0.py", "SEN0401_Ch02_HowBitcoinWorks_3e_v2_0_0.pptx", "SEN0401_Ch02_HowBitcoinWorks_3e_v2_1_0.pptx", "lite", None),
 3: ("deck_plan_v2_0_0.json", "deck_plan_v2_1_0.json", "sen0401_ch03_stories_v1_0_0.py", "sen0401_ch03_stories_v1_1_0.py", "SEN0401_Ch03_BitcoinCore_3e_v2_0_0.pptx", "SEN0401_Ch03_BitcoinCore_3e_v2_1_0.pptx", "lite", None),
 4: ("deck_plan_v3_0_0.json", "deck_plan_v3_1_0.json", "sen0401_ch04_stories_v1_0_0.py", "sen0401_ch04_stories_v1_1_0.py", "SEN0401_Ch04_KeysAndAddresses_3e_v3_0_0.pptx", "SEN0401_Ch04_KeysAndAddresses_3e_v3_1_0.pptx", "lite", None),
 5: ("deck_plan_v2_1_0.json", "deck_plan_v2_2_0.json", "sen0401_ch05_stories_v1_0_0.py", "sen0401_ch05_stories_v1_1_0.py", "SEN0401_Ch05_WalletRecovery_3e_v2_1_0.pptx", "SEN0401_Ch05_WalletRecovery_3e_v2_2_0.pptx", "full", "SEN0401 Chapter 5 - Wallet Recovery"),
 6: ("deck_plan_v1_1_0.json", "deck_plan_v1_2_0.json", "sen0401_ch06_stories_v1_0_0.py", "sen0401_ch06_stories_v1_1_0.py", "SEN0401_Ch06_Transactions_3e_v1_1_0.pptx", "SEN0401_Ch06_Transactions_3e_v1_2_0.pptx", "full", "SEN0401 Chapter 6"),
 7: ("deck_plan_v1_1_0.json", "deck_plan_v1_2_0.json", "sen0401_ch07_stories_v1_0_0.py", "sen0401_ch07_stories_v1_1_0.py", "SEN0401_Ch07_AuthorizationAuthentication_3e_v1_1_0.pptx", "SEN0401_Ch07_AuthorizationAuthentication_3e_v1_2_0.pptx", "full", "SEN0401 Chapter 7"),
}


def run(cmd, cwd=None, env=None):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True)
    print(r.stdout.strip());
    if r.returncode:
        print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))


def main(n):
    op, np_, os_, ns, oldp, newp, pipe, title = CFG[n]
    chd = os.path.join(HERE, "ch%02d-deck" % n)
    new_ver = np_.split("_v", 1)[1][:-5].replace("_", ".")
    run([sys.executable, os.path.join(HERE, "sen0401_links_v1_1_0.py"), "plan", str(n), os.path.join(chd, op), os.path.join(chd, np_)])
    run([sys.executable, os.path.join(HERE, "sen0401_links_v1_1_0.py"), "stories", str(n), os.path.join(HERE, os_), os.path.join(HERE, ns)])
    run([sys.executable, os.path.join(HERE, ns)])
    out = os.path.join(chd, "sen0401_ch%02d_deck_v%s.pptx" % (n, new_ver.replace(".", "_")))
    npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    rend = os.path.join(HERE, "sen0401_deck_render_v1_2_0.js")
    if pipe == "lite":
        run(["node", rend, os.path.join(chd, np_), out], cwd=chd, env={"NODE_PATH": npath, "SEN_LITE": "1"})
    else:
        raw = out[:-5] + "_raw.pptx"
        run(["node", rend, os.path.join(chd, np_), raw], cwd=chd, env={"NODE_PATH": npath})
        run([sys.executable, os.path.join(HERE, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out])
        os.remove(raw)
        run([sys.executable, os.path.join(HERE, "office_stamp_v1_0_0.py"), out, new_ver, title])
    shutil.copy(out, os.path.join(ROOT, "03-materials", "ch%02d" % n, newp))
    run([sys.executable, os.path.join(HERE, "sen0401_lecture_export_v1_1_0.py"), "%02d" % n, newp])
    print("built", out)


if __name__ == "__main__":
    main(int(sys.argv[1]))
