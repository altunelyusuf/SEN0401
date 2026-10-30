"""SEN0401 midterm paper builder, version 1.0.0 (new file; the engine v1.1.0, its renderer and the answer sheet module are imported unchanged and never edited).
Builds the MIDTERM paper from the authored items file sen0401_exam_items_midterm_v1_0_0.json in BOTH orders and writes, per order:
  paper PDF, answer sheet PDF (+ layout JSON the reader needs), paper graph (TTL), answer key (JSON for the grader and a printable PDF), and the page measurement (JSON).
Orders:  chapter  - items sorted by their primary chapter (the engine's own order)
         type     - items grouped by item type across the chapters (choice, matching, ordering, fill-in, number, trace), then by chapter inside a type.
                    The only difference to the engine's build_paper is the sort line; everything else (selection, higher-order top-up, letter balance, bank order) is the engine's code path.
The make-up paper is NOT built here (deferred by the owner on 2026-10-30).
Usage: sen0401_exam_papers_build_v1_0_0.py OUTDIR [--seed 4701] [--chapters 1-6] [--items 24]"""
import argparse, json, os, random, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_render_v1_1_0 as R0
import sen0401_exam_engine_render_v1_2_0 as R
from sen0401_exam_engine_v1_1_0 import units, CHOICE
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
VERSION = '1.0.0'
ITEMS = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_0_0.json')
TYPE_RANK = {'ChoiceFour': 0, 'ChoiceFourCode': 1, 'Matching': 2, 'Ordering': 3, 'FillBlankGroup': 4, 'NumericAnswer': 5, 'CodeTrace': 6, 'ShortAnswer': 7}


def build_paper(P, kind, order):
    """The engine's build_paper (v1.1.0), same steps, with one added ordering: 'type'."""
    rnd = random.Random(P.seed * 7)
    auth, skipped = E.load_authored(P.authored, P.chapters)
    pages, pkey = E.pages_for(P.chapters)
    pool = [i for i in auth if kind in i['papers']]
    picks, q = E.select(P, kind, pool, rnd)
    tot = lambda L_: sum(units(i) for i in L_); hi_n = lambda L_: sum(units(i) for i in L_ if i['bloom'] >= P.higher_from)
    guard = 0
    while hi_n(picks) * 2 <= tot(picks) and guard < 200:
        guard += 1; swap = None
        for lo_ in [i for i in picks if i['bloom'] < P.higher_from]:
            alt = [i for i in pool if i['primary'] == lo_['primary'] and i['bloom'] >= P.higher_from and i not in picks and units(i) == units(lo_)]
            if alt: swap = (lo_, rnd.choice(alt)); break
        if not swap: break
        picks[picks.index(swap[0])] = swap[1]
    allit = [dict(i) for i in picks]
    for i in allit:
        i['matches'] = E.check_copies(i, pages); i['checked_against'] = len(pages)
    if order == 'type': allit.sort(key=lambda i: (TYPE_RANK[i['type']], i['primary'], rnd.random()))
    elif order == 'chapter': allit.sort(key=lambda i: (i['primary'], rnd.random()))
    else: raise ValueError(order)
    E.balance_letters([i for i in allit if i['type'] in CHOICE], rnd)
    pos = 0
    for i in allit:
        pos += 1; i['position'] = pos
        if i['type'] == 'FillBlankGroup':
            r = random.Random(P.seed * 31 + i['position']); nt = len(i['blanks']) + len(i['distractors'])
            for _ in range(200):
                o = list(range(nt)); r.shuffle(o)
                ap = [o.index(k) for k in range(len(i['blanks']))]
                if any(ap[a] > ap[b] for a in range(len(ap)) for b in range(a + 1, len(ap))): break
            i['bank_order'] = o; pos += len(i['blanks']) - 1
        if i['type'] == 'Ordering': i['display_order'] = E.order_of_steps(i['position'], len(i['steps']), P.seed)
        if i['type'] == 'Matching':
            i['responses'] = list(i['responses']); random.Random(P.seed * 17 + i['position']).shuffle(i['responses'])
    return dict(kind=kind, version=1, previous=0, chapters=list(P.chapters), quotas=q, params=P.snapshot(), items=allit, pool_size=len(pool), skipped=skipped, page_chapters=list(pkey), page_items=len(pages))


def key_pdf(paper, key, path):
    W, H = A4; c = canvas.Canvas(path, pagesize=A4, invariant=1); c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0)
    m = 15 * mm; y = H - m
    def line(t, f='Sans', s=10, dy=13):
        nonlocal y
        if y < m + 14: c.showPage(); y = H - m
        c.setFont(f, s); c.drawString(m, y, t); y -= dy
    line('SEN0401 midterm v%d - ANSWER KEY (for the grader; not for students) - order: %s' % (paper['version'], paper['params']['order']), 'SansB', 11, 18)
    line('Chapters %s. Pages of the paper: %s (content %s + sheet %s).' % (', '.join(map(str, paper['chapters'])), paper['pageCount'], paper['contentPages'], paper['sheetPages']))
    line('Letters/answers are those of the answer sheet rows. Numbers: tolerance as stated. Traces: the printed text.', dy=18)
    for e in key['items']:
        a = e['answer']
        if isinstance(a, dict) and 'value' in a: s = 'value %s %s (tolerance %s)' % (a['value'], a['unit'], a['tolerance'])
        elif isinstance(a, dict): s = '   '.join('%s=%s' % (k, v) for k, v in a.items())
        else: s = str(a)
        line('%2d  %-15s ch %-8s Bloom %d  %s' % (e['position'], e['type'], ','.join(map(str, e['chapters'])), e['bloom'], ''), 'Mono' if False else 'Sans', 10, 12)
        for k in range(0, len(s), 95): line('      ' + s[k:k + 95], 'Sans', 10, 12)
    c.save()


def pages_of(path):
    import subprocess
    o = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    return int([l for l in o.splitlines() if l.startswith('Pages:')][0].split()[1])


def build(outdir, order, chapters, nitems, seed):
    M = E.M
    P = E.Params(nitems, M.parse_ch(chapters), None, 'GridOnCover', synthesis_min=0, higher_from=3, indirect_enabled=False, seed=seed, sitting=60, columns=2, code_cap=45,
                 page_limit=None, enable=[], allow_repeat=False, authored=ITEMS, order=order)
    paper = build_paper(P, 'midterm', order)
    base = os.path.join(outdir, 'sen0401_exam_midterm_%s_v1_0_0' % order)
    for ext in ('.pdf', '_sheet.pdf'):
        if os.path.exists(base + ext): raise RuntimeError('refusing to overwrite ' + base + ext)
    paper['contentPages'] = R.render(paper, base + '.pdf')
    sp, layout = R.render_sheet(paper, base + '_sheet.pdf'); paper['sheetPages'] = sp; paper['pageCount'] = paper['contentPages'] + sp
    g, pid = E.to_graph(paper)
    viol = E.validate(g, P.chapters)
    if any(s == 'Violation' for r, s, m in viol): raise E.ExamRefused(viol)
    g.serialize(base + '_paper.ttl', format='turtle')
    json.dump(layout, open(base + '_sheet_layout.json', 'w'), indent=1)
    key = R.answer_key(paper); json.dump(key, open(base + '_key.json', 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    key_pdf(paper, key, base + '_key.pdf')
    meas = dict(order=order, content_pages=paper['contentPages'], sheet_pages=sp, pages_with_sheet=paper['pageCount'], key_pages=pages_of(base + '_key.pdf'), units=sum(units(i) for i in paper['items']),
                items=len(paper['items']), seed=seed, chapters=paper['chapters'], warnings=[v[2] for v in viol if v[1] != 'Violation'], item_order=[(i['position'], i['key']) for i in paper['items']])
    json.dump(meas, open(base + '_measure.json', 'w'), indent=1)
    return meas


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('outdir'); a.add_argument('--seed', type=int, default=4701); a.add_argument('--chapters', default='1-6'); a.add_argument('--items', type=int, default=24)
    a.add_argument('--orders', default='chapter,type'); x = a.parse_args(); os.makedirs(x.outdir, exist_ok=True)
    for o in x.orders.split(','):
        m = build(x.outdir, o, x.chapters, x.items, x.seed)
        print('ORDER %-8s content pages %d + sheet pages %d = %d pages with the sheet; key pages %d; units %d' % (o, m['content_pages'], m['sheet_pages'], m['pages_with_sheet'], m['key_pages'], m['units']))
        for w in m['warnings']: print('  WARNING', w)
