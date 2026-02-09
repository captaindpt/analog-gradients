# Phase 2 Summary (Rows 6-14, Second Attempt)

Phase 2 was re-run for rows 6-14 in strict order using `BEST_P1=10` with the corrected `TrapVolume` template. New run artifacts are stored at `tcad/memristor/runs/20260209_085016_phase2_row6` through `tcad/memristor/runs/20260209_085040_phase2_row14`.

## What happened

- Outcomes: 9/9 runs ended as `FAIL:convergence`.
- IV extraction: 0/9 (`has_iv_data=no` in all manifests).
- Convergence status: no run reached `Good Bye`; all exited during early solve startup.
- Common SDevice error in all sampled rerun logs:
  - `Error: No valid electron BarrierTunneling mass has been specified for region 'R.Oxide'. !`

## Phase 2 Gate (Second Attempt)

- Required: at least 3/9 runs show nonlinear I-V.
- Observed: 0/9 runs produced any I-V data.
- Gate status: **FAIL (hard stop)**.

Per the second-attempt rule, this is treated as a real Phase 2 stop condition and work does not proceed to Phases 3-5 in this session.

## Carry-Forward Substitutions

- `BEST_P1 = 10`
- `BEST_P2_TRAP = NA` (no nonlinear I-V run available)
- `BEST_P2_ENERGY = NA` (no nonlinear I-V run available)

## Requested log interpretation

- Did it converge? **No** (0/9 converged).
- Is current still zero? **Not measurable from this rerun**, because no valid IV files were produced.
- What does the I-V look like? **No I-V curve generated** in this rerun due to solver termination before waveform output.
