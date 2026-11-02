#!/usr/bin/env python3
"""SEN0401 exam readability check, version 1.0.0 (new file). Holds no question and no answer.

Reads (a) a private items file (JSON, the items-file format of the paper builder) and (b) the text of a paper Word file (.docx),
both given by path, and applies the rules of sen0401_exam_readability_rule_v1_0_0.json:
  R1 stem at most 60 words           R2 no word Tips and no glossary sentence 'term: meaning' in a stem
  R3 a needed tip is named 'see tip <label>' and the label is on the tips list
  R4 answer-format line: at most 25 words, starts with a verb, names the unit, no unexplained 'Sheet row' / 'Unit:' / 'digit per box'
  R5 every direction sentence of the cover at most 25 words      R6 every abbreviation spelled out at first use
It prints, per rule and per source, the count of items that fail, by KEY and LABEL only (never the text).

Usage:
  check    --items ITEMS.json --paper PAPER.docx [--rule RULE.json] [--json OUT.json]
  fixtures --spec FIXTURES.json --workdir DIR [--rule RULE.json]      (builds a synthetic items file and a synthetic paper from the fixtures,
                                                                      runs both readers on them and prints expected against reported; exit 1 on any difference)
Exit codes: 0 all clear (check: no failing item; fixtures: all as expected), 1 failing items found / fixtures differ, 2 usage or input error.
A rule that cannot be measured from a source prints NOT_MEASURED (never a pass)."""
import argparse, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULE = os.path.join(HERE, 'sen0401_exam_readability_rule_v1_0_0.json')
RULES = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']


def load_rule(path):
    with open(path, encoding='utf-8') as f: return json.load(f)


def words(text):
    return [t for t in text.split() if re.search(r'[A-Za-z0-9]', t)]


def nwords(text): return len(words(text))


def norm(text): return re.sub(r'\s+', ' ', text).strip()


def sentences(text, rule):
    text = norm(text)
    return [s for s in re.split(rule['sentence_split'], text) if s.strip()] if text else []


class Unit:
    """One checked unit: an item (key + labels) or a cover paragraph."""
    def __init__(self, key, labels, kind='item'):
        self.key = key; self.labels = labels; self.kind = kind
        self.stems = []          # stem texts (no code, no format line)
        self.formats = []        # answer-format lines
        self.inline_tips = False  # paper: a paragraph that starts with Tips under the question
        self.needs_tip = False
        self.unit = None
        self.abbr_declared = []  # keys of the item's own abbreviations list
        self.abbr_texts = []     # every text of the unit read in order for R6 (stems, options, bank, format lines)

    def tag(self): return '%s [%s]' % (self.key, ','.join(self.labels)) if self.labels else self.key


# ---------------------------------------------------------------------------------------------- items file reader
def labels_of(sub):
    out = []
    for m in re.finditer(r'Q(\d+)\.([a-z])', sub or ''): out.append('%s%s' % (m.group(1), m.group(2)))
    return out


def strings_of(v):
    if isinstance(v, str): return [v]
    if isinstance(v, list): return [s for x in v for s in strings_of(x)]
    if isinstance(v, dict): return [s for k, x in v.items() if k in ('text', 'answer', 'entry') for s in strings_of(x)]
    return []


def read_items(path, rule):
    with open(path, encoding='utf-8') as f: d = json.load(f)
    items = d['items'] if isinstance(d, dict) else d
    units = []
    for it in items:
        u = Unit(it.get('key', '?'), labels_of(it.get('sub_question', '')))
        stems = []
        if it.get('q'): stems.append(it['q'])
        elif it.get('instruction'): stems.append(it['instruction'])
        for b in it.get('blanks', []) or []:
            if isinstance(b, dict) and b.get('text'): stems.append(b['text'])
        pm = re.compile(rule['points_marker'])
        u.stems = [norm(pm.sub('', s)) for s in stems]
        fl = it.get('format_line')
        u.formats = [fl] if isinstance(fl, str) else list(fl or [])
        u.has_format_field = 'format_line' in it
        u.needs_tip = bool(it.get('tips'))
        u.unit = it.get('unit')
        u.abbr_declared = list((it.get('abbreviations') or {}).keys())
        texts = list(u.stems)
        for fld in ('options', 'premises', 'responses', 'steps', 'distractors'):
            texts += strings_of(it.get(fld))
        for b in it.get('blanks', []) or []:
            if isinstance(b, dict) and b.get('answer'): texts.append(b['answer'])
        texts += u.formats
        u.abbr_texts = texts
        units.append(u)
    def order(u):
        m = re.match(r'(\d+)([a-z])', u.labels[0]) if u.labels else None
        return (int(m.group(1)), m.group(2)) if m else (999, '')
    units.sort(key=order)
    tips = d.get('tips_page') if isinstance(d, dict) else None
    return units, (dict(tips) if isinstance(tips, dict) else {})


# ---------------------------------------------------------------------------------------------- paper reader
def expand_labels(a, b):
    if not b: return [a]
    ma, mb = re.match(r'(\d+)([a-z])', a), re.match(r'(\d+)([a-z])', b)
    if not (ma and mb and ma.group(1) == mb.group(1)): return [a, b]
    return ['%s%s' % (ma.group(1), chr(c)) for c in range(ord(ma.group(2)), ord(mb.group(2)) + 1)]


def is_format_sentence(s, rule):
    pat = '|'.join(rule['rules']['R4']['format_markers'])
    return re.search(pat, s, re.I) is not None


def key_text(t): return re.sub(r'[^a-z0-9]+', '', t.lower())


def common_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y: break
        n += 1
    return n


def read_paper(path, rule, iu):
    import docx
    doc = docx.Document(path)
    pm = re.compile(rule['points_marker']); lab = re.compile(rule['label_paragraph']); opt = re.compile(rule['option_paragraph'])
    qh = re.compile(rule['question_heading']); th = re.compile(rule['tips_heading'], re.I); tp = re.compile(rule['tip_paragraph'])
    directions = []      # (id, text)
    qdirections = []
    entries = []         # label entries: dict(labels, stems, formats, inline_tips, texts)
    tips = {}; tip_texts = []
    section = 'front'; cur = None; after_heading = False; qn = 0
    for p in doc.paragraphs:
        raw = p.text; t = norm(raw)
        if not t: continue
        if section != 'tips' and th.match(t): section = 'tips'; continue
        if section == 'tips':
            m = tp.match(t)
            if m: tips[m.group(1)] = t; tip_texts.append((m.group(1), t))
            continue
        m = qh.match(t)
        if m:
            section = 'q'; after_heading = True; qn = int(m.group(1)); cur = None
            directions.append(('Q%d-head' % qn, t, 'q-heading')); continue
        if section == 'front':
            if re.search(r'[.!?](\s|$)', t): directions.append(('cover', t, 'cover'))
            continue
        if after_heading:
            after_heading = False
            if not lab.match(t): directions.append(('Q%d-instruction' % qn, t, 'q-instruction')); continue
        m = lab.match(t)
        if m:
            labs = expand_labels(m.group(1), m.group(2))
            body = pm.sub('', t[m.end():])
            stem_s, fmt_s = [], []
            for s in sentences(body, rule): (fmt_s if is_format_sentence(s, rule) else stem_s).append(s)
            cur = dict(labels=labs, stems=[' '.join(stem_s)] if stem_s else [], formats=fmt_s, inline_tips=False, texts=[' '.join(stem_s)] + fmt_s)
            entries.append(cur); continue
        if cur is None: continue
        if re.match(r'^Tips\b', t): cur['inline_tips'] = True; cur['texts'].append(t); continue
        if opt.match(raw.lstrip()): cur['texts'].append(t); continue
        mono = any(any(k.lower() in (r.font.name or '').lower() for k in rule['code_fonts']) for r in p.runs)
        if '\n' in raw or mono: continue      # a code listing
        cur['formats'].append(t); cur['texts'].append(t); continue      # any other paragraph under a label is its answer-format line
    # map the label entries to items: by the opening words of the stem (the paper's printed labels follow the paper order, not the items file's);
    # an entry with no stem of its own, or a group direction over several labels, takes the item of the next entry
    stem_index = [(key_text(st), u.key) for u in iu for st in u.stems if key_text(st)]
    def match(e):
        best = (0, None, False)         # (common prefix length, key, ambiguous)
        for st in e['stems']:
            k = key_text(st)
            for kk, key in stem_index:
                n = 10 ** 6 if (k and k == kk) else common_prefix(k, kk)
                if n > best[0]: best = (n, key, False)
                elif n == best[0] and n > 0 and key != best[1]: best = (n, best[1], True)
        return best[1] if best[0] >= 40 and not best[2] else None
    keys = [match(e) for e in entries]
    for i in range(len(entries) - 2, -1, -1):
        if keys[i] is None and (not entries[i]['stems'] or len(entries[i]['labels']) > 1) and keys[i + 1] is not None: keys[i] = keys[i + 1]
    by_key = {}
    order = []
    for e, key in zip(entries, keys):
        unitkey = key if key else '(paper only):' + ','.join(e['labels'])
        u = by_key.get(unitkey)
        if u is None:
            u = Unit(key or '(paper only)', []); by_key[unitkey] = u; order.append(u)
        for l in e['labels']:
            if l not in u.labels: u.labels.append(l)
        u.stems += e['stems']; u.formats += e['formats']; u.inline_tips = u.inline_tips or e['inline_tips']
        u.abbr_texts += e['texts']
    return order, directions, tips, tip_texts


# ---------------------------------------------------------------------------------------------- rules
def strip_tip_refs(text, rule):
    r3 = rule['rules']['R3']
    return re.sub(r3['name_pattern'] + r'(?:\s+on the tips page)?', '', text, flags=re.I)


def tip_refs(text, rule):
    r3 = rule['rules']['R3']; out = []
    for m in re.finditer(r3['name_pattern'], text, re.I): out += re.findall(r3['label_pattern'], m.group(1))
    return out


def check_r1(u, rule):
    lim = rule['rules']['R1']['max_stem_words']; w = max([nwords(s) for s in u.stems] or [0])
    return w > lim, 'words=%d' % w


def check_r2(u, rule):
    pat = re.compile(rule['rules']['R2']['glossary_pattern']); bad = []
    for s in u.stems:
        c = strip_tip_refs(s, rule)
        if re.search(r'\btips\b', c, re.I): bad.append('word Tips')
        if pat.search(c): bad.append('glossary form')
    if u.inline_tips: bad.append('tips paragraph under the question')
    return bool(bad), '; '.join(sorted(set(bad)))


def check_r3(u, rule, tips_list):
    refs = [r for s in u.stems for r in tip_refs(s, rule)]
    needs = u.needs_tip or u.inline_tips
    why = []
    if needs and not refs: why.append('needs a tip, names none')
    missing = [r for r in refs if r not in tips_list]
    if missing: why.append('%d label(s) not on the tips list' % len(set(missing)))
    return bool(why), '; '.join(why)


def check_r4(u, rule):
    r4 = rule['rules']['R4']; why = []
    if u.unit and not u.formats: why.append('item has a unit, no format line')
    for line in u.formats:
        n = nwords(line)
        if n > r4['max_format_words']: why.append('%d words' % n)
        fw = re.match(r'[A-Za-z]+', line.strip())
        if not fw or fw.group(0) not in r4['verbs']: why.append('does not start with a listed verb')
        for ph in r4['forbidden_phrases']:
            for m in re.finditer(re.escape(ph), line, re.I):
                rest = line[m.end():]
                if not any(re.match(x, rest, re.I) for x in r4['explained_after']): why.append('unexplained phrase #%d' % (r4['forbidden_phrases'].index(ph) + 1)); break
    if u.unit and u.formats and not any(re.search(r'\b' + re.escape(str(u.unit)) + r'\b', l, re.I) and not re.search(r'unit:', l, re.I) for l in u.formats):
        why.append('unit not named in words')
    return bool(why), '; '.join(sorted(set(why)))


def abbreviations_in(text, rule, doc_text):
    r6 = rule['rules']['R6']; found = []
    for pat in r6['capital_patterns']:
        for m in re.finditer(pat, text):
            tok = m.group(0)
            if tok in r6['not_abbreviations']: continue
            if r6.get('lower_case_twin_is_a_word') and tok.isupper() and re.search(r'\b' + re.escape(tok.lower()) + r'\b', doc_text): continue
            found.append((m.start(), m.end(), tok))
    return found


def spelled_out(text, s, e, rule):
    before, after = text[:s], text[e:]
    if re.match(r'\s*\(\s*[^()]*[a-z][^()]*\)', after) and len(re.match(r'\s*\(\s*([^()]*)\)', after).group(1).split()) >= 1 and len(re.match(r'\s*\(\s*([^()]*)\)', after).group(1)) >= 4: return True
    if before.endswith('(') and after.startswith(')'):
        pre = before[:-1].rstrip()
        if len(re.findall(r"[A-Za-z][\w'-]*", pre[-60:])) >= 2: return True
    return False


def check_r6(units, rule, extra_after=None):
    """Reading order = the order of units, then of their texts. Returns {unit tag: n abbreviations unexpanded at first use}."""
    alltext = ' '.join(t for u in units for t in u.abbr_texts) + ' ' + ' '.join(extra_after or [])
    doc_lower = alltext; seen = set(); fails = {}
    for u in units:
        for text in u.abbr_texts:
            toks = abbreviations_in(text, rule, doc_lower)
            for d in u.abbr_declared:
                for m in re.finditer(r'\b' + re.escape(d) + r'\b', text, re.I): toks.append((m.start(), m.end(), m.group(0)))
            toks.sort()
            for s, e, tok in toks:
                k = tok.lower()
                if k in seen: continue
                seen.add(k)
                if not spelled_out(text, s, e, rule): fails[u] = fails.get(u, 0) + 1
    return fails


def check_r5(directions, rule):
    lim = rule['rules']['R5']['max_direction_words']; out = {'cover': [], 'q': []}
    n = 0
    for ident, text, kind in directions:
        if kind == 'q-heading': continue
        key = 'cover' if kind == 'cover' else 'q'
        if key == 'cover': n += 1
        ss = sentences(text, rule); mx = max([nwords(s) for s in ss] or [0])
        out[key].append(('P%02d' % n if key == 'cover' else ident, mx, mx > lim))
    return out


# ---------------------------------------------------------------------------------------------- one source
def run_source(name, units, directions, tips_list, rule, has_formats):
    res = {}
    for r, fn in (('R1', lambda u: check_r1(u, rule)), ('R2', lambda u: check_r2(u, rule)), ('R3', lambda u: check_r3(u, rule, tips_list)), ('R4', lambda u: check_r4(u, rule))):
        if r == 'R4' and not has_formats: res[r] = dict(status='NOT_MEASURED', why='the source has no answer-format lines', fail=[], checked=0); continue
        fails = []
        for u in units:
            bad, detail = fn(u)
            if bad: fails.append((u.tag(), detail))
        res[r] = dict(status='MEASURED', fail=fails, checked=len(units))
    if directions is None: res['R5'] = dict(status='NOT_MEASURED', why='the source has no cover', fail=[], checked=0)
    else:
        d5 = check_r5(directions, rule)
        res['R5'] = dict(status='MEASURED', fail=[('cover:%s' % k, 'max sentence words=%d' % mx) for k, mx, bad in d5['cover'] if bad], checked=len(d5['cover']))
        res['R5q'] = dict(status='MEASURED', fail=[('%s' % k, 'max sentence words=%d' % mx) for k, mx, bad in d5['q'] if bad], checked=len(d5['q']))
    chain = list(units) if directions is None else [front_unit(directions)] + list(units)
    if tips_list:
        tu = Unit('tips', [], 'tips'); tu.abbr_texts = [t for t in tips_list.values() if isinstance(t, str)]; chain.append(tu)
    f6 = check_r6(chain, rule)
    res['R6'] = dict(status='MEASURED', fail=[(u.tag(), '%d abbreviation(s) not spelled out at first use' % n) for u, n in f6.items() if u.kind == 'item'] + [(u.tag(), '%d abbreviation(s) not spelled out at first use' % n) for u, n in f6.items() if u.kind != 'item'], checked=len(units))
    return res


def front_unit(directions):
    u = Unit('cover', [], 'cover'); u.abbr_texts = [t for i, t, k in directions if k in ('cover', 'q-instruction')]
    return u


def print_report(name, res, out=sys.stdout):
    titles = {'R1': 'stem at most 60 words', 'R2': 'no Tips word, no glossary sentence in a stem', 'R3': 'needed tip named, label on the tips list', 'R4': 'answer-format line',
              'R5': 'cover direction sentence at most 25 words', 'R5q': '(information, not part of R5) question-heading direction sentences at most 25 words', 'R6': 'abbreviation spelled out at first use'}
    print('SOURCE %s' % name, file=out)
    for r in ['R1', 'R2', 'R3', 'R4', 'R5', 'R5q', 'R6']:
        if r not in res: continue
        x = res[r]
        if x['status'] != 'MEASURED': print('  %-4s NOT_MEASURED  %s  (%s)' % (r, titles[r], x['why']), file=out); continue
        print('  %-4s %s  fail %d of %d  %s' % (r, 'FAIL' if x['fail'] else 'PASS', len(x['fail']), x['checked'], titles[r]), file=out)
        for tag, detail in x['fail']: print('         - %s  (%s)' % (tag, detail), file=out)


def cmd_check(a):
    rule = load_rule(a.rule)
    iu, itips = read_items(a.items, rule)
    pu, directions, ptips, _ = read_paper(a.paper, rule, iu)
    keyinfo = {u.key: u for u in iu}
    for u in pu:
        src = keyinfo.get(u.key)
        if src: u.needs_tip = src.needs_tip; u.unit = src.unit; u.abbr_declared = src.abbr_declared
    has_fmt_items = any(u.has_format_field for u in iu)
    r_items = run_source('items file', iu, None, itips, rule, has_fmt_items)
    r_paper = run_source('paper', pu, directions, ptips, rule, True)
    print('Readability check v1.0.0  rule file %s' % os.path.basename(a.rule))
    print('items units: %d   paper units: %d (of which paper-only: %d)   tips on the tips list: items %d, paper %d' % (len(iu), len(pu), sum(1 for u in pu if u.key == '(paper only)'), len(itips), len(ptips)))
    print('Labels: items file = the structure label of the sub-question; paper = the label printed on the paper (the paper order is shuffled by the builder).')
    print_report('items file', r_items); print_report('paper', r_paper)
    total = sum(len(r_items[r]['fail']) + len(r_paper[r]['fail']) for r in RULES if r in r_items and r in r_paper)
    if a.json:
        with open(a.json, 'w') as f: json.dump(dict(items=r_items, paper=r_paper), f, indent=1)
    print('RESULT %s' % ('PASS' if total == 0 and all(r_items[r]['status'] == 'MEASURED' for r in RULES) else 'FAIL'))
    return 0 if total == 0 else 1


# ---------------------------------------------------------------------------------------------- fixtures
def build_fixture_files(spec, workdir):
    import docx
    items = []
    for c in spec['cases']:
        it = dict(key='fx:%s' % c['id'], type=c.get('type', 'ChoiceFour'), sub_question='Q%s.%s' % (c['label'][:-1], c['label'][-1]), q=c['stem'],
                  options=c.get('options', ['Option one.', 'Option two.', 'Option three.', 'Option four.']), tips=c.get('tips', []), abbreviations=c.get('abbreviations', {}))
        if 'unit' in c: it['unit'] = c['unit']
        if 'format_line' in c: it['format_line'] = c['format_line']
        items.append(it)
    ipath = os.path.join(workdir, 'fixture_items.json')
    with open(ipath, 'w', encoding='utf-8') as f: json.dump(dict(items=items, tips_page=spec['tips_page']), f)
    d = docx.Document()
    d.add_paragraph('Synthetic Fixture Course'); d.add_paragraph('Fixture Exam')
    for dd in spec['directions']: d.add_paragraph(dd['text'])
    d.add_paragraph('Question 1 - Fixture questions (10 points)'); d.add_paragraph('Read each case and answer it.')
    for c in spec['cases']:
        d.add_paragraph('%s. %s  (2 points)' % (c['label'], c['stem']))
        if 'format_line' in c: d.add_paragraph(c['format_line'])
        for k, o in enumerate(c.get('options', ['Option one.', 'Option two.', 'Option three.', 'Option four.'])): d.add_paragraph('%s.\t%s' % ('ABCD'[k], o))
    d.add_paragraph('Tips')
    for lab, text in spec['tips_page'].items(): d.add_paragraph('Tip %s. %s' % (lab, text))
    ppath = os.path.join(workdir, 'fixture_paper.docx'); d.save(ppath)
    return ipath, ppath


def cmd_fixtures(a):
    rule = load_rule(a.rule)
    with open(a.spec, encoding='utf-8') as f: spec = json.load(f)
    os.makedirs(a.workdir, exist_ok=True)
    ipath, ppath = build_fixture_files(spec, a.workdir)
    iu, itips = read_items(ipath, rule)
    pu, directions, ptips, _ = read_paper(ppath, rule, iu)
    keyinfo = {u.key: u for u in iu}
    for u in pu:
        src = keyinfo.get(u.key)
        if src: u.needs_tip = src.needs_tip; u.unit = src.unit; u.abbr_declared = src.abbr_declared
    r_items = run_source('items file', iu, None, itips, rule, True)
    r_paper = run_source('paper', pu, directions, ptips, rule, True)
    fails = lambda res, r: dict((t.split(' [')[0], d) for t, d in res[r]['fail'])
    print('FIXTURES v1.0.0  spec %s   cases %d   directions %d' % (os.path.basename(a.spec), len(spec['cases']), len(spec['directions'])))
    print('Table: one row per fixture. E = expected, I = reported from the items file, P = reported from the paper; letters are the rules R1 R2 R3 R4 R6 (p = pass, F = fail).')
    print('%-5s %-5s %-6s %-7s %-7s %-7s %s' % ('fixt', 'label', 'broken', 'E', 'I', 'P', 'match'))
    wrong = 0; rows = 0
    for c in spec['cases']:
        key = 'fx:%s' % c['id']; E_ = I_ = P_ = ''; allok = True
        for r in ['R1', 'R2', 'R3', 'R4', 'R6']:
            e = c['expect'].get(r, 'PASS')
            ri = 'FAIL' if key in fails(r_items, r) else 'PASS'; rp = 'FAIL' if key in fails(r_paper, r) else 'PASS'
            why = c.get('why', {}).get(r)
            wi = fails(r_items, r).get(key, ''); wp = fails(r_paper, r).get(key, '')
            ok = (ri == e and rp == e and (why is None or (why in wi and why in wp))); rows += 1
            if not ok: wrong += 1; allok = False
            E_ += 'F' if e == 'FAIL' else 'p'; I_ += 'F' if ri == 'FAIL' else 'p'; P_ += 'F' if rp == 'FAIL' else 'p'
        broken = ','.join(r for r in c['expect'] if c['expect'][r] == 'FAIL') or '-'
        print('%-5s %-5s %-6s %-7s %-7s %-7s %s' % (c['id'], c['label'], broken, E_, I_, P_, 'ok' if allok else 'WRONG'))
    cover_fail = set(k.split(':')[1] for k, _ in r_paper['R5']['fail'])
    for n, dd in enumerate(spec['directions'], 1):
        e = dd['expect']; rp = 'FAIL' if 'P%02d' % n in cover_fail else 'PASS'
        wd = dict((k.split(':')[1], d) for k, d in r_paper['R5']['fail']).get('P%02d' % n, '')
        ok = rp == e and (dd.get('why') is None or dd['why'] in wd); rows += 1
        if not ok: wrong += 1
        print('%-5s %-5s %-6s %-7s %-7s %-7s %s' % (dd['id'], 'cover', 'R5' if e == 'FAIL' else '-', 'F' if e == 'FAIL' else 'p', 'n/a', 'F' if rp == 'FAIL' else 'p', 'ok' if ok else 'WRONG'))
    n_fail_cases = sum(1 for c in spec['cases'] if 'FAIL' in c['expect'].values()) + sum(1 for d in spec['directions'] if d['expect'] == 'FAIL')
    n_good = len(spec['cases']) + len(spec['directions']) - n_fail_cases
    print('rows compared (case x rule, both sources; directions on the paper) %d; broken-in-one-way fixtures %d; good or boundary fixtures %d' % (rows, n_fail_cases, n_good))
    print('items file R5: %s' % r_items['R5']['status'])
    print('RESULT %s  (%d row(s) answered wrongly)' % ('PASS' if wrong == 0 else 'FAIL', wrong))
    return 0 if wrong == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check'); c.add_argument('--items', required=True); c.add_argument('--paper', required=True); c.add_argument('--rule', default=DEFAULT_RULE); c.add_argument('--json')
    f = sub.add_parser('fixtures'); f.add_argument('--spec', required=True); f.add_argument('--workdir', required=True); f.add_argument('--rule', default=DEFAULT_RULE)
    a = ap.parse_args()
    try:
        return cmd_check(a) if a.cmd == 'check' else cmd_fixtures(a)
    except (OSError, KeyError, ValueError) as e:
        print('INPUT ERROR: %s' % type(e).__name__, file=sys.stderr); return 2


if __name__ == '__main__':
    sys.exit(main())
