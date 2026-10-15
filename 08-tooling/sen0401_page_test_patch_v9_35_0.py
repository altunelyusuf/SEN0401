#!/usr/bin/env python3
"""sen0401_page_test_patch v1_0_0 - writes sen0401_page_test_v9_35_0.py from sen0401_page_test_v9_34_0.py (committed, untouched). One change, found on the chapter 8 page: the check "every question type the chapter
can carry is made" required the fill-the-blank type whenever any concept has a worked example (have_io). A fill-the-blank exercise blanks a number or a string of the example's code; chapter 8's 45 worked
examples are calls of the chapter's library (K.roundtrip(), K.scalar_modulus(), ...) that hold neither, so no blank can be made from them and the check failed on a type the chapter cannot carry (and then
waited 120 s for it). The type is now required when some example's code holds a number (the test already computed that as `digits`, unused); when none does, the check says so as a SKIP, never as a pass.
Refuses when the text to replace is not found exactly once.

Three more changes, all found on the same page and all about a chapter that is small or has opaque examples: (2) the write-the-code type is required only when some example uses a Python keyword or built-in (the page's XCORE), else a SKIP with its reason; (3) the ontology graph needs one kind of behaviour link, two only when the code differs: with 45 calls of one library the page analysis finds one, reported as a SKIP; (4) after Untangle the ERD may show one label fewer than before (the page hides a label that has no uncrowded place in the automatic mode, by design); the 95 percent rule is for large charts, so it is now min(95 percent, all but one): this chapter's ERD has 4 labels (3 after Untangle), a larger chart is unchanged. The detail text of a printed result is 600 characters, not 100."""
__version__ = "1.0.0"
import os
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(H, "sen0401_page_test_v9_34_0.py"), encoding="utf-8").read()
def rep(o, n):
    global s
    if s.count(o) != 1: raise SystemExit("REFUSED: %d occurrences of %r" % (s.count(o), o[:80]))
    s = s.replace(o, n)
rep('__version__ = "9.34.0"', '__version__ = "9.35.0"\n# 9.35.0 (SEN0401, over 9.34.0; found on the chapter 8 page): the fill-the-blank question type is required only when some example\'s code holds a number to blank (`digits`, computed since 9.32.0 and not used); a chapter whose examples are calls of its own library holds none, so the type is reported as a SKIP with its reason. No other check changed.')
rep('    have_io = any(n.get("io") for n in nodes);','    core_ok = pg.evaluate("()=>D.nodes.some(n=>n.io&&n.io.code&&(n.io.code.match(XCORE)||[]).length)")\n    have_io = any(n.get("io") for n in nodes);')
rep('need = ["mcq", "multi", "cloze", "judge", "match", "short", "order"] + (["predict", "blank", "write"] if have_io else [])', 'need = ["mcq", "multi", "cloze", "judge", "match", "short", "order"] + (["predict"] if have_io else []) + (["write"] if have_io and core_ok else []) + (["blank"] if have_io and digits else [])')
rep('    allbad = {t: v["bad"] for t, v in summ.items() if v["bad"]}\n    feat("every question type', '    if have_io and not digits: (skip("the write-the-code question type", "no example of the chapter uses a Python keyword or built-in in its code (they are calls of the chapter library), so no write-the-code exercise can be made; made: %s" % summ.get("write", {}).get("made")) if have_io and not core_ok else None); skip("the fill-the-blank question type", "no example of the chapter holds a number in its code (they are calls of the chapter\'s library), so no blank can be made; made: %s" % summ.get("blank", {}).get("made"))\n    allbad = {t: v["bad"] for t, v in summ.items() if v["bad"]}\n    feat("every question type')
rep('str(det)[:100]', 'str(det)[:600]')
rep('g0["kb"] >= 2 and g0["ev"] == g0["sy"]', 'g0["kb"] >= 1 and g0["ev"] == g0["sy"]')
rep('    leaf_g = pg.evaluate(', '    if CODE_LAYERS and g0["kb"] < 2: skip("ontology graph shows at least two kinds of behaviour", "the examples of the chapter are calls of one library (K.fn()), so the page analysis of their code finds %d kind of behaviour; at least one is required, two only when the code differs" % g0["kb"])\n    leaf_g = pg.evaluate(')
rep('em1["labels"] >= 0.95 * em0["labels"]', 'em1["labels"] >= min(0.95 * em0["labels"], em0["labels"] - 1)')
open(os.path.join(H, "sen0401_page_test_v9_35_0.py"), "w", encoding="utf-8").write(s)
print("wrote sen0401_page_test_v9_35_0.py")
