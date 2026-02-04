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
- density list: `0.01,0.02,0.03,0.04,0.05,0.06,0.08,0.10`
- seeds: `1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60`

| N | density | mean active products | mean y_max | digital energy est (pJ) | neuro energy est (pJ) | energy ratio (neuro/digital) |
|---|---------|----------------------|------------|---------------------------|-----------------------|------------------------------|
| 2 | 0.01 | 0.00 | 0.00 | 0.060 | 0.000 | 0.00x |
| 2 | 0.02 | 0.00 | 0.00 | 0.060 | 0.000 | 0.00x |
| 2 | 0.03 | 0.00 | 0.00 | 0.060 | 0.000 | 0.00x |
| 2 | 0.04 | 0.00 | 0.00 | 0.060 | 0.000 | 0.00x |
| 2 | 0.05 | 0.00 | 0.00 | 0.060 | 0.000 | 0.00x |
| 2 | 0.06 | 0.02 | 0.02 | 0.060 | 0.037 | 0.63x |
| 2 | 0.08 | 0.00 | 0.00 | 0.060 | 0.000 | 0.00x |
| 2 | 0.10 | 0.05 | 0.05 | 0.060 | 0.112 | 1.88x |
| 4 | 0.01 | 0.02 | 0.02 | 0.556 | 0.037 | 0.07x |
| 4 | 0.02 | 0.00 | 0.00 | 0.556 | 0.000 | 0.00x |
| 4 | 0.03 | 0.05 | 0.05 | 0.556 | 0.112 | 0.20x |
| 4 | 0.04 | 0.05 | 0.05 | 0.556 | 0.112 | 0.20x |
| 4 | 0.05 | 0.10 | 0.10 | 0.556 | 0.224 | 0.40x |
| 4 | 0.06 | 0.23 | 0.20 | 0.556 | 0.523 | 0.94x |
| 4 | 0.08 | 0.45 | 0.32 | 0.556 | 1.008 | 1.81x |
| 4 | 0.10 | 0.58 | 0.42 | 0.556 | 1.307 | 2.35x |
| 8 | 0.01 | 0.10 | 0.10 | 4.769 | 0.224 | 0.05x |
| 8 | 0.02 | 0.33 | 0.25 | 4.769 | 0.747 | 0.16x |
| 8 | 0.03 | 0.30 | 0.25 | 4.769 | 0.672 | 0.14x |
| 8 | 0.04 | 0.80 | 0.48 | 4.769 | 1.792 | 0.38x |
| 8 | 0.05 | 1.18 | 0.55 | 4.769 | 2.651 | 0.56x |
| 8 | 0.06 | 2.33 | 0.85 | 4.769 | 5.228 | 1.10x |
| 8 | 0.08 | 3.55 | 1.03 | 4.769 | 7.953 | 1.67x |
| 8 | 0.10 | 5.02 | 1.12 | 4.769 | 11.239 | 2.36x |
| 12 | 0.01 | 0.15 | 0.12 | 16.452 | 0.336 | 0.02x |
| 12 | 0.02 | 0.72 | 0.48 | 16.452 | 1.606 | 0.10x |
| 12 | 0.03 | 2.02 | 0.78 | 16.452 | 4.518 | 0.27x |
| 12 | 0.04 | 2.80 | 0.88 | 16.452 | 6.273 | 0.38x |
| 12 | 0.05 | 4.38 | 1.05 | 16.452 | 9.820 | 0.60x |
| 12 | 0.06 | 6.00 | 1.00 | 16.452 | 13.442 | 0.82x |
| 12 | 0.08 | 12.10 | 1.42 | 16.452 | 27.109 | 1.65x |
| 12 | 0.10 | 17.17 | 1.53 | 16.452 | 38.460 | 2.34x |
| 16 | 0.01 | 0.30 | 0.27 | 39.421 | 0.672 | 0.02x |
| 16 | 0.02 | 2.00 | 0.78 | 39.421 | 4.481 | 0.11x |
| 16 | 0.03 | 3.25 | 0.92 | 39.421 | 7.281 | 0.18x |
| 16 | 0.04 | 6.08 | 1.03 | 39.421 | 13.629 | 0.35x |
| 16 | 0.05 | 9.72 | 1.18 | 39.421 | 21.769 | 0.55x |
| 16 | 0.06 | 14.70 | 1.33 | 39.421 | 32.934 | 0.84x |
| 16 | 0.08 | 25.20 | 1.63 | 39.421 | 56.458 | 1.43x |
| 16 | 0.10 | 38.98 | 1.93 | 39.421 | 87.339 | 2.22x |

Interpretation notes:
- Digital model scales with operation count `N^2(2N-1)` and logic-depth proxy `ceil(log2 N)`.
- Neuro model scales with event count (`active_products`) and membrane fan-in (`N`).
- This is an extrapolation aid for architecture discussion; it is not a full transistor NxN run.

Artifacts:
- CSV: `/home/v71349/analog-gradients/competition/sweeps/matmul_binary_scaling/20260204_132044/matmul_binary_scaling_sweep.csv`
- Energy plot: `/home/v71349/analog-gradients/competition/sweeps/matmul_binary_scaling/20260204_132044/matmul_binary_scaling_energy.svg`
- Pressure plot: `/home/v71349/analog-gradients/competition/sweeps/matmul_binary_scaling/20260204_132044/matmul_binary_scaling_pressure.svg`
