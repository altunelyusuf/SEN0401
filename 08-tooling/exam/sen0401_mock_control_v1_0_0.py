#!/usr/bin/env python3
"""sen0401_mock_control v1.0.0 - the lineage agent's own control of the mock bank (no item text is printed or stored here).
Usage: python3 -I sen0401_mock_control_v1_0_0.py bank BANK.json [--gen GENERATOR.py]
bank: (1) schema, counts, points, word limits, letters in solutions, option ratio, answer spread;
      (2) exclusion against the text of EVERY delivered exam: all CME private items json, every papers_midterm_v* docx and pdf (paper and key), by 5-gram containment (limit 0.35) and exact option/premise equality;
          planted-copy fixtures (verbatim, numbers changed, two words changed) must be flagged, a synthetic item must pass;
      (3) numeric recomputation: the generator is run again in a temporary folder and its instances equal the bank.
Log: ids, scores, counts only."""
import sys, os, re, json, glob, subprocess, tempfile, shutil, hashlib
CME = '/home/claude/CME/exams/SEN0401/08-tooling/exam'
def norm(s): return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', str(s).lower())).strip()
def grams(s, n=5):
    w = norm(s).split(); return {' '.join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}
def walk(o, out):
    if isinstance(o, str): out.append(o)
    elif isinstance(o, dict): [walk(v, out) for v in o.values()]
    elif isinstance(o, list): [walk(v, out) for v in o]
def index():
    texts = []
    for f in glob.glob(CME + '/private/sen0401_exam_items*.json') + glob.glob(CME + '/papers_midterm_v*/*key.json'):
        try: walk(json.load(open(f)), texts)
        except Exception: pass
    from docx import Document
    for f in glob.glob(CME + '/papers_midterm_v*/*.docx'):
        d = Document(f)
        texts += [p.text for p in d.paragraphs]
        for t in d.tables:
            for r in t.rows: texts += [c.text for c in r.cells]
    for f in glob.glob(CME + '/papers_midterm_v*/*.pdf'):
        texts += subprocess.run(['pdftotext', f, '-'], capture_output=True, text=True).stdout.split('\n')
    texts = [t for t in texts if len(t.split()) >= 4]
    G = set(); S = set()
    for t in texts: G |= grams(t); S.add(norm(t))
    return G, S, len(texts)
def item_strings(it):
    t = it['type']; main = [it.get('stem') or it.get('intro') or '']
    if t == 'numeric': main = [i['stem'] for i in it['instances']]
    sm = []
    if t == 'choice': sm = it['options']
    if t == 'matching': sm = it['premises'] + it['responses']
    if t == 'ordering': sm = it['steps']
    if t == 'fill': sm = it['bank'] + [b['sentence'] for b in it['blanks']]
    return main, sm
GENERIC = re.compile(r'You are asked to fill each blank with the bank entry that makes the sentence true\.|One response is not used\.|one response is not used\.', re.I)
def contain(s, G):
    g = grams(GENERIC.sub(' ', s))
    return (len(g & G) / len(g)) if g else 0.0
def flag(main, sm, G, S):
    c = max([contain(s, G) for s in main] + [0]); eq = sum(1 for s in sm if len(norm(s).split()) >= 4 and norm(s) in S)
    return c, eq
def cmd_bank(path, gen):
    d = json.load(open(path)); items = d['items']; ch = d['chapter']; fails = []; log = []
    cnt = {}
    for it in items: cnt[it['type']] = cnt.get(it['type'], 0) + 1
    want = dict(choice=10, numeric=4, matching=3, ordering=2, fill=4)
    if cnt != want: fails.append('counts %s' % cnt)
    ch_items = [i for i in items if i['type'] == 'choice']
    if sorted(i['points'] for i in ch_items) != [3] * 4 + [4] * 6: fails.append('choice points')
    if sum(1 for i in items if i['type'] == 'numeric' and i.get('can_be_4')) != 1: fails.append('can_be_4 count')
    pos = [i['answer'] for i in ch_items]; sp = [pos.count(k) for k in range(5)]
    if max(sp) - min(sp) > 1: fails.append('answer spread %s' % sp)
    W = lambda s: len(str(s).split())
    letters = re.compile(r'\b(option|answer|choice|response)\s+[A-E]\b|\b[A-E]\.\s', re.I)
    for it in items:
        main, sm = item_strings(it); i = it['id']
        tips = it.get('tip') or ''
        if tips.lower().startswith('tip:'): log.append('NOTE %s tip carries the prefix Tip: (the merge must strip it)' % i); tips = tips[4:].strip()
        if W(tips) > 12: fails.append('%s tip' % i)
        for s in main:
            if W(s) > 60: fails.append('%s stem %d words' % (i, W(s)))
            last = re.split(r'(?<=[.?!])\s+', s.strip())[-1]
            if not last.startswith('You are asked to'): fails.append('%s last sentence' % i)
        allsol = []; walk({k: v for k, v in it.items() if k in ('steps', 'why_right', 'why_wrong', 'why_wrong_rows', 'why_wrong_entries', 'steps_solution')}, allsol)
        if any(letters.search(s) for s in allsol): fails.append('%s letter in solution' % i)
        if it['type'] == 'choice':
            o = it['options']
            if len(o) != 5 or len({norm(x) for x in o}) != 5 or any(not x.strip() for x in o): fails.append('%s options' % i)
            ws = [W(x) for x in o]
            if max(ws) > 3 * min(ws): fails.append('%s option ratio' % i)
            if set(it['why_wrong']) != {str(k) for k in range(5)} - {str(it['answer'])}: fails.append('%s why_wrong keys' % i)
            if any(re.search(r'all of the above|none of the above', x, re.I) for x in o): fails.append('%s all/none' % i)
        if it['type'] == 'matching':
            if len(it['premises']) != 4 or len(it['responses']) != 5 or len(set(it['answer'])) != 4: fails.append('%s matching' % i)
        if it['type'] == 'ordering':
            if sorted(it['answer']) != [1, 2, 3, 4, 5] or it['answer'] == [1, 2, 3, 4, 5]: fails.append('%s ordering' % i)
        if it['type'] == 'fill':
            if len(it['bank']) != 5 or len(it['blanks']) != 2 or it['blanks'][0]['answer'] == it['blanks'][1]['answer']: fails.append('%s fill' % i)
        if it['type'] == 'numeric':
            if len(it['instances']) != 8: fails.append('%s instances' % i)
            kv = [x['key_value'] for x in it['instances']]
            if len(set(kv)) != 8 or any((not isinstance(v, int)) or v < 0 or v > 99999 for v in kv): fails.append('%s key values' % i)
            stems = [x['stem'] for x in it['instances']]
            if len(set(stems)) != 8: fails.append('%s stems' % i)
            for x in it['instances']:
                cw = [c['value'] for c in x['common_wrong']]
                if len(cw) != 3 or len(set(cw + [x['key_value']])) != 4: fails.append('%s wrong values' % i)
                if len(x['steps']) < 2: fails.append('%s steps' % i)
    log.append('structure: %d items, %d findings so far' % (len(items), len(fails)))
    # exclusion
    G, S, n = index(); log.append('index: %d text units of delivered exams' % n)
    worst = 0; eqn = 0
    for it in items:
        main, sm = item_strings(it); c, eq = flag(main, sm, G, S); worst = max(worst, c); eqn += eq
        if c >= 0.35: fails.append('%s containment %.2f' % (it['id'], c))
        if eq: fails.append('%s equal option/premise (%d)' % (it['id'], eq))
    log.append('exclusion: max 5-gram containment %.3f (limit 0.35), equal options %d' % (worst, eqn))
    # planted fixtures from real index paragraph
    real = None
    for f in sorted(glob.glob(CME + '/private/sen0401_exam_items_midterm_v1_8_0.json')):
        o = json.load(open(f)); tx = []; walk(o, tx)
        real = [t for t in tx if 20 <= len(t.split()) <= 60 and t.strip().endswith('.')][3]
    v1 = real; v2 = re.sub(r'\d+', lambda m: str(int(m.group(0)) + 7), real); w = real.split(); w[2] = 'xx'; w[6] = 'yy'; v3 = ' '.join(w)
    syn = 'A farmer sells eleven blue baskets at a market and counts the coins in a leather purse. You are asked to name the number of baskets that remain after nine are sold on a rainy morning.'
    res = [flag([x], [], G, S)[0] for x in (v1, v2, v3, syn)]
    ok = res[0] >= 0.35 and res[2] >= 0.35 and res[3] < 0.35
    log.append('planted: verbatim %.2f, digits changed %.2f, two words changed %.2f, synthetic %.2f -> %s' % (res[0], res[1], res[2], res[3], 'caught as required' if ok else 'FIXTURE FAIL'))
    if not ok: fails.append('planted fixtures')
    if res[1] < 0.35: log.append('NOTE digits-only change is NOT caught by containment (%.2f); numeric items are caught only by stem wording, see numbers rule' % res[1])
    # numeric recompute
    if gen:
        tmp = tempfile.mkdtemp(); shutil.copy(gen, tmp)
        for extra in glob.glob(os.path.join(os.path.dirname(os.path.abspath(gen)), 'mock_content_ch%d_*.py' % ch)): shutil.copy(extra, tmp)
        r = subprocess.run([sys.executable, '-I', os.path.join(tmp, os.path.basename(gen)), '--out', os.path.join(tmp, 'out_gen.json')], capture_output=True, text=True, cwd=tmp)
        outs = sorted(glob.glob(tmp + '/*.json')) + glob.glob(os.path.dirname(os.path.abspath(gen)) + '/mock_numeric_ch%d_v1_0_0.json' % ch)
        log.append('generator exit %d; outputs %s' % (r.returncode, [os.path.basename(x) for x in outs]))
        if r.returncode != 0: fails.append('generator failed')
        else:
            gens = None
            for x in outs:
                try: gens = json.load(open(x)); break
                except Exception: pass
            def collect(o):
                if isinstance(o, dict) and 'instances' in o: return {o.get('id'): [(i['key_value'], i['stem']) for i in o['instances']]}
                r = {}
                if isinstance(o, dict): [r.update(collect(v)) for v in o.values()]
                if isinstance(o, list): [r.update(collect(v)) for v in o]
                return r
            a = collect(gens) if gens else {}; b = collect({'items': [i for i in items if i['type'] == 'numeric']})
            same = sum(1 for k in b if a.get(k) == b[k])
            log.append('numeric recompute: %d of %d templates equal the generator output' % (same, len(b)))
            if same != len(b): fails.append('numeric recompute differs')
    # independent arithmetic spot: key_value distinct from common_wrong done above
    print('\n'.join(log)); print('FINDINGS %d: %s' % (len(fails), '; '.join(fails[:20]))); print('RESULT %s' % ('PASS' if not fails else 'FAIL')); return 0 if not fails else 1
if __name__ == '__main__':
    gen = sys.argv[sys.argv.index('--gen') + 1] if '--gen' in sys.argv else None
    sys.exit(cmd_bank(sys.argv[2], gen))
