# 0012: Founder Thesis Evidence Track

**Status:** Completed (phase-1 evidence pack)
**Priority:** High
**Created:** 2026-02-02

## Description

Elevate project narrative from "tool proficiency" to a defensible original
compute thesis: clockless continuous-time computation encoded in analog spike
dynamics.

## Tasks

- [x] Publish founder-thesis reference doc
- [x] Update core vision/reference docs with thesis-first framing
- [x] Add ODE-fit analysis (measured vs model) with error metrics
- [x] Add temporal sensitivity extraction (`dt_spike/dparameter`)
- [x] Add energy-per-event estimate from transient supply behavior
- [x] Add mixed-signal coupling experiment plan and first smoke artifact

## Latest Artifacts (2026-02-02)

- ODE fit:
  - `competition/analysis/lif_ode_fit_summary.md`
  - `competition/analysis/lif_ode_fit_trace.csv`
- Temporal sensitivity:
  - `competition/analysis/temporal_sensitivity_summary.md`
  - `competition/analysis/temporal_sensitivity_slopes.csv`
- Energy/event:
  - `competition/analysis/lif_energy_summary.md`
  - `competition/analysis/lif_energy_summary.txt`
- Mixed-signal smoke:
  - `competition/mixed-signal-smoke-evidence.md`
  - `results/neuro_tile4_mixed_signal_test.txt`

## Acceptance Criteria

1. Every thesis claim maps to at least one reproducible artifact
2. Math-oriented evidence is present (fit, sensitivity, energy)
3. Demo narrative leads with original idea, not only flow tooling
