#!/usr/bin/env python3
"""SEN0401 exam key-letters check, version 1.0.0 (new file). Holds no question and no answer.
For each choice item of the key (docx): (1) the letter after 'Correct answer:' equals the key place letter; (2) the text after it equals the option printed on the paper (docx) with that letter;
(3) every 'Why L is wrong' names a printed letter that is not the correct one, and the four wrong letters appear once each, in letter order; (4) the word PROVISIONAL is not doubled.
Usage: check.py DIR --tag TAG        runs the check on the set, then the SELF-TEST: planted wrong letters (a wrong 'Correct answer' letter, a wrong 'Why' letter, a doubled 'Why' letter, a doubled PROVISIONAL) must each make the check FAIL.
Exit 1 on any failure."""
import argparse, json, os, re, sys
sys.dont_write_bytecode = True
from docx import Document


def paras(p): return [x.text for x in Document(p).paragraphs]


def paper_options(pp):
    """{item label: {letter: option text}} from the printed paper: the stem paragraph starts with the label and a point; option paragraphs are 'A.<tab>text'."""
    out, cur = {}, None
    for t in pp:
        m = re.match(r'(\d[a-h])\. ', t)
        if m: cur = m.group(1); out[cur] = {}; continue
        o = re.match(r'([A-E])\.\t(.*)$', t)
        if o and cur is not None: out[cur][o.group(1)] = o.group(2)
        elif not o and t.strip() and not t.startswith(('Tip', 'Write', 'Circle', 'Choose')): pass
    return out


def key_blocks(kp):
    """{item label: lines of the item's entry} from the key paragraphs (heading '1a<tab>type ...')."""
    out, cur = {}, None
    for t in kp:
        m = re.match(r'(\d[a-h])\t(ChoiceFour\w*|Matching|Ordering|FillBlankGroup|NumericAnswer|CodeTrace)\s', t)
        if m: cur = m.group(1); out[cur] = []; continue
        if t.startswith(('DISCLOSURES', 'The answers, in')): cur = None
        if cur: out[cur].append(t)
    return out


def check(kp, pp, key):
    fails = []; PO = paper_options(pp); KB = key_blocks(kp)
    for e in key['items']:
        if not e['type'].startswith('ChoiceFour'): continue
        n = e['label']; place = e['answer'][n]; lines = KB.get(n)
        if not lines: fails.append('%s: no entry in the key' % n); continue
        opts = PO.get(n) or {}
        if len(opts) != 5: fails.append('%s: the paper prints %d options, expected 5' % (n, len(opts)))
        ca = [re.match(r'-?\s*Correct answer: ([A-E])\.\s*(.*)$', l.lstrip('-\t ')) for l in lines]; ca = [m for m in ca if m]
        if len(ca) != 1: fails.append('%s: %d Correct answer lines' % (n, len(ca))); continue
        L_, txt = ca[0].group(1), ca[0].group(2).strip()
        if L_ != place: fails.append('%s: Correct answer letter %s but the key place letter is %s' % (n, L_, place))
        if txt != opts.get(L_, '').strip(): fails.append('%s: Correct answer text differs from the printed option %s' % (n, L_))
        ws = [m.group(1) for m in (re.match(r'Why ([A-E]) is wrong:', l.lstrip('-\t ')) for l in lines) if m]
        want = [c for c in 'ABCDE' if c != place]
        if ws != want: fails.append('%s: Why-wrong letters %s, expected %s (each wrong printed letter once, in order)' % (n, ws, want))
        if any(re.search(r'PROVISIONAL\.\s*PROVISIONAL', l) for l in lines): fails.append('%s: PROVISIONAL doubled' % n)
    for t in kp:
        if re.search(r'PROVISIONAL\.?\s+PROVISIONAL', t): fails.append('PROVISIONAL doubled in: ' + t[:60])
    return fails


def plant(kp, kind):
    kp = list(kp)
    for i, t in enumerate(kp):
        if kind == 'correct' and 'Correct answer: ' in t and t.lstrip('-\t ').startswith('Correct answer: '):
            c = re.search(r'Correct answer: ([A-E])', t).group(1); kp[i] = t.replace('Correct answer: ' + c, 'Correct answer: ' + 'ABCDE'['ABCDE'.index(c) - 1], 1); return kp
        if kind == 'why' and re.match(r'-?\s*Why [A-E] is wrong', t.lstrip('-\t ') if False else t.replace('-\t', '', 1)):
            c = re.search(r'Why ([A-E]) is wrong', t).group(1); kp[i] = t.replace('Why ' + c + ' is wrong', 'Why ' + 'ABCDE'['ABCDE'.index(c) - 1] + ' is wrong', 1); return kp
        if kind == 'prov' and t.startswith('PROVISIONAL.'):
            kp[i] = 'PROVISIONAL. ' + t; return kp
    raise SystemExit('selftest: nothing to plant for ' + kind)


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('dir'); a.add_argument('--tag', required=True); x = a.parse_args()
    f = lambda e: os.path.join(x.dir, x.tag + e)
    kp, pp, key = paras(f('_key.docx')), paras(f('_paper.docx')), json.load(open(f('_key.json')))
    n = sum(1 for e in key['items'] if e['type'].startswith('ChoiceFour'))
    fl = check(kp, pp, key)
    for m in fl: print('FAIL ', m)
    print('%s  key letters check on the real key: %d choice items, %d failures' % ('PASS' if not fl and n == 7 else 'FAIL', n, len(fl)))
    bad = len(fl) or n != 7
    for kind, what in (('correct', 'planted wrong Correct answer letter'), ('why', 'planted wrong Why letter (a duplicate of another)'), ('prov', 'planted doubled PROVISIONAL')):
        r = check(plant(kp, kind), pp, key)
        ok = bool(r)
        print('%s  self-test, %s: the check %s (%d failure(s)%s)' % ('PASS' if ok else 'FAIL', what, 'failed as it must' if ok else 'did NOT fail', len(r), ': ' + r[0] if r else '')); bad = bad or not ok
    sys.exit(1 if bad else 0)
