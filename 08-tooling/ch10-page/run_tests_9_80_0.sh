#!/bin/bash
cd /home/claude/sen0401; S=/tmp/ch10run/schedule.txt
for T in 9_37_0 9_34_1 9_35_1; do
  echo "start $T $(date -u +%FT%TZ)" >> $S
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=/tmp/ch10run/full_$T.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 10 9_80_0 > /tmp/ch10run/runner_$T.txt 2>&1
  echo "end $T exit $? $(date -u +%FT%TZ)" >> $S
done
echo "start storyprobe $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_story_layout_probe_v1_0_0.py 10 9_80_0 /tmp/ch10run/probe.log > /tmp/ch10run/probe_stdout.txt 2>&1
echo "end storyprobe exit $? $(date -u +%FT%TZ)" >> $S
echo ALLDONE >> $S
