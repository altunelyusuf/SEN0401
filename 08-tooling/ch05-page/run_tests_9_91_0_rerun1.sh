#!/bin/bash
# rerun 1 of the page tests on the chapter 5 page 9.91.0 (9.34.3 was killed by SIGTERM at 26 s; 9.38.0 and 9.35.3 failed only the main-thread budget feature); new logs, the first ones kept
cd /home/claude/sen0401; L=08-tooling/ch05-page/page_9_91_0_logs; S=$L/schedule_rerun1.txt
for T in 9_34_3 9_38_0 9_35_3; do
  echo "start $T $(date -u +%FT%TZ)" >> $S
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=$L/rerun1_page_test_${T}_full.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 05 9_91_0 > $L/rerun1_runner_$T.txt 2>&1
  echo "end $T exit $? $(date -u +%FT%TZ)" >> $S
done
echo ALLDONE >> $S
