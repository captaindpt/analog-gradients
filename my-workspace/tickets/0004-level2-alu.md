# 0004: Build Level 2 ALU

**Status:** Open
**Priority:** High
**Created:** 2026-02-01

## Description

Build and verify a minimal ALU path to support the GPU-Lite spec.

## Tasks

- [x] ALU1 netlist + OCEAN test
- [x] ALU4 netlist + OCEAN test (spot checks)
- [ ] Verify truth tables / spot checks
- [ ] Update STATUS.md with verification

## Acceptance Criteria

1. Files created:
   - `netlists/alu1.scs`
   - `netlists/alu4.scs`
   - `ocean/test_alu1.ocn`
   - `ocean/test_alu4.ocn`
2. `./build.sh alu1` and `./build.sh alu4` pass
3. STATUS.md updated with PASS results
