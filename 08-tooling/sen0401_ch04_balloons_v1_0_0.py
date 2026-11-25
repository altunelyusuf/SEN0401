#!/usr/bin/env python3
"""sen0401_ch04_balloons v1.0.0: the code slides of Chapter 4 in the layout of chapter 8 (owner request 2026-11-25/26): a numbered step badge on each code box, a speech balloon with one story sentence (First / Next / Then) beside it, the output line under the code, the result balloon under that, the result table or chart lower right. No new slides; code, tables, charts and notes are unchanged; the story sentences are the old explanation sentences of the slides, said as steps.
Reads 03-materials/ch04/SEN0401_Ch04_KeysAndAddresses_3e_v3_8_0.pptx, writes ..._v3_9_0.pptx, the manifest 1.2.1 -> chapter_code_ch04_v1_2_1.json is made by the follow script. Refuses to overwrite. Usage: python3 sen0401_ch04_balloons_v1_0_0.py [preview.pptx]"""
__version__ = "1.0.0"
import os, re, sys, math
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
E = 914400; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "03-materials/ch04/SEN0401_Ch04_KeysAndAddresses_3e_v3_8_0.pptx"); DST = os.path.join(REPO, "03-materials/ch04/SEN0401_Ch04_KeysAndAddresses_3e_v3_9_0.pptx")
INK = RGBColor(0x2B, 0x26, 0x22); ORANGE = RGBColor(0xD9, 0x7A, 0x14); BAL = RGBColor(0xFF, 0xFB, 0xEF); BEDGE = RGBColor(0xE8, 0xB8, 0x78); VOICE = "Trebuchet MS"
STORY = {
 11: ["**First**, the private key of the book's example is loaded: one very large whole number.", "**Next**, a lambda checks that a key lies strictly between 0 and n, and five numbers are tested."],
 12: ["**First**, entropy is the length times the base-2 logarithm of the size of the alphabet.", "**Next**, four secrets are measured: a PIN, a lowercase word, a long password and 256 fair coin flips."],
 14: ["**First**, the generator point G is the fixed starting point that every key multiplies.", "**Next**, both sides of y squared equals x cubed plus 7 are counted modulo the prime p, and they agree."],
 19: ["**First**, G is multiplied by one, two, three and four; every result is another point.", "**Next**, adding G to itself gives 2G, the same point that the multiplication found."],
 20: ["**First**, the multiples of one point are walked on a toy curve over only 17 numbers.", "**Next**, the ninth multiple is None, the point at infinity, so the walk closes into a cycle."],
 21: ["**First**, key sizes in bits are listed, from a toy key to the size Bitcoin uses.", "**Next**, half of the keys must be tried on average; the list gives that as a power of ten."],
 30: ["**First**, G is multiplied by the book's private key, and the public key is a point (x, y).", "**Next**, compressed keeps x and a parity byte; uncompressed writes x and y after 04."],
 31: ["**First**, the compressed public key of the book's example is taken.", "**Next**, P2PK holds the key itself; P2PKH holds only a 20-byte hash of it, a commitment."],
 33: ["**First**, SHA256 turns the 33-byte key into a 32-byte fingerprint.", "**Next**, RIPEMD-160 shortens it to 20 bytes; the pair of hashes is what HASH160 means."],
 36: ["**First**, the 20-byte key hash of the book's example is computed.", "**Next**, the version byte 00 goes in front; the checksum is four bytes of a double SHA256.", "**Then** twenty-five bytes in base58 become a 34-character address that starts with 1."],
 39: ["**First**, the example address is taken, and one character at a time will be changed.", "**Next**, every one-character substitution is tried; the pair counts the typos and the accepted ones."],
 45: ["**First**, three public keys are taken for a two-of-three multisignature wallet.", "**Next**, the redeem script lists the keys and asks for any two signatures.", "**Then** the address is HASH160 of that script with version 05, so it starts with 3."],
 46: ["**First**, a hash of n bits falls to a collision after about 2 to the n over 2 tries.", "**Next**, a preimage needs 2 to the n tries; the list gives the exponents for two hash sizes."],
 50: ["**First**, a version 0 SegWit address is built for the book's key hash.", "**Next**, it is split at the last 1 into network name, version letter, program letters and checksum."],
 52: ["**First**, three programs from the book are decoded: a key hash, a script hash and a Taproot key.", "**Next**, decoding each address returns the witness version and the program length."],
 54: ["**First**, a string passes when its checksum equals the constant of the format.", "**Next**, the book's strings insert q before the last p, and the old checksum cannot tell."],
 60: ["**First**, the same key is written twice: as WIF and as WIF-compressed.", "**Next**, the first form starts with 5 and has 51 characters; the second starts with K or L and has 52."],
 61: ["**First**, the 65-byte key and then the 33-byte key are hashed: two different addresses.", "**Next**, the compressed flag in WIF tells a wallet which of the two addresses it must watch."],
 64: ["**First**, keys 1, 2, 3 are tried until the address has A as its first letter after the 1.", "**Next**, one chosen letter took this many tries; each further letter costs 58 times more."],
 65: ["**First**, a paper wallet prints two strings: the secret WIF key and the public address.", "**Next**, scanning the paper decodes the key from its WIF text.", "**Then** the restored key must reproduce the printed address; test it before you fund it."],
 73: ["**First**, the address spells a message after the leading 1, and six more letters close it.", "**Next**, the checksum is correct, so a wallet accepts the address without any warning."]}
WARN = []
def plain(t): return t.replace("**", "")
def need_h(t, size, w):
    cw = size * 0.54 * 1.03 / 72.0; avail = w - 0.22; lines = 1; cur = 0.0
    for word in plain(t).split():
        L = (len(word) + 1) * cw
        if cur + L > avail + cw and cur > 0: lines += 1; cur = L
        else: cur += L
    return lines * size * 1.2 / 72.0 + 0.08
def fit(t, w, h, sizes):
    for sz in sizes:
        if need_h(t, sz, w) <= h: return sz
    WARN.append("no fit (%.2f x %.2f): %s" % (w, h, plain(t)[:40])); return sizes[-1]
def box(s, shape, x, y, w, h, fill, line=None):
    b = s.shapes.add_shape(shape, Emu(int(x * E)), Emu(int(y * E)), Emu(int(w * E)), Emu(int(h * E)))
    b.fill.solid(); b.fill.fore_color.rgb = fill
    if line is None: b.line.fill.background()
    else: b.line.color.rgb = line; b.line.width = Pt(0.9)
    b.shadow.inherit = False; return b
def text(b, t, size, font=VOICE, bold=False, anchor=MSO_ANCHOR.MIDDLE, m=0.1, color=INK, align=PP_ALIGN.LEFT):
    tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Emu(int(m * E)); tf.margin_top = tf.margin_bottom = Emu(int(0.03 * E))
    pa = tf.paragraphs[0]; pa.alignment = align
    for i, p in enumerate(t.split("**")):
        if not p: continue
        r = pa.add_run(); r.text = p; r.font.size = Pt(size); r.font.name = font; r.font.bold = bold or (i % 2 == 1); r.font.color.rgb = color
def balloon(s, x, y, w, h, t, sizes, tail=False, name="Balloon"):
    if tail:
        b = box(s, MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT, x, y, w, h, BAL, BEDGE); b.adjustments[0] = -0.56 if w > 4 else -0.6; b.adjustments[1] = 0.0; b.adjustments[2] = 0.16667
    else: b = box(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, BAL, BEDGE)
    text(b, t, fit(t, w, h, sizes)); b.name = name; return b
def drop(sh): sh._element.getparent().remove(sh._element)
def setpos(sh, x=None, y=None, w=None, h=None):
    if x is not None: sh.left = Emu(int(x * E))
    if y is not None: sh.top = Emu(int(y * E))
    if w is not None: sh.width = Emu(int(w * E))
    if h is not None: sh.height = Emu(int(h * E))
def dark(sh):
    try: return sh.fill.type == 1 and str(sh.fill.fore_color.rgb) == "23272E"
    except Exception: return False
def code_slide(s, n):
    shapes = list(s.shapes); inch = lambda v: v / E
    codes = sorted([sh for sh in shapes if re.match(r"code \d+$", sh.name)], key=lambda sh: sh.top)
    res_t = [sh for sh in shapes if re.match(r"result \d+$", sh.name)]; assert len(res_t) == 1, (n, len(res_t))
    rt = res_t[0]; strip_bg = next(sh for sh in shapes if dark(sh) and abs(sh.left - 457200) < 40000 and sh.top <= rt.top <= sh.top + sh.height and sh.name.startswith("Rounded"))
    backs = [next(sh for sh in shapes if dark(sh) and sh.name.startswith("Rounded") and sh.top <= c.top <= sh.top + sh.height) for c in codes]
    inside = strip_bg in backs
    assert len(codes) == len(STORY[n]), (n, len(codes))
    obj = next(sh for sh in shapes if sh.has_table or sh.has_chart)
    texts = [sh for sh in shapes if sh.shape_type == 17 and sh.has_text_frame and sh.text_frame.text.strip() and 1.2 * E <= sh.top < 5.0 * E and sh not in codes and sh is not rt]
    label = next(t for t in texts if t.text_frame.text.startswith("Result:")); run = next(t for t in texts if t.text_frame.text.startswith("run under"))
    caption = next(t for t in texts if t.left > 6.0 * E and t is not label); expl = [t for t in texts if t not in (label, run, caption)]
    cap = caption.text_frame.text.strip(); labtxt = label.text_frame.text.strip(); runtxt = run.text_frame.text.strip(); out_runs = rt
    for sh in expl + [label, caption]: drop(sh)
    # sizes
    maxc = max(len(pa.text) for c in codes for pa in c.text_frame.paragraphs)
    bw = min(5.6, max(3.3, maxc * 0.0835 + 0.35)); RX = 0.5 + bw + 0.3; RW = 9.5 - RX
    for b, c in zip(backs, codes): setpos(b, w=bw); setpos(c, w=bw - 0.1)
    y = 1.26; units = []
    for i, c in enumerate(codes):
        hb = len(c.text_frame.paragraphs) * 0.17 + 0.16 + (0.24 if inside and i == len(codes) - 1 else 0); hs = min(max(need_h(STORY[n][i], 10.5, RW), 0.5), 0.95); unit = max(hb, hs)
        units.append((y, unit, hb, hs)); y += unit + 0.1
    code_end = y - 0.1
    for i, (c, b) in enumerate(zip(codes, backs)):
        yy, unit, hb, hs = units[i]; by0 = yy + (unit - hb) / 2 if hs > hb else yy
        setpos(b, y=by0, h=hb); setpos(c, y=by0 + 0.08)
        d = box(s, MSO_SHAPE.OVAL, 0.33, by0 - 0.11, 0.26, 0.26, ORANGE, ORANGE); d.name = "Step %d" % (i + 1)
        t = s.shapes.add_textbox(Emu(int(0.33 * E)), Emu(int((by0 - 0.11) * E)), Emu(int(0.26 * E)), Emu(int(0.26 * E))); t.name = "Step number %d" % (i + 1)
        text(t, str(i + 1), 11, "Cambria", True, MSO_ANCHOR.MIDDLE, 0, RGBColor(255, 255, 255), PP_ALIGN.CENTER)
        balloon(s, RX, yy, RW, hs, STORY[n][i], [10.5, 10, 9.5, 9], tail=True, name="Balloon note %d" % (i + 1))
    # output line under the code (or inside the last code box on slides where the line sits in that box)
    if inside:
        c = codes[-1]; setpos(out_runs, x=0.66, y=(c.top / E) + len(c.text_frame.paragraphs) * 0.17 + 0.07, w=bw - 0.3)
        for pa in out_runs.text_frame.paragraphs:
            for r in pa.runs: r.font.size = Pt(9 if len(out_runs.text_frame.text) * 0.064 > bw - 0.3 else 10)
        if len(out_runs.text_frame.text) * 0.058 > bw - 0.3: WARN.append("slide %d: output line long" % n)
        left_y = code_end + 0.1; sy = None
    else:
      sy = code_end + 0.1; osz = 10 if len(out_runs.text_frame.text) * 0.064 <= bw - 0.3 else 9
      two = len(out_runs.text_frame.text) * (0.064 if osz == 10 else 0.058) > bw - 0.3; sh_ = 0.5 if two else 0.3
      setpos(strip_bg, x=0.5, y=sy, w=bw, h=sh_); setpos(out_runs, x=0.66, y=sy + (0.07 if two else 0.075), w=bw - 0.3, h=sh_ - 0.1)
      out_runs.text_frame.word_wrap = True
      for pa in out_runs.text_frame.paragraphs:
          for r in pa.runs: r.font.size = Pt(osz)
    if not inside: left_y = sy + sh_ + 0.08
    # right column
    ry = max(yy + hs for (yy, unit, hb, hs) in units) + 0.1
    lab = box(s, MSO_SHAPE.ROUNDED_RECTANGLE, RX, ry, RW, 0.26, BAL); text(lab, labtxt, 10, bold=True); lab.name = "Result label"
    is_chart = obj.has_chart; avail = 4.97 - ry - 0.3
    if is_chart:
        setpos(obj, x=RX, y=ry + 0.3, w=RW, h=max(avail, 1.0))
        if avail < 1.3: WARN.append("slide %d: small chart %.2f in" % (n, avail))
    else:
        rows = len(obj.table.rows); rh = min(0.24, avail / rows)
        if rh < 0.2: WARN.append("slide %d: table rows %.2f in" % (n, rh))
        W0 = sum(c.width for c in obj.table.columns)
        for c in obj.table.columns: c.width = Emu(int(c.width * RW * E / W0))
        setpos(obj, x=RX, y=ry + 0.3, w=RW)
        for r in obj.table.rows:
            r.height = Emu(int(rh * E))
            for c in r.cells:
                c.margin_top = c.margin_bottom = Emu(int(0.02 * E))
                for pa in c.text_frame.paragraphs:
                    for rn_ in pa.runs: rn_.font.size = Pt(10 if rh >= 0.22 else 9)
    chb = max(need_h(cap, 10.5, bw), 0.42)
    balloon(s, 0.5, left_y, bw, chb, cap, [10.5, 10, 9.5], name="Result balloon")
    setpos(run, x=0.5, y=left_y + chb + 0.06, w=bw, h=0.34)
    if left_y + chb + 0.3 > 5.0: WARN.append("slide %d: left stack ends %.2f" % (n, left_y + chb + 0.3))
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else DST
    if os.path.exists(out) and out == DST: sys.exit("refuse: " + out + " exists")
    P = Presentation(SRC)
    for n in sorted(STORY): code_slide(P.slides[n - 1], n)
    print("slides changed:", len(STORY)); print("\n".join(WARN) if WARN else "no layout warnings"); P.save(out); print("wrote", out)
