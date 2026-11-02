#!/usr/bin/env python3
"""SEN0401 exam items v1.4.0 part A (question 1, seven choice sub-questions): builder, version 1.0.0 (new file).

This script holds NO question text and NO answer. It assembles the part-A file from
  - the committed items v1.3.0 (read only): the two kept items mt2:i02 and mt2:i05 are copied byte-for-byte (as parsed JSON),
  - the private spec (08-tooling/exam/private/sen0401_exam_items5a_spec_v1_0_0.json): the five new items.
It composes each new stem from its parts (body, 'Tips: term: meaning; ...', question), fills the schema fields of items v1.3.0,
and evaluates every arithmetic claim of the spec ('calc': [expression, expected]) with a program; a mismatch stops the build (exit 1).
It refuses to overwrite and refuses any output path outside 08-tooling/exam/private/ (leak guard: the repository is public).

Usage: sen0401_exam_items5a_build_v1_0_0.py [--spec FILE] [--out FILE]
Output (default): 08-tooling/exam/private/sen0401_exam_items5a_v1_0_0.json
"""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PRIV = os.path.join(HERE, 'private')
SRC = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_3_0.json')
SPEC = os.path.join(PRIV, 'sen0401_exam_items5a_spec_v1_0_0.json')
OUT = os.path.join(PRIV, 'sen0401_exam_items5a_v1_0_0.json')
if '--spec' in sys.argv: SPEC = sys.argv[sys.argv.index('--spec') + 1]
if '--out' in sys.argv: OUT = sys.argv[sys.argv.index('--out') + 1]


def stem(body, tips, ask):
    t = 'Tips: ' + '; '.join('%s: %s' % (a, b) for a, b in tips) + '.'
    return ' '.join((body, t, ask))


def main():
    if os.path.commonpath([os.path.abspath(OUT), PRIV]) != PRIV:
        print('REFUSED: the output must lie in 08-tooling/exam/private/ (leak guard)'); return 2
    if os.path.exists(OUT):
        print('REFUSED: %s exists (new files only)' % OUT); return 2
    base = {i['key']: i for i in json.load(open(SRC, encoding='utf8'))['items']}
    spec = json.load(open(SPEC, encoding='utf8'))
    new = {n['key']: n for n in spec['new_items']}
    items = []; slots = []
    for s in spec['slots']:
        if 'keep' in s:
            it = json.loads(json.dumps(base[s['keep']])); key = s['keep']
        else:
            n = new[s['new']]; key = n['key']
            for expr, expect in n['calc']:
                got = eval(expr, {'__builtins__': {}}, {})
                if got != expect:
                    print('FAIL calc %s: %r gives %r, expected %r' % (key, expr, got, expect)); return 1
            it = {
                'key': key, 'type': n['type'], 'chapters': n['chapters'], 'bloom': n['bloom'], 'kind': n['kind'],
                'source': n['source'], 'sources': n['sources'], 'critical_points': n['critical_points'],
                'seeds': [], 'no_seed_reason': n['no_seed_reason'], 'enhancements': n['enhancements'],
                'papers': ['midterm'], 'from_item': [], 'replaces': s['replaces'],
                'q': stem(n['q_body'], n['tips'], n['q_ask']), 'options': n['options'], 'answer': n['answer'],
                'tips': n['tips'], 'terms': n['terms'], 'computed': n['computed'], 'abbreviations': {},
                'understanding': n['understanding'], 'owner_points': n['owner_points'], 'sub_question': s['sub'],
            }
            if n.get('provisional'):
                it['provisional'] = True; it['provisional_reason'] = n['provisional_reason']
        items.append(it)
        slots.append({'sub': s['sub'], 'item': key, 'points': s['points'], 'kept': 'keep' in s, 'replaces': s.get('replaces', [])})
    doc = {'note': 'SEN0401 midterm items v1.4.0 part A (question 1), built by sen0401_exam_items5a_build_v1_0_0.py from items v1.3.0 (two items kept unchanged) and the private spec (five new items). One form only. PRIVATE: never commit.',
           'version': '1.0.0', 'part': 'A', 'chapters': [1, 2, 3, 4, 5, 6], 'slots': slots, 'items': items}
    with open(OUT, 'w', encoding='utf8') as f: json.dump(doc, f, ensure_ascii=False, indent=1)
    print('WROTE %s (%d items, %d new, %d kept)' % (OUT, len(items), sum(1 for s in slots if not s['kept']), sum(1 for s in slots if s['kept'])))
    return 0


if __name__ == '__main__': sys.exit(main())
