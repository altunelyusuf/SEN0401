#!/usr/bin/env python3
"""sen0401_lineage_correct_note v1_0_0 - ONE new register version that corrects, forward, two audit notes written in v0.115 (the committed version and its notes stay as the record, L-112; no state, evidence or digest changes).
The error is the course session's: it took the coordinator's briefing for both chapters and did not check it against the research files before writing. Read from the physical files (research v1.3.0 of chapters 3 and 4):
chapter 3's finding F15 cites only the JSON-RPC 2.0 specification (P85) beside the sources it already had; BIP 142 (P17) is chapter 4's F15 source, and chapter 4 has no P85 at all.
Usage: sen0401_lineage_correct_note_v1_0_0.py"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def has(n, tok):
    return tok in open(os.path.join(REPO, "03-materials/ch0%d/rdodi/sen0401_ch0%d_research_v1_3_0.ttl" % (n, n)), encoding="utf-8").read()


def main():
    assert has(3, "chx:P85") and not has(4, "chx:P85") and has(4, "chx:P17"), "the files no longer say what this correction says"
    f3 = re.search(r"chx:F15 a sen0401:Finding.*?\n", open(os.path.join(REPO, "03-materials/ch03/rdodi/sen0401_ch03_research_v1_3_0.ttl"), encoding="utf-8").read()).group(0)
    assert "P17" not in f3 and "P85" in f3
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read()
    base = ("Correction recorded %s, an error of the course session (not of the framework or the research agent's files): the audit note written in register v0.115 for this task named the wrong sources for finding F15. " % M.now()[:10])
    c3 = base + ("It said that chapter 3's F15 cites the JSON-RPC 2.0 specification (P85) and BIP 142 (P17). Read from the research file v1.3.0 of chapter 3, F15 cites only the JSON-RPC 2.0 specification (P85), beside the sources it already had (P01, P25); it does not cite BIP 142. "
                 "BIP 142 (P17) is chapter 4's F15 source. The briefing the session was given said both, and the session wrote it without checking the file. Nothing else in the note changes; the older note stays as the dated record (L-112).")
    c4 = base + ("It said that chapter 4's F15 cites P85 and BIP 142 (P17). Read from the research file v1.3.0 of chapter 4, F15 cites BIP 142 (P17), with its existing sources; chapter 4 has no P85 (the JSON-RPC 2.0 specification) at all - that source is chapter 3's. "
                 "The P17 label correction from Wuille 2015 to Lau 2015, and the statement about F15's Closed status and BIP 173 replacing 142 being read from saved copies, stand as written. The session wrote the note from the briefing without checking the file. The older note stays as the dated record (L-112).")
    add = "".join('ex:%s backlog:hasAuditNote "%s" .\n' % (k, M.esc(v)) for k, v in (("TK_Research_Ch03_Stage3F", c3), ("TK_Research_Ch04_Stage3F", c4)))
    out = M.write_new(src, t + "\n" + add, nxt, cur, "Two audit notes of v0.115 corrected forward: chapter 3's F15 cites only P85 and chapter 4's F15 cites P17 and not P85 (an error of the course session).")
    print(os.path.basename(out))


main()
