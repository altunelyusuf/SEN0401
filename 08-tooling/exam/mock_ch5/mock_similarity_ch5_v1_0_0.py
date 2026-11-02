#!/usr/bin/env python3
"""Chapter 5 self-check against the delivered exam items (reads the private item files to AVOID copying; prints item ids and scores only, never text).
Rule of the plan: token 5-gram Jaccard of a stem to every indexed stem below 0.35 and word-level (unigram) Jaccard below 0.6; no option or premise equal to an indexed one.
This is the chapter executor's own pre-check; the formal exclusion gate is the other executor's tool."""
import glob, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PRIV = '/home/claude/CME/exams/SEN0401/08-tooling/exam'
def tok(t): return re.findall(r'[a-z0-9]+', t.lower())
def grams(t, n=5):
    w = tok(t); return {tuple(w[i:i + n]) for i in range(max(0, len(w) - n + 1))} or {tuple(w)}
def jac(a, b): return len(a & b) / len(a | b) if a | b else 0.0
def strings(x, out):
    if isinstance(x, str): out.append(x)
    elif isinstance(x, list): [strings(y, out) for y in x]
    elif isinstance(x, dict): [strings(y, out) for y in x.values()]
files = sorted(glob.glob(PRIV + '/sen0401_exam_items_*.json') + glob.glob(PRIV + '/private/sen0401_exam_items_*.json'))
idx = []
for f in files:
    try: strings(json.load(open(f, encoding='utf-8')), idx)
    except Exception as e: print('skip', os.path.basename(f), e)
idx = [s for s in set(idx) if len(tok(s)) >= 3]
idx_g = [(grams(s), set(tok(s)), re.sub(r'\W+', ' ', s.lower()).strip()) for s in idx]
print('indexed files %d, indexed strings %d' % (len(files), len(idx)))
bank = json.load(open(os.path.join(HERE, 'mock_bank_ch5_v1_0_0.json'), encoding='utf-8'))
def mine(it):
    t = it['type']
    if t == 'choice': return [('stem', it['stem'])], it['options']
    if t == 'numeric': return [('stem#%d' % k, x['stem']) for k, x in enumerate(it['instances'], 1)], []
    if t == 'matching': return [('intro', it['intro'])], it['premises'] + it['responses']
    if t == 'ordering': return [('intro', it['intro'])], it['steps']
    if t == 'fill': return [('stem', it['stem'])] + [('blank', b['sentence']) for b in it['blanks']], it['bank']
worst = 0; bad = 0
exact = {e for _, _, e in idx_g}
for it in bank['items']:
    texts, opts = mine(it); best = (0, 0)
    for lab, s in texts:
        g, w = grams(s), set(tok(s))
        for G, W, _ in idx_g:
            a, b = jac(g, G), jac(w, W)
            if (a, b) > best: best = (a, b)
    eq = [o for o in opts if re.sub(r'\W+', ' ', o.lower()).strip() in exact and len(tok(o)) >= 3]
    ok = best[0] < 0.35 and best[1] < 0.6 and not eq
    bad += (not ok); worst = max(worst, best[0])
    print('%-6s max 5-gram %.2f  max word %.2f  equal options %d  %s' % (it['id'], best[0], best[1], len(eq), 'PASS' if ok else 'FAIL'))
print('RESULT %s  (items failing: %d, highest 5-gram score %.2f)' % ('PASS' if not bad else 'FAIL', bad, worst))
