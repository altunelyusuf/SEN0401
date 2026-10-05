#!/usr/bin/env python3
"""SEN0401 chapter 4 corpus, version 1.2.0: Keys and addresses. Over 1.1.0 this version changes the TEXT and the WORKED
EXAMPLES of named concepts and nothing else - every concept identifier, label, level, parent, example label and
definition of 1.1.0 is kept exactly, so the change is additive and the version is MINOR.

Why it exists. An adversarial audit of the chapter 1 page (2026-10-04) found two defects that measurement showed to
hold for this chapter too, and more sharply:

  * ten of the thirteen second-level sections had three paragraphs against the owner's standard of four to six -
    Randomness 196 words, Checksummed text 211, Hash functions 213, Key encoding 226, Assurance 235, Identifiers 274,
    Representation of data 274, Locking and unlocking scripts 282, Key pair 284, The curve 327; and
  * every one of those ten closed on a paragraph that only listed the concepts beneath it, which is the same list the
    page's breadcrumb row already prints, so the closing paragraph taught nothing.

This version replaces each of those ten closing paragraphs with one that explains how the section's subject works, and
brings all ten to five paragraphs - the length the chapter's first-level branches and third-level concepts already
have. It also gives a worked example to four of the five concepts that had none. The fifth is named in the declining
list below with its reason.

Figures the new prose states are executed: the byte lengths of a private and a compressed public key, the number of
bits by which two SHA-256 digests of near-identical messages differ, the leading character each version byte produces
in base58check, and the three parts of a decentralized identifier. Each is either the worked example of the concept
that states it or a CHECKS entry of this file.
"""
__version__ = "1.2.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch04_corpus_v1_1_0 as B

CHAPTER = B.CHAPTER
_c = B._c
CQS, PROVENANCE, TOOLING, DOC_TITLE, DOC_ABOUT = B.CQS, B.PROVENANCE, B.TOOLING, B.DOC_TITLE, B.DOC_ABOUT
OWNERS, ERRORS, RAISES = getattr(B, "OWNERS", []), getattr(B, "ERRORS", []), B.RAISES
W, Y, E, H, K = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out"

CHANGE = ("1.2.0 keeps every concept of 1.1.0 and changes only text and worked examples, so it is MINOR. Ten "
          "second-level sections had three paragraphs and each closed on a list of its own children, which the page's "
          "breadcrumb row already prints; every one of those closing paragraphs is replaced by a paragraph on how the "
          "section's subject works, and all ten are brought to five paragraphs. Four concepts that had no worked "
          "example are given one, each executed by the chapter builder: public key cryptography, the digital "
          "signature, the version prefix and the decentralized identifier. Proof of control by a key is left without "
          "one on purpose, because the page's in-browser interpreter has no elliptic-curve library and a keyed-hash "
          "stand-in would demonstrate a shared secret rather than a signature anyone can check.")

# ---------------------------------------------------------------------------------------------------------------------
# the new paragraphs: concept id -> [(facet, text, "replace-last" | "append")]
# ---------------------------------------------------------------------------------------------------------------------
PARA_EDITS = {

 "KeyPair": [
  (H, "The pair works in one direction only, and everything else follows from that. The private key is simply a very "
      "large whole number, chosen at random; the public key is obtained by adding a fixed point on the curve to "
      "itself that many times, an operation the next level of the chapter sets out in full. Computing forward is "
      "cheap, because doubling and adding reach any multiple in a few hundred steps rather than in as many steps as "
      "the number is large. Computing backward - recovering the multiplier from the result - has no comparable "
      "shortcut, and that asymmetry is the whole of the protection. It also explains the book's tip that a wallet "
      "need store only the private key: the public key is not a second secret to be guarded but a value that can be "
      "recalculated from the first whenever it is wanted [BK].", "replace-last"),
  (E, "The reader meets the pair wherever a wallet is created or a key is moved. A new wallet reports the keys it has "
      "made rather than their values; an export writes the private key out in a text form and leaves the public key "
      "to be recomputed; a block explorer shows the public side, or a commitment to it, because that is the half "
      "which has to travel. The pair is met again in every later chapter of this course: the signature of chapter 2 "
      "is made with the private half and checked with the public half, and the tree of keys in chapter 5 is a way of "
      "making very many pairs from one secret [BK].", "append"),
  (K, "Two cautions. The names mislead a little: a public key is public only once it has been used, and a wallet that "
      "hands out a fresh commitment for each payment is deliberately keeping it back, for reasons the section on "
      "address reuse gives. And the pair is not an identity. It proves that whoever signs holds the private key; it "
      "says nothing about who that is, nor about whether the key is still in the hands it was in yesterday. Treating "
      "a key as a person is the mistake behind most of the losses this chapter's later sections warn about [BK].",
      "append"),
 ],

 "RandomSource": [
  (H, "Secure randomness works by gathering unpredictability from the physical world and then stretching it. The "
      "operating system collects events whose exact timing nobody can reproduce - the intervals between interrupts, "
      "the arrival of network packets, the noise of a dedicated hardware source - and mixes them into a pool. A "
      "program then asks the system for bytes, and the system returns the output of a cryptographic generator seeded "
      "from that pool, which is indistinguishable from random to anyone who does not know the seed. Two consequences "
      "matter for a learner. The amount of genuine unpredictability is a property of the seed, not of the length of "
      "the output, so stretching 128 bits of entropy into 256 bits of key leaves 128 bits of real strength. And "
      "because the quality lives in the system rather than in the arithmetic, the book's rule - use the "
      "cryptographically secure generator and do not write your own - is advice about which door to knock on rather "
      "than about which formula to use [BK].", "replace-last"),
  (E, "The reader meets the distinction in the standard library of almost any language, which offers two generators "
      "side by side: one made for simulations, fast and deliberately reproducible from a seed, and one made for "
      "secrets, which cannot be reseeded by the caller and so cannot be replayed. Python names them in just that way, "
      "and its documentation says outright that the reproducible one must not be used for security [PSF]. The same "
      "distinction appears in this chapter's own visual for the concept, where four thousand keys drawn from the "
      "reproducible generator are sorted by their first digit: the bars are level, which is what a usable generator "
      "looks like, and the picture is identical on every build because the draw was seeded on purpose.", "append"),
  (K, "The failures here are historical rather than hypothetical, and they share a shape: the arithmetic was correct "
      "and the source was not. A generator seeded from the clock, a generator that restarts from the same state after "
      "a reboot, a generator whose output is derived from a passphrase a person invented - each produces keys that "
      "look like arbitrary sixty-four-digit numbers and that an attacker can search in a tiny fraction of the key "
      "space. A learner should take from this that the size of the key space is an upper bound on security and never "
      "a measurement of it [BK].", "append"),
 ],

 "Curve": [
  (H, "The construction works in three layers, each built from the one below. The bottom layer is a finite field: the "
      "numbers are the remainders after division by one very large prime, and addition and multiplication are the "
      "ordinary operations followed by taking the remainder, which keeps every result inside the same finite set. The "
      "middle layer is the curve, the set of pairs in that field satisfying the curve's equation, together with one "
      "extra point that acts as a zero. On that set an addition of points is defined geometrically - draw the line "
      "through two points, take the third point where it meets the curve, reflect it - and the definition turns the "
      "curve into a group, which is the only property the cryptography needs. The top layer is multiplication of a "
      "point by a whole number, which is repeated addition carried out by doubling, so that a multiplier of two "
      "hundred and fifty-six bits costs a few hundred operations rather than astronomically many. A public key is "
      "the generator point multiplied by the private key, and the discrete logarithm problem is the absence of any "
      "comparable shortcut in the other direction [BK] [SEC2].", "replace-last"),
  (E, "The reader meets this level twice over, at two scales. The small scale is the chapter's own worked examples "
      "over the field with seventeen elements, where the whole curve has few enough points to list and a student can "
      "check an addition on paper; the arithmetic there is identical to the arithmetic Bitcoin uses, which is the "
      "point of showing it. The large scale is the curve named in the standard, whose parameters this chapter quotes "
      "from the specification and whose generator point it encodes; the same parameters are what the library inside "
      "every wallet is compiled with [SEC2] [CORE].", "append"),
  (K, "Two cautions about pictures and about proofs. The smooth curve drawn in textbooks over the real numbers is a "
      "teaching aid: over a finite field the points are a scatter with no shape to the eye, and a learner who "
      "reasons from the drawing will reach wrong conclusions about how many points lie near one another. And the "
      "hardness of the discrete logarithm problem is not a theorem but the present state of the art; no proof exists "
      "that no shortcut can be found, so every statement about the strength of a key in this chapter is a statement "
      "about what is known today [BK].", "append"),
 ],

 "Hashing": [
  (H, "A hash function works by consuming its input in fixed-size blocks and stirring each block into a small block "
      "of internal state, so that the state at the end depends on every bit of the input and on the order in which "
      "the bits arrived. Three properties are what make the result usable as a reference. The output has the same "
      "length whatever the input is, so a reference to a short key and a reference to a long script cost the same. "
      "Changing any part of the input changes about half the bits of the output, so two inputs that differ slightly "
      "have outputs with nothing visibly in common. And the function cannot be run backwards, so a reference can be "
      "published without publishing what it refers to - which is exactly what an address does. Chaining two "
      "different functions, as Bitcoin does when it applies the second to the output of the first, shortens the "
      "result and means that a weakness found in one of them is not on its own a weakness in the pair [BK] [FIPS].",
      "replace-last"),
  (E, "The reader meets these functions at every step of the chapter and then everywhere else in the course. Here "
      "they turn a public key into the twenty bytes an address commits to, and they produce the four checksum bytes "
      "that protect the text of the address. In chapter 2 the same arithmetic gave the identifier of a transaction "
      "and the root of a block's Merkle tree; in chapter 3 it gave the identifier of a block; in chapter 5 it is the "
      "engine of the key-stretching step that turns a recovery code into a seed. The functions themselves are "
      "published standards rather than Bitcoin's own, which is why this course quotes a national standard for the "
      "first of them [FIPS].", "append"),
  (K, "The caution is about strength and about length. A hash is only as strong as the shorter of the function and the "
      "output: cutting a thirty-two byte result down to twenty bytes, as Bitcoin does, lowers the work an attacker "
      "needs, and the three attacks described later in this chapter are the reason the newer addresses commit to "
      "thirty-two bytes instead. And one of the two functions used here is no longer available in every current "
      "software library, which is why this course states the lengths it produces and cites them to their standard "
      "rather than recomputing them in the browser [BK] [PSF].", "append"),
 ],

 "Representation": [
  (H, "A representation works by fixing two things: an alphabet of symbols, and a rule for reading a sequence of them "
      "as a number. The number is what exists; the text is one of many ways of writing it. Choosing a larger alphabet "
      "makes the text shorter, because each symbol carries more of the number - a byte written in base sixteen takes "
      "two characters, in base fifty-eight roughly one and a third, in base thirty-two exactly one and three fifths "
      "- and choosing which symbols the alphabet leaves out decides how safely a person can copy the text by hand. "
      "That is why the formats of this chapter differ: one drops the characters that look alike, another uses one "
      "case only so the text can be spoken and packed into a barcode. A picture such as a barcode is the same "
      "choice taken further, with the alphabet made of marks rather than letters [BK] [B173].", "replace-last"),
  (E, "The reader meets these three notions in every length the chapter quotes. A private key is thirty-two bytes, "
      "which is sixty-four hexadecimal digits and fifty-one characters in the wallet's export format; an "
      "uncompressed public key is sixty-five bytes and a hundred and thirty hexadecimal digits; a native-segwit "
      "address of this chapter is forty-two characters of a thirty-two symbol alphabet. Each of those statements is "
      "about a representation and not about a different value, and the chapter's own figures for them are computed "
      "rather than quoted [BK].", "append"),
  (K, "The caution is that a conversion can lose information even when it looks harmless. Case is the common trap: "
      "the older format distinguishes upper from lower case and the newer one does not, so a reader who writes an "
      "older address in capitals has destroyed it, while writing a newer one in capitals is permitted and changes "
      "nothing. The second trap is the leading zero: a number has no leading zeros but a byte string does, and an "
      "encoding that forgets them produces text of the wrong length, which is why the procedure later in this "
      "chapter handles them as a separate step [BK].", "append"),
 ],

 "KeyEncoding": [
  (H, "The encodings work by wrapping the same value in a few bytes that say how to read it. A public key is a point "
      "with two coordinates; writing both gives sixty-five bytes, but the curve's equation determines the second "
      "coordinate up to its sign, so a single byte recording which sign applies is enough and the compressed form "
      "is thirty-three bytes. The export form of a private key is the thirty-two secret bytes with a version byte in "
      "front, a checksum behind and, when the key belongs to a compressed public key, one extra byte in the middle "
      "whose only job is to tell the importing wallet which of the two public keys to derive. Nothing is encrypted "
      "and nothing is compressed in the ordinary sense: every one of these forms can be converted into any other, "
      "which is what the book means when it says the formats are interchangeable [BK].", "replace-last"),
  (E, "The reader meets the encodings whenever a key crosses a boundary between programs. A key handed to a learner "
      "in a tutorial is in hexadecimal; a key exported by a wallet for a backup is in the text format that begins "
      "with a recognisable character; a key inside a transaction is the compressed binary form. The place where the "
      "distinction bites is an import, because the receiving wallet has to decide which addresses to look for, and "
      "the chapter quotes the book's warning about exactly that case [BK].", "append"),
  (K, "The caution is that one of these names is a misnomer and the book says so. Nothing about a private key is "
      "compressed; what the extra byte records is that the public key derived from it should be the compressed one. "
      "A learner who reads the name literally will expect the key itself to be shorter, find that it is not, and "
      "distrust the rest of the section. The second caution is that these text forms carry the secret in plain "
      "sight: an exported private key is the funds, and the chapter's section on passphrase protection exists "
      "because a backup of one is as sensitive as the wallet it came from [BK].", "append"),
 ],

 "Checksummed": [
  (H, "A checksum works by adding characters that are a function of everything before them, so that the valid strings "
      "are a tiny scattered subset of all the strings that could be written. The older format of this chapter hashes "
      "the version byte together with the payload, twice, and appends the first four bytes of the result; a decoder "
      "recomputes the hash and compares. Because the four bytes are thirty-two bits, a string altered at random "
      "passes by chance about once in four thousand million attempts, and because a hash spreads any change over the "
      "whole output, there is no family of mistakes it is systematically blind to. What such a check cannot do is say "
      "where the mistake was or repair it - it only refuses - and the newer format of the next level was designed "
      "with that limitation in mind. The version byte sits inside the protected data rather than beside it, which is "
      "why altering the byte that decides the network also breaks the check [BK] [B173].", "replace-last"),
  (E, "The reader meets the check as the wallet's refusal. Pasting an address with one character changed produces an "
      "error rather than a payment, and that error is this section at work; the same check runs on an imported "
      "private key and on an extended key of chapter 5. The reader meets the version byte as the first character of "
      "the text, which is why an address beginning with one digit and an address beginning with another are "
      "recognisably different kinds, and why a key or an address for the test network cannot be mistaken for one on "
      "the main network [BK].", "append"),
  (K, "The caution is about what the guarantee covers. The check catches mistakes in copying; it cannot catch an "
      "address that was copied perfectly from the wrong place. A string substituted by malicious software, or taken "
      "from the wrong line of a message, is a valid address with a valid checksum and the payment is final. The "
      "second caution is that four bytes is a defence against accident and not against a determined search, which is "
      "the difference between a checksum and the cryptographic commitments elsewhere in this chapter [BK].", "append"),
 ],

 "Scripts": [
  (H, "The two scripts work as a single program assembled at spending time and run on a stack machine. A node takes "
      "the input script written by the spender, runs it, and the values it pushes are left on the stack; it then runs "
      "the output script that the earlier transaction attached to the funds, which consumes those values and tests "
      "them. For the commonest case the input script pushes a signature and a public key, and the output script "
      "checks that the public key hashes to the commitment recorded in it and that the signature matches both the "
      "key and the transaction being authorised. The spend is allowed when the machine finishes with a true value on "
      "top and nothing has failed. Two consequences explain the whole of the rest of this chapter: the condition is "
      "chosen by the receiver and recorded in the output, so an address is nothing but a compact way of telling a "
      "payer which output script to write; and because the condition is a program rather than a key, it can require "
      "two signatures, or a delay, or anything else the language can express [BK].", "replace-last"),
  (E, "The reader meets the scripts without seeing them. Every payment in chapter 2 was authorised this way, and "
      "every full node of chapter 3 ran the machine on it; a block explorer shows the two scripts side by side when "
      "a transaction is opened. In this chapter the scripts are met as the thing each address kind names: the "
      "sections that follow differ from one another only in which output script the address stands for, which is why "
      "they can be read quickly once this level is understood [BK].", "append"),
  (K, "The caution is that this level is deliberately shallow. It gives only what is needed to read the address kinds, "
      "and the book promises the full treatment later; a learner who tries to settle questions about the language's "
      "operations or its limits from this level will not find the answers here. The second caution is that a script "
      "guards the funds and a mistake in one is not recoverable: an output script that nobody can satisfy locks the "
      "money for ever, which is why addresses, standard templates and published test vectors exist rather than "
      "hand-written scripts [BK].", "append"),
 ],

 "Assurance": [
  (H, "Assurance works by comparing a program against something that was not produced by that program. A test vector "
      "does this by fixing an input and the answer the standard requires, so that an implementation which disagrees "
      "is wrong by definition rather than by opinion; vectors that cover cases the implementer did not think of - "
      "strings that must be rejected, versions not yet defined - are the valuable ones, because they test the "
      "boundaries where an implementation silently guesses. A cross-check does it by running two implementations "
      "written by different people on the same input and comparing, which catches a shared misreading of the "
      "standard only when the two authors read it independently. Neither method proves a program correct: both are "
      "ways of raising the cost of being wrong, and the published record of wallets that could not pay the newer "
      "addresses is what that cost looks like when nobody pays it [BK] [B350].", "replace-last"),
  (E, "The reader meets assurance in this course as a habit rather than a topic. Every figure in this chapter is "
      "recomputed before it is stated, and where a standard publishes a vector the computation is run against the "
      "vector; where an independent program is available, the answer is asked of it as well, which for this chapter "
      "meant putting the derivations to a real release of the reference implementation. The same habit appears in the "
      "chapter's own record of findings, where a statement of the book that did not survive the check is written down "
      "with what the sources actually say [BK] [CORE].", "append"),
  (K, "The caution is that passing the vectors is a floor and not a ceiling. A decoder can agree with every published "
      "example and still mishandle an input nobody published; an implementation can be right about the arithmetic "
      "and wrong about where it keeps the key. And a cross-check between two programs that share a library is not "
      "independent, however separate the programs look, which is worth remembering whenever two tools agree "
      "suspiciously quickly [B350].", "append"),
 ],

 "Identifiers": [
  (H, "The ladder works by separating three questions that are easy to run together: what a name is, who may issue "
      "it, and how a claim made under it is checked. A uniform resource identifier answers the first by fixing a "
      "syntax, so that the same string denotes the same thing in every program that reads it. The usual answer to "
      "the second is an authority - a registry that assigns the name and can take it back - and the identifiers of "
      "this section replace that authority with a key: the name contains, or resolves to, a document naming the "
      "public keys whose holder controls it, so issuing the name needs nobody's permission and control is "
      "demonstrated rather than recorded. The third question is answered by a signature, which anyone holding the "
      "public key can check and nobody else can produce. A Bitcoin key pair supplies exactly that third piece and "
      "nothing more, which is why it maps onto one field of such a document - a verification method - rather than "
      "onto the identifier as a whole [DID] [R3986].", "replace-last"),
  (E, "The reader meets this level wherever data from two systems has to be joined. Within this course it is met in "
      "the semantic branch of each chapter, where a concept, a source and a finding each carry an identifier so that "
      "a statement about one can be stored and found; outside it, in any catalogue that must refer to records it "
      "does not own. The identifiers that a key controls are met in practice in credential systems, where the holder "
      "of a name proves control at the moment of use instead of relying on a directory that may be offline or "
      "mistaken [DID] [W3C].", "append"),
  (K, "The caution is that a key proves control and nothing else. It does not say who the controller is, that the "
      "controller is the person they claim to be, or that the key has not changed hands; a document naming keys is "
      "only as current as whoever last updated it. And Bitcoin's own identifiers are not of this family: an address "
      "is a commitment to a spending condition, not a name with a document behind it, and a learner who treats the "
      "two as the same thing will expect a resolution step that Bitcoin does not have [DID].", "append"),
 ],
}

# ---------------------------------------------------------------------------------------------------------------------
# the new worked examples, each executed by the chapter builder
# ---------------------------------------------------------------------------------------------------------------------
IO_EDITS = {
 # the two halves of one pair, measured: the secret is 32 bytes, the publishable point 33, the extra byte being the
 # parity prefix that stands in for the whole second coordinate
 "PublicKeyCryptography": (
   "(lambda priv, pub: (len(bytes.fromhex(priv)), len(bytes.fromhex(pub)), len(bytes.fromhex(pub)) - "
   "len(bytes.fromhex(priv))))('1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD', "
   "'0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798')", "(32, 33, 1)"),
 # a signature is over a digest, so changing one character of the message changes about half the digest's bits:
 # the number signed is a different number, which is why a signature cannot be moved to another message
 "DigitalSignature": (
   "(lambda h, a, b: sum(bin(x ^ y).count('1') for x, y in zip(h(a), h(b))))"
   "(lambda m: __import__('hashlib').sha256(m).digest(), b'pay Bob 1 BTC', b'pay Bob 2 BTC')", "135"),
 # the version byte is inside the data the checksum protects, and it is what fixes the first character of the text
 "VersionPrefix": (
   "(lambda B58, h, payload: tuple((lambda p: (lambda full: '1' * (len(full) - len(full.lstrip(bytes([0])))) + "
   "(lambda n: ''.join(B58[n // 58 ** i % 58] for i in range(40)[::-1]).lstrip('1'))(int.from_bytes(full, 'big')))"
   "(p + h(h(p).digest()).digest()[:4]))(bytes([v]) + payload)[0] for v in (0x00, 0x05, 0x6f)))"
   "('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', __import__('hashlib').sha256, "
   "bytes.fromhex('bbc1e42a39d05a4cc61752d6963b7f69d09bb27b'))",
   "('1', '3', 'm')"),
 # a decentralized identifier is three parts separated by colons: the scheme, the method, and the name inside it
 "DecentralizedIdentifier": (
   "'did:example:123456789abcdefghi'.split(':')", "['did', 'example', '123456789abcdefghi']"),
}

NO_EXAMPLE = {
 "KeyControlProof": "Proving control means producing a signature that anyone holding the public key can check and "
                    "nobody else can produce. The page's in-browser interpreter has no elliptic-curve library, so the "
                    "only self-contained expression available would be a keyed hash, which both sides must know the "
                    "secret to check; that demonstrates a shared secret rather than public verification, and would "
                    "teach the opposite of what the concept says. The concept's own section instead points at the "
                    "signature examples of chapter 2 and at the derivations of this chapter, both of which are "
                    "executed.",
}

# ---------------------------------------------------------------------------------------------------------------------
def _apply(node):
    nid, lab, lv, par, leaf, paras = node
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
    return (nid, lab, lv, par, leaf, paras)


NODES = [_apply(n) for n in B.NODES]

_seen = {n[0] for n in NODES}
assert set(PARA_EDITS) <= _seen, sorted(set(PARA_EDITS) - _seen)
assert set(IO_EDITS) <= _seen, sorted(set(IO_EDITS) - _seen)
assert set(NO_EXAMPLE) <= _seen, sorted(set(NO_EXAMPLE) - _seen)
assert not (set(IO_EDITS) & set(NO_EXAMPLE))
for n in NODES:
    if n[2] == 2:
        assert 4 <= len(n[5]) <= 6, "%s has %d paragraphs" % (n[0], len(n[5]))

CHECKS = list(B.CHECKS) + [
 # the lengths the Representation section quotes
 ("(32 * 2, 65 * 2, len('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'))", "(64, 130, 42)"),
 # how many characters a byte costs in each base this chapter uses
 ("tuple(round(8 / __import__('math').log2(b), 3) for b in (16, 58, 32))", "(2.0, 1.366, 1.6)"),
 # a four-byte checksum: a string altered at random passes about once in this many tries
 ("2 ** 32", "4294967296"),
 # the compressed public key drops one of the two coordinates and adds a parity byte
 ("(65 - 33, 33 - 32)", "(32, 1)"),
 # the three version bytes and the first character each produces, recomputed
 ("(lambda B58, h, payload: tuple((lambda p: (lambda full: '1' * (len(full) - len(full.lstrip(bytes([0])))) + "
  "(lambda n: ''.join(B58[n // 58 ** i % 58] for i in range(40)[::-1]).lstrip('1'))(int.from_bytes(full, 'big')))"
  "(p + h(h(p).digest()).digest()[:4]))(bytes([v]) + payload)[0] for v in (0x00, 0x05, 0x6f)))"
  "('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', __import__('hashlib').sha256, "
  "bytes.fromhex('bbc1e42a39d05a4cc61752d6963b7f69d09bb27b'))", "('1', '3', 'm')"),
 # two near-identical messages, and how much of the digest changes
 ("(lambda h, a, b: (sum(bin(x ^ y).count('1') for x, y in zip(h(a), h(b))), 256))"
  "(lambda m: __import__('hashlib').sha256(m).digest(), b'pay Bob 1 BTC', b'pay Bob 2 BTC')", "(135, 256)"),
 # the three parts of a decentralized identifier
 ("len('did:example:123456789abcdefghi'.split(':'))", "3"),
]
