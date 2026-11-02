#!/usr/bin/env python3
"""SEN0401 exam v7 ONE-COMMAND render, version 7.0.0 (new file). The script holds no question and no answer.
  render_v7.py                 REAL run: takes the real items (v1.6.x) and structure (v1.3.x, default the highest present, v1.3.0 or later) from the CME private folder (when they exist), builds the paper (.docx, .pdf), the key (.docx, .pdf), the sheet (.pdf, sheet module v7.0.0,
                               units_from_list, a real form code) and SHA256.txt in CME exams/SEN0401/08-tooling/exam/papers_midterm_v7/, then runs the readability check v1.1.0, the scoring module v2.0.0 and the tooling check, and prints the page counts.
                               If a real file is missing it prints NOT_FOUND with the path and exits 3: it never falls back to another file and never renders a partial set.
  render_v7.py --synthetic     SYNTHETIC run: writes the invented items/structure (generator v1.0.0) and renders the same pipeline into CME .../papers_v7_synthetic/ with names that carry SYNTHETIC; disclosed in every output; never delivered.
Heavy steps run under the page-test lock (/tmp/page_test.lock, taken here) at nice 10. Existing files are never overwritten (the builder and the SHA256 writer refuse).
Options: --seed N (default 5701) --out DIR --keep-going (run the later checks even when one fails)."""
import argparse, fcntl, json, os, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
CME_EXAM = '/home/claude/CME/exams/SEN0401/08-tooling/exam'
PRIV = os.path.join(CME_EXAM, 'private')


def real_pair(structure_version=None):
    """The real structure (v1.3.x) and the items file it names, from the CME private folder. Default: the highest v1.3.N present (v1.3.0 is the brief's; a later patch such as v1.3.1 supersedes it and is printed). Returns (structure path, items path) or (None, None)."""
    import glob, re as _re
    cands = sorted(glob.glob(os.path.join(PRIV, 'sen0401_exam_structure_v1_5_*.json')), key=lambda f: int(_re.search(r'v1_5_(\d+)', f).group(1)))
    if structure_version: cands = [c for c in cands if c.endswith('_v%s.json' % structure_version.replace('.', '_'))]
    if not cands: return None, None
    st = cands[-1]; it = os.path.join(os.path.dirname(st), os.path.basename(json.load(open(st))['items_file']))
    return st, it
PY = sys.executable
ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); ap.add_argument('--synthetic', action='store_true'); ap.add_argument('--seed', type=int, default=5701); ap.add_argument('--out'); ap.add_argument('--keep-going', action='store_true'); ap.add_argument('--structure-version', help='for example 1.3.0 (default: the highest 1.3.N in CME private)')
x = ap.parse_args()


def run(label, cmd, log=None):
    print('\n=== %s' % label, flush=True); t0 = time.time()
    r = subprocess.run(['nice', '-n', '10'] + cmd, capture_output=True, text=True, cwd=HERE)
    out = r.stdout + r.stderr
    print(out.rstrip(), flush=True)
    if log: open(log, 'w').write('$ ' + ' '.join(cmd) + '\n' + out + '\nexit %d\n' % r.returncode)
    print('--- exit %d (%.0f s)' % (r.returncode, time.time() - t0), flush=True)
    return r.returncode


if x.synthetic:
    out = x.out or os.path.join(CME_EXAM, 'papers_v7_synthetic'); tag = 'sen0401_exam_midterm_v7_0_0_SYNTHETIC'
    inp = os.path.join(out, 'input'); items = os.path.join(inp, 'sen0401_exam_items_SYNTHETIC_v7_0_0.json'); struct = os.path.join(inp, 'sen0401_exam_structure_SYNTHETIC_v7_0_0.json')
    print('SYNTHETIC INPUT: invented placeholder wording, not a real exam, never delivered.')
    if not os.path.isfile(struct):
        if run('synthetic items and structure', [PY, os.path.join(HERE, 'sen0401_exam_synthetic_v7_build_v1_0_0.py'), inp]): sys.exit(2)
else:
    REAL_STRUCT, REAL_ITEMS = real_pair(x.structure_version)
    if not REAL_STRUCT or not os.path.isfile(REAL_ITEMS):
        print('NOT_FOUND  the real structure v1.3.x%s and its items file in %s' % (' (version %s)' % x.structure_version if x.structure_version else '', PRIV))
        print('The real items and structure are not in the CME private folder yet; nothing was rendered.'); sys.exit(3)
    st = json.load(open(REAL_STRUCT))
    if not str(st.get('version')).startswith('1.5.') or st.get('synthetic'): print('REFUSED: the structure file is not a real v1.3.x (version %r, synthetic %r)' % (st.get('version'), st.get('synthetic'))); sys.exit(2)
    print('REAL INPUT: structure v%s (%s), items file %s' % (st['version'], os.path.basename(REAL_STRUCT), os.path.basename(REAL_ITEMS)))
    out = x.out or os.path.join(CME_EXAM, 'papers_midterm_v7_2'); tag = 'sen0401_exam_midterm_v7_2_0'; items, struct = REAL_ITEMS, REAL_STRUCT
os.makedirs(out, exist_ok=True)
lockf = open('/tmp/page_test.lock', 'a'); print('taking /tmp/page_test.lock (queues behind other browser or LibreOffice runs)', flush=True); fcntl.flock(lockf, fcntl.LOCK_EX)
fails = []
def step(label, cmd, log=None):
    rc = run(label, cmd, log)
    if rc: fails.append((label, rc))
    return rc
step('BUILD paper, key, sheet', [PY, os.path.join(HERE, 'sen0401_exam_papers_build_v7_2_1.py'), out, '--structure', struct, '--tag', tag, '--seed', str(x.seed)], os.path.join(out, 'sen0401_exam_papers_build_log_v7_2_1%s.txt' % ('_SYNTHETIC' if x.synthetic else '')))
if fails and not x.keep_going: print('\nSTOP: the build failed; nothing else was run'); sys.exit(2)
step('SHA256 write', [PY, os.path.join(HERE, 'sen0401_exam_sha256_v7_0_0.py'), 'write', out, '--tag', tag] + (['--synthetic'] if x.synthetic else []))
step('SHA256 verify', [PY, os.path.join(HERE, 'sen0401_exam_sha256_v7_0_0.py'), 'verify', out, '--tag', tag])
step('READABILITY CHECK v1.1.0', [PY, os.path.join(HERE, 'sen0401_exam_readability_check_v1_1_0.py'), 'check', '--items', items, '--paper', os.path.join(out, tag + '_paper.docx'), '--json', os.path.join(out, 'sen0401_exam_readability_v1_1_0_result%s.json' % ('_SYNTHETIC' if x.synthetic else ''))],
     os.path.join(out, 'sen0401_exam_readability_log_v7_2_1%s.txt' % ('_SYNTHETIC' if x.synthetic else '')))
step('SCORING MODULE v2.0.0 on the key of this set (its own check on its own shape file stays separate)', [PY, '-c', 'import sys,json;sys.path.insert(0,%r);import sen0401_exam_scoring_rows_v1_0_0 as S;k=json.load(open(%r));p=S.score(S.perfect_marks(k),k);b=S.expected_blind(k);print("perfect sheet:",p["total"],"of",p["max_total"],"; exact blind total:",b["total"],"=",float(b["total"]),"; closed",b["closed"],"; number and trace",b["number_and_trace"])' % (HERE, os.path.join(out, tag + '_key.json'))])
step('TOOLING CHECK v1.0.0', [PY, os.path.join(HERE, 'sen0401_exam_papertool_v7_check_v1_0_1.py'), out, '--tag', tag] + (['--leak-source', os.path.join(HERE, 'private', 'sen0401_exam_items_midterm_v1_6_0.json')] if x.synthetic and os.path.isfile(os.path.join(HERE, 'private', 'sen0401_exam_items_midterm_v1_6_0.json')) else []),
     os.path.join(out, 'sen0401_exam_papertool_v7_check_log_v1_0_1_on_v7_2_0%s.txt' % ('_SYNTHETIC' if x.synthetic else '')))
m = json.load(open(os.path.join(out, tag + '_measure.json')))
print('\nPAGE COUNTS (%s, LibreOffice export): paper %d (cover 1 + question pages %d) + sheet %d = %d in all; key %d; limit 7 (owner decision 2026-11-02): %s' % ('SYNTHETIC' if x.synthetic else 'REAL', m['paper_pages'], m['question_pages'], m['sheet_pages'], m['pages_total'], m['key_pages'], 'WITHIN 7' if m['pages_total'] <= 7 else 'OVER THE LIMIT'))
print('STEPS THAT FAILED:', fails if fails else 'none'); sys.exit(1 if fails else 0)
