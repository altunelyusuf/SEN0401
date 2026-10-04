#!/usr/bin/env python3
"""Browser tests for version 9 - visualisations computed by Python (evaluation steps, step-through tracer, code pipeline, chapter visualisations) and wheel zoom - on top of version 8 - a seven-item top menu, subject overviews without repeated lists, folded introductions, one rooted taxonomy with fitting labels, zoom on every diagram - on top of version 7 - the RDODI fit-gap views (ontology graph, Code Lab, SPARQL console, question views, About, downloads) on top of version 6 - the conversation view (roster with role icons, guide, handoff, follow-ups, memory) on top of version 5 - version 4's checks, plus: the page's own thread never blocks for long, and an endless program is stopped while the page stays responsive ( (version 3's rule checks plus the agents' toolkit) of a SEN0414 page - the owner's rules of 2026-09-25 made checkable:
code the student edits really runs (edited code must change the result); agents answer from their own
slice, so different questions get different answers; a menu click changes the main area and leaves the
detail card closed; the card opens only on an explicit request; the tab row is the sub-menu of the
selected top-level item. Every stored result must also equal what the build's interpreter printed."""
__version__ = "9.25.0"
# 9.25.0 (over 9.24.0): the course question the course-ontology check asks, and the outcome code it looks for, come from the chapter's test_config (course_q / course_lo); SEN0414's wording asked about choosing libraries, which is not an SEN0401 outcome. No other change.
# 9.24.0 (SEN0401; over SEN0414's 9.23.0, which is otherwise unchanged): runs against sen0401_chNN_page_v9_24_0.html; the page lives in 03-materials/chNN/page of the SEN0401 repository; the questions put to the guide and to one agent come from the chapter's test_config_v*.json (the SEN0414 default questions, about Python, are replaced by a blockchain default); the exam release codes are made by sen0401_exam_release_v1_0_0.py with the SEN0401 instructor key (default /home/claude/instructor_keys/sen0401_instructor_key_v1_0_0.json, override with KEY=); the default page version is 9_24_0.
# 9.23.0 (over 9.22.0): multiple choice has no "None of the above"; a multiple-answer type (select all that apply, partial credit) is made, read, marked and kept like the others; the input row shows only when the code calls input(), with values that fit; concept text is shown as paragraphs opening with what they answer.
# 9.22.0 (over 9.19.0): the owner's review of chapter 1 - a link back to the index; ONE Playground list (examples and code patterns, every pattern run); the header wraps on a phone with no sideways scroll in any pane; light theme only; the audit log as a zip; the clear option asks first.
# 9.19.0 (over 9.18.0): the mock exam is a graded exam - nothing starts without student number, name and surname; Finish shows only 'Submitted' (no score, no corrections); the result is released by the instructor's release code (made here with the instructor key kept outside the repository); a book-concept count of zero is allowed (chapter 15's labels have none). The full exam-and-desk flow is tested by sen0414_exam_test_v1_0_0.py.
# 9.18.0 (over 9.17.0): serves every chapter - the map node it taps is one nothing covers, the search word is the label's longest word, and the graph thresholds are relative to a small chapter (at least 5 syntax and 5 behaviour links, 3 syntax and 2 behaviour kinds).
# 9.17.0 (over 9.16.0): the ERD detail is checked with a real mouse click (the 9.16.0 test used a synthetic event and missed a handler that real clicks never reached); checks that depend on a chapter having a runnable program are guarded, so the test serves every chapter.
# 9.16.0 (over 9.15.0): the taxonomy is the tree with its leaves; the ontology is a graph of meaning, syntax and behaviour with class-diagram and ERD views; code can be saved and opened as a .py file; corrections are folded; exams are kept in a list with review, retake and new alternatives; a complete-the-program question type (owner request 2026-09-30 17:29).
# 9.15.0 (over 9.14.0): checks the code editor (colours, indent, brackets, suggestions, templates, hover help, font controls, scroll sync), the short adjustable agent list with tips, the Playground default, the card closing on context change, the ontology tree and the Back/Forward trail (all as the owner asked on 2026-09-30 16:15).
# 9.14.0 (over 9.13.0): ten question types are made and marked (a right answer scores in full, a wrong one does not, every one carries a correction), code questions are varied and their expected result equals a fresh run; mock midterm and final exams are the same for the same code, marked through the page's own controls (answers filled in, timer, report, history, copy); the live model choice and the model comment; the emoji heading of the question builder shows no escape text; axe over the two new panes
# 9.11.0 (over 9.10.0): the chapter-visualisation section skips keys of the visuals file that are not concept ids (the deck-only framing slide) and checks the 13 kinds of chapter 6 against the specification by reading the drawn DOM/SVG: boxes (every index label, item and back index, each pick highlights its boxes, the error), slices (every cell, the selected indexes of each row, the order numbers), lanes (before and after lists, the marked boxes, the returned value, the same-object flag, the errors), hist (label, count and bar length of each bar), refgraph (for every scenario and step: each name, the object it reaches - by its arrow ending on that object's frame -, every item, every reference arrow), keysort (items, keys, output, the lines from input to output), matrix (frames stepped, the hazard rows, the counter table), mutation and passes (stepped rows), unpack, seqtypes, classify and facts; each check runs only when the chapter has that kind. Also: zoom on every SVG visual (keysort, refgraph, range, pairs) and its kept view when a step redraws it; axe (WCAG 2 A/AA) over all chapter visuals shown; the lecture-slide check ignores slides whose visual is not a concept.
# 9.10.0 (over 9.9.0): the builder draws on the chapter's written question bank (every concept, every Apply item re-run in the page) and asks for it first when it asks one question for every concept; the live-model question is refused when malformed or when its code does not print the marked answer, and says so when the browser has no model.
# 9.9.0 (over 9.8.0): choosing a SPARQL sample fills the query at once (no Load sample button); agent answers are formatted (lead sentence, bullets, coloured code, example block, related chips; markdown-lite for LLM text); the quiz builder makes a question of every kind for every concept on request, checks answers, reports coverage.
# 9.8.0 (over 9.7.0): choosing an example fills the code at once (Playground, Code Lab, Step through, Code pipeline - no Load button); Step through traces on the first Step, Back, First or Play without a Trace button and traces again when the code changes; the Code pipeline offers examples, runs on the first stage or next-stage click, and every example of both lists is run.
# 9.7.0 (over 9.6.0): the leaf widget is a static Example (no Next step, no walk-through); checks the Lecture tab, the Resources tab, the fitted work area (h2 hidden under the tab row, notes folded, code areas that do not scroll inside), and the debugger, logging-level and unwinding visuals.
# 9.6.0 (over 9.5.1): checks the visualisations that are executed specifications: a trace steps through every pass of every run and its last row matches the specification; a range draws one dot per value and the stop marker; pairs draw every pair; the names visual states its count.
# 9.5.1 (over 9.5.0): the concept tap uses the first visible concept link (9.5.0 took the first one, at every such site, which can sit in a hidden pane, so a chapter whose first subject has one timed out).
# 9.5.0 (over 9.4.2): the questions put to the guide and to one agent come from the chapter's test_config_v*.json, when it has one
# (9.4.2 hard-coded chapters 1 and 2 and asked chapter 2's questions of every other chapter); and the browser is launched
# through the environment's proxy (HTTPS_PROXY) when there is one, keeping the rest of the environment (9.4.2 replaced the whole
# environment, so where the network is reached only through a proxy Pyodide could not load and the first Python run timed out).
import re, json, os, re, sys, time
PV = os.environ.get("PAGE_VER", "9_24_0")  # generated files carry the page version they were produced for
from playwright.sync_api import sync_playwright
N = sys.argv[1]; NUM = N; N = ("ch%s" % N) if N.isdigit() else N
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page_path = os.environ.get("PAGE", os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_v%s.html" % (N, os.environ.get("PAGE_VER", "9_24_0"))))
d = json.load(open(os.path.join(REPO, "08-tooling", "%s-page" % N, "page_data_v%s.json" % PV)))

# CDN files (Pyodide, oxigraph, transformers.js) are fetched once and kept on disk, so the test does not depend on how fast the proxy serves several parallel downloads
import hashlib as _hl, ssl as _ssl, urllib.request as _ur
def _cdn_cached(route):
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
import glob as _g
_tc = sorted(_g.glob(os.path.join(REPO, "08-tooling", "%s-page" % N, "test_config_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
# SEN0401 defaults; a chapter's test_config_v*.json overrides any key. The switches say what the SEN0401 corpus does NOT have, so the
# checks that need it are skipped (and listed under R["skipped"]) instead of failing:
#   corpus_kinds     the kinds of passage the agents search (SEN0401 has no textbook ontology and no course ontology yet: chapter, page, research)
#   course_outcomes  a course ontology with learning outcomes (LO-1 ...) is part of the corpus
#   code_layers      the chapter's concept examples are Python programs, so the ontology graph can draw syntax and behaviour links
#                    (SEN0401's examples are descriptions such as "a desktop wallet"; the computed examples are only a few)
#   bank_complete    the question bank has an item for every concept (false for a seed bank)
CFG = {"guide_q": "how does proof of work stop a double-spend?", "agent": "agent-Consensus", "root": "what is proof of work?",
       "corpus_kinds": ["chapter", "page", "research"], "course_outcomes": False, "code_layers": False, "bank_complete": True,
       "course_q": "which course learning outcome is about choosing libraries?", "course_lo": "LO-1"}
if _tc: CFG.update(json.load(open(_tc[-1])))
CODE_LAYERS, COURSE_OUT, BANK_COMPLETE = CFG["code_layers"], CFG["course_outcomes"], CFG["bank_complete"]
AXE = "/home/claude/Ontologies/rdodi-ecosystem/07-pedagogy-professional-stage/lib/axe.min.js"
R = {"_version": PV.replace("_", "."), "widgets": {}, "features": {}, "gates": {}}
def skip(k, why):
    R.setdefault("skipped", {})[k] = why; print("  [SKIP] %s  %s" % (k[:150], why), flush=True)
def feat(k, ok, det=""):
    R["features"][k] = {"passed": bool(ok), "detail": det}; print("  [%s] %s  %s" % ("PASS" if ok else "FAIL", k[:150], str(det)[:100]), flush=True)   # printed as it happens, so a crash does not lose the run
nodes = d["nodes"]; tops = [n for n in nodes if n["level"] == 1]
in_view = "id=>{const e=document.getElementById(id);if(!e)return false;const r=e.getBoundingClientRect();return r.height>0&&r.top<innerHeight&&r.bottom>0&&!e.closest('[hidden]')}"
with sync_playwright() as p:
    b = p.chromium.launch(env=dict(os.environ, LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8"), **({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {})); ctx = b.new_context(locale="en-US", viewport={"width": 1400, "height": 900}, permissions=["clipboard-read", "clipboard-write"]); ctx.route(re.compile(r"^https://cdn\.jsdelivr\.net/"), _cdn_cached); pg = ctx.new_page(); errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.add_init_script("window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push(Math.round(e.duration)))).observe({type:'longtask',buffered:true});")
    pg.goto("file://" + page_path); pg.wait_for_timeout(400)
    GROUP = pg.evaluate("GROUP_OF")
    def view(k):
        g = GROUP.get(k)
        if g:
            view(g); pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="%s"]' % k) if not pg.locator('[data-pane="%s"]' % k).is_visible() else None
        else:
            pg.click('#groups [data-tab="%s"]' % k)
        pg.wait_for_timeout(150)
        if k == "taxonomy": pg.wait_for_function("()=>document.querySelector('#taxo svg')", timeout=120000)
    # one top-level menu; tabs inside a subject are its sub-menu
    labels = [pg.locator("#groups button").nth(k).get_attribute("data-tab") for k in range(pg.locator("#groups button").count())]
    top2 = next(t for t in tops if len([n for n in nodes if n["parent"] == t["id"]]) >= 2)
    view(top2["id"])
    mids = [n for n in nodes if n["parent"] == top2["id"]]
    third_row = pg.locator('[data-pane="%s"] .subtabs:not(.viewsub)' % top2["id"]).count()
    sub_in_pane = pg.locator('#crumb-%s option' % top2["id"]).count() - 1 if third_row == 0 else -1
    pg.select_option('#crumb-%s select' % top2["id"], mids[-1]["id"])
    learn_tabs = [pg.locator('[data-pane="%s"] .viewsub [data-tab]' % top2["id"]).nth(k).get_attribute("data-tab") for k in range(pg.locator('[data-pane="%s"] .viewsub [data-tab]' % top2["id"]).count())]
    feat("one top menu; its tab row is the only row of tabs - sub-subjects are chosen from a breadcrumb", pg.locator("#tabs").count() == 0 and labels == ["intro", "learn", "maps", "lab", "agents", "practice", "reference", "about"] and all(t["id"] in learn_tabs for t in tops) and sub_in_pane == len(mids)
         and pg.locator('[data-subpane="%s"]' % mids[-1]["id"]).is_visible() and not pg.locator('[data-subpane="%s"]' % mids[0]["id"]).is_visible(), "top menu: %s" % ", ".join(labels))
    # the explorer drives the main area; the card stays closed
    leaf = [n for n in nodes if n["level"] == 3 and n["parent"] != mids[-1]["id"]][0]
    pg.click("#expandAll"); pg.click('#tree .tn[data-c="%s"]' % leaf["id"]); pg.wait_for_timeout(300)
    feat("menu click changes the main area first, card stays closed", pg.evaluate(in_view, "s-" + leaf["id"]) and pg.locator("#card").is_hidden(), leaf["label"])
    pg.click('[data-detail="%s"]' % leaf["id"]); opened = pg.locator("#card").is_visible() and leaf["label"] in pg.text_content("#card")
    pg.click("#card [data-close]"); closed = pg.locator("#card").is_hidden()
    pg.click('[data-detail="%s"]' % leaf["id"]); pg.keyboard.press("Escape")
    feat("detail card only on explicit request; closes by button and Esc", opened and closed and pg.locator("#card").is_hidden())
    pg.click('#tree .tn[data-c="%s"]' % leaf["id"], button="right"); menu_ok = pg.is_visible("#ctx"); pg.locator('#ctx [data-cmd^="card:"]').click()
    feat("context menu offers details on request", menu_ok and pg.locator("#card").is_visible()); pg.keyboard.press("Escape")
    pg.hover('#tree .tn[data-c="%s"]' % leaf["id"]); feat("tooltips", pg.is_visible("#tip"))
    view("map"); gi = pg.evaluate("()=>{const l=[...document.querySelectorAll('#graph g.gn')];for(let i=3;i<l.length;i++){const r=l[i].getBoundingClientRect(),e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);if(e&&l[i].contains(e))return i}return 3}"); g = pg.locator("#graph g.gn").nth(gi); gid = g.get_attribute("data-c"); g.click(); pg.wait_for_timeout(300)
    feat("tapping a map node shows its options in the detail card; the main area stays where it was", pg.locator("#card").is_visible() and ("Go to its section" in pg.text_content("#card")) and pg.locator('[data-pane="map"]').is_visible(), gid)
    pg.keyboard.press("Escape")
    view("taxonomy"); feat("taxonomy diagram", pg.locator("#taxo svg g.on").count() > len(nodes) and pg.locator("#taxo svg g.n.root").count() == 1)
    # widgets
    for n in nodes:
        w = "w-" + n["id"]; ok = False; why = ""
        try:
            pg.evaluate("id=>goTo(id)", n["id"])
            if "io" in n:
                pg.fill("#%s-code" % w, n["io"]["code"]); pg.fill("#%s-guess" % w, n["io"]["out"]); pg.click('[data-run="%s"]' % n["id"])
                pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent&&o.textContent!=='running...'}", arg=w + "-out", timeout=120000)
                got = pg.text_content("#%s-out" % w); ok = got == n["io"]["out"] and "matched" in pg.text_content("#%s-verdict" % w); why = "printed %r" % got
                pg.fill("#%s-code" % w, "2 + 2"); pg.click('[data-run="%s"]' % n["id"])
                pg.wait_for_function("id=>{const o=document.getElementById(id);return o&&o.textContent!=='running...'}", arg=w + "-out", timeout=60000)
                edited = pg.text_content("#%s-out" % w); ok = ok and edited == "4"; why += "; edited to 2 + 2 printed %r" % edited
                pg.click('[data-reset="%s"]' % n["id"]); ok = ok and pg.input_value("#%s-code" % w) == n["io"]["code"]
                pg.click('[data-detail="%s"]' % n["id"]); shown = pg.locator("#card output.out").first.text_content().split("\n", 1)[-1]; pg.keyboard.press("Escape")
                ok = ok and shown == n["io"]["out"]; why += "; card shows %r" % shown
            elif n.get("chart"):
                pg.wait_for_function("id=>{const c=document.getElementById(id);const ch=c&&window.Chart&&Chart.getChart(c);return ch&&ch.data.datasets.some(x=>x.data&&x.data.length)&&c.offsetWidth>0}", arg=n["chart"], timeout=20000)
                ok = True; why = "chart %s drawn" % n["chart"]
            elif n["level"] == 3:
                ex = pg.text_content("#%s pre.exs" % w); ok = ex == n["example"] and pg.locator("#%s [data-step]" % w).count() == 0 and "Walk through it" not in pg.text_content("#%s" % w); why = "static example shown; no step button"
            elif n["level"] == 1:
                card = pg.locator("#%s .ovcard" % w).first; sub = card.get_attribute("data-sub"); card.click(); pg.wait_for_timeout(200)
                ok = pg.locator('[data-subpane="%s"]' % sub).is_visible() and pg.locator("#%s .ovcard" % w).count() == len([m for m in nodes if m["parent"] == n["id"]]); why = "overview card opens its sub-subject"
            else:
                leaves = [m["id"] for m in nodes if m["parent"] == n["id"]]
                ok = pg.locator("#%s > section.leaf" % w).count() == len(leaves) and pg.locator("#%s" % w).is_visible(); why = "grid shows its %d concepts" % len(leaves)
        except Exception as e:
            ok, why = False, "%s: %s" % (type(e).__name__, str(e)[:100])
        R["widgets"][w] = {"passed": ok, "detail": why}
    PG_DEF = pg.evaluate("D.course.playground.code")
    ios = [n for n in nodes if "io" in n]
    feat("edited code really runs: every example re-run after editing prints the new result", all(R["widgets"]["w-" + n["id"]]["passed"] for n in ios), "%d examples" % len(ios))
    view("play"); opts = pg.locator("#pex option"); sel_ok = True
    for k in range(min(opts.count(), 4)):
        v = opts.nth(k).get_attribute("value"); pg.select_option("#pex", v)
        want = PG_DEF if v == "first" else next(n_ for n_ in nodes if n_["id"] == v)["io"]["code"]; sel_ok &= pg.input_value("#pcode") == want
    feat("choosing an example in the Playground fills the code at once, with no Load button", sel_ok and pg.locator("#pload").count() == 0, "%d examples" % opts.count())
    tpls = [o.get_attribute("value") for o in pg.locator("#pex option").all() if (o.get_attribute("value") or "").startswith("tpl:")]; bad_t = []
    for v in tpls:
        pg.select_option("#pex", v); pg.wait_for_timeout(700); pg.click("#prun"); pg.wait_for_function("()=>{const o=document.getElementById('pout');return o&&o.textContent.trim().length>0&&!/Running/.test(o.textContent)}", timeout=60000); o_ = pg.text_content("#pout")
        if re.search(r"Traceback|Error|Exception", o_): bad_t.append((v, o_[:60]))
    feat("the Playground has ONE list; its code patterns are complete programs and every one runs without an error", len(tpls) >= 15 and not bad_t and pg.locator('[data-pane="play"] [data-edtpl]').count() == 0 and pg.locator('[data-pane="play"] select:not(.edsel)').count() == 1, "%d patterns; %s" % (len(tpls), bad_t[:2]))
    view("play"); pg.fill("#pcode", "x = 7\nx * 6"); pg.click("#prun")
    pg.wait_for_function("()=>document.getElementById('pout').textContent!=='running...'", timeout=60000); free = pg.text_content("#pout")
    feat("playground runs code typed from scratch", free == "42", repr(free))
    # agents answer from their own slice: different questions, different answers
    a = max(d["agents"], key=lambda x: len(x["covers"])); view("agents")
    pg.click('[data-agenttab="%s"]' % a["id"])
    q1 = [n for n in nodes if n["id"] == a["covers"][0]][0]["label"]; q2 = [n for n in nodes if n["id"] == a["covers"][-2]][0]["label"] if len(a["covers"]) > 2 else a["covers"][-1]
    def ask(q):
        before = pg.locator("#%s-log .msg" % a["id"]).count(); pg.fill("#%s-q" % a["id"], q); pg.click('[data-ask="%s"]' % a["id"])
        pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=[a["id"], before], timeout=240000)
        return pg.locator("#%s-log .msg" % a["id"]).last.text_content()
    ans1, ans2 = ask("what is " + q1.lower()), ask("what is " + q2.lower() + " used for in a program?"); ans3 = ask("how do I bake bread")
    feat("agents answer from their own slice; different questions get different answers", ans1 != ans2 and len(ans1) > 40 and len(ans2) > 40 and ("Nothing in the book, course or chapter material answers that" in ans3),
         "%s | %s | %s" % (ans1[:60], ans2[:60], ans3[:60]))
    st = pg.text_content(".kitstat"); kinds = pg.evaluate("()=>[...new Set(KIT.chunks.map(c=>c.kind))].sort()")
    files = pg.evaluate("()=>document.querySelectorAll('script[data-kind]').length")
    how = pg.locator("#%s-log .msg details pre" % a["id"]).first.text_content(); cites = pg.locator("#%s-log .msg .src" % a["id"]).count()
    feat("agents search a knowledge graph of the book, course and chapter ontologies, the research record and this page", "Knowledge graph: ready" in st and ("from %d files" % files) in st and kinds == sorted(CFG["corpus_kinds"]), st + " | kinds " + ",".join(kinds))
    feat("agents rank by meaning (sentence embeddings) and show how they found the answer", "Semantic search: ready" in st and "SPARQL" in how and "rows:" in how and cites > 0, "%d cited passages" % cites)
    q_out = pg.evaluate("async([id,q])=>{const a=D.agents.find(x=>x.id===id);const r=await rank(a,q,8);return r.top.map(x=>x.c.label).join(' | ')}", [a["id"], CFG["course_q"]])
    feat("a course question reaches the course ontology", CFG["course_lo"] in q_out, q_out[:150]) if COURSE_OUT else skip("a course question reaches the course ontology", "test_config course_outcomes is false: SEN0401 has no course ontology yet")
    pg.click("#llmbtn"); pg.wait_for_timeout(1500); llm = pg.text_content(".kitstat").split("Live LLM:")[1].strip()
    feat("live LLM is capability-checked; without WebGPU the agents keep working and say so", llm.startswith("unavailable") or llm.startswith("ready") or llm.startswith("downloading"), llm[:90])
    lt = pg.evaluate("window.__lt"); R["gates"]["longest main-thread task (ms)"] = max(lt or [0])
    feat("no main-thread task over 200 ms through the whole session (graph, embeddings, Python, agents)", max(lt or [0]) <= 200, "longest %d ms over %d long tasks" % (max(lt or [0]), len(lt)))
    view("play"); pg.fill("#pcode", "while True:\n    pass"); t0 = time.time(); pg.click("#prun"); pg.wait_for_timeout(1500)
    t1 = time.time(); view("glossary"); responsive = (time.time() - t1) < 1.0 and pg.locator('[data-pane="glossary"]').is_visible()
    view("play"); pg.wait_for_function("()=>document.getElementById('pout').textContent.startsWith('Stopped after')", timeout=40000); stopped_in = time.time() - t0
    pg.fill("#pcode", "6 * 7"); pg.click("#prun"); pg.wait_for_function("()=>document.getElementById('pout').textContent==='42'", timeout=90000)
    feat("an endless program is stopped; the page stays responsive while it runs; Python works again after", responsive, "stopped after %.0f s; menu answered during the loop; fresh Python printed 42" % stopped_in)
    # ---- the conversation view ----
    view("agents"); pg.wait_for_timeout(200)
    roster = pg.locator(".roster .persona"); icons = [roster.nth(k).locator(".av").text_content() for k in range(roster.count())]
    feat("agents are listed like people: role icons, what each knows, a guide first", roster.count() == len(d["agents"]) + 1 and icons[0] == "🧭" and "🤖" not in icons and all((pg.locator('[data-agenttab="%s"]' % x["id"]).get_attribute("data-tip") or "").startswith("Ask me about") for x in d["agents"]), " ".join(icons))
    pg.click('[data-agenttab="guide"]'); gl = pg.locator("#guide-log .msg").count(); pg.fill("#guide-q", CFG["guide_q"]); pg.press("#guide-q", "Enter")
    pg.wait_for_function("n=>{const m=document.querySelectorAll('#guide-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=gl, timeout=120000)
    sugg = [pg.locator("#guide-log .msg").last.locator("[data-handoff]").nth(k).get_attribute("data-handoff") for k in range(pg.locator("#guide-log .msg").last.locator("[data-handoff]").count())]
    target = CFG["agent"]
    pg.locator('#guide-log .msg').last.locator('[data-handoff="%s"]' % target).click()
    pg.wait_for_function("id=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=3&&!m[m.length-1].classList.contains('typing')}", arg=target, timeout=120000)
    feat("the guide introduces the right agent and hands the question over", target in sugg and pg.locator('[data-conv="%s"]' % target).is_visible(), "suggested: " + ", ".join(sugg))
    def say(q):
        n = pg.locator("#%s-log .msg" % target).count(); pg.fill("#%s-q" % target, q); pg.press("#%s-q" % target, "Enter")
        pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=[target, n], timeout=120000)
        return pg.locator("#%s-log .msg" % target).last.inner_text()
    root = CFG["root"]
    r1 = say(root); r2 = say("can you give me an example?"); r3 = say("and why?")
    feat("follow-up questions are answered in the context of the conversation", ('Following on from "%s"' % root) in r2 and ('Following on from "%s"' % root) in r3 and "for example:" in r2.lower(), r2[:90].replace("\n", " "))
    kept = pg.locator("#%s-log .msg" % target).count(); pg.reload(); view("agents"); pg.wait_for_timeout(400)
    feat("conversations are remembered across a reload", pg.locator("#%s-log .msg" % target).count() == kept and pg.locator('[data-conv="%s"]' % target).is_visible(), "%d messages kept" % kept)
    # ---- the fit-gap views ----
    view("howto"); howto = pg.text_content('[data-pane="howto"] .prose')
    view("arch"); arch_rows = pg.locator('#archout table').last.locator("tr").count() - 1
    view("mission"); pg.wait_for_function("()=>!document.getElementById('missionout').textContent.includes('reading the course ontology')", timeout=60000); mission = pg.text_content("#missionout")
    view("prov"); limits = pg.locator("#provout ul li").count()
    feat("About: how it works, agents & tools with the corpus, mission & backlog with course outcomes, provenance & known limits", len(howto) > 400 and arch_rows == files and "Mission" in mission and (not COURSE_OUT or "LO-1" in mission) and limits >= 4, "corpus rows %d, limits %d" % (arch_rows, limits))
    view("sparql"); pg.click("#sqrun"); pg.wait_for_function("()=>/result/.test(document.getElementById('sqstat').textContent)||document.querySelector('#sqres .err')", timeout=60000)
    rows = pg.locator("#sqres tr").count() - 1
    pg.click("#sqcsv"); pg.wait_for_timeout(200); csv_copy = pg.evaluate("navigator.clipboard.readText()")
    pg.select_option("#sqsamp", "5"); sel_ok = pg.evaluate("()=>document.getElementById('sqtext').value===SPARQL_SAMPLES[5][1]&&!document.getElementById('sqload')"); pg.click("#sqrun"); pg.wait_for_function("()=>/result/.test(document.getElementById('sqstat').textContent)", timeout=60000); ask_ans = pg.text_content("#sqres")
    feat("SPARQL console: editable queries over the knowledge graph, results table, results copied as CSV, ASK", rows > 5 and csv_copy.count("\n") >= rows and ask_ans.strip() in ("Yes", "No"), "%d rows; ASK -> %s" % (rows, ask_ans.strip()))
    feat("choosing a SPARQL sample loads it at once; no Load sample button", sel_ok)
    view("play"); pg.fill("#pcode", "print('hello')")
    pg.click('[data-dl="pcode"]'); pg.wait_for_timeout(200); code_copy = pg.evaluate("navigator.clipboard.readText()")
    view("mydata")
    pg.click("#dlconvmd"); pg.wait_for_timeout(200); conv_md = pg.evaluate("navigator.clipboard.readText()")
    feat("copying out: playground code, SPARQL results, conversations - to the clipboard, with no file built and saved by the page", code_copy == "print('hello')" and conv_md.startswith("# Conversations") and pg.locator("#mydataout tr").count() >= 1, "code, CSV and %d characters of conversation copied" % len(conv_md))
    view("agents"); pg.wait_for_timeout(200)
    pg.click('[data-newconv="%s"]' % target); feat("a new conversation starts clean", pg.locator("#%s-log .msg" % target).count() == 1)
    view("browse"); chips = pg.locator("#browse [data-browseq]"); nchips = chips.count(); qtext = chips.first.text_content(); target_b = chips.first.get_attribute("data-browseq")
    nb = pg.locator("#%s-log .msg" % target_b).count(); chips.first.click()
    pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=[target_b, nb], timeout=120000)
    feat("browse questions by subject; choosing one asks the right agent", nchips > 10 and pg.locator('[data-conv="%s"]' % target_b).is_visible(), "%d questions; '%s' went to %s" % (nchips, qtext, target_b))
    view("expert"); pg.click('[data-role="data analyst"]'); pg.wait_for_function("()=>document.querySelectorAll('#exout [data-expertq]').length>0", timeout=60000); ne = pg.locator("#exout [data-expertq]").count()
    eqt = pg.locator("#exout [data-expertq]").first.text_content(); pg.locator("#exout [data-expertq]").first.click()
    pg.wait_for_function("q=>{const c=document.querySelector('.conv:not([hidden])');if(!c)return false;const m=c.querySelectorAll('.msg');return m.length>=3&&!m[m.length-1].classList.contains('typing')&&[...c.querySelectorAll('.msg.me')].some(x=>x.textContent===q)}", arg=eqt, timeout=120000)
    feat("expert questions for a role; choosing one asks the best-fitting agent", ne >= 5 and "data analyst" in eqt, "%d questions, e.g. %s" % (ne, eqt))
    view("checks"); pg.click("#ckrun"); pg.wait_for_function("()=>/checks pass/.test(document.getElementById('ckstat').textContent)", timeout=240000); ck = pg.text_content("#ckstat")
    a_, b_ = [int(x) for x in ck.split(" checks")[0].split(" of ")]
    feat("built-in checks: every stored example re-run, agents' citations, an off-topic refusal - all pass in the page", a_ == b_ and b_ > 10, ck)
    view("codelab"); pg.select_option("#clsnip", "3"); code_fill = pg.input_value("#clcode"); pg.click("#clrun"); pg.wait_for_function("()=>{const t=document.getElementById('clout').textContent;return t&&t!=='running...'}", timeout=120000)
    cl = pg.text_content("#clout"); n_io = len([n for n in nodes if "io" in n])
    feat("Code Lab: Python over this page's own data re-runs every example", cl.count("same |") == n_io and "DIFFERENT" not in cl, "%d of %d examples the same" % (cl.count("same |"), n_io))
    feat("choosing a Code Lab snippet fills the code at once, with no Load button", code_fill == pg.evaluate("CODELAB_SNIPPETS[3][1]") and pg.locator("#clload").count() == 0)
    # ---- version 8 ----
    view(tops[0]["id"]); pg.select_option('#crumb-%s select' % tops[0]["id"], "ov-" + tops[0]["id"])
    dup = pg.evaluate("()=>[...document.querySelectorAll('[data-pane]')].filter(p=>byId[p.dataset.pane]&&byId[p.dataset.pane].level===1).reduce((a,p)=>a+p.querySelectorAll('.chip').length,0)")
    feat("subject screens carry no repeated lists: an overview sub-tab, one-sentence sub-subject headers", dup == 0 and pg.locator('[data-pane="%s"] .ovcard' % tops[0]["id"]).count() > 0 and pg.locator("details.more").count() == len([n for n in nodes if n["level"] == 2]), "0 duplicate chip rows")
    view("taxonomy"); tx = pg.evaluate("()=>{const g=[...document.querySelectorAll('#taxo g.n,#taxo g.on')];return {svgs:document.querySelectorAll('#taxo svg').length,boxes:document.querySelectorAll('#taxo g.n').length,root:document.querySelectorAll('#taxo g.n.root').length,overflow:g.filter(x=>x.querySelector('text').getBBox().width>x.querySelector('rect').getBBox().width+0.5).length}}")
    feat("one taxonomy tree rooted at the chapter, every label inside its box", tx["svgs"] == 1 and tx["root"] == 1 and tx["boxes"] == 1 and tx["overflow"] == 0, str(tx))
    helps = pg.evaluate("()=>[...document.querySelectorAll('details.help')].map(d=>d.open)")
    feat("view introductions are folded until asked for", len(helps) >= 8 and not any(helps), "%d folded" % len(helps))
    zooms = []
    for k, sel in (("taxonomy", "#taxo"), ("map", "#graph"), ("ontograph", "#onto")):
        view(k)
        if k == "ontograph": pg.wait_for_function("()=>document.querySelector('#onto svg')", timeout=60000)
        v0 = pg.get_attribute("%s svg" % sel, "viewBox"); pg.click('%s [data-z="in"]' % sel); v1 = pg.get_attribute("%s svg" % sel, "viewBox"); pg.click('%s [data-z="reset"]' % sel); v2 = pg.get_attribute("%s svg" % sel, "viewBox")
        zooms.append(v1 != v0 and (v2 == v0 or v2 == pg.get_attribute("%s svg" % sel, "data-vb0")))
    pg.evaluate("goTo('%s')" % [n for n in nodes if "io" in n][0]["id"]); pg.click('[data-diagram="%s"]' % [n for n in nodes if "io" in n][0]["id"])
    zooms.append(pg.locator('#w-%s-diagram .zbar' % [n for n in nodes if "io" in n][0]["id"]).count() == 1)
    feat("zoom in, zoom out and show-all on every diagram (taxonomy, concept map, ontology graph, parse trees)", all(zooms), str(zooms))
    # ---- version 9: visualisations ----
    evs = [n for n in nodes if "io" in n and len(n["io"].get("steps", [])) > 1]
    ok_ev = True
    for n in evs:
        pg.evaluate("goTo('%s')" % n["id"]); pg.click('[data-evtoggle="%s"]' % n["id"])
        for st in n["io"]["steps"]:
            ok_ev &= st["value"] in pg.text_content("#ev-%s" % n["id"]); pg.click('[data-evnext="%s"]' % n["id"])
        ok_ev &= pg.text_content("#ev-%s" % n["id"]) == n["io"]["out"]
    feat("evaluation steps: each example replays Python's own reduction, one operation at a time, ending on the stored result", ok_ev, "%d multi-step examples (a chapter of statements has none; the stepper is then absent, not broken)" % len(evs))
    view("trace"); pg.fill("#trcode", "total = 0\nfor n in range(1, 5):\n    total = total + n\nprint(total)"); pg.click("#trnext")  # no Trace button: the first Step traces the program
    pg.wait_for_function("()=>/steps/.test(document.getElementById('trstat').textContent)", timeout=120000)
    first_pos = pg.text_content("#trpos"); no_trace_btn = pg.locator("#trgo").count() == 0; nsteps = int(pg.text_content("#trstat").split()[0])
    pg.click("#trfirst"); [pg.click("#trnext") for _ in range(nsteps - 1)]; last_out = pg.text_content("#trout").strip(); tot = [r for r in pg.locator("#trvars tr").all_inner_texts() if r.startswith("total")]
    feat("step through: Python's line tracer records every line, the variables after it and the output", nsteps > 8 and last_out == "10" and tot and "10" in tot[0], "%d steps, output %s" % (nsteps, last_out) + "; first Step showed '%s'" % first_pos)
    feat("Step through starts on the first Step: no Trace button, the program is traced and its first line shown", no_trace_btn and first_pos.startswith("step 1 of"), first_pos)
    # every example offered by Step through traces from a plain selection followed by Step; changing the code traces again
    ex_ok = True; nex = pg.locator("#trex option").count()
    for k in range(nex):
        pg.select_option("#trex", str(k)); pg.wait_for_function("()=>/steps|ended|Error|error/.test(document.getElementById('trstat').textContent)", timeout=120000)
        ex_ok &= pg.input_value("#trcode").strip() != "" and pg.text_content("#trpos").startswith("step 1 of"); pg.click("#trnext"); ex_ok &= pg.text_content("#trpos").startswith("step 2 of")
    pg.fill("#trcode", "y = 1\ny = y + 41\nprint(y)"); pg.click("#trnext"); pg.wait_for_function("()=>document.getElementById('trpos').textContent.startsWith('step 1 of 3')||/step 1 of/.test(document.getElementById('trpos').textContent)", timeout=60000); retrace = pg.text_content("#trstat")
    feat("Step through offers examples, each traced when chosen; editing the code and pressing Step traces the new program", ex_ok and nex >= 4 and retrace.startswith("4 steps"), "%d examples; edited program: %s" % (nex, retrace))
    feat("the Lab has no Code pipeline view (it was removed: one list of examples, in the Playground)", pg.locator('[data-tab="pipeline"]').count() == 0 and pg.locator("#ppex").count() == 0, "")
    # ---- 9.11.0: the 13 kinds of chapter 6 - helpers ----
    NEWKINDS = ["boxes", "classify", "facts", "hist", "keysort", "lanes", "matrix", "mutation", "passes", "refgraph", "seqtypes", "slices", "unpack"]
    T = lambda sel: pg.evaluate("s=>[...document.querySelectorAll(s)].map(e=>e.textContent)", sel)
    def zoom_check(cid):
        sel = "#wv-%s-out" % cid
        if pg.locator(sel + " .zbar").count() != 1 or pg.locator(sel + " .diagram.vz svg").count() != 1: return "no zoom bar or no diagram"
        v0 = pg.get_attribute(sel + " svg", "viewBox"); pg.click(sel + ' [data-z="in"]'); v1 = pg.get_attribute(sel + " svg", "viewBox"); pg.click(sel + ' [data-z="out"]'); pg.click(sel + ' [data-z="in"]'); pg.click(sel + ' [data-z="reset"]'); v2 = pg.get_attribute(sel + " svg", "viewBox")
        return "" if (v1 != v0 and v2 == v0) else "zoom in/reset did not work (%s | %s | %s)" % (v0, v1, v2)
    def open_vis(cid):
        pg.evaluate("goTo('%s')" % cid)
        if pg.evaluate("id=>document.getElementById('wvp-'+id).hidden", cid): pg.click('[data-vistoggle="%s"]' % cid)
    RG_JS = """w=>{const o=document.getElementById(w+'-out');
 const rect=oid=>{const r=o.querySelector('g.rgo[data-oid="'+oid+'"] > rect.rgb');return r?[+r.getAttribute('x'),+r.getAttribute('y'),+r.getAttribute('width'),+r.getAttribute('height')]:null};
 const end=p=>{const n=p.getAttribute('d').match(/-?[0-9.]+/g).map(Number);return [n[n.length-2],n[n.length-1]]};
 return {names:[...o.querySelectorAll('g.rgn')].map(g=>[g.dataset.name,g.dataset.oid,g.querySelector('text').textContent]),
  arrows:[...o.querySelectorAll('path.rga')].map(p=>[p.dataset.name,p.dataset.oid,end(p),rect(p.dataset.oid)]),
  objs:[...o.querySelectorAll('g.rgo')].map(g=>[g.dataset.oid,[...g.querySelectorAll('text.rgt')].map(t=>t.textContent),[...g.querySelectorAll('g.rgi[data-ref]')].map(i=>i.dataset.ref),g.querySelectorAll('g.rgi').length]),
  refs:[...o.querySelectorAll('path.rgr')].map(p=>[p.dataset.from,+p.dataset.i,p.dataset.oid,end(p),rect(p.dataset.oid)]),
  cap:o.querySelector('.rgcap').textContent,scopes:[...o.querySelectorAll('.rgsc')].map(t=>t.textContent)}}"""
    KS_JS = """w=>{const o=document.getElementById(w+'-out'),cx=r=>+r.getAttribute('x')+ +r.getAttribute('width')/2;
 return {expr:o.querySelector('.kse').textContent,items:[...o.querySelectorAll('g.ksi text')].map(t=>t.textContent),keys:[...o.querySelectorAll('text.ksk')].map(t=>t.textContent),out:[...o.querySelectorAll('g.kso text')].map(t=>t.textContent),
  lines:[...o.querySelectorAll('line.ksln')].map(l=>[+l.dataset.from,+l.dataset.to,+l.getAttribute('x1'),+l.getAttribute('x2')]),inX:[...o.querySelectorAll('g.ksi rect')].map(cx),outX:[...o.querySelectorAll('g.kso rect')].map(cx)}}"""
    def check_new(cid, v, w):
        ok = False; why = ""
        bad = []; chk = lambda c, m: (None if c else bad.append(m)); K = v["kind"]; out = "#%s-out" % w
        if K == "boxes":
            n = len(v["list"]); pg.click('[data-nv="%s:pick:all"]' % cid)
            cells = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out .bxc:not(.ghost)')].map(c=>[c.querySelector('.ix').textContent,c.querySelector('.it').textContent,c.querySelector('.nx').textContent])", w)
            chk(cells == [[str(i), t, str(i - n)] for i, t in enumerate(v["list"])], "index labels or items differ: %s" % cells)
            hitjs = "w=>[...document.querySelectorAll('#'+w+'-out .bxc:not(.ghost)')].flatMap((c,i)=>c.classList.contains('hit')?[i]:[])"
            chk(pg.evaluate(hitjs, w) == sorted({a for p in v["picks"] for a in p["at"]}), "show all: highlighted boxes %s" % pg.evaluate(hitjs, w))
            for i, p in enumerate(v["picks"]):
                pg.click('[data-nv="%s:pick:%d"]' % (cid, i)); hit = pg.evaluate(hitjs, w)
                chk(hit == sorted(p["at"]), "pick %s highlights %s, not %s" % (p["expr"], hit, p["at"]))
                chk(pg.text_content('[data-nv="%s:pick:%d"] .pe' % (cid, i)) == p["expr"] and pg.text_content('[data-nv="%s:pick:%d"] .rs' % (cid, i)) == p["result"], "pick text of %s" % p["expr"])
            if v.get("error"):
                pg.click('[data-nv="%s:pick:e"]' % cid)
                chk(pg.locator(out + " .bxc.ghost").count() == 1 and pg.evaluate(hitjs, w) == [], "error: a dashed empty box after the last one and nothing highlighted")
                chk(pg.text_content('[data-nv="%s:pick:e"] .pe' % cid) == v["error"]["expr"] and pg.text_content('[data-nv="%s:pick:e"] .rs' % cid) == v["error"]["message"], "error text")
            else: chk(pg.locator(out + " .bxc.ghost").count() == 0, "a ghost box without an error")
            pg.click('[data-nv="%s:pick:all"]' % cid); why = "%d boxes with front and back indexes; %d picks each light their boxes%s" % (n, len(v["picks"]), "; the error shows an empty box and its message" if v.get("error") else "")
        if K == "slices":
            n = len(v["list"]); chk(T(out + " .slr.hdr .sli") == [str(i) for i in range(n)], "header indexes")
            for r, R_ in enumerate(v["rows"]):
                pg.click('[data-nv="%s:row:%d"]' % (cid, r))
                row = pg.evaluate("a=>{const b=document.querySelectorAll('#'+a[0]+'-out button.slr')[a[1]];return {x:b.querySelector('.slx').textContent,res:b.querySelector('.slres').textContent,pl:b.querySelector('.slp').textContent,cells:[...b.querySelectorAll('.slc')].map(c=>[c.querySelector('.itx').textContent,c.classList.contains('on'),(c.querySelector('.ord')||{}).textContent||null]),sel:b.classList.contains('sel')}}", [w, r])
                chk(row["x"] == R_["expr"] and row["res"] == R_["result"] and row["pl"] == R_["picked_label"], "row %d text" % r)
                chk([c[0] for c in row["cells"]] == v["list"], "row %d items" % r)
                chk([i for i, c in enumerate(row["cells"]) if c[1]] == sorted(R_["picked"]), "row %d (%s) selects %s, not %s" % (r, R_["expr"], [i for i, c in enumerate(row["cells"]) if c[1]], R_["picked"]))
                chk(row["sel"] and all(row["cells"][i][2] == str(k + 1) for k, i in enumerate(R_["picked"])), "row %d order numbers" % r)
            pg.click('[data-nv="%s:row:%d"]' % (cid, len(v["rows"]) - 1)); chk(pg.locator(out + " .ord").count() == 0, "order numbers stay after the row is chosen again")
            why = "%d rows: expression, result, label and the selected indexes match; the order numbers follow the slice" % len(v["rows"])
        if K == "lanes":
            for i, L in enumerate(v["lanes"]):
                pg.click('[data-nv="%s:lane:%d"]' % (cid, i))
                ln = pg.evaluate("a=>{const b=document.querySelectorAll('#'+a[0]+'-out button.lane')[a[1]];const cl=s=>[...b.querySelectorAll(s+' .cl')].map(c=>[c.textContent,c.classList.contains('rm'),c.classList.contains('add')]);return {op:b.querySelector('.lop').textContent,name:b.querySelector('.lname').textContent,cat:b.querySelector('.lcat').textContent,ret:b.querySelector('.lret').textContent,retnone:b.querySelector('.lret').classList.contains('none'),id:b.querySelector('.lid').textContent,same:b.querySelector('.lid').classList.contains('same'),before:cl('.lb'),after:cl('.la'),det:(b.querySelector('.ldet')||{}).textContent||'',sel:b.classList.contains('sel')}}", [w, i])
                chk(ln["op"] == L["op"] and ln["name"] == L["name"] and ln["cat"] == L["cat_label"], "lane %d op/name/category" % i)
                chk(ln["ret"] == L["ret_label"] and ln["retnone"] == (L["returns"] is None), "lane %d returned value" % i)
                chk(ln["id"] == "same object: " + ("yes" if L["same_object"] else "no") and ln["same"] == L["same_object"], "lane %d same-object flag: %s" % (i, ln["id"]))
                chk([c[0] for c in ln["before"]] == L["before"] and [c[0] for c in ln["after"]] == L["after"], "lane %d before/after lists" % i)
                chk([k for k, c in enumerate(ln["before"]) if c[1]] == L["before_marks"] and not any(c[2] for c in ln["before"]), "lane %d marks in the before list" % i)
                chk([k for k, c in enumerate(ln["after"]) if c[2]] == L["after_marks"] and not any(c[1] for c in ln["after"]), "lane %d marks in the after list" % i)
                chk(ln["sel"] and all(L["before"][k] in ln["det"] for k in L["before_marks"]) and all(L["after"][k] in ln["det"] for k in L["after_marks"]) and (("same list object" in ln["det"]) == L["same_object"]), "lane %d detail line: %s" % (i, ln["det"][:80]))
            chk(T(out + " .lerr") == [e["expr"] + " → " + e["message"] for e in v["errors"]], "error lines")
            why = "%d operations: before and after lists, marked boxes, returned value and same-object flag match; %d error lines" % (len(v["lanes"]), len(v["errors"]))
        if K == "hist":
            rows = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out tr')].map(r=>[r.querySelector('.hl').textContent,r.querySelector('.hn').textContent,r.querySelector('.hbar').getBoundingClientRect().width])", w)
            mx = max(b_["count"] for b_ in v["bars"]); wmax = max(r[2] for r in rows)
            chk(len(rows) == len(v["bars"]), "number of bars")
            for b_, r in zip(v["bars"], rows): chk(r[0] == b_["text"] and r[1] == str(b_["count"]) and abs(r[2] / wmax - b_["count"] / mx) < .02, "bar %s: %s" % (b_["text"], r))
            chk(sum(b_["count"] for b_ in v["bars"]) == v["draws"], "the counts add up to the draws")
            why = "%d bars: label, count and bar length match; the counts add up to %d draws" % (len(rows), v["draws"])
        if K == "refgraph":
            npass = 0
            for si, S in enumerate(v["scenarios"]):
                if len(v["scenarios"]) > 1: pg.click('[data-nv="%s:sc:%d"]' % (cid, si))
                for sti, St in enumerate(S["steps"]):
                    if sti: pg.click('[data-nv="%s:st:1"]' % cid)
                    g = pg.evaluate(RG_JS, w); tag = "scenario %d step %d" % (si + 1, sti + 1); want = sorted((n_, oid) for sc in St["scopes"] for n_, oid in sc["names"])
                    chk(g["cap"] == St["code"], tag + " caption")
                    chk(sorted((a[0], a[1]) for a in g["names"]) == want and all(a[0] == a[2] for a in g["names"]), tag + " names %s" % g["names"])
                    chk(sorted((a[0], a[1]) for a in g["arrows"]) == want, tag + " arrows")
                    for a in g["arrows"]: chk(a[3] and abs(a[2][0] - a[3][0]) < 1 and a[3][1] <= a[2][1] <= a[3][1] + a[3][3], tag + " the arrow of %s ends on the frame of its object" % a[0])
                    reach = set(); todo = [oid for _, oid in want]
                    while todo:
                        o_ = todo.pop()
                        if o_ in reach: continue
                        reach.add(o_); ob = St["objects"][o_]
                        if ob["type"] == "list": todo += [it["ref"] for it in ob["items"] if it.get("ref")]
                    chk({o_[0] for o_ in g["objs"]} == reach, tag + " objects drawn %s vs %s" % ([o_[0] for o_ in g["objs"]], sorted(reach)))
                    for o_ in g["objs"]:
                        ob = St["objects"][o_[0]]
                        if ob["type"] == "list": chk(o_[1] == [it["v"] for it in ob["items"] if not it.get("ref")] and o_[2] == [it["ref"] for it in ob["items"] if it.get("ref")] and o_[3] == len(ob["items"]), tag + " items of %s: %s" % (o_[0], o_[1]))
                        else: chk(o_[1] == [ob["v"]], tag + " value of %s" % o_[0])
                    wantrefs = sorted((o_, i, it["ref"]) for o_, ob in St["objects"].items() if o_ in reach and ob["type"] == "list" for i, it in enumerate(ob["items"]) if it.get("ref"))
                    chk(sorted((r[0], r[1], r[2]) for r in g["refs"]) == wantrefs, tag + " reference arrows")
                    for r in g["refs"]: chk(r[4] and abs(r[3][0] - r[4][0]) < 1 and r[4][1] <= r[3][1] <= r[4][1] + r[4][3], tag + " a reference arrow ends on its object")
                    chk(g["scopes"] == ([sc["scope"] for sc in St["scopes"]] if len(St["scopes"]) > 1 else []), tag + " scope labels %s" % g["scopes"])
                    npass += 1
            zc = zoom_check(cid); chk(not zc, "zoom: " + zc)
            z0 = pg.get_attribute(out + " svg", "viewBox"); pg.click(out + ' [data-z="in"]'); z1 = pg.get_attribute(out + " svg", "viewBox"); pg.click('[data-nv="%s:st:-1"]' % cid); z2 = pg.get_attribute(out + " svg", "viewBox"); chk(z1 != z0 and z2 == z1, "a redrawn step keeps the zoomed view"); pg.click(out + ' [data-z="reset"]')
            why = "%d steps: every name reaches the object its arrow ends on, every item and reference arrow matches; zoom keeps its view" % npass
        if K == "keysort":
            for ei, E in enumerate(v["examples"]):
                pg.click('[data-nv="%s:ex:%d"]' % (cid, ei)); g = pg.evaluate(KS_JS, w); tag = "example %d" % (ei + 1)
                chk(g["expr"] == E["expr"] and g["items"] == E["items"] and g["out"] == E["result"] and g["keys"] == (E["keys"] or []), tag + " texts")
                chk(sorted((l[0], l[1]) for l in g["lines"]) == sorted((s_, p_) for p_, s_ in enumerate(E["order"])), tag + " lines")
                chk(all(abs(l[2] - g["inX"][l[0]]) < .5 and abs(l[3] - g["outX"][l[1]]) < .5 and E["items"][l[0]] == E["result"][l[1]] for l in g["lines"]), tag + " each line joins an input box to the same item in the output")
            zc = zoom_check(cid); chk(not zc, "zoom: " + zc); why = "%d sorts: items, keys, output and the lines from input to output match" % len(v["examples"])
        if K == "matrix":
            nfr = len(v["frames"]); pos = lambda: pg.text_content("#%s-pos" % w)
            for _ in range(nfr): pg.click('[data-nv="%s:fr:-1"]' % cid)
            for a, F in enumerate(v["frames"]):
                chk(pos() == "frame %d of %d" % (a + 1, nfr) and T(out + " .mxl") == [F["label"]] and T(out + " pre.frame .mxr") == F["rows"], "frame %d" % (a + 1))
                pg.click('[data-nv="%s:fr:1"]' % cid)
            chk(pos() == "frame %d of %d" % (nfr, nfr), "the last frame stays")
            chk(T(out + " .hzt") == [H["label"] for H in v["hazard"]] and T(out + " .hzn") == [H["spaces_label"] for H in v["hazard"]] and T(out + " pre.hzg .mxr") + T(out + " pre.hzb .mxr") == [H["row"] for H in v["hazard"]], "hazard rows")
            chk(all(H["row"].count(" ") == H["spaces"] for H in v["hazard"]), "the spaces of a hazard row are the number stated")
            chk(T(out + " table.life th") == v["life_cols"] and pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out table.life tbody tr')].map(r=>[...r.children].map(c=>c.textContent))", w) == [[str(r_["row"]), r_["char"], str(r_["counter"])] for r_ in v["life"]], "the counter table")
            why = "%d frames stepped (rows exact), %d hazard rows, %d counter rows" % (nfr, len(v["hazard"]), len(v["life"]))
        if K == "mutation":
            n = len(v["passes"]); pg.click('[data-nv="%s:mu:reset"]' % cid)
            for r, P in enumerate(v["passes"]):
                row = pg.evaluate("a=>{const rs=[...document.querySelectorAll('#'+a[0]+'-out .mrow')],e=rs[a[1]],cl=s=>[...e.querySelectorAll(s+' .cl')].map(c=>c.textContent);return {vis:rs.filter(x=>!x.hidden).length,head:e.querySelector('.mh').textContent,before:cl('.mb'),cur:[...e.querySelectorAll('.mb .cl')].findIndex(c=>c.classList.contains('cur')),act:e.querySelector('.mact').textContent,after:cl('.ma'),fin:document.querySelectorAll('#'+a[0]+'-out .mfin').length}}", [w, r])
                chk(row["vis"] == r + 1 and row["head"] == P["head"] and row["before"] == P["before"] and row["cur"] == P["pos"] and row["act"] == P["action"] and row["after"] == P["after"], "pass %d: %s" % (r + 1, row))
                chk(pg.text_content("#%s-pos" % w) == "pass %d of %d" % (r + 1, n) and row["fin"] == (1 if r == n - 1 else 0), "pass %d position or final block" % (r + 1))
                if r < n - 1: pg.click('[data-nv="%s:mu:1"]' % cid)
            chk(T(out + " .mfl") == [v["final_label"]] and T(out + " .mfs") == [v["skip_label"]] and T(out + " .mfp") == [v["printed"]], "final block")
            chk(v["original"] == v["passes"][0]["before"] and v["final"] == v["passes"][-1]["after"], "the passes run from the original list to the final one")
            pg.click('[data-nv="%s:mu:-1"]' % cid); chk(pg.locator(out + " .mfin").count() == 0, "Previous hides the final block"); pg.click('[data-nv="%s:mu:reset"]' % cid)
            why = "%d passes stepped: head, list at the start, the position reached, action and list at the end; then the final block" % n
        if K == "passes":
            n = len(v["tables"][0]["rows"]); pg.click('[data-nv="%s:pa:all"]' % cid)
            chk(T(out + " table caption code") == [t_["header"] for t_ in v["tables"]], "table headers")
            chk(pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out table')].map(t=>[[...t.querySelectorAll('th')].map(x=>x.textContent),[...t.querySelectorAll('tbody tr')].map(r=>[...r.children].map(c=>c.textContent))])", w) == [[t_["cols"], t_["rows"]] for t_ in v["tables"]], "table columns and rows")
            chk(T(out + " .nvprint .pl") == v["printed"] and T(out + " .wl")[0] == v["printed_label"], "printed lines")
            chk(T(out + " .nse") == [v["start"]["expr"]] and T(out + " .nsr") == [v["start"]["result"]], "start example")
            for k in range(n):
                pg.click('[data-nv="%s:pa:1"]' % cid)
                now = pg.evaluate("w=>[[...document.querySelectorAll('#'+w+'-out table')].map(t=>[...t.querySelectorAll('tbody tr')].findIndex(r=>r.classList.contains('now'))),[...document.querySelectorAll('#'+w+'-out .pl')].findIndex(p=>p.classList.contains('now'))]", w)
                chk(now == [[k] * len(v["tables"]), k] and pg.text_content("#%s-pos" % w) == "pass %d of %d" % (k + 1, n), "step %d highlights %s" % (k + 1, now))
            pg.click('[data-nv="%s:pa:all"]' % cid); chk(pg.locator(out + " .now").count() == 0, "Show all clears the highlight")
            why = "%d tables, %d printed lines and the start example match; %d passes stepped across the tables and the printed lines" % (len(v["tables"]), len(v["printed"]), n)
        if K == "seqtypes":
            got = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out .sqc')].map(c=>[c.querySelector('.sqn').textContent,c.querySelector('.sqs2').textContent,c.querySelector('.sqm').textContent,c.querySelector('.sqa').textContent,c.querySelector('.sqr').textContent,c.classList.contains('mut')])", w)
            chk(got == [[t_["type"], t_["sample"], t_["mutable_label"], t_["assign"], t_["result"], t_["mutable"]] for t_ in v["types"]], "cards %s" % got)
            why = "%d types: sample, mutability, assignment and its result match" % len(v["types"])
        if K == "unpack":
            for ci, c in enumerate(v["cases"]):
                base = out + ' [data-uc="%d"]' % ci
                chk(T(base + " .ups") == [c["stmt"]] and T(base + " .upi") == c["items"] and T(base + " .unn") == [t_["name"] for t_ in c["targets"]] and T(base + " .unv") == [t_["value"] for t_ in c["targets"]], "case %d texts" % (ci + 1))
                chk(pg.evaluate("s=>[...document.querySelectorAll(s+' .unt')].map(b=>b.style.gridColumn)", base) == ["%d / %d" % (t_["from"] + 1, t_["to"] + 1) for t_ in c["targets"]], "case %d: each name spans the items it took" % (ci + 1))
                for m, t_ in enumerate(c["targets"]):
                    pg.click('[data-nv="%s:tg:%d.%d"]' % (cid, ci, m)); picked = pg.evaluate("s=>[...document.querySelectorAll(s+' .upi')].flatMap((e,i)=>e.classList.contains('pick')?[i]:[])", base)
                    chk(picked == list(range(t_["from"], t_["to"])), "case %d: %s marks items %s" % (ci + 1, t_["name"], picked))
            if v.get("error"): chk(T(out + " .uerr") == [v["error"]["expr"]] and v["error"]["message"] in T(out + " .lerr")[0], "the error")
            why = "%d cases: statement, items, names, values and the items each name marks match" % len(v["cases"])
        if K == "classify":
            got = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out .clc')].map(c=>[c.querySelector('.clq').textContent,c.querySelector('.clh').textContent,[...c.querySelectorAll('.clk')].map(k=>[k.querySelector('.cke').textContent,k.querySelector('.cle').textContent])])", w)
            chk(got == [[c["question"], c["head"], [[k["expr"], k["evidence"]] for k in c["chips"]]] for c in v["columns"]], "columns %s" % got)
            why = "%d columns with their chips and evidence match" % len(v["columns"])
        if K == "facts":
            got = pg.evaluate("w=>[...document.querySelectorAll('#'+w+'-out .fc')].map(c=>[c.querySelector('.fct').textContent,c.querySelector('.fce').textContent,c.querySelector('.fcr').textContent])", w)
            chk(got == [[f["label"], f["expr"], f["result"]] for f in v["facts"]], "facts %s" % got)
            why = "%d facts: label, expression and result match" % len(v["facts"])
        ok = not bad
        if bad: why = bad[0][:200]
        return ok, why
    vis_ok = []
    NODE_IDS = {n["id"] for n in nodes}  # a visual whose key is not a concept id (the deck-only "ThreeQuestions") is not on the page
    SKIPPED = [k for k in d.get("visuals", {}) if not k.startswith("_") and k not in NODE_IDS]
    for cid, v in ((k, x) for k, x in d.get("visuals", {}).items() if not k.startswith("_") and k in NODE_IDS):
        w = "wv-" + cid; pg.evaluate("goTo('%s')" % cid); pg.click('[data-vistoggle="%s"]' % cid); ok = False; why = ""
        try:
            if v["kind"] == "floatbits":
                pg.wait_for_function("id=>document.querySelector('#'+id+'-out .bits')", arg=w, timeout=120000); bits = pg.text_content("#%s-out .bits" % w).strip()
                import struct; x = float(eval(v["start"])); ok = bits == format(struct.unpack(">Q", struct.pack(">d", x))[0], "064b"); why = "64 bits match the build interpreter's"
            if v["kind"] == "truthtable":
                pg.wait_for_function("id=>document.querySelector('#'+id+'-out table')", arg=w, timeout=120000); rows = pg.locator("#%s-out tr" % w).count() - 1
                names = sorted(set(__import__("re").findall(r"\b[abc]\b", v["start"]))); ok = rows == 2 ** len(names); why = "%d rows for %d inputs" % (rows, len(names))
            if v["kind"] == "trace":
                for ri, run in enumerate(v["runs"]):
                    if ri: pg.click('[data-vrun="%s:%d"]' % (cid, ri))
                    else: pg.wait_for_function("id=>document.querySelector('#'+id+'-out table')", arg=w, timeout=60000)
                    n = len(run["rows"]); [pg.click('[data-vnext="%s"]' % cid) for _ in range(n - 1)]
                    shown = pg.locator("#%s-out tr:not([hidden])" % w).count() - 1; last = pg.locator("#%s-out tr.now" % w).inner_text()
                    ok = shown == n and str(n) in pg.text_content("#%s-pos" % w) and all(x.strip("'") in last or x in last for x in run["rows"][-1]["vals"]); why = "run %d: %d passes shown, last row matches" % (ri + 1, n)
                    if not ok: break
                    if run["printed"]: ok = run["printed"] in pg.text_content("#%s-out" % w); why += "; printed text shown"
                    if not ok: break
            if v["kind"] == "range":
                dots = pg.locator("#%s-out svg circle" % w).count(); ok = dots == len(v["values"]) + 1 and ("stop %d" % v["stop"]) in pg.text_content("#%s-out" % w); why = "%d value dots and the stop marker" % len(v["values"])
            if v["kind"] == "pairs":
                txt = pg.text_content("#%s-out" % w); ok = all(x in txt for x in v["reprs"]) and (not v.get("error") or v["error"] in txt) and pg.locator("#%s-out svg line" % w).count() == len(v["pairs"]); why = "%d pairs drawn" % len(v["pairs"])
            if v["kind"] == "names":
                ok = ("%d names" % v["count"]) in pg.text_content("#%s" % w); why = "states %d names" % v["count"]
            if v["kind"] == "debugger":
                E = v["events"]; bp = v["breakpoints"]
                pg.click('[data-dbg="%s:stop"]' % cid); pos = lambda: pg.text_content("#%s-pos" % w)
                first_line = E[0]["line"]; ok = ("line %d" % first_line) in pos()
                # toggle a breakpoint on and off
                tgt = next(x for x in range(1, len(v["lines"]) + 1) if x not in bp)
                pg.click('[data-bp="%s:%d"]' % (cid, tgt)); on = "on" in (pg.get_attribute('[data-bp="%s:%d"]' % (cid, tgt), "class") or ""); pg.click('[data-bp="%s:%d"]' % (cid, tgt)); off = "on" not in (pg.get_attribute('[data-bp="%s:%d"]' % (cid, tgt), "class") or "")
                ok = ok and on and off
                pg.click('[data-dbg="%s:in"]' % cid); i1 = E[1]["line"] if len(E) > 1 else None; ok = ok and ("line %d" % i1) in pos()
                pg.click('[data-dbg="%s:stop"]' % cid)
                if bp:
                    nxt = next((e for e in E[1:] if e["line"] in bp), None); pg.click('[data-dbg="%s:cont"]' % cid)
                    ok = ok and (nxt is None or (("line %d (breakpoint)" % nxt["line"]) in pos())); why = "stopped at line %s (breakpoint) after Continue" % (nxt["line"] if nxt else "-")
                else:
                    why = "no breakpoint set in this run"
                # Step Over skips a call, Step Out leaves it: checked against the recorded depths
                ci = next((k for k in range(len(E) - 1) if E[k + 1]["depth"] > E[k]["depth"]), None); sem = "no call in this run"
                if ci is not None:
                    d0 = E[ci]["depth"]; ov = next((k for k in range(ci + 1, len(E)) if E[k]["depth"] <= d0), len(E)); ou = next((k for k in range(ci + 2, len(E)) if E[k]["depth"] <= d0), len(E))
                    pg.click('[data-dbg="%s:stop"]' % cid); [pg.click('[data-dbg="%s:in"]' % cid) for _ in range(ci)]; pg.click('[data-dbg="%s:over"]' % cid)
                    ok = ok and (pos() == "finished" if ov >= len(E) else ("line %d" % E[ov]["line"]) in pos())
                    pg.click('[data-dbg="%s:stop"]' % cid); [pg.click('[data-dbg="%s:in"]' % cid) for _ in range(ci + 1)]; pg.click('[data-dbg="%s:out"]' % cid)
                    ok = ok and (pos() == "finished" if ou >= len(E) else ("line %d" % E[ou]["line"]) in pos()); sem = "Step Over and Step Out from the call at event %d land where the recorded depths say" % ci
                pg.click('[data-dbg="%s:stop"]' % cid)
                for _ in range(len(E) + 2): pg.click('[data-dbg="%s:in"]' % cid)
                ok = ok and pos() == "finished" and v["printed"] in pg.text_content("#%s-out" % w); why += "; Step In reaches the end and shows the program output; breakpoint toggles; " + sem
            if v["kind"] == "levels":
                good = True
                for i, t in enumerate(v["settings"]):
                    pg.click('[data-lv="%s:%d"]' % (cid, i)); rows = pg.locator("#%s-out tbody tr, #%s-out tr:has(td)" % (w, w)); shown = pg.locator("#%s-out td.t" % w).count()
                    good &= shown == sum(1 for x in t["shown"] if x) and t["output"] == [x for x in pg.text_content("#%s-out pre.out" % w).split("\n") if x and x != "(nothing)"]
                ok = good; why = "%d settings; shown counts and printed lines match the recorded specification" % len(v["settings"])
            if v["kind"] == "unwind":
                for _ in range(len(v["frames"]) + 1): pg.click('[data-uw="%s:next"]' % cid)
                ok = ("caught in %s" % v["handler"]["func"]) in pg.text_content("#%s-pos" % w) and v["traceback"].splitlines()[0] in pg.text_content("#%s-out" % w); why = "%d frames climbed, caught in %s, traceback shown" % (len(v["frames"]), v["handler"]["func"])
            if v["kind"] == "branchflow":
                pg.wait_for_function("id=>/Output/.test(document.getElementById(id+'-out').textContent)", arg=w, timeout=120000); first = pg.text_content("#%s-out" % w)
                pg.fill("#%s-x" % w, "8"); pg.click('[data-vis="%s"]' % cid); pg.wait_for_function("id=>/child ticket/.test(document.getElementById(id+'-out').textContent)", arg=w, timeout=60000)
                ok = ("adult ticket" in first or "senior ticket" in first) and pg.locator("#%s-src .tl.now" % w).count() >= 3; why = "path follows the input: %s then child ticket" % ("adult" if "adult" in first else "senior")
            if v["kind"] in NEWKINDS:
                ok, why = check_new(cid, v, w)
        except Exception as e:
            why = "%s: %s" % (type(e).__name__, str(e)[:200])
        R["widgets"][w] = {"passed": ok, "detail": why}; vis_ok.append(ok)
    feat("chapter visualisations: float bits, truth tables, branch paths, loop traces, ranges and pairs - each computed by Python or by an executed specification", all(vis_ok), "%d of %d" % (sum(vis_ok), len(vis_ok)))
    # ---- 9.11.0: zoom on every SVG chapter visual, the ignored framing slide, WCAG over the new visuals ----
    svgv = [k for k, x in d.get("visuals", {}).items() if k in NODE_IDS and x["kind"] in ("keysort", "refgraph", "range", "pairs")]
    zbad = []
    for cid in svgv:
        open_vis(cid); z = zoom_check(cid)
        if z: zbad.append((cid, z))
    feat("zoom in, out and show-all on every SVG chapter visual (sorts, name-and-object pictures, ranges, pairs), the same controls as the other diagrams", not zbad, "%d diagrams; %s" % (len(svgv), zbad[:2]))
    feat("a visual whose key is not a concept id (the deck-only framing slide) is not drawn and raises no error", all(pg.locator("#wv-%s" % k).count() == 0 for k in SKIPPED), "ignored keys: %s" % (SKIPPED or "none"))
    newids = [k for k, x in d.get("visuals", {}).items() if k in NODE_IDS and x["kind"] in NEWKINDS]
    if newids:
        ax = ctx.new_page(); ax.goto("file://" + page_path); ax.wait_for_timeout(400); ax.add_script_tag(path=AXE)
        ax.evaluate("ids=>{document.querySelectorAll('.vis').forEach(e=>{let p=e;while(p&&p!==document.body){p.hidden=false;p=p.parentElement}});ids.forEach(id=>nvShow(id))}", newids)
        viol = ax.evaluate("async()=>{const r=await axe.run({include:[['.nv']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.impact,v.nodes.length,v.nodes.slice(0,2).map(n=>n.target.join(' ')+' :: '+((n.any[0]||{}).message||''))])}")
        feat("WCAG 2 A/AA (axe-core) over all %d new chapter visuals shown at once" % len(newids), not viol, str(viol)[:300]); ax.close()
    view("taxonomy"); v0 = pg.get_attribute("#taxo svg", "viewBox"); pg.hover("#taxo svg"); pg.mouse.wheel(0, -300); pg.wait_for_timeout(200); v1 = pg.get_attribute("#taxo svg", "viewBox")
    feat("the mouse wheel zooms diagrams, without a key held", v1 != v0, "viewBox changed on wheel")
    # ---- 9.1.0: phones and tablets ----
    for (W, H, dev) in ((360, 740, "small phone"), (390, 844, "phone"), (768, 1024, "tablet")):
        mctx = b.new_context(locale="en-US", viewport={"width": W, "height": H}, is_mobile=True, has_touch=True, device_scale_factor=2); m = mctx.new_page(); m.goto("file://" + page_path); m.wait_for_timeout(400)
        bad = []
        for k in ["intro"] + [x for x in GROUP] + ["agents"]:
            m.evaluate("k=>showTab(k)", k); m.wait_for_timeout(120)
            r = m.evaluate("""()=>{const W=innerWidth;return {wide:document.documentElement.scrollWidth>W+1,
              tiny:[...document.querySelectorAll('button,a,input,select,textarea')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&!e.closest('[hidden],.tv')&&!(e.tagName==='A'&&e.closest('p,li,td'))&&(r.height<24||r.width<24)}).map(e=>(e.id||e.className||e.textContent).toString().slice(0,20)).slice(0,3),
              font:Math.min(...[...document.querySelectorAll('main p, main li, .note, .msg')].filter(e=>e.getBoundingClientRect().width>0).map(e=>parseFloat(getComputedStyle(e).fontSize)).concat([99]))}}""")
            if r["wide"] or r["tiny"] or (W < 700 and r["font"] < 14): bad.append((k, r))
        header = m.evaluate("()=>Math.round(document.querySelector('header').getBoundingClientRect().height)")
        m.click("#exploreBtn"); m.wait_for_timeout(350); drawer = m.evaluate("()=>{const r=document.getElementById('explorerTree').getBoundingClientRect();return r.left>=-1&&r.width>200}")
        leaf = [n for n in nodes if n["level"] == 3][0]; m.click("#expandAll"); m.click('#tree .tn[data-c="%s"]' % leaf["id"]); m.wait_for_timeout(400)
        closed = m.evaluate("()=>document.getElementById('explorerTree').getBoundingClientRect().right<=0") and m.evaluate(in_view, "s-" + leaf["id"])
        feat("%s (%dpx): no view wider than the screen, every control at least 24px, text at least 14px%s, explorer as a drawer" % (dev, W, "" if W >= 700 else ", header compact"), not bad and drawer and closed and (W >= 700 or header <= 100), "header %dpx; problems: %s" % (header, bad[:2]))
        mctx.close()
    # ---- 9.2.0: any screen - the page scales with the window, live, without a reload ----
    dctx = b.new_context(locale="en-US", viewport={"width": 1280, "height": 800}); dp = dctx.new_page(); dp.goto("file://" + page_path); dp.wait_for_timeout(300); dp.evaluate("showTab('%s')" % tops[0]["id"])
    sizes = []
    for (W, H) in ((1280, 800), (1920, 1080), (2560, 1440), (3840, 2160), (3440, 1440)):
        dp.set_viewport_size({"width": W, "height": H}); dp.wait_for_timeout(200)
        sizes.append(dp.evaluate("""()=>({root:parseFloat(getComputedStyle(document.documentElement).fontSize),body:parseFloat(getComputedStyle(document.querySelector('main p')).fontSize),
            tree:Math.round(document.querySelector('aside.tree').getBoundingClientRect().width),wide:document.documentElement.scrollWidth>innerWidth+1,card:Math.round(document.querySelector('.ovcard').getBoundingClientRect().width)})"""))
    grows = all(sizes[k + 1]["root"] > sizes[k]["root"] for k in range(3)) and sizes[0]["root"] >= 17 and sizes[3]["root"] <= 28 and not any(x["wide"] for x in sizes)
    scales = all(abs(x["body"] / x["root"] - sizes[0]["body"] / sizes[0]["root"]) < 0.01 and x["tree"] > 0 for x in sizes) and sizes[3]["card"] > sizes[0]["card"]
    feat("any screen: text, explorer and cards scale with the window as it is resized, 1280 to 3840 pixels, bounded at 17 and 28 pixel text", grows and scales,
         "root text %s px" % " / ".join("%g" % x["root"] for x in sizes))
    dctx.close()
    # ---- 9.4.0: the explorer opens one concept; its siblings stay a click away ----
    mid2 = next(m for m in nodes if m["level"] == 2 and len([x for x in nodes if x["parent"] == m["id"]]) >= 2); sibs = [x for x in nodes if x["parent"] == mid2["id"]]
    pg.click("#expandAll"); pg.click('#tree .tn[data-c="%s"]' % sibs[0]["id"]); pg.wait_for_timeout(250)
    shown = pg.evaluate("id=>[...document.querySelectorAll('[data-subpane=\"'+id+'\"] .cards > section.leaf')].filter(s=>!s.hidden).map(s=>s.dataset.concept)", mid2["id"])
    crumb = pg.text_content("#crumb-%s" % [n for n in nodes if n["id"] == mid2["parent"]][0]["id"])
    pg.click('#crumb-%s [data-sub="%s"]' % (mid2["parent"], mid2["id"])); pg.wait_for_timeout(200)
    all_back = pg.evaluate("id=>[...document.querySelectorAll('[data-subpane=\"'+id+'\"] .cards > section.leaf')].filter(s=>!s.hidden).length", mid2["id"])
    feat("the explorer opens a single concept; the breadcrumb shows where it sits, with its neighbours and 'show all' a click away", shown == [sibs[0]["id"]] and sibs[0]["label"] in crumb and sibs[1]["label"] in crumb and all_back == len(sibs), "%s alone, then all %d" % (sibs[0]["label"], all_back))
    # ---- 9.4.1: the explorer follows every move of the main area ----
    sel = lambda: pg.evaluate("()=>{const x=document.querySelector('#tree .tn.sel');return x?x.dataset.c:null}")
    steps = []
    view(mid2["parent"]); pg.select_option('#crumb-%s select' % mid2["parent"], mid2["id"]); pg.wait_for_timeout(150); steps.append(("breadcrumb chooser", sel() == mid2["id"]))
    pg.evaluate("goTo('%s')" % sibs[0]["id"]); pg.click('#crumb-%s [data-go="%s"]' % (mid2["parent"], sibs[1]["id"])); pg.wait_for_timeout(150); steps.append(("next concept", sel() == sibs[1]["id"]))
    pg.click('#crumb-%s [data-sub="%s"]' % (mid2["parent"], mid2["id"])); pg.wait_for_timeout(150); steps.append(("show all", sel() == mid2["id"]))
    other = next(t_ for t_ in tops if t_["id"] != mid2["parent"]); view(other["id"]); pg.wait_for_timeout(150)
    shown_at = pg.evaluate("""id=>{const p=document.querySelector('[data-pane="'+id+'"]'),sp=p.querySelector('[data-subpane]:not([hidden])'),m=sp.dataset.subpane;
        const f=sp.classList.contains('focused')?[...sp.querySelectorAll('.cards > section.leaf')].find(x=>!x.hidden):null;return f?f.dataset.concept:(m.startsWith('ov-')?m.slice(3):m)}""", other["id"])
    steps.append(("subject tab", sel() == shown_at))
    view(mid2["parent"]); pg.wait_for_timeout(150); steps.append(("back to the subject", sel() == mid2["id"]))
    link = pg.locator('[data-subpane="%s"] p [data-c]:visible' % mid2["id"]).first
    if link.count(): link.click(); pg.wait_for_timeout(150); steps.append(("concept tap keeps the location", sel() == mid2["id"])); pg.keyboard.press("Escape")
    view("taxonomy"); steps.append(("non-subject view clears it", sel() is None))
    feat("the explorer stays in step with the main area: chooser, next, show all, subject tabs, concept taps, other views", all(ok for _, ok in steps), ", ".join("%s %s" % (n_, "ok" if ok else "OUT OF STEP") for n_, ok in steps))
    # ---- 9.4.2: nothing an antivirus reads as a downloader or HTML smuggling ----
    html = open(page_path).read()
    risky = {k: len(re.findall(p, html)) for k, p in (("evaluated fetched code", r"\(0,\s*eval\)|[^\w.'\"]eval\((?!n\[|compile|_last|e,|'\+)"), ("new Function", r"new Function\("), ("scripted download", r"\.download\s*=|msSaveOrOpenBlob"), ("document.write", r"document\.write"), ("base64 decode", r"\batob\("), ("redirect", r"location\.(href|replace|assign)\s*="))}
    feat("no evaluated fetched code, no scripted file download, no document.write, base64 decoding or redirect in the page", not any(risky.values()), str(risky))
    # ---- 9.3.0: text-size control, zoom bar outside the drawing, concept taps show options ----
    fctx = b.new_context(locale="en-US", viewport={"width": 1280, "height": 800}); fp = fctx.new_page(); fp.goto("file://" + page_path); fp.wait_for_timeout(300)
    r0 = fp.evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)"); fp.click("#fsUp"); fp.click("#fsUp"); r2 = fp.evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)")
    fp.reload(); fp.wait_for_timeout(300); r3 = fp.evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)"); lab = fp.text_content("#fsVal")
    fp.click("#fsReset"); r4 = fp.evaluate("parseFloat(getComputedStyle(document.documentElement).fontSize)")
    feat("text-size control: larger and smaller text, remembered after a reload, one click back to the default", r0 >= 17 and abs(r2 - r0 * 1.2) < 0.6 and abs(r3 - r2) < 0.1 and lab == "120%" and abs(r4 - r0) < 0.1, "%g -> %g px (%s), reset %g px" % (r0, r2, lab, r4))
    fp.evaluate("showTab('taxonomy')"); fp.wait_for_function("()=>document.querySelector('#taxo .zbar')", timeout=120000)
    ov = fp.evaluate("()=>{const bar=document.querySelector('#taxo .zbar'),d=document.querySelector('#taxo .diagram');const a=bar.getBoundingClientRect(),c=d.getBoundingClientRect();return a.bottom<=c.top+0.5&&!d.contains(bar)}")
    feat("zoom controls sit above each diagram, never covering it", ov)
    fp.evaluate("goTo('%s')" % tops[0]["id"]); fp.wait_for_timeout(200); link = fp.locator('[data-pane="%s"] p [data-c]:visible' % tops[0]["id"]).first
    if link.count():
        tgt = link.get_attribute("data-c"); before = fp.evaluate("[...document.querySelectorAll('[data-pane]')].find(p=>!p.hidden).dataset.pane"); link.click(); fp.wait_for_timeout(200)
        after = fp.evaluate("[...document.querySelectorAll('[data-pane]')].find(p=>!p.hidden).dataset.pane"); card = fp.text_content("#card") if fp.locator("#card").is_visible() else ""
        feat("tapping a concept in the text opens its options in the detail card, without leaving the page", before == after and "Go to its section" in card and byid_label_ok(card, tgt) if False else (before == after and "Go to its section" in card), "%s: card with options, still on %s" % (tgt, after))
    fctx.close()
    pg.evaluate("showTab('taxonomy')"); pg.wait_for_function("()=>document.querySelector('#taxo svg')", timeout=120000)
    pinch = pg.evaluate("""()=>{showTab('taxonomy');const svg=document.querySelector('#taxo svg'),v0=svg.getAttribute('viewBox'),r=svg.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
      const ev=(t,id,x,y)=>svg.dispatchEvent(new PointerEvent(t,{pointerId:id,clientX:x,clientY:y,bubbles:true,pointerType:'touch',isPrimary:id===1}));
      ev('pointerdown',1,cx-20,cy);ev('pointerdown',2,cx+20,cy);ev('pointermove',1,cx-80,cy);ev('pointermove',2,cx+80,cy);ev('pointerup',1,cx-80,cy);ev('pointerup',2,cx+80,cy);return v0!==svg.getAttribute('viewBox')}""")
    feat("pinch zoom: two fingers spreading zoom a diagram", pinch)
    lt2 = pg.evaluate("window.__lt"); feat("no main-thread task over 200 ms, including the ontology layout", max(lt2 or [0]) <= 200, "longest %d ms" % max(lt2 or [0]))
    # ---- 9.7.0: no step button, lecture, resources, fitted work area ----
    leafw = pg.evaluate("ids=>ids.map(id=>{const e=document.getElementById('w-'+id);return e?e.querySelectorAll('button,[data-step]').length:0}).reduce((a,b)=>a+b,0)", [n["id"] for n in nodes if n["level"] == 3 and not n.get("chart") and "io" not in n])
    feat("concept sections carry no Next-step or Walk-through button (a static example only)", leafw == 0 and "Walk through it" not in pg.evaluate("()=>document.body.innerText"), "%d buttons in %d static example widgets" % (leafw, len([n for n in nodes if n["level"] == 3 and "io" not in n and not n.get("chart")])))
    if d.get("lecture"):
        view("lecture"); ls = pg.locator("#ls-1").count(); cnt = pg.locator(".lslide").count()
        jump = next((x for x in d["lecture"] if x.get("concept")), None); jok = True
        if jump:
            pg.click('#ls-%d [data-go]' % jump["n"]); pg.wait_for_timeout(250); jok = pg.evaluate(in_view, "s-" + jump["concept"]) or pg.evaluate(in_view, "w-" + jump["concept"]); view("lecture")
        vj = next((x for x in d["lecture"] if x.get("visual") and x["visual"] in d.get("visuals", {}) and x["visual"] in NODE_IDS and x.get("concept")), None); vok = True
        if vj:
            pg.click('#ls-%d [data-lvis]' % vj["n"]); pg.wait_for_timeout(300); vok = pg.evaluate("id=>{const e=document.getElementById('wv-'+id);return !!e&&e.getBoundingClientRect().height>0&&!e.closest('[hidden]')}", vj["visual"])
        feat("Lecture tab: one slide text per deck slide, each with a jump to its concept and a button that shows its visual", cnt == len(d["lecture"]) and ls == 1 and jok and vok, "%d lecture slides; jumps land on the concept and the visual" % cnt)
    if d.get("resources"):
        view("resources"); lis = pg.locator("ul.res li"); nres = lis.count(); okl = all(lis.nth(k).locator("a").first.get_attribute("target") == "_blank" and "noopener" in lis.nth(k).locator("a").first.get_attribute("rel") for k in range(nres))
        has_vid = any(r["kind"] == "video" for r in d["resources"]); note = "No video has been checked yet" in pg.text_content('[data-pane="resources"]')
        n3 = len([n for n in nodes if n["level"] == 3]); srows = pg.locator('[data-pane="resources"] table tr').count(); hrefs = pg.evaluate("()=>[...document.querySelectorAll('[data-pane=\"resources\"] table a')].map(a=>a.href)")
        feat("Resources tab: every checked link opens in a new tab safely, videos are never invented, and each concept has a labelled search", nres == len(d["resources"]) and okl and (has_vid or note) and srows == n3 and all(("youtube.com/results" in h or "stackoverflow.com/search" in h or "discuss.python.org/search" in h) for h in hrefs), "%d links, %d search rows" % (nres, srows))
    # fitted work area
    fit = []
    for (W, H) in ((1400, 900), (1280, 720)):
        pg.set_viewport_size({"width": W, "height": H}); pg.wait_for_timeout(200)
        leaf_id = [n for n in nodes if n["level"] == 3][0]["id"]; pg.evaluate("id=>goTo(id)", leaf_id); pg.wait_for_timeout(250)
        r = pg.evaluate("""()=>{const p=document.querySelector('[data-pane]:not([hidden])'),h2=p.querySelector('.viewsub h2, h2'),vs=p.querySelector('.viewsub');
          const tv=[...document.querySelectorAll('textarea.code')].filter(t=>t.offsetParent).map(t=>t.scrollHeight>t.clientHeight+2);
          return {h2:h2?getComputedStyle(h2).position==='absolute'||h2.getBoundingClientRect().height<=1:true,scrollw:document.documentElement.scrollWidth>innerWidth+1,ta:tv.some(x=>x)}}""")
        fit.append((W, H, r))
    pg.set_viewport_size({"width": 1400, "height": 900})
    feat("fit: sub-page heading hidden under the tab row, introductions folded, code areas show all their text", all(not f[2]["scrollw"] and not f[2]["ta"] for f in fit), str([(f[0], f[2]) for f in fit]))
    view("play"); pcode = pg.evaluate("()=>{const t=document.getElementById('pcode');const r=t.getBoundingClientRect();return {top:Math.round(r.top),bottom:Math.round(r.bottom),H:innerHeight,inner:t.scrollHeight>t.clientHeight+2}}")
    feat("the playground code area uses the free height and does not scroll inside", pcode["bottom"] <= pcode["H"] + 2 and pcode["bottom"] > pcode["H"] * 0.55 and not pcode["inner"], str(pcode))
    view("quiz"); fs = pg.locator("fieldset:not([data-gen])"); qok = True
    for k in range(fs.count()):
        f = fs.nth(k); f.locator("input").nth(int(f.get_attribute("data-answer"))).check(); f.locator("button").click(); qok &= pg.text_content("#q%d-fb" % k) == "Correct."
    feat("quiz", qok)
    # ---- 9.9.0: answer formatting ----
    view("agents"); pg.click('[data-agenttab="%s"]' % a["id"])
    fm = pg.evaluate("""()=>{const m=[...document.querySelectorAll('.msg.agent')].filter(x=>x.querySelector('.lead'));const x=m[m.length-1];if(!x)return null;return {lead:!!x.querySelector('.lead'),pts:x.querySelectorAll('ul.pts li').length,tk:x.querySelectorAll('.tk').length,ex:x.querySelectorAll('.exblock').length,rel:x.querySelectorAll('.rel').length,cls:x.classList.contains('answer')}}""")
    feat("agent answers are formatted: lead sentence, bullet points, coloured code, example block, related concepts", bool(fm) and fm["lead"] and fm["pts"] >= 1 and fm["cls"], str(fm))
    md = pg.evaluate("()=>fmt('First paragraph.\\n\\n- one\\n- two\\n\\n```python\\nprint(1)\\n```')")
    feat("markdown text (live LLM) is rendered as paragraphs, bullets and a code block", "<ul" in md and "<pre" in md and md.count("<li") == 2, md[:120])
    # ---- 9.9.0: question builder ----
    view("quiz"); nn = len(d["nodes"])
    gen = pg.evaluate("""()=>{let bad=[],n=0;for(const x of D.nodes){for(const k of qKindsFor(x)){const q=qMake(x.id,k);n++;if(!q||q.options.length<2||q.answer<0||q.answer>=q.options.length||new Set(q.options).size!==q.options.length||!q.q||!q.why)bad.push(x.id+':'+k)}
      if(!qKindsFor(x).length)bad.push(x.id+':none')}return {n,bad:bad.slice(0,5)}}""")
    feat("the question builder can ask about every concept in every kind it offers, with distinct options", not gen["bad"] and gen["n"] >= nn, "%d questions over %d concepts; bad %s" % (gen["n"], nn, gen["bad"]))
    kinds_seen = pg.evaluate("()=>[...new Set(D.nodes.flatMap(n=>qKindsFor(n)))].sort()")
    pg.click("#qgnew"); pg.wait_for_timeout(150)
    f = pg.locator("#qgout fieldset").first; ok1 = f.count() == 1
    f.locator("input").nth(int(f.get_attribute("data-answer"))).check(); f.locator("[data-gcheck]").click(); v1 = f.locator(".verdict").text_content()
    pg.click("#qgall"); pg.wait_for_timeout(300); gf = pg.locator("#qgout fieldset"); cnt = gf.count()
    for k in range(cnt):
        g = gf.nth(k); g.locator("input").nth(int(g.get_attribute("data-answer"))).check(); g.locator("[data-gcheck]").click()
    sc = pg.text_content("#qgscore"); cv = pg.text_content("#qgcover")
    feat("New question makes a question that checks correctly; One question for every concept covers the chapter and scores", ok1 and v1.startswith("Correct") and cnt == nn and ("%d of %d answered correctly" % (cnt, cnt)) in sc and ("all %d" % nn in cv or ("%d of the %d" % (nn, nn)) in cv or str(nn) in cv), "%s | %s | %s" % (v1[:40], sc, cv[:120]))
    pg.locator("#qgout fieldset").first.locator("input").nth(0).check()
    wrong = pg.evaluate("()=>{const f=document.querySelector('#qgout fieldset');const a=+f.dataset.answer;return a===0?1:0}")
    pg.click("#qgclear"); pg.wait_for_timeout(100)
    feat("Clear removes the generated questions and resets coverage", pg.locator("#qgout fieldset").count() == 0 and pg.text_content("#qgscore") == "")
    pg.click("#qgall"); pg.wait_for_timeout(200); g = pg.locator("#qgout fieldset").first; g.locator("input").nth(1 - int(g.get_attribute("data-answer")) if int(g.get_attribute("data-answer")) < 2 else 0).check(); g.locator("[data-gcheck]").click()
    feat("a wrong answer is explained and links to the concept", g.locator(".verdict").text_content().startswith("Not quite") and g.locator("[data-go]").count() == 1)
    # ---- 9.10.0: question bank and live question ----
    bank = pg.evaluate("()=>BANK.length")
    if bank:
        pg.select_option("#qgkind", "authored"); pg.click("#qgall"); pg.wait_for_timeout(300)
        leg = pg.evaluate("()=>[...document.querySelectorAll('#qgout legend')].map(l=>l.textContent)")
        feat("written question bank: it covers every concept and 'One question for every concept' asks the written item first" + ("" if BANK_COMPLETE else " (a seed bank: every concept that has an item asks it)"), (pg.evaluate("()=>D.nodes.every(n=>BANK.some(b=>b.concept===n.id))") and len(leg) == nn and all(l.startswith("From the question bank") for l in leg) if BANK_COMPLETE else (len(leg) == nn and sum(l.startswith("From the question bank") for l in leg) == pg.evaluate("()=>new Set(BANK.map(b=>b.concept)).size"))), "%d bank items; %d written questions of %d" % (bank, sum(l.startswith("From the question bank") for l in leg), len(leg)))
        perm = pg.evaluate("""()=>{let bad=[];for(const b of BANK){for(let k=0;k<3;k++){const q=qMake(b.concept,'authored');const src=BANK.filter(x=>x.concept===b.concept).some(x=>x.q===q.q&&x.options[x.answer]===q.options[q.answer]&&[...x.options].sort().join('|')===[...q.options].sort().join('|'));if(!src)bad.push(b.concept)}}return bad.slice(0,5)}""")
        feat("shuffled written items keep their right answer", not perm, str(perm))
        appl = pg.evaluate_handle("()=>BANK.filter(b=>b.code)")
        n_apply = pg.evaluate("()=>BANK.filter(b=>b.code).length"); badrun = []
        for k in range(n_apply):
            r = pg.evaluate("async k=>{const b=BANK.filter(b=>b.code)[k];let out;try{out=String(await runPy(b.code)).trim()}catch(e){out='ERR:'+String(e).split('\\n').pop()}return [out,b.options[b.answer],b.concept]}", k)
            ok = r[0] == r[1] or r[0].rstrip(":") == r[1] or (r[0].startswith("ERR:") and r[1] in r[0]) or (r[0].startswith("ERR:") and r[1].split()[0].endswith("Error")) or (r[1].split()[0].endswith("Error") and r[0].split(':')[0].strip()==r[1].split()[0])
            if not ok: badrun.append(r)
        feat("every written item with code is re-run in the page and its marked answer is what the browser's Python prints", not badrun, "%d re-run; mismatches %s" % (n_apply, str(badrun[:3])[:300]))
    pg.select_option("#qgkind", "any"); pg.click("#qgclear")
    pg.click("#qglive"); pg.wait_for_timeout(200); msg0 = pg.text_content("#qgout")
    feat("without a live model the live question says so and changes nothing else", "not available in this browser" in msg0)
    pg.evaluate("()=>{KIT.llm={chat:{completions:{create:async()=>({choices:[{message:{content:window.__reply}}]})}}}}")
    def live(reply):
        pg.evaluate("r=>{window.__reply=r}", reply); pg.click("#qglive"); pg.wait_for_function("()=>!/Asking the model/.test(document.getElementById('qgout').textContent)", timeout=60000); return pg.text_content("#qgout"), pg.locator("#qgout fieldset").count()
    t1, c1 = live('Sure! {"q":"What is a traceback?","options":["A report of the calls that led to an error","A kind of loop","A file format","A log level"],"answer":0,"why":"It lists the calls."}')
    t2, c2 = live('{"q":"What does this print?","code":"print(6*7)","options":["13","42","67","Error"],"answer":1,"why":"6 times 7."}')
    t3, c3 = live('{"q":"What does this print?","code":"print(6*7)","options":["13","42","67","Error"],"answer":0,"why":"wrong on purpose"}')
    t4, c4 = live('I cannot do that')
    t5, c5 = live('{"q":"x","options":["a","a","b","c"],"answer":1}')
    feat("live-model question: a well-formed one is shown with its label; one with code is shown only when its code prints the marked answer; malformed or wrong ones are refused with a reason", c1 == 1 and "live model" in t1 and c2 == 1 and "was run" in t2 and c3 == 0 and "not what its code prints" in t3 and c4 == 0 and "well-formed" in t4 and c5 == 0, "%s | %s | %s | %s" % (t3[:60], t4[:60], t5[:60], t2[-80:]))
    pg.evaluate("()=>{KIT.llm=null}"); pg.click("#qgclear")
    # ---- 9.12.0: clickable references, page search, grounding of the local model's reply ----
    view("agents"); pg.click('[data-agenttab="%s"]' % a["id"])
    ans4 = ask("how is " + q1.lower() + " written")
    nrn = pg.locator("#%s-log .msg button.rn" % a["id"]).count(); nsrc = pg.locator("#%s-log .msg button.src" % a["id"]).count()
    pg.locator("#%s-log .msg button.src" % a["id"]).last.click(); pg.wait_for_selector("#card .srcview .full, #card.srcview .full", timeout=60000)
    cardtxt = pg.text_content("#card"); flashed = pg.locator("#%s-log button.src.flash" % a["id"]).count()
    feat("every source chip in an answer opens its passage in the detail card and is marked in the answer", nsrc >= 3 and len(pg.text_content("#card .full")) > 20 and flashed >= 1 and pg.locator("#card [data-close]").count() == 1, "%d chips; card %d chars; %d marked" % (nsrc, len(cardtxt), flashed))
    if nrn:
        pg.keyboard.press("Escape"); pg.locator("#%s-log .msg button.rn" % a["id"]).last.click(); pg.wait_for_timeout(600)
    feat("inline [n] references in an answer are buttons that open the same passage", nrn >= 1 and pg.locator("#card .full").count() == 1 and len(pg.text_content("#card .full")) > 20, "%d inline references" % nrn)
    view("intro"); pg.keyboard.press("/"); pg.wait_for_selector("#srch:not([hidden])", timeout=5000)
    opened = pg.evaluate("()=>document.activeElement.id==='srchq'&&document.getElementById('srch').getAttribute('role')==='dialog'")
    lab = [n for n in nodes if n.get("level", 3) >= 2][3]["label"]
    pg.fill("#srchq", lab); pg.wait_for_timeout(200); hit1 = pg.locator("#srch .hit").first.text_content()
    pg.keyboard.press("Enter"); pg.wait_for_timeout(800)
    closed = pg.evaluate("()=>document.getElementById('srch').hidden&&!document.getElementById('srch').hasAttribute('role')")
    feat("search: the / key opens it with focus in the box, a concept name finds that concept first, Enter goes to it and closes the search", opened and lab.lower() in hit1.lower() and closed and lab.lower() in pg.text_content("#card").lower(), "%s -> %s" % (lab, hit1[:50]))
    pg.keyboard.press("Control+k"); pg.wait_for_selector("#srch:not([hidden])", timeout=5000)
    pg.fill("#srchq", max(lab.split(), key=len)); pg.wait_for_timeout(200); nh = pg.locator("#srch .hit").count()
    pg.click("#srchmore"); pg.wait_for_selector("#srchpass .hit", timeout=120000); npass = pg.locator("#srchpass .hit").count()
    pg.locator("#srchpass .hit").first.click(); pg.wait_for_selector("#card .full", timeout=60000)
    feat("search: Ctrl+K opens it, finds concepts by definition or code, can also search the book, course and research passages, and a passage opens in the card", nh >= 1 and npass >= 1 and pg.evaluate("()=>document.getElementById('srch').hidden"), "%d concepts, %d passages" % (nh, npass))
    pg.keyboard.press("Control+k"); pg.fill("#srchq", "zzqqxx"); pg.wait_for_timeout(200); none = "No concept" in pg.text_content("#srchres"); pg.keyboard.press("Escape")
    feat("search: a word that is nowhere says so, and Esc closes it", none and pg.evaluate("()=>document.getElementById('srch').hidden"))
    gt = pg.evaluate(r"""()=>{const top=[{c:{text:'The if statement runs its block when the condition holds. Otherwise it skips to the next block.',label:'If statement'}}];
      const a=groundText('At the top of this page you would find a lovely section labelled banana. An if statement runs its block when the condition holds [1].',top);
      const b=groundText('Bananas grow in warm countries and are yellow.',top);
      const c=groundText('Here:\n```\nprint(1)\n```\nThe condition holds.',top);return [a,b,c]}""")
    feat("the local model's reply is checked against its passages: unsupported sentences go, a wholly unsupported reply is dropped, code and supported text stay", gt[0]["dropped"] == 1 and "banana" not in gt[0]["text"] and "condition holds" in gt[0]["text"] and gt[1]["text"] is None and "print(1)" in gt[2]["text"], str(gt)[:200])
    pg.evaluate("()=>{KIT.llm={chat:{completions:{create:async()=>({choices:[{message:{content:'At the top of this page you would find a section labelled banana. It is yellow and grows in warm countries.'}}]})}}}}")
    pg.keyboard.press("Escape"); view("agents"); pg.click('[data-agenttab="%s"]' % a["id"])
    ans5 = ask("what is " + q1.lower()); pg.evaluate("()=>{KIT.llm=null}")
    lastby = pg.locator("#%s-log .msg" % a["id"]).last.text_content()
    feat("an invented reply from the model never reaches the reader; the passages' own sentences are shown with a note", "banana" not in ans5 and "not supported by the passages" in lastby, ans5[:120])
    # ---- 9.13.0: progress, links, copy, notes, cheat sheet, marks, review queue, exercises ----
    pg.keyboard.press("Escape"); leaf = [n_ for n_ in nodes if int(n_.get("level", 3)) >= 3]; A, B = leaf[0]["id"], leaf[1]["id"]; NN = len(nodes)
    pg.evaluate("id=>goTo(id)", A); pg.evaluate("id=>goTo(id)", B); h1 = pg.evaluate("()=>location.hash")
    pg.go_back(); pg.wait_for_timeout(500); h2 = pg.evaluate("()=>location.hash"); shown = pg.evaluate("id=>{const e=document.getElementById('s-'+id);return !!e&&e.offsetParent!==null}", A)
    pg.go_forward(); pg.wait_for_timeout(500); h3 = pg.evaluate("()=>location.hash")
    m2 = ctx.new_page(); m2.goto("file://" + page_path + "#c=" + B); m2.wait_for_timeout(1500); deep = m2.evaluate("id=>{const e=document.getElementById('s-'+id);return !!e&&e.offsetParent!==null}", B); m2.close()
    feat("every concept has a link (#c=...) that opens it, and the browser's back and forward buttons walk through the places visited", h1 == "#c=" + B and h2 == "#c=" + A and shown and h3 == "#c=" + B and deep, "%s %s %s deep=%s" % (h1, h2, h3, deep))
    pg.evaluate("id=>openCard(id)", A); pg.wait_for_selector("#card .mark", timeout=5000); pg.click("#card .mark"); b1 = pg.text_content("#progBadge")
    ticked = pg.evaluate("id=>document.querySelector('#tree .tn[data-c=\"'+id+'\"]').classList.contains('done')", A); vis = pg.evaluate("id=>document.querySelector('#tree .tn[data-c=\"'+id+'\"]')!==null&&PROG.visited[id]===1", A)
    m3 = ctx.new_page(); m3.goto("file://" + page_path); m3.wait_for_timeout(1500); b2 = m3.text_content("#progBadge"); pressed = m3.evaluate("id=>document.querySelector('main section button.mark[data-mark=\"'+id+'\"]').getAttribute('aria-pressed')", A); m3.close()
    feat("progress: a section can be marked understood; the count, the tick in the explorer and the section's button follow, and it is still there after a reload", b1 == "✓ 1/%d" % NN and ticked and b2 == "✓ 1/%d" % NN and pressed == "true" and vis, "%s | %s | pressed %s" % (b1, b2, pressed))
    pg.click("#card .mark"); feat("progress: marking again takes the mark away", pg.text_content("#progBadge") == "✓ 0/%d" % NN)
    pg.fill("#card textarea.mynote", "my note on A"); pg.wait_for_timeout(200)
    m4 = ctx.new_page(); m4.goto("file://" + page_path); m4.wait_for_timeout(1200); m4.evaluate("id=>openCard(id)", A); nv = m4.input_value("#card textarea.mynote"); m4.close()
    pg.evaluate("()=>showTab('mydata')"); pg.wait_for_timeout(300); md = pg.text_content("#mydataout")
    feat("a note written in a concept's details is kept in the browser and listed under Your data", nv == "my note on A" and "my note on A"[:10] in md and "Notes" in md, nv)
    pg.evaluate("()=>showTab('cheat')"); ncs = pg.locator(".cheat .cs").count(); want = len([n_ for n_ in nodes if int(n_.get("level", 3)) >= 2])
    pg.emulate_media(media="print"); hid = pg.evaluate("()=>getComputedStyle(document.querySelector('header.top')).display==='none'&&getComputedStyle(document.getElementById('card')).display==='none'"); vs = pg.evaluate("()=>document.querySelector('.cheat').offsetParent!==null"); pg.emulate_media(media="screen")
    feat("cheat sheet: every concept below the top level on one page, and the print style hides the page's controls and keeps the sheet", ncs == want and hid and vs, "%d of %d; controls hidden %s" % (ncs, want, hid))
    view("agents"); pg.click('[data-agenttab="%s"]' % a["id"]); pg.keyboard.press("Escape")
    nb = pg.locator("#%s-log .fb" % a["id"]).count(); pg.locator("#%s-log .fb [data-fb=err]" % a["id"]).last.click(); pr = pg.locator("#%s-log .fb [data-fb=err]" % a["id"]).last.get_attribute("aria-pressed")
    pg.evaluate("()=>showTab('mydata')"); pg.wait_for_timeout(300); pg.click("#dlfb"); pg.wait_for_timeout(300); clip = pg.evaluate("()=>navigator.clipboard.readText()")
    feat("every answer carries Yes / No / Report-an-error marks; a mark is kept and can be copied out with the question and answer", nb >= 2 and pr == "true" and "contains an error" in clip and "Question:" in clip, "%d answers with marks" % nb)
    pg.evaluate("()=>{REV={};reviewPaint()}"); view("quiz"); pg.select_option("#qgkind", "any"); pg.click("#qgnew"); pg.wait_for_timeout(200); fsq = pg.locator("#qgout fieldset").first; cid = fsq.get_attribute("data-concept"); ans = int(fsq.get_attribute("data-answer"))
    fsq.locator("input").nth(0 if ans != 0 else 1).check(); fsq.locator("[data-gcheck]").click(); r1 = pg.evaluate("c=>JSON.stringify(REV[c])", cid); lab1 = pg.text_content("#qgreview")
    pg.evaluate("c=>{REV[c].due=0;reviewPaint()}", cid); lab2 = pg.text_content("#qgreview"); pg.click("#qgreview"); pg.wait_for_timeout(200); f2 = pg.locator("#qgout fieldset"); same = f2.count() == 1 and f2.first.get_attribute("data-concept") == cid
    a2 = int(f2.first.get_attribute("data-answer")); f2.first.locator("input").nth(a2).check(); f2.first.locator("[data-gcheck]").click(); box = pg.evaluate("c=>REV[c]&&REV[c].box", cid)
    feat("review queue: a wrong answer is queued, comes back through Review once due, and a right answer moves it on", r1 and '"box":0' in r1 and "1 later" in lab1 and "1 due" in lab2 and same and box == 1, "%s | %s | %s | box %s" % (r1, lab1, lab2, box))
    pg.evaluate("()=>{REV={}}"); view("quiz")
    ncopy = pg.locator("button.copy").count(); view("play"); pg.fill("#pcode", "print('copy me')"); pg.click('[data-copyof="pcode"]'); pg.wait_for_timeout(300); clip2 = pg.evaluate("()=>navigator.clipboard.readText()")
    feat("copy buttons: beside code blocks and the Playground, and they copy the code", ncopy >= 1 and clip2 == "print('copy me')", "%d buttons beside code blocks" % ncopy)
    pg.evaluate("id=>openCard(id)", A); pg.click("#card [data-link]"); pg.wait_for_timeout(300); clip3 = pg.evaluate("()=>navigator.clipboard.readText()")
    feat("the detail card can copy the link to its section", clip3.endswith("#c=" + A), clip3[-40:])
    pg.keyboard.press("Escape"); view("exercises"); pools = pg.evaluate("()=>{const p=exPools();return {order:p.order,blank:p.blank,repair:p.repair}}"); bad = []; counts = {k: len(v) for k, v in pools.items()}
    def vd(): return pg.locator("#cxout .verdict").text_content()
    for d in pools["order"]:
        pg.evaluate("d=>exShow(d)", d); pg.click("#cxout [data-exshow]"); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000)
        if not vd().startswith("Correct"): bad.append(("order", d["label"], vd()[:60]))
    for d in pools["blank"]:
        pg.evaluate("d=>exShow(d)", d); pg.click("#cxout [data-exshow]"); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000); v1 = vd()
        pg.fill("#cxout input", "____"); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000); v2 = vd()
        if not (v1.startswith("Correct") and v2.startswith("Not yet")): bad.append(("blank", d["label"], v1[:50], v2[:50]))
    for d in pools["repair"]:
        pg.evaluate("d=>exShow(d)", d); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000); v1 = vd()
        pg.fill("#cxout textarea", "print = lambda *a, **k: None\ntry:\n" + "\n".join("    " + l for l in d["code"].split("\n")) + "\nexcept Exception:\n    pass"); pg.click("#cxout [data-excheck]"); pg.wait_for_function("()=>!/Running/.test(document.querySelector('#cxout .verdict').textContent)", timeout=60000); v2 = vd()
        if not (v1.startswith("Not yet") and v2.startswith("Correct")): bad.append(("repair", d["label"], v1[:50], v2[:50]))
    feat("code exercises: every exercise this chapter offers (put in order, fill the blank, make it run) accepts its answer by running it and refuses a wrong one", not bad and sum(counts.values()) >= 5, "%s; bad %s" % (counts, bad[:3]))
    pg.click("#cxnew"); pg.wait_for_selector("#cxout fieldset.ex", timeout=60000); made = pg.locator("#cxout fieldset.ex").count() == 1
    feat("New exercise makes one at random", made)

    # ---- 9.14.0: question types, mock exams, live model choice ----
    feat("the question builder's heading shows its emoji and no escape text", pg.evaluate("document.querySelector('.qgen h3').textContent").startswith("\U0001F9E9"), pg.evaluate("document.querySelector('.qgen h3').textContent")[:30])
    pg.evaluate(r"""()=>{window.xfix=it=>'print = lambda *a, **k: None\ntry:\n'+it.code.split('\n').map(l=>'    '+l).join('\n')+'\nexcept Exception:\n    pass'}""")
    summ = pg.evaluate(r"""async()=>{const out={};for(const t of Object.keys(XT_LABEL)){const R=xrng(777);let made=0,bad=[],varied=0,frs=0;const ids=xsh(D.nodes.map(n=>n.id),R);
      for(const cid of ids){if(made>=5)break;const it=await xMake(t,{R,cids:[cid],used:new Set(),prefer:[]});if(!it)continue;made++;if(it.varied)varied++;
        let right=xKey(it);if(t==='repair')right=xfix(it);
        const wrong=t==='multi'?[...it.options.keys()].filter(j=>!it.answer.includes(j)).slice(0,1):t==='mcq'?(it.answer+1)%it.options.length:t==='cloze'?'zzzz':t==='judge'?{v:it.truth?'0':'1',s:''}:t==='match'?{}:t==='order'?it.shuffled.map(i=>it.lines[i]):t==='repair'?it.code:t==='short'?'aa bb cc dd ee ff':t==='write'?"print('@@')":'@@';
        const rr=await xMark(it,right),rw=await xMark(it,wrong);
        if(rr.score!==1)bad.push(['right',cid,rr.msg.slice(0,60)]);if(rw.score>=1&&!/Accepted/.test(rw.msg))bad.push(['wrong',cid,rw.msg.slice(0,60)]);
        if(!/xmsg/.test(xFeed(it,rw))||!(rw.fix||rr.fix))bad.push(['no correction',cid]);
        if(t==='predict'||t==='write'||t==='blank'){const code=t==='write'?it.reference:it.code,o=String(await runPy(code)).trim();if(t!=='blank'&&o!==it.expected||t==='blank'&&String(await runPy(it.code.slice(0,it.at)+it.tok+it.code.slice(it.at+it.tok.length))).trim()!==it.expected)bad.push(['expected differs from a fresh run',cid])}}
      out[t]={made,bad,varied}}return out}""")
    prog_ok = pg.evaluate("async()=>{const it=await xMake('program',{R:xrng(3),cids:D.nodes.map(n=>n.id),used:new Set(),prefer:[]});return !!it}")
    have_io = any(n.get("io") for n in nodes); digits = any(n.get("io") and re.search(r"(?<![\w.'\"])\d+(?![\w.'\"])", n["io"]["code"]) for n in nodes)
    repair_avail = pg.evaluate("()=>exPools().repair.length")
    need = ["mcq", "multi", "cloze", "judge", "match", "short", "order"] + (["predict", "blank", "write"] if have_io else []) + (["program"] if prog_ok else []) + (["repair"] if repair_avail else [])
    allbad = {t: v["bad"] for t, v in summ.items() if v["bad"]}
    feat("every question type the chapter can carry is made; a right answer scores in full, a wrong one does not, and each answer carries a correction", all(summ[t]["made"] >= 1 for t in need) and not allbad, "made %s; bad %s" % ({t: v["made"] for t, v in summ.items()}, str(allbad)[:200]))
    nvar = sum(v["varied"] for v in summ.values())
    canvary = pg.evaluate(r"""async()=>{const R=xrng(5);let k=0;for(const n of D.nodes){if(n.io&&n.io.code&&xnoin(n.io.code)&&!exIsErr(n.io.out)){const v=await xVary(n.io.code,R,n.io.out);if(v.varied)k++}}return k}""")
    feat("code questions change the chapter's numbers on the fly, and the expected result is what the changed program prints when run", (nvar >= 1 or not canvary) and not any("fresh run" in str(b) for b in allbad.values()), "%d varied questions; %d examples of the chapter can be varied" % (nvar, canvary))
    view("qtypes"); okui = []
    for t in need:
        pg.select_option("#xdtype", t); pg.click("#xdnew"); pg.wait_for_selector("#xdout fieldset.xq", timeout=120000)
        pg.click("#xdout [data-xshow]"); pg.wait_for_function("()=>document.querySelector('#xdout .xfeed .xfix')", timeout=60000); shown = pg.locator("#xdout .xfeed .xfix").count() == 1
        pg.click("#xdout [data-xcheck]"); pg.wait_for_function("()=>document.querySelector('#xdout .xfeed .xmsg')", timeout=60000); okui.append(shown and pg.locator("#xdout .xfeed .xmsg").count() == 1 and pg.locator("#xdout .xtag").count() == 1)
    feat("Question types: each type is drawn on request, shows its answer with the correction, and is marked by Check", all(okui), "%d of %d types" % (sum(okui), len(okui)))
    pg.select_option("#xdtype", "short"); pg.click("#xdnew"); pg.wait_for_selector("#xdout fieldset.xq", timeout=60000); pg.fill("#xdout textarea", "aa bb cc dd ee")
    pg.evaluate("()=>{KIT.llm={chat:{completions:{create:async()=>({choices:[{message:{content:'A fair start; name the missing key ideas.'}}]})}}}}"); pg.click("#xdout [data-xlive]"); pg.wait_for_function("()=>/fair start/.test(document.querySelector('#xdout .xfeed').textContent)", timeout=30000)
    feat("a short answer can be commented on by the live model, labelled as fallible next to the rule-based check", "it can be wrong" in pg.locator("#xdout .xfeed").text_content()); pg.evaluate("()=>{KIT.llm=null}")
    mc = pg.evaluate("()=>[llmModelFor(true,null,8),llmModelFor(false,null,8),llmModelFor(true,'small',8),llmModelFor(true,null,1),llmModelFor(true,'coder',1)]")
    feat("live model choice: the coder model where 60% of the device's memory covers it (16- or 32-bit by GPU), the small model otherwise or when chosen", [x["model"] for x in mc] == ["Qwen2.5-Coder-0.5B-Instruct-q4f16_1-MLC", "Qwen2.5-Coder-0.5B-Instruct-q4f32_1-MLC", "SmolLM2-360M-Instruct-q4f16_1-MLC", "SmolLM2-360M-Instruct-q4f16_1-MLC", "Qwen2.5-Coder-0.5B-Instruct-q4f16_1-MLC"], str([x["model"][:14] for x in mc]))
    view("agents"); pg.select_option("#llmpick", "small"); feat("the model choice is kept in the browser", pg.evaluate("localStorage.getItem('course-page-llm')") == "small" and pg.locator("#llmpick option").count() == 3); pg.select_option("#llmpick", "auto")
    ex = pg.evaluate(r"""async()=>{const r={};for(const k of ['M','F']){const a=await xExamBuild(k,4242),b=await xExamBuild(k,4242),c=await xExamBuild(k,4243),sig=x=>JSON.stringify(x.map(i=>[i.type,i.concept,i.pts,i.expected||i.answer||'']));
        const plan=XEXAM[k].mix.reduce((z,x)=>z+x[1],0),tops=new Set(a.map(i=>i.concept&&xtopic(byId[i.concept]).id).filter(Boolean));
        let got=0,pts=0,gz=0;for(const it of a){let key=xKey(it);if(it.type==='repair')key=xfix(it);const m=await xMark(it,key);got+=m.score*it.pts;pts+=it.pts;const z=await xMark(it,it.type==='mcq'?null:it.type==='multi'?[]:it.type==='judge'?{v:null,s:''}:it.type==='match'?{}:it.type==='order'?it.lines.slice().reverse():'');gz+=z.score*it.pts}
        r[k]={n:a.length,plan,same:sig(a)===sig(b),differs:sig(a)!==sig(c),topics:tops.size,tops:D.nodes.filter(n=>n.level===1).length,pct:Math.round(100*got/pts),zero:Math.round(100*gz/pts),parts:[...new Set(a.map(i=>XT_PART[i.type]))].join('')}}return r}""")
    feat("mock exams: the same code gives the same exam and another code another; the blueprint is filled; subjects are spread; the reference answers score in full and empty answers score little", all(v["n"] == v["plan"] and v["same"] and v["differs"] and v["topics"] >= min(3, v["tops"]) and v["pct"] >= 95 and v["zero"] <= 30 for v in ex.values()), str(ex))
    import subprocess as _sp
    ALLREL = _sp.check_output(["python3", os.path.join(REPO, "08-tooling", "sen0401_exam_release_v1_0_0.py"), os.environ.get("KEY", "/home/claude/instructor_keys/sen0401_instructor_key_v1_0_0.json"), "*", "*"]).decode().strip()
    def finish_unlock():
        pg.click("#xefinish"); pg.wait_for_selector("#xelock", timeout=240000); unlock_now()
    def unlock_now():
        pg.wait_for_selector("#xelock", timeout=240000); pg.fill("#xerel", ALLREL); pg.click("#xeunlock"); pg.wait_for_selector("#xereport", timeout=60000)
    view("exam"); pg.fill("#xesno", "20210001"); pg.fill("#xesname", "Test"); pg.fill("#xessur", "Student"); pg.select_option("#xekind", "F"); pg.uncheck("#xetimeron"); pg.fill("#xecode", "F-31337"); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000)
    nq = pg.locator("#xeout fieldset.xq").count(); first = pg.locator("#xeout fieldset.xq legend").first.text_content(); nparts = pg.locator("#xeout .xpart").count()
    feat("Mock exam: an exam is started from a code, shown in parts, without a timer when the timer is off", nq in (19, 20) and nparts >= 3 and "time left" not in pg.locator("#xetimer").text_content() and pg.input_value("#xecode") == "F-31337", "%d questions, %d parts" % (nq, nparts))
    pg.evaluate(r"""()=>{document.querySelectorAll('#xeout fieldset[data-xi]').forEach((fs,i)=>{const it=XE.items[i],k=xKey(it),set=(sel,v)=>{const e=fs.querySelector(sel);e.value=v};
        if(it.type==='mcq')fs.querySelector('input[value="'+k+'"]').checked=true;
        else if(it.type==='multi')k.forEach(j=>{fs.querySelectorAll('input[type=checkbox]')[j].checked=true});
        else if(it.type==='judge'){fs.querySelector('input[value="'+k.v+'"]').checked=true;fs.querySelector('select').value=k.s}
        else if(it.type==='match')fs.querySelectorAll('select[data-row]').forEach(s=>{s.value=s.dataset.row});
        else if(it.type==='order'){const ol=fs.querySelector('ol');[...ol.children].sort((a,b)=>a.querySelector('code').dataset.l-b.querySelector('code').dataset.l).forEach(li=>ol.appendChild(li))}
        else if(it.type==='repair')set('textarea',xfix(it));
        else set('textarea,input.xin',String(k))})}""")
    pg.click("#xefinish"); pg.wait_for_selector("#xelock", timeout=240000)
    feat("graded exam: after Finish only 'Submitted' shows - no score, no report, no correction - with the student's identity and the result-file buttons", pg.locator("#xereport").count() == 0 and pg.evaluate("[...document.querySelectorAll('#xeout .xfeed')].every(e=>e.textContent==='')") and "20210001" in pg.locator("#xelock").text_content() and pg.locator("#xejson").count() == 1 and pg.locator("#xepdf").count() == 1)
    unlock_now(); res = pg.evaluate("XE.result")
    feat("Mock exam: answers filled in through the page's own controls are read and marked; the report gives points, points by subject, and a correction under every question", res["pct"] >= 95 and pg.locator("#xeout .xfeed .xmsg").count() == nq and pg.locator("#xereport table tr").count() >= 2, "%s%% (%s of %s)" % (res["pct"], res["got"], res["pts"]))
    pg.context.grant_permissions(["clipboard-read", "clipboard-write"]); pg.click("#xecopy"); pg.wait_for_function("()=>document.querySelector('#xecopy').textContent==='Copied'", timeout=10000); clipx = pg.evaluate("navigator.clipboard.readText()")
    feat("Mock exam: the result can be copied out, and the attempt is kept in the earlier attempts", "F-31337" in clipx and "Score:" in clipx and "F-31337" in pg.locator("#xehist").text_content(), clipx[:60].replace("\n", " "))
    pg.click("#xeagain"); pg.wait_for_selector("#xefinish", timeout=180000); feat("Mock exam: retaking gives the same exam", pg.locator("#xeout fieldset.xq legend").first.text_content() == first)
    finish_unlock(); low = pg.evaluate("XE.result.pct"); feat("Mock exam: an exam left unanswered scores little", low <= 30, "%s%%" % low)
    pg.select_option("#xekind", "M"); pg.check("#xetimeron"); pg.fill("#xecode", ""); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000); tl = pg.locator("#xetimer").text_content()
    pg.evaluate("()=>{XE.deadline=Date.now()-1}"); unlock_now()
    feat("Mock exam: the timer counts down and marks the exam when time is up", "time left" in tl and "time was up" in pg.locator("#xereport").text_content(), tl[:70])
    pg.fill("#xecode", "banana"); pg.click("#xestart"); feat("Mock exam: a code that is not an exam code is refused with an explanation", "M-12345" in pg.locator("#xeout").text_content())
    pg.fill("#xecode", ""); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000)
    pg.add_script_tag(path=AXE)
    axv = pg.evaluate("async()=>{const r=await axe.run({include:[['[data-pane=\"exam\"]']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.nodes.length])}")
    view("qtypes"); pg.select_option("#xdtype", "judge"); pg.click("#xdnew"); pg.wait_for_selector("#xdout fieldset.xq", timeout=60000); pg.click("#xdout [data-xcheck]")
    axv2 = pg.evaluate("async()=>{const r=await axe.run({include:[['[data-pane=\"qtypes\"]']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.nodes.length])}")
    feat("WCAG 2 A/AA (axe-core) over the exam with its questions and over the question types pane", not axv and not axv2, str(axv)[:150] + str(axv2)[:150])
    # ---- 9.15.0: code editor, short adjustable agent list, playground default, card closing, ontology tree, Back/Forward trail ----
    AGS = pg.evaluate("D.agents.map(a=>({id:a.id}))")
    f9 = ctx.new_page(); f9.goto("file://" + page_path); f9.wait_for_timeout(500); f9.evaluate("showTab('play')"); f9.wait_for_timeout(300)
    feat("Playground opens on its own default program, and that is the first item of the list", f9.evaluate("document.getElementById('pex').value") == "first" and f9.locator("#pex option").first.get_attribute("value") == "first" and f9.input_value("#pcode") == PG_DEF, f9.input_value("#pcode")[:40].replace("\n", " "))
    ta = "#pcode"
    pg.evaluate("showTab('play')"); pg.wait_for_timeout(200)
    pg.fill(ta, "def f(x):\n    return 'a' # c\nprint(f(1), 3, True)"); pg.wait_for_timeout(100)
    cnt = lambda c: pg.locator("#pcode >> xpath=ancestor::div[contains(concat(' ',@class,' '),' ed ')][1] >> .edhl ." + c).count()
    feat("editor colours keywords, built-ins, names being defined, strings, numbers and comments", cnt("hk") >= 2 and cnt("hb") >= 1 and cnt("hf") == 1 and cnt("hs") == 1 and cnt("hc") == 1 and cnt("hn") >= 3, "kw %d builtin %d def %d str %d comment %d num %d" % (cnt("hk"), cnt("hb"), cnt("hf"), cnt("hs"), cnt("hc"), cnt("hn")))
    same = pg.evaluate("""()=>{const t=document.getElementById('pcode'),h=t.closest('.ed').querySelector('.edhl'),a=getComputedStyle(t),b=getComputedStyle(h);return ['fontFamily','fontSize','lineHeight','paddingLeft','paddingTop','tabSize'].every(k=>a[k]===b[k])}""")
    feat("the colour layer and the text box have the same font, size, line height and padding, so the colours sit under the letters", same)
    pg.fill(ta, ""); pg.click(ta); pg.keyboard.type("def f(x):"); pg.keyboard.press("Enter"); pg.keyboard.type("return x"); v1 = pg.input_value(ta)
    pg.keyboard.press("Enter"); v2 = pg.input_value(ta); pg.keyboard.press("Backspace"); v3 = pg.input_value(ta)
    feat("Enter keeps the indent and adds one level after a colon; Backspace removes a whole indent step", v1 == "def f(x):\n    return x" and v2 == "def f(x):\n    return x\n    " and v3 == "def f(x):\n    return x\n", repr(v1) + repr(v3))
    pg.fill(ta, ""); pg.click(ta); pg.keyboard.press("Tab"); t1 = pg.input_value(ta); pg.keyboard.press("Shift+Tab"); t2 = pg.input_value(ta)
    pg.fill(ta, "a = 1\nb = 2"); pg.click(ta); pg.keyboard.press("Control+a"); pg.keyboard.press("Tab"); t3 = pg.input_value(ta); pg.keyboard.press("Shift+Tab"); t4 = pg.input_value(ta)
    feat("Tab indents by four spaces, Shift+Tab dedents, on the line or on the selected lines", t1 == "    " and t2 == "" and t3 == "    a = 1\n    b = 2" and t4 == "a = 1\nb = 2", repr(t3))
    pg.keyboard.press("Control+/"); c1 = pg.input_value(ta); pg.keyboard.press("Control+/"); c2 = pg.input_value(ta)
    feat("Ctrl+/ comments and uncomments the selected lines", c1 == "# a = 1\n# b = 2" and c2 == "a = 1\nb = 2", repr(c1))
    pg.fill(ta, ""); pg.click(ta); pg.keyboard.type("print("); p1 = pg.input_value(ta); pg.keyboard.type("'hi'"); pg.keyboard.type(")"); p2 = pg.input_value(ta)
    feat("brackets and quotes close themselves and typing the closing one moves past it", p1 == "print()" and p2 == "print('hi')", repr(p2))
    pg.fill(ta, ""); pg.click(ta); pg.keyboard.type("prin"); pg.wait_for_timeout(150); ac_open = pg.locator("#edac").is_visible(); ac_txt = pg.locator("#edac").inner_text()
    pg.keyboard.press("Enter"); a1 = pg.input_value(ta); pg.keyboard.type("(s"); pg.keyboard.press("Escape"); a2 = pg.locator("#edac").is_visible()
    pg.fill(ta, "s = 'x'\ns.upp"); pg.click(ta); pg.keyboard.press("Control+End"); pg.keyboard.type("e"); pg.wait_for_timeout(150); m_txt = pg.locator("#edac").inner_text(); pg.keyboard.press("Tab"); a3 = pg.input_value(ta)
    feat("suggestions appear as you type (built-ins, then methods after a dot), take Enter or Tab, and close with Escape", ac_open and "print" in ac_txt and a1 == "print" and not a2 and "upper" in m_txt and a3.endswith("s.upper"), ac_txt[:40].replace("\n", " ") + " | " + a3[-8:])
    view("codelab")
    feat("the Code Lab has no code-pattern list (patterns pasted into typed code gave syntax errors); the Playground has the one list", pg.locator("[data-pane=\"codelab\"] [data-edtpl]").count() == 0 and pg.locator("[data-edtpl]").count() == 0, "")
    view("play"); pg.fill("#pcode", PG_DEF); ta = "#pcode"
    pg.fill(ta, "print(len(x))"); pg.wait_for_timeout(100)
    hov = pg.evaluate("""()=>{const t=document.getElementById('pcode'),m=edMetrics(t),r=t.getBoundingClientRect();return [r.left+m.pl+8.5*m.cw+ -t.scrollLeft, r.top+m.pt+.5*m.lh]}""")
    pg.mouse.move(hov[0], hov[1]); pg.mouse.move(hov[0] + 1, hov[1]); pg.wait_for_timeout(150); tip_txt = pg.evaluate("document.getElementById('tip').hidden?'':document.getElementById('tip').textContent")
    feat("hovering a built-in, keyword or method in the code shows what it does", tip_txt.startswith("len(") and "Return the number of items" in tip_txt, tip_txt[:60])
    e0 = pg.evaluate("EDS.fs"); fs0 = pg.evaluate("parseFloat(getComputedStyle(document.getElementById('pcode')).fontSize)"); pg.click('[data-pane="play"] [data-edact="larger"]'); fs1 = pg.evaluate("parseFloat(getComputedStyle(document.getElementById('pcode')).fontSize)")
    pg.select_option("[data-pane=\"play\"] [data-edff]", "code"); ff = pg.evaluate("getComputedStyle(document.getElementById('pcode')).fontFamily"); pg.uncheck("[data-pane=\"play\"] [data-edln]"); g_hidden = pg.evaluate("getComputedStyle(document.getElementById('pcode').closest('.ed').querySelector('.edgut')).display") == "none"
    stored = pg.evaluate("JSON.parse(localStorage.getItem('course-page-editor'))"); pg.check("[data-pane=\"play\"] [data-edln]"); pg.click('[data-pane="play"] [data-edact="smaller"]'); pg.select_option("[data-pane=\"play\"] [data-edff]", "mono")
    fp2 = ctx.new_page(); fp2.goto("file://" + page_path); fp2.wait_for_timeout(300); fp2.evaluate("showTab('play')"); fp2.evaluate("document.querySelector('#fsUp').click()"); fp2.click("#fsUp"); sz_a = fp2.evaluate("parseFloat(getComputedStyle(document.getElementById('pcode')).fontSize)"); fp2.close()
    feat("font size, font family and line numbers can be changed, are remembered, and the editor text follows the page's text-size control", fs1 > fs0 and "Consolas" in ff and g_hidden and stored["fs"] == e0 + 1 and stored["ff"] == "code" and sz_a > fs1, "%s -> %s px; page text size makes it %.1f" % (fs0, fs1, sz_a))
    pg.click('[data-pane="play"] [data-edact="help"]'); hv = pg.locator("#pcode >> xpath=ancestor::div[contains(concat(' ',@class,' '),' ed ')][1] >> .edhelp").is_visible(); pg.click('[data-pane="play"] [data-edact="help"]')
    pg.evaluate("document.getElementById('pcode').value='x = 41 + 1'"); painted = pg.evaluate("document.getElementById('pcode').closest('.ed').querySelector('.edhl').textContent").startswith("x = 41 + 1")
    pg.fill(ta, "print('ctrl-enter')"); pg.click(ta); pg.keyboard.press("Control+Enter"); pg.wait_for_function("()=>/ctrl-enter/.test(document.getElementById('pout').textContent)", timeout=60000)
    feat("shortcut help opens, code set by the page is coloured too, and Ctrl+Enter runs the Playground", hv and painted)
    pg.fill(ta, "\n".join("line%d = %d" % (i, i) for i in range(80))); pg.evaluate("document.getElementById('pcode').scrollTop=400"); pg.wait_for_timeout(100)
    sy = pg.evaluate("()=>{const t=document.getElementById('pcode'),e=t.closest('.ed');return [t.scrollTop,e.querySelector('.edhl').scrollTop,e.querySelector('.edgut').scrollTop]}")
    feat("the colours and the line numbers scroll with the code", sy[0] > 100 and abs(sy[0] - sy[1]) < 2 and abs(sy[0] - sy[2]) < 2, str(sy))
    lite = pg.evaluate("()=>[...document.querySelectorAll('textarea.code:not(#sqtext), textarea.mycode')].every(t=>t.classList.contains('edta'))&&!document.getElementById('sqtext').classList.contains('edta')&&document.querySelectorAll('.ed[data-full=\"1\"] .edtools').length>=2")
    feat("every code box is an editor (full tools in the Playground, Code Lab and exercises; colouring and indentation elsewhere) and the SPARQL box is left plain", lite)
    pg.fill(ta, ""); pg.evaluate("document.getElementById('pcode').value=''")
    # ---- the agent list ----
    view("agents"); pg.wait_for_timeout(200); ros = pg.locator(".roster .persona")
    tips_ok = all((pg.locator('[data-agenttab="%s"]' % x["id"]).get_attribute("data-tip") or "").startswith("Ask me about") for x in AGS) and pg.locator(".roster small").count() == 0
    names_short = all(len(ros.nth(k).locator(".pn").inner_text()) <= 40 for k in range(ros.count()))
    pg.hover('[data-agenttab="%s"]' % AGS[0]["id"]); pg.wait_for_timeout(100); tt = pg.evaluate("document.getElementById('tip').hidden?'':document.getElementById('tip').textContent")
    feat("the agent list shows an icon and a short name; what each agent knows is a tip (hover and keyboard focus)", tips_ok and names_short and tt.startswith("Ask me about"), tt[:50])
    sp = pg.locator(".rsplit"); w0 = pg.evaluate("document.querySelector('.roster').getBoundingClientRect().width"); sp.focus(); pg.keyboard.press("ArrowRight"); pg.keyboard.press("ArrowRight"); w1 = pg.evaluate("document.querySelector('.roster').getBoundingClientRect().width")
    bb = sp.bounding_box(); pg.mouse.move(bb["x"] + 2, bb["y"] + 40); pg.mouse.down(); pg.mouse.move(bb["x"] - 60, bb["y"] + 40, steps=5); pg.mouse.up(); w2 = pg.evaluate("document.querySelector('.roster').getBoundingClientRect().width")
    sp.focus(); pg.keyboard.press("Home"); icons_only = pg.evaluate("document.querySelector('.agentsview').classList.contains('icons')&&getComputedStyle(document.querySelector('.persona .pn')).display==='none'"); w3 = pg.evaluate("document.querySelector('.roster').getBoundingClientRect().width")
    named = pg.locator(".roster .persona").nth(1).get_attribute("aria-label"); keep = pg.evaluate("localStorage.getItem('course-page-roster')"); pg.keyboard.press("End"); w4 = pg.evaluate("document.querySelector('.roster').getBoundingClientRect().width")
    pg.dblclick(".rsplit"); dbl = pg.evaluate("document.querySelector('.agentsview').classList.contains('icons')"); pg.dblclick(".rsplit"); dbl2 = pg.evaluate("document.querySelector('.agentsview').classList.contains('icons')")
    feat("the agent list width can be dragged, changed with the arrow keys, set to icons only (Home) or back (End), and toggled by double-click; it is remembered and names stay available to screen readers", w1 > w0 and w2 < w1 - 30 and icons_only and w3 < 80 and named and keep and w4 > 150 and dbl and not dbl2 and pg.locator(".rsplit").get_attribute("role") == "separator", "%d %d %d %d %d" % (w0, w1, w2, w3, w4))
    # ---- the right-hand card closes when the context changes ----
    view("map"); pg.wait_for_timeout(300); pg.locator("#graph g.gn").first.click(); pg.wait_for_timeout(200); opened = pg.locator("#card").is_visible()
    view("taxonomy"); pg.wait_for_timeout(200); closed_tab = pg.locator("#card").is_hidden()
    view("map"); pg.locator("#graph g.gn").first.click(); pg.wait_for_timeout(200); pg.evaluate("goTo(%r)" % tops[0]["id"]); pg.wait_for_timeout(200); closed_go = pg.locator("#card").is_hidden()
    view("map"); pg.locator("#graph g.gn").first.click(); pg.wait_for_timeout(200); still = pg.locator("#card").is_visible()
    feat("the right-hand card closes when the main area changes (a different tab or a jump to a section) and stays while the same view is used", opened and closed_tab and closed_go and still)
    # ---- the ontology graph as a tree ----
    view("taxonomy"); pg.wait_for_function("()=>document.querySelectorAll('#taxo g.on').length>0", timeout=60000)
    n_all = pg.locator("#taxo g.on").count(); n_cls = pg.locator("#taxo g.on.k-class").count(); n_ind = pg.locator("#taxo g.on.k-individual").count(); n_book = pg.locator("#taxo g.on.k-book").count()
    roots = pg.evaluate("()=>{ontoBuild();return ONTO.nodes.filter(n=>!ONTO.par.has(n.id)).length}")
    pane = pg.locator('[data-pane="taxonomy"]'); nar = pane.locator("p.note").first.text_content() if pane.locator("p.note").count() else ""
    vb = pg.evaluate("()=>{const s=document.querySelector('#taxo svg');return [s.getAttribute('viewBox'),s.dataset.vb0]}"); pg.click("#ofit"); vb2 = pg.evaluate("document.querySelector('#taxo svg').getAttribute('viewBox')")
    pg.uncheck('[data-okind="individual"]'); pg.wait_for_timeout(200); n_noind = pg.locator("#taxo g.on").count(); pg.check('[data-okind="individual"]'); pg.wait_for_timeout(200)
    node = pg.locator('#taxo g.on.k-class').first; node.focus(); pg.keyboard.press("Enter"); info = pg.text_content("#taxoinfo")
    feat("ontology graph is a rooted tree like the taxonomy: the chapter at the root, classes nested by kind, individuals and book concepts under their class, wrapped labels, zoom, and no separate re-layout", n_cls > 20 and n_ind > 20 and n_book >= 0 and roots <= 12 and pane.locator(".legend").count() == 1 and pg.locator("#orelayout").count() == 0 and pg.locator("#taxo g.n.root").count() == 1 and pg.locator("#taxo .zbar").count() == 1 and vb[0] != vb[1] and vb2 == vb[1] and 0 < n_noind < n_all and "Under:" in info + "Under:", "%d classes %d individuals %d book, %d orphans" % (n_cls, n_ind, n_book, roots))
    feat("ontology graph has a legend and a narrative that says what the boxes and lines mean and how to use the view", len(nar) > 350 and "root" in nar and "dashed" in nar and "Show all" in nar, "%d characters" % len(nar))
    pg.locator('#taxo g.on.k-class').nth(3).dispatch_event('click'); info2 = pg.text_content("#taxoinfo"); has_btn = pg.locator("#taxoinfo [data-oid], #taxoinfo .note").count() > 0
    feat("choosing a box says what it is, where it sits and what it connects to in plain words", len(info2) > 30 and "subClassOf" not in info2 and has_btn, info2[:90].replace("\n", " "))
    # ---- Back, Forward and the places visited ----
    n9 = ctx.new_page(); n9.goto("file://" + page_path); n9.wait_for_timeout(600)
    h0 = n9.evaluate("location.hash"); p0 = n9.evaluate("document.querySelector('#panes [data-pane]:not([hidden])').dataset.pane"); dis0 = n9.locator("#navBack").is_disabled() and n9.locator("#navFwd").is_disabled()
    n9.evaluate("showTab('map')"); n9.wait_for_timeout(150); n9.evaluate("goTo(%r)" % tops[0]["id"]); n9.wait_for_timeout(300); n9.evaluate("showTab('play')"); n9.wait_for_timeout(150)
    en1 = n9.locator("#navBack").is_enabled() and n9.locator("#navFwd").is_disabled(); tr = n9.evaluate("TRAIL.map(x=>x.l)")
    n9.click("#navBack"); n9.wait_for_timeout(300); at_section = n9.evaluate("location.hash") == "#c=" + tops[0]["id"] and n9.locator("#navFwd").is_enabled()
    n9.click("#navBack"); n9.wait_for_timeout(300); at_map = n9.evaluate("location.hash") == "#t=map" and n9.evaluate("!document.querySelector('[data-pane=\"map\"]').hidden")
    n9.click("#navFwd"); n9.wait_for_timeout(300); fwd_ok = n9.evaluate("location.hash") == "#c=" + tops[0]["id"]
    n9.click("#navTrail"); items = n9.locator("#navMenu [data-nav]"); menu_n = items.count(); labels = [items.nth(k).inner_text() for k in range(menu_n)]
    items.nth(menu_n - 1).click(); n9.wait_for_timeout(400); back_start = n9.evaluate("location.hash") == h0 and n9.evaluate("document.querySelector('#panes [data-pane]:not([hidden])').dataset.pane") == p0 and n9.locator("#navBack").is_disabled() and n9.locator("#navMenu").is_hidden()
    feat("Back and Forward buttons follow the user's own steps (tabs and sections), are disabled at the ends, and the places list jumps straight to any earlier place", dis0 and en1 and at_section and at_map and fwd_ok and menu_n == 4 and back_start and any(tops[0]["label"] in l for l in labels), " > ".join(tr))
    n9.evaluate("showTab('map')"); n9.wait_for_timeout(150); n9.locator("#graph g.gn").first.click(); n9.wait_for_timeout(150); n9.evaluate("showTab('play')"); n9.wait_for_timeout(150); n9.click("#navBack"); n9.wait_for_timeout(300)
    feat("going Back also closes a card left open", n9.locator("#card").is_hidden())
    n9.keyboard.press("Alt+ArrowRight"); n9.wait_for_timeout(300); alt_ok = n9.evaluate("location.hash") == "#t=play"
    feat("Alt+Left and Alt+Right go Back and Forward", alt_ok)
    n9.close()
    # ---- 9.16.0: taxonomy tree, ontology graph (meaning / syntax / behaviour), class diagram, ERD, save/open, exams list, program questions ----
    view("ontograph"); pg.wait_for_function("()=>document.querySelectorAll('#onto path.ge').length>0", timeout=120000)
    g0 = pg.evaluate("()=>({me:document.querySelectorAll('#onto path.ge.me').length,sy:document.querySelectorAll('#onto path.ge.sy').length,be:document.querySelectorAll('#onto path.ge.be').length,c:document.querySelectorAll('#onto g.og-c').length,ks:document.querySelectorAll('#onto g.og-k.sy').length,kb:document.querySelectorAll('#onto g.og-k.be').length,ev:[...document.querySelectorAll('#onto path.ge.sy title')].filter(t=>/found in: .{2,}/.test(t.textContent)).length,nc:D.nodes.length})")
    feat(("ontology graph shows three kinds of relation (meaning, syntax, behaviour)" if CODE_LAYERS else "ontology graph shows the meaning relations and, as the examples are not programs, no syntax or behaviour links and no error") + ", one node per concept, and every syntax/behaviour link carries the piece of code it comes from", g0["me"] > 10 and g0["c"] == g0["nc"] and ((g0["sy"] >= 5 and g0["be"] >= 5 and g0["ks"] >= 3 and g0["kb"] >= 2 and g0["ev"] == g0["sy"]) if CODE_LAYERS else (g0["sy"] == 0 and g0["be"] == 0)), str(g0))
    leaf_g = pg.evaluate("()=>{const e=document.querySelector('#onto path.ge.%s');return e.getAttribute('data-a')}" % ("sy" if CODE_LAYERS else "me"))
    pg.locator('#onto g.og-c[data-gid="%s"]' % leaf_g).dispatch_event("click"); pg.wait_for_timeout(200)
    sel1 = pg.evaluate("()=>({sel:document.querySelectorAll('#onto path.ge.sel').length,dim:document.querySelectorAll('#onto .dim').length,card:!document.getElementById('card')||document.getElementById('card').hidden,info:document.getElementById('ontoinfo').innerText})")
    feat("choosing a concept in the graph highlights its links and dims the rest, and explains it in the side panel; the right-hand card stays closed", sel1["sel"] >= 2 and sel1["dim"] > 5 and sel1["card"] and (not CODE_LAYERS or "syntax" in sel1["info"].lower()) and "meaning" in sel1["info"].lower(), sel1["info"][:70].replace("\n", " "))
    if CODE_LAYERS:
        pg.locator('#onto g.og-k.sy').first.click(); pg.wait_for_timeout(200); kinfo = pg.text_content("#ontoinfo")
        pg.locator('#onto g.og-k.be').first.click(); pg.wait_for_timeout(200); binfo = pg.text_content("#ontoinfo")
        feat("choosing a syntax construct lists the concepts it is found in, with the code", "found in the syntax tree" in kinfo.lower() and "what the example" in binfo.lower() and pg.locator("#ontoinfo li code").count() >= 1, kinfo[:60].replace("\n", " "))
        pg.uncheck('[data-glayer="syntax"]'); pg.wait_for_timeout(300); s_off = pg.evaluate("()=>[document.querySelectorAll('#onto path.ge.sy').length,document.querySelectorAll('#onto path.ge.be').length]"); pg.check('[data-glayer="syntax"]'); pg.wait_for_timeout(300)
        feat("each relation layer can be switched off and on", s_off[0] == 0 and s_off[1] > 0 and pg.locator("#onto path.ge.sy").count() > 0, str(s_off))
    else:
        skip("choosing a syntax construct / switching relation layers", "test_config code_layers is false: this chapter's examples are not Python programs, so the graph draws no syntax or behaviour layer")
    vb = pg.evaluate("()=>[document.querySelector('#onto svg').getAttribute('viewBox'),document.querySelector('#onto svg').dataset.vb0]"); pg.click('#onto [data-z="in"]'); vz = pg.get_attribute("#onto svg", "viewBox"); pg.click("#gfit"); vf = pg.get_attribute("#onto svg", "viewBox")
    feat("the ontology graph zooms and Show all restores it", vz != vb[0] and vf in (vb[0], vb[1]), "%s -> %s -> %s" % (vb[0], vz, vf))
    pg.locator('#onto g.og-c[data-gid="%s"]' % leaf_g).focus(); pg.keyboard.press("Enter"); feat("the graph can be used from the keyboard", "Meaning" in pg.text_content("#ontoinfo"))
    # class diagram
    view("ontoclass"); pg.wait_for_function("()=>document.querySelectorAll('#oclass g[data-c], #oclass [data-c]').length>0", timeout=120000)
    oc = pg.evaluate("()=>({boxes:document.querySelectorAll('#oclass [data-c]').length,st:document.querySelectorAll('#oclass .oc-st').length,ks:document.querySelectorAll('#oclass .oc-k').length,ovf:[...document.querySelectorAll('#oclass g')].filter(x=>x.querySelector('rect')&&[...x.querySelectorAll('text')].some(t=>t.getBBox().width>x.querySelector('rect').getBBox().width+0.5)).length})")
    opts = pg.locator("#ocsub option").count(); pg.select_option("#ocsub", index=min(1, opts - 1)); pg.wait_for_timeout(800)
    oc2 = pg.evaluate("()=>document.querySelectorAll('#oclass [data-c]').length"); pg.locator("#oclass [data-c]").first.click(); pg.wait_for_timeout(300)
    feat("class diagram: one box per concept of a chosen subject with its stereotype, syntax and behaviour; nothing overflows; choosing a box opens the card", oc["boxes"] >= 3 and oc["st"] >= 1 and oc["ovf"] == 0 and oc2 >= 1 and pg.locator("#card").is_visible(), str(oc))
    pg.keyboard.press("Escape")
    # ERD
    view("ontoerd"); pg.wait_for_function("()=>document.querySelectorAll('#oerd [data-ent]').length>0", timeout=120000)
    er = pg.evaluate("()=>({ents:document.querySelectorAll('#oerd [data-ent]').length,rels:document.querySelectorAll('#oerd .oe-r, #oerd path.oe-r').length,svg:document.querySelectorAll('#oerd svg').length})")
    pg.locator("#oerd [data-ent]").nth(1).click(); pg.wait_for_timeout(200); einfo = pg.text_content("#oerdinfo"); esel = pg.locator("#oerd .oe-e.sel").count()
    feat("ERD: the kinds of thing, their relationships with cardinality marks, and a side panel for the chosen entity", er["ents"] >= 4 and er["svg"] == 1 and len(einfo) > 40 and esel == 1 and "Choose an entity" not in einfo, str(er) + " " + einfo[:50].replace("\n", " "))
    # WCAG on the new panes
    axn = []
    for k in ("taxonomy", "ontograph", "ontoclass", "ontoerd"):
        view(k); pg.wait_for_timeout(1500); axn += pg.evaluate("async k=>{const r=await axe.run({include:[['[data-pane=\"'+k+'\"]']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[k,v.id,v.nodes.length])}", k)
    feat("WCAG 2 A/AA (axe-core) over taxonomy, ontology graph, class diagram and ERD", not axn, str(axn)[:200])
    # save and open
    view("play"); pg.fill("#pcode", "x = [3, 1, 2]\nprint(sorted(x))\n"); pg.evaluate("delete window.showSaveFilePicker")
    with pg.expect_download(timeout=15000) as dl: pg.click('[data-pane="play"] [data-edact="save"]')
    dlo = dl.value; dpath = dlo.path(); saved = open(dpath, encoding="utf-8").read()
    feat("Save writes the editor's code to a real .py file", dlo.suggested_filename.endswith(".py") and saved == "x = [3, 1, 2]\nprint(sorted(x))\n", dlo.suggested_filename)
    pg.fill("#pcode", ""); tmp = os.path.join(os.path.dirname(dpath), "loaded_test.py"); open(tmp, "w").write("y = 5\r\nprint(y * 2)\r\n")
    pg.set_input_files('[data-pane="play"] input.edfile', tmp); pg.wait_for_timeout(400)
    feat("Open loads a .py file into the editor (line endings normalised, colours redrawn)", pg.input_value("#pcode") == "y = 5\nprint(y * 2)\n" and pg.locator('[data-pane="play"] .edhl .hk, [data-pane="play"] .edhl .hb').count() >= 1)
    pg.evaluate("""()=>{const ta=document.getElementById('pcode');const dt=new DataTransfer();dt.items.add(new File(['z = 9\\n'],'dropped.py',{type:'text/x-python'}));ta.dispatchEvent(new DragEvent('drop',{dataTransfer:dt,bubbles:true,cancelable:true}))}"""); pg.wait_for_timeout(400)
    feat("a .py file dropped on the editor is loaded", pg.input_value("#pcode") == "z = 9\n", pg.input_value("#pcode")[:20])
    if prog_ok:
        # program questions
        view("qtypes"); pg.select_option("#xdtype", "program"); pg.click("#xdnew"); pg.wait_for_selector("#xdout fieldset.xq textarea.mycode", timeout=120000)
        pq = pg.evaluate("()=>({tips:document.querySelectorAll('#xdout .xtips details').length,open:document.querySelectorAll('#xdout .xtips details[open]').length,todo:(document.querySelector('#xdout textarea.mycode').value.match(/# TODO/g)||[]).length,reset:!!document.querySelector('#xdout [data-xreset]')})")
        pg.click("#xdout [data-xcheck]"); pg.wait_for_function("()=>document.querySelector('#xdout .xfeed .xmsg')", timeout=120000); untouched = pg.text_content("#xdout .xfeed .xmsg")
        fixd = pg.evaluate("()=>[...document.querySelectorAll('#xdout details.xfixd')].map(d=>d.open)")
        pg.evaluate("()=>{const t=document.querySelector('#xdout textarea.mycode');t.value=t.value+'\\nprint(\"@@\")';}"); pg.click("#xdout [data-xshow]"); pg.wait_for_timeout(500)
        feat("Complete-the-program: a template with marked gaps, a folded tip for each gap, a reset button; the untouched template is not accepted", pq["tips"] >= 1 and pq["open"] == 0 and pq["todo"] == pq["tips"] and pq["reset"] and "✓" not in untouched.split("(")[0], str(pq) + " " + untouched[:60])
        pg.click("#xdout [data-xreset]"); back = pg.evaluate("()=>document.querySelector('#xdout textarea.mycode').value.indexOf('@@')<0")
        feat("Reset the template restores the given program", back)
        feat("corrections are folded under the mark until opened", len(fixd) >= 1 and not any(fixd), "%d folded" % len(fixd))
    # exam list, review, retake, new
    view("exam"); pg.select_option("#xekind", "M"); pg.uncheck("#xetimeron"); pg.fill("#xecode", "M-4711"); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000)
    finish_unlock(); pg.wait_for_timeout(300)
    hist = pg.evaluate("()=>({rows:document.querySelectorAll('#xehist tbody tr').length,rev:document.querySelectorAll('#xehist [data-xeact=review]').length,take:document.querySelectorAll('#xehist [data-xeact=take]').length,ls:localStorage.getItem('course-page-exams2:'+D.title)!==null})")
    feat("every exam taken is kept in a My exams list with Review and Retake", hist["rows"] >= 1 and hist["rev"] >= 1 and hist["take"] >= 1 and hist["ls"], str(hist))
    pg.click("#xenew"); pg.wait_for_selector("#xefinish", timeout=180000); newcode = pg.input_value("#xecode")
    feat("New exam draws a different exam with a fresh code", newcode != "M-4711" and newcode.startswith("M-"), newcode)
    rp = ctx.new_page(); rp.goto("file://" + page_path); rp.wait_for_timeout(800); rp.evaluate("showTab('exam')"); rp.wait_for_timeout(800)
    kept = rp.evaluate("()=>document.querySelectorAll('#xehist tbody tr').length")
    rp.close()
    feat("the exam list survives a reload", kept >= 2, "%d exams kept" % kept)
    pg.locator("#xehist [data-xeact=review]").first.click(); pg.wait_for_selector("#xereport", timeout=120000); pg.wait_for_timeout(500)
    rv = pg.evaluate("()=>({msgs:document.querySelectorAll('#xeout .xfeed .xmsg').length,dis:[...document.querySelectorAll('#xeout fieldset[data-xi] input,#xeout fieldset[data-xi] textarea')].every(e=>e.disabled),fix:document.querySelectorAll('#xeout details.xfixd').length})")
    feat("Review shows the earlier attempt with its marks and corrections, locked", rv["msgs"] >= 10 and rv["dis"] and rv["fix"] >= 1, str(rv))
    pg.locator("#xehist [data-xeact=take]").first.click(); pg.wait_for_selector("#xefinish", timeout=180000)
    feat("Retake runs the same questions again", pg.locator("#xeout fieldset.xq").count() >= 10 and pg.input_value("#xecode").startswith("M-"))
    pg.evaluate("showTab('exam')"); pg.locator("#xehist [data-xedel]").first.click() if pg.locator("#xehist [data-xedel]").count() else None
    pg.once("dialog", lambda d: d.accept()); 
    if pg.locator("#xeclear").count():
        pg.click("#xeclear"); asked = pg.locator("#xeclearyes").count() == 1 and pg.locator("#xeclearzip").count() == 1 and pg.locator("#xehist tbody tr").count() > 0
        feat("the clear option asks first (and offers the audit zip) before it removes anything", asked)
        pg.click("#xeclearyes")
    pg.wait_for_timeout(300); feat("the exam list can be cleared", pg.locator("#xehist tbody tr").count() == 0)
    # ---- phones ----
    mctx2 = b.new_context(locale="en-US", viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True); mp = mctx2.new_page(); mp.goto("file://" + page_path); mp.wait_for_timeout(500)
    mp.evaluate("showTab('play')"); mp.wait_for_timeout(300)
    no_x = mp.evaluate("document.documentElement.scrollWidth<=innerWidth+1"); nav_vis = mp.locator("#navBack").is_visible() and mp.locator("#navTrail").is_visible(); tools = mp.locator(".edtools").first.is_visible()
    mp.evaluate("showTab('agents')"); mp.wait_for_timeout(300); split_hidden = mp.locator(".rsplit").is_hidden(); names_vis = mp.locator(".roster .persona .pn").first.is_visible(); no_x2 = mp.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
    feat("on a phone: Back/Forward and Places are visible, the editor tools wrap, the agent list has no splitter and keeps names, and the page does not scroll sideways", no_x and no_x2 and nav_vis and tools and split_hidden and names_vis)
    mctx2.close()
    # ---- WCAG over everything new ----
    pg.evaluate("showTab('play')"); pg.fill(ta, ""); pg.click(ta); pg.keyboard.type("prin"); pg.wait_for_timeout(150); pg.click('[data-pane="play"] [data-edact="help"]')
    axv3 = pg.evaluate("async()=>{const r=await axe.run({include:[['[data-pane=\"play\"]'],['#edac'],['header.top']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.nodes.length])}")
    pg.keyboard.press("Escape"); pg.click('[data-pane="play"] [data-edact="help"]'); pg.click("#navTrail"); axv4 = pg.evaluate("async()=>{const r=await axe.run({include:[['#navMenu']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.nodes.length])}"); pg.keyboard.press("Escape")
    view("agents"); axv5 = pg.evaluate("async()=>{const r=await axe.run({include:[['[data-pane=\"agents\"]']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.nodes.length])}")
    view("ontograph"); pg.wait_for_timeout(500); axv6 = pg.evaluate("async()=>{const r=await axe.run({include:[['[data-pane=\"ontograph\"]']]},{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.nodes.length])}")
    feat("WCAG 2 A/AA (axe-core) over the editor with its suggestions and help, the header trail and its menu, the agent list and the ontology tree", not (axv3 or axv4 or axv5 or axv6), str(axv3 + axv4 + axv5 + axv6)[:200])
    f9.close()
    R["gates"]["Stage4.C console errors"] = errors
    R["gates"]["Stage4.D dialogs"] = pg.locator('[role="dialog"],dialog').count()
    R["gates"]["Stage4.E sections"] = pg.locator("section[data-source]").count()
    m = ctx.new_page(); m.set_viewport_size({"width": 390, "height": 844}); m.goto("file://" + page_path)
    R["gates"]["Stage4.F top menu visible on mobile without clicks"] = m.locator("#groups button").first.is_visible()
    view("intro"); pg.add_script_tag(path=AXE)
    R["gates"]["WCAG 2 AA (axe-core)"] = pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.impact,v.nodes.length])}")
    # ---- 9.22.0: the owner's review of chapter 1 ----
    import zipfile as _zf, io as _io
    ix = pg.locator("a.idxlink")
    feat("a link 'All chapters' leads back to the index (index.html in the same folder)", ix.count() == 1 and ix.get_attribute("href") == "index.html" and ix.is_visible())
    feat("light theme only: the page carries no dark-mode rules", "prefers-color-scheme: dark" not in open(page_path, encoding="utf-8").read())
    ovs = {}
    for w in (320, 390, 768):
        ph = ctx.new_page(); ph.set_viewport_size({"width": w, "height": 800}); ph.goto("file://" + page_path); ph.wait_for_timeout(500)
        for gk in range(ph.locator("#groups button").count()):
            ph.locator("#groups button").nth(gk).click(); ph.wait_for_timeout(250)
            sw = ph.evaluate("document.documentElement.scrollWidth")
            if sw > w + 1: ovs["%d:%s" % (w, ph.locator("#groups button").nth(gk).text_content().strip())] = sw
        hdr_ok = ph.evaluate("()=>{const r=document.querySelector('.fsctl').getBoundingClientRect();return r.right<=innerWidth+1&&r.left>=0}") ; ovs["hdr%d" % w] = None if hdr_ok else "text-size buttons off screen"
        ph.close()
    ovs = {k: v for k, v in ovs.items() if v}
    feat("no sideways scroll at 320, 390 and 768 px in any top menu item, and the text-size buttons stay on screen", not ovs, str(ovs))
    view("exam"); pg.uncheck("#xetimeron"); pg.fill("#xesno", "20210001"); pg.fill("#xesname", "Test"); pg.fill("#xessur", "Student"); pg.fill("#xecode", "M-2024"); pg.click("#xestart"); pg.wait_for_selector("#xefinish", timeout=180000); finish_unlock()
    with pg.expect_download() as dl_: pg.click("#xeauditzip")
    zp = os.path.join(os.path.dirname(page_path), "_audit_test.zip"); dl_.value.save_as(zp); z = _zf.ZipFile(zp); names = z.namelist(); bad = z.testzip(); log = json.loads(z.read("audit_log.json")); evs = [e["event"] for e in log["events"]]; txt = z.read("audit_log.json").decode() + z.read("audit_log.csv").decode("utf-8")
    os.remove(zp)
    feat("the audit log downloads as a valid zip with README, JSON, CSV and the saved results; it records opened, started, finished and release, and holds no release code", bad is None and {"README.txt", "audit_log.json", "audit_log.csv"} <= set(names) and any(n.startswith("results/") for n in names) and {"page_opened", "exam_started", "exam_finished", "release_accepted"} <= set(evs) and "R1." not in txt, "%s; %s" % (names, evs[-6:]))
    b.close()
json.dump(R, open(os.environ.get("RESULTS", os.path.join(REPO, "08-tooling", "%s-page" % N, "test_results_v%s.json" % PV)), "w"), indent=1)
bad = [k for k, v in R["widgets"].items() if not v["passed"]]
print("widgets: %d tested, %d passed; failing: %s" % (len(R["widgets"]), len(R["widgets"]) - len(bad), [(k, R["widgets"][k]["detail"][:120]) for k in bad[:3]]))
for k, v in R["features"].items(): print("  [%s] %s  %s" % ("PASS" if v["passed"] else "FAIL", k, v["detail"][:150]))
for k, v in R["gates"].items(): print("  %-52s %s" % (k, v))
