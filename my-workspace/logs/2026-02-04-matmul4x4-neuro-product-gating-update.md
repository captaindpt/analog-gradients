# 2026-02-04 - Matmul4x4 Neuro Product-Gating Update

## Objective

Reduce neuro-path wasted activity by gating per-product current injection on
binary product terms (`a*b`) instead of independent per-input injection.

## Change

- Updated generator:
  - `scripts/generate_matmul4x4_checkpoint_assets.py`
- Neuro product source emitted as:
  - `val1=(a_ik*b_kj)*(2*iin_amp)`
  - preserves nominal active-product drive while suppressing single-input-only
    charge injection.

## Validation

Executed and passed:

- `./build.sh matmul2x2_binary_digital`
- `./build.sh matmul2x2_binary_neuro`
- `./build.sh matmul4x4_binary_digital`
- `./build.sh matmul4x4_binary_neuro`

Also re-ran:

- `scripts/run_matmul4x4_binary_comparison.sh`
- `scripts/run_matmul4x4_crossover_sweep.sh` (latest run: `20260204_135024`)

## Result Snapshot

- Dense 4x4 checkpoint neuro energy:
  - before: `~76.66 pJ`
  - after:  `~53.38 pJ`
- Correctness unchanged (PASS for both digital and neuro checkpoint tests).
- Sparse active-point crossover still not observed in latest measured sweep.
