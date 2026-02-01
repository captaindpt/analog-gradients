#!/bin/bash
# build.sh - Master build and test script for GPU building blocks
# Usage: ./build.sh [component]
# Examples:
#   ./build.sh           # Build and test all
#   ./build.sh inverter  # Build and test inverter only
#   ./build.sh nand2     # Build and test nand2 only

set -e  # Exit on error

# Setup Cadence environment
source /home/v71349/analog-gradients/setup_cadence.sh

REPO=/home/v71349/analog-gradients
NETLISTS=$REPO/netlists
OCEAN=$REPO/ocean
RESULTS=$REPO/results

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

run_sim() {
    local name=$1
    echo -e "${YELLOW}=== Building $name ===${NC}"

    # Create results directory
    mkdir -p $RESULTS/$name

    # Run Spectre simulation
    echo "Running Spectre simulation..."
    cd $RESULTS/$name
    spectre $NETLISTS/${name}.scs -raw ${name}.raw +log spectre.log 2>&1 | tail -5

    # Check for errors
    if grep -q "completes with 0 errors" spectre.log; then
        echo -e "${GREEN}Simulation: OK${NC}"
    else
        echo -e "${RED}Simulation: FAILED${NC}"
        return 1
    fi

    # Run OCEAN verification
    echo "Running OCEAN verification..."
    cd $REPO
    ocean -nograph < $OCEAN/test_${name}.ocn 2>&1 | grep -E "(PASS|FAIL|done)" || true

    # Check results
    if grep -q "PASS" $RESULTS/${name}_test.txt 2>/dev/null; then
        echo -e "${GREEN}Verification: PASS${NC}"
    else
        echo -e "${RED}Verification: FAILED${NC}"
        cat $RESULTS/${name}_test.txt 2>/dev/null || echo "No results file"
        return 1
    fi

    echo ""
}

# Special verification for inverter (different result file location)
run_sim_inverter() {
    local name="inverter"
    echo -e "${YELLOW}=== Building $name ===${NC}"

    mkdir -p $RESULTS/$name

    echo "Running Spectre simulation..."
    cd $RESULTS/$name
    spectre $NETLISTS/${name}.scs -raw ${name}.raw +log spectre.log 2>&1 | tail -5

    if grep -q "completes with 0 errors" spectre.log; then
        echo -e "${GREEN}Simulation: OK${NC}"
    else
        echo -e "${RED}Simulation: FAILED${NC}"
        return 1
    fi

    echo "Running OCEAN verification..."
    cd $REPO
    ocean -nograph < $OCEAN/verify_${name}.ocn 2>&1 | grep -E "(PASS|FAIL|Done)" || true

    if grep -q "PASS" $RESULTS/inverter_verify.txt 2>/dev/null; then
        echo -e "${GREEN}Verification: PASS${NC}"
    else
        echo -e "${RED}Verification: FAILED${NC}"
        cat $RESULTS/inverter_verify.txt 2>/dev/null || echo "No results file"
        return 1
    fi

    echo ""
}

# Main
echo "========================================"
echo "GPU Building Blocks - Build & Test"
echo "========================================"
echo ""

COMPONENT=${1:-all}

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
        echo "=================================="
        echo -e "${GREEN}All Level 0-5 components verified!${NC}"
        ;;
    *)
        echo "Unknown component: $COMPONENT"
        echo "Available: inverter, nand2, nor2, and2, or2, xor2, xnor2, mux2, half_adder, full_adder, alu1, alu4, pe1, pe4, gpu_core, all"
        exit 1
        ;;
esac
