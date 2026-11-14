#!/usr/bin/env python3
"""sen0401_lineage7_stages v1.0.0 - stage events (Mission, Scope, Goal, Objective) of ex:Lineage7, the urgent lineage that corrects the chapter 11 deck and page to the owner's rulings of 2026-11-14. Parented to the sixth lineage so both may be active (G104); opens under Profile_Standard from backlog_open_lineage. Usage: python3 sen0401_lineage7_stages_v1_0_0.py mission|scope|goal|objective [PREV_COMMIT]"""
import datetime, glob, importlib.util, os, re, subprocess, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = REPO
FRAMEWORK = os.environ.get('BRSF_ROOT', '/home/claude/altunelyusuf/backlog-roadmap-framework')
LIN = os.path.join(REPO, "07-lineage")
FW = "/home/claude/Ontologies/backlog-roadmap-framework"
BASE = "http://example.org/sen0401-slides-lineage"
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace(BASE + "#")
STAGES = ["Mission", "Scope", "Goal", "Objective", "Backlog"]
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
    return _pv().state_digest(g, "Stage_" + stage, EX.Lineage7)


def output(text, stage):
    i = STAGES.index(stage)
    consumes = ("\n    backlog:consumesOutput ex:Out7_%s ;" % STAGES[i - 1]) if i else ""
    return ('\nex:Out7_%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the seventh lineage"@en ;\n    backlog:belongsToLineage ex:Lineage7 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;%s\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, digest(text, stage))


def fill_previous(text, stage, commit):
    pat = re.compile(r'(ex:Out7_%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % stage, re.S)
    assert pat.search(text), "no PENDING on Out7_" + stage
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, text, count=1)


def set_lineage_status(text, lin, status):
    m = re.search(r"(ex:%s a backlog:Lineage ;.*?)backlog:hasLineageStatus backlog:\w+" % lin, text, re.S)
    assert m
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:" + status + text[m.end():]


def set_status(text, status):
    pat = re.compile(r'(ex:Lineage7 a backlog:Lineage ;.*?)(backlog:hasLineageStatus backlog:\w+ ;\s*)?(backlog:adoptsObligationSet)', re.S)
    m = pat.search(text); assert m
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:%s ;\n    " % status + m.group(3) + text[m.end():]



CLAUSE7 = "Every SEN0401 lecture teaches what the third edition of Mastering Bitcoin teaches"
COMMIT_URG = None


def opening_block():
    import subprocess
    tool = FW + "/03-tooling/backlog_open_lineage_v1_3_0.py"
    out = subprocess.run([sys.executable, tool, "--profile", "Profile_Standard", "--lineage", "Lineage7", "--prefix", "ex"], capture_output=True, text=True, check=True).stdout
    assert "RS_ConcurrentLineages" in out
    return "\n" + out


def lineage_header():
    return ('\nex:Lineage7 a backlog:Lineage ;\n'
            '    rdfs:label "Seventh lineage: the chapter 11 deck and page corrected to the owner\'s rulings of 2026-11-14 (urgent)"@en ;\n'
            '    backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 7 ; backlog:lineageArchived false ;\n'
            '    backlog:parentLineage ex:Lineage6 ;\n'
            '    backlog:adoptsObligationSet backlog:OS_SDLC_v2 .\n') + opening_block()


def mission_block():
    return '\nex:Lineage7 backlog:lineageForMission ex:Mission .\n'


def scope_block():
    return '''
ex:Area7_Ch11 a backlog:ScopeArea ; rdfs:label "The chapter 11 deck and its page, corrected to the deck and page rulings of 2026-11-14"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:areaLocation "03-materials/ch11 (the deck) and 03-materials/ch11/page (the page); the correction script in 08-tooling" ;
    backlog:areaMeasure "1 deck and 1 page, each passing the CME material check (title words, visual per slide, notes of 60-140 words, no prompt markers, code that parses, no untaught lambda, slide code on the page)" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del7_Ch11 a backlog:ScopeDeliverable ; rdfs:label "The chapter 11 deck and page that pass the material rulings"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:derivesFromMissionClause "%(c)s"^^xsd:string ;
    backlog:hasDeliverableText "A new version of the chapter 11 deck and of its page. Every slide title has at least four words; every content slide carries a visual; every presenter note is 60 to 140 words (30 to 140 on the opening, closing and divider slides) and teaches the slide; no code frame carries a prompt marker and every frame parses as shown; no lambda appears in slide code or page code; every slide code frame is on the page; the page has the Slide code tab. The CME material check passes on both, run fresh." ;
    backlog:deliverableForArea ex:Area7_Ch11 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Excl7_Rest a backlog:ScopeExclusion ; rdfs:label "Chapters 12-14 and the older chapters are not corrected here"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:excludesConcern "The decks and pages of chapters 12, 13 and 14, and of chapters 1-10 including 7 and 8. They fail the same rulings and are corrected by later lineages, one lineage per round of chapters." ;
    backlog:hasExclusionRationale "The owner ruled on 2026-11-14 that the corrections come first and that the older files are processed by the next lineages, not all in one lineage, if that causes complications. This lineage keeps the smallest closeable slice: one chapter, one deck and one page." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .
ex:Scope7 a backlog:ScopeStatement ; rdfs:label "Correct the chapter 11 deck and page to the owner's rulings, as an urgent lineage"@en ;
    backlog:belongsToLineage ex:Lineage7 ; backlog:scopeForMission ex:Mission ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:scopeCompletionState backlog:Proposed ;
    backlog:hasScopeStatementText "IN: a corrected chapter 11 deck and page that pass the CME material check. OUT: every other chapter (see the exclusion). The sixth lineage, which admits the finished chapter 11-14 files, is paused by the urgency ceremony while this lineage works and resumes when it is done." ;
    backlog:coversArea ex:Area7_Ch11 ;
    backlog:hasScopeExclusion ex:Excl7_Rest ;
    backlog:producedByStage ex:Out7_Scope ;
    backlog:requiresDeliverable ex:Del7_Ch11 .
ex:Blueprint7 a backlog:Blueprint ; rdfs:label "What the chapter 11 correction is about"@en ;
    backlog:belongsToLineage ex:Lineage7 ; backlog:blueprintFor ex:Scope7 ; backlog:hasDomainEntity ex:DE3_Deck, ex:DE3_InteractivePage .
''' % {"c": CLAUSE7}


def goal_block():
    return '''
ex:G7_Ch11Meets a backlog:Goal ; rdfs:label "The chapter 11 deck and page meet the written material rulings when the check is run fresh"@en ; backlog:belongsToLineage ex:Lineage7 ; backlog:derivesFromScope ex:Scope7 ; backlog:goalCoversArea ex:Area7_Ch11 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalOrigin backlog:GoalOrigin_New ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale "Derived from the scope of the seventh lineage: the chapter 11 files fail the owner's rulings of 2026-11-14 on a measured run of the CME material check, and the owner ordered the corrections first, in an urgent lineage." ;
    backlog:producedByStage ex:Out7_Goal .
'''


def objective_block(now_iso):
    return '''
ex:Obj7_Ch11Pass a backlog:Objective ; rdfs:label "Material-check conditions passing on the chapter 11 deck and page: from 2 to 16"@en ; backlog:belongsToLineage ex:Lineage7 ;
    backlog:contributesToGoal ex:G7_Ch11Meets ; backlog:fillsScope ex:Scope7 ; backlog:hasSuccessMetric ex:Met7_Ch11Pass ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of the 16 conditions (8 checks on the deck, 8 on the deck with its page) reported PASS by cme_material_check on the newest chapter 11 deck and page." ;
    backlog:hasBaselineValue "2"^^xsd:decimal ; backlog:hasTargetValue "16"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP7_Ch11Pass ;
    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out7_Objective .
ex:Met7_Ch11Pass a backlog:Metric ; rdfs:label "Material-check conditions passing on the chapter 11 deck and page"@en ; backlog:belongsToLineage ex:Lineage7 .
ex:CP7_Ch11Pass a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the Backlog stage output of this lineage is closed"@en ;
    backlog:checkpointCondition "Taken after the Backlog stage output of this lineage is closed." ; backlog:expectedValue "16"^^xsd:decimal .
ex:Obs70_Ch11Pass a backlog:MetricObservation ; rdfs:label "Baseline measured on 2026-11-14 on deck v2.1.0 and page 9.94.0"@en ;
    backlog:observesMetric ex:Met7_Ch11Pass ; backlog:observationFor ex:Obj7_Ch11Pass ; backlog:hasObservedValue "2"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "cme_material_check_v1_0_0.py run on SEN0401_Ch11_TheBlockchain_3e_v2_1_0.pptx and sen0401_ch11_page_v9_94_0.html: the notes-labels and code-in-page conditions pass, the other conditions fail." .
''' % now_iso


def main():
    ev = sys.argv[1]; prev = sys.argv[2] if len(sys.argv) > 2 else None
    src = newest(); t = open(src, encoding="utf-8").read(); nxt, cur = next_version(src)
    now_iso = now()
    if ev == "mission":
        t2 = set_status(t + lineage_header() + mission_block(), "LS_Opened")
        t = t2 + output(t2, "Mission")
        comment = "seventh lineage opened as an urgent lineage parented to the sixth (Profile_Standard from backlog_open_lineage), Mission stage closed; the sixth lineage is untouched."
    elif ev == "scope":
        t = fill_previous(t, "Mission", prev); t = set_status(t, "LS_Scoped"); t2 = t + scope_block()
        t = t2 + output(t2, "Scope"); comment = "seventh lineage, Scope stage closed (chapter 11 deck and page only)."
    elif ev == "goal":
        t = fill_previous(t, "Scope", prev); t = set_status(t, "LS_Goaled"); t2 = t + goal_block()
        t = t2 + output(t2, "Goal"); comment = "seventh lineage, Goal stage closed."
    elif ev == "objective":
        t = fill_previous(t, "Goal", prev); t = set_status(t, "LS_Objectived"); t2 = t + objective_block(now_iso)
        t = t2 + output(t2, "Objective"); comment = "seventh lineage, Objective stage closed."
    else:
        raise SystemExit("unknown event " + ev)
    out = write_new(src, t, nxt, cur, comment)
    print(os.path.basename(out))


if __name__ == "__main__":
    main()
