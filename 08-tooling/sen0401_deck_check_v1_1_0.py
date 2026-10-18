#!/usr/bin/env python3
"""sen0401_deck_check v1.1.0 (over v1.0.0: the loose provenance test of a chart value compares numbers, not text: a plotted value must equal, as a number, a number printed by an executed output; v1.0.0 compared the text
'%g' of the value with the printed digits, so a value of a million or more (printed 1e+07) or of more than six digits (0.2045873 against 0.204587) could never be found even when the executed output printed it exactly; every other rule is unchanged) - everything the finished SEN0401 chapter deck shows as a result is produced again, now, and compared. One script for every chapter.
Port of SEN0414's newest deck check (chapter 24's deck_check_v1_0_0.py) to the SEN0401 deck format (console rows in examples_out_v1_0_0.json, no programs):
  1. every '>>>' row on a slide is re-run, in one fresh namespace per slide after the chapter's PRELUDE (examples_v*.py of the chapter's deck folder); what Python answers
     must equal the line shown under it (SEN0401's own check, unchanged in this part: chapter 7 gives the same count and verdict as ch07-deck/deck_check_v1_0_0.py);
  2. (new, from SEN0414) the row, with the result shown, must be a row the recording (examples_out) holds;
  3. (new) the interpreter running this check must be the one the recording was made under (examples_out _python);
  4. native charts: when the recording holds _charts / _tables (SEN0414's format) each must equal a re-execution of its expression and every chart/table on a slide must be
     recorded; for a SEN0401 deck without them, every chart on a slide must equal the chart item of the plan and every plotted value must occur in an executed output
     (a loose provenance test, stated as such in the output);
  5. (new) every ppt/charts part carries data labels.
Usage: sen0401_deck_check_v1_0_0.py NN [deck.pptx]       Environment: SEN0401_ROOT (default the parent of this file's folder).  Exit 0 when nothing mismatches."""
__version__ = "1.1.0"
import glob, importlib.util, json, os, platform, re, sys, zipfile
from xml.dom import minidom

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
newest = lambda pat: sorted(glob.glob(pat), key=vkey)[-1]


def slides(path):
    z = zipfile.ZipFile(path)
    names = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
    out = []
    for n in sorted(names, key=lambda n: int(re.findall(r"\d+", n)[0])):
        d = minidom.parseString(z.read(n))
        paras = []
        for p in d.getElementsByTagName("a:p"):
            paras.append("".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")))
        out.append((n, paras))
    return out


def load_examples(folder):
    f = newest(os.path.join(folder, "examples_v*.py"))
    sys.path.insert(0, folder)
    spec = importlib.util.spec_from_file_location("sen0401_examples", f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.PRELUDE


def rows_check(deck, PRELUDE):
    """SEN0401's own row re-run, byte for byte the logic of ch07-deck/deck_check_v1_0_0.py"""
    bad, n_ex, seen = [], 0, []
    for name, paras in slides(deck):
        ns = {}
        exec(PRELUDE, ns)
        i = 0
        while i < len(paras):
            p = paras[i]
            if p.startswith(">>> "):
                src = p[4:]
                nxt = paras[i + 1] if i + 1 < len(paras) else ""
                shown = None if nxt.startswith(">>> ") else nxt
                try:
                    try:
                        got = repr(eval(src, ns))
                    except SyntaxError:
                        exec(src, ns)
                        got = None
                except Exception as e:
                    got = "%s: %s" % (type(e).__name__, e)
                if got is not None or shown is not None:
                    n_ex += 1
                    if shown is not None and got != shown:
                        bad.append((name, src, shown, got))
                    if shown is not None:
                        seen.append((name, src, shown))
                i += 1 if shown is None else 2
            else:
                i += 1
    return n_ex, bad, seen


def charts_of(z):
    out = []
    for nm in sorted(n for n in z.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", n)):
        d = minidom.parseString(z.read(nm))
        ser = d.getElementsByTagName("c:ser")
        cats = d.getElementsByTagName("c:cat")
        pts = lambda node: [t.firstChild.nodeValue if t.firstChild else "" for p in node.getElementsByTagName("c:pt") for t in p.getElementsByTagName("c:v")]
        labels = pts(cats[0]) if cats else []
        vals = [[float(v) for v in pts(s.getElementsByTagName("c:val")[0])] for s in ser]
        dl = any(x.getAttribute("val") in ("1", "true") for x in d.getElementsByTagName("c:showVal"))
        out.append({"part": nm, "labels": labels, "series": vals, "datalabels": dl})
    return out


def main(argv):
    n = argv[0]; chd = os.path.join(ROOT, "08-tooling", "ch%s-deck" % n)
    deck = argv[1] if len(argv) > 1 else newest(os.path.join(chd, "sen0401_ch%s_deck_v*.pptx" % n))
    rec_path = newest(os.path.join(chd, "examples_out_v*.json")); rec = json.load(open(rec_path))
    PRELUDE = load_examples(chd)
    n_ex, bad, seen = rows_check(deck, PRELUDE)
    notes = []
    if platform.python_version() != rec.get("_python"):
        bad.append(("interpreter", "running %s, the recording was made under %s" % (platform.python_version(), rec.get("_python"))))
    recorded = {(s, o or "") for k, v in rec.items() if not k.startswith("_") and isinstance(v, list) for s, o in v}
    for name, src, shown in seen:
        if (src, shown) not in recorded:
            bad.append((name, src, "not a recorded row with this result"))
    z = zipfile.ZipFile(deck); ch = charts_of(z)
    for c in ch:
        if not c["datalabels"]:
            bad.append(("chart %s" % c["part"], "has no data labels"))
    if "_charts" in rec:
        for k, c in rec["_charts"].items():
            ns = {"HERE": chd}; exec(c["setup"], ns); want = eval(c["expr"], ns)
            labels, values = [w[0] for w in want], [float(w[1]) for w in want]
            if not any(x["labels"] == labels and x["series"] and x["series"][0] == values for x in ch):
                bad.append(("chart", k, "no chart on any slide with the labels and values of a re-run of its expression"))
        for x in ch:
            if not any(x["labels"] == c["labels"] and x["series"] and x["series"][0] == [float(v) for v in c["values"]] for c in rec["_charts"].values()):
                bad.append(("chart %s" % x["part"], "is not a recorded chart"))
        notes.append("charts compared with %d recorded expression(s)" % len(rec["_charts"]))
    else:
        plan = json.load(open(newest(os.path.join(chd, "deck_plan_v*.json"))))
        pc = [it for s in plan["slides"] for it in s.get("items", []) if it.get("t") == "chart"]
        outtext = " ".join(o for k, v in rec.items() if not k.startswith("_") and isinstance(v, list) for s, o in v)
        toks = {float(t) for t in re.findall(r"-?\d+(?:\.\d+)?", outtext.replace(",", "").replace("_", ""))}
        if len(pc) != len(ch):
            bad.append(("charts", "the plan has %d chart item(s), the file %d chart part(s)" % (len(pc), len(ch))))
        for it in pc:
            want = [[float(v) for v in s["data"]] for s in it["series"]]
            if not any(x["labels"] == [str(l) for l in it["labels"]] and x["series"] == want for x in ch):
                bad.append(("chart", it.get("title", ""), "no chart part equals the plan's chart item"))
            for s in it["series"]:
                for v in s["data"]:
                    if float(v) not in toks:
                        bad.append(("chart", it.get("title", ""), "value %g is in no executed output (provenance)" % float(v)))
        notes.append("charts compared with the plan's %d chart item(s); every plotted value found in an executed output (loose provenance)" % len(pc))
    print("sen0401_deck_check %s (chapter %s, %s) under Python %s: %d examples re-run on %d slides; %d chart(s); %d mismatch(es); %s"
          % (__version__, n, os.path.basename(deck), platform.python_version(), n_ex, len(slides(deck)), len(ch), len(bad), "; ".join(notes)))
    for b in bad:
        print("  REFUSED", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
