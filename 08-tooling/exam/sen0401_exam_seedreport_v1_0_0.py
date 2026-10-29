#!/usr/bin/env python3
"""sen0401_exam_seedreport v1_0_0 - measured report on the interactive page questions as SEEDS for the exam (owner ruling of 2026-10-30). Written by the lineage agent; facts only, from files and git.
Sections: 1 what the bank is physically (files, pages, generators, first commit, sources, earlier exams); 2 per chapter 1-6: items, forms, levels, critical-point coverage (method stated below, two thresholds) with the uncovered points named by label;
3 aspects: the items' forms (stem patterns, stated) and the learning outcome clauses (verbatim from 01-outcomes) with no matching item, and what the seeds cannot give; 4 the page exam desk's question types against the paper types.
METHOD (stated, deterministic): a token is a lower-case [a-z0-9]+ word of at least 3 letters, minus a fixed stop list, with a final 's' removed. An item's text is its stem, its correct option, its explanation and its code. A critical point or an outcome clause is COVERED by an item when at least
THETA of its tokens occur in the item's text and at least MINTOK tokens do; strict THETA 0.5 and lenient 0.35 (MINTOK 3) for points; 0.4 and 2 for outcome clauses. This is a lexical proxy: it can miss a paraphrase and can credit a shared vocabulary; the fixture (--selftest) fixes what it must give on known data.
Usage: seedreport.py [--json FILE] | --selftest"""
import collections, glob, hashlib, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/"; HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
STOP = set("the and for that with this from are was were has have had not but can its into than then them they their there what which when where who why how does did will would should could may might must also only such each every any all one two more most other some very about over under between after before during because while still just like use used using said say".split())
LEVELS = {"Remember": 1, "Understand": 2, "Apply": 3, "Analyze": 4, "Evaluate": 5, "Create": 6}
def toks(s):
    out = set()
    for w in re.findall(r"[a-z0-9]+", s.lower()):
        if len(w) >= 3 and w not in STOP: out.add(w[:-1] if w.endswith("s") and len(w) > 3 else w)
    return out
def item_text(i): return " ".join([i["q"], i["options"][i["answer"]], i.get("why", ""), i.get("code") or ""])
def covered(ptoks, itoks, theta, mintok):
    n = len(ptoks & itoks); return len(ptoks) > 0 and n >= mintok and n / len(ptoks) >= theta
def coverage(points, items, theta, mintok=3):
    """points: [(label, text)], items: [item]; returns {label: number of items covering it}"""
    its = [toks(item_text(i)) for i in items]; return {l: sum(covered(toks(t), x, theta, mintok) for x in its) for l, t in points}
FORMS = collections.OrderedDict([
    ("program output or calculation", r"what does this program print|\bcompute|\bcalculat|how many|\bresult of\b|\b\d[\d,.]*\s*(?:bytes|satoshi|bits|%)"),
    ("reading a given transaction, block, address or script", r"this (?:transaction|block|address|script|output|input|header|message|response|sheet|file)|the following"),
    ("comparing options or designs", r"differ|compar|rather than|instead of|trade-?off|versus|\bbetter\b|advantage|which of these (?:is|are) (?:safer|more)"),
    ("security or failure reasoning", r"attack|attacker|risk|secur|steal|stolen|\blos[et]|vulnerab|threat|protect|defend|fail|compromis"),
    ("cause, reason or consequence", r"\bwhy\b|because|consequence|what happens|would happen|\bso that\b|\bleads? to\b|\bresults? in\b"),
    ("definition or naming", r"what is|what does .* (?:mean|stand)|called|\bdefine|the term")])
def forms(items):
    c = collections.Counter(); 
    for i in items:
        t = i["q"].lower() + " " + (i.get("code") or "").lower(); hit = [k for k, p in FORMS.items() if re.search(p, t)]
        for k in hit: c[k] += 1
        if not hit: c["none of these stem patterns"] += 1
    return dict(c)
def distinctive(points_by_ch, minlen=6):
    df = collections.defaultdict(set)
    for ch, pts in points_by_ch.items():
        for l, t in pts:
            for w in toks(t):
                if len(w) >= minlen: df[w].add(ch)
    return {ch: {w for w, s in df.items() if s == {ch}} for ch in points_by_ch}
def cross(items, ch, dist, need=3):
    n = 0
    for i in items:
        t = toks(item_text(i)); n += any(len(t & d) >= need for c, d in dist.items() if c != ch)
    return n
def clauses(stmt):
    out = []
    for part in re.split(r" - |; |—|, and |: ", stmt):
        part = part.strip(" .,")
        if len(part.split()) >= 3: out.append(part)
    return out
def latest(pat):
    fs = glob.glob(pat); return sorted(fs, key=lambda x: [int(v) for v in re.findall(r"_v(\d+)_(\d+)_(\d+)", x)[-1]])[-1] if fs else None
def git(*a): return subprocess.run(["git", "-C", R] + list(a), capture_output=True, text=True).stdout.strip()
def selftest():
    fx = json.load(open(HERE + "sen0401_exam_seedreport_fixture_v1_0_0.json")); got = {}
    items = fx["items"]; pts = [(p["label"], p["text"]) for p in fx["points"]]
    got["coverage_strict"] = coverage(pts, items, 0.5); got["coverage_lenient"] = coverage(pts, items, 0.35)
    got["forms"] = forms(items); d_ = distinctive({1: pts[:2], 2: pts[2:]}, 6); got["cross_need1"] = cross(items, 1, d_, 1); got["cross_need2"] = cross(items, 1, d_, 2)
    got["clauses"] = clauses(fx["outcome"]); ok = got == fx["expected"]
    print("SELFTEST", "PASS" if ok else "FAIL"); 
    if not ok: print(json.dumps(got, indent=1, sort_keys=True)); print(json.dumps(fx["expected"], indent=1, sort_keys=True))
    return ok
def main():
    rep = {"method_note": "see the module docstring", "chapters": {}}
    cp = json.load(open(HERE + "sen0401_exam_critical_points_v1_0_0.json")); A = cp["list_A_points_carried_by_a_source"]
    pb = {n: [(p["point"][:90], p["point"]) for p in A if p["chapter"] == n] for n in range(1, 7)}; dist = distinctive(pb, 6)
    outc = open(R + "01-outcomes/sen0401_outcomes_v1_1_1.ttl").read(); LO = {int(m.group(1)): (m.group(2), re.search(r"cme:bloomLevel ld:(\w+)", outc[m.end():m.end() + 900]).group(1)) for m in re.finditer(r'humanCodingScheme "LO-(\d+)" ; case:CFItemType sen0401:LearningOutcome ;\s*case:fullStatement "([^"]+)"', outc)}
    # section 1: physical
    sec1 = {}; legacy = [f for f in git("ls-files").splitlines() if re.search(r"(^|[_\-.])(exam|midterm|quiz)([_\-.]|$)", os.path.basename(f), re.I) and f.endswith((".json", ".md", ".html", ".pdf", ".docx", ".pptx", ".txt", ".csv")) and not f.startswith("08-tooling/exam/") and "briefs" not in f and "verify" not in f]
    for n in range(1, 8):
        bf = latest(R + "08-tooling/ch%02d-page/question_bank_v*.json" % n); pg = latest(R + "03-materials/ch%02d/page/sen0401_ch%02d_page_v*.html" % (n, n))
        bank = json.load(open(bf, encoding="utf8")); html = open(pg, encoding="utf8").read()
        m = re.search(r'<script[^>]*id="qbank"[^>]*>(.*?)</script>', html, re.S); emb = json.loads(m.group(1)) if m else []
        same = [(i["q"], i["options"]) for i in emb] == [(i["q"], i["options"]) for i in bank]
        rel = os.path.relpath(bf, R); gens = sorted(glob.glob(R + "08-tooling/sen0401_ch%02d_bank_gen_*.py" % n))
        first = git("log", "--follow", "--diff-filter=A", "--format=%h %ad %an | %s", "--date=short", "--", rel).splitlines()[-1:]
        gdoc = ""
        if gens:
            d = open(gens[-1]).read().split('"""')[1:2]; gdoc = re.sub(r"\s+", " ", d[0])[:420] if d else ""
        sec1[n] = {"bank_file": rel, "items": len(bank), "page_file": os.path.relpath(pg, R), "page_embeds_the_same_items": same, "generator_files": [os.path.relpath(g, R) for g in gens] or "none in 08-tooling writes this bank",
                   "first_commit": first[0] if first else "?", "generator_says": gdoc, "embedded_in_page_items": len(emb)}
    rep["section1_physical"] = {"per_chapter": sec1, "files_named exam/midterm/quiz/final outside the exam work (tracked)": legacy,
        "page_exam_desk": "each chapter page embeds the bank as JSON (script id qbank) and builds its own exam desk (xExamBuild) from the page's concept tree and the bank; the desk's kinds are listed in section 4"}
    # sections 2,3
    pageclass = {}
    for n in range(1, 7):
        bank = json.load(open(R + sec1[n]["bank_file"], encoding="utf8")); lev = collections.Counter(i["level"] for i in bank)
        quiz = json.load(open(R + "08-tooling/ch%02d-page/quiz_v1_0_0.json" % n, encoding="utf8"))["items"]
        qz = [{"q": x["q"], "options": x["options"], "answer": x["answer"], "why": " ".join(x.get("rationales", [])), "code": None} for x in quiz]; allseeds = bank + qz
        st = coverage(pb[n], allseeds, 0.5); le = coverage(pb[n], allseeds, 0.35)
        hist = collections.Counter(min(v, 4) for v in st.values()); un = [l for l, v in st.items() if v == 0]
        lo = LO.get(n); cl = clauses(lo[0]) if lo else []; its = [toks(item_text(i)) for i in bank]
        clr = []
        for c in cl:
            ct = toks(c); m_ = [j for j, x in enumerate(its) if covered(ct, x, 0.4, 2)]; clr.append({"clause": c, "matching_items": len(m_), "highest_level_among_them": max([LEVELS[bank[j]["level"]] for j in m_], default=0)})
        rep["chapters"][n] = {"items": len(bank), "four_option_single_answer": sum(len(i["options"]) == 4 for i in bank), "with_code": sum(bool(i.get("code")) for i in bank), "levels": dict(lev), "critical_points": len(pb[n]),
            "points_with_seed_strict": sum(v > 0 for v in st.values()), "points_with_seed_lenient": sum(v > 0 for v in le.values()), "points_by_seed_count_strict(0,1,2,3,4+)": [hist.get(k, 0) for k in range(5)],
            "uncovered_points_strict": un, "forms": forms(bank), "quiz_items_in_the_page": len(quiz), "seed_items_total(bank+quiz)": len(allseeds), "concepts_of_the_bank": len({i["concept"] for i in bank}), "concepts_shared_with_another_chapter": {m: len({i["concept"] for i in bank} & {j["concept"] for j in json.load(open(R + sec1[m]["bank_file"], encoding="utf8"))}) for m in range(1, 7) if m != n},
            "items_naming_3_or_more_tokens_distinctive_of_another_chapter(weak proxy)": cross(allseeds, n, dist, 3),
            "outcome": (lo[0], lo[1]) if lo else None, "outcome_clauses": clr}
    # section 4
    html = open(R + sec1[4]["page_file"], encoding="utf8").read()
    lab = dict(re.findall(r"(\w+):'([^']*)'", re.search(r"const XT_LABEL=\{([^}]*)\}", html).group(1))); mix = re.search(r"mix:\[(.*?)\]\}", html).group(1)
    mp = {"mcq": "ChoiceFour / ChoiceFourCode", "multi": "MultiSelect", "cloze": "FillBlank", "judge": "TrueFalse", "match": "Matching", "predict": "CodeTrace", "blank": "FillBlank (code)", "order": "Ordering", "repair": "none (run code)", "write": "WriteCode", "short": "ShortAnswer", "program": "WriteCode"}
    from rdflib import Graph, Namespace, RDF
    PR = Namespace("http://example.org/sen0401/paperrules#"); g = Graph().parse(HERE + "sen0401_exam_papertypes_v1_0_0.ttl"); stat = {str(t).split("#")[-1]: str(g.value(t, PR.status)).split("#")[-1] for t in g.subjects(RDF.type, PR.ItemType)}
    rep["section4_types"] = {"page_desk_kinds": {k: {"label": v, "paper_type": mp[k], "paper_status": stat.get(mp[k].split(" ")[0], "n/a")} for k, v in lab.items()}, "page_midterm_mix": mix, "kinds_present_in_the_banks": "four-option single-answer choice only (%d of %d items), %d with a code listing" % (sum(v["four_option_single_answer"] for v in rep["chapters"].values()), sum(v["items"] for v in rep["chapters"].values()), sum(v["with_code"] for v in rep["chapters"].values())),
        "paper_types_suited": [k for k, v in stat.items() if v == "Suited"], "paper_types_conditional": [k for k, v in stat.items() if v == "Conditional"]}
    print(json.dumps(rep, indent=1)); 
    if "--json" in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index("--json") + 1], "x"), indent=1)
if __name__ == "__main__":
    sys.exit(0 if selftest() else 1) if "--selftest" in sys.argv else main()
