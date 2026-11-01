#!/bin/bash
# second set of quiet-window runs (the coordinator's Ch03 request): Ch03 page v9_74_0 against the shipped v9_73_0, back to back under one lock hold, with the budget-carrying tests 9.38.0 and 9.34.3, v9_73_0 and v9_74_0 alternating.
cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule2.txt
echo "queued ch03cmp $(date -u +%FT%TZ)" >> $S
flock /tmp/page_test.lock bash -c "source $Q/stage_lib.sh; S=$Q/schedule2.txt; t ch03cmp_9_74_0_t9_38_0 03 9_74_0 9_38_0; t ch03cmp_9_73_0_t9_38_0 03 9_73_0 9_38_0; t ch03cmp_9_74_0_t9_34_3 03 9_74_0 9_34_3; t ch03cmp_9_73_0_t9_34_3 03 9_73_0 9_34_3"
echo "stage ch03cmp done $(date -u +%FT%TZ)" >> $S; echo ALLDONE >> $S
