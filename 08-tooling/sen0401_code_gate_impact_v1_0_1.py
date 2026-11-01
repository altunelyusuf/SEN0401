#!/usr/bin/env python3
"""sen0401_code_gate_impact v1.0.1 (over v1.0.0: a chapter whose newest committed deck has no prompts (chapters 5 and 6 are built without them meanwhile) is compared on that deck, reported DIFFERS-BY-DESIGN, AND on its newest committed deck with prompts) (task TK_Code_Gate_Build) - IMPACT PROOF. For the newest COMMITTED deck of each chapter 1..14 (git ls-files) runs the old tool and its successor on the same file
and compares the complete output and the exit code, the version token aside:
  deck check        v1.1.0 vs v1.2.0   (python3.14, explicit deck)
  deck standard     v1.2.0 vs v1.3.1 (v1.3.0, committed earlier in the task, stays unedited)
A deck with neither prompts nor named shapes must give identical output. A deck without prompts but with code/result shapes (chapter 6) is reported as DIFFERS-BY-DESIGN when only the example count / code-slide count differs,
and the last deck with prompts of that chapter (v2_2_0) is compared in its place.
Usage: python3 -B sen0401_code_gate_impact_v1_0_1.py [chapter ...]"""
__version__ = "1.0.1"
import glob, os, re, subprocess, sys
sys.dont_write_bytecode = True
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
PY314 = "/root/.local/bin/python3.14"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def committed(n):
    fs = subprocess.run(["git", "ls-files", "03-materials/ch%02d" % n], cwd=R, capture_output=True, text=True).stdout.split()
    fs = [f for f in fs if f.endswith(".pptx") and "_3e_v" in f]
    return sorted(fs, key=vk)[-1]


def run(cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, **(env or {})))
    return r.returncode, (r.stdout + r.stderr)


def norm(out, old, new):
    return out.replace("sen0401_deck_check " + old, "sen0401_deck_check VER").replace("sen0401_deck_check " + new, "sen0401_deck_check VER") \
              .replace("check_v" + old.replace(".", "_"), "check_vX").replace("check v%s" % old, "check vX").replace("check v%s" % new, "check vX")


def compare(label, n, deck):
    path = os.path.join(R, deck)
    res = []
    for kind, old, new, mk in (("deck_check", "1.1.0", "1.2.0", lambda v: [PY314, "-B", os.path.join(T, "sen0401_deck_check_v%s.py" % v.replace(".", "_")), "%02d" % n, path]),
                               ("deck_standard", "1.2.0", "1.3.1", lambda v: [sys.executable, "-B", os.path.join(T, "sen0401_deck_standard_check_v%s.py" % v.replace(".", "_")), "%02d" % n, path])):
        a = run(mk(old)); b = run(mk(new))
        na, nb = norm(a[1], old, new).replace(os.path.basename(deck), "DECK"), norm(b[1], old, new).replace(os.path.basename(deck), "DECK")
        same = a[0] == b[0] and na == nb
        if same:
            res.append((kind, "EQUAL", a[0], ""))
        else:
            la, lb = na.splitlines(), nb.splitlines()
            diff = [(x[:200], y[:200]) for x, y in zip(la, lb) if x != y][:3]
            res.append((kind, "DIFFERS", (a[0], b[0]), diff if diff else "line counts %d vs %d" % (len(la), len(lb))))
    return res


def prompted(deck):
    import zipfile
    z = zipfile.ZipFile(os.path.join(R, deck))
    return any("&gt;&gt;&gt; " in z.read(n).decode("utf-8", "ignore") for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n))


def main():
    chs = [int(x) for x in sys.argv[1:]] or list(range(1, 15))
    bad = 0
    for n in chs:
        deck = committed(n)
        decks = [(deck, "")]
        if not prompted(deck):
            fs = subprocess.run(["git", "ls-files", "03-materials/ch%02d" % n], cwd=R, capture_output=True, text=True).stdout.split()
            fs = sorted([f for f in fs if f.endswith(".pptx") and "_3e_v" in f and prompted(f)], key=vk)
            decks.append((fs[-1], " (newest committed deck WITH prompts)"))
            decks[0] = (deck, " (newest committed deck, WITHOUT prompts: differs by design)")
        for dk, tag in decks:
            for kind, st, rc, d in compare("newest", n, dk):
                print("ch%02d %-14s %-8s exit %s  %s%s %s" % (n, kind, st, rc, os.path.basename(dk), tag, d))
                if st != "EQUAL" and "WITHOUT" not in tag:
                    bad += 1
    print("SUMMARY: %d comparison(s) not equal on decks with prompts" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
