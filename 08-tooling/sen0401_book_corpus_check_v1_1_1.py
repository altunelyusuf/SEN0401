#!/usr/bin/env python3
"""Verifies, in a real browser, that a built SEN0401 chapter page carries the ontology of its own book chapter and that
the page's agents and SPARQL console really answer from it. Written for the repair that added the book block; it answers
the one question neither the smoke test nor the full page test asks, because until now there was no book block to ask
about.

Six checks, nothing random and nothing waited on by guess:
  1 the page embeds exactly one Turtle block of kind "book"; its name is the book ontology of THIS chapter at the pinned
    commit; its declared sha256 is the hash of the bytes the pin really holds; and the block's own text is byte-identical
    to those bytes (the escape the build applies to "</script" is undone before comparing)
  2 the knowledge graph loads and reports its triple total and file count; the book graph's own triple count is read back
    with SPARQL and printed, so a before-and-after comparison is a measurement, not a recollection
  3 the SPARQL console answers a query restricted to the book graph with rows (the console's own store, the console's
    own query path)
  4 a question that can only be answered from the book ontology is answered by an agent from a book passage. The
    question is built, by SPARQL over the book graph alone, from an index term the book introduces with a sentence of
    the authors' own wording - a term chosen because neither the term nor that sentence occurs anywhere else in the
    page's corpus, so no other passage could answer it. The agent must cite at least one source labelled "Book", and
    the sentence it leads with must be found in the book graph and in nothing else
  5 the chapter's own natural question (the agent and question the chapter's test_config names) still answers, and the
    kinds of passage it was ranked over are reported
  6 the chapter taxonomy counts the book concepts it draws

usage: sen0401_book_corpus_check_v1_1_1.py NN        (PAGE_VER default 9_26_0; exit 1 on any FAIL)"""
__version__ = "1.1.1"
# 1.1.1 (PATCH over 1.1.0): the checkout the pinned bytes are re-read from is the book package's own repository,
#   altunelyusuf/mastering-bitcoin, not the Ontologies monorepo it used to sit in; the constant naming it is
#   renamed in the same change so the name says what it is. Check 1 is otherwise identical and is still the
#   check that proves the pin: it re-reads the bytes at the pin and compares the embedded block's name, its
#   sha256 and its text, so a repoint that is wrong fails here and nowhere quieter.
# 1.1.0 (over 1.0.0): check 4 builds its question from the book graph itself, by SPARQL - an index term whose
#   introducing sentence the book carries, and which occurs nowhere else in the corpus - instead of from the first
#   sentence of a book chunk's assembled text. Version 1.0.0 took that first sentence from a passage chunk whose text
#   begins with the passage's attribution literals, so for two chapters the "question" was a fragment of an author's
#   name and the check measured nothing about the book. The failure was real and is the reason for this version.
import glob, hashlib, json, os, re, ssl as _ssl, subprocess, sys, urllib.request as _ur
from playwright.sync_api import sync_playwright

NUM = sys.argv[1]; N = "ch%s" % NUM; PV = os.environ.get("PAGE_VER", "9_26_0")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_REPO = os.environ.get("SEN0401_BOOK_REPO", "/home/claude/mastering-bitcoin")  # 1.1.1: a checkout of altunelyusuf/mastering-bitcoin holding the pinned commit
page_path = os.environ.get("PAGE", os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_v%s.html" % (N, PV)))
P = os.path.join(REPO, "08-tooling", "%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v%s.json" % PV)))
C = d["course"]["corpus"]
_tc = sorted(glob.glob(os.path.join(P, "test_config_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
TC = json.load(open(_tc[-1])) if _tc else {"agent": d["agents"][0]["id"], "root": "what is this chapter about?"}

RES = []
def feat(name, ok, det=""):
    RES.append((name, bool(ok), str(det)[:400])); print("  [%s] %s  %s" % ("PASS" if ok else "FAIL", name, str(det)[:300]), flush=True)

# ---- 1  the embedded book block against the bytes the pin holds -----------------------------------------------------
html = open(page_path, encoding="utf-8").read()
BLK = re.compile(r'<script type="text/turtle" data-kind="([a-z]+)" data-name="([^"]*)" data-sha256="([0-9a-f]+)">(.*?)</script>', re.S)
found = BLK.findall(html)
books = [b for b in found if b[0] == "book"]
entry = (C.get("book") or {}).get(str(int(NUM)))
want_path = (entry["path"] if isinstance(entry, dict) else entry) if entry else None
if want_path:
    pin = C.get("book_pin_commit")
    src = C.get("book_pin_source") or ""
    if src:
        pin = re.search(r'pinnedCommit "([0-9a-f]{40})"', open(os.path.join(REPO, src)).read()).group(1)
    raw = subprocess.run(["git", "-C", BOOK_REPO, "show", "%s:%s" % (pin, want_path)], capture_output=True, text=True).stdout
    want_name = os.path.basename(want_path) + "@" + pin[:8]
    want_sha = hashlib.sha256(raw.encode()).hexdigest()[:16]
    ok = len(books) == 1 and books[0][1] == want_name and books[0][2] == want_sha and books[0][3].replace("<\\/script", "</script") == raw
    feat("1 the page embeds the ontology of its own book chapter at the pinned commit, and its hash matches the pinned bytes",
         ok, "%d book blocks; want %s %s; got %s" % (len(books), want_name, want_sha, [(b[1], b[2]) for b in books]))
else:
    raw = ""
    feat("1 the page embeds the ontology of its own book chapter at the pinned commit, and its hash matches the pinned bytes",
         False, "the page data's corpus names no book ontology for chapter %s: corpus.book = %r" % (NUM, C.get("book")))

def _cdn_cached(route):   # the CDN files are kept on disk, shared with the smoke and full tests
    u = route.request.url; f = "/tmp/cdncache/" + hashlib.sha1(u.encode()).hexdigest()
    try:
        if not os.path.exists(f):
            os.makedirs("/tmp/cdncache", exist_ok=True)
            with _ur.urlopen(_ur.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=180,
                             context=_ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt") if os.path.exists("/root/.ccr/ca-bundle.crt") else None) as rr:
                data = rr.read(); ct = rr.headers.get("content-type", "application/octet-stream")
            open(f, "wb").write(data); open(f + ".ct", "w").write(ct)
        route.fulfill(status=200, body=open(f, "rb").read(), headers={"content-type": open(f + ".ct").read(), "access-control-allow-origin": "*"})
    except Exception:
        route.continue_()

NUMBERS = {}
with sync_playwright() as p:
    b = p.chromium.launch(env=dict(os.environ, LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8"),
                          **({"proxy": {"server": os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {}))
    ctx = b.new_context(locale="en-US", viewport={"width": 1400, "height": 900})
    ctx.route(re.compile(r"^https://cdn\.jsdelivr\.net/"), _cdn_cached)
    pg = ctx.new_page(); errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto("file://" + page_path); pg.wait_for_timeout(1200)
    GROUP = pg.evaluate("GROUP_OF")
    def view(k):
        g = GROUP.get(k)
        if g:
            view(g)
            if not pg.locator('[data-pane="%s"]' % k).is_visible(): pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="%s"]' % k)
        else: pg.click('#groups [data-tab="%s"]' % k)
        pg.wait_for_timeout(150)

    # ---- 2  the knowledge graph, and the book graph's own share of it -----------------------------------------------
    view("agents")
    pg.evaluate("async()=>{await ensureGraph()}")
    pg.wait_for_function("()=>document.querySelector('.kitstat').textContent.includes('Knowledge graph: ready')", timeout=180000)
    st = pg.text_content(".kitstat")
    per = pg.evaluate("async()=>await sparql('SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g')")
    total = int(re.search(r"ready, (\d+) triples", st).group(1)); files = int(re.search(r"from (\d+) files", st).group(1))
    bookrows = [r for r in per if ":book:" in r["g"]]
    bookn = sum(int(r["n"]) for r in bookrows)
    NUMBERS = {"triples_total": total, "corpus_files": files, "book_graph_triples": bookn,
               "per_graph": {r["g"].split("urn:corpus:")[-1]: int(r["n"]) for r in per}}
    feat("2 the knowledge graph loads; its triple total, file count and the book graph's own triples are measured",
         total > 0 and files == len(found), "%d triples from %d files (%d Turtle blocks in the file); book graph %d triples in %d graph(s)" % (total, files, len(found), bookn, len(bookrows)))

    # ---- 3  the SPARQL console over the book graph ------------------------------------------------------------------
    rows = pg.evaluate("async()=>await sparql('SELECT ?s ?p ?o WHERE { GRAPH ?g { ?s ?p ?o } FILTER(CONTAINS(STR(?g),\":book:\")) } LIMIT 5')")
    feat("3 the SPARQL console's own store answers a query restricted to the book graph", len(rows) > 0, "%d rows, first subject %s" % (len(rows), rows[0]["s"] if rows else "-"))

    # ---- 4  a question only the book can answer ---------------------------------------------------------------------
    pick = pg.evaluate("""async()=>{const ch=await ensureChunks();
      const kinds=[...new Set(ch.map(c=>c.kind))].sort();
      // the book's own index terms, each with the sentence of the authors' wording that introduces it, read from the
      // book graph alone - no other graph is consulted, so every candidate is the book's to answer
      const q='PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> SELECT ?term ?text WHERE { GRAPH ?g { ?c rdfs:label ?term ; ?ip ?p . ?p ?tp ?text . FILTER(STRENDS(STR(?ip),"introducedBy") && STRENDS(STR(?tp),"#text")) } FILTER(CONTAINS(STR(?g),":book:")) }';
      const rows=await sparql(q);
      const pageText=(D.nodes.map(n=>n.label+' '+n.body+' '+(n.paras||[]).map(p=>p.text).join(' ')).join(' ')
        +' '+ch.filter(c=>c.kind!=='book').map(c=>c.label+' '+c.text).join(' ')).toLowerCase();
      // keep a term the rest of the corpus never names, whose sentence the rest of the corpus never carries
      const cand=rows.filter(r=>r.term.length>5&&r.text.split(/\s+/).length>=10
        &&!pageText.includes(r.term.toLowerCase())
        &&!pageText.includes(r.text.toLowerCase().slice(0,50)));
      cand.sort((a,b)=>b.text.length-a.text.length);
      if(!cand.length)return {kinds,chunks:ch.length,none:true};
      const c=cand[0];
      const question='What does the book say about '+c.term+'?';
      const ag=(await routeScores(question)).find(x=>x.best>0)||(await routeScores(question))[0];
      return {kinds,chunks:ch.length,label:c.term,body:c.text,question,agent:ag?ag.a.id:null,agentName:ag?ag.a.name:null}}""")
    NUMBERS["chunks"] = pick.get("chunks"); NUMBERS["kinds"] = pick.get("kinds")
    if pick.get("none") or not pick.get("agent"):
        feat("4 a question only the book ontology can answer is answered from a book passage", False,
             "no book-only passage an agent would own; kinds present: %s" % ",".join(pick.get("kinds") or []))
        answer = ""
    else:
        aid = pick["agent"]; q = pick["question"]
        pg.click('[data-agenttab="%s"]' % aid)
        before = pg.locator("#%s-log .msg" % aid).count()
        pg.fill("#%s-q" % aid, q); pg.click('[data-ask="%s"]' % aid)
        pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}",
                             arg=[aid, before], timeout=300000)
        last = pg.locator("#%s-log .msg" % aid).last
        answer = last.inner_text()
        booksrc = last.locator(".src.book").count()
        srcs = [last.locator(".src").nth(k).text_content() for k in range(last.locator(".src").count())]
        lead = last.locator(".lead").first.text_content() if last.locator(".lead").count() else ""
        where = pg.evaluate("""async(lead)=>{const t=lead.replace(/\\s*\\[\\d+\\]\\s*$/,'').trim().toLowerCase();const ch=await ensureChunks();
          return {inBook:ch.some(c=>c.kind==='book'&&c.text.toLowerCase().includes(t)),inOther:ch.some(c=>c.kind!=='book'&&c.text.toLowerCase().includes(t))}}""", lead)
        feat("4 a question only the book ontology can answer is answered from a book passage",
             booksrc > 0 and bool(lead) and where["inBook"] and not where["inOther"],
             "%s asked %r (the book's own sentence for it: %r); %d of %d cited sources are Book; lead sentence in book=%s, in anything else=%s" % (
                 pick["agentName"], q, pick["body"][:110], booksrc, len(srcs), where["inBook"], where["inOther"]))
        NUMBERS["book_probe"] = {"agent": pick["agentName"], "term": pick["label"], "book_sentence": pick["body"], "question": q, "lead": lead, "sources": srcs[:6]}

    # ---- 5  the chapter's own natural question ----------------------------------------------------------------------
    aid2 = TC["agent"]
    pg.click('[data-agenttab="%s"]' % aid2)
    n2 = pg.locator("#%s-log .msg" % aid2).count()
    pg.fill("#%s-q" % aid2, TC["root"]); pg.click('[data-ask="%s"]' % aid2)
    pg.wait_for_function("([id,n])=>{const m=document.querySelectorAll('#'+id+'-log .msg');return m.length>=n+2&&!m[m.length-1].classList.contains('typing')}",
                         arg=[aid2, n2], timeout=300000)
    l2 = pg.locator("#%s-log .msg" % aid2).last
    s2 = [l2.locator(".src").nth(k).text_content() for k in range(l2.locator(".src").count())]
    feat("5 the chapter's own question still answers, over a corpus that now includes the book",
         len(l2.inner_text()) > 60 and len(s2) > 0, "%r -> %s | kinds ranked: %s" % (TC["root"], l2.inner_text()[:90].replace("\n", " "), ",".join(pick.get("kinds") or [])))
    NUMBERS["chapter_question"] = {"agent": aid2, "question": TC["root"], "sources": s2[:6]}

    # ---- 6  the taxonomy's book layer ------------------------------------------------------------------------------
    view("taxonomy")
    pg.wait_for_function("()=>/book concepts/.test(document.getElementById('ostat').textContent)", timeout=180000)
    ostat = pg.text_content("#ostat")
    bc = int(re.search(r"(\d+) book concepts", ostat).group(1))
    NUMBERS["taxonomy_book_concepts"] = bc
    feat("6 the chapter taxonomy draws the book's concepts", bc > 0, ostat)

    feat("7 no console or page error through all of that", not errors, "errors=%s" % errors[:2])
    b.close()

out = os.path.join(P, "book_corpus_check_v%s.json" % PV)
json.dump({"_version": PV.replace("_", "."), "page": os.path.basename(page_path), "numbers": NUMBERS,
           "checks": [{"check": a, "passed": o, "detail": t} for a, o, t in RES]}, open(out, "w"), indent=1)
print("\n%d of %d checks pass; numbers: %s" % (sum(1 for _, o, _ in RES if o), len(RES),
      json.dumps({k: v for k, v in NUMBERS.items() if k in ("triples_total", "corpus_files", "book_graph_triples", "chunks", "kinds", "taxonomy_book_concepts")})))
print("wrote", out)
sys.exit(0 if all(o for _, o, _ in RES) else 1)
