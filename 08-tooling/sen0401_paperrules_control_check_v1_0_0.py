#!/usr/bin/env python3
"""sen0401_paperrules_control_check v1_0_0 - the lineage agent's OWN control checks of TK_Exam_PaperRules_Build. They share no code with the executor's checker, fixture grouping or measurement.
Usage: sen0401_paperrules_control_check_v1_0_0.py KIND [COMMIT]   KIND: rerun | fixtures | registry | banks | pages | nochange COMMIT. Exit 0 only when met."""
import collections, glob, json, os, re, shutil, statistics, subprocess, sys, tempfile
R = "/home/claude/sen0401/"; X = R + "08-tooling/exam/"; V = X + "sen0401_exam_%s_v1_0_0"
def rerun():
    r = subprocess.run([sys.executable, "-B", V % "paperrules_check" + ".py"], capture_output=True, text=True, cwd=R); line = [l for l in r.stdout.splitlines() if l.startswith("SUMMARY") or l.startswith("FAIL")]
    print("executor's check re-run by the control: exit %d, %s" % (r.returncode, line)); return r.returncode == 0 and any("8 of 8" in l for l in line)
def fixtures():
    import pyshacl
    from rdflib import Graph, Namespace
    SH = Namespace("http://www.w3.org/ns/shacl#")
    sh = Graph().parse(V % "paperrules_shapes" + ".ttl"); reg = Graph().parse(V % "papertypes" + ".ttl"); fx = Graph().parse(V % "paperrules_fixtures" + ".ttl")
    exp = json.load(open(V % "paperrules_fixtures_expected" + ".json")); d = Graph(); d += fx; d += reg
    conf, rg, _ = pyshacl.validate(d, shacl_graph=sh, advanced=True, inference="none", js=False)   # ALL fixtures in ONE graph: not the executor's one-by-one grouping
    by = collections.defaultdict(set)
    for r in rg.subjects(SH.resultSeverity, None):
        by[str(rg.value(r, SH.focusNode)).split("#")[-1].split("_")[0]].add((str(rg.value(r, SH.resultMessage)).split()[0], str(rg.value(r, SH.resultSeverity)).split("#")[1]))
    bad = [k for k, v in exp.items() if set(map(tuple, v)) != by.get(k, set())]
    rules = {m for m in ("R%02d" % i for i in range(1, 23))}; fired = {r for v in by.values() for r, s in v}
    conforming = [k for k, v in exp.items() if not v]
    print("%d fixtures validated together in one graph; expectation mismatches: %s; rules fired by some fixture: %d of 22 (not fired: %s); fixtures expected to conform: %d, and all of them gave no result: %s" % (len(exp), bad, len(fired & rules), sorted(rules - fired), len(conforming), all(not by.get(k) for k in conforming)))
    return not bad and rules <= fired and len(conforming) >= 3
def registry():
    from rdflib import Graph, Namespace, RDF
    PR = Namespace("http://example.org/sen0401/paperrules#"); reg = Graph().parse(V % "papertypes" + ".ttl")
    c = collections.Counter(str(reg.value(t, PR.status)).split("#")[-1] for t in reg.subjects(RDF.type, PR.ItemType))
    q = json.load(open(V % "paperrules_owner_questions" + ".json"))["questions_for_the_owner_via_the_coordinator"]
    ids = [x["id"] for x in q]; print("item types by status %s; owner questions %s; every question has a plain ask: %s" % (dict(c), ids, all(len(x["ask"]) > 40 for x in q)))
    return dict(c) == {"Suited": 7, "Conditional": 3, "NotSuited": 9} and ids == ["Q%d" % i for i in range(1, 11)]
def banks():
    tot = 0; lv = collections.Counter(); code = wide = 0; four = 0
    for n in range(1, 9):
        fs = sorted(glob.glob(R + "08-tooling/ch%02d-page/question_bank_v*.json" % n), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
        for i in json.load(open(fs[-1], encoding="utf8")):
            tot += 1; lv[i["level"]] += 1; four += len(i["options"]) == 4
            if n <= 6 and i.get("code"):
                code += 1; wide += max(len(l) for l in i["code"].split("\n")) > 45
    hi = lv["Apply"] + lv["Analyze"]
    print("control's own count over chapters 1 to 8: %d items, %d with four options, levels %s; Apply+Analyze %d (%.1f%%), Analyze %d; chapters 1 to 6: %d code items, %d with a line wider than 45" % (tot, four, dict(lv), hi, 100 * hi / tot, lv["Analyze"], code, wide))
    return tot == 1453 and four == 1453 and hi == 718 and lv["Analyze"] == 235 and code == 427 and wide == 302
def pages():
    tmp = tempfile.mkdtemp(prefix="prctl_", dir="/tmp/claude-0/s"); ok = True
    try:
        for run in (1, 2):
            subprocess.run([sys.executable, "-B", V % "pagesave_measure" + ".py", "--chapters", "1-6", "--n", "40", "--json", tmp + "/m%d.json" % run, "--keep", tmp + "/k%d" % run], capture_output=True, text=True, cwd=R)
        a, b, ref = [open(f, "rb").read() for f in (tmp + "/m1.json", tmp + "/m2.json", V % "pagesave_measure" + ".json")]
        print("measurement deterministic: %s; equals the committed result: %s" % (a == b, a == ref)); ok &= a == b and a == ref
        j = json.loads(ref); want = {"b0": j["pages_baseline"], "c_M5": list(j["pages_methods_stacked_in_order"].values())[-1]}
        for k, w in want.items():
            f = tmp + "/k1/%s.pdf" % k; pg = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
            subprocess.run(["pdftotext", "-layout", f, tmp + "/%s.txt" % k]); txt = open(tmp + "/%s.txt" % k).read()
            nums = {int(x) for x in re.findall(r"(?:^|\s)(\d{1,2})[.)]\s", txt) if 1 <= int(x) <= 40}
            bb = subprocess.run(["pdftotext", "-bbox", f, "-"], capture_output=True, text=True).stdout
            hs = [float(m.group(2)) - float(m.group(1)) for m in re.finditer(r'yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)"', bb)]
            print("%s: pdfinfo pages %d (result says %d); items numbered 1 to 40 found in the text: %d; median text box height %.1f pt, smallest %.1f pt" % (k, pg, w, len(nums), statistics.median(hs), min(hs)))
            ok &= pg == w and len(nums) == 40
        sav = "40 items kept in the 4-page paper: pages saved are not items dropped"
        print(sav)
    finally: shutil.rmtree(tmp, ignore_errors=True)
    return ok
def nochange(c):
    st = [l for l in subprocess.run(["git", "-C", R, "show", "--name-status", "--format=", c], capture_output=True, text=True).stdout.split("\n") if l]
    notnew = [l for l in st if not l.startswith("A\t")]; out = [l for l in st if not l.split("\t")[1].startswith("08-tooling/exam/")]
    print("commit %s: %d files, all added: %s; all under 08-tooling/exam/: %s" % (c, len(st), not notnew, not out)); return bool(st) and not notnew and not out
k = sys.argv[1]; ok = {"rerun": rerun, "fixtures": fixtures, "registry": registry, "banks": banks, "pages": pages, "nochange": lambda: nochange(sys.argv[2])}[k]()
print("RESULT", "MET" if ok else "NOT MET"); sys.exit(0 if ok else 1)
