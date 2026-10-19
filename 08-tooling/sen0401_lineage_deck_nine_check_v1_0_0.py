#!/usr/bin/env python3
"""sen0401_lineage_deck_nine_check v1_0_0 - the check the evidence bridge runs for the nine engine checks of a deck: deck_check, structure, fit, picture, links, honesty, story, arc, lookfeel,
and the stale-fixture runner, all through sen0401_deck_nine_v1_0_0.py --fixtures on the chapter's newest deck. Exit 0 only when all pass.
Usage: sen0401_lineage_deck_nine_check_v1_0_0.py Deck/ChNN"""
__version__ = "1.0.0"
import os, subprocess, sys
n = sys.argv[1].split("Ch")[-1]
sys.exit(subprocess.run([sys.executable, "-B", os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0401_deck_nine_v1_0_0.py"), n, "--fixtures"]).returncode)
