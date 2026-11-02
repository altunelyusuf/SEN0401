#!/usr/bin/env python3
"""SEN0401 mock bank checker for the chapter 3 extra family 'release_tags', v1.0.2. Holds no question text: it reads the bank file given.
It recomputes every key independently (its own parser and sorter, separate from the generator), checks schema, counts, word limits,
list variety and the fixed why_question line, and re-runs the generator to compare the file byte for byte.
Usage:  check --bank FILE --gen GENERATOR.py     |     selftest --bank FILE --gen GENERATOR.py  (three planted defects must each FAIL)"""
import argparse, copy, hashlib, json, os, re, subprocess, sys, tempfile, itertools
sys.dont_write_bytecode = True
WHY_SHA256 = "12783f630cabc79c2a04458cb36cda8d661b4ad92b171dd86ca06aebfa7d829a"   # the fixed why_question line is compared by hash (the line itself stays private)
BANNED_FILE = "/home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts/mock_banned_ch3x_v1_0_2.txt"   # private; one phrase per line
try:
    BANNED = [l.strip() for l in open(BANNED_FILE, encoding="utf-8") if l.strip()]
except OSError:
    BANNED = []
    print("NOTE banned-wording rule NOT_MEASURED: private phrase file not readable", file=sys.stderr)


def nw(t): return len(str(t).split())


def tags_of(stem):
    m = re.match(r"Release tags: (.*?)\. Text order", stem)
    return [x.strip() for x in m.group(1).split(",")] if m else []


def recompute(tid, stem, tags):
    """Independent recomputation of the key from the tag list (and the named tag in the stem)."""
    num = sorted(tags, key=lambda t: tuple(int(x) for x in t[1:].split(".")))
    txt = sorted(tags)
    pt = {t: i + 1 for i, t in enumerate(txt)}; pn = {t: i + 1 for i, t in enumerate(num)}
    mv = {t: abs(pt[t] - pn[t]) for t in tags}
    named = re.search(r"(?:move of|place of) (v\d+\.\d+)", stem)
    named = named.group(1) if named else None
    if tid == "n3x_1": return sum(mv.values())
    if tid == "n3x_2": return mv[named]
    if tid == "n3x_3": return sum(1 for t in tags if mv[t])
    if tid == "n3x_4": return pt[named]
    if tid == "n3x_5": return max(mv.values())
    if tid == "n3x_6": return sum(1 for a, b in itertools.combinations(tags, 2) if (pt[a] < pt[b]) != (pn[a] < pn[b]))
    if tid == "n3x_7": return pt[num[0]]
    if tid == "n3x_8": return sum(1 for t in tags if not mv[t])
    return None


def check_bank(d, genfile=None, bank_path=None):
    errs = []
    def bad(m): errs.append(m)
    if d.get("chapter") != 3 or d.get("family") != "release_tags": bad("header")
    its = d.get("items", [])
    if len(its) < 6: bad("fewer than 6 templates")
    if sum(1 for i in its if i.get("can_be_4")) != 1: bad("can_be_4 not on exactly one template")
    seen_sets, seen_stems, total = set(), set(), 0
    for it in its:
        tid = it.get("id", "?")
        if not re.fullmatch(r"n3x_\d+", tid) or it.get("type") != "numeric" or it.get("chapter") != 3 or it.get("points") != 3: bad(tid + ": id/type/chapter/points")
        if hashlib.sha256(str(it.get("why_question")).encode()).hexdigest() != WHY_SHA256: bad(tid + ": why_question differs from the fixed line")
        tip = it.get("tip", "")
        if nw(tip) > 12 or tip.lower().startswith("tip") or not tip: bad(tid + ": tip")
        if not it.get("unit"): bad(tid + ": unit")
        ins = it.get("instances", [])
        if len(ins) < 8: bad(tid + ": fewer than 8 instances")
        if len({x.get("key_value") for x in ins}) < 8: bad(tid + ": fewer than 8 distinct key values")
        for k, x in enumerate(ins):
            w = "%s[%d]" % (tid, k); total += 1
            st = x.get("stem", "")
            if nw(st) > 60: bad(w + ": stem over 60 words")
            last = re.split(r"(?<=[.?!])\s+", st.strip())[-1]
            if not last.startswith("You are asked to"): bad(w + ": last sentence")
            for b in BANNED:
                if b.lower() in st.lower() or b.lower() in tip.lower(): bad(w + ": banned wording")
            tg = tags_of(st)
            if not (4 <= len(tg) <= 9) or len(set(tg)) != len(tg) or not all(re.fullmatch(r"v\d+\.\d+", t) for t in tg): bad(w + ": tag list"); continue
            fs = frozenset(tg)
            if fs in seen_sets: bad(w + ": list reused")
            seen_sets.add(fs)
            if st in seen_stems: bad(w + ": stem reused")
            seen_stems.add(st)
            if sorted(tg) == sorted(tg, key=lambda t: tuple(int(y) for y in t[1:].split("."))): bad(w + ": the two orders do not differ")
            kv = x.get("key_value")
            if not isinstance(kv, int) or isinstance(kv, bool) or not (0 <= kv <= 99999): bad(w + ": key_value range"); continue
            if recompute(tid, st, tg) != kv: bad(w + ": key_value %s differs from recomputed %s" % (kv, recompute(tid, st, tg)))
            if len(x.get("steps", [])) < 2 or not all(re.search(r"\d", s) for s in x["steps"][2:]): bad(w + ": steps")
            if not x.get("why_right"): bad(w + ": why_right")
            cw = x.get("common_wrong", [])
            vals = [c.get("value") for c in cw]
            if len(cw) != 3 or len(set(vals)) != 3 or kv in vals or not all(isinstance(v, int) and 0 <= v <= 99999 for v in vals) or not all(c.get("why") for c in cw): bad(w + ": common_wrong")
            if re.search(r"\b(e\.g\.|i\.e\.|vs\.?|approx)\b", st): bad(w + ": abbreviation")
    if total < 48: bad("fewer than 48 instances")
    if genfile and bank_path is not None:
        with tempfile.TemporaryDirectory() as td:
            o = os.path.join(td, "g.json")
            subprocess.run([sys.executable, "-I", genfile, "--out", o], check=True, capture_output=True)
            if open(o, "rb").read() != open(bank_path, "rb").read(): bad("generator re-run differs from the file")
    return errs, total


def planted(d, n):
    c = copy.deepcopy(d)
    if n == 1: c["items"][0]["instances"][0]["key_value"] += 1
    elif n == 2: c["items"][1]["instances"][2]["stem"] = c["items"][1]["instances"][2]["stem"].replace("You are asked to", "Please")
    elif n == 4:
        ins = c["items"][3]["instances"]; ins[1]["key_value"] = ins[0]["key_value"]; ins[2]["key_value"] = ins[0]["key_value"]; ins[3]["key_value"] = ins[0]["key_value"]
    else: c["items"][2]["instances"][1]["stem"] = c["items"][2]["instances"][0]["stem"]
    return c


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=["check", "selftest"])
    ap.add_argument("--bank", required=True); ap.add_argument("--gen")
    a = ap.parse_args()
    d = json.load(open(a.bank, encoding="utf-8"))
    errs, total = check_bank(d, a.gen, a.bank)
    print("clean bank: %d templates, %d instances, %d failure(s)" % (len(d["items"]), total, len(errs)))
    for e in errs: print("  FAIL", e)
    if a.mode == "check": sys.exit(1 if errs else 0)
    ok = not errs
    for n, nm in ((1, "wrong key value"), (2, "stem without the ask phrase"), (3, "repeated list"), (4, "four instances share one key value")):
        e, _ = check_bank(planted(d, n))
        print("planted defect %d (%s): %s (%d failure(s))" % (n, nm, "FAILS as required" if e else "NOT CAUGHT", len(e)))
        for x in e[:3]: print("    ", x)
        ok = ok and bool(e)
    print("SELFTEST", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
