# Executor briefs of iteration 14 (generated from sen0401_slides_lineage_v0_161_0.ttl)

The Verify tasks (TK_SecLinks_Ch10_Verify, TK_SecLinks_Ch11_Verify) have no executor: the builder session runs them through the evidence bridge after the executors report.

| Task | Executor session | Can start |
|---|---|---|
| TK_SecLinks_Ch10_Research | SEN0401-I14-research-ch10 | yes |
| TK_SecLinks_Ch11_Research | SEN0401-I14-research-ch11 | yes |
| TK_SecLinks_PageData | SEN0401-I14-pagedata | no, after TK_SecLinks_Ch10_Research |
| TK_SecLinks_Ch10_Page | SEN0401-I14-page-ch10 | no, after TK_SecLinks_Ch10_Research, TK_SecLinks_PageData |
| TK_SecLinks_Ch11_Page | SEN0401-I14-page-ch11 | no, after TK_SecLinks_Ch11_Research, TK_SecLinks_PageData |
