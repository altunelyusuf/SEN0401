#!/usr/bin/env python3
"""CME material check v1.2.0 (adds the check no-analogy: no everyday analogy in the deck or the page, owner ruling of 2026-11-24; the pattern is read from the deck-standard shapes file 06-quality/sen0401_deck_standard_shapes_v1_1_0.ttl, shape D4, so the ruling has one home). CME material check v1.1.0 (page lambda count looks for real lambda expressions, not keyword names): tests the built automatic conditions of the material rulings
(cme_standards_adoption_v1_4_0.ttl, module material-rulings) on one deck and, optionally, its page.
Checks: title-words, visual-present, notes-words, notes-labels, code-in-page, no-prompts, code-parses, no-lambda.
NOT built (never read as a pass): page-runs-slide-code, taught-only. Reviewed conditions are not tested here.
Usage: python3 cme_material_check_v1_3_0.py DECK.pptx [PAGE.html] [--taught lambda] [--json OUT.json]"""
import sys, re, ast, json, html
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE as T

args = [a for a in sys.argv[1:]]
taught = set(); out = None
if '--taught' in args: i = args.index('--taught'); taught = set(args[i+1].split(',')); del args[i:i+2]
if '--json' in args: i = args.index('--json'); out = args[i+1]; del args[i:i+2]
deck = args[0]; page = args[1] if len(args) > 1 else None
LABEL = re.compile(r'^\s*(SAY|ASK|STORY[^:]{0,30}|NOTE|CUE|TIP)\s*:', re.M)
PROMPT = re.compile(r'^\s*(>>>|\.\.\.|>>)', re.M)
SPECIAL = re.compile(r'^(part\s+\d+|agenda|summary|resources|questions|practice|title|references|further)', re.I)

def frames(slide):
    for sh in slide.shapes:
        if not sh.has_text_frame: continue
        fonts = {r.font.name for p in sh.text_frame.paragraphs for r in p.runs}
        if 'Courier New' in fonts: yield sh
def title_of(slide):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.name.lower() == 'title': return sh.text_frame.text.strip()
    for sh in slide.shapes:
        tx = sh.text_frame.text.strip() if sh.has_text_frame else ''
        if len(tx) > 2 and not re.match(r'^\d+\s*/\s*\d+$', tx) and not any(r.font.name == 'Courier New' for p in sh.text_frame.paragraphs for r in p.runs):
            return tx.split('\n')[0]
    return ''
def has_visual(slide):
    for sh in slide.shapes:
        if sh.shape_type in (T.PICTURE, T.CHART, T.TABLE, T.GROUP): return True
        if sh.has_text_frame and sh.name != 'chip' and any(r.font.name == 'Courier New' for p in sh.text_frame.paragraphs for r in p.runs): return True
    return sum(1 for sh in slide.shapes if sh.shape_type == T.LINE or 'Connector' in sh.name) >= 2

prs = Presentation(deck); n = len(prs.slides)
R = {k: {'fail': [], 'checked': 0} for k in ['title-words','visual-present','notes-words','notes-labels','no-prompts','code-parses','no-lambda','code-in-page','no-analogy']}
blocks = []
for i, s in enumerate(prs.slides, 1):
    t = title_of(s); special = (i == 1 or i == n or bool(SPECIAL.match(t)))
    notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ''
    nw = len(notes.split())
    if not special:
        R['title-words']['checked'] += 1
        if len(t.split()) < 4: R['title-words']['fail'].append((i, t[:50]))
        R['visual-present']['checked'] += 1
        if not has_visual(s): R['visual-present']['fail'].append((i, t[:50]))
    R['notes-words']['checked'] += 1
    lo, hi = (30, 140) if special else (60, 140)
    if not (lo <= nw <= hi): R['notes-words']['fail'].append((i, nw))
    R['notes-labels']['checked'] += 1
    if LABEL.search(notes): R['notes-labels']['fail'].append((i, 'label prefix'))
    for sh in s.shapes:
        if sh.has_text_frame and sh.name == 'chip' and sh.text_frame.text.strip() in ('>>>', '>>'):
            R['no-prompts']['checked'] += 1; R['no-prompts']['fail'].append((i, 'decorative prompt chip'))
    for sh in frames(s):
        if sh.name == 'chip': continue
        code = sh.text_frame.text
        blocks.append((i, code))
        R['no-prompts']['checked'] += 1
        if PROMPT.search(code): R['no-prompts']['fail'].append((i, 'prompt marker in code frame'))
        R['code-parses']['checked'] += 1
        try: ast.parse(code)
        except SyntaxError: R['code-parses']['fail'].append((i, 'does not parse as shown'))
        R['no-lambda']['checked'] += 1
        if 'lambda' not in taught and re.search(r'\blambda\b[^:\n]{0,40}:', code): R['no-lambda']['fail'].append((i, 'lambda in slide code'))
pagetxt = None
if page:
    raw = open(page, encoding='utf-8').read()
    pagetxt = html.unescape(raw).replace('\\n', '\n').replace('\\"', '"')
    def norm(x): return re.sub(r'\s+', ' ', x.replace('\\', '')).strip()
    P = norm(pagetxt)
    for i, code in blocks:
        lines = [PROMPT.sub('', l, count=1).rstrip() if PROMPT.match(l) else l.rstrip() for l in code.split('\n')]
        R['code-in-page']['checked'] += 1
        probe = norm(lines[0]) if lines else ''
        if not probe or probe not in P: R['code-in-page']['fail'].append((i, probe[:50]))
    pl = len(re.findall(r"\blambda\s[^:\n\"']{0,40}:", pagetxt)) if 'lambda' not in taught else 0
    # v1.3.0: book listings quoted inside an embedded ontology literal (mbb:text "...") are the book's own text, not page code
    code_only = re.sub(r'mbb:text "(?:[^"\\]|\\.|"(?!\s*;))*"', 'mbb:text ""', pagetxt)
    pp = len(re.findall(r'^\s*(>>>|\.\.\.)', code_only, re.M))
    R['no-lambda']['page_occurrences'] = pl; R['no-prompts']['page_prompt_lines'] = pp
else: R['code-in-page']['note'] = 'no page given'

# no-analogy: the pattern of shape D4 in the shapes file is the single source of the ruling
import os, rdflib
_here = os.path.dirname(os.path.abspath(__file__))
_g = rdflib.Graph(); _g.parse(os.path.join(os.path.dirname(_here), '06-quality', 'sen0401_deck_standard_shapes_v1_1_0.ttl'), format='turtle')
_SH = rdflib.Namespace('http://www.w3.org/ns/shacl#')
_pat = str(next(_g.objects(None, _SH.pattern)))
_rx = re.compile(_pat, re.I)
def _walk(shs):
    for x in shs:
        if x.shape_type == T.GROUP: yield from _walk(x.shapes)
        else: yield x
for i, s in enumerate(prs.slides, 1):
    texts = [x.text_frame.text for x in _walk(s.shapes) if x.has_text_frame] + [s.notes_slide.notes_text_frame.text if s.has_notes_slide else '']
    R['no-analogy']['checked'] += len(texts)
    for tx in texts:
        m = _rx.search(tx)
        if m: R['no-analogy']['fail'].append((i, tx[max(0, m.start()-20):m.end()+30]))
if page:
    _pt = re.sub(r'"hex": "[0-9a-f]{200,}"', '"hex": "X"', open(page, encoding='utf-8').read())
    R['no-analogy']['checked'] += 1
    for m in _rx.finditer(_pt): R['no-analogy']['fail'].append(('page', _pt[max(0, m.start()-20):m.end()+30]))
res = {'deck': deck, 'page': page, 'slides': n, 'code_frames': len(blocks), 'checks': {}}
for k, v in R.items():
    res['checks'][k] = {'checked': v['checked'], 'failed': len(v['fail']), 'first_failures': v['fail'][:5], **{x: v[x] for x in v if x not in ('fail', 'checked')}}
print(f"{deck.split('/')[-1]}  slides {n}  code frames {len(blocks)}")
for k, v in res['checks'].items():
    extra = ' '.join(f'{x}={y}' for x, y in v.items() if x not in ('checked','failed','first_failures'))
    print(f"  {k:15} {'PASS' if v['failed']==0 and not any(isinstance(y,int) and y>0 for x,y in v.items() if x in ('page_occurrences','page_prompt_lines')) else 'FAIL'}  failed {v['failed']}/{v['checked']} {extra}")
if out: json.dump(res, open(out, 'w'), indent=1)
