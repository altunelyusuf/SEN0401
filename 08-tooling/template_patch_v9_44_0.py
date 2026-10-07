#!/usr/bin/env python3
"""Patches course_page_template_v9_43_0.html into course_page_template_v9_44_0.html.

One subject, the third part of the owner's review of 2026-10-07 14:46: "use-case, sequence, activity, state and mindmap
diagrams would be added to the paragraph depending on the content. For example if there is a work flow like spending,
activity diagram, possible usages of bitcoin a use-case diagram, the life of a transaction a state diagram, etc. You can
match the narrative with appropriate diagram types. We need to add these mappings to our ontology as well so that it
would be reused later."

The mapping lives in CME (cme_narrative_diagram_v1_0_0.ttl: ten narrative patterns, each with the question it answers
and the diagram type it suggests) and the page data carries it as D.diagram_map; a chapter's authored diagrams arrive as
D.ndiag (sen0401_chNN_diagrams_v*.py, checked against the mapping and the chapter corpus by the data builder). 9.44.0
draws them: five renderers - activity (UML actions, decisions with guarded flows, initial and final nodes), use-case
(actors, use cases in the system boundary), state (states, events, initial and final), sequence (lifelines and messages
in time order) and mind map (root and branches) - each placed under the paragraph of every concept the diagram
accompanies, headed by the diagram type and its title, with an (i) that opens a card saying which narrative pattern was
recognised, the question it answers, and why this diagram type follows. Every diagram is zoomable and relocatable
(9.43.0): its nodes carry identifiers, its edges name their ends. Drawn on reveal, like the rest of a section.
"""
__version__ = "9.44.0"

SRC, DST = "course_page_template_v9_43_0.html", "course_page_template_v9_44_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# --- placement: a placeholder in every rich section and every level-2 section, filled on reveal ---
rep("function richInner(n,tag){return secHead(n,tag)+'<div class=\"cgrid\"><div class=\"ctext\">'+bodyHtml(n)+storychips(n)+'</div><div class=\"nbh\" data-nbhfor=\"'+n.id+'\"></div></div>'+secVis(n)+chartBox(n)+widget(n)}",
    "function richInner(n,tag){return secHead(n,tag)+'<div class=\"cgrid\"><div class=\"ctext\">'+bodyHtml(n)+storychips(n)+'</div><div class=\"nbh\" data-nbhfor=\"'+n.id+'\"></div></div>'+ndSlot(n)+secVis(n)+chartBox(n)+widget(n)}", 1)
rep("'>'+secHead(n,tag)+bodyHtml(n)+chartBox(n)+widget(n)+secVis(n)+'</section>'}",
    "'>'+secHead(n,tag)+bodyHtml(n)+(n.level<3?ndSlot(n):'')+chartBox(n)+widget(n)+secVis(n)+'</section>'}", 1)
# a section's own heading block (shown with its concepts) carries the section's diagrams too
rep("""aria-label="Show details of '+esc(m.label)+'">ⓘ</button></h3>'+bodyHtml(m)+secVis(m)+'</section>'}""",
    """aria-label="Show details of '+esc(m.label)+'">ⓘ</button></h3>'+bodyHtml(m)+ndSlot(m)+secVis(m)+'</section>'}""", 1)
rep("(root||panes).querySelectorAll('.nbh .diagram:not([data-z])').forEach(d=>{d.dataset.z='1';zoomable(d)})}",
    "(root||panes).querySelectorAll('.ndslot[data-ndfor]:not([data-done])').forEach(h=>{const sc=h.closest('section');if(sc&&sc.hidden)return;h.dataset.done='1';h.outerHTML=ndBoxes(h.dataset.ndfor)});ndOnce();(root||panes).querySelectorAll('.nbh .diagram:not([data-z]),.ndiag .diagram:not([data-z])').forEach(d=>{d.dataset.z='1';zoomable(d)})}", 1)

# --- the renderers ---
rep("function storychips(n){",
    r"""// ---------- narrative diagrams (9.44.0): the chapter's authored diagrams, each of the type the CME mapping gives its narrative pattern ----------
let ND_SEQ=0;const ND_LABEL={ActivityDiagram:'Activity diagram',UseCaseDiagram:'Use-case diagram',StateDiagram:'State diagram',SequenceDiagram:'Sequence diagram',MindMap:'Mind map'};
function ndFor(id){return (D.ndiag||[]).filter(g=>(g.concepts||[]).indexOf(id)>=0)}
function ndSlot(n){return ndFor(n.id).length?'<div class="ndslot" data-ndfor="'+n.id+'"></div>':''}
function ndBoxes(id){return ndFor(id).map(g=>{const R={ActivityDiagram:ndActivity,UseCaseDiagram:ndUsecase,StateDiagram:ndState,SequenceDiagram:ndSequence,MindMap:ndMindmap}[g.type];let svg='';try{svg=R?R(g.data,g.id+'-'+(++ND_SEQ)):''}catch(e){console.error(e);svg=''}if(!svg)return '';
  const m=(D.diagram_map||{})[g.pattern]||{};const lead=(ND_LABEL[g.type]||g.type)+': this passage is '+(m.label?'a '+m.label:'a '+g.pattern.toLowerCase())+' - it answers "'+(m.question||'')+'"';
  return '<div class="ndiag" data-nd="'+g.id+'"><div class="ndhead"><b>'+esc(ND_LABEL[g.type]||g.type)+'</b> · '+esc(g.title)+' <button class="ptip" data-ndwhy="'+g.id+'" title="'+esc(lead)+'" aria-label="Why this diagram">ⓘ why this diagram</button></div><div class="diagram small nd">'+svg+'</div></div>'}).join('')}
// one copy of a diagram per view: a diagram accompanying a section and its concepts is shown once, under the first of them that is visible
function ndOnce(){const seen=new Set();panes.querySelectorAll('.ndiag[data-nd]').forEach(d=>{d.hidden=false;const vis=d.getClientRects().length>0;if(!vis)return;if(seen.has(d.dataset.nd))d.hidden=true;else{seen.add(d.dataset.nd);d.hidden=false}})}
function ndCard(id){const g=(D.ndiag||[]).find(x=>x.id===id);if(!g)return;const m=(D.diagram_map||{})[g.pattern]||{},c=document.getElementById('card');c.hidden=false;
  c.innerHTML='<button class="close" data-close title="Close (Esc)" aria-label="Close">✕</button><h3>'+esc(ND_LABEL[g.type]||g.type)+': '+esc(g.title)+'</h3><p><b>Narrative pattern:</b> '+esc(m.label||g.pattern)+'. <b>The question it answers:</b> '+esc(m.question||'')+'</p><p><b>Why this diagram type:</b> '+esc(g.why||'')+'</p><p><b>The rule, from the CME ontology:</b> a passage recognised as '+esc(m.label||g.pattern)+' is drawn as '+esc((m.types||[]).map(k=>ND_LABEL[k]||k).join(' or ')||ND_LABEL[g.type])+' ('+esc(m.notation||'')+').</p><p class="note">Read from: '+esc(g.read_from||'')+'. Cue phrases of the pattern: '+esc((m.cues||[]).join(', '))+'.</p>';c.classList.add('open')}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('button[data-ndwhy]');if(b){e.stopImmediatePropagation();ndCard(b.dataset.ndwhy)}},true);
function ndW(s,f){return Math.max(60,String(s).length*(f||6.6)+22)}
function ndWrap(s,max){return wrapText(s,max||18)}
function ndTextBox(x,y,lines,cls){return lines.map((l,i)=>'<text class="'+(cls||'')+'" x="'+x+'" y="'+(y+i*14)+'" text-anchor="middle">'+esc(l)+'</text>').join('')}
function ndArrowDefs(k){return '<defs><marker id="nda-'+k+'" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="var(--ink)"/></marker></defs>'}
// the activity and state diagrams share one layout: the nodes in reading order (longest path from the start, back edges ignored) laid as a snake over a grid shaped like the room, so a long flow reads at full size; neighbours join by straight lines, a skip by an arc above, a loop by an arc below
function ndOrder(ids,edges,start){const depth={};const out={};ids.forEach(i=>out[i]=[]);edges.forEach(([a,b])=>{if(out[a])out[a].push(b)});const seen=new Set();const visit=(v,d,stack)=>{if(stack.has(v))return;if((depth[v]||0)>=d&&seen.has(v))return;seen.add(v);depth[v]=Math.max(depth[v]||0,d);stack.add(v);out[v].forEach(w=>visit(w,d+1,stack));stack.delete(v)};visit(start,0,new Set());ids.forEach(i=>{if(depth[i]===undefined)depth[i]=0});return ids.slice().sort((p,q)=>depth[p]-depth[q]||ids.indexOf(p)-ids.indexOf(q))}
function ndFlow(nodes,edges,k,aria,size){const ids=nodes.map(n=>n.id),order=ndOrder(ids,edges,'start'),n=order.length;const CW=206,RH=96;const C=Math.max(2,Math.min(n,Math.ceil(Math.sqrt(n*1.15)))),R=Math.ceil(n/C);const B={};
  order.forEach((id,i)=>{const r=Math.floor(i/C),c=r%2?C-1-(i%C):i%C;const nd=nodes.find(x=>x.id===id),d=size(nd);const cx=20+c*CW+CW/2,cy=16+r*RH+RH/2;B[id]={id,x:cx-d.w/2,y:cy-d.h/2,w:d.w,h:d.h,cx,cy,lines:d.lines,kind:nd.kind,i,r}});
  const hasBack=edges.some(([a,b])=>order.indexOf(b)<=order.indexOf(a)&&a!==b);const W=20+C*CW+(hasBack?90:20),H=16+R*RH+16;let s='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="'+aria+'">'+ndArrowDefs(k);
  const pt=(A,B2)=>{const dx=B2.cx-A.cx,dy=B2.cy-A.cy;if(Math.abs(dy)>Math.abs(dx)*1.2){const down=dy>0;return [[A.cx,down?A.y+A.h:A.y],[B2.cx,down?B2.y:B2.y+B2.h]]}const right=dx>0;return [[right?A.x+A.w:A.x,A.cy],[right?B2.x:B2.x+B2.w,B2.cy]]};
  edges.forEach(([a,b,g])=>{const A=B[a],Z=B[b];if(!A||!Z)return;const adj=Z.i===A.i+1,back=Z.i<=A.i;const [p1,p2]=pt(A,Z);let d,mx,my;let anchor='middle';if(adj){d='M'+p1[0]+' '+p1[1]+' L'+p2[0]+' '+p2[1];if(Math.abs(p2[1]-p1[1])>Math.abs(p2[0]-p1[0])){mx=p1[0]+8;my=(p1[1]+p2[1])/2+8;anchor='start'}else{mx=(p1[0]+p2[0])/2;my=Math.min(A.y,Z.y)-4}}else if(A.r!==Z.r&&back){const x1=A.x+A.w,x2=Z.x+Z.w,xo=Math.max(x1,x2)+CW*0.3;d='M'+x1+' '+A.cy+' C'+xo+' '+A.cy+' '+xo+' '+Z.cy+' '+x2+' '+Z.cy;mx=xo-CW*0.1;my=(A.cy+Z.cy)/2+4;anchor='start'}else if(A.r!==Z.r&&!back){const q1=[A.cx,A.y+A.h],q2=[Z.cx,Z.y];d='M'+q1[0]+' '+q1[1]+' L'+q2[0]+' '+q2[1];mx=(q1[0]+q2[0])/2+8;my=(q1[1]+q2[1])/2+4;anchor='start'}else{const q1=[A.cx,back?A.y+A.h:A.y],q2=[Z.cx,back?Z.y+Z.h:Z.y];const off=(back?1:-1)*(Math.abs(q2[0]-q1[0])>CW*1.5?RH*0.55:RH*0.42);const cx=(q1[0]+q2[0])/2,cy=(q1[1]+q2[1])/2+off;d='M'+q1[0]+' '+q1[1]+' Q'+cx+' '+cy+' '+q2[0]+' '+q2[1];mx=0.25*q1[0]+0.5*cx+0.25*q2[0];my=0.25*q1[1]+0.5*cy+0.25*q2[1]}
    s+='<path class="nde" data-a="'+a+'" data-b="'+b+'" d="'+d+'" fill="none" marker-end="url(#nda-'+k+')"/>'+(g?'<text class="ndl" data-a="'+a+'" data-b="'+b+'" x="'+mx+'" y="'+(my-4)+'" text-anchor="'+anchor+'">'+esc(g)+'</text>':'')});
  nodes.forEach(nd=>{const b=B[nd.id];s+='<g class="ndn k-'+nd.kind+'" data-gid="'+nd.id+'" tabindex="0" role="img" aria-label="'+esc(nd.label||nd.kind)+'">';if(nd.kind==='start')s+='<circle cx="'+b.cx+'" cy="'+b.cy+'" r="9" class="ndstart"/>';else if(nd.kind==='end')s+='<circle cx="'+b.cx+'" cy="'+b.cy+'" r="10" class="ndendo"/><circle cx="'+b.cx+'" cy="'+b.cy+'" r="6" class="ndstart"/>';else if(nd.kind==='decision')s+='<path d="M'+b.cx+' '+b.y+' L'+(b.x+b.w)+' '+b.cy+' L'+b.cx+' '+(b.y+b.h)+' L'+b.x+' '+b.cy+' Z"/>'+ndTextBox(b.cx,b.cy-(b.lines.length-1)*7+4,b.lines);else s+='<rect x="'+b.x+'" y="'+b.y+'" width="'+b.w+'" height="'+b.h+'" rx="'+(nd.kind==='state'?14:10)+'"/>'+ndTextBox(b.cx,b.y+16,b.lines);s+='</g>'});
  return s+'</svg>'}
function ndActivity(dt,k){const nodes=[{id:'start',label:'',kind:'start'}].concat((dt.nodes||[]).map(x=>Object.assign({kind:'action'},x))).concat([{id:'end',label:'',kind:'end'}]);const edges=(dt.flows||[]).map(f=>[f[0],f[1],f[2]||'']);
  return ndFlow(nodes,edges,k,'Activity diagram',nd=>{if(nd.kind==='start'||nd.kind==='end')return {w:22,h:22,lines:[]};const lines=ndWrap(nd.label,nd.kind==='decision'?16:24);const lw=Math.max(...lines.map(l=>l.length));return nd.kind==='decision'?{w:Math.min(196,Math.max(120,lw*7+44)),h:Math.max(56,lines.length*14+30),lines}:{w:Math.min(190,Math.max(100,lw*6.6+24)),h:lines.length*14+18,lines}})}
function ndState(dt,k){const states=(dt.states||[]).map(x=>typeof x==='string'?{id:x,label:x}:x);const nodes=[{id:'start',label:'',kind:'start'}].concat(states.map(x=>Object.assign({kind:'state'},x))).concat([{id:'end',label:'',kind:'end'}]);const edges=[['start',dt.initial,'']].concat((dt.transitions||[]).map(f=>[f[0],f[1],f[2]||''])).concat((dt.final||[]).map(f=>[f,'end','']));
  return ndFlow(nodes,edges,k,'State diagram',nd=>{if(nd.kind!=='state')return {w:22,h:22,lines:[]};const lines=ndWrap(nd.label,22);return {w:Math.min(190,Math.max(100,Math.max(...lines.map(l=>l.length))*6.6+26)),h:lines.length*14+18,lines}})}
function ndUsecase(dt,k){const actors=(dt.actors||[]).map(a=>typeof a==='string'?{id:a,label:a}:a),uc=(dt.usecases||[]).map(u=>typeof u==='string'?{id:u,label:u}:u),links=dt.links||[];const cols=uc.length>4?2:1,rows=Math.ceil(uc.length/cols);const UW=176,UH=54,AW=90,BW=cols*(UW+22)+22,BH=rows*(UH+16)+46;const left=actors.filter((a,i)=>i%2===0),right=actors.filter((a,i)=>i%2===1);const BX=AW+20;const H=Math.max(BH+40,Math.max(left.length,right.length)*84+40);const B={};const W=BX+BW+(right.length?AW+20:20);
  const placeActors=(list,x)=>list.forEach((a,i)=>{const cy=40+(H-70)*(list.length===1?0.5:i/(list.length-1));B[a.id]={id:a.id,x:x-22,y:cy-26,w:44,h:64,cx:x,cy,side:x<BX?1:-1}});placeActors(left,AW/2+10);placeActors(right,BX+BW+AW/2+10);
  uc.forEach((u,i)=>{const c=i%cols,r=Math.floor(i/cols);const cx=BX+22+c*(UW+22)+UW/2,cy=40+32+r*(UH+16)+UH/2;B[u.id]={id:u.id,x:cx-UW/2,y:cy-UH/2,w:UW,h:UH,cx,cy}});
  let s='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Use-case diagram">';s+='<rect class="ndsys" x="'+BX+'" y="30" width="'+BW+'" height="'+(H-50)+'" rx="8"/><text class="ndsyst" x="'+(BX+BW/2)+'" y="50" text-anchor="middle">'+esc(dt.system||'')+'</text>';
  // a link runs from the actor's side to the point of the ellipse that faces the actor, so it pierces nothing it joins
  links.forEach(([a,u])=>{const A=B[a],U=B[u];if(!A||!U)return;const x1=A.cx+A.side*14,y1=A.cy;const dx=U.cx-x1,dy=U.cy-y1,L=Math.hypot(dx,dy)||1,rx=U.w/2,ry=U.h/2;const t=1/Math.sqrt((dx/L)*(dx/L)/(rx*rx)+(dy/L)*(dy/L)/(ry*ry));const x2=U.cx-dx/L*t,y2=U.cy-dy/L*t;s+='<line class="nde" data-a="'+a+'" data-b="'+u+'" x1="'+x1+'" y1="'+y1+'" x2="'+x2.toFixed(1)+'" y2="'+y2.toFixed(1)+'"/>'});
  actors.forEach(a=>{const b=B[a.id];s+='<g class="ndn k-actor" data-gid="'+a.id+'" tabindex="0" role="img" aria-label="'+esc(a.label)+'"><rect class="hit" x="'+b.x+'" y="'+(b.y-4)+'" width="'+b.w+'" height="'+(b.h+30)+'"/><circle cx="'+b.cx+'" cy="'+(b.cy-18)+'" r="7"/><line x1="'+b.cx+'" y1="'+(b.cy-11)+'" x2="'+b.cx+'" y2="'+(b.cy+8)+'"/><line x1="'+(b.cx-12)+'" y1="'+(b.cy-4)+'" x2="'+(b.cx+12)+'" y2="'+(b.cy-4)+'"/><line x1="'+b.cx+'" y1="'+(b.cy+8)+'" x2="'+(b.cx-10)+'" y2="'+(b.cy+22)+'"/><line x1="'+b.cx+'" y1="'+(b.cy+8)+'" x2="'+(b.cx+10)+'" y2="'+(b.cy+22)+'"/>'+ndTextBox(b.cx,b.cy+38,ndWrap(a.label,14))+'</g>'});
  uc.forEach(u=>{const b=B[u.id];const lines=ndWrap(u.label,24);s+='<g class="ndn k-uc" data-gid="'+u.id+'" tabindex="0" role="img" aria-label="'+esc(u.label)+'"><ellipse cx="'+b.cx+'" cy="'+b.cy+'" rx="'+(b.w/2)+'" ry="'+(b.h/2)+'"/>'+ndTextBox(b.cx,b.cy-(lines.length-1)*7+4,lines)+'</g>'});
  return s+'</svg>'}
function ndSequence(dt,k){const P=(dt.participants||[]).map(p=>typeof p==='string'?{id:p,label:p}:p),M=dt.messages||[];const CW=150,TOP=44,RH=36;const W=P.length*CW+20,H=TOP+30+M.length*RH+20;const X={};P.forEach((p,i)=>X[p.id]=20+i*CW+CW/2);let s='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Sequence diagram">'+ndArrowDefs(k);
  P.forEach(p=>{const x=X[p.id];const lines=ndWrap(p.label,18);s+='<line class="ndlife" x1="'+x+'" y1="'+(TOP)+'" x2="'+x+'" y2="'+(H-10)+'"/><g class="ndn k-part" data-part="'+p.id+'" role="img" aria-label="'+esc(p.label)+'"><rect x="'+(x-62)+'" y="8" width="124" height="'+(lines.length*14+16)+'" rx="6"/>'+ndTextBox(x,24,lines)+'</g>'});
  M.forEach((m,i)=>{const [a,b,txt,kind]=m;const xa=X[a],xb=X[b];if(xa===undefined||xb===undefined)return;const y=TOP+30+i*RH;if(a===b){s+='<path class="nde'+(kind==='reply'?' reply':'')+'" d="M'+xa+' '+(y-6)+' H'+(xa+40)+' V'+(y+10)+' H'+(xa+4)+'" fill="none" marker-end="url(#nda-'+k+')"/><text class="ndl" x="'+(xa+46)+'" y="'+(y+2)+'">'+esc(txt)+'</text>'}else{s+='<line class="nde'+(kind==='reply'?' reply':'')+'" x1="'+xa+'" y1="'+y+'" x2="'+(xb+(xb>xa?-4:4))+'" y2="'+y+'" marker-end="url(#nda-'+k+')"/><text class="ndl" x="'+((xa+xb)/2)+'" y="'+(y-5)+'" text-anchor="middle">'+esc(txt)+'</text>'}});
  return s+'</svg>'}
function ndMindmap(dt,k){const br=dt.branches||[];const tones=['#D97A14','#2F6D62','#9A5A10','#5B6B9C','#7A8A3A','#A04A4A','#4A7A8A','#8A6A2A'];const LH=30;
  // the classic mind-map shape: branches alternate right and left of the root, each stacked with its children in a column further out, so nothing overlaps whatever the count
  const kh=c=>ndWrap(c,30).length*14+18;const blockH=b=>Math.max(LH,(b.children||[]).reduce((h,c)=>h+kh(c),0));const sides=[[],[]],load=[0,0];br.forEach((b,i)=>{const si=load[0]<=load[1]?0:1;sides[si].push(i);load[si]+=blockH(b)+22});const colH=side=>side.reduce((h,i)=>h+blockH(br[i])+22,0);const H=Math.max(300,colH(sides[0]),colH(sides[1]))+40;const W=1080,cx=W/2,cy=H/2;const B={};let s='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Mind map">';
  sides.forEach((side,si)=>{const dir=si===0?1:-1;let y=(H-colH(side))/2+11;side.forEach(i=>{const b=br[i],kids=b.children||[],block=blockH(b);const bx=cx+dir*200,by=y+block/2,id='b'+i,tone=tones[i%tones.length];B[id]={x:bx,y:by};let ky0=y;
    s+='<path class="ndm" data-a="root" data-b="'+id+'" d="M'+cx+' '+cy+' C'+(cx+dir*110)+' '+cy+' '+(bx-dir*110)+' '+by+' '+bx+' '+by+'" stroke="'+tone+'" fill="none"/>';
    kids.forEach((c,j)=>{const cid=id+'c'+j,kx=cx+dir*360,ky=ky0+kh(c)/2;ky0+=kh(c);B[cid]={x:kx,y:ky};s+='<path class="ndm thin" data-a="'+id+'" data-b="'+cid+'" d="M'+bx+' '+by+' C'+(bx+dir*60)+' '+by+' '+(kx-dir*60)+' '+ky+' '+kx+' '+ky+'" stroke="'+tone+'" fill="none"/>'});y+=block+22})});
  const box=(id,x,y,label,cls,max,tone,anchor)=>{const lines=ndWrap(label,max||22),w=Math.max(60,Math.max(...lines.map(l=>l.length))*6.6+18),h=lines.length*14+12;const x0=anchor===1?x:anchor===-1?x-w:x-w/2;return '<g class="ndn '+cls+'" data-gid="'+id+'" tabindex="0" role="img" aria-label="'+esc(label)+'"><rect x="'+x0+'" y="'+(y-h/2)+'" width="'+w+'" height="'+h+'" rx="8"'+(tone?' style="stroke:'+tone+'"':'')+'/>'+ndTextBox(x0+w/2,y-(lines.length-1)*7+4,lines)+'</g>'};
  br.forEach((b,i)=>{const id='b'+i,p=B[id],tone=tones[i%tones.length],dir=sides[0].indexOf(i)>=0?1:-1;(b.children||[]).forEach((c,j)=>{const q=B[id+'c'+j];s+=box(id+'c'+j,q.x,q.y,c,'k-leaf',30,tone,dir)});s+=box(id,p.x,p.y,b.label,'k-branch',18,tone,0)});
  s+=box('root',cx,cy,dt.root||'',' k-root',18,null,0);return s+'</svg>'}
function storychips(n){""", 1)

# --- styles ---
rep("</style>", """.ndiag{margin:.5rem 0 .3rem}.ndhead{display:flex;flex-wrap:wrap;gap:.3rem .6rem;align-items:center;font-size:.92rem;margin:.1rem 0 .25rem}.ndhead .ptip{margin-left:auto}
.ndiag .diagram.nd{background:var(--panel);border:1px solid var(--line);border-radius:8px;height:19rem;min-height:9rem;resize:vertical;overflow:hidden}
.nd .ndn rect,.nd .ndn ellipse,.nd .ndn path{fill:var(--card);stroke:var(--ink);stroke-width:1.3}.nd .ndn.k-root rect{fill:var(--navy);stroke:var(--navy)}.nd .ndn.k-root text{fill:#fff;font-weight:700}.nd .ndn.k-branch rect{fill:var(--band);stroke-width:2}.nd .ndn.k-decision path{fill:var(--yellow)}.nd .ndn.k-uc ellipse{fill:var(--bg)}.nd .ndn.k-part rect{fill:var(--band)}
.nd .ndn text{font:12px Calibri,Arial,sans-serif;fill:var(--ink);pointer-events:none}.nd .ndn{cursor:grab}.nd .ndn:focus-visible rect,.nd .ndn:focus-visible ellipse{stroke:var(--blue);stroke-width:3}
.nd .ndn.k-actor rect.hit{fill:transparent;stroke:none}.nd .ndstart{fill:var(--ink)}.nd .ndendo{fill:none;stroke:var(--ink);stroke-width:1.5}.nd .k-actor circle,.nd .k-actor line{stroke:var(--ink);stroke-width:1.6;fill:none}
.nd .nde{stroke:var(--ink);stroke-width:1.4}.nd .nde.reply{stroke-dasharray:5 4}.nd .ndl{font:italic 11px Calibri,Arial,sans-serif;fill:var(--mute)}.nd .ndlife{stroke:var(--line);stroke-dasharray:4 4}.nd .ndsys{fill:none;stroke:var(--mute);stroke-dasharray:6 4}.nd .ndsyst{font:700 12px Calibri,Arial,sans-serif;fill:var(--mute);letter-spacing:.05em}
.nd .ndm{stroke-width:3;opacity:.8}.nd .ndm.thin{stroke-width:1.6}
</style>""", 1)
# the agents' knowledge graph indexes every Turtle block; the standard gets its label
rep("KIND_LABEL={book:'Book',course:'Course',chapter:'Chapter ontology',research:'Research',page:'This page'};", "KIND_LABEL={book:'Book',course:'Course',chapter:'Chapter ontology',research:'Research',page:'This page',standard:'CME standard'};", 1)
rep("<!-- course_page_template version 9.43.0:",
    "<!-- course_page_template version 9.44.0: narrative-matched diagrams - the chapter's authored activity, use-case, "
    "state, sequence and mind-map diagrams (typed by the CME narrative-to-diagram mapping) drawn under the paragraphs of "
    "the concepts they accompany, each with a card saying which pattern was recognised and why the type follows; zoomable "
    "and relocatable. Earlier: --><!-- course_page_template version 9.43.0:", 1)
open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
