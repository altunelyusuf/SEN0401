"""Check of the grading tool v1.0.0 (new file; no existing gate, test or threshold is edited). Prints PASS / FAIL per check and a SUMMARY line; exit 0 only when every check passes.
The checks use the key and layout files of the two orders of the midterm by their format, handmade read fixtures (no images), and synthetic sheets (no student data).
C1 pair check passes on both orders; C2 refuses mutated pairs; C3 grading logic on handmade reads with known answers (both orders); C4 score bounds and the doubtful list on handmade flagged reads;
C5 the command line end to end on synthetic sheets (PDF and PNG), outputs and exit codes; C6 item review flags a planted key mistake and nothing else; C7 measurement on a held-out seed block (criteria below);
C8 no committed file is edited. Usage: check.py [--sheets 100] [--seed-base 62000]"""
import copy, json, os, random, subprocess, sys, tempfile, shutil, argparse
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import sen0401_exam_grading_v1_0_0 as G
import sen0401_exam_grading_measure_v1_0_0 as M
A0 = G.A0
P = M.PAPERS; results = []
def rec(name, ok, detail): results.append(ok); print(('PASS  ' if ok else 'FAIL  ') + name + ': ' + detail)
def load(o):
    stem = M.ORDERS[o]; return G.load_json(os.path.join(P, stem + '_key.json')), G.load_json(os.path.join(P, stem + '_sheet_layout.json')), stem

def perfect_reads(key, layout):
    """Reads as the reader would print them for a student who marked exactly the key (written places: WRITTEN)."""
    kp = G.key_places(key); lp = G.layout_places(layout); r = {}
    for u, k in kp.items():
        r[u] = {'value': 'WRITTEN', 'flag': None} if lp[u]['kind'] == 'human' else {'value': str(k['answer']), 'flag': None}
    return r
def perfect_typed(key):
    return {u: (str(int(k['answer']['value'])) if isinstance(k['answer'], dict) else str(k['answer'])) for u, k in G.key_places(key).items() if k['type'] in ('NumericAnswer', 'CodeTrace')}

def c1():
    for o in ('chapter', 'type'):
        key, lay, _ = load(o); pr = G.check_pair(key, lay); rec('C1 pair check ' + o, not pr, 'problems=%s, places=%d, items=%d' % (pr, len(G.layout_places(lay)), len(key['items'])))

def c2():
    key, lay, _ = load('chapter'); cases = {}
    k = copy.deepcopy(key); k['items'] = [i for i in k['items'] if i['position'] != 1]; cases['key entry missing'] = (k, lay)
    k = copy.deepcopy(key); k['items'][0]['answer'] = 'E'; cases['letter outside the options'] = (k, lay)
    k = copy.deepcopy(key); [i for i in k['items'] if i['type'] == 'FillBlankGroup'][0]['answer']['13'] = '58'; cases['bad check digit'] = (k, lay)
    k = copy.deepcopy(key); [i for i in k['items'] if i['type'] == 'Ordering'][0]['answer']['8a'] = 5; cases['ordering not a permutation'] = (k, lay)
    k = copy.deepcopy(key); k['items'].append({'position': 99, 'type': 'ChoiceFour', 'answer': 'A', 'chapters': [1]}); cases['key place with no sheet place'] = (k, lay)
    k2, l2, _ = load('type'); cases['key of one order with the layout of the other'] = (key, l2)
    for n, (kk, ll) in cases.items():
        pr = G.check_pair(kk, ll); rec('C2 refuse: ' + n, bool(pr), '%d problems, first: %s' % (len(pr), pr[0] if pr else None))
    # the command line refuses with exit 2 and grades nothing
    d = tempfile.mkdtemp(prefix='sen0401_gck_')
    try:
        kb = copy.deepcopy(key); kb['items'][0]['answer'] = 'E'; kf = os.path.join(d, 'k.json'); json.dump(kb, open(kf, 'w'))
        lf = os.path.join(P, M.ORDERS['chapter'] + '_sheet_layout.json'); os.makedirs(os.path.join(d, 'scans'))
        rc = G.main(['grade', '--key', kf, '--layout', lf, '--scan-dir', os.path.join(d, 'scans'), '--out', os.path.join(d, 'out')])
        rec('C2 command line refuses a bad pair', rc == 2 and not os.path.exists(os.path.join(d, 'out')), 'exit %s, output folder exists: %s' % (rc, os.path.exists(os.path.join(d, 'out'))))
    finally: shutil.rmtree(d, ignore_errors=True)

def c3():
    for o in ('chapter', 'type'):
        key, lay, _ = load(o); reads = perfect_reads(key, lay); typed = perfect_typed(key)
        g = G.grade_places(key, lay, reads, typed=typed)
        rec('C3 perfect sheet ' + o, g['status'] == 'FINAL' and g['lowest'] == 24 == g['max'], 'status %s lowest %s max %s' % (g['status'], g['lowest'], g['max']))
        g = G.grade_places(key, lay, reads)
        rec('C3 written places not entered are never final ' + o, g['status'] == 'PROVISIONAL' and g['highest'] == 24 and all(t['task'] == 'enter' for t in g['to_do']) and g['lowest'] < 24,
            'status %s, lowest %s, highest %s, to enter %d' % (g['status'], g['lowest'], g['highest'], len(g['to_do'])))
        # all choice-like wrong, nothing blank: shift every letter to a different option
        wr = {}
        for u, k in G.key_places(key).items():
            L = G.layout_places(lay)[u]
            if L['kind'] in ('choice', 'match'): wr[u] = {'value': [x for x in L['opts'] if x != k['answer']][0], 'flag': None}
            elif L['kind'] == 'order': wr[u] = {'value': [x for x in L['opts'] if x != str(k['answer'])][0], 'flag': None}
            elif L['kind'] == 'bank': wr[u] = {'value': A0.make_code(7, 1) if len(k['answer']) == 2 else k['answer'][::-1], 'flag': None}
            else: wr[u] = {'value': 'WRITTEN', 'flag': None}
        tw = {u: '0' for u in perfect_typed(key)}
        g = G.grade_places(key, lay, wr, typed=tw)
        rec('C3 all-wrong sheet ' + o, g['status'] == 'FINAL' and g['lowest'] == 0, 'status %s lowest %s' % (g['status'], g['lowest']))
        blank = {u: {'value': None, 'flag': 'blank'} for u in reads}
        g = G.grade_places(key, lay, blank)
        rec('C3 empty sheet ' + o, g['status'] == 'FINAL' and g['lowest'] == 0, 'status %s lowest %s' % (g['status'], g['lowest']))
    # partial credit on a multi-place item, both modes, on the chapter order: item 10 (four match rows), 2 of 4 right
    key, lay, _ = load('chapter'); reads = perfect_reads(key, lay); typed = perfect_typed(key)
    for u in ('10a', '10b'): reads[u] = {'value': 'A' if key['items'][9]['answer'][u] != 'A' else 'B', 'flag': None}
    gp = G.grade_places(key, lay, reads, typed=typed); ga = G.grade_places(key, lay, reads, typed=typed, mode='all')
    rec('C3 partial credit: 2 of 4 match rows', abs(gp['lowest'] - 23.5) < 1e-9 and ga['lowest'] == 23, 'proportional %s (expect 23.5), all-or-nothing %s (expect 23)' % (gp['lowest'], ga['lowest']))
    w = G.grade_places(key, lay, perfect_reads(key, lay), typed=typed, weights={1: 3})
    rec('C3 weights parameter', w['max'] == 26 and w['lowest'] == 26, 'max %s lowest %s (item 1 weight 3)' % (w['max'], w['lowest']))
    # numeric tolerance and trace
    kn = {'value': 100, 'unit': 'u', 'tolerance': 2}
    tests = [(kn, '100', True), (kn, '102', True), (kn, '103', False), (kn, ' 99 ', True), (kn, '', False), (kn, 'abc', False), ('12', '12', True), ('12', '21', False), ('12', ' 12', True)]
    bad = [(a, b, e) for a, b, e in tests if G.judge_typed(a, b) != e]
    rec('C3 typed answers judged against the key (tolerance, trace)', not bad, '%d cases, wrong: %s' % (len(tests), bad))

def c4():
    key, lay, _ = load('chapter'); reads = perfect_reads(key, lay); typed = perfect_typed(key)
    reads['1'] = {'value': None, 'flag': 'double'}; reads['5'] = {'value': 'D', 'flag': 'held-block'}; reads['13'] = {'value': '58', 'flag': 'check-digit'}; reads['9'] = {'value': 'A', 'flag': None}
    g = G.grade_places(key, lay, reads, typed=typed)
    ok = g['status'] == 'PROVISIONAL' and g['lowest'] == 24 - 3 - 1 + 0 and g['highest'] == 24 - 1
    # lowest: places 1, 5, 13 counted 0 (3 points) and 9 wrong (key C, read A) -> 20; highest: 1, 5, 13 counted right -> 23
    rec('C4 bounds with doubtful places', ok and g['lowest'] == 20 and g['highest'] == 23, 'lowest %s (expect 20) highest %s (expect 23) status %s' % (g['lowest'], g['highest'], g['status']))
    rec('C4 doubtful list is exactly the flagged places', sorted(t['unit'] for t in g['to_do']) == ['1', '13', '5'] and all(t['task'] == 'resolve' for t in g['to_do']), 'list %s' % [t['unit'] for t in g['to_do']])
    g2 = G.grade_places(key, lay, reads, typed=typed, resolved={'1': key['items'][0]['answer'], '5': 'A', '13': G.key_places(key)['13']['answer']})
    rec('C4 resolution makes the grade final', g2['status'] == 'FINAL' and g2['lowest'] == 22 and not g2['to_do'], 'status %s lowest %s (expect 22: place 5 resolved wrong, 9 wrong)' % (g2['status'], g2['lowest']))
    g3 = G.grade_places(key, lay, reads, typed=typed, resolved={'1': 'A', '5': 'D', '13': '59', '12': 'C'})
    rec('C4 override of an accepted read is listed', g3['overrides'] == ['12'], 'overrides %s' % g3['overrides'])
    b = perfect_reads(key, lay); b['2'] = {'value': None, 'flag': 'blank'}
    g4 = G.grade_places(key, lay, b, typed=typed)
    rec('C4 typed answer on a box the reader sees empty is doubtful', g4['units']['2']['status'] == 'doubtful' and g4['units']['2']['why'] == 'entry-on-blank' and g4['status'] == 'PROVISIONAL', 'status of place 2: %s / %s' % (g4['units']['2']['status'], g4['units']['2'].get('why')))
    r = G.reading_check(lay, {u: {'value': None, 'flag': 'blank'} for u in reads}, [{'undeclared_blank': []}] * 3, [], lay['pages'], True)
    rec('C4 reading check warns on an empty sheet and a wrong page count', any('blank share' in n for n in r['notes']) and any('page count' in n for n in G.reading_check(lay, reads, [{'undeclared_blank': []}], [], 1, True)['notes']), 'notes %s' % r['notes'])

def make_sheets(order, n, seed, outdir):
    key, lay, stem = load(order); work = tempfile.mkdtemp(prefix='sen0401_gckb_'); truth_all = {}
    try:
        blank = [np.array(Image.open(p).convert('L')) for p in A0.rasterise(os.path.join(P, stem + '_sheet.pdf'), os.path.join(work, 'b'))]
        for i in range(n):
            rng = random.Random(seed + i); ims, tr = M.student_keyed(lay, key, blank, rng, rng.choice([.5, .9]))
            lab = 'S%03d' % i; truth_all[lab] = tr
            if i == 0:
                pil = [Image.fromarray(im) for im in ims]; pil[0].save(os.path.join(outdir, lab + '.pdf'), save_all=True, append_images=pil[1:], resolution=A0.DPI)
            else:
                for p, im in enumerate(ims): Image.fromarray(im).save(os.path.join(outdir, '%s_p%d.png' % (lab, p + 1)))
    finally: shutil.rmtree(work, ignore_errors=True)
    return truth_all

def c5():
    key, lay, stem = load('chapter'); d = tempfile.mkdtemp(prefix='sen0401_gck_')
    try:
        scans = os.path.join(d, 'scans'); os.makedirs(scans); truth = make_sheets('chapter', 4, 63000, scans)
        # a sheet with a missing page: only page 1 of S002 is kept
        os.remove(os.path.join(scans, 'S002_p2.png'))
        kf = os.path.join(P, stem + '_key.json'); lf = os.path.join(P, stem + '_sheet_layout.json'); out = os.path.join(d, 'out')
        rc = G.main(['grade', '--key', kf, '--layout', lf, '--scan-dir', scans, '--out', out])
        rep = G.load_json(os.path.join(out, 'grading_report.json')); st = {s['label']: s['status'] for s in rep['sheets']}
        files = sorted(os.listdir(out))
        rec('C5 command line on 4 synthetic sheets (one PDF, three PNG sets, one with a missing page)', rc == 0 and files == ['grades.csv', 'grading_report.json', 'worklist.csv'] and st['S002'] == 'NOT_GRADED' and all(st[k] in ('FINAL', 'PROVISIONAL') for k in ('S000', 'S001', 'S003')),
            'exit %s, files %s, statuses %s' % (rc, files, st))
        # every graded sheet: bounds contain the true score (plain scorer of the measurement)
        okb = True; det = []
        for s in rep['sheets']:
            if s['status'] == 'NOT_GRADED': continue
            t, _ = M.true_score(key, lay, truth[s['label']]); inb = s['lowest'] - 1e-6 <= t <= s['highest'] + 1e-6; okb &= inb; det.append((s['label'], s['lowest'], t, s['highest']))
        rec('C5 the printed bounds contain the true score of each graded sheet', okb, str(det))
        # entries file: the instructor types the written answers and resolves the doubtful places
        ent = {}
        for s in rep['sheets']:
            if s['status'] == 'NOT_GRADED': continue
            tr = truth[s['label']]
            ent[s['label']] = {'typed': {u: tr[u]['meant'] for u, e in s['units'].items() if e['kind'] == 'human' and tr[u]['meant'] is not None},
                               'resolved': {t['unit']: (tr[t['unit']]['meant'] or '') for t in s['to_do'] if t['task'] == 'resolve'}}
        ef = os.path.join(d, 'entries.json'); json.dump(ent, open(ef, 'w'))
        out2 = os.path.join(d, 'out2'); rc2 = G.main(['grade', '--key', kf, '--layout', lf, '--scan-dir', scans, '--entries', ef, '--out', out2])
        rep2 = G.load_json(os.path.join(out2, 'grading_report.json')); good = True; det = []
        for s in rep2['sheets']:
            if s['status'] == 'NOT_GRADED': continue
            t, _ = M.true_score(key, lay, truth[s['label']]); good &= (s['status'] == 'FINAL' and abs(s['lowest'] - t) < 1e-6); det.append((s['label'], s['status'], s['lowest'], t))
        rec('C5 with the instructor entries the grades are final and equal the true scores', rc2 == 0 and good, str(det))
    finally: shutil.rmtree(d, ignore_errors=True)

def c6():
    key, lay, stem = load('chapter'); work = tempfile.mkdtemp(prefix='sen0401_gckc_')
    try:
        blank = [np.array(Image.open(p).convert('L')) for p in A0.rasterise(os.path.join(P, stem + '_sheet.pdf'), os.path.join(work, 'b'))]
        reads = []
        for i in range(36):
            rng = random.Random(64000 + i); ims, tr = M.student_keyed(lay, key, blank, rng, .9); got = G.read_images(ims, lay); reads.append(got[0])
    finally: shutil.rmtree(work, ignore_errors=True)
    def review(k):
        sheets = [G.grade_places(k, lay, r, typed=perfect_typed(k)) for r in reads]; return [x['item'] for x in G.item_review(sheets, k, lay) if x['review']]
    clean = review(key); k = copy.deepcopy(key); old = k['items'][0]['answer']; k['items'][0]['answer'] = [x for x in 'ABCD' if x != old][0]
    planted = review(k)
    rec('C6 item review: clean key lists nothing, planted wrong key on item 1 is listed', clean == [] and planted == [1], 'clean %s, planted %s (36 sheets of ability 0.9)' % (clean, planted))

def c7(n, seed):
    r = M.run(n, seed); ok = True; det = []
    for o, v in r.items():
        c = v['counters']; n_ok = n
        crit = {'no sheet unregistered': c.get('not_registered', 0) == 0,
                'bounds always contain the true score (4 counters)': not any(c.get(k, 0) for k in ('bounds_miss_proportional', 'bounds_miss_typed_proportional', 'bounds_miss_all', 'bounds_miss_typed_all')),
                'no accepted unit differs from what the student meant': c.get('units_accepted_but_not_what_was_meant', 0) == 0,
                'every sheet declared FINAL without any resolution equals the true score': not any(c.get(k, 0) for k in ('final_wrong_proportional', 'final_wrong_all')),
                'after the instructor resolves the listed places every grade equals the true score (both modes)': c.get('end_to_end_exact_proportional', 0) == n and c.get('end_to_end_exact_all', 0) == n and not c.get('unresolved_after_resolution_proportional', 0),
                'doubtful share of places at or below 25 percent (the reader limit)': v['doubtful_share_of_places_percent'] <= 25}
        for k, b in crit.items(): ok &= b; det.append('%s %s: %s' % (o, k, 'yes' if b else 'NO'))
        det.append('%s: sheets %d, doubtful places per sheet mean %s max %s, share %s percent, sheets final without resolution (proportional) %s, (all-or-nothing) %s, registration failures %s' % (
            o, v['sheets'], v['doubtful_places_per_sheet_mean'], v['doubtful_places_per_sheet_max'], v['doubtful_share_of_places_percent'], c.get('final_without_resolution_proportional', 0), c.get('final_without_resolution_all', 0), c.get('not_registered', 0)))
    rec('C7 measurement on held-out block %d-%d, %d sheets of each order' % (seed, seed + n - 1, n), ok, '\n        ' + '\n        '.join(det))

def c8():
    root = subprocess.run(['git', '-C', HERE, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    mod = subprocess.run(['git', '-C', root, 'status', '--porcelain', '--', '08-tooling', '04-assessment', '02-textbook', '03-materials', '07-lineage', '01-outcomes'], capture_output=True, text=True).stdout.splitlines()
    edited = [l for l in mod if l[:2].strip() in ('M', 'D', 'R', 'MM', 'AM') or l[1] in 'MD']
    rec('C8 no committed file edited (git status shows no modified or deleted tracked file)', not edited, 'modified/deleted: %s' % edited)

if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('--sheets', type=int, default=100); a.add_argument('--seed-base', type=int, default=62000); o = a.parse_args()
    c1(); c2(); c3(); c4(); c5(); c6(); c7(o.sheets, o.seed_base); c8()
    print('SUMMARY %d of %d checks PASS' % (sum(results), len(results)))
    sys.exit(0 if all(results) else 1)
