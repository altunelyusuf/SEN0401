"""Every computation the SEN0401 chapter 8 (Digital Signatures) lecture deck shows. The outputs come from executing these statements, never from typing them:
sen0401_deck_examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE loads the chapter's own library (sen0401_ch08_sig_lib_v1_0_0.py, checked against the 19 BIP340 vectors, Bitcoin Core's 500 signature hash vectors, the BIP327 key
aggregation vectors and the RFC 6979 vector) and the chapter's claims module (sen0401_ch08_claims_v1_0_0.py), whose functions are the executed claims of the research package.
Rows that begin 'K.core_' only READ the record of one run of Bitcoin Core 31.1.0 on regtest (08-tooling/ch08-evidence/core_regtest_record_v1_0_0.json); the slides call them Recorded.
Every group is named after the concept (or story) whose slide shows it. deck_check re-runs every '>>>' line of the finished deck in this same namespace, so a statement is ONE line.
"""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))

PRELUDE = """
import sys, json, hashlib
sys.path.insert(0, %r)
import sen0401_ch07_script_lib_v1_0_0 as L
import sen0401_ch08_sig_lib_v1_0_0 as C
import sen0401_ch08_claims_v1_0_0 as K

def yn(d):
    return ' | '.join('%%s %%s' %% (k, ''.join('Y' if x else '.' for x in v) if isinstance(v, list) else ('Y' if v else '.')) for k, v in d.items())

def ok(d):
    return ''.join('Y' if v[0] else '.' for v in d.values())

def bips(d):
    return ' '.join('%%d %%s' %% (k, v[:3]) for k, v in d.items())
""" % TOOLING

EX = {
 # ---- part 1: what a signature is and what it signs ------------------------------------------------------------
 "SignVerify": [
  "d, pk = L.ecdsa_sign(K.SK, K.MSG), L.pubkey_create(K.SK)",
  "len(d), L.ecdsa_verify(pk, K.MSG, d)",
  "L.ecdsa_verify(pk, bytes([K.MSG[0] ^ 1]) + K.MSG[1:], d)",
  "L.ecdsa_verify(L.pubkey_create(K.SK + 1), K.MSG, d)",
  "K.two_parties_two_inputs()",
 ],
 "Moduli": [
  "5 % 3",
  "K.toy()",
  "K.scalar_modulus()",
  "L.P - L.N > 2 ** 128, L.P.bit_length(), L.N.bit_length()",
 ],
 "Flags": [
  "{h: ''.join('Y' if x else '.' for x in v) for h, v in K.commitments_table().items()}",
 ],
 "CoreFlags": [
  'yn(K.core_signature_survives_changes())',
  'yn(K.core_anyonecanpay_survives_other_input_change())',
 ],
 "SingleBug": [
  "K.single_bug_hash()  # input 1, no output 1",
  "K.single_bug_equals_uint256_one()",
  "K.sighash_json_vectors()",
  "K.core_refuses_single_bug_signature()",
 ],
 # ---- part 2: Schnorr --------------------------------------------------------------------------------------------
 "Fiat": [
  "K.toy()  # a small field first",
  "K.identity_round_secp256k1(), K.identity_wrong_s()",
  "K.impersonation_without_x()",
  "K.fiat_shamir_signature()",
 ],
 "PatentStory": [
  "K.patent_dates()  # filed, granted, expired",
  "K.schnorr_to_taproot_years()",
  "K.bip340_vectors()",
 ],
 "Bip340": [
  "K.bip340_vectors()  # published tests",
  "K.signature_sizes()",
  "K.xonly_even_y()",
  "K.tagged_hash_prefix_len()",
  "K.bip340_default_signing_deterministic()",
  "K.related_key_attack()",
  "K.batch_equation()",
 ],
 "KeyAgg": [
  "K.linearity()  # keys add, so do signatures",
  "K.naive_multisig()",
  "K.key_cancellation()",
  "K.musig2_keyagg_vectors()",
  "K.musig2_blocks_cancellation()",
 ],
 "Threshold": [
  "K.shamir_any_two_of_three()  # any 2 pieces",
  "K.single_share_hides_secret()",
  "K.shamir_manipulation()",
  "K.no_threshold_bip_in_index()",
 ],
 # ---- part 3: ECDSA, DER and nonces -------------------------------------------------------------------------------
 "EcdsaMath": [
  "K.ecdsa_book_formulas()  # the book, run",
  "K.malleability()",
  "K.lib_signature_low_s_and_strict()",
  "K.own_variants_digests()",
 ],
 "BookSignature": [
  "K.book_der_sample()  # the book bytes",
  "K.book_sample_in_mainnet_tx()",
  "K.book_sample_verifies()",
  "K.book_sample_s_low()",
  "K.timestamp_of_book_tx()",
 ],
 "NonceDet": [
  'K.rfc6979_p256_vector()',
  'K.rfc6979_deterministic()',
  'K.core_ecdsa_deterministic_and_schnorr_aux_zero()',
  'K.library_signatures_high_r_share()',
  "dict(K._core()['lengths']['sig_lengths'])",
  'K.core_signatures_low_r()',
 ],
 "NonceReuse": [
  "K.nonce_reuse()  # same k twice",
  "K.nonce_not_reused_is_safe()",
  "K.rfc6979_matches_library_nonce()",
 ],
 # ---- part 4: segwit, taproot and since the book -------------------------------------------------------------------
 "Hashing": [
  'K.hashing_bytes()[1:3]',
  'K.hashing_growth()',
  'K.bip143_commits_to_amount()',
  'K.bip341_commits_to_all_spent_amounts()',
  'K.first_taproot_spend()',
 ],
 "PolicyConsensus": [
  'ok(K.core_policy_verdicts())  # Recorded',
  'K.core_high_s_consensus()',
  'K.own_variants_digests()',
 ],
 "TaprootTypes": [
  'K.bip341_valid_hash_types()',
  'ok(K.core_taproot_verdicts())',
  'K.core_node_identity()',
 ],
 "SinceBook": [
  "dict(__import__('collections').Counter(K.bips_status().values()))",
  "K.core_musig_support(), K.libsecp_changes()",
  "K.sigops_limit_in_core_and_bip54(), [K.bips_status()[n] for n in (118, 461, 361)]",
 ],
}
