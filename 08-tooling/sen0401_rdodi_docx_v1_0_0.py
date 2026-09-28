#!/usr/bin/env python3
"""Writes a chapter's RDODI Stage 3 document (the Turtle document) as a Word file: the chapter title, a one-line
provenance, then one heading per section at its hierarchy level with its body below - exactly the text of the Turtle,
nothing added. The file's version property carries the version in its name.
Usage: sen0401_rdodi_docx_v1_0_0.py <NN> <docx-version, e.g. 1.0.0>"""
__version__ = "1.0.0"
import glob, os, sys
import docx, rdflib
N, VER = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RD = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi")
f = sorted(glob.glob(os.path.join(RD, "sen0401_ch%s_document_v*.ttl" % N)), key=lambda x: [int(v) for v in os.path.splitext(x.rsplit("_v", 1)[1])[0].split("_")])[-1]
g = rdflib.Graph().parse(f)
DOC = rdflib.Namespace("http://example.org/rdodi/document-ontology#"); SK = rdflib.namespace.SKOS; RDFS = rdflib.RDFS
title = next(str(o) for s, o in g.subject_objects(RDFS.label) if str(s).endswith("#Document"))
short = title.split(":")[0]
secs = sorted(((int(g.value(s, DOC.sectionOrder)), int(g.value(s, DOC.hierarchyLevel)), str(g.value(s, DOC.sectionTitle)), str(g.value(s, SK.definition))) for s in g.subjects(DOC.sectionTitle, None)))
d = docx.Document(); d.add_heading(short, 0)
d.add_paragraph("SEN0401 Block Chain — chapter %d. RDODI Stage 3 document, derived from the Stage 2 domain ontology; every number shown was executed under the interpreter the research record names." % int(N))
for _, lv, t, body in secs:
    d.add_heading(t, lv); d.add_paragraph(body)
cp = d.core_properties; cp.title = "SEN0401 chapter %d — RDODI document" % int(N); cp.author = "Yusuf Altunel"; cp.version = VER
out = os.path.join(RD, "sen0401_ch%s_document_v%s.docx" % (N, VER.replace(".", "_"))); d.save(out); print("written", out, len(secs), "sections")
