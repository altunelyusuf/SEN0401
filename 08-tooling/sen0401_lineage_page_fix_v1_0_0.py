#!/usr/bin/env python3
"""sen0401_lineage_page_fix v1_0_0 - records, in ONE new register version, the pages of chapters 1 to 7 rebuilt on template 9.51.0 from the corrected decks' lecture exports, as NEW dated evidence on the existing Done
page stories (G125 option 1: the defect is against each story's own criterion, stale links; the earlier evidence of the replaced page stays as the dated record). A chapter is recorded only where the evidence bridge
verified BOTH the chapter check Page/ChNN (v1_2_0, newest page test on a copy with a TEST release key: it proves the page's logic, not the real instructor key) AND the deck match check (the page carries what the deck carries),
and the SHA-256 of the page. The template 9.51.0 regression record of the page agent is cited by hash as a file; its counts are the agent's, not re-run here. The owner's direction is quoted.
Usage:  draft OUT.ttl   |   record BRIDGE.ttl"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = range(1, 8)
SPEC1 = "08-tooling/sen0401_lineage_chapter_check_v1_2_0.py"
SPEC2 = "08-tooling/sen0401_lineage_page_match_check_v1_0_0.py"
REG = "08-tooling/page_jobs_status.md"
CRIT = "backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission"
Q = "Keep the same standards with all other pages."
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def git_last(p):
    c = subprocess.check_output(["git", "log", "-1", "--format=%h %cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", p], cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).split()
    return c[0], c[1]


def pfile(n):
    p = os.path.relpath(sorted(glob.glob(os.path.join(REPO, "03-materials/ch%02d/page/sen0401_ch%02d_page_v*.html" % (n, n))), key=vkey)[-1], REPO)
    h, u = git_last(p); return p, hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest(), h, u


def nodes(vd=None, chapters=CH):
    items = []
    for n in chapters:
        tag = "Ch%02d" % n; p, s, h, u = pfile(n)
        items += [("Ev3PF_Page_" + tag, "T", 'ex:Ev3PF_Page_%s a backlog:TestEvidence ; rdfs:label "Chapter check for Page %s, run again on the rebuilt page (PF)"@en ; %s ;\n    backlog:hasTestId "Page/%s" ; backlog:hasTestSpec "%s"' % (tag, tag, CRIT, tag, SPEC1)),
                  ("Ev3PF_Match_" + tag, "T", 'ex:Ev3PF_Match_%s a backlog:TestEvidence ; rdfs:label "The page of %s carries what its deck carries (story cards, READ links, resources) (PF)"@en ; %s ;\n    backlog:hasTestId "Page/%s" ; backlog:hasTestSpec "%s"' % (tag, tag, CRIT, tag, SPEC2)),
                  ("Ev3PF_Page_%s_File1" % tag, "A", 'ex:Ev3PF_Page_%s_File1 a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC), rebuilt page"@en ; %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (tag, os.path.basename(p), h, u, CRIT, p, s))]
    h, u = git_last(REG)
    items.append(("Ev3PF_Regression", "A", 'ex:Ev3PF_Regression a backlog:ArtifactEvidence ; rdfs:label "page_jobs_status.md, committed %s (last change %s UTC): the page agent\'s record of the template 9.51.0 regression (agent-reported counts, not re-run here)"@en ; %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (h, u, CRIT, REG, hashlib.sha256(open(os.path.join(REPO, REG), "rb").read()).hexdigest())))
    out = ""
    for name, kind, body in items:
        if vd is None:
            out += body + " .\n"
        else:
            ok, at, meth = vd[name]; assert ok, name
            tool = "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" if kind == "T" else "backlog_evidence_bridge_v1_1_0"
            out += body + ' ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (S.esc(meth), tool, at)
    return out


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read()
    if sys.argv[1] == "draft":
        pre = "".join(l + "\n" for l in t.splitlines() if l.startswith("@prefix") or l.startswith("PREFIX"))
        open(sys.argv[2], "w", encoding="utf-8").write(pre + "\n" + nodes()); print("draft", sys.argv[2]); return
    vd = S.verdicts(sys.argv[2]); nxt, cur = M.next_version(src); now = M.now()
    good, bad = [], []
    for n in CH:
        tag = "Ch%02d" % n
        (good if all(("Ev3PF_%s_%s" % (k, tag)) in vd and vd["Ev3PF_%s_%s" % (k, tag)][0] for k in ("Page", "Match")) and vd["Ev3PF_Page_%s_File1" % tag][0] else bad).append(n)
    reg_ok = "Ev3PF_Regression" in vd and vd["Ev3PF_Regression"][0]
    add = nodes({k: v for k, v in vd.items()}, [n for n in good]) if good else ""
    if not reg_ok:
        add = add.split("ex:Ev3PF_Regression")[0]
    superseded = {1: 8, 2: 1, 3: 1, 4: 1, 5: 3, 6: 1, 7: 0}
    for n in CH:
        tag = "Ch%02d" % n; sid = "ST_Page_" + tag
        if n in good:
            p, s, h, u = pfile(n)
            ev = "ex:Ev3PF_Page_%s, ex:Ev3PF_Match_%s, ex:Ev3PF_Page_%s_File1" % (tag, tag, tag) + (", ex:Ev3PF_Regression" if reg_ok else "")
            add += ('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote "Correction recorded %s (G125 option 1, new evidence on the same Done story): the page had stale links against the story\'s own criterion; it was rebuilt as %s (commit %s) on template 9.51.0 from the corrected deck\'s lecture export, so story cards, READ links and resource lists equal the deck\'s. '
                    'The evidence bridge ran the chapter check Page/%s (newest page test, a TEST release key: it proves the page\'s logic, not the real instructor key) and the deck match check, and verified the SHA-256 of the page. The earlier evidence of the replaced page stays as the dated record. '
                    'Disclosed: the older tool pages_link_verify still compares with the OLD deck link registers (link_register_v1_0_0.json, 2026-10-16, untouched) and reports their superseded entries as not carried (%d for this chapter). Owner-directed: \\"%s\\" (2026-10-19)." .\n'
                    % (sid, ev, now[:10], os.path.basename(p), h, tag, superseded[n], S.esc(Q)))
        else:
            add += 'ex:%s backlog:hasAuditNote "Checked %s through the evidence bridge: the chapter check, the deck match check or the page hash did not verify for the rebuilt page, so nothing is recorded for it." .\n' % (sid, now[:10])
    out = M.write_new(src, t + "\n" + add, nxt, cur, "Rebuilt pages of chapters %s recorded as new evidence on the page stories (verified by the bridge); not recorded: %s." % (good, bad or "none"))
    print(os.path.basename(out), "good", good, "not", bad)


main()
