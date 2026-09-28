#!/usr/bin/env python3
"""Chapter 4: read the public sources the chapter's checks rest on and save the parts they use, next to this script:
  segwit_addr_sipa_v1_0_0.py      - the bech32/bech32m reference code the book runs (sipa/bech32, MIT licence, header kept)
  bip350_vectors_v1_0_0.json      - the valid and invalid segwit address test vectors of BIP350 and the bech32m strings
  bip_status_v1_0_0.txt           - the Status lines of BIP173 and BIP350 as the BIPs repository gives them
  sec2_table2_v1_0_0.txt          - the rows for secp256k1 and secp256r1 of Table 2 of SEC 2 (Certicom Research, 2010)
  hashrate_v1_0_0.json            - the network's hash rate as mempool.space reports it (a third party's estimate)
  did_core_abstract_v1_0_0.txt    - the title, date and abstract of W3C's Decentralized Identifiers (DIDs) v1.0
Usage: sen0401_ch04_sources_v1_0_0.py   (needs outbound HTTPS and pdftotext)"""
__version__ = "1.0.0"
import html, json, os, re, subprocess, sys, tempfile, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
def get(url, binary=False):
    for a in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "sen0401-course-research"}), timeout=60) as r:
                d = r.read(); return d if binary else d.decode("utf-8", "replace")
        except Exception: time.sleep(2 + 2 * a)
    raise SystemExit("failed: " + url)
w = lambda name, text: open(os.path.join(HERE, name), "w").write(text)
w("segwit_addr_sipa_v1_0_0.py", get("https://raw.githubusercontent.com/sipa/bech32/master/ref/python/segwit_addr.py"))
b350 = get("https://raw.githubusercontent.com/bitcoin/bips/master/bip-0350.mediawiki"); b173 = get("https://raw.githubusercontent.com/bitcoin/bips/master/bip-0173.mediawiki")
tt = lambda s: re.findall(r"<tt>(.*?)</tt>", s)
sec = lambda name: b350.split(name)[1]
valid_m = tt(b350.split("The following strings are valid Bech32m:")[1].split("No string can be")[0])
va = b350.split("The following list gives valid segwit addresses")[1].split("The following list gives invalid segwit addresses")[0]
inv = b350.split("The following list gives invalid segwit addresses")[1].split("==Appendix")[0]
valid_seg = [(m.group(1), m.group(2)) for m in re.finditer(r"<tt>([^<]+)</tt>: <tt>([0-9a-f]+)</tt>", va)]
invalid_seg = [(m.group(1), m.group(2).strip()) for m in re.finditer(r"<tt>([^<]+)</tt>: ([^\n]+)", inv)]
json.dump({"source": "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0350.mediawiki", "read": time.strftime("%Y-%m-%d", time.gmtime()), "valid_bech32m": valid_m, "valid_segwit": valid_seg, "invalid_segwit": invalid_seg}, open(os.path.join(HERE, "bip350_vectors_v1_0_0.json"), "w"), indent=1)
st = lambda s, n: [l.strip() for l in s.splitlines() if re.match(r"\s*(BIP|Title|Status):", l)][:3]
w("bip_status_v1_0_0.txt", "\n".join(st(b173, 173) + st(b350, 350)) + "\n")
with tempfile.TemporaryDirectory() as t:
    open(t + "/s.pdf", "wb").write(get("https://www.secg.org/sec2-v2.pdf", True)); subprocess.run(["pdftotext", "-layout", "-f", "1", "-l", "60", t + "/s.pdf", t + "/s.txt"], check=True)
    lines = open(t + "/s.txt").read().splitlines()
hdr = next(l for l in lines if "ANSI X9.62" in l and "NIST" in l); rows = [l for l in lines if re.match(r"\s*secp256[kr]1\s+2\.4\.[12]\s+[a-z-]", l)]
w("sec2_table2_v1_0_0.txt", "Standards for Efficient Cryptography 2 (SEC 2), Certicom Research, version 2.0, 27 January 2010, Table 2:\n" + hdr.strip() + "\n" + "\n".join(r.strip() for r in rows) + "\n")
hr = json.loads(get("https://mempool.space/api/v1/mining/hashrate/3m"))
json.dump({"source": "https://mempool.space/api/v1/mining/hashrate/3m", "read": time.strftime("%Y-%m-%d", time.gmtime()), "currentHashrate": hr["currentHashrate"]}, open(os.path.join(HERE, "hashrate_v1_0_0.json"), "w"), indent=1)
did = get("https://www.w3.org/TR/did-core/"); ab = re.search(r'id="abstract"[^>]*>(.*?)</section>', did, re.S)
w("did_core_abstract_v1_0_0.txt", re.search(r"<title>(.*?)</title>", did, re.S).group(1).strip() + "\n" + re.search(r'dt-published" datetime="([^"]+)"', did).group(1) + "\n" + re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", ab.group(1)))).strip() + "\n")
print("sources saved:", len(valid_m), "bech32m strings,", len(valid_seg), "valid and", len(invalid_seg), "invalid segwit vectors")
