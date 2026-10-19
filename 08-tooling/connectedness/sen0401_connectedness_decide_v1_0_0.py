#!/usr/bin/env python3
"""sen0401_connectedness_decide v1_0_0 - second step of the link-discovery ceremony for one chapter (BP-D57 steps 2 and 5): lists the candidates oe_link_discovery still finds
in the chapter's file set (medium and low trust; the high ones were set or declared in the T-Box), requires the spec to hold a reason for each (spec.REJECT_TO maps the target's
local name, or spec.REJECT maps (from, to) local names, to the reason), writes the ledger sen0401_chNN_link_decisions_vX_Y_Z.tsv beside the T-Box in the format of
LINK_DECISIONS_v*.tsv (set stem, family, from, to, reason) and appends the rows to the decisions file. A candidate without a reason stops the run."""
import glob, importlib.util, os, re, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); KEY = sys.argv[1]
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location("spec", os.path.join(HERE, "spec_%s.py" % KEY)); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
sub = ("ch" + KEY) if KEY != "numbers" else "numbers"
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]
RD = os.path.join(REPO, "03-materials", sub, "rdodi")
tb = sorted(glob.glob(os.path.join(RD, "sen0401_%s_domain_tbox_v*.ttl" % sub)), key=vk)[-1]
nvu = "_".join(map(str, vk(tb)))
out = tempfile.mktemp(suffix=".tsv")
subprocess.run([sys.executable, "-B", "/home/claude/Ontologies/repo-tooling/oe_link_discovery_v1_0_1.py", REPO, "--only", "03-materials/%s/" % sub, "--candidates", out], capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
rows = [l.rstrip("\n").split("\t") for l in open(out, encoding="utf-8")][1:]
ln = lambda u: u.split("#")[-1]
rej, mdrows, missing = [], [], []
for r in rows:
    st, fam, kind, trust, fr, to, ev = r[:7]
    reason = getattr(S, "REJECT", {}).get((ln(fr), ln(to))) or getattr(S, "REJECT_TO", {}).get(ln(to)) or getattr(S, "REJECT_FROM", {}).get(ln(fr))
    if not reason: missing.append((kind, trust, ln(fr), ln(to), ev)); continue
    rej.append((st, fam, fr, to, reason)); mdrows.append("| %s %s -> %s | %s | rejected | %s |" % (kind, ln(fr), ln(to), trust, reason))
if missing:
    print("NO REASON FOR:"); [print("  ", m) for m in missing]; sys.exit(1)
if rej:
    open(os.path.join(RD, "sen0401_%s_link_decisions_v%s.tsv" % (sub, nvu)), "w", encoding="utf-8").write("".join("\t".join(x) + "\n" for x in rej))
    md = os.path.join(RD, "sen0401_%s_connectedness_decisions_v%s.md" % (sub, nvu)); t = open(md, encoding="utf-8").read()
    if "rejected |" not in t: open(md, "w", encoding="utf-8").write(t.rstrip("\n") + "\n" + "\n".join(mdrows) + "\n\nThe rejected rows are the ledger sen0401_%s_link_decisions_v%s.tsv, in the format of LINK_DECISIONS_v*.tsv.\n" % (sub, nvu))
print("decided", len(rej), "candidate(s)")
