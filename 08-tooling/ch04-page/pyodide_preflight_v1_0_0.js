const {loadPyodide}=require('pyodide');const fs=require('fs');
(async()=>{const py=await loadPyodide();
const R='/home/claude/sen0401/';const man=JSON.parse(fs.readFileSync(R+'03-materials/ch04/page/chapter_code_ch04_v1_0_0.json'));
const pw=JSON.parse(fs.readFileSync(R+'08-tooling/ch04-page/pywheels_v1_0_0.json'));
py.FS.writeFile('/home/pyodide/sen0401_ch04_lib_v1_0_0.py',fs.readFileSync(R+'08-tooling/sen0401_ch04_lib_v1_0_0.py'));
py.runPython("import sys;sys.path.insert(0,'/home/pyodide')");
console.log(py.runPython("import sys;sys.version"));
let fail=0;
for(const e of man.examples){
 py.globals.set('boot',pw.boot_python);py.globals.set('code',e.code);py.globals.set('shows',JSON.stringify(e.show));
 const r=py.runPython(`
import json,traceback,builtins
ns={'__name__':'__main__'}
try:
    exec(boot,ns); exec(code,ns)
    out=[]
    for s in json.loads(shows):
        v=repr(eval(s['expression'],ns)); out.append((v==s['expected'],s['expression'],v,s['expected']))
    res=json.dumps(out)
except BaseException:
    res=json.dumps('ERR '+traceback.format_exc())
res`);
 const j=JSON.parse(r);
 if(typeof j==='string'){fail++;console.log(e.order,e.name,'FAIL',j.slice(-400));continue}
 const bad=j.filter(x=>!x[0]);if(bad.length){fail++;console.log(e.order,e.name,'MISMATCH',JSON.stringify(bad))}else console.log(e.order,e.name,'ok',j.length)
}
console.log('failures',fail);})();
