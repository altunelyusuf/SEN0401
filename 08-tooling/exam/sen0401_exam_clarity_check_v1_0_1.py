#!/usr/bin/env python3
"""SEN0401 exam clarity check, version 1.0.0 (new file; no existing gate is changed). Holds no question and no answer.

Rules of sen0401_exam_clarity_rule_v1_0_0.json:
  C1 undefined references: no phrase that needs outside context (the story, the history, above, as before, the previous question, the following example,
     in the text, a block height, a date, a person or company name) unless the same stem, or the Tip line directly under it, explains it at once
  C2 intention sentence: the LAST sentence of every stem starts with 'You are asked to'
  C3 key entry: every item has a solution with ordered steps (calculation: at least 2 steps, each with a number; others: at least 1), a why_right sentence
     and a why_wrong clause for every other option (choice) or every row, step or blank (matching, ordering, fill-in)
  C4 options: distinct, none empty, none 'all/none of the above', longest at most 3 times the shortest (choice), the answer points at one option;
     plausibility and trick wording are a human judgement and print NOT_MEASURED
  C5 each stem at most 60 words, each tip at most 12 words (as R1 and R3 of the readability check, which stays)
Items file: the items-file format of the paper builder plus a 'solution' field per item. Paper mode (optional, --paper): the stems of the paper .docx are read with the
reader of sen0401_exam_readability_check_v1_1_0.py; C1, C2 (items with a q field), C5 are measured on the paper; C3 and C4 are NOT_MEASURED on a paper.
Output: per rule and source, PASS / FAIL / NOT_MEASURED, failing items by KEY and LABEL only (never the text).

Usage:
  check    --items ITEMS.json [--paper PAPER.docx] [--rule RULE.json] [--json OUT.json]
  fixtures --spec FIXTURES.json --workdir DIR [--rule RULE.json]
Exit codes: 0 all clear, 1 a FAIL (check) or a wrong answer (fixtures), 2 usage or input error."""
import argparse, importlib.util, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULE = os.path.join(HERE, 'sen0401_exam_clarity_rule_v1_0_0.json')
READ_PATH = os.path.join(HERE, 'sen0401_exam_readability_check_v1_1_0.py')
READ_RULE = os.path.join(HERE, 'sen0401_exam_readability_rule_v1_1_0.json')
RULES = ['C1', 'C2', 'C3', 'C4', 'C5']
TITLES = {'C1': 'no undefined reference (story, above, as before, block height, date, name) without a one-clause explanation in the stem or the tip',
          'C2': "last sentence of every stem starts with 'You are asked to'",
          'C3': 'key entry: ordered steps (calculation: 2+ with numbers), why_right, why_wrong for every other option or row',
          'C4': 'options distinct, none empty, no all/none of the above, longest at most 3 times the shortest, one right answer',
          'C5': 'stem at most 60 words, tip at most 12 words'}


def load(path):
    with open(path, encoding='utf-8') as f: return json.load(f)


def norm(t): return re.sub(r'\s+', ' ', t or '').strip()


def nwords(t): return len([w for w in t.split() if re.search(r'[A-Za-z0-9]', w)])


def sentences(t, rule):
    t = norm(t)
    return [s for s in re.split(rule['sentence_split'], t) if s.strip()] if t else []


class Unit:
    def __init__(self, key, label, typ):
        self.key, self.label, self.type = key, label, typ
        self.stems = []; self.c1_texts = []; self.tips = []; self.options = None; self.answer = None
        self.bank = None; self.solution = None; self.rows = 0; self.has_q = False
    def tag(self): return '%s [%s]' % (self.key, self.label) if self.label else self.key


def labels_of(sub): return ','.join(re.findall(r'Q(\d+\.[a-z])', sub or ''))


def read_items(path, rule):
    d = load(path); items = d['items'] if isinstance(d, dict) else d; out = []
    pm = re.compile(rule['points_marker'])
    for it in items:
        u = Unit(it.get('key', '?'), labels_of(it.get('sub_question', '')), it.get('type', ''))
        if it.get('q'): u.stems = [pm.sub('', norm(it['q']))]; u.has_q = True
        elif it.get('instruction'): u.stems = [pm.sub('', norm(it['instruction']))]
        u.c1_texts = list(u.stems)
        for b in it.get('blanks') or []:
            if isinstance(b, dict) and b.get('text'): u.c1_texts.append(norm(b['text']))
        for p in it.get('premises') or []:
            if isinstance(p, dict) and p.get('text'): u.c1_texts.append(norm(p['text']))
        tl = it.get('tip'); tl = [] if not tl else ([tl] if isinstance(tl, str) else list(tl))
        u.tips = [re.sub(rule['tip_prefix'], '', norm(t)) for t in tl]
        if it.get('options') is not None: u.options = list(it['options']); u.answer = it.get('answer')
        if it.get('responses') is not None: u.bank = list(it['responses'])
        if it.get('type') == 'FillBlankGroup':
            u.bank = [b.get('answer', '') for b in (it.get('blanks') or []) if isinstance(b, dict)] + list(it.get('distractors') or [])
        u.rows = len(it.get('premises') or it.get('blanks') or it.get('steps') or [])
        u.solution = it.get('solution')
        out.append(u)
    return out


# ------------------------------------------------------------------------------------------------ rules
def explained(text, end, rule):
    rest = text[end:end + 160]
    return any(re.match(p, rest) for p in rule['rules']['C1']['explanation_patterns'])


def tip_explains(tips, phrase, rule):
    for t in tips:
        for m in re.finditer(re.escape(phrase), t, re.I):
            rest = t[m.end():m.end() + 160]
            if any(re.match(x, rest) for x in rule['rules']['C1']['tip_explanation_patterns']): return True
    return False


def check_c1_texts(texts, rule, tips=()):
    c1 = rule['rules']['C1']; bad = []
    for t in texts:
        for pat, flags in [(p, re.I) for p in c1['phrase_patterns']] + [(p, 0) for p in c1['name_patterns']]:
            for m in re.finditer(pat, t, flags):
                if not explained(t, m.end(), rule) and not tip_explains(tips, m.group(0), rule): bad.append(m.group(0).lower() if flags else m.group(0))
    return sorted(set(bad))


def c1(u, rule):
    b = check_c1_texts(u.c1_texts, rule, u.tips)
    return bool(b), ('unexplained: ' + ', '.join(b)) if b else ''


def c2(u, rule):
    req = rule['rules']['C2']['required_start']; bad = []
    for s in getattr(u, 'c2_stems', u.stems):
        ss = sentences(s, rule)
        if not ss or not ss[-1].startswith(req): bad.append('last sentence does not start with the required words')
    if not getattr(u, 'c2_stems', u.stems): bad.append('no stem')
    return bool(bad), '; '.join(sorted(set(bad)))


def c3(u, rule):
    c = rule['rules']['C3']; sol = u.solution; why = []
    if not isinstance(sol, dict): return True, 'no solution'
    steps = sol.get('steps'); steps = steps if isinstance(steps, list) else []
    calc = u.type in c['calculation_types']
    need = c['min_steps_calculation'] if calc else c['min_steps_other']
    if len(steps) < need: why.append('steps %d, need %d' % (len(steps), need))
    if calc:
        for i, s in enumerate(steps, 1):
            if not (isinstance(s, dict) and re.search(r'\d', str(s.get('number', '')))): why.append('step %d has no number' % i)
    for i, s in enumerate(steps, 1):
        txt = s.get('text') if isinstance(s, dict) else s
        if not norm(txt if isinstance(txt, str) else ''): why.append('step %d is empty' % i)
    if not norm(sol.get('why_right') if isinstance(sol.get('why_right'), str) else ''): why.append('why_right missing')
    if not calc:
        ww = sol.get('why_wrong') if isinstance(sol.get('why_wrong'), dict) else {}
        if u.type.startswith(c['choice_type_prefix']) and u.options is not None:
            want = [chr(65 + i) for i in range(len(u.options)) if i != u.answer]
        else: want = [str(i) for i in range(1, u.rows + 1)]
        for k in want:
            if not norm(ww.get(k) if isinstance(ww.get(k), str) else ''): why.append('why_wrong %s missing' % k)
    return bool(why), '; '.join(sorted(set(why)))


def c4(u, rule):
    c = rule['rules']['C4']; why = []; lists = []
    if u.options is not None: lists.append((u.options, u.type.startswith(rule['rules']['C3']['choice_type_prefix'])))
    if u.bank is not None: lists.append((u.bank, False))
    for lst, choice in lists:
        txt = [norm(x) if isinstance(x, str) else '' for x in lst]
        if any(not t for t in txt): why.append('empty option')
        low = [t.lower() for t in txt if t]
        if len(set(low)) != len(low): why.append('duplicate options')
        for t in low:
            if any(f in t for f in c['forbidden_options']): why.append("'all/none of the above'"); break
        if choice:
            ws = [nwords(t) for t in txt if t]
            if ws and min(ws) > 0 and max(ws) > c['max_length_ratio'] * min(ws): why.append('longest %d words, shortest %d' % (max(ws), min(ws)))
            if not isinstance(u.answer, int) or isinstance(u.answer, bool) or not (0 <= u.answer < len(lst)): why.append('answer does not point at one option')
    return bool(why), '; '.join(sorted(set(why)))


def c5(u, rule):
    c = rule['rules']['C5']; why = []
    for s in u.c1_texts:
        n = nwords(s)
        if n > c['max_stem_words']: why.append('stem %d words' % n)
    for t in u.tips:
        n = nwords(t)
        if n > c['max_tip_words']: why.append('tip %d words' % n)
    return bool(why), '; '.join(sorted(set(why)))


FUN = {'C1': c1, 'C2': c2, 'C3': c3, 'C4': c4, 'C5': c5}


def run_items(units, rule):
    return {r: dict(status='MEASURED', checked=len(units), fail=[(u.tag(), d) for u in units for bad, d in [FUN[r](u, rule)] if bad]) for r in RULES}


# ------------------------------------------------------------------------------------------------ paper
def load_reader():
    spec = importlib.util.spec_from_file_location('sen0401_readability_v110', READ_PATH)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def paper_units(paper, items, item_units):
    rd = load_reader(); rrule = rd.load_rule(READ_RULE)
    iu, _ = rd.read_items(items, rrule)
    pu, _, _, _, _ = rd.read_paper(paper, rrule, iu)
    typ = {u.key: u for u in item_units}; out = []
    for p in pu:
        src = typ.get(p.key)
        u = Unit(p.key, ','.join(p.labels), src.type if src else '')
        u.stems = [norm(s) for s in p.stems if norm(s)]; u.c1_texts = list(u.stems)
        # v1.0.1: a paper unit of a fill-in group carries the group stem and one sentence per blank (marked ____); the blank sentences are not stems, C2 reads the stems that hold no blank (a group with no stem of its own still fails: 'no stem')
        u.c2_stems = [t for t in u.stems if '____' not in t]
        u.tips = [norm(t) for t in p.tip_lines if t]
        u.has_q = bool(src and src.has_q)
        out.append(u)
    return out


def run_paper(units, rule):
    res = {}
    for r in ('C1', 'C5'):
        res[r] = dict(status='MEASURED', checked=len(units), fail=[(u.tag(), d) for u in units for bad, d in [FUN[r](u, rule)] if bad])
    q = [u for u in units if u.has_q]
    res['C2'] = dict(status='MEASURED', checked=len(q), fail=[(u.tag(), d) for u in q for bad, d in [c2(u, rule)] if bad],
                     note='items with a q field only; %d paper unit(s) built from an instruction are not measured' % (len(units) - len(q)))
    res['C3'] = dict(status='NOT_MEASURED', why='a paper holds no key entry; read the items file or the key', fail=[], checked=0)
    res['C4'] = dict(status='NOT_MEASURED', why='the options of the paper are not read by this tool; read the items file', fail=[], checked=0)
    return res


def print_report(name, res, out=sys.stdout):
    print('SOURCE %s' % name, file=out)
    for r in RULES:
        x = res[r]
        if x['status'] != 'MEASURED': print('  %-3s NOT_MEASURED  %s  (%s)' % (r, TITLES[r], x['why']), file=out); continue
        print('  %-3s %s  fail %d of %d  %s' % (r, 'FAIL' if x['fail'] else 'PASS', len(x['fail']), x['checked'], TITLES[r]), file=out)
        if x.get('note'): print('         note: %s' % x['note'], file=out)
        for tag, d in x['fail']: print('         - %s  (%s)' % (tag, d), file=out)


def cmd_check(a):
    rule = load(a.rule); units = read_items(a.items, rule)
    results = [('items file', run_items(units, rule))]
    if a.paper: results.append(('paper', run_paper(paper_units(a.paper, a.items, units), rule)))
    print('Clarity check v1.0.1  rule file %s   items %d' % (os.path.basename(a.rule), len(units)))
    for n, r in results: print_report(n, r)
    print('C4b  NOT_MEASURED  every option plausible, no trick wording (a human judgement; not part of the C4 result)')
    nfail = sum(len(r[k]['fail']) for _, r in results for k in RULES)
    if a.json:
        with open(a.json, 'w') as f: json.dump({n: r for n, r in results}, f, indent=1)
    print('RESULT %s' % ('PASS' if nfail == 0 else 'FAIL'))
    return 0 if nfail == 0 else 1


# ------------------------------------------------------------------------------------------------ fixtures
def build_fixture_files(cases, workdir, tag):
    import docx
    items = []
    for c in cases:
        it = dict(key='fx:%s' % c['id'], type=c['type'], sub_question='Q%s.%s' % (c['label'][:-1], c['label'][-1]))
        for k in ('q', 'instruction', 'options', 'answer', 'premises', 'responses', 'blanks', 'distractors', 'steps', 'solution'):
            if k in c: it[k] = c[k]
        if c.get('tip'): it['tip'] = c['tip']
        items.append(it)
    ipath = os.path.join(workdir, 'fixture_items_%s.json' % tag)
    with open(ipath, 'w', encoding='utf-8') as f: json.dump(dict(items=items), f)
    d = docx.Document(); d.add_paragraph('Synthetic Fixture Course'); d.add_paragraph('Fixture Exam')
    d.add_paragraph('Question 1 - Fixture questions (10 points)'); d.add_paragraph('Read each case and answer it.')
    for c in cases:
        if 'q' in c:
            d.add_paragraph('%s. %s  (2 points)' % (c['label'], c['q']))
            if c.get('tip'): d.add_paragraph(c['tip'])
            for k, o in enumerate(c.get('options', [])): d.add_paragraph('%s.\t%s' % ('ABCDE'[k], o))
    ppath = os.path.join(workdir, 'fixture_paper_%s.docx' % tag); d.save(ppath)
    return ipath, ppath


def cmd_fixtures(a):
    rule = load(a.rule); spec = load(a.spec); os.makedirs(a.workdir, exist_ok=True)
    cases = spec['cases']
    ipath, ppath = build_fixture_files(cases, a.workdir, 'all')
    units = read_items(ipath, rule)
    ri = run_items(units, rule); rp = run_paper(paper_units(ppath, ipath, units), rule)
    def fails(res, r): return dict((t.split(' [')[0], d) for t, d in res[r]['fail'])
    print('FIXTURES v1.0.0  spec %s   cases %d' % (os.path.basename(a.spec), len(cases)))
    print('E = expected, I = reported from the items file, P = reported from the paper (letters are rules C1..C5; p = pass, F = fail, - = not measured on the paper).')
    print('%-5s %-5s %-6s %-6s %-6s %-6s %s' % ('fixt', 'label', 'broken', 'E', 'I', 'P', 'match')); wrong = 0; rows = 0
    for c in cases:
        key = 'fx:%s' % c['id']; E_ = I_ = P_ = ''; allok = True
        for r in RULES:
            e = c['expect'].get(r, 'PASS'); fi = fails(ri, r)
            i_ = 'FAIL' if key in fi else 'PASS'
            why = c.get('why', {}).get(r); why = [why] if isinstance(why, str) else (why or [])
            ok = i_ == e and all(w in fi.get(key, '') for w in why); rows += 1
            P = '-'
            if rp[r]['status'] == 'MEASURED' and not (r == 'C2' and 'q' not in c):
                fp = fails(rp, r); p_ = 'FAIL' if key in fp else 'PASS'; rows += 1
                if not (p_ == e and all(w in fp.get(key, '') for w in why)): ok = False
                P = 'F' if p_ == 'FAIL' else 'p'
            if not ok: wrong += 1; allok = False
            E_ += 'F' if e == 'FAIL' else 'p'; I_ += 'F' if i_ == 'FAIL' else 'p'; P_ += P
        broken = ','.join(r for r in RULES if c['expect'].get(r) == 'FAIL') or '-'
        print('%-5s %-5s %-6s %-6s %-6s %-6s %s' % (c['id'], c['label'], broken, E_, I_, P_, 'ok' if allok else 'WRONG'))
    nb = sum(1 for c in cases if 'FAIL' in c['expect'].values())
    print('rows compared %d; broken-in-one-way fixtures %d; good or boundary fixtures %d' % (rows, nb, len(cases) - nb))
    print('paper: C3 %s, C4 %s' % (rp['C3']['status'], rp['C4']['status']))
    print('RESULT %s  (%d fixture(s) answered wrongly)' % ('PASS' if wrong == 0 else 'FAIL', wrong))
    return 0 if wrong == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check'); c.add_argument('--items', required=True); c.add_argument('--paper'); c.add_argument('--rule', default=DEFAULT_RULE); c.add_argument('--json')
    f = sub.add_parser('fixtures'); f.add_argument('--spec', required=True); f.add_argument('--workdir', required=True); f.add_argument('--rule', default=DEFAULT_RULE)
    a = ap.parse_args()
    try:
        return cmd_check(a) if a.cmd == 'check' else cmd_fixtures(a)
    except (OSError, KeyError, ValueError, ImportError) as e:
        print('INPUT ERROR: %s %s' % (type(e).__name__, e), file=sys.stderr); return 2


if __name__ == '__main__':
    sys.exit(main())
