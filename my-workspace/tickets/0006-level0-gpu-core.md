# 0006: Build Level 0 GPU Core

**Status:** Open
**Priority:** High
**Created:** 2026-02-01

## Description

Integrate PE4 into a top-level GPU-Lite core and verify spot checks.

## Tasks

- [x] GPU core netlist + OCEAN test
- [ ] Verify spot checks
- [ ] Update STATUS.md with verification

## Acceptance Criteria

1. Files created:
   - `netlists/gpu_core.scs`
   - `ocean/test_gpu_core.ocn`
2. `./build.sh gpu_core` passes
3. STATUS.md updated with PASS results
