#!/usr/bin/env python3
"""backlog_package_check v1.0.0 — does an adopter's register package ship what it
must, under the naming rules that already govern it?

The framework does not restate filename or version rules. The OE configuration
subject owns them: fifteen NamingConvention individuals, each carrying a
`filenamePattern` template and the artifact type it applies to. A register
artifact declares which convention it follows; this tool reads that convention's
pattern **from the pack at check time** and tests the declared filename against
it. There is therefore one source of truth for naming, and it is not this file.

Without --pack the naming check reports NOT RUN. It is never assumed to pass:
a pattern this tool cannot read is a pattern it cannot enforce.

Usage:
  backlog_package_check_v1_0_0.py REGISTER.ttl [--pack /path/to/oepack]
"""

import argparse
import glob
import os
import re
import sys

import rdflib
from rdflib import Graph, RDF, Namespace

BL = Namespace("http://example.org/backlog#")
CFG = Namespace("http://example.org/configuration#")

PLACEHOLDERS = [
    ("{Capitalised_name}", r"[A-Z][A-Za-z0-9_]*"),
    ("{prefix}", r"[a-z][a-z0-9_]*"),
    ("{name}", r"[A-Za-z][A-Za-z0-9_-]*"),
    ("{module}", r"[a-z][a-z0-9_-]*"),
    ("{scope}", r"[a-z][a-z0-9_-]*"),
    ("{variant}", r"[a-z0-9_]+"),
    ("{ext}", r"[a-z0-9]+"),
    ("{M}", r"\d+"),
    ("{m}", r"\d+"),
    ("{p}", r"\d+"),
]


def template_to_regex(template):
    """Translate an OE filenamePattern template into a regex, mechanically."""
    out = re.escape(template)
    for token, pattern in PLACEHOLDERS:
        out = out.replace(re.escape(token), pattern)
    return "^" + out + "$"


def load_conventions(pack):
    """Read the naming conventions from the pack's configuration subject."""
    g = Graph()
    for f in glob.glob(os.path.join(pack, "01-ontologies", "configuration_*.ttl")):
        g.parse(f, format="turtle")
    conventions = {}
    for s in g.subjects(RDF.type, CFG.NamingConvention):
        pattern = g.value(s, CFG.filenamePattern)
        if pattern is not None:
            conventions[str(s)] = str(pattern)
    return conventions


def main():
    ap = argparse.ArgumentParser(description="Check a register package against OE naming conventions.")
    ap.add_argument("register", help="Turtle file declaring the RegisterPackage")
    ap.add_argument("--pack", default=None, help="path to an extracted OE Pack, enabling the naming check")
    args = ap.parse_args()

    g = Graph()
    g.parse(args.register, format="turtle")

    packages = list(g.subjects(RDF.type, BL.RegisterPackage))
    if not packages:
        print("no RegisterPackage declared in %s" % os.path.basename(args.register))
        return 1

    conventions = load_conventions(args.pack) if args.pack else None
    print("register    : %s" % os.path.basename(args.register))
    print("conventions : %s" % ("%d read from the pack" % len(conventions) if conventions
                                else "NOT RUN — no --pack given, so no filename is checked"))

    failures = 0
    for pkg in packages:
        version = g.value(pkg, BL.hasPackageVersion)
        artifacts = list(g.objects(pkg, BL.hasPackageArtifact))
        print("\npackage %s  version %s  %d artifact(s)"
              % (str(pkg).rsplit("#", 1)[-1], version, len(artifacts)))
        roles = {}
        for a in artifacts:
            role = g.value(a, BL.hasArtifactRole)
            name = g.value(a, BL.hasArtifactFileName)
            conv = g.value(a, BL.conformsToNamingConvention)
            role_name = str(role).rsplit("#", 1)[-1] if role else "—"
            roles[role_name] = roles.get(role_name, 0) + 1
            verdict = "not checked"
            if conventions is not None and conv is not None:
                template = conventions.get(str(conv))
                if template is None:
                    verdict = "FAIL — convention %s not in the pack" % str(conv).rsplit("#", 1)[-1]
                    failures += 1
                elif re.match(template_to_regex(template), str(name or "")):
                    verdict = "matches %s" % template
                else:
                    verdict = "FAIL — %s does not match %s" % (name, template)
                    failures += 1
            elif conventions is not None and role_name != "Role_Manifest":
                verdict = "FAIL — no convention declared"
                failures += 1
            print("  %-22s %-34s %s" % (role_name, str(name), verdict))
        for required in ("Role_RegisterData", "Role_Manifest"):
            if roles.get(required, 0) < 1:
                print("  MISSING role: %s" % required)
                failures += 1
        if roles.get("Role_Manifest", 0) > 1:
            print("  MORE THAN ONE manifest artifact")
            failures += 1

    print("\nVERDICT     : %s" % ("PASS" if failures == 0 else "FAIL — %d finding(s)" % failures))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
