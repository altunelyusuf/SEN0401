#!/usr/bin/env python3
"""template_patch v9_52_7 - writes course_page_template_v9_52_7.html from SEN0401's course_page_template_v9_52_5.html (committed, untouched).
Urgent owner request of 2026-10-30 02:23 Istanbul (ex:CR3_PanelView, task TK_Urgent_Ch06_Page_Build). Two changes and nothing else:
 1. EVERY diagram or visualisation panel (the page's .diagram hosts: concept map, ontology graph, ERD, neighbourhood maps, narrative diagrams, lab visualisations, chapter-code result pictures, parse trees)
    gets a visible Full screen control (the browser Fullscreen API on the page, and a full-viewport overlay in every case, so a browser that refuses the API still shows the panel full screen; Esc and the
    control close it), a drag handle under the panel that resizes it by mouse and touch with arrow keys for the keyboard, and Panel + / Panel - buttons. The size is kept between tabs (in memory, and in
    localStorage inside try/catch). The controls sit in the row above the drawing (the existing zoom bar, or a bar of their own for a panel without zoom) and never over it; the handle sits below it.
 2. The Playground lists FIRST (after its own default program, which the page tests require to be the first item) the chapter's real slide examples (the Chapter code entries) in slide order with their slide
    number and title; the group that held the concept examples is named 'Concept examples (one small example for each concept)'; one line says which list is which.
9.52.7 over the committed draft 9.52.6 (never edited; its panel code had not met a browser test): the panel kinds are named as the page names them (taxonomy, ontology graph, concept map), the HTML lab visualisations
(facts cards, bars) are panels too, the smallest panel is 80 px and the largest 8000 px, a touch drag does not stop when the browser refuses pointer capture.
Refuses when a text to replace is not found exactly once."""
__version__ = "1.0.0"
import os
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(H, "course_page_template_v9_52_5.html"), encoding="utf-8").read()
def rep(o, n):
    global s
    if s.count(o) != 1: raise SystemExit("REFUSED: %d occurrences of %r" % (s.count(o), o[:80]))
    s = s.replace(o, n)
rep("<!-- course_page_template version 9.24.0 (SEN0401)", "<!-- course_page_template version 9.52.7: every diagram or visualisation panel has a Full screen control (Fullscreen API plus a full-viewport overlay; Esc closes), a drag handle with keyboard and Panel +/- buttons that sets its size (kept between tabs); the Playground lists the chapter's slide examples first, in slide order, and the concept examples group is renamed. -->\n<!-- course_page_template version 9.24.0 (SEN0401)")
CSS = r"""
.pzbar{display:flex;justify-content:flex-end;flex-wrap:wrap;gap:.3rem;align-items:center;margin:.2rem 0 .35rem}.pzbar .btn,.zbar .btn[data-pz]{font-size:.82rem;padding:.2rem .55rem}
.pzh{height:14px;margin:2px 0 0;border-radius:7px;cursor:ns-resize;touch-action:none;position:relative;background:transparent}.pzh:before{content:"";position:absolute;left:50%;top:4px;width:46px;height:5px;margin-left:-23px;border-radius:3px;background:var(--line);border-top:1px solid var(--mute);border-bottom:1px solid var(--mute);box-sizing:border-box}.pzh:hover:before,.pzh:focus-visible:before{background:var(--blue)}.pzh:focus-visible{outline:2px solid var(--blue)}
.diagram[data-uh],.pzhtml[data-uh]{max-height:none!important;min-height:0!important}.pzhtml[data-uh]{overflow:auto}.pzhtml.pfs{overflow:auto;padding:.8rem 1.2rem;font-size:1.2rem;box-sizing:border-box}.diagram[data-uh] svg{max-height:none!important}.diagram.small.vz[data-uh]{aspect-ratio:auto!important;max-width:none!important}
@media (pointer:coarse){.pzh{height:26px}.pzh:before{top:10px}.pzbar .btn,.zbar .btn[data-pz]{min-height:40px}}
body.pfs-on{overflow:hidden}
.diagram.pfs,.pzhtml.pfs{position:fixed!important;z-index:2147483000;left:0;right:0;top:3.2rem;bottom:0;height:auto!important;max-height:none!important;min-height:0!important;max-width:none!important;width:auto!important;aspect-ratio:auto!important;border-radius:0;border:0;border-top:1px solid var(--line);background:var(--bg);margin:0}.diagram.pfs svg{max-height:none!important}
.zbar.pfsbar,.pzbar.pfsbar{position:fixed!important;z-index:2147483001;left:0;right:0;top:0;height:3.2rem;box-sizing:border-box;margin:0;padding:.35rem .6rem;background:var(--panel)!important;box-shadow:0 1px 4px rgba(0,0,0,.18)!important;justify-content:flex-end;align-items:center;flex-wrap:nowrap;overflow-x:auto}
.pzh.pfshide{display:none}
"""
rep(".zoomhost{position:relative}.zbar{position:absolute;", CSS.strip("\n") + "\n.zoomhost{position:relative}.zbar{position:absolute;")
rep("@media print{.navgrp,", "@media print{.pzbar,.pzh,.navgrp,")
JS = r"""
// ---------- panels (9.52.6): full screen and a reader-set size for every diagram or visualisation panel ----------
const PZ={sizes:{},open:null,key:'sen0401.panelsize.v1'};
try{const o=JSON.parse(localStorage.getItem(PZ.key)||'{}');if(o&&typeof o==='object')PZ.sizes=o}catch(_){}
function pzSave(){try{localStorage.setItem(PZ.key,JSON.stringify(PZ.sizes))}catch(_){}}
function pzKind(h){const p=h.parentElement,id=(p&&p.id)||'';if(id==='taxo')return'taxonomy';if(id==='onto')return'ontology';if(id==='graph')return'conceptmap';if(id==='oerd')return'erd';if(/^wv-/.test(id))return'lab';if(/^w-.*-diagram$/.test(id))return'tree';
 if(h.classList.contains('nd'))return'narrative';if(h.closest('.nbh'))return'neighbourhood';if(h.classList.contains('ccviz'))return'result';return id||'panel'}
const PZ_NAME={taxonomy:'concept taxonomy',conceptmap:'concept map',ontology:'ontology graph',erd:'entity-relationship diagram',lab:'visualisation',tree:'syntax tree',narrative:'diagram',neighbourhood:'neighbourhood map',result:'result picture'};
function pzPane(h){const p=h.closest('[data-pane]');return p?p.dataset.pane:''}
function pzKey(h){return pzPane(h)+'/'+pzKind(h)}
function pzSetH(h,px,store){px=Math.round(Math.max(80,Math.min(px,8000)));h.dataset.uh=px;h.style.height=px+'px';
 if(store){const k=pzKey(h);PZ.sizes[k]=px;pzSave();document.querySelectorAll('.diagram[data-pz]').forEach(o=>{if(o!==h&&pzKey(o)===k&&!o.classList.contains('pfs')){o.dataset.uh=px;o.style.height=px+'px'}})}
 const svg=h.querySelector('svg');if(svg&&h.classList.contains('zoomhost')){svg.style.height='100%'}}
function pzCur(h){return h.getBoundingClientRect().height}
function pzFull(h,on){const bar=h.previousElementSibling&&(h.previousElementSibling.classList.contains('zbar')||h.previousElementSibling.classList.contains('pzbar'))?h.previousElementSibling:null,hd=h.nextElementSibling&&h.nextElementSibling.classList.contains('pzh')?h.nextElementSibling:null;
 if(on){if(PZ.open&&PZ.open!==h)pzFull(PZ.open,false);PZ.open=h;h.classList.add('pfs');if(bar)bar.classList.add('pfsbar');if(hd)hd.classList.add('pfshide');document.body.classList.add('pfs-on');
  const b=bar&&bar.querySelector('[data-pz="full"]');if(b){b.textContent='✕ Close full screen';b.setAttribute('aria-label','Close full screen (Esc)');b.title='Close full screen (Esc)';b.focus()}
  try{const r=document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();if(r&&r.catch)r.catch(()=>{})}catch(_){}}
 else{if(PZ.open===h)PZ.open=null;h.classList.remove('pfs');if(bar)bar.classList.remove('pfsbar');if(hd)hd.classList.remove('pfshide');document.body.classList.remove('pfs-on');
  const b=bar&&bar.querySelector('[data-pz="full"]');if(b){b.textContent='⛶ Full screen';b.setAttribute('aria-label','Full screen');b.title='Show this panel full screen';b.focus()}
  try{if(document.fullscreenElement&&document.exitFullscreen){const r=document.exitFullscreen();if(r&&r.catch)r.catch(()=>{})}}catch(_){}}
 setTimeout(()=>{try{fitViews()}catch(_){}window.dispatchEvent(new Event('resize'))},60)}
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&PZ.open){e.preventDefault();e.stopPropagation();pzFull(PZ.open,false)}},true);
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement&&PZ.open)pzFull(PZ.open,false)});
function pzPanel(h){if(!h||h.dataset.pz)return;h.dataset.pz='1';const nm=PZ_NAME[pzKind(h)]||'panel';
 let bar=h.previousElementSibling&&h.previousElementSibling.classList.contains('zbar')?h.previousElementSibling:null;
 if(!bar){bar=document.createElement('div');bar.className='pzbar';h.parentNode.insertBefore(bar,h)}
 const mk=(a,t,ti,al)=>{const b=document.createElement('button');b.type='button';b.className='btn g';b.dataset.pz=a;b.textContent=t;b.title=ti;b.setAttribute('aria-label',al||ti);b.addEventListener('click',ev=>{ev.stopPropagation();pzAct(h,a)});return b};
 bar.appendChild(mk('full','⛶ Full screen','Show this '+nm+' full screen','Full screen'));bar.appendChild(mk('bigger','Panel ＋','Make this '+nm+' larger','Larger panel'));bar.appendChild(mk('smaller','Panel －','Make this '+nm+' smaller','Smaller panel'));
 const hd=document.createElement('div');hd.className='pzh';hd.tabIndex=0;hd.setAttribute('role','separator');hd.setAttribute('aria-orientation','horizontal');hd.setAttribute('aria-label','Resize this '+nm+': drag, or use the up and down arrow keys');hd.title='Drag to resize this '+nm+' (arrow keys also work)';
 h.parentNode.insertBefore(hd,h.nextSibling);
 let dr=null;hd.addEventListener('pointerdown',e=>{dr={y:e.clientY,h:pzCur(h)};try{hd.setPointerCapture(e.pointerId)}catch(_){}e.preventDefault()});
 hd.addEventListener('pointermove',e=>{if(!dr)return;pzSetH(h,dr.h+(e.clientY-dr.y),false)});
 const end=e=>{if(!dr)return;dr=null;pzSetH(h,pzCur(h),true);setTimeout(()=>{try{fitViews()}catch(_){}},0)};hd.addEventListener('pointerup',end);hd.addEventListener('pointercancel',end);
 hd.addEventListener('keydown',e=>{const st=e.shiftKey?120:40;if(e.key==='ArrowDown'||e.key==='ArrowRight'){e.preventDefault();pzSetH(h,pzCur(h)+st,true)}else if(e.key==='ArrowUp'||e.key==='ArrowLeft'){e.preventDefault();pzSetH(h,pzCur(h)-st,true)}});
 const k=pzKey(h);if(PZ.sizes[k]>0)pzSetH(h,PZ.sizes[k],false)}
function pzAct(h,a){if(a==='full')pzFull(h,!h.classList.contains('pfs'));else if(a==='bigger')pzSetH(h,pzCur(h)*1.25,true);else if(a==='smaller')pzSetH(h,pzCur(h)/1.25,true);setTimeout(()=>{try{fitViews()}catch(_){}},0)}
(function(){let q=0;const scan=()=>{q=0;document.querySelectorAll('.diagram:not([data-pz])').forEach(h=>{if(h.querySelector('svg'))pzPanel(h)});document.querySelectorAll('.vis.nv[data-nvk="facts"]>[id$="-out"]:not([data-pz]),.vis.nv[data-nvk="hist"]>[id$="-out"]:not([data-pz])').forEach(h=>{if(h.children.length&&!h.querySelector('.diagram')){h.classList.add('pzhtml');pzPanel(h)}})};
 new MutationObserver(()=>{if(!q)q=setTimeout(scan,0)}).observe(document.body,{childList:true,subtree:true})})();
"""
rep("// ---------- relocate: any diagram whose nodes carry an identifier", JS.strip("\n") + "\n// ---------- relocate: any diagram whose nodes carry an identifier")
rep("host.classList.add('zoomhost');relocatable(host)}", "host.classList.add('zoomhost');relocatable(host);pzPanel(host)}")
rep("el.style.height='auto';const top=el.getBoundingClientRect().top;", "if(el.classList.contains('pfs'))return;if(el.dataset.uh){el.style.height=el.dataset.uh+'px';return}el.style.height='auto';const top=el.getBoundingClientRect().top;")
# 2. the Playground lists
rep("""s.innerHTML='<option value="first" data-pg-item selected title="'+esc(D.course.playground.label)+'">'+esc(pgName(D.course.playground.label))+'</option><optgroup label="Examples from this chapter">'+ex.map(o=>o.outerHTML).join('')+'</optgroup>""",
    """const ccg=CC.length?'<optgroup label="Slide examples ('+CC.length+', in slide order)">'+CC.map((e,i)=>'<option value="cc:'+i+'" data-pg-item title="'+esc((e.slide?'Slide '+e.slide+': ':'')+e.name)+'">'+esc(pgName((e.slide?'Slide '+e.slide+' \\u2013 ':'')+e.name))+'</option>').join('')+'</optgroup>':'';
 s.innerHTML='<option value="first" data-pg-item selected title="'+esc(D.course.playground.label)+'">'+esc(pgName(D.course.playground.label))+'</option>'+ccg+'<optgroup label="Concept examples (one small example for each of the '+ex.length+' concepts)">'+ex.map(o=>o.outerHTML).join('')+'</optgroup>""")
rep("""ED_TPL.map((t,i)=>'<option value="tpl:'+i+'" data-pg-item title="'+esc(t[0])+'">'+esc(pgName(t[0]))+'</option>').join('')+'</optgroup>'})();""",
    """ED_TPL.map((t,i)=>'<option value="tpl:'+i+'" data-pg-item title="'+esc(t[0])+'">'+esc(pgName(t[0]))+'</option>').join('')+'</optgroup>';
 const row=s.closest('.pgrow');if(row&&!document.getElementById('pexnote')){const p=document.createElement('p');p.className='note';p.id='pexnote';p.textContent=(CC.length?'Two lists of examples: the Slide examples are the '+CC.length+' code examples shown on the lecture slides, in slide order; the Concept examples are one small example for each of the '+ex.length+' concepts of the chapter. ':'')+'Choose one and it fills the editor.';row.parentNode.insertBefore(p,row)}})();""")
rep("v.slice(0,4)==='tpl:'?ED_TPL[+v.slice(4)][1]:byId[v].io.code;fitViews()}", "v.slice(0,4)==='tpl:'?ED_TPL[+v.slice(4)][1]:v.slice(0,3)==='cc:'?CC[+v.slice(3)].code:byId[v].io.code;fitViews()}")
open(os.path.join(H, "course_page_template_v9_52_7.html"), "w", encoding="utf-8").write(s)
print("wrote course_page_template_v9_52_7.html", len(s))
