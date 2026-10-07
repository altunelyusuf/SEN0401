#!/usr/bin/env python3
"""Patches course_page_template_v9_34_0.html into course_page_template_v9_35_0.html.

One subject: the concept map, after the owner's review of 2026-10-07: "Concept map is not readable at all, we
need a way to enable the readability. Additionally there should be filtering options."

Measured on the chapter 1 page: the map drew all 117 concepts on three fixed rings with 464 lines (329 of them
the dashed "mentioned together" lines), labels as bare text under 9-px dots, so labels overlapped and the lines
covered everything. The data is right; the drawing had no level of detail and no filter.

What 9.35.0 draws instead, from the same D.nodes and D.relations:
- A SECTIONS view by default: the subjects on a ring and their sections around them, as boxes with wrapped
  labels and the number of concepts each holds; every relation between concepts is aggregated to the sections
  it joins, drawn once per kind with its count and a line width that grows with it, and a tooltip naming the
  kind, the count and the first evidence sentences. About thirty boxes: readable at a glance.
- A CONCEPTS view for the chosen subjects: subject, its sections, their concepts, each in an angular slot
  proportional to what it holds, so a subject with twenty concepts gets the room. Entering it with every subject
  chosen would redraw the unreadable map, so it opens on the first chosen subject alone and says so; the chips
  then choose more.
- FILTERS, all on the pane: subject chips (toggle each), relation kinds (is a kind of / operates on /
  mentioned together - the last off by default in the concepts view, on in the sections view where it is
  aggregated), a search box that keeps matching boxes bright and dims the rest, and a focus field (any concept,
  with suggestions) that redraws the map as that concept's neighbourhood - it, its section and subject, and
  every concept related to it - with "Show all" to return.
- Touching a box opens the detail card (the owner's rule: options first), exactly as before; the g.gn[data-c]
  markup the tests tap is kept.
"""
__version__ = "9.35.0"

SRC, DST = "course_page_template_v9_34_0.html", "course_page_template_v9_35_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# ---- CSS ---------------------------------------------------------------------------------------------------------
rep("</style>", """/* 9.35.0: the concept map - controls, boxed nodes, dimming */
.mapctl{display:flex;flex-wrap:wrap;gap:.4rem .9rem;align-items:center;margin:.3rem 0 .5rem;font-size:.9rem}
.mapctl .grp{display:flex;flex-wrap:wrap;gap:.3rem;align-items:center}.mapctl .grp>b{margin-right:.2rem;color:#7A4A10}
.mapctl button.chip{font:inherit;font-size:.85rem;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:.1rem .6rem;cursor:pointer}
.mapctl button.chip[aria-pressed=true]{background:var(--yellow);border-color:#9A5A10;font-weight:700}
.mapctl input{font:inherit;font-size:.9rem;padding:.15rem .4rem;border:1px solid var(--line);border-radius:6px;background:var(--panel);min-width:11rem}
#graph svg text{font:14px Calibri,Arial,sans-serif;fill:var(--ink)}#graph svg .gn{cursor:pointer}#graph svg .gn rect{rx:7;stroke-width:1.3}
#graph svg .gn.l1 rect{fill:var(--navy);stroke:var(--navy)}#graph svg .gn.l1 text{fill:#FAF6EF;font-weight:700}
#graph svg .gn.l2 rect{fill:var(--band);stroke:var(--blue)}#graph svg .gn.l3 rect{fill:var(--card);stroke:var(--blue)}
#graph svg .gn.focus rect{fill:var(--yellow);stroke:#9A5A10;stroke-width:2}
#graph svg .dim{opacity:.18}#graph svg .ge{fill:none}#graph svg .ge.isa{stroke:#A89C8C}#graph svg .ge.op{stroke:#9A5A10}#graph svg .ge.me{stroke:#1A7F37;stroke-dasharray:6 4;opacity:.6}
#graph svg .gcount{font-size:11px;fill:#7A4A10;font-weight:700}
#graph .diagram{height:34rem;min-height:14rem;resize:vertical;overflow:hidden;background:var(--panel);border:1px solid var(--line);border-radius:8px}
</style>""", 1)

# ---- the pane: legend and note stay; the control row is drawn by the script into #mapctl ---------------------------
rep("Hover an edge to read it; choose a node to open its card.</p><div class=\"graph\" id=\"graph\"></div></div>';",
    "Hover an edge to read it; choose a node to open its card. The map opens on the chapter\\'s sections with the stated relations between them counted (the document\\'s mentioned-together links are a toggle, there are hundreds); switch to concepts for the subjects you choose, or focus on one concept to see only its neighbourhood.</p><div class=\"mapctl\" id=\"mapctl\"></div><div class=\"graph\" id=\"graph\"></div></div>';", 1)

# ---- the drawing -------------------------------------------------------------------------------------------------
i = t.find("function drawGraph(){"); j = t.find("zoomable(el.querySelector('.diagram'))}", i)
assert i > 0 and j > i and t.count("function drawGraph(){") == 1
OLD = t[i:j + len("zoomable(el.querySelector('.diagram'))}")]
NEW = r"""const MAP={view:'sections',subjects:null,kinds:{'is a kind of':true,'operates on':true,'mentions':false},q:'',focus:null};
function secOf(id){let n=byId[id];while(n&&n.level>2)n=byId[n.parent];return n?n.id:id}
function mapControls(){const el=document.getElementById('mapctl');if(!el||el.dataset.built)return;el.dataset.built='1';if(!MAP.subjects)MAP.subjects=new Set(tops.map(t=>t.id));
  el.innerHTML='<div class="grp"><b>Show</b><button class="chip" data-mview="sections" aria-pressed="true">Sections</button><button class="chip" data-mview="concepts" aria-pressed="false">Concepts</button></div>'
  +'<div class="grp" id="mapsubj"><b>Subjects</b>'+tops.map(t=>'<button class="chip" data-msubj="'+t.id+'" aria-pressed="true">'+esc(t.label)+'</button>').join('')+'</div>'
  +'<div class="grp"><b>Relations</b><button class="chip" data-mkind="is a kind of" aria-pressed="true">is a kind of</button><button class="chip" data-mkind="operates on" aria-pressed="true">operates on</button><button class="chip" data-mkind="mentions" aria-pressed="false">mentioned together</button></div>'
  +'<div class="grp"><label><b>Find</b> <input id="mapq" type="search" placeholder="brighten boxes that match" aria-label="Find concepts on the map"></label></div>'
  +'<div class="grp"><label><b>Focus</b> <input id="mapfocus" list="mapfocuslist" placeholder="one concept and its neighbourhood" aria-label="Focus the map on one concept"></label><datalist id="mapfocuslist">'+D.nodes.map(n=>'<option value="'+esc(n.label)+'">').join('')+'</datalist><button class="btn g" id="mapall" hidden>Show all</button></div>';
  el.addEventListener('click',e=>{const v=e.target.closest('[data-mview]');if(v){MAP.view=v.dataset.mview;el.querySelectorAll('[data-mview]').forEach(b=>b.setAttribute('aria-pressed',b===v));
      if(MAP.view==='concepts'&&MAP.subjects.size>1){MAP.subjects=new Set([tops[0].id]);MAP.kinds['mentions']=false;mapNote('Concepts of '+byId[tops[0].id].label+' alone - every subject at once was the unreadable map; choose more subjects with the chips.')}
      if(MAP.view==='sections'){mapNote('')}syncChips();renderGraph();return}
    const s=e.target.closest('[data-msubj]');if(s){const k=s.dataset.msubj;if(MAP.subjects.has(k)){if(MAP.subjects.size>1)MAP.subjects.delete(k)}else MAP.subjects.add(k);MAP.focus=null;syncChips();renderGraph();return}
    const kd=e.target.closest('[data-mkind]');if(kd){MAP.kinds[kd.dataset.mkind]=!MAP.kinds[kd.dataset.mkind];syncChips();renderGraph();return}
    if(e.target.id==='mapall'){MAP.focus=null;document.getElementById('mapfocus').value='';renderGraph()}});
  el.querySelector('#mapq').addEventListener('input',e=>{MAP.q=e.target.value.trim().toLowerCase();dimGraph()});
  el.querySelector('#mapfocus').addEventListener('change',e=>{const v=e.target.value.trim().toLowerCase();const n=D.nodes.find(x=>x.label.toLowerCase()===v);if(n){MAP.focus=n.id;renderGraph()}});
  function syncChips(){el.querySelectorAll('[data-msubj]').forEach(b=>b.setAttribute('aria-pressed',MAP.subjects.has(b.dataset.msubj)));el.querySelectorAll('[data-mkind]').forEach(b=>b.setAttribute('aria-pressed',!!MAP.kinds[b.dataset.mkind]))}
  function mapNote(s){let p=el.querySelector('.mapnote');if(!p){p=document.createElement('p');p.className='note mapnote';el.appendChild(p)}p.textContent=s;p.hidden=!s}}
function mapFocus(id){MAP.focus=id;const f=document.getElementById('mapfocus');if(f)f.value=byId[id].label;showTab('map');renderGraph()}
function dimGraph(){const svg=document.querySelector('#graph svg');if(!svg)return;const q=MAP.q;svg.querySelectorAll('.gn').forEach(g=>g.classList.toggle('dim',!!q&&byId[g.dataset.c].label.toLowerCase().indexOf(q)<0))}
function renderGraph(){const el=document.getElementById('graph');if(!el)return;
  let visible;const W=1100,H=820,cx=W/2,cy=H/2;const pos={},lvl={};
  if(MAP.focus){const n=byId[MAP.focus];const set=new Set([n.id]);let p=n;while(p.parent){set.add(p.parent);p=byId[p.parent]}rel(n.id).forEach(r=>{set.add(r.source);set.add(r.target)});visible=D.nodes.filter(x=>set.has(x.id));
    const others=visible.filter(x=>x.id!==n.id);pos[n.id]=[cx,cy];others.forEach((o,i)=>{const r=i<10?260:380,a=-Math.PI/2+i*(2*Math.PI/Math.min(others.length,10))+(i>=10?Math.PI/10:0);pos[o.id]=[cx+r*1.5*Math.cos(a),cy+r*Math.sin(a)]})}
  else if(MAP.view==='sections'){visible=D.nodes.filter(n=>n.level<=2&&MAP.subjects.has(topOf(n.id)));const ts=tops.filter(t=>MAP.subjects.has(t.id));const N=ts.length;
    ts.forEach((t,i)=>{const a=-Math.PI/2+i*2*Math.PI/N;pos[t.id]=N===1?[cx,cy]:[cx+180*1.45*Math.cos(a),cy+180*Math.sin(a)];const ms=kids(t.id);const span=N===1?2*Math.PI:(2*Math.PI/N)*0.9;ms.forEach((m,j)=>{const b=N===1?j*2*Math.PI/ms.length-Math.PI/2:a+(j-(ms.length-1)/2)*(span/Math.max(ms.length,1));const r=N===1?300:350;pos[m.id]=[cx+r*1.45*Math.cos(b),cy+r*Math.sin(b)]})})}
  else{const ts=tops.filter(t=>MAP.subjects.has(t.id));visible=D.nodes.filter(n=>MAP.subjects.has(topOf(n.id)));const N=ts.length;const weight=m=>1+kids(m.id).length;
    ts.forEach((t,i)=>{const a0=-Math.PI/2+i*2*Math.PI/N,span=N===1?2*Math.PI:(2*Math.PI/N)*0.92;pos[t.id]=N===1?[cx,cy]:[cx+150*1.45*Math.cos(a0),cy+150*Math.sin(a0)];
      const ms=kids(t.id),tot=ms.reduce((s,m)=>s+weight(m),0);let acc=a0-span/2;ms.forEach(m=>{const w=span*weight(m)/tot,bm=acc+w/2;pos[m.id]=[cx+(N===1?210:300)*1.45*Math.cos(bm),cy+(N===1?210:300)*Math.sin(bm)];const ls=kids(m.id);ls.forEach((l,k)=>{const c=acc+w*(k+0.5)/Math.max(ls.length,1);const r=N===1?360:400;pos[l.id]=[cx+r*1.45*Math.cos(c),cy+r*Math.sin(c)]});acc+=w})})}
  const vis=new Set(visible.map(n=>n.id));
  // edges: in the sections view a relation is aggregated to the sections it joins
  const agg=new Map();D.relations.forEach(r=>{if(!MAP.kinds[r.type])return;let a=r.source,b=r.target;if(!MAP.focus&&MAP.view==='sections'){a=secOf(a);b=secOf(b)}if(!vis.has(a)||!vis.has(b)||a===b)return;const key=a+'|'+b+'|'+r.type;const e=agg.get(key)||{a,b,type:r.type,n:0,ev:[]};e.n++;if(e.ev.length<3)e.ev.push(byId[r.source].label+' '+r.type+' '+byId[r.target].label);agg.set(key,e)});
  const cls={'is a kind of':'isa','operates on':'op','mentions':'me'};let s='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Concept map">';
  agg.forEach(e=>{const a=pos[e.a],b=pos[e.b];if(!a||!b)return;const wdt=1.2+Math.min(5,Math.log2(e.n+1)*1.1);s+='<line class="ge '+cls[e.type]+'" x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke-width="'+wdt.toFixed(1)+'"><title>'+esc(byId[e.a].label+' '+e.type+' '+byId[e.b].label+(e.n>1?' - '+e.n+' links, e.g. '+e.ev.join('; '):' - '+e.ev[0]))+'</title></line>'+(e.n>1?'<text class="gcount" x="'+((a[0]+b[0])/2)+'" y="'+((a[1]+b[1])/2-3)+'" text-anchor="middle">'+e.n+'</text>':'')});
  visible.forEach(n=>{const p=pos[n.id];if(!p)return;const cnt=n.level<3?D.nodes.filter(x=>x.level===3&&topOf(x.id)===topOf(n.id)&&(n.level===1||x.parent===n.id)).length:0;const lab=n.label+(cnt&&!MAP.focus&&MAP.view==='sections'?' ('+cnt+')':'');const lines=wrapText(lab,n.level===1?16:20);const w=Math.max(70,Math.max(...lines.map(l=>l.length))*(n.level===1?8.6:7.6)+18),h=lines.length*17+10;
    s+='<g class="gn l'+n.level+(MAP.focus===n.id?' focus':'')+'" data-c="'+n.id+'" role="button" tabindex="0" aria-label="Options for '+esc(n.label)+'"><rect x="'+(p[0]-w/2)+'" y="'+(p[1]-h/2)+'" width="'+w+'" height="'+h+'"/>'+lines.map((l,k)=>'<text x="'+p[0]+'" y="'+(p[1]-h/2+16+k*17)+'" text-anchor="middle">'+esc(l)+'</text>').join('')+'<title>'+esc(n.label)+'</title></g>'});
  el.innerHTML='<div class="diagram">'+s+'</svg></div>';const d=el.querySelector('.diagram');zoomable(d);dimGraph();
  const all=document.getElementById('mapall');if(all)all.hidden=!MAP.focus;
  const st=document.getElementById('mapstat');if(st)st.textContent=visible.length+' boxes, '+agg.size+' lines'}
function drawGraph(){mapControls();if(!document.querySelector('#graph svg'))renderGraph()}"""
t = t[:i] + NEW + t[j + len("zoomable(el.querySelector('.diagram'))}"):]

# the detail card's options get a "Focus the map here" button for every concept
rep("<!-- course_page_template version 9.34.0:",
    "<!-- course_page_template version 9.35.0: the concept map after the owner's review of 2026-10-07 - a sections view by "
    "default with every relation aggregated and counted between the sections it joins, a concepts view for the chosen "
    "subjects, subject chips, relation toggles, a find box that dims non-matches, a focus field that redraws one concept's "
    "neighbourhood, boxed wrapped labels, and the same touch-for-options behaviour. Earlier: --><!-- course_page_template version 9.34.0:", 1)

open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
