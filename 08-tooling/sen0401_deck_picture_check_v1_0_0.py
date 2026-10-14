#!/usr/bin/env python3
"""sen0401_deck_picture_check v1.0.0 - every picture a slide shows is a file of the chapter, pixel for pixel (new for SEN0401; the pixel comparison is SEN0414's program_check idea for its
program-made pictures, applied here to the photographs and book figures of 03-materials/chNN/assets and to pictures made for the deck under chNN-deck/images). From the finished .pptx:
  1. every picture part (ppt/media) must equal, byte for byte or pixel for pixel (same size and mode, identical pixels - a re-encoding passes), some file of those two folders;
  2. every picture the plan names (item 'img', path) must exist, and the deck must hold as many picture parts as the plan has img items (a picture lost or swapped is a mismatch);
  3. a picture swapped for another asset of the chapter in the right place is caught by the plan: the picture on slide k must equal the plan's file for slide k.
Usage: sen0401_deck_picture_check_v1_0_0.py NN [deck.pptx]       Environment: SEN0401_ROOT (needs Pillow).  Exit 0 when nothing is refused."""
__version__ = "1.0.0"
import glob, io, json, os, re, sys, zipfile
from PIL import Image

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
newest = lambda pat: sorted(glob.glob(pat), key=vkey)[-1]


def pix(b):
    im = Image.open(io.BytesIO(b)); im.load(); return im.size, im.mode, im.tobytes()


def main(a):
    n = a[0]; chd = os.path.join(TOOL, "ch%s-deck" % n)
    deck = [x for x in a[1:] if x.endswith(".pptx")]; deck = deck[0] if deck else newest(os.path.join(chd, "sen0401_ch%s_deck_v*.pptx" % n))
    plan = json.load(open(newest(os.path.join(chd, "deck_plan_v*.json"))))
    files = {}
    for d in (os.path.join(ROOT, "03-materials", "ch%s" % n, "assets"), os.path.join(chd, "images")):
        for f in glob.glob(os.path.join(d, "*")):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")): files[f] = open(f, "rb").read()
    z = zipfile.ZipFile(deck); bad = []
    parts = sorted((p for p in z.namelist() if p.startswith("ppt/media/") and not p.endswith("/")), key=lambda s: [int(x) for x in re.findall(r"\d+", s)] or [0])
    want = [(i, it) for i, s in enumerate(plan["slides"], 1) for it in s["items"] if it.get("t") == "img"]
    ctrl = 0; raw = 0; px = 0
    for p in parts:
        b = z.read(p)
        if any(b == v for v in files.values()): raw += 1; continue
        try: k = pix(b)
        except Exception: bad.append("%s cannot be decoded" % p); continue
        if any(pix(v) == k for v in files.values()): px += 1
        else: bad.append("%s equals no file of the chapter's assets or deck images, byte for byte or pixel for pixel" % p)
    if len(parts) != len(want): bad.append("the deck holds %d picture part(s), the plan has %d img item(s)" % (len(parts), len(want)))
    for i, it in want:
        f = os.path.normpath(os.path.join(chd, it["path"]))
        if not os.path.exists(f): bad.append("slide %d: the plan names %s, which does not exist" % (i, it["path"]))
    # the picture on slide k must be the plan's file for slide k (rels name the media part)
    for i, s in enumerate(plan["slides"], 1):
        its = [it for it in s["items"] if it.get("t") == "img"]
        rel = "ppt/slides/_rels/slide%d.xml.rels" % i
        if not its or rel not in z.namelist(): continue
        tg = re.findall(r'Target="\.\./media/([^"]+)"', z.read(rel).decode())
        got = sorted(pix(z.read("ppt/media/" + t)) for t in tg if ("ppt/media/" + t) in z.namelist())
        exp = []
        for it in its:
            f = os.path.normpath(os.path.join(chd, it["path"]))
            if os.path.exists(f): exp.append(pix(open(f, "rb").read()))
        if len(got) == len(exp) and sorted(exp) != got: bad.append("slide %d: its picture is not the file the plan names" % i)
    print("sen0401_deck_picture_check %s (chapter %s): %d picture part(s): %d byte-identical, %d pixel-identical; plan has %d img item(s); %d refusal(s)" % (__version__, n, len(parts), raw, px, len(want), len(bad)))
    for b in bad: print("  REFUSED", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
