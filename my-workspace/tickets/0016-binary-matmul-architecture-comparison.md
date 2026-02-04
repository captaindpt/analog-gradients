# 0016: Binary 2x2 Matmul Architecture Comparison

**Status:** In Progress
**Priority:** High
**Created:** 2026-02-04

## Description

Build a reproducible proof demo that runs the same binary 2x2 matmul task on:

1. a clocked digital baseline, and
2. the neuromorphic spike/integration path.

Goal is a defensible comparison of correctness, latency, and energy.

## Tasks

- [x] Add reference spec for binary matmul comparison method
- [x] Implement neuro binary 2x2 matmul netlist + verifier
- [x] Integrate neuro target into `build.sh`
- [x] Implement digital binary 2x2 matmul baseline + verifier
- [x] Add matched energy extraction for both architectures
- [x] Publish side-by-side comparison summary under `competition/analysis/`
- [x] Add matrix-size scaling sweep harness (`N=2..16`, density/seed sweep)
- [x] Generate scaling plots + markdown summary for architecture discussion

## Acceptance Criteria

1. Both architectures compute the same binary 2x2 workload with deterministic
   PASS/FAIL verification.
2. Energy and latency are reported using explicit, reproducible methods.
3. Final report states scope limits clearly (binary-only first proof).

## Latest Progress (2026-02-04)

- Added neuro binary matmul netlist:
  - `netlists/matmul2x2_binary_neuro.scs`
- Added verifier:
  - `ocean/test_matmul2x2_binary_neuro.ocn`
- Added build target:
  - `./build.sh matmul2x2_binary_neuro`
  - included in `./build.sh all`
- First PASS run:
  - `results/matmul2x2_binary_neuro_test.txt`
  - `results/_runlogs/build_matmul2x2_binary_neuro_20260203_212412.manifest.txt`
- Added digital binary matmul baseline:
  - `netlists/matmul2x2_binary_digital.scs`
  - `ocean/test_matmul2x2_binary_digital.ocn`
  - `./build.sh matmul2x2_binary_digital` (included in `./build.sh all`)
- Added side-by-side run script:
  - `scripts/run_matmul2x2_binary_comparison.sh`
- Latest comparison artifacts:
  - `competition/analysis/matmul2x2_binary_comparison.md`
  - `competition/analysis/matmul2x2_binary_comparison.csv`

## Open Follow-Up

- Upgrade digital baseline from minimal combinational netlist to a clocked
  PE/GPU-core-linked workload harness for a stricter apples-to-apples comparison.
- Move from model-based scaling extrapolation to transistor-run NxN points
  (at least `N=4` and `N=8`) for calibration hardening.

## Latest Progress (2026-02-04, scaling sweep)

- Added model-based scaling scripts:
  - `scripts/run_matmul_binary_scaling_sweep.sh`
  - `scripts/analyze_matmul_binary_scaling.py`
- New latest artifacts:
  - `competition/sweeps/matmul_binary_scaling_sweep.csv`
  - `competition/analysis/matmul_binary_scaling_summary.md`
  - `competition/analysis/matmul_binary_scaling_energy.svg`
  - `competition/analysis/matmul_binary_scaling_pressure.svg`
- Run snapshots now archived per run:
  - `competition/sweeps/matmul_binary_scaling/<timestamp>/...`
