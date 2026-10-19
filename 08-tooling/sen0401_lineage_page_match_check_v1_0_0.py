#!/usr/bin/env python3
"""sen0401_lineage_page_match_check v1_0_0 - the check the evidence bridge runs to show that the newest page of chapters 1 to 7 carries what its deck carries: it runs pages_deck_match_verify_v1_0_0.py
on the chapter's newest page data and exits 1 when that tool reports any item not carried (the tool itself always exits 0). Usage: sen0401_lineage_page_match_check_v1_0_0.py Page/ChNN"""
__version__ = "1.0.0"
import glob, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); nn = sys.argv[1].split("Ch")[-1]
pd = sorted(glob.glob(os.path.join(H, "ch%s-page" % nn, "page_data_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
pv = re.search(r"page_data_v([0-9_]+_0)\.json", pd).group(1)
r = subprocess.run([sys.executable, "-B", os.path.join(H, "pages_deck_match_verify_v1_0_0.py"), nn, pv], capture_output=True, text=True)
print(r.stdout.strip()); m = re.search(r"not carried: (\d+)", r.stdout)
sys.exit(0 if r.returncode == 0 and m and int(m.group(1)) == 0 else 1)
