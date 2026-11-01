#!/usr/bin/env python3
"""sen0401_exam_reader_gap_control v1_1_0 - adaptation of the gap control v1_0_0 (unchanged) to read a chosen reader (default 1.2.0) and to add (a) the default layout of the reader, (b) the held share of recoverable rows (same row kinds as the reader measurement v1.1.0).
Layouts: chapter and type (the midterm paper's own sheets, papers_midterm_v1) and default (A.build_layout(default_spec())). Synthetic students: the v1.0.0 generator, unchanged.
Usage: gap_control.py SEEDBASE N [--reader 1.2.0|1.1.0]   -> one line per layout; exit 1 when a bad outcome is counted, a registration fails, or the held share is above 25 percent."""
import collections, json, os, random, shutil, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import sen0401_exam_answersheet_v1_0_0 as A0
import sen0401_exam_answersheet_measure_v1_0_0 as MS
args = [a for a in sys.argv[1:] if not a.startswith('--')]; rv = '1.2.0'
if '--reader' in sys.argv: rv = sys.argv[sys.argv.index('--reader') + 1]; args = [a for a in args if a != rv]
if rv == '1.2.0': import sen0401_exam_answersheet_v1_2_0 as A
else: import sen0401_exam_answersheet_v1_1_0 as A
base, n = int(args[0]), int(args[1]); COM = os.path.join(HERE, "papers_midterm_v1"); bad = 0; fail = 0
RECOV = ('clean', 'light', 'changed_struck', 'code_ok', 'human_written')
def layouts():
    for order in ("chapter", "type"):
        b = "sen0401_exam_midterm_%s_v1_0_0" % order; yield order, json.load(open(os.path.join(COM, b + "_sheet_layout.json"))), os.path.join(COM, b + "_sheet.pdf")
    work = tempfile.mkdtemp(prefix='sen0401_i54_def_'); lay = A0.build_layout(A0.default_spec()); pdf = os.path.join(work, 'd.pdf'); A0.render(lay, pdf); yield "default", lay, pdf
for order, lay, pdf in layouts():
    work = tempfile.mkdtemp(prefix='sen0401_i54_'); pngs = A.rasterise(pdf, os.path.join(work, "b")); blank = [np.array(Image.open(p).convert("L")) for p in pngs]
    tot = collections.Counter(); regf = 0; rows = 0; sheets_bad = 0; shifts = 0; rec = 0; rec_held = 0
    for i in range(n):
        rng = random.Random(base + i); ims, truth = MS.student(lay, blank, rng); reg = [A.register(im, lay, p) for p, im in enumerate(ims)]
        if any(r is None for r in reg): regf += 1; continue
        out, bst, held = A.read_sheet(reg, lay); o, p = MS.score(out, truth); tot.update(o); rows += len(truth)
        shifts += any(t["kind"].startswith("shift") for t in truth.values())
        for no, t in truth.items():
            if t['expect'] == 'accept' and t['kind'] in RECOV:
                rec += 1; rec_held += out[no]['flag'] not in (None, 'blank')
        if any(o[k] for k in ("missed", "silent_wrong", "empty_not_flagged")): sheets_bad += 1
    badn = sum(tot[k] for k in ("missed", "silent_wrong", "empty_not_flagged")); share = rec_held / rec if rec else 0.0
    bad += badn; fail += (regf > 0) + (share > 0.25)
    print("reader %s %-8s seeds %d..%d: %d sheets (%d with a shift), registration failures %d, rows %d, %s; BAD rows %d on %d sheets; recoverable rows %d held %d = %.1f percent%s" % (
        rv, order, base, base + n - 1, n, shifts, regf, rows, dict(tot), badn, sheets_bad, rec, rec_held, 100 * share, "  [HELD SHARE ABOVE 25]" if share > 0.25 else ""))
    shutil.rmtree(work, ignore_errors=True)
sys.exit(1 if (bad or fail) else 0)
