"""Chapter check for the chapter 1 lecture deck.

Three things are re-run or re-read against the finished .pptx, and any one of them failing refuses the deck:

1. every '>>>' example on a slide is executed again, in one session per slide started after the chapter
   PRELUDE, and what it answers must equal what the slide shows;
2. every program the deck shows as a whole (examples_v1_1_0.BLOCKS) is executed again, and the value of
   `result` must appear on the slide that carries that program's last lines;
3. every program excerpt is a real excerpt: a slide captioned 'program <id>, lines a to b of n' must carry
   exactly lines a to b of that program, in order.

Usage: deck_check_v1_1_0.py <deck.pptx>
"""
__version__ = "1.1.0"
import os, re, sys, zipfile
from xml.dom import minidom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_1_0 import PRELUDE, BLOCKS

CAP = re.compile(r"program ([A-Za-z0-9_]+), lines (\d+) to (\d+) of (\d+)")


def slides(path):
    z = zipfile.ZipFile(path); out = []
    names = [n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
    for n in sorted(names, key=lambda n: int(re.findall(r'\d+', n)[0])):
        d = minidom.parseString(z.read(n)); paras = []
        for p in d.getElementsByTagName('a:p'):
            paras.append("".join(t.firstChild.nodeValue if t.firstChild else ""
                                 for t in p.getElementsByTagName('a:t')))
        out.append((n, paras))
    return out


def check(path):
    bad = []; n_ex = 0
    pages = slides(path)
    for name, paras in pages:
        ns = {}; exec(PRELUDE, ns); i = 0
        while i < len(paras):
            p = paras[i]
            if p.startswith('>>> '):
                src = p[4:]; nxt = paras[i + 1] if i + 1 < len(paras) else ""
                shown = None if nxt.startswith('>>> ') else nxt
                try:
                    try: got = repr(eval(src, ns))
                    except SyntaxError: exec(src, ns); got = None
                except Exception as e: got = "%s: %s" % (type(e).__name__, e)
                if got is not None or shown is not None:
                    n_ex += 1
                    if shown is not None and got != shown:
                        bad.append((name, src, shown, got))
                i += 1 if shown is None else 2
            else:
                i += 1
    # the programs, and the honesty of every excerpt
    seen = {}
    for name, paras in pages:
        for p in paras:
            m = CAP.search(p)
            if not m: continue
            key, a, b, total = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            if key not in BLOCKS:
                bad.append((name, "program " + key, "a program of this chapter", "no such program")); continue
            lines = BLOCKS[key].split("\n")
            if total != len(lines):
                bad.append((name, key, "%d lines" % len(lines), "the slide says %d" % total)); continue
            want = lines[a - 1:b]
            if not _contains_run(paras, want):
                bad.append((name, key, "lines %d to %d verbatim and in order" % (a, b), "not on the slide"))
            seen.setdefault(key, set()).update(range(a, b + 1))
    for key, body in BLOCKS.items():
        ns = {}; exec(PRELUDE, ns)
        try:
            exec(body, ns); got = repr(ns["result"])
        except Exception as e:
            bad.append(("programs", key, "runs", "%s: %s" % (type(e).__name__, e))); continue
        n_ex += 1
        if not any(got in " ".join(paras) for _n, paras in pages):
            bad.append(("programs", key, got, "the deck does not show this result"))
        if seen.get(key, set()) != set(range(1, len(body.split("\n")) + 1)):
            missing = sorted(set(range(1, len(body.split("\n")) + 1)) - seen.get(key, set()))
            if len(missing) and min(missing) > 10:
                bad.append(("programs", key, "every line shown", "lines %s are not on any slide" % missing[:6]))
    return n_ex, bad


def _contains_run(paras, want):
    for i in range(len(paras) - len(want) + 1):
        if paras[i:i + len(want)] == want:
            return True
    return False


n, bad = check(sys.argv[1])
print("%d examples re-run; %d mismatch(es)" % (n, len(bad)))
for b in bad: print("  REFUSED", b)
sys.exit(1 if bad else 0)
