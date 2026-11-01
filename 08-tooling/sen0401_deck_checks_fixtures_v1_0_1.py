#!/usr/bin/env python3
"""sen0401_deck_checks_fixtures v1.0.1 (over v1.0.0: reads expected v1_0_1, runs the indentation check v1_0_1, three fixtures with a compound statement split over code boxes) (task TK_Deck_Checks_Build) - writes the fixture decks (small .pptx files) for the four deck checks into a scratch folder, runs each check on its fixtures and compares
verdict and number of findings with the expected values written beforehand in deck_checks_logs/sen0401_deck_checks_expected_v1_0_1.json. Removes the scratch folder.
Usage: python3 -B sen0401_deck_checks_fixtures_v1_0_1.py"""
__version__ = "1.0.1"
import json, os, re, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
from pptx import Presentation
from pptx.util import Inches, Pt

T = os.path.dirname(os.path.abspath(__file__))
EXP = json.load(open(os.path.join(T, "deck_checks_logs", "sen0401_deck_checks_expected_v1_0_1.json")))["fixtures"]
CHECK = {"indent": "sen0401_deck_code_indent_check_v1_0_1.py", "lambda": "sen0401_deck_lambda_check_v1_0_0.py",
         "labels": "sen0401_deck_label_words_check_v1_0_0.py", "prompts": "sen0401_deck_prompt_check_v1_0_0.py"}


def tb(sl, l, t, w, h, lines, name):
    s = sl.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h)); s.name = name
    tf = s.text_frame; tf.word_wrap = True
    for k, ln in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = ln; r.font.size = Pt(14)
    return s


def deck(path, slides):
    """slides = [(title, [(name, [lines]) ...]) ...]"""
    p = Presentation(); p.slide_width = Inches(13.333); p.slide_height = Inches(7.5)
    for title, boxes in slides:
        sl = p.slides.add_slide(p.slide_layouts[6])
        tb(sl, 0.5, 0.2, 9, 0.6, [title], "title")
        for k, (name, lines) in enumerate(boxes):
            tb(sl, 1.0, 1.2 + 1.8 * k, 8, 1.6, lines, name)
    p.save(path)


C = lambda *lines: ("code 1", list(lines))          # a code box by shape name
P = lambda *lines: ("listing", list(lines))         # a code box by prompts (any shape name)
FIX = {
    "fx_indent_pass_shape": [("Loops", [C("for i in range(3):  # a loop", "    print(i)", "if x:", "    y = 1", "else:", "    y = 2", "def f(a, b):", "    return a + b",
                                          "total = sum([1,", "             2,", "             3])")])],
    "fx_indent_pass_prompts": [("Loops", [P(">>> for i in range(3):", "...     print(i)", "... ", "0", "1", "2", ">>> x = 1")])],
    "fx_indent_pass_brackets": [("Brackets", [C("d = {'a': 1}", "x = d['a']", "y = s[1:2]", "f = d.get('b', 0)", "h = lambda v: v + 1")])],
    "fx_indent_pass_nested": [("Nested", [C("for a in x:", "    if a:", "        print(a)", "    else:", "        print(0)")])],
    "fx_indent_fail_headerline": [("Loops", [C("for i in range(3): print(i)")])],
    "fx_indent_fail_unindented": [("Loops", [C("for i in range(3):", "print(i)")])],
    "fx_indent_fail_twospaces": [("Branch", [C("if x:", "  y = 1")])],
    "fx_indent_fail_continuation": [("Sum", [C("total = sum([1,", "2,", "3])")])],
    "fx_indent_fail_prompts": [("Loops", [P(">>> for i in range(3): print(i)", "0", "1", "2")])],
    "fx_indent_pass_split": [("Split", [("code 1", ["for k in range(3):"]), ("code 2", ["    print(k)"])])],
    "fx_indent_fail_split_end": [("Split", [("code 1", ["x = 1"]), ("code 2", ["for k in range(3):"])])],
    "fx_indent_fail_split_body": [("Split", [("code 1", ["for k in range(3):"]), ("code 2", ["print(k)"])])],
    "fx_lambda_fail": [("Sorting", [C("key = lambda x: x")])],
    "fx_lambda_pass_declared": [("Sorting", [C("key = lambda x: x")])],
    "fx_lambda_pass_title": [("Lambda functions in one line", [C("key = lambda x: x")])],
    "fx_lambda_pass_prose": [("Counting", [("note", ["A lambda is an anonymous function; this chapter does not use it."]), C("lambda_count = 3")])],
    "fx_lambda_fail_prompts": [("Functions", [P(">>> f = lambda x: x", ">>> f(2)", "2")])],
    "fx_labels_fail_what": [("Story", [("t1", ["WHAT: a block is a bundle of transactions."])])],
    "fx_labels_fail_why_dash": [("Story", [("t1", ["why - because the fee pays the miner."])])],
    "fx_labels_fail_endash": [("Story", [("t1", ["HOW – step by step."])])],
    "fx_labels_fail_three": [("Story one", [("t1", ["Who: Satoshi Nakamoto"]), ("t2", ["WHEN - January 2009"])]), ("Story two", [("t1", ["Where: the genesis block"])])],
    "fx_labels_pass_sentences": [("Story", [("t1", ["What a block is, in one sentence: a bundle of transactions."]), ("t2", ["Who signs? The sender signs."]), ("t3", ["Whenever the node restarts, it reloads the chain."])])],
    "fx_prompts_fail_input": [("Console", [P(">>> x = 1", ">>> x", "1")])],
    "fx_prompts_fail_more": [("Console", [P(">>> for i in range(2):", "...     print(i)", "0", "1")])],
    "fx_prompts_fail_inshape": [("Console", [C("x = 1", ">>> x")])],
    "fx_prompts_pass_shapes": [("Code", [C("x = 1", "y = x + 1")])],
    "fx_prompts_pass_nocode": [("Prose", [("t1", ["Nothing to run on this slide."])])],
}


def main():
    tmp = tempfile.mkdtemp(prefix="sen0401_dc_fx_"); bad = []
    try:
        for fx, e in EXP.items():
            f = os.path.join(tmp, fx + ".pptx"); deck(f, FIX[fx])
            exe = os.path.join(T, CHECK[e["check"]])
            if not os.path.exists(exe):
                print("%-30s CANNOT_RUN  %s does not exist" % (fx, CHECK[e["check"]])); bad.append(fx); continue
            r = subprocess.run([sys.executable, "-B", exe, f] + e.get("args", []), capture_output=True, text=True)
            out = r.stdout + r.stderr
            v = re.search(r"^VERDICT: (PASS|FAIL)", out, re.M)
            n = len(re.findall(r"^FINDING ", out, re.M))
            ok = bool(v) and v.group(1) == e["verdict"] and n == e["findings"] and (r.returncode == 0) == (e["verdict"] == "PASS")
            print("%-30s %-5s %-8s verdict %s findings %d exit %d (expected %s, %d)" % (fx, "PASS" if ok else "FAIL", e["check"], v and v.group(1), n, r.returncode, e["verdict"], e["findings"]))
            if not ok:
                bad.append(fx); print(out[:600])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("RESULT %s (%d of %d fixtures disagree)" % ("PASS" if not bad else "FAIL", len(bad), len(EXP)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
