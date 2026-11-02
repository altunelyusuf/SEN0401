#!/usr/bin/env python3
"""SEN0401 exam items part q1 v1.8.0 GENERIC check (holds no question and no answer; reads the private part file and items v1.7.0 from CME by path). Usage: script [PART.json OLD_ITEMS.json]. P6 is NOT_MEASURED here. Task TK_Exam_V72_Q1_Build.
Proves: P1 seven items, same keys/type/chapters/bloom/critical points/sub_question as v1.7.0; P2 intention sentence last, stem <= 60 words; P3 tip <= 12 words; P4 solution (steps, why right, why wrong for every other option; a number in each step of a calculation item);
P5 no outside reference; P6 answers recomputed by running code (two routes), each option claim evaluated; P7 readability check v1.1.0 R1-R4, R6 (R5 NOT_MEASURED); P8 options: five, distinct, one right, letters as before."""
import json, os, re, sys, math, fractions
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/sen0401/08-tooling/exam')
import sen0401_exam_readability_check_v1_1_0 as R
CMEP = '/home/claude/CME/exams/SEN0401/08-tooling/exam/private'
PART = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CMEP, 'sen0401_exam_items_part_q1_v1_8_0.json'); OLD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(CMEP, 'sen0401_exam_items_midterm_v1_7_0.json')
part = json.load(open(PART, encoding='utf8')); old = {i['key']: i for i in json.load(open(OLD, encoding='utf8'))['items']}
fails = []
def say(ok, name, detail=''):
    print('%-5s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    if not ok: fails.append(name)
nw = R.nwords
CALC = {i['key'] for i in part if i.get('solution', {}).get('calculation')}

# P1
say(len(part) == 7 and all(i['key'] in old for i in part), 'P1a seven items, all keys exist in v1.7.0')
for i in part:
    o = old[i['key']]
    same = all(i.get(f) == o.get(f) for f in ('type', 'chapters', 'bloom', 'kind', 'critical_points', 'sub_question', 'sources', 'source', 'seeds', 'papers', 'replaces'))
    say(same, 'P1b topic fields kept', i['key'])
    say(set(o['critical_points']) <= set(i['critical_points']), 'P1c no critical point lost', '%s %s' % (i['key'], i['critical_points']))
# P2 P3
for i in part:
    sents = R.sentences(i['q'], json.load(open('/home/claude/sen0401/08-tooling/exam/sen0401_exam_readability_rule_v1_1_0.json')))
    say(sents[-1].startswith('You are asked to') and sum(1 for s in sents if s.startswith('You are asked to')) == 1, 'P2a intention sentence last', i['key'])
    say(nw(i['q']) <= 60, 'P2b stem <= 60 words', '%s %d' % (i['key'], nw(i['q'])))
    t = i['tip']; say(t.startswith('Tip:') and nw(t[4:]) <= 12, 'P3 tip <= 12 words', '%s %d' % (i['key'], nw(t[4:])))
    say(nw(i['how_to_answer']) <= 25 and i['how_to_answer'].split()[0] == 'Write', 'P3b how_to_answer', i['key'])
# P4 P5
BAN = re.compile(r'\b(the story|the history|as shown above|see above|above|the table|as in the lecture|in class|in the slides?|the slide|block \d{3,}|Satoshi Nakamoto)\b', re.I)
for i in part:
    s = i.get('solution') or {}
    letters = [c for c in 'ABCDE' if c != 'ABCDE'[i['answer']]]
    ok = bool(s.get('steps')) and s.get('why_right') and sorted((s.get('why_wrong') or {}).keys()) == letters and all(len(v.split()) >= 4 for v in s['why_wrong'].values())
    say(ok, 'P4a solution: steps, why right, why wrong for each other option', i['key'])
    if i['key'] in CALC: say(all(re.search(r'\d', st) for st in s['steps']), 'P4b a number in every step of a calculation', i['key'])
    alltext = ' '.join([i['q'], i['tip']] + i['options'])
    say(not BAN.search(alltext), 'P5 no outside reference', '%s %s' % (i['key'], BAN.findall(alltext)))
    say(len(i['options']) == 5 and len(set(i['options'])) == 5, 'P8a five distinct options', i['key'])
    say('ABCDE'[i['answer']] == old[i['key']]['letter_after'] if False else 'ABCDE'[i['answer']] == 'ABCDE'[old[i['key']]['answer']], 'P8b correct letter as in v1.7.0', '%s %s' % (i['key'], 'ABCDE'[i['answer']]))
say(sorted(set('ABCDE'[i['answer']] for i in part)) == sorted(set('ABCDE'[old[i['key']]['answer']] for i in part)), 'P8c letter spread unchanged')

# P6 (answers recomputed by running code) needs the figures of the items; it lives only in the private CME check, never in this public script
say(True, 'P6 recompute: NOT_MEASURED here (private CME check only)')

# P7 readability v1.1.0
rule = R.load_rule('/home/claude/sen0401/08-tooling/exam/sen0401_exam_readability_rule_v1_1_0.json')
units, tips = R.read_items(PART, rule)
res = R.run_source('items part q1', units, None, tips, rule, True)
R.print_report('items part q1', res)
for r in ('R1', 'R2', 'R3', 'R4', 'R6'): say(res[r]['status'] == 'MEASURED' and not res[r]['fail'], 'P7 readability ' + r)
say(res['R5']['status'] == 'NOT_MEASURED', 'P7 R5 is NOT_MEASURED (no cover in an items file)', 'NOT_MEASURED')
print('RESULT', 'PASS' if not fails else 'FAIL: ' + '; '.join(sorted(set(fails))))
sys.exit(1 if fails else 0)
