"""Answer sheet reader, version 1.1.0 (repair of v1.0.0). The sheet itself (layout, renderer, check digit, rasteriser, registration, naive reader) is the v1.0.0 module, imported unchanged;
this file replaces only the reading of marks. Pure library (no output when imported).
WHAT WAS WRONG IN v1.0.0 (root cause, shown on the failing rows of the register-v0.647 control):
 (a) a written number box was judged by the share of pixels darker than grey 140. A thin pen stroke that the scan blurs has a grey above 140, so a box that really holds a number
     (seed 9108, box 31: five digits written, binarised ink 0.0138 against a limit of 0.02) was read as empty. The amount of ink was there; the test threw it away.
 (b) a faint mark was judged the same way, on the share of pixels darker than grey 140 inside the bubble. A very light mark (stripes narrower than one pixel after the blur) leaves
     nearly nothing under grey 140, so the bubble is called empty; a bank code with two faint rows was then read as 'blank' with no flag. A faint mark in a choice row was only caught by chance,
     through the block closure (an undeclared blank row), not by the reading itself.
THE REPAIR: the amount of ink is measured as integrated optical density, not by a hard threshold: for each pixel (paper grey - pixel grey) / (paper grey - pen grey 45), clipped to 0..1,
 where the paper grey is the median of the registered page (the paper level of that scan). Blur and noise leave the integrated amount nearly unchanged, so a thin or faint stroke keeps its weight.
 Written number box: od >= T_H_WRITTEN is a written number; od < T_H_BLANK is blank; in between the box is held with the flag 'faint' (it is never read as blank and never as a value).
 Row of bubbles: v1.0.0 behaviour is kept for every row that has a clearly filled bubble. A row WITHOUT a filled bubble, in which a bubble that is not struck holds ink (od >= T_INK_OD),
 is flagged 'faint' (held for a person); it is read as blank only if no bubble holds ink.
Thresholds were fixed on the calibration seeds only (1000-1099 and 2000-2199): see the measurement file. Nothing else of v1.0.0 is changed."""
import collections, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v1_0_0 as A0
from sen0401_exam_answersheet_v1_0_0 import (PW, PH, MARG, BR, S, DPI, BLOCK_MAX, damm_check, damm_valid, make_code, serial_width, default_spec, build_layout, render, write_pair,
                                              rasterise, register, bubble_features, classify, read_naive, T_FILLED, T_FAINT, T_CORNERS, T_CORNER_INK)
VERSION = '1.1.0'
PEN_GREY = 45.0
T_INK_OD = 0.03          # a bubble that is not struck and not filled holds a mark when its mean optical density inside the ring is at least this
T_H_BLANK = 0.02         # number box: below this it is blank
T_H_WRITTEN = 0.035      # number box: from this it is a written number; between the two it is held ('faint')

def paper_grey(img):
    import numpy as np
    return float(np.median(img))

def bubble_od(img, cx, cy, paper):
    import numpy as np
    if A0._M is None: A0._M = A0._masks()
    h, inner, quad = A0._M
    px, py = int(round(cx * S)), int(round(cy * S))
    cell = img[py - h:py + h + 1, px - h:px + h + 1].astype(np.float32)
    if cell.shape != inner.shape: return 0.0
    d = np.clip((paper - cell) / (paper - PEN_GREY), 0, 1)
    return float(d[inner].mean())

def human_od(img, bx, paper):
    """The largest mean optical density in any one digit box, with 3 pt kept off the printed lines."""
    import numpy as np
    best = 0.0
    for i in range(int(round(bx['w'] / 18))):
        x1, x2 = int((bx['x'] + i * 18 + 3) * S), int((bx['x'] + i * 18 + 15) * S); y1, y2 = int((bx['y'] + 3) * S), int((bx['y'] + bx['h'] - 3) * S)
        c = img[y1:y2, x1:x2].astype(np.float32)
        best = max(best, float(np.clip((paper - c) / (paper - PEN_GREY), 0, 1).mean()))
    return best

def human_state(ink):
    return 'written' if ink >= T_H_WRITTEN else ('blank' if ink < T_H_BLANK else 'faint')

def read_row(img, row, paper):
    st = [classify(*bubble_features(img, cx, row['cy'])) for cx in row['cx']]
    filled = [i for i, s in enumerate(st) if s == 'filled']; faint = [i for i, s in enumerate(st) if s == 'faint']
    if len(filled) == 1 and not faint: return row['opts'][filled[0]], None
    if len(filled) >= 2: return None, 'double'
    if faint: return None, 'faint'
    if any(s == 'empty' and bubble_od(img, cx, row['cy'], paper) >= T_INK_OD for s, cx in zip(st, row['cx'])): return None, 'faint'    # v1.1.0: ink below the old threshold is a mark nobody can call
    return None, 'blank'

def read_sheet(imgs, layout, check_digits=True, closure=True):
    """Same contract and same closure logic as v1.0.0; only the reading of rows and number boxes differs (see the module text)."""
    out = {}; blockstate = []
    papers = [paper_grey(im) for im in imgs]
    region_of = {}; r = -1; prev = None
    for b in layout['blocks']:
        if b['kind'] != prev: r += 1; prev = b['kind']
        region_of[b['id']] = r
    region_answered = collections.defaultdict(bool)
    for b in layout['blocks']:
        img = imgs[b['page']]; pp = papers[b['page']]
        for u in b['units']:
            if u['kind'] == 'human': region_answered[region_of[b['id']]] |= human_od(img, u['box'], pp) >= T_H_BLANK
            else: region_answered[region_of[b['id']]] |= any(read_row(img, row, pp)[1] != 'blank' for row in u['rows'])
    for b in layout['blocks']:
        img = imgs[b['page']]; pp = papers[b['page']]; blank = set(); res = {}
        for u in b['units']:
            if u['kind'] == 'human':
                ink = human_od(img, u['box'], pp); stt = human_state(ink)
                res[u['no']] = {'value': 'WRITTEN' if stt == 'written' else None, 'flag': None if stt == 'written' else ('faint' if stt == 'faint' else 'blank'), 'ink': ink}
                if stt == 'blank': blank.add(u['no'])
                continue
            vals = []; flags = []
            for row in u['rows']:
                v, fl = read_row(img, row, pp); vals.append(v); flags.append(fl)
            if u['kind'] == 'bank':
                if all(f == 'blank' for f in flags): res[u['no']] = {'value': None, 'flag': 'blank'}; blank.add(u['no'])
                elif any(f in ('double', 'faint') for f in flags): res[u['no']] = {'value': None, 'flag': [f for f in flags if f and f != 'blank'][0]}
                elif any(f == 'blank' for f in flags): res[u['no']] = {'value': None, 'flag': 'incomplete'}
                else:
                    code = ''.join(vals)
                    if check_digits and not damm_valid(code): res[u['no']] = {'value': code, 'flag': 'check-digit'}
                    else: res[u['no']] = {'value': code, 'flag': None}
            else:
                v, fl = vals[0], flags[0]
                res[u['no']] = {'value': v, 'flag': None if fl in (None, 'blank') else fl}
                if fl == 'blank': blank.add(u['no'])
        declared = set()
        for q in b['closure']:
            fin, cor = bubble_features(img, q['cx'], q['cy'])
            if classify(fin, cor) in ('filled',): declared.add(q['no'])
        reg_id = region_of[b['id']]
        declared_filled = declared - blank
        undeclared_blank = (blank - declared) if region_answered[reg_id] else set()
        blockstate.append({'id': b['id'], 'blank': sorted(blank), 'declared': sorted(declared), 'declared_filled': sorted(declared_filled),
                           'undeclared_blank': sorted(undeclared_blank), 'mismatch': bool(closure and (declared_filled or undeclared_blank))})
        for no, r in res.items(): out[no] = r
    held = set()
    if closure:
        for i, st in enumerate(blockstate):
            if st['mismatch']: held.add(i)
            if st['declared_filled']:
                for j in range(i + 1, len(blockstate)):
                    if layout['blocks'][j]['kind'] != layout['blocks'][i]['kind']: break
                    held.add(j)
                    if blockstate[j]['undeclared_blank']: break
        for i, st in enumerate(blockstate):
            if st['undeclared_blank'] and layout['blocks'][i]['units'][-1]['no'] in st['undeclared_blank'] and (i + 1 == len(blockstate) or layout['blocks'][i + 1]['kind'] != layout['blocks'][i]['kind']):
                j = i
                while j >= 0 and layout['blocks'][j]['kind'] == layout['blocks'][i]['kind']: held.add(j); j -= 1
    for i in held:
        for u in layout['blocks'][i]['units']:
            r = out[u['no']]
            if r['flag'] is None: r['flag'] = 'held-block'
    return out, blockstate, sorted(held)
