# 0009: NeuroCore Robustness Sweeps

**Status:** Complete
**Priority:** High
**Created:** 2026-02-02

## Description

Harden the neuromorphic path by running parameter sweeps and defining stronger
stability criteria beyond nominal-point PASS checks.

## Tasks

- [x] Define initial sweep matrix for `neuro_tile4_coupled` (r_fb, rleak)
- [x] Add batch sweep automation (`scripts/sweep_neuro_tile4_coupled.sh`)
- [x] Capture spike count and membrane/spike maxima per sweep point
- [x] Expand sweep matrix to `synapse`, `lif_neuron`, and `neuron_tile`
- [x] Add first-spike latency extraction per sweep point
- [x] Define PASS bands for robust behavior (not just single-point PASS)
- [x] Publish first robustness summary under `competition/sweeps/`

## Acceptance Criteria

1. Sweep automation runs without manual edits
2. Sweep results are recorded in machine-readable form
3. A documented robustness verdict exists for each key analog block

## Completion Notes

- Added expanded sweep automation:
  - `scripts/sweep_synapse.sh`
  - `scripts/sweep_lif_neuron.sh`
  - `scripts/sweep_neuron_tile.sh`
  - `scripts/sweep_analog_robustness.sh`
- Added first-spike / first-pulse extraction in:
  - `ocean/test_synapse.ocn`
  - `ocean/test_lif_neuron.ocn`
  - `ocean/test_neuron_tile.ocn`
- Latest bundle summary confirms PASS coverage across key blocks:
  - `competition/sweeps/robustness_summary.md`
