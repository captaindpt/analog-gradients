# Founder Thesis Analysis Artifacts

This folder contains math-oriented evidence artifacts for the founder-thesis track.

## ODE Fit (LIF Dynamics)

- `lif_ode_fit_summary.md`
- `lif_ode_fit_trace.csv`

## Temporal Sensitivity (Timing Gradients)

- `temporal_sensitivity_summary.md`
- `temporal_sensitivity_slopes.csv`

## Energy Per Event

- `lif_energy_summary.md`
- `lif_energy_summary.txt`

## Regeneration Commands

```bash
python3 scripts/analyze_lif_ode_fit.py
python3 scripts/analyze_temporal_sensitivity.py
scripts/analyze_lif_energy.sh
```
