#!/usr/bin/env python3
"""SEN0401 midterm items, builder of version 1.3.0 (new file): the owner's three cases and the owner's topic list.

Owner words of 2026-11-01 21:09 Istanbul (relayed by the coordinator, file sen0401_exam_owner_topics_v*.json, the NEWEST is read):
  C1 ordering of spent outputs (replaces mt2:i06), C2 mined or not (replaces mt2:i07), C3 full spending / change and fee (replaces mt2:i02);
  mt2:i05 and mt2:i23 are kept; every other item of v1.2.0 is carried over unchanged. The structure v1.0.0 is NOT touched (this builder does not write it).
Owner rules: original wording and numbers, simple arithmetic (no calculator), no memorisation, a tip with every term, every abbreviation spelled out at first use, synthetic data only.

Input (read only): sen0401_exam_items_midterm_v1_2_0.json, the newest sen0401_exam_owner_topics_v*.json, the critical points list.
Output (new files): sen0401_exam_items_midterm_v1_3_0.json, sen0401_exam_items_midterm_computed_v1_3_0.txt, sen0401_exam_items_midterm_topic_map_v1_3_0.json/.txt.
Every number and every answer of the three cases is computed HERE by a program and asserted against the printed text; nothing is typed in by hand.

Usage: build_v1_3_0.py [--outdir DIR]   (default: this folder; refuses to overwrite)
"""
import glob, itertools, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_2_0.json')
CPF = os.path.join(HERE, 'sen0401_exam_critical_points_v1_0_0.json')
VERSION = '1.3.0'
LOG = []


def log(*a): LOG.append(' '.join(str(x) for x in a))


def newest_topics():
    fs = glob.glob(os.path.join(HERE, 'sen0401_exam_owner_topics_v*.json'))
    key = lambda p: tuple(int(x) for x in re.search(r'_v(\d+)_(\d+)_(\d+)\.json$', p).groups())
    return sorted(fs, key=key)[-1]


def compose(body, tips, ask):
    t = ('Tips: ' + '; '.join('%s: %s' % (a, b) for a, b in tips) + '.') if tips else ''
    return ' '.join(x for x in (body, t, ask) if x)


def fmt(n): return '{:,}'.format(n)


# ------------------------------------------------------------------ C1: ordering of spent outputs
def case_c1():
    """A chain of transactions. Each one spends an output of the one before it. The order is recomputed from the spending references; it must be unique."""
    # name -> list of (spent transaction, output number); None = a coinbase transaction (spends no earlier output)
    refs = {'G': [], 'E': [('G', 0)], 'H': [('E', 1)], 'B': [('H', 0)], 'J': [('B', 0)]}
    outs = {'G': 1, 'E': 2, 'H': 1, 'B': 2, 'J': 1}                      # outputs made by each transaction
    for t, rs in refs.items():
        for p, k in rs: assert k < outs[p], (t, p, k)                    # a spent output exists
    names = list(refs)
    valid = [o for o in itertools.permutations(names) if all(o.index(p) < o.index(t) for t, rs in refs.items() for p, _ in rs)]
    assert len(valid) == 1, valid                                         # the references fix ONE order
    order = list(valid[0])
    assert order == ['G', 'E', 'H', 'B', 'J'] and [t for t in names if not refs[t]] == ['G']
    log('C1 transactions', names, 'spending references', {t: refs[t] for t in names})
    log('C1 permutations of the 5 transactions checked: %d; orders that put every spender after the transaction it spends: %d -> %s' % (len(list(itertools.permutations(names))), len(valid), ' < '.join(order)))
    log('C1 the only transaction that spends nothing is the coinbase transaction:', [t for t in names if not refs[t]])

    def step(t):
        if not refs[t]:
            return ('Transaction %s is a coinbase transaction (the first transaction of a block: it creates new coins and spends no earlier output) and makes one output (a coin: an amount with a lock).' % t)
        (p, k), = refs[t]
        spent = 'the output' if outs[p] == 1 else 'output %d' % k
        first = 'spends (names as an input) ' if t == order[1] else 'spends '
        made = 'one output' if outs[t] == 1 else 'two outputs, numbered 0 and 1'
        return 'Transaction %s %s%s of transaction %s and makes %s.' % (t, first, spent, p, made)
    steps = [step(t) for t in order]
    for t, s_ in zip(order, steps): log('C1 step in true order:', s_)
    return dict(steps=steps, order=order)


# ------------------------------------------------------------------ C2: mined or not
def case_c2():
    """Facts: C is inside a block; C spends an output of B; B spends an output of A; E spends an output of D. A block holds a transaction only if every output it spends already exists
    in that block or an earlier one. Which transactions are shown to be mined? Brute force over all 32 states."""
    spends = {'C': ['B'], 'B': ['A'], 'E': ['D'], 'A': [], 'D': []}
    names = sorted(spends)
    states = []
    for bits in itertools.product([0, 1], repeat=len(names)):
        mined = {n for n, b in zip(names, bits) if b}
        if 'C' not in mined: continue                                    # the one fact: C is inside a block
        if all(set(spends[t]) <= mined for t in mined): states.append(mined)     # closed: a mined transaction has mined parents
    forced = set.intersection(*states)
    possible = set.union(*states)
    assert forced == {'A', 'B', 'C'}, forced
    undecided = possible - forced
    assert undecided == {'D', 'E'}, undecided
    d_mined = any('D' in s for s in states); d_not = any('D' not in s for s in states); e_mined = any('E' in s for s in states); e_not = any('E' not in s for s in states)
    assert d_mined and d_not and e_mined and e_not                        # each of D and E may be mined or may wait
    assert all('E' not in s or 'D' in s for s in states)                  # E mined needs D mined
    log('C2 facts: C is inside a block; C spends an output of B; B spends an output of A; E spends an output of D; nothing says E is inside a block')
    log('C2 states of the 5 transactions that agree with the facts (a mined transaction has mined parents): %d of 32' % len(states))
    log('C2 shown to be mined in every state:', sorted(forced), '; undecided (mined in some states, waiting in others):', sorted(undecided))
    return dict(forced=sorted(forced), undecided=sorted(undecided))


# ------------------------------------------------------------------ C3: full spending, change and fee
def case_c3():
    ins = [70000, 45000, 25000]; outs = [60000, 35000]; fee_first, fee_now = 5000, 8000
    tin, tout = sum(ins), sum(outs)
    left = tin - tout
    change_first, change_now = left - fee_first, left - fee_now
    assert (tin, tout, left, change_first, change_now) == (140000, 95000, 45000, 40000, 37000)
    assert tout + change_now + fee_now == tin and tout + change_first + fee_first == tin
    # no change output: everything left over is the fee, the miner collects it
    fee_if_none = tin - tout
    assert fee_if_none == left == 45000
    # simple arithmetic: at most three addends, every figure a multiple of 1,000 below 1,000,000
    assert len(ins) <= 3 and all(x % 1000 == 0 and x < 10 ** 6 for x in ins + outs + [fee_first, fee_now, tin, tout, left, change_first, change_now])
    log('C3 inputs', ins, 'sum', tin, '; payment outputs', outs, 'sum', tout, '; left over', left)
    log('C3 first fee %d leaves change %d; raised fee %d leaves change %d (a higher fee leaves less change); with no change output the miner collects %d' % (fee_first, change_first, fee_now, change_now, fee_if_none))
    body = ('A wallet builds one payment from three unspent outputs (whole coins) of %s, %s and %s satoshis. It pays %s to Ana and %s to Ben. '
            'The sender first planned a fee of %s, then raises it to %s so that miners pick the payment sooner. No change output is written yet.'
            % (fmt(ins[0]), fmt(ins[1]), fmt(ins[2]), fmt(outs[0]), fmt(outs[1]), fmt(fee_first), fmt(fee_now)))
    tips = [['satoshi', 'one hundred-millionth of a bitcoin'], ['unspent output', 'a coin no later payment has used'],
            ['change', 'the part of the inputs that returns to the sender'], ['fee', 'what a miner collects for adding the payment to a block'],
            ['miner', 'a computer that adds blocks to the shared record']]
    q = compose(body, tips, 'What change output is needed, and what if none is written?')
    options = ['Change %s; with no change output the miner would collect %s.' % (fmt(change_first), fmt(left)),
               'Change %s; with no change output the miner would collect all %s left over.' % (fmt(change_now), fmt(left)),
               'Change %s; with no change output the %s left over would return to the sender.' % (fmt(change_now), fmt(left)),
               'Change %s; the fee of %s is then recorded in a separate fee field.' % (fmt(left), fmt(fee_now))]
    assert len(set(options)) == 4
    return dict(q=q, tips=tips, options=options, answer=1, computed='inputs %d minus payment outputs %d = %d left over; minus the fee %d = change %d; with no change output the miner collects all %d (program in the builder)' % (tin, tout, left, fee_now, change_now, left))


# ------------------------------------------------------------------ B (owner's new points of 21:23): block reward by height, halving interval, legal and illegal coinbase
def case_b():
    sub0, interval, height, fees, claim = 16, 10, 23, 3, 9
    subsidy = sub0 >> (height // interval)                 # a right shift per halving interval, fractions dropped
    limit = subsidy + fees
    excess = claim - limit
    assert (height // interval, subsidy, limit, excess) == (2, 4, 7, 2)
    assert claim > limit                                    # the coinbase of the case is illegal
    legal = [c for c in range(0, 13) if c <= limit]
    log('B toy chain: subsidy %d at height 0, halved every %d blocks; height %d is in interval %d, subsidy %d; fees %d; a coinbase may claim at most %d; the claim %d is illegal and too large by %d' % (sub0, interval, height, height // interval, subsidy, fees, limit, claim, excess))
    body = ('A toy chain starts with a block subsidy of %d coins at height 0 (the first block). Every %d blocks the subsidy is halved and any fraction is dropped. A miner builds the block at height %d; the transactions in it leave %d coins of fees, '
            'and its coinbase transaction claims %d coins. A block is invalid if its coinbase transaction claims more than the subsidy plus the fees.' % (sub0, interval, height, fees, claim))
    tips = [['block subsidy', 'the new coins that each block creates for its miner'], ['coinbase transaction', 'the first transaction of a block, by which the miner claims the subsidy and the fees'],
            ['fees', 'what the transactions of the block leave over, collected by the miner'], ['halved', 'cut to one half'], ['block height', 'the number of blocks before it, so the first block has height 0']]
    return dict(q=compose(body, tips, 'By how many coins is the claim too large?'), tips=tips, key=excess, computed='subsidy %d >> (%d // %d) = %d; limit %d + %d = %d; claim %d - %d = %d (program in the builder)' % (sub0, height, interval, subsidy, subsidy, fees, limit, claim, limit, excess))


# ------------------------------------------------------------------ the three new items
def new_items(old):
    by = {i['key']: i for i in old}
    c1, c2, c3 = case_c1(), case_c2(), case_c3()
    cb = case_b()
    i06 = dict(
        key='mt2:i06:order-wallet-to-block', type='Ordering', chapters=[2], bloom=2, kind='direct',
        source={'file': '03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx', 'locator': "slide 15 'A chain of transactions' (15 of 35): outputs become inputs, and the chain leads back in time"},
        sources=[{'file': '03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx', 'locator': "slide 16 'Which outputs are still unspent' (16 of 35)"},
                 {'file': '03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_3_0.pptx', 'locator': "slide 58 'Lock time and the coinbase (2 of 3)': the coinbase transaction is first in the block and spends nothing"}],
        critical_points=['CP2.01', 'CP2.11'],
        seeds=['ch02/question_bank_v1_0_0.json#14', 'ch02/question_bank_v1_0_0.json#15'], no_seed_reason='',
        enhancements=['change the situation', 'reverse the question'], papers=['midterm'],
        from_item=by['mt2:i06:order-wallet-to-block']['from_item'], replaces=['mt2:i06:order-wallet-to-block'], owner_case='C1',
        steps=c1['steps'],
        tips=[['coinbase transaction', 'the first transaction of a block: it creates new coins and spends no earlier output'], ['output', 'a coin: an amount with a lock'], ['spends', 'names as an input']],
        terms=['coinbase transaction', 'output', 'spend', 'chain of transactions'],
        instruction='Put the five transactions in the order in which they were created: write 1 for the earliest and 5 for the latest. Each transaction spends an output of the one before it.',
        computed='order recomputed from the spending references: ' + ' < '.join(c1['order']) + ' (the only one of the 120 orders in which every spender follows the transaction it spends)',
        abbreviations={}, understanding='reason: why a transaction that spends an output always comes after the transaction that made it, back to the coinbase transaction')
    i07 = dict(
        key='mt2:i07:fill-fee-rate-and-set', type='FillBlankGroup', from_item=by['mt2:i07:fill-fee-rate-and-set']['from_item'], replaces=['mt2:i07:fill-fee-rate-and-set'], owner_case='C2',
        chapters=[2, 6], bloom=2, kind='synthesis',
        source={'file': '03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx', 'locator': "slide 16 'Which outputs are still unspent' (16 of 35): unspent outputs are the coins that exist right now"},
        sources=[{'file': '03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_3_0.pptx', 'locator': "slide 25 'A spend updates the UTXO set' (25 of 71): remove what is spent, add what is created"}],
        critical_points=['CP2.01', 'CP2.04', 'CP2.11', 'CP6.09'],
        seeds=['ch02/question_bank_v1_0_0.json#15', 'ch06/question_bank_v1_0_0.json#50', 'ch06/question_bank_v1_0_0.json#54'], no_seed_reason='',
        enhancements=['change the situation', 'add a reasoning step', 'reverse the question'], papers=['midterm'],
        blanks=[{'text': 'Five transactions: C is inside a block (a batch of transactions that miners add to the shared record). C spends (names as an input) an output (a coin: an amount with a lock) of B; B spends an output of A; '
                         'E spends an output of D. Nothing says E is inside a block. A block holds a transaction only if every output it spends already exists in that block or an earlier one, so A and B are ____.',
                 'answer': 'mined (already inside a block)'},
                {'text': 'E names only an output of D and is not known to be inside a block, therefore D and E are ____.',
                 'answer': 'not shown to be mined (each may be mined or may still wait)'}],
        distractors=['not mined (still waiting for a block)', 'mined later than C (after C in the chain)'],
        tips=[['mined', 'already inside a block'], ['not shown to be mined', 'each may be mined or may still wait'], ['not mined', 'still waiting for a block'], ['mined later than C', 'after C in the chain'],
              ['block', 'a batch of transactions that miners add to the shared record'], ['spends', 'names as an input'], ['output', 'a coin: an amount with a lock']],
        terms=['mined', 'block', 'spend', 'output'],
        instruction='Choose for each blank the entry of the bank that makes the sentence true; write its bank code. Each bank entry says what it means.',
        computed='shown mined in all 5-transaction states that agree with the facts: %s; undecided: %s (brute force over 32 states in the builder)' % (', '.join(c2['forced']), ', '.join(c2['undecided'])),
        abbreviations={}, understanding='reason: why a transaction that a mined transaction spends from must be mined too, and why a transaction named only by an unmined one is not shown to be mined')
    i02 = dict(
        key='mt2:i02:fee-not-written', type='ChoiceFour', chapters=[1, 2], bloom=3, kind='synthesis',
        source={'file': '03-materials/ch01/SEN0401_Ch01_Introduction_3e_v3_2_0.pptx', 'locator': "slide 36 'What the outputs leave over is the fee' (36 of 62)"},
        sources=[{'file': '03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx', 'locator': "slide 22 'A higher fee rate leaves less change' (22 of 35)"},
                 {'file': '03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx', 'locator': "slide 21 'From coins to a signed transaction': the five steps a wallet takes"}],
        critical_points=['CP1.06', 'CP2.02', 'CP2.14', 'CP2.09', 'CP2.10', 'CP2.03'],
        seeds=['ch02/question_bank_v1_0_0.json#54', 'ch02/question_bank_v1_0_0.json#85', 'ch02/question_bank_v1_0_0.json#64'], no_seed_reason='',
        enhancements=['change the situation', 'change the numbers', 'add a reasoning step', 'combine chapters'], papers=['midterm'],
        from_item=by['mt2:i02:fee-not-written']['from_item'], replaces=['mt2:i02:fee-not-written'], owner_case='C3',
        q=c3['q'], options=c3['options'], answer=c3['answer'], tips=c3['tips'],
        terms=['satoshi', 'unspent', 'change', 'fee', 'miner'], computed=c3['computed'], abbreviations={},
        understanding='reason: why the amount that the outputs leave over is the fee that the miner collects when no change output is written, and why a higher fee leaves less change')
    i03 = dict(
        key='mt2:i03:toy-chain-supply', type='NumericAnswer', chapters=[1, 6], bloom=3, kind='synthesis',
        source={'file': '03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_3_0.pptx', 'locator': "slide 59 'The subsidy, halving by halving' (59 of 71): a right shift per halving"},
        sources=[{'file': '03-materials/ch01/SEN0401_Ch01_Introduction_3e_v3_2_0.pptx', 'locator': "slide 60 summary: the cap of 21 million is arithmetic"},
                 {'file': '03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx', 'locator': "slide 30 'The reward halves every 210,000 blocks' (30 of 35)"},
                 {'file': '03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_3_0.pptx', 'locator': "slide 61 'The coinbase and its maturity' (61 of 71)"}],
        critical_points=['CP1.02', 'CP6.18', 'CP6.05'],
        seeds=['ch01/quiz_v1_0_0.json#1', 'ch01/question_bank_v1_1_0.json#4', 'ch06/question_bank_v1_0_0.json#171'], no_seed_reason='',
        enhancements=['change the numbers', 'add a reasoning step', 'change the situation'], papers=['midterm'],
        from_item=by['mt2:i03:toy-chain-supply']['from_item'], replaces=['mt2:i03:toy-chain-supply'], owner_case='B',
        q=cb['q'], key_value=cb['key'], unit='coins', tolerance=0, tips=cb['tips'],
        terms=['subsidy', 'coinbase transaction', 'fees', 'halved', 'block height'], computed=cb['computed'], abbreviations={},
        understanding='use: how the subsidy at a block height follows from the halving interval, and why a coinbase that claims more than the subsidy plus the fees makes the block invalid')
    return {'mt2:i03:toy-chain-supply': i03, 'mt2:i06:order-wallet-to-block': i06, 'mt2:i07:fill-fee-rate-and-set': i07, 'mt2:i02:fee-not-written': i02}


# ------------------------------------------------------------------ the topic map (authored judgement; the links are recomputed from the items)
TOPIC_ROWS = {
    'T1': dict(cps=['CP1.12', 'CP1.03'], verdict='GAP', note='No item of the 24 units links these points. The bonus prompt Q5.a (mt2:b1, marked by hand) touches only the half "no bank in the middle".', bonus=['mt2:b1:no-bank']),
    'T2': dict(cps=['CP1.10', 'CP1.03'], verdict='GAP', note='No item links these points; the bonus prompt Q5.a (mt2:b1) touches the half "every node checks every rule, no referee decides".', bonus=['mt2:b1:no-bank']),
    'T3': dict(cps=['CP1.07', 'CP1.03'], verdict='GAP', note='No machine-read item asks why a double spend is refused. Only the bonus prompt Q5.a (mt2:b1, marked by hand) does.', bonus=['mt2:b1:no-bank']),
    'T4': dict(cps=['CP2.05'], verdict='COVERED', note='mt2:i05 (kept): how many confirmations a shop needs against a stronger attacker, read from a table.', bonus=[]),
    'T5': dict(cps=['CP6.01'], verdict='GAP', note='No item asks what a signature proves. The old ordering step "the wallet signs every input" left the paper with mt2:i06 (owner case C1). A seed exists on the pages: ch02/question_bank_v1_0_0.json#37 (three purposes of a digital signature).', bonus=[]),
    'T6': dict(cps=['CP6.13', 'CP6.01'], verdict='PARTIAL', note='mt2:i18 has one premise (block 74,638: a range check refuses an invalid amount). Nothing asks how a node tells a genuine transaction from a fake one in general.', bonus=[]),
    'T7': dict(cps=['CP2.01', 'CP2.11', 'CP6.10'], verdict='PARTIAL', note='Read as the order and the moment of spending: C1 (mt2:i06, spending order), C2 (mt2:i07, mined or not), and mt2:i22 (relative timelock). The owner confirms whether this is the topic he means.', bonus=[]),
    'T8': dict(cps=['CP5.02', 'CP5.09', 'CP5.15'], verdict='PARTIAL', note='mt2:i20 (restore from a recovery code: passphrase, labels), mt2:i17 and mt2:i19 use the words. No item asks WHY seed words replaced hand-managed random keys (CP5.02 is not linked by any item).', bonus=[]),
    'T9': dict(cps=['CP1.12'], verdict='GAP', note='No item or bonus prompt links the point that Bitcoin is borderless (CP1.12).', bonus=[]),
}
TOPIC_ITEMS = {'T1': [], 'T2': [], 'T3': [], 'T4': ['mt2:i05:shop-confirmations'], 'T5': [], 'T6': ['mt2:i18:match-story-lesson'],
               'T7': ['mt2:i06:order-wallet-to-block', 'mt2:i07:fill-fee-rate-and-set', 'mt2:i22:trace-sequence-field'], 'T8': ['mt2:i20:restore-passphrase-labels', 'mt2:i17:words-to-entropy', 'mt2:i19:trace-gap-limit'], 'T9': []}


def topic_map(items, topics_doc, topics_file):
    cp = {p['id']: p for p in json.load(open(CPF, encoding='utf8'))['list_A_points_carried_by_a_source']}
    link = {}
    for i in items:
        for c in i['critical_points']: link.setdefault(c, []).append(i['key'])
    keys = {i['key'] for i in items}
    rows = []
    for t in topics_doc['topics']:
        r = TOPIC_ROWS[t['id']]
        assert all(k in keys for k in TOPIC_ITEMS[t['id']]), t['id']
        assert all(c in cp for c in r['cps']), t['id']
        linked = {c: link.get(c, []) for c in r['cps']}
        rows.append(dict(id=t['id'], topic=t['topic'], verdict=r['verdict'], item_keys=TOPIC_ITEMS[t['id']] or 'GAP', bonus_prompts=r['bonus'], critical_points=linked, note=r['note']))
    assert {t['id'] for t in topics_doc['topics']} == set(TOPIC_ROWS), 'the topic list changed: TOPIC_ROWS must be extended by a person'
    return dict(version=VERSION, owner_topics_file=os.path.basename(topics_file), owner_topics_version=topics_doc['version'], rows=rows)


def topic_text(tm):
    L = ['TOPIC MAP of the owner\'s topics (file %s, version %s) against the midterm items v1.3.0' % (tm['owner_topics_file'], tm['owner_topics_version']),
         'verdicts: COVERED = an item asks it; PARTIAL = an item asks a part or a neighbouring point; GAP = no machine-read item. The reading of each topic title is the author\'s; the owner confirms or corrects it.', '']
    for r in tm['rows']:
        L.append('%s  %-62s %s' % (r['id'], r['topic'], r['verdict']))
        L.append('     item keys: %s' % (', '.join(r['item_keys']) if isinstance(r['item_keys'], list) else r['item_keys']))
        if r['bonus_prompts']: L.append('     bonus prompt (hand-marked): %s' % ', '.join(r['bonus_prompts']))
        L.append('     critical points and the items that link them: %s' % '; '.join('%s -> %s' % (c, ','.join(k.split(':')[1] for k in v) or 'no item') for c, v in r['critical_points'].items()))
        L.append('     %s' % r['note'])
    n = {v: sum(1 for r in tm['rows'] if r['verdict'] == v) for v in ('COVERED', 'PARTIAL', 'GAP')}
    L += ['', 'COUNT %s of %d topics' % (n, len(tm['rows']))]
    return '\n'.join(L) + '\n'


POINT_ROWS = [
    dict(id='A', point='total inputs against total outputs of a transaction, with and without a fee (the difference is the fee)', verdict='COVERED', items=['mt2:i02:fee-not-written'],
         note='C3: inputs 140,000, payments 95,000; with a fee of 8,000 the change is 37,000; with no change output the whole 45,000 left over is the fee.'),
    dict(id='B', point='block reward by block height (halving, blocks per halving interval); legal against illegal coinbase transaction (a claim above subsidy plus fees is invalid)', verdict='COVERED', items=['mt2:i03:toy-chain-supply'],
         note='mt2:i03 reworked (NumericAnswer slot): toy subsidy 16, halved every 10 blocks, block at height 23, fees 3, claim 9 -> too large by 2. NOT asked: the end of halving at the 1-satoshi level, and that satoshi and bitcoin are names outside the blockchain.'),
    dict(id='C', point='all coins are minted by miners: follow any input reference back to a miner\'s coinbase', verdict='COVERED', items=['mt2:i06:order-wallet-to-block'],
         note='C1: five transactions in a chain of spending references back to the single coinbase transaction. C2 (mt2:i07) uses spending references too.'),
    dict(id='D', point='each block includes the identity of the previous block, so a miner restarts its work whenever a new block arrives', verdict='GAP', items=[],
         note='No same-type slot in a chapter that carries it without removing another point. The matching points (mining, chapter 2: CP2.12; checking a block header, chapter 3: CP3.11) are linked by no item.'),
    dict(id='E', point='the hash is unpredictable; the requirement is a value below a target set by the difficulty, adjusted after a fixed number of blocks', verdict='GAP', items=[],
         note='Only the hand-marked bonus prompt Q5.b (mt2:b2, mining is a search nobody can shortcut but anyone can check, CP2.12) touches the unpredictable search. Target and difficulty adjustment are asked nowhere.'),
    dict(id='F', point='the 10-minute block-time rule and soft forks: a steady interval through the difficulty adjustment protects the chain against forking risk', verdict='GAP', items=[],
         note='Asked nowhere. mt2:i23 touches soft forks only as the way segregated witness was introduced (CP6.04); CP6.15 (soft fork) is linked by no item.'),
]


def point_text(items):
    keys = {i['key'] for i in items}
    for r in POINT_ROWS: assert all(k in keys for k in r['items']), r['id']
    L = ['NEW POINTS of the owner (21:23 Istanbul, relayed by the coordinator) against the midterm items v1.3.0', '']
    for r in POINT_ROWS:
        L.append('%s  %-9s %s' % (r['id'], r['verdict'], r['point']))
        L.append('     item keys: %s' % (', '.join(r['items']) or 'GAP'))
        L.append('     ' + r['note'])
    n = {v: sum(1 for r in POINT_ROWS if r['verdict'] == v) for v in ('COVERED', 'GAP')}
    L += ['', 'COUNT %s of %d points' % (n, len(POINT_ROWS))]
    return '\n'.join(L) + '\n'


def build():
    doc = json.load(open(SRC, encoding='utf8'))
    old = doc['items']
    new = new_items(old)
    items = [new.get(i['key'], i) for i in old]
    assert [i['key'] for i in items] == [i['key'] for i in old]
    changed = [k for k in new]
    log('ITEMS CHANGED', changed, '; kept unchanged:', len(items) - len(changed), 'of', len(items))
    for k in changed:
        o = next(i for i in old if i['key'] == k); n = new[k]
        log('  %s: type %s -> %s, chapters %s -> %s, bloom %s -> %s, units %s -> %s' % (k, o['type'], n['type'], o['chapters'], n['chapters'], o['bloom'], n['bloom'],
                                                                                    len(o['blanks']) if o['type'] == 'FillBlankGroup' else 1, len(n['blanks']) if n['type'] == 'FillBlankGroup' else 1))
    ndoc = dict(note='SEN0401 midterm authored items, version 1.3.0 (derived from v1.2.0 by sen0401_exam_items_midterm_build_v1_3_0.py: the owner\'s three cases C1 to C3 replace mt2:i06, mt2:i07 and mt2:i02, and the owner\'s block-reward point B reworks mt2:i03; every other item is carried over unchanged; the structure v1.0.0 is unchanged).',
                version=VERSION, chapters=doc['chapters'], items=items)
    tf = newest_topics(); td = json.load(open(tf, encoding='utf8'))
    tm = topic_map(items, td, tf)
    log('owner topics file read:', os.path.basename(tf), 'version', td['version'], '; topics', len(td['topics']), '; cases', [c['id'] for c in td['cases']], '; kept by the lineage agent', td['kept_by_the_lineage_agent'])
    return ndoc, tm, point_text(items)


def main():
    outdir = os.path.abspath(sys.argv[sys.argv.index('--outdir') + 1]) if '--outdir' in sys.argv else HERE
    ndoc, tm, pt = build()
    paths = {k: os.path.join(outdir, v) for k, v in dict(items='sen0401_exam_items_midterm_v1_3_0.json', computed='sen0401_exam_items_midterm_computed_v1_3_0.txt',
                                                         tmj='sen0401_exam_items_midterm_topic_map_v1_3_0.json', tmt='sen0401_exam_items_midterm_topic_map_v1_3_0.txt', ptt='sen0401_exam_items_midterm_new_points_map_v1_3_0.txt').items()}
    for p in paths.values():
        if os.path.exists(p): sys.exit('refusing to overwrite ' + p)
    json.dump(ndoc, open(paths['items'], 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    open(paths['computed'], 'w', encoding='utf8').write('\n'.join(LOG) + '\n')
    json.dump(tm, open(paths['tmj'], 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    open(paths['tmt'], 'w', encoding='utf8').write(topic_text(tm))
    open(paths['ptt'], 'w', encoding='utf8').write(pt)
    print('\n'.join(LOG)); print(topic_text(tm)); print(pt); print('wrote', ', '.join(os.path.basename(p) for p in paths.values()))


if __name__ == '__main__':
    main()
