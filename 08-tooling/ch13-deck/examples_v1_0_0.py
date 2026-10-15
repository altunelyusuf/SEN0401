"""Every computation the SEN0401 chapter 13 (Bitcoin Security) lecture deck shows. The outputs come from executing these statements, never from typing them:
sen0401_deck_examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE loads the chapter's own library (sen0401_ch13_lib_v1_0_0.py: an independent BIP 39, BIP 32, Shamir and odds code, and readers of the saved sources) and the saved records it reads:
R is the single run of Bitcoin Core 31.1 on regtest (ch13-evidence/regtest_run; one run, so its values are Recorded on the slides); the real blocks and heights are public figures from mempool.space,
saved in ch13-evidence on 2026-10-15 (L.jload and L.raw read them, J(n) reads block n). seen(file, text) finds a passage in a saved source, src(file, name) reads a constant from a saved source file.
Rows that read R only read the record; rows that call L.bip39_*, L.bip32_master, L.shamir_*, L.p_lose and L.p_theft compute. The statements are the research package's executed claims
(sen0401_ch13_leaves_v1_0_0.py, research v1_0_1), cut into one-line rows. Every group is named after the slide that shows it. deck_check re-runs every '>>>' line of the finished deck in this same namespace,
so a statement is ONE line."""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))

PRELUDE = """
import sys, math, hashlib, datetime
sys.path.insert(0, %r)
import sen0401_ch13_lib_v1_0_0 as L
R = L.run()
src, seen = L.const, L.has
J = lambda n: L.jload('mempool_block_' + str(n) + '.json')
cr = lambda k: src('core_src_wallet_crypter.h', k)
sm = 'shamir_1979_how_to_share_a_secret.txt'
hww = 'bitcoinwiki_hardware_wallet.txt'
""" % TOOLING

EX = {
 # ---- part A: trust --------------------------------------------------------------------------------------------------------
 "Payment": [
  "s, t, r = R['b1_secrecy'], R['b1_tamper'], R['b1_replay']",
  "s['tx_bytes'], s['witness_item_lengths'], s['private_key_hex_in_tx'], s['wif_in_tx']",
  "t['valid']['allowed'], t['address_replaced']['allowed'], t['amount_changed']['allowed']",
  "s['sighash_byte'], r['testmempoolaccept']['reject-reason'], r['balance_r'], r['balance_r_after']",
  "r['sendrawtransaction']['error'].split('message: ')[1]",
 ],
 "Transport": [
  "p, n = R['b2_peers'], R['b2_netinfo']",
  "p['Q'][0]['transport'], p['P'][0]['transport'], R['b2_session_ids_match'], 'P2P_V2' in n['P_localservices']",
  "p['X'][0]['transport'], [y['transport'] for y in p['P']].count('v1'), n['X_localservices']",
  "seen('book_ch13_security.adoc', 'no encryption is required for Bitcoin traffic')",
  "seen('core_relnotes_27.0.md', 'BIP324 v2 transport is now enabled by default')",
 ],
 "Root": [
  "g, b = J(0), J(938343)",
  "g['id'][:20], g['height'], seen('core_src_kernel_chainparams.cpp', g['id'])",
  "b['height'], b['id'][:24], seen('core_src_kernel_chainparams.cpp', b['id'])",
  "seen('bitcoind_help_31.1.txt', 'potentially skip their script verification')",
  "int(L.raw('mempool_tip_height.txt')) - b['height']",
 ],
 "Release": [
  "r = R['b8_release']",
  "r['match'], r['tarball_sha256'][:16], r['tarball_bytes'], r['n_lines_in_list']",
  "r['gpg_exit'], r['gpg_has_signature_line'], r['n_signatures_made'], r['n_cannot_check_no_public_key']",
  "seen('core_contrib_guix_README.md', 'instead of blindly _trusting_ binary downloads')",
 ],
 # ---- part B: keeping keys ----------------------------------------------------------------------------------------------------
 "Cold": [
  "h, c, b = R['b3_hot'], R['b3_cold'], R['b3_broadcast']",
  "h['watch_private_keys_enabled'], h['hot_sign_complete'], h['partial_sigs_before']",
  "h['hot_listdescriptors_private']['error'].split('message: ')[1]",
  "c['blocks'], c['connections'], c['sign_complete'], h['psbt_chars'], c['psbt_chars_signed']",
  "b['finalize_complete'], b['confirmations'], b['dest_received']",
 ],
 "Hardware": [
  "w = [2 ** k for k in range(15)]",
  "w, sum(w), round(sum(w) / 3600, 1)",
  "seen('bitcoinwiki_trezor.txt', 'wipe itself after 16 failed PIN entry attempts')",
  "seen('core_doc_external-signer.md', '-signer=<cmd>'), seen(hww, 'swap out the recipient')",
 ],
 "Encryption": [
  "l, w, u, f = R['b4_locked'], R['b4_wrong'], R['b4_unlocked'], R['b4_file']",
  "l['send']['error']",
  "w['error'], l['balance_visible']",
  "u['unlocked_until'] - u['now'], u['send_ok'], R['b4_after_timeout']['unlocked_until']",
  "[cr('WALLET_CRYPTO_' + k) for k in ('KEY_SIZE', 'SALT_SIZE', 'IV_SIZE')], cr('DEFAULT_DERIVE_ITERATIONS')",
  "f['encryptwallet_message'][:60], f['xprv_text_in_file_before']",
 ],
 "Backups": [
  "b, d = R['b5_backup'], R['b6_backup']",
  "b['balance_src'], b['balance_fresh'], b['fresh_next_matches'], b['far_address_ismine_fresh']",
  "b['keypool_range_end'], b['far_index'], b['balance_stale'], b['far_address_ismine_stale']",
  "d['m1_knows_multisig_address'], d['ms_balance'], d['rebuilt_balance'], d['wrongorder_balance']",
  "seen('bitcoind_help_31.1.txt', 'Smaller sizes may increase the risk of losing funds')",
 ],
 "Seeds": [
  "v = L.jload('bip39_trezor_vectors.json')['english'][0]; w = v[1].split()",
  "L.bip39_mnemonic(bytes.fromhex(v[0])) == v[1], len(w), L.bip39_valid(v[1])",
  "L.bip39_valid(' '.join(w[:-1] + ['zoo'])), 12 * 11 - 128",
  "L.bip39_seed(v[1], 'TREZOR').hex() == v[2], L.bip39_seed(v[1]).hex()[:16]",
  "sum(seen(f, 'mnemonic') for f in ('core_doc_descriptors.md', 'bitcoind_help_31.1.txt'))",
 ],
 "TrezorStory": [
  "w = [2 ** k for k in range(15)]",
  "sum(w), round(sum(w) / 3600, 1)",
  "seen('bitcoinwiki_trezor.txt', 'an EAL 6+ secure element')",
 ],
 "CasasciusStory": [
  "t = 'bitcoinwiki_casascius.txt'",
  "seen(t, 'sold until Nov 26, 2013'), seen(t, '1000 BTC increments')",
  "seen(t, 'qualifies him as a money transmitter')",
 ],
 # ---- part C: surviving loss and theft -----------------------------------------------------------------------------------------------
 "Multisig": [
  "s, l, o = R['b6_sign'], R['b6_loss'], R['b6_order']",
  "s['m1_alone'], s['m1_m3'], s['vsize']",
  "l['lose_m1_sign_with_m2_m3'], l['lose_m2_m3_sign_with_m1']",
  "R['b6_single_vsize'], s['vsize'], o['sortedmulti_same'], o['multi_same']",
 ],
 "Odds": [
  "[round(L.p_lose(0.1, m, n), 4) for m, n in ((1, 1), (2, 3), (1, 3))]",
  "[round(L.p_theft(0.05, m, n), 5) for m, n in ((1, 1), (2, 3), (1, 3))]",
  "round(L.p_lose(0.5, 2, 3), 4)",
 ],
 "Heir": [
  "h, lim = R['b7_heir'], R['b7_limits']",
  "R['b7_owner']['allowed'], R['b7_descriptor']['policy']",
  "[h[k]['allowed'] for k in ('at_1_conf', 'at_9_conf', 'at_10_conf')], h['at_9_conf']['reject_reason']",
  "lim['65535'], lim['65536'], R['b7_older_65536']['allowed'], R['b7_older_65536']['confirmations']",
  "round(65535 * 10 / 1440, 1), round(R['b7_unit_seconds_x65535'] / 86400, 1)",
 ],
 "Shamir": [
  "sh, c = L.shamir_split(123456789, 2, 3, [987654321]), L.shamir_candidates((1, 100))",
  "sh",
  "[L.shamir_recover(x) for x in (sh[:2], sh[1:])], L.shamir_recover(sh[:1]) == 123456789",
  "len(c), len({s for s, _ in c}), len({sl for _, sl in c})",
 ],
 "MtGoxStory": [
  "t = 'wikipedia_mt_gox.txt'",
  "seen(t, '744,408 bitcoins'), seen(t, 'over 70% of all bitcoin')",
  "round(850000 - 199999.99, 2), seen(t, '199,999.99')",
 ],
 "ShamirStory": [
  "sh = L.shamir_split(123456789, 2, 3, [987654321])",
  "L.shamir_recover(sh[:2]), L.shamir_recover(sh[1:])",
  "seen(sm, '(k, n) threshold scheme'), seen(sm, 'completely undetermined')",
 ],
}
