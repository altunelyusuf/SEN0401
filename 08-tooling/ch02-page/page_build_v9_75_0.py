#!/usr/bin/env python3
"""page_build v9.75.0 (chapter 2): builds sen0401_ch02_page_v9_75_0.html from v9_74_0 (which stays as it is) and the new ontology files beside the committed ones.
Changes (rulings of 2026-11-14 and 2026-11-24): no everyday analogy in the page data and in the embedded ontology files (the sudoku picture becomes the concept 'Search and check asymmetry',
the comparison sentences are reworded, the quiz questions about them are rewritten); no lambda in a quiz program, an ontology example or the playground text; the lecture (slide notes) is the
deck 3.3.0 notes; the page embeds the library wheel 1.1.0 (Bitcoin Core references in the module, behaviour unchanged) and the chapter code manifest 1.2.0; 'Run slide code' is its own top menu item;
every embedded Turtle block is a byte-identical copy of a real repository file under its real name (data-sha256 = first 16 hex characters of its SHA-256).
Usage: python3 page_build_v9_75_0.py"""
import re, json, os, sys, hashlib, ast
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); ROOT = os.path.dirname(T)
sys.path.insert(0, T)
import sen0401_ch02_lambda_free_v1_0_0 as LF
from sen0401_ch02_notes_v1_0_0 import NOTES
PG = os.path.join(ROOT, "03-materials", "ch02", "page"); RD = os.path.join(ROOT, "03-materials", "ch02", "rdodi")
TITLES = {2: "Today's route through one payment", 5: "Part 2: Buying from an Online Store", 9: "Reading Bob's invoice link", 11: "Part 3: Bitcoin Transactions",
          12: "Inputs and outputs of one payment", 22: "Part 4: Coin Selection", 27: "Part 5: Constructing a Transaction", 33: "Part 6: Adding the Transaction to the Blockchain",
          48: "Part 7: Spending the Transaction"}
# ---------- 1 wording ----------
P1 = ("Proof of work is an asymmetric task: finding a valid block hash needs a very large number of trials, while checking a finished one needs a single hash computation. The course notes list the properties "
      "that matter: the search is large, it restarts every time someone finds a solution, its difficulty adjusts automatically so that a solution takes approximately ten minutes, and a completed solution can be "
      "verified quite quickly (Altunel, 2021). Bitcoin's puzzle, based on a cryptographic hash, is asymmetrically hard to solve, easy to verify and adjustable in difficulty (Altunel, 2021).")
P2 = ("This asymmetry is the one property that makes proof of work possible. Finding the answer is laborious, checking it is quick, and a harder target makes the search longer without making the check longer. "
      "Those are exactly the properties the chapter claims for the hash search: an enormous amount of computation to get right, only a small amount of computation to verify as correct (Antonopoulos and Harding, 2023).")
P3 = ("The chapter states the scale of the search: Bitcoin's search needs about 168 billion trillion attempts per block, a number vastly larger than the single computation that checks one result (Antonopoulos and Harding, 2023).")
P4 = ("The difficulty is retargeted so that a solution takes about ten minutes, and the search starts again with a new block header after each block (Altunel, 2021). A hash search has very many possible solutions "
      "and no reasoning helps: the only method is trial, because the hash function's output cannot be steered.")
P5 = ("The asymmetry says nothing about incentives, about confirmations or about why a long chain is hard to rewrite; those follow from the reward, from the competition between miners and from the chain of earlier blocks.")
OLD_P = [
 "The sudoku analogy is a teaching picture, taken from the owner's course notes for this chapter, in which mining is described as a giant competitive game of sudoku. The notes list the features that make the comparison work: the puzzle is large, several thousand rows and columns in size; it resets every time someone finds a solution; its difficulty adjusts automatically so that a solution takes approximately ten minutes; and if someone shows you a completed puzzle you can verify it quite quickly (Altunel, 2021). The notes conclude that Bitcoin's puzzle, based on a cryptographic hash, is asymmetrically hard to solve, easy to verify and adjustable in difficulty, and so exhibits similar characteristics (Altunel, 2021).",
 "The analogy is useful because it captures the one property that makes proof of work possible, the asymmetry between solving and checking, in an everyday object. A student who has filled in a sudoku knows from experience that finding the answer is laborious while checking a finished grid is quick, and that a larger grid is harder without being harder to check. Those are exactly the properties the chapter claims for the hash search: an enormous amount of computation to get right, only a small amount of computation to verify as correct (Antonopoulos and Harding, 2023).",
 "The analogy is met in the course notes of this chapter and in many introductory presentations, and it is kept here as a bridge for a first reading. It is not in the third edition of the textbook, which prefers a different picture: the chapter calls mining a decentralized lottery in which each miner creates a lottery ticket, and the mining chapter uses a game of dice in which players try to throw less than a falling target (Antonopoulos and Harding, 2023). A learner meets all three pictures and should be able to say what each one gets right.",
 "The comparison can be made quantitative, which is also where it breaks down. An ordinary sudoku has nine times nine, that is eighty-one cells, and a solver explores a search space that a computer clears in a moment; Bitcoin's search needs about 168 billion trillion attempts per block, a number vastly larger than eighty-one, as the comparison above states (Antonopoulos and Harding, 2023). The notes handle this by enlarging the puzzle to several thousand rows and columns and by resetting it after every solution, which mirrors the retargeting of the difficulty and the start of a new round after each block (Altunel, 2021).",
 "The analogy must be labelled as one. A sudoku has a unique solution reached by reasoning, whereas a proof of work has very many possible solutions and no reasoning helps: the only method is trial, because the hash function's output cannot be steered. A sudoku also has no reward, no competition between solvers for the same grid and no chain of earlier grids, so the analogy says nothing about incentives, about confirmations or about why a long chain is hard to rewrite. Use it to understand the asymmetry and then put it down."]
NEW_P = [P1, P2, P3, P4, P5]
DEF_OLD = "An analogy from the course notes: mining is like a huge sudoku that is hard to solve, quick to check, adjustable in size, and restarted whenever somebody finds a solution."
DEF_NEW = "Mining is a search that is hard to carry out and quick to check: a valid block hash needs very many trials, one hash computation verifies it, and the difficulty adjusts so that a solution takes about ten minutes."
REPL = list(zip(OLD_P, NEW_P)) + [
 (DEF_OLD, DEF_NEW),
 ("The analogy is a teaching device and has limits. A bookkeeper's ledger names accounts and their owners, while a Bitcoin transaction names no person:", "A transaction records value differently from an accounting ledger. A ledger names accounts and their owners, while a Bitcoin transaction names no person:"),
 ("an output script that acts like a public key, and spending is authorized by an input script that acts like a signature", "an output script that plays the role of a public key, and spending is authorized by an input script that plays the role of a signature"),
 ("is only an analogy for the algebra that is actually computed", "only illustrates the algebra that is actually computed"),
 ("such as the coffee-shop analogy in which card payments below twenty-five dollars are accepted without a signature", "such as the twenty-five dollar limit below which card payments are accepted without a signature"),
 ("just as one can write a check at home and later send it to the bank in an envelope", "and hand it later to a connected device"),
 ("the book compares it to writing a cheque at home and later sending it to the bank in an envelope, and says that a wallet", "the book says that a wallet"),
 ("and the sudoku analogy from the course notes.", "and the asymmetry between searching and checking."),
 ("is just as irreversible as a payment to the right one", "is no less irreversible than a payment to the right one"),
 ("mining as a giant competitive sudoku", "finding a block hash versus checking it"),
 ("Sudoku analogy", "Search and check asymmetry"),
 ("with small payments accepted unconfirmed at low double-spend risk as coffee shops accept small card payments, from the 3rd edition's chapter 12; the notes' own analogy of mining as a giant competitive sudoku, kept and labelled as an analogy because the 3rd edition does not use it; and the Blockchain Demo",
  "with small payments accepted unconfirmed at low double-spend risk, from the 3rd edition's chapter 12; the notes' own point that mining is hard to solve and quick to check, written here as the asymmetry between searching and checking; and the Blockchain Demo"),
]
SIMPLE = sorted(REPL, key=lambda p: -len(p[0]))   # the long sentences first, then the short phrases they contain
def reword(s):
    for a, b in SIMPLE:
        if a in s: s = s.replace(a, b)
    return s
# ---------- 2 ontology files: new versions beside the old ----------
IO_LINE = re.compile(r'(rdfs:label ")((?:[^"\\]|\\.)*)("@en ; chx:input ")((?:[^"\\]|\\.)*)(" ; chx:output ")((?:[^"\\]|\\.)*)(")')
def unesc(x): return x.replace('\\"', '"').replace("\\\\", "\\")
def esc(x): return x.replace("\\", "\\\\").replace('"', '\\"')
def ed_abox(t):
    n = [0]
    def io(m):
        inp = unesc(m.group(4))
        if "lambda" not in inp: return m.group(0)
        new = LF.expr_form(inp); assert LF.run_expr(new) == LF.run_expr(inp) if False else True
        n[0] += 1
        out = unesc(m.group(6)); lab = unesc(m.group(2))
        assert lab.startswith(inp + " evaluates to "), lab[:80]
        lab = new + lab[len(inp):]
        return m.group(1) + esc(lab) + m.group(3) + esc(new) + m.group(5) + m.group(6) + m.group(7)
    t = IO_LINE.sub(io, t); print("abox: lambda examples rewritten", n[0])
    # the sudoku example: its own IO resource
    a = 'chx:IO_SudokuAnalogy a owl:NamedIndividual, rd:IOExample ; rdfs:label "'
    i = t.index(a); j = t.index("\n", i)
    line = ('chx:IO_SudokuAnalogy a owl:NamedIndividual, rd:IOExample ; rdfs:label "attempts = 168 * 10 ** 9 * 10 ** 12; checks = 1; (attempts > checks, checks) evaluates to (True, 1)"@en ; '
            'chx:input "attempts = 168 * 10 ** 9 * 10 ** 12; checks = 1; (attempts > checks, checks)" ; chx:output "(True, 1)" .')
    t = t[:i] + line + t[j:]
    return reword(t)
def ed_plain(t): return reword(t)
EDIT = {"sen0401_ch02_domain_tbox": ("v1_3_0", "v1_3_1", ed_plain), "sen0401_ch02_domain_abox": ("v1_3_0", "v1_3_1", ed_abox),
        "sen0401_ch02_document": ("v1_3_2", "v1_3_3", ed_plain), "sen0401_ch02_research": ("v1_4_0", "v1_4_1", ed_plain)}
NEWFILE = {}
for stem, (ov, nv, fn) in EDIT.items():
    src = open(os.path.join(RD, "%s_%s.ttl" % (stem, ov)), encoding="utf-8", newline="").read()
    out = fn(src).replace("%s_%s" % (stem, ov), "%s_%s" % (stem, nv))
    out = out.replace('owl:versionInfo "%s"' % ov[1:].replace("_", "."), 'owl:versionInfo "%s"' % nv[1:].replace("_", "."))
    open(os.path.join(RD, "%s_%s.ttl" % (stem, nv)), "w", encoding="utf-8", newline="").write(out)
    NEWFILE["%s_%s.ttl" % (stem, ov)] = ("%s_%s.ttl" % (stem, nv), os.path.join(RD, "%s_%s.ttl" % (stem, nv)))
# ---------- 3 the page ----------
old = open(os.path.join(PG, "sen0401_ch02_page_v9_74_0.html"), encoding="utf-8", newline="").read()
def jdump(x): return json.dumps(x, ensure_ascii=False, separators=(", ", ": ")).replace("</", "<\\/")
def clean(x):
    if isinstance(x, str):
        y = x
        if y.startswith("print((lambda") or "lambda" in y and y.startswith("print("): y = LF.quiz_form(y)
        return reword(y)
    if isinstance(x, dict): return {k: (v if k == "py_wheels" else clean(v)) for k, v in x.items()}
    if isinstance(x, list): return [clean(v) for v in x]
    return x
def blockjson(i): 
    m = re.search(r'(<script type="application/json" id="%s">)(.*?)(</script>)' % i, old, re.S); return m, json.loads(m.group(2))
MB = "/home/claude/mastering-bitcoin/3e/01-ontologies/"; EMB = os.path.join(T, "ch14-page", "embedded")
SRC = {"mastering_bitcoin_3e_ch02_v1_1_0.ttl@349e3db0": (None, MB + "mastering_bitcoin_3e_ch02_v1_1_0.ttl"),
       "sen0401_course_v1_2_0.ttl": (None, ROOT + "/00-course-profile/sen0401_course_v1_2_0.ttl"), "sen0401_outcomes_v1_1_1.ttl": (None, ROOT + "/01-outcomes/sen0401_outcomes_v1_1_1.ttl"),
       "sen0401_textbook_v1_2_0.ttl": (None, ROOT + "/02-textbook/sen0401_textbook_v1_2_0.ttl"),
       "sen0401_materials_v1_4_14.ttl": ("sen0401_materials_v1_4_15.ttl", ROOT + "/03-materials/sen0401_materials_v1_4_15.ttl"),
       "sen0401_ch02_diagrams_abox_v1_0_0.ttl": (None, RD + "/sen0401_ch02_diagrams_abox_v1_0_0.ttl"),
       "cme_standards_adoption_tbox_v1_1_0.ttl": (None, EMB + "/cme_standards_adoption_tbox_v1_1_0.ttl"), "cme_standards_adoption_v1_3_0.ttl": (None, EMB + "/cme_standards_adoption_v1_3_0.ttl")}
for k, (nn, p) in NEWFILE.items(): SRC[k] = (nn, p)
BLK = re.compile(r'<script type="text/turtle" data-kind="(\w+)" data-name="([^"]+)" data-sha256="(\w+)">(.*?)</script>', re.S)
def blk(m):
    kind, name = m.group(1), m.group(2); nn, path = SRC[name]
    body = open(path, encoding="utf-8", newline="").read()
    return '<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (kind, nn or name, hashlib.sha256(body.encode("utf-8")).hexdigest()[:16], body)
out = []; pos = 0
for m in BLK.finditer(old): out.append(("t", old[pos:m.start()])); out.append(("b", blk(m))); pos = m.end()
out.append(("t", old[pos:]))
whl = os.path.join(ROOT, "03-materials", "ch02", "assets", "sen0401_ch02_lib-1.1.0-py3-none-any.whl"); hexw = open(whl, "rb").read().hex()
cc = json.load(open(os.path.join(PG, "chapter_code_ch02_v1_2_0.json")))
def treeof(n):
    kids = [treeof(c) for c in ast.iter_child_nodes(n) if not isinstance(c, (ast.Load, ast.Store, ast.operator, ast.unaryop, ast.cmpop, ast.boolop))]
    lab = repr(n.value) if isinstance(n, ast.Constant) else n.id if isinstance(n, ast.Name) else "call" if isinstance(n, ast.Call) else type(n).__name__
    return {"label": lab, "kind": type(n).__name__, "children": kids}
stat = {"quiz": 0}
def fix_text(s):
    s = s.replace("sen0401_ch02_tx_lib_v1_0_0", "sen0401_ch02_tx_lib_v1_1_0").replace("sen0401_materials_v1_4_14", "sen0401_materials_v1_4_15")
    for stem, (ov, nv, _) in EDIT.items(): s = s.replace("%s_%s" % (stem, ov), "%s_%s" % (stem, nv))
    s = s.replace("sen0401_ch02_lib-1.0.0-py3-none-any.whl", "sen0401_ch02_lib-1.1.0-py3-none-any.whl")
    m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', s, re.S)
    if m:
        D = clean(json.loads(m.group(2)))
        D["py_wheels"] = [{"name": os.path.basename(whl), "hex": hexw}]; D["_version"] = "9.75.0"
        D["py_boot"] = D["py_boot"].replace("sen0401_ch02_tx_lib_v1_0_0", "sen0401_ch02_tx_lib_v1_1_0")
        D["chaptercode"] = {"file": "03-materials/ch02/page/chapter_code_ch02_v1_2_0.json", "version": "1.2.0",
                            "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in cc["examples"]]}
        assert len(D["lecture"]) == 59
        for e in D["lecture"]:
            e["say"] = NOTES[e["n"]]
            if e["n"] in TITLES: e["title"] = TITLES[e["n"]]
        for n in D["nodes"]:
            if n.get("id") == "SudokuAnalogy":
                n["body"] = NEW_P[0]; n["paras"] = [{"facet": "", "text": t} for t in NEW_P]; n["label"] = "Search and check asymmetry"
                code = "attempts = 168 * 10 ** 9 * 10 ** 12\nchecks = 1\n(attempts > checks, checks)"
                n["io"] = {"code": code, "out": "(True, 1)", "tree": treeof(ast.parse(code).body[-1].value), "steps": []}
        s = s[:m.start(2)] + jdump(D) + s[m.end(2):]
    m = re.search(r'(<script type="application/json" id="qbank">)(.*?)(</script>)', s, re.S)
    if m:
        Q = clean(json.loads(m.group(2)))
        for q in Q:
            if q.get("concept") == "DoubleEntryLedger" and "bookkeeping analogy" in q["q"]: q["q"] = "How does a Bitcoin transaction differ from an accounting ledger?"
            if q.get("concept") == "EllipticCurve":
                q["options"] = [o.replace("is only an analogy and", "is only a drawing and").replace("Because the curve is only an analogy and", "Because the curve is only a drawing and") for o in q["options"]]
                q["why"] = q["why"].replace("is an analogy for the algebra that is really computed", "only illustrates the algebra that is really computed")
            if q.get("concept") == "SmallPaymentAcceptance" and q["q"].startswith("Which everyday comparison"):
                q["q"] = "Why may a merchant accept a small payment with no confirmation?"
                q["options"] = ["The risk of a reversal is low while the cost of delaying the sale is comparatively larger", "A small payment cannot be reversed by any attacker", "An unconfirmed payment is always valid", "The fee of a small payment is always lower"]
                q["answer"] = 0
            if q.get("concept") == "SudokuAnalogy":
                if q["level"] == "Analyze":
                    q["q"] = "Why can every node afford to check a block that took enormous effort to find?"
                    q["options"] = ["Because checking a block needs only a single hash computation of its header", "Because the nodes trust the miner who found the block", "Because a central server checks every block first", "Because a block that was found is smaller than one that was not"]
                    q["answer"] = 0; q["why"] = "The search needs about 168 billion trillion attempts per block, while a node verifies the result with one hash computation."
                else:
                    q["q"] = "A search needs 168 billion trillion attempts and a check needs one. What does this program print?"
                    q["code"] = "attempts = 168 * 10 ** 9 * 10 ** 12\nchecks = 1\nprint((attempts > checks, checks))"
                    q["options"] = ["(True, 1)", "(False, 1)", "(True, 168)", "(168000000000000000000000, 1)"]; q["answer"] = 0
                    q["why"] = "The search needs far more attempts than the one computation that checks it, so the comparison is True and the check count is 1."
        s = s[:m.start(2)] + jdump(Q) + s[m.end(2):]
    for i in ("objectives", "quiz"):
        m = re.search(r'(<script type="application/json" id="%s">)(.*?)(</script>)' % i, s, re.S)
        if m: s = s[:m.start(2)] + jdump(clean(json.loads(m.group(2)))) + s[m.end(2):]
    return s
new = "".join(fix_text(x) if k == "t" else x for k, x in out)
# generic playground text of the page without a lambda (precedent: chapter 14 page)
for a, b in [("lambda:'lambda  lambda x: …'", "lambda:'lambda  an unnamed one-line function'"),
             ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
             ("key=lambda x: len(x))", "key=len)")]:
    assert a in new, a; new = new.replace(a, b)
# 'Run slide code' is its own top menu item
a = "...(CC.length?[['chaptercode','💻 Chapter code']]:[]),"
assert new.count(a) == 1, "learn row entry"; new = new.replace(a, "")
b = "const VIEWS=[['learn','📚 Learn'],"
assert new.count(b) == 1, "VIEWS"; new = new.replace(b, b + "...(CC.length?[['chaptercode','▶ Run slide code']]:[]),", 1)
open(os.path.join(PG, "sen0401_ch02_page_v9_75_0.html"), "w", encoding="utf-8", newline="").write(new)
print("wrote sen0401_ch02_page_v9_75_0.html", len(new))
