#!/usr/bin/env python3
"""Build the PRIVATE exclusion index of every delivered SEN0401 exam item (mock plan, 'NEW items only').
Reads: CME private items files (sen0401_exam_items*.json, private/ and top level), every papers_midterm_v* folder
(docx text of paper and key; pdf text where no docx exists; key json), papers_v7_synthetic is NOT delivered (excluded, reported).
Writes ONLY into the private CME folder mock/exclusion/. The log prints ids, counts and hashes, never text."""
import json, glob, os, sys, hashlib, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_exclusion_lib_v1_0_0 import *

EXAM = "/home/claude/CME/exams/SEN0401/08-tooling/exam"
OUT = EXAM + "/mock/exclusion/sen0401_mock_exclusion_index_v1_0_0.json"

stems, opts, nums, docs = {}, {}, [], {}
sigs, taglists = {}, {}   # stems: normkey -> {id, text}; opts: normtext -> [ids]

def add_stem(i, text):
    ns = re.findall(r"\d+", str(text))
    if len(ns) >= 4 and tuple(ns) not in sigs:
        sigs[tuple(ns)] = i
    tg = re.findall(r"v\d+(?:\.\d+)+", str(text))
    if len(tg) >= 3 and tuple(tg) not in taglists:
        taglists[tuple(tg)] = i
    t = norm(text)
    if len(t.split()) >= 6 and t not in stems:
        stems[t] = i

def add_opt(i, text):
    t = norm(text)
    if len(t.split()) >= MIN_OPT_TOKENS and t not in opts:
        opts[t] = i

def walk_item(fid, it):
    iid = fid + "#" + str(it.get("key") or it.get("id") or it.get("label") or "?")
    for k in ("q", "stem", "intro", "text"):
        if isinstance(it.get(k), str):
            add_stem(iid, it[k])
    for k in ("options", "responses", "bank", "distractors", "steps"):
        v = it.get(k)
        if isinstance(v, list):
            for x in v:
                if isinstance(x, str):
                    add_opt(iid, x)
                elif isinstance(x, dict) and isinstance(x.get("text"), str):
                    add_opt(iid, x["text"])
    for p in (it.get("premises") or []):
        t = p["text"] if isinstance(p, dict) else p
        add_opt(iid, t)
        if isinstance(p, dict) and isinstance(p.get("match"), str):
            add_opt(iid, p["match"])
    def blanks(bl):
        for b in bl or []:
            if isinstance(b, dict):
                if isinstance(b.get("text"), str):
                    add_opt(iid, b["text"]); add_stem(iid, b["text"])
                if isinstance(b.get("answer"), str):
                    add_opt(iid, b["answer"])
    blanks(it.get("blanks"))
    for alt in it.get("alternatives") or []:
        if isinstance(alt, dict):
            blanks(alt.get("blanks"))
    if it.get("type") == "NumericAnswer" or "key_value" in it:
        if isinstance(it.get("key_value"), (int, float)):
            nums.append({"id": iid, "unit": norm(it.get("unit", "")), "value": int(it["key_value"]), "stem": norm(it.get("q", ""))})

def walk_json(fid, d):
    n = 0
    if isinstance(d, dict) and isinstance(d.get("items"), list):
        for it in d["items"]:
            if isinstance(it, dict):
                walk_item(fid, it); n += 1
    elif isinstance(d, list):
        for it in d:
            if isinstance(it, dict):
                walk_item(fid, it); n += 1
    return n

def docx_text(path):
    import docx
    d = docx.Document(path)
    out = [p.text for p in d.paragraphs if p.text.strip()]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                if c.text.strip():
                    out.append(c.text)
    return out

def pdf_text(path):
    from pypdf import PdfReader
    lines = []
    for pg in PdfReader(path).pages:
        lines += (pg.extract_text() or "").splitlines()
    paras, cur = [], ""
    for ln in lines:
        if re.match(r"^\s*(?:[A-E][\.\)]|\d+[a-c]?[\.\)]|Tip:|Question|SEN0401)", ln) and cur:
            paras.append(cur); cur = ln
        else:
            cur = (cur + " " + ln).strip()
    if cur:
        paras.append(cur)
    return paras

def main():
    rep = {"json_files": [], "doc_files": [], "skipped": []}
    files = sorted(set(glob.glob(EXAM + "/sen0401_exam_items*.json") + glob.glob(EXAM + "/private/sen0401_exam_items*.json")))
    files += sorted(glob.glob(EXAM + "/papers_midterm_v*/*key.json"))
    for f in files:
        rel = os.path.relpath(f, EXAM)
        try:
            d = json.load(open(f))
        except Exception as e:
            rep["skipped"].append([rel, "json error"]); continue
        n = walk_json(rel, d)
        rep["json_files"].append([rel, n])
    for folder in sorted(glob.glob(EXAM + "/papers_midterm_v*")):
        fs = sorted(glob.glob(folder + "/*paper*.docx") + glob.glob(folder + "/*key*.docx"))
        have = {os.path.splitext(os.path.basename(x))[0] for x in fs}
        for p in sorted(glob.glob(folder + "/*.pdf")):
            b = os.path.splitext(os.path.basename(p))[0]
            if b.endswith("_sheet") or "answersheet" in b:
                continue
            if b not in have:
                fs.append(p)
        for f in fs:
            rel = os.path.relpath(f, EXAM)
            try:
                paras = docx_text(f) if f.endswith(".docx") else pdf_text(f)
            except Exception as e:
                rep["skipped"].append([rel, "read error " + type(e).__name__]); continue
            allg = set()
            for j, p in enumerate(paras):
                p2 = strip_label(p)
                add_stem(rel + "#p%d" % j, p2)
                add_opt(rel + "#p%d" % j, p2)
                allg |= grams(toks(p2))
            # whole-document 5-grams across paragraph joins (stems wrapped over lines)
            full = toks(" ".join(paras))
            allg |= grams(full)
            docs[rel] = sorted(" ".join(g) for g in allg)
            rep["doc_files"].append([rel, len(paras)])
    idx = {"version": "1.0.0", "note": "PRIVATE exclusion index of delivered SEN0401 exam items; never commit to a public repository",
           "stems": [{"id": v, "t": k} for k, v in stems.items()],
           "options": [{"id": v, "t": k} for k, v in opts.items()],
           "numeric": nums, "documents": docs,
           "sigs": [{"id": v, "sig": list(k)} for k, v in sigs.items()], "taglists": [{"id": v, "tags": list(k)} for k, v in taglists.items()]}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(idx, open(OUT, "w"), ensure_ascii=False)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("exclusion index built (counts only, no text)")
    print("json files:", len(rep["json_files"]), "items read:", sum(n for _, n in rep["json_files"]))
    print("document files (docx/pdf):", len(rep["doc_files"]), "paragraphs read:", sum(n for _, n in rep["doc_files"]))
    print("distinct indexed stems:", len(stems), "distinct indexed options/premises/blanks:", len(opts), "indexed numeric key values:", len(nums))
    print("number signatures (4 or more numbers in a stem):", len(sigs), "tag lists (3 or more version tags):", len(taglists))
    print("skipped:", rep["skipped"])
    print("index file:", OUT)
    print("index sha256:", sha)
    for rel, n in rep["json_files"]:
        print("  json", rel, n)
    for rel, n in rep["doc_files"]:
        print("  doc ", rel, n)

main()
