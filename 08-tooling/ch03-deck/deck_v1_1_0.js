// SEN0401 chapter 3 lecture deck. Draws exactly what deck_plan_v1_1_0.json places and invents nothing:
// the plan is built by ../sen0401_deck_plan_v1_0_0.py from the chapter corpus, the chapter's executed
// examples (examples_out_v1_1_0.json) and the chapter's research record, and it has already checked that
// every piece of text fits the box it is placed in.
// Usage: node deck_v1_1_0.js <out.pptx>
const VERSION = "1.1.0";
const PLAN = "deck_plan_v1_1_0.json";
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const plan = JSON.parse(fs.readFileSync(PLAN)); const M = plan.meta;
const pres = new pptxgen(); pres.layout = 'LAYOUT_16x9'; pres.author = 'Yusuf Altunel';
pres.title = 'SEN0401 ' + M.title;
const C = { dark:'1B1F24', orange:'F7931A', ink:'1F2933', mute:'5B6B7B', card:'F4F2EE', code:'15191E',
            codeTxt:'E6EDF3', green:'7EE787', white:'FFFFFF', slate:'3A4250', rule:'D9D4CC', pale:'C9D1DA' };
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
function drawCode(s,e){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y,w:e.w,h:e.h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  const runs=[]; e.rows.forEach(([st,out],i)=>{ const last=i===e.rows.length-1;
    runs.push({text:'>>> ',options:{color:C.orange,bold:true}});
    runs.push({text:st,options:{color:C.codeTxt,breakLine:!(last&&out==='')}});
    if(out!=='') runs.push({text:out,options:{color:C.green,breakLine:!last}}); });
  s.addText(runs,{x:e.x+0.2,y:e.y+0.13,w:e.w-0.4,h:e.h-0.26,fontFace:MONO,fontSize:e.fs,valign:'top',margin:0,isTextBox:true});
  if(e.cap) s.addText(e.cap,{x:e.x,y:e.y+e.h+0.02,w:e.w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }

// a program the example runs as a whole: its lines verbatim, then the value of result
function drawProg(s,e){ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y,w:e.w,h:e.h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  const runs=e.lines.map((t,i)=>({text:t,options:{color:C.codeTxt,breakLine:i<e.lines.length-1}}));
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

const DRAW = {card:drawCard, code:drawCode, prog:drawProg, table:drawTable, boxes:drawBoxes,
              text:drawText, foot:drawFoot, numlist:drawNumList, bullets:drawBullets, question:drawQuestion};

const FOOTER = 'SEN0401 Special Topics in Software Engineering: Block Chain · Fall 2026 · Yusuf Altunel, PhD · İstanbul Kültür University';

plan.slides.forEach((sl,idx)=>{
  const s = pres.addSlide();
  s.background = {color: sl.bg==='dark' ? C.dark : C.white};
  if(sl.kind==='title'){
    [0,1,2].forEach(i=>{ s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6+i*1.05,y:1.05,w:0.8,h:0.8,fill:{color:i===2?C.orange:C.slate},line:{color:C.orange,width:1.5},rectRadius:0.1});
      if(i<2) s.addShape(pres.shapes.LINE,{x:1.4+i*1.05,y:1.45,w:0.25,h:0,line:{color:C.orange,width:1.5}}); });
    s.addText('₿',{x:2.7,y:1.05,w:0.8,h:0.8,fontFace:B,fontSize:30,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
    s.addText(sl.title,{x:0.6,y:2.20,w:8.8,h:0.80,fontFace:H,fontSize:36,bold:true,color:C.white,margin:0,isTextBox:true});
    s.addText(sl.sub,{x:0.6,y:3.00,w:8.8,h:0.70,fontFace:B,fontSize:16,italic:true,color:C.orange,margin:0,valign:'top',isTextBox:true});
    s.addText(FOOTER,{x:0.6,y:4.62,w:8.8,h:0.45,fontFace:B,fontSize:12,color:C.pale,margin:0,isTextBox:true});
  } else if(sl.kind==='section'){
    s.addShape(pres.shapes.RECTANGLE,{x:0.5,y:1.05,w:0.14,h:1.55,fill:{color:C.orange},line:{color:C.orange}});
    s.addText(sl.title,{x:0.85,y:1.02,w:8.6,h:0.72,fontFace:H,fontSize:32,bold:true,color:C.white,margin:0,valign:'middle',isTextBox:true});
    s.addText(sl.sub,{x:0.85,y:1.80,w:8.6,h:0.90,fontFace:B,fontSize:15,italic:true,color:C.pale,margin:0,valign:'top',isTextBox:true});
    sl.items.forEach(e=>{ if(e.t==='boxes'){ const n=e.items.length, cols=Math.max(1,e.cols), rows=Math.ceil(n/cols);
      const gx=0.16, gy=0.14, bw=(e.w-(cols-1)*gx)/cols, bh=(e.h-(rows-1)*gy)/rows;
      e.items.forEach((it,i)=>{ const r=Math.floor(i/cols), c=i%cols, x=e.x+c*(bw+gx), y=e.y+r*(bh+gy);
        s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:bw,h:bh,fill:{color:C.slate},line:{color:C.orange,width:1},rectRadius:0.08});
        s.addText([{text:it.label,options:{bold:true,fontSize:e.fs,color:C.white,breakLine:!!it.sub}},
                   {text:it.sub||'',options:{fontSize:e.subfs,color:C.pale}}],
          {x:x+0.08,y:y+0.05,w:bw-0.16,h:bh-0.10,fontFace:B,align:'center',valign:'middle',margin:0,isTextBox:true}); }); } });
  } else if(sl.kind==='closing'){
    s.addText(sl.title,{x:0.6,y:1.65,w:8.8,h:0.95,fontFace:H,fontSize:28,bold:true,color:C.white,margin:0,valign:'middle',isTextBox:true});
    s.addText(sl.sub,{x:0.6,y:2.70,w:8.8,h:0.80,fontFace:B,fontSize:16,color:C.orange,margin:0,valign:'top',isTextBox:true});
    s.addText('Questions?',{x:0.6,y:4.20,w:8.8,h:0.60,fontFace:H,fontSize:24,italic:true,color:C.pale,margin:0,isTextBox:true});
  } else {
    head(s, sl.title, sl.sub);
    sl.items.forEach(e=>{ const f=DRAW[e.t]; if(!f) throw new Error('slide '+(idx+1)+': no renderer for '+e.t); f(s,e); });
  }
  if(sl.notes) s.addNotes(sl.notes);
});

pres.writeFile({fileName:process.argv[2]}).then(f=>console.log('written', f, '-', plan.slides.length, 'slides, deck', VERSION));
