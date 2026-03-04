# Project Pause Handoff (2026-03-04)

## Context

- Owner-requested temporary project sunset/pause on 2026-03-04.
- Goal of this checkpoint: preserve a clean, restartable state with truthful docs.

## Repo Cleanup Performed

- Removed generated local artifacts from working tree before commit:
  - `memristor_vteam_sweep.ahdlSimDB/`
  - `results/memristor_vteam/`
  - `results/memristor_vteam_sweep/`
  - `tcad/memristor/results/`
  - `results/memristor_linkedin_figure.png`
- Tightened ignore rules for recurring generated outputs in `.gitignore`:
  - `*.ahdlSimDB/`
  - `tcad/memristor/results/`
  - `results/memristor_linkedin_figure.png`

## Memristor Track Snapshot

- Sweep matrix source: `tcad/memristor/config/sweep_matrix_reram.csv`
  - Planned rows: `64` (rows `1..64`).
- Recorded outcomes source: `tcad/memristor/runs/reram_results.csv`
  - Recorded rows: `1..27`
  - Outcome tally: `25 CONVERGED`, `2 FAIL:convergence`
  - Latest entries: rows 16-19 reruns on 2026-02-17.
- Harness hardening in place:
  - `scripts/run_memristor_tcad_sweep.sh` now supports log throttling,
    optional timeout, and log capping.
  - Batch launch helpers:
    `scripts/run_phase_f_scout_34_40.sh`, `scripts/run_reram_blitz.sh`.

## Durable Verification Snapshot

- Compact memristor behavioral test artifact:
  `results/memristor_vteam_test.txt`
- Latest timestamp in that artifact: `Feb 17 10:19:10 2026`.

## Known Open Risk (Still True)

- Sentaurus direct tunneling path still unresolved for physically credible
  switching-current claims.
- `BarrierTunneling` keyword rejection remains a blocker for fully defensible
  Phase-H+ physical claim quality.

## Restart Checklist

1. `source setup_cadence.sh`
2. `source scripts/setup_sentaurus.sh`
3. `./build.sh memristor_vteam`
4. Resume target rows (examples):
   - `scripts/run_phase_f_scout_34_40.sh`
   - `MEMRISTOR_BLITZ_ROWS="901 902 903" scripts/run_reram_blitz.sh`
5. After each batch, update:
   - `tcad/memristor/runs/reram_results.csv`
   - `my-workspace/docs/STATUS.md`
   - next dated log in `my-workspace/logs/`
