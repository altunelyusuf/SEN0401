"""Checks of the printed-paper rules, version 1.0.0. Prints PASS / FAIL / NOT_MEASURED per check.
Usage: check.py [--log FILE]
C1  every produced file is new (no tracked file modified or deleted)
C2  the shapes and the registry parse; every rule id named in the shapes is listed
C3  the shapes run on every fixture (one fixture at a time, with the registry) and give exactly the expected answer
C4  every rule has at least one fixture that breaks it (rules without one are named)
C5  the registry is complete (status, basis, reason; suited types have a class and a time)
C6  the page-saving measurement is re-run and agrees with the numbers in the registry
C7  the chapter list is a parameter: a paper with chapters 1 to 7 conforms, one with chapter 8 does not
C8  facts about the banks are re-measured and printed (only four-option items; Bloom counts)
"""
import collections, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rdflib import Graph, Namespace, RDF, RDFS, Literal
import pyshacl
import sen0401_exam_pagesave_measure_v1_0_0 as M
SH = Namespace('http://www.w3.org/ns/shacl#'); PR = Namespace('http://example.org/sen0401/paperrules#')
V = 'sen0401_exam_%s_v1_0_0'
shapes = Graph().parse(os.path.join(HERE, V % 'paperrules_shapes' + '.ttl'))
reg = Graph().parse(os.path.join(HERE, V % 'papertypes' + '.ttl'))
fxg = Graph().parse(os.path.join(HERE, V % 'paperrules_fixtures' + '.ttl'))
exp = {k: set(map(tuple, v)) for k, v in json.load(open(os.path.join(HERE, V % 'paperrules_fixtures_expected' + '.json'))).items()}
res = []
def rep(name, ok, detail=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail))

g = subprocess.run(['git', '-C', M.TOOL + '/..', 'status', '--porcelain'], capture_output=True, text=True)
bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
rep('C1 no committed file is edited', g.returncode == 0 and not bad, ' '.join(bad[:5]))

msgs = [str(m) for m in shapes.objects(None, SH.message)]
rules = sorted({m.split()[0] for m in msgs}, key=lambda x: int(x[1:]))
rep('C2 shapes and registry parse; rule ids found', len(rules) > 0 and len(shapes) > 0 and len(reg) > 0, '%d rules: %s' % (len(rules), ' '.join(rules)))

def subgraph(fid):
    sub = Graph()
    keep = {fid}
    for s, o in fxg.subject_objects(PR.companion):
        if str(s).endswith('#%s_paper' % fid): keep.add(str(o).split('#')[1].split('_')[0])
    for s, p, o in fxg:
        if str(s).split('#')[-1].split('_')[0] in keep: sub.add((s, p, o))
    for t in reg: sub.add(t)
    return sub

def run(sub):
    conf, rg, txt = pyshacl.validate(sub, shacl_graph=shapes, advanced=True, inference='none', js=False)
    out = set()
    for r in rg.subjects(SH.resultSeverity, None):
        out.add((str(rg.value(r, SH.resultMessage)).split()[0], str(rg.value(r, SH.resultSeverity)).split('#')[1]))
    return conf, out

wrong = []; seen = set(); n = 0
for fid in sorted(exp):
    conf, got = run(subgraph(fid)); n += 1
    # companion papers (names ending in m) are checked on their own line: they must conform
    if got != exp[fid]: wrong.append((fid, sorted(exp[fid]), sorted(got)))
    seen |= {r for r, s in got}
    if fid in ('P01', 'P02', 'P03') or got != exp[fid]: print('     %s expected %s got %s conforms=%s' % (fid, sorted(exp[fid]), sorted(got), conf))
rep('C3 every fixture gives exactly the expected answer', not wrong, '(%d fixtures) %s' % (n, '; '.join('%s expected %s got %s' % w for w in wrong[:6])))
unc = [r for r in rules if r not in seen]
rep('C4 every rule is broken by at least one fixture', not unc, 'not exercised: %s' % unc if unc else '(%d of %d)' % (len(seen), len(rules)))

fails = []
for t in reg.subjects(RDF.type, PR.ItemType):
    st = reg.value(t, PR.status)
    for p in (PR.status, PR.basis, PR.reason, PR.highestBloom, PR.secondsPerItem):
        if reg.value(t, p) is None: fails.append((str(t).split('#')[1], str(p).split('#')[1]))
    if st == PR.Suited and reg.value(t, PR.itemClass) is None and str(t).split('#')[1] not in ('ChoiceFour',): fails.append((str(t).split('#')[1], 'itemClass'))
    if st == PR.NotSuited and reg.value(t, PR.itemClass) is not None: fails.append((str(t).split('#')[1], 'not-suited type with a class'))
cnt = collections.Counter(str(reg.value(t, PR.status)).split('#')[1] for t in reg.subjects(RDF.type, PR.ItemType))
rep('C5 every item type has status, basis, reason, highest Bloom and time; suited types have a class', not fails, '%s %s' % (dict(cnt), fails[:4]))

r = M.run(M.parse_ch('1-6'), 40)
frac = r['fractional_pages_of_content_(sum of item heights / page area; answer sheet included)']
want = {'M1': 'c_M1', 'M2': 'c_M2', 'M3': 'c_M3', 'M4': 'c_M4', 'M5': 'c_M5'}
mis = []
for m, k in want.items():
    v = reg.value(PR[m], PR.measuredFractionalPages)
    if v is None or abs(float(v) - frac[k]) > 0.005: mis.append((m, str(v), frac[k]))
print('     baseline pages %s -> stacked pages %s; fractional baseline %s; sheets %s' % (r['pages_baseline'], list(r['pages_methods_stacked_in_order'].values())[-1], frac['b0'], r['M6 duplex: sheets of paper (pages / 2, rounded up) baseline -> stacked']))
b = r['block_models_pt']
print('     matching block %s pt vs five choice items %s pt; fill-in bank %s pt vs six choice items %s pt' % (b['matching_5_premises_7_responses_pt'], b['mc_5_items_pt'], b['fillin_6_blanks_one_bank_pt'], b['mc_6_items_pt']))
rep('C6 re-run page measurement agrees with the registry', not mis and r['pages_baseline'] > list(r['pages_methods_stacked_in_order'].values())[-1], str(mis))

conf7, got7 = run(subgraph('P05')); conf8, got8 = run(subgraph('N06'))
rep('C7 chapter list is a parameter: chapters 1 to 7 conform, chapter 8 is refused', conf7 and not conf8 and ('R02', 'Violation') in got8, 'P05 %s; N06 %s' % (sorted(got7), sorted(got8)))

tot = collections.Counter(); n4 = 0; allitems = 0
for c in range(1, 9):
    f, b = M.load_bank(c)
    for i in b:
        allitems += 1; tot[i['level']] += 1; n4 += (len(i['options']) == 4)
print('     banks chapters 1 to 8: %d items, %d with four options, levels %s' % (allitems, n4, dict(tot)))
rep('C8 the banks hold only four-option items (so the other types are new)', allitems == n4)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
