#!/usr/bin/env python3
"""SEN0401 midterm items report, version 1.0.0 (new file). Prints, and writes to sen0401_exam_items_midterm_report_v1_0_0.json, the measured facts about
sen0401_exam_items_midterm_v1_0_0.json: chapters, types, Bloom levels (with the counts at Apply or above and at Analyze or above), kinds, the critical points tested and not tested
(named by label), the share of items with a seed, and the seed table (each seed's stem). Read only: it edits nothing but its own output file. A point is 'tested' when an item lists it."""
import collections, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_similarity_v1_1_0 as S

doc = json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_v1_0_0.json'), encoding='utf8')); items = doc['items']
units = lambda i: len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1
cp = E.cp_index()
rep = {}
rep['items'] = len(items); rep['units'] = sum(units(i) for i in items)
rep['units_per_primary_chapter'] = dict(sorted(collections.Counter(i['chapters'][0] for i in items for _ in range(units(i))).items()))
rep['items_naming_chapter'] = {c: sum(1 for i in items if c in i['chapters']) for c in range(1, 7)}
rep['types_items'] = dict(collections.Counter(i['type'] for i in items))
rep['types_units'] = dict(collections.Counter({t: sum(units(i) for i in items if i['type'] == t) for t in {i['type'] for i in items}}))
rep['bloom_units'] = {b: sum(units(i) for i in items if i['bloom'] == b) for b in range(1, 7)}
rep['at_apply_or_above'] = sum(units(i) for i in items if i['bloom'] >= 3)
rep['at_analyze_or_above'] = sum(units(i) for i in items if i['bloom'] >= 4)
rep['kinds_units'] = dict(collections.Counter({k: sum(units(i) for i in items if i['kind'] == k) for k in ('direct', 'synthesis')}))
rep['with_seed_items'] = sum(1 for i in items if i.get('seeds')); rep['without_seed_items'] = [i['key'] for i in items if not i.get('seeds')]
rep['with_seed_units'] = sum(units(i) for i in items if i.get('seeds'))
rep['seed_links'] = sum(len(i.get('seeds', [])) for i in items); rep['distinct_seed_items'] = len({s for i in items for s in i.get('seeds', [])})
rep['enhancements'] = dict(collections.Counter(e for i in items for e in i['enhancements']))
tested = collections.defaultdict(list)
for i in items:
    for c in i['critical_points']: tested[c].append(i['key'])
rep['points_in_list_A_chapters_1_to_6'] = sum(1 for p in cp.values() if p['chapter'] <= 6)
rep['points_tested'] = {c: dict(label=cp[c]['point'], chapter=cp[c]['chapter'], items=v) for c, v in sorted(tested.items())}
rep['points_not_tested'] = {c: dict(label=p['point'], chapter=p['chapter']) for c, p in sorted(cp.items()) if p['chapter'] <= 6 and c not in tested}
pages = {p['ref']: p for p in S.page_items((1, 2, 3, 4, 5, 6))}
def stem_of(ref):
    n, idx = ref.split('#'); ch = int(n[2:4]); idx = int(idx)
    f = S.newest_bank(ch) if 'question_bank' in n else os.path.join(S.TOOL, 'ch%02d-page' % ch, 'quiz_v1_0_0.json')
    d = json.load(open(f, encoding='utf8')); d = d if isinstance(d, list) else d['items']
    return d[idx]['q'].split('\n')[0]
rep['seed_table'] = {i['key']: [dict(seed=s, stem=stem_of(s)) for s in i.get('seeds', [])] or i['no_seed_reason'] for i in items}
json.dump(rep, open(os.path.join(HERE, 'sen0401_exam_items_midterm_report_v1_0_0.json'), 'w', encoding='utf8'), indent=1, ensure_ascii=False)

print('MIDTERM ITEMS REPORT (chapters 1 to 6, 4 items per chapter, 24 items; the builder and the check are separate files)')
print('items %d, units %d (a fill-in blank counts as one)' % (rep['items'], rep['units']))
print('chapters (units by primary chapter):', rep['units_per_primary_chapter'], ' items that name the chapter:', rep['items_naming_chapter'])
print('types (items):', rep['types_items'], ' (units):', rep['types_units'])
print('Bloom levels (units):', rep['bloom_units'])
print('AT APPLY OR ABOVE: %d of %d   AT ANALYZE OR ABOVE: %d of %d' % (rep['at_apply_or_above'], rep['units'], rep['at_analyze_or_above'], rep['units']))
print('kinds (units):', rep['kinds_units'])
print('items with a seed: %d of %d items (%d of %d units); seed links %d, distinct seed items %d; without a seed: %s' % (
    rep['with_seed_items'], rep['items'], rep['with_seed_units'], rep['units'], rep['seed_links'], rep['distinct_seed_items'], rep['without_seed_items']))
print('enhancements used (count of items):', rep['enhancements'])
print('CRITICAL POINTS TESTED: %d of %d points of list A (chapters 1 to 6)' % (len(rep['points_tested']), rep['points_in_list_A_chapters_1_to_6']))
for c, v in rep['points_tested'].items(): print('  TESTED  %s [%s]: %s' % (c, ', '.join(k.split(':')[1] for k in v['items']), v['label']))
print('CRITICAL POINTS NOT TESTED: %d' % len(rep['points_not_tested']))
for c, v in rep['points_not_tested'].items(): print('  NOT     %s: %s' % (c, v['label']))
