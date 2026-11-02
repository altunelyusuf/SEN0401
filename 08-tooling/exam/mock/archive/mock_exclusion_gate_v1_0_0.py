#!/usr/bin/env python3
"""SEN0401 mock exclusion gate v1.0.0 - a mock item passes only when it is NEW against the private index of every delivered item.
Usage: mock_exclusion_gate_v1_0_0.py --selftest | --bank FILE.json [FILE2.json ..] | --html FILE.html [..]
The index is read from the private CME path. The log prints ids, scores and counts, never item text.
Rules (plan, 'NEW items only'):
 (a) token 5-gram Jaccard of the stem with every indexed stem < 0.35 AND word-level sequence ratio < 0.60 (each taken as the max of the raw and the number-masked reading);
     the same 5-gram containment of the stem in each whole delivered document must be < 0.35;
 (b) no option / premise / response / step / bank entry / fill sentence (3 tokens or more) equals an indexed one (normalised);
 (c) numeric: key_value with the same unit is not an indexed key value of a stem with similarity > 0.30."""
import json, os, sys, re, copy, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_exclusion_lib_v1_0_0 import *

EXAM = "/home/claude/CME/exams/SEN0401/08-tooling/exam"
INDEX = EXAM + "/mock/exclusion/sen0401_mock_exclusion_index_v1_0_0.json"

class Gate:
    def __init__(self, path=INDEX):
        d = json.load(open(path))
        self.stems = []
        for s in d["stems"]:
            t = drop_fixed(s["t"]).split()
            m = ["#" if w.isdigit() else w for w in t]
            self.stems.append((s["id"], t, m, grams(t), grams(m)))
        self.opts = {o["t"]: o["id"] for o in d["options"]}
        self.nums = d["numeric"]
        self.sigs = {tuple(x["sig"]): x["id"] for x in d.get("sigs", [])}
        self.taglists = {tuple(x["tags"]): x["id"] for x in d.get("taglists", [])}
        for n in self.nums:
            t = n["stem"].split(); m = ["#" if w.isdigit() else w for w in t]
            n["_g"], n["_gm"] = grams(t), grams(m)
        self.docs = {}
        for name, lst in d["documents"].items():
            raw = {tuple(x.split(" ")) for x in lst}
            msk = {tuple("#" if w.isdigit() else w for w in g) for g in raw}
            self.docs[name] = (raw, msk)

    def stem_check(self, text):
        t = toks(text); m = toks(text, mask=True)
        g, gm = grams(t), grams(m)
        best = (0.0, None); bestw = (0.0, None)
        for iid, it, im, ig, igm in self.stems:
            j = max(jacc(g, ig), jacc(gm, igm))
            if j > best[0]:
                best = (j, iid)
            if ratio_upper(m, im) >= 0.5:
                w = max(seqratio(t, it), seqratio(m, im))
                if w > bestw[0]:
                    bestw = (w, iid)
        dbest = (0.0, None)
        for name, (raw, msk) in self.docs.items():
            if not g:
                continue
            c = max(len(g & raw), len(gm & msk)) / len(g)
            if c > dbest[0]:
                dbest = (c, name)
        return {"g5": best, "word": bestw, "doc": dbest}

    def opt_check(self, text):
        t = drop_fixed(text)
        if len(t.split()) < MIN_OPT_TOKENS:
            return None
        return self.opts.get(t)

    def family_check(self, stem, value):
        """family numeric rule (addenda E8/E9): fails when (1) the key equals an indexed real key and the stem has 5-gram containment above 0.2
        with the stem of that real item, (2) the sequence of numbers of the stem (4 or more) equals the one of an indexed stem
        (bit count, accepted results, speed, tags...), (3) the list of version tags (3 or more) equals an indexed list. returns reasons"""
        t = toks(stem); m = toks(stem, mask=True); g, gm = grams(t), grams(m)
        out = []
        for n in self.nums:
            if n["value"] == int(value):
                c = max(len(g & n["_g"]), len(gm & n["_gm"])) / max(1, len(g))
                if c > 0.2:
                    out.append("c3:key-equals-%s+containment%.2f" % (n["id"], c))
        ns = tuple(re.findall(r"\d+", stem))
        if len(ns) >= 4 and ns in self.sigs:
            out.append("c2:number-sequence-equals-%s" % self.sigs[ns])
        tg = tuple(re.findall(r"v\d+(?:\.\d+)+", stem))
        if len(tg) >= 3 and tg in self.taglists:
            out.append("c4:tag-list-equals-%s" % self.taglists[tg])
        return out

    def num_check(self, stem, value, unit):
        t = toks(stem); m = toks(stem, mask=True); g, gm = grams(t), grams(m)
        u = norm(unit)
        hits = []
        for n in self.nums:
            if n["value"] == int(value) and n["unit"] == u:
                s = max(jacc(g, n["_g"]), jacc(gm, n["_gm"]))
                if s > THRESH_NUM_SIM:
                    hits.append((n["id"], round(s, 3)))
        return hits

def item_texts(it):
    """returns (stems, option_like, numeric_list)"""
    ty = it.get("type")
    stems, opts, nums = [], [], []
    if ty == "choice":
        stems.append(it["stem"]); opts += it["options"]
    elif ty == "numeric":
        for k, ins in enumerate(it["instances"]):
            nums.append((it["id"] + "#i%d" % k, ins["stem"], ins["key_value"], it.get("unit", "")))
            stems.append(ins["stem"])
    elif ty == "matching":
        stems.append(it["intro"]); opts += it["premises"] + it["responses"]
    elif ty == "ordering":
        stems.append(it["intro"]); opts += it["steps"]
    elif ty == "fill":
        stems.append(it["stem"]); opts += it["bank"]
        for b in it["blanks"]:
            opts.append(b["sentence"])      # blanks are compared by equality (rule b), as in the plan
    return stems, opts, nums

def advisory_texts(it):
    """beyond the plan: the short blank sentences of a fill group are also read like stems; findings are ADVISORY (reported, listed, not a gate failure)"""
    return [b["sentence"] for b in it["blanks"]] if it.get("type") == "fill" else []

def run_items(gate, items, log, label=""):
    fails = 0; n = 0; maxg = 0; maxw = 0; maxd = 0; advisories = []
    for it in items:
        stems, opts, nums = item_texts(it)
        if it.get("type") == "numeric":
            units = [(nid, st, kv, un) for (nid, st, kv, un) in nums]
            subs = [(nid, [st], [], [(st, kv, un)]) for (nid, st, kv, un) in units]
        else:
            subs = [(it["id"], stems, opts, [])]
        for sid, sts, ops, nm in subs:
            n += 1
            reasons = []; ng = (0, None); nw = (0, None); nd = (0, None)
            for s in sts:
                r = gate.stem_check(s)
                if r["g5"][0] > ng[0]: ng = r["g5"]
                if r["word"][0] > nw[0]: nw = r["word"]
                if r["doc"][0] > nd[0]: nd = r["doc"]
            if ng[0] >= THRESH_GRAM5: reasons.append("a:gram5>=%.2f" % THRESH_GRAM5)
            if nw[0] >= THRESH_WORD: reasons.append("a:word>=%.2f" % THRESH_WORD)
            if nd[0] >= DOC_CONTAIN: reasons.append("a:doc>=%.2f" % DOC_CONTAIN)
            oh = [gate.opt_check(o) for o in ops]
            oh = [x for x in oh if x]
            if oh: reasons.append("b:option-equals-indexed(%d)" % len(oh))
            for (st, kv, un) in nm:
                h = gate.num_check(st, kv, un)
                if h: reasons.append("c:key-value-seen(%s)" % h[0][0])
                if it.get("family") or re.match(r"n[34]x_", str(it.get("id", ""))):
                    reasons += gate.family_check(st, kv)
            maxg = max(maxg, ng[0]); maxw = max(maxw, nw[0]); maxd = max(maxd, nd[0])
            adv = []
            for a_ in advisory_texts(it) if sid == it["id"] else []:
                r2 = gate.stem_check(a_)
                if r2["g5"][0] >= THRESH_GRAM5 or r2["word"][0] >= THRESH_WORD or r2["doc"][0] >= DOC_CONTAIN:
                    adv.append("blank sentence: 5g %s %.3f word %s %.3f doc %s %.3f" % (r2["g5"][1], r2["g5"][0], r2["word"][1], r2["word"][0], r2["doc"][1], r2["doc"][0]))
            if adv:
                advisories.append(sid)
                log("%s %s ADVISORY (beyond the plan, not counted as failure): %s" % (label, sid, "; ".join(adv)))
            ok = not reasons
            fails += (not ok)
            log("%s %s nearest5g=%s %.3f nearestword=%s %.3f doc=%s %.3f optHits=%d %s%s" % (
                label, sid, ng[1], ng[0], nw[1], nw[0], nd[1], nd[0], len(oh),
                "PASS" if ok else "FAIL ", ",".join(reasons)))
    log("%s units checked: %d, failed: %d, max5gram=%.3f maxword=%.3f maxdoc=%.3f; advisory (blank sentences read like stems): %d %s" % (label, n, fails, maxg, maxw, maxd, len(advisories), advisories))
    return n, fails

# ---------- fixtures (planted copies are taken from the private items file in memory only) ----------
def bump_numbers(s):
    return re.sub(r"\d[\d,]*", lambda m: str(int(m.group(0).replace(",", "")) + 7), s)

def change_two_words(s):
    w = s.split(" ")
    idx = [i for i, x in enumerate(w) if x.isalpha() and len(x) > 4]
    pick = [idx[len(idx) // 3], idx[(2 * len(idx)) // 3]] if len(idx) >= 4 else idx[:2]
    for i in pick:
        w[i] = "other"
    return " ".join(w)

def fixtures(gate, log):
    src = json.load(open(EXAM + "/private/sen0401_exam_items_midterm_v1_8_0.json"))["items"]
    ch = [x for x in src if x["type"] == "ChoiceFour"][0]
    nu = [x for x in src if x["type"] == "NumericAnswer"][0]
    def mkchoice(i, stem, opts):
        return {"id": i, "type": "choice", "stem": stem, "options": opts, "answer": 0}
    def mknum(i, stem, kv, unit):
        return {"id": i, "type": "numeric", "unit": unit, "instances": [{"stem": stem, "key_value": kv}]}
    fx = [
        ("FX-copy-verbatim", mkchoice("fx1", ch["q"], ch["options"]), False),
        ("FX-copy-numbers-changed", mkchoice("fx2", bump_numbers(ch["q"]), [bump_numbers(o) for o in ch["options"]]), False),
        ("FX-copy-two-words-changed", mkchoice("fx3", change_two_words(ch["q"]), [change_two_words(o) for o in ch["options"]]), False),
        ("FX-numeric-verbatim", mknum("fx4", nu["q"], nu["key_value"], nu["unit"]), False),
        ("FX-numeric-numbers-changed", mknum("fx5", bump_numbers(nu["q"]), nu["key_value"] + 3, nu["unit"]), False),
        ("FX-numeric-same-key-new-wording-near", mknum("fx6", nu["q"].replace("A toy hash", "A small hash"), nu["key_value"], nu["unit"]), False),
        ("FX-family-number-sequence-copy-reworded", dict(mknum("fx9", "A different story uses the quantities " + ", ".join(re.findall(r"\d+", nu["q"])) + " in some other way. You are asked to calculate the total of the story.", nu["key_value"] + 1, "widgets"), family="hash_search"), False),
        ("FX-family-tag-list-copy-reworded", dict(mknum("fx11", "Another team ships these tags: " + ", ".join(list(gate.taglists)[0]) + ". You are asked to calculate how many tags there are times seven.", 4242, "tags"), family="release_tags"), False),
        ("FX-family-genuinely-new", dict(mknum("fx10", "A depot has 7 shelves, 9 boxes on each shelf and 3 empty boxes. You are asked to calculate how many boxes hold goods.", 60, "boxes"), family="hash_search"), True),
        ("FX-genuinely-new", mkchoice("fx7",
            "A bakery packs 6 rolls in each of 14 trays and sells 59 rolls before noon. You are asked to choose the statement that tells how many rolls are left.",
            ["25 rolls are left, because 6 x 14 = 84 and 84 - 59 = 25.", "20 rolls are left, because 14 + 6 = 20 and the sold rolls are not counted.",
             "143 rolls are left, because 84 + 59 = 143 rolls remain on the trays.", "78 rolls are left, because 84 - 6 = 78 after one tray is sold.",
             "73 rolls are left, because 59 + 14 = 73 is the count that remains."]), True),
        ("FX-genuinely-new-numeric", mknum("fx8",
            "A garden has 12 beds. Each bed holds 15 plants and 38 plants are removed in spring. You are asked to calculate how many plants stay in the garden.",
            142, "plants"), True),
    ]
    bad = 0
    for name, it, should_pass in fx:
        stems, opts, nums = item_texts(it)
        reasons = []
        for s in stems:
            r = gate.stem_check(s)
            if r["g5"][0] >= THRESH_GRAM5: reasons.append("g5")
            if r["word"][0] >= THRESH_WORD: reasons.append("word")
            if r["doc"][0] >= DOC_CONTAIN: reasons.append("doc")
            g5 = r["g5"][0]; w = r["word"][0]; dd = r["doc"][0]
        if any(gate.opt_check(o) for o in opts): reasons.append("opt")
        for (nid, st, kv, un) in nums:
            if gate.num_check(st, kv, un): reasons.append("num")
            if it.get("family"): reasons += ["fam:" + x.split("-")[0] for x in gate.family_check(st, kv)]
        passed = not reasons
        good = (passed == should_pass)
        bad += (not good)
        log("%s expected=%s got=%s (reasons %s; g5=%.3f word=%.3f doc=%.3f) %s" % (
            name, "PASS" if should_pass else "FAIL", "PASS" if passed else "FAIL", ",".join(sorted(set(reasons))) or "-", g5, w, dd, "FIXTURE OK" if good else "FIXTURE WRONG"))
    return bad

def load_bank_json(p):
    d = json.load(open(p)); return d["items"]

def load_html_bank(p):
    s = open(p, encoding="utf-8").read()
    m = re.search(r'<script id="mock-bank" type="application/json">(.*?)</script>', s, re.S)
    if not m:
        raise SystemExit("no embedded bank in " + p)
    return json.loads(m.group(1).replace("<\\/", "</"))["items"]

def main():
    a = sys.argv[1:]
    lines = []
    def log(x):
        print(x); lines.append(x)
    t0 = time.time()
    gate = Gate()
    log("exclusion gate v1.0.0; index: %d stems, %d options, %d numeric keys, %d documents" % (len(gate.stems), len(gate.opts), len(gate.nums), len(gate.docs)))
    rc = 0
    if "--selftest" in a:
        bad = fixtures(gate, log)
        log("SELFTEST " + ("PASS" if bad == 0 else "FAIL (%d fixtures wrong)" % bad)); rc |= (bad != 0)
    for mode in ("--bank", "--html"):
        if mode in a:
            files = []
            for x in a[a.index(mode) + 1:]:
                if x.startswith("--"): break
                files.append(x)
            for f in files:
                items = load_bank_json(f) if mode == "--bank" else load_html_bank(f)
                log("source %s: %d bank units" % (os.path.basename(f), len(items)))
                n, fl = run_items(gate, items, log, label=os.path.basename(f))
                rc |= (fl != 0)
    log("GATE RESULT " + ("PASS" if rc == 0 else "FAIL") + " (%.1f s)" % (time.time() - t0))
    if "--log" in a:
        open(a[a.index("--log") + 1], "w").write("\n".join(lines) + "\n")
    sys.exit(rc)
if __name__ == "__main__":
    main()
