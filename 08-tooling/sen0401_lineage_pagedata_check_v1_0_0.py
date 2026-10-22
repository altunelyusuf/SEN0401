#!/usr/bin/env python3
"""sen0401_lineage_pagedata_check v1_0_0 - compares the page-data builder v2_23_0 with v2_22_0 on one chapter, as an exit-code check for the evidence bridge (criteria AC3L_Ch10 and AC3L_Ch11, task TK_SecLinks_PageData):
  cmp:NN   builds the page data of chapter NN with both builders (temporary files page_data_vctl22.json and page_data_vctl23.json in 08-tooling/chNN-page, removed afterwards), then requires:
           every key of the data other than the relations is equal; the relations of v2_22_0 are all still present;
           a chapter whose research states no section link: the relations are identical; chapters 10 and 11 (research with section links): the added relations are all of type 'operates on', join two different sections, and their evidence names the property, its relationship category and the link's sentence;
           and prints the relation counts and the number of sections without a relation to another section.
Usage: sen0401_lineage_pagedata_check_v1_0_0.py cmp:NN"""
__version__ = "1.0.0"
import json, os, subprocess, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(nn, ver, tag):
    env = dict(os.environ, PAGE_VER=tag)
    r = subprocess.run([sys.executable, "-B", os.path.join(REPO, "08-tooling", "sen0401_page_data_v%s.py" % ver), nn, sys.executable], cwd=REPO, capture_output=True, text=True, env=env)
    p = os.path.join(REPO, "08-tooling", "ch%s-page" % nn, "page_data_v%s.json" % tag)
    if r.returncode or not os.path.exists(p):
        print("BUILD FAILED", ver, r.stderr[-400:]); return None
    return p


def main():
    kind, nn = sys.argv[1].split(":"); assert kind == "cmp"
    pa = build(nn, "2_22_0", "ctl22"); pb = build(nn, "2_23_0", "ctl23")
    if not (pa and pb): return 1
    try:
        a = json.load(open(pa)); b = json.load(open(pb))
    finally:
        for p in (pa, pb):
            for q in (p, p.replace("page_data_v", "extra_resolved_v").replace(".json", ".html")):
                if os.path.exists(q): os.remove(q)
    ok = True
    diff = [k for k in set(a) | set(b) if k not in ("relations", "_version") and a.get(k) != b.get(k)]
    print("keys other than relations that differ:", diff); ok &= not diff
    ra, rb = a["relations"], b["relations"]; key = lambda r: json.dumps(r, sort_keys=True)
    sa = {key(r) for r in ra}; sb = {key(r) for r in rb}
    lost = sa - sb; added = [r for r in rb if key(r) not in sa]
    print("relations v2_22_0: %d, v2_23_0: %d, lost %d, added %d" % (len(ra), len(rb), len(lost), len(added))); ok &= not lost
    nodes = {n["id"]: n for n in b["nodes"]}; sec = {i: (i if n["level"] == 2 else n["parent"] if n["level"] == 3 else None) for i, n in nodes.items()}
    if nn in ("10", "11"):
        bad = [r for r in added if r["type"] != "operates on" or not (sec.get(r["source"]) and sec.get(r["target"]) and sec[r["source"]] != sec[r["target"]]) or "relationship of category" not in r["evidence"] or "carries no sentence" in r["evidence"]]
        print("added relations not 'operates on' between two sections with property, category and sentence in the evidence:", len(bad)); ok &= not bad and len(added) > 0
        secs = [i for i, n in nodes.items() if n["level"] == 2]
        linked = {sec[r["source"]] for r in rb if sec.get(r["source"]) and sec.get(r["target"]) and sec[r["source"]] != sec[r["target"]]} | {sec[r["target"]] for r in rb if sec.get(r["source"]) and sec.get(r["target"]) and sec[r["source"]] != sec[r["target"]]}
        print("sections: %d, with a relation to another section: %d" % (len(secs), len(linked & set(secs)))); ok &= len(linked & set(secs)) == len(secs)
    else:
        print("a chapter without section links: relations identical:", not added and not lost); ok &= not added
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
