#!/usr/bin/env python3
"""sen0401_deck_fixtures v1.2.0 (over v1.1.0: the credit and date fixtures find their story picture's credit whatever its licence - CC BY-SA, else CC BY with or without a version, e.g. deck 14's 'CC BY 4.0' - and change the licence to CC BY-NC; no check, threshold or other fixture is changed). v1.1.0 (over v1.0.0: the owners are the current versions of the checks - deck_check 1.1.0, picture_check 1.1.0 - and the arc and lookfeel owners are run with --slides N for the fixture's own slide count, so a deck of other than 26 slides is refused for the fixture's reason, not for its length; the fixtures are written as fixture_<name>_v1_2_0.pptx; the rest is unchanged) - the checks must discriminate: stale fixtures that each check must REFUSE, and one control it must ACCEPT (port of the idea of SEN0414's
fixtures_make_v1_0_0.py, which is bound to chapter 24's slide numbers and texts; here every target is FOUND in the finished deck, so one script serves every chapter).
Each fixture is the finished deck with ONE run of text, ONE chart value, ONE picture, ONE background or ONE paragraph changed to something plausible that is not what Python printed,
what the file must say or what the standard allows. `--run` makes them in a temporary folder and runs the check that owns each, two at a time; a fixture that is not refused, or the control
that is refused, fails the run (exit 1).
  stale_expr           the first console result changed ('OK' -> 'OK0' style: last number +1, else a character appended)      owner: sen0401_deck_check
  stale_chart          the first value of the first native chart +1                                                          owner: sen0401_deck_check
  stale_caption        'run under Python <v>' on the first console slide changed to another version                         owner: sen0401_deck_honesty_check
  stale_credit         the licence in the first story picture's credit changed (CC BY-SA -> CC BY-NC)                         owner: sen0401_story_check
  stale_date           the first story's date on its slide changed by one day                                                owner: sen0401_story_check
  stale_background     the background of slide 3 changed to black                                                           owner: sen0401_deck_lookfeel_check
  stale_number         the number 'n / N' of slide 4 changed                                                                 owner: sen0401_deck_lookfeel_check
  stale_colour         the first code-block fill 23272E changed to 000011                                                    owner: sen0401_deck_lookfeel_check
  stale_agenda         the first agenda range changed ('slides 3-4' -> 'slides 3-5')                                         owner: sen0401_deck_arc_check
  stale_pPr            a paragraph-properties element placed after a run on slide 3                                          owner: sen0401_deck_structure_check
  stale_directive      'SAY: ' put in front of the notes of slide 3                                                          owner: deck_notes_check
  stale_image_pixel    the first picture replaced by the same picture with ONE pixel changed                                 owner: sen0401_deck_picture_check
  stale_image_swap     the first picture replaced by the second picture of the deck                                          owner: sen0401_deck_picture_check
  ok_image_reencoded   (control, must be accepted) the first picture re-encoded by Pillow: other bytes, the same pixels      owner: sen0401_deck_picture_check
Usage: sen0401_deck_fixtures_v1_0_0.py NN --run [--deck file.pptx]       or       sen0401_deck_fixtures_v1_0_0.py NN <outdir> [--deck file.pptx]   (needs Pillow, python-pptx not needed)
Environment: SEN0401_ROOT, PY314 (the interpreter the deck check needs, default /root/.local/bin/python3.14)."""
__version__ = "1.2.0"
import glob, io, os, re, subprocess, sys, tempfile, zipfile
from concurrent.futures import ThreadPoolExecutor
from xml.sax.saxutils import escape
from PIL import Image

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
PY314 = os.environ.get("PY314", "/root/.local/bin/python3.14")
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
newest = lambda pat: sorted(glob.glob(pat), key=vkey)[-1]


def zi(it):
    i = zipfile.ZipInfo(it.filename, it.date_time); i.compress_type = zipfile.ZIP_DEFLATED; i.external_attr = it.external_attr; return i


def make(n, deck, out):
    os.makedirs(out, exist_ok=True); z = zipfile.ZipFile(deck); N = len([x for x in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", x)])
    S = lambda k: z.read("ppt/slides/slide%d.xml" % k).decode("utf-8")
    f = lambda name: os.path.join(out, "fixture_%s_v1_2_0.pptx" % name)

    def edit(name, part, old, new):
        zo = zipfile.ZipFile(f(name), "w", zipfile.ZIP_DEFLATED); hit = 0
        for it in z.infolist():
            data = z.read(it.filename)
            if it.filename == part:
                if isinstance(new, bytes): data = new
                else:
                    assert data.decode("utf-8").count(old) == 1, (name, part, old, data.decode("utf-8").count(old))
                    data = data.decode("utf-8").replace(old, new, 1).encode("utf-8")
                hit += 1
            zo.writestr(zi(it), data)
        zo.close(); assert hit == 1, (name, part)

    made = []
    # a console result: '>>> src' paragraph followed by the result paragraph, whose text is unique on its slide
    for k in range(1, N + 1):
        paras = re.findall(r"<a:p>.*?</a:p>", S(k), re.S); txt = ["".join(re.findall(r"<a:t>([^<]*)</a:t>", p)) for p in paras]
        hit = None
        for i in range(len(txt) - 1):
            if txt[i].startswith("&gt;&gt;&gt; ") and txt[i + 1] and not txt[i + 1].startswith("&gt;&gt;&gt; ") and S(k).count("<a:t>%s</a:t>" % txt[i + 1]) == 1:
                hit = txt[i + 1]; break
        if hit:
            m = list(re.finditer(r"\d+", hit))
            new = hit[:m[-1].start()] + str(int(m[-1].group()) + 1) + hit[m[-1].end():] if m else hit + "0"
            edit("stale_expr", "ppt/slides/slide%d.xml" % k, "<a:t>%s</a:t>" % hit, "<a:t>%s</a:t>" % new); made.append("stale_expr"); break
    ch = sorted(x for x in z.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", x))
    if ch:
        x = z.read(ch[0]).decode("utf-8"); m = re.search(r"(<c:val>.*?<c:v>)(\d+(?:\.\d+)?)(</c:v>)", x, re.S)
        old = m.group(1) + m.group(2) + m.group(3); new = m.group(1) + (str(int(m.group(2)) + 1) if "." not in m.group(2) else "%.2f" % (float(m.group(2)) + 0.01)) + m.group(3)
        zo = zipfile.ZipFile(f("stale_chart"), "w", zipfile.ZIP_DEFLATED)
        for it in z.infolist(): zo.writestr(zi(it), x.replace(old, new, 1).encode("utf-8") if it.filename == ch[0] else z.read(it.filename))
        zo.close(); made.append("stale_chart")
    for k in range(1, N + 1):
        m = re.search(r"run under Python ([0-9.]+)", S(k))
        if m and S(k).count(m.group(0)) == 1:
            edit("stale_caption", "ppt/slides/slide%d.xml" % k, m.group(0), "run under Python 3.13.0"); made.append("stale_caption"); break
    for lic in (r"CC BY-SA", r"CC BY(?: \d\.\d)?"):  # CC BY-SA first (decks 1-13); a plain CC BY credit (deck 14) only when no slide has a BY-SA one
        if "stale_date" in made: break
        for k in range(1, N + 1):
            m = re.search(lic, S(k))
            if m and "<a:t>" in S(k):
                s = S(k); i = m.start()
                if re.search(r"\d{4}-\d{2}-\d{2}", s):
                    zo = zipfile.ZipFile(f("stale_credit"), "w", zipfile.ZIP_DEFLATED)
                    for it in z.infolist(): zo.writestr(zi(it), (s[:i] + "CC BY-NC" + s[m.end():]).encode("utf-8") if it.filename == "ppt/slides/slide%d.xml" % k else z.read(it.filename))
                    zo.close(); made.append("stale_credit")
                    d = re.search(r"<a:t>(\d{4})-(\d{2})-(\d{2})</a:t>", s)
                    edit("stale_date", "ppt/slides/slide%d.xml" % k, d.group(0), "<a:t>%s-%s-%02d</a:t>" % (d.group(1), d.group(2), (int(d.group(3)) % 27) + 1)); made.append("stale_date"); break
    edit("stale_background", "ppt/slides/slide3.xml", re.search(r"<p:bg>.*?</p:bg>", S(3), re.S).group(0), re.sub(r'srgbClr val="[0-9A-Fa-f]{6}"', 'srgbClr val="000000"', re.search(r"<p:bg>.*?</p:bg>", S(3), re.S).group(0))); made.append("stale_background")
    edit("stale_number", "ppt/slides/slide4.xml", "<a:t>4 / %d</a:t>" % N, "<a:t>5 / %d</a:t>" % N); made.append("stale_number")
    for k in range(2, N + 1):
        if S(k).count('srgbClr val="23272E"') >= 1:
            s = S(k); i = s.index('srgbClr val="23272E"')
            zo = zipfile.ZipFile(f("stale_colour"), "w", zipfile.ZIP_DEFLATED)
            for it in z.infolist(): zo.writestr(zi(it), (s[:i] + 'srgbClr val="000011"' + s[i + 20:]).encode("utf-8") if it.filename == "ppt/slides/slide%d.xml" % k else z.read(it.filename))
            zo.close(); made.append("stale_colour"); break
    for k in range(1, N + 1):
        m = re.search(r"\(slides 3-(\d+)\)", S(k))
        if m:
            edit("stale_agenda", "ppt/slides/slide%d.xml" % k, m.group(0), "(slides 3-%d)" % (int(m.group(1)) + 1)); made.append("stale_agenda"); break
    s3 = S(3); p = re.search(r"<a:p>(<a:pPr[^>]*?(?:/>|>.*?</a:pPr>))(<a:r>.*?</a:r>)(<a:endParaRPr.*?(?:/>|</a:endParaRPr>))?</a:p>", s3, re.S)
    if p:
        bad = "<a:p>" + p.group(2) + p.group(1) + (p.group(3) or "") + "</a:p>"
        edit("stale_pPr", "ppt/slides/slide3.xml", p.group(0), bad); made.append("stale_pPr")
    nn = "ppt/notesSlides/notesSlide3.xml"
    if nn in z.namelist():
        t = re.search(r"<a:t>([^<]+)</a:t>", z.read(nn).decode("utf-8")); edit("stale_directive", nn, t.group(0), "<a:t>SAY: %s</a:t>" % t.group(1)); made.append("stale_directive")
    media = sorted((x for x in z.namelist() if x.startswith("ppt/media/") and not x.endswith("/") and x.lower().endswith((".png", ".jpg", ".jpeg"))), key=lambda s: [int(v) for v in re.findall(r"\d+", s)])
    if len(media) >= 2:
        fmt = "PNG" if media[0].lower().endswith(".png") else "JPEG"
        im = Image.open(io.BytesIO(z.read(media[0]))).convert("RGB"); v = im.getpixel((10, 10)); im.putpixel((10, 10), ((v[0] + 40) % 256,) + v[1:])
        b = io.BytesIO(); im.save(b, fmt, **({} if fmt == "PNG" else {"quality": 100, "subsampling": 0})); edit("stale_image_pixel", media[0], None, b.getvalue()); made.append("stale_image_pixel")
        edit("stale_image_swap", media[0], None, z.read(media[1])); made.append("stale_image_swap")
        b = io.BytesIO(); Image.open(io.BytesIO(z.read(media[0]))).save(b, fmt, **({"optimize": True} if fmt == "PNG" else {"quality": 100, "subsampling": 0}))
        if b.getvalue() != z.read(media[0]): edit("ok_image_reencoded", media[0], None, b.getvalue()); made.append("ok_image_reencoded")
    return made


REASON = {"stale_expr": r"slide\d+\.xml", "stale_chart": r"chart", "stale_caption": r"caption says", "stale_credit": r"credit", "stale_date": r"date and the picture", "stale_background": r"background 000000",
          "stale_number": r"no visible number", "stale_colour": r"colours outside", "stale_agenda": r"agenda", "stale_pPr": r"slide\d+\.xml", "stale_directive": r"FAIL", "stale_image_pixel": r"equals no file",
          "stale_image_swap": r"not the file the plan names"}


def owners(n, deck_of):
    py = sys.executable; T = TOOL
    return {"stale_expr": ("sen0401_deck_check", [PY314, T + "/sen0401_deck_check_v1_1_0.py", n, "{fx}"]),
            "stale_chart": ("sen0401_deck_check", [PY314, T + "/sen0401_deck_check_v1_1_0.py", n, "{fx}"]),
            "stale_caption": ("sen0401_deck_honesty_check", [py, T + "/sen0401_deck_honesty_check_v1_0_0.py", n]),
            "stale_credit": ("sen0401_story_check", [py, T + "/sen0401_story_check_v1_0_0.py", n]),
            "stale_date": ("sen0401_story_check", [py, T + "/sen0401_story_check_v1_0_0.py", n]),
            "stale_background": ("sen0401_deck_lookfeel_check", [py, T + "/sen0401_deck_lookfeel_check_v1_0_0.py", n, "{fx}"]),
            "stale_number": ("sen0401_deck_lookfeel_check", [py, T + "/sen0401_deck_lookfeel_check_v1_0_0.py", n, "{fx}"]),
            "stale_colour": ("sen0401_deck_lookfeel_check", [py, T + "/sen0401_deck_lookfeel_check_v1_0_0.py", n, "{fx}"]),
            "stale_agenda": ("sen0401_deck_arc_check", [py, T + "/sen0401_deck_arc_check_v1_1_0.py", n]),
            "stale_pPr": ("sen0401_deck_structure_check", [py, T + "/sen0401_deck_structure_check_v1_0_0.py", "{fx}"]),
            "stale_directive": ("deck_notes_check", [py, T + "/deck_notes_check_v1_0_0.py", "{fx}"]),
            "stale_image_pixel": ("sen0401_deck_picture_check", [py, T + "/sen0401_deck_picture_check_v1_1_0.py", n, "{fx}"]),
            "stale_image_swap": ("sen0401_deck_picture_check", [py, T + "/sen0401_deck_picture_check_v1_1_0.py", n, "{fx}"]),
            "ok_image_reencoded": ("sen0401_deck_picture_check", [py, T + "/sen0401_deck_picture_check_v1_1_0.py", n, "{fx}"])}


def main(a):
    n = a[0]; run = "--run" in a
    deck = a[a.index("--deck") + 1] if "--deck" in a else newest(os.path.join(TOOL, "ch%s-deck" % n, "sen0401_ch%s_deck_v*.pptx" % n))
    out = tempfile.mkdtemp(prefix="sen0401_fx_") if run else [x for x in a[1:] if not x.startswith("--") and x != deck][0]
    made = make(n, deck, out); print("sen0401_deck_fixtures %s: %d fixture(s) made from %s in %s" % (__version__, len(made), os.path.basename(deck), out))
    if not run: return 0
    own = owners(n, deck); bad = []

    def one(name):
        fx = os.path.join(out, "fixture_%s_v1_2_0.pptx" % name); owner, cmd = own[name]
        cmd = [c.replace("{fx}", fx) for c in cmd]
        if owner in ("sen0401_deck_arc_check", "sen0401_deck_lookfeel_check"):
            cmd += ["--slides", str(len([x for x in zipfile.ZipFile(fx).namelist() if re.match(r"ppt/slides/slide\d+\.xml$", x)]))]
        r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, SEN0401_DECK=fx, SEN0401_ROOT=ROOT), cwd=TOOL)
        why = next((l.strip() for l in (r.stdout + r.stderr).splitlines() if "REFUSED" in l), (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "")
        full = r.stdout + r.stderr
        right = name not in REASON or re.search(REASON[name], full) is not None
        return name, owner, (r.returncode if right else 0 if name in REASON else r.returncode), why[:150] if right else "refused, but not for the fixture's reason (%s)" % REASON[name]
    with ThreadPoolExecutor(2) as ex:
        for name, owner, rc, why in sorted(ex.map(one, made)):
            control = name.startswith("ok_")
            ok = (rc == 0) if control else (rc != 0)
            print("%s %s %s by %s: %s" % ("ok  " if ok else "FAIL", "control" if control else "fixture", name, owner, ("accepted" if control else "refused") if ok else ("REFUSED but must be accepted" if control else "NOT REFUSED")) + ("" if control and ok else " | " + why))
            if not ok: bad.append(name)
    expected = {"stale_expr", "stale_chart", "stale_caption", "stale_credit", "stale_date", "stale_background", "stale_number", "stale_colour", "stale_agenda", "stale_pPr", "stale_directive", "stale_image_pixel", "stale_image_swap", "ok_image_reencoded"}
    print("fixtures not made for this deck (no target found): %s" % (sorted(expected - set(made)) or "none"))
    print("sen0401_deck_fixtures: %s" % ("every stale fixture refused, the control accepted" if not bad else "FAILED: %s" % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
