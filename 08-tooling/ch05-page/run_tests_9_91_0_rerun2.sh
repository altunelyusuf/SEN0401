#!/bin/bash
# rerun 2: root-cause control. 9.38.0 on the OLD page 9.84.0 (same machine, same test), then 9.38.0 on the new page 9.91.0 again; new logs, earlier ones kept
cd /home/claude/sen0401; L=08-tooling/ch05-page/page_9_91_0_logs; S=$L/schedule_rerun2.txt
for P in 9_84_0 9_91_0; do
  echo "start 9_38_0 on $P $(date -u +%FT%TZ)" >> $S
  PAGE_TEST=sen0401_page_test_v9_38_0.py FULL_LOG=$L/rerun2_page_test_9_38_0_on_${P}_full.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 05 $P > $L/rerun2_runner_9_38_0_on_$P.txt 2>&1
  echo "end 9_38_0 on $P exit $? $(date -u +%FT%TZ)" >> $S
done
echo ALLDONE >> $S
