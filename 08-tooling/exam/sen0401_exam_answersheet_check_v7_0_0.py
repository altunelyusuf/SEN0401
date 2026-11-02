"""Check of the v7 answer sheet (ONE A4 page, choice-type answers only, five alternatives) and the reader v1.4.0. New file; the v6.1.0 check stays unchanged. Holds no question and no answer.
Prints PASS / FAIL per check; exit 1 on any FAIL. Given: the folder with the sheet PDF and its layout JSON (same stem), the stem, and a key JSON of which ONLY the labels and item types are read (the unit shape of the proof layout: the v6 key).
  K1  no committed file of the exam folder is edited (git status shows only new files)
  L1  one A4 page; four corner marks; no tips page, no number box, no answer line, no bonus line
  L2  every unit of the unit list has its place: the rows of the sheet are exactly the labels of the shape (7 choice, 1 ordering of 5 rows, 2 matchings of 4 rows, 3 fill-in groups of 2 blanks); five bubbles per place with the right alternatives (A-E, 1-5)
  L3  position-exact: every bubble inside the margins, no two bubbles overlap, no block area overlaps another, every row label printed at its row
  L4  block types are the reader's own and each sub-question is one block (the block sizes equal the groups of the shape)
  L5a a blank sheet registers and the reader v1.4.0 invents no value;  L5b the same with every 'left blank' bubble filled reads blank
  L6  the form code is valid by the check digit
  L7  the 'left blank' row of every block ends inside its column or at most half the gutter beyond it
  L8  the printed sentences: each at most 25 words; the answers on the question pages count; the sheet is for fast reading; if they differ the question pages count; two filled bubbles in one place count as no answer; no word about points taken away, bonus or tips; 10 point or larger
  L9  every unit fits one page (capacity measured); overflow is refused, never clipped; a number box (human), a bank-digit unit, a four-option unit and a repeated label are refused
  R   the reader reads page 1 only: a layout of two pages is refused; read_pdf equals the page-1 raster reading; control: ink in a row changes the reading
  D   fixtures where the sheet and the question page differ: the rule (the page counts; an empty page takes the sheet) with the v7 scoring rule (right answer its points, wrong or blank 0), against hand arithmetic; two filled bubbles read as no answer
  M   the reader measure on N synthetic sheets at each of two seed bases: 0 registration failures, 0 silent wrong, 0 missed, 0 empty-not-flagged, held share at most 25 percent
Usage: check_v7.py DIR --tag STEM --key KEY.json [--sheets 40] [--seed-bases 57000,58000] [--log FILE]   (the log is created new; an existing log is refused)"""
import argparse, json, os, random, re, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import pdfplumber
import sen0401_exam_answersheet_v1_0_0 as A0
import sen0401_exam_answersheet_v1_4_0 as A
import sen0401_exam_answersheet_v7_0_0 as V
import sen0401_exam_answersheet_v7_build_v1_0_0 as B
import sen0401_exam_answersheet_measure_v7_0_0 as M
import sen0401_exam_scoring_v1_0_0 as SC            # only its resolve() rule (the question page counts; an empty page takes the sheet) and DOUBLE are used; its penalty tables are NOT used
ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--tag', required=True); ap.add_argument('--sheets', type=int, default=40); ap.add_argument('--seed-bases', default='57000,58000'); ap.add_argument('--key', required=True); ap.add_argument('--log'); args = ap.parse_args()
if args.log and os.path.exists(args.log): print('REFUSED: the log file exists and is never appended to: ' + args.log); sys.exit(2)
res = []
def rep(name, ok, detail=''):
    res.append(bool(ok)); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail), flush=True)
g = subprocess.run(['git', '-C', HERE, 'status', '--porcelain', '--', '.'], capture_output=True, text=True)
bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
rep('K1 no committed file of the exam folder is edited (git status of 08-tooling/exam shows only new files)', g.returncode == 0 and not bad, ' '.join(bad[:5]))
tag = args.tag; pdf = os.path.join(args.dir, tag + '.pdf'); layp = os.path.join(args.dir, tag + '_layout.json'); lay = json.load(open(layp))
shape = B.shape_from_key(args.key)
want = [l for e in shape for l in e['labels']]
work = tempfile.mkdtemp(prefix='sen0401_as_chk7_')
try:
    pi = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', pi).group(1)); size = re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', pi)
    with pdfplumber.open(pdf) as d:
        p1 = d.pages[0]; w1 = p1.extract_words(); sizes1 = [c['size'] for c in p1.chars]; t1 = ' '.join(w['text'] for w in w1)
    has_extra = any('box' in u for b in lay['blocks'] for u in b['units']) or lay.get('lines') or any(u['kind'] in ('human', 'bank') for b in lay['blocks'] for u in b['units'])
    rep('L1 one A4 page (%s x %s pt), four corner marks, no tips page, no number box, no answer line, no bonus line' % (size.group(1), size.group(2)), pages == 1 and lay['pages'] == 1 and abs(float(size.group(1)) - 595.28) < .5 and len(lay['fiducials']) == 4 and all(f['page'] == 0 for f in lay['fiducials']) and not has_extra and lay['reader_pages'] == [0],
        'pages %d, fiducials %d' % (pages, len(lay['fiducials'])))
    sheetplaces = [u['no'] for b in lay['blocks'] for u in b['units']]
    nopt = {u['no']: (u['rows'][0]['opts'], len(u['rows'][0]['cx']), len(u['rows'])) for b in lay['blocks'] for u in b['units']}
    five = all(n == 5 and r == 1 and o in ('ABCDE', '12345') for o, n, r in nopt.values())
    kinds = {}
    for b in lay['blocks']:
        for u in b['units']: kinds[u['kind']] = kinds.get(u['kind'], 0) + 1
    rep('L2 every unit has its place: %d rows = the %d labels of the shape %s; five bubbles per place with the alternatives A-E or 1-5; rows by kind %s' % (len(sheetplaces), len(want), '(7 choice, ordering 5, matching 4+4, fill-in 3x2)', kinds),
        sorted(sheetplaces) == sorted(want) and len(set(sheetplaces)) == len(sheetplaces) and five and kinds == {'choice': 7, 'order': 5, 'match': 8, 'fill': 6},
        'only in shape %s, only on sheet %s, five-way %s' % (sorted(set(want) - set(sheetplaces)), sorted(set(sheetplaces) - set(want)), five))
    PW, PH = lay['page_pt']; MARG = A0.MARG; pts = []; inside = True; rects = []
    for b in lay['blocks']:
        rects.append((b['x'], b['y'], b['x'] + A0.COLW, b['y'] + b['h'], 'block%d' % b['id']))
        for u in b['units']:
            for r in u['rows']:
                for cx in r['cx']:
                    pts.append((cx, r['cy'])); inside &= (MARG - 1 <= cx - A0.BR and cx + A0.BR <= PW - MARG + 1 and MARG - 1 <= r['cy'] - A0.BR and r['cy'] + A0.BR <= PH - MARG + 1)
        for q in b['closure']: pts.append((q['cx'], q['cy'])); inside &= (q['cx'] + A0.BR <= PW - MARG + 1)
    overl = sum(1 for i in range(len(pts)) for j in range(i + 1, len(pts)) if ((pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2) ** .5 < 2 * A0.BR + 1)
    rov = [(a[4], b[4]) for i, a in enumerate(rects) for b in rects[i + 1:] if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]]
    missing = []
    for b in lay['blocks']:
        for u in b['units']:
            cy = u['rows'][0]['cy']
            if not any(w['text'] == u['no'] and w['top'] - 2 <= cy <= w['bottom'] + 2 for w in w1): missing.append(u['no'])
    rep('L3 position-exact: bubbles inside the margins, no two bubbles overlap, no block area overlaps another, every row label printed at its row', inside and overl == 0 and not rov and not missing,
        'inside %s, bubble overlaps %d, area overlaps %s, labels not found at their row %s' % (inside, overl, rov, missing[:6]))
    colw = A0.COLW; over = [b['id'] for b in lay['blocks'] if b['closure'][-1]['cx'] + A0.BR + 3 + 6.5 * len(b['closure'][-1]['no']) > b['x'] + colw + A0.COLGAP / 2]
    rep('L7 the closure row ("left blank") of every block ends inside its column or at most half the gutter (10 pt) beyond it', not over, 'blocks beyond column + 10 pt: %s' % over)
    sizes = [(b['kind'], len(b['units'])) for b in lay['blocks']]; groups = [len(e['labels']) for e in shape]
    expect_sizes = []
    for e in shape:
        k = V.TYPE_KIND[e['type']]; n = len(e['labels'])
        while n > 0: expect_sizes.append((k, min(n, V.BLOCK_MAX[k]))); n -= V.BLOCK_MAX[k]
    rep('L4 block types are the reader\'s own (choice, match, order, fill) and each sub-question is one block: %s' % sizes, {k for k, _ in sizes} <= {'choice', 'match', 'order', 'fill'} and sizes == expect_sizes, 'expected %s' % expect_sizes)
    png = A0.rasterise(pdf, os.path.join(work, 'blank')); img = np.array(Image.open(png[0]).convert('L')); reg = [A0.register(img, lay, 0)]
    o, bs, held = A.read_sheet_v7(reg, lay); flags = {k: v for k, v in o.items() if v['flag'] not in (None, 'blank')}; vals = {k: v['value'] for k, v in o.items() if v['value'] is not None}
    rep('L5a a completely blank sheet registers and the reader v1.4.0 invents no value', reg[0] is not None and not vals, 'rows %d, values %d, flags %d, held blocks %d' % (len(o), len(vals), len(flags), len(held)))
    img2 = img.copy(); rg = random.Random(5)
    for b_ in lay['blocks']:
        for q_ in b_['closure']: M.MS.paint_fill(img2, q_['cx'], q_['cy'], .95, rg)
    reg2 = [A0.register(img2, lay, 0)]; o2, bs2, held2 = A.read_sheet_v7(reg2, lay); fl2 = {k: v for k, v in o2.items() if v['flag'] not in (None, 'blank')}; v2 = {k: v['value'] for k, v in o2.items() if v['value'] is not None}
    rep('L5b a blank sheet with every "left blank" bubble filled reads blank (no value, no flag, no block held)', reg2[0] is not None and not fl2 and not v2 and not held2, 'rows %d, flags %d, values %d, held blocks %d' % (len(o2), len(fl2), len(v2), len(held2)))
    rep('L6 the form code %s passes the check digit' % lay['form_code'], A0.damm_valid(lay['form_code']), '')
    norm = lambda s: re.sub(r'\s+', ' ', s)
    need = ['The answers written on the question pages count.', 'This sheet is only for fast reading.', 'If the sheet and the question pages differ, the question pages count.', 'Two filled bubbles in one place count as no answer.']
    miss = [n for n in need if n not in norm(t1)]
    longest = max(len(s.split()) for s in V.PRINTED_SENTENCES); sent_missing = [s for s in V.PRINTED_SENTENCES if norm(s) not in norm(t1)]
    forbidden = ['penalt', 'deduct', 'minus', 'taken away', 'take away', 'bonus', 'tip', 'cost', 'lose', 'lost', 'points off', 'subtract', 'floor', 'fraction']
    found_bad = [f for f in forbidden if f in t1.lower()]
    rep('L8 the printed sentences (%d, longest %d words, limit 25) are on the page: the four required statements present, no word about points taken away, bonus or tips (%s), all type 10 point or larger (smallest %.1f)' % (len(V.PRINTED_SENTENCES), longest, 'none found' if not found_bad else found_bad, min(sizes1)),
        not miss and not sent_missing and longest <= 25 and not found_bad and min(sizes1) >= 10 - 1e-6, 'missing: %s %s' % (miss, sent_missing))
    # L9
    ok = {}; spec0 = dict(lay['spec'])
    many = dict(spec0); many['units'] = [dict(u, no=u['no'] + 'x%d' % i) for i in range(5) for u in spec0['units']]
    try: V.build_layout(many); ok['too many units refused'] = False
    except V.SheetOverflow: ok['too many units refused'] = True
    for name, u in (('number box (human) refused', {'no': 'q1', 'kind': 'human', 'cells': 5}), ('bank-digit unit refused', {'no': 'q1', 'kind': 'bank', 'digits': 2}), ('four-option unit refused', {'no': 'q1', 'kind': 'choice', 'opts': 'ABCD'})):
        s_ = dict(spec0); s_['units'] = list(spec0['units']) + [u]
        try: V.build_layout(s_); ok[name] = False
        except V.SheetError: ok[name] = True
    s_ = dict(spec0); s_['units'] = list(spec0['units']) + [dict(spec0['units'][0])]
    try: V.build_layout(s_); ok['repeated label refused'] = False
    except V.SheetError: ok['repeated label refused'] = True
    try: V.units_from_list([{'type': 'number', 'labels': ['9a']}]); ok['unit type number refused'] = False
    except V.SheetError: ok['unit type number refused'] = True
    cap = 0
    while True:
        s_ = dict(spec0); s_['units'] = V.units_from_list([{'type': 'choice', 'labels': ['c%d' % i for i in range(cap + 1)]}]); s_['form_code'] = lay['form_code']
        try: V.build_layout(s_)
        except V.SheetOverflow: break
        cap += 1
        if cap > 400: break
    print('     measured capacity: %d choice rows alone fit the page (paired lines); the proof shape has %d rows and uses %.0f of %.0f pt of column height' % (cap, len(sheetplaces), lay['free_height_pt']['page_used'], lay['free_height_pt']['page_columns']))
    rep('L9 every unit of the v6 key shape fits one page (%d rows, no overflow) and overflow is refused, never clipped; units the sheet does not carry are refused' % len(sheetplaces), all(ok.values()) and 5 < cap < 400, str(ok))
    # R
    blank1 = [np.array(Image.open(png[0]).convert('L'))]
    two = dict(lay); two['pages'] = 2; two['reader_pages'] = [0, 1]
    try: A.read_sheet_v7([blank1[0], blank1[0]], two); refused = False
    except ValueError: refused = True
    rng = random.Random(81000); ims, truth = M.MS.student(lay, blank1, rng); base_ = A.read_sheet_v7([A0.register(ims[0], lay, 0)], lay)[0]; cz = ims[0].copy(); ub = lay['blocks'][0]['units'][0]['rows'][0]
    for cx in ub['cx']: M.MS.paint_fill(cz, cx, ub['cy'], .95, rng)
    ctrl = A.read_sheet_v7([A0.register(cz, lay, 0)], lay)[0]
    rd = A.read_pdf(pdf, lay, work); out_pdf = A.read_sheet_v7(reg, lay)[0]
    rep('R0 control of the test: ink inside a bubble row DOES change the reading', ctrl != base_, '')
    rep('R the reader v1.4.0 reads page 1 only: a two-page layout is refused; read_pdf equals the page-1 raster reading, every mark provisional (legal copy: %s)' % A.LEGAL_COPY, refused and rd is not None and rd['pages_read'] == [0] and all(v['status'] == 'provisional' for v in rd['marks'].values()) and {k: v['mark'] for k, v in rd['marks'].items()} == {k: v['mark'] for k, v in A.provisional(out_pdf).items()}, '')
    # D: sheet and question page differ
    rngk = random.Random(7071); labels = sheetplaces; kind_of = {u['no']: u for b in lay['blocks'] for u in b['units']}
    keyans = {l: rngk.choice(kind_of[l]['rows'][0]['opts']) for l in labels}; pts_ = {l: 1 + (i % 4) for i, l in enumerate(labels)}      # synthetic key: random letters, 1 to 4 points per place
    score7 = lambda marks: sum(pts_[l] for l in labels if marks.get(l) == keyans[l])                                                    # the v7 rule: a right answer its points, wrong or blank 0
    full = sum(pts_.values())
    def other(l, cur): return [o for o in kind_of[l]['rows'][0]['opts'] if o != cur][0]
    def paint(answers, rng_):
        im = blank1[0].copy()
        for l, v in answers.items():
            row = kind_of[l]['rows'][0]
            if v == 'DOUBLE':
                M.MS.paint_fill(im, row['cx'][0], row['cy'], .95, rng_); M.MS.paint_fill(im, row['cx'][1], row['cy'], .95, rng_)
            else: M.MS.paint_fill(im, row['cx'][row['opts'].index(v)], row['cy'], .95, rng_)
        return im
    def read_marks(answers):
        r = [A0.register(paint(answers, random.Random(9)), lay, 0)]; out = A.read_sheet_v7(r, lay)[0]; prov = A.provisional(out); return {k: v['mark'] for k, v in prov.items()}, prov
    ch3 = [l for l in labels if kind_of[l]['kind'] == 'choice'][:3]; mt = [l for l in labels if kind_of[l]['kind'] == 'match'][0]; fl = [l for l in labels if kind_of[l]['kind'] == 'fill'][0]; od = [l for l in labels if kind_of[l]['kind'] == 'order'][0]
    sm, prov = read_marks(keyans)
    rep('D0 the reader reads painted fixture sheets back as provisional marks (every one of the %d places equal to what was painted)' % len(labels), sm == keyans and all(v['status'] == 'provisional' for v in prov.values()), '')
    r1_, _ = SC.resolve({}, sm); rep('D1 sheet all right, page empty -> the sheet counts (score %d of %d)' % (score7(r1_), full), score7(r1_) == full)
    pg = {l: other(l, keyans[l]) for l in ch3}; pg[mt] = SC.DOUBLE; pg[fl] = other(fl, keyans[fl]); pg[od] = keyans[od]
    r2_, s2_ = SC.resolve(pg, sm); exp2 = full - sum(pts_[l] for l in ch3) - pts_[mt] - pts_[fl]
    rep('D2 sheet all right; the page has 3 wrong choices, one place with two answers, one wrong fill-in, one right ordering step -> the page counts (score %d, hand arithmetic %d; no deduction: every lost place is 0)' % (score7(r2_), exp2), score7(r2_) == exp2 and s2_[od] == 'page')
    sheet_wins = score7({l: (sm[l]) for l in labels}); rep('D5 control of the fixture: if the sheet won over the page, D2 would score %d, not the expected %d' % (sheet_wins, exp2), sheet_wins != exp2)
    wrong_s = dict(keyans); wrong_s.update({l: other(l, keyans[l]) for l in ch3}); smw, provw = read_marks(wrong_s)
    r3_, _ = SC.resolve({l: keyans[l] for l in ch3}, smw); rep('D3 sheet shows 3 wrong choices, the page has them right -> the page counts (score %d of %d)' % (score7(r3_), full), score7(r3_) == full)
    r4_, _ = SC.resolve({}, smw); exp4 = full - sum(pts_[l] for l in ch3); rep('D4 the same sheet, page empty -> the sheet counts, the 3 wrong choices score 0 (score %d, hand arithmetic %d)' % (score7(r4_), exp4), score7(r4_) == exp4)
    dbl = dict(keyans); dbl[ch3[0]] = 'DOUBLE'; smd, provd = read_marks(dbl)
    rep('D6 two filled bubbles in one place read as no answer (mark None, flag double) and score 0 (the other places unchanged)', smd[ch3[0]] is None and provd[ch3[0]]['flag'] == 'double' and score7(SC.resolve({}, smd)[0]) == full - pts_[ch3[0]] and all(smd[l] == keyans[l] for l in labels if l != ch3[0]), '')
    for fl_, base in zip(['A', 'B'], [int(x) for x in args.seed_bases.split(',')]):
        ev = M.run(pdf, layp, args.sheets, base, True)
        wm, nv, pk = ev['with_methods'], ev['naive_reader'], ev['per_kind_with_methods']; share = ev['recoverable_rows_held_by_a_flag'] / max(1, ev['recoverable_rows'])
        print('     [seeds %d-%d] %d sheets, %d rows, registration failures %d' % (base, base + args.sheets - 1, ev['sheets'], ev['rows_scored'], ev['registration_failures']))
        print('     with the methods : %s' % json.dumps(wm, sort_keys=True)); print('     reader without them: %s' % json.dumps(nv, sort_keys=True))
        print('     recoverable rows %d, held for a person %d (%.1f percent) by flag kind %s' % (ev['recoverable_rows'], ev['recoverable_rows_held_by_a_flag'], 100 * share, ev['recoverable_rows_held_by_flag_kind']))
        for k, v in pk.items(): print('       %-22s with methods %-44s naive %s' % (k, json.dumps(v, sort_keys=True), json.dumps(ev['per_kind_naive'].get(k, {}), sort_keys=True)))
        if ev.get('failing_rows'): print('     failing rows: %s' % json.dumps(ev['failing_rows']))
        c = {'registration_failures_0': ev['registration_failures'] == 0, 'silent_wrong_0': wm.get('silent_wrong', 0) == 0, 'missed_0': wm.get('missed', 0) == 0, 'empty_not_flagged_0': wm.get('empty_not_flagged', 0) == 0, 'held_share_le_25_percent': share <= 0.25}
        rep('M reader v1.4.0 on %d synthetic sheets (seeds %d-%d): 0 registration failures, 0 silent wrong, 0 missed, 0 empty-not-flagged, held share <= 25 percent' % (args.sheets, base, base + args.sheets - 1), all(c.values()),
            'registration failures %d, silent_wrong %d, missed %d, empty_not_flagged %d, held share %.1f percent; failed %s' % (ev['registration_failures'], wm.get('silent_wrong', 0), wm.get('missed', 0), wm.get('empty_not_flagged', 0), 100 * share, [k for k, v in c.items() if not v]))
finally:
    shutil.rmtree(work, ignore_errors=True)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
