# 0020: Memristor Primitive Physics-First Workstream

**Status:** In Progress  
**Priority:** High  
**Created:** 2026-02-09

## Description

Define and execute a physics-first path for a new memristor primitive:

1. Select and calibrate a mainstream RRAM (VCM) physical model.
2. Validate behavior against paper metrics (hysteresis, thresholds, ON/OFF,
   retention, switching energy).
3. Extract a compact model and integrate into Spectre/OCEAN for reusable
   circuit-level verification.

Planning references:
- `my-workspace/docs/reference/MEMRISTOR_PAPER_STOCK.md`
- `my-workspace/docs/reference/MEMRISTOR_PRIMITIVE_SPEC.md`

Paper inventory root:
- `papers/manifest.md`

## Tasks

### Prior (Planning + Compact Model Scaffold)
- [x] Add durable memristor paper stock index in reference docs
- [x] Add exhaustive physics-first primitive planning specification
- [x] Add first compact primitive netlist + OCEAN verifier (`memristor_vteam`)
- [x] Wire `memristor_vteam` into `build.sh` and verify local PASS
- [x] Add phase-A TCAD scaffold (`tcad/memristor/`) and run-init/analyzer scripts
- [x] Select anchor paper/device definition for phase-A calibration target
- [x] Stand up minimal headless physics simulation run (Sentaurus-first)

### Current (Physical TCAD Exploration)
- [x] Create Codex runbook with anti-spiral rules (`tcad/memristor/CODEX_RUNBOOK.md`)
- [x] Create sweep matrix with 38 planned runs across 5 phases
- [x] Create parameterized SDE + SDevice deck templates (Phase 1-3)
- [x] Create run harness (`scripts/run_memristor_tcad_sweep.sh`)
- [x] Create Sentaurus setup script (`scripts/setup_sentaurus.sh`)
- [x] Create PLT-to-CSV extractor (`scripts/extract_plt_to_csv.py`)
- [x] Run Phase 1 example: 10nm HfO2 MIM, DC 0-1V -> CONVERGED (zero current)
- [x] **BLOCKER**: Resolve correct SDevice tunneling/conduction syntax for oxide
- [x] Run Phase 1 sweep (rows 1-5): oxide thickness scan
- [x] Run Phase 2 sweep (rows 6-14): trap-assisted conduction (gate failed)
- [ ] Run Phase 3 sweep (rows 15-23): defect drift + state dependence
- [ ] Run Phase 4 sweep (rows 24-31): hysteresis tuning
- [ ] Run Phase 5 sweep (rows 32-38): pulse SET/RESET characterization
- [ ] Publish phase summaries and aggregate data for LinkedIn post

## Acceptance Criteria

1. Physical model reproduces baseline memristive behavior with bounded state and
   pinched hysteresis.
2. Set/reset thresholds and ON/OFF ratio are within defined spec bands from
   `MEMRISTOR_PRIMITIVE_SPEC.md`.
3. Set/reset energy per event is computed and reported with explicit method.
4. Compact model is runnable in Spectre and verified by deterministic OCEAN
   PASS/FAIL output.
5. Workstream remains fail-closed and reproducible under repo build conventions.

## Latest Progress (2026-02-09, Session 2)

Pivoted from planning docs to systematic TCAD physics exploration.

- Built full run infrastructure:
  - Codex runbook with strict anti-spiral rules
  - 38-row sweep matrix across 5 phases
  - Parameterized deck templates (SDE geometry + SDevice physics)
  - Automated run harness, PLT extractor, Sentaurus setup script
- Ran first real MIM structure (Phase 1 example):
  - 10nm HfO2 oxide, metal contacts top/bottom
  - SDE meshing: success
  - SDevice simulation: CONVERGED
  - Result: zero current (expected — no conduction model in Phase 1)
  - Run artifacts: `tcad/memristor/runs/example_phase1_mim_10nm/`
- Discovered blocker: `BarrierTunneling` keyword not recognized by SDevice
  vX-2025.09. Need to find correct syntax for enabling tunneling/conduction
  through insulator before Phase 2 can proceed.

## Latest Progress (2026-02-09, Session 3)

- Resolved Phase 2 syntax blocker using Sentaurus vX-2025.09 local examples from
  `Applications_Library` and `Sentaurus_Training`:
  - replaced fragile `BarrierTunneling` usage with
    `eBarrierTunneling`/`hBarrierTunneling`
  - added required `Math { NonLocal ... }` definitions
  - updated trap syntax to include `fromCondBand` and trap-coupled nonlocal
    tunneling terms
- Updated templates:
  - `tcad/memristor/templates/mim_sdevice_phase1.cmd.tmpl`
  - `tcad/memristor/templates/mim_sdevice_phase2.cmd.tmpl`
- Executed Phase 1 sweep matrix rows 1-5 in order with harness:
  - runs: `tcad/memristor/runs/20260209_083318_phase1_row1/`
    through `tcad/memristor/runs/20260209_083331_phase1_row5/`
  - outcomes: 5/5 CONVERGED, all with `iv_data.csv` and `metrics.json`
  - observed electrical result: extracted current remains effectively zero at
    all Phase 1 points
- Published phase artifacts per runbook:
  - aggregate CSV: `tcad/memristor/runs/phase1_results.csv`
  - summary note: `tcad/memristor/runs/phase1_summary.md`
  - recommended `BEST_P1` carry-forward: `oxide_thickness_nm=10` (row 2 baseline)

### Prior Progress (2026-02-09, Session 1)

- `memristor_vteam` compact model added and verified
- Sentaurus headless environment validated (silicon bar smoke test)
- Paper stock and primitive spec docs consolidated

## Latest Progress (2026-02-09, Session 4)

- Executed Phase 2 sweep matrix rows 6-14 in strict row order with
  `BEST_P1=10` via `scripts/run_memristor_tcad_sweep.sh`.
- Run outputs saved for all 9 rows:
  - `tcad/memristor/runs/20260209_084222_phase2_row6/`
  - `tcad/memristor/runs/20260209_084225_phase2_row7/`
  - `tcad/memristor/runs/20260209_084228_phase2_row8/`
  - `tcad/memristor/runs/20260209_084231_phase2_row9/`
  - `tcad/memristor/runs/20260209_084234_phase2_row10/`
  - `tcad/memristor/runs/20260209_084237_phase2_row11/`
  - `tcad/memristor/runs/20260209_084240_phase2_row12/`
  - `tcad/memristor/runs/20260209_084243_phase2_row13/`
  - `tcad/memristor/runs/20260209_084246_phase2_row14/`
- Outcome: 9/9 runs ended without IV extraction (`FAIL:convergence` in manifest).
- Common SDevice termination message (sampled logs):
  `TrapVolume must be positive for each trap for which the barrier tunneling model is turned on !`
- Applied syntax-level deck correction for next attempt:
  - added `TrapVolume=1e-21` in trap definitions for
    `tcad/memristor/templates/mim_sdevice_phase2.cmd.tmpl` and
    `tcad/memristor/templates/mim_sdevice_phase3.cmd.tmpl`
- Phase 2 stop gate result:
  - required: >=3/9 nonlinear IV runs
  - observed: 0/9 nonlinear IV runs (no usable IV output)
  - status: hard stop, no Phase 3 execution this session
- Published Phase 2 artifacts:
  - `tcad/memristor/runs/phase2_results.csv`
  - `tcad/memristor/runs/phase2_summary.md`
  - carry-forward values: `BEST_P2_TRAP=NA`, `BEST_P2_ENERGY=NA`

## Latest Progress (2026-02-09, Session 5)

- Re-ran Phase 2 rows 6-14 as a second attempt with corrected trap template:
  - command pattern: `BEST_P1=10 scripts/run_memristor_tcad_sweep.sh <row>`
  - rows executed in order: 6, 7, 8, 9, 10, 11, 12, 13, 14
- New rerun artifact directories:
  - `tcad/memristor/runs/20260209_085016_phase2_row6/`
  - `tcad/memristor/runs/20260209_085019_phase2_row7/`
  - `tcad/memristor/runs/20260209_085022_phase2_row8/`
  - `tcad/memristor/runs/20260209_085025_phase2_row9/`
  - `tcad/memristor/runs/20260209_085028_phase2_row10/`
  - `tcad/memristor/runs/20260209_085031_phase2_row11/`
  - `tcad/memristor/runs/20260209_085034_phase2_row12/`
  - `tcad/memristor/runs/20260209_085037_phase2_row13/`
  - `tcad/memristor/runs/20260209_085040_phase2_row14/`
- Rerun result:
  - 9/9 `FAIL:convergence`
  - 0/9 with extracted IV data
  - common SDevice error: `No valid electron BarrierTunneling mass has been specified for region 'R.Oxide'`
- Phase 2 stop gate on second attempt:
  - required: >=3/9 nonlinear IV
  - observed: 0/9 nonlinear IV (no IV output)
  - status: hard stop; no Phase 3 execution in this session
- Phase 2 outputs were overwritten with rerun data:
  - `tcad/memristor/runs/phase2_results.csv`
  - `tcad/memristor/runs/phase2_summary.md`

## Latest Progress (2026-02-09, Session 6, KMC Pivot)

- Pivoted TCAD method from drift-diffusion tunneling deck to Sentaurus KMC ReRAM:
  - new 3D geometry template: `tcad/memristor/templates/mim_sde_3d.scm.tmpl`
  - new KMC SDevice template: `tcad/memristor/templates/mim_sdevice_reram.cmd.tmpl`
  - new KMC material parameter file: `tcad/memristor/templates/reram.par`
  - harness updated to KMC sweep matrix + SET/RESET extraction:
    `scripts/run_memristor_tcad_sweep.sh`
- Executed 15-run capped session (rows 1-15 of
  `tcad/memristor/config/sweep_matrix_reram.csv`):
  - run dirs: `tcad/memristor/runs/20260209_104232_reram_baseline/` through
    `tcad/memristor/runs/20260209_113745_reram_row15_oxide_thickness/`
  - outcomes: 15/15 `CONVERGED`
  - extracted SET/RESET CSV: 15/15
  - nonzero current: 15/15 (`~3e-15 A` to `~5e-15 A`)
  - switching proxy ratio (`set/reset abs max`) > 2x: 0/15
- Published KMC aggregate artifacts:
  - `tcad/memristor/runs/reram_results.csv`
  - `tcad/memristor/runs/reram_summary.md`
- Notable observation:
  - only row 2 (`gen_ea=0.6`) showed non-zero KMC event counters in sampled
    log summaries, but still no macro-level SET/RESET separation.
- Session cap reached (15 runs), so remaining planned Phase C points are
  deferred:
  - row 16 (`oxide_thickness_nm=8`)
  - rows 17-19 (`sweep_vmax_v = 2.0, 3.0, 4.0`)

## Latest Progress (2026-02-09, Session 7, KMC Corrective Phase D)

- Applied corrective KMC changes for vacancy pre-seeding and aggressive
  generation:
  - `tcad/memristor/templates/mim_sdevice_reram.cmd.tmpl` now supports
    `Particle2(Conc=%%INITIAL_VAC_CONC%%)`
  - `scripts/run_memristor_tcad_sweep.sh` now parses/substitutes/persists
    `initial_vac_conc`
  - `tcad/memristor/config/sweep_matrix_reram.csv` extended to include rows
    20-26 with pre-seeded Phase D points
- Executed rows 20-26 in order:
  - `tcad/memristor/runs/20260209_141652_reram_row20_preseeded_baseline/`
  - `tcad/memristor/runs/20260209_142104_reram_row21_preseeded_low_ea/`
  - `tcad/memristor/runs/20260209_142505_reram_row22_preseeded_high_freq/`
  - `tcad/memristor/runs/20260209_142901_reram_row23_preseeded_aggressive/`
  - `tcad/memristor/runs/20260209_143359_reram_row24_preseeded_very_aggressive/`
  - `tcad/memristor/runs/20260209_145041_reram_row25_preseeded_4V/`
  - `tcad/memristor/runs/20260209_145818_reram_row26_preseeded_thin/`
- Outcomes:
  - 6/7 `CONVERGED`
  - row 24 recorded `FAIL:convergence` after forced termination due extreme
    runtime outlier under very-aggressive settings
- Corrective criteria status:
  - `KMC generation count > 50`: met in 6/7 rows
  - `Filament growth count > 0`: 0/7 (no breakthrough)
  - `SET current > 1e-10 A`: 0/7 (still leakage-scale, `~1e-15` to `~3e-15 A`)
  - `SET/RESET current ratio > 2x`: 0/7 (`ratio=1.0` on converged rows)
- Published aggregated results (Phase D appended, not discarded prior rows):
  - `tcad/memristor/runs/reram_results.csv`
  - `tcad/memristor/runs/reram_summary.md`
