# Template 9.51.1 - evidence (task TK_PageGates_Template, executor SEN0401-I16-template, 2026-10-22)

## Finding on the click timeout of the chapter 11 page (FACT, measured; no workaround used)
Page 9.78.0 of chapter 11 built on template 9.51.0 (probe: template_v9_51_1_erd_probe.py, which repeats the test's steps up to the failing click):
- ERD sections choice: 16 entities, 0 overlapping pairs before any drag. erdUntangle never ran (the test has not reached its Untangle click). The entities sit on the template's grid slots.
- The test (line 1253-1257 of sen0401_page_test_v9_35_0.py, same in 9.34.0) drags the FIRST entity, BlockContainer, 120 px right and 70 px down. After the drag BlockContainer overlaps 3 entities: HeaderFields, GenesisQuirks, BackLinks.
- The test then clicks the first end of the first relationship, which is the same entity, BlockContainer (index 0). The element at its centre is the rect of HeaderFields (drawn later, so on top). Playwright reports "<rect ...> from <g data-ent=HeaderFields> subtree intercepts pointer events".
- Chapter 10: the dragged entity is FlatNetwork, the entity clicked is Discovery; 0 overlapping pairs before and after the drag; the click works.
- On template 9.51.1 the same probe gives the identical result (3 overlapping pairs after the drag, HeaderFields at the click point).
Conclusion: the timeout does NOT come from the template layout (no entity overlaps before the test's drag; neither rlUntangle nor erdUntangle is involved). It comes from the test's own sequence: it drags an entity onto its neighbours and then clicks that same entity. It is a test artefact, so template 9.51.1 does not change it, and erdUntangle is left unchanged. A test change (choosing the click target not dragged) is outside this task (9.35.1 changes one assertion only) and needs the coordinator's/owner's ruling.

## Cause of the concept-map overlaps (rlUntangle, 9.51.0)
Probe template_v9_51_1_map_probe.py (drag target chosen as the test does, then Untangle, boxes and overlaps measured as the test does with rlCenters):
- 9.51.0, chapter 10: boxes 24, overlaps 2 (LightClients/Spv, EncryptedTransport/OrphanPool). Chapter 11: boxes 22, overlaps 4 (HeaderFields/HeightAndMaturity, BlockIdentifiers/GenesisConstants, HashIdentity/GenesisConstants, GenesisBlock/BackLinks).
- Reason: with 40 and 48 section edges the link springs (pull 0.4 per unit beyond 190) outweigh the overlap push, whose step is capped by the cooling temperature (18 falling to 1 over 90 passes), so overlaps left at the end are not resolved.

## Diff 9.51.0 -> 9.51.1 (2 lines of 5000+)
- line 2: a version comment for 9.51.1 placed before the 9.51.0 comment (names the change and the reason).
- line 690, function rlUntangle, end of the last step: before the result is applied through rlPlace, a separation loop (at most 400 passes) pushes every still-overlapping pair apart along the axis of least overlap, to the same 12 px gap the force passes use, boxes marked fixed stay, positions clamped to the view box as before. No other function, text, style or threshold differs. erdUntangle unchanged.

## Build of the scratch pages
Builder sen0401_page_build_v4_14_0.py, run from a scratch tree outside the repository (symlinks to the repository folders, own copies of 08-tooling/chNN-page and an empty 03-materials/chNN/page), with env PAGE_VER=9_78_0 and PAGE_TEMPLATE=course_page_template_v9_51_1.html (the builder reads the template from 08-tooling/<PAGE_TEMPLATE>; default in the builder is 9.44.0). The 9.51.0 control was built the same way (PAGE_TEMPLATE=course_page_template_v9_51_0.html); it differs from the shipped 9.78.0 pages in one line of the generated page (lineage data read from the newer 07-lineage register), not in the template.

## Results as printed (9.51.1, drag, Untangle, measured as the page test measures)
- chapter 10: AFTER UNTANGLE: boxes 24 overlaps 0 meanEdge 201 outside 0; Reset: moved boxes 0 (9.51.0: overlaps 2, meanEdge 200)
- chapter 11: AFTER UNTANGLE: boxes 22 overlaps 0 meanEdge 208 outside 0; Reset: moved boxes 0 (9.51.0: overlaps 4, meanEdge 204)
- Untangle time 467 ms and 401 ms (9.51.0: 396 and 423 ms).
- Click timeout of chapter 11: NOT resolved by the template (see finding): still "HeaderFields" at the click point on 9.51.1.
- Full page tests not run (the regression task does).
