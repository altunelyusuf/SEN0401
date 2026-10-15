"""Every computation the SEN0401 chapter 14 (Second-Layer Applications) lecture deck shows. The outputs come from executing these statements, never from typing them:
sen0401_deck_examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE loads the chapter's own library (sen0401_ch14_lib_v1_0_0.py: the BOLT 3, 4, 8 and 11 test vectors recomputed in Python, and readers of the saved sources) and the saved records it reads:
R is the single run of Bitcoin Core 31.1 on regtest chains and of five lnd 0.21.3-beta nodes (ch14-evidence; one run, so its values are Recorded on the slides); the public figures of mempool.space
are saved in ch14-evidence on 2026-10-15 (L.jload reads them). seen(file, text) finds a passage in a saved source. Rows that read R only read the record; rows that call L.bolt8, L.onion,
L.invoice, L.bolt3_keys, L.route_fees and L.timelocks compute. The statements are the research package's executed claims (sen0401_ch14_leaves_v1_0_0.py, research 14), cut into one-line rows.
Every group is named after the slide that shows it. deck_check re-runs every '>>>' line of the finished deck in this same namespace, so a statement is ONE line."""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))

PRELUDE = "\nimport sys, math, hashlib, datetime\nsys.path.insert(0, " + repr(TOOLING) + ")\nimport sen0401_ch14_lib_v1_0_0 as L\nR = L.run()\nseen = L.has\n"

EX = {
 # ---- part A: what the base chain guarantees -------------------------------------------------------------------------------
 "Double": [
  "d, n = R['c1']['double_spend'], R['c1']['non_expiration']",
  "d['first_accepted'], d['second_lower_fee'].split(',')[0]",
  "d['second_higher_fee'], d['first_still_in_mempool'], d['first_after_block'].split(' ')[-1]",
  "R['c1']['outputs_exceed_inputs'], n['allowed'], n['tested_at_height'] - n['signed_at_height']",
  "seen('core_relnotes_28.0.md', '-mempoolfullrbf` configuration option has been changed from 0 to 1')",
 ],
 "Pledge": [
  "p, l = R['c1']['proof_of_existence'], R['c1']['lighthouse']",
  "p['contains_hash'], p['nulldata_asm'] == 'OP_RETURN ' + p['sha256'], len(p['sha256']) // 2, p['value']",
  "l['pledge_a_sat'] + l['pledge_b_sat'] - l['fee_sat'] == l['goal_sat'], l['only_a']['reason']",
  "l['both']['allowed'], l['output_changed']['reason'].split(' (')[0], l['a_signed_all_then_b_added']['allowed']",
 ],
 "Seals": [
  "c, p = R['c2']['client_side_validation'], R['c2']['p2c']",
  "c['spent_by_next'], len(c['tx_ids']), len({h['outpoint'] for h in c['history']})",
  "p['same_as_plain_p2wpkh'], p['reveal_check'], p['reveal_wrong_contract']",
  "p['spend_with_plain_key']['allowed'], p['spend_with_tweaked_key']['allowed']",
  "c['commitments_match'], c['forged_contract_matches'], c['tokens_visible_in_chain']",
 ],
 # ---- part B: payment channels -------------------------------------------------------------------------------------------------
 "Emma": [
  "c = R['c3']; k = 1000; cap = 36 * 100000",
  "k * 3600, k * 3600 == cap, k * 600, cap - k * 600, c['capacity_sat'] == cap, c['settlement_outputs_sat'][0] // k",
  "c['emma_alone']['reason'].split(' (')[0], c['both_sign']['allowed'], c['funding_vsize']",
  "c['witness_script_hex'][:2], c['witness_script_hex'][-4:], c['witness_script_len']",
 ],
 "Ladder": [
  "c = R['c3']",
  "c['locktimes'], c['at_start'].count('non-final')",
  "c['tip_l_minus_6']['c6']['reason'], c['tip_l_minus_5']['c6']['allowed']",
  "c['after_c6_mined']['c1_to_c5'], c['after_all_timelocks']['c1']",
 ],
 "Commit": [
  "c = R['c4']; a = c['to_local_script_asm'].split(' ')",
  "a[0], a[3], a[4], a[-1], c['delay_at_999_confirmations']['reason']",
  "c['delay_at_1000_confirmations']['allowed'], c['commitment_vsize']",
  "c['revoke_with_one_half']['reason'].split(' (')[0], c['revoke_with_both_halves']['allowed']",
  "c['revoke_witness_items'], c['revoke_confirmed']",
  "c['delay_blocks'], R['l5']['state1']['csv_delay'], R['l2']['channels_after']['alice'][0]['csv_delay']",
 ],
 "Htlc": [
  "h = R['c5']; a = lambda k: h[k]['allowed']; w = lambda k: h[k]['reason'].split(' (')[-1].rstrip(')')",
  "a('claim_with_secret'), w('claim_with_wrong_secret'), a('claim_with_secret_but_payer_key')",
  "w('refund_before_timeout'), w('refund_at_tip_lock_minus_1'), a('refund_at_tip_lock')",
  "h['lock_height'] - h['height_at_funding'], h['hash160_is_ripemd160_of_sha256'], h['secret_len']",
 ],
 # ---- part C: the Lightning Network ------------------------------------------------------------------------------------------
 "Five": [
  "h = R['l2']['htlcs'][0]; a = [int(x['amt_to_forward_msat']) // 1000 for x in h['hops']]",
  "[x - 10 ** 8 for x in a], int(h['total_fees_msat']) // 1000",
  "e = [x['expiry'] for x in h['hops']]",
  "[p - q for p, q in zip(e, e[1:])], h['total_time_lock'] - e[0], R['l2']['invoice']['cltv_expiry']",
 ],
 "Hold": [
  "h = R['l3']; n = ['alice', 'bob', 'carol', 'diana', 'eric']; f = h['inflight']",
  "sorted({p['amount'] for k in n for c in f[k] for p in c['pending']})",
  "h['cancel']['balances_before'] == h['cancel']['balances_after'], [h['cancel']['pending_during'][k] for k in n]",
  "h['settled_status']",
 ],
 "Wire": [
  "b = L.bolt8(); mine, want, hops = L.onion()",
  "b['act1'] == b['want_act1'], b['act3'] == b['want_act3'], b['sk'] == b['want_sk']",
  "(len(b['act1']) - 2) // 2, (len(b['act3']) - 2) // 2, L.bolt8_hello()[1]",
  "mine == want, len(mine) // 2, hops, [L.onion_size(n) for n in (1, 2, 5)]",
  "L.onion_hmac_ok(mine), L.onion_hmac_ok(mine, 0), L.onion_hmac_ok(mine, 1299 * 8 + 7)",
 ],
 "Invoice": [
  "i = R['l2']['invoice']; p = L.C.bolt11(i['payment_request'])",
  "p['hrp'], p['msat'], L.C.field_int(p['fields']['c'][0])",
  "hashlib.sha256(bytes.fromhex(R['l2']['preimage'])).hexdigest() == i['payment_hash']",
  "v = L.invoice()",
  "v['hrp'], v['msat'] // 1000, L.iso(v['timestamp']), len(v['sig'])",
 ],
 "Chain": [
  "f, c, k = R['l4']['funding'], R['l4']['close'], R['l5']['revoked_commitment']",
  "f['type'], f['value'], c['witness_script_asm'].split(' ')[4]",
  "hex(k['locktime'] >> 24), hex(k['sequence'] >> 24), len(k['outputs']), k['witness_items'], k['vsize']",
  "c['locktime'], [o['type'] for o in c['outputs']], c['vsize'], R['l4']['onchain_transactions_in_lifetime']",
  "L.bolt3_keys()",
 ],
 "Breach": [
  "l = R['l5']; j = l['justice']; c = R['c6']; r = c['package']['ok']['tx-results']",
  "l['state2']['hitesh'], l['state2']['irene'], l['hitesh_closed'][0]['close_type'], len(j['inputs'])",
  "[i['witness_items'] for i in j['inputs']], round(j['outputs'][0]['value'] * 1e8)",
  "c['parent_alone']['reject-reason'], c['package_msg'], c['anchor_witness_len'], c['both_confirmed']",
  "round(max(v['fees']['effective-feerate'] for v in r.values()) * 1e5, 1), c['parent_vsize'], c['child_vsize']",
 ],
 # ---- stories ----------------------------------------------------------------------------------------------------------------------
 "PizzaStory": [
  "s = L.jload('mempool_lightning_statistics.json')['latest']",
  "s['channel_count'], s['node_count'], round(s['total_capacity'] / 1e8, 1)",
  "s['med_base_fee_mtokens'], s['med_fee_rate']",
 ],
 "SpillmanStory": [
  "t = 'bitcoinwiki_payment_channels.html'",
  "seen(t, 'Anti DoS for tx replacement'), seen(t, '20 April 2013')",
  "seen(t, 'An unrecorded open transaction can keep being replaced')",
 ],
 "PaperStory": [
  "seen('wikipedia_lightning_network.html', 'white paper in February 2015')",
  "(datetime.date(2016, 1, 14) - datetime.date(2015, 2, 28)).days",
  "seen('book_ch14_applications.adoc', 'is a proposed routed network')",
 ],
 "TorchStory": [
  "L.route_fees(10 ** 8, [10 ** 5] * 3)[0]",
  "L.route_fees(1000, [1, 1, 1])[0]",
  "seen('wikipedia_lightning_network.html', 'added 10,000 satoshis')",
 ],
}
