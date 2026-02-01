# 0005: Build Level 1 PE Array

**Status:** Open
**Priority:** High
**Created:** 2026-02-01

## Description

Create a minimal PE (ALU4-only) and a 4-PE array with shared opcode to match
the GPU-Lite v2 demo spec.

## Tasks

- [x] PE1 netlist + OCEAN test
- [x] PE4 netlist + OCEAN test
- [x] Verify spot checks (PE0 only)
- [x] Update STATUS.md with verification

## Acceptance Criteria

1. Files created:
   - `netlists/pe1.scs`
   - `netlists/pe4.scs`
   - `ocean/test_pe1.ocn`
   - `ocean/test_pe4.ocn`
2. `./build.sh pe1` and `./build.sh pe4` pass
3. STATUS.md updated with PASS results
