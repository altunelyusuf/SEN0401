"""Answer sheet reader of record, version 1.3.0 (new file, built on v1.2.0, which is imported UNCHANGED together with v1.1.0 and v1.0.0). Pure library (no output when imported).
WHAT IS NEW (owner points 2 and 5 of 2026-11-02): the answer sheet of the papers v6 has TWO pages. Page 1 holds the answer boxes (read as before, on the registration marks); page 2 is the tips page and is NEVER read.
The reading itself, its thresholds, its holds and its flags are the v1.2.0 ones: read_sheet is v1.2.0's function, not a rewrite; no gate is changed. What this file adds:
  * read_sheet_v6(imgs, layout): reads only the pages named in layout['reader_pages'] (page 1); any other page image is not looked at, and ink on it (or on the answer lines of the bonus parts, which are not blocks) cannot change a reading.
  * provisional(out, held): turns a reading into PROVISIONAL marks for the marker. The question pages are the legal copy; the sheet is an option for fast reading; where the two differ the question pages count (resolve() of sen0401_exam_scoring_v1_0_0.py applies the rule).
    A row the reader flagged (double, faint, held-block, check-digit, incomplete) or left blank gives no mark (None): a person looks. A number box gives only 'WRITTEN' (the reader does not read digits): the marker reads the number, so no mark is given for it.
  * read_pdf(pdf, layout, workdir): rasterises the sheet, registers page 1 on its four corner marks and returns the reading (None when the registration fails)."""
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v1_2_0 as R2
from sen0401_exam_answersheet_v1_2_0 import *            # every v1.0.0, v1.1.0 and v1.2.0 name stays available unchanged (thresholds, read_row, classify ...)
VERSION = '1.3.0'
STATUS = 'provisional'
LEGAL_COPY = 'question pages'


def read_sheet_v6(imgs, layout, check_digits=True, closure=True):
    """Same contract as v1.2.0's read_sheet: (out, blockstate, held). Only the reader pages are used."""
    rp = layout.get('reader_pages', sorted({b['page'] for b in layout['blocks']}))
    bad = [b['id'] for b in layout['blocks'] if b['page'] not in rp]
    if bad: raise ValueError('blocks %s lie on a page the reader does not read' % bad)
    sel = [imgs[p] if p in rp else None for p in range(max(rp) + 1)]
    return R2.read_sheet(sel, layout, check_digits, closure)


def provisional(out, held=()):
    """{label: {'mark': value or None, 'flag': flag or None, 'status': 'provisional', 'legal_copy': 'question pages'}}."""
    res = {}
    for no, r in out.items():
        v = r['value']
        mark = None if (v is None or v == 'WRITTEN' or r['flag'] not in (None,)) else v
        res[no] = {'mark': mark, 'flag': r['flag'], 'status': STATUS, 'legal_copy': LEGAL_COPY}
    return res


def read_pdf(pdf, layout, workdir):
    import numpy as np
    from PIL import Image
    pngs = rasterise(pdf, os.path.join(workdir, 'pg'))
    rp = layout.get('reader_pages', [0])
    imgs = [np.array(Image.open(pngs[p]).convert('L')) if p in rp else None for p in range(max(rp) + 1)]
    reg = [register(im, layout, p) if im is not None else None for p, im in enumerate(imgs)]
    if any(reg[p] is None for p in rp): return None
    out, bst, held = read_sheet_v6(reg, layout)
    return dict(reader_version=VERSION, status=STATUS, legal_copy=LEGAL_COPY, marks=provisional(out, held), held_blocks=held, pages_read=rp)
