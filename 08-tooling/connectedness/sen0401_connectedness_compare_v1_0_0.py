#!/usr/bin/env python3
"""sen0401_connectedness_compare v1_0_0 - compares two verify results (before, after) of one chapter: the gate verdicts must be identical, HermiT must be consistent, and the after-file must have no class standing alone and no island. Exit 0 only then.
Usage: sen0401_connectedness_compare_v1_0_0.py BEFORE.json AFTER.json"""
import json, sys
b, a = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
ok = True
diff = {k: (b["gates"].get(k), a["gates"].get(k)) for k in set(b["gates"]) | set(a["gates"]) if b["gates"].get(k) != a["gates"].get(k)}
print("chapter", a["key"], "| before: alone %d islands %d | after: alone %d islands %d (hasOwner left out: alone %d islands %d)" % (b["alone"], b["islands"], a["alone"], a["islands"], a["alone_without_hasOwner"], a["islands_without_hasOwner"]))
print("gate verdicts changed:", diff or "none", "| hermit:", b["hermit"], "->", a["hermit"])
ok = not diff and a["hermit"] == "consistent" and a["alone"] == 0 and a["islands"] == 0
print("RESULT:", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
