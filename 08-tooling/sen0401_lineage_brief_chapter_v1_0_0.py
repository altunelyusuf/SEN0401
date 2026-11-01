#!/usr/bin/env python3
"""sen0401_lineage_brief_chapter v1_0_0 - joins the task briefs written by sen0401_lineage_brief_exam_v1_7_0.py into ONE brief per executor session (one per chapter; one for the code gate and deck checks): a preface, the first task brief whole, and of every later task brief only the sections that are not repeated. Usage: brief_chapter TASKDIR OUTDIR"""
__version__ = "1.0.0"
import os, re, sys
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
SES = {"deck0%d" % c: (["TK_Ch0%d_DeckCode_Build" % c] + (["TK_Repair_Ch06_DeckLayout_Build"] if c == 6 else []) + ["TK_Ch0%d_DeckTeach_Build" % c, "TK_Ch0%d_PageCode_Build" % c] + (["TK_Repair_Ch06_Lecture_Build"] if c == 6 else []) + ["TK_Ch0%d_PageMeasure_Build" % c]) for c in range(1, 7)}
SES["codegate"] = ["TK_Code_Gate_Build", "TK_Deck_Checks_Build"]
for k, tasks in SES.items():
    name = "SEN0401-I52-" + k; seen = set(); parts = []
    for n, tid in enumerate(tasks):
        txt = open(os.path.join(src, "BRIEF_%s.md" % tid), encoding="utf-8").read()
        secs = re.split(r"\n(?=## )", txt); head = secs[0]; keep = []
        for sct in secs[1:]:
            h = sct.split("\n", 1)[0]
            if h in seen and n > 0: continue
            seen.add(h); keep.append(sct)
        if n == 0: parts.append(head + "\n" + "\n".join(keep))
        else: parts.append("\n\n---\n\n# NEXT TASK of the same session: %s\n\n" % tid + "\n".join(keep))
    pre = ("# Brief for the executor session %s (several tasks, one after another)\n\nThis session does the tasks below IN THIS ORDER, one at a time: %s. Where the rules say 'the one task below', read: the one task you are on. Commit each verified step at once (under the git lock). Work begun is recorded by the lineage agent for each task at the instant the coordinator gives; report to the coordinator after each task with the commit SHAs and the verbatim output of each check.\n\n" % (name, ", ".join(tasks)))
    open(os.path.join(out, "BRIEF_%s.md" % name), "w", encoding="utf-8").write(pre + "\n".join(parts) + "\n"); print(name, len(tasks), "tasks")
