"""Check of the repaired answer sheet reader v1.1.0. Prints PASS / FAIL per check; exit 1 on any FAIL. Written by the executor of the repair task; run by the control with its own seed blocks.
The C6 criteria of sen0401_exam_answersheet_check_v1_0_0.py are applied UNCHANGED with the SAME thresholds, to every evaluation block, plus one NEW criterion (zero marks read as empty without a flag):
  no registration failure; no silent wrong answer; no missed ambiguous row; every code slip and swap detected; the reader without the methods makes at least one silent wrong answer or misses one;
  at most 25 percent of recoverable rows held for a person;  NEW: empty_not_flagged == 0.
Blocks named BEFORE the run: calibration 1000-1099 and 2000-2199 (thresholds chosen there only); evaluation 9000-9199 (original) and 31000-31199 (held-out). The control adds its own blocks with --blocks.
Usage: check.py [--log FILE] [--sheets 200] [--blocks 9000,31000,...]   (the log file is created new; an existing log is refused, never appended to)"""
import argparse, json, os, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import sen0401_exam_answersheet_v1_0_0 as A0
import sen0401_exam_answersheet_v1_1_0 as A
import sen0401_exam_answersheet_measure_v1_0_0 as MS0
import sen0401_exam_answersheet_measure_v1_1_0 as MS
CAL = [(1000, 100), (2000, 200)]
ap = argparse.ArgumentParser(); ap.add_argument('--log'); ap.add_argument('--sheets', type=int, default=200); ap.add_argument('--blocks', default='9000,31000'); args = ap.parse_args()
EVAL = [int(x) for x in args.blocks.split(',')]
if args.log and os.path.exists(args.log): print('REFUSED: the log file exists and is never appended to: ' + args.log); sys.exit(2)
res = []; logv = {}
def rep(name, ok, detail=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail), flush=True)
def overlap(a0, an, b0, bn): return a0 < b0 + bn and b0 < a0 + an
work = tempfile.mkdtemp(prefix='sen0401_as_chk11_')
try:
    g = subprocess.run(['git', '-C', HERE, 'status', '--porcelain'], capture_output=True, text=True)
    bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
    rep('K1 no committed file is edited', g.returncode == 0 and not bad, ' '.join(bad[:5]))
    clash = [(c, e) for c in CAL for e in EVAL if overlap(c[0], c[1], e, args.sheets)]
    rep('K2 the calibration seeds (1000-1099, 2000-2199) are not among the evaluation seeds %s' % EVAL, not clash, str(clash))

    lay = A0.build_layout(A0.default_spec()); p1 = os.path.join(work, 'a.pdf'); A0.render(lay, p1)
    img = np.array(Image.open(A0.rasterise(p1, os.path.join(work, 'blank'))[0]).convert('L'))
    reg = [A0.register(img, lay, 0)]; out, bs, held = A.read_sheet(reg, lay)
    flags = {k: v for k, v in out.items() if v['flag'] not in (None, 'blank')}; vals = {k: v['value'] for k, v in out.items() if v['value'] is not None}
    rep('K3 a blank sheet reads blank with the v1.1.0 reader: no value, no flag, no block held', not flags and not vals and not held and reg[0] is not None, 'rows %d, flags %d, values %d, held blocks %d' % (len(out), len(flags), len(vals), len(held)))

    ex = MS0.exhaustive_codes(); bad_ex = [(k, v) for k, v in ex.items() if isinstance(k, int) and (v['undetected'] or v['swaps_undetected'])]
    rep('K4 check digit (unchanged v1.0.0 code): every single-digit slip and adjacent swap of every code of 2 to 5 digits is detected', not bad_ex and ex[5]['substitutions'] == 450000, str(bad_ex))

    def criteria(ev, label, informational=False):
        wm, nv, pk = ev['with_methods'], ev['naive_reader'], ev['per_kind_with_methods']
        share = ev['recoverable_rows_held_by_a_flag'] / ev['recoverable_rows']
        slip = pk.get('code_slip', {}); swap = pk.get('code_swap', {})
        c = {'registration_failures_0': ev['registration_failures'] == 0, 'silent_wrong_0': wm.get('silent_wrong', 0) == 0, 'missed_0': wm.get('missed', 0) == 0,
             'every_slip_detected': slip.get('detected', 0) == sum(slip.values()), 'every_swap_detected': swap.get('detected', 0) == sum(swap.values()),
             'naive_reader_fails_at_least_once': (nv.get('silent_wrong', 0) + nv.get('missed', 0)) > 0, 'held_share_le_25_percent': share <= 0.25,
             'NEW_empty_not_flagged_0': wm.get('empty_not_flagged', 0) == 0}
        print('     [%s] %d sheets, %d rows, registration failures %d' % (label, ev['sheets'], ev['rows_scored'], ev['registration_failures']))
        print('     [%s] with the methods : %s' % (label, json.dumps(wm, sort_keys=True))); print('     [%s] reader without them: %s' % (label, json.dumps(nv, sort_keys=True)))
        print('     [%s] recoverable rows %d, held for a person %d (%.1f percent) by flag kind %s' % (label, ev['recoverable_rows'], ev['recoverable_rows_held_by_a_flag'], 100 * share, ev['recoverable_rows_held_by_flag_kind']))
        for k, v in pk.items(): print('       %-22s with methods %-40s naive %s' % (k, json.dumps(v, sort_keys=True), json.dumps(ev['per_kind_naive'].get(k, {}), sort_keys=True)))
        if ev.get('failing_rows'): print('     [%s] failing rows: %s' % (label, json.dumps(ev['failing_rows'])))
        return c, share
    for b0, n in CAL:
        ev = MS.run(n, b0, True); logv['calibration_%d' % b0] = ev; c, sh = criteria(ev, 'calibration %d-%d (informational: thresholds were chosen here)' % (b0, b0 + n - 1))
        print('     calibration %d criteria: %s' % (b0, {k: v for k, v in c.items()}))
    for b0 in EVAL:
        ev = MS.run(args.sheets, b0, True); logv['evaluation_%d' % b0] = ev; c, sh = criteria(ev, 'evaluation %d-%d' % (b0, b0 + args.sheets - 1))
        rep('K5 block %d: the C6 criteria of v1.0.0 unchanged, and NEW zero marks read as empty without a flag' % b0, all(c.values()),
            'silent_wrong %d, missed %d (naive %d and %d), unflagged empty reads %d, held share %.1f percent; failed criteria %s' % (ev['with_methods'].get('silent_wrong', 0), ev['with_methods'].get('missed', 0),
            ev['naive_reader'].get('silent_wrong', 0), ev['naive_reader'].get('missed', 0), ev['with_methods'].get('empty_not_flagged', 0), 100 * sh, [k for k, v in c.items() if not v]))
    if args.log: json.dump(logv, open(args.log.replace('.txt', '.json'), 'x'), indent=1)
finally:
    shutil.rmtree(work, ignore_errors=True)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
