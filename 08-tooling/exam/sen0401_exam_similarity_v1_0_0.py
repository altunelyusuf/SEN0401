"""SEN0401 page-copy similarity method, version 1.0.0 (new file). Pure library: no output when imported.

PURPOSE  The engine rule EN11 refuses a paper item that COPIES a page-visible item. The page-visible set is what a student can open before the sitting:
  - 08-tooling/ch0N-page/question_bank_v*.json, the NEWEST version of each chapter (the bank items embedded in the page), and
  - 08-tooling/ch0N-page/quiz_v1_0_0.json (the page quiz items),
  for N = 1 to 6 (and any further chapter that is in the chapter list of the paper, if its page files exist).

THE METHOD (stated here BEFORE the first run of the fixtures; the thresholds are constants below and are not tuned on the fixtures)
  1. Normalise. Lower case; every character that is not a letter or a digit becomes a space (punctuation and spacing are removed); runs of spaces collapse.
     A text is then a list of WORDS, and its SQUASHED form is the words joined without spaces.
  2. A text of an item has two halves: the STEM TEXT (the question, followed by the code listing if there is one: a stem like 'What does this program print?' is generic,
     the program makes the item) and the OPTION SET (the options after normalisation, as a set).
  3. Four tests. A candidate component matches a page item when ANY of them holds:
       STEM_EXACT     the squashed stem texts are equal.
       STEM_NEAR      both stems have at least STEM_MIN_WORDS words and the Jaccard share of their WORD 2-SHINGLES (pairs of neighbouring words) is at least STEM_NEAR_J2.
       OPTIONS_EXACT  the two option sets are equal after normalisation (order does not matter) and hold at least 3 DISTINCTIVE options.
       OPTIONS_NEAR   the share of equal DISTINCTIVE options, taken over the size of the smaller set, is at least OPTIONS_NEAR_SHARE (3 of 4).
     and a fifth, COMBINED: the stem share is at least COMBINED_STEM_J2 AND the option share is at least COMBINED_OPTIONS_SHARE (a stem partly kept and options partly kept).
     A DISTINCTIVE option is one that is longer than 3 characters after squashing and is not made only of the words true / false / none / yes / no and digits.
  4. Components. A choice item is one component (stem text, options). A matching item has each premise as a stem and the response list as an option set.
     An ordering item has each step as a stem and the step list as an option set. A fill-in group has each blank sentence as a stem and the bank entries as an option set.
     A number item, a trace item and a short-answer item have the stem text.

WHY EACH THRESHOLD IS WHERE IT IS  (measured on the page-visible set itself, 1228 items; the numbers are printed by the check)
  STEM_NEAR_J2 = 0.60 and STEM_MIN_WORDS = 10. For a stem of n words in which one interior word is changed, the 2-shingle Jaccard is (n-3)/(n+1): 0.636 for n = 10 and higher for longer
     stems. So 0.60 keeps a copy with one changed word (and two changed words in a stem of about 20 words or more) while a stem shorter than 10 words is judged by the exact test only
     (one changed word in 6 words leaves a share of 0.43, and 'What is a protocol?' against 'What is a database?' differs by one word yet asks something else).
     On the other side: among the 637 pairs of DIFFERENT page items of the SAME concept in the same chapter the largest stem share is 0.40 (99th percentile 0.18). 0.60 sits above all of them.
     Among all 130195 same-chapter pairs of page items only 22 reach 0.60: they are template siblings (a program whose hex literal changed, a seed asked for two word lists).
  OPTIONS_NEAR_SHARE = 0.75. With four options this is three equal options of four: a copy with one distractor replaced. Two of four (0.5) happens by chance for options such as
     numbers and truth values; that is why the guard 'distinctive' exists. Without the guard 70 pairs of different page items reach 0.75 (truth tables, small numbers); with it 3 do.
  COMBINED: 0.35 and 0.50 are a stem about half kept and half the options kept; the weakest evidence the method acts on. Among the page items it fires on 4 pairs.
  The thresholds are chosen so that a copy and a near copy (a word changed, an option order changed, one option replaced) are refused and an item that asks the same concept in
  its own words is not. The error that is accepted is the safe one: a false REFUSE costs the item author one rewording; a false PASS leaks a question.

WHAT THE METHOD CANNOT SEE  (disclosed in the check as well)
  - a PARAPHRASE of the idea (new words, same question and same answer): shares no shingles and no options. A person has to judge it; the seed and critical-point links of the item help.
  - a short stem (under 10 words) with two or more options rewritten: it passes unless the stem is exactly equal.
  - an item whose options are only truth values, small numbers or very short tokens and whose stem is rewritten: the options are not counted.
  - the same question in another language, with the numbers or the code only renamed (renamed identifiers change shingles), or the same code with a different question.
  - items the page builds on the fly in the browser (the exam desk, xExamBuild): they are not in any file, so they are not in the page-visible set.
  - any version of a bank that is not the newest of its chapter.
"""
import glob, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.dirname(HERE)
VERSION = '1.0.0'

STEM_MIN_WORDS = 10
STEM_NEAR_J2 = 0.60
OPTIONS_NEAR_SHARE = 0.75
OPTIONS_MIN_DISTINCTIVE_FOR_EXACT = 3
COMBINED_STEM_J2 = 0.35
COMBINED_OPTIONS_SHARE = 0.50
DEFAULT_PAGE_CHAPTERS = (1, 2, 3, 4, 5, 6)
_TRIVIAL = re.compile(r'^(true|false|none|yes|no|\d)+$')


def words(s): return re.findall(r'[a-z0-9]+', (s or '').lower())
def squash(s): return ''.join(words(s))
def shingles(w, n=2): return {tuple(w[i:i + n]) for i in range(max(1, len(w) - n + 1))} if w else set()
def distinctive(o):
    s = squash(o); return len(s) > 3 and not _TRIVIAL.match(s)


def prepare(stem, options=None):
    """A comparable record of one component: stem text and option set (either may be empty)."""
    w = words(stem); opts = [squash(o) for o in (options or []) if squash(o)]
    return dict(stem=stem or '', w=w, sq=''.join(w), sh=shingles(w), opts=set(opts), n_opts=len(set(opts)), dist={squash(o) for o in (options or []) if distinctive(o)})


def jaccard(a, b): return len(a & b) / len(a | b) if (a | b) else 0.0


def compare(c, p):
    """Compare a prepared candidate component c with a prepared page item p. Returns (kinds, stem_share, option_share)."""
    ss = jaccard(c['sh'], p['sh']) if (c['w'] and p['w']) else 0.0
    n = min(c['n_opts'], p['n_opts'])
    os_ = (len(c['dist'] & p['dist']) / n) if n else 0.0
    kinds = []
    if c['sq'] and c['sq'] == p['sq']: kinds.append('STEM_EXACT')
    elif len(c['w']) >= STEM_MIN_WORDS and len(p['w']) >= STEM_MIN_WORDS and ss >= STEM_NEAR_J2: kinds.append('STEM_NEAR')
    if c['opts'] and c['opts'] == p['opts'] and len(c['dist']) >= OPTIONS_MIN_DISTINCTIVE_FOR_EXACT and len(p['dist']) >= OPTIONS_MIN_DISTINCTIVE_FOR_EXACT: kinds.append('OPTIONS_EXACT')
    elif os_ >= OPTIONS_NEAR_SHARE: kinds.append('OPTIONS_NEAR')
    if not kinds and ss >= COMBINED_STEM_J2 and os_ >= COMBINED_OPTIONS_SHARE: kinds.append('COMBINED')
    return kinds, ss, os_


def newest_bank(n):
    fs = glob.glob(os.path.join(TOOL, 'ch%02d-page' % n, 'question_bank_v*.json'))
    if not fs: return None
    fs.sort(key=lambda x: [int(v) for v in x.rsplit('_v', 1)[1][:-5].split('_')])
    return fs[-1]


def page_items(chapters=DEFAULT_PAGE_CHAPTERS):
    """The page-visible set for the chapters: a list of dicts {ref, chapter, source, file, index, prepared}. Read only.
    ref is the stable name of a page item: 'ch02/question_bank_v1_0_0.json#17' (bank item 17, counted from 0) or 'ch02/quiz_v1_0_0.json#3'."""
    out = []
    for n in sorted(set(chapters)):
        f = newest_bank(n)
        if f:
            for i, b in enumerate(json.load(open(f, encoding='utf8'))):
                st = (b['q'] + '\n' + b['code']) if b.get('code') else b['q']
                out.append(dict(ref='ch%02d/%s#%d' % (n, os.path.basename(f), i), chapter=n, source='bank', file=os.path.relpath(f, os.path.dirname(TOOL)), index=i, p=prepare(st, b['options'])))
        q = os.path.join(TOOL, 'ch%02d-page' % n, 'quiz_v1_0_0.json')
        if os.path.exists(q):
            for i, b in enumerate(json.load(open(q, encoding='utf8'))['items']):
                out.append(dict(ref='ch%02d/quiz_v1_0_0.json#%d' % (n, i), chapter=n, source='quiz', file=os.path.relpath(q, os.path.dirname(TOOL)), index=i, p=prepare(b['q'], b['options'])))
    return out


def find_matches(c, pages):
    """All page items a prepared component matches: [(ref, kinds, stem_share, option_share)]."""
    out = []
    for pg in pages:
        kinds, ss, os_ = compare(c, pg['p'])
        if kinds: out.append((pg['ref'], kinds, round(ss, 3), round(os_, 3)))
    return out


def thresholds():
    return dict(version=VERSION, STEM_MIN_WORDS=STEM_MIN_WORDS, STEM_NEAR_J2=STEM_NEAR_J2, OPTIONS_NEAR_SHARE=OPTIONS_NEAR_SHARE,
                OPTIONS_MIN_DISTINCTIVE_FOR_EXACT=OPTIONS_MIN_DISTINCTIVE_FOR_EXACT, COMBINED_STEM_J2=COMBINED_STEM_J2, COMBINED_OPTIONS_SHARE=COMBINED_OPTIONS_SHARE)


def components(item):
    """The comparable components of an authored item of any type: [(label, stem_text, options_list)]."""
    t = item['type']
    if t in ('ChoiceFour', 'ChoiceFourCode'):
        return [('item', (item['q'] + '\n' + item['code']) if item.get('code') else item['q'], item['options'])]
    if t == 'Matching':
        return [('premise %d' % (k + 1), p['text'], None) for k, p in enumerate(item['premises'])] + [('responses', '', item['responses'])]
    if t == 'Ordering':
        return [('step %d' % (k + 1), s, None) for k, s in enumerate(item['steps'])] + [('steps', '', item['steps'])]
    if t == 'FillBlankGroup':
        return [('blank %d' % (k + 1), b['text'], None) for k, b in enumerate(item['blanks'])] + [('bank', '', [b['answer'] for b in item['blanks']] + list(item['distractors']))]
    if t in ('NumericAnswer', 'ShortAnswer'): return [('item', item['q'], None)]
    if t == 'CodeTrace': return [('item', item['q'] + '\n' + item['code'], None)]
    raise ValueError('unknown item type %s' % t)
