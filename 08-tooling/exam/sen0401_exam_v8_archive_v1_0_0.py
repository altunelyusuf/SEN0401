#!/usr/bin/env python3
"""SEN0401 midterm v8.0.0, X3a: move the SUPERSEDED item-stage files (v8_0_0 and v1_0_0 files, old logs) of exam/v8 into exam/v8/archive/ and write ONE release-history record
(file, sha256, replaced by, date). Holds no question text. The record is written by this script, from the files as they are before the move.
Rule: a file is superseded when a file of the same family (name without its version) with a higher version exists; a file another CURRENT script reads or imports stays (listed as RETAINED in the record).
Usage: archive.py EXAM_DIR [--dry-run]   (git mv under flock /tmp/sen0401_git.lock, by path)"""
import argparse, datetime, hashlib, os, re, subprocess, sys
sys.dont_write_bytecode = True
ap = argparse.ArgumentParser(); ap.add_argument('exam'); ap.add_argument('--dry-run', action='store_true'); x = ap.parse_args()
EX = os.path.abspath(x.exam); V8 = os.path.join(EX, 'v8'); AR = os.path.join(V8, 'archive'); CME = subprocess.run(['git', '-C', EX, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
# explicit family overrides (the file name changed between versions, or the version label is not ordered by number)
REPLACED = {
    'v8_2a_target_after_adjustment.json': 'v8_2a_target_after_adjustment_v1_0_1.json',
    'v8_2b_release_tag_text_place.json': 'v8_2b_release_tag_text_place_v1_0_1.json',
    'v8_2c_coinbase_claim_too_large.json': 'v8_2c_coinbase_most_claim_v1_0_1.json',
    'v8_2d_hash_search_seconds.json': 'v8_2d_hash_search_seconds_v1_0_1.json',
}
RETAINED = {'sen0401_v8_x1b_build_v1_0_1.py': 'imported by sen0401_v8_x1b_build_v1_0_2.py', 'sen0401_v8_x1b_tool_items_v1_0_1.json': 'source of sen0401_v8_x1b_build_v1_0_2.py',
            'sen0401_v8_x1b_tool_paper_v1_0_1.docx': 'source of sen0401_v8_x1b_build_v1_0_2.py'}
UNTRACKED_SKIP = {'sen0401_exam_x2_readability_log_v8_0_1.txt'}      # not committed, written by another executor: left where it is
VER = re.compile(r'^(.*)_v(\d+)_(\d+)_(\d+)(\..+)$')


def fam(name):
    m = VER.match(name)
    if not m: return None
    v = tuple(int(m.group(i)) for i in (2, 3, 4))
    if m.group(1).startswith('sen0401_exam_x2_') and v[0] == 8: v = (0,) + v[1:]      # X2 labelled its first releases v8_0_x; they come BEFORE its v1_0_1
    return (m.group(1), m.group(5), v)


rows = []; moves = []
for d in (V8, os.path.join(V8, 'items')):
    files = sorted(f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f)))
    fams = {}
    for f in files:
        k = fam(f)
        if k: fams.setdefault((k[0], k[1]), []).append((k[2], f))
    for f in files:
        rel = os.path.relpath(os.path.join(d, f), V8)
        if f in UNTRACKED_SKIP: continue
        newer = None
        if f in REPLACED: newer = REPLACED[f]
        else:
            k = fam(f)
            if k:
                later = sorted(v_g for v_g in fams[(k[0], k[1])] if v_g[0] > k[2])
                newer = later[-1][1] if later else None
        if newer is None: continue
        if f in RETAINED: rows.append((rel, sha(os.path.join(d, f)), newer, 'RETAINED: ' + RETAINED[f])); continue
        rows.append((rel, sha(os.path.join(d, f)), newer, 'moved')); moves.append((os.path.join(d, f), os.path.join(AR, rel.replace('/', '__') if d != V8 else rel)))
today = datetime.date.today().isoformat()
if x.dry_run:
    for r in rows: print('\t'.join(r))
    sys.exit(0)
os.makedirs(AR, exist_ok=True)
rec = os.path.join(AR, 'RELEASE_HISTORY_v8_0_0.tsv')
if os.path.exists(rec): raise SystemExit('REFUSED: record exists')
with open(rec, 'w') as fh:
    fh.write('file\tsha256\treplaced_by\tdate\tstatus\n')
    for r in rows: fh.write('%s\t%s\t%s\t%s\t%s\n' % (r[0], r[1], r[2], today, r[3]))
for a, b in moves:
    if os.path.exists(b): raise SystemExit('REFUSED: target exists ' + b)
    subprocess.run(['flock', '/tmp/sen0401_git.lock', 'git', '-C', CME, 'mv', os.path.relpath(a, CME), os.path.relpath(b, CME)], check=True)
print('moved %d files, retained %d, record %s' % (len(moves), len(rows) - len(moves), rec))
