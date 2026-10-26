#!/bin/bash
# second run of page test 9.37.0 on page 9_78_0, to keep its results.json as the stored result (the folder of the first run was removed with my temporary directory before it was copied)
export TMPDIR=/tmp/i28_ch12_own
cd /home/claude/sen0401; S=/tmp/i28_ch12_own/rerun37_schedule.txt; : > $S
while true; do L=$(cut -d' ' -f1 /proc/loadavg); awk "BEGIN{exit !($L<2.5)}" && break; sleep 30; done
echo "uptime before: $(uptime)" >> $S; echo "start $(date -u +%FT%TZ)" >> $S
PAGE_TEST=sen0401_page_test_v9_37_0.py FULL_LOG=/tmp/i28_ch12_own/rerun37_full.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 12 9_78_0 > /tmp/i28_ch12_own/rerun37_runner.txt 2>&1
echo "end exit $? $(date -u +%FT%TZ); uptime after: $(uptime)" >> $S; echo ALLDONE >> $S
