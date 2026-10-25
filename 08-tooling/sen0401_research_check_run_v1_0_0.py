#!/usr/bin/env python3
"""sen0401_research_check_run v1_0_0 - runs the Research chapter check v1_3_0 for Research/ChNN under the Python 3.14 environment (as the chapter check requires) and passes its exit code and output through. Usage: sen0401_research_check_run_v1_0_0.py NN"""
import os, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); r = subprocess.run(["/home/claude/venv314/bin/python", "-B", os.path.join(T, "sen0401_lineage_chapter_check_v1_3_0.py"), "Research/Ch" + sys.argv[1]], capture_output=True, text=True, cwd=T)
sys.stdout.write(r.stdout + r.stderr); sys.exit(r.returncode)
