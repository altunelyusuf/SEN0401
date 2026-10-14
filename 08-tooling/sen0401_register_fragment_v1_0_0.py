#!/usr/bin/env python3
"""sen0401_register_fragment v1.0.0 - prints the four register entries (Deck_ChNN_3e, Doc_ChNN, Ontology_ChNN, Page_ChNN) for a chapter in the style of
03-materials/sen0401_materials_v1_4_8.ttl, from the files that PHYSICALLY exist under 03-materials/chNN (newest version of each), so a register entry can never name a file
that is not there. It writes nothing to the register: the owner of the register pastes the fragment (the lineage register is another agent's file).
Usage: sen0401_register_fragment_v1_0_0.py NN [--lo K] [--out file.ttl]      Environment: SEN0401_ROOT.   Exit 1 when a part is missing (the part is named)."""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1:]
if not a:
    sys.exit(__doc__)
n = "%02d" % int(a[0]); lo = a[a.index("--lo") + 1] if "--lo" in a else str(int(n)); out = a[a.index("--out") + 1] if "--out" in a else None
M = os.path.join(ROOT, "03-materials", "ch" + n)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
def newest(pat):
    fs = sorted(glob.glob(os.path.join(M, pat)), key=vk)
    return os.path.relpath(fs[-1], ROOT) if fs else None
deck = newest("SEN0401_Ch%s_*_3e_v*.pptx" % n); docx = newest("rdodi/sen0401_ch%s_document_v*.docx" % n); doct = newest("rdodi/sen0401_ch%s_document_v*.ttl" % n)
ont = [newest("rdodi/sen0401_ch%s_%s_v*.ttl" % (n, p)) for p in ("research", "domain_tbox", "domain_abox", "domain_shacl")]
page = newest("page/sen0401_ch%s_page_v*.html" % n); pabox = newest("page/sen0401_ch%s_page_abox_v*.ttl" % n)
missing = [k for k, v in (("deck", deck), ("document docx", docx), ("document ttl", doct), ("research", ont[0]), ("tbox", ont[1]), ("abox", ont[2]), ("shacl", ont[3]), ("page", page)) if not v]
if missing:
    sys.exit("REFUSED: chapter %s has no %s under 03-materials/ch%s" % (n, ", ".join(missing), n))
pv = ".".join(re.findall(r"_v(\d+)_(\d+)_(\d+)", page)[-1][:2])
frag = '''sen0401:Deck_Ch%(n)s_3e a schema:LearningResource ;
    dcterms:title "Chapter %(c)d: TODO title - built for the third edition" ;
    dcterms:format "application/vnd.openxmlformats-officedocument.presentationml.presentation" ;
    cme:fileInPart "%(deck)s" ;
    cme:renewalStatus "TODO: when built, to which standard (CME materials look-and-feel v1.0.0), by which renderer and checks; slide count read from the file." ;
    dcterms:source "%(ont0)s; 08-tooling/sen0401_ch%(n)s_stories_v1_0_0.py (self-checked); 08-tooling/ch%(n)s-deck/examples_out_v1_0_0.json." ;
    cme:servesOutcome sen0401:LO%(lo)s .

sen0401:Doc_Ch%(n)s a schema:LearningResource ;
    dcterms:title "TODO: chapter %(c)d document title" ;
    dcterms:format "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ;
    cme:fileInPart "%(docx)s" ;
    dcterms:source "%(doct)s" .

sen0401:Ontology_Ch%(n)s a schema:LearningResource ;
    dcterms:title "Chapter %(c)d ontology package: research record and domain ontology" ;
    dcterms:format "text/turtle" ;
    cme:fileInPart %(parts)s ;
    cme:servesOutcome sen0401:LO%(lo)s .

sen0401:Page_Ch%(n)s a schema:LearningResource ;
    dcterms:title "Chapter %(c)d interactive page, version %(pv)s" ;
    dcterms:format "text/html" ;
    cme:fileInPart "%(page)s" ;
    cme:servesOutcome sen0401:LO%(lo)s ;
    dcterms:source "%(psrc)s" .
''' % dict(n=n, c=int(n), deck=deck, ont0=ont[0], lo=lo, docx=docx, doct=doct, pv=pv, page=page, psrc=pabox or ont[2],
           parts=" ,\n                   ".join('"%s"' % p for p in ont))
if out:
    open(out, "w").write(frag)
else:
    print(frag)
