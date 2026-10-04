"""Every number, date, hash and computed result that the chapter 1 text (version 1.2.0) quotes outside its worked examples, as
(expression, expected repr) pairs that the chapter builder executes. Nothing here is copied from memory: each pair is the arithmetic
the prose states, so that a wrong figure in the text stops the build."""
_SRC = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "ch01-sources") + "/"
_J = lambda name: "__import__('json').load(open(%r))" % (_SRC + name)
_DT = "__import__('datetime')"
_HL = "__import__('hashlib')"

NUM = [
 # ---- the unit and the supply ----
 ("int(__import__('decimal').Decimal('0.001') * 10**8)", "100000"),                      # 0.001 BTC is 100,000 satoshis
 ("0.001 * 10**3", "1.0"),                                                               # ... and 1 millibitcoin
 ("21_000_000 * 10**8", "2100000000000000"),                                             # the cap, counted in satoshis
 ("sum((50 * 10**8 >> era) * 210000 for era in range(33)) / 10**8", "20999999.9769"),    # the real total ever issued
 ("round(21_000_000 - sum((50 * 10**8 >> era) * 210000 for era in range(33)) / 10**8, 4)", "0.0231"),
 ("(50 * 10**8) >> 33", "0"),                                                            # the 34th era pays nothing
 ("33 * 210000", "6930000"),                                                             # the height at which the subsidy ends
 ("840000 // 210000", "4"),                                                              # four halvings by block 840000
 ("(50 * 10**8) >> 4", "312500000"),                                                     # 3.125 bitcoin, in satoshis
 ("[(50 * 10**8 >> h // 210000) for h in (0, 210000, 420000, 630000, 840000)]",
  "[5000000000, 2500000000, 1250000000, 625000000, 312500000]"),
 ("round(210000 * 10 / 60 / 24 / 365.25, 2)", "3.99"),                                   # 210,000 blocks of 10 minutes: just under 4 years
 # the script the chapter leaves as a comment: the block at which 99 per cent of all bitcoin has been issued
 ("(lambda g: (exec('total = 0.0\\nfor i in range(0, 10_000_000):\\n    total += 50 / (2 ** int(i / 210000))\\n    if total / 21e6 > 0.99:\\n        result = i\\n        break', g), g['result'])[1])({})", "1411200"),
 ("312_500_000 + 12_500_000", "325000000"),                                              # the most a block at height 840000 may claim
 # ---- dates read from the saved block data ----
 ("%s['timestamp']" % _J("block0.json"), "1231006505"),
 ("%s['timestamp']" % _J("block840000.json"), "1713571767"),
 ("str(%s.datetime.fromtimestamp(%s['timestamp'], %s.timezone.utc))" % (_DT, _J("block840000.json"), _DT), "'2024-04-20 00:09:27+00:00'"),
 ("str((%s.datetime.fromtimestamp(%s['timestamp'], %s.timezone.utc) + %s.timedelta(seconds=6_930_000 * 600)).date())" % (_DT, _J("block0.json"), _DT, _DT), "'2140-10-08'"),
 ("%s['height']" % _J("block840000.json"), "840000"),
 # ---- the two block hashes and the difficulty they show ----
 ("len(%s['id']) - len(%s['id'].lstrip('0'))" % (_J("block0.json"), _J("block0.json")), "10"),
 ("len(%s['id']) - len(%s['id'].lstrip('0'))" % (_J("block840000.json"), _J("block840000.json")), "19"),
 ("%s['id'][:12]" % _J("block0.json"), "'000000000019'"),
 # ---- the price example ----
 ("round(0.001 * 60000, 2)", "60.0"),
 ("sum(p * v for p, v in [(100, 3), (104, 1)]) / sum(v for p, v in [(100, 3), (104, 1)])", "101.0"),
 ("(100 + 104) / 2", "102.0"),                                                           # the simple average, for comparison
 # ---- proof of work and Hashcash ----
 ("next(n for n in range(10**6) if %s.sha256(f'SEN0401-{n}'.encode()).hexdigest().startswith('0000'))" % _HL, "15083"),
 ("len([n for n in range(15084) if True])", "15084"),                                    # attempts made, counting the successful one
 ("%s.sha256(b'SEN0401-15083').hexdigest()[:8]" % _HL, "'0000a1fa'"),
 ("16 ** 4", "65536"),                                                                   # expected attempts for four zero digits
 ("format(int(%s.sha256(b'SEN0401-15083').hexdigest(), 16), '0256b').index('1')" % _HL, "16"),
 # ---- mining pace and difficulty ----
 ("24 * 60 // 10", "144"),                                                               # blocks a day at the target pace
 ("10 * 60", "600"),
 ("14 * 24 * 60 * 60", "1209600"),
 ("14 * 24 * 60 * 60 // (10 * 60)", "2016"),                                             # blocks in a retarget period
 # ---- hashes, keys, entropy, checksum, stretching ----
 ("%s.sha256(b'abc').hexdigest()" % _HL, "'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'"),
 ("bin(int(%s.sha256(b'abc').hexdigest(), 16) ^ int(%s.sha256(b'abd').hexdigest(), 16)).count('1')" % (_HL, _HL), "122"),
 ("len(%s.sha256(b'').digest())" % _HL, "32"),
 ("len(%s.sha256(b'').hexdigest())" % _HL, "64"),
 ("256 // 4", "64"),                                                                     # a 256-bit value is 64 hexadecimal digits
 ("len(str(2**256))", "78"),
 ("2 ** 11", "2048"),
 ("12 * 11", "132"),
 ("128 + 128 // 32", "132"),
 ("[(ent, ent // 32, (ent + ent // 32) // 11) for ent in (128, 160, 192, 224, 256)]",
  "[(128, 4, 12), (160, 5, 15), (192, 6, 18), (224, 7, 21), (256, 8, 24)]"),
 ("%s.sha256(bytes(16)).digest()[0] >> 4" % _HL, "3"),
 ("format(%s.sha256(bytes(16)).digest()[0] >> 4, '04b')" % _HL, "'0011'"),
 ("2 ** 4, 2 ** 8", "(16, 256)"),                                                        # odds a 4-bit and an 8-bit checksum miss
 ("len(%s.pbkdf2_hmac('sha512', b'abandon', b'mnemonic', 2048))" % _HL, "64"),
 # the derivation the worked example builds out of the keyed hash is the real PBKDF2 of the standard
 ('(lambda g: (exec("import hmac, hashlib\\npassword, salt, iters = b\'abandon\', b\'mnemonic\', 2048\\nu = hmac.new(password, salt + bytes([0, 0, 0, 1]), \'sha512\').digest()\\nseed = u\\nfor _ in range(iters - 1):\\n    u = hmac.new(password, u, \'sha512\').digest()\\n    seed = bytes(a ^ b for a, b in zip(seed, u))\\nresult = (seed == hashlib.pbkdf2_hmac(\'sha512\', password, salt, iters), seed.hex()[:8])", g), g[\'result\'])[1])({})', "(True, 'd96147bf')"),
 ("512 // 8", "64"),
 # ---- the toy key pair ----
 ("61 * 53", "3233"),
 ("60 * 52", "3120"),
 ("(17 * 2753) % 3120", "1"),
 ("pow(65, 2753, 3233)", "588"),
 ("pow(pow(65, 17, 3233), 2753, 3233)", "65"),
 # ---- the payment of the story ----
 ("sum([110000]) - sum([100000, 5000])", "5000"),                                        # the fee of the example transaction
 ("110_000 - 100_000", "10000"),
 ("int(__import__('decimal').Decimal('0.01577764') * 10**8)", "1577764"),
 # ---- confirmations: the whitepaper's own figure ----
 ("(lambda m, q, z: (lambda p: (lambda l: round(1 - sum(m.exp(-l) * l**k / m.factorial(k) * (1 - (q / p)**(z - k)) for k in range(z + 1)), 7))(z * q / p))(1 - q))(__import__('math'), 0.1, 6)", "0.0002428"),
 # ---- the QR code ----
 ("[21 + 4 * (v - 1) for v in (1, 40)]", "[21, 177]"),
 # ---- the gossip example of the peer-to-peer network ----
 ("len({'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'E'], 'D': ['B', 'F'], 'E': ['C', 'F'], 'F': ['D', 'E', 'G'], 'G': ['F']})", "7"),
 # ---- the payment channel ----
 ("(60_000 - 100 * 10, 40_000 + 100 * 10)", "(59000, 41000)"),
 ("60_000 + 40_000", "100000"),
 # ---- the Byzantine Generals' Problem: the bound of the 1982 paper ----
 ("3 * 1 + 1", "4"),                                                                     # m traitors need more than 3m generals
]
