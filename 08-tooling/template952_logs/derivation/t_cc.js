// ---------- 9.52.0: the chapter code - the deck's code examples, listed by name in the order of the slides ----------
// The list holds names only; choosing a name opens that example in the editor beside it. The code runs with the chapter library the page defines
// (the page data's py_wheels and py_boot, loaded into Pyodide by the same worker as the Playground); the result is drawn, not only printed.
const CCS={i:0,running:false};
function ccPane(){return '<div role="tabpanel" data-pane="chaptercode" hidden><h2>💻 Chapter code</h2><p class="note">The code examples of the lecture, listed by name in the order of the slides. Choose one to open it in the editor; edit it if you like; Run shows its result as a picture and as text. The chapter’s own library is already loaded, so every example runs as it is. Python loads on your first run.</p>'
 +'<div class="ccwrap"><ol class="cclist" role="listbox" aria-label="Code examples in the order of the slides">'+CC.map((e,i)=>'<li role="option" tabindex="'+(i?-1:0)+'" aria-selected="'+(i?'false':'true')+'" data-cc-item="'+i+'" data-cc-name="'+esc(e.name)+'" data-cc-order="'+e.order+'"'+(e.slide?' data-cc-slide="'+esc(e.slide)+'" title="Slide '+esc(e.slide)+'"':'')+'>'+esc(e.name)+'</li>').join('')+'</ol>'
 +'<div class="ccmain"><div class="cchead"><h3 class="cctitle"></h3><span class="ccslide note"></span></div><p class="ccnote"></p>'
 +'<textarea class="code" data-cc-editor id="cccode" data-fill="0" aria-label="Chapter code example" spellcheck="false"></textarea>'
 +'<div class="row ccbar"><button class="btn" data-cc-run>▶ Run</button><button class="btn g" data-cc-reset>Reset</button><button class="btn g" data-cc-prev aria-label="Previous example">◀ Previous</button><button class="btn g" data-cc-next aria-label="Next example">Next ▶</button><button class="btn g" data-cc-runall title="Run every example in order and mark each one">Run all</button><span class="ccprog note" aria-live="polite"></span></div>'
 +'<div class="ccres" data-cc-result aria-live="polite"></div></div></div></div>'}
function ccPaneEl(){return panes.querySelector('[data-pane="chaptercode"]')}
function ccOpen(i,keep){const pane=ccPaneEl();if(!pane||!CC.length)return;i=Math.max(0,Math.min(CC.length-1,i));CCS.i=i;const e=CC[i];
 pane.querySelectorAll('[data-cc-item]').forEach((li,k)=>{li.setAttribute('aria-selected',k===i?'true':'false');li.tabIndex=k===i?0:-1});
 const ta=pane.querySelector('[data-cc-editor]');ta.value=e.code;ta.dispatchEvent(new Event('input',{bubbles:true}));
 pane.querySelector('.cctitle').textContent=e.order+'. '+e.name;pane.querySelector('.ccslide').textContent=e.slide?'Slide '+e.slide:'';
 pane.querySelector('.ccnote').textContent=e.note||'';pane.querySelector('.ccnote').hidden=!e.note;
 if(!keep)pane.querySelector('[data-cc-result]').innerHTML='<p class="note ccidle">Press Run to see the result.'+(e.expected?' The slide shows: <code>'+esc(String(e.expected).split('\n')[0].slice(0,80))+'</code>':'')+'</p>';
 const li=pane.querySelector('[data-cc-item="'+i+'"]');if(li&&li.scrollIntoView)li.scrollIntoView({block:'nearest'});
 pane.querySelector('[data-cc-prev]').disabled=i===0;pane.querySelector('[data-cc-next]').disabled=i===CC.length-1;setTimeout(fitViews,30)}
const ccNorm=s=>String(s).trim().replace(/\s+/g,' ');
// reads an output and says what to draw: bars for numbers, coloured byte cells for hexadecimal, a result card for anything else
function ccParse(out){const s=String(out).trim();let v=null;
 try{v=JSON.parse(s.replace(/'/g,'"').replace(/\bNone\b/g,'null').replace(/\bTrue\b/g,'true').replace(/\bFalse\b/g,'false').replace(/\(/g,'[').replace(/\)/g,']'))}catch(_){}
 if(Array.isArray(v)&&v.length>=2&&v.length<=48&&v.every(x=>typeof x==='number'&&isFinite(x)))return {kind:'bars',labels:v.map((_,i)=>String(i)),values:v};
 if(v&&typeof v==='object'&&!Array.isArray(v)){const ks=Object.keys(v);if(ks.length>=2&&ks.length<=48&&ks.every(k=>typeof v[k]==='number'&&isFinite(v[k])))return {kind:'bars',labels:ks,values:ks.map(k=>v[k])}}
 const lines=s.split('\n').filter(l=>l.trim());const kv=lines.map(l=>l.match(/^\s*([^:=]{1,40}?)\s*[:=]\s*(-?\d[\d_,]*(?:\.\d+)?)\s*(?:[A-Za-z%]{0,8})\s*$/));
 if(lines.length>=2&&lines.length<=48&&kv.every(Boolean))return {kind:'bars',labels:kv.map(m=>m[1]),values:kv.map(m=>parseFloat(m[2].replace(/[_,]/g,'')))};
 const hx=s.match(/(?:0x)?\b[0-9a-fA-F]{16,}\b/g);if(hx&&hx.length)return {kind:'bytes',hex:hx.slice(0,3).map(h=>h.replace(/^0x/,''))};
 return {kind:'text',lines:lines.slice(0,10),more:Math.max(0,lines.length-10)}}
function ccSvg(p){const W=560;let h=0,s='';
 if(p.kind==='bars'){const n=p.values.length,mx=Math.max(...p.values.map(Math.abs),1e-9),bw=Math.min(46,(W-60)/n-6),H=170,base=H-34,hh=H-60;h=H;
  s+='<line class="ccax" x1="30" y1="'+base+'" x2="'+(W-10)+'" y2="'+base+'"/>';
  p.values.forEach((v,i)=>{const x=36+i*((W-60)/n),bh=Math.max(2,Math.abs(v)/mx*hh),lab=String(p.labels[i]);s+='<rect class="ccbar" x="'+x+'" y="'+(base-bh)+'" width="'+bw+'" height="'+bh+'" rx="3"><title>'+esc(lab+': '+v)+'</title></rect><text class="ccval" x="'+(x+bw/2)+'" y="'+(base-bh-4)+'" text-anchor="middle">'+esc(Math.abs(v)>=1e6?v.toExponential(1):String(Math.round(v*100)/100))+'</text><text class="cclab" x="'+(x+bw/2)+'" y="'+(base+14)+'" text-anchor="middle">'+esc(lab.length>(n>12?5:9)?lab.slice(0,n>12?4:8)+'…':lab)+'</text>'})}
 else if(p.kind==='bytes'){let y=8;p.hex.forEach(hx=>{const bytes=hx.length>=2?hx.match(/../g):[],cols=Math.min(16,Math.max(4,bytes.length)),cw=Math.min(32,(W-20)/cols),maxb=Math.min(bytes.length,64);
   s+='<text class="cclab" x="10" y="'+(y+10)+'">'+esc(hx.length>40?hx.slice(0,20)+'…'+hx.slice(-12):hx)+'  ('+bytes.length+' bytes)</text>';y+=18;
   for(let i=0;i<maxb;i++){const b=parseInt(bytes[i],16),cx=10+(i%cols)*cw,cy=y+Math.floor(i/cols)*cw;s+='<rect x="'+cx+'" y="'+cy+'" width="'+(cw-2)+'" height="'+(cw-2)+'" rx="3" fill="hsl('+Math.round(b/255*300)+',55%,'+(40+Math.round(b/255*22))+'%)"><title>byte '+i+' = 0x'+bytes[i]+' ('+b+')</title></rect>'+(cw>=24?'<text class="ccbyte" x="'+(cx+cw/2-1)+'" y="'+(cy+cw/2+3)+'" text-anchor="middle">'+bytes[i]+'</text>':'')}
   y+=Math.ceil(maxb/cols)*cw+10});h=y}
 else{const L=p.lines;h=22+L.length*20+(p.more?20:0);s+='<rect class="cccard" x="6" y="6" width="'+(W-12)+'" height="'+(h-12)+'" rx="8"/>';L.forEach((l,i)=>{s+='<text class="ccln" x="18" y="'+(28+i*20)+'">'+(i+1)+'</text><text class="cctx" x="40" y="'+(28+i*20)+'">'+esc(l.length>64?l.slice(0,63)+'…':l)+'</text>'});if(p.more)s+='<text class="cclab" x="40" y="'+(28+L.length*20)+'">… and '+p.more+' more lines</text>'}
 return '<svg viewBox="0 0 '+W+' '+Math.max(h,40)+'" role="img" aria-label="'+(p.kind==='bars'?'Bar chart of the printed numbers':p.kind==='bytes'?'The printed hexadecimal as coloured byte cells':'The printed lines as a result card')+'">'+s+'</svg>'}
function ccVisual(out,e,ms,same){const o=String(out),p=ccParse(o),err=/^(\w*Error|Traceback|Stopped after)/.test(o.trim());
 const exp=e.expected!==undefined?ccNorm(e.expected):null,ok=exp!==null&&same?(ccNorm(o)===exp):null;
 const chip=err?'<span class="cchip bad">✗ Python reported an error</span>':ok===true?'<span class="cchip ok">✓ same result as on the slide</span>':ok===false?'<span class="cchip bad">✗ differs from the slide, which shows: <code>'+esc(String(e.expected).slice(0,90))+'</code></span>':exp!==null?'<span class="cchip">code edited: the slide’s result no longer applies</span>':'';
 CCS.last={ok:err?'error':ok===false?'diff':'ok'};
 return '<div class="ccflow"><span>code</span> → <span>Python</span> → <span><b>'+(p.kind==='bars'?'numbers drawn as bars':p.kind==='bytes'?'bytes drawn as cells':'lines in a result card')+'</b></span> <small>('+ms+' ms)</small> '+chip+'</div>'
  +(err?'':'<div class="diagram small ccviz">'+ccSvg(p)+'</div>')+'<output class="out'+(err?' err':'')+'" data-cc-text>'+esc(o)+'</output>'}
async function ccRun(){const pane=ccPaneEl();if(!pane||CCS.running)return;const ta=pane.querySelector('[data-cc-editor]'),res=pane.querySelector('[data-cc-result]'),e=CC[CCS.i],i=CCS.i;CCS.running=true;res.innerHTML='<p class="note">Running…</p>';
 const t0=performance.now();let out;try{out=await runPy(ta.value,[])}catch(err){out='Error: '+err.message}
 CCS.running=false;res.innerHTML=ccVisual(out,e,Math.round(performance.now()-t0),ta.value===e.code);const h=res.querySelector('.diagram');if(h)zoomable(h);
 const li=pane.querySelector('[data-cc-item="'+i+'"]');if(li)li.dataset.ccStatus=CCS.last.ok;return CCS.last.ok}
async function ccRunAll(){const pane=ccPaneEl(),pr=pane.querySelector('.ccprog');let ok=0;for(let i=0;i<CC.length;i++){ccOpen(i,true);pr.textContent='Running '+(i+1)+' of '+CC.length+'…';const r=await ccRun();if(r==='ok')ok++}pr.textContent=ok+' of '+CC.length+' examples ran and match their slide.'}
(function(){const pane=ccPaneEl();if(!pane)return;ccOpen(0);
 pane.addEventListener('click',e=>{const li=e.target.closest('[data-cc-item]');if(li){ccOpen(+li.dataset.ccItem);return}
  if(e.target.closest('[data-cc-run]')){ccRun();return}if(e.target.closest('[data-cc-reset]')){ccOpen(CCS.i);return}
  if(e.target.closest('[data-cc-prev]')){ccOpen(CCS.i-1);return}if(e.target.closest('[data-cc-next]')){ccOpen(CCS.i+1);return}if(e.target.closest('[data-cc-runall]')){ccRunAll();return}});
 pane.addEventListener('keydown',e=>{const li=e.target.closest&&e.target.closest('[data-cc-item]');if(!li)return;
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();ccOpen(+li.dataset.ccItem+(e.key==='ArrowDown'?1:-1));const n=pane.querySelector('[data-cc-item="'+CCS.i+'"]');if(n)n.focus()}
  else if(e.key==='Enter'||e.key===' '){e.preventDefault();ccOpen(+li.dataset.ccItem)}})})();

// ---------- 9.52.0: a panel is at most one screen high: its box gets the height that is left under the tabs and the breadcrumb ----------
function fitPanels(){const c=document.getElementById('center');if(!c)return;const wide=innerWidth>1000;
 if(wide)c.scrollTop=0;const bp=wide?(parseFloat(getComputedStyle(c).paddingBottom)||0):0;
 document.querySelectorAll('#panes>[data-pane]').forEach(p=>{if(!wide||p.hidden){p.style.removeProperty('max-height');return}p.style.maxHeight=Math.max(240,Math.floor(c.clientHeight-(p.getBoundingClientRect().top-c.getBoundingClientRect().top)-bp-2))+'px'});
 document.querySelectorAll('#panes [data-panel]').forEach(p=>{if(!wide){p.style.removeProperty('--ph');return}if(p.hidden||!p.offsetParent)return;
  const sp=p.closest('[data-subpane]')||p.parentElement,first=[...sp.querySelectorAll('[data-panel]')].find(x=>!x.hidden&&x.offsetParent)||p;
  const off=first.getBoundingClientRect().top-c.getBoundingClientRect().top;p.style.setProperty('--ph',Math.max(300,Math.floor(c.clientHeight-off-bp-6))+'px')})}
