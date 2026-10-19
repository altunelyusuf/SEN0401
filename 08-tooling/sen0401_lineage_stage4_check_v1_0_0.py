#!/usr/bin/env python3
"""sen0401_lineage_stage4_check v1_0_0 - the check the evidence bridge runs for the Stage 4 page ABox of a chapter: RDODI's own pipeline validator over the chapter's Stage 1-4 artefacts through sen0401_stage4_gates_v1_0_0.py.
Exit 0 only when that runner exits 0 (no gate FAILs). NOT_MEASURED and CANNOT_RUN gates do not fail the runner and are NOT passes: they are printed and must be disclosed, never claimed.
Usage: sen0401_lineage_stage4_check_v1_0_0.py Stage4/ChNN"""
__version__ = "1.0.0"
import os, subprocess, sys
n = sys.argv[1].split("Ch")[-1]
r = subprocess.run([sys.executable, "-B", os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0401_stage4_gates_v1_0_0.py"), n], capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip()[-500:])
sys.exit(r.returncode)
