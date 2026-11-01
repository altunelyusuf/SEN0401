#!/usr/bin/env python3
"""sen0401_deck_honesty_control_check v1_0_0 - the control's own check of the honesty successor (commit a3f9719): (1) on old decks WITH prompts honesty v1_1_0 and v1_0_0 print the same lines and exit code; (2) on the prompt-free Chapter 1 v3_3_0 and Chapter 5 v3_7_0 decks v1_1_0 exits 0; (3) the control's own stale caption (one caption changed to another Python version in a copy of Chapter 1 v3_3_0) is REFUSED by v1_1_0; (4) the executor's fixtures v1_4_0 for chapter 1 end with every stale fixture refused and the control accepted. Usage: run"""
import os, re, subprocess, sys, shutil, tempfile
from pptx import Presentation
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); M3 = os.path.join(R, "03-materials")
res = []
def chk(ok, m): res.append(bool(ok)); print("PASS " if ok else "FAIL ", m)
def hon(ver, nn, deck):
    r = subprocess.run([sys.executable, os.path.join(H, "sen0401_deck_honesty_check_v%s.py" % ver), nn], capture_output=True, text=True, env=dict(os.environ, SEN0401_ROOT=R, SEN0401_DECK=deck)); return r.returncode, r.stdout.strip()
for nn, d in (("02", "ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0"), ("03", "ch03/SEN0401_Ch03_BitcoinCore_3e_v3_0_0"), ("04", "ch04/SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0")):
    nz = lambda x: (x[0], re.sub(r"check \d+\.\d+\.\d+", "check V", x[1])); a = nz(hon("1_0_0", nn, os.path.join(M3, d + ".pptx"))); b = nz(hon("1_1_0", nn, os.path.join(M3, d + ".pptx"))); chk(a == b, "Ch%s deck with prompts: v1_0_0 and v1_1_0 give the same exit code (%d, %d) and lines" % (nn, a[0], b[0]))
c1 = os.path.join(M3, "ch01/SEN0401_Ch01_Introduction_3e_v3_3_0.pptx"); c5 = os.path.join(M3, "ch05/SEN0401_Ch05_WalletRecovery_3e_v3_7_0.pptx")
chk(hon("1_1_0", "01", c1)[0] == 0, "Ch01 v3_3_0 (prompt-free) accepted by v1_1_0"); chk(hon("1_1_0", "05", c5)[0] == 0, "Ch05 v3_7_0 (prompt-free) accepted by v1_1_0")
p = Presentation(c1); n = 0
for s in p.slides:
    if not any(x.name.startswith("result") for x in s.shapes): continue
    for sh in s.shapes:
        if sh.has_text_frame and re.search(r"python 3\.\d+\.\d+", sh.text_frame.text, re.I) and n == 0:
            for para in sh.text_frame.paragraphs:
                for r in para.runs:
                    if re.search(r"python 3\.\d+\.\d+", r.text, re.I): r.text = re.sub(r"python 3\.\d+\.\d+", "Python 3.9.1", r.text, flags=re.I); n += 1
tmp = tempfile.mkdtemp(); t = os.path.join(tmp, "stale.pptx"); p.save(t)
chk(n > 0, "the control changed %d caption to a different Python version" % n); rc, out = hon("1_1_0", "01", t); chk(rc != 0, "the stale caption copy is refused by v1_1_0 (exit %d)" % rc); shutil.rmtree(tmp)
r = subprocess.run([sys.executable, os.path.join(H, "sen0401_deck_fixtures_v1_4_0.py"), "01", "--run"], capture_output=True, text=True); last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
chk(r.returncode == 0 and "refused" in last, "executor's fixtures v1_4_0 chapter 1: " + last[:160])
print("RESULT", "PASS" if all(res) else "FAIL"); sys.exit(0 if all(res) else 1)
