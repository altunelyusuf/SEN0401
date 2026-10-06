#!/usr/bin/env python3
"""Patches course_page_template_v9_32_0.html into course_page_template_v9_33_0.html.

One subject, the owner's two-fold rule of 2026-10-06 13:42: the decks and the pages carry ONE
look-and-feel, "to support the teachability, adaptation, and fire the remembering of the
students". The deck side already exists - the CME materials look-and-feel v1.0.0
(cme/00-standards/CME_MaterialsLookAndFeel_v1_0_0.md), shipped on all ten chapter decks. This
patch brings the page side onto the same standard, in two measured moves:

1. THE WARM-IVORY TOKENS. The template's Python-flavoured palette (white page, navy header,
   #FFD43B yellow, cool greys) becomes the deck palette: page #FAF6EF, ink #2B2622, orange
   accent #D97A14, slate #2F6D62 for the teaching accent the blue used to carry, card #F2ECE1,
   band #EFE6D6, rule #DFD6C7, mute #6E655C, code panels #23272E with #E6EDF3 text and the
   #7EE787 result green the page already shared with the decks. The --yellow variable KEEPS ITS
   NAME and now holds the orange, because 19 var() sites and drawn SVG read it; renaming was
   measured as a wider, riskier diff for zero behaviour. Every companion hardcoded colour is
   re-derived, not blanket-replaced: text-on-accent pairs move to ink-on-orange (4.8:1), the
   yellow-dark strokes and legend inks (#B08900, #8A6A00, #7A5F00, #8A5A00) become the orange-
   browns #9A5A10/#7A4A10 (6.0:1+ on the ivory family), the cool washes (#EEF3F8, #FFF6DB,
   #DCE6F0) become warm ones, the editor chrome moves from GitHub navy (#0F1720/#2B3A4B) to the
   deck's neutral darks (#1B1E24/#3A3F47), and the editor's syntax tokens adopt the deck's code
   colours where the deck defines one: keywords #F2A860 bold, strings #9ECBFF, numbers #FFD28A,
   comments #8FA98F italic (builtins, f-strings and decorators keep their old hues - the deck
   defines none for them). Alpha highlights follow the accent (#FFD43B55 -> #D97A1440 etc.).
   Every swap below asserts its expected occurrence count, so a drifted template refuses the
   patch instead of half-applying it.

2. THE DECK'S STORY LAYER AND MOTIFS. The chapter's 5N1K story companion (already the deck's
   backbone) joins Learn as a Stories tab, shown only when the page data carries stories
   (sen0401_page_data_v2_7_0.py embeds them with the companion's own run_checks() as the gate).
   Each story is drawn with the deck slide's own motifs, as CSS the rest of the page can reuse:
   the date CHIP (orange, ink text), the WHO / WHERE / WHEN / READ fact row (band-coloured
   chips, READ a live link), the photograph strip with its credit line under every picture
   (licences from ASSETS_PROVENANCE, carried in the data), the story paragraph, the lesson as
   a TAKEAWAY STRIP (band background, orange left bar, bold line), the source line, and
   On-the-page jump buttons for the concepts the story touches - the existing .jump/data-go
   machinery, so a story click changes the main area and leaves the detail card closed, exactly
   as the owner's menu rule demands.

Checked after writing: the patched template still carries no dark-mode rule (the light-theme
gate), all replaced counts matched, and the new pane builder sits between the lecture and
resources builders so pane order stays Learn-first.

Usage: python3 template_patch_v9_33_0.py
"""
__version__ = "9.33.0"
import re

SRC, DST = "course_page_template_v9_32_0.html", "course_page_template_v9_33_0.html"
t = open(SRC).read()
n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# ---- 1. the warm-ivory tokens -----------------------------------------------------------------------------------
rep(":root{color-scheme:light;--ink:#1F2933;--mute:#5B6B7B;--navy:#1E2A3A;--blue:#306998;--yellow:#FFD43B;"
    "--card:#F1F4F8;--line:#D0D7DE;--code:#17202B;--ok:#1A7F37;--bad:#B42318;--bg:#FFFFFF;--panel:#FAFBFC;",
    ":root{color-scheme:light;--ink:#2B2622;--mute:#6E655C;--navy:#2B2622;--blue:#2F6D62;--yellow:#D97A14;"
    "--card:#F2ECE1;--line:#DFD6C7;--code:#23272E;--ok:#1A7F37;--bad:#B42318;--bg:#FAF6EF;--panel:#F6F0E3;--band:#EFE6D6;")

# the alpha accents first, so the plain #FFD43B swap cannot eat them
rep("#FFD43B55", "#D97A1440", 5)
rep("#FFD43B33", "#D97A1426", 3)
rep("#FFD43B66", "#D97A1450", 1)   # --tamb, the .nv ambiguity tint
rep("#FFD43BAA", "#D97A14AA", 1)
rep("#FFD43B", "#D97A14", 10)      # remaining accent fills/strokes, the drawn graphs' level-3 node fill among them

# old ink and navy hardcodes (text-on-accent pairs land on ink-on-orange, 4.8:1)
rep("#1F2933", "#2B2622", 13)
rep("#1E2A3A", "#2B2622", 7)
rep("#C9D4E0", "#D8CFC2", 1)       # header subtitle on the warm dark bar, 9.7:1

# yellow-dark strokes and inks -> orange-browns measured on the ivory family
rep("#B08900", "#9A5A10", 10)
rep("#8A6A00", "#9A5A10", 3)
rep("#8A5A00", "#7A4A10", 2)
rep("#7A5F00", "#7A4A10", 2)
rep("#5A3A00", "#5A3A10", 1)
rep("#7A4F00", "#7A4A10", 2)      # --amb, and a reference-graph scenario colour

# cool washes -> warm washes
rep("#FFF6DB", "#F7E8CE", 2)
rep("#EEF3F8", "#F0E8D8", 1)       # .tk inline-token background
rep("#1B3A57", "#235A50", 1)       # .tk text: navy -> dark slate, 6.5:1 on the warm wash
rep("#DCE6F0", "#DDD5C8", 2)
rep("--tint:#30699820", "--tint:#2F6D6220", 1)
rep("#306998", "#2F6D62", 6)       # the drawn graphs and the exam PDF: python blue -> the deck slate
rep("#5B6B7B", "#6E655C", 4)       # the exam PDF's muted text: the old mute, warm now
rep(".bits .man{background:#79B8FF33}", ".bits .man{background:#2F6D6233}", 1)

# editor chrome: GitHub navy -> the deck's neutral darks
rep("#0F1720", "#1B1E24", 3)
rep("#2B3A4B", "#3A3F47", 4)
rep("#3B4D61", "#4A5058", 2)
rep("#1B2836", "#2A2E36", 1)
rep("#2A4A73", "#3A5A54", 1)       # autocomplete selection: slate dark
rep("#B7C6D6", "#C9C4BC", 1)
rep("#8896A5", "#A89C8C", 3)       # input borders and the concept map's is-a-kind-of line, warm

# editor syntax tokens -> the deck's code colours (comments split from the gutter grey first)
rep(".edhl .hc{color:#93A6B9;font-style:italic}", ".edhl .hc{color:#8FA98F;font-style:italic}", 1)
rep("#93A6B9", "#8E959E", 1)       # the remaining one: the line-number gutter
rep(".edhl .hk{color:#FF8B84}", ".edhl .hk{color:#F2A860;font-weight:700}", 1)
rep(".edhl .hs{color:#A8DDA8}", ".edhl .hs{color:#9ECBFF}", 1)
rep(".edhl .hn{color:#FFD07A}", ".edhl .hn{color:#FFD28A}", 1)

# ---- 2. the deck motifs and the Stories pane --------------------------------------------------------------------
rep("</style>", """/* 9.33.0: the CME materials look-and-feel v1.0.0 - the deck's motifs as page CSS */
.story{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.8rem .95rem;margin:.7rem 0;max-width:46rem}
.story h3{margin:.1rem 0 .4rem;font-family:Cambria,Georgia,serif}
.story .swhen{display:inline-block;background:var(--yellow);color:#2B2622;font-weight:700;border-radius:999px;padding:.05rem .6rem;font-size:.85rem;margin-right:.45rem;vertical-align:.08em}
.factrow{display:flex;flex-wrap:wrap;gap:.35rem;margin:.45rem 0}
.factrow .fr{background:var(--band);border:1px solid var(--line);border-radius:7px;padding:.15rem .5rem;font-size:.85rem;color:var(--ink)}
.factrow .fr b{color:#7A4A10;margin-right:.3rem}
.factrow a.fr{text-decoration:underline}
.takeaway{background:var(--band);border-left:4px solid var(--yellow);border-radius:0 8px 8px 0;padding:.4rem .7rem;margin:.5rem 0;font-weight:700}
.simgrow{display:flex;flex-wrap:wrap;gap:.6rem;margin:.5rem 0}
.simgrow figure{margin:0;flex:1 1 10rem;max-width:22rem}
.simgrow img{width:100%;height:auto;border-radius:8px;border:1px solid var(--line);display:block}
.simgrow figcaption{font-size:.85rem;color:var(--mute);margin-top:.15rem}
.story .ssrc{font-size:.85rem;color:var(--mute);margin:.45rem 0 0}
</style>""", 1)

rep("GROUPS={learn:[...(D.lecture&&D.lecture.length?[['lecture','\U0001F393 Lecture']]:[]),",
    "GROUPS={learn:[...(D.lecture&&D.lecture.length?[['lecture','\U0001F393 Lecture']]:[]),"
    "...(D.stories&&D.stories.length?[['stories','\U0001F4DC Stories']]:[]),", 1)

STORIES_PANE = ("if(D.stories&&D.stories.length)P+='<div role=\"tabpanel\" data-pane=\"stories\" hidden>'+subbar('learn')"
 "+'<h2>\U0001F4DC Stories from the record</h2><p class=\"note\">The dated, sourced stories the chapter deck tells, "
 "with the same photographs and credits. Every story names who, where and when, links where to read on, and ends with "
 "its lesson; the buttons jump to the concepts it touches.</p>'"
 "+D.stories.map((s,si)=>'<article class=\"story\" id=\"story-'+s.id+'\"><h3><span class=\"swhen\">'+esc(s.when)+'</span>'+esc(s.title)+'</h3>'"
 "+(s.imgs&&s.imgs.length?'<div class=\"simgrow\">'+s.imgs.map((im,j)=>'<figure><img data-simg=\"'+si+','+j+'\" width=\"'+im.w+'\" height=\"'+im.h+'\" alt=\"'+esc(im.credit)+'\" loading=\"lazy\"><figcaption>'+esc(im.credit)+'</figcaption></figure>').join('')+'</div>':'')"
 "+'<div class=\"factrow\"><span class=\"fr\"><b>WHO</b>'+esc(s.who)+'</span><span class=\"fr\"><b>WHERE</b>'+esc(s.where)+'</span>"
 "<span class=\"fr\"><b>WHEN</b>'+esc(s.when)+'</span><a class=\"fr\" href=\"'+esc(s.link)+'\" target=\"_blank\" rel=\"noopener\"><b>READ</b>'+esc(s.link.replace(/^https?:\\/\\//,''))+'</a></div>'"
 "+'<p>'+esc(s.story)+'</p><p class=\"takeaway\">'+esc(s.lesson)+'</p><p class=\"ssrc\">Source: '+esc(s.source)+'</p>'"
 "+(s.concepts&&s.concepts.some(c=>byId[c])?'<p class=\"lact\">'+s.concepts.filter(c=>byId[c]).map(c=>'<button class=\"jump\" data-go=\"'+c+'\">On the page: '+esc(byId[c].label)+'</button>').join(' ')+'</p>':'')"
 "+'</article>').join('')+'</div>'; ")
rep("'</div></div>';\nif(D.resources&&D.resources.length){const RKLAB",
    "'</div></div>';\n" + STORIES_PANE + "\nif(D.resources&&D.resources.length){const RKLAB", 1)
# the photographs' bytes are assigned AFTER the single innerHTML parse: a megabyte of base64 inside attribute
# values makes the parser's one task long (measured 1171 ms on the first build of this patch); as src
# assignments the strings never pass through the HTML tokenizer and the image decode is asynchronous anyway
rep("panes.innerHTML=P",
    "panes.innerHTML=P;if(D.stories&&D.stories.length)document.querySelectorAll('#panes [data-simg]').forEach(el=>{const [i,j]=el.dataset.simg.split(',');el.src=D.stories[+i].imgs[+j].data})", 1)

# ---- the version-comment chain ----------------------------------------------------------------------------------
rep("<!-- course_page_template version 9.32.0:",
    "<!-- course_page_template version 9.33.0: the CME materials look-and-feel v1.0.0, two-fold with the chapter "
    "decks - the warm-ivory deck tokens (page #FAF6EF, ink #2B2622, orange #D97A14, slate #2F6D62, dark code panels "
    "#23272E with #7EE787 results) restyle every pane with measured AA contrast, the editor's syntax colours adopt "
    "the deck's code colours, and the deck's 5N1K story layer joins Learn as a Stories tab: date chip, photographs "
    "with credits, the WHO/WHERE/WHEN/READ fact row with a live link, the story, its lesson as a takeaway strip, "
    "the source line, and On-the-page jumps that leave the detail card closed. Earlier: -->"
    "<!-- course_page_template version 9.32.0:", 1)

open(DST, "w").write(t)
assert "prefers-color-scheme: dark" not in t and "prefers-color-scheme:dark" not in t
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
