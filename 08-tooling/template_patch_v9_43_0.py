#!/usr/bin/env python3
"""Patches course_page_template_v9_42_0.html into course_page_template_v9_43_0.html.

One subject, the second sentence of the owner's review of 2026-10-07 14:46 on the relocate function: "The same would
be adapted to other diagrams as well."

9.42.0 gave the ERD its own relocate machinery. The other diagrams of the page are drawn by five renderers with five
layouts (radial concept map, radial neighbourhood map, two left-to-right trees, the three-column ontology graph and the
class diagram), so 9.43.0 adds one renderer-independent relocate function instead of five: a diagram whose node groups
carry an identifier and whose edges name their two ends (data-a, data-b - the ontology graph already did; the concept
map, the neighbourhood map, the taxonomy, the ontology tree and the class diagram now do) can be rearranged by hand.
A pointer drag on a node moves its group and rewrites the geometry of every edge that touches it - lines by their end
points, paths by the end that moved (the start, the end, or a midpoint control follows the nearer end), count labels by
the mean of both ends; a tap without movement stays the click that opens the options. The concept map also gets Untangle
- a force-directed relocation from the current positions, run in short chunks - and Reset, in its control row. The
relocate function attaches itself wherever zoomable() does, so every diagram of the page relocates the same way.
"""
__version__ = "9.43.0"

SRC, DST = "course_page_template_v9_42_0.html", "course_page_template_v9_43_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# --- edges name their ends ---
rep("""s+='<line class="ge '+cls[e.type]+'" x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke-width="'+wdt.toFixed(1)+'">""",
    """s+='<line class="ge '+cls[e.type]+'" data-a="'+e.a+'" data-b="'+e.b+'" x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'" stroke-width="'+wdt.toFixed(1)+'">""", 1)
rep("""(e.n>1?'<text class="gcount" x="'+((a[0]+b[0])/2)+'" y="'+((a[1]+b[1])/2-3)+'" text-anchor="middle">'+e.n+'</text>':'')""",
    """(e.n>1?'<text class="gcount" data-a="'+e.a+'" data-b="'+e.b+'" x="'+((a[0]+b[0])/2)+'" y="'+((a[1]+b[1])/2-3)+'" text-anchor="middle">'+e.n+'</text>':'')""", 1)
rep("""s+='<path class="e" fill="none" d="M'+x1+' '+y1+' C'+mx+' '+y1+' '+mx+' '+y2+' '+x2+' '+y2+'"/>'}))""",
    """s+='<path class="e" data-a="'+(n.id||'root')+'" data-b="'+c.id+'" fill="none" d="M'+x1+' '+y1+' C'+mx+' '+y1+' '+mx+' '+y2+' '+x2+' '+y2+'"/>'}))""", 1)
rep("""s+='<path class="e" fill="none" d="M'+x1+' '+y1+' C'+mx+' '+y1+' '+mx+' '+y2+' '+x2+' '+y2+'"'+(c.kind==='book'?' stroke-dasharray="5 4"':'')+'/>'}))""",
    """s+='<path class="e" data-a="'+esc(n.id||'root')+'" data-b="'+esc(c.id)+'" fill="none" d="M'+x1+' '+y1+' C'+mx+' '+y1+' '+mx+' '+y2+' '+x2+' '+y2+'"'+(c.kind==='book'?' stroke-dasharray="5 4"':'')+'/>'}))""", 1)
rep("""s+='<line class="nbe '+cls+'" x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'">""",
    """s+='<line class="nbe '+cls+'" data-a="'+n.id+'" data-b="'+o.id+'" x1="'+a[0]+'" y1="'+a[1]+'" x2="'+b[0]+'" y2="'+b[1]+'">""", 1)
rep("""s+='<path class="oc-e" fill="none" marker-end="url(#oc-tri)" d="M'+x1+' '+y1+' H'+mx+' V'+y2+' H'+(x2+1)+'">""",
    """s+='<path class="oc-e" data-a="'+esc(c.n.id)+'" data-b="'+esc(t.n.id)+'" fill="none" marker-end="url(#oc-tri)" d="M'+x1+' '+y1+' H'+mx+' V'+y2+' H'+(x2+1)+'">""", 1)

# --- the relocate function, attached wherever zoomable() is ---
rep("svg.onpointerup=svg.onpointercancel=()=>{drag=null};host.classList.add('zoomhost')}",
    "svg.onpointerup=svg.onpointercancel=()=>{drag=null};host.classList.add('zoomhost');relocatable(host)}\n"
    + r"""// ---------- relocate: any diagram whose nodes carry an identifier and whose edges name their two ends can be rearranged by hand; the ERD has its own (9.42.0) ----------
const RL_NODE='g[data-c],g[data-gid],g[data-nbh],g[data-oid],g.n.root';
function rlId(g){return g.dataset.c||g.dataset.gid||g.dataset.nbh||g.dataset.oid||'root'}
function rlPath(d,A,B){const cmds=[];const re=/([MLCHVSQTZz])([^MLCHVSQTZz]*)/g;let m;while((m=re.exec(d)))cmds.push({c:m[1],v:(m[2].match(/-?[\d.]+(?:e-?\d+)?/g)||[]).map(Number)});
 let x=0,y=0,x0=null,y0=null;cmds.forEach(k=>{if(k.c==='H'){x=k.v[k.v.length-1]}else if(k.c==='V'){y=k.v[k.v.length-1]}else if(k.v.length>=2){x=k.v[k.v.length-2];y=k.v[k.v.length-1]}if(x0===null&&k.c==='M'){x0=x;y0=y}});const xe=x,ye=y,mx=(x0+xe)/2,my=(y0+ye)/2,n=cmds.length;
 const fx=(v,i)=>Math.abs(v-x0)<.6?v+A.dx:Math.abs(v-xe)<.6?v+B.dx:Math.abs(v-mx)<.6?v+(A.dx+B.dx)/2:v+(i<n/2?A.dx:B.dx),fy=(v,i)=>Math.abs(v-y0)<.6?v+A.dy:Math.abs(v-ye)<.6?v+B.dy:Math.abs(v-my)<.6?v+(A.dy+B.dy)/2:v+(i<n/2?A.dy:B.dy);
 return cmds.map((k,i)=>k.c+(k.c==='H'?k.v.map(v=>fx(v,i)):k.c==='V'?k.v.map(v=>fy(v,i)):k.v.map((v,j)=>j%2?fy(v,i):fx(v,i))).map(v=>Math.round(v*10)/10).join(' ')).join(' ')}
function relocatable(host){const svg=host.querySelector('svg');if(!svg||svg.dataset.rl||svg.querySelector('.oe-e'))return;const nodes=[...svg.querySelectorAll(RL_NODE)].filter(g=>!g.parentNode.closest(RL_NODE));if(!nodes.length)return;svg.dataset.rl='1';
 const N={};nodes.forEach(g=>{N[rlId(g)]={g,dx:0,dy:0}});const Z={dx:0,dy:0};
 const edges=[...svg.querySelectorAll('line[data-a],path[data-a],text[data-a]')].map(e=>({e,a:e.dataset.a,b:e.dataset.b,d:e.tagName==='path'?e.getAttribute('d'):null,x1:+e.getAttribute('x1'),y1:+e.getAttribute('y1'),x2:+e.getAttribute('x2'),y2:+e.getAttribute('y2'),x:+e.getAttribute('x'),y:+e.getAttribute('y')}));
 const adj={};edges.forEach(ed=>{(adj[ed.a]=adj[ed.a]||[]).push(ed);(adj[ed.b]=adj[ed.b]||[]).push(ed)});
 const redraw=ed=>{const A=N[ed.a]||Z,B=N[ed.b]||Z,e=ed.e;if(e.tagName==='line'){e.setAttribute('x1',ed.x1+A.dx);e.setAttribute('y1',ed.y1+A.dy);e.setAttribute('x2',ed.x2+B.dx);e.setAttribute('y2',ed.y2+B.dy)}else if(e.tagName==='text'){e.setAttribute('x',ed.x+(A.dx+B.dx)/2);e.setAttribute('y',ed.y+(A.dy+B.dy)/2)}else e.setAttribute('d',rlPath(ed.d,A,B))};
 const place=(id,dx,dy)=>{const n=N[id];if(!n)return;n.dx=dx;n.dy=dy;n.g.setAttribute('transform',dx||dy?'translate('+Math.round(dx*10)/10+','+Math.round(dy*10)/10+')':'');(adj[id]||[]).forEach(redraw)};
 svg.rlReset=()=>Object.keys(N).forEach(id=>place(id,0,0));
 svg.rlCenters=()=>Object.keys(N).map(id=>{const r=N[id].g.querySelector('rect,ellipse,circle');const b=r?r.getBBox():N[id].g.getBBox();return {id,x:b.x+b.width/2+N[id].dx,y:b.y+b.height/2+N[id].dy,w:b.width,h:b.height,fixed:N[id].g.classList.contains('focus')||N[id].g.classList.contains('me')}});
 svg.rlEdges=()=>edges.filter(e=>e.e.tagName!=='text'&&N[e.a]&&N[e.b]).map(e=>[e.a,e.b]);svg.rlPlace=place;
 let drag=null;svg.addEventListener('pointerdown',e=>{const g=e.target.closest(RL_NODE);if(!g||e.button||!svg.contains(g))return;const id=rlId(g);if(!N[id])return;const vb=svg.getAttribute('viewBox').split(/\s+/).map(Number),r=svg.getBoundingClientRect();drag={id,x:e.clientX,y:e.clientY,dx:N[id].dx,dy:N[id].dy,sx:vb[2]/r.width,sy:vb[3]/r.height,moved:false,pid:e.pointerId}});
 svg.addEventListener('pointermove',e=>{if(!drag||e.pointerId!==drag.pid)return;if(!drag.moved){if(Math.hypot(e.clientX-drag.x,e.clientY-drag.y)<4)return;drag.moved=true;try{svg.setPointerCapture(e.pointerId)}catch(x){}}place(drag.id,drag.dx+(e.clientX-drag.x)*drag.sx,drag.dy+(e.clientY-drag.y)*drag.sy)});
 const up=e=>{if(!drag||e.pointerId!==drag.pid)return;const was=drag.moved;drag=null;try{svg.releasePointerCapture(e.pointerId)}catch(x){}if(was)svg.dataset.moved=String(Date.now())};svg.addEventListener('pointerup',up);svg.addEventListener('pointercancel',up);
 svg.addEventListener('click',e=>{if(svg.dataset.moved&&Date.now()-Number(svg.dataset.moved)<500){e.stopPropagation();e.preventDefault()}},true);
 const note=host.previousElementSibling&&host.previousElementSibling.querySelector&&host.previousElementSibling.querySelector('.zbar .note, .note');if(note&&/drag moves/.test(note.textContent))note.textContent='wheel or pinch zooms · drag moves · drag a box to relocate it'}
// Untangle: a force-directed relocation from the current positions (repulsion between every two boxes, springs along the edges, a pull to the centre), run in short chunks, applied through the same relocate function
function rlUntangle(svg,done){if(!svg||!svg.rlCenters||svg.dataset.busy)return;const C=svg.rlCenters(),E=svg.rlEdges(),vb=svg.getAttribute('viewBox').split(/\s+/).map(Number),W=vb[2],H=vb[3];const ix={};C.forEach((c,i)=>{ix[c.id]=i;c.x0=c.x;c.y0=c.y});const k=110,L=190;let temp=18,it=0;svg.dataset.busy='1';
 // local forces only: boxes repel within two box-lengths, overlapping boxes push apart, a link longer than L pulls its ends together; the drawn shape is kept, the knots come out
 const step=()=>{const t0=performance.now();while(performance.now()-t0<25&&it<90){const F=C.map(()=>[0,0]);for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){const a=C[i],b=C[j];let dx=a.x-b.x,dy=a.y-b.y,d=Math.hypot(dx,dy)||0.1;if(d<2*k){const f=k*k/d*(1-d/(2*k));dx/=d;dy/=d;F[i][0]+=dx*f;F[i][1]+=dy*f;F[j][0]-=dx*f;F[j][1]-=dy*f}const px=(a.w+b.w)/2+12-Math.abs(a.x-b.x),py=(a.h+b.h)/2+12-Math.abs(a.y-b.y);if(px>0&&py>0){const sx=a.x>=b.x?1:-1,sy=a.y>=b.y?1:-1;if(px*(a.h+b.h)<py*(a.w+b.w)){F[i][0]+=sx*px;F[j][0]-=sx*px}else{F[i][1]+=sy*py;F[j][1]-=sy*py}}}
   E.forEach(([p,q])=>{const a=C[ix[p]],b=C[ix[q]];if(!a||!b)return;let dx=a.x-b.x,dy=a.y-b.y,d=Math.hypot(dx,dy)||0.1;if(d<=L)return;const f=(d-L)*0.4;dx/=d;dy/=d;F[ix[p]][0]-=dx*f;F[ix[p]][1]-=dy*f;F[ix[q]][0]+=dx*f;F[ix[q]][1]+=dy*f});
   C.forEach((c,i)=>{if(c.fixed)return;let fx=F[i][0],fy=F[i][1];const m=Math.hypot(fx,fy)||0.1,s=Math.min(m,temp)/m;c.x=Math.min(W-c.w/2,Math.max(c.w/2,c.x+fx*s));c.y=Math.min(H-c.h/2,Math.max(c.h/2,c.y+fy*s))});temp=Math.max(1,temp*0.97);it++}
  if(it<90){setTimeout(step,0);return}C.forEach(c=>svg.rlPlace(c.id,c.x-c.x0+(svg.rlDx(c.id)),c.y-c.y0+(svg.rlDy(c.id))));delete svg.dataset.busy;if(done)done()};setTimeout(step,0)}""", 1)
# the current offsets are needed to apply an untangle on top of what was already moved
rep("svg.rlEdges=()=>edges.filter(e=>e.e.tagName!=='text'&&N[e.a]&&N[e.b]).map(e=>[e.a,e.b]);svg.rlPlace=place;",
    "svg.rlEdges=()=>edges.filter(e=>e.e.tagName!=='text'&&N[e.a]&&N[e.b]).map(e=>[e.a,e.b]);svg.rlPlace=place;svg.rlDx=id=>N[id]?N[id].dx:0;svg.rlDy=id=>N[id]?N[id].dy:0;", 1)
# the concept map's control row: Relocate - Untangle, Reset
rep("""  +'<div class="grp"><label><b>Find</b> <input id="mapq" type="search" placeholder="brighten boxes that match" aria-label="Find concepts on the map"></label></div>'""",
    """  +'<div class="grp"><b>Relocate</b><button class="chip" data-mrl="untangle" title="Move the boxes apart along their links from where they are">Untangle</button><button class="chip" data-mrl="reset" title="Back to the drawn layout">Reset</button><span class="note">drag a box to move it</span></div>'
  +'<div class="grp"><label><b>Find</b> <input id="mapq" type="search" placeholder="brighten boxes that match" aria-label="Find concepts on the map"></label></div>'""", 1)
rep("""    const kd=e.target.closest('[data-mkind]');if(kd){MAP.kinds[kd.dataset.mkind]=!MAP.kinds[kd.dataset.mkind];syncChips();renderGraph();return}""",
    """    const kd=e.target.closest('[data-mkind]');if(kd){MAP.kinds[kd.dataset.mkind]=!MAP.kinds[kd.dataset.mkind];syncChips();renderGraph();return}
    const rl=e.target.closest('[data-mrl]');if(rl){const svg=document.querySelector('#graph svg');if(!svg)return;if(rl.dataset.mrl==='reset'&&svg.rlReset)svg.rlReset();if(rl.dataset.mrl==='untangle')rlUntangle(svg);return}""", 1)
rep("<!-- course_page_template version 9.42.0:",
    "<!-- course_page_template version 9.43.0: the relocate function reaches every diagram - a renderer-independent "
    "drag that moves a node and rewrites the edges naming it (concept map, neighbourhood map, taxonomy, ontology tree, "
    "ontology graph, class diagram), with Untangle (force-directed, chunked) and Reset on the concept map. Earlier: "
    "--><!-- course_page_template version 9.42.0:", 1)
open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
