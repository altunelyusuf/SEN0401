#!/usr/bin/env bash
# Chapter 7 evidence run (version 1.0.0): the standards that define authorization and authentication in Bitcoin, saved
# beside the corpus so that every quotation can be re-read from a saved copy by an executed claim. No Bitcoin Core node is
# available in this environment, so Bitcoin Core is read as source at the commit pinned for the course (05bc2f5, the local
# checkout /home/claude/src/bitcoin) with `git show`: its script interpreter, opcodes, policy and the test vectors the
# project ships. Real transactions come from mempool.space (raw hex plus the explorer's JSON record with each spent
# output), fetched on 2026-10-08.
# Usage: <script> <out-dir>        (curl through the session's proxy; raw.githubusercontent.com and mempool.space are reachable)
set -u
O=$(realpath -m "$1"); mkdir -p "$O"
GH=https://raw.githubusercontent.com
get() { curl -sSL --fail -o "$O/$2" "$1" && echo "saved $2 ($(wc -c < "$O/$2") bytes)" || echo "FAILED $1"; }
for n in 0011 0013 0016 0032 0065 0066 0068 0086 0112 0114 0116 0141 0143 0146 0147 0173 0327 0340 0341 0342 0350; do
  get $GH/bitcoin/bips/master/bip-$n.mediawiki bip-$n.mediawiki
done
get $GH/bitcoin/bips/master/bip-0340/test-vectors.csv bip-0340_test-vectors.csv
get $GH/bitcoinbook/bitcoinbook/275c4eb8eab8800c6adc39f8def8e8f8fa356a57/ch07_authorization-authentication.adoc book_ch07_authorization-authentication.adoc
C=05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940; R=/home/claude/src/bitcoin
for f in src/script/interpreter.cpp src/script/interpreter.h src/script/script.h src/script/script.cpp src/script/script_error.h \
         src/script/solver.cpp src/script/solver.h src/policy/policy.cpp src/policy/policy.h src/consensus/consensus.h \
         src/kernel/chainparams.cpp src/consensus/params.h src/pubkey.cpp src/script/sign.cpp doc/bips.md; do
  git -C $R show $C:$f > "$O/core_$(echo $f | tr '/' '_')" && echo "saved core_$(echo $f | tr '/' '_')"
done
echo "$C" > "$O/core_commit_v1_0_0.txt"
# --- added in the same version before first use: the 2010 script engine, read from the tagged releases, and the bug list
get $GH/bitcoin/bips/master/bip-0379.md bip-0379.md
for v in v0.3.0 v0.3.7; do get $GH/bitcoin/bitcoin/$v/script.cpp old_bitcoin_${v}_script.cpp; done
get $GH/bitcoin/bitcoin/v0.3.0/main.cpp old_bitcoin_v0.3.0_main.cpp
curl -sSL --fail https://en.bitcoin.it/wiki/Common_Vulnerabilities_and_Exposures | python3 -c "
import sys,re,html
t=sys.stdin.read(); t=re.sub(r'(?s)<(script|style).*?</\1>','',t); t=re.sub(r'<[^>]+>',' ',t); print(' '.join(html.unescape(t).split()))" > "$O/bitcoinwiki_common_vulnerabilities_v1_0_0.txt" && echo "saved bitcoinwiki_common_vulnerabilities_v1_0_0.txt"
