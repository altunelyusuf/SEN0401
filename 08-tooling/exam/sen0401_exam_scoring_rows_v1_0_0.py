"""SEN0401 exam scoring ROW-POINTS adapter, version 1.0.0 (new file). Holds no question and no answer.
WHY: the scoring module v2.0.0 reads ONE number 'points_per_part' for every row of a matching or ordering unit. The v7 items carry whole-number row points that are NOT equal inside a unit
(measured on the real structure v1.3.0: ordering rows 1, 2, 2, 2, 1; matching rows 3, 2, 2, 2; no equal whole-number split of 8 over 5 rows exists). The module cannot be edited (committed). This adapter
leaves the module file untouched: it calls the module's own functions with the module's marks_of_key replaced IN MEMORY by a wrapper that takes the row points from the key field 'row_points' (a dict label -> points).
Everything else (right/wrong/blank/double, the exact match, the blind chances, the exact blind figure) is the module's own code.
A key whose matching or ordering unit has no 'row_points' and no 'points_per_part' is refused (KeyError from the module), never guessed.
Usage as a library: score(marks, key), expected_blind(key), perfect_marks(key), blind_marks(key, rng), marks_of_key(key), sum_of_row_points_check(key)."""
import contextlib, copy, sys
sys.dont_write_bytecode = True
import sen0401_exam_scoring_v2_0_0 as SC
VERSION = '1.0.0'
_ORIG = SC.marks_of_key


def _prepared(key):
    k = copy.deepcopy(key)
    for it in k['items']:
        rp = it.get('row_points')
        if rp and 'points_per_part' not in it: it['points_per_part'] = next(iter(rp.values()))      # placeholder only so that the module can read the key; replaced below per label
    return k


def marks_of_key(key):
    out = _ORIG(_prepared(key)); rows = {}
    for it in key['items']:
        for lab, v in (it.get('row_points') or {}).items(): rows[lab] = SC.F(str(v))
    for m in out:
        if m['label'] in rows: m['points'] = rows[m['label']]
    return out


@contextlib.contextmanager
def patched():
    SC.marks_of_key = marks_of_key
    try: yield
    finally: SC.marks_of_key = _ORIG


def score(marks, key):
    with patched(): return SC.score(marks, key)


def expected_blind(key):
    with patched(): return SC.expected_blind(key)


def perfect_marks(key):
    with patched(): return SC.perfect_marks(key)


def blind_marks(key, rng):
    with patched(): return SC.blind_marks(key, rng)


def row_points_agree(key):
    """Every unit with rows: the row points add up to the unit's points. Returns the list of units that do not."""
    bad = []
    for it in key['items']:
        rp = it.get('row_points')
        if rp and sum(rp.values()) != it['points']: bad.append((it['label'], sum(rp.values()), it['points']))
    return bad
