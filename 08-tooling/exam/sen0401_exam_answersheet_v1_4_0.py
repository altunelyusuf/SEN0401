"""Answer sheet reader of record, version 1.4.0 (new file, a copy of sen0401_exam_answersheet_v1_3_0.py, which stays unchanged; built on v1.2.0, which is imported UNCHANGED together with v1.1.0 and v1.0.0). Pure library (no output when imported).
WHAT IS NEW (owner redesign of 2026-11-02, ruling 5): the answer sheet of the papers v7 is ONE page with choice-type answers only (five alternatives per place). The reader reads page 1, and ONLY page 1:
  * read_sheet_v7(imgs, layout): a layout that names any reader page other than page 1, or has more than one page, is refused (ValueError); only imgs[0] is looked at.
  * provisional(out): turns a reading into PROVISIONAL marks for the marker. The question pages are the legal copy; the sheet is for fast reading; where the two differ the question pages count.
    A row the reader flagged (double, faint, held-block, incomplete) or left blank gives no mark (None): a person looks.
  * read_pdf(pdf, layout, workdir): rasterises the sheet, registers page 1 on its four corner marks and returns the reading (None when the registration fails).
The reading itself, its thresholds, its holds and its flags are the v1.2.0 ones: read_sheet is v1.2.0's function, not a rewrite; no gate is changed."""
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v1_2_0 as R2
from sen0401_exam_answersheet_v1_2_0 import *            # every v1.0.0, v1.1.0 and v1.2.0 name stays available unchanged (thresholds, read_row, classify ...)
VERSION = '1.4.0'
STATUS = 'provisional'
LEGAL_COPY = 'question pages'


def read_sheet_v7(imgs, layout, check_digits=True, closure=True):
    """Same contract as v1.2.0's read_sheet: (out, blockstate, held). Page 1 only."""
    rp = layout.get('reader_pages', [0])
    if rp != [0] or layout.get('pages', 1) != 1 or any(b['page'] != 0 for b in layout['blocks']):
        raise ValueError('the reader v1.4.0 reads the one-page sheet (page 1 only); this layout names reader pages %s and %s page(s)' % (rp, layout.get('pages')))
    return R2.read_sheet([imgs[0]], layout, check_digits, closure)


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
    im = np.array(Image.open(pngs[0]).convert('L'))
    reg = register(im, layout, 0)
    if reg is None: return None
    out, bst, held = read_sheet_v7([reg], layout)
    return dict(reader_version=VERSION, status=STATUS, legal_copy=LEGAL_COPY, marks=provisional(out, held), held_blocks=held, pages_read=[0])
