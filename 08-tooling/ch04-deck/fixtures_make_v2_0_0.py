"""Makes the stale fixture that deck_check_v2_0_0.py must refuse, so that the gate has its own proof it can fail: the
compressed public key printed on the finished deck is edited by one character, and nothing else is touched.
Usage: fixtures_make_v2_0_0.py <deck.pptx> <out-dir>"""
__version__ = "2.0.0"
import os, sys, zipfile

GOOD = b"03f028892bad7ed57d2fb57bf33081d5cfcf6f9ed3d3d7f159c2e2fff579dc341a"
BAD = b"03f028892bad7ed57d2fb57bf33081d5cfcf6f9ed3d3d7f159c2e2fff579dc3410"

deck, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
zin = zipfile.ZipFile(deck)
zout = zipfile.ZipFile(os.path.join(out, "fixture_stale_expr_v2_0_0.pptx"), "w", zipfile.ZIP_DEFLATED)
n = 0
for it in zin.infolist():
    d = zin.read(it.filename)
    if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml") and GOOD in d:
        d = d.replace(GOOD, BAD)
        n += 1
    zout.writestr(it, d)
zout.close()
assert n >= 1, "the compressed public key was not found on any slide"
print("fixture written from", n, "slide(s)")
