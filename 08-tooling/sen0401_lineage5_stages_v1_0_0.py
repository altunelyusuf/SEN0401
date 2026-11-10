#!/usr/bin/env python3
"""sen0401_lineage5_stages v1_0_0 - the five stage events (Mission, Scope, Goal, Objective, Backlog) of ex:Lineage5, opened by
sen0401_lineage_succession5_v1_0_0.py close. One stage per call, one commit per call (the caller commits between calls and passes the real
commit hash into the next). Digest comes from the framework's own backlog_pipeline_verify.state_digest (table auto-matches what the register's
rule sets declare - RS_DigestTable_v5 is adopted here, same as the rest of the register). Scope: admits chapter 7 and 8 production (deck+page,
each already built and verified this week, finished before this lineage existed to plan it - backfilled with real git dates/hashes and a FRESH
re-run of the deck checker today, not a remembered result) and carries in, unchanged, the 161 items ex:Lineage3 out-scoped (reassigned from
Out3_Backlog's admission to Out5_Backlog's - no new evidence manufactured for them, they stay exactly as open as they were).

Usage: sen0401_lineage5_stages_v1_0_0.py mission|scope|goal|objective|backlog PREV_COMMIT
"""
__version__ = "1.0.0"
import datetime, glob, importlib.util, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
FW = "/home/claude/Ontologies/backlog-roadmap-framework"
BASE = "http://example.org/sen0401-slides-lineage"
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace(BASE + "#")
STAGES = ["Mission", "Scope", "Goal", "Objective", "Backlog"]
GAP = "ex:Gap_OutScope_Lineage3"
CLAUSE = "Every SEN0401 lecture teaches what the third edition of Mastering Bitcoin teaches"


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


def header_version(text):
    m = re.search(r'owl:versionInfo "([\d.]+)" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;', text)
    assert m, "no owl:versionInfo header found"
    return m.group(1)


def write_new(src, text, nxt, cur, comment):
    hv = header_version(text)
    assert hv == cur, "header (%s) and filename (%s) disagree - resync first" % (hv, cur)
    pat = re.compile(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(hv))
    repl = 'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, BASE, nxt, BASE, cur)
    t, n = pat.subn(repl, text, count=1)
    assert n == 1, "header not found"
    ident = 'dcterms:identifier "sen0401_slides_lineage"'
    cm = 'rdfs:comment "%s (%s): %s"@en' % (nxt, now()[:10], esc(comment))
    if ident + " ;" in t:
        t2 = t.replace(ident + " ;", ident + " ;\n    " + cm + " ;", 1)
    else:
        t2 = t.replace(ident + " .", ident + " ;\n    " + cm + " .", 1)
    assert t2 != t, "header comment not placed"
    out = os.path.join(LIN, "sen0401_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    assert not os.path.exists(out), out
    rdflib.Graph().parse(data=t2, format="turtle")
    open(out, "w", encoding="utf-8").write(t2)
    return out


def _pv():
    spec = importlib.util.spec_from_file_location("pv", FW + "/03-tooling/backlog_pipeline_verify_v1_15_0.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    tb = sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"))[-1]
    m.STAGE_TYPES = m._load_stage_types(tb, table="v5")
    return m


def digest(text, stage):
    g = rdflib.Graph(); g.parse(data=text, format="turtle")
    return _pv().state_digest(g, "Stage_" + stage, EX.Lineage5)


def output(text, stage):
    i = STAGES.index(stage)
    consumes = ("\n    backlog:consumesOutput ex:Out5_%s ;" % STAGES[i - 1]) if i else ""
    return ('\nex:Out5_%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the fifth lineage"@en ;\n    backlog:belongsToLineage ex:Lineage5 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;%s\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, digest(text, stage))


def fill_previous(text, stage, commit):
    pat = re.compile(r'(ex:Out5_%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % stage, re.S)
    assert pat.search(text), "no PENDING on Out5_" + stage
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, text, count=1)


def set_status(text, status):
    pat = re.compile(r'(ex:Lineage5 a backlog:Lineage ;.*?)(backlog:hasLineageStatus backlog:\w+ ;\s*)?(backlog:adoptsObligationSet)', re.S)
    m = pat.search(text); assert m
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:%s ;\n    " % status + m.group(3) + text[m.end():]


# ---------------------------------------------------------------- stage content
def mission_block():
    return ('\nex:Lineage5 backlog:lineageForMission ex:Mission .\n'
            '')  # Mission already exists and is unchanged; the successor's Mission-stage output just witnesses it (no new Mission individual)


def scope_block():
    return '''
ex:Area5_Ch0708 a backlog:ScopeArea ; rdfs:label "Chapters 7 and 8 produced and verified this week"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:areaLocation "03-materials/ch07, ch08 and their page/ subfolders; checks in 08-tooling" ;
    backlog:areaMeasure "2 chapters, each a deck and a page, recorded Done with real finish dates from git and a fresh deck-check run" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Area5_Carried a backlog:ScopeArea ; rdfs:label "The open work of the third lineage, carried unchanged"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:areaLocation "07-lineage (this register)" ;
    backlog:areaMeasure "161 items (stories, tasks, epics, one initiative) admitted open, with an executor, to be finished, ruled on or planned in the ordinary way" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del5_Ch0708 a backlog:ScopeDeliverable ; rdfs:label "The chapter 7 and 8 deck and page recorded Done"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:derivesFromMissionClause "%(c)s"^^xsd:string ;
    backlog:hasDeliverableText "The decks and pages of chapters 7 and 8 are recorded Done, each with its real finish date from git and a fresh re-run of the deck standard check (D1-D12, all PASS on both); the page's 5N1K-hidden-from-audience assertion was verified on both this week, the rest of that test suite did not finish end-to-end in this sandbox (an unrelated environment gap, disclosed, not claimed as run)." ;
    backlog:deliverableForArea ex:Area5_Ch0708 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del5_Carried a backlog:ScopeDeliverable ; rdfs:label "The open work of the third lineage carried in unchanged"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:derivesFromMissionClause "%(c)s"^^xsd:string ;
    backlog:hasDeliverableText "The 161 open items of the third lineage (chapters 1-6 deck/page/teach rebuild, the chapter 8/11 page-measure remnants, the exam-paper V6/V7 story chain) are admitted open, unchanged, each with an executor, to be finished, ruled on, or planned (chapters 9-10 next, per the owner's direction) in the ordinary way." ;
    backlog:deliverableForArea ex:Area5_Carried ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Excl5_NoRebuild a backlog:ScopeExclusion ; rdfs:label "The admission rebuilds nothing"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:excludesConcern "Any change to the chapter 7/8 deck or page made in order to admit them: they enter this register exactly as they stand in the course repository." ;
    backlog:hasExclusionRationale "Chapters 7 and 8 were built, verified and committed before this lineage existed to plan them. Recording them records what happened; it does not redo it." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .
ex:Scope5 a backlog:ScopeStatement ; rdfs:label "Admit chapter 7/8 production as finished; carry the open work of the third lineage"@en ;
    backlog:belongsToLineage ex:Lineage5 ; backlog:scopeForMission ex:Mission ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:scopeCompletionState backlog:Proposed ;
    backlog:hasScopeStatementText "IN: (1) the admission of the chapter 7 and 8 deck and page, built and verified this week before this lineage existed, recorded Done with real dates from git and a fresh deck-check run; (2) the 161 open items of the third lineage, carried in unchanged and with an executor. OUT: rebuilding either chapter to admit it; planning chapters 9-14 or the chapter 1-6 retrofit beyond admitting them open (that planning is this lineage's own next ordinary work, through change management, not re-opening a closed lineage)." ;
    backlog:coversArea ex:Area5_Ch0708, ex:Area5_Carried ;
    backlog:hasScopeExclusion ex:Excl5_NoRebuild ;
    backlog:producedByStage ex:Out5_Scope ;
    backlog:requiresDeliverable ex:Del5_Ch0708, ex:Del5_Carried .
ex:Blueprint5 a backlog:Blueprint ; rdfs:label "What the chapter 7/8 admission and the carried work are about"@en ;
    backlog:belongsToLineage ex:Lineage5 ; backlog:blueprintFor ex:Scope5 ; backlog:hasDomainEntity ex:DE3_Deck, ex:DE3_InteractivePage .
''' % {"c": CLAUSE}


GOALS5 = [
    ("G5_Ch0708Done", "Chapter 7 and 8 production is recorded Done with real, re-verified evidence", "Facing_Mission", "GoalOrigin_New", "Area5_Ch0708"),
    ("G5_DeckStandardMet", "Both decks pass the current deck standard check (D1-D12) when re-run, not merely remembered as passing", "Facing_Scope", "GoalOrigin_New", "Area5_Ch0708"),
    ("G5_CarriedWorkVisible", "The 161 carried items of the third lineage stay visible and open, none silently dropped or re-scoped", "Facing_Containment", "GoalOrigin_Carried", "Area5_Carried"),
]


def goal_block():
    L = []
    for i, label, f, origin, area in GOALS5:
        gap = ("\n    backlog:goalAnswersGap %s ;" % GAP) if origin == "GoalOrigin_Carried" else ""
        L.append('''
ex:%(i)s a backlog:Goal ; rdfs:label "%(label)s"@en ; backlog:belongsToLineage ex:Lineage5 ; backlog:derivesFromScope ex:Scope5 ; backlog:goalCoversArea ex:%(area)s ;%(gap)s
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:%(f)s ; backlog:hasGoalOrigin backlog:%(origin)s ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale "Derived from the scope of the fifth lineage: chapters 7/8 were built outside any registered lineage and are admitted now with real evidence; the third lineage's unfinished work was out-scoped by ex:Gap_OutScope_Lineage3 and this lineage is its successor." ;
    backlog:producedByStage ex:Out5_Goal .
''' % dict(i=i, label=label, area=area, gap=gap, f=f, origin=origin))
    return "".join(L)


OBJS5 = [
    ("Obj5_Ch0708Done", "G5_Ch0708Done", "Met5_Ch0708Done", "chapter 7/8 deck+page stories (4) recorded Done", 0, 4, "Dir_Increase"),
    ("Obj5_DeckStdPass", "G5_DeckStandardMet", "Met5_DeckStdPass", "deck-standard elements (D1-D12) passing on a fresh run of both chapters' decks", 0, 24, "Dir_Increase"),
]


def objective_block(n_carried, now_iso):
    L = []
    objs = OBJS5 + [("Obj5_CarriedVisible", "G5_CarriedWorkVisible", "Met5_CarriedVisible", "carried items admitted open by this lineage's Backlog output", 0, n_carried, "Dir_Increase")]
    for i, g, m, what, b, tg, d in objs:
        gap = "\n    backlog:resolvesPartialScope %s ;" % GAP if i == "Obj5_CarriedVisible" else ""
        L.append('''
ex:%(i)s a backlog:Objective ; rdfs:label "%(what)s: from %(b)d to %(tg)d"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:contributesToGoal ex:%(g)s ; backlog:fillsScope ex:Scope5 ; backlog:hasSuccessMetric ex:%(m)s ;%(gap)s
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %(what)s, read from this register." ;
    backlog:hasBaselineValue "%(b)d"^^xsd:decimal ; backlog:hasTargetValue "%(tg)d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%(d)s ;
    backlog:hasCheckpoint ex:CP5_%(i)s ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out5_Objective .
ex:%(m)s a backlog:Metric ; rdfs:label "%(what)s"@en ; backlog:belongsToLineage ex:Lineage5 .
ex:CP5_%(i)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the Backlog stage output of this lineage is closed"@en ;
    backlog:checkpointCondition "Taken after the Backlog stage output of this lineage is closed." ;
    backlog:expectedValue "%(tg)d"^^xsd:decimal .
ex:Obs50_%(i)s a backlog:MetricObservation ; rdfs:label "Baseline, before this lineage's Backlog stage closes"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(i)s ; backlog:hasObservedValue "%(b)d"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Read from this register at the Objective stage of the fifth lineage: nothing has been admitted by this lineage's Backlog output yet." .
''' % dict(i=i, g=g, m=m, what=what, b=b, tg=tg, d=d, gap=gap, now=now_iso))
    return "".join(L)


# ---------------------------------------------------------------- Backlog stage
AC_BLOCK5 = '''
ex:AC5_Ch0708 a backlog:AcceptanceCriterion ; rdfs:label "A chapter 7/8 deck or page is accepted when its real finish date and file hash are recorded and, for the deck, the deck standard check passes on a fresh run"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:hasGherkinText "Given a deck or page built this week outside this register, when its finish date is taken from git and its file hashed, and for a deck the standard check (D1-D12) is run again, then it is admitted Done with that evidence; a chapter whose check fails would be admitted failing and named, not Done." ;
    backlog:satisfiedByArtifact "the deck-standard-check output and the file hash, recorded in this register" .
'''

EXEC5 = "ex:Executor_ClaudeCodeSession"
DECK07 = dict(path="03-materials/ch07/SEN0401_Ch07_AuthorizationAuthentication_3e_v2_3_0.pptx",
              sha="3ebb32bf578a67bd323e4e2a2b34de5c525894e1ae9cde41ffdb2f2e3678541b", commit="0278076",
              dt="2026-11-09T10:40:35")
DECK08 = dict(path="03-materials/ch08/SEN0401_Ch08_DigitalSignatures_3e_v2_1_0.pptx",
              sha="f8e7d71e5fce11221fc1451379890467512abdf4e1b19a3db35309afc4372464", commit="0278076",
              dt="2026-11-09T10:40:35")
PAGE07 = dict(path="03-materials/ch07/page/sen0401_ch07_page_v9_89_0.html",
              sha="2f65857ce7ba95c40f0598b6a4552d83dbc79765f4547b9c96d002659f9e24b9", commit="0278076",
              dt="2026-11-09T10:40:35")
PAGE08 = dict(path="03-materials/ch08/page/sen0401_ch08_page_v9_90_0.html",
              sha="5e06bec562a7316565aa89dd0305327fa6a42645e664ee18cad7611f6bcb725c", commit="b1b6eee",
              dt="2026-11-09T15:36:13")
START = "2026-11-08T18:04:55"  # 6040f74, Lineage 4 drafts opened (UTC, +03:00 source 21:04:55)


def _story(kind, ch, f, aud):
    sid = "ST_%s_Ch%s_Lineage5" % (kind, ch)
    ev = "Ev5_%s_Ch%s" % (kind, ch)
    return ('\nex:%(sid)s a backlog:Story ; rdfs:label "%(kind)s of chapter %(ch)s, admitted as pre-lineage finished work"@en ;\n'
            '    backlog:hasIdentifier "%(sid)s" ; backlog:hasTitle "Chapter %(ch)s %(kindlow)s, built before this lineage existed" ;\n'
            '    backlog:belongsToLineage ex:Lineage5 ; backlog:preLineageItem true ; backlog:admittedByOutput ex:Out5_Backlog ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
            '    backlog:asRole "SEN0401 student and instructor" ; backlog:wantsCapability "the %(kindlow)s of chapter %(ch)s, built to the current deck/page standard" ;\n'
            '    backlog:soThat "chapter %(ch)s is taught from material that meets the current 5N1K-hidden-from-audience and deck-standard rulings" ;\n'
            '    backlog:satisfiesDeliverable ex:Del5_Ch0708 ; backlog:pursuesObjective ex:Obj5_Ch0708Done ; backlog:hasAcceptanceCriterion ex:AC5_Ch0708 ;\n'
            '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:responsible %(exec)s ;\n'
            '    backlog:hasState backlog:Done ; backlog:startedAt "%(start)s"^^xsd:dateTime ; backlog:finishedAt "%(fin)s"^^xsd:dateTime ;\n'
            '    backlog:lastAuditedAt "%(fin)s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n'
            '    backlog:hasEvidence ex:%(ev)s ;\n'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Admitted as finished: this story was never planned, so it is not scored." ;\n'
            '    backlog:hasAuditNote "Built and committed before this lineage existed (git commit %(commit)s, %(dt)s local). %(note)s" .\n'
            'ex:%(ev)s a backlog:ArtifactEvidence ; rdfs:label "%(path)s, committed %(dt)s"@en ; backlog:belongsToLineage ex:Lineage5 ; backlog:attestsCriterion ex:AC5_Ch0708 ;\n'
            '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%(path)s" ; backlog:hasArtifactSHA256 "%(sha)s" ;\n'
            '    backlog:hasVerificationMethod "%(method)s" ; backlog:verifiedByTool "%(tool)s" ; backlog:verifiedAt "%(aud)s"^^xsd:dateTime .\n'
            ) % dict(sid=sid, kind=kind, kindlow=kind.lower(), ch=ch, exec=EXEC5, start=START, fin=f["dt"], ev=ev,
                      commit=f["commit"], dt=f["dt"], path=f["path"], sha=f["sha"], aud=aud,
                      note=("Deck standard check v2.0.0 re-run fresh today (not a remembered result): D1-D12 all PASS, 0 of 12 failing." if kind == "Deck"
                            else "Interactive page: the 5N1K-hidden-from-audience assertion (sen0401_page_test_v9_39_0.py) was verified on this page this week; the rest of that suite did not finish end-to-end in this sandbox, an unrelated environment gap, disclosed at the time and not claimed as run."),
                      method=("Fresh re-run, this session, of sen0401_deck_standard_check_v2_0_0.py: SUMMARY PASS=12 FAIL=0 NOT_MEASURED=0." if kind == "Deck"
                              else "5N1K fact-row assertion of sen0401_page_test_v9_39_0.py, run this week and recorded in 08-tooling/lineage_status.md; full suite incomplete (environment gap, disclosed)."),
                      tool=("sen0401_deck_standard_check_v2_0_0.py" if kind == "Deck" else "sen0401_page_test_v9_39_0.py (partial) + direct grep for the three label tags (0 occurrences)"))


def backlog_stage(t, prev_commit, now_iso):
    t = fill_previous(t, "Objective", prev_commit)
    t = set_status(t, "LS_Backlogged")
    out = []
    for kind, ch in (("Deck", "Deck"),):
        pass
    aud = now_iso
    add = [AC_BLOCK5,
           _story("Deck", "07", DECK07, aud), _story("Page", "07", PAGE07, aud),
           _story("Deck", "08", DECK08, aud), _story("Page", "08", PAGE08, aud)]
    t += "".join(add)
    for o in ("Obj5_Ch0708Done",):
        t += "ex:%s backlog:metricMovableBy ex:ST_Deck_Ch07_Lineage5, ex:ST_Page_Ch07_Lineage5, ex:ST_Deck_Ch08_Lineage5, ex:ST_Page_Ch08_Lineage5 .\n" % o
    for o in ("Obj5_DeckStdPass",):
        t += "ex:%s backlog:metricMovableBy ex:ST_Deck_Ch07_Lineage5, ex:ST_Deck_Ch08_Lineage5 .\n" % o
    # carry the 161 items: reassign admittedByOutput from Out3_Backlog to Out5_Backlog, read from the register (not listed by hand)
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    carried = []
    for cls in (B.Story, B.Epic, B.Initiative, B.ExecutionTask):
        for s in g.subjects(rdflib.RDF.type, cls):
            if (s, B.belongsToLineage, EX.Lineage3) in g and (s, B.hasState, B.Done) not in g and (s, B.hasState, B.Cancelled) not in g:
                carried.append(str(s).split("#")[-1])
    carried = sorted(set(carried))
    n = 0
    not_found = []
    for name in carried:
        # the real admittedByOutput target carries a stage-revision suffix (e.g. Out3_BacklogR62), discovered by
        # inspection after this script's first, word-boundary-free attempt silently produced a dangling
        # "Out5_BacklogR62" reference (matched "Out3_Backlog" as a PREFIX of "Out3_BacklogR62" and left the
        # suffix dangling off the replacement) - caught before committing, not shipped. \b enforces the real token.
        pat = re.compile(r"(ex:%s a backlog:\w+ ;.*?)backlog:admittedByOutput ex:Out3_Backlog\w*\b" % re.escape(name), re.S)
        t2, k = pat.subn(lambda m: m.group(1) + "backlog:preLineageItem true ; backlog:admittedByOutput ex:Out5_Backlog", t, count=1)
        if k:
            t = t2; n += 1
        else:
            not_found.append(name)
    t += "ex:Obj5_CarriedVisible backlog:metricMovableBy %s .\n" % ", ".join("ex:" + x for x in carried) if carried else ""
    assert not not_found, "items not re-admitted (admittedByOutput pattern did not match): %s" % not_found
    return t + output(t, "Backlog"), ("the fifth lineage's Backlog stage closes: 4 chapter 7/8 stories admitted Done with real evidence "
                                       "(deck standard check re-run fresh, PASS on both; page 5N1K assertion verified, full suite incomplete and disclosed); "
                                       "all %d of the third lineage's open items re-admitted (admittedByOutput moved from ex:Out3_BacklogR62 to ex:Out5_Backlog, preLineageItem set true), read from the register, not listed by hand." % n)


EVENTS_SIMPLE = {"mission": (mission_block, "Mission"), "scope": (scope_block, "Scope"), "goal": (goal_block, "Goal")}


def main():
    ev = sys.argv[1]; prev = sys.argv[2] if len(sys.argv) > 2 else None
    src = newest(); t = open(src, encoding="utf-8").read(); nxt, cur = next_version(src)
    now_iso = now()
    if ev == "mission":
        t = t + mission_block() + output(t + mission_block(), "Mission")
        comment = "fifth lineage, Mission stage closed (Mission unchanged, re-affirmed)."
    elif ev == "scope":
        t = fill_previous(t, "Mission", prev); t = set_status(t, "LS_Scoped"); t2 = t + scope_block()
        t = t2 + output(t2, "Scope")
        comment = "fifth lineage, Scope stage closed (admit chapter 7/8 production; carry the open work of the third lineage)."
    elif ev == "goal":
        t = fill_previous(t, "Scope", prev); t = set_status(t, "LS_Goaled"); t2 = t + goal_block()
        t = t2 + output(t2, "Goal")
        comment = "fifth lineage, Goal stage closed."
    elif ev == "objective":
        t = fill_previous(t, "Goal", prev); t = set_status(t, "LS_Objectived")
        g = rdflib.Graph(); g.parse(data=t, format="turtle")
        n_carried = sum(1 for cls in (B.Story, B.Epic, B.Initiative, B.ExecutionTask) for s in g.subjects(rdflib.RDF.type, cls)
                         if (s, B.belongsToLineage, EX.Lineage3) in g and (s, B.hasState, B.Done) not in g and (s, B.hasState, B.Cancelled) not in g)
        t2 = t + objective_block(n_carried, now_iso)
        t = t2 + output(t2, "Objective")
        comment = "fifth lineage, Objective stage closed."
    elif ev == "backlog":
        t, comment = backlog_stage(t, prev, now_iso)
    else:
        raise SystemExit("unknown event " + ev)
    out = write_new(src, t, nxt, cur, comment)
    print(os.path.basename(out))


if __name__ == "__main__":
    main()
