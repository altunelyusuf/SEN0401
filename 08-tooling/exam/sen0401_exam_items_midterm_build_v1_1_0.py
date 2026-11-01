#!/usr/bin/env python3
"""SEN0401 midterm items, builder of version 1.1.0 (new file). Reads the committed items v1.0.0 (never edited) and writes items v1.1.0 plus a change report.
THE ONLY CHANGE: item mt1:i20:trace-compactsize. v1.0.0 used the function cs_encode without defining it. v1.1.0 defines it inside the question in one line, as the
standard CompactSize sizes (Mastering Bitcoin ch. 6, slide 20 of the chapter 6 deck): a count below 253 takes 1 byte, up to 65535 takes 3 bytes, up to 4294967295 takes 5 bytes,
anything larger takes 9 bytes. The code, the output 14, the chapter, the Bloom level, the options and the computed value stay.
NO ITEM IS SHORTENED: the page budget (3 Word pages) is reached by the font (Arial / Liberation Sans) and the layout alone, measured by the paper builder v2.0.0; a shortened item would be a change
to the owner's seed items that nothing requires.
The answer 14 is checked here on a REAL implementation of CompactSize (bytes written as a Bitcoin transaction writes them), and the one-line definition is checked against that implementation
on the edges 0, 252, 253, 65535, 65536, 4294967295, 4294967296.
Usage: build_v1_1_0.py [--outdir DIR]   (default: this folder; refuses to overwrite)"""
import json, os, sys, io, contextlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_0_0.json')
OUT = os.path.abspath(sys.argv[sys.argv.index('--outdir') + 1]) if '--outdir' in sys.argv else HERE
KEY = 'mt1:i20:trace-compactsize'
OLD_SENT = 'The function cs_encode writes a count as a transaction does (the CompactSize encoding of the chapter). '
NEW_SENT = ('The function cs_encode writes a count in the CompactSize encoding: a count below 253 takes 1 byte, up to 65535 takes 3 bytes, up to 4294967295 takes 5 bytes, '
            'anything larger takes 9 bytes. ')


def cs_real(n):
    """CompactSize as a Bitcoin transaction writes it (Mastering Bitcoin ch. 6): the real encoder, not the one-line summary."""
    if n < 0xfd: return n.to_bytes(1, 'little')
    if n <= 0xffff: return b'\xfd' + n.to_bytes(2, 'little')
    if n <= 0xffffffff: return b'\xfe' + n.to_bytes(4, 'little')
    return b'\xff' + n.to_bytes(8, 'little')


def cs_stated(n):
    """The sizes exactly as the question states them (below 253: 1; up to 65535: 3; up to 4294967295: 5; larger: 9)."""
    return 1 if n < 253 else 3 if n <= 65535 else 5 if n <= 4294967295 else 9


def run(code, ns):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code, '<item>', 'exec'), dict(ns))
    return buf.getvalue().strip()


doc = json.load(open(SRC, encoding='utf8'))
new = json.loads(json.dumps(doc)); rep = []
it = next(i for i in new['items'] if i['key'] == KEY); old = next(i for i in doc['items'] if i['key'] == KEY)
assert it['q'].startswith(OLD_SENT)
it['q'] = NEW_SENT + it['q'][len(OLD_SENT):]
new['version'] = '1.1.0'
new['note'] = doc['note'].replace('version 1.0.0', 'version 1.1.0 (derived from v1.0.0 by sen0401_exam_items_midterm_build_v1_1_0.py: only item ' + KEY + ' changed, cs_encode is defined in its question)').replace('builder sen0401_exam_items_midterm_build_v1_0_0.py', 'builder of v1.0.0 sen0401_exam_items_midterm_build_v1_0_0.py')
lines = []
edges = [0, 252, 253, 65535, 65536, 4294967295, 4294967296]
lines.append('CHECK the one-line definition against the real CompactSize encoder on the edges %s: real %s stated %s' % (edges, [len(cs_real(n)) for n in edges], [cs_stated(n) for n in edges]))
assert [len(cs_real(n)) for n in edges] == [cs_stated(n) for n in edges] == [1, 1, 3, 3, 5, 5, 9]
got_real = run(it['code'], {'cs_encode': lambda n: cs_real(n)}); got_stated = run(it['code'], {'cs_encode': lambda n: b'x' * cs_stated(n)})
lines.append('CHECK the listing run with the REAL encoder prints %s; with the stated sizes prints %s; the key is %s' % (got_real, got_stated, it['output']))
assert got_real == got_stated == it['output'] == '14'
longest = max(len(l) for l in it['code'].split('\n'))
lines.append('CHECK code listing unchanged: %s; longest line %d characters (limit 45), %d lines (limit 12)' % (it['code'] == old['code'], longest, len(it['code'].split('\n'))))
assert it['code'] == old['code'] and longest <= 45
for f in ('chapters', 'bloom', 'output', 'computed', 'kind', 'type', 'terms', 'papers', 'enhancements'): assert it[f] == old[f], f
lines.append('ITEM CHANGED %s (chapter %s, Bloom %d, answer %s, computed %s: all unchanged)' % (KEY, it['chapters'], it['bloom'], it['output'], it['computed']))
lines.append('  BEFORE (%d characters): %s' % (len(old['q']), old['q']))
lines.append('  AFTER  (%d characters): %s' % (len(it['q']), it['q']))
lines.append('  CHARACTERS SAVED: %d (negative = the definition adds %d characters)' % (len(old['q']) - len(it['q']), len(it['q']) - len(old['q'])))
same = [i['key'] for i, j in zip(new['items'], doc['items']) if i == j]
lines.append('ITEMS UNCHANGED: %d of %d (no item is shortened: the 3-page budget is reached by font and layout, see the paper builder v2.0.0 measurement)' % (len(same), len(doc['items'])))
out = os.path.join(OUT, 'sen0401_exam_items_midterm_v1_1_0.json'); rp = os.path.join(OUT, 'sen0401_exam_items_midterm_report_v1_1_0.txt')
for p in (out, rp):
    if os.path.exists(p): sys.exit('refusing to overwrite ' + p)
json.dump(new, open(out, 'w', encoding='utf8'), indent=1, ensure_ascii=False); open(rp, 'w', encoding='utf8').write('\n'.join(lines) + '\n')
print('\n'.join(lines)); print('wrote', out)
