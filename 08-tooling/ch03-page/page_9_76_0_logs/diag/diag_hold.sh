#!/bin/bash
# diagnostic hold: diag copy of 9.38.0 (stamps long tasks) on v9_75_0, 5 runs unloaded then 2 runs under two busy loops
cd /home/claude/sen0401; L=08-tooling/ch03-page/page_9_76_0_logs/diag; S=$L/schedule.txt
one() { echo "start $1 $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
  PAGE_TEST=/home/claude/sen0401/08-tooling/sen0401_i63_diag_page_test_v1_0_0.py FULL_LOG=$L/$1_full.log python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 03 9_75_0 > $L/$1_runner.txt 2>&1
  echo "end $1 exit $? $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S; }
for i in 1 2 3 4 5; do one run${i}_v9_75_0_plain; done
python3 -c "while True: pass" & P1=$!; python3 -c "while True: pass" & P2=$!
for i in 1 2; do one run${i}_v9_75_0_busy; done
kill $P1 $P2
echo "hold done $(date -u +%FT%TZ)" >> $S
