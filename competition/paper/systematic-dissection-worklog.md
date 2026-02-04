# Systematic Dissection Worklog

Date: 2026-02-03

Purpose: keep paper-facing architecture reasoning explicit, auditable, and easy to continue.

## What was done in this pass

1. Re-checked the latest verification reports used by the paper:
   - `results/synapse_test.txt`
   - `results/lif_neuron_test.txt`
   - `results/neuron_tile_test.txt`
   - `results/neuro_tile4_test.txt`
   - `results/neuro_tile4_coupled_test.txt`
   - `results/neuro_tile4_mixed_signal_test.txt`

2. Updated manuscript metrics to match report values.

3. Expanded architecture articulation in:
   - `competition/paper/architecture-dissection.md`
   - `competition/paper/neurocore_workthrough.tex`
   - `competition/paper/full-architecture-atlas.md`

4. Added a larger assembled architecture figure and claim-to-artifact table in the LaTeX source.
5. Added one singular primitive-to-system architecture figure covering both digital and neuromorphic branches.

6. Added an explicit limitations/hardening section so claims are bounded and auditable.

## Architecture decomposition used

- Primitive dynamics:
  - Synapse RC
  - LIF membrane + threshold/reset
- Local composition:
  - Neuron tile (single channel)
- Spatial composition:
  - Tile4 parallel channels
  - Coupled feed-forward channels
- Mixed-signal control:
  - digital enable gating analog propagation

## Open paper TODOs

- Add one short subsection comparing clocked digital semantics vs trajectory/timing semantics.
- Add one figure callout panel for mixed-signal pre-enable vs post-enable behavior.
- Freeze a release-paper snapshot after ticket `0013` rigor updates land.
