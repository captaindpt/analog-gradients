# Session: 2026-02-02 - Ticket 0013 Phase 2 (ODE + Energy Uncertainty)

## Summary

Completed the remaining rigor-hardening tasks on ticket 0013:

1. phase-aware LIF ODE fitting with baseline comparison,
2. uncertainty-aware energy-per-spike reporting.

## Changes Applied

1. **Phase-aware ODE analysis**
   - Reworked `scripts/analyze_lif_ode_fit.py` to produce:
     - global baseline fit (`dV/dt = a*V + b*out + c*spike + d`),
     - piecewise phase-aware fit (`charge`, `reset`, `decay`),
     - per-phase sample counts and per-phase fit quality,
     - global vs piecewise comparison metrics.
   - Updated artifacts:
     - `competition/analysis/lif_ode_fit_summary.md`
     - `competition/analysis/lif_ode_fit_trace.csv`
   - Key result:
     - derivative `R^2`: `0.029 -> 0.312` (global -> piecewise)
     - one-step reconstruction RMSE: `0.0707V -> 0.0595V`

2. **Energy uncertainty reporting**
   - Reworked `ocean/extract_lif_energy.ocn` to also emit:
     - `competition/analysis/lif_energy_trace.csv`
     - interpolated spike-crossing timestamps.
   - Reworked `scripts/analyze_lif_energy.sh` to compute:
     - per-spike event-window energies,
     - event std/CV,
     - bootstrap mean + 95% CI (`N=2000`, deterministic seed).
   - Updated artifacts:
     - `competition/analysis/lif_energy_summary.txt`
     - `competition/analysis/lif_energy_summary.md`
     - `competition/analysis/lif_energy_bootstrap.csv`
   - Key result:
     - energy/spike (total/spike): `3.270599 pJ`
     - bootstrap 95% CI: `[3.154657, 3.424110] pJ`

## Validation

- `python3 scripts/analyze_lif_ode_fit.py` -> PASS
- `scripts/analyze_lif_energy.sh` -> PASS
- `python3 -m py_compile scripts/analyze_lif_ode_fit.py` -> PASS
- `bash -n scripts/analyze_lif_energy.sh` -> PASS
