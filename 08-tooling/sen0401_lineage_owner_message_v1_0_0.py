#!/usr/bin/env python3
"""sen0401_lineage_owner_message v1_0_0 - ONE new register version, notes only: the owner's message of 2026-10-21 about the pages built on older templates, recorded as owner-directed with the quote and the time (relayed by the
course coordinator), with the facts the coordinator measured and the page strings I re-checked. No state, evidence, digest or output changes. Usage: no arguments."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

Q = ("Owner's message, relayed by the course coordinator on Wednesday 2026-10-21 08:12 Istanbul (05:12 UTC), quoted: \"Do we have any solutions for older template pages? Do we have work items for these chapters? If they are not matching with the standards "
     "how can we say the mission is reached? Is it about a gap in the goals or mission? If you think it is better to close the current lineage and start a new one for those quality enhancements, we can consider on that. But my current feeling tells me to finish "
     "them first before the final closure. What do you say?\" ")
F = ("Measured on 2026-10-21 (coordinator; the strings re-checked by the builder session in the newest page HTML of each chapter): pages 8, 10, 11, 12 and 14 (page versions 9.51.0, 9.53.0, 9.54.0, 9.55.0, 9.57.0) do not contain the template 9.50.0/9.51.0 code "
     "('const LBLRE=LBL.map' and 'function edVars()' are present in pages 1 to 7, 9 and 13 and absent in 8, 10, 11, 12 and 14): they lack the label-aware ERD untangle of 9.50.0 and the faster load of 9.51.0. Their content matches the decks (0 not carried on all five); "
     "their test counts do not change on 9.51.0 (regression, commit 0f7d21f). Page 8 also fails page test 9.34.0 (113 pass, 1 fail, then a crash): no chapter 8 example has a number in its code. The register holds no work item for any of this. "
     "The question is open, not decided: this note records the message and the facts; it opens no story, changes no scope and records no outcome. The Mission outcome stays the owner's act and is not recorded.")


def main():
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read()
    L = ['ex:%s rdfs:comment "%s"@en .\n' % (s, M.esc(x)) for s, x in (
        ("Lineage3", "Owner-directed question, not yet answered by a decision. " + Q + F),
        ("CR_SEN0401", "Before the closure act: " + Q + F))]
    out = M.write_new(src, t + "\n" + "".join(L), nxt, cur, "The owner's message of 2026-10-21 on the pages of older templates recorded with the quote and time; notes only.")
    print(os.path.basename(out))


main()
