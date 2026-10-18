"""Chapter 03 deck check, version 1_2_0 - the lineage-facing entry of the chapter's deck check.
It runs sen0401_deck_check_v1_1_0.py (every '>>>' example of the deck re-run under the interpreter of the newest recording, the recording and chart provenance compared)
on the given deck, under Python 3.14 (PY314, default /root/.local/bin/python3.14), and exits with its status; the output is the engine check's own.
Usage: deck_check_v1_2_0.py <deck.pptx>"""
__version__ = "1.2.0"
import os, subprocess, sys
TOOL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY314 = os.environ.get("PY314", "/root/.local/bin/python3.14")
sys.exit(subprocess.call([PY314, "-B", os.path.join(TOOL, "sen0401_deck_check_v1_1_0.py"), "03", os.path.abspath(sys.argv[1])]))
