"""Chapter 14 deck 2.0.1 (TK_Deck14_StoryLink2_Build): the story SpillmanChannels (slide 23) shows the host of its READ link (web.archive.org) as visible text in the link bar, beside the live link.
Only the READ label of slide 23 changes; the plan keeps every other field of deck_plan_v2_0_0.json. Same method as the chapter 12 deck 3.0.2."""
import json, os, subprocess, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.dirname(HERE); ROOT = os.path.dirname(TOOL)
sys.path.insert(0, TOOL)
import sen0401_deck_story_v1_0_0 as ST
VER, VER_US = "2.0.1", "2_0_1"
LABEL = "Reply: Anti DoS for tx replacement (list post)"
NEWLABEL = "Reply: Anti DoS (list post); archived: web.archive.org"
plan = json.load(open(os.path.join(HERE, "deck_plan_v2_0_0.json")))
f = ST.items(plan, 23, "factrow")[0]; assert f["linkText"] == LABEL
ST.set_fact(plan, 23, linkText=NEWLABEL)
NOTES = {
 22: "Emma funds one hour of video, at 1,000 satoshis a second, in a two-of-two script output. Emma alone cannot spend it, and both together can. The witness script begins with a 2 and ends with a 2 and CHECKMULTISIG. It is example 7 in the chapter code tab of the course page.",
 40: "Lightning nodes talk over an encrypted link, and the specification prints a test vector with fixed keys. We rerun the handshake and compare the three outputs, the two acts and the transport key. The sizes are 50, 66 and 39 bytes. It is example 15 in the chapter code tab of the course page.",
 42: "A node made an invoice for 100,000,000,000 millisatoshis and the library parsed it; it asks 80 blocks for the last hop. The secret, hashed once, equals the payment hash. The invoice in BOLT 11 is dated 1 June 2017. It is example 17 in the chapter code tab of the course page.",
}
for n, t in NOTES.items():
    assert len(plan["slides"][n-1]["notes"].split()) > 40; plan["slides"][n-1]["notes"] = t
plan["meta"]["version"] = VER; plan["meta"]["sub"] = "SEN0401, third-edition deck 2.0.1"
plan["meta"]["redesign"] = "2026-10-25, task TK_Deck14_StoryLink2_Build (2.0.1 over 2.0.0): the notes of slides 22, 40 and 42 are cut to 4 sentences within 100 words (same facts, same pointer to the chapter code example); the link bar of the story Spillman channels (slide 23) now shows the host web.archive.org of the story record's READ link as visible text beside the live link; nothing else changes. Previous: " + plan["meta"]["redesign"]
p = os.path.join(HERE, "deck_plan_v%s.json" % VER_US); json.dump(plan, open(p, "w"), indent=1, ensure_ascii=False); print("written", p)
out = os.path.join(HERE, "sen0401_ch14_deck_v%s.pptx" % VER_US); raw = out[:-5] + "_raw.pptx"
npath = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
def run(cmd, env=None):
    r = subprocess.run(cmd, cwd=HERE, env=dict(os.environ, **(env or {})), capture_output=True, text=True); print(r.stdout.strip())
    if r.returncode: print(r.stderr.strip()); raise SystemExit("FAILED: " + " ".join(cmd))
run(["node", os.path.join(TOOL, "sen0401_deck_render_v2_1_0.js"), p, raw], env={"NODE_PATH": npath, "SEN_CAPTION_TOP": "1"})
run(["python3", os.path.join(TOOL, "sen0401_deck_ooxml_fix_v1_0_0.py"), raw, out]); os.remove(raw)
run(["python3", os.path.join(TOOL, "office_stamp_v1_0_0.py"), out, VER, "SEN0401 Chapter 14"])
mat = os.path.join(ROOT, "03-materials", "ch14", "SEN0401_Ch14_SecondLayerApplications_3e_v%s.pptx" % VER_US); shutil.copy(out, mat); print("built", out, mat)
