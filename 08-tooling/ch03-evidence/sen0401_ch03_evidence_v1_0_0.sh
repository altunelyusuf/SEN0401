#!/usr/bin/env bash
# Chapter 3 evidence run: download the real Bitcoin Core release, verify it, run the book's commands on an offline node,
# and save what came back. Usage: sen0401_ch03_evidence_v1_0_0.sh <work-dir> <out-dir> [<guix.sigs clone>]
# Needs curl, tar, sha256sum, python3 (with uv for the Python 3.14.4 venv), and gpg when a guix.sigs clone is given.
# Nothing here touches a real wallet or the real chain: the node runs with -connect=0 in a throw-away HOME.
set -u
W=$(realpath -m "$1"); O=$(realpath -m "$2"); SIGS=${3:-}; VER=31.1
mkdir -p "$W" "$O"; cd "$W"
BASE=https://bitcoincore.org/bin/bitcoin-core-$VER
T=bitcoin-$VER-x86_64-linux-gnu.tar.gz
[ -f SHA256SUMS ] || curl -sS -m 120 -O $BASE/SHA256SUMS
[ -f SHA256SUMS.asc ] || curl -sS -m 120 -O $BASE/SHA256SUMS.asc
[ -f $T ] || curl -sS -m 600 -O $BASE/$T
{ echo "release: $VER"; echo "expected (from SHA256SUMS):"; grep " $T\$" SHA256SUMS; echo "computed:"; sha256sum $T; } > "$O/release_check_31_1_v1_0_0.txt"
if [ -n "$SIGS" ]; then
  export GNUPGHOME=$W/gnupg; mkdir -p $GNUPGHOME; chmod 700 $GNUPGHOME
  for k in "$SIGS"/builder-keys/*.gpg; do gpg --batch -q --import "$k" 2>/dev/null; done
  { echo "builder keys imported from the guix.sigs clone: $(gpg --list-keys 2>/dev/null | grep -c '^pub')"; echo "good signatures on SHA256SUMS: $(gpg --batch --verify SHA256SUMS.asc SHA256SUMS 2>&1 | grep -c 'Good signature')"; echo "(the keys' own trust is not established by this check: they come from the guix.sigs repository, not from an out-of-band source)"; } >> "$O/release_check_31_1_v1_0_0.txt"
fi
grep -E "win64-setup.exe|x86_64-linux-gnu.tar.gz|arm64-apple-darwin.tar.gz" SHA256SUMS | awk '{print $2}' > "$O/release_files_31_1_v1_0_0.txt"
[ -d bitcoin-$VER ] || tar xzf $T
B=$W/bitcoin-$VER/bin
ls bitcoin-$VER/bin bitcoin-$VER/libexec > "$O/release_layout_31_1_v1_0_0.txt"
$B/bitcoind --version | head -2 > "$O/version_31_1_v1_0_0.txt"
$B/bitcoind -help > "$O/help_bitcoind_31_1_v1_0_0.txt" 2>&1
$B/bitcoin --help > "$O/help_bitcoin_wrapper_31_1_v1_0_0.txt" 2>&1
# an offline mainnet node in a throw-away HOME
export HOME=$W/home; rm -rf $HOME; mkdir -p $HOME/.bitcoin
printf 'connect=0\ndnsseed=0\nlisten=0\nfixedseeds=0\n' > $HOME/.bitcoin/bitcoin.conf
(timeout 6 $B/bitcoind -printtoconsole > "$O/startup_31_1_v1_0_0.log" 2>&1; true); sleep 1
$B/bitcoind -daemonwait > /dev/null 2>&1; sleep 2
$B/bitcoin-cli getblockchaininfo > "$O/getblockchaininfo_31_1_v1_0_0.json"
$B/bitcoin-cli getnetworkinfo > "$O/getnetworkinfo_31_1_v1_0_0.json"
$B/bitcoin-cli help > "$O/help_rpc_31_1_v1_0_0.txt"
HEX=$(python3 - <<'PY'
print("01000000000101eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a0100000000ffffffff02204e0000000000002251203b41daba4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068f8240100000000001600147752c165ea7be772b2c0acb7f4d6047ae6f4768e0141cf5efe2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e521c00b51be739df2f899c49dc267c0ad280aca6dab0d2fa2b42a45182fc83e817130100000000")
PY
)
echo "$HEX" > "$O/alice_tx_hex_book_v1_0_0.txt"
$B/bitcoin-cli decoderawtransaction "$HEX" > "$O/alice_decoded_31_1_v1_0_0.json"
$B/bitcoin-cli createwallet demo > "$O/createwallet_31_1_v1_0_0.json" 2>&1
$B/bitcoin-cli -rpcwallet=demo getwalletinfo > "$O/getwalletinfo_31_1_v1_0_0.json" 2>&1
$B/bitcoin-cli -named createwallet wallet_name=legacy descriptors=false > "$O/createwallet_legacy_31_1_v1_0_0.txt" 2>&1
python3 "${RPCAUTH:-/dev/null}" alice 2>/dev/null | sed 's/rpcauth=alice:.*/rpcauth=alice:<salt>$<hash>/; /^Your password:/{n;s/.*/<random password>/}' > "$O/rpcauth_31_1_v1_0_0.txt"
# the book's own script, unchanged, under Python 3.14.4 with python-bitcoinlib 0.12.2
if command -v uv >/dev/null; then
  uv venv --python 3.14.4 -q $W/v314 >/dev/null 2>&1; uv pip install -q --python $W/v314/bin/python python-bitcoinlib==0.12.2 >/dev/null 2>&1
  (cd "${BOOKCODE:-.}" && $W/v314/bin/python rpc_example.py > "$O/rpc_example_output_31_1_v1_0_0.txt" 2>&1; $W/v314/bin/python -c "import sys,bitcoin; print(sys.version.split()[0], bitcoin.__file__ and 'python-bitcoinlib imported')" >> "$O/rpc_example_output_31_1_v1_0_0.txt" 2>&1)
fi
ls $HOME/.bitcoin | sed 's/^/data dir entry: /' > "$O/datadir_entries_31_1_v1_0_0.txt"
$B/bitcoin-cli stop > /dev/null 2>&1
# the book's constrained-node setting together with txindex, refused by the release
rm -rf $W/pt; mkdir -p $W/pt; (timeout 20 $B/bitcoind -datadir=$W/pt -regtest -connect=0 -listen=0 -dnsseed=0 -prune=5000 -txindex=1 -printtoconsole 2>&1 | tail -3 > "$O/prune_txindex_31_1_v1_0_0.txt"; true)
echo "evidence written to $O"
