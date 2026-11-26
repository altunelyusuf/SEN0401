#!/usr/bin/env python3
# v1.6.0 (Lineage 19, DC-S04): what is cut is read from the data. Each module record declares its audience (backlog:moduleAudience) and the deriver cuts every
# module declared private, banner to END MODULE line, in every data file. The list of seven IRIs that lived here is gone. The deriver now STOPS with an error
# when a module record declares no audience, when a module record has no END MODULE line (or an END line has no record), or when a module is declared private
# and its banner cannot be found: v1.5.0 skipped a listed module it could not find, which its own comment called "reported, never silent".
# v1.5.0 (Lineage 18, OC-S03/S05): the provenance records and the lesson deposit are modules of the two data files now, so the directories that held them
# no longer exist as files. The public copy leaves the same material out by module: each module that declares itself private is cut out, from its banner
# to its END MODULE line, before anything else is scrubbed. Nothing else is cut. (v1.6.0 reads the declaration; the list is gone.)
# v1.4.0 (Lineage 17, OESC-S04): follows the package's new layout. The alignment file now lives in 06-package-provenance, which is dropped whole.
"""make_public_distribution v1.3.0 — derive the public variant, reproducibly.

A public copy of a governed package is a second copy of the same vocabulary, and
two copies drift. So this is a script, not a hand-scrub: the transformation is
declared here, re-runnable, and its output is regenerable from the governed
package at any time. Per BP-D26 as enriched at OE Pack v20.27.0 — a verification
(or a scrub) performed but not encoded proves the moment, not the property.

WHAT IS REMOVED, and why each is removed rather than edited:

  the lesson deposit          proposals to OEE's lesson catalogue. Correspondence
                               with another session about their artifacts. A module of the live
                               data file now (the folder is gone); cut out by module.
  06-package-provenance/       ORCP registration records, publish records, and
                               cross-session proposals — the same.
  07-handover-inbox/           incoming proposals from lineage-consumer sessions
                               (VAF, code-abundance-rdodi, and others), pending,
                               accepted, rejected or deferred — correspondence
                               with other sessions about their own artifacts,
                               the same reason as the two directories above.
  06-package-provenance/  (the alignment file moved there at v1.339.0; the directory is dropped whole)
                               an alignment to ONE adopting project's private
                               deposit. Useless without that deposit and names it
                               throughout; scrubbing would leave an alignment to
                               nothing.
  04-documentation/Mapping_ProductBacklog_To_Backlog_v1_0_0.md
                               its companion document, likewise.
  04-documentation/ORCP_Submission_Backlog_v1_1_0.md
  04-documentation/OE_Registration_Readiness_Assessment_v1_0_0.md
  04-documentation/Discipline_Ceremony_Record_v1_0_0.md
  04-documentation/Discipline_Ceremony_Record_Addendum_v1_1_0.md
                               OE governance process records naming other
                               registrants and internal pack releases.

WHAT IS REWRITTEN rather than removed:

  Provenance sentences in skos:definition and prose that name the originating
  project are generalised to "an adopting project" / "an adopting project's
  product-backlog deposit". The FACT that the subject was generalised from a
  real deposit is true and worth keeping — L-112's spirit is that a record is
  corrected by stating the correction, not by pretending the history was
  different. What is removed is the identification, not the provenance.

WHAT IS DELIBERATELY KEPT:

  The author's name and institution. This is CC BY 4.0: attribution is not
  private data, it is the licence condition. Stripping it would breach the
  licence the package ships under. Only the unresolvable oe-prov: IRIs are
  replaced by literal attribution, since those dereference to nothing outside
  the ecosystem.

Usage: make_public_distribution_v1_5_0.py <governed-pkg> <output-dir>
"""

import os
import re
import shutil
import sys

# Modules of the data files are cut by what each declares about its audience (backlog:moduleAudience), not by a list kept here.


DROP_DIRS = ["06-package-provenance", "07-handover-inbox"]

DROP_FILES = [
    "04-documentation/Mapping_ProductBacklog_To_Backlog_v1_0_0.md",
    "04-documentation/ORCP_Submission_Backlog_v1_1_0.md",
    "04-documentation/OE_Registration_Readiness_Assessment_v1_0_0.md",
    "04-documentation/Discipline_Ceremony_Record_v1_0_0.md",
    "04-documentation/Discipline_Ceremony_Record_Addendum_v1_1_0.md",
    "04-documentation/Registration_Controls_v1_0_0.md",
    "04-documentation/Packaging_Requirements_v1_0_0.md",
    "03-tooling/backlog_registration_readiness_v1_2_0.py",
    "03-tooling/backlog_package_check_v1_0_0.py",
    "RELEASE_METRICS.txt",
    # the deriver removes ITSELF: its substitution patterns necessarily contain
    # the very names it strips, so shipping it in the public copy would
    # reintroduce them. Found by the leak scan before the first publication, and
    # again by the drift check, which reported the published copy as diverging
    # because the deriver was copying itself into its own output.
    "03-tooling/make_public_distribution_v1_6_0.py",
    "03-tooling/backlog_distribution_drift_check_v1_0_0.py",
]

# Order matters: longest and most specific first, so a later rule cannot
# re-match text an earlier one already generalised.
SUBSTITUTIONS = [
    # identified project -> generic adopter
    # Article-absorbing forms come FIRST. A bare-name rule applied to
    # "the FizyoVibe X" yields "the an adopting project X" — the substitution
    # is correct per-occurrence and the sentence is broken. Found by the
    # post-scrub damage check below, not by the residual scan, which is why
    # both exist.
    (r"\bthe FizyoVibe product-backlog deposit in OE Pack v[\d.]+[^)]*\)?",
     "an adopting project's product-backlog deposit"),
    (r"\bthe FizyoVibe product-backlog deposit", "an adopting project's product-backlog deposit"),
    (r"\bthe FizyoVibe\b", "an adopting project"),
    (r"\bThe FizyoVibe\b", "An adopting project"),
    (r"the FizyoVibe product-backlog deposit in OE Pack v[\d.]+",
     "an adopting project's product-backlog deposit"),
    (r"FizyoVibe's (own )?product-backlog deposit", r"an adopting project's product-backlog deposit"),
    (r"FizyoVibe methodology standard", "the originating project's methodology standard"),
    (r"the FizyoVibe (session|project|register|deposit)", r"an adopting project"),
    (r"FizyoVibe's", "the adopting project's"),
    (r"\bFizyoVibe\b", "an adopting project"),
    (r"fizyovibe-backlog-pattern", "adopter-backlog-pattern"),
    (r"\bfizyovibe\b", "adopting-project"),
    # other registrants
    (r"\bZT4SWE\b", "another registrant"),
    (r"\bRDODI\b", "another registrant"),
    (r"\bVAF\b", "another registrant"),
    (r"\bgradebook\b", "another registrant"),
    # private infrastructure
    (r"https://github\.com/altunelyusuf/[A-Za-z0-9_.-]+", "the project repository"),
    (r"github\.com/altunelyusuf/[A-Za-z0-9_.-]+", "the project repository"),
    (r"\baltunelyusuf\b", "the maintainer"),
    # unresolvable OE-internal provenance IRIs -> literal attribution
    (r"oe-prov:Agent_YusufAltunel", '"Yusuf Altunel"'),
    (r"oe-prov:Org_IKU_Department_of_ComputerEngineering",
     '"İstanbul Kültür Üniversitesi, Department of Computer Engineering"'),
    (r"<http://example\.org/oe-prov#Agent_YusufAltunel>", '"Yusuf Altunel"'),
    (r"<http://example\.org/oe-prov#Org_IKU_Department_of_ComputerEngineering>",
     '"İstanbul Kültür Üniversitesi, Department of Computer Engineering"'),
    # any remaining oe-prov term or its prefix declaration: that namespace does
    # not resolve outside the ecosystem, so a public consumer gets a dead pointer
    (r"@prefix oe-prov:\s*<[^>]*>\s*\.\n", ""),
    (r"oe-prov:[A-Za-z_]+", '"OE provenance record"'),
    (r"<http://example\.org/oe-prov#[A-Za-z_]+>", '"OE provenance record"'),
    # internal pack paths
    (r"OE Pack v[\d.]+,\s*06-registrant-deposits/[A-Za-z0-9_/-]*", "an OE Pack registrant deposit"),
    (r"06-registrant-deposits/[A-Za-z0-9_/-]*", "a registrant deposit"),
]

# Damage the substitutions themselves can cause. A residual scan asks "is the
# identifier gone"; this asks "is the sentence still English". Different questions,
# and the first cannot answer the second — found when a bare-name rule turned
# "the FizyoVibe deposit" into "the an adopting project deposit".
DAMAGE = [
    (r"\bthe an\b", "an"), (r"\ba an\b", "an"), (r"\ban a\b", "a"),
    (r"\bthe the\b", "the"), (r"\bof the an\b", "of an"),
]


TEXT_EXT = (".ttl", ".md", ".py", ".sh", ".txt", ".json")

BAR = "#" * 65


class ModuleError(SystemExit):
    pass


def cut_modules(text, name="a data file"):
    """Cut every module that declares moduleAudience Aud_Private out of a data file's text. Returns (new text, list of IRIs cut).

    Stops with an error (never skips) when: a module record declares no audience or an unknown one; a module record has no END MODULE line, or an END MODULE
    line has no record; or the banner before a private module's record cannot be found."""
    rec_re = re.compile(r"^<([^>\n]+)> dcterms:isPartOf <[^>\n]+> ;", re.M)
    end_re = re.compile(r"^#  END MODULE <([^>\n]+)>\n", re.M)
    records = {m.group(1): m.start() for m in rec_re.finditer(text)}
    ends = {m.group(1): m for m in end_re.finditer(text)}
    for iri in records:
        if iri not in ends:
            raise ModuleError("%s: module %s has a record but no '#  END MODULE <%s>' line, so it cannot be cut or kept with certainty" % (name, iri, iri))
    for iri in ends:
        if iri not in records:
            raise ModuleError("%s: '#  END MODULE <%s>' has no module record before it" % (name, iri))
    cut = []
    for iri, rstart in sorted(records.items(), key=lambda kv: -kv[1]):
        rend = text.index(" .\n", rstart)
        aud = re.search(r"backlog:moduleAudience\s+backlog:(Aud_\w+)", text[rstart:rend])
        if aud is None or aud.group(1) not in ("Aud_Public", "Aud_Private"):
            raise ModuleError("%s: module %s declares no audience (backlog:moduleAudience Aud_Public or Aud_Private)" % (name, iri))
        if aud.group(1) == "Aud_Public":
            continue
        e = ends[iri]
        bar = text.rfind(BAR + "\n#  MODULE ", 0, rstart)
        if bar < 0 or bar > rstart:
            raise ModuleError("%s: module %s is declared private and has no banner before its record, so it cannot be cut" % (name, iri))
        text = text[:bar].rstrip("\n") + "\n\n" + text[e.end():].lstrip("\n")
        cut.append(iri)
    return text, cut[::-1]


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    src, dst = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    if os.path.exists(dst):
        shutil.rmtree(dst)
    # .fixture-suite-stamp is a LOCAL cache key written by the gate after a passing
    # run. It is not part of the package: it records the state of one machine's
    # last run, so copying it makes a fresh derivation differ from any published
    # copy and the drift gate fails on a difference that means nothing. Found by
    # the drift gate refusing a publish for exactly this reason.
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
        "__pycache__", "*.pyc", ".git", ".fixture-suite-stamp",
        # .clause-proof-stamp is the same kind of thing and was missed when it
        # was added: a local cache key, meaningless in another checkout, and
        # shipping it made the drift gate report the public copy stale against
        # a fresh derivation that contained a file the public copy could not
        # have. One exclusion list, two caches, and only one was updated.
        ".clause-proof-stamp"))

    removed = []
    for d in DROP_DIRS:
        p = os.path.join(dst, d)
        if os.path.isdir(p):
            removed.append((d, sum(len(f) for _, _, f in os.walk(p))))
            shutil.rmtree(p)
    for f in DROP_FILES:
        p = os.path.join(dst, f)
        if os.path.exists(p):
            removed.append((f, 1))
            os.remove(p)

    rewritten = {}
    for dp, ds, fs in os.walk(dst):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in sorted(fs):
            if not f.endswith(TEXT_EXT):
                continue
            p = os.path.join(dp, f)
            try:
                t = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            orig = t
            n = 0
            if f.endswith(".ttl") and ("dcterms:isPartOf <" in t or "#  END MODULE <" in t):
                t, cut = cut_modules(t, f)
                for iri in cut:
                    removed.append(("module %s in %s" % (iri.rsplit("/", 1)[-1], f), 1))
            for pat, rep in SUBSTITUTIONS:
                t, k = re.subn(pat, rep, t)
                n += k
            for pat, rep in DAMAGE:
                t, k = re.subn(pat, rep, t)
                n += k
            if t != orig:
                open(p, "w", encoding="utf-8").write(t)
                rewritten[os.path.relpath(p, dst)] = n

    print("source : %s" % src)
    print("output : %s" % dst)
    print("\nremoved (%d):" % len(removed))
    for name, n in removed:
        print("   %-58s %d file(s)" % (name, n))
    print("\nrewritten (%d files, %d substitutions):" % (rewritten and len(rewritten) or 0,
                                                        sum(rewritten.values())))
    for f, n in sorted(rewritten.items(), key=lambda kv: -kv[1])[:14]:
        print("   %-58s %d" % (f, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
