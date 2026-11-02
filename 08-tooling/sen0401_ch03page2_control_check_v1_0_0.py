#!/usr/bin/env python3
"""Control of the Ch03 page repair 2 report (new file v1.0.0). Modes: cause | page. Prints what it finds; exit 0 only if the element holds.
cause: my own count of the diagnostic runner files (by page version, plain or busy, with a [FAIL] line or not), the 2063 ms task searched in every
       log, the DOM probe numbers; agrees with the report on the budget lines: 10 runs of v9_75_0 (2 with a budget [FAIL]), 1 of v9_73_0 (0). NOT in the report: the endless-program feature failed in one v9_75_0 busy run and in the one v9_73_0 busy run (printed as other-feature), no 2063 ms task, 98 editors on both.
page:  element (3) of the criterion: a new page v9_76_0 exists and the page test passed on it five times; exit 1 if there is no such page (the executor built none)."""
import glob, os, re, sys, subprocess
R = "/home/claude/sen0401/"; L = R + "08-tooling/ch03-page/page_9_76_0_logs/"
mode = sys.argv[1]
if mode == "page":
    pg = glob.glob(R + "03-materials/ch03/page/sen0401_ch03_page_v9_76_0*.html"); print("pages v9_76_0 found: %d" % len(pg)); logs = glob.glob(L + "*5x*") + glob.glob(L + "*five*"); print("five-in-a-row logs found: %d" % len(logs))
    print("RESULT %s" % ("PASS" if pg and logs else "FAIL: no new page, so no proof step ran (NOT_RUN, not a pass)")); sys.exit(0 if pg and logs else 1)
runs = {}
for f in sorted(glob.glob(L + "diag*/*_runner.txt")):
    m = re.search(r"_(v9_\d+_0)_(plain|busy)_runner", f); t = open(f, errors="replace").read(); runs.setdefault((m.group(1), m.group(2)), []).append((os.path.basename(f), len(re.findall(r"\[FAIL\] main-thread budget", t)), bool(re.search(r"\b2063 ms|\b2063\.\d* ms|duration 2063\b", t)), len(re.findall(r"\[FAIL\]", t)) - len(re.findall(r"\[FAIL\] main-thread budget", t))))
tot = {}
for (v, k), lst in sorted(runs.items()):
    print("%s %s: %d runs, %d with a main-thread budget [FAIL] (%s); other-feature [FAIL] in %d" % (v, k, len(lst), sum(1 for x in lst if x[1]), ", ".join(x[0].split("_")[0] for x in lst if x[1]) or "none", sum(1 for x in lst if x[3]))); a = tot.setdefault(v, [0, 0, 0]); a[0] += len(lst); a[1] += sum(1 for x in lst if x[1]); a[2] += sum(1 for x in lst if x[3])
print("totals", tot); any2063 = any(x[2] for l in runs.values() for x in l) 
print("2063 ms found in any diagnostic log: %s" % any2063); d = open(L + "diag3/domprobe.txt").read(); ed = re.findall(r'"editors": (\d+)', d); print("DOM probe editors:", ed, "elements:", re.findall(r'"elements": (\d+)', d))
okk = tot.get("v9_75_0") == [10, 2, 1] and tot.get("v9_73_0") == [1, 0, 1] and not any2063 and ed == ["98", "98"]; print("RESULT %s" % ("PASS" if okk else "FAIL (the numbers differ from the report)")); sys.exit(0 if okk else 1)
