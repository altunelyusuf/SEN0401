#!/usr/bin/env python3
"""SEN0401 exam key-only rebuild, version 7.2.2 (new file). Holds no question and no answer.
Rebuilds ONLY the key (docx, pdf, json) of the set v7_2_0 with the key writer of lib v7_2_2 (letters of the worked solutions mapped to the printed paper letters; PROVISIONAL once).
The paper is re-created in memory with the same seed and the same recorded order (measure.json), never written; paper, sheet, ttl, layout and measure are COPIED byte for byte into the new folder.
Usage: key_rebuild.py SRC_DIR OUT_DIR --tag TAG --structure STRUCT --seed 5701   (refuses to overwrite)"""
import argparse, hashlib, json, os, shutil, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_exam_paper_lib_v7_2_2 as L
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('--tag', required=True); ap.add_argument('--structure', required=True); ap.add_argument('--seed', type=int, default=5701); x = ap.parse_args()
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
meas = json.load(open(os.path.join(x.src, x.tag + '_measure.json')))
L.set_cfg(meas['config'])
want = [o[1] for o in meas['order']]
paper = L.make_form(1, x.seed, accept=lambda o: [s['skey'] for s in o] == want, structure_path=os.path.abspath(x.structure))
assert [('%d%s' % (s['q'], s['label']), s['skey'], s['type']) for s in paper['slots']] == [tuple(o) for o in meas['order']], 'the order differs from the recorded order'
assert paper['form']['code'] == '70017', paper['form']['code']
paper['contentPages'] = meas['paper_pages']; paper['sheetPages'] = meas['sheet_pages']; paper['pageCount'] = meas['pages_total']
key = L.answer_key(paper); key.update(paper_file=x.tag + '_paper.docx', sheet_file=x.tag + '_sheet.pdf')
old = json.load(open(os.path.join(x.src, x.tag + '_key.json')))
assert json.dumps(key, sort_keys=True, ensure_ascii=False) == json.dumps(old, sort_keys=True, ensure_ascii=False), 'the rebuilt key.json differs from the committed key.json'
print('rebuilt key.json equals the committed key.json (same places, same letters, same scoring)')
os.makedirs(x.out, exist_ok=True)
for ext in ('_key.docx', '_key.pdf', '_key.json', '_paper.docx', '_paper.pdf', '_paper.ttl', '_sheet.pdf', '_sheet_layout.json', '_measure.json'):
    if os.path.exists(os.path.join(x.out, x.tag + ext)): raise SystemExit('REFUSED: ' + x.tag + ext + ' exists')
tmp = tempfile.mkdtemp()
try:
    L.write_key_docx(paper, key, os.path.join(tmp, x.tag + '_key.docx'), note='Key letters mapped to the printed paper (tooling v7.2.2).')
    L.export_pdf(os.path.join(tmp, x.tag + '_key.docx'), tmp)
    json.dump(key, open(os.path.join(tmp, x.tag + '_key.json'), 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    for ext in ('_key.docx', '_key.pdf', '_key.json'): shutil.copy(os.path.join(tmp, x.tag + ext), os.path.join(x.out, x.tag + ext))
finally: shutil.rmtree(tmp, ignore_errors=True)
for ext in ('_paper.docx', '_paper.pdf', '_paper.ttl', '_sheet.pdf', '_sheet_layout.json', '_measure.json'):
    shutil.copyfile(os.path.join(x.src, x.tag + ext), os.path.join(x.out, x.tag + ext))
    assert sha(os.path.join(x.src, x.tag + ext)) == sha(os.path.join(x.out, x.tag + ext))
print('key rebuilt; paper, sheet, ttl, layout, measure copied byte for byte into', x.out, '; key pages', L.pdf_pages(os.path.join(x.out, x.tag + '_key.pdf')))
