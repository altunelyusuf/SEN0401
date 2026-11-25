#!/usr/bin/env python3
"""sen0401_ch02_lambda_free v1.0.0 - rewrites the one-line quiz and example programs of the chapter 2 page that call an anonymous function at once, (lambda a, b: BODY)(x, y), as plain
statements (a, b = x, y). quiz_form() returns the program for the page (print is kept), expr_form() the one-line form of the ontology examples ('a = x; b = y; BODY'). Behaviour is unchanged;
the test in __main__ runs both forms against the originals. Standard library only."""
__version__ = "1.0.0"
import ast, contextlib, io, re

HAND = {  # the programs whose function arguments are functions or that hold a second function: written out by hand, keyed by the original text
 "chains": ("chains = {'A': [100, 100, 100], 'B': [100, 100, 120]}\ntotals = {k: sum(v) for k, v in chains.items()}\nprint(max(totals, key=totals.get))",
            "chains = {'A': [100, 100, 100], 'B': [100, 100, 120]}; totals = {k: sum(v) for k, v in chains.items()}; max(totals, key=totals.get)"),
 "header": ("hl = __import__('hashlib')\ndef d(b): return hl.sha256(hl.sha256(b).digest()).digest()\ns = __import__('struct')\nprint(d(s.pack('<I', 1) + bytes(32) + bytes.fromhex('4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b')[::-1] + s.pack('<III', 1231006505, 0x1d00ffff, 2083236893))[::-1].hex())",
            "hl = __import__('hashlib'); s = __import__('struct'); hl.sha256(hl.sha256(s.pack('<I', 1) + bytes(32) + bytes.fromhex('4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b')[::-1] + s.pack('<III', 1231006505, 0x1d00ffff, 2083236893)).digest()).digest()[::-1].hex()"),
 "merkle": ("hl = __import__('hashlib')\ndef d(b): return hl.sha256(hl.sha256(b).digest()).digest()\nL = [d(x) for x in (b'A', b'B', b'C', b'D')]\nprint(d(d(L[0] + L[1]) + d(L[2] + L[3])).hex()[:16])",
            "hl = __import__('hashlib'); L = [hl.sha256(hl.sha256(x).digest()).digest() for x in (b'A', b'B', b'C', b'D')]; hl.sha256(hl.sha256(hl.sha256(hl.sha256(L[0] + L[1]).digest()).digest() + hl.sha256(hl.sha256(L[2] + L[3]).digest()).digest()).digest()).digest().hex()[:16]"),
}

def _split(src):
    """(statements, body source) of a simple (lambda ...)(...) call, or None"""
    t = ast.parse(src.strip(), mode="eval").body
    if not (isinstance(t, ast.Call) and isinstance(t.func, ast.Lambda) and not t.keywords): return None
    lam = t.func; a = lam.args
    if a.vararg or a.kwarg or a.kwonlyargs or a.defaults or len(a.args) != len(t.args): return None
    if any(isinstance(n, ast.Lambda) for n in ast.walk(lam.body)) or any(isinstance(n, ast.Lambda) for x in t.args for n in ast.walk(x)): return None
    seg = lambda n: ast.get_source_segment(src.strip(), n)
    return ["%s = %s" % (p.arg, seg(x)) for p, x in zip(a.args, t.args)], seg(lam.body)

def _hand(src):
    if "lambda c: sum(chains[c])" in src: return HAND["chains"]
    if "s.pack('<III'" in src and "lambda d, s" in src: return HAND["header"]
    if "lambda L: d(d(L[0]" in src: return HAND["merkle"]
    return None

def quiz_form(code):
    if "lambda" not in code: return code
    h = _hand(code)
    if h: return h[0]
    m = ast.parse(code).body
    assert len(m) == 1 and isinstance(m[0], ast.Expr) and m[0].value.func.id == "print", code
    r = _split(ast.get_source_segment(code, m[0].value.args[0]))
    assert r, code
    return "\n".join(r[0] + ["print(%s)" % r[1]])

def expr_form(expr):
    if "lambda" not in expr: return expr
    r = _split(expr)
    if r is None:
        for k, v in HAND.items():
            pass
        if "lambda c: sum(chains[c])" in expr: return HAND["chains"][1]
        if "lambda d, s" in expr: return HAND["header"][1]
        if "lambda L: d(d(L[0]" in expr: return HAND["merkle"][1]
        raise ValueError(expr)
    return "; ".join(r[0] + [r[1]])

def run_quiz(code):
    b = io.StringIO()
    with contextlib.redirect_stdout(b): exec(code, {})
    return b.getvalue()

def run_expr(expr):
    parts = [p for p in re.split(r";\s+(?=[A-Za-z_(\[])", expr)]
    g = {}
    for p in parts[:-1]: exec(p, g)
    return eval(parts[-1], g)

if __name__ == "__main__":
    import sys, json
    raw = open(sys.argv[1], encoding="utf-8").read(); n = 0
    for m in re.finditer(r'"code": ("(?:[^"\\]|\\.)*")', raw):
        s = json.loads(m.group(1))
        if "lambda" in s:
            new = quiz_form(s); assert "lambda" not in new and run_quiz(new) == run_quiz(s), s; n += 1
    print("quiz programs equal:", n)
