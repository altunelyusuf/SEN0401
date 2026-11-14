#!/usr/bin/env python3
"""sen0401_ch11_page_stories_narrate v1.0.0 - owner's ruling of 2026-11-14 23:59: stories are told in human language with storytelling technique, not as reports.
Rewrites the 'story' text of the four chapter 11 stories on the page (and its page_data) in telling form from the facts the records already hold; adds no new fact.
Reads page v9.95.0 / page_data v9.95.0, writes v9.96.0 of each."""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(R, "03-materials", "ch11", "page", "sen0401_ch11_page_v9_95_0.html")
J = os.path.join(R, "08-tooling", "ch11-page", "page_data_v9_95_0.json")
NEW = {
 "The genesis block of Bitcoin has the timestamp 1231006505": (
  "Imagine the first minutes of a brand-new money. The genesis block of Bitcoin carries the timestamp 1231006505, which is 18:15:05 UTC on 3 January 2009, and its single coinbase transaction, written by Satoshi Nakamoto, holds 69 characters of free text: The Times 03/Jan/2009 Chancellor on brink of second bailout for banks. On that date the Chancellor of the Exchequer was Alistair Darling, who served under Gordon Brown from 2007 to 2010, and the newspaper itself began in 1785 as The Daily Universal Register. Why quote it? Because the text shows that the block cannot be older than that day, and the book adds that it was meant as a reminder of the need for an independent monetary system. In this chapter we rebuilt the block from the constants in chainparams.cpp and hashed it to 000000000019d668..., and found that its 50 coins are the first that can never be spent."),
 "Ralph Merkle patented the hash tree in 1979, and the United States patent 4309569": (
  "Go back to Stanford University in California. Ralph Merkle patented the hash tree in 1979, and the United States patent 4309569, Method of providing digital signatures, was published on 5 January 1982 with the Board of Trustees of Stanford University as assignee. The patent explains both the tree and how it handles many one-time signatures, and in 1980 Merkle wrote about tree authentication in his paper Protocols for Public Key Cryptosystems. Decades later Satoshi Nakamoto's paper hashes the transactions of a block in a Merkle tree and keeps only the root in the block header, so that one small value vouches for a whole list. We followed it in this chapter: the 40 transaction ids of block 277,315 were hashed in pairs up six levels and gave the root 5e049f40..., the value in its header, and a path of 4 hashes proved one transaction among 16."),
 "On 4 May 2024 Jameson Lopp published Griefing Bitcoin's Testnet": (
  "Picture a sandpit where anyone may practise, and then someone leaves the tap open. On 4 May 2024 Jameson Lopp published Griefing Bitcoin's Testnet, which describes how the testnet3 rule of minimum difficulty after 20 minutes lets miners create hundreds of blocks in a single day. The fix was testnet4: it had its genesis block on 3 May 2024 and BIP 94 was assigned to Fabian Jahr on 27 May 2024; it starts the retarget from the first block of the previous period and bounds the time of the first block of a period. Bitcoin Core 28.0 added the network with the option -testnet4. BIP 94 notes that three years' worth of blocks had been mined on testnet3 in a few weeks, and on 15 October 2026 testnet3 stood at height 5,189,394, against 156,618 on testnet4. Bitcoin Core 31.1 still starts testnet3 but says in its help that the support will be removed."),
 "BIP 325, Signet, was assigned on 20 March 2019": (
  "Think of a club with a doorman. BIP 325, Signet, was assigned on 20 March 2019 to Karl-Johan Alm and Anthony Towns: a test network in which a block is valid only if it carries a solution to a challenge script, so that its creators decide who may make blocks. Bitcoin Core 0.21.0 added the support, with one public signet maintained and personal signets possible with -signetchallenge. The challenge of the default signet is a 1-of-2 multisig of two keys, and its four message-start bytes, 0a03cf40, are the start of the double SHA-256 of that script. Its genesis block has the time 2020-09-01 00:00:00 UTC, and on 15 October 2026 its tip was at height 326,440, 2.27 times the 143,619 blocks of the book's listing. To see the other extreme, a signet that anyone could sign, with the challenge 51, ran on the test node of this chapter."),
}
def patch(t):
    for start, new in NEW.items():
        m = re.search(re.escape(start) + r'[^"]*(?:\\"[^"]*)*"', t)
        assert m, start
        t = t[:m.start()] + new + '"' + t[m.end():]
    return t
for p in (H, J):
    t = open(p, encoding="utf-8").read()
    n = patch(t).replace('"_version": "9.95.0"', '"_version": "9.96.0"')
    q = p.replace("9_95_0", "9_96_0"); assert not os.path.exists(q), q
    open(q, "w", encoding="utf-8").write(n); print(os.path.basename(q))
