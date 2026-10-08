#!/usr/bin/env bash
# Chapter 6 evidence run (version 1.0.0): the primary standards of the Transactions chapter, saved beside the
# corpus so that every quotation can be re-read from a saved copy by an executed claim. No Bitcoin Core node is
# available in this environment, so where chapter 5 asked a running release, this chapter reads the project's
# source at the commit pinned for the course (05bc2f5, in the local checkout /home/claude/src/bitcoin) with
# `git show` - the consensus constants and the transaction checks are code, not runtime output - and records the
# one runtime value the book quotes (the weight 569 that bitcoin-cli reported for Alice's transaction) as a cited
# value, recomputed from the serialization by the chapter's own library.
# Usage: <script> <out-dir>        (curl through the session's proxy; raw.githubusercontent.com is reachable)
set -u
O=$(realpath -m "$1"); mkdir -p "$O"
GH=https://raw.githubusercontent.com
get() { curl -sSL --fail -o "$O/$2" "$1" && echo "saved $2 ($(wc -c < "$O/$2") bytes)" || echo "FAILED $1"; }
for n in 0030 0034 0062 0065 0068 0112 0113 0125 0141 0143 0144 0174; do
  get $GH/bitcoin/bips/master/bip-$n.mediawiki bip-$n.mediawiki
done
get $GH/bitcoin/bips/master/bip-0370.mediawiki bip-0370.mediawiki
get $GH/bitcoin/bips/master/bip-0431.mediawiki bip-0431.mediawiki
# the book's own chapter at the pinned commit of the textbook ontology (CC BY-SA 4.0)
get $GH/bitcoinbook/bitcoinbook/275c4eb8eab8800c6adc39f8def8e8f8fa356a57/ch06_transactions.adoc book_ch06_transactions.adoc
# Bitcoin Core at the course's pinned commit: the files the chapter's statements are checked against
C=05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940; R=/home/claude/src/bitcoin
for f in src/consensus/consensus.h src/consensus/tx_check.cpp src/consensus/amount.h src/consensus/tx_verify.cpp \
         src/primitives/transaction.h src/primitives/transaction.cpp src/policy/policy.h src/policy/policy.cpp \
         src/script/script.h src/serialize.h src/validation.cpp src/consensus/validation.h src/policy/rbf.h src/chain.h src/kernel/chainparams.cpp doc/bips.md doc/release-notes/release-notes-28.0.md; do
  git -C $R show $C:$f > "$O/core_$(echo $f | tr '/' '_')" && echo "saved core_$(echo $f | tr '/' '_')"
done
echo "$C" > "$O/core_commit_v1_0_0.txt"
# explorer evidence (no node here): the raw hex and the explorer's JSON record of four transactions, fetched from
# mempool.space on 2026-10-08T11:03Z - Alice's transaction of the chapter (block 775,072), the transaction whose output it
# spends (block 774,958), the first bitcoin transaction (block 170) and the pizza transaction of 2010-05-22 (block 57,043).
# A JSON record is saved as mempool_tx_<first 16 hex>_v1_0_0.json, a raw transaction as tx_<name>_<first 8 hex>_v1_0_0.hex.
MP=https://mempool.space/api/tx
for t in 466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177:alice 4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19278fe33aeb:alice_prev \
         f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16:first a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d:pizza; do
  id=${t%%:*}; nm=${t##*:}
  curl -sS -m 30 "$MP/$id" | python3 -m json.tool > "$O/mempool_tx_${id:0:16}_v1_0_0.json"
  curl -sS -m 30 -o "$O/tx_${nm}_${id:0:8}_v1_0_0.hex" "$MP/$id/hex"
done
