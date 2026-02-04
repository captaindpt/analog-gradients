# Matmul4x4 Sparse Crossover Sweep (Measured)

Source CSV: `/home/v71349/analog-gradients/competition/sweeps/matmul4x4_crossover/20260204_133053/matmul4x4_crossover.csv`

| density | points | mean ratio (neuro/digital) | std ratio | neuro wins (ratio<1) | mean active products |
|---------|--------|----------------------------|-----------|----------------------|----------------------|
| 0.040 | 2 | 12490.304 | 11960.361 | 0/2 | 1.000 |
| 0.060 | 2 | 13336.783 | 12806.840 | 0/2 | 1.000 |

Crossover estimate (linear interpolation on mean ratio):
- No crossing within sampled density range.

Notes:
- This sweep is transistor-measured at `N=4` for both architectures.
- `ratio<1` means neuro consumes less total energy than digital for that point.
