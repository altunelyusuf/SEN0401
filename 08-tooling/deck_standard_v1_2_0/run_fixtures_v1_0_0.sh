#!/bin/bash
# Runs v1_2_0 on the five fixtures and prints the D9 line of each. Usage: run_fixtures_v1_0_0.sh FIXDIR
T="$(cd "$(dirname "$0")/.." && pwd)"
for f in "$1"/*.pptx; do echo "== $(basename "$f")"; python3 -B "$T/sen0401_deck_standard_check_v1_2_0.py" 05 "$f" | grep -E "^(sen0401_deck_standard_check|D9 )"; done
