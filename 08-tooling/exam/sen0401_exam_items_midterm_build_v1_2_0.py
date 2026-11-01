#!/usr/bin/env python3
"""SEN0401 midterm items, builder of version 1.2.0 (new file) and of the exam structure v1.0.0.

Owner's rules of 2026-11-01 13:04 (relayed by the coordinator): never ask memorising questions; never require a student to recall a specific term; if a term is used, a short tip
(what it is) is printed with it; every abbreviation is spelled out in full at first use; ask about the USE, the IMPORTANCE and the REASON things exist in Bitcoin; items of the
cs_encode type may stay when the rule is given inside the question. Five question formats: four questions of 25 points and a fifth bonus question of 10 points.

Input (read only, never edited): sen0401_exam_items_midterm_v1_1_0.json (23 items, 24 units).
Output (new files): sen0401_exam_items_midterm_v1_2_0.json, sen0401_exam_structure_v1_0_0.json, sen0401_exam_items_midterm_audit_v1_2_0.txt/.json,
                    sen0401_exam_items_midterm_computed_v1_2_0.txt.
Every computed value (sums, answers of traces, tables, fee, factor, entropy) is computed HERE by a program and asserted against the text of the item; nothing is typed in by hand.
The audit verdicts (memorisation / abbreviation / term without tip / KEEP-REWRITE-REPLACE) are the result of a full reading of the 23 items by the author, not of a name heuristic;
they are data in this file (AUDIT) and the file prints the counts by chapter from them.

Usage: build_v1_2_0.py [--outdir DIR]   (default: this folder; refuses to overwrite)
"""
import json, os, sys, io, contextlib, random
from math import exp, factorial
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_1_0.json')
VERSION = '1.2.0'
LOG = []


def log(*a): LOG.append(' '.join(str(x) for x in a))


def run(code, ns=None):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code, '<item>', 'exec'), dict(ns or {}))
    return buf.getvalue().strip()


# ------------------------------------------------------------------ real implementations used to compute and to check the numbers
def cs_real(n):
    if n < 0xfd: return n.to_bytes(1, 'little')
    if n <= 0xffff: return b'\xfd' + n.to_bytes(2, 'little')
    if n <= 0xffffffff: return b'\xfe' + n.to_bytes(4, 'little')
    return b'\xff' + n.to_bytes(8, 'little')


def cs_encode(n): return cs_real(n)


def catch_up(q, z):
    p = 1 - q; lam = z * q / p; s = 0.0
    for k in range(z + 1): s += (lam ** k * exp(-lam) / factorial(k)) * (1 - (q / p) ** (z - k))
    return 1 - s


def node_start(file_opts, cmd_opts):
    """The rules the chapter teaches: a command-line option replaces the same option of the file for that run; a node with pruning on and a transaction index on refuses to start."""
    o = dict(file_opts); o.update(cmd_opts)
    if o.get('prune', 0) and o.get('txindex', 0): return 'refuses'
    return 'starts: prune=%s txindex=%s dbcache=%s' % (o.get('prune'), o.get('txindex'), o.get('dbcache'))


# ------------------------------------------------------------------ the text helpers
def compose(body, tips, ask):
    """stem = situation + the tips (term: what it is) + the question. The tips are printed with the stem on the paper."""
    t = ('Tips: ' + '; '.join('%s: %s' % (a, b) for a, b in tips) + '.') if tips else ''
    return ' '.join(x for x in (body, t, ask) if x)


def place(correct, wrongs, pos):
    o = list(wrongs); o.insert(pos, correct); return o


# ------------------------------------------------------------------ the audit of the 23 items of v1.1.0 (full reading; see the report for the reasons)
# mem: the item asks to recall a fact or a name that the stem does not give; abbr: abbreviations met unexpanded; tip: terms used without a printed tip
AUDIT = {
 'mt1:i01:gox-two-events': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='asks what two events teach (reason); terms keys, wallet file, bankruptcy and the exchange had no tip'),
 'mt1:i02:toy-chain-supply': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='calculation; block subsidy and right shift had no tip'),
 'mt1:i03:vwap-third-trade': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='calculation; volume-weighted had no tip'),
 'mt1:i04:fee-not-written': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='reason why a transaction can be valid; satoshi, batching, consolidation, change, node had no tip'),
 'mt1:i05:change-after-fee-rate': dict(mem='Y', abbr='N', tip='Y', verdict='REPLACE', why='needs the unstated conversion of 4 weight units to 1 virtual byte (a recalled number); weight unit, virtual byte, fee rate had no tip; its idea (a higher fee rate leaves less change) is not lost'),
 'mt1:i06:order-wallet-to-block': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='ordering by dependence of the steps; unspent outputs, nonce, relay, change had no tip'),
 'mt1:i07:shop-confirmations': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='reading a table and deciding; confirmation, hash power, attacker had no tip'),
 'mt1:i08:utxo-set-trace': dict(mem='N', abbr='Y', tip='Y', verdict='REPLACE', why='the code variable utxo and the idea of the set were never spelled out; the idea moves into the fill-in groups of chapters 2 and 6'),
 'mt1:i09:conf-precedence-and-refusal': dict(mem='Y', abbr='N', tip='Y', verdict='REWRITE', why='needed the recalled rules (which option wins, which two options clash) with no tip; the rules and the reasons are now printed as tips and the question asks what happens and why'),
 'mt1:i10:match-node-options': dict(mem='Y', abbr='N', tip='Y', verdict='REWRITE', why='asked to recall option names for a need; the responses now carry the option name and what it does, the student judges the need'),
 'mt1:i11:trace-release-tags': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='trace; release tag and release candidate had only a partial explanation'),
 'mt1:i12:rpcauth-and-p2pkh': dict(mem='N', abbr='Y', tip='Y', verdict='REWRITE', why='P2PKH not spelled out; rpcauth, salted hash, commitment had no tip'),
 'mt1:i13:vanity-factor': dict(mem='Y', abbr='N', tip='Y', verdict='REWRITE', why='needed the recalled number 58 (the alphabet size); it is now printed in the stem; vanity address had no tip'),
 'mt1:i14:wif-flag-and-balance': dict(mem='Y', abbr='Y', tip='Y', verdict='REWRITE', why='WIF not spelled out; needed the recalled flag byte; compressed key, version byte, checksum had no tip'),
 'mt1:i15:fill-hash-and-collision': dict(mem='Y', abbr='Y', tip='Y', verdict='REPLACE', why='fill-in of the word commitment and of the number 80 (pure recall); P2PKH, SegWit, SHA256 not spelled out; replaced by fill-in sentences about why, with a bank of described entries'),
 'mt1:i16:words-to-entropy': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='calculation with the rules given; recovery code, entropy, checksum had no tip'),
 'mt1:i17:match-story-lesson': dict(mem='N', abbr='Y', tip='Y', verdict='REWRITE', why='stories to lessons (reason); txid in a response; malleability, range check, reference implementation, coinbase, Bech32m had no tip'),
 'mt1:i18:trace-gap-limit': dict(mem='N', abbr='N', tip='N', verdict='KEEP', why='the stem itself explains that the scan stops after a run of unused keys; no abbreviation; trace of a rule that is given'),
 'mt1:i19:restore-passphrase-labels': dict(mem='N', abbr='Y', tip='Y', verdict='REWRITE', why='BIP329 not spelled out; passphrase, labels, gap limit, recovery code had no tip'),
 'mt1:i20:trace-compactsize': dict(mem='N', abbr='N', tip='N', verdict='KEEP', why='the rule of cs_encode is given inside the question (the owner allows this type); no abbreviation'),
 'mt1:i21:trace-sequence-field': dict(mem='N', abbr='N', tip='Y', verdict='REWRITE', why='the rules are given; sequence value, opt-in replacement, relative timelock, bit 31, hexadecimal notation had no tip'),
 'mt1:i22:overflow-range-check': dict(mem='N', abbr='Y', tip='Y', verdict='REPLACE', why='txid unexpanded in an option; signed 64-bit, range check had no tip; its lesson (a range check on every output) lives on in the matching item of chapter 5'),
 'mt1:i23:tracker-legacy-vs-segwit': dict(mem='N', abbr='Y', tip='Y', verdict='REPLACE', why='txid, wtxid, segwit not spelled out, witness without a tip; its lesson moves into the fill-in group of chapter 6'),
}

# ------------------------------------------------------------------ abbreviations used in the new texts: abbreviation -> (full form, where the full form comes from)
ABBR = {
 'WIF': ('Wallet Import Format', 'course corpus (chapter 4)'),
 'P2PKH': ('pay to public key hash', 'course corpus (chapters 3 and 4)'),
 'SegWit': ('segregated witness', 'course corpus (chapters 4 and 6)'),
 'SHA256': ('Secure Hash Algorithm 256-bit', 'standard expansion, not found in the corpus (the course writes SHA256 and SHA-256)'),
 'BIP329': ('Bitcoin Improvement Proposal 329', 'course corpus (expansion of BIP); the standard is the label export format'),
 'txid': ('transaction identifier', 'course corpus (chapters 2 and 6)'),
 'wtxid': ('witness transaction identifier', 'standard expansion; the corpus describes the wtxid as the identifier that covers the witness'),
 'UTXO': ('unspent transaction output', 'standard expansion; the corpus writes unspent output'),
 'rc': ('release candidate', 'course corpus (chapter 3)'),
}


def build(outdir=None):
    LOG.clear()
    doc = json.load(open(SRC, encoding='utf8'))
    old = {i['key']: i for i in doc['items']}
    items = []

    def meta(k, **kw):
        """copy the source, sources, seeds, critical points, enhancements and chapters of an old item; the keyword arguments override"""
        o = old[k]
        m = dict(chapters=list(o['chapters']), bloom=o['bloom'], kind=o['kind'], source=dict(o['source']), sources=[dict(s) for s in o.get('sources', [])],
                 critical_points=list(o['critical_points']), seeds=list(o['seeds']), no_seed_reason=o['no_seed_reason'], enhancements=list(o['enhancements']), papers=['midterm'], from_item=[k])
        m.update(kw); return m

    def add(key, type_, **kw):
        d = dict(key=key, type=type_); d.update(kw); d.setdefault('computed', ''); d.setdefault('tips', []); d.setdefault('abbreviations', {}); items.append(d); return d

    # ============================================================ CHAPTER 1
    # U1  Mt. Gox: two stories, what each shows
    tips = [('Mt. Gox', 'a Tokyo bitcoin exchange'), ('keys', 'secret numbers that let their holder spend coins'),
            ('wallet file', 'stores a wallet\'s keys'), ('bankruptcy', 'a court closes a company that cannot pay')]
    body = ('Two stories about the exchange Mt. Gox in 2014. On 28 February it filed for bankruptcy after admitting that about 850,000 bitcoin were gone. '
            'Three weeks later it said it had found about 200,000 bitcoin in an old-format wallet file it believed was empty.')
    opts = place('Filing: whoever holds the keys holds the coins, and customers held none. Old file: an untested file is not an empty one.',
                 ['Filing: an untested file is not an empty one. Old file: whoever holds the keys holds the coins.',
                  'Filing: the network let the exchange spend the same coins twice. Old file: miners held the coins back for a fee.',
                  'Filing: customers lost their own keys. Old file: backups expire, so an old file can be thrown away.'], 0)
    add('mt2:i01:gox-two-events', 'ChoiceFour', **meta('mt1:i01:gox-two-events'), q=compose(body, tips, 'Which statement says correctly what each story teaches?'), options=opts, answer=0,
        tips=[list(t) for t in tips], terms=['mt. gox', 'old-format wallet', 'whoever holds the keys holds the coins', 'bankruptcy'],
        asks='reason: why it matters who holds the keys, and why a stored file must be tested')

    # U2  the fee is not written (chapters 1 and 2)
    ins, outs = [400000, 250000], [300000, 200000, 100000, 29000]; fee = sum(ins) - sum(outs)
    assert fee == 21000; log('U2 fee: inputs', ins, 'outputs', outs, 'fee', fee)
    tips = [('satoshi', 'one hundred-millionth of a bitcoin'), ('batching', 'one transaction paying several people'), ('node', 'a computer that checks the rules'),
            ('consolidation', 'many small coins gathered into one'), ('change', 'the part of the inputs that returns to the sender')]
    body = ('A wallet shows a draft batching payment: inputs of 400,000 and 250,000 satoshis, outputs of 300,000, 200,000, 100,000 and 29,000 satoshis. '
            'A colleague says that every node will refuse it because inputs and outputs are not equal.')
    opts = place('No: the 21,000 satoshis left over are the miner\'s fee, the difference between inputs and outputs; no field records it.',
                 ['Yes: the ledger must balance exactly, so one output must be lowered by 21,000.',
                  'No: the 21,000 satoshis return to the wallet as change, so no fee is paid.',
                  'Yes: four outputs make it a consolidation, which must spend exactly its inputs.'], 1)
    add('mt2:i02:fee-not-written', 'ChoiceFour', **meta('mt1:i04:fee-not-written'), q=compose(body, tips, 'Which reply is correct, and why?'), options=opts, answer=1,
        tips=[list(t) for t in tips], terms=['fee', 'batching', 'consolidation', 'change'], computed='fee %d = inputs %d minus outputs %d (program in the builder)' % (fee, sum(ins), sum(outs)),
        asks='reason: why the fee needs no field and why the transaction is valid')

    # U3  toy chain: the cap is arithmetic (chapters 1 and 6)
    sub, every, parts = 40, 50, []
    while sub > 0: parts.append(sub * every); sub >>= 1
    toy_total = sum(parts); assert toy_total == 3900
    log('U3 toy chain: subsidy 40 halved by a right shift every 50 blocks:', parts, 'total', toy_total)
    tips = [('block subsidy', 'the new coins that each block creates for its miner'),
            ('right shift', 'moving every binary digit one place to the right, which halves a whole number and drops the fraction (for example 5 becomes 2)')]
    body = ('A toy chain pays a block subsidy of 40 coins. Every 50 blocks the subsidy is halved by a right shift, so any fraction is dropped, and once it reaches zero no more coins are created. '
            'The same arithmetic limits the real supply to about 21 million.')
    add('mt2:i03:toy-chain-supply', 'NumericAnswer', **meta('mt1:i02:toy-chain-supply'), q=compose(body, tips, 'How many coins does the subsidy create in total over the whole life of the chain?'),
        key_value=toy_total, unit='coins', tolerance=0, tips=[list(t) for t in tips], terms=['halves', 'subsidy', 'right shift', '21 million'],
        computed='toy chain subsidy sum (program in the builder)', asks='importance: why a halving schedule makes the supply limit a matter of arithmetic')

    # U4  volume-weighted price (chapter 1)
    known = [(1, 62000), (2, 63000)]; day = 63250; vol = 4
    third = (day * vol - sum(b * p for b, p in known)) / (vol - sum(b for b, p in known)); assert third == 65000
    log('U4 volume-weighted price: day figure', day, 'volume', vol, 'third trade price', third)
    tips = [('volume-weighted figure', 'an average in which each trade counts in proportion to the amount traded, so a large trade moves it more than a small one')]
    body = ('Trades discover the price of bitcoin. On one day a price service sees three trades of bitcoin: '
            '1 bitcoin at 62,000 dollars, 2 bitcoin at 63,000 dollars, and 1 bitcoin at a price that is not shown. The service publishes a volume-weighted figure for the day of 63,250 dollars per bitcoin.')
    add('mt2:i04:vwap-third-trade', 'NumericAnswer', **meta('mt1:i03:vwap-third-trade'), q=compose(body, tips, 'At what price, in dollars per bitcoin, did the third trade happen?'),
        key_value=int(third), unit='dollars per bitcoin', tolerance=0, tips=[list(t) for t in tips], terms=['volume-weighted', 'price is discovered by trades'],
        computed='third trade price (program in the builder)', asks='use: how a published day figure is built from trades')

    # ============================================================ CHAPTER 2
    # U5  shop confirmations
    t10 = {z: round(100 * catch_up(0.1, z), 1) for z in (1, 2, 3)}; t10[6] = round(100 * catch_up(0.1, 6), 2)
    t30 = {z: round(100 * catch_up(0.3, z), 1) for z in (1, 3, 6, 9, 10)}
    assert t10 == {1: 20.5, 2: 5.1, 3: 1.3, 6: 0.02} and t30 == {1: 62.8, 3: 32.5, 6: 13.2, 9: 5.5, 10: 4.2}
    z10 = min(z for z in range(1, 30) if 100 * catch_up(0.1, z) < 5); z30 = min(z for z in range(1, 40) if 100 * catch_up(0.3, z) < 5); assert (z10, z30) == (3, 10)
    log('U5 catch-up table checked against the stem: attacker 10 percent', t10, 'attacker 30 percent', t30, '; smallest z below 5 percent:', z10, z30)
    tips = [('confirmation', 'each further block built on the block that holds a payment'), ('hash power', 'computing power used to add blocks'), ('attacker', 'someone who rebuilds the latest blocks to take a payment back')]
    body = ('Chance, in percent, that an attacker with a share of the hash power ever catches up when a payment has z confirmations: for 10 percent, z = 1 gives 20.5, z = 2 gives 5.1, z = 3 gives 1.3 and z = 6 gives 0.02; '
            'for 30 percent, z = 1 gives 62.8, z = 3 gives 32.5, z = 6 gives 13.2, z = 9 gives 5.5 and z = 10 gives 4.2. A shop accepts a payment only when the chance of a reversal is below 5 percent.')
    opts = place('A shop needs three confirmations against the 10 percent attacker but ten against the 30 percent one.',
                 ['Six confirmations are equally safe against either attacker, because each divides the chance equally.',
                  'Two confirmations are enough against the 10 percent attacker, because z = 2 is below 5 percent.',
                  'Three confirmations are enough against the 30 percent attacker, because the chance is below 5 percent at z = 3.'], 2)
    add('mt2:i05:shop-confirmations', 'ChoiceFour', **meta('mt1:i07:shop-confirmations'), q=compose(body, tips, 'Which statement follows from these figures?'), options=opts, answer=2,
        tips=[list(t) for t in tips], terms=['confirmations', 'attacker', 'hash power', '20.5'], computed='catch-up table (formula of section 11 of the white paper, in the builder)',
        asks='reason: why a shop waits for confirmations, and how many it needs for a stronger attacker')

    # U6  ordering: from a wallet to a block
    steps = ['The wallet takes whole coins from its unspent outputs (coins no later payment has used) until they cover the payment and the fee.',
             'The wallet writes the payee output and the change output (the part that returns to the sender) and leaves the fee as the difference.',
             'The wallet signs every input (proves that it may spend the coin the input names).',
             'A node (a computer that checks the rules) checks the transaction and relays it, that is, passes it on to its peers.',
             'A miner finds a valid nonce (the number varied in the search for a block) and adds a block that holds the transaction.']
    add('mt2:i06:order-wallet-to-block', 'Ordering', **meta('mt1:i06:order-wallet-to-block', critical_points=['CP2.03', 'CP2.04', 'CP2.09']), steps=steps, tips=[['unspent outputs', 'coins that no later payment has used yet'], ['change', 'the part that returns to the sender'],
        ['node', 'a computer that checks the rules'], ['relay', 'pass a transaction on to peers'], ['nonce', 'the number that is varied in the search for a block']],
        terms=['unspent outputs', 'nonce', 'relays', 'change', 'fee'], asks='reason: why each step of a payment needs the result of the step before it',
        instruction='Put the five steps of one payment in the order in which they happen: write 1 for the first and 5 for the last. Each step needs the result of the step before it.')

    # U7/U8  fill-in group of chapter 2 (blanks: less, unspent)
    bank = [('less', 'a smaller amount'), ('unspent', 'not yet used as an input by a later transaction')]
    dis = [('more', 'a larger amount'), ('spent', 'already used as an input by a later transaction')]
    add('mt2:i07:fill-fee-rate-and-set', 'FillBlankGroup', from_item=['mt1:i05:change-after-fee-rate', 'mt1:i08:utxo-set-trace'], chapters=[2, 6], bloom=2, kind='synthesis', source={'file': old['mt1:i05:change-after-fee-rate']['source']['file'], 'locator': "slide 22 'A higher fee rate leaves less change' (22 of 35) and slide 16 'Which outputs are still unspent' notes (wallets and nodes keep exactly this set)"},
        sources=[{'file': old['mt1:i20:trace-compactsize']['source']['file'], 'locator': "slide 25 'A spend updates the UTXO set' (25 of 71): remove what is spent, add what is created"}],
        critical_points=['CP2.10', 'CP2.11', 'CP6.09'], seeds=list(old['mt1:i05:change-after-fee-rate']['seeds'][:1]), no_seed_reason='', enhancements=['change the situation'], papers=['midterm'],
        blanks=[{'text': 'The fee is taken from what would otherwise return to the wallet as change. With the same coin and the same payment, a higher fee rate therefore leaves ____ change.', 'answer': 'less (%s)' % bank[0][1]},
                {'text': 'A spend removes the outputs it uses from the set of ____ outputs and adds the outputs it creates. Wallets and nodes keep exactly that set, because only its members can be spent.', 'answer': 'unspent (%s)' % bank[1][1]}],
        distractors=['%s (%s)' % d for d in dis], tips=[list(x) for x in bank + dis] + [['fee rate', 'the fee that is paid for each virtual byte of the transaction'], ['change', 'the part of the inputs that returns to the sender']],
        terms=['fee rate', 'change', 'unspent'],
        asks='reason: why a higher fee rate leaves less change, and why wallets and nodes keep the set of unspent outputs',
        instruction='Choose for each blank the entry of the bank that makes the sentence true; write its bank code. Each bank entry says what it means.')

    # ============================================================ CHAPTER 3
    # U9  configuration and command line (what happens and why)
    res = node_start({'prune': 550, 'txindex': 1, 'dbcache': 450}, {'txindex': 0, 'dbcache': 2048}); assert res == 'starts: prune=550 txindex=0 dbcache=2048'
    res_file_only = node_start({'prune': 550, 'txindex': 1, 'dbcache': 450}, {}); assert res_file_only == 'refuses'
    log('U9 node start with the file and the command line:', res, '; with the file alone:', res_file_only)
    tips = [('prune', 'deletes old block files to save disk'), ('txindex', 'indexes all transactions; it needs all blocks, which pruning deletes'),
            ('dbcache and bitcoind', 'the memory cache size and the node program'), ('command line', 'options typed at the start; they replace the same options of the file for that run')]
    opts = place('It starts with pruning 550, no index and cache 2048: the command line replaces the file, and no index removes the clash.',
                 ['It refuses to start: the file asks for pruning and the index together, which clash.',
                  'It starts with the index on and a cache of 450, because the file replaces the command line.',
                  'It starts with pruning and the index on, because the refusal covers only the command line.'], 3)
    add('mt2:i09:conf-precedence-and-refusal', 'ChoiceFourCode', **meta('mt1:i09:conf-precedence-and-refusal'),
        q=compose('A node reads the configuration file and is started with the command line shown.', tips, 'What happens, and why?'),
        code='# bitcoin.conf\nprune=550\ntxindex=1\ndbcache=450\n# the command line\nbitcoind -txindex=0 -dbcache=2048', options=opts, answer=3,
        tips=[list(t) for t in tips], terms=['prune', 'txindex', 'dbcache', 'bitcoind', 'command line'], computed=res,
        asks='reason: why the node starts, using what each option does')

    # U10  matching: a need to the option that serves it
    resp = ['prune: deletes old blocks to save disk space',
            'txindex: indexes all transactions (needs all blocks)',
            'alertnotify: sends emergency alerts, usually by email',
            'maxconnections: limits connecting nodes, to save bandwidth',
            'datadir: chooses where all blockchain data is stored',
            'maxmempool: limits memory for waiting transactions']
    prem = [('A volunteer runs a validating node (a node that checks all blocks and transactions) on a laptop with little disk space and does not need old blocks.', resp[0]),
            ('A block-explorer service (a website for looking up blocks and transactions) must find any transaction by its identifier.', resp[1]),
            ('The operator wants a message, usually by email, when the node meets an emergency.', resp[2]),
            ('A node on a thin connection must limit how many other nodes it accepts.', resp[3])]
    add('mt2:i10:match-node-options', 'Matching', **meta('mt1:i10:match-node-options'), premises=[{'text': a, 'match': b} for a, b in prem], responses=resp,
        tips=[['validating node', 'a node that checks all blocks and transactions'], ['block explorer', 'a website for looking up blocks and transactions']],
        terms=['prune', 'txindex', 'alertnotify', 'maxconnections', 'datadir', 'maxmempool'], asks='use: which node setting serves which need',
        instruction='Match each need (left) with the setting (right) that serves it. Each response says what the setting does. Two responses are not used.')

    # U11  release tags (trace)
    tag_code = ("tags = ['v28.0', 'v3.1', 'v28.0rc1',\n        'v4.0', 'v24.2', 'v9.1']\nfinal = [t for t in tags if 'rc' not in t]\ndef key(t):\n    return [int(p) for p in t[1:].split('.')]\n"
                "a = sorted(final)\nb = sorted(final, key=key)\nmove = 0\nfor t in final:\n    move += abs(a.index(t) - b.index(t))\nprint(move)")
    assert tag_code == old['mt1:i11:trace-release-tags']['code']
    tag_out = run(tag_code); assert tag_out == '12'; log('U11 tags listing prints', tag_out)
    tips = [('release tag', 'the name of one version of a program, such as v3.1'), ('release candidate', 'a test version before the final one; its tag carries rc'),
            ('sorted as text', 'letter by letter, so "v28.0" comes before "v3.1"')]
    body = ('A script drops the release candidates from a list of release tags and compares the final releases sorted as text with the same releases sorted by version number. It adds up how far each tag moves between the two orders.')
    add('mt2:i11:trace-release-tags', 'CodeTrace', **meta('mt1:i11:trace-release-tags'), q=compose(body, tips, 'What does it print?'), code=tag_code, output=tag_out,
        tips=[list(t) for t in tips], terms=['release tags', 'release candidates', 'rc'], computed=tag_out, asks='reason: why version tags must be sorted by number, not by text')

    # U12  rpcauth and P2PKH
    tips = [('rpcauth', 'the node setting (remote procedure call authentication) that checks passwords of programs calling the node'),
            ('hash', 'a one-way fingerprint'), ('salted', 'mixed with random data, so equal passwords give different hashes'), ('commitment', 'fixes a secret now; its owner reveals it later')]
    body = 'A node\'s configuration file holds an rpcauth line, and a pay to public key hash (P2PKH) output script (the lock of the older address format) holds a 20-byte hash of a public key. Both keep a hash, not the secret.'
    opts = place('A leak reveals no password, because rpcauth is salted; the P2PKH hash is a commitment, and the key appears only when coins are spent.',
                 ['A leak reveals the password, because rpcauth is only an encoding; the P2PKH hash comes with the key.',
                  'The rpcauth hash is a commitment revealed when coins are spent; the P2PKH hash is salted, so a leak reveals no key.',
                  'Both hashes are salted checksums that catch typos, and both secrets appear when a node reads them.'], 0)
    add('mt2:i12:rpcauth-and-p2pkh', 'ChoiceFour', **meta('mt1:i12:rpcauth-and-p2pkh'), q=compose(body, tips, 'Which statement compares them correctly, and why do both keep a hash?'), options=opts, answer=0,
        tips=[list(t) for t in tips], terms=['rpcauth', 'salted hash', 'p2pkh', 'commitment', '20-byte hash'], asks='reason: why a hash is kept instead of the secret',
        abbreviations={'P2PKH': ABBR['P2PKH'][0]})

    # ============================================================ CHAPTER 4
    # U13  vanity factor
    fac = 58 ** (3 - 1); assert fac == 3364; log('U13 vanity: 58 symbols; from 1 to 3 chosen letters the average work is multiplied by 58^2 =', fac)
    tips = [('vanity address', 'an address chosen to start with letters its owner likes'),
            ('58 symbols', 'an address is written with 58 symbols, so each further chosen letter makes a match 58 times less likely')]
    body = ('A search for a vanity address needs, on average, a number of tries for one chosen letter after the leading 1. Nobody can shorten the search.')
    add('mt2:i13:vanity-factor', 'NumericAnswer', **meta('mt1:i13:vanity-factor'), q=compose(body, tips, 'By what factor is the average number of tries larger when the search asks for three chosen letters instead of one?'),
        key_value=fac, unit='times', tolerance=0, tips=[list(t) for t in tips], terms=['vanity', '58 times'], computed='58 raised to 2 (program in the builder)',
        asks='importance: why a longer vanity name costs so much more work')

    # U14  Wallet Import Format, flag and balance
    tips = [('compressed public key', 'the shorter form of a public key; a private key has two public key forms and so two addresses, and coins sent to one are not seen at the other')]
    body = ('Dana\'s coins were sent to the address of the compressed public key of her private key. Her paper backup holds that key in Wallet Import Format (WIF), the text form for importing a private key; '
            'a WIF for a compressed key ends with an extra byte 01, but hers does not. A new wallet imports it and shows zero balance.')
    opts = place('The wallet took the key as uncompressed and watches its other address; comparing the first address after a test restore would have caught it.',
                 ['The missing byte changed the private key; only a second copy of the paper would have caught it.',
                  'The coins went to an address with no key behind it; checking the address again would have caught it.',
                  'The wallet looks on another network; a tiny first payment and a day\'s wait would have caught it.'], 1)
    add('mt2:i14:wif-flag-and-balance', 'ChoiceFour', **meta('mt1:i14:wif-flag-and-balance'), q=compose(body, tips, 'Which diagnosis fits, and which check before funding would have caught it?'), options=opts, answer=1,
        tips=[list(t) for t in tips], terms=['wif', 'compressed', 'final 01'], asks='reason: why the balance is zero and why a paper wallet must give back its address first',
        abbreviations={'WIF': ABBR['WIF'][0]})

    # U15/U16  fill-in group of chapter 4 (commitment, 256-bit hash)
    b1 = ('commitment', 'a value that fixes a secret now and lets its owner reveal it later')
    b2 = ('256-bit hash', 'the hash function Secure Hash Algorithm 256-bit (SHA256), whose result is 256 bits long')
    d1 = ('checksum', 'a few extra bytes that catch typing mistakes'); d2 = ('salt', 'random data mixed in before hashing')
    add('mt2:i15:fill-hash-commitment', 'FillBlankGroup', from_item=['mt1:i15:fill-hash-and-collision'], chapters=[4], bloom=2, kind='direct', source=dict(old['mt1:i15:fill-hash-and-collision']['source']), sources=[],
        critical_points=['CP4.05', 'CP4.07'], seeds=list(old['mt1:i15:fill-hash-and-collision']['seeds']), no_seed_reason='', enhancements=['change the situation', 'reverse the question'], papers=['midterm'],
        blanks=[{'text': 'A pay to public key hash (P2PKH) output holds only a 20-byte hash of the public key; the key stays hidden until the coins are spent. The hash is a ____ to the key.', 'answer': '%s (%s)' % b1},
                {'text': 'A 160-bit hash gives only about 80 bits of protection against collisions (two different inputs with the same result). That is why the newer segregated witness (SegWit) scripts use the ____ instead.', 'answer': '%s (%s)' % b2}],
        distractors=['%s (%s)' % d1, '%s (%s)' % d2], tips=[list(x) for x in (b1, b2, d1, d2)], terms=['commitment', '160-bit hash', 'segwit', 'sha256'],
        asks='reason: why the older address hides the key and why newer scripts use a longer hash',
        abbreviations={'P2PKH': ABBR['P2PKH'][0], 'SegWit': ABBR['SegWit'][0], 'SHA256': ABBR['SHA256'][0]},
        instruction='Choose for each blank the entry of the bank that makes the sentence true; write its bank code. Each bank entry says what it means.')

    # ============================================================ CHAPTER 5
    # U17  words to entropy
    words, bits_per_word = 18, 11
    fit = [e for e in (128, 160, 192, 224, 256) if e + e // 32 == words * bits_per_word]; assert fit == [192]
    log('U17 a code of', words, 'words holds', words * bits_per_word, 'bits; entropy sizes that fit with one checksum bit per 32 bits:', fit)
    tips = [('recovery code', 'words that write down the secret a wallet is built from'), ('entropy', 'the amount of randomness in the secret, in bits'),
            ('checksum', 'extra bits that catch a mistyped word')]
    body = 'A recovery code has 18 words. Each word carries 11 bits, and the checksum is one bit for every 32 bits of entropy.'
    add('mt2:i17:words-to-entropy', 'NumericAnswer', **meta('mt1:i16:words-to-entropy'), q=compose(body, tips, 'How many bits of entropy does the code hold?'),
        key_value=fit[0], unit='bits', tolerance=0, tips=[list(t) for t in tips], terms=['11 bits', 'checksum', 'entropy'], computed='entropy sizes that fit 18 words (program in the builder)',
        asks='use: how the length of a recovery code follows from the secret it writes down')

    # U18  matching: a story to its lesson
    r = ['Memory is not a backup: test a recovery code by restoring it.',
         'A signed amount needs a range check (zero up to the maximum) on each output, not only on the total.',
         'A reference implementation (the program that defines the rules) needs a team and public review.',
         'A stated cause is tested against data: malleability changes the transaction identifier (txid).',
         'A transaction has no fee field: the fee is inputs minus outputs.',
         'A double spend is refused by a shared rule, and no bank decides.']
    p = [('A programmer, paid 7,002 bitcoin in 2011, lost the password of the drive with his keys; two guesses are left.', r[0]),
         ('In block 74,638 (15 August 2010) two huge outputs summed to a negative number; 184 billion bitcoin appeared.', r[1]),
         ('On 7 April 2014 the reference software got a new lead maintainer.', r[2]),
         ('On 10 February 2014 an exchange blamed transaction malleability (changing a transaction\'s identifier, not the payment) for missing bitcoin; researchers checked a year of traffic.', r[3])]
    add('mt2:i18:match-story-lesson', 'Matching', **meta('mt1:i17:match-story-lesson'), premises=[{'text': a, 'match': b} for a, b in p], responses=r,
        tips=[['transaction identifier (txid)', 'the hash that names a transaction']],
        terms=['7,002 bitcoin', '184 billion', 'malleability', 'reference implementation', 'range check'], asks='reason: what each story teaches',
        abbreviations={'txid': ABBR['txid'][0]},
        instruction='Match each story (left) with the lesson (right) that it teaches. Two lessons are not used.')

    # U19  gap limit (trace)  KEEP
    gap_code = old['mt1:i18:trace-gap-limit']['code']; gap_out = run(gap_code); assert gap_out == '15'; log('U19 gap listing prints', gap_out)
    add('mt2:i19:trace-gap-limit', 'CodeTrace', **meta('mt1:i18:trace-gap-limit'), q=old['mt1:i18:trace-gap-limit']['q'], code=gap_code, output=gap_out, tips=[],
        terms=list(old['mt1:i18:trace-gap-limit']['terms']), computed=gap_out, asks='use: how far a recovery scan looks')

    # U20  restore with a passphrase and labels
    tips = [('recovery code', 'words that write down the secret a wallet is built from'), ('passphrase', 'an extra secret; the same words with another passphrase open another wallet'),
            ('labels', 'notes on addresses and payments'), ('gap limit', 'unused keys in a row after which a recovery scan stops')]
    body = ('Lena\'s phone is stolen. From her twelve-word recovery code a new phone shows different addresses, an empty balance and no labels. '
            'She had set a passphrase and had exported her labels in the Bitcoin Improvement Proposal 329 (BIP329) format, a standard label file.')
    opts = place('A passphrase forks the wallet and labels cannot be derived from the seed; she must enter the passphrase and import the labels file.',
                 ['The recovery code was on the stolen phone, so the thief has spent the coins.',
                  'The gap limit stopped the scan too early; a larger one would bring back the balance and the labels.',
                  'Labels come from the seed and were lost with the phone; the passphrase only changes the spelling.'], 2)
    add('mt2:i20:restore-passphrase-labels', 'ChoiceFour', **meta('mt1:i19:restore-passphrase-labels'), q=compose(body, tips, 'What is the most complete explanation and the fix?'), options=opts, answer=2,
        tips=[list(t) for t in tips], terms=['passphrase', 'bip329', 'labels', 'gap limit', 'recovery code'], asks='reason: why a backup needs the passphrase and the labels as well as the words',
        abbreviations={'BIP329': ABBR['BIP329'][0]})

    # ============================================================ CHAPTER 6
    # U21  CompactSize (trace)  KEEP (the rule is inside the question)
    cs = old['mt1:i20:trace-compactsize']; got = run(cs['code'], {'cs_encode': cs_real}); assert got == '14'
    log('U21 CompactSize listing prints', got, 'with the real encoder; sizes', [len(cs_real(n)) for n in (252, 253, 65536, 4294967295)])
    add('mt2:i21:trace-compactsize', 'CodeTrace', **meta('mt1:i20:trace-compactsize'), q=cs['q'], code=cs['code'], output=got, tips=[], terms=list(cs['terms']), computed=got,
        asks='use: how a count is written in few bytes')

    # U22  sequence field (trace)
    seq_code = old['mt1:i21:trace-sequence-field']['code']; seq_out = run(seq_code); assert seq_out == '35'; log('U22 sequence listing prints', seq_out)
    tips = [('opt-in replacement', 'the unconfirmed payment may be replaced by one with a higher fee'),
            ('relative timelock', 'the spent output must first wait a set time'), ('bit 31', 'the highest of the 32 bits; clear means 0'), ('0x', 'starts a hexadecimal number')]
    body = 'The program reads five sequence values (a 32-bit number in each input). A value signals opt-in replacement when it is below 0xfffffffe and carries a relative timelock when bit 31 is clear. It adds up the low 16 bits of the values that do both.'
    add('mt2:i22:trace-sequence-field', 'CodeTrace', **meta('mt1:i21:trace-sequence-field'), q=compose(body, tips, 'What does it print?'), code=seq_code, output=seq_out,
        tips=[list(t) for t in tips], terms=['sequence', '0xfffffffe', 'bit 31', 'relative timelock'], computed=seq_out, asks='use: which inputs allow a replacement and carry a timelock')

    # U23/U24  fill-in group of chapter 6 (txid, less)
    c1 = ('txid', 'the transaction identifier, a hash that ignores the witness'); c2 = ('less', 'a smaller amount')
    e1 = ('wtxid', 'the witness transaction identifier, a hash that also covers the witness'); e2 = ('more', 'a larger amount')
    add('mt2:i23:fill-txid-and-weight', 'FillBlankGroup', from_item=['mt1:i23:tracker-legacy-vs-segwit', 'mt1:i05:change-after-fee-rate'], chapters=[6, 3], bloom=2, kind='synthesis',
        source={'file': old['mt1:i23:tracker-legacy-vs-segwit']['source']['file'], 'locator': "slide 49 'Segwit: change the witness, keep the txid' (49 of 71) and slide 63 'From 194 bytes to 569 weight' (63 of 71)"},
        sources=[], critical_points=['CP6.14', 'CP6.04', 'CP3.09', 'CP6.19'], seeds=list(old['mt1:i23:tracker-legacy-vs-segwit']['seeds'][:2]), no_seed_reason='', enhancements=['change the situation', 'combine chapters'], papers=['midterm'],
        blanks=[{'text': 'Segregated witness (SegWit) keeps the signatures outside the data that gives the transaction identifier, so a changed signature changes the witness transaction identifier (wtxid) but not the ____.', 'answer': '%s (%s)' % c1},
                {'text': 'A block is filled by weight: each byte counts four units, but the witness (the signatures) and the marker and flag (two bytes that announce a witness) count one. A payment with many witness bytes therefore uses ____ block space than one with the same number of other bytes.', 'answer': '%s (%s)' % c2}],
        distractors=['%s (%s)' % e1, '%s (%s)' % e2], tips=[list(x) for x in (c1, c2, e1, e2)] + [['witness', 'the signatures'], ['marker and flag', 'two bytes that announce a witness']],
        terms=['txid', 'wtxid', 'segwit', 'witness', 'marker'],
        asks='importance: why a payment tracker can rely on the transaction identifier after segregated witness, and why witness bytes make a payment cheaper in a block',
        abbreviations={'SegWit': ABBR['SegWit'][0], 'wtxid': ABBR['wtxid'][0]},
        instruction='Choose for each blank the entry of the bank that makes the sentence true; write its bank code. Each bank entry says what it means.')
    for it in items:
        if not it['seeds'] and not it['no_seed_reason'].startswith('none:'): it['no_seed_reason'] = 'none: written from the source of the point (the page banks and quizzes hold no matching question)'
        if it['seeds']: it['no_seed_reason'] = ''
        it['understanding'] = it.pop('asks')
    ndoc = dict(note=doc['note'].replace('version 1.1.0', 'version 1.2.0').split(' (derived from')[0] + ' version 1.2.0 (derived from v1.1.0 by sen0401_exam_items_midterm_build_v1_2_0.py under the owner\'s rules of 2026-11-01 13:04: '
                'no memorisation, a tip with every term, abbreviations spelled out, five question formats).', version=VERSION, chapters=doc['chapters'], items=items)
    return ndoc, doc


# ------------------------------------------------------------------ structure
BLOCK = {'ChoiceFour': 'ChoiceFour', 'ChoiceFourCode': 'ChoiceFour', 'NumericAnswer': 'NumericAnswer', 'CodeTrace': 'NumericAnswer', 'Ordering': 'Ordering', 'Matching': 'Matching', 'FillBlankGroup': 'FillBlankGroup'}
SEED = 5701
BONUS = [
 dict(key='mt2:b1:no-bank', chapters=[1], critical_points=['CP1.03', 'CP1.07'], points=5,
      prompt='In two or three sentences, explain who refuses a double spend (the same coin offered to two people) in Bitcoin when no bank stands in the middle, and why that makes the history costly to change.',
      tips=[['double spend', 'the same coin offered to two different people'], ['node', 'a computer that checks every rule'], ['proof of work', 'the costly search that every new block must contain']],
      rubric=['Every node checks every rule, so the shared rule refuses the second spend of a coin; no referee decides.', 'Proof of work makes each block costly to produce, so rewriting history costs real work.', 'The answer connects the two: a rule everybody checks, and a history that is costly to change.'],
      terms=['double spend', 'proof of work', 'every node checks every rule'], sources=[{'file': '03-materials/ch01/SEN0401_Ch01_Introduction_3e_v3_2_0.pptx', 'locator': "slide 60 (the six lines) and slide 33 notes (the same coin offered twice; no bank decides)"}]),
 dict(key='mt2:b2:mining-check', chapters=[2], critical_points=['CP2.12'], points=5,
      prompt='In two or three sentences, explain why mining is called a search that nobody can shortcut, and why it is still easy for every other node to check a block.',
      tips=[['mining', 'the search for a number that makes the hash of a block header small enough'], ['hash', 'a one-way fingerprint: easy to compute, practically impossible to reverse'], ['node', 'a computer that checks every rule']],
      rubric=['The search can only be done by trying numbers; there is no shortcut.', 'Anyone can check the found number with one hash.', 'The answer states why this matters: the work is costly to produce but cheap to verify.'],
      terms=['mining', 'hash', 'nobody can shortcut'], sources=[{'file': '03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx', 'locator': "slide 25 'One more zero, many more tries' notes (nobody can shortcut the search; anyone can check with one hash)"}]),
]


def structure(ndoc):
    items = ndoc['items']; by = {i['key']: i for i in items}
    rnd = random.Random(SEED)

    def pick(types): return [i for i in items if i['type'] in types]
    Q = []

    def order_mixed(lst):
        l = list(lst); rnd.shuffle(l); return l

    def points_for(lst, pts):
        """points go to the harder sub-questions first (higher Bloom, then more chapters, then key); the list pts is the share of the 25"""
        ranked = sorted(lst, key=lambda i: (-i['bloom'], -len(i['chapters']), i['key']))
        return {i['key']: p for i, p in zip(ranked, pts)}
    # Q1 reading and choice: 7 items
    c = pick(('ChoiceFour', 'ChoiceFourCode')); pt = points_for(c, [4, 4, 4, 4, 3, 3, 3]); assert len(c) == 7 and sum(pt.values()) == 25
    Q.append(dict(number=1, title='Reading and choice', format='reading/choice', points=25, machine_read=True, hand_marked=False, answer_block='ChoiceFour',
                  instruction='Read the situation and its tips. Mark the one statement that is correct (letters A to D) on the answer sheet.',
                  sub=[dict(key='Q1.%s' % 'abcdefg'[n], item=i['key'], type=i['type'], block=BLOCK[i['type']], points=pt[i['key']], units=1, chapters=i['chapters'], bloom=i['bloom']) for n, i in enumerate(order_mixed(c))]))
    # Q2 calculation and tracing: 8 items
    c = pick(('NumericAnswer', 'CodeTrace')); pt = points_for(c, [4, 3, 3, 3, 3, 3, 3, 3]); assert len(c) == 8 and sum(pt.values()) == 25
    Q.append(dict(number=2, title='Calculation and tracing', format='calculation', points=25, machine_read=True, hand_marked=False, answer_block='NumericAnswer',
                  instruction='Work out each number (by calculation, or by following the program) and write it, at most five characters, in the boxes of the answer sheet.',
                  sub=[dict(key='Q2.%s' % 'abcdefgh'[n], item=i['key'], type=i['type'], block=BLOCK[i['type']], points=pt[i['key']], units=1, chapters=i['chapters'], bloom=i['bloom']) for n, i in enumerate(order_mixed(c))]))
    # Q3 ordering and matching: 3 items, points shared among their parts
    o = pick(('Ordering', 'Matching')); assert len(o) == 3
    p3 = {'mt2:i06:order-wallet-to-block': 8, 'mt2:i10:match-node-options': 8, 'mt2:i18:match-story-lesson': 9}; assert sum(p3.values()) == 25 and set(p3) == {i['key'] for i in o}
    sub = []
    for n, i in enumerate(order_mixed(o)):
        parts = len(i['steps']) if i['type'] == 'Ordering' else len(i['premises'])
        sub.append(dict(key='Q3.%s' % 'abc'[n], item=i['key'], type=i['type'], block=BLOCK[i['type']], points=p3[i['key']], units=1, parts=parts, points_per_part=round(p3[i['key']] / parts, 4), chapters=i['chapters'], bloom=i['bloom'],
                        instruction=i['instruction']))
    Q.append(dict(number=3, title='Ordering and matching', format='ordering/matching', points=25, machine_read=True, hand_marked=False, answer_block='Ordering and Matching',
                  instruction='Follow the instruction under each part. Partial credit is a rule for the owner to fix (open question P1): the points of a part divide equally over its steps or pairs.', sub=sub))
    # Q4 fill-in: 3 groups of 2 blanks
    f = pick(('FillBlankGroup',)); assert len(f) == 3
    pts = [4, 4, 4, 4, 4, 5]; sub = []; k = 0
    f_sorted = sorted(f, key=lambda i: i['chapters'])
    blanks = [(i, b) for i in f_sorted for b in range(len(i['blanks']))]
    # the single 5-point blank is the first blank of the multi-chapter group (the hardest sentence)
    for n, (i, b) in enumerate(blanks):
        pass
    five = next(idx for idx, (i, b) in enumerate(blanks) if i['key'] == 'mt2:i23:fill-txid-and-weight' and b == 0)
    for n, (i, b) in enumerate(blanks):
        sub.append(dict(key='Q4.%s' % 'abcdef'[n], item=i['key'], type='FillBlankGroup', block='FillBlankGroup', blank=b + 1, points=5 if n == five else 4, units=1, chapters=i['chapters'], bloom=i['bloom']))
    assert sum(s['points'] for s in sub) == 25
    Q.append(dict(number=4, title='Fill in the sentence', format='fill-in', points=25, machine_read=True, hand_marked=False, answer_block='FillBlankGroup',
                  instruction='Each group has its own bank. Choose for each blank the entry that makes the sentence true; each entry says what it means. Write the bank code.', sub=sub))
    # Q5 bonus: short explanation, marked by hand
    bsub = []
    for n, b in enumerate(BONUS):
        bsub.append(dict(key='Q5.%s' % 'ab'[n], item=b['key'], type='ShortExplanation', block='NONE (marked by hand)', points=b['points'], units=0, chapters=b['chapters'], critical_points=b['critical_points'],
                         prompt=b['prompt'], tips=b['tips'], rubric=b['rubric'], rubric_points=len(b['rubric']), lines=3, terms=b['terms'], sources=b['sources'], machine_read=False, hand_marked=True))
    Q.append(dict(number=5, title='Short explanation (bonus)', format='short explanation', points=10, bonus=True, machine_read=False, hand_marked=True, answer_block='none: written on the paper and marked by hand',
                  instruction='BONUS, marked by hand, NOT read by the machine. Answer in two or three sentences in the lines under the question. Each tip says what a term means.', sub=bsub))
    return dict(version='1.0.0', items_file='sen0401_exam_items_midterm_v1_2_0.json', seed_for_sub_question_order=SEED, chapters=ndoc['chapters'], total_points_without_bonus=sum(q['points'] for q in Q if not q.get('bonus')),
                bonus_points=sum(q['points'] for q in Q if q.get('bonus')), questions_main=4, formats=[q['format'] for q in Q], questions=Q)


AUDIT_ORDER = list(AUDIT)


def audit_text(doc):
    old = {i['key']: i for i in doc['items']}
    L = ['AUDIT of the 23 items of sen0401_exam_items_midterm_v1_1_0.json (each item read in full by the author; judgements in the builder, data AUDIT)',
         'columns: key | chapter(s) | type | memorisation | unexpanded abbreviation | term without tip | verdict | reason',
         'memorisation Y = the item asks to recall a fact or a name that the stem does not give; abbreviation Y = an abbreviation met before it is spelled out; tip Y = a term used without a printed tip', '']
    for k in AUDIT_ORDER:
        a = AUDIT[k]; i = old[k]
        L.append('%-40s ch%-8s %-15s mem=%s abbr=%s tipless=%s %-8s %s' % (k, ','.join(map(str, i['chapters'])), i['type'], a['mem'], a['abbr'], a['tip'], a['verdict'], a['why']))
    L.append('')
    L.append('COUNTS BY CHAPTER (primary chapter = the first chapter of the item; items, not units)')
    L.append('%-8s %5s %5s %5s %5s %5s %5s %5s' % ('chapter', 'items', 'mem-Y', 'abbr-Y', 'tip-Y', 'KEEP', 'REWR', 'REPL'))
    tot = [0] * 7
    for ch in range(1, 7):
        ks = [k for k in AUDIT_ORDER if old[k]['chapters'][0] == ch]
        row = [len(ks), sum(AUDIT[k]['mem'] == 'Y' for k in ks), sum(AUDIT[k]['abbr'] == 'Y' for k in ks), sum(AUDIT[k]['tip'] == 'Y' for k in ks), sum(AUDIT[k]['verdict'] == 'KEEP' for k in ks),
               sum(AUDIT[k]['verdict'] == 'REWRITE' for k in ks), sum(AUDIT[k]['verdict'] == 'REPLACE' for k in ks)]
        tot = [a + b for a, b in zip(tot, row)]
        L.append('%-8s %5d %5d %5d %5d %5d %5d %5d' % ((ch,) + tuple(row)))
    L.append('%-8s %5d %5d %5d %5d %5d %5d %5d' % (('total',) + tuple(tot)))
    return '\n'.join(L) + '\n', tot


def main():
    outdir = os.path.abspath(sys.argv[sys.argv.index('--outdir') + 1]) if '--outdir' in sys.argv else HERE
    ndoc, doc = build()
    st = structure(ndoc)
    at, tot = audit_text(doc)
    paths = {k: os.path.join(outdir, v) for k, v in dict(items='sen0401_exam_items_midterm_v1_2_0.json', structure='sen0401_exam_structure_v1_0_0.json', audit='sen0401_exam_items_midterm_audit_v1_2_0.txt',
                                                         computed='sen0401_exam_items_midterm_computed_v1_2_0.txt').items()}
    for p in paths.values():
        if os.path.exists(p): sys.exit('refusing to overwrite ' + p)
    json.dump(ndoc, open(paths['items'], 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    json.dump(st, open(paths['structure'], 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    open(paths['audit'], 'w', encoding='utf8').write(at)
    open(paths['computed'], 'w', encoding='utf8').write('\n'.join(LOG) + '\n')
    print(at); print('\n'.join(LOG)); print('wrote', ', '.join(os.path.basename(p) for p in paths.values()))


if __name__ == '__main__':
    main()
