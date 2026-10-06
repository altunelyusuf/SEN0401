# Chapter 1 deck and page assets - provenance and licences (v1.1.0)

Two sources. First, the owner's own 2025 lecture decks
(`03-materials/owner-legacy-2025/slides-2025/`), reused on his instruction of 2026-10-06. Second,
external free-licence material, fetched on 2026-10-06: Wikimedia Commons answers polite,
rate-limited requests from this container (HTTP 429 on bursts - wait and retry; the v1.0.0 claim
that image hosts are unreachable was wrong, a malformed first request), and the course textbook's
own public repository serves its figures raw. Every external file's licence REQUIRES the
attribution kept below and carried on the slide that shows it.

## From the owner's 2025 decks

| file | from deck | slide | shows |
|---|---|---|---|
| c1s18_circulation.png | Chapter_1_Introduction_v1_0_0.pptx | 18 | circuit-board Bitcoin artwork |
| c1s24_protocol.png | Chapter_1_Introduction_v1_0_0.pptx | 24 | gold coin on circuit traces |
| c1s32_nakamoto.jpg | Chapter_1_Introduction_v1_0_0.pptx | 32 | masked figure (the Satoshi anonymity visual) |
| c2s04_overview.png | Chapter_2_HowBitcoinWorks_v1_0_0.pptx | 4 | users-wallets-nodes-miners overview diagram |
| c2s07_fractions.jpg | Chapter_2_HowBitcoinWorks_v1_0_0.pptx | 7 | satoshi-to-bitcoin fraction table |
| c8s06_mesh.png | Chapter_8_TheBitcoinNetwork_v1_0_0.pptx | 6 | mesh network with flat topology |
| c8s32_miningnodes.png | Chapter_8_TheBitcoinNetwork_v1_0_0.pptx | 32 | floating blocks mining render |

## External, free-licence (attribution required, kept verbatim)

| file | source | licence | attribution |
|---|---|---|---|
| photo_rai_stone.jpg | Wikimedia Commons, "Yap Stone Money.jpg" | CC BY-SA 3.0 | photo: Eric Guinther |
| photo_pizza_margherita.jpg | Wikimedia Commons, "Eq it-na pizza-margherita sep2005 sml.jpg" | CC BY-SA 3.0 | photo: Valerio Capello (ElfQrin) |
| photo_cma_stater.jpg | Cleveland Museum of Art open access, Stater: Lion (2000.203, 600-550 BCE) | CC0 | Cleveland Museum of Art |
| photo_met_tablet.jpg | Wikimedia Commons, "Cuneiform tablet- administrative account concerning the distribution of barley and emmer MET DP297601.jpg" (The Met open access) | CC0 | The Metropolitan Museum of Art |
| photo_lydian_coins.jpg | Wikimedia Commons, "Lydian electrum Lion coins - Flickr - brewbooks.jpg" | CC BY-SA 2.0 | photo: brewbooks (Flickr) |
| mbc3_0101.png | github.com/bitcoinbook/bitcoinbook (the course textbook, 3rd ed.), images/ | CC BY-SA 4.0 (book); figure derived from Bitcoin Design Guide, CC-BY | Antonopoulos & Harding, Mastering Bitcoin 3e |
| mbc3_0102.png | github.com/bitcoinbook/bitcoinbook, images/ | CC BY-SA 4.0 (book); figure derived from Bitcoin Design Guide, CC-BY | Antonopoulos & Harding, Mastering Bitcoin 3e |

Reusing CC BY-SA material inside these course materials keeps the materials' own distribution of
those images under the same licence family; each slide that shows one carries its credit line.

## Self-made from live, verified data (2026-10-06)

| file | made from | note |
|---|---|---|
| genesis_hexdump.png | block 0's raw 285 bytes, fetched from blockstream.info/api in this build | double-SHA256 of the 80-byte header recomputed and matched against the genesis hash before rendering; the Times sentence highlighted |

Since deck v2.5.0 the value chart is a NATIVE PowerPoint chart (its data series live in the
chart object; deck_chart_logaxis_v1_0_0.py guarantees the logarithmic axis), so the earlier
rendered chart picture left the assets; the milestone data stays in the story companion.
