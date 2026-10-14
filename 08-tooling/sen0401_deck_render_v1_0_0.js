// sen0401_deck_render v1.0.0 - SEN0401 wrapper over the shared renderer deck_render_v1_0_0.js (which it reads as text and compiles; the shared file is not edited).
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
const m = new Module(file, module); m.filename = file; m.paths = Module._nodeModulePaths(path.dirname(file)); m._compile(src, file);
