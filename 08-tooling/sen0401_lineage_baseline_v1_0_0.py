#!/usr/bin/env python3
"""sen0401_lineage_baseline v1_0_0 - the lineage agent's own measurement of the state of chapters 1 to 14 against the current teaching-material standard (Iteration 24 planning,
2026-10-25). It RUNS the committed checks as they stand, per chapter, with a time limit each, and writes every raw output once to a log file in the folder given; it edits nothing.
Measures (all non-browser): deck standard check v1_1_0 (D1-D12), deck overlap check v1_0_0, chapter-code manifest (exists; deck control check manifest:NN; first-line error name scan),
page charset check v1_0_0 on the newest page, the page declares standard 9.52 and a chapter-code tab, Stage 4 gate runner v1_1_0, chapter check v1_3_0 Research/ChNN (venv314), story check v1_0_0.
NOT measured here (browser, serial under the lock): the page test 9.37.0 and the story layout at three viewports - they are the controller's runs after a page is rebuilt.
Usage: sen0401_lineage_baseline_v1_0_0.py OUTDIR [NN ...]        Prints one line per chapter and writes OUTDIR/baseline_summary.json (only when OUTDIR/baseline_summary.json does not exist)."""
__version__ = "1.0.0"
import glob, json, os, re, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
OUT = sys.argv[1]; CH = sys.argv[2:] or ["%02d" % i for i in range(1, 15)]
VK = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
newest = lambda pat: (sorted(glob.glob(os.path.join(R, pat)), key=VK) or [None])[-1]
V314 = "/home/claude/venv314/bin/python"
ERR = re.compile(r"^(\w*Error|Traceback|Stopped after)")
def run(cmd, log, to=600, cwd=T):
    p = os.path.join(OUT, log)
    assert not os.path.exists(p), "log exists: " + p
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=to, cwd=cwd); o = (r.stdout or "") + (r.stderr or ""); rc = r.returncode
    except subprocess.TimeoutExpired as e:
        o = "TIMEOUT after %d s\n%s" % (to, (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")); rc = 124
    open(p, "w").write("$ %s\nexit %d\n%s" % (" ".join(cmd), rc, o)); return rc, o
res = {}
for nn in CH:
    d = {}; deck = newest("03-materials/ch%s/*.pptx" % nn); page = newest("03-materials/ch%s/page/sen0401_ch%s_page_v*.html" % (nn, nn))
    d["deck"] = os.path.relpath(deck, R) if deck else None; d["page"] = os.path.relpath(page, R) if page else None
    rc, o = run(["python3", "-B", "sen0401_deck_standard_check_v1_1_0.py", nn], "ch%s_deck_standard.log" % nn)
    m = re.search(r"SUMMARY PASS=(\d+) FAIL=(\d+) NOT_MEASURED=(\d+)(?: \| failing: ([\w,]+))?", o); d["deck_std"] = {"exit": rc, "pass": int(m.group(1)) if m else None, "fail": int(m.group(2)) if m else None, "not_measured": int(m.group(3)) if m else None, "failing": (m.group(4) or "") if m else None}
    f = re.search(r"FACTS (.*)", o); d["deck_facts"] = f.group(1) if f else None
    rc, o = run(["python3", "-B", "deck_overlap_check_v1_0_0.py", deck], "ch%s_deck_overlap.log" % nn)
    d["deck_overlap"] = {"exit": rc, "result": "CLEAN" if rc == 0 else "FINDINGS", "findings": len(re.findall(r"^(OVERLAP|SPILL|EDGE)", o, re.M))}
    mf = newest("03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (nn, nn)); d["manifest"] = os.path.relpath(mf, R) if mf else None
    if mf:
        rc, o = run(["python3", "-B", "sen0401_deck_control_check_v1_1_0.py", "manifest:" + nn], "ch%s_manifest_control.log" % nn)
        d["manifest_control_exit"] = rc
        J = json.load(open(mf)); bad = []
        for e in J["examples"]:
            for s in (e.get("show") or []):
                first = str(s.get("expected", "")).strip().splitlines()[:1]
                if first and ERR.match(first[0]): bad.append((e.get("order"), e.get("name")))
            ex = e.get("expected")
            if isinstance(ex, str) and ERR.match(ex.strip().splitlines()[0] if ex.strip() else ""): bad.append((e.get("order"), e.get("name")))
        d["manifest_examples"] = len(J["examples"]); d["manifest_error_first"] = bad
    if page:
        rc, o = run(["python3", "-B", "sen0401_page_charset_check_v1_0_0.py", page], "ch%s_page_charset.log" % nn)
        txt = open(page, encoding="utf-8", errors="replace").read()
        d["page_charset_exit"] = rc; d["page_declares_9_52"] = 'name="page-standard" content="9.52"' in txt; d["page_has_chaptercode_tab"] = 'data-pane="chaptercode"' in txt
        tm = re.search(r"page-template[^>]*content=\"([^\"]+)\"", txt); d["page_template_meta"] = tm.group(1) if tm else None
    pa = newest("03-materials/ch%s/page/sen0401_ch%s_page_abox_v*.ttl" % (nn, nn)); d["page_abox"] = os.path.relpath(pa, R) if pa else None
    rc, o = run(["python3", "-B", "sen0401_stage4_gates_v1_1_0.py", nn], "ch%s_stage4_gates.log" % nn, 900)
    ov = re.findall(r"OVERALL: (\w+)", o); d["stage4_gates"] = {"exit": rc, "overall": ov[-1] if ov else None, "fails": re.findall(r"^\[(?:FAIL|CANNOT_RUN)\s*\] (\S+)", o, re.M)}
    rc, o = run([V314, "-B", "sen0401_lineage_chapter_check_v1_3_0.py", "Research/Ch" + nn], "ch%s_chapter_check_research.log" % nn, 900)
    d["chapter_check_research"] = {"exit": rc, "crash": "Traceback" in o, "last": o.strip().splitlines()[-1][:160] if o.strip() else ""}
    rc, o = run(["python3", "-B", "sen0401_story_check_v1_0_0.py", nn], "ch%s_story_check.log" % nn, 300)
    d["story_check"] = {"exit": rc, "last": o.strip().splitlines()[-1][:200] if o.strip() else ""}
    res[nn] = d
    print(nn, "deck PASS=%s FAIL=%s NM=%s [%s] overlap=%s(%s) manifest=%s charset=%s tab=%s s4=%s research=%s%s story_exit=%s" % (
        d["deck_std"]["pass"], d["deck_std"]["fail"], d["deck_std"]["not_measured"], d["deck_std"]["failing"], d["deck_overlap"]["result"], d["deck_overlap"]["findings"],
        d["manifest"] and "yes(%d, errfirst=%s)" % (d["manifest_examples"], d["manifest_error_first"]) or "NO", d.get("page_charset_exit"), d.get("page_has_chaptercode_tab"),
        d["stage4_gates"]["overall"], d["chapter_check_research"]["exit"], " CRASH" if d["chapter_check_research"]["crash"] else "", d["story_check"]["exit"]), flush=True)
sp = os.path.join(OUT, "baseline_summary.json")
assert not os.path.exists(sp); json.dump(res, open(sp, "w"), indent=1)
