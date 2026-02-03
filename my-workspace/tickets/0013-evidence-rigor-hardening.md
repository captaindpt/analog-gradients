# 0013: Evidence Rigor Hardening

**Status:** Completed
**Priority:** High
**Created:** 2026-02-02

## Description

Now that build/test auditability is fail-closed and reproducible, harden the
founder-evidence track so claims are quantitatively robust and not overfit to
coarse measurement windows.

## Tasks

- [x] Expand coupled-tile sweep granularity (`r_fb`, `rleak`) and preserve full raw traces per sweep point
- [x] Increase transient/time-resolution where needed to reduce 0.5ns quantization effects
- [x] Add slope fit-quality and uncertainty outputs (R2 + CI95 + quantization diagnostics)
- [x] Rework ODE fitting into phase-aware model(s) and report both local and global fit quality
- [x] Add uncertainty reporting (multi-run or bootstrap) for energy-per-spike estimates
- [x] Update competition evidence docs with explicit confidence/limitation statements

## Latest Progress (2026-02-02)

- Upgraded sweep grid to `r_fb={600,700,800,900,1000,1100,1200,1300,1500}` and
  `rleak={5M,6M,7M,8M,9M,10M,12M}` (63 points).
- Added per-point raw/log/result archive under:
  `results/neuro_tile4_coupled/sweeps/20260202_215026/`
- Added sweep run manifest:
  `results/neuro_tile4_coupled/sweeps/20260202_215026/sweep_manifest.txt`
- Increased timing extraction fidelity in OCEAN (`100ps` sampling +
  interpolated crossing timestamps with `%.3f ns` output).
- Refreshed temporal sensitivity analysis with per-rleak fit metrics:
  - slope `dt_spike/dr_fb`
  - `R2`
  - 95% CI for slope
  - min nonzero timing-step diagnostic
- New analysis artifacts:
  - `competition/analysis/temporal_sensitivity_slopes.csv`
  - `competition/analysis/temporal_sensitivity_summary.md`
- Added phase-aware ODE fit + baseline comparison:
  - `competition/analysis/lif_ode_fit_summary.md`
  - `competition/analysis/lif_ode_fit_trace.csv`
- Added energy uncertainty artifacts:
  - `competition/analysis/lif_energy_trace.csv`
  - `competition/analysis/lif_energy_bootstrap.csv`
  - `competition/analysis/lif_energy_summary.md`

## Latest Progress (2026-02-03)

- Hardened `build.sh` for fail-closed auditability:
  - `set -euo pipefail`
  - stale `.raw` + `*_test.txt` deletion before each component run
  - fresh raw/result timestamp checks required for PASS
  - timestamped run logs/manifests under `results/_runlogs/`
- Verified hardened full regression:
  - `./build.sh all` PASS
  - manifest: `results/_runlogs/build_all_20260202_224417.manifest.txt`
- Added corner-conditioned founder-evidence runner:
  - `scripts/run_lif_corner_evidence.sh`
  - extractor: `ocean/extract_lif_corner_metrics.ocn`
  - analyzers: `scripts/analyze_lif_ode_fit.py`, `scripts/analyze_lif_energy_trace.py`
- Completed 9-corner LIF sweep:
  - run root: `competition/analysis/lif_corners/20260202_224254/`
  - summary: `competition/analysis/lif_corners/20260202_224254/lif_corner_summary.md`

## Latest Progress (2026-02-03, Audit Follow-up)

- Hardened false-pass prevention in `build.sh`:
  - requires exactly one terminal `=== PASS|FAIL:` verdict line
  - fails on any `FAIL:` / `[FAIL]` / `ERROR:` markers in result text
- Expanded top-level digital checks from PE0 spot checks to full-array checks:
  - `ocean/test_pe4.ocn`
  - `ocean/test_gpu_core.ocn`
- Promoted prior warning-only behaviors to hard failures in analog tests:
  - `ocean/test_synapse.ocn`
  - `ocean/test_lif_neuron.ocn`
  - `ocean/test_coincidence_detector.ocn`
  - `ocean/test_xor_spike2.ocn`
- Revalidated with full regression under strict criteria:
  - `./build.sh all` PASS
  - manifest: `results/_runlogs/build_all_20260203_121041.manifest.txt`

## Latest Progress (2026-02-03, Fake-Pass Follow-up)

- Fixed OCEAN helper syntax regression in top-level digital tests:
  - `ocean/test_pe4.ocn`
  - `ocean/test_gpu_core.ocn`
- Hardened build harness against OCEAN runtime script failures:
  - any `*Error*` marker in `results/<component>/ocean.log` now fails verification
- Removed machine-locked absolute paths across OCEAN scripts:
  - switched to repo-relative `results/...` paths
- Revalidated:
  - `./build.sh pe4` PASS
  - `./build.sh gpu_core` PASS
  - `./build.sh all` PASS
  - manifest: `results/_runlogs/build_all_20260203_122255.manifest.txt`

## Latest Progress (2026-02-03, Strict Warning Gate)

- Enabled strict Spectre warning policy in `build.sh`:
  - known model/convergence/accuracy warning classes in `spectre.log` are now fatal
- Validation:
  - `bash -n build.sh` PASS
  - `./build.sh pe4` now FAILS as expected under strict policy
- Next implication:
  - model and convergence warning cleanup is now required for all-green runs in strict mode

## Latest Progress (2026-02-03, Strict Gate Stabilization)

- Stabilized strict-warning rollout after baseline regression:
  - strict gate now enforces explicit Spectre warning codes only
    (`WARNING (SPECTRE-xxxxx)`)
  - warning allowlist introduced:
    - `config/spectre_warning_allowlist.txt`
  - initial allowlist entries: `SPECTRE-17191`, `SPECTRE-17192`
- Fixed OCEAN relative-path portability when invoked outside repo root:
  - `build.sh` now runs OCEAN from `$REPO_DIR`
- Revalidated:
  - `./build.sh all` PASS
    - `results/_runlogs/build_all_20260203_133924.manifest.txt`
  - `cd /tmp && /home/v71349/analog-gradients/build.sh pe4` PASS
    - `results/_runlogs/build_pe4_20260203_134239.manifest.txt`

## Latest Progress (2026-02-03, Warning-Count Drift Gate)

- Added fail-closed warning-count drift checks in `build.sh`:
  - each component/code warning count must not exceed prior green baseline
  - baseline file: `config/spectre_warning_baseline.csv`
  - baseline source run: `results/_runlogs/build_all_20260203_134652.manifest.txt`
- Added per-component warning summary to run manifests (`warnings=...`) for auditability.
- Revalidated:
  - `./build.sh all` PASS
    - `results/_runlogs/build_all_20260203_135841.manifest.txt`
  - negative test with lowered temp baseline fails as expected:
    - `SPECTRE_WARNING_BASELINE_FILE=/tmp/spectre_warning_baseline_test.csv ./build.sh pe4`

## Acceptance Criteria

1. Temporal sensitivity trends vary meaningfully with parameters (or explicitly
   show and justify invariance with higher-fidelity data).
2. ODE-fit section reports a defensible global model or clearly bounded local
   models with rationale.
3. Energy metric includes uncertainty and method assumptions.
4. All claims in `competition/founder-thesis.md` map to reproducible artifacts
   and confidence statements.
