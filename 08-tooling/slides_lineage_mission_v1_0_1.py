"""Mission stage of the SEN0401 slide-renewal lineage. Forked from SEN0414's under time pressure on
2026-09-25 - recorded as a finding to consolidate both into one CME-held builder, not left implicit."""

__version__ = "1.0.1"
MISSION = """
ex:Mission a backlog:Mission ;
    rdfs:label "Teach SEN0401 from the edition students can now read for free"@en ;
    backlog:missionFor ex:Backlog ;
    backlog:hasMissionStatement "Every SEN0401 lecture teaches what the third edition of Mastering Bitcoin teaches, chapter by chapter, with a deck, the research behind it and an interactive page - renewed from the book and researched evidence, within the term theme of semantic technologies." ;
    backlog:hasMissionOrigin "Owner rulings of 2026-09-24 and 2026-09-25: the course outline was updated to the third edition of Mastering Bitcoin (Antonopoulos and Harding, O'Reilly, December 2023, CC BY-SA 4.0) and its fourteen chapters; the term theme is semantic technologies; and on 2026-09-25 at 01:15 Istanbul time the owner made SEN0401's first chapter the most urgent work, ahead of SEN0414's second, because SEN0401 teaches at 09:00 that morning. Measured before this mission was written: the SEN0401 repository was created empty on 2026-09-24 and holds nothing; the book's source, tag third_edition_print1, lists fourteen chapters." ;
    backlog:hasMissionOutcome "A student in SEN0401 finds, for each chapter, a deck, an interactive page and the sources behind them, grounded in the edition they can read for free." ;
    backlog:outcomeRationale "The course was being taught from a second-edition outline whose chapter structure the third edition changed: Signatures and Transaction Fees are new chapters, and the old scripting chapter became Authorization and Authentication. Renewing chapter by chapter against the source is the only way to teach what students actually read." ;
    backlog:decidedBy backlog:Owner ;
    backlog:producedByStage ex:Out_Mission ;
    backlog:missionSource "Mastering Bitcoin, 3rd edition, from the authors' own repository at tag third_edition_print1 (github.com/bitcoinbook/bitcoinbook); research by RDODI's four-stage procedure v1.6.0 with its pedagogy stage; structured by CME's course profile." .
"""


def mission_block():
    return MISSION
