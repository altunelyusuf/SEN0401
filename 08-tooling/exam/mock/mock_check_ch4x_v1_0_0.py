#!/usr/bin/env python3
"""mock_check_ch4x v1.0.0 - checks of the hash-search family file; independent recomputation of every key from the numbers in the stem.
Usage: python3 -I mock_check_ch4x_v1_0_0.py BANK.json [--gen GENERATOR.py] [--selftest]
Prints ids and counts only."""
import sys, re, json, copy, subprocess, tempfile, os, shutil, hashlib
WHY = ("Why this question: mining is a search that nobody can shorten except by accepting more results, "
       "and anyone can check an answer with one hash. Counting the tries shows why a bigger target makes "
       "mining faster and a smaller one slower.")
def num(m): return int(m.replace(',', ''))
def parse(tid, st):
    g = lambda pat: num(re.search(pat, st).group(1))
    N = r'([\d,]+)'
    if tid == 'n4x_1': return 2 ** g(r'(\d+) bits')
    if tid == 'n4x_2':
        v = g(N + r' (?:possible|different) results'); return v.bit_length() - 1
    if tid == 'n4x_3': return g(N + r' tries in total') // g(r'(\d+) tries per second')
    if tid == 'n4x_4': return 2 ** g(r'(\d+) bits') // g(r'set of (\d+) results')
    if tid == 'n4x_5': return 2 ** g(r'(\d+) bits') // g(r'(\d+) tries per second')
    if tid == 'n4x_6': return 2 ** g(r'(\d+) bits') // g(r'set of (\d+) results') // g(r'(\d+) tries per second')
    if tid == 'n4x_7': return 2 ** g(r'(\d+) bits') // g(r'(?:in|take) (\d+) seconds')
    return None
ABBR = re.compile(r'\b(e\.g\.|i\.e\.|etc|approx|sec\.|secs|hrs?|min\.|vs\.|w/)\b', re.I)
BANNED = re.compile(r'\btarget\b|\bA toy hash has\b|\bA second search accepts\b|^Tip:', re.I)
def W(s): return len(str(s).split())
def check(d, label=''):
    F = []
    its = d.get('items', [])
    if d.get('chapter') != 4 or d.get('family') != 'hash_search': F.append('header')
    if len(its) < 6: F.append('templates < 6')
    if sum(len(i['instances']) for i in its) < 48: F.append('instances < 48')
    if sum(1 for i in its if i.get('can_be_4')) != 1: F.append('can_be_4 count')
    for k, it in enumerate(its):
        i = it['id']
        if i != 'n4x_%d' % (k + 1) or it.get('type') != 'numeric' or it.get('chapter') != 4 or it.get('points') != 3: F.append('%s header' % i)
        if it.get('why_question') != WHY: F.append('%s why_question' % i)
        if not it.get('unit'): F.append('%s unit' % i)
        tip = it.get('tip', '')
        if W(tip) > 12 or W(tip) == 0 or BANNED.search(tip) or ABBR.search(tip): F.append('%s tip' % i)
        ins = it['instances']
        if len(ins) < 8: F.append('%s instances < 8' % i)
        if len({x['key_value'] for x in ins}) != len(ins): F.append('%s duplicate keys' % i)
        if len({x['stem'] for x in ins}) != len(ins): F.append('%s duplicate stems' % i)
        for j, x in enumerate(ins):
            tag = '%s#%d' % (i, j + 1)
            kv = x['key_value']
            if type(kv) is not int or kv < 1 or kv > 99999: F.append('%s key range' % tag)
            try:
                if parse(i, x['stem']) != kv: F.append('%s key differs from recomputation' % tag)
            except Exception: F.append('%s unparsable stem' % tag)
            st = x['stem']
            if W(st) > 60: F.append('%s stem %d words' % (tag, W(st)))
            if not re.split(r'(?<=[.?!])\s+', st.strip())[-1].startswith('You are asked to'): F.append('%s last sentence' % tag)
            if BANNED.search(st) or ABBR.search(st): F.append('%s banned wording or abbreviation' % tag)
            cw = x['common_wrong']
            vals = [c['value'] for c in cw]
            if len(cw) != 3 or len(set(vals + [kv])) != 4 or any(type(v) is not int or v < 1 or v > 99999 for v in vals): F.append('%s wrong values' % tag)
            if any(not c.get('why', '').strip() or W(c['why']) > 30 for c in cw): F.append('%s wrong why' % tag)
            if len(x['steps']) < 2 or not x.get('why_right'): F.append('%s steps' % tag)
            if re.search(r'\b(option|answer|choice)\s+[A-E]\b', ' '.join(x['steps'])): F.append('%s letter' % tag)
    return F
def plant(d, which):
    d = copy.deepcopy(d); x = d['items'][5]['instances'][0]
    if which == 0: x['key_value'] += 1                                   # key not equal to the recomputation
    if which == 1: x['stem'] = x['stem'].replace('You are asked to', 'Please') # last sentence rule
    if which == 2: x['common_wrong'][0]['value'] = x['key_value']        # a wrong value equals the key
    return d
def main():
    path = sys.argv[1]; d = json.load(open(path)); out = []
    F = check(d)
    n_t = len(d['items']); n_i = sum(len(i['instances']) for i in d['items'])
    out.append('file sha256 %s' % hashlib.sha256(open(path, 'rb').read()).hexdigest())
    out.append('templates %d, instances %d, can_be_4 on %d' % (n_t, n_i, sum(1 for i in d['items'] if i.get('can_be_4'))))
    out.append('words per stem: min %d max %d' % (min(W(x['stem']) for i in d['items'] for x in i['instances']), max(W(x['stem']) for i in d['items'] for x in i['instances'])))
    out.append('recomputed keys from the numbers in the stems: %d of %d equal' % (n_i - sum(1 for f in F if 'differs' in f), n_i))
    out.append('CHECK findings %d: %s' % (len(F), '; '.join(F[:20])))
    if '--gen' in sys.argv:
        gen = sys.argv[sys.argv.index('--gen') + 1]; tmp = tempfile.mkdtemp(); shutil.copy(gen, tmp)
        r = subprocess.run([sys.executable, '-I', os.path.join(tmp, os.path.basename(gen)), '--out', os.path.join(tmp, 'again.json')], capture_output=True, text=True, cwd=tmp)
        same = r.returncode == 0 and open(os.path.join(tmp, 'again.json'), 'rb').read() == open(path, 'rb').read()
        out.append('generator run again: exit %d, output byte-identical to the file: %s' % (r.returncode, same))
        if not same: F.append('regeneration differs')
    ok = not F
    if '--selftest' in sys.argv:
        for w, name in enumerate(['key off by one', 'last sentence not starting You are asked to', 'wrong value equal to the key']):
            fw = check(plant(d, w)); out.append('PLANTED %d (%s): %s (%d findings)' % (w + 1, name, 'FAILED as required' if fw else 'NOT CAUGHT', len(fw)))
            if not fw: ok = False
    out.append('RESULT %s' % ('PASS' if ok else 'FAIL'))
    print('\n'.join(out)); return 0 if ok else 1
if __name__ == '__main__': sys.exit(main())
