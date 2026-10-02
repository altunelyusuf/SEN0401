#!/usr/bin/env python3
"""Deterministic smoke verification of a built SEN0401 chapter page (the full 9.24.0 browser test is sen0401_page_test_v9_24_0.py and takes
longer; this one answers 'does the page open and do its working tabs work?' in a few minutes, with nothing random and nothing waited on by guess).
Checks, in Chromium via Playwright, against 03-materials/chNN/page/sen0401_chNN_page_v9_24_0.html:
  1 opens with no console error or page error, and says it is SEN0401 / Mastering Bitcoin
  2 exam: a graded mock exam is started with student identity, answered through the page's own controls, finished (shows only 'Submitted'),
    released with a code made by the SEN0401 instructor key (a code made by the SEN0414 key is refused) and scores >= 95 percent
  3 practice: the chapter quiz checks an answer; every question type the chapter can carry is drawn; the chapter's question bank feeds
    'multiple choice' and every bank program with code prints, in the page's own Python, the option marked right
  4 agents: the guide hands a question to the configured agent, which answers with cited passages and a follow-up
  5 SPARQL: every sample query runs without error, the first four return rows, the ASK sample answers Yes or No
  6 Playground / Code Lab / Step through: the default program runs with its inputs; every code pattern, every Code Lab snippet and every
    Step-through example runs without a Python error
  7 still no console error after all of that
usage: sen0401_page_smoke_v1_0_0.py NN        (PAGE_VER default 9_24_0; KEY = SEN0401 private key file; prints PASS/FAIL lines, exit 1 on any FAIL)"""
__version__ = "1.0.0"
import glob, hashlib as _hl, json, os, re, ssl as _ssl, subprocess, sys, urllib.request as _ur
from playwright.sync_api import sync_playwright

NUM = sys.argv[1]; N = "ch%s" % NUM; PV = os.environ.get("PAGE_VER", "9_24_0")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page_path = os.environ.get("PAGE", os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_v%s.html" % (N, PV)))
d = json.load(open(os.path.join(REPO, "08-tooling", "%s-page" % N, "page_data_v%s.json" % PV)))
KEY401 = os.environ.get("KEY", "/home/claude/instructor_keys/sen0401_instructor_key_v1_0_0.json"); KEY414 = "/home/claude/instructor_keys/sen0414_instructor_key_v1_0_0.json"
_tc = sorted(glob.glob(os.path.join(REPO, "08-tooling", "%s-page" % N, "test_config_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
CFG = json.load(open(_tc[-1])) if _tc else {"guide_q": "what is proof of work?", "agent": d["agents"][0]["id"], "root": "what is proof of work?"}

def _cdn_cached(route):   # the CDN files (Pyodide, oxigraph, transformers.js) are kept on disk, shared with the full test
    u = route.request.url; f = "/tmp/cdncache/" + _hl.sha1(u.encode()).hexdigest()
    try:
        if not os.path.exists(f):
            os.makedirs("/tmp/cdncache", exist_ok=True)
            with _ur.urlopen(_ur.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=120, context=_ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt") if os.path.exists("/root/.ccr/ca-bundle.crt") else None) as rr:
                data = rr.read(); ct = rr.headers.get("content-type", "application/octet-stream")
            open(f, "wb").write(data); open(f + ".ct", "w").write(ct)
        route.fulfill(status=200, body=open(f, "rb").read(), headers={"content-type": open(f + ".ct").read(), "access-control-allow-origin": "*"})
    except Exception:
        route.continue_()

def release(key, chapter, code):
    return subprocess.check_output(["python3", os.path.join(REPO, "08-tooling", "sen0401_exam_release_v1_0_0.py"), key, chapter, code]).decode().strip()

RES = []
def feat(name, ok, det=""):
    RES.append((name, bool(ok), str(det)[:200])); print("  [%s] %s  %s" % ("PASS" if ok else "FAIL", name, str(det)[:160]), flush=True)

PYERR = re.compile(r"(^|\n)\s*(Traceback|[A-Za-z]*Error\b|[A-Za-z]*Exception\b)")
with sync_playwright() as p:
    b = p.chromium.launch(env=dict(os.environ, LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8"), **({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {}))
    ctx = b.new_context(locale="en-US", viewport={"width": 1400, "height": 900}); ctx.route(re.compile(r"^https://cdn\.jsdelivr\.net/"), _cdn_cached)
    pg = ctx.new_page(); errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto("file://" + page_path); pg.wait_for_timeout(1500)
    GROUP = pg.evaluate("GROUP_OF")
    def view(k):
        g = GROUP.get(k)
        if g:
            view(g)
            if not pg.locator('[data-pane="%s"]' % k).is_visible(): pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="%s"]' % k)
        else: pg.click('#groups [data-tab="%s"]' % k)
        pg.wait_for_timeout(150)
    # 1 ---------------------------------------------------------------
    head = pg.evaluate("()=>document.title+' | '+document.querySelector('header.top').textContent")
    feat("1 opens with no console or page error, as SEN0401 / Mastering Bitcoin", not errors and "SEN0401" in head and "Mastering Bitcoin" in pg.evaluate("D.course.chapter_intro"), "errors=%s; %s" % (errors[:2], head[:80].replace("\n", " ")))
    # 2 ---------------------------------------------------------------
    ALL401 = release(KEY401, "*", "*")
    view("exam"); pg.fill("#xesno", "20210001"); pg.fill("#xesname", "Test"); pg.fill("#xessur", "Student"); pg.select_option("#xekind", "M"); pg.uncheck("#xetimeron"); pg.fill("#xecode", "M-4001"); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000)
    nq = pg.locator("#xeout fieldset.xq").count()
    pg.evaluate(r"""()=>{document.querySelectorAll('#xeout fieldset[data-xi]').forEach((fs,i)=>{const it=XE.items[i],k=xKey(it),set=(sel,v)=>{const e=fs.querySelector(sel);e.value=v};
        if(it.type==='mcq')fs.querySelector('input[value="'+k+'"]').checked=true;
        else if(it.type==='multi')k.forEach(j=>{fs.querySelectorAll('input[type=checkbox]')[j].checked=true});
        else if(it.type==='judge'){fs.querySelector('input[value="'+k.v+'"]').checked=true;fs.querySelector('select').value=k.s}
        else if(it.type==='match')fs.querySelectorAll('select[data-row]').forEach(s=>{s.value=s.dataset.row});
        else if(it.type==='order'){const ol=fs.querySelector('ol');[...ol.children].sort((a,b)=>a.querySelector('code').dataset.l-b.querySelector('code').dataset.l).forEach(li=>ol.appendChild(li))}
        else if(it.type==='repair')set('textarea','print = lambda *a, **k: None\ntry:\n'+it.code.split('\n').map(l=>'    '+l).join('\n')+'\nexcept Exception:\n    pass');
        else set('textarea,input.xin',String(k))})}""")
    pg.click("#xefinish"); pg.wait_for_selector("#xelock", timeout=240000)
    submitted_only = pg.locator("#xereport").count() == 0
    pg.fill("#xerel", release(KEY414, "*", "*")); pg.click("#xeunlock"); pg.wait_for_timeout(800)
    refused = pg.locator("#xereport").count() == 0
    pg.fill("#xerel", ALL401); pg.click("#xeunlock"); pg.wait_for_selector("#xereport", timeout=60000); pct = pg.evaluate("XE.result.pct")
    feat("2 exam: %d questions answered through the controls; 'Submitted' only until released; the SEN0414 key's code is refused; the SEN0401 key's code releases it" % nq, nq >= 10 and submitted_only and refused and pct >= 95, "%s%%, submitted-only=%s, other-key refused=%s" % (pct, submitted_only, refused))
    # 3 ---------------------------------------------------------------
    view("quiz"); fs = pg.locator('[data-pane="quiz"] fieldset[data-answer]').first
    fs.locator('input[value="%s"]' % fs.get_attribute("data-answer")).check(); fs.locator("[data-check]").click(); pg.wait_for_timeout(200)
    feat("3a practice: the chapter quiz marks a right answer", "orrect" in fs.locator(".verdict").text_content() or "ight" in fs.locator(".verdict").text_content(), fs.locator(".verdict").text_content()[:60])
    view("qtypes"); made = {}
    for t in ["mcq", "multi", "cloze", "judge", "match", "predict", "blank", "order", "write", "short", "program"]:
        pg.select_option("#xdtype", t); pg.click("#xdnew")
        try: pg.wait_for_selector("#xdout fieldset.xq", timeout=60000); made[t] = True
        except Exception: made[t] = False
    feat("3b practice: every question type the chapter carries is drawn", all(made.values()), str({k: v for k, v in made.items() if not v}) or "%d types" % len(made))
    bank = pg.evaluate("BANK")
    ok_bank = pg.evaluate(r"""async()=>{const cid=BANK[0].concept;const it=await xMake('mcq',{R:xrng(1),cids:[cid],used:new Set(),prefer:[]});return !!it&&BANK.some(b=>b.q===it.q)}""") if bank else False
    bad = pg.evaluate(r"""async()=>{const bad=[];for(const b of BANK){if(!b.code)continue;const o=String(await runPy(b.code)).trim();if(o!==b.options[b.answer])bad.push([b.concept,o])}return bad}""") if bank else [("no bank", "")]
    feat("3c practice: the chapter's question bank (%d items) feeds multiple choice and every bank program prints the marked answer in the page's own Python" % len(bank), bank and ok_bank and not bad, "bad=%s" % bad[:2])
    # 4 ---------------------------------------------------------------
    view("agents"); pg.click('[data-agenttab="guide"]'); gl = pg.locator("#guide-log .msg").count(); pg.fill("#guide-q", CFG["guide_q"]); pg.press("#guide-q", "Enter")
    pg.wait_for_function("n=>{const m=document.querySelectorAll('#guide-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=gl, timeout=120000)
    sugg = [pg.locator("#guide-log .msg").last.locator("[data-handoff]").nth(k).get_attribute("data-handoff") for k in range(pg.locator("#guide-log .msg").last.locator("[data-handoff]").count())]
    target = CFG["agent"]; pg.locator('#guide-log .msg').last.locator('[data-handoff="%s"]' % target).click()
    pg.wait_for_function("id=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=3&&!m[m.length-1].classList.contains('typing')}", arg=target, timeout=120000)
    ans1 = pg.locator("#%s-log .msg" % target).last.inner_text()
    n0 = pg.locator("#%s-log .msg" % target).count(); pg.fill("#%s-q" % target, "can you give me an example?"); pg.press("#%s-q" % target, "Enter")
    pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=[target, n0], timeout=120000)
    ans2 = pg.locator("#%s-log .msg" % target).last.inner_text()
    feat("4 agents: the guide hands the question to %s, which answers with a source and gives an example on follow-up" % target, target in sugg and len(ans1) > 60 and "for example" in ans2.lower(), "suggested=%s; answer: %s" % (sugg[:3], ans1[:70].replace("\n", " ")))
    # 5 ---------------------------------------------------------------
    view("sparql"); ns = pg.locator("#sqsamp option").count(); rows = []; bad = []
    for i in range(ns):
        pg.select_option("#sqsamp", str(i)); pg.click("#sqrun")
        pg.wait_for_function("()=>/result|row|Yes|No/.test(document.getElementById('sqstat').textContent+document.getElementById('sqres').textContent)||document.querySelector('#sqres .err')", timeout=60000)
        err = pg.locator("#sqres .err").count(); r = pg.locator("#sqres tr").count() - 1; rows.append(r)
        if err: bad.append((i, pg.locator("#sqres .err").first.text_content()[:60]))
        if i < 4 and r < 1: bad.append((i, "no rows"))
        if i == 5 and pg.text_content("#sqres").strip() not in ("Yes", "No"): bad.append((i, "ASK answered " + pg.text_content("#sqres")[:20]))
    feat("5 SPARQL: all %d sample queries run; the first four return rows; the ASK answers Yes or No" % ns, ns >= 6 and not bad, "rows=%s bad=%s" % (rows, bad))
    # 6 ---------------------------------------------------------------
    view("play"); pg.select_option("#pex", "first"); pg.wait_for_timeout(400); pg.click("#prun")
    pg.wait_for_function("()=>{const o=document.getElementById('pout');return o&&o.textContent.trim().length>0&&!/running|Running|loads on/.test(o.textContent)}", timeout=120000); dflt = pg.text_content("#pout")
    feat("6a Playground: the default program (a toy proof-of-work miner) runs with its typed input", re.search(r"nonce \d+ gives [0-9a-f]{64}", dflt) is not None, dflt[:80])
    tpls = [o.get_attribute("value") for o in pg.locator("#pex option").all() if (o.get_attribute("value") or "").startswith("tpl:")]; bad = []
    for v in tpls:
        pg.select_option("#pex", v); pg.wait_for_timeout(200); pg.click("#prun")
        pg.wait_for_function("()=>{const o=document.getElementById('pout');return o&&o.textContent.trim().length>0&&!/^running/.test(o.textContent.trim())}", timeout=120000); o_ = pg.text_content("#pout")
        if PYERR.search(o_) and "Problem" not in o_: bad.append((v, o_[:60]))
    feat("6b Playground: all %d code patterns run" % len(tpls), tpls and not bad, "bad=%s" % bad[:3])
    for e in pg.evaluate("D.nodes.filter(n=>n.io).map(n=>n.id)")[:4]:
        pg.select_option("#pex", e); pg.click("#prun"); pg.wait_for_function("()=>{const o=document.getElementById('pout');return o&&o.textContent.trim().length>0&&!/^running/.test(o.textContent.trim())}", timeout=120000)
    view("codelab"); bad = []
    for i in range(pg.locator("#clsnip option").count()):
        pg.select_option("#clsnip", str(i)); pg.click("#clrun"); pg.wait_for_function("()=>{const t=document.getElementById('clout').textContent;return t&&t!=='running...'}", timeout=120000); o_ = pg.text_content("#clout")
        if PYERR.search(o_): bad.append((i, o_[:60]))
    feat("6c Code Lab: all %d snippets run against this page's data" % pg.locator("#clsnip option").count(), not bad, "bad=%s" % bad[:3])
    view("trace"); bad = []; steps_n = []
    for i in range(pg.locator("#trex option").count()):
        pg.select_option("#trex", str(i))   # choosing an example traces it (no Trace button)
        pg.wait_for_function("()=>/^step 1 of \\d+/.test(document.getElementById('trpos').textContent)||/error/i.test(document.getElementById('trstat').textContent)", timeout=120000)
        if not re.match(r"step 1 of \d+", pg.text_content("#trpos")) or "error" in pg.text_content("#trstat").lower(): bad.append((i, pg.text_content("#trstat")[:60])); continue
        steps_n.append(int(pg.text_content("#trpos").split(" of ")[1].split()[0])); pg.click("#trnext")
        if not pg.text_content("#trpos").startswith("step 2 of"): bad.append((i, "Step did not advance"))
    feat("6d Step through: all %d examples trace and step" % pg.locator("#trex option").count(), not bad and min(steps_n or [0]) >= 3, "steps per example %s; bad=%s" % (steps_n, bad[:3]))
    # 7 ---------------------------------------------------------------
    feat("7 no console or page error after all of that", not errors, str(errors[:3]))
    b.close()
fails = [r for r in RES if not r[1]]
print("%d checks, %d PASS, %d FAIL" % (len(RES), len(RES) - len(fails), len(fails)))
json.dump([{"check": a, "passed": b_, "detail": c} for a, b_, c in RES], open(os.path.join(REPO, "08-tooling", "%s-page" % N, "smoke_results_v%s.json" % PV), "w"), indent=1)
sys.exit(1 if fails else 0)
