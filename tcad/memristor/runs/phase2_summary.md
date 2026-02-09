# Phase 2 Summary (Rows 6-14)

Phase 2 executed rows 6-14 in strict order using `scripts/run_memristor_tcad_sweep.sh` with `BEST_P1=10` (from Phase 1 baseline). All nine runs produced complete manifests and logs under `tcad/memristor/runs/20260209_084222_phase2_row6` through `tcad/memristor/runs/20260209_084246_phase2_row14`, but all exited before waveform generation (`has_iv_data=no`). The common SDevice termination message across sampled runs is `TrapVolume must be positive for each trap for which the barrier tunneling model is turned on !`, so no valid I-V traces were produced for nonlinearity evaluation.

## Phase 2 Gate Result

- Required: at least 3/9 runs with nonlinear I-V.
- Observed: 0/9 runs with usable I-V (all `FAIL:convergence` in manifests).
- Gate status: **FAIL (hard stop)**.

## Carry-Forward Substitutions

- `BEST_P1 = 10`
- `BEST_P2_TRAP = NA` (not selected; no valid nonlinear run)
- `BEST_P2_ENERGY = NA` (not selected; no valid nonlinear run)

Per runbook hard-stop rules, execution does not proceed to Phase 3 in this session.

## Syntax Follow-Up Applied

- Added `TrapVolume=1e-21` to trap entries in:
  - `tcad/memristor/templates/mim_sdevice_phase2.cmd.tmpl`
  - `tcad/memristor/templates/mim_sdevice_phase3.cmd.tmpl`
- This addresses the explicit SDevice runtime requirement reported in Phase 2 logs.
