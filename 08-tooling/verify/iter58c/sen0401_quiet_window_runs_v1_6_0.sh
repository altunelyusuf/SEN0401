#!/bin/bash
# seventh set (one stage per call): usage v1_6_0.sh ch03ctl | flaky
#  ch03ctl: the lineage agent's control of the Ch03 repair page v9_75_0 against the shipped v9_73_0, all in one lock hold: 9.38.0 (v9_75_0, v9_73_0), 9.34.3 (v9_75_0, v9_73_0), the panel test on v9_75_0, the Page/Ch03 chapter check v1_7_0.
#  flaky: the third runs of the two flaky features by the rule 'rerun before counting odd failures': 9.38.0 on Ch02 v9_73_0 and on Ch04 v9_75_0, one lock hold each.
cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule7.txt
stage() { name=$1; shift; echo "queued $name $(date -u +%FT%TZ)" >> $S; flock /tmp/page_test.lock bash -c "source $Q/stage_lib.sh; S=$Q/schedule7.txt; $*"; echo "stage $name done $(date -u +%FT%TZ)" >> $S; }
case $1 in
  ch03ctl) stage ch03ctl "t ch03ctl_9_75_0_t9_38_0 03 9_75_0 9_38_0; t ch03ctl_9_73_0_t9_38_0 03 9_73_0 9_38_0; t ch03ctl_9_75_0_t9_34_3 03 9_75_0 9_34_3; t ch03ctl_9_73_0_t9_34_3 03 9_73_0 9_34_3; echo start ch03ctl_panels \$(date -u +%FT%TZ) >> \$S; python3 -B 08-tooling/sen0401_page_panels_test_v1_0_0.py 03-materials/ch03/page/sen0401_ch03_page_v9_75_0.html /tmp/q_panels3 > \$Q/ch03ctl_panels.txt 2>&1; echo end ch03ctl_panels exit \$? \$(date -u +%FT%TZ) >> \$S; echo start ch03ctl_chk \$(date -u +%FT%TZ) >> \$S; python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_7_0.py Page/Ch03 > \$Q/ch03ctl_chaptercheck_Page.txt 2>&1; echo end ch03ctl_chk exit \$? \$(date -u +%FT%TZ) >> \$S; rm -rf /tmp/q_panels3" ;;
  flaky) stage ch02third "t ch02third_9_73_0_t9_38_0 02 9_73_0 9_38_0"; stage ch04third "t ch04third_9_75_0_t9_38_0 04 9_75_0 9_38_0" ;;
esac
