S=/tmp/claude-0/-home-claude/7b499b1c-1b38-5415-81de-45b731a5a6db/scratchpad; R=$S/repo; O=$S/out
cd $R
echo "# wrapper started $(date -u +%FT%TZ)" > $O/schedule.txt
for T in 9_37_0 9_34_1 9_35_1; do
  echo "start $T $(date -u +%FT%TZ)" >> $O/schedule.txt
  PAGE_TEST=sen0401_page_test_v$T.py FULL_LOG=$O/page_test_${T}_full.log flock /tmp/page_test.lock bash -c "ls -d /tmp/sen0401_page_test_* | sort > $O/before_$T.txt; python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py 10 9_80_0 > $O/runner_$T.txt 2>&1; echo \$? > $O/exit_$T.txt; ls -d /tmp/sen0401_page_test_* | sort > $O/after_$T.txt"
  echo "end $T exit $(cat $O/exit_$T.txt) $(date -u +%FT%TZ)" >> $O/schedule.txt
done
for c in "5 9_84_0" "6 9_84_0" "7 9_85_0" "8 9_86_0" "10 9_80_0"; do set -- $c
  echo "start storyprobe ch$1 $(date -u +%FT%TZ)" >> $O/schedule.txt
  flock /tmp/page_test.lock python3 -B 08-tooling/sen0401_story_layout_probe_v1_0_0.py $1 $2 $O/story_layout_probe_ch$1.log > $O/story_stdout_ch$1.txt 2>&1
  echo "end storyprobe ch$1 exit $? $(date -u +%FT%TZ)" >> $O/schedule.txt
done
echo "start control ch11 on 9.52.4 build $(date -u +%FT%TZ)" >> $O/schedule.txt
flock /tmp/page_test.lock python3 -B /home/claude/sen0401/08-tooling/sen0401_erd_collision_probe_v1_0_0.py $S/w/ch11_t4/sen0401_ch11_page_v9_79_0.html > $O/probe_control_ch11_t4.txt 2>&1
echo "end control exit $? $(date -u +%FT%TZ)" >> $O/schedule.txt
echo ALLDONE >> $O/schedule.txt
