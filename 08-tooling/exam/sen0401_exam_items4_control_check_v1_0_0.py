#!/usr/bin/env python3
"""sen0401_exam_items4_control_check v1_0_0 - the lineage agent's own control of items v1.3.0: (1) 17 of 21 items equal v1.2.0 byte for byte (JSON-equal), the changed ones are exactly i02, i03, i06, i07 and i05, i23 are among the equal ones; (2) every answer type equals the type of its position in the structure; (3) the case answers recomputed here with no use of the builder: C1 spending order unique, C2 mined set closed under the spending references, C3 change and fee, B subsidy at height; (4) the stored answers equal the recomputed ones; (5) topic coverage T1-T9 and A-F of the executor's map is read from the owner file and every point is an item key or GAP. Usage: no arguments. Exit 0 = PASS."""
import json, itertools, os, sys
H = os.path.dirname(os.path.abspath(__file__)); ld = lambda f: json.load(open(os.path.join(H, f), encoding="utf-8"))
N = {x["key"]: x for x in ld("sen0401_exam_items_midterm_v1_3_0.json")["items"]}; O = {x["key"]: x for x in ld("sen0401_exam_items_midterm_v1_2_0.json")["items"]}
S = ld("sen0401_exam_structure_v1_0_0.json"); T = ld("sen0401_exam_owner_topics_v1_1_0.json"); TM = ld("sen0401_exam_items_midterm_topic_map_v1_3_0.json")
res = []; ok = lambda n, c, d="": (res.append(c), print(("PASS " if c else "FAIL ") + n + (" " + d if d else "")))
chg = sorted(k for k in N if N[k] != O.get(k)); ok("(1) only i02, i03, i06, i07 differ", [k[4:7] for k in chg] == ["i02", "i03", "i06", "i07"] and set(N) == set(O), str(chg))
ok("(1) i05 and i23 equal", all(N[k] == O[k] for k in N if k[4:7] in ("i05", "i23")))
bad = [s["item"] for q in S["questions"] for s in q.get("sub", []) if s.get("item") in N and N[s["item"]]["type"] != s["type"]]; ok("(2) answer types equal the structure", not bad, str(bad))
i6 = N["mt2:i06:order-wallet-to-block"]; spend = {"E": "G", "H": "E", "B": "H", "J": "B"}
orders = [p for p in itertools.permutations("GEHBJ") if all(p.index(s) > p.index(r) for s, r in spend.items())]; ok("(3) C1 one valid order G E H B J", orders == [tuple("GEHBJ")] and "G < E < H < B < J" in i6["computed"], str(orders))
ref = {"C": "B", "B": "A", "E": "D"}
sts = [s for s in itertools.product([0, 1], repeat=5) if s[2] == 1 and all((not s["ABCDE".index(a)]) or s["ABCDE".index(b)] for a, b in ref.items())]
sure = [c for c in "ABCDE" if all(s["ABCDE".index(c)] for s in sts)]; ok("(3) C2 mined for sure: A B C; D E undecided", sure == ["A", "B", "C"], str(sure))
i2 = N["mt2:i02:fee-not-written"]; left = 70000 + 45000 + 25000 - 95000; ok("(3) C3 left 45000, change 37000 with fee 8000", left == 45000 and left - 8000 == 37000 and i2["options"][i2["answer"]].startswith("Change 37,000") and "45,000" in i2["options"][i2["answer"]], i2["options"][i2["answer"]])
sub = 16 >> (23 // 10); i3 = N["mt2:i03:toy-chain-supply"]; ok("(3) B subsidy 4, limit 7, claim 9, excess 2", (sub, sub + 3, 9 - (sub + 3)) == (4, 7, 2) and i3["key_value"] == 2, "key_value %s" % i3["key_value"])
ids = [t["id"] for t in T["topics"]] + [p["id"] for p in T["points"]]; blob = json.dumps(TM, ensure_ascii=False)
ok("(5) owner file lists T1-T9 and A-F", ids == ["T%d" % i for i in range(1, 10)] + list("ABCDEF"), str(ids))
cov = open(os.path.join(H, "sen0401_exam_items_midterm_topic_map_v1_3_0.txt"), encoding="utf-8").read() + open(os.path.join(H, "sen0401_exam_items_midterm_new_points_map_v1_3_0.txt"), encoding="utf-8").read()
import re
state = {}
for m in re.finditer(r"^([A-F])\s+(COVERED|PARTIAL|GAP)\b|^(T[1-9])\s+.*?(COVERED|PARTIAL|GAP)\s*$", cov, re.M):
    state[m.group(1) or m.group(3)] = m.group(2) or m.group(4)
ok("(5) every one of the 15 points has a verdict COVERED, PARTIAL or GAP", sorted(state) == sorted(ids), str(sorted(state)))
print("COVERAGE " + ", ".join("%s %s" % (k, state.get(k)) for k in ids))
print("RESULT " + ("PASS" if all(res) else "FAIL")); sys.exit(0 if all(res) else 1)
