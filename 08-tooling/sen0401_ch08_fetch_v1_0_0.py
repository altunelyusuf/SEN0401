#!/usr/bin/env python3
"""sen0401_ch08_fetch v1.0.0 - fetches every URL of sen0401_ch08_sources_v1_0_0.py through the study's proxy, saves the readable copy in ch08-evidence, checks that every passage the
chapter relies on occurs in the saved copy, and writes ch08-evidence/sources_record_v1_0_0.json (HTTP status, bytes, SHA-256 of what was received and of what was saved, passages found).
Usage: sen0401_ch08_fetch_v1_0_0.py [--only P01,P02] [--keep-existing]. Exits 1 when a URL did not answer 200 or a passage is missing."""
__version__ = "1.0.0"
import hashlib, html, json, os, re, subprocess, sys, tempfile, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch08_sources_v1_0_0 as S

EV = os.path.join(HERE, "ch08-evidence")
REC = os.path.join(EV, "sources_record_v1_0_0.json")
norm = lambda s: " ".join(s.split())


def html_to_text(b):
    t = b.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|pre|section|article)>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t); t = html.unescape(t)
    t = re.sub(r"[ \t\r\f\v\xa0]+", " ", t); t = re.sub(r"\n\s*\n+", "\n", t)
    return t.encode("utf-8")


def fetch(url):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        name = f.name
    r = subprocess.run(["curl", "-sS", "-L", "-m", "120", "-o", name, "-w", "%{http_code}", url], capture_output=True, text=True)
    data = open(name, "rb").read(); os.unlink(name)
    return r.stdout.strip(), data


def main():
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    rec = json.load(open(REC)) if os.path.exists(REC) else {}
    rec.setdefault("_fetched", {})
    bad = 0
    for s in S.SRC:
        if only and s["id"] not in only:
            continue
        code, raw = fetch(s["url"])
        if code != "200" or len(raw) < 100:
            print("FAIL %s %s %s bytes=%d" % (s["id"], code, s["url"], len(raw))); bad += 1; continue
        if s["kind"] == "html":
            saved = html_to_text(raw)
        elif s["kind"] == "pdf":
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                f.write(raw); pn = f.name
            saved = subprocess.run(["pdftotext", "-layout", pn, "-"], capture_output=True).stdout; os.unlink(pn)
        else:
            saved = raw
        open(os.path.join(EV, s["save"]), "wb").write(saved)
        text = saved.decode("utf-8", "replace"); nt = norm(text)
        found = {p: (norm(p) in nt) for p in s["passages"]}
        miss = [p for p, ok in found.items() if not ok]
        rec[s["id"]] = {"url": s["url"], "http": int(code), "received_bytes": len(raw), "received_sha256": hashlib.sha256(raw).hexdigest(), "saved_as": s["save"],
                        "saved_bytes": len(saved), "saved_sha256": hashlib.sha256(saved).hexdigest(), "passages": len(s["passages"]), "passages_found": len(s["passages"]) - len(miss),
                        "fetched": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        print("%s %s %-48s %8d B  passages %d/%d%s" % ("OK  " if not miss else "MISS", s["id"], s["save"], len(raw), len(s["passages"]) - len(miss), len(s["passages"]), "" if not miss else "  missing: " + repr(miss)))
        bad += bool(miss)
    json.dump(rec, open(REC, "w"), indent=1, sort_keys=True)
    print("sources:", len([k for k in rec if k.startswith("P")]), "bad:", bad)
    sys.exit(1 if bad else 0)


main()
