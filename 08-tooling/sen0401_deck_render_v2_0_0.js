// sen0401_deck_render v2.0.0 (over v1.3.0, a NEW file for the remedy decks of chapters 5 and 6, 2026-10-22: adds the items 'codex' (a code listing whose line groups are numbered and explained beside it, never a REPL transcript), 'concepts' (a card grid: concept, meaning, everyday analogy), draws every item of a divider (section) slide, numbers the title slide too and gives the divider's subtitle frame the height of one line; every other behaviour is v1.3.0's). v1.3.0 (over v1.1.0: the READ box of a story takes 0.44 of a narrow fact row (0.40 of a full one; WHEN keeps the 0.17 of the shared renderer, WHO and WHERE give way) and wraps a long label onto a second line at 8 pt instead of overflowing; with environment SEN_LITE=1 only the READ card and the links item are changed (the plain shared renderer of chapters 1 to 4, no shapes, no syntax colouring). v1.1.0 text follows: (over v1.0.0: the READ card of a story gets a wider box so that its label names the resource without a truncation mark; the links item takes an optional third column, one line saying what the reader finds there). Previously: v1.0.0 - SEN0401 wrapper over the shared renderer deck_render_v1_0_0.js (which it reads as text and compiles; the shared file is not edited).
// It adds what SEN0414's chapter wrapper (ch24-deck/render_v1_0_0.js) adds - the 'shapes' item (narrative diagrams as native PowerPoint shapes), a title-slide 'foot' item and a table
// cell margin - and one thing SEN0414's shared renderer gets from its programs: SYNTAX COLOURING of the statements of a console (keywords F2A860 bold, strings 9ECBFF, numbers FFD28A,
// comments 8FA98F), as the CME look and feel asks. The statement stays one paragraph '>>> ...' with the same text, so the deck check still finds and re-runs every row.
// Usage (from the chapter's deck folder): NODE_PATH=$(npm root -g) node ../sen0401_deck_render_v1_0_0.js <plan.json> <out.pptx>
const Module = require('module'), fs = require('fs'), path = require('path');
const file = path.resolve(__dirname, 'deck_render_v1_0_0.js');
let src = fs.readFileSync(file, 'utf8');
function swap(a, b) { if (src.indexOf(a) < 0) throw new Error('the shared renderer no longer has the text this wrapper extends: ' + a.slice(0, 60)); src = src.replace(a, b); }
const LITE = process.env.SEN_LITE === '1';
const MARK = 'const DRAW = {card:drawCard,';
const DRAWSHAPES = `
function drawShapes(s,e){ const SH={rect:pres.shapes.RECTANGLE, round:pres.shapes.ROUNDED_RECTANGLE, hex:pres.shapes.HEXAGON, oval:pres.shapes.OVAL};
  e.shapes.forEach(p=>{
    if(p.k==='box'){ const o={x:p.x,y:p.y,w:p.w,h:p.h,fill:{color:p.fill},line:{color:p.line,width:p.lw}}; if(p.shape==='round') o.rectRadius=0.08; s.addShape(SH[p.shape],o); }
    else if(p.k==='line'){ const o={x:Math.min(p.x1,p.x2),y:Math.min(p.y1,p.y2),w:Math.abs(p.x2-p.x1),h:Math.abs(p.y2-p.y1),line:{color:p.color,width:p.w}};
      if(p.arrow) o.line.endArrowType='triangle'; if(p.dash) o.line.dashType='dash';
      if(p.x2<p.x1) o.flipH=true; if(p.y2<p.y1) o.flipV=true;
      if(p.x1!==p.x2 && p.y1!==p.y2){ o.flipH=(p.x2<p.x1); o.flipV=(p.y2<p.y1); }
      s.addShape(pres.shapes.LINE,o); }
    else if(p.k==='text'){ const o={x:p.x,y:p.y,w:p.w,h:p.h,fontFace:B,fontSize:p.fs,color:p.color,bold:p.bold,italic:p.italic,align:p.align,valign:p.valign,margin:0,isTextBox:true}; if(p.fill) o.fill={color:p.fill}; s.addText(p.t,o); }
  }); }
`;
if (!LITE) {
swap(MARK, DRAWSHAPES + '\nconst DRAW = {shapes:drawShapes, card:drawCard,');
swap("runs.push({text:st,options:{color:C.codeTxt,breakLine:!(last&&out==='')}});",
     "{ const rs=colorLine(st); rs[rs.length-1].options=Object.assign({},rs[rs.length-1].options,{breakLine:!(last&&out==='')}); rs.forEach(r=>runs.push(r)); }");
swap("(sl.items||[]).forEach(e=>{ if(e.t==='img') drawImg(s,e); });", "(sl.items||[]).forEach(e=>{ if(e.t==='img') drawImg(s,e); else if(e.t==='foot') drawFoot(s,e); });");
swap("rowH:e.rowH,valign:'middle'}", "rowH:e.rowH,valign:'middle'" + ",...(e.cellMargin?{margin:e.cellMargin}:{})}");

}
const FACT2 = `
function drawFactrow2(s,e){ const gap=0.12, fr=e.w<8?[0.20,0.19,0.17,0.44]:[0.22,0.21,0.17,0.40];
  const parts=[["WHO",e.who,fr[0]],["WHERE",e.where,fr[1]],["WHEN",e.when,fr[2]],["READ",e.linkText,fr[3]]];
  let x=e.x; const totW=e.w-3*gap;
  parts.forEach(([k,v,f],i)=>{ const w=totW*f, link=i===3;
    const budget=Math.floor((w-0.5)/0.055); let txt=v;
    if(!link && txt.length>budget) txt=txt.slice(0,Math.max(4,budget-1))+'\\u2026';
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:e.y,w,h:0.4,fill:{color:link?C.slate:'EFE9DC'},line:{color:link?C.slate:C.rule,width:0.75},rectRadius:0.2});
    const runs=[{text:k+'  ',options:{bold:true,fontSize:7.5,color:link?'D7E4E0':C.slate}}];
    if(link){ const host=e.link.replace(/^https?:\\/\\/(www\\.)?/,'').split('/')[0];
      const line1=(w-0.16-0.32), one=txt.length<=Math.floor(line1/0.068);
      if(one){ runs.push({text:txt,options:{fontSize:9,color:C.white,underline:true,hyperlink:{url:e.link},breakLine:true}});
        runs.push({text:host,options:{fontSize:7,color:'D7E4E0'}}); }
      else runs.push({text:txt,options:{fontSize:8,color:C.white,underline:true,hyperlink:{url:e.link}}}); }
    else runs.push({text:txt,options:{fontSize:txt.length>34?8.5:9,color:C.ink}});
    s.addText(runs,{x:x+0.1,y:e.y,w:w-0.16,h:0.4,fontFace:B,valign:'middle',margin:0,isTextBox:true});
    x+=w+gap; }); }
function drawLinks2(s,e){ const cols=2, gw=0.35, cw=(e.w-gw)/cols; let col=0, y=[e.y,e.y];
  const hasF=e.groups.some(g=>g.rows.some(r=>r[2]));
  const packs=RH=>{ let c=0, yy=[0,0]; for(const g of e.groups){ const need=0.30+g.rows.length*RH+0.08; if(yy[c]+need>e.h && c===0) c=1; if(yy[c]+need>e.h) return false; yy[c]+=need; } return true; };
  const RH=hasF?([0.44,0.40,0.37,0.34].find(packs)||0.34):0.36;
  e.groups.forEach(g=>{ const need=0.30+g.rows.length*RH+0.08;
    if(y[col]+need>e.y+e.h && col===0) col=1;
    let x=e.x+col*(cw+gw);
    s.addText(g.head,{x,y:y[col],w:cw,h:0.3,fontFace:H,fontSize:e.fs+2.5,bold:true,color:C.slate,margin:0,isTextBox:true});
    y[col]+=0.30;
    g.rows.forEach(r=>{ s.addShape(pres.shapes.OVAL,{x:x+0.04,y:y[col]+0.08,w:0.09,h:0.09,fill:{color:C.orange},line:{color:C.orange}});
      const host=r[1].replace(/^https?:\\/\\/(www\\.)?/,'').split('/')[0];
      const runs=r[2]?[{text:r[0],options:{color:C.slate,bold:true,underline:true,hyperlink:{url:r[1]},fontSize:e.fs,breakLine:true}},
                       {text:r[2]+(r[2].length+host.length<=62?'  '+host:''),options:{color:C.ink,fontSize:e.fs-2}}]
                     :[{text:r[0]+'  ',options:{color:C.ink}},{text:r[1].replace(/^https?:\\/\\/(www\\.)?/,''),options:{color:C.slate,underline:true,hyperlink:{url:r[1]}}}];
      s.addText(runs,{x:x+0.22,y:y[col],w:cw-0.22,h:RH-0.02,fontFace:B,fontSize:e.fs,margin:0,valign:'top',isTextBox:true});
      y[col]+=RH; });
    y[col]+=0.08; });
}
`;
if (LITE) swap(MARK, FACT2 + '\n' + MARK); else swap('const DRAW = {shapes:drawShapes,', FACT2 + '\nconst DRAW = {shapes:drawShapes,');
swap('factrow:drawFactrow,', 'factrow:drawFactrow2,');
swap('links:drawLinks,', 'links:drawLinks2,');
// v1.3.0 (over v1.2.0): the colours and the font of the shared renderer's own pictures (newspaper clipping, double-spend, ledger, hash chain, bars, funnel) that are not in the CME look-and-feel standard
// are mapped to the standard's palette and tints (ok = teal slate, wrong = accent orange, the newspaper's black ink = ink); the font Times New Roman becomes Cambria. Nothing else changes. SEN_PALETTE=0 switches it off.
// v1.3.0, caption of a code box or program (env SEN_CAPTION_TOP=1): 'run under Python X' (a program: 'program P, lines a to b of n, run under Python X') is printed on the line of the box's label, right-aligned above the box,
// not below it (code) or inside its bottom edge (compact program), where the next element of the slide and the page number so often stand. The label gives up the caption's width for it when both still fit
// on the box's width; otherwise the caption stays where it was. Nothing else of the box changes.
if (process.env.SEN_CAPTION_TOP === '1') {
  const HELP = "function capW(e){ return Math.min(e.w*0.62, Math.max(1.8, e.cap.length*0.062+0.15)); }\nfunction capTop(e){ return !!(e.cap && e.label && e.cap.length*0.062+0.15<=e.w*0.62 && e.label.length*0.085+capW(e)+0.1<=e.w); }\n";
  const rep = (a, b) => { if (src.indexOf(a) < 0) throw new Error('caption text not found: ' + a.slice(0, 60)); src = src.replace(a, b); };
  rep("function codeLabel(s,e){", HELP + "function codeLabel(s,e){");
  rep("s.addText(e.label,{x:e.x,y:e.y-0.30,w:e.w,h:0.28,", "s.addText(e.label,{x:e.x,y:e.y-0.30,w:capTop(e)?e.w-capW(e)-0.1:e.w,h:0.28,");
  rep("if(e.cap) s.addText(e.cap,{x:e.x,y:e.y+e.h+0.02,w:e.w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }",
      "if(e.cap){ if(capTop(e)) s.addText(e.cap,{x:e.x+e.w-capW(e),y:e.y-0.30,w:capW(e),h:0.28,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',valign:'bottom',margin:0,isTextBox:true}); else s.addText(e.cap,{x:e.x,y:e.y+e.h+0.02,w:e.w,h:0.24,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); } }");
  rep("if(e.compact){ if(e.cap) s.addText(e.cap,{x:e.x+0.2,y:e.y+e.h-0.26,w:e.w-0.4,h:0.22,fontFace:B,fontSize:8,italic:true,color:'8B949E',align:'right',margin:0,isTextBox:true}); return; }",
      "if(e.compact){ if(e.cap){ if(capTop(e)) s.addText(e.cap,{x:e.x+e.w-capW(e),y:e.y-0.30,w:capW(e),h:0.28,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',valign:'bottom',margin:0,isTextBox:true}); else s.addText(e.cap,{x:e.x+0.2,y:e.y+e.h-0.26,w:e.w-0.4,h:0.22,fontFace:B,fontSize:8,italic:true,color:'8B949E',align:'right',margin:0,isTextBox:true}); } return; }");
}
// v1.3.0, geometry the fit check refuses in the shared renderer (all on by default; SEN_GEOM=0 switches them off): the number of a stat tile ends where its label begins; the closing slide's
// 'Questions?' stops left of the page number; a compact program's caption sits below the code frame, which gives up its height.
if (process.env.SEN_GEOM !== '0') {
  const G = [
    ["w:tw-0.24,h:e.h*0.5,fontFace:H", "w:tw-0.24,h:e.h*0.5-0.08,fontFace:H"],
    ["w:e.w-0.24,h:th*0.52,fontFace:H", "w:e.w-0.24,h:th*0.52-0.04,fontFace:H"],
    ["s.addText('Questions?',{x:0.6,y:4.82,w:8.8,", "s.addText('Questions?',{x:0.6,y:4.82,w:7.8,"],
    ["w:e.w-0.4,h:e.h-0.26,fontFace:MONO,fontSize:e.fs,valign:'top',margin:0,isTextBox:true});\n  if(e.compact){", "w:e.w-0.4,h:e.h-0.26-(e.compact&&e.cap&&!(typeof capTop==='function'&&capTop(e))?0.22:0),fontFace:MONO,fontSize:e.fs,valign:'top',margin:0,isTextBox:true});\n  if(e.compact){"]];
  G.forEach(([a, b]) => { if (src.indexOf(a) < 0) throw new Error('geometry text not found: ' + a.slice(0, 50)); src = src.replace(a, b); });
}
// v1.3.0, chips honour their box (SEN_GEOM): the chips are laid out as before (wrapping where a row is full), and when the rows need more height than the item's h the chip height and the row gap shrink
// (down to 0.30 and 0.08 in) so that the last row ends at y+h.
if (process.env.SEN_GEOM !== '0') {
  const a = src.indexOf('function drawChips(s,e){'), b = src.indexOf('x+=w+0.22; }); }', a) + 'x+=w+0.22; }); }'.length;
  if (a < 0 || b < a) throw new Error('drawChips text not found');
  const NEW = `function drawChips(s,e){ const fs=e.fs||13; let hh=e.big?0.58:0.46, gy=0.18;
  const widths=e.items.map(t=>0.42+t.length*fs*0.0115);
  const rowsOf=()=>{ let x=e.x, r=0; const at=[]; widths.forEach(w=>{ if(x+w>e.x+e.w && x>e.x){ x=e.x; r++; } at.push([x,r]); x+=w+0.22; }); return at; };
  const at=rowsOf(), nr=at.length?at[at.length-1][1]+1:1;
  if(e.h && nr>1 && nr*hh+(nr-1)*gy>e.h){ gy=0.08; hh=Math.max(0.30,Math.min(hh,(e.h-(nr-1)*gy)/nr)); }
  e.items.forEach((t,i)=>{ const w=widths[i], x=at[i][0], y=e.y+at[i][1]*(hh+gy);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h:hh,fill:{color:C.card},line:{color:C.orange,width:1},rectRadius:hh/2});
    s.addText(t,{x,y,w,h:hh,fontFace:B,fontSize:fs,bold:!!e.big,color:C.ink,align:'center',valign:'middle',margin:0,isTextBox:true}); }); }`;
  src = src.slice(0, a) + NEW + src.slice(b);
}
// v1.3.0, horizontal timeline (SEN_GEOM): the year and label frames of neighbouring points no longer overlap at the two ends of the line; a frame is cut to the line's own extent, not shifted.
if (process.env.SEN_GEOM !== '0') {
  [["x:Math.max(e.x,Math.min(x-0.6,e.x+e.w-1.2)),y:y-0.52,w:1.2,", "x:Math.max(e.x,x-0.6),y:y-0.52,w:Math.min(x+0.6,e.x+e.w)-Math.max(e.x,x-0.6),"],
   ["x:Math.max(e.x,Math.min(x-0.85,e.x+e.w-1.7)),y:y+0.14,w:1.7,", "x:Math.max(e.x,x-0.85),y:y+0.14,w:Math.min(x+0.85,e.x+e.w)-Math.max(e.x,x-0.85),"]
  ].forEach(([a, b]) => { if (src.indexOf(a) < 0) throw new Error('timeline text not found: ' + a.slice(0, 50)); src = src.replace(a, b); });
}
// v1.3.0, double-spend picture (SEN_GEOM): the two middle boxes shrink with the item's width (2.0 in at most) so that they end left of the two end boxes, which they overlapped in a picture narrower than 6.8 in.
if (process.env.SEN_GEOM !== '0') {
  const a = src.indexOf('function drawDsolve(s,e){'), b = src.indexOf('\n\n', a);
  if (a < 0 || b < a) throw new Error('drawDsolve text not found');
  let f = src.slice(a, b);
  f = f.replace("const mx=e.x+e.w*0.42;", "const mx=e.x+e.w*0.42, PW=Math.max(1.2,Math.min(2.0,e.w-4.15));").split("mx+2.0").join("mx+PW").split("w:2.0,h:0.6").join("w:PW,h:0.6").split("w:1.84,h:0.6").join("w:PW-0.16,h:0.6");
  src = src.slice(0, a) + f + src.slice(b);
}
// v1.3.0, route picture and double-spend picture (SEN_GEOM): the route's caption ends inside the item's own height; a narrow double-spend picture starts its middle boxes earlier.
if (process.env.SEN_GEOM !== '0') {
  const R = [["function drawRoute(s,e){ const n=e.hops.length, y=e.y+e.h*0.4;", "function drawRoute(s,e){ const n=e.hops.length, y=e.y+Math.max(0.25,Math.min(e.h*0.4,e.h-1.06));"],
             ["const mx=e.x+e.w*0.42, PW=Math.max(1.2,Math.min(2.0,e.w-4.15));", "const mx=e.x+e.w*(e.w<6.8?0.36:0.42), PW=Math.max(1.2,Math.min(2.0,e.w<6.8?e.w*0.64-2.45:e.w-4.15));"]];
  R.forEach(([a, b]) => { if (src.indexOf(a) < 0) throw new Error('text not found: ' + a.slice(0, 50)); src = src.replace(a, b); });
}

// ---- v2.0.0 additions -------------------------------------------------------------------------------------------------------------------------
const V2 = `
function drawCodex(s,e){ const fs=e.fs||10, lh=fs*1.3, lhi=lh/72, n=e.lines.length;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x,y:e.y,w:e.w,h:e.h,fill:{color:C.code},line:{color:C.code},rectRadius:0.1});
  const runs=[]; e.lines.forEach((t,i)=>{ const rs=colorLine(t); rs[rs.length-1].options=Object.assign({},rs[rs.length-1].options,{breakLine:i<n-1}); rs.forEach(r=>{ r.options=Object.assign({},r.options,{lineSpacing:lh}); runs.push(r); }); });
  s.addText(runs,{x:e.x+0.45,y:e.y+0.13,w:e.w-0.6,h:e.h-0.26,fontFace:MONO,fontSize:fs,valign:'top',margin:0,isTextBox:true});
  const gs=e.groups, ng=gs.length;
  gs.forEach((g,k)=>{ const py=e.y+0.13+g.line*lhi+(lhi-0.17)/2;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:e.x+0.1,y:py,w:0.24,h:0.17,fill:{color:C.orange},line:{color:C.orange},rectRadius:0.08});
    s.addText(String(k+1),{x:e.x+0.1,y:py,w:0.24,h:0.17,fontFace:B,fontSize:8,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
    const ny=g.ny, nh=g.nh, nx=e.nx, nw=e.nw;
    s.addShape(pres.shapes.OVAL,{x:nx,y:ny+0.06,w:0.28,h:0.28,fill:{color:C.orange},line:{color:C.orange}});
    s.addText(String(k+1),{x:nx,y:ny+0.06,w:0.28,h:0.28,fontFace:H,fontSize:11,bold:true,color:C.white,align:'center',valign:'middle',margin:0,isTextBox:true});
    s.addText(g.note,{x:nx+0.38,y:ny,w:nw-0.38,h:nh,fontFace:B,fontSize:e.nfs||11,color:C.ink,valign:'top',margin:0,isTextBox:true}); });
  if(e.cap) s.addText(e.cap,{x:e.x,y:e.y+e.h+0.03,w:e.w,h:0.22,fontFace:B,fontSize:9,italic:true,color:C.mute,align:'right',margin:0,isTextBox:true}); }
function drawConcepts(s,e){ const n=e.items.length, cols=e.cols, rows=Math.ceil(n/cols), gx=0.16, gy=0.14, bw=(e.w-(cols-1)*gx)/cols, bh=(e.h-(rows-1)*gy)/rows;
  e.items.forEach((it,i)=>{ const r=Math.floor(i/cols), c=i%cols, x=e.x+c*(bw+gx), y=e.y+r*(bh+gy);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w:bw,h:bh,fill:{color:C.card},line:{color:C.rule},rectRadius:0.08});
    s.addShape(pres.shapes.RECTANGLE,{x:x+0.02,y:y+0.14,w:0.07,h:bh-0.28,fill:{color:C.orange},line:{color:C.orange}});
    const t=[{text:it.label,options:{bold:true,fontFace:H,fontSize:e.fs+1.5,color:C.dark,breakLine:true}},
             {text:it.meaning,options:{fontSize:e.fs,color:C.ink,breakLine:true}},
             {text:'Like '+it.analogy,options:{fontSize:e.fs,italic:true,color:C.slate}}];
    s.addText(t,{x:x+0.2,y:y+0.07,w:bw-0.3,h:bh-0.14,fontFace:B,valign:'top',margin:0,paraSpaceAfter:3,isTextBox:true}); }); }
`;
swap('const DRAW = {shapes:drawShapes,', V2 + '\nconst DRAW = {codex:drawCodex, concepts:drawConcepts, shapes:drawShapes,');
// every item of a divider (section) slide is drawn (v1.3.0 drew pictures and boxes only), the subtitle frame is one line high, the title slide is numbered too
swap("s.addText(sl.sub,{x:0.85,y:1.80,w:8.6,h:0.90,", "s.addText(sl.sub,{x:0.85,y:1.80,w:8.6,h:0.42,");
swap("  if(sl.kind!=='title'){\n    if(sl.take)", "  if(sl.kind==='section') sl.items.forEach(e=>{ if(e.t!=='img'&&e.t!=='boxes'){ const f=DRAW[e.t]; if(!f) throw new Error('section: no renderer for '+e.t); f(s,e); } });\n  if(sl.kind==='title') s.addText(String(idx+1)+' / '+plan.slides.length,{x:8.6,y:5.08,w:0.95,h:0.34,fontFace:B,fontSize:11,color:C.mute,align:'right',valign:'middle',margin:0,isTextBox:true});\n  if(sl.kind!=='title'){\n    if(sl.take)");

if (process.env.SEN_PALETTE !== '0') {
  const MAP = {B6533C:'D97A14', '5B8C5A':'2F6D62', '3C6B3B':'2F6D62', F3DED6:'EFE6D6', '1A1A1A':'2B2622', '444444':'6E655C', B9AE9C:'C9BFAE', FFFDF7:'FBF8F2', D8D0C2:'DFD6C7', '9A9183':'6E655C',
               E8B94B:'D97A14', B98A2B:'D97A14', '7A5A14':'2B2622', '8A9B94':'6E655C', '54504A':'6E655C', BBB1A2:'DFD6C7'};
  src = src.replace(/\b([0-9A-Fa-f]{6})\b/g, (m0, h) => MAP[h.toUpperCase()] || m0).replace(/Times New Roman/g, 'Cambria');
}
const m = new Module(file, module); m.filename = file; m.paths = Module._nodeModulePaths(path.dirname(file)); m._compile(src, file);
