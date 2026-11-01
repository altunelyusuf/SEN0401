#!/usr/bin/env python3
"""sen0401_deck_checks_control_check v1_0_0 - the control's own counts of the four successor checks on the old decks of chapters 1 to 6, against the lineage agent's independent counts (prompts, lambda LINES, label shapes). Usage: run"""
import subprocess, sys, re, os
H = os.path.dirname(os.path.abspath(__file__)); M3 = os.path.join(H, "..", "03-materials")
DECKS = {1: "ch01/SEN0401_Ch01_Introduction_3e_v3_2_0", 2: "ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0", 3: "ch03/SEN0401_Ch03_BitcoinCore_3e_v3_0_0", 4: "ch04/SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0", 5: "ch05/SEN0401_Ch05_WalletRecovery_3e_v3_4_0", 6: "ch06/SEN0401_Ch06_Transactions_3e_v2_3_0"}
EXP = {1: (62, 0, 27), 2: (50, 3, 0), 3: (64, 1, 0), 4: (67, 3, 0), 5: (163, 2, 0), 6: (0, 0, 0)}  # lambda = code LINES (Ch4 owner count 4 was occurrences: slide 31 has two on one line)
bad = 0
for c, d in DECKS.items():
    f = os.path.join(M3, d + ".pptx"); got = []
    for k, key in (("prompt", "prompt_rows"), ("lambda", "code_lines_with_lambda"), ("label_words", "label_shapes")):
        o = subprocess.run([sys.executable, os.path.join(H, "sen0401_deck_%s_check_v1_0_0.py" % k), f], capture_output=True, text=True).stdout
        got.append(int(re.search(key + r"=(\d+)", o).group(1)))
    ok = tuple(got) == EXP[c]; bad += not ok
    print("%s  Ch0%d prompts/lambda lines/label shapes %s expected %s" % ("PASS" if ok else "FAIL", c, tuple(got), EXP[c]))
print("RESULT", "FAIL" if bad else "PASS"); sys.exit(1 if bad else 0)
