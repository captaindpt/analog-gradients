# KMC ReRAM Sweep Summary (Session Cap: 15 Runs)

Date: 2026-02-09
Scope: Phase B baseline + Phase C one-variable sensitivity, rows 1-15 from `tcad/memristor/config/sweep_matrix_reram.csv`.

## Run Outcomes

- Total runs executed: 15
- Converged (`outcome=CONVERGED`): 15/15
- Runs with extracted SET/RESET CSV: 15/15
- Runs with non-zero SET current: 15/15
- SET current magnitude range: `2.97501e-15 A` to `4.95835e-15 A`
- ON/OFF proxy (`set_current_abs_max_a / reset_current_abs_max_a`) > 2x: 0/15

Aggregate table: `tcad/memristor/runs/reram_results.csv`

## Parameter Combinations That Converged

All tested combinations converged for rows 1-15:
- baseline
- `gen_ea` sweep (0.6, 0.8, 1.0)
- `diff_ea` sweep (0.3, 0.4, 0.5)
- `fil_growth_ea` sweep (0.3, 0.4, 0.5)
- `fil_recess_ea` sweep (0.4, 0.5, 0.6)
- `oxide_thickness_nm` sweep points tested in this session: 3nm, 5nm

## Filament/Defect Activity Signals

Log-derived KMC event counters (from `sdevice_stdout.log`) showed non-zero activity in one run:
- Row 2 (`gen_ea=0.6`): max generation count = 5, max vacancy diffusion count = 537

All other rows in this session reported zero generation/diffusion counts in sampled summaries.

## Resistance Switching Result

No run showed measurable SET/RESET separation in the current proxy metric:
- `current_ratio_set_over_reset = 1.0` for all rows 1-15.

I-V extraction indicates near-constant current magnitude across voltage ramps in both SET and RESET files for tested runs.

## Best Observed Parameter Set (This Session)

Best conduction magnitude observed:
- Row 14 (`oxide_thickness_nm=3`, others baseline)
- `set_current_abs_max_a = 4.95835e-15 A`
- `reset_current_abs_max_a = 4.95835e-15 A`
- ON/OFF proxy ratio = `1.0`

This is best for absolute current, but it is not a switching solution.

## Acceptance Gate Status vs Spec

Compared against `my-workspace/docs/reference/MEMRISTOR_PRIMITIVE_SPEC.md` section 7:
- Pinched hysteresis: not demonstrated in rows 1-15.
- Distinct SET/RESET thresholds: not demonstrated.
- ON/OFF ratio > 2x minimum proof: not met.

Conclusion: KMC infrastructure is operational and stable, but memristive switching proof is not yet achieved in this run budget.

## Run Budget Status

Session cap reached (15 runs). Remaining planned points were not executed in this session:
- Row 16 (`oxide_thickness_nm=8`)
- Rows 17-19 (`sweep_vmax_v` sweep: 2V, 3V, 4V)

