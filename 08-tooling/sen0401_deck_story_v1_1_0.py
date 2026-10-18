"""sen0401_deck_story v1.1.0 (v1.0.0 plus the link-group helpers) - helpers for the deck patches that bring a story slide to the story and arc contracts (owner's coordinator, 2026-10-19):
a story slide shows its licence-clear picture with the credit as the caption, and the ISO date of the story in its fact row, together on the same slide.
Nothing here relaxes a check; the helpers only edit the plan dictionary that the renderer draws."""
__version__ = "1.1.0"

def slide(plan, n):
    return plan["slides"][n - 1]

def items(plan, n, t):
    return [it for it in slide(plan, n)["items"] if it["t"] == t]

def set_pic(plan, n, chapter, fname, cap, x, y, w, h, drop=()):
    """Put the story's picture on slide n: drop the images named in drop (file names), then add (or reuse the first image) at the given box with the credit as caption."""
    sl = slide(plan, n)
    sl["items"] = [it for it in sl["items"] if not (it["t"] == "img" and it["path"].split("/")[-1] in drop)]
    path = "../../03-materials/ch%s/assets/%s" % (chapter, fname)
    for it in sl["items"]:
        if it["t"] == "img" and it["path"].split("/")[-1] == fname:
            it.update(x=x, y=y, w=w, h=h, cap=cap); return it
    it = {"t": "img", "x": x, "y": y, "w": w, "h": h, "cap": cap, "path": path}
    sl["items"].insert(0, it); return it

def set_fact(plan, n, **kw):
    f = items(plan, n, "factrow")[0]; f.update(kw); return f

def move(plan, n, t, nth=0, **kw):
    it = items(plan, n, t)[nth]; it.update(kw); return it


def groups(plan, n):
    return items(plan, n, "links")[0]["groups"]

def find_row(plan, n, frag):
    for g in groups(plan, n):
        for r in g["rows"]:
            if frag in r[1]: return g, r
    raise KeyError(frag)

def swap_row(plan, n, frag, label=None, url=None, desc=None):
    g, r = find_row(plan, n, frag)
    if label: r[0] = label
    if url: r[1] = url
    if desc: r[2] = desc
    return r

def drop_row(plan, n, frag):
    g, r = find_row(plan, n, frag); g["rows"].remove(r)
    if not g["rows"]: groups(plan, n).remove(g)

def add_group(plan, n, head, rows, at=None):
    gs = groups(plan, n); g = {"head": head, "rows": [list(r) for r in rows]}
    gs.insert(len(gs) if at is None else at, g); return g
