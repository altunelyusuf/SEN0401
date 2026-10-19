#!/usr/bin/env python3
"""sen0401_lineage_licence_check v1_1_0 (over v1_0_0, which keeps its one id) - the checks the evidence bridge runs for the licence tasks of the chapter 9 page. They read the PHYSICAL page:
the newest chapter 9 page's embedded wheel (the page data 'py_wheels', hex) is opened and its file names listed.
  Licence/BOLT_Ch09     the newest provenance file names the BOLT file with exactly "CC BY 4.0" (the owner's ruling of 2026-10-19)
  Licence/Mempool_Ch09  the page embeds no mempool.space census of an earlier version (mainnet_fee_census_v1_0_0.json) and no saved mempool.space market file; it embeds the course's own census
                        (mainnet_fee_census_v2_0_0.json) whose own licence field says CC BY 4.0; the provenance row of that census says CC BY 4.0 as well
  Licence/Texts_Ch09    the page embeds none of the three third-party texts without a clear licence (the Carlsten et al. 2016 paper, the Moeser and Boehme 2015 paper, the Corallo 2018 mailing-list post)
Exit 0 = holds. Usage: sen0401_lineage_licence_check_v1_1_0.py Licence/<id>_Ch09"""
__version__ = "1.1.0"
import glob, io, json, os, re, sys, zipfile
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
prov = sorted(glob.glob(os.path.join(repo, "03-materials/ch09/assets/ASSETS_PROVENANCE_v*.md")), key=vk)[-1]
page = sorted(glob.glob(os.path.join(repo, "03-materials/ch09/page/sen0401_ch09_page_v*.html")), key=vk)[-1]
ptxt = open(prov, encoding="utf-8").read()


def rows(word):
    return [l for l in ptxt.splitlines() if l.startswith("|") and word in l.lower().split("|")[1]]


def wheel_files():
    s = open(page, encoding="utf-8").read()
    m = re.search(r'<script type="application/json" id="data">(.*?)</script>', s, re.S)
    d = json.loads(m.group(1)); out = {}
    for w in d["py_wheels"]:
        z = zipfile.ZipFile(io.BytesIO(bytes.fromhex(w["hex"])))
        for n in z.namelist():
            out[os.path.basename(n)] = z.read(n) if n.endswith("census_v2_0_0.json") else b""
    return out


which = sys.argv[1]; ok = False
if which == "Licence/BOLT_Ch09":
    r = rows("bolt"); ok = len(r) == 1 and r[0].split("|")[3].strip().startswith("CC BY 4.0"); print(os.path.basename(prov), r)
elif which == "Licence/Mempool_Ch09":
    f = wheel_files(); c = f.get("mainnet_fee_census_v2_0_0.json", b"")
    lic = json.loads(c).get("licence", "") if c else ""
    r = rows("census_v2")
    ok = ("mainnet_fee_census_v1_0_0.json" not in f and "mempool_fees_recommended.json" not in f and bool(c) and "CC BY 4.0" in lic and len(r) == 1 and "CC BY 4.0" in r[0].split("|")[3])
    print(os.path.basename(page), os.path.basename(prov), sorted(k for k in f if "census" in k or "mempool" in k), r)
elif which == "Licence/Texts_Ch09":
    f = wheel_files(); gone = ["carlsten_2016_instability.txt", "moeser_boehme_2015_fees.txt", "ml_corallo_2018-12_carveout.txt"]
    ok = bool(f) and not any(g in f for g in gone); print(os.path.basename(page), "embedded files:", len(f), "third-party texts present:", [g for g in gone if g in f])
sys.exit(0 if ok else 1)
