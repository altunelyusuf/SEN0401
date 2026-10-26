cd /home/claude/sen0401
S=/tmp/claude-0/-home-claude/7b499b1c-1b38-5415-81de-45b731a5a6db/scratchpad; W=$S/w
for p in "01 9_72_0" "05 9_84_0" "06 9_84_0" "07 9_85_0" "08 9_86_0" "09 9_82_0" "10 9_80_0" "11 9_79_0"; do set -- $p
 for t in 4 5; do d=$W/ch$1_t$t; mkdir -p $d
  echo "== ch$1 page $2 template 9.52.$t"
  PAGE_VER=$2 PAGE_TEMPLATE=course_page_template_v9_52_$t.html PAGE_SCRATCH=$d python3 -B 08-tooling/sen0401_page_build_v4_15_0.py $1 > $d/build.out 2>&1; echo "exit $?"; head -1 $d/build.out | cut -c1-250
 done
 diff $W/ch$1_t4/sen0401_ch$1_page_v$2.html $W/ch$1_t5/sen0401_ch$1_page_v$2.html > $W/diff_ch$1.txt; echo "diff ch$1 exit $? lines $(wc -l < $W/diff_ch$1.txt) bytes $(wc -c < $W/diff_ch$1.txt)"
done
