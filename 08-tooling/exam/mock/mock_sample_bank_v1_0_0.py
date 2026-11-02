#!/usr/bin/env python3
"""SYNTHETIC sample bank generator for the SEN0401 mock shell tests (v1.0.0).
Invented items about everyday topics (bakery, bicycle, garden, library, railway, orchard). NOT real exam text and NOT course content.
Usage: mock_sample_bank_v1_0_0.py OUTDIR  -> writes mock_bank_ch{1..6}_v1_0_0.json (flag synthetic:true) and the merged mock_bank_sample.json"""
import json, os, sys, random

THEMES = {1: ("bakery", "roll", "tray", "oven"), 2: ("bicycle shop", "tyre", "box", "pump"), 3: ("garden", "plant", "bed", "spade"),
          4: ("library", "book", "shelf", "ladder"), 5: ("railway depot", "ticket", "booth", "stamp"), 6: ("orchard", "apple", "crate", "basket")}
LET = "ABCDE"

def choice(ch, n):
    th, thing, box, tool = THEMES[ch]
    rnd = random.Random(ch * 1000 + n)
    a, b, c = rnd.randint(4, 9), rnd.randint(10, 19), rnd.randint(20, 60)
    pts = 3 if n <= 4 else 4
    right = a * b - c
    stem = ("SYNTHETIC. A %s packs %d %ss in each of %d %ss and sells %d %ss before noon (item %d). You are asked to choose the statement that tells how many %ss are left."
            % (th, a, thing, b, box, c, thing, n, thing))
    opts = ["%d %ss are left, because %d x %d = %d and %d - %d = %d." % (right, thing, a, b, a * b, a * b, c, right),
            "%d %ss are left, because the %ss sold are added to the %ss packed." % (a * b + c, thing, thing, thing),
            "%d %ss are left, because only the number of %ss is counted, not the %ss in them." % (b - a, thing, box, thing),
            "%d %ss are left, because the %ss are subtracted from the %ss and the %s is ignored." % (a * b - c - a, thing, thing, box, tool),
            "%d %ss are left, because each %s sold takes one %s away from the total." % (a * b - c + b, thing, thing, box)]
    ans = rnd.randrange(5)
    opts[0], opts[ans] = opts[ans], opts[0]
    wr = {}
    for i in range(5):
        if i != ans:
            wr[str(i)] = "Option {o%d} fails: the count does not follow the packing and selling of the %ss." % (i, thing)
    return {"id": "c%d_%02d" % (ch, n), "type": "choice", "chapter": ch, "points": pts, "synthetic": True, "stem": stem,
            "tip": "boxes times items, then subtract.", "options": opts, "answer": ans,
            "steps": ["Multiply %d by %d to get %d." % (a, b, a * b), "Subtract the %d sold: %d - %d = %d." % (c, a * b, c, right), "The statement with %d is option {o%d}." % (right, ans)],
            "why_right": "Option {o%d} multiplies first and then subtracts the sold %ss." % (ans, thing), "why_wrong": wr}

def numeric_template(ch, t):
    th, thing, box, tool = THEMES[ch]
    can4 = (t == 4)
    insts = []
    for i in range(8):
        a, b, c = 3 + i * 2 + t, 5 + i + t * 3, 11 + i * 7 + t
        if t == 1:
            stem = "SYNTHETIC. A %s has %d %ss with %d %ss in each, and %d more %ss arrive. You are asked to calculate how many %ss it has now." % (th, a, box, b, thing, c, thing, thing)
            key = a * b + c; steps = ["Multiply %d by %d = %d." % (a, b, a * b), "Add %d: %d + %d = %d." % (c, a * b, c, key)]
            wrong = [(a * b, "forgot the arrivals"), (a + b + c, "added everything"), (a * (b + c), "multiplied the arrivals too")]
        elif t == 2:
            stem = "SYNTHETIC. A %s sells %d %ss a day for %d days and then throws away %d. You are asked to calculate how many %ss were sold and kept." % (th, a + 20, thing, b + 4, c, thing)
            key = (a + 20) * (b + 4) - c; steps = ["Multiply %d by %d = %d." % (a + 20, b + 4, (a + 20) * (b + 4)), "Subtract %d: %d." % (c, key)]
            wrong = [((a + 20) * (b + 4), "forgot the loss"), (a + 20 + b + 4 - c, "added days"), ((a + 20) * (b + 4) + c, "added the loss")]
        elif t == 3:
            stem = "SYNTHETIC. A %s shares %d %ss equally between %d %ss and keeps %d %ss. You are asked to calculate how many %ss each %s gets." % (th, (a + 3) * (b + 2) + c, thing, b + 2, box, c, thing, thing, box)
            key = (a + 3); steps = ["Take away the kept %d: %d." % (c, (a + 3) * (b + 2)), "Divide by %d: %d." % (b + 2, key)]
            wrong = [((a + 3) * (b + 2) + c) // (b + 2), ("forgot to keep").__len__() + key, key + c]
            wrong = [(wrong[0], "forgot the kept ones"), (wrong[1], "wrong count"), (wrong[2], "added kept")]
        else:
            stem = "SYNTHETIC. A %s pays %d coins for each %s and buys %d %ss, then gets %d coins back. You are asked to calculate how many coins it paid in all." % (th, a * 10 + 5, thing, b, thing, c)
            key = (a * 10 + 5) * b - c; steps = ["Multiply %d by %d = %d." % (a * 10 + 5, b, (a * 10 + 5) * b), "Subtract %d: %d." % (c, key)]
            wrong = [((a * 10 + 5) * b, "forgot the coins back"), ((a * 10 + 5) * b + c, "added the coins back"), (a * 10 + 5 + b - c, "added instead of multiplying")]
        wrong = [{"value": v, "why": w} for v, w in wrong]
        insts.append({"stem": stem, "key_value": key, "steps": steps, "why_right": "The steps follow the story in order.", "common_wrong": wrong})
    return {"id": "n%d_%d" % (ch, t), "type": "numeric", "chapter": ch, "points": 3, "can_be_4": can4, "synthetic": True, "unit": thing + "s",
            "tip": "do the multiplication first.", "instances": insts}

def matching(ch, n):
    th, thing, box, tool = THEMES[ch]
    prem = ["SYNTHETIC set %d.%d premise %d: the %s used to %s" % (ch, n, i + 1, w, v) for i, (w, v) in enumerate(
        [(tool, "move heavy %ss" % thing), ("label", "name a %s" % box), ("scale", "weigh a %s" % thing), ("list", "count the %ss" % thing)])]
    resp = ["Response %d.%d.%d about %s work, number %d" % (ch, n, i + 1, th, i + 1) for i in range(5)]
    rnd = random.Random(ch * 100 + n)
    perm = rnd.sample(range(5), 4)
    return {"id": "m%d_%d" % (ch, n), "type": "matching", "chapter": ch, "synthetic": True,
            "intro": "SYNTHETIC. Four jobs of a %s are listed. You are asked to match each job with the tool that fits it; one response is not used." % th,
            "tip": "match by purpose.", "premises": prem, "responses": resp, "answer": perm,
            "steps": ["Match each job with its tool.", "Leave the unused response aside."], "why_right": "Each response names the purpose of one job.",
            "why_wrong_rows": ["The other responses name a different purpose for this job."] * 4}

def ordering(ch, n):
    th, thing, box, tool = THEMES[ch]
    right = ["Open the %s." % th, "Count the %ss." % thing, "Put the %ss in a %s." % (thing, box), "Label the %s." % box, "Close the %s." % th]
    disp = [3, 0, 4, 1, 2]
    steps = ["SYNTHETIC %d.%d: %s" % (ch, n, right[d]) for d in disp]
    ans = [0] * 5
    for pos, d in enumerate(disp):
        ans[pos] = d + 1
    return {"id": "o%d_%d" % (ch, n), "type": "ordering", "chapter": ch, "synthetic": True,
            "intro": "SYNTHETIC. Five tasks of a %s are listed. You are asked to put the five tasks in the order in which they are done, 1 for the first." % th,
            "tip": "open first, close last.", "steps": steps, "answer": ans,
            "steps_solution": ["Opening comes first.", "Counting follows.", "Packing follows counting.", "Labelling follows packing.", "Closing is last."],
            "why_right": "The day runs from opening to closing.", "why_wrong_rows": ["This task has a fixed place in the day."] * 5}

def fill(ch, n):
    th, thing, box, tool = THEMES[ch]
    bank = ["entry %d.%d.%d (%s)" % (ch, n, i + 1, w) for i, w in enumerate(["packed", "counted", "sold", "weighed", "stored"])]
    rnd = random.Random(ch * 10 + n)
    a1, a2 = rnd.sample(range(5), 2)
    return {"id": "f%d_%d" % (ch, n), "type": "fill", "chapter": ch, "synthetic": True,
            "stem": "SYNTHETIC. Two sentences about a %s have a blank each. You are asked to fill each blank with the bank entry that makes the sentence true." % th,
            "tip": "read both sentences first.",
            "bank": bank, "blanks": [{"sentence": "At the %s the %ss are ____ before they leave (set %d.%d, blank 1)." % (th, thing, ch, n), "answer": a1},
                                     {"sentence": "At the %s the %ss are ____ at the end of the day (set %d.%d, blank 2)." % (th, box, ch, n), "answer": a2}],
            "steps": ["Read each sentence.", "Pick the entry that fits."], "why_right": "Each entry fits one sentence.",
            "why_wrong_entries": {str(i): "This entry does not fit the sentence." for i in range(5)}}

WQ = "Why this question: SYNTHETIC reason line shown after the worked solution."

def family(ch, fam, prefix):
    tpls = []
    for t in range(1, 7):
        insts = []
        for i in range(8):
            a, b, c = 4 + i + t, 6 + 2 * i + t, 3 + 5 * i + t * 2
            key = a * b + c
            insts.append({"stem": "SYNTHETIC family %s: a crate holds %d pens, there are %d crates\nand %d loose pens (case %d.%d). You are asked to calculate how many pens there are." % (fam, a, b, c, t, i),
                          "key_value": key, "steps": ["Multiply %d by %d = %d." % (a, b, a * b), "Add %d = %d." % (c, key)], "why_right": "Crates first, then loose pens.",
                          "common_wrong": [{"value": a * b, "why": "forgot loose pens"}, {"value": a + b + c, "why": "added all"}, {"value": a * (b + c), "why": "multiplied loose pens"}]})
        tpls.append({"id": "%s_%d" % (prefix, t), "type": "numeric", "chapter": ch, "family": fam, "points": 3, "can_be_4": t == 6, "synthetic": True, "unit": "pens",
                     "tip": "Crates times pens, then add.", "why_question": WQ, "instances": insts})
    return {"chapter": ch, "family": fam, "synthetic": True, "items": tpls}

def chapter_file(ch):
    items = [choice(ch, n) for n in range(1, 11)] + [numeric_template(ch, t) for t in range(1, 5)] + [matching(ch, n) for n in range(1, 4)] \
        + [ordering(ch, n) for n in range(1, 3)] + [fill(ch, n) for n in range(1, 5)]
    return {"chapter": ch, "synthetic": True, "items": items}

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    allitems = []
    for ch in range(1, 7):
        d = chapter_file(ch)
        json.dump(d, open(os.path.join(out, "mock_bank_ch%d_v1_0_0.json" % ch), "w"), indent=1)
        allitems += d["items"]
    f1 = family(1, "weighted_price", "n1x"); f2 = family(2, "fee_selection", "n2x"); f3 = family(3, "release_tags", "n3x"); f4 = family(4, "hash_search", "n4x"); f5 = family(5, "gap_scan", "n5x")
    for ff, nm in ((f1, "1x"), (f2, "2x"), (f5, "5x")):
        json.dump(ff, open(os.path.join(out, "mock_bank_ch%s_v1_0_0.json" % nm), "w"), indent=1)
    json.dump(f3, open(os.path.join(out, "mock_bank_ch3x_v1_0_0.json"), "w"), indent=1); json.dump(f4, open(os.path.join(out, "mock_bank_ch4x_v1_0_0.json"), "w"), indent=1)
    json.dump({"synthetic": True, "items": allitems + f1["items"] + f2["items"] + f3["items"] + f4["items"] + f5["items"]}, open(os.path.join(out, "mock_bank_sample_families.json"), "w"), indent=1)
    json.dump({"synthetic": True, "items": allitems + f3["items"]}, open(os.path.join(out, "mock_bank_sample_one_family.json"), "w"), indent=1)
    json.dump({"synthetic": True, "items": allitems}, open(os.path.join(out, "mock_bank_sample.json"), "w"), indent=1)
    print("sample bank written:", len(allitems), "units")
