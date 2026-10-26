const {loadPyodide}=require('pyodide');const fs=require('fs');
(async()=>{const py=await loadPyodide();
const R='/home/claude/sen0401/';const man=JSON.parse(fs.readFileSync(R+'03-materials/ch12/page/chapter_code_ch12_v1_2_0.json'));
const pw=JSON.parse(fs.readFileSync(R+'08-tooling/ch12-page/pywheels_v1_1_0.json'));
// the page unpacks the wheel into site-packages (as its worker does); the chapter library is only what the wheel holds
for(const w of pw.wheels){const b=fs.readFileSync(R+'03-materials/ch12/assets/'+w.file);py.unpackArchive(new Uint8Array(b),'zip',{extractDir:'/lib/python3.13/site-packages'});}
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
