"""Makes the stale fixture that deck_check_v2_0_0.py must refuse, so that the gate has its own proof it can fail: the
compressed public key printed on the finished deck is edited by one character, and nothing else is touched.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile

GOOD = b"e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35"
BAD = b"e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b30"

deck, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
zin = zipfile.ZipFile(deck)
zout = zipfile.ZipFile(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "w", zipfile.ZIP_DEFLATED)
n = 0
for it in zin.infolist():
    d = zin.read(it.filename)
    if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml") and GOOD in d:
        d = d.replace(GOOD, BAD)
        n += 1
    zout.writestr(it, d)
zout.close()
assert n >= 1, "the master private key was not found on any slide"
print("fixture written from", n, "slide(s)")
