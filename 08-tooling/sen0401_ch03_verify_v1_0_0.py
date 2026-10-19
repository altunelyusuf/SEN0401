#!/usr/bin/env python3
"""SEN0401 chapter 3 verify script: the research package's own consistency checks that need no network and no node, over the newest committed
research, domain TBox, domain ABox and document files of chapter 3 (the six parts are described in sen0401_research_verify_lib_v1_0_0.py:
sources recorded, saved evidence intact, stories, classes-sections-citations, every ABox example executed, findings and sources citing each other).
Exit 0 and 'failures: []' when all hold. Run: python3.14 sen0401_ch03_verify_v1_0_0.py"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_research_verify_lib_v1_0_0 as L
L.run(3)
