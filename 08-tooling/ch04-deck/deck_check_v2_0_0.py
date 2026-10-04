"""Chapter 4 deck check, version 2.0.0. Every '>>>' example on the finished slides is re-run, one fresh namespace per
slide after the deck's PRELUDE, and what Python answers is compared with what the slide prints. One mismatch refuses
the deck. The elliptic-curve source the deck shows must also still equal the source the examples run.

Fork of deck_check_v1_0_0.py for the 2.0.0 deck: a statement meant to fail is compared against 'ErrorClass: message',
exactly as examples_run_v2_0_0.py records it, so the error messages on the slides are checked too.
Usage: deck_check_v2_0_0.py <deck.pptx>"""
__version__ = "2.0.0"
import os, sys, re, zipfile
from xml.dom import minidom

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v2_0_0 import PRELUDE, EC_SRC


def slides(path):
    z = zipfile.ZipFile(path)
    names = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
    out = []
    for n in sorted(names, key=lambda n: int(re.findall(r"\d+", n)[0])):
        d = minidom.parseString(z.read(n))
        paras = []
        for p in d.getElementsByTagName("a:p"):
            paras.append("".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")))
        out.append((n, paras))
    return out


def check(path):
    bad, n_ex = [], 0
    for name, paras in slides(path):
        ns = {}
        exec(PRELUDE, ns)
        i = 0
        while i < len(paras):
            p = paras[i]
            if p.startswith(">>> "):
                src = p[4:]
                nxt = paras[i + 1] if i + 1 < len(paras) else ""
                shown = None if nxt.startswith(">>> ") else nxt
                try:
                    try:
                        got = repr(eval(src, ns))
                    except SyntaxError:
                        exec(src, ns)
                        got = None
                except Exception as e:
                    got = "%s: %s" % (type(e).__name__, e)
                if got is not None or shown is not None:
                    n_ex += 1
                    if shown is not None and got != shown:
                        bad.append((name, src, shown, got))
                i += 1 if shown is None else 2
            else:
                i += 1
    return n_ex, bad


deck = sys.argv[1]
n, bad = check(deck)
norm = lambda t: re.sub(r"\s+", " ", t).strip()
flat = [norm(" ".join(p)) for _, p in slides(deck)]
if not any(norm(EC_SRC) in t for t in flat):
    bad.append(("deck", "ec_add and ec_mul as the slide shows them", "must equal the source the examples run", ""))
n += 1
print("%d examples re-run on %d slides; %d mismatch(es)" % (n, len(flat), len(bad)))
for b in bad:
    print("  REFUSED", b)
sys.exit(1 if bad else 0)
