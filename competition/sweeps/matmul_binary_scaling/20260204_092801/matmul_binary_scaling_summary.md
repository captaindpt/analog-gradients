# Binary Matmul Scaling Sweep (Model-Based)

This sweep uses calibrated 2x2 transistor measurements and extrapolates
larger NxN binary workloads algorithmically.

Calibration sources:
- Digital: `/home/v71349/analog-gradients/results/matmul2x2_binary_digital_test.txt`
- Neuro: `/home/v71349/analog-gradients/results/matmul2x2_binary_neuro_test.txt`

Calibration values:
- Digital energy/op: `0.004967 pJ/op`
- Digital 2x2 latency: `0.141 ns`
- Neuro 2x2 total energy: `11.202 pJ`
- Neuro 2x2 partial spikes: `5`
- Neuro measured-calibrated energy/spike: `2.240 pJ/spike`
- Neuro spike-model energy/spike: `3.270 pJ/spike`

Sweep setup:
- N list: `2,4,8,12,16`
- density list: `0.10,0.30,0.50,0.80`
- seeds: `1,2,3,4,5`

| N | density | mean active products | mean y_max | digital energy est (pJ) | neuro energy est (pJ) | energy ratio (neuro/digital) |
|---|---------|----------------------|------------|---------------------------|-----------------------|------------------------------|
| 2 | 0.10 | 0.00 | 0.00 | 0.060 | 0.000 | 0.00x |
| 2 | 0.30 | 0.80 | 0.20 | 0.060 | 1.792 | 30.07x |
| 2 | 0.50 | 3.40 | 1.20 | 0.060 | 7.617 | 127.79x |
| 2 | 0.80 | 6.80 | 2.00 | 0.060 | 15.235 | 255.58x |
| 4 | 0.10 | 0.80 | 0.60 | 0.556 | 1.792 | 3.22x |
| 4 | 0.30 | 4.60 | 1.60 | 0.556 | 10.306 | 18.52x |
| 4 | 0.50 | 19.00 | 2.60 | 0.556 | 42.568 | 76.51x |
| 4 | 0.80 | 42.20 | 3.80 | 0.556 | 94.546 | 169.94x |
| 8 | 0.10 | 6.20 | 1.20 | 4.769 | 13.891 | 2.91x |
| 8 | 0.30 | 46.80 | 2.60 | 4.769 | 104.851 | 21.99x |
| 8 | 0.50 | 130.20 | 4.80 | 4.769 | 291.702 | 61.17x |
| 8 | 0.80 | 321.20 | 8.00 | 4.769 | 719.622 | 150.91x |
| 12 | 0.10 | 18.20 | 1.60 | 16.452 | 40.776 | 2.48x |
| 12 | 0.30 | 176.00 | 5.00 | 16.452 | 394.313 | 23.97x |
| 12 | 0.50 | 404.40 | 7.40 | 16.452 | 906.024 | 55.07x |
| 12 | 0.80 | 1110.60 | 11.20 | 16.452 | 2488.206 | 151.24x |
| 16 | 0.10 | 51.60 | 2.00 | 39.421 | 115.605 | 2.93x |
| 16 | 0.30 | 396.00 | 5.00 | 39.421 | 887.205 | 22.51x |
| 16 | 0.50 | 959.60 | 8.60 | 39.421 | 2149.903 | 54.54x |
| 16 | 0.80 | 2592.80 | 14.80 | 39.421 | 5808.951 | 147.36x |

Interpretation notes:
- Digital model scales with operation count `N^2(2N-1)` and logic-depth proxy `ceil(log2 N)`.
- Neuro model scales with event count (`active_products`) and membrane fan-in (`N`).
- This is an extrapolation aid for architecture discussion; it is not a full transistor NxN run.

Artifacts:
- CSV: `/home/v71349/analog-gradients/competition/sweeps/matmul_binary_scaling/20260204_092801/matmul_binary_scaling_sweep.csv`
- Energy plot: `/home/v71349/analog-gradients/competition/sweeps/matmul_binary_scaling/20260204_092801/matmul_binary_scaling_energy.svg`
- Pressure plot: `/home/v71349/analog-gradients/competition/sweeps/matmul_binary_scaling/20260204_092801/matmul_binary_scaling_pressure.svg`
