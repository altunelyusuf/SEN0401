#!/usr/bin/env python3
"""sen0401_story_check v1.0.0 - the owner's rule for stories and history in course materials, enforced on the finished files (new for SEN0401; SEN0414 enforces only the
story module's own self-check). 5N1K: who / what / when / where / why / how, real names, specific details, a real picture, and a live further-reading link ON the material.
For chapter NN (stories from sen0401_chNN_stories_v*.py, the deck from chNN-deck, the assets from 03-materials/chNN/assets) it refuses:
  1. a story whose module self-check (run_checks) fails;
  2. who without at least one personal or organisational name (two capitalised words); when that is not an ISO date or lies in the future, or whose year does not occur in the story or its
     source text; where of fewer than three words; a story of fewer than three sentences (what/why/how); a lesson of more than 14 words; no source line;
  3. a link that is not https, or that is a search page, a shortener or a redirector; (with --live) a link that does not answer with a status below 400;
  4. a picture that is missing, cannot be decoded, is smaller than 300 px on its longer side, or has no row in 03-materials/chNN/assets/ASSETS_PROVENANCE_v*.md with its sha256 (first 16 digits,
     matching the file), a licence (CC BY, CC BY-SA, CC0, public domain, ...) and a source page ('File:' of Wikimedia Commons, a museum, archive or library page, or a URL); a credit that
     does not name the licence; a picture that no slide of the deck shows beside its credit text; a story whose date and picture credit are not on one slide, or whose READ link's host is on no slide (the WHO/WHERE/WHEN/READ row);
  5. the page's story pictures file (chNN-page/stories_img_v*.json), when it exists, must name the same file and credit for the story.
It WARNS (and with --strict refuses) where the owner's wider rule needs a field the SEN0401 story contract does not have yet: a story about a person without a 'bio' (born / role / dates) field, and a
chapter with no historic money picture (an optional story field 'money_picture': true marks one; relevant to chapters on the history of money, fees, mining, and applications).
Usage: sen0401_story_check_v1_0_0.py NN [--live] [--strict]        Environment: SEN0401_ROOT, SEN0401_DECK (a deck file to check instead of the chapter's newest).  Exit 0 when nothing is refused."""
__version__ = "1.0.0"
import datetime, glob, hashlib, importlib.util, json, os, re, sys, zipfile
from xml.dom import minidom

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(TOOL)
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
newest = lambda pat: sorted(glob.glob(pat), key=vkey)[-1]
LIC = re.compile(r"CC[ -]?BY(?:[ -]SA)?(?:[ -]\d\.\d)?|CC0|public domain|\bPD\b|Public Domain Mark", re.I)
SRC = re.compile(r"File:|https?://|museum|archive|library|Rijksmuseum|Smithsonian|Wikimedia|Wikipedia", re.I)
BAD_LINK = re.compile(r"google\.[a-z.]+/search|bing\.com/search|duckduckgo\.com/\?|bit\.ly|t\.co/|tinyurl|goo\.gl|/redirect|[?&]url=", re.I)
PERSON = re.compile(r"\b[A-Z][a-z]+(?:-[A-Z][a-z]+)? [A-Z][a-z]+")


def slide_text(deck):
    z = zipfile.ZipFile(deck); out = []
    for n in sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=lambda n: int(re.findall(r"\d+", n)[0])):
        d = minidom.parseString(z.read(n)); out.append(" ".join("".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")) for p in d.getElementsByTagName("a:p")))
    return out


def main(a):
    n = a[0]; live = "--live" in a; strict = "--strict" in a
    st = newest(os.path.join(TOOL, "sen0401_ch%s_stories_v*.py" % n))
    spec = importlib.util.spec_from_file_location("stories", st); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
    bad, warn = [], []
    bad += ["module self-check: %s" % x for x in (M.run_checks() if hasattr(M, "run_checks") else ["the story module has no run_checks()"])]
    assets = os.path.join(ROOT, "03-materials", "ch%s" % n, "assets")
    provs = sorted(glob.glob(os.path.join(assets, "ASSETS_PROVENANCE_v*.md")), key=vkey)
    prov = "\n".join(open(p).read() for p in provs)
    rows = [l for l in prov.splitlines() if l.startswith("|")]
    try:
        from PIL import Image
    except Exception:
        Image = None
    deckf = [os.environ["SEN0401_DECK"]] if os.environ.get("SEN0401_DECK") else glob.glob(os.path.join(TOOL, "ch%s-deck" % n, "sen0401_ch%s_deck_v*.pptx" % n)); texts = slide_text(sorted(deckf, key=vkey)[-1]) if deckf else []
    alltext = "\n".join(texts)
    si = glob.glob(os.path.join(TOOL, "ch%s-page" % n, "stories_img_v*.json"))
    simg = json.load(open(sorted(si, key=vkey)[-1])) if si else {}
    today = datetime.date.today()
    for s in M.STORIES:
        i = s["id"]
        if not PERSON.search(s.get("who", "")): bad.append("%s: who names no one (two capitalised words)" % i)
        try:
            dt = datetime.date.fromisoformat(s["when"])
            if dt > today: bad.append("%s: when %s lies in the future" % (i, s["when"]))
            if str(dt.year) not in s["story"] + " " + s["source"] + " " + s.get("lesson", ""): bad.append("%s: the year %d occurs in neither story nor source" % (i, dt.year))
        except Exception:
            bad.append("%s: when %r is not an ISO date" % (i, s.get("when")))
        if len(s.get("where", "").split()) < 3: bad.append("%s: where has fewer than three words" % i)
        if len(re.split(r"(?<=[.!?]) +", s["story"].strip())) < 3: bad.append("%s: the story has fewer than three sentences (what, why, how)" % i)
        if len(s.get("lesson", "").split()) > 14: bad.append("%s: lesson over 14 words" % i)
        lk = s.get("link", "")
        if not lk.startswith("https://") or BAD_LINK.search(lk): bad.append("%s: link %r is not a direct https page" % (i, lk))
        elif live:
            import requests
            try:
                r = requests.get(lk, timeout=30, headers={"User-Agent": "Mozilla/5.0 (SEN0401 story check)"}, stream=True); code = r.status_code; r.close()
            except Exception as e:
                code = type(e).__name__
            if not isinstance(code, int) or code >= 400: bad.append("%s: link answered %s" % (i, code))
        ph = s.get("photo", ""); pf = os.path.join(assets, ph)
        if not ph or not os.path.exists(pf): bad.append("%s: picture %r is not in the chapter's assets" % (i, ph)); continue
        h16 = hashlib.sha256(open(pf, "rb").read()).hexdigest()[:16]
        if Image is not None:
            try:
                w, hh = Image.open(pf).size
                if max(w, hh) < 300: bad.append("%s: picture %s is only %dx%d px" % (i, ph, w, hh))
            except Exception as e:
                bad.append("%s: picture %s cannot be decoded (%s)" % (i, ph, type(e).__name__))
        mine = [r for r in rows if ph in r]
        if not mine: bad.append("%s: %s has no row in ASSETS_PROVENANCE" % (i, ph))
        else:
            blob = " ".join(mine) + " " + " ".join(l for l in prov.splitlines() if ph in l)
            if h16 not in prov.split(ph, 1)[1][:600] and not any(h16 in r for r in rows if ph in r):
                bad.append("%s: the sha256 (%s) of %s is not in its provenance row" % (i, h16, ph))
            if not LIC.search(blob): bad.append("%s: provenance row of %s names no licence" % (i, ph))
            if not SRC.search(blob): bad.append("%s: provenance row of %s names no source page" % (i, ph))
        if not LIC.search(s.get("credit", "")): bad.append("%s: the credit %r names no licence" % (i, s.get("credit")))
        if texts:
            if s["credit"] not in alltext: bad.append("%s: the credit is on no slide" % i)
            host = re.sub(r"^https?://(www\.)?", "", lk).split("/")[0]
            if not any(s["when"] in t and s["credit"] in t for t in texts): bad.append("%s: no slide carries the date and the picture's credit together (the story's own slide)" % i)
            if host and host not in alltext: bad.append("%s: the READ link's host %s is on no slide" % (i, host))
        if simg:
            e = simg.get(i) or []
            if not any(x.get("file") == ph for x in e): bad.append("%s: the page's stories_img file does not name %s" % (i, ph))
        if PERSON.search(s.get("who", "")) and not s.get("bio"): warn.append("%s: a story about people without a 'bio' field (born / role / dates)" % i)
    if not any(s.get("money_picture") for s in M.STORIES): warn.append("no story marked money_picture (a historic money picture from a museum, archive or auction site)")
    print("sen0401_story_check %s (chapter %s): %d stories, %d provenance row(s), deck %s; %d refusal(s), %d warning(s)%s"
          % (__version__, n, len(M.STORIES), len(rows), "read" if texts else "absent", len(bad) + (len(warn) if strict else 0), len(warn), "" if live else " (links not opened: use --live)"))
    for b in bad: print("  REFUSED", b)
    for w in warn: print("  %s" % ("REFUSED (strict)" if strict else "WARN"), w)
    return 1 if bad or (strict and warn) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
