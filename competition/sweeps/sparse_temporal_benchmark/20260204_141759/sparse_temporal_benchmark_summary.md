# Sparse Temporal Event Benchmark (Trace-Driven, Calibrated)

Goal: compare digital vs neuro on **energy per correct event** under fixed quality gates.

Calibration sources:
- Energy windows (active/idle): `/home/v71349/analog-gradients/competition/sweeps/matmul4x4_crossover/matmul4x4_crossover.csv`
- Neuro temporal detection quality: `/home/v71349/analog-gradients/results/coincidence_detector_test.txt`

Window-energy calibration (measured):

| Regime | Digital (pJ/window) | Neuro (pJ/window) | Neuro/Digital |
|--------|----------------------|-------------------|---------------|
| Active | 0.029817 | 3.339743 | 112.009x |
| Idle | 0.000332 | 0.000050 | 0.151x |

Quality-gate setup:
- min recall: `0.990`
- max false-positive rate: `0.0100`
- max latency: `15.000 ns`
- digital quality model: recall=`1.000`, FPR=`0.0000`, latency=`0.152 ns`
- neuro quality from coincidence test: recall=`1.000`, FPR=`0.0000`, latency=`12.229 ns`

| Active fraction | Digital energy (pJ) | Neuro energy (pJ) | Ratio (N/D) | Digital pJ/TP | Neuro pJ/TP | Quality pass (D/N) |
|-----------------|---------------------|-------------------|-------------|---------------|-------------|--------------------|
| 0.0010% | 332.324 | 83.440 | 0.251x | 33.232 | 8.344 | 1/1 |
| 0.0030% | 332.913 | 150.234 | 0.451x | 11.097 | 5.008 | 1/1 |
| 0.0100% | 334.977 | 384.012 | 1.146x | 3.350 | 3.840 | 1/1 |
| 0.0300% | 340.874 | 1051.951 | 3.086x | 1.136 | 3.507 | 1/1 |
| 0.1000% | 361.514 | 3389.736 | 9.377x | 0.362 | 3.390 | 1/1 |
| 0.3000% | 420.483 | 10069.121 | 23.947x | 0.140 | 3.356 | 1/1 |
| 1.0000% | 626.876 | 33446.971 | 53.355x | 0.063 | 3.345 | 1/1 |
| 3.0000% | 1216.572 | 100240.827 | 82.396x | 0.041 | 3.341 | 1/1 |
| 10.0000% | 3280.505 | 334019.322 | 101.819x | 0.033 | 3.340 | 1/1 |

Crossover result:
- Estimated `ratio=1` active-fraction crossover: `0.00008526` (`0.0085%` active windows, `99.9915%` idle windows).

Interpretation:
- Neuro wins only when traces are extremely idle; digital wins once active windows are frequent.
- This benchmark is trace-driven and calibrated from measured transistor data, not a direct transistor detector-vs-detector netlist pair.

Artifacts:
- CSV: `/home/v71349/analog-gradients/competition/sweeps/sparse_temporal_benchmark/20260204_141759/sparse_temporal_benchmark.csv`
- Ratio plot: `/home/v71349/analog-gradients/competition/sweeps/sparse_temporal_benchmark/20260204_141759/sparse_temporal_benchmark_ratio.svg`
- Energy/TP plot: `/home/v71349/analog-gradients/competition/sweeps/sparse_temporal_benchmark/20260204_141759/sparse_temporal_benchmark_eptp.svg`
