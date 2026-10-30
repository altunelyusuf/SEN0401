#!/usr/bin/env python3
"""SEN0401 midterm exam items, builder version 1.0.0 (new file; writes sen0401_exam_items_midterm_v1_0_0.json and sen0401_exam_items_midterm_computed_v1_0_0.txt).

WHAT THIS IS. The 24 AUTHORED items of the MIDTERM exam (the make-up items are the later story ST_Exam_Items_Makeup and are not written here), in the authored-items format of the exam
engine v1.1.0. The owner's ruling of 2026-10-30: the questions of the interactive pages are SEEDS, not exam items. Every item below is new: it was made from one or more seed items
(links 'chNN/question_bank_vX.json#idx', or 'chNN/quiz_v1_0_0.json#idx') or, where the course holds no page question on the point, from the source of the critical point itself
('none: written from the source of the point'). Each item records the enhancement(s) applied (the five of the ruling: change the situation, combine chapters, reverse the question,
add a reasoning step, change the numbers), the critical point(s) of list A that it tests, its chapters, Bloom level, kind (direct or synthesis; 'indirect' is not used), type, source and terms.

CODE AND NUMBERS ARE COMPUTED. Every number item and every trace item is computed here by running a program; the printed output is the key. Every factual claim that a choice item
rests on is asserted by a program as well (a statement that must be true or false by arithmetic is computed, then asserted). The text printed by this run is kept in
sen0401_exam_items_midterm_computed_v1_0_0.txt.

CONVENTIONS that this file builds in: chapter list 1 to 6 with 4 items per chapter (equal weight, the working default; the owner has not decided weights), 24 items, a majority at
Apply or above, at least 6 at Analyze or above, code lines at most 45 characters and at most 12 lines, no letter-referencing options, answers of number and trace items of at most five
characters (the answer sheet gives such an answer five boxes), no real student data.

Usage: sen0401_exam_items_midterm_build_v1_0_0.py [--outdir DIR]   (default: the folder of this file)
"""
import io, json, os, sys, contextlib
from math import exp, factorial
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = '1.0.0'

DECK = {1: '03-materials/ch01/SEN0401_Ch01_Introduction_3e_v3_2_0.pptx',
        2: '03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx',
        3: '03-materials/ch03/SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx',
        4: '03-materials/ch04/SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx',
        5: '03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx',
        6: '03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_3_0.pptx'}
LEG3 = '03-materials/owner-legacy-2025/slides-2025/Chapter_3_BitcoinCore_TheReferenceImplementation_v1_0_0.pptx'
LOG = []


def log(*a):
    LOG.append(' '.join(str(x) for x in a))


def run(code, extra=None):
    """Run a code listing and return what it printed (stripped). The listing is the one printed on the paper."""
    ns = dict(extra or {}); buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, '<item>', 'exec'), ns)
    return buf.getvalue().strip()


def src(ch, locator):
    return {'file': DECK[ch], 'locator': locator}


ITEMS = []


def add(**kw):
    kw.setdefault('papers', ['midterm'])
    ITEMS.append(kw)
    return kw


# ===================================================================================================================== chapter 1
# I01  Mt. Gox, two events, two lessons (chapters 1 and 5)
add(key='mt1:i01:gox-two-events', type='ChoiceFour', chapters=[1, 5], bloom=4, kind='synthesis',
    q=('The course tells two stories about the exchange Mt. Gox in 2014. On 28 February it filed for bankruptcy after admitting that about 850,000 bitcoin were gone. Three weeks later it '
       'said it had found about 200,000 bitcoin in an old-format wallet file that it believed was empty. Which statement says correctly what each story teaches?'),
    options=['The filing: customers held balances on a website while the keys were in other hands, so whoever holds the keys holds the coins; the old file: a wallet file can still hold '
             'spendable keys, so an untested file is not an empty one.',
             'The filing: an untested backup file is not an empty one; the old file: whoever holds the keys holds the coins, exchanges included.',
             'The filing: the network let the exchange spend the same coins twice; the old file: miners had held the coins back until the exchange paid a larger fee.',
             'The filing: customers lost their own keys while writing down a recovery code; the old file: backups expire, so an old wallet file can safely be thrown away.'],
    answer=0,
    source=src(1, "slide 44 notes and slide 'The exchange that lost everyone's coins' (44 of 62)"),
    sources=[src(1, "slide 44 (custody lesson, 28 February 2014)"), src(5, "slide 56 'The 200,000 BTC in a forgotten wallet file' (56 of 68)")],
    critical_points=['CP1.09', 'CP5.18', 'CP1.04'], seeds=[],
    no_seed_reason='none: written from the source of the point (the page banks and quizzes hold no question on the Mt. Gox stories)',
    enhancements=['combine chapters', 'add a reasoning step'],
    terms=['mt. gox', 'old-format wallet', 'whoever holds the keys holds the coins', 'bankruptcy'])

# I02  toy chain issuance (chapters 1 and 6): the cap is arithmetic
toy = []
sub, blocks, era = 40, 50, 0
while sub > 0:
    toy.append(blocks * sub); sub >>= 1
toy_total = sum(toy)
log('I02 toy chain: subsidy 40, halved by a right shift every 50 blocks:', toy, 'total', toy_total)
assert toy_total == 3900
add(key='mt1:i02:toy-chain-supply', type='NumericAnswer', chapters=[1, 6], bloom=3, kind='synthesis',
    q=('A toy chain pays a block subsidy of 40 coins. Every 50 blocks the subsidy is halved by a right shift, so any fraction is dropped, and once it reaches zero no more coins are '
       'created. How many coins does the subsidy create in total over the whole life of the chain?'),
    key_value=toy_total, unit='coins', tolerance=0,
    source=src(6, "slide 59 'The subsidy, halving by halving' (59 of 71): a right shift; the last subsidy at block 6,929,999"),
    sources=[src(1, "slide 60 summary: the cap of 21 million is arithmetic"), src(2, "slide 30 'The reward halves every 210,000 blocks' (30 of 35)")],
    critical_points=['CP1.02', 'CP6.18'], seeds=['ch01/quiz_v1_0_0.json#1', 'ch06/question_bank_v1_0_0.json#100'], no_seed_reason='',
    enhancements=['change the numbers', 'add a reasoning step', 'change the situation'],
    terms=['halves', 'subsidy', 'right shift', '21 million'], computed='toy chain subsidy sum (program in the builder)')

# I03  volume-weighted price, reversed
vw_known = [(1, 62000), (2, 63000)]
vw_day, vw_vol = 63250, 4
vw_third = vw_day * vw_vol - sum(b * p for b, p in vw_known)
vw_third_price = vw_third / (vw_vol - sum(b for b, p in vw_known))
log('I03 volume-weighted price: day figure', vw_day, 'volume', vw_vol, 'third trade price', vw_third_price)
assert vw_third_price == 65000 and sum(b * p for b, p in vw_known + [(1, vw_third_price)]) / vw_vol == vw_day
add(key='mt1:i03:vwap-third-trade', type='NumericAnswer', chapters=[1], bloom=3, kind='direct',
    q=('On one day a price service sees three trades of bitcoin: 1 bitcoin at 62,000 dollars, 2 bitcoin at 63,000 dollars, and 1 bitcoin at a price that is not shown. The service '
       'publishes a volume-weighted figure for the day of 63,250 dollars per bitcoin. At what price, in dollars per bitcoin, did the third trade happen?'),
    key_value=int(vw_third_price), unit='dollars per bitcoin', tolerance=0,
    source=src(1, "slide 23 'No one sets the price: trades do' (23 of 62)"), sources=[src(1, "slide 23 notes: a volume-weighted average gives one fair figure for the day")],
    critical_points=['CP1.11', 'CP1.02'], seeds=['ch01/question_bank_v1_1_0.json#52'], no_seed_reason='',
    enhancements=['reverse the question', 'change the numbers', 'add a reasoning step'],
    terms=['volume-weighted', 'price is discovered by trades'], computed='third trade price (program in the builder)')

# I04  no fee field; batching shape (chapters 1 and 2)
inp, outp = [400000, 250000], [300000, 200000, 100000, 29000]
fee4 = sum(inp) - sum(outp)
log('I04 batching: inputs', inp, 'outputs', outp, 'fee', fee4)
assert fee4 == 21000
add(key='mt1:i04:fee-not-written', type='ChoiceFour', chapters=[1, 2], bloom=3, kind='synthesis',
    q=('A wallet shows a draft batching payment. Its inputs are 400,000 and 250,000 satoshis. Its outputs are 300,000, 200,000, 100,000 and 29,000 satoshis. A colleague says that '
       'every node will refuse it because the inputs and the outputs are not equal. Which reply is correct?'),
    options=['No: the 21,000 satoshis that the outputs leave over are the miner\'s fee; no field records it, it is the difference between inputs and outputs, so the transaction can be valid.',
             'Yes: the ledger must balance exactly, so the wallet must lower one output by 21,000 satoshis before any node will accept the transaction.',
             'No: the nodes return the 21,000 satoshis left over to the wallet as change, so nothing is lost and no fee is paid.',
             'Yes: with four outputs the payment is a consolidation, and a consolidation must spend exactly the sum of its inputs.'],
    answer=0,
    source=src(1, "slide 36 'What the outputs leave over is the fee' (36 of 62)"), sources=[src(1, "slide 36 notes: fees are implied, never written"), src(2, "slide 19 notes: in every shape inputs minus outputs is the fee")],
    critical_points=['CP1.06', 'CP2.14', 'CP2.02'], seeds=['ch02/question_bank_v1_0_0.json#3', 'ch02/question_bank_v1_0_0.json#62'], no_seed_reason='',
    enhancements=['combine chapters', 'change the situation', 'change the numbers', 'add a reasoning step'],
    terms=['fee', 'batching', 'consolidation', 'change'])

# ===================================================================================================================== chapter 2
# I05  fee rate, weight and change (chapters 2 and 6)
w5, rate5, coin5, pay5 = 1126, 18, 200000, 120000
vb5 = -(-w5 // 4); fee5 = rate5 * vb5; chg5 = coin5 - pay5 - fee5
log('I05 weight', w5, 'virtual bytes', vb5, 'fee at', rate5, 'sat/vB', fee5, 'change', chg5)
assert (vb5, fee5, chg5) == (282, 5076, 74924)
add(key='mt1:i05:change-after-fee-rate', type='NumericAnswer', chapters=[2, 6], bloom=3, kind='synthesis',
    q=('A wallet spends one coin of 200,000 satoshis to pay 120,000 satoshis to a payee; everything else returns to the wallet as change. The finished transaction weighs 1,126 weight '
       'units and the wallet pays a fee rate of 18 satoshis per virtual byte. How many satoshis does the change output hold?'),
    key_value=chg5, unit='satoshis', tolerance=0,
    source=src(2, "slide 22 'A higher fee rate leaves less change' (22 of 35)"),
    sources=[src(2, "slide 14 (569 weight units are 143 virtual bytes, rounded up)"), src(6, "slide 63 'From 194 bytes to 569 weight' (63 of 71)")],
    critical_points=['CP2.10', 'CP2.09', 'CP6.19', 'CP2.02'], seeds=['ch02/question_bank_v1_0_0.json#62'], no_seed_reason='',
    enhancements=['combine chapters', 'add a reasoning step', 'change the numbers'],
    terms=['weight units', 'virtual bytes', 'fee rate', 'change'], computed='virtual bytes, fee and change (program in the builder)')

# I06  ordering: from a wallet to a block
add(key='mt1:i06:order-wallet-to-block', type='Ordering', chapters=[2], bloom=2, kind='direct',
    steps=['The wallet takes whole coins from its unspent outputs until they cover the payment and the fee.',
           'The wallet writes the payee output and the change output and leaves the fee as the difference.',
           'The wallet signs every input.',
           'A node checks the rules and relays the transaction to its peers.',
           'A miner finds a valid nonce and adds a block that holds the transaction.'],
    source=src(2, "slide 33 'Summary: the six answers', questions 3 and 4 (33 of 35)"),
    sources=[src(2, "slide 18 'Coin selection: pick, pay, change back'"), src(2, "slide 25 'One more zero, many more tries'")],
    critical_points=['CP2.03', 'CP2.04'], seeds=['ch02/question_bank_v1_0_0.json#81'], no_seed_reason='',
    enhancements=['change the situation'],
    terms=['unspent outputs', 'nonce', 'relays', 'change', 'fee'])

# I07  confirmations, computed table (chapter 2)
def catch_up(q, z):
    p = 1 - q; lam = z * q / p; s = 0.0
    for k in range(z + 1):
        s += (lam ** k * exp(-lam) / factorial(k)) * (1 - (q / p) ** (z - k))
    return 1 - s


pct = lambda q, z: round(100 * catch_up(q, z), 1)
row10 = {z: pct(0.1, z) for z in (1, 2, 3, 6)}
row10[6] = round(100 * catch_up(0.1, 6), 2)
row30 = {z: pct(0.3, z) for z in (1, 3, 6, 9, 10)}
log('I07 catch-up chances in percent, attacker 10 percent:', row10, ' attacker 30 percent:', row30)
assert row10 == {1: 20.5, 2: 5.1, 3: 1.3, 6: 0.02} and row30 == {1: 62.8, 3: 32.5, 6: 13.2, 9: 5.5, 10: 4.2}
below5_10 = min(z for z in range(0, 40) if 100 * catch_up(0.1, z) < 5)
below5_30 = min(z for z in range(0, 60) if 100 * catch_up(0.3, z) < 5)
log('I07 smallest z with a chance below 5 percent: attacker 10 percent', below5_10, ' attacker 30 percent', below5_30)
assert (below5_10, below5_30) == (3, 10)
add(key='mt1:i07:shop-confirmations', type='ChoiceFour', chapters=[2], bloom=4, kind='direct',
    q=('The chapter recomputes the white paper\'s table: the chance, in percent, that an attacker who holds a share of the hash power ever catches up when a payment has z confirmations. '
       'For an attacker with 10 percent: z = 1 gives 20.5, z = 2 gives 5.1, z = 3 gives 1.3 and z = 6 gives 0.02. For an attacker with 30 percent: z = 1 gives 62.8, z = 3 gives 32.5, '
       'z = 6 gives 13.2, z = 9 gives 5.5 and z = 10 gives 4.2. A shop accepts a payment only when the chance of a reversal is below 5 percent. Which statement follows from these figures?'),
    options=['The shop needs three confirmations against the 10 percent attacker but ten against the 30 percent attacker.',
             'The shop is equally safe at six confirmations against either attacker, because every confirmation divides the chance by the same factor.',
             'Two confirmations are enough against the 10 percent attacker, because the figure for z = 2 is below 5 percent.',
             'Three confirmations are enough against the 30 percent attacker, because the chance falls below 5 percent once z reaches the attacker\'s share.'],
    answer=0,
    source=src(2, "slide 28 'Nakamoto's catch-up table, recomputed' (28 of 35)"), sources=[src(2, "slide 33 summary, question 5: a 10 percent attacker's chance falls from 20.5 to 0.02 percent")],
    critical_points=['CP2.05'], seeds=[], no_seed_reason='',
    enhancements=['change the situation', 'add a reasoning step', 'change the numbers'],
    terms=['confirmations', 'attacker', 'hash power', '20.5'], computed='catch-up table (formula of section 11 of the white paper, in the builder)')

# I08  UTXO set trace, with a code listing
utxo_code = ("utxo = {'a:0': 50, 'b:1': 30}\n"
             "def apply(ins, outs, txid):\n"
             "    for i in ins:\n"
             "        del utxo[i]\n"
             "    for n, v in enumerate(outs):\n"
             "        utxo[txid + ':' + str(n)] = v\n"
             "apply(['a:0'], [20, 29], 'c')\n"
             "apply(['c:0', 'b:1'], [45], 'd')\n"
             "print(sorted(utxo), sum(utxo.values()))")
utxo_out = run(utxo_code)
log('I08 utxo listing prints:', utxo_out)
assert utxo_out == "['c:1', 'd:0'] 74" and 80 - 74 == (50 - 49) + (50 - 45)
no_del = run(utxo_code.replace("        del utxo[i]\n", "        pass\n"))
log('I08 the same listing without the removal of spent outputs prints:', no_del)
add(key='mt1:i08:utxo-set-trace', type='ChoiceFourCode', chapters=[2, 6], bloom=4, kind='synthesis',
    q='The program applies two transactions to a set of unspent outputs that starts at 80 satoshis in total. What does it print, and what explains the total?',
    code=utxo_code,
    options=["['c:1', 'd:0'] 74 : the 6 satoshis that are missing are the fees of the two transactions",
             "['c:1', 'd:0'] 80 : spending moves value to new outputs but never removes any",
             "['a:0', 'b:1', 'c:0', 'c:1', 'd:0'] 174 : spent outputs stay in the set and every new output is added",
             "['c:1', 'd:0'] 74 : the 6 satoshis that are missing are change that was never created"],
    answer=0,
    source=src(2, "slide 16 'Which outputs are still unspent' (16 of 35)"), sources=[src(2, "slide 19 notes: inputs minus outputs is the fee"), src(6, "slide 21 'Inputs: concepts (2 of 4)': an output is spent at most once")],
    critical_points=['CP2.11', 'CP6.09', 'CP2.14'], seeds=['ch02/question_bank_v1_0_0.json#62'], no_seed_reason='',
    enhancements=['combine chapters', 'add a reasoning step', 'change the situation'],
    terms=['unspent', 'fee', 'utxo'], computed=utxo_out)

# ===================================================================================================================== chapter 3
# I09  configuration precedence and the prune / txindex conflict
conf_code = ("# bitcoin.conf\n"
             "prune=550\n"
             "txindex=1\n"
             "dbcache=450\n"
             "# the command line\n"
             "bitcoind -txindex=0 -dbcache=2048")
add(key='mt1:i09:conf-precedence-and-refusal', type='ChoiceFourCode', chapters=[3], bloom=4, kind='direct',
    q='A node reads the configuration file and is started with the command line shown. What happens?',
    code=conf_code,
    options=['It starts with pruning at 550, no transaction index and a cache of 2048: the command line overrides the file, and that removes the conflict.',
             'It refuses to start: the file asks for pruning and the transaction index together, and the file is applied after the command line.',
             'It starts with the transaction index on and a cache of 450, because the configuration file overrides the command line.',
             'It starts with pruning and the transaction index both on, because the refusal applies only to options given on the command line.'],
    answer=0,
    source=src(3, "slide 16 'The command line wins over the file' (16 of 42)"), sources=[src(3, "slide 19 'Pruning and the transaction index do not mix' (19 of 42)")],
    critical_points=['CP3.05', 'CP3.06'], seeds=[], no_seed_reason='',
    enhancements=['add a reasoning step', 'change the situation'],
    terms=['prune', 'txindex', 'dbcache', 'bitcoind', 'command line'])

# I10  matching: situations to options (owner's 2025 chapter 3 option slides)
add(key='mt1:i10:match-node-options', type='Matching', chapters=[3], bloom=3, kind='direct',
    premises=[{'text': 'A volunteer runs a validating node on a laptop with little free disk space and does not need the old blocks.', 'match': 'prune'},
              {'text': 'A block-explorer service must be able to look up any transaction by its identifier.', 'match': 'txindex'},
              {'text': 'The operator wants a message, usually by email, when the node meets an emergency.', 'match': 'alertnotify'},
              {'text': 'A node on a thin connection must limit how many other nodes it accepts, to reduce its bandwidth use.', 'match': 'maxconnections'}],
    responses=['prune', 'txindex', 'alertnotify', 'maxconnections', 'datadir', 'maxmempool'],
    source={'file': LEG3, 'locator': 'slides 25 to 30 (option diagram: alertnotify, datadir, prune, txindex, maxconnections, maxmempool)'},
    sources=[src(3, "slide 19 (prune and txindex)")],
    critical_points=['CP3.14', 'CP3.16', 'CP3.17', 'CP3.18'], seeds=[], no_seed_reason='',
    enhancements=['change the situation', 'reverse the question'],
    terms=['prune', 'txindex', 'alertnotify', 'maxconnections', 'datadir', 'maxmempool'])
ITEMS[-1]['no_seed_reason'] = 'none: written from the source of the point (the option names and purposes come from the owner\'s 2025 chapter 3 slides; no page question matches situations to options)'

# I11  release tags sort by number
tag_code = ("tags = ['v28.0', 'v3.1', 'v28.0rc1',\n"
            "        'v4.0', 'v24.2', 'v9.1']\n"
            "final = [t for t in tags if 'rc' not in t]\n"
            "def key(t):\n"
            "    return [int(p) for p in t[1:].split('.')]\n"
            "a = sorted(final)\n"
            "b = sorted(final, key=key)\n"
            "move = 0\n"
            "for t in final:\n"
            "    move += abs(a.index(t) - b.index(t))\n"
            "print(move)")
tag_out = run(tag_code)
log('I11 tags listing prints:', tag_out)
assert tag_out == '12'
add(key='mt1:i11:trace-release-tags', type='CodeTrace', chapters=[3], bloom=3, kind='direct',
    q=('A script lists release tags, drops the release candidates (their tag carries rc), and compares the order of the final releases sorted as text with the order sorted by version '
       'number. It adds up how far each tag moves between the two orders. What does it print?'),
    code=tag_code, output=tag_out,
    source=src(3, "slide 11 'Release tags sort by number, not by letters' (11 of 42)"),
    critical_points=['CP3.03'], seeds=[], no_seed_reason='',
    enhancements=['change the numbers', 'add a reasoning step', 'change the situation'],
    terms=['release tags', 'release candidates', 'rc'], computed=tag_out)

# I12  rpcauth and P2PKH: two hashes standing in for a secret (chapters 3 and 4)
add(key='mt1:i12:rpcauth-and-p2pkh', type='ChoiceFour', chapters=[3, 4], bloom=4, kind='synthesis',
    q=('A node\'s configuration file holds an rpcauth line, and a P2PKH output script holds a 20-byte hash of a public key. Both keep a hash instead of the secret. '
       'Which statement compares them correctly?'),
    options=['A leak of the file reveals no password, because the rpcauth hash is salted; the P2PKH hash is a commitment to the key, and the key is revealed only when the coins are spent.',
             'A leak of the file reveals the password at once, because rpcauth is only an encoding; the P2PKH hash is revealed together with the key when the output is created.',
             'The rpcauth hash is a commitment that the owner reveals when the coins are spent; the P2PKH hash is salted, so a leak of the script reveals no key.',
             'Both hashes are salted checksums that catch typos, and both secrets are revealed as soon as a node reads the line or the script.'],
    answer=0,
    source=src(3, "slide 26 'rpcauth stores a salted hash, not the password' (26 of 42)"), sources=[src(4, "slide 21 'P2PK holds the key, P2PKH only its hash' (21 of 47)")],
    critical_points=['CP3.08', 'CP4.05'], seeds=[], no_seed_reason='',
    enhancements=['combine chapters', 'change the situation', 'add a reasoning step'],
    terms=['rpcauth', 'salted hash', 'p2pkh', 'commitment', '20-byte hash'])

# ===================================================================================================================== chapter 4
# I13  vanity work factor
v13 = 58 ** (3 - 1)
log('I13 vanity: going from 1 to 3 chosen letters multiplies the average work by 58^2 =', v13)
assert v13 == 3364
add(key='mt1:i13:vanity-factor', type='NumericAnswer', chapters=[4], bloom=3, kind='direct',
    q=('A search for a vanity address needs, on average, a number of tries for one chosen letter after the leading 1. By what factor is the average number of tries larger when the search '
       'asks for three chosen letters instead of one?'),
    key_value=v13, unit='times', tolerance=0,
    source=src(4, "slide 41 'Vanity search: 58 times harder per letter' (41 of 47)"), critical_points=['CP4.12'], seeds=[], no_seed_reason='',
    enhancements=['reverse the question', 'add a reasoning step', 'change the numbers'],
    terms=['vanity', '58 times'], computed='58 raised to 2 (program in the builder)')

# I14  WIF without the final 01 (chapters 4 and 5)
add(key='mt1:i14:wif-flag-and-balance', type='ChoiceFour', chapters=[4, 5], bloom=4, kind='synthesis',
    q=('Dana\'s coins were sent to the address that comes from the compressed public key of her private key. Her paper backup holds that private key in WIF, but this WIF has no '
       'final 01 byte. A new wallet imports it and shows a zero balance. Which diagnosis fits, and which check before funding would have caught it?'),
    options=['The wallet took the key as uncompressed and watches the other address of the same key; restoring from the paper and comparing the first address with the printed one, before any coins were sent, would have caught it.',
             'The missing byte changed the private key itself, so it can no longer produce her public key at all; only a second written copy of the paper would have caught it.',
             'The coins were sent to an address with no key behind it, because a valid checksum does not prove that a key exists; checking the checksum of the address again would have caught it.',
             'The version byte 80 marks a test network key, so the wallet looks for her coins on another network; sending a very small amount first and waiting a day would have caught it.'],
    answer=0,
    source=src(4, "slide 38 'One private key, two addresses' (38 of 47)"), sources=[src(4, "slide 42 'A paper wallet must give back its address' (42 of 47)"), src(4, "slide 45 summary: WIF is Base58Check of version 80, the key and a final 01 when compressed"), src(5, "slide 62 'Code 27: The restore drill' (62 of 68)")],
    critical_points=['CP4.09', 'CP4.10', 'CP4.13', 'CP5.07'], seeds=[], no_seed_reason='',
    enhancements=['combine chapters', 'change the situation', 'add a reasoning step'],
    terms=['wif', 'compressed', 'final 01', 'version 80', 'checksum'])

# I15  fill-in bank (two blanks)
add(key='mt1:i15:fill-hash-and-collision', type='FillBlankGroup', chapters=[4], bloom=2, kind='direct',
    blanks=[{'text': 'A P2PKH output holds only a 20-byte hash of the public key, which acts as a ____ to the key until the coins are spent.', 'answer': 'commitment'},
            {'text': 'Against collisions a 160-bit hash gives only ____ bits of work, which is why SegWit scripts use SHA256.', 'answer': '80'}],
    distractors=['128', 'checksum', 'salt'],
    source=src(4, "slide 21 notes (a commitment) and slide 31 'Collision and preimage: bits of work' (31 of 47)"),
    critical_points=['CP4.05', 'CP4.07'], seeds=[], no_seed_reason='',
    enhancements=['change the situation', 'change the numbers'],
    terms=['commitment', '160-bit hash', '80 bits', 'segwit', 'sha256'])

# ===================================================================================================================== chapter 5
# I16  words and bits, reversed
words16 = 18
tot16 = words16 * 11
ent16 = [e for e in (128, 160, 192, 224, 256) if e + e // 32 == tot16]
log('I16 a code of', words16, 'words holds', tot16, 'bits; entropy sizes that fit:', ent16)
assert ent16 == [192]
add(key='mt1:i16:words-to-entropy', type='NumericAnswer', chapters=[5], bloom=3, kind='direct',
    q=('A recovery code has 18 words. Each word carries 11 bits, and the checksum is one bit for every 32 bits of entropy. How many bits of entropy does the code hold?'),
    key_value=ent16[0], unit='bits', tolerance=0,
    source=src(5, "slide 21 'Generating a recovery code' (21 of 68) and slide 23 'Code 5' (23 of 68)"), critical_points=['CP5.03', 'CP5.08'], seeds=[], no_seed_reason='',
    enhancements=['reverse the question', 'change the numbers'],
    terms=['11 bits', 'checksum', 'entropy'], computed='entropy sizes that fit 18 words (program in the builder)')

# I17  matching: the story and its lesson (chapters 5, 2, 3, 6)
add(key='mt1:i17:match-story-lesson', type='Matching', chapters=[5, 2, 3, 6], bloom=2, kind='synthesis',
    premises=[{'text': 'A programmer paid 7,002 bitcoin in 2011 locked the keys on an encrypted drive, lost the password and has two guesses left.',
               'match': 'Memory is not a backup: a recovery code must be tested by restoring it.'},
              {'text': 'On 15 August 2010 two huge outputs added up to a negative number and about 184 billion bitcoin were created in block 74,638.',
               'match': 'A signed amount needs a range check on each output, not only on the total.'},
              {'text': 'On 7 April 2014 the lead of the reference software passed from one maintainer to the next.',
               'match': 'A reference implementation needs a team and public review, not one keyholder.'},
              {'text': 'On 10 February 2014 an exchange blamed transaction malleability for its missing bitcoin, and researchers checked a year of network traffic.',
               'match': 'A stated cause is tested against the data: malleability changes the txid, not the amount.'}],
    responses=['Memory is not a backup: a recovery code must be tested by restoring it.',
               'A signed amount needs a range check on each output, not only on the total.',
               'A reference implementation needs a team and public review, not one keyholder.',
               'A stated cause is tested against the data: malleability changes the txid, not the amount.',
               'Coins created by a coinbase are locked for 100 blocks, so a reorganisation cannot invalidate coins already spent.',
               'Bech32m closes a weakness of Bech32: an extra q before a final p no longer keeps the checksum valid.'],
    source=src(5, "slide 5 'Two guesses from 7,002 bitcoin' (5 of 68)"),
    sources=[src(6, "slide 41 'The block that created 184 billion bitcoins' (41 of 71)"), src(3, "slide 22 'The project that outlives its keyholders' (22 of 42)"),
             src(6, "slide 50 'Mt. Gox blames malleability' (50 of 71)")],
    critical_points=['CP5.19', 'CP6.13', 'CP2.13', 'CP3.13', 'CP6.16'], seeds=[], no_seed_reason='',
    enhancements=['combine chapters', 'reverse the question'],
    terms=['7,002 bitcoin', '184 billion', 'malleability', 'reference implementation', 'range check'])
ITEMS[-1]['no_seed_reason'] = 'none: written from the source of the point (the page banks and quizzes hold no question that links these four stories to their lessons)'

# I18  gap limit trace
gap_code = ("used = {0, 3, 12, 30}\n"
            "gap, run, found = 10, 0, []\n"
            "for i in range(40):\n"
            "    if i in used:\n"
            "        found.append(i)\n"
            "        run = 0\n"
            "    else:\n"
            "        run += 1\n"
            "        if run == gap:\n"
            "            break\n"
            "print(sum(found))")
gap_out = run(gap_code)
log('I18 gap listing prints:', gap_out)
assert gap_out == '15'
add(key='mt1:i18:trace-gap-limit', type='CodeTrace', chapters=[5], bloom=4, kind='direct',
    q=('A wallet that is recovered from its code scans its keys in order and stops after gap unused keys in a row. The wallet received payments on keys 0, 3, 12 and 30. '
       'The program adds up the numbers of the keys that the scan finds. What does it print?'),
    code=gap_code, output=gap_out,
    source=src(5, "slide 59 'Code 25: The gap limit decides how far a scan looks' (59 of 68)"), critical_points=['CP5.20'], seeds=[], no_seed_reason='',
    enhancements=['change the numbers', 'add a reasoning step', 'reverse the question'],
    terms=['gap limit', 'unused'], computed=gap_out)

# I19  passphrase and labels after a restore
add(key='mt1:i19:restore-passphrase-labels', type='ChoiceFour', chapters=[5], bloom=4, kind='direct',
    q=('Lena\'s phone is stolen. She restores her wallet from her twelve-word recovery code on a new phone. The wallet opens with different addresses, an empty balance and none of her labels. '
       'She had set a passphrase in the old wallet and had exported her labels in the BIP329 format. What is the most complete explanation and the fix?'),
    options=['A passphrase forks the wallet, so the same twelve words without it give a different wallet, and labels cannot be derived from the seed; she must enter the passphrase and import the labels file.',
             'The recovery code was stored on the stolen phone, so the thief has already spent the coins and nothing can be restored.',
             'The gap limit stopped the scan too early; a larger gap limit would bring back both the balance and the labels.',
             'Labels are derived from the seed and were lost with the phone, while the passphrase only changes how the twelve words are spelled, so nothing else is missing.'],
    answer=0,
    source=src(5, "slide 28 'Code 10: A passphrase opens a different wallet' (28 of 68)"), sources=[src(5, "slide 54 'Code 23: Labels exported in the BIP329 format'"), src(5, "slide 63 'A complete backup'")],
    critical_points=['CP5.05', 'CP5.11', 'CP5.17', 'CP5.15', 'CP5.09'], seeds=[], no_seed_reason='',
    enhancements=['change the situation', 'add a reasoning step'],
    terms=['passphrase', 'bip329', 'labels', 'gap limit', 'recovery code'])

# ===================================================================================================================== chapter 6
# I20  CompactSize trace; cs_encode is the encoder of the chapter and is not part of the listing
def cs_encode(n):
    if n < 253: return bytes([n])
    if n <= 0xffff: return b'\xfd' + n.to_bytes(2, 'little')
    if n <= 0xffffffff: return b'\xfe' + n.to_bytes(4, 'little')
    return b'\xff' + n.to_bytes(8, 'little')


assert [len(cs_encode(n)) for n in (1, 252, 253, 65535, 65536, 2 ** 32)] == [1, 1, 3, 3, 5, 9]      # the chapter's own table (slide 20)
cs_code = ("values = [252, 253, 65536, 4294967295]\n"
           "sizes = [len(cs_encode(n)) for n in values]\n"
           "print(sum(sizes))")
cs_out = run(cs_code, {'cs_encode': cs_encode})
log('I20 CompactSize listing prints:', cs_out, '(sizes', [len(cs_encode(n)) for n in (252, 253, 65536, 4294967295)], ')')
assert cs_out == '14'
add(key='mt1:i20:trace-compactsize', type='CodeTrace', chapters=[6], bloom=3, kind='direct',
    q=('The function cs_encode writes a count as a transaction does (the CompactSize encoding of the chapter). The program measures four counts that sit at the edges where the encoding '
       'changes length. What does it print?'),
    code=cs_code, output=cs_out,
    source=src(6, "slide 20 'CompactSize: counting in few bytes' (20 of 71)"), critical_points=['CP6.21'], seeds=[], no_seed_reason='',
    enhancements=['change the numbers', 'add a reasoning step'],
    terms=['compactsize', 'fd', 'fe', 'ff'], computed=cs_out)

# I21  sequence field trace
seq_code = ("seqs = [0xffffffff, 0xfffffffd, 0x0000001e,\n"
            "        0x80000010, 0x00400005]\n"
            "total = 0\n"
            "for s in seqs:\n"
            "    replace = s < 0xfffffffe\n"
            "    timed = (s >> 31) == 0\n"
            "    if replace and timed:\n"
            "        total += s & 0xffff\n"
            "print(total)")
seq_out = run(seq_code)
log('I21 sequence listing prints:', seq_out)
assert seq_out == '35'
add(key='mt1:i21:trace-sequence-field', type='CodeTrace', chapters=[6], bloom=4, kind='direct',
    q=('The program reads five sequence values. A value signals opt-in replacement when it is below 0xfffffffe, and it carries a relative timelock when bit 31 is clear. '
       'The program adds up the low 16 bits of the values that do both. What does it print?'),
    code=seq_code, output=seq_out,
    source=src(6, "slide 29 'The 32 bits of the sequence field' (29 of 71)"), sources=[src(6, "slide 31 'Four sequence values, three meanings' (31 of 71)")],
    critical_points=['CP6.10', 'CP6.02'], seeds=[], no_seed_reason='',
    enhancements=['change the numbers', 'add a reasoning step', 'reverse the question'],
    terms=['sequence', '0xfffffffe', 'bit 31', 'relative timelock'], computed=seq_out)

# I22  block 74,638 and the range check (chapters 6 and 2)
big = 9223372036854277039
wrapped = (2 * big) & 0xffffffffffffffff
signed_total = wrapped - 2 ** 64 if wrapped >= 2 ** 63 else wrapped
MAX_MONEY = 21_000_000 * 100_000_000
log('I22 block 74,638: each output', big, 'sum stored in 64 bits', signed_total, 'old test (total <= max):', signed_total <= MAX_MONEY, 'new test (each in range):', 0 <= big <= MAX_MONEY)
assert signed_total == -997538 and (signed_total <= MAX_MONEY) and not (0 <= big <= MAX_MONEY)
add(key='mt1:i22:overflow-range-check', type='ChoiceFour', chapters=[6, 2], bloom=4, kind='synthesis',
    q=('In block 74,638 two outputs held 9,223,372,036,854,277,039 satoshis each. The old software checked only the total of the outputs, stored in a signed 64-bit number: it was not above '
       'the inputs or the allowed maximum, so the check passed. Which rule, shipped within hours, would have refused that block, and why?'),
    options=['Each output amount must lie between 0 and 2.1 quadrillion satoshis: a range check on every output stops a huge amount before any sum can wrap around to a negative number.',
             'The total of the outputs must not exceed the total of the inputs: the old software already checked that, and the wrapped total still passed it.',
             'Newly created coins must wait 100 blocks before they are spent: the 184 billion bitcoin could then not have moved.',
             'The txid must hash only the legacy serialization: the witness could then not hide the amounts.'],
    answer=0,
    source=src(6, "slide 40 'The 2010 overflow, in five lines' (40 of 71)"), sources=[src(6, "slide 41 'The block that created 184 billion bitcoins'"), src(2, "slide 32 'Two outputs that wrapped around'")],
    critical_points=['CP6.13', 'CP2.13'], seeds=['ch06/question_bank_v1_0_0.json#99'], no_seed_reason='',
    enhancements=['reverse the question', 'add a reasoning step', 'combine chapters'],
    terms=['block 74,638', 'range check', 'signed 64-bit', '2.1 quadrillion'], computed='wrapped sum -997,538 (program in the builder)')

# I23  malleability, tracked by txid: legacy against segwit (chapters 6 and 3)
add(key='mt1:i23:tracker-legacy-vs-segwit', type='ChoiceFour', chapters=[6, 3], bloom=4, kind='synthesis',
    q=('A payment tracker identifies each withdrawal by its txid. Before two withdrawals confirm, a stranger changes one of them: for a legacy payment the stranger re-encodes the '
       'signature inside the input script, and for a segwit payment the stranger changes only the signature bytes in the witness. Both payments stay valid. Which outcome is right?'),
    options=['The legacy payment gets a new txid, so the tracker may believe it failed; the segwit payment keeps its txid, because the witness lies outside the txid.',
             'Both payments keep their txid, because a signature is never part of any hash of the transaction.',
             'The legacy payment keeps its txid and the segwit payment gets a new one, because the txid covers the extended serialization.',
             'Both payments get a new txid, so the tracker must follow the wtxid of every payment.'],
    answer=0,
    source=src(6, "slide 49 'Segwit: change the witness, keep the txid' (49 of 71)"), sources=[src(6, "slide 50 'Mt. Gox blames malleability' (50 of 71): a stranger re-encodes an input script and changes the txid"), src(3, "slide 40 summary: the txid ignores the witness, and weight counts it")],
    critical_points=['CP6.14', 'CP6.04', 'CP3.09'], seeds=[], no_seed_reason='',
    enhancements=['change the situation', 'combine chapters', 'add a reasoning step'],
    terms=['txid', 'wtxid', 'witness', 'input script', 'extended serialization'])


# ===================================================================================================================== seeds (set from the seed search, see the comments in the data below)
# The seed links below are page items the author READ and used as the starting point (the stem of the page item is quoted in the seed table of the report).
SEEDS = {
    'mt1:i02:toy-chain-supply': ['ch01/quiz_v1_0_0.json#1', 'ch01/question_bank_v1_1_0.json#4', 'ch06/question_bank_v1_0_0.json#171'],
    'mt1:i03:vwap-third-trade': ['ch01/question_bank_v1_1_0.json#52', 'ch01/question_bank_v1_1_0.json#53'],
    'mt1:i04:fee-not-written': ['ch02/question_bank_v1_0_0.json#9', 'ch02/question_bank_v1_0_0.json#62', 'ch02/question_bank_v1_0_0.json#64'],
    'mt1:i05:change-after-fee-rate': ['ch02/question_bank_v1_0_0.json#13', 'ch02/question_bank_v1_0_0.json#83', 'ch02/question_bank_v1_0_0.json#54'],
    'mt1:i06:order-wallet-to-block': ['ch02/question_bank_v1_0_0.json#54', 'ch02/question_bank_v1_0_0.json#81'],
    'mt1:i07:shop-confirmations': ['ch02/quiz_v1_0_0.json#3', 'ch02/question_bank_v1_0_0.json#140', 'ch02/question_bank_v1_0_0.json#143'],
    'mt1:i08:utxo-set-trace': ['ch06/question_bank_v1_0_0.json#53', 'ch02/question_bank_v1_0_0.json#60'],
    'mt1:i09:conf-precedence-and-refusal': ['ch03/question_bank_v1_0_0.json#66', 'ch03/question_bank_v1_0_0.json#68', 'ch03/question_bank_v1_0_0.json#76', 'ch03/quiz_v1_0_0.json#1'],
    'mt1:i11:trace-release-tags': ['ch03/question_bank_v1_0_0.json#38', 'ch03/question_bank_v1_0_0.json#29'],
    'mt1:i12:rpcauth-and-p2pkh': ['ch03/question_bank_v1_0_0.json#130', 'ch03/question_bank_v1_0_0.json#131', 'ch04/question_bank_v1_0_0.json#79', 'ch04/question_bank_v1_0_0.json#92'],
    'mt1:i13:vanity-factor': ['ch04/quiz_v1_0_0.json#6', 'ch04/question_bank_v1_0_0.json#156'],
    'mt1:i14:wif-flag-and-balance': ['ch04/quiz_v1_0_0.json#2', 'ch04/question_bank_v1_0_0.json#46', 'ch04/question_bank_v1_0_0.json#61', 'ch05/question_bank_v1_0_0.json#113'],
    'mt1:i15:fill-hash-and-collision': ['ch04/question_bank_v1_0_0.json#79', 'ch04/question_bank_v1_0_0.json#42'],
    'mt1:i16:words-to-entropy': ['ch05/question_bank_v1_0_0.json#18', 'ch05/question_bank_v1_0_0.json#20', 'ch05/quiz_v1_0_0.json#1'],
    'mt1:i18:trace-gap-limit': ['ch05/question_bank_v1_0_0.json#161'],
    'mt1:i19:restore-passphrase-labels': ['ch05/question_bank_v1_0_0.json#31', 'ch05/question_bank_v1_0_0.json#142', 'ch05/question_bank_v1_0_0.json#113'],
    'mt1:i20:trace-compactsize': ['ch06/question_bank_v1_0_0.json#39'],
    'mt1:i21:trace-sequence-field': ['ch06/question_bank_v1_0_0.json#80', 'ch06/question_bank_v1_0_0.json#81', 'ch06/question_bank_v1_0_0.json#89'],
    'mt1:i22:overflow-range-check': ['ch06/question_bank_v1_0_0.json#99'],
    'mt1:i23:tracker-legacy-vs-segwit': ['ch06/question_bank_v1_0_0.json#117', 'ch06/question_bank_v1_0_0.json#125', 'ch03/question_bank_v1_0_0.json#167', 'ch03/question_bank_v1_0_0.json#168'],
}


def finish(outdir):
    for it in ITEMS:
        it['seeds'] = list(SEEDS.get(it['key'], it.get('seeds', [])))
        if it['seeds']:
            it['no_seed_reason'] = ''
        else:
            it.setdefault('no_seed_reason', '')
            if not it['no_seed_reason']:
                it['no_seed_reason'] = 'none: written from the source of the point'
        it.setdefault('computed', '')
    doc = {'note': 'SEN0401 midterm authored items, version %s, builder sen0401_exam_items_midterm_build_v1_0_0.py. Format of the exam engine v1.1.0 plus the fields sources, enhancements and computed. '
                   'Authored for the MIDTERM only (papers: midterm).' % VERSION,
           'version': VERSION, 'chapters': [1, 2, 3, 4, 5, 6], 'items': ITEMS}
    json.dump(doc, open(os.path.join(outdir, 'sen0401_exam_items_midterm_v%s.json' % VERSION.replace('.', '_')), 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    open(os.path.join(outdir, 'sen0401_exam_items_midterm_computed_v%s.txt' % VERSION.replace('.', '_')), 'w', encoding='utf8').write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    out = HERE
    if '--outdir' in sys.argv: out = sys.argv[sys.argv.index('--outdir') + 1]
    os.makedirs(out, exist_ok=True)
    finish(out)
    print('wrote', len(ITEMS), 'items to', out)
