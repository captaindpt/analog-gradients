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

## Phase D Corrective Run (Rows 20-26)

Scope: pre-seeded vacancy corrective sweep requested after diagnosing event starvation in pristine HfO2.

Template/harness changes applied before these runs:
- Added `Particle2(Conc=%%INITIAL_VAC_CONC%%)` to `tcad/memristor/templates/mim_sdevice_reram.cmd.tmpl`
- Added `initial_vac_conc` column to `tcad/memristor/config/sweep_matrix_reram.csv`
- Updated `scripts/run_memristor_tcad_sweep.sh` to parse/substitute/record `initial_vac_conc`

Run outcomes for rows 20-26:
- Converged: 6/7
- Failed: 1/7 (row 24, terminated during extreme KMC runtime; recorded as `FAIL:convergence`)

Key quantitative observations:
- KMC generation increased dramatically with pre-seeding + aggressive kinetics:
  - row 21: generation max `11854`, vacancy diffusion max `200678`
  - row 23: generation max `965488`, vacancy diffusion max `1275661`
  - row 25: generation max `3219786`, vacancy diffusion max `4264385`
  - row 26: generation max `1930997`, vacancy diffusion max `2559497`
- Despite large vacancy populations, filament growth remained zero in all rows:
  - `ImmobileVacancy Growth count max = 0` for rows 20-26
- Extracted SET current remained leakage-scale:
  - `set_current_abs_max_a` ranged from `1.19e-15 A` to `2.97501e-15 A`
- SET/RESET separation was not observed:
  - `current_ratio_set_over_reset = 1.0` for all converged Phase D rows

Requested success criteria check (rows 20-26):
- `KMC generation count > 50`: met in 6/7 rows
- `Filament growth count > 0`: not met (0/7)
- `SET current > 1e-10 A`: not met (0/7)
- `SET/RESET current ratio > 2x`: not met (0/7)

Breakthrough status:
- No filament-formation breakthrough in this sweep.

## Phase E Corrective Run (Filament Nuclei + Growth-Rate Boost)

Scope: apply filament pre-seeding and higher growth kinetics; stop immediately on first non-zero filament growth.

Changes applied:
- Added `Filament1(Conc=%%INITIAL_FIL_CONC%%)` in the HfO2 `KMCDefects` block.
- Added `%%FIL_GROWTH_FREQ%%` placeholder for `FilamentGrowth(Frequency=...)`.
- Updated sweep schema and harness to support `initial_fil_conc` and `fil_growth_freq`.

Execution outcome:
- Row executed: `27` (`fil_seed_baseline`)
- Stop condition triggered: yes (`ImmobileVacancy Growth count > 0`)
- Rows `28-33`: intentionally not run after breakthrough, per stop rule.

Breakthrough evidence (row 27):
- Run directory: `tcad/memristor/runs/20260209_163928_reram_row27_fil_seed_baseline/`
- `ImmobileVacancy Growth count` became non-zero and climbed during transient:
  - sampled maxima reached `91`
- `Number of ImmobileVacancy` in KMC particle summaries increased (seeded filament particles present and extending).

Row 27 key metrics:
- Outcome: `FAIL:convergence` (run was terminated after breakthrough to honor immediate-stop policy)
- KMC generation max: `881745`
- KMC vacancy diffusion max: `1162105`
- Extracted SET/RESET current files: unavailable (`NA`) due early termination.

Interpretation:
- This session achieved the requested first filament-growth proof.
- The growth bottleneck (no Filament1 nucleation) is resolved by pre-seeding filament nuclei.
