"""Every computation the SEN0401 chapter 10 (The Bitcoin Network) lecture deck shows. The outputs come from executing these statements, never from typing them:
sen0401_deck_examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE loads the chapter's own library (sen0401_ch10_lib_v1_0_0.py: readers of the saved sources, the Bitnodes snapshot, the filter and Bloom code; sen0401_ch10_p2p_v1_0_0.py: the wire
format written independently of Bitcoin Core) and the saved records it reads: R is the run of Bitcoin Core 31.1 on regtest (ch10-evidence/regtest_run; one run, so its values are Recorded on the
slides), b is the Bitnodes snapshot of 2026-10-15. Rows that read R only read the record; rows that call P.frame, L.gcs_book_example, L.rice_roundtrip and so on compute. The statements are the
research package's executed claims (sen0401_ch10_leaves_v1_0_0.py), cut into one-line rows. Every group is named after the slide that shows it. deck_check re-runs every '>>>' line of the
finished deck in this same namespace, so a statement is ONE line."""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))

PRELUDE = """
import sys, json
sys.path.insert(0, %r)
import sen0401_ch10_lib_v1_0_0 as L
import sen0401_ch10_p2p_v1_0_0 as P
R = L.run(); b = L.bitnodes()
src, seen = L.const, L.has
""" % TOOLING

EX = {
 # ---- part A: who is on the network --------------------------------------------------------------------------------------
 "Census": [
  "b['total'], sorted(b['nets'].items())",
  "b['nets']['ipv4'] + b['nets']['ipv6'], seen('book_ch10_network.adoc', 'about 10,000', 'listening nodes')",
  "b['satoshi_prefix'], b['knots'], round(100 * b['core_plain'] / b['total'], 2), b['top_agent']",
  "sorted(b['services'].items())",
 ],
 "Handshake": [
  "e, v = R['e1_handshake'], R['e1_handshake']['node_version']",
  "P.frame('verack', b'').hex(), len(P.frame('verack', b'')), P.MAGIC['main'].hex(), e['magic']",
  "v['version'], v['services'], v['user_agent'], v['start_height'], v['relay'], v['payload_bytes']",
  "[c for t, c, n in e['sequence']]",
  "src('core_src_node_protocol_version.h', 'PROTOCOL_VERSION'), seen('book_ch10_network.adoc', '(e.g., 70002)')",
  "R['networkinfo_A']['localservicesnames'], R['e10_pruned']['services'], R['e10_pruned']['prune_info']['pruned']",
 ],
 # ---- part B: peers, blocks, transactions --------------------------------------------------------------------------------
 "Discovery": [
  "d, a = R['e11_dns_seeds'], R['e9_addr']; n = [len(v['ipv4']) for v in d['answers'].values()]",
  "len(d['seeds_in_chainparams']), d['distinct_ipv4'], min(n), max(n)",
  "src('core_src_kernel_chainparams.cpp', 'nDefaultPort'), d['tcp_probe']['connected']",
  "a['without']['addr']['count'], a['with_sendaddrv2']['addrv2']['count'], src('core_src_net_processing.cpp', 'MAX_PCT_ADDR_TO_SEND')",
  "a['with_sendaddrv2']['addrv2']['networks'], a['with_sendaddrv2']['addrv2']['addr_len']",
  "R['e9_addrman']['addrman_info']['ok']['all_networks']['total'], seen('bip-0155.mediawiki', 'TORV3', 'I2P', 'CJDNS')",
 ],
 "ConnTypes": [
  "t, n = R['e8_types'], 'core_src_net.h'",
  "t",
  "src(n, 'MAX_OUTBOUND_FULL_RELAY_CONNECTIONS'), src(n, 'MAX_BLOCK_RELAY_ONLY_CONNECTIONS'), src(n, 'DEFAULT_MAX_PEER_CONNECTIONS')",
  "i = R['e5_relay']['invs']",
  "len(i['normal_wtxidrelay']), len(i['relay_false']), len(i['feefilter_5sat'])",
 ],
 "Eclipse": [
  "src('core_src_net.h', 'MAX_BLOCK_RELAY_ONLY_CONNECTIONS')",
  "seen('heilman_2015_eclipse.pdf', 'Eclipse Attacks on Bitcoin’s Peer-to-Peer')",
  "seen('apostolaki_2017_hijacking.pdf', 'isolate ∼50% of the mining power')",
 ],
 "Compact": [
  "c = R['e3_compact']",
  "c['short_id_count'], c['tx_count'] - 1, c['short_ids_match'], c['short_id_bytes'], src('core_src_blockencodings.h', 'SHORTTXIDS_LENGTH')",
  "c['prefilled_indexes'], c['prefilled_txids'] == [c['coinbase_txid']], len(c['blocktxn_txids']), c['blocktxn_txids'] == c['expected_txids']",
  "c['cmpctblock_bytes'], c['full_block_bytes'], round(c['cmpctblock_bytes'] / c['full_block_bytes'], 4)",
 ],
 "CompactStory": [
  "seen('book_ch10_network.adoc', 'In 2015, a new version of Bitcoin Core added')",
  "seen('core_doc_bips.md', 'are used as of **v0.13.0**')",
  "parts = [b'compac', b't bloc', b'k mess', b'age!!!']; par = L.parity_code(parts)",
  "b''.join(L.rebuild([parts[0], None, parts[2], parts[3]], par))",
 ],
 "Headers": [
  "h, i, p, c = R['e2_headers'], R['e10_ibd'], 'core_src_net_processing.h', 'core_src_net_processing.cpp'",
  "h['first_count'], h['second_count'], h['height'], src(p, 'MAX_HEADERS_RESULTS')",
  "h['first_bytes'] == 3 + 2000 * 81, h['header_size'], h['chain_links_ok']",
  "R['e2_announce']",
  "src(c, 'BLOCK_DOWNLOAD_WINDOW'), src(c, 'MAX_BLOCKS_IN_TRANSIT_PER_PEER'), i['height'], i['chain_equal']",
 ],
 "Relay": [
  "r, m, o = R['e5_relay'], R['e10_mempool_vs_utxo'], R['e4_orphan']; k, u = r['invs'], m['before_block']",
  "[i[1] for i in k['normal_wtxidrelay']], seen('bip-0339.mediawiki', 'MSG_WTX (0x00000005)')",
  "round(r['feerate_low'], 1), round(r['feerate_high'], 1), r['peer_feefilter_sat_per_kvb'], len(k['feefilter_5sat'])",
  "u['F_mempool'], u['G_mempool'], m['utxo_hash_F'] == m['utxo_hash_G'], m['utxo_count_F']",
  "o['child_in_mempool_after_child'], hex(o['node_asked_for_parent'][0][0]), o['parent_in_mempool_after'], o['child_in_mempool_after']",
  "seen('bitcoind_help_31.1.txt', 'transaction reconciliations per BIP 330 (default: 0)')",
 ],
 # ---- part C: light clients, privacy, transport --------------------------------------------------------------------------
 "Spv": [
  "s, c = R['e6_spv'], L.chain_size_ratio()",
  "c['tip_height'], c['headers_mb'], c['chain_mb'], c['ratio']",
  "s['path_len'], s['root_from_path'] == s['header_root'], s['block_tx_count'], s['proof_bytes'], R['e6_bloom_enabled']['full_block_bytes']",
  '[round(L.double_spend_probability(q, 6), 7) for q in (0.1, 0.3)]',
 ],
 "Bloom": [
  "r, e = L.toy_bloom_experiment(), R['e6_bloom_enabled']",
  "r['inserted_ok'], r['bits_set'], r['fp_measured'], r['fp_formula'], r['maybe_exists'], r['nope_exists']",
  "L.bloom_bip37_vector(), src('core_src_common_bloom.h', 'MAX_BLOOM_FILTER_SIZE'), src('core_src_common_bloom.h', 'MAX_HASH_FUNCS')",
  "len(e['matched_txids']), e['merkleblock_bytes'], e['full_block_bytes'], e['block_txs'], e['filter_bytes'], e['hash_functions']",
  "R['e6_bloom_default']['has_bloom_bit'], R['e6_bloom_default']['disconnected_after_filterload'], b['services']['BLOOM']",
 ],
 "BloomStory": [
  "seen('gervais_2014_bloom_privacy.txt', 'leaks considerable information ab')",
  "(d := R['e6_bloom_default'])['has_bloom_bit'], d['disconnected_after_filterload']",
  "b['services']['BLOOM'], b['total']",
 ],
 "Filters": [
  "g, r, f = L.gcs_book_example(), L.rice_roundtrip([379, 476, 653, 849, 900], 7), R['e7_filter']",
  "g['sorted'], g['deltas'], g['equal'], g['max_bits_original'], g['max_bits_deltas']",
  "r['decoded'] == [379, 476, 653, 849, 900], r['bits'], r['fixed_bits'], r['bytes']",
  'P.GCS_P, P.GCS_M, L.bip158_vectors(), P.siphash_test_vector()',
  "f['my_filter_equal'], f['my_header_equal'], f['n_elements'], f['filter_bytes'], f['bits_per_element']",
  "f['op_return_outputs'], f['any_op_return_in_filter'], f['scripts_total'], f['n_elements']",
 ],
 "FilterStory": [
  "seen('ml_bfd_2016-05_committed_bloom.html', 'Date: Mon, 09 May 2016')",
  "(w := R['e7_wire'])['cfilter_count'], w['node_without_option']['disconnected']",
  "b['services']['COMPACT_FILTERS'], b['total']",
 ],
 "Transport": [
  "v1, v2 = R['e8_transport']['v1'], R['e8_transport']['v2']",
  "v1['transport_a'], v1['contains_magic'], v1['contains_version_command'], v1['first_bytes_a_to_b'][:8]",
  "v2['transport_a'], v2['contains_magic'], v2['contains_version_command'], v2['entropy_first_4096']",
  "v2['session_id_a'] == v2['session_id_n'], len(v2['session_id_a'])",
  "src('core_src_net.h', 'DEFAULT_V2_TRANSPORT'), round(100 * b['services']['P2P_V2'] / b['total'], 1)",
  "seen('bip-0324.mediawiki', 'unencrypted and unauthenticated'), seen('bip-0324.mediawiki', 'man-in-the-middle')",
 ],
 "EncStory": [
  "seen('core_relnotes_27.0.md', 'BIP324 v2 transport is now enabled by default')",
  "seen('bip-0151.mediawiki', 'Status: Closed')",
  "R['e8_transport']['v2']['contains_magic'], b['services']['P2P_V2']",
 ],
 "Anon": [
  "[(x['name'], x['reachable']) for x in R['networkinfo_A']['networks']]",
  "[x for x in R['e8_onion_node']['networks'] if x[1]]",
  "b['nets']['onion'], b['nets']['i2p'], b['nets']['cjdns']",
  "seen('core_relnotes_22.0.md', 'I2P (Invisible'), seen('core_relnotes_23.0.md', 'for the CJDNS network')",
  "seen('bitcoind_help_31.1.txt', 'Automatically create Tor onion service (default: 1)')",
 ],
}
