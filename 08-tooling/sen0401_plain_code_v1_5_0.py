#!/usr/bin/env python3
"""sen0401_plain_code v1_5_0 (over 1.4.0: six more hand-written cases, the chapter 4 examples PointAddition, WalletImportFormat, VersionPrefix, P2pkhAddress, P2shAddress and SegwitUpgrade, whose immediate lambdas nest other lambdas; each is rewritten as assignments, a def and the closing expression and the caller checks that the result is the same). Original text of 1.4.0: (over 1.3.0: three more hand-written cases, the chapter 3 wrapper examples Proxy/getblockhash, the work comparison and the chain tips, whose wrappers hold an inner lambda used as a sort key or a returned function; each is rewritten with a def and the caller checks that the result is the same). Original text of 1.3.0: (over 1.2.0: three more hand-written cases, the chapter 2 examples BlockHeader, MerkleTree and BestBlockchain, whose immediate lambdas take a lambda as an argument or hold a nested lambda; the result is checked by the caller). Original text of 1.2.0: (over 1.1.0: one more hand-written case, the chapter 1 example with the nested lambdas of the double-spend race (the result is checked by the caller). Over 1.0.0: one more hand-written case in MANUAL, the chapter 5 example DigitalSignature, whose immediate lambda takes a lambda as an argument; the result is checked by the caller) - rewrites a worked example that is stored as ONE expression with a lambda in it as plain Python statements with the same result (owner, 2026-10-30:
no lambda unless the subject teaches lambda). Three forms, each by the syntax tree, never by guessing:
  (a) the wrapper  (lambda g: (exec("SOURCE", g), g['result'])[1])({})   ->  SOURCE followed by a last line  result
  (b) an immediate lambda  (lambda a, b: BODY)(x, y)                        ->  a = x / b = y / BODY      (the text of each part is kept exactly as written)
  (c) a helper  name = lambda a: BODY  inside SOURCE                        ->  def name(a):  /  return BODY
A code with no lambda is returned unchanged. A form it cannot rewrite raises ValueError (the build stops). Usage: plain(code) -> code. --selftest runs known answers."""
__version__ = "1.5.0"
import ast, re, sys
MANUAL = {
    '(lambda g: (exec("import json\\nclass Proxy:\\n    def __getattr__(self, name):\\n        return lambda *args: json.dumps({\'version\': \'1.1\', \'method\': name, \'params\': list(args), \'id\': 1})\\nresult = Proxy().getblockhash(1000)", g), g[\'result\'])[1])({})':
    "import json\nclass Proxy:\n    def __getattr__(self, name):\n        def call(*args):\n            return json.dumps({'version': '1.1', 'method': name, 'params': list(args), 'id': 1})\n        return call\nresult = Proxy().getblockhash(1000)\nresult",
    '(lambda g: (exec("a_work = 3 * (2**256 // (0xffff * 256**26 + 1))\\nb_work = 2 * (2**256 // ((0xffff * 256**26) // 4 + 1))\\nresult = (a_work < b_work, max([(\'A\', a_work), (\'B\', b_work)], key=lambda c: c[1])[0])", g), g[\'result\'])[1])({})':
    "a_work = 3 * (2**256 // (0xffff * 256**26 + 1))\nb_work = 2 * (2**256 // ((0xffff * 256**26) // 4 + 1))\ndef work_of(c):\n    return c[1]\nresult = (a_work < b_work, max([('A', a_work), ('B', b_work)], key=work_of)[0])\nresult",
    '(lambda g: (exec("blocks = {\'G\': (None, 0), \'A1\': (\'G\', 1), \'B1\': (\'G\', 1), \'A2\': (\'A1\', 2)}\\ntips = sorted(b for b in blocks if not any(p == b for p, h in blocks.values()))\\nresult = (tips, max(tips, key=lambda b: blocks[b][1]), sorted(b for b, (p, h) in blocks.items() if h == 1))", g), g[\'result\'])[1])({})':
    "blocks = {'G': (None, 0), 'A1': ('G', 1), 'B1': ('G', 1), 'A2': ('A1', 2)}\ntips = sorted(b for b in blocks if not any(p == b for p, h in blocks.values()))\ndef height_of(b):\n    return blocks[b][1]\nresult = (tips, max(tips, key=height_of), sorted(b for b, (p, h) in blocks.items() if h == 1))\nresult",
  # an immediate lambda whose body is a tuple of side effects ending in [-1], or that takes a lambda as an argument: written by hand, the result is checked by the caller
    "(lambda d, s: d(s.pack('<I', 1) + bytes(32) + bytes.fromhex('4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b')[::-1] + s.pack('<III', 1231006505, 0x1d00ffff, 2083236893))[::-1].hex())(lambda b: __import__('hashlib').sha256(__import__('hashlib').sha256(b).digest()).digest(), __import__('struct'))":
    "import hashlib\nimport struct\ndef d(b):\n    return hashlib.sha256(hashlib.sha256(b).digest()).digest()\ns = struct\nd(s.pack('<I', 1) + bytes(32) + bytes.fromhex('4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b')[::-1] + s.pack('<III', 1231006505, 0x1d00ffff, 2083236893))[::-1].hex()",
    "(lambda d: (lambda L: d(d(L[0] + L[1]) + d(L[2] + L[3])).hex()[:16])([d(x) for x in (b'A', b'B', b'C', b'D')]))(lambda b: __import__('hashlib').sha256(__import__('hashlib').sha256(b).digest()).digest())":
    "import hashlib\ndef d(b):\n    return hashlib.sha256(hashlib.sha256(b).digest()).digest()\nL = [d(x) for x in (b'A', b'B', b'C', b'D')]\nd(d(L[0] + L[1]) + d(L[2] + L[3])).hex()[:16]",
    "(lambda chains: max(chains, key=lambda c: sum(chains[c])))({'A': [100, 100, 100], 'B': [100, 100, 120]})":
    "chains = {'A': [100, 100, 100], 'B': [100, 100, 120]}\ndef work(c):\n    return sum(chains[c])\nmax(chains, key=work)",
    "(lambda h, a, b: sum(bin(x ^ y).count('1') for x, y in zip(h(a), h(b))))(lambda m: __import__('hashlib').sha256(m).digest(), b'pay Bob 1 BTC', b'pay Bob 2 BTC')":
    "import hashlib\ndef h(m):\n    return hashlib.sha256(m).digest()\na = b'pay Bob 1 BTC'\nb = b'pay Bob 2 BTC'\nsum(bin(x ^ y).count('1') for x, y in zip(h(a), h(b)))",
    "(lambda m, q, z: (lambda p: (lambda l: round(1 - sum(m.exp(-l) * l**k / m.factorial(k) * (1 - (q / p)**(z - k)) for k in range(z + 1)), 7))(z * q / p))(1 - q))(__import__('math'), 0.1, 6)":
    'import math\nq = 0.1\nz = 6\np = 1 - q\nl = z * q / p\nround(1 - sum(math.exp(-l) * l**k / math.factorial(k) * (1 - (q / p)**(z - k)) for k in range(z + 1)), 7)',
    "(lambda record: (record['Alice'], record.pop('Alice'), record.update({'Bob': 100000}), record)[-1])({'Alice': 100000})":
    "record = {'Alice': 100000}\nrecord.pop('Alice')\nrecord.update({'Bob': 100000})\nrecord"}
# chapter 4 (v1_5_0): the immediate lambdas that nest other lambdas, written by hand
MANUAL.update({
    '(lambda a, b, p: (lambda m: (lambda x: (x, (m * (a[0] - x) - a[1]) % p))((m * m - a[0] - b[0]) % p))((b[1] - a[1]) * pow(b[0] - a[0], -1, p) % p))((1, 5), (2, 7), 17)':
    'a = (1, 5)\nb = (2, 7)\np = 17\nm = (b[1] - a[1]) * pow(b[0] - a[0], -1, p) % p\nx = (m * m - a[0] - b[0]) % p\n(x, (m * (a[0] - x) - a[1]) % p)',
    "(lambda h, d: (lambda n: ''.join('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'[n // 58 ** i % 58] for i in range(60)[::-1]).lstrip('1'))(int.from_bytes(d + h(h(d).digest()).digest()[:4], 'big')))(__import__('hashlib').sha256, bytes.fromhex('801E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD'))":
    "import hashlib\nh = hashlib.sha256\nd = bytes.fromhex('801E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD')\nn = int.from_bytes(d + h(h(d).digest()).digest()[:4], 'big')\n''.join('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'[n // 58 ** i % 58] for i in range(60)[::-1]).lstrip('1')",
    "(lambda B58, h, payload: tuple((lambda p: (lambda full: '1' * (len(full) - len(full.lstrip(bytes([0])))) + (lambda n: ''.join(B58[n // 58 ** i % 58] for i in range(40)[::-1]).lstrip('1'))(int.from_bytes(full, 'big')))(p + h(h(p).digest()).digest()[:4]))(bytes([v]) + payload)[0] for v in (0x00, 0x05, 0x6f)))('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', __import__('hashlib').sha256, bytes.fromhex('bbc1e42a39d05a4cc61752d6963b7f69d09bb27b'))":
    "import hashlib\nB58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\nh = hashlib.sha256\npayload = bytes.fromhex('bbc1e42a39d05a4cc61752d6963b7f69d09bb27b')\ndef encode(v):\n    p = bytes([v]) + payload\n    full = p + h(h(p).digest()).digest()[:4]\n    n = int.from_bytes(full, 'big')\n    digits = ''.join(B58[n // 58 ** i % 58] for i in range(40)[::-1]).lstrip('1')\n    return '1' * (len(full) - len(full.lstrip(bytes([0])))) + digits\ntuple(encode(v)[0] for v in (0x00, 0x05, 0x6f))",
    "(lambda B58, a: (lambda n: (n.to_bytes(25, 'big')[0], len(n.to_bytes(25, 'big'))))(sum(B58.index(c) * 58 ** i for i, c in enumerate(a[::-1]))))('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', '1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy')":
    "B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\na = '1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy'\nn = sum(B58.index(c) * 58 ** i for i, c in enumerate(a[::-1]))\n(n.to_bytes(25, 'big')[0], len(n.to_bytes(25, 'big')))",
    "(lambda a: (lambda n: n.to_bytes(25, 'big')[0])(sum('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'.index(c) * 58 ** i for i, c in enumerate(a[::-1]))))('3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM')":
    "a = '3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM'\nn = sum('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'.index(c) * 58 ** i for i, c in enumerate(a[::-1]))\nn.to_bytes(25, 'big')[0]",
    "(lambda sha: (lambda nowit, wit: (sha(sha(nowit).digest()).hexdigest()[:8], sha(sha(nowit + wit).digest()).hexdigest()[:8]))(b'the bytes of a transaction without its witness', b' and the witness bytes'))(__import__('hashlib').sha256)":
    "import hashlib\nsha = hashlib.sha256\nnowit = b'the bytes of a transaction without its witness'\nwit = b' and the witness bytes'\n(sha(sha(nowit).digest()).hexdigest()[:8], sha(sha(nowit + wit).digest()).hexdigest()[:8])",
})
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
