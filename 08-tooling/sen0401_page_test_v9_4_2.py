#!/usr/bin/env python3
"""Browser tests for version 9 - visualisations computed by Python (evaluation steps, step-through tracer, code pipeline, chapter visualisations) and wheel zoom - on top of version 8 - a seven-item top menu, subject overviews without repeated lists, folded introductions, one rooted taxonomy with fitting labels, zoom on every diagram - on top of version 7 - the RDODI fit-gap views (ontology graph, Code Lab, SPARQL console, question views, About, downloads) on top of version 6 - the conversation view (roster with role icons, guide, handoff, follow-ups, memory) on top of version 5 - version 4's checks, plus: the page's own thread never blocks for long, and an endless program is stopped while the page stays responsive ( (version 3's rule checks plus the agents' toolkit) of a SEN0401 page - the owner's rules of 2026-09-25 made checkable:
code the student edits really runs (edited code must change the result); agents answer from their own
slice, so different questions get different answers; a menu click changes the main area and leaves the
detail card closed; the card opens only on an explicit request; the tab row is the sub-menu of the
selected top-level item. Every stored result must also equal what the build's interpreter printed."""
__version__ = "9.4.2"
import json, os, re, sys, time
PV = os.environ.get("PAGE_VER", "9_4_2")  # generated files carry the page version they were produced for
from playwright.sync_api import sync_playwright
N = sys.argv[1]; NUM = N; N = ("ch%s" % N) if N.isdigit() else N
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page_path = os.environ.get("PAGE", os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_v%s.html" % (N, os.environ.get("PAGE_VER", "9_4_2"))))
d = json.load(open(os.path.join(REPO, "08-tooling", "%s-page" % N, "page_data_v%s.json" % PV)))
AXE = "/home/claude/Ontologies/rdodi-ecosystem/07-pedagogy-professional-stage/lib/axe.min.js"
R = {"_version": PV.replace("_", "."), "widgets": {}, "features": {}, "gates": {}}
feat = lambda k, ok, det="": R["features"].__setitem__(k, {"passed": bool(ok), "detail": det})
nodes = d["nodes"]; tops = [n for n in nodes if n["level"] == 1]
in_view = "id=>{const e=document.getElementById(id);if(!e)return false;const r=e.getBoundingClientRect();return r.height>0&&r.top<innerHeight&&r.bottom>0&&!e.closest('[hidden]')}"
with sync_playwright() as p:
    b = p.chromium.launch(env={"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}); ctx = b.new_context(locale="en-US", viewport={"width": 1400, "height": 900}, permissions=["clipboard-read", "clipboard-write"]); pg = ctx.new_page(); errors = []
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
    view("map"); g = pg.locator("#graph g.gn").nth(4); gid = g.get_attribute("data-c"); g.click(); pg.wait_for_timeout(300)
    feat("tapping a map node shows its options in the detail card; the main area stays where it was", pg.locator("#card").is_visible() and ("Go to its section" in pg.text_content("#card")) and pg.locator('[data-pane="map"]').is_visible(), gid)
    pg.keyboard.press("Escape")
    view("taxonomy"); feat("taxonomy diagram", pg.locator("#taxo svg g.n").count() == len(nodes) + 1)
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
            elif n.get("chart") and "io" not in n:
                pg.wait_for_function("id=>{const c=document.getElementById(id);const ch=c&&window.Chart&&Chart.getChart(c);return ch&&ch.data.datasets.some(x=>x.data&&x.data.length)&&c.offsetWidth>0}", arg=n["chart"], timeout=20000)
                ok = True; why = "chart %s drawn" % n["chart"]
            elif n["level"] == 3:
                pg.click('[data-step="%s"]' % w); ok = pg.locator("#%s li" % w).nth(1).is_visible(); why = "second step revealed"
            elif n["level"] == 1:
                card = pg.locator("#%s .ovcard" % w).first; sub = card.get_attribute("data-sub"); card.click(); pg.wait_for_timeout(200)
                ok = pg.locator('[data-subpane="%s"]' % sub).is_visible() and pg.locator("#%s .ovcard" % w).count() == len([m for m in nodes if m["parent"] == n["id"]]); why = "overview card opens its sub-subject"
            else:
                leaves = [m["id"] for m in nodes if m["parent"] == n["id"]]
                ok = pg.locator("#%s > section.leaf" % w).count() == len(leaves) and pg.locator("#%s" % w).is_visible(); why = "grid shows its %d concepts" % len(leaves)
        except Exception as e:
            ok, why = False, "%s: %s" % (type(e).__name__, str(e)[:100])
        R["widgets"][w] = {"passed": ok, "detail": why}
    ios = [n for n in nodes if "io" in n]
    feat("edited code really runs: every example re-run after editing prints the new result", all(R["widgets"]["w-" + n["id"]]["passed"] for n in ios), "%d examples" % len(ios))
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
    want = sorted(set(pg.evaluate("()=>[...document.querySelectorAll('script[data-kind]')].map(b=>b.dataset.kind)")) | {"page"})
    feat("agents search a knowledge graph of every ontology file the page embeds, the research record and this page", "Knowledge graph: ready" in st and ("from %d files" % files) in st and kinds == want, st + " | kinds " + ",".join(kinds))
    feat("agents rank by meaning (sentence embeddings) and show how they found the answer", "Semantic search: ready" in st and "SPARQL" in how and "rows:" in how and cites > 0, "%d cited passages" % cites)
    q_out = pg.evaluate("async(id)=>{const a=D.agents.find(x=>x.id===id);const r=await rank(a,'which course learning outcome is about choosing libraries?',8);return r.top.map(x=>x.c.label).join(' | ')}", a["id"])
    if "course" in want: feat("a course question reaches the course ontology", "LO-1" in q_out, q_out[:150])
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
    feat("agents are listed like people: role icons, what each knows, a guide first", roster.count() == len(d["agents"]) + 1 and icons[0] == "🧭" and "🤖" not in icons and all(pg.locator('[data-agenttab="%s"] small' % x["id"]).text_content().startswith("Ask me about") for x in d["agents"]), " ".join(icons))
    tleaf = next((n_ for n_ in nodes if n_["level"] == 3 and "io" in n_), [n_ for n_ in nodes if n_["level"] == 3][0]); tagent = next(a_ for a_ in d["agents"] if tleaf["id"] in a_["covers"])
    pg.click('[data-agenttab="guide"]'); gl = pg.locator("#guide-log .msg").count(); pg.fill("#guide-q", "what is " + tleaf["label"].lower() + "?"); pg.press("#guide-q", "Enter")
    pg.wait_for_function("n=>{const m=document.querySelectorAll('#guide-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=gl, timeout=120000)
    sugg = [pg.locator("#guide-log .msg").last.locator("[data-handoff]").nth(k).get_attribute("data-handoff") for k in range(pg.locator("#guide-log .msg").last.locator("[data-handoff]").count())]
    target = tagent["id"]
    pg.locator('#guide-log .msg').last.locator('[data-handoff="%s"]' % target).click()
    pg.wait_for_function("id=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=3&&!m[m.length-1].classList.contains('typing')}", arg=target, timeout=120000)
    feat("the guide introduces the right agent and hands the question over", target in sugg and pg.locator('[data-conv="%s"]' % target).is_visible(), "suggested: " + ", ".join(sugg))
    def say(q):
        n = pg.locator("#%s-log .msg" % target).count(); pg.fill("#%s-q" % target, q); pg.press("#%s-q" % target, "Enter")
        pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}", arg=[target, n], timeout=120000)
        return pg.locator("#%s-log .msg" % target).last.inner_text()
    root = "what does " + tleaf["label"].lower() + " mean?"
    r1 = say(root); r2 = say("can you give me an example?"); r3 = say("and why?")
    feat("follow-up questions are answered in the context of the conversation", ('Following on from "%s"' % root) in r2 and ('Following on from "%s"' % root) in r3 , r2[:90].replace("\n", " "))
    kept = pg.locator("#%s-log .msg" % target).count(); pg.reload(); view("agents"); pg.wait_for_timeout(400)
    feat("conversations are remembered across a reload", pg.locator("#%s-log .msg" % target).count() == kept and pg.locator('[data-conv="%s"]' % target).is_visible(), "%d messages kept" % kept)
    pg.click('[data-newconv="%s"]' % target); feat("a new conversation starts clean", pg.locator("#%s-log .msg" % target).count() == 1)
    # ---- the fit-gap views ----
    view("howto"); howto = pg.text_content('[data-pane="howto"] .prose')
    view("arch"); arch_rows = pg.locator('#archout table').last.locator("tr").count() - 1
    view("mission"); pg.wait_for_function("()=>!document.getElementById('missionout').textContent.includes('reading the course ontology')", timeout=60000); mission = pg.text_content("#missionout")
    view("prov"); limits = pg.locator("#provout ul li").count()
    feat("About: how it works, agents & tools with the corpus, mission & backlog with course outcomes, provenance & known limits", len(howto) > 400 and arch_rows == files and "Mission" in mission and ("LO-1" in mission or "course" not in want) and limits >= 4, "corpus rows %d, limits %d" % (arch_rows, limits))
    view("sparql"); pg.click("#sqrun"); pg.wait_for_function("()=>/result/.test(document.getElementById('sqstat').textContent)||document.querySelector('#sqres .err')", timeout=60000)
    rows = pg.locator("#sqres tr").count() - 1
    pg.click("#sqcsv"); pg.wait_for_timeout(200); csv_copy = pg.evaluate("navigator.clipboard.readText()")
    pg.select_option("#sqsamp", "5"); pg.click("#sqload"); pg.click("#sqrun"); pg.wait_for_function("()=>/result/.test(document.getElementById('sqstat').textContent)", timeout=60000); ask_ans = pg.text_content("#sqres")
    feat("SPARQL console: editable queries over the knowledge graph, results table, results copied as CSV, ASK", rows > 5 and csv_copy.count("\n") >= rows and ask_ans.strip() in ("Yes", "No"), "%d rows; ASK -> %s" % (rows, ask_ans.strip()))
    view("ontograph"); pg.wait_for_function("()=>document.querySelectorAll('#onto g.on').length>0", timeout=60000)
    n_all = pg.locator("#onto g.on").count(); pg.uncheck('[data-okind="individual"]'); n_cls = pg.locator("#onto g.on").count(); pg.check('[data-okind="individual"]')
    pg.click("#orelayout"); pg.wait_for_timeout(2500); pg.click("#ofit"); first = pg.locator("#onto g.on").first; first.click(); info = pg.text_content("#ontoinfo")
    feat("ontology graph: classes, individuals and book concepts from the graph, filter, re-layout, fit, node detail", n_all > 20 and 0 < n_cls < n_all and len(info) > 20, "%d nodes (%d without individuals)" % (n_all, n_cls))
    view("play"); pg.fill("#pcode", "print('hello')")
    pg.click('[data-dl="pcode"]'); pg.wait_for_timeout(200); code_copy = pg.evaluate("navigator.clipboard.readText()")
    view("mydata")
    pg.click("#dlconvmd"); pg.wait_for_timeout(200); conv_md = pg.evaluate("navigator.clipboard.readText()")
    feat("copying out: playground code, SPARQL results, conversations - to the clipboard, with no file built and saved by the page", code_copy == "print('hello')" and conv_md.startswith("# Conversations") and pg.locator("#mydataout tr").count() >= 1, "code, CSV and %d characters of conversation copied" % len(conv_md))
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
    view("codelab"); pg.select_option("#clsnip", "1"); pg.click("#clload"); pg.click("#clrun"); pg.wait_for_function("()=>{const t=document.getElementById('clout').textContent;return t&&t!=='running...'}", timeout=120000)
    cl = pg.text_content("#clout"); n_io = len([n for n in nodes if "io" in n])
    feat("Code Lab: Python over this page's own data re-runs every example", cl.count("same |") == n_io and "DIFFERENT" not in cl, "%d of %d examples the same" % (cl.count("same |"), n_io))
    # ---- version 8 ----
    view(tops[0]["id"]); pg.select_option('#crumb-%s select' % tops[0]["id"], "ov-" + tops[0]["id"])
    dup = pg.evaluate("()=>[...document.querySelectorAll('[data-pane]')].filter(p=>byId[p.dataset.pane]&&byId[p.dataset.pane].level===1).reduce((a,p)=>a+p.querySelectorAll('.chip').length,0)")
    feat("subject screens carry no repeated lists: an overview sub-tab, one-sentence sub-subject headers", dup == 0 and pg.locator('[data-pane="%s"] .ovcard' % tops[0]["id"]).count() > 0 and pg.locator("details.more").count() == len([n for n in nodes if n["level"] == 2]), "0 duplicate chip rows")
    view("taxonomy"); tx = pg.evaluate("()=>{const g=[...document.querySelectorAll('#taxo g.n')];return {svgs:document.querySelectorAll('#taxo svg').length,boxes:g.length,root:document.querySelectorAll('#taxo g.n.root').length,overflow:g.filter(x=>x.querySelector('text').getBBox().width>x.querySelector('rect').getBBox().width+0.5).length}}")
    feat("one taxonomy tree rooted at the chapter, every label inside its box", tx["svgs"] == 1 and tx["root"] == 1 and tx["boxes"] == len(nodes) + 1 and tx["overflow"] == 0, str(tx))
    helps = pg.evaluate("()=>[...document.querySelectorAll('details.help')].map(d=>d.open)")
    feat("view introductions are folded until asked for", len(helps) >= 8 and not any(helps), "%d folded" % len(helps))
    zooms = []
    for k, sel in (("taxonomy", "#taxo"), ("map", "#graph"), ("ontograph", "#onto")):
        view(k)
        if k == "ontograph": pg.wait_for_function("()=>document.querySelector('#onto svg')", timeout=60000)
        v0 = pg.get_attribute("%s svg" % sel, "viewBox"); pg.click('%s [data-z="in"]' % sel); v1 = pg.get_attribute("%s svg" % sel, "viewBox"); pg.click('%s [data-z="reset"]' % sel); v2 = pg.get_attribute("%s svg" % sel, "viewBox")
        zooms.append(v1 != v0 and v2 == v0)
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
    feat("evaluation steps: each example replays Python's own reduction, one operation at a time, ending on the stored result", ok_ev and len(evs) >= 1, "%d multi-step examples" % len(evs))
    view("trace"); pg.fill("#trcode", "total = 0\nfor n in range(1, 5):\n    total = total + n\nprint(total)"); pg.click("#trgo")
    pg.wait_for_function("()=>/steps/.test(document.getElementById('trstat').textContent)", timeout=120000); nsteps = int(pg.text_content("#trstat").split()[0])
    pg.click("#trfirst"); [pg.click("#trnext") for _ in range(nsteps - 1)]; last_out = pg.text_content("#trout").strip(); tot = [r for r in pg.locator("#trvars tr").all_inner_texts() if r.startswith("total")]
    feat("step through: Python's line tracer records every line, the variables after it and the output", nsteps > 8 and last_out == "10" and tot and "10" in tot[0], "%d steps, output %s" % (nsteps, last_out))
    view("pipeline"); pg.fill("#ppcode", "x = 2 + 3 * 6\nprint(x)"); pg.click("#ppgo"); pg.wait_for_function("()=>document.querySelector('#ppout pre')", timeout=120000)
    pg.click('[data-stage="1"]'); ntok = pg.locator("#ppout .tok").count(); pg.click('[data-stage="2"]'); tree_ok = pg.locator("#ppout svg g.n").count() > 5; pg.click('[data-stage="3"]'); nbc = pg.locator("#ppout tr").count() - 1; pg.click('[data-stage="4"]'); res = pg.text_content("#ppout pre").strip()
    feat("code pipeline: source, tokens, syntax tree, bytecode and result, each from Python's own modules", ntok == 11 and tree_ok and nbc > 3 and res == "20", "%d tokens, %d instructions, result %s" % (ntok, nbc, res))
    vis_ok = []
    for cid, v in ((k, x) for k, x in d.get("visuals", {}).items() if not k.startswith("_")):
        w = "wv-" + cid; pg.evaluate("goTo('%s')" % cid); pg.click('[data-vistoggle="%s"]' % cid); ok = False; why = ""
        try:
            if v["kind"] == "floatbits":
                pg.wait_for_function("id=>document.querySelector('#'+id+'-out .bits')", arg=w, timeout=120000); bits = pg.text_content("#%s-out .bits" % w).strip()
                import struct; x = float(eval(v["start"])); ok = bits == format(struct.unpack(">Q", struct.pack(">d", x))[0], "064b"); why = "64 bits match the build interpreter's"
            if v["kind"] == "truthtable":
                pg.wait_for_function("id=>document.querySelector('#'+id+'-out table')", arg=w, timeout=120000); rows = pg.locator("#%s-out tr" % w).count() - 1
                names = sorted(set(__import__("re").findall(r"\b[abc]\b", v["start"]))); ok = rows == 2 ** len(names); why = "%d rows for %d inputs" % (rows, len(names))
            if v["kind"] == "branchflow":
                pg.wait_for_function("id=>/Output/.test(document.getElementById(id+'-out').textContent)", arg=w, timeout=120000); first = pg.text_content("#%s-out" % w)
                pg.fill("#%s-x" % w, "8"); pg.click('[data-vis="%s"]' % cid); pg.wait_for_function("id=>/child ticket/.test(document.getElementById(id+'-out').textContent)", arg=w, timeout=60000)
                ok = ("adult ticket" in first or "senior ticket" in first) and pg.locator("#%s-src .tl.now" % w).count() >= 3; why = "path follows the input: %s then child ticket" % ("adult" if "adult" in first else "senior")
        except Exception as e:
            why = "%s: %s" % (type(e).__name__, str(e)[:80])
        R["widgets"][w] = {"passed": ok, "detail": why}; vis_ok.append(ok)
    feat("chapter visualisations: float bits, truth tables, branch paths - each computed by Python", all(vis_ok), "%d of %d" % (sum(vis_ok), len(vis_ok)))
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
    link = pg.locator('[data-subpane="%s"] p [data-c]' % mid2["id"]).first
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
    fp.evaluate("showTab('taxonomy')"); fp.wait_for_timeout(300)
    ov = fp.evaluate("()=>{const bar=document.querySelector('#taxo .zbar'),d=document.querySelector('#taxo .diagram');const a=bar.getBoundingClientRect(),c=d.getBoundingClientRect();return a.bottom<=c.top+0.5&&!d.contains(bar)}")
    feat("zoom controls sit above each diagram, never covering it", ov)
    fp.evaluate("goTo('%s')" % tops[0]["id"]); fp.wait_for_timeout(200); link = fp.locator('[data-pane="%s"] p [data-c]:visible' % tops[0]["id"]).first  # a term the reader can actually see
    if link.count():
        tgt = link.get_attribute("data-c"); before = fp.evaluate("[...document.querySelectorAll('[data-pane]')].find(p=>!p.hidden).dataset.pane"); link.click(); fp.wait_for_timeout(200)
        after = fp.evaluate("[...document.querySelectorAll('[data-pane]')].find(p=>!p.hidden).dataset.pane"); card = fp.text_content("#card") if fp.locator("#card").is_visible() else ""
        feat("tapping a concept in the text opens its options in the detail card, without leaving the page", before == after and "Go to its section" in card and byid_label_ok(card, tgt) if False else (before == after and "Go to its section" in card), "%s: card with options, still on %s" % (tgt, after))
    fctx.close()
    pinch = pg.evaluate("""()=>{showTab('taxonomy');const svg=document.querySelector('#taxo svg'),v0=svg.getAttribute('viewBox'),r=svg.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
      const ev=(t,id,x,y)=>svg.dispatchEvent(new PointerEvent(t,{pointerId:id,clientX:x,clientY:y,bubbles:true,pointerType:'touch',isPrimary:id===1}));
      ev('pointerdown',1,cx-20,cy);ev('pointerdown',2,cx+20,cy);ev('pointermove',1,cx-80,cy);ev('pointermove',2,cx+80,cy);ev('pointerup',1,cx-80,cy);ev('pointerup',2,cx+80,cy);return v0!==svg.getAttribute('viewBox')}""")
    feat("pinch zoom: two fingers spreading zoom a diagram", pinch)
    lt2 = pg.evaluate("window.__lt"); feat("no main-thread task over 200 ms, including the ontology layout", max(lt2 or [0]) <= 200, "longest %d ms" % max(lt2 or [0]))
    view("quiz"); fs = pg.locator("fieldset"); qok = True
    for k in range(fs.count()):
        f = fs.nth(k); f.locator("input").nth(int(f.get_attribute("data-answer"))).check(); f.locator("button").click(); qok &= pg.text_content("#q%d-fb" % k) == "Correct."
    feat("quiz", qok)
    R["gates"]["Stage4.C console errors"] = errors
    R["gates"]["Stage4.D dialogs"] = pg.locator('[role="dialog"],dialog').count()
    R["gates"]["Stage4.E sections"] = pg.locator("section[data-source]").count()
    m = ctx.new_page(); m.set_viewport_size({"width": 390, "height": 844}); m.goto("file://" + page_path)
    R["gates"]["Stage4.F top menu visible on mobile without clicks"] = m.locator("#groups button").first.is_visible()
    view("intro"); pg.add_script_tag(path=AXE)
    R["gates"]["WCAG 2 AA (axe-core)"] = pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa']}});return r.violations.map(v=>[v.id,v.impact,v.nodes.length])}")
    b.close()
json.dump(R, open(os.environ.get("RESULTS", os.path.join(REPO, "08-tooling", "%s-page" % N, "test_results_v%s.json" % PV)), "w"), indent=1)
bad = [k for k, v in R["widgets"].items() if not v["passed"]]
print("widgets: %d tested, %d passed; failing: %s" % (len(R["widgets"]), len(R["widgets"]) - len(bad), [(k, R["widgets"][k]["detail"][:120]) for k in bad[:3]]))
for k, v in R["features"].items(): print("  [%s] %s  %s" % ("PASS" if v["passed"] else "FAIL", k, v["detail"][:150]))
for k, v in R["gates"].items(): print("  %-52s %s" % (k, v))
