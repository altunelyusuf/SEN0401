#!/usr/bin/env python3
"""sen0401_arccheck_control_check v1_1_0 - the lineage agent's OWN checks of the deck arc check v1_3_0 (criterion AC9_ArcLookup), independent of the executor's logs. (v1_0_0 checked v1_2_0 and stays.)
Usage: sen0401_arccheck_control_check_v1_1_0.py MODE   MODE = sha | diff | compare | lookup | fixture
sha: v1_2_0 SHA-256 equals 73617904...9642 and git shows its one commit and no change
diff: the diff v1_2_0 to v1_3_0 changes only the version line, comments, the deck lookup, the length-mismatch refusal and the analogy-slide guard
compare: on every chapter with an arc plan: v1_2_0 given the SAME deck (SEN0401_DECK = the newest deck v1_3_0 would pick, or none when 03-materials has none) versus v1_3_0: v1_3_0 must lose NO refusal (v1_2_0 crashes count as nothing lost); added refusals are listed and must be 'plan/deck mismatch' lines only
lookup: for every chapter the deck v1_3_0 reports (its slide count) equals the slide count of the newest .pptx of 03-materials/chNN (read from the file), so the stale 08-tooling deck is no longer used; chapters 3 and 5 give no crash
fixture: the chapter 4 plan run against the chapter 9 deck (SEN0401_DECK) is refused with exit 1 and a message naming both lengths, and v1_2_0 on the same pair does not give such a message; the real chapter 4 deck passes"""
import difflib, glob, hashlib, os, re, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(T); V1 = T + "/sen0401_deck_arc_check_v1_2_0.py"; V2 = T + "/sen0401_deck_arc_check_v1_3_0.py"
mode = sys.argv[1]; fail = []
def run(script, ch, env=None):
    r = subprocess.run([sys.executable, "-B", script, ch], capture_output=True, text=True, cwd=T, env=dict(os.environ, **(env or {}))); return r.returncode, (r.stdout + r.stderr).strip().splitlines()
refusals = lambda L: [l.strip() for l in L if l.strip().startswith("REFUSED")]
def newest_delivered(ch):
    fs = glob.glob("%s/03-materials/ch%s/*_v*_*_*.pptx" % (REPO, ch)); return max(fs, key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]) if fs else None
def nslides(p):
    import zipfile; return len([n for n in zipfile.ZipFile(p).namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)])
chapters = ["%02d" % n for n in range(1, 15) if glob.glob("%s/ch%02d-deck/deck_plan_v*.json" % (T, n))]
if mode == "sha":
    h = hashlib.sha256(open(V1, "rb").read()).hexdigest(); print("v1_2_0 SHA-256", h)
    if not (h.startswith("73617904") and h.endswith("9642")): fail.append("sha")
    d = subprocess.run(["git", "log", "--oneline", "--", "08-tooling/sen0401_deck_arc_check_v1_2_0.py"], cwd=REPO, capture_output=True, text=True).stdout.strip().splitlines(); st = subprocess.run(["git", "status", "--short", "08-tooling/sen0401_deck_arc_check_v1_2_0.py"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    print("commits touching v1_2_0:", d, "status:", repr(st)); fail += ["v1_2_0 changed"] if (len(d) != 1 or st) else []
elif mode == "diff":
    a = open(V1).read().splitlines(); b = open(V2).read().splitlines(); ch = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    ok = lambda l: any(k in l for k in ("__version__", "# 1.3.0", "#   chNN-deck only", "#   Every other rule", "newest_of", "delivered", "plan/deck mismatch", "len(S) != len(T)", "analogy for %s", "not 1 <= x", "SEN0401_DECK"))
    for l in ch: print(l[:200]); fail += [] if ok(l) else ["unexpected change: " + l[:100]]
    print("changed lines:", len(ch))
elif mode == "compare":
    for ch in chapters:
        dk = newest_delivered(ch); rc1, o1 = run(V1, ch, {"SEN0401_DECK": dk} if dk else {}); rc2, o2 = run(V2, ch)
        r1, r2 = refusals(o1), refusals(o2); crash1 = any("Traceback" in x for x in o1); lost = [x for x in r1 if x not in r2]; added = [x for x in r2 if x not in r1]
        print("ch%s deck %s: v1_2_0 %s, v1_3_0 %d refusals (exit %d); lost %d, added %d" % (ch, os.path.basename(dk) if dk else "(08-tooling)", "CRASH" if crash1 else "%d refusals" % len(r1), len(r2), rc2, len(lost), len(added)))
        for x in lost: print("   LOST ", x[:140]); fail.append("lost refusal ch" + ch)
        for x in added: print("   ADDED", x[:140]); fail += [] if "plan/deck mismatch" in x else ["added other refusal ch" + ch]
        if any("Traceback" in x for x in o2): fail.append("v1_3_0 crashes on ch" + ch)
elif mode == "lookup":
    for ch in chapters:
        dk = newest_delivered(ch); rc, o = run(V2, ch); m = re.search(r"(\d+) slides", " ".join(o)); n = nslides(dk) if dk else None
        print("ch%s: v1_3_0 reports %s slides; newest delivered deck %s has %s" % (ch, m.group(1) if m else "?", os.path.basename(dk) if dk else "-", n)); crash = any("Traceback" in x for x in o)
        if crash: fail.append("crash ch" + ch)
        elif dk and not (m and int(m.group(1)) == n) and not any("plan/deck mismatch" in x for x in o): fail.append("ch%s lookup does not use the delivered deck" % ch)
elif mode == "fixture":
    d9 = newest_delivered("09"); rc, o = run(V2, "04", {"SEN0401_DECK": d9}); print("fixture: ch04 plan against the ch09 deck, v1_3_0 exit", rc); [print("   ", x[:200]) for x in refusals(o) if "mismatch" in x]
    ms = [x for x in refusals(o) if "plan/deck mismatch" in x]; fail += [] if rc == 1 and ms and re.search(r"plan has 47 slides.*has \d+ slides", ms[0]) else ["mismatch not refused with both lengths"]
    rc1, o1 = run(V1, "04", {"SEN0401_DECK": d9}); print("same pair on v1_2_0: exit", rc1, "traceback" if any("Traceback" in x for x in o1) else "no traceback", "-", [x.strip()[:100] for x in refusals(o1)][:2])
    rc, o = run(V2, "04"); print("control: real ch04 deck exit", rc); fail += [] if rc == 0 else ["real ch04 refused"]
print("RESULT", "FAIL %s" % fail if fail else "PASS"); sys.exit(1 if fail else 0)
