#!/usr/bin/env python3
"""SEN0401 mock bank check, chapter N (default 1), version 1.0.0. Holds no question and no answer; prints ids and counts only.
  check    [--bank FILE] [--chapter N]    schema, counts, points, word limits, distinct options, answer spread, numeric recomputation by the generator, no letter patterns
  selftest [--bank FILE] [--chapter N]    plants three defects (a letter in a solution, a 70-word stem, a changed numeric key) in copies; each must make the check FAIL
  rules    [--bank FILE] [--chapter N]    adapter to the items-file shape, then readability R1 R2 R3 R4 R6 (v1.1.0) and clarity C1 to C5 (v1.0.1); R5 and C4b are NOT_MEASURED
Exit 0 all clear, 1 a failure, 2 input error."""
import argparse, copy, importlib.util, json, os, re, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = '/home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts'   # private folder: bank and generator live there only
EXAM = '/home/claude/sen0401/08-tooling/exam'
LETTER = re.compile(r'\b(?:[Oo]ption|[Cc]hoice|[Aa]nswer|[Rr]esponse|[Aa]lternative)s? \(?[A-E]\b|\(\s?[A-E]\s?\)|\b[A-E]\)|\bletter\b')

def nw(t): return len([w for w in str(t).split() if re.search(r'[A-Za-z0-9]', w)])
def last_sentence(t): return [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"(])', re.sub(r'\s+', ' ', t).strip()) if s][-1]
def paths(a, ch): return (a.bank or os.path.join(PARTS, 'mock_bank_ch%d_v1_0_0.json' % ch))
def load_gen(ch):
    spec = importlib.util.spec_from_file_location('gen%d' % ch, os.path.join(PARTS, 'mock_numeric_gen_ch%d_v1_0_0.py' % ch)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def solution_texts(it):
    t = it['type']; out = []
    if t == 'numeric':
        for ins in it['instances']: out += ins['steps'] + [ins['why_right']] + [w['why'] for w in ins['common_wrong']]
    else:
        out += list(it.get('steps') or []) + list(it.get('steps_solution') or []) + [it.get('why_right', '')]
        out += list((it.get('why_wrong') or {}).values()) + list(it.get('why_wrong_rows') or []) + list((it.get('why_wrong_entries') or {}).values())
    return out

def check(bank, ch, gen_items=None):
    errs = []; E = errs.append
    items = bank.get('items', [])
    if bank.get('chapter') != ch: E('chapter field is not %d' % ch)
    ids = [i.get('id') for i in items]
    if len(set(ids)) != len(ids): E('duplicate ids')
    by = lambda t: [i for i in items if i.get('type') == t]
    cho, num, mat, orde, fil = by('choice'), by('numeric'), by('matching'), by('ordering'), by('fill')
    for name, got, want in [('choice', len(cho), 10), ('numeric', len(num), 4), ('matching', len(mat), 3), ('ordering', len(orde), 2), ('fill', len(fil), 4)]:
        if got != want: E('%s count %d, need %d' % (name, got, want))
    for i in items:
        if i.get('chapter') != ch: E('%s chapter field' % i.get('id'))
        if not str(i.get('id', '')).startswith({'choice': 'c', 'numeric': 'n', 'matching': 'm', 'ordering': 'o', 'fill': 'f'}.get(i.get('type'), '?') + str(ch) + '_'): E('%s id prefix' % i.get('id'))
        tip = i.get('tip')
        if not tip or nw(tip) > 12: E('%s tip missing or over 12 words' % i['id'])
        if tip and re.match(r'^\s*Tips?:', tip): E('%s tip must not carry its own prefix' % i['id'])
        for s in solution_texts(i):
            if not str(s).strip(): E('%s empty solution text' % i['id'])
            if LETTER.search(str(s)): E('%s letter pattern in a solution' % i['id'])
    # choice
    p3 = sum(1 for i in cho if i.get('points') == 3); p4 = sum(1 for i in cho if i.get('points') == 4)
    if (p3, p4) != (4, 6): E('choice points: %d of 3, %d of 4 (need 4 and 6)' % (p3, p4))
    cnt = [sum(1 for i in cho if i.get('answer') == k) for k in range(5)]
    if cho and max(cnt) - min(cnt) > 1: E('answer spread %s' % cnt)
    for i in cho:
        o = i.get('options', []); ws = [nw(x) for x in o]
        if len(o) != 5 or len(set(x.strip().lower() for x in o)) != 5: E('%s options not 5 distinct' % i['id'])
        if ws and (min(ws) == 0 or max(ws) > 3 * min(ws)): E('%s option length ratio' % i['id'])
        if not (isinstance(i.get('answer'), int) and 0 <= i['answer'] < 5): E('%s answer index' % i['id'])
        elif sorted((i.get('why_wrong') or {}).keys()) != sorted(str(k) for k in range(5) if k != i['answer']): E('%s why_wrong keys' % i['id'])
        if any(re.search(r'all of the above|none of the above', x, re.I) for x in o): E('%s all/none of the above' % i['id'])
        if nw(i.get('stem', '')) > 60: E('%s stem over 60 words (%d)' % (i['id'], nw(i['stem'])))
        if not last_sentence(i.get('stem', '')).startswith('You are asked to'): E('%s last sentence' % i['id'])
        if not i.get('steps') or not i.get('why_right'): E('%s steps or why_right missing' % i['id'])
    # numeric
    if sum(1 for i in num if i.get('can_be_4')) != 1: E('can_be_4 must be true on exactly one template')
    for i in num:
        if i.get('points') != 3: E('%s points must be 3' % i['id'])
        ins = i.get('instances', [])
        if len(ins) != 8: E('%s needs 8 instances' % i['id'])
        keys = [x.get('key_value') for x in ins]
        if len(set(keys)) != len(keys): E('%s key values not all different' % i['id'])
        if len(set(x.get('stem') for x in ins)) != len(ins): E('%s stems not all different' % i['id'])
        for k, x in enumerate(ins):
            tag = '%s#%d' % (i['id'], k + 1)
            if not (isinstance(x.get('key_value'), int) and 0 <= x['key_value'] <= 99999): E('%s key_value range' % tag)
            if nw(x['stem']) > 60: E('%s stem over 60 words' % tag)
            if not last_sentence(x['stem']).startswith('You are asked to calculate'): E('%s last sentence' % tag)
            if len(x.get('steps', [])) < 2 or not all(re.search(r'\d', s) for s in x['steps']): E('%s steps need 2 or more with numbers' % tag)
            cw = x.get('common_wrong', []); vals = [x.get('key_value')] + [w.get('value') for w in cw]
            if len(cw) != 3 or len(set(vals)) != 4 or not all(isinstance(v, int) and v >= 0 for v in vals) or not all(w.get('why') for w in cw): E('%s common_wrong' % tag)
    # numeric recomputation by running the generator again
    if gen_items is not None:
        fresh = {g['id']: g for g in gen_items}
        for i in num:
            if i['id'] not in fresh: E('%s not produced by the generator' % i['id']); continue
            for k, (a, b) in enumerate(zip(i.get('instances', []), fresh[i['id']]['instances'])):
                if a != b: E('%s#%d differs from the generator output (recomputation)' % (i['id'], k + 1))
            for fld in ('unit', 'tip', 'can_be_4', 'points'):
                if i.get(fld) != fresh[i['id']].get(fld): E('%s field %s differs from the generator' % (i['id'], fld))
    # matching
    for i in mat:
        pr, rs, an = i.get('premises', []), i.get('responses', []), i.get('answer', [])
        if len(pr) != 4 or len(rs) != 5 or len(set(pr)) != 4 or len(set(rs)) != 5 or set(pr) & set(rs): E('%s premises/responses' % i['id'])
        if len(an) != 4 or len(set(an)) != 4 or not all(isinstance(a, int) and 0 <= a < 5 for a in an): E('%s answer' % i['id'])
        if len(i.get('why_wrong_rows', [])) != 4 or not i.get('steps'): E('%s why_wrong_rows or steps' % i['id'])
        if nw(i.get('intro', '')) > 60: E('%s intro over 60 words' % i['id'])
        if not last_sentence(i.get('intro', '')).startswith('You are asked to match') or 'One response is not used' not in i.get('intro', ''): E('%s intro sentences' % i['id'])
    # ordering
    for i in orde:
        st, an = i.get('steps', []), i.get('answer', [])
        if len(st) != 5 or len(set(st)) != 5: E('%s steps' % i['id'])
        if sorted(an) != [1, 2, 3, 4, 5]: E('%s answer is not a permutation of 1..5' % i['id'])
        if an == [1, 2, 3, 4, 5]: E('%s displayed order is the right order' % i['id'])
        if len(i.get('steps_solution', [])) != 5 or len(i.get('why_wrong_rows', [])) != 5: E('%s solution lists' % i['id'])
        if nw(i.get('intro', '')) > 60 or not last_sentence(i.get('intro', '')).startswith('You are asked to put'): E('%s intro' % i['id'])
    # fill
    for i in fil:
        bk, bl = i.get('bank', []), i.get('blanks', [])
        if len(bk) != 5 or len(set(x.lower() for x in bk)) != 5: E('%s bank' % i['id'])
        if len(bl) != 2: E('%s needs 2 blanks' % i['id'])
        for b in bl:
            if '____' not in b.get('sentence', '') or not (isinstance(b.get('answer'), int) and 0 <= b['answer'] < 5) or nw(b.get('sentence', '')) > 60: E('%s blank' % i['id'])
        if len(bl) == 2 and bl[0].get('answer') == bl[1].get('answer'): E('%s both blanks have the same answer' % i['id'])
        if nw(i.get('stem', '')) > 60 or not last_sentence(i.get('stem', '')).startswith('You are asked to fill'): E('%s stem' % i['id'])
        wrong = {str(k) for k in range(5)} - {str(b.get('answer')) for b in bl}
        if set((i.get('why_wrong_entries') or {}).keys()) != wrong or not i.get('steps') or not i.get('why_right'): E('%s why_wrong_entries' % i['id'])
    return errs

def report(errs, out=sys.stdout):
    for e in errs: print('  FAIL  ' + e, file=out)
    print('RESULT %s  (%d finding(s))' % ('PASS' if not errs else 'FAIL', len(errs)), file=out)

def run_check(a, ch):
    bank = json.load(open(paths(a, ch), encoding='utf-8'))
    gen = load_gen(ch)
    errs = check(bank, ch, gen.build())
    its = bank['items']
    print('Mock bank check chapter %d  file %s' % (ch, os.path.basename(paths(a, ch))))
    print('counts: choice %d numeric %d (instances %d) matching %d ordering %d fill %d'
          % tuple([sum(1 for i in its if i['type'] == t) for t in ('choice',)] + [sum(1 for i in its if i['type'] == 'numeric'), sum(len(i['instances']) for i in its if i['type'] == 'numeric')]
                  + [sum(1 for i in its if i['type'] == t) for t in ('matching', 'ordering', 'fill')]))
    print('choice points 3/4: %d/%d; answer positions %s' % (sum(1 for i in its if i['type'] == 'choice' and i['points'] == 3), sum(1 for i in its if i['type'] == 'choice' and i['points'] == 4),
                                                             [sum(1 for i in its if i['type'] == 'choice' and i['answer'] == k) for k in range(5)]))
    report(errs); return 1 if errs else 0

def run_selftest(a, ch):
    bank = json.load(open(paths(a, ch), encoding='utf-8')); gen = load_gen(ch); fresh = gen.build()
    base = check(bank, ch, fresh); print('baseline: %d finding(s)' % len(base))
    bad = 0
    # 1 a letter in a solution
    b1 = copy.deepcopy(bank); c = [i for i in b1['items'] if i['type'] == 'choice'][0]; c['why_right'] += ' Option B is the one.'
    # 2 a stem of 70 words
    b2 = copy.deepcopy(bank); c = [i for i in b2['items'] if i['type'] == 'choice'][0]; c['stem'] = ' '.join(['word'] * 68) + ' You are asked to choose.'
    # 3 a numeric instance with a changed key
    b3 = copy.deepcopy(bank); n = [i for i in b3['items'] if i['type'] == 'numeric'][0]; n['instances'][2]['key_value'] += 1
    for name, b, needle in [('letter in a solution', b1, 'letter pattern'), ('stem of 70 words', b2, 'over 60 words'), ('numeric key changed', b3, 'recomputation')]:
        e = check(b, ch, fresh); hit = any(needle in x for x in e)
        print('planted defect "%s": check %s (%d finding(s); expected finding present: %s)' % (name, 'FAILED as required' if e and hit else 'DID NOT FAIL', len(e), hit))
        if not (e and hit): bad += 1
    print('RESULT %s' % ('PASS' if bad == 0 and not base else 'FAIL')); return 0 if bad == 0 and not base else 1

# ------------------------------------------------------------------------------------------------ adapter and rules
def first_num(t):
    m = re.search(r'\d[\d,]*(?:\.\d+)?', t); return m.group(0) if m else ''
def adapt(bank):
    out = []
    for i in bank['items']:
        t = i['type']; tip = 'Tip: ' + i['tip']; base = dict(chapters=[bank['chapter']], tip=tip, needs_tip=True, sub_question='Q%s.a' % bank['chapter'])
        if t == 'choice':
            letters = 'ABCDE'
            out.append(dict(base, key=i['id'], type='ChoiceFive', q=i['stem'], options=i['options'], answer=i['answer'],
                            solution=dict(steps=i['steps'], why_right=i['why_right'], why_wrong={letters[int(k)]: v for k, v in i['why_wrong'].items()})))
        elif t == 'numeric':
            for k, x in enumerate(i['instances'], 1):
                out.append(dict(base, key='%s#%d' % (i['id'], k), type='NumericAnswer', q=x['stem'], key_value=x['key_value'], unit=i['unit'], format_line='Write the answer in %s.' % i['unit'],
                                solution=dict(steps=[dict(text=s, number=first_num(s)) for s in x['steps']], why_right=x['why_right'])))
        elif t == 'matching':
            out.append(dict(base, key=i['id'], type='Matching', q=i['intro'], premises=[dict(text=p) for p in i['premises']], responses=i['responses'],
                            solution=dict(steps=i['steps'], why_right=i['why_right'], why_wrong={str(k + 1): v for k, v in enumerate(i['why_wrong_rows'])})))
        elif t == 'ordering':
            out.append(dict(base, key=i['id'], type='Ordering', q=i['intro'], steps=i['steps'],
                            solution=dict(steps=i['steps_solution'], why_right=i['why_right'], why_wrong={str(k + 1): v for k, v in enumerate(i['why_wrong_rows'])})))
        elif t == 'fill':
            bl = [dict(text=b['sentence'], answer=i['bank'][b['answer']]) for b in i['blanks']]
            used = {b['answer'] for b in i['blanks']}
            ww = {str(k + 1): 'Entries that fail here: ' + ' '.join(i['why_wrong_entries'][str(j)] for j in sorted(map(int, i['why_wrong_entries']))) for k in range(len(bl))}
            out.append(dict(base, key=i['id'], type='FillBlankGroup', q=i['stem'], blanks=bl, distractors=[x for j, x in enumerate(i['bank']) if j not in used],
                            solution=dict(steps=i['steps'], why_right=i['why_right'], why_wrong=ww)))
    return dict(items=out)

def run_rules(a, ch):
    bank = json.load(open(paths(a, ch), encoding='utf-8')); ad = adapt(bank)
    tmp = tempfile.mkdtemp(prefix='mockrules_'); ip = os.path.join(tmp, 'items.json')
    json.dump(ad, open(ip, 'w', encoding='utf-8'))
    spec = importlib.util.spec_from_file_location('rd110', os.path.join(EXAM, 'sen0401_exam_readability_check_v1_1_0.py')); rd = importlib.util.module_from_spec(spec); spec.loader.exec_module(rd)
    rule = rd.load_rule(os.path.join(EXAM, 'sen0401_exam_readability_rule_v1_1_0.json')); units, _ = rd.read_items(ip, rule)
    print('Rules on chapter %d: %d units (numeric instances counted one by one); items shape built by an adapter (the readability tool reads only a paper and an items file together)' % (ch, len(units)))
    bad = 0
    for r, fn in [('R1', rd.check_r1), ('R2', rd.check_r2), ('R3', rd.check_r3), ('R4', rd.check_r4)]:
        f = [(u.tag(), d) for u in units for x, d in [fn(u, rule)] if x]
        print('  %s %s  fail %d of %d' % (r, 'FAIL' if f else 'PASS', len(f), len(units)));
        for t, d in f: print('       - %s (%s)' % (t, d))
        bad += len(f)
    f6 = rd.check_r6(units, rule); print('  R6 %s  fail %d of %d' % ('FAIL' if f6 else 'PASS', len(f6), len(units)))
    for u, n in f6.items(): print('       - %s (%d abbreviation(s) not spelled out at first use)' % (u.tag(), n))
    bad += len(f6)
    print('  R5 NOT_MEASURED  (cover directions only; a mock item has no cover)')
    r = subprocess.run(['nice', '-n', '10', sys.executable, '-B', os.path.join(EXAM, 'sen0401_exam_clarity_check_v1_0_1.py'), 'check', '--items', ip], capture_output=True, text=True)
    print(r.stdout.rstrip()); print(r.stderr.rstrip()) if r.stderr.strip() else None
    return 1 if (bad or r.returncode) else 0

def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); ap.add_argument('cmd', choices=['check', 'selftest', 'rules']); ap.add_argument('--bank'); ap.add_argument('--chapter', type=int, default=1)
    a = ap.parse_args()
    try: return {'check': run_check, 'selftest': run_selftest, 'rules': run_rules}[a.cmd](a, a.chapter)
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as e: print('INPUT ERROR: %s %s' % (type(e).__name__, e), file=sys.stderr); return 2
if __name__ == '__main__': sys.exit(main())
