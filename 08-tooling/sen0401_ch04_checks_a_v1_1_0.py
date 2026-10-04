"""SEN0401 chapter 4, executed claims, part A (version 1.1.0): the branch 'Keys' down to randomness and the hash functions.
Each entry is (expression, expected repr); the chapter builder evaluates it alone under CPython 3.14. Sentences the text takes from the book
or a standard are checked by reading the saved copy of the source (has); numbers and outputs are computed by the chapter's own toolkit."""
from sen0401_ch04_checkhelp_v1_1_0 import *
BK = book("ch04_keys.adoc")
BK1, BK5 = book("ch01_intro.adoc"), book("ch05_wallets.adoc")
B340, B141 = rd(S1 + "bip-0340.mediawiki"), rd(S1 + "bip-0141.mediawiki")
SEC2 = rd(S3 + "sec2_v2_0_full.txt")
PSF = rd(S1 + "secrets.rst")
KH = "0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD"
NH = "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141"
XH = "0xF028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A"
YH = "0x07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB"
PUB = "%s.ec_mul(%s)" % (KT, KH)

CHECKS_A = [
 # ---- Keys (level 1) and the key pair
 (has(BK, "the thousands of Bitcoin full nodes who will verify her transaction don't know who Alice or Bob are",
      "The method Alice uses must ensure that only Bob can further spend the bitcoins he receives",
      "A receiver like Bob accepts bitcoins to a public key in a transaction that is signed by the spender",
      "Full nodes can verify that Alice's signature commits to the output of a hash function that itself commits to Bob's public key and other transaction details"), "True"),
 (has(BK, "The private key must remain secret at all times because revealing it to third parties is equivalent to giving them control over the bitcoins secured by that key",
      "if it's lost, it cannot be recovered and the funds secured by it are forever lost too"), "True"),
 (has(prev("01"), "noncustodial", "keys"), "True"),
 (has(prev("02"), "signature", "input", "output"), "True"),
 (has(BK, "The key pair consists of a private key and a public key derived from the private key. The public key is used to receive funds, and the private key is used to sign transactions to spend the funds",
      "A Bitcoin wallet contains a collection of key pairs, each consisting of a private key and a public key",
      "the public key can be calculated from the private key, so storing only the private key is also possible",
      "There is a mathematical relationship between the public and the private key that allows the private key to be used to generate signatures on messages"), "True"),
 # ---- public key cryptography and digital signatures
 (has(BK, "Public key cryptography was invented in the 1970s and is a mathematical foundation for modern computer and information security",
      "prime number exponentiation and elliptic curve multiplication", "easy to calculate in one direction and infeasible to calculate in the opposite direction using the computers and algorithms available today",
      "Bitcoin uses elliptic curve addition and multiplication as the basis for its cryptography",
      "It's not used to \"encrypt\" (make secret) the transactions", "a useful property of asymmetric cryptography is the ability to generate _digital signatures_",
      "possible for anyone to verify every signature on every transaction, while ensuring that only the owners of private keys can produce valid signatures"), "True"),
 (has(prev("03"), "OpenPGP", "signature"), "True"),
 (has(B340, "ECDSA] signatures over the [https://www.secg.org/sec2-v2.pdf secp256k1 curve] with [https://en.wikipedia.org/wiki/SHA-2 SHA256] hashes", "64-byte Schnorr signatures over the elliptic curve ''secp256k1''",
      "(which are variable size, and up to 72 bytes), we can use a simple fixed 64-byte format", "32-byte public keys and 64-byte signatures", "Title: Schnorr Signatures for secp256k1"), "True"),
 (has(B340, "If ''(r,s)'' is a valid ECDSA signature for a given message and key, then ''(r,n-s)'' is also valid for the same message and key", "as Bitcoin does through a policy rule on the network",
      "ECDSA signatures are inherently malleable"), "True"),
 (has(B141, "Nonintentional malleability becomes impossible", "Since signature data is no longer part of the transaction hash, changes to how the transaction was signed are no longer relevant to transaction identification"), "True"),
 ("(lambda T: (lambda d, z, k: (lambda Q, sig: (T.ecdsa_verify(Q, z, sig), T.ecdsa_verify(Q, z + 1, sig), T.ecdsa_verify(T.ec_mul(d + 1), z, sig), T.ecdsa_verify(Q, z, (sig[0], T.N - sig[1]))))(T.ec_mul(d), T.ecdsa_sign(d, z, k)))(%s, 12345678901234567890, 987654321987654321))(%s)" % (KH, KT), "(True, False, False, True)"),
 ("(lambda T: (lambda d, z, k: T.ecdsa_sign(d, z, k) == T.ecdsa_sign(d, z, k) != T.ecdsa_sign(d, z, k + 1))(%s, 12345678901234567890, 987654321987654321))(%s)" % (KH, KT), "True"),
 # ---- private key
 (has(BK, "A private key is simply a number, picked at random", "Control over the private key is the root of user control over all funds associated with the corresponding Bitcoin public key",
      "toss a coin 256 times and you have the binary digits of a random private key", "any process that's less than completely random can significantly reduce the security of your private key",
      "1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD", "256 bits shown as 64 hexadecimal digits, each 4 bits"), "True"),
 ("(len('%s'), len(bytes.fromhex('%s')) * 8)" % (KH[2:], KH[2:]), "(64, 256)"),
 (has(BK, "the private key can be any number between 0 and _n_ - 1 inclusive", "_n_ = 1.1578 × 10^77^, slightly less than 2^256^", "defined as the order of the elliptic curve used in Bitcoin",
      "we randomly pick a 256-bit number and check that it is less than _n_", "Otherwise, we simply try again with another random number",
      "approximately 10^77^ in decimal", "visible universe is estimated to contain 10^80^ atoms"), "True"),
 ("(%s < 2 ** 256, 2 ** 256 - %s, '%%.4e' %% %s, '%%.1e' %% ((2 ** 256 - %s) / 2 ** 256))" % (NH, NH, NH, NH), "(True, 432420386565659656852420866394968145599, '1.1579e+77', '3.7e-39')"),
 ("(len(str(2 ** 256)), round(__import__('math').log10(2 ** 256), 2), 2 ** 32)", "(78, 77.06, 4294967296)"),
 ("%s.ec_mul(0)" % KT, "None"),
 (has(SEC2, "n = FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141", "h = 01", "Recommended Parameters secp256k1"), "True"),
 ("%s.N == %s" % (KT, NH), "True"),
 # ---- public key
 (has(BK, "irreversible: _K_ = _k_ × _G_", "_G_ is a constant point called the _generator point_", "calculating _k_ if you know __K__", "is as difficult as trying all possible values of _k_ (i.e., a brute-force search)",
      "A private key can be converted into a public key, but a public key cannot be converted back into a private key because the math only works one way",
      "libsecp256k1 cryptographic library", "Imagine Bob trying to read that to Alice over the phone",
      "x = F028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A", "y = 07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB"), "True"),
 ("(%s == (%s, %s), %s %% 2, (%s ** 3 + 7 - %s ** 2) %% %s.P)" % (PUB, XH, YH, YH, XH, YH, KT), "(True, 1, 0)"),
 ("'03' if %s %% 2 else '02'" % YH, "'03'"),
 # ---- randomness, entropy
 (has(BK, "find a secure source of randomness (which computer scientists call _entropy_)", "The exact method you use to pick that number does not matter as long as it is not predictable or repeatable",
      "Bitcoin software uses cryptographically secure random number generators to produce 256 bits of entropy",
      "feeding a larger string of random bits, collected from a cryptographically secure source of randomness, into the SHA256 hash algorithm, which will conveniently produce a 256-bit value that can be interpreted as a number",
      "If the result is less than _n_, we have a suitable private key"), "True"),
 (has(prev("01"), "recovery code", "128 to 256"), "True"),
 (has(PSF, "module provides access to the most secure source of randomness that your operating system provides", "module, which is designed for modelling and simulation, not security or cryptography",
      "Return a random int in the range [0, *exclusive_upper_bound*)", "generating cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets"), "True"),
 ("len(__import__('hashlib').sha256(b'x').digest()) * 8", "256"),
 (has(BK, "Do not write your own code to create a random number or use a \"simple\" random number generator offered by your programming language",
      "Use a cryptographically secure pseudorandom number generator (CSPRNG) with a seed from a source of sufficient entropy",
      "Study the documentation of the random number generator library you choose to make sure it is cryptographically secure",
      "Correct implementation of the CSPRNG is critical to the security of the keys",
      "the possibility that the generating code is compromised with a \"back door.\""), "True"),
 ("(lambda r: (r.seed(7), r.random())[1] == (r.seed(7), r.random())[1])(__import__('random'))", "True"),
 ("(lambda s, n: all(1 <= (s.randbelow(n - 1) + 1) < n for _ in range(1000)))(__import__('secrets'), %s)" % NH, "True"),
]
