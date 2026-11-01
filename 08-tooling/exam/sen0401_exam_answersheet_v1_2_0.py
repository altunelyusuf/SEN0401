"""Answer sheet reader, version 1.2.0 (repair of the cross-gap shift miss of v1.1.0). v1.0.0 and v1.1.0 are imported UNCHANGED; this file adds only what the reader lacked.
WHAT WAS WRONG IN v1.1.0 (measured 2026-10-30, control sen0401_exam_reader_gap_control_v1_0_0.py): the block closure follows a run of blocks of ONE kind and stops where another kind begins.
On a paper whose choice items are interleaved with other kinds (the midterm CHAPTER-ORDER layout) a skipped-row shift that begins in one block runs on across such a gap unflagged
(seeds 41000-41039: 17 rows on 7 of 40 sheets; 52000-52199: 91 rows on 28 of 200 sheets).
THE REPAIR: the two cross-gap screens of the grading tool v1.0.0 (extend_holds, G7) are built into the reader, applied across gaps on every layout:
  backward: the LAST answer place of the LAST block of a kind is blank and not declared -> every earlier block of that kind is held (a run shift leaves exactly this blank at its end);
  forward : a block with a declared place that holds a mark -> every later block of that kind is held up to the first block with an undeclared blank.
Held places that the reader left unflagged get the flag 'held-block', like the reader's own holds.
SECOND DEFECT FOUND BY THE CONTROL (seed 62050, default layout, a miss that v1.1.0 has too): the v1.0.0 'struck' test counts dark corners of the bubble cell. The arms of a strike (up to 10.2 pt) of a bubble in the row above and below
(and in the next column) reach into the corners of this bubble's cell. A bubble that is really filled (a second mark of a double) and sits between two struck bubbles of its column showed 3 or 4 dark corners, was called 'struck' (a cancelled answer),
and the row was accepted with the other mark. THE REPAIR (new in v1.2.0): a bubble called 'struck' with another struck bubble within 20.5 pt (centre to centre: 8.5 pt cell + 10.2 pt arm + 1.8 pt allowance) cannot be told from a neighbour's strike;
it counts as a MARK (filled when its ink share is at least T_FILLED, else faint). A true strike beside another strike is then held for a person (the safe direction: a hold, never a missed double). Thresholds and read_row otherwise are v1.1.0.
Pure library."""
import collections, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v1_1_0 as R1
from sen0401_exam_answersheet_v1_1_0 import *            # the v1.0.0 and v1.1.0 names stay available unchanged
VERSION = '1.2.0'
NEIGH_PT = 20.5

def ambiguous_strikes(imgs, layout):
    """Set of (page, cx, cy) of bubbles that v1.0.0 calls 'struck' and that have another 'struck' bubble within NEIGH_PT."""
    pts = []
    for b in layout['blocks']:
        for u in b['units']:
            if u['kind'] in ('human',) or 'rows' not in u or u['kind'] == 'bank': continue
            for row in u['rows']:
                for cx in row['cx']:
                    if classify(*bubble_features(imgs[b['page']], cx, row['cy'])) == 'struck': pts.append((b['page'], cx, row['cy']))
    return {p for p in pts if any(q != p and q[0] == p[0] and ((q[1] - p[1]) ** 2 + (q[2] - p[2]) ** 2) ** .5 <= NEIGH_PT for q in pts)}

def make_read_row(amb):
    def read_row(img, row, paper, page=None):
        st = []
        for cx in row['cx']:
            fin, cor = bubble_features(img, cx, row['cy']); c = classify(fin, cor)
            if c == 'struck' and (page, cx, row['cy']) in amb: c = 'filled' if fin >= T_FILLED else 'faint'
            st.append(c)
        filled = [i for i, s in enumerate(st) if s == 'filled']; faint = [i for i, s in enumerate(st) if s == 'faint']
        if len(filled) == 1 and not faint: return row['opts'][filled[0]], None
        if len(filled) >= 2: return None, 'double'
        if faint: return None, 'faint'
        if any(s == 'empty' and bubble_od(img, cx, row['cy'], paper) >= T_INK_OD for s, cx in zip(st, row['cx'])): return None, 'faint'
        return None, 'blank'
    return read_row

def extend_holds(layout, out, bst, held):
    blocks = layout['blocks']; held = set(held); by_kind = collections.defaultdict(list)
    for i, b in enumerate(blocks): by_kind[b['kind']].append(i)
    for kind, idx in by_kind.items():
        last = idx[-1]; lastno = blocks[last]['units'][-1]['no']
        if lastno in bst[last]['blank'] and lastno not in bst[last]['declared']: held.update(i for i in idx if i < last)
        for i in idx:
            if bst[i]['declared_filled']:
                for j in idx:
                    if j <= i: continue
                    held.add(j)
                    if bst[j]['undeclared_blank']: break
    for i in held:
        for u in blocks[i]['units']:
            if out[u['no']]['flag'] is None: out[u['no']]['flag'] = 'held-block'
    return sorted(held)

def read_sheet(imgs, layout, check_digits=True, closure=True):
    """v1.1.0 reading with the neighbour-strike rule, then (when closure is on) the cross-gap holds. Same contract: (out, blockstate, held).
    The v1.1.0 function is run with its row reader swapped for the v1.2.0 one for the duration of the call (the v1.1.0 file itself is not changed)."""
    amb = ambiguous_strikes(imgs, layout); page_of = {id(im): p for p, im in enumerate(imgs)}; rr = make_read_row(amb); old = R1.read_row
    R1.read_row = lambda img, row, paper: rr(img, row, paper, page_of[id(img)])
    try: out, bst, held = R1.read_sheet(imgs, layout, check_digits, closure)
    finally: R1.read_row = old
    if closure: held = extend_holds(layout, out, bst, held)
    return out, bst, held
