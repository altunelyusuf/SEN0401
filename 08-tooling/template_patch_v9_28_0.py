#!/usr/bin/env python3
"""SEN0401 page template 9.28.0, from 9.27.0 - the shared-template repairs the adversarial audit of the chapter 1
page (version 9.28.0 of the page, built on template 9.27.0) asked for. Every change below is in the template, so it
reaches all five SEN0401 chapter pages; the same changes are applied to SEN0414's own chain by
advancedprogrammingwithpython/08-tooling/template_patch_v9_24_0.py, whose base (9.23.0) is the file this chain was
copied from.

WHAT CHANGES, AND WHY

 1. ONE SUBJECT, ONE SLICE (audit F-B1). A subject agent retrieved from the WHOLE corpus and merely added a small
    bonus to passages of its own slice, so any agent answered any question: the Units agent answered "what is
    phishing?" from the Threats agent's passages, citing the same six sources. `ownsChunk` was the cause: for a
    passage with no concept of its own it searched the passage's whole TEXT for any label of the agent's slice, and
    "unit" occurs in the text of almost everything. A passage is now tied to a concept, not to a word:
      - a page section carries its concept already;
      - an ontology subject is read from its own identifier (`S_`, `X_`, `IO_`, `Err_` before a concept name) and,
        failing that, from an exact match of its label to a concept's label;
      - a passage with no concept of its own (a book passage, a research finding) is owned only when the agent's own
        concept label occurs as a WORD in the passage's LABEL, singular or plural - never in its body text.
    `rank` then keeps only the passages the agent owns, so an agent cannot retrieve outside its slice at all. An
    agent asked something outside its slice says so and hands the question to the agent that owns it. A rank call
    with an empty `covers` (the page-wide search over the book, course and research passages) is unrestricted, as
    before.
 2. THE GUIDE RANKS ONLY OWNERS (F-B2). The guide already scored each agent over the passages `ownsChunk` gave it, so
    repairing ownership repairs the guide: `DoubleSpend` belongs to the Consensus agent's slice alone, and the Units
    and History agents can no longer be offered for it.
 3. THE ABOUT TEXT IS TRUE AGAIN (F-A3). "How it works" and "Agents & tools" promised retrieval restricted to an
    agent's own slice and a guide that ranks by slice. Both are now facts; the wording says exactly what happens,
    including the handover.
 4. AN UNAPPROVED SET OF OUTCOMES SAYS SO (F-A4). The Mission pane printed ten learning outcomes with no hint that
    their own source file calls them a DRAFT that is NOT APPROVED. The pane now reads the approval state out of the
    course ontology itself - a CASE document's approver and approval date, or their absence - and prints either
    "Approved by ... on ..." or a draft warning carrying the document's own note. Nothing about SEN0401 is written
    into the template, so SEN0414's approved outcomes are never labelled a draft.
 5. LEARNING OUTCOMES SORT BY NUMBER (F-E3). The query orders by code as a string, so LO-10 landed between LO-1 and
    LO-2. The pane now sorts the rows it got with a numeric-aware comparison.
 6. THE TAXONOMY OPENS READABLE (F-B3). All three layers were on (295 nodes over 8061 px) and the view opened at an
    arbitrary vertical offset, so 9 of 295 labels were legible. It now opens with the Classes layer only - the plain
    hierarchy of subjects and concepts - and the view is placed on the root at natural size. The other two layers are
    one click away and the note says so.
 7. AN EXECUTED EXAMPLE IS NAMED BY WHAT IT SHOWS (F-B4). 47 taxonomy boxes read as broken Python, because an
    IOExample's and an ErrorCondition's own `rdfs:label` IS the code. The code moves to the detail card: an example is
    labelled with the human label of the concept individual that owns it, an error with "the error <class> raises",
    and a repeated label is numbered so two boxes never read the same. Both are matched by the local name of the
    linking predicate (`has...Example`, `has...Condition`), so no ontology's namespace is named here.
 8. THE "ALL CHAPTERS" LINK IS SHOWN ONLY WHEN THERE IS AN INDEX (F-B5). The header always linked to `index.html`,
    which exists nowhere in either repository. The link is now removed unless the page data names an index
    (`index_page`), which the page build sets from what is really on disk beside the page.
 9. A SPARQL SAMPLE'S NAME IS SUBSTITUTED TOO (F-B6). `SPQ_FIX` was applied to the query only, so the visible option
    read 'Does the chapter define a class labelled "{FIRST_LEAF}"?'. It is now applied to the name as well.
10. A LAYER WITH NO LINKS IS NOT OFFERED (F-B7). The ontology graph showed Syntax and Behaviour checkboxes and their
    legend over zero links (SEN0401 chapters have none). Each control, its legend entry and its share of the status
    line now appear only when the chapter really has links of that kind, and a line explains the absence.
11. A BLANK ENDS WHERE THE READER CAN SEE IT (F-B8). The blank-filling generator picked `100` inside `100_000`, so
    `110_000 - _____000` hid where the blank ended. A numeric token is now taken whole, underscores included, and
    only at a token boundary.
12. A NON-DEREFERENCEABLE REFERENCE IS NOT A LINK (F-B9). The course-notes `urn:` was rendered as an anchor that does
    nothing when clicked. A reference whose address is not http(s) is now plain text, with its address shown.
13. THE HELP NAMES THE MENUS THE PAGE HAS (F-B10). "Questions" is called Practice, and the built-in checks are under
    About, not under Practice.
14. CODE QUESTIONS NO LONGER READ ALIKE (F-E2). 42 of 161 bank items share the stem "What does this program print?".
    A stem more than one item uses is now qualified by the concept it asks about, and numbered when one concept has
    several, so a list of them is readable. The bank file is not touched.
15. THE PAGE EXPLAINS ITS OWN VOCABULARY (F-D5). Ontology, knowledge graph, taxonomy, SPARQL, agent, Pyodide, class
    diagram and entity-relationship diagram were used throughout and defined nowhere. A new About sub-tab, "Words we
    use", explains each one in cohesive teaching paragraphs, and the panes where a student first meets a term carry a
    one-line explanation and a link to it.

usage: template_patch_v9_28_0.py [IN.html OUT.html]"""
__version__ = "9.28.0"
import json, sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_27_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_28_0.html")
h = open(src, encoding="utf-8").read()
APPLIED = []


def rep(a, b, n=1, tag=""):
    global h
    assert h.count(a) == n, ("anchor not found %dx: %r (found %d)" % (n, a[:90], h.count(a)))
    h = h.replace(a, b)
    APPLIED.append(tag or a[:40])


# ---- 1/2  one subject, one slice; the guide ranks only owners -------------------------------------------------------
rep("function ownsChunk(a,c){if(c.concept)return a.covers.includes(c.concept);const T=(c.label+' '+c.text).toLowerCase();return a.covers.some(id=>{const l=byId[id].label.toLowerCase();return l.length>3&&T.includes(l)})}",
    "// 9.28.0 - a passage belongs to an agent because of the CONCEPT it is about, never because one of the agent's words\n"
    "// appears somewhere in its body. conceptOfChunk reads the concept off the passage: a page section carries it; an\n"
    "// ontology subject states it in its own identifier (S_/X_/IO_/Err_ before a concept name) or matches a concept's\n"
    "// label exactly. A passage with no concept of its own - a book passage, a research finding - is owned only when the\n"
    "// agent's own concept label stands as a word in that passage's LABEL.\n"
    "const RXQ=s=>String(s).replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&');\n"
    "function conceptOfChunk(c){if('cid' in c)return c.cid;let id=c.concept||null;\n"
    " if(!id&&c.id){const loc=String(c.id).split(/[#/]/).pop();const bare=loc.replace(/^(X|IO|Err|S)_/,'');if(byId[bare])id=bare;else if(byId[loc])id=loc}\n"
    " if(!id){const l=String(c.label||'').replace(/\\s*\\([^)]*\\)\\s*$/,'').trim().toLowerCase();if(l.length>2){const n=D.nodes.find(x=>String(x.label).toLowerCase()===l);if(n)id=n.id}}\n"
    " c.cid=id||null;return c.cid}\n"
    "function sliceLabels(a){if(!a.__sl)a.__sl=((a.covers||[]).map(k=>String((byId[k]||{}).label||'').replace(/\\s*\\([^)]*\\)\\s*$/,'').trim().toLowerCase()).filter(l=>l.length>=4));return a.__sl}\n"
    "function ownsChunk(a,c){const cov=(a&&a.covers)||[];if(!cov.length)return false;\n"
    " const id=conceptOfChunk(c);if(id)return cov.indexOf(id)>=0;\n"
    " const L=String(c.label||'').toLowerCase();return sliceLabels(a).some(l=>new RegExp('\\\\b'+RXQ(l)+'s?\\\\b').test(L))}",
    tag="F-B1 ownsChunk")

rep(" scored.sort((x,y)=>y.score-x.score);return {top:scored.slice(0,k),semantic}}",
    " // 9.28.0 - an agent retrieves from its own slice and nowhere else; an empty covers set (the page-wide passage\n"
    " // search) is unrestricted, as before.\n"
    " if(a&&a.covers&&a.covers.length)scored=scored.filter(x=>ownsChunk(a,x.c));\n"
    " scored.sort((x,y)=>y.score-x.score);return {top:scored.slice(0,k),semantic}}",
    tag="F-B1 rank")

rep("if(!top.length||(semantic?best<0.33:best<=0)){const g=await routeScores(q);const o=g.find(x=>x.a.id!==aid);html='Nothing in the book, course or chapter material answers that.'+(o&&o.best>=0.33?' The <button class=\"jump\" data-handoff=\"'+o.a.id+'\" data-q=\"'+esc(q)+'\">'+agentIcon(o.a)+' '+esc(o.a.name)+'</button> may know - I can pass your question on.':'')+sourcesHtml([],how);topics=[]}",
    "if(!top.length||(semantic?best<0.33:best<=0)){const g=await routeScores(q);const o=g.find(x=>x.a.id!==aid&&x.best>=0.33);\n"
    "    // 9.28.0 - outside its own slice an agent hands over by name instead of answering from someone else's passages\n"
    "    const mine=(a.covers||[]).slice(0,3).map(i=>(byId[i]||{}).label).filter(Boolean).join(', ');\n"
    "    html=(o?'That is not in my subject'+(mine?' - I answer about '+esc(mine)+(a.covers.length>3?' and the rest of my own slice':''):'')+'. That belongs to the <button class=\"jump\" data-handoff=\"'+o.a.id+'\" data-q=\"'+esc(q)+'\">'+agentIcon(o.a)+' '+esc(o.a.name)+'</button> - I can pass your question on.':'Nothing in the book, course or chapter material answers that.')+sourcesHtml([],how);topics=[]}",
    tag="F-B1 handover")

# ---- 3  the About text says what the page really does --------------------------------------------------------------
rep("+'<p><b>Asking the agents.</b> Each agent knows one subject. Start with the Guide if you are unsure who to ask; it hands your question over. Agents answer from the book, the course and this chapter only, cite their passages, and follow on from earlier questions; open \"How I found this\" under an answer to see the query and the ranking. Enable the live LLM for written answers (desktop Chrome or Edge with WebGPU).</p>'",
    "+'<p><b>Asking the agents.</b> An agent is a question-answering assistant that owns one subject of this chapter, and it searches only the passages of that subject: the concepts it covers, their sections on this page, their entries in the chapter ontology, and the book, course and research passages written about them. Ask it something another agent owns and it will say so and offer to pass the question on, rather than answer from material that is not its own; start with the Guide if you are unsure who to ask, and it will name the agents whose subject really contains your question. Every answer cites the passages it was built from and follows on from your earlier questions, and \"How I found this\" under an answer shows the query that fetched the slice and the ranking over it. Enable the live LLM for answers written as prose (desktop Chrome or Edge with WebGPU).</p>'",
    tag="F-A3 howto agents")

rep("function drawProv(){const agentsHtml='<p>'+D.agents.length+' subject agents and a guide. Each agent owns a slice of this chapter\\u2019s ontology; the guide ranks agents by how well their slice matches a question.",
    "function drawProv(){const agentsHtml='<p>'+D.agents.length+' subject agents and a guide. Each agent owns a slice of this chapter\\u2019s ontology and retrieves from that slice alone, so two agents whose slices do not overlap cannot give the same answer to the same question; asked outside its slice, an agent hands the question to the agent that owns it. The guide scores only agents whose slice contains the concept a question matched.",
    tag="F-A3 arch")

# ---- 4/5  the approval state of the outcomes, and their order ------------------------------------------------------
rep(" try{await ensureGraph();const _lo=SPARQL_SAMPLES.find(s=>/learning outcome/i.test(s[0]))||SPARQL_SAMPLES[3];const rows=_lo?await sparql(_lo[1]):[];el.innerHTML=h+'<h3>Course learning outcomes</h3>'+(rows.length?'<ul>'+rows.map(r=>'<li><b>'+esc(r.code)+'</b> '+esc(r.statement)+'</li>').join('')+'</ul>':'<p class=\"note\">The course ontology states none.</p>')}catch(e){}}",
    " try{await ensureGraph();const _lo=SPARQL_SAMPLES.find(s=>/learning outcome/i.test(s[0]))||SPARQL_SAMPLES[3];let rows=_lo?await sparql(_lo[1]):[];\n"
    "  // 9.28.0 - a code is ordered by the number in it, so LO-10 follows LO-9 instead of landing between LO-1 and LO-2\n"
    "  rows=rows.slice().sort((x,y)=>natCmp(x.code,y.code));\n"
    "  const status=rows.length?await outcomeStatus():'';\n"
    "  el.innerHTML=h+'<h3>Course learning outcomes</h3>'+status+(rows.length?'<ul>'+rows.map(r=>'<li><b>'+esc(r.code)+'</b> '+esc(r.statement)+'</li>').join('')+'</ul>':'<p class=\"note\">The course ontology states none.</p>')}catch(e){}}\n"
    "const natCmp=(a,b)=>{const S=x=>String(x==null?'':x).split(/(\\d+)/).map(p=>/^\\d+$/.test(p)?p.padStart(9,'0'):p).join('');const u=S(a),v=S(b);return u<v?-1:u>v?1:0};\n"
    "// 9.28.0 - whether a set of course outcomes is approved is a fact of the course ontology, not of this template: a\n"
    "// CASE document that records an approver or an approval date is approved, and one that records neither is a draft\n"
    "// and is published as one, with the document's own note. Nothing here is specific to one course.\n"
    "async function outcomeStatus(){try{\n"
    " const q='PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> SELECT ?doc ?by ?at ?note WHERE { GRAPH ?g { ?doc a ?ty . FILTER(STRENDS(STR(?ty),\"dtCFDocument\")) OPTIONAL { ?doc ?pb ?by . FILTER(STRENDS(STR(?pb),\"approvedBy\")) } OPTIONAL { ?doc ?pa ?at . FILTER(STRENDS(STR(?pa),\"approvedAt\")) } OPTIONAL { ?doc rdfs:comment ?note } } }';\n"
    " const rs=await sparql(q);if(!rs.length)return '';const r=rs.find(x=>x.by||x.at)||rs[0];\n"
    " if(r.by||r.at)return '<p class=\"note\">These outcomes are approved'+(r.by?' by '+esc(r.by):'')+(r.at?', on '+esc(String(r.at).slice(0,10)):'')+', as the course ontology itself records.</p>';\n"
    " return '<p class=\"draftnote\"><b>Draft - not approved.</b> The course ontology records no approver and no approval date for these outcomes, so they are a proposal and not yet the course\\u2019s agreed outcomes; do not rely on them until the owner has ruled on them.'+(r.note?' <span class=\"note\">'+esc(r.note)+'</span>':'')+'</p>'}catch(e){return ''}}",
    tag="F-A4/F-E3 mission")

rep(".idxlink{color:#fff;",
    ".draftnote{border:1px solid #8A5A00;background:#FFF6DB;color:#5A3A00;border-radius:8px;padding:.5rem .7rem;margin:.4rem 0}\n"
    ".term{border-bottom:1px dotted currentColor}\n"
    ".idxlink{color:#fff;",
    tag="draft/term css")

# ---- 6/7  the taxonomy: classes only, placed on the root, examples named by what they show -------------------------
rep('<label><input type="checkbox" data-okind="individual" checked> Individuals</label><label><input type="checkbox" data-okind="book" checked> Book concepts</label>',
    '<label><input type="checkbox" data-okind="individual"> Worked examples</label><label><input type="checkbox" data-okind="book"> Book concepts</label>',
    tag="F-B3 defaults")

rep("Use the checkboxes to hide a kind of node (with only the classes shown this is the plain hierarchy of subjects and concepts), and Show all to fit the whole tree; wheel or pinch to zoom, drag to move.",
    "It opens as the plain hierarchy of subjects and concepts - the classes alone, placed on the root at full size - because all three layers at once draw several hundred boxes and none of them stays readable. Tick Worked examples or Book concepts to add those leaves, Show all to fit the whole tree into the window, and wheel, pinch or drag to move about at your own size. A worked example is named by what it shows; its code is in the card on the right.",
    tag="F-B3 note")

rep(" const N=new Map();(await sparql(nodesQ)).forEach(r=>{if(!N.has(r.s))N.set(r.s,{id:r.s,label:r.label||r.s.split(/[#/]/).pop(),kind:r.kind})});",
    " const N=new Map();(await sparql(nodesQ)).forEach(r=>{if(!N.has(r.s))N.set(r.s,{id:r.s,label:r.label||r.s.split(/[#/]/).pop(),kind:r.kind})});\n"
    " // 9.28.0 - a worked example and an error case carry their CODE as their own rdfs:label, which drew 47 boxes that\n"
    " // read as broken Python. The code is kept (the detail card shows it) and the box is named by what the example\n"
    " // shows: the human label of the concept individual that owns it, or, for an error, the class that raises it.\n"
    " const ioQ=PFX+'SELECT ?s ?in ?out WHERE { GRAPH ?g { ?s ?pi ?in . OPTIONAL { ?s ?po ?out . FILTER(STRENDS(STR(?po),\"#output\")) } FILTER(STRENDS(STR(?pi),\"#input\")) } FILTER(CONTAINS(STR(?g),\":chapter:\")) }';\n"
    " (await sparql(ioQ)).forEach(r=>{const n=N.get(r.s);if(n){n.code=r['in'];if(r.out!==undefined)n.out=r.out}});",
    tag="F-B4 io query")

rep(" ONTO={nodes:[...N.values()],edges:E,seed:1};return ONTO}",
    " {const cls=new Map();E.forEach(e=>{if(e.p==='type'&&N.has(e.b)&&N.get(e.b).kind==='class'&&!cls.has(e.a))cls.set(e.a,e.b)});\n"
    "  const used=new Map();[...N.values()].forEach(x=>{const k=String(x.label||'').toLowerCase();used.set(k,(used.get(k)||0)+1)});\n"
    "  E.forEach(e=>{const m=/^has([A-Za-z]*)(Example|Condition)$/.exec(e.p);if(!m)return;const n=N.get(e.b),ow=N.get(e.a);if(!n||!ow)return;\n"
    "   if(!n.code)n.code=n.label;                                         // an error case keeps its code in its own label\n"
    "   const owner=String(ow.label||'').trim(),kcls=N.get(cls.get(e.a)),cl=kcls?String(kcls.label||'').trim():'';\n"
    "   let lab=m[2]==='Condition'?('the error '+(cl||owner)+' raises'):((owner?owner+' (computed)':(cl?cl+': worked example':n.label)));\n"
    "   const k=lab.toLowerCase();used.set(k,(used.get(k)||0)+1);if(used.get(k)>1)lab+=' ('+used.get(k)+')';\n"
    "   n.label=lab;n.role=m[2]==='Condition'?'error':'example'});}\n"
    " ONTO={nodes:[...N.values()],edges:E,seed:1};return ONTO}",
    tag="F-B4 relabel")

rep(" {const sv=el.querySelector('svg'),vw=Math.min(W,Math.max(640,el.clientWidth||760)),vh=Math.min(H,Math.max(420,(el.clientHeight||560))),cy=root.y+root.h/2;sv.dataset.vbkeep='0 '+Math.max(0,Math.min(H-vh,cy-vh/2))+' '+vw+' '+vh}",
    " // 9.28.0 - the view opens on the ROOT, showing every column of the tree. The old window was 740 units wide\n"
    " // whatever the tree measured, so the deepest column was cut off the right-hand edge, and its vertical offset was\n"
    " // taken from the middle of the tree rather than from the root. It now takes the tree's full width, keeps the\n"
    " // pane's own aspect so nothing is distorted, and is placed on the root.\n"
    " {const sv=el.querySelector('svg'),cw=Math.max(320,el.clientWidth||760),chh=Math.max(240,el.clientHeight||560),\n"
    "  vw=Math.max(W,cw),vh=Math.min(H,Math.max(360,vw*chh/cw)),cy=root.y+root.h/2;\n"
    "  sv.dataset.vbkeep='0 '+Math.max(0,Math.min(Math.max(0,H-vh),Math.round(cy-vh/2)))+' '+vw+' '+vh}",
    tag="F-B3 open view")

rep(" const page=D.nodes.find(x=>x.class_iri===id),KL={class:'class',individual:'individual',book:'concept from the book'};",
    " const page=D.nodes.find(x=>x.class_iri===id),KL={class:'class',individual:(n.role==='error'?'error case':n.role==='example'?'executed example':'individual'),book:'concept from the book'};\n"
    " // 9.28.0 - the code of a worked example lives here, in the card, and not in the box's name\n"
    " const codeHtml=n.code?'<div class=\"kv\">Its code</div><pre>'+esc(n.code)+'</pre>'+(n.out!==undefined?'<div class=\"exout\">\\u2192 '+esc(n.out)+'</div>':''):'';",
    tag="F-B4 card code")

rep("document.getElementById('taxoinfo').innerHTML='<b>'+esc(n.label)+'</b> <span class=\"note\">('+KL[n.kind]+')</span>'+(path.length?'<p class=\"note\">Under: '+path.map(p=>esc(p.label)).join(' › ')+'</p>':'')",
    "document.getElementById('taxoinfo').innerHTML='<b>'+esc(n.label)+'</b> <span class=\"note\">('+KL[n.kind]+')</span>'+(path.length?'<p class=\"note\">Under: '+path.map(p=>esc(p.label)).join(' › ')+'</p>':'')+codeHtml",
    tag="F-B4 card code use")

# ---- 8  the "All chapters" link only when an index really exists ---------------------------------------------------
rep("setTimeout(()=>{tops.forEach(t=>crumbs(t.id,'ov-'+t.id));restoreConversations();",
    "// 9.28.0 - the header linked to an index.html that exists nowhere; the link is shown only when the page data names\n"
    "// one (the page build sets index_page from what is really on disk beside the page).\n"
    "{const _ix=document.querySelector('a.idxlink');if(_ix){if(D.index_page)_ix.setAttribute('href',D.index_page);else _ix.remove()}}\n"
    "setTimeout(()=>{tops.forEach(t=>crumbs(t.id,'ov-'+t.id));restoreConversations();",
    tag="F-B5 index link")

# ---- 9  a sample's visible name is substituted too -----------------------------------------------------------------
rep("D.course.sparql_samples.map(x=>[x[0],SPQ_FIX(x[1])])",
    "D.course.sparql_samples.map(x=>[SPQ_FIX(x[0]),SPQ_FIX(x[1])])",
    tag="F-B6 sample label")

# ---- 10  a layer with no links is not offered ----------------------------------------------------------------------
rep(" st.textContent='reading the knowledge graph and the examples...';let O=null;try{O=await ontoLoad()}catch(e){}const F=await ogFacts();ogRender(O,F)}",
    " st.textContent='reading the knowledge graph and the examples...';let O=null;try{O=await ontoLoad()}catch(e){}const F=await ogFacts();\n"
    " // 9.28.0 - a chapter whose examples are not programs has no syntax and no behaviour links at all, and was still\n"
    " // offered both filters and their legend over an empty graph. A layer is offered only when it has links.\n"
    " {const E0=ogEdges(ogRows(),F||{}),has={syntax:E0.some(e=>e.layer==='syntax'),behaviour:E0.some(e=>e.layer==='behaviour')};\n"
    "  const pane=document.querySelector('[data-pane=\"ontograph\"]');\n"
    "  document.querySelectorAll('[data-glayer]').forEach(c=>{const k=c.dataset.glayer;if((k in has)&&!has[k]){c.checked=false;const lb=c.closest('label');if(lb)lb.hidden=true}});\n"
    "  if(pane){[...pane.querySelectorAll('.legend span')].forEach(sp=>{const t=sp.textContent.toLowerCase();if((/syntax/.test(t)&&!has.syntax)||(/behaviour/.test(t)&&!has.behaviour))sp.hidden=true});\n"
    "   if(!has.syntax&&!has.behaviour&&!pane.querySelector('.nolayers')){const p=document.createElement('p');p.className='note nolayers';p.textContent='This chapter\\u2019s examples are not Python programs, so the syntax and behaviour layers have nothing to draw and are not offered; the view shows the meaning layer - what each concept is a kind of.';const lg=pane.querySelector('.legend');if(lg)lg.insertAdjacentElement('afterend',p)}}\n"
    "  pane&&(pane.dataset.layers=['meaning'].concat(Object.keys(has).filter(k=>has[k])).join(','))}\n"
    " ogRender(O,F)}",
    tag="F-B7 layers")

rep(" st.textContent=rows.length+' concepts · '+nM+' meaning links · '+nS+' syntax links · '+nB+' behaviour links';el.__E=E;el.__O=O;setTimeout(fitViews,30)}",
    " st.textContent=rows.length+' concepts · '+nM+' meaning links'+(nS?' · '+nS+' syntax links':'')+(nB?' · '+nB+' behaviour links':'');el.__E=E;el.__O=O;setTimeout(fitViews,30)}",
    tag="F-B7 status")

# ---- 11  a blank that ends where the reader can see it --------------------------------------------------------------
rep("function blankTokens(code){const re=/'[^'\\n]*'|\"[^\"\\n]*\"|\\d+(?:\\.\\d+)?|[A-Za-z_]\\w*/g,T=[];",
    "// 9.28.0 - a numeric literal is taken WHOLE, underscores included, and only at a token boundary: the old pattern\n"
    "// matched 100 inside 100_000 and left `110_000 - _____000`, where the reader cannot see the blank end.\n"
    "function blankTokens(code){const re=/'[^'\\n]*'|\"[^\"\\n]*\"|(?<![\\w.])\\d[\\d_]*(?:\\.\\d+)?(?![\\w.])|[A-Za-z_]\\w*/g,T=[];",
    tag="F-B8 tokens")

# ---- 12  a non-dereferenceable reference is not a link --------------------------------------------------------------
rep("<ol>'+D.refs.map(([l,u])=>'<li>'+esc(l)+' - <a href=\"'+esc(u)+'\">'+esc(u)+'</a></li>').join('')+'</ol>",
    "<ol>'+D.refs.map(([l,u])=>'<li>'+esc(l)+' - '+(/^https?:/i.test(String(u))?'<a href=\"'+esc(u)+'\">'+esc(u)+'</a>':'<span class=\"note\">'+esc(u)+' <i>(not a web address: this source was supplied as a file, and the name above carries its sha256)</i></span>')+'</li>').join('')+'</ol>",
    tag="F-B9 urn")

# ---- 13  the help names the menus the page has ----------------------------------------------------------------------
rep("+'<p><b>Learning.</b> Maps show the chapter as a taxonomy, a concept map and an ontology graph. Questions offers questions by subject, questions for a role, and the page\\u2019s own built-in checks. The quiz, glossary and references close the chapter.</p>'",
    "+'<p><b>Learning.</b> Maps show the chapter as a taxonomy, a concept map and an ontology graph. Practice holds the quiz, the code exercises, the twelve question types, the mock exam, questions by subject and questions for a role. Reference holds the glossary, the cheat sheet and the sources. About explains how the page works, what its agents and tools are, the words it uses, where its text comes from, and the page\\u2019s own built-in checks.</p>'",
    tag="F-B10 learning")

rep("The top menu holds the chapter\\u2019s subjects and the views; a subject\\u2019s tabs are its sub-subjects, and grouped views (Maps, Lab, Questions, About) show their own tabs.",
    "The top menu holds the chapter\\u2019s subjects and the views; a subject\\u2019s tabs are its sub-subjects, and the grouped views (Maps, Lab, Practice, Reference, About) show their own tabs.",
    tag="F-B10 moving")

# ---- 14  code questions no longer read alike -------------------------------------------------------------------------
rep("const BANK=(()=>{try{return JSON.parse(document.getElementById('qbank').textContent)||[]}catch(e){return[]}})(),BSEEN=new Set();",
    "const BANK=(()=>{try{return JSON.parse(document.getElementById('qbank').textContent)||[]}catch(e){return[]}})(),BSEEN=new Set();\n"
    "// 9.28.0 - 42 of this chapter's bank items share the stem \"What does this program print?\", so a list of them read\n"
    "// identically. A stem more than one item uses is shown with the concept it asks about, and numbered when one\n"
    "// concept has several. The bank file itself is unchanged.\n"
    "const BSTEM={},BSEQ={};BANK.forEach(b=>{BSTEM[b.q]=(BSTEM[b.q]||0)+1;const k=b.q+'\\u0000'+b.concept;BSEQ[k]=(BSEQ[k]||0)+1;b._seq=BSEQ[k]});\n"
    "function bankStem(b){if((BSTEM[b.q]||0)<2)return b.q;const n=byId[b.concept];const k=b.q+'\\u0000'+b.concept;\n"
    " return b.q+(n?' \\u2014 '+n.label:'')+(BSEQ[k]>1?' ('+b._seq+')':'')}",
    tag="F-E2 bankStem")

rep("return {kind,concept:cid,q:b.q,code:b.code||'',options:idx.map(i=>b.options[i]),answer:idx.indexOf(b.answer),why:b.why,level:b.level}}",
    "return {kind,concept:cid,q:bankStem(b),code:b.code||'',options:idx.map(i=>b.options[i]),answer:idx.indexOf(b.answer),why:b.why,level:b.level}}",
    tag="F-E2 qMake")

rep(" return {type:'mcq',pts:XT_PTS.mcq,concept:b.concept,level:b.level||'Understand',q:b.q,code:b.code||'',options:idx.map(i=>b.options[i]),answer:idx.indexOf(b.answer),why:b.why}}",
    " return {type:'mcq',pts:XT_PTS.mcq,concept:b.concept,level:b.level||'Understand',q:(b.options&&BSTEM[b.q]?bankStem(b):b.q),code:b.code||'',options:idx.map(i=>b.options[i]),answer:idx.indexOf(b.answer),why:b.why}}",
    tag="F-E2 xMcq")

# ---- 15  the page explains its own vocabulary -----------------------------------------------------------------------
WORDS = [
    ("Ontology", "ontology",
     "An ontology is a written-down model of a subject: the kinds of thing it contains, the sentence that says what each kind means, how the kinds sit under one another, and which things of each kind are known. The chapter you are reading has one, built before the page was written, and the page is generated from it rather than typed beside it - which is why a definition here, a box in the taxonomy and a passage an agent cites are always the same sentence. It is useful for exactly that reason: a model a program can read can also be checked by a program, so a claim cannot drift away from the material it came from without something noticing."),
    ("Knowledge graph", "knowledge graph",
     "A knowledge graph is what an ontology looks like once it is loaded and ready to be questioned: every statement is a small three-part sentence - a subject, a relation and a value - and the statements join up into one network through the subjects they share. This page carries several such files, each kept in its own named compartment so you can always tell a sentence of the book from a sentence of the course, of the chapter, or of the research record. The agents search it, the maps are drawn from it, and the console queries it, all in your browser and with nothing sent anywhere."),
    ("Triple", "triple",
     "A triple is one statement of a knowledge graph: a subject, the relation being asserted, and the thing the relation points at, which may be another subject or a plain value such as a label, a date or a sentence. Counting triples is the usual way of saying how much a graph holds, which is why the page tells you the total it loaded and how much each file contributed."),
    ("Taxonomy", "taxonomy",
     "A taxonomy is the part of an ontology that says what is a kind of what, drawn as a single tree: the chapter sits at the root, its subjects hang beneath it, their concepts beneath those, and a worked example or a matching concept of the book hangs as a leaf under the concept it belongs to. Reading downwards tells you what a subject is made of; reading upwards tells you what a concept is an instance of, which is the fastest way to see where a new term fits among the ones you already know."),
    ("SPARQL", "SPARQL",
     "SPARQL is the query language for knowledge graphs, and it does for triples what SQL does for tables: you write a pattern of statements with question marks where the unknowns are, and the answer is every set of values that makes the pattern true. The console in the Lab runs real SPARQL over the files this page embeds, so you can ask a question the page does not have a button for - every class and its parent, every computed example and its result, every source the research record cites - and read the answer as rows you can copy."),
    ("Agent", "agent",
     "An agent here is a question-answering assistant that owns one subject of the chapter and answers only from that subject's own passages. Asking it a question runs a query for its slice of the knowledge graph, ranks that slice's passages against your words, and builds an answer from the best of them with every passage cited, so you can always open the source and judge it; a question belonging to another subject is handed to the agent that owns it instead of being answered from material that is not its own. There are as many agents as the chapter has subjects, plus a guide whose only job is to tell you which of them to ask."),
    ("Semantic search", "semantic search",
     "Semantic search ranks passages by what they mean rather than by the words they happen to share with your question, which is what lets \u201chow is new bitcoin created?\u201d find a passage that only ever says \u201cmining\u201d. It works by turning each passage and your question into a list of numbers - an embedding - with a small language model that runs in this page, and then measuring which lists point in the same direction. When that model cannot be loaded the page falls back to plain keyword matching and says so in its status line."),
    ("Pyodide", "Pyodide",
     "Pyodide is CPython itself, compiled to WebAssembly so that it runs inside the browser; this page uses it to execute every program you see, in a background thread, with no server and no network. That is why an example is not a picture of a result: you can edit the code and run it again, and what appears is what Python really printed on your own machine. It carries the standard library but nothing that needs the network or the operating system, so a program here is limited to what the standard library alone can do."),
    ("Class diagram", "class diagram",
     "A class diagram shows the kinds in an ontology as boxes joined by the \u201cis a kind of\u201d relation, with a hollow triangle pointing at the more general kind, in the notation UML uses for software designs. It answers the same question as the taxonomy for one branch at a time, and in a form a software engineer will already recognise from design work, which makes it the natural view to put beside a design discussion."),
    ("Entity-relationship diagram (ERD)", "entity-relationship diagram",
     "An entity-relationship diagram shows the same ontology the way a database designer would draw it: each kind of thing is an entity, each property that joins two kinds is a relationship with its own name, and the diagram is read as what would have to be stored to record the facts the chapter states. It is useful when the question is not \u201cwhat does this term mean\u201d but \u201cwhat would a system that kept track of this have to hold\u201d."),
]
WORDS_HTML = "".join(
    "<h3 id=\"w-%s\">%s</h3><p>%s</p>" % (k.lower().replace(" ", "-").replace("(", "").replace(")", ""), t, p)
    for t, k, p in WORDS)
assert "</script" not in WORDS_HTML
rep("const HOWTO_HTML=",
    "// 9.28.0 - the page used its own vocabulary (ontology, knowledge graph, taxonomy, SPARQL, agent, Pyodide, class\n"
    "// diagram, ERD) and explained none of it. Each term is explained here, in About > Words we use, and the panes\n"
    "// where a student first meets one carry a line and a link to it.\n"
    "const WORDS_HTML=" + json.dumps(WORDS_HTML) + ";\n"
    "const WORDLINK='<button class=\"jump\" data-words=\"1\">What do these words mean?</button>';\n"
    "const HOWTO_HTML=",
    tag="F-D5 words html")

rep("about:[['howto','📘 How it works'],['arch','🧠 Agents & tools']",
    "about:[['howto','📘 How it works'],['words','🔤 Words we use'],['arch','🧠 Agents & tools']",
    tag="F-D5 words tab")

rep("P+='<div role=\"tabpanel\" data-pane=\"arch\" hidden>'+subbar('about')+'<h2>🧠 Agents & tools</h2><div id=\"archout\" class=\"prose\"></div></div>';",
    "P+='<div role=\"tabpanel\" data-pane=\"words\" hidden>'+subbar('about')+'<h2>🔤 Words we use</h2><p class=\"note\">Every term and tool this page relies on, explained before you are asked to use it. Nothing here is specific to one chapter.</p><div class=\"prose\">'+WORDS_HTML+'</div></div>';\n"
    "P+='<div role=\"tabpanel\" data-pane=\"arch\" hidden>'+subbar('about')+'<h2>🧠 Agents & tools</h2><div id=\"archout\" class=\"prose\"></div></div>';",
    tag="F-D5 words pane")

rep("if(t.id==='ofit')",
    "if(t.dataset.words){showTab('words');return}\n if(t.id==='ofit')",
    tag="F-D5 words link")

rep("<h2>🔎 SPARQL console</h2><p class=\"note\">Query the knowledge graph the agents use: the book, course and chapter ontologies and the research record, each file in its own named graph. SELECT and ASK queries run in the background thread.</p>",
    "<h2>🔎 SPARQL console</h2><p class=\"note\">SPARQL is the query language of a knowledge graph: you write a pattern of three-part statements with question marks for the unknowns, and every set of values that makes the pattern true comes back as a row. Query the same graph the agents use - the book, course and chapter ontologies and the research record, each file in its own named compartment. SELECT and ASK queries run in the background thread. '+WORDLINK+'</p>",
    tag="F-D5 sparql note")

rep("<h2>🌳 Chapter taxonomy</h2>",
    "<h2>🌳 Chapter taxonomy</h2><p class=\"note\">A taxonomy is the \\u201cis a kind of\\u201d part of the chapter\\u2019s ontology, drawn as one tree. '+WORDLINK+'</p>",
    tag="F-D5 taxonomy note")

rep("<h2>🧬 Ontology graph</h2>",
    "<h2>🧬 Ontology graph</h2><p class=\"note\">An ontology is the written-down model this page is generated from; this view draws it as a graph of three kinds of relation. '+WORDLINK+'</p>",
    tag="F-D5 ontograph note")

rep("The arrow points from a class to the class it is a kind of. Choose a box to open the concept\\'s card.",
    "The arrow points from a class to the class it is a kind of. Choose a box to open the concept\\'s card. A class diagram is the notation UML uses for a software design, so the same picture can be read beside one. '+WORDLINK+'",
    tag="F-D5 class note")

rep("Choose an entity to see its attributes, its relationships and some of its members.",
    "Choose an entity to see its attributes, its relationships and some of its members. An entity-relationship diagram answers what a system keeping track of this would have to store, rather than what a term means. '+WORDLINK+'",
    tag="F-D5 erd note")

# ---- the version comment ---------------------------------------------------------------------------------------------
rep("<!-- course_page_template version 9.16.0:",
    "<!-- course_page_template version 9.28.0: an agent retrieves only from its own slice and hands over outside it; the guide ranks only owners; the taxonomy opens as classes only on the root and names worked examples by what they show; unapproved course outcomes say so and sort by number; a layer with no links, and an index link with no index, are not shown; the page explains its own vocabulary. Earlier: --><!-- course_page_template version 9.16.0:",
    tag="version comment")

open(out, "w", encoding="utf-8").write(h)
print("wrote", os.path.basename(out), len(h), "bytes;", len(APPLIED), "changes:")
for t in APPLIED:
    print("   -", t)
