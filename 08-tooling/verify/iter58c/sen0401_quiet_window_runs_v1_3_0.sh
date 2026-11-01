#!/bin/bash
# (v1_3_0: the stages ch02, ch01, ch03, ch04 of v1_0_0, which was stopped at its time limit before they started) the lineage agent's quiet-window runs, stage by stage; each stage holds /tmp/page_test.lock for the whole stage, so nothing runs between the tests of a stage.
cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule4.txt; R=08-tooling/sen0401_lineage_page_test_run_v1_2_0.py
cat > $Q/stage_lib.sh <<'L'
cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule4.txt; R=08-tooling/sen0401_lineage_page_test_run_v1_2_0.py
guard() { f=$(df --output=avail -k / | tail -1); if [ "$f" -lt 900000 ]; then echo "STOP disk $f KB free" >> $S; exit 1; fi; }
t() { # label chapter pagever testver
  guard; echo "start $1 $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
  PAGE_TEST=sen0401_page_test_v$4.py FULL_LOG=$Q/$1_full.log python3 -B $R $2 $3 > $Q/$1_runner.txt 2>&1
  echo "end $1 exit $? $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
}
L
stage() { name=$1; shift; echo "queued $name $(date -u +%FT%TZ)" >> $S; flock /tmp/page_test.lock bash -c "source $Q/stage_lib.sh; $*"; echo "stage $name done $(date -u +%FT%TZ)" >> $S; }
stage ch02 "t ch02_9_73_0_t9_37_0 02 9_73_0 9_37_0; t ch02_9_73_0_t9_34_2 02 9_73_0 9_34_2; echo start ch02_panels \$(date -u +%FT%TZ) >> \$S; python3 -B 08-tooling/sen0401_page_panels_test_v1_0_0.py 03-materials/ch02/page/sen0401_ch02_page_v9_73_0.html /tmp/q_panels2 > \$Q/ch02_panels.txt 2>&1; echo end ch02_panels exit \$? \$(date -u +%FT%TZ) >> \$S; echo start ch02_chk \$(date -u +%FT%TZ) >> \$S; python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_7_0.py Page/Ch02 > \$Q/ch02_chaptercheck_Page.txt 2>&1; echo end ch02_chk exit \$? \$(date -u +%FT%TZ) >> \$S"
stage ch01 "t ch01_9_74_0_t9_37_0 01 9_74_0 9_37_0; t ch01_9_74_0_t9_34_2 01 9_74_0 9_34_2"
stage ch04 "t ch04_9_75_0_t9_37_0 04 9_75_0 9_37_0; t ch04_9_75_0_t9_34_2 04 9_75_0 9_34_2"
echo ALLDONE >> $S
