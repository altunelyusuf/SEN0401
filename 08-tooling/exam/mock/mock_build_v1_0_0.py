#!/usr/bin/env python3
"""Build self-contained mock HTML files from a merged bank (v1.0.0). Code only; the output goes to the private CME mock folder.
Usage: mock_build_v1_0_0.py BANK.json OUTDIR [--sample]
Writes mock_ch_all_master.html and mock_ch_all_mock{1..8}.html (SAMPLE_ prefix with --sample)."""
import json, os, sys, hashlib
H = os.path.dirname(os.path.abspath(__file__))

def read(n):
    return open(os.path.join(H, n), encoding="utf-8").read()

def build(bank, preset):
    t = read("mock_shell_v1_0_0.html")
    bj = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = "window.MOCK_PRESET=%s;" % json.dumps(preset)
    for ph, val in (("/*@@BANK@@*/", bj), ("/*@@PRESET@@*/", pre), ("/*@@SCORING@@*/", read("mock_scoring_v1_0_0.js")),
                    ("/*@@DERIVE@@*/", read("mock_derive_v1_0_0.js")), ("/*@@UI@@*/", read("mock_ui_v1_0_0.js"))):
        assert t.count(ph) == 1, ph
        t = t.replace(ph, val)
    return t

def main():
    bankf, out = sys.argv[1], sys.argv[2]
    sample = "--sample" in sys.argv
    bank = json.load(open(bankf))
    if bank.get("synthetic") and not sample:
        raise SystemExit("refusing: synthetic bank without --sample")
    if sample and not bank.get("synthetic"):
        raise SystemExit("refusing: --sample on a non-synthetic bank")
    os.makedirs(out, exist_ok=True)
    pre = "SAMPLE_" if sample else ""
    files = [(pre + "mock_ch_all_master.html", {"k": 1})] + [(pre + "mock_ch_all_mock%d.html" % k, {"k": k}) for k in range(1, 9)]
    for name, preset in files:
        p = os.path.join(out, name)
        open(p, "w", encoding="utf-8").write(build(bank, preset))
        print(name, os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest())
main()
