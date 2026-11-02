#!/usr/bin/env python3
"""SEN0401 midterm v8.0.0, step X3a-1: assemble the merged items file, the worked-solutions file and the structure file of the delivered set from the CONTROLLED item files.
Holds no question and no answer: every text is read from the files named on the command line (private CME files); nothing of an item is printed.
Inputs  (all by path): --base-items (items v1.8.0), --base-solutions (key solutions v1.8.0), --base-structure (structure v1.5.1),
        --x2 (the wording file: printed 1c, 3c, 4a-4b), --numeric (eight numeric item files, 2a..2h, in any order; each names the old key it replaces).
Outputs (new files, refuses to overwrite): items v8.0.0, solutions v8.0.0, structure v1.6.0, and a map file (old key -> new key, file, sha256).
Rules kept: same structure labels, same points, same position slots, same chapters and Bloom level as the item it replaces; numeric key recomputed by RUNNING the item's own code;
an item file without a running recompute, or with a key that differs from it, refuses the assembly (exit 2)."""
import argparse, copy, hashlib, json, os, re, sys
from fractions import Fraction
sys.dont_write_bytecode = True
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
fmt = lambda v: '{:,}'.format(int(v))


def last_sentence(stem):
    last = stem.rstrip().split('\n')[-1]
    return 'You are asked' + last.split('You are asked', 1)[1]


def numbers_of(text):
    m = re.findall(r'\d[\d,]*(?:\.\d+)?', text)
    return m[-1].replace(',', '') if m else ''


def convert(nf, old):
    """New numeric item file (schema X1a or X1b) -> an item in the items-file format, on a copy of the old item it replaces (same chapters, Bloom, source)."""
    new = copy.deepcopy(old)
    x1b = 'recompute' in nf
    ns = {}
    if x1b: exec(nf['recompute'], ns); rv = ns['recompute']()
    else: exec(nf['recompute_python'], ns); rv = ns['recompute'](nf['data'])
    if rv != nf['key_value']: raise SystemExit('REFUSED: %s recompute %r differs from the key %r' % (nf['key'], rv, nf['key_value']))
    vals = [int(str(o).replace(',', '')) for o in nf['options']]
    if len(set(vals)) != 5 or vals[nf['key_index']] != rv: raise SystemExit('REFUSED: %s options or key index' % nf['key'])
    wrong = {int(str(k).replace(',', '')): v for k, v in (nf['wrong_why'] if x1b else nf['why_wrong']).items()}
    if set(wrong) != set(vals) - {rv}: raise SystemExit('REFUSED: %s wrong values lack a reason' % nf['key'])
    steps = nf['solution_steps']
    nums = nf['solution_step_numbers'] if x1b else [numbers_of(s) for s in steps]
    if nums[-1] != str(rv): raise SystemExit('REFUSED: %s last step number is not the key' % nf['key'])
    why_q = nf['why_this_question']; why_right = nf['why_right'] if x1b else re.sub(r'^Why this question:\s*', '', why_q)
    cp = nf['cp'] if x1b else nf['critical_point']
    new['key'] = nf['key']; new['q'] = nf['stem']; new['key_value'] = rv; new['unit'] = nf['unit']; new['tolerance'] = 0
    new['answer_digits'] = len(str(rv)); assert nf['answer_digits'] == len(str(rv)), nf['key']
    new['tip'] = nf['tip']; new['needs_tip'] = True
    new['how_to_answer'] = nf['format_line'] if x1b else nf['how_to_answer']; new['format_line'] = new['how_to_answer']
    new['intent'] = last_sentence(nf['stem'])
    new['critical_points'] = [c.strip() for c in re.split(r'[/,]', cp)]
    new['understanding'] = why_q
    new['computed'] = 'run: ' + ' ; '.join(steps) + ' (recompute by the item code gives %d)' % rv
    new['data'] = nf['data'] if not x1b else {'model': 'direct', 'recompute_code': nf['recompute']}
    new['numeric_alternatives'] = vals
    new['solution'] = dict(steps=[dict(text=t, number=n) for t, n in zip(steps, nums)], why_right=why_right,
                           why_wrong={fmt(k): wrong[k] for k in vals if k != rv})
    new['why_this_question'] = why_q
    for k in ('v1_7_0_changes', 'v1_8_0_changes', 'merge_edits', 'merged_origin', 'merged_v1_8_0', 'computed_old', 'terms', 'abbreviations', 'from_item', 'replaces'):
        if k in new and k not in ('terms', 'abbreviations'): new.pop(k)
    new['terms'] = []; new['abbreviations'] = {}
    new['from_item'] = [old['key']]; new['replaces'] = [old['key']]
    new['v8_0_0_changes'] = ['numeric rewrite (X1a/X1b): new numbers, one or two plain steps; same course point, points and position as %s' % old['key']]
    new['v8_source_file'] = nf['_file']; new['v8_source_sha256'] = nf['_sha']
    return new


def solution_lines(it, label):
    s = it['solution']; L = ['Task: ' + it['intent'], 'Correct answer: %s %s (exact; no partial credit).' % (fmt(it['key_value']), it['unit'])]
    for n, st in enumerate(s['steps'], 1): L.append('Step %d. %s' % (n, st['text']))
    if s['why_right'] and it['why_this_question'] != 'Why this question: ' + s['why_right']: L.append('Why this is right: ' + s['why_right'])
    L.append(it['why_this_question'])
    for v in it['numeric_alternatives']:
        if fmt(v) in s['why_wrong']: L.append('If a student writes %s: %s' % (fmt(v), s['why_wrong'][fmt(v)]))
    return L


def main():
    a = argparse.ArgumentParser()
    for n in ('base-items', 'base-solutions', 'base-structure', 'x2', 'out-items', 'out-solutions', 'out-structure', 'out-map'): a.add_argument('--' + n, required=True)
    a.add_argument('--numeric', nargs=8, required=True); x = a.parse_args()
    for p in (x.out_items, x.out_solutions, x.out_structure, x.out_map):
        if os.path.exists(p): raise SystemExit('REFUSED: exists ' + p)
    base = json.load(open(x.base_items, encoding='utf8')); byk = {i['key']: i for i in base['items']}
    sols = json.load(open(x.base_solutions, encoding='utf8')); sbyk = {e['key']: e for e in sols['items']}
    S = json.load(open(x.base_structure, encoding='utf8'))
    x2 = {i['key']: i for i in json.load(open(x.x2, encoding='utf8'))}
    newitems = dict(byk); replaced = {}; mapping = []
    # wording items: the X2 file holds the whole item; only 'q' (and for 4a-4b nothing) differs from items v1.8.0 besides the note field x2
    for k, it in x2.items():
        d = [f for f in set(it) | set(byk[k]) if it.get(f) != byk[k].get(f) and f != 'x2']
        if not set(d) <= {'q', 'alternatives'}: raise SystemExit('REFUSED: X2 item %s differs from items v1.8.0 in %s' % (k, d))
        for f in ('options', 'answer', 'steps', 'blanks', 'distractors', 'premises', 'responses', 'key', 'type', 'row_points', 'tip'):
            if it.get(f) != byk[k].get(f): raise SystemExit('REFUSED: X2 item %s changes %s' % (k, f))
        newitems[k] = copy.deepcopy(it); newitems[k]['v8_0_0_changes'] = ['wording-only fix from the X2 file (stem text); key and option set unchanged']
        mapping.append(dict(old=k, new=k, file=os.path.basename(x.x2), sha256=sha(x.x2), kind='wording'))
    nsol = {}
    for p in x.numeric:
        nf = json.load(open(p, encoding='utf8')); nf['_file'] = os.path.basename(p); nf['_sha'] = sha(p)
        ok = nf.get('replaces_key') or nf.get('old_key'); old = byk[ok]
        it = convert(nf, old)
        if (it['points'] if 'points' in it else None) not in (None, nf['points']): raise SystemExit('REFUSED: points of ' + nf['key'])
        if nf['points'] != old.get('points', nf['points']): raise SystemExit('REFUSED: points differ for ' + ok)
        del newitems[ok]; newitems[it['key']] = it; replaced[ok] = it['key']
        mapping.append(dict(old=ok, new=it['key'], file=os.path.basename(p), sha256=sha(p), kind='numeric', key_value=it['key_value'], unit=it['unit'], digits=it['answer_digits']))
    if len(replaced) != 8: raise SystemExit('REFUSED: %d numeric items replaced, expected 8' % len(replaced))
    # items file in the order of the base file
    order = [replaced.get(i['key'], i['key']) for i in base['items']]
    out = dict(base); out['items'] = [newitems[k] for k in order]; out['version'] = '8.0.0'
    out['note'] = 'SEN0401 midterm authored items, version 8.0.0 (assembled by X3a from the controlled item files: numeric 2a-2h new numbers; printed 1c and 3c stems from the X2 wording file; 4a-4b unchanged). PRIVATE exam material. | ' + base['note']
    out['derived_from'] = [os.path.basename(x.base_items), os.path.basename(x.x2)] + [os.path.basename(p) for p in x.numeric]
    out['parts_sha256'] = {os.path.basename(x.base_items): sha(x.base_items), os.path.basename(x.x2): sha(x.x2), **{os.path.basename(p): sha(p) for p in x.numeric}}
    json.dump(out, open(x.out_items, 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    # solutions: unchanged entries copied, numeric entries rebuilt, wording entries copied (their lines do not quote the stem wording)
    ns = dict(sols); ns['items'] = []
    for e in sols['items']:
        k = e['key']
        if k in replaced:
            it = newitems[replaced[k]]; lab = list(e['lines_by_label'])[0]
            e2 = dict(e); e2['key'] = it['key']; e2['lines_by_label'] = {lab: solution_lines(it, lab)}; ns['items'].append(e2)
        else: ns['items'].append(copy.deepcopy(e))
    ns['version'] = '8.0.0'; ns['note'] = 'Worked solutions of the set v8.0.0 (numeric entries rebuilt from the controlled numeric item files; the others copied from solutions v1.8.0). | ' + sols.get('note', '')
    ns['derived_from'] = [os.path.basename(x.base_solutions)]
    json.dump(ns, open(x.out_solutions, 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    # structure: same questions, labels, points; item references, digit counts, chances, tips and format lines of the eight numeric sub-questions updated
    S2 = copy.deepcopy(S); S2['version'] = '1.6.0'; S2['derived_from'] = os.path.basename(x.base_structure)
    S2['items_file'] = 'private/' + os.path.basename(x.out_items)
    S2['items_file_note'] = S['items_file_note']
    blind = Fraction(15); digs = set()
    for q in S2['questions']:
        for sub in q['sub']:
            if sub['item'] in replaced:
                it = newitems[replaced[sub['item']]]; d = it['answer_digits']
                sub['item'] = it['key']; sub['how_to_answer'] = it['how_to_answer']; sub['tip'] = it['tip']
                sub['chance'] = '1/%d' % 10 ** d; sub['chance_basis'] = 'a blind number must hit all %d digits of the key: 1 in 10 to the %d' % (d, d); sub['chance_value'] = 10.0 ** -d; sub['answer_digits'] = d
                blind += Fraction(sub['points'], 10 ** d); digs.add(d)
    S2['chance_by_type'] = dict(S['chance_by_type']); S2['chance_by_type']['NumericAnswer'] = ['1/%d' % 10 ** d for d in sorted(digs)]
    S2['blind_total_exact'] = dict(fraction='%d/%d' % (blind.numerator, blind.denominator), decimal=float(blind), closed_units_points=75, closed_units_blind=15,
                                   note='closed units 75 of 100 points, exactly 15 blind; the 8 hand calculations add the rest with the digit counts of the v8.0.0 keys')
    S2['v1_6_0_changes'] = ['items file is items v8.0.0 (numeric 2a-2h new, 1c and 3c wording)', 'item references, digit counts, chances, tips and format lines of the eight numeric sub-questions follow the new items', 'labels, points, chapters, Bloom levels unchanged']
    json.dump(S2, open(x.out_structure, 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    json.dump(dict(items=mapping, structure=os.path.basename(x.out_structure), blind_exact=S2['blind_total_exact']['fraction']), open(x.out_map, 'w'), indent=1)
    tp = sum(s['points'] for q in S2['questions'] for s in q['sub'])
    assert tp == S['total_points'] == 100 and all(sum(s['points'] for s in q['sub']) == q['points'] for q in S2['questions'])
    print('assembled: %d items (%d numeric replaced, %d wording items), points %d, per-question points unchanged, blind exact %s' % (len(out['items']), len(replaced), len(x2), tp, S2['blind_total_exact']['fraction']))
    for m in mapping: print('  %s -> %s  [%s %s]' % (m['old'], m['new'], m['kind'], m['sha256'][:12]))


main()
