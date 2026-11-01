#!/bin/bash
# third set of quiet-window runs: Ch04 page v9_75_0 against the shipped v9_74_0 (budget feature, back to back under one lock hold) and the Page/Ch04 chapter check; Ch01 v9_74_0 against v9_73_0 likewise.
cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule3.txt
echo "queued ch04cmp $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock bash -c "source $Q/stage_lib.sh; S=$Q/schedule3.txt; t ch04cmp_9_75_0_t9_38_0 04 9_75_0 9_38_0; t ch04cmp_9_74_0_t9_38_0 04 9_74_0 9_38_0; echo start ch04_chk \$(date -u +%FT%TZ) >> \$S; python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_7_0.py Page/Ch04 > \$Q/ch04_chaptercheck_Page.txt 2>&1; echo end ch04_chk exit \$? \$(date -u +%FT%TZ) >> \$S"
echo "queued ch01cmp $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock bash -c "source $Q/stage_lib.sh; S=$Q/schedule3.txt; t ch01cmp_9_74_0_t9_38_0 01 9_74_0 9_38_0; t ch01cmp_9_73_0_t9_38_0 01 9_73_0 9_38_0"
echo ALLDONE >> $S
