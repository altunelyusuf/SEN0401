#!/usr/bin/env python3
"""SEN0401 mock bank check, one chapter file (run for chapter 2). Holds NO item text; prints item ids and counts only.
Usage:  mock_check_ch2_v1_0_0.py check [--bank BANK.json]      selftest (three planted defects must FAIL)
Exit 0 all clear, 1 a failure."""
import argparse, copy, importlib, json, math, os, re, sys, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CH = 2
SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"(])')

def nw(t): return len([w for w in t.split() if re.search(r'[A-Za-z0-9]', w)])
def last_sentence(t): return [s for s in SENT.split(' '.join(t.split())) if s.strip()][-1]
LETTER = re.compile(r"\b(?:option|options|answer|choice|alternative)\s+\(?[A-E]\b|\(\s*[A-E]\s*\)|\b[A-E]\)|\bletter\b", re.I)

def text_fields(it):
    t = it['type']; out = []
    out += it.get('steps', []) if t != 'ordering' else it.get('steps_solution', [])
    out.append(it.get('why_right', ''))
    out += list(it.get('why_wrong', {}).values()) + list(it.get('why_wrong_rows', [])) + list(it.get('why_wrong_entries', {}).values())
    if t == 'numeric':
        for ins in it['instances']:
            out += ins['steps'] + [ins['why_right']] + [w['why'] for w in ins['common_wrong']]
    return [x for x in out if isinstance(x, str)]

def ints(s): return [int(x.replace(',', '')) for x in re.findall(r'\d[\d,]*\d|\d', s)]

def recompute(tid, stem):
    n = ints(stem)
    if tid == 'n%d_1' % CH: return -(-(4 * n[0] + n[1]) // 4)
    if tid == 'n%d_2' % CH: return n[0] - n[1] - n[3] * n[2]
    if tid == 'n%d_3' % CH: return int(round(math.log2(n[0])))
    if tid == 'n%d_4' % CH: return n[0] + n[2] - 1 - n[3]
    return None

def check_bank(bank, regen=None):
    F = []  # (id, rule)
    def bad(i, r): F.append((i, r))
    items = bank.get('items', [])
    if bank.get('chapter') != CH: bad('bank', 'chapter field')
    cnt = collections.Counter(i['type'] for i in items)
    for t, n in dict(choice=10, numeric=4, matching=3, ordering=2, fill=4).items():
        if cnt[t] != n: bad('bank', 'count %s %d != %d' % (t, cnt[t], n))
    ids = [i['id'] for i in items]
    if len(set(ids)) != len(ids): bad('bank', 'duplicate ids')
    ch = [i for i in items if i['type'] == 'choice']
    pts = collections.Counter(i['points'] for i in ch)
    if pts.get(3) != 4 or pts.get(4) != 6: bad('bank', 'choice points %s' % dict(pts))
    pos = collections.Counter(i['answer'] for i in ch)
    if len(ch) == 10 and max(pos.get(k, 0) for k in range(5)) - min(pos.get(k, 0) for k in range(5)) > 1: bad('bank', 'answer spread %s' % dict(pos))
    c4 = [i for i in items if i['type'] == 'numeric' and i.get('can_be_4')]
    if len(c4) != 1: bad('bank', 'can_be_4 count %d' % len(c4))
    for it in items:
        i = it['id']; t = it['type']
        if it.get('chapter') != CH: bad(i, 'chapter')
        stem = it.get('stem') or it.get('intro') or ''
        if t == 'numeric': stems = [x['stem'] for x in it['instances']]
        else: stems = [stem]
        for s in stems:
            if nw(s) > 60: bad(i, 'stem over 60 words (%d)' % nw(s))
            if not last_sentence(s).startswith('You are asked to'): bad(i, 'last sentence')
            if t == 'numeric' and not last_sentence(s).startswith('You are asked to calculate'): bad(i, 'last sentence calculate')
            if ':' in s: bad(i, 'colon in stem')
        if t == 'fill':
            for b in it['blanks']:
                if '____' not in b['sentence']: bad(i, 'blank marker')
        if nw(it.get('tip', '')) > 12 or not it.get('tip'): bad(i, 'tip words')
        for x in text_fields(it):
            if LETTER.search(x): bad(i, 'letter pattern in solution')
        if t in ('choice', 'matching', 'fill') and not it.get('why_right'): bad(i, 'why_right')
        if t == 'choice':
            o = it['options']
            if len(o) != 5 or len(set(x.lower() for x in o)) != 5: bad(i, 'options not 5 distinct')
            if not isinstance(it['answer'], int) or not 0 <= it['answer'] < 5: bad(i, 'answer index')
            ws = [nw(x) for x in o]
            if max(ws) > 3 * min(ws): bad(i, 'length ratio')
            if any(re.search(r'(all|none) of (the above|these)', x, re.I) for x in o): bad(i, 'all/none')
            if sorted(it['why_wrong'].keys()) != sorted(str(k) for k in range(5) if k != it['answer']): bad(i, 'why_wrong keys')
            if any(not v.strip() for v in it['why_wrong'].values()): bad(i, 'why_wrong empty')
            if len(it['steps']) < 1: bad(i, 'steps')
        elif t == 'numeric':
            ins = it['instances']
            if len(ins) != 8: bad(i, 'instances %d' % len(ins))
            keys = [x['key_value'] for x in ins]
            if len(set(keys)) != len(keys): bad(i, 'keys not all different')
            if len(set(x['stem'] for x in ins)) != len(ins): bad(i, 'stems not all different')
            if it['points'] != 3 or not isinstance(it.get('can_be_4'), bool) or not it.get('unit'): bad(i, 'points/can_be_4/unit')
            for k, x in enumerate(ins):
                tag = '%s#%d' % (i, k + 1)
                kv = x['key_value']
                if not isinstance(kv, int) or isinstance(kv, bool) or kv < 0 or kv > 99999: bad(tag, 'key_value not 0..99999 integer')
                if len(x['steps']) < 2 or not all(re.search(r'\d', s) for s in x['steps']): bad(tag, 'steps need 2+ with numbers')
                cw = x['common_wrong']; vals = [w['value'] for w in cw]
                if len(cw) != 3 or len(set(vals + [kv])) != 4: bad(tag, 'common_wrong not 3 distinct and different from key')
                if any(not isinstance(v, int) or v < 0 or v > 99999 for v in vals): bad(tag, 'wrong value range')
                if any(not w.get('why') for w in cw): bad(tag, 'wrong why')
                r = recompute(i, x['stem'])
                if r is None or r != kv: bad(tag, 'independent recomputation from the stem differs')
            if regen is not None:
                g = next((y for y in regen['items'] if y['id'] == i), None)
                if g != it: bad(i, 'generator output differs from the bank file')
        elif t == 'matching':
            if len(it['premises']) != 4 or len(it['responses']) != 5: bad(i, 'sizes')
            if len(set(it['premises'])) != 4 or len(set(it['responses'])) != 5: bad(i, 'not distinct')
            a = it['answer']
            if len(a) != 4 or len(set(a)) != 4 or not all(0 <= v < 5 for v in a): bad(i, 'answer')
            if len(it['why_wrong_rows']) != 4 or not all(it['why_wrong_rows']): bad(i, 'why_wrong_rows')
            if len(it['steps']) < 1: bad(i, 'steps')
        elif t == 'ordering':
            if len(it['steps']) != 5 or len(set(it['steps'])) != 5: bad(i, 'steps')
            a = it['answer']
            if sorted(a) != [1, 2, 3, 4, 5]: bad(i, 'answer not a permutation')
            if a == [1, 2, 3, 4, 5]: bad(i, 'displayed order is the right order')
            if len(it['why_wrong_rows']) != 5 or not all(it['why_wrong_rows']): bad(i, 'why_wrong_rows')
            if len(it.get('steps_solution', [])) != 5: bad(i, 'steps_solution')
            sol = it['steps_solution']
            # the displayed statements, put in the keyed order, must read as the right order
            rec = [None] * 5
            for j, p in enumerate(a): rec[p - 1] = it['steps'][j]
            if None in rec: bad(i, 'answer places')
        elif t == 'fill':
            if len(it['bank']) != 5 or len(set(it['bank'])) != 5: bad(i, 'bank')
            if len(it['blanks']) != 2: bad(i, 'blanks')
            ans = [b['answer'] for b in it['blanks']]
            if len(set(ans)) != 2 or not all(isinstance(v, int) and 0 <= v < 5 for v in ans): bad(i, 'blank answers')
            if sorted(it['why_wrong_entries'].keys()) != ['0', '1', '2', '3', '4']: bad(i, 'why_wrong_entries keys')
            if len(it['steps']) < 1: bad(i, 'steps')
        else: bad(i, 'unknown type')
    return F

def load_bank(path):
    with open(path, encoding='utf-8') as fh: return json.load(fh)

def regen():
    import mock_numeric_gen_ch2_v1_0_0 as G
    importlib.reload(G); return G.build()

def selftest(bank):
    ok = True
    def run(name, mut, want):
        nonlocal ok
        b = copy.deepcopy(bank); mut(b); F = check_bank(b, regen())
        hit = any(w in r for _, r in F for w in [want])
        print('PLANTED %-34s %s  (%d failure(s) reported, expected rule "%s")' % (name, 'FAILS as it must' if hit else 'NOT DETECTED', len(F), want)); ok = ok and hit
    def m1(b):
        c = [x for x in b['items'] if x['type'] == 'choice'][0]; k = next(iter(c['why_wrong'])); c['why_wrong'][k] += ' Option B is wrong.'
    def m2(b):
        c = [x for x in b['items'] if x['type'] == 'choice'][0]; c['stem'] = ' '.join(['word'] * 68) + '. You are asked to choose one.'
    def m3(b):
        n = [x for x in b['items'] if x['type'] == 'numeric'][0]; n['instances'][0]['key_value'] += 1
    run('a letter in a solution', m1, 'letter pattern')
    run('a stem of 70 words', m2, 'over 60 words')
    run('a numeric instance with a changed key', m3, 'recomputation')
    return ok

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['check', 'selftest']); ap.add_argument('--bank', default=os.path.join(HERE, 'mock_bank_ch%d_v1_0_0.json' % CH))
    a = ap.parse_args(); bank = load_bank(a.bank)
    if a.cmd == 'selftest':
        ok = selftest(bank); print('SELFTEST %s' % ('PASS' if ok else 'FAIL')); return 0 if ok else 1
    F = check_bank(bank, regen())
    cnt = collections.Counter(i['type'] for i in bank['items'])
    print('Mock bank check chapter %d  items %d  %s' % (CH, len(bank['items']), dict(cnt)))
    print('numeric instances %d' % sum(len(i['instances']) for i in bank['items'] if i['type'] == 'numeric'))
    for i, r in F: print('FAIL %s  %s' % (i, r))
    print('RESULT %s  (%d failure(s))' % ('PASS' if not F else 'FAIL', len(F)))
    return 0 if not F else 1

if __name__ == '__main__': sys.exit(main())
