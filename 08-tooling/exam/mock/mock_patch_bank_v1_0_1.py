#!/usr/bin/env python3
"""Patch v1.0.1: builds mock_bank_all_v1_0_1.json from mock_bank_all_v1_0_0.json by replacing only the two fill units f4_4 and f6_1 with the versions
in the new chapter part files (ch4 v1.0.1, ch6 v1.0.1), after verifying that every other field of those units and every other unit is unchanged.
Prints ids/counts/hashes only. Usage: mock_patch_bank_v1_0_1.py"""
import json, hashlib, re
M = "/home/claude/CME/exams/SEN0401/08-tooling/exam/mock"; P = M + "/parts"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
old = json.load(open(M + "/mock_bank_all_v1_0_0.json"))
new = json.loads(json.dumps(old)); new["version"] = "1.0.1"
for n, uid in ((4, "f4_4"), (6, "f6_1")):
    pf = "%s/mock_bank_ch%d_v1_0_1.json" % (P, n)
    src = [i for i in json.load(open(pf))["items"] if i["id"] == uid][0]
    src["tip"] = re.sub(r"^\s*Tip:\s*", "", src["tip"], flags=re.I)
    k = [j for j, i in enumerate(new["items"]) if i["id"] == uid][0]
    o = old["items"][k]
    assert {a: b for a, b in o.items() if a != "blanks"} == {a: b for a, b in src.items() if a != "blanks"}, uid + " other fields differ"
    assert [b["answer"] for b in o["blanks"]] == [b["answer"] for b in src["blanks"]], uid + " answers differ"
    assert all(a["sentence"] != b["sentence"] for a, b in zip(o["blanks"], src["blanks"]))
    new["items"][k] = src
    new["parts_sha256"][str(n)] = sha(pf)
    print(uid, "replaced at position", k, "part sha256", sha(pf))
diff = [i["id"] for i, j in zip(old["items"], new["items"]) if i != j]
assert diff == ["f4_4", "f6_1"] and len(old["items"]) == len(new["items"])
json.dump(new, open(M + "/mock_bank_all_v1_0_1.json", "w"), ensure_ascii=False, indent=0)
print("units changed:", diff, "of", len(new["items"]), "bank sha256", sha(M + "/mock_bank_all_v1_0_1.json"))
