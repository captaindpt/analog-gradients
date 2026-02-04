# Founder Thesis Analysis Artifacts

This folder contains math-oriented evidence artifacts for the founder-thesis track.

## ODE Fit (LIF Dynamics)

- `lif_ode_fit_summary.md`
- `lif_ode_fit_trace.csv`
- Includes global baseline + phase-aware piecewise model comparison.

## Temporal Sensitivity (Timing Gradients)

- `temporal_sensitivity_summary.md`
- `temporal_sensitivity_slopes.csv`
- Source sweep: `competition/sweeps/neuro_tile4_coupled_sweep.csv`

## Energy Per Event

- `lif_energy_summary.md`
- `lif_energy_summary.txt`
- `lif_energy_trace.csv`
- `lif_energy_bootstrap.csv`

## Corner-Conditioned Evidence (LIF)

- Run root:
  `competition/analysis/lif_corners/20260202_224254/`
- Summary artifacts:
  - `lif_corner_summary.csv`
  - `lif_corner_summary.md`
- Per-corner folders include:
  - waveform CSV + energy trace CSV
  - ODE fit summary/trace
  - energy summary + bootstrap CSV

## Regeneration Commands

```bash
python3 scripts/analyze_lif_ode_fit.py
scripts/sweep_neuro_tile4_coupled.sh
python3 scripts/analyze_temporal_sensitivity.py
scripts/analyze_lif_energy.sh
scripts/run_lif_corner_evidence.sh
```

Recent update (2026-02-03):
- Coupled-tile sweep resolution increased to 63 points.
- Temporal sensitivity output now includes `R2`, slope `CI95`, and minimum
  nonzero timing-step diagnostics.
- LIF ODE output now reports phase-aware fit metrics and baseline comparison.
- Energy report now includes per-event variation, CV, and bootstrap CI.
- Corner-conditioned LIF ODE/energy sweep added (9-point baseline run).
