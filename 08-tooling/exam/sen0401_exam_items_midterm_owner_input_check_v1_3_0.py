#!/usr/bin/env python3
"""Owner input check for the midterm items v1.3.0 (new file). Reads the NEWEST sen0401_exam_owner_topics_v*.json and tests that the committed items v1.3.0, the topic map and the new-points map
(built when the newest owner file was v1.0.0) still answer it: same cases, same kept items, same nine topics, and every point A-F of the newest file has a row. Prints the coverage T1-T9 and A-F
as the item key that covers it or GAP. Exit 0 only when no line is FAIL."""
import glob, importlib.util, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
fs = sorted(glob.glob(os.path.join(HERE, 'sen0401_exam_owner_topics_v*.json')), key=lambda p: tuple(int(x) for x in re.search(r'_v(\d+)_(\d+)_(\d+)\.json$', p).groups()))
new = json.load(open(fs[-1], encoding='utf8')); first = json.load(open(fs[0], encoding='utf8'))
items = {i['key']: i for i in json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_v1_3_0.json'), encoding='utf8'))['items']}
tm = json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_topic_map_v1_3_0.json'), encoding='utf8'))
spec = importlib.util.spec_from_file_location('b13', os.path.join(HERE, 'sen0401_exam_items_midterm_build_v1_3_0.py')); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
fails = []
def say(ok, name, d=''):
    print('%-5s %s %s' % ('PASS' if ok else 'FAIL', name, d))
    if not ok: fails.append(name)
say(True, 'newest owner file', '%s (version %s; files found: %s)' % (os.path.basename(fs[-1]), new['version'], [os.path.basename(f) for f in fs]))
say(new['cases'] == first['cases'] and new['topics'] == first['topics'] and new['kept_by_the_lineage_agent'] == first['kept_by_the_lineage_agent'], 'cases, nine topics and kept items are the same in the newest file as in the file the topic map was built from (%s)' % tm['owner_topics_file'])
say([t['id'] for t in new['topics']] == [r['id'] for r in tm['rows']], 'every topic of the newest file has a row in the topic map')
say([p['id'] for p in new['points']] == [r['id'] for r in b.POINT_ROWS], 'every point A-F of the newest file has a row in the new-points map', str([p['id'] for p in new['points']]))
say(all(k in items for r in b.POINT_ROWS for k in r['items']) and all(r['item_keys'] == 'GAP' or all(k in items for k in r['item_keys']) for r in tm['rows']), 'every item key named in either map exists in the items file')
print('\nCOVERAGE required by the owner file (item key that covers, or GAP):')
for r in tm['rows']: print('  %s %-62s %-8s %s' % (r['id'], r['topic'], r['verdict'], ', '.join(r['item_keys']) if isinstance(r['item_keys'], list) else 'GAP'))
for r in b.POINT_ROWS: print('  %s %-62s %-8s %s' % (r['id'], r['point'][:62], r['verdict'], ', '.join(r['items']) or 'GAP'))
print('\nRESULT', 'FAIL (%s)' % '; '.join(fails) if fails else 'PASS')
sys.exit(1 if fails else 0)
