"""Chapter 10 deck 2.2.0 (TK_Deck10_StoryLink_Build): the story BloomFiltersLeak (slide 37) shows the host of its READ link (eprint.iacr.org) as visible text in the link bar.
Only the READ label of slide 37 changes (shortened to fit the renderer's two-line link cell, which prints the host under the label); the plan keeps every other field of deck_plan_v2_1_0.json."""
import json, os, subprocess, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, TOOL)
import sen0401_deck_story_v1_0_0 as ST
VER, VER_US = "2.2.0", "2_2_0"
LABEL = "Gervais et al.: Bloom filter privacy (paper)"
NEWLABEL = "Gervais: Bloom filter privacy (paper)"
plan = json.load(open(os.path.join(HERE, "deck_plan_v2_1_0.json")))
f = ST.items(plan, 37, "factrow")[0]; assert f["linkText"] == LABEL and "eprint.iacr.org" in f["link"]
ST.set_fact(plan, 37, linkText=NEWLABEL)
plan["meta"]["version"] = VER; plan["meta"]["sub"] = "SEN0401, third-edition deck 2.2.0"
p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p)
out = os.path.join(HERE, "sen0401_ch10_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
def run(cmd, env=None):
    r = subprocess.run(cmd, cwd=HERE, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
    if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"})
run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 10"])
mat = os.path.join(ROOT, "03-materials", "ch10", "SEN0401_Ch10_TheBitcoinNetwork_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)
