#!/usr/bin/env python3
"""sen0401_code_gate_fixtures v1.0.0 (task TK_Code_Gate_Build) - builds the fixture decks in a scratch root, runs the old and the successor checks on them and compares each outcome
with the expected verdicts written beforehand in code_gate_logs/sen0401_code_gate_expected_v1_0_0.json. Prints one line per fixture and tool, then RESULT PASS/FAIL. Removes its scratch root.
Usage: python3 -B sen0401_code_gate_fixtures_v1_0_0.py      (python-pptx from the system python; the deck checks run under /root/.local/bin/python3.14)"""
__version__ = "1.0.0"
import json, os, re, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
from pptx import Presentation
from pptx.util import Inches, Pt

T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
PY314 = "/root/.local/bin/python3.14"
EXP = json.load(open(os.path.join(T, "code_gate_logs", "sen0401_code_gate_expected_v1_0_0.json")))["fixtures"]
NOTE = "This note explains the code beside it in plain words so that a reader understands what the lines do and why."


def tb(sl, l, t, w, h, text, name=None, mono=False):
    s = sl.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = s.text_frame; tf.word_wrap = True
    lines = text.split("\n")
    for k, ln in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = ln; r.font.size = Pt(14)
        if mono:
            r.font.name = "Courier New"
    if name:
        s.name = name
    return s


def deck(path, kind):
    p = Presentation(); p.slide_width = Inches(13.333); p.slide_height = Inches(7.5)
    sl = p.slides.add_slide(p.slide_layouts[6])
    tb(sl, 0.5, 0.2, 8, 0.6, "Fixture slide", "title")
    tb(sl, 12.0, 7.0, 1.2, 0.4, "1 / 1", "number")
    if kind != "std_longresult":
        tb(sl, 1.0, 3.1, 6.0, 0.6, NOTE, "note")
    tbl = sl.shapes.add_table(2, 2, Inches(8), Inches(2), Inches(4), Inches(1)).table
    tbl.cell(0, 0).text = "a"; tbl.cell(0, 1).text = "b"; tbl.cell(1, 0).text = "1"; tbl.cell(1, 1).text = "2"
    if kind == "prompts":
        tb(sl, 1.0, 2.0, 6.0, 1.0, ">>> x = 5\n>>> x * 2\n10\n>>> sorted([3, 1, 2])\n[1, 2, 3]", "listing", True)
    else:
        tb(sl, 1.0, 2.0, 6.0, 1.0, "x = 5", "code 1", True)
        if kind in ("results", "wrong", "above"):
            top = 3.8 if kind != "above" else 1.2
            tb(sl, 1.0, top, 6.0, 0.4, "x * 2  →  " + ("11" if kind == "wrong" else "10"), "result 1", True)
            tb(sl, 1.0, top + 0.4, 6.0, 0.4, "sorted([3, 1, 2])  →  [1, 2, 3]", "result 1", True)
            tb(sl, 1.0, top - 0.3 if kind != "above" else 0.8, 6.0, 0.3, "RESULT", "result header")
        if kind == "std_longresult":
            tb(sl, 1.0, 3.8, 6.0, 0.4, "list(range(10))  →  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]", "result 1", True)
    p.save(path)


def run(cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, **(env or {})))
    return r.returncode, r.stdout + r.stderr


def main():
    root = tempfile.mkdtemp(prefix="sen0401_cg_fx_")
    fails = []
    try:
        chd = os.path.join(root, "08-tooling", "ch99-deck"); os.makedirs(chd)
        os.symlink(os.path.join(R, "06-quality"), os.path.join(root, "06-quality"))
        open(os.path.join(chd, "examples_v1_0_0.py"), "w").write('PRELUDE = ""\n')
        rows = [["x * 2", "10"], ["sorted([3, 1, 2])", "[1, 2, 3]"]]
        py = run([PY314, "-c", "import platform;print(platform.python_version())"])[1].strip()
        json.dump({"_python": py, "g": rows}, open(os.path.join(chd, "examples_out_v1_0_0.json"), "w"))
        json.dump({"slides": []}, open(os.path.join(chd, "deck_plan_v1_0_0.json"), "w"))
        kinds = {"fx_prompts": "prompts", "fx_noprompts_results": "results", "fx_noprompts_wrong": "wrong", "fx_noprompts_noresults": "noresults",
                 "fx_noprompts_above": "above", "fx_std_longresult": "std_longresult"}
        env = {"SEN0401_ROOT": root}
        outs = {}
        for fx, kind in kinds.items():
            f = os.path.join(root, fx + ".pptx"); deck(f, kind); e = EXP[fx]
            def chk(label, ok, detail):
                print("%-24s %-22s %s  %s" % (fx, label, "PASS" if ok else "FAIL", detail))
                if not ok:
                    fails.append((fx, label, detail))
            for tool, key in (("sen0401_deck_check_v1_1_0.py", "deck_check_old"), ("sen0401_deck_check_v1_2_0.py", "deck_check_new")):
                if key in e:
                    rc, out = run([PY314, "-B", os.path.join(T, tool), "99", f], env)
                    outs[(fx, key)] = out
                    m = re.search(r"(\d+) examples re-run", out); mm = re.search(r"(\d+) mismatch", out)
                    want = e[key]
                    ok = rc == want["exit"] and m and int(m.group(1)) == want["examples"] and ("mismatches" not in want or int(mm.group(1)) == want["mismatches"])
                    chk(key, bool(ok), "exit %d, %s examples, %s mismatches (expected exit %d, %d examples)" % (rc, m and m.group(1), mm and mm.group(1), want["exit"], want["examples"]))
            if e.get("new_equals_old_but_version"):
                a = outs[(fx, "deck_check_old")].replace("1.1.0", "X"); b = outs[(fx, "deck_check_new")].replace("1.2.0", "X")
                chk("new equals old", a == b, "outputs identical but the version token")
            for tool, key in (("sen0401_deck_standard_check_v1_2_0.py", "std_old"), ("sen0401_deck_standard_check_v1_3_0.py", "std_new")):
                if key in e:
                    rc, out = run([sys.executable, "-B", os.path.join(T, tool), "99", f], env)
                    d3 = re.search(r"^D3 (\w+)", out, re.M); cs = re.search(r"code_slides=(\d+)", out)
                    ok = d3 and cs and d3.group(1) == e[key]["D3"] and int(cs.group(1)) == e[key]["code_slides"]
                    chk(key, bool(ok), "D3 %s, code_slides %s (expected %s, %d)" % (d3 and d3.group(1), cs and cs.group(1), e[key]["D3"], e[key]["code_slides"]))
        if "-v" in sys.argv:
            for k, v in outs.items():
                print(k, v.strip()[:400])
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("RESULT %s (%d failing)" % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
