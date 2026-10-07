#!/usr/bin/env python3
"""Patches course_page_template_v9_41_0.html into course_page_template_v9_42_0.html.

One subject, the owner's review of 2026-10-07 14:46: "ERD, when filled the readability is reduced. We need a relocate
function to solve the over-display and label visibility problems including other visualization problems as well."

Measured first, on the 9.40.0 chapter 1 page at 1366x768 (scratchpad erd_probe.py): the sections view draws 21 entities
and 139 relationships on a fixed 4-column grid, every line leaving the midpoint of a box side and every label sitting at
the midpoint of its line - 469 pairs of overlapping labels, 68 labels drawn over an entity, 94 lines running through an
entity they do not connect, and the 990x1282 canvas fitted into a 716x444 room renders the label text 5 px tall. The
subjects view: 29 relationships, 106 overlapping label pairs, 12 over an entity.

9.42.0, the relocate function for the ERD (the same machinery is adapted to the other diagrams in 9.43.0):
- the entities are draggable (pointer drag, mouse or touch); the lines and labels follow, and the canvas regrows to
  what was placed; a drag is not a click, so the entity card opens on a tap only;
- Untangle: an automatic relocation on the same grid that swaps entities until the weighted connection length and
  the number of lines crossing unrelated entities stop falling; Wider/Tighter change the spacing; Reset layout returns
  to the grouped grid;
- the grid takes the room's shape (columns from the diagram's own width and height), so the canvas is no longer a
  tall strip shrunk into a wide room;
- lines leave a box side at distinct points spread along the side instead of one bundle at the midpoint;
- labels are placed where they fit - eleven candidate points along each line and a step or two to either side, never
  over an entity or another label; a label with no free spot shrinks to its count, and if the count finds no spot
  either it is left out of the fitted view (the relationship keeps its tooltip, and its label appears on choice); a
  Labels control offers all / fitted (default) / on choice (shown only for the chosen entity);
- choosing an entity lifts its relationships and labels and dims the rest, so a single entity reads in a full diagram.
"""
__version__ = "9.42.0"

SRC, DST = "course_page_template_v9_41_0.html", "course_page_template_v9_42_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# --- the model: positions come from the grid unless relocated; the grid takes the room's shape; spacing scales ---
rep("const ERD={mode:'subjects',mentions:true};", "const ERD={mode:'subjects',mentions:true};const ERD_LAY={pos:{},spread:1,labels:'auto',sel:null,drag:null};", 1)
rep("  const COLS=lvl===1?3:4,BW=170,GX=60,GY=50;const ENT={},REL=[];",
    "  const BW=170,GX=Math.round(60*ERD_LAY.spread),GY=Math.round(50*ERD_LAY.spread),COLS=erdCols(ents.length,BW+GX,30+7*16+10+GY);const ENT={},REL=[];const P=ERD_LAY.pos[ERD.mode]||{};", 1)
rep("ENT[e.id]={x:20+(i%COLS)*(BW+GX),y:30+Math.floor(i/COLS)*(30+7*16+10+GY),label:e.label,",
    "ENT[e.id]={x:P[e.id]?P[e.id].x:20+(i%COLS)*(BW+GX),y:P[e.id]?P[e.id].y:30+Math.floor(i/COLS)*(30+7*16+10+GY),label:e.label,", 1)
rep("agg.forEach(e=>REL.push([e.a,e.b,e.as.size>1?'many':'one',e.bs.size>1?'many':'one',(e.type==='mentions'?'mentioned with':'operates on')+' ×'+e.n,e.ev]));",
    "agg.forEach(e=>REL.push([e.a,e.b,e.as.size>1?'many':'one',e.bs.size>1?'many':'one',(e.type==='mentions'?'mentioned with':'operates on')+' ×'+e.n,e.ev,e.n]));", 1)
rep("function erdApply(){erdLegend();if(ERD.mode==='schema'){OE_ENT=OE_SCHEMA_ENT;OE_REL=OE_SCHEMA_REL;return {W:990,H:400}}const m=cerdModel();OE_ENT=m.ENT;OE_REL=m.REL;return {W:Math.max(990,20+m.cols*(m.bw+m.gx)),H:30+m.rows*(30+7*16+10+m.gy)+40}}",
    "function erdCols(n,cw,ch){const host=document.getElementById('oerd');const w=(host&&host.clientWidth)||990,top=host?host.getBoundingClientRect().top:0,h=Math.max(300,window.innerHeight-top-40);return Math.max(2,Math.min(n,Math.ceil(Math.sqrt(n*(w/h)*(ch/cw)))))}\n"
    "function erdApply(){erdLegend();if(ERD.mode==='schema'){const P=ERD_LAY.pos.schema||{};OE_ENT={};Object.keys(OE_SCHEMA_ENT).forEach(k=>{OE_ENT[k]=Object.assign({},OE_SCHEMA_ENT[k],P[k]||{})});OE_REL=OE_SCHEMA_REL;return erdExtent(160)}const m=cerdModel();OE_ENT=m.ENT;OE_REL=m.REL;return erdExtent(170)}\n"
    "function erdExtent(BW){let W=0,H=0;Object.values(OE_ENT).forEach(e=>{W=Math.max(W,e.x+BW+30);H=Math.max(H,e.y+30+e.attrs.length*16+10+50)});return {W:Math.max(600,W),H:Math.max(240,H)}}", 1)

# --- the controls: relocate (Untangle, Wider, Tighter, Reset layout) and Labels (all / fitted / on choice) ---
rep("""<div class="grp"><b>Relationships</b><button class="chip" data-erdm="1" aria-pressed="true">mentioned together</button></div>';""",
    """<div class="grp"><b>Relationships</b><button class="chip" data-erdm="1" aria-pressed="true">mentioned together</button></div><div class="grp"><b>Relocate</b><button class="chip" data-erdl="untangle" title="Swap entities on the grid until the connections are shortest and cross the fewest unrelated entities">Untangle</button><button class="chip" data-erdl="wider" title="More room between entities">Wider</button><button class="chip" data-erdl="tighter" title="Less room between entities">Tighter</button><button class="chip" data-erdl="reset" title="Back to the grouped grid">Reset layout</button><span class="note">drag an entity to move it</span></div><div class="grp"><b>Labels</b><button class="chip" data-erdlab="all" aria-pressed="false" title="Every label in full, even where labels overlap">all</button><button class="chip" data-erdlab="auto" aria-pressed="true" title="Full where a label fits, its count where it does not">fitted</button><button class="chip" data-erdlab="hover" aria-pressed="false" title="Only the chosen entity\\'s labels">on choice</button></div>';""", 1)
rep("""    const m=e.target.closest('[data-erdm]');if(m){ERD.mentions=!ERD.mentions;m.setAttribute('aria-pressed',ERD.mentions);document.getElementById('oerd').innerHTML='';drawOerd()}})}""",
    """    const m=e.target.closest('[data-erdm]');if(m){ERD.mentions=!ERD.mentions;m.setAttribute('aria-pressed',ERD.mentions);document.getElementById('oerd').innerHTML='';drawOerd();return}
    const l=e.target.closest('[data-erdl]');if(l){const k=l.dataset.erdl;if(k==='untangle'){erdUntangle();return}if(k==='wider'||k==='tighter'){const s0=ERD_LAY.spread;ERD_LAY.spread=k==='wider'?Math.min(2.5,s0*1.25):Math.max(0.5,s0/1.25);if(ERD_LAY.pos[ERD.mode])ERD_LAY.pos[ERD.mode]=erdScaled(ERD_LAY.pos[ERD.mode],s0,ERD_LAY.spread)}if(k==='reset'){ERD_LAY.spread=1;delete ERD_LAY.pos[ERD.mode]}document.getElementById('oerd').innerHTML='';drawOerd();return}
    const lb=e.target.closest('[data-erdlab]');if(lb){ERD_LAY.labels=lb.dataset.erdlab;el.querySelectorAll('[data-erdlab]').forEach(x=>x.setAttribute('aria-pressed',x===lb));erdRender();return}})}
// wider/tighter keep a relocated layout: the positions scale with the spacing
function erdScaled(P,s0,s1){const out={};Object.keys(P).forEach(k=>{out[k]={x:Math.round(20+(P[k].x-20)*(170+60*s1)/(170+60*s0)),y:Math.round(30+(P[k].y-30)*(162+50*s1)/(162+50*s0))}});return out}
// Untangle: the entities keep their grid slots as a set; pairs swap while the weighted connection length plus a penalty for every line crossing an unrelated entity falls
function erdUntangle(){const ids=Object.keys(OE_ENT);if(ids.length<3||ERD_LAY.busy)return;const BW=ERD.mode==='schema'?160:170;const slots=ids.map(k=>({x:OE_ENT[k].x,y:OE_ENT[k].y}));const hgt=k=>30+OE_ENT[k].attrs.length*16+10;let at={};ids.forEach((k,i)=>at[k]=i);
  const cost=()=>{let c=0;const B={};ids.forEach(k=>{const s=slots[at[k]],h=hgt(k);B[k]={l:s.x,t:s.y,r:s.x+BW,b:s.y+h,cx:s.x+BW/2,cy:s.y+h/2}});
    OE_REL.forEach(r=>{const A=B[r[0]],Z=B[r[1]],w=r[6]||1;c+=w*(Math.abs(A.cx-Z.cx)+Math.abs(A.cy-Z.cy))/100;ids.forEach(k=>{if(k===r[0]||k===r[1])return;const b=B[k];for(let s=.1;s<.95;s+=.1){const x=A.cx+(Z.cx-A.cx)*s,y=A.cy+(Z.cy-A.cy)*s;if(x>b.l&&x<b.r&&y>b.t&&y<b.b){c+=12*w;break}}})});return c};
  // the swap passes run in short chunks (one row of pairs each) so the page stays responsive; the result is applied once
  let best=cost(),pass=0,i=0,moved=false;ERD_LAY.busy=true;const info=document.getElementById('oerdinfo');if(info)info.innerHTML='<p class="note">relocating…</p>';
  const step=()=>{const t0=performance.now();while(performance.now()-t0<30){if(i>=ids.length){if(!moved||++pass>=12){finish();return}i=0;moved=false}const a=ids[i];for(let j=i+1;j<ids.length;j++){const b=ids[j];const t1=at[a];at[a]=at[b];at[b]=t1;const c=cost();if(c<best-1e-9){best=c;moved=true}else{at[b]=at[a];at[a]=t1}}i++}setTimeout(step,0)};
  const finish=()=>{const P={};ids.forEach(k=>P[k]={x:slots[at[k]].x,y:slots[at[k]].y});ERD_LAY.pos[ERD.mode]=P;ERD_LAY.busy=false;document.getElementById('oerd').innerHTML='';if(info)info.textContent='Choose an entity to see what it holds.';drawOerd()};setTimeout(step,0)}""", 1)

# --- the drawing: anchors spread along the sides, labels placed where they fit, a draggable canvas that regrows ---
i = t.find("async function drawOerd(){"); j = t.find("setTimeout(fitViews,30)}", i) + len("setTimeout(fitViews,30)}")
assert i > 0 and j > i and t.count("async function drawOerd(){") == 1
NEW = r"""async function drawOerd(){const el=document.getElementById('oerd');if(!el)return;erdControls();erdApply();if(ERD.mode==='schema'){await ogFacts();try{await ontoLoad()}catch(e){}}
 const dims=erdExtent(ERD.mode==='schema'?160:170);const keep=el.querySelector('svg')?el.querySelector('svg').getAttribute('viewBox'):null;
 el.innerHTML='<div class="diagram"><svg viewBox="0 0 '+dims.W+' '+dims.H+'" role="group" aria-label="Entity-relationship diagram of the ontology" data-h="'+dims.H+'"'+(keep?' data-vbkeep="'+keep+'"':'')+'></svg></div>';erdRender();const d=el.querySelector('.diagram');zoomable(d);erdDrag(d.querySelector('svg'));setTimeout(fitViews,30)}
function erdBoxes(){const BW=ERD.mode==='schema'?160:170,LH=16;const B={};Object.keys(OE_ENT).forEach(k=>{const e=OE_ENT[k];B[k]={x:e.x,y:e.y,w:BW,h:30+e.attrs.length*LH+10}});return B}
// every relationship gets its own point on a box side: the lines of one side are spread along it in the order of where they go
function erdAnchors(B){const side={};const use=[];OE_REL.forEach((r,i)=>{const A=B[r[0]],Z=B[r[1]];const ax=A.x+A.w/2,ay=A.y+A.h/2,bx=Z.x+Z.w/2,by=Z.y+Z.h/2;let s1,s2;if(Math.abs(ax-bx)>Math.abs(ay-by)){const right=bx>ax;s1=right?'r':'l';s2=right?'l':'r'}else{const down=by>ay;s1=down?'b':'t';s2=down?'t':'b'}use.push({i,a:r[0],b:r[1],s1,s2});(side[r[0]+s1]=side[r[0]+s1]||[]).push({i,end:0,o:s1==='l'||s1==='r'?by:bx});(side[r[1]+s2]=side[r[1]+s2]||[]).push({i,end:1,o:s2==='l'||s2==='r'?ay:ax})});
  const pt={};Object.keys(side).forEach(key=>{const k=key.slice(0,-1),s=key.slice(-1),L=side[key].sort((p,q)=>p.o-q.o),b=B[k];L.forEach((p,n)=>{const f=(n+1)/(L.length+1);const P=s==='l'?[b.x,b.y+b.h*f]:s==='r'?[b.x+b.w,b.y+b.h*f]:s==='t'?[b.x+b.w*f,b.y]:[b.x+b.w*f,b.y+b.h];pt[p.i+':'+p.end]=P})});
  return use.map(u=>{const d=s=>s==='l'?[-1,0]:s==='r'?[1,0]:s==='t'?[0,-1]:[0,1];return {i:u.i,p1:pt[u.i+':0'],p2:pt[u.i+':1'],d1:d(u.s1),d2:d(u.s2)}})}
function erdRender(){const el=document.getElementById('oerd'),svg=el&&el.querySelector('svg');if(!svg)return;const B=erdBoxes(),LH=16,H=parseFloat(svg.dataset.h);const sel=ERD_LAY.sel;let s='';
 const anchors=erdAnchors(B);const ov=(a,b)=>!(a.x+a.w<=b.x||b.x+b.w<=a.x||a.y+a.h<=b.y||b.y+b.h<=a.y);const boxes=Object.values(B);const placed=[];
 // the chosen entity's relationships are drawn last and labelled first, so they read over the rest
 const order=anchors.slice().sort((p,q)=>{const ps=sel&&(OE_REL[p.i][0]===sel||OE_REL[p.i][1]===sel)?1:0,qs=sel&&(OE_REL[q.i][0]===sel||OE_REL[q.i][1]===sel)?1:0;return ps-qs});
 order.forEach(u=>{const [a,b,ca,cb,verb,ev]=OE_REL[u.i];const on=sel?(a===sel||b===sel):false;const cls=(/^mentioned/.test(verb)?' oe-me':'')+(sel?(on?' sel':' dim'):'');
  s+='<g class="oe-r'+cls+'" data-a="'+a+'" data-b="'+b+'"><title>'+esc(OE_ENT[a].label+' '+verb+' '+OE_ENT[b].label+(ev&&ev.length?' - e.g. '+ev.join('; '):''))+'</title><line x1="'+u.p1[0]+'" y1="'+u.p1[1]+'" x2="'+u.p2[0]+'" y2="'+u.p2[1]+'"/>'+oeGlyph(u.p1[0],u.p1[1],u.d1[0],u.d1[1],ca)+oeGlyph(u.p2[0],u.p2[1],u.d2[0],u.d2[1],cb)+'</g>'});
 // labels: seven candidate points along the line, the first that is over no entity and no placed label; none free -> the count alone
 const labs=order.slice().reverse();labs.forEach(u=>{const [a,b,ca,cb,verb,ev]=OE_REL[u.i];const on=sel?(a===sel||b===sel):false;const full=ERD_LAY.labels==='all'||on;const short=(verb.match(/×\d+/)||['·'])[0],txt=(/^mentioned/.test(verb)&&!full)?short:verb;const dim=w=>({w:w*6.8+12,h:20});let pick=null,text=txt;
  const L=Math.hypot(u.p2[0]-u.p1[0],u.p2[1]-u.p1[1])||1,nx=-(u.p2[1]-u.p1[1])/L,ny=(u.p2[0]-u.p1[0])/L;const spot=(f,o,len)=>{const mx=u.p1[0]+(u.p2[0]-u.p1[0])*f+nx*o,my=u.p1[1]+(u.p2[1]-u.p1[1])*f+ny*o,d=dim(len),r={x:mx-d.w/2,y:my-d.h/2,w:d.w,h:d.h};return boxes.some(bx=>ov(r,bx))||placed.some(p=>ov(r,p))?null:r};
  const F=[0.5,0.42,0.58,0.34,0.66,0.26,0.74,0.18,0.82,0.1,0.9],O=[0,14,-14,28,-28];for(const o of O){for(const f of F){pick=spot(f,o,txt.length);if(pick)break}if(pick)break}
  if(!pick&&!full){text=short;for(const o of O){for(const f of F){pick=spot(f,o,text.length);if(pick)break}if(pick)break}}
  // fitted mode: a label with no free spot is left out rather than drawn over something (the relationship keeps its tooltip and shows its label on choice); all mode draws it anyway
  if(!pick){if(!full)return;const d=dim(text.length);pick={x:(u.p1[0]+u.p2[0])/2-d.w/2,y:(u.p1[1]+u.p2[1])/2-d.h/2,w:d.w,h:d.h,crowded:true}}
  placed.push(pick);const cls='oe-l'+(text!==txt?' oe-vc':'')+(pick.crowded?' oe-vx':'')+(sel?(on?' sel':' dim'):'');
  s+='<g class="'+cls+'" data-a="'+a+'" data-b="'+b+'"><title>'+esc(OE_ENT[a].label+' '+verb+' '+OE_ENT[b].label)+'</title><rect class="oe-v" x="'+pick.x+'" y="'+pick.y+'" width="'+pick.w+'" height="'+pick.h+'" rx="10"/><text class="oe-vt" x="'+(pick.x+pick.w/2)+'" y="'+(pick.y+14)+'" text-anchor="middle">'+esc(text)+'</text></g>'});
 Object.keys(OE_ENT).forEach(k=>{const e=OE_ENT[k],b=B[k];s+='<g class="oe-e'+(sel===k?' sel':'')+'" data-ent="'+k+'" tabindex="0" role="button" aria-label="'+esc(e.label)+', '+e.n()+' in this chapter; drag to move"><rect x="'+b.x+'" y="'+b.y+'" width="'+b.w+'" height="'+b.h+'" rx="6"/><rect class="oe-hd" x="'+b.x+'" y="'+b.y+'" width="'+b.w+'" height="26" rx="6"'+(e.tone?' style="fill:'+e.tone+'"':'')+'/><text class="oe-t" x="'+(b.x+b.w/2)+'" y="'+(b.y+18)+'" text-anchor="middle">'+esc(e.label)+' ('+e.n()+')</text>'+e.attrs.map((a,i)=>'<text x="'+(b.x+10)+'" y="'+(b.y+26+LH*(i+1))+'">'+(i===0?'◆ ':'· ')+esc(a)+'</text>').join('')+'</g>'});
 s+='<g class="oe-key" transform="translate(20,'+(H-15)+')"><text x="0" y="0">'+(ERD.mode==='schema'?'Key: | one · crow’s foot many · ○ optional. Each line reads from either end, for example one subject contains many topics; one concept is shown by zero or more examples.':'Key: | one · crow’s foot many. A side is many when more than one concept of that entity takes part; the verb carries the count of concept-level links. Drag an entity to move it.')+'</text></g>';
 svg.innerHTML=s;svg.classList.toggle('has-sel',!!sel);svg.classList.toggle('lab-hover',ERD_LAY.labels==='hover')}
// relocate by hand: a pointer drag on an entity moves it in canvas units; the lines and labels follow; a tap without movement is the click that opens the card
function erdDrag(svg){svg.addEventListener('pointerdown',e=>{const g=e.target.closest('.oe-e');if(!g||e.button)return;const vb=svg.getAttribute('viewBox').split(/\s+/).map(Number),r=svg.getBoundingClientRect(),k=g.dataset.ent;ERD_LAY.drag={k,x:e.clientX,y:e.clientY,ox:OE_ENT[k].x,oy:OE_ENT[k].y,sx:vb[2]/r.width,sy:vb[3]/r.height,moved:false,id:e.pointerId}});
 svg.addEventListener('pointermove',e=>{const d=ERD_LAY.drag;if(!d||e.pointerId!==d.id)return;const dx=(e.clientX-d.x)*d.sx,dy=(e.clientY-d.y)*d.sy;if(!d.moved&&Math.hypot(e.clientX-d.x,e.clientY-d.y)<4)return;if(!d.moved){d.moved=true;try{svg.setPointerCapture(e.pointerId)}catch(x){}}OE_ENT[d.k].x=Math.max(0,Math.round(d.ox+dx));OE_ENT[d.k].y=Math.max(0,Math.round(d.oy+dy));if(!d.raf)d.raf=requestAnimationFrame(()=>{d.raf=0;erdRender();const g=svg.querySelector('.oe-e[data-ent="'+d.k+'"]');if(g)g.classList.add('drag')})});
 const up=e=>{const d=ERD_LAY.drag;if(!d||e.pointerId!==d.id)return;ERD_LAY.drag=null;try{svg.releasePointerCapture(e.pointerId)}catch(x){}if(!d.moved)return;ERD_LAY.pos[ERD.mode]=ERD_LAY.pos[ERD.mode]||{};Object.keys(OE_ENT).forEach(k=>ERD_LAY.pos[ERD.mode][k]={x:OE_ENT[k].x,y:OE_ENT[k].y});ERD_LAY.justDragged=Date.now();drawOerd()};
 svg.addEventListener('pointerup',up);svg.addEventListener('pointercancel',up)}"""
t = t[:i] + NEW + t[j:]
rep("if(b){ERD.mode=b.dataset.erd;el.querySelectorAll('[data-erd]')", "if(b){ERD.mode=b.dataset.erd;ERD_LAY.sel=null;el.querySelectorAll('[data-erd]')", 1)
# the entity card: the choice also lifts the entity's relationships; a drag that just ended is not a choice
rep("function oeInfo(k){const e=OE_ENT[k];document.querySelectorAll('#oerd .oe-e').forEach(x=>x.classList.toggle('sel',x.dataset.ent===k));",
    "function oeInfo(k){if(ERD_LAY.justDragged&&Date.now()-ERD_LAY.justDragged<400)return;const e=OE_ENT[k];ERD_LAY.sel=k;erdRender();", 1)
rep(".onto svg .oe-r.oe-me line{stroke-dasharray:6 4;opacity:.7}\n",
    ".onto svg .oe-r.oe-me line{stroke-dasharray:6 4;opacity:.7}\n"
    ".onto svg .oe-e{cursor:grab}.onto svg .oe-e.drag{cursor:grabbing}.onto svg .oe-l.oe-vc .oe-vt{font-style:normal;font-weight:700;font-size:11px}.onto svg .oe-l.oe-vx{opacity:.55}\n"
    ".onto svg.has-sel .oe-r.dim,.onto svg.has-sel .oe-l.dim{opacity:.07}.onto svg.has-sel .oe-r.sel line{stroke-width:2.6}.onto svg.has-sel .oe-l.sel{opacity:1}.onto svg.has-sel .oe-l.sel .oe-v{stroke:var(--blue);stroke-width:1.5}\n"
    ".onto svg.lab-hover .oe-l:not(.sel){display:none}\n", 1)
# the pane's introduction says what relocating offers
rep("Choose an entity to see its members, its relationships with their counts and the sentences behind them. The page\\'s own schema",
    "Choose an entity to see its members, its relationships with their counts and the sentences behind them; its lines are lifted and the others dimmed. Drag an entity to move it; Untangle relocates them all so the lines are short and cross little; labels are placed where they fit and shrink to their count where nothing fits. The page\\'s own schema", 1)
rep("<!-- course_page_template version 9.41.0:",
    "<!-- course_page_template version 9.42.0: the ERD gets a relocate function - draggable entities, Untangle (grid "
    "swaps minimising connection length and crossings), Wider/Tighter/Reset, a grid shaped to the room, anchors spread "
    "along the box sides, labels placed where they fit (count only where nothing fits; all / fitted / on choice), and "
    "the chosen entity's relationships lifted over dimmed others. Earlier: --><!-- course_page_template version 9.41.0:", 1)
open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
