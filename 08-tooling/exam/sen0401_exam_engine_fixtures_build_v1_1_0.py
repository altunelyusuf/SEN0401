"""Builds the SHACL fixtures of known answer for the rules EN11, EN12, EN13 of engine v1.1.0 (new file).
Writes sen0401_exam_engine_fixtures_v1_1_0.ttl and sen0401_exam_engine_fixtures_expected_v1_1_0.json.
The conforming fixtures (P) are pairs of synthetic papers built by the v1.1.0 engine from the authored FIXTURE items; each N fixture is that pair with ONE thing broken by editing the graph.
The expected answer of each fixture is written in this file from the intent of the break, BEFORE the fixtures are first run. Expected answers are sets of (rule, severity)."""
import copy, json, os, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rdflib import Graph, URIRef, Literal, RDF
import sen0401_exam_engine_v1_1_0 as E
PR, EN, EX = E.PR, E.EN, E.EX
AUTH = os.path.join(HERE, 'sen0401_exam_engine_fixture_authored_v1_1_0.json')
V_, W_ = 'Violation', 'Warning'
fixtures = {}; expected = {}
def keep(fid, g, ans): fixtures[fid] = g; expected[fid] = sorted(ans)

def pair_graph(P):
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
    base = str(EX); out = Graph()
    f = lambda t: URIRef(str(t).replace(base, base + fid + '/', 1)) if isinstance(t, URIRef) and str(t).startswith(base) else t
    for s, p, o in g: out.add((f(s), p, f(o)))
    return out
def items_of(g, p): return sorted(g.objects(p, PR.hasItem), key=lambda i: int(g.value(i, PR.position)))

P0 = E.Params(24, authored=AUTH)
base, pm, pk, pair = pair_graph(P0)
def clone():
    g = Graph(); g.bind('pr', PR); g.bind('en', EN)
    for t in base: g.add(t)
    return g
pages, _ = E.pages_for(P0.chapters)
ctx = E.context_graph(pages)
page_with_opts = [n for n in ctx.subjects(EN.optionSetKey, None)][0]
page_any = [n for n in ctx.subjects(EN.normStem, None)][0]
cp7 = [pid for pid, p in E.cp_index().items() if p['chapter'] == 7][0]

keep('P01', clone(), [])
# P02: the circle-on-item answer mode with a ten-entry bank is allowed (EN13 is a rule of the grid only)
tmp = tempfile.mkdtemp(prefix='sen0401_fxauth_', dir=os.environ.get('SEN0401_ENGINE_TMP'))
a = json.load(open(AUTH))
for it in a['items']:
    if it['key'] == 'fx:m:fill': it['distractors'] = ['FIXTURE m spare %d' % k for k in range(7)]
a['items'] = [it for it in a['items'] if not (it['key'].startswith('fx:c1:choice') and it['key'] not in ('fx:c1:choice0', 'fx:c1:choice1'))]   # chapter 1 can only take the fill-in group plus one choice item, so the ten-entry bank is on the midterm
ap = os.path.join(tmp, 'a.json'); json.dump(a, open(ap, 'w'))
g, _, _, _ = pair_graph(E.Params(24, authored=ap, answer_mode='CircleOnItem')); keep('P02', g, [])
# N54: the same bank (10 entries) with the grid answer mode
g, _, _, _ = pair_graph(E.Params(24, authored=ap, answer_mode='GridOnCover')); keep('N54', g, [('EN13', V_)])
os.remove(ap); os.rmdir(tmp)

# ---- EN11
g = clone(); i = items_of(g, pm)[0]; g.add((i, EN.normStem, ctx.value(page_any, EN.normStem))); keep('N40', g, [('EN11', V_)])
g = clone(); i = items_of(g, pm)[0]; g.add((i, EN.optionSetKey, ctx.value(page_with_opts, EN.optionSetKey))); keep('N41', g, [('EN11', V_)])
g = clone(); i = items_of(g, pm)[0]; m = EX['fxmatch']; g.add((i, EN.pageMatch, m)); g.add((m, EN.matchedPageItem, page_any)); g.add((m, EN.matchKinds, Literal('STEM_NEAR'))); keep('N42', g, [('EN11', V_)])
g = clone(); i = items_of(g, pm)[0]; g.set((i, EN.origin, EN.PageBank)); keep('N43', g, [('EN11', V_)])
g = clone(); i = items_of(g, pm)[0]; g.set((i, EN.copyChecked, E.B(False))); keep('N44', g, [('EN11', V_)])
g = clone(); i = items_of(g, pm)[0]; g.remove((i, EN.copyChecked, None)); keep('N45', g, [('EN11', V_)])
g = clone(); g.set((pm, EN.pageVisibleItems, E.I(0))); keep('N46', g, [('EN11', V_)])
g = clone(); g.remove((pm, EN.requiredPageChapter, E.I(6))); keep('N47', g, [('EN11', V_)])
g = clone(); g.set((pm, EN.pageVisibleItems, E.I(1000))); keep('N48', g, [('EN11', V_)])
g = clone(); g.remove((pm, EN.similarityVersion, None)); keep('N55', g, [('EN11', V_)])
# ---- EN12
g = clone(); i = items_of(g, pm)[0]; g.remove((i, EN.tests, None)); keep('N49', g, [('EN12', V_)])
g = clone(); i = items_of(g, pm)[0]; g.remove((i, EN.tests, None)); g.add((i, EN.tests, E.CPN['CP99.99'])); keep('N50', g, [('EN12', V_)])
g = clone(); i = [x for x in items_of(g, pm) if (x, EN.seedItem, None) in g][0]; g.remove((i, EN.seedItem, None)); g.add((i, EN.seedItem, E.PG['ch99_nothing_here_0'])); keep('N51', g, [('EN12', V_)])
g = clone(); i = [x for x in items_of(g, pm) if (x, EN.seedItem, None) in g][0]; g.remove((i, EN.seedItem, None)); keep('N52', g, [('EN12', V_)])
g = clone(); i = items_of(g, pm)[0]; g.add((i, EN.tests, E.CPN[cp7])); keep('N53', g, [('EN12', V_)])

big = Graph(); big.bind('pr', PR); big.bind('en', EN)
for fid, gg in fixtures.items():
    for t in shift(gg, fid): big.add(t)
big.serialize(os.path.join(HERE, 'sen0401_exam_engine_fixtures_v1_1_0.ttl'), format='turtle')
json.dump({k: [list(x) for x in v] for k, v in expected.items()}, open(os.path.join(HERE, 'sen0401_exam_engine_fixtures_expected_v1_1_0.json'), 'w'), indent=1)
print('fixtures', len(fixtures), 'triples', len(big))
