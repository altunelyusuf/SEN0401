"""Rewrites a Python expression so that it contains no double quote character, with the same value.
Why: the generic builder (sen0401_rdodi_build_v1_1_0.py) rewrites every double quote of an example's code to a single quote in the ABox literal,
which turns valid code into invalid code. Every string literal that holds or is delimited by a double quote becomes a join of quote-free pieces,
the quote characters coming from chr(34) and chr(39). Other tokens are left as they are."""
__version__ = "1.0.0"
import io, tokenize, ast


def noquote(expr):
    out, last = [], (1, 0)
    lines = expr.split("\n")
    assert len(lines) == 1, "one-line expressions only"
    toks = list(tokenize.generate_tokens(io.StringIO(expr).readline))
    pos = 0
    res = ""
    for t in toks:
        if t.type == tokenize.STRING and '"' in t.string:
            val = ast.literal_eval(t.string)
            assert isinstance(val, str)
            parts, cur = [], ""
            for ch in val:
                if ch in "\"'":
                    if cur:
                        parts.append(repr(cur)); cur = ""
                    parts.append("chr(%d)" % ord(ch))
                else:
                    cur += ch
            if cur or not parts:
                parts.append(repr(cur))
            res += expr[pos:t.start[1]] + "(" + " + ".join(parts) + ")"
            pos = t.end[1]
    res += expr[pos:]
    assert '"' not in res, res
    return res
