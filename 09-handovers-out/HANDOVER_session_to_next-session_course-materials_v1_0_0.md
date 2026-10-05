# Handover to the next session: SEN0401 and SEN0414 course materials, the book ontology, and the ceremony

**From:** the course-materials session of 2026-10-01 to 2026-10-05 (one session, 443 API calls, measured).
It is being closed deliberately, not because anything broke: its context had grown to 623,335 tokens per call
from a measured floor of 101,590, and 96.1% of the 152,117,612 tokens it was billed were cache reads of its own
history. A fresh session costs about a fifth as much over the next 25 calls. The numbers come from the
transcript's own API-reported usage, not from an estimate.

**To:** the next session working on these course materials.

**Covers two course repositories and one resource package.** This file lives in SEN0401 because that is where
most of the open items are; everything it says about SEN0414 is equally current.

---

## 1. Standing instruction, unchanged

Revive the OE discipline from the GitHub page first of all and never trust your memory or summaries. Proceed
under the strict OE discipline file latest version on
<https://github.com/altunelyusuf/Ontologies/tree/main/oe-method/04-documentation/> and the lineage discipline
file on <https://github.com/altunelyusuf/Ontologies/blob/main/backlog-roadmap-framework/04-documentation/> if
accessible, otherwise use local disk, and execute the ceremony first.

**The ceremony is now one command**, and it is stricter than reading files by hand:

    bash /home/claude/Ontologies/repo-tooling/oe_ceremony_v1_0_0.sh

It checks access, freshness against origin, the discipline version compared with the repository through the
authenticated API, the counts, and the manifest with the stowaway-aware verifier, then prints PROCEED or REFUSE.
It earned its keep in this session's last hour: it refused because the checkout had silently gone one commit
behind. Clear a REFUSE before any governed action; do not work around it.

**Measured fact that corrects an old belief.** The GitHub web page and raw.githubusercontent return 404 for
these repositories because they are private and the request carries no credential — not because of robots.txt.
`gh api` reads them, and the discipline file fetched that way hashes identically to disk
(sha256 `ee2052c9a5b1a18c`). So the ceremony can verify against GitHub rather than merely trusting disk.

## 2. State, verified against the remotes at handover time

| repository | branch | head |
|---|---|---|
| altunelyusuf/Ontologies | main | `8ec6313f` |
| altunelyusuf/SEN0401 | main | `0054301` |
| altunelyusuf/AdvancedProgrammingWithPython | wip/template-9-15-0-ch06 | `bee81f5` |
| altunelyusuf/mastering-bitcoin | main | `ff2fa2d` |
| altunelyusuf/CME | main | `52468ed` |

All five checkouts were clean and zero behind their upstreams. SEN0414 is on a working branch, not main.

**Interactive pages.** SEN0401 chapters 1-5 at page 9.36.0 on template 9.32.0; SEN0414 chapters 1-5 at page
9.26.0 on template 9.25.0. Build with the newest data step and build script in each `08-tooling` and the
chapter's own `PAGE_VER`; both chains resolve their inputs by version rather than naming them.

**Decks.** Both courses have lecture decks for chapters 1-5, 1,006 slides in all, every shown output re-executed
and re-checked off the finished slides, speaker notes on every content slide.

**The textbook ontology moved.** Mastering Bitcoin, 3rd edition is no longer in the monorepo. It is
`altunelyusuf/mastering-bitcoin` (private), package under `3e/`, version 0.9.2, history preserved by subtree
split. SEN0401 pins it there; the per-chapter part version is resolved from the pinned tree, so a later release
of that package needs no edit in the course.

## 3. What is open, with what proves it

1. **SEN0414 is not on main.** Its work sits on `wip/template-9-15-0-ch06`. Decide whether to merge.
2. **SEN0401's repository manifest FAILs** — stowaways from sessions before this one. Run
   `python3 /home/claude/Ontologies/repo-tooling/verify_manifest_v1_1_0.py` against it to list them, then
   regenerate the manifest. Pre-existing, not caused by this session's work.
3. **The release tag `mastering-bitcoin-3e-v0.9.2` does not exist.** Tag pushes from a session are refused
   (HTTP 403, re-measured on a throwaway tag; note that `git push --dry-run` falsely reports success). The
   monorepo's `oe-tags.yml` workflow creates tags there, but `altunelyusuf/mastering-bitcoin` has no workflows at
   all, and the monorepo's variant would derive the slug `3e` and make the wrong tag. A workflow variant taking a
   package folder and a tag prefix is filed as a proposal in `Ontologies/oe-pack/07-handover-inbox/pending/`,
   proven in ten cases but never yet run on GitHub. **This is the recommended next step:** adopt it with
   `PKG_DIR: 3e` and `TAG_PREFIX: mastering-bitcoin-3e`, then confirm the tag lands at `349e3db`.
4. **Eight items wait in the monorepo's handover inbox**, two of them filed by this session: the oe-method tag
   wording and ceremony, and the workflow variant above. G39 says read the inbox before working.
5. **Chapter 1 of SEN0401 still has content gaps** from the adversarial audit (`/tmp` copy is gone; the report
   is committed in SEN0401 as `AUDIT_sen0401_ch01_page_v9_28_0.md` inside the delivered zip and was summarised
   in the session): 48 of 90 leaf concepts carry no worked example, 13 of them judged not worth one.
6. **The SEN0401 learning outcomes are a draft.** They were written from sourced evidence and carry no
   approval; the pages now say so. Registration under CME profile v1 still needs assessment, projects and
   outcome alignment, which needs the owner's approval first.
7. **Chapter 3 of SEN0401 misses the 200 ms main-thread budget** by 1-5 ms on an idle machine. Pre-existing and
   structural, measured at 204 ms before any of this work. Fixing it means restructuring the boot render in both
   templates.
8. **Not measured:** the start-up context split between system prompt, tool schemas, memory and attachments.
   The transcript records per-call totals only; an instrumented fresh session is needed.

## 4. How the owner works

Minimal output during development, files and code rather than commentary; continuous execution; decisions resting
on rules or provable facts, and a question only where they do not; human labels rather than internal identifiers;
and for the interactive pages, the standing interface rules recorded in the owner's own preferences — every term
explained, comprehensive cohesive paragraphs, one agent one slice, real running code, zoomable diagrams,
synchronised explorer and tabs, no third level of sub-tabs.
