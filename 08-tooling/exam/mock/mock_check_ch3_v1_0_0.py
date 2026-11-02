#!/usr/bin/env python3
"""SEN0401 mock bank checker for one chapter, version 1.0.0. Holds NO question, option or answer text: it reads the bank file it is given.
Checks: schema and counts, points, word limits, distinct options, answer spread, numeric recomputation (the generator is run again and compared),
no option letters in solutions, matching/ordering/fill structure, and the readability rules R1, R2, R3, R6 (R4 and R5 are about the paper and are NOT_MEASURED)
and the clarity rules C1 to C5 through the two existing tools (imported, not copied), on an adapter that turns the bank into the items-file shape.
Usage:
  check    --bank BANK.json --gen GENERATOR.py --chapter N [--tools DIR]
  selftest --bank BANK.json --gen GENERATOR.py --chapter N [--tools DIR]     (three planted defects; each must FAIL, the clean bank must PASS)
Exit code 0 = all clear (selftest: every planted defect caught), 1 = a failure."""
import argparse, copy, importlib.util, json, os, re, subprocess, sys, tempfile
sys.dont_write_bytecode = True
DEFAULT_TOOLS = '/home/claude/sen0401/08-tooling/exam'


def nwords(t): return len([w for w in str(t).split() if re.search(r'[A-Za-z0-9]', w)])


def load_tool(tools, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(tools, name + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


LETTER_PATTERNS = [r'\b[Oo]ption\s+[A-E]\b', r'\b[Aa]nswer\s+[A-E]\b', r'\b[Cc]hoice\s+[A-E]\b', r'\([A-E]\)', r'(?:^|\s)[A-E]\)\s', r'\bletter\s+[A-E]\b', r'\b[Rr]esponse\s+[A-E]\b']


def solution_texts(it):
    t = it['type']; out = []
    if t == 'numeric':
        for ins in it['instances']:
            out += ins['steps'] + [ins['why_right']] + [c['why'] for c in ins['common_wrong']]
        return out
    out += list(it.get('steps_solution') or []) if t == 'ordering' else list(it.get('steps') or [])
    out.append(it.get('why_right', ''))
    for k in ('why_wrong', 'why_wrong_entries'):
        if isinstance(it.get(k), dict): out += list(it[k].values())
    if isinstance(it.get('why_wrong_rows'), list): out += it['why_wrong_rows']
    return [x for x in out if isinstance(x, str)]


def last_sentence_ok(stem):
    ss = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"(])', re.sub(r'\s+', ' ', stem).strip()) if s]
    return bool(ss) and ss[-1].startswith('You are asked to')


def structure(bank, ch, gen, fails):
    F = lambda m: fails.append(m)
    items = bank.get('items', [])
    if bank.get('chapter') != ch: F('chapter field is not %d' % ch)
    ids = [i.get('id') for i in items]
    if len(set(ids)) != len(ids): F('duplicate ids')
    by = {}
    for i in items: by.setdefault(i.get('type'), []).append(i)
    want = {'choice': 10, 'numeric': 4, 'matching': 3, 'ordering': 2, 'fill': 4}
    for t, n in want.items():
        if len(by.get(t, [])) != n: F('count of %s is %d, want %d' % (t, len(by.get(t, [])), n))
    for i in items:
        if not re.fullmatch(r'[cnmof]%d_\d+' % ch, str(i.get('id'))): F('bad id %s' % i.get('id'))
        if i.get('chapter') != ch: F('%s chapter field' % i.get('id'))
    # ---- choice
    ch_items = by.get('choice', [])
    pts = sorted(i.get('points') for i in ch_items)
    if pts != [3] * 4 + [4] * 6: F('choice points %s, want four of 3 and six of 4' % pts)
    pos = [0] * 5
    for i in ch_items:
        n = i['id']; o = i.get('options', [])
        if len(o) != 5: F('%s has %d options' % (n, len(o))); continue
        if len({re.sub(r'\W+', ' ', x.lower()).strip() for x in o}) != 5: F('%s options not distinct' % n)
        a = i.get('answer')
        if not (isinstance(a, int) and not isinstance(a, bool) and 0 <= a < 5): F('%s answer not an index' % n); continue
        pos[a] += 1
        ws = [nwords(x) for x in o]
        if min(ws) == 0 or max(ws) > 3 * min(ws): F('%s longest option %d words, shortest %d' % (n, max(ws), min(ws)))
        if any(re.search(r'all of the above|none of the above|all of these|none of these', x, re.I) for x in o): F('%s all/none of the above' % n)
        if sorted(i.get('why_wrong', {}).keys()) != sorted(str(k) for k in range(5) if k != a): F('%s why_wrong keys are not the four wrong indices' % n)
        if not i.get('steps') or not i.get('why_right'): F('%s lacks steps or why_right' % n)
    if ch_items and max(pos) - min(pos) > 1: F('answer positions %s differ by more than 1' % pos)
    # ---- numeric
    nums = by.get('numeric', [])
    if sum(1 for n in nums if n.get('can_be_4')) != 1: F('numeric templates with can_be_4 true: %d, want 1' % sum(1 for n in nums if n.get('can_be_4')))
    for n in nums:
        if n.get('points') != 3: F('%s points not 3' % n['id'])
        ins = n.get('instances', [])
        if len(ins) != 8: F('%s has %d instances' % (n['id'], len(ins))); continue
        keys = [x.get('key_value') for x in ins]
        if len(set(keys)) != 8: F('%s key values not all different' % n['id'])
        if len({x.get('stem') for x in ins}) != 8: F('%s stems not all different' % n['id'])
        for x in ins:
            k = x.get('key_value')
            if not (isinstance(k, int) and not isinstance(k, bool) and 0 <= k <= 99999): F('%s key %r not a non-negative integer of at most five digits' % (n['id'], k))
            cw = x.get('common_wrong', [])
            vals = [k] + [c.get('value') for c in cw]
            if len(cw) != 3 or len(set(vals)) != 4: F('%s common_wrong not three values different from key and each other' % n['id'])
            if any(not c.get('why') for c in cw): F('%s common_wrong without a named mistake' % n['id'])
            if len(x.get('steps', [])) < 2 or not any(re.search(r'\d', s) for s in x.get('steps', [])): F('%s needs 2+ steps with numbers' % n['id'])
            if not last_sentence_ok(x.get('stem', '')) or not x['stem'].split('You are asked to')[-1].lstrip().startswith('calculate'): F('%s stem intention sentence' % n['id'])
            if nwords(x.get('stem', '')) > 60: F('%s stem over 60 words' % n['id'])
        if nwords(n.get('tip', '')) > 12 or not n.get('tip'): F('%s tip' % n['id'])
    # ---- matching, ordering, fill
    for m in by.get('matching', []):
        n = m['id']; p, r, a = m.get('premises', []), m.get('responses', []), m.get('answer', [])
        if len(p) != 4 or len(r) != 5 or len(set(p)) != 4 or len(set(r)) != 5: F('%s premises/responses shape' % n)
        if len(a) != 4 or len(set(a)) != 4 or any(not (isinstance(x, int) and 0 <= x < 5) for x in a): F('%s answer not 4 distinct response indices' % n)
        if len(m.get('why_wrong_rows', [])) != 4 or not all(m.get('why_wrong_rows', [])): F('%s why_wrong_rows' % n)
        if not m.get('steps') or not m.get('why_right'): F('%s lacks steps or why_right' % n)
        if not last_sentence_ok(m.get('intro', '')) or nwords(m.get('intro', '')) > 60: F('%s intro' % n)
        if not m.get('tip') or nwords(m['tip']) > 12: F('%s tip' % n)
    for o in by.get('ordering', []):
        n = o['id']; s, a = o.get('steps', []), o.get('answer', [])
        if len(s) != 5 or len(set(s)) != 5: F('%s steps shape' % n)
        if sorted(a) != [1, 2, 3, 4, 5]: F('%s answer is not a permutation of 1..5' % n)
        elif a == [1, 2, 3, 4, 5]: F('%s displayed order is the right order' % n)
        sol = o.get('steps_solution', [])
        if len(sol) != 5 or (sorted(a) == [1, 2, 3, 4, 5] and any(sol[a[k] - 1] != s[k] for k in range(5))): F('%s steps_solution does not agree with answer' % n)
        if len(o.get('why_wrong_rows', [])) != 5 or not all(o.get('why_wrong_rows', [])): F('%s why_wrong_rows' % n)
        if not last_sentence_ok(o.get('intro', '')) or nwords(o.get('intro', '')) > 60: F('%s intro' % n)
        if not o.get('tip') or nwords(o['tip']) > 12 or not o.get('why_right'): F('%s tip or why_right' % n)
    for f in by.get('fill', []):
        n = f['id']; b, bl = f.get('bank', []), f.get('blanks', [])
        if len(b) != 5 or len({x.lower() for x in b}) != 5: F('%s bank shape' % n)
        if len(bl) != 2 or any('____' not in x.get('sentence', '') for x in bl): F('%s blanks shape' % n)
        ans = [x.get('answer') for x in bl]
        if len(set(ans)) != 2 or any(not (isinstance(x, int) and 0 <= x < 5) for x in ans): F('%s blank answers' % n)
        if sorted(f.get('why_wrong_entries', {}).keys()) != ['0', '1', '2', '3', '4']: F('%s why_wrong_entries keys' % n)
        if not last_sentence_ok(f.get('stem', '')) or nwords(f.get('stem', '')) > 60: F('%s stem' % n)
        if not f.get('tip') or nwords(f['tip']) > 12 or not f.get('steps') or not f.get('why_right'): F('%s tip/steps/why_right' % n)
        if any(nwords(x['sentence']) > 60 for x in bl): F('%s sentence over 60 words' % n)
    # ---- choice stems
    for i in ch_items:
        if not last_sentence_ok(i.get('stem', '')): F('%s last sentence does not start You are asked to' % i['id'])
        if nwords(i.get('stem', '')) > 60: F('%s stem over 60 words (%d)' % (i['id'], nwords(i['stem'])))
        if not i.get('tip') or nwords(i['tip']) > 12: F('%s tip missing or over 12 words' % i['id'])
    # ---- letters in solutions
    for i in items:
        for t in solution_texts(i):
            if any(re.search(p, t) for p in LETTER_PATTERNS): F('%s a solution names an option by letter' % i['id']); break
    # ---- numeric recomputation: run the generator again and compare
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, 'regen.json')
        r = subprocess.run(['nice', '-n', '10', sys.executable, gen, '--out', out], capture_output=True, text=True)
        if r.returncode != 0: F('generator failed: %s' % r.stderr.strip().splitlines()[-1:])
        else:
            regen = {i['id']: i for i in json.load(open(out, encoding='utf-8'))['items'] if i['type'] == 'numeric'}
            for n in nums:
                if regen.get(n['id']) != n: F('%s numeric template differs from the generator output (recomputation)' % n['id'])
    return by


def adapt(bank):
    """Bank -> items-file shape of the readability and clarity tools (adapter; the bank files themselves keep option indices)."""
    out = []
    for it in bank['items']:
        t = it['type']; tip = ('Tip: ' + it['tip']) if it.get('tip') else None
        if t == 'choice':
            ww = {chr(65 + int(k)): v for k, v in it['why_wrong'].items()}
            out.append(dict(key=it['id'], type='ChoiceFive', q=it['stem'], tip=tip, options=it['options'], answer=it['answer'],
                            solution=dict(steps=[dict(text=s, number=str(n + 1)) for n, s in enumerate(it['steps'])], why_right=it['why_right'], why_wrong=ww)))
        elif t == 'numeric':
            for k, ins in enumerate(it['instances'], 1):
                st = [dict(text=s, number=(re.findall(r'\d[\d,.]*', s) or [''])[0]) for s in ins['steps']]
                out.append(dict(key='%s#%d' % (it['id'], k), type='NumericAnswer', q=ins['stem'], tip=tip, unit=it['unit'], solution=dict(steps=st, why_right=ins['why_right'])))
        elif t == 'matching':
            out.append(dict(key=it['id'], type='Matching', instruction=it['intro'], tip=tip, premises=[dict(text=p) for p in it['premises']], responses=it['responses'],
                            solution=dict(steps=[dict(text=s, number=str(n + 1)) for n, s in enumerate(it['steps'])], why_right=it['why_right'],
                                          why_wrong={str(n + 1): v for n, v in enumerate(it['why_wrong_rows'])})))
        elif t == 'ordering':
            out.append(dict(key=it['id'], type='Ordering', instruction=it['intro'], tip=tip, steps=it['steps'],
                            solution=dict(steps=[dict(text=s, number=str(n + 1)) for n, s in enumerate(it['steps_solution'])], why_right=it['why_right'],
                                          why_wrong={str(n + 1): v for n, v in enumerate(it['why_wrong_rows'])})))
        elif t == 'fill':
            used = {b['answer'] for b in it['blanks']}
            ww = {str(n + 1): ' '.join(it['why_wrong_entries'][str(e)] for e in range(len(it['bank'])) if e != b['answer']) for n, b in enumerate(it['blanks'])}
            out.append(dict(key=it['id'], type='FillBlankGroup', q=it['stem'], tip=tip, blanks=[dict(text=b['sentence'], answer=it['bank'][b['answer']]) for b in it['blanks']],
                            distractors=[it['bank'][e] for e in range(len(it['bank'])) if e not in used],
                            solution=dict(steps=[dict(text=s, number=str(n + 1)) for n, s in enumerate(it['steps'])], why_right=it['why_right'], why_wrong=ww)))
    return out


def tools_run(bank, tools, fails, report):
    rd = load_tool(tools, 'sen0401_exam_readability_check_v1_1_0'); cl = load_tool(tools, 'sen0401_exam_clarity_check_v1_0_1')
    rrule = rd.load_rule(os.path.join(tools, 'sen0401_exam_readability_rule_v1_1_0.json'))
    crule = json.load(open(os.path.join(tools, 'sen0401_exam_clarity_rule_v1_0_0.json'), encoding='utf-8'))
    items = adapt(bank)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'adapted.json'); json.dump(dict(items=items), open(p, 'w'))
        iu, itips = rd.read_items(p, rrule)
        res = rd.run_source('adapted bank', iu, None, itips, rrule, False)
        for r in ('R1', 'R2', 'R3', 'R4', 'R6'):
            x = res[r]
            if x['status'] != 'MEASURED': report.append('  %-4s NOT_MEASURED  (%s)' % (r, x['why']))
            else:
                report.append('  %-4s %s  fail %d of %d' % (r, 'FAIL' if x['fail'] else 'PASS', len(x['fail']), x['checked']))
                for tag, d in x['fail']: report.append('         - %s (%s)' % (tag, d)); fails.append('readability %s %s' % (r, tag))
        report.append('  R5   NOT_MEASURED  (cover rule; a bank has no cover)')
        # R6 for every item read alone (stricter: items are drawn into mocks in any order)
        bad = []
        for u in iu:
            f6 = rd.check_r6([u], rrule)
            if f6: bad.append(u.tag())
        report.append('  R6 each item alone  %s  fail %d of %d' % ('FAIL' if bad else 'PASS', len(bad), len(iu)))
        for t in bad: report.append('         - %s' % t); fails.append('readability R6 alone %s' % t)
        cu = cl.read_items(p, crule); cres = cl.run_items(cu, crule)
        for r in ('C1', 'C2', 'C3', 'C4', 'C5'):
            x = cres[r]
            report.append('  %-4s %s  fail %d of %d' % (r, 'FAIL' if x['fail'] else 'PASS', len(x['fail']), x['checked']))
            for tag, d in x['fail']: report.append('         - %s (%s)' % (tag, d)); fails.append('clarity %s %s' % (r, tag))
        report.append('  C4 plausibility of options and trick wording: NOT_MEASURED (human judgement)')
    return len(items)


def run_check(bank, gen, ch, tools, quiet=False):
    fails, report = [], []
    structure(bank, ch, gen, fails)
    n = tools_run(bank, tools, fails, report)
    if not quiet:
        print('Structure and content checks: %s (%d failure(s))' % ('PASS' if not [f for f in fails if not f.startswith(('readability', 'clarity'))] else 'FAIL', len([f for f in fails if not f.startswith(('readability', 'clarity'))])))
        for f in fails:
            if not f.startswith(('readability', 'clarity')): print('  - ' + f)
        print('Rule tools on the adapter (%d units: items, numeric instances counted one each):' % n)
        print('\n'.join(report))
    return fails


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    for c in ('check', 'selftest'):
        p = sub.add_parser(c); p.add_argument('--bank', required=True); p.add_argument('--gen', required=True); p.add_argument('--chapter', type=int, required=True); p.add_argument('--tools', default=DEFAULT_TOOLS)
    a = ap.parse_args()
    bank = json.load(open(a.bank, encoding='utf-8'))
    if a.cmd == 'check':
        fails = run_check(bank, a.gen, a.chapter, a.tools)
        print('RESULT %s  (%d failure(s))' % ('PASS' if not fails else 'FAIL', len(fails)))
        return 1 if fails else 0
    # selftest
    print('Selftest: the clean bank must PASS, each planted defect must FAIL')
    clean = run_check(bank, a.gen, a.chapter, a.tools, quiet=True)
    print('  clean bank: %s (%d failure(s))' % ('PASS' if not clean else 'FAIL', len(clean)))
    ok = not clean
    cases = []
    b1 = copy.deepcopy(bank); c = [i for i in b1['items'] if i['type'] == 'choice'][0]; c['why_right'] += ' Option B is the one.'; cases.append(('a letter in a solution', b1))
    b2 = copy.deepcopy(bank); c = [i for i in b2['items'] if i['type'] == 'choice'][1]
    c['stem'] = ' '.join(['filler'] * 66) + '. You are asked to choose one.'; cases.append(('a stem of 70 words', b2))
    b3 = copy.deepcopy(bank); n = [i for i in b3['items'] if i['type'] == 'numeric'][0]; n['instances'][3]['key_value'] += 1; cases.append(('a numeric instance with a changed key', b3))
    for name, b in cases:
        f = run_check(b, a.gen, a.chapter, a.tools, quiet=True)
        want = {'a letter in a solution': 'by letter', 'a stem of 70 words': 'over 60 words', 'a numeric instance with a changed key': 'differs from the generator'}[name]
        caught = any(want in x for x in f)
        ok = ok and caught
        print('  planted defect "%s": %s (%d failure(s); expected reason found: %s)' % (name, 'caught (FAIL as expected)' if caught else 'NOT CAUGHT', len(f), caught))
    print('SELFTEST %s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
