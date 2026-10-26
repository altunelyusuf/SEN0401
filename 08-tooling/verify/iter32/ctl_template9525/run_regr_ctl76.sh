#!/bin/bash
# lineage agent's control run: page tests on the chapter 10 scratch page built from the template 9.52.5 (scratch tree W of symlinks, like the executor's), temp folders of the runs under /tmp/claude-0/ctl76tmp (mine, removed afterwards)
R=/home/claude/sen0401; D=$R/08-tooling/verify/iter32/ctl_template9525; W=/tmp/claude-0/ctl76w; export TMPDIR=/tmp/claude-0/ctl76tmp
rm -rf $W $TMPDIR; mkdir -p $W/03-materials $TMPDIR
for e in $R/* $R/.[a-z]*; do b=$(basename $e); [ "$b" = 03-materials ] && continue; ln -s $e $W/$b; done
for c in $R/03-materials/*; do b=$(basename $c); if [ "$b" = ch10 ]; then mkdir -p $W/03-materials/ch10/page; for e in $c/*; do [ "$(basename $e)" = page ] || ln -s $e $W/03-materials/ch10/$(basename $e); done; for e in $c/page/*; do ln -s $e $W/03-materials/ch10/page/$(basename $e); done; else ln -s $c $W/03-materials/$b; fi; done
rm $W/03-materials/ch10/page/sen0401_ch10_page_v9_80_0.html
cd $R && PAGE_VER=9_80_0 PAGE_TEMPLATE=course_page_template_v9_52_5.html PAGE_SCRATCH=$W/03-materials/ch10/page python3 -B 08-tooling/sen0401_page_build_v4_15_0.py 10 > $D/regr_build.txt 2>&1; echo "build exit $?" >> $D/regr_runner.txt
cd $W
for T in 9_37_0 9_34_1 9_35_1; do
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=$D/regr_ch10_page_9_80_0_test_$T.full.log flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 10 9_80_0 > $D/regr_ch10_page_9_80_0_test_$T.run.log 2>&1
  echo "ch10 scratch 9_80_0 on 9.52.5 test $T exit $?" >> $D/regr_runner.txt
done
echo ALLDONE >> $D/regr_runner.txt
ls -d $TMPDIR/* > $D/regr_temp_folders_created.txt 2>/dev/null
