#!/usr/bin/env python3
"""sen0401_lineage5_change1 v1.0.0 - the fifth lineage's first change-management cycle: grows its Scope to admit
chapter 9/10 production (deck+page, built and verified this session before this change existed to plan it - same
shape as chapter 7/8's admission at the lineage's own opening, now done through change management because
ex:Scope5's own OUT clause named chapters 9-14 as this lineage's "own next ordinary work, through change
management, not re-opening a closed lineage").

Events, one per call, one commit between calls (caller commits and passes the real commit hash forward):
  request   - ex:CR1_Ch0910 (ChangeRequest, Direction_Grow, Disp_Pending) + ex:IA1_Ch0910 (ImpactAssessment)
  accept    - moves CR1's disposition to Disp_Accepted (the owner's "Yes, proceed") + ex:SC1_Ch0910 (ScopeChange)
  scope     - revises Scope5 (new Area5_Ch0910 / Del5_Ch0910) -> ex:Out5_ScopeR1 (consumes ex:Out5_Scope)
  goal      - revises Goal (new G5_Ch0910Done / G5_Ch0910DeckStdMet) -> ex:Out5_GoalR1 (consumes ex:Out5_ScopeR1)
  objective - revises Objective (new Obj5_Ch0910Done / Obj5_Ch0910DeckStdPass) -> ex:Out5_ObjectiveR1
  backlog   - admits 4 stories (ch09 deck/page, ch10 deck/page) Done, real evidence -> ex:Out5_BacklogR1

Digest/output mechanics reused as-is from sen0401_lineage5_stages_v1_0_0.py; only the revision-suffixed output
naming and the consumesOutput chain differ (R1 consumes the un-suffixed original, matching this register's own
Out3_BacklogR62-style revision-numbering precedent).

Usage: sen0401_lineage5_change1_v1_0_0.py request|accept|scope|goal|objective|backlog PREV_COMMIT
"""
__version__ = "1.0.0"
import re, sys
import rdflib
import sen0401_lineage5_stages_v1_0_0 as S

B, EX = S.B, S.EX
newest, ver, next_version, header_version, write_new = S.newest, S.ver, S.next_version, S.header_version, S.write_new
now, esc, digest, fill_previous, set_status = S.now, S.esc, S.digest, S.fill_previous, S.set_status
STAGES = S.STAGES
CLAUSE = S.CLAUSE


def output_rev(text, stage, rev, consumes_name):
    """Like S.output() but for a REVISION of an already-closed stage: names it ex:Out5_<Stage>R<rev> and makes it
    consume the named prior output instead of the previous STAGE's output."""
    return ('\nex:Out5_%s a backlog:StageOutput ;\n    rdfs:label "Revision %d of the %s stage of the fifth lineage (change management)"@en ;\n'
            '    backlog:belongsToLineage ex:Lineage5 ;\n    backlog:outputOfStage backlog:Stage_%s ;\n    backlog:consumesOutput ex:%s ;\n'
            '    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n'
            ) % ("%sR%d" % (stage, rev), rev, stage, stage, consumes_name, digest(text, stage))


def fill_previous_named(text, name, commit):
    pat = re.compile(r'(ex:%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % re.escape(name), re.S)
    assert pat.search(text), "no PENDING on " + name
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, text, count=1)


# ---------------------------------------------------------------- request + accept
def request_block():
    return '''
ex:CR1_Ch0910 a backlog:ChangeRequest ; rdfs:label "Grow Scope5 to admit chapter 9/10 production"@en ;
    backlog:belongsToLineage ex:Lineage5 ; backlog:requestsChangeTo ex:Scope5 ; backlog:hasChangeDirection backlog:Direction_Grow ;
    backlog:hasChangeRequestRationale "Chapters 9 and 10 were built and verified this session, the same shape as chapter 7/8's admission at this lineage's opening (deck story slides and pages brought to the current D5 5N1K-hidden-from-audience standard, re-checked fresh, not remembered). ex:Scope5's own text named this future chapter admission explicitly as this lineage's next ordinary work through change management, not a reason to re-open a closed lineage." ;
    backlog:hasDisposition backlog:Disp_Pending ; backlog:decidedBy backlog:Owner .
ex:IA1_Ch0910 a backlog:ImpactAssessment ; rdfs:label "Impact of admitting chapter 9/10 production into Scope5"@en ;
    backlog:belongsToLineage ex:Lineage5 ; backlog:analyzesRequest ex:CR1_Ch0910 ;
    backlog:hasImpactStatement "ex:Lineage5 is the only active lineage in this register (ex:Lineage3 is LS_Achieved and retired to a successor; ex:Lineage4 is an unrelated, already-Abandoned midterm lineage). Growing Scope5 adds two new ScopeAreas and ScopeDeliverables that mirror ex:Area5_Ch0708/ex:Del5_Ch0708 in shape and touch no existing area, goal, objective or story; the 161 carried items and the chapter 7/8 admission are untouched. No concurrently active lineage carries any risk from this change." ;
    backlog:identifiesAffectedLineage ex:Lineage5 .
'''


def accept_block():
    return '''
ex:SC1_Ch0910 a backlog:ScopeChange ; rdfs:label "Chapter 9/10 production admitted into Scope5"@en ;
    backlog:belongsToLineage ex:Lineage5 ; backlog:changeRequestAccepted ex:CR1_Ch0910 ;
    backlog:hasScopeChangeRationale "Owner's direction: complete for chapters 9/10 the same D5 5N1K-hidden-from-audience fix already shipped for chapters 7/8; impact assessed as touching no other active lineage; owner said 'Yes, proceed' to the change-management cycle itself." ;
    backlog:decidedBy backlog:Owner .
'''


def fill_disposition_accepted(text):
    pat = re.compile(r'(ex:CR1_Ch0910 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', re.S)
    assert pat.search(text), "CR1 not found or already decided"
    return pat.sub(lambda m: m.group(1) + "backlog:Disp_Accepted", text, count=1)


# ---------------------------------------------------------------- scope revision
def scope_rev_block():
    return '''
ex:Area5_Ch0910 a backlog:ScopeArea ; rdfs:label "Chapters 9 and 10 produced and verified this session"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:areaLocation "03-materials/ch09, ch10 and their page/ subfolders; checks in 08-tooling" ;
    backlog:areaMeasure "2 chapters, each a deck and a page, recorded Done with real finish dates from git and a fresh deck-check run" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del5_Ch0910 a backlog:ScopeDeliverable ; rdfs:label "The chapter 9 and 10 deck and page recorded Done"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:derivesFromMissionClause "%(c)s"^^xsd:string ;
    backlog:hasDeliverableText "The decks and pages of chapters 9 and 10 are recorded Done, each with its real finish date from git and a fresh re-run of the deck standard check (D1-D12, all PASS on both); the page's 5N1K-hidden-from-audience fix was verified on both by direct inspection (0 occurrences of the WHO/WHERE/WHEN label tags in either built page); the real headless-browser test suite was launched against the chapter 9 page but did not finish within this session and its buffered output was lost entirely on termination, disclosed, not claimed as run." ;
    backlog:deliverableForArea ex:Area5_Ch0910 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Scope5 backlog:coversArea ex:Area5_Ch0910 ; backlog:requiresDeliverable ex:Del5_Ch0910 ;
    backlog:scopeGrownBy ex:SC1_Ch0910 .
''' % {"c": CLAUSE}


# ---------------------------------------------------------------- goal revision
GOALS5R1 = [
    ("G5_Ch0910Done", "Chapter 9 and 10 production is recorded Done with real, re-verified evidence", "Facing_Mission", "GoalOrigin_New", "Area5_Ch0910"),
    ("G5_Ch0910DeckStdMet", "Both decks pass the current deck standard check (D1-D12) when re-run, not merely remembered as passing", "Facing_Scope", "GoalOrigin_New", "Area5_Ch0910"),
]


def goal_rev_block():
    L = []
    for i, label, f, origin, area in GOALS5R1:
        L.append('''
ex:%(i)s a backlog:Goal ; rdfs:label "%(label)s"@en ; backlog:belongsToLineage ex:Lineage5 ; backlog:derivesFromScope ex:Scope5 ; backlog:goalCoversArea ex:%(area)s ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:%(f)s ; backlog:hasGoalOrigin backlog:%(origin)s ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale "Derived from Scope5 as grown by ex:SC1_Ch0910: chapters 9/10 are admitted with the same real-evidence discipline as chapter 7/8 at this lineage's opening." ;
    backlog:producedByStage ex:Out5_GoalR1 .
''' % dict(i=i, label=label, area=area, f=f, origin=origin))
    return "".join(L)


# ---------------------------------------------------------------- objective revision
OBJS5R1 = [
    ("Obj5_Ch0910Done", "G5_Ch0910Done", "Met5_Ch0910Done", "chapter 9/10 deck+page stories (4) recorded Done", 0, 4, "Dir_Increase"),
    ("Obj5_Ch0910DeckStdPass", "G5_Ch0910DeckStdMet", "Met5_Ch0910DeckStdPass", "deck-standard elements (D1-D12) passing on a fresh run of both chapters' decks", 0, 24, "Dir_Increase"),
]


def objective_rev_block(now_iso):
    L = []
    for i, g, m, what, b, tg, d in OBJS5R1:
        L.append('''
ex:%(i)s a backlog:Objective ; rdfs:label "%(what)s: from %(b)d to %(tg)d"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:contributesToGoal ex:%(g)s ; backlog:fillsScope ex:Scope5 ; backlog:hasSuccessMetric ex:%(m)s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %(what)s, read from this register." ;
    backlog:hasBaselineValue "%(b)d"^^xsd:decimal ; backlog:hasTargetValue "%(tg)d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%(d)s ;
    backlog:hasCheckpoint ex:CP5_%(i)s ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out5_ObjectiveR1 .
ex:%(m)s a backlog:Metric ; rdfs:label "%(what)s"@en ; backlog:belongsToLineage ex:Lineage5 .
ex:CP5_%(i)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the Backlog-stage revision ex:Out5_BacklogR1 is closed"@en ;
    backlog:checkpointCondition "Taken after ex:Out5_BacklogR1 is closed." ;
    backlog:expectedValue "%(tg)d"^^xsd:decimal .
ex:Obs50_%(i)s a backlog:MetricObservation ; rdfs:label "Baseline, before this change's Backlog revision closes"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(i)s ; backlog:hasObservedValue "%(b)d"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Read from this register at the Objective revision of the fifth lineage's first change: nothing has been admitted by ex:Out5_BacklogR1 yet." .
''' % dict(i=i, g=g, m=m, what=what, b=b, tg=tg, d=d, now=now_iso))
    return "".join(L)


# ---------------------------------------------------------------- backlog revision
AC_BLOCK5R1 = '''
ex:AC5_Ch0910 a backlog:AcceptanceCriterion ; rdfs:label "A chapter 9/10 deck or page is accepted when its real finish date and file hash are recorded and, for the deck, the deck standard check passes on a fresh run"@en ; backlog:belongsToLineage ex:Lineage5 ;
    backlog:hasGherkinText "Given a deck or page built this session, when its finish date is taken from git and its file hashed, and for a deck the standard check (D1-D12) is run again, then it is admitted Done with that evidence; a chapter whose check fails would be admitted failing and named, not Done." ;
    backlog:satisfiedByArtifact "the deck-standard-check output and the file hash, recorded in this register" .
'''

DECK09 = dict(path="03-materials/ch09/SEN0401_Ch09_TransactionFees_3e_v2_1_0.pptx",
              sha="c6857000b769d98f13e0fd34c6325210bfbc134c8a8289d2015f6a20f889bd81", commit="841f808",
              dt="2026-11-10T16:15:20")
DECK10 = dict(path="03-materials/ch10/SEN0401_Ch10_TheBitcoinNetwork_3e_v2_3_0.pptx",
              sha="4d913a1a78b17552c2144f4776fce60e1d0d37eed80dac380d7788914ce36140", commit="841f808",
              dt="2026-11-10T16:15:20")
PAGE09 = dict(path="03-materials/ch09/page/sen0401_ch09_page_v9_92_0.html",
              sha="193ae63ddfd3ae209f6c1182f3bac5ccc6ec4596ddf5a31c1b58baef6c35faab", commit="841f808",
              dt="2026-11-10T16:15:20")
PAGE10 = dict(path="03-materials/ch10/page/sen0401_ch10_page_v9_93_0.html",
              sha="f6ab51b60648711e5f61c16ee94c6d8b26cbf7cfa001c6f123d88de86ad3e287", commit="841f808",
              dt="2026-11-10T16:15:20")
EXEC5 = S.EXEC5
START = "2026-11-10T16:00:00"  # this change cycle's own work began within today's session


def _story(kind, ch, f, aud):
    sid = "ST_%s_Ch%s_Lineage5" % (kind, ch)
    ev = "Ev5_%s_Ch%s" % (kind, ch)
    deck_note = "Deck standard check v2.0.0 re-run fresh today (not a remembered result): D1-D12 all PASS, 0 of 12 failing; D5 itself genuinely verified (5N1K=how/what/when/where/who/why, real picture, real live link) on every story slide."
    page_note = ("Interactive page: 0 occurrences of the WHO/WHERE/WHEN label tags verified by direct grep against the built page; the real headless-browser suite "
                 "(sen0401_page_test_v9_39_0.py) was launched against the chapter 9 page the same way as chapter 7/8's but did not finish within this session's time "
                 "bound and its buffered output was lost entirely on termination (worse than 7/8's run, which at least printed several PASS lines before its own gap) - "
                 "disclosed plainly; nothing from that suite is claimed, only the direct-inspection result above.")
    return ('\nex:%(sid)s a backlog:Story ; rdfs:label "%(kind)s of chapter %(ch)s, admitted by this lineage\'s first change"@en ;\n'
            '    backlog:hasIdentifier "%(sid)s" ; backlog:hasTitle "Chapter %(ch)s %(kindlow)s, brought to the D5 5N1K-hidden-from-audience standard" ;\n'
            '    backlog:belongsToLineage ex:Lineage5 ; backlog:admittedByOutput ex:Out5_BacklogR1 ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
            '    backlog:asRole "SEN0401 student and instructor" ; backlog:wantsCapability "the %(kindlow)s of chapter %(ch)s, built to the current deck/page standard" ;\n'
            '    backlog:soThat "chapter %(ch)s is taught from material that meets the current 5N1K-hidden-from-audience and deck-standard rulings" ;\n'
            '    backlog:satisfiesDeliverable ex:Del5_Ch0910 ; backlog:pursuesObjective ex:Obj5_Ch0910Done ; backlog:hasAcceptanceCriterion ex:AC5_Ch0910 ;\n'
            '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:responsible %(exec)s ;\n'
            '    backlog:hasState backlog:Done ; backlog:startedAt "%(start)s"^^xsd:dateTime ; backlog:finishedAt "%(fin)s"^^xsd:dateTime ;\n'
            '    backlog:lastAuditedAt "%(fin)s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n'
            '    backlog:hasEvidence ex:%(ev)s ;\n'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Admitted by a change-management cycle at close, same as chapter 7/8: it was never planned ahead of its own completion, so it is not scored." ;\n'
            '    backlog:hasAuditNote "Built and committed this session (git commit %(commit)s, %(dt)s local). %(note)s" .\n'
            'ex:%(ev)s a backlog:ArtifactEvidence ; rdfs:label "%(path)s, committed %(dt)s"@en ; backlog:belongsToLineage ex:Lineage5 ; backlog:attestsCriterion ex:AC5_Ch0910 ;\n'
            '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%(path)s" ; backlog:hasArtifactSHA256 "%(sha)s" ;\n'
            '    backlog:hasVerificationMethod "%(method)s" ; backlog:verifiedByTool "%(tool)s" ; backlog:verifiedAt "%(aud)s"^^xsd:dateTime .\n'
            ) % dict(sid=sid, kind=kind, kindlow=kind.lower(), ch=ch, exec=EXEC5, start=START, fin=f["dt"], ev=ev,
                      commit=f["commit"], dt=f["dt"], path=f["path"], sha=f["sha"], aud=aud,
                      note=(deck_note if kind == "Deck" else page_note),
                      method=("Fresh re-run, this session, of sen0401_deck_standard_check_v2_0_0.py: SUMMARY PASS=12 FAIL=0 NOT_MEASURED=0." if kind == "Deck"
                              else "Direct grep of the built page for the three WHO/WHERE/WHEN label tags (0 occurrences); the browser test suite's run did not complete."),
                      tool=("sen0401_deck_standard_check_v2_0_0.py" if kind == "Deck" else "grep (direct inspection) + sen0401_page_test_v9_39_0.py (attempted, incomplete)"))


def backlog_rev_stage(t, prev_commit, now_iso):
    t = fill_previous_named(t, "Out5_ObjectiveR1", prev_commit)
    aud = now_iso
    add = [AC_BLOCK5R1,
           _story("Deck", "09", DECK09, aud), _story("Page", "09", PAGE09, aud),
           _story("Deck", "10", DECK10, aud), _story("Page", "10", PAGE10, aud)]
    t += "".join(add)
    t += "ex:Obj5_Ch0910Done backlog:metricMovableBy ex:ST_Deck_Ch09_Lineage5, ex:ST_Page_Ch09_Lineage5, ex:ST_Deck_Ch10_Lineage5, ex:ST_Page_Ch10_Lineage5 .\n"
    t += "ex:Obj5_Ch0910DeckStdPass backlog:metricMovableBy ex:ST_Deck_Ch09_Lineage5, ex:ST_Deck_Ch10_Lineage5 .\n"
    t += output_rev(t, "Backlog", 1, "Out5_Backlog")
    comment = ("fifth lineage, first change (ex:CR1_Ch0910/ex:SC1_Ch0910), Backlog revision R1 closed: 4 chapter "
               "9/10 stories admitted Done with real evidence (deck standard check re-run fresh, PASS all 12 on "
               "both, D5 itself genuinely verified; page fix verified by direct grep, the browser suite did not "
               "complete and is disclosed as such, not claimed).")
    return t, comment


def main():
    ev = sys.argv[1]; prev = sys.argv[2] if len(sys.argv) > 2 else None
    src = newest(); t = open(src, encoding="utf-8").read(); nxt, cur = next_version(src)
    now_iso = now()
    if ev == "request":
        t = t + request_block()
        comment = "fifth lineage, first change-management cycle opened: ex:CR1_Ch0910 (grow Scope5 for chapter 9/10) + ex:IA1_Ch0910 (impact assessment, Disp_Pending)."
    elif ev == "accept":
        t = fill_disposition_accepted(t)
        t = t + accept_block()
        comment = "fifth lineage, ex:CR1_Ch0910 disposition moved to Disp_Accepted (owner's 'Yes, proceed'); ex:SC1_Ch0910 (ScopeChange) recorded."
    elif ev == "scope":
        t2 = t + scope_rev_block()
        t = t2 + output_rev(t2, "Scope", 1, "Out5_Scope")
        comment = "fifth lineage, Scope revision R1 closed (ex:SC1_Ch0910): admit chapter 9/10 production."
    elif ev == "goal":
        t = fill_previous_named(t, "Out5_ScopeR1", prev)
        t2 = t + goal_rev_block()
        t = t2 + output_rev(t2, "Goal", 1, "Out5_ScopeR1")
        comment = "fifth lineage, first change, Goal revision R1 closed."
    elif ev == "objective":
        t = fill_previous_named(t, "Out5_GoalR1", prev)
        t2 = t + objective_rev_block(now_iso)
        t = t2 + output_rev(t2, "Objective", 1, "Out5_GoalR1")
        comment = "fifth lineage, first change, Objective revision R1 closed."
    elif ev == "backlog":
        t, comment = backlog_rev_stage(t, prev, now_iso)
    else:
        raise SystemExit("unknown event " + ev)
    out = write_new(src, t, nxt, cur, comment)
    print(out)


if __name__ == "__main__":
    main()
