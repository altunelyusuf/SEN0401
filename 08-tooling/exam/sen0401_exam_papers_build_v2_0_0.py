#!/usr/bin/env python3
"""SEN0401 midterm paper v2 builder, version 2.0.0 (new file). Builds, per form (default 2 forms, A and B, different seeds):
  paper .docx (3 pages) + PDF export, answer key .docx + PDF export + JSON, answer sheet PDF (1 page) + layout JSON, paper graph (TTL, checked against the shapes EN01-EN13 and R01-R22), measurement JSON.
THE PAGE BUDGET (measured, never assumed): every item is first laid out alone (a measuring document, one item per column) in LibreOffice; the columns are then filled by an exact search that
maximises the smallest free space of the six columns (3 pages x 2 columns); the paper is written with an explicit column break at each start of a column; the result is exported again and
every column is measured on the render (pdfplumber). The build is REFUSED (exit 2, nothing kept) when the paper is not exactly 3 pages or a column keeps less than MIN_FREE of its height free.
Usage: sen0401_exam_papers_build_v2_0_0.py OUTDIR [--seed 4701] [--forms 2] [--chapters 1-6] [--items 24] [--items-file FILE] [--min-free 0.03]"""
import argparse, json, os, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_paper_lib_v2_0_0 as L
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_render_v1_2_0 as R
from sen0401_exam_engine_v1_1_0 import units, CHOICE
VERSION = '2.0.0'
ITEMS = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_1_0.json')
PT = 72 / 25.4
FRAME_TOP, FRAME_BOTTOM = L.TOP * PT, 841.8898 - L.BOTTOM * PT
COLH = FRAME_BOTTOM - FRAME_TOP
CUSHION = 3.0                                    # points added to every measured item (Word may break a line differently)


class Refused(Exception): pass


def item_heights(paper, tmp):
    L.write_docx(paper, os.path.join(tmp, 'meas.docx'), per_item_break=True)
    pdf = L.export_pdf(os.path.join(tmp, 'meas.docx'), tmp)
    cols = [c for pg in L.columns_of_pdf(pdf) for c in pg if c]
    if len(cols) != len(paper['items']): raise Refused('measuring document: %d columns for %d items' % (len(cols), len(paper['items'])))
    return [max(w['bottom'] for w in c) - FRAME_TOP + CUSHION + L.GAP_AFTER + 1.0 for c in cols]


def title_height(paper, tmp):
    L.write_docx(paper, os.path.join(tmp, 'nobreak.docx'))
    pdf = L.export_pdf(os.path.join(tmp, 'nobreak.docx'), tmp)
    first = L.columns_of_pdf(pdf)[0]
    top_items = min(w['top'] for c in first for w in c if w['size'] < 11 and w['top'] > FRAME_TOP + 20)    # first line of an item (not the 12 pt title)
    return top_items - FRAME_TOP


def pack(h, caps, flat=0.0):
    """Assign consecutive items to the columns so that the smallest free space (cap - used) is as large as possible; ties: the smaller spread. Returns (list of lists of indexes, min free)."""
    n, m = len(h), len(caps); pre = [0.0]
    for x in h: pre.append(pre[-1] + x)
    best = {}
    def f(i, c):
        if (i, c) in best: return best[(i, c)]
        if c == m: r = (float('inf'), None) if i == n else (-1e9, None)
        else:
            r = (-1e9, None)
            for j in range(i, n + 1):
                used = pre[j] - pre[i]
                if used > caps[c]: break
                sub = f(j, c + 1)[0]
                v = min(caps[c] - used, sub)
                if v > r[0]: r = (v, j)
        best[(i, c)] = r; return r
    v, _ = f(0, 0)
    if v < 0: return None, v
    if not flat: 
        cols = []; i = 0
        for c in range(m):
            j = f(i, c)[1]; cols.append(list(range(i, j))); i = j
        return cols, v
    # second pass: keep every column at least `floor` free (the largest possible, capped) and make the largest free space as small as possible (the free space is spread evenly)
    floor = min(v, flat); g = {}
    def f2(i, c):
        if (i, c) in g: return g[(i, c)]
        if c == m: r = (0.0, None) if i == n else (1e9, None)
        else:
            r = (1e9, None)
            for j in range(i, n + 1):
                used = pre[j] - pre[i]
                if used > caps[c]: break
                free = caps[c] - used
                if free < floor: continue
                val = max(free, f2(j, c + 1)[0])
                if val < r[0]: r = (val, j)
        g[(i, c)] = r; return r
    cols = []; i = 0
    for c in range(m):
        j = f2(i, c)[1]; cols.append(list(range(i, j))); i = j
    return cols, v


def measure_render(pdf, paper, min_free):
    """Per page and column: lowest line, free space as a share of the column height; fonts; code boxes."""
    import pdfplumber
    cols = L.columns_of_pdf(pdf); res = dict(pages=len(cols), columns=[], fonts={}, code_boxes=[])
    with pdfplumber.open(pdf) as d:
        for pi, pg in enumerate(d.pages):
            for ci in (0, 1):
                ws = cols[pi][ci]
                low = max((w['bottom'] for w in ws), default=FRAME_TOP)
                res['columns'].append(dict(page=pi + 1, column=ci + 1, lowest_line_pt=round(low, 1), free_pt=round(FRAME_BOTTOM - low, 1), free_share=round((FRAME_BOTTOM - low) / COLH, 4)))
            for c in pg.chars:
                k = c['fontname'].split('+')[-1]; s = round(c['size'], 2)
                res['fonts'].setdefault(k, set()).add(s)
        res['fonts'] = {k: sorted(v) for k, v in res['fonts'].items()}
        # code boxes: mono text clusters and the vertical border segments around them
        for pi, pg in enumerate(d.pages):
            for ci in (0, 1):
                mono = [c for c in pg.chars if 'Mono' in c['fontname'] and (((c['x0'] + c['x1']) / 2 < pg.width / 2) == (ci == 0))]
                if not mono: continue
                lines = sorted({round(c['top'], 0) for c in mono})
                groups = []; cur = [lines[0]]
                for y in lines[1:]:
                    if y - cur[-1] <= 12: cur.append(y)
                    else: groups.append(cur); cur = [y]
                groups.append(cur)
                hsegs = [(ln['x0'], ln['x1'], ln['top']) for ln in pg.lines if abs(ln['top'] - ln['bottom']) < 0.5]
                for g in groups:
                    cs = [c for c in mono if g[0] - 1 <= round(c['top'], 0) <= g[-1] + 1]
                    x_min, x_max = min(c['x0'] for c in cs), max(c['x1'] for c in cs)
                    above = [h for h in hsegs if h[2] < g[0] and g[0] - h[2] < 8 and h[0] <= x_min and h[1] >= x_max]
                    if not above: res['code_boxes'].append(dict(page=pi + 1, column=ci + 1, text_x0=round(x_min, 1), text_x1=round(x_max, 1), box='NOT_FOUND')); continue
                    h = max(above, key=lambda t_: t_[2])
                    byline = {}
                    for c in cs: byline.setdefault(round(c['top'], 0), []).append(c)
                    nchars = max(len(v_) for v_ in byline.values()); cw = 0.6 * L.CODE
                    res['code_boxes'].append(dict(page=pi + 1, column=ci + 1, lines=len(byline), box_x0=round(h[0], 1), box_x1=round(h[1], 1), box_width_pt=round(h[1] - h[0], 1), text_x0=round(x_min, 1), text_x1=round(x_max, 1),
                                                  widest_line_chars=nchars, widest_line_pt=round(x_max - x_min, 1), inner_capacity_chars=int((h[1] - h[0] - 2 * 6) / cw),
                                                  fits=bool(x_min >= h[0] and x_max <= h[1]), wide_enough_for_45=bool((h[1] - h[0] - 2 * 6) / cw >= 45)))
    return res


MAX_FREE = 0.18                                  # the layout test also wants the free space spread: no column keeps more than this share free
PLAN_FREE = 0.045                                # the layout test of the order plans for this free share per column (the build then needs min_free on the render)


def build_form(outdir, items_path, chapters, seed, form_no, nitems, min_free, tmpbase):
    paper0, P0 = L.make_form(items_path, chapters, seed, form_no, version=2, nitems=nitems)       # preliminary order: only to measure the height of every item
    tmp0 = tempfile.mkdtemp(dir=tmpbase)
    try: hk = dict(zip([i['key'] for i in paper0['items']], item_heights(paper0, tmp0))); T0 = title_height(paper0, tmp0)
    finally: shutil.rmtree(tmp0, ignore_errors=True)
    caps0 = [COLH - T0 - 2] * 2 + [COLH] * 4
    def accept(order):
        hh = [hk[i['key']] for i in order]
        cols_, v_ = pack(hh, caps0)
        if cols_ is None or v_ < PLAN_FREE * COLH: return False
        cols_, v_ = pack(hh, caps0, flat=PLAN_FREE * COLH)
        return max(cap - sum(hh[k] for k in c_) for cap, c_ in zip(caps0, cols_)) <= MAX_FREE * COLH
    paper, P = L.make_form(items_path, chapters, seed, form_no, version=2, nitems=nitems, accept=accept)
    f = paper['form']; tag = 'sen0401_exam_midterm_v2_0_0_form%s' % f['letter']
    for ext in ('_paper.docx', '_paper.pdf', '_key.docx', '_key.pdf', '_key.json', '_sheet.pdf', '_sheet_layout.json', '_paper.ttl', '_measure.json'):
        if os.path.exists(os.path.join(outdir, tag + ext)): raise Refused('refusing to overwrite ' + tag + ext)
    tmp = tempfile.mkdtemp(dir=tmpbase)
    try:
        h = item_heights(paper, tmp); T = title_height(paper, tmp)
        caps = [COLH - T, COLH - T] + [COLH] * 4
        cols, v = pack(h, caps, flat=PLAN_FREE * COLH)
        if cols is None: raise Refused('form %s: the items do not fit 6 columns (best free space %.1f pt)' % (f['letter'], v))
        breaks = [c[0] for c in cols[1:] if c]
        L.write_docx(paper, os.path.join(tmp, tag + '_paper.docx'), breaks=breaks)
        pdf = L.export_pdf(os.path.join(tmp, tag + '_paper.docx'), tmp)
        m = measure_render(pdf, paper, min_free)
        pages = L.pdf_pages(pdf)
        worst = min(c['free_share'] for c in m['columns'])
        if pages != 3: raise Refused('form %s: the paper has %d pages on the LibreOffice render, not 3' % (f['letter'], pages))
        if worst < min_free: raise Refused('form %s: a column keeps only %.1f percent free (minimum %.1f)' % (f['letter'], worst * 100, min_free * 100))
        if any(not b.get('fits') for b in m['code_boxes']): raise Refused('form %s: a code line is wider than its box: %s' % (f['letter'], [x for x in m['code_boxes'] if not x.get('fits')]))
        paper['contentPages'] = pages
        sp, layout = L.render_sheet(paper, os.path.join(tmp, tag + '_sheet.pdf'))
        if sp != 1: raise Refused('form %s: the answer sheet has %d pages, not 1' % (f['letter'], sp))
        paper['sheetPages'] = sp; paper['pageCount'] = pages + sp
        g, pid = E.to_graph(paper); viol = E.validate(g, P.chapters)
        if any(s == 'Violation' for r_, s, m_ in viol): raise E.ExamRefused(viol)
        g.serialize(os.path.join(tmp, tag + '_paper.ttl'), format='turtle')
        key = R.answer_key(paper); key.update(form=f['letter'], form_code=f['code'], seed=f['seed'], order_rule=f['order_rule'], paper_file=tag + '_paper.docx', sheet_file=tag + '_sheet.pdf')
        layout['form_code'] = f['code']
        json.dump(layout, open(os.path.join(tmp, tag + '_sheet_layout.json'), 'w'), indent=1)
        json.dump(key, open(os.path.join(tmp, tag + '_key.json'), 'w', encoding='utf8'), indent=1, ensure_ascii=False)
        L.write_key_docx(paper, key, os.path.join(tmp, tag + '_key.docx'))
        L.export_pdf(os.path.join(tmp, tag + '_key.docx'), tmp)
        meas = dict(version=VERSION, form=f, items_file=os.path.basename(items_path), chapters=paper['chapters'], items=len(paper['items']), units=sum(units(i) for i in paper['items']),
                    paper_pages=pages, sheet_pages=sp, pages_total=pages + sp, key_pages=L.pdf_pages(os.path.join(tmp, tag + '_key.pdf')), sheet_pages_if_in_paper_order=L.sheet_pages_in_paper_order(paper),
                    title_height_pt=round(T, 1), column_height_pt=round(COLH, 1), item_heights_pt=[round(x, 1) for x in h], column_plan=[[paper['items'][k]['position'] for k in c] for c in cols],
                    min_free_share=worst, min_free_required=min_free, render=m,
                    item_order=[(i['position'], i['key'], i['type'], i['bloom'], i['chapters']) for i in paper['items']], warnings=[v_[2] for v_ in viol if v_[1] != 'Violation'])
        json.dump(meas, open(os.path.join(tmp, tag + '_measure.json'), 'w'), indent=1)
        for ext in ('_paper.docx', '_paper.pdf', '_key.docx', '_key.pdf', '_key.json', '_sheet.pdf', '_sheet_layout.json', '_paper.ttl', '_measure.json'):
            shutil.copy(os.path.join(tmp, tag + ext), os.path.join(outdir, tag + ext))
        return meas
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('outdir'); a.add_argument('--seed', type=int, default=4701); a.add_argument('--forms', type=int, default=2)
    a.add_argument('--chapters', default='1-6'); a.add_argument('--items', type=int, default=24); a.add_argument('--items-file', default=ITEMS); a.add_argument('--min-free', type=float, default=0.03)
    x = a.parse_args(); os.makedirs(x.outdir, exist_ok=True); tb = tempfile.mkdtemp(prefix='sen0401_paperfix_')
    try:
        for fno in range(1, x.forms + 1):
            try: m = build_form(x.outdir, x.items_file, x.chapters, x.seed + fno - 1, fno, x.items, x.min_free, tb)
            except (Refused, E.ExamRefused, RuntimeError) as e:
                print('REFUSED', e); sys.exit(2)
            f = m['form']
            print('FORM %s seed %d code %s: paper %d pages (docx) + sheet %d page = %d; key %d page(s); min free %.1f percent; sheet pages if in paper order %d; order draws %d' %
                  (f['letter'], f['seed'], f['code'], m['paper_pages'], m['sheet_pages'], m['pages_total'], m['key_pages'], m['min_free_share'] * 100, m['sheet_pages_if_in_paper_order'], f['order_draws']))
            for c in m['render']['columns']: print('   page %d column %d: lowest line %.1f pt, free %.1f pt = %.1f percent of the column' % (c['page'], c['column'], c['lowest_line_pt'], c['free_pt'], c['free_share'] * 100))
            for b in m['render']['code_boxes']: print('   code box page %d: %s' % (b['page'], b))
            print('   fonts on the render:', m['render']['fonts'])
    finally:
        shutil.rmtree(tb, ignore_errors=True)
