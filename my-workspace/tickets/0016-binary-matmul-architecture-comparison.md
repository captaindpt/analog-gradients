# 0016: Binary 2x2 Matmul Architecture Comparison

**Status:** In Progress
**Priority:** High
**Created:** 2026-02-04

## Description

Build a reproducible proof demo that runs the same binary 2x2 matmul task on:

1. a clocked digital baseline, and
2. the neuromorphic spike/integration path.

Goal is a defensible comparison of correctness, latency, and energy.

## Tasks

- [x] Add reference spec for binary matmul comparison method
- [x] Implement neuro binary 2x2 matmul netlist + verifier
- [x] Integrate neuro target into `build.sh`
- [x] Implement digital binary 2x2 matmul baseline + verifier
- [x] Add matched energy extraction for both architectures
- [x] Publish side-by-side comparison summary under `competition/analysis/`
- [x] Add matrix-size scaling sweep harness (`N=2..16`, density/seed sweep)
- [x] Generate scaling plots + markdown summary for architecture discussion
- [x] Add transistor-run 4x4 checkpoint netlists + verifiers (digital + neuro)
- [x] Publish side-by-side 4x4 checkpoint comparison report
- [x] Add sparse-density 4x4 transistor crossover sweep harness
- [x] Run low-density measured sweep and publish crossover report
- [x] Add sparse fixed-point neuro-parameter sweep (`iin_amp`) for efficiency probing
- [x] Add sparse temporal event benchmark with fixed quality gates (energy/event)

## Acceptance Criteria

1. Both architectures compute the same binary 2x2 workload with deterministic
   PASS/FAIL verification.
2. Energy and latency are reported using explicit, reproducible methods.
3. Final report states scope limits clearly (binary-only first proof).

## Latest Progress (2026-02-04)

- Added neuro binary matmul netlist:
  - `netlists/matmul2x2_binary_neuro.scs`
- Added verifier:
  - `ocean/test_matmul2x2_binary_neuro.ocn`
- Added build target:
  - `./build.sh matmul2x2_binary_neuro`
  - included in `./build.sh all`
- First PASS run:
  - `results/matmul2x2_binary_neuro_test.txt`
  - `results/_runlogs/build_matmul2x2_binary_neuro_20260203_212412.manifest.txt`
- Added digital binary matmul baseline:
  - `netlists/matmul2x2_binary_digital.scs`
  - `ocean/test_matmul2x2_binary_digital.ocn`
  - `./build.sh matmul2x2_binary_digital` (included in `./build.sh all`)
- Added side-by-side run script:
  - `scripts/run_matmul2x2_binary_comparison.sh`
- Latest comparison artifacts:
  - `competition/analysis/matmul2x2_binary_comparison.md`
  - `competition/analysis/matmul2x2_binary_comparison.csv`

## Open Follow-Up

- Upgrade digital baseline from minimal combinational netlist to a clocked
  PE/GPU-core-linked workload harness for a stricter apples-to-apples comparison.
- Move from 4x4 checkpoint to at least one additional transistor-run larger point
  (`N=8`) for calibration hardening.
- Reduce neuro static/event overhead enough to approach measured crossover
  (current 4x4 sparse sweep shows no active-point crossover).
- Add architecture-level energy reductions (e.g., comparator elimination/gating)
  so sparse points remain correct while reducing baseline neuro energy by orders
  of magnitude.

## Latest Progress (2026-02-04, scaling sweep)

- Added model-based scaling scripts:
  - `scripts/run_matmul_binary_scaling_sweep.sh`
  - `scripts/analyze_matmul_binary_scaling.py`
- New latest artifacts:
  - `competition/sweeps/matmul_binary_scaling_sweep.csv`
  - `competition/analysis/matmul_binary_scaling_summary.md`
  - `competition/analysis/matmul_binary_scaling_energy.svg`
  - `competition/analysis/matmul_binary_scaling_pressure.svg`
- Run snapshots now archived per run:
  - `competition/sweeps/matmul_binary_scaling/<timestamp>/...`

## Latest Progress (2026-02-04, 4x4 transistor checkpoint)

- Added generated checkpoint assets:
  - `netlists/matmul4x4_binary_digital.scs`
  - `netlists/matmul4x4_binary_neuro.scs`
  - `ocean/test_matmul4x4_binary_digital.ocn`
  - `ocean/test_matmul4x4_binary_neuro.ocn`
  - `scripts/generate_matmul4x4_checkpoint_assets.py`
- Added reproducible comparison runner:
  - `scripts/run_matmul4x4_binary_comparison.sh`
- Added build targets:
  - `./build.sh matmul4x4_binary_digital`
  - `./build.sh matmul4x4_binary_neuro`
- Published measured comparison artifacts:
  - `competition/analysis/matmul4x4_binary_comparison.md`
  - `competition/analysis/matmul4x4_binary_comparison.csv`

## Latest Progress (2026-02-04, 4x4 sparse crossover sweep)

- Added sparse sweep runner:
  - `scripts/run_matmul4x4_crossover_sweep.sh`
- Extended checkpoint generator:
  - `scripts/generate_matmul4x4_checkpoint_assets.py`
    - now supports `--density`, `--seed`, and metadata export.
- Published measured sparse sweep artifacts:
  - `competition/sweeps/matmul4x4_crossover/matmul4x4_crossover.csv`
  - `competition/analysis/matmul4x4_crossover_summary.md`
- Current measured outcome:
  - no crossover observed for active-product points in sampled range
    (`p=0.03..0.10`, `N=4`, 4 seeds in latest run);
  - active-point neuro/digital energy ratio remains O(10^2).

## Latest Progress (2026-02-04, sparse-point neuro tuning sweep)

- Added sweep runner:
  - `scripts/sweep_matmul4x4_neuro_iin.sh`
- Latest artifacts:
  - `competition/analysis/matmul4x4_neuro_iin_sweep.csv`
  - `competition/analysis/matmul4x4_neuro_iin_sweep_summary.md`
- Current measured outcome:
  - reducing `iin_amp` lowers neuro energy, but decode correctness fails before
    parity with digital baseline at the sparse fixed point;
  - best passing setting in latest run remained `iin_amp=220u`, still with
    large energy gap vs digital (O(10^2) ratio).

## Latest Progress (2026-02-04, neuro product-gated source optimization)

- Updated 4x4 neuro generator to gate product-drive current by binary product
  term (`a*b`) instead of independent per-input injection.
- Revalidated checkpoint + sweep targets:
  - `./build.sh matmul2x2_binary_neuro` ✅
  - `./build.sh matmul4x4_binary_neuro` ✅
  - `scripts/run_matmul4x4_binary_comparison.sh` ✅
  - `scripts/run_matmul4x4_crossover_sweep.sh` ✅
- Measured effect at dense 4x4 checkpoint:
  - neuro energy reduced from `~76.66 pJ` to `~53.38 pJ` (same correctness).
- Sparse active-point gap remains large (latest sweep: active-point ratio
  still roughly O(10^2)); no active-point crossover observed yet.

## Latest Progress (2026-02-04, sparse temporal benchmark)

- Added quality-gated sparse benchmark runner:
  - `scripts/run_sparse_temporal_benchmark.sh`
  - `scripts/analyze_sparse_temporal_benchmark.py`
- Benchmark metric:
  - energy per true positive (`pJ/TP`) under fixed gates:
    - recall `>=0.99`
    - FPR `<=0.01`
    - latency `<=15ns`
- Calibration sources:
  - active/idle window energy from measured 4x4 crossover CSV
  - neuro temporal quality/latency from `results/coincidence_detector_test.txt`
- Published artifacts:
  - `competition/analysis/sparse_temporal_benchmark_summary.md`
  - `competition/analysis/sparse_temporal_benchmark.csv`
  - `competition/analysis/sparse_temporal_benchmark_ratio.svg`
  - `competition/analysis/sparse_temporal_benchmark_eptp.svg`
- Current calibrated result:
  - estimated crossover remains deep idle (`~0.0085%` active windows).
