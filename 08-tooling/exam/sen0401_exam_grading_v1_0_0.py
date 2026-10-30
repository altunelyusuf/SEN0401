"""SEN0401 printed-paper grading tool, version 1.0.0. Reads a filled answer sheet (reader v1.1.0, imported unchanged), assesses it against the answer key of a paper and grades it.
Works on the key file and the sheet-layout file BY THEIR FORMAT, for either order of a paper (no position that only one order has). No student data: a sheet is known by a label the caller gives.

THE METHOD (each step is a rule the check tests):
 G1 Pair check. Before any sheet is graded the key and the layout are cross-checked: every answer place (unit) of the layout has exactly one key entry and the reverse; a choice or match key is a letter
    of the row's options; an ordering group is a permutation; a fill-in code has the right length and a valid Damm check digit; a written place has a numeric or trace key. Any problem refuses grading (exit 2).
 G2 Reading check per sheet. Registration of every page, page count, held share, blank share and the blocks the reader held; a sheet that cannot be registered is NOT graded (listed for a rescan).
 G3 Three outcomes per answer place, never two. A place the reader accepted (no flag) is graded; a place the reader flagged (double, faint, check-digit, held block, incomplete) is DOUBTFUL and is not guessed:
    it goes on the instructor's list. A written place (number or trace) is read by the machine only as written / blank; its content is entered by the instructor ('typed') and judged by the tool against the key.
 G4 Score bounds. Every sheet gets a lowest and a highest possible score: a doubtful place counts 0 in the lowest and its full credit in the highest. When lowest equals highest the grade is FINAL; otherwise it is
    PROVISIONAL and the list of places that make the difference is printed with the points each could move. A grade is never printed as final while a doubtful place or an unentered written place remains.
 G5 Resolution by the instructor. The instructor looks at the paper only at the doubtful places and enters the letter or code (resolved) and the written answers (typed); the tool re-grades. A resolution on a place the
    reader had accepted is accepted but listed as an override (audit).
 G6 Item review over a batch. An item whose correct share is at or below a limit (default chance level of its options) in a batch of at least 30 sheets is listed as a possible key or printing mistake.
Parameters that are NOT decided here (the owner's): points per numbered question (default 1; the printed question numbers, so a two-blank fill-in item is worth 2), partial credit for multi-place items (default proportional; 'all' = all places right), the grade scale (not applied: percent of the maximum only).
No negative marking. Black-and-white print logic is unchanged: the tool only reads the sheet of the paper (the bubble grid).
Command line:
  grading.py check-pair --key K.json --layout L.json
  grading.py grade --key K.json --layout L.json --scan-dir DIR [--entries E.json] [--mode proportional|all] [--out OUTDIR]
     DIR holds one PDF or one set of PNG pages per sheet: LABEL.pdf  or  LABEL_p1.png, LABEL_p2.png ...; E.json = {LABEL: {"typed": {unit: text}, "resolved": {unit: answer}}}
  Exit codes: 0 done, 2 pair check failed or input missing."""
import collections, csv, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v1_0_0 as A0
import sen0401_exam_answersheet_v1_1_0 as R
VERSION = '1.0.0'
DOUBT_FLAGS = ('double', 'faint', 'check-digit', 'held-block', 'incomplete')
BLANK_SHARE_WARN = 0.5       # a sheet with more than this share of places blank is listed for a look (wrong page, missing page, or a student who left it)
HELD_SHARE_WARN = 0.4        # a sheet with more than this share of places doubtful is listed for a rescan
FACILITY_MIN_SHEETS = 30


# ------------------------------------------------------------------ the key read by its format
def load_json(p):
    with open(p) as f: return json.load(f)

def key_places(key):
    """{unit_no: {'item': position, 'type': t, 'answer': a}} from the key by format: a dict answer with 'value' is one numeric place; any other dict gives one place per entry; a scalar is the place named by the position."""
    places = {}; problems = []
    for it in key['items']:
        a = it['answer']; pos = it['position']
        if isinstance(a, dict) and 'value' in a: places[str(pos)] = {'item': pos, 'type': it['type'], 'answer': a}
        elif isinstance(a, dict):
            for u, v in a.items(): places[str(u)] = {'item': pos, 'type': it['type'], 'answer': v}
        else: places[str(pos)] = {'item': pos, 'type': it['type'], 'answer': a}
    return places

def layout_places(layout):
    out = {}
    for b in layout['blocks']:
        for u in b['units']:
            out[u['no']] = {'kind': u['kind'], 'block': b['id'], 'opts': (u['rows'][0]['opts'] if u['kind'] in ('choice', 'match', 'order') else None), 'rows': len(u['rows']), 'cells': (round(u['box']['w'] / 18) if u['kind'] == 'human' else None)}
    return out

def check_pair(key, layout):
    """Returns the list of problems (empty = the key and the layout fit)."""
    kp = key_places(key); lp = layout_places(layout); pr = []
    for u in lp:
        if u not in kp: pr.append('layout place %s has no key entry' % u)
    for u in kp:
        if u not in lp: pr.append('key entry %s has no layout place' % u)
    if len({it['position'] for it in key['items']}) != len(key['items']): pr.append('duplicate item positions in the key')
    groups = collections.defaultdict(list)
    for u, k in kp.items():
        if u not in lp: continue
        L = lp[u]; a = k['answer']
        if L['kind'] in ('choice', 'match'):
            if not (isinstance(a, str) and a in L['opts']): pr.append('place %s: key %r is not one of the options %s' % (u, a, L['opts']))
        elif L['kind'] == 'order':
            if not isinstance(a, (int, str)) or str(a) not in L['opts']: pr.append('place %s: key %r is not one of the ranks %s' % (u, a, L['opts']))
            groups[re.match(r'\d+', u).group()].append(str(a))
        elif L['kind'] == 'bank':
            if not (isinstance(a, str) and a.isdigit() and len(a) == L['rows']): pr.append('place %s: key %r is not a %d-digit code' % (u, a, L['rows']))
            elif not A0.damm_valid(a): pr.append('place %s: key code %s fails the check digit' % (u, a))
        elif L['kind'] == 'human':
            if isinstance(a, dict):
                if not isinstance(a.get('value'), (int, float)) or not isinstance(a.get('tolerance', 0), (int, float)): pr.append('place %s: numeric key malformed' % u)
            elif not isinstance(a, str) or not a.strip(): pr.append('place %s: trace key malformed' % u)
    for g, vals in groups.items():
        if sorted(vals) != sorted(set(vals)): pr.append('ordering group %s: ranks %s are not a permutation' % (g, vals))
    return pr


# ------------------------------------------------------------------ judging one place
def _num(s):
    s = str(s).strip().replace(' ', '').replace(' ', '')
    if not re.fullmatch(r'-?\d+([.,]\d+)?', s): return None
    return float(s.replace(',', '.'))

def judge_typed(keyans, text):
    """True/False, whether the text the instructor typed is the key answer (numeric: within tolerance; trace: same string after trimming)."""
    if isinstance(keyans, dict):
        v = _num(text)
        return v is not None and abs(v - float(keyans['value'])) <= float(keyans.get('tolerance', 0)) + 1e-9
    return str(text).strip() == str(keyans).strip()

def grade_places(key, layout, reads, typed=None, resolved=None, weights=None, mode='proportional'):
    """reads = {unit: {'value','flag', ...}} as the reader prints. Returns the graded sheet (no image work)."""
    typed = typed or {}; resolved = resolved or {}; weights = weights or {}
    kp = key_places(key); lp = layout_places(layout); units = {}; overrides = []
    for u, k in kp.items():
        L = lp[u]; r = reads.get(u, {'value': None, 'flag': 'blank'}); flag = r.get('flag'); val = r.get('value')
        keyans = k['answer']; ent = {'item': k['item'], 'kind': L['kind'], 'reader_value': val, 'reader_flag': flag}
        if L['kind'] == 'human':
            if u in typed:
                good = judge_typed(keyans, typed[u]); ent.update(status='correct' if good else 'wrong', lo=int(good), hi=int(good), entered=typed[u])
                if flag == 'blank': ent.update(status='doubtful', why='entry-on-blank', lo=0, hi=int(good))      # the instructor typed an answer where the reader sees an empty box: look again
                elif flag == 'faint': ent.update(note='faint box, answer entered by the instructor')
            elif flag == 'blank': ent.update(status='blank', lo=0, hi=0)
            else: ent.update(status='await-entry', why=(flag if flag else 'written'), lo=0, hi=1)
        else:
            if u in resolved:
                good = str(resolved[u]) == str(keyans)      # an empty string means: the instructor looked and the place is blank
                ent.update(status='correct' if good else ('blank' if str(resolved[u]) == '' else 'wrong'), lo=int(good), hi=int(good), entered=str(resolved[u]))
                if flag is None: overrides.append(u)
            elif flag in DOUBT_FLAGS: ent.update(status='doubtful', why=flag, lo=0, hi=1)
            elif flag == 'blank' or val is None: ent.update(status='blank', lo=0, hi=0)
            else:
                good = str(val) == str(keyans); ent.update(status='correct' if good else 'wrong', lo=int(good), hi=int(good))
        units[u] = ent
    items = {}
    for it in key['items']:
        pos = it['position']; us = [u for u, k in kp.items() if k['item'] == pos]; w = float(weights.get(pos, weights.get(str(pos), len({_unit_sort(u)[0] for u in us}))))     # default: one point per numbered question (a two-blank fill-in item holds two numbers)
        if mode == 'all': lo = w * all(units[u]['lo'] for u in us); hi = w * all(units[u]['hi'] for u in us)
        else: lo = w * sum(units[u]['lo'] for u in us) / len(us); hi = w * sum(units[u]['hi'] for u in us) / len(us)
        items[pos] = {'weight': w, 'places': sorted(us, key=_unit_sort), 'lo': round(lo, 6), 'hi': round(hi, 6), 'chapters': it.get('chapters'), 'type': it['type']}
    mx = sum(i['weight'] for i in items.values()); lo = sum(i['lo'] for i in items.values()); hi = sum(i['hi'] for i in items.values())
    todo = []
    for u, e in units.items():
        if e['status'] in ('doubtful', 'await-entry'):
            it = items[e['item']]; swing = it['weight'] / len(it['places']) if mode != 'all' else it['weight']
            todo.append({'unit': u, 'item': e['item'], 'chapters': it['chapters'], 'what': e.get('why'), 'status': e['status'], 'reader_value': e['reader_value'], 'max_points_moved': round(swing, 4), 'task': 'resolve' if e['status'] == 'doubtful' else 'enter'})
    todo.sort(key=lambda t: (t['task'] != 'resolve', -t['max_points_moved'], _unit_sort(t['unit'])))
    final = abs(hi - lo) < 1e-9
    return {'units': units, 'items': items, 'max': mx, 'lowest': round(lo, 6), 'highest': round(hi, 6), 'status': 'FINAL' if final else 'PROVISIONAL', 'percent_lowest': round(100 * lo / mx, 2),
            'percent_highest': round(100 * hi / mx, 2), 'to_do': todo, 'overrides': overrides, 'mode': mode}

def _unit_sort(u):
    m = re.match(r'(\d+)(.*)', u); return (int(m.group(1)), m.group(2))


# ------------------------------------------------------------------ reading check of a sheet
def reading_check(layout, reads, blockstate, held, page_count, registered):
    n = len(reads); fl = collections.Counter((r.get('flag') or 'none') for r in reads.values())
    held_n = sum(1 for r in reads.values() if r.get('flag') in DOUBT_FLAGS); blank_n = sum(1 for r in reads.values() if r.get('flag') == 'blank')
    notes = []
    if page_count != layout['pages']: notes.append('page count %d, layout has %d' % (page_count, layout['pages']))
    if held_n / n > HELD_SHARE_WARN: notes.append('doubtful share %.0f percent above %.0f: rescan the sheet' % (100 * held_n / n, 100 * HELD_SHARE_WARN))
    if blank_n / n > BLANK_SHARE_WARN: notes.append('blank share %.0f percent above %.0f: check for a missing page or the wrong sheet' % (100 * blank_n / n, 100 * BLANK_SHARE_WARN))
    undecl = sorted({u for st in blockstate for u in st['undeclared_blank']}, key=_unit_sort)
    return {'places': n, 'flags': dict(fl), 'doubtful': held_n, 'blank': blank_n, 'blocks_held': held, 'undeclared_blank_places': undecl, 'notes': notes, 'registered': registered}


# ------------------------------------------------------------------ images to reads
def read_images(imgs, layout):
    """imgs: raw page images (grey arrays). Returns (reads, blockstate, held, reading_info) or None when a page cannot be registered."""
    reg = [A0.register(im, layout, p) for p, im in enumerate(imgs)] if len(imgs) == layout['pages'] else None
    if reg is None or any(r is None for r in reg): return None
    out, bst, held = R.read_sheet(reg, layout)
    held = extend_holds(layout, out, bst, held)
    return out, bst, held

def extend_holds(layout, out, bst, held):
    """G7 (new in the tool, the reader is not touched). The reader's block closure follows a run of blocks of ONE kind and stops where another kind begins. On a paper whose choice items are interleaved with
    other kinds (the chapter order) a skipped-row shift can run on across such a gap. Two screens, applied across gaps:
      backward: the LAST answer place of the LAST region of a kind is blank and not declared -> every earlier block of that kind is held (a run shift leaves exactly this blank at its end);
      forward: a block whose declared-blank place holds a mark -> every later block of that kind is held up to the first block that has an undeclared blank.
    Blocks added are marked 'held-block' on places the reader left unflagged, like the reader's own holds. Returns the extended list of held block indices."""
    blocks = layout['blocks']; held = set(held); by_kind = collections.defaultdict(list)
    for i, b in enumerate(blocks): by_kind[b['kind']].append(i)
    for kind, idx in by_kind.items():
        last = idx[-1]
        lastno = blocks[last]['units'][-1]['no']      # blank and not ticked as blank; the reader's own 'undeclared_blank' is empty when the whole region is blank, so the test is made on blank and declared
        if lastno in bst[last]['blank'] and lastno not in bst[last]['declared']: held.update(i for i in idx if i < last)
        for i in idx:
            if bst[i]['declared_filled']:
                for j in idx:
                    if j <= i: continue
                    held.add(j)
                    if bst[j]['undeclared_blank']: break
    for i in held:
        for u in blocks[i]['units']:
            if out[u['no']]['flag'] is None: out[u['no']]['flag'] = 'held-block'
    return sorted(held)

def grade_sheet(key, layout, imgs, label, typed=None, resolved=None, weights=None, mode='proportional'):
    got = read_images(imgs, layout)
    if got is None:
        return {'label': label, 'status': 'NOT_GRADED', 'reason': 'a page could not be registered or the page count differs (%d pages, layout %d): rescan' % (len(imgs), layout['pages'])}
    reads, bst, held = got
    g = grade_places(key, layout, reads, typed, resolved, weights, mode)
    g['label'] = label; g['reading'] = reading_check(layout, reads, bst, held, len(imgs), True)
    return g


# ------------------------------------------------------------------ batch outputs
def item_review(sheets, key, layout):
    """G6: per item, the share of graded sheets with full credit, over sheets where every place of the item was decided; listed when at or below chance."""
    lp = layout_places(layout); kp = key_places(key); rows = []
    graded = [s for s in sheets if s.get('status') in ('FINAL', 'PROVISIONAL')]
    for it in key['items']:
        pos = it['position']; places = [u for u, k in kp.items() if k['item'] == pos]
        decided = [s for s in graded if all(s['units'][u]['lo'] == s['units'][u]['hi'] for u in places)]
        if not decided: continue
        right = sum(1 for s in decided if all(s['units'][u]['lo'] == 1 for u in places))
        kinds = {lp[u]['kind'] for u in places}
        chance = 0.25 if kinds == {'choice'} else None
        if chance is None and kinds == {'match'}: chance = 1.0 / len(lp[places[0]]['opts'])
        share = right / len(decided)
        rows.append({'item': pos, 'decided_sheets': len(decided), 'correct_share': round(share, 3), 'chance': chance,
                     'review': bool(len(decided) >= FACILITY_MIN_SHEETS and chance is not None and share <= chance)})
    return rows

def write_outputs(sheets, key, layout, outdir):
    os.makedirs(outdir, exist_ok=True)
    gr = [s for s in sheets if s.get('status') in ('FINAL', 'PROVISIONAL')]
    with open(os.path.join(outdir, 'grades.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['sheet', 'status', 'lowest', 'highest', 'max', 'percent_lowest', 'percent_highest', 'places_to_resolve', 'places_to_enter'])
        for s in sheets:
            if s['status'] == 'NOT_GRADED': w.writerow([s['label'], 'NOT_GRADED', '', '', '', '', '', '', s['reason']]); continue
            w.writerow([s['label'], s['status'], s['lowest'], s['highest'], s['max'], s['percent_lowest'], s['percent_highest'],
                        sum(1 for t in s['to_do'] if t['task'] == 'resolve'), sum(1 for t in s['to_do'] if t['task'] == 'enter')])
    with open(os.path.join(outdir, 'worklist.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['sheet', 'task', 'place', 'item', 'chapters', 'why', 'reader_saw', 'max_points_moved'])
        for s in gr:
            for t in s['to_do']: w.writerow([s['label'], t['task'], t['unit'], t['item'], ' '.join(map(str, t['chapters'] or [])), t['what'], t['reader_value'], t['max_points_moved']])
    rev = item_review(sheets, key, layout)
    json.dump({'tool_version': VERSION, 'reader_version': R.VERSION, 'sheets': sheets, 'item_review': rev}, open(os.path.join(outdir, 'grading_report.json'), 'w'), indent=1, default=str)
    return rev

def sheets_from_dir(d):
    import glob
    from PIL import Image
    import numpy as np
    found = collections.OrderedDict()
    for p in sorted(glob.glob(os.path.join(d, '*'))):
        b = os.path.basename(p)
        if b.lower().endswith('.pdf'): found[b[:-4]] = ('pdf', p)
        else:
            m = re.fullmatch(r'(.+)_p(\d+)\.png', b)
            if m: found.setdefault(m.group(1), ('png', {}))[1][int(m.group(2))] = p
    for label, (kind, p) in found.items():
        if kind == 'pdf':
            import tempfile, shutil
            w = tempfile.mkdtemp(prefix='sen0401_grade_')
            try: yield label, [np.array(Image.open(q).convert('L')) for q in A0.rasterise(p, os.path.join(w, 'pg'))]
            finally: shutil.rmtree(w, ignore_errors=True)
        else: yield label, [np.array(Image.open(p[i]).convert('L')) for i in sorted(p)]

def main(argv=None):
    import argparse
    a = argparse.ArgumentParser(); sp = a.add_subparsers(dest='cmd', required=True)
    c = sp.add_parser('check-pair'); c.add_argument('--key', required=True); c.add_argument('--layout', required=True)
    g = sp.add_parser('grade'); g.add_argument('--key', required=True); g.add_argument('--layout', required=True); g.add_argument('--scan-dir', required=True)
    g.add_argument('--entries'); g.add_argument('--mode', default='proportional', choices=['proportional', 'all']); g.add_argument('--out', default='grading_out'); g.add_argument('--weights')
    o = a.parse_args(argv)
    key = load_json(o.key); layout = load_json(o.layout); pr = check_pair(key, layout)
    if pr:
        print('PAIR CHECK FAILED (%d problems)' % len(pr)); [print('  ' + p) for p in pr]; return 2
    print('PAIR CHECK OK: %d answer places, %d items' % (len(layout_places(layout)), len(key['items'])))
    if o.cmd == 'check-pair': return 0
    if not os.path.isdir(o.scan_dir): print('scan dir missing'); return 2
    ent = load_json(o.entries) if o.entries else {}; weights = load_json(o.weights) if o.weights else None; sheets = []
    for label, imgs in sheets_from_dir(o.scan_dir):
        e = ent.get(label, {})
        s = grade_sheet(key, layout, imgs, label, e.get('typed'), e.get('resolved'), weights, o.mode); sheets.append(s)
        print(label, s['status'], ('%s-%s of %s' % (s['lowest'], s['highest'], s['max'])) if s['status'] != 'NOT_GRADED' else s['reason'])
    rev = write_outputs(sheets, key, layout, o.out)
    for r in rev:
        if r['review']: print('ITEM REVIEW: item %s correct share %.3f at or below chance %.2f over %d sheets' % (r['item'], r['correct_share'], r['chance'], r['decided_sheets']))
    return 0

if __name__ == '__main__': sys.exit(main())
