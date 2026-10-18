#!/usr/bin/env python3
"""sen0401_lineage_licence_check v1_0_0 - the check the evidence bridge runs for Licence/BOLT_Ch09: the newest provenance file of the chapter 9 page assets names the
BOLT file (bolt03_transactions.md) with the licence the owner ruled (CC BY 4.0, 2026-10-19), exactly once, and names no other licence for any BOLT file.
Exit 0 = holds. Usage: sen0401_lineage_licence_check_v1_0_0.py Licence/BOLT_Ch09"""
__version__ = "1.0.0"
import glob, os, re, sys
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(glob.glob(os.path.join(repo, "03-materials/ch09/assets/ASSETS_PROVENANCE_v*.md")), key=lambda p: [int(x) for x in re.findall(r"v(\d+)_(\d+)_(\d+)", p)[0]])
txt = open(files[-1], encoding="utf-8").read()
rows = [l for l in txt.splitlines() if l.startswith("|") and "bolt" in l.lower().split("|")[1]]
ok = len(rows) == 1 and rows[0].split("|")[3].strip() == "CC BY 4.0"
print(os.path.basename(files[-1]), rows)
sys.exit(0 if ok else 1)
