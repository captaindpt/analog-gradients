#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORK_DIR="$REPO_DIR/implementation/fullflow_demo/work/dc"
WARN_FILE="$WORK_DIR/reports/alu4_flow_demo_dc_fallback.warn"
LIB_WARN_FILE="$WORK_DIR/reports/alu4_flow_demo_dc_target_lib.warn"

export REPO_DIR
# Default to a curated minimal Liberty subset that compiles cleanly in lc_shell.
# The full PDK Liberty contains cells that fail strict LC consistency checks.
export DC_TARGET_LIB="${DC_TARGET_LIB:-$REPO_DIR/implementation/fullflow_demo/lib/alu4_min_cells.lib}"

mkdir -p "$WORK_DIR"
mkdir -p "$WORK_DIR/out" "$WORK_DIR/reports"

# Keep stage-local defaults so direct stage runs are reproducible.
source "$REPO_DIR/scripts/setup_fullflow_licenses.sh"

rm -f "$WARN_FILE" "$LIB_WARN_FILE"

DC_BIN="/CMC/tools/synopsys/syn_vW-2024.09-SP2/syn/W-2024.09-SP2/bin/dc_shell"
LC_BIN="${LC_BIN:-/CMC/tools/synopsys/lc_vW-2024.09-SP2/lc/W-2024.09-SP2/bin/lc_shell}"

# DC target_library must be a Synopsys DB. If a Liberty .lib is supplied,
# compile it once into a local DB artifact and reuse it.
if [[ "$DC_TARGET_LIB" == *.lib ]]; then
    COMPILED_LIB_DIR="$WORK_DIR/libcache"
    COMPILED_DB="$COMPILED_LIB_DIR/$(basename "${DC_TARGET_LIB%.lib}").db"
    COMPILE_TCL="$WORK_DIR/libcache_compile.tcl"
    COMPILE_LOG="$WORK_DIR/libcache_compile.log"
    mkdir -p "$COMPILED_LIB_DIR"

    if [[ ! -f "$COMPILED_DB" || "$DC_TARGET_LIB" -nt "$COMPILED_DB" ]]; then
        LIB_NAME="$(
            awk '
                match($0, /^[[:space:]]*library[[:space:]]*\(([[:alnum:]_]+)\)/, m) {
                    print m[1]
                    exit
                }
            ' "$DC_TARGET_LIB"
        )"

        if [[ ! -x "$LC_BIN" ]]; then
            echo "WARN: lc_shell not found at $LC_BIN. Falling back to direct path and legacy handling." >&2
        elif [[ -n "$LIB_NAME" ]]; then
            cat > "$COMPILE_TCL" <<EOF
read_lib "$DC_TARGET_LIB"
write_lib -output "$COMPILED_DB" "$LIB_NAME"
exit
EOF
            echo "Compiling Liberty to DB for DC target_library..."
            set +e
            "$LC_BIN" -f "$COMPILE_TCL" | tee "$COMPILE_LOG"
            lib_compile_rc=${PIPESTATUS[0]}
            set -e
            if [[ $lib_compile_rc -eq 0 && -f "$COMPILED_DB" ]]; then
                export DC_TARGET_LIB="$COMPILED_DB"
                echo "Using compiled DB target library: $DC_TARGET_LIB"
            else
                echo "WARN: Failed to compile Liberty to DB. Falling back to direct path and legacy handling." >&2
            fi
        else
            echo "WARN: Could not parse Liberty library name from $DC_TARGET_LIB. Falling back to direct path and legacy handling." >&2
        fi
    else
        export DC_TARGET_LIB="$COMPILED_DB"
        echo "Using cached DB target library: $DC_TARGET_LIB"
    fi
fi

echo "Running DC synthesis smoke flow..."
set +e
"$DC_BIN" -f "$REPO_DIR/implementation/fullflow_demo/scripts/dc_synth.tcl" | tee "$WORK_DIR/dc_shell.log"
dc_rc=${PIPESTATUS[0]}
set -e

dc_issue=""
if grep -q "DCSH-1" "$WORK_DIR/dc_shell.log"; then
    dc_issue="license"
elif grep -q "DB-1" "$WORK_DIR/dc_shell.log" || grep -q "UIO-3" "$WORK_DIR/dc_shell.log"; then
    dc_issue="target_lib"
fi

if [[ "$dc_issue" == "license" ]]; then
    echo "WARN: DC license unavailable (DCSH-1). Using fallback mapped netlist for flow bring-up." >&2
    cp "$REPO_DIR/implementation/fullflow_demo/rtl/alu4_flow_demo_fallback_mapped.v" \
       "$WORK_DIR/out/alu4_flow_demo_mapped.v"
    cat > "$WARN_FILE" <<EOF
DC synthesis could not run due license issue (DCSH-1).
Fallback gate-level netlist was used:
  implementation/fullflow_demo/rtl/alu4_flow_demo_fallback_mapped.v
EOF
elif [[ "$dc_issue" == "target_lib" ]]; then
    echo "WARN: DC target library path is not DB-compatible (DB-1/UIO-3). Using fallback mapped netlist for flow bring-up." >&2
    cp "$REPO_DIR/implementation/fullflow_demo/rtl/alu4_flow_demo_fallback_mapped.v" \
       "$WORK_DIR/out/alu4_flow_demo_mapped.v"
    cat > "$LIB_WARN_FILE" <<EOF
DC synthesis reached runtime but target library setup is incompatible (DB-1).
Current DC_TARGET_LIB:
  $DC_TARGET_LIB
Fallback gate-level netlist was used:
  implementation/fullflow_demo/rtl/alu4_flow_demo_fallback_mapped.v
EOF
elif [[ $dc_rc -ne 0 ]]; then
    echo "ERROR: DC smoke flow failed for a non-license reason." >&2
    exit $dc_rc
fi

if [[ ! -f "$WORK_DIR/out/alu4_flow_demo_mapped.v" ]]; then
    echo "ERROR: Missing synthesized netlist: $WORK_DIR/out/alu4_flow_demo_mapped.v" >&2
    exit 3
fi

echo "DC smoke flow complete."
