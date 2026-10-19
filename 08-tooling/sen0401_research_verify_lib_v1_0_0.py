#!/usr/bin/env python3
"""Shared body of the research verify scripts of SEN0401 chapters 2, 3 and 4 (sen0401_ch02_verify, sen0401_ch03_verify, sen0401_ch04_verify).

Chapters 10-13 have a verify script that checks the research package's own consistency without a network and without a node, in six parts
(sources fetched and recorded; passages found in the saved copy; the stories; every class has a cited paragraph; the evidence record is complete;
findings and sources cite each other). Chapters 2-4 keep their research record in the RDODI Stage 1 file instead of a module and an index, so this
library carries the same six parts over to the newest committed research / TBox / ABox / document file of the chapter, with the same strictness
(a failure of any single item is a failure of the script). Nothing here needs rdflib: the Turtle files are written one statement per line by the
chapter generators and are read with the same literal-aware patterns for every chapter.

1 sources    every publication of the research file: verification status Verified, a verifiedAt time, a source URI, a role; every saved BIP copy of the
              chapter's source folder is the BIP its file name says; the owner's course-notes presentation named by a digest is the committed file whose
              full sha256 begins with that digest and agrees with the legacy inventory
2 passages   every saved text and JSON file of the chapter's source and evidence folders is non-empty and (JSON) parses; the chapter's own saved
              verify results, where it has them, are all positive
3 stories    the newest stories module of the chapter: its own run_checks() returns no failure; counts
4 classes    every class of the TBox has a section of the document, every section of the document cites (Author, Year), and every citation is a label
              of a publication of the research file (Stage 3.F in its own form, checked again here independently of the validator)
5 abox       every IO individual of the ABox has input and output, the input is a valid one-line expression, the count equals the number of leaf concepts that carry an example, and EVERY input is executed under the running interpreter
              (working directory: the repository root) and must give exactly its recorded output
6 findings   every finding cites at least one publication, cites only publications of the research file, and every publication is cited by a finding,
              is the source of a concept, or is cited by (Author, Year) in a paragraph of the document
Exit 0 and 'failures: []' when all hold."""
__version__ = "1.0.0"
import ast, glob, hashlib, importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LIT = r'"((?:[^"\\]|\\.)*)"'
CITE = re.compile(r"\(([A-Z][A-Za-z\.' ]+(?: et al\.)?, \d{4})\)")


def newest(pattern):
    fs = glob.glob(pattern)
    key = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]
    return sorted(fs, key=key)[-1] if fs else None


def unesc(s):
    return s.replace('\\"', '"').replace("\\\\", "\\")


def statements(path):
    """The statements of a Turtle file whose subject starts in column 0 (the generators write each subject so), as (subject, text)."""
    out = []; cur = None
    for line in open(path, encoding="utf-8"):
        if line.startswith("@prefix"):
            continue
        if line[:1] not in (" ", "\t", "\n", "\r") and not line.startswith("#"):
            if cur:
                out.append(cur)
            cur = [line.split()[0], line]
        elif cur is not None:
            cur[1] += line
    if cur:
        out.append(cur)
    return [(s, t) for s, t in out]


def bare(text):
    """The statement with every string literal replaced by a placeholder, so that predicates are read outside the literals only."""
    return re.sub(LIT, '"_"', text)


def run(n):
    fail = []
    rd = os.path.join(REPO, "03-materials", "ch%02d" % n, "rdodi")
    P = lambda part: newest(os.path.join(rd, "sen0401_ch%02d_%s_v*.ttl" % (n, part)))
    paths = {k: P(k) for k in ("research", "domain_tbox", "domain_abox", "document")}
    for k, v in paths.items():
        if not v:
            fail.append(("missing file", k))
    if fail:
        print("failures:", fail); sys.exit(1)
    R = statements(paths["research"]); T = statements(paths["domain_tbox"]); A = statements(paths["domain_abox"]); D = statements(paths["document"])

    # ---- 1 sources
    pubs = {}
    for s, t in R:
        if re.search(r"\ba res:Publication\b", bare(t)[:200]):
            lab = re.search(r"rdfs:label " + LIT, t); src = re.search(r"dcterms:source " + LIT + r"\^\^xsd:anyURI", t)
            pubs[s] = {"label": unesc(lab.group(1)) if lab else "", "source": src.group(1) if src else "",
                       "status": "res:hasVerificationStatus res:Status_Verified" in t, "at": re.search(r'sen0401:verifiedAt "\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d"\^\^xsd:dateTime', t) is not None,
                       "role": re.search(r'sen0401:sourceRole "(primary|secondary)"', t) is not None}
    for s, p in pubs.items():
        if not p["label"]: fail.append(("publication without label", s))
        if not p["source"]: fail.append(("publication without source", s))
        if not p["status"]: fail.append(("publication not verified", s))
        if not p["at"]: fail.append(("publication without verifiedAt", s))
        if not p["role"]: fail.append(("publication without role", s))
    legacy = json.load(open(os.path.join(REPO, "03-materials", "owner-legacy-2025", "legacy_inventory_v1_0_0.json")))
    inv = {}
    def walk(x):
        if isinstance(x, dict):
            if "sha256" in x and "path" in x: inv[x["path"]] = x["sha256"]
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(legacy)
    notes = 0
    for s, p in pubs.items():
        m = re.match(r"urn:sen0401:course-notes:(.+\.pptx):([0-9a-f]{16})$", p["source"])
        if not m:
            continue
        hits = [f for f in inv if os.path.basename(f).replace("_v1_0_0", "") == m.group(1) and inv[f].startswith(m.group(2))]
        if not hits:
            fail.append(("course-notes digest not in the legacy inventory", s, m.group(1))); continue
        f = os.path.join(REPO, hits[0])
        if not os.path.exists(f) or hashlib.sha256(open(f, "rb").read()).hexdigest() != inv[hits[0]] or not inv[hits[0]].startswith(m.group(2)):
            fail.append(("course-notes file differs from its recorded digest", s, hits[0]))
        notes += 1
    src_dir = os.path.join(HERE, "ch%02d-sources" % n); ev_dir = os.path.join(HERE, "ch%02d-evidence" % n)
    bips = 0
    for f in sorted(glob.glob(os.path.join(src_dir, "bip*.txt"))):
        num = int(re.search(r"bip(\d+)\.txt", f).group(1)); txt = open(f, encoding="utf-8", errors="replace").read()
        if not re.search(r"(?im)^\s*BIP:\s*0*%d\s*$" % num, txt) and ("bip-%04d" % num) not in txt:
            fail.append(("saved BIP is not the BIP its name says", os.path.basename(f)))
        bips += 1

    # ---- 2 passages / saved evidence
    nfiles = 0
    for d in (src_dir, ev_dir):
        for f in sorted(glob.glob(os.path.join(d, "*"))):
            if os.path.isdir(f) or f.endswith((".py", ".sh", ".log")):
                continue
            nfiles += 1
            if os.path.getsize(f) == 0: fail.append(("empty saved file", os.path.basename(f)))
            if f.endswith(".json"):
                try:
                    if json.load(open(f, encoding="utf-8")) in (None, [], {}): fail.append(("empty json", os.path.basename(f)))
                except Exception as e:
                    fail.append(("json does not parse", os.path.basename(f), str(e)[:60]))
    vr = os.path.join(ev_dir, "verify_results_v1_0_0.json")
    if os.path.exists(vr):
        res = json.load(open(vr))
        for k, v in res.items():
            if isinstance(v, bool) and not v: fail.append(("saved verify result false", k))
            if isinstance(v, list) and len(v) == 2 and v[0] != v[1] and not k.endswith("bech32m_valid"): fail.append(("saved verify result short", k, v))
        if res.get("length_extension_bech32m_valid", [0])[0] != 0: fail.append(("length extension must fail under bech32m",))
        sub = res.get("substitution_errors_undetected", {})
        if any(sub.get(k) for k in ("one", "two", "three_or_four_random_of_200000")): fail.append(("substitution error undetected", sub))

    # ---- 3 stories
    sm = newest(os.path.join(HERE, "sen0401_ch%02d_stories_v*.py" % n)); mod = os.path.basename(sm)[:-3]
    sys.path.insert(0, HERE); ST = importlib.import_module(mod)
    fail += [("stories", b) for b in ST.run_checks()]
    if len(ST.STORIES) < 3: fail.append(("stories count", len(ST.STORIES)))

    # ---- 4 classes <-> document <-> citations
    classes = {s.split(":", 1)[1] for s, t in T if re.search(r"\ba owl:Class\b", bare(t))}
    secs = {}
    for s, t in D:
        if s.startswith("chx:S_"):
            m = re.search(r"skos:definition " + LIT, t); secs[s[6:]] = unesc(m.group(1)) if m else ""
    for c in sorted(classes):
        if c not in secs: fail.append(("class without section", c))
    for c in sorted(set(secs) - classes):
        fail.append(("section without class", c))
    def known_by(x, label):
        a, y = x.rsplit(", ", 1)
        return (re.search(r"\([^()]*" + re.escape(a) + r"[^()]*\b" + y + r"\b[^()]*\)", label) is not None
                or re.search(r"(?<![\w])(?:[A-Z][a-z]+ )*" + re.escape(a) + r", " + y + r"\b", label) is not None)

    def known(x):
        """'Author, Year' names a publication when one label has the author and the year inside one parenthesis."""
        a, y = x.rsplit(", ", 1)
        return any(known_by(x, p["label"]) for p in pubs.values())
    cited = set()
    for c, body in secs.items():
        cs = CITE.findall(body)
        if not cs: fail.append(("section without citation", c))
        for x in cs:
            cited.add(x)
            if not known(x): fail.append(("section cites an unknown label", c, x))

    # ---- 5 abox
    ios = {}
    for s, t in A:
        if s.startswith("chx:IO_"):
            i = re.search(r"chx:input " + LIT, t); o = re.search(r"chx:output " + LIT, t)
            ios[s[7:]] = (unesc(i.group(1)) if i else None, unesc(o.group(1)) if o else None)
    for k, (i, o) in sorted(ios.items()):
        if i is None or o is None: fail.append(("example without input or output", k)); continue
        if "\n" in i or "\n" in o: fail.append(("newline in an example", k))
        try:
            ast.parse(i, mode="eval")
        except SyntaxError:
            try: ast.parse(i)
            except SyntaxError: fail.append(("input does not compile", k))
        if k not in classes: fail.append(("example of no class", k))
    os.chdir(REPO)
    nexec = 0
    for k, (i, o) in sorted(ios.items()):
        if i is None or o is None: continue
        try:
            t = ast.parse(i); last = t.body.pop() if t.body and isinstance(t.body[-1], ast.Expr) else None
            ns = {"__name__": "__verify__"}; exec(compile(t, k, "exec"), ns)
            got = repr(eval(compile(ast.Expression(last.value), k, "eval"), ns)) if last else repr(None)
        except BaseException as e:
            got = "EXC %r" % (e,)
        nexec += 1
        if got != o: fail.append(("example result differs", k, o[:60], got[:60]))
    if len(ios) < 40: fail.append(("example count", len(ios)))

    # ---- 6 findings and sources
    findings = {}
    for s, t in R:
        if re.search(r"\ba sen0401:Finding\b", bare(t)[:200]):
            b = bare(t); m = re.search(r"sen0401:cites ([^;.]*(?:chx:\w+[ ,]*)+)\s*[;.]", b)
            findings[s] = re.findall(r"chx:(\w+)", m.group(1)) if m else []
    ids = {s.split(":", 1)[1] for s in pubs}
    for f, cs in findings.items():
        if not cs: fail.append(("finding cites nothing", f))
        for c in cs:
            if c not in ids: fail.append(("finding cites an unknown publication", f, c))
    concept_src = set()
    for s, t in R:
        if re.search(r"\ba sen0401:PrimarySourceConcept\b", bare(t)[:200]):
            concept_src |= set(re.findall(r"dcterms:source chx:(\w+)", bare(t)))
    used = {c for cs in findings.values() for c in cs} | concept_src
    for s, p in pubs.items():
        k = s.split(":", 1)[1]
        if k in used: continue
        # cited in a paragraph by (Author, Year): the publication's label contains a cited label
        if any(known_by(x, p["label"]) for x in cited): continue
        fail.append(("publication never cited", k, p["label"][:60]))
    if len(pubs) < 25 or len(findings) < 8: fail.append(("counts", len(pubs), len(findings)))

    print("%s | %s | %s | %s" % tuple(os.path.basename(paths[k]) for k in ("research", "domain_tbox", "domain_abox", "document")))
    print("publications %d (course-notes digests %d, saved BIPs %d); saved files %d; stories %d; classes %d with sections %d; citations %d distinct; examples %d, executed %d; findings %d"
          % (len(pubs), notes, bips, nfiles, len(ST.STORIES), len(classes), len(secs), len(cited), len(ios), nexec, len(findings)))
    print("failures:", fail)
    sys.exit(1 if fail else 0)
