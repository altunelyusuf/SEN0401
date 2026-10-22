# Rebuild of chapters 1, 8, 12 and 14 on template 9.51.1 (task TK_PageGates_Regression, scratch, not shipped)

Scratch copy of the working tree (no .git) in the session scratchpad; nothing below touches a committed file.
Page data builder: sen0401_page_data_v2_22_0.py (verified: with PAGE_VER=9_80_0 it reproduces the committed page_data of each shipped page, 01 9.70.0, 08 9.77.0, 12 9.77.0, 14 9.77.0, with only _version different).
    PAGE_VER=9_80_0 /home/claude/venv314/bin/python -B 08-tooling/sen0401_page_data_v2_22_0.py NN /home/claude/venv314/bin/python
Page builder v4_14_0, template 9.51.1 passed with its documented environment override PAGE_TEMPLATE (the builder default is 9.44.0; the override is the stated way):
    PAGE_VER=9_80_0 PAGE_TEMPLATE=course_page_template_v9_51_1.html /home/claude/venv314/bin/python -B 08-tooling/sen0401_page_build_v4_14_0.py NN
Control: the same builder on template 9.51.0 for chapter 14 (PAGE_VER=9_77_0) gives the shipped page byte for byte except the embedded mission block, which the builder reads from the newest register in 07-lineage (the register moved since).
Scratch page: 03-materials/chNN/page/sen0401_chNN_page_v9_80_0.html (page test run from the scratch copy's 08-tooling, same test files as the repository).
