# Matmul4x4 Sparse Crossover Sweep (Measured)

Source CSV: `/home/v71349/analog-gradients/competition/sweeps/matmul4x4_crossover/20260204_133308/matmul4x4_crossover.csv`

| density | points | mean ratio (neuro/digital) | std ratio | neuro wins (ratio<1) | mean active products |
|---------|--------|----------------------------|-----------|----------------------|----------------------|
| 0.010 | 4 | 2430.409 | 4209.251 | 3/4 | 0.000 |
| 0.020 | 4 | 4870.211 | 4870.032 | 2/4 | 0.000 |
| 0.030 | 4 | 7208.732 | 7670.187 | 1/4 | 0.500 |
| 0.040 | 4 | 6363.047 | 10444.911 | 1/4 | 0.750 |
| 0.050 | 4 | 6363.047 | 10444.911 | 1/4 | 0.750 |
| 0.060 | 4 | 6786.286 | 11177.850 | 1/4 | 0.750 |
| 0.080 | 4 | 9187.838 | 10507.095 | 0/4 | 1.000 |
| 0.100 | 4 | 5903.968 | 9205.627 | 0/4 | 1.500 |

Crossover estimate (linear interpolation on mean ratio):
- No crossing within sampled density range.

Notes:
- This sweep is transistor-measured at `N=4` for both architectures.
- `ratio<1` means neuro consumes less total energy than digital for that point.
