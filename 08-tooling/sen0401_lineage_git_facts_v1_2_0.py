#!/usr/bin/env python3
"""sen0401_lineage_git_facts v1_2_0 - reads, for the nine stories of chapters 5 to 7, the facts the register needs from git and from the files (ported from
sen0414_lineage_git_facts_v1_2_0): which built files carry each story, their SHA-256, the commits that first added and last changed them, and the UTC time of
that last change, which is the story's real finish (the moment its cited files, a .docx rendering apart, reached the form that is cited). "started" is the
earliest commit that added ANY version of the story's files. Writes FACTS.json; changes nothing in the repository. Needs the full history (git fetch --unshallow).

v1.1.0: the chapters and the kinds are arguments, and a part a chapter does not have (the .docx rendering) is skipped, not an error.
v1.2.0: a Deck also cites its link register, 08-tooling/chNN-deck/link_register_v1_0_0.json (the owner finding on links, read from that file).
Usage: sen0401_lineage_git_facts_v1_2_0.py OUT.json [CHAPTERS e.g. 5,6,7 (default)] [KINDS e.g. Research,Deck,Page (default)]
"""
__version__ = "1.2.0"
import datetime, glob, hashlib, json, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = (5, 6, 7)
vkey = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, check=True).stdout.strip()


def sha(p):
    return hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()


def newest(pattern):
    fs = glob.glob(os.path.join(REPO, pattern))
    return os.path.relpath(sorted(fs, key=vkey)[-1], REPO) if fs else None


def utc(iso):
    return datetime.datetime.fromisoformat(iso).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def first_any(patterns):
    ts = []
    for pat in patterns:
        for f in glob.glob(os.path.join(REPO, pat)):
            ts.append(git("log", "--diff-filter=A", "--format=%aI", "--", os.path.relpath(f, REPO)).splitlines()[-1])
    return min(utc(x) for x in ts)


def art(path):
    assert git("status", "--porcelain", "--", path) == "", "uncommitted change in " + path
    adds = git("log", "--diff-filter=A", "--format=%h %aI", "--", path).splitlines()
    first, ft = adds[-1].split()
    last, lt = git("log", "-1", "--format=%h %aI", "--", path).split()
    return {"path": path, "sha256": sha(path), "first_commit": first, "first_commit_utc": utc(ft), "last_commit": last, "last_commit_utc": utc(lt)}


def main():
    assert git("rev-parse", "--is-shallow-repository") == "false", "shallow clone: dates cannot be read; git fetch --unshallow"
    out = {"head": git("rev-parse", "--short", "HEAD"), "stories": {}}
    chapters = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else CHAPTERS
    kinds = sys.argv[3].split(",") if len(sys.argv) > 3 else ["Deck", "Research", "Page"]
    for n in chapters:
        m = "03-materials/ch%02d/" % n
        rd = m + "rdodi/sen0401_ch%02d_" % n
        sets = {"Deck": [newest(m + "SEN0401_Ch%02d_*_3e_v*.pptx" % n), "08-tooling/ch%02d-deck/link_register_v1_0_0.json" % n],
                "Research": [newest(rd + "research_v*.ttl"), newest(rd + "document_v*.ttl"), newest(rd + "document_v*.docx"),
                             newest(rd + "domain_tbox_v*.ttl"), newest(rd + "domain_abox_v*.ttl"), newest(rd + "domain_shacl_v*.ttl")],
                "Page": [newest(m + "page/sen0401_ch%02d_page_v*.html" % n)]}
        allv = {"Deck": [m + "SEN0401_Ch%02d_*_3e_v*.pptx" % n],
                "Research": [rd + "%s_v*.%s" % (p, e) for p, e in (("research", "ttl"), ("document", "ttl"), ("document", "docx"), ("domain_tbox", "ttl"), ("domain_abox", "ttl"), ("domain_shacl", "ttl"))],
                "Page": [m + "page/sen0401_ch%02d_page_v*.html" % n]}
        for kind, paths in sets.items():
            if kind not in kinds:
                continue
            a = [art(p) for p in paths if p]
            fin = max(x["last_commit_utc"] for x in a if not x["path"].endswith(".docx"))
            out["stories"]["ST_%s_Ch%02d" % (kind, n)] = {"artifacts": a, "started": first_any(allv[kind]), "finished": fin}
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    for k, v in out["stories"].items():
        print(k, v["started"], v["finished"], [os.path.basename(x["path"]) for x in v["artifacts"]][:2])


if __name__ == "__main__":
    main()
