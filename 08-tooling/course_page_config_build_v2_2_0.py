#!/usr/bin/env python3
"""Writes course_page_config_v2_2_0.json (the SEN0401 course configuration) and checks every program in it.

What this version corrects. Version 2.1.0 declared an empty page corpus and said, in its own note, that "SEN0401 has no
textbook ontology for Mastering Bitcoin and no course ontology yet". The first half of that sentence was false: the
ontology of the course textbook - Mastering Bitcoin, 3rd edition, one file per chapter - exists and is published in the
Ontologies monorepo as the package `mastering-bitcoin-3e`. Because the configuration said it did not exist, the page
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

usage: course_page_config_build_v2_2_0.py [interpreter ...]"""
__version__ = "2.2.0"
# 2.2.0 (over 2.1.0): corpus.book names one book-chapter ontology per course chapter, with the book's own chapter label,
#   pinned by commit; corpus.course is globbed from the course parts that exist (empty today); corpus.note corrected.
#   Everything else - name, line, chapter_sub, chapter_intro, playground, codelab_snippets, sparql_samples,
#   trace_examples, code_patterns, limits, exam - is taken from course_page_config_build_v2_1_0 unchanged.
import glob, importlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ONT = "/home/claude/Ontologies"
PKG = "mastering-bitcoin-3e"
sys.path.insert(0, HERE)
base = importlib.import_module("course_page_config_build_v2_1_0")

# ---- the book ontology: one file per chapter, in the monorepo package, at one pinned commit -------------------------
BOOK_DIR = PKG + "/01-ontologies"
BOOK_FILE = "mastering_bitcoin_3e_ch%02d_v1_1_0.ttl"
CHAPTERS = range(1, 15)          # the package holds an ontology for each of the book's 14 chapters
TEXTBOOK_PART = "02-textbook/sen0401_textbook_v1_0_0.ttl"


def git(*args):
    r = subprocess.run(["git", "-C", ONT] + list(args), capture_output=True, text=True)
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
    pin = git("log", "-1", "--format=%H", "--", PKG).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", pin or ""):
        raise SystemExit("no commit of %s found in %s" % (PKG, ONT))
    return pin, "", "newest commit of %s in the Ontologies monorepo (git log -1 -- %s); the course's own textbook part %s does not exist yet" % (PKG, PKG, TEXTBOOK_PART)


def book_entries(pin):
    """One entry per chapter: the file to read at the pin and the book's own label for that chapter.

    Each entry is verified at the pin before it is written: the file must exist there, and inside it the chapter
    individual must carry the matching inventory key and part number, so the course chapter N really is book chapter N.
    """
    out, labels = {}, {}
    for n in CHAPTERS:
        path = "%s/%s" % (BOOK_DIR, BOOK_FILE % n)
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
    "mastering-bitcoin-3e package of the Ontologies monorepo at the pinned commit in book_pin_commit, the chapter whose "
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
CFG["_version"] = "2.2.0"
CFG["corpus"] = {
    "book_pin_repository": "altunelyusuf/Ontologies",
    "book_pin_package": PKG,
    "book_pin_commit": PIN,
    "book_pin_how": PIN_HOW,
    "book_pin_source": PIN_SOURCE,
    "book_package_version": open(os.path.join(ONT, PKG, "VERSION.txt")).read().strip(),
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
    out = os.path.join(HERE, "course_page_config_v2_2_0.json")
    json.dump(CFG, open(out, "w"), indent=1, ensure_ascii=False)
    print("wrote", out)
