#!/usr/bin/env python3
"""Patches course_page_template_v9_39_0.html into course_page_template_v9_40_0.html.

One subject, the owner's review of 2026-10-07 10:10: "ERD connections are missing."

Measured on the 9.38.0 chapter 1 page: the ERD opened on the chapter's six subjects with only the two
operates-on relationships drawn, because the document's mentioned-together links were an opt-in toggle (off by
default, 9.37.0). Six boxes and two lines read as a diagram without connections. The data holds many more:
with the toggle on, the subjects view draws every pair of subjects whose concepts the document mentions together,
counted, and the sections view 139 such lines.

9.40.0: the mentioned-together relationships are on by default in both views (the toggle remains, to switch them
off); in the sections view the entities are grouped under their subject and each header is tinted with its
subject's colour, with a legend above the diagram, so the hierarchy reads without extra lines; the stated
operates-on lines keep their heavier stroke so the two kinds stay apart.
"""
__version__ = "9.40.0"

SRC, DST = "course_page_template_v9_39_0.html", "course_page_template_v9_40_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

rep("const ERD={mode:'subjects',mentions:false};", "const ERD={mode:'subjects',mentions:true};const ERD_TONES=['#D9C4A3','#B9D1C9','#E6C9B3','#C9CDE0','#D5D9B8','#E3C2C2','#C7D6D2','#E0D0B8'];", 1)
rep('<button class="chip" data-erdm="1" aria-pressed="false">mentioned together</button>', '<button class="chip" data-erdm="1" aria-pressed="true">mentioned together</button>', 1)
# the model carries a tone per entity (its subject's index) and a legend
rep("ENT[e.id]={x:20+(i%COLS)*(BW+GX),y:30+Math.floor(i/COLS)*(30+7*16+10+GY),label:e.label,attrs:attrs.length?attrs:['(no parts)'],n:()=>leaves.length,sample:()=>leaves.map(x=>x.label),id:e.id}});",
    "ENT[e.id]={x:20+(i%COLS)*(BW+GX),y:30+Math.floor(i/COLS)*(30+7*16+10+GY),label:e.label,attrs:attrs.length?attrs:['(no parts)'],n:()=>leaves.length,sample:()=>leaves.map(x=>x.label),id:e.id,tone:ERD_TONES[tops.findIndex(s=>s.id===topOf(e.id))%ERD_TONES.length],subject:byId[topOf(e.id)].label}});", 1)
rep("<rect class=\"oe-hd\" x=\"'+b.x+'\" y=\"'+b.y+'\" width=\"'+b.w+'\" height=\"26\" rx=\"6\"/>",
    "<rect class=\"oe-hd\" x=\"'+b.x+'\" y=\"'+b.y+'\" width=\"'+b.w+'\" height=\"26\" rx=\"6\"'+(e.tone?' style=\"fill:'+e.tone+'\"':'')+'/>", 1)
# legend of subjects in the sections view, drawn into the control row's note
rep("function erdApply(){if(ERD.mode==='schema'){OE_ENT=OE_SCHEMA_ENT;OE_REL=OE_SCHEMA_REL;return {W:990,H:400}}const m=cerdModel();OE_ENT=m.ENT;OE_REL=m.REL;",
    "function erdLegend(){const el=document.getElementById('erdctl');if(!el)return;let p=el.querySelector('.erdlegend');if(!p){p=document.createElement('p');p.className='note erdlegend';el.appendChild(p)}if(ERD.mode!=='sections'){p.hidden=true;return}p.hidden=false;p.innerHTML='Sections grouped by subject: '+tops.map((s,i)=>'<span style=\"background:'+ERD_TONES[i%ERD_TONES.length]+';padding:0 .4rem;border-radius:4px;margin-right:.3rem\">'+esc(s.label)+'</span>').join('')}"
    " function erdApply(){erdLegend();if(ERD.mode==='schema'){OE_ENT=OE_SCHEMA_ENT;OE_REL=OE_SCHEMA_REL;return {W:990,H:400}}const m=cerdModel();OE_ENT=m.ENT;OE_REL=m.REL;", 1)
# the stated operates-on lines keep a heavier stroke: the relationship group carries its kind
rep("s+='<g class=\"oe-r\"><title>'+esc(OE_ENT[a].label+' '+verb+' '+OE_ENT[b].label",
    "s+='<g class=\"oe-r'+(/^mentioned/.test(verb)?' oe-me':'')+'\"><title>'+esc(OE_ENT[a].label+' '+verb+' '+OE_ENT[b].label", 1)
rep("</style>", ".onto svg .oe-r.oe-me line{stroke-dasharray:6 4;opacity:.7}\n</style>", 1)
rep("<h2>🔗 Entity-relationship diagram</h2><p class=\"legend\"><span>| one</span><span>crow\\'s foot: many</span><span>○ optional</span></p>",
    "<h2>🔗 Entity-relationship diagram</h2><p class=\"legend\"><span>| one</span><span>crow\\'s foot: many</span><span>○ optional</span><span>━ operates on</span><span>┅ mentioned together</span></p>", 1)
rep("<!-- course_page_template version 9.39.0:",
    "<!-- course_page_template version 9.40.0: the ERD draws its connections by default - the mentioned-together "
    "relationships are on in both views (dashed, the stated operates-on lines solid), and in the sections view the "
    "entities are grouped and tinted by subject with a legend, so the hierarchy reads without extra lines. Earlier: "
    "--><!-- course_page_template version 9.39.0:", 1)
open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
