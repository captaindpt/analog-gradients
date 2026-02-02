# 0009: NeuroCore Robustness Sweeps

**Status:** In Progress
**Priority:** High
**Created:** 2026-02-02

## Description

Harden the neuromorphic path by running parameter sweeps and defining stronger
stability criteria beyond nominal-point PASS checks.

## Tasks

- [x] Define initial sweep matrix for `neuro_tile4_coupled` (r_fb, rleak)
- [x] Add batch sweep automation (`scripts/sweep_neuro_tile4_coupled.sh`)
- [x] Capture spike count and membrane/spike maxima per sweep point
- [ ] Expand sweep matrix to `synapse`, `lif_neuron`, and `neuron_tile`
- [ ] Add first-spike latency extraction per sweep point
- [ ] Define PASS bands for robust behavior (not just single-point PASS)
- [x] Publish first robustness summary under `competition/sweeps/`

## Acceptance Criteria

1. Sweep automation runs without manual edits
2. Sweep results are recorded in machine-readable form
3. A documented robustness verdict exists for each key analog block
