#!/usr/bin/env python3
"""sen0401_deck_honesty_check v1.0.0 - a reader must be able to tell what ran as shown from what was recorded or not run at all (port of SEN0414's chapter 24 honesty check, generalised:
SEN0414's is bound to its stand-ins for a sound card; SEN0401's honesty is about a machine with no Bitcoin Core node, no wallet, no hardware, no live network). From the finished .pptx, the
recording (examples_out) and the plan's meta:
  1. every slide that shows a '>>>' console carries the caption 'run under Python <version>' of the recording's _python (the SEN0401 console caption), and no slide shows a different version;
  2. plan meta 'honesty' (optional) = {"title": [phrases the title slide must carry], "notExecuted": [slide numbers], "recorded": [slide numbers], "standin": {"<slide>": [phrases]}}:
     every listed notExecuted slide must carry 'NOT EXECUTED', every recorded slide the word 'Recorded', every standin slide each of its phrases, the title slide each of its phrases; and
     (only when the key exists) no other slide may say 'NOT EXECUTED' or 'Recorded', and no unlisted slide may call something a 'stand-in';
  3. the title slide of a deck without a Bitcoin Core node (meta.honesty.no_node true) must say so ('no Bitcoin Core node' or 'no node'), and every slide that shows a result taken from
     Core's published vectors or from a saved block says 'published' or 'saved' on the slide (the plan lists those slides under meta.honesty.vectors);
  4. when meta has no 'honesty' key the check reports that nothing is configured (exit 0, and says so) unless --require is given - a SEN0401 deck must then state its limits in 'honesty'.
Usage: sen0401_deck_honesty_check_v1_0_0.py NN [--require]       Environment: SEN0401_ROOT, SEN0401_DECK (a deck file to check instead of the chapter's newest).  Exit 0 when nothing is refused."""
__version__ = "1.0.0"
import glob, json, os, re, sys, zipfile
from xml.dom import minidom

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
newest = lambda pat: sorted(glob.glob(pat), key=vkey)[-1]


def slide_texts(deck):
    z = zipfile.ZipFile(deck); out = []
    for nm in sorted((x for x in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", x)), key=lambda s: int(re.findall(r"\d+", s)[0])):
        d = minidom.parseString(z.read(nm)); out.append([ "".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")) for p in d.getElementsByTagName("a:p")])
    return out


def main(a):
    n = a[0]; chd = os.path.join(TOOL, "ch%s-deck" % n)
    plan = json.load(open(newest(os.path.join(chd, "deck_plan_v*.json")))); rec = json.load(open(newest(os.path.join(chd, "examples_out_v*.json"))))
    T = slide_texts(os.environ.get("SEN0401_DECK") or newest(os.path.join(chd, "sen0401_ch%s_deck_v*.pptx" % n)))
    hon = plan["meta"].get("honesty"); bad = []; py = rec["_python"]
    shown = 0
    for i, paras in enumerate(T, 1):
        text = "\n".join(paras)
        if any(p.startswith(">>> ") for p in paras):
            shown += 1
            vs = set(re.findall(r"run under Python ([0-9.]+)", text))
            if vs != {py}: bad.append((i, "shows a console but its caption says Python %s, the recording was made under %s" % (sorted(vs) or "nothing", py)))
    if hon is None:
        if "--require" in a: bad.append((0, "plan meta has no 'honesty' key (a SEN0401 deck must state what it did not run)"))
        note = "no meta.honesty: only the console captions were checked"
    else:
        ne, rc = set(hon.get("notExecuted", [])), set(hon.get("recorded", [])); note = "meta.honesty read"
        for i, paras in enumerate(T, 1):
            text = "\n".join(paras)
            if (i in ne) != ("NOT EXECUTED" in text): bad.append((i, "NOT EXECUTED is %s on the slide and %s in the plan" % ("present" if "NOT EXECUTED" in text else "absent", "listed" if i in ne else "not listed")))
            if (i in rc) != (re.search(r"\bRecorded\b", text) is not None): bad.append((i, "'Recorded' is %s on the slide and %s in the plan" % ("present" if re.search(r"\bRecorded\b", text) else "absent", "listed" if i in rc else "not listed")))
            for ph in hon.get("standin", {}).get(str(i), []):
                if ph not in text: bad.append((i, "a stand-in slide lacks the phrase %r" % ph))
            if str(i) not in hon.get("standin", {}) and re.search(r"stand-in|stands in for", text, re.I) and i != 1: bad.append((i, "calls something a stand-in but is not listed"))
        t1 = "\n".join(T[0]).lower()
        for ph in hon.get("title", []):
            if ph.lower() not in t1: bad.append((1, "the title slide lacks %r" % ph))
        if hon.get("no_node") and not re.search(r"no (bitcoin core )?node", t1): bad.append((1, "the deck ran without a Bitcoin Core node but the title slide does not say 'no node'"))
        if "NOT EXECUTED" in "\n".join(T[0]): bad.append((1, "the title slide says NOT EXECUTED, which belongs to slides of results"))
        for i in hon.get("vectors", []):
            if not re.search(r"published|saved", "\n".join(T[i - 1]), re.I): bad.append((i, "shows a result of Core's vectors or a saved block without saying published or saved"))
    print("sen0401_deck_honesty_check %s (chapter %s): %d console slide(s) captioned with Python %s; %s; %d refusal(s)" % (__version__, n, shown, py, note, len(bad)))
    for b in bad: print("  REFUSED slide %d: %s" % b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
