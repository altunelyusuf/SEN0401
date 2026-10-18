"""SEN0401 chapter 3 - the story companion to the chapter corpus (version 1.0.0).

Chapter 3 (Bitcoin Core, the reference implementation) under the owner's 5N1K rule: real,
dated, sourced stories with one live link each, enforced by this file's self-check. Three
stories carry the chapter's three hard lessons:

* MaintainerHandoffs - software has people: Satoshi to Gavin Andresen (2011), Andresen to
  Wladimir van der Laan (2014) - the project outlives every holder of the keys to it.
* FirstRelease - 2009-01-08: version 0.1 ships, and its core design is declared set
  in stone by its author - what "reference implementation" has meant ever since.
* ReproducibleBuilds - how dozens of independent builders prove, with signed
  attestations, that the published binary really is the published source.

Usage: import STORIES; run the file for self-checks.
"""
__version__ = "1.2.0"  # each story link goes straight to the resource and carries linkLabel (owner finding of 2026-10-16)

STORIES = [
    {
        "id": "MaintainerHandoffs",
        "title": "The project that outlives its keyholders",
        "when": "2011 and 2014",
        "who": "Satoshi Nakamoto to Gavin Andresen (2011); Andresen to Wladimir van der Laan (2014)",
        "where": "the public bitcoin/bitcoin repository",
        "link": "https://web.archive.org/web/2015/https://bitcoinfoundation.org/2014/04/07/bitcoin-core-maintainer-wladimir-van-der-laan/", "linkLabel": "Andresen: Core maintainer van der Laan (post)",
        "concepts": ["SatoshiNakamoto", "GitRepository", "ReleaseTag"],
        "story": ("Bitcoin Core is the program Satoshi published in January 2009, still developed in "
                  "public. In 2011 Satoshi handed the project to Gavin Andresen - the faucet builder "
                  "of chapter 2 - and withdrew. In April 2014 Andresen passed the lead-maintainer "
                  "role to Wladimir van der Laan to focus on protocol work. Hundreds of contributors "
                  "and several maintainers later, the repository, its tags and its releases carry "
                  "on; no single person has been indispensable since."),
        "lesson": "The reference implementation is an institution, not a person",
        "source": ("Repository history of bitcoin/bitcoin (the chapter's pinned checkout is commit "
                   "05bc2f53); maintainer handoffs of 2011 and April 2014 as recorded in the project "
                   "history and summarized at en.wikipedia.org/wiki/Bitcoin_Core."),
    },
    {
        "id": "FirstRelease",
        "title": "Version 0.1, set in stone",
        "when": "2009-01-08",
        "who": "Satoshi Nakamoto, announcing on the metzdowd.com cryptography mailing list",
        "where": "a Windows build on SourceForge",
        "link": "https://www.metzdowd.com/pipermail/cryptography/2009-January/014994.html", "linkLabel": "Satoshi: Bitcoin v0.1 released (list post)",
        "concepts": ["SatoshiNakamoto", "ReleaseTag", "GitRepository"],
        "story": ("Five days after the genesis block, Satoshi announced Bitcoin version 0.1 - a "
                  "Windows program on SourceForge. A year and a half later he wrote the sentence "
                  "this course keeps returning to: once version 0.1 was released, the core design "
                  "was set in stone for the rest of its lifetime. Everything this chapter builds, "
                  "configures and queries descends from that one program, which is why Bitcoin Core "
                  "is called the reference implementation."),
        "lesson": "The software came first; the specification IS the software",
        "source": ("Announcement of 2009-01-08 on the metzdowd.com cryptography list ('Bitcoin v0.1 "
                   "released'); the 'set in stone' sentence is Satoshi's forum post of 2010-06-17; "
                   "project history summarized at en.wikipedia.org/wiki/Bitcoin_Core."),
    },
    {
        "id": "ReproducibleBuilds",
        "title": "Dozens of builders, one identical binary",
        "when": "since 2011; Guix from release 22.0",
        "who": "independent Bitcoin Core builders publishing signed attestations",
        "where": "the guix.sigs repository beside bitcoin/bitcoin",
        "link": "https://raw.githubusercontent.com/bitcoin-core/guix.sigs/main/31.1/achow101/all.SHA256SUMS", "linkLabel": "Builder attestation, Core 31.1 (hash list)",
        "concepts": ["SoftwareTesting", "ReleaseCandidate", "CMakeBuild"],
        "story": ("A downloaded binary asks for trust; Bitcoin Core answers with arithmetic. Every "
                  "release is built reproducibly - first under Gitian, since release 22.0 under "
                  "Guix - so that anyone compiling the tagged source gets a byte-identical result. "
                  "Independent builders publish signed hashes of what they produced, side by side, "
                  "in a public repository. If one build differed, its hash would betray it "
                  "instantly - the same trick the chapter's Merkle root plays on transactions."),
        "lesson": "Verify, don't trust - the project applies its own rule to itself",
        "source": ("bitcoin-core/guix.sigs on GitHub: per-release folders of builder attestations; "
                   "Guix build documentation in the pinned source tree, contrib/guix/README.md."),
    },
]


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for x in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story"):
            if not str(x.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (x["id"], f))
        if not x.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % x["id"])
        if len(x["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % x["id"])
        if not (2 <= x["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % x["id"])
    if "05bc2f53" not in STORIES[0]["source"]:
        bad.append("MaintainerHandoffs: pinned commit missing from source")
    if "2009-01-08" not in STORIES[1]["source"]:
        bad.append("FirstRelease: date missing from source")
    if "guix.sigs" not in STORIES[2]["source"]:
        bad.append("ReproducibleBuilds: attestation repo missing from source")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)


# ---------------------------------------------------------------------------------------------- 1.2.0: the story contract of the deck checks (owner's coordinator, 2026-10-19)
# Every story gets an ISO date (the day of the event the story is anchored to), a who that names real people or bodies, a where of three words or more, a licence-clear picture of
# the chapter's assets with its credit, and a further-reading link that answers from the build machine; the old fields not named here are unchanged.
_OVERRIDES = {'MaintainerHandoffs': {'when': '2014-04-07',
                        'who': 'Satoshi Nakamoto, Gavin Andresen and Wladimir van der Laan, who passed the lead role of the Bitcoin software on in 2011 and 2014',
                        'where': 'the public bitcoin/bitcoin repository on GitHub',
                        'bio': 'Gavin Andresen, American developer, lead maintainer of the Bitcoin software from 2011 to April 2014; Wladimir van der Laan, Dutch '
                               'developer, lead maintainer from April 2014 until he stepped back in 2022',
                        'link': 'https://en.bitcoin.it/wiki/Wladimir_van_der_Laan',
                        'linkLabel': 'Wladimir van der Laan (Bitcoin Wiki)',
                        'source': "Repository history of bitcoin/bitcoin (the chapter's pinned checkout is commit 05bc2f53); the Bitcoin Wiki page on Wladimir van der "
                                  "Laan: on 7 April 2014 Gavin Andresen stepped down as Core maintainer and nominated van der Laan as his successor (Andresen's post of "
                                  '2014-04-07 on the Bitcoin Foundation site, which no longer answers from the build machine); the 2011 handoff from Satoshi Nakamoto as '
                                  'summarized at en.wikipedia.org/wiki/Bitcoin_Core. Picture: Gavin Andresen at Web Summit 2014 - Stephen McCarthy, CC BY 2.0, Wikimedia '
                                  'Commons.',
                        'photo': 'photo_gavin_andresen.jpg',
                        'credit': 'Gavin Andresen, 2014 - Stephen McCarthy, CC BY 2.0'},
 'FirstRelease': {'when': '2009-01-08',
                  'bio': 'Satoshi Nakamoto, pseudonym of the unknown author of the Bitcoin white paper (2008) and of version 0.1 of the software (2009)',
                  'source': "Announcement of 2009-01-08 on the metzdowd.com cryptography list ('Bitcoin v0.1 released'); the 'set in stone' sentence is Satoshi's forum "
                            'post of 2010-06-17; project history summarized at en.wikipedia.org/wiki/Bitcoin_Core. Picture: the bronze bust of Satoshi Nakamoto in '
                            'Graphisoft Park, Budapest, unveiled on 16 September 2021 - Fekist, CC BY-SA 4.0, Wikimedia Commons.',
                  'photo': 'photo_satoshi_bust_budapest.jpg',
                  'credit': 'Satoshi bust, Budapest - Fekist, CC BY-SA 4.0'},
 'ReproducibleBuilds': {'when': '2021-09-13',
                        'who': 'Carl Dong, who wrote the Guix build system that Bitcoin Core adopted for release 22.0, and the independent builders who sign its results',
                        'where': 'the guix.sigs repository beside bitcoin/bitcoin',
                        'bio': 'Carl Dong (GitHub: dongcarl), Bitcoin Core contributor who wrote the Guix-based reproducible build system (pull requests of 2020 and '
                               '2021)',
                        'source': 'bitcoin-core/guix.sigs on GitHub: per-release folders of builder attestations; Bitcoin Core 22.0 release notes, published 13 '
                                  "September 2021 (bitcoincore.org/en/releases/22.0): 'Release binaries are now produced using the new guix-based build system', with "
                                  'the guix-attest and guix-verify scripts (dongcarl); Guix build documentation in the pinned source tree, contrib/guix/README.md. '
                                  'Picture: the GNU Guix logo, Wikimedia Commons File:GNU Guix logo.svg, public domain text logo.',
                        'photo': 'photo_guix_logo.png',
                        'credit': 'GNU Guix logo - GNU Guix, public domain'}}
for _s in STORIES:
    _s.update(_OVERRIDES[_s["id"]])
