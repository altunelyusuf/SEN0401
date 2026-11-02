#!/usr/bin/env python3
"""SEN0401 mock bank check, chapter 6, version 1.0.0. Holds no question and no answer; prints item ids only.
Usage:  mock_check_ch6_v1_0_0.py check    --bank BANK.json --gen GENERATOR.py
        mock_check_ch6_v1_0_0.py planted  --bank BANK.json --gen GENERATOR.py
Checks: schema and counts, points, word limits (stem 60, tip 12), 'You are asked to' last sentence, distinct options and length ratio,
answer spread, matching / ordering / fill structure, solution entries, no letter patterns in solutions, numeric recomputation
(the generator is run again and its templates compared with the bank), numeric key range, distinct keys and distinct numbers per instance, common_wrong.
Exit 0 when everything passes (check) or when all planted defects are caught and the clean bank passes (planted); 1 otherwise; 2 input error."""
import argparse, copy, importlib.util, json, re, sys, collections
sys.dont_write_bytecode = True

COUNTS = dict(choice=10, numeric=4, matching=3, ordering=2, fill=4)
LETTER = re.compile(r'\b(?i:options?|answers?|choices?|letters?)\s+\(?[A-E]\b|\([A-E]\)|\b[A-E]\)\s')
REQ = 'You are asked to'


def words(t): return len([w for w in t.split() if re.search(r'[A-Za-z0-9]', w)])


def last_sentence(t):
    ss = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"(])', re.sub(r'\s+', ' ', t).strip()) if s.strip()]
    return ss[-1] if ss else ''


def load_gen(path):
    spec = importlib.util.spec_from_file_location('mock_gen_check', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def solution_texts(it):
    out = []
    for k in ('steps', 'steps_solution'):
        if isinstance(it.get(k), list) and it['type'] != 'ordering' or (k == 'steps_solution' and isinstance(it.get(k), list)):
            out += [s for s in it[k] if isinstance(s, str)]
    for k in ('why_right',):
        if isinstance(it.get(k), str): out.append(it[k])
    for k in ('why_wrong', 'why_wrong_entries'):
        if isinstance(it.get(k), dict): out += [v for v in it[k].values() if isinstance(v, str)]
    for k in ('why_wrong_rows',):
        if isinstance(it.get(k), list): out += [v for v in it[k] if isinstance(v, str)]
    for ins in it.get('instances', []):
        out += ins.get('steps', []) + [ins.get('why_right', '')] + [c.get('why', '') for c in ins.get('common_wrong', [])]
    return out


def nums_of(stem): return frozenset(re.findall(r'\d[\d,]*', stem))


def check(bank, gen_path):
    F = []   # (id, message)

    def bad(i, m): F.append((i, m))
    items = bank.get('items') if isinstance(bank, dict) else None
    if not isinstance(items, list): return [('bank', 'no items list')]
    N = bank.get('chapter')
    if not isinstance(N, int): bad('bank', 'chapter missing')
    ids = [it.get('id') for it in items]
    if len(set(ids)) != len(ids): bad('bank', 'duplicate ids')
    cnt = collections.Counter(it.get('type') for it in items)
    for t, n in COUNTS.items():
        if cnt.get(t, 0) != n: bad('bank', 'count of %s is %d, need %d' % (t, cnt.get(t, 0), n))
    for it in items:
        i = it.get('id', '?'); t = it.get('type')
        if it.get('chapter') != N: bad(i, 'chapter field differs')
        if not re.match(r'^[cnmof]%s_\d+$' % N, str(i)): bad(i, 'id shape')
        for s in solution_texts(it):
            if LETTER.search(s): bad(i, 'letter pattern in a solution text')
        def stem_ok(txt, what='stem'):
            if not isinstance(txt, str) or not txt.strip(): bad(i, 'empty ' + what); return
            if words(txt) > 60: bad(i, '%s has %d words' % (what, words(txt)))
            if not last_sentence(txt).startswith(REQ): bad(i, 'last sentence of %s does not start with the required words' % what)
        def tip_ok():
            tp = it.get('tip')
            if not isinstance(tp, str) or not tp.strip(): bad(i, 'tip missing')
            elif words(tp) > 12: bad(i, 'tip has %d words' % words(tp))
        if t == 'choice':
            stem_ok(it.get('stem')); tip_ok()
            o = it.get('options'); a = it.get('answer')
            if not (isinstance(o, list) and len(o) == 5 and all(isinstance(x, str) and x.strip() for x in o)): bad(i, 'options not five strings'); continue
            if len({x.strip().lower() for x in o}) != 5: bad(i, 'options not distinct')
            if any(re.search(r'\b(all|none) of (the above|these)\b', x, re.I) for x in o): bad(i, 'all/none of the above')
            w = [words(x) for x in o]
            if max(w) > 3 * min(w): bad(i, 'option length ratio %d:%d' % (max(w), min(w)))
            if not (isinstance(a, int) and not isinstance(a, bool) and 0 <= a < 5): bad(i, 'answer index'); continue
            if it.get('points') not in (3, 4): bad(i, 'points')
            ww = it.get('why_wrong') or {}
            if set(ww) != {str(k) for k in range(5) if k != a} or any(not str(v).strip() for v in ww.values()): bad(i, 'why_wrong keys')
            if not it.get('steps') or not str(it.get('why_right', '')).strip(): bad(i, 'steps or why_right missing')
        elif t == 'numeric':
            tip_ok()
            ins = it.get('instances')
            if it.get('points') != 3: bad(i, 'numeric template points must be 3')
            if not isinstance(it.get('can_be_4'), bool): bad(i, 'can_be_4 missing')
            if not (isinstance(ins, list) and len(ins) == 8): bad(i, 'instances not 8'); continue
            keys = [x.get('key_value') for x in ins]
            if len(set(keys)) != 8: bad(i, 'key values not all different')
            if len({nums_of(x.get('stem', '')) for x in ins}) != 8: bad(i, 'stems share the same set of numbers')
            for k, x in enumerate(ins, 1):
                tag = '%s#%d' % (i, k)
                stem_ok(x.get('stem'), 'instance stem')
                if 'calculate' not in last_sentence(x.get('stem', '')): bad(tag, "last sentence lacks 'calculate'")
                kv = x.get('key_value')
                if not (isinstance(kv, int) and not isinstance(kv, bool) and 0 <= kv <= 99999): bad(tag, 'key_value not a non-negative integer of at most five digits')
                if len(x.get('steps', [])) < 2 or not all(re.search(r'\d', s) for s in x.get('steps', [])): bad(tag, 'steps: need 2 or more, each with a number')
                if not str(x.get('why_right', '')).strip(): bad(tag, 'why_right missing')
                cw = x.get('common_wrong', [])
                vals = [c.get('value') for c in cw]
                if len(cw) != 3 or len(set(vals)) != 3 or kv in vals or any(not (isinstance(v, int) and 0 <= v <= 99999) for v in vals) or any(not str(c.get('why', '')).strip() for c in cw): bad(tag, 'common_wrong')
        elif t == 'matching':
            stem_ok(it.get('intro'), 'intro'); tip_ok()
            p, r, a = it.get('premises'), it.get('responses'), it.get('answer')
            if not (isinstance(p, list) and len(p) == 4 and isinstance(r, list) and len(r) == 5): bad(i, 'premises 4 / responses 5'); continue
            if len({x.lower() for x in p}) != 4 or len({x.lower() for x in r}) != 5 or {x.lower() for x in p} & {x.lower() for x in r}: bad(i, 'premises/responses not distinct')
            if not (isinstance(a, list) and len(a) == 4 and len(set(a)) == 4 and all(isinstance(k, int) and 0 <= k < 5 for k in a)): bad(i, 'answer shape')
            if len(it.get('why_wrong_rows', [])) != 4 or any(not str(v).strip() for v in it.get('why_wrong_rows', [])): bad(i, 'why_wrong_rows')
            if not it.get('steps') or not str(it.get('why_right', '')).strip(): bad(i, 'steps or why_right missing')
        elif t == 'ordering':
            stem_ok(it.get('intro'), 'intro'); tip_ok()
            s, a = it.get('steps'), it.get('answer')
            if not (isinstance(s, list) and len(s) == 5 and len(set(s)) == 5): bad(i, 'five distinct steps'); continue
            if not (isinstance(a, list) and sorted(a) == [1, 2, 3, 4, 5]): bad(i, 'answer is not a permutation of 1..5'); continue
            if a == [1, 2, 3, 4, 5]: bad(i, 'displayed order is the right order')
            if len(it.get('steps_solution', [])) != 5 or len(it.get('why_wrong_rows', [])) != 5: bad(i, 'solution rows')
            if not str(it.get('why_right', '')).strip(): bad(i, 'why_right missing')
        elif t == 'fill':
            stem_ok(it.get('stem')); tip_ok()
            b, bl = it.get('bank'), it.get('blanks')
            if not (isinstance(b, list) and len(b) == 5 and len({x.lower() for x in b}) == 5): bad(i, 'bank of five distinct entries'); continue
            if not (isinstance(bl, list) and len(bl) == 2): bad(i, 'two blanks'); continue
            ans = [x.get('answer') for x in bl]
            if not all(isinstance(k, int) and 0 <= k < 5 for k in ans) or len(set(ans)) != 2: bad(i, 'blank answers')
            for x in bl:
                if '____' not in x.get('sentence', '') or words(x.get('sentence', '')) > 60: bad(i, 'blank sentence')
            if set((it.get('why_wrong_entries') or {})) != {'0', '1', '2', '3', '4'}: bad(i, 'why_wrong_entries keys')
            if not it.get('steps') or not str(it.get('why_right', '')).strip(): bad(i, 'steps or why_right missing')
        else:
            bad(i, 'unknown type %r' % t)
    ch = [it for it in items if it.get('type') == 'choice']
    if len(ch) == 10:
        pts = collections.Counter(it.get('points') for it in ch)
        if pts.get(3) != 4 or pts.get(4) != 6: bad('bank', 'choice points: need four of 3 and six of 4, have %s' % dict(pts))
        pos = collections.Counter(it.get('answer') for it in ch)
        sp = [pos.get(k, 0) for k in range(5)]
        if max(sp) - min(sp) > 1: bad('bank', 'answer index counts %s differ by more than 1' % sp)
    nm = [it for it in items if it.get('type') == 'numeric']
    if sum(1 for it in nm if it.get('can_be_4') is True) != 1: bad('bank', 'can_be_4 must be true on exactly one template')
    # recomputation: run the generator again and compare
    try:
        g = load_gen(gen_path); fresh = {t['id']: t for t in g.build_templates()}
        for it in nm:
            if fresh.get(it.get('id')) != it: bad(it.get('id'), 'differs from the recomputed generator output')
        if set(fresh) != {it.get('id') for it in nm}: bad('bank', 'numeric template ids differ from the generator')
    except Exception as e:
        bad('bank', 'generator run failed: %s' % type(e).__name__)
    return F


def planted(bank, gen_path):
    """Three planted defects must be caught; the clean bank must pass."""
    res = []
    clean = check(bank, gen_path); res.append(('clean bank', 'PASS' if not clean else 'FAIL', len(clean)))
    b1 = copy.deepcopy(bank); c = [it for it in b1['items'] if it['type'] == 'choice'][0]
    c['why_right'] = c['why_right'] + ' Option B is right here.'
    b2 = copy.deepcopy(bank); c2 = [it for it in b2['items'] if it['type'] == 'choice'][1]
    c2['stem'] = ' '.join(['word'] * 68) + '. You are asked to choose one.'
    b3 = copy.deepcopy(bank); n3 = [it for it in b3['items'] if it['type'] == 'numeric'][0]
    n3['instances'][3]['key_value'] += 7
    ok = not clean
    for name, b in (('planted letter in a solution', b1), ('planted stem of 70 words', b2), ('planted changed numeric key', b3)):
        f = check(b, gen_path); caught = len(f) > 0; res.append((name, 'CAUGHT (check FAILS as it must)' if caught else 'NOT CAUGHT', len(f))); ok = ok and caught
    return ok, res


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); sub = ap.add_subparsers(dest='cmd', required=True)
    for n in ('check', 'planted'):
        p = sub.add_parser(n); p.add_argument('--bank', required=True); p.add_argument('--gen', required=True)
    a = ap.parse_args()
    try:
        bank = json.load(open(a.bank, encoding='utf-8'))
    except (OSError, ValueError) as e:
        print('INPUT ERROR: %s' % type(e).__name__, file=sys.stderr); return 2
    if a.cmd == 'check':
        F = check(bank, a.gen); items = bank['items']
        cnt = collections.Counter(it['type'] for it in items)
        print('Mock bank check v1.0.0  chapter %s  items %d  (%s)' % (bank.get('chapter'), len(items), ', '.join('%s %d' % (k, cnt[k]) for k in sorted(cnt))))
        print('numeric instances %d' % sum(len(it.get('instances', [])) for it in items if it.get('type') == 'numeric'))
        for i, m in F: print('  FAIL %s: %s' % (i, m))
        print('RESULT %s (%d failure(s))' % ('PASS' if not F else 'FAIL', len(F)))
        return 0 if not F else 1
    ok, res = planted(bank, a.gen)
    print('Mock bank check v1.0.0, planted-defect test, chapter %s' % bank.get('chapter'))
    for n, s, k in res: print('  %-32s %-34s (%d failure line(s) reported)' % (n, s, k))
    print('RESULT %s' % ('PASS (all three planted defects caught, clean bank passes)' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
