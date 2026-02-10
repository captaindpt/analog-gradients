# Memristor TCAD Runbook (KMC ReRAM Pivot)

Purpose: Execute a physics-first RRAM primitive using Sentaurus KMC ReRAM.

This runbook supersedes the old drift-diffusion MIM flow. Use the KMC flow only.

## Scope

Allowed simulation stack:
- 3D geometry: `tcad/memristor/templates/mim_sde_3d.scm.tmpl`
- KMC deck: `tcad/memristor/templates/mim_sdevice_reram.cmd.tmpl`
- KMC parameters: `tcad/memristor/templates/reram.par`
- Sweep matrix: `tcad/memristor/config/sweep_matrix_reram.csv`
- Harness: `scripts/run_memristor_tcad_sweep.sh`

Obsolete for this workstream:
- `mim_sde.scm.tmpl`
- `mim_sdevice_phase1.cmd.tmpl`
- `mim_sdevice_phase2.cmd.tmpl`
- `mim_sdevice_phase3.cmd.tmpl`
- `hfo2.par`

## Ground Rules

1. One variable change per run.
2. Execute sweep rows in numeric order.
3. Save every run directory, including failures.
4. Do not modify `sweep_matrix_reram.csv` during execution.
5. Do not add extra physics models beyond the KMC deck.
6. Cap each session at 15 runs.
7. Stop immediately on syntax/parser errors and log exact error text.

## Environment Setup

```bash
source scripts/setup_sentaurus.sh
which sde sdevice snmesh
```

## Run Command

```bash
scripts/run_memristor_tcad_sweep.sh <row_number>
```

The harness will:
1. Read one row from `sweep_matrix_reram.csv`.
2. Materialize concrete SDE/SDevice decks in a timestamped run directory.
3. Run `sde` then `sdevice`.
4. Extract SET/RESET I-V to CSV when available.
5. Delete transient per-step snapshot files by default (`set_*_des.tdr`,
   `reset_*_des.tdr`, `set_*_circuit_des.sav`, `reset_*_circuit_des.sav`)
   to prevent disk/inode exhaustion.
6. Emit `manifest.txt` with parameters and metrics.

To keep transient snapshots for a targeted debug run only:

```bash
MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS=1 scripts/run_memristor_tcad_sweep.sh <row_number>
```

## Sweep Plan

File: `tcad/memristor/config/sweep_matrix_reram.csv`

- Row 1: Phase B baseline
- Rows 2-19: Phase C one-variable-at-a-time sensitivity
- Rows 20-26: Phase D corrective pre-seeded vacancy sweep

Key variables:
- `gen_ea`
- `diff_ea`
- `fil_growth_ea`
- `fil_growth_freq`
- `fil_recess_ea`
- `oxide_thickness_nm`
- `sweep_vmax_v`
- `initial_vac_conc`
- `initial_fil_conc`

## Run Artifact Contract

Every run directory under `tcad/memristor/runs/<timestamp>_reram_*` must contain:
- `manifest.txt`
- `mim.scm`
- `mim_device.cmd`
- `reram.par`
- `sde.log`
- `sdevice_stdout.log`
- `memdev_msh.tdr`
- `memdev_des.plt` and/or current files (`SET*.plt`, `RESET*.plt`) when converged
- `set_current.csv` and `reset_current.csv` when extraction succeeds
- transient per-step `set_*/reset_*` TDR/SAV files are optional and normally
  removed by the harness

## Manifest Fields

Required keys in `manifest.txt`:
- `run_id`
- `sweep_row`
- `phase`
- `sweep_group`
- `oxide_thickness_nm`
- `gen_ea`
- `diff_ea`
- `fil_growth_ea`
- `fil_growth_freq`
- `fil_recess_ea`
- `initial_vac_conc`
- `initial_fil_conc`
- `sweep_vmax_v`
- `compliance_a`
- `set_time_s`
- `reset_time_s`
- `outcome`
- `wall_time_s`
- `has_set_csv`
- `has_reset_csv`
- `set_current_abs_max_a`
- `reset_current_abs_max_a`
- `current_ratio_set_over_reset`
- `keep_transient_snapshots`

## Phase Gates

Phase B pass gate:
- `outcome=CONVERGED`
- non-zero current visible in SET/RESET extraction

Phase C progress gate:
- at least one parameter point with ON/OFF proxy ratio (`set_current_abs_max_a / reset_current_abs_max_a`) > 2x

If no switching ratio >2x in the capped run budget:
- publish summary, identify best-conduction point, and stop for human review.

## Session Deliverables

After each capped run session:
1. Update aggregate table: `tcad/memristor/runs/reram_results.csv`
2. Update narrative: `tcad/memristor/runs/reram_summary.md`
3. Update ticket: `my-workspace/tickets/0020-memristor-primitive-physics-first-workstream.md`
4. Commit with a message that states the KMC phase outcome.

## What Not To Do

- Do not return to drift-diffusion for RRAM switching proof.
- Do not move simulation artifacts outside `tcad/memristor/runs/`.
- Do not delete failed runs.
- Do not claim primitive success without hysteresis/switching evidence.
