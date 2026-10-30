#!/usr/bin/env python3
"""sen0401_exam_reader_gap_control v1_0_0 - the lineage agent's OWN reproduction of the reader gap reported by the grading executor: the COMMITTED reader v1.1.0 alone (no grading screens) on synthetic sheets of the midterm paper's own layouts (chapter order and grouped-by-type order), with the committed v1.0.0 student generator (stress model incl. the skipped-row shift). Counts per seed block: ok, held, detected, and the bad outcomes missed, silent_wrong, empty_not_flagged.
Usage: gap_control.py SEEDBASE N   -> prints one line per layout; exit 1 when any bad outcome is counted."""
import collections, json, os, random, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import sen0401_exam_answersheet_v1_1_0 as A
import sen0401_exam_answersheet_measure_v1_0_0 as MS
base, n = int(sys.argv[1]), int(sys.argv[2]); COM = os.path.join(HERE, "papers_midterm_v1"); bad = 0
for order in ("chapter", "type"):
    b = "sen0401_exam_midterm_%s_v1_0_0" % order; lay = json.load(open(os.path.join(COM, b + "_sheet_layout.json")))
    work = tempfile.mkdtemp(); pngs = A.rasterise(os.path.join(COM, b + "_sheet.pdf"), os.path.join(work, "b")); blank = [np.array(Image.open(p).convert("L")) for p in pngs]
    tot = collections.Counter(); regf = 0; rows = 0; sheets_bad = 0; shifts = 0
    for i in range(n):
        rng = random.Random(base + i); ims, truth = MS.student(lay, blank, rng); reg = [A.register(im, lay, p) for p, im in enumerate(ims)]
        if any(r is None for r in reg): regf += 1; continue
        out, bst, held = A.read_sheet(reg, lay); o, p = MS.score(out, truth); tot.update(o); rows += len(truth)
        shifts += any(t["kind"].startswith("shift") for t in truth.values())
        if any(o[k] for k in ("missed", "silent_wrong", "empty_not_flagged")): sheets_bad += 1
    badn = sum(tot[k] for k in ("missed", "silent_wrong", "empty_not_flagged")); bad += badn
    print("%-8s seeds %d..%d: %d sheets (%d with a shift), registration failures %d, rows %d, %s; BAD rows %d on %d sheets" % (order, base, base + n - 1, n, shifts, regf, rows, dict(tot), badn, sheets_bad))
sys.exit(1 if bad else 0)
