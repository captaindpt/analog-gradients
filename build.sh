#!/bin/bash
# build.sh - Master build and test script for GPU building blocks
# Usage: ./build.sh [component]
# Examples:
#   ./build.sh           # Build and test all
#   ./build.sh inverter  # Build and test inverter only
#   ./build.sh nand2     # Build and test nand2 only

set -euo pipefail

REPO=/home/v71349/analog-gradients
NETLISTS="$REPO/netlists"
OCEAN="$REPO/ocean"
RESULTS="$REPO/results"
COMPONENT="${1:-all}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

RUN_TS=""
RUN_LOG=""
RUN_MANIFEST=""
CURRENT_COMPONENT=""

init_all_run_artifacts() {
    if [[ "$COMPONENT" != "all" ]]; then
        return
    fi

    mkdir -p "$RESULTS/_runlogs"
    RUN_TS="$(date +%Y%m%d_%H%M%S)"
    RUN_LOG="$RESULTS/_runlogs/build_all_${RUN_TS}.log"
    RUN_MANIFEST="$RESULTS/_runlogs/build_all_${RUN_TS}.manifest.txt"

    # Mirror all output to a timestamped log for auditable full builds.
    exec > >(tee -a "$RUN_LOG") 2>&1

    {
        echo "run_id=$RUN_TS"
        echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "host=$(hostname)"
        echo "repo=$REPO"
        echo "target=$COMPONENT"
        echo "status=running"
    } > "$RUN_MANIFEST"

    echo "Run log: $RUN_LOG"
    echo "Run manifest: $RUN_MANIFEST"
}

finalize_run_manifest() {
    local exit_code=$?
    if [[ -z "$RUN_MANIFEST" ]]; then
        return
    fi

    {
        echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "exit_code=$exit_code"
        if [[ "$exit_code" -eq 0 ]]; then
            echo "status=PASS"
        else
            echo "status=FAIL"
            if [[ -n "$CURRENT_COMPONENT" ]]; then
                echo "failed_component=$CURRENT_COMPONENT"
            fi
        fi
    } >> "$RUN_MANIFEST"
}

record_component_manifest() {
    local name=$1
    local result_file=$2
    local raw_psfxl=$3
    local raw_bytes
    local raw_mtime
    local result_mtime

    if [[ -z "$RUN_MANIFEST" ]]; then
        return
    fi

    raw_bytes="$(wc -c < "$raw_psfxl")"
    raw_mtime="$(date -u -r "$raw_psfxl" +%Y-%m-%dT%H:%M:%SZ)"
    result_mtime="$(date -u -r "$result_file" +%Y-%m-%dT%H:%M:%SZ)"

    {
        echo "component=$name status=PASS raw_psfxl=$raw_psfxl raw_bytes=$raw_bytes raw_mtime_utc=$raw_mtime result_file=$result_file result_mtime_utc=$result_mtime"
    } >> "$RUN_MANIFEST"
}

require_fresh_raw() {
    local name=$1
    local raw_psfxl=$2
    local start_epoch=$3
    local raw_epoch

    if [[ ! -f "$raw_psfxl" ]]; then
        echo -e "${RED}Simulation: FAILED${NC}"
        echo "Missing raw data file for $name: $raw_psfxl"
        return 1
    fi

    raw_epoch="$(stat -c %Y "$raw_psfxl")"
    if (( raw_epoch < start_epoch )); then
        echo -e "${RED}Simulation: FAILED${NC}"
        echo "Raw data for $name is stale: $raw_psfxl"
        return 1
    fi
}

run_ocean_and_check() {
    local ocean_script=$1
    local result_file=$2
    local ocean_log=$3
    local done_pattern=$4

    rm -f "$result_file"
    ocean -nograph < "$ocean_script" > "$ocean_log" 2>&1

    if ! grep -E "$done_pattern" "$ocean_log"; then
        echo "No PASS/FAIL marker found in OCEAN output ($ocean_log)."
    fi

    if [[ ! -f "$result_file" ]]; then
        echo -e "${RED}Verification: FAILED${NC}"
        echo "Missing verification file: $result_file"
        return 1
    fi

    if ! grep -q "PASS" "$result_file"; then
        echo -e "${RED}Verification: FAILED${NC}"
        cat "$result_file" 2>/dev/null || echo "No results file"
        return 1
    fi

    rm -f "$ocean_log"
}

init_all_run_artifacts
trap finalize_run_manifest EXIT

# Setup Cadence environment
source /home/v71349/analog-gradients/setup_cadence.sh

run_sim() {
    local name=$1
    local sim_dir="$RESULTS/$name"
    local raw_dir="$sim_dir/${name}.raw"
    local raw_psfxl="$raw_dir/tran_test.tran.tran.psfxl"
    local result_file="$RESULTS/${name}_test.txt"
    local ocean_log="$sim_dir/ocean.log"
    local sim_start_epoch

    CURRENT_COMPONENT="$name"
    echo -e "${YELLOW}=== Building $name ===${NC}"

    # Create results directory
    mkdir -p "$sim_dir"
    rm -rf "$raw_dir"
    rm -f "$sim_dir/spectre.log" "$ocean_log" "$result_file"

    # Run Spectre simulation
    echo "Running Spectre simulation..."
    sim_start_epoch="$(date +%s)"
    (
        cd "$sim_dir"
        spectre "$NETLISTS/${name}.scs" -raw "${name}.raw" +log spectre.log > /dev/null
    )
    tail -5 "$sim_dir/spectre.log"

    # Check for errors
    if ! grep -q "completes with 0 errors" "$sim_dir/spectre.log"; then
        echo -e "${RED}Simulation: FAILED${NC}"
        return 1
    fi

    require_fresh_raw "$name" "$raw_psfxl" "$sim_start_epoch"
    echo -e "${GREEN}Simulation: OK${NC}"

    # Run OCEAN verification
    echo "Running OCEAN verification..."
    run_ocean_and_check "$OCEAN/test_${name}.ocn" "$result_file" "$ocean_log" "(PASS|FAIL|done|Done)"

    # Check results
    echo -e "${GREEN}Verification: PASS${NC}"
    record_component_manifest "$name" "$result_file" "$raw_psfxl"

    echo ""
    CURRENT_COMPONENT=""
}

# Special verification for inverter (different result file location)
run_sim_inverter() {
    local name="inverter"
    local sim_dir="$RESULTS/$name"
    local raw_dir="$sim_dir/${name}.raw"
    local raw_psfxl="$raw_dir/tran_test.tran.tran.psfxl"
    local result_file="$RESULTS/inverter_verify.txt"
    local ocean_log="$sim_dir/ocean.log"
    local sim_start_epoch

    CURRENT_COMPONENT="$name"
    echo -e "${YELLOW}=== Building $name ===${NC}"

    mkdir -p "$sim_dir"
    rm -rf "$raw_dir"
    rm -f "$sim_dir/spectre.log" "$ocean_log" "$result_file"

    echo "Running Spectre simulation..."
    sim_start_epoch="$(date +%s)"
    (
        cd "$sim_dir"
        spectre "$NETLISTS/${name}.scs" -raw "${name}.raw" +log spectre.log > /dev/null
    )
    tail -5 "$sim_dir/spectre.log"

    if ! grep -q "completes with 0 errors" "$sim_dir/spectre.log"; then
        echo -e "${RED}Simulation: FAILED${NC}"
        return 1
    fi

    require_fresh_raw "$name" "$raw_psfxl" "$sim_start_epoch"
    echo -e "${GREEN}Simulation: OK${NC}"

    echo "Running OCEAN verification..."
    run_ocean_and_check "$OCEAN/verify_${name}.ocn" "$result_file" "$ocean_log" "(PASS|FAIL|done|Done)"

    echo -e "${GREEN}Verification: PASS${NC}"
    record_component_manifest "$name" "$result_file" "$raw_psfxl"

    echo ""
    CURRENT_COMPONENT=""
}

# Main
echo "========================================"
echo "GPU Building Blocks - Build & Test"
echo "========================================"
echo ""

case $COMPONENT in
    inverter)
        run_sim_inverter
        ;;
    nand2)
        run_sim nand2
        ;;
    nor2)
        run_sim nor2
        ;;
    and2)
        run_sim and2
        ;;
    or2)
        run_sim or2
        ;;
    xor2)
        run_sim xor2
        ;;
    xnor2)
        run_sim xnor2
        ;;
    mux2)
        run_sim mux2
        ;;
    half_adder)
        run_sim half_adder
        ;;
    full_adder)
        run_sim full_adder
        ;;
    alu1)
        run_sim alu1
        ;;
    alu4)
        run_sim alu4
        ;;
    pe1)
        run_sim pe1
        ;;
    pe4)
        run_sim pe4
        ;;
    gpu_core)
        run_sim gpu_core
        ;;
    synapse)
        run_sim synapse
        ;;
    lif_neuron)
        run_sim lif_neuron
        ;;
    neuron_tile)
        run_sim neuron_tile
        ;;
    neuro_tile4)
        run_sim neuro_tile4
        ;;
    neuro_tile4_coupled)
        run_sim neuro_tile4_coupled
        ;;
    neuro_tile4_mixed_signal)
        run_sim neuro_tile4_mixed_signal
        ;;
    all)
        echo "Building Level 5: CMOS primitives"
        echo "=================================="
        run_sim_inverter
        run_sim nand2
        run_sim nor2
        echo ""
        echo "Building Level 4: Logic gates"
        echo "=================================="
        run_sim and2
        run_sim or2
        run_sim xor2
        run_sim xnor2
        echo ""
        echo "Building Level 3: Blocks"
        echo "=================================="
        run_sim mux2
        run_sim half_adder
        run_sim full_adder
        echo ""
        echo "Building Level 2: RTL Components"
        echo "=================================="
        run_sim alu1
        run_sim alu4
        echo ""
        echo "Building Level 1: Functional Blocks"
        echo "=================================="
        run_sim pe1
        run_sim pe4
        echo ""
        echo "Building Level 0: System"
        echo "=================================="
        run_sim gpu_core
        echo ""
        echo "Building Competition Analog Primitives"
        echo "=================================="
        run_sim synapse
        run_sim lif_neuron
        echo ""
        echo "Building Competition Analog Compositions"
        echo "=================================="
        run_sim neuron_tile
        run_sim neuro_tile4
        run_sim neuro_tile4_coupled
        run_sim neuro_tile4_mixed_signal
        echo "=================================="
        echo -e "${GREEN}All Level 0-5 components + analog competition path verified!${NC}"
        ;;
    *)
        echo "Unknown component: $COMPONENT"
        echo "Available: inverter, nand2, nor2, and2, or2, xor2, xnor2, mux2, half_adder, full_adder, alu1, alu4, pe1, pe4, gpu_core, synapse, lif_neuron, neuron_tile, neuro_tile4, neuro_tile4_coupled, neuro_tile4_mixed_signal, all"
        exit 1
        ;;
esac
