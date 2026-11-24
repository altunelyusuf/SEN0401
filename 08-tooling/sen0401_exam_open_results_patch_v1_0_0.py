#!/usr/bin/env python3
"""Chapter page patch: the mock exam shows its results and answers at once, and exam and results are two views.

  sen0401_exam_open_results_patch_v1_0_0.py PAGE.html            writes the next minor version beside it (never edits PAGE)

Owner request 2026-11-24: students must see their mock exam results and the answers after finishing; the same exam can be taken
again as often as they wish; the exam and the results are two different functions.
Before: finishing an exam locked the score and the answers until the instructor gave a signed release code.
After : finishing stores the attempt, marks it as open (release 'open') and switches to the RESULTS view (score, subjects, every
        question with the student's answer and the correction). "Take the exam" is the exam view: it never shows a result
        or a correction. Earlier locked attempts in the browser are opened. Retake opens the same questions blank.
Everything else in the page stays byte-identical; each anchor must occur exactly once or the script stops."""
import re, sys, os

def sub1(s, old, new, name):
    if s.count(old) != 1:
        sys.exit('anchor "%s" found %d times (need 1) - page not patched' % (name, s.count(old)))
    return s.replace(old, new, 1)

CSS = ('.xvtabs{margin:.4rem 0}.xvtabs .btn[aria-pressed="true"]{background:var(--blue);color:#fff}'
       '[data-pane="exam"][data-xv="exam"] #xehist,[data-pane="exam"][data-xv="exam"] #xeclearbox{display:none}'
       '[data-pane="exam"][data-xv="res"] .xsetup{display:none}'
       '[data-pane="exam"][data-xv="exam"] #xeout.xreview{display:none}'
       '[data-pane="exam"][data-xv="res"] #xeout:not(.xreview){display:none}\n')

JS = r'''
// ---- results are open; exam and results are two views (page patch 1.0.0) ----
function xvSet(v){const p=document.querySelector('[data-pane="exam"]');if(!p)return;p.dataset.xv=v;[['xvexam','exam'],['xvres','res']].forEach(([i,k])=>{const b=document.getElementById(i);if(b)b.setAttribute('aria-pressed',k===v?'true':'false')})}
XS.recs.forEach(r=>{if(r.status==='done'&&r.res&&!r.released){r.released=true;r.release='open'}});xSave();xHistPaint();
{const _st=xExamStart;xExamStart=async function(fromRec){const o=document.getElementById('xeout');if(o)o.classList.remove('xreview');xvSet('exam');await _st(fromRec)}}
{const _rv=xExamReview;xExamReview=async function(rec){await _rv(rec);const o=document.getElementById('xeout');if(o)o.classList.add('xreview');xvSet('res')}}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('#xvexam,#xvres');if(!b)return;e.stopImmediatePropagation();xvSet(b.id==='xvres'?'res':'exam')},true);
xvSet('exam');
'''

def patch(src):
    s = src
    m = re.search(r'"_version": "(\d+)\.(\d+)\.(\d+)"', s)
    a, b, c = map(int, m.groups())
    new = '%d.%d.0' % (a, b + 1)
    s = sub1(s, m.group(0), '"_version": "%s"' % new, 'data _version')
    # 1. texts
    s = sub1(s, "After you finish, your score and the correct answers stay hidden until your instructor gives you the release code; the result file is what gets marked.",
             "After you finish, your score, the correct answers and the corrections are shown at once under My results, and you may take the same exam again as often as you wish. The result file is there if your instructor asks you to hand one in.", 'pane text')
    s = sub1(s, "Score (released by the instructor): ", "Score: ", 'pdf score')
    s = sub1(s, "put('The score and the correct answers are withheld until the instructor gives the release code. The instructor marks the result file.',24,false,'#B42318',14)",
             "put('The score and the answers are in the page under My results.',24,false,'#2F6D62',14)", 'pdf withheld')
    # 2. finishing opens the result instead of locking it
    s = sub1(s, "if(rec&&!rec.released)xLockPaint(rec)}}",
             "if(rec){rec.released=true;rec.release='open';xSave();xHistPaint();await xExamReview(rec)}}}", 'finish wrapper')
    s = sub1(s, "xExamReview=async function(rec){if(rec.released){",
             "xExamReview=async function(rec){if(!rec.released&&rec.res){rec.released=true;rec.release='open';xSave();xHistPaint()}if(rec.released){", 'review wrapper')
    # review of an open attempt: keep the hand-in buttons under the summary (already added by that branch)
    # 3. two views
    s = sub1(s, 'data-pane="exam" hidden>', 'data-pane="exam" data-xv="exam" hidden>', 'pane attr')
    s = sub1(s, '<div class="xid"', '<div class="row xvtabs" role="group" aria-label="Exam or results"><button class="btn" id="xvexam" aria-pressed="true">Take the exam</button><button class="btn g" id="xvres" aria-pressed="false">My results</button></div><div class="xsetup"><div class="xid"', 'xid')
    s = sub1(s, '<div id="xeout" aria-live="polite">', '</div><div id="xeout" aria-live="polite">', 'xeout')
    s = sub1(s, '.xid{border:1px solid', CSS + '.xid{border:1px solid', 'css')
    s = sub1(s, "document.addEventListener('click',e=>{if(e.target&&e.target.id==='xestart')xidPaint()},true);\nxidPaint();\n",
             "document.addEventListener('click',e=>{if(e.target&&e.target.id==='xestart')xidPaint()},true);\nxidPaint();\n" + JS, 'tail anchor')
    # 3b. repair (Ch14 page 9.99.0 only): a doubled comma in the group list left a hole that made the tab trail fail, so the Mock exam tab could not open
    if ']]:[]),,...tops' in s:
        s = sub1(s, ']]:[]),,...tops', ']]:[]),...tops', 'ch14 doubled comma')
    # 4. header note
    s = sub1(s, '<!doctype html><html lang="en"><head><meta charset="utf-8">',
             '<!doctype html><html lang="en"><head><meta charset="utf-8"><!-- page %s over %d.%d.%d (owner request 2026-11-24): the mock exam opens its score, answers and corrections after finishing (no release code); exam and results are two views; the same exam can be retaken as often as wished. Nothing else changed. -->' % (new, a, b, c), 'head')
    return s, new

def main():
    p = os.path.abspath(sys.argv[1])
    src = open(p, encoding='utf-8').read()
    out, new = patch(src)
    d, f = os.path.split(p)
    nf = re.sub(r'_v\d+_\d+_\d+\.html$', '_v' + new.replace('.', '_') + '.html', f)
    dst = os.path.join(d, nf)
    if os.path.exists(dst):
        sys.exit('refuse: %s exists' % dst)
    open(dst, 'w', encoding='utf-8').write(out)
    print(dst)

if __name__ == '__main__':
    main()
