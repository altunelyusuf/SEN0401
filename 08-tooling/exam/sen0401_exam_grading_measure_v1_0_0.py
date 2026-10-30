"""Measurement of the grading tool v1.0.0 on SYNTHETIC filled sheets of the two orders of the midterm (no real student, no real scan, no real handwriting).
Synthetic students answer the paper from its own key with an ability (share of places meant right), mark the real sheet PDF of the paper (painted on the raster, then a scan is simulated), and the tool reads and grades.
The painting, scan simulation and error rates (a STRESS MODEL chosen by the author, not measured human behaviour) are the answer-sheet measurement v1.0.0's, imported unchanged; the keyed student below is a modified copy of its student().
THE TRUTH is computed here by a separate, plain scorer (key compared with what each student MEANT), not by the tool. Written places: the tool never reads digits; the simulated instructor types what the student meant to write.
Seed blocks named before the run: 41000-41039 (both orders, 40 sheets each). Nothing was tuned on them. Usage: measure.py [--sheets 40] [--seed-base 41000] [--json FILE]"""
import argparse, collections, json, os, random, shutil, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import sen0401_exam_answersheet_v1_0_0 as A0
import sen0401_exam_answersheet_measure_v1_0_0 as MS
import sen0401_exam_grading_v1_0_0 as G
PAPERS = os.path.join(HERE, 'papers_midterm_v1')
ORDERS = {'chapter': 'sen0401_exam_midterm_chapter_v1_0_0', 'type': 'sen0401_exam_midterm_type_v1_0_0'}

def student_keyed(layout, key, blank_imgs, rng, ability):
    """Like MS.student, but the intended answers come from the key: each place is meant right with probability `ability`."""
    ims = [b.copy() for b in blank_imgs]; truth = {}
    kp = G.key_places(key)
    bank_n = sum(1 for u in layout['spec']['units'] if u['kind'] == 'bank') + 2; width = A0.serial_width(bank_n)
    def wrong_letter(opts, right): return rng.choice([o for o in opts if o != right])
    flat = [u['no'] for b in layout['blocks'] if b['kind'] == 'choice' for u in b['units']]
    blk_of = {u['no']: b['id'] for b in layout['blocks'] for u in b['units']}
    ans = {}
    for b in layout['blocks']:
        if b['kind'] in ('choice', 'match', 'order'):
            for u in b['units']:
                opts = u['rows'][0]['opts']; right = str(kp[u['no']]['answer'])
                ans[u['no']] = right if rng.random() < ability else wrong_letter(opts, right)
    shiftmap = {}; skipped = None; skip_declared = False; shift_kind = None
    if rng.random() < MS.SHIFT_PER_SHEET:
        i0 = rng.randrange(0, len(flat) - 1); skipped = flat[i0]; skip_declared = rng.random() < .5
        shift_kind = 'shift_in_block' if rng.random() < .5 else 'shift_run'
        for j in range(i0, len(flat)):
            if shift_kind == 'shift_in_block' and blk_of[flat[j]] != blk_of[skipped]: break
            nxt = flat[j + 1] if j + 1 < len(flat) else None
            if shift_kind == 'shift_in_block' and nxt is not None and blk_of[nxt] != blk_of[skipped]: nxt = None
            shiftmap[flat[j]] = ans[nxt] if nxt else None
            if nxt is None: break
    for b in layout['blocks']:
        im = ims[b['page']]; units = b['units']; declare = set()
        if b['kind'] in ('choice', 'match', 'order'):
            for u in units:
                row = u['rows'][0]; opts = row['opts']; k = MS.pick(rng, MS.PROB); intended = ans[u['no']]
                if u['no'] in shiftmap:
                    placed = shiftmap[u['no']]
                    if u['no'] == skipped and skip_declared: declare.add(u['no'])
                    if placed: MS.paint_fill(im, row['cx'][opts.index(placed)], row['cy'], rng.uniform(.8, 1), rng)
                    truth[u['no']] = {'kind': shift_kind, 'intended': intended if placed else None, 'expect': ('blank_undeclared' if placed is None else 'hold' if placed != intended else 'accept'), 'meant': intended if placed else None}
                    continue
                ci = lambda ch: row['cx'][opts.index(ch)]
                if k in ('clean', 'light'): MS.paint_fill(im, ci(intended), row['cy'], rng.uniform(.82, 1) if k == 'clean' else rng.uniform(.62, .8), rng); exp = 'accept'
                elif k == 'changed_struck':
                    old = rng.choice([o for o in opts if o != intended]); MS.paint_fill(im, ci(old), row['cy'], rng.uniform(.8, 1), rng); MS.paint_strike(im, ci(old), row['cy'], rng); MS.paint_fill(im, ci(intended), row['cy'], rng.uniform(.82, 1), rng); exp = 'accept'
                elif k == 'double':
                    old = rng.choice([o for o in opts if o != intended]); MS.paint_fill(im, ci(old), row['cy'], rng.uniform(.8, 1), rng); MS.paint_fill(im, ci(intended), row['cy'], rng.uniform(.82, 1), rng); exp = 'hold'
                elif k == 'faint': MS.paint_fill(im, ci(intended), row['cy'], rng.uniform(.12, .38), rng); exp = 'hold'
                elif k == 'blank_declared': declare.add(u['no']); exp = 'blank'
                else: exp = 'blank_undeclared'
                if k != 'blank_declared' and rng.random() < MS.STRAY_DOT:
                    MS.paint_dot(im, ci(rng.choice([o for o in opts if o != intended])), row['cy'], rng)
                truth[u['no']] = {'kind': k, 'intended': intended if exp not in ('blank', 'blank_undeclared') else None, 'expect': exp, 'meant': intended if exp not in ('blank', 'blank_undeclared') else None}
        elif b['kind'] == 'bank':
            for u in units:
                right = str(kp[u['no']]['answer'])
                if rng.random() < ability: code = right
                else:
                    code = right
                    while code == right: code = A0.make_code(rng.randint(1, 10 ** width - 1), width)
                k = MS.pick(rng, MS.BANK_P); shown = code
                if k == 'code_slip':
                    i = rng.randrange(len(code)); d = rng.choice([x for x in '0123456789' if x != code[i]]); shown = code[:i] + d + code[i + 1:]
                if k == 'code_swap' and code[0] != code[1]: shown = code[1] + code[0]
                elif k == 'code_swap': k = 'code_ok'
                if k == 'blank_declared': declare.add(u['no'])
                for ri, row in enumerate(u['rows']):
                    if k == 'blank_declared': break
                    MS.paint_fill(im, row['cx'][int(shown[ri])], row['cy'], rng.uniform(.12, .38) if k == 'faint' else rng.uniform(.82, 1), rng)
                exp = {'code_ok': 'accept', 'code_slip': 'hold', 'code_swap': 'hold', 'blank_declared': 'blank', 'faint': 'hold'}[k]
                truth[u['no']] = {'kind': k, 'intended': code if exp == 'accept' else None, 'expect': exp, 'meant': code if exp != 'blank' else None}
        else:
            for u in units:
                k = MS.pick(rng, MS.HUMAN_P); keyans = kp[u['no']]['answer']; text = None
                if k == 'written':
                    if rng.random() < ability: text = str(int(keyans['value'])) if isinstance(keyans, dict) else str(keyans)
                    else: text = str(rng.randint(1, 99999)) if isinstance(keyans, dict) else str(rng.randint(1, 99))
                    MS.paint_human(im, u['box'], text, rng)
                if k == 'blank_declared': declare.add(u['no'])
                truth[u['no']] = {'kind': 'human_' + k, 'intended': 'WRITTEN' if k == 'written' else None, 'expect': 'accept' if k == 'written' else ('blank' if k == 'blank_declared' else 'blank_undeclared'), 'meant': text}
        for q in b['closure']:
            if q['no'] in declare: MS.paint_fill(im, q['cx'], q['cy'], rng.uniform(.82, 1), rng)
    return [MS.scan(im, rng) for im in ims], truth

def true_score(key, layout, truth, mode='proportional'):
    """Plain scorer for the truth: what the student meant against the key. Independent of the tool's grade_places."""
    kp = G.key_places(key); lp = G.layout_places(layout); tot = 0.0; mx = 0.0
    byitem = collections.defaultdict(list)
    for u, k in kp.items(): byitem[k['item']].append(u)
    for pos, us in byitem.items():
        w = len({G._unit_sort(u)[0] for u in us}); mx += w; hit = []
        for u in us:
            m = truth[u]['meant']; a = kp[u]['answer']
            if m is None: hit.append(0)
            elif lp[u]['kind'] == 'human':
                hit.append(int(abs(float(m) - a['value']) <= a.get('tolerance', 0)) if isinstance(a, dict) else int(m == a))
            else: hit.append(int(str(m) == str(a)))
        tot += (w * all(hit)) if mode == 'all' else w * sum(hit) / len(us)
    return tot, mx

def run(n, seed_base, orders=('chapter', 'type')):
    res = {}
    for order in orders:
        stem = ORDERS[order]; key = G.load_json(os.path.join(PAPERS, stem + '_key.json')); layout = G.load_json(os.path.join(PAPERS, stem + '_sheet_layout.json'))
        assert not G.check_pair(key, layout)
        work = tempfile.mkdtemp(prefix='sen0401_grm_')
        try:
            blank = [np.array(Image.open(p).convert('L')) for p in A0.rasterise(os.path.join(PAPERS, stem + '_sheet.pdf'), os.path.join(work, 'b'))]
            c = collections.Counter(); sheets = []; sizes = []; err_prov = []; per_unit_silent = 0; doubts_total = 0; places_total = 0; leftovers = []
            for i in range(n):
                rng = random.Random(seed_base + i); ability = rng.choice([.3, .5, .7, .85, .95])
                ims, truth = student_keyed(layout, key, blank, rng, ability)
                got = G.read_images(ims, layout)
                if got is None: c['not_registered'] += 1; continue
                reads, bst, held = got
                for mode in ('proportional', 'all'):
                    t, mx = true_score(key, layout, truth, mode)
                    # step 1: no entries at all
                    g0 = G.grade_places(key, layout, reads, mode=mode)
                    c['sheets_' + mode] += 1
                    if not (g0['lowest'] - 1e-6 <= t <= g0['highest'] + 1e-6): c['bounds_miss_' + mode] += 1; leftovers.append({'seed': seed_base + i, 'mode': mode, 'stage': 'bounds', 'true': t, 'lo': g0['lowest'], 'hi': g0['highest']})
                    # step 2: the instructor types the written places (what the student meant) but resolves nothing
                    typed = {u: truth[u]['meant'] for u, e in g0['units'].items() if e['kind'] == 'human' and truth[u]['meant'] is not None}
                    g1 = G.grade_places(key, layout, reads, typed=typed, mode=mode)
                    if not (g1['lowest'] - 1e-6 <= t <= g1['highest'] + 1e-6): c['bounds_miss_typed_' + mode] += 1; leftovers.append({'seed': seed_base + i, 'mode': mode, 'stage': 'typed', 'true': t, 'lo': g1['lowest'], 'hi': g1['highest']})
                    if g1['status'] == 'FINAL':
                        c['final_without_resolution_' + mode] += 1
                        if abs(g1['lowest'] - t) > 1e-6: c['final_wrong_' + mode] += 1; leftovers.append({'seed': seed_base + i, 'mode': mode, 'stage': 'final', 'true': t, 'got': g1['lowest']})
                    # step 3: the instructor looks at the paper only where the list says and resolves it to what the student meant
                    res_map = {t_['unit']: (truth[t_['unit']]['meant'] or '') for t_ in g1['to_do'] if t_['task'] == 'resolve'}
                    g2 = G.grade_places(key, layout, reads, typed=typed, resolved=res_map, mode=mode)
                    left = [t_ for t_ in g2['to_do']]
                    if left: c['unresolved_after_resolution_' + mode] += 1
                    elif abs(g2['lowest'] - t) > 1e-6: c['end_to_end_wrong_' + mode] += 1; leftovers.append({'seed': seed_base + i, 'mode': mode, 'stage': 'end', 'true': t, 'got': g2['lowest']})
                    else: c['end_to_end_exact_' + mode] += 1
                    if mode == 'proportional':
                        err_prov.append(round(t - g1['lowest'], 4)); nres = sum(1 for t_ in g1['to_do'] if t_['task'] == 'resolve'); sizes.append(nres); doubts_total += nres
                        places_total += len(g1['units'])
                # unit-level: an accepted (unflagged, non-blank) read that differs from what the student meant
                for u, t_ in truth.items():
                    r = reads[u]
                    if G.layout_places(layout)[u]['kind'] == 'human': continue
                    if r['flag'] is None and r['value'] is not None and str(r['value']) != str(t_['meant']): per_unit_silent += 1
                    if r['flag'] is None and r['value'] is None and t_['meant'] is not None and r['flag'] != 'blank': pass
            c['units_accepted_but_not_what_was_meant'] = per_unit_silent
            res[order] = {'sheets': n, 'counters': dict(c), 'doubtful_places_per_sheet_mean': round(sum(sizes) / max(1, len(sizes)), 2), 'doubtful_places_per_sheet_max': max(sizes) if sizes else 0,
                          'doubtful_share_of_places_percent': round(100 * doubts_total / max(1, places_total), 2), 'sheets_with_no_doubtful_place': sum(1 for s in sizes if s == 0),
                          'mean_point_error_if_doubtful_counted_wrong': round(sum(err_prov) / max(1, len(err_prov)), 3), 'max_point_error_if_doubtful_counted_wrong': max(err_prov) if err_prov else 0,
                          'failures': leftovers[:20]}
        finally: shutil.rmtree(work, ignore_errors=True)
    return res

def main():
    a = argparse.ArgumentParser(); a.add_argument('--sheets', type=int, default=40); a.add_argument('--seed-base', type=int, default=41000); a.add_argument('--json'); a.add_argument('--without-g7', action='store_true', help='switch off the tool\'s cross-gap screens (to show their effect)')
    o = a.parse_args()
    if o.without_g7: G.extend_holds = lambda layout, out, bst, held: held
    r = run(o.sheets, o.seed_base)
    out = {'tool_version': G.VERSION, 'reader_version': G.R.VERSION, 'seed_base': o.seed_base, 'g7_cross_gap_screens': not o.without_g7, 'result': r}
    print(json.dumps(out, indent=1))
    if o.json: json.dump(out, open(o.json, 'w'), indent=1)
if __name__ == '__main__': main()
