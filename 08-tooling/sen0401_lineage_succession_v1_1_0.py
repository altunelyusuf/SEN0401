#!/usr/bin/env python3
"""sen0401_lineage_succession v1_1_0 (1.1.0: calls the successor stages 1.1.0; otherwise 1.0.0 unchanged) - records, in NEW versions of the SEN0401 slides lineage register, the route for work that was finished before it was
planned (backlog-roadmap-framework ruling G105, 2026-10-12): out-scope first, close the finished lineage, a successor under the same mission takes the out-scoped
work in. One call, one new file, one event; the caller commits it alone. Ported from sen0414_lineage_outscope_v1_1_0 with SEN0401's namespace and facts.

Usage: sen0401_lineage_succession_v1_0_0.py EVENT [ARGS]
EVENT: declare | close | mission | scope | goal | objective | backlog PREV_COMMIT FACTS.json BRIDGE_OUT.ttl | fill STAGE HASH
Nothing is placed in a file that was not computed or read here: the out-scoped items are read from the register (every story, epic and initiative not Done), stage
digests come from the framework's own backlog_pipeline_verify (state_digest), times from the clock (UTC), commits from git, finish dates and hashes from the FACTS
file that sen0401_lineage_git_facts reads out of git and the files themselves. Older register files are never opened for writing.
SEN0401_LINEAGE_DIR may point at a scratch copy of 07-lineage (used to rehearse; never for a committed version).
"""
__version__ = "1.1.0"
import datetime, glob, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.environ.get("SEN0401_LINEAGE_DIR", os.path.join(REPO, "07-lineage"))
FW = "/home/claude/Ontologies/backlog-roadmap-framework"
BASE = "http://example.org/sen0401-slides-lineage"
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace(BASE + "#")
ADMIT = [5, 6, 7]                    # chapters built before they were planned
REMAIN = list(range(8, 15))          # chapters not built
KINDS = ("Deck", "Research", "Page")
ADMIT_STORIES = ["ST_%s_Ch%02d" % (k, n) for n in ADMIT for k in KINDS]
REMAIN_STORIES = ["ST_%s_Ch%02d" % (k, n) for n in REMAIN for k in KINDS]
OUT_STORIES = ADMIT_STORIES + REMAIN_STORIES
CONTAINERS = ["EP_Deck", "EP_Research", "EP_Page", "Init_Slides"]


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]


def newest():
    return sorted(glob.glob(os.path.join(LIN, "sen0401_slides_lineage_v*.ttl")), key=ver)[-1]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def next_version(src):
    v = ver(src)
    return "%d.%d.0" % (v[0], v[1] + 1), "%d.%d.%d" % tuple(v)


def write_new(src, text, nxt, cur, comment):
    t = re.sub(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(cur),
               'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, BASE, nxt, BASE, cur), text, count=1)
    assert t != text, "header not found"
    ident = 'dcterms:identifier "sen0401_slides_lineage"'
    cm = 'rdfs:comment "%s (%s): %s"@en' % (nxt, now()[:10], esc(comment))
    if ident + " ;" in t:
        t2 = t.replace(ident + " ;", ident + " ;\n    " + cm + " ;", 1)
    else:                              # the header still ends at the identifier (as in 0.22.0): the comment becomes its last statement
        t2 = t.replace(ident + " .", ident + " ;\n    " + cm + " .", 1)
    assert t2 != t, "header comment not placed"
    out = os.path.join(LIN, "sen0401_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    assert not os.path.exists(out), out
    rdflib.Graph().parse(data=t2, format="turtle")
    open(out, "w", encoding="utf-8").write(t2)
    return out


def ids(names):
    return ", ".join("ex:" + n for n in names)


def open_items(t):
    """Every story, epic and initiative of the register that is not Done - read from the register, not listed by hand."""
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    out = []
    for cls in (B.Story, B.Epic, B.Initiative):
        for s in g.subjects(rdflib.RDF.type, cls):
            if (s, B.hasState, B.Done) not in g and str(s).startswith(str(EX)):
                out.append(str(s).split("#")[-1])
    return sorted(out)


# ---------------------------------------------------------------- events
def ev_declare(t):
    """Closure commit 1: the PartialScopeDeclaration, on the live lineage. Drops the asserted state of the register's root container, which the rules derive
    from its members (R1): with the unfinished work out-scoped the derived state is Done, and a container whose asserted state disagrees is refused."""
    out = open_items(t)
    assert sorted(out) == sorted(OUT_STORIES + CONTAINERS), "the register's open items are not the ones this tool was written for: %s" % out
    blk = ('\nex:Gap_OutScope_Ch05_14 a backlog:PartialScopeDeclaration ;\n'
           '    rdfs:label "Out-scoping of the work of this lineage that is not finished"@en ;\n'
           '    backlog:declaresGapFor ex:Lineage ; backlog:decidedBy backlog:Owner ;\n'
           '    backlog:outScopes %s ;\n'
           '    backlog:describesUncoveredScope "The deck, research and page stories of chapters 5 to 14 (30 stories) are not Done in this register. Chapters 5, 6 and 7 exist in the course repository but were built outside this register: their stories read Proposed, were never planned, started or recorded here, and recording them Done inside this lineage would be backfilling closed work that was never planned (G23, G105). Chapters 8 to 14 (21 stories) are not built at all. The three epics and the initiative that group the stories are open while any of those stories is open. All of them leave this lineage unchanged and unfinished, so that this lineage closes with no unfinished work inside it; the successor lineage under the same mission takes them in: chapters 5 to 7 by admission with their real finish dates from git and evidence run again, chapters 8 to 14 by admission and ordinary planning. The route is the owner\'s rule of 2026-10-12 (framework ruling G105: closing unfinished work is not allowed; out-scope it first, close the finished lineage, a successor takes it in), applied to SEN0401 on the instruction given to the course session on 2026-10-14; the owner confirms it by accepting this record." .\n') % ids(sorted(out))
    old = "    backlog:hasState backlog:InProgress ; backlog:producedByStage ex:Out_Backlog ;"
    assert old in t
    t = t.replace(old, "    backlog:producedByStage ex:Out_Backlog ;", 1)
    return t + blk, "the lineage's unfinished work is out-scoped by an owner-rule PartialScopeDeclaration (30 stories of chapters 5-14, three epics, one initiative); the root container's asserted state is dropped because the rules derive it."


def ev_close(t):
    """Closure commit 2: the lineage is Achieved on its finished scope; the succession under the same mission opens the successor lineage."""
    a = 'backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 1 ; backlog:lineageArchived false ;\n    backlog:hasLineageStatus backlog:LS_InProgress ;'
    assert a in t
    t = t.replace(a, a.replace("LS_InProgress", "LS_Achieved"), 1)
    blk = ('\nex:Lineage2 a backlog:Lineage ;\n    rdfs:label "Second lineage run for the SEN0401 decks: the work finished before it was planned, and the chapters still to build"@en ;\n'
           '    backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 2 ; backlog:lineageArchived false ;\n'
           '    backlog:adoptsObligationSet backlog:OS_SDLC_v2 ; backlog:adoptionRecordedAtOpen true .\n'
           '\nex:Succession_Ch05_14 a backlog:LineageSuccession ;\n    rdfs:label "Succession that takes in the out-scoped work of chapters 5 to 14"@en ;\n'
           '    backlog:succeedsLineage ex:Lineage ; backlog:successorLineage ex:Lineage2 ;\n    backlog:resolvesGap ex:Gap_OutScope_Ch05_14 ;\n'
           '    backlog:decidedBy backlog:Owner ;\n'
           '    backlog:successionRationale "The first lineage planned and finished chapters 1 to 4 and the supplementary Numbers page, each with a planning event before its work and evidence after it. Chapters 5 to 7 were built, committed and pushed before they were planned, so the first lineage can neither record them Done (that would add planning events after the work and move finished-late items) nor close with them still Proposed (closing unfinished work is not allowed); chapters 8 to 14 are not built. Restarting it would retract five correct stage outputs and answer a bypass that the order check does not find. The unfinished and unrecorded work was therefore out-scoped in the previous event, this lineage closes complete on what it finished, and a successor under the same mission opens with the Scope of admitting the finished chapters 5 to 7, recorded now with their real finish dates from git, and of building chapters 8 to 14 in the ordinary way. Cost of waiting: the register keeps stating Proposed for finished work and cannot plan chapter 8 honestly; cost of acting: one succession, five stage commits, and evidence run again for nine items; enforcement value forgone: none, the chain of the first lineage stays untouched." .\n')
    return t + blk, "the lineage is Achieved on its finished scope; the succession ex:Succession_Ch05_14 under the same mission opens the successor lineage ex:Lineage2 and resolves the out-scoping declaration."


EVENTS = {"declare": ev_declare, "close": ev_close}


def main():
    ev = sys.argv[1]
    src = newest()
    t = open(src, encoding="utf-8").read()
    nxt, cur = next_version(src)
    if ev in EVENTS:
        nt, comment = EVENTS[ev](t)
    else:
        import sen0401_lineage_successor_stages_v1_1_0 as stg
        nt, comment = stg.run(ev, t, sys.argv[2:], sys.modules[__name__])
    out = write_new(src, nt, nxt, cur, comment)
    print(os.path.basename(out))


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
