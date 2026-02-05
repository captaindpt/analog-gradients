# 0015: Workspace Rendezvous and Scale Ramp

**Status:** Complete
**Priority:** High
**Created:** 2026-02-03

## Description

Create a clean, repeatable execution baseline for the next growth phase:
license-configured full-flow replay + stronger analog robustness + larger
neuromorphic block integration.

## Tasks

- [x] Publish workspace rendezvous contract and operating loop
- [x] Tighten repository hygiene for local scratch/probe artifacts
- [x] Update full-flow scripts/docs to reflect license-env preconditions by default
- [x] Resolve DC `DB-1` target-library path issue for strict full-flow replay
- [x] Expand robustness sweeps to `synapse`, `lif_neuron`, and `neuron_tile`
- [x] Define and enforce robust PASS bands for expanded sweep set
- [x] Propose next larger integration target beyond current 4-neuron compute demos

## Acceptance Criteria

1. `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh` is reproducible with clear
   preconditions and no ambiguous license narrative.
2. Robustness summary includes `synapse`, `lif_neuron`, `neuron_tile`,
   and `neuro_tile4_coupled` with explicit PASS bands.
3. A documented next-scale integration target is ready with netlist + verifier
   plan and ticket references.

## Progress Notes

- 2026-02-04: Added sweep automation for `synapse`, `lif_neuron`, and
  `neuron_tile`:
  - `scripts/sweep_synapse.sh`
  - `scripts/sweep_lif_neuron.sh`
  - `scripts/sweep_neuron_tile.sh`
  - `scripts/sweep_analog_robustness.sh` (bundle + summary)
- 2026-02-04: Added first-spike / first-pulse timing extraction to:
  - `ocean/test_synapse.ocn`
  - `ocean/test_lif_neuron.ocn`
  - `ocean/test_neuron_tile.ocn`
- 2026-02-04: Enforced pass-band based `overall_pass` for expanded sweeps and
  regenerated bundle evidence:
  - `competition/sweeps/robustness_summary.md`
- 2026-02-05: Defined next-scale integration target as ticket 0018 with
  concrete netlist + verifier plan:
  - `my-workspace/tickets/0018-neuro-tile16-hierarchical-integration.md`
