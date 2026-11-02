#!/bin/bash
# eighth set: usage v1_7_0.sh ch03rep
#  ch03rep: two repeat runs of 9.38.0 on the Ch03 repair page v9_75_0 in one lock hold (the first control run had one 2063 ms task after load; the executor's two runs had none).
cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule8.txt
stage() { name=$1; shift; echo "queued $name $(date -u +%FT%TZ)" >> $S; flock /tmp/page_test.lock bash -c "source $Q/stage_lib.sh; S=$Q/schedule8.txt; $*"; echo "stage $name done $(date -u +%FT%TZ)" >> $S; }
case $1 in
  ch03rep) stage ch03rep "t ch03rep1_9_75_0_t9_38_0 03 9_75_0 9_38_0; t ch03rep2_9_75_0_t9_38_0 03 9_75_0 9_38_0" ;;
esac
