#!/usr/bin/env python3
"""Fetches every source of sen0401_ch10_sources_v1_0_0.py into ch10-evidence (curl through the sandbox proxy), converts PDFs to text (pdftotext) and
HTML to text, and writes ch10-evidence/sources_index_v1_0_0.json: per source the URL, HTTP status, bytes, sha256 and the day fetched. The command line help of the
Bitcoin Core 31.1 binary (source P50) is produced by running the binary, not downloaded; its record carries the sha256 of the binary as well.
Usage: sen0401_ch10_fetch_v1_0_0.py [--only P01,P02]"""
__version__ = "1.0.0"
import hashlib, html, json, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_sources_v1_0_0 as SR
EV = os.path.join(HERE, "ch10-evidence"); os.makedirs(EV, exist_ok=True)
IDX = os.path.join(EV, "sources_index_v1_0_0.json")
idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
BIN = os.environ.get("BITCOIN_BIN", "/home/claude/core31/bitcoin-31.1/bin")


def get(url, path, retries=6):
    code = "0"
    for k in range(retries):
        r = subprocess.run(["curl", "-sS", "-L", "-m", "120", "-A", "sen0401-research/1.0 (altunel.yusuf@gmail.com)", "-o", path, "-w", "%{http_code}", url], capture_output=True, text=True)
        code = r.stdout.strip()
        if r.returncode == 0 and code == "200":
            return 200
        time.sleep(4 * (k + 1))
    return int(code) if code.isdigit() else 0


def totext(path):
    if path.endswith(".pdf"):
        subprocess.run(["pdftotext", "-layout", path, path[:-4] + ".txt"], check=True)
    elif path.endswith(".html"):
        t = open(path, errors="replace").read()
        t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", t)
        t = re.sub(r"(?s)<[^>]+>", " ", t)
        open(path[:-5] + ".txt", "w").write(html.unescape(t))


for sid, ay, label, url, fn, role in SR.S:
    if only and sid not in only:
        continue
    p = os.path.join(EV, fn)
    if url.startswith("local:"):
        out = subprocess.run([BIN + "/bitcoind", "-help"], capture_output=True, text=True).stdout + "\n" + subprocess.run([BIN + "/bitcoind", "-help-debug"], capture_output=True, text=True).stdout
        open(p, "w").write(out)
        code = 200
        extra = {"binary_sha256": hashlib.sha256(open(BIN + "/bitcoind", "rb").read()).hexdigest()}
    else:
        code = get(url, p)
        extra = {}
    if code != 200:
        print("FAILED", sid, url, code); idx[sid] = {"url": url, "http": code}; continue
    totext(p)
    b = open(p, "rb").read()
    idx[sid] = dict({"url": url, "file": fn, "http": 200, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "fetched": time.strftime("%Y-%m-%d", time.gmtime())}, **extra)
    print("ok", sid, fn, len(b), flush=True)
    time.sleep(1.5 if "wikipedia" in url else 0.3)
json.dump(idx, open(IDX, "w"), indent=1, sort_keys=True)
