#!/bin/bash
# sixth set (one stage per call, because a background call is stopped after two hours): usage: v1_5_0.sh ch01cmp | ch02rerun
cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule6.txt
stage() { name=$1; shift; echo "queued $name $(date -u +%FT%TZ)" >> $S; flock /tmp/page_test.lock bash -c "source $Q/stage_lib.sh; S=$Q/schedule6.txt; $*"; echo "stage $name done $(date -u +%FT%TZ)" >> $S; }
case $1 in
  ch01cmp) stage ch01cmp "t ch01cmp_9_74_0_t9_38_0 01 9_74_0 9_38_0; t ch01cmp_9_73_0_t9_38_0 01 9_73_0 9_38_0" ;;
  ch02rerun) stage ch02rerun "t ch02rerun_9_73_0_t9_38_0 02 9_73_0 9_38_0" ;;
esac
