#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$REPO_DIR/implementation/fullflow_demo/work/logs"
DC_WARN="$REPO_DIR/implementation/fullflow_demo/work/dc/reports/alu4_flow_demo_dc_fallback.warn"
CAL_WARN="$REPO_DIR/implementation/fullflow_demo/work/calibre/alu4_flow_demo_calibre_license.warn"
STRICT_MODE="${FULLFLOW_STRICT:-0}"
mkdir -p "$LOG_DIR"

echo "[1/3] Design Compiler synthesis"
"$REPO_DIR/scripts/run_dc_smoke.sh" | tee "$LOG_DIR/stage1_dc.log"

echo "[2/3] Innovus place/route"
"$REPO_DIR/scripts/run_innovus_smoke.sh" | tee "$LOG_DIR/stage2_innovus.log"

echo "[3/3] Calibre DRC smoke"
"$REPO_DIR/scripts/run_calibre_smoke.sh" | tee "$LOG_DIR/stage3_calibre.log"

echo "Full-flow smoke pipeline complete."

if [[ -f "$DC_WARN" ]]; then
    echo "WARN: DC stage used fallback netlist (license constrained)." >&2
fi

if [[ -f "$CAL_WARN" ]]; then
    echo "WARN: Calibre stage blocked by license." >&2
fi

if [[ "$STRICT_MODE" == "1" ]] && { [[ -f "$DC_WARN" ]] || [[ -f "$CAL_WARN" ]]; }; then
    echo "ERROR: FULLFLOW_STRICT=1 and at least one stage is license-blocked." >&2
    exit 20
fi
