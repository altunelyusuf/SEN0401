#!/usr/bin/env python3
"""sen0401_deck_nine v1.1.0 (over v1.0.0: --fixtures runs deck_fixtures 1.2.0, which finds the credit of any licence) - runs the nine build checks of a SEN0401 deck (chapters 1 to 14) with the options each one needs, on the chapter's newest deck, and prints one line per check.
Why a runner and not 'sen0401_chbuild_v1_2_0.py deckchecks': that command names deck_check 1.0.0 (which reads a chart value as text and refuses a million), picture_check 1.0.0 (which does not count
the pictures of a 'cases' item) and runs the arc and lookfeel checks without --slides N (so a deck of other than 26 slides is refused for its length). This runner names deck_check 1.1.0, picture_check 1.1.0
and passes the deck's own slide count; every other rule of every check is the check's own, nothing is relaxed. deck_check, structure, fit, picture, links (--no-write), honesty, story, arc, lookfeel.
Usage: sen0401_deck_nine_v1_0_0.py NN [--fixtures]      Environment: PY314 (default /root/.local/bin/python3.14).  Exit 0 when all nine pass."""
__version__ = "1.1.0"
import glob, os, re, subprocess, sys, zipfile
TOOL = os.path.dirname(os.path.abspath(__file__)); n = sys.argv[1]
PY314 = os.environ.get("PY314", "/root/.local/bin/python3.14"); py = sys.executable
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
deck = os.path.realpath(sorted(glob.glob(os.path.join(TOOL, "ch%s-deck" % n, "sen0401_ch%s_deck_v*.pptx" % n)), key=vk)[-1])
N = len([x for x in zipfile.ZipFile(deck).namelist() if re.match(r"ppt/slides/slide\d+\.xml$", x)])
S = lambda f, *a: [py, os.path.join(TOOL, f)] + list(a)
steps = [("deck_check", [PY314, os.path.join(TOOL, "sen0401_deck_check_v1_1_0.py"), n, deck]), ("structure", S("sen0401_deck_structure_check_v1_0_0.py", deck)),
         ("fit", S("sen0401_deck_fit_check_v1_0_0.py", deck)), ("picture", S("sen0401_deck_picture_check_v1_1_0.py", n)), ("links", S("sen0401_deck_links_check_v1_0_0.py", n, "--no-write")),
         ("honesty", S("sen0401_deck_honesty_check_v1_0_0.py", n)), ("story", S("sen0401_story_check_v1_0_0.py", n)), ("arc", S("sen0401_deck_arc_check_v1_1_0.py", n, "--slides", str(N))),
         ("lookfeel", S("sen0401_deck_lookfeel_check_v1_0_0.py", n, deck, "--slides", str(N)))]
if "--fixtures" in sys.argv: steps.append(("fixtures", S("sen0401_deck_fixtures_v1_2_0.py", n, "--run", "--deck", deck)))
bad = 0; print("deck:", os.path.basename(deck), "(%d slides)" % N)
for name, cmd in steps:
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, SEN0401_DECK=deck), cwd=TOOL); out = (r.stdout + r.stderr).strip().splitlines()
    ref = [l.strip() for l in out if "REFUSED" in l]
    print("%-10s %s" % (name, "PASS" if r.returncode == 0 else "FAIL"))
    for l in ref[:8]: print("    " + l[:230])
    if r.returncode != 0 and not ref: print("    " + (out[-1][:230] if out else ""))
    bad += r.returncode != 0
sys.exit(1 if bad else 0)
