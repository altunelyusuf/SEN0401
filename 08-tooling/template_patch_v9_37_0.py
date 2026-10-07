#!/usr/bin/env python3
"""Patches course_page_template_v9_36_0.html into course_page_template_v9_37_0.html.

One subject: the entity-relationship diagram, after the owner's review of 2026-10-07: "ERD is not about the
chapter, it is about the book ontology."

Measured: the ERD pane drew a fixed schema of the page's own data model - Subject, Topic, Concept, Example,
Syntax construct, Behaviour, Book concept - the same seven boxes on every chapter, with only the counts
changing. It explained what a system keeping track of the page would store, not what the chapter is about.

9.37.0 draws the CHAPTER as the ERD, from the chapter data the page carries: the entities are the chapter's
subjects (Money, Network, Wallet ...) by default, or its sections when chosen; an entity's attributes are what it
holds (its sections, or its concepts, the first six named and the rest counted); a relationship is drawn where
concepts of one entity operate on, or - as a toggle - are mentioned together with, concepts of another, and its
cardinality marks come from the data: a side is "many" when more than one distinct concept of that entity takes
part, "one" otherwise; the verb carries the count. Choosing an entity lists its members, its relationships with
their counts and the first evidence sentences. The page's own schema stays reachable as a third choice, "the
page's schema", because the About pane's vocabulary refers to it; it is no longer what the pane opens on.
"""
__version__ = "9.37.0"

SRC, DST = "course_page_template_v9_36_0.html", "course_page_template_v9_37_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# the schema model keeps its definitions under new names; OE_ENT / OE_REL become the CURRENT model
rep("const OE_ENT={", "const OE_SCHEMA_ENT={", 1)
rep("const OE_REL=[", "const OE_SCHEMA_REL=[", 1)
rep("function oeGlyph(x,y,dx,dy,kind){",
    r"""let OE_ENT=OE_SCHEMA_ENT,OE_REL=OE_SCHEMA_REL;const ERD={mode:'subjects',mentions:false};
function cerdModel(){const lvl=ERD.mode==='sections'?2:1;const ents=D.nodes.filter(n=>n.level===lvl);const entOf=id=>{let n=byId[id];while(n&&n.level>lvl)n=byId[n.parent];return n?n.id:null};
  const COLS=lvl===1?3:4,BW=170,GX=60,GY=50;const ENT={},REL=[];
  ents.forEach((e,i)=>{const members=lvl===1?kids(e.id):kids(e.id);const leaves=D.nodes.filter(x=>x.level===3&&entOf(x.id)===e.id);const names=members.map(m=>m.label+(lvl===1?' ('+kids(m.id).length+')':''));
    const attrs=names.slice(0,6).concat(names.length>6?['and '+(names.length-6)+' more']:[]);
    ENT[e.id]={x:20+(i%COLS)*(BW+GX),y:30+Math.floor(i/COLS)*(30+7*16+10+GY),label:e.label,attrs:attrs.length?attrs:['(no parts)'],n:()=>leaves.length,sample:()=>leaves.map(x=>x.label),id:e.id}});
  const agg=new Map();D.relations.forEach(r=>{if(r.type==='is a kind of')return;if(r.type==='mentions'&&!ERD.mentions)return;const a=entOf(r.source),b=entOf(r.target);if(!a||!b||a===b)return;const key=a+'|'+b+'|'+r.type;const e=agg.get(key)||{a,b,type:r.type,n:0,as:new Set(),bs:new Set(),ev:[]};e.n++;e.as.add(r.source);e.bs.add(r.target);if(e.ev.length<3)e.ev.push(byId[r.source].label+' '+r.type+' '+byId[r.target].label);agg.set(key,e)});
  agg.forEach(e=>REL.push([e.a,e.b,e.as.size>1?'many':'one',e.bs.size>1?'many':'one',(e.type==='mentions'?'mentioned with':'operates on')+' ×'+e.n,e.ev]));
  return {ENT,REL,rows:Math.ceil(ents.length/COLS),cols:COLS,bw:BW,gx:GX,gy:GY}}
function erdApply(){if(ERD.mode==='schema'){OE_ENT=OE_SCHEMA_ENT;OE_REL=OE_SCHEMA_REL;return {W:990,H:400}}const m=cerdModel();OE_ENT=m.ENT;OE_REL=m.REL;return {W:Math.max(990,20+m.cols*(m.bw+m.gx)),H:30+m.rows*(30+7*16+10+m.gy)+40}}
function erdControls(){const el=document.getElementById('erdctl');if(!el||el.dataset.built)return;el.dataset.built='1';
  el.innerHTML='<div class="grp"><b>Entities</b><button class="chip" data-erd="subjects" aria-pressed="true">The chapter\'s subjects</button><button class="chip" data-erd="sections" aria-pressed="false">Its sections</button><button class="chip" data-erd="schema" aria-pressed="false">The page\'s schema</button></div><div class="grp"><b>Relationships</b><button class="chip" data-erdm="1" aria-pressed="false">mentioned together</button></div>';
  el.addEventListener('click',e=>{const b=e.target.closest('[data-erd]');if(b){ERD.mode=b.dataset.erd;el.querySelectorAll('[data-erd]').forEach(x=>x.setAttribute('aria-pressed',x===b));document.getElementById('oerd').innerHTML='';document.getElementById('oerdinfo').textContent='Choose an entity to see what it holds.';drawOerd();return}
    const m=e.target.closest('[data-erdm]');if(m){ERD.mentions=!ERD.mentions;m.setAttribute('aria-pressed',ERD.mentions);document.getElementById('oerd').innerHTML='';drawOerd()}})}
function oeGlyph(x,y,dx,dy,kind){""", 1)

rep("async function drawOerd(){const el=document.getElementById('oerd');if(!el)return;await ogFacts();try{await ontoLoad()}catch(e){}\n const BW=160,LH=16;const H=400,W=990;",
    "async function drawOerd(){const el=document.getElementById('oerd');if(!el)return;erdControls();const dims=erdApply();if(ERD.mode==='schema'){await ogFacts();try{await ontoLoad()}catch(e){}}  const BW=ERD.mode==='schema'?160:170,LH=16;const H=dims.H,W=dims.W;", 1)
rep("s+='<g class=\"oe-key\" transform=\"translate(20,385)\"><text x=\"0\" y=\"0\">Key: | one · crow’s foot many · ○ optional. Each line reads from either end, for example one subject contains many topics; one concept is shown by zero or more examples.</text></g></svg>';",
    "s+='<g class=\"oe-key\" transform=\"translate(20,'+(H-15)+')\"><text x=\"0\" y=\"0\">'+(ERD.mode==='schema'?'Key: | one · crow’s foot many · ○ optional. Each line reads from either end, for example one subject contains many topics; one concept is shown by zero or more examples.':'Key: | one · crow’s foot many. A side is many when more than one concept of that entity takes part; the verb carries the count of concept-level links.')+'</text></g></svg>';", 1)
# the entity box shows the verb's evidence on the line's tooltip, and the panel lists evidence for chapter models
rep("s+='<g class=\"oe-r\"><line x1=\"'+p1[0]+'\" y1=\"'+p1[1]+'\" x2=\"'+p2[0]+'\" y2=\"'+p2[1]+'\"/>'",
    "s+='<g class=\"oe-r\"><title>'+esc(OE_ENT[a].label+' '+verb+' '+OE_ENT[b].label+(ev&&ev.length?' - e.g. '+ev.join('; '):''))+'</title><line x1=\"'+p1[0]+'\" y1=\"'+p1[1]+'\" x2=\"'+p2[0]+'\" y2=\"'+p2[1]+'\"/>'", 1)
rep("OE_REL.forEach(([a,b,ca,cb,verb])=>{const A=box(a),B=box(b);", "OE_REL.forEach(([a,b,ca,cb,verb,ev])=>{const A=box(a),B=box(b);", 1)
rep("<div class=\"kv\">Relationships</div><ul>'+OE_REL.filter(r=>r[0]===k||r[1]===k).map(r=>'<li>'+esc(OE_ENT[r[0]].label)+' <i>'+esc(r[4])+'</i> '+esc(OE_ENT[r[1]].label)+'</li>').join('')+'</ul>",
    "<div class=\"kv\">Relationships</div><ul>'+OE_REL.filter(r=>r[0]===k||r[1]===k).map(r=>'<li>'+esc(OE_ENT[r[0]].label)+' <i>'+esc(r[4])+'</i> '+esc(OE_ENT[r[1]].label)+(r[5]&&r[5].length?'<br><span class=\"note\">e.g. '+esc(r[5].join('; '))+'</span>':'')+'</li>').join('')+(OE_REL.some(r=>r[0]===k||r[1]===k)?'':'<li class=\"note\">no stated relationship with another entity'+(ERD.mode!=='schema'&&!ERD.mentions?' (turn on mentioned together)':'')+'</li>')+'</ul>", 1)

# the pane: a control row, and a note that says what the diagram now is
rep("<h2>🔗 Entity-relationship diagram</h2><p class=\"legend\"><span>| one</span><span>crow\\'s foot: many</span><span>○ optional</span></p><p class=\"note\">The schema behind the ontology as an entity-relationship diagram: the kinds of thing it knows about, their attributes, and how they relate, with the number of each in this chapter. Read a line from either end: one subject contains many topics; one concept is shown by zero or more examples; an example is written with many constructs and a construct is used by many examples. Choose an entity to see its attributes, its relationships and some of its members. An entity-relationship diagram answers what a system keeping track of this would have to store, rather than what a term means. '+WORDLINK+'</p><div class=\"ontowrap\">",
    "<h2>🔗 Entity-relationship diagram</h2><p class=\"legend\"><span>| one</span><span>crow\\'s foot: many</span><span>○ optional</span></p><p class=\"note\">The chapter as an entity-relationship diagram: its subjects (or its sections) are the entities, what each holds are its attributes, and a line is drawn where concepts of one entity operate on concepts of another - the document\\'s mentioned-together links can be added. The marks at the ends are read from the data: a side is many when more than one concept of that entity takes part. Choose an entity to see its members, its relationships with their counts and the sentences behind them. The page\\'s own schema - what a system keeping track of this page would store - is the third choice. '+WORDLINK+'</p><div class=\"mapctl\" id=\"erdctl\"></div><div class=\"ontowrap\">", 1)

rep("<!-- course_page_template version 9.36.0:",
    "<!-- course_page_template version 9.37.0: the entity-relationship diagram draws the chapter - its subjects or sections as "
    "entities with what they hold as attributes, relationships aggregated from the concept relations with data-derived "
    "cardinalities and counts, evidence in the panel - and keeps the page's schema as a third choice. Earlier: "
    "--><!-- course_page_template version 9.36.0:", 1)
open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
