#!/usr/bin/env python3
"""sen0401_ch01_bank_v1_2_0_build v1.0.0: adds one question (no analogy) for the section concept Computing to the Chapter 1 question bank, which lost its only question when the wallet-and-browser comparison was removed (ruling of 2026-11-24). Writes 08-tooling/ch01-page/question_bank_v1_2_0.json (160 items) and the page 03-materials/ch01/page/sen0401_ch01_page_v9_77_0.html beside v9_76_0 (unchanged). Refuses to overwrite. Usage: python3 sen0401_ch01_bank_v1_2_0_build_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def new(p):
    p = os.path.join(R, p); assert not os.path.exists(p), p; return p
NQ = {"concept": "Computing", "level": "Remember",
      "q": "What does a protocol fix between two computers that exchange data?",
      "options": ["The price of each message that passes between them", "The physical cable that links them",
                  "The operating system that both of them must run", "The format and the order in which they exchange data"],
      "answer": 3, "why": "A protocol is a set of rules that defines how data is exchanged, so both sides must agree on its format."}
old = json.load(open(os.path.join(R, "08-tooling/ch01-page/question_bank_v1_1_0.json"), encoding="utf-8"))
pg = open(os.path.join(R, "03-materials/ch01/page/sen0401_ch01_page_v9_76_0.html"), encoding="utf-8", newline="").read()
pat = re.compile(r'(<script type="application/json" id="qbank">)(.*?)(</script>)', re.S); m = pat.search(pg)
ser = lambda J: json.dumps(J, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/")
J = json.loads(m.group(2)); assert ser(J) == m.group(2) and len(J) == 159
J.append(NQ)
json.dump(old[:0] + J, open(new("08-tooling/ch01-page/question_bank_v1_2_0.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
out = pg[:m.start(2)] + ser(J) + pg[m.end(2):]
assert out.count('<meta name="version" content="9.76.0">') == 1 and out.count('{"_version": "9.76.0"') == 1
out = out.replace('<meta name="version" content="9.76.0">', '<meta name="version" content="9.77.0">').replace('{"_version": "9.76.0"', '{"_version": "9.77.0"')
open(new("03-materials/ch01/page/sen0401_ch01_page_v9_77_0.html"), "w", encoding="utf-8", newline="").write(out)
import collections; print(len(J), collections.Counter(q["answer"] for q in J))
