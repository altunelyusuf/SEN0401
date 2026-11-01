"""Render check of the exam cover demos (AC9_Exam_Cover): LibreOffice -> PDF, page count, ink inside the margins, required content, abbreviations.
Usage: python3 sen0401_exam_cover_check_v1_0_0.py DEMO.docx [DEMO2.docx ...]   Prints PASS/FAIL per check; exit 1 on any FAIL. Scratch files are removed."""
import os, re, subprocess, sys, tempfile, shutil
import numpy as np
from PIL import Image
DPI = 80
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B, PW, PH = 1134, 1133, 360, 270, 11906, 16838   # twips, from the template's page setup
TOL = 2.0   # pixels at 80 dpi = 0.64 mm (anti-aliasing of a thick border)
# capital-letter words allowed without a spelled-out form: course codes, names, the template's own emphasis words, headings
ALLOWED = {'SEN0401', 'SEN0414', 'ALTUNEL', 'INSTRUCTIONS', 'WARNING', 'ZERO', 'FORBIDDEN', 'ISTANBUL', 'KÜLTÜR', 'UNIVERSITY'}
fails = 0
def res(ok, msg):
    global fails
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok: fails += 1
def check(docx_path, tmp):
    name = os.path.basename(docx_path)
    print('--- ' + name)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, docx_path], capture_output=True, timeout=180)
    pdf = os.path.join(tmp, name[:-5] + '.pdf')
    if not os.path.exists(pdf):
        print('CANNOT_RUN LibreOffice produced no PDF'); global fails; fails += 1; return
    pages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    res(pages == 1, '%s: LibreOffice render is %d page(s), required 1' % (name, pages))
    subprocess.run(['pdftoppm', '-r', str(DPI), '-png', '-f', '1', '-l', '1', pdf, os.path.join(tmp, 'pg')], check=True)
    png = [f for f in os.listdir(tmp) if f.startswith('pg') and f.endswith('.png')][0]
    im = np.array(Image.open(os.path.join(tmp, png)).convert('L'))
    h, w = im.shape
    px = lambda tw, total, n: tw / total * n
    l, r, t, b = px(MARGIN_L, PW, w), w - px(MARGIN_R, PW, w), px(MARGIN_T, PH, h), h - px(MARGIN_B, PH, h)
    xs = np.where((im < 160).any(axis=0))[0]; ys = np.where((im < 160).any(axis=1))[0]
    res(xs.min() >= l - TOL and xs.max() <= r + TOL, 'ink x range %d..%d px inside margins %.1f..%.1f (tolerance %.0f px)' % (xs.min(), xs.max(), l, r, TOL))
    res(ys.min() >= t - TOL and ys.max() <= b + TOL, 'ink y range %d..%d px inside margins %.1f..%.1f' % (ys.min(), ys.max(), t, b))
    res(ys.max() < b - 0.05 * h, 'lowest ink leaves %.1f percent of the page height free above the bottom margin (cover page is not at the limit)' % ((b - ys.max()) / h * 100))
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    code = 'SEN0401' if '0401' in name and 'sen0414' not in name else 'SEN0414'
    need = {'department': 'Department of Computer Engineering', 'course code': code, 'exam title': 'Midterm Exam', 'academic year': '2026-2027',
            'term': 'Fall', 'duration': '60 Minutes', 'instructor': 'Dr. Yusuf ALTUNEL', 'date fill-in': '____ / ____ / 2026',
            'Q5 bonus row': '5 (bonus)', 'total': '/100 + bonus', 'warning': 'WARNING:', 'zero rule': 'ZERO', 'learning outcome row': 'Learning Outcomes',
            'program outcome row': 'Program Outcomes', 'machine-read answer sheet': 'separate answer sheet, which is read by a machine'}
    for k, v in need.items(): res(v in txt, 'content: ' + k + ' (' + v + ')')
    res(len(re.findall(r'/25', txt)) == 4 and '/10' in txt, 'grade table: four rows of /25 and one of /10')
    res(not re.search(r'CSE3003|Object Oriented|Patlar|PATLAR|2023-2024|75 Minutes|19\.09', txt), 'no text of the template course is left')
    # abbreviations: every capital-letter word of 2+ letters (outside the allowed list) must be spelled out in the text before it is used
    words = [x for x in re.findall(r'\b[A-Z][A-Z0-9]{1,}\b', txt) if x not in ALLOWED and not re.fullmatch(r'Q\d', x)]
    res(not words, 'abbreviations without a spelled-out form: %s' % (sorted(set(words)) or 'none'))
    res(re.search(r'Question \(Q\)', txt) is not None, 'the abbreviation Q is spelled out at first use ("Question (Q)") before Q1..Q5')
    shutil.copy(os.path.join(tmp, png), os.path.join(tmp, 'keep_' + name + '.png')) if False else None
if __name__ == '__main__':
    tmp = tempfile.mkdtemp(prefix='sen0401_cover_chk_')
    try:
        for p in sys.argv[1:]:
            for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
            check(os.path.abspath(p), tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('RESULT: %s' % ('FAIL (%d)' % fails if fails else 'PASS'))
    sys.exit(1 if fails else 0)
