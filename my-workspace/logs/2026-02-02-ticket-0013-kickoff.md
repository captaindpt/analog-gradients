# Session: 2026-02-02 - Ticket 0013 Kickoff (Rigor Hardening)

## Summary

Started ticket `0013-evidence-rigor-hardening` with a first implementation
slice focused on temporal-sensitivity evidence quality:

1. finer coupled-tile sweep coverage,
2. preserved per-point raw artifacts,
3. higher-fidelity spike timing extraction,
4. slope uncertainty/fit-quality reporting.

## Changes Applied

1. **Coupled sweep script upgrade**
   - Updated `scripts/sweep_neuro_tile4_coupled.sh`.
   - Default grid expanded to:
     - `r_fb={600,700,800,900,1000,1100,1200,1300,1500}`
     - `rleak={5M,6M,7M,8M,9M,10M,12M}`
   - Added per-run archive root with manifest:
     - `results/neuro_tile4_coupled/sweeps/<run_id>/`
     - `sweep_manifest.txt` includes settings + start/end timestamps.
   - Preserves per-point raw/log/result files for auditability.
   - Injects `maxstep=100p` into sweep netlists for improved transient fidelity.

2. **OCEAN timing extraction hardening**
   - Updated `ocean/test_neuro_tile4_coupled.ocn`.
   - Reduced sampling step from `500p` to `100p`.
   - Added linear interpolation for threshold crossing times.
   - Increased first-spike output precision to `%.3f ns`.

3. **Temporal sensitivity analysis upgrade**
   - Rewrote `scripts/analyze_temporal_sensitivity.py` to emit:
     - slope + intercept
     - fit quality (`R2`)
     - slope uncertainty (`CI95`)
     - min nonzero timing-step diagnostic
   - Output artifacts:
     - `competition/analysis/temporal_sensitivity_slopes.csv`
     - `competition/analysis/temporal_sensitivity_summary.md`

4. **Model parameter correctness**
   - Replaced invalid `vth=` with valid `vto=` model parameter in all netlists.
   - Set analog-path netlists to `vto=0.0` to preserve prior verified behavior.

## Verification Runs

- `./build.sh neuro_tile4_coupled` -> PASS after updates.
- `scripts/sweep_neuro_tile4_coupled.sh` -> PASS (`63/63` points).
  - Run ID: `20260202_215026`
  - Run archive: `results/neuro_tile4_coupled/sweeps/20260202_215026/`
- `RFB_LIST=1000 RLEAK_LIST=8M scripts/sweep_neuro_tile4_coupled.sh` -> PASS
  (smoke test for new run-archive paths and manifest wiring).
  - Run ID: `20260202_220756`
  - Canonical sweep CSV/summary restored to the 63-point run afterward.
- `python3 scripts/analyze_temporal_sensitivity.py` -> PASS
- `./build.sh all` -> PASS

## Next on Ticket 0013

- Phase-aware ODE modeling update (`scripts/analyze_lif_ode_fit.py`).
- Uncertainty reporting for energy-per-spike (`scripts/analyze_lif_energy.sh`).
