#!/usr/bin/env python3
"""inputs_make v1_1_0 (SEN0401 chapter 13 page). Writes the page's authored inputs (objectives, quiz, question_bank, discussion, resources, stories_img, test_config, all v1_0_0) from the chapter's page data
(page_data_v*.json, the concepts exactly as the research states them) and from the deck's own links. Nothing here adds or rewords research prose: a question's right answer is the FIRST SENTENCE of the concept's
own explanation, its wrong answers are first sentences of other concepts, and its rationale names the concept the wrong answer belongs to. Run after sen0401_page_data_v2_18_0.py has written page_data.
v1_1_0 writes only question_bank_v1_1_0.json: the page data of 9_69_0 has 84 concepts (research v1_0_2) and the 1_0_0 bank covered 68; the method is unchanged. Usage: inputs_make_v1_0_0.py PAGEVER   (e.g. 9_48_0)"""
__version__ = "1.1.0"
import hashlib, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); PV = sys.argv[1]
d = json.load(open(os.path.join(H, "page_data_v%s.json" % PV))); nodes = d["nodes"]; by = {n["id"]: n for n in nodes}
def top(n):
    while n["parent"]: n = by[n["parent"]]
    return n["id"]
def first(n):
    t = (n["paras"][0]["text"] if n["paras"] else n["body"]).strip()
    m = re.search(r"(?<=[a-z0-9\)])\. (?=[A-Z])", t)
    s = t[:m.start() + 1] if m else t
    return s if len(s) <= 230 else s[:s.rfind(" ", 0, 227)] + " ..."
J = lambda name, obj: json.dump(obj, open(os.path.join(H, name), "w"), indent=1, ensure_ascii=False)
# ---- question bank: one item per concept ---------------------------------------------------------------------
OBJ = {"SecurityModel": "CO1", "ProtectingKeys": "CO2", "KeepingAccess": "CO3", "SharingControl": "CO4", "CustodyHistory": "CO5", "Survivability": "CO6"}
OBJ_G = {}
def obj(n):
    k = n
    while k:
        if k["id"] in OBJ_G: return OBJ_G[k["id"]]
        k = by[k["parent"]] if k["parent"] else None
    return OBJ[top(n)]
bank = []; pool = sorted(nodes, key=lambda n: hashlib.sha256(n["id"].encode()).hexdigest())
for n in nodes:
    right = first(n); others = []
    for m in pool:
        if m["id"] == n["id"] or top(m) == top(n) and len(others) < 1: continue
        s = first(m)
        if s != right and all(first(o) != s for o in others): others.append(m)
        if len(others) == 3: break
    opts = [(right, None)] + [(first(m), m) for m in others]
    order = sorted(range(4), key=lambda i: hashlib.sha256((n["id"] + str(i)).encode()).hexdigest())
    options = [opts[i][0] for i in order]; ans = order.index(0)
    lv = "Remember"
    why = "That sentence opens the chapter's explanation of '%s'. The others open the explanations of %s." % (n["label"], ", ".join("'%s'" % m["label"] for _, m in sorted([o for o in opts if o[1]], key=lambda o: o[1]["label"])))
    bank.append({"concept": n["id"], "level": lv, "q": "Which of these sentences opens the explanation of '%s' in this chapter?" % n["label"], "options": options, "answer": ans, "why": why})
J("question_bank_v1_1_0.json", bank)
