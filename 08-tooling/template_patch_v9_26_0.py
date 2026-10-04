#!/usr/bin/env python3
"""SEN0401 page template 9.26.0, from 9.25.0.

One change, in one query. The chapter-taxonomy view offers a "Book concepts" layer: its legend promises a dashed branch
for "concept from the book, matched by name", its checkbox offers to hide them and its status line counts them. The query
behind that layer, `bookQ`, asked for a book subject that carries BOTH an `rdfs:label` AND a `skos:definition`. That is
how SEN0414's textbook ontology writes a concept's own sentence, and it is the only shape the layer accepted.

The SEN0401 textbook ontology - Mastering Bitcoin, 3rd edition - carries a concept's own sentence differently, and
deliberately: the sentence is the authors' verbatim wording, so it lives on a passage of its own, with its source file,
line, pinned commit, authors and licence attached, and the concept points at it (`introducedBy` -> the passage, whose
`text` is the sentence). None of the five chapter ontologies in that package uses `skos:definition` at all - checked, all
five: zero occurrences. So with the book block newly embedded in the page, the taxonomy would still have reported "0 book
concepts" and drawn none, while its own legend said otherwise: a claim the page's data contradicted.

`bookQ` now accepts either shape, and names neither ontology's vocabulary: a book subject qualifies if it has a label and
either a `skos:definition` of its own, or a property whose name ends in `introducedBy` leading to something with a
property whose name ends in `#text`. Matching by the local name of the predicate is the style the template already uses
in its own SPARQL samples (`FILTER(STRENDS(STR(?pi), "#input"))`), so the page stays course-neutral.

Nothing else changes. The agents and the SPARQL console needed no change at all: they read every embedded Turtle block
whatever its kind, so the book triples became searchable the moment the page build embedded them.

usage: template_patch_v9_26_0.py [IN.html OUT.html]"""
__version__ = "9.26.0"
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_25_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_26_0.html")
h = open(src, encoding="utf-8").read()


def rep(a, b, n=1):
    assert h.count(a) == n, (a[:80], h.count(a))
    return h.replace(a, b)


h = rep(
    """ const bookQ=PFX+'SELECT ?s ?label WHERE { GRAPH ?g { ?s skos:definition ?d ; rdfs:label ?label } FILTER(CONTAINS(STR(?g),":book:")) }';""",
    """ // A concept of the book qualifies for the taxonomy's book layer when it has a label and the book's own sentence for
 // it: either a skos:definition on the concept itself, or an "introducedBy" link to a passage carrying the sentence as
 // its text (the shape a textbook ontology uses when the sentence is the authors' verbatim wording, kept on a passage
 // of its own with its attribution). Predicates are matched by local name, so no ontology's namespace is named here.
 const bookQ=PFX+'SELECT ?s ?label WHERE { GRAPH ?g { ?s rdfs:label ?label . { ?s skos:definition ?d } UNION { ?s ?ip ?pass . ?pass ?tp ?d . FILTER(STRENDS(STR(?ip),"introducedBy") && STRENDS(STR(?tp),"#text")) } } FILTER(CONTAINS(STR(?g),":book:")) }';""")
open(out, "w", encoding="utf-8").write(h)
print("wrote", os.path.basename(out), len(h), "bytes")
