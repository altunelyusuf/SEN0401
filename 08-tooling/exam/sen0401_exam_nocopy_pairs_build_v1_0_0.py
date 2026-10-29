"""Builds the fixture of known answer for the copy test (EN11 and the similarity method), version 1.0.0. New file.
Writes sen0401_exam_nocopy_pairs_v1_0_0.json: candidate paper items, each paired with the page-visible item it is a copy of, a near copy of, or genuinely different from, and the
EXPECTED ANSWER of each pair (REFUSE or PASS), written here from the intent of the construction BEFORE the first run of the method on these pairs.
Classes (per base item, 8 base items chosen from chapters 1 to 6, the candidates written by hand or by a stated rule):
  copy                         the page item as it is                                                 expected REFUSE (stem exact and options exact)
  options_reversed             the same stem, the four options in the opposite order                  expected REFUSE (stem exact, options exact: order does not matter)
  near_word_isolated           one interior word of the stem changed to 'other', options replaced      expected REFUSE (STEM_NEAR: stems of 10 words or more)
  stem_same_options_new        the same stem, four new options                                        expected REFUSE (stem exact)
  stem_rewritten_options_same  a hand-reworded stem, the four original options                        expected REFUSE (options exact)
  one_option_replaced          a hand-reworded stem, three original options and one new one            expected REFUSE (OPTIONS_NEAR)
  different_same_concept       hand-written new question on the same concept, new options             expected PASS
  paraphrase                   hand-written paraphrase of the same idea (new words, new options)      expected PASS  - a DECLARED BLIND SPOT of the method: a person would call it a copy of the idea
Special pairs (guards and item types): see 'special'. The sweeps over the whole page-visible set are defined in 'sweeps' (the rule of expectation is written here, the candidates are made by the check).
A candidate that is meant to be different shares no sentence with the base; all terms come from the course corpus. Synthetic stand-ins only: no student data."""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_similarity_v1_0_0 as S
pages = S.page_items(); byq = {}
import glob
RAW = {}
for pg in pages:
    f = os.path.join(os.path.dirname(os.path.dirname(HERE)), pg['file']); RAW.setdefault(f, json.load(open(f, encoding='utf8')))
def raw(pg):
    f = os.path.join(os.path.dirname(os.path.dirname(HERE)), pg['file']); d = RAW[f]
    return d[pg['index']] if pg['source'] == 'bank' else d['items'][pg['index']]
for pg in pages: byq.setdefault(raw(pg)['q'], []).append(pg)
def find(q):
    c = byq[q]; assert len(c) == 1 or q.startswith('What is a protocol'), (q, len(c)); return c[0]

H = lambda q, o, a: dict(q=q, options=o, answer=a)
BASES = [
 ("A merchant gives an auditor the account's extended public key. What has the auditor gained?",
  H("An auditor receives an account's extended public key from a merchant. What can the auditor now do?", None, None),
  H("A shop keeps the extended public key of its account on the web server to hand out a new receiving address to every customer. What is the main risk if the server is stolen?",
    ["The thief can spend all the funds of the account", "The thief can see all addresses and payments of the account but cannot spend", "The thief can change the seed of the wallet", "The thief can reverse the payments already confirmed"], 1),
  H("An accountant is handed the xpub of a company wallet account. What does the accountant receive?",
    ["The right to move the money of the company", "The ability to follow every incoming and outgoing payment of the account without spending", "Only the list of change addresses", "Nothing useful, because a public key reveals no information"], 1)),
 ("Why did BIP 113 make the median time the time that time locks use?",
  H("For time locks, BIP 113 uses the median time past. What is the reason for that choice?", None, None),
  H("A transaction has a time lock set to a given timestamp. According to BIP 113, which value is compared with that lock time?",
    ["The timestamp of the newest block alone", "The median of the timestamps of the previous eleven blocks", "The clock time of the node that validates", "The average of all block timestamps of the same day"], 1),
  H("What weakness of block timestamps does the use of the median of the last eleven blocks for time locks remove?",
    ["A single miner could choose a false timestamp to decide which transactions are final", "Block timestamps are not stored in the chain", "Timestamps are encrypted by the miner", "The median is faster to compute than the average"], 0)),
 ("Which two properties of a hash function do transaction identifiers rely on?",
  H("Transaction identifiers are hashes. Name the two properties of hashing that they depend on.", None, None),
  H("Two transactions differ only in one output amount. How do their transaction identifiers compare?",
    ["They differ in a single hexadecimal digit", "They look completely unrelated", "They share the first half of their digits", "They are equal, because the identifier ignores the amounts"], 1),
  H("Which features make the hash of a transaction a reliable fingerprint of it?",
    ["A constant output size and a large unpredictable change for a small change of input", "Being invertible and cheap to compute", "A secret key shared among the nodes", "Compression of the transaction into a short code that can be decoded"], 0)),
 ("What is the only difference between the bech32 and the bech32m algorithm?",
  H("Bech32 and bech32m are two encodings. What single thing separates them?", None, None),
  H("Which witness versions of a segwit address use the bech32m encoding?", ["Version 0 only", "Version 1 and later", "Only version 16", "All versions use bech32"], 1),
  H("Bech32m changes one thing relative to bech32. What is it?", ["The number that is mixed into the checksum calculation", "The number of characters in the alphabet", "The number of checksum characters", "The prefix that names the network"], 0)),
 ("Why is there no such thing as the memory pool of the network?",
  H("There is no single memory pool of the network. What is the reason?", None, None),
  H("A low-fee transaction is in the mempool of one node but absent from the mempool of another node. What is the most likely reason?",
    ["The second node has a higher minimum relay fee or a full memory limit", "The transaction is invalid and was rejected by the first node", "The second node has no connection to the Internet", "The transaction was already mined into a block"], 0),
  H("The list of unconfirmed transactions waiting for a block is not a single shared list. Why not?",
    ["Every node maintains its own list and the lists differ between nodes", "Miners delete the list every ten minutes", "Only wallets keep such a list", "The list is stored by explorers only"], 0)),
 ("Why does the chapter call the bitcoin currency deflationary over the long term?",
  H("According to the chapter, why is the bitcoin currency deflationary in the long run?", None, None),
  H("A holder expects the purchasing power of bitcoin to grow over decades. Which rule of the currency supports that expectation?",
    ["The block subsidy halves about every four years, so new supply keeps shrinking", "Fees are burned in every block", "Miners vote on the supply each year", "Wallets destroy a part of every payment"], 0),
  H("In what sense does the chapter describe Bitcoin as deflationary as the years pass?",
    ["New coins arrive ever more slowly and in the end stop arriving", "Existing coins are destroyed at each halving", "Prices must fall because more coins are mined", "Every fee is removed from circulation"], 0)),
 ("Why can pasting a transaction identifier from one tool into another find nothing?",
  H("Why may a transaction identifier that is pasted from one tool into another turn up no result?", None, None),
  H("A developer hashes a serialized transaction twice with SHA-256 and gets a value that differs from the identifier an explorer shows. Which step is probably missing?",
    ["Reversing the byte order of the hash for display", "Hashing a third time", "Encoding the value in base58", "Removing the first byte of the hash"], 0),
  H("Why might an identifier copied out of one program be rejected by another program's search?",
    ["The same hash is printed with its bytes in the opposite order in the two programs", "Identifiers expire after a day", "Explorers index by address only", "The identifier is regenerated at each relay"], 0)),
 ("What is the other name for a lightweight client, and what does it describe?",
  H("A lightweight client has another name. What is it, and what does it describe?", None, None),
  H("A phone wallet asks a server for block headers and for proofs of its own transactions only. What does it trust the server for?",
    ["For the data that it does not check itself, such as which transactions exist in the chain", "For the signing of its transactions", "For the private keys of the wallet", "For the proof of work of the headers"], 0),
  H("Which other term describes a client that validates only partly and relies on others for data?",
    ["Simplified-payment-verification client", "Archival full node", "Mining pool operator", "Custodial exchange"], 0)),
]
pairs = []
def add(pid, cls, cand, ref, expect, kinds=None, note=''):
    pairs.append(dict(id=pid, cls=cls, candidate=cand, page_ref=ref, expected=dict(answer=expect, kinds_include=kinds or []), note=note))
def middle_word_changed(q):
    t = q.split(' '); m = len(t) // 2
    for d in range(len(t)):
        for j in (m + d, m - d):
            if 0 < j < len(t) - 1 and t[j].isalpha() and t[j].lower() != 'other': t[j] = 'other'; return ' '.join(t)
    raise ValueError(q)
for k, (q, reworded, different, para) in enumerate(BASES, 1):
    pg = find(q); r = raw(pg); ref = pg['ref']; opts = list(r['options']); ch = lambda qq, oo, a=0: dict(type='ChoiceFour', q=qq, options=oo, answer=a)
    add('B%d-copy' % k, 'copy', ch(r['q'], opts, r['answer']), ref, 'REFUSE', ['STEM_EXACT', 'OPTIONS_EXACT'])
    add('B%d-options_reversed' % k, 'options_reversed', ch(r['q'], opts[::-1]), ref, 'REFUSE', ['STEM_EXACT', 'OPTIONS_EXACT'])
    add('B%d-near_word_isolated' % k, 'near_word_isolated', ch(middle_word_changed(r['q']), ['FIXTURE option one', 'FIXTURE option two', 'FIXTURE option three', 'FIXTURE option four']), ref, 'REFUSE', ['STEM_NEAR'])
    add('B%d-stem_same_options_new' % k, 'stem_same_options_new', ch(r['q'], ['FIXTURE option one', 'FIXTURE option two', 'FIXTURE option three', 'FIXTURE option four']), ref, 'REFUSE', ['STEM_EXACT'])
    add('B%d-stem_rewritten_options_same' % k, 'stem_rewritten_options_same', ch(reworded['q'], opts[1:] + opts[:1]), ref, 'REFUSE', ['OPTIONS_EXACT'])
    add('B%d-one_option_replaced' % k, 'one_option_replaced', ch(reworded['q'], opts[:3] + ['FIXTURE replaced distractor']), ref, 'REFUSE', ['OPTIONS_NEAR'])
    add('B%d-different_same_concept' % k, 'different_same_concept', ch(different['q'], different['options'], different['answer']), ref, 'PASS', note='a new question on the same concept')
    add('B%d-paraphrase' % k, 'paraphrase', ch(para['q'], para['options'], para['answer']), ref, 'PASS', note='DECLARED BLIND SPOT: the same idea in other words is not seen by a lexical method')
special = []
def sp(pid, cls, cand, ref, expect, kinds=None, note=''):
    special.append(dict(id=pid, cls=cls, candidate=cand, page_ref=ref, expected=dict(answer=expect, kinds_include=kinds or []), note=note))
# short stems: exact test only
p1 = find('What is a protocol?') if False else byq['What is a protocol?'][0]; r1 = raw(p1)
sp('S1-short_stem_copy', 'short_stem', dict(type='ChoiceFour', q='What is a protocol?', options=['FIXTURE option one', 'FIXTURE option two', 'FIXTURE option three', 'FIXTURE option four'], answer=0), p1['ref'], 'REFUSE', ['STEM_EXACT'])
sp('S2-short_stem_word_changed', 'short_stem', dict(type='ChoiceFour', q='What is a standard?', options=['FIXTURE option one', 'FIXTURE option two', 'FIXTURE option three', 'FIXTURE option four'], answer=0), p1['ref'], 'PASS',
   note='DECLARED BLIND SPOT: a stem under 10 words is judged by the exact test only (a short stem with a word changed asks something else as often as not)')
# trivial options (truth values) must not make a copy of a different question
tt = [p for p in pages if p['p']['opts'] == {'falsetrue', 'truetrue', 'falsefalse', 'truefalse'}][0]
sp('S3-truth_table_options', 'guard', dict(type='ChoiceFour', q='FIXTURE which pair of truth values does the fixture condition give', options=['True True', 'True False', 'False True', 'False False'], answer=0), tt['ref'], 'PASS',
   note='the four options are only truth values: not distinctive, so a coincidence is not a copy')
# quiz items (three options)
qz = find('What problem does proof of work solve without a central clearinghouse?'); rq = raw(qz)
sp('S4-quiz_copy', 'quiz', dict(type='ChoiceFour', q=rq['q'], options=rq['options'] + ['FIXTURE a fourth option'], answer=0), qz['ref'], 'REFUSE', ['STEM_EXACT'])
sp('S5-quiz_options_only', 'quiz', dict(type='ChoiceFour', q='FIXTURE a stem that shares nothing with the quiz stem', options=rq['options'] + ['FIXTURE a fourth option'], answer=0), qz['ref'], 'REFUSE', ['OPTIONS_NEAR'],
   note='three of the four options are the three options of a page quiz item')
# code items: the generic stem alone is not the item
cp = [p for p in pages if p['p']['stem'].startswith('What does this program print?') and p['ref'].startswith('ch01/question_bank_v1_1_0.json#5')][0]; rc = raw(cp)
sp('S6-code_copy', 'code', dict(type='ChoiceFourCode', q=rc['q'].split('\n')[0], code=rc.get('code') or rc['q'].split('\n', 1)[1], options=['FIXTURE option one', 'FIXTURE option two', 'FIXTURE option three', 'FIXTURE option four'], answer=0), cp['ref'], 'REFUSE', ['STEM_EXACT'])
sp('S7-code_other_program', 'code', dict(type='ChoiceFourCode', q='What does this program print?', code="FIXTURE_values = [3, 1, 2]\nFIXTURE_values.sort()\nprint(FIXTURE_values[-1] * 7)", options=['FIXTURE option one', 'FIXTURE option two', 'FIXTURE option three', 'FIXTURE option four'], answer=0), cp['ref'], 'PASS',
   note='the same generic stem but another program: not a copy')
# other item types: components are compared too
mq = find("A merchant gives an auditor the account's extended public key. What has the auditor gained?"); rmq = raw(mq)
sp('S8-matching_premise_copy', 'matching', dict(type='Matching', premises=[dict(text=rmq['q'], match='FIXTURE response A'), dict(text='FIXTURE premise two', match='FIXTURE response B'), dict(text='FIXTURE premise three', match='FIXTURE response C')],
                                              responses=['FIXTURE response %s' % x for x in 'ABCDE']), mq['ref'], 'REFUSE', ['STEM_EXACT'], 'a premise that is a page question')
sp('S9-matching_responses_are_page_options', 'matching', dict(type='Matching', premises=[dict(text='FIXTURE premise %d' % k, match=rmq['options'][k]) for k in range(3)], responses=rmq['options'] + ['FIXTURE spare response']), mq['ref'], 'REFUSE', ['OPTIONS_NEAR'],
   'the response list holds the four options of a page item')
sp('S10-fill_blank_sentence_copy', 'fill', dict(type='FillBlankGroup', blanks=[dict(text=rmq['q'], answer='FIXTURE alpha'), dict(text='FIXTURE sentence two ____.', answer='FIXTURE beta'), dict(text='FIXTURE sentence three ____.', answer='FIXTURE gamma')],
                                            distractors=['FIXTURE delta', 'FIXTURE epsilon']), mq['ref'], 'REFUSE', ['STEM_EXACT'], 'a blank sentence that is a page question')
sp('S11-ordering_steps_are_page_options', 'ordering', dict(type='Ordering', steps=rmq['options'][:4]), mq['ref'], 'REFUSE', ['OPTIONS_EXACT'], 'the steps are the four options of a page item')
sp('S12-matching_all_different', 'matching', dict(type='Matching', premises=[dict(text='FIXTURE premise %d about a topic of its own' % k, match='FIXTURE response %s' % 'ABC'[k]) for k in range(3)], responses=['FIXTURE response %s' % x for x in 'ABCDE']), mq['ref'], 'PASS')
sp('S13-number_item_stem_copy', 'number', dict(type='NumericAnswer', q=rmq['q'], key_value=1, unit='FIXTURE', tolerance=0), mq['ref'], 'REFUSE', ['STEM_EXACT'])
sp('S14-trace_item_different', 'trace', dict(type='CodeTrace', q='FIXTURE what does this listing print', code='print(len("FIXTURE"))', output='7'), mq['ref'], 'PASS')
sweeps = [
 dict(id='W1-copy_of_every_page_item', rule='every one of the page-visible items, as a candidate, is refused and the match names the item it was copied from', expected='REFUSE for all'),
 dict(id='W2-stem_rewritten_options_kept', rule="every page-visible item with at least 3 distinctive options, with its stem replaced by an unrelated fixture stem and its options kept, is refused (OPTIONS_EXACT or OPTIONS_NEAR); with fewer than 3 distinctive options it passes", expected='REFUSE iff the item has >= 3 distinctive options'),
 dict(id='W3-one_word_changed', rule="every page-visible bank item without a code listing whose question has 10 words or more and whose middle word is a plain word: that word changed to 'other', options replaced by fixture options, is refused (STEM_NEAR)", expected='REFUSE for all'),
]
json.dump(dict(note='Fixture of known answer for EN11 and the similarity method. The expected answer of every pair is written by sen0401_exam_nocopy_pairs_build_v1_0_0.py from the intent of its construction, before the first run.',
               method_version=S.VERSION, thresholds=S.thresholds(), pairs=pairs, special=special, sweeps=sweeps), open(os.path.join(HERE, 'sen0401_exam_nocopy_pairs_v1_0_0.json'), 'w', encoding='utf8'), indent=1, ensure_ascii=False)
print('pairs', len(pairs), 'special', len(special), 'sweeps', len(sweeps))
