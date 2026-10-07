#!/usr/bin/env python3
"""Patches course_page_template_v9_33_0.html into course_page_template_v9_34_0.html.

One subject: the Learn sections, after the owner's review of the chapter 1 page 9.37.0 (2026-10-07 00:09):
"rich in content ... but lacks visualizations and interactions in the learn sections. Additionally the long
explanations cannot fit into single page, we need a mechanism to sub-divide the sub-pages and provide direct
access to them."

Measured first, on the chapter 1 page: a concept section is a heading, five unlabelled paragraphs of about 90
words each, a run widget for 42 of the 90 concepts and a drawn visual for 5 of them; a section of the chapter
(a level-2 subject) stacks every one of its concepts, so "Money > Units" is four such blocks in one scroll.
Nothing is invented to fill the gap: every addition below is drawn from data the page already carries.

1. SUB-DIVISION WITH DIRECT ACCESS. (a) Under the breadcrumb of every subject, a row of concept pills - one
   per concept of the chosen section - jumps straight to that concept and marks the one in view; the existing
   focus mode (one concept at a time, previous / next, "Show all") is what a pill opens, so the explorer, the
   breadcrumb and the pills stay synchronized through the same goTo(). (b) Inside a concept, paragraphs after
   the first fold under their own lead sentence (the sentence is the summary, the fold holds the rest, nothing
   is repeated), so a long explanation reads as a short page of openable parts; the text stays whole in the
   DOM for the agents and the search.

2. VISUALIZATION AND INTERACTION ON EVERY CONCEPT. (a) A facts strip in the deck's fact-row motif: WHERE the
   concept sits (subject > section), WHO explains it (its subject agent), its executed example when it has one.
   (b) A neighbourhood map - a small zoomable SVG of the concept with its parent and every concept the
   ontology or the document relates it to (is a kind of, operates on, mentions, in both directions), each node
   a button that opens the detail card (touching a concept shows its options first) - built from D.relations,
   which already carry their evidence. (c) The worked example as a labelled card (the example and its
   definition from the chapter ABox), which the section never showed. (d) Story chips: every story of the
   companion that names the concept, jumping to its card in the Stories tab.

Usage: python3 template_patch_v9_34_0.py
"""
__version__ = "9.34.0"

SRC, DST = "course_page_template_v9_33_0.html", "course_page_template_v9_34_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# ---- CSS --------------------------------------------------------------------------------------------------------
rep("</style>", """/* 9.34.0: the Learn sections - concept pills, paragraph folds, facts strip, neighbourhood map, example card, story chips */
.leafpick{display:flex;flex-wrap:wrap;gap:.3rem;margin:.35rem 0 .5rem}
.leafpick button{font:inherit;font-size:.85rem;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:.12rem .6rem;cursor:pointer}
.leafpick button[aria-current=true]{background:var(--yellow);border-color:#9A5A10;font-weight:700}
details.para{margin:.25rem 0 .4rem}details.para>summary{cursor:pointer;color:var(--ink)}details.para>summary::marker{color:var(--yellow)}details.para>.bp{margin-top:.3rem}
.cfacts{margin:.3rem 0 .5rem}
.nbh{margin:.5rem 0}.nbh .nbhl{font-size:.85rem;color:var(--mute);margin-bottom:.2rem}
.nbh .diagram{background:var(--panel);border:1px solid var(--line);border-radius:8px;height:13rem;min-height:9rem;resize:vertical;overflow:hidden}
.nbh svg text{font:12px Calibri,Arial,sans-serif;fill:var(--ink)}.nbh svg .nbc{cursor:pointer}.nbh svg .nbc rect{fill:var(--card);stroke:var(--blue);stroke-width:1.2;rx:7}.nbh svg .nbc.me rect{fill:var(--yellow);stroke:#9A5A10;stroke-width:1.6}.nbh svg .nbc.up rect{fill:var(--band)}
.nbh svg .nbe{stroke:#A89C8C;stroke-width:1.3}.nbh svg .nbe.op{stroke:#9A5A10;stroke-width:2}.nbh svg .nbe.me{stroke:#1A7F37;stroke-dasharray:5 4;stroke-width:1.6}
.excard{background:var(--band);border-left:4px solid var(--blue);border-radius:0 8px 8px 0;padding:.45rem .7rem;margin:.5rem 0}.excard b{color:#235A50}
.storychips{display:flex;flex-wrap:wrap;gap:.3rem;margin:.4rem 0}.storychips button{font:inherit;font-size:.85rem;background:var(--band);border:1px solid var(--line);border-radius:7px;padding:.12rem .55rem;cursor:pointer;color:var(--ink)}
</style>""", 1)

# ---- 1b. paragraph folds in a concept's body ---------------------------------------------------------------------
rep("function bodyHtml(n){const ps=n.paras&&n.paras.length?n.paras:[{facet:'',text:n.body}];return ps.map(p=>'<p class=\"bp\">'+(p.facet?'<b class=\"facet\">'+esc(p.facet)+'.</b> ':'')+linkify(p.text,n.id)+'</p>').join('')}",
    "function bodyHtml(n){const ps=n.paras&&n.paras.length?n.paras:[{facet:'',text:n.body}];return ps.map(p=>'<p class=\"bp\">'+(p.facet?'<b class=\"facet\">'+esc(p.facet)+'.</b> ':'')+linkify(p.text,n.id)+'</p>').join('')}"
    " function bodyRich(n){const ps=n.paras&&n.paras.length?n.paras:[{facet:'',text:n.body}];const para=p=>'<p class=\"bp\">'+(p.facet?'<b class=\"facet\">'+esc(p.facet)+'.</b> ':'')+linkify(p.text,n.id)+'</p>';"
    "if(ps.length<2)return ps.map(para).join('');"
    "return para(ps[0])+ps.slice(1).map(p=>{const lead=firstSentence(p.text),rest=p.text.slice(lead.length).trim();"
    "if(!rest||p.facet)return para(p);"
    "return '<details class=\"para\"><summary>'+esc(lead)+'</summary> <p class=\"bp\">'+linkify(rest,n.id)+'</p></details>'}).join('')}", 1)

# ---- 2. the concept's facts strip, neighbourhood map, example card and story chips --------------------------------
rep("function sec(n,tag){return ",
    "function agentOf(id){return D.agents.find(a=>a.covers.indexOf(id)>=0)}"
    " function cfacts(n){const p=n.parent?byId[n.parent]:null,tp=byId[topOf(n.id)],ag=agentOf(n.id),nr=rel(n.id).length;"
    "return '<div class=\"factrow cfacts\"><span class=\"fr\"><b>WHERE</b>'+esc(tp.label)+(p&&p.id!==tp.id?' \\u203a '+esc(p.label):'')+'</span>'"
    "+(ag?'<span class=\"fr\"><b>WHO</b>'+esc(ag.name)+'</span>':'')"
    "+(n.io?'<span class=\"fr\"><b>RUN</b>'+esc(n.io.code)+' \\u2192 '+esc(n.io.out)+'</span>':'')"
    "+(nr?'<span class=\"fr\"><b>LINKS</b>'+nr+' related concept'+(nr===1?'':'s')+'</span>':'')+'</div>'}"
    " function nbhSvg(n){const R=rel(n.id),seen=new Set([n.id]),others=[];"
    "if(n.parent&&!seen.has(n.parent)){seen.add(n.parent);others.push({id:n.parent,kind:'up',type:'is a kind of'})}"
    "R.forEach(r=>{const o=r.source===n.id?r.target:r.source;if(seen.has(o)||!byId[o])return;seen.add(o);others.push({id:o,kind:'rel',type:r.type,out:r.source===n.id})});"
    "if(!others.length)return '';const k=others.length,ring=Math.min(k,8),W=560,H=k>8?290:200,cx=W/2,cy=H/2;"
    "const pos={};pos[n.id]=[cx,cy];others.forEach((o,i)=>{const r=i<8?(k>8?70:78):118,a=-Math.PI/2+(i%8)*(2*Math.PI/ring)+(i>=8?Math.PI/8:0);pos[o.id]=[cx+r*2.1*Math.cos(a),cy+r*Math.sin(a)]});"
    "const box=(id,cls)=>{const p=pos[id],lab=byId[id].label,w=Math.min(150,Math.max(60,lab.length*6.4+14));return '<g class=\"nbc '+cls+'\" data-nbh=\"'+id+'\" role=\"button\" tabindex=\"0\" aria-label=\"Options for '+esc(lab)+'\"><rect x=\"'+(p[0]-w/2)+'\" y=\"'+(p[1]-11)+'\" width=\"'+w+'\" height=\"22\"/><text x=\"'+p[0]+'\" y=\"'+(p[1]+4)+'\" text-anchor=\"middle\">'+esc(lab.length>23?lab.slice(0,22)+'\\u2026':lab)+'</text></g>'};"
    "let s='<svg viewBox=\"0 0 '+W+' '+H+'\" role=\"img\" aria-label=\"Neighbourhood of '+esc(n.label)+'\">';"
    "others.forEach(o=>{const a=pos[n.id],b=pos[o.id];const cls=o.type==='operates on'?'op':(o.type==='mentions'?'me':'');s+='<line class=\"nbe '+cls+'\" x1=\"'+a[0]+'\" y1=\"'+a[1]+'\" x2=\"'+b[0]+'\" y2=\"'+b[1]+'\"><title>'+esc((o.out||o.kind==='up'?n.label:byId[o.id].label)+' '+o.type+' '+(o.out||o.kind==='up'?byId[o.id].label:n.label))+'</title></line>'});"
    "others.forEach(o=>{s+=box(o.id,o.kind)});s+=box(n.id,'me');"
    "return '<div class=\"nbh\"><div class=\"nbhl\">Neighbourhood: '+esc(n.label)+' with '+k+' related concept'+(k===1?'':'s')+' (solid: is a kind of; brown: operates on; green dashes: mentioned together). Touch a box for its options.</div><div class=\"diagram\"'+(k>8?' style=\"height:18rem\"':'')+'>'+s+'</svg></div></div>'}"
    " function excard(n){return n.example?'<div class=\"excard\"><b>Worked example.</b> '+esc(n.example)+(n.definition?' <span class=\"note\">'+esc(n.definition)+'</span>':'')+'</div>':''}"
    " function storychips(n){const S=(D.stories||[]).filter(s=>(s.concepts||[]).indexOf(n.id)>=0);return S.length?'<div class=\"storychips\">'+S.map(s=>'<button data-story=\"'+s.id+'\" title=\"'+esc(s.when)+'\">\U0001F4DC '+esc(s.title)+'</button>').join('')+'</div>':''}"
    " function sec(n,tag){return ", 1)
rep("function sec(n,tag){return '<section id=\"s-'+n.id+'\" data-source=\"'+esc(n.section_iri)+'\" data-concept=\"'+n.id+'\" class=\"'+(n.level===3?'leaf':'')+'\">",
    "function secHead(n,tag){return '<'+tag+'>'+(n.level<3?ICON[n.level]+' ':'')+'<span data-c=\"'+n.id+'\" class=\"c\">'+esc(n.label)+'</span> <button class=\"info\" data-detail=\"'+n.id+'\" title=\"Show details of '+esc(n.label)+'\" aria-label=\"Show details of '+esc(n.label)+'\">\u24d8</button></'+tag+'>'}"
    " function richInner(n,tag){return secHead(n,tag)+cfacts(n)+bodyRich(n)+excard(n)+storychips(n)+chartBox(n)+widget(n)+secVis(n)+'<div class=\"nbh\" data-nbhfor=\"'+n.id+'\"></div>'}"
    " function enrich(root){(root||panes).querySelectorAll('section.leaf[data-rich=\"0\"]').forEach(sc=>{const sp=sc.closest('[data-subpane]');if((sp&&sp.hidden)||sc.hidden)return;sc.dataset.rich='1';sc.innerHTML=richInner(byId[sc.dataset.concept],'h4')});"
    "(root||panes).querySelectorAll('.nbh[data-nbhfor]:not([data-done])').forEach(h=>{const sc=h.closest('section');if(sc&&sc.hidden)return;h.dataset.done='1';h.outerHTML=nbhSvg(byId[h.dataset.nbhfor])||'';});(root||panes).querySelectorAll('.nbh .diagram:not([data-z])').forEach(d=>{d.dataset.z='1';zoomable(d)})}"
    " function sec(n,tag){return '<section id=\"s-'+n.id+'\" data-source=\"'+esc(n.section_iri)+'\" data-concept=\"'+n.id+'\" class=\"'+(n.level===3?'leaf':'')+'\"'+(n.level===3?' data-rich=\"0\"':'')+'>", 1)

# ---- 1a. the concept pills under the breadcrumb ------------------------------------------------------------------
rep("' ('+kids(x.id).length+')</option>').join('')+'</select>';",
    "' ('+kids(x.id).length+')</option>').join('')+'</select>';"
    "  const lv=m.startsWith('ov-')?[]:kids(m);if(lv.length)h+='<div class=\"leafpick\" role=\"group\" aria-label=\"Concepts of '+esc(byId[m].label)+'\">'+lv.map(x=>'<button data-go=\"'+x.id+'\"'+(x.id===focus?' aria-current=\"true\"':'')+'>'+esc(x.label)+'</button>').join('')+'</div>';", 1)

# ---- wiring: neighbourhood boxes open the card; story chips open the story; maps become zoomable after render ----
# the boxes carry data-nbh, not data-detail: a test or a script that addresses [data-detail=id] must keep finding the one
# section button, not every neighbourhood box that names the concept; the handlers below open the card from data-nbh
rep("panes.innerHTML=P;",
    "panes.innerHTML=P;"
    "panes.addEventListener('keydown',e=>{const g=e.target.closest&&e.target.closest('g.nbc[data-nbh]');if(g&&(e.key==='Enter'||e.key===' ')){e.preventDefault();openCard(g.dataset.nbh)}});"
    "panes.addEventListener('click',e=>{const g=e.target.closest&&e.target.closest('g.nbc[data-nbh]');if(g){openCard(g.dataset.nbh);return}const b=e.target.closest&&e.target.closest('button[data-story]');if(!b)return;const k=b.dataset.story;showTab('stories');const el=document.getElementById('story-'+k);if(el){el.scrollIntoView({block:'start'});el.classList.add('flash');setTimeout(()=>el.classList.remove('flash'),1200)}});"
    "", 1)

# a touch on a neighbourhood box is a choice, not the start of a pan
rep("svg.onpointerdown=e=>{if(touches.size>1)return;if(e.target.closest('g.n,g.gn,g.on,[data-c],[data-oid],[data-gid],[data-ent]'",
    "svg.onpointerdown=e=>{if(touches.size>1)return;if(e.target.closest('g.n,g.gn,g.on,g.nbc,[data-c],[data-oid],[data-gid],[data-ent]'", 1)
rep("crumbs(p,m,focus);syncTree()}", "crumbs(p,m,focus);syncTree();enrich(pane)}", 1)
rep("<!-- course_page_template version 9.33.0:",
    "<!-- course_page_template version 9.34.0: the Learn sections after the owner's review of 2026-10-07 - concept pills "
    "under the breadcrumb for direct access to each concept of a section, paragraphs after the first folded under their lead "
    "sentence, and on every concept a WHERE/WHO/RUN/LINKS facts strip, a zoomable neighbourhood map whose boxes open the "
    "detail card, the worked example as a card, and chips to the stories that name it - all built when the section is first "
    "shown, so the page boots with exactly the work it did before; all from data the page already carried. Earlier: --><!-- course_page_template version 9.33.0:", 1)

open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
