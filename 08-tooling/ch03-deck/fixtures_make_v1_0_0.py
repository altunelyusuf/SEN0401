"""Makes the stale fixture the deck check must refuse, from the deck itself: the difficulty result edited.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "w", zipfile.ZIP_DEFLATED); n = 0
for it in zin.infolist():
    d = zin.read(it.filename)
    if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml") and b"157416.4018436489" in d: d = d.replace(b"157416.4018436489", b"157416.4018436480"); n += 1
    zout.writestr(it, d)
zout.close(); assert n == 1, n
print("fixture written")
