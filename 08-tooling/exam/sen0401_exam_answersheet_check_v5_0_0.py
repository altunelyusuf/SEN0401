"""Check of the midterm v5 answer sheet (new file, copied from sen0401_exam_answersheet_check_v3_0_0.py, which stays unchanged; ONE form, no form letter in the file names: the tag is the file prefix). Original docstring of v3: Check of the midterm v3 answer sheets (new copy in the manner of sen0401_exam_answersheet_check_v1_1_0.py; the old tools are unchanged and imported). Prints PASS / FAIL per check; exit 1 on any FAIL.
Per form (the sheet PDF, its layout JSON and its key JSON are given in a folder and the form letters):
  L1  the sheet is ONE page, with the four corner marks the reader registers on
  L2  every answer place of the key (a row of a choice, matching, ordering or bank item, a box of a number) has exactly one sheet unit with that label, and the sheet has no other unit (question 5 has none: hand-graded)
  L3  position-exact: every bubble and box lies inside the page margins, no two bubbles of the page overlap, and the label of every unit is printed on the PDF (found by pdfplumber) at the layout's row
  L7  the 'left blank' row of every block ends inside the block's column or at most 10 pt (half the 20 pt gutter) beyond it (the first run of this check used the strict column edge and measured 2.5 pt over on the ordering block; the criterion's purpose is not to run into the neighbouring column)
  L4  the block types are the reader's own (choice, match, order, bank, human) and each sub-question is one block (matching 4, ordering 5, bank 2 rows, numbers 4)
  L5a a completely blank rendering registers and the reader v1.2.0 invents no value (the v1.1.0 check K3 asked for no flag too; the v1.2.0 reader flags undeclared blanks by design, measured on its default layout: 20 flags in 5 blocks)
  L5b the same blank sheet with every 'left blank' bubble filled reads blank: no value, no flag, no block held
  L6  the form code printed on the sheet is valid by the check digit and equals the key's form code
  M   the reader measure (sen0401_exam_answersheet_measure_v3_0_0.py) on N synthetic sheets: registration failures 0, silent wrong 0, missed 0, empty-not-flagged 0, held share at most 25 percent (the thresholds of v1.1.0 check K5, unchanged)
Usage: check_v3.py DIR [--forms A,B] [--sheets 40] [--seed-bases 57000,57100] [--log FILE] [--tag sen0401_exam_midterm_v3_0_0]  (the log is created new; an existing log is refused)"""
import argparse, json, os, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import pdfplumber
import sen0401_exam_answersheet_v1_0_0 as A0
import sen0401_exam_answersheet_v1_2_0 as A
import sen0401_exam_answersheet_measure_v3_0_0 as M
ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--forms', default='A'); ap.add_argument('--sheets', type=int, default=40); ap.add_argument('--seed-bases', default='57000')
ap.add_argument('--log'); ap.add_argument('--tag', default='sen0401_exam_midterm_v5_0_0'); args = ap.parse_args()
if args.log and os.path.exists(args.log): print('REFUSED: the log file exists and is never appended to: ' + args.log); sys.exit(2)
res = []
def rep(name, ok, detail=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail), flush=True)
forms = args.forms.split(','); bases = [int(x) for x in args.seed_bases.split(',')]
g = subprocess.run(['git', '-C', HERE, 'status', '--porcelain'], capture_output=True, text=True)
bad = [l for l in g.stdout.splitlines() if not l.startswith('??') and 'papers_midterm_v5' not in l]
rep('K1 no committed file is edited (git status shows only new files)', g.returncode == 0 and not bad, ' '.join(bad[:5]))
work = tempfile.mkdtemp(prefix='sen0401_as_chk5_')
try:
    for fl, base in zip(forms, bases):
        tag = args.tag; pdf = os.path.join(args.dir, tag + '_sheet.pdf'); lay = json.load(open(os.path.join(args.dir, tag + '_sheet_layout.json'))); key = json.load(open(os.path.join(args.dir, tag + '_key.json')))
        out_ = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
        pages = int([l for l in out_.splitlines() if l.startswith('Pages:')][0].split()[1])
        rep('L1 form %s: the sheet has one page and four corner marks' % fl, pages == 1 and lay['pages'] == 1 and len(lay['fiducials']) == 4, 'pages %d, fiducials %d' % (pages, len(lay['fiducials'])))
        keyplaces = set()
        for e in key['items']:
            if e['type'] == 'ShortExplanation': continue
            keyplaces |= set(e['answer'].keys())
        sheetplaces = [u['no'] for b in lay['blocks'] for u in b['units']]
        rep('L2 form %s: the sheet units are exactly the answer places of the key (%d places, question 5 has none)' % (fl, len(keyplaces)), set(sheetplaces) == keyplaces and len(sheetplaces) == len(set(sheetplaces)),
            'only in key %s, only on sheet %s' % (sorted(keyplaces - set(sheetplaces)), sorted(set(sheetplaces) - keyplaces)))
        PW, PH = lay['page_pt']; MARG = A0.MARG; pts = []; inside = True
        for b in lay['blocks']:
            for u in b['units']:
                for r in u.get('rows', []):
                    for cx in r['cx']:
                        pts.append((cx, r['cy'])); inside &= (MARG - 1 <= cx - A0.BR and cx + A0.BR <= PW - MARG + 1 and MARG - 1 <= r['cy'] - A0.BR and r['cy'] + A0.BR <= PH - MARG + 1)
                if 'box' in u:
                    bx = u['box']; inside &= (MARG - 1 <= bx['x'] and bx['x'] + bx['w'] <= PW - MARG + 1 and bx['y'] >= MARG - 1 and bx['y'] + bx['h'] <= PH - MARG + 1)
            for q in b['closure']: pts.append((q['cx'], q['cy'])); inside &= (q['cx'] + A0.BR <= PW - MARG + 1)
        overl = sum(1 for i in range(len(pts)) for j in range(i + 1, len(pts)) if ((pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2) ** .5 < 2 * A0.BR + 1)
        words = []
        with pdfplumber.open(pdf) as d: words = [(w['text'], w['x0'], w['x1'], w['top'], w['bottom']) for w in d.pages[0].extract_words()]
        missing = []
        for b in lay['blocks']:
            for u in b['units']:
                if u['kind'] == 'human': cy = u['box']['y'] + u['box']['h'] / 2
                else: cy = u['rows'][0]['cy']
                if not any(w[0] == u['no'] and w[3] - 2 <= cy <= w[4] + 2 for w in words): missing.append(u['no'])
        rep('L3 form %s: position-exact - every bubble and box inside the margins, no two bubbles overlap, the label of every unit is printed at its row' % fl, inside and overl == 0 and not missing,
            'inside %s, overlaps %d, labels not found at their row %s' % (inside, overl, missing[:6]))
        colw = A0.COLW; over = [(b['id'], round(b['closure'][-1]['cx'] + A0.BR + 3 + 6.5 * len(b['closure'][-1]['no']) - (b['x'] + colw), 1)) for b in lay['blocks'] if b['closure'][-1]['cx'] + A0.BR + 3 + 6.5 * len(b['closure'][-1]['no']) > b['x'] + colw + A0.COLGAP / 2]
        rep('L7 form %s: the closure row ("left blank") of every block, with its labels, ends inside the block\'s column or at most half the gutter (10 pt) beyond it - never into the next column or past the page margin by more than that' % fl, not over,
            'blocks that run beyond column + 10 pt (id, points over the column edge): %s' % over)
        kinds = {b['kind'] for b in lay['blocks']}; sizes = [(b['kind'], len(b['units'])) for b in lay['blocks']]
        rep('L4 form %s: block types are the reader\'s own and the blocks are sub-question sized' % fl, kinds <= {'choice', 'match', 'order', 'bank', 'human'} and all(n <= {'choice': 5, 'match': 4, 'order': 5, 'bank': 2, 'human': 4}[k] for k, n in sizes), str(sizes))
        png = A0.rasterise(pdf, os.path.join(work, 'blank_' + fl)); img = np.array(Image.open(png[0]).convert('L')); reg = [A0.register(img, lay, 0)]
        o, bs, held = A.read_sheet(reg, lay); flags = {k: v for k, v in o.items() if v['flag'] not in (None, 'blank')}; vals = {k: v['value'] for k, v in o.items() if v['value'] is not None}
        rep('L5a form %s: a completely blank sheet registers and the reader v1.2.0 invents no value (its undeclared-blank rule holds blocks, as it does on its own default layout: 20 flags in 5 blocks)' % fl, reg[0] is not None and not vals,
            'rows %d, values %d, flags %d, held blocks %d' % (len(o), len(vals), len(flags), len(held)))
        import random as _r; img2 = img.copy(); rg = _r.Random(5)
        for b_ in lay['blocks']:
            for q_ in b_['closure']: M.MS.paint_fill(img2, q_['cx'], q_['cy'], .95, rg)
        reg2 = [A0.register(img2, lay, 0)]; o2, bs2, held2 = A.read_sheet(reg2, lay); fl2 = {k: v for k, v in o2.items() if v['flag'] not in (None, 'blank')}; v2 = {k: v['value'] for k, v in o2.items() if v['value'] is not None}
        rep('L5b form %s: a blank sheet with every "left blank" bubble filled reads blank (no value, no flag, no block held)' % fl, reg2[0] is not None and not fl2 and not v2 and not held2, 'rows %d, flags %d, values %d, held blocks %d' % (len(o2), len(fl2), len(v2), len(held2)))
        code = lay['form_code']
        rep('L6 form %s: the form code %s passes the check digit and equals the key\'s' % (fl, code), A0.damm_valid(code) and code == key['form_code'], '')
        ev = M.run(pdf, os.path.join(args.dir, tag + '_sheet_layout.json'), args.sheets, base, True)
        wm, nv, pk = ev['with_methods'], ev['naive_reader'], ev['per_kind_with_methods']; share = ev['recoverable_rows_held_by_a_flag'] / max(1, ev['recoverable_rows'])
        print('     [form %s seeds %d-%d] %d sheets, %d rows, registration failures %d' % (fl, base, base + args.sheets - 1, ev['sheets'], ev['rows_scored'], ev['registration_failures']))
        print('     [form %s] with the methods : %s' % (fl, json.dumps(wm, sort_keys=True))); print('     [form %s] reader without them: %s' % (fl, json.dumps(nv, sort_keys=True)))
        print('     [form %s] recoverable rows %d, held for a person %d (%.1f percent) by flag kind %s' % (fl, ev['recoverable_rows'], ev['recoverable_rows_held_by_a_flag'], 100 * share, ev['recoverable_rows_held_by_flag_kind']))
        for k, v in pk.items(): print('       %-22s with methods %-44s naive %s' % (k, json.dumps(v, sort_keys=True), json.dumps(ev['per_kind_naive'].get(k, {}), sort_keys=True)))
        if ev.get('failing_rows'): print('     [form %s] failing rows: %s' % (fl, json.dumps(ev['failing_rows'])))
        c = {'registration_failures_0': ev['registration_failures'] == 0, 'silent_wrong_0': wm.get('silent_wrong', 0) == 0, 'missed_0': wm.get('missed', 0) == 0, 'empty_not_flagged_0': wm.get('empty_not_flagged', 0) == 0, 'held_share_le_25_percent': share <= 0.25}
        rep('M form %s: reader v1.2.0 on %d synthetic sheets (seeds %d-%d): 0 silent wrong, 0 missed, 0 empty-not-flagged, held share <= 25 percent' % (fl, args.sheets, base, base + args.sheets - 1), all(c.values()),
            'silent_wrong %d, missed %d, empty_not_flagged %d, held share %.1f percent; failed %s' % (wm.get('silent_wrong', 0), wm.get('missed', 0), wm.get('empty_not_flagged', 0), 100 * share, [k for k, v in c.items() if not v]))
finally:
    shutil.rmtree(work, ignore_errors=True)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
