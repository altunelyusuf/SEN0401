#!/usr/bin/env python3
"""sen0401_lineage_research_check v1_0_0 - runs, as an exit-code check for the evidence bridge, one research check of the section-links criteria on the NEWEST research package of a chapter:
  seclinks:NN   sen0401_ch_seclinks_check v1_0_0 NN (declared, links between sections, every section covered)
  annotated:NN  the same with --evidence (every link annotated with the sentence that states it)
  linkdisc:NN   OE missing-link discovery oe_link_discovery v1_1_0 on the chapter's research folder (syntactic, semantic, temporal and duplicate families, BP-D57 and BP-D61): 0 violations beyond the baseline
  kindrule:NN   OE kind rule check oe_kind_rule_check v1_1_0 on the chapter's domain T-Box, with the governance A-Box of the Ontologies checkout (BP-D58, BP-D59)
  samepairs:NN  every link (subject, object) of research v1.1.0 is still stated in the newest research version (the same 28 meanings kept)
  singular:NN   one meaning, one property (BP-D61, rule S6, the owner's standing rule of 2026-10-21): a measurable floor: no two properties with a relationship category in the newest domain T-Box share a label, and no two share both
                a category and a super-property (two properties of one group carry one meaning; their class pair belongs to the link and its sentence, not to a new property). Prints the groups.
Usage: sen0401_lineage_research_check_v1_0_0.py KIND:NN"""
__version__ = "1.0.0"
import glob, os, re, subprocess, sys, tempfile
import rdflib
from rdflib import RDFS
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OEE = os.environ.get("OEE_ROOT", "/home/claude/Ontologies")
KB = rdflib.Namespace("http://example.org/knowledge-base#")
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", p)[0]]


def newest(nn, part):
    fs = glob.glob(os.path.join(REPO, "03-materials", "ch" + nn, "rdodi", "sen0401_ch%s_%s_v*.ttl" % (nn, part)))
    return sorted(fs, key=vkey)[-1]


def main():
    kind, nn = sys.argv[1].split(":")
    if kind in ("seclinks", "annotated"):
        return subprocess.run([sys.executable, "-B", os.path.join(REPO, "08-tooling", "sen0401_ch_seclinks_check_v1_0_0.py"), nn] + (["--evidence"] if kind == "annotated" else [])).returncode
    if kind == "linkdisc":
        return subprocess.run([sys.executable, "-B", OEE + "/repo-tooling/oe_link_discovery_v1_1_0.py", os.path.join(REPO, "03-materials", "ch" + nn, "rdodi")]).returncode
    if kind == "kindrule":
        d = tempfile.mkdtemp(); os.symlink(OEE + "/oe-method", d + "/oe-method"); os.makedirs(d + "/ch" + nn)
        for part in ("domain_tbox", "domain_abox"):
            p = newest(nn, part); os.symlink(p, d + "/ch%s/sen0401_ch%s_%s.ttl" % (nn, nn, part))
        return subprocess.run([sys.executable, "-B", OEE + "/repo-tooling/oe_kind_rule_check_v1_1_0.py", d]).returncode
    if kind == "samepairs":   # every link of the previous research version is still stated, between the same two individuals, in the newest
        fs = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch" + nn, "rdodi", "sen0401_ch%s_domain_abox_v*.ttl" % nn)), key=vkey)
        ts = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch" + nn, "rdodi", "sen0401_ch%s_domain_tbox_v*.ttl" % nn)), key=vkey)
        base = os.environ.get("SAMEPAIRS_BASE", "1.1.0"); bv = "_v" + base.replace(".", "_") + "."
        ob = [f for f in fs if bv in f][0]; ot = [f for f in ts if bv in f][0]
        def pairs(a, tb):
            g = rdflib.Graph(); g.parse(a); h = rdflib.Graph(); h.parse(tb); cats = set(h.subjects(KB.hasRelationshipCategory, None))
            return {frozenset((s, o)) for s, p, o in g if p in cats and isinstance(o, rdflib.URIRef)}
        old = pairs(ob, ot); new = pairs(fs[-1], ts[-1]); miss = sorted(old - new, key=lambda x: sorted(map(str, x)))
        print("%d link pairs in %s, %d in %s; %d of the earlier pairs are no longer stated: %s" % (len(old), os.path.basename(ob), len(new), os.path.basename(fs[-1]), len(miss), [sorted(str(a).split("#")[-1] for a in m) for m in miss][:30]))
        print("RESULT: %s" % ("PASS" if not miss and fs[-1] != ob else "FAIL"))
        return 0 if not miss and fs[-1] != ob else 1
    if kind == "singular":
        g = rdflib.Graph(); g.parse(newest(nn, "domain_tbox"))
        props = sorted(g.subjects(KB.hasRelationshipCategory, None), key=str)
        by = {}
        for p in props:
            cat = str(g.value(p, KB.hasRelationshipCategory)).split("_")[-1]; sup = tuple(sorted(str(x).split("#")[-1].split("/")[-1] for x in g.objects(p, RDFS.subPropertyOf)))
            by.setdefault((cat, sup), []).append((str(p).split("#")[-1], str(g.value(p, RDFS.label))))
        bad = 0; labels = {}
        for p in props:
            labels.setdefault(str(g.value(p, RDFS.label)).lower(), []).append(str(p).split("#")[-1])
        for lab, ps in labels.items():
            if len(ps) > 1: bad += 1; print("FAIL same label %r: %s" % (lab, ps))
        print("%d properties with a relationship category; groups by (category, super-property): %d" % (len(props), len(by)))
        for (cat, sup), ps in sorted(by.items()):
            if len(ps) > 1 and cat != "Comparative": pass
            if len(ps) > 1: bad += 1
            print("  %s %-22s %-24s %d: %s" % ("FAIL" if len(ps) > 1 else "ok  ", cat, ",".join(sup) or "-", len(ps), "; ".join("%s (%s)" % x for x in ps)))
        print("RESULT: %s (a measurable floor of BP-D61: one property per category and super-property; two properties in one group are one meaning unless they differ in category or super-property; the reviewer reads the groups for meanings that differ in the label only)" % ("FAIL" if bad else "PASS"))
        return 1 if bad else 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
