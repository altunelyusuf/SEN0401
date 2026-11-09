#!/usr/bin/env python3
"""sen0401_story_marker v1.0.0 - THE ONE PLACE where the marker of a story box and of its 5N1K coverage is defined
(owner's ruling 2026-11-09: 5N1K stays an internal authoring/review pattern; it must never surface to the audience
as visible WHO/WHAT/WHEN/WHERE/WHY/HOW field labels, in any order). Successor checks import this file and define
nothing of their own, the same convention sen0401_code_marker_v1_0_0.py set for code boxes.

THE MARKER
  story box   : a text box whose shape NAME starts with 'Story' (invisible metadata, never rendered on the slide canvas) -
                this is the narrative prose that carries the chapter's story; the audience sees only its sentence text.
  5N1K tag    : the shape's alt-text/description attribute (p:cNvPr/@descr, also invisible - the same field this deck
                standard already reads for chart-picture detection), holding a space-separated subset of
                who/what/when/where/why/how that the box's sentence actually covers. One story box rarely covers all
                six alone; the slide's coverage is the UNION of every story box's tags on that slide.
  visible label ban : a text box's visible text must never START with one of WHO/WHAT/WHEN/WHERE/WHY/HOW in ALL
                CAPS (the deck's own label marker) anywhere in the deck - not only on story slides. An ordinary
                sentence that happens to start with the same word in title case ("How a lock is written...") is
                not a label and is not banned. 'READ' is not part of 5N1K and is not banned either way.
"""
__version__ = "1.0.0"
import re

STORY_PREFIX = "story"
REQUIRED = frozenset({"who", "what", "when", "where", "why", "how"})
LABEL_RE = re.compile(r"^\s*(WHO|WHAT|WHEN|WHERE|WHY|HOW)\b\s*:?")  # case-sensitive: ALL CAPS is the on-screen label marker,
# distinct from an ordinary sentence that happens to start with the same word in title case ("How a lock is written...").


def is_story_name(name):
    return (name or "").strip().lower().startswith(STORY_PREFIX)


def tags_of(descr):
    """Alt-text/description -> the subset of REQUIRED words it names."""
    return {w.lower() for w in re.findall(r"[A-Za-z]+", descr or "")} & REQUIRED


def has_visible_label(text):
    return bool(LABEL_RE.match(text or ""))
