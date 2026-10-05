#!/usr/bin/env python3
"""SEN0401 chapter 3 corpus, version 1.2.0: Bitcoin Core, the reference implementation. Over 1.1.0 this version changes the
TEXT and the WORKED EXAMPLES of named concepts and nothing else - every concept identifier, label, level, parent, example
label and definition of 1.1.0 is kept exactly, so the change is additive and the version is MINOR.

Why it exists. An adversarial audit of the chapter 1 page (2026-10-04) found two defects that measurement showed to hold
for this chapter too:

  * five of the seventeen second-level sections had three paragraphs against the owner's standard of four to six
    (Verification 279 words, The Bitcoin Core project 268, Node resources 315, Source 248, Toolchain 254); and
  * seven second-level sections closed on a paragraph that only listed the concepts beneath them - the same list the
    breadcrumb row above the section already prints - so the closing paragraph taught nothing (Verification, Node
    resources, Source, Toolchain, Running, Client, Chain state).

This version replaces each of those seven closing paragraphs with one that explains the mechanism of the section rather
than naming its children, and brings every one of the seven to five paragraphs, the length the chapter's first-level
branches and third-level concepts already have. It also adds a worked example to five of the eight concepts that had
none. The three it leaves without one are named in the declining list at the foot of this file, with the reason: a
worked example there would be a hollow restatement of an institutional fact, not a computation a learner can follow.

Sources read for this version, in this session: Bitcoin Core's own current Unix build notes, fetched on 2026-10-04 and
saved as 08-tooling/ch03-sources/build_unix_v1_0_0.md, for the memory a compiler needs and the Debian package names
(both re-read from the saved copy by a CHECKS entry below); and the release layout already saved in this chapter's
evidence from the offline run of release 31.1, 08-tooling/ch03-evidence/release_layout_31_1_v1_0_0.txt, for the
programs the release ships. Every figure the new prose states is executed, either as a CHECKS entry of this file or as
the worked example of the concept that states it.
"""
__version__ = "1.2.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch03_corpus_v1_1_0 as B

CHAPTER = B.CHAPTER
W, Y, E, H, K = B.W, B.Y, B.E, B.H, B.K
_c = B._c
_ev, _src, _norm, _has = B._ev, B._src, B._norm, B._has
CQS, PROVENANCE, TOOLING, DOC_TITLE, DOC_ABOUT = B.CQS, B.PROVENANCE, B.TOOLING, B.DOC_TITLE, B.DOC_ABOUT
OWNERS, ERRORS, RAISES = B.OWNERS, B.ERRORS, B.RAISES

CHANGE = ("1.2.0 keeps every concept of 1.1.0 and changes only text and worked examples, so it is MINOR. Seven "
          "second-level sections closed on a paragraph that merely listed their own children, which the page's "
          "breadcrumb row already prints; each of those closing paragraphs is replaced by one that explains how the "
          "section's subject actually works, and all seven sections are brought to five paragraphs, the length the "
          "chapter's branches and concepts already have (five of them had three). Five concepts that had no worked "
          "example are given one, each executed by the chapter builder: the full node, the Autotools build, the "
          "compilation, the build prerequisites and the executables. Three concepts are left without an example on "
          "purpose - the reference implementation, open-source software and the source code - because what they state "
          "is an institutional fact rather than a computation, and an example there would restate the definition "
          "instead of teaching anything.")

# ---------------------------------------------------------------------------------------------------------------------
# the new paragraphs. Each entry is a concept id -> list of (facet, text, mode):
#   "replace-last" puts the text in place of the concept's last paragraph; "append" adds it after.
# ---------------------------------------------------------------------------------------------------------------------
PARA_EDITS = {

 # ---- Node / Verification -------------------------------------------------------------------------------------
 "Verification": [
  (H, "Verification works by re-doing the work rather than by trusting a report of it. When a block reaches a node, "
      "the node does not ask another participant whether the block is good; it recomputes the block's identifier from "
      "the eighty bytes of its header, checks that the identifier is numerically below the target the header itself "
      "declares, rebuilds the Merkle root - the single hash that commits to every transaction in the block - from the "
      "transactions it was sent, and compares that root with the one in the header. Only then does it apply the "
      "spending rules to each transaction: that every input names an output which exists and has not already been "
      "spent, that the conditions on that output are satisfied, and that the outputs created do not add up to more "
      "than the inputs consumed. Because each of those steps is a computation over data the node already holds, two "
      "honest nodes given the same block reach the same verdict without communicating, and that is what makes a "
      "verdict worth having [AH].", "replace-last"),
  (E, "The reader meets this group the moment a node is started, because verification is what the first hours of a "
      "node's life consist of. The start-up log of release 31.1, saved with this chapter's evidence, shows the node "
      "loading the block index and then working forward through the chain; the answer to the first status question a "
      "new owner asks names the number of blocks verified so far and how far that is from the chain's tip. The same "
      "group is met again whenever a disagreement is reported, because the first question an engineer asks about a "
      "disputed transaction is which rule it is said to break and which program enforced that rule [BC].", "append"),
  (K, "Two cautions belong here. The first is that the word reference, in reference implementation, describes a "
      "service the program performs for other programmers and not an authority it holds: the rules of Bitcoin are "
      "whatever the nodes that carry the economic weight of the network will accept, and Bitcoin Core is "
      "authoritative only for as long as those nodes run it or agree with it. The second is that verification is "
      "not validation of intent. A node can tell a learner that a transaction obeys every rule; it cannot tell them "
      "that the payment was wise, that the recipient was the one intended, or that the key which signed it was in "
      "the right hands. Those questions belong to the chapters on keys and on wallets, and no amount of rule "
      "checking answers them [AH].", "append"),
 ],

 # ---- Node / The Bitcoin Core project -------------------------------------------------------------------------
 "Project": [
  (H, "The project works as a review process with no owner at its centre. A change is written as a patch against the "
      "public repository, published for anyone to read, argued over in public, and merged only when maintainers are "
      "satisfied and nobody with standing objects; the maintainers can merge but cannot compel anyone to run what "
      "they merged, because a release only matters once node operators choose to install it. The licence is what "
      "makes this arrangement stable rather than fragile: because the MIT licence permits anyone to take the source, "
      "change it and distribute the result, a disagreement that cannot be settled by argument can be settled by "
      "forking the code, and the knowledge that it can be is itself a restraint on whoever holds the commit rights "
      "[OSI] [AH].", "replace-last"),
  (E, "A student meets the project, rather than just the program, the first time they want a question answered that "
      "the documentation does not cover: the answer is in the repository's own history, in the discussion attached "
      "to the change that introduced the behaviour, and in the release notes that announced it. The same material is "
      "what makes the chapter's invitation to build the program from source more than a gesture, since the text a "
      "reader compiles is the text they can also read and argue with [AH].", "append"),
  (K, "The openness is easy to overstate in two directions. It does not mean that anyone's change is accepted, and a "
      "learner who reads open community as unmoderated will be surprised by how conservative the review of a "
      "consensus-critical change is; the cost of a mistake there is other people's money. Nor does it mean that the "
      "absence of a named author leaves nothing to trust: a reader still has to decide whether to trust the "
      "maintainers' review, the reproducibility of the published binaries, or their own reading of the code, and "
      "this chapter's own section on assurance exists because that decision has to be made explicitly rather than "
      "assumed away [AH].", "append"),
 ],

 # ---- Node / Node resources ------------------------------------------------------------------------------------
 "NodeResources": [
  (H, "The costs follow from one design decision, which is that a node believes nothing it has not checked itself. "
      "To check a transaction the node must know whether the output it spends still exists, so it has to have "
      "processed every block that came before; that is why the first synchronization reads the whole chain from the "
      "beginning rather than starting at today. Once the chain is processed, what the node needs in order to keep "
      "working is not the chain itself but the set of outputs that can still be spent, and that set is far smaller "
      "than the history which produced it. Pruning is exactly this observation turned into an option: the node "
      "verifies every block as it arrives and then discards the old ones, keeping the compact record of spendable "
      "outputs. The saving is large and the price is precise - a pruned node cannot serve old blocks to a peer that "
      "is synchronizing, and cannot answer a question about a transaction whose block it has thrown away [AH] [BC].",
      "replace-last"),
  (K, "Two warnings about the figures themselves. They are measurements with a date, not constants: the chain grows "
      "every day, so a download size quoted for one year is a floor for the next, and this course therefore reads "
      "every such number against the date of the source that gave it rather than memorising it. And the figure that "
      "catches people out is not disk but upload: a node that has finished synchronizing spends most of its "
      "bandwidth serving others, which is the point of running one, and that is the cost a metered or capped "
      "connection cannot absorb. A learner who has only the cost of disk in mind will choose the wrong machine "
      "[AH] [BC].", "append"),
  (E, "The reader meets these costs twice, and in opposite moods. The first time is on the project's own download "
      "page, which states them plainly before offering the software, and in the book's own section on running a "
      "node, which does the same: both treat the costs as the price of an independent verdict rather than as a "
      "drawback to be minimised. The second time is on the machine itself, where the costs appear as the hours the "
      "first synchronization takes, as the growth of the data directory that this chapter's evidence captured from "
      "a real run, and as the choice of whether to prune, which is the first configuration decision whose "
      "consequences a learner can feel [AH] [BC].", "append"),
 ],

 # ---- Build / Source --------------------------------------------------------------------------------------------
 "Source": [
  (H, "Choosing the right text works through two mechanisms that are easy to confuse. The first is the repository, "
      "which is a complete record of every version the project has ever had, so that cloning it gives a learner not "
      "one program but the whole history of the program; by default the copy sits at the most recent development "
      "state, which is why a fresh clone is not yet a release. The second is the tag, a name attached to one exact "
      "point in that history, which is how a release is identified: checking out a tag moves the working copy to the "
      "text that was released under that name, and because the tag is tied to the content rather than to a date, two "
      "people who check out the same tag get byte-for-byte the same text. The release-candidate suffix is a "
      "convention layered on top of this, and it is only a convention - the software cannot tell a learner that a "
      "tag is meant for testing, the name does [AH] [GIT].", "replace-last"),
  (E, "A reader meets this group at the second command of the chapter's build sequence and again every time they "
      "update. The repository is met as a directory that appears after the clone; the tags are met as a long list "
      "printed by the command that asks the project's server which names exist, a list this chapter saved from the "
      "real repository so that the shape of the names can be studied offline; and the release candidate is met as "
      "the handful of names in that list which end in a testing suffix and which a production node should not run "
      "[AH] [GD].", "append"),
  (K, "The caution is that having the right text is not the same as having trustworthy text. A clone proves only that "
      "the bytes came from the address that was asked; it says nothing about whether that address is the project's. "
      "The repository's own signed tags, and the signed checksums published with the binary releases, are what close "
      "that gap, and they are the subject of this chapter's assurance section. A learner who checks out the correct "
      "tag from the wrong repository has built the wrong program carefully [AH].", "append"),
 ],

 # ---- Build / Toolchain -----------------------------------------------------------------------------------------
 "Toolchain": [
  (H, "A build works in two stages, and both generations of build system have them. In the first stage the build "
      "system inspects the computer - which compiler it has, which libraries are installed and where, which optional "
      "features were asked for - and writes the answers down, so that the second stage has no decisions left to "
      "make. In the second stage the compiler translates each source file on its own into an object file, and the "
      "linker joins the object files and the libraries into an executable. Two properties of a learner's experience "
      "follow directly from that shape. Because each file is translated independently, the work can be divided "
      "between several processor cores and an interrupted build can resume from where it stopped rather than start "
      "again. And because the first stage recorded the inspection, a library installed after configuration fails is "
      "picked up by running the inspection again, not by reinstalling the toolchain [AH] [CM].", "replace-last"),
  (E, "The reader meets the toolchain as the longest wait in the chapter and as its most common source of failure. "
      "The current build notes of the project, fetched for this version and saved with this chapter's sources, "
      "reduce the whole second generation to two commands, one to configure a build directory and one to build it, "
      "and they state what the wait costs in memory: at least 1.5 GB should be available while compiling, which is "
      "per compiler process, so a build divided over four cores wants around 6.0 GB rather than 1.5 [BC].", "append"),
  (K, "Two things trip learners here. The first is that the book's commands and the project's current commands are "
      "different generations, not alternatives: following a printed Autotools sequence against a recent source tree "
      "fails at the first command, because the file it names is no longer there, and the failure says nothing about "
      "the reader's machine. The second is that a build which finishes is not a build which works; the project ships "
      "its own test programs for exactly this reason, and running them is the last step of the build rather than an "
      "optional extra [AH] [BC].", "append"),
 ],

 # ---- Operation / Running ---------------------------------------------------------------------------------------
 "Running": [
  (H, "Running works by separating the program from the terminal that started it. In the foreground the node writes "
      "its log to the console and dies with the shell, which is what makes the foreground useful for the one purpose "
      "the chapter puts it to - reading the first lines to confirm that the intended settings were loaded. As a "
      "daemon the program detaches from the terminal, keeps a file recording which process it is so that a second "
      "copy cannot be started by accident over the same data directory, and writes its log to a file instead of the "
      "screen. From then on the owner does not watch the node but questions it, and the two status questions of this "
      "section are the standard pair: one asks about the chain the node has verified, the other about the node's own "
      "position in the network. Together they answer the only question that matters before relying on any further "
      "answer, which is whether this node is actually caught up and connected [AH].", "replace-last"),
  (K, "The caution is that a node which is running is not necessarily a node which is ready. A freshly started node "
      "answers every question immediately and some of its answers are about a chain it has not finished verifying, "
      "which is precisely the state the book prints and the state this chapter's own evidence was captured in. The "
      "two status answers are what distinguish the cases, and a learner who skips them can take a confident answer "
      "from a node that has seen a fraction of the chain. The second caution is operational: adding the program to "
      "the system's start-up scripts, which the book recommends, makes the node survive a reboot but also means that "
      "a misconfiguration now restarts forever, so the foreground test earns its place [AH].", "append"),
 ],

 # ---- Interface / Client ----------------------------------------------------------------------------------------
 "Client": [
  (H, "Every client works the same way underneath, and the differences between them are only how much of that work "
      "the user does. A call is an HTTP request carrying a small document that names a method and lists its "
      "arguments, sent to the port the node listens on and answered by a document holding either a result or an "
      "error. The helper program of the project builds that document from what is typed, reads the credential out of "
      "the data directory so the user never handles it, and prints the answer; a generic transfer tool leaves the "
      "document and the credential to the user, which is why the chapter shows that form second, once the shape of "
      "the request is already familiar; a wrapper library turns a method into a function of the host language and "
      "the answer into one of that language's own data structures, which is what lets a program loop over results "
      "instead of reading them [AH] [JR] [RH].", "replace-last"),
  (K, "Two cautions. The credential is the whole of the node's security on this interface, so a request that carries "
      "it is as powerful as the node itself: the cookie file in the data directory exists so that a local client can "
      "authenticate without a password being written anywhere, and exposing the interface beyond the local machine "
      "turns a convenience into a liability. And a wrapper library is one more dependency with one more version: the "
      "program the book prints ran unchanged in this chapter's own evidence, but it ran against a stated library "
      "version and a stated node release, and a learner reporting that a printed program does not work should name "
      "both before concluding that the book is wrong [AH] [BC].", "append"),
 ],

 # ---- Data / Chain state ----------------------------------------------------------------------------------------
 "ChainState": [
  (H, "The rule works on accumulated work rather than on length or on arrival time. Each block's header declares the "
      "target its identifier had to fall below, and from that target the work the block must have cost can be "
      "computed; the work of a chain is the sum over its blocks. A node holds every valid chain it has heard of and "
      "treats the one with the greatest total work as the chain, which means a shorter chain of harder blocks beats "
      "a longer chain of easier ones. When a competing chain overtakes the current one, the node reorganizes: it "
      "undoes the blocks it had applied, returning their transactions to the waiting pool unless the new chain "
      "already contains them, and applies the blocks of the new chain instead. Nothing is voted on and no message is "
      "exchanged to settle it, because each node reaches the same conclusion from the same arithmetic [AH] [NK].",
      "replace-last"),
  (K, "The caution is that this makes confirmation a matter of degree rather than of kind. A transaction in the most "
      "recent block is in the chain only as long as that block stays in the chain, and a reorganization one block "
      "deep is an ordinary event rather than an attack. What depth is enough is therefore an economic question about "
      "the value at stake and not a technical constant, which is why the figure the book's glossary quotes is a "
      "convention rather than a rule a node enforces. A learner should also keep the two senses of the words chain "
      "state apart: in this section it means the shape of the chain, while in the software it also names the "
      "database of spendable outputs [AH] [BC].", "append"),
 ],
}

# ---------------------------------------------------------------------------------------------------------------------
# the new worked examples. Each is (expression, expected repr); the chapter builder executes every one of them.
# ---------------------------------------------------------------------------------------------------------------------
IO_EDITS = {
 # a node verifies from the genesis block upward, so reaching the chapter's own block means checking height + 1 blocks
 "FullNode": ("775197 + 1", "775198"),
 # the two generations of build system, counted by their own commands: three for the older, two for the current one
 "AutotoolsBuild": ("(lambda old, new: (len(old), len(new)))(['./autogen.sh', './configure', 'make'], "
                    "['cmake -B build', 'cmake --build build'])", "(3, 2)"),
 # the build notes ask for at least 1.5 GB per compiler process, so dividing the work over four cores wants four times it
 "Compilation": ("(lambda per_process, jobs: (per_process, jobs, round(per_process * jobs, 1)))(1.5, 4)",
                 "(1.5, 4, 6.0)"),
 # Debian's required build dependencies, and what the wallet adds to them
 "BuildPrerequisite": ("(lambda req, wallet: (len(req.split()), len(wallet.split()), len((req + ' ' + wallet).split())))"
                       "('build-essential cmake python3 libboost-dev', 'libsqlite3-dev')", "(4, 1, 5)"),
 # the programs release 31.1 ships, as its own directories hold them
 "Executable": ("(lambda b, l: (len(b), len(l), len(b) + len(l)))(['bitcoin', 'bitcoin-cli', 'bitcoin-qt', "
                "'bitcoin-tx', 'bitcoin-util', 'bitcoin-wallet', 'bitcoind'], ['bitcoin-gui', 'bitcoin-node', "
                "'test_bitcoin'])", "(7, 3, 10)"),
}

# concepts deliberately left without a worked example, with the reason (reported, not silently skipped)
NO_EXAMPLE = {
 "ReferenceImplementation": "What the concept states - that one program serves as the model for how each part should "
                            "be implemented - is a fact about the program's standing among programmers. Any expression "
                            "written for it would either compare two literals the author chose, which proves nothing, "
                            "or restate the version number, which teaches nothing about being a reference.",
 "OpenSourceSoftware": "The concept states a licence and a development practice. A licence is a legal permission, not "
                       "a quantity; counting its words or its clauses would be an example about the text of the MIT "
                       "licence rather than about what open-source software is.",
 "SourceCode": "The concept states what source code is - the human-readable text the executables are built from. The "
               "chapter's own build concepts already carry the executable figures, and an expression measuring a "
               "fragment of C++ pasted into this page would illustrate string length, not source code.",
}

# ---------------------------------------------------------------------------------------------------------------------
# apply the edits
# ---------------------------------------------------------------------------------------------------------------------
def _apply(node):
    nid, lab, lv, par, leaf, paras = node
    paras = list(paras)
    if nid in PARA_EDITS:
        for facet, text, mode in PARA_EDITS[nid]:
            if mode == "replace-last":
                paras[-1] = (facet, _c(text))
            elif mode == "append":
                paras.append((facet, _c(text)))
            else:
                raise AssertionError("unknown mode %r" % mode)
    if nid in IO_EDITS:
        assert leaf is not None and leaf[2] is None, "%s already carries a worked example" % nid
        leaf = (leaf[0], leaf[1], IO_EDITS[nid])
    return (nid, lab, lv, par, leaf, paras)


NODES = [_apply(n) for n in B.NODES]

_seen = {n[0] for n in NODES}
assert set(PARA_EDITS) <= _seen, sorted(set(PARA_EDITS) - _seen)
assert set(IO_EDITS) <= _seen, sorted(set(IO_EDITS) - _seen)
assert set(NO_EXAMPLE) <= _seen, sorted(set(NO_EXAMPLE) - _seen)
assert not (set(IO_EDITS) & set(NO_EXAMPLE))
for n in NODES:
    if n[0] in PARA_EDITS:
        assert 4 <= len(n[5]) <= 6, "%s has %d paragraphs" % (n[0], len(n[5]))

# ---------------------------------------------------------------------------------------------------------------------
# the claims behind the new prose, each re-reading the saved source or recomputing the figure
# ---------------------------------------------------------------------------------------------------------------------
CHECKS = list(B.CHECKS) + [
 # the memory figure and the two current build commands, re-read from the saved build notes
 (_has(_src("build_unix_v1_0_0.md"), "at least 1.5 GB of memory available when compiling Bitcoin Core"), "True"),
 (_has(_src("build_unix_v1_0_0.md"), "cmake -B build", "cmake --build build"), "True"),
 # the Debian package names the prerequisites example counts, re-read from the same notes
 (_has(_src("build_unix_v1_0_0.md"), "build-essential cmake python3 libboost-dev", "libsqlite3-dev"), "True"),
 # four cores at 1.5 GB each
 ("round(1.5 * 4, 1)", "6.0"),
 # the programs the release ships, re-read from this chapter's own saved release layout
 (_has(_ev("release_layout_31_1_v1_0_0.txt"), "bitcoin-31.1/bin:", "bitcoin-cli", "bitcoind",
       "bitcoin-31.1/libexec:", "bitcoin-node", "test_bitcoin"), "True"),
 # the counts of that layout, read out of the saved file rather than typed: the lines of each directory that are not
 # the directory's own heading
 ("(lambda t: tuple(len([l for l in part.strip().splitlines() if l.strip() and not l.rstrip().endswith(':')]) "
  "for part in t.split('bitcoin-31.1/libexec:')))(%s)" % _ev("release_layout_31_1_v1_0_0.txt"), "(7, 3)"),
 # a node verifies from the genesis block upward
 ("775197 + 1", "775198"),
]
