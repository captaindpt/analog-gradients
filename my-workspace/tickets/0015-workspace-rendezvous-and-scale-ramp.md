# 0015: Workspace Rendezvous and Scale Ramp

**Status:** In Progress
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
- [ ] Resolve DC `DB-1` target-library path issue for strict full-flow replay
- [ ] Expand robustness sweeps to `synapse`, `lif_neuron`, and `neuron_tile`
- [ ] Define and enforce robust PASS bands for expanded sweep set
- [ ] Propose next larger integration target beyond current 4-neuron compute demos

## Acceptance Criteria

1. `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh` is reproducible with clear
   preconditions and no ambiguous license narrative.
2. Robustness summary includes `synapse`, `lif_neuron`, `neuron_tile`,
   and `neuro_tile4_coupled` with explicit PASS bands.
3. A documented next-scale integration target is ready with netlist + verifier
   plan and ticket references.
