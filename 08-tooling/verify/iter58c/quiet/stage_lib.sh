cd /home/claude/sen0401; Q=08-tooling/verify/iter58c/quiet; S=$Q/schedule.txt; R=08-tooling/sen0401_lineage_page_test_run_v1_2_0.py
guard() { f=$(df --output=avail -k / | tail -1); if [ "$f" -lt 900000 ]; then echo "STOP disk $f KB free" >> $S; exit 1; fi; }
t() { # label chapter pagever testver
  guard; echo "start $1 $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
  PAGE_TEST=sen0401_page_test_v$4.py FULL_LOG=$Q/$1_full.log python3 -B $R $2 $3 > $Q/$1_runner.txt 2>&1
  echo "end $1 exit $? $(date -u +%FT%TZ) load $(cat /proc/loadavg)" >> $S
}
