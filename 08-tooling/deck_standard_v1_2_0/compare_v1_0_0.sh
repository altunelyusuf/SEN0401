#!/bin/bash
# For chapters 1-14: newest deck, v1_1_0 vs v1_2_0 element results side by side. Usage: compare_v1_0_0.sh
T="$(cd "$(dirname "$0")/.." && pwd)"
for n in 01 02 03 04 05 06 07 08 09 10 11 12 13 14; do
  a=$(python3 -B "$T/sen0401_deck_standard_check_v1_1_0.py" $n 2>&1 | grep -E "^D[0-9]+ " | awk '{print $1":"$2}')
  b=$(python3 -B "$T/sen0401_deck_standard_check_v1_2_0.py" $n 2>&1 | grep -E "^D[0-9]+ " | awk '{print $1":"$2}')
  echo "ch$n v1_1_0: $(echo $a)"; echo "ch$n v1_2_0: $(echo $b)"
  [ "$a" == "$b" ] && echo "ch$n EQUAL" || echo "ch$n DIFFERENT"
done
