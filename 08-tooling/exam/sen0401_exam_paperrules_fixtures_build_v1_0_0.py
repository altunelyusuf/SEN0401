"""Builds the fixtures of known answer for the printed-paper rules, version 1.0.0.
Writes sen0401_exam_paperrules_fixtures_v1_0_0.ttl and sen0401_exam_paperrules_fixtures_expected_v1_0_0.json.
Every fixture is a synthetic paper (no student data). P01 and P02 must conform; each N-fixture breaks exactly the rules listed as its expected answer.
P03 is built from the real chapter banks (read only) so the rules are also tried on real item texts."""
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rdflib import Graph, Namespace, Literal, RDF, URIRef, XSD
import sen0401_exam_pagesave_measure_v1_0_0 as M
PR = Namespace('http://example.org/sen0401/paperrules#'); FX = Namespace('http://example.org/sen0401/paperrules/fixture#')
HERE = os.path.dirname(os.path.abspath(__file__))
g = Graph(); g.bind('pr', PR); g.bind('fx', FX)
expected = {}
L = lambda v: Literal(v)
I = lambda v: Literal(v, datatype=XSD.integer)
B = lambda v: Literal(v, datatype=XSD.boolean)
D = lambda v: Literal(v, datatype=XSD.decimal)

def src(fid, n):
    s = FX['%s_src%d' % (fid, n)]
    g.add((s, RDF.type, PR.CorpusSource)); g.add((s, PR.file, L('FIXTURE source file'))); g.add((s, PR.locator, L('slide %d' % n)))
    return s

def paper(fid, kind='Midterm', chapters=(1, 2, 3, 4, 5, 6), ver=2, prev=1, **o):
    p = FX[fid + '_paper']
    g.add((p, RDF.type, PR.Paper)); g.add((p, PR.paperKind, PR[kind]))
    d = dict(theme='light', background='white', ink='black', fillColourUsed=False, containsPersonalData=False, fontPt=10, codeFontPt=9, sittingMinutes=60,
             columns=2, codeColumnCapacity=45, answerMode=PR.CircleOnItem)
    d.update(o)
    for c in chapters: g.add((p, PR.chapterList, I(c)))
    g.add((p, PR.versionSeq, I(ver))); g.add((p, PR.previousVersionSeq, I(prev)))
    for k, v in d.items():
        if v is None: continue
        val = v if isinstance(v, URIRef) else (B(v) if isinstance(v, bool) else I(v) if isinstance(v, int) else L(v))
        g.add((p, PR[k], val))
    return p

def item(fid, p, n, typ, cls, bloom, chapter=1, key='A', letters=None, source=True, synth=False, **o):
    i = FX['%s_item%d' % (fid, n)]
    g.add((p, PR.hasItem, i)); g.add((i, RDF.type, PR.Item))
    if cls: g.add((i, RDF.type, PR[cls]))
    g.add((i, PR.itemType, PR[typ])); g.add((i, PR.position, I(n))); g.add((i, PR.itemKey, L('%s-k%d' % (o.get('keyprefix', fid), n))))
    for c in (chapter if isinstance(chapter, (list, tuple)) else [chapter]): g.add((i, PR.chapter, I(c)))
    g.add((i, PR.bloomLevel, I(bloom)))
    if source: g.add((i, PR.source, src(fid, n)))
    if synth: g.add((i, PR.synthesis, B(True)))
    return i

def options(fid, i, key, texts=None, n=4, keys=1, letters='ABCD'):
    texts = texts or ['FIXTURE option %s of item %s' % (c, i.split('_')[-1]) for c in letters]
    g.add((i, PR.stem, L('FIXTURE stem of ' + i.split('_')[-1])))
    for a, c in enumerate(letters[:n]):
        o = FX['%s_opt_%s' % (i.split('#')[1], c)]
        g.add((i, PR.option, o)); g.add((o, PR.letter, L(c))); g.add((o, PR.isKey, B(c == key or (keys == 2 and c == 'B' and key != 'B')))); g.add((o, PR.text, L(texts[a])))

KEYS = 'ABCDDCBAB'  # nine choice items: A2 B3 C2 D2? computed below to stay even
def base(fid, kind='Midterm', mut=None, **po):
    """16 items: 9 choice (one with code), matching, ordering, 3 blanks, numeric, trace."""
    mut = mut or {}
    p = paper(fid, kind, **po)
    keys = mut.get('keys', 'ABCDDCBAC')   # A2 B2 C3 D2: even
    blooms = mut.get('blooms', [3, 4, 3, 4, 3, 2, 2, 1, 3])
    n = 0
    for k in range(9):
        n += 1; code = (k == 8)
        i = item(fid, p, n, 'ChoiceFourCode' if code else 'ChoiceFour', 'ChoiceItem', blooms[k], chapter=(k % 6) + 1, key=keys[k])
        options(fid, i, keys[k], texts=mut.get('optiontexts', {}).get(k), n=mut.get('nopts', {}).get(k, 4), keys=mut.get('nkeys', {}).get(k, 1), letters=mut.get('letters', {}).get(k, 'ABCD'))
        if code:
            g.add((i, PR.codeLines, I(mut.get('codelines', 6)))); g.add((i, PR.codeMaxColumns, I(mut.get('codecols', 38))))
    n += 1  # matching
    m = item(fid, p, n, 'Matching', 'MatchingItem', 2, chapter=[1, 4], synth=True)
    npre = mut.get('npremise', 4); nresp = mut.get('nresp', 6)
    resp = []
    for r in range(nresp):
        x = FX['%s_resp%d' % (fid, r)]; g.add((x, RDF.type, PR.Response)); g.add((x, PR.letter, L('ABCDEFGH'[r]))); g.add((x, PR.text, L('FIXTURE response %d' % r))); g.add((m, PR.hasResponse, x)); resp.append(x)
    for q in range(npre):
        x = FX['%s_prem%d' % (fid, q)]; g.add((x, RDF.type, PR.Premise)); g.add((x, PR.text, L('FIXTURE premise %d' % q))); g.add((m, PR.hasPremise, x))
        g.add((x, PR.matchesTo, resp[mut.get('dupkey', {}).get(q, q)]))
    n += 1  # ordering
    o = item(fid, p, n, 'Ordering', 'OrderingItem', 3, chapter=2)
    pos = mut.get('steps', [1, 2, 3, 4])
    for s, cp in enumerate(pos):
        x = FX['%s_step%d' % (fid, s)]; g.add((x, RDF.type, PR.Step)); g.add((x, PR.text, L('FIXTURE step %d' % s))); g.add((x, PR.correctPosition, I(cp))); g.add((o, PR.step, x))
    bank = FX[fid + '_bank']; g.add((bank, RDF.type, PR.Bank))
    if not mut.get('noseed'): g.add((bank, PR.shuffleSeed, I(4701)))
    labels = mut.get('labels', ['1', '2', '3', '4', '5']); bpos = mut.get('bankpos', [4, 1, 3, 5, 2]); nent = mut.get('nentries', 5)
    ents = []
    for e in range(nent):
        x = FX['%s_entry%d' % (fid, e)]; g.add((x, RDF.type, PR.BankEntry)); g.add((x, PR.label, L(labels[e]))); g.add((x, PR.position, I(bpos[e]))); g.add((x, PR.text, L('FIXTURE entry %d' % e))); g.add((bank, PR.entry, x)); ents.append(x)
    for b in range(3):
        n += 1
        f = item(fid, p, n, 'FillBlank', 'FillBlankItem', 1 if b < 2 else 2, chapter=3)
        g.add((f, PR.bank, bank)); g.add((f, PR.blankNo, I(b + 1))); g.add((f, PR.answerEntry, ents[mut.get('answers', [0, 1, 2])[b]]))
    n += 1
    u = item(fid, p, n, 'NumericAnswer', 'NumericItem', 3, chapter=1)
    g.add((u, PR.keyValue, D('50'))); g.add((u, PR.tolerance, D('0'))); g.add((u, PR.answerBoxes, I(1)))
    if not mut.get('nounit'): g.add((u, PR.unit, L('FIXTURE unit')))
    n += 1
    t = item(fid, p, n, 'CodeTrace', 'CodeTraceItem', 4, chapter=5)
    g.add((t, PR.keyOutput, L('FIXTURE output'))); g.add((t, PR.codeLines, I(5))); g.add((t, PR.codeMaxColumns, I(30)))
    return p

def fx_(fid, ans, **kw):
    expected[fid] = ans; return base(fid, **kw)

# ---------------- positives
fx_('P01', [])
p2 = fx_('P02', [], kind='MakeUp', mut={'keys': 'BADCCDBAD'}, ver=3, prev=2)   # make-up of P01 below (same chapters, different item keys)
midterm = FX['P01_paper']
# the make-up needs a companion: point it at its own midterm P02m (a separate paper with keys different from the make-up)
pm = fx_('P02m', [], kind='Midterm', ver=3, prev=2)
for i in list(g.objects(pm, PR.hasItem)): g.set((i, PR.itemKey, L('mid-' + str(i).split('item')[-1])))
g.add((p2, PR.companion, pm))
for i in list(g.objects(p2, PR.hasItem)): g.set((i, PR.itemKey, L('mk-' + str(i).split('item')[-1])))
# P03: real bank items, thirty choice items
chs = [1, 2, 3, 4, 5, 6]; items, _ = M.sample(chs, 30)
p3 = paper('P03', chapters=chs, ver=2, prev=1); expected['P03'] = []
for n, it in enumerate(items, 1):
    code = bool(it.get('code'))
    i = item('P03', p3, n, 'ChoiceFourCode' if code else 'ChoiceFour', 'ChoiceItem', {'Remember': 1, 'Understand': 2, 'Apply': 3, 'Analyze': 4}[it['level']], chapter=it['chapter'])
    g.add((i, PR.stem, L(it['q'])))
    for a, c in enumerate('ABCD'):
        o = FX['P03_item%d_opt_%s' % (n, c)]; g.add((i, PR.option, o)); g.add((o, PR.letter, L(c))); g.add((o, PR.isKey, B(a == it['answer']))); g.add((o, PR.text, L(it['options'][a])))
    if code: g.add((i, PR.codeLines, I(len(it['code'].split('\n'))))); g.add((i, PR.codeMaxColumns, I(max(len(l) for l in it['code'].split('\n')))))
    s = FX['P03_src%d' % n]; g.remove((i, PR.source, None)); g.add((i, PR.source, s)); g.remove((s, None, None))
    g.add((s, RDF.type, PR.CorpusSource)); g.add((s, PR.file, L('08-tooling/ch%02d-page/question_bank (concept %s)' % (it['chapter'], it['concept'])))); g.add((s, PR.locator, L('bank item')))
# ---------------- negatives: (id, expected rule ids with severity, mutation)
def neg(fid, ans, **kw):
    fx_(fid, ans, **kw)
V, W = 'Violation', 'Warning'
neg('N01', [('R01', V)], theme='dark')
neg('N02', [('R01', V)], background='yellow')
neg('N03', [('R01', V)], fillColourUsed=True)
neg('N04', [('R01', V)], containsPersonalData=True)
neg('N05', [('R01', V)], fontPt=9)
neg('N06', [('R02', V)], chapters=(1, 2, 3, 4, 5, 6, 8))
neg('N07', [('R03', V)], ver=3, prev=1)
neg('N08', [('R05', V)], sittingMinutes=20)
# not-suited type: a TrueFalse item added to the base
def extra_item(fid, ans, typ, cls=None, bloom=2, chapter=1, enable=False, **kw):
    p = fx_(fid, ans, **kw)
    i = item(fid, p, 99, typ, cls, bloom, chapter=chapter)
    if enable: g.add((p, PR.enables, PR[typ]))
    return p, i
extra_item('N09', [('R04', V)], 'TrueFalse')
extra_item('N10', [('R04', V)], 'ShortAnswer', 'ShortAnswerItem', bloom=4)   # conditional, not enabled (rubric present below)
g.add((FX['N10_item99'], PR.rubricPoint, L('FIXTURE point'))); g.add((FX['N10_item99'], PR.answerLines, I(2)))
p, i = extra_item('N10b', [], 'ShortAnswer', 'ShortAnswerItem', bloom=4, enable=True)   # enabled: conforms
g.add((i, PR.rubricPoint, L('FIXTURE point'))); g.add((i, PR.answerLines, I(2)))
p, i = extra_item('N11', [('R21', V)], 'ShortAnswer', 'ShortAnswerItem', bloom=4, enable=True)
for k in range(5): g.add((i, PR.rubricPoint, L('FIXTURE point %d' % k)))
g.add((i, PR.answerLines, I(2)))
neg('N12', [('R08', V)])
g.remove((FX['N12_item1'], PR.source, None))
neg('N13', [('R02', V)], chapters=(1, 2, 3, 4, 5))      # item 6 names chapter 6, not in the list
neg('N14', [('R09', V)])
g.remove((FX['N14_item10'], PR.chapter, I(4)))           # synthesis item left with one chapter
neg('N15', [('R06', V)], mut={'blooms': [1, 2, 1, 2, 1, 2, 2, 1, 3]})
neg('N16', [('R07', V), ('R07', W)], mut={'keys': 'AAAAABCDA'})       # uneven and a run of five (a run of four is a warning)
neg('N18', [('R11', V)], mut={'nopts': {2: 3}, 'letters': {2: 'ABC'}})   # three options in one item
neg('N19', [('R11', V)], mut={'nkeys': {0: 2}})          # two keys
neg('N20', [('R11', V)], mut={'optiontexts': {3: ['FIXTURE a', 'FIXTURE b', 'All of the above', 'FIXTURE d']}})
neg('N21', [('R10', V)], mut={'codecols': 70})
neg('N22', [('R10', V)], mut={'codelines': 20})
neg('N23', [('R13', V)], mut={'nentries': 3, 'labels': ['1', '2', '3'], 'bankpos': [3, 1, 2]})   # bank has 3 entries for 3 blanks
neg('N24', [('R13', V)], mut={'bankpos': [1, 2, 3, 4, 5]})   # bank order follows blank order
neg('N25', [('R14', V)], mut={'labels': ['a', '2', '3', '4', '5']})
neg('N26', [('R13', V)], mut={'noseed': True})
neg('N27', [('R15', V)], mut={'nresp': 5})              # four premises, five responses
neg('N28', [('R15', V)], mut={'dupkey': {1: 0}})        # premise 1 shares the key of premise 0
neg('N29', [('R16', V)], mut={'steps': [1, 2]})   # two steps only
neg('N30', [('R16', V)], mut={'steps': [1, 2, 2, 4]})
neg('N31', [('R19', V)], mut={'nounit': True})
neg('N32', [('R17', V)], pageCount=9, pageLimit=6)
neg('N33', [('R10', V)], columns=2, codeColumnCapacity=60)
neg('N34', [('R16', V)], answerMode=PR.OnSeparateSheetOnly)
p = fx_('N35', [('R01', V)]); g.add((p, PR.studentName, L('SYNTHETIC STAND-IN')))
p = fx_('N36', [('R22', V)]); f = FX['N36_fig']; g.add((p, PR.hasFigure, f)); g.add((f, RDF.type, PR.Figure)); g.add((f, PR.lineArt, B(False))); g.add((f, PR.fillColourUsed, B(False))); g.add((f, PR.source, src('N36', 50)))
p = fx_('P04', []); f = FX['P04_fig']; g.add((p, PR.hasFigure, f)); g.add((f, RDF.type, PR.Figure)); g.add((f, PR.lineArt, B(True))); g.add((f, PR.fillColourUsed, B(False))); g.add((f, PR.source, src('P04', 50)))
# make-up with a different chapter list from its midterm; and a make-up that repeats an item
pm5 = fx_('N37m', [], kind='Midterm', ver=3, prev=2)
pk5 = fx_('N37', [('R18', V)], kind='MakeUp', ver=3, prev=2, chapters=(1, 2, 3, 4, 5)); g.add((pk5, PR.companion, pm5))
for i in list(g.objects(pk5, PR.hasItem)): g.set((i, PR.itemKey, L('mk37-' + str(i).split('item')[-1])))
for i in list(g.objects(pm5, PR.hasItem)): g.set((i, PR.itemKey, L('mid37-' + str(i).split('item')[-1])))
# N37 uses chapter 6 in item 6: the shorter list also breaks R02
expected['N37'] = [('R18', V), ('R02', V)]
pm6 = fx_('N38m', [], kind='Midterm', ver=3, prev=2)
pk6 = fx_('N38', [('R18', W)], kind='MakeUp', ver=3, prev=2); g.add((pk6, PR.companion, pm6))
for i in list(g.objects(pm6, PR.hasItem)): g.set((i, PR.itemKey, L('mid38-' + str(i).split('item')[-1])))
for i in list(g.objects(pk6, PR.hasItem)): g.set((i, PR.itemKey, L('mk38-' + str(i).split('item')[-1])))
g.set((FX['N38_item2'], PR.itemKey, L('mid38-2')))   # one repeated item
p = fx_('N39', [('R06', V)]); g.set((FX['N39_item1'], PR.bloomLevel, I(5)))   # a four-option choice item claims Evaluate
p = fx_('N40', [('R07', V), ('R07', W)], mut={'keys': 'AAAABCDDB'})   # counts A4 B2 C1 D2 are uneven, and four A in a row
# a run of four with even counts: nine items cannot have a run of four AND even counts, so the run is tried on a sixteen-key paper of choice items
p = paper('N42', ver=2, prev=1); expected['N42'] = [('R07', W)]
for n, k in enumerate('AAAABBBBCCCCDDDD', 1):
    i = item('N42', p, n, 'ChoiceFour', 'ChoiceItem', 3, chapter=1 + n % 6); options('N42', i, k)
p = fx_('P05', [], chapters=(1, 2, 3, 4, 5, 6, 7))   # chapter 7 selected: the list is a parameter
g.add((FX['N43_foreign'], RDF.type, PR.BankEntry)); g.add((FX['N43_foreign'], PR.label, L('9'))); g.add((FX['N43_foreign'], PR.position, I(9))); g.add((FX['N43_foreign'], PR.text, L('FIXTURE foreign entry')))
p = fx_('N43', [('R12', V)]); g.set((FX['N43_item13'], PR.answerEntry, FX['N43_foreign']))
p = fx_('N44', [('R12', V)], mut={'answers': [0, 0, 2]})
p = fx_('N45', [('R04', V)]); g.set((FX['N45_item2'], PR.position, I(1)))
p = fx_('N46', [('R20', V)]); g.remove((FX['N46_item16'], PR.keyOutput, None))
p = fx_('N47', [('R04', V)]); g.remove((FX['N47_item1'], RDF.type, PR.ChoiceItem))
p = fx_('N48', [('R10', V)]); g.add((FX['N48_item1'], PR.codeLines, I(4)))
# ---------------- write
g.serialize(os.path.join(HERE, 'sen0401_exam_paperrules_fixtures_v1_0_0.ttl'), format='turtle')
json.dump({k: sorted(set(map(tuple, v))) for k, v in expected.items()}, open(os.path.join(HERE, 'sen0401_exam_paperrules_fixtures_expected_v1_0_0.json'), 'w'), indent=1)
print('fixtures:', len(expected), 'triples:', len(g))
