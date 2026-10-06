#!/usr/bin/env python3
"""Ensures a logarithmic value axis on the native charts that declare one (BP: the chart object
must match the calculation it draws). pptxgenjs 3.12 does not emit <c:logBase>, so this step
rewrites the finished .pptx: every chart whose title contains "(log axis)" gets
<c:logBase val="10"/> as the first child of its value-axis <c:scaling>, which PowerPoint and
LibreOffice both honour. Run after the deck is rendered:  deck_chart_logaxis_v1_0_0.py <deck.pptx>
Refuses (exit 1) if it finds no chart titled "(log axis)", so a silent no-op cannot pass."""
__version__ = "1.0.0"
import re
import shutil
import sys
import zipfile

p = sys.argv[1]
tmp = p + ".tmp"
zin = zipfile.ZipFile(p)
fixed = 0
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        data = zin.read(it.filename)
        if re.match(r"ppt/charts/chart\d+\.xml$", it.filename):
            x = data.decode("utf-8")
            if "(log axis)" in x and "c:valAx" in x:
                before = x
                # value axis only: insert logBase as the first child of its <c:scaling>
                head, val = x.split("<c:valAx>", 1)
                val = val.replace("<c:scaling>", '<c:scaling><c:logBase val="10"/>', 1)
                x = head + "<c:valAx>" + val
                if x != before:
                    fixed += 1
                data = x.encode("utf-8")
        zout.writestr(it, data)
zin.close()
if not fixed:
    print("REFUSED: no '(log axis)' chart found - nothing was fixed", file=sys.stderr)
    sys.exit(1)
shutil.move(tmp, p)
print("log axis ensured on %d chart(s)" % fixed)
