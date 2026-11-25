#!/usr/bin/env python3
"""Chapter 4 deck v3_8_0 builder (reads v3_7_0, which stays as released). Brings the deck to the standard of the Ch7-14 decks:
notes 60-140 reader-facing words, no everyday analogy, titles of at least four words, a visual on every slide, parseable code frames
(results and tiles are not code, so they leave the code font), 5N1K alt text on the three story slides.
Usage: python3 ch04_deck_build_v3_8_0.py SRC.pptx OUT.pptx"""
import sys, re, copy
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.oxml.ns import qn
from lxml import etree
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ch04_notes_v3_8_0_a import NOTES_A
from ch04_notes_v3_8_0_b import NOTES_B
NOTES = {**NOTES_A, **NOTES_B}
src, out = sys.argv[1], sys.argv[2]
prs = Presentation(src)
S = lambda i: prs.slides[i - 1]
log = []

def walk(shs):
    for x in shs:
        yield x
        if x.shape_type == 6: yield from walk(x.shapes)

def set_text(sh, text):
    """replace the text of the first run of a frame, keep its formatting, drop other runs/paragraphs"""
    tf = sh.text_frame; p0 = tf.paragraphs[0]
    for p in tf.paragraphs[1:]: p._p.getparent().remove(p._p)
    runs = p0.runs
    runs[0].text = text
    for r in runs[1:]: r._r.getparent().remove(r._r)

# 1. titles
TITLES = {2: ("TextBox 2", "Today's route through the chapter"),
          5: ("TextBox 1", "Part 2: Public Key Cryptography"), 24: (None, "Part 3: Legacy Addresses"),
          41: (None, "Part 4: Script Hashes and Bech32"), 58: (None, "Part 5: Private Key Formats"),
          62: (None, "Part 6: Advanced Keys and Addresses"), 15: ("TextBox 2", "A finite field: arithmetic that wraps at p")}
for i, (nm, t) in TITLES.items():
    s = S(i); sh = next(x for x in s.shapes if x.has_text_frame and (x.name == nm if nm else x.name == 'TextBox 1'))
    set_text(sh, t); log.append(f'title {i}: {t}')

# 2a. the takeaway line of the concept tables says what the slide holds
for i in (6, 7, 25, 26, 27, 42, 43, 59, 63):
    sh = next(x for x in S(i).shapes if x.name == 'TextBox 5'); set_text(sh, 'Each row names one concept and says what it means')
# 2. analogy removal
THINK = re.compile(r'(^|\s)Think of\b.*$', re.S)
for i, s in enumerate(prs.slides, 1):
    for sh in list(walk(s.shapes)):
        if sh.shape_type == 19:
            t = sh.table
            if t.cell(0, len(t.columns) - 1).text.strip() == 'Think of':
                grid = t._tbl.tblGrid; cols = grid.findall(qn('a:gridCol'))
                w = int(cols[1].get('w')) + int(cols[2].get('w'))
                cols[1].set('w', str(w)); grid.remove(cols[2])
                for tr in t._tbl.findall(qn('a:tr')):
                    tcs = tr.findall(qn('a:tc')); tr.remove(tcs[-1])
                log.append(f'slide {i}: dropped the Think-of column of {sh.name}')
            continue
        if not sh.has_text_frame: continue
        tf = sh.text_frame; changed = False
        for p in list(tf.paragraphs):
            txt = p.text
            core = txt.lstrip('▪  ')
            if core.startswith('Think of') or core.startswith('Think of each row'):
                p._p.getparent().remove(p._p); changed = True; continue
            m = THINK.search(txt)
            if m:
                keep = txt[:m.start()].rstrip()
                if p.runs:
                    p.runs[0].text = keep
                    for r in p.runs[1:]: r._r.getparent().remove(r._r)
                changed = True
        if changed:
            if not tf.text.strip() or tf.text.strip() in ('▪', ''):
                sh._element.getparent().remove(sh._element); log.append(f'slide {i}: removed empty box {sh.name}')
            else: log.append(f'slide {i}: trimmed analogy in {sh.name}')

# fixed wording where the sentence itself changes
def sub_text(i, old, new, exact=False):
    for sh in walk(S(i).shapes):
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if old in r.text: r.text = r.text.replace(old, new); log.append(f'slide {i}: "{old[:30]}" -> "{new[:30]}"'); return
    raise SystemExit(f'not found slide {i}: {old}')
for i in (6, 7, 25, 26, 27, 42, 43, 59, 63):
    sub_text(i, 'with everyday pictures', 'in one line')
    sub_text(i, 'Each row: the idea in one line, then something you already know', 'Each row: the concept and what it means')
sub_text(15, ', like the hours on a clock face', '')
sub_text(44, 'Three of the eight combinations above pass.', 'Four of the eight combinations above pass.')

# 3. code font: results, tiles and samples that are not code leave the code font
for i, s in enumerate(prs.slides, 1):
    for sh in walk(s.shapes):
        if not sh.has_text_frame: continue
        nm = sh.name
        if nm.startswith(('result', 'tile ')) or nm in ('bip38 card text', 'doc text', 'descriptor card text'):
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.name == 'Courier New': r.font.name = 'Calibri'; 
            log.append(f'slide {i}: {nm} set to Calibri') if nm.startswith('result') is False else None


# 3b. slide 10: the def card becomes the 22nd code box (code 1), with the run line, so that the page carries the same code
s10 = S(10); card = next(x for x in s10.shapes if x.name == 'def card text'); bg = next(x for x in s10.shapes if x.name == 'def card')
tf = card.text_frame; p0 = tf.paragraphs[0]._p; p1 = tf.paragraphs[1]._p
p2 = copy.deepcopy(p1); p1.addnext(p2)
rr = tf.paragraphs[2].runs; rr[0].text = '[ok(x) for x in (0, 1, K.BOOK_K, K.N - 1, K.N)]'
for r in rr[1:]: r._r.getparent().remove(r._r)
for pa in tf.paragraphs:
    for r in pa.runs: r.font.size = Pt(10)
card.name = 'code 1'; card.height = card.height + Emu(int(0.2 * 914400)); bg.height = bg.height + Emu(int(0.2 * 914400))
for x in s10.shapes:
    if x.name == 'def read': x.top = x.top + Emu(int(0.2 * 914400))
# 3c. the number of code examples and the library version named on the code slides
sub_text(2, 'twenty-one examples', 'twenty-two examples')
sub_text(2, '21', '22')
for i, s in enumerate(prs.slides, 1):
    for sh in walk(s.shapes):
        if sh.has_text_frame and 'sen0401_ch04_lib_v1_0_0' in sh.text_frame.text:
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs: r.text = r.text.replace('sen0401_ch04_lib_v1_0_0', 'sen0401_ch04_lib_v1_1_0')

# 4. visuals
def connect(slide, a, b, kind):
    if kind == 'h': x1, y1, x2, y2 = a.left + a.width, a.top + a.height // 2, b.left, b.top + b.height // 2
    else: x1, y1, x2, y2 = a.left + a.width // 2, a.top + a.height, b.left + b.width // 2, b.top
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    c.line.width = Pt(1.5)
    ln = c.line._get_or_add_ln(); tail = etree.SubElement(ln, qn('a:tailEnd')); tail.set('type', 'triangle')
    try: c.line.color.rgb = a.fill.fore_color.rgb if a.fill.type == 1 else c.line.color.rgb
    except Exception: pass
    return c
s2 = S(2); boxes = {x.name: x for x in s2.shapes}
for a, b, k in (('Rounded Rectangle 7', 'Rounded Rectangle 8', 'h'), ('Rounded Rectangle 8', 'Rounded Rectangle 9', 'h'),
                ('Rounded Rectangle 10', 'Rounded Rectangle 11', 'h'), ('Rounded Rectangle 11', 'Rounded Rectangle 12', 'h'),
                ('Rounded Rectangle 7', 'Rounded Rectangle 10', 'v'), ('Rounded Rectangle 10', 'Rounded Rectangle 13', 'v')):
    connect(s2, boxes[a], boxes[b], k)
s3 = S(3); ov = [x for x in s3.shapes if x.name.startswith('Oval')]
for a, b in zip(ov, ov[1:]): connect(s3, a, b, 'v')
def group(i, pred, name):
    s = S(i); members = [x for x in s.shapes if pred(x)]
    g = s.shapes.add_group_shape(members); g.name = name; log.append(f'slide {i}: grouped {len(members)} shapes as {name}')
group(32, lambda x: x.name in ('stack head', 'opcode', 'stack 0 chip', 'stack 1 chip', 'stack 2 chip', 'stack 3 chip', 'stack 4 chip', 'stack 5 chip'), 'Diagram: P2PKH on a stack')
group(44, lambda x: x.name in ('script head', 'msig part', 'msig legend', 'msig legend more', 'grid head', 'signers'), 'Diagram: 2-of-3 script and signer sets')
group(48, lambda x: x.name in ('before head', 'before part', 'before id', 'after head', 'after txid part', 'witness part', 'after id'), 'Diagram: txid before and after segwit')
group(76, lambda x: x.name in ('uri head', 'uri part', 'uri tags', 'did head', 'did part', 'did tags', 'doc card', 'doc text'), 'Diagram: URI and DID anatomy')
group(53, lambda x: x.name.startswith('type '), 'Diagram: three segwit output types')

# 5. story alt text (5N1K stays invisible)
TAGS = {8: ['when where', 'who what where', 'when how', 'why how', 'what why'],
        35: ['when where', 'who what when', 'what why how', 'how what', 'when where'],
        72: ['when where', 'who what how', 'what why', 'who when where how', 'why']}
for i, tags in TAGS.items():
    boxes = [x for x in S(i).shapes if x.name.lower().startswith('story')]
    assert len(boxes) == len(tags), (i, len(boxes))
    for b, t in zip(boxes, tags): b._element.xpath('.//p:cNvPr')[0].set('descr', '5N1K ' + t)

# 6. notes
for i, s in enumerate(prs.slides, 1):
    s.notes_slide.notes_text_frame.text = NOTES[i]
prs.save(out)
print('\n'.join(log)); print('saved', out)
