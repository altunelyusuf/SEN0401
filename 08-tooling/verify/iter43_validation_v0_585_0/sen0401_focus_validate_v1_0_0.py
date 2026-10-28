import importlib.util, sys, subprocess, rdflib, os
from rdflib import Graph
p="/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_validate_v1_17_0.py"
sp=importlib.util.spec_from_file_location("bv",p); bv=importlib.util.module_from_spec(sp); sp.loader.exec_module(bv)
old,new=sys.argv[1],sys.argv[2]
a=Graph(); a.parse(old,format="turtle"); b=Graph(); b.parse(new,format="turtle")
olds=set(a.subjects()); changed={s for s in set(b.subjects()) if s not in olds and not isinstance(s,rdflib.BNode)}
print("changed subjects:",len(changed))
ov=bv.promoted_overlay([new]); shapes=ov if ov else bv.SHAPES
sh=bv.serialize(bv.load([shapes]),".shapes.ttl"); da=bv.serialize(bv.load([bv.TBOX,bv.reference_abox([new]),new]),".data.ttl")
open("/tmp/claude-0/q7tmp/focus_list.txt","w").write(",".join(sorted(str(s) for s in changed)))
proc=subprocess.run([sys.executable,"-m","pyshacl","-s",sh,"-a","-f","turtle","--focus",",".join(sorted(str(s) for s in changed)),da],capture_output=True,text=True)
open("/tmp/claude-0/q7tmp/focus_report.ttl","w").write(proc.stdout); print("pyshacl rc",proc.returncode, proc.stderr[-300:])
r=Graph(); r.parse(data=proc.stdout,format="turtle")
SH=rdflib.Namespace("http://www.w3.org/ns/shacl#")
from collections import Counter
c=Counter(); 
for x in r.subjects(rdflib.RDF.type,SH.ValidationResult):
    c[(str(r.value(x,SH.resultSeverity)).split("#")[-1], str(r.value(x,SH.sourceShape)).split("#")[-1])]+=1
print(c.most_common(20)); print("conforms:", r.value(None,SH.conforms))
