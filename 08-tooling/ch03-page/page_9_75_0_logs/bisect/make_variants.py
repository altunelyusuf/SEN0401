#!/usr/bin/env python3
# makes the scratch variants of the page 9.74.0 used by the bisect (as run on 2026-11-01/02): one difference to the shipped 9.73.0 undone at a time, built with builder 4.19.0 into /tmp/i60/<name>
# v1 / v1b: concept examples (io) of 9.73.0 | v2: Lecture tab of 9.73.0 | v3: chapter-code listing of 9.73.0 | v4: template 9.52.4 | v5: all three data differences undone, template 9.52.9 | v6: the same, template 9.52.4
# (v1 changed the page only, the test still typed the plain code of its page data; v1b changed page and test data together: that is the plain-code undo)
import json,os,subprocess,shutil
R='/home/claude/sen0401/08-tooling/ch03-page/'
a=json.load(open(R+'page_data_v9_73_0.json'));b=json.load(open(R+'page_data_v9_74_0.json'))
na={n['id']:n for n in a['nodes']}
def mk(name,mut,tpl=None):
    d=json.loads(json.dumps(b)); mut(d)
    S='/tmp/i60/'+name; shutil.rmtree(S,ignore_errors=True); os.makedirs(S+'/d',exist_ok=True)
    json.dump(d,open(S+'/d/page_data_v9_74_0.json','w'),ensure_ascii=False)
    shutil.copy(R+'extra_resolved_v9_74_0.html',S+'/d/')
    env=dict(os.environ,PAGE_VER='9_74_0',PAGE_DATA_DIR=S+'/d',PAGE_SCRATCH=S)
    if tpl: env['PAGE_TEMPLATE']=tpl
    r=subprocess.run(['python3','-B','08-tooling/sen0401_page_build_v4_19_0.py','03'],env=env,capture_output=True,text=True)
    print(name,r.returncode,r.stderr[-200:],os.path.getsize(S+'/sen0401_ch03_page_v9_74_0.html'))
def io(d):
    for n in d['nodes']:
        o=na[n['id']]
        if 'io' in o: n['io']=o['io']
        else: n.pop('io',None)
def allold(d): io(d); d['lecture']=a['lecture']; d['chaptercode']=a['chaptercode']
mk('v1_noplain',io); mk('v2_oldlecture',lambda d:d.__setitem__('lecture',a['lecture'])); mk('v3_oldchaptercode',lambda d:d.__setitem__('chaptercode',a['chaptercode'])); mk('v4_tpl9524',lambda d:None,'course_page_template_v9_52_4.html')
mk('v1b_noplain',io); mk('v5_alldata73_tpl9529',allold); mk('v6_alldata73_tpl9524',allold,'course_page_template_v9_52_4.html')
