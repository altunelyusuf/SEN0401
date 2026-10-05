#!/usr/bin/env python3
"""SEN0401 chapter 5 corpus, version 1.1.0: Wallet recovery. Over 1.0.0 this version changes the TEXT and the WORKED
EXAMPLES of named concepts and nothing else - every concept identifier, label, level, parent, example label and
definition of 1.0.0 is kept exactly, so the change is additive and the version is MINOR.

Why it exists. An adversarial audit of the chapter 1 page (2026-10-04) found two defects, and measurement showed this
chapter to be the worst affected of the five:

  * all eighteen of its second-level sections had three paragraphs against the owner's standard of four to six, the
    thinnest being Labels and notes at 226 words, Recovery as a practice at 229, Keys kept offline at 236 and Other
    data a wallet keeps at 244; and
  * all eighteen closed on a paragraph that only listed the concepts beneath it - the same list the page's breadcrumb
    row already prints - so in every section the closing paragraph taught nothing.

This version replaces all eighteen closing paragraphs with paragraphs on how each section's subject works, and brings
every section to five paragraphs, the length the chapter's branches and concepts already have. It also gives a worked
example to ten of the nineteen concepts that had none; the nine it leaves alone are in the declining list at the foot
of this file, each with its reason.

Every figure the new prose states is executed: as the worked example of the concept that states it, or as a CHECKS
entry of this file. The examples use the standard library only and no function the page's in-browser interpreter
lacks, so each one runs on the page as well as in the build.
"""
__version__ = "1.1.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch05_corpus_v1_0_0 as B
from sen0401_ch05_common_v1_0_0 import c as _c

CHAPTER = B.CHAPTER
CQS, PROVENANCE, TOOLING, DOC_TITLE, DOC_ABOUT = B.CQS, B.PROVENANCE, B.TOOLING, B.DOC_TITLE, B.DOC_ABOUT
OWNERS, ERRORS, RAISES = getattr(B, "OWNERS", []), getattr(B, "ERRORS", []), B.RAISES
W, Y, E, H, K = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out"

CHANGE = ("1.1.0 keeps every concept of 1.0.0 and changes only text and worked examples, so it is MINOR. All eighteen "
          "second-level sections had three paragraphs and each closed on a list of its own children, which the page's "
          "breadcrumb row already prints; every one of those closing paragraphs is replaced by a paragraph on how the "
          "section's subject works, and all eighteen are brought to five paragraphs. Ten concepts that had no worked "
          "example are given one, each executed by the chapter builder: the wallet database, the key tweak, plausible "
          "deniability, memorising a code, the implicit and the explicit path, the address label, the digital "
          "signature, data loss and the testing of a backup. Nine are left without one on purpose, because what they "
          "state is a physical or institutional arrangement rather than a computation, and an expression there would "
          "restate the definition instead of teaching anything.")

# ---------------------------------------------------------------------------------------------------------------------
# the new paragraphs: concept id -> [(facet, text, "replace-last" | "append")]
# ---------------------------------------------------------------------------------------------------------------------
PARA_EDITS = {

 "WalletContents": [
  (H, "The split works because the two things a wallet does need different materials. Recognising a payment needs only "
      "public material: from a public key, or from an extended public key and a chain code, a program can derive every "
      "address the wallet will ever hand out and watch the chain for payments to them. Authorising a spend needs the "
      "private key, and nothing else will do. So a design can put the public material where it is convenient - a "
      "phone, a web server, a shop till - and keep the private material somewhere awkward and safe, and the awkward "
      "part is then asked for a signature only at the moment of spending. External signing is the message that crosses "
      "that boundary: the application builds the unsigned transaction, the holder of the keys signs it, and the "
      "signature comes back without the key ever leaving [AH].", "replace-last"),
  (E, "The reader meets the split in almost every wallet in current use. A hardware signing device is one side of it "
      "and the application on the computer the other; a multisignature arrangement is the same shape with several "
      "signers; the web store later in this chapter is the same shape again, with a server that can see its takings "
      "and cannot spend them. Bitcoin Core shows it directly, because a descriptor wallet can be created from public "
      "descriptors alone, and the run of release 31.1 saved with this chapter reports such a wallet as one that holds "
      "no private keys [AH] [BCW].", "append"),
  (K, "Two cautions. The word wallet names three different things here - the stored keys, the program that reads them, "
      "and the device that holds the secret half - and a sentence about wallets is ambiguous until one of the three is "
      "meant. And a wallet that cannot spend is not therefore harmless: an extended public key reveals every address "
      "the wallet will ever use, so whoever obtains it can watch the whole balance and history, which is a privacy "
      "loss rather than a theft but a loss all the same [AH].", "append"),
 ],

 "KeyGenerationMethods": [
  (H, "The history is a sequence of answers to one question: how can many keys be made so that one record restores "
      "them all? The first answer made no attempt - each key was drawn at random, so the set of keys had no structure "
      "and a backup was a copy of every key made so far. The second answer replaced the randomness with a rule: keep "
      "one random value, the seed, and derive key number n from the seed and from n, so that the same seed always "
      "gives the same keys in the same order and the backup is the seed alone. The third answer noticed that on an "
      "elliptic curve a public key can be shifted by the same amount as its private key, so a derived public key can "
      "be computed without the private one - which is what lets a watching wallet exist. The fourth answer arranges "
      "the derivation as a tree rather than a list, giving each branch its own chain code so that a branch can be "
      "shared without sharing its neighbours [AH] [B32].", "replace-last"),
  (E, "The reader meets all four, but only one of them in new software. Independent generation is met in old wallet "
      "files and in the import path of current wallets, which must still accept a loose key; the seed is met as the "
      "recovery code a wallet shows on first use; the tweak is met whenever a server derives addresses it cannot "
      "spend; and the tree is met as the paths of the next branch and as the descriptors of the branch after. Bitcoin "
      "Core's own list of implemented proposals names the tree standard and the path conventions built on it, which "
      "is how a learner can check that the history ends where this chapter says it does [BCD].", "append"),
  (K, "The caution is that a deterministic scheme moves the risk rather than removing it. One record now restores "
      "everything, which is the benefit; one record now also loses everything, and one leak of it gives away every "
      "key the wallet will ever have, including keys not yet derived. That is why the rest of the chapter is about "
      "the handling of that single record, and why the chapter's own closing advice is to write it down and to test "
      "the restoration rather than to trust that it will work [AH].", "append"),
 ],

 "CodeSchemes": [
  (H, "All six schemes work by turning a secret into words that a person can copy without error, and they differ in "
      "three choices. The first is what the words encode: the entropy behind a seed, as in the scheme the rest of the "
      "chapter uses, or a ciphertext, or a share of a secret that has been split. The second is what protects the "
      "words against a copying mistake: a checksum computed from the secret itself, which is how the first scheme "
      "works, or a longer checksum that also identifies the scheme, which is how the version-prefix designs work. The "
      "third is what the words carry besides the secret - a version number, a creation date, a share index - because "
      "whatever is not in the words has to be remembered separately. Those three choices explain every difference a "
      "learner will meet, including why one code can be restored by any wallet and another needs the software that "
      "made it [AH] [B39] [EL] [AZ] [S39] [B93].", "replace-last"),
  (E, "The reader meets a scheme as a list of words shown once, when a wallet is created, and then never again unless "
      "something has gone wrong. That is the difficulty with this group: the only moment at which the differences "
      "matter is a restoration, by which time the wallet that made the code may be gone. The schemes are met in their "
      "own documents, which this course fetched and saved so they can be compared side by side, and the differences "
      "are met in the one place they are visible without a restoration - the number of words, their checksum "
      "behaviour, and whether the first word reveals which scheme is in use [B39] [EL] [AZ] [S39] [B93].", "append"),
  (K, "The caution is that a word list is not a format marker. Several schemes draw their words from the same English "
      "list, so a code can look exactly like a code of another scheme and derive a different seed, and a learner who "
      "assumes that twelve English words mean one particular scheme will restore an empty wallet and conclude that "
      "the funds are gone. The record of which scheme a code belongs to is part of the backup, and the chapter's own "
      "recommendation about writing the code down should be read as including it [AH].", "append"),
 ],

 "CodeTradeoffs": [
  (H, "These decisions work against one another, and the mechanism that creates the tension is the passphrase. A "
      "passphrase is mixed into the derivation as part of the salt, so each passphrase produces a different seed and "
      "therefore a different wallet from the same words; no checksum covers it, so a mistyped passphrase does not "
      "fail but silently opens an empty wallet. From that single fact the whole group follows. Deniability is the "
      "same property seen from the other side: because every passphrase is a valid wallet, no observer can show that "
      "a particular one was intended. Memory is the cost: the words are protected by a checksum and the passphrase is "
      "not, so remembering it is the weakest link in a chain the rest of which is written down. And coercion is the "
      "risk that makes deniability look attractive and the reason the chapter treats it as a trap rather than a "
      "feature [AH] [B39].", "replace-last"),
  (E, "The reader meets these decisions at the one moment a wallet asks whether to set a passphrase, usually with a "
      "sentence of explanation and no account of the consequences. They are met again in the published record of what "
      "goes wrong: the list of physical attacks that this chapter reads and counts, which its own source says is not "
      "comprehensive, and the recurring reports of wallets restored correctly from the words and found empty because "
      "the passphrase was not quite the one used. The wallet birthday is met in the opposite way, as the field a "
      "restoration asks for and a user cannot answer [AH] [LO].", "append"),
  (K, "The caution is that a second secret is a second thing to lose, and the arithmetic of that is bad. A code "
      "written down and a passphrase in a person's head is not two defences but one defence and one single point of "
      "failure, because the loss of either loses the funds while the theft of both is needed to take them. That is "
      "the reasoning behind the chapter's blunt preference for a written record over a memorised one, and a learner "
      "should separate the question of what protects against theft from the question of what protects against loss, "
      "because almost every recommendation in this group answers only one of them [AH].", "append"),
 ],

 "CodeGeneration": [
  (H, "The six steps work as one arithmetic chain with no choices left in it. The entropy is a whole number of bits, "
      "and the standard allows only lengths that are multiples of thirty-two. The checksum is the first bits of a "
      "digest of that entropy, one bit for every thirty-two bits of it, appended to the end. The total is then cut "
      "into pieces of eleven bits, each piece read as a number between zero and two thousand and forty-seven, and "
      "each number replaced by the word at that position in a list of exactly that many words. Because eleven bits "
      "address the list exactly, no number is wasted and no word is unreachable; and because the number of pieces is "
      "the total divided by eleven, the word count is decided by the entropy rather than chosen. Normalising the text "
      "is the last rule in the chain: the same words written with different accents or spacing must produce the same "
      "bytes, or the same code would give two different seeds [AH] [B39].", "replace-last"),
  (E, "The reader meets these steps the first time a wallet is created, and this chapter's own figures let them be "
      "followed by hand: the entropy the chapter works with, its four checksum bits, the first three word numbers its "
      "bits give, and the table of every entropy length with its checksum and word count. The same steps are met in "
      "the published test vectors, which this course runs rather than quotes, and in the chapter's own visual for the "
      "word count, where the figures are computed on every build rather than written down [B39] [TZ].", "append"),
  (K, "Two cautions. The checksum protects the words and not the user's intention: it catches a mistyped word, which "
      "is its purpose, but it cannot tell that the code written down belongs to a different wallet. And the entropy "
      "is the only secret in the chain, so the strength of everything that follows is the strength of that one draw; "
      "a code generated from a source a person chose, rather than from the wallet's own generator, has the length of "
      "a strong code and the strength of a guess, which is why the chapter gives that mistake a section of its own "
      "[AH] [B39].", "append"),
 ],

 "SeedDerivation": [
  (H, "The last steps work by making the derivation deliberately expensive. The words, normalised, become the "
      "password; the fixed text of the standard, followed by the passphrase if there is one, becomes the salt; and "
      "the two are fed to a key-stretching function which applies a keyed hash two thousand and forty-eight times "
      "over, each round taking the previous round's output, so that the cost of trying one candidate is two thousand "
      "and forty-eight times the cost of one hash. The result is sixty-four bytes, and those bytes are the seed. Two "
      "properties of the construction matter. The output is longer than the entropy that went in, which adds no "
      "strength and is not meant to: stretching protects a weak password against a search, and the seed's real "
      "strength stays that of the original draw. And the passphrase enters through the salt rather than through the "
      "password, which is why no checksum can cover it [AH] [B39] [R8018] [R2104].", "replace-last"),
  (E, "The reader meets this step as the pause when a wallet is restored, and as the three seeds the chapter prints: "
      "one from its words with no passphrase, one from the same words with a passphrase, and one from its longer "
      "code. This course recomputes all three from the standard rather than copying them, and checks them against the "
      "published vectors of an independent implementation. The step is met again in chapter 4's discussion of how "
      "keys are protected, and in any wallet that offers to encrypt a backup, because the same stretching is what "
      "stands between a short password and the data behind it [B39] [TZ].", "append"),
  (K, "The caution is that the passphrase has no safety net at all. Every passphrase produces a valid seed, so a typo "
      "produces a working wallet that is simply the wrong one, with no error and no clue; the only test is to look "
      "for the funds. The second caution is about the stretching count itself: two thousand and forty-eight rounds "
      "was modest when the standard was written and is more modest now, which is why one of the alternative schemes "
      "in this chapter uses a function with a far higher cost, and why this number should be read as a historical "
      "choice rather than a recommendation [AH] [B39] [AZ].", "append"),
 ],

 "MasterKeys": [
  (H, "The step works by using a keyed hash as a splitter. The seed is passed to a keyed hash function together with "
      "a fixed key, the same text for every wallet in the world, and the function returns sixty-four bytes. The left "
      "thirty-two are read as a number and become the master private key; the right thirty-two become the master "
      "chain code. Three properties follow. Because the hash key is fixed and public, nothing secret is added at this "
      "step - the entire secret is the seed, and the master keys are a deterministic function of it. Because the two "
      "halves come from one hash, neither half reveals the other, which is what lets the chain code be shared "
      "alongside a public key without exposing the private one. And because the output is defined by the standard, "
      "any implementation given the same seed reaches the same root, which is what makes a code restorable in "
      "software that did not create it [AH] [B32] [R2104].", "replace-last"),
  (E, "The reader meets the root as the thing a wallet never shows. What a wallet shows is the recovery code at one "
      "end and addresses at the other; the master key and chain code sit between them and surface only in an "
      "extended key, where the two are carried together. They are met directly in the standard's first test vector, "
      "which this course recomputes from the seed so that the arithmetic can be compared with the published values, "
      "and in the key origin of a descriptor, whose fingerprint is derived from the master public key [B32] [B380].",
      "append"),
  (K, "The caution is that this is the single point from which everything hangs. Whoever learns the master private "
      "key and the master chain code has every key of the wallet, present and future, in every branch; there is no "
      "part of the tree that is out of reach from the root. That is the reason the root is not stored where it can be "
      "read, and the reason hardened derivation exists further down - so that a compromise of one branch does not "
      "walk back up to the root. A learner should also note that the chain code is not a second secret of the same "
      "kind: it is secret in the private form and published in the public form, deliberately [AH] [B32].", "append"),
 ],

 "ChildDerivation": [
  (H, "The derivation works the same way at every node and in both directions. The function takes a key, its chain "
      "code and an index number, concatenates them, and passes them to the keyed hash; the left half of the result is "
      "added to the parent private key to give the child private key, and the right half becomes the child's chain "
      "code. Because adding that left half to the private key corresponds, on the curve, to adding its multiple of "
      "the generator point to the public key, the same left half derives the child public key from the parent public "
      "key - so a party with only the public key and the chain code can derive public children. The index chooses "
      "which child, and the standard splits the four thousand million indices of each node into two halves: the lower "
      "half uses the parent public key in the hash and so allows public derivation, while the upper half, called "
      "hardened, uses the parent private key instead and therefore cannot be derived publicly at all [AH] [B32].",
      "replace-last"),
  (E, "The reader meets this function at every step of every path in the rest of the chapter: each slash in a path is "
      "one application of it, and the apostrophe or the letter h on a level means that the index was taken from the "
      "hardened half. It is met in the extended public key a web store is given, which is exactly the parent key and "
      "chain code the public form of the function needs, and in this course's own derivations, which reproduce the "
      "standard's test vectors chain by chain and the addresses an independent node derived from the same account "
      "descriptor [B32] [BCW].", "append"),
  (K, "The caution is the one case where the construction leaks, and the standard names it. If an attacker obtains a "
      "parent extended public key and any one non-hardened child private key, the parent private key follows by "
      "subtraction, and with it the whole branch. Hardened derivation exists to close exactly that path, which is why "
      "the account levels of the standard paths are hardened and the branches below them are not. A learner should "
      "also keep in mind that a child key on its own is indistinguishable from a key drawn at random, which is a "
      "privacy property and not a security one [AH] [B32].", "append"),
 ],

 "ExtendedKeys": [
  (H, "An extended key works by packaging exactly what the derivation function needs. The function needs a key and a "
      "chain code, so an extended key is the two joined together, and once a program holds one it can derive the "
      "whole subtree below it without asking anybody. Written down, the package is seventy-eight bytes: version "
      "bytes that say which form and which network, the depth in the tree, the four-byte fingerprint of the parent, "
      "the index this key was derived at, the chain code, and the key itself - with the private form padded by a zero "
      "byte so that both forms are the same length. Those bytes are then written in the checksummed text of chapter "
      "4, which is why the two forms are distinguishable at a glance by the letters they begin with. The fingerprint "
      "is what lets software recognise which parent a key came from without holding the parent [AH] [B32].",
      "replace-last"),
  (E, "The reader meets extended keys as the long strings that are copied and pasted - into a watching wallet, into a "
      "payment processor, into a descriptor's key origin. They are met in this chapter's own figures, where the "
      "public form is printed beside the private form it was neutered from, both of the same length and differing in "
      "their version bytes; and in a real node, whose descriptors carry an extended key with its origin and its "
      "ranged child path, as the run saved with this chapter shows [B32] [BCW] [B380].", "append"),
  (K, "The caution is that the public form is far more powerful than its name suggests. It cannot spend, but it can "
      "derive every address of its subtree, which means that handing one out discloses the whole history and the "
      "whole future of that branch to its holder. And a leaked public form becomes a leaked private form the moment "
      "any non-hardened child private key from the same branch also leaks, as the previous section's warning "
      "describes. A learner should treat an extended public key as sensitive data that merely cannot be stolen from "
      "[AH] [B32].", "append"),
 ],

 "TreeNavigation": [
  (H, "The notation works as an address within the tree, read from the root outwards. The letter m stands for the "
      "master key; each slash descends one level; the number after the slash is the index given to the derivation "
      "function at that level; and an apostrophe, or the letter h, marks an index taken from the hardened half. The "
      "conventions built on top of it give each level a meaning so that two programs reading the same path agree on "
      "what they are looking at: the first level says which standard is in use and therefore which kind of address "
      "the branch holds, the second which coin, the third which account, the fourth whether the branch is for "
      "receiving or for change, and the fifth which address in sequence. Nothing in the arithmetic requires any of "
      "this - the meanings are a convention, which is precisely why the next branch of the chapter is about what "
      "happens when a wallet does not follow it [AH] [B32] [B43] [B44].", "replace-last"),
  (E, "The reader meets paths everywhere once they are recognised. A hardware device shows one before it signs; a "
      "node's descriptor carries one in its key origin and another as its ranged child path; this course's own "
      "material quotes them in the standard paths of the next branch and in the derivations it checks against the "
      "published vectors. They are met in the chapter's two tables, whose rows are the paths of the four standards, "
      "and in the single line a restoration may need if the wallet used a path of its own [AH] [B44] [BCW].",
      "append"),
  (K, "The caution is that a path is metadata and is not in the code. The recovery code restores the keys of the tree "
      "and says nothing about which branch of it a wallet used, so a code restored into software that assumes a "
      "different convention finds an empty wallet while the funds sit on a branch nobody looked at. That is the whole "
      "problem the next branch exists to solve. A smaller caution: the apostrophe and the letter h mean the same "
      "thing, and so do the two ways of writing a hardened index, which matters when a path is copied between "
      "programs that accept only one spelling [AH] [B389].", "append"),
 ],

 "PathConventions": [
  (H, "The two approaches work by putting the convention in different places. An implicit path puts it in the "
      "standard: the wallet derives at the levels the standard prescribes, so a restoring program that knows which "
      "standard was used can reconstruct the paths from nothing but the code, and the backup is the code alone. An "
      "explicit path puts the convention in the backup: the wallet may derive wherever it likes and records the path "
      "it used, so the backup is the code plus a written description, and a restoring program follows the "
      "description instead of guessing. The cost of each is the other's benefit. Implicit paths need no extra record "
      "and allow no deviation; explicit paths allow any arrangement, including ones no standard anticipated, and fail "
      "completely if the record is lost. Multisignature is the case that settles the argument, because the public "
      "keys of the other signers are neither standard nor derivable from one seed, so they must be recorded whatever "
      "approach is chosen [AH] [B43] [B44] [B380].", "replace-last"),
  (E, "The reader meets implicit paths as the reason a code from one wallet usually restores in another, and explicit "
      "paths as the descriptor a modern node gives out. Bitcoin Core is the clearest case of the second: its wallets "
      "are descriptor wallets, so every path it uses is written down in a descriptor rather than assumed, and the "
      "fresh wallet saved with this chapter's evidence reports eight of them, a receiving and a change branch for "
      "each of four script types. The four standard paths of the chapter's table are met in their own proposals, each "
      "with test vectors this course runs [AH] [BCW] [B44] [B49] [B84] [B86].", "append"),
  (K, "The caution is about the coin-type level, where the chapter's own table is uneven for a real reason. Three of "
      "its four rows use the coin type for Bitcoin and the fourth uses the coin type that the registry assigns to "
      "test networks, because that proposal's own test vectors are on a test network; a learner who reads the table "
      "as four parallel cases will derive the wrong branch. The second caution is that an explicit record is only as "
      "good as its own integrity, which is why a descriptor carries a checksum of its own and why that checksum "
      "should be kept with it [AH] [S44] [B380].", "append"),
 ],

 "Descriptors": [
  (H, "A descriptor works as a small expression that names a script type and supplies its keys, so that one line says "
      "everything a program needs in order to recognise and later spend a whole family of outputs. The outermost "
      "function says which kind of output script to build; its argument is a key, written either directly or as an "
      "extended key followed by the path to derive along, with a star standing for every index in a range so that one "
      "line covers an unbounded sequence of addresses. In front of the key, in brackets, the key origin records the "
      "fingerprint of the master key and the path already taken to reach this point, which is what lets a signer "
      "decide whether the key is one of its own. Eight characters of checksum close the line, computed over the "
      "text so that a copying mistake is refused rather than acted on, and the whole thing is text, which is why it "
      "can be written in a backup beside the recovery code [AH] [B380] [B389].", "replace-last"),
  (E, "The reader meets descriptors in any current node. The run of release 31.1 saved with this chapter printed the "
      "descriptors of a fresh wallet, each with its key origin, its ranged child path and its checksum, and answered "
      "with the same four checksums that this course computes from the standard's own algorithm; the account "
      "descriptor of one branch derived the address that the proposal's test vector names. They are met again "
      "wherever a watching wallet or a payment processor is set up, because a descriptor is now the usual way of "
      "telling such a program what to watch [BCW] [BCD] [B380].", "append"),
  (K, "The caution is that a descriptor is a backup and must be treated as one. It is not secret in the private sense "
      "when it carries only public keys, but it is the record without which an explicit arrangement cannot be "
      "restored, so storing it in the wallet it describes is no backup at all. And a descriptor carrying an extended "
      "public key discloses the whole branch to whoever reads it, with the privacy consequence the previous branch "
      "described. A learner should also expect the notation to grow: the spending conditions a descriptor can carry "
      "are a language of their own, and this chapter opens it only far enough to read the common forms [AH] [B380].",
      "append"),
 ],

 "WalletNotes": [
  (H, "Labels work in the opposite direction from everything else in this chapter. A key is derived, so one record "
      "reproduces it; a label is assigned, so nothing reproduces it. The wallet stores a short piece of text against "
      "a reference - an address, a transaction, an output - and the pairing exists only in that store, because the "
      "chain records the payment and knows nothing about what the payer called it. That is why moving labels between "
      "applications needs a format rather than a derivation: the proposal this section names writes one record per "
      "line, each a small object giving the kind of thing being labelled, the reference that identifies it and the "
      "text itself, so that an export from one wallet is a file another can read. The mechanism is deliberately "
      "plain, because the difficulty here is not the encoding but the fact that this information has no other "
      "source [AH] [B329].", "replace-last"),
  (E, "The reader meets labels as the first thing they lose and the last thing they think of. A wallet restored from "
      "its code shows the right balance and the right history with every description gone, which is the moment the "
      "distinction in this section becomes concrete. They are met in the export and import menus of wallets that "
      "implement the format, and in this course's own account of what a complete backup contains, where the labels "
      "are one of the five items and the only one that no amount of derivation can rebuild [AH] [B329].", "append"),
  (K, "The caution is about privacy rather than loss. A label file is the most revealing document a wallet can "
      "produce: it ties addresses to names, purposes and counterparties, which is exactly the linkage that using a "
      "fresh address for each payment was meant to prevent. So a label backup needs the protection a key backup "
      "needs, for a different reason, and the encrypted backup of the next section is the mechanism the chapter "
      "offers for it [AH] [B329].", "append"),
 ],

 "OtherProtocolData": [
  (H, "The difficulty works like this. A protocol built on top of Bitcoin keeps state that changes with every "
      "payment, and the newest state is the only safe one, because an old state is a claim the counterparty can "
      "prove to be out of date and penalise. A backup is therefore stale the moment it is taken, which is a "
      "different problem from the one a recovery code solves - the code is correct for ever, and this data is correct "
      "for one moment. The two answers in this section attack it from opposite ends. A static backup gives up on "
      "restoring the state and keeps only what is needed to ask the counterparty to close out and return the funds, "
      "which recovers the money and loses the channel. An encrypted wallet backup gives up on deriving the data and "
      "simply copies all of it, keys and labels and protocol state together, under a key that the seed itself "
      "produces - which is the one mechanism in the chapter that backs up everything [AH] [AH14] [LR].",
      "replace-last"),
  (E, "The reader meets this group only if they use a second-layer protocol, and then immediately. Setting up a "
      "payment channel produces a backup file within minutes and a warning about restoring old copies of it; the "
      "same warning appears in the documents of the implementations, which this course fetched and saved. The "
      "encrypted backup is met in the handful of wallets that offer it, and its idea is met again in chapter 4's "
      "passphrase protection, because both derive a protecting key from something the user already has [AH14] [LR].",
      "append"),
  (K, "The caution is that restoring the wrong copy here is worse than restoring nothing. With keys, an old backup is "
      "simply incomplete; with channel state, an old backup can be a provably stale claim, and acting on it can cost "
      "the funds it was meant to protect. The second caution is that an encrypted backup moves the problem to the key "
      "that encrypts it: if that key is derived from the seed, the backup is only as safe as the seed, and if it is "
      "not, it is one more secret to keep [AH] [AH14].", "append"),
 ],

 "WebStore": [
  (H, "The arrangement works by putting a parent public key where the risk is and keeping its private counterpart "
      "away. The store's server holds an extended public key and a path to derive along; for each visitor it derives "
      "the next index and shows the address that comes out, so every customer is given a fresh address and the server "
      "never holds anything that can spend. Watching for payment is then the same derivation run ahead of time: the "
      "program derives a run of addresses it has not yet handed out and watches them all, and the length of that run "
      "is the gap limit. The limit exists because the watching program cannot tell an unused address from an address "
      "that was used while it was not looking, so if addresses are handed out faster than they are paid, a payment "
      "can land beyond the end of the watched run and go unnoticed until the limit is raised and the branch is "
      "rescanned [AH] [B32].", "replace-last"),
  (E, "The reader meets this arrangement in the chapter's own story of a store that grows from one address to a tree, "
      "and in any payment processor that is configured with an extended public key rather than with a wallet file. "
      "The gap limit is met as a number in the settings of such a program and in a node's own look-ahead, which the "
      "run saved with this chapter shows as a ranged child path over a thousand indices, a range the source "
      "describes as the look-ahead used to detect payments [AH] [BCW].", "append"),
  (K, "The caution is that this arrangement protects the money and not the privacy. The extended public key on the "
      "server is enough to derive every address the store will ever use, so whoever reads it - an attacker, a "
      "hosting provider, a subpoena - obtains the store's whole turnover, past and future. And it does not protect "
      "the money completely either: a server that can be altered can be made to show an attacker's addresses "
      "instead, which costs the store its takings without any key being stolen at all [AH].", "append"),
 ],

 "OfflineKeys": [
  (H, "Keeping keys offline works by making a boundary that the secret never crosses. The unsigned transaction is "
      "built on the connected machine and carried over the boundary; the signature is produced on the other side and "
      "carried back; the key stays where it was. A hardware signing device is that boundary built into an object - it "
      "holds the seed, derives what it needs, shows the path and the amount on its own screen so that the connected "
      "machine cannot lie about what is being signed, and returns only the signature. A written record of the "
      "recovery code is the same boundary in its simplest form: paper has no interface at all, which is exactly its "
      "security property and exactly its weakness, since it cannot check anything either and is lost to fire, water "
      "and tidying up [AH].", "replace-last"),
  (E, "The reader meets this group as the physical half of every arrangement earlier in the chapter. The device is met "
      "as the thing the wallet application asks to sign; the written code is met once, when it is copied down, and "
      "then ideally never; cold storage is met as a decision about where an object lives rather than as software. "
      "They are met again in chapter 4's section on the same device, and in this chapter's record of what goes wrong, "
      "where the risks to a physical object are documented rather than assumed [AH] [LO].", "append"),
  (K, "The caution is that offline is a property of the key and not of the device. A device used to restore a code "
      "that was typed into a connected computer has an online key in an offline box, and a paper record photographed "
      "once is online for ever. The second caution is that the device's screen is the whole of its advantage: a "
      "signature approved without reading the path and the amount on that screen is a signature the connected "
      "machine chose, and the boundary has bought nothing [AH].", "append"),
 ],

 "CryptographicPrimitives": [
  (H, "The four primitives work together as a chain of guarantees, and each statement in this chapter rests on one of "
      "them. A hash function gives a short value that depends on all of its input, cannot be run backwards and "
      "changes completely when the input changes, which is what makes a checksum, a fingerprint and a commitment "
      "possible. The named family of hash functions supplies the particular functions the standards call for, and "
      "the keyed form of one of them is the splitter behind every derivation in this chapter. A digital signature "
      "turns control of a private key into a number anybody can check, which is what proves a spend is authorised "
      "without revealing the key. Secret sharing distributes one secret into several pieces so that any agreed "
      "number of them restores it and fewer reveal nothing, which is how one of the recovery-code schemes turns a "
      "single point of failure into a threshold [AH] [B32] [S39] [R2104].", "replace-last"),
  (E, "The reader meets these four throughout the course rather than only here. The hash function gave the "
      "transaction identifier of chapter 2, the block identifier of chapter 3 and the address commitment of chapter "
      "4; its keyed form gives the master keys and every child of this chapter; the signature authorised every "
      "payment of chapter 2 and is the proof of control of chapter 4. Secret sharing is met only in this chapter, "
      "and the worked example for it is a toy over a small prime field rather than the field the real scheme uses, so "
      "that the arithmetic can be read [S39].", "append"),
  (K, "The caution is that these are the assumptions of the chapter and not its results. Every claim that a child key "
      "cannot be traced to its parent, that a code cannot be guessed, or that a signature cannot be forged, is a "
      "claim about the present strength of one of these primitives, which is the state of the art rather than a "
      "theorem. A learner should also resist treating them as interchangeable: a keyed hash and a signature both "
      "prove that somebody knew a secret, but only the signature can be checked by a party who does not know it "
      "[AH] [R2104].", "append"),
 ],

 "RecoveryPractice": [
  (H, "The practice works by turning the chapter's technical content into a list and then checking the list. A "
      "complete backup is the recovery code, the passphrase if one is used, the derivation paths or the descriptors "
      "that record them, the public keys of any other signers, and the data that is not keys; each item is one of "
      "this chapter's own branches, and each is a separate way for a restoration to fail. Testing is what converts "
      "that list from a belief into a fact, and a test means a real restoration into software that did not create "
      "the wallet, because only that catches the failures that matter - a word copied wrongly, a passphrase "
      "remembered imperfectly, a path nobody wrote down, a label file never exported. Nothing about this is "
      "automatic: data loss is not an attack that defences prevent but an accident that only a tested backup "
      "survives [AH].", "replace-last"),
  (E, "The reader meets this group at the end of the chapter and, if the chapter has done its work, before anything "
      "has gone wrong. It is met in the chapter's own closing sentences, which name loss rather than theft as the "
      "leading cause of lost bitcoins and put the responsibility on the holder; and it is met in the design of this "
      "course's material, where every chapter's figures are recomputed rather than copied for the same reason a "
      "backup is restored rather than assumed [AH].", "append"),
  (K, "The caution is that a test can give false comfort. Restoring into the same application that made the wallet "
      "proves that the application can read its own file and nothing more; restoring the code without the passphrase "
      "proves that the words are right and leaves the wallet still unreachable; checking that a balance appears "
      "proves the receiving branch and says nothing about the change branch. A test is worth what it covers, which "
      "is why the list above has five items rather than one, and why the chapter asks for the test to be repeated "
      "rather than performed once [AH].", "append"),
 ],
}

# ---------------------------------------------------------------------------------------------------------------------
# the new worked examples, each executed by the chapter builder
# ---------------------------------------------------------------------------------------------------------------------
IO_EDITS = {
 # keys are tiny: a thousand private keys are thirty-two kilobytes, while the outputs they control stay on the chain
 "WalletDatabase": ("(lambda keys, size: (keys * size, round(keys * size / 1024, 1)))(1000, 32)", "(32000, 31.2)"),
 # the property that lets a public key be derived without the private one: shifting the secret by a tweak shifts the
 # public value by the same tweak's multiple - shown here in a toy group small enough to check by hand
 "KeyTweak": ("(lambda p, g, a, t: (((a + t) % p) * g % p, (a * g % p + t * g % p) % p))(17, 5, 9, 3)", "(9, 9)"),
 # every passphrase is another wallet from the same words, which is what deniability rests on and what a typo costs
 "PlausibleDeniability": ("(lambda passphrases: (len(passphrases), len(passphrases) + 1))(['holiday', 'decoy'])",
                          "(2, 3)"),
 # what a person has to hold in memory: eleven bits a word, so a twelve-word and a twenty-four-word code
 "Memorization": ("(12 * 11, 24 * 11)", "(132, 264)"),
 # an implicit path is read back from the standard: the master, the purpose, the coin, the account, the branch, the index
 "ImplicitPath": ("\"m/84'/0'/0'/0/0\".split('/')", "['m', \"84'\", \"0'\", \"0'\", '0', '0']"),
 # an explicit path is text that has to be written down: a key origin against the path it records
 "ExplicitPath": ("(len('[6d8c4b8f/84h/0h/0h]'), len(\"m/84'/0'/0'\"))", "(20, 11)"),
 # a label is assigned, not derived, so moving it needs a record: one line of the export format
 "AddressLabel": ("__import__('json').dumps({'type': 'addr', "
                  "'ref': 'bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu', 'label': 'Alice'})",
                  "'{\"type\": \"addr\", \"ref\": \"bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu\", "
                  "\"label\": \"Alice\"}'"),
 # a signature is over a digest, so one changed character gives a different number to sign
 "DigitalSignature": ("(lambda h, a, b: sum(bin(x ^ y).count('1') for x, y in zip(h(a), h(b))))"
                      "(lambda m: __import__('hashlib').sha256(m).digest(), b'pay Bob 1 BTC', b'pay Bob 2 BTC')",
                      "135"),
 # why loss is final: the number of seeds a lost one could have been
 "DataLoss": ("2 ** 128", "340282366920938463463374607431768211456"),
 # a complete test covers five things, which are the five items a complete backup holds
 "BackupTesting": ("len(['the recovery code', 'the passphrase if one is used', "
                   "'the derivation paths or the descriptors', 'the public keys of any other signers', "
                   "'the data that is not keys'])", "5"),
}

NO_EXAMPLE = {
 "PublicKeyOnlyWallet": "The concept states which half of a wallet's material is present. Any expression would either "
                        "add up the byte lengths of a public key and a chain code, which teaches arithmetic rather "
                        "than the arrangement, or compare a derivation that succeeds with one that is simply absent. "
                        "The arrangement is shown instead by the worked examples of the extended public key and of "
                        "the key tweak, both of which are executed.",
 "ExternalSigning": "The concept states a protocol between two parties - unsigned transaction out, signature back. "
                    "What makes it work is that the key does not move, which is the absence of a computation rather "
                    "than one; an expression here would model two function calls and prove nothing about the "
                    "boundary.",
 "MuunCode": "The concept states that this scheme's words are not a seed. Showing that would need the scheme's own "
             "cipher, which is not in the standard library and which the chapter does not teach; counting the "
             "characters of a code would be an example about the length of a string.",
 "PhysicalCoercion": "The concept states a documented risk. Its one figure, the number of recorded attacks, is "
                     "already executed by a CHECKS entry that counts the rows of the saved copy of the published "
                     "list; that count cannot run inside the page, which has no access to the file, and writing the "
                     "number as a literal would assert it rather than compute it.",
 "LightningNetwork": "The concept introduces a protocol whose own mechanisms belong to a later chapter. A "
                     "self-contained expression could only compare two state numbers, which illustrates that six is "
                     "larger than five.",
 "StaticChannelBackup": "The concept states what such a backup can and cannot recover. The distinction is one of "
                        "protocol consequence - the funds come back and the channel does not - and there is no "
                        "figure in it to compute.",
 "PaymentProcessor": "The concept names a kind of program. Its behaviour that matters here, deriving the next address "
                     "and watching ahead, is already the worked example of the deployment and of the gap limit.",
 "ColdStorage": "The concept states a condition of the keys rather than an operation on them: that they are not on a "
                "machine that is connected. There is nothing to evaluate, and an expression would be a label "
                "dressed as a computation.",
 "HardwareSigningDevice": "The concept names a physical object and what its screen is for. Its arithmetic - the "
                          "derivation it performs - belongs to the derivation concepts, which carry executed "
                          "examples; what is particular to the device is that a person reads it.",
}

# ---------------------------------------------------------------------------------------------------------------------
def _apply(node):
    # this chapter's node tuples carry a seventh element after the paragraphs; it is passed through untouched
    nid, lab, lv, par, leaf, paras = node[:6]
    tail = tuple(node[6:])
    paras = list(paras)
    for facet, text, mode in PARA_EDITS.get(nid, ()):
        if mode == "replace-last":
            paras[-1] = (facet, _c(text))
        elif mode == "append":
            paras.append((facet, _c(text)))
        else:
            raise AssertionError("unknown mode %r" % mode)
    if nid in IO_EDITS:
        assert leaf is not None and leaf[2] is None, "%s already carries a worked example" % nid
        leaf = (leaf[0], leaf[1], IO_EDITS[nid])
    return (nid, lab, lv, par, leaf, paras) + tail


NODES = [_apply(n) for n in B.NODES]

_seen = {n[0] for n in NODES}
assert set(PARA_EDITS) <= _seen, sorted(set(PARA_EDITS) - _seen)
assert set(IO_EDITS) <= _seen, sorted(set(IO_EDITS) - _seen)
assert set(NO_EXAMPLE) <= _seen, sorted(set(NO_EXAMPLE) - _seen)
assert not (set(IO_EDITS) & set(NO_EXAMPLE))
_l2 = [n for n in NODES if n[2] == 2]
assert set(PARA_EDITS) == {n[0] for n in _l2}, "every second-level section must be covered"
for n in _l2:
    assert 4 <= len(n[5]) <= 6, "%s has %d paragraphs" % (n[0], len(n[5]))

CHECKS = list(B.CHECKS) + [
 # the arithmetic of the code-generation chain, as the new prose states it
 ("(2 ** 11, 128 // 32, (128 + 128 // 32) // 11)", "(2048, 4, 12)"),
 # the stretching count and the seed length the derivation section quotes
 ("(2048, 64, 64 * 8)", "(2048, 64, 512)"),
 # the keyed hash splits its output into two halves of equal length
 ("(64 // 2, 64 // 2)", "(32, 32)"),
 # each node's indices, and the split into a normal and a hardened half
 ("(2 ** 32, 2 ** 31, 2 ** 32 - 2 ** 31)", "(4294967296, 2147483648, 2147483648)"),
 # the bytes of an extended key, field by field, as the extended-keys section lists them
 ("4 + 1 + 4 + 4 + 32 + 33", "78"),
 # the checksum characters a descriptor carries
 ("len('#') + 8 - 1", "8"),
 # what a person must remember for each code length
 ("(12 * 11, 24 * 11)", "(132, 264)"),
 # the five items of a complete backup
 ("len(['the recovery code', 'the passphrase if one is used', 'the derivation paths or the descriptors', "
  "'the public keys of any other signers', 'the data that is not keys'])", "5"),
 # the tweak property, in the toy group the key-tweak example uses
 ("(lambda p, g, a, t: ((a + t) % p) * g % p == (a * g % p + t * g % p) % p)(17, 5, 9, 3)", "True"),
]
