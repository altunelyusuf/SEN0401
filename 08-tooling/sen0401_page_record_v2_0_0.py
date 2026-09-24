#!/usr/bin/env python3
"""Derives the page ABox's build record from version 2's page data and browser results, so the ABox writer
records every v2 widget - and marks it tested only if its v2 browser test passed. Usage: <NN>"""
import json, os, sys
N = sys.argv[1]; P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v2.json"))); t = json.load(open(os.path.join(P, "test_results_v2.json")))
W = []
for n in d["nodes"]:
    if "io" in n: kind, prim, war = "predict", "Primitive_CoupledVariableExplorer", "Feature_AsymmetricContrast: the learner edits and predicts %s, then Pyodide shows what Python actually does" % n["io"]["code"]
    elif n["level"] == 3: kind, prim, war = "steps", "Primitive_GuidedNarrativeWalkthrough", "Feature_OrderedArgument: example first, then its explanation"
    else: kind, prim, war = "map", "Primitive_OverviewDetailBrushing", "Feature_KCategoryEnumeration: the section enumerates its kinds; choosing one opens its card"
    W.append({"id": "w-" + n["id"], "kind": kind, "cls": n["class_iri"], "prim": prim, "warrant": war})
rec = {"widgets": W, "sections": [(i, n["level"], n["label"], "s-" + n["id"], n["section_iri"]) for i, n in enumerate(d["nodes"], 1)],
       "python": d["python"], "quiz": json.load(open(os.path.join(P, "quiz.json")))}
json.dump(rec, open(os.path.join(P, "build_record.json"), "w"), indent=1)
json.dump({"widgets": t["widgets"], "gates": t["gates"]}, open(os.path.join(P, "test_results.json"), "w"), indent=1)
print("record: %d widgets, %d passed in the browser" % (len(W), sum(1 for w in W if t["widgets"][w["id"]]["passed"])))
