"""Chapter 04 deck check, version 3_4_0 - the lineage-facing entry of the chapter's deck check for the deck 3.4.0 (a NEW file; deck_check_v2_1_0.py stays as it is).
It runs sen0401_deck_check_v1_1_0.py (every '>>>' example of the deck re-run under the interpreter of the newest recording, the recording and chart provenance compared)
on the given deck, under Python 3.14 (PY314, default /root/.local/bin/python3.14), and exits with its status; the output is the engine check's own. The newest recording is
examples_out_v3_4_0.json, the newest examples module examples_v3_4_0.py, the newest plan deck_plan_v3_4_0.json.
Usage: deck_check_v3_4_0.py <deck.pptx>"""
__version__ = "3.4.0"
import os, subprocess, sys
TOOL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY314 = os.environ.get("PY314", "/root/.local/bin/python3.14")
sys.exit(subprocess.call([PY314, "-B", os.path.join(TOOL, "sen0401_deck_check_v1_1_0.py"), "04", os.path.abspath(sys.argv[1])]))
