"""sen0401_deck_geom v1.0.0 - helper for the chapter deck patches: a code or program item with a label and a caption draws its label row 0.22 in ABOVE its box (the caption shares that row),
so it needs a clear 0.24 in above it. gap_pass(plan) moves such an item down to the end of the nearest item above that it overlaps horizontally, keeping its height and shortening it only to stay above y 4.98; items below it are moved in turn."""
__version__ = "1.0.0"
LABEL_ROW = 0.24; BOTTOM = 4.98; TOP = 1.62
def _end(it): return it.get("y", 0) + it.get("h", 0)
def gap_pass(plan, only=None, log=True):
    for si, s in enumerate(plan["slides"], 1):
        if only and si not in only: continue
        its = s["items"]
        for k, it in enumerate(sorted([i for i in its if i["t"] in ("code", "prog") and i.get("cap") and i.get("label")], key=lambda i: i["y"])):
            above = [o for o in its if o is not it and o.get("h") and o["y"] < it["y"] + 0.05 and _end(o) > it["y"] - 0.5 and o["x"] < it["x"] + it["w"] - 0.05 and o["x"] + o["w"] > it["x"] + 0.05 and _end(o) <= it["y"] + 0.3]
            need = max([_end(o) for o in above] + [(1.66 if s.get('lede') else TOP - LABEL_ROW)]) + LABEL_ROW
            if it["y"] < need - 0.005:
                old = (it["y"], it["h"]); it["y"] = round(need, 2); it["h"] = round(max(0.5, min(_end(it) if False else it["y"] + old[1], BOTTOM) - it["y"]), 2)
                if log: print("  gap_pass slide %d: %s y %.2f->%.2f h %.2f->%.2f" % (si, it["t"], old[0], it["y"], old[1], it["h"]))
