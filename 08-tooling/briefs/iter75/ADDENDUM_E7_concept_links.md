# Addendum for E7 only (owner hint 2026-11-03 01:35: use the mock with the semantic technologies of the chapter pages)
Costs you nothing now, do not delay the core:
1. In the shell, accept an OPTIONAL field "concept" on every bank item: {"label":"...","page":"relative path of the chapter page","anchor":"#id"} or null. When present, the result view after Check shows under each item "Review this: <label>" as a link to page+anchor (opens in a new tab). When null or absent, nothing is shown. Never fail on a missing field.
2. Derivation: if at least 80 percent of the items carry a concept, prefer drawing items so that a mock does not repeat a concept in Q1 and Q4 (soft preference, never at the cost of the disjointness of mocks 1 to 8).
3. The chapter pages are read-only: never edit them. A link is written only if the anchor exists in the page (the tagging step checks it by code).
4. The tags themselves are filled in a second increment AFTER the first usable mock, by a separate step; the page questions stay off-limits as items (use them only as seeds), and the exclusion gate stays unchanged.
