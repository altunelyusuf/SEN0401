#!/bin/bash
# runs the page tests 9.37.0, 9.34.1, 9.35.1 and the story layout probe on the chapter 5 page 9.84.0, serially, each under flock /tmp/page_test.lock
cd /home/claude/sen0401; L=08-tooling/ch05-page/logs_9_84_0; S=$L/schedule.txt
for T in 9_37_0 9_34_1 9_35_1; do
  echo "start $T $(date -u +%FT%TZ)" >> $S
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=$L/page_test_${T}_full.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 05 9_84_0 > $L/runner_$T.txt 2>&1
  echo "end $T exit $? $(date -u +%FT%TZ)" >> $S
done
echo "start storyprobe $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_story_layout_probe_v1_0_0.py 05 9_84_0 $L/story_layout_probe_9_84_0.log > $L/story_layout_probe_stdout.txt 2>&1
echo "end storyprobe exit $? $(date -u +%FT%TZ)" >> $S
echo ALLDONE >> $S
