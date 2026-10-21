"""SEN0401 chapter 8 corpus bridge (version 1.2.0: over the data module 1.2.0): NODES and CQS for the deck engine, derived from the chapter's RDODI data module (sen0401_ch08_rdodi_data_v1_2_0.py) so that research and deck cannot
drift apart, and run_checks_inprocess() for the lineage check: every executed leaf, claim and behaviour of the data module, run under the interpreter that imports this file.
A node is (name, label, level, parent, example, paragraphs)."""
__version__ = "1.2.0"
import ast, importlib, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
D = importlib.import_module("sen0401_ch08_rdodi_data_v1_2_0")
LAB = lambda c: D.LABELS.get(c) or (lambda t: t[0].upper() + t[1:])("".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip())
NODES, _seen = [], set()
for top, mid, leaf, ex, d, io in D.TAX:
    for c, lv, par in ((top, 1, None), (mid, 2, top), (leaf, 3, mid)):
        if c in _seen:
            continue
        _seen.add(c)
        NODES.append([c, LAB(c), lv, par, (ex, d, io) if lv == 3 else None, [("What it is", D.BODY[c])]])
CQS = list(D.CQS)
REPO = os.path.dirname(HERE)


def _eval(src):
    """a claim is an expression, or statements whose last line is the expression (as sen0401_rdodi_checks runs it); run from the repository root"""
    t = ast.parse(src); last = t.body.pop(); ns = {}
    cwd = os.getcwd(); os.chdir(REPO)
    try:
        exec(compile(t, "claim", "exec"), ns)
        return repr(eval(compile(ast.Expression(last.value), "claim", "eval"), ns))
    finally:
        os.chdir(cwd)


def run_checks_inprocess():
    bad = []; n = 0
    for top, mid, leaf, ex, d, io in D.TAX:
        n += 1
        try:
            got = _eval(io[0])
        except BaseException as e:
            got = "EXC %r" % (e,)
        if got != io[1]:
            bad.append((leaf, io[1], got))
    for e, x in D.CLAIMS:
        n += 1
        try:
            got = _eval(e)
        except BaseException as ex_:
            got = "EXC %r" % (ex_,)
        if got != x:
            bad.append((e[-60:], x, got))
    for what, code, want in D.BEH:
        n += 1
        r = subprocess.run([sys.executable, "-W", "ignore::SyntaxWarning", "-c", code], capture_output=True, text=True)
        got = r.stdout.strip() if r.returncode == 0 else r.stderr.strip().splitlines()[-1]
        if got != want:
            bad.append((what[:60], want, got))
    return n, bad


if __name__ == "__main__":
    n, bad = run_checks_inprocess()
    print(n, "claims executed under CPython", sys.version.split()[0], "- failures:", bad)
    ids = [x[0] for x in NODES]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    print(len(NODES), "nodes;", sum(1 for x in NODES if x[2] == 1), "branches;", sum(1 for x in NODES if x[2] == 2), "groups;", sum(1 for x in NODES if x[2] == 3), "leaves;",
          sum(len(t.split()) for x in NODES for f, t in x[5]), "words")
