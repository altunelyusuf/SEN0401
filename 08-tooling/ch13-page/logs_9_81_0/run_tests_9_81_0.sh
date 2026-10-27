#!/bin/bash
export TMPDIR=/tmp/i28_ch13_own
cd /home/claude/sen0401; S=/tmp/i28_ch13_own/schedule.txt; echo "# wrapper started $(date -u +%FT%TZ)" > $S
gate(){ while true; do L=$(cut -d' ' -f1 /proc/loadavg); awk "BEGIN{exit !($L<2.5)}" && break; sleep 20; done; echo "$1 load before: $(uptime)" >> $S; }
gate erdprobe
echo "start erdprobe $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_erd_collision_probe_v1_0_0.py /home/claude/sen0401/03-materials/ch13/page/sen0401_ch13_page_v9_81_0.html > /tmp/i28_ch13_own/erd_probe.txt 2>&1
echo "end erdprobe exit $? $(date -u +%FT%TZ)" >> $S
for T in 9_37_0 9_34_1 9_35_1; do
  gate $T
  echo "start $T $(date -u +%FT%TZ)" >> $S
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=/tmp/i28_ch13_own/full_$T.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 13 9_81_0 > /tmp/i28_ch13_own/runner_$T.txt 2>&1
  echo "end $T exit $? $(date -u +%FT%TZ)" >> $S
done
gate storyprobe
echo "start storyprobe $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_story_layout_probe_v1_0_0.py 13 9_81_0 /tmp/i28_ch13_own/probe_story.log > /tmp/i28_ch13_own/probe_story_stdout.txt 2>&1
echo "end storyprobe exit $? $(date -u +%FT%TZ)" >> $S
echo ALLDONE >> $S
