# Where every fact in SEN0401's course-level parts came from

Version: 1.0.0 · Recorded 2026-10-04

This file is the per-fact source record for the four course-level parts written on 2026-10-04:
`00-course-profile/sen0401_course_v1_2_0.ttl` (individuals; its two classes in
`sen0401_course_tbox_v1_0_0.ttl` since the BP-D53 split of 2026-10-05), `01-outcomes/sen0401_outcomes_v1_1_0.ttl`,
`02-textbook/sen0401_textbook_v1_2_0.ttl`, `03-materials/sen0401_materials_v1_4_2.ttl`,
`04-assessment/sen0401_assessment_v1_0_0.ttl`, `05-projects/sen0401_projects_v1_0_0.ttl` and
`06-quality/sen0401_quality_v1_1_0.ttl`. Superseded part versions leave the tree (BP-D7) and live in git history.
Everything below was read in the session that wrote those files; nothing is carried over from a
summary. Where a fact could not be sourced it is listed under **Not sourced** and left out of the
ontologies rather than guessed.

## The sources themselves

| Key | What it is | Read as |
|---|---|---|
| **README** | `README.md` of this repository | the course's own statement of instructor, lecture, textbook, theme and visibility |
| **CAT** | İstanbul Kültür University ECTS catalogue page for SEN0401, `https://akademikpaket.iku.edu.tr/EN/ects_bolum.php?m=1&p=11&f=4&r=0&ders_id=7084&ects=ders_detay` | fetched 2026-10-04, HTTP 200, 26 227 bytes, sha256 `bbc734f528d1c2ab9fa93ca68078894dac9a40b90fc3c2944cda3e09fe47e845` |
| **LEGACY** | `03-materials/owner-legacy-2025/` — `ATTRIBUTION_v1_0.md`, `legacy_inventory_v1_0_0.json` (144 files, written 2026-09-27T08:38:41), the twelve 2025 decks, the `llm-content-2025` tree | what the course has in fact covered |
| **CORPORA** | `08-tooling/sen0401_ch01_corpus_v1_2_0.py`, `ch02_corpus_v1_2_0`, `ch03_corpus_v1_1_0`, `ch04_corpus_v1_1_0`, `ch05_corpus_v1_0_0` | what the course in fact teaches, chapter by chapter |
| **PKG** | `03-materials/chNN/rdodi/*` and `03-materials/numbers/*` | the built chapter and dashboard packages |
| **MBB3E** | `/home/claude/Ontologies/mastering-bitcoin-3e` — `README.md`, `VERSION.txt` (0.9.0), `PUBLISH_RECORD.ttl`, `01-ontologies/` | the textbook ontology package |
| **LIN** | `07-lineage/sen0401_slides_lineage_v0_21_0.ttl` | the deck lineage's mission, its origin and its per-deck verification |
| **CME** | `cme_course_profile_v1_1_0.ttl`, `cme_standards_adoption_v1_1_0.ttl`, `cme_lifecycle_v1_0_0.ttl`, `cme_registry_v1_0_0.ttl`, `cme_registration_v1_0_0.ttl`, `cme_course_profile_shacl_v1_0_0.ttl` | which parts are required, which standard governs each, and how the claim is checked |
| **CASE** | `https://purl.imsglobal.org/spec/case/v1p0/context/imscasev1p0_context_v1p0.jsonld` | fetched 2026-10-04, sha256 `ed4e4ce92aac01ff84c610733583649b42be1d25688b0da18dda1aec34ffa3e9` |
| **LD** | `rdodi-ecosystem/07-pedagogy-professional-stage/01-vocabularies/learning_design_tbox_v1_0_0.ttl` | the six Bloom levels, `ld:Remember` to `ld:Create` |

## Course profile, fact by fact

| Fact | Value | Source |
|---|---|---|
| Course code | SEN0401 | README title, CAT |
| Course name | Special Topics in Software Engineering: Block Chain | README title |
| Alternate name | Special Topics in Software Engineering | CAT (the shell course's catalogue name) |
| Provider | İstanbul Kültür University, Faculty of Engineering and Architecture, Department of Computer Engineering | README ("Computer Engineering Department, İstanbul Kültür University"), CAT breadcrumb (faculty) |
| Instructor | Yusuf Altunel | README; CAT gives "Dr. Yusuf Altunel" |
| Instructor email | y.altunel@iku.edu.tr | README |
| Language | en | CAT, "Language of Instruction: English" |
| Lecture day, hours, room | Friday 09:00–12:45, LAB 2B-12/14 | README |
| Term | 2026-2027 Fall | CME, `cme:Act_SEN0401_Fall2026` (`cme:forTerm`) |
| Local credit notation | 2/0/2 | CAT, the LE/RC/LA column |
| Course type, ECTS | DE, 6 | CAT — recorded in the credit note only, because CME's ECTS adoption is `cme:Pending` and under it the credit field carries the figure *the owner* states; the owner states none here |
| Term theme | Semantic technologies — real users, domain engineering, collected requirements, team projects favoured | README, the "Term theme" line; the same theme appears as the mission origin in LIN |
| Visibility | public, student-readable, no student data | README; CME registry already records `cme:declaredVisibility "public"` and `cme:declaredWriter "altunelyusuf"` |
| Repository name | altunelyusuf/SEN0401 | CME lifecycle and registry. The git remote spells it lower case (`github.com/altunelyusuf/sen0401`); recorded in the ontology as a comment |
| Parts carried | course profile, outcomes, textbook, materials | the folder listing of this repository on 2026-10-04 |
| Parts missing | assessment, projects, quality | same listing: no `04-assessment`, no `05-projects`; `06-quality` holds only `games_strategy_risk_benefit_v1_0.md` |

### The catalogue describes a different topic — checked, not assumed

SEN0414's outcomes file records that the catalogue carried **no** outcomes for that course. For
SEN0401 the opposite was found. CAT carries a full entry, but for an earlier topic of this
special-topics course: course goals about software architectures, principal sources
(Taylor/Medvidovic/Dashofy 2009; Freeman *et al.* 2004; Gamma *et al.* 1994), a fourteen-week plan
pairing architecture lectures with a design pattern each week, an assessment scheme of
**midterm 40 / laboratory 20 / final 40**, a Saturday schedule (Theory 09:00–11:00 3B0305; Lab
11:00–13:00 and 13:00–15:00 2B-04/06), and five learning outcomes, all about software architecture
and design patterns. None of it describes the blockchain course being taught, so none of it is
carried into the ontologies. The divergence is recorded in the profile (schedule, topic note) so
the owner can decide whether to have the catalogue entry updated.

## Learning outcomes

Ten outcomes, LO-1 to LO-10, each with its own `dcterms:source`. Their evidence in short:

| Outcome | Bloom | Evidence |
|---|---|---|
| LO-1 what Bitcoin is | Understand | CORPORA ch01, PKG ch01, 2026 deck ch01, LEGACY deck 1 |
| LO-2 one payment traced end to end | Analyze | CORPORA ch02, PKG ch02, 2026 deck ch02, LEGACY deck 2 |
| LO-3 run and query Bitcoin Core | Apply | CORPORA ch03 (run of release 31.1, evidence in `08-tooling/ch03-evidence`), PKG ch03, 2026 deck ch03, LEGACY deck 3 |
| LO-4 derive keys and addresses | Apply | CORPORA ch04 (SEC 2, FIPS 180-4, BIPs 16/38/141/142/173/340/350, sipa/bech32), PKG ch04, 2026 deck ch04, LEGACY deck 4 |
| LO-5 wallet and recovery designs | Evaluate | CORPORA ch05 (BIP32/39/43/44/49/84/86/93/329/379/380/389, SLIP-0039/0044, Electrum, aezeed, Muun, BTCPay, Lopp), PKG ch05, LEGACY deck 5 and its wallet reports |
| LO-6 transactions, scripting, fees | Apply | LEGACY decks 6 and 7 and the `Chapter_6_Transactions` tree; the third edition's chapters 6–9 per LIN's mission. **No 2026 package exists for these chapters** |
| LO-7 network, blockchain, consensus | Analyze | LEGACY decks 8, 9 and 10 and the chapter 8 and 9 reports and ontologies; the third edition's chapters 10–12 per LIN's mission. **No 2026 package** |
| LO-8 security and second-layer applications | Evaluate | LEGACY decks 11 and 12; the third edition's chapters 13–14 per LIN's mission. **No 2026 package** |
| LO-9 Bitcoin's public figures | Analyze | PKG numbers (Blockchain.com snapshot) |
| LO-10 team project in the term theme | Create | README's term theme |

**They are approved.** The owner approved all ten as drafted, with their levels, on 2026-10-05 (`01-outcomes/sen0401_outcomes_v1_1_0.ttl` carries `cme:approvedBy` and `cme:approvedAt`; version 1.0.0, the draft, remains in git history). One alignment is asserted in `06-quality/sen0401_quality_v1_1_0.ttl`: the Project assesses LO-10. The Midterm and Final are not aligned: the outline does not say what they cover, so the gap stays declared.

CASE terms were verified before use: `dtCFDocument`, `dtCFItem`, `dtCFItemType`, `title`,
`humanCodingScheme`, `CFItemType` and `fullStatement` were each confirmed present in the fetched
CASE context. Bloom levels were read from LD, not reconstructed.

## Textbook

| Fact | Value | Source |
|---|---|---|
| Title, authors, publisher, date | *Mastering Bitcoin: Programming the Open Blockchain*, 3rd Edition; Andreas M. Antonopoulos and David A. Harding; O'Reilly; December 2023 | README |
| Licence and where it is free | CC BY-SA 4.0, from `github.com/bitcoinbook/bitcoinbook` | README; MBB3E README records the same statement at the commit it pinned |
| Upstream tag | `third_edition_print1` | README names the tag; its commit `6d1c26e1640ae32b28389d5ae4caf1214c2be7db` was resolved independently on 2026-10-04 with `git ls-remote --tags https://github.com/bitcoinbook/bitcoinbook` (the same tree is also tagged `third_edition_github`) |
| Chapter list, 14 chapters + 3 appendices + preface | Introduction; How Bitcoin Works; Bitcoin Core: The Reference Implementation; Keys and Addresses; Wallet Recovery; Transactions; Authorization and Authentication; Digital Signatures; Transaction Fees; The Bitcoin Network; The Blockchain; Mining and Consensus; Bitcoin Security; Second-Layer Applications | MBB3E `01-ontologies/mastering_bitcoin_3e_chNN_v1_1_0.ttl` part labels, read file by file |
| Why the decks are being renewed rather than relabelled | the third edition changed the second edition's chapter structure | LIN, mission origin and outcome rationale |
| Ontology package pin | repository `altunelyusuf/Ontologies`, folder `mastering-bitcoin-3e`, version 0.9.0, commit `7557bb81ae4f6ce9f71eeb87cbcbc1cc38732e75` | `git -C /home/claude/Ontologies log -1 --format=%H -- mastering-bitcoin-3e`, run 2026-10-04; that commit carries the monorepo tag `rdodi-ecosystem v1.142.0` (2026-09-28) |
| **No tag for the folder** | none exists | `git tag --list` in the Ontologies monorepo returns 668 tags, none matching `mastering`, `bitcoin` or `mbb`. SEN0414's textbook part could pin a tag as well as a commit; this one pins the commit only and says so |
| Package coverage figures | 315 sections, 449 concepts, 170 code listings, 79 figures, 65 BIPs, 78 glossary entries, 895 carried passages in all; 233 repository files registered | MBB3E README at 0.9.0 |
| Package publish state | version 0.9.0, ceremony 2026-09-26T22:48:32Z, 44/44 manifest files verified, 29/29 Turtle files parsed | MBB3E `VERSION.txt` and `PUBLISH_RECORD.ttl` |
| Source commit every passage is attributed to | `275c4eb8eab8800c6adc39f8def8e8f8fa356a57` | MBB3E chapter ontologies (`mbb:pinnedCommit`) and its README |

## Materials register

Every `cme:fileInPart` path was listed on disk on 2026-10-04 before being written, and re-checked
afterwards. The register holds: four renewed decks (chapters 1–4, 21/20/27/26 slides, counted from
the files); six RDODI documents; six ontology packages (research, TBox, ABox, shapes); six
interactive pages; twelve 2025 decks; and the 2025 content collection, represented by its inventory
and attribution file rather than by 144 separate entries. Per-deck verification sentences are quoted
from LIN. Three absences are registered as absences: chapter 5 has no deck, chapter 5 has no page
ABox, and the numbers page is still at 9.4.2 while the chapter pages are at 9.25.

## Not sourced — left out, for the owner to fill

- **ECTS credit as an owner statement.** The catalogue's 6 is recorded as read; CME's ECTS adoption is pending, so no owner figure is asserted.
- **Assessment weights for this term.** The catalogue's 40/20/40 belongs to its earlier topic. Nothing in this repository states this term's scheme.
- **Prerequisites and co-requisites.** The catalogue's fields are empty placeholder text.
- **A week-by-week syllabus for the blockchain topic.** The catalogue's fourteen weeks are the architecture topic's.
- **The project brief, its weight and its deliverables.** Only the one-sentence term theme exists.
- **ISBN and page count of the third edition.** Stated in neither the README, the textbook ontology package, nor the authors' repository as read here.
- **Course goals as the university prints them for this topic.** The catalogue's goals are the architecture topic's.
