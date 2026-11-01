#!/usr/bin/env python3
"""sen0401_lineage_note_due v1_0_0 - appends to ex:CR3_MidtermQuality the owner's two statements of 2026-11-01 12:17 and 12:19 (the date 15.11.2026 is a DUE date for Chapters 7-8 of SEN0401, not a start date; the remaining content starts the moment the midterm files are finished) and the plan with agent hours, as a comment (append, nothing edited)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
txt = ("Owner, 2026-11-01 12:17: 'I will continue with Chapters 7-8 for SEN0401 and Chapters 9-10 for SEN0414 after the Midterm week on 15.11.2026.' CORRECTED by the owner at 12:19: 'No, you misunderstood. All the remaining content should start as soon as we finish the Midterm files including the exam, slides and interactive pages. The given date is a due, not a wait date.' So 15.11.2026 is the DUE date of SEN0401 Chapters 7-8 (and the remaining content); the order is: (1) the midterm files first (exam, slides, pages of chapters 1 to 6 to the Friday standard), (2) the moment they are finished Chapters 7-8 start (one lineage at a time), due before 15.11.2026. PLAN (agent hours, G120 estimates): exams in progress 8 (reader 3, paper 5); foundations 21 (deck checks 4, code gate 4, code template 6, panels template 7; critical path 17); chapters: 6 = 24.5, 5 = 21.5, 1 = 17, 4 = 15.5, 3 = 15, 2 = 13.5, total 107.0; midterm quality total 128; Chapters 7-8 about 32 (an estimate: they are not yet measured; the as-is fit-gap and their stories follow when the midterm files are finished). Recommended chapter order (gap size and exam value): 6, 5, 1, 4, 3, 2.")
c = '\nex:CR3_MidtermQuality rdfs:comment %s@en .\n' % C.lit(txt)
print(os.path.basename(M.write_new(src, X.set_status(t + c, "LS_InProgress"), nxt, cur, "Owner's due date 15.11.2026 (a due, not a wait date) and the plan with agent hours appended to the change request of the midterm scope")))
