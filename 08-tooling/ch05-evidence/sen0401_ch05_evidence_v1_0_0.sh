#!/usr/bin/env bash
# Chapter 5 evidence run: ask the real Bitcoin Core 31.1 release (offline node, throw-away HOME, -connect=0) about descriptors,
# the BIP84 test vector, a fresh wallet's descriptors, and its option and RPC lists. Usage: <script> <core-dir> <out-dir>
set -u
B=$(realpath -m "$1")/bitcoin-31.1/bin; O=$(realpath -m "$2")
[ -x $B/bitcoind ] || { echo "no release in $1"; exit 1; }
export HOME=$(mktemp -d); mkdir -p $HOME/.bitcoin
printf 'connect=0\ndnsseed=0\nlisten=0\nfixedseeds=0\n' > $HOME/.bitcoin/bitcoin.conf
$B/bitcoind -daemonwait > /dev/null 2>&1; sleep 2
C="$B/bitcoin-cli"
$C --version | head -1 > "$O/core_version_31_1_v1_0_0.txt"
python3 - "$C" "$O" <<'PY'
import json, subprocess, sys
C, O = sys.argv[1], sys.argv[2]
cli = lambda *a: subprocess.run([C, *a], capture_output=True, text=True)
out = {}
# the BIP84 test vector's account-level extended public key, as an ordinary xpub, with key origin
XPUB84 = sys.stdin.read() if False else None
descs = ["pkh(02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5)",
         "sh(multi(2,022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01,03acd484e2f0c7f65309ad178a9f559abde09796974c57e714c35f110dfc27ccbe))",
         "pkh([d34db33f/44'/0'/0']xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL/1/*)",
         "raw(deadbeef)"]
out["getdescriptorinfo"] = {d: json.loads(cli("getdescriptorinfo", d).stdout) for d in descs}
json.dump(out, open(O + "/core_getdescriptorinfo_31_1_v1_0_0.json", "w"), indent=1)
PY
# the BIP84 account xpub is computed by the verify script and passed in a file
if [ -f "$O/bip84_account_descriptor_v1_0_0.txt" ]; then
  d=$(cat "$O/bip84_account_descriptor_v1_0_0.txt")
  full=$($C getdescriptorinfo "$d" | python3 -c "import sys,json; print(json.load(sys.stdin)['descriptor'])")
  python3 - "$C" "$full" "$O" <<'PY'
import json, subprocess, sys
C, full, O = sys.argv[1:4]
r = subprocess.run([C, "deriveaddresses", full, "[0,2]"], capture_output=True, text=True)
json.dump({"descriptor": full, "addresses": json.loads(r.stdout)}, open(O + "/core_deriveaddresses_bip84_31_1_v1_0_0.json", "w"), indent=1)
PY
fi
$C createwallet w5 > /dev/null 2>&1
python3 - "$C" "$O" <<'PY'
import json, subprocess, sys
C, O = sys.argv[1], sys.argv[2]
run = lambda *a: json.loads(subprocess.run([C, "-rpcwallet=w5", *a], capture_output=True, text=True).stdout)
d = run("listdescriptors")
for x in d["descriptors"]: pass
a = subprocess.run([C, "-rpcwallet=w5", "getnewaddress"], capture_output=True, text=True).stdout.strip()
info = run("getaddressinfo", a)
w = run("getwalletinfo")
json.dump({"descriptors": d["descriptors"], "first_address": a, "addressinfo": {k: info.get(k) for k in ("desc", "hdkeypath", "hdseedid", "ismine", "iswitness", "ischange")}, "walletinfo": {k: w.get(k) for k in ("walletname", "format", "private_keys_enabled", "descriptors", "keypoolsize", "keypoolsize_hd_internal")}}, open(O + "/core_fresh_wallet_31_1_v1_0_0.json", "w"), indent=1)
PY
$C help > "$O/core_rpc_help_31_1_v1_0_0.txt" 2>&1
$B/bitcoind -help 2>&1 | grep -B1 -A3 "^  -keypool" > "$O/core_help_keypool_31_1_v1_0_0.txt"
$C help backupwallet > "$O/core_help_backupwallet_31_1_v1_0_0.txt" 2>&1
$C help listdescriptors > "$O/core_help_listdescriptors_31_1_v1_0_0.txt" 2>&1
$C stop > /dev/null 2>&1; sleep 2; rm -rf "$HOME"
echo "chapter 5 evidence written to $O"
