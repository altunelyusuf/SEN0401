#!/usr/bin/env python3
"""Shared helpers for the SEN0401 lecture decks of chapters 1 to 3.

Three jobs, none of which may invent anything:

* `recast` turns a chapter corpus's worked example - written as one expression so that the interactive
  page can run it - into the readable console rows a slide shows, keeping the author's own spelling of
  every literal (0x1d00ffff stays hexadecimal, 100_000 keeps its separators) by cutting source segments
  out of the original text rather than re-printing the parsed tree. An example whose program needs an
  indented block becomes a block instead of rows, and the deck shows the program verbatim.
* `sentences` / `take` cut a corpus paragraph down to the opening sentences that fit a slide, whole
  sentences only, so that what the slide says is what the chapter says.
* `fits` / `wrap_lines` estimate how many lines a string occupies in a box of a given width at a given
  point size, so that the plan builder can refuse a slide whose text would overflow its frame.

Nothing here reads the network and nothing here decides a fact: the facts come from the chapter corpus
and from the executed examples.
"""
__version__ = "1.0.0"

import ast
import re

# ----------------------------------------------------------------------------------------------------
# 1. recasting a worked example
# ----------------------------------------------------------------------------------------------------

MAXSTR = 90          # a string literal longer than this is hoisted into the chapter prelude under a name

_IMPORT = re.compile(r"__import__\('([A-Za-z0-9_.]+)'(?:, fromlist=\[[^\]]*\])?\)")


def fix_imports(src, imports):
    """`__import__('hashlib').sha256(...)` reads badly on a slide; turn it into a plain module use and
    record the import so that the prelude can carry it."""
    def repl(m):
        full = m.group(1)
        imports.add(full)
        return full if "fromlist" in m.group(0) else full.split(".")[0]
    return _IMPORT.sub(repl, src)


class Block(Exception):
    """Raised when an example's program contains an indented block and cannot become console rows."""

    def __init__(self, text):
        super().__init__(text)
        self.text = text


def _exec_body(node):
    """`(lambda g: (exec(BODY, g), g['result'])[1])({})` -> BODY, the program the corpus really runs."""
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Lambda)):
        return None
    lam = node.func
    if len(lam.args.args) != 1 or lam.args.args[0].arg != "g":
        return None
    body = lam.body
    if not (isinstance(body, ast.Subscript) and isinstance(body.value, ast.Tuple)):
        return None
    first = body.value.elts[0]
    if not (isinstance(first, ast.Call) and isinstance(first.func, ast.Name) and first.func.id == "exec"):
        return None
    arg = first.args[0]
    return arg.value if isinstance(arg, ast.Constant) and isinstance(arg.value, str) else None


def _lambda_call(node):
    """`(lambda a, b: EXPR)(x, y)` -> the argument names, the argument nodes and the body node."""
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Lambda)):
        return None
    lam = node.func
    if lam.args.kwonlyargs or lam.args.vararg or node.keywords:
        return None
    names = [a.arg for a in lam.args.args]
    if len(names) != len(node.args) or not names:
        return None
    return names, node.args, lam.body


def expand(src, depth=0):
    """One expression -> (the rows that set things up, the row whose value is shown)."""
    node = ast.parse(src, mode="eval").body
    body = _exec_body(node)
    if body is not None:
        lines = [l.rstrip() for l in body.strip("\n").split("\n") if l.strip()]
        if any(l[:1] in (" ", "\t") for l in lines):
            raise Block("\n".join(lines))
        if re.match(r"^result\s*=\s*", lines[-1]):
            lines = lines[:-1] + [re.sub(r"^result\s*=\s*", "", lines[-1])]
        else:
            lines = lines + ["result"]
        return lines[:-1], lines[-1]
    call = _lambda_call(node)
    if call is not None and depth < 4:
        names, args, inner = call
        pre = ["%s = %s" % (", ".join(names), ", ".join(ast.get_source_segment(src, a) for a in args))]
        sub, final = expand(ast.get_source_segment(src, inner), depth + 1)
        return pre + sub, final
    return [], src.strip()


def hoist(line, prefix, prelude):
    """Move a long string literal out of a row and into the prelude, so the slide shows a name."""
    try:
        tree = ast.parse(line)
    except SyntaxError:
        return line
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) > MAXSTR:
            seg = ast.get_source_segment(line, node)
            if seg:
                found.append(seg)
    for seg in sorted(set(found), key=len, reverse=True):
        name = next((k for k, v in prelude.items() if v == seg), None)
        if name is None:
            name = "%s_D%d" % (prefix, sum(1 for k in prelude if k.startswith(prefix + "_D")) + 1)
            prelude[name] = seg
        line = line.replace(seg, name)
    return line


def recast(expr, prefix, prelude):
    """A corpus worked example -> {'kind': 'rows'|'block', ...} for the deck to show."""
    imports = set()
    try:
        pre, final = expand(expr)
        rows = [hoist(fix_imports(r, imports), prefix, prelude) for r in pre + [final]]
        return {"kind": "rows", "rows": rows, "imports": sorted(imports)}
    except Block as blk:
        text = "\n".join(hoist(fix_imports(l, imports), prefix, prelude) for l in blk.text.split("\n"))
        if not re.search(r"^result\s*=", text, re.M):
            text += "\nresult = None"
        return {"kind": "block", "text": text, "imports": sorted(imports)}


# ----------------------------------------------------------------------------------------------------
# 2. cutting a paragraph down to what a slide can hold
# ----------------------------------------------------------------------------------------------------

_ABBREVIATION = ("e.g.", "i.e.", "etc.", "cf.", "vs.", "Mr.", "Dr.", "No.", "ch.", "ed.", "approx.")


def sentences(text):
    """Split continuous prose into sentences, leaving decimal points and abbreviations alone."""
    text = " ".join(text.split())
    out, buf, i = [], "", 0
    while i < len(text):
        buf += text[i]
        if text[i] in ".!?":
            if any(buf.rstrip().endswith(a) for a in _ABBREVIATION):
                i += 1
                continue
            nxt = text[i + 1:i + 3]
            if nxt[:1] == " " and (nxt[1:2].isupper() or nxt[1:2] in "“\"'"):
                out.append(buf.strip())
                buf = ""
                i += 2
                continue
            if i == len(text) - 1:
                out.append(buf.strip())
                buf = ""
                i += 1
                continue
        i += 1
    if buf.strip():
        out.append(buf.strip())
    return out


def take(text, max_chars, min_sentences=1):
    """The opening sentences of a paragraph, whole, up to a character budget."""
    out = []
    for sentence in sentences(text):
        if out and len(" ".join(out)) + 1 + len(sentence) > max_chars and len(out) >= min_sentences:
            break
        out.append(sentence)
        if len(" ".join(out)) > max_chars and len(out) >= min_sentences:
            break
    return " ".join(out)


def facet(paras, name):
    """The paragraph written under one facet of a concept ('What it is', 'Watch out', ...)."""
    for f, t in paras:
        if f.lower().startswith(name.lower()):
            return t
    return ""


# ----------------------------------------------------------------------------------------------------
# 3. will it fit?
# ----------------------------------------------------------------------------------------------------

# average advance width as a fraction of the point size, measured conservatively (wider than the fonts
# really are, so the estimate errs towards refusing a slide rather than letting it overflow)
WIDTH = {"Calibri": 0.50, "Cambria": 0.53, "Courier New": 0.60}
LINE = 1.22                       # line height as a multiple of the point size


def chars_per_line(width_in, size_pt, font="Calibri"):
    return max(1, int(width_in * 72.0 / (size_pt * WIDTH[font])))


def wrap_lines(text, width_in, size_pt, font="Calibri"):
    """How many lines the text takes in a box that wide, breaking at spaces as a renderer does."""
    per = chars_per_line(width_in, size_pt, font)
    total = 0
    for para in str(text).split("\n"):
        if not para:
            total += 1
            continue
        line = 0
        for word in para.split(" "):
            need = len(word) if line == 0 else line + 1 + len(word)
            if need <= per:
                line = need
            else:
                total += 1
                line = len(word)
                while line > per:          # a single word longer than the line (a hash, a long call)
                    total += 1
                    line -= per
        total += 1
    return total


def text_height(text, width_in, size_pt, font="Calibri"):
    return wrap_lines(text, width_in, size_pt, font) * size_pt * LINE / 72.0


def fits(text, width_in, height_in, size_pt, font="Calibri"):
    return text_height(text, width_in, size_pt, font) <= height_in
