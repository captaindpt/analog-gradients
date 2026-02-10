#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/v71349/analog-gradients"
cd "$REPO_DIR"

source scripts/setup_sentaurus.sh

for r in {28..40}; do
  echo "=== START ROW $r $(date -Iseconds) ==="
  scripts/run_memristor_tcad_sweep.sh "$r"
  rc=$?
  echo "=== END ROW $r rc=$rc $(date -Iseconds) ==="
done
