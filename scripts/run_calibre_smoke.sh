#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORK_DIR="$REPO_DIR/implementation/fullflow_demo/work/calibre"
INNOVUS_OUT="$REPO_DIR/implementation/fullflow_demo/work/innovus/out"
GDS_IN="$INNOVUS_OUT/alu4_flow_demo.gds"
WARN_FILE="$WORK_DIR/alu4_flow_demo_calibre_license.warn"

mkdir -p "$WORK_DIR"

# Keep stage-local defaults so direct stage runs are reproducible.
source "$REPO_DIR/scripts/setup_fullflow_licenses.sh"

rm -f "$WARN_FILE"

if [[ ! -f "$GDS_IN" ]]; then
    echo "ERROR: Missing GDS for Calibre DRC smoke: $GDS_IN" >&2
    exit 5
fi

RULE_FILE="$WORK_DIR/alu4_flow_demo_drc_smoke.svrf"
RESULT_DB="$WORK_DIR/alu4_flow_demo_drc.results"
SUMMARY="$WORK_DIR/alu4_flow_demo_drc.summary"

cat > "$RULE_FILE" <<EOF
LAYOUT PATH "$GDS_IN"
LAYOUT PRIMARY "alu4_flow_demo"
LAYOUT SYSTEM GDSII

DRC RESULTS DATABASE "$RESULT_DB" ASCII
DRC SUMMARY REPORT "$SUMMARY" REPLACE HIER
DRC MAXIMUM RESULTS ALL

LAYER M1 11
LAYER M2 12

M1_WIDTH_CHECK {
  @ Smoke check: minimum width on layer 11
  INTERNAL M1 < 0.04
}

M2_WIDTH_CHECK {
  @ Smoke check: minimum width on layer 12
  INTERNAL M2 < 0.04
}
EOF

CALIBRE_BIN="/CMC/tools/siemens/aok_cal_2025.4_24/bin/calibre"

echo "Running Calibre DRC smoke flow..."
set +e
"$CALIBRE_BIN" -drc -hier "$RULE_FILE" | tee "$WORK_DIR/calibre_drc.log"
cal_rc=${PIPESTATUS[0]}
set -e

if [[ $cal_rc -ne 0 ]]; then
    if grep -qi "Unable to acquire the first license" "$WORK_DIR/calibre_drc.log" \
       || grep -qi "products could not be licensed" "$WORK_DIR/calibre_drc.log"; then
        echo "WARN: Calibre DRC license unavailable. Recording blocked status." >&2
        cat > "$WARN_FILE" <<EOF
Calibre DRC smoke could not run due unavailable DRC license.
Command:
  $CALIBRE_BIN -drc -hier $RULE_FILE
EOF
        cat > "$SUMMARY" <<EOF
Calibre DRC smoke status: BLOCKED (license unavailable)
EOF
    else
        echo "ERROR: Calibre DRC smoke failed for a non-license reason." >&2
        exit $cal_rc
    fi
fi

if [[ ! -f "$SUMMARY" ]]; then
    echo "ERROR: Missing Calibre DRC summary: $SUMMARY" >&2
    exit 6
fi

echo "Calibre smoke flow complete."
