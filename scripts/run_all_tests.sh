#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Source Cadence environment
# shellcheck disable=SC1091
source "$ROOT/setup_cadence.sh"

# Ensure license is set (CMC default)
export CDS_LIC_FILE="${CDS_LIC_FILE:-6055@licaccess.cmc.ca}"

LOG_DIR="$ROOT/results/_runlogs"
mkdir -p "$LOG_DIR"
TS="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$LOG_DIR/build_all_${TS}.log"

echo "Running full test suite..."
echo "Log: $LOG_FILE"
./build.sh all 2>&1 | tee "$LOG_FILE"

echo ""
echo "PASS summary:"
grep -H "=== PASS" "$ROOT"/results/*_test.txt || true
