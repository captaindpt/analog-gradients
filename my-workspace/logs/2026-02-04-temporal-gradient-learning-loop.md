# 2026-02-04 - Temporal Gradient Learning Loop (Finite Difference)

## Objective

Implement a concrete clockless-learning workflow where analog circuit
parameters are optimized using measured temporal gradients from transistor
simulations.

## Work Completed

- Added finite-difference trainer:
  - `scripts/train_temporal_gradient_loop.py`
- Added benchmark runner:
  - `scripts/run_temporal_gradient_benchmark.sh`
- Added artifacts + latest pointers:
  - `competition/analysis/temporal_gradient_learning.csv`
  - `competition/analysis/temporal_gradient_trace.csv`
  - `competition/analysis/temporal_gradient_learning_summary.md`
  - `competition/analysis/temporal_gradient_learning_loss.svg`

## Method

- Netlist base: `netlists/neuro_tile4_coupled.scs`
- Trainable knobs in generated training netlists:
  - `r_fb`
  - `rleak`
  - `iin_amp` (mapped to `V_PRE0` pulse amplitude)
- Loss terms per trace:
  - first-spike timing error (MSE)
  - missing-spike penalty
  - ordering penalty
  - optional energy regularization from `V_VDD:p`
- Gradient estimate:
  - central finite difference per normalized parameter

## Latest Run

- Command:
  - `ITERS=6 TRAIN_TRACE_DELAYS_NS=4.5,5.5,7.5 HOLDOUT_TRACE_DELAYS_NS=6.5,9.0,10.5 scripts/run_temporal_gradient_benchmark.sh`
- Archive:
  - `competition/sweeps/temporal_gradient_learning/20260204_155533/`
- Outcome:
  - train objective: `3.008759 -> 2.290754` over 6 iterations
  - holdout objective: `2.991241 -> 2.276373` (generalization gap stayed small: `-0.014381`)
  - final point had no missing/count/order penalties with reachable targets
  - mean train energy term decreased (energy from `134.527 pJ` to `127.563 pJ`).

## Post-Review Fixes Applied

- Targeting:
  - added `target_mode=measured_anchor_shift` so training targets are anchored
    to measured baseline timings of this block, then shifted by configurable deltas.
- Count loss:
  - changed from only `count < 1` penalty to explicit count-mismatch penalty
    (`abs(actual - expected)` per channel).
- Ordering loss:
  - changed from flat inversion penalty to magnitude-sensitive penalty
    (`order_weight * violation^2`) with configurable margin.
- Gradients near bounds:
  - finite-difference denominator now uses actual perturbed span (`x_plus-x_minus`)
    instead of fixed `2*delta`.
- Update dynamics:
  - replaced clip-dominated raw steps with normalized-gradient updates, then
    bounded by max step for safety.
- Energy weighting:
  - replaced near-zero raw lambda with normalized energy term:
    `energy_weight * (energy_pJ / energy_ref_pJ)`.
- Generalization split:
  - added separate train/holdout delay sets and per-iteration holdout-loss
    reporting in summary + CSV.

## Caveat

This is a training-method proof on one analog block. A matched digital temporal
baseline for strict apples-to-apples comparison is still pending.
