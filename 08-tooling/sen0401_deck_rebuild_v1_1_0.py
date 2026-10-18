#!/usr/bin/env python3
"""sen0401_deck_rebuild v1.1.0 (v1.0.0 plus the names of decks 5 to 7 and the lecture export version: 1_3_0 for decks 1 to 4, whose 1_2_0 is committed) - rebuilds the deck of chapter 1 to 7 as a new version on the same pipeline as decks 5 to 7 (owner's coordinator, 2026-10-19):
  0. the chapter's own plan corrections, when chNN-deck/deck_patch_v<new>.py exists (a function patch(plan));
  0b. every 'Python x.y.z' of the plan is set to the interpreter of the newest examples_out recording of the chapter;
  1. the notes of the newest plan are rewritten into short reader's prose by sen0401_notes_rewrite_v1_0_0.py (2-4 sentences, at most 100 words, no presenter label);
  2. the plan is drawn by sen0401_deck_render_v1_3_0.js (no SEN_LITE), repaired by sen0401_deck_ooxml_fix_v1_0_0.py and stamped by office_stamp_v1_0_0.py;
  3. the pptx is saved to the deck folder and to 03-materials/chNN, and the lecture export v1.2.0 is written.
Nothing committed is edited: the plan, the pptx and the lecture file are new versions.
Usage: sen0401_deck_rebuild_v1_1_0.py NN"""
__version__ = "1.1.0"
import glob, json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
NAME = {1: "SEN0401_Ch01_Introduction_3e_v%s.pptx", 2: "SEN0401_Ch02_HowBitcoinWorks_3e_v%s.pptx", 3: "SEN0401_Ch03_BitcoinCore_3e_v%s.pptx", 4: "SEN0401_Ch04_KeysAndAddresses_3e_v%s.pptx",
        5: "SEN0401_Ch05_WalletRecovery_3e_v%s.pptx", 6: "SEN0401_Ch06_Transactions_3e_v%s.pptx", 7: "SEN0401_Ch07_AuthorizationAuthentication_3e_v%s.pptx"}
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
def run(cmd, cwd=None, env=None):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
n = int(sys.argv[1]); chd = os.path.join(HERE, "ch%02d-deck" % n)
old = sorted(glob.glob(os.path.join(chd, "deck_plan_v*.json")), key=vk)[-1]
v = vk(old); new_v = "%d_%d_0" % (v[0], v[1] + 1); dotted = new_v.replace("_", ".")
newp = os.path.join(chd, "deck_plan_v%s.json" % new_v)
assert not os.path.exists(newp), newp
import importlib.util, tempfile
plan = json.load(open(old))
pf = os.path.join(chd, "deck_patch_v%s.py" % new_v)       # the chapter's own corrections of the plan (geometry, captions, honesty, links), a new file per version
if os.path.exists(pf):
    sp = importlib.util.spec_from_file_location("deck_patch", pf); pm = importlib.util.module_from_spec(sp); sp.loader.exec_module(pm); pm.patch(plan)
    print("patched with", os.path.basename(pf))
# every 'Python x.y.z' of the plan (the console captions, the programs' captions, meta.python) names the interpreter of the NEWEST recording of the chapter's examples
recs = sorted(glob.glob(os.path.join(chd, "examples_out_v*.json")), key=vk)
py = json.load(open(recs[-1]))["_python"]
def retag(x):
    if isinstance(x, str): return re.sub(r"Python \d+\.\d+\.\d+", "Python " + py, x)
    if isinstance(x, list): return [retag(i) for i in x]
    if isinstance(x, dict): return {k: (py if k == "python" and isinstance(v, str) else retag(v)) for k, v in x.items()}
    return x
plan = retag(plan); print("captions and meta.python set to", py, "from", os.path.basename(recs[-1]))
tmp = os.path.join(tempfile.mkdtemp(), "plan_patched.json"); json.dump(plan, open(tmp, "w"), indent=1, ensure_ascii=False)
run([sys.executable, os.path.join(HERE, "sen0401_notes_rewrite_v1_0_0.py"), tmp, newp])
out = os.path.join(chd, "sen0401_ch%02d_deck_v%s.pptx" % (n, new_v)); raw = out[:-5] + "_raw.pptx"
npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
run(["node", os.path.join(HERE, "sen0401_deck_render_v1_3_0.js"), newp, raw], cwd=chd, env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"})
run([sys.executable, os.path.join(HERE, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
run([sys.executable, os.path.join(HERE, "office_stamp_v1_0_0.py"), out, dotted, "SEN0401 Chapter %d" % n])
mat = os.path.join(ROOT, "03-materials", "ch%02d" % n, NAME[n] % new_v)
shutil.copy(out, mat)
run([sys.executable, os.path.join(HERE, "sen0401_lecture_export_v1_2_0.py"), "%02d" % n, os.path.basename(mat), "1_3_0" if n <= 4 else "1_2_0"])
print("built", out, mat)
