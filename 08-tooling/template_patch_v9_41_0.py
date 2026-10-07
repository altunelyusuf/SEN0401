#!/usr/bin/env python3
"""Patches course_page_template_v9_40_0.html into course_page_template_v9_41_0.html.

One subject, the owner's review of 2026-10-07 12:04: the reading area. In his words: "keep the top the most
valuable area and never spend it cheaply"; "use tool tips instead of messages and accordions whenever
possible"; "the lastly added visualizations and interactions are mostly appended not merged with the content";
"there is a hiding content, only randomly clicking displays. Such hidden interaction should never exist";
"some tool tips are long paragraphs, they should be shorter and if there are details we can use the right
branch cards instead".

Measured on the 9.39.0 chapter 1 page, Money > Unit > Satoshi: above the concept's first sentence stood the
sub-tab row, the breadcrumb row, a second row of concept pills, a third row (the concept's name, previous /
next, Show all), the section's own heading, a "Mark as understood" row, the section's one-sentence summary, and
- when "more" had been opened - the section's whole text again; the concept's reading text began mid-screen.
Inside a concept, paragraphs after the first were folded under their lead sentences (an accordion), the
chapter visual sat behind a "Visualise" button (hidden until clicked), the neighbourhood map was appended
under the run panel with a two-line explanation and a zoom hint, and the hover tooltip of a concept carried its
whole first paragraph.

9.41.0:
- The breadcrumb is one row: subject > section (select) > the concept pills, the current one marked, and
  "Show all" while one concept is open. The previous / next / name row is gone (adjacent pills do that).
- A focused concept starts at the top: the section's heading, mark and summary are shown only in the
  section's "Show all" view, and there as one heading and its full text, with no "more" accordion.
- Nothing hides behind a click inside a concept: the paragraphs are all shown (the sub-division is the
  per-concept paging), the chapter visual is shown where it belongs, after the text and before the run panel.
- The neighbourhood map is merged with the text, not appended: on screens wider than 900 px it sits beside the
  paragraphs (text left, map right); on phones it follows them.
- Helpers become tooltips: the map's explanation and the zoom hint are titles on the map and its buttons; each
  pane's introductory note becomes a small (i) floated at the pane's top right, whose tooltip is the note's first
  sentence and whose click opens the full note in the right-hand card.
- The hover tooltip of a concept is its first sentence; the (i) button and the card carry the rest.
- "Mark as understood" is a compact control at the right of the concept's heading, not a row of its own.
"""
__version__ = "9.41.0"

SRC, DST = "course_page_template_v9_40_0.html", "course_page_template_v9_41_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# ---- CSS ---------------------------------------------------------------------------------------------------------
rep("</style>", """/* 9.41.0: the reading area */
.cgrid{display:grid;grid-template-columns:minmax(0,1fr);gap:.4rem .9rem;align-items:start}
@media (min-width:900px){.cgrid{grid-template-columns:minmax(0,3fr) minmax(16rem,2fr)}.cgrid .nbh{position:sticky;top:.3rem}}
.cgrid .ctext>p:first-child{margin-top:0}
.nbh{margin:0 0 .4rem}.nbh .diagram{height:15rem}
section.leaf h4,section.midhead h3{display:flex;align-items:center;gap:.4rem;flex-wrap:wrap}
button.mark{margin-left:auto;font-size:.8rem;padding:.05rem .5rem;border-radius:999px;background:var(--card);color:var(--mute);border:1px solid var(--line);cursor:pointer;font-weight:400}
button.mark[aria-pressed=true]{background:var(--band);color:#1A7F37;border-color:#1A7F37}
.markrow{display:none}
.zbar>.note{display:none}
.cbnav{display:none}
.ptip{font:inherit;background:none;border:0;color:var(--blue);cursor:pointer;padding:0 .2rem;font-size:.85rem;vertical-align:middle}
.pnoterow{float:right;margin:0 0 .2rem .6rem}
</style>""", 1)

# ---- a focused concept starts at the top: no paragraph folds, no visual toggle, the map beside the text ---------
rep("function secVis(n){const v=visHTML(n);return v?'<div class=\"row\"><button class=\"btn g\" data-vistoggle=\"'+n.id+'\">🎨 Visualise</button></div><div id=\"wvp-'+n.id+'\" hidden>'+v+'</div>':''}",
    "function secVis(n){const v=visHTML(n);return v?'<div id=\"wvp-'+n.id+'\" class=\"visinline\">'+v+'</div>':''}", 1)
# the heading carries the compact mark control (lean and rich sections alike); the boot-time row is no longer added
rep("function secHead(n,tag){return '<'+tag+'>'+(n.level<3?ICON[n.level]+' ':'')+'<span data-c=\"'+n.id+'\" class=\"c\">'+esc(n.label)+'</span> <button class=\"info\" data-detail=\"'+n.id+'\" title=\"Show details of '+esc(n.label)+'\" aria-label=\"Show details of '+esc(n.label)+'\">ⓘ</button></'+tag+'>'}",
    "function secHead(n,tag){return '<'+tag+'>'+(n.level<3?ICON[n.level]+' ':'')+'<span data-c=\"'+n.id+'\" class=\"c\">'+esc(n.label)+'</span> <button class=\"info\" data-detail=\"'+n.id+'\" title=\"Show details of '+esc(n.label)+'\" aria-label=\"Show details of '+esc(n.label)+'\">ⓘ</button><button class=\"mark\" data-mark=\"'+n.id+'\" aria-pressed=\"false\" title=\"Mark '+esc(n.label)+' as understood\">☐ Mark as understood</button></'+tag+'>'}", 1)
rep("function richInner(n,tag){return secHead(n,tag)+bodyRich(n)+storychips(n)+chartBox(n)+widget(n)+secVis(n)+'<div class=\"nbh\" data-nbhfor=\"'+n.id+'\"></div>'}",
    "function richInner(n,tag){return secHead(n,tag)+'<div class=\"cgrid\"><div class=\"ctext\">'+bodyHtml(n)+storychips(n)+'</div><div class=\"nbh\" data-nbhfor=\"'+n.id+'\"></div></div>'+secVis(n)+chartBox(n)+widget(n)}", 1)
# the lean section (the boot markup) uses the same heading, so the mark control exists before enrichment too
rep("'\"'+(n.level===3?' data-rich=\"0\"':'')+'><'+tag+'>'+(n.level<3?ICON[n.level]+' ':'')+'<span data-c=\"'+n.id+'\" class=\"c\">'+esc(n.label)+'</span> <button class=\"info\" data-detail=\"'+n.id+'\" title=\"Show details of '+esc(n.label)+'\" aria-label=\"Show details of '+esc(n.label)+'\">ⓘ</button></'+tag+'>'+bodyHtml(n)",
    "'\"'+(n.level===3?' data-rich=\"0\"':'')+'>'+secHead(n,tag)+bodyHtml(n)", 1)
rep("document.querySelectorAll('main section[data-source]').forEach(sec=>{const h=sec.querySelector('h2,h3,h4'),id=sec.dataset.concept;if(h&&id&&byId[id])h.insertAdjacentHTML('afterend','<div class=\"markrow\"><button class=\"btn g mark\" data-mark=\"'+id+'\" aria-pressed=\"false\">☐ Mark as understood</button></div>')});", "", 1)
# the neighbourhood map keeps its wrapper markup but explains itself in a tooltip, not a paragraph
rep("return '<div class=\"nbh\"><div class=\"nbhl\">Neighbourhood: '+esc(n.label)+' with '+k+' related concept'+(k===1?'':'s')+' (solid: is a kind of; brown: operates on; green dashes: mentioned together). Touch a box for its options.</div><div class=\"diagram\"'+(k>8?' style=\"height:18rem\"':'')+'>'+s+'</svg></div></div>'}",
    "return '<div class=\"nbh\" title=\"Neighbourhood of '+esc(n.label)+': '+k+' related concept'+(k===1?'':'s')+'. Solid: is a kind of; brown: operates on; green dashes: mentioned together. Touch a box for its options; wheel or pinch zooms, drag moves.\"><div class=\"diagram small\">'+s+'</svg></div></div>'}", 1)
# the section overview: one heading and its full text, no accordion; hidden while one concept is focused
rep("<details class=\"more\"><summary>'+linkify(firstSentence(m.body),m.id)+'</summary>'+bodyHtml(m)+'</details>'+secVis(m)+'</section>'}",
    "'+bodyHtml(m)+secVis(m)+'</section>'}", 1)
rep("x.querySelectorAll('.cards > section.leaf').forEach(sc=>sc.hidden=!!focus&&sc.dataset.concept!==focus);x.classList.toggle('focused',!!focus)}});",
    "x.querySelectorAll('.cards > section.leaf').forEach(sc=>sc.hidden=!!focus&&sc.dataset.concept!==focus);x.querySelectorAll('section.midhead').forEach(sc=>sc.hidden=!!focus);x.classList.toggle('focused',!!focus)}});", 1)
# the breadcrumb: one row - select, pills, Show all
rep("if(focus){const sib=kids(byId[focus].parent),i=sib.findIndex(x=>x.id===focus);\n  h+='<span class=\"sep\">›</span><span class=\"cb leafcb\">'+ICON[3]+' '+esc(byId[focus].label)+'</span><span class=\"cbnav\">'+(i>0?'<button class=\"btn g\" data-go=\"'+sib[i-1].id+'\" title=\"'+esc(sib[i-1].label)+'\">◀ '+esc(sib[i-1].label)+'</button>':'')+(i<sib.length-1?'<button class=\"btn g\" data-go=\"'+sib[i+1].id+'\" title=\"'+esc(sib[i+1].label)+'\">'+esc(sib[i+1].label)+' ▶</button>':'')+(sib.length>1?'<button class=\"btn g\" data-sub=\"'+byId[focus].parent+'\">Show all '+sib.length+'</button>':'')+'</span>'}",
    "if(focus){const sib=kids(byId[focus].parent);if(sib.length>1)h+='<button class=\"btn g\" data-sub=\"'+byId[focus].parent+'\" title=\"Show every concept of '+esc(byId[byId[focus].parent].label)+' together\">Show all '+sib.length+'</button>'}", 1)
# the pills sit on the same row as the select
rep(".leafpick{display:flex;flex-wrap:wrap;gap:.3rem;margin:.2rem 0 .3rem}", ".leafpick{display:inline-flex;flex-wrap:wrap;gap:.3rem;margin:0 .3rem;vertical-align:middle}", 1)
# the concept hover tooltip: one sentence
rep("tip.textContent=n.label+': '+(n.definition||n.body);tip.hidden=false}", "tip.textContent=n.label+': '+firstSentence(n.definition||n.body);tip.hidden=false}", 1)
# pane notes become (i) tooltips with the full note in the card: a pass over the built panes
rep("panes.innerHTML=P;",
    "panes.innerHTML=P;panes.querySelectorAll('[data-pane] > h2').forEach(h=>{const notes=[];let e=h.nextElementSibling;while(e&&(e.matches('p.note')||e.matches('p.legend'))){if(e.matches('p.note'))notes.push(e);e=e.nextElementSibling}if(!notes.length)return;const full=notes.map(p=>p.innerHTML).join('</p><p>'),lead=firstSentence(notes[0].textContent);const first=notes[0];first.insertAdjacentHTML('beforebegin','<div class=\"pnoterow\"><button class=\"ptip\" data-tip=\"'+esc(lead)+'\" data-notecard=\"'+esc(h.textContent.trim())+'\" aria-label=\"About this view\" title=\"'+esc(lead)+'\">ⓘ about this view</button></div>');notes.forEach(p=>p.remove());h.dataset.note=full});"
    "panes.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('button[data-notecard]');if(!b)return;const h=b.closest('[data-pane]').querySelector('h2'),c=document.getElementById('card');c.hidden=false;c.innerHTML='<button class=\"close\" data-close title=\"Close (Esc)\" aria-label=\"Close\">\\u2715</button><h3>'+esc(b.dataset.notecard)+'</h3><p>'+h.dataset.note+'</p>';c.classList.add('open')});", 1)


# the neighbourhood map is drawn for the side column now: a squarer, denser viewBox and a box that keeps its aspect
rep("const k=others.length,ring=Math.min(k,8),W=560,H=k>8?290:200,cx=W/2,cy=H/2;", "const k=others.length,ring=Math.min(k,8),W=440,H=k>8?330:250,cx=W/2,cy=H/2;", 1)
rep("const r=i<8?(k>8?70:78):118,a=-Math.PI/2+(i%8)*(2*Math.PI/ring)+(i>=8?Math.PI/8:0);pos[o.id]=[cx+r*2.1*Math.cos(a),cy+r*Math.sin(a)]", "const r=i<8?(k>8?82:92):140,a=-Math.PI/2+(i%8)*(2*Math.PI/ring)+(i>=8?Math.PI/8:0);pos[o.id]=[cx+r*1.45*Math.cos(a),cy+r*Math.sin(a)]", 1)
rep("const box=(id,cls)=>{const p=pos[id],lab=byId[id].label,w=Math.min(150,Math.max(60,lab.length*6.4+14));", "const box=(id,cls)=>{const p=pos[id],lab=byId[id].label,w=Math.min(126,Math.max(54,Math.min(lab.length,18)*6.6+12));", 1)
rep("esc(lab.length>23?lab.slice(0,22)+'\\u2026':lab)", "esc(lab.length>19?lab.slice(0,18)+'\\u2026':lab)", 1)
rep(".nbh .diagram{background:var(--panel);border:1px solid var(--line);border-radius:8px;height:13rem;min-height:9rem;resize:vertical;overflow:hidden}", ".nbh .diagram{background:var(--panel);border:1px solid var(--line);border-radius:8px;height:16rem;min-height:9rem;resize:vertical;overflow:hidden}", 1)
rep(".nbh{margin:0 0 .4rem}.nbh .diagram{height:15rem}", ".nbh{margin:0 0 .4rem}", 1)
rep(".nbh svg text{font:12px Calibri,Arial,sans-serif;fill:var(--ink)}", ".nbh svg text{font:13px Calibri,Arial,sans-serif;fill:var(--ink)}", 1)

# the 9.7.0 pass that folded a pane's legend and note into an "About" accordion is retired: the note is the (i) above, the
# legend stays as its one visible line
rep("if(p.dataset.pane==='agents'||byId[p.dataset.pane])return;const h=p.querySelector(':scope > h2');if(!h)return;const ns=[];let n=h.nextElementSibling;while(n&&n.matches('p.note,p.legend')){ns.push(n);n=n.nextElementSibling}if(ns.length){const d=document.createElement('details');d.className='help';d.innerHTML='<summary title=\"About this view\">ⓘ About</summary>';ns[0].replaceWith(d);ns.forEach(x=>d.appendChild(x))}});", "});", 1)
# a visual shown on reveal is also RUN on reveal (the toggle used to run it)
rep("sc.dataset.rich='1';sc.innerHTML=richInner(byId[sc.dataset.concept],'h4')});",
    "sc.dataset.rich='1';sc.innerHTML=richInner(byId[sc.dataset.concept],'h4')});(root||panes).querySelectorAll('.visinline:not([data-run])').forEach(vi=>{const sc=vi.closest('section'),sp=sc&&sc.closest('[data-subpane]');if(!sc||(sp&&sp.hidden)||sc.hidden)return;vi.dataset.run='1';const id=sc.dataset.concept,v=D.visuals[id];if(v&&v.kind==='branchflow'&&document.getElementById('wv-'+id+'-src'))document.getElementById('wv-'+id+'-src').textContent=v.program;try{visRun(id)}catch(e){console.error(e)}});", 1)
rep("<!-- course_page_template version 9.40.0:",
    "<!-- course_page_template version 9.41.0: the reading area - a focused concept starts at the top (one breadcrumb row, "
    "the section's overview only in Show all), nothing hidden behind a click inside a concept (no paragraph folds, the "
    "visual shown, the map beside the text on wide screens), helpers as tooltips (map, zoom bar, pane notes as an (i) "
    "whose click opens the card), one-sentence hover tooltips, a compact mark control in the heading. Earlier: "
    "--><!-- course_page_template version 9.40.0:", 1)
open(DST, "w").write(t)
assert "bodyRich(" not in t.replace("function bodyRich(", ""), "bodyRich still used"
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
