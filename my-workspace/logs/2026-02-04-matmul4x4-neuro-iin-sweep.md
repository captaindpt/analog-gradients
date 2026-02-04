# 2026-02-04 - Matmul4x4 Neuro `iin_amp` Sweep (Sparse Fixed Point)

## Objective

Probe whether tuning neuro input-current amplitude can close the measured
energy gap at a sparse 4x4 checkpoint point (`density=0.06`, `seed=1`).

## Work Completed

- Added sweep script:
  - `scripts/sweep_matmul4x4_neuro_iin.sh`
- Script flow:
  1. generate sparse checkpoint matrices,
  2. measure digital baseline once,
  3. sweep neuro `iin_amp`,
  4. record PASS/FAIL + energy/latency/spike metrics,
  5. restore default checkpoint assets.

## Latest Results

Artifacts:

- `competition/analysis/matmul4x4_neuro_iin_sweep.csv`
- `competition/analysis/matmul4x4_neuro_iin_sweep_summary.md`

Observed behavior:

- Digital sparse fixed-point energy: `~0.0323 pJ`.
- Neuro energy decreases as `iin_amp` decreases, but decode fails for all
  tested values below `220u` (spikes collapse to zero).
- Best passing point remained:
  - `iin_amp=220u`, neuro energy `~3.82 pJ`,
  - ratio vs digital `~118.2x` (neuro worse on this metric).

## Implication

Parameter tuning alone is insufficient. Achieving energy crossover requires
architecture-level overhead reduction while preserving decode correctness.
