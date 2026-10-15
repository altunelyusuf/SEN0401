#!/usr/bin/env python3
"""provenance_make v1_0_0 (SEN0401 chapter page). Writes 03-materials/chNN/assets/ASSETS_PROVENANCE_v1_2_0.md for the wheel of pywheels_v1_0_0.json: sha256, the shipped files with a licence status
by file-name class, and the files left out with the examples that are recorded because of them (from standin_v1_0_0.json). Usage: provenance_make_v1_0_0.py NN"""
__version__ = "1.0.0"
import hashlib, json, os, re, sys, zipfile
NN = sys.argv[1]; H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch%s" % NN, "assets")
pw = json.load(open(os.path.join(H, "pywheels_v1_0_0.json"))); so = json.load(open(os.path.join(H, "standin_v1_0_0.json")))
wf = pw["wheels"][0]["file"]; wp = os.path.join(A, wf); z = zipfile.ZipFile(wp)
LIC = [("bip-", "the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain)"), ("bitcoind_help_", "MIT (Bitcoin Core)"), ("core_", "MIT (Bitcoin Core)"),
       ("book_", "CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition)"), ("optech_", "CC BY 4.0 (Bitcoin Optech)"), ("nakamoto_2008_bitcoin", "MIT, as published on bitcoin.org"),
       ("regtest_run_", "this course's own run record"), ("bitcoinwiki_", "CC BY 3.0 (Bitcoin Wiki)"), ("bolt0", "CC BY 4.0 (stated in the BOLT file itself)"), ("bolt1", "CC BY 4.0 (stated in the BOLT file itself)"), ("lnd_", "MIT (lnd)"), ("wikipedia_", "CC BY-SA (Wikipedia)")]
rows = []; mods = []
for i in z.infolist():
    n = i.filename
    if n.startswith(NN and "ch%s-evidence/" % NN):
        b = n.split("/", 1)[1]; lic = next(l for p, l in LIC if b.startswith(p)); rows.append("| %s | %d | %s |" % (b, i.file_size, lic))
    elif n.endswith(".py"): mods.append(n)
rec = so["recorded"]; by = {}
for k, v in rec.items():
    m = re.search(r"reads (\S+?),", v); by.setdefault(m.group(1) if m else "(other)", []).append(k)
nrun = len(json.load(open(os.path.join(H, "page_data_v%s.json" % sorted(f for f in os.listdir(H) if f.startswith("page_data_v"))[-1][11:-5])))["nodes"]) if False else None
out = ["# Chapter %s page assets - the wheel (v1.2.0)" % NN, "",
       "Adds to ASSETS_PROVENANCE_v1_0_0.md and v1_1_0.md (the story pictures: unchanged, licences there) the one new asset of the chapter %s page." % NN, "",
       "## %s" % wf, "",
       "- sha256 `%s`, %d bytes; written by `08-tooling/ch%s-page/pywheels_make_v1_0_0.py` (reproducible: zip dates fixed)." % (hashlib.sha256(open(wp, "rb").read()).hexdigest(), os.path.getsize(wp), NN),
       "- Holds %s (copied byte for byte from 08-tooling) and, in `ch%s-evidence`, %d saved files copied byte for byte. The files are those the worked examples really open (found by running every example once with open() logged, not guessed from the text) AND whose terms clearly allow redistribution." % (", ".join("`%s`" % m for m in mods), NN, len(rows)),
       "- %d of the chapter's %d worked examples run in the browser over them; %d are shown as 'Recorded, not run on this page' because they read a file that is NOT in the wheel (below)." % (len(so.get("run", [])) or int(re.search(r"(\d+) of the (\d+)", so["notice"]).group(1)), int(re.search(r"(\d+) of the (\d+)", so["notice"]).group(2)), len(rec)), "",
       "| File shipped | Bytes | Licence status |", "|---|---|---|"] + sorted(rows) + ["", "## Left out of the wheel (terms of redistribution not clear), and the examples that are recorded instead", ""]
for f, ks in sorted(by.items()): out.append("- `%s`: %d example%s (%s)." % (f, len(ks), "" if len(ks) == 1 else "s", ", ".join(sorted(ks))))
out += ["", "- Note: the recorded examples are the ones counted by the page's standin record (`08-tooling/ch%s-page/standin_v1_0_0.json`). Left out because their terms of redistribution are not clear to this author: mempool.space data, papers (Danezis and Goldberg 2009, Decker and Wattenhofer 2015), forum posts (bitcointalk), web pages (Lightning Engineering), the lnd release manifest, the BIP 341 and BOLT 4 test-vector files (no licence statement in the file itself), the README files of other implementations, any BIP whose header has no License line, and any code listing of the book (`book_code_*`). The wheel also carries the chapter's two helper modules (`sen0401_ch14_crypto_v1_0_0.py`, `sen0401_ch10_p2p_v1_0_0.py`), copied byte for byte from 08-tooling." % NN]
open(os.path.join(A, "ASSETS_PROVENANCE_v1_2_0.md"), "w").write("\n".join(out) + "\n"); print("rows", len(rows), "withheld files", len(by))
