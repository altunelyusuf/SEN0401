#!/usr/bin/env python3
"""SEN0401 chapter 11: runs every code frame of the chapter code manifest under the current Python, in slide order, and compares each shown result with the slide's expected value (Definition of Done criterion 'every code example runs as the slide shows')."""
__version__ = "1.0.0"
import json, os, sys, glob, re, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
mf = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch11", "page", "chapter_code_ch11_v*.json")), key=lambda x: [int(v) for v in re.findall(r"_v(\d+)_(\d+)_(\d+)\.json$", x)[0]])[-1]
d = json.load(open(mf, encoding="utf-8"))
ns = {}
exec(d["setup"]["code"], ns)
bad, n_ex, n_show = [], 0, 0
for ex in d["examples"]:
    n_ex += 1
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(ex["code"], ns)
    except Exception as e:
        bad.append((ex["id"], "raised %s: %s" % (type(e).__name__, e))); print("FAIL", ex["id"], ex["name"], type(e).__name__, e); continue
    for sh in ex.get("show", []):
        n_show += 1
        try:
            got = eval(sh["expression"], ns)
        except Exception as e:
            bad.append((ex["id"], sh["expression"], "raised %s" % e)); print("FAIL", ex["id"], sh["expression"], e); continue
        ok = str(got) == str(sh["expected"]) or repr(got) == str(sh["expected"])
        print("%s %s %s = %s (slide shows %s)" % ("ok  " if ok else "FAIL", ex["id"], sh["expression"], str(got)[:60], str(sh["expected"])[:60]))
        if not ok: bad.append((ex["id"], sh["expression"], str(got)[:80], str(sh["expected"])[:80]))
print("manifest", os.path.basename(mf), "deck", d["deck_version"], "examples", n_ex, "shown results", n_show, "failures", len(bad))
print("RESULT:", "PASS" if not bad else "FAIL")
sys.exit(1 if bad else 0)
