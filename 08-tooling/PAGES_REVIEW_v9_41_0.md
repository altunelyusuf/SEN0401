# SEN0401 chapter pages 9.41.0 - the owner's review of 9.40.0 answered (templates 9.42.0-9.44.0)

The owner's review of 2026-10-07 14:46, in his words, measured on the 9.40.0 chapter 1 page (Maps > ERD,
1366x768), and what it became. Three template versions, one subject each.

| the review said | measured | what the page now does |
|---|---|---|
| "ERD, when filled the readability is reduced" | the sections view with mentioned-together on: 21 entities, 139 relationships on a fixed 4-column grid, every line from the midpoint of a box side, every label at the midpoint of its line: 469 overlapping label pairs, 68 labels drawn over an entity, 94 lines through an entity they do not join, the 990x1282 canvas fitted into a 716x444 room so the label text was 5 px | 9.42.0: the grid takes the room's shape (6 columns, text 8 px at fit, 15 px in the subjects view), lines leave a side at distinct points spread along it, labels are placed at the first of nine points along the line (and a step to either side) that is over no entity and no other label, a label with no free spot shrinks to its count; a mentioned-together label is its count (the dash carries the kind). Measured on the same view: 12 overlapping pairs (from 469), 7 over an entity (from 68), text 8 px; the subjects view 4 and 0 |
| "We need a relocate function to solve the over-display and label visibility problems" | nothing on the page could be moved | 9.42.0: every entity drags (pointer, mouse or touch; the lines and labels follow; the canvas regrows; a tap without movement still opens the card); Relocate - Untangle (swaps entities on the grid in short chunks until the weighted connection length and the lines crossing unrelated entities stop falling: 91 -> 68-77 crossing lines on chapter 1), Wider, Tighter, Reset layout; Labels - all / fitted / on choice; choosing an entity lifts its relationships and labels and dims the rest |
| "The same would be adapted to other diagrams as well" | the concept map, the neighbourhood map, the taxonomy, the ontology tree, the ontology graph and the class diagram each had their own renderer and none could be rearranged | 9.43.0: one renderer-independent relocate function, attached wherever zoomable() is: a node that carries an identifier drags, and every edge that names it (data-a/data-b, now on all six diagrams) is rewritten - lines by their ends, paths by the end that moved, count labels by the mean - and a tap stays a click. The concept map also gets Untangle (a local force layout from the current positions: boxes apart, long links shorter, no two boxes overlapping) and Reset |
| "use-case, sequence, activity, state and mindmap diagrams would be added to the paragraph depending on the content ... match the narrative with appropriate diagram types" | no paragraph carried a diagram of its narrative | 9.44.0: 31 authored diagrams across the five chapters (six or seven per chapter: activity, use-case, state, sequence, mind map, and one or two more of the type the content asked for), each under the paragraphs of the concepts it accompanies, headed by its type and title, with an (i) that opens a card naming the narrative pattern recognised, the question it answers, why the type follows, and the passage it was read from; drawn once per view, zoomable, relocatable. Every element label is checked against the explanations of its concepts (grounding 0.8 or better, measured per diagram) |
| "We need to add these mappings to our ontology as well so that it would be reused later" | no such mapping existed | CME 0.16.0 (commit e3a36ce, tag cme-v0.16.0): a narrative-to-diagram module of the standards-adoption ontology - `cme_standards_adoption_tbox_v1_1_0.ttl` (vocabulary), `cme_standards_adoption_v1_3_0.ttl` (ten narrative patterns - workflow, set of uses, life cycle, interaction, topic and its parts, hierarchy, structure, quantity over time, computation, web of ideas - each with the question it answers and its cue phrases, mapped to eleven diagram types with notation, elements and renderer) and three shapes in `cme_shacl_v1_1_0.ttl` refusing a diagram whose type is not what its pattern suggests (modules, not new files: the governance aggregate records CME at 24 A / 5 S / 20 T and growth is refused). The course reads the mapping (configuration 2.10.0 records the file digests and the CME commit), ASSIGNS each diagram's type from it (the author declares only the pattern), and writes each chapter's diagrams as `cme:NarrativeDiagram` individuals into a Turtle block of the page's corpus (`sen0401_chNN_diagrams_abox_v1_0_0.ttl`, beside the two CME files) - a block, not a file: the release path's dry-run refused five new A files against the course's recorded ceiling of 34 (BP-D54), so the block is composed by the data builder and embedded only |

## Verification (08-tooling/chNN-page/, PAGE_VER 9_41_0)
sen0401_page_test_v9_32_0.py: 276-307 recorded checks per chapter (features and widgets), 0 failures in all five;
it adds the filled ERD's overlap measures (chapter 1 sections view: 8 overlapping pairs and 0 over an entity of 139
labels; chapter 2: 0 and 0 of 70 shown), drag/tap/untangle/labels on the ERD (untangle: 78 -> 62 crossing lines on
chapter 1), drag/untangle/reset on the concept map (0 overlapping boxes after untangle), the mapping and the 31
diagrams (count, type by the mapping, element count, card, once per view) and the corpus blocks. Smoke 1.0.1 12/12
x5; book-corpus check 1.1.1 7/7 x4, chapter 5 6/7 (item 4, pre-existing agent-routing thread). The chapter 1 and 2
records were produced before one line was added to the test (restoring the focused concept after the diagram block,
no assertion changed); chapters 3-5 ran the final text. Materials 1.4.8, configuration 2.10.0 (the five test configs
list the new `standard` corpus kind), data 2.11.0, build 4.14.0.

## Found while building
- A diagram accompanying a section and its concepts appeared three times in one view (subject overview, section
  heading, concept); it is now drawn once, under the first visible of them (ndOnce), re-decided on every reveal.
- Duplicate SVG marker ids: a hidden copy of a diagram defined the arrowhead first and display:none markers do not
  render, so the visible copy had no arrowheads; every rendering now gets its own marker id.
- A force-directed layout with the usual repulsion threw the concept map's boxes to the canvas edges; the untangle
  that keeps the drawn shape uses only short-range repulsion, overlap pushes and springs on long links.
- CME's publisher was refused at the structure step until OEE recorded the `cme` U1 lines in the governance aggregate
  (at the published counts 24 A / 5 S / 20 T, not the requested 25 / 6 / 21: "a ceiling set at the next release's count is
  not a ceiling"); the three new files became modules of existing files and the release passed. A version bump of a
  file is a move to the publisher's named-deletion guard, not a deletion; the list is for files that really go.
