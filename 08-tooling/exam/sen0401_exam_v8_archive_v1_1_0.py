#!/usr/bin/env python3
"""SEN0401 midterm v8.0.1, X3a2: archive the SUPERSEDED files and write ONE release-history record (file, sha256, replaced by, date, status), by script, from the files as they are before the move. Holds no question text.
New file (sen0401_exam_v8_archive_v1_0_0.py stays unchanged). Moves, by `git mv` under flock /tmp/sen0401_git.lock and by path (committed files are moved, never edited):
  (1) the delivered-for-control set papers_midterm_v8_0_0/ (five files) and the v8.0.0 build outputs and logs  -> exam/papers_midterm_archive/
  (2) the superseded item-stage files of exam/v8 and exam/v8/items (same family rule as v1.0.0: a higher version of the same family exists) -> exam/v8/archive/ (name prefix items__ for files from items/)
A file another CURRENT script reads stays (status RETAINED with the reason). Private item/solution/structure files of v8.0.0 stay (read by library v8.0.0, kept for reproduction).
Usage: archive.py EXAM_DIR [--dry-run]"""
import argparse, datetime, hashlib, os, re, subprocess, sys
sys.dont_write_bytecode = True
ap = argparse.ArgumentParser(); ap.add_argument('exam'); ap.add_argument('--dry-run', action='store_true'); x = ap.parse_args()
EX = os.path.abspath(x.exam); V8 = os.path.join(EX, 'v8'); AR = os.path.join(V8, 'archive'); PA = os.path.join(EX, 'papers_midterm_archive')
CME = subprocess.run(['git', '-C', EX, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
RETAINED = {'sen0401_v8_x1b_build_v1_0_1.py': 'imported by sen0401_v8_x1b_build_v1_0_2.py', 'sen0401_v8_x1b_tool_items_v1_0_1.json': 'source of sen0401_v8_x1b_build_v1_0_2.py',
            'sen0401_v8_x1b_tool_paper_v1_0_1.docx': 'source of sen0401_v8_x1b_build_v1_0_2.py', 'v8_2c_coinbase_most_claim_v1_0_1.json': 'read by sen0401_exam_v8_x1a_retag_2c_v1_0_2.py and sen0401_exam_v8_x1a_build_v1_0_1.py'}
UNTRACKED_SKIP = {'sen0401_exam_x2_readability_log_v8_0_1.txt'}      # written by another executor, not committed: left where it is
VER = re.compile(r'^(.*)_v(\d+)_(\d+)_(\d+)(\..+)$')
T0, T1 = 'sen0401_exam_midterm_v8_0_0', 'sen0401_exam_midterm_v8_0_1'
rows = []; moves = []


def fam(name):
    m = VER.match(name)
    if not m: return None
    v = tuple(int(m.group(i)) for i in (2, 3, 4))
    if m.group(1).startswith('sen0401_exam_x2_') and v[0] == 8: v = (0,) + v[1:]
    return (m.group(1), m.group(5), v)


# (1) the v8.0.0 set and its build outputs and logs
for f in sorted(os.listdir(os.path.join(EX, 'papers_midterm_v8_0_0'))):
    a = os.path.join(EX, 'papers_midterm_v8_0_0', f); new = f.replace('v8_0_0', 'v8_0_1') if f != 'MANIFEST_SHA256' else 'MANIFEST_SHA256'
    rows.append(('papers_midterm_v8_0_0/' + f, sha(a), 'papers_midterm_v8_0_1/' + new, 'moved')); moves.append((a, os.path.join(PA, 'papers_midterm_v8_0_0', f)))
BUILD = os.path.join(V8, 'assembly', 'build'); LOGS = os.path.join(V8, 'assembly', 'logs')
for d, sub in ((BUILD, 'build'), (LOGS, 'logs')):
    for f in sorted(os.listdir(d)):
        if T0 in f or f.endswith('_v8_0_0.json') or f.endswith('_v8_0_0.txt') or f in ('sen0401_exam_v8_assemble_items_log_v1_0_0.txt', 'sen0401_exam_v8_assembly_check_log_v1_0_0.txt'):
            a = os.path.join(d, f); new = f.replace('v8_0_0', 'v8_0_1').replace('_v1_0_0.txt', '_v1_1_0.txt' if 'assembly_check' in f else '_v1_0_1.txt')
            rows.append(('v8/assembly/%s/%s' % (sub, f), sha(a), 'v8/assembly/%s/%s' % (sub, new), 'moved')); moves.append((a, os.path.join(PA, 'papers_midterm_v8_0_0_%s' % sub, f)))
mp = os.path.join(V8, 'assembly', 'sen0401_exam_v8_assembly_map_v1_0_0.json')
rows.append(('v8/assembly/sen0401_exam_v8_assembly_map_v1_0_0.json', sha(mp), 'v8/assembly/sen0401_exam_v8_assembly_map_v1_0_1.json', 'moved')); moves.append((mp, os.path.join(PA, 'papers_midterm_v8_0_0_build', os.path.basename(mp))))
for f, why in (('private/sen0401_exam_items_midterm_v8_0_0.json', 'sen0401_exam_items_midterm_v8_0_1.json'), ('private/sen0401_exam_key_solutions_v8_0_0.json', 'sen0401_exam_key_solutions_v8_0_1.json'), ('private/sen0401_exam_structure_v1_6_0.json', 'sen0401_exam_structure_v1_6_1.json')):
    rows.append((f, sha(os.path.join(EX, f)), 'private/' + why, 'RETAINED: read by library v8.0.0 (kept for reproduction of the first assembly)'))
# (2) item-stage families
for d in (V8, os.path.join(V8, 'items')):
    files = sorted(f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))); fams = {}
    for f in files:
        k = fam(f)
        if k: fams.setdefault((k[0], k[1]), []).append((k[2], f))
    for f in files:
        rel = os.path.relpath(os.path.join(d, f), V8)
        if f in UNTRACKED_SKIP: continue
        k = fam(f)
        if not k: continue
        later = sorted(v_g for v_g in fams[(k[0], k[1])] if v_g[0] > k[2])
        if not later: continue
        newer = later[-1][1]
        if f in RETAINED: rows.append((rel, sha(os.path.join(d, f)), newer, 'RETAINED: ' + RETAINED[f])); continue
        rows.append((rel, sha(os.path.join(d, f)), newer, 'moved')); moves.append((os.path.join(d, f), os.path.join(AR, rel.replace('/', '__') if d != V8 else rel)))
today = datetime.date.today().isoformat()
if x.dry_run:
    for r in rows: print('\t'.join(r))
    sys.exit(0)
os.makedirs(PA, exist_ok=True); rec = os.path.join(PA, 'RELEASE_HISTORY_v8_0_1.tsv')
if os.path.exists(rec): raise SystemExit('REFUSED: record exists')
with open(rec, 'w') as fh:
    fh.write('file\tsha256\treplaced_by\tdate\tstatus\n')
    for r in rows: fh.write('%s\t%s\t%s\t%s\t%s\n' % (r[0], r[1], r[2], today, r[3]))
for a, b in moves:
    if os.path.exists(b): raise SystemExit('REFUSED: target exists ' + b)
    os.makedirs(os.path.dirname(b), exist_ok=True)
    subprocess.run(['flock', '/tmp/sen0401_git.lock', 'git', '-C', CME, 'mv', os.path.relpath(a, CME), os.path.relpath(b, CME)], check=True)
print('moved %d files, retained %d, record %s' % (len(moves), len(rows) - len(moves), rec))
