#!/usr/bin/env python3
"""sen0401_lineage_succession5 v1_0_0 - records, in NEW versions of the SEN0401 slides lineage register, the owner-decided route for Lineage3
(route "out-scope, close, succeed", framework ruling G105/2.5c-xxi-n): Lineage3's own unfinished work (every Story/Epic/Initiative/ExecutionTask it
holds that is not Done or Cancelled, read from the register, not listed by hand) is out-scoped by a PartialScopeDeclaration; Lineage3 then closes
Achieved on what it finished; a successor opens under the same Mission. The successor is numbered Lineage5, not Lineage4: ex:Lineage4 already exists
in this register (Mission_Midterm, Abandoned) - lineage ordinals are taken from the live register, never assigned in markdown. This script performs
only the two closure-commit events (declare, close); the successor's five staged stage commits (Mission..Backlog) are a separate, heavier piece of
work (real Ch7/8 evidence synthesis + carrying the out-scoped items) tracked separately, not performed here.

Usage: sen0401_lineage_succession5_v1_0_0.py declare|close
"""
__version__ = "1.0.0"
import datetime, glob, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
BASE = "http://example.org/sen0401-slides-lineage"
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace(BASE + "#")
GAP = "ex:Gap_OutScope_Lineage3"


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]


def newest():
    return sorted(glob.glob(os.path.join(LIN, "sen0401_slides_lineage_v*.ttl")), key=ver)[-1]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def header_version(text):
    m = re.search(r'owl:versionInfo "([\d.]+)" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;', text)
    assert m, "no owl:versionInfo header found"
    return m.group(1)


def next_version(src):
    v = ver(src)
    return "%d.%d.0" % (v[0], v[1] + 1), "%d.%d.%d" % tuple(v)


def write_new(src, text, nxt, cur, comment, resync_note=None):
    """cur is the FILENAME's version; the header's own owl:versionInfo may lag it (found here: it had been frozen at 0.1016.0 since file
    v0_1016_0.ttl while 28 later filename-versioned snapshots - up to v0_1044_0.ttl - were produced without the header ever advancing; this
    repository's git history has only one commit before this week (21f699c, a bulk handover import), so no earlier commit trail exists here
    to show when or why that freeze started - the files themselves, not a traceable edit, are the only evidence available in this environment).
    This call resyncs the header to the real current filename version in the same edit that advances it to nxt, and the resync is stated in the
    version comment, never silently folded in."""
    hv = header_version(text)
    pat = re.compile(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(hv))
    repl = 'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, BASE, nxt, BASE, cur)
    t, n = pat.subn(repl, text, count=1)
    assert n == 1, "header not found"
    if resync_note:
        comment = resync_note + " " + comment
    ident = 'dcterms:identifier "sen0401_slides_lineage"'
    cm = 'rdfs:comment "%s (%s): %s"@en' % (nxt, now()[:10], esc(comment))
    if ident + " ;" in t:
        t2 = t.replace(ident + " ;", ident + " ;\n    " + cm + " ;", 1)
    else:
        t2 = t.replace(ident + " .", ident + " ;\n    " + cm + " .", 1)
    assert t2 != t, "header comment not placed"
    out = os.path.join(LIN, "sen0401_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    assert not os.path.exists(out), out
    rdflib.Graph().parse(data=t2, format="turtle")  # turtle-syntax sanity check only; full SHACL conformance is a separate, not-yet-run step
    open(out, "w", encoding="utf-8").write(t2)
    return out


def open_items(t):
    """Every Story/Epic/Initiative/ExecutionTask belonging to Lineage3 that is not Done or Cancelled - read from the register, not listed by hand."""
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    out = []
    for cls in (B.Story, B.Epic, B.Initiative, B.ExecutionTask):
        for s in g.subjects(rdflib.RDF.type, cls):
            if (s, B.belongsToLineage, EX.Lineage3) in g and (s, B.hasState, B.Done) not in g and (s, B.hasState, B.Cancelled) not in g:
                out.append(str(s).split("#")[-1])
    return sorted(set(out))


def ev_declare(t):
    out = open_items(t)
    assert out, "no open items found under Lineage3 - is this the current register?"
    ids = ", ".join("ex:" + x for x in out)
    blk = ('\n%s a backlog:PartialScopeDeclaration ;\n'
           '    rdfs:label "Out-scoping of the work of the third lineage that is not finished"@en ;\n'
           '    backlog:declaresGapFor ex:Lineage3 ; backlog:decidedBy backlog:Owner ;\n'
           '    backlog:outScopes %s ;\n'
           '    backlog:describesUncoveredScope "Not Done or Cancelled in this register at the time of this declaration and belonging to the third lineage: %d items (stories, tasks, epics and the initiative), spanning the chapter 1-6 deck/page/teach rebuild work, the chapter 8 and 11 page-measure remnants, and the exam-paper (V6/V7) story chain. Markdown closure notes written earlier this week (sen0401_lineage3_closure_narrowing_v1_0_0.md) described this lineage as closed by narrowing; that description was never recorded in this register, which still read LS_InProgress - this declaration and the following close event are the first time that narrowing is actually recorded here. This leaves the third lineage unchanged and unfinished so that it closes with no unfinished work inside it; the successor lineage under the same mission takes the open work in. Ordinal: the next lineage after the third is numbered Lineage5 here, not Lineage4 - ex:Lineage4 already exists in this register for Mission_Midterm (Abandoned) and that ordinal is not free; markdown this week used the name Lineage4 for a different, unregistered piece of work (the chapter 7/8 production charter), which is renumbered to match this register rather than the register being bent to match the markdown. The owner confirms this record by accepting it." .\n'
           ) % (GAP, ids, len(out))
    return t + blk, "the third lineage's unfinished work is out-scoped by an owner-decided PartialScopeDeclaration (%d items: stories, tasks, epics and the initiative)." % len(out)


def ev_close(t):
    a = re.search(r'ex:Lineage3 a backlog:Lineage ;.*?backlog:hasLineageStatus backlog:LS_InProgress', t, re.S)
    assert a, "Lineage3 is not LS_InProgress"
    t = t[:a.start()] + a.group(0).replace("LS_InProgress", "LS_Achieved") + t[a.end():]
    blk = ('\nex:Lineage5 a backlog:Lineage ;\n'
           '    rdfs:label "Fifth lineage for the SEN0401 decks: chapters 7-8 production and the carried-forward open work of the third lineage"@en ;\n'
           '    backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 5 ; backlog:lineageArchived false ;\n'
           '    backlog:adoptsObligationSet backlog:OS_SDLC_v2 ; backlog:adoptionRecordedAtOpen true .\n'
           '\nex:Succession_Lineage3_5 a backlog:LineageSuccession ;\n'
           '    rdfs:label "Succession that takes in the open work of the third lineage"@en ;\n'
           '    backlog:succeedsLineage ex:Lineage3 ; backlog:successorLineage ex:Lineage5 ;\n'
           '    backlog:resolvesGap %s ;\n'
           '    backlog:decidedBy backlog:Owner ;\n'
           '    backlog:successionRationale "The third lineage\'s own Backlog-stage output is closed and digest-verified; new work (chapters 7 and 8 produced and verified this week outside this register, and chapters 9 and 10 planned next) cannot be added to it without moving that digest. Its real unfinished work was therefore out-scoped in the previous event, it closes complete on what it finished (the link passes and whatever else this register already records Done under it), and a successor under the same unchanged Mission opens to take the carried-forward items in and to admit the chapter 7/8 production as pre-lineage finished work with its real evidence. The successor\'s five staged stage commits (Mission, Scope, Goal, Objective, Backlog), each with the framework\'s own digest verification, are a separate, not-yet-performed piece of work: this succession record only declares that Lineage5 is the successor and which gap it resolves, so the open work is not left orphaned while that follow-on work is done. Cost of waiting: markdown keeps describing a closure this register does not record, and chapter 7/8 is unregistered; cost of acting: one succession record now plus five stage commits still owed; enforcement value forgone: none, the chain of the first three lineages stays untouched." .\n'
           ) % GAP
    return t + blk, "the third lineage is Achieved on its finished scope; the succession ex:Succession_Lineage3_5 under the same mission opens the fifth lineage ex:Lineage5 (not Lineage4, already taken) and resolves the out-scoping declaration. The successor's own five staged stage commits are still owed."


EVENTS = {"declare": ev_declare, "close": ev_close}


def main():
    ev = sys.argv[1]
    src = newest()
    t = open(src, encoding="utf-8").read()
    nxt, cur = next_version(src)
    nt, comment = EVENTS[ev](t)
    hv = header_version(t)
    resync = None
    if hv != cur:
        resync = ("Header resync: owl:versionInfo had been frozen at %s since file v%s.ttl while later filename-versioned snapshots were produced up to this file (%s) without it advancing; this repository's git history holds only one commit before this week (21f699c, a bulk handover import), so no earlier commit trail exists here to show when or why - the files are the only evidence available. Resynced to %s now, in the same edit, not silently." % (hv, hv.replace(".", "_"), cur, cur))
    out = write_new(src, nt, nxt, cur, comment, resync)
    print(os.path.basename(out))


if __name__ == "__main__":
    main()
