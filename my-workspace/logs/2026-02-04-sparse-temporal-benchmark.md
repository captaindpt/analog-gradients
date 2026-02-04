# 2026-02-04 - Sparse Temporal Benchmark (Quality-Gated)

## Objective

Add a metric-driven benchmark where neuromorphic value is expected:
energy per true-positive event under explicit quality gates
(recall/FPR/latency), using measured calibrations.

## Work Completed

- Added benchmark analysis script:
  - `scripts/analyze_sparse_temporal_benchmark.py`
- Added benchmark runner:
  - `scripts/run_sparse_temporal_benchmark.sh`
- Added regenerated artifacts:
  - `competition/analysis/sparse_temporal_benchmark_summary.md`
  - `competition/analysis/sparse_temporal_benchmark.csv`
  - `competition/analysis/sparse_temporal_benchmark_ratio.svg`
  - `competition/analysis/sparse_temporal_benchmark_eptp.svg`

## Calibration Inputs

- Active/idle energy windows from measured matmul crossover:
  - `competition/sweeps/matmul4x4_crossover/matmul4x4_crossover.csv`
- Neuro temporal quality and latency from coincidence detector result:
  - `results/coincidence_detector_test.txt`

## Quality Gates

- Recall `>= 0.99`
- False-positive rate `<= 0.01`
- Latency `<= 15 ns`

## Latest Result (run 20260204_141759)

- Estimated neuro/digital energy crossover at:
  - active fraction `~0.00008526` (`~0.0085%` active windows)
- Interpretation:
  - neuro wins only in ultra-idle duty cycle regimes;
  - digital dominates once active windows become frequent.

## Scope Caveat

This benchmark is calibrated from measured transistor artifacts and trace-level
quality checks; it is not yet a direct matched transistor detector-vs-detector
pair for both architectures.
