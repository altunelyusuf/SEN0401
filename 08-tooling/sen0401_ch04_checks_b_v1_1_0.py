"""SEN0401 chapter 4, executed claims, part B (version 1.1.0): the curve and the hash functions."""
from sen0401_ch04_checkhelp_v1_1_0 import *
from sen0401_ch04_checks_a_v1_1_0 import BK, B340, SEC2, KH, NH, XH, YH, PUB
RP = rd(os.path.join(HERE, "README_PORT.md"))
FIPS = rd(S1 + "fips180_4_description.txt")
VR = evj("verify_results_v1_0_0.json")
VA = evj("core_validateaddress_31_1_v1_0_0.json")
GX = "0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798"
GY = "0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8"
PP = "(2 ** 256 - 2 ** 32 - 977)"
# SEC 2 Table 1 / Table 2 rows read from the saved text of the standard
SECROWS = ("[tuple(l.split()) for l in %s.splitlines() if l.split()[:1] and l.split()[0].startswith('secp') and len(l.split()) == 9]" % rd(S3 + "sec2_v2_0_full.txt"))
ADDR_C, ADDR_U = "1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy", "1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x"
H160C, H160U = "bbc1e42a39d05a4cc61752d6963b7f69d09bb27b", "211b74ca4686f81efda5641767fc84ef16dafe0b"

CHECKS_B = [
 # ---- the curve level, finite field
 (has(BK, "Elliptic curve cryptography (ECC) is a type of asymmetric or public key cryptography based on the discrete logarithm problem as expressed by addition and multiplication on the points of an elliptic curve",
      "the math is identical to that of an elliptic curve over real numbers", "it looks like a pattern of dots scattered in two dimensions, which makes it difficult to visualize",
      "a much more complex pattern of dots on a unfathomably large grid", "over a much smaller finite field of prime order 17"), "True"),
 (has(BK, "The _mod p_ (modulo prime number _p_) indicates that this curve is over a finite field of prime order _p_", "a very large prime number"), "True"),
 ("(pow(5, -1, 17), 5 * 7, 5 * 7 % 17, all(a * pow(a, -1, 17) % 17 == 1 for a in range(1, 17)))", "(7, 35, 1, True)"),
 ("(%s == 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1, %s == int('FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFFC2F'.replace(' ', ''), 16), 2 ** 256 - %s)" % (PP, PP, PP), "(True, True, 4294968273)"),
 (has(SEC2, "p = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE FFFFFC2F", "= 2256 − 232 − 29 − 28 − 27 − 26 − 24 − 1"), "True"),
 ("%s.is_probable_prime(%s)" % (KT, PP), "True"),
 ("%s.is_probable_prime(%s) and not %s.is_probable_prime(%s * 3)" % (KT, NH, KT, NH), "True"),
 ("(%s.P == %s, %s != %s.P)" % (KT, PP, NH, KT), "(True, True)"),
 # ---- the elliptic curve
 (has(BK, "{y^2 = (x^3 + 7)}~\\text{over}~(\\mathbb{F}_p)", "{y^2 \\mod p = (x^3 + 7) \\mod p}"), "True"),
 (has(BK, "the curve is symmetric, meaning it is reflected like a mirror by the x-axis"), "True"),
 (has(SEC2, "The curve E: y 2 = x3 + ax + b over Fp is defined by:", "a = 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000", "b = 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000007"), "True"),
 ("(len([(x, y) for x in range(17) for y in range(17) if (y * y - x ** 3 - 7) % 17 == 0]), [(1, 5), (1, 12), (2, 7), (2, 10)] == [q for q in [(x, y) for x in range(17) for y in range(17) if (y * y - x ** 3 - 7) % 17 == 0] if q[0] in (1, 2)])", "(17, True)"),
 ("(lambda p, x, y: (x ** 3 + 7 - y ** 2) % p)(115792089237316195423570985008687907853269984665640564039457584007908834671663, 55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)", "0"),
 ("115792089237316195423570985008687907853269984665640564039457584007908834671663 == %s" % PP, "True"),
 (has(BK, "55066263022277343669578718895168534326250603453777594175500187360389116729240", "32670510020758816978083085130507043184471273380659243275938904335757337482424",
      "115792089237316195423570985008687907853269984665640564039457584007908834671663"), "True"),
 # ---- point addition
 (has(BK, "there is a third point P~3~ = P~1~ + P~2~, also on the elliptic curve", "line will intersect the elliptic curve in exactly one additional place", "Then reflect in the x-axis to get P~3~ = (x, –y)",
      "If P~1~ and P~2~ are the same point, the line \"between\" P~1~ and P~2~ should extend to be the tangent on the curve at this point P~1~",
      "the tangent line will be exactly vertical, in which case P~3~ = \"point at infinity.\"", "If P~1~ is the \"point at infinity,\" then P~1~ + P~2~ = P~2~",
      "(A pass:[+] B) pass:[+] C = A pass:[+] (B pass:[+] C)", "it's sometimes represented by x = y = 0 (which doesn't satisfy the elliptic curve equation"), "True"),
 ("(lambda T: (T.small_add((1, 5), (2, 7), 17), T.small_add((1, 5), (1, 5), 17), T.small_add((1, 5), (1, 12), 17), T.small_add(None, (1, 5), 17), T.small_add((1, 5), None, 17)))(%s)" % KT, "((1, 12), (2, 10), None, (1, 5), (1, 5))"),
 (X("(lambda T: (lambda pts: all(T.small_add(T.small_add(a, b, 17), c, 17) == T.small_add(a, T.small_add(b, c, 17), 17) for a in pts for b in pts for c in pts))([None] + [(x, y) for x in range(17) for y in range(17) if (y * y - x ** 3 - 7) % 17 == 0]))($T)"), "True"),
 (X("(lambda T: (lambda pts: all((lambda s: s is None or (s[1] ** 2 - s[0] ** 3 - 7) % 17 == 0)(T.small_add(a, b, 17)) for a in pts for b in pts))([None] + [(x, y) for x in range(17) for y in range(17) if (y * y - x ** 3 - 7) % 17 == 0]))($T)"), "True"),
 ("(lambda T: (lambda G: (T.ec_add(G, G) == T.ec_mul(2), T.ec_add(G, (G[0], T.P - G[1])), T.ec_add(None, G) == G, T.ec_add(T.ec_mul(5), T.ec_mul(7)) == T.ec_mul(12)))(T.G))(%s)" % KT, "(True, None, True, True)"),
 # ---- secp256k1
 (has(BK, "as defined in a standard called +secp256k1+, established by the National Institute of Standards and Technology (NIST)"), "True"),
 (has(SEC2, "specified by the sextuple T = (p, a, b, G, n, h)", "associated with a Koblitz curve secp256k1", "SEC 2: Recommended Elliptic Curve Domain Parameters", "Certicom Research", "January 27, 2010", "Version 2.0",
      "Each name begins with sec to denote ‘Standards for Efficient Cryptography’, followed by a p to denote parameters over", "Fp , followed by a number denoting the length in bits of the field size p, followed by a k to denote parameters associated with a Koblitz curve or an r to denote verifiably random parameters, followed by a sequence number",
      "The column labelled ‘strength’ gives the approximate number of bits of security the parameters offer", "SEC 2 (Draft) Ver. 2.0"), "True"),
 ("%s" % SECROWS, "[('secp192k1', '2.2.1', 'c', 'c', 'c', 'c', '-', '-', 'c'), ('secp192r1', '2.2.2', 'r', 'r', 'c', 'c', 'r', 'r', 'c'), ('secp224k1', '2.3.1', 'c', 'c', 'c', 'c', '-', '-', 'c'), ('secp224r1', '2.3.2', 'r', 'r', 'c', 'c', 'r', 'r', 'c'), ('secp256k1', '2.4.1', 'c', 'c', 'c', 'c', '-', '-', 'c'), ('secp256r1', '2.4.2', 'r', 'r', 'c', 'c', 'r', 'r', 'c'), ('secp384r1', '2.5.1', 'c', 'r', 'c', 'c', 'r', 'r', 'c'), ('secp521r1', '2.6.1', 'r', 'r', 'c', 'c', 'r', 'r', 'c')]"),
 ("[(r[0], r[7]) for r in %s if r[0] in ('secp256k1', 'secp256r1')]" % SECROWS, "[('secp256k1', '-'), ('secp256r1', 'r')]"),
 (has(SEC2, "Parameters Section ANSI X9.62 ANSI X9.63 echeck IEEE P1363 IPSec NIST WAP", "‘NIST’ refers to the list of recommended parameters recently released by the U.S. government",
      "In these columns, a ‘-’ denotes parameters non-", "a ‘c’ denotes parameters conformant with the standard, and an ‘r’ denotes parameters explicitly recommended in the standard",
      "2.4.1 Recommended Parameters secp256k1", "2.4.2 Recommended Parameters secp256r1"), "True"),
 (has(SEC2, "secp256k1 2.4.1 128 256 3072 k", "secp192k1 2.2.1 96 192 1536 k", "secp521r1 2.6.1 256 521 15360 r"), "True"),
 ("(%s == (%s, %s))" % (PUB, XH, YH), "True"),
 (has(rd(S1 + "bip-0340.mediawiki"), "Title: Schnorr Signatures for secp256k1"), "True"),
 # ---- generator point
 (X("(lambda T: (T.G == ($GX, $GY), (T.G[1] ** 2 - T.G[0] ** 3 - 7) % T.P, T.G[1] % 2 == 0))($T)", GX=GX, GY=GY), "(True, 0, True)"),
 (X("(lambda p, x, y: (x ** 3 + 7 - y ** 2) % p)(2 ** 256 - 2 ** 32 - 977, $GX, $GY)", GX=GX, GY=GY), "0"),
 (has(SEC2, "cofactor h = #E(Fp )/n"), "True"),
 (has(SEC2, "G = 02 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798",
      "G = 04 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798 483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8"), "True"),
 (has(BK, "The generator point is specified as part of the +secp256k1+ standard and is always the same for all keys in bitcoin", "a private key _k_ multiplied with _G_ will always result in the same public key _K_",
      "shows the process for deriving _G_, _2G_, _4G_"), "True"),
 ("(lambda T: (T.ec_mul(T.N), T.ec_mul(T.N - 1) == (T.G[0], T.P - T.G[1]), T.ec_mul(T.N + 1) == T.G, T.is_probable_prime(T.N)))(%s)" % KT, "(None, True, True, True)"),
 # ---- elliptic curve multiplication
 (has(BK, "if k is a whole number, then kP = P + P + P + ... + P (k times)", "k is sometimes confusingly called an \"exponent\"", "Elliptic curve multiplication is a type of function that cryptographers call a \"trap door\" function: it is easy to do in one direction (multiplication) and impossible to do in the reverse direction (division)",
      "adding a point to itself is the equivalent of drawing a tangent line on the point and finding where it intersects the curve again, then reflecting that point on the x-axis"), "True"),
 ("(%s.bit_length(), bin(%s).count('1'), %s.bit_length() - 1, bin(%s).count('1') - 1)" % (KH, KH, KH, KH), "(253, 124, 252, 123)"),
 ("(lambda T: (lambda a, b: T.ec_mul(a + b) == T.ec_add(T.ec_mul(a), T.ec_mul(b)) and T.ec_mul(a * b) == T.ec_mul(a, T.ec_mul(b)))(123456789123456789, 987654321987654321))(%s)" % KT, "True"),
 # ---- discrete logarithm
 ("(next(k for k in range(1, 101) if pow(2, k, 101) == 7), pow(2, 9), pow(2, 9, 101))", "(9, 512, 7)"),
 (has(BK, "The reverse operation, known as \"finding the discrete logarithm\"—calculating _k_ if you know __K__—is as difficult as trying all possible values of _k_ (i.e., a brute-force search)",
      "using the computers and algorithms available today"), "True"),
 ("(2 ** 128, 128 * 2 == 256)", "(340282366920938463463374607431768211456, True)"),
 # ---- cryptographic library
 (has(BK, "Many Bitcoin implementations use the https://oreil.ly/wD60m[libsecp256k1 cryptographic library] to do the elliptic curve math"), "True"),
 (has(B340, "To be safe for usage in consensus systems, the verification algorithm must be completely specified at the byte level. This guarantees that nobody can construct a signature that is valid to some verifiers but not all"), "True"),
 ("(lambda i: (len(i.getsource(%s.ec_add).splitlines()) + len(i.getsource(%s.ec_mul).splitlines()) < 20))(__import__('inspect'))" % (KT, KT), "True"),
 (X("(lambda p, x, y: pow((x ** 3 + 7) % p, (p + 1) // 4, p) in (y, p - y))($PP, $XH, $YH)", PP=PP, XH=XH, YH=YH), "True"),
 (VR + "['book_addresses_agree']", "True"),
 (VR + "['core_validate_agrees_on_segwit_examples']", "True"),
 (has(rd(os.path.join(HERE, "sen0401_ch04_keys_v1_1_0.py")), "Not for use with real funds: it is not constant-time and takes no care over where randomness comes from"), "True"),
 # ---- hash functions
 (has(BK, "Bitcoin already contains several data structures much larger than 65 bytes that need to be securely referenced in other parts of Bitcoin using the smallest amount of data that was secure",
      "Bitcoin accomplishes that with a _hash function_, a function that takes a potentially large amount of data, scrambles it (hashes it), and outputs a fixed amount of data",
      "A cryptographic hash function will always produce the same output when given the same input, and a secure function will also make it impractical for somebody to choose a different input that produces a previously-seen output",
      "That makes the output a _commitment_ to the input. It's a promise that, in practice, only input _x_ will produce output _X_"), "True"),
 (has(FIPS, "This standard specifies hash algorithms that can be used to generate digests of messages. The digests are used to detect whether messages have been changed since the digests were generated"), "True"),
 (has(prev("01"), "Proof of work"), "True"),
 (has(prev("03"), "SHA-256", "release"), "True"),
 ("__import__('hashlib').sha256(b'2007.  He said about a year and a half before Oct 2008\\n').hexdigest()", "'94d7a772612c8f2f2ec609d41f5bd3d04a5aa1dfe3582f04af517d396a302e4e'"),
 (has(BK, "94d7a772612c8f2f2ec609d41f5bd3d04a5aa1dfe3582f04af517d396a302e4e", "echo \"2007.  He said about a year and a half before Oct 2008\" | sha256sum"), "True"),
 ("(bin(int(__import__('hashlib').sha256(b'a').hexdigest(), 16) ^ int(__import__('hashlib').sha256(b'`').hexdigest(), 16)).count('1'), ord('a') - ord('`'))", "(139, 1)"),
 ("(__import__('hashlib').sha256(b'a').hexdigest() == __import__('hashlib').sha256(b'a').hexdigest())", "True"),
 ("(len(__import__('hashlib').sha256(b'').digest()), len(__import__('hashlib').sha256(b'abc').digest()), len(__import__('hashlib').sha256(bytes(1000000)).digest()))", "(32, 32, 32)"),
 ("__import__('hashlib').sha256(b'abc').hexdigest()[:8]", "'ba7816bf'"),
 (has(BK, "The SHA256 hash function is considered to be very secure and produces 256 bits (32 bytes) of output, less than half the size of original Bitcoin public keys",
      "the equivalent of 130 characters when written in hexadecimal", "The shortest version of Bitcoin public keys known to the developers of early Bitcoin were 65 bytes"), "True"),
 ("(32 < 65 / 2, 65 * 2, len(bytes.fromhex('04' + 'F028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A' + '07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB').hex()))", "(True, 130, 130)"),
 (has(RP, "`hashlib` has md5, sha1, sha2, sha3 and blake2 but **not ripemd160**"), "True"),
 ("(len(__import__('hashlib').new('ripemd160', b'abc').digest()), __import__('hashlib').new('ripemd160', b'abc').hexdigest())", "(20, '8eb208f7e05d987a9b044a8e98c6b087f15a0bfc')"),
 (has(BK, "there are other slightly less secure hash functions that produce smaller output, such as the RIPEMD-160 hash function whose output is 160 bits (20 bytes)",
      "For reasons Satoshi Nakamoto never stated, the original version of Bitcoin made commitments to public keys by first hashing the key with SHA256 and then hashing that output with RIPEMD-160; this produced a 20-byte commitment to the public key",
      "{A = RIPEMD160(SHA256(K))}", "where _K_ is the public key and _A_ is the resulting commitment"), "True"),
 ("(2 ** 160, 2 ** 160 // 2 ** 80 == 2 ** 80, 256 // 2, 160 // 2)", "(1461501637330902918203684832716283019655932542976, True, 128, 80)"),
 (has(BK, "For a secure 160-bit algorithm like HASH160, the probability is 1-in-2^160^", "the strength of hash algorithm is reduced to its square root. For HASH160, the probability becomes 1-in-2^80^"), "True"),
 # HASH160 of the example key
 ("(lambda T: (lambda K: (T.hash160(T.pub_bytes(K)).hex(), T.hash160(T.pub_bytes(K, False)).hex(), T.p2pkh(T.pub_bytes(K)), T.p2pkh(T.pub_bytes(K, False))))(T.ec_mul(%s)))(%s)" % (KH, KT), "('%s', '%s', '%s', '%s')" % (H160C, H160U, ADDR_C, ADDR_U)),
 ("(lambda h, r: r(h('sha256', bytes.fromhex('03' + 'F028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A')).digest()))(lambda n, d: __import__('hashlib').new(n, d), lambda d: __import__('hashlib').new('ripemd160', d).hexdigest())", "'%s'" % H160C),
 ("[%s['%s']['scriptPubKey'], %s['%s']['scriptPubKey']]" % (VA, ADDR_C, VA, ADDR_U), "['76a914%s88ac', '76a914%s88ac']" % (H160C, H160U)),
 ("(len(bytes.fromhex('%s')), len(bytes.fromhex('%s')))" % (H160C, H160U), "(20, 20)"),
 (has(BK, "it will produce a _different_ commitment than the uncompressed public key, leading to a different address", "a single private key can produce a public key expressed in two different formats (compressed and uncompressed) that produce two different Bitcoin addresses"), "True"),
]
