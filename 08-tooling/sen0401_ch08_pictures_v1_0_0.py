#!/usr/bin/env python3
"""sen0401_ch08_pictures v1.0.0 - fetches the story pictures of chapter 8 from Wikimedia Commons with their licence data (the Commons API's extmetadata), downloads the file
(at most 1200 px wide through Commons' thumbnail service when larger), and writes 03-materials/ch08/assets/<name> and ch08-evidence/pictures_record_v1_0_0.json
(file, source page, author, credit, licence short name and URL, date, sha256). The Commons file page itself is saved as ch08-evidence/commons_<name>.txt so that the licence line can be re-read.
Usage: sen0401_ch08_pictures_v1_0_0.py   (waits and retries when Wikimedia answers 'too many requests')"""
__version__ = "1.0.0"
import hashlib, html, json, os, re, subprocess, sys, time, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "03-materials", "ch08", "assets")
EV = os.path.join(HERE, "ch08-evidence")
UA = "SEN0401-course-research/1.0 (Istanbul Kultur University teaching materials; github.com/altunelyusuf)"
FILES = [("schnorr", "Claus-Peter Schnorr.jpg"), ("shamir", "Adi Shamir Royal Society.jpg"), ("bitcoinqt", "Screenshot of Bitcoin-qt-0.5.2.png")]
if len(sys.argv) > 1:
    FILES = [tuple(a.split("=", 1)) for a in sys.argv[1:]]
os.makedirs(ASSETS, exist_ok=True)


def curl(args):
    for _ in range(20):
        r = subprocess.run(["curl", "-sS", "-L", "-m", "90", "-A", UA] + args, capture_output=True)
        head = r.stdout[:800].lower()
        if b"too many requests" in head or b"wikimedia error" in head or b"rate limit" in head:
            time.sleep(30); continue
        return r.stdout
    raise SystemExit("rate limited")


rec_path = os.path.join(EV, "pictures_record_v1_0_0.json")
rec = json.load(open(rec_path)) if os.path.exists(rec_path) else {}
for key, title in FILES:
    out = curl(["-G", "https://commons.wikimedia.org/w/api.php", "--data-urlencode", "action=query", "--data-urlencode", "titles=File:" + title, "--data-urlencode",
                "prop=imageinfo", "--data-urlencode", "iiprop=url|extmetadata|size|sha1|timestamp|mime", "--data-urlencode", "iiurlwidth=1200", "--data-urlencode", "format=json"])
    p = list(json.loads(out)["query"]["pages"].values())[0]; ii = p["imageinfo"][0]; m = ii["extmetadata"]
    g = lambda k: html.unescape(re.sub(r"<[^>]+>", "", m.get(k, {}).get("value", ""))).strip()
    ext = os.path.splitext(title)[1].lower()
    name = "ch08_%s%s" % (key, ".jpg" if ext in (".jpg", ".jpeg") else ".png")
    url = ii.get("thumburl") or ii["url"]
    data = curl([url])
    if len(data) < 2000 or data[:200].lstrip().startswith(b"<"):
        raise SystemExit("download failed for " + title)
    open(os.path.join(ASSETS, name), "wb").write(data)
    page = curl(["https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_"))])
    txt = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", page.decode("utf-8", "replace")); txt = html.unescape(re.sub(r"<[^>]+>", " ", txt)); txt = re.sub(r"\s+", " ", txt)
    open(os.path.join(EV, "commons_%s.txt" % key), "w", encoding="utf-8").write(txt)
    rec[key] = {"file": name, "title": "File:" + title, "page": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(title.replace(" ", "_")), "download": url, "mime": ii.get("mime"),
                "width": ii.get("thumbwidth") or ii["width"], "author": g("Artist"), "credit": g("Credit"), "license": g("LicenseShortName"), "license_url": g("LicenseUrl"),
                "date": g("DateTimeOriginal") or g("DateTime"), "description": g("ImageDescription")[:300], "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                "commons_page_saved_as": "commons_%s.txt" % key, "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    print(key, name, len(data), rec[key]["license"], "|", rec[key]["author"][:60])
    json.dump(rec, open(rec_path, "w"), indent=1, sort_keys=True)
    time.sleep(6)
json.dump(rec, open(rec_path, "w"), indent=1, sort_keys=True)
