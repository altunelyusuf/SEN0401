#!/usr/bin/env python3
"""sen0401_arccheck_control_check v1_0_0 - the lineage agent's OWN checks of the deck arc check v1_2_0 (criterion AC9_ArcCheck), independent of the executor's logs.
Usage: sen0401_arccheck_control_check_v1_0_0.py MODE   MODE = sha | diff | compare | named | fixture
sha: v1_1_0 SHA-256 equals 9b2583bb...c341 (the value of its only commit 026a2be) and git shows no change to it since that commit
diff: the unified diff v1_1_0 to v1_2_0 changes only the version line, the comment lines, the reading of --slides, the 'want' default and the closing-part agenda rule (every changed line is one of an allowed set)
compare: (refusal texts compared with the number in "the standard is N" neutralised, since v1_1_0 is given N by this tool) for every chapter that has an arc plan and a deck: v1_1_0 --slides <deck length> versus v1_2_0 (no --slides): v1_2_0 may LOSE only refusals 'agenda range starting at slide X does not start at a section slide' and must ADD none; both outputs are printed
named: on chapters 1, 4, 8 v1_1_0 as shipped refuses the 26-slide standard and v1_2_0 neither that nor the closing-part range
fixture: three fixtures made from the chapter 4 deck by editing the agenda text only: (a) a range starting inside a section (the closing range not touched), (b) the closing range moved to start at slide 44 (inside section 5, not the summary slide), (c) a plan/file mismatch fixture (--slides 40 given for the 47-slide deck): v1_2_0 must refuse each (exit 1)"""
import difflib, glob, hashlib, os, re, shutil, subprocess, sys, tempfile, zipfile
T = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(T); V1 = T + "/sen0401_deck_arc_check_v1_1_0.py"; V2 = T + "/sen0401_deck_arc_check_v1_2_0.py"
mode = sys.argv[1]; fail = []
def run(script, ch, extra=(), env=None):
    r = subprocess.run([sys.executable, "-B", script, ch] + list(extra), capture_output=True, text=True, cwd=T, env=dict(os.environ, **(env or {}))); return r.returncode, (r.stdout + r.stderr).strip().splitlines()
refusals = lambda L: [re.sub(r"the standard is \d+", "the standard is N", l.strip()) for l in L if l.strip().startswith("REFUSED")]
if mode == "sha":
    h = hashlib.sha256(open(V1, "rb").read()).hexdigest(); print("v1_1_0 SHA-256", h)
    if not h.startswith("9b2583bb") or not h.endswith("c341"): fail.append("sha")
    d = subprocess.run(["git", "log", "--oneline", "--", "08-tooling/sen0401_deck_arc_check_v1_1_0.py"], cwd=REPO, capture_output=True, text=True).stdout.strip().splitlines(); print("commits touching v1_1_0:", d)
    st = subprocess.run(["git", "status", "--short", "08-tooling/sen0401_deck_arc_check_v1_1_0.py"], cwd=REPO, capture_output=True, text=True).stdout.strip(); print("git status:", repr(st))
    if len(d) != 1 or st: fail.append("v1_1_0 changed")
elif mode == "diff":
    a = open(V1).read().splitlines(); b = open(V2).read().splitlines(); ch = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    ok = lambda l: ("__version__" in l or l[1:].lstrip().startswith("# 1.2.0") or l[1:].lstrip().startswith("#   (2)") or "--slides" in l or "if want is None" in l or "closing_start" in l or "rs = [i + 1" in l or "does not start at a section slide" in l)
    for l in ch: print(l[:230]); fail += [] if ok(l) else ["unexpected change: " + l[:120]]
    print("changed lines:", len(ch))
elif mode == "compare":
    for d in sorted(glob.glob(T + "/ch*-deck")):
        ch = re.search(r"ch(\d\d)-deck", d).group(1)
        if not glob.glob(d + "/deck_plan_v*.json"): continue
        rc2, o2 = run(V2, ch); m = re.search(r"(\d+) slides", " ".join(o2))
        if not m:
            rc1, o1 = run(V1, ch, ["--slides", "42"]); same = (rc1 == rc2 and o1[-1:] == o2[-1:]); print("ch%s: both versions end the same way (exit %s, last line %r): %s" % (ch, rc2, o2[-1][:90], "same" if same else "DIFFERENT")); fail += [] if same else ["ch" + ch + " crash differs"]; continue
        rc1, o1 = run(V1, ch, ["--slides", m.group(1)]); r1, r2 = refusals(o1), refusals(o2)
        lost = [x for x in r1 if x not in r2]; added = [x for x in r2 if x not in r1]
        print("ch%s deck %s slides: v1_1_0(--slides N) %d refusals, v1_2_0 %d refusals; lost %d, added %d" % (ch, m.group(1), len(r1), len(r2), len(lost), len(added)))
        for x in lost: print("   LOST  ", x[:150]); fail += [] if "does not start at a section slide" in x else ["lost another refusal: " + x[:80] + " (ch%s)" % ch]
        for x in added: print("   ADDED ", x[:150]); fail.append("added refusal ch" + ch)
elif mode == "named":
    for ch in ("01", "04", "08"):
        rc1, o1 = run(V1, ch); rc2, o2 = run(V2, ch); d1 = [x for x in o1 if "the standard is 26" in x]; d2 = [x for x in o2 if "the standard is" in x]; r2 = [x for x in o2 if "does not start at a section slide" in x]
        print("ch%s: v1_1_0 as shipped: %d refusal line(s) naming the 26-slide standard, v1_2_0: %d; v1_2_0 agenda-closing-range refusals: %d; v1_2_0 remaining refusals: %s" % (ch, len(d1), len(d2), len(r2), [x.strip()[:90] for x in refusals(o2)]))
        if not d1 or d2 or r2: fail.append("ch" + ch + ": named refusal not shown gone")
elif mode == "fixture":
    deck = sorted(glob.glob(T + "/ch04-deck/sen0401_ch04_deck_v*.pptx"), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]; tmp = tempfile.mkdtemp()
    def edit(name, f):
        zin = zipfile.ZipFile(deck); out = tmp + "/" + name; zo = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "ppt/slides/slide2.xml": data = f(data.decode("utf-8")).encode("utf-8")
            zo.writestr(it, data)
        zo.close(); return out
    rg = re.findall(r"\(slides (\d+)-(\d+)\)", zipfile.ZipFile(deck).read("ppt/slides/slide2.xml").decode("utf-8")); print("agenda ranges of the real deck:", rg)
    a = edit("a.pptx", lambda s: s.replace("(slides %s-%s)" % rg[2], "(slides %d-%s)" % (int(rg[2][0]) + 1, rg[2][1]), 1).replace("(slides %s-%s)" % rg[1], "(slides %s-%d)" % (rg[1][0], int(rg[1][1]) + 1), 1))
    b = edit("b.pptx", lambda s: s.replace("(slides %s-%s)" % rg[-1], "(slides 44-%s)" % rg[-1][1], 1).replace("(slides %s-%s)" % rg[-2], "(slides %s-43)" % rg[-2][0], 1))
    for name, f, extra in (("a (range starts inside a section)", a, []), ("b (closing range moved to slide 44, inside a section)", b, []), ("c (plan/file mismatch: --slides 40)", deck, ["--slides", "40"])):
        rc, o = run(V2, "04", extra, {"SEN0401_DECK": f}); print("fixture", name, "exit", rc); [print("   ", x[:170]) for x in refusals(o)]; fail += [] if rc == 1 else ["fixture not refused: " + name]
    rc, o = run(V2, "04"); print("control: real ch04 deck exit", rc); fail += [] if rc == 0 else ["real ch04 deck refused"]
print("RESULT", "FAIL %s" % fail if fail else "PASS"); sys.exit(1 if fail else 0)
