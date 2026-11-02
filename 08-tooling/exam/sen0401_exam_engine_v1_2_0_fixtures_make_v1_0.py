#!/usr/bin/env python3
"""Makes the v1.2.0 fixture builders from the committed ones by counted string replacements (the committed files are only read), for FIVE alternatives:
 paperrules fixtures  (v1_0_0 -> v1_2_0): five options with letters A-E, five responses for four premises, bank entries lettered A-E, key lists spread over A-E; two fixtures added (N18b a four-option item, N27b four responses).
 authored fixture     (v1_1_1 -> v1_2_0): five options, five responses.
 engine fixtures      (v1_1_0 -> v1_2_0): the engine v1_2_0 and the authored fixture v1_2_0.
Then it runs the three builders. Holds no question and no answer (fixture text only)."""
import os, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
def rd(n): return open(os.path.join(HERE, n), encoding='utf8').read()
def wr(n, s):
    with open(os.path.join(HERE, n), 'x', encoding='utf8') as f: f.write(s)
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a), n)
    return s.replace(a, b)
# ---- paperrules fixtures
s = rd('sen0401_exam_paperrules_fixtures_build_v1_0_0.py')
s = s.replace('v1_0_0.ttl', 'v1_2_0.ttl').replace('expected_v1_0_0.json', 'expected_v1_2_0.json')
s = rep(s, "def options(fid, i, key, texts=None, n=4, keys=1, letters='ABCD'):", "def options(fid, i, key, texts=None, n=5, keys=1, letters='ABCDE'):")
s = rep(s, "keys = mut.get('keys', 'ABCDDCBAC')   # A2 B2 C3 D2: even", "keys = mut.get('keys', 'ABCDEEDCB')   # A1 B2 C2 D2 E2: even")
s = rep(s, "mut.get('nopts', {}).get(k, 4)", "mut.get('nopts', {}).get(k, 5)")
s = rep(s, "letters=mut.get('letters', {}).get(k, 'ABCD'))", "letters=mut.get('letters', {}).get(k, 'ABCDE'))")
s = rep(s, "nresp = mut.get('nresp', 6)", "nresp = mut.get('nresp', 5)")
s = rep(s, "labels = mut.get('labels', ['1', '2', '3', '4', '5'])", "labels = mut.get('labels', ['A', 'B', 'C', 'D', 'E'])")
s = rep(s, "mut={'keys': 'BADCCDBAD'}", "mut={'keys': 'EDCBAABCD'}")
s = rep(s, "['FIXTURE a', 'FIXTURE b', 'All of the above', 'FIXTURE d']", "['FIXTURE a', 'FIXTURE b', 'All of the above', 'FIXTURE d', 'FIXTURE e']")
s = rep(s, "mut={'labels': ['a', '2', '3', '4', '5']}", "mut={'labels': ['a', 'B', 'C', 'D', 'E']}")
s = rep(s, "mut={'nentries': 3, 'labels': ['1', '2', '3'], 'bankpos': [3, 1, 2]}", "mut={'nentries': 3, 'labels': ['A', 'B', 'C'], 'bankpos': [3, 1, 2]}")
s = rep(s, "neg('N27', [('R15', V)], mut={'nresp': 5})              # four premises, five responses", "neg('N27', [('R15', V)], mut={'nresp': 6})              # four premises, six responses (the old shape)\nneg('N27b', [('R15', V)], mut={'nresp': 4})             # four premises, four responses")
s = rep(s, "neg('N19', [('R11', V)], mut={'nkeys': {0: 2}})", "neg('N18b', [('R11', V)], mut={'nopts': {2: 4}, 'letters': {2: 'ABCD'}})   # four options (the old shape)\nneg('N19', [('R11', V)], mut={'nkeys': {0: 2}, 'keys': 'CADEEBDCA'})")
s = rep(s, "for n, k in enumerate('AAAABBBBCCCCDDDD', 1):", "for n, k in enumerate('AAAABBBBCCCCDDDDEEEE', 1):")
# P03: real bank items get a synthetic fifth option; the key is moved to the letter (n-1) % 5 so that the 30 keys are even
a = "    for a, c in enumerate('ABCD'):\n        o = FX['P03_item%d_opt_%s' % (n, c)]; g.add((i, PR.option, o)); g.add((o, PR.letter, L(c))); g.add((o, PR.isKey, B(a == it['answer']))); g.add((o, PR.text, L(it['options'][a])))\n"
b = ("    tg = (n - 1) % 5; others = [it['options'][x] for x in range(4) if x != it['answer']] + ['FIXTURE fifth option']; ol = others[:tg] + [it['options'][it['answer']]] + others[tg:]\n"
     "    for a, c in enumerate('ABCDE'):\n        o = FX['P03_item%d_opt_%s' % (n, c)]; g.add((i, PR.option, o)); g.add((o, PR.letter, L(c))); g.add((o, PR.isKey, B(a == tg))); g.add((o, PR.text, L(ol[a])))\n")
s = rep(s, a, b)
s = rep(s, "PR.label, L('9')", "PR.label, L('Z')")
wr('sen0401_exam_paperrules_fixtures_build_v1_2_0.py', s)
# ---- authored fixture
s = rd('sen0401_exam_engine_authored_fixture_build_v1_1_1.py')
s = s.replace('fixture_authored_v1_1_1.json', 'fixture_authored_v1_2_0.json')
s = rep(s, "BL = [2, 3, 3, 4, 4, 4, 3, 4, 3, 2]   # the ceilings of the paper types: choice 4, matching 3, ordering 3, fill-in 2, number 3, trace 4", "BL = [2, 3, 3, 4, 4, 4, 3, 4, 3, 2]")
s = rep(s, "'FIXTURE c%d n%d fourth statement delta' % (c, n)], answer=n % 4)", "'FIXTURE c%d n%d fourth statement delta' % (c, n), 'FIXTURE c%d n%d fifth statement epsilon' % (c, n)], answer=n % 5)")
s = rep(s, "options=['FIXTURE c%d code option %d' % (c, k) for k in range(4)], answer=1)", "options=['FIXTURE c%d code option %d' % (c, k) for k in range(5)], answer=1)")
s = rep(s, "match='FIXTURE %s response %s' % (tag, 'ABCD'[k])) for k in range(4)],\n                      responses=['FIXTURE %s response %s' % (tag, x) for x in 'ABCDEF']))", "match='FIXTURE %s response %s' % (tag, 'ABCD'[k])) for k in range(4)],\n                      responses=['FIXTURE %s response %s' % (tag, x) for x in 'ABCDE']))")
wr('sen0401_exam_engine_authored_fixture_build_v1_2_0.py', s)
# ---- engine fixtures
s = rd('sen0401_exam_engine_fixtures_build_v1_1_0.py')
s = s.replace('engine_v1_1_0', 'engine_v1_2_0').replace('fixtures_v1_1_0.ttl', 'fixtures_v1_2_0.ttl').replace('expected_v1_1_0.json', 'expected_v1_2_0.json').replace('fixture_authored_v1_1_0.json', 'fixture_authored_v1_2_0.json')
wr('sen0401_exam_engine_fixtures_build_v1_2_0.py', s)
for n in ('sen0401_exam_paperrules_fixtures_build_v1_2_0.py', 'sen0401_exam_engine_authored_fixture_build_v1_2_0.py', 'sen0401_exam_engine_fixtures_build_v1_2_0.py'):
    r = subprocess.run([sys.executable, os.path.join(HERE, n)], capture_output=True, text=True, cwd=HERE); print(n, r.returncode, (r.stdout + r.stderr).strip()[-300:])
    if r.returncode: sys.exit(1)
