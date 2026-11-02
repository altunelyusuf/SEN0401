"""Check of the v6.1 answer sheet (page 1 of answers and one or more tips pages) and the reader v1.3.0 (new file, a copy of sen0401_exam_answersheet_check_v6_0_0.py, which stays unchanged; the changes are only those the tips pages need: L1 expects 1 + the number of tips pages, none of them with a bubble, box or corner mark; L9 reads the tips from all tips pages and compares the type size with a tolerance of 1e-6 pt (pdfplumber reports a 10 point font as 9.999999999999972 from the text matrix; the setFont size in the file is exactly 10); L10 asks that ONE tip longer than a page is refused and prints the number of tips pages the tips need; R blackens every tips page; the module is sen0401_exam_answersheet_v6_1_0.py; no other check is changed). Original docstring of v6.0.0: in the manner of sen0401_exam_answersheet_check_v5_0_0.py, which stays unchanged). Holds no question and no answer; the key is read at run time and nothing of it is printed except labels and points.
Prints PASS / FAIL per check; exit 1 on any FAIL. Given: the folder with the sheet PDF, its layout JSON and the key JSON (the same stem), the stem.
  K1 no committed file is edited (git status shows only new files)
  L1  two A4 pages; four corner marks on page 1 only; page 2 holds no bubble, no box and no corner mark (the tips page is not read)
  L2  every answer place of the key has a place on the sheet: the rows and boxes of the sheet units are exactly the key's answer places, and the answer lines are exactly the hand-marked parts (5a, 5b)
  L3  position-exact on page 1: every bubble, box and line inside the margins, no two bubbles overlap, no block or line area overlaps another, the label of every unit is printed at its row
  L4  block types are the reader's own (choice, match, order, bank, human) and each sub-question is one block
  L7  the 'left blank' row of every block ends inside its column or at most half the gutter beyond it
  L5a a completely blank sheet registers, the reader v1.3.0 invents no value;  L5b the same with every 'left blank' bubble filled reads blank (no value, no flag, no block held)
  L6  the form code is valid by the check digit and equals the key's
  L8  the printed sentences: the answers on the question pages count; the sheet is for fast reading; if they differ the question pages count; two filled bubbles count as no answer
  L9  the tips page: every tip's label and words are printed on page 2, all type is 10 point or larger on both pages, the scoring note is printed
  L10 overflow is refused, not clipped: too many units raise SheetOverflow; tips beyond page 2 raise SheetOverflow; the capacity of page 2 for tips is measured and printed
  R   the reader ignores page 2 and the answer lines: the same synthetic sheet read with ink scribbled over every answer line and with a black page 2 gives exactly the same reading; reading the PDF itself (read_pdf) equals reading its page-1 raster
  D   fixtures where the sheet and the question page differ: marks painted on the sheet, read by the reader v1.3.0 (provisional), resolved with the page marks by the rule (page counts), scored by the scoring module and compared with the independent hand arithmetic of the key's points
  M   the reader measure (sen0401_exam_answersheet_measure_v6_0_0.py) on N synthetic sheets: registration failures 0, silent wrong 0, missed 0, empty-not-flagged 0, held share at most 25 percent
Usage: check_v6.py DIR --tag STEM --key KEY.json [--sheets 40] [--seed-bases 57000,58000] [--log FILE]   (the log is created new; an existing log is refused)"""
import argparse, json, os, random, re, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import pdfplumber
import sen0401_exam_answersheet_v1_0_0 as A0
import sen0401_exam_answersheet_v1_3_0 as A
import sen0401_exam_answersheet_v6_1_0 as V
import sen0401_exam_answersheet_measure_v6_0_0 as M
import sen0401_exam_scoring_v1_0_0 as SC
ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--tag', required=True); ap.add_argument('--sheets', type=int, default=40); ap.add_argument('--seed-bases', default='57000,58000'); ap.add_argument('--key'); ap.add_argument('--log'); args = ap.parse_args()
if args.log and os.path.exists(args.log): print('REFUSED: the log file exists and is never appended to: ' + args.log); sys.exit(2)
res = []
def rep(name, ok, detail=''):
    res.append(bool(ok)); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail), flush=True)
g = subprocess.run(['git', '-C', HERE, 'status', '--porcelain', '--', '.'], capture_output=True, text=True)      # the exam folder only: other executors work in other folders of the repository at the same time
bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
rep('K1 no committed file of the exam folder is edited (git status of 08-tooling/exam shows only new files)', g.returncode == 0 and not bad, ' '.join(bad[:5]))
tag = args.tag; pdf = os.path.join(args.dir, tag + '.pdf'); layp = os.path.join(args.dir, tag + '_layout.json'); lay = json.load(open(layp))
if not args.key or not os.path.exists(args.key): print('FAIL  the key json (--key) is not found'); sys.exit(1)
key = json.load(open(args.key))
work = tempfile.mkdtemp(prefix='sen0401_as_chk6_')
try:
    pi = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', pi).group(1)); size = re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', pi)
    with pdfplumber.open(pdf) as d:
        p1 = d.pages[0]; tp_ = d.pages[1:]
        w1 = p1.extract_words(); w2 = [w for q in tp_ for w in q.extract_words()]; curves2 = sum(len(q.curves) + len(q.rects) for q in tp_); curves1 = len(p1.curves) + len(p1.rects)
        sizes1 = [c['size'] for c in p1.chars]; sizes2 = [c['size'] for q in tp_ for c in q.chars]; t1 = ' '.join(w['text'] for w in w1); t2 = ' '.join(w['text'] for w in w2)
    rep('L1 1 + %d tips page(s) = %d A4 pages (%s x %s pt); four corner marks, all on page 1; the tips pages hold no bubble, box or corner mark' % (len(lay['tips_pages']), 1 + len(lay['tips_pages']), size.group(1), size.group(2)), pages == 1 + len(lay['tips_pages']) and lay['pages'] == pages and abs(float(size.group(1)) - 595.28) < .5 and len(lay['fiducials']) == 4 and all(f['page'] == 0 for f in lay['fiducials']) and curves2 == 0 and curves1 > 50 and lay['reader_pages'] == [0],
        'pages %d, fiducials %d, shapes on the tips pages: %d, shapes on page 1: %d' % (pages, len(lay['fiducials']), curves2, curves1))
    keyplaces = set(); hand = set()
    for e in key['items']:
        if e['type'] == 'ShortExplanation': hand.add(e['label'])
        else: keyplaces |= set(e['answer'].keys())
    sheetplaces = [u['no'] for b in lay['blocks'] for u in b['units']]; linesplaces = [l['no'] for l in lay['lines']]
    rep('L2 every answer place of the key has a place: %d rows/boxes = the key\'s places, and %d answer lines = the hand-marked parts %s' % (len(keyplaces), len(linesplaces), sorted(hand)),
        set(sheetplaces) == keyplaces and len(sheetplaces) == len(set(sheetplaces)) and set(linesplaces) == hand and len(linesplaces) == len(set(linesplaces)),
        'only in key %s, only on sheet %s, lines %s' % (sorted(keyplaces - set(sheetplaces)), sorted(set(sheetplaces) - keyplaces), linesplaces))
    PW, PH = lay['page_pt']; MARG = A0.MARG; pts = []; inside = True; rects = []
    for b in lay['blocks']:
        rects.append((b['x'], b['y'], b['x'] + A0.COLW, b['y'] + b['h'], 'block%d' % b['id']))
        for u in b['units']:
            for r in u.get('rows', []):
                for cx in r['cx']:
                    pts.append((cx, r['cy'])); inside &= (MARG - 1 <= cx - A0.BR and cx + A0.BR <= PW - MARG + 1 and MARG - 1 <= r['cy'] - A0.BR and r['cy'] + A0.BR <= PH - MARG + 1)
            if 'box' in u:
                bx = u['box']; inside &= (MARG - 1 <= bx['x'] and bx['x'] + bx['w'] <= PW - MARG + 1 and bx['y'] >= MARG - 1 and bx['y'] + bx['h'] <= PH - MARG + 1)
        for q in b['closure']: pts.append((q['cx'], q['cy'])); inside &= (q['cx'] + A0.BR <= PW - MARG + 1)
    for l in lay['lines']:
        rects.append((l['x'], l['y'], l['x'] + l['w'], l['y'] + l['h'], 'lines' + l['no'])); inside &= (MARG - 1 <= l['x'] and l['x'] + l['w'] <= PW - MARG + 1 and l['ys'][-1] <= PH - MARG + 1)
    overl = sum(1 for i in range(len(pts)) for j in range(i + 1, len(pts)) if ((pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2) ** .5 < 2 * A0.BR + 1)
    rov = [(a[4], b[4]) for i, a in enumerate(rects) for b in rects[i + 1:] if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]]
    missing = []
    for b in lay['blocks']:
        for u in b['units']:
            cy = u['box']['y'] + u['box']['h'] / 2 if u['kind'] == 'human' else u['rows'][0]['cy']
            if not any(w['text'] == u['no'] and w['top'] - 2 <= cy <= w['bottom'] + 2 for w in w1): missing.append(u['no'])
    for l in lay['lines']:
        if not any(w['text'] == l['no'] and abs(w['top'] - l['y']) < 14 for w in w1): missing.append('lines ' + l['no'])
    rep('L3 position-exact on page 1: bubbles, boxes and lines inside the margins, no two bubbles overlap, no block or line area overlaps another, every label printed at its row', inside and overl == 0 and not rov and not missing,
        'inside %s, bubble overlaps %d, area overlaps %s, labels not found at their row %s' % (inside, overl, rov, missing[:6]))
    colw = A0.COLW; over = [(b['id'], round(b['closure'][-1]['cx'] + A0.BR + 3 + 6.5 * len(b['closure'][-1]['no']) - (b['x'] + colw), 1)) for b in lay['blocks'] if b['closure'][-1]['cx'] + A0.BR + 3 + 6.5 * len(b['closure'][-1]['no']) > b['x'] + colw + A0.COLGAP / 2]
    rep('L7 the closure row ("left blank") of every block ends inside its column or at most half the gutter (10 pt) beyond it', not over, 'blocks beyond column + 10 pt: %s' % over)
    kinds = {b['kind'] for b in lay['blocks']}; sizes = [(b['kind'], len(b['units'])) for b in lay['blocks']]
    rep('L4 block types are the reader\'s own and the blocks are sub-question sized', kinds <= {'choice', 'match', 'order', 'bank', 'human'} and all(n <= {'choice': 5, 'match': 4, 'order': 5, 'bank': 2, 'human': 4}[k] for k, n in sizes), str(sizes))
    png = A0.rasterise(pdf, os.path.join(work, 'blank')); img = np.array(Image.open(png[0]).convert('L')); reg = [A0.register(img, lay, 0)]
    o, bs, held = A.read_sheet_v6(reg, lay); flags = {k: v for k, v in o.items() if v['flag'] not in (None, 'blank')}; vals = {k: v['value'] for k, v in o.items() if v['value'] is not None}
    rep('L5a a completely blank sheet registers and the reader v1.3.0 invents no value (its undeclared-blank rule holds blocks, as in v1.2.0)', reg[0] is not None and not vals, 'rows %d, values %d, flags %d, held blocks %d' % (len(o), len(vals), len(flags), len(held)))
    img2 = img.copy(); rg = random.Random(5)
    for b_ in lay['blocks']:
        for q_ in b_['closure']: M.MS.paint_fill(img2, q_['cx'], q_['cy'], .95, rg)
    reg2 = [A0.register(img2, lay, 0)]; o2, bs2, held2 = A.read_sheet_v6(reg2, lay); fl2 = {k: v for k, v in o2.items() if v['flag'] not in (None, 'blank')}; v2 = {k: v['value'] for k, v in o2.items() if v['value'] is not None}
    rep('L5b a blank sheet with every "left blank" bubble filled reads blank (no value, no flag, no block held)', reg2[0] is not None and not fl2 and not v2 and not held2, 'rows %d, flags %d, values %d, held blocks %d' % (len(o2), len(fl2), len(v2), len(held2)))
    rep('L6 the form code %s passes the check digit and equals the key\'s' % lay['form_code'], A0.damm_valid(lay['form_code']) and lay['form_code'] == key['form_code'], '')
    norm = lambda s: re.sub(r'\s+', ' ', s)
    need = ['the answers you write on the question pages count', 'This sheet is only for fast reading', 'If the sheet and the question pages differ, the question pages count', 'two filled bubbles count as no answer']
    miss = [n for n in need if n not in norm(t1)]
    rep('L8 the plain sentences are printed on page 1 (answers on the question pages count; sheet for fast reading; if they differ the question pages count; two bubbles = no answer)', not miss, 'missing: %s' % miss)
    tips = lay['spec'].get('tips', []); missing_tips = [t['label'] for t in tips if ('Question %s.' % t['label']) not in t2 or norm(t['text']) not in norm(t2)]
    note_ok = norm(V.scoring_note_text()) in norm(t2) if lay['spec'].get('scoring_note', True) else True
    rep('L9 the tips pages: %d tips with their question labels and full text on pages 2 to %d; all type 10 point or larger on every page (smallest %.1f and %.1f); the scoring note is printed' % (len(tips), pages, min(sizes1), min(sizes2)), not missing_tips and note_ok and min(sizes1) >= 10 - 1e-6 and min(sizes2) >= 10 - 1e-6 and len(tips) >= 1,
        'tips not found %s, note printed %s' % (missing_tips, note_ok))
    ok_over = {}
    spec0 = dict(lay['spec']); many = dict(spec0); many['units'] = spec0['units'] * 2
    try: V.build_layout(many); ok_over['units'] = False
    except V.SheetOverflow as e: ok_over['units'] = True
    long_tips = dict(spec0); long_tips['tips'] = [dict(label='q1', text='word ' * 1200)]
    try: V.build_layout(long_tips); ok_over['tips'] = False
    except V.SheetOverflow as e: ok_over['tips'] = True
    cap = {}
    for per_tip, txt in ((2, 'a tip of about two lines of text ' * 5), (3, 'a tip of about three lines of text ' * 8)):
        n = 0
        while True:
            t = dict(spec0); t['tips'] = [dict(label='q%d' % i, text=txt.strip()) for i in range(n + 1)]
            if len(V.build_layout(t)['tips']['pages']) > 1: break
            n += 1
            if n > 60: break
        cap[per_tip] = n
    fit = cap[2] > 0 and cap[3] > 0 and cap[2] >= cap[3]
    print('     measured tips capacity of the FIRST tips page (with the scoring note): %d tips of about two lines, %d tips of about three lines; this form needs %d tips page(s)' % (cap[2], cap[3], len(lay['tips_pages'])))
    rep('L10 overflow is refused, not clipped (too many units; one tip longer than a page), and the capacity of the first tips page is measured (printed above)', ok_over['units'] and ok_over['tips'] and fit, str(ok_over) + ' capacity ok: %s' % fit)
    # R: independence of page 2 and the answer lines
    blank1 = [np.array(Image.open(png[0]).convert('L'))]; same = 0; N = 8
    for i in range(N):
        rng = random.Random(81000 + i); ims, truth = M.MS.student(lay, blank1, rng)
        r0 = [A0.register(ims[0], lay, 0)]; a0 = A.read_sheet_v6(r0, lay)[0]
        sc = ims[0].copy()
        for l in lay['lines']:
            for yl in l['ys']: M.MS.line(sc, int(l['x'] * A0.S + 4), int((yl - 5) * A0.S), int((l['x'] + l['w'] - 4) * A0.S), int((yl - 3) * A0.S), 3, rng)
        black2 = np.zeros_like(sc); blacks = [black2] * len(lay['tips_pages'])
        r1 = [A0.register(sc, lay, 0)]; a1 = A.read_sheet_v6(r1, lay)[0]
        a2 = A.read_sheet_v6([r1[0]] + blacks, lay)[0]
        same += (a0 == a1 == a2)
    rng = random.Random(81000); ims, truth = M.MS.student(lay, blank1, rng); base_ = A.read_sheet_v6([A0.register(ims[0], lay, 0)], lay)[0]; cz = ims[0].copy(); ub = lay['blocks'][0]['units'][0]['rows'][0]
    for cx in ub['cx']: M.MS.paint_fill(cz, cx, ub['cy'], .95, rng)
    ctrl = A.read_sheet_v6([A0.register(cz, lay, 0)], lay)[0]
    rep('R0 control of the test: ink inside a bubble row DOES change the reading (so the equality above can fail)', ctrl != base_, '')
    rd = A.read_pdf(pdf, lay, work)
    out_pdf = A.read_sheet_v6(reg, lay)[0]
    rep('R the reader ignores page 2 and the answer lines: %d of %d sheets read the same with ink scribbled over every answer line and with every tips page black; read_pdf equals the page-1 reading, every mark provisional (legal copy: %s)' % (same, N, A.LEGAL_COPY),
        same == N and rd is not None and all(v['status'] == 'provisional' for v in rd['marks'].values()) and {k: v['mark'] for k, v in rd['marks'].items()} == {k: v['mark'] for k, v in A.provisional(out_pdf).items()} and rd['pages_read'] == [0], '')
    # D: sheet and question page differ
    S_ = A0.S
    def paint(answers, rng):
        im = blank1[0].copy()
        for b in lay['blocks']:
            for u in b['units']:
                v = answers.get(u['no'])
                if v is None: continue
                if u['kind'] == 'human': M.MS.paint_human(im, u['box'], str(v), rng)
                elif u['kind'] == 'bank':
                    for ri, row in enumerate(u['rows']): M.MS.paint_fill(im, row['cx'][int(v[ri])], row['cy'], .95, rng)
                else:
                    row = u['rows'][0]; M.MS.paint_fill(im, row['cx'][row['opts'].index(str(v))], row['cy'], .95, rng)
        return im
    perfect = SC.perfect_marks(key); items = {e['label']: e for e in key['items']}
    humans = {u['no'] for b in lay['blocks'] for u in b['units'] if u['kind'] == 'human'}
    def wrong_letter(lab, kind):
        cur = str(perfect[lab]); opts = [u for b in lay['blocks'] for u in b['units'] if u['no'] == lab][0]['rows'][0]['opts']; return [o for o in opts if o != cur][0]
    def read_sheet_marks(answers):
        rng = random.Random(9); im = paint(answers, rng); r = [A0.register(im, lay, 0)]; out = A.read_sheet_v6(r, lay)[0]; prov = A.provisional(out)
        sm = {k: v['mark'] for k, v in prov.items()}
        for h in humans: sm[h] = answers.get(h)                       # the marker reads the number boxes (the reader only sees that something is written)
        return sm, prov
    chlabs = [e['label'] for e in key['items'] if e['type'].startswith('ChoiceFour')][:3]; m1 = [e['label'] + '1' for e in key['items'] if e['type'] == 'Matching'][0]; bk = [l for e in key['items'] if e['type'] == 'FillBlankGroup' for l in e['answer']][0]
    cpts = {e['label']: e['points'] for e in key['items'] if e['type'].startswith('ChoiceFour')}; mppp = [e['points_per_part'] for e in key['items'] if e['type'] == 'Matching'][0]; bpts = [e['points_per_blank'][bk] for e in key['items'] if e['type'] == 'FillBlankGroup' and bk in e['answer']][0]
    full_pts = sum(SC.score(perfect, key)['per_mark'].values())
    results = []
    sm, prov = read_sheet_marks(perfect)
    r1_, s1_ = SC.resolve({}, sm); t1_ = SC.score(r1_, key)['total']; results.append(('D1 sheet all right, page empty -> the sheet counts', t1_, full_pts))
    wrong_p = {l: wrong_letter(l, 'c') for l in chlabs}; pg = dict(wrong_p); pg[m1] = SC.DOUBLE; pg[bk] = '00'
    r2_, s2_ = SC.resolve(pg, sm); t2_ = SC.score(r2_, key)['total']
    exp2 = full_pts - sum(cpts[l] * 4 / 3 for l in chlabs) - mppp - bpts * 4 / 3
    results.append(('D2 sheet all right; the question page differs (3 wrong choices, one matching pair with two answers, one wrong bank entry) -> the page counts', t2_, exp2))
    wrong_s = dict(perfect); wrong_s.update(wrong_p); smw, provw = read_sheet_marks(wrong_s); pgr = {l: perfect[l] for l in chlabs}
    r3_, s3_ = SC.resolve(pgr, smw); t3_ = SC.score(r3_, key)['total']; results.append(('D3 sheet shows 3 wrong choices, the page has them right -> the page counts', t3_, full_pts))
    r4_, s4_ = SC.resolve({}, smw); t4_ = SC.score(r4_, key)['total']; exp4 = full_pts - sum(cpts[l] * 4 / 3 for l in chlabs); results.append(('D4 the same sheet, page empty -> the sheet counts, the wrong choices cost their penalty', t4_, exp4))
    sheet_read_ok = all(prov[k]['mark'] == str(v) for k, v in perfect.items() if k not in humans) and all(provw[l]['mark'] == wrong_p[l] for l in chlabs)
    sheet_wins = SC.score(SC.resolve({}, sm)[0], key)['total']; rep('D5 control of the fixture: if the sheet won over the page, D2 would score %.4f, not the expected %.4f' % (sheet_wins, exp2), abs(sheet_wins - exp2) > 1)
    for name, got, exp in results: rep(name + ' (score %.4f, hand arithmetic %.4f)' % (got, exp), abs(got - exp) < 1e-9)
    rep('D0 the reader v1.3.0 reads the painted fixture sheets back as provisional marks (every choice, matching, ordering and bank mark equal to what was painted; numbers are left to the marker)', sheet_read_ok and all(v['status'] == 'provisional' for v in prov.values()), '')
    for fl_, base in zip(['A', 'B'], [int(x) for x in args.seed_bases.split(',')]):
        ev = M.run(pdf, layp, args.sheets, base, True)
        wm, nv, pk = ev['with_methods'], ev['naive_reader'], ev['per_kind_with_methods']; share = ev['recoverable_rows_held_by_a_flag'] / max(1, ev['recoverable_rows'])
        print('     [seeds %d-%d] %d sheets, %d rows, registration failures %d' % (base, base + args.sheets - 1, ev['sheets'], ev['rows_scored'], ev['registration_failures']))
        print('     with the methods : %s' % json.dumps(wm, sort_keys=True)); print('     reader without them: %s' % json.dumps(nv, sort_keys=True))
        print('     recoverable rows %d, held for a person %d (%.1f percent) by flag kind %s' % (ev['recoverable_rows'], ev['recoverable_rows_held_by_a_flag'], 100 * share, ev['recoverable_rows_held_by_flag_kind']))
        for k, v in pk.items(): print('       %-22s with methods %-44s naive %s' % (k, json.dumps(v, sort_keys=True), json.dumps(ev['per_kind_naive'].get(k, {}), sort_keys=True)))
        if ev.get('failing_rows'): print('     failing rows: %s' % json.dumps(ev['failing_rows']))
        c = {'registration_failures_0': ev['registration_failures'] == 0, 'silent_wrong_0': wm.get('silent_wrong', 0) == 0, 'missed_0': wm.get('missed', 0) == 0, 'empty_not_flagged_0': wm.get('empty_not_flagged', 0) == 0, 'held_share_le_25_percent': share <= 0.25}
        rep('M reader v1.3.0 on %d synthetic sheets (seeds %d-%d): 0 registration failures, 0 silent wrong, 0 missed, 0 empty-not-flagged, held share <= 25 percent' % (args.sheets, base, base + args.sheets - 1), all(c.values()),
            'registration failures %d, silent_wrong %d, missed %d, empty_not_flagged %d, held share %.1f percent; failed %s' % (ev['registration_failures'], wm.get('silent_wrong', 0), wm.get('missed', 0), wm.get('empty_not_flagged', 0), 100 * share, [k for k, v in c.items() if not v]))
finally:
    shutil.rmtree(work, ignore_errors=True)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
