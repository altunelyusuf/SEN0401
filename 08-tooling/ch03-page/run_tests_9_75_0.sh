#!/bin/bash
# chapter 3 page 9.75.0 proof (task TK_Repair_Ch03_Page_Build). Step 1: ONE hold of /tmp/page_test.lock for the pair, back to back:
# 9.38.0 on 9.75.0 then on the shipped 9.73.0, then 9.34.3 on 9.75.0 then on 9.73.0. Step 2: each remaining test under its own hold.
cd /home/claude/sen0401; L=08-tooling/ch03-page/page_9_75_0_logs; S=$L/schedule.txt
run() { # run NAME PAGEVER TEST
  echo "start $1 $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
  PAGE_TEST=sen0401_page_test_v$3.py FULL_LOG=$L/page_test_$1_full.log python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 03 $2 > $L/runner_$1.txt 2>&1
  echo "end $1 exit $? $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
}
export -f run; export L S
flock /tmp/page_test.lock bash -c '
run 9_38_0_on_9_75_0 9_75_0 9_38_0
run 9_38_0_on_9_73_0 9_73_0 9_38_0
run 9_34_3_on_9_75_0 9_75_0 9_34_3
run 9_34_3_on_9_73_0 9_73_0 9_34_3'
echo "pair hold released $(date -u +%FT%TZ)" >> $S
run_locked() { flock /tmp/page_test.lock bash -c "$(declare -f run); L=$L; S=$S; $*"; }
run_locked run 9_37_0_on_9_75_0 9_75_0 9_37_0
run_locked run 9_34_2_on_9_75_0 9_75_0 9_34_2
echo "start panels $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_page_panels_test_v1_0_0.py 03-materials/ch03/page/sen0401_ch03_page_v9_75_0.html /tmp/i60_panels3 > $L/panels_test.txt 2>&1
echo "end panels exit $? $(date -u +%FT%TZ)" >> $S
echo "start chapter check Page/Ch03 $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_7_0.py Page/Ch03 > $L/chapter_check_Page.txt 2>&1
echo "end chapter check Page/Ch03 exit $? $(date -u +%FT%TZ)" >> $S
echo ALLDONE >> $S
