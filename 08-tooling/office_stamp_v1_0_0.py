#!/usr/bin/env python3
"""Writes the version a file's name carries into the file's own properties (title, author, version), as the
configuration-management rule requires of every office file this course repository produces.
Usage: office_stamp_v1_0_0.py <file.pptx|file.docx> <version> [title]"""
__version__ = "1.0.0"
import os, sys
p, v = sys.argv[1], sys.argv[2]; title = sys.argv[3] if len(sys.argv) > 3 else None
if p.endswith(".pptx"): from pptx import Presentation; d = Presentation(p)
else: import docx; d = docx.Document(p)
cp = d.core_properties; cp.version = v; cp.author = "Yusuf Altunel"
if title: cp.title = title
d.save(p); print("stamped", os.path.basename(p), v)
