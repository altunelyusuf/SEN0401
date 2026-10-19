# Connectedness repair status (branch connectedness-repair, 2026-10-19)

Rules: BP-D56 (zero standing alone, zero islands per T-Box file) and BP-D57 (link discovery). New versioned T-Box beside each committed one; nothing overwritten; 07-lineage untouched; not merged.

| File set | New T-Box | Islands before to after | Object properties added | SHA (last commit) |
|---|---|---|---|---|
| course | 00-course-profile v1.1.0 | 2 alone to 0 alone, 0 islands (2 outward only) | 3 | d8465f8 |
| ch01 | 1.3.0 | 5 to 0 | 22 | 20eac61, 8051b2e, 9169f1a |
| ch02 | 1.4.0 | 4 to 0 | 16 | cbac04a |
| ch03 | 1.3.0 | 7 to 0 | 25 | 9cd4669 |
| ch04 | 1.3.0 | 4 to 0 | 23 | 5d05576 |
| ch05 | 1.2.0 | 7 to 0 | 23 | 3ed5583 |
| ch06 | 1.1.0 | 7 to 0 | 28 | 2d3e2a2 |
| ch07 | 1.2.0 | 8 to 0 | 17 | 25fa2c9 |
| ch08 | 1.1.0 | 6 to 0 | 14 | dd70ca6 |
| ch09 | 1.1.0 | 6 to 0 | 16 | 767c456 |
| ch10 | 1.1.0 | 6 to 0 | 15 | f752128 |
| ch11 | 1.1.0 | 5 to 0 | 10 | 73263cb |
| ch12 | 1.1.0 | 5 to 0 | 18 | 115c9aa |
| ch13 | 1.1.0 | 5 to 0 | 15 | 1d2c629 |
| ch14 | 1.1.0 | 4 to 0 | 16 | 1f186fe |
| numbers | 1.1.0 | 3 to 0 | 8 | 60f8c85 |

Chapter counts exclude chx:hasOwner domain/range (ch01-07) and the chx:input / chx:output datatype declarations. Commit messages of ch01 ("21 properties") and ch02 ("21 checks") are wrong in the pushed history; the table is correct.

Verification per chapter: oe_connectedness zero alone and zero islands (also with hasOwner left out); gate verdicts unchanged against main; HermiT consistent; Research/ChNN PASS for ch02-ch14 (ch13, ch14 included). Link discovery: 0 high-trust candidates after repair; decided medium candidates are in the link_decisions TSV and decisions md beside each T-Box (ch01, ch03, ch04, ch12).

Pre-existing on main, unchanged: Stage3.F fails in ch01 and numbers; Stage4.cov and Stage4.sub fail in ch01-04 and numbers; Cross.B CANNOT_RUN everywhere; Research/Ch01 crashes (no verify script).

Not achieved:
- Course T-Box: PartGap and TermTheme are connected only outward (cme:CoursePart, cme:CourseRepository, schema:Course). No source supports a relation between them; none invented.
- Legacy 2025 files, untouched, still fail: blockchain_wallets_tbox_v1_1_0.ttl (22 alone, 1 island), blockchain_transactions_tbox_v1_0_0.ttl (1 island, 7 outward only). blockchain_tbox_v1_0_0.ttl passes.
- Deck and Page chapter checks not run (they do not read the T-Box); no chapter check exists for numbers or runs for ch01.
- MANIFEST_SHA256.txt and PUBLISH_RECORD.ttl not updated; register recording left to the owner session.
