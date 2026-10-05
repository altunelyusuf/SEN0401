#!/usr/bin/env python3
"""Reissues the RDODI Stage 1 research record of SEN0401 chapters 2 to 5 as a new MINOR version, with three changes and
nothing else. It follows the incremental idiom the chapter 3 and chapter 4 research generators already use - read the
current record, edit it, write the next version - and handles all four chapters from one file because the three changes
are identical in each; a per-chapter copy would be four files differing only in a version token.

The three changes:

1. The prefix that names this course's own vendor namespace <http://example.org/sen0401#> is written `sen0401:`
   throughout. The records of chapters 2 to 5 inherited the name `sen0414:` from the sibling Python course's generator,
   bound to the SEN0401 IRI; the name was wrong, the IRI was right, so every subject, predicate and object keeps its
   identity and the reissued graph carries exactly the triples the old one did, plus the two additions below. Chapter 1's
   own record already writes `sen0401:` in its body, so this brings chapters 2 to 5 to the convention the course
   already follows, and it removes a token of another course from a SEN0401 artifact.

2. The chapter's renewed lecture deck becomes a publication of the record, `chx:P_DECK`, exactly as the owner's 2021
   course notes are already a publication of it: a label that says what the file is, a `urn:sen0401:` source carrying
   the file's own sha256, a verification status and time. The page's Reference tab lists the research record's
   publications, so this is what makes the deck reachable from the chapter page. The deck is the newest
   `03-materials/chNN/SEN0401_Ch*_3e_v*.pptx`; its size, slide count and sha256 are measured here, by this script, at
   the moment of the reissue, and written into the label.

3. A finding records a known limit of the chapter page: the chapter's own SHACL shape file is not among the Turtle
   blocks the page embeds, so the page cannot show or run the quality gate that governs the ontology it teaches from.
   The limit is stated where a reader of the record will meet it rather than left for a reader to discover.

Usage: python3 sen0401_research_reissue_v1_0_0.py            (all four chapters)
       python3 sen0401_research_reissue_v1_0_0.py 03 05      (named chapters)
Needs rdflib, to re-parse each written file and to prove the reissue added only the intended triples."""
__version__ = "1.0.0"
import glob, hashlib, os, re, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TODAY = "2026-10-05"
VERIFIED = "2026-10-05T01:30:00"

# chapter -> (current research version, the version this reissue carries)
STEPS = {"02": ("1.2.0", "1.3.0"), "03": ("1.1.0", "1.2.0"), "04": ("1.1.0", "1.2.0"), "05": ("1.0.0", "1.1.0")}

NOTE = ("MINOR over %s, additive: the prefix naming this course's own vendor namespace is written sen0401: throughout "
        "(the same IRI under its proper name, so every triple of %s is carried over unchanged); the chapter's renewed "
        "lecture deck is added as a publication, which is what puts it in the chapter page's reference list; and a "
        "finding records that the chapter's SHACL shape file is not among the page's embedded corpus files.")

SHAPES_FINDING = (
    "Known limit of the chapter page. The quality gate that governs this chapter's ontology is a SHACL shape file, "
    "%(shapes)s, which states %(n)d node shapes: that every individual carries a label, that anything defined cites its "
    "source, and that a worked example carries exactly one input and one output. The chapter builder applies those "
    "shapes to the TBox and the ABox before it writes them, and the build fails if they are violated, so the gate does "
    "run; what it does not do is reach the student. The interactive page embeds the chapter's TBox, ABox, document and "
    "this research record as Turtle, and the shape file is not among them, so a reader who opens the page can read the "
    "ontology it teaches from but cannot read, query or re-run the gate that admitted it, and the page's own list of "
    "the triples in each corpus file never mentions the shapes. The limit is recorded here rather than repaired here "
    "because the list of files the page embeds is set by the page build chain, which this chapter does not own; "
    "repairing it means adding the shape file to that chain's corpus list, after which this finding should be revised "
    "to say that the gate is shipped.")


def q(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def deck_facts(ch):
    """The newest deck of the chapter, with the figures measured now."""
    vk = lambda p: [int(x) for x in re.search(r"_v(\d+_\d+_\d+)\.pptx$", p).group(1).split("_")]
    cands = sorted(glob.glob(os.path.join(REPO, "03-materials", ch, "SEN0401_*_3e_v*.pptx")), key=vk)
    if not cands:
        raise SystemExit("%s: no deck 03-materials/%s/SEN0401_*_3e_v*.pptx on disk" % (ch, ch))
    f = cands[-1]
    raw = open(f, "rb").read()
    with zipfile.ZipFile(f) as z:
        slides = sum(1 for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n))
    if not slides:
        raise SystemExit("%s: %s holds no slides" % (ch, os.path.basename(f)))
    return os.path.basename(f), len(raw), slides, hashlib.sha256(raw).hexdigest()


def shape_facts(ch):
    """The newest shape file of the chapter and how many node shapes it states."""
    vk = lambda p: [int(x) for x in re.search(r"_v(\d+_\d+_\d+)\.ttl$", p).group(1).split("_")]
    cands = sorted(glob.glob(os.path.join(REPO, "03-materials", ch, "rdodi",
                                          "sen0401_%s_domain_shacl_v*.ttl" % ch)), key=vk)
    if not cands:
        raise SystemExit("%s: no shape file on disk" % ch)
    import rdflib
    g = rdflib.Graph().parse(cands[-1], format="turtle")
    SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    return os.path.basename(cands[-1]), len(set(g.subjects(rdflib.RDF.type, SH.NodeShape)))


def reissue(ch):
    """ch is the chapter folder name, e.g. "ch03"."""
    old, new = STEPS[ch[2:]]
    ov, nv = old.replace(".", "_"), new.replace(".", "_")
    rd = os.path.join(REPO, "03-materials", ch, "rdodi")
    src = os.path.join(rd, "sen0401_%s_research_v%s.ttl" % (ch, ov))
    t = open(src, encoding="utf-8").read()
    base = "http://example.org/sen0401/%s/research" % ch

    # ---- 1. the prefix, by name only ----
    t = t.replace("@prefix sen0414: <http://example.org/sen0401#> .",
                  "@prefix sen0401: <http://example.org/sen0401#> .")
    if "@prefix sen0401:" not in t:
        raise SystemExit("%s: the record does not declare the vendor namespace as expected" % ch)
    t = re.sub(r"\bsen0414:", "sen0401:", t)
    if "sen0414" in t:
        raise SystemExit("%s: a foreign token survives the rename" % ch)

    # ---- the header: version, identity, revision chain, date ----
    t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % new, 1)
    t = t.replace("/research/%s>" % old, "/research/%s>" % new, 1)
    t = t.replace('"sen0401_%s_research_v%s"' % (ch, ov), '"sen0401_%s_research_v%s"' % (ch, nv), 1)
    t = re.sub(r'dcterms:modified "[0-9-]+"\^\^xsd:date', 'dcterms:modified "%s"^^xsd:date' % TODAY, t, count=1)
    # the record inherits whatever revision statement its own predecessor carried; a release states exactly one
    # link in the chain, so any inherited prov:wasRevisionOf on the ontology header is dropped before the new pair
    # is written. The statement may be the last in the header block, in which case it ends the block with a period.
    inherited = re.findall(r"\n *prov:wasRevisionOf <%s/[0-9.]+> *([;.])" % re.escape(base), t)
    for term in inherited:
        t = re.sub(r"\n *prov:wasRevisionOf <%s/[0-9.]+> *;" % re.escape(base), "", t, count=1)
        if term == ".":
            # it closed the block: the statement before it must now close it instead
            t = re.sub(r"(\n *prov:wasRevisionOf <%s/[0-9.]+> *)\." % re.escape(base),
                       "", t, count=1)
            t = re.sub(r"(<%s> a owl:Ontology ;(?:.|\n)*?prov:wasAttributedTo <[^>]+>) ;" % re.escape(base),
                       r"\1 .", t, count=1)
    if re.search(r"prov:wasRevisionOf <%s/" % re.escape(base), t):
        raise SystemExit("%s: an inherited revision statement survives" % ch)
    t = t.replace("    prov:wasGeneratedBy",
                  "    owl:priorVersion <%s/%s> ;\n    prov:wasRevisionOf <%s/%s> ;\n    prov:wasGeneratedBy"
                  % (base, old, base, old), 1)
    note = NOTE % (old, old)
    m = re.search(r'rdfs:comment "([^"]*)"@en ;', t)
    if m:
        t = t[:m.start()] + 'rdfs:comment "%s %s"@en ;' % (m.group(1), q(note)) + t[m.end():]
    else:
        t = re.sub(r"(owl:versionIRI <[^>]+> ;)", lambda mm: mm.group(1) + '\n    rdfs:comment "%s"@en ;' % q(note),
                   t, count=1)

    # ---- 2. the deck, as a publication of the record ----
    name, size, slides, sha = deck_facts(ch)
    label = ("Lecture deck: %s, the newest lecture deck of this chapter in 03-materials/%s - %d slides, %d bytes "
             "(sha256 %s); the slide count, the size and the digest were measured from the file itself on %s"
             % (name, ch, slides, size, sha[:16], TODAY))
    pub = ('chx:P_DECK a res:Publication ; rdfs:label "%s"@en ; '
           'dcterms:source "urn:sen0401:lecture-deck:%s:%s"^^xsd:anyURI ; '
           'res:hasVerificationStatus res:Status_Verified ; sen0401:verifiedAt "%s"^^xsd:dateTime ; '
           'sen0401:sourceRole "secondary" .' % (q(label), name, sha[:16], VERIFIED))
    mem = re.search(r"(rdfs:member )((?:chx:\w+, )*chx:\w+)( \.)", t)
    if not mem:
        raise SystemExit("%s: the research project lists no members to add the deck to" % ch)
    t = t[:mem.start()] + mem.group(1) + mem.group(2) + ", chx:P_DECK" + mem.group(3) + t[mem.end():]

    # ---- 3. the known limit ----
    shapes, nshapes = shape_facts(ch)
    fids = [int(x) for x in re.findall(r"\bchx:F(\d+) a sen0401:Finding", t)]
    fid = (max(fids) + 1) if fids else 1
    fnd = ('chx:F%d a sen0401:Finding ; rdfs:label "Known limit"@en ; sen0401:findingText "%s" ; '
           "sen0401:cites chx:P_DECK ." % (fid, q(SHAPES_FINDING % dict(shapes=shapes, n=nshapes))))

    # both additions go in before the scorecard, which closes the record
    anchor = "chx:Scorecard a sen0401:QualityScorecard"
    if anchor not in t:
        raise SystemExit("%s: no scorecard to write before" % ch)
    t = t.replace(anchor, pub + "\n" + fnd + "\n" + anchor, 1)

    out = os.path.join(rd, "sen0401_%s_research_v%s.ttl" % (ch, nv))
    open(out, "w", encoding="utf-8").write(t)

    # ---- the reissue must parse, and must have added only what it says it added ----
    import rdflib
    a = rdflib.Graph().parse(src, format="turtle")
    b = rdflib.Graph().parse(out, format="turtle")
    hdr = rdflib.URIRef(base)
    sa = {x for x in a if x[0] != hdr}
    sb = {x for x in b if x[0] != hdr}
    CHX = rdflib.Namespace("http://example.org/sen0401/%s#" % ch)
    added = sb - sa
    removed = sa - sb
    allowed_new = {CHX.P_DECK, CHX["F%d" % fid]}
    stray = {x for x in added if x[0] not in allowed_new and not (x[0] == CHX.Research and x[1] == rdflib.RDFS.member)}
    if stray or removed:
        raise SystemExit("%s: unintended change\n  added %s\n  removed %s" % (ch, sorted(stray)[:3], sorted(removed)[:3]))
    print("%s research %s -> %s | %d triples -> %d (+%d) | deck %s (%d slides) | finding F%d on %s (%d shapes)"
          % (ch, old, new, len(a), len(b), len(b) - len(a), name, slides, fid, shapes, nshapes))


for ch in (sys.argv[1:] or sorted(STEPS)):
    reissue(ch if ch.startswith("ch") else "ch" + ch)
