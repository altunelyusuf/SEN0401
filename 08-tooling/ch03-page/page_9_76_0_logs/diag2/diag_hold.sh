#!/bin/bash
# diagnostic hold 2: diag copy v1.1.0 (adds a V8 CPU profile per long task) - v9_75_0 plain once, then under two busy loops: v9_75_0 twice, v9_73_0 once
cd /home/claude/sen0401; L=08-tooling/ch03-page/page_9_76_0_logs/diag2; S=$L/schedule.txt
one() { echo "start $1 $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
  PAGE_TEST=/home/claude/sen0401/08-tooling/sen0401_i63_diag_page_test_v1_1_0.py FULL_LOG=$L/$1_full.log python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 03 $2 > $L/$1_runner.txt 2>&1
  echo "end $1 exit $? $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S; }
one runA_v9_75_0_plain 9_75_0
python3 -c "while True: pass" & P1=$!; python3 -c "while True: pass" & P2=$!
one runB_v9_75_0_busy 9_75_0
one runC_v9_75_0_busy 9_75_0
one runD_v9_73_0_busy 9_73_0
kill $P1 $P2
echo "hold done $(date -u +%FT%TZ)" >> $S
