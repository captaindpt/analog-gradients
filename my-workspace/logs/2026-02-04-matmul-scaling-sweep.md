# 2026-02-04 - Binary Matmul Scaling Sweep (Ticket 0016)

## Objective

Add a reproducible matrix-size sweep to compare digital and neuromorphic
architecture behavior as binary matmul size increases.

## Work Completed

- Added sweep runner:
  - `scripts/run_matmul_binary_scaling_sweep.sh`
- Added analysis/model script:
  - `scripts/analyze_matmul_binary_scaling.py`
- Sweep script now:
  1. re-runs calibrated 2x2 transistor baselines (`digital` + `neuro`),
  2. runs size/density/seed sweep with model extrapolation,
  3. emits CSV + markdown + SVG plots,
  4. archives run snapshots under timestamped folders.

## Latest Run

- Command:
  - `scripts/run_matmul_binary_scaling_sweep.sh`
- Run snapshot:
  - `competition/sweeps/matmul_binary_scaling/20260204_092801/`
- Latest artifacts:
  - `competition/sweeps/matmul_binary_scaling_sweep.csv`
  - `competition/analysis/matmul_binary_scaling_summary.md`
  - `competition/analysis/matmul_binary_scaling_energy.svg`
  - `competition/analysis/matmul_binary_scaling_pressure.svg`

## Notes

- This sweep is intentionally marked **model-based**:
  - calibration from verified 2x2 transistor evidence,
  - extrapolation to larger `N` done algorithmically.
- Next hardening step is to add true transistor-run `N>2` checkpoints
  (`N=4`, `N=8`) to tighten model credibility.
