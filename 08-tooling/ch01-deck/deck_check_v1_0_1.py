"""Chapter check for a deck: every '>>>' example on its slides is re-run under the Python given, in one
shell session per slide, and its output compared with what the slide shows. A mismatch refuses the deck."""
__version__ = "1.0.1"
import sys, re, zipfile
from xml.dom import minidom
def slides(path):
    z=zipfile.ZipFile(path); out=[]
    for n in sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',n)], key=lambda n:int(re.findall(r'\d+',n)[0])):
        d=minidom.parseString(z.read(n)); paras=[]
        for p in d.getElementsByTagName('a:p'):
            paras.append("".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName('a:t')))
        out.append((n,paras))
    return out
def check(path):
    bad=[]; n_ex=0
    for name,paras in slides(path):
        ns={}; i=0
        while i < len(paras):
            p=paras[i]
            if p.startswith('>>> '):
                src=p[4:]; nxt=paras[i+1] if i+1<len(paras) else ""
                shown=None if nxt.startswith('>>> ') else nxt
                try:
                    try: got=repr(eval(src,ns))
                    except SyntaxError: exec(src,ns); got=None
                except Exception as e: got="%s: %s" % (type(e).__name__, e)
                if got is not None or shown is not None:
                    n_ex+=1
                    if shown is not None and got != shown: bad.append((name, src, shown, got))
                i+= 1 if shown is None else 2
            else: i+=1
    return n_ex, bad
n,bad=check(sys.argv[1])
print("%d examples re-run; %d mismatch(es)" % (n, len(bad)))
for b in bad: print("  REFUSED", b)
sys.exit(1 if bad else 0)
