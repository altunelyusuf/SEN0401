#!/usr/bin/env python3
"""sen0401_exam_nocopy_control_check v1_0_0 - the lineage agent's OWN control of the engine v1.1.0 (task TK_Exam_NoCopy_Build). Own pairs and an own ground truth (difflib ratio, not the executor's shingles), the engine's command line, a static read, and the byte identity of the v1.0.0 files. Usage: control.py"""
import difflib, glob, json, os, random, re, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); sys.path.insert(0, HERE)
import sen0401_exam_similarity_v1_1_0 as S
fails = []
def rep(n, ok, d=""): print("%s  %s  %s" % ("PASS" if ok else "FAIL", n, d)); (None if ok else fails.append(n))
pages = S.page_items((1, 2, 3, 4, 5, 6)); banks = [p for p in pages if p["source"] == "bank"]
rnd = random.Random(20261030)
def raw(p):
    return json.load(open(os.path.join(os.path.dirname(TOOL), p["file"]), encoding="utf8"))[p["index"]]
def own_sim(a, b):   # own measure: character-level ratio of the normalised stems
    n = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()); return difflib.SequenceMatcher(None, n(a), n(b)).ratio()
sample = rnd.sample([p for p in banks if len(p["p"]["w"]) >= 12 and len(p["p"]["dist"]) >= 3], 60)
cnt = {"copy": [0, 0], "shuffled": [0, 0], "oneword": [0, 0], "different": [0, 0]}
for p in sample:
    r = raw(p); st = (r["q"] + "\n" + r["code"]) if r.get("code") else r["q"]; opts = list(r["options"])
    cnt["copy"][1] += 1; cnt["copy"][0] += bool(S.find_matches(S.prepare(st, opts), pages))
    o2 = opts[:]; rnd.shuffle(o2); cnt["shuffled"][1] += 1; cnt["shuffled"][0] += bool(S.find_matches(S.prepare(st.upper(), o2), pages))
    w = st.split(); k = len(w) // 2; w[k] = "certain"; cnt["oneword"][1] += 1; cnt["oneword"][0] += bool(S.find_matches(S.prepare(" ".join(w), opts), pages))
    same = [q for q in banks if q["chapter"] == p["chapter"] and q["ref"] != p["ref"]]
    other = [q for q in same if own_sim(raw(q)["q"], r["q"]) < 0.5 and len(set(map(S.squash, raw(q)["options"])) & set(map(S.squash, opts))) == 0]
    if other:
        q = rnd.choice(other); rq = raw(q)
        # the candidate is the sample item's sibling written as a NEW item: use the different bank item's idea with its stem reworded by the control (a different text); it must not be flagged against p itself
        cand = S.prepare("Consider this situation. " + rq["q"].replace("?", "").lower() + " Which of these holds in your own words", ["our rewording: " + o for o in rq["options"]])
        hit = [m for m in S.find_matches(cand, pages) if m[0] == p["ref"]]
        cnt["different"][1] += 1; cnt["different"][0] += (not hit)
for k, (a, b) in cnt.items(): print("   %-10s %d of %d" % (k, a, b))
rep("A1 copies of real page items are all found", cnt["copy"][0] == cnt["copy"][1], "%d of %d" % tuple(cnt["copy"]))
rep("A2 shuffled options and changed case are all found", cnt["shuffled"][0] == cnt["shuffled"][1], "%d of %d" % tuple(cnt["shuffled"]))
rep("A3 one word replaced in the middle of the stem is found in at least 90 percent", cnt["oneword"][0] >= 0.9 * cnt["oneword"][1], "%d of %d" % tuple(cnt["oneword"]))
rep("A4 a different item on the same concept is not taken for the sibling it is compared with", cnt["different"][0] == cnt["different"][1], "%d of %d" % tuple(cnt["different"]))
# B command line
ENGINE = os.path.join(HERE, "sen0401_exam_engine_v1_1_0.py"); AUTH = os.path.join(HERE, "sen0401_exam_engine_fixture_authored_v1_1_1.json")
tmp = tempfile.mkdtemp(prefix="sen0401_nocopy_ctl_")
try:
    a = json.load(open(AUTH, encoding="utf8")); n = 0
    per = {}
    for it in a["items"]:
        if it["type"] == "ChoiceFour" and "options" in it:
            ch = it["chapters"][0]; cands = [p for p in banks if p["chapter"] == ch and not raw(p).get("code")]
            if not cands: continue
            r = cands[per.get(ch, 0) % len(cands)]; per[ch] = per.get(ch, 0) + 1; rr = raw(r)
            it["q"] = rr["q"]; it["options"] = list(rr["options"]); it["answer"] = rr["answer"]; n += 1
    f = os.path.join(tmp, "copies.json"); json.dump(a, open(f, "w", encoding="utf8"))
    od = os.path.join(tmp, "out_copies"); p = subprocess.run([sys.executable, ENGINE, "build", "--items", "24", "--outdir", od, "--authored", f], capture_output=True, text=True)
    rep("B1 a paper whose choice items are all copies of page items is refused (exit 2, EN11, nothing written)", p.returncode == 2 and "EN11" in p.stdout + p.stderr and not (os.path.isdir(od) and os.listdir(od)), "%d items replaced; exit %s; written %s" % (n, p.returncode, os.listdir(od) if os.path.isdir(od) else []))
    od2 = os.path.join(tmp, "out_ok"); p2 = subprocess.run([sys.executable, ENGINE, "build", "--items", "24", "--outdir", od2, "--authored", AUTH], capture_output=True, text=True)
    rep("B2 the authored fixture (different items) builds papers", p2.returncode == 0 and os.path.isdir(od2) and len(os.listdir(od2)) > 0, "exit %s, %d files" % (p2.returncode, len(os.listdir(od2)) if os.path.isdir(od2) else 0))
    if p.returncode not in (0, 2): print(p.stdout[-300:], p.stderr[-300:])
finally: shutil.rmtree(tmp, ignore_errors=True)
# C static: no call that pools a bank into a paper
src = open(ENGINE, encoding="utf8").read(); code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
rep("C1 the engine v1.1.0 has no bank_pool( or compose_matching( call and requires --authored", "bank_pool(" not in code and "compose_matching(" not in code and "--authored" in code)
# D old files byte-identical to their committed content
root = os.path.dirname(TOOL); old = [f for f in glob.glob(os.path.join(HERE, "*_v1_0_0.*")) if "log" not in f]
bad = [os.path.basename(f) for f in old if subprocess.run(["git", "-C", root, "diff", "--quiet", "HEAD", "--", os.path.relpath(f, root)]).returncode]
rep("D1 every v1.0.0 file of 08-tooling/exam equals its committed content (%d files)" % len(old), not bad, ",".join(bad[:5]))
print("OWN CONTROL:", "FAIL " + ",".join(fails) if fails else "PASS"); sys.exit(1 if fails else 0)
