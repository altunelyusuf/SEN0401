#!/usr/bin/env python3
"""Method: the rendered slide (soffice -> PDF) is read with pdftotext -bbox-layout; the words inside the chart area (x > 60 percent of the page width, y between 33 and 72 percent
of the page height) that are numbers are the data labels and axis numbers; every pair of word boxes whose rectangles intersect (positive area) is one overlapping pair.
Usage: label_overlap_count_v1_0_0.py PDF PAGE"""
import re, subprocess, sys, itertools
pdf, pg = sys.argv[1], sys.argv[2]
x = subprocess.run(["pdftotext", "-bbox", "-f", pg, "-l", pg, pdf, "-"], capture_output=True, text=True).stdout
W = float(re.search(r'<page width="([\d.]+)" height="([\d.]+)"', x).group(1)); H = float(re.search(r'<page width="([\d.]+)" height="([\d.]+)"', x).group(2))
ws = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', x)]
ch = [w for w in ws if w[0] > .6 * W and .33 * H < w[1] < .72 * H and re.fullmatch(r"[\d.,]+", w[4])]
pairs = [(p[4], q[4]) for p, q in itertools.combinations(ch, 2) if min(p[2], q[2]) - max(p[0], q[0]) > 0 and min(p[3], q[3]) - max(p[1], q[1]) > 0]
print("chart numeric words:", [w[4] for w in ch]); print("overlapping label pairs:", len(pairs), pairs)
