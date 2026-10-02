"""Checker for a SEN0401 chapter's question bank (the newest chNN-page/question_bank_v*.json, or the file named). Generalised from SEN0414's
question_bank_check_v1_1_0.py (which sat inside chapter 1's folder and named its bank): one script for every chapter.
usage: question_bank_check_v1_2_0.py NN [--partial] [BANKFILE]
  --partial   do not require an item for every concept (a seed bank, or a bank still being written); every item present is still checked in full.
Runs every Apply program under Python 3.14.4 and compares its
output with the marked answer; as a compatibility guard for the page (which runs programs in Pyodide, an older CPython) it also
runs each program under every older interpreter found on this machine and requires the same output."""
import glob, json, os, shutil, subprocess, sys, collections
__version__ = "1.2.0"
args = [a for a in sys.argv[1:] if not a.startswith("--")]; PARTIAL = "--partial" in sys.argv
NN = args[0]
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch%s-page" % NN)
_vk = lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")]
PY = "/root/.local/bin/python3.14"
OLDER = sorted({os.path.realpath(p) for p in ("/usr/bin/python3.11", "/usr/bin/python3.12", "/usr/bin/python3.13") if os.path.exists(p)})  # stand-ins for the page's Pyodide
LEVELS = {"Remember", "Understand", "Apply", "Analyze"}
NOOUT = "(no output)"
errors = []

def err(msg):
    errors.append(msg)

BANKFILE = args[1] if len(args) > 1 else sorted(glob.glob(os.path.join(HERE, "question_bank_v*.json")), key=_vk)[-1]
bank = json.load(open(BANKFILE, encoding="utf-8"))
_pd = sorted(glob.glob(os.path.join(HERE, "page_data_v*.json")), key=_vk)[-1]
nodes = json.load(open(_pd, encoding="utf-8"))["nodes"]
quiz = []
for _qf in glob.glob(os.path.join(HERE, "quiz_v*.json")):  # every quiz version, so no item can duplicate any of them
    _q = json.load(open(_qf, encoding="utf-8")); quiz += _q["items"] if isinstance(_q, dict) else _q
quiz_q = {i["q"].strip() for i in quiz}
ids = {n["id"] for n in nodes}
io_ids = {n["id"] for n in nodes if "io" in n}

if not isinstance(bank, list):
    err("bank is not a list"); bank = []

per = collections.defaultdict(list)
for k, it in enumerate(bank):
    tag = f"item {k} ({it.get('concept')})"
    if not isinstance(it, dict):
        err(f"{tag}: not an object"); continue
    allowed = {"concept", "level", "q", "code", "options", "answer", "why"}
    if set(it) - allowed: err(f"{tag}: extra keys {set(it) - allowed}")
    if not {"concept", "level", "q", "options", "answer", "why"} <= set(it):
        err(f"{tag}: missing keys"); continue
    if it["concept"] not in ids: err(f"{tag}: unknown concept")
    per[it["concept"]].append(it)
    if it["level"] not in LEVELS: err(f"{tag}: bad level")
    for f in ("q", "why"):
        if not isinstance(it[f], str) or not it[f].strip() or "\n" in it[f] or "\r" in it[f]:
            err(f"{tag}: {f} must be a non-empty single line")
    o = it["options"]
    if not (isinstance(o, list) and len(o) == 4 and all(isinstance(x, str) and x.strip() and "\n" not in x for x in o)):
        err(f"{tag}: options must be 4 single-line strings"); continue
    if len(set(o)) != 4: err(f"{tag}: options not distinct")
    if any("all of the above" in x.lower() for x in o): err(f"{tag}: 'all of the above'")
    if not (isinstance(it["answer"], int) and not isinstance(it["answer"], bool) and 0 <= it["answer"] < 4):
        err(f"{tag}: bad answer index"); continue
    if "code" in it and not isinstance(it["code"], str): err(f"{tag}: code not a string")
    if it["q"].strip() in quiz_q: err(f"{tag}: duplicates existing quiz item")

for nid in (sorted(ids) if not PARTIAL else []):
    if not per[nid]: err(f"concept {nid}: no item")
for nid in (sorted(io_ids) if not PARTIAL else []):
    if not any(i["level"] == "Apply" and i.get("code") for i in per[nid]):
        err(f"io concept {nid}: no Apply item with code")
    if len(per[nid]) < 2: err(f"io concept {nid}: fewer than 2 items")

# answer balance
cnt = collections.Counter(i["answer"] for i in bank if isinstance(i.get("answer"), int))
for p in (range(4) if not (PARTIAL and len(bank) < 12) else []):   # a seed of fewer than 12 items cannot be balanced
    share = cnt[p] / max(len(bank), 1)
    if not 0.20 <= share <= 0.30: err(f"answer index {p} share {share:.2%} outside 20-30%")

# run Apply code
def run(interp, code):
    try:
        r = subprocess.run([interp, "-c", code], capture_output=True, text=True, timeout=10, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return None
    if r.returncode == 0:
        return r.stdout.strip() or NOOUT
    lines = [l for l in r.stderr.strip().splitlines() if l.strip()]
    return lines[-1].split(":")[0].strip() if lines else "?"

ran = 0; cross = 0
for k, it in enumerate(bank):
    if it.get("level") != "Apply" or not it.get("code"):
        continue
    tag = f"item {k} ({it['concept']})"
    actual = run(PY, it["code"])
    if actual is None:
        err(f"{tag}: timeout"); continue
    ran += 1
    exp = it["options"][it["answer"]]
    if actual != exp:
        err(f"{tag}: real result {actual!r} != option {exp!r}")
    for old in OLDER:
        other = run(old, it["code"])
        cross += 1
        if other != actual:
            err(f"{tag}: {os.path.basename(old)} prints {other!r} but 3.14.4 prints {actual!r}")

lv = collections.Counter(i.get("level") for i in bank)
print("bank:", os.path.basename(BANKFILE), "(partial)" if PARTIAL else "")
print(f"items: {len(bank)}; concepts covered: {sum(1 for n in ids if per[n])}/{len(ids)}; io concepts: {len(io_ids)}")
print("levels:", dict(sorted(lv.items())))
print("answer positions:", {p: cnt[p] for p in range(4)})
print(f"apply programs run under 3.14.4: {ran}; cross-version runs under {[os.path.basename(p) for p in OLDER]}: {cross}")
longest = sum(1 for i in bank if max(i["options"], key=len) == i["options"][i["answer"]])
print(f"correct option is the longest in {longest}/{len(bank)} items")
if errors:
    print(f"FAIL: {len(errors)} problem(s)")
    for e in errors: print(" -", e)
    sys.exit(1)
print("PASS")
