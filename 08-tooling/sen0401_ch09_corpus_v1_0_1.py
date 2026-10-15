"""SEN0401 chapter 09 corpus bridge: NODES and CQS for the deck engine, derived from the chapter's RDODI data module
(sen0401_ch09_rdodi_data_v1_0_1.py) so that research and deck cannot drift apart. A node is (name, label, level, parent, example, paragraphs)."""
__version__ = "1.1.0"
import importlib
D = importlib.import_module("sen0401_ch09_rdodi_data_v1_0_1")
LAB = lambda c: D.LABELS.get(c) or (lambda t: t[0].upper() + t[1:])("".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip())
NODES, _seen = [], set()
for top, mid, leaf, ex, d, io in D.TAX:
    for c, lv, par in ((top, 1, None), (mid, 2, top), (leaf, 3, mid)):
        if c in _seen:
            continue
        _seen.add(c)
        NODES.append([c, LAB(c), lv, par, (ex, d, io) if lv == 3 else None, [("What it is", D.BODY[c])]])
CQS = list(D.CQS)


def run_checks_inprocess():
    """Execute every taxonomy expression and every extra claim of the data module in this interpreter, from the repository root; returns (n, failures)."""
    import ast, os, sys
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    old = os.getcwd(); os.chdir(repo)
    if os.path.join(repo, "08-tooling") not in sys.path:
        sys.path.insert(0, os.path.join(repo, "08-tooling"))
    def ev(src):
        t = ast.parse(src); last = t.body.pop(); ns = {}
        exec(compile(t, "claim", "exec"), ns)
        return repr(eval(compile(ast.Expression(last.value), "claim", "eval"), ns))
    bad, n = [], 0
    try:
        for top, mid, leaf, ex, d, io in D.TAX:
            if io:
                n += 1
                try: got = ev(io[0])
                except BaseException as e: got = "EXC %r" % (e,)
                if got != io[1]: bad.append((leaf, io[1], got))
        for expr, want in D.CLAIMS:
            n += 1
            try: got = ev(expr)
            except BaseException as e: got = "EXC %r" % (e,)
            if got != want: bad.append((expr[:80], want, got))
    finally:
        os.chdir(old)
    return n, bad
