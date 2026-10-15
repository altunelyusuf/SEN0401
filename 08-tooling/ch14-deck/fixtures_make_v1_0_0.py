"""Makes the stale fixture that deck_check_v1_0_0.py must refuse, so that the gate has its own proof it can fail: the delay of the to_local script, 1000 blocks, printed on the commitment slide of the
finished deck, is edited by one digit (1001) and nothing else is touched. Chapter 14 version of chapter 13's fixtures_make_v1_0_0.py: the same mechanism, this chapter's printed value.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile

GOOD = b"<a:t>('OP_IF', '1000', 'OP_CHECKSEQUENCEVERIFY', 'OP_CHECKSIG', 'non-BIP68-final')</a:t>"
BAD = b"<a:t>('OP_IF', '1001', 'OP_CHECKSEQUENCEVERIFY', 'OP_CHECKSIG', 'non-BIP68-final')</a:t>"

deck, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
zin = zipfile.ZipFile(deck)
zout = zipfile.ZipFile(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "w", zipfile.ZIP_DEFLATED)
n = 0
for it in zin.infolist():
    d = zin.read(it.filename)
    if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml") and d.count(GOOD) == 1:
        d = d.replace(GOOD, BAD)
        n += 1
    zout.writestr(it, d)
zout.close()
assert n == 1, "the delay was not found on exactly one slide"
print("fixture written from", n, "slide(s)")
