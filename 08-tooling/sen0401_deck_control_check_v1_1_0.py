#!/usr/bin/env python3
"""sen0401_deck_control_check v1.1.0 (python-pptx 1.0.2) - the control's own exit-coded checks of a rebuilt deck. A NEW tool; it edits nothing.
Usage: sen0401_deck_control_check_v1_0_0.py manifest:NN | nochange:NN:SHA[,SHA...]
  manifest:NN  the newest chapter-code manifest of chapter NN (03-materials/chNN/page): order numbers run 1..n, every name is non-empty and unique, the 'deck' field names an existing deck,
               the slide numbers in manifest order equal the numbers of the deck's code slides (a slide holding a paragraph that starts with '>>> ') in slide order, the library and data
               files exist, with the stated SHA-256 where the manifest states one (v1.1.0: chapter 6 manifests state none; the deck path may be a bare file name). Exit 0 only when all hold.
  nochange     every file of the listed commits has git status A (added); a modified or deleted committed file fails. Exit 0 only when all are added."""
__version__ = "1.1.0"
import glob, hashlib, json, os, re, subprocess, sys
R = os.environ.get("SEN0401_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def manifest(nn):
    vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
    mp = sorted(glob.glob(os.path.join(R, "03-materials", "ch%s" % nn, "page", "chapter_code_ch%s_v*.json" % nn)), key=vk)[-1]; m = json.load(open(mp)); ex = m["examples"]; bad = []
    from pptx import Presentation
    dk = os.path.join(R, m["deck"])
    if not os.path.exists(dk): dk = os.path.join(R, "03-materials", "ch%s" % nn, m["deck"])
    assert os.path.exists(dk), "deck missing"
    code = [i + 1 for i, s in enumerate(Presentation(dk).slides) if any(p.text.startswith(">>> ") for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs)]
    if [e["order"] for e in ex] != list(range(1, len(ex) + 1)): bad.append("order numbers are not 1..n")
    names = [e["name"].strip() for e in ex]
    if not all(names) or len(set(names)) != len(names): bad.append("names empty or not unique")
    if [e["slide"] for e in ex] != code: bad.append("manifest slides %s differ from code slides %s" % ([e["slide"] for e in ex], code))
    for f in [m["library"]] + m["library"].get("data_files", []):
        p = os.path.join(R, f["file"])
        if not os.path.exists(p): p = os.path.join(R, "08-tooling", f["file"])
        if not os.path.exists(p) or ("sha256" in f and hashlib.sha256(open(p, "rb").read()).hexdigest() != f["sha256"]): bad.append("library or data file missing, or hash mismatch " + f["file"])
    print("manifest %s | %d examples | %d code slides | deck %s | %s" % (os.path.basename(mp), len(ex), len(code), m["deck"], "FAIL " + "; ".join(bad) if bad else "PASS order equals code-slide order, names unique, library files exist, hashes match where stated"))
    return not bad
def nochange(shas):
    bad = []
    for s in shas:
        out = subprocess.run(["git", "show", "--name-status", "--format=", s], cwd=R, capture_output=True, text=True).stdout.split("\n")
        for l in out:
            if l.strip() and not l.startswith("A\t"): bad.append("%s %s" % (s, l))
    print("nochange commits %s | %s" % (",".join(shas), "FAIL " + "; ".join(bad) if bad else "PASS every file of the commits was added, none modified or deleted"))
    return not bad
if __name__ == "__main__":
    a = sys.argv[1].split(":")
    ok = manifest(a[1]) if a[0] == "manifest" else nochange(a[2].split(","))
    sys.exit(0 if ok else 1)
