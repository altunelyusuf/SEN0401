// SEN0401 shared deck renderer v1.0.0 - the chapter-1 v2.8.0 renderer promoted to shared
// tooling so every chapter's deck draws the SAME look-and-feel (the CME materials standard:
// warm-ivory palette, Cambria/Calibri, the B-chip, fact rows, takeaway strips, native charts
// with data labels, syntax-coloured never-wrapping code). It draws exactly what the given plan
// places and invents nothing. Chapter deck_check conventions are unchanged.
// Usage: node deck_render_v1_0_0.js <deck_plan.json> <out.pptx>
const VERSION = "render-1.0.0";
const PLAN = process.argv[2];
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const plan = JSON.parse(fs.readFileSync(PLAN)); const M = plan.meta;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel';
pres.title = 'SEN0401 ' + M.title;
const C = { dark:'2B2622', orange:'D97A14', ink:'2B2622', mute:'6E655C', card:'F2ECE1', code:'23272E',
            codeTxt:'E6EDF3', green:'7EE787', white:'FFFFFF', slate:'2F6D62', rule:'DFD6C7', pale:'8A9B94',
            bgc:'FAF6EF', band:'EFE6D6' };
const H='Cambria', B='Calibri', MONO='Courier New';
const COL = {ink:C.ink, mute:C.mute, white:C.white, orange:C.orange, dark:C.dark};

function chip(s,x,y){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:0.62,h:0.42,fill:{color:C.orange},line:{color:C.orange},rectRadius:0.08});
  s.addText('₿',{x,y,w:0.62,h:0.42,fontFace:B,fontSize:18,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true}); }
function head(s,t,sub){ chip(s,0.5,0.38);
  s.addText(t,{x:1.25,y:0.26,w:8.25,h:0.62,fontFace:H,fontSize:t.length>46?22:(t.length>32?25:28),bold:true,color:C.dark,margin:0,valign:'middle',isTextBox:true});
  if(sub) s.addText(sub,{x:1.25,y:0.86,w:8.25,h:0.34,fontFace:B,fontSize:13,italic:true,color:C.mute,margin:0,isTextBox:true}); }

function drawCard(s,e){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y,w:e.w,h:e.h,fill:{color:C.card},line:{color:C.card},rectRadius:0.1});
  s.addText(e.head,{x:e.x+0.2,y:e.y+0.13,w:e.w-0.4,h:0.38,fontFace:H,fontSize:16,bold:true,color:e.accent==='slate'?C.slate:C.orange,margin:0,valign:'middle',isTextBox:true});
  s.addText(e.body,{x:e.x+0.2,y:e.y+0.55,w:e.w-0.4,h:e.h-0.70,fontFace:B,fontSize:e.fs,color:C.ink,margin:0,valign:'top',isTextBox:true}); }

// a console transcript: each statement is its own paragraph beginning '>>> ', its answer the next one,
// so the chapter's deck check can find every example on the finished slide and run it again.
function codeLabel(s,e){ if(e.label) s.addText(e.label,{x:e.x,y:e.y-0.30,w:e.w,h:0.28,fontFace:B,fontSize:11.5,bold:true,color:C.slate,margin:0,valign:'bottom',isTextBox:true}); }

function drawCode(s,e){ codeLabel(s,e); s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y,w:e.w,h:e.h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  const runs=[]; e.rows.forEach(([st,out],i)=>{ const last=i===e.rows.length-1;
    runs.push({text:'>>> ',options:{color:C.orange,bold:true}});
    runs.push({text:st,options:{color:C.codeTxt,breakLine:!(last&&out==='')}});
    if(out!=='') runs.push({text:out,options:{color:C.green,breakLine:!last}}); });
  s.addText(runs,{x:e.x+0.2,y:e.y+0.13,w:e.w-0.4,h:e.h-0.26,fontFace:MONO,fontSize:e.fs,valign:'top',margin:0,isTextBox:true});
  if(e.cap) s.addText(e.cap,{x:e.x,y:e.y+e.h+0.02,w:e.w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }

// a program the example runs as a whole: its lines verbatim, then the value of result
function drawProg(s,e){ codeLabel(s,e); s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y,w:e.w,h:e.h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  const runs=[]; e.lines.forEach((t,i)=>{ const rs=colorLine(t); rs[rs.length-1].options=Object.assign({},rs[rs.length-1].options,{breakLine:i<e.lines.length-1}); rs.forEach(r=>runs.push(r)); });
  s.addText(runs,{x:e.x+0.2,y:e.y+0.13,w:e.w-0.4,h:e.h-0.26,fontFace:MONO,fontSize:e.fs,valign:'top',margin:0,isTextBox:true});
  let y=e.y+e.h+0.02;
  if(e.out){ s.addText([{text:'result  ',options:{color:C.orange,bold:true}},{text:e.out,options:{color:C.dark}}],
    {x:e.x,y:y,w:e.w,h:0.28,fontFace:MONO,fontSize:Math.max(9,e.fs),margin:0,valign:'middle',isTextBox:true}); y+=0.28; }
  if(e.cap) s.addText(e.cap,{x:e.x,y:y,w:e.w,h:0.22,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }

function drawTable(s,e){ const tb=e.rows.map((r,i)=>r.map(t=>i===0?{text:t,options:{bold:true,color:C.white,fill:{color:C.dark}}}:{text:t}));
  s.addTable(tb,{x:e.x,y:e.y,w:e.w,colW:e.colW,fontFace:B,fontSize:e.fs,color:C.ink,border:{type:'solid',pt:0.5,color:C.rule},rowH:e.rowH,valign:'middle'}); }

function drawBoxes(s,e){ const n=e.items.length, cols=Math.max(1,e.cols), rows=Math.ceil(n/cols);
  const gx=0.16, gy=0.14, bw=(e.w-(cols-1)*gx)/cols, bh=(e.h-(rows-1)*gy)/rows;
  e.items.forEach((it,i)=>{ const r=Math.floor(i/cols), c=i%cols, x=e.x+c*(bw+gx), y=e.y+r*(bh+gy);
    const hot=e.accent.indexOf(i)>=0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:bw,h:bh,fill:{color:hot?C.orange:C.card},line:{color:hot?C.orange:C.rule},rectRadius:0.08});
    const t=[{text:it.label,options:{bold:true,fontSize:e.fs,color:hot?C.white:C.dark,breakLine:!!it.sub}}];
    if(it.sub) t.push({text:it.sub,options:{fontSize:e.subfs,color:hot?C.white:C.mute}});
    s.addText(t,{x:x+0.10,y:y+0.06,w:bw-0.20,h:bh-0.12,fontFace:B,align:'center',valign:'middle',margin:0,isTextBox:true});
    if(e.arrows&&c<cols-1&&i<n-1) s.addShape(pres.shapes.LINE,{x:x+bw,y:y+bh/2,w:gx,h:0,line:{color:C.orange,width:1.5,endArrowType:'triangle'}}); }); }

function drawText(s,e){ s.addText(e.body,{x:e.x,y:e.y,w:e.w,h:e.h,fontFace:e.font==='H'?H:B,fontSize:e.fs,
  italic:!!e.italic,bold:!!e.bold,color:COL[e.color]||C.ink,align:e.align||'left',valign:'top',margin:0,isTextBox:true}); }

function drawFoot(s,e){ s.addText(e.body,{x:e.x,y:e.y,w:e.w,h:e.h,fontFace:B,fontSize:e.fs,italic:true,color:C.mute,margin:0,valign:'top',isTextBox:true}); }

function drawNumList(s,e){ const step=Math.min(0.72,e.h/e.items.length);
  e.items.forEach((t,i)=>{ const y=e.y+i*step;
    s.addShape(pres.shapes.OVAL,{x:e.x,y:y+0.04,w:0.44,h:0.44,fill:{color:C.orange},line:{color:C.orange}});
    s.addText(String(i+1),{x:e.x,y:y+0.04,w:0.44,h:0.44,fontFace:H,fontSize:14,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
    s.addText(t,{x:e.x+0.62,y:y,w:e.w-0.62,h:step-0.04,fontFace:B,fontSize:e.fs,color:C.ink,valign:'middle',margin:0,isTextBox:true}); }); }

function drawBullets(s,e){ s.addText(e.items.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<e.items.length-1}})),
  {x:e.x,y:e.y,w:e.w,h:e.h,fontFace:B,fontSize:e.fs,color:C.ink,paraSpaceAfter:4,margin:0,valign:'top',isTextBox:true}); }

function drawQuestion(s,e){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y,w:e.w,h:e.h,fill:{color:C.card},line:{color:C.rule},rectRadius:0.08});
  s.addText(e.q,{x:e.x+0.18,y:e.y+0.07,w:e.w-0.36,h:0.34,fontFace:B,fontSize:e.fs,bold:true,color:C.dark,margin:0,valign:'middle',isTextBox:true});
  const letters='ABCD';
  s.addText(e.options.map((o,i)=>({text:letters[i]+')  '+o,options:{breakLine:i<e.options.length-1}})),
    {x:e.x+0.18,y:e.y+0.40,w:e.w-0.36,h:e.h-0.46,fontFace:B,fontSize:e.fs-1.5,color:C.ink,margin:0,valign:'top',isTextBox:true}); }


// ---- v2 visual primitives --------------------------------------------------------------------
function line(s,x1,y1,x2,y2,color,width,arrow){ const o={x:Math.min(x1,x2),y:Math.min(y1,y2),w:Math.abs(x2-x1),h:Math.abs(y2-y1),
  line:{color:color||C.pale,width:width||1.25}}; if(arrow) o.line.endArrowType='triangle';
  o.flipV=((x2>x1)!==(y2>y1))&&y1!==y2; if(x2<x1){o.flipH=true;o.flipV=((x1>x2)!==(y2>y1))&&y1!==y2;}
  s.addShape(pres.shapes.LINE,o); }

function drawStat(s,e){ const n=e.items.length;
  if(e.vert){ const gh=0.14, th=(e.h-(n-1)*gh)/n;
    e.items.forEach((it,i)=>{ const y=e.y+i*(th+gh);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y,w:e.w,h:th,fill:{color:C.card},line:{color:C.rule},rectRadius:0.08});
      s.addText(String(it.n),{x:e.x+0.12,y:y+0.04,w:e.w-0.24,h:th*0.52,fontFace:H,fontSize:String(it.n).length>10?20:26,bold:true,color:C.orange,margin:0,valign:'middle',isTextBox:true});
      s.addText(it.label,{x:e.x+0.12,y:y+th*0.52,w:e.w-0.24,h:th*0.44,fontFace:B,fontSize:11,color:C.mute,margin:0,valign:'top',isTextBox:true}); });
  } else { const g=0.25, tw=(e.w-(n-1)*g)/n;
    e.items.forEach((it,i)=>{ const x=e.x+i*(tw+g);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:e.y,w:tw,h:e.h,fill:{color:C.card},line:{color:C.rule},rectRadius:0.08});
      s.addText(String(it.n),{x:x+0.12,y:e.y+0.08,w:tw-0.24,h:e.h*0.5,fontFace:H,fontSize:String(it.n).length>8?22:28,bold:true,color:C.orange,margin:0,valign:'middle',isTextBox:true});
      s.addText(it.label,{x:x+0.12,y:e.y+e.h*0.52,w:tw-0.24,h:e.h*0.44,fontFace:B,fontSize:11.5,color:C.ink,margin:0,valign:'top',isTextBox:true}); }); } }

function drawFlow(s,e){ const n=e.steps.length, g=0.52, bw=(e.w-(n-1)*g)/n, bh=e.h;
  e.steps.forEach((st,i)=>{ const x=e.x+i*(bw+g);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:e.y,w:bw,h:bh,fill:{color:C.slate},line:{color:C.slate,width:1},rectRadius:0.1});
    s.addText([{text:st.label,options:{bold:true,fontSize:e.fs,color:C.white,breakLine:!!st.sub}},
               {text:st.sub||'',options:{fontSize:e.fs-2.5,color:'D7E4E0'}}],
      {x:x+0.08,y:e.y+0.05,w:bw-0.16,h:bh-0.10,fontFace:B,align:'center',valign:'middle',margin:0,isTextBox:true});
    if(i<n-1) line(s,x+bw+0.06,e.y+bh/2,x+bw+g-0.06,e.y+bh/2,C.orange,2,true); }); }

function drawTree(s,e){ const n=e.nodes.length, rw=1.55, bx=e.x+2.15, bw=1.85;
  const rh=0.52, gap=Math.min(0.62,(e.h-n*rh)/Math.max(1,n-1)+rh), step=(e.h-rh)/Math.max(1,n-1);
  const rootY=e.y+e.h/2-0.3;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:rootY,w:rw,h:0.6,fill:{color:C.orange},line:{color:C.orange},rectRadius:0.1});
  s.addText(e.root,{x:e.x,y:rootY,w:rw,h:0.6,fontFace:H,fontSize:15,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
  e.nodes.forEach((nd,i)=>{ const y=e.y+i*step;
    line(s,e.x+rw,rootY+0.3,bx-0.05,y+rh/2,'C9BFAE',1.1,false);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:bx,y,w:bw,h:rh,fill:{color:C.slate},line:{color:C.slate,width:0.75},rectRadius:0.08});
    s.addText(nd.label,{x:bx+0.06,y,w:bw-0.12,h:rh,fontFace:B,fontSize:e.fs+1,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
    const kids=(nd.kids||[]).join('  ·  ');
    if(kids){ line(s,bx+bw,y+rh/2,bx+bw+0.3,y+rh/2,'C9BFAE',1.1,false);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:bx+bw+0.3,y:y+0.02,w:e.w-(bx-e.x)-bw-0.3,h:rh-0.04,fill:{color:C.card},line:{color:C.rule,width:0.5},rectRadius:0.06});
      s.addText(kids,{x:bx+bw+0.42,y:y+0.02,w:e.w-(bx-e.x)-bw-0.54,h:rh-0.04,fontFace:B,fontSize:e.fs,color:C.ink,valign:'middle',margin:0,isTextBox:true}); } }); }

function drawNet(s,e){ const pw=(e.w-0.4)/2;
  [[e.x,e.left],[e.x+pw+0.4,e.right]].forEach(([px,cfg],side)=>{
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:px,y:e.y,w:pw,h:e.h,fill:{color:C.card},line:{color:C.rule},rectRadius:0.1});
    s.addText(cfg.title,{x:px+0.15,y:e.y+0.08,w:pw-0.3,h:0.4,fontFace:H,fontSize:13.5,bold:true,color:side?C.orange:'54504A',margin:0,isTextBox:true});
    const cx=px+pw/2, cy=e.y+0.35+(e.h-0.35)/2, R=Math.min(pw,e.h-0.5)/2-0.42, r=0.21;
    if(side===0){ // hub and spokes
      const k=6;
      for(let i=0;i<k;i++){ const a=i*2*Math.PI/k-Math.PI/2, nx=cx+R*Math.cos(a), ny=cy+R*Math.sin(a);
        line(s,cx,cy,nx,ny,'BBB1A2',1.1,false);
        s.addShape(pres.shapes.OVAL,{x:nx-r,y:ny-r,w:2*r,h:2*r,fill:{color:'54504A'},line:{color:'54504A',width:0.75}}); }
      s.addShape(pres.shapes.OVAL,{x:cx-0.33,y:cy-0.33,w:0.66,h:0.66,fill:{color:C.dark},line:{color:C.orange,width:1.5}});
      s.addText(cfg.hub,{x:cx-0.5,y:cy-0.33,w:1.0,h:0.66,fontFace:B,fontSize:11,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
    } else { // mesh
      const k=cfg.n||8, pts=[];
      for(let i=0;i<k;i++){ const a=i*2*Math.PI/k-Math.PI/2; pts.push([cx+R*Math.cos(a),cy+R*Math.sin(a)]); }
      for(let i=0;i<k;i++){ [[1,1],[2,0.8],[3,0.55]].forEach(([d,w])=>{ const j=(i+d)%k; if(j>i||d===3&&i<k/2)
        line(s,pts[i][0],pts[i][1],pts[j][0],pts[j][1],'BBB1A2',w,false); }); }
      pts.forEach(p=>{ s.addShape(pres.shapes.OVAL,{x:p[0]-r,y:p[1]-r,w:2*r,h:2*r,fill:{color:C.orange},line:{color:C.white,width:0.75}}); }); } }); }

function drawChart(s,e){ const data=e.series.map(se=>({name:se.name,labels:e.labels,values:se.data}));
  const o={x:e.x,y:e.y,w:e.w,h:e.h};
  if(e.log){ o.valAxisLogScale=true; if(e.min) o.valAxisMinVal=e.min; if(e.max) o.valAxisMaxVal=e.max; o.valAxisLabelFormatCode=e.fmt||'General'; }
  if(e.dataLabels){ o.showValue=true; o.dataLabelFormatCode=e.dlFmt||'General'; o.dataLabelPosition=e.dlPos||'t';
    o.dataLabelFontSize=e.dlFs||8; o.dataLabelColor=e.dlColor||C.ink; o.dataLabelFontFace=B; }
  s.addChart(pres.ChartType[e.ctype||'line'], data, {...o,
    chartColors:[C.orange,C.slate], lineSize:2.5, lineSmooth:false, lineDataSymbol:'circle', lineDataSymbolSize:5,
    showTitle:!!e.title, title:e.title, titleFontFace:H, titleFontSize:13, titleColor:C.dark,
    catAxisLabelFontSize:10, valAxisLabelFontSize:10, catAxisLabelColor:C.mute, valAxisLabelColor:C.mute,
    valGridLine:{style:'solid',color:'E3DACB',size:0.5}, catGridLine:{style:'none'},
    showLegend:false, chartArea:{fill:{color:C.bgc}}, plotArea:{fill:{color:C.bgc}}}); }

function drawChips(s,e){ let x=e.x, y=e.y; const hh=e.big?0.58:0.46, fs=e.fs||13;
  e.items.forEach(t=>{ const w=0.42+t.length*fs*0.0115;
    if(x+w>e.x+e.w){ x=e.x; y+=hh+0.18; }
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h:hh,fill:{color:C.card},line:{color:C.orange,width:1},rectRadius:hh/2});
    s.addText(t,{x,y,w,h:hh,fontFace:B,fontSize:fs,bold:!!e.big,color:C.ink,align:'center',valign:'middle',margin:0,isTextBox:true});
    x+=w+0.22; }); }

function drawCompare(s,e){ const pw=(e.w-0.4)/2;
  [[e.x,e.left,C.orange],[e.x+pw+0.4,e.right,C.slate]].forEach(([px,cfg,ac])=>{
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:px,y:e.y,w:pw,h:e.h,fill:{color:C.card},line:{color:ac,width:1.25},rectRadius:0.1});
    s.addText(cfg.head,{x:px+0.2,y:e.y+0.12,w:pw-0.4,h:0.4,fontFace:H,fontSize:15,bold:true,color:ac,margin:0,isTextBox:true});
    s.addText(cfg.rows.map((t,i)=>({text:t,options:{bullet:{code:'2022'},breakLine:i<cfg.rows.length-1}})),
      {x:px+0.2,y:e.y+0.58,w:pw-0.4,h:e.h-0.72,fontFace:B,fontSize:e.fs,color:C.ink,paraSpaceAfter:5,margin:0,valign:'top',isTextBox:true}); }); }

// ---- v2.2 primitives: images, stories, result visualizations --------------------------------
function drawImg(s,e){ s.addImage({path:e.path,x:e.x,y:e.y,w:e.w,h:e.h,sizing:{type:'contain',w:e.w,h:e.h}});
  if(e.cap) s.addText(e.cap,{x:e.x,y:e.y+e.h+0.02,w:e.w,h:0.36,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'center',margin:0,isTextBox:true}); }

function drawWhen(s,e){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y,w:e.w,h:0.44,fill:{color:C.slate},line:{color:C.slate},rectRadius:0.22});
  s.addText(e.body,{x:e.x,y:e.y,w:e.w,h:0.44,fontFace:B,fontSize:13,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true}); }

function drawBeats(s,e){ const step=e.h/e.items.length;
  e.items.forEach((t,i)=>{ const y=e.y+i*step;
    s.addShape(pres.shapes.DIAMOND,{x:e.x,y:y+step/2-0.07,w:0.14,h:0.14,fill:{color:C.orange},line:{color:C.orange}});
    s.addText(t,{x:e.x+0.3,y:y,w:e.w-0.3,h:step,fontFace:B,fontSize:e.fs,color:C.ink,valign:'middle',margin:0,isTextBox:true}); }); }

function drawTimelineH(s,e){ const n=e.items.length, y=e.y+e.h*0.42;
  line(s,e.x+0.1,y,e.x+e.w-0.1,y,'C9BFAE',2,false);
  e.items.forEach((it,i)=>{ const x=e.x+0.3+i*(e.w-0.6)/(n-1);
    s.addShape(pres.shapes.OVAL,{x:x-0.09,y:y-0.09,w:0.18,h:0.18,fill:{color:it.hot?C.orange:C.slate},line:{color:C.white,width:1}});
    s.addText(it.year,{x:Math.max(e.x,Math.min(x-0.6,e.x+e.w-1.2)),y:y-0.52,w:1.2,h:0.3,fontFace:H,fontSize:12,bold:true,color:it.hot?C.orange:C.ink,align:'center',margin:0,isTextBox:true});
    s.addText(it.label,{x:Math.max(e.x,Math.min(x-0.85,e.x+e.w-1.7)),y:y+0.14,w:1.7,h:0.72,fontFace:B,fontSize:10,color:C.mute,align:'center',valign:'top',margin:0,isTextBox:true}); }); }

function drawNews(s,e){ s.addShape(pres.shapes.RECTANGLE,{x:e.x,y:e.y,w:e.w,h:e.h,fill:{color:'FFFDF7'},line:{color:'B9AE9C',width:1.25},shadow:{type:'outer',blur:6,offset:2,angle:45,opacity:0.25}});
  const SC=Math.min(1,e.w/5.3); s.addText(e.paper,{x:e.x,y:e.y+0.12,w:e.w,h:0.5,fontFace:'Times New Roman',fontSize:Math.round(22*SC+4*(1-SC)),bold:true,color:'1A1A1A',align:'center',margin:0,isTextBox:true});
  line(s,e.x+0.25,e.y+0.68,e.x+e.w-0.25,e.y+0.68,'1A1A1A',1,false);
  s.addText(e.date,{x:e.x,y:e.y+0.72,w:e.w,h:0.3,fontFace:'Times New Roman',fontSize:10.5,italic:true,color:'444444',align:'center',margin:0,isTextBox:true});
  s.addText(e.headline,{x:e.x+0.18,y:e.y+0.98,w:e.w-0.36,h:0.95,fontFace:'Times New Roman',fontSize:Math.max(11.5,Math.round(17*SC)),bold:true,color:'1A1A1A',align:'center',valign:'middle',margin:0,isTextBox:true});
  [0,1].forEach(i=>{ if(e.y+2.0+i*0.15<e.y+e.h-0.5) line(s,e.x+0.2,e.y+1.95+i*0.15,e.x+e.w-0.2,e.y+1.95+i*0.15,'C9C2B4',2.2,false); });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x+e.w/2-1.15,y:e.y+e.h-0.44,w:2.3,h:0.34,fill:{color:C.orange},line:{color:C.orange},rectRadius:0.18});
  s.addText(e.badge||'embedded in block 0',{x:e.x+e.w/2-1.15,y:e.y+e.h-0.44,w:2.3,h:0.34,fontFace:B,fontSize:10,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true}); }

function drawLedger(s,e){ const names=e.owners, n=names.length, cw=e.w/n;
  names.forEach((nm,i)=>{ const cx=e.x+i*cw+cw/2;
    s.addShape(pres.shapes.OVAL,{x:cx-0.52,y:e.y+0.15,w:1.04,h:1.04,fill:{color:'D8D0C2'},line:{color:'9A9183',width:2}});
    s.addShape(pres.shapes.OVAL,{x:cx-0.14,y:e.y+0.55,w:0.28,h:0.28,fill:{color:C.bgc},line:{color:'9A9183',width:1.5}});
    s.addText(nm,{x:cx-0.85,y:e.y+1.28,w:1.7,h:0.3,fontFace:B,fontSize:11,bold:true,color:C.ink,align:'center',margin:0,isTextBox:true});
    if(i<n-1) line(s,cx+0.6,e.y+0.67,cx+cw-0.6,e.y+0.67,C.orange,2,true); });
  s.addText(e.cap,{x:e.x,y:e.y+1.62,w:e.w,h:0.32,fontFace:B,fontSize:11,italic:true,color:C.mute,align:'center',margin:0,isTextBox:true}); }

function drawSwap(s,e){ const mid=e.x+e.w/2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y+0.2,w:e.w/2-0.7,h:e.h-0.6,fill:{color:C.card},line:{color:C.orange,width:1.25},rectRadius:0.1});
  s.addText(e.left.n,{x:e.x,y:e.y+0.34,w:e.w/2-0.7,h:0.62,fontFace:H,fontSize:30,bold:true,color:C.orange,align:'center',margin:0,isTextBox:true});
  s.addText(e.left.label,{x:e.x+0.1,y:e.y+1.0,w:e.w/2-0.9,h:0.5,fontFace:B,fontSize:12,color:C.ink,align:'center',margin:0,isTextBox:true});
  line(s,mid-0.5,e.y+e.h/2-0.1,mid+0.5,e.y+e.h/2-0.1,C.slate,2.5,true);
  line(s,mid+0.5,e.y+e.h/2+0.18,mid-0.5,e.y+e.h/2+0.18,C.slate,2.5,true);
  const px=e.x+e.w/2+0.7, pw=e.w/2-0.7;
  [0,1].forEach(k=>{ const cx=px+pw/2+(k?0.62:-0.62), cy=e.y+e.h/2;
    s.addShape(pres.shapes.OVAL,{x:cx-0.5,y:cy-0.5,w:1.0,h:1.0,fill:{color:'E8B94B'},line:{color:'B98A2B',width:2}});
    for(let a=0;a<6;a++){ const r=0.48; line(s,cx,cy,cx+r*Math.cos(a*Math.PI/3),cy+r*Math.sin(a*Math.PI/3),'B98A2B',1,false); } });
  s.addText(e.right.label,{x:px,y:e.y+e.h-0.42,w:pw,h:0.3,fontFace:B,fontSize:12,color:C.ink,align:'center',margin:0,isTextBox:true}); }

function drawBars(s,e){ const max=Math.max(...e.rows.map(r=>r.v)), bw=e.w-1.9;
  e.rows.forEach((r,i)=>{ const y=e.y+i*(e.h/e.rows.length), bh=0.34;
    s.addText(r.label,{x:e.x,y,w:1.3,h:bh+0.1,fontFace:B,fontSize:10.5,color:C.ink,valign:'middle',margin:0,isTextBox:true});
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x+1.4,y:y+0.03,w:Math.max(0.12,bw*r.v/max),h:bh,fill:{color:r.hot?C.orange:C.slate},line:{color:r.hot?C.orange:C.slate},rectRadius:0.05});
    s.addText(String(r.v.toLocaleString('en-US')),{x:e.x+1.4+Math.max(0.12,bw*r.v/max)+0.06,y:y+0.03,w:1.1,h:bh,fontFace:B,fontSize:10,bold:true,color:C.mute,valign:'middle',margin:0,isTextBox:true}); }); }

function drawRoute(s,e){ const n=e.hops.length, y=e.y+e.h*0.4;
  e.hops.forEach((h,i)=>{ const x=e.x+0.35+i*(e.w-0.7)/(n-1);
    if(i<n-1){ const x2=e.x+0.35+(i+1)*(e.w-0.7)/(n-1); line(s,x+0.22,y,x2-0.26,y,C.orange,2.25,true); }
    s.addShape(pres.shapes.OVAL,{x:x-0.24,y:y-0.24,w:0.48,h:0.48,fill:{color:i===0||i===n-1?C.orange:C.slate},line:{color:C.white,width:1.5}});
    s.addText(h,{x:x-0.6,y:y+0.3,w:1.2,h:0.3,fontFace:B,fontSize:10.5,bold:true,color:C.ink,align:'center',margin:0,isTextBox:true}); });
  s.addText(e.cap,{x:e.x,y:y+0.72,w:e.w,h:0.34,fontFace:B,fontSize:11,italic:true,color:C.mute,align:'center',margin:0,isTextBox:true}); }

function drawClaims(s,e){ e.rows.forEach((r,i)=>{ const y=e.y+i*(e.h/e.rows.length), hh=e.h/e.rows.length-0.12;
    const ok=r.ok;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y,w:e.w,h:hh,fill:{color:C.card},line:{color:ok?'5B8C5A':'B6533C',width:1.5},rectRadius:0.08});
    s.addShape(pres.shapes.OVAL,{x:e.x+0.1,y:y+hh/2-0.16,w:0.32,h:0.32,fill:{color:ok?'5B8C5A':'B6533C'},line:{color:ok?'5B8C5A':'B6533C'}});
    s.addText(ok?'✓':'✗',{x:e.x+0.1,y:y+hh/2-0.16,w:0.32,h:0.32,fontFace:B,fontSize:14,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
    s.addText(r.label,{x:e.x+0.52,y,w:e.w-0.6,h:hh,fontFace:B,fontSize:10.5,color:C.ink,valign:'middle',margin:0,isTextBox:true}); }); }

function drawChainviz(s,e){ const n=3, bw=(e.w-0.8)/n;
  for(let i=0;i<n;i++){ const x=e.x+i*(bw+0.4), bad=e.tampered&&i>0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:e.y,w:bw,h:e.h-0.5,fill:{color:bad?'F3DED6':C.card},line:{color:bad?'B6533C':'5B8C5A',width:1.75},rectRadius:0.08});
    s.addText('block '+i,{x,y:e.y+0.06,w:bw,h:0.3,fontFace:B,fontSize:11,bold:true,color:bad?'B6533C':'3C6B3B',align:'center',margin:0,isTextBox:true});
    s.addText(i===e.hit?'data changed!':(i===0?'the genesis record':'digest of block '+(i-1)),{x:x+0.05,y:e.y+0.4,w:bw-0.1,h:0.5,fontFace:MONO,fontSize:8.5,color:bad?'B6533C':C.mute,align:'center',valign:'top',margin:0,isTextBox:true});
    if(i<n-1) line(s,x+bw,e.y+(e.h-0.5)/2,x+bw+0.4,e.y+(e.h-0.5)/2,bad||i+1>0&&e.tampered?'B6533C':'5B8C5A',2,true); }
  s.addText(e.cap,{x:e.x,y:e.y+e.h-0.42,w:e.w,h:0.34,fontFace:B,fontSize:10.5,italic:true,color:C.mute,align:'center',margin:0,isTextBox:true}); }

function drawFunnel(s,e){ const steps=e.steps, n=steps.length;
  steps.forEach((st,i)=>{ const w=e.w*(1-0.18*i), x=e.x+(e.w-w)/2, y=e.y+i*(e.h-0.3)/n, hh=(e.h-0.3)/n-0.12;
    s.addShape(pres.shapes.TRAPEZOID,{x,y,w,h:hh,fill:{color:i===n-1?C.orange:C.slate},line:{color:C.white,width:1},flipV:true});
    s.addText(st,{x,y,w,h:hh,fontFace:B,fontSize:10.5,bold:i===n-1,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true}); });
  s.addText(e.cap,{x:e.x,y:e.y+e.h-0.26,w:e.w,h:0.3,fontFace:B,fontSize:10.5,italic:true,color:C.mute,align:'center',margin:0,isTextBox:true}); }

function drawLinks(s,e){ const cols=2, gw=0.35, cw=(e.w-gw)/cols; let col=0, y=[e.y,e.y];
  e.groups.forEach(g=>{ const RH=0.36; const need=0.30+g.rows.length*RH+0.08;
    if(y[col]+need>e.y+e.h && col===0) col=1;
    let x=e.x+col*(cw+gw);
    s.addText(g.head,{x,y:y[col],w:cw,h:0.3,fontFace:H,fontSize:e.fs+2.5,bold:true,color:C.slate,margin:0,isTextBox:true});
    y[col]+=0.30;
    g.rows.forEach(r=>{ s.addShape(pres.shapes.OVAL,{x:x+0.04,y:y[col]+0.08,w:0.09,h:0.09,fill:{color:C.orange},line:{color:C.orange}});
      s.addText([{text:r[0]+'  ',options:{color:C.ink}},{text:r[1].replace(/^https?:\/\/(www\.)?/,''),options:{color:C.slate,underline:true,hyperlink:{url:r[1]}}}],
        {x:x+0.22,y:y[col],w:cw-0.22,h:RH-0.02,fontFace:B,fontSize:e.fs,margin:0,valign:'top',isTextBox:true});
      y[col]+=RH; });
    y[col]+=0.08; });
}

// ---- v2.5 primitives: the copy problem and its solution --------------------------------------
function coinbox(s,x,y,lbl,color){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:1.15,h:0.62,fill:{color:C.card},line:{color,width:1.5},rectRadius:0.08});
  s.addShape(pres.shapes.OVAL,{x:x+0.08,y:y+0.14,w:0.34,h:0.34,fill:{color:'E8B94B'},line:{color:'B98A2B',width:1.25}});
  s.addText('₿',{x:x+0.08,y:y+0.14,w:0.34,h:0.34,fontFace:B,fontSize:12,bold:true,color:'7A5A14',align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addText(lbl,{x:x+0.44,y,w:0.72,h:0.62,fontFace:B,fontSize:9.5,color:C.ink,valign:'middle',margin:0,isTextBox:true}); }

function drawCopyviz(s,e){ const cx=e.x+0.25, cy=e.y+e.h/2-0.31;
  coinbox(s,cx,cy,'a coin,\nas a file',C.slate);
  const tx=e.x+e.w-1.75;
  coinbox(s,tx,e.y+0.1,'copy 1\n> Shop A','B6533C');
  coinbox(s,tx,e.y+e.h-0.75,'copy 2\n> Shop B','B6533C');
  line(s,cx+1.2,cy+0.31,tx-0.35,e.y+0.41,'B6533C',2,true);
  line(s,cx+1.2,cy+0.31,tx-0.35,e.y+e.h-0.44,'B6533C',2,true);
  s.addText('perfect copy',{x:(cx+tx)/2-0.6,y:e.y+0.02,w:1.8,h:0.3,fontFace:B,fontSize:10,italic:true,color:'B6533C',margin:0,isTextBox:true});
  s.addText('both shops see valid money - the same money',{x:e.x,y:e.y+e.h+0.02,w:e.w,h:0.3,fontFace:B,fontSize:10.5,italic:true,color:C.mute,align:'center',margin:0,isTextBox:true}); }

function drawDsolve(s,e){ const lx=e.x+0.2, ly=e.y+e.h/2-0.31;
  coinbox(s,lx,ly,"Alice's\ncoin",C.slate);
  const mx=e.x+e.w*0.42;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:mx,y:e.y+0.05,w:2.0,h:0.6,fill:{color:C.card},line:{color:'5B8C5A',width:1.5},rectRadius:0.08});
  s.addText('pay Bob - seen first',{x:mx+0.08,y:e.y+0.05,w:1.84,h:0.6,fontFace:B,fontSize:10,color:C.ink,valign:'middle',margin:0,isTextBox:true});
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:mx,y:e.y+e.h-0.65,w:2.0,h:0.6,fill:{color:C.card},line:{color:'B6533C',width:1.5},rectRadius:0.08});
  s.addText('pay Carol - same coin',{x:mx+0.08,y:e.y+e.h-0.65,w:1.84,h:0.6,fontFace:B,fontSize:10,color:C.ink,valign:'middle',margin:0,isTextBox:true});
  line(s,lx+1.2,ly+0.31,mx-0.1,e.y+0.35,'8A9B94',1.75,true);
  line(s,lx+1.2,ly+0.31,mx-0.1,e.y+e.h-0.35,'8A9B94',1.75,true);
  const bx=e.x+e.w-1.95;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:bx,y:e.y+0.02,w:1.75,h:0.66,fill:{color:'5B8C5A'},line:{color:'5B8C5A'},rectRadius:0.08});
  s.addText([{text:'into the block ',options:{color:C.white,fontSize:10}},{text:'✓',options:{color:C.white,fontSize:12,bold:true}}],{x:bx,y:e.y+0.02,w:1.75,h:0.66,fontFace:B,align:'center',valign:'middle',margin:0,isTextBox:true});
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:bx,y:e.y+e.h-0.68,w:1.75,h:0.66,fill:{color:'F3DED6'},line:{color:'B6533C',width:1.25},rectRadius:0.08});
  s.addText([{text:'refused by every node ',options:{color:'B6533C',fontSize:9.5}},{text:'✗',options:{color:'B6533C',fontSize:12,bold:true}}],{x:bx+0.05,y:e.y+e.h-0.68,w:1.65,h:0.66,fontFace:B,align:'center',valign:'middle',margin:0,isTextBox:true});
  line(s,mx+2.0,e.y+0.35,bx-0.08,e.y+0.35,'5B8C5A',2,true);
  line(s,mx+2.0,e.y+e.h-0.35,bx-0.08,e.y+e.h-0.35,'B6533C',2,true);
  s.addText('every node hears both; the shared ledger keeps only one order',{x:e.x,y:e.y+e.h+0.02,w:e.w,h:0.3,fontFace:B,fontSize:10.5,italic:true,color:C.mute,align:'center',margin:0,isTextBox:true}); }

// ---- v2.6: 5N1K fact row, key analogy, syntax colouring ---------------------------------------
function drawFactrow(s,e){ const gap=0.12, parts=[["WHO",e.who,0.31],["WHERE",e.where,0.31],["WHEN",e.when,0.17],["READ",e.linkText,0.21]];
  let x=e.x; const totW=e.w-3*gap;
  parts.forEach(([k,v,fr],i)=>{ const w=totW*fr, link=i===3;
    const budget=Math.floor((w-0.5)/0.055); let txt=v;
    if(txt.length>budget) txt=txt.slice(0,Math.max(4,budget-1))+'\u2026';
    const fs=txt.length>30?8:9;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:e.y,w,h:0.4,fill:{color:link?C.slate:'EFE9DC'},line:{color:link?C.slate:C.rule,width:0.75},rectRadius:0.2});
    const runs=[{text:k+'  ',options:{bold:true,fontSize:7.5,color:link?'D7E4E0':C.slate}}];
    runs.push(link?{text:txt,options:{fontSize:fs,color:C.white,underline:true,hyperlink:{url:e.link}}}
                  :{text:txt,options:{fontSize:fs,color:C.ink}});
    s.addText(runs,{x:x+0.1,y:e.y,w:w-0.16,h:0.4,fontFace:B,valign:'middle',margin:0,isTextBox:true});
    x+=w+gap; }); }

function drawKeyhouse(s,e){ const colw=(e.w-0.5)/2;
  [[e.x,'your house, your car','One key opens it. Lose the key, lose access. But the deed, the registry, still names you.',C.slate],
   [e.x+colw+0.5,'your bitcoin','The key IS the deed. Signing with it is the only proof of ownership there is.',C.orange]].forEach(([px,t,b,ac],i)=>{
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:px,y:e.y,w:colw,h:e.h,fill:{color:C.card},line:{color:ac,width:1.5},rectRadius:0.1});
    // little house
    const hx=px+0.35, hy=e.y+0.4;
    s.addShape(pres.shapes.RECTANGLE,{x:hx,y:hy+0.3,w:0.7,h:0.5,fill:{color:ac},line:{color:ac}});
    s.addShape(pres.shapes.ISOSCELES_TRIANGLE,{x:hx-0.08,y:hy,w:0.86,h:0.34,fill:{color:ac},line:{color:ac}});
    // key
    const kx=px+1.45, ky=e.y+0.62;
    s.addShape(pres.shapes.OVAL,{x:kx,y:ky,w:0.26,h:0.26,fill:{color:'E8B94B'},line:{color:'B98A2B',width:1.5}});
    s.addShape(pres.shapes.RECTANGLE,{x:kx+0.24,y:ky+0.09,w:0.5,h:0.08,fill:{color:'E8B94B'},line:{color:'B98A2B',width:0.75}});
    s.addShape(pres.shapes.RECTANGLE,{x:kx+0.58,y:ky+0.15,w:0.07,h:0.12,fill:{color:'E8B94B'},line:{color:'B98A2B',width:0.75}});
    s.addText(t,{x:px+0.2,y:e.y+1.08,w:colw-0.4,h:0.34,fontFace:H,fontSize:14,bold:true,color:ac==='D97A14'?C.orange:C.slate,margin:0,isTextBox:true});
    s.addText(b,{x:px+0.2,y:e.y+1.44,w:colw-0.4,h:e.h-1.6,fontFace:B,fontSize:12,color:C.ink,margin:0,valign:'top',isTextBox:true}); }); }

const PYKW=/\b(def|return|for|in|if|else|elif|while|import|from|not|and|or|lambda|True|False|None)\b/g;
function colorLine(t){ const runs=[]; let rest=t;
  const cm=rest.indexOf('#');
  let code=cm>=0?rest.slice(0,cm):rest, comment=cm>=0?rest.slice(cm):null;
  let last=0, m; const rx=/("[^"]*"|'[^']*'|\b\d[\d_]*\.?\d*\b|\b(?:def|return|for|in|if|else|elif|while|import|from|not|and|or|lambda|True|False|None)\b)/g;
  while((m=rx.exec(code))){ if(m.index>last) runs.push({text:code.slice(last,m.index),options:{color:C.codeTxt}});
    const tok=m[0]; let col=C.codeTxt;
    if(/^["']/.test(tok)) col='9ECBFF'; else if(/^\d/.test(tok)) col='FFD28A'; else col='F2A860';
    runs.push({text:tok,options:{color:col,bold:col==='F2A860'}}); last=m.index+tok.length; }
  if(last<code.length) runs.push({text:code.slice(last),options:{color:C.codeTxt}});
  if(comment) runs.push({text:comment,options:{color:'8FA98F',italic:true}});
  if(!runs.length) runs.push({text:'',options:{color:C.codeTxt}});
  return runs; }

function drawCases(s,e){ const n=e.items.length, cols=e.cols||n, gw=0.22, cw=(e.w-(cols-1)*gw)/cols;
  e.items.forEach((c,i)=>{ const x=e.x+(i%cols)*(cw+gw), y=e.y+Math.floor(i/cols)*(e.h+0.2);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:cw,h:e.h,fill:{color:C.card},line:{color:C.rule,width:1},rectRadius:0.1});
    let top=y+0.12;                              // v2.8: an optional photo strip tops the card
    if(c.img){ s.addImage({path:c.img,x:x+0.10,y:y+0.10,w:cw-0.20,h:0.72,sizing:{type:'cover',w:cw-0.20,h:0.72}}); top=y+0.88; }
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:x+0.12,y:top,w:cw-0.24,h:0.36,fill:{color:C.slate},line:{color:C.slate},rectRadius:0.18});
    s.addText([{text:c.place+'  ',options:{bold:true,fontSize:11,color:C.white}},{text:c.year,options:{fontSize:10,color:'D7E4E0'}}],
      {x:x+0.12,y:top,w:cw-0.24,h:0.36,fontFace:B,align:'center',valign:'middle',margin:0,isTextBox:true});
    s.addText(c.text,{x:x+0.14,y:top+0.42,w:cw-0.28,h:y+e.h-0.42-(top+0.42),fontFace:B,fontSize:c.img?9.5:10,color:C.ink,valign:'top',margin:0,isTextBox:true});
    s.addText([{text:'READ →',options:{fontSize:8.5,bold:true,color:C.orange,underline:true,hyperlink:{url:c.link}}}],
      {x:x+0.14,y:y+e.h-0.38,w:cw-0.28,h:0.3,fontFace:B,valign:'middle',margin:0,isTextBox:true}); }); }

const DRAW = {card:drawCard, code:drawCode, prog:drawProg, table:drawTable, boxes:drawBoxes,
              text:drawText, foot:drawFoot, numlist:drawNumList, bullets:drawBullets, question:drawQuestion,
              stat:drawStat, flow:drawFlow, tree:drawTree, net:drawNet, chart:drawChart, chips:drawChips, compare:drawCompare,
              img:drawImg, when:drawWhen, beats:drawBeats, timeline:drawTimelineH, news:drawNews, ledger:drawLedger,
              swap:drawSwap, bars:drawBars, route:drawRoute, claims:drawClaims, chainviz:drawChainviz, funnel:drawFunnel, links:drawLinks, copyviz:drawCopyviz, dsolve:drawDsolve, factrow:drawFactrow, keyhouse:drawKeyhouse, cases:drawCases};

const FOOTER = 'SEN0401 Special Topics in Software Engineering: Block Chain · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University';

plan.slides.forEach((sl,idx)=>{
  const s = pres.addSlide();
  s.background = {color: C.bgc};
  if(sl.kind==='title'){
    [0,1,2].forEach(i=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6+i*1.05,y:1.05,w:0.8,h:0.8,fill:{color:i===2?C.orange:C.slate},line:{color:C.orange,width:1.5},rectRadius:0.1});
      if(i<2) s.addShape(pres.shapes.LINE,{x:1.4+i*1.05,y:1.45,w:0.25,h:0,line:{color:C.orange,width:1.5}}); });
    s.addText('₿',{x:2.7,y:1.05,w:0.8,h:0.8,fontFace:B,fontSize:30,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
    s.addText(sl.title,{x:0.6,y:2.20,w:8.8,h:0.80,fontFace:H,fontSize:36,bold:true,color:C.ink,margin:0,isTextBox:true});
    s.addText(sl.sub,{x:0.6,y:3.00,w:8.8,h:0.70,fontFace:B,fontSize:16,italic:true,color:C.slate,margin:0,valign:'top',isTextBox:true});
    s.addText(FOOTER,{x:0.6,y:4.62,w:8.8,h:0.45,fontFace:B,fontSize:12,color:C.mute,margin:0,isTextBox:true});
    (sl.items||[]).forEach(e=>{ if(e.t==='img') drawImg(s,e); });
  } else if(sl.kind==='section'){
    s.addShape(pres.shapes.RECTANGLE,{x:0,y:0,w:10,h:0.24,fill:{color:C.orange},line:{color:C.orange}});
    s.addShape(pres.shapes.RECTANGLE,{x:0.5,y:1.05,w:0.14,h:1.55,fill:{color:C.orange},line:{color:C.orange}});
    s.addText(sl.title,{x:0.85,y:1.02,w:8.6,h:0.72,fontFace:H,fontSize:32,bold:true,color:C.ink,margin:0,valign:'middle',isTextBox:true});
    s.addText(sl.sub,{x:0.85,y:1.80,w:8.6,h:0.90,fontFace:B,fontSize:15,italic:true,color:C.slate,margin:0,valign:'top',isTextBox:true});
    sl.items.forEach(e=>{ if(e.t==='img'){ drawImg(s,e); } else if(e.t==='boxes'){ const n=e.items.length, cols=Math.max(1,e.cols), rows=Math.ceil(n/cols);
      const gx=0.16, gy=0.14, bw=(e.w-(cols-1)*gx)/cols, bh=(e.h-(rows-1)*gy)/rows;
      e.items.forEach((it,i)=>{ const r=Math.floor(i/cols), c=i%cols, x=e.x+c*(bw+gx), y=e.y+r*(bh+gy);
        s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:bw,h:bh,fill:{color:C.slate},line:{color:C.slate,width:1},rectRadius:0.08});
        s.addText([{text:it.label,options:{bold:true,fontSize:e.fs,color:C.white,breakLine:!!it.sub}},
                   {text:it.sub||'',options:{fontSize:e.subfs,color:'D7E4E0'}}],
          {x:x+0.08,y:y+0.05,w:bw-0.16,h:bh-0.10,fontFace:B,align:'center',valign:'middle',margin:0,isTextBox:true}); }); } });
  } else if(sl.kind==='closing'){
    s.addShape(pres.shapes.RECTANGLE,{x:0,y:0,w:10,h:0.24,fill:{color:C.orange},line:{color:C.orange}});
    s.addText(sl.title,{x:0.6,y:1.45,w:8.8,h:0.95,fontFace:H,fontSize:28,bold:true,color:C.ink,margin:0,valign:'middle',isTextBox:true});
    s.addText(sl.sub,{x:0.6,y:2.40,w:8.8,h:0.60,fontFace:B,fontSize:16,color:C.slate,margin:0,valign:'top',isTextBox:true});
    sl.items.forEach(e=>{ const f=DRAW[e.t]; if(!f) throw new Error('closing: no renderer for '+e.t); f(s,e); });
    s.addText('Questions?',{x:0.6,y:4.82,w:8.8,h:0.50,fontFace:H,fontSize:20,italic:true,color:C.mute,margin:0,isTextBox:true});
  } else {
    head(s, sl.title, sl.sub);
    if(sl.lede) s.addText(sl.lede,{x:0.5,y:1.16,w:9.0,h:0.47,fontFace:B,fontSize:12.5,color:C.ink,margin:0,valign:'middle',isTextBox:true});
    sl.items.forEach(e=>{ const f=DRAW[e.t]; if(!f) throw new Error('slide '+(idx+1)+': no renderer for '+e.t); f(s,e); });
  }
  if(sl.kind!=='title'){
    if(sl.take){ s.addShape(pres.shapes.RECTANGLE,{x:0.5,y:5.07,w:0.1,h:0.34,fill:{color:C.orange},line:{color:C.orange}});
      s.addText(sl.take,{x:0.72,y:5.03,w:7.6,h:0.42,fontFace:H,fontSize:13.5,bold:true,italic:true,color:C.ink,margin:0,valign:'middle',isTextBox:true}); }
    s.addText(String(idx+1)+' / '+plan.slides.length,{x:8.6,y:5.08,w:0.95,h:0.34,fontFace:B,fontSize:11,color:C.mute,align:'right',valign:'middle',margin:0,isTextBox:true});
  }
  if(sl.notes) s.addNotes(sl.notes);
});

pres.writeFile({fileName:process.argv[3]}).then(f=>console.log('written', f, '-', plan.slides.length, 'slides, deck', VERSION));
