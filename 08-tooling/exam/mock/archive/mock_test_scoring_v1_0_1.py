#!/usr/bin/env python3
"""Scoring test (brief point 6). Run under: flock /tmp/page_test.lock nice -n 10 python3 mock_test_scoring_v1_0_0.py BANK.json MOCK.html [--log F]
 - independent Python key (from the bank texts, not from the page code) and Python reference scorer (right = points else 0);
 - 50 seeded sheets (right / wrong / blank mix) scored by (1) node running the same scoring.js + derive.js text and (2) the page in headless Chromium
   (answers put on the page controls, button 'Check my answers' pressed, score read from the page text); all three must agree;
 - 4 sheets driven with real clicks, typing and select choices on the controls;
 - before the check no solution text is in the page; after it the solution text is there;
 - blind random sheets: exact expected value against node simulation;
 - planted defects: deduction scorer, wrong letter map after the shuffle: both must be caught."""
import json, sys, os, random, subprocess, tempfile, math
H = os.path.dirname(os.path.abspath(__file__))
bankf, htmlf = sys.argv[1], sys.argv[2]
lines = []
def log(x):
    print(x, flush=True); lines.append(x)
BANK = {x["id"]: x for x in json.load(open(bankf))["items"]}

def node(job):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(job, f); p = f.name
    r = subprocess.run(["nice", "-n", "10", "node", os.path.join(H, "mock_node_driver_v1_0_0.js"), p], capture_output=True, text=True)
    os.unlink(p)
    if r.returncode: raise SystemExit("node: " + r.stderr[:600])
    return json.loads(r.stdout)

# ---- independent key from the bank texts ----
def py_key(it):
    b = BANK[it["uid"].split("#")[0]]
    t = it["type"]
    if t == "choice":
        want = b["options"][b["answer"]]
        return [i for i, o in enumerate(it["options"]) if o["text"] == want][0]
    if t == "numeric":
        return b["instances"][int(it["uid"].split("#")[1])]["key_value"]
    if t == "ordering":
        return list(b["answer"])
    if t == "matching":
        return [[i for i, o in enumerate(it["responses"]) if o["text"] == b["responses"][a]][0] for a in b["answer"]]
    if t == "fill":
        return [[i for i, o in enumerate(it["bank"]) if o["text"] == b["bank"][bl["answer"]]][0] for bl in b["blanks"]]

def places(it):
    t = it["type"]
    if t in ("choice", "numeric"): return 1
    return {"matching": 4, "ordering": 5, "fill": 2}[t]

def place_pts(it, j):
    t = it["type"]
    if t in ("choice", "numeric"): return it["points"]
    if t == "matching": return it["rowPoints"][j]
    if t == "ordering": return 1
    return it["blankPoints"][j]

def make_sheet(mock, rnd):
    pr = rnd.uniform(0.1, 0.9); pb = rnd.uniform(0.0, 0.3)
    ans = {}
    for Q in mock["questions"]:
        for it in Q["items"]:
            key = py_key(it); t = it["type"]; out = []
            for j in range(places(it)):
                r = rnd.random()
                if t == "choice":
                    if r < pb: v = None
                    elif r < pb + (1 - pb) * pr: v = key
                    else: v = rnd.choice([i for i in range(5) if i != key])
                elif t == "numeric":
                    if r < pb: v = None
                    elif r < pb + (1 - pb) * pr: v = str(key)
                    else: v = str(rnd.choice([x for x in [key + 1, max(0, key - 1), key * 10 % 100000, rnd.randrange(100000)] if x != key]))
                elif t == "ordering":
                    k = key[j]
                    if r < pb: v = None
                    elif r < pb + (1 - pb) * pr: v = k
                    else: v = rnd.choice([i for i in range(1, 6) if i != k])
                else:
                    k = key[j]
                    if r < pb: v = None
                    elif r < pb + (1 - pb) * pr: v = k
                    else: v = rnd.choice([i for i in range(5) if i != k])
                out.append(v)
            ans[it["uid"]] = out[0] if t in ("choice", "numeric") else out
    return ans

def py_score(mock, ans):
    tot = 0; byq = {}
    for Q in mock["questions"]:
        g = 0
        for it in Q["items"]:
            key = py_key(it); a = ans[it["uid"]]; t = it["type"]
            if t == "choice":
                g += it["points"] if (a is not None and a == key) else 0
            elif t == "numeric":
                g += it["points"] if (a not in (None, "") and int(a) == key) else 0
            else:
                for j in range(places(it)):
                    if a[j] is not None and a[j] == key[j]:
                        g += place_pts(it, j)
        byq[Q["q"]] = g; tot += g
    return tot, byq

pairs = [(4 + (i % 2), (1000 + 37 * (4 + i)) if i < 2 else 5000 + 13 * i) for i in range(50)]   # v1.0.1: 50 seeded sheets of mocks 4 and 5 (the two that draw f6_1 and f4_4)
uniq = sorted(set(pairs))
dumps = node({"bank": bankf, "ops": [{"op": "derive", "k": k, "seed": s} for k, s in uniq]})
D = {(m["k"], m["seed"]): m for m in dumps}
rnd = random.Random(20261103)
sheets = []
for (k, s) in pairs:
    m = D[(k, s)]
    sheets.append((k, s, make_sheet(m, rnd)))
ref = [py_score(D[(k, s)], a) for (k, s, a) in sheets]
log("python reference: %d sheets over %d distinct mocks (k,seed); totals range %d..%d, mean %.1f" % (len(sheets), len(uniq), min(r[0] for r in ref), max(r[0] for r in ref), sum(r[0] for r in ref) / len(ref)))
# full-marks and empty-sheet sanity
full = node({"bank": bankf, "ops": [{"op": "score", "k": 2, "seed": 77, "answers": {}}]})
log("empty sheet scores %d (expected 0)" % full[0]["total"])
ok = full[0]["total"] == 0

# ---- node: same scoring.js/derive.js text ----
res = node({"bank": bankf, "ops": [{"op": "score", "k": k, "seed": s, "answers": a} for (k, s, a) in sheets]})
mism = [i for i, (r, n) in enumerate(zip(ref, res)) if r[0] != n["total"] or any(r[1][q] != n["byQuestion"][str(q)]["got"] for q in r[1])]
log("node (same scoring.js + derive.js text): %d sheets, mismatches" % len(sheets) + " against the Python scorer: %d" % len(mism))
ok = ok and not mism

# ---- planted defects (node, patched source) ----
dd = node({"bank": bankf, "patch": "deduct", "ops": [{"op": "score", "k": k, "seed": s, "answers": a} for (k, s, a) in sheets]})
mm = sum(1 for r, n in zip(ref, dd) if r[0] != n["total"])
log("PLANTED DEFECT deduction scorer: %d of 50 sheets disagree with the reference -> %s" % (mm, "CAUGHT" if mm else "NOT CAUGHT"))
ok = ok and mm > 0
lt = node({"bank": bankf, "patch": "letter", "ops": [{"op": "derive", "k": k, "seed": s} for (k, s) in uniq]})
bad_keys = 0
for m in lt:
    for Q in m["questions"]:
        for it in Q["items"]:
            if it["type"] == "choice" and it["correct"] != py_key(it): bad_keys += 1
clean_bad = sum(1 for m in dumps for Q in m["questions"] for it in Q["items"] if it["type"] == "choice" and it["correct"] != py_key(it))
log("PLANTED DEFECT wrong letter map after the shuffle: choice items whose printed key disagrees with the bank text: %d (clean code: %d) -> %s" % (bad_keys, clean_bad, "CAUGHT" if bad_keys and not clean_bad else "NOT CAUGHT"))
ok = ok and bad_keys > 0 and clean_bad == 0
# keys of all kinds, clean code
kbad = 0
for m in dumps:
    for Q in m["questions"]:
        for it in Q["items"]:
            if it["type"] != "numeric" and it["correct"] != py_key(it): kbad += 1
            if it["type"] == "numeric" and it["key"] != py_key(it): kbad += 1
log("clean code: items whose key differs from the independent Python key: %d" % kbad)
ok = ok and kbad == 0

# ---- blind sheets ----
def exact(m):
    e = 0.0
    for Q in m["questions"]:
        for it in Q["items"]:
            for j in range(places(it)):
                p = 1e-5 if it["type"] == "numeric" else 0.2
                e += p * place_pts(it, j)
    return e
for k in (4, 5):
    b = node({"bank": bankf, "ops": [{"op": "blind", "k": k, "seed": 31, "n": 40000, "rngseed": 99 + k}]})[0]
    m = node({"bank": bankf, "ops": [{"op": "derive", "k": k, "seed": 31}]})[0]
    ex = exact(m); se = math.sqrt(b["var"] / b["n"])
    z = abs(b["mean"] - ex) / se
    log("blind random answers, mock %d: exact expected %.4f, simulated mean %.4f over %d sheets (standard error %.4f, z = %.2f) -> %s" % (k, ex, b["mean"], b["n"], se, z, "OK" if z < 4 else "FAIL"))
    ok = ok and z < 4

# ---- browser ----
from playwright.sync_api import sync_playwright
url = "file://" + htmlf
bm = 0; checked = 0
with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={"width": 1280, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("requestfailed", lambda r: errs.append("request failed " + r.url))
    reqs = []
    pg.on("request", lambda r: reqs.append(r.url) if not r.url.startswith("file:") and not r.url.startswith("data:") else None)
    pg.goto(url)
    pg.wait_for_selector("#paper .item")
    # no solution before the check
    probe = json.loads(pg.evaluate("JSON.stringify(MockApp.getMock().questions[0].items[0].src.why_right)"))
    probe = probe.split("{o")[0].strip() or probe[:25]
    DOMTXT = "document.getElementById('paper').textContent + ' ' + document.getElementById('result').textContent + ' ' + document.body.innerText"
    before = pg.evaluate(DOMTXT)
    absent = (probe not in before) and "Worked solution" not in before and "Why it is right" not in before
    pg.click("#btn-check")
    after = pg.evaluate(DOMTXT)
    present = "Worked solution" in after and "Why it is right" in after
    log("before the check the solution text is in the page: %s; after the check it is: %s -> %s" % (not absent, present, "OK" if absent and present else "FAIL"))
    ok = ok and absent and present
    # "Why this question" line: shown after the check for items that carry it, nowhere else
    wq_bad = 0; wq_tot = 0
    for k in (4, 5):
        pg.evaluate("localStorage.clear()"); pg.evaluate("([k,s]) => MockApp.derive(k,s)", [k, 4000 + k])
        before_n = pg.evaluate("document.querySelectorAll('.whyq').length")
        want = pg.evaluate("MockApp.getMock().questions[1].items.filter(it => (it.inst && it.inst.why_question) || (it.src && it.src.why_question)).length")
        pg.click("#btn-check")
        got = pg.evaluate("document.querySelectorAll('.whyq').length")
        wq_tot += want; wq_bad += (before_n != 0 or got != want)
    log("'Why this question' lines after the check: expected %d over 3 mocks, mocks with a wrong count (or a line before the check): %d" % (wq_tot, wq_bad))
    ok = ok and wq_bad == 0
    # 200 sheets via the page
    for i, (k, s, a) in enumerate(sheets):
        pg.evaluate("([k,s]) => MockApp.derive(k,s)", [k, s])
        pg.evaluate("(a) => MockApp.apply(a)", a)
        pg.click("#btn-check")
        tot = int(pg.get_attribute("#score-total", "data-score"))
        txt = pg.inner_text("#score-total")
        qs = {int(li.get_attribute("data-q")): int(li.get_attribute("data-score")) for li in pg.query_selector_all("#score-q li")}
        r = ref[i]
        if tot != r[0] or qs != r[1] or ("Total: %d / 100" % tot) != txt.strip():
            bm += 1
        checked += 1
    log("page (headless Chromium, answers set on the controls, Check pressed, score read from the page text): %d sheets, mismatches against the Python scorer: %d" % (checked, bm))
    ok = ok and bm == 0
    # page derive equals node derive
    pg.evaluate("([k,s]) => MockApp.derive(k,s)", [4, 5000])
    pids = pg.evaluate("MockApp.getMock().itemIds")
    nid = node({"bank": bankf, "ops": [{"op": "derive", "k": 4, "seed": 5000}]})[0]["itemIds"]
    log("page and node derive the same item ids for k=4 seed 5000: %s" % (pids == nid))
    ok = ok and pids == nid
    # real UI sheets
    real_ok = 0
    for n in range(4):
        k, s, a = sheets[n]
        pg.evaluate("localStorage.clear()")
        pg.evaluate("([k,s]) => MockApp.derive(k,s)", [k, s])
        mock = D[(k, s)]
        for Q in mock["questions"]:
            for it in Q["items"]:
                v = a[it["uid"]]
                card = pg.locator('[data-uid="%s"]' % it["uid"])
                if it["type"] == "choice":
                    if v is not None: card.locator('.opt[data-idx="%d"]' % v).click()
                elif it["type"] == "numeric":
                    if v not in (None, ""): card.locator(".digin").fill(str(v), force=True)
                else:
                    for j, x in enumerate(v):
                        if x is not None:
                            card.locator("select").nth(j).select_option(index=(x if it["type"] == "ordering" else x + 1))
        pg.click("#btn-check")
        tot = int(pg.get_attribute("#score-total", "data-score"))
        real_ok += (tot == ref[n][0])
        log("  real-click sheet %d: page %d, reference %d" % (n + 1, tot, ref[n][0]))
    ok = ok and real_ok == 4
    log("external requests made by the page: %d %s; page errors: %d %s" % (len(reqs), reqs[:3], len(errs), errs[:3]))
    ok = ok and not reqs and not errs
    br.close()
log("SCORING TEST " + ("PASS" if ok else "FAIL"))
if "--log" in sys.argv:
    open(sys.argv[sys.argv.index("--log") + 1], "w").write("\n".join(lines) + "\n")
sys.exit(0 if ok else 1)
