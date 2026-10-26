#!/bin/bash
# reruns of page test 9.35.1 on page 9_78_0 (coordinator decision): up to 3, stop at the first pass; start only when load average (1 min) < 2.5
export TMPDIR=/tmp/i28_ch12_own
cd /home/claude/sen0401; S=/tmp/i28_ch12_own/rerun_schedule.txt; : > $S
for N in 1 2 3; do
  while true; do L=$(cut -d' ' -f1 /proc/loadavg); awk "BEGIN{exit !($L<2.5)}" && break; sleep 30; done
  echo "run $N uptime before: $(uptime)" >> $S
  echo "start run $N $(date -u +%FT%TZ)" >> $S
  PAGE_TEST=sen0401_page_test_v9_35_1.py FULL_LOG=/tmp/i28_ch12_own/rerun${N}_full.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 12 9_78_0 > /tmp/i28_ch12_own/rerun${N}_runner.txt 2>&1
  echo "end run $N exit $? $(date -u +%FT%TZ); uptime after: $(uptime)" >> $S
  grep -q "RESULT: PASS" /tmp/i28_ch12_own/rerun${N}_runner.txt && break
done
echo ALLDONE >> $S
