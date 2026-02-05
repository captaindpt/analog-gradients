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
  - `ITERS=4 ENERGY_WEIGHT=0.03 scripts/run_temporal_gradient_benchmark.sh`
- Archive:
  - `competition/sweeps/temporal_gradient_learning/20260204_183829/`
- Outcome:
  - absolute-target objective: `0.098085 -> 0.095554` over 4 iterations
  - holdout objective: `0.096863 -> 0.095044` (gap: `-0.000510`)
  - final point had no missing/count/order penalties
  - term mix stayed timing-dominant (`~68.6% timing`, `~31.4% energy`).
  - summary now explicitly labels claim scope as method demo.

## Post-Review Fixes Applied

- Targeting:
  - default mode switched to `target_mode=absolute` for headline runs.
  - `measured_anchor_shift` retained for development/debug.
  - default absolute targets set to measured coupled-tile regime
    (`9.388,11.896,12.985,13.640 ns` at base delay).
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
  - added optional schedule (`--energy-weight-start/--energy-weight-end`) and
    per-iteration contribution percentages in reports.
- Generalization split:
  - added separate train/holdout delay sets and per-iteration holdout-loss
    reporting in summary + CSV.
  - anchor probing now defaults to train-only delays (`anchor_probe_split=train`)
    to prevent holdout leakage in adaptive-target mode.
- Runtime robustness:
  - fixed relative `--out-dir` handling (Spectre netlist path + out-dir normalization)
    so direct trainer invocation works from relative and absolute output paths.

## Penalty Stress Checks (Post-Hardening)

- Count-penalty activation run:
  - command: `... --target-spike-counts 1,1,1,1 --iters 1`
  - archive:
    `competition/sweeps/temporal_gradient_learning/20260204_185340_count_stress3/`
  - result: count penalty active (`672.0`) and dominates objective as expected.
- Order-penalty activation run:
  - command: `... --order-margin-ns 5.0 --iters 1`
  - archive:
    `competition/sweeps/temporal_gradient_learning/20260204_185702_order_stress/`
  - result: order penalty active (`~1481.4`) and reduced after one update.

## Caveat

This is a training-method proof on one analog block. A matched digital temporal
baseline for strict apples-to-apples comparison is still pending.
