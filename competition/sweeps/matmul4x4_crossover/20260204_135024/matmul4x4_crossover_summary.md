# Matmul4x4 Sparse Crossover Sweep (Measured)

Source CSV: `/home/v71349/analog-gradients/competition/sweeps/matmul4x4_crossover/20260204_135024/matmul4x4_crossover.csv`

| density | points | mean ratio (all points) | mean ratio (active>0) | neuro wins (active>0) | mean active products |
|---------|--------|-------------------------|-------------------------|----------------------|----------------------|
| 0.010 | 4 | 0.184 | n/a | n/a | 0.000 |
| 0.020 | 4 | 0.172 | n/a | n/a | 0.000 |
| 0.030 | 4 | 29.656 | 118.140 | 0/1 | 0.500 |
| 0.040 | 4 | 62.227 | 124.295 | 0/2 | 0.750 |
| 0.050 | 4 | 62.227 | 124.295 | 0/2 | 0.750 |
| 0.060 | 4 | 62.221 | 124.295 | 0/2 | 0.750 |
| 0.080 | 4 | 51.076 | 102.030 | 0/2 | 1.000 |
| 0.100 | 4 | 80.861 | 107.778 | 0/3 | 1.500 |

Crossover estimate (linear interpolation on mean ratio, active-products-only):
- No crossing within sampled density range.

Notes:
- This sweep is transistor-measured at `N=4` for both architectures.
- `ratio<1` means neuro consumes less total energy than digital for that point.
- Active-products-only statistics exclude trivial `Y=0` points (no useful multiply events).
