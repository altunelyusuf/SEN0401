#!/usr/bin/env python3
"""SEN0401 items group q34 v1.8.0, public runner. Holds no question and no answer: it runs the private builder check in the private CME repository
(exams/SEN0401/08-tooling/exam/private/sen0401_exam_items_part_q34_check_v1_8_0.py, CME commit 757e1d7) and prints its result lines. Usage: runner.py [CME_DIR]"""
import os, subprocess, sys
sys.dont_write_bytecode = True
cme = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/CME'
p = os.path.join(cme, 'exams/SEN0401/08-tooling/exam/private/sen0401_exam_items_part_q34_check_v1_8_0.py')
here = os.path.dirname(os.path.abspath(__file__))
r = subprocess.run(['nice', '-n', '10', sys.executable, p, '--readability', os.path.join(here, 'sen0401_exam_readability_check_v1_1_0.py')], capture_output=True, text=True)
lines = r.stdout.splitlines()
print('\n'.join(l for l in lines if l.startswith(('RESULT', '  R', 'R5')) or l.startswith('[FAIL]')))
sys.exit(r.returncode)
