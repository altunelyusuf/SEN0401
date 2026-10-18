"""sen0401_deck_story v1.0.0 - helpers for the deck patches that bring a story slide to the story and arc contracts (owner's coordinator, 2026-10-19):
a story slide shows its licence-clear picture with the credit as the caption, and the ISO date of the story in its fact row, together on the same slide.
Nothing here relaxes a check; the helpers only edit the plan dictionary that the renderer draws."""
__version__ = "1.0.0"

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
