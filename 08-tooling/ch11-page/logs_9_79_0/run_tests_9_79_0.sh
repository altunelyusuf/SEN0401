#!/bin/bash
cd /home/claude/sen0401; S=/tmp/ch11run_i27/schedule.txt
echo "# ch11 session SEN0401-I27-page-ch11 schedule; wrapper started $(date -u +%FT%TZ)" > $S
for T in 9_37_0 9_34_1 9_35_1; do
  echo "start $T $(date -u +%FT%TZ)" >> $S
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=/tmp/ch11run_i27/full_$T.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 11 9_79_0 > /tmp/ch11run_i27/runner_$T.txt 2>&1
  echo "end $T exit $? $(date -u +%FT%TZ)" >> $S
done
echo "start storyprobe $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_story_layout_probe_v1_0_0.py 11 9_79_0 /tmp/ch11run_i27/probe.log > /tmp/ch11run_i27/probe_stdout.txt 2>&1
echo "end storyprobe exit $? $(date -u +%FT%TZ)" >> $S
echo ALLDONE >> $S
