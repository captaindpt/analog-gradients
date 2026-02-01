# 0003: Build Level 3 Blocks

**Status:** Open
**Priority:** High
**Created:** 2026-02-01

## Description

Build and verify core Level 3 blocks needed for the ALU path.

## Tasks

- [x] MUX2 netlist + OCEAN test
- [x] Half Adder netlist + OCEAN test
- [x] Full Adder netlist + OCEAN test
- [x] Verify all truth tables
- [x] Update STATUS.md with verification

## Acceptance Criteria

1. Files created:
   - `netlists/mux2.scs`
   - `netlists/half_adder.scs`
   - `netlists/full_adder.scs`
   - `ocean/test_mux2.ocn`
   - `ocean/test_half_adder.ocn`
   - `ocean/test_full_adder.ocn`
2. `./build.sh mux2`, `./build.sh half_adder`, `./build.sh full_adder` pass
3. STATUS.md updated with PASS results
