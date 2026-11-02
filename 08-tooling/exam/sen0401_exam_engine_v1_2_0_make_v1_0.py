#!/usr/bin/env python3
"""Makes the v1.2.0 copies of the shapes, the renderer, the engine and the fixture builders for FIVE alternatives (owner redesign 2026-11-02, ruling 3).
Every change is a string replacement that must hit exactly the stated number of times (an assertion), so the list below IS the list of differences from the committed v1.0.0 / v1.1.0 / v1.2.0 files, which are only read.
No rule is dropped: R07 (even letters, now over A to E), R11 (exactly N options, now five, letters A to E, each once), R14 (bank labels: one capital letter, A to E for the five entries, because the owner wants a letter per blank),
R15 (matching: now exactly one response more than premises, so 4 premises have 5 responses), all other rules and all engine rules EN01-EN13 are carried over word for word. Holds no question and no answer."""
import os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
def rd(n): return open(os.path.join(HERE, n), encoding='utf8').read()
def wr(n, s):
    p = os.path.join(HERE, n)
    with open(p, 'x', encoding='utf8') as f: f.write(s)
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a), n)
    return s.replace(a, b)
LOG = []
# ---------------------------------------------------------------- shapes
s = rd('sen0401_exam_paperrules_shapes_v1_0_0.ttl')
s = rep(s, 'counts of A, B, C, D differ by more than one', 'counts of A, B, C, D, E differ by more than one')
s = rep(s, '''        OPTIONAL { SELECT $this (COUNT(?o) AS ?cD) WHERE { $this pr:hasItem ?i . ?i pr:option ?o . ?o pr:isKey true ; pr:letter "D" } GROUP BY $this }
''', '''        OPTIONAL { SELECT $this (COUNT(?o) AS ?cD) WHERE { $this pr:hasItem ?i . ?i pr:option ?o . ?o pr:isKey true ; pr:letter "D" } GROUP BY $this }
        OPTIONAL { SELECT $this (COUNT(?o) AS ?cE) WHERE { $this pr:hasItem ?i . ?i pr:option ?o . ?o pr:isKey true ; pr:letter "E" } GROUP BY $this }
''')
s = rep(s, 'BIND(COALESCE(?cD, 0) AS ?d)\n        FILTER(abs(?a - ?b) > 1 || abs(?a - ?c) > 1 || abs(?a - ?d) > 1 || abs(?b - ?c) > 1 || abs(?b - ?d) > 1 || abs(?c - ?d) > 1)',
        'BIND(COALESCE(?cD, 0) AS ?d) BIND(COALESCE(?cE, 0) AS ?e)\n        FILTER(abs(?a - ?b) > 1 || abs(?a - ?c) > 1 || abs(?a - ?d) > 1 || abs(?a - ?e) > 1 || abs(?b - ?c) > 1 || abs(?b - ?d) > 1 || abs(?b - ?e) > 1 || abs(?c - ?d) > 1 || abs(?c - ?e) > 1 || abs(?d - ?e) > 1)')
s = rep(s, 'sh:minCount 4 ; sh:maxCount 4 ; sh:node pr:OptionShape ; sh:message "R11 a choice item has exactly four options"', 'sh:minCount 5 ; sh:maxCount 5 ; sh:node pr:OptionShape ; sh:message "R11 a choice item has exactly five options"')
s = rep(s, '''  sh:property [ sh:path pr:option ; sh:qualifiedValueShape [ sh:property [ sh:path pr:letter ; sh:hasValue "D" ] ] ; sh:qualifiedMinCount 1 ; sh:qualifiedMaxCount 1 ; sh:message "R11 letter D is used once" ] ;
''', '''  sh:property [ sh:path pr:option ; sh:qualifiedValueShape [ sh:property [ sh:path pr:letter ; sh:hasValue "D" ] ] ; sh:qualifiedMinCount 1 ; sh:qualifiedMaxCount 1 ; sh:message "R11 letter D is used once" ] ;
  sh:property [ sh:path pr:option ; sh:qualifiedValueShape [ sh:property [ sh:path pr:letter ; sh:hasValue "E" ] ] ; sh:qualifiedMinCount 1 ; sh:qualifiedMaxCount 1 ; sh:message "R11 letter E is used once" ] ;
''')
s = rep(s, 'sh:in ( "A" "B" "C" "D" ) ; sh:message "R11 an option letter is one of A, B, C, D"', 'sh:in ( "A" "B" "C" "D" "E" ) ; sh:message "R11 an option letter is one of A, B, C, D, E"')
s = rep(s, 'sh:pattern "^[0-9]+$" ; sh:message "R14 bank entries are numbered with digits, so they cannot be mistaken for the choice letters A to D"',
        'sh:pattern "^[A-Z]$" ; sh:message "R14 bank entries are lettered with one capital letter, A to E for the five entries of a bank (the owner wants a letter per blank)"')
s = rep(s, 'sh:message "R15 matching needs at least two more responses than premises"', 'sh:message "R15 matching needs exactly one response more than premises (four premises, five responses)"')
s = rep(s, 'FILTER(?nr < ?np + 2) }', 'FILTER(?nr != ?np + 1) }')
wr('sen0401_exam_paperrules_shapes_v1_2_0.ttl', s); LOG.append('shapes v1_2_0 written (R07, R11, R14, R15 changed as listed in the docstring)')
# ---------------------------------------------------------------- renderer v1_3_0 (copy of v1_2_0)
r = rd('sen0401_exam_engine_render_v1_2_0.py')
r = rep(r, "'ABCD'[k]", "'ABCDE'[k]", 1)
r = rep(r, "'opts': 'ABCD'", "'opts': 'ABCDE'", 1)
r = rep(r, "e['answer'] = 'ABCD'[it['answer']]", "e['answer'] = 'ABCDE'[it['answer']]", 1)
r = rep(r, "    return bank_code(position) if paper['params']['answer_mode'] == GRID else str(position)", "    return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[position - 1]      # v1.3.0: a bank entry is lettered A, B, C ... (a bank of five: A to E; a letter per blank)")
wr('sen0401_exam_engine_render_v1_3_0.py', r)
# ---------------------------------------------------------------- engine v1_2_0 (copy of v1_1_0)
e = rd('sen0401_exam_engine_v1_1_0.py')
e = rep(e, 'import sen0401_exam_engine_render_v1_1_0 as R', 'import sen0401_exam_engine_render_v1_3_0 as R')
e = rep(e, "VERSION = '1.1.0'", "VERSION = '1.2.0'")
e = rep(e, "'ABCD'[k]", "'ABCDE'[k]", 2)
e = rep(e, "from sen0401_exam_engine_v1_0_0 import ExamRefused, quotas, balance_letters, order_of_steps, L, I, B, D, SH, PR, EN, EX",
        "from sen0401_exam_engine_v1_0_0 import ExamRefused, quotas, order_of_steps, L, I, B, D, SH, PR, EN, EX\n\n\ndef balance_letters(choice_items, rnd):\n    \"\"\"v1.2.0: the keys of the choice items are spread evenly over A-E (counts differ by at most one), no run of four equal keys.\"\"\"\n    n = len(choice_items)\n    for _ in range(500):\n        t = [k % 5 for k in range(n)]; rnd.shuffle(t)\n        if not any(t[k] == t[k + 1] == t[k + 2] == t[k + 3] for k in range(n - 3)): break\n    for it, ti in zip(choice_items, t):\n        key = it['options'][it['answer']]; rest = [o for k, o in enumerate(it['options']) if k != it['answer']]; rnd.shuffle(rest)\n        rest.insert(ti, key); it['options'] = rest; it['answer'] = ti\n")
e = rep(e, "'sen0401_exam_paperrules_shapes_v1_0_0.ttl'", "'sen0401_exam_paperrules_shapes_v1_2_0.ttl'")
wr('sen0401_exam_engine_v1_2_0.py', e)
LOG.append('engine v1_2_0 and render v1_3_0 written')
print('\n'.join(LOG))
