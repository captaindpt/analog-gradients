#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TCAD_ROOT="$REPO_DIR/tcad/memristor"
CFG_FILE="${1:-$TCAD_ROOT/config/phase_a_anchor.env}"
RUN_TAG="${RUN_TAG:-phaseA}"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$TCAD_ROOT/runs/${RUN_ID}_${RUN_TAG}"

if [[ ! -f "$CFG_FILE" ]]; then
  echo "Missing config: $CFG_FILE" >&2
  exit 1
fi

mkdir -p "$RUN_DIR"

# shellcheck source=/dev/null
source "$CFG_FILE"

cat > "$RUN_DIR/manifest.txt" <<EOF
run_id=$RUN_ID
run_tag=$RUN_TAG
created_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
anchor_id=${ANCHOR_ID:-unknown}
device_class=${DEVICE_CLASS:-unknown}
config_file=$CFG_FILE
ron_ohm=${RON_OHM:-}
roff_ohm=${ROFF_OHM:-}
von_v=${VON_V:-}
voff_v=${VOFF_V:-}
xinit=${XINIT:-}
threshold_err_max_pct=${THRESHOLD_ERR_MAX_PCT:-}
energy_ratio_max=${ENERGY_RATIO_MAX:-}
EOF

cp "$TCAD_ROOT/templates/metrics_schema.csv" "$RUN_DIR/metrics_template.csv"

echo "Initialized memristor phase-A run:"
echo "  $RUN_DIR"
echo "Manifest:"
echo "  $RUN_DIR/manifest.txt"
