"""Builds the critical-points files (json and a plain markdown list) from the data file. Version 1.0.0.
New files only. Usage: build.py [--out DIR]   Reads the decks; never writes one."""
import sys
sys.dont_write_bytecode = True
import glob, json, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_exam_pptx_text_v1_0_0 as L
import sen0401_exam_critical_points_data_v1_0_0 as D

sys.dont_write_bytecode = True
VER = '1_0_0'
HERE = os.path.dirname(os.path.abspath(__file__))
BASIS = {'Q': 'chapter question answered in the summary', 'SUM': 'line of the deck summary', 'LES': 'lesson line of a true story',
         'EMP': 'speaker note or slide sets the point apart', 'EXAM': 'deck says the exam builds on it',
         'OWN25': "owner's 2025 deck titles it most important", 'PAGE': 'course page discussion item'}


def newest_page(ch):
    fs = glob.glob(L.MAT + 'ch%02d/page/sen0401_ch%02d_page_v*.html' % (ch, ch))
    key = lambda p: tuple(int(x) for x in re.search(r'_v(\d+)_(\d+)_(\d+)\.html$', p).groups())
    return sorted([f for f in fs if re.search(r'_v\d+_\d+_\d+\.html$', f)], key=key)[-1]


def main():
    out = HERE
    pts = []
    count = {}
    for (ch, basis, text, slide, field, quote) in D.A:
        count[ch] = count.get(ch, 0) + 1
        if field in ('slide', 'notes'):
            f = L.newest_deck(ch)
            src = {'kind': 'deck', 'file': os.path.relpath(f, L.ROOT), 'slide': slide, 'field': field, 'quote': quote}
        elif field == 'legacy':
            leg = sorted(glob.glob(L.LEG + 'Chapter_%d_*.pptx' % ch))[0]
            src = {'kind': 'legacy2025', 'file': os.path.relpath(leg, L.ROOT), 'slide': slide, 'field': 'diagram', 'quote': quote}
        else:
            f = newest_page(ch)
            src = {'kind': 'page', 'file': os.path.relpath(f, L.ROOT), 'slide': None, 'field': 'page', 'quote': quote}
        pts.append({'id': 'CP%d.%02d' % (ch, count[ch]), 'chapter': ch, 'basis': basis,
                    'doubtful': ch == 7, 'point': text, 'source': src})
    doc = {'version': VER.replace('_', '.'), 'default_chapters': [1, 2, 3, 4, 5, 6], 'selectable_chapters': [7],
           'basis_codes': BASIS,
           'list_A_points_carried_by_a_source': pts,
           'list_B_not_carried_for_the_owner': [{'id': i, 'chapters': c, 'gap': g, 'asked_of_owner': q} for (i, c, g, q) in D.B]}
    jp = os.path.join(out, 'sen0401_exam_critical_points_v%s.json' % VER)
    json.dump(doc, open(jp, 'w'), indent=1, ensure_ascii=False)
    # plain list
    md = ['# SEN0401 critical points of the exam chapters, version 1.0.0', '',
          'Chapters are a parameter: default 1 to 6; chapter 7 is doubtful and selectable.',
          'A point is listed in A only when a source carries it; the source is named. List B is separate.', '',
          '## A. Points carried by a source', '']
    for ch in range(1, 8):
        md.append('### Chapter %d%s' % (ch, ' (doubtful)' if ch == 7 else ''))
        for p in [p for p in pts if p['chapter'] == ch]:
            s = p['source']
            where = ('%s, slide %s, %s' % (os.path.basename(s['file']), s['slide'], s['field'])) if s['slide'] else os.path.basename(s['file'])
            md.append('- %s [%s] %s  (source: %s)' % (p['id'], p['basis'], p['point'], where))
        md.append('')
    md += ['Basis codes: ' + '; '.join('%s = %s' % kv for kv in BASIS.items()), '',
           '## B. What no source carries (for the owner)', '']
    for (i, c, g, q) in D.B:
        md.append('- %s (chapters %s): %s  ASKED OF THE OWNER: %s' % (i, c, g, q))
    open(os.path.join(out, 'sen0401_exam_critical_points_v%s.md' % VER), 'w').write('\n'.join(md) + '\n')
    print('wrote', jp, len(pts), 'points')


main()
