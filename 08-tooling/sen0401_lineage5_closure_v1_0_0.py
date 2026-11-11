#!/usr/bin/env python3
"""sen0401_lineage5_closure v1_0_0 - closes ex:Lineage5 the way BRSF G105 and the register's own three earlier successions do:
(1) a PartialScopeDeclaration, owner-decided, out-scopes every item of the lineage that is not Done or Cancelled; (2) a ClosureReport
states what was delivered and what is not claimed; (3) the lineage status becomes LS_Achieved in the next version (a LineageSuccession to the successor,
recorded in the successor's Mission commit, is what the validator reads as the exemption for the Achieved claim). The out-scoped list is
computed from the register at run time, never typed. Owner's decision: 2026-11-11 15:22 Istanbul, after the test drive of 14:48."""
import glob, os, re, sys, datetime
import rdflib
sys.path.insert(0, "/tmp/l6")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); LIN = os.path.join(REPO, "07-lineage")
BASE = "http://example.org/sen0401-slides-lineage"; B = rdflib.Namespace("http://example.org/backlog#"); EX = rdflib.Namespace(BASE + "#")
ver = lambda p: [int(v) for v in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
src = sorted(glob.glob(os.path.join(LIN, "sen0401_slides_lineage_v*.ttl")), key=ver)[-1]
t = open(src, encoding="utf-8").read(); g = rdflib.Graph(); g.parse(data=t, format="turtle")
cur = "%d.%d.%d" % tuple(ver(src)); nxt = "%d.%d.0" % (ver(src)[0], ver(src)[1] + 1)
assert str(g.value(EX.Lineage5, B.hasLineageStatus)).endswith("LS_Backlogged"), "Lineage5 is not Backlogged"
open_ = []
for s in set(g.subjects(B.hasState, None)):
    st = [x.split("#")[-1] for x in g.objects(s, B.hasState)]
    if any(x in ("Done", "Cancelled") for x in st): continue
    ln = [x.split("#")[-1] for x in g.objects(s, B.belongsToLineage)]; ad = [x.split("#")[-1] for x in g.objects(s, B.admittedByOutput)]
    if "Lineage5" in ln or any(a.startswith("Out5") for a in ad): open_.append(s)
open_.sort(); n = len(open_); print("out-scoped:", n)
objs = sorted({o for o in g.subjects(B.belongsToLineage, EX.Lineage5) if (o, rdflib.RDF.type, B.Objective) in g})
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
add = '\nex:Gap_OutScope_Lineage5 a backlog:PartialScopeDeclaration ;\n    rdfs:label "Out-scoping of the work of the fifth lineage that is not finished"@en ;\n    backlog:declaresGapFor ex:Lineage5 ; backlog:decidedBy backlog:Owner ;\n'
add += '    backlog:describesUncoveredScope "%s" ;\n' % esc("Not Done or Cancelled in this register at the time of this declaration and belonging to the fifth lineage (its own items and the third lineage's items it carried in): %d items (stories, tasks, epics and the initiative), the same open work the third lineage out-scoped to the fifth: the chapter 1-6 deck/page/teach rebuild work, the chapter 8 and 11 page-measure remnants, the exam work items and the repair items. The owner decided on 2026-11-11 (15:22 Istanbul), after a test drive of the options, that the fifth lineage closes by out-scoping, and that a successor lineage under the same mission takes them in, as G105 rules and as the third lineage's own succession did." % n)
add += '    backlog:outScopes ' + " , ".join("ex:" + str(s).split("#")[-1] for s in open_) + " .\n"
summ = ("Closure report of the fifth lineage, written 2026-11-11. Delivered and recorded Done with evidence: the chapter 7 and 8 deck and page (admitted as finished work with real git dates), and the chapter 9 and 10 deck and page admitted by the lineage's first change cycle. NOT delivered and not claimed: the %d open items above, out-scoped by ex:Gap_OutScope_Lineage5 and taken in by the successor. Disclosed, not repaired here: the framework's current validator reports, against this lineage's Done stories, that a Done item needs a test harness whose completeness was derived and evidence anchored by a test or release (not review evidence alone), that the chapter 9 and 10 items carry no planning event, and that the scope change of the first change cycle (SC1_Ch0910) is missing what it names; the same findings are reported against the stories of every earlier lineage under today's rules, and none is claimed as passed. This report does not set the Mission outcome; that is the owner's act." % n)
add += '\nex:CR5_SEN0401 a backlog:ClosureReport ; rdfs:label "Closure report of the fifth lineage"@en ; backlog:belongsToLineage ex:Lineage5 ; backlog:closesForMission ex:Mission ;\n    backlog:reportGeneratedAt "%s"^^xsd:dateTime ;\n    backlog:hasClosureSummary "%s" ;\n    backlog:reportsOnObjective %s .\n' % (now, esc(summ), " , ".join("ex:" + str(o).split("#")[-1] for o in objs))
t2 = t  # the status flips to LS_Achieved in the successor's Mission commit, where the LineageSuccession that the validator reads as the exemption is recorded
pat = re.compile(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(cur))
t3, k = pat.subn('owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, BASE, nxt, BASE, cur), t2, count=1); assert k == 1
cm = 'rdfs:comment "%s (%s): the fifth lineage is closed on its finished scope: its %d unfinished items are out-scoped by ex:Gap_OutScope_Lineage5, a closure report is recorded, ; the status flips to Achieved in the next version, where the successor lineage and its LineageSuccession are recorded (G105)."@en' % (nxt, now[:10], n)
ident = 'dcterms:identifier "sen0401_slides_lineage"'
t4 = t3.replace(ident + " ;", ident + " ;\n    " + cm + " ;", 1) if ident + " ;" in t3 else t3.replace(ident + " .", ident + " ;\n    " + cm + " .", 1)
assert t4 != t3
out = os.path.join(LIN, "sen0401_slides_lineage_v%s.ttl" % nxt.replace(".", "_")); assert not os.path.exists(out)
t4 += add; rdflib.Graph().parse(data=t4, format="turtle"); open(out, "w", encoding="utf-8").write(t4); print(os.path.basename(out))
