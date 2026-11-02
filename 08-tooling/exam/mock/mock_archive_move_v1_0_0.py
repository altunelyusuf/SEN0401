#!/usr/bin/env python3
"""Archive move v1.0.0 (X3b): retires every superseded file of the SEN0401 mock tree under the archive rule: one current version per identity, the rest moved (never deleted) to archive/
with a release-history record. Identity = file name with all version tokens (_vN_N_N) removed; newest = highest version tuple (a versioned file beats an unversioned one).
Private tree (CME): exam/mock/ (root files), exam/mock/parts/, exam/mock/exclusion/, exam/mock/screens/ -> exam/mock/archive/{,parts/,exclusion/,screens/} + ARCHIVE_RECORD.tsv
  (file, sha256, superseded_by, reason, date, set_version_archived_in); the unversioned master page (sent to the owner) and the screenshots are mapped to the files of the delivered set.
Public tree: 08-tooling/exam/mock/ (and the mock script families in 08-tooling/exam/) -> 08-tooling/exam/mock/archive/ + ARCHIVE_REGISTER.tsv (file name only: file, superseded_by, date, set_version_archived_in).
Usage: mock_archive_move_v1_0_0.py --dry-run | --do        Prints counts and file names only."""
import os, re, sys, hashlib, shutil, datetime
VT = re.compile(r"_v(\d+)_(\d+)_(\d+)")
PRIV = "/home/claude/CME/exams/SEN0401/08-tooling/exam/mock"
PUB = "/home/claude/sen0401/08-tooling/exam/mock"; PUBX = "/home/claude/sen0401/08-tooling/exam"
SETV = "v1_0_0"; DATE = "2026-11-03"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def ident(n): return VT.sub("", n), tuple(tuple(int(x) for x in m) for m in VT.findall(n))
def plan(folder, accept=lambda n: True):
    groups = {}
    for n in sorted(os.listdir(folder)):
        p = os.path.join(folder, n)
        if not os.path.isfile(p) or n in ("ARCHIVE_RECORD.tsv", "ARCHIVE_REGISTER.tsv") or not accept(n): continue
        i, v = ident(n); groups.setdefault(i, []).append((v, n))
    out = []   # (old name, newest name)
    for i, lst in groups.items():
        if len(lst) < 2: continue
        lst.sort(key=lambda t: (len(t[0]) > 0, t[0]))
        newest = lst[-1][1]
        out += [(n, newest) for v, n in lst[:-1]]
    return out
do = "--do" in sys.argv
rows = []; moves = []   # moves: (src, dst)
# ---- private tree
A = PRIV + "/archive"
fixed_root = {"mock_ch_all_master.html": ("sen0401_mock_exam_master_v1_0_0.html", "unversioned master page of the first release; it was SENT TO THE OWNER (sent to the owner before this release); superseded by the master of set v1_0_0"),
              "SHA256.txt": ("MANIFEST_SHA256", "hash list of the first release; replaced by the manifest of the set folder (written by script)")}
for k in range(1, 9):
    fixed_root["mock_ch_all_mock%d.html" % k] = ("sen0401_mock_exam_m%d_v1_0_0.html" % k, "unversioned mock page of the first release; superseded by the page of set v1_0_0")
for k in (4, 5):
    fixed_root["mock_ch_all_mock%d_v1_0_1.html" % k] = ("sen0401_mock_exam_m%d_v1_0_0.html" % k, "re-issued page of mock %d (bank v1.0.1); superseded by the page of set v1_0_0" % k)
fixed_root["mock_bank_all_v1_0_0.json"] = ("sen0401_mock_bank_all_v1_1_0.json", "whole bank of the first release; superseded by the rebuilt bank v1.1.0 of set v1_0_0")
fixed_root["mock_bank_all_v1_0_1.json"] = ("sen0401_mock_bank_all_v1_1_0.json", "whole bank after the X4 reword; superseded by the rebuilt bank v1.1.0 of set v1_0_0")
for n, (by, why) in sorted(fixed_root.items()):
    assert os.path.isfile(PRIV + "/" + n), n
    moves.append((PRIV + "/" + n, A + "/" + n, by, why))
shot = {"checked_1280.png": "checked_1280", "checked_390.png": "checked_390", "print_1280.png": "print_1280", "print_390.png": "print_390", "student_1280.png": "student_1280", "student_390.png": "student_390"}
for n, t in sorted(shot.items()):
    assert os.path.isfile(PRIV + "/screens/" + n), n
    moves.append((PRIV + "/screens/" + n, A + "/screens/" + n, "sen0401_mock_exam_set_v1_0_0_%s.png" % t, "unversioned screenshot of the first release; replaced by the screenshot named with the set version"))
for sub in ("parts", "exclusion"):
    for old, new in plan(PRIV + "/" + sub):
        moves.append((PRIV + "/%s/%s" % (sub, old), A + "/%s/%s" % (sub, old), new, "superseded version of its identity; one current file per identity"))
# ---- public tree
PA = PUB + "/archive"; pubmoves = []
for old, new in plan(PUB):
    pubmoves.append((PUB + "/" + old, PA + "/" + old, new))
for old, new in plan(PUBX, accept=lambda n: re.match(r"^sen0401_mock_", n) is not None):
    pubmoves.append((PUBX + "/" + old, PA + "/" + old, new))
print("private moves: %d (root %d, screens %d, parts %d, exclusion %d); public moves: %d" % (len(moves), len(fixed_root), len(shot),
      sum(1 for m in moves if "/parts/" in m[0]), sum(1 for m in moves if "/exclusion/" in m[0]), len(pubmoves)))
for m in moves: assert not os.path.exists(m[1]), "archive name taken: " + m[1]
for m in pubmoves: assert not os.path.exists(m[1]), "archive name taken: " + m[1]
names = {n for d in (PRIV, PRIV + "/parts", PRIV + "/exclusion", PRIV + "/set_v1_0_0") for n in os.listdir(d)}
for m in moves: assert m[2] in names or (not do and m[2] == "MANIFEST_SHA256"), "superseded_by missing: " + m[2]
pnames = set(os.listdir(PUB)) | set(os.listdir(PUBX))
for m in pubmoves: assert m[2] in pnames and m[2] != os.path.basename(m[0]), "superseded_by missing: " + m[2]
if not do:
    for m in moves: print("P", os.path.relpath(m[0], PRIV), "->", m[2])
    for m in pubmoves: print("U", os.path.relpath(m[0], "/home/claude/sen0401"), "->", m[2])
    sys.exit(0)
os.makedirs(A, exist_ok=True)
lines = ["\t".join(["file", "sha256", "superseded_by", "reason", "date", "set_version_archived_in"])]
for src, dst, by, why in moves:
    h = sha(src); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.move(src, dst)
    lines.append("\t".join([os.path.relpath(dst, A), h, by, why, DATE, SETV]))
open(A + "/ARCHIVE_RECORD.tsv", "w", encoding="utf-8").write("\n".join(lines) + "\n")
if os.path.isdir(PRIV + "/screens") and not os.listdir(PRIV + "/screens"): os.rmdir(PRIV + "/screens")
os.makedirs(PA, exist_ok=True)
pl = ["\t".join(["file", "superseded_by", "date", "set_version_archived_in"])]
for src, dst, by in pubmoves:
    shutil.move(src, dst); pl.append("\t".join([os.path.basename(dst), by, DATE, SETV]))
open(PA + "/ARCHIVE_REGISTER.tsv", "w", encoding="utf-8").write("\n".join(pl) + "\n")
print("moved; records written:", A + "/ARCHIVE_RECORD.tsv", PA + "/ARCHIVE_REGISTER.tsv")
