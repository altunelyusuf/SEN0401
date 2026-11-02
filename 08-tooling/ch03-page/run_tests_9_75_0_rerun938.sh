#!/bin/bash
# re-run of the pair 9.38.0 on 9.75.0 then on the shipped 9.73.0 under ONE hold (the first run of 9.38.0 on 9.75.0 printed one FAIL line, the second budget feature, after load 235 ms over 2 long tasks)
cd /home/claude/sen0401; L=08-tooling/ch03-page/page_9_75_0_logs; S=$L/schedule_rerun938.txt; N=${1:-2}
run() { echo "start $1 $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
  PAGE_TEST=sen0401_page_test_v9_38_0.py FULL_LOG=$L/page_test_$1_full.log python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 03 $2 > $L/runner_$1.txt 2>&1
  echo "end $1 exit $? $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S; }
export -f run; export L S
flock /tmp/page_test.lock bash -c "run 9_38_0_on_9_75_0_run$N 9_75_0; run 9_38_0_on_9_73_0_run$N 9_73_0"
echo ALLDONE >> $S
