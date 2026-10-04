"""SEN0401 chapter 4, executed claims, part D (version 1.1.0): scripts and the legacy addresses."""
from sen0401_ch04_checkhelp_v1_1_0 import *
from sen0401_ch04_checks_a_v1_1_0 import BK, KH, NH, XH, YH, PUB
B16 = rd(S1 + "bip-0016.mediawiki")
R791, R3022 = rd(S2 + "rfc791.txt"), rd(S2 + "rfc3022.txt")
VA = evj("core_validateaddress_31_1_v1_0_0.json")
DERIVE = ev("core_deriveaddresses_31_1_v1_0_0.txt")
HASHRATE = evj("hashrate_v1_0_0.json")
SCRIPTH = core("src/script/script.h")
BK13 = book("ch13_security.adoc")
KHX = KH[2:]
H160C, H160U = "bbc1e42a39d05a4cc61752d6963b7f69d09bb27b", "211b74ca4686f81efda5641767fc84ef16dafe0b"
ADDR_C, ADDR_U, ADDR_S = "1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy", "1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x", "3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM"
D_ = lambda s, **kw: X(s, KHX=KHX, H160C=H160C, H160U=H160U, ADDRC=ADDR_C, ADDRU=ADDR_U, ADDRS=ADDR_S, SCR=SCRIPTH, **kw)
OPS = "{m.group(1): int(m.group(2), 16) for m in __import__('re').finditer(r'(OP_\\w+) = (0x[0-9a-fA-F]+)', %s)}" % SCRIPTH

CHECKS_D = [
 # ---- the branch: address
 (has(BK, "The shortest version of Bitcoin public keys known to the developers of early Bitcoin were 65 bytes, the equivalent of 130 characters when written in hexadecimal",
      "any mistake made in copying a commitment would result in the bitcoins being sent to an unspendable output, causing them to be lost forever"), "True"),
 (has(prev("01"), "Bitcoin address"), "True"),
 (has(prev("02"), "output"), "True"),
 (has(prev("01"), "full node"), "True"),
 # ---- scripts
 (has(BK, "the first version of Bitcoin instead had payments sent to a field called _output script_ and had spends of those bitcoins authorized by a field called _input script_",
      "These fields allow additional operations to be performed in addition to (or instead of) verifying that a signature corresponds to a public key",
      "an output script can contain two public keys and require two corresponding signatures be placed in the spending input script",
      "bitcoins are received to an output script that acts like a public key, and bitcoin spending is authorized by an input script that acts like a signature"), "True"),
 (D_("(len(bytes.fromhex('76a914$H160C' + '88ac')), bytes.fromhex('76a914$H160C' + '88ac')[0], bytes.fromhex('76a914$H160C' + '88ac')[1], bytes.fromhex('76a914$H160C' + '88ac')[2], bytes.fromhex('76a914$H160C' + '88ac')[-2:])"),
  "(25, 118, 169, 20, b'\\x88\\xac')"),
 ("%s['%s']['scriptPubKey']" % (VA, ADDR_C), "'76a914%s88ac'" % H160C),
 (X("(lambda ops: (ops['OP_DUP'], ops['OP_HASH160'], ops['OP_EQUAL'], ops['OP_EQUALVERIFY'], ops['OP_CHECKSIG'], ops['OP_CHECKSIGVERIFY'], ops['OP_CHECKMULTISIG'], ops['OP_1'], ops['OP_16']))($OPS)", OPS=OPS),
  "(118, 169, 135, 136, 172, 173, 174, 81, 96)"),
 (D_("(lambda T: bytes([0x76, 0xa9, 20]) + T.hash160(T.pub_bytes(T.ec_mul(0x$KHX))) + bytes([0x88, 0xac]))($T).hex()"), "'76a914%s88ac'" % H160C),
 (has(B16, "scriptPubKey", "scriptSig", "Layer: Consensus (soft fork)"), "True"),
 (has(BK, "If the output script is not exactly +OP_HASH160 <20 bytes> OP_EQUAL+, the redeem script will not be used and any bitcoins may either be unspendable or spendable by anyone (meaning anyone can take them)"), "True"),
 (has(B16, "Validation fails if there are any operations other than \"push data\" operations in the scriptSig"), "True"),
 (has(BK, "each piece of data (shown in angle brackets) is placed at the top of a list of items, called a stack", "When an operation code (opcode) is encountered, it uses items from the stack, starting with the topmost items",
      "If there's a nonzero item on top of the stack at the end of evaluation, the script passes", "If all scripts in a transaction pass, and all of the other details about the transaction are valid, then full nodes will consider the transaction to be valid",
      "The +OP_CHECKSIG+ operation consumes two elements, starting with the public key and followed by the signature, removing them from the stack",
      "If the signature is correct, +OP_CHECKSIG+ replaces itself on the stack with the value 1; if the signature was not correct, it replaces itself with a 0",
      "The +OP_DUP+ operation duplicates the top item", "The +OP_HASH160+ operation consumes (removes) the top public key and replaces it with the result of hashing it",
      "The +OP_EQUALVERIFY+ operation consumes the top two items and verifies that they are equal", "If +OP_EQUALVERIFY+ fails, the whole script fails",
      "It verifies the signature corresponds to the public key and also commits to (signs) the various fields in the transaction"), "True"),
 ("(lambda s: (s.append(s[-1]), s)[1])(['sig', 'pub'])", "['sig', 'pub', 'pub']"),
 # the book prints OP_EQUAL in the output script of P2PKH and OP_EQUALVERIFY in the combined script
 (has(BK, "OP_DUP OP_HASH160 <Bob's commitment> OP_EQUAL OP_CHECKSIG", "<sig> <pubkey> OP_DUP OP_HASH160 <commitment> OP_EQUALVERIFY OP_CHECKSIG"), "True"),
 (D_("(lambda T: (lambda pub: (T.run_p2pkh('S', pub, T.hash160(pub)) == ['S', pub], T.run_p2pkh('S', pub, T.hash160(pub + b'x')), T.run_p2pkh('S', pub, bytes(20))))(T.pub_bytes(T.ec_mul(0x$KHX))))($T)"), "(True, False, False)"),
 (D_("(lambda T: (lambda d, z, k: (lambda Q, sig: (T.ecdsa_verify(Q, z, sig), T.ecdsa_verify(Q, z + 1, sig), T.ecdsa_verify(T.ec_mul(d + 1), z, sig)))(T.ec_mul(d), T.ecdsa_sign(d, z, k)))(0x$KHX, 777, 424242))($T)"), "(True, False, False)"),
 (X("$SCR", SCR=SCRIPTH) + ".count('OP_CHECKSIGVERIFY = 0xad') + " + SCRIPTH + ".count('MAX_PUBKEYS_PER_MULTISIG = 20')", "2"),
 (has(core("src/script/interpreter.cpp"), "case OP_CHECKSIGVERIFY:", "if (opcode == OP_CHECKSIGVERIFY)", "return set_error(serror, SCRIPT_ERR_CHECKSIGVERIFY);"), "True"),
 # ---- legacy
 (has(BK, "P2PKH and P2SH are the only two script templates used with base58check encoding. They are now known as legacy addresses and have become less common over time. Legacy addresses were supplanted by the bech32 family of addresses",
      "Although we do not believe there is any immediate threat to anyone creating new P2SH addresses, we recommend all new wallets use newer types of addresses to eliminate address collision attacks as a concern"), "True"),
 # ---- payment to an IP address
 (has(R791, "transmitting blocks of data called datagrams from sources to destinations, where sources and destinations are hosts identified by fixed length addresses"), "True"),
 (has(R791, "four octets (32 bits)"), "True"),
 ("(2 ** 32, 4 * 8)", "(4294967296, 32)"),
 (has(R3022, "IP addresses are mapped from one group to another, transparent to end users", "connect a realm with private addresses to an external realm with globally unique registered addresses"), "True"),
 (has(BK, "If Alice entered Bob's IP address in Bitcoin 0.1, her full node would establish a connection with his full node and receive a new public key from Bob's wallet that his node had never previously given anyone"), "True"),
 (has(BK, "Instead of direct public key entry, the earliest version of Bitcoin software allowed a spender to enter the receiver's IP address", "This feature was later removed--there are many problems with using IP addresses",
      "her full node would establish a connection with his full node and receive a new public key from Bob's wallet that his node had never previously given anyone",
      "different transactions paying Bob couldn't be connected together by someone looking at the blockchain and noticing that all of the transactions paid the same public key",
      "no widely used program has supported IP address payments for almost a decade", "One particular downside is that the receiver needs their wallet to be online at their IP address, and it needs to be accessible from the outside world",
      "They turn their computers off at night, their laptops go to sleep, they're behind firewalls, or they're using Network Address Translation (NAT)"), "True"),
 # ---- P2PK
 (has(BK, "<Bob's public key> OP_CHECKSIG", "<Bob's signature>", "This type of output is known today as _pay to public key_, or _P2PK_ for short. It was never widely used for payments",
      "the preceding script uses the same public key and signature described in the original paper but adds in the complexity of two script fields and an opcode"), "True"),
 ("(lambda s: (s.pop(), s.pop(), s.append(1), s)[3])(['<Bob signature>', '<Bob public key>'])", "[1]"),
 ("(65, 20, 65 > 20)", "(65, 20, True)"),
 # ---- commitment
 (has(BK, "Now imagine that we ask Bob the question, \"what is your public key?\" Bob can use a hash function to give us a cryptographically secure commitment to his public key",
      "we can be sure it was the exact same key that was used to create that earlier commitment", "in what year did Satoshi Nakamoto start working on Bitcoin"), "True"),
 (D_("(lambda T: (len(T.hash160(T.pub_bytes(T.ec_mul(0x$KHX)))), len(T.pub_bytes(T.ec_mul(0x$KHX), False))))($T)"), "(20, 65)"),
 # ---- P2PKH address
 (has(BK, "Although this process of paying to a public key hash (_P2PKH_) may seem convoluted, it allows Alice's payment to Bob to contain only a 20 byte commitment to his public key instead of the key itself, which would've been 65 bytes in the original version of Bitcoin",
      "That's a lot less data for Bob to have to communicate to Alice", "prefix zero (0x00 in hex) indicates that the data should be used as the commitment (hash) in a legacy P2PKH output script"), "True"),
 (D_("(lambda T: (T.b58check_decode('$ADDRC').hex(), T.b58check_decode('$ADDRU').hex(), T.b58check_decode('$ADDRC')[0], len(T.b58check_decode('$ADDRC')[1:])))($T)"),
  "('00%s', '00%s', 0, 20)" % (H160C, H160U)),
 (X("[ln.split(' => ')[1] for ln in $DERIVE.splitlines() if ln.startswith('pkh(')]", DERIVE=ev("core_deriveaddresses_31_1_v1_0_0.txt")), "['1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy', '1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x', '1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x', '1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy']"),
 (X("[(c, v['isvalid']) for c, v in $VA.items() if c in ('%s', '%s')]" % (ADDR_C, ADDR_U), VA=VA), "[('1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy', True), ('1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x', True)]"),
 # ---- redeem script and multisig
 (has(BK, "The BIP16 upgrade to the Bitcoin protocol in 2012 allows an output script to commit to a _redemption script_ (_redeem script_)",
      "his input script needs to provide a redeem script that matches the commitment and also any data necessary to satisfy the redeem script (such as signatures)",
      "<public key 1> OP_CHECKSIGVERIFY <public key 2> OP_CHECKSIG", "RIPEMD160(SHA256(script))", "OP_HASH160 <commitment> OP_EQUAL",
      "<signature2> <signature1> <redeem script>", "they'll verify that the serialized redeem script will hash to the same value as the commitment",
      "Then they'll replace it on the stack with its deserialized value", "one signature from his desktop wallet and one from a hardware signing device",
      "thousands of bytes for which she needs to pay transaction fees every time she wants to spend money to Bob"), "True"),
 (has(B16, "The purpose of pay-to-script-hash is to move the responsibility for supplying the conditions to redeem a transaction from the sender of the funds to the redeemer",
      "the ''serialized script'' - also referred to as the ''redeemScript''", "no data greater than 520 bytes may be pushed to the stack",
      "with 33-byte compressed pubkeys it is only possible to spend a P2SH output requiring a maximum of 15 pubkeys to redeem: 3 bytes + 15 pubkeys * 34 bytes/pubkey = 513 bytes",
      "{2 [pubkey1] [pubkey2] [pubkey3] 3 OP_CHECKMULTISIG}", "While the OP_CHECKMULTISIG opcode can itself accept up to 20 pubkeys".replace("While", "For instance while").replace("For instance while the", "For instance while the"),
      "All other OP_CHECKMULTISIG and OP_CHECKMULTISIGVERIFY are counted as 20 signature operations", "contribute to the maximum number allowed per block (20,000)"), "True"),
 (has(BK13, "a Bitcoin hardware signing device only needs to hold keys and use them to generate signatures", "Without general-purpose software to compromise and with limited interfaces, hardware signing devices can deliver strong security to nonexpert users", "Hardware signing devices may become the predominant method of storing bitcoins"), "True"),
 (has(BK, "P2SH is not necessarily the same as a multisignature transaction. A P2SH address _most often_ represents a multisignature script, but it might also represent a script encoding other types of transactions"), "True"),
 ("(3 + 15 * 34, 3 + 16 * 34, 3 + 15 * 34 <= 520 < 3 + 16 * 34, 1 + 3 * 34 + 2)", "(513, 547, True, 105)"),
 ("len(bytes([0x52]) + b''.join(bytes([33]) + bytes(33) for _ in range(3)) + bytes([0x53, 0xae]))", "105"),
 (D_("(lambda T: len(bytes.fromhex('a914' + '9314bd593b869c78a539b93810eefe8d296f5157' + '87')))($T)"), "23"),
 (X("(lambda ops: (ops['OP_HASH160'], ops['OP_EQUAL']))($OPS)", OPS=OPS), "(169, 135)"),
 # ---- P2SH address
 (has(BK, "Addresses for P2SH are also created with base58check. The version prefix is set to 5, which results in an encoded address starting with a +3+", "An example of a P2SH address is +3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM+"), "True"),
 (D_("(lambda T: (T.b58check_decode('$ADDRS')[0], T.b58check_decode('$ADDRS')[1:].hex(), len(T.b58check_decode('$ADDRS')[1:])))($T)"), "(5, '9314bd593b869c78a539b93810eefe8d296f5157', 20)"),
 ("(%s['%s']['scriptPubKey'], %s['%s']['isscript'])" % (VA, ADDR_S, VA, ADDR_S), "('a9149314bd593b869c78a539b93810eefe8d296f515787', True)"),
 ("(%s['%s']['scriptPubKey'][:2], %s['%s']['scriptPubKey'][-2:])" % (VA, ADDR_S, VA, ADDR_S), "('a9', '87')"),
 (D_("(lambda T: T.p2sh(bytes.fromhex('00') ) [0])($T)"), "'3'"),
 (has(B16, "These new rules should only be applied when validating transactions in blocks with timestamps >= 1333238400 (Apr 1 2012)", "put the string \"/P2SH/\" in the input of the coinbase transaction for blocks that they create",
      "The benefit is allowing a sender to fund any arbitrary transaction, no matter how complicated, using a fixed-length 20-byte hash that is short enough to scan from a QR code or easily copied and pasted",
      "validation fails immediately if it does not match the hash in the outpoint", "the transaction is validated again using the popped stack and the deserialized script as the scriptPubKey".replace("the transaction", "{serialized script} is popped off the initial stack, and the transaction")), "True"),
 ("__import__('datetime').datetime.fromtimestamp(1333238400, __import__('datetime').timezone.utc).isoformat()", "'2012-04-01T00:00:00+00:00'"),
 # ---- preimage, second preimage, collision
 (has(BK, "if they find the input the same way the original user did, they'll know the user's private key and be able to spend that user's bitcoins",
      "For a secure 160-bit algorithm like HASH160, the probability is 1-in-2^160^. This is a _preimage attack_",
      "the chance of an attacker generating a different input for an existing commitment is also about 1-in-2^160^ for the HASH160 algorithm. This is a _second preimage attack_",
      "an attacker participates in the creation of a multisignature script where they don't need to submit their public key until after they learn all of the other partys' public keys",
      "the strength of hash algorithm is reduced to its square root. For HASH160, the probability becomes 1-in-2^80^. This is a _collision attack_",
      "all Bitcoin miners combined execute about 2^80^ hash functions every hour", "They run a different hash function than HASH160, so their existing hardware can't create collision attacks for it",
      "the existence of the Bitcoin network proves that collision attacks against 160-bit functions like HASH160 are practical",
      "there are organizations that expect to receive billions of dollars in bitcoins to addresses generated by processes involving multiple parties, which could make the attack profitable",
      "a simple solution that doesn't require any special knowledge on the part of wallet developers is to simply use a stronger hash function",
      "newer Bitcoin addresses provide at least 128 bits of collision resistance", "To perform 2^128^ hash operations would take all current Bitcoin miners about 32 billion years"), "True"),
 ("(2 ** 160, len(str(2 ** 160)), float(1 / 2 ** 160))", "(1461501637330902918203684832716283019655932542976, 49, 6.842277657836021e-49)"),
 ("(2 ** 80 / 8766 > 1e20, round(2 ** 80 / 8766 / 1e20, 2))", "(True, 1.38)"),
 ("(2 ** 160) ** 0.5 == 2 ** 80", "True"),
 ("(lambda yr: round(2 ** 128 / 2 ** 80 / yr / 1e9, 1))(24 * 365.25)", "32.1"),
 (X("(lambda hr: (round(hr['currentHashrate'] * 3600 / 2 ** 80, 2), round(2 ** 128 / (hr['currentHashrate'] * 3600) / (24 * 365.25) / 1e9, 1)))($HR)", HR=HASHRATE), "(2.83, 11.4)"),
 (X("$HR['read']", HR=HASHRATE), "'2026-09-28'"),
 ("(lambda f: f(__import__('hashlib').sha256))(lambda H: (lambda seen: next((i, seen[h]) for i in range(2 ** 20) for h in [H(str(i).encode()).digest()[:4]] if (h in seen) or seen.setdefault(h, i) < 0))({}))", "(95303, 69235)"),
 ("(2 ** 16, 2 ** 32, round(95303 / 2 ** 16, 2))", "(65536, 4294967296, 1.45)"),
 ("(256 // 2, 160 // 2)", "(128, 80)"),
 # the behaviour of OP_CHECKSIGVERIFY in the script interpreter of Bitcoin Core at the checked-out commit
 (has(core("src/script/interpreter.cpp"), "case OP_CHECKSIG: case OP_CHECKSIGVERIFY:", "stack.push_back(fSuccess ? vchTrue : vchFalse);",
      "if (opcode == OP_CHECKSIGVERIFY) { if (fSuccess) popstack(stack); else return set_error(serror, SCRIPT_ERR_CHECKSIGVERIFY); }"), "True"),
]
