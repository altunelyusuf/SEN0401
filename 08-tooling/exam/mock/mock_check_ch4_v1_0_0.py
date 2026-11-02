#!/usr/bin/env python3
"""SEN0401 mock bank check for one chapter, v1.0.0. Holds no question and no answer text.
Usage: mock_check_ch4_v1_0_0.py check [--bank FILE]   |   selftest [--bank FILE]
Checks schema, counts, points, word limits, 'You are asked to' ending, distinct options, answer spread, numeric recomputation
(the generator in the same folder is run again and compared), no option-letter patterns in solutions.
selftest plants three defects (a letter in a solution, a 70-word stem, a changed numeric key) and expects each to FAIL."""
import argparse, copy, importlib.util, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER = 4
PRIV = '/home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts'
DEFAULT_BANK = os.path.join(PRIV, 'mock_bank_ch%d_v1_0_0.json' % CHAPTER)
GEN = os.path.join(PRIV, 'mock_numeric_gen_ch%d_v1_0_0.py' % CHAPTER)
W = lambda t: len([w for w in (t or '').split() if re.search(r'[A-Za-z0-9]', w)])
LETTER = [r'\b[Oo]ption\s+[A-E]\b', r'\b(?:answer|choice|response|entry)\s+[A-E]\b', r'\(\s*[A-E]\s*\)', r'(?:^|\s)[A-E][.)]\s', r'\bletter\s+[A-E]\b']
SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"(])')

def texts_of(v):
    if isinstance(v, str): return [v]
    if isinstance(v, list): return [s for x in v for s in texts_of(x)]
    if isinstance(v, dict): return [s for x in v.values() for s in texts_of(x)]
    return []

def run_gen():
    spec = importlib.util.spec_from_file_location('mock_gen_ch%d' % CHAPTER, GEN)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.build()

def stem_ok(f, who, s, tip=None):
    if W(s) > 60: f.append('%s: stem %d words' % (who, W(s)))
    last = [x for x in SPLIT.split(' '.join(s.split())) if x.strip()]
    if not last or not last[-1].startswith('You are asked to'): f.append('%s: last sentence does not start with "You are asked to"' % who)
    if tip is not None:
        if not tip.startswith('Tip: '): f.append('%s: tip does not start with "Tip: "' % who)
        elif W(tip[5:]) > 12: f.append('%s: tip %d words' % (who, W(tip[5:])))

def check(bank, regen=True):
    f = []; items = bank.get('items', [])
    if bank.get('chapter') != CHAPTER: f.append('chapter field is not %d' % CHAPTER)
    by = {}
    for it in items: by.setdefault(it.get('type'), []).append(it)
    ids = [it.get('id') for it in items]
    if len(set(ids)) != len(ids): f.append('duplicate ids')
    for t, n in (('choice', 10), ('numeric', 4), ('matching', 3), ('ordering', 2), ('fill', 4)):
        if len(by.get(t, [])) != n: f.append('count %s: %d, want %d' % (t, len(by.get(t, [])), n))
    for it in items:
        if it.get('chapter') != CHAPTER: f.append('%s: chapter field' % it.get('id'))
        for s in texts_of([it.get(k) for k in ('steps', 'steps_solution', 'why_right', 'why_wrong', 'why_wrong_rows', 'why_wrong_entries')] + ([[i.get('steps'), i.get('why_right'), i.get('common_wrong')] for i in it.get('instances', [])])):
            for p in LETTER:
                if re.search(p, s): f.append('%s: option-letter pattern in a solution (%s)' % (it.get('id'), p)); break
    # choice
    ch = by.get('choice', [])
    pts = sorted(c.get('points') for c in ch)
    if pts != [3] * 4 + [4] * 6: f.append('choice points %s, want four 3 and six 4' % pts)
    cnt = [0] * 5
    for c in ch:
        w = c['id']; stem_ok(f, w, c.get('stem', ''), c.get('tip', ''))
        o = c.get('options') or []
        if len(o) != 5: f.append('%s: %d options' % (w, len(o))); continue
        if len({x.strip().lower() for x in o}) != 5 or any(not x.strip() for x in o): f.append('%s: options not distinct or empty' % w)
        if any(re.search(r'\b(all|none) of (the above|these)\b', x, re.I) for x in o): f.append('%s: all/none of the above' % w)
        ws = [W(x) for x in o]
        if max(ws) > 3 * min(ws): f.append('%s: longest %d words, shortest %d' % (w, max(ws), min(ws)))
        a = c.get('answer')
        if not isinstance(a, int) or isinstance(a, bool) or not 0 <= a < 5: f.append('%s: answer index' % w); continue
        cnt[a] += 1
        ww = c.get('why_wrong') or {}
        if sorted(ww) != sorted(str(i) for i in range(5) if i != a) or any(not str(v).strip() for v in ww.values()): f.append('%s: why_wrong keys' % w)
        if not c.get('steps') or not str(c.get('why_right', '')).strip(): f.append('%s: steps or why_right missing' % w)
    if ch and max(cnt) - min(cnt) > 1: f.append('answer spread %s differs by more than 1' % cnt)
    # numeric
    num = by.get('numeric', [])
    if sum(1 for n in num if n.get('can_be_4')) != 1: f.append('numeric: can_be_4 must be true on exactly one template')
    for n in num:
        w = n['id']
        if n.get('points') != 3: f.append('%s: points' % w)
        if W(n.get('tip', '')[5:]) > 12 or not n.get('tip', '').startswith('Tip: '): f.append('%s: tip' % w)
        ins = n.get('instances') or []
        if len(ins) != 8: f.append('%s: %d instances' % (w, len(ins)))
        keys = [i.get('key_value') for i in ins]
        if len(set(keys)) != len(keys): f.append('%s: key values not all different' % w)
        if len({i.get('stem') for i in ins}) != len(ins): f.append('%s: stems not all different' % w)
        for k, i in enumerate(ins, 1):
            x = '%s#%d' % (w, k); stem_ok(f, x, i.get('stem', ''))
            kv = i.get('key_value')
            if not isinstance(kv, int) or isinstance(kv, bool) or not 0 <= kv <= 99999: f.append('%s: key_value not a non-negative integer of at most five digits' % x)
            st = i.get('steps') or []
            if len(st) < 2 or not all(re.search(r'\d', s) for s in st): f.append('%s: fewer than 2 steps or a step without a number' % x)
            cw = i.get('common_wrong') or []
            vals = [c.get('value') for c in cw]
            if len(cw) != 3 or len(set(vals + [kv])) != 4 or any(not isinstance(v, int) or v < 0 or v > 99999 for v in vals) or any(not str(c.get('why', '')).strip() for c in cw): f.append('%s: common_wrong' % x)
        if regen:
            g = next((t for t in run_gen() if t['id'] == w), None)
            if g is None or g['instances'] != ins: f.append('%s: instances differ from the generator output' % w)
    # matching
    for m in by.get('matching', []):
        w = m['id']; stem_ok(f, w, m.get('intro', ''), m.get('tip', ''))
        p, r, a = m.get('premises') or [], m.get('responses') or [], m.get('answer') or []
        if len(p) != 4 or len(r) != 5 or len(a) != 4 or len(set(a)) != 4 or not all(isinstance(i, int) and 0 <= i < 5 for i in a): f.append('%s: shape or answer' % w); continue
        if len(set(x.lower() for x in p + r)) != 9: f.append('%s: premises and responses not distinct' % w)
        if a == sorted(a): f.append('%s: answer is in display order' % w)
        if len(m.get('why_wrong_rows') or []) != 4 or not m.get('steps') or not m.get('why_right'): f.append('%s: solution parts' % w)
    # ordering
    for o in by.get('ordering', []):
        w = o['id']; stem_ok(f, w, o.get('intro', ''), o.get('tip', ''))
        s, a, sol = o.get('steps') or [], o.get('answer') or [], o.get('steps_solution') or []
        if len(s) != 5 or sorted(a) != [1, 2, 3, 4, 5] or len(sol) != 5: f.append('%s: shape' % w); continue
        if a == [1, 2, 3, 4, 5]: f.append('%s: displayed order is the right order' % w)
        if any(sol[a[i] - 1] != s[i] for i in range(5)): f.append('%s: answer does not agree with steps_solution' % w)
        if len(set(s)) != 5 or len(o.get('why_wrong_rows') or []) != 5 or not o.get('why_right'): f.append('%s: distinct steps or solution parts' % w)
    # fill
    for q in by.get('fill', []):
        w = q['id']; stem_ok(f, w, q.get('stem', ''), q.get('tip', ''))
        b, bl = q.get('bank') or [], q.get('blanks') or []
        if len(b) != 5 or len({x.lower() for x in b}) != 5 or len(bl) != 2: f.append('%s: bank or blanks' % w); continue
        ans = [x.get('answer') for x in bl]
        if len(set(ans)) != 2 or not all(isinstance(i, int) and 0 <= i < 5 for i in ans) or not all('____' in x.get('sentence', '') for x in bl): f.append('%s: blank answers or marks' % w)
        if sorted((q.get('why_wrong_entries') or {})) != ['0', '1', '2', '3', '4'] or not q.get('steps') or not q.get('why_right'): f.append('%s: solution parts' % w)
    return f

def selftest(bank):
    bad = 0
    base = check(bank)
    print('baseline failures: %d' % len(base))
    d1 = copy.deepcopy(bank); c = next(i for i in d1['items'] if i['type'] == 'choice'); c['why_right'] += ' Option B is the right one.'
    d2 = copy.deepcopy(bank); c = next(i for i in d2['items'] if i['type'] == 'choice'); c['stem'] = ' '.join(['word'] * 68) + ' You are asked to choose.'
    d3 = copy.deepcopy(bank); n = next(i for i in d3['items'] if i['type'] == 'numeric'); n['instances'][2]['key_value'] += 1
    for name, d, pat in (('letter in a solution', d1, 'option-letter'), ('70-word stem', d2, 'stem '), ('changed numeric key', d3, 'differ from the generator')):
        r = check(d); hit = [x for x in r if pat in x]
        print('planted defect "%s": %s (%s)' % (name, 'FAIL as expected' if hit else 'NOT DETECTED', hit[0][:70] if hit else '-'))
        if not hit: bad += 1
    print('SELFTEST %s' % ('PASS' if bad == 0 and not base else 'FAIL'))
    return 0 if bad == 0 and not base else 1

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['check', 'selftest']); ap.add_argument('--bank', default=DEFAULT_BANK); a = ap.parse_args()
    with open(a.bank, encoding='utf-8') as fh: bank = json.load(fh)
    if a.cmd == 'selftest': return selftest(bank)
    r = check(bank); items = bank['items']
    print('Mock bank check chapter %d  file %s' % (CHAPTER, os.path.basename(a.bank)))
    print('items: choice %d, numeric templates %d (instances %d), matching %d, ordering %d, fill %d' % tuple([sum(1 for i in items if i['type'] == t) for t in ('choice', 'numeric')][:1] + [sum(1 for i in items if i['type'] == 'numeric'), sum(len(i['instances']) for i in items if i['type'] == 'numeric')] + [sum(1 for i in items if i['type'] == t) for t in ('matching', 'ordering', 'fill')]))
    print('choice answer index counts: %s' % [sum(1 for i in items if i['type'] == 'choice' and i['answer'] == k) for k in range(5)])
    for x in r: print('  FAIL', x)
    print('RESULT %s (%d failure(s))' % ('PASS' if not r else 'FAIL', len(r)))
    return 0 if not r else 1

if __name__ == '__main__': sys.exit(main())
