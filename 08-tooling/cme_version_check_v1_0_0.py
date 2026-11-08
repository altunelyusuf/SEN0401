#!/usr/bin/env python3
"""cme_version_check v1.0.0 - a course material file's version continues from its own predecessor, with a step sized by the change.

The rule (the OEE rule on the size of a version bump, applied to course material files): in one series - one chapter, one kind of file
(deck, page, document) - the newest file's version is its predecessor's plus ONE step, and the step is the size of the change:
  patch  a.b.c -> a.b.c+1      the file says and demands the same (a wording, a value corrected)
  minor  a.b.c -> a.b+1.0      something added, nothing taken away
  major  a.b.c -> a+1.0.0      something a user relied on removed, renamed or changed in meaning
A number reached by another file's release, or any jump that is not one such step, is refused. A released file is never renumbered, so the
rule is read for a series from its baseline (the version a series held when the rule began) onward; earlier gaps are history, reported and not failed.

The tool compares two files side by side, which no shape on one file can do (the OEE rule says so). It only reads.

Usage:
  cme_version_check.py <course-repo> [--baseline FILE.json] [--declare 03-materials/ch07/page=minor ...] [--write-baseline FILE.json]
  --write-baseline  records each series' newest version now (the point from which the rule binds)
  --declare         DIR=size: the size the releasing agent declares for the newest file in that directory; it must equal the size the version step shows.
                    Whether the declared size matches the change itself is read by the independent reviewer of the release; no tool can see the change
Exit code 0 when no series fails, 1 otherwise."""
__version__ = "1.0.0"
import argparse, json, os, re, sys

KINDS = {
    "deck": re.compile(r"^(?P<stem>.+?)_v(?P<v>\d+_\d+_\d+)\.pptx$"),
    "page": re.compile(r"^(?P<stem>.+?_page)_v(?P<v>\d+_\d+_\d+)\.html$"),
    "document": re.compile(r"^(?P<stem>.+?_document)_v(?P<v>\d+_\d+_\d+)\.docx$"),
}


def parse(v):
    return tuple(int(x) for x in v.split("_"))


def step(prev, new):
    """the size of the step from prev to new, or None when it is not one single step"""
    (a, b, c), (x, y, z) = prev, new
    if (x, y, z) == (a, b, c + 1):
        return "patch"
    if (x, y, z) == (a, b + 1, 0):
        return "minor"
    if (x, y, z) == (a + 1, 0, 0):
        return "major"
    return None


def series(root):
    """{(directory, kind, stem): [versions ascending]} over the course materials"""
    out = {}
    for d, _, files in os.walk(os.path.join(root, "03-materials")):
        for f in files:
            for kind, rx in KINDS.items():
                m = rx.match(f)
                if m:
                    out.setdefault((os.path.relpath(d, root), kind, m.group("stem")), []).append(parse(m.group("v")))
    return {k: sorted(set(v)) for k, v in out.items()}


def key(k):
    return f"{k[0]}|{k[1]}|{k[2]}"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--baseline")
    ap.add_argument("--write-baseline")
    ap.add_argument("--declare", action="append", default=[])
    a = ap.parse_args(argv)
    ser = series(a.repo)
    if a.write_baseline:
        json.dump({key(k): ".".join(map(str, v[-1])) for k, v in sorted(ser.items())}, open(a.write_baseline, "w"), indent=1)
        print(f"baseline written: {len(ser)} series -> {a.write_baseline}")
        return 0
    base = json.load(open(a.baseline)) if a.baseline else {}
    declared = dict(d.split("=", 1) for d in a.declare)
    fails, history, ok = [], 0, 0
    for k, vs in sorted(ser.items()):
        b = base.get(key(k))
        bv = tuple(int(x) for x in b.split(".")) if b else None
        after = [v for v in vs if bv is None or v > bv]
        prev = bv if bv else (vs[0] if vs else None)
        chain = [prev] + after if bv else vs
        for p, n in zip(chain, chain[1:]):
            s = step(p, n)
            if s is None:
                if bv is None:
                    history += 1  # no baseline: history, reported
                else:
                    fails.append(f"{key(k)}: {'.'.join(map(str,p))} -> {'.'.join(map(str,n))} is not one step of its own")
        if bv and after:
            s = step(chain[-2], chain[-1])
            want = declared.get(k[0])
            if want and s and want != s:
                fails.append(f"{key(k)}: declared {want} but the version step is {s}")
            if s:
                ok += 1
    print(f"series {len(ser)}; steps in history that are not one step of their own (reported, not failed): {history}; series passing since baseline: {ok}")
    for f in fails:
        print("FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
