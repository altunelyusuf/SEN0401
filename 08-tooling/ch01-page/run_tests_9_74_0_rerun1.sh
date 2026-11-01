#!/bin/bash
# runs the page tests 9.34.3, 9.38.0 and 9.35.3 and the panel test on the chapter 1 page 9.74.0, serially, each under flock /tmp/page_test.lock, each as its own log
cd /home/claude/sen0401; L=08-tooling/ch01-page/page_9_74_0_logs; S=$L/schedule_rerun1.txt
for T in 9_38_0 9_34_3; do
  echo "start $T $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=$L/rerun1_page_test_${T}_full.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 01 9_74_0 > $L/rerun1_runner_$T.txt 2>&1
  echo "end $T exit $? $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
done

echo ALLDONE >> $S
