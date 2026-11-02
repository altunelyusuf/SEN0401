#!/usr/bin/env python3
"""Manifest writer (X3b). Usage: mock_release_manifest_v1_0_0.py SETDIR
Writes SETDIR/MANIFEST_SHA256 (sha256sum format, every file of the folder except the manifest itself, sorted by name) and verifies it with `sha256sum -c`.
Refuses when the master page is not byte-identical to m1. Prints names and hashes only."""
import hashlib, os, subprocess, sys
d = sys.argv[1]
names = sorted(f for f in os.listdir(d) if f != "MANIFEST_SHA256" and os.path.isfile(os.path.join(d, f)))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ms = [f for f in names if "_master_" in f and f.endswith(".html")]; m1 = [f for f in names if "_m1_" in f and f.endswith(".html")]
assert len(ms) == 1 and len(m1) == 1 and sha(os.path.join(d, ms[0])) == sha(os.path.join(d, m1[0])), "master must equal m1"
open(os.path.join(d, "MANIFEST_SHA256"), "w", encoding="utf-8").write("".join("%s  %s\n" % (sha(os.path.join(d, f)), f) for f in names))
r = subprocess.run(["sha256sum", "-c", "MANIFEST_SHA256"], cwd=d, capture_output=True, text=True)
print(r.stdout.strip()); print("sha256sum -c exit", r.returncode, "; files listed", len(names), "; master equals m1: True")
sys.exit(r.returncode)
