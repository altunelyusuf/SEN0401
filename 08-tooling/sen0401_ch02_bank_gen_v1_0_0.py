#!/usr/bin/env python3
"""Writes ch02-page/question_bank_v1_0_0.json from the three item tables of this chapter.

The Apply items take their program from the concept's own worked example in the newest ch02-page/page_data_v*.json: the code is
`print(<the worked example's expression>)` and the correct option is what that program really prints, obtained by running it here.
The correct option of every item is placed at an index chosen by a rotating counter, so that the four answer positions are used
about equally often and the correct option is not systematically the longest. Nothing else about an item is changed.

usage: python3 sen0401_ch02_bank_gen_v1_0_0.py [--out FILE]
Check the result with: python3 question_bank_check_v1_2_0.py 02
"""
__version__ = "1.0.0"
import collections, glob, json, os, runpy, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "ch02-page")
PY = "/root/.local/bin/python3.14"
_vk = lambda x: [int(v) for v in x.rsplit("_v", 1)[1].rsplit(".", 1)[0].split("_")]
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(PAGE, "question_bank_v1_0_0.json")

APPLY = runpy.run_path(os.path.join(HERE, "sen0401_ch02_bank_apply_v1_0_0.py"))["APPLY"]
TEXT = (runpy.run_path(os.path.join(HERE, "sen0401_ch02_bank_text_a_v1_0_0.py"))["TEXT_A"]
        + runpy.run_path(os.path.join(HERE, "sen0401_ch02_bank_text_b_v1_0_0.py"))["TEXT_B"])

pd = sorted(glob.glob(os.path.join(PAGE, "page_data_v*.json")), key=_vk)[-1]
nodes = json.load(open(pd, encoding="utf-8"))["nodes"]
by = {n["id"]: n for n in nodes}
io_ids = [n["id"] for n in nodes if "io" in n]

missing_apply = [i for i in io_ids if i not in {a[0] for a in APPLY}]
missing_text = [n["id"] for n in nodes if n["id"] not in {t[0] for t in TEXT}]
assert not missing_apply, "no Apply item for %s" % missing_apply
assert not missing_text, "no text item for %s" % missing_text

def run(code):
    r = subprocess.run([PY, "-c", code], capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, "%s\n%s" % (code[:120], r.stderr[-300:])
    return r.stdout.strip()

# the correct option goes to a rotating position, in the order 0,1,2,3,0,1,...
pos = 0
def place(correct, wrong):
    global pos
    assert len(wrong) == 3, wrong
    assert correct not in wrong, "a distractor repeats the right answer: %r" % correct
    o = list(wrong); o.insert(pos % 4, correct); a = pos % 4; pos += 1
    return o, a

bank = []
# the items are interleaved by concept, in the order of the page, so a reader of the bank follows the chapter
text_by = collections.defaultdict(list)
for t in TEXT: text_by[t[0]].append(t)
apply_by = collections.defaultdict(list)
for a in APPLY: apply_by[a[0]].append(a)

for n in nodes:
    cid = n["id"]
    for concept, level, q, correct, wrong, why in text_by[cid]:
        o, a = place(correct, wrong)
        bank.append({"concept": concept, "level": level, "q": q, "options": o, "answer": a, "why": why})
    for concept, q, wrong, why in apply_by[cid]:
        code = "print(%s)" % by[concept]["io"]["code"]
        correct = run(code)
        assert correct, "%s: the program printed nothing" % concept
        o, a = place(correct, wrong)
        bank.append({"concept": concept, "level": "Apply", "q": q, "code": code, "options": o, "answer": a, "why": why})

json.dump(bank, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
cnt = collections.Counter(i["answer"] for i in bank)
longest = sum(1 for i in bank if max(i["options"], key=len) == i["options"][i["answer"]])
print("wrote %s: %d items, %d concepts, answer positions %s, correct option longest in %d items (%.0f%%)"
      % (os.path.basename(OUT), len(bank), len({i["concept"] for i in bank}), {p: cnt[p] for p in range(4)}, longest, 100.0 * longest / len(bank)))
