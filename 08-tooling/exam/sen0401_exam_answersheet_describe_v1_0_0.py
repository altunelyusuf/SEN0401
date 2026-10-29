"""Describes a built answer sheet as RDF (class as:Sheet) from its layout and from measurements of its PDF, version 1.0.0.
Measured, not declared: smallest font size (pdfplumber), raster images (pdfimages), colour (pixels of the rendered page), page count (pdfinfo)."""
import os, subprocess, sys, tempfile, shutil, glob
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rdflib import Graph, Namespace, Literal, RDF, XSD
import sen0401_exam_answersheet_v1_0_0 as A
AS = Namespace('http://example.org/sen0401/answersheet#'); FX = Namespace('http://example.org/sen0401/answersheet/instance#')
I = lambda v: Literal(v, datatype=XSD.integer); B = lambda v: Literal(v, datatype=XSD.boolean)

def measure_pdf(pdf):
    import pdfplumber, numpy as np
    from PIL import Image
    with pdfplumber.open(pdf) as d: sizes = [c['size'] for pg in d.pages for c in pg.chars]
    imgs = subprocess.run(['pdfimages', '-list', pdf], capture_output=True, text=True).stdout.strip().splitlines()
    n_img = max(0, len(imgs) - 2)
    pages = int([l for l in subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages:')][0].split()[1])
    w = tempfile.mkdtemp(prefix='sen0401_as_col_')
    try:
        subprocess.run(['pdftoppm', '-r', '72', '-png', pdf, w + '/c'], check=True)
        coloured = 0; dark_share = []
        for f in sorted(glob.glob(w + '/c*.png')):
            a = np.array(Image.open(f).convert('RGB')).astype(int)
            coloured += int(((a[..., 0] != a[..., 1]) | (a[..., 1] != a[..., 2])).sum())
            dark_share.append(float((a[..., 0] < 128).mean()))
    finally: shutil.rmtree(w, ignore_errors=True)
    return {'min_font_pt': min(sizes), 'chars': len(sizes), 'raster_images': n_img, 'pages': pages, 'coloured_pixels': coloured, 'dark_pixel_share': max(dark_share)}

def describe(layout, pdf, version_seq=1, previous=0, bank_entries=6):
    m = measure_pdf(pdf); g = Graph(); g.bind('as', AS); g.bind('fx', FX)
    spec = layout['spec']; sh = FX['sheet']
    g.add((sh, RDF.type, AS.Sheet)); g.add((sh, AS.paperKind, Literal(spec['paper_kind']))); g.add((sh, AS.formCode, Literal(spec['form_code'])))
    g.add((sh, AS.formCodeValid, B(A.damm_valid(spec['form_code']))))
    g.add((sh, AS.fontPt, I(int(m['min_font_pt'] + 1e-6)))); g.add((sh, AS.fillColourUsed, B(m['coloured_pixels'] > 0)))
    g.add((sh, AS.rasterImages, I(m['raster_images']))); g.add((sh, AS.containsPersonalData, B(False))); g.add((sh, AS.pageCount, I(m['pages'])))
    g.add((sh, AS.thresholdFilled, Literal(str(A.T_FILLED), datatype=XSD.decimal))); g.add((sh, AS.thresholdFaint, Literal(str(A.T_FAINT), datatype=XSD.decimal)))
    g.add((sh, AS.fiducialCount, I(len(layout['fiducials']))))
    for kind, text in (('StrikeVoids', 'an X through a bubble voids it'), ('DoubleIsNoAnswer', 'two filled bubbles in a row count as no answer'), ('DeclareBlank', 'every number left blank is declared in the block closure')):
        r = FX['rule_' + kind]; g.add((sh, AS.hasRule, r)); g.add((r, RDF.type, AS.Rule)); g.add((r, AS.ruleKind, Literal(kind))); g.add((r, AS.text, Literal(text)))
    for b in layout['blocks']:
        bn = FX['block%d' % b['id']]; g.add((sh, AS.hasBlock, bn)); g.add((bn, RDF.type, AS.Block)); g.add((bn, AS.kind, Literal(b['kind'])))
        g.add((bn, AS.unitCount, I(len(b['units'])))); g.add((bn, AS.closureBubbles, I(len(b['closure']))))
        cl = {q['no'] for q in b['closure']}
        for u in b['units']:
            un = FX['unit_' + u['no']]; g.add((sh, AS.hasUnit, un)); g.add((un, RDF.type, AS.Unit)); g.add((un, AS.label, Literal(u['no']))); g.add((un, AS.kind, Literal(u['kind'])))
            g.add((un, AS.placeCount, I(1))); g.add((un, AS.numberAtBothEnds, B(True))); g.add((un, AS.inBlock, bn)); g.add((un, AS.hasClosureBubble, B(u['no'] in cl)))
            if u['kind'] != 'human': g.add((un, AS.choicesPerRow, I(len(u['rows'][0]['opts']))))
            if u['kind'] == 'bank': g.add((un, AS.checkScheme, Literal('Damm')))
    w = A.serial_width(bank_entries)
    for s in range(1, bank_entries + 1):
        c = A.make_code(s, w); cn = FX['code%d' % s]; g.add((cn, RDF.type, AS.BankCode)); g.add((cn, AS.digits, Literal(c))); g.add((cn, AS.checkValid, B(A.damm_valid(c))))
    return g, m, {s: A.make_code(s, w) for s in range(1, bank_entries + 1)}

if __name__ == '__main__':
    out = sys.argv[1]; kind = sys.argv[2] if len(sys.argv) > 2 else 'Midterm'
    spec = A.default_spec(kind); lay = A.build_layout(spec)
    pdf, js = A.write_pair(lay, out, 'sen0401_exam_answersheet_%s_v1_0_0' % kind.lower())
    g, m, codes = describe(lay, pdf)
    g.serialize(os.path.join(out, 'sen0401_exam_answersheet_%s_description_v1_0_0.ttl' % kind.lower()), format='turtle'); print(m, codes)
