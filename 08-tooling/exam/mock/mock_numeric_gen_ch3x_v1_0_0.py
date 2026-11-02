#!/usr/bin/env python3
"""SEN0401 mock bank, chapter 3 extra family 'release_tags', generator v1.0.0.
Every order, place, move and key is computed here from the tag list. Usage: mock_numeric_gen_ch3x_v1_0_0.py --out PATH
Holds no real exam content. Tag counts used are 4, 5 and 7; each instance has its own list; no tag pair is a prefix case,
so the first differing character of two tags is always a digit in both and no hidden sorting rule is needed."""
import argparse, json, random, sys
sys.dont_write_bytecode = True

WHY_QUESTION = ("Why this question: a software version is a sequence of numbers, not a word. A tool that sorts text puts v10 "
                "before v9, so someone who trusts text order picks the wrong release. Listing both orders step by step "
                "shows how far they differ.")
COUNTS = (4, 5, 7)
N_INST = 8


def ordinal(n):
    return "%d%s" % (n, "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def parse(t):
    a, b = t[1:].split(".")
    return int(a), int(b)


def orders(tags):
    txt = sorted(tags)
    num = sorted(tags, key=parse)
    return txt, num


def facts(tags):
    txt, num = orders(tags)
    pt = {t: txt.index(t) + 1 for t in tags}
    pn = {t: num.index(t) + 1 for t in tags}
    mv = {t: abs(pt[t] - pn[t]) for t in tags}
    inv = sum(1 for i in range(len(tags)) for j in range(i + 1, len(tags))
              if (pt[tags[i]] < pt[tags[j]]) != (pn[tags[i]] < pn[tags[j]]))
    return dict(txt=txt, num=num, pt=pt, pn=pn, mv=mv, inv=inv)


def prefix_free(tags):
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            a, b = tags[i], tags[j]
            k = 0
            while k < min(len(a), len(b)) and a[k] == b[k]:
                k += 1
            if k >= min(len(a), len(b)) or not (a[k].isdigit() and b[k].isdigit()):
                return False
    return True


def draw_list(rng, n, want_minor_pair):
    for _ in range(5000):
        tags = set()
        if want_minor_pair:
            m = rng.randint(2, 30)
            tags.add("v%d.%d" % (m, rng.randint(1, 9)))
            tags.add("v%d.%d" % (m, rng.randint(10, 15)))
        while len(tags) < n:
            maj = rng.choice([rng.randint(1, 9), rng.randint(10, 39)])
            tags.add("v%d.%d" % (maj, rng.randint(1, 12)))
        tags = sorted(tags)
        if len(tags) != n:
            continue
        majors = [parse(t)[0] for t in tags]
        if not (any(m < 10 for m in majors) and any(m >= 10 for m in majors)):
            continue
        if not prefix_free(tags):
            continue
        rng.shuffle(tags)
        return tags
    raise RuntimeError("no list")


PRE_ORDERS = ("Text order compares tags character by character, from the left. "
              "Number order compares major numbers, then minor numbers, as numbers. ")
MOVE_DEF = "A tag's move is how many places apart its text-order position and number-order position are. "


def stem(tags, ask, with_move):
    return ("Release tags: %s. " % ", ".join(tags)) + PRE_ORDERS + (MOVE_DEF if with_move else "") + "You are asked to " + ask


def nonzero_movers(f):
    return [t for t in f["pt"] if f["mv"][t] > 0]


# each template: (id, unit, tip, with_move, builder(f, tags, rng) -> (ask, key, tail_step, wrongs[(value, why)]) or None)
def b1(f, tags, rng):
    key = sum(f["mv"].values())
    ch = sum(1 for t in tags if f["mv"][t])
    return ("calculate the sum of the moves of all tags.", key,
            "Add all moves: %s = %d." % (" + ".join(str(f["mv"][t]) for t in f["txt"]), key),
            [(key // 2, "Summed one direction only (tags that moved later), which is half of the total."),
             (ch, "Counted the tags that change place instead of adding their moves."),
             (max(f["mv"].values()), "Took the largest single move instead of the sum of all moves."),
             (f["inv"], "Counted pairs in a different relative order instead of adding moves.")])


def b2(f, tags, rng):
    t = rng.choice(nonzero_movers(f))
    key = f["mv"][t]
    return ("calculate the move of %s." % t, key,
            "%s is %s in text order and %s in number order, so its move is %d." % (t, ordinal(f["pt"][t]), ordinal(f["pn"][t]), key),
            [(f["pt"][t], "Gave the place in text order instead of the gap between the two places."),
             (f["pn"][t], "Gave the place in number order instead of the gap between the two places."),
             (f["pt"][t] + f["pn"][t], "Added the two places instead of subtracting them."),
             (sum(f["mv"].values()), "Gave the sum of all moves instead of the move of this tag.")])


def b3(f, tags, rng):
    key = sum(1 for t in tags if f["mv"][t])
    return ("calculate how many tags change place between the two orders.", key,
            "Tags with a move above 0: %s. Their count is %d." % (", ".join(t for t in f["txt"] if f["mv"][t]), key),
            [(sum(f["mv"].values()), "Added the moves instead of counting the tags that move."),
             (len(tags), "Counted every tag, including those that keep their place."),
             (len(tags) - key, "Counted the tags that keep their place instead of those that change."),
             (f["inv"], "Counted pairs in a different relative order instead of tags.")])


def b4(f, tags, rng):
    t = rng.choice(nonzero_movers(f))
    key = f["pt"][t]
    return ("calculate the place of %s in the text order." % t, key,
            "In the text order written above, %s stands %s." % (t, ordinal(key)),
            [(f["pn"][t], "Gave the place in number order, ranking by number instead of by text."),
             (len(tags) + 1 - key, "Counted the place from the end of the list instead of the start."),
             (key - 1, "Counted the tags before it instead of giving its place."),
             (key + 1, "Counted one place too far, starting the count at 2.")])


def b5(f, tags, rng):
    key = max(f["mv"].values())
    big = [t for t in f["txt"] if f["mv"][t] == key]
    return ("calculate the largest move among the tags.", key,
            "Largest move: %d, for %s." % (key, " and ".join(big)),
            [(sum(f["mv"].values()), "Added all moves instead of taking the largest."),
             (sum(1 for t in tags if f["mv"][t]), "Counted the tags that change place instead of taking the largest move."),
             (len(tags), "Gave the number of tags instead of the largest move."),
             (sum(f["mv"].values()) // 2, "Summed one direction only instead of taking the largest move.")])


def b6(f, tags, rng):
    key = f["inv"]
    n = len(tags)
    pairs = [(a, b) for i, a in enumerate(f["txt"]) for b in f["txt"][i + 1:] if f["pn"][a] > f["pn"][b]]
    return ("calculate how many pairs of tags stand in a different relative order in the two orders.", key,
            "Pairs whose order is reversed (%d): %s." % (key, ", ".join("%s/%s" % p for p in pairs)),
            [(sum(1 for t in tags if f["mv"][t]), "Counted the tags that change place instead of the pairs."),
             (sum(f["mv"].values()), "Added the moves instead of counting pairs."),
             (n * (n - 1) // 2 - key, "Counted the pairs in the same relative order instead of the reversed ones."),
             (n * (n - 1) // 2, "Counted all pairs, not only those in a different relative order.")])


def b7(f, tags, rng):
    first = f["num"][0]
    key = f["pt"][first]
    if key < 2:
        return None
    return ("calculate the place in the text order of the tag that is first in the number order.", key,
            "First in number order is %s; in text order it stands %s." % (first, ordinal(key)),
            [(1, "Gave its number-order place, ranking by number twice."),
             (len(tags) + 1 - key, "Counted its text-order place from the end of the list."),
             (key - 1, "Counted the tags before it instead of giving its place."),
             (key + 1, "Counted one place too far, starting the count at 2.")])


def b8(f, tags, rng):
    key = sum(1 for t in tags if not f["mv"][t])
    if key < 1:
        return None
    return ("calculate how many tags keep the same place in both orders.", key,
            "Tags with move 0: %s. Their count is %d." % (", ".join(t for t in f["txt"] if not f["mv"][t]), key),
            [(len(tags) - key, "Counted the tags that change place instead of those that keep it."),
             (len(tags), "Counted every tag, including those that change place."),
             (sum(f["mv"].values()), "Added the moves instead of counting the tags that stay."),
             (key + 1, "Counted one tag too many, adding a tag that moves.")])


TEMPLATES = [
    ("n3x_1", "places", "Find each tag's two places, then add the gaps.", True, b1, True),
    ("n3x_2", "places", "Subtract the smaller place from the larger place.", True, b2, False),
    ("n3x_3", "tags", "A tag changes place when its two places differ.", False, b3, False),
    ("n3x_4", "place", "Sort by characters, left to right, then count places.", False, b4, False),
    ("n3x_5", "places", "Work out every gap first, then choose the biggest.", True, b5, False),
    ("n3x_6", "pairs", "Look at each pair of tags in both orders.", False, b6, False),
    ("n3x_7", "place", "Find the lowest number first, then locate it in text order.", False, b7, False),
    ("n3x_8", "tags", "Count the tags whose two places are equal.", False, b8, False),
]


def build():
    items = []
    seen = set()
    for ti, (tid, unit, tip, wm, fn, can4) in enumerate(TEMPLATES):
        insts = []
        k = 0
        rng = random.Random(30000 + ti * 101)
        guard = 0
        tries = 0
        usedkeys = set()
        while len(insts) < N_INST:
            guard += 1
            tries += 1
            if guard > 400000:
                raise RuntimeError("stuck " + tid)
            n = COUNTS[len(insts) % 3]
            tags = draw_list(rng, n, len(insts) % 2 == 0)
            if frozenset(tags) in seen:
                continue
            f = facts(tags)
            if f["txt"] == f["num"]:
                continue
            r = fn(f, tags, rng)
            if r is None:
                continue
            ask, key, tail, wr = r
            if not (1 <= key <= 99999):
                continue
            if key in usedkeys and tries < 20000:   # prefer a new key value; repeats only when the range is used up
                continue
            wrongs, used = [], {key}
            for v, why in wr:
                if v >= 0 and v not in used and v <= 99999:
                    used.add(v); wrongs.append({"value": v, "why": why})
                if len(wrongs) == 3:
                    break
            if len(wrongs) < 3:
                continue
            seen.add(frozenset(tags))
            usedkeys.add(key)
            tries = 0
            per = "; ".join("%s: %d and %d, move %d" % (t, f["pt"][t], f["pn"][t], f["mv"][t]) for t in f["txt"])
            steps = ["Text order: %s." % ", ".join(f["txt"]),
                     "Number order: %s." % ", ".join(f["num"]),
                     "Places in text order and number order, with each move: %s." % per,
                     tail]
            insts.append({"stem": stem(tags, ask, wm), "key_value": key, "steps": steps,
                          "why_right": "Both orders were written out from the tag list, each tag's two places were compared, and the asked value was computed from them: %d." % key,
                          "common_wrong": wrongs})
        items.append({"id": tid, "type": "numeric", "chapter": 3, "points": 3, "can_be_4": can4, "unit": unit,
                      "tip": tip, "why_question": WHY_QUESTION, "instances": insts})
    return {"chapter": 3, "family": "release_tags", "items": items}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(build(), fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote", a.out)
