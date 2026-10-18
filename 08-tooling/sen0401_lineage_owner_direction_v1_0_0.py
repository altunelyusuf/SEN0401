#!/usr/bin/env python3
"""sen0401_lineage_owner_direction v1_0_0 - records, in ONE new register version, that the stage revision of the third lineage from the Objective stage was directed by the owner and
confirmed by him, with both statements quoted and dated (as relayed by the course coordinator). Notes only: no state, evidence, digest or output changes; the earlier records stay as
committed (the revision's recorded decider stays the Builder role, which carried out his direction).
Usage: sen0401_lineage_owner_direction_v1_0_0.py"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

DIR = ("Owner's direction, 2026-10-19 00:51 Istanbul (2026-10-18T21:51:00 UTC), relayed by the course coordinator: \"If there is a requirement in the lineage you should never bypass it. "
       "This is a drift and breaking the rules. You should never do such a thing. And you should do this in time not after the completion of the work.\" This direction started the stage revision.")
CONF = ("Owner's confirmation, 2026-10-19 01:50 Istanbul (2026-10-18T22:50:00 UTC), relayed by the course coordinator: \"OK, confirmed. But do you need this? The current adaptations are initiated by my directions.\" "
        "He confirmed the stage revision from the Objective stage that paid the class-model debt, and said it follows from his direction.")
RULE = "From now on, work that follows from an owner's direction is recorded as owner-directed with the quoted direction and its time, and is not listed as an open owner confirmation."


def main():
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read()
    L = ['ex:%s rdfs:comment "%s"@en .\n' % (s, M.esc(x)) for s, x in (
        ("Revision_Lineage3_Objective", "Owner-directed and owner-confirmed. " + DIR + " " + CONF + " " + RULE),
        ("Out3_ObjectiveR", "Rebuilt by the owner-directed stage revision. " + DIR),
        ("Out3_BacklogR", "Rebuilt by the owner-directed stage revision, without a waiver. " + DIR + " " + CONF),
        ("Lineage3", "The stage revision of this lineage from the Objective stage is owner-directed and owner-confirmed; see the revision's note for both statements, quoted with their times."))]
    out = M.write_new(src, t + "\n" + "".join(L), nxt, cur, "The owner's direction (00:51) and confirmation (01:50) of 2026-10-19 recorded on the stage revision of the third lineage; notes only.")
    print(os.path.basename(out))


main()
