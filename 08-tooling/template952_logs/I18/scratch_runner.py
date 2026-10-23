import os,re,subprocess,sys,tempfile,shutil
sys.path.insert(0,'/home/claude/sen0401/08-tooling')
REPO='/home/claude/sen0401'; TOOL=REPO+'/08-tooling'; MIR='/tmp/claude-0/-home-claude/7b499b1c-1b38-5415-81de-45b731a5a6db/scratchpad/mirror'
n,pv,page,test=sys.argv[1:5]
import json
jwk=json.load(open('/home/claude/instructor_keys_test/test_key.json'))["private_jwk"] if os.path.exists('/home/claude/instructor_keys_test/test_key.json') else None
if jwk is None:
    subprocess.run([sys.executable,TOOL+'/sen0401_lineage_page_key_substitute_v1_0_0.py','05','9_80_0','/tmp/ks_tmp'],check=True)
    jwk=json.load(open('/home/claude/instructor_keys_test/test_key.json'))["private_jwk"]
d=tempfile.mkdtemp(prefix='sen0401_page_test_')
s=open(page,encoding='utf-8').read()
a,b=("0Sa8MtDE94xNCAAucUwWWoWgdLIgKRY42weFJWUDVrU","PQfE3vB8fPYCKQ4RPxZZovRuFZ4yQz9u4pmiObDqjus")
assert a in s and b in s
s=s.replace(a,jwk['x']).replace(b,jwk['y'])
named=os.path.join(d,'sen0401_ch%s_page_v%s.html'%(n,pv)); open(named,'w',encoding='utf-8').write(s)
shutil.copy('/home/claude/instructor_keys_test/test_key.json',d+'/test_key.json')
pk=lambda f:[int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.html$",f).groups()]
import glob
earlier=[f for f in glob.glob(REPO+'/03-materials/ch%s/page/sen0401_ch%s_page_v*.html'%(n,n)) if pk(f)<pk(named)]
if earlier:
    pred=sorted(earlier,key=pk)[-1]; shutil.copy(pred,d); print('predecessor',os.path.basename(pred))
env=dict(os.environ,PAGE=named,RESULTS=d+'/results.json',PAGE_VER=pv,KEY=d+'/test_key.json',PYTHONDONTWRITEBYTECODE='1')
print('page test:',os.path.basename(test),'on scratch page',pv,'chapter',n,flush=True)
r=subprocess.run([sys.executable,test.replace(TOOL,MIR+'/08-tooling'),n],capture_output=True,text=True,env=env,cwd=MIR)
out=r.stdout+r.stderr
open(os.environ['FULL_LOG'],'w').write(out)
fails=[l for l in out.splitlines() if l.strip().startswith('[FAIL]')]
npass=sum(1 for l in out.splitlines() if l.strip().startswith('[PASS]'))
m=re.search(r"widgets: (\d+) tested, (\d+) passed",out)
print('\n'.join(out.splitlines()[-16:]))
for l in fails: print(l[:300])
print('chapter %s: exit %d, widgets %s, features passed %d, failed %d'%(n,r.returncode,m.groups() if m else None,npass,len(fails)))
print('RESULT:','PASS' if r.returncode==0 and m and m.group(1)==m.group(2) and not fails else 'FAIL')
