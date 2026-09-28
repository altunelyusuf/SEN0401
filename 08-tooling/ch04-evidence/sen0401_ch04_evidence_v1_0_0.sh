#!/usr/bin/env bash
# Chapter 4 evidence run: ask the real Bitcoin Core 31.1 release, run as an offline node, about the book's keys and
# addresses, and save what came back. Usage: sen0401_ch04_evidence_v1_0_0.sh <work-dir> <out-dir>
# <work-dir> must already hold the unpacked release from sen0401_ch03_evidence_v1_0_0.sh (bitcoin-31.1/). Nothing here
# touches a real wallet or chain: -connect=0 in a throw-away HOME, and the keys used are the book's published example.
set -u
W=$(realpath -m "$1"); O=$(realpath -m "$2"); B=$W/bitcoin-31.1/bin
[ -x $B/bitcoind ] || { echo "no release in $W"; exit 1; }
export HOME=$W/home4; rm -rf $HOME; mkdir -p $HOME/.bitcoin
printf 'connect=0\ndnsseed=0\nlisten=0\nfixedseeds=0\n' > $HOME/.bitcoin/bitcoin.conf
$B/bitcoind -daemonwait > /dev/null 2>&1; sleep 2
C="$B/bitcoin-cli"
PUBC=03f028892bad7ed57d2fb57bf33081d5cfcf6f9ed3d3d7f159c2e2fff579dc341a
PUBU=04f028892bad7ed57d2fb57bf33081d5cfcf6f9ed3d3d7f159c2e2fff579dc341a07cf33da18bd734c600b96a72bbc4749d5141c90ec8ac328ae52ddfe2e505bdb
XONLY=2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311
WIFU=5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn
WIFC=KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ
# addresses from public keys, through descriptors (a descriptor carries a checksum: getdescriptorinfo adds it)
: > "$O/core_deriveaddresses_31_1_v1_0_0.txt"
for d in "pkh($PUBC)" "pkh($PUBU)" "wpkh($PUBC)" "sh(wpkh($PUBC))" "tr($XONLY)" "pkh($WIFU)" "pkh($WIFC)" "wpkh($WIFC)"; do
  full=$($C getdescriptorinfo "$d" | python3 -c "import sys,json; print(json.load(sys.stdin)['descriptor'])")
  addr=$($C deriveaddresses "$full" | python3 -c "import sys,json; print(json.load(sys.stdin)[0])")
  # a descriptor that holds a private key is shown with the key hidden
  echo "$d" | sed "s/$WIFU/<WIF>/; s/$WIFC/<WIF>/" | tr '\n' ' ' >> "$O/core_deriveaddresses_31_1_v1_0_0.txt"; echo "=> $addr" >> "$O/core_deriveaddresses_31_1_v1_0_0.txt"
done
# validation of every address string the chapter prints, and of the typo and length-extension examples
python3 - "$C" > "$O/core_validateaddress_31_1_v1_0_0.json" <<'PY'
import json, subprocess, sys
C = sys.argv[1]
ADDR = ["1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy", "1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x", "3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM", "1LoveBPzzD72PUXLzCkYAtGFYmK5vYNR33",
        "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee", "bc1qvj9r9egtd7mu2gemy28kpf4zefq4ssqzdzzycj7zjhk4arpavfhsct5a3p",
        "bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7", "bc1sqqqqkfw08p",
        "bc1p9nh05ha8wrljf7ru236awn4t2x0d5ctkkywmv9sclnm4t0av2vgs4k3au7",
        "bc1pqqqsq9txsqp", "bc1pqqqsq9txsqqqqp", "bc1pqqqsq9txsqqqqqqp", "bc1pqqqsq9txsqqqqqqqqp", "bc1pqqqsq9txsqqqqqqqqqp", "bc1pqqqsq9txsqqqqqqqqqqqp"]
out = {}
for a in ADDR:
    r = subprocess.run([C, "validateaddress", a], capture_output=True, text=True)
    out[a] = json.loads(r.stdout) if r.returncode == 0 else {"error": r.stderr.strip()}
json.dump(out, sys.stdout, indent=1)
PY
$C help getnewaddress > "$O/core_help_getnewaddress_31_1_v1_0_0.txt"
$B/bitcoind -help 2>&1 | grep -A6 "^  -addresstype" > "$O/core_help_addresstype_31_1_v1_0_0.txt"
# what a new wallet hands out by default and for each type, and what Core says of them
$C createwallet demo > /dev/null 2>&1
python3 - "$C" > "$O/core_wallet_addresses_31_1_v1_0_0.json" <<'PY'
import json, subprocess, sys
C = sys.argv[1]
run = lambda *a: json.loads(subprocess.run([C, "-rpcwallet=demo", *a], capture_output=True, text=True).stdout)
out = {}
for t in (None, "legacy", "p2sh-segwit", "bech32", "bech32m"):
    a = subprocess.run([C, "-rpcwallet=demo", "getnewaddress"] + (["", t] if t else []), capture_output=True, text=True).stdout.strip()
    i = run("getaddressinfo", a)
    out[t or "default"] = {"address": a, "desc_kind": i["desc"].split("(")[0], "iswitness": i.get("iswitness"), "witness_version": i.get("witness_version"), "isscript": i.get("isscript"), "scriptPubKey": i.get("scriptPubKey")}
json.dump(out, sys.stdout, indent=1)
PY
$C help importdescriptors | head -3 > "$O/core_help_importdescriptors_31_1_v1_0_0.txt"
: > "$O/core_removed_rpcs_31_1_v1_0_0.txt"
for rpc in dumpprivkey importprivkey; do echo "$rpc: $($C help $rpc 2>&1 | head -1)" >> "$O/core_removed_rpcs_31_1_v1_0_0.txt"; done
$C stop > /dev/null 2>&1
echo "chapter 4 evidence written to $O"
