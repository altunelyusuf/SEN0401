"""SEN0401 general exam engine, version 1.1.0 (new file; v1.0.0 and its shapes, fixtures and check stay as committed).

WHAT CHANGED against v1.0.0, and why
  The owner's ruling of 2026-10-30: the questions of the interactive pages are open to students before the exam; they are chapter specific; they must not be used directly, but they can
  seed better questions. So:
  1. PAPERS ARE BUILT FROM AUTHORED ITEMS ONLY. v1.0.0 pooled the chapter banks (bank_pool) and composed matching items from bank items (compose_matching). Neither exists here: this file
     never reads a question bank to put an item on a paper. --authored FILE is REQUIRED. Every item type of the paper rules (choice, matching, ordering, fill-in bank, number, trace) is an
     authored item. Authored-items format of v1.0.0 (see sen0401_exam_engine_v1_0_0.py) plus three fields:
        "seeds": ["ch02/question_bank_v1_0_0.json#17", ...]   page items the item was made from (links; they must resolve to page-visible items)
        "no_seed_reason": "..."                              only when the item has no seed
        "critical_points": ["CP2.05", ...]                   critical points of sen0401_exam_critical_points_v1_0_0.json that the item tests (at least one; they must resolve)
        "papers": ["midterm"|"makeup", ...]                   optional: which paper(s) the item may enter (default both)
  2. RULE EN11 (SHACL, sen0401_exam_engine_shapes_v1_1_0.ttl): a paper is REFUSED (ExamRefused, exit code 2, nothing written) when an item's stem or option set matches a page-visible item.
     The method and its thresholds are stated in sen0401_exam_similarity_v1_1_0.py. The exact tests also run in SHACL against the page-visible items loaded into the data graph.
  3. RULES EN12 (seed and critical-point links resolve) and EN13 (bank of at most 9 entries when the answer mode is the grid).
  4. ANSWER MODE: GridOnCover by default (the owner's decision: a separate bubble grid, one extra A4 page). The sheet is produced from the paper and its pages are COUNTED in the page count.
  5. The output folder is created when it is missing (v1.0.0 required it to exist: a defect the control found).
Everything else is kept: EN01-EN10 and R01-R22 run on every paper, the chapter list is a parameter (default 1-6, chapter 7 selectable), versions increment, the make-up never reuses a midterm item
(EN05), 24 items is the owner's decision and is a REQUIRED --items parameter, answer letters are evenly distributed, fill-in banks are randomised, higher Bloom levels are a majority.
Usage: engine.py build --items N --authored FILE --outdir DIR [--chapters 1-6] [--seed S] [--weights 1:2,2:1] [--answer-mode GridOnCover|CircleOnItem] [options]
"""
import argparse, glob, json, math, os, random, re, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
from rdflib import Graph, Namespace, Literal, RDF, URIRef, XSD
import pyshacl
import sen0401_exam_engine_v1_0_0 as E0          # imported unchanged: parameters, helpers, term index, ExamRefused. Its bank_pool and compose_matching are never called.
import sen0401_exam_similarity_v1_1_0 as S
import sen0401_exam_engine_render_v1_1_0 as R
import sen0401_exam_pagesave_measure_v1_0_0 as M
from sen0401_exam_engine_v1_0_0 import ExamRefused, quotas, balance_letters, order_of_steps, L, I, B, D, SH, PR, EN, EX
VERSION = '1.1.0'
CHOICE = ('ChoiceFour', 'ChoiceFourCode')
PG = Namespace('http://example.org/sen0401/engine/page#')
CPN = Namespace('http://example.org/sen0401/engine/criticalpoint#')
CP_FILE = os.path.join(HERE, 'sen0401_exam_critical_points_v1_0_0.json')


def rel(p): return os.path.relpath(p, ROOT)
def units(i): return len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1


class Params(E0.Params):
    def __init__(self, items, chapters=(1, 2, 3, 4, 5, 6), weights=None, answer_mode='GridOnCover', **kw):
        kw.setdefault('matching', 0)
        super().__init__(items, chapters, weights, answer_mode=answer_mode, **kw)


# ------------------------------------------------------------------ the page-visible set and the critical points (read only)
_PAGES = {}
def pages_for(chapters):
    key = tuple(sorted(set(S.DEFAULT_PAGE_CHAPTERS) | set(chapters)))
    if key not in _PAGES: _PAGES[key] = S.page_items(key)
    return _PAGES[key], key


def cp_index():
    d = json.load(open(CP_FILE, encoding='utf8'))
    return {p['id']: p for p in d['list_A_points_carried_by_a_source']}


def _uri(ref): return PG[re.sub(r'[^A-Za-z0-9]+', '_', ref)]


def context_graph(pages):
    """Nodes that make the page-visible items and the critical points visible to SHACL (validation context only; never written into a paper file)."""
    g = Graph()
    for pg in pages:
        n = _uri(pg['ref']); p = pg['p']
        g.add((n, RDF.type, EN.PageItem)); g.add((n, EN.pageRef, L(pg['ref']))); g.add((n, EN.pageChapter, I(pg['chapter'])))
        if p['sq']: g.add((n, EN.normStem, L(p['sq'])))
        if len(p['dist']) >= S.OPTIONS_MIN_DISTINCTIVE_FOR_EXACT: g.add((n, EN.optionSetKey, L('|'.join(sorted(p['opts'])))))
    for pid, pt in cp_index().items():
        n = CPN[pid]; g.add((n, RDF.type, EN.CriticalPoint)); g.add((n, EN.pointChapter, I(pt['chapter'])))
    return g


# ------------------------------------------------------------------ authored items
def load_authored(path, chapters):
    if not path: raise ExamRefused([('EN11', 'Violation', 'EN11 no authored items file was given: papers are built from authored items only')])
    raw = json.load(open(path, encoding='utf8'))['items']; out = []; skipped = []; seen = set()
    need = ('key', 'type', 'chapters', 'bloom', 'source')
    for r in raw:
        miss = [k for k in need if k not in r]
        if miss: raise ExamRefused([('INPUT', 'Violation', 'INPUT authored item %s lacks %s' % (r.get('key', '?'), ', '.join(miss)))])
        if r['key'] in seen: raise ExamRefused([('EN06', 'Violation', 'EN06 the authored items file holds the key %s twice' % r['key'])])
        seen.add(r['key'])
        ch = list(r['chapters'])
        if not set(ch) <= set(chapters): skipped.append((r['key'], 'chapters %s not all in the chapter list' % ch)); continue
        it = dict(r); it['primary'] = ch[0]; it.setdefault('kind', 'direct'); it.setdefault('papers', ['midterm', 'makeup']); it.setdefault('terms', [])
        it.setdefault('seeds', []); it.setdefault('critical_points', [])
        # an item that is not an authored item: its key or source names a question bank or a page quiz
        pagey = str(it['key']).startswith('bank:') or 'question_bank' in str(it['source'].get('file', '')) or re.search(r'quiz_v\d', str(it['source'].get('file', '')))
        it['origin'] = 'PageBank' if pagey else 'Authored'
        out.append(it)
    return out, skipped


def check_copies(item, pages):
    """Run the similarity method on every component of an item. Returns [(component label, page ref, kinds, stem share, option share)]."""
    hits = []
    for label, stem, opts in S.components(item):
        c = S.prepare(stem, opts)
        for ref, kinds, ss, os_ in S.find_matches(c, pages): hits.append((label, ref, kinds, ss, os_))
    return hits


# ------------------------------------------------------------------ selection
def select(P, kind, pool, rnd):
    """Pick, for each chapter, authored items whose units add up to the chapter quota; prefer a higher-order share. Items may be tagged with the paper(s) they may enter."""
    q = quotas(P.chapters, P.weights, P.items); picks = []
    for c in P.chapters:
        cand = [i for i in pool if i['primary'] == c]; k = q[c]; take = []
        for _ in range(400):
            hi = [i for i in cand if i['bloom'] >= P.higher_from]; lo = [i for i in cand if i['bloom'] < P.higher_from]; rnd.shuffle(hi); rnd.shuffle(lo)
            want = int(math.ceil(P.higher_share * k)); take = []; tot = 0; hit = 0
            for i in hi:
                if hit + units(i) <= want and tot + units(i) <= k: take.append(i); tot += units(i); hit += units(i)
            for i in lo:
                if tot + units(i) <= k: take.append(i); tot += units(i)
            for i in hi:
                if i not in take and tot + units(i) <= k: take.append(i); tot += units(i)
            if tot == k: break
        if tot != k:                  # the greedy pass could not hit the quota exactly (multi-unit items): exact search over a shuffled order
            order = cand[:]; rnd.shuffle(order); order.sort(key=lambda i: 0 if i['bloom'] >= P.higher_from else 1)
            def dfs(idx, tot_, chosen):
                if tot_ == k: return chosen
                for j in range(idx, len(order)):
                    u = units(order[j])
                    if tot_ + u <= k:
                        r = dfs(j + 1, tot_ + u, chosen + [order[j]])
                        if r is not None: return r
                return None
            found = dfs(0, 0, [])
            if found is not None: take = found
        picks += take
    return picks, q


def build_paper(P, kind, exclude=frozenset(), prev_seq=0, rnd_salt=0):
    rnd = random.Random(P.seed * 7 + rnd_salt)
    auth, skipped = load_authored(P.authored, P.chapters)
    pages, pkey = pages_for(P.chapters)
    pool = [i for i in auth if kind in i['papers'] and i['key'] not in exclude]
    picks, q = select(P, kind, pool, rnd)
    tot = lambda L_: sum(units(i) for i in L_); hi_n = lambda L_: sum(units(i) for i in L_ if i['bloom'] >= P.higher_from)
    guard = 0
    while hi_n(picks) * 2 <= tot(picks) and guard < 200:      # top up towards a higher-order majority
        guard += 1; swap = None
        for lo_ in [i for i in picks if i['bloom'] < P.higher_from]:
            alt = [i for i in pool if i['primary'] == lo_['primary'] and i['bloom'] >= P.higher_from and i not in picks and units(i) == units(lo_)]
            if alt: swap = (lo_, rnd.choice(alt)); break
        if not swap: break
        picks[picks.index(swap[0])] = swap[1]
    allit = [dict(i) for i in picks]
    for i in allit:
        i['matches'] = check_copies(i, pages); i['checked_against'] = len(pages)
    if P.order == 'mixed': rnd.shuffle(allit)
    else: allit.sort(key=lambda i: (i['primary'], rnd.random()))
    balance_letters([i for i in allit if i['type'] in CHOICE], rnd)
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
        if i['type'] == 'Matching':       # the author's order of responses is not kept: the letters of the keys are spread by a seeded shuffle
            i['responses'] = list(i['responses']); random.Random(P.seed * 17 + i['position']).shuffle(i['responses'])
    return dict(kind=kind, version=prev_seq + 1, previous=prev_seq, chapters=list(P.chapters), quotas=q, params=P.snapshot(), items=allit, pool_size=len(pool),
                skipped=skipped, page_chapters=list(pkey), page_items=len(pages))


# ------------------------------------------------------------------ graph
def to_graph(paper, g=None, pid=None):
    """Paper dict -> RDF: the vocabulary of the printed-paper rules and of the engine rules, plus the EN11-EN13 facts."""
    return _base_graph(paper, g, pid)


def _base_graph(paper, g, pid):
    """Copy of the v1.0.0 paper-to-RDF mapping with the v1.1.0 additions (item links, copy-check facts, bank labels as grid codes, page counts)."""
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
    if paper.get('contentPages'): g.add((p, EN.contentPages, I(paper['contentPages'])))
    if paper.get('sheetPages') is not None: g.add((p, EN.sheetPages, I(paper['sheetPages'])))
    g.add((p, EN.engineVersion, L(VERSION))); g.add((p, EN.similarityVersion, L(S.VERSION))); g.add((p, EN.pageVisibleItems, I(paper['page_items'])))
    for c in paper['page_chapters']: g.add((p, EN.requiredPageChapter, I(c)))
    for c in paper['chapters']:
        g.add((p, PR.chapterList, I(c)))
        qn = EX['%s_quota%d' % (pid, c)]; g.add((p, EN.chapterQuota, qn)); g.add((qn, EN.quotaChapter, I(c))); g.add((qn, EN.quotaItems, I(paper['quotas'][c])))
    g.add((p, EN.higherFrom, I(P['higher_from']))); g.add((p, EN.synthesisMin, I(P['synthesis_min']))); g.add((p, EN.indirectEnabled, B(P['indirect_enabled'])))
    for t in P['enable']: g.add((p, PR.enables, PR[t]))
    srcn = [0]; matchn = [0]
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
        for t in E0.unfound_terms(it): g.add((i, EN.unfoundTerm, L(t)))
        g.add((i, PR.source, src(it)))
        # v1.1.0: origin, copy check, normalised texts for the exact tests in SHACL, links to critical points and seeds
        g.add((i, EN.origin, EN[it['origin']])); g.add((i, EN.copyChecked, B(it.get('checked_against', 0) > 0)))
        for label, stem, opts in S.components(it):
            c = S.prepare(stem, opts)
            if c['sq']: g.add((i, EN.normStem, L(c['sq'])))
            if len(c['dist']) >= S.OPTIONS_MIN_DISTINCTIVE_FOR_EXACT: g.add((i, EN.optionSetKey, L('|'.join(sorted(c['opts'])))))
        for label, ref, kinds, ss, os_ in it.get('matches', []):
            matchn[0] += 1; m = EX['%s_match%d' % (pid, matchn[0])]
            g.add((i, EN.pageMatch, m)); g.add((m, EN.matchedPageItem, _uri(ref))); g.add((m, EN.matchComponent, L(label))); g.add((m, EN.matchKinds, L(' '.join(kinds))))
            g.add((m, EN.stemShare, D(str(ss)))); g.add((m, EN.optionShare, D(str(os_))))
        for cp in it.get('critical_points', []): g.add((i, EN.tests, CPN[cp]))
        for sd in it.get('seeds', []): g.add((i, EN.seedItem, _uri(sd)))
        if it.get('no_seed_reason'): g.add((i, EN.noSeedReason, L(it['no_seed_reason'])))
        return i
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
            texts = [b['answer'] for b in it['blanks']] + list(it['distractors']); order = it['bank_order']; ents = {}
            for k in range(len(texts)):
                x = EX['%s_bank%d_e%d' % (pid, n, k)]; g.add((x, RDF.type, PR.BankEntry)); g.add((x, PR.label, L(R.bank_label(paper, order.index(k) + 1)))); g.add((x, PR.position, I(order.index(k) + 1)))
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
        g = Graph()
        for f in ('sen0401_exam_paperrules_shapes_v1_0_0.ttl', 'sen0401_exam_engine_shapes_v1_0_0.ttl', 'sen0401_exam_engine_shapes_v1_1_0.ttl'): g.parse(os.path.join(HERE, f))
        _SHAPES.append(g)
    return _SHAPES[0]


def validate(data, chapters=S.DEFAULT_PAGE_CHAPTERS):
    """Run the printed-paper rules, the engine rules EN01-EN10 and the rules EN11-EN13 on a paper graph. The registry, the page-visible items and the critical points are added as context."""
    d = Graph()
    for t in data: d.add(t)
    for t in E0.registry(): d.add(t)
    pages, _ = pages_for(chapters)
    for t in context_graph(pages): d.add(t)
    conf, rg, txt = pyshacl.validate(d, shacl_graph=shapes_graph(), advanced=True, inference='none', js=False)
    out = []
    for r in rg.subjects(SH.resultSeverity, None):
        m = str(rg.value(r, SH.resultMessage)); out.append((m.split()[0], str(rg.value(r, SH.resultSeverity)).split('#')[1], m))
    return sorted(set(out))


def refuse_on(viol):
    if any(s == 'Violation' for r, s, m in viol): raise ExamRefused(viol)


def make_and_check(P, kind, exclude=frozenset(), prev=0, salt=0, render=True):
    paper = build_paper(P, kind, exclude, prev, salt)
    if render:
        tmp = tempfile.mkdtemp(prefix='sen0401_engine_', dir=os.environ.get('SEN0401_ENGINE_TMP')); pdf = os.path.join(tmp, 'p.pdf'); sh = os.path.join(tmp, 's.pdf')
        paper['contentPages'] = R.render(paper, pdf)
        paper['sheetPages'] = R.render_sheet(paper, sh)[0] if P.answer_mode == R.GRID else 0
        paper['pageCount'] = paper['contentPages'] + paper['sheetPages']
        for f in (pdf, sh):
            try: os.remove(f)
            except OSError: pass
        try: os.rmdir(tmp)
        except OSError: pass
    g, p = to_graph(paper)
    return paper, g, p


def build_pair(P, outdir=None, write=True):
    """Build the midterm and the make-up, check both and the pair, refuse on any Violation (nothing is written). Returns (midterm, makeup, warnings)."""
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
    viol = validate(g, P.chapters); refuse_on(viol)
    warn = [v for v in viol if v[1] != 'Violation']
    if write:
        od = outdir or HERE
        os.makedirs(od, exist_ok=True)                                  # v1.1.0: the folder is created when it is missing
        for paper, kind in ((mid, 'midterm'), (mk, 'makeup')):
            base = os.path.join(od, 'sen0401_exam_%s_v%d_0_0' % (kind, paper['version']))
            if glob.glob(base + '*'): raise RuntimeError('refusing to overwrite an existing file: ' + base)
        for paper, kind, gg in ((mid, 'midterm', gm), (mk, 'makeup', gk)):
            base = os.path.join(od, 'sen0401_exam_%s_v%d_0_0' % (kind, paper['version']))
            R.render(paper, base + '.pdf'); gg.serialize(base + '_paper.ttl', format='turtle')
            if P.answer_mode == R.GRID:
                n, layout = R.render_sheet(paper, base + '_sheet.pdf'); json.dump(layout, open(base + '_sheet_layout.json', 'w'), indent=1)
            json.dump(R.answer_key(paper), open(base + '_key.json', 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    return mid, mk, warn


def main():
    a = argparse.ArgumentParser(); sub = a.add_subparsers(dest='cmd', required=True); b = sub.add_parser('build')
    b.add_argument('--items', type=int, required=True, help='total items per paper (the owner decides; no default)')
    b.add_argument('--chapters', default='1-6'); b.add_argument('--seed', type=int, default=4701)
    b.add_argument('--authored', help='authored items file (required: papers are built from authored items only)'); b.add_argument('--outdir', required=True)
    b.add_argument('--weights', help='e.g. 1:2,2:1,3:1 (chapter:weight); default equal')
    b.add_argument('--higher-from', type=int, default=3); b.add_argument('--synthesis-min', type=int, default=0); b.add_argument('--enable', default='')
    b.add_argument('--indirect', action='store_true'); b.add_argument('--allow-repeat', action='store_true'); b.add_argument('--page-limit', type=int)
    b.add_argument('--columns', type=int, default=2); b.add_argument('--sitting', type=int, default=60); b.add_argument('--order', default='chapter')
    b.add_argument('--answer-mode', default='GridOnCover', choices=['GridOnCover', 'CircleOnItem'])
    x = a.parse_args(); chs = M.parse_ch(x.chapters)
    w = {int(k): float(v) for k, v in (s.split(':') for s in x.weights.split(','))} if x.weights else None
    P = Params(x.items, chs, w, x.answer_mode, synthesis_min=x.synthesis_min, higher_from=x.higher_from, indirect_enabled=x.indirect, seed=x.seed, sitting=x.sitting, columns=x.columns,
               code_cap=45 if x.columns == 2 else 90, page_limit=x.page_limit, enable=[e for e in x.enable.split(',') if e], allow_repeat=x.allow_repeat, authored=x.authored, order=x.order)
    try:
        mid, mk, warn = build_pair(P, x.outdir)
    except ExamRefused as e:
        print(e); sys.exit(2)
    for w_ in warn: print('WARNING', w_[2])
    print('BUILT midterm v%d (%d pages with the sheet) and makeup v%d (%d pages with the sheet) in %s' % (mid['version'], mid.get('pageCount', 0), mk['version'], mk.get('pageCount', 0), x.outdir))


if __name__ == '__main__': main()
