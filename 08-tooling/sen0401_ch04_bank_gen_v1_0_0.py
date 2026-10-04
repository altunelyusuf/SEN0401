#!/usr/bin/env python3
"""Writes 08-tooling/ch04-page/question_bank_v1_0_0.json for SEN0401 chapter 4 (Keys and Addresses).

One item at least for every concept of the chapter's page data, at least two for every concept that carries a worked
example and one of those an Apply item with a program. Every program is run here while the file is written and its
printed output must equal the option that is marked correct, so the bank cannot be written with a wrong answer; the
programs use only the standard library and avoid RIPEMD-160, which the page's Pyodide does not provide, so values that
need it appear as data. The answer position is assigned in rotation, which keeps each of the four positions at about a
quarter of the items. Check with: python3 question_bank_check_v1_2_0.py 04
"""
__version__ = "1.0.0"
import collections
import json
import os
import subprocess
import sys

PY = "/root/.local/bin/python3.14"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ch04-page", "question_bank_v1_0_0.json")
ITEMS = []


def it(concept, level, question, right, wrongs, why, code=None):
    """one bank item; `right` is the correct option, `wrongs` three distractors; with `code` the program is run and
    its output must equal `right`."""
    assert len(wrongs) == 3, (concept, question)
    ITEMS.append({"concept": concept, "level": level, "q": question, "code": code,
                  "right": right, "wrongs": list(wrongs), "why": why})


def ap(concept, right, code, wrongs, why, question="What does this program print?"):
    """an Apply item whose marked option is the program's own output"""
    it(concept, "Apply", question, right, wrongs, why, code)


# ============================================================================================================
# 1  KEYS
# ============================================================================================================
it("Keys", "Understand",
   "Why can Alice not simply tell the network who Bob is when she pays him?",
   "The nodes that verify the payment are not meant to learn any party's real-world identity",
   ["Node software has no field in which a name of more than 20 characters would fit",
    "Only miners are allowed to read the identities attached to a transaction",
    "The identities of both parties are kept in a separate registry that every wallet queries after each payment"],
   "The chapter opens by saying that the thousands of full nodes do not know who Alice or Bob are and that the design keeps it that way to protect their privacy.")
it("Keys", "Analyze",
   "Which two demands does the chapter say a method of paying Bob has to meet at the same time?",
   "No link to Bob's identity or his other payments, and only Bob able to spend afterwards",
   ["A fee of less than one satoshi for each virtual byte, and a confirmation in one of the next two blocks",
    "A public name for Bob, and a record of the payment in a central register",
    "An online wallet for Bob, and a signature from a trusted third party"],
   "Alice must communicate that Bob should receive the coins without tying the transaction to his identity or his other payments, and only Bob may spend them.")
it("KeyPair", "Remember",
   "In a Bitcoin key pair, which key is used for which purpose?",
   "The public key receives funds and the private key signs transactions that spend them",
   ["The public key signs transactions and the private key receives funds",
    "Both keys sign, and a third key is needed to receive funds",
    "The public key encrypts the transaction so that the nodes cannot read it, and the private key decrypts it again"],
   "The book says the public key is used to receive funds and the private key to sign transactions to spend them.")
it("KeyPair", "Understand",
   "Why can a wallet store only the private key of a pair and still work?",
   "The public key can be recalculated from the private key at any time",
   ["The public key is published on the blockchain and can be looked up there",
    "The two keys are the same number written in two different bases",
    "A wallet without the public key can still sign but not receive"],
   "A tip in the book notes that the public key can be calculated from the private key, so storing only the private key is also possible.")
it("PublicKeyCryptography", "Remember",
   "What does the book give as the useful property of asymmetric cryptography for Bitcoin?",
   "The ability to generate digital signatures that anyone can verify",
   ["The ability to encrypt a transaction so that only the receiver can read it",
    "The ability to compress a public key into a shorter form",
    "The ability to prove that a transaction was broadcast at a particular time"],
   "The book states plainly that asymmetric cryptography is not used to encrypt the transactions; its useful property is the ability to generate digital signatures.")
it("PublicKeyCryptography", "Analyze",
   "A student says the one-way property of elliptic curve multiplication has been proved. What is wrong?",
   "The book claims only that the reverse is infeasible with today's computers and algorithms",
   ["Nothing: the proof appears in the standard that defines the curve",
    "The property has been proved, but it holds only for private keys smaller than the order of the curve",
    "The property was proved for prime exponentiation but not for elliptic curves"],
   "The book speaks of functions that are infeasible to calculate in the opposite direction using the computers and algorithms available today, which is a statement about the present state of knowledge.")
it("DigitalSignature", "Understand",
   "Why can every full node check every signature without being trusted by anybody?",
   "Verification needs only the public key, the message and the signature, all of them public",
   ["Each node receives a copy of the signer's private key together with the transaction that it has to verify",
    "Nodes trust the miner who included the transaction in a block",
    "The signature contains the private key in an encrypted form"],
   "A signature can only be produced with the private key but can be verified by anyone who has the public key and the transaction.")
it("DigitalSignature", "Analyze",
   "What does a signature on a transaction fail to tell a verifier?",
   "Who the signer is, beyond the fact that they hold the matching private key",
   ["Whether the signature belongs to that particular message",
    "Whether the public key and the signature really do correspond to one another",
    "Whether the message was altered after it was signed"],
   "A signature proves control of the key, not the identity of its holder, which is the privacy aim the chapter begins with.")
ap("PrivateKey", "432420386565659656852420866394968145599",
   "n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141\nprint(2 ** 256 - n)",
   ["0", "115792089237316195423570985008687907852837564279074904382605163141518161494337",
    "1461501637330902918203684832716283019655932542976"],
   "The order of the curve is slightly smaller than 2 to the 256, and the difference is this 39-digit number, which is how many 256-bit values are not valid private keys.")
it("PrivateKey", "Understand",
   "Which numbers may a Bitcoin private key be?",
   "Any number from 1 to n minus 1, where n is the order of the curve",
   ["Any 256-bit number without exception, including zero",
    "Any prime number below 2 to the 256",
    "Any number below p, which is the prime that defines the finite field"],
   "The book says the private key can be any number between 0 and n minus 1, and a key of zero is useless because zero times the generator is the point at infinity.")
it("PrivateKey", "Analyze",
   "Why does the enormous size of the key space not by itself make a key safe?",
   "A key drawn from a predictable source can be guessed in far fewer tries",
   ["Keys larger than n are rejected, which halves the usable space",
    "An attacker who already knows the public key can halve the search by using the symmetry",
    "The space shrinks every time another user generates a key"],
   "The book warns that any process that is less than completely random can significantly reduce the security of the key, whatever the size of the space.")
ap("PublicKey", "'03'",
   "y = 0x07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB\nprint(repr('03' if y % 2 else '02'))",
   ["'02'", "'04'", "'0279'"],
   "The last hexadecimal digit of this y coordinate is B, which is odd, so the compressed form of the key starts with the prefix 03.")
it("PublicKey", "Remember",
   "How is a public key obtained from a private key?",
   "By multiplying the generator point of the curve by the private key",
   ["By hashing the private key with SHA256 and then with RIPEMD-160",
    "By encoding the private key in base58check with the version byte 0x80",
    "By adding the private key to the order of the curve"],
   "The relation is K = k times G, where k is the private key, G the generator point and K the resulting public key.")
it("PublicKey", "Analyze",
   "Why is an address, and not a public key, the thing a receiver usually hands over?",
   "A public key is long and error-prone to dictate or copy",
   ["A public key would let the payer spend the receiver's earlier coins",
    "Public keys change with every block, so they cannot be written down",
    "Nodes reject outputs that contain a public key in any form"],
   "The book pictures Bob reading two 64-digit coordinates to Alice over the phone, which is the practical problem that the later sections solve.")
it("RandomSource", "Understand",
   "Why does the chapter treat the source of a key's randomness as more important than the key itself?",
   "A key from a predictable or repeatable source can be guessed whatever it looks like",
   ["A key from a slow source is more expensive to generate than one from a fast source",
    "Only a key generated on a node that is fully synchronised is accepted by the network",
    "Keys from different sources have different lengths, which wallets must agree on"],
   "The first and most important step in generating keys is a secure source of randomness, because an unpredictable source is what the size of the key space relies on.")
ap("Entropy", "77.06",
   "import math\nprint(round(math.log10(2 ** 256), 2))",
   ["256.0", "78.0", "38.53"],
   "Two to the 256 is about ten to the 77, which is the order of magnitude the book gives for the size of the key space.")
it("Entropy", "Analyze",
   "A generator prints a 256-bit key but seeds itself from the current second. How much entropy does the key have?",
   "About as much as the number of possible seconds, far less than 256 bits",
   ["256 bits, because the output is 256 bits long",
    "128 bits, because passing a value through a hash function halves the entropy of its input",
    "No entropy at all, because the key is a fixed number"],
   "A formula can only stretch the entropy that already exists, so the key is only as unpredictable as its seed.")
ap("SecureRandomness", "True",
   "import secrets\nn = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141\nk = secrets.randbelow(n - 1) + 1\nprint(1 <= k < n)",
   ["False", "None", "0"],
   "Asking for a number below n minus 1 and adding one gives a value from 1 to n minus 1, which is exactly the range of a valid private key.")
it("SecureRandomness", "Understand",
   "What does Python's documentation say about the default generator of its random module?",
   "It is designed for modelling and simulation, not for security or cryptography",
   ["It is cryptographically secure as long as the program seeds it from the clock of the system",
    "It is the same generator as the one in the secrets module",
    "It is secure for keys but not for passwords"],
   "The documentation of the secrets module says it should be used in preference to the default generator of the random module, which is designed for modelling and simulation.")

# ============================================================================================================
# 2  THE CURVE AND THE HASH FUNCTIONS
# ============================================================================================================
it("Curve", "Understand",
   "Why does the chapter spend a whole group of concepts on one elliptic curve?",
   "Every claim that a public key does not reveal its private key rests on that curve's properties",
   ["Each Bitcoin user may choose a different curve, so all of them must be described",
    "The curve has to be recomputed whenever the difficulty of mining changes",
    "Wallets store the parameters of the curve they use in the blockchain, so every reader must look them up there"],
   "A reader who wants to judge the security of Bitcoin cannot treat the conversion from private to public key as a black box.")
ap("FiniteField", "7",
   "print(pow(5, -1, 17))",
   ["12", "3", "5"],
   "Five times seven is 35, which leaves the remainder one when divided by 17, so seven is the multiplicative inverse of five in the field with 17 elements.")
it("FiniteField", "Analyze",
   "Why is Bitcoin's curve defined over a finite field instead of over the real numbers?",
   "Arithmetic modulo a prime is exact, while a computer would have to round real numbers",
   ["A finite field turns the curve into a smooth line, which is far easier to draw and to explain",
    "Real numbers would make the private keys longer than 256 bits",
    "Only finite fields allow a point to be added to itself"],
   "The price of exactness is that the curve becomes a scatter of dots, but the book notes that the mathematics is identical.")
ap("EllipticCurve", "17",
   "print(sum(1 for x in range(17) for y in range(17) if (y * y - x ** 3 - 7) % 17 == 0))",
   ["18", "16", "289"],
   "Over the field with 17 elements the curve has 17 points with whole-number coordinates, and the point at infinity makes 18 in all.")
it("EllipticCurve", "Remember",
   "What is the equation of the curve that Bitcoin uses?",
   "y squared equals x cubed plus 7, taken modulo a large prime p",
   ["y equals x cubed plus 7, taken modulo a large prime p",
    "y squared equals x squared plus 7, taken modulo a large prime p",
    "y squared equals x cubed plus x plus 7, taken modulo a large prime p"],
   "The book writes the curve as y squared mod p equals x cubed plus 7 mod p, so the coefficient a is zero and b is seven.")
ap("PointAddition", "(1, 12)",
   "p = 17\na, b = (1, 5), (2, 7)\nm = (b[1] - a[1]) * pow(b[0] - a[0], -1, p) % p\nx = (m * m - a[0] - b[0]) % p\nprint((x, (m * (a[0] - x) - a[1]) % p))",
   ["(2, 10)", "(1, 5)", "(3, 12)"],
   "Adding the points (1, 5) and (2, 7) of the small curve gives (1, 12), which is the mirror image of (1, 5) in the x axis.")
it("PointAddition", "Understand",
   "What is the result of adding two points that have the same x value and different y values?",
   "The point at infinity, which plays the role of zero",
   ["The point with x doubled and y unchanged",
    "The generator point of the curve",
    "An error, because such a pair cannot be added"],
   "The line through two such points is vertical, and the book introduces the point at infinity exactly for this case.")
ap("Secp256k1", "0",
   "p = 2 ** 256 - 2 ** 32 - 977\nx = 55066263022277343669578718895168534326250603453777594175500187360389116729240\ny = 32670510020758816978083085130507043184471273380659243275938904335757337482424\nprint((x ** 3 + 7 - y ** 2) % p)",
   ["1", "7", "17"],
   "The remainder is zero, which is what it means for the point to satisfy the curve equation, and it reproduces the book's own Python check.")
it("Secp256k1", "Analyze",
   "The book says the secp256k1 curve was established by NIST. What do the primary sources show?",
   "It is defined in SEC 2 by Certicom Research, which marks it as not on the NIST list",
   ["It was established by NIST in 2010 together with secp256r1",
    "It was established by the Bitcoin developers and was later adopted unchanged by NIST",
    "It has no written standard, only an implementation in libsecp256k1"],
   "SEC 2's status table marks secp256k1 with a dash in the NIST column and secp256r1 with an r for explicitly recommended.")
ap("CurveStandard", "[('secp256k1', '-'), ('secp256r1', 'r')]",
   "table = [('secp224k1', '-'), ('secp224r1', 'r'), ('secp256k1', '-'), ('secp256r1', 'r')]\nprint([row for row in table if row[0].startswith('secp256')])",
   ["[('secp256k1', 'r'), ('secp256r1', '-')]", "[('secp256k1', 'c'), ('secp256r1', 'c')]",
    "[('secp224k1', '-'), ('secp224r1', 'r')]"],
   "In the NIST column of the standard's alignment table a dash means not conformant and an r means explicitly recommended.")
it("CurveStandard", "Understand",
   "What do the letters k and r in a name such as secp256k1 or secp256r1 denote?",
   "A Koblitz curve and verifiably random parameters",
   ["A key curve and a reference curve",
    "A kilobit field and a reduced field",
    "A Korean and a Russian national standard"],
   "The standard explains that each name carries sec, then p for a prime field, the field size in bits, then k or r, then a sequence number.")
ap("GeneratorPoint", "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798",
   "x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798\ny = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8\nprint(('02' if y % 2 == 0 else '03') + format(x, '064x'))",
   ["0379be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798",
    "0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798",
    "79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"],
   "The generator's y coordinate is even, so its compressed encoding carries the prefix 02, exactly as the standard prints it.")
it("GeneratorPoint", "Analyze",
   "Why are the valid private keys the numbers from 1 to n minus 1 and no larger?",
   "Adding the generator to itself n times reaches the point at infinity, so larger keys only repeat",
   ["Numbers above n minus 1 do not fit into 256 bits",
    "The standard forbids them so that every wallet in the network agrees on the length of a private key",
    "Numbers above n minus 1 give points that are not on the curve"],
   "The multiples of the generator form a loop of exactly n members, so a multiplier beyond n minus 1 gives a public key that some smaller multiplier already gives.")
ap("PointMultiplication", "(252, 123)",
   "k = 0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD\nprint((k.bit_length() - 1, bin(k).count('1') - 1))",
   ["(253, 124)", "(256, 128)", "(123, 252)"],
   "The double-and-add method doubles once for every bit after the leading one and adds once for every further bit that is set, so this key needs 252 doublings and 123 additions.")
it("PointMultiplication", "Understand",
   "Why is multiplying a point by a 256-bit number practical at all?",
   "Double-and-add reads the bits of the multiplier and needs only a few hundred steps",
   ["Libraries keep a table of all possible multiples of the generator",
    "The multiplier is reduced modulo 256 before the calculation",
    "The result is simply read from the blockchain, in which every public key that exists is stored"],
   "Adding the generator to itself k times would be impossible, so software doubles the running point for each bit and adds the point where the bit is one.")
ap("DiscreteLogarithm", "9",
   "print(next(k for k in range(1, 101) if pow(2, k, 101) == 7))",
   ["7", "101", "11"],
   "Finding the exponent requires trying candidates one after another, and the search stops at nine, while computing two to the ninth modulo 101 is a single step.")
it("DiscreteLogarithm", "Analyze",
   "The book says finding k from K is as hard as trying every value of k. How should that be read?",
   "As a simplification: the standard puts the strength of the curve at 128 bits, not 256",
   ["As a proof that no better algorithm can ever exist",
    "As a claim that the search takes exactly 2 to the 256 steps on any computer ever built",
    "As a statement about the prime p rather than about the order n"],
   "The security strength that SEC 2 gives for secp256k1 is 128 bits for a 256-bit field, which is half of what a search over every key would mean.")
ap("CryptoLibrary", "True",
   "src = 'def ec_add(a, b):\\n    pass\\ndef ec_mul(k, pt):\\n    pass'\nprint(len(src.splitlines()) < 20)",
   ["False", "4", "20"],
   "The point addition and multiplication of the chapter's teaching toolkit take thirteen lines in all, which is well under twenty, and a real library does the same arithmetic with far more care.")
it("CryptoLibrary", "Analyze",
   "Why does the chapter's toolkit say that it must not be used with real funds?",
   "It is not constant-time and takes no care over where randomness comes from",
   ["It gives addresses that differ from the ones Bitcoin Core gives for the same private key",
    "It cannot compute the public key of a 256-bit private key",
    "It has no licence that permits use outside teaching"],
   "Its own description names those two limits, which is why it is only a readable sketch of what a library such as libsecp256k1 does.")
it("Hashing", "Understand",
   "What problem do hash functions solve in this chapter?",
   "Referring to a large object by a short value without losing the guarantee of identity",
   ["Hiding the amount of a payment from the nodes that verify it",
    "Compressing the blockchain so that a pruned node can store it",
    "Turning a public key back into the private key from which it was once produced, if needed"],
   "The book notes that Bitcoin contains data structures much larger than 65 bytes that must be referenced with the smallest amount of data that is secure.")
ap("HashFunction", "139",
   "import hashlib\na = int(hashlib.sha256(b'a').hexdigest(), 16)\nb = int(hashlib.sha256(b'`').hexdigest(), 16)\nprint(bin(a ^ b).count('1'))",
   ["128", "1", "256"],
   "The two inputs differ by a single bit, yet 139 of the 256 output bits differ, a little more than half, so a near miss reveals nothing about the right input.")
it("HashFunction", "Analyze",
   "Why would the book's commitment game be broken if the answer could only be one of a few years?",
   "Anyone could hash every candidate and compare it with the published value",
   ["The hash of a short input is shorter and therefore easier to invert",
    "A hash function gives nearly the same output for two inputs that are close together",
    "The answerer could change the answer after publishing the hash"],
   "A commitment binds its author, but it hides the hidden value only when the set of possible values is huge.")
ap("Sha256", "ba7816bf",
   "import hashlib\nprint(hashlib.sha256(b'abc').hexdigest()[:8])",
   ["8eb208f7", "94d7a772", "bbc1e42a"],
   "The SHA256 digest of the three bytes abc begins ba7816bf, and the function always gives the same 32 bytes for the same input.")
it("Sha256", "Understand",
   "Why does a 256-bit output not mean 256 bits of security against every attack?",
   "Finding two inputs with the same hash costs about the square root of the output space",
   ["Half of the output bits are discarded by Bitcoin's scripts",
    "The function is applied twice, which halves its strength",
    "A 256-bit output has only 128 bits in it that are genuinely random and quite unpredictable"],
   "For collisions the work is about the square root, so a 256-bit function offers about 128 bits and a 160-bit one about 80.")
ap("Ripemd160", "(20, 160)",
   "d = 'bbc1e42a39d05a4cc61752d6963b7f69d09bb27b'\nprint((len(bytes.fromhex(d)), len(bytes.fromhex(d)) * 8))",
   ["(40, 320)", "(32, 256)", "(20, 20)"],
   "A RIPEMD-160 digest is 20 bytes, which is 160 bits, written as 40 hexadecimal digits.")
it("Ripemd160", "Remember",
   "Where does RIPEMD-160 appear in Bitcoin, according to the chapter?",
   "As the second step of the commitment to a public key or to a script",
   ["As the function that produces the checksum of base58check",
    "As the function that produces a transaction identifier",
    "As the function that turns a private key into the public key that belongs to it"],
   "The commitments of the legacy addresses and of a version 0 witness public key hash are the RIPEMD-160 of a SHA256 digest.")
ap("Hash160", "(20, 20, False)",
   "c = 'bbc1e42a39d05a4cc61752d6963b7f69d09bb27b'\nu = '211b74ca4686f81efda5641767fc84ef16dafe0b'\nprint((len(bytes.fromhex(c)), len(bytes.fromhex(u)), c == u))",
   ["(20, 20, True)", "(32, 32, False)", "(40, 40, False)"],
   "Both commitments are 20 bytes, but they differ, because the compressed and the uncompressed encoding of the same key are different byte strings.")
it("Hash160", "Analyze",
   "Why does one private key lead to two different legacy addresses?",
   "HASH160 commits to bytes, and the key has two different byte encodings",
   ["The key is hashed once for mainnet and once for testnet",
    "The address includes a counter that increases with every use",
    "The two addresses carry one and the same commitment but two different checksums"],
   "The compressed and the uncompressed public key are two encodings of one point, and hashing them gives two different 20-byte values.")

# ============================================================================================================
# 3  FORMAT
# ============================================================================================================
it("Format", "Understand",
   "Why does the chapter treat the way a number is written down as a matter of safety?",
   "A mistake in copying a commitment sends the coins to an output nobody can spend",
   ["A longer representation takes up more space in a block and therefore raises the fee",
    "A badly chosen alphabet makes the private key easier to guess",
    "Only one representation is accepted by the consensus rules"],
   "The book says that any mistake made in copying a commitment would result in the bitcoins being sent to an unspendable output and lost forever.")
it("Representation", "Remember",
   "Which three basic notions does the representation group gather?",
   "Bits and bytes, the number base, and the two-dimensional barcode",
   ["The private key, the public key and the address",
    "The version byte, the payload and the checksum",
    "Binary, decimal and Roman numerals"],
   "Lengths are counted in bits and bytes, hexadecimal and base58 are number bases, and the barcode decides how an address is shared between wallets.")
ap("BitsAndBytes", "(520, 264)",
   "print((65 * 8, 33 * 8))",
   ["(130, 66)", "(512, 256)", "(65, 33)"],
   "An uncompressed public key of 65 bytes is 520 bits and a compressed one of 33 bytes is 264 bits, the figures the book prints.")
it("BitsAndBytes", "Analyze",
   "A student reads that a key is 64 hexadecimal digits and concludes it is 64 bytes. What is the error?",
   "Each hexadecimal digit carries 4 bits, so 64 digits are 32 bytes",
   ["A hexadecimal digit carries eight bits, so 64 of them are indeed 64 bytes",
    "A key is 64 bytes but only 32 of them are used",
    "Hexadecimal digits cannot be counted in bytes at all"],
   "Two hexadecimal digits make one byte, so 64 digits are 32 bytes, which is the 256 bits of a private key.")
ap("NumberBase", "(255, 255)",
   "print((int('ff', 16), int('11111111', 2)))",
   ["(255, 8)", "(16, 2)", "(170, 255)"],
   "The same value can be written in any base: ff in base 16 and 11111111 in base 2 both stand for 255.")
it("NumberBase", "Understand",
   "Which characters does base58 leave out of the base64 alphabet, and why?",
   "Zero, capital O, lower l, capital I and the symbols plus and slash, which are easily confused",
   ["The vowels, so that no address can spell a word",
    "The digits from 1 to 9, so that no address can ever begin with a number rather than with a letter",
    "The capital letters, so that an address can be read aloud"],
   "Base58 is base64 without the characters that are frequently mistaken for one another in certain fonts, together with the two symbols.")
ap("QrCode", "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee",
   "print('BC1Q9D3XA5GG45Q2J39M9Y32XZVYGCGAY4RGC6AAEE'.lower())",
   ["BC1Q9D3XA5GG45Q2J39M9Y32XZVYGCGAY4RGC6AAEE", "bc1Q9d3Xa5gg45Q2j39M9y32Xzvygcgay4Rgc6Aaee",
    "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaff"],
   "An uppercase bech32 address is the same address: the lowercase form is what an encoder must output, and uppercase is used only for presentation and inside QR codes.")
it("QrCode", "Understand",
   "Why is the uppercase form of a bech32 address used inside a QR code?",
   "It permits the alphanumeric mode, which is about 45 percent more compact than byte mode",
   ["It is the only form that a camera can read reliably",
    "It hides the address from anyone who photographs the code",
    "It allows a longer address to be encoded within the same number of modules of the picture"],
   "The specification says uppercase should be used inside QR codes because the alphanumeric mode is 45 percent more compact than the normal byte mode.")
it("KeyEncoding", "Understand",
   "Why must two wallets agree on the encoding of a key they exchange?",
   "A wallet that scans for the wrong kind of key may miss part of the balance",
   ["An encoding that is not agreed makes the key invalid for the curve",
    "The encoding decides whether the key may be used on the main network or on testnet",
    "A wrongly encoded key changes the private number it stands for"],
   "The book explains that an importing wallet must know whether to scan for 65-byte keys and their commitments or for 33-byte keys and theirs.")
ap("CompressedPublicKey", "0.492",
   "print(round(1 - 33 / 65, 3))",
   ["0.508", "0.5", "0.33"],
   "Dropping the y coordinate saves 49.2 percent of the bytes of a public key, which the book calls an almost 50 percent reduction.")
it("CompressedPublicKey", "Understand",
   "What does the prefix byte of a compressed public key say?",
   "Whether the y coordinate is even, with 02, or odd, with 03",
   ["Whether the key is for mainnet, with 02, or testnet, with 03",
    "Whether the key belongs to a P2PKH or to a P2WPKH output",
    "How many bytes of the x coordinate follow"],
   "Knowing x leaves two possible values of y, one even and one odd, and the prefix settles which of them it is.")
ap("UncompressedPublicKey", "65",
   "k = '04F028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB'\nprint(len(bytes.fromhex(k)))",
   ["130", "33", "64"],
   "The prefix 04 followed by two 32-byte coordinates is 65 bytes, written as 130 hexadecimal digits.")
it("UncompressedPublicKey", "Analyze",
   "Why does some software still have to support uncompressed public keys?",
   "Keys imported from older wallets were used in that form and their outputs must be found",
   ["Uncompressed keys are required for every taproot output",
    "The consensus rules reject compressed public keys in every legacy output script that uses them",
    "Only uncompressed keys can be printed as a QR code"],
   "A wallet that imports a private key from an older wallet has to scan the blockchain for the right kind of key, or the user cannot spend the full balance.")
ap("WalletImportFormat", "5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn",
   ("import hashlib\n"
    "B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\n"
    "d = bytes.fromhex('80' + '1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD')\n"
    "d += hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]\n"
    "n = int.from_bytes(d, 'big')\n"
    "s = ''\n"
    "while n:\n"
    "    n, r = divmod(n, 58)\n"
    "    s = B58[r] + s\n"
    "print(s)"),
   ["KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ",
    "1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy",
    "6PRHv1jg1ytiE4kT2QtrUz8gEjMQghZDWg1FuxjdYDzjUkcJeGdFj9q9Vi"],
   "The version byte 0x80, the 32-byte key and four checksum bytes written in base58 give the book's uncompressed WIF string, which starts with 5.")
it("WalletImportFormat", "Remember",
   "What does the wallet import format add to the raw bytes of a private key?",
   "A version byte in front, a checksum behind, and base58 for the whole",
   ["A passphrase and a salt derived from the address",
    "The matching public key, so that both can travel together",
    "A timestamp, so that an importing wallet knows when to start its rescan"],
   "The format is the base58check encoding of version 0x80 and the key, with a 0x01 byte added for keys that produce compressed public keys.")
ap("CompressedPrivateKey", "1",
   "print(len('KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ') - len('5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn'))",
   ["0", "-1", "2"],
   "The so-called compressed form is one character longer, because a byte was added, which is why the book calls the name a misnomer.")
it("CompressedPrivateKey", "Analyze",
   "What does the byte 0x01 at the end of a WIF-compressed key actually say?",
   "That only compressed public keys should be derived from this key",
   ["That the key itself has been compressed into a smaller number of bits",
    "That the key belongs to a deterministic wallet",
    "That the key may be used only once"],
   "Private keys are not themselves compressed and cannot be; the suffix is a message to the importing wallet about which public keys to expect.")
it("Checksummed", "Understand",
   "What does a checksum in an address format buy the user?",
   "A mistyped address is refused instead of being paid",
   ["A payment to a wrong address can be reversed within one block",
    "The address becomes shorter and easier to read aloud",
    "The receiver learns who sent the payment"],
   "The wallet recomputes the check and refuses an address that does not match, which prevents a loss that could not otherwise be undone.")
ap("Checksum", "True",
   ("import hashlib\n"
    "B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\n"
    "a = '1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy'\n"
    "n = 0\n"
    "for ch in a:\n"
    "    n = n * 58 + B58.index(ch)\n"
    "raw = n.to_bytes(25, 'big')\n"
    "print(hashlib.sha256(hashlib.sha256(raw[:21]).digest()).digest()[:4] == raw[21:])"),
   ["False", "None", "25"],
   "The last four bytes of the decoded address are exactly the first four bytes of the double SHA256 of the rest, which is what a valid base58check string means.")
it("Checksum", "Analyze",
   "Against what does a checksum give no protection at all?",
   "Someone who replaces the whole address and computes a matching checksum",
   ["A character that was transposed with its neighbour",
    "A single character that was mistyped as another one that looks similar to it",
    "A digit that was dropped during dictation"],
   "A checksum detects accident, not attack: the address of a different person passes every check.")
ap("Base58Check", "c47e83ff",
   ("import hashlib\n"
    "d = bytes.fromhex('80' + '1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD')\n"
    "print(hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4].hex())"),
   ["ba7816bf", "bbc1e42a", "2bc830a3"],
   "The four checksum bytes of the book's uncompressed WIF are the first four bytes of the double SHA256 of the version byte and the key.")
it("Base58Check", "Analyze",
   "Which weaknesses of base58check did the designers of bech32 list?",
   "A slow checksum without guarantees, mixed case, and complicated decoding",
   ["A short alphabet, a missing version byte, and no support for scripts of any kind",
    "A checksum that cannot be computed without a node",
    "An alphabet that varies between implementations"],
   "The bech32 proposal names the double SHA256 checksum without error-detection guarantees, the mixed case and the complicated decoding among its reasons.")
it("VersionPrefix", "Remember",
   "Which first character does the version byte 0x05 produce in base58check?",
   "The digit 3, which marks a P2SH address",
   ["The digit 1, which marks a P2PKH address",
    "The letter m or n, which marks a testnet address",
    "The digit 5, which marks a private key in WIF"],
   "The book's table pairs 0x00 with 1, 0x05 with 3, 0x6F with m or n, 0xC4 with 2 and 0x80 with 5, K or L.")
it("VersionPrefix", "Analyze",
   "Why does the leading character of a base58check string follow from the version byte?",
   "The version byte is the most significant part of the number that is written in base 58",
   ["The alphabet is ordered in such a way that each separate type of data has its own first letter",
    "The encoder writes the type's name before the data",
    "The checksum is computed over the version byte alone"],
   "The prefix is not a separate field: its value decides the first digit or digits of the number when it is written in base 58.")
ap("NetworkSelector", "('bc', 'tb')",
   "main = 'bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'\ntest = 'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx'\nprint((main[:2], test[:2]))",
   ["('bc1', 'tb1')", "('1', 'm')", "('bt', 'tb')"],
   "The human-readable part names the network: bc for the main network and tb for testnet.")
it("NetworkSelector", "Analyze",
   "Why does replacing bc by tb in a valid address not give a valid testnet address?",
   "The human-readable part is mixed into the checksum, so the checksum no longer matches",
   ["An address for testnet is always two characters longer than the matching mainnet address",
    "Testnet uses base58check and not bech32",
    "The witness version has to change with the network"],
   "The checksum covers the human-readable part as well as the data, which is why an address cannot be moved between networks by editing its prefix.")

# ============================================================================================================
# 4  ADDRESS: SCRIPTS AND THE LEGACY KINDS
# ============================================================================================================
it("Address", "Understand",
   "What is an address, in the terms this chapter uses?",
   "A short string from which a payer's wallet can build the right output script",
   ["An account at a wallet provider that holds a balance",
    "The public key of the receiver of the payment, written out in hexadecimal digits",
    "A number that the network assigns to each user once"],
   "Each kind of address is a convenient way of writing down what an output script contains, and it says nothing about who owns the funds.")
it("Address", "Analyze",
   "Why is a valid address no promise that the coins sent to it can be spent?",
   "A wallet accepts a well-formed address even if its owner has lost the key",
   ["Addresses expire after a fixed number of blocks",
    "An address can be used only once before it becomes invalid",
    "The nodes verify the identity of the owner before they accept a payment to the address"],
   "The checks built into an address kind reduce the chance of paying a wrong string, but they say nothing about the receiver's ability to spend.")
it("Scripts", "Remember",
   "What did the first version of Bitcoin put in place of a bare public key and signature?",
   "An output script that locks the funds and an input script that unlocks them",
   ["A pair of addresses, one of them for the payer and the other for the receiver",
    "A witness structure separate from the transaction",
    "A redeem script hashed into the transaction identifier"],
   "The book explains that payments were sent to a field called the output script and spends authorised by a field called the input script.")
ap("OutputScript", "25",
   "print(len(bytes.fromhex('76a914bbc1e42a39d05a4cc61752d6963b7f69d09bb27b88ac')))",
   ["22", "20", "34"],
   "A P2PKH output script is 25 bytes: two opcodes, a push of 20 bytes, the commitment, and two more opcodes.")
it("OutputScript", "Analyze",
   "Why does the book warn against assembling a P2SH output script by hand?",
   "Anything but the exact template makes the coins unspendable or spendable by anyone",
   ["A script written by hand is rejected by the relay policy of every node on the network",
    "The script must be signed by the receiver before it can be used",
    "A hand-written script cannot be encoded as an address"],
   "If the output script is not exactly OP_HASH160, 20 bytes and OP_EQUAL, the redeem script is not used, with the loss the book describes.")
ap("InputScript", "('<Bob public key>', '<Bob signature>', 2)",
   "stack = ['<Bob signature>', '<Bob public key>']\nprint((stack[-1], stack[0], len(stack)))",
   ["('<Bob signature>', '<Bob public key>', 2)", "('<Bob public key>', '<Bob signature>', 1)",
    "('<Bob signature>', '<Bob signature>', 2)"],
   "The data of the input script is pushed first, the signature before the public key, so the public key ends up on top of the stack.")
it("InputScript", "Understand",
   "What does an output that commits to a hash of a key keep hidden until it is spent?",
   "The public key itself, which appears for the first time in the input script",
   ["The amount of the output, which only the spender of that output reveals later",
    "The address, which the payer learns only from the spend",
    "The signature, which is created when the output is made"],
   "The separation of the two scripts lets the receiver keep the key private until the moment of spending, when a node checks it against the commitment.")
ap("StackExecution", "['sig', 'pub', 'pub']",
   "stack = ['sig', 'pub']\nstack.append(stack[-1])\nprint(stack)",
   ["['sig', 'pub']", "['pub', 'sig', 'pub']", "['sig', 'sig', 'pub']"],
   "OP_DUP duplicates the top item of the stack, which in the P2PKH script leaves the public key on the stack twice.")
it("StackExecution", "Understand",
   "When does the script machine consider a script to have passed?",
   "When a nonzero item is on top of the stack at the end of evaluation",
   ["When the stack is completely empty at the end",
    "When every opcode of the output script has been executed at least once",
    "When the input script and the output script have the same length"],
   "The book says that if there is a nonzero item on top of the stack at the end, the script passes, and a transaction is valid when all its scripts pass.")
it("StackExecution", "Analyze",
   "The book prints OP_EQUAL in one P2PKH script and OP_EQUALVERIFY in the next. Which does the real script use?",
   "OP_EQUALVERIFY, which stops the script if the two items differ",
   ["OP_EQUAL, because it leaves a truth value for OP_CHECKSIG to read",
    "Either one, because the two opcodes have the same byte value",
    "Neither: the comparison is made by OP_CHECKSIG itself"],
   "The combined script the book prints and the script that Bitcoin Core reports for such an address both use OP_EQUALVERIFY, whose value is 0x88.")
it("Legacy", "Remember",
   "Which two script templates are the only ones used with base58check?",
   "Pay to public key hash and pay to script hash",
   ["Pay to public key and pay to witness public key hash",
    "Pay to script hash and pay to taproot",
    "Pay to public key hash and pay to witness script hash"],
   "The book says P2PKH and P2SH are the only two templates used with base58check and that they are now known as legacy addresses.")
it("Legacy", "Analyze",
   "Why does the book recommend newer address types although it sees no immediate threat to P2SH?",
   "Cost, convenience and a theoretical collision risk, which a longer commitment removes",
   ["Legacy addresses will stop being valid after the next soft fork",
    "Legacy addresses cannot be used with deterministic wallets",
    "A legacy address reveals the public key that stands behind it as soon as the address is created"],
   "The book states that there is no immediate threat to anyone creating new P2SH addresses but recommends newer types to eliminate the concern.")
ap("IpAddressPayment", "(32, 4294967296)",
   "octets = 4\nprint((octets * 8, 2 ** (octets * 8)))",
   ["(4, 16)", "(32, 4294967295)", "(8, 256)"],
   "An Internet Protocol address of four octets is 32 bits long, which is why there are about four thousand million of them.")
it("IpAddressPayment", "Understand",
   "Which good idea of the payment by IP address survived its removal?",
   "A fresh public key for every payment, so that payments cannot be linked",
   ["Sending the amount in the address itself",
    "Letting the payer choose the receiver's script",
    "Confirming the payment directly between the two nodes without any block"],
   "The receiver's node gave a key it had never given before, and later address kinds reach the same effect without needing the receiver to be online.")
ap("P2pk", "[1]",
   "stack = ['<Bob signature>', '<Bob public key>']\nstack.pop()\nstack.pop()\nstack.append(1)\nprint(stack)",
   ["[0]", "['<Bob signature>']", "[1, 1]"],
   "OP_CHECKSIG consumes the public key and the signature and replaces itself with 1 when the signature is correct, which leaves a nonzero item on top.")
it("P2pk", "Analyze",
   "What is the main cost of a pay to public key output?",
   "The whole public key sits in the output from the start, 65 bytes in the early encoding",
   ["The spender of the output has to provide two separate signatures for it instead of only one",
    "The output cannot be spent before 100 blocks have passed",
    "The receiver has to publish the output script in advance"],
   "P2PK gives up the protection a hash provides and makes the output as long as the key, against the 20 bytes of a commitment.")
ap("Commitment", "94d7a772612c8f2f2ec609d41f5bd3d04a5aa1dfe3582f04af517d396a302e4e",
   "import hashlib\nprint(hashlib.sha256(b'2007.  He said about a year and a half before Oct 2008\\n').hexdigest())",
   ["94d7a772612c8f2f2ec609d41f5bd3d04a5aa1dfe3582f04af517d396a302e4f",
    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    "bbc1e42a39d05a4cc61752d6963b7f69d09bb27b"],
   "This reproduces the book's commitment exactly, including the line break that the echo command adds to the sentence.")
it("Commitment", "Understand",
   "What makes the output of a hash function a commitment to its input?",
   "The same input always gives it, and finding another input that gives it is impractical",
   ["It can be decrypted back into the input with the right key",
    "It is always shorter than the input itself and is therefore very much easier to publish",
    "It is signed by the party that publishes it"],
   "Those two properties make the output a promise that, in practice, only input x will produce output X.")
ap("P2pkhAddress", "(0, 25)",
   ("B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\n"
    "a = '1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy'\n"
    "n = 0\n"
    "for ch in a:\n"
    "    n = n * 58 + B58.index(ch)\n"
    "raw = n.to_bytes(25, 'big')\n"
    "print((raw[0], len(raw)))"),
   ["(5, 25)", "(0, 20)", "(1, 34)"],
   "Decoding the address gives 25 bytes whose first is the version byte zero, which marks a legacy pay to public key hash output.")
it("P2pkhAddress", "Understand",
   "What does a P2PKH address let Alice send instead of Bob's public key?",
   "A 20-byte commitment to the key instead of 65 bytes of key",
   ["The key in a compressed form of 33 bytes",
    "The key's first four bytes together with a checksum",
    "A reference to the block in which Bob's key appeared"],
   "The book admits the scheme is convoluted but notes that it reduces what Bob has to communicate from 65 bytes to 20.")
ap("RedeemScript", "[20, 118, 169, 135, 136, 172]",
   "print([0x14, 0x76, 0xa9, 0x87, 0x88, 0xac])",
   ["[14, 76, 169, 87, 88, 172]", "[20, 118, 169, 135, 136, 173]", "[0, 20, 118, 169, 135, 136]"],
   "These are the byte values of a 20-byte push and of OP_DUP, OP_HASH160, OP_EQUAL, OP_EQUALVERIFY and OP_CHECKSIG, read as decimal numbers.")
it("RedeemScript", "Understand",
   "What does a spender have to put in the input script of a P2SH output?",
   "The data the script needs and the serialised redeem script itself",
   ["The private keys that the redeem script names",
    "Only the signatures, since the script itself is already in the output",
    "The address from which the output was created"],
   "Nodes first check that the serialised redeem script hashes to the commitment and then run it on the remaining stack.")
ap("MultisigScript", "(513, True)",
   "n = 15\nprint((3 + n * 34, 3 + (n + 1) * 34 > 520))",
   ["(510, True)", "(513, False)", "(520, True)"],
   "Fifteen compressed keys of 34 bytes plus three bytes of opcodes make 513 bytes, and a sixteenth key would pass the 520-byte limit on a data push.")
it("MultisigScript", "Analyze",
   "Why does a P2SH address not necessarily mean a multisignature script?",
   "The commitment hides any script, and multisignature is only the commonest one",
   ["Multisignature scripts always use a separate address type",
    "The address records how many keys the script names in its own first character",
    "Nodes reject multisignature scripts inside P2SH"],
   "The book says a P2SH address most often represents a multisignature script but might represent a script encoding other types of transaction.")
ap("P2shAddress", "5",
   ("B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\n"
    "a = '3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM'\n"
    "n = 0\n"
    "for ch in a:\n"
    "    n = n * 58 + B58.index(ch)\n"
    "print(n.to_bytes(25, 'big')[0])"),
   ["3", "0", "128"],
   "The version byte of a P2SH address is 5, which is what makes the encoded string begin with the digit 3.")
it("P2shAddress", "Remember",
   "What does the output script of a P2SH payment contain?",
   "OP_HASH160, a 20-byte commitment and OP_EQUAL, and nothing else",
   ["OP_DUP, OP_HASH160, a commitment, OP_EQUALVERIFY and OP_CHECKSIG",
    "A witness version byte followed by a 20-byte program",
    "The redeem script itself, followed by OP_EQUAL"],
   "The template is fixed, and the book warns that any extra data or condition makes the redeem script unusable.")
ap("PreimageAttack", "1461501637330902918203684832716283019655932542976",
   "print(2 ** 160)",
   ["1208925819614629174706176", "340282366920938463463374607431768211456",
    "115792089237316195423570985008687907853269984665640564039457584007908834671663"],
   "Two to the 160 is the number of possible outputs of HASH160, and the book gives one in that number as the chance of finding a preimage.")
it("PreimageAttack", "Understand",
   "What is an attacker looking for in a preimage attack on an address?",
   "Any input whose hash equals the commitment in an existing output",
   ["Two scripts that have the same hash as each other",
    "A private key whose public key hashes to a value of their choosing",
    "A second signature for a transaction that is already signed"],
   "The attacker has only the output and looks for an input that produces it, which for a secure 160-bit function means a chance of one in 2 to the 160.")
ap("SecondPreimageAttack", "6.842277657836021e-49",
   "print(float(1 / 2 ** 160))",
   ["6.842277657836021e-25", "8.636168555094445e-78", "0.0"],
   "The chance of hitting a given 160-bit output with one random attempt is one in 2 to the 160, which is this very small number.")
it("SecondPreimageAttack", "Analyze",
   "What does an attacker know in a second preimage attack that they do not know in a preimage attack?",
   "One input that produces the output, which does not help them find another",
   ["The private key behind the output",
    "The checksum of the address itself, which narrows down the search a little",
    "The order in which the inputs were hashed"],
   "The two attacks cost about the same for HASH160, and the difference is only the starting knowledge.")
ap("CollisionAttack", "True",
   "print((2 ** 160) ** 0.5 == 2 ** 80)",
   ["False", "1.2089258196146292e+24", "80"],
   "The work for a collision is about the square root of the output space, which for a 160-bit function is 2 to the 80.")
it("CollisionAttack", "Analyze",
   "When does the strength of HASH160 drop from 2 to the 160 to 2 to the 80?",
   "When the attacker can influence the input, for instance a shared multisignature script",
   ["When the same address is used for more than one payment",
    "When the public key that stands behind the address is compressed rather than uncompressed",
    "When the output is spent and the key becomes public"],
   "An attacker who submits their key only after learning the others' keys can search for two inputs at once, which is a collision attack.")

# ============================================================================================================
# 5  THE SEGWIT ADDRESSES
# ============================================================================================================
it("Segwit", "Understand",
   "Which practical question do the segwit address formats answer?",
   "How to give a payer a short string that works for new and for future output kinds",
   ["How to hide the amount of a payment from the nodes",
    "How to let a receiver spend without a private key",
    "How to make a transaction confirm in the block that comes next"],
   "Bech32 takes advantage of an upgrade mechanism so that a wallet built today can still pay the outputs of later protocol upgrades.")
it("Segwit", "Analyze",
   "Why does a valid bech32 address not guarantee that any wallet can pay it?",
   "The paying wallet must also recognise the format, and old wallets do not",
   ["The address is only ever valid on the single network whose name its prefix carries",
    "The address has to be registered with a node before use",
    "The address expires when the witness version changes"],
   "The book lists the need for every spender wallet to upgrade as one of the problems the designers wanted to reduce.")
ap("SegwitUpgrade", "('3116f499', 'd97ceb07')",
   ("import hashlib\n"
    "def dsha(b):\n"
    "    return hashlib.sha256(hashlib.sha256(b).digest()).hexdigest()[:8]\n"
    "nowit = b'the bytes of a transaction without its witness'\n"
    "print((dsha(nowit), dsha(nowit + b' and the witness bytes')))"),
   ["('3116f499', '3116f499')", "('d97ceb07', '3116f499')", "('ba7816bf', '94d7a772')"],
   "The two identifiers differ completely once the witness bytes are included, which is why the txid is computed without them and the wtxid with them.")
it("SegwitUpgrade", "Remember",
   "What does the segregated witness upgrade move into a separate structure?",
   "The scripts and signatures that authorise a spend",
   ["The amounts of the outputs",
    "The transaction identifiers of the inputs",
    "The commitment to the public key"],
   "The specification says the witness holds the data required to check validity but not the data that determines what the transaction does.")
it("SegwitUpgrade", "Analyze",
   "A student says segwit removes signatures from a transaction. What is wrong?",
   "Signatures are still transmitted and verified, only stored elsewhere and left out of the txid",
   ["Signatures are indeed removed from the transaction and replaced by one signature for the whole block",
    "Signatures remain in the input script but are no longer checked",
    "Signatures are kept only by the miner who produced the block"],
   "Transmission of signature data becomes optional only for a peer that merely wants to check that a transaction exists.")
ap("NestedSegwit", "('0014bbc1e42a39d05a4cc61752d6963b7f69d09bb27b', 22)",
   "h = 'bbc1e42a39d05a4cc61752d6963b7f69d09bb27b'\nprint((bytes([0, 20]).hex() + h, len(bytes.fromhex('0014' + h))))",
   ["('0014bbc1e42a39d05a4cc61752d6963b7f69d09bb27b', 20)",
    "('0020bbc1e42a39d05a4cc61752d6963b7f69d09bb27b', 22)",
    "('5120bbc1e42a39d05a4cc61752d6963b7f69d09bb27b', 22)"],
   "The redeem script of a nested segwit address is the witness output script itself: the version byte 00, the length 20 and the key hash, 22 bytes in all.")
it("NestedSegwit", "Understand",
   "What did nesting a witness program inside a P2SH address achieve?",
   "Receivers could use segwit before every paying wallet had upgraded",
   ["It made the transaction identifier shorter",
    "It removed the need to carry any checksum in the address",
    "It allowed a witness program longer than 40 bytes"],
   "Every wallet that could pay a P2SH address could pay the nested form, which is why the upgrade was designed to use that mechanism.")
ap("Bech32Address", "42",
   "print(len('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'))",
   ["62", "34", "41"],
   "A version 0 address for a 20-byte program is 42 characters long, and one for a 32-byte program is 62.")
it("Bech32Address", "Remember",
   "What do the two halves of the name bech32 stand for?",
   "BCH, the error detection algorithm, and the 32 characters of the alphabet",
   ["Bitcoin enhanced checksum and the 32 bytes of a program",
    "Base encoding for cryptographic hashes and 32 bits of checksum",
    "The initials of the authors and the year 2032"],
   "The book explains that bech contains the initials of the three discoverers of the cyclic code and 32 is the size of the alphabet.")
it("Bech32Address", "Analyze",
   "Which four characters does the bech32 alphabet leave out, and why?",
   "One, b, i and o, because they resemble other characters",
   ["Zero, O, l and I, as base58 does",
    "The vowels a, e, i and o, so that no address spells a word",
    "The digits 1, 2, 3 and 4, which are reserved for the version"],
   "The data part consists of alphanumeric characters excluding 1, b, i and o, and the character set was chosen to minimise visual ambiguity.")
ap("WitnessVersion", "(0, 1)",
   "charset = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'\nprint((charset.index('q'), charset.index('p')))",
   ["(1, 0)", "(0, 16)", "(16, 1)"],
   "The character q stands for the value 0, the first segwit version, and p for 1, the version of taproot.")
ap("WitnessVersion", "[0, 81, 82, 96]",
   "print([0x00 if v == 0 else 0x50 + v for v in (0, 1, 2, 16)])",
   ["[0, 1, 2, 16]", "[80, 81, 82, 96]", "[0, 81, 82, 95]"],
   "Witness version 0 is the byte 0x00, but versions 1 to 16 are the opcodes OP_1 to OP_16, the bytes 0x51 to 0x60, that is 81 to 96 in decimal.")
it("WitnessVersion", "Analyze",
   "Which mistake does the book warn about when turning an address into an output script?",
   "Writing version 1 as the byte 0x01 instead of the opcode byte 0x51",
   ["Writing the version after the program instead of before it",
    "Writing the version in decimal instead of hexadecimal",
    "Leaving out the length byte before the program"],
   "A wrong byte here produces an output that is likely to be unspendable or insecure, as the specification also warns.")
ap("WitnessProgram", "(20, 32)",
   "p20 = '2b626ed108ad00a944bb2922a309844611d25468'\np32 = '648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f'\nprint((len(bytes.fromhex(p20)), len(bytes.fromhex(p32))))",
   ["(40, 64)", "(22, 34)", "(20, 20)"],
   "For witness version 0 the program must be exactly 20 or 32 bytes, which is what distinguishes a key hash from a script hash.")
it("WitnessProgram", "Remember",
   "How long may a witness program be in general?",
   "Between 2 and 40 bytes",
   ["Between 20 and 32 bytes",
    "Exactly 32 bytes for every version",
    "Between 1 and 64 bytes"],
   "The general range is 2 to 40 bytes, and version 0 narrows it to 20 or 32.")
ap("HumanReadablePart", "bc",
   "print('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'.rpartition('1')[0])",
   ["bc1", "tb", "bc1q"],
   "Everything before the last 1 of the string is the human-readable part, and for the main network it is bc.")
it("HumanReadablePart", "Understand",
   "Why was the number 1 chosen as the separator instead of a colon?",
   "A double click selects a whole word up to a colon but not past it",
   ["A colon is not allowed in a URI",
    "The number 1 is the first character of the bech32 alphabet",
    "A colon would make the address one character longer"],
   "The number also cannot be confused with the letter l, and bech32 strings do not otherwise use it.")
it("HumanReadablePart", "Analyze",
   "A prefix may itself contain the character 1. How does a decoder then split the string?",
   "At the last 1 in the string",
   ["At the first 1 in the string",
    "At the first character that is not in the alphabet",
    "Such a prefix is not allowed"],
   "The specification says that in case 1 is allowed inside the human-readable part, the last one in the string is the separator.")
ap("BchCode", "(30, 1073741824, True)",
   "print((6 * 5, 2 ** 30, 1 / 2 ** 30 < 1e-9))",
   ["(30, 1073741824, False)", "(6, 64, True)", "(32, 4294967296, True)"],
   "Six characters of five bits are 30 bits, giving just over a thousand million possibilities, which is the origin of the one-in-a-billion figure.")
it("BchCode", "Understand",
   "What does the BCH code guarantee that a truncated hash cannot?",
   "That any error affecting at most four characters is always detected",
   ["That any error can be corrected without asking the user",
    "That the checksum is shorter than a hash-based one",
    "That the address cannot be changed by an attacker"],
   "A hash gives a probabilistic check, while a BCH code can be designed so that a whole class of errors is caught with certainty.")
it("BchCode", "Analyze",
   "Why do the specifications ask software not to correct errors in an address?",
   "Correction turns invalid input into valid input, which may not be the intended one",
   ["Correction is too slow to run inside a wallet",
    "Correction would require the private key of the receiver of the payment to be known",
    "Correction is patented and may not be implemented freely"],
   "Error correction erodes error detection, and use of an incorrect but valid address can cause funds to be lost irrecoverably.")
ap("ErrorDetection", "[25, 40]",
   "good = 'bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7'\ntyped = 'bc1p9nh05ha8wrljf7ru236awn4t2x0d5ctkkywmv9sclnm4t0av2vgs4k3au7'\nprint([i for i, (a, b) in enumerate(zip(good, typed)) if a != b])",
   ["[24, 39]", "[25]", "[]"],
   "The two characters that differ are at positions 25 and 40, exactly the error locations that Bitcoin Core 31.1 reports for the mistyped address.")
it("ErrorDetection", "Analyze",
   "Under which condition does the guarantee about four wrong characters hold?",
   "The string entered has the same length as the original address",
   ["The address is written in uppercase",
    "The wallet is connected to a node",
    "The errors are all of them in the data part and not in the checksum"],
   "If characters are added or removed during transcription the guarantee does not apply, which is the root of the length extension weakness.")
ap("LengthExtension", "[15, 18, 20]",
   "print([len(a) for a in ('bc1pqqqsq9txsqp', 'bc1pqqqsq9txsqqqqp', 'bc1pqqqsq9txsqqqqqqp')])",
   ["[14, 18, 20]", "[13, 17, 19]", "[15, 19, 23]"],
   "The intended address has 15 characters and the first two extensions 18 and 20, so three and five letters q have been inserted before the final p.")
it("LengthExtension", "Understand",
   "What exactly is the flaw in the bech32 checksum?",
   "Inserting or deleting letters q just before a final p keeps the checksum valid",
   ["Any address ending in q can be shortened without detection",
    "Two different addresses that have the same length always end in the very same checksum",
    "The checksum ignores the human-readable part"],
   "The specification of the repair states the weakness in exactly those terms, and the book prints six strings that show it.")
it("LengthExtension", "Analyze",
   "Why was the flaw harmless for version 0 addresses?",
   "Only two program lengths are valid, so twenty insertions would be needed",
   ["Version 0 addresses do not end in the letter p",
    "Version 0 uses a different checksum constant",
    "Wallets simply reject any version 0 address that turns out to be too long for its program"],
   "The valid lengths of 42 and 62 characters are twenty apart, and each insertion adds one character.")
ap("Bech32mAddress", "(True, 'q2p3eu', '4k3au7')",
   ("b32 = 'bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgsq2p3eu'\n"
    "b32m = 'bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7'\n"
    "print((b32[:-6] == b32m[:-6], b32[-6:], b32m[-6:]))"),
   ["(False, 'q2p3eu', '4k3au7')", "(True, '4k3au7', 'q2p3eu')", "(True, 'vgsq2p', 'vgs4k3')"],
   "The two encodings of the same program agree in every character but the last six, which are the checksum.")
it("Bech32mAddress", "Remember",
   "What is the only difference between the bech32 and the bech32m algorithm?",
   "The constant combined into the checksum, 0x2bc830a3 instead of 1",
   ["The size of the alphabet, 32 instead of 58",
    "The length of the checksum itself, which is six characters instead of four",
    "The human-readable part, bcm instead of bc"],
   "All other aspects of the encoding remain the same, including the human-readable parts.")
it("Bech32mAddress", "Analyze",
   "Why is version 0 not allowed to use either encoding?",
   "Permitting both would reduce the error detection to the equivalent of 29 bits",
   ["Version 0 programs are much too short to be used together with the bech32m constant",
    "Bech32m was published after version 0 was frozen",
    "Version 0 addresses are always written in uppercase"],
   "The specification gives exactly that reason for keeping bech32 for version 0 and bech32m for the later versions.")
ap("P2wpkh", "22",
   "print(len(bytes.fromhex('00142b626ed108ad00a944bb2922a309844611d25468')))",
   ["25", "34", "20"],
   "A P2WPKH output script is 22 bytes: the version byte, the length 20 and the 20-byte commitment, three bytes less than the P2PKH equivalent.")
it("P2wpkh", "Understand",
   "How is the commitment inside a P2WPKH program built?",
   "Exactly as for P2PKH: SHA256 of the public key, then RIPEMD-160 of that",
   ["SHA256 of the public key alone, without RIPEMD-160",
    "RIPEMD-160 of the public key alone, without SHA256",
    "The double SHA256 of the public key"],
   "The book says the commitment is constructed in exactly the same way as the commitment for a P2PKH output.")
it("P2wpkh", "Analyze",
   "Why can a key that was used uncompressed with a legacy address not be used with P2WPKH?",
   "Only compressed public keys are accepted in P2WPKH and P2WSH",
   ["The witness program has room for 20 bytes only",
    "Uncompressed keys produce a 32-byte commitment",
    "Uncompressed keys cannot be hashed with SHA256"],
   "The specification states the restriction, so the uncompressed form has no place in a version 0 witness output.")
ap("P2wsh", "34",
   "print(len(bytes.fromhex('0020648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f')))",
   ["22", "32", "25"],
   "A P2WSH output script is 34 bytes: the version byte, the length 32 and the 32-byte SHA256 of the script.")
it("P2wsh", "Analyze",
   "Why does P2WSH use SHA256 alone where P2SH used SHA256 and then RIPEMD-160?",
   "A 32-byte commitment gives at least 128 bits of collision resistance",
   ["RIPEMD-160 is not available in every implementation",
    "SHA256 is faster, which matters for a node that verifies many scripts",
    "The witness program has no room for a 20-byte value"],
   "The book says the RIPEMD-160 step may not be secure in some cases and that the result is a commitment of 32 instead of 20 bytes.")
ap("P2tr", "32",
   "print(len(bytes.fromhex('2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311')))",
   ["20", "33", "64"],
   "The witness program of a taproot output is a 32-byte x coordinate, the key encoding that the Schnorr signature standard uses.")
it("P2tr", "Understand",
   "What does the witness program of a P2TR output hold?",
   "A point on the secp256k1 curve, usually a key that commits to more data",
   ["The HASH160 of a public key",
    "The SHA256 of a redeem script",
    "A 32-byte random value chosen by the receiver"],
   "The book says it may be a simple public key but in most cases should be a public key that commits to additional data.")
it("P2tr", "Analyze",
   "What is traded away when an output commits to a key rather than to a hash of it?",
   "The key is visible from the start, so the hash no longer hides it until spending",
   ["The output can no longer be spent with a signature",
    "The address becomes longer than a legacy address",
    "The output cannot be paid by a wallet that supports bech32m"],
   "A taproot address commits to a key, and the benefit of a hiding hash is exchanged for flexibility and smaller signatures.")

# ============================================================================================================
# 6  PRACTICE, ASSURANCE AND THE SEMANTIC LINK
# ============================================================================================================
it("Practice", "Understand",
   "Why does this branch compare the book with a recent release of Bitcoin Core?",
   "A chapter is a snapshot, and a student who learns only its practice may look for removed features",
   ["Because the book's statements about the curve are wrong",
    "Because Bitcoin Core is the only program in the whole ecosystem that can validate an address at all",
    "Because the book was written before segwit existed"],
   "The branch sets the book of 2023 beside software of 2026 and says where they differ, with the date of each source attached.")
it("Modern", "Analyze",
   "What changed when wallets moved from independent keys to a single seed?",
   "One backup covers every key, but exporting one key endangers the others",
   ["Keys became shorter, so addresses became shorter too",
    "Keys no longer need to be random, because the seed is",
    "Backups became quite unnecessary, because the seed itself is kept on the blockchain"],
   "The book warns that an attacker with one exported key and some nonprivate data about the wallet can potentially derive every key in it.")
ap("DefaultAddressType", "2",
   "print(['legacy', 'p2sh-segwit', 'bech32', 'bech32m'].index('bech32'))",
   ["0", "3", "1"],
   "The four values of the address type option are listed in this order and the default, bech32, is the third of them.")
it("DefaultAddressType", "Remember",
   "Which kind of address does Bitcoin Core 31.1 hand out when nothing is asked for?",
   "A bech32 address for a P2WPKH output of witness version 0",
   ["A legacy P2PKH address beginning with 1",
    "A bech32m taproot address of witness version 1",
    "A P2SH address beginning with 3"],
   "The run of the release for this chapter gave a bech32 address by default, and the help text names bech32 as the default value of the option.")
ap("KeyExport", "['getnewaddress', 'importdescriptors']",
   ("present = ['getnewaddress', 'dumpprivkey', 'importdescriptors', 'importprivkey']\n"
    "removed = ['dumpprivkey', 'importprivkey']\n"
    "print(sorted(set(present) - set(removed)))"),
   ["['dumpprivkey', 'importprivkey']", "['getnewaddress', 'dumpprivkey', 'importdescriptors']",
    "['importdescriptors']"],
   "The 30.0 release notes list dumpprivkey and importprivkey among the removed legacy wallet commands, while getnewaddress and importdescriptors remain.")
it("KeyExport", "Understand",
   "How can a single private key still be brought into a current Bitcoin Core?",
   "Inside a descriptor given to importdescriptors, for example pkh with a WIF string",
   ["With the importprivkey command, which still exists in release 31.1",
    "By editing the wallet file while the node is stopped",
    "Not at all: a key from outside can never be used again"],
   "The chapter's run obtained the book's own addresses from descriptors that carry its WIF strings, after dumpprivkey and importprivkey had been removed.")
ap("PassphraseProtection", "(58, '6P')",
   "s = '6PRHv1jg1ytiE4kT2QtrUz8gEjMQghZDWg1FuxjdYDzjUkcJeGdFj9q9Vi'\nprint((len(s), s[:2]))",
   ["(58, '6p')", "(56, '6P')", "(59, '6P')"],
   "A passphrase-protected record is always 58 characters and always starts with 6P, and this is the smallest such string the specification prints.")
it("PassphraseProtection", "Analyze",
   "BIP38 has the status Deployed and the comment summary Unanimously Discourage. How do the two fit together?",
   "The format exists and is in use, and those who commented advise against new implementations",
   ["The status is out of date and should read Withdrawn",
    "The comment applies only to the variant with elliptic curve multiplication",
    "A document cannot be deployed and discouraged at the same time, so one of the two lines is an error"],
   "The format is of interest for old paper wallets and encrypted keys, not for new software.")
ap("DeterministicWallet", "50b18e0b",
   ("import hashlib\n"
    "seed = 'f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73'\n"
    "print(hashlib.sha256((seed + ' + 0\\n').encode()).hexdigest()[:8])"),
   ["a965dbcd", "19580c97", "f1cc3bc0"],
   "Hashing the seed together with the number 0, exactly as the book's shell command does, gives the first derived value of its example.")
it("DeterministicWallet", "Analyze",
   "In which two directions is the seed of a deterministic wallet a single point of failure?",
   "Whoever learns it can derive every key, and whoever loses it loses every key",
   ["It can be used only once, and it cannot be changed afterwards",
    "It is stored on the blockchain, and it is always encrypted with a passphrase first",
    "It must be at least 256 bits, and it must be a prime number"],
   "The book says that if someone else gets your seed they can also generate all of the private keys, and a lost seed cannot be recovered.")
ap("AddressReuse", "(1, 3)",
   ("reused = ['bc1qh0q7g23e6pdye3sh2ttfvwmld8gfhvnmmfxuck'] * 3\n"
    "fresh = ['bc1qaaa', 'bc1qbbb', 'bc1qccc']\n"
    "print((len(set(reused)), len(set(fresh))))"),
   ["(3, 1)", "(3, 3)", "(1, 1)"],
   "Three payments to one address leave one address for an observer to group them by, while three fresh addresses leave nothing visible in common.")
it("AddressReuse", "Understand",
   "Whose privacy does the reuse of an address reduce, besides the receiver's?",
   "The people who pay the address or are paid from it",
   ["Only the miner who includes the transactions",
    "Nobody else: the loss is the receiver's alone",
    "Everyone who holds a key on the same curve"],
   "The book's two small stories are Alice who wants to donate anonymously and Bob who does not want his discount to be known.")
ap("VanityAddress", "11316496",
   "print(58 ** 4)",
   ["195112", "656356768", "3364"],
   "Each further character of a pattern multiplies the work by 58, so a four-character pattern occurs about once in 11 million keys.")
it("VanityAddress", "Analyze",
   "Why have vanity addresses almost disappeared, according to the book?",
   "Deterministic wallets cannot take them in, and they invite address reuse",
   ["They turned out to be considerably easier to attack than other addresses",
    "The base58 alphabet no longer contains readable letters",
    "Bitcoin Core refuses to validate them"],
   "The book names those two likely causes and notes that most wallets do not allow importing a key from a vanity generator.")
it("VanityAddress", "Understand",
   "Is a vanity address less secure than any other address?",
   "No: it rests on the same curve and the same hash functions",
   ["Yes, because its first characters are known in advance",
    "Yes, because the search reveals part of the private key",
    "It depends on how many characters the pattern has"],
   "The book says one can no more easily find the private key of a vanity address than that of any other address.")
ap("PaperWallet", "(64, 32)",
   "k = '1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD'\nprint((len(k), len(bytes.fromhex(k))))",
   ["(32, 64)", "(64, 64)", "(66, 33)"],
   "What has to be printed and kept safe is 64 hexadecimal digits, which are the 32 bytes of the private key.")
it("PaperWallet", "Analyze",
   "The book warns against paper wallets but recommends writing a recovery code on paper. Where is the difference?",
   "A recovery code regenerates a wallet from a trusted device; a paper wallet is one key from an unchecked program",
   ["A recovery code is encrypted and a paper wallet is not",
    "A recovery code is shorter than a printed private key, so it is much harder to copy down wrongly, and it can be read aloud",
    "A recovery code can be used only on the device that made it"],
   "The warning is about generation and about a single static key, not about paper itself.")
ap("HardwareSigningDevice", "(1, False)",
   "steps = ['prepare', 'sign', 'broadcast']\nprint((steps.index('sign'), 'private key' in steps))",
   ["(1, True)", "(2, False)", "(0, False)"],
   "Signing is the middle step and the private key is not among the things that cross the boundary: it stays inside the device.")
it("HardwareSigningDevice", "Understand",
   "What does a hardware signing device protect a key from, and what not?",
   "From software on the computer, but not from loss or from a wrong signing decision",
   ["From loss, but not from software on the computer",
    "From every threat there is, which is the reason why a recovery code is unnecessary with one",
    "From nothing: it only stores the key more conveniently"],
   "The book calls the name hardware wallet confusing because the device holds keys, not coins, and a recovery code is still needed.")
it("Assurance", "Understand",
   "Why does the chapter treat an error in address code as more than a minor bug?",
   "A wrong decoder sends money to a place from which it cannot be recovered",
   ["A wrong decoder makes the node reject every block",
    "A wrong decoder reveals the private key of the receiver",
    "A wrong decoder breaks the consensus rules that the whole network enforces"],
   "That is why the book asks implementers to use the published test vectors and why the chapter compares independent implementations.")
ap("TestVectors", "(7, 8, 15)",
   ("b32m = ['A1LQFN3A', 'a1lqfn3a', 'an83character', 'abcdef1l7aum6echk45nj3s0wdvt2fg8x9yrzpqzd3ryx',\n"
    "        '11lllllllll', 'split1checkupstage', '?1v759aa']\n"
    "valid = ['v%d' % i for i in range(8)]\n"
    "invalid = ['x%d' % i for i in range(15)]\n"
    "print((len(b32m), len(valid), len(invalid)))"),
   ["(8, 7, 15)", "(7, 15, 8)", "(6, 8, 15)"],
   "BIP350 publishes seven valid bech32m strings, eight valid segwit addresses with their output scripts and fifteen invalid addresses with reasons.")
it("TestVectors", "Analyze",
   "Why does the specification include valid addresses of versions that do not exist yet?",
   "So that a wallet written today can still pay the outputs of a future upgrade",
   ["So that the miners can test out the next soft fork well before the day it activates",
    "So that a decoder can reject every version above 1",
    "Because those versions were used on testnet before mainnet"],
   "All higher versions should be recognised as valid recipients, although no wallet should ever create one.")
it("TestVectors", "Understand",
   "What does passing the published vectors not prove?",
   "That the implementation is correct for inputs the vectors do not try",
   ["That the implementation computes the checksum of a string at all",
    "That the implementation rejects a mixed-case address",
    "That the implementation accepts a version 16 address"],
   "Vectors sample the space of inputs, so they are necessary but not sufficient and should be combined with other checks.")
ap("IndependentCheck", "(1, True)",
   ("answers = ['1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy'] * 3\n"
    "print((len(set(answers)), len(set(answers)) == 1))"),
   ["(3, False)", "(1, False)", "(3, True)"],
   "Three independent implementations gave one and the same address for the book's key, which is what agreement looks like when it is counted.")
it("IndependentCheck", "Analyze",
   "What does agreement between two implementations not show?",
   "That the answer is right, since both may share a misreading of the specification",
   ["That the two implementations were written by different people in different places",
    "That the inputs were the same for both",
    "That each of them is faster than the other"],
   "Agreement covers only the inputs that were tried, and a shared source of error can make two programs agree on a mistake.")
it("Semantics", "Understand",
   "Which property of a key pair links this chapter to the course theme of identity?",
   "Its holder can prove control without asking anyone's permission",
   ["Its public key can always be looked up in some central registry",
    "Its private key can be recovered from the blockchain",
    "Its address contains the owner's name in base58"],
   "That is the property around which the W3C's Decentralized Identifiers are designed, as the branch explains.")
it("Identifiers", "Analyze",
   "Why does a name controlled by a key need no central authority?",
   "Its holder can show by a signature that a statement comes from them",
   ["Its holder registers it once and then owns it forever",
    "Its holder publishes it on a blockchain, which acts as the authority",
    "Its holder can revoke anybody else's name"],
   "Most identifiers depend on an authority that assigns and can withdraw names, while a key-controlled name needs only verification.")
it("KeyControlProof", "Understand",
   "How does a key holder prove control without revealing the key?",
   "By signing a challenge that the verifier chooses",
   ["By sending the key over an encrypted channel",
    "By publishing the key's hash on the blockchain",
    "By asking a trusted third party to vouch for the key"],
   "A fresh challenge prevents an old signature from being replayed, and the verifier checks the signature against the public key.")
it("KeyControlProof", "Analyze",
   "What does proof of control not establish?",
   "Who the prover is, or that the key is the one the verifier meant",
   ["That the prover holds the private key",
    "That the message was not altered",
    "That the signature really matches the public key that was given"],
   "Binding a key to a person or an organisation needs something further, and a stolen key proves control for the thief.")
ap("Uri", "['did', 'example', '123456789abcdefghi']",
   "print('did:example:123456789abcdefghi'.split(':'))",
   ["['did:example', '123456789abcdefghi']", "['did', 'example:123456789abcdefghi']",
    "['did', 'example', '123456789', 'abcdefghi']"],
   "A decentralized identifier has three parts: the scheme did, the name of a method, and an identifier that the method defines.")
it("Uri", "Remember",
   "How does RFC 3986 define a uniform resource identifier?",
   "A compact sequence of characters that identifies an abstract or physical resource",
   ["A web address that always leads to a page",
    "A number that a registry assigns to each resource that it knows about",
    "A name that is unique within one application"],
   "The generic syntax lets an implementation parse the common components of a URI without knowing the requirements of every scheme.")
it("DecentralizedIdentifier", "Remember",
   "What does a decentralized identifier associate its subject with?",
   "A DID document, which can carry verification methods such as public keys",
   ["A balance held at a wallet provider",
    "A certificate that some certificate authority has issued for it",
    "An entry in a national identity register"],
   "The recommendation says DIDs are URIs that associate a DID subject with a DID document, allowing trustable interactions.")
it("DecentralizedIdentifier", "Analyze",
   "Is a Bitcoin address a decentralized identifier?",
   "No: the two share a design idea but are different things with different specifications",
   ["Yes, every Bitcoin address is in fact a decentralized identifier of the method called bitcoin",
    "Yes, as soon as it is published in a DID document",
    "No, because a DID cannot contain a public key"],
   "A DID is meaningful only with a method that says how documents are created, resolved, updated and deactivated.")

# ============================================================================================================
# emit
# ============================================================================================================
def run(code):
    r = subprocess.run([PY, "-c", code], capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL)
    if r.returncode == 0:
        return r.stdout.strip() or "(no output)"
    lines = [l for l in r.stderr.strip().splitlines() if l.strip()]
    return lines[-1].split(":")[0].strip() if lines else "?"


def main():
    _vk = lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")]
    pd = sorted((f for f in os.listdir(os.path.join(HERE, "ch04-page")) if f.startswith("page_data_v")), key=_vk)[-1]
    data = json.load(open(os.path.join(HERE, "ch04-page", pd), encoding="utf-8"))
    ids = {n["id"] for n in data["nodes"]}
    io_ids = {n["id"] for n in data["nodes"] if "io" in n}
    bad = []
    bank = []
    for i, src in enumerate(ITEMS):
        opts = [src["right"]] + src["wrongs"]
        if len(set(opts)) != 4:
            bad.append("item %d (%s): options not distinct" % (i, src["concept"]))
        if src["concept"] not in ids:
            bad.append("item %d: unknown concept %s" % (i, src["concept"]))
        if src["code"]:
            got = run(src["code"])
            if got != src["right"]:
                bad.append("item %d (%s): program prints %r, option says %r" % (i, src["concept"], got, src["right"]))
        pos = i % 4
        ws = src["wrongs"][:]
        # when a distractor is as long as the marked option, show it first, so that the length of an option
        # is never a cue: max() picks the first of several equally long strings
        if pos > 0 and max(len(w) for w in ws) >= len(src["right"]):
            j = max(range(3), key=lambda k: len(ws[k]))
            ws.insert(0, ws.pop(j))
        ordered = ws
        ordered.insert(pos, src["right"])
        item = {"concept": src["concept"], "level": src["level"], "q": src["q"]}
        if src["code"]:
            item["code"] = src["code"]
        item["options"] = ordered
        item["answer"] = pos
        item["why"] = src["why"]
        bank.append(item)
    per = collections.defaultdict(list)
    for b in bank:
        per[b["concept"]].append(b)
    for nid in sorted(ids):
        if not per[nid]:
            bad.append("concept %s: no item" % nid)
    for nid in sorted(io_ids):
        if len(per[nid]) < 2:
            bad.append("io concept %s: fewer than two items" % nid)
        if not any(b["level"] == "Apply" and b.get("code") for b in per[nid]):
            bad.append("io concept %s: no Apply item with a program" % nid)
    cnt = collections.Counter(b["answer"] for b in bank)
    for p in range(4):
        share = cnt[p] / len(bank)
        if not 0.20 <= share <= 0.30:
            bad.append("answer index %d share %.1f%% outside 20-30%%" % (p, 100 * share))
    longest = sum(1 for b in bank if max(b["options"], key=len) == b["options"][b["answer"]])
    print("items %d; concepts covered %d/%d; io concepts %d" % (len(bank), sum(1 for n in ids if per[n]), len(ids), len(io_ids)))
    print("levels", dict(sorted(collections.Counter(b["level"] for b in bank).items())))
    print("answer positions", {p: cnt[p] for p in range(4)})
    print("correct option is the longest in %d/%d items" % (longest, len(bank)))
    if bad:
        print("NOT WRITTEN -", len(bad), "problem(s):")
        for b in bad:
            print("  -", b)
        return 1
    json.dump(bank, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("written", os.path.relpath(OUT, HERE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
