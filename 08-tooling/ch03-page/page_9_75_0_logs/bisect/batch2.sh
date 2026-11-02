#!/bin/bash
cd /home/claude/sen0401; L=/tmp/i60
echo "hold start $(date -u +%T) load $(cat /proc/loadavg)" >> $L/batch2.sched
for V in "v1b_noplain chapter_code_ch03_v1_1_0.json" "v5_alldata73_tpl9529 chapter_code_ch03_v1_0_0.json" "v6_alldata73_tpl9524 chapter_code_ch03_v1_0_0.json"; do
  set -- $V
  python3 -B $L/vrun2.py $1 sen0401_page_test_v9_38_0.py $2 > $L/${1}_summary.txt 2>&1
  echo "$1 end $(date -u +%T) load $(cat /proc/loadavg)" >> $L/batch2.sched
done
echo ALLDONE >> $L/batch2.sched
