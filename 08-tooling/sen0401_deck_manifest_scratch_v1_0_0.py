#!/usr/bin/env python3
"""sen0401_deck_manifest_scratch v1_0_0 - a new tool of the builder session. Runs the chapter-code manifest check of sen0401_deck_control_check v1_1_0 with the 'deck' field of the newest manifest of a chapter replaced IN MEMORY by the named deck file, in a scratch root of symbolic links (nothing in the repository is written):
it measures whether the manifest's order and names equal the code slides of THAT deck. Usage: sen0401_deck_manifest_scratch_v1_0_0.py NN DECKFILE   (DECKFILE under 03-materials/chNN)"""
__version__ = "1.0.0"
import glob, json, os, re, sys, tempfile
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); nn, deck = sys.argv[1], sys.argv[2]
td = tempfile.mkdtemp(prefix="sen0401_ms_"); os.makedirs(os.path.join(td, "03-materials", "ch%s" % nn, "page")); os.symlink(H, os.path.join(td, "08-tooling"))
os.symlink(os.path.join(R, "03-materials", "ch%s" % nn, deck), os.path.join(td, "03-materials", "ch%s" % nn, deck))
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
mp = sorted(glob.glob(os.path.join(R, "03-materials", "ch%s" % nn, "page", "chapter_code_ch%s_v*.json" % nn)), key=vk)[-1]; m = json.load(open(mp)); m["deck"] = deck
json.dump(m, open(os.path.join(td, "03-materials", "ch%s" % nn, "page", os.path.basename(mp)), "w"))
os.environ["SEN0401_ROOT"] = td; sys.path.insert(0, H)
import sen0401_deck_control_check_v1_1_0 as K
sys.exit(0 if K.manifest(nn) else 1)
