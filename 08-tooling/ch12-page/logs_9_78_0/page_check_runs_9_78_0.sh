#!/bin/bash
# Page/Ch12 chapter check runs (run 1 failed the load-dependent budget right after a container restart, load average 2.29; reruns up to 3 as decided by the coordinator, start only below 2.5)
export TMPDIR=/tmp/i28_ch12_own; mkdir -p $TMPDIR
cd /home/claude/sen0401; S=/tmp/i28_ch12_own/pc_schedule.txt; : > $S
for N in 2 3 4; do
  while true; do L=$(cut -d' ' -f1 /proc/loadavg); awk "BEGIN{exit !($L<1.5)}" && break; sleep 30; done
  echo "run $N uptime before: $(uptime)" >> $S
  flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Page/Ch12 > 08-tooling/ch12-page/chapter_check_Page_9_78_0_run$N.txt 2>&1
  echo "run $N exit $? uptime after: $(uptime)" >> $S
  grep -q "RESULT Page/Ch12: PASS" 08-tooling/ch12-page/chapter_check_Page_9_78_0_run$N.txt && break
done
echo ALLDONE >> $S
