#!/usr/bin/env python3
"""sen0401_plain_code v1_0_0 - rewrites a worked example that is stored as ONE expression with a lambda in it as plain Python statements with the same result (owner, 2026-10-30:
no lambda unless the subject teaches lambda). Three forms, each by the syntax tree, never by guessing:
  (a) the wrapper  (lambda g: (exec("SOURCE", g), g['result'])[1])({})   ->  SOURCE followed by a last line  result
  (b) an immediate lambda  (lambda a, b: BODY)(x, y)                        ->  a = x / b = y / BODY      (the text of each part is kept exactly as written)
  (c) a helper  name = lambda a: BODY  inside SOURCE                        ->  def name(a):  /  return BODY
A code with no lambda is returned unchanged. A form it cannot rewrite raises ValueError (the build stops). Usage: plain(code) -> code. --selftest runs known answers."""
__version__ = "1.0.0"
import ast, re, sys
MANUAL = {  # an immediate lambda whose body is a tuple of side effects ending in [-1]: written by hand, the result is checked by the caller
    "(lambda record: (record['Alice'], record.pop('Alice'), record.update({'Bob': 100000}), record)[-1])({'Alice': 100000})":
    "record = {'Alice': 100000}\nrecord.pop('Alice')\nrecord.update({'Bob': 100000})\nrecord"}
HELPER = re.compile(r"^(\s*)(\w+) = lambda ([\w, ]*): (.*)$")
def _helpers(src):
    out = []
    for ln in src.split("\n"):
        m = HELPER.match(ln)
        if m: out += [m.group(1) + "def %s(%s):" % (m.group(2), m.group(3).strip()), m.group(1) + "    return " + m.group(4)]
        else: out.append(ln)
    return "\n".join(out)
def plain(code):
    if "lambda" not in code: return code
    if code in MANUAL: return MANUAL[code]
    tree = ast.parse(code)
    if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Call) and isinstance(tree.body[0].value.func, ast.Lambda):
        call = tree.body[0].value; lam = call.func; a = lam.args
        if a.vararg or a.kwarg or a.defaults or a.kwonlyargs or call.keywords or len(a.args) != len(call.args): raise ValueError("unsupported lambda call: " + code[:80])
        body = lam.body
        if [x.arg for x in a.args] == ["g"] and isinstance(body, ast.Subscript) and isinstance(body.value, ast.Tuple) and len(body.value.elts) == 2:
            first, second = body.value.elts
            if isinstance(first, ast.Call) and isinstance(first.func, ast.Name) and first.func.id == "exec" and isinstance(first.args[0], ast.Constant) and isinstance(first.args[0].value, str) and ast.unparse(second) == "g['result']":
                src = first.args[0].value.rstrip("\n")
                if not re.search(r"^result\s*=", src, re.M): raise ValueError("wrapper without result: " + code[:80])
                new = _helpers(src) + "\nresult"
                if "lambda" in new: raise ValueError("lambda left in wrapper source: " + new[:120])
                return new
            raise ValueError("unknown wrapper: " + code[:80])
        lines = ["%s = %s" % (p.arg, ast.get_source_segment(code, v)) for p, v in zip(a.args, call.args)]
        new = "\n".join(lines + [ast.get_source_segment(code, body)])
        if "lambda" in new: raise ValueError("lambda left: " + new[:120])
        return new
    raise ValueError("lambda in an unsupported form: " + code[:80])
def selftest():
    c = {"(lambda g: (exec(\"a = 1\\nb = a + 1\\nresult = (a, b)\", g), g['result'])[1])({})": "a = 1\nb = a + 1\nresult = (a, b)\nresult",
         "(lambda x, y: (x + y, x * y))(2, 3)": "x = 2\ny = 3\n(x + y, x * y)",
         "(lambda g: (exec(\"f = lambda n: n * 2\\nresult = f(4)\", g), g['result'])[1])({})": "def f(n):\n    return n * 2\nresult = f(4)\nresult",
         "1 + 2": "1 + 2"}
    ok = all(plain(k) == v for k, v in c.items())
    for k in c:
        a = eval(k) if "exec" not in k else None
    print("SELFTEST", "PASS" if ok else "FAIL"); return ok
if __name__ == "__main__": sys.exit(0 if selftest() else 1)
