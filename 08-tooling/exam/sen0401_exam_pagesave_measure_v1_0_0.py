"""Page-saving measurement for the printed paper, version 1.0.0.
Builds a deterministic sample paper from the chapter question banks (read only) with reportlab, counts the pages of the real PDF (pdfinfo),
and prints pages for the baseline layout, each method alone, and the methods stacked.
Usage: measure.py [--chapters 1-6] [--n 40] [--json FILE] [--keep DIR]
Layout-only models (matching block, fill-in bank) use the text of real bank items and are NOT exam items."""
import argparse, glob, json, os, random, re, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted, Spacer, Table, TableStyle, KeepTogether, PageBreak
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.dirname(HERE)
FD = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('Sans', FD + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SansB', FD + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Mono', FD + 'DejaVuSansMono.ttf'))
LET = 'ABCD'
MONO_W = 0.602  # DejaVu Sans Mono advance, em

def parse_ch(s):
    out = []
    for p in s.split(','):
        if '-' in p: a, b = p.split('-'); out += range(int(a), int(b) + 1)
        else: out.append(int(p))
    return out

def load_bank(n):
    fs = glob.glob(os.path.join(TOOL, 'ch%02d-page' % n, 'question_bank_v*.json'))
    fs.sort(key=lambda x: [int(v) for v in x.rsplit('_v', 1)[1][:-5].split('_')])
    return fs[-1], json.load(open(fs[-1], encoding='utf8'))

HIGHER = {'Apply', 'Analyze'}
CODE_COLS = 45  # a code line that prints unwrapped in one column of a two-column A4 page at 9 pt (measured below)

def sample(chs, n, seed=4701):
    """Deterministic sample: equal share per chapter, higher Bloom levels a majority, code lines unwrapped in a column, answer letters balanced."""
    rnd = random.Random(seed); pool = {}; elig = {}
    for c in chs:
        f, b = load_bank(c)
        ok = [dict(i, chapter=c) for i in b if len(i['q']) < 400 and (not i.get('code') or (max(len(l) for l in i['code'].split('\n')) <= CODE_COLS and len(i['code'].split('\n')) <= 12))]
        elig[c] = (len(b), len(ok)); pool[c] = ok
    per = [n // len(chs) + (1 if k < n % len(chs) else 0) for k in range(len(chs))]
    picked = []
    for c, k in zip(chs, per):
        hi = [i for i in pool[c] if i['level'] in HIGHER]; lo = [i for i in pool[c] if i['level'] not in HIGHER]
        rnd.shuffle(hi); rnd.shuffle(lo)
        kh = min(len(hi), -(-k * 6 // 10)); take = hi[:kh] + lo[:k - kh]
        if len(take) < k: take += hi[kh:kh + k - len(take)]
        picked += take
    rnd.shuffle(picked)
    # balance the answer letters: rotate each item's options so that the key lands on the letter its position demands (position mod 4, shuffled once)
    targets = [k % 4 for k in range(len(picked))]; rnd.shuffle(targets)
    for it, t in zip(picked, targets):
        opts = list(it['options']); key = opts[it['answer']]
        rest = [o for k, o in enumerate(opts) if k != it['answer']]; rnd.shuffle(rest)
        rest.insert(t, key); it['options'] = rest; it['answer'] = t
    return picked, elig

class Cfg:
    def __init__(s, **k):
        s.margin = 25; s.font = 12; s.cols = 1; s.grid = False; s.answer = 'sheet'; s.duplex = False
        for a, v in k.items(): setattr(s, a, v)

GRIDN_ = [0]
def _h(f, cw):
    if isinstance(f, KeepTogether): return sum(_h(g, cw) for g in f._content)
    return f.wrap(cw, 10000)[1] + (f.getSpaceAfter() if hasattr(f, 'getSpaceAfter') else 0)
def build(items, cfg, path):
    GRIDN_[0] = 0
    W, H = A4; m = cfg.margin * mm; gap = 8 * mm
    cw = (W - 2 * m - (cfg.cols - 1) * gap) / cfg.cols
    fs = cfg.font; ld = fs * 1.25; cfs = min(9, fs - 1) if cfg.font <= 10 else 9
    st = ParagraphStyle('q', fontName='Sans', fontSize=fs, leading=ld, spaceAfter=2)
    so = ParagraphStyle('o', parent=st, leftIndent=14, firstLineIndent=-14, spaceAfter=0)
    sh = ParagraphStyle('h', fontName='SansB', fontSize=fs + 3, leading=(fs + 3) * 1.25)
    sc = ParagraphStyle('c', fontName='Mono', fontSize=cfs, leading=cfs * 1.2)
    top = m + (0 if True else 0)
    frames = [Frame(m + k * (cw + gap), m, cw, H - 2 * m, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='f%d' % k) for k in range(cfg.cols)]
    doc = BaseDocTemplate(path, pagesize=A4, pageTemplates=[PageTemplate(id='p', frames=frames)], compress=0)
    story = [Paragraph('SEN0401 Midterm (sample for page measurement)', sh), Paragraph('Name: ______________________   Number: ______________   Time: 60 minutes', st),
             Paragraph('Circle one letter per question. Write nothing outside the boxes. A wrong answer costs nothing.', st), Spacer(1, 8)]
    if cfg.cols == 2:  # the header is above the columns in a real layout; the sample keeps it inside column 1, which costs the same height
        pass
    sep = 12 if cfg.font >= 12 else 7
    for k, it in enumerate(items, 1):
        fl = [Paragraph('<b>%d.</b> %s' % (k, escape(it['q'])), st)]
        if it.get('code'): fl.append(Preformatted(it['code'], sc))
        shortopts = all(len(o) * fs * 0.55 < (cw - 30) / 2 for o in it['options'])
        if cfg.grid and shortopts:
            GRIDN_[0] += 1
            cells = [[Paragraph('%s) %s' % (LET[a], escape(it['options'][a])), so), Paragraph('%s) %s' % (LET[a + 1], escape(it['options'][a + 1])), so)] for a in (0, 2)]
            t = Table(cells, colWidths=[cw / 2] * 2); t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
            fl.append(t)
        else:
            fl += [Paragraph('%s) %s' % (LET[a], escape(o)), so) for a, o in enumerate(it['options'])]
        fl.append(Spacer(1, sep)); story.append(KeepTogether(fl))
    if cfg.answer == 'sheet':
        story += [PageBreak(), Paragraph('Answer sheet', sh), Spacer(1, 6)]
        for k in range(1, len(items) + 1): story.append(Paragraph('%d.  ______' % k, ParagraphStyle('a', fontName='Sans', fontSize=fs, leading=fs * 1.9)))
    global LASTH
    LASTH = sum(_h(f, cw) for f in story if not isinstance(f, PageBreak)) / ((H - 2 * m) * cfg.cols)
    doc.build(story)
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout).group(1))
    return n

LASTH = 0.0
GRIDN = 0

def block_models(chs, tmp):
    """Layout-only cost of two denser item types against the same number of MC items, same engine (single column, 10 pt), height in points."""
    items, _ = sample(chs, 30)
    W, H = A4; m = 15 * mm; cw = W - 2 * m
    st = ParagraphStyle('q', fontName='Sans', fontSize=10, leading=12.5, spaceAfter=2)
    so = ParagraphStyle('o', parent=st, leftIndent=14, firstLineIndent=-14, spaceAfter=0)
    def height(fl):
        h = 0
        for f in fl: h += f.wrap(cw, 10000)[1] + getattr(f, 'getSpaceAfter', lambda: 0)()
        return h
    mc = []
    five = [i for i in items if not i.get('code')][:5]
    for k, it in enumerate(five, 1):
        mc += [Paragraph('<b>%d.</b> %s' % (k, escape(it['q'])), st)] + [Paragraph('%s) %s' % (LET[a], escape(o)), so) for a, o in enumerate(it['options'])] + [Spacer(1, 7)]
    prem = [Paragraph('%d. %s' % (k, escape(it['q'])), st) for k, it in enumerate(five, 1)]
    resp = [Paragraph('%s) %s' % ('ABCDEFG'[k], escape(it['options'][it['answer']])), so) for k, it in enumerate(five)]
    extra = [Paragraph('%s) %s' % ('ABCDEFG'[len(five) + k], escape(five[k]['options'][(five[k]['answer'] + 1) % 4])), so) for k in range(2)]
    t = Table([[prem[k] if k < 5 else '', (resp + extra)[k]] for k in range(7)], colWidths=[cw * .46, cw * .54])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)]))
    mt = [Paragraph('Match each statement to one answer (each answer is used at most once).', st), t, Spacer(1, 7)]
    # fill-in: 6 short sentences with one bank
    allb = []
    for c in chs: allb += [dict(i, chapter=c) for i in load_bank(c)[1]]
    short = [i for i in allb if not i.get('code') and len(i['options'][i['answer']]) <= 40 and len(i['q']) < 120][:6]
    sents = [Paragraph('%d. %s ______' % (k, escape(it['q'])), st) for k, it in enumerate(short, 1)]
    bank = Paragraph('Bank: ' + ' | '.join('[%d] %s' % (k + 1, escape(it['options'][it['answer']])) for k, it in enumerate(short)), st)
    fi = sents + [bank, Spacer(1, 7)]
    mc6 = []
    for k, it in enumerate(short, 1):
        mc6 += [Paragraph('<b>%d.</b> %s' % (k, escape(it['q'])), st)] + [Paragraph('%s) %s' % (LET[a], escape(o)), so) for a, o in enumerate(it['options'])] + [Spacer(1, 7)]
    return {'mc_5_items_pt': round(height(mc), 1), 'matching_5_premises_7_responses_pt': round(height(mt), 1),
            'mc_6_items_pt': round(height(mc6), 1), 'fillin_6_blanks_one_bank_pt': round(height(fi), 1), 'fillin_items_found': len(short),
            'usable_page_height_pt': round(H - 2 * m, 1)}

def run(chs, n, keep=None):
    tmp = keep or tempfile.mkdtemp(prefix='sen0401_exam_pagesave_')
    os.makedirs(tmp, exist_ok=True)
    items, elig = sample(chs, n)
    lv = {}
    for i in items: lv[i['level']] = lv.get(i['level'], 0) + 1
    let = [LET[i['answer']] for i in items]
    out = {'chapters': chs, 'n_items': len(items), 'paper': 'A4 (a default; the owner fixes the paper size)', 'sample_levels': lv,
           'sample_letters': {l: let.count(l) for l in LET}, 'eligible_per_chapter_(bank_size, fits_one_column)': {str(c): list(v) for c, v in elig.items()}}
    frac = {}
    def P(name, **k):
        r = build(items, Cfg(**k), os.path.join(tmp, name + '.pdf')); frac[name] = (round(LASTH, 2), GRIDN_[0]); return r
    base = dict(margin=25, font=12, cols=1, grid=False, answer='sheet')
    res = {'B0 baseline (25 mm margin, 12 pt, one column, options listed, separate answer sheet)': P('b0', **base)}
    steps = [('M1 margins 25 -> 15 mm', dict(margin=15)), ('M2 text 12 -> 10 pt', dict(font=10)), ('M3 two columns', dict(cols=2)),
             ('M4 short options in a 2 x 2 block', dict(grid=True)), ('M5 circle the letter on the item, no answer sheet', dict(answer='item'))]
    alone = {}
    for name, k in steps: alone[name] = P('a_' + name[:2], **dict(base, **k))
    cum = {}; cur = dict(base)
    for name, k in steps:
        cur.update(k); cum[name] = P('c_' + name[:2], **cur)
    out['pages_baseline'] = list(res.values())[0]
    out['pages_each_method_alone'] = alone
    out['pages_methods_stacked_in_order'] = cum
    final = list(cum.values())[-1]
    out['M6 duplex: sheets of paper (pages / 2, rounded up) baseline -> stacked'] = [-(-out['pages_baseline'] // 2), -(-final // 2)]
    out['fractional_pages_of_content_(sum of item heights / page area; answer sheet included)'] = {k: v[0] for k, v in frac.items()}
    out['items_set_in_a_2x2_block_when_M4_is_on'] = {k: v[1] for k, v in frac.items() if k.startswith('c_M4') or k.startswith('c_M5')}
    out['block_models_pt'] = block_models(chs, tmp)
    # code width fact over the whole banks
    fact = {}
    for c in chs:
        f, b = load_bank(c); cds = [i for i in b if i.get('code')]
        w = [max(len(l) for l in i['code'].split('\n')) for i in cds]
        fact[str(c)] = {'items': len(b), 'code_items': len(cds), 'code_wider_than_%d_cols' % CODE_COLS: sum(1 for x in w if x > CODE_COLS), 'code_longer_than_12_lines': sum(1 for i in cds if len(i['code'].split('\n')) > 12)}
    out['code_width_fact'] = fact
    if not keep: shutil.rmtree(tmp)
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--chapters', default='1-6'); ap.add_argument('--n', type=int, default=40)
    ap.add_argument('--json'); ap.add_argument('--keep')
    a = ap.parse_args(); r = run(parse_ch(a.chapters), a.n, a.keep)
    print(json.dumps(r, indent=1, ensure_ascii=False))
    if a.json: json.dump(r, open(a.json, 'w'), indent=1, ensure_ascii=False)
