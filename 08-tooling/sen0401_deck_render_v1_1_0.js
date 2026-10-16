// sen0401_deck_render v1.1.0 (over v1.0.0: the READ card of a story gets a wider box so that its label names the resource without a truncation mark; the links item takes an optional third column, one line saying what the reader finds there). Previously: v1.0.0 - SEN0401 wrapper over the shared renderer deck_render_v1_0_0.js (which it reads as text and compiles; the shared file is not edited).
// It adds what SEN0414's chapter wrapper (ch24-deck/render_v1_0_0.js) adds - the 'shapes' item (narrative diagrams as native PowerPoint shapes), a title-slide 'foot' item and a table
// cell margin - and one thing SEN0414's shared renderer gets from its programs: SYNTAX COLOURING of the statements of a console (keywords F2A860 bold, strings 9ECBFF, numbers FFD28A,
// comments 8FA98F), as the CME look and feel asks. The statement stays one paragraph '>>> ...' with the same text, so the deck check still finds and re-runs every row.
// Usage (from the chapter's deck folder): NODE_PATH=$(npm root -g) node ../sen0401_deck_render_v1_0_0.js <plan.json> <out.pptx>
const Module = require('module'), fs = require('fs'), path = require('path');
const file = path.resolve(__dirname, 'deck_render_v1_0_0.js');
let src = fs.readFileSync(file, 'utf8');
function swap(a, b) { if (src.indexOf(a) < 0) throw new Error('the shared renderer no longer has the text this wrapper extends: ' + a.slice(0, 60)); src = src.replace(a, b); }
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
swap(MARK, DRAWSHAPES + '\nconst DRAW = {shapes:drawShapes, card:drawCard,');
swap("runs.push({text:st,options:{color:C.codeTxt,breakLine:!(last&&out==='')}});",
     "{ const rs=colorLine(st); rs[rs.length-1].options=Object.assign({},rs[rs.length-1].options,{breakLine:!(last&&out==='')}); rs.forEach(r=>runs.push(r)); }");
swap("(sl.items||[]).forEach(e=>{ if(e.t==='img') drawImg(s,e); });", "(sl.items||[]).forEach(e=>{ if(e.t==='img') drawImg(s,e); else if(e.t==='foot') drawFoot(s,e); });");
swap("rowH:e.rowH,valign:'middle'}", "rowH:e.rowH,valign:'middle'" + ",...(e.cellMargin?{margin:e.cellMargin}:{})}");

const FACT2 = `
function drawFactrow2(s,e){ const gap=0.12, parts=[["WHO",e.who,0.24],["WHERE",e.where,0.23],["WHEN",e.when,0.13],["READ",e.linkText,0.40]];
  let x=e.x; const totW=e.w-3*gap;
  parts.forEach(([k,v,fr],i)=>{ const w=totW*fr, link=i===3;
    const budget=Math.floor((w-0.5)/0.055); let txt=v;
    if(!link && txt.length>budget) txt=txt.slice(0,Math.max(4,budget-1))+'\\u2026';
    const fs=txt.length>34?8.5:9;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:e.y,w,h:0.4,fill:{color:link?C.slate:'EFE9DC'},line:{color:link?C.slate:C.rule,width:0.75},rectRadius:0.2});
    const runs=[{text:k+'  ',options:{bold:true,fontSize:7.5,color:link?'D7E4E0':C.slate}}];
    if(link){ const host=e.link.replace(/^https?:\\/\\/(www\\.)?/,'').split('/')[0];
      runs.push({text:txt,options:{fontSize:fs,color:C.white,underline:true,hyperlink:{url:e.link},breakLine:true}});
      runs.push({text:host,options:{fontSize:7,color:'D7E4E0'}}); }
    else runs.push({text:txt,options:{fontSize:fs,color:C.ink}});
    s.addText(runs,{x:x+0.1,y:e.y,w:w-0.16,h:0.4,fontFace:B,valign:'middle',margin:0,isTextBox:true});
    x+=w+gap; }); }
function drawLinks2(s,e){ const cols=2, gw=0.35, cw=(e.w-gw)/cols; let col=0, y=[e.y,e.y];
  e.groups.forEach(g=>{ const RH=g.rows.some(r=>r[2])?0.44:0.36; const need=0.30+g.rows.length*RH+0.08;
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
swap('const DRAW = {shapes:drawShapes,', FACT2 + '\nconst DRAW = {shapes:drawShapes,');
swap('factrow:drawFactrow,', 'factrow:drawFactrow2,');
swap('links:drawLinks,', 'links:drawLinks2,');
const m = new Module(file, module); m.filename = file; m.paths = Module._nodeModulePaths(path.dirname(file)); m._compile(src, file);
