#!/usr/bin/env python3
"""backlog_lineage_template v1.1.0 -- the chain of a lineage generated from one specification (Lineage 33, urgent; Owner, 2026-11-24).

A lineage is Mission -> Scope -> Goal -> Objective -> Backlog, one commit per stage (ceremony step 2, G18, G148). Written by hand that is some
two hundred lines and five commits. The obligations are the same for the smallest lineage (G99: compressed, not skipped), so this tool writes them
from a short JSON specification, in the order the order check witnesses:

  backlog_lineage_template.py REGISTER SPEC.json [--commit]

For each stage, in turn: the stage's records and its StageOutput (digest computed from the register as it stands, as backlog_pipeline_verify
computes it), the lineage status that points at it, and, with --commit, one git commit of the register. The commit hash of a stage is
recorded on its output (closedAtCommit) in the next stage's commit, which is how an output can name a commit that already exists; the last
stage's hash is recorded by a final commit. Nothing is edited except the lineage's own status line; everything else is appended.

v1.1.0 (box 66, review r1): every record the tool writes carries belongsToLineage (the checkpoints, observations, metrics, criteria and gaps did not, so the lineage-scope check never looked at them), and the specification below is the one the tool reads (the v1.0.0 text listed keys it no longer read).
SPEC (JSON):
 {"lineage": "L_X", "key": "X", "title": "...", "prefix": "fw", "date": "2026-11-24T08:00:00Z",
  "scope": {"text": "...", "area": "...", "area_measure": "...", "area_location": "...",
            "deliverables": [["label", "mission clause"], ...], "exclusion": "...", "exclusion_why": "...", "entity_iri": "fw:Entity_X"},
  "goals": {"mission": "...", "area": "...", "contain": "..."},
  "objectives": {"mission": OBJ, "area": OBJ, "contain": OBJ},   OBJ = {"metric": "...", "unit": "...", "baseline": 1, "target": 0,
                "direction": "Decrease|Increase|Hold", "rationale": "...", "method": "...", "checkpoint": "2026-11-27T00:00:00Z"}
  "stories": ["ST_X_Seed", {"iri": "ST_X_Two", "id": "X-S2", "title": "...", "ac": "...", "reach": 3, "impact": 2, "confidence": 0.8, "effort": 3,
                            "covers": "Creation", "deliverable": 1}],
  "gaps": {"ActiveUse": "why", "SuspensionException": "why", "Termination": "why"}}
The mission record and the seed story may already exist (an urgent seed is recorded at the declaration); the tool adds to them, never rewrites.
Exit 0 when the chain is written, 2 when the specification or the register refuses it.
"""
import glob, json, os, re, subprocess, sys
import rdflib
from rdflib import URIRef, RDF
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
B = "http://example.org/backlog#"
FW = "http://example.org/backlog-framework-register#"
STATUS = {"Mission": "LS_Opened", "Scope": "LS_Scoped", "Goal": "LS_Goaled", "Objective": "LS_Objectived", "Backlog": "LS_Backlogged"}
sv = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", p)[0]]


def verify_module():
    return __import__(os.path.basename(sorted(glob.glob(os.path.join(HERE, "backlog_pipeline_verify_v*.py")), key=sv)[-1])[:-3])


def esc(t): return str(t).replace("\\", "\\\\").replace('"', '\\"')


def digest(path, stage, lineage_iri):
    g = rdflib.Graph(); g.parse(path, format="turtle")
    pv = verify_module()
    adopted = {str(o).rsplit("#", 1)[-1] for o in g.objects(URIRef(lineage_iri), URIRef(B + "adoptsRuleSet"))}
    table = next((x for x in ("v5", "v4", "v3", "v2") if "RS_DigestTable_" + x in adopted), "v1")
    tbox = sorted(glob.glob(os.path.join(os.path.dirname(HERE), "01-ontologies", "backlog_tbox_v*.ttl")), key=sv)[-1]
    pv.STAGE_TYPES = pv._load_stage_types(tbox, table=table)
    return pv.state_digest(g, "Stage_" + stage, URIRef(lineage_iri), admitted=True, change_managed=True)


def git(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)


def blocks(s, p):
    L, K = s["lineage"], s["key"]; sc = s["scope"]; d = s["date"]
    q = lambda n: f"{p}:{n}"
    out = lambda st: f"{p}:Out_{st}_{L[2:]}"
    ln = f"{p}:{L}"
    b = {}
    b["Mission"] = (f'{q("Mission_" + L[2:])} backlog:producedByStage {out("Mission")} .\n'
                    f'{q("Mission_" + L[2:])} backlog:hasMissionOutcome backlog:Out_InFlight .\n')
    b["Scope"] = (f'{q("Scope_" + K)} a backlog:ScopeStatement ; rdfs:label "Scope: {esc(s["title"])}"@en ;\n'
                  f'    backlog:hasScopeStatementText "{esc(sc["text"])}" ;\n    backlog:scopeForMission {q("Mission_" + L[2:])} ;\n'
                  f'    backlog:producedByStage {out("Scope")} ; backlog:hasIntentOrigin backlog:IOrigin_Derived ;\n'
                  f'    backlog:requiresDeliverable {" , ".join(q("Del_" + K + str(i)) for i in range(len(sc["deliverables"])))} ; backlog:coversArea {q("Area_" + K)} ; backlog:hasScopeExclusion {q("Ex_" + K)} ;\n'
                  f'    backlog:belongsToLineage {ln} .\n'
                  f'{q("Area_" + K)} a backlog:ScopeArea ; rdfs:label "Area: {esc(sc["area"])}"@en ;\n'
                  f'    backlog:areaMeasure "{esc(sc["area_measure"])}" ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:areaLocation "{esc(sc["area_location"])}" ; backlog:belongsToLineage {ln} .\n'
                  + "".join(f'{q("Del_" + K + str(i))} a backlog:ScopeDeliverable ; rdfs:label "{esc(dl[0])}"@en ;\n    backlog:deliverableForArea {q("Area_" + K)} ; backlog:hasScopeLayer backlog:Layer_Work ;\n    backlog:derivesFromMissionClause "{esc(dl[1])}" ; backlog:belongsToLineage {ln} .\n' for i, dl in enumerate(sc["deliverables"]))
                  + (
                  f'{q("Ex_" + K)} a backlog:ScopeExclusion ; rdfs:label "Exclusion: {esc(sc["exclusion"])}"@en ;\n'
                  f'    backlog:excludesConcern "{esc(sc["exclusion"])}" ; backlog:hasExclusionRationale "{esc(sc["exclusion_why"])}" ;\n'
                  f'    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:belongsToLineage {ln} .\n'))
    gl = lambda n, label, facing, extra: (f'{q("Goal_" + K + n)} a backlog:Goal ; rdfs:label "{esc(label)}"@en ;\n'
                 f'    backlog:contributesToMission {q("Mission_" + L[2:])} ; backlog:derivesFromScope {q("Scope_" + K)} ; backlog:hasGoalFacing backlog:Facing_{facing} ;{extra}\n'
                 f'    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:producedByStage {out("Goal")} ; backlog:belongsToLineage {ln} ; backlog:decidedBy backlog:Owner .\n')
    g = s["goals"]
    b["Goal"] = (gl("_Mission", g["mission"], "Mission", "") + gl("_Area", g["area"], "Scope", f' backlog:goalCoversArea {q("Area_" + K)} ;')
                 + gl("_Contain", g["contain"], "Containment", ""))
    obs = {"Mission": ("_Mission", "Mission"), "Area": ("_Area", "Area"), "Contain": ("_Contain", "Contain")}
    o = ""
    for key in ("mission", "area", "contain"):
        ob = s["objectives"][key]; n = "_" + key.capitalize()
        dr = {"Decrease": "Dir_Decrease", "Increase": "Dir_Increase", "Hold": "Dir_Hold"}[ob["direction"]]
        o += (f'{q("Metric_" + K + n)} a core:Metric ; backlog:belongsToLineage {ln} ; rdfs:label "{esc(ob["metric"])}"@en ; skos:definition "Counted in units of: {esc(ob["unit"])}."@en .\n'
              f'{q("CP_" + K + n)} a backlog:ObjectiveCheckpoint ; backlog:belongsToLineage {ln} ; backlog:checkpointDate "{ob["checkpoint"]}"^^xsd:dateTime .\n'
              f'{q("Obj_" + K + n)} a backlog:Objective ; backlog:hasIntentOrigin backlog:IOrigin_Derived ; rdfs:label "Objective: {esc(ob["metric"])}"@en ;\n'
              f'    backlog:contributesToGoal {q("Goal_" + K + n)} ; backlog:fillsScope {q("Scope_" + K)} ;\n'
              f'    backlog:hasSuccessMetric {q("Metric_" + K + n)} ; backlog:hasMeasurementKind backlog:Meas_Counted ;\n'
              f'    backlog:hasBaselineValue "{ob["baseline"]}"^^xsd:decimal ; backlog:hasTargetValue "{ob["target"]}"^^xsd:decimal ; backlog:hasTargetDirection backlog:{dr} ;\n'
              f'    backlog:hasCheckpoint {q("CP_" + K + n)} ; backlog:hasRationale "{esc(ob["rationale"])}" ;\n'
              f'    backlog:producedByStage {out("Objective")} ; backlog:belongsToLineage {ln} .\n'
              f'{q("Obs_" + K + n)} a backlog:MetricObservation ; backlog:belongsToLineage {ln} ; rdfs:label "Baseline: {esc(ob["metric"])}"@en ;\n'
              f'    backlog:observesMetric {q("Metric_" + K + n)} ; backlog:observationFor {q("Obj_" + K + n)} ;\n'
              f'    backlog:hasObservedValue {float(ob["baseline"])} ; backlog:observedAt "{d}"^^xsd:dateTime ; backlog:hasObservationMethod "{esc(ob["method"])}" .\n')
    b["Objective"] = o
    bk = ""
    ent = sc["entity_iri"]
    for i, st in enumerate(s["stories"]):
        if isinstance(st, str):
            st = {"iri": st, "deliverable": 0}
        iri = st["iri"]
        if "title" in st:
            bk += (f'{p}:AC_{iri[3:]} a backlog:AcceptanceCriterion ; backlog:belongsToLineage {ln} ; backlog:hasGherkinText "{esc(st["ac"])}" .\n'
                   f'{p}:{iri} a backlog:Story ;\n    backlog:hasIdentifier "{st["id"]}" ; backlog:hasTitle "{esc(st["title"])}"@en ; backlog:hasState backlog:Proposed ;\n'
                   f'    backlog:responsible {p}:Run_{K}_0_Builder ;\n'
                   f'    backlog:hasReach {st["reach"]} ; backlog:hasImpact {st["impact"]} ; backlog:hasConfidence {st["confidence"]} ; backlog:hasEffort {st["effort"]} ; backlog:hasPriorityScore {round(st["reach"]*st["impact"]*st["confidence"]/st["effort"], 2)} ;\n'
                   f'    backlog:hasExecutionModality backlog:Mode_Automated ; backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
                   f'    backlog:coversEntity {ent} ; backlog:coversStage backlog:Stage_{st["covers"]} ;\n'
                   f'    backlog:hasAcceptanceCriterion {p}:AC_{iri[3:]} ;\n    backlog:memberOfContainer {p}:Register ; backlog:belongsToLineage {ln} .\n')
        bk += (f'{p}:{iri} backlog:pursuesObjective {q("Obj_" + K + "_Mission")} , {q("Obj_" + K + "_Area")} ; backlog:satisfiesDeliverable {q("Del_" + K + str(st["deliverable"]))} ;\n'
               f'    backlog:admittedByOutput {out("Backlog")} ; backlog:producedByStage {out("Backlog")} .\n'
               f'{q("Obj_" + K + "_Area")} backlog:metricMovableBy {p}:{iri} .\n{q("Obj_" + K + "_Mission")} backlog:metricMovableBy {p}:{iri} .\n')
    for stage, why in s["gaps"].items():
        bk += (f'{q("Gap_" + K + "_" + stage)} a backlog:BlueprintGap ; backlog:belongsToLineage {ln} ; backlog:gapForEntity {ent} ; backlog:gapForStage backlog:Stage_{stage} ;\n'
               f'    backlog:hasGapReason "{esc(why)}" .\n')
    b["Backlog"] = bk
    return b


def main(argv):
    if len(argv) < 3: print(__doc__); return 2
    reg, spec, commit = argv[1], json.load(open(argv[2])), "--commit" in argv
    L, p = spec["lineage"], spec.get("prefix", "fw")
    root = subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(reg)), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    lin_iri = FW + L
    bl = blocks(spec, p)
    prev_out = prev_commit = None
    for st in ("Mission", "Scope", "Goal", "Objective", "Backlog"):
        t = open(reg).read()
        if not t.endswith("\n"): t += "\n"
        t += f"\n# ---- {L}: {st} stage (generated by backlog_lineage_template 1.1.0) ----\n"
        if prev_out and prev_commit:
            t += f"{prev_out} backlog:closedAtCommit \"{prev_commit}\" .\n"
        t += bl[st]
        open(reg, "w").write(t)
        d = digest(reg, st, lin_iri)
        o = f"{p}:Out_{st}_{L[2:]}"
        t = open(reg).read()
        t += (f"{o} a backlog:StageOutput ; backlog:outputOfStage backlog:Stage_{st} ; backlog:belongsToLineage {p}:{L} ;\n"
              + (f"    backlog:consumesOutput {prev_out} ;\n" if prev_out else "")
              + f"    backlog:hasStateDigest \"{d}\" ;\n    backlog:hasRationale \"{st} stage of {L}, generated from the lineage specification. One commit per stage.\" .\n")
        t = re.sub(rf"({re.escape(p + ':' + L)} a backlog:Lineage[^\n]*\n(?:[^\n]*\n)*?\s*backlog:hasLineageStatus )backlog:LS_\w+", rf"\1backlog:{STATUS[st]}", t, count=1)
        open(reg, "w").write(t)
        if commit:
            git(root, "add", "-A", "."); r = git(root, "commit", "-q", "-m", f"{L}: {st} stage\n\nGenerated by backlog_lineage_template 1.1.0.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_019rj4rmc2f14zp2u3XPWrMX")
            if r.returncode: print(r.stdout + r.stderr); return 2
            prev_commit = git(root, "rev-parse", "HEAD").stdout.strip()
        else:
            prev_commit = "0" * 40
        prev_out = o
        print(f"{st}: digest {d[:12]} commit {prev_commit[:8]}")
    t = open(reg).read() + f"{prev_out} backlog:closedAtCommit \"{prev_commit}\" .\n"
    open(reg, "w").write(t)
    if commit:
        git(root, "add", "-A", "."); git(root, "commit", "-q", "-m", f"{L}: Backlog stage commit recorded\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_019rj4rmc2f14zp2u3XPWrMX")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--deps"]:
        print(os.path.abspath(__file__)); sys.exit(0)
    sys.exit(main(sys.argv))
