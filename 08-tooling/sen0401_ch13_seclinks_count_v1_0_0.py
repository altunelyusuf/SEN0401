import json, sys, collections
d = json.load(open(sys.argv[1]))
ns = {n["id"]: n for n in d["nodes"]}
def sec(i):
    n = ns[i]
    while n and n["level"] > 2: n = ns.get(n["parent"])
    return n["id"] if n and n["level"] == 2 else None
secs = sorted(n["id"] for n in d["nodes"] if n["level"] == 2)
types = collections.Counter(r["type"] for r in d["relations"])
cross = [r for r in d["relations"] if r["type"] != "is a kind of" and sec(r["source"]) and sec(r["target"]) and sec(r["source"]) != sec(r["target"])]
cnt = {s: 0 for s in secs}
for r in cross: cnt[sec(r["source"])] += 1; cnt[sec(r["target"])] += 1
print("page data:", sys.argv[1]); print("research_file:", d["research_file"], "| python:", d["python"])
print("relations in all:", len(d["relations"]), dict(types))
print("sections (level 2):", len(secs))
print("relations between two different sections:", len(cross), "| types:", dict(collections.Counter(r["type"] for r in cross)))
print("distinct section pairs related:", len({frozenset((sec(r["source"]), sec(r["target"]))) for r in cross}))
print("sections with no relation to another section:", [s for s, c in cnt.items() if c == 0], "(count %d)" % sum(1 for c in cnt.values() if c == 0))
print("per section:", dict(sorted(cnt.items())))
print("min per section:", min(cnt.values()))
