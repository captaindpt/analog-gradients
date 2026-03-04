#!/usr/bin/env bash
set -u
set +e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR" || exit 1

if ! command -v sde >/dev/null 2>&1; then
  if [ -f scripts/setup_sentaurus.sh ]; then
    # shellcheck disable=SC1091
    source scripts/setup_sentaurus.sh || exit 1
    # setup script may enable errexit; keep scout loop fail-open.
    set +e
  fi
fi

export MEMRISTOR_SWEEP_CSV="${MEMRISTOR_SWEEP_CSV:-tcad/memristor/config/sweep_matrix_reram_scout.csv}"
export MEMRISTOR_SDEVICE_LOG_MODE="${MEMRISTOR_SDEVICE_LOG_MODE:-compact}"
export MEMRISTOR_SDEVICE_TIMEOUT_S="${MEMRISTOR_SDEVICE_TIMEOUT_S:-14400}"
export MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS="${MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS:-0}"
MEMRISTOR_SCOUT_ROWS="${MEMRISTOR_SCOUT_ROWS:-34 35 36 37 38 39 40}"

echo "Scout sweep config:"
echo "  MEMRISTOR_SWEEP_CSV=$MEMRISTOR_SWEEP_CSV"
echo "  MEMRISTOR_SDEVICE_LOG_MODE=$MEMRISTOR_SDEVICE_LOG_MODE"
echo "  MEMRISTOR_SDEVICE_TIMEOUT_S=$MEMRISTOR_SDEVICE_TIMEOUT_S"
echo "  MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS=$MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS"
echo "  MEMRISTOR_SCOUT_ROWS=$MEMRISTOR_SCOUT_ROWS"

for r in $MEMRISTOR_SCOUT_ROWS; do
  echo "=== START SCOUT ROW $r $(date -Iseconds) ==="
  scripts/run_memristor_tcad_sweep.sh "$r"
  rc=$?
  echo "=== END SCOUT ROW $r rc=$rc $(date -Iseconds) ==="
done
