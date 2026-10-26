import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1366,'height':768})
    pg.goto('file:///tmp/sen0401_page_test_6rm1wsw1/sen0401_ch01_page_v9_71_0.html'); pg.wait_for_timeout(3000)
    try: pg.evaluate("showTab('chaptercode')")
    except Exception as e: print('showTab',e)
    pg.wait_for_timeout(500)
    for i in (10,0):
        pg.locator("[data-cc-item]").nth(i).click(); pg.wait_for_timeout(300)
        pg.locator("[data-cc-run]").first.click()
        pg.wait_for_function("()=>{const r=document.querySelector('[data-cc-result]');const t=r.textContent.trim();return t.length>0&&!/^Running/.test(t)}",timeout=90000)
        print(i, pg.evaluate("()=>document.querySelector('[data-cc-result]').textContent.trim().slice(0,800)"))
    b.close()
