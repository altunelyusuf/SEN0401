#!/usr/bin/env python3
"""sen0401_deck_checks_agreement v1.0.1 (the indentation check is v1_0_1) (task TK_Deck_Checks_Build) - runs the four deck checks on the newest committed deck of each chapter 1 to 6 and, next to them, the numbers of
sen0401_deck_teach_measure_v1_0_0.py computed on the SAME decks (the measure's own functions; its 'latest' lookup is pointed at the deck named here). For a chapter whose newest deck has no prompts the
newest committed deck WITH prompts is measured too, because the measure reads prompt rows only. Prints, per deck, check count | measure count and AGREE or DIFFERS.
Usage: python3 -B sen0401_deck_checks_agreement_v1_0_1.py"""
__version__ = "1.0.1"
import glob, importlib.util, io, contextlib, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def committed_decks(n):
    fs = subprocess.run(["git", "ls-files", "03-materials/ch%02d" % n], cwd=R, capture_output=True, text=True).stdout.split()
    return sorted((os.path.join(R, f) for f in fs if f.endswith(".pptx") and "_3e_v" in f), key=vk)


def prompted(deck):
    import zipfile
    z = zipfile.ZipFile(deck)
    return any("&gt;&gt;&gt; " in z.read(n).decode("utf-8", "ignore") for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n))


def run(check, deck):
    r = subprocess.run([sys.executable, "-B", os.path.join(T, check), deck], capture_output=True, text=True)
    c = re.search(r"^COUNTS (.*)$", r.stdout, re.M)
    return dict(re.findall(r"(\w+)=(\[[^\]]*\]|\S+)", c.group(1))) if c else {}, r.stdout


def measure(n, deck):
    spec = importlib.util.spec_from_file_location("mz", os.path.join(T, "sen0401_deck_teach_measure_v1_0_0.py")); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.latest = lambda pat: deck
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        m.main()
    return json.loads(buf.getvalue())[str(n)] if str(n) in json.loads(buf.getvalue()) else json.loads(buf.getvalue())[n]


def main():
    import sen0401_deck_teach_measure_v1_0_0 as _  # noqa  (selftest of the measure is run separately)
    ok_all = True
    for n in range(1, 7):
        ds = committed_decks(n); cands = [ds[-1]] + ([[d for d in ds if prompted(d)][-1]] if not prompted(ds[-1]) else [])
        for deck in cands:
            ind, _o = run("sen0401_deck_code_indent_check_v1_0_1.py", deck)
            lam, _o = run("sen0401_deck_lambda_check_v1_0_0.py", deck)
            lab, _o = run("sen0401_deck_label_words_check_v1_0_0.py", deck)
            pro, _o = run("sen0401_deck_prompt_check_v1_0_0.py", deck)
            print("ch%02d %s (%s)" % (n, os.path.basename(deck), "with prompts" if prompted(deck) else "without prompts"))
            print("   checks : code_lines=%s indented=%s one_line_compounds=%s | lambda code lines=%s | label shapes=%s on slides %s | prompt rows=%s" %
                  (ind.get("code_lines"), ind.get("lines_with_leading_indentation"), ind.get("one_line_compounds"), lam.get("code_lines_with_lambda"), lab.get("label_shapes"), lab.get("slides_with_such_shape"), pro.get("prompt_rows")))
            m = measure(n, deck)
            print("   measure: code_lines=%s indented=%s one_line_compounds=%s | lambda lines (any text shape)=%s | label shapes=%s on slides %s" %
                  (m["code_lines_prompt_rows_stripped"], m["with_leading_indentation"], m["one_line_compound"], m["lambda_lines"], m["text_shapes_beginning_with_5N1K_label"], m["slides_with_such_shape"]))
            if prompted(deck):
                a = (str(m["code_lines_prompt_rows_stripped"]), str(m["with_leading_indentation"]), str(m["one_line_compound"]), str(m["text_shapes_beginning_with_5N1K_label"]))
                b = (ind.get("code_lines"), ind.get("lines_with_leading_indentation"), ind.get("one_line_compounds"), lab.get("label_shapes"))
                print("   code lines / indented / one-line compounds / label shapes:", "AGREE" if a == b else "DIFFERS %s vs %s" % (b, a), "; lambda: check %s vs measure %s%s" % (lam.get("code_lines_with_lambda"), m["lambda_lines"], "" if str(m["lambda_lines"]) == lam.get("code_lines_with_lambda") else " (the measure counts the substring in any text shape, prose included)"))
                ok_all &= a == b
            else:
                print("   (measure reads prompt rows only: 0 code lines on this deck; not comparable)")
    print("AGREEMENT:", "all compared counts agree" if ok_all else "some differ, see above")


if __name__ == "__main__":
    main()
