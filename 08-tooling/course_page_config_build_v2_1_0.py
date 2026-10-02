#!/usr/bin/env python3
"""Writes course_page_config_v2_1_0.json (the SEN0401 course configuration for template 9.24.0) and checks every program in it.
The programs are Python that really runs in the page's in-browser CPython (Pyodide): standard library only, no network, no files,
no ripemd160 (hashlib in the page's Pyodide has md5, sha1, sha2, sha3, blake2 only). Each program is executed here under every interpreter
given (default python3 and python3.14) and must exit 0 with the expected first output line, so a snippet cannot silently rot.
usage: course_page_config_build_v2_1_0.py [interpreter ...]"""
__version__ = "2.1.0"
# 2.1.0 (over 2.0.0): adds exam{} (SEN0401's own instructor public key, release prefix, bonus), codelab_snippets, sparql_samples,
# trace_examples, code_patterns (template 9.24.0 reads them), limits, and a new Playground default; keeps name, line, chapter_sub,
# chapter_intro and the empty corpus lists of 2.0.0.
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = json.load(open("/home/claude/instructor_keys/sen0401_instructor_public_key_v1_0_0.json"))["public_jwk"] if os.path.exists("/home/claude/instructor_keys/sen0401_instructor_public_key_v1_0_0.json") else json.load(open(os.path.join(HERE, "course_page_config_v2_1_0.json")))["exam"]["public_key"]

PLAYGROUND = {
    "label": "Toy proof-of-work miner (uses input)",
    "code": "import hashlib\nprefix = input('Block data: ')\nzeros = int(input('Leading zeros required: '))\nnonce = 0\nwhile not hashlib.sha256(f'{prefix}-{nonce}'.encode()).hexdigest().startswith('0' * zeros):\n    nonce += 1\nprint(f'nonce {nonce} gives', hashlib.sha256(f'{prefix}-{nonce}'.encode()).hexdigest())",
    "inputs": "SEN0401|3",
}

# (label, code, expected first line of output or None).  The ASK sample must stay at index 5: the page test selects it by position.
PATTERNS = [
 ("SHA-256 of a message", "import hashlib\nmessage = 'Bitcoin'\nprint(hashlib.sha256(message.encode()).hexdigest())",
  "b4056df6691f8dc72e56302ddad345d65fead3ead9299609a826e2344eb63aa4"),
 ("Avalanche: one letter changes about half the bits", "import hashlib\ndef bits(text):\n    return int(hashlib.sha256(text.encode()).hexdigest(), 16)\na, b = bits('Bitcoin'), bits('bitcoin')\ndiff = bin(a ^ b).count('1')\nprint(diff, 'of 256 bits differ')", None),
 ("Double SHA-256, as Bitcoin hashes a block header", "import hashlib\ndef sha256d(data):\n    return hashlib.sha256(hashlib.sha256(data).digest()).digest()\nprint(sha256d(b'hello').hex())", "9595c9df90075148eb06860365df33584b75bff782a510c6cd4883a419833d50"),
 ("Proof of work: find a nonce", "import hashlib\nblock = 'SEN0401'\nnonce = 0\nwhile not hashlib.sha256(f'{block}-{nonce}'.encode()).hexdigest().startswith('0000'):\n    nonce += 1\nprint('nonce', nonce)", "nonce 15083"),
 ("Chain of blocks: each hash covers the one before", "import hashlib\ndef h(text):\n    return hashlib.sha256(text.encode()).hexdigest()\nchain = []\nprev = '0' * 64\nfor data in ['Alice pays Bob 1', 'Bob pays Carol 2', 'Carol pays Dan 1']:\n    prev = h(prev + data)\n    chain.append(prev)\nfor i, x in enumerate(chain):\n    print(i, x[:16])", None),
 ("Tamper check: change block 1 and the later hashes change", "import hashlib\ndef h(text):\n    return hashlib.sha256(text.encode()).hexdigest()\ndef build(items):\n    prev, out = '0' * 64, []\n    for data in items:\n        prev = h(prev + data)\n        out.append(prev)\n    return out\nok = build(['a pays b 1', 'b pays c 2', 'c pays d 1'])\nbad = build(['a pays b 1', 'b pays c 9', 'c pays d 1'])\nprint([x == y for x, y in zip(ok, bad)])", "[True, False, False]"),
 ("Merkle root of four transactions", "import hashlib\ndef h(b):\n    return hashlib.sha256(hashlib.sha256(b).digest()).digest()\nlevel = [h(t.encode()) for t in ['tx1', 'tx2', 'tx3', 'tx4']]\nwhile len(level) > 1:\n    if len(level) % 2:\n        level.append(level[-1])\n    level = [h(level[i] + level[i + 1]) for i in range(0, len(level), 2)]\nprint(level[0].hex())", None),
 ("Base58 encoding of bytes", "ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\ndef b58(data):\n    n = int.from_bytes(data, 'big')\n    out = ''\n    while n:\n        n, r = divmod(n, 58)\n        out = ALPHABET[r] + out\n    zeros = len(data) - len(data.lstrip(b'\\x00'))\n    return '1' * zeros + out\nprint(b58(b'\\x00\\x00hello'))", "11Cn8eVZg"),
 ("Base58Check: a payload with a four-byte checksum", "import hashlib\nALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\ndef b58(data):\n    n = int.from_bytes(data, 'big')\n    out = ''\n    while n:\n        n, r = divmod(n, 58)\n        out = ALPHABET[r] + out\n    return '1' * (len(data) - len(data.lstrip(b'\\x00'))) + out\ndef b58check(payload):\n    check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]\n    return b58(payload + check)\nprint(b58check(b'\\x00' + bytes(20)))", "1111111111111111111114oLvT2"),
 ("Block subsidy halves every 210000 blocks", "subsidy = 50 * 10**8  # satoshi\nfor era in range(6):\n    print(f'blocks {era * 210000}-{(era + 1) * 210000 - 1}: {subsidy / 10**8} BTC')\n    subsidy //= 2", "blocks 0-209999: 50.0 BTC"),
 ("Total supply is just below 21 million", "total = sum((50 * 10**8 >> era) * 210000 for era in range(33))\nprint(total / 10**8, 'BTC')", "20999999.9769 BTC"),
 ("Compact difficulty bits to a target", "bits = 0x1d00ffff\nexponent, mantissa = bits >> 24, bits & 0xffffff\ntarget = mantissa * 256 ** (exponent - 3)\nprint(hex(target))", None),
 ("Little-endian bytes of a number", "n = 50 * 10**8\nprint(n.to_bytes(8, 'little').hex())", "00f2052a01000000"),
 ("Toy elliptic curve y^2 = x^3 + 7 over a small field", "p = 17\npoints = [(x, y) for x in range(p) for y in range(p) if (y * y - (x ** 3 + 7)) % p == 0]\nprint(len(points), 'points:', points)", None),
 ("Add two points on the toy curve", "p = 17\ndef add(P, Q):\n    if P is None: return Q\n    if Q is None: return P\n    (x1, y1), (x2, y2) = P, Q\n    if x1 == x2 and (y1 + y2) % p == 0:\n        return None\n    if P == Q:\n        s = 3 * x1 * x1 * pow(2 * y1, -1, p) % p\n    else:\n        s = (y2 - y1) * pow(x2 - x1, -1, p) % p\n    x3 = (s * s - x1 - x2) % p\n    return (x3, (s * (x1 - x3) - y1) % p)\nG = (1, 5)\nprint(G, '+', G, '=', add(G, G))", None),
 ("Scalar multiplication on the toy curve: the multiples of G", "p = 17\ndef add(P, Q):\n    if P is None: return Q\n    if Q is None: return P\n    (x1, y1), (x2, y2) = P, Q\n    if x1 == x2 and (y1 + y2) % p == 0:\n        return None\n    if P == Q:\n        s = 3 * x1 * x1 * pow(2 * y1, -1, p) % p\n    else:\n        s = (y2 - y1) * pow(x2 - x1, -1, p) % p\n    x3 = (s * s - x1 - x2) % p\n    return (x3, (s * (x1 - x3) - y1) % p)\nG, P = (1, 5), None\nfor k in range(1, 8):\n    P = add(P, G)\n    print(k, '*G =', P)", None),
 ("secp256k1: double the generator point", "p = 2**256 - 2**32 - 977\nGx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798\nGy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8\ns = 3 * Gx * Gx * pow(2 * Gy, -1, p) % p\nx = (s * s - 2 * Gx) % p\nprint(hex(x))", "0xc6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5"),
 ("Ask for a message and hash it ('abc' if left empty)", "import hashlib\ntext = input('Message: ') or 'abc'\nprint(hashlib.sha256(text.encode()).hexdigest())", None),
 ("Satoshi and bitcoin with an f-string", "sats = 123456789\nprint(f'{sats} satoshi = {sats / 10**8:.8f} BTC')", "123456789 satoshi = 1.23456789 BTC"),
 ("Check a claim with assert", "import hashlib\ndigest = hashlib.sha256(b'abc').hexdigest()\nassert digest.startswith('ba7816bf'), 'SHA-256 of abc changed'\nprint('ok', len(digest) * 4, 'bits')", "ok 256 bits"),
]
TRACE = [
 ("Chain two blocks by hand", "import hashlib\nprev = '0' * 8\nfor data in ['a pays b', 'b pays c']:\n    prev = hashlib.sha256((prev + data).encode()).hexdigest()[:8]\n    print(data, '->', prev)", None),
 ("Proof of work with one leading zero", "import hashlib\nnonce = 0\nwhile True:\n    d = hashlib.sha256(f'SEN0401-{nonce}'.encode()).hexdigest()\n    if d.startswith('0'):\n        break\n    nonce += 1\nprint(nonce, d[:12])", None),
 ("A Merkle root, level by level", "import hashlib\ndef h(a, b):\n    return hashlib.sha256((a + b).encode()).hexdigest()[:6]\nlevel = ['t1', 't2', 't3', 't4']\nwhile len(level) > 1:\n    level = [h(level[i], level[i + 1]) for i in range(0, len(level), 2)]\n    print(level)\nprint('root', level[0])", None),
 ("Halving: the subsidy era by era", "subsidy = 50.0\ntotal = 0.0\nfor era in range(4):\n    total = total + subsidy * 210000\n    subsidy = subsidy / 2\n    print(era, subsidy, total)", None),
 ("Double-and-add on a toy curve", "p = 17\ndef add(P, Q):\n    if P is None:\n        return Q\n    (x1, y1), (x2, y2) = P, Q\n    if P == Q:\n        s = 3 * x1 * x1 * pow(2 * y1, -1, p) % p\n    else:\n        s = (y2 - y1) * pow(x2 - x1, -1, p) % p\n    x3 = (s * s - x1 - x2) % p\n    return (x3, (s * (x1 - x3) - y1) % p)\nG = (1, 5)\nprint(add(G, G))", None),
 ("Base58: peel off one digit at a time", "ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\nn = 3000\nout = ''\nwhile n:\n    n, r = divmod(n, 58)\n    out = ALPHABET[r] + out\nprint(out)", None),
]
CODELAB = [
 ("How many concepts are on this page?", "print(len(PAGE['nodes']), 'concepts')", None),
 ("Print the name of every main subject", "for n in PAGE['nodes']:\n    if n['level'] == 1:\n        print(n['label'])", None),
 ("Quiz answer key", "for q in PAGE['quiz']:\n    print(q['q'], '->', q['options'][q['answer']])", None),
 ("Re-run every example on this page", "for n in PAGE['nodes']:\n    if n.get('io'):\n        got = repr(eval(n['io']['code']))\n        print('same' if got == n['io']['out'] else 'DIFFERENT', '|', n['label'], '|', n['io']['code'], '->', got)", None),
 ("Fingerprint every concept with SHA-256", "import hashlib\nfor n in PAGE['nodes']:\n    if n['level'] == 3:\n        print(hashlib.sha256(n['body'].encode()).hexdigest()[:12], n['label'])", None),
 ("Merkle root of all concept labels (a fingerprint of the page)", "import hashlib\ndef h(b):\n    return hashlib.sha256(hashlib.sha256(b).digest()).digest()\nlevel = [h(n['label'].encode()) for n in PAGE['nodes']]\nwhile len(level) > 1:\n    if len(level) % 2:\n        level.append(level[-1])\n    level = [h(level[i] + level[i + 1]) for i in range(0, len(level), 2)]\nprint('leaves:', len(PAGE['nodes']))\nprint('root:', level[0].hex())", None),
 ("Chain the concepts: change one text and every later hash changes", "import hashlib\ndef chain(texts):\n    prev, out = '0' * 64, []\n    for t in texts:\n        prev = hashlib.sha256((prev + t).encode()).hexdigest()\n        out.append(prev)\n    return out\ntexts = [n['body'] for n in PAGE['nodes'] if n['level'] == 3]\nok = chain(texts)\ntexts[1] = texts[1] + ' (edited)'\nbad = chain(texts)\nprint([a == b for a, b in zip(ok, bad)][:8])", None),
 ("Mine the page title: a nonce for three leading zeros", "import hashlib\nnonce = 0\nwhile not hashlib.sha256(f\"{PAGE['title']}-{nonce}\".encode()).hexdigest().startswith('000'):\n    nonce += 1\nprint('nonce', nonce)", None),
 ("Advanced: concepts per subject (dictionary, function, Counter)", "from collections import Counter\nnodes = {n['id']: n for n in PAGE['nodes']}\ndef subject(n):\n    while n['parent']:\n        n = nodes[n['parent']]\n    return n['label']\nCounter(subject(n) for n in PAGE['nodes'] if n['level'] == 3)", None),
 ("Advanced: relations by type (Counter)", "from collections import Counter\nCounter(r['type'] for r in PAGE['relations'])", None),
 ("Advanced: concepts that mention a word (list comprehension)", "word = 'hash'\n[n['label'] for n in PAGE['nodes'] if word in (n['body'] + ' ' + (n.get('definition') or '')).lower()]", None),
]
SPARQL = [
 ("Classes and their parents in this chapter", "{PFX}SELECT ?class ?label ?parentLabel WHERE {\n  GRAPH ?g { ?class a owl:Class ; rdfs:label ?label .\n    OPTIONAL { ?class rdfs:subClassOf ?p . ?p rdfs:label ?parentLabel } }\n  FILTER(CONTAINS(STR(?g), \":chapter:\"))\n} ORDER BY ?parentLabel ?label"),
 ("Concepts and their definitions", "{PFX}SELECT ?concept ?definition WHERE {\n  GRAPH ?g { ?s a owl:NamedIndividual ; rdfs:label ?concept ; skos:definition ?definition }\n  FILTER(CONTAINS(STR(?g), \":chapter:\"))\n} ORDER BY ?concept"),
 ("Computations the chapter checks and what they give", "{PFX}SELECT ?example ?input ?output WHERE {\n  GRAPH ?g { ?io ?pi ?input ; ?po ?output ; rdfs:label ?example .\n    FILTER(STRENDS(STR(?pi), \"#input\") && STRENDS(STR(?po), \"#output\")) }\n}"),
 ("Research findings and what they say", "{PFX}SELECT ?finding ?text WHERE {\n  GRAPH ?g { ?f a <http://example.org/sen0401#Finding> ; rdfs:label ?finding ; <http://example.org/sen0401#findingText> ?text }\n} ORDER BY ?finding"),
 ("Triples in each corpus file", "SELECT ?file (COUNT(*) AS ?triples) WHERE { GRAPH ?file { ?s ?p ?o } } GROUP BY ?file ORDER BY DESC(?triples)"),
 ("Does the chapter define a class labelled \"{FIRST_LEAF}\"?", "{PFX}ASK { GRAPH ?g { ?c a owl:Class ; rdfs:label ?l . FILTER(LCASE(STR(?l)) = \"{FIRST_LEAF}\") } }"),
 ("Sources the research cites", "{PFX}SELECT ?source ?address WHERE {\n  GRAPH ?g { ?p a <http://example.org/rdodi/research-ontology#Publication> ; rdfs:label ?source ; <http://purl.org/dc/terms/source> ?address }\n} ORDER BY ?source"),
]
LIMITS = ["The hashing, Base58 and elliptic-curve programs on this page are teaching models: they use the standard library only, handle no real keys or coins, and must never be used to protect value. Real wallets use audited libraries and secure random numbers."]

CFG = {
 "_version": "2.1.0",
 "name": "SEN0401 Block Chain",
 "line": "SEN0401 Block Chain",
 "chapter_sub": "chapter {n} of Mastering Bitcoin, 3rd edition",
 "chapter_intro": "Chapter {n} of <i>Mastering Bitcoin</i>, 3rd edition (Antonopoulos and Harding, 2023), free under CC BY-SA 4.0, renewed for SEN0401.",
 "playground": PLAYGROUND,
 "codelab_snippets": [[a, b] for a, b, _ in CODELAB],
 "sparql_samples": [[a, b] for a, b in SPARQL],
 "trace_examples": [[a, b] for a, b, _ in TRACE],
 "code_patterns": [[a, b] for a, b, _ in PATTERNS],
 "limits": LIMITS,
 "exam": {"course": "SEN0401", "title": "SEN0401 Special Topics: Block Chain", "release_prefix": "sen0401-exam-release", "public_key": PUB, "bonus_points": 10},
 "corpus": {
  "book": [],
  "course": [],
  "note": "SEN0401 has no textbook ontology for Mastering Bitcoin and no course ontology yet; the agents search the chapter's ontology, document and research record and the page itself."
 }
}

def run_checks(interps):
    page = "PAGE = {'title': 'T', 'nodes': [{'id': 'a', 'label': 'A', 'level': 1, 'parent': None, 'body': 'hash text'}, {'id': 'b', 'label': 'B', 'level': 3, 'parent': 'a', 'body': 'second', 'definition': 'd', 'io': {'code': '1+1', 'out': '2'}}, {'id': 'c', 'label': 'C', 'level': 3, 'parent': 'a', 'body': 'third'}], 'quiz': [{'q': 'q', 'options': ['x', 'y'], 'answer': 1}], 'relations': [{'type': 't'}]}\n"
    bad = []
    for kind, rows, pre in (("pattern", PATTERNS, ""), ("trace", TRACE, ""), ("codelab", CODELAB, page)):
        for label, code, expect in rows:
            for py in interps:
                src = pre + code
                r = subprocess.run([py, "-c", src], capture_output=True, text=True, timeout=60, input="\n\n")
                first = r.stdout.splitlines()[0] if r.stdout.splitlines() else ""
                if r.returncode != 0:
                    bad.append((kind, label, py, r.stderr.strip().splitlines()[-1:]))
                elif expect is not None and first != expect:
                    bad.append((kind, label, py, "expected %r got %r" % (expect, first)))
    return bad

if __name__ == "__main__":
    interps = sys.argv[1:] or ["python3", "/root/.local/bin/python3.14"]
    bad = run_checks(interps)
    n = len(PATTERNS) + len(TRACE) + len(CODELAB)
    print("%d programs x %d interpreters (%s): %s" % (n, len(interps), ", ".join(interps), "all ran" if not bad else "FAILURES"))
    for b in bad: print(" -", b)
    if bad: sys.exit(1)
    out = os.path.join(HERE, "course_page_config_v2_1_0.json")
    json.dump(CFG, open(out, "w"), indent=1, ensure_ascii=False)
    print("wrote", out)
