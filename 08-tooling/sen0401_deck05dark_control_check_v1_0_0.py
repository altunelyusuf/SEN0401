#!/usr/bin/env python3
"""sen0401_deck05dark_control_check v1.0.0 - the control's OWN checks of the chapter 5 deck v3_4_0 (story ST_Ch05_DeckDark, criterion AC9_Ch05_DeckDark). A NEW tool (derived from sen0401_deck05_control_check_v1_0_0.py); it edits nothing.
Usage: sen0401_deck05dark_control_check_v1_0_0.py KIND
  sha       the deck v3_3_0 has the same SHA-256 in the commit before the executor's work (parent of the first commit) as now, and no later commit touches it
  parts     the part lists of v3_3_0 and v3_4_0 are equal and only docProps/core.xml and ppt/slides/slide68.xml differ
  textdiff  the text of every shape and table and the notes of every slide are identical
  links     the hyperlink addresses of v3_3_0 equal those of v3_4_0
  charts    the chart parts are byte-identical
  contrast  the control's OWN reading of slide 68: slide background colour, luminance below 0.5 (dark), and for every text run the contrast ratio against the filled shape or background under it (WCAG AA: 4.5 normal, 3 large = 18pt or 14pt bold); every other slide (1..67) is byte-identical to v3_3_0 and light
  plan      plan v3_4_0 declares the last slide kind closing and bg dark; its other slides equal those of the newest earlier plan
  dcheck    the deck check v1_1_0 under venv314 on v3_4_0: exit 0 and '0 mismatch(es)'
  arc0      the arc check v1_3_0 on v3_4_0: exit 0 and no REFUSED line
  std       the deck standard check v1_2_0 on v3_4_0: exit 0, D1 to D12 all PASS, D9 reads exactly one dark slide, number 68
Exit 0 only when the kind holds."""
__version__ = "1.0.0"
import glob, hashlib, json, os, re, subprocess, sys, zipfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(R, "03-materials/ch05")
OLD = os.path.join(D, "SEN0401_Ch05_WalletRecovery_3e_v3_3_0.pptx"); NEW = os.path.join(D, "SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx")
PARENT = "4ec9684"; V = "/home/claude/venv314/bin/python"
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*a): return subprocess.run(["git", "-C", R] + list(a), capture_output=True).stdout
def done(ok, msg): print(msg); print("RESULT " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
def texts(path):
    from pptx import Presentation
    out = []
    for s in Presentation(path).slides:
        l = []
        for sh in s.shapes:
            if sh.has_text_frame: l += [p.text for p in sh.text_frame.paragraphs]
            if sh.has_table: l += [" | ".join(c.text for c in r.cells) for r in sh.table.rows]
        out.append((l, s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""))
    return out
def links(p):
    z = zipfile.ZipFile(p); o = set()
    for n in z.namelist():
        if re.match(r"ppt/slides/_rels/slide\d+\.xml\.rels$", n):
            for m in re.finditer(r"<Relationship [^>]*>", z.read(n).decode()):
                if "/hyperlink" in m.group(0): o.add(re.search(r'Target="([^"]+)"', m.group(0)).group(1))
    return o
def k_sha():
    rel = "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_3_0.pptx"; b = git("show", "%s:%s" % (PARENT, rel)); n = open(os.path.join(R, rel), "rb").read(); ok = len(b) > 0 and sha(b) == sha(n)
    print("%s before(%s) %s after %s %s" % (rel, PARENT, sha(b), sha(n), "equal" if ok else "DIFFERENT"))
    ch = git("log", "--format=%h", "%s..HEAD" % PARENT, "--", rel).split(); print("commits since touching it: %s" % ch); done(ok and not ch, "sha")
def k_parts():
    a, b = zipfile.ZipFile(OLD), zipfile.ZipFile(NEW); na, nb = sorted(a.namelist()), sorted(b.namelist()); diff = [n for n in na if n in nb and a.read(n) != b.read(n)]
    print("part lists equal: %s (%d parts); differing parts: %s" % (na == nb, len(na), diff)); done(na == nb and sorted(diff) == ["docProps/core.xml", "ppt/slides/slide68.xml"], "parts")
def k_text():
    a, b = texts(OLD), texts(NEW); ch = [i + 1 for i in range(min(len(a), len(b))) if a[i] != b[i]]; print("slides %d and %d; slides whose text or notes differ: %s" % (len(a), len(b), ch)); done(len(a) == len(b) and not ch, "textdiff")
def k_links():
    a, b = links(OLD), links(NEW); print("distinct addresses v3_3_0: %d, v3_4_0: %d; only in old: %s; only in new: %s" % (len(a), len(b), sorted(a - b), sorted(b - a))); done(a == b and len(b) > 0, "links")
def k_charts():
    a, b = zipfile.ZipFile(OLD), zipfile.ZipFile(NEW); ca = sorted(n for n in a.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", n)); cb = sorted(n for n in b.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", n))
    same = ca == cb and all(a.read(n) == b.read(n) for n in ca)
    print("chart parts v3_3_0: %d, v3_4_0: %d, byte-identical: %s (the comparison of the charts with the plan's chart items is made by the deck check, kind dcheck)" % (len(ca), len(cb), same)); done(same and len(cb) > 0, "charts")
def k_dcheck():
    r = subprocess.run([V, "-B", os.path.join(R, "08-tooling/sen0401_deck_check_v1_1_0.py"), "05", NEW], capture_output=True, text=True); out = (r.stdout + r.stderr).strip(); print(out[-900:]); print("exit %d" % r.returncode)
    done(r.returncode == 0 and "0 mismatch(es)" in out, "dcheck")
def lum(h):
    f = lambda c: (c / 255 / 12.92) if c / 255 <= 0.03928 else (((c / 255 + 0.055) / 1.055) ** 2.4)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16); return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb); return (hi + 0.05) / (lo + 0.05)
def fillhex(fill):
    try:
        if fill.type == 1: return str(fill.fore_color.rgb)
    except Exception: pass
    return None
def k_contrast():
    from pptx import Presentation
    pn, po = Presentation(NEW), Presentation(OLD); sl = pn.slides[len(pn.slides) - 1]; ok = True
    bg = fillhex(sl.background.fill); print("slide %d of %d background: %s" % (len(pn.slides), len(pn.slides), bg))
    if not bg: print("background colour not read"); done(False, "contrast")
    L = lum(bg); print("relative luminance %.3f (dark below 0.5)" % L); ok &= L < 0.5
    boxes = []
    for sh in sl.shapes:
        h = fillhex(sh.fill) if hasattr(sh, "fill") else None
        if h: boxes.append((sh.left, sh.top, sh.left + sh.width, sh.top + sh.height, h, sh.shape_id))
    n = 0
    for sh in sl.shapes:
        if not sh.has_text_frame: continue
        own = fillhex(sh.fill) if hasattr(sh, "fill") else None; cx, cy = sh.left + sh.width / 2, sh.top + sh.height / 2
        under = own or next((b[4] for b in reversed(boxes) if b[5] != sh.shape_id and b[0] <= cx <= b[2] and b[1] <= cy <= b[3]), None) or bg
        for para in sh.text_frame.paragraphs:
            for r in para.runs:
                if not r.text.strip(): continue
                try: fg = str(r.font.color.rgb)
                except Exception: fg = None
                if not fg: print("  unresolved colour for run %r" % r.text[:30]); ok = False; continue
                pt = r.font.size.pt if r.font.size else 18.0; big = pt >= 18 or (pt >= 14 and bool(r.font.bold)); need = 3.0 if big else 4.5; c = ratio(fg, under); good = c >= need; n += 1
                print("  %-5.1fpt %s on %s %.2f:1 needs %.1f %s | %s" % (pt, fg, under, c, need, "OK" if good else "BELOW", r.text[:44])); ok &= good
    print("%d text runs measured" % n); ok &= n > 0
    # the other slides: byte-identical slide parts, and light
    a, b = zipfile.ZipFile(OLD), zipfile.ZipFile(NEW); other = [m for m in b.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", m) and m != "ppt/slides/slide%d.xml" % len(pn.slides) and a.read(m) != b.read(m)]
    print("other slide parts that differ from v3_3_0: %s" % other); ok &= not other
    light = [i + 1 for i, s_ in enumerate(pn.slides) if (fillhex(s_.background.fill) and lum(fillhex(s_.background.fill)) < 0.5)]; print("dark slides in v3_4_0 by the control's own read: %s" % light); ok &= light == [len(pn.slides)]
    done(ok, "contrast")
def k_plan():
    ps = sorted(glob.glob(os.path.join(R, "08-tooling/ch05-deck/deck_plan_v*.json")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[0]]); new, old = json.load(open(ps[-1])), json.load(open(ps[-2])); print("plans: %s, %s" % (os.path.basename(ps[-2]), os.path.basename(ps[-1])))
    ls = new["slides"][-1]; print("last slide of the new plan: %s" % {k: ls[k] for k in ls if k in ("kind", "bg", "title", "n", "id")}); ok = ls.get("kind") == "closing" and ls.get("bg") == "dark"
    d = [i + 1 for i in range(min(len(new["slides"]), len(old["slides"]))) if new["slides"][i] != old["slides"][i]]; print("slides of the plan that differ from the earlier plan: %s (slides %d and %d)" % (d, len(old["slides"]), len(new["slides"]))); ok &= len(new["slides"]) == len(old["slides"]) and d in ([], [len(new["slides"])])
    done(ok, "plan")
def k_dcheck():
    r = subprocess.run([V, "-B", os.path.join(R, "08-tooling/sen0401_deck_check_v1_1_0.py"), "05", NEW], capture_output=True, text=True); out = (r.stdout + r.stderr).strip(); print(out[-600:]); print("exit %d" % r.returncode)
    done(r.returncode == 0 and "0 mismatch(es)" in out, "dcheck")
def k_arc0():
    r = subprocess.run([sys.executable, "-B", os.path.join(R, "08-tooling/sen0401_deck_arc_check_v1_3_0.py"), "05"], capture_output=True, text=True, env=dict(os.environ, SEN0401_DECK=NEW)); o = r.stdout + r.stderr; ref = [l.strip() for l in o.splitlines() if "REFUSED" in l]
    print(o.strip()[-500:]); print("exit %d, refusals %d" % (r.returncode, len(ref))); done(r.returncode == 0 and not ref, "arc0")
def k_std():
    r = subprocess.run([sys.executable, "-B", os.path.join(R, "08-tooling/sen0401_deck_standard_check_v1_2_0.py"), "05", NEW], capture_output=True, text=True); o = r.stdout + r.stderr; res = dict(re.findall(r"^(D\d+) (PASS|FAIL|NOT_MEASURED|CANNOT_RUN)", o, re.M)); d9 = [l for l in o.splitlines() if l.startswith("D9")]
    print("exit %d; %s" % (r.returncode, " ".join("%s:%s" % kv for kv in sorted(res.items())))); print(d9[0][:230] if d9 else "no D9 line")
    done(r.returncode == 0 and len(res) == 12 and set(res.values()) == {"PASS"} and bool(d9) and "1 dark, 67 light" in d9[0] and "[68]" in d9[0], "std")
if __name__ == "__main__":
    {"sha": k_sha, "parts": k_parts, "textdiff": k_text, "links": k_links, "charts": k_charts, "contrast": k_contrast, "plan": k_plan, "dcheck": k_dcheck, "arc0": k_arc0, "std": k_std}[sys.argv[1]]()
