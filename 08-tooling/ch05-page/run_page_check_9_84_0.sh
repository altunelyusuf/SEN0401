#!/bin/bash
# runs the lineage Page chapter check for chapter 5 under the lock; output written once, after the run
cd /home/claude/sen0401; O=08-tooling/ch05-page/chapter_check_Page_v9_84_0.txt
echo "start $(date -u +%FT%TZ)" > /tmp/page_check_ch05.state
flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Page/Ch05 > /tmp/page_check_ch05.out 2>&1
echo "exit $? $(date -u +%FT%TZ)" >> /tmp/page_check_ch05.state
cp /tmp/page_check_ch05.out $O; echo DONE >> /tmp/page_check_ch05.state
