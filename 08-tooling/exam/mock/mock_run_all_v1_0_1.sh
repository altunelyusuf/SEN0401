#!/bin/bash
# X3b release flow for the mock set v1_0_0 (bank v1.1.0). Every step logs next to this script; page tests run under flock /tmp/page_test.lock; all at nice 10.
# The executor ran these steps one by one with exactly these commands (family prune make, checks and controls were run before step 1).
H=/home/claude/sen0401/08-tooling/exam/mock; M=/home/claude/CME/exams/SEN0401/08-tooling/exam/mock; S=$M/set_v1_0_0; B=$S/sen0401_mock_bank_all_v1_1_0.json; SV=v1_0_0
cd $H
nice -n 10 python3 -B mock_exclusion_index_build_v1_0_1.py > mock_exclusion_index_build_log_v1_0_1.txt           # index v1.0.1 (v8 items included)
nice -n 10 python3 -B mock_family_gate_v1_0_0.py --log mock_family_gate_log_v1_0_0.txt                           # every family instance against the index
nice -n 10 python3 -B mock_assemble_v1_0_1.py > /dev/null; cp mock_assemble_log_v1_0_1.txt /dev/null             # bank v1.1.0 into the set folder (refuses on any failure)
nice -n 10 python3 -B mock_build_v1_0_2.py $B $S --set $SV > mock_build_log_v1_0_2.txt                           # master + m1..m8
nice -n 10 python3 -B mock_test_disjoint_v1_0_0.py $B --log mock_disjoint_log_v1_1_0.txt > /dev/null
nice -n 10 python3 -B mock_exclusion_gate_v1_0_1.py --selftest --bank $B --log mock_exclusion_gate_full_bank_log_v1_1_0.txt > /dev/null
nice -n 10 python3 -B mock_exclusion_gate_v1_0_1.py --selftest --html $S/sen0401_mock_exam_master_$SV.html $S/sen0401_mock_exam_m{1..8}_$SV.html --log mock_exclusion_gate_html_log_v1_1_0.txt > /dev/null
nice -n 10 python3 -B mock_test_planted_v8_v1_0_0.py $B --log mock_planted_v8_log_v1_1_0.txt > /dev/null
nice -n 10 python3 -B mock_test_nodrop_v1_0_0.py $B --removed n3x_4,n4x_5,n4x_6,n5x_1,n5x_4,n5y_8 --log mock_nodrop_log_v1_1_0.txt > /dev/null
flock /tmp/page_test.lock nice -n 10 python3 -B mock_test_scoring_v1_0_2.py $B $S/sen0401_mock_exam_master_$SV.html --log mock_test_scoring_log_v1_1_0.txt > /dev/null
flock /tmp/page_test.lock nice -n 10 python3 -B mock_test_noextern_v1_0_0.py $S/sen0401_mock_exam_master_$SV.html $S/sen0401_mock_exam_m{1..8}_$SV.html --log mock_noextern_log_v1_1_0.txt > /dev/null
flock /tmp/page_test.lock nice -n 10 python3 -B mock_screens_v1_0_1.py $S/sen0401_mock_exam_master_$SV.html $S sen0401_mock_exam_set_$SV > mock_screens_log_v1_1_0.txt 2>&1
python3 -B mock_release_manifest_v1_0_0.py $S > mock_release_manifest_log_v1_0_0.txt
python3 -B mock_archive_move_v1_0_0.py --do > mock_archive_move_log_v1_0_0.txt                                     # superseded files to archive/ with records
python3 -B mock_release_check_v1_0_0.py selftest > mock_release_check_selftest_log_v1_0_0.txt
python3 -B mock_release_check_v1_0_0.py check --set $SV > mock_release_check_log_v1_0_0.txt
