import sys, json, time
from playwright.sync_api import sync_playwright
page = sys.argv[1]
RL = open(sys.argv[2]).read()
OV = "()=>{const svg=document.querySelector('#graph svg');const C=svg.rlCenters();const ov=(a,b)=>Math.abs(a.x-b.x)<(a.w+b.w)/2&&Math.abs(a.y-b.y)<(a.h+b.h)/2;const pairs=[];for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++)if(ov(C[i],C[j]))pairs.push([C[i].id,C[j].id,Math.round(C[i].x),Math.round(C[i].y),Math.round(C[j].x),Math.round(C[j].y)]);const E=svg.rlEdges();const idx={};C.forEach(c=>idx[c.id]=c);let L=0;E.forEach(([a,b])=>{L+=Math.hypot(idx[a].x-idx[b].x,idx[a].y-idx[b].y)});return {boxes:C.length,overlaps:pairs.length,pairs,edges:E.length,meanEdge:Math.round(L/Math.max(E.length,1)),outside:C.filter(c=>c.x-c.w/2<-0.5||c.y-c.h/2<-0.5).length}}"
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(locale="en-US", viewport={"width":1400,"height":900}); pg = ctx.new_page()
    pg.goto("file://"+page); pg.wait_for_timeout(1500)
    GROUP = pg.evaluate("GROUP_OF")
    def view(k):
        g = GROUP.get(k)
        if g:
            view(g)
            if not pg.locator('[data-pane="%s"]' % k).is_visible(): pg.click('[data-pane]:not([hidden]) .viewsub [data-tab="%s"]' % k)
        else: pg.click('#groups [data-tab="%s"]' % k)
    view("map"); pg.wait_for_timeout(400)
    print("drawn layout:", json.dumps(pg.evaluate(OV))[:400])
    a = pg.evaluate(RL); print("dragged box", a["id"] if a else None)
    pg.mouse.move(a["cx"], a["cy"]); pg.mouse.down(); pg.mouse.move(a["cx"]+40, a["cy"]+25, steps=5); pg.mouse.move(a["cx"]+90, a["cy"]+50, steps=5); pg.mouse.up(); pg.wait_for_timeout(300)
    print("after drag:", json.dumps(pg.evaluate(OV))[:400])
    t=time.time(); pg.click('[data-mrl="untangle"]'); pg.wait_for_function("()=>!document.querySelector('#graph svg').dataset.busy", timeout=120000); pg.wait_for_timeout(300)
    print("untangle took ms", int((time.time()-t)*1000))
    u = pg.evaluate(OV); print("AFTER UNTANGLE: boxes", u["boxes"], "overlaps", u["overlaps"], "meanEdge", u["meanEdge"], "outside", u["outside"], "pairs", u["pairs"])
    pg.click('[data-mrl="reset"]'); pg.wait_for_timeout(200)
    print("reset: moved boxes", pg.evaluate("()=>[...document.querySelectorAll('#graph svg g[data-c]')].filter(g=>g.getAttribute('transform')).length"))
    b.close()
