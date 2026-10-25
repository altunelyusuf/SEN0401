#!/bin/bash
# runs the Stage 4 gates and the three lineage chapter checks and the deck match check for chapter 6 (page 9.84.0); the Page check under the lock; each output written once, after its run
cd /home/claude/sen0401; D=08-tooling/ch06-page; P=python3
$P -B 08-tooling/sen0401_stage4_gates_v1_1_0.py 06 > /tmp/ch06_s4.out 2>&1; echo "stage4 exit $?" >> /tmp/ch06_checks.state
$P -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Research/Ch06 > /tmp/ch06_res.out 2>&1; echo "research exit $?" >> /tmp/ch06_checks.state
$P -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Deck/Ch06 > /tmp/ch06_deck.out 2>&1; echo "deck exit $?" >> /tmp/ch06_checks.state
$P -B 08-tooling/pages_deck_match_verify_v1_0_0.py 06 > /tmp/ch06_match.out 2>&1; echo "match exit $?" >> /tmp/ch06_checks.state
flock /tmp/page_test.lock $P -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Page/Ch06 > /tmp/ch06_page.out 2>&1; echo "page exit $?" >> /tmp/ch06_checks.state
echo ALLDONE >> /tmp/ch06_checks.state
