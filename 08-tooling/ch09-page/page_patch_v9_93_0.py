#!/usr/bin/env python3
"""page_patch v9.93.0 (chapter 9) - makes the course page 9.93.0 from the released 9.92.0 (never edited) to the owner's rulings of 2026-11-24, as the chapter 8 page 9.91.0 stands:
 (1) no everyday analogy: the sentences 'It is like ...', 'Think of ...', 'It is as if ...' and the cheque sentence are removed from the concept texts, and the embedded document ontology is the new version 1.0.2 of the same text;
 (2) no lambda: the five worked examples that used one are written with comprehensions and dictionaries; their result, syntax tree and steps are recomputed by the page-data runner (sen0401_page_data_v2_24_0.EXEC) and the embedded
     domain ABox is the new version 1.0.2 with the same five codes;
 (3) the lecture (title, notes of 60 to 140 words, takeaway of every slide) and the chapter-code list are those of the deck 2.2.0 and chapter_code_ch09_v1_1_0.json (comment-led code, no prompts, no lambdas);
 (4) the top menu has the item '▶ Run slide code' (the chapter code pane left the Learn sub-menu), as in the chapter 8 page 9.91.0.
New files: 03-materials/ch09/rdodi/sen0401_ch09_document_v1_0_2.ttl, sen0401_ch09_domain_abox_v1_0_2.ttl, 03-materials/ch09/page/sen0401_ch09_page_v9_93_0.html, 08-tooling/ch09-page/page_data_v9_93_0.json. Nothing released is edited.
Usage: python3 page_patch_v9_93_0.py"""
__version__ = "9.93.0"
import hashlib, importlib.util, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
M9 = os.path.join(ROOT, "03-materials", "ch09")
OLD = os.path.join(M9, "page", "sen0401_ch09_page_v9_92_0.html"); NEW = os.path.join(M9, "page", "sen0401_ch09_page_v9_93_0.html")
TODAY = "2026-11-24"
START = re.compile(r"(?:(?<=[.!?] )|^)(It is like |Think of |It is as if |A cheque works in the same way)[^.!?]*(?:[.!?]|$) ?")
MID = "; it is like quoting a price from the catalogue and not from the till."


def clean(t):
    t = START.sub("", t).replace(MID, ".")
    return t.strip()


LAMBDA = {   # node id -> code without a lambda (single line, statements then the closing expression, as the page-data runner takes it)
 "DustThreshold": "d = R2['dust']; names = ('p2wpkh_293', 'p2wpkh_294', 'p2wsh_329', 'p2wsh_330', 'p2a_239', 'p2a_240'); ((31 + 67) * 3, (43 + 67) * 3, (13 + 67) * 3, [d[k]['result']['allowed'] for k in names], L.has('bolt03_transactions.md', 'pay to anchor (p2a): 240 satoshis'))",
 "EstimateSmartFeeCall": "E = R['estimate']['results']; keys = ('2_default', '6_default', '25_default'); (R['estimate_fresh']['ok']['errors'][0], R['estimate']['rounds'], R['estimate']['sent'], [round(E[k]['ok']['feerate'] * 10 ** 8 / 1000, 3) for k in keys])",
 "ChildBeatsHighRateTransaction": "a = R['ancestor_mining']['cpfp_wins']; b = a['block_txids']; ids = {k: a[k]['txid'] for k in ('P', 'C', 'A')}; (ids['P'] in b, ids['C'] in b, ids['A'] in b, b.index(ids['P']) < b.index(ids['C']), a['block_weight'])",
 "LowFeeChildLoses": "a = R['ancestor_mining']['cpfp_loses']; b = a['block_txids']; ids = {k: a[k]['txid'] for k in ('A', 'P', 'C')}; (round((a['fees_sat']['P'] + a['fees_sat']['C']) / (a['mempoolentries']['P']['chunkweight'] / 4), 2), ids['A'] in b, ids['P'] in b, ids['C'] in b)",
 "TrucLimits": "t = R['truc']; names = ('TRUC_VERSION', 'TRUC_ANCESTOR_LIMIT', 'TRUC_MAX_VSIZE', 'TRUC_CHILD_MAX_VSIZE'); (*[L.const('core_src_policy_truc_policy.h', n) for n in names], t['big_child']['vsize'], 'TRUC-violation' in L.reason(t['big_child']['result']), t['child1']['vsize'], 'ok' in t['child1']['result'])",
}
PRE = "import sys; sys.path.insert(0, '08-tooling'); import sen0401_ch09_lib_v1_0_1 as L; R = L.run(); R2 = L.run2(); C = L.census(); "


def exec_runner():
    src = open(os.path.join(TOOL, "sen0401_page_data_v2_24_0.py"), encoding="utf-8").read()
    return re.search(r"EXEC = r'''(.*?)'''", src, re.S).group(1)


def run_expr(expr):
    r = subprocess.run(["python3.14", "-c", exec_runner(), expr, PRE], capture_output=True, text=True, timeout=240, cwd=ROOT)
    if r.returncode: raise SystemExit("REFUSED: runner failed: " + r.stderr[-600:])
    return json.loads(r.stdout.strip().splitlines()[-1])


def new_ttl(kind, old_name, new_name, fn):
    src = open(os.path.join(M9, "rdodi", old_name), encoding="utf-8").read()
    src = fn(src)
    for a, b in (('owl:versionInfo "1.0.1"', 'owl:versionInfo "1.0.2"'), ("/%s/1.0.1>" % kind, "/%s/1.0.2>" % kind), ('dcterms:modified "2026-10-15"', 'dcterms:modified "%s"' % TODAY),
                 ("sen0401_ch09_%s_v1_0_1" % ("abox" if kind == "abox" else "document"), "sen0401_ch09_%s_v1_0_2" % ("abox" if kind == "abox" else "document"))):
        assert a in src, a
        src = src.replace(a, b, 1)
    open(os.path.join(M9, "rdodi", new_name), "w", encoding="utf-8").write(src)
    return src


def main():
    h = open(OLD, encoding="utf-8").read()
    i = re.search(r'<script type="application/json" id="data">', h).end(); j = h.index("</script>", i)
    D = json.loads(h[i:j])
    assert json.dumps(D, ensure_ascii=False).replace("</", "<\\/") == h[i:j]
    # (1) analogies
    nb = 0
    for n in D["nodes"]:
        c = clean(n["body"])
        if c != n["body"]: nb += 1
        n["body"] = c
    # (2) lambdas
    old_codes = {}
    for n in D["nodes"]:
        if n["id"] in LAMBDA:
            io = n["io"]; old_codes[n["id"]] = io["code"]; old_out = io["out"]
            r = run_expr(LAMBDA[n["id"]])
            if r["out"] != old_out: raise SystemExit("REFUSED: %s result changed: %r vs %r" % (n["id"], r["out"], old_out))
            n["io"] = {"code": LAMBDA[n["id"]], "out": r["out"], "tree": r["tree"], "steps": r.get("steps", [])}
    # (3) lecture and chapter code
    plan = json.load(open(os.path.join(TOOL, "ch09-deck", "deck_plan_v2_2_0.json")))["slides"]
    assert len(plan) == len(D["lecture"])
    for l, s in zip(D["lecture"], plan):
        assert l["n"] == D["lecture"].index(l) + 1
        l["title"] = s["title"]; l["say"] = s["notes"]
        if s.get("take"): l["takeaway"] = s["take"]
    man = json.load(open(os.path.join(M9, "page", "chapter_code_ch09_v1_1_0.json")))
    D["chaptercode"] = {"file": "03-materials/ch09/page/chapter_code_ch09_v1_1_0.json", "version": "1.1.0",
                        "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in man["examples"]]}
    D["_version"] = "9.93.0"
    # the ontologies embedded in the page
    def doc_fn(src):
        return re.sub(r'skos:definition "((?:[^"\\]|\\.)*)"', lambda m: 'skos:definition "%s"' % clean(m.group(1)), src)
    def abox_fn(src):
        for nid, code in LAMBDA.items():
            old = old_codes[nid]; assert src.count(old) == 2, (nid, src.count(old))
            src = src.replace(old, code)
        return src
    doc = new_ttl("document", "sen0401_ch09_document_v1_0_1.ttl", "sen0401_ch09_document_v1_0_2.ttl", doc_fn)
    abx = new_ttl("abox", "sen0401_ch09_domain_abox_v1_0_1.ttl", "sen0401_ch09_domain_abox_v1_0_2.ttl", abox_fn)
    body = json.dumps(D, ensure_ascii=False).replace("</", "<\\/")
    out = h[:i] + body + h[j:]
    for old_name, new_name, txt in (("sen0401_ch09_document_v1_0_1.ttl", "sen0401_ch09_document_v1_0_2.ttl", doc), ("sen0401_ch09_domain_abox_v1_0_1.ttl", "sen0401_ch09_domain_abox_v1_0_2.ttl", abx)):
        m = re.search(r'<script type="text/turtle" data-kind="chapter" data-name="%s" data-sha256="(\w+)">' % re.escape(old_name), out)
        e = out.index("</script>", m.end())
        sha = hashlib.sha256(txt.encode()).hexdigest()[:16]
        out = out[:m.start()] + '<script type="text/turtle" data-kind="chapter" data-name="%s" data-sha256="%s">' % (new_name, sha) + txt + out[e:]
    # the course-level register embedded in the page (released, unedited as a file) describes the chapter 1 deck with an analogy; the embedded copy leaves that clause out, as the chapter 8 page 9.91.0 does (the digest in the tag stays that of the file)
    a = ", a key-analogy slide maps house and car keys onto bitcoin keys"; assert out.count(a) == 1; out = out.replace(a, "")
    # (4) the menu
    a = "const VIEWS=[['learn','📚 Learn'],['maps','🗺 Maps']"; b = "const VIEWS=[['learn','📚 Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),['maps','🗺 Maps']"
    assert out.count(a) == 1; out = out.replace(a, b)
    a = "...(CC.length?[['chaptercode','💻 Chapter code']]:[]),...tops.map"; assert out.count(a) == 1; out = out.replace(a, "...tops.map")
    for a, b in (("lambda:'lambda  lambda x: …'", "lambda:'lambda  an unnamed one-line function'"),   # the page template's lambda hints, as the chapter 8 page 9.91.0 has them
                 ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
                 ('key=lambda x: len(x)', 'key=len')):
        assert out.count(a) >= 1, a; out = out.replace(a, b)
    a = '<meta name="version" content="9.92.0">'; assert out.count(a) == 1; out = out.replace(a, '<meta name="version" content="9.93.0">')
    open(NEW, "w", encoding="utf-8").write(out)
    json.dump(D, open(os.path.join(HERE, "page_data_v9_93_0.json"), "w"), ensure_ascii=False, indent=1)
    print("page written", NEW, len(out), "bytes; node texts cleaned:", nb, "; lambda nodes rewritten:", len(LAMBDA), "; lecture slides:", len(D["lecture"]), "; chapter code examples:", len(D["chaptercode"]["examples"]))


if __name__ == "__main__": main()
