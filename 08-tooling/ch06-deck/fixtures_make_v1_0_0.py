"""Makes the stale fixture that deck_check_v1_0_0.py must refuse, so that the gate has its own proof it can fail: the first
sixteen hexadecimal characters of Alice's transaction identifier printed on the finished deck are edited by one character,
and nothing else is touched. Chapter 6 version of chapter 5's fixtures_make_v1_0_0.py: the same mechanism, this chapter's
printed value (the identifier the segregated-witness slide recomputes from the 125 legacy bytes).
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile

GOOD = b"(&apos;466200308696215b&apos;, &apos;466200308696215b&apos;)"   # the renderer writes quotes as XML entities
BAD = b"(&apos;466200308696215b&apos;, &apos;466200308696215c&apos;)"

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
assert n >= 1, "the recomputed identifier was not found on any slide"
print("fixture written from", n, "slide(s)")
