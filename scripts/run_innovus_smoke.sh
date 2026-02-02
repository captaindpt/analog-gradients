#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORK_DIR="$REPO_DIR/implementation/fullflow_demo/work/innovus"

export REPO_DIR
export DC_TARGET_LIB="${DC_TARGET_LIB:-/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/timing/slow_vdd1v0_basicCells.lib}"
export GPDK045_TECH_LEF="${GPDK045_TECH_LEF:-/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/lef/gsclib045_tech.lef}"
export GPDK045_MACRO_LEF="${GPDK045_MACRO_LEF:-/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/lef/gsclib045_macro.lef}"
export GPDK045_QRC="${GPDK045_QRC:-/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/qrc/qx/gpdk045.tch}"
export GPDK045_STD_GDS="${GPDK045_STD_GDS:-/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/gds/gsclib045.gds}"

mkdir -p "$WORK_DIR"
source "$REPO_DIR/setup_cadence.sh" >/dev/null

INNOVUS_BIN="/CMC/tools/cadence/INNOVUS21.17.000_lnx86/tools.lnx86/bin/innovus"

echo "Running Innovus place/route smoke flow..."
"$INNOVUS_BIN" -no_gui -overwrite -files "$REPO_DIR/implementation/fullflow_demo/scripts/innovus_pnr.tcl" | tee "$WORK_DIR/innovus.log"

if [[ ! -f "$WORK_DIR/out/alu4_flow_demo.def" ]]; then
    echo "ERROR: Missing routed DEF: $WORK_DIR/out/alu4_flow_demo.def" >&2
    exit 4
fi

if [[ -f "$WORK_DIR/out/alu4_flow_demo.gds" ]]; then
    echo "INFO: GDS generated at $WORK_DIR/out/alu4_flow_demo.gds"
else
    echo "WARN: GDS was not generated (streamOut may have failed)." >&2
fi

echo "Innovus smoke flow complete."
