"""Shared text normalisation and similarity for the SEN0401 mock exclusion index and gate (v1.0.0).
Code only. The index (private) lives in the private CME repository; this file holds no item text."""
import re, difflib
from collections import Counter

NUM_RE = re.compile(r"\d[\d,\.]*")
THRESH_GRAM5 = 0.35     # token 5-gram Jaccard, stem against indexed stem (fail at or above)
THRESH_WORD = 0.60      # word-level similarity (sequence ratio over tokens), fail at or above
THRESH_NUM_SIM = 0.30   # numeric: stem similarity above which an equal key value with the same unit fails
MIN_OPT_TOKENS = 3      # options / premises shorter than this are not compared by equality
DOC_CONTAIN = 0.35      # containment of the 5-grams of a stem in the 5-grams of one whole document

def norm(s):
    s = str(s).lower()
    s = s.replace("’", "'").replace("–", "-").replace("—", "-")
    s = re.sub(r"[^0-9a-z' ,\.]+", " ", s)
    s = re.sub(r"(?<=\d)[,\.](?=\d)", "", s)       # 37,000 -> 37000
    s = re.sub(r"[,\.]+(?=\s|$)", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def toks(s, mask=False):
    t = drop_fixed(s).split()
    if mask:
        t = ["#" if re.fullmatch(r"[\d]+", w) else w for w in t]
    return t

def grams(t, n=5):
    if len(t) < n:
        return {tuple(t)} if t else set()
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)}

def jacc(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def ratio_upper(ta, tb):
    c = sum((Counter(ta) & Counter(tb)).values())
    return 2.0 * c / (len(ta) + len(tb)) if (ta or tb) else 0.0

def seqratio(ta, tb):
    return difflib.SequenceMatcher(None, ta, tb, autojunk=False).ratio()

def stem_scores(ta_raw, tb_raw, ta_mask, tb_mask, ga_raw, gb_raw, ga_mask, gb_mask):
    """returns (gram5_jaccard, word_ratio); each is the max of the raw and the number-masked reading."""
    g = max(jacc(ga_raw, gb_raw), jacc(ga_mask, gb_mask))
    w = 0.0
    if ratio_upper(ta_mask, tb_mask) >= 0.5:   # necessary condition: sequence ratio never exceeds multiset ratio
        w = max(seqratio(ta_raw, tb_raw), seqratio(ta_mask, tb_mask))
    return g, w

def strip_label(p):
    return re.sub(r"^\s*(?:[A-Ea-e]|\d+[a-c]?|[1-5])[\.\)]\s+", "", p.strip())

FIXED_SENTENCES = ["You are asked to fill each blank with the bank entry that makes the sentence true.", "One response is not used."]

def drop_fixed(text):
    """removes the sentences shared by every exam (fixed wording) before any comparison"""
    t = " " + norm(text) + " "
    for f in FIXED_SENTENCES:
        t = t.replace(" " + norm(f) + " ", " ")
    return t.strip()
