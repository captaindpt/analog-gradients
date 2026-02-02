#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORK_DIR="$REPO_DIR/implementation/fullflow_demo/work/dc"

export REPO_DIR
export DC_TARGET_LIB="${DC_TARGET_LIB:-/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/timing/slow_vdd1v0_basicCells.lib}"

mkdir -p "$WORK_DIR"

DC_BIN="/CMC/tools/synopsys/syn_vW-2024.09-SP2/syn/W-2024.09-SP2/bin/dc_shell"

echo "Running DC synthesis smoke flow..."
set +e
"$DC_BIN" -f "$REPO_DIR/implementation/fullflow_demo/scripts/dc_synth.tcl" | tee "$WORK_DIR/dc_shell.log"
dc_rc=${PIPESTATUS[0]}
set -e

if [[ $dc_rc -ne 0 ]]; then
    if grep -q "DCSH-1" "$WORK_DIR/dc_shell.log"; then
        echo "WARN: DC license unavailable (DCSH-1). Using fallback mapped netlist for flow bring-up." >&2
        mkdir -p "$WORK_DIR/out" "$WORK_DIR/reports"
        cp "$REPO_DIR/implementation/fullflow_demo/rtl/alu4_flow_demo_fallback_mapped.v" \
           "$WORK_DIR/out/alu4_flow_demo_mapped.v"
        cat > "$WORK_DIR/reports/alu4_flow_demo_dc_fallback.warn" <<EOF
DC synthesis could not run due license issue (DCSH-1).
Fallback gate-level netlist was used:
  implementation/fullflow_demo/rtl/alu4_flow_demo_fallback_mapped.v
EOF
    else
        echo "ERROR: DC smoke flow failed for a non-license reason." >&2
        exit $dc_rc
    fi
fi

if [[ ! -f "$WORK_DIR/out/alu4_flow_demo_mapped.v" ]]; then
    echo "ERROR: Missing synthesized netlist: $WORK_DIR/out/alu4_flow_demo_mapped.v" >&2
    exit 3
fi

echo "DC smoke flow complete."
