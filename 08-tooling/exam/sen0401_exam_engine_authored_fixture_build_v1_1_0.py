"""Builds the synthetic authored-items fixture of engine v1.1.0 (sen0401_exam_engine_fixture_authored_v1_1_0.json). New file.
FIXTURE ITEMS ONLY: every text begins with FIXTURE, none is exam content, none is meant to be given to a student. They exist so that the engine and its rules can be run end to end
(24 items per paper, chapters 1 to 6, every item type of the paper rules) without any real question. Seed links point at real page items and critical-point links at real points, so
that EN12 resolves them; the texts are unrelated to those items, so EN11 must not fire."""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_similarity_v1_0_0 as S
cp = json.load(open(os.path.join(HERE, 'sen0401_exam_critical_points_v1_0_0.json'), encoding='utf8'))['list_A_points_carried_by_a_source']
pg = S.page_items()
def seed(c): return [p['ref'] for p in pg if p['chapter'] == c and p['source'] == 'bank'][:1]
def points(c): return [p['id'] for p in cp if p['chapter'] == c][:2]
SRC = dict(file='FIXTURE source', locator='FIXTURE')
items = []
BL = [2, 3, 3, 4, 4, 4, 3, 4, 3, 2]   # the ceilings of the paper types: choice 4, matching 3, ordering 3, fill-in 2, number 3, trace 4
def common(key, typ, chs, bloom, c, k, papers=None, kind='direct'):
    d = dict(key=key, type=typ, chapters=chs, bloom=bloom, kind=kind, source=SRC, critical_points=points(c))
    if k % 5 == 4: d['no_seed_reason'] = 'FIXTURE: written without a seed'
    else: d['seeds'] = seed(c)
    if papers: d['papers'] = papers
    return d
for c in range(1, 8):          # chapter 7 is selectable; its fixture items enter a paper only when the chapter list holds 7
    for n in range(10):
        d = common('fx:c%d:choice%d' % (c, n), 'ChoiceFour', [c], BL[n], c, n)
        d.update(q='FIXTURE chapter %d choice item %d asks which statement about fixture subject %d.%d is the one that holds' % (c, n, c, n),
                 options=['FIXTURE c%d n%d first statement alpha' % (c, n), 'FIXTURE c%d n%d second statement beta' % (c, n), 'FIXTURE c%d n%d third statement gamma' % (c, n), 'FIXTURE c%d n%d fourth statement delta' % (c, n)], answer=n % 4)
        items.append(d)
    # a code choice item in every chapter
    d = common('fx:c%d:codechoice' % c, 'ChoiceFourCode', [c], 4, c, 3)
    d.update(q='FIXTURE chapter %d code item: what does the fixture listing show' % c, code='FIXTURE_x = %d\nFIXTURE_y = FIXTURE_x + %d' % (c, c + 1),
             options=['FIXTURE c%d code option %d' % (c, k) for k in range(4)], answer=1); items.append(d)
for tag, paper in (('m', 'midterm'), ('k', 'makeup')):
    items.append(dict(common('fx:%s:fill' % tag, 'FillBlankGroup', [1], 2, 1, 1, [paper]), blanks=[dict(text='FIXTURE %s sentence %d has the blank ____ for its word.' % (tag, k), answer='FIXTURE %s answer %s' % (tag, w)) for k, w in enumerate(['alpha', 'beta', 'gamma'])],
                      distractors=['FIXTURE %s spare one' % tag, 'FIXTURE %s spare two' % tag]))
    items.append(dict(common('fx:%s:order2' % tag, 'Ordering', [2], 3, 2, 2, [paper]), steps=['FIXTURE %s step %d of the fixture procedure' % (tag, k) for k in range(1, 5)]))
    items.append(dict(common('fx:%s:match' % tag, 'Matching', [3, 4], 3, 3, 2, [paper], 'synthesis'),
                      premises=[dict(text='FIXTURE %s premise %d from the fixture subjects' % (tag, k), match='FIXTURE %s response %s' % (tag, 'ABCD'[k])) for k in range(4)],
                      responses=['FIXTURE %s response %s' % (tag, x) for x in 'ABCDEF']))
    items.append(dict(common('fx:%s:num' % tag, 'NumericAnswer', [4], 3, 4, 2, [paper]), q='FIXTURE %s number item: give the fixture quantity' % tag, key_value=(50 if tag == 'm' else 60), unit='FIXTURE unit', tolerance=0))
    items.append(dict(common('fx:%s:trace' % tag, 'CodeTrace', [5], 4, 5, 2, [paper]), q='FIXTURE %s trace item: what does the fixture listing print' % tag, code='FIXTURE_a = %d\nprint(FIXTURE_a * 2)' % (7 if tag == 'm' else 9), output=str(14 if tag == 'm' else 18)))
    items.append(dict(common('fx:%s:order6' % tag, 'Ordering', [6], 3, 6, 2, [paper]), steps=['FIXTURE %s sixth-chapter step %d of the procedure' % (tag, k) for k in range(1, 5)]))
json.dump(dict(note='Synthetic fixture items only (text marked FIXTURE); not exam content; for the run of the engine and its rules. Built by sen0401_exam_engine_authored_fixture_build_v1_1_0.py.', items=items),
          open(os.path.join(HERE, 'sen0401_exam_engine_fixture_authored_v1_1_0.json'), 'w', encoding='utf8'), indent=1, ensure_ascii=False)
print('authored fixture items', len(items))
