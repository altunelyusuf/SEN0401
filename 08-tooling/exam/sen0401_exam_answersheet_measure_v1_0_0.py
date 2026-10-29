"""Measurement of the answer sheet on SYNTHETIC filled sheets, version 1.0.0.
Synthetic students fill the rendered sheet (marks are painted on the raster, then a scan is simulated: rotation, shift, blur, noise), the reader reads it,
and every row is scored against what the synthetic student meant. The error rates injected are a STRESS MODEL chosen by the author, NOT measured human behaviour:
the measurement says how well the methods detect and read the injected kinds, not how often real students make them.
Thresholds in the reader were fixed on the calibration seeds (--seed-base 1000) and are frozen; the reported run uses the evaluation seeds (--seed-base 9000).
Usage: measure.py [--sheets 200] [--seed-base 9000] [--json FILE] [--samples DIR]   (no real student data; no file kept except the json and the sample images)"""
import argparse, json, math, os, random, sys, tempfile, shutil, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, cv2
from PIL import Image
import sen0401_exam_answersheet_v1_0_0 as A
S = A.S

PROB = {   # per choice-like row (stress model)
    'clean': .66, 'light': .10, 'changed_struck': .07, 'double': .03, 'faint': .03, 'blank_declared': .05, 'blank_forgot': .03, 'wrong_row_shift_marker': 0.0}
STRAY_DOT = .06          # a stray dot in another bubble of a row
SHIFT_PER_SHEET = .30    # a sheet with one skipped-row shift (half inside one block, half running to the end of the choice rows)
BANK_P = {'code_ok': .80, 'code_slip': .08, 'code_swap': .06, 'blank_declared': .03, 'faint': .03}
HUMAN_P = {'written': .90, 'blank_declared': .06, 'blank_forgot': .04}

def pen(rng): return int(rng.uniform(20, 70))
def paint_fill(im, cx, cy, cov, rng):
    r = A.BR * S * rng.uniform(.95, 1.2); jx, jy = rng.gauss(0, .8), rng.gauss(0, .8)
    h = int(r + 6); X, Y = int(round(cx * S + jx)), int(round(cy * S + jy))
    yy, xx = np.mgrid[-h:h + 1, -h:h + 1]; disc = (xx ** 2 + yy ** 2) <= r * r
    th = rng.uniform(0, math.pi); per = 6.0; t = (xx * math.cos(th) + yy * math.sin(th)) % per
    keep = disc & (t >= (1 - cov) * per) if cov < .98 else disc
    sub = im[Y - h:Y + h + 1, X - h:X + h + 1]; sub[keep] = np.minimum(sub[keep], pen(rng))
def line(im, x1, y1, x2, y2, w, rng):
    tmp = Image.fromarray(im); from PIL import ImageDraw
    ImageDraw.Draw(tmp).line([(x1, y1), (x2, y2)], fill=pen(rng), width=max(1, int(round(w)))); im[:] = np.array(tmp)
def paint_strike(im, cx, cy, rng):
    e = rng.uniform(8.8, 10.2) * S; X, Y = cx * S + rng.gauss(0, 1), cy * S + rng.gauss(0, 1); w = rng.uniform(2.4, 3.6)
    line(im, X - e, Y - e + rng.gauss(0, 1.5), X + e, Y + e + rng.gauss(0, 1.5), w, rng); line(im, X - e, Y + e + rng.gauss(0, 1.5), X + e, Y - e + rng.gauss(0, 1.5), w, rng)
def paint_dot(im, cx, cy, rng):
    r = rng.uniform(1.2, 2.6); X, Y = int(cx * S + rng.uniform(-3, 3) * S), int(cy * S + rng.uniform(-3, 3) * S)
    yy, xx = np.mgrid[-4:5, -4:5]; im[Y - 4:Y + 5, X - 4:X + 5][(xx ** 2 + yy ** 2) <= r * r] = pen(rng)
def paint_human(im, box, text_digits, rng):
    for i, ch in enumerate(text_digits):
        x = (box['x'] + i * 18 + 9) * S; y = (box['y'] + box['h'] / 2) * S
        for _ in range(3):
            line(im, x + rng.uniform(-5, 5) * S / 2, y + rng.uniform(-8, 8) * S / 2, x + rng.uniform(-5, 5) * S / 2, y + rng.uniform(-8, 8) * S / 2, 2.5, rng)
def scan(im, rng):
    ang = max(-.6, min(.6, rng.gauss(0, .25))); tx, ty = rng.uniform(-12, 12), rng.uniform(-12, 12)
    M = cv2.getRotationMatrix2D((im.shape[1] / 2, im.shape[0] / 2), ang, 1.0); M[0, 2] += tx; M[1, 2] += ty
    o = cv2.warpAffine(im, M, (im.shape[1], im.shape[0]), flags=cv2.INTER_LINEAR, borderValue=255)
    o = cv2.GaussianBlur(o, (0, 0), rng.uniform(.5, 1.0)).astype(np.float32)
    o = o * rng.uniform(.9, 1.0) + rng.uniform(0, 12) + np.random.RandomState(rng.randint(0, 2 ** 31)).normal(0, 5, o.shape)
    return np.clip(o, 0, 255).astype(np.uint8)

def pick(rng, probs):
    r = rng.random(); a = 0
    for k, p in probs.items():
        a += p
        if r < a: return k
    return list(probs)[0]

def student(layout, blank_imgs, rng):
    """Returns (scanned page images, truth dict unit -> record)."""
    ims = [b.copy() for b in blank_imgs]; truth = {}
    bank_n = sum(1 for u in layout['spec']['units'] if u['kind'] == 'bank') + 2; width = A.serial_width(bank_n)
    serials = list(range(1, bank_n + 1)); rng.shuffle(serials); bank_serials = iter(serials)
    flat = [u['no'] for b in layout['blocks'] if b['kind'] == 'choice' for u in b['units']]
    blk_of = {u['no']: b['id'] for b in layout['blocks'] for u in b['units']}
    ans = {u['no']: rng.choice(u['rows'][0]['opts']) for b in layout['blocks'] if b['kind'] in ('choice', 'match', 'order') for u in b['units']}
    shiftmap = {}; skipped = None; skip_declared = False; shift_kind = None
    if rng.random() < SHIFT_PER_SHEET:
        i0 = rng.randrange(0, len(flat) - 1); skipped = flat[i0]; skip_declared = rng.random() < .5
        shift_kind = 'shift_in_block' if rng.random() < .5 else 'shift_run'
        for j in range(i0, len(flat)):
            if shift_kind == 'shift_in_block' and blk_of[flat[j]] != blk_of[skipped]: break
            nxt = flat[j + 1] if j + 1 < len(flat) else None
            if shift_kind == 'shift_in_block' and nxt is not None and blk_of[nxt] != blk_of[skipped]: nxt = None
            shiftmap[flat[j]] = ans[nxt] if nxt else None
            if nxt is None: break
    for b in layout['blocks']:
        im = ims[b['page']]; units = b['units']; declare = set(); kinds = {}
        if b['kind'] in ('choice', 'match', 'order'):
            n = len(units)
            for idx, u in enumerate(units):
                row = u['rows'][0]; opts = row['opts']; k = pick(rng, PROB); intended = ans[u['no']]
                if u['no'] in shiftmap:
                    # the student skipped item `skipped` but did not leave its row: later answers sit one row too high; the last row of the run stays empty
                    placed = shiftmap[u['no']]
                    if u['no'] == skipped and skip_declared: declare.add(u['no'])
                    if placed: paint_fill(im, row['cx'][opts.index(placed)], row['cy'], rng.uniform(.8, 1), rng)
                    truth[u['no']] = {'kind': shift_kind, 'intended': intended if placed else None, 'expect': ('blank_undeclared' if placed is None else 'hold' if placed != intended else 'accept'), 'unit_kind': b['kind']}
                    continue
                ci = lambda ch: row['cx'][opts.index(ch)]
                if k in ('clean', 'light'): paint_fill(im, ci(intended), row['cy'], rng.uniform(.82, 1) if k == 'clean' else rng.uniform(.62, .8), rng); exp = 'accept'
                elif k == 'changed_struck':
                    old = rng.choice([o for o in opts if o != intended]); paint_fill(im, ci(old), row['cy'], rng.uniform(.8, 1), rng); paint_strike(im, ci(old), row['cy'], rng); paint_fill(im, ci(intended), row['cy'], rng.uniform(.82, 1), rng); exp = 'accept'
                elif k == 'double':
                    old = rng.choice([o for o in opts if o != intended]); paint_fill(im, ci(old), row['cy'], rng.uniform(.8, 1), rng); paint_fill(im, ci(intended), row['cy'], rng.uniform(.82, 1), rng); exp = 'hold'
                elif k == 'faint': paint_fill(im, ci(intended), row['cy'], rng.uniform(.12, .38), rng); exp = 'hold'
                elif k == 'blank_declared': declare.add(u['no']); exp = 'blank'
                else: exp = 'blank_undeclared'
                if k != 'blank_declared' and rng.random() < STRAY_DOT:
                    o2 = rng.choice([o for o in opts if o != intended]); paint_dot(im, ci(o2), row['cy'], rng)
                truth[u['no']] = {'kind': k, 'intended': intended if exp not in ('blank', 'blank_undeclared') else None, 'expect': exp, 'unit_kind': b['kind']}
        elif b['kind'] == 'bank':
            for u in units:
                ser = next(bank_serials); code = A.make_code(ser, width); k = pick(rng, BANK_P)
                shown = code
                if k == 'code_slip':
                    i = rng.randrange(len(code)); d = rng.choice([x for x in '0123456789' if x != code[i]]); shown = code[:i] + d + code[i + 1:]
                if k == 'code_swap' and code[0] != code[1]: shown = code[1] + code[0]
                elif k == 'code_swap': k = 'code_ok'
                if k == 'blank_declared': declare.add(u['no'])
                for ri, row in enumerate(u['rows']):
                    if k == 'blank_declared': break
                    cov = rng.uniform(.12, .38) if k == 'faint' else rng.uniform(.82, 1)
                    paint_fill(im, row['cx'][int(shown[ri])], row['cy'], cov, rng)
                exp = {'code_ok': 'accept', 'code_slip': 'hold', 'code_swap': 'hold', 'blank_declared': 'blank', 'faint': 'hold'}[k]
                truth[u['no']] = {'kind': k, 'intended': code if exp == 'accept' else None, 'expect': exp, 'unit_kind': 'bank', 'meant': code}
        else:
            for u in units:
                k = pick(rng, HUMAN_P)
                if k == 'written': paint_human(im, u['box'], '%d' % rng.randint(1, 99999), rng)
                if k == 'blank_declared': declare.add(u['no'])
                truth[u['no']] = {'kind': 'human_' + k, 'intended': 'WRITTEN' if k == 'written' else None, 'expect': 'accept' if k == 'written' else ('blank' if k == 'blank_declared' else 'blank_undeclared'), 'unit_kind': 'human'}
        for q in b['closure']:
            if q['no'] in declare: paint_fill(im, q['cx'], q['cy'], rng.uniform(.82, 1), rng)
    return [scan(im, rng) for im in ims], truth

def score(out, truth, naive=None):
    """Per row outcome. 'accept' truth: accepted equal -> ok, accepted different -> silent_wrong, held -> held.
    'hold' truth (unrecoverable or slip): held -> detected, accepted any value -> missed. blank truths: a value -> silent_wrong; no value -> ok."""
    o = collections.Counter(); per = collections.defaultdict(collections.Counter)
    for no, t in truth.items():
        if naive is None:
            r = out[no]; flag = r['flag'] if r['flag'] not in ('blank',) else None; val = r['value'] if flag is None else None
            held = flag is not None
        else:
            val = naive[no]; held = False
        exp = t['expect']
        if exp == 'accept':
            res = 'held' if held else ('ok' if val == t['intended'] else 'silent_wrong')
        elif exp == 'hold':
            res = 'detected' if held else ('missed' if val is not None else 'detected')      # an unreadable mark that the reader leaves empty is not a wrong answer
            if held is False and val is None: res = 'empty_not_flagged'
        elif exp in ('blank', 'blank_undeclared'):
            res = 'silent_wrong' if val is not None else ('ok' if not held else 'held')
        o[res] += 1; per[t['kind']][res] += 1
    return o, per

def run(n, seed_base, samples=None):
    work = tempfile.mkdtemp(prefix='sen0401_as_meas_')
    try:
        spec = A.default_spec(); lay = A.build_layout(spec); pdf = os.path.join(work, 's.pdf'); A.render(lay, pdf)
        pngs = A.rasterise(pdf, os.path.join(work, 'b')); blank = [np.array(Image.open(p).convert('L')) for p in pngs]
        tot = collections.Counter(); totn = collections.Counter(); per = collections.defaultdict(collections.Counter); pern = collections.defaultdict(collections.Counter)
        reg_fail = 0; rows = 0; collateral = collections.Counter(); clean_rows = 0; sheets_flagged = 0; blocks_mismatch = collections.Counter()
        for i in range(n):
            rng = random.Random(seed_base + i)
            ims, truth = student(lay, blank, rng)
            reg = [A.register(im, lay, p) for p, im in enumerate(ims)]
            if any(r is None for r in reg): reg_fail += 1; continue
            out, bst, held = A.read_sheet(reg, lay); nv = A.read_naive(reg, lay)
            o, p = score(out, truth); on, pn = score(out, truth, naive=nv)
            tot.update(o); totn.update(on)
            for k, c in p.items(): per[k].update(c)
            for k, c in pn.items(): pern[k].update(c)
            rows += len(truth)
            for no, t in truth.items():
                if t['expect'] in ('accept',) and t['kind'] in ('clean', 'light', 'changed_struck', 'code_ok', 'human_written'):
                    clean_rows += 1
                    if out[no]['flag'] not in (None, 'blank'): collateral[out[no]['flag']] += 1
            sheets_flagged += any(r['flag'] not in (None, 'blank') for r in out.values())
            if samples and i < 2:
                os.makedirs(samples, exist_ok=True)
                Image.fromarray(ims[0]).resize((int(PWpx(lay) * .6), int(PHpx(lay) * .6))).save(os.path.join(samples, 'sen0401_exam_answersheet_synthetic_sample_%d_v1_0_0.png' % (i + 1)), optimize=True)
        return {'sheets': n, 'registration_failures': reg_fail, 'rows_scored': rows, 'with_methods': dict(tot), 'naive_reader': dict(totn),
                'per_kind_with_methods': {k: dict(v) for k, v in sorted(per.items())}, 'per_kind_naive': {k: dict(v) for k, v in sorted(pern.items())},
                'recoverable_rows': clean_rows, 'recoverable_rows_held_by_a_flag': sum(collateral.values()), 'recoverable_rows_held_by_flag_kind': dict(collateral), 'sheets_with_any_flag': sheets_flagged, 'seed_base': seed_base,
                'pages': lay['pages'], 'dpi': A.DPI}
    finally:
        shutil.rmtree(work, ignore_errors=True)
def PWpx(l): return A.PW * S
def PHpx(l): return A.PH * S

def exhaustive_codes():
    """Every single-digit substitution and every adjacent swap of every valid code of 2 to 5 digits (serial + check): how many go unnoticed. Compared with no check digit."""
    res = {}
    for L in (2, 3, 4, 5):
        sub_total = sub_miss = sw_total = sw_miss = 0; sub_naive_miss = 0
        import itertools
        for serial in range(0, 10 ** (L - 1)):
            code = A.make_code(serial, L - 1)
            for i in range(L):
                for d in '0123456789':
                    if d == code[i]: continue
                    bad = code[:i] + d + code[i + 1:]; sub_total += 1; sub_miss += A.damm_valid(bad)
            for i in range(L - 1):
                if code[i] == code[i + 1]: continue
                bad = code[:i] + code[i + 1] + code[i] + code[i + 2:]; sw_total += 1; sw_miss += A.damm_valid(bad)
        res[L] = {'substitutions': sub_total, 'undetected': sub_miss, 'swaps': sw_total, 'swaps_undetected': sw_miss}
    # without a check digit: serials 1..9 of a bank of 8 entries; a one-digit slip to another used serial is an answer that looks valid
    used = set(range(1, 9)); tot = miss = 0
    for s in used:
        for d in range(0, 10):
            if d == s: continue
            tot += 1; miss += (d in used)
    res['no_check_digit_bank_of_8'] = {'substitutions': tot, 'undetected': miss}
    return res

def main():
    a = argparse.ArgumentParser(); a.add_argument('--sheets', type=int, default=200); a.add_argument('--seed-base', type=int, default=9000); a.add_argument('--json'); a.add_argument('--samples')
    o = a.parse_args()
    r = run(o.sheets, o.seed_base, o.samples); r['check_digit_exhaustive'] = exhaustive_codes()
    print(json.dumps(r, indent=1))
    if o.json: json.dump(r, open(o.json, 'w'), indent=1)
if __name__ == '__main__': main()
