#!/bin/bash
# one lock hold: probe on 9_74_0 (diagnostic copy of 9.38.0 that stamps long tasks), then 9.38.0 on the four one-difference-undone variants
cd /home/claude/sen0401; L=/tmp/i60
echo "hold start $(date -u +%T) load $(cat /proc/loadavg)" >> $L/batch1.sched
PAGE_TEST=sen0401_i60_probe_test.py FULL_LOG=$L/probe74_full.log python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 03 9_74_0 > $L/probe74_runner.txt 2>&1
echo "probe end $(date -u +%T) load $(cat /proc/loadavg)" >> $L/batch1.sched
for V in v1_noplain v2_oldlecture v3_oldchaptercode v4_tpl9524; do
  python3 -B $L/vrun.py $L/$V/sen0401_ch03_page_v9_74_0.html $V sen0401_page_test_v9_38_0.py > $L/${V}_summary.txt 2>&1
  echo "$V end $(date -u +%T) load $(cat /proc/loadavg)" >> $L/batch1.sched
done
echo ALLDONE >> $L/batch1.sched
