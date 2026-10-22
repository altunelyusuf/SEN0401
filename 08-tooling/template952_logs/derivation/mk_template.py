#!/usr/bin/env python3
# derives course_page_template_v9_52_0.html from the committed v9_51_1 (never edited) by exact, counted replacements
import sys
SRC = "/home/claude/sen0401/08-tooling/course_page_template_v9_51_1.html"
DST = "/home/claude/sen0401/08-tooling/course_page_template_v9_52_0.html"
t = open(SRC).read()
def rep(a, b, c=1):
    global t
    n = t.count(a)
    if n != c: raise SystemExit("expected %d occurrence(s), found %d, of: %s" % (c, n, a[:120]))
    t = t.replace(a, b)

# ---- 0. head: version comment, the page-standard declaration -------------------------------------------------------------
VERSION = open("/tmp/claude-0/s17/t_version.txt").read().strip()
rep('<!-- course_page_template version 9.51.1:', '<!-- course_page_template version 9.52.0: ' + VERSION + ' Before: --><!-- course_page_template version 9.51.1:')
rep('<meta name="version" content="__PAGEVERSION__">', '<meta name="version" content="__PAGEVERSION__"><meta name="page-standard" content="9.52">')

# ---- 1. CSS --------------------------------------------------------------------------------------------------------------
rep('</style></head><body>', open("/tmp/claude-0/s17/t_css.css").read().strip() + '\n</style></head><body>')

# ---- 2. the Learn menu: the chapter-code tab, one row of tabs, subjects as numbered tabs ---------------------------------
rep("...(D.stories&&D.stories.length?[['stories','📜 Stories']]:[]),...tops.map(",
    "...(D.stories&&D.stories.length?[['stories','📜 Stories']]:[]),...(CC.length?[['chaptercode','💻 Chapter code']]:[]),...tops.map(")
rep("""const subbarHTML=g=>'<div class="subtabs viewsub" role="tablist" aria-label="'+esc(VIEWS.find(v=>v[0]===g)[1])+'">'+GROUPS[g].map(([k,l])=>'<button role="tab" data-tab="'+k+'">'+esc(l)+'</button>').join('')+'</div>',subbar=g=>'';""",
    """const subbarHTML=g=>{let sep=false;return '<div class="subtabs viewsub" role="tablist" aria-label="'+esc(VIEWS.find(v=>v[0]===g)[1])+'">'+GROUPS[g].map(([k,l])=>{const nd=byId[k];
 if(g==='learn'&&nd&&nd.level===1){const i=tops.findIndex(t=>t.id===k)+1,lead=sep?'':'<span class="tabsep" role="presentation" data-tip="One tab for each subject of the chapter. The name of the open subject is in the line below; the explorer on the left lists them all.">Subjects</span>';sep=true;return lead+'<button role="tab" class="subjtab" data-tab="'+k+'" data-tip="'+esc(nd.label)+'" aria-label="Subject '+i+', '+esc(nd.label)+'">'+i+'</button>'}
 return '<button role="tab" data-tab="'+k+'">'+esc(l)+'</button>'}).join('')+'</div>'},subbar=g=>'';""")
rep("""'<button data-tab="intro" aria-current="page">🏠 Start</button>'+VIEWS.map(([k,l])=>'<button data-tab="'+k+'">'+l+'</button>').join('')""",
    """'<button role="tab" data-tab="intro" aria-current="page">🏠 Start</button>'+VIEWS.map(([k,l])=>'<button role="tab" data-tab="'+k+'">'+l+'</button>').join('');document.getElementById('groups').setAttribute('role','tablist')""")
# the data the chapter-code tab reads is declared with the other page data
rep("const ICON={1:'📁',2:'📂',3:'🔷'},", "const CC=(D.chaptercode&&D.chaptercode.examples)||[];\n// the Playground lists names: the part before a colon, a bracketed note after a dash, an equals sign as the word, at most 56 characters; the whole text stays in the item's tooltip\nconst pgName=s=>{let t=String(s);const i=t.indexOf(': ');if(i>0&&i<=48)t=t.slice(0,i);t=t.replace(/\\s*[(\\[{]([^)\\]}]*)[)\\]}]/g,' \u2013 $1').trim();t=t.replace(/\\s*=\\s*/g,' equals ');return t.length>56?t.slice(0,55).trimEnd()+'\u2026':t};\nconst ICON={1:'📁',2:'📂',3:'🔷'},")

# ---- 3. the panel level ---------------------------------------------------------------------------------------------------
rep("""'<section id="s-'+m.id+'" data-source="'+esc(m.section_iri)+'" data-concept="'+m.id+'" class="midhead">""",
    """'<section id="s-'+m.id+'" data-source="'+esc(m.section_iri)+'" data-concept="'+m.id+'" data-panel="'+m.id+'" class="midhead">""")
rep("""'<section id="s-'+n.id+'" data-source="'+esc(n.section_iri)+'" data-concept="'+n.id+'" class="'+(n.level===3?'leaf':'')+'"'""",
    """'<section id="s-'+n.id+'" data-source="'+esc(n.section_iri)+'" data-concept="'+n.id+'" data-panel="'+n.id+'" class="'+(n.level===3?'leaf':'')+'"'""")
rep("""'<div class="cards widget" id="w-'+m.id+'">'+kids(m.id).map(l=>sec(l,'h4')).join('')+'</div></div>'""",
    """'<div class="cards widget" id="w-'+m.id+'"><p class="panelhint">'+kids(m.id).length+(kids(m.id).length===1?' concept':' concepts')+' in <b>'+esc(m.label)+'</b>, one panel for each. Choose one in the row above, or <button class="btn" data-go="'+(kids(m.id)[0]||{}).id+'">start with '+esc((kids(m.id)[0]||{}).label||'')+' ▶</button></p>'+kids(m.id).map(l=>sec(l,'h4')).join('')+'</div></div>'""")
rep("""function showSub(m,focus){const p=m.startsWith('ov-')?m.slice(3):byId[m].parent;const pane=panes.querySelector('[data-pane="'+p+'"]');
 pane.querySelectorAll('[data-subpane]').forEach(x=>{x.hidden=x.dataset.subpane!==m;if(!x.hidden){x.querySelectorAll('.cards > section.leaf').forEach(sc=>sc.hidden=!!focus&&sc.dataset.concept!==focus);x.querySelectorAll('section.midhead').forEach(sc=>sc.hidden=!!focus);x.classList.toggle('focused',!!focus)}});""",
    """function showSub(m,focus,all){const p=m.startsWith('ov-')?m.slice(3):byId[m].parent;const pane=panes.querySelector('[data-pane="'+p+'"]');
 // 9.52.0: a group holds panels, one concept in each. Opening a group shows the group's own panel; a concept shows its panel alone; 'all' (Show all) is the one way to see every panel of the group together.
 pane.querySelectorAll('[data-subpane]').forEach(x=>{x.hidden=x.dataset.subpane!==m;if(!x.hidden){const grp=!m.startsWith('ov-');x.querySelectorAll('.cards > section.leaf').forEach(sc=>sc.hidden=focus?sc.dataset.concept!==focus:(grp&&!all));x.querySelectorAll('section.midhead').forEach(sc=>sc.hidden=!!focus);x.classList.toggle('focused',!!focus);x.classList.toggle('paneled',grp&&!focus&&!all)}});""")
rep("""const s=t.closest('[data-sub]');if(s){showSub(s.dataset.sub);return}""",
    """const s=t.closest('[data-sub]');if(s){showSub(s.dataset.sub,null,!!s.closest('.crumbs'));return}""")


# ---- 3b. a panel is one screen: its text and its pictures are two regions of one box ------------------------------------------
rep("""function richInner(n,tag){return secHead(n,tag)+'<div class="cgrid"><div class="ctext">'+bodyHtml(n)+storychips(n)+'</div><div class="nbh" data-nbhfor="'+n.id+'"></div></div>'+ndSlot(n)+secVis(n)+chartBox(n)+widget(n)}""",
    """function richInner(n,tag){return secHead(n,tag)+'<div class="cgrid pbody"><div class="ctext">'+bodyHtml(n)+storychips(n)+'</div><div class="pright"><div class="nbh" data-nbhfor="'+n.id+'"></div>'+ndSlot(n)+secVis(n)+chartBox(n)+widget(n)+'</div></div>'}""")
rep("""'+secHead(n,tag)+bodyHtml(n)+(n.level<3?ndSlot(n):'')+chartBox(n)+widget(n)+secVis(n)+'</section>'}""",
    """'+secHead(n,tag)+(n.level<3?'<div class="cgrid pbody"><div class="ctext">'+bodyHtml(n)+widget(n)+'</div><div class="pright">'+ndSlot(n)+chartBox(n)+secVis(n)+'</div></div>':bodyHtml(n)+chartBox(n)+widget(n)+secVis(n))+'</section>'}""")
rep("""</h3>'+bodyHtml(m)+ndSlot(m)+secVis(m)+'</section>'}""", """</h3><div class="cgrid pbody"><div class="ctext">'+bodyHtml(m)+'</div><div class="pright">'+ndSlot(m)+secVis(m)+'</div></div></section>'}""")

# ---- 4. the Playground lists names; the code opens in the editor --------------------------------------------------------
rep("""<div class="row"><select id="pex" aria-label="Examples"><option value="first">'+esc(D.course.playground.label)+'</option>'+D.nodes.filter(n=>n.io).map(n=>'<option value="'+n.id+'">'+esc(n.label)+': '+esc(n.io.code)+'</option>').join('')+'</select></div>""",
    """<div class="row pgrow"><select id="pex" class="pglist" size="7" aria-label="Examples, by name"><option value="first" data-pg-item selected title="'+esc(D.course.playground.label)+'">'+esc(pgName(D.course.playground.label))+'</option>'+D.nodes.filter(n=>n.io).map(n=>'<option value="'+n.id+'" data-pg-item title="'+esc(n.label)+'">'+esc(pgName(n.label))+'</option>').join('')+'</select></div>""")
rep("""s.innerHTML='<option value="first">'+esc(D.course.playground.label)+'</option><optgroup label="Examples from this chapter">'+ex.map(o=>o.outerHTML).join('')+'</optgroup><optgroup label="Code patterns (each one runs as it is)">'+ED_TPL.map((t,i)=>'<option value="tpl:'+i+'">'+esc(t[0])+'</option>').join('')+'</optgroup>'})();""",
    """s.innerHTML='<option value="first" data-pg-item selected title="'+esc(D.course.playground.label)+'">'+esc(pgName(D.course.playground.label))+'</option><optgroup label="Examples from this chapter">'+ex.map(o=>o.outerHTML).join('')+'</optgroup><optgroup label="Code patterns (each one runs as it is)">'+ED_TPL.map((t,i)=>'<option value="tpl:'+i+'" data-pg-item title="'+esc(t[0])+'">'+esc(pgName(t[0]))+'</option>').join('')+'</optgroup>'})();""")
rep("""<textarea class="code" id="pcode" data-fill="0.5" style="min-height:9rem\"""", """<textarea class="code" id="pcode" data-fill="0.5" style="min-height:7rem\"""")

# ---- 5. the chapter-code pane and its behaviour -----------------------------------------------------------------------------
rep("P+=cheatPane();P+=exercisesPane();", "if(CC.length)P+=ccPane();P+=cheatPane();P+=exercisesPane();")
rep("function goTo(id){", open("/tmp/claude-0/s17/t_cc.js").read().strip() + "\nfunction goTo(id){")
# code areas inside a panel stay short, so a panel keeps within one screen

rep("document.querySelectorAll('textarea.code:not([data-fill])').forEach(t=>{", "fitPanels();document.querySelectorAll('textarea.code:not([data-fill])').forEach(t=>{")
rep("crumbs(p,m,focus);syncTree();enrich(pane)}","crumbs(p,m,focus);syncTree();enrich(pane);setTimeout(fitViews,0)}")
rep("""'<section class="leaf" style="margin-bottom:.7rem"><h3>'""", """'<section class="pgroup" style="margin-bottom:.7rem"><h3>'""")
rep("""'<section class="leaf" style="margin-bottom:.6rem"><h4>'+esc(h)+'</h4><p>'""", """'<section class="pgroup" style="margin-bottom:.6rem"><h5>'+esc(h)+'</h5><p>'""")
# Ctrl+Enter runs the chapter-code editor as it runs the Playground
rep("if(mod&&k==='Enter'&&ta.id==='pcode'){", "if(mod&&k==='Enter'&&ta.hasAttribute('data-cc-editor')){e.preventDefault();ccRun();return}\n if(mod&&k==='Enter'&&ta.id==='pcode'){")
open(DST, "w").write(t)
print("written", DST, len(t))
