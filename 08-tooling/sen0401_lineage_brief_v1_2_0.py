#!/usr/bin/env python3
"""sen0401_lineage_brief v1_2_0 - generates the executor brief of each task of the section-links story of iteration 14 FROM THE REGISTER (task text, its story, the criterion it satisfies, the exclusions of the scope, the tools and
versions the criterion is measured with) plus the written method (OEE relationship taxonomy), the precedents and the rules of an executor, and names the executor session. The coordinator passes a brief unedited; the register's note on
'work begun' names the same session. A brief is a rendering of the register at the version it names: if the register changes, the brief is generated again. Version 1.2.0 over 1.1.0: the rule one meaning one property (BP-D61, rules S1 to S6) and the consolidation task of iteration 15; it writes only the briefs of tasks that have not started (the briefs passed to the two research sessions stay as they were passed, in git 000288a). Version 1.0.0 was for iteration 13 and is unchanged.
Usage: sen0401_lineage_brief_v1_2_0.py [OUTDIR]   (default 08-tooling/briefs/iter14)"""
__version__ = "1.2.0"
import os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#")
REPO = M.REPO
SESSIONS = {"TK_SecLinks_Ch10_Consolidate": "SEN0401-I15-consolidate-ch10", "TK_SecLinks_PageData": "SEN0401-I14-pagedata", "TK_SecLinks_Ch10_Page": "SEN0401-I14-page-ch10", "TK_SecLinks_Ch11_Page": "SEN0401-I14-page-ch11"}
PASSED = {"TK_SecLinks_Ch10_Research": "SEN0401-I14-research-ch10", "TK_SecLinks_Ch11_Research": "SEN0401-I14-research-ch11"}   # briefs passed earlier; not regenerated
VERIFY_TASKS = ["TK_SecLinks_Ch10_Verify", "TK_SecLinks_Ch11_Verify"]   # no executor: the builder session controls and runs the evidence bridge
CRIT = {"Ch10": "AC3L_Ch10", "Ch11": "AC3L_Ch11"}
EXTRA_CRIT = {"TK_SecLinks_Ch10_Consolidate": ["AC3L_Ch10_Singular"]}
BLOCKED = {"TK_SecLinks_PageData": ["TK_SecLinks_Ch10_Consolidate"], "TK_SecLinks_Ch10_Page": ["TK_SecLinks_Ch10_Consolidate", "TK_SecLinks_PageData"], "TK_SecLinks_Ch11_Page": ["TK_SecLinks_PageData"]}
OWNER = ('"Sections are linked with each other at least by menu, possibly by semantic, syntactic, temporal, concepts, content or other relationships. You need to discover it by using the OEE relationship taxonomy and if necessary class categorization in a similar manner." '
         '(the owner, relayed by the coordinator, Thursday 2026-10-22 01:24 Istanbul)')
OEE_DOCS = [("One meaning, one term (BP-D61)", "/home/claude/Ontologies/oe-method/04-documentation/OE_Operating_Discipline_v2_33_0.md", "section 'One meaning, one term (BP-D61, v2.27.0)', rules S1 to S6: same meaning is proved, same use (domain and range), the survivor, the merge is one change (the other name becomes a label, the retirement is a link), the detector"),
            ("Relationship taxonomy research", "/home/claude/Ontologies/oe-method/04-documentation/RELATIONSHIP_TAXONOMY_RESEARCH_v1_11_0.md", "read sections 4 (construction method BP-D58), 5 (the missing-link families, BP-D57) and 6 (class kinds, BP-D59) first"),
            ("OE governance A-Box", "/home/claude/Ontologies/oe-method/09-governance/oegov_abox_v1_36_0.ttl", "the kb:RelationshipCategory_* individuals (semantic, syntactic, temporal, containment and membership, ordering and sequence, succession and transformation, characterization, association, and others) and the class kinds"),
            ("OE governance T-Box", "/home/claude/Ontologies/oe-method/09-governance/oegov_tbox_v1_15_0.ttl", "kb:hasRelationshipCategory (on a property) and kb:hasClassKind (on a class)"),
            ("Missing-link discovery", "/home/claude/Ontologies/repo-tooling/oe_link_discovery_v1_1_0.py", "run it on the chapter's domain T-Box and A-Box pair; it found only the syntactic input/output pair on chapters 10 and 11"),
            ("Kind rule check", "/home/claude/Ontologies/repo-tooling/oe_kind_rule_check_v1_1_0.py", "run it on a T-Box that declares class kinds (OE v2.31.0 and v2.32.0 added kind rules and two class kinds)")]
import glob as _g
def _newest(path):   # the committed file of that name with the highest version in its folder (the OE files move on)
    m = re.match(r"(.*_v)\d+_\d+_\d+(\..*)$", path)
    fs = sorted(_g.glob(m.group(1) + "*" + m.group(2)), key=lambda f: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", f)[-1]]) if m else []
    return fs[-1] if fs else path
OEE_DOCS = [(a, _newest(b), c) for a, b, c in OEE_DOCS]
TOOLS = [("Stage 4 gate runner", "08-tooling/sen0401_stage4_gates_v1_1_0.py", "python3 -B 08-tooling/sen0401_stage4_gates_v1_1_0.py NN   (reads the CURRENT RDODI pipeline validator v1.13.0)"),
         ("Lineage chapter check", "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py", "python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Research/ChNN | Deck/ChNN | Page/ChNN   (reads the PINNED validator v1.6.0, /home/claude/eco_pin/rdodi-ecosystem)"),
         ("Page test 9.35.0", "08-tooling/sen0401_page_test_v9_35_0.py", "the page test as committed; do not edit it. Its ERD label features are skipped when the page has no relation between two different sections (NOREL, line 153); they must RUN and PASS (labels after Untangle at least 95 percent of the grid's)"),
         ("Page test 9.34.0", "08-tooling/sen0401_page_test_v9_34_0.py", "the page test as committed; do not edit it"),
         ("Page test runner for the lineage", "08-tooling/sen0401_lineage_page_test_run_v1_2_0.py", "runs the page test on a key-substituted TEST copy (about 9 minutes per run; a flaky main-thread budget failure is run again and every run kept)"),
         ("Page check wrapper", "08-tooling/sen0401_lineage_page_check_v1_0_0.py", "template markers and page test run as the bridge runs them"),
         ("Page template", "08-tooling/course_page_template_v9_51_0.html", "template 9.51.0; markers 'const LBLRE=LBL.map' and 'function edVars()'. The template draws every relation type other than 'mentions' as 'operates on' and fixes three types in the concept map: do not change it"),
         ("Page-data builder (current)", "08-tooling/sen0401_page_data_v2_22_0.py", "reads chx:hasOwner (line 219-227) as 'operates on' and builds the text co-mention 'mentions'; a NEW version reads the section links; do not edit this file"),
         ("Page builder", "08-tooling/sen0401_page_build_v4_14_0.py", "the newest page builder"),
         ("Stage 4 ABox builder", "08-tooling/sen0401_page_abox_build_v2_1_0.py", "builds the Stage 4 page ABox from the newest page; a new file, ABox version = page version"),
         ("Deck match check", "08-tooling/pages_deck_match_verify_v1_0_0.py", "0 'not carried' is required"),
         ("Page link check", "08-tooling/pages_link_verify_v1_0_0.py", "as the precedent commits ran it"),
         ("Research package generators", "08-tooling/sen0401_ch10_rdodi_data_v1_0_1.py", "chapter 10 (chapter 11: the counterpart rdodi_data file in 08-tooling) generates the research package files; a new version is a new file with a new version number")]
PRECEDENT = [("42764b2", "chapter 1 package: how chx:hasOwner is declared (domain T-Box, subproperty of rd:hasOwningConcept) and stated between concept individuals of different sections (domain A-Box)"),
             ("5533071", "chapter 13 page 9.69.0 with page-data builder v2_22_0: the newest builder and the way a page is built from a research version"),
             ("2a20df6", "chapter 10 page 9.77.0 on template 9.51.0 (the page this work replaces; 2 skipped features)"), ("e11eff8", "chapter 11 page 9.77.0 (the page this work replaces; 2 skipped features)"),
             ("48dc4d0", "chapter 10 Stage 4 page ABox v2.0.0: how the Stage 4 page ABox and the chapter checks were recorded")]
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0401_lineage_brief_v1_0_0.py"), encoding="utf-8").read()
_m = re.search(r'RULES = """(.*?)"""', _src, re.S)   # the rules of an executor of version 1.0.0, read as text (importing that file would run it)
RULES = _m.group(1) + """
- THE FORM TO ADD (ruling G134: links, not text; the owner's answer): relationships between sections are stated in the chapter RESEARCH as object-property links (an object property between the individuals or classes of two different sections) in the domain A-Box (or the class/T-Box, where the relation is between classes),
  each property DECLARED in the domain T-Box (owl:ObjectProperty with rdfs:domain, rdfs:range, rdfs:label and kb:hasRelationshipCategory taken from the OEE taxonomy), a standard relation REUSED where one says it (rdfs:subPropertyOf of an RDODI or standard property as chx:hasOwner is), class kinds (kb:hasClassKind) where the kind rule needs them.
  A relationship stated only in prose, in a label, a comment or the document text is not a link. Every section of the chapter must be related to at least one other section. If, for some section, no relation of the taxonomy states a relationship, report that section by name: do not invent one.
- ONE MEANING, ONE PROPERTY (the owner's standing rule of 2026-10-21; OE BP-D61, rules S1 to S6, detector family 'duplicate' of oe_link_discovery): real equals are ONE property with several labels (skos:altLabel), never parallel properties. Do not state one property per class pair: the class pair belongs to the link and to the sentence that states it
  (every link carries that sentence as an owl:Axiom rdfs:comment, as the chapter 11 research v1.1.0 does). A meaning that really differs (a different relationship category or a different standard super-property) stays a separate property whose definition says how it differs. Chapter 11 is the model: 6 general properties for 32 links.
  OE v2.33.0 (repo-tooling v1.78.0) also asks that every new object property carries its category (Gate K, oe_kind_coverage); do that. The detector passes properties whose definitions are not word for word equal, so it does not replace your judgment: read the meanings.
- Discover with the taxonomy, do not guess: for each section pair ask the categories one by one (semantic, syntactic, temporal, containment, ordering and succession, characterization, association, ...) and keep the relationship only when the research content states it; record which category each property has."""


def text(g, s, p):
    return " ".join(str(o) for o in g.objects(s, p))


def run(*a):
    return subprocess.run(a, cwd=REPO, capture_output=True, text=True).stdout.strip()


def main():
    out = os.path.join(REPO, sys.argv[1] if len(sys.argv) > 1 else "08-tooling/briefs/iter14"); os.makedirs(out, exist_ok=True)
    src = M.newest(); g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    excl = [x for x in g.objects(E.Scope3, B.hasScopeExclusion)]
    spec = E.Spec3L_L
    index = ["# Executor briefs of iteration 14 (generated from %s)\n" % ver, "The research tasks of iteration 14 are Done (briefs passed earlier). The Verify tasks (%s) have no executor: the builder session runs them through the evidence bridge after the executors report.\n" % ", ".join(VERIFY_TASKS),
             "| Task | Executor session | Can start |", "|---|---|---|"]
    for tid, sess in list(PASSED.items()) + list(SESSIONS.items()):
        if tid in PASSED:
            index.append("| %s | %s | done: brief passed earlier (git 000288a) |" % (tid, sess)); continue
        t = E[tid]
        assert (t, None, None) in g, tid
        note = text(g, t, B.hasAuditNote); title = text(g, t, rdflib.RDFS.label)
        story = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
        chap = re.search(r"Ch1[01]", tid); crits = ([CRIT[chap.group(0)]] if chap else list(CRIT.values())) + EXTRA_CRIT.get(tid, [])
        deps = [str(x).split("#")[1] for x in g.objects(t, B.dependsOn)]
        state = str(g.value(t, B.hasState)).split("#")[1]
        L = ["# Brief for the executor session %s" % sess, "", "Generated from the register %s. Task %s (state in the register: %s)." % (ver, tid, state),
             "Executor session name: **%s**. The register's note on 'work begun' for this task names this session." % sess, "",
             "## Why this work exists (the owner's answer)", OWNER, "",
             "## Rules of an executor", RULES, ""]
        if tid in BLOCKED:
            L += ["## Do not start until", "Task(s) %s Done or reported finished by their executors (the builder session will tell the coordinator). %s" % (", ".join(BLOCKED[tid]), "The builder is checked on chapter 10's new research first." if tid == "TK_SecLinks_PageData" else ""), ""]
        L += ["## The task", "**%s**" % title, "", note, "", "Depends on: %s" % (", ".join(deps) or "nothing"), "",
              "## The story it belongs to", "**%s**" % text(g, story, B.hasTitle), "", "As a %s I want %s so that %s." % (text(g, story, B.asRole), text(g, story, B.wantsCapability), text(g, story, B.soThat)), ""]
        for crit in crits:
            c = E[crit]
            tools = sorted(str(x).split("#")[1] for x in g.objects(c, B.measuredWithTool))
            L += ["## The criterion it satisfies (%s)" % crit, "**%s**" % text(g, c, rdflib.RDFS.label), "", text(g, c, B.hasGherkinText), "",
                  "Measured with (register, G136): %s. Versions: %s" % (", ".join(tools), text(g, c, B.measuredWithVersion)), "", "Satisfied by: %s" % text(g, c, B.satisfiedByArtifact), ""]
        L += ["## The written standard (Spec3L_L)", text(g, spec, B.hasSpecificationText), "", "## What the scope excludes"]
        for x in excl:
            L += ["- **%s**: %s" % (text(g, x, rdflib.RDFS.label), text(g, x, B.excludesConcern))]
        L += ["", "## The OEE relationship taxonomy (read first; OE v2.33.0, repo-tooling v1.78.0)"]
        for name, path, how in OEE_DOCS:
            L.append("- %s: `%s`%s - %s" % (name, path, "" if os.path.exists(path) else " (**not found: search for the committed file of that name**)", how))
        L += ["", "## Tools and gates, by version"]
        for name, path, how in TOOLS:
            L.append("- %s: `%s`%s - %s" % (name, path, "" if os.path.exists(os.path.join(REPO, path)) else " (**not found at this path: search for the committed file of that name before you start**)", how))
        L += ["- Validators: the Stage 4 runner reads the CURRENT RDODI pipeline validator v1.13.0; the chapter checks read the PINNED v1.6.0. Both must pass; they differ, so report each as printed.",
              "- Stage 3.F and the Stage 4 gates for the chapter must stay PASS exactly as for the pages of the previous iteration; no gate, test or threshold is changed.", "", "## Precedents in git (read them first)"]
        for sha, what in PRECEDENT:
            L.append("- `%s` %s%s" % (sha, what, "" if run("git", "cat-file", "-t", sha) == "commit" else " (**commit not found**)"))
        L += ["- `08-tooling/page_jobs_status.md` and `08-tooling/stage4_status.md` describe how the pages were built and checked.", "",
              "## Facts measured on 2026-10-22 (builder session)",
              "Control of 2026-10-22 on chapter 10 research v1.1.0 (commit d4dda4c): 26 properties for 28 links, one per class pair, the same meaning stated more than once (five 'precedes' variants, six requirement variants, five comparison variants, two 'defend against an attack' variants), and no link carries its sentence (0 of 28; chapter 11: 32 of 32). Chapter 11 research v1.1.0 (commit 4a2f709) passes the floor check singular. "
              "Chapters 10 and 11: 17 and 16 sections, 0 relations between two different sections in the page data; the research states none (the domain T-Box holds subclass links inside sections and disjointness; the domain A-Box holds only the I/O examples). The page test 9.35.0 therefore skips two ERD label features on each page. "
              "Chapters 1 to 7 are linked by the builder's text co-mention ('mentions', 1,644 relations) and by a few chx:hasOwner links ('operates on', 39 relations); that is not the form asked of this work. The text co-mention does not arise in chapters 10 and 11.",
              "The pages of the previous iteration (9.77.0) pass all five elements of AC3T_Ch10 / AC3T_Ch11 except element 3 (ERD labels); the new pages must pass all five.", ""]
        open(os.path.join(out, "BRIEF_%s.md" % tid), "w", encoding="utf-8").write("\n".join(L))
        index.append("| %s | %s | %s |" % (tid, sess, "no, after %s" % ", ".join(BLOCKED[tid]) if tid in BLOCKED else "yes"))
    open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8").write("\n".join(index) + "\n")
    print(out, len(SESSIONS), "briefs from", ver)


main()
