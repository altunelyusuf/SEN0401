#!/usr/bin/env python3
"""SEN0401 midterm v8.0.0, X3a: copy the four delivered files of the set from the build folder into the delivery folder and WRITE MANIFEST_SHA256 by script (never by hand).
Delivery folder = exactly: TAG_paper.docx, TAG_paper.pdf, TAG_key.docx, TAG_sheet.pdf, MANIFEST_SHA256 (format of `sha256sum`: hash, two spaces, name; verify with `sha256sum -c MANIFEST_SHA256`).
Holds no question text. Refuses when the folder exists or a source file is missing.  Usage: manifest.py BUILD_DIR DELIVERY_DIR --tag TAG"""
import argparse, hashlib, os, shutil, sys
sys.dont_write_bytecode = True
ap = argparse.ArgumentParser(); ap.add_argument('build'); ap.add_argument('out'); ap.add_argument('--tag', required=True); x = ap.parse_args()
names = [x.tag + e for e in ('_paper.docx', '_paper.pdf', '_key.docx', '_sheet.pdf')]
if os.path.exists(x.out): raise SystemExit('REFUSED: exists ' + x.out)
miss = [n for n in names if not os.path.isfile(os.path.join(x.build, n))]
if miss: raise SystemExit('REFUSED: missing %s' % miss)
os.makedirs(x.out)
for n in names: shutil.copyfile(os.path.join(x.build, n), os.path.join(x.out, n))
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
with open(os.path.join(x.out, 'MANIFEST_SHA256'), 'w') as fh:
    for n in sorted(names): fh.write('%s  %s\n' % (sha(os.path.join(x.out, n)), n))
print(open(os.path.join(x.out, 'MANIFEST_SHA256')).read())
