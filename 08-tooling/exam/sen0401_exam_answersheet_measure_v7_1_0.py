"""Measurement v7.1.0 (new file, a copy of sen0401_exam_answersheet_measure_v7_0_0.py, which stays unchanged): the same measurement, with DIGITS DRAWN AT RANDOM IN THE BOXES of Question 2 (layout["boxes"]) of every synthetic sheet: 0 to 5 digits per place, right-aligned, random size, position, tilt and pen darkness, sometimes touching the box line. The reader never looks at the boxes; this proves the digits do not disturb the bubble reading.
Was: Measurement of the answer sheet reader v1.4.0 on SYNTHETIC filled sheets of a v7 sheet (ONE page, choice-type answers only). New file, a copy of sen0401_exam_answersheet_measure_v6_0_0.py, which stays unchanged.
Changes: the reader is v1.4.0 (read_sheet_v7); the synthetic student of sen0401_exam_answersheet_measure_v1_0_0.py (imported, unchanged) paints rows of kind choice, match and order only, so its source is taken at run time with the one
word 'fill' added to those kinds (a fill-in blank is a five-bubble row like a choice row); nothing else of the student, the stress model, the scan simulation or the scoring is changed.
Seed blocks (named before the run; the calibration seeds 1000-1099 and 2000-2199 of the thresholds are never used): the caller gives the base.
Usage: measure_v7.py SHEET.pdf LAYOUT.json [--sheets 40] [--seed-base 57000] [--json FILE] [--print-failures]"""
import argparse, collections, json, os, random, shutil, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import sen0401_exam_answersheet_v1_0_0 as A0
import sen0401_exam_answersheet_v1_4_0 as A


import inspect
import sen0401_exam_answersheet_measure_v1_0_0 as MS0
_src = inspect.getsource(MS0.student); assert _src.count("('choice', 'match', 'order')") == 2
_ns = dict(MS0.__dict__); exec(_src.replace("('choice', 'match', 'order')", "('choice', 'match', 'order', 'fill')"), _ns)
class MS:                                          # the v1.0.0 module with the patched student
    pass
for _k, _v in MS0.__dict__.items():
    if not _k.startswith('__'): setattr(MS, _k, _v)
_student0 = _ns['student']


def draw_digits(im, lay, rng):
    from PIL import ImageDraw, ImageFont
    bx = lay.get('boxes')
    if not bx: return 0
    S = MS.S; tmp = Image.fromarray(im); dr = ImageDraw.Draw(tmp); n = 0
    for e in bx['places']:
        b = e['box']; k = rng.randint(0, e['cells']); digits = [str(rng.randint(0, 9)) for _ in range(k)]
        for j, ch in enumerate(digits):                       # right-aligned: the last digit goes in the last box
            cell = e['cells'] - k + j; size = int(rng.uniform(11, 15) * S)
            f = ImageFont.truetype(A0.FD + 'DejaVuSans.ttf', size)
            x = (b['x'] + cell * 18.0 + 9.0 + rng.gauss(0, 1.2)) * S; y = (b['y'] + b['h'] / 2 + rng.gauss(0, 1.2)) * S
            dr.text((x, y), ch, font=f, fill=MS.pen(rng), anchor='mm'); n += 1
        if rng.random() < .15:                                # a stray stroke across a box line (ink touching the line)
            x = (b['x'] + rng.randint(0, e['cells']) * 18.0) * S; y = (b['y'] + rng.uniform(0, b['h'])) * S
            dr.line([(x - 5 * S / 2, y), (x + 5 * S / 2, y + rng.uniform(-3, 3))], fill=MS.pen(rng), width=max(1, int(S * 0.6)))
    im[:] = np.array(tmp); return n


_scan0 = _ns['scan']; _CUR = {}


def _scan_with_digits(im, rng):
    """The v1.0.0 scan simulation (skew, shift, noise), applied AFTER the digits are drawn, so the digits move with the page like real ink."""
    if _CUR.get('lay') is not None: draw_digits(im, _CUR['lay'], rng)
    return _scan0(im, rng)


_ns['scan'] = _scan_with_digits


def student_with_digits(lay, blank, rng):
    _CUR['lay'] = lay
    return _student0(lay, blank, rng)


MS.student = student_with_digits


def run(pdf, layout_json, n, seed_base, print_failures=False):
    work = tempfile.mkdtemp(prefix='sen0401_as_meas71_')
    try:
        lay = json.load(open(layout_json)); blank = [np.array(Image.open(p).convert('L')) for p in A0.rasterise(pdf, os.path.join(work, 'b'))][:1]     # v7: the sheet is one page
        tot = collections.Counter(); totn = collections.Counter(); per = collections.defaultdict(collections.Counter); pern = collections.defaultdict(collections.Counter)
        reg_fail = 0; rows = 0; collateral = collections.Counter(); clean_rows = 0; failures = []
        for i in range(n):
            rng = random.Random(seed_base + i)
            ims, truth = MS.student(lay, blank, rng)
            reg = [A0.register(im, lay, p) for p, im in enumerate(ims)]
            if any(r is None for r in reg): reg_fail += 1; continue
            out, bst, held = A.read_sheet_v7(reg, lay); nv = A.read_naive(reg, lay)
            o, p = MS.score(out, truth); on, pn = MS.score(out, truth, naive=nv)
            tot.update(o); totn.update(on)
            for k, c in p.items(): per[k].update(c)
            for k, c in pn.items(): pern[k].update(c)
            rows += len(truth)
            for no, t in truth.items():
                if t['expect'] in ('accept',) and t['kind'] in ('clean', 'light', 'changed_struck', 'code_ok', 'human_written'):
                    clean_rows += 1
                    if out[no]['flag'] not in (None, 'blank'): collateral[out[no]['flag']] += 1
                if print_failures:
                    res = MS.score({no: out[no]}, {no: t})[0]
                    bad = [k for k in res if k in ('silent_wrong', 'empty_not_flagged', 'missed')]
                    if bad: failures.append({'seed': seed_base + i, 'unit': no, 'kind': t['kind'], 'result': bad, 'reader': {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out[no].items()}})
        r = {'reader_version': A.VERSION, 'sheet_pdf': os.path.basename(pdf), 'form_code': lay.get('form_code'), 'sheets': n, 'registration_failures': reg_fail, 'rows_scored': rows, 'with_methods': dict(tot), 'naive_reader': dict(totn),
             'per_kind_with_methods': {k: dict(v) for k, v in sorted(per.items())}, 'per_kind_naive': {k: dict(v) for k, v in sorted(pern.items())},
             'recoverable_rows': clean_rows, 'recoverable_rows_held_by_a_flag': sum(collateral.values()), 'recoverable_rows_held_by_flag_kind': dict(collateral), 'seed_base': seed_base,
             'thresholds': {'T_INK_OD': A.T_INK_OD, 'T_H_BLANK': A.T_H_BLANK, 'T_H_WRITTEN': A.T_H_WRITTEN}}
        if print_failures: r['failing_rows'] = failures
        return r
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    a = argparse.ArgumentParser(); a.add_argument('pdf'); a.add_argument('layout'); a.add_argument('--sheets', type=int, default=40); a.add_argument('--seed-base', type=int, default=57000)
    a.add_argument('--json'); a.add_argument('--print-failures', action='store_true')
    o = a.parse_args(); r = run(o.pdf, o.layout, o.sheets, o.seed_base, o.print_failures)
    print(json.dumps(r, indent=1))
    if o.json: json.dump(r, open(o.json, 'w'), indent=1)


if __name__ == '__main__': main()
