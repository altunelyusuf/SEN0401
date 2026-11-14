#!/usr/bin/env python3
"""sen0401_ch11_stories_narrate v1.0.0 - owner's ruling of 2026-11-14 23:59: the story slides tell the story in human language with storytelling technique
(scene, turn, resolution), not as question-based single sentences. Rewrites the three story lines and the presenter note of the four chapter 11 story slides
(14, 25, 33, 38) from the facts already on those slides and in their sources; adds no new fact. Reads deck v2.2.0, writes v2.3.0."""
import os, re
from pptx import Presentation
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(R, "03-materials", "ch11")
src = os.path.join(D, "SEN0401_Ch11_TheBlockchain_3e_v2_2_0.pptx"); dst = os.path.join(D, "SEN0401_Ch11_TheBlockchain_3e_v2_3_0.pptx")
assert not os.path.exists(dst)
S = {
 14: ({1: "On 3 January 2009 Satoshi Nakamoto opened the chain with a line from The Times: Chancellor on brink of second bailout for banks.",
       2: "Quoting that day's paper pinned the block to a date, because it cannot be older, and it hints at why an independent money was wanted.",
       3: "Our chapter rebuilt the block from the constants in chainparams.cpp, hashed it to 000000000019d668, and found its 50 coins can never be spent."},
      "On 3 January 2009 a person using the name Satoshi Nakamoto switched on a new kind of money. At 18:15:05 UTC, timestamp 1231006505, the first block was stamped, and inside it sat a headline from The Times of that day: Chancellor on brink of second bailout for banks. Why quote a newspaper? A date written in a block proves the block is not older than that day, and the headline hints at why an independent money was wanted. Ask students what else could prove the age of a document, then compare their answers with this trick. Point to the source line so that they see the claim can be checked rather than believed."),
 25: ({1: "Ralph Merkle's hash tree dates from 1979; on 5 January 1982 the United States published patent 4,309,569, assigned to Stanford University.",
       2: "Its idea is small and strong: one short root vouches for a long list, which is how a block header covers every transaction.",
       3: "In block 277,315 the 40 transaction ids were hashed in pairs, six levels up, until a single root sat in the header."},
      "Picture the patent office on 5 January 1982. The United States publishes patent 4,309,569, Method of providing digital signatures, by Ralph Merkle, with the Board of Trustees of Stanford University as assignee; his hash tree dates from 1979. Decades later the same idea sits in every Bitcoin block, where one small root vouches for a long list of transactions. Ask students why a patent about digital signatures became the base of a block header, and let them find the answer: a header only has room for one hash. Then point to the source line, which names the patent number and the date, so that the story can be checked."),
 33: ({1: "On 4 May 2024 Jameson Lopp wrote that testnet3's easy-block rule let miners create hundreds of blocks in a single day.",
       2: "Free coins invite vandals, so Fabian Jahr's BIP 94 and testnet4 put rules against abuse into the chain itself.",
       3: None},
      "Imagine a sandpit where children come to practise, and then someone floods it. On 4 May 2024 Jameson Lopp published Griefing Bitcoin's Testnet and told how the testnet3 rule, easy blocks after twenty idle minutes, let miners create hundreds of blocks in a single day. A rule meant to keep a small chain moving had become an invitation to vandals, because test coins cost nothing. The answer was testnet4 with BIP 94, which writes rules against abuse into the chain itself. Ask students which other free systems face the same problem and how they could defend themselves."),
 38: ({1: "On 20 March 2019 Karl-Johan Alm and Anthony Towns wrote BIP 325: a signet block is valid only if it solves a challenge script.",
       2: "Instead of paying for blocks with work, a doorman signs them, and the test network stays calm.",
       3: None},
      "Think of a club with a doorman. In 2019, on 20 March, Karl-Johan Alm and Anthony Towns wrote BIP 325 for a test network where mining is replaced by a signature: a block is valid only if it solves a challenge script, so the creators decide who may make blocks. The test network stays calm because nobody can flood it. Ask students what is traded away when a trusted signer replaces mining, and let them reach the answer: open participation is given up for stability. Then show that the default challenge is a one-of-two multisig whose hash gives the four magic bytes 0a03cf40."),
}
def put(par, text):
    par.runs[0].text = text
    for r in par.runs[1:]: r._r.getparent().remove(r._r)
prs = Presentation(src)
for i, (lines, note) in S.items():
    s = prs.slides[i - 1]
    for k, t in lines.items():
        if t is None: continue
        sh = next(x for x in s.shapes if x.name == "Story Text %d" % k)
        put(sh.text_frame.paragraphs[0], t)
    assert 60 <= len(note.split()) <= 140, (i, len(note.split()))
    s.notes_slide.notes_text_frame.text = note
prs.save(dst); print(os.path.basename(dst))
