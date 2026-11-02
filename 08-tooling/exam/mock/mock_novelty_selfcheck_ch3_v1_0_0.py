#!/usr/bin/env python3
"""SEN0401 mock chapter bank: novelty self-check against every delivered exam text, version 1.0.0. Holds no question text.
This is the executor's own pre-check (the official exclusion gate is built by another executor). It indexes, in memory only, the text of every
items file (sen0401_exam_items*.json, any folder under the exam tooling folder) and every paper/key .docx under papers_* folders, and compares the
stems, options, premises, blanks and key values of the mock bank with it. The report prints item ids, the number of the nearest indexed text and scores; never text.
Rules (plan): stem 5-gram Jaccard < 0.35 and word-level Jaccard < 0.6 to every indexed text; no option/premise equal to an indexed one (normalised);
numeric key value with the same unit not equal to an indexed key for a stem with similarity above 0.3.
Usage: nice python3 SCRIPT --bank BANK.json --exam-root DIR [--selftest]"""
import argparse, glob, json, os, re, sys
sys.dont_write_bytecode = True


def norm(t): return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9]+', ' ', str(t).lower())).strip()


def grams(tokens, n=5): return {tuple(tokens[i:i + n]) for i in range(max(0, len(tokens) - n + 1))}


def jac(a, b):
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)


def sim(a, b):
    ta, tb = a.split(), b.split()
    return jac(grams(ta), grams(tb)), jac(set(ta), set(tb))


def texts_of_item(it):
    stems = [t for t in (it.get('q'), it.get('instruction'), it.get('stem'), it.get('intro')) if isinstance(t, str)]
    for b in it.get('blanks') or []:
        if isinstance(b, dict):
            for k in ('text', 'sentence'):
                if isinstance(b.get(k), str): stems.append(b[k])
    opts = []
    for k in ('options', 'responses', 'bank', 'steps', 'distractors'):
        v = it.get(k)
        if isinstance(v, list): opts += [x for x in v if isinstance(x, str)]
    for p in it.get('premises') or []:
        if isinstance(p, dict) and isinstance(p.get('text'), str): opts.append(p['text'])
        elif isinstance(p, str): opts.append(p)
    for b in it.get('blanks') or []:
        if isinstance(b, dict) and isinstance(b.get('answer'), str): opts.append(b['answer'])
    return stems, [o for o in opts if isinstance(o, str)]


def build_index(root):
    stems, opts, keys = [], set(), []
    nfiles = 0
    for f in glob.glob(os.path.join(root, '**', 'sen0401_exam_items*.json'), recursive=True):
        try: d = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        its = d.get('items') if isinstance(d, dict) else d
        if not isinstance(its, list): continue
        nfiles += 1
        for it in its:
            if not isinstance(it, dict): continue
            s, o = texts_of_item(it)
            ns = [norm(x) for x in s if norm(x)]
            stems += ns
            opts |= {norm(x) for x in o if norm(x)}
            if 'key_value' in it and isinstance(it['key_value'], (int, float)):
                keys.append((it['key_value'], norm(it.get('unit', '')), ns[0] if ns else ''))
    ndocx = 0
    try:
        import docx
        for f in glob.glob(os.path.join(root, '**', 'papers_*', '*.docx'), recursive=True):
            try: d = docx.Document(f)
            except Exception: continue
            ndocx += 1
            paras = [p.text for p in d.paragraphs] + [c.text for t in d.tables for r in t.rows for c in r.cells]
            for p in paras:
                if norm(p): stems.append(norm(p))
    except ImportError: pass
    stems = list(dict.fromkeys(stems))
    return stems, opts, keys, nfiles, ndocx


def mock_units(bank):
    """Yield (id, stem list, option list, key info) for every item and every numeric instance."""
    for it in bank['items']:
        t = it['type']
        if t == 'choice': yield it['id'], [it['stem']], it['options'], None
        elif t == 'numeric':
            for k, ins in enumerate(it['instances'], 1): yield '%s#%d' % (it['id'], k), [ins['stem']], [], (ins['key_value'], norm(it['unit']))
        elif t == 'matching': yield it['id'], [it['intro']], it['premises'] + it['responses'], None
        elif t == 'ordering': yield it['id'], [it['intro']], it['steps'], None
        elif t == 'fill': yield it['id'], [it['stem']] + [b['sentence'].replace('____', ' ') for b in it['blanks']], it['bank'], None


def evaluate(units, stems, opts, keys, idxsets):
    rows, fails = [], []
    for uid, st, op, key in units:
        best = (0.0, 0.0, -1); best_any = (0.0, 0.0, -1)
        for s in st:
            ns = norm(s)
            g = grams(ns.split()); w = set(ns.split())
            for i, (ig, iw) in enumerate(idxsets):
                j5 = jac(g, ig); jw = jac(w, iw)
                if j5 > best[0] or (j5 == best[0] and jw > best[1]): best = (j5, jw, i)
                if jw > best_any[1]: best_any = (j5, jw, i)
        eq = [o for o in op if norm(o) in opts]
        keyhit = None
        if key is not None:
            for kv, ku, kstem in keys:
                if kv == key[0] and ku == key[1]:
                    ns = norm(st[0]); a, b = sim(ns, kstem)
                    if max(a, b) > 0.3: keyhit = (a, b)
        bad = best[0] >= 0.35 or best_any[1] >= 0.6 or bool(eq) or keyhit is not None
        rows.append((uid, best[0], best_any[1], best[2], len(eq), keyhit))
        if bad: fails.append(uid)
    return rows, fails


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--bank', required=True); ap.add_argument('--exam-root', required=True); ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    bank = json.load(open(a.bank, encoding='utf-8'))
    stems, opts, keys, nf, nd = build_index(a.exam_root)
    idxsets = [(grams(s.split()), set(s.split())) for s in stems]
    print('Index (in memory only): %d distinct normalised texts from %d items files and %d paper/key documents; %d option texts; %d numeric keys' % (len(stems), nf, nd, len(opts), len(keys)))
    units = list(mock_units(bank))
    rows, fails = evaluate(units, stems, opts, keys, idxsets)
    print('Per unit: id, max 5-gram Jaccard (limit < 0.35), max word Jaccard (limit < 0.6), nearest indexed text number, equal options, numeric key hit')
    for r in rows: print('  %-8s 5gram %.3f  word %.3f  nearest #%-5d equal_options %d  key_hit %s' % (r[0], r[1], r[2], r[3], r[4], 'yes' if r[5] else 'no'))
    mx5 = max(r[1] for r in rows); mxw = max(r[2] for r in rows)
    print('Max over the chapter: 5-gram %.3f, word %.3f; units failing: %d of %d %s' % (mx5, mxw, len(fails), len(rows), fails))
    ok = not fails
    if a.selftest:
        # planted copies built in memory from the INDEX (a real delivered stem) - never written out
        base = next(s for s in stems if 25 <= len(s.split()) <= 55)
        toks = base.split()
        twonum = re.sub(r'\d+', lambda m: str(int(m.group(0)) + 3), base)
        two = toks[:]; two[3] = 'quickly'; two[11] = 'often'
        planted = [('verbatim copy', base), ('copy with numbers changed only', twonum), ('copy with two words changed', ' '.join(two)),
                   ('genuinely new text', 'zebra quartz harbour violin meadow lantern sparrow ' * 4)]
        pu = [(n, [t], [], None) for n, t in planted]
        prow, pfail = evaluate(pu, stems, opts, keys, idxsets)
        exp = {'verbatim copy': True, 'copy with numbers changed only': True, 'copy with two words changed': True, 'genuinely new text': False}
        print('Planted fixtures (built in memory from one indexed text, not stored):')
        for (n, _), r in zip(planted, prow):
            failed = n in pfail
            print('  %-34s 5gram %.3f word %.3f -> %s (expected %s)' % (n, r[1], r[2], 'FAIL' if failed else 'PASS', 'FAIL' if exp[n] else 'PASS'))
            ok = ok and (failed == exp[n])
    print('RESULT %s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
