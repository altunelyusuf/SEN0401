#!/usr/bin/env python3
"""SEN0401 exam v7 real-shape probe, version 1.0.0 (new file). Holds no question and no answer.
Runs the papers library v7.0.0 on a REAL structure and items pair IN MEMORY ONLY (no file is written, LibreOffice is not run) and prints COUNTS and pass/fail only, never any text of an item: it shows that every field shape of the real files is read,
that every slot builds its paragraphs (tips of at most 12 words, answer-format lines), that the key is built, that a perfect sheet scores 100 and that the exact blind figure equals the figure the structure file states.
Usage: probe.py --structure STRUCTURE.json   (the items file sits beside it, as the library resolves it)"""
import argparse, io, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_paper_lib_v7_0_0 as L
import sen0401_exam_scoring_rows_v1_0_0 as SR
ap = argparse.ArgumentParser(); ap.add_argument('--structure', required=True); a = ap.parse_args()
st = json.load(open(a.structure)); L.set_cfg('compact10')
paper = L.make_form(1, 5701, structure_path=a.structure)
n_blocks = 0; tips = []; kinds = {}
for i, s in enumerate(paper['slots']):
    bl = L.slot_blocks(s, paper, first_of_question=True); n_blocks += len(bl); kinds[s['type']] = kinds.get(s['type'], 0) + 1
    t = L.tip_of(s['item'])
    if t: tips.append(len(t[5:].split()))
buf = io.BytesIO(); L.write_docx(paper, buf, breaks=[]); docx_bytes = len(buf.getvalue())
key = L.answer_key(paper); sc = key['scoring']
print('structure version %s, synthetic %s; sub-questions %d, units %d, points %s' % (st.get('version'), st.get('synthetic', False), len(paper['slots']), sum(L.units(i) for i in paper['items']), key['total_points']))
print('slot kinds', kinds, '; paragraphs built', n_blocks, '; in-memory .docx bytes', docx_bytes)
print('tips: %d, longest %d words (limit 12)' % (len(tips), max(tips or [0])))
print('perfect sheet %s of %s ; exact blind total %s = %.6f' % (sc['perfect_sheet_total'], sc['max_total'], sc['blind_total_exact'], sc['blind_total_exact_decimal']))
bt = st.get('blind_total_exact')
if bt:
    from fractions import Fraction as F
    same = F(sc['blind_total_exact']) == F(bt['fraction'])
    print('the structure file states %s: %s' % (bt['fraction'], 'EQUAL to the key figure' if same else 'DIFFERENT from the key figure'))
    sys.exit(0 if same and sc['perfect_sheet_total'] == 100.0 else 1)
sys.exit(0 if sc['perfect_sheet_total'] == 100.0 else 1)
