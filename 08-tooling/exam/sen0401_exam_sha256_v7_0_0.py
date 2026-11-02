#!/usr/bin/env python3
"""SEN0401 exam v7 SHA256 writer, version 7.0.0 (new file). Holds no question and no answer.
Writes SHA256.txt for the delivered set of ONE version:  TAG_paper.docx, TAG_paper.pdf, TAG_key.docx, TAG_key.pdf, TAG_sheet.pdf   (TAG default sen0401_exam_midterm_v7_0_0).
The file is in the format of `sha256sum` (hash, two spaces, name; names sorted), so that `sha256sum -c SHA256.txt` verifies it. A comment line (starting with #) states the version, and for a synthetic set the disclosure.
Commands:
  write  DIR [--tag TAG] [--synthetic]    refuses when a file of the set is missing, when SHA256.txt exists, or when the folder holds a file of the set with another version in its name
  verify DIR [--tag TAG]                  recomputes every hash and compares; prints PASS / FAIL per file; exit 1 on any FAIL
SHA256.txt does not list itself (a file cannot hold its own hash)."""
import argparse, hashlib, os, re, sys
sys.dont_write_bytecode = True
VERSION = '7.0.0'
DEFAULT_TAG = 'sen0401_exam_midterm_v7_0_0'
SET = ('_paper.docx', '_paper.pdf', '_key.docx', '_key.pdf', '_sheet.pdf')
SYNTH = '# SYNTHETIC INPUT: invented placeholder wording, not a real exam, never delivered.'


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()


def names(tag): return [tag + e for e in SET]


def write(d, tag, synthetic):
    out = os.path.join(d, 'SHA256.txt')
    if os.path.exists(out): raise SystemExit('REFUSED: %s exists (a committed or delivered file is never overwritten)' % out)
    miss = [n for n in names(tag) if not os.path.isfile(os.path.join(d, n))]
    if miss: raise SystemExit('REFUSED: missing files of the set: %s' % ', '.join(miss))
    other = sorted(f for f in os.listdir(d) if re.match(r'sen0401_exam_midterm_v\d+_\d+_\d+', f) and not f.startswith(tag) and f.endswith(('.docx', '.pdf')))
    if other: raise SystemExit('REFUSED: the folder holds files of another version or name: %s' % ', '.join(other))
    lines = ['# SEN0401 midterm exam set, SHA256 of the files, tooling v%s; verify with: sha256sum -c SHA256.txt' % VERSION]
    if synthetic: lines.append(SYNTH)
    lines += ['%s  %s' % (sha(os.path.join(d, n)), n) for n in sorted(names(tag))]
    open(out, 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines)); return out


def verify(d, tag):
    p = os.path.join(d, 'SHA256.txt')
    if not os.path.isfile(p): print('FAIL  SHA256.txt is missing'); return 1
    listed = {}
    for ln in open(p).read().splitlines():
        if not ln.strip() or ln.startswith('#'): continue
        m = re.fullmatch(r'([0-9a-f]{64})  (\S+)', ln)
        if not m: print('FAIL  malformed line: %r' % ln); return 1
        listed[m.group(2)] = m.group(1)
    bad = 0
    if sorted(listed) != sorted(names(tag)): print('FAIL  the list names %s, the set is %s' % (sorted(listed), sorted(names(tag)))); bad += 1
    for n, h in sorted(listed.items()):
        f = os.path.join(d, n); ok = os.path.isfile(f) and sha(f) == h
        print('%s  %s %s' % ('PASS' if ok else 'FAIL', n, h)); bad += 0 if ok else 1
    return 1 if bad else 0


def main():
    a = argparse.ArgumentParser(description=__doc__.split('\n')[0]); a.add_argument('cmd', choices=['write', 'verify']); a.add_argument('dir'); a.add_argument('--tag', default=DEFAULT_TAG); a.add_argument('--synthetic', action='store_true')
    x = a.parse_args()
    if x.cmd == 'write': write(x.dir, x.tag, x.synthetic)
    else: sys.exit(verify(x.dir, x.tag))


if __name__ == '__main__': main()
