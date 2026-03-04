#!/usr/bin/env bash
set -u
set +e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR" || exit 1

if ! command -v sde >/dev/null 2>&1; then
  if [ -f scripts/setup_sentaurus.sh ]; then
    # shellcheck disable=SC1091
    source scripts/setup_sentaurus.sh || exit 1
    set +e
  fi
fi

export MEMRISTOR_SWEEP_CSV="${MEMRISTOR_SWEEP_CSV:-tcad/memristor/config/sweep_matrix_reram_blitz.csv}"
export MEMRISTOR_SDEVICE_LOG_MODE="${MEMRISTOR_SDEVICE_LOG_MODE:-full}"
export MEMRISTOR_SDEVICE_TIMEOUT_S="${MEMRISTOR_SDEVICE_TIMEOUT_S:-1200}"
export MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS="${MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS:-0}"
BLITZ_ROWS="${MEMRISTOR_BLITZ_ROWS:-901 902 903}"

echo "Blitz config:"
echo "  MEMRISTOR_SWEEP_CSV=$MEMRISTOR_SWEEP_CSV"
echo "  MEMRISTOR_SDEVICE_LOG_MODE=$MEMRISTOR_SDEVICE_LOG_MODE"
echo "  MEMRISTOR_SDEVICE_TIMEOUT_S=$MEMRISTOR_SDEVICE_TIMEOUT_S"
echo "  MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS=$MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS"
echo "  MEMRISTOR_BLITZ_ROWS=$BLITZ_ROWS"

for r in $BLITZ_ROWS; do
  echo "=== START BLITZ ROW $r $(date -Iseconds) ==="
  scripts/run_memristor_tcad_sweep.sh "$r"
  rc=$?
  echo "=== END BLITZ ROW $r rc=$rc $(date -Iseconds) ==="
done
