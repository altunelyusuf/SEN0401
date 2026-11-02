#!/bin/bash
# assemble -> build -> disjointness -> gate (bank, html) -> scoring test (real bank, sample with all four families). Logs next to this script.
H=/home/claude/sen0401/08-tooling/exam/mock; M=/home/claude/CME/exams/SEN0401/08-tooling/exam/mock; S=$M/sample; cd $H
python3 mock_assemble_v1_0_0.py > /tmp/claude-0/run_assemble.out 2>&1 || { echo ASSEMBLE FAILED; cat /tmp/claude-0/run_assemble.out; exit 1; }
python3 mock_build_v1_0_0.py $M/mock_bank_all_v1_0_0.json $M > mock_build_log_v1_0_0.txt
(cd $M && sha256sum mock_bank_all_v1_0_0.json mock_ch_all_*.html > SHA256.txt)
python3 mock_test_disjoint_v1_0_0.py $M/mock_bank_all_v1_0_0.json --log mock_disjoint_log_v1_0_0.txt > /dev/null
nice -n 10 python3 mock_exclusion_gate_v1_0_0.py --selftest --bank $M/mock_bank_all_v1_0_0.json --log mock_exclusion_gate_full_bank_log_v1_0_0.txt > /dev/null
nice -n 10 python3 mock_exclusion_gate_v1_0_0.py --selftest --html $M/mock_ch_all_master.html $M/mock_ch_all_mock1.html $M/mock_ch_all_mock2.html $M/mock_ch_all_mock3.html $M/mock_ch_all_mock4.html $M/mock_ch_all_mock5.html $M/mock_ch_all_mock6.html $M/mock_ch_all_mock7.html $M/mock_ch_all_mock8.html --log mock_exclusion_gate_html_log_v1_0_0.txt > /dev/null
flock /tmp/page_test.lock nice -n 10 python3 mock_test_scoring_v1_0_0.py $M/mock_bank_all_v1_0_0.json $M/mock_ch_all_master.html --log mock_test_scoring_log_v1_0_0.txt > /dev/null
python3 mock_build_v1_0_0.py $S/mock_bank_sample_families.json $S --sample > /dev/null
flock /tmp/page_test.lock nice -n 10 python3 mock_test_scoring_v1_0_0.py $S/mock_bank_sample_families.json $S/SAMPLE_mock_ch_all_master.html --log mock_test_scoring_sample_log_v1_0_0.txt > /dev/null
flock /tmp/page_test.lock nice -n 10 python3 mock_screens_v1_0_0.py $M/mock_ch_all_master.html $M/screens > mock_screens_log_v1_0_0.txt 2>&1
echo RUNALL DONE > /tmp/claude-0/runall.flag
