#!/usr/bin/env python3
"""sen0401_code_findings_measure v1_0_0 - measured facts on the chapter code of the SEN0401 slides and pages (owner findings of 2026-10-30 02:00 Istanbul). Written by the lineage agent; facts only, from the newest deck and page of each chapter.
(1) prompt lines ('>>> ' and '... ') in the slide text; (2) where the page offers code examples: the Playground list (concept examples, node.io.code) against the Chapter code list (the slide examples, in slide order); (3) the lambda word: slides, page data, and what kind of code carries it;
(4) slide code lines (prompts stripped, exact text, whitespace at the ends ignored) that occur nowhere in the page's strings. Usage: measure.py [--json FILE] | --selftest"""
import collections, glob, json, os, re, sys
sys.dont_write_bytecode = True
R = "/home/claude/sen0401/03-materials/"
PROMPT = re.compile(r"^(>>> |\.\.\. |\.\.\.$)")
def strip_prompt(l): return PROMPT.sub("", l, count=1)
def lam_kind(code):
    if re.search(r"\(lambda \w+: \(exec\(", code): return "wrapper: the example is stored as one expression, (lambda g: (exec(...)))"
    if re.search(r"^\s*\w+\s*=\s*lambda", code, re.M): return "setup helper: name = lambda ..."
    if "lambda" in code: return "lambda inside an example"
    return None
def strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from strings(v)
    elif isinstance(o, list):
        for v in o: yield from strings(v)
def latest(pat):
    fs = glob.glob(pat); return sorted(fs, key=lambda x: [int(v) for v in re.findall(r"_v(\d+)_(\d+)_(\d+)", x)[-1]])[-1]
def selftest():
    ok = strip_prompt(">>> x = 1") == "x = 1" and strip_prompt("... y = 2") == "y = 2" and strip_prompt("...") == "" and strip_prompt("print(1)") == "print(1)"
    ok &= lam_kind('(lambda g: (exec("a=1"), g)[1])({})') .startswith("wrapper") and lam_kind("h = lambda x: x").startswith("setup") and lam_kind("sorted(a, key=lambda t: t)").startswith("lambda inside") and lam_kind("print(1)") is None
    print("SELFTEST", "PASS" if ok else "FAIL"); return ok
def main():
    from pptx import Presentation
    out = {}
    for n in range(1, 9):
        deck = latest(R + "ch%02d/SEN0401_Ch%02d_*_3e_v*.pptx" % (n, n)); page = latest(R + "ch%02d/page/sen0401_ch%02d_page_v*.html" % (n, n))
        slides = {}; 
        for i, s in enumerate(Presentation(deck).slides, 1):
            for sh in s.shapes:
                if sh.has_text_frame:
                    for p in sh.text_frame.paragraphs:
                        for ln in "".join(r.text for r in p.runs).split("\n"): slides.setdefault(i, []).append(ln)
        lines = [(i, l) for i, ls in slides.items() for l in ls]
        pr = [(i, l) for i, l in lines if PROMPT.match(l)]
        # code lines of the slides: the lines of shapes that carry a prompt, plus the continuation lines (outputs) are not counted
        code = [(i, strip_prompt(l).rstrip()) for i, l in pr]; code = [(i, l) for i, l in code if l.strip()]
        h = open(page, encoding="utf8").read(); m = re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>', h, re.S); D = json.loads(m.group(1))
        blob = "\n".join(strings(D)); plines = {l.rstrip() for l in blob.split("\n")}
        unm = [(i, l) for i, l in code if l not in plines]
        cc = (D.get("chaptercode") or {}).get("examples", []); nodes = [x for x in D["nodes"] if x.get("io")]
        lam_nodes = collections.Counter(lam_kind(x["io"]["code"]) for x in nodes if lam_kind(x["io"]["code"]))
        lam_cc = collections.Counter(lam_kind(e.get("code", "")) for e in cc if lam_kind(e.get("code", "")))
        lam_slides = sum("lambda" in l for _, l in lines)
        out[n] = {"deck": os.path.basename(deck), "page": os.path.basename(page), "slides_with_prompt_lines": len({i for i, _ in pr}), "prompt_lines": len(pr), "code_lines_after_stripping": len(code),
                  "slide_code_lines_found_nowhere_in_the_page": len(unm), "unmatched_slides": sorted({i for i, _ in unm}), "unmatched_examples": [l for _, l in unm][:5],
                  "playground_group_examples_from_this_chapter(concept examples)": len(nodes), "chapter_code_examples(slide examples)": len(cc), "chapter_code_in_slide_order": [(e.get("order"), e.get("name"), e.get("slide")) for e in cc],
                  "lambda_word_in_slide_text_lines": lam_slides, "lambda_word_in_page_html": h.count("lambda"), "lambda_in_playground_concept_examples": dict(lam_nodes), "lambda_in_chapter_code_examples": dict(lam_cc),
                  "concept_nodes_whose_text_teaches_lambda": [x["label"] for x in D["nodes"] if re.search(r"\blambda\b", (x.get("label", "") + " " + (x.get("definition") or "")), re.I)]}
    print(json.dumps(out, indent=1))
    if "--json" in sys.argv: json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "x"), indent=1)
if __name__ == "__main__": sys.exit(0 if selftest() else 1) if "--selftest" in sys.argv else main()
