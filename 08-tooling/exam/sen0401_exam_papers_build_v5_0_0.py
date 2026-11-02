#!/usr/bin/env python3
"""SEN0401 midterm paper v5 builder, version 5.0.0 (new file, copied from sen0401_exam_papers_build_v3_0_0.py, which stays unchanged; ONE form, library v5.0.0, items v1.4.0, structure v1.1.0; output names carry no form letter). Original docstring of v3: Per form (default 2 forms, A and B):
  paper .docx (cover page + question pages) and its PDF export, answer key .docx + PDF export + JSON, answer sheet PDF + layout JSON, paper graph (TTL, checked against the engine shapes), measurement JSON.
THE PAGE BUDGET (measured, never assumed, no item is ever shortened):
  Step 1  every sub-question is laid out alone in LibreOffice (a measuring document, one per column) at each layout configuration (library CONFIGS);
  Step 2  the 4-PAGE TARGET (cover + 2 question pages of 2 columns + sheet) is tested on the most compact configuration: the summed heights against the 4 columns it has;
  Step 3  when the target does not fit, the 6-PAGE PLAN (cover + 4 question pages + sheet) takes the MOST READABLE configuration whose sub-questions pack in order into the columns of 4 pages
          with at least MIN_FREE of every column free; the packing is exact (maximise the smallest free space); explicit column breaks; the result is exported and every column measured on the render.
The build is REFUSED (exit 2, nothing kept) when the render has another page count than planned or a column keeps less than MIN_FREE free, or a code line is wider than its box.
Usage: sen0401_exam_papers_build_v3_0_0.py OUTDIR [--seed 5701] [--forms 2] [--min-free 0.03] [--measure-only]"""
import argparse, json, os, random, shutil, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_paper_lib_v5_0_0 as L
import sen0401_exam_engine_v1_1_0 as E
VERSION = '5.0.0'
PREFERENCE = ['single11', 'read11', 'read105', 'air10a', 'air10b', 'air10c', 'compact10']          # most readable first
ROBUST_FREE = 0.06                                                               # a setting is taken only when some order keeps at least this share free in EVERY column (room for Word's own line breaks)
MAX_FREE = 0.32                                                                  # the order search also wants the free space spread: no column keeps more than this share free
PLAN_FREE = 0.04                                                                 # the order search plans for this free share per column; the render must keep MIN_FREE
PT = 72 / 25.4
CUSHION = 3.0                                                                    # points added to every measured slot (Word may break a line differently)


class Refused(Exception): pass


def slot_heights(paper, tmp):
    g = L.geom()
    L.write_docx(paper, os.path.join(tmp, 'meas.docx'), per_item_break=True)
    pdf = L.export_pdf(os.path.join(tmp, 'meas.docx'), tmp)
    cols = [c for pg in L.columns_of_pdf(pdf) for c in pg if c]
    if len(cols) != len(paper['slots']): raise Refused('measuring document: %d columns for %d sub-questions' % (len(cols), len(paper['slots'])))
    return [max(w['bottom'] for w in c) - g['frame_top'] + CUSHION + L.CFG['gap'] + 1.0 for c in cols]


def heading_heights(paper, tmp):
    """Height of each question heading with its instruction (raw, from the top of the frame to the bottom of the last line), measured alone."""
    g = L.geom(); firsts = []
    for q in range(1, 6): firsts.append([s for s in paper['slots'] if s['q'] == q][0])
    p2 = dict(paper); p2['slots'] = firsts
    L.write_docx(p2, os.path.join(tmp, 'head.docx'), per_item_break=True, blocks_override=[L.heading_blocks(paper, q) for q in range(1, 6)])
    pdf = L.export_pdf(os.path.join(tmp, 'head.docx'), tmp)
    cols = [c for pg in L.columns_of_pdf(pdf) for c in pg if c]
    if len(cols) != 5: raise Refused('heading measuring document: %d columns for 5 headings' % len(cols))
    return {q: max(w['bottom'] for w in c) - g['frame_top'] + 1.0 + 3.0 for q, c in zip(range(1, 6), cols)}      # + the gap the heading paragraph keeps below it (3 pt) already inside; +1 safety


def title_height(paper, tmp):
    g = L.geom()
    L.write_docx(paper, os.path.join(tmp, 'nobreak.docx'), cover=False)
    pdf = L.export_pdf(os.path.join(tmp, 'nobreak.docx'), tmp)
    first = L.columns_of_pdf(pdf)[0]
    tops = [w['top'] for c in first for w in c if w['text'] == 'Question' and abs(w['size'] - L.CFG['head']) < 0.3]
    if not tops: raise Refused('title height: no question heading found on page 1')
    return min(tops) - g['frame_top']


def pack(h, caps, flat=0.0):
    """Consecutive sub-questions to the columns so that the smallest free space is as large as possible; a second pass spreads the free space. Returns (list of index lists, min free)."""
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
                v = min(caps[c] - used, f(j, c + 1)[0])
                if v > r[0]: r = (v, j)
        best[(i, c)] = r; return r
    v, _ = f(0, 0)
    if v < 0: return None, v
    if not flat:
        cols = []; i = 0
        for c in range(m):
            j = f(i, c)[1]; cols.append(list(range(i, j))); i = j
        return cols, v
    floor = min(v, flat); gmemo = {}
    def f2(i, c):
        if (i, c) in gmemo: return gmemo[(i, c)]
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
        gmemo[(i, c)] = r; return r
    cols = []; i = 0
    for c in range(m):
        j = f2(i, c)[1]; cols.append(list(range(i, j))); i = j
    return cols, v


def measure_render(pdf, min_free, skip=1):
    """Per question page and column: lowest line, free space as a share of the column height; fonts; code boxes. skip = the cover page."""
    import pdfplumber
    g = L.geom(); colh = g['frame_bottom'] - g['frame_top']; n = L.CFG['cols']
    cols = L.columns_of_pdf(pdf, skip=skip); res = dict(pages=len(cols), columns=[], fonts={}, code_boxes=[])
    with pdfplumber.open(pdf) as d:
        for pi, pg in enumerate(d.pages[skip:]):
            for ci in range(n):
                ws = cols[pi][ci]; low = max((w['bottom'] for w in ws), default=g['frame_top'])
                res['columns'].append(dict(page=pi + 1 + skip, column=ci + 1, lowest_line_pt=round(low, 1), free_pt=round(g['frame_bottom'] - low, 1), free_share=round((g['frame_bottom'] - low) / colh, 4)))
            for c in pg.chars:
                k = c['fontname'].split('+')[-1]; s = round(c['size'], 2); res['fonts'].setdefault(k, set()).add(s)
        res['fonts'] = {k: sorted(v) for k, v in res['fonts'].items()}
        for pi, pg in enumerate(d.pages[skip:]):
            for ci in range(n):
                mono = [c for c in pg.chars if 'Mono' in c['fontname'] and (n == 1 or ((c['x0'] + c['x1']) / 2 < pg.width / 2) == (ci == 0))]
                if not mono: continue
                lines = sorted({round(c['top'], 0) for c in mono}); groups = []; cur = [lines[0]]
                for y in lines[1:]:
                    if y - cur[-1] <= 12: cur.append(y)
                    else: groups.append(cur); cur = [y]
                groups.append(cur)
                hsegs = [(ln['x0'], ln['x1'], ln['top']) for ln in pg.lines if abs(ln['top'] - ln['bottom']) < 0.5]
                for gr in groups:
                    cs = [c for c in mono if gr[0] - 1 <= round(c['top'], 0) <= gr[-1] + 1]
                    x_min, x_max = min(c['x0'] for c in cs), max(c['x1'] for c in cs)
                    above = [h for h in hsegs if h[2] < gr[0] and gr[0] - h[2] < 8 and h[0] <= x_min and h[1] >= x_max]
                    if not above: res['code_boxes'].append(dict(page=pi + 1 + skip, column=ci + 1, text_x0=round(x_min, 1), text_x1=round(x_max, 1), box='NOT_FOUND', fits=False)); continue
                    h = max(above, key=lambda t_: t_[2]); byline = {}
                    for c in cs: byline.setdefault(round(c['top'], 0), []).append(c)
                    nchars = max(len(v_) for v_ in byline.values()); cw = 0.6 * L.CFG['code']
                    res['code_boxes'].append(dict(page=pi + 1 + skip, column=ci + 1, lines=len(byline), box_width_pt=round(h[1] - h[0], 1), widest_line_chars=nchars, widest_line_pt=round(x_max - x_min, 1),
                                                  inner_capacity_chars=int((h[1] - h[0] - 12) / cw), fits=bool(x_min >= h[0] and x_max <= h[1]), wide_enough_for_45=bool((h[1] - h[0] - 12) / cw >= 45)))
    return res


def base_heights(paper, tmp):
    """Height of every sub-question WITHOUT the question heading (the heading is added to the first sub-question of a question, whichever it is in the form's order)."""
    g = L.geom()
    L.write_docx(paper, os.path.join(tmp, 'meas.docx'), per_item_break=True, blocks_override=[L.slot_blocks(s, paper, first_of_question=False) for s in paper['slots']])
    pdf = L.export_pdf(os.path.join(tmp, 'meas.docx'), tmp)
    cols = [c for pg in L.columns_of_pdf(pdf) for c in pg if c]
    if len(cols) != len(paper['slots']): raise Refused('measuring document: %d columns for %d sub-questions' % (len(cols), len(paper['slots'])))
    return {s['skey']: max(w['bottom'] for w in c) - g['frame_top'] + CUSHION + L.CFG['gap'] + 1.0 for s, c in zip(paper['slots'], cols)}


def heights_in_order(order, base, head):
    out = []; seen = set()
    for s in order:
        x = base[s['skey']]
        if s['q'] not in seen: seen.add(s['q']); x += head[s['q']]
        out.append(x)
    return out


def caps_for(T, pages):
    g = L.geom(); colh = g['frame_bottom'] - g['frame_top']; n = L.CFG['cols']
    return ([colh - T] * n) + [colh] * (n * pages - n), colh


def measure_config(name, seed, tmpbase):
    L.set_cfg(name); paper = L.make_form(1, seed); tmp = tempfile.mkdtemp(dir=tmpbase)
    try:
        base = base_heights(paper, tmp); head = heading_heights(paper, tmp); T = title_height(paper, tmp)
    finally: shutil.rmtree(tmp, ignore_errors=True)
    g = L.geom(); colh = g['frame_bottom'] - g['frame_top']
    return dict(config=name, cfg=dict(L.CFG), base=base, head=head, title_height_pt=round(T, 1), column_height_pt=round(colh, 1),
                summed_pt=round(sum(base.values()) + sum(head.values()), 1), columns_needed=round((sum(base.values()) + sum(head.values()) + T * L.CFG['cols']) / colh, 2), paper=paper)


def search_order(m, pages, draws=6000, seed=1):
    """Feasibility of the 6-page plan on measured heights: random mixed orders inside the questions; returns (orders that pack with PLAN_FREE, best smallest free space, draws)."""
    L.set_cfg(m['config']); caps, colh = caps_for(m['title_height_pt'], pages); slots = m['paper']['slots']; rnd = random.Random(seed); ok = 0; best = -1e9
    for _ in range(draws):
        o = []
        for q in range(1, 6):
            part = [s for s in slots if s['q'] == q]; rnd.shuffle(part); o += part
        cols, v = pack(heights_in_order(o, m['base'], m['head']), caps)
        best = max(best, v)
        if cols is not None and v >= PLAN_FREE * colh: ok += 1
    return ok, best, draws


def build_form(outdir, form_no, seed, min_free, tmpbase, m, pages_q):
    L.set_cfg(m['config'])
    g = L.geom(); colh = g['frame_bottom'] - g['frame_top']; caps0, _ = caps_for(m['title_height_pt'], pages_q)
    def accept(order):
        hh_ = heights_in_order(order, m['base'], m['head']); cols_, v_ = pack(hh_, caps0)
        if cols_ is None or v_ < PLAN_FREE * colh: return False
        cols_, v_ = pack(hh_, caps0, flat=PLAN_FREE * colh)
        return max(cap - sum(hh_[k] for k in c_) for cap, c_ in zip(caps0, cols_)) <= MAX_FREE * colh
    paper = L.make_form(form_no, seed, accept=accept)
    f = paper['form']; tag = 'sen0401_exam_midterm_v5_0_0'
    for ext in ('_paper.docx', '_paper.pdf', '_key.docx', '_key.pdf', '_key.json', '_sheet.pdf', '_sheet_layout.json', '_paper.ttl', '_measure.json'):
        if os.path.exists(os.path.join(outdir, tag + ext)): raise Refused('refusing to overwrite ' + tag + ext)
    tmp = tempfile.mkdtemp(dir=tmpbase)
    try:
        base = base_heights(paper, tmp); head = heading_heights(paper, tmp); T = title_height(paper, tmp)
        h = heights_in_order(paper['slots'], base, head); caps, _ = caps_for(T, pages_q)
        cols, v = pack(h, caps, flat=PLAN_FREE * colh)
        if cols is None: raise Refused('form: the sub-questions do not fit the %d question pages (best free space %.1f pt)' % (pages_q, v))
        breaks = [c[0] for c in cols[1:] if c]
        L.write_docx(paper, os.path.join(tmp, tag + '_paper.docx'), breaks=breaks)
        pdf = L.export_pdf(os.path.join(tmp, tag + '_paper.docx'), tmp)
        meas_r = measure_render(pdf, min_free, skip=1); pages = L.pdf_pages(pdf)
        worst = min(c['free_share'] for c in meas_r['columns'])
        if pages != 1 + pages_q: raise Refused('form: the paper has %d pages on the LibreOffice render, planned %d (cover + %d)' % (pages, 1 + pages_q, pages_q))
        if worst < min_free: raise Refused('form: a column keeps only %.1f percent free (minimum %.1f)' % (worst * 100, min_free * 100))
        if any(not b.get('fits') for b in meas_r['code_boxes']): raise Refused('form: a code line is wider than its box: %s' % ([x for x in meas_r['code_boxes'] if not x.get('fits')]))
        paper['contentPages'] = pages
        sp, layout = L.render_sheet(paper, os.path.join(tmp, tag + '_sheet.pdf'))
        if sp != 1: raise Refused('form: the answer sheet has %d pages, not 1' % (sp))
        paper['sheetPages'] = sp; paper['pageCount'] = pages + sp
        gr_, pid = E.to_graph(paper)
        viol = E.validate(gr_, paper['chapters'])
        gr_.serialize(os.path.join(tmp, tag + '_paper.ttl'), format='turtle')
        key = L.answer_key(paper); key.update(paper_file=tag + '_paper.docx', sheet_file=tag + '_sheet.pdf')
        json.dump(layout, open(os.path.join(tmp, tag + '_sheet_layout.json'), 'w'), indent=1)
        json.dump(key, open(os.path.join(tmp, tag + '_key.json'), 'w', encoding='utf8'), indent=1, ensure_ascii=False)
        L.write_key_docx(paper, key, os.path.join(tmp, tag + '_key.docx')); L.export_pdf(os.path.join(tmp, tag + '_key.docx'), tmp)
        meas = dict(version=VERSION, form=f, config=m['config'], cfg=dict(L.CFG), chapters=paper['chapters'], sub_questions=len(paper['slots']), units=sum(E.units(i) for i in paper['items']),
                    paper_pages=pages, question_pages=pages - 1, sheet_pages=sp, pages_total=pages + sp, key_pages=L.pdf_pages(os.path.join(tmp, tag + '_key.pdf')),
                    title_height_pt=round(T, 1), column_height_pt=round(colh, 1), heights_in_order_pt=[round(x, 1) for x in h], column_plan=[[('%d%s' % (paper['slots'][k]['q'], paper['slots'][k]['label'])) for k in c] for c in cols],
                    min_free_share=worst, min_free_required=min_free, render=meas_r,
                    order=[('%d%s' % (s['q'], s['label']), s['skey'], s['type']) for s in paper['slots']],
                    graph_violations=[(r_, s_, m_) for r_, s_, m_ in viol if s_ == 'Violation'], graph_warnings=[m_ for r_, s_, m_ in viol if s_ != 'Violation'])
        json.dump(meas, open(os.path.join(tmp, tag + '_measure.json'), 'w'), indent=1)
        for ext in ('_paper.docx', '_paper.pdf', '_key.docx', '_key.pdf', '_key.json', '_sheet.pdf', '_sheet_layout.json', '_paper.ttl', '_measure.json'):
            shutil.copy(os.path.join(tmp, tag + ext), os.path.join(outdir, tag + ext))
        return meas
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('outdir'); a.add_argument('--seed', type=int, default=5701); a.add_argument('--forms', type=int, default=1)
    a.add_argument('--min-free', type=float, default=0.03); a.add_argument('--measure-only', action='store_true')
    x = a.parse_args(); os.makedirs(x.outdir, exist_ok=True); tb = tempfile.mkdtemp(prefix='sen0401_papers5_')
    try:
        print('LAYOUT MEASUREMENT (every sub-question laid out alone in LibreOffice, + %.0f pt cushion each; the question headings measured alone):' % CUSHION)
        ms = {}
        for name in ['compact10', 'air10c', 'air10b', 'air10a', 'read105', 'read11', 'single11']:
            m = measure_config(name, x.seed, tb); ms[name] = m; c = m['cfg']
            print('  %-9s text %.1f/%.1f pt, code %.1f pt, gap %.0f pt, %d column(s): summed heights %.0f pt, title block %.0f pt, one column %.0f pt -> %.2f columns needed' %
                  (name, c['txt'], c['lead'], c['code'], c['gap'], c['cols'], m['summed_pt'], m['title_height_pt'], m['column_height_pt'], m['columns_needed']))
        m = ms['compact10']; caps2, colh = caps_for(m['title_height_pt'], 2) if not L.set_cfg('compact10') else None
        ok2, best2, _ = search_order(m, 2, 6000)
        print('4-PAGE TARGET (cover + 2 question pages of 2 columns + sheet): the most compact setting (10 pt, the smallest the print rules allow) needs %.2f columns and has 4: orders packing with the planned free share: %d of 6000, best smallest free space %.1f pt: %s' %
              (m['columns_needed'], ok2, best2, 'FITS' if ok2 else 'DOES NOT FIT'))
        plan = None
        if ok2: plan = (m, 2)
        else:
            for qpages in (4, 5, 6):        # v5: the v3 builder tried 4 question pages only; the measured heights of the v1.4.0 items need more, so pages are ADDED (nothing is shortened, no limit is relaxed)
                for name in PREFERENCE:
                    mm = ms.get(name)
                    if mm is None: continue
                    ok, best, nd = search_order(mm, qpages, 6000)
                    print('%d-PAGE PLAN (cover + %d question pages + sheet): %-9s needs %.2f columns of %d: orders packing with %.0f percent free per column: %d of %d, best smallest free space %.1f pt (%.1f percent)' %
                          (qpages + 2, qpages, name, mm['columns_needed'], (mm['cfg']['cols'] * qpages), PLAN_FREE * 100, ok, nd, best, 100 * best / mm['column_height_pt']))
                    if ok and best >= ROBUST_FREE * mm['column_height_pt'] and plan is None: plan = (mm, qpages)
                if plan is not None: break
        if plan is None: print('REFUSED no layout fits'); sys.exit(2)
        choice, qp = plan
        print('CHOSEN: %s with %d question pages -> %d pages in all (cover + %d + answer sheet)' % (choice['config'], qp, 1 + qp + 1, qp))
        if x.measure_only: sys.exit(0)
        for fno in range(1, x.forms + 1):
            try: m = build_form(x.outdir, fno, x.seed + fno - 1 if fno > 1 else x.seed, x.min_free, tb, choice, qp)
            except (Refused, E.ExamRefused, RuntimeError) as e:
                print('REFUSED', e); sys.exit(2)
            f = m['form']
            print('PAPER seed %d code %s: paper %d pages (cover + %d) + sheet %d page = %d; key %d page(s); min free %.1f percent; order draws %d' %
                  (f['seed'], f['code'], m['paper_pages'], m['question_pages'], m['sheet_pages'], m['pages_total'], m['key_pages'], m['min_free_share'] * 100, f['order_draws']))
            for c in m['render']['columns']: print('   page %d column %d: lowest line %.1f pt, free %.1f pt = %.1f percent of the column' % (c['page'], c['column'], c['lowest_line_pt'], c['free_pt'], c['free_share'] * 100))
            for b in m['render']['code_boxes']: print('   code box page %d: %s' % (b['page'], b))
            print('   fonts on the render:', m['render']['fonts'])
            print('   graph violations:', m['graph_violations'], ' warnings:', len(m['graph_warnings']))
    finally:
        shutil.rmtree(tb, ignore_errors=True)
