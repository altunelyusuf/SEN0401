# Executor briefs of the page gates (generated from sen0401_slides_lineage_v0_180_0.ttl)

The Verify tasks (TK_SecLinks_Ch10_Verify, TK_SecLinks_Ch11_Verify) have no executor: the builder session controls and runs the evidence bridge after the executors report. The earlier briefs of the page tasks (08-tooling/briefs/iter14/BRIEF_TK_SecLinks_Ch1[01]_Page.md) are superseded by the ones here.

| Task | Executor session | Can start |
|---|---|---|
| TK_PageGates_Template | SEN0401-I16-template | yes |
| TK_PageGates_Test | SEN0401-I16-test | yes |
| TK_PageGates_Regression | SEN0401-I16-regression | no, after TK_PageGates_Template, TK_PageGates_Test |
| TK_SecLinks_Ch10_Page | SEN0401-I14-page-ch10-r2 | no, after TK_PageGates_Template, TK_PageGates_Test, TK_PageGates_Regression |
| TK_SecLinks_Ch11_Page | SEN0401-I14-page-ch11-r2 | no, after TK_PageGates_Template, TK_PageGates_Test, TK_PageGates_Regression |
