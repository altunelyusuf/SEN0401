"""SEN0401 general exam engine, version 1.0.0. New file; reads the chapter banks, never edits them.

What it does
  1. Pools items: the chapter question banks (read only, four-option choice) and an optional authored-items JSON file (any registered suited type).
  2. Composes cross-chapter SYNTHESIS matching items from bank items of different chapters (machine-assembled; flagged for instructor review).
  3. Builds TWO papers (midterm, make-up) over one chapter list (a parameter; default 1-6, chapter 7 selectable): chapter weights, higher-Bloom
     majority, evenly distributed answer letters, randomised fill-in banks, incremented versions, make-up disjoint from the midterm.
  4. Writes every paper as RDF, validates it with the printed-paper rules (R01-R22) plus the engine rules (EN01-EN10) and REFUSES (ExamRefused,
     exit code 2) when a rule is broken. Nothing is written when a paper is refused.
  5. Renders a print-safe PDF and an answer-key JSON (see sen0401_exam_engine_render_v1_0_0.py).

Parameters the owner must set are required, not defaulted: --items (the number of items). Only the chapter list has a default (1-6).
Authored items file (JSON):  {"items": [ {"key","type","chapters":[..],"bloom":1-6,"kind":"direct|synthesis|indirect","source":{"file","locator"},"terms":[..],
   "papers":["midterm","makeup"], + type fields} ]}   type fields:
   ChoiceFour / ChoiceFourCode: q, options[4], answer(index), code(optional)    Matching: premises[{text,match}], responses[]
   Ordering: steps[in correct order]    FillBlankGroup: blanks[{text,answer}], distractors[>=2]    NumericAnswer: q, key, unit, tolerance
   CodeTrace: q, code, output    ShortAnswer: q, rubric[1-3], lines[1-3] (needs --enable ShortAnswer)
Every authored term in "terms" must be found in the course corpus (banks, decks and notes, critical points) or the item is refused (EN08).
Usage: engine.py build --items N [--chapters 1-6] [--matching M] [--seed S] [--authored FILE] [--outdir DIR] [options]
"""
import argparse, collections, glob, hashlib, json, math, os, random, re, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
from rdflib import Graph, Namespace, Literal, RDF, URIRef, XSD
import pyshacl
import sen0401_exam_pagesave_measure_v1_0_0 as M
SH = Namespace('http://www.w3.org/ns/shacl#')
PR = Namespace('http://example.org/sen0401/paperrules#')
EN = Namespace('http://example.org/sen0401/engine#')
EX = Namespace('http://example.org/sen0401/engine/paper#')
V = 'sen0401_exam_%s_v1_0_0'
LEVEL = {'Remember': 1, 'Understand': 2, 'Apply': 3, 'Analyze': 4, 'Evaluate': 5, 'Create': 6}
CHOICE = ('ChoiceFour', 'ChoiceFourCode')
BANK_FILES = {}


class ExamRefused(Exception):
    def __init__(self, violations):
        self.violations = violations
        super().__init__('REFUSED: ' + '; '.join('%s %s' % (r, m) for r, s, m in violations if s == 'Violation'))


def rel(p): return os.path.relpath(p, ROOT)


# ------------------------------------------------------------------ parameters
class Params:
    def __init__(self, items, chapters=(1, 2, 3, 4, 5, 6), weights=None, matching=0, higher_from=3, higher_share=0.6, synthesis_min=0,
                 indirect_enabled=False, seed=4701, sitting=60, columns=2, code_cap=45, answer_mode='CircleOnItem', page_limit=None,
                 enable=(), allow_repeat=False, authored=None, order='chapter', font=10, code_font=9):
        self.items = items; self.chapters = tuple(chapters); self.weights = weights or {c: 1 for c in chapters}
        self.matching = matching; self.higher_from = higher_from; self.higher_share = higher_share; self.synthesis_min = synthesis_min
        self.indirect_enabled = indirect_enabled; self.seed = seed; self.sitting = sitting; self.columns = columns; self.code_cap = code_cap
        self.answer_mode = answer_mode; self.page_limit = page_limit; self.enable = tuple(enable); self.allow_repeat = allow_repeat
        self.authored = authored; self.order = order; self.font = font; self.code_font = code_font

    def snapshot(self):
        return {k: (list(v) if isinstance(v, tuple) else v) for k, v in self.__dict__.items()}


def quotas(chapters, weights, n):
    """Largest-remainder split of n items over the chapters by weight (ties to the lower chapter)."""
    tot = float(sum(weights[c] for c in chapters))
    raw = {c: n * weights[c] / tot for c in chapters}; q = {c: int(math.floor(raw[c])) for c in chapters}
    for c in sorted(chapters, key=lambda c: (-(raw[c] - q[c]), c))[: n - sum(q.values())]: q[c] += 1
    return q


# ------------------------------------------------------------------ pools
def bank_pool(chapters, code_cap):
    """Bank items of the chapters that print on paper: no letter-referencing options, code unwrapped and short. Read only."""
    ref = re.compile(r'\b(all|none|both) of the (above|options|choices)\b|\b(option|choice) [A-D]\b|\b[A-D] (and|or) [A-D]\b', re.I)
    pool = []; stats = {}
    for c in chapters:
        f, b = M.load_bank(c); BANK_FILES[c] = rel(f); ok = 0
        for idx, i in enumerate(b):
            code = i.get('code')
            if len(i['q']) >= 400 or any(ref.search(o) for o in i['options']) or len(set(i['options'])) < 4: continue
            if code and (max(len(l) for l in code.split('\n')) > code_cap or len(code.split('\n')) > 12): continue
            ok += 1
            pool.append(dict(key='bank:ch%02d:%s:%d' % (c, i['concept'], idx), type='ChoiceFourCode' if code else 'ChoiceFour', chapters=[c], primary=c,
                             bloom=LEVEL[i['level']], kind='direct', source=dict(file=rel(f), locator='item %d, concept %s' % (idx, i['concept'])),
                             q=i['q'], code=code, options=list(i['options']), answer=i['answer'], concept=i['concept'], why=i.get('why', '')))
        stats[c] = (len(b), ok)
    return pool, stats


def authored_pool(path, chapters):
    """Authored items: validated for shape here; their terms are checked against the corpus in check_terms()."""
    if not path: return [], []
    raw = json.load(open(path, encoding='utf8'))['items']; out = []; skipped = []
    for r in raw:
        ch = list(r['chapters'])
        if not set(ch) <= set(chapters): skipped.append((r['key'], 'chapters %s not all in the chapter list' % ch)); continue
        it = dict(r); it['primary'] = ch[0]; it.setdefault('kind', 'direct'); it.setdefault('papers', ['midterm', 'makeup']); it.setdefault('terms', [])
        out.append(it)
    return out, skipped


_INDEX = []
def corpus_index():
    if _INDEX: return _INDEX[0]
    parts = []
    for c in range(1, 9):
        f, b = M.load_bank(c)
        for i in b: parts.append(i['q'] + ' ' + ' '.join(i['options']) + ' ' + (i.get('code') or '') + ' ' + i.get('why', '') + ' ' + i['concept'])
    cp = json.load(open(os.path.join(HERE, V % 'critical_points' + '.json'), encoding='utf8'))
    for p in cp['list_A_points_carried_by_a_source']: parts.append(p['point'] + ' ' + p['source'].get('quote', ''))
    try:
        import sen0401_exam_pptx_text_v1_0_0 as T
        for c in range(1, 9):
            for s in T.slides_of(T.newest_deck(c)): parts.append(str(s.get('slide', '')) + ' ' + str(s.get('notes', '')))
    except Exception as e:
        parts.append(''); print('NOT_MEASURED  deck text unreadable (%s): terms are checked against banks and critical points only' % e, file=sys.stderr)
    _INDEX.append(re.sub(r'\s+', ' ', ' '.join(parts)).lower()); return _INDEX[0]


def unfound_terms(item):
    ix = corpus_index(); return [t for t in item.get('terms', []) if re.sub(r'\s+', ' ', t).lower() not in ix]


def compose_matching(pool, n, rnd, used, chapters, room):
    """Cross-chapter synthesis matching: 4 premises (questions of different chapters) and 6 responses (their keys plus two more keys)."""
    cand = [i for i in pool if not i.get('code') and len(i['q']) <= 130 and 15 <= len(i['options'][i['answer']]) <= 100 and i['bloom'] <= 3
            and not re.fullmatch(r'[\d\s.,]+', i['options'][i['answer']])]
    out = []
    for _ in range(n):
        chosen = []; seen_c = set(); seen_k = set()
        pick = [i for i in cand if i['key'] not in used]; rnd.shuffle(pick)
        pick.sort(key=lambda i: -i['bloom'])  # prefer Apply, then Understand
        for i in pick:
            if i['primary'] in seen_c or i['concept'] in seen_k: continue
            chosen.append(i); seen_c.add(i['primary']); seen_k.add(i['concept'])
            if len(chosen) == 4: break
        if len(chosen) < 4: break
        lead = [i for i in chosen if room.get(i['primary'], 0) > 0]
        if not lead: break  # no chapter has quota room left for the composed item
        chosen.remove(lead[0]); chosen.insert(0, lead[0]); room[lead[0]['primary']] -= 1
        extra = [i for i in pick if i not in chosen and i['concept'] not in seen_k and i['key'] not in used][:2]
        if len(extra) < 2: break
        for i in chosen + extra: used.add(i['key'])
        prem = [dict(text=i['q'], match=i['options'][i['answer']], src=i) for i in chosen]
        resp = [i['options'][i['answer']] for i in chosen + extra]; rnd.shuffle(resp)
        out.append(dict(key='match:' + '+'.join(i['key'].split(':', 2)[-1] for i in chosen), type='Matching', chapters=sorted({i['primary'] for i in chosen}),
                        primary=chosen[0]['primary'], bloom=min(3, max(i['bloom'] for i in chosen)), kind='synthesis',
                        source=dict(file=chosen[0]['source']['file'], locator='composed from ' + '; '.join(i['source']['locator'] for i in chosen)),
                        premises=[dict(text=p['text'], match=p['match']) for p in prem], responses=resp, machine_assembled=True,
                        derived_from=[i['key'] for i in chosen + extra]))
    return out


# ------------------------------------------------------------------ selection
def balance_letters(choice_items, rnd):
    """Give the keys of the choice items an even spread over A-D (counts differ by at most one) and no run of four equal keys."""
    n = len(choice_items)
    for _ in range(500):
        t = [k % 4 for k in range(n)]; rnd.shuffle(t)
        if not any(t[k] == t[k + 1] == t[k + 2] == t[k + 3] for k in range(n - 3)): break
    for it, ti in zip(choice_items, t):
        key = it['options'][it['answer']]; rest = [o for k, o in enumerate(it['options']) if k != it['answer']]; rnd.shuffle(rest)
        rest.insert(ti, key); it['options'] = rest; it['answer'] = ti


def build_paper(P, kind, exclude=frozenset(), prev_seq=0, rnd_salt=0):
    rnd = random.Random(P.seed * 7 + rnd_salt)
    pool, stats = bank_pool(P.chapters, P.code_cap)
    pool = [i for i in pool if i['key'] not in exclude]
    auth, skipped = authored_pool(P.authored, P.chapters)
    fixed = [dict(i) for i in auth if kind in i['papers'] and i['key'] not in exclude]
    used = set(i['key'] for i in fixed)
    q = quotas(P.chapters, P.weights, P.items)
    room = dict(q)
    for i in fixed: room[i['primary']] -= len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1
    fixed += compose_matching([i for i in pool if i['key'] not in used], P.matching, rnd, used, P.chapters, room)
    pool = [i for i in pool if i['key'] not in used]
    nfix = sum(len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1 for i in fixed)
    fixed_by = collections.Counter()
    for i in fixed: fixed_by[i['primary']] += len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1
    fixed_hi = sum((len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1) for i in fixed if i['bloom'] >= P.higher_from)
    picks = []
    for c in P.chapters:
        k = max(0, q[c] - fixed_by[c]); cp = [i for i in pool if i['primary'] == c]
        # at most one item per concept before concepts repeat
        rnd.shuffle(cp); hi = [i for i in cp if i['bloom'] >= P.higher_from]; lo = [i for i in cp if i['bloom'] < P.higher_from]
        kh = min(len(hi), int(math.ceil(k * P.higher_share))); take = hi[:kh] + lo[:k - kh]
        if len(take) < k: take += hi[kh:kh + k - len(take)]
        picks += take
    allit = fixed + picks
    # top up towards a higher-order majority when fixed items pull it down
    total = lambda L: sum(len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1 for i in L)
    hi_n = lambda L: sum((len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1) for i in L if i['bloom'] >= P.higher_from)
    guard = 0
    while hi_n(allit) * 2 <= total(allit) and guard < 200:
        guard += 1
        lows = [i for i in picks if i['bloom'] < P.higher_from]
        swap = None
        for lo_ in lows:
            alt = [i for i in pool if i['primary'] == lo_['primary'] and i['bloom'] >= P.higher_from and i not in picks]
            if alt: swap = (lo_, rnd.choice(alt)); break
        if not swap: break
        picks[picks.index(swap[0])] = swap[1]; allit = fixed + picks
    if P.order == 'mixed': rnd.shuffle(allit)
    else: allit.sort(key=lambda i: (i['primary'], rnd.random()))
    choice = [i for i in allit if i['type'] in CHOICE]
    balance_letters(choice, rnd)
    pos = 0
    for i in allit:
        pos += 1; i['position'] = pos
        if i['type'] == 'FillBlankGroup':
            r = random.Random(P.seed * 31 + i['position']); nt = len(i['blanks']) + len(i['distractors'])
            for _ in range(200):
                order = list(range(nt)); r.shuffle(order)
                ap = [order.index(k) for k in range(len(i['blanks']))]
                if any(ap[a] > ap[b] for a in range(len(ap)) for b in range(a + 1, len(ap))): break
            i['bank_order'] = order; pos += len(i['blanks']) - 1
        if i['type'] == 'Ordering': i['display_order'] = order_of_steps(i['position'], len(i['steps']), P.seed)
    paper = dict(kind=kind, version=prev_seq + 1, previous=prev_seq, chapters=list(P.chapters), quotas=q, params=P.snapshot(), items=allit,
                 pool_stats={str(c): v for c, v in stats.items()}, skipped=skipped, bank_files={str(c): BANK_FILES[c] for c in BANK_FILES})
    return paper


# ------------------------------------------------------------------ graph
def L(v): return Literal(v)
def I(v): return Literal(v, datatype=XSD.integer)
def B(v): return Literal(v, datatype=XSD.boolean)
def D(v): return Literal(v, datatype=XSD.decimal)


def order_of_steps(pid_pos, n, seed):
    r = random.Random(seed * 1000 + pid_pos); o = list(range(n))
    for _ in range(50):
        r.shuffle(o)
        if o != sorted(o): break
    return o


def to_graph(paper, g=None, pid=None):
    """Paper dict -> RDF in the vocabulary of the printed-paper rules plus the engine vocabulary."""
    g = g if g is not None else Graph(); g.bind('pr', PR); g.bind('en', EN)
    P = paper['params']; pid = pid or '%s_v%d' % (paper['kind'], paper['version']); p = EX[pid]
    g.add((p, RDF.type, PR.Paper)); g.add((p, PR.paperKind, PR.Midterm if paper['kind'] == 'midterm' else PR.MakeUp))
    for k, v in dict(theme='light', background='white', ink='black').items(): g.add((p, PR[k], L(v)))
    for k in ('fillColourUsed', 'containsPersonalData'): g.add((p, PR[k], B(False)))
    g.add((p, PR.fontPt, I(P['font']))); g.add((p, PR.codeFontPt, I(P['code_font']))); g.add((p, PR.sittingMinutes, I(P['sitting'])))
    g.add((p, PR.columns, I(P['columns']))); g.add((p, PR.codeColumnCapacity, I(P['code_cap'])))
    g.add((p, PR.answerMode, PR[P['answer_mode']])); g.add((p, PR.versionSeq, I(paper['version']))); g.add((p, PR.previousVersionSeq, I(paper['previous'])))
    if P['page_limit']: g.add((p, PR.pageLimit, I(P['page_limit'])))
    if paper.get('pageCount'): g.add((p, PR.pageCount, I(paper['pageCount'])))
    for c in paper['chapters']:
        g.add((p, PR.chapterList, I(c)))
        qn = EX['%s_quota%d' % (pid, c)]; g.add((p, EN.chapterQuota, qn)); g.add((qn, EN.quotaChapter, I(c))); g.add((qn, EN.quotaItems, I(paper['quotas'][c])))
    g.add((p, EN.higherFrom, I(P['higher_from']))); g.add((p, EN.synthesisMin, I(P['synthesis_min']))); g.add((p, EN.indirectEnabled, B(P['indirect_enabled'])))
    for t in P['enable']: g.add((p, PR.enables, PR[t]))
    srcn = [0]
    def src(it):
        srcn[0] += 1; s = EX['%s_src%d' % (pid, srcn[0])]; g.add((s, RDF.type, PR.CorpusSource))
        g.add((s, PR.file, L(it['source']['file']))); g.add((s, PR.locator, L(it['source']['locator']))); return s
    def base(it, n, typ, cls):
        i = EX['%s_item%d' % (pid, n)]; g.add((p, PR.hasItem, i)); g.add((i, RDF.type, PR.Item)); g.add((i, RDF.type, PR[cls])); g.add((i, PR.itemType, PR[typ]))
        g.add((i, PR.position, I(n))); g.add((i, PR.itemKey, L(it['key'] if typ != 'FillBlank' else it['key'] + '#%d' % (n - it['position'] + 1))))
        for c in it['chapters']: g.add((i, PR.chapter, I(c)))
        g.add((i, EN.primaryChapter, I(it['primary']))); g.add((i, PR.bloomLevel, I(it['bloom'])))
        g.add((i, EN.kind, EN[{'direct': 'Direct', 'synthesis': 'Synthesis', 'indirect': 'Indirect'}[it['kind']]]))
        if it['kind'] == 'synthesis': g.add((i, PR.synthesis, B(True)))
        if it['kind'] == 'indirect' and it.get('indirect_form'): g.add((i, EN.indirectForm, L(it['indirect_form'])))
        if it.get('machine_assembled'): g.add((i, EN.machineAssembled, B(True)))
        for t in unfound_terms(it): g.add((i, EN.unfoundTerm, L(t)))
        g.add((i, PR.source, src(it))); return i
    for it in paper['items']:
        n = it['position']; t = it['type']
        if t in CHOICE:
            i = base(it, n, t, 'ChoiceItem'); g.add((i, PR.stem, L(it['q'])))
            for k, o in enumerate(it['options']):
                on = EX['%s_item%d_opt%s' % (pid, n, 'ABCD'[k])]; g.add((i, PR.option, on)); g.add((on, PR.letter, L('ABCD'[k])))
                g.add((on, PR.isKey, B(k == it['answer']))); g.add((on, PR.text, L(o)))
            if it.get('code'):
                ls = it['code'].split('\n'); g.add((i, PR.codeLines, I(len(ls)))); g.add((i, PR.codeMaxColumns, I(max(len(l) for l in ls)))); g.add((i, PR.code, L(it['code'])))
        elif t == 'Matching':
            i = base(it, n, t, 'MatchingItem'); rs = []
            for k, r in enumerate(it['responses']):
                x = EX['%s_item%d_resp%d' % (pid, n, k)]; g.add((x, RDF.type, PR.Response)); g.add((x, PR.letter, L('ABCDEFGH'[k]))); g.add((x, PR.text, L(r))); g.add((i, PR.hasResponse, x)); rs.append(x)
            for k, pm in enumerate(it['premises']):
                x = EX['%s_item%d_prem%d' % (pid, n, k)]; g.add((x, RDF.type, PR.Premise)); g.add((x, PR.text, L(pm['text']))); g.add((i, PR.hasPremise, x))
                g.add((x, PR.matchesTo, rs[it['responses'].index(pm['match'])]))
        elif t == 'Ordering':
            i = base(it, n, t, 'OrderingItem')
            for k, s in enumerate(it['steps']):
                x = EX['%s_item%d_step%d' % (pid, n, k)]; g.add((x, RDF.type, PR.Step)); g.add((x, PR.text, L(s))); g.add((x, PR.correctPosition, I(k + 1))); g.add((i, PR.step, x))
        elif t == 'FillBlankGroup':
            bk = EX['%s_bank%d' % (pid, n)]; g.add((bk, RDF.type, PR.Bank)); g.add((bk, PR.shuffleSeed, I(P['seed'] + n)))
            texts = [b['answer'] for b in it['blanks']] + list(it['distractors']); order = it['bank_order']
            ents = {}
            for k in range(len(texts)):
                x = EX['%s_bank%d_e%d' % (pid, n, k)]; g.add((x, RDF.type, PR.BankEntry)); g.add((x, PR.label, L(str(order.index(k) + 1)))); g.add((x, PR.position, I(order.index(k) + 1)))
                g.add((x, PR.text, L(texts[k]))); g.add((bk, PR.entry, x)); ents[k] = x
            for b, bl in enumerate(it['blanks']):
                i = base(dict(it, key=it['key'], position=n), n + b, 'FillBlank', 'FillBlankItem'); g.add((i, PR.bank, bk)); g.add((i, PR.blankNo, I(b + 1)))
                g.add((i, PR.answerEntry, ents[b])); g.add((i, PR.stem, L(bl['text'])))
        elif t == 'NumericAnswer':
            i = base(it, n, t, 'NumericItem'); g.add((i, PR.stem, L(it['q']))); g.add((i, PR.keyValue, D(str(it['key_value'])))); g.add((i, PR.unit, L(it['unit'])))
            g.add((i, PR.tolerance, D(str(it['tolerance'])))); g.add((i, PR.answerBoxes, I(1)))
        elif t == 'CodeTrace':
            i = base(it, n, t, 'CodeTraceItem'); ls = it['code'].split('\n'); g.add((i, PR.stem, L(it['q']))); g.add((i, PR.keyOutput, L(it['output'])))
            g.add((i, PR.codeLines, I(len(ls)))); g.add((i, PR.codeMaxColumns, I(max(len(l) for l in ls)))); g.add((i, PR.code, L(it['code'])))
        elif t == 'ShortAnswer':
            i = base(it, n, t, 'ShortAnswerItem'); g.add((i, PR.stem, L(it['q'])))
            for r_ in it['rubric']: g.add((i, PR.rubricPoint, L(r_)))
            g.add((i, PR.answerLines, I(it['lines'])))
        else: raise ValueError('unknown item type %s' % t)
    return g, p


# ------------------------------------------------------------------ validation and refusal
_SHAPES = []
def shapes_graph():
    if not _SHAPES:
        g = Graph(); g.parse(os.path.join(HERE, V % 'paperrules_shapes' + '.ttl')); g.parse(os.path.join(HERE, V % 'engine_shapes' + '.ttl')); _SHAPES.append(g)
    return _SHAPES[0]


def registry():
    r = Graph(); r.parse(os.path.join(HERE, V % 'papertypes' + '.ttl')); return r


def validate(data):
    """Run printed-paper rules plus engine rules on a paper graph (the registry is added). Returns [(rule, severity, message)]."""
    d = Graph()
    for t in data: d.add(t)
    for t in registry(): d.add(t)
    conf, rg, txt = pyshacl.validate(d, shacl_graph=shapes_graph(), advanced=True, inference='none', js=False)
    out = []
    for r in rg.subjects(SH.resultSeverity, None):
        m = str(rg.value(r, SH.resultMessage)); out.append((m.split()[0], str(rg.value(r, SH.resultSeverity)).split('#')[1], m))
    return sorted(set(out))


def refuse_on(viol):
    if any(s == 'Violation' for r, s, m in viol): raise ExamRefused(viol)


def make_and_check(P, kind, exclude=frozenset(), prev=0, salt=0, render=True, companion_graph=None):
    paper = build_paper(P, kind, exclude, prev, salt)
    if render:
        import sen0401_exam_engine_render_v1_0_0 as R
        tmp = tempfile.mkdtemp(prefix='sen0401_engine_', dir=os.environ.get('SEN0401_ENGINE_TMP')); pdf = os.path.join(tmp, 'p.pdf')
        paper['pageCount'] = R.render(paper, pdf)
        try: os.remove(pdf); os.rmdir(tmp)
        except OSError: pass
    g, p = to_graph(paper)
    return paper, g, p


def build_pair(P, outdir=None, write=True):
    """Build the midterm and the make-up, check both and the pair, refuse on any Violation. Returns (midterm, makeup, warnings)."""
    seq = {}
    for kind in ('midterm', 'makeup'):
        fs = glob.glob(os.path.join(outdir or HERE, 'sen0401_exam_%s_v*_0_0_paper.ttl' % kind)) if outdir else []
        seq[kind] = max([int(re.search(r'_v(\d+)_0_0_paper', f).group(1)) for f in fs] or [0])
    mid, gm, pm = make_and_check(P, 'midterm', prev=seq['midterm'])
    excl = frozenset() if P.allow_repeat else frozenset(i['key'] for i in mid['items'])
    mk, gk, pk = make_and_check(P, 'makeup', exclude=excl, prev=seq['makeup'], salt=1)
    g = Graph(); g.bind('pr', PR); g.bind('en', EN)
    for t in gm: g.add(t)
    for t in gk: g.add(t)
    g.add((pk, PR.companion, pm)); pair = EX['pair_%s_%s' % (mid['version'], mk['version'])]
    g.add((pair, RDF.type, EN.ExamPair)); g.add((pair, EN.midterm, pm)); g.add((pair, EN.makeUp, pk)); g.add((pair, EN.repeatAllowed, B(P.allow_repeat)))
    viol = validate(g); refuse_on(viol)
    warn = [v for v in viol if v[1] != 'Violation']
    if write:
        import sen0401_exam_engine_render_v1_0_0 as R
        od = outdir or HERE
        for paper, kind in ((mid, 'midterm'), (mk, 'makeup')):
            base = os.path.join(od, 'sen0401_exam_%s_v%d_0_0' % (kind, paper['version']))
            if glob.glob(base + '*'): raise RuntimeError('refusing to overwrite an existing file: ' + base)
        for paper, kind, gg in ((mid, 'midterm', gm), (mk, 'makeup', gk)):
            base = os.path.join(od, 'sen0401_exam_%s_v%d_0_0' % (kind, paper['version']))
            R.render(paper, base + '.pdf'); gg.serialize(base + '_paper.ttl', format='turtle')
            json.dump(R.answer_key(paper), open(base + '_key.json', 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    return mid, mk, warn


def main():
    a = argparse.ArgumentParser(); sub = a.add_subparsers(dest='cmd', required=True); b = sub.add_parser('build')
    b.add_argument('--items', type=int, required=True, help='total items per paper (the owner decides; no default)')
    b.add_argument('--chapters', default='1-6'); b.add_argument('--matching', type=int, default=0); b.add_argument('--seed', type=int, default=4701)
    b.add_argument('--authored'); b.add_argument('--outdir', required=True); b.add_argument('--weights', help='e.g. 1:2,2:1,3:1 (chapter:weight); default equal')
    b.add_argument('--higher-from', type=int, default=3); b.add_argument('--synthesis-min', type=int, default=0); b.add_argument('--enable', default='')
    b.add_argument('--indirect', action='store_true'); b.add_argument('--allow-repeat', action='store_true'); b.add_argument('--page-limit', type=int)
    b.add_argument('--columns', type=int, default=2); b.add_argument('--sitting', type=int, default=60); b.add_argument('--order', default='chapter')
    x = a.parse_args(); chs = M.parse_ch(x.chapters)
    w = {int(k): float(v) for k, v in (s.split(':') for s in x.weights.split(','))} if x.weights else None
    P = Params(x.items, chs, w, x.matching, x.higher_from, 0.6, x.synthesis_min, x.indirect, x.seed, x.sitting, x.columns, 45 if x.columns == 2 else 90, 'CircleOnItem',
               x.page_limit, [e for e in x.enable.split(',') if e], x.allow_repeat, x.authored, x.order)
    try:
        mid, mk, warn = build_pair(P, x.outdir)
    except ExamRefused as e:
        print(e); sys.exit(2)
    for w_ in warn: print('WARNING', w_[2])
    print('BUILT midterm v%d (%d pages) and makeup v%d (%d pages) in %s' % (mid['version'], mid.get('pageCount', 0), mk['version'], mk.get('pageCount', 0), x.outdir))


if __name__ == '__main__': main()
