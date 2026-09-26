#!/usr/bin/env python3
"""Derives the page ABox's build record from version 2's page data and browser results, so the ABox writer
records every v2 widget - and marks it tested only if its v2 browser test passed. Usage: <NN>"""
__version__ = "2.1.0"
import json, os, sys
PV = os.environ.get("PAGE_VER", "9_4_2")  # generated files carry the page version they were produced for
N = sys.argv[1]; N = ("ch%s" % N) if N.isdigit() else N; P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v%s.json" % PV))); t = json.load(open(os.path.join(P, "test_results_v%s.json" % PV)))
W = []
for n in d["nodes"]:
    if "io" in n: kind, prim, war = "predict", "Primitive_CoupledVariableExplorer", "Feature_AsymmetricContrast: the learner edits and predicts %s, then Pyodide shows what Python actually does" % n["io"]["code"]
    elif n.get("chart"): kind, prim, war = "chart", "Primitive_OverviewDetailBrushing", "Feature_LargeCollectionOverview: the section is a long sampled series; the chart gives the overview and hovering a point gives its exact value"
    elif n["level"] == 3: kind, prim, war = "steps", "Primitive_GuidedNarrativeWalkthrough", "Feature_OrderedArgument: example first, then its explanation"
    else: kind, prim, war = "map", "Primitive_OverviewDetailBrushing", "Feature_KCategoryEnumeration: the section enumerates its kinds; choosing one opens its card"
    W.append({"id": "w-" + n["id"], "kind": kind, "cls": n["class_iri"], "prim": prim, "warrant": war})
# the chapter's visualisations are widgets of their own, recorded with the interaction they offer
VPRIM = {"floatbits": ("Primitive_CoupledVariableExplorer", "Feature_AsymmetricContrast: the learner types a number and sees the bits Python stores, against the decimal it shows"),
         "truthtable": ("Primitive_CoupledVariableExplorer", "Feature_CrossAttributeRelation: the learner edits a Boolean expression and sees its value for every combination of inputs"),
         "branchflow": ("Primitive_DynamicQueryContinuous", "Feature_OrderedArgument: the learner moves the input and sees which branch of the chain actually runs")}
for cid, v in ((k, x) for k, x in d.get("visuals", {}).items() if not k.startswith("_")):
    n = next(x for x in d["nodes"] if x["id"] == cid)
    W.append({"id": "wv-" + cid, "kind": "visual", "cls": n["class_iri"], "prim": VPRIM[v["kind"]][0], "warrant": VPRIM[v["kind"]][1]})
rec = {"widgets": W, "sections": [(i, n["level"], n["label"], "s-" + n["id"], n["section_iri"]) for i, n in enumerate(d["nodes"], 1)],
       "python": d["python"], "quiz": (lambda q: q["items"] if isinstance(q, dict) else q)(json.load(open(sorted(__import__("glob").glob(os.path.join(P, "quiz_v*.json")))[-1]))), "_version": PV.replace("_", ".")}
json.dump(rec, open(os.path.join(P, "build_record_v%s.json" % PV), "w"), indent=1)
json.dump({"_version": PV.replace("_", "."), "widgets": t["widgets"], "gates": t["gates"]}, open(os.path.join(P, "test_results_abox_v%s.json" % PV), "w"), indent=1)
print("record: %d widgets, %d passed in the browser" % (len(W), sum(1 for w in W if t["widgets"][w["id"]]["passed"])))
