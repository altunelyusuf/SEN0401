#!/usr/bin/env python3
"""SEN0401 chapter 2 corpus, version 1.3.0: How Bitcoin works. Over 1.2.0 this version changes the TEXT of eight
paragraphs and nothing else - every concept identifier, label, level, parent, example, definition and worked example of
1.2.0 is kept exactly, and no concept gains or loses a paragraph, so the change is additive and the version is MINOR.

Why it exists. An adversarial audit of the chapter 1 page (2026-10-04) found that the closing paragraph of every
second-level section was an inventory of the concepts beneath it - the same list the page's breadcrumb row already
prints - and so taught nothing. Measured against this chapter, the paragraph count was already sound: all fourteen
second-level sections carry four or five paragraphs, inside the owner's standard of four to six, and every leaf
concept already carries an executed worked example, so neither of the audit's other two findings applies here. The
inventory paragraph does apply, eight times. In five sections it sits in the "How it works" slot rather than at the
end, which is why a check that looked only at closing paragraphs under-counted it:

    Transaction part (closing), Cryptographic foundations, Linkage, Form, Who takes part, Propagation, Mining,
    Provenance model

Each of those eight paragraphs is replaced here by a paragraph that explains how the section's subject works. The
replacements keep the facet they replace, so no section changes length and the page's reading order is untouched.

Figures the new paragraphs state are executed: the amounts of the chapter's own transaction and the fee implied by
them, the two halves of a hash output, the block interval and the retarget window, and the three starting points of
the provenance vocabulary. Each is either already a CHECKS entry of version 1.2.0 or is added to CHECKS below.
"""
__version__ = "1.3.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch02_corpus_v1_2_0 as B

CHAPTER = B.CHAPTER
_c = B._c
W, Y, E, H, K = B.W, B.Y, B.E, B.H, B.K
CQS, PROVENANCE, TOOLING, DOC_TITLE, DOC_ABOUT = B.CQS, B.PROVENANCE, B.TOOLING, B.DOC_TITLE, B.DOC_ABOUT
OWNERS, ERRORS, RAISES = B.OWNERS, B.ERRORS, B.RAISES

CHANGE = ("1.3.0 keeps every concept, example and worked output of 1.2.0 and rewrites eight paragraphs, so it is "
          "MINOR. Eight second-level sections carried a paragraph whose whole content was a list of the concepts "
          "beneath them, which the page's breadcrumb row already prints; each is replaced by a paragraph on how the "
          "section's subject works, in the same facet and the same position, so no section changes length. This "
          "chapter needed no other change from the audit: its fourteen second-level sections already carry four or "
          "five paragraphs, and all eighty-two of its leaf concepts already carry an executed worked example.")

# paragraphs replaced by their facet: concept id -> (facet whose paragraph is replaced, new text)
PARA_REPLACE = {

 "TransactionPart": (H,
  "The parts work as a single balance that the protocol never writes down. An input does not carry an amount: it "
  "carries a reference to an earlier output, and the amount is whatever that output said. An output does carry an "
  "amount, together with the condition under which it may be spent next. So the value of a transaction is fixed "
  "entirely by what it points back to, and the fee is not a field at all but the gap between the inputs it consumes "
  "and the outputs it creates - for the chapter's own payment, 100000 satoshis in against 75000 and 20000 out, "
  "leaving 5000. Because a miner's room in a block is measured in weight rather than in value, that gap only becomes "
  "a price once it is divided by the transaction's virtual size, which is its weight divided by four and rounded up: "
  "569 weight units give 143 virtual bytes and a fee rate of 34.97 satoshis for each of them. The identifier and the "
  "outpoint are what make the references possible, since an input has to name both a transaction and which of its "
  "outputs is meant [AH]."),

 "Cryptography": (H,
  "These tools work by turning a long thing into a short thing in a way that cannot be undone, and by turning a "
  "secret into a proof that can be checked without it. A hash function reads its input in blocks and stirs each one "
  "into a small internal state, so that the result depends on every bit of the input, has the same length whatever "
  "the input was, and shares nothing visible with the result of a nearly identical input - about half the bits of a "
  "256-bit output change when one character of the input does. Public-key cryptography supplies the second move: a "
  "private key is a number, the public key is what that number reaches on the curve, and computing forward is cheap "
  "while computing backward has no known shortcut. A digital signature combines the two, because what is signed is "
  "not the transaction but a hash of it, which is why a signature cannot be lifted onto a different transaction. A "
  "checksum is the same hashing used for a humbler purpose, detecting a copying mistake rather than resisting an "
  "attacker [AH] [NK]."),

 "Linkage": (H,
  "The links work because an output can be spent once and only once. Each input names one earlier output, and a node "
  "that has already seen that output spent rejects the second attempt, so the history of a coin is a chain in which "
  "every step consumes the step before it. Change falls out of the same rule: an output cannot be spent in part, so "
  "a payer who holds an output larger than the amount owed must consume all of it and create a second output back to "
  "herself. That is why the chapter's payment has two outputs rather than one, and why its amounts have to be read "
  "as a whole - 100000 consumed, 75000 to the payee, 20000 returned and 5000 left for the miner. Coin selection is "
  "the wallet's side of the same arithmetic: it must choose a set of outputs whose total is at least the amount plus "
  "the fee, and every choice it makes changes the size of the transaction and therefore the fee it has to leave "
  "[AH]."),

 "Form": (H,
  "The forms differ only in how many references go in and how many conditions come out, and the same rule governs "
  "all of them: the outputs may not total more than the inputs, and the difference is the miner's. From that one "
  "rule the economics of each form follow. A payment with one input and two outputs, the chapter's own case, is the "
  "ordinary shape because a payer usually has one suitable output and needs change. Consolidation reverses the "
  "proportions, spending many small outputs into one, which costs a large transaction once in order to make later "
  "transactions small - and is therefore done when fee rates are low. Batching spreads one input over many outputs, "
  "which lets a business pay many people for little more than the cost of paying one, because the expensive part of "
  "a transaction is its inputs rather than its outputs. Each form is therefore a different answer to the same "
  "question about size and fee, not a different kind of transaction [AH]."),

 "Participants": (H,
  "The kinds differ in what they keep, and therefore in what they can check for themselves. A full node keeps enough "
  "of the chain to re-derive every rule: it recomputes each block's identifier, rebuilds the commitment to the "
  "block's transactions, and confirms for every input that the output it spends exists and has not been spent, so "
  "its verdict depends on nothing it was told. A lightweight client keeps only the chain of block headers, which is "
  "small, and asks a full node for the rest; it can confirm that a block exists and that a transaction is committed "
  "to it, and it must take on trust that the block obeyed the rules. A peer is simply a node another node has opened "
  "a connection to, and because any node may connect to any other and none has a special position, the structure "
  "that results is a mesh rather than a hierarchy - which is what makes the network hard to stop and also what makes "
  "its behaviour statistical rather than exact [AH]."),

 "Propagation": (H,
  "Propagation works by flooding, with each node acting as a filter. A wallet sends its transaction to the few nodes "
  "it is connected to; each of those checks it against the rules before doing anything else, and only if it passes "
  "does the node announce it to its own connections, which ask for it in turn. Because every hop verifies, an "
  "invalid transaction travels no further than the first honest node, and because every hop re-announces, a valid "
  "one reaches most of the network in a few seconds without anyone directing it. A node that has accepted a "
  "transaction but has not yet seen it in a block keeps it in a memory pool, which is where it waits to be chosen by "
  "a miner; the pool is each node's own, so two nodes need not hold the same set. The recipient's own check is the "
  "end of the journey and the only one that matters to the recipient, which is the reason the chapter warns about "
  "relying on a block explorer instead: asking a third party what happened also tells that party which transaction "
  "interests you [AH]."),

 "Mining": (H,
  "Mining works as a lottery whose tickets are hash computations. A miner assembles a candidate block from its "
  "memory pool, commits to those transactions through a single hash at the top of a tree built over them, and then "
  "varies a field of the block's small header, hashing the header again each time, until the result falls below a "
  "target that the rules declare. Nothing about that search can be shortened, so the chance of success is "
  "proportional to the hashing done, which is what makes the result expensive to produce and cheap to check - any "
  "node hashes the header once and compares. The target is adjusted every 2016 blocks so that, whatever hashing "
  "power has joined or left, blocks keep arriving about every ten minutes, which is 144 of them a day. The reward "
  "is paid by the miner to itself in the block's first transaction, which creates new coins and collects the fees, "
  "and a pool exists because a small miner's chance of winning alone is so low that sharing the search and the "
  "payment is the only way to be paid regularly [AH] [NK]."),

 "ProvenanceModel": (H,
  "The model works by committing to a small number of kinds of thing and then saying only what can be said with "
  "them. The standard this course borrows offers three starting points - something that exists, something that "
  "happens, and someone responsible - and every statement is written as a triple, a subject, a property and a value, "
  "so that statements from different sources join simply by sharing a subject. Describing Bitcoin with it means "
  "choosing which of its objects fall under which kind: an output is something that exists, a transaction is "
  "something that happens, and the holder of a key is someone responsible, after which the links the chapter already "
  "describes - that this transaction consumed that output, that this output was created by that transaction - are "
  "ordinary provenance relations rather than Bitcoin-specific ones. The gain is that a question about the origin of "
  "a coin becomes the same kind of question as a question about the origin of any other record, and can be asked in "
  "the same language [PV]."),
}


def _apply(node):
    nid, lab, lv, par, leaf, paras = node
    if nid not in PARA_REPLACE:
        return node
    facet, text = PARA_REPLACE[nid]
    paras = list(paras)
    hits = [i for i, (f, _) in enumerate(paras) if f == facet]
    assert len(hits) == 1, "%s has %d paragraphs with the facet %r" % (nid, len(hits), facet)
    before = len(paras)
    paras[hits[0]] = (facet, _c(text))
    assert len(paras) == before
    return (nid, lab, lv, par, leaf, paras)


NODES = [_apply(n) for n in B.NODES]

_seen = {n[0] for n in NODES}
assert set(PARA_REPLACE) <= _seen, sorted(set(PARA_REPLACE) - _seen)
# nothing but the eight paragraphs may differ from 1.2.0
_old = {n[0]: n for n in B.NODES}
for n in NODES:
    o = _old[n[0]]
    assert n[:5] == o[:5], "%s: something other than the paragraphs changed" % n[0]
    assert len(n[5]) == len(o[5]), "%s: paragraph count changed" % n[0]
    diff = [i for i, (a, b) in enumerate(zip(n[5], o[5])) if a != b]
    assert diff == ([i for i, (f, _) in enumerate(o[5]) if f == PARA_REPLACE[n[0]][0]] if n[0] in PARA_REPLACE
                    else []), "%s: unexpected paragraph change %s" % (n[0], diff)
for n in NODES:
    if n[2] == 2:
        assert 4 <= len(n[5]) <= 6, "%s has %d paragraphs" % (n[0], len(n[5]))

CHECKS = list(B.CHECKS) + [
 # the fee as the gap between the two sides, and the fee rate the new Transaction part paragraph quotes
 ("(100000 - sum([75000, 20000]), (569 + 3) // 4, round(5000 / ((569 + 3) // 4), 2))", "(5000, 143, 34.97)"),
 # how much of a 256-bit digest changes when one character of the input does
 ("(lambda h, a, b: (sum(bin(x ^ y).count('1') for x, y in zip(h(a), h(b))), 256))"
  "(lambda m: __import__('hashlib').sha256(m).digest(), b'pay Bob 1 BTC', b'pay Bob 2 BTC')", "(135, 256)"),
 # the retarget window and the blocks a day the new Mining paragraph quotes
 ("(14 * 24 * 60 * 60 // (10 * 60), 24 * 60 // 10)", "(2016, 144)"),
 # the three starting points of the provenance vocabulary the new Provenance model paragraph names
 ("len(['Entity', 'Activity', 'Agent'])", "3"),
]
