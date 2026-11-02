#!/usr/bin/env python3
"""SEN0401 mock bank, chapter 5: own check v1.0.0. Reads mock_bank_ch5_v1_0_0.json (private) and re-runs the numeric generator.
Prints item ids and failure reasons only, never item text. Modes: (default) check the bank; --planted run three planted defects that must FAIL."""
import copy, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BANK = os.path.join(HERE, 'mock_bank_ch5_v1_0_0.json')
CH = 5
LETTER = re.compile(r'\b(?:option|answer|choice|response)s?\s+\(?[A-E]\)?(?![a-z])|\(\s*[A-E]\s*\)|\bletter\s+[A-E]\b', re.I)


def nw(t): return len([w for w in t.split() if re.search(r'[A-Za-z0-9]', w)])


def last_sentence(t):
    ss = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"(])', re.sub(r'\s+', ' ', t).strip()) if s.strip()]
    return ss[-1] if ss else ''


def texts_of(it):
    """every solution string of an item (for the letter test)"""
    out = []
    def walk(x):
        if isinstance(x, str): out.append(x)
        elif isinstance(x, list): [walk(y) for y in x]
        elif isinstance(x, dict): [walk(y) for y in x.values()]
    for k in ('steps', 'why_right', 'why_wrong', 'why_wrong_rows', 'why_wrong_entries', 'steps_solution', 'instances'):
        if k in it: walk(it[k])
    return out


def stem_ok(f, iid, text, tip, kind='stem'):
    if nw(text) > 60: f.append((iid, '%s %d words' % (kind, nw(text))))
    if not last_sentence(text).startswith('You are asked to'): f.append((iid, '%s last sentence does not start with the required words' % kind))
    if tip is not None and (not tip.strip() or nw(tip) > 12): f.append((iid, 'tip %d words' % nw(tip)))


def check(bank, regen):
    f = []
    items = bank.get('items', [])
    if bank.get('chapter') != CH: f.append(('bank', 'chapter field'))
    ids = [i.get('id') for i in items]
    if len(set(ids)) != len(ids): f.append(('bank', 'duplicate ids'))
    by = {}
    for i in items: by.setdefault(i.get('type'), []).append(i)
    want = {'choice': 10, 'numeric': 4, 'matching': 3, 'ordering': 2, 'fill': 4}
    for t, n in want.items():
        if len(by.get(t, [])) != n: f.append(('bank', 'count of %s is %d, need %d' % (t, len(by.get(t, [])), n)))
    ch = by.get('choice', [])
    if sorted(c.get('points') for c in ch) != [3] * 4 + [4] * 6: f.append(('bank', 'choice points are not 4 x 3 and 6 x 4'))
    if sum(1 for n in by.get('numeric', []) if n.get('can_be_4') is True) != 1: f.append(('bank', 'can_be_4 not true on exactly one template'))
    pos = [c.get('answer') for c in ch]
    cnt = [pos.count(k) for k in range(5)]
    if max(cnt) - min(cnt) > 1: f.append(('bank', 'answer positions %s differ by more than 1' % cnt))
    for it in items:
        iid = it.get('id', '?'); t = it.get('type')
        if it.get('chapter') != CH: f.append((iid, 'chapter'))
        for s in texts_of(it):
            if LETTER.search(s): f.append((iid, 'letter pattern in a solution'))
        if t == 'choice':
            stem_ok(f, iid, it['stem'], it.get('tip'))
            o = it['options']; low = [x.strip().lower() for x in o]
            if len(o) != 5 or len(set(low)) != 5 or any(not x for x in low): f.append((iid, 'options not five distinct non-empty'))
            if any(re.search(r'(all|none) of (the above|these)', x) for x in low): f.append((iid, 'all/none of the above'))
            ws = [nw(x) for x in o]
            if ws and min(ws) and max(ws) > 3 * min(ws): f.append((iid, 'longest %d words, shortest %d' % (max(ws), min(ws))))
            if not (isinstance(it['answer'], int) and 0 <= it['answer'] < 5): f.append((iid, 'answer index'))
            else:
                if set(it['why_wrong']) != {str(k) for k in range(5) if k != it['answer']} or any(not v.strip() for v in it['why_wrong'].values()): f.append((iid, 'why_wrong keys'))
            if len(it['steps']) < 1 or not it['why_right'].strip(): f.append((iid, 'solution'))
        elif t == 'numeric':
            stem_ok(f, iid, 'x', it.get('tip'), 'tip') if False else None
            if nw(it.get('tip', '')) > 12 or not it.get('tip'): f.append((iid, 'tip'))
            if it.get('points') != 3 or not isinstance(it.get('can_be_4'), bool): f.append((iid, 'points or can_be_4'))
            inst = it['instances']
            if len(inst) != 8: f.append((iid, 'instances %d' % len(inst)))
            keys = [x['key_value'] for x in inst]
            if len(set(keys)) != len(keys): f.append((iid, 'key values not all different'))
            if len({x['stem'] for x in inst}) != len(inst): f.append((iid, 'stems not all different'))
            for k, x in enumerate(inst, 1):
                tag = '%s#%d' % (iid, k)
                stem_ok(f, tag, x['stem'], None)
                if not re.search(r'You are asked to calculate', last_sentence(x['stem'])): f.append((tag, 'stem does not ask to calculate'))
                kv = x['key_value']
                if not (isinstance(kv, int) and not isinstance(kv, bool) and 0 <= kv <= 99999): f.append((tag, 'key_value not a non-negative integer of at most 5 digits'))
                if len(x['steps']) < 2 or not all(re.search(r'\d', s) for s in x['steps']): f.append((tag, 'steps need 2 or more, each with a number'))
                cw = [c['value'] for c in x['common_wrong']]
                if len(cw) != 3 or len(set(cw + [kv])) != 4 or any(not isinstance(v, int) or v < 0 for v in cw) or any(not c['why'].strip() for c in x['common_wrong']): f.append((tag, 'common_wrong not 3 different integers different from the key, each with a reason'))
            # recomputation by running the generator again
            g = {t_['id']: t_ for t_ in regen}.get(iid)
            if g is None or json.dumps(g, sort_keys=True) != json.dumps(it, sort_keys=True): f.append((iid, 'does not equal the generator output'))
        elif t == 'matching':
            stem_ok(f, iid, it['intro'], it.get('tip'), 'intro')
            P, R = it['premises'], it['responses']
            if len(P) != 4 or len(R) != 5 or len(set(x.lower() for x in P + R)) != 9: f.append((iid, 'need 4 premises and 5 responses, all distinct'))
            a = it['answer']
            if len(a) != 4 or len(set(a)) != 4 or any(not (isinstance(x, int) and 0 <= x < 5) for x in a): f.append((iid, 'answer not 4 distinct response indices'))
            if len(it['why_wrong_rows']) != 4 or any(not s.strip() for s in it['why_wrong_rows']) or not it['steps'] or not it['why_right'].strip(): f.append((iid, 'solution'))
            if not re.search(r'one (?:response|feature|meaning|result|item) is not used', last_sentence(it['intro'])): f.append((iid, 'last sentence does not say that one response is unused'))
        elif t == 'ordering':
            stem_ok(f, iid, it['intro'], it.get('tip'), 'intro')
            s = it['steps']; a = it['answer']
            if len(s) != 5 or len(set(x.lower() for x in s)) != 5: f.append((iid, 'need 5 distinct steps'))
            if sorted(a) != [1, 2, 3, 4, 5]: f.append((iid, 'answer not a permutation of 1..5'))
            elif a == [1, 2, 3, 4, 5]: f.append((iid, 'displayed order equals the right order'))
            if len(it['steps_solution']) != 5 or len(it['why_wrong_rows']) != 5 or any(not x.strip() for x in it['steps_solution'] + it['why_wrong_rows']) or not it['why_right'].strip(): f.append((iid, 'solution'))
        elif t == 'fill':
            stem_ok(f, iid, it['stem'], it.get('tip'))
            b = it['bank']; bl = it['blanks']
            if len(b) != 5 or len(set(x.lower() for x in b)) != 5: f.append((iid, 'bank not 5 distinct entries'))
            if len(bl) != 2 or any('____' not in x['sentence'] for x in bl): f.append((iid, 'need 2 blanks marked ____'))
            ans = [x['answer'] for x in bl]
            if len(set(ans)) != 2 or any(not (isinstance(x, int) and 0 <= x < 5) for x in ans): f.append((iid, 'blank answers'))
            else:
                unused = {str(k) for k in range(5)} - {str(x) for x in ans}
                if set(it['why_wrong_entries']) != unused or any(not v.strip() for v in it['why_wrong_entries'].values()): f.append((iid, 'why_wrong_entries must cover the unused bank entries'))
            if not it['steps'] or not it['why_right'].strip(): f.append((iid, 'solution'))
        else: f.append((iid, 'unknown type'))
    return f


def planted(bank, regen):
    res = []
    b = copy.deepcopy(bank); [i for i in b['items'] if i['id'] == 'c5_03'][0]['why_right'] = 'This is Option B because it follows from the passphrase.'
    res.append(('P1 a letter in a solution', check(b, regen)))
    b = copy.deepcopy(bank); c = [i for i in b['items'] if i['id'] == 'c5_04'][0]; c['stem'] = ' '.join(['word'] * 68) + '. You are asked to choose one.'
    res.append(('P2 a stem of 70 words', check(b, regen)))
    b = copy.deepcopy(bank); n = [i for i in b['items'] if i['id'] == 'n5_2'][0]; n['instances'][3]['key_value'] += 1
    res.append(('P3 a numeric instance with a changed key', check(b, regen)))
    return res


def main():
    import mock_numeric_gen_ch5_v1_0_0 as gen
    regen = json.loads(json.dumps(gen.build()))
    with open(BANK, encoding='utf-8') as fh: bank = json.load(fh)
    rc = 0
    if '--planted' in sys.argv:
        print('Planted-defect test, chapter %d (each defect must produce a failure)' % CH)
        for name, fails in planted(bank, regen):
            ok = bool(fails)
            print('  %-45s %s  (%d failure(s): %s)' % (name, 'DETECTED' if ok else 'MISSED', len(fails), '; '.join('%s %s' % x for x in fails[:3])))
            if not ok: rc = 1
        print('Clean bank on the same run: %s' % ('PASS' if not check(bank, regen) else 'FAIL'))
        print('RESULT %s' % ('PASS (all 3 planted defects detected)' if rc == 0 else 'FAIL'))
        return rc
    fails = check(bank, regen)
    c = {t: sum(1 for i in bank['items'] if i['type'] == t) for t in ('choice', 'numeric', 'matching', 'ordering', 'fill')}
    pos = [sum(1 for i in bank['items'] if i['type'] == 'choice' and i['answer'] == k) for k in range(5)]
    print('Mock bank check, chapter %d: counts %s, choice answer positions %s, numeric instances %d' % (CH, c, pos, sum(len(i['instances']) for i in bank['items'] if i['type'] == 'numeric')))
    for x in fails: print('  FAIL %s  %s' % x)
    print('RESULT %s' % ('PASS' if not fails else 'FAIL (%d)' % len(fails)))
    return 0 if not fails else 1


if __name__ == '__main__': sys.exit(main())
