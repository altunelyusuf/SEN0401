#!/usr/bin/env python3
"""provenance_make v1_0_2 (SEN0401 chapter page). Writes 03-materials/chNN/assets/ASSETS_PROVENANCE_v1_5_0.md for the wheel of pywheels_v1_0_2.json: sha256, the shipped files with a licence status
by file-name class, and the files left out with the examples that are recorded because of them (from standin_v1_0_2.json). Usage: provenance_make_v1_0_2.py NN"""
__version__ = "1.0.2"
import hashlib, json, os, re, sys, zipfile
NN = sys.argv[1]; H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch%s" % NN, "assets")
pw = json.load(open(os.path.join(H, "pywheels_v1_0_2.json"))); so = json.load(open(os.path.join(H, "standin_v1_0_2.json")))
wf = pw["wheels"][0]["file"]; wp = os.path.join(A, wf); z = zipfile.ZipFile(wp)
LIC = [("bip-", "the open licence each BIP states (BSD-2-Clause, BSD-3-Clause, CC0 or public domain)"), ("bitcoind_help_", "MIT (Bitcoin Core)"), ("core_", "MIT (Bitcoin Core)"),
       ("book_", "CC BY-SA 4.0 (Mastering Bitcoin, 3rd edition)"), ("optech_", "CC BY 4.0 (Bitcoin Optech)"), ("nakamoto_2008_bitcoin", "MIT, as published on bitcoin.org"),
       ("regtest_run_", "this course's own run record"), ("regtest2_run_", "this course's own run record"), ("bolt03_", "CC BY 4.0 (BOLT 3; the file itself states it)"), ("mainnet_fee_census_v2_0_0", "CC BY 4.0 (the course's own census: facts of the block chain collected from mempool.space and blockstream.info and cross-checked, statistics computed by sen0401_ch09_census_collect_v1_0_0.py; licence statement in the file)"), ("bitcoinwiki_", "CC BY 3.0 (Bitcoin Wiki)"), ("wikipedia_", "CC BY-SA (Wikipedia)")]
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
out = ["# Chapter %s page assets - the wheel (v1.5.0)" % NN, "",
       "Adds to ASSETS_PROVENANCE_v1_0_0.md, v1_1_0.md and v1_2_0.md (the story pictures, unchanged, licences there) the new wheel of the chapter %s page, which replaces wheel 1.0.1 of v1_3_0 and v1_4_0 (the mempool.space census, which states no licence, is no longer shipped; the page built on wheel 1.0.1 is superseded) and carries only texts whose redistribution is clear." % NN, "",
       "## %s" % wf, "",
       "- sha256 `%s`, %d bytes; written by `08-tooling/ch%s-page/pywheels_make_v1_0_2.py` (reproducible: zip dates fixed)." % (hashlib.sha256(open(wp, "rb").read()).hexdigest(), os.path.getsize(wp), NN),
       "- Holds %s (copied byte for byte from 08-tooling) and, in `ch%s-evidence`, %d saved files copied byte for byte. The files are those the worked examples really open (found by running every example once with open() logged, not guessed from the text) AND whose terms clearly allow redistribution." % (", ".join("`%s`" % m for m in mods), NN, len(rows)),
       "- %d of the chapter's %d worked examples run in the browser over them; %d are shown as 'Recorded, not run on this page' because they read a file that is NOT in the wheel (below)." % (len(so.get("run", [])) or int(re.search(r"(\d+) of the (\d+)", so["notice"]).group(1)), int(re.search(r"(\d+) of the (\d+)", so["notice"]).group(2)), len(rec)), "",
       "| File shipped | Bytes | Licence status |", "|---|---|---|"] + sorted(rows) + ["", "## Left out of the wheel (terms of redistribution not clear), and the examples that are recorded instead", ""]
for f, ks in sorted(by.items()): out.append("- `%s`: %d example%s (%s)." % (f, len(ks), "" if len(ks) == 1 else "s", ", ".join(sorted(ks))))
out += ["", "- Note: the recorded examples are the ones counted by the page's standin record (`08-tooling/ch%s-page/standin_v1_0_2.json`). Left out for unclear terms: the full text of two academic papers (Carlsten et al., ACM CCS 2016; Moeser and Boehme, 2015) and of one mailing-list post (Corallo, 2018), which the wheel of v1_2_0 carried and this wheel does not; and the two saved market files fetched from the public mempool.space interface (`mempool_blocks_fees_1y.json`, `mempool_fees_recommended.json`; no licence stated by the service), which this wheel no longer carries either, as in the chapter 11 page. The mainnet census of the earlier wheel (`mainnet_fee_census_v1_0_0.json`, two blocks fetched from mempool.space, no licence stated) is no longer carried: this wheel carries the course's own census `mainnet_fee_census_v2_0_0.json` (20 blocks, CC BY 4.0, collected by `08-tooling/sen0401_ch09_census_collect_v1_0_0.py`, both services named and cross-checked inside the file)." % NN]
open(os.path.join(A, "ASSETS_PROVENANCE_v1_5_0.md"), "w").write("\n".join(out) + "\n"); print("rows", len(rows), "withheld files", len(by))
