# Session: 2026-02-02 - Founder Evidence Analyses

## Summary

Executed first quantitative proof set for the founder-thesis track:
ODE-fit analysis, timing-sensitivity extraction, and energy-per-spike estimate.

## Added Scripts

- `scripts/analyze_lif_ode_fit.py`
- `scripts/analyze_temporal_sensitivity.py`
- `scripts/analyze_lif_energy.sh`
- `ocean/extract_lif_energy.ocn`

## Updated Automation

- `scripts/sweep_neuro_tile4_coupled.sh` now records `first_spike_times_ns`
  for each sweep point.

## Generated Artifacts

- ODE fit:
  - `competition/analysis/lif_ode_fit_summary.md`
  - `competition/analysis/lif_ode_fit_trace.csv`
- Temporal sensitivity:
  - `competition/analysis/temporal_sensitivity_summary.md`
  - `competition/analysis/temporal_sensitivity_slopes.csv`
- Energy estimate:
  - `competition/analysis/lif_energy_summary.md`
  - `competition/analysis/lif_energy_summary.txt`

## Notable Metrics

- LIF decay-window ODE fit (12ns-19ns): `R^2 = 0.931`
- Coupled-tile sensitivity: `dt_spike0/dr_fb ≈ -0.663 ns/kOhm`
- First-pass energy per spike (LIF): `4.718 pJ/spike`
