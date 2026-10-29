"""Checks of the answer sheet and the answering methods, version 1.0.0. Prints PASS / FAIL per check; exit 1 on any FAIL. Written by the executor of the task; run by the control on the evidence bridge.
Usage: check.py [--log FILE] [--sheets 200]
Criteria are fixed here BEFORE the evaluation run (evaluation seeds 9000 and up; the reader's thresholds were set on the calibration seeds 1000 to 1099):
 C6: no registration failure; with the methods no silent wrong answer and no missed ambiguous row; every code slip and swap detected; the reader without the methods makes at least one
     silent wrong answer or misses at least one ambiguous row (so the methods change something); at most 25 percent of recoverable rows are held for a person.
C1 no tracked file edited      C2 sheet builds twice to identical bytes, geometry is sound      C3 a blank sheet reads blank with no flag, and its layout is registered on a scan
C4 the check digit, exhaustively  C5 sheet description conforms to the sheet shapes, and each negative control fails exactly its rule  C6 the measurement on synthetic filled sheets
C7 the sheet conforms to the printed-paper rules (R01 to R22) and the negative controls fail  C8 page cost and capacity  C9 registry and questions are complete"""
import argparse, collections, hashlib, json, os, subprocess, sys, tempfile, shutil, glob
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
from rdflib import Graph, Namespace, RDF, Literal, XSD
import pyshacl
import sen0401_exam_answersheet_v1_0_0 as A
import sen0401_exam_answersheet_measure_v1_0_0 as MS
import sen0401_exam_answersheet_describe_v1_0_0 as D
import sen0401_exam_pagesave_measure_v1_0_0 as PM
SH = Namespace('http://www.w3.org/ns/shacl#'); PR = Namespace('http://example.org/sen0401/paperrules#'); AS = Namespace('http://example.org/sen0401/answersheet#'); AM = Namespace('http://example.org/sen0401/answermethods#')
V = lambda stem, ext='ttl': os.path.join(HERE, 'sen0401_exam_%s_v1_0_0.%s' % (stem, ext))
ap = argparse.ArgumentParser(); ap.add_argument('--log'); ap.add_argument('--sheets', type=int, default=200); args = ap.parse_args()
res = []
def rep(name, ok, detail=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail), flush=True)
work = tempfile.mkdtemp(prefix='sen0401_as_chk_')
try:
    g = subprocess.run(['git', '-C', HERE, 'status', '--porcelain'], capture_output=True, text=True)
    bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
    rep('C1 no committed file is edited', g.returncode == 0 and not bad, ' '.join(bad[:5]))

    spec = A.default_spec(); lay = A.build_layout(spec)
    p1 = os.path.join(work, 'a.pdf'); p2 = os.path.join(work, 'b.pdf'); A.render(lay, p1); A.render(A.build_layout(A.default_spec()), p2)
    same = hashlib.sha256(open(p1, 'rb').read()).hexdigest() == hashlib.sha256(open(p2, 'rb').read()).hexdigest()
    pts = []
    for b in lay['blocks']:
        for u in b['units']:
            for r in u['rows']:
                for cx in r['cx']: pts.append((b['page'], cx, r['cy']))
        for q in b['closure']: pts.append((b['page'], q['cx'], q['cy']))
    arr = np.array([(p, x, y) for p, x, y in pts]); mind = 1e9
    for pg in set(arr[:, 0]):
        s = arr[arr[:, 0] == pg][:, 1:]; d = np.sqrt(((s[:, None, :] - s[None, :, :]) ** 2).sum(-1)); np.fill_diagonal(d, 1e9); mind = min(mind, d.min())
    inside = all(A.MARG - 1 <= x - A.BR and x + A.BR <= A.PW - A.MARG + 1 and A.MARG <= y - A.BR and y + A.BR <= A.PH - A.MARG for _, x, y in pts)
    rep('C2 deterministic build and sound geometry', same and mind >= 2 * A.BR + 3 and inside, 'identical bytes=%s; smallest gap between bubble centres %.1f pt (need %.1f); all inside the margins=%s; %d bubbles' % (same, mind, 2 * A.BR + 3, inside, len(pts)))

    png = A.rasterise(p1, os.path.join(work, 'blank')); img = np.array(Image.open(png[0]).convert('L'))
    reg = [A.register(img, lay, 0)]; out, bs, held = A.read_sheet(reg, lay)
    flags = {k: v for k, v in out.items() if v['flag'] not in (None, 'blank')}; vals = {k: v['value'] for k, v in out.items() if v['value'] is not None}
    rep('C3 a blank sheet reads blank: no value, no flag, no block held', not flags and not vals and not held and reg[0] is not None, 'rows %d, flags %d, values %d, held blocks %d' % (len(out), len(flags), len(vals), len(held)))

    ex = MS.exhaustive_codes(); bad_ex = [(k, v) for k, v in ex.items() if isinstance(k, int) and (v['undetected'] or v['swaps_undetected'])]
    for k, v in ex.items(): print('     %s: %s' % (k, v))
    rep('C4 check digit: every single-digit slip and adjacent swap of every code of 2 to 5 digits is detected', not bad_ex and ex[5]['substitutions'] == 450000, '%s' % bad_ex)

    shapes_as = Graph().parse(V('answersheet_shapes')); gdesc, meas, codes = D.describe(lay, p1)
    def run_as(gr):
        c, rg, t = pyshacl.validate(gr, shacl_graph=shapes_as, advanced=True, inference='none', js=False)
        return c, {str(rg.value(r, SH.resultMessage)).split()[0] for r in rg.subjects(SH.resultSeverity, None)}
    c0, m0 = run_as(gdesc); print('     measured pdf: %s' % meas)
    FX = Namespace('http://example.org/sen0401/answersheet/instance#')
    def mutate(fn):
        gg = Graph(); [gg.add(t) for t in gdesc]; fn(gg); return gg
    neg = {
      'S01': lambda gg: gg.set((FX['unit_1'], AS.placeCount, Literal(2, datatype=XSD.integer))),
      'S02': lambda gg: gg.set((FX['unit_2'], AS.numberAtBothEnds, Literal(False))),
      'S03': lambda gg: gg.set((FX['block0'], AS.closureBubbles, Literal(4, datatype=XSD.integer))),
      'S04': lambda gg: (gg.set((FX['block0'], AS.unitCount, Literal(6, datatype=XSD.integer))), gg.set((FX['block0'], AS.closureBubbles, Literal(6, datatype=XSD.integer)))),
      'S05': lambda gg: gg.set((FX['code3'], AS.checkValid, Literal(False))),
      'S06': lambda gg: gg.remove((FX['sheet'], AS.hasRule, FX['rule_StrikeVoids'])),
      'S07': lambda gg: gg.set((FX['sheet'], AS.fiducialCount, Literal(3, datatype=XSD.integer))),
      'S08': lambda gg: gg.set((FX['sheet'], AS.fontPt, Literal(9, datatype=XSD.integer))),
      'S09': lambda gg: gg.set((FX['sheet'], AS.formCode, Literal('12'))),
      'S10': lambda gg: gg.set((FX['sheet'], AS.thresholdFaint, Literal('0.7', datatype=XSD.decimal))),
    }
    wrong = []
    for rid, fn in neg.items():
        c, m = run_as(mutate(fn))
        if c or m != {rid}: wrong.append((rid, sorted(m)))
    rules_in_shapes = sorted({str(m).split()[0] for m in shapes_as.objects(None, SH.message)})
    rep('C5 sheet description conforms to the sheet shapes; each of %d negative controls fails exactly its own rule' % len(neg), c0 and not m0 and not wrong and set(rules_in_shapes) == set(neg), 'rules %s; wrong %s' % (rules_in_shapes, wrong))
    # the description must not lie: recompute each code's check digit independently
    lie = [k for k, v in codes.items() if not A.damm_valid(v)]
    rep('C5b every printed bank code passes the check digit, recomputed here', not lie, str(codes))

    ev = MS.run(args.sheets, 9000, samples=None); ev['check_digit_exhaustive'] = ex
    wm, nv = ev['with_methods'], ev['naive_reader']; pk = ev['per_kind_with_methods']
    print('     evaluation: %d sheets, %d rows, seed base 9000, registration failures %d' % (ev['sheets'], ev['rows_scored'], ev['registration_failures']))
    print('     with the methods : %s' % json.dumps(wm, sort_keys=True)); print('     reader without them: %s' % json.dumps(nv, sort_keys=True))
    for k, v in pk.items(): print('       %-22s with methods %-40s naive %s' % (k, json.dumps(v, sort_keys=True), json.dumps(ev['per_kind_naive'].get(k, {}), sort_keys=True)))
    share = ev['recoverable_rows_held_by_a_flag'] / ev['recoverable_rows']
    print('     recoverable rows %d, held for a person %d (%.1f percent) by flag kind %s' % (ev['recoverable_rows'], ev['recoverable_rows_held_by_a_flag'], 100 * share, ev['recoverable_rows_held_by_flag_kind']))
    slip = pk.get('code_slip', {}); swap = pk.get('code_swap', {})
    ok6 = (ev['registration_failures'] == 0 and wm.get('silent_wrong', 0) == 0 and wm.get('missed', 0) == 0 and slip.get('detected', 0) == sum(slip.values()) and swap.get('detected', 0) == sum(swap.values())
           and (nv.get('silent_wrong', 0) + nv.get('missed', 0)) > 0 and share <= 0.25)
    rep('C6 measurement on synthetic filled sheets meets the criteria fixed before the run', ok6,
        'silent_wrong %d, missed %d (naive %d and %d), unflagged empty reads of faint marks %d, held share %.1f percent' % (wm.get('silent_wrong', 0), wm.get('missed', 0), nv.get('silent_wrong', 0), nv.get('missed', 0), wm.get('empty_not_flagged', 0), 100 * share))
    if args.log: json.dump(ev, open(args.log.replace('.txt', '.json'), 'w'), indent=1)

    # C7 the sheet against the printed-paper rules
    shapes_pr = Graph().parse(V('paperrules_shapes')); reg_pr = Graph().parse(V('papertypes')); fxg = Graph().parse(V('paperrules_fixtures'))
    sub = Graph(); keep = 'P01'
    for s, p, o in fxg:
        if str(s).split('#')[-1].split('_')[0] == keep: sub.add((s, p, o))
    for t in reg_pr: sub.add(t)
    pap = [s for s in sub.subjects(RDF.type, PR.Paper)][0]
    def setp(gr, p, v): gr.set((pap, PR[p], v))
    setp(sub, 'answerMode', PR.GridOnCover); setp(sub, 'fontPt', Literal(int(meas['min_font_pt'] + 1e-6), datatype=XSD.integer)); setp(sub, 'fillColourUsed', Literal(meas['coloured_pixels'] > 0))
    setp(sub, 'pageCount', Literal(meas['pages'], datatype=XSD.integer))
    ents = sorted(sub.subjects(RDF.type, PR.BankEntry), key=str); labels = [A.make_code(i + 1, 1) for i in range(len(ents))]
    for e, lab in zip(ents, labels): sub.set((e, PR.label, Literal(lab)))
    def run_pr(gr):
        c, rg, t = pyshacl.validate(gr, shacl_graph=shapes_pr, advanced=True, inference='none', js=False)
        return c, {(str(rg.value(r, SH.resultMessage)).split()[0], str(rg.value(r, SH.resultSeverity)).split('#')[1]) for r in rg.subjects(SH.resultSeverity, None)}
    c7, m7 = run_pr(sub)
    def mut2(fn):
        gg = Graph(); [gg.add(t) for t in sub]; fn(gg); return gg
    n_colour = run_pr(mut2(lambda gg: gg.set((pap, PR.fillColourUsed, Literal(True)))))
    n_label = run_pr(mut2(lambda gg: gg.set((ents[0], PR.label, Literal('A7')))))
    n_font = run_pr(mut2(lambda gg: gg.set((pap, PR.fontPt, Literal(9, datatype=XSD.integer)))))
    kinds = {'choice': ('ChoiceFour', 'ChoiceFourCode'), 'match': ('Matching',), 'order': ('Ordering',), 'bank': ('FillBlank',), 'human': ('NumericAnswer', 'CodeTrace')}
    unsuited = [t for ks in kinds.values() for t in ks if reg_pr.value(PR[t], PR.status) != PR.Suited]
    print('     paper P01 as a grid-on-cover paper with the sheet\'s measured values and coded bank labels %s: conforms=%s %s' % (labels, c7, sorted(m7)))
    rep('C7 the sheet conforms to the printed-paper rules; the bank labels are digits (R14); every unit kind maps to a suited item type; negative controls fail',
        c7 and not m7 and not unsuited and ('R01', 'Violation') in n_colour[1] and ('R14', 'Violation') in n_label[1] and ('R01', 'Violation') in n_font[1],
        'unsuited %s; colour %s; label %s; font %s' % (unsuited, sorted(n_colour[1]), sorted(n_label[1]), sorted(n_font[1])))

    # C8 page cost and capacity
    cap = 0
    for n in range(10, 140, 2):
        L = A.build_layout({'paper_kind': 'Midterm', 'paper_version': 1, 'form_code': '10100', 'units': [{'no': str(k), 'kind': 'choice', 'opts': 'ABCD'} for k in range(1, n + 1)]})
        if L['pages'] == 1: cap = n
        else: break
    r = PM.run(PM.parse_ch('1-6'), 40); st = list(r['pages_methods_stacked_in_order'].values())[-1]
    print('     the demonstration sheet has %d page (%d units: 24 choice, 4 matching, 3 ordering, 4 code blanks, 3 written); one page holds up to %d four-option rows' % (meas['pages'], len(spec['units']), cap))
    print('     sample paper (40 items, stacked page methods): %d pages without a sheet, %d with the sheet; sheets of paper when printed on both sides: %d without, %d with' % (st, st + meas['pages'], -(-st // 2), -(-(st + meas['pages']) // 2)))
    rep('C8 the sheet is one page for the demonstration paper and its capacity is measured', meas['pages'] == 1 and cap >= 40, 'capacity %d' % cap)

    mg = Graph().parse(V('answermethods')); qs = json.load(open(V('answersheet_owner_questions', 'json')))['questions_for_the_owner_via_the_coordinator']
    mist = set(mg.subjects(RDF.type, AM.Mistake)); meth = set(mg.subjects(RDF.type, AM.Method)); covered = {o for m in meth for o in mg.objects(m, AM.addresses)}
    gaps = []
    for m in meth:
        for p in (AM.addresses, AM.basis, AM.reason, AM.appliesIn):
            if mg.value(m, p) is None: gaps.append((str(m).split('#')[1], str(p).split('#')[1]))
        if str(mg.value(m, AM.basis)) in ('FACT', 'SYNTHETIC') and mg.value(m, AM.measuredBy) is None: gaps.append((str(m).split('#')[1], 'measuredBy'))
    rep('C9 every method names its mistake, reason, basis and mode; every mistake has a method; every owner question has an id and text', not gaps and mist <= covered and all(q['id'] and q['ask'] for q in qs),
        '%d mistakes, %d methods, %d questions, gaps %s, uncovered %s' % (len(mist), len(meth), len(qs), gaps, sorted(str(x).split('#')[1] for x in mist - covered)))
finally:
    shutil.rmtree(work, ignore_errors=True)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
