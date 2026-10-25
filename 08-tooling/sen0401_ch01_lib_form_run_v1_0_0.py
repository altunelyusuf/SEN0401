#!/usr/bin/env python3
"""sen0401_ch01_lib_form_run v1_0_0 - runs the form of the chapter 2 verify script (the shared library sen0401_research_verify_lib_v1_0_0.run(1), unedited) on the chapter 1 research under Python 3.14 and passes exit code and output through. Usage: sen0401_ch01_lib_form_run_v1_0_0.py NN (NN = 01)"""
import os, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__))
r = subprocess.run(["/home/claude/venv314/bin/python", "-B", "-c", "import sys; sys.path.insert(0, %r); import sen0401_research_verify_lib_v1_0_0 as L; L.run(%d)" % (T, int(sys.argv[1]))], capture_output=True, text=True, cwd=T)
sys.stdout.write(r.stdout + r.stderr); sys.exit(r.returncode)
