#!/usr/bin/env python3
"""sen0401_deck_code_read v1.0.0 (task TK_Deck_Checks_Build) - the shared reader of the four deck checks (indentation, lambda, label words, prompts). It finds the code boxes of a deck in BOTH forms
by the marker of sen0401_code_marker_v1_0_0.py: a text shape with a paragraph that starts with '>>> ' (form 'prompt'), or a text shape whose name starts with 'code' (form 'shape').
A code box of the prompt form has as code lines its input rows (a '>>> ' or '... ' row, prompt stripped); the other rows are results. A code box of the shape form has every line as a code line.
Nothing here judges; it only reads. The checks that use it are new files; no committed file is edited."""
__version__ = "1.0.0"
import os, re, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_code_marker_v1_0_0 as MARK
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

KEYWORDS = re.compile(r"^\s*(if|elif|else|for|while|def|class|with|try|except|finally|async\s+def|async\s+for|async\s+with|match|case)\b")
ONE_LINE_KEYWORDS = re.compile(r"^\s*(for|while|if|elif|else|def|class|with|try|except|finally)\b[^#]*:\s*\S")   # the measure's own rule (sen0401_deck_teach_measure_v1_0_0.py)
LABEL = re.compile(r"^\s*(WHAT|WHO|WHEN|WHERE|WHY|HOW)\s*[:\-–—]", re.I)                                 # the measure's own rule


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from walk(sh.shapes)
        else:
            yield sh


def lines_of(sh):
    out = []
    for p in sh.text_frame.paragraphs:
        out.extend(re.split(r"[\n\x0b]", "".join(r.text for r in p.runs) if p.runs else p.text))
    return out


def one_line_compound(l):
    """a for/while/if/... header with its body on the same line (colon outside brackets and strings followed by text); the measure's rule"""
    if not ONE_LINE_KEYWORDS.match(l):
        return False
    head = l.split("#")[0]
    depth = 0; q = None
    for i, c in enumerate(head):
        if q:
            if c == q:
                q = None
        elif c in "'\"":
            q = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == ":" and depth == 0 and head[i + 1:].strip():
            return True
    return False


def slide_title(slide):
    for sh in walk(slide.shapes):
        if sh.has_text_frame:
            t = sh.text_frame.text.strip()
            if t and t != "₿" and not re.fullmatch(r"\d+\s*/\s*\d+", t):
                return t
    return ""


def code_boxes(slide):
    """[{'name', 'form', 'lines': [(text, is_prompt_row)], 'raw': [all lines]}] of one slide, in shape order"""
    out = []
    for sh in walk(slide.shapes):
        if not sh.has_text_frame or not sh.text_frame.text.strip():
            continue
        raw = lines_of(sh)
        has_prompt = any(l.startswith(MARK.PROMPT_INPUT) for l in raw)
        if not has_prompt and not MARK.is_code_name(sh.name):
            continue
        if has_prompt:
            lines = []
            for l in raw:
                if l.startswith(MARK.PROMPT_INPUT) or l.startswith(MARK.PROMPT_MORE):
                    lines.append((l[4:], True))
                elif l.strip() in (">>>", "..."):
                    lines.append(("", True))
            out.append({"name": sh.name, "form": "prompt", "lines": lines, "raw": raw})
        else:
            out.append({"name": sh.name, "form": "shape", "lines": [(l, False) for l in raw], "raw": raw})
    return out


def decks_slides(path):
    return list(Presentation(path).slides)


def strip_code(line):
    """the line without string contents and comment (for word searches)"""
    out, q = [], None
    for c in line:
        if q:
            if c == q:
                q = None
            continue
        if c in "'\"":
            q = c; continue
        if c == "#":
            break
        out.append(c)
    return "".join(out)


def indent_findings(lines):
    """lines: list of code line strings (one listing). Returns (findings [(line number from 1, reason)], one_line_compounds, indented_lines)."""
    findings = []; depth = 0; triple = None; cont = False; pending = None; logical_indent = 0
    for no, raw in enumerate(lines, 1):
        line = raw.replace("\t", "    ")
        stripped = line.strip()
        start_of_logical = depth == 0 and triple is None and not cont
        indent = len(line) - len(line.lstrip(" "))
        if triple is None and stripped and not stripped.startswith("#"):
            if start_of_logical:
                if pending is not None:
                    if indent <= pending:
                        findings.append((no, "the body of the header above is not indented: %s" % stripped[:70]))
                    elif indent != pending + 4:
                        findings.append((no, "the body is indented %d spaces more than its header, not 4: %s" % (indent - pending, stripped[:70])))
                    pending = None
                logical_indent = indent
                if one_line_compound(line):
                    findings.append((no, "a body stands on the header line: %s" % stripped[:70]))
            elif depth > 0 and not cont:
                if indent <= logical_indent and stripped[0] not in ")]}":
                    findings.append((no, "a continuation line inside brackets is not indented: %s" % stripped[:70]))
        # scan the characters of the line
        i, n = 0, len(line); ends_colon_ok = False; code_part_end = n
        while i < n:
            c = line[i]
            if triple:
                if line.startswith(triple, i):
                    i += 3; triple = None; continue
                i += 1; continue
            if c == "#":
                code_part_end = i; break
            if c in "'\"":
                if line.startswith(c * 3, i):
                    triple = c * 3; i += 3; continue
                j = i + 1
                while j < n and line[j] != c:
                    j += 2 if line[j] == "\\" else 1
                i = j + 1; continue
            if c in "([{":
                depth += 1
            elif c in ")]}":
                depth = max(0, depth - 1)
            i += 1
        cont = line.rstrip().endswith("\\") and triple is None
        if triple is None and depth == 0 and stripped and not stripped.startswith("#"):
            code = line[:code_part_end].rstrip()
            if code.endswith(":") and KEYWORDS.match(code) and start_of_logical:
                pending = indent
    if pending is not None:
        findings.append((len(lines), "a header ends the listing without a body"))
    nonblank = [l for l in lines if l.strip()]
    return findings, sum(1 for l in nonblank if one_line_compound(l)), sum(1 for l in nonblank if l[:1] in " \t")
