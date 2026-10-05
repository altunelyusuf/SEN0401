#!/usr/bin/env python3
"""Builds a SEN0401 page - a chapter, or a named unit such as "numbers" - from SEN0401's template, with SEN0401's text
from its course configuration.

The page embeds, as Turtle with file names and hashes, the corpus its agents, its chapter taxonomy and its SPARQL
console search. Over version 4.1.0 this build adds the one block that was missing: the ontology of the book chapter the
page teaches - Mastering Bitcoin, 3rd edition, from the mastering-bitcoin-3e package of the Ontologies monorepo, read
with `git show <pinned commit>:<path>` exactly as SEN0414's page build reads its own book, and embedded with
data-kind="book" so the template's book handling (the Book passage kind, the dashed "concept from the book" branches of
the taxonomy, the book graph in SPARQL) finally has triples to work on.

The pin is resolved in this order, and a pin that does not resolve stops the build:
  1. the course's own textbook part, when the configuration names one in corpus.book_pin_source (SEN0414's arrangement);
  2. otherwise corpus.book_pin_commit, which the configuration builder read from the monorepo and recorded.
Every embedded block is named and hashed, and the corpus manifest records, for the book block, the file name, the commit
it was read at and its sha256.

A named unit (the numbers page) has no book chapter, so it gets no book block, and that is stated rather than implied:
the configuration's corpus.book is keyed by chapter number, and a page with no chapter number asks for nothing.

Usage: sen0401_page_build_v4_4_0.py <NN|unit>"""
__version__ = "4.5.0"
# 4.5.0 (over 4.4.0): one change - the default template is course_page_template_v9_29_0.html, so a page this version
#   builds carries the 9.29.0 repairs: the Resources pane shows every kind of checked resource rather than only the
#   five kinds the Python course uses (of their checked links the five chapters were showing 2 of 20, 3 of 14, 9 of 14,
#   1 of 14 and 2 of 16 - only the ones whose kind happened to be 'documentation'); the chapter taxonomy is explained in one cohesive paragraph instead of a single
#   sentence stacked above a paragraph about the same diagram; and a question's stem is written into the question bank
#   as the bank is loaded, so the browser of questions, a generated question and the mock exam all show the stem the
#   item itself carries. Nothing else about the build changes, and the template can still be overridden for a trial
#   with PAGE_TEMPLATE. Recorded here rather than left implicit: page version 9.30.0 = template 9.29.0 + course
#   configuration 2.3.0, which is what the audit's F-C8 asked for.
# 4.4.0 (over 4.3.0): two changes, both for the adversarial audit of the chapter 1 page of 2026-10-04.
#   a) the default template is course_page_template_v9_28_0.html (agent slicing and handover, the taxonomy's default
#      and its example labels, the unapproved-outcomes notice, the hidden empty layers, the vocabulary pane).
#   b) the page data gains "index_page": the file name of the chapter index that really sits beside the page, or ""
#      when there is none. Template 9.28.0 shows the header's "All chapters" link only when this names something, so
#      the dead link to a non-existent index.html (audit F-B5) cannot ship again; generate the index with
#      sen0401_index_build_v1_0_0.py and the link appears by itself on the next build.
#   NOT changed, deliberately, and this is the finding: the audit's F-C1 asked for `&` to be HTML-escaped when a corpus
#   file is embedded, on the evidence that two `&#x27;` sequences in the book ontology "decode to '" before the graph
#   is parsed, making the embedded block differ from the pinned bytes. Checked in Chromium this session rather than
#   assumed: the content of a <script> element is RAW TEXT, so a browser does NOT resolve character references inside
#   it - a one-element test page carrying `Byzantine Generals&#x27; Problem` and `&amp;` in a text/turtle block reads
#   back from textContent with both sequences intact (has_x27 true, has_amp_entity true). Hashing the nine blocks of
#   the shipped 9.28.0 page straight out of the HTML, with only the build's own "</script" escape undone, gives
#   d17a3f30b3c3f333 for the book block against d17a3f30b3c3f333 on disk, and an exact match for all nine. The audit's
#   differing hash came from an extractor that decodes entities, not from the page. Escaping `&` here would have
#   introduced the corruption the finding describes (the browser would deliver `&amp;#x27;`), so the escape is NOT
#   added; what IS added is the measurement, in sen0401_book_corpus_check_v1_2_0.py, which now hashes every embedded
#   block both from the file and from the browser's own textContent against the bytes on disk.
# 4.2.0 (over 4.1.0): embeds the book chapter ontology at the configuration's pinned commit (data-kind="book"), with the
#   file name, commit and sha256 in the corpus manifest; a pin, a path or a book entry that does not resolve raises and
#   stops the build instead of quietly producing a page without the book. Default template is now
#   course_page_template_v9_27_0.html (4.1.0 still defaulted to 9.24.0), so a page built by this version carries both
#   the narrow-screen title-bar fix of 9.25.0 and the taxonomy's book-concept query of 9.26.0.
import glob, hashlib, json, os, re, subprocess, sys
import rdflib
PV = os.environ.get("PAGE_VER", "9_26_0")  # generated files carry the page version they were produced for
N = sys.argv[1]; NUM = N if N.isdigit() else None; N = ("ch%s" % N) if N.isdigit() else N
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ONT = "/home/claude/Ontologies"
T = open(os.path.join(REPO, "08-tooling", os.environ.get("PAGE_TEMPLATE", "course_page_template_v9_29_0.html"))).read()
P = os.path.join(REPO, "08-tooling", "%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v%s.json" % PV))); C = d["course"]["corpus"]
safe = lambda o: json.dumps(o).replace("</", "<\\/")
vkey = lambda x: [int(v) for v in x.rsplit("_v", 1)[1].split(".")[0].split("_")]
latest = lambda pat: sorted(glob.glob(pat), key=vkey)[-1]
blocks, log = [], []
def add(kind, name, text):
    h = hashlib.sha256(text.encode()).hexdigest()[:16]
    blocks.append('<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (kind, name, h, text.replace("</script", "<\\/script")))
    log.append("%s %s %s" % (kind, name, h))
    return h

# ---- the book chapter, at the pinned commit -------------------------------------------------------------------------
def book_pin():
    """The commit the book ontology is read at. Raises if neither source gives a usable one."""
    src = C.get("book_pin_source") or ""
    if src:
        f = os.path.join(REPO, src)
        if not os.path.exists(f):
            raise SystemExit("corpus.book_pin_source names %s, which does not exist; fix the configuration or add the file" % src)
        m = re.search(r'pinnedCommit "([0-9a-f]{40})"', open(f).read())
        if not m:
            raise SystemExit("%s carries no pinnedCommit; the book ontology cannot be pinned from it" % src)
        return m.group(1), src
    pin = C.get("book_pin_commit") or ""
    if not re.fullmatch(r"[0-9a-f]{40}", pin):
        raise SystemExit("the configuration carries neither a usable corpus.book_pin_source nor a 40-character corpus.book_pin_commit; re-run course_page_config_build_v2_2_0.py")
    return pin, "corpus.book_pin_commit in the course configuration"

BOOK = C.get("book") or {}
if NUM is not None:
    if str(int(NUM)) not in BOOK:
        raise SystemExit("the configuration's corpus.book has no entry for chapter %s; re-run course_page_config_build_v2_2_0.py" % NUM)
    pin, pin_from = book_pin()
    entry = BOOK[str(int(NUM))]; path = entry["path"] if isinstance(entry, dict) else entry
    r = subprocess.run(["git", "-C", ONT, "show", "%s:%s" % (pin, path)], capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        raise SystemExit("the pin does not resolve: git -C %s show %s:%s -> %s" % (ONT, pin[:12], path, (r.stderr or "empty file").strip()))
    h = add("book", os.path.basename(path) + "@" + pin[:8], r.stdout)
    book_note = "%s at %s (%s), sha256 %s" % (path, pin[:12], pin_from, h)
else:
    book_note = "no book block: a named unit has no chapter of the book"

for path in C.get("course", []): add("course", os.path.basename(path), open(os.path.join(REPO, path)).read())
RD = os.path.join(REPO, "03-materials", N, "rdodi")
for part, kind in (("domain_tbox", "chapter"), ("domain_abox", "chapter"), ("document", "chapter"), ("research", "research")):
    f = latest(os.path.join(RD, "sen0401_%s_%s_v*.ttl" % (N, part))); add(kind, os.path.basename(f), open(f).read())
LG = rdflib.Graph(); LG.parse(latest(os.path.join(REPO, "07-lineage", "*.ttl")), format="turtle")
BK = rdflib.Namespace("http://example.org/backlog#"); mis = next(LG.subjects(rdflib.RDF.type, BK.Mission), None)
d["mission"] = {"statement": str(LG.value(mis, BK.hasMissionStatement) or ""), "outcome": str(LG.value(mis, BK.hasMissionOutcome) or ""),
                "goals": sorted(str(LG.value(g, rdflib.RDFS.label)) for g in LG.subjects(rdflib.RDF.type, BK.Goal)),
                "objectives": sorted(str(LG.value(o, rdflib.RDFS.label)) for o in LG.subjects(rdflib.RDF.type, BK.Objective))}
_bk = glob.glob(os.path.join(P, "question_bank_v*.json"));
unwrap = lambda x: x["items"] if isinstance(x, dict) and "items" in x else x
QUIZ = unwrap(json.load(open(latest(os.path.join(P, "quiz_v*.json"))))); OBJ = json.load(open(latest(os.path.join(P, "objectives_v*.json"))))
sub = d["unit"]["sub"] if d.get("unit") else d["course"]["chapter_sub"].replace("{n}", str(d["chapter"]))
# 4.4.0: the header's "All chapters" link is shown only when an index really sits beside the page (audit F-B5)
outdir = os.path.join(REPO, "03-materials", N, "page")
d["index_page"] = "index.html" if os.path.exists(os.path.join(outdir, "index.html")) else ""
h = (T.replace("__TITLE__", d["title"]).replace("__PAGEVERSION__", PV.replace("_", ".")).replace("__COURSE__", d["course"]["line"]).replace("__SUB__", sub)
      .replace("__PY__", d["python"]).replace("__DATA__", safe(d)).replace("__QUIZ__", safe(QUIZ)).replace("__BANK__", safe(json.load(open(latest(os.path.join(P, "question_bank_v*.json")))) if _bk else [])).replace("__OBJ__", safe(OBJ)).replace("__CORPUS__", "\n".join(blocks)))
X = os.path.join(P, "extra_resolved_v%s.html" % PV)
h = h.replace("</body></html>", (open(X).read() if os.path.exists(X) else "") + "</body></html>")
out = os.path.join(outdir, "sen0401_%s_page_v%s.html" % (N, PV))
open(out, "w").write(h)
json.dump({"_version": PV.replace("_", "."), "book": book_note, "items": log}, open(os.path.join(P, "corpus_manifest_v%s.json" % PV), "w"), indent=1)
print("written", out, len(h), "bytes")
print("  book:", book_note)
print("  corpus:", "; ".join(log))
