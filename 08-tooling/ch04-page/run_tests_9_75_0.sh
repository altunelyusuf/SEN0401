#!/bin/bash
# runs the page tests 9.34.3, 9.38.0 and 9.35.3 and the panel test on the chapter 4 page 9.75.0, serially, each under flock /tmp/page_test.lock, each as its own log
cd /home/claude/sen0401; L=08-tooling/ch04-page/page_9_75_0_logs; S=$L/schedule.txt
for T in 9_34_3 9_38_0 9_35_3; do
  echo "start $T $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=$L/page_test_${T}_full.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 04 9_75_0 > $L/runner_$T.txt 2>&1
  echo "end $T exit $? $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
done
echo "start panels $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_page_panels_test_v1_0_0.py 03-materials/ch04/page/sen0401_ch04_page_v9_75_0.html /tmp/i52d4_panels > $L/panels_test.txt 2>&1
echo "end panels exit $? $(date -u +%FT%TZ)" >> $S
echo ALLDONE >> $S
