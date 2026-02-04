# 2026-02-04 - Matmul4x4 Sparse Crossover Sweep (Measured)

## Objective

Validate the predicted low-density energy crossover with transistor-measured
`N=4` runs (digital vs neuro), instead of model-only extrapolation.

## Work Completed

- Added sparse sweep harness:
  - `scripts/run_matmul4x4_crossover_sweep.sh`
- Extended checkpoint generator for random sparse stimuli:
  - `scripts/generate_matmul4x4_checkpoint_assets.py`
  - new args: `--density`, `--seed`, `--metadata-out`
- Added measured sweep artifacts:
  - `competition/sweeps/matmul4x4_crossover/matmul4x4_crossover.csv`
  - `competition/analysis/matmul4x4_crossover_summary.md`

## Latest Measured Sweep (run 20260204_133308)

- Density points: `p = 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01`
- Seeds: `1..4`
- Scope: transistor runs for both architectures per point

### Key Outcome

- **No active-point crossover observed** in sampled range.
- Active-point neuro/digital energy ratio remains very high (O(10^2-10^3)).
- Trivial all-zero output points can show ratio<1 due near-zero energy in both
  paths, so report now separates active-product-only statistics.

## Implication

The simple spike-count energy model underestimates neuro overhead in sparse
regime. Next optimization work should target static/event overhead reduction
before expecting energy crossover on this matmul primitive.
