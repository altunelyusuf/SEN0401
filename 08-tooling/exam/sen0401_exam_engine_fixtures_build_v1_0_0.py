"""Builds the fixtures of known answer for the exam engine, version 1.0.0.
Writes sen0401_exam_engine_fixtures_v1_0_0.ttl and sen0401_exam_engine_fixtures_expected_v1_0_0.json.
Each fixture is a synthetic pair of papers (midterm and make-up, no student data). The conforming fixtures are built by the engine; each N-fixture is that
pair with ONE convention broken by editing the graph. The expected answer of an N-fixture is written here from the intent of the break, before any run."""
import copy, json, os, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rdflib import Graph, URIRef, Literal, RDF, XSD
import sen0401_exam_engine_v1_0_0 as E
PR, EN, EX = E.PR, E.EN, E.EX
V = E.V
AUTH = os.path.join(HERE, V % 'engine_fixture_authored')

def pair_graph(P, extra_items=None):
    mid, gm, pm = E.make_and_check(P, 'midterm', prev=1, render=False)
    excl = frozenset() if P.allow_repeat else frozenset(i['key'] for i in mid['items'])
    mk, gk, pk = E.make_and_check(P, 'makeup', exclude=excl, prev=1, salt=1, render=False)
    g = Graph(); g.bind('pr', PR); g.bind('en', EN)
    for t in gm: g.add(t)
    for t in gk: g.add(t)
    g.add((pk, PR.companion, pm)); pair = EX['pair']
    g.add((pair, RDF.type, EN.ExamPair)); g.add((pair, EN.midterm, pm)); g.add((pair, EN.makeUp, pk)); g.add((pair, EN.repeatAllowed, E.B(P.allow_repeat)))
    return g, pm, pk, pair

def shift(g, fid):
    """Move every engine-paper URI under a fixture-specific namespace so that all fixtures live in one file."""
    base = str(EX); out = Graph()
    f = lambda t: URIRef(str(t).replace(base, base + fid + '/', 1)) if isinstance(t, URIRef) and str(t).startswith(base) else t
    for s, p, o in g: out.add((f(s), p, f(o)))
    return out

fixtures = {}; expected = {}
def keep(fid, g, ans): fixtures[fid] = g; expected[fid] = sorted(ans)
def items_of(g, p): return sorted(g.objects(p, PR.hasItem), key=lambda i: int(g.value(i, PR.position)))
def choice_items(g, p): return [i for i in items_of(g, p) if (i, RDF.type, PR.ChoiceItem) in g]
def opts(g, i): return sorted(g.objects(i, PR.option), key=lambda o: str(g.value(o, PR.letter)))
V_, W_ = 'Violation', 'Warning'

P0 = E.Params(18, matching=1, synthesis_min=1, indirect_enabled=True, authored=AUTH + '.json')
base, pm, pk, pair = pair_graph(P0)
cp = lambda: copy.deepcopy(base)
def clone():
    g = Graph(); g.bind('pr', PR); g.bind('en', EN)
    for t in base: g.add(t)
    return g

keep('P01', clone(), [])
# P02: chapter 7 selectable (chapters 1 to 7)
g, _, _, _ = pair_graph(E.Params(21, chapters=(1, 2, 3, 4, 5, 6, 7), matching=1, synthesis_min=1, indirect_enabled=True, authored=AUTH + '.json')); keep('P02', g, [])
# P03: a chapter list of two chapters
g, _, _, _ = pair_graph(E.Params(10, chapters=(2, 5), authored=AUTH + '.json')); keep('P03', g, [])
# P04: unequal chapter weights
g, _, _, _ = pair_graph(E.Params(21, weights={1: 3, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, matching=1, indirect_enabled=True, authored=AUTH + '.json')); keep('P04', g, [])
# P05: higher-order reading Analyze and up, a pool without authored items
g, _, _, _ = pair_graph(E.Params(20, higher_from=4, higher_share=0.8)); keep('P05', g, [])
# P06: a short written answer enabled by the paper (authored item from a temporary file)
tmp = tempfile.mkdtemp(prefix='sen0401_fxauth_', dir=os.environ.get('SEN0401_ENGINE_TMP'))
a = json.load(open(AUTH + '.json')); a['items'].append(dict(key='fx:short1', type='ShortAnswer', chapters=[6], bloom=5, kind='direct', source=dict(file='FIXTURE source', locator='FIXTURE'),
                                                            q='FIXTURE short answer stem', rubric=['FIXTURE point one', 'FIXTURE point two'], lines=2, papers=['midterm']))
ap = os.path.join(tmp, 'a.json'); json.dump(a, open(ap, 'w'))
g, gm_, gk_, _ = pair_graph(E.Params(18, matching=1, synthesis_min=1, indirect_enabled=True, authored=ap, enable=['ShortAnswer'])); keep('P06', g, [])
g2 = Graph(); g2.bind('pr', PR); g2.bind('en', EN)
for t in g:
    if t[1] != PR.enables: g2.add(t)
keep('N14', g2, [('R04', V_)])
os.remove(ap); os.rmdir(tmp)
# P07: the make-up repeats a midterm item and the pair allows it (R18 stays a warning)
g = clone(); mi = items_of(g, pm)[0]; ki = items_of(g, pk)[0]
g.set((ki, PR.itemKey, g.value(mi, PR.itemKey))); g.set((pair, EN.repeatAllowed, E.B(True))); keep('P07', g, [('R18', W_)])

# ---- convention: even answer letters
g = clone()
for i in choice_items(g, pm):
    for o in opts(g, i): g.set((o, PR.isKey, E.B(str(g.value(o, PR.letter)) == 'A')))
keep('N01', g, [('R07', V_), ('R07', W_)])
# ---- convention: Bloom majority
g = clone()
for i in items_of(g, pm): g.set((i, PR.bloomLevel, E.I(1)))
keep('N02', g, [('R06', V_), ('EN04', V_)])
g = clone()  # the same paper judged at the Analyze-and-up reading: Apply items no longer count
g.set((pm, EN.higherFrom, E.I(4))); keep('N03', g, [('EN04', V_)])
# ---- chapter weights
g = clone(); q = list(g.objects(pm, EN.chapterQuota))[0]; g.set((q, EN.quotaItems, E.I(int(g.value(q, EN.quotaItems)) + 1))); keep('N04', g, [('EN01', V_), ('EN07', V_)])
g = clone(); q = list(g.objects(pm, EN.chapterQuota))[0]; g.remove((pm, EN.chapterQuota, q)); keep('N05', g, [('EN01', V_), ('EN07', V_)])
g = clone(); i = items_of(g, pm)[0]; g.add((i, PR.chapter, E.I(8))); keep('N06', g, [('R02', V_)])
g = clone(); g.add((pm, PR.chapterList, E.I(8))); g.add((pk, PR.chapterList, E.I(8))); keep('N07', g, [('EN01', V_), ('R02', V_)])
g = clone(); g.remove((pm, PR.chapterList, None)); keep('N08', g, [('R02', V_), ('R18', V_)])
# ---- synthesis and indirect kinds
g = clone(); si = [i for i in items_of(g, pm) if (i, PR.synthesis, E.B(True)) in g][0]; pc = g.value(si, EN.primaryChapter)
for c in list(g.objects(si, PR.chapter)):
    if c != pc: g.remove((si, PR.chapter, c))
keep('N09', g, [('R09', V_)])
g = clone(); g.set((pm, EN.synthesisMin, E.I(99))); keep('N10', g, [('EN02', V_)])
g = clone(); g.set((pm, EN.indirectEnabled, E.B(False))); keep('N11', g, [('EN03', V_)])
g = clone(); ii = [i for i in items_of(g, pm) if (i, EN.kind, EN.Indirect) in g][0]; g.remove((ii, EN.indirectForm, None)); keep('N12', g, [('EN03', V_)])
# ---- versions and the pair
g = clone(); g.set((pm, PR.versionSeq, E.I(5))); keep('N13', g, [('R03', V_)])
g = clone(); mi = items_of(g, pm)[0]; ki = items_of(g, pk)[0]; g.set((ki, PR.itemKey, g.value(mi, PR.itemKey))); keep('N15', g, [('EN05', V_), ('R18', W_)])
g = clone(); g.remove((pk, PR.chapterList, E.I(6))); keep('N16', g, [('R02', V_), ('R18', V_)])
g = clone(); g.remove((pair, EN.makeUp, None)); keep('N17', g, [('EN09', V_)])
g = clone(); g.set((pair, EN.midterm, pk)); keep('N18', g, [('EN05', V_), ('EN09', V_)])
g = clone(); g.remove((pk, PR.companion, None)); keep('N19', g, [('EN09', V_), ('R18', V_)])
# ---- item types
g = clone(); lo = [i for i in choice_items(g, pm) if int(g.value(i, PR.bloomLevel)) <= 2][0]; g.set((lo, PR.itemType, PR.TrueFalse)); keep('N20', g, [('R04', V_)])
g = clone(); ci = choice_items(g, pm)[0]; g.set((ci, PR.itemType, PR.Essay)); keep('N21', g, [('R04', V_)])
# ---- print safety, personal data
g = clone(); g.set((pm, PR.theme, E.L('dark'))); keep('N22', g, [('R01', V_)])
g = clone(); g.add((pm, PR.studentName, E.L('FIXTURE name'))); keep('N23', g, [('R01', V_)])
g = clone(); g.set((pm, PR.sittingMinutes, E.I(20))); keep('N24', g, [('R05', V_)])
g = clone(); g.set((pm, PR.codeColumnCapacity, E.I(60))); keep('N25', g, [('R10', V_)])
g = clone(); g.set((pm, PR.pageLimit, E.I(1))); g.set((pm, PR.pageCount, E.I(3))); keep('N26', g, [('R17', V_)])
# ---- terms, keys, sources
g = clone(); i = items_of(g, pm)[1]; g.add((i, EN.unfoundTerm, E.L('FIXTURE term absent from the corpus'))); keep('N27', g, [('EN08', V_)])
g = clone(); its = items_of(g, pm); g.set((its[1], PR.itemKey, g.value(its[0], PR.itemKey))); keep('N28', g, [('EN06', V_)])
g = clone(); i = items_of(g, pm)[2]; g.remove((i, PR.source, None)); keep('N29', g, [('R08', V_)])
# ---- fill-in bank, matching, ordering, choice options
g = clone(); bk = list(g.subjects(RDF.type, PR.Bank))
bk = [b for b in bk if str(b).startswith(str(EX) + 'midterm')][0]
ents = {}
for i in g.subjects(PR.bank, bk): ents[int(g.value(i, PR.blankNo))] = g.value(i, PR.answerEntry)
for k, e in sorted(ents.items()): g.set((e, PR.position, E.I(k)))
keep('N30', g, [('R13', V_)])
g = clone(); e = list(g.objects(bk, PR.entry))[0]; g.set((e, PR.label, E.L('A'))); keep('N31', g, [('R14', V_)])
g = clone(); mi = [i for i in items_of(g, pm) if (i, RDF.type, PR.MatchingItem) in g][0]
used = {g.value(p_, PR.matchesTo) for p_ in g.objects(mi, PR.hasPremise)}; spare = [r for r in g.objects(mi, PR.hasResponse) if r not in used][0]
g.remove((mi, PR.hasResponse, spare)); keep('N32', g, [('R15', V_)])
g = clone(); oi = [i for i in items_of(g, pm) if (i, RDF.type, PR.OrderingItem) in g][0]; st = sorted(g.objects(oi, PR.step), key=lambda x: int(g.value(x, PR.correctPosition))); g.set((st[1], PR.correctPosition, E.I(1))); keep('N33', g, [('R16', V_)])
g = clone(); ci = choice_items(g, pm)[0]; o = opts(g, ci); g.set((o[1], PR.text, g.value(o[0], PR.text))); keep('N34', g, [('R11', V_)])

g = clone(); i = items_of(g, pm)[0]; g.set((i, EN.primaryChapter, E.I(3 if int(g.value(i, EN.primaryChapter)) != 3 else 4)))
keep('N35', g, [('EN01', V_), ('EN10', V_)])
g = clone(); si = [i for i in items_of(g, pm) if (i, PR.synthesis, E.B(True)) in g][0]; g.remove((si, PR.synthesis, None)); keep('N36', g, [('EN10', V_)])

big = Graph(); big.bind('pr', PR); big.bind('en', EN)
for fid, gg in fixtures.items():
    for t in shift(gg, fid): big.add(t)
big.serialize(os.path.join(HERE, V % 'engine_fixtures' + '.ttl'), format='turtle')
json.dump({k: [list(x) for x in v] for k, v in expected.items()}, open(os.path.join(HERE, V % 'engine_fixtures_expected' + '.json'), 'w'), indent=1)
print('fixtures', len(fixtures), 'triples', len(big))
