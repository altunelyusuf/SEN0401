#!/bin/bash
export TMPDIR=/tmp/i28_ch12_own
cd /home/claude/sen0401; S=/tmp/i28_ch12_own/schedule.txt; echo "# wrapper started $(date -u +%FT%TZ)" > $S
echo "start erdprobe $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_erd_collision_probe_v1_0_0.py /home/claude/sen0401/03-materials/ch12/page/sen0401_ch12_page_v9_78_0.html > /tmp/i28_ch12_own/erd_probe.txt 2>&1
echo "end erdprobe exit $? $(date -u +%FT%TZ)" >> $S
grep -q CLEAR /tmp/i28_ch12_own/erd_probe.txt || { echo "ERD PROBE NOT CLEAR - STOP" >> $S; exit 1; }
for T in 9_37_0 9_34_1 9_35_1; do
  echo "start $T $(date -u +%FT%TZ)" >> $S
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=/tmp/i28_ch12_own/full_$T.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 12 9_78_0 > /tmp/i28_ch12_own/runner_$T.txt 2>&1
  echo "end $T exit $? $(date -u +%FT%TZ)" >> $S
done
echo "start storyprobe $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_story_layout_probe_v1_0_0.py 12 9_78_0 /tmp/i28_ch12_own/probe_story.log > /tmp/i28_ch12_own/probe_story_stdout.txt 2>&1
echo "end storyprobe exit $? $(date -u +%FT%TZ)" >> $S
echo ALLDONE >> $S
