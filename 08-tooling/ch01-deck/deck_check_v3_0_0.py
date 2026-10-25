"""Chapter 1 deck check, version 3.0.0 - the chapter's own deck check for the deck 3.0.0 (NEW file; deck_check_v1_2_0.py, which wraps the engine check over the earlier recordings, stays unchanged).
Fork of ch08-deck/deck_check_v1_0_0.py for this chapter's examples module. Every '>>>' example on the finished slides is re-run, one slide after the deck's PRELUDE, and what Python answers
is compared with what the slide prints. One mismatch refuses the deck. In addition the provenance of every native chart is checked: each plotted value must be a number that an executed
example printed (examples_out_v3_0_0.json, recorded by examples_run_v3_0_0.py), as it stands or in millions (the issuance chart draws millions). Run it under the interpreter the examples were
recorded with (the deck prints that version on every code slide).
Usage: deck_check_v3_0_0.py <deck.pptx>"""
__version__ = "3.0.0"
import json, os, re, sys, zipfile
from xml.dom import minidom

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from examples_v3_0_0 import PRELUDE


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


def numbers(o):
    out = set()
    if isinstance(o, (int, float)) and not isinstance(o, bool): out.add(round(float(o), 6))
    elif isinstance(o, (list, tuple)):
        for x in o: out |= numbers(x)
    elif isinstance(o, dict):
        for x in o.values(): out |= numbers(x)
    elif isinstance(o, str):
        for m in re.findall(r"-?\d+(?:\.\d+)?", o): out.add(round(float(m), 6))
    return out


def chart_provenance(path):
    import ast
    rec = json.load(open(os.path.join(HERE, "examples_out_v3_0_0.json")))
    known = set()
    for k, rows in rec.items():
        if k.startswith("_"): continue
        for expr, out in rows:
            try: known |= numbers(ast.literal_eval(out))
            except Exception: known |= numbers(out)
    z = zipfile.ZipFile(path); bad = []; n = 0
    for name in sorted(x for x in z.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", x)):
        x = z.read(name).decode("utf-8")
        for blk in re.findall(r"<c:val>.*?</c:val>", x, re.S):
            for v in re.findall(r"<c:v>([^<]*)</c:v>", blk):
                try: f = float(v)
                except ValueError: continue
                n += 1
                if not (round(f, 6) in known or round(f * 1e6, 4) in {round(k, 4) for k in known} or any(abs(f * 1e6 - k) < 1.0 for k in known)):
                    bad.append((name, v, "value %s is in no executed output (provenance)" % v))
    return n, bad


deck = sys.argv[1]
n, bad = check(deck)
print("%d examples re-run on %d slides; %d mismatch(es)" % (n, len(slides(deck)), len(bad)))
for b in bad:
    print("  REFUSED", b)
nc, badc = chart_provenance(deck)
print("%d plotted chart values compared with the executed outputs; %d without provenance" % (nc, len(badc)))
for b in badc:
    print("  REFUSED", b)
sys.exit(1 if bad or badc else 0)
