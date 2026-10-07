#!/usr/bin/env python3
"""Writes course_page_config_v2_5_0.json (the SEN0401 course configuration) and checks every program in it.

What this version changes. The textbook ontology package left the Ontologies monorepo. It now has its own private
repository, `altunelyusuf/mastering-bitcoin`, with one folder per edition of the book, and the third edition is `3e/`.
So three things that used to be one thing are now separate here: the repository the pin is resolved in (BOOK_REPO, a
checkout of the new repository), the package's own name, which is its identity and has not changed
(PKG = "mastering-bitcoin-3e"), and the folder it occupies inside that repository (FOLDER = "3e"). The configuration
records all three, because a reader asking "where does this come from" needs the repository and the folder, and a
reader asking "which package is this" needs the name. Nothing about how a chapter's part file is resolved changes:
2.4.0 stopped naming a version token and read the newest part of each chapter out of the pinned tree, and that is what
this version still does, so the package's own later releases are picked up without editing this file.

What version 2.2.0 corrected. Version 2.1.0 declared an empty page corpus and said, in its own note, that "SEN0401 has no
textbook ontology for Mastering Bitcoin and no course ontology yet". The first half of that sentence was false: the
ontology of the course textbook - Mastering Bitcoin, 3rd edition, one file per chapter - exists and is published in the
package `mastering-bitcoin-3e`. Because the configuration said it did not exist, the page
build embedded no book Turtle, so the page's agents, its taxonomy and its SPARQL console had no book triples to search
even though the page template has carried a "book" corpus kind all along. This configuration names the book ontology of
each chapter, pinned to one commit of the monorepo, and states plainly what is and is not available.

Where the pin comes from. The course's own textbook part (`02-textbook/sen0401_textbook_v1_0_0.ttl`) is the authoritative
place for it, exactly as SEN0414 keeps it; that file is being written by another worker and does not exist yet. While it
is absent the pin is read from the monorepo itself (the newest commit touching the package) and recorded here with the
method used. As soon as the course textbook part exists, re-running this builder records it as `book_pin_source` and the
page build reads the pin from it instead - no edit to this file needed.

The course-level ontologies are discovered, not listed by hand: this builder globs the four course parts (profile,
outcomes, textbook, materials) and writes the newest version of each that exists. Today none exists, so `course` is an
empty list; re-run the builder once they land and they are picked up.

The programs (Playground, code patterns, Step-through, Code Lab) are unchanged from 2.1.0 and are imported from its
builder rather than copied, so there is one source for them. Each is executed here under every interpreter given and must
exit 0 with the expected first output line, so a snippet cannot silently rot.

usage: course_page_config_build_v2_7_0.py [interpreter ...]"""
__version__ = "2.7.0"
# 2.7.0 (over 2.6.0): no change of logic. The materials register moved to 1.4.5 (the pages at 9.38.0), and the
#   configuration lists the course parts by name, so the output must be a new file rather than an in-place edit of
#   the released 2.6.0: a configuration a page embeds is frozen the moment that page ships.
# 2.6.0 (over 2.5.0): one change - the instructor key pair is re-provisioned. The private half of the exam key is
#   kept OUTSIDE every repository (README_PORT.md) and did not survive the move to this build environment, so no
#   release code could be minted for the page test, and none could ever be minted for the owner either: the old
#   private key is gone everywhere. README_PORT.md names the remedy - 'Replace the pair...: new key file, new
#   exam.public_key in the configuration, rebuild' - and this version is that rebuild. The new pair was generated
#   on 2026-10-06 into /home/claude/instructor_keys/ (private, mode 600); the public half reaches the
#   configuration through course_page_config_build_v2_1_0's existing preference for the public-key file. Pages
#   built with this configuration accept codes from the new key; pages built earlier answered to the old key,
#   whose loss leaves their exam release orphaned until they are rebuilt - which this cycle does.
# 2.5.0 (over 2.4.0): the book package is read from its own repository, altunelyusuf/mastering-bitcoin, at
#   folder 3e, instead of from the Ontologies monorepo at folder mastering-bitcoin-3e. The package name is kept
#   as the package's identity and the folder is recorded beside it (corpus.book_pin_folder is new), because the
#   two were the same string in the monorepo and are not any more. The pin itself comes from the course's own
#   textbook part exactly as before, and each chapter's newest part is still resolved from the pinned tree.
# 2.2.0 (over 2.1.0): corpus.book names one book-chapter ontology per course chapter, with the book's own chapter label,
#   pinned by commit; corpus.course is globbed from the course parts that exist (empty today); corpus.note corrected.
#   Everything else - name, line, chapter_sub, chapter_intro, playground, codelab_snippets, sparql_samples,
#   trace_examples, code_patterns, limits, exam - is taken from course_page_config_build_v2_1_0 unchanged.
import glob, importlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
# 2.5.0: the checkout the pin is resolved in, the package's name, and the folder it occupies there. BOOK_REPO must be
# a checkout of altunelyusuf/mastering-bitcoin that contains the pinned commit; it is a path on this machine, which is
# why it is a constant here and the repository's real name is written into the configuration below.
BOOK_REPO = os.environ.get("SEN0401_BOOK_REPO", "/home/claude/mastering-bitcoin")
BOOK_REPO_NAME = "altunelyusuf/mastering-bitcoin"
PKG = "mastering-bitcoin-3e"
FOLDER = "3e"
sys.path.insert(0, HERE)
base = importlib.import_module("course_page_config_build_v2_1_0")

# ---- the book ontology: one file per chapter, in the package's own repository, at one pinned commit -----------------
BOOK_DIR = FOLDER + "/01-ontologies"
CHAPTERS = range(1, 15)          # the package holds an ontology for each of the book's 14 chapters
def _newest_textbook_part():
    """The newest 02-textbook part on disk. 2.4.0: the name was fixed at v1_0_0, so the pin kept being read from the
    superseded part after 1.1.0 moved it to the package's 0.9.1 release."""
    import glob as _g
    c = sorted(_g.glob(os.path.join(REPO, "02-textbook", "sen0401_textbook_v*.ttl")),
               key=lambda f: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", f).groups()])
    return os.path.relpath(c[-1], REPO) if c else "02-textbook/sen0401_textbook_v1_0_0.ttl"
TEXTBOOK_PART = _newest_textbook_part()

# 2.4.0: the book part's own version is no longer written into this builder. The package released 0.9.1, in which
# chapters 1, 8, 9, 12 and 14 and appendix A became 1.1.1 because HTML character references had reached their labels
# ("Byzantine Generals&#x27; Problem"); a builder naming "_v1_1_0" would have pinned the superseded file. The newest
# part for a chapter is now read from the pinned commit's own tree, so a later release of the package is picked up
# without editing this file, and the file actually pinned is recorded in the configuration.
def _book_files_at(pin):
    r = subprocess.run(["git", "-C", BOOK_REPO, "ls-tree", "--name-only", pin, BOOK_DIR + "/"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:300]
    return [os.path.basename(x) for x in r.stdout.split()]
def _newest_book_file(chapter, pin, _cache={}):
    names = _cache.get(pin) or _cache.setdefault(pin, _book_files_at(pin))
    pat = re.compile(r"^mastering_bitcoin_3e_ch%02d_v(\d+)_(\d+)_(\d+)\.ttl$" % chapter)
    cands = [(tuple(int(x) for x in m.groups()), m.group(0)) for m in (pat.match(n) for n in names) if m]
    assert cands, "no ontology for book chapter %d at %s" % (chapter, pin[:8])
    return sorted(cands)[-1][1]



def git(*args):
    r = subprocess.run(["git", "-C", BOOK_REPO] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def resolve_pin():
    """The commit the book ontology is read at, and a sentence saying how it was obtained."""
    part = os.path.join(REPO, TEXTBOOK_PART)
    if os.path.exists(part):
        m = re.search(r'pinnedCommit "([0-9a-f]{40})"', open(part).read())
        if m:
            return m.group(1), TEXTBOOK_PART, "read from the course's own textbook part %s" % TEXTBOOK_PART
        raise SystemExit("%s exists but carries no pinnedCommit; fix the textbook part, do not guess a pin" % TEXTBOOK_PART)
    pin = git("log", "-1", "--format=%H", "--", FOLDER).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", pin or ""):
        raise SystemExit("no commit touching %s found in %s" % (FOLDER, BOOK_REPO))
    return pin, "", "newest commit touching %s in %s (git log -1 -- %s); the course's own textbook part %s does not exist yet" % (FOLDER, BOOK_REPO_NAME, FOLDER, TEXTBOOK_PART)


def book_entries(pin):
    """One entry per chapter: the file to read at the pin and the book's own label for that chapter.

    Each entry is verified at the pin before it is written: the file must exist there, and inside it the chapter
    individual must carry the matching inventory key and part number, so the course chapter N really is book chapter N.
    """
    out, labels = {}, {}
    for n in CHAPTERS:
        path = "%s/%s" % (BOOK_DIR, _newest_book_file(n, pin))
        text = git("show", "%s:%s" % (pin, path))
        m = re.search(r'mbb:Chapter_%02d a mbb:Chapter ; rdfs:label "([^"]+)"@en ; mbb:inventoryKey "ch%02d" ; mbb:partNumber %d\b' % (n, n, n), text)
        if not m:
            raise SystemExit("%s at %s does not declare chapter %d with inventory key ch%02d and part number %d" % (path, pin[:8], n, n, n))
        out[str(n)] = {"path": path, "chapter": m.group(1)}
        labels[n] = m.group(1)
    return out, labels


def course_parts():
    """The newest version of each SEN0401 course-level ontology that exists on disk, in SEN0414's order."""
    found = []
    for folder, stem in (("00-course-profile", "sen0401_course"), ("01-outcomes", "sen0401_outcomes"),
                         ("02-textbook", "sen0401_textbook"), ("03-materials", "sen0401_materials")):
        fs = sorted(glob.glob(os.path.join(REPO, folder, stem + "_v*.ttl")),
                    key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-4].split("_")])
        if fs:
            found.append("%s/%s" % (folder, os.path.basename(fs[-1])))
    return found


PIN, PIN_SOURCE, PIN_HOW = resolve_pin()
BOOK, BOOK_LABELS = book_entries(PIN)
COURSE = course_parts()

NOTE = (
    "The page's agents, its chapter taxonomy and its SPARQL console search: the ontology of the course textbook - "
    "Mastering Bitcoin, 3rd edition (Antonopoulos and Harding), one file per book chapter, taken from the "
    "mastering-bitcoin-3e package, which lives in its own private repository altunelyusuf/mastering-bitcoin in the "
    "folder 3e, read at the pinned commit in book_pin_commit; the chapter whose "
    "number the page carries; the chapter's own RDODI domain ontology, document and research record; and the text of the "
    "page itself. %s "
    "This corrects version 2.1.0, which declared an empty corpus and stated that no textbook ontology existed - it did, "
    "and the pages were built without it."
) % ("SEN0401's own course-level ontologies - course profile, learning outcomes, textbook part and materials - are "
     "listed in corpus.course: " + ", ".join(COURSE) + "." if COURSE else
     "SEN0401's own course-level ontologies - course profile, learning outcomes, textbook part and materials - do not "
     "exist on disk yet, so corpus.course is empty; re-running this builder lists whichever of them are present and the "
     "next page build embeds them.")

CFG = dict(base.CFG)
CFG["_version"] = "2.7.0"
# The About > Mission pane lists the course learning outcomes. Template 9.27.0 finds that query by name, so the
# sample belongs in this list; it is appended, not inserted, because the page test selects a sample by position.
CFG["sparql_samples"] = list(base.CFG["sparql_samples"]) + [
 ("Course learning outcomes", "{PFX}SELECT ?code ?statement WHERE {\n  GRAPH ?g { ?o <https://purl.imsglobal.org/spec/case/v1p0/vocab#humanCodingScheme> ?code ;\n"
  "              <https://purl.imsglobal.org/spec/case/v1p0/vocab#fullStatement> ?statement }\n} ORDER BY ?code"),
]
CFG["corpus"] = {
    "book_pin_repository": BOOK_REPO_NAME,
    "book_pin_package": PKG,
    "book_pin_folder": FOLDER,
    "book_pin_commit": PIN,
    "book_pin_how": PIN_HOW,
    "book_pin_source": PIN_SOURCE,
    "book_package_version": open(os.path.join(BOOK_REPO, FOLDER, "VERSION.txt")).read().strip(),
    "book": BOOK,
    "course": COURSE,
    "note": NOTE,
}

if __name__ == "__main__":
    interps = sys.argv[1:] or ["python3", "/root/.local/bin/python3.14"]
    bad = base.run_checks(interps)
    n = len(base.PATTERNS) + len(base.TRACE) + len(base.CODELAB)
    print("%d programs x %d interpreters (%s): %s" % (n, len(interps), ", ".join(interps), "all ran" if not bad else "FAILURES"))
    for b in bad:
        print(" -", b)
    if bad:
        sys.exit(1)
    print("book ontology pinned at %s (%s)" % (PIN[:12], PIN_HOW))
    for k in sorted(BOOK, key=int):
        print("  course chapter %-2s -> %s  [book chapter: %s]" % (k, os.path.basename(BOOK[k]["path"]), BOOK[k]["chapter"]))
    print("course-level ontologies found: %s" % (", ".join(COURSE) if COURSE else "none yet"))
    out = os.path.join(HERE, "course_page_config_v2_7_0.json")
    json.dump(CFG, open(out, "w"), indent=1, ensure_ascii=False)
    print("wrote", out)
