"""Every computation the SEN0401 chapter 11 (The Blockchain) lecture deck shows. The outputs come from executing these statements, never from typing them:
sen0401_deck_examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE loads the chapter's own library (sen0401_ch11_lib_v1_0_0.py: an independent block-header, merkle-tree and chain-parameter code, and readers of the saved sources) and the saved
records it reads: R is the single run of Bitcoin Core 31.1 on regtest (ch11-evidence/regtest_run; one run, so its values are Recorded on the slides); the real blocks and heights are
public figures from mempool.space, saved in ch11-evidence on 2026-10-15 (tip(k) reads a saved height, age(y, m, d) counts days to that date); L.chainparams_genesis reads the constants of chainparams.cpp. Rows that read R only read the record; rows that call
L.merkle_root, L.merkle_path, L.tamper_chain, L.catchup, L.signet_magic and so on compute. The statements are the research package's executed claims (sen0401_ch11_leaves_v1_0_0.py), cut into
one-line rows. Every group is named after the slide that shows it. deck_check re-runs every '>>>' line of the finished deck in this same namespace, so a statement is ONE line."""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))

PRELUDE = """
import sys, hashlib, datetime
sys.path.insert(0, %r)
import sen0401_ch11_lib_v1_0_0 as L
R = L.run()
src, seen = L.const, L.has
tip = lambda k: int(L.raw('mempool_' + (k + '_' if k else '') + 'tip_height.txt'))
age = lambda y, m, d: (datetime.date(2026, 10, 15) - datetime.date(y, m, d)).days
""" % TOOLING

EX = {
 # ---- part A: the block and the chain ------------------------------------------------------------------------------------
 "Container": [
  "g, s = L.chainparams_genesis('main'), {n: R['b4_blocks'][str(n)]['size'] for n in (1, 2, 3, 4)}",
  "80 + 1 + g['tx_bytes'], R['b1_genesis']['block']['size'], g['tx_bytes'], s",
  "R['b3_blk_size_field'], R['b3_blk_first_bytes'][:8], R['b3_blk_first_bytes_raw'] != R['b3_blk_first_bytes']",
  "R['b3_xor_key'], R['b3_blk_size_field'] + 8 == R['b1_info0']['size_on_disk'], R['b3_blk_genesis_equals']",
  "[len(L.compact_size(n)) for n in (252, 253, 65535, 65536)], 4000000 // (4 * 60)",
 ],
 "Header": [
  "t = L.raw('mempool_header_277315.txt'); h = L.header(t); v = L.jload('mempool_block_840000.json')['version']",
  "len(bytes.fromhex(t)), 4000000 // 80, h['version'], h['time'], h['nonce'], h['bits']",
  "h['version'].to_bytes(4, 'little').hex(), h['prev'][-8:], bytes.fromhex(h['prev'])[::-1][:4].hex()",
  "hex(v), v >> 29, hex(v & 0x1fffe000), R['b3_block']['json']['versionHex']",
  "L.header(L.raw('mempool_header_0.txt'))['version'], h['version'], seen('bip-0009.mediawiki', 'The top 3 bits of such blocks must be 001')",
 ],
 "TimeTarget": [
  "d, t = L.jload('mempool_block_277315.json'), R['b3_timestamps_110_121']",
  "L.iso(1231006505), L.iso(2 ** 32 - 1), 2 * 60 * 60, seen('core_src_chain.h', 'MAX_FUTURE_BLOCK_TIME = 2 * 60 * 60')",
  "L.median_time_past(t), R['b3_mediantime_121'], d['mediantime'], d['timestamp'] - d['mediantime']",
  "hex(L.bits_to_target('1d00ffff')), L.difficulty('1903a30c'), d['difficulty']",
  "hex(L.work('1d00ffff')), 2 ** 32, d['nonce'], round(L.work('1903a30c') / 2 ** 32)",
 ],
 "Genesis": [
  "L.chainparams_genesis('main')['hash'][:16], L.chainparams_genesis('main')['time']",
  "L.chainparams_genesis('main')['message']",
  "R['b1_genesis']['coinbase_getrawtransaction']['error'][:44]",
 ],
 "Identity": [
  "b, g, hs = bytes.fromhex(L.raw('mempool_header_0.txt')), R['b1_genesis'], R['b3_headers_480_489']",
  "hashlib.sha256(hashlib.sha256(b).digest()).digest()[::-1].hex()[:16], hashlib.sha256(b).digest()[::-1].hex()[:16]",
  "g['hash'] in g['block_hex'], L.rev(g['hash']) in g['block_hex'], len(g['block_hex']) // 2",
  "L.rev(L.header(hs[0])['hash']) in hs[1], L.header(hs[1])['prev'] == L.header(hs[0])['hash']",
  "zero = lambda n: L.leading_zero_hex(L.header(L.raw('mempool_header_%s.txt' % n))['hash'])",
  "[zero(n) for n in ('0', '277315')], L.leading_zero_hex(L.jload('mempool_block_840000.json')['id'])",
 ],
 "Height": [
  "c, m, k = R['b3_bip34'], R['b7_maturity'], 'core_src_consensus_consensus.h'",
  "tip(''), round(tip('') * 600 / 86400 / 365.25, 1), R['b1_info0']['blocks']",
  "{h: L.bip34_height(v) for h, v in c.items()} == {h: int(h) for h in c}, c['1'], c['17'], c['128'], c['256']",
  "src(k, 'COINBASE_MATURITY'), m['confirmations_99']['allowed'], m['confirmations_100']['allowed']",
  "m['confirmations_99']['reject-details']",
 ],
 "Links": [
  "hs = R['b3_headers_480_489']; p = [L.header(h) for h in hs]; w = R['b3_chainwork']",
  "[p[i]['prev'] == p[i - 1]['hash'] for i in range(1, 10)].count(True), len(p), p[0]['prev'][:8], p[9]['hash'][:8]",
  "L.tamper_chain(hs, 3), p[3]['hash'][:8]",
  "[int(w[str(i)], 16) for i in range(4)], L.work('207fffff'), int(R['b2_info']['chainwork'], 16), 2 * 501",
 ],
 "Forks": [
  "f = R['b6_fork']",
  "f['height1'], f['height2'], f['child1'] != f['child2'], f['prev1'] == f['prev2'] == f['parent']",
  "[(t['height'], t['branchlen'], t['status']) for t in f['tips']]",
  "[(t['height'], t['branchlen'], t['status']) for t in f['tips_after']], f['active_is'] == f['extension']",
  "[round(L.catchup(0.1, z), 7) for z in (0, 1, 2, 6)], round(L.catchup(0.3, 6), 4)",
 ],
 # ---- part B: merkle trees ----------------------------------------------------------------------------------------------
 "Tree": [
  "b = R['b4_blocks']['4']; i = [bytes.fromhex(t)[::-1] for t in b['txids']]; h = L.sha256d",
  "[len(l) for l in L.merkle_levels(b['txids'])], h(h(i[0] + i[1]) + h(i[2] + i[3]))[::-1].hex() == b['merkleroot']",
  "o = R['b4_blocks']['3']",
  "[len(l) for l in L.merkle_levels(o['txids'])], L.merkle_root(o['txids']) == o['merkleroot']",
  "L.merkle_root(o['txids'] + o['txids'][-1:]) == o['merkleroot']",
 ],
 "Proof": [
  "b = R['b4_blocks']['16']; ids = b['txids']; p = L.merkle_path(ids, 10)",
  "len(p), 32 * len(p), [r for s, r in p], L.follow_path(ids[10], p) == b['merkleroot']",
  "L.follow_path(ids[10], p, swap=True) == b['merkleroot'], [int(c) for c in bin(10)[2:].zfill(4)][::-1]",
  "[(n, L.depth(n), 32 * L.depth(n)) for n in (1024, 4096, 16000)]",
  "round(4000000 / (80 + 448)), round(4000000 / (250 + 80 + 448)), 4000000 // 10000",
 ],
 "Flaws": [
  "ids = [L.sha256d(bytes([i])).hex() for i in range(1, 7)]; b = ids + [ids[4], ids[5]]",
  "L.merkle_root(ids) == L.merkle_root(b), len(ids), len(b)",
  "m, k = R['b5_mutation'], R['b4_blocks']['4']['txids']",
  "m['n_original'], m['n_mutated'], m['same_header'], m['submit_mutated'], m['submit_original'], m['tip_is_original']",
  "len(bytes.fromhex(k[0]) + bytes.fromhex(k[1])), 240 // 4, seen('bip-0054.md', 'exactly 64 bytes are invalid')",
 ],
 "MerkleStory": [
  "seen('wikipedia_merkle_tree.html', 'patent 4309569')",
  "ids = L.jload('mempool_txids_277315.json')",
  "L.merkle_root(ids) == L.header(L.raw('mempool_header_277315.txt'))['merkle'], len(ids)",
 ],
 # ---- part C: test blockchains --------------------------------------------------------------------------------------------
 "Chains": [
  "c, n = R['b9_chains'], ('main', 'test', 'testnet4', 'signet', 'regtest')",
  "[L.chain_facts(k)['port'] for k in n], [L.chain_facts(k)['assumed_gb'] for k in n]",
  "f = lambda a: (a['legacy'][0], a['p2sh-segwit'][0], a['bech32'][:a['bech32'].index('1') + 2])",
  "f(R['b8_regtest_addresses']), f(c['testnet4']['addresses']), f(c['signet']['addresses'])",
  "[(k, L.chain_facts(k)['halving']) for k in ('main', 'regtest')], R['b2_balance'], R['b1_datadir']",
 ],
 "Testnet": [
  "n, d = tip('testnet3'), age(2011, 2, 2)",
  "n, d * 144, round(n / (d * 144), 1), tip('testnet4')",
  "{k: L.chain_facts(k)['min_diff'] for k in ('main', 'test', 'testnet4', 'signet', 'regtest')}",
  "seen('bitcoind_help_31.1.txt', 'Support for testnet3 is deprecated'), L.chainparams_genesis('testnet4')['hash'][:16]",
 ],
 "GriefStory": [
  "seen('bip-0094.mediawiki', 'worth of blocks were mined in a few weeks')",
  "t3, t4 = tip('testnet3'), tip('testnet4')",
  "t3, t4, round(t3 / t4)",
  "seen('core_relnotes_28.0.md', 'Support for Testnet4 as specified in')",
 ],
 "Signet": [
  "c = R['b9_chains']; ch = c['signet']['info']['signet_challenge']",
  "L.script_ops(ch), len(ch) // 2, L.script_ops(c['custom_signet']['info']['signet_challenge'])",
  "L.signet_magic(ch), L.signet_magic('51')",
  "c['signet']['genesis_hash'] == c['custom_signet']['genesis_hash'], c['signet']['genesis_hash'][:12], c['signet']['info']['bits']",
  "tip('signet'), round(tip('signet') / 143619, 2)",
 ],
 "SignetStory": [
  "seen('bip-0325.mediawiki', 'challenge')",
  "L.signet_magic(R['b9_chains']['signet']['info']['signet_challenge'])",
  "round(tip('signet') / 143619, 2)",
 ],
}
