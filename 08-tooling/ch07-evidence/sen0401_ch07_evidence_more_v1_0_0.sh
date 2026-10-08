#!/bin/sh
# More sources for the chapter 7 corpus, fetched after sen0401_ch07_evidence_v1_0_0.sh: files of Bitcoin Core at the pinned commit
# (05bc2f5) and book chapters. Version 1.0.0. Run from this folder.
CORE=05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940
for f in src/consensus/tx_verify.cpp src/primitives/transaction.h src/script/descriptor.cpp src/test/data/bip341_wallet_vectors.json; do
  curl -sS -L -m 60 -o "core_$(echo $f | tr / _)" "https://raw.githubusercontent.com/bitcoin/bitcoin/$CORE/$f"
done
