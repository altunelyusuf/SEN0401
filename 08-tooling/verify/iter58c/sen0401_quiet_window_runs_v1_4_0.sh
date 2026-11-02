#!/bin/bash
# fifth set: the older committed tests 9.37.0 and 9.34.2 crash on the Playground of the new pages (they do not know the 'cc:' example values that 9.34.3 handles), so they are not run again on Ch01 and Ch04; instead the budget-carrying 9.38.0 is run again where a feature failed or the comparison is missing: Ch04 v9_75_0 once more, Ch01 v9_74_0 against v9_73_0 (one lock hold), then Ch02 v9_73_0 once more.
cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule5.txt
stage() { name=$1; shift; echo "queued $name $(date -u +%FT%TZ)" >> $S; flock /tmp/page_test.lock bash -c "source $Q/stage_lib.sh; S=$Q/schedule5.txt; $*"; echo "stage $name done $(date -u +%FT%TZ)" >> $S; }
stage ch04rerun "t ch04rerun_9_75_0_t9_38_0 04 9_75_0 9_38_0"
stage ch01cmp "t ch01cmp_9_74_0_t9_38_0 01 9_74_0 9_38_0; t ch01cmp_9_73_0_t9_38_0 01 9_73_0 9_38_0"
stage ch02rerun "t ch02rerun_9_73_0_t9_38_0 02 9_73_0 9_38_0"
echo ALLDONE >> $S
