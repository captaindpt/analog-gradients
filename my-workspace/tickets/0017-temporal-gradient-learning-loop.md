# 0017: Temporal Gradient Learning Loop (Clockless Compute)

**Status:** In Progress  
**Priority:** High  
**Created:** 2026-02-04

## Description

Build a reproducible finite-difference learning loop that tunes physical
circuit parameters to match temporal spike targets.

Primary goal: demonstrate a concrete "analog gradients" workflow where
parameter updates are driven by measured timing loss from transistor runs.

## Tasks

- [x] Add finite-difference training script for temporal targets
- [x] Add benchmark runner wrapper with run manifests and latest artifacts
- [x] Generate first training run artifacts (CSV + summary + plot)
- [x] Add stronger multi-trace training batch (+ holdout split)
- [ ] Add multi-pattern training batch (beyond delay-only variation)
- [ ] Add digital temporal-detector baseline for strict apples-to-apples comparison

## Acceptance Criteria

1. Scripted run produces deterministic artifacts from command line.
2. Loss is explicitly decomposed (timing + penalties + optional energy).
3. Parameter updates and gradients are logged per iteration.
4. Results include per-trace first-spike metrics and target references.

## Latest Progress (2026-02-04)

- Added trainer:
  - `scripts/train_temporal_gradient_loop.py`
- Added runner:
  - `scripts/run_temporal_gradient_benchmark.sh`
- Hardened learning objective after review:
  - promoted `target_mode=absolute` as default for headline runs
  - kept `target_mode=measured_anchor_shift` as explicit dev/debug mode
  - default absolute targets now come from measured coupled-tile verification regime
  - count penalty now uses absolute count mismatch vs expected counts
  - ordering penalty now scales with inversion magnitude squared
  - finite-difference gradient denominator now uses actual perturbed span at bounds
  - update rule now uses normalized gradients (avoids repeated clip-dominated steps)
  - energy term now uses normalized weight/reference (no longer negligible by default)
  - added optional energy-weight schedule (`energy_weight_start/end`)
  - added per-term contribution percentages (timing/count/order/energy) in CSV + summary
- Added train/holdout generalization split:
  - independent `train_trace_delays` and `holdout_trace_delays`
  - per-iteration holdout loss logging in eval CSV + summary
  - anchor probe now defaults to train-only delays (`anchor_probe_split=train`)
    to avoid holdout leakage in `measured_anchor_shift` mode
- Ran extended benchmark with stronger trace batch:
  - command:
    `ITERS=6 TRAIN_TRACE_DELAYS_NS=4.5,5.5,7.5 HOLDOUT_TRACE_DELAYS_NS=6.5,9.0,10.5 scripts/run_temporal_gradient_benchmark.sh`
  - archive:
    `competition/sweeps/temporal_gradient_learning/20260204_155533/`
  - result:
    - train loss `3.008759 -> 2.290754`
    - holdout loss `2.991241 -> 2.276373`
    - final gap (holdout-train): `-0.014381`
    - penalties stayed zero at final point (no missing/count/order failures)
- Latest artifacts:
  - `competition/analysis/temporal_gradient_learning.csv`
  - `competition/analysis/temporal_gradient_trace.csv`
  - `competition/analysis/temporal_gradient_learning_summary.md`
  - `competition/analysis/temporal_gradient_learning_loss.svg`
- Latest run archive:
  - `competition/sweeps/temporal_gradient_learning/20260204_183829/`
- Current outcome:
  - absolute-target run (`ENERGY_WEIGHT=0.03`) reduced objective with blind holdout:
    - train `0.098085 -> 0.095554`
    - holdout `0.096863 -> 0.095044`
  - latest run shows timing-dominant contribution (`~69% timing / ~31% energy`)
  - no missing-spike, count-mismatch, or ordering penalties in latest final point.
- Penalty activation stress checks (to verify hardening is exercised):
  - count mismatch stress (`target_spike_counts=1,1,1,1`):
    `competition/sweeps/temporal_gradient_learning/20260204_185340_count_stress3/`
    (count penalty active at `672.0`).
  - order stress (`order_margin_ns=5.0`):
    `competition/sweeps/temporal_gradient_learning/20260204_185702_order_stress/`
    (order penalty active at `1481.4` and reduced after one update).

## Notes

- Current implementation uses `neuro_tile4_coupled` with trainable
  `r_fb`, `rleak`, and an input-drive amplitude knob (`iin_amp` mapped to
  `V_PRE0` pulse level in generated training netlists).
- This is a training-method proof step, not yet a full learning benchmark
  against a matched digital temporal detector.
