# 2026-02-05 - Next-Scale Integration Target Definition

## Objective

Close the remaining scale-ramp planning gap by defining a concrete post-tile4
integration target with explicit netlist and verifier plan.

## Work Completed

- Added new scale ticket:
  - `my-workspace/tickets/0018-neuro-tile16-hierarchical-integration.md`
- Marked workspace rendezvous scale-ramp ticket complete:
  - `my-workspace/tickets/0015-workspace-rendezvous-and-scale-ramp.md`
- Updated status tracker with 0015 completion and 0018 activation:
  - `my-workspace/docs/STATUS.md`

## Defined Next Target

- Block: `neuro_tile16_hier` (working name)
- Scope:
  - 16-neuron hierarchical coupled integration (4x `neuro_tile4_coupled` quadrants)
  - inter-quadrant feed-forward links for deeper propagation chain
  - parameterized for sweepability (`r_fb`, `rleak`, `r_couple`, `cmem`, `cpost`)
- Planned files:
  - `netlists/neuro_tile16_hier.scs`
  - `ocean/test_neuro_tile16_hier.ocn`

## Immediate Next Steps

1. Implement `netlists/neuro_tile16_hier.scs`.
2. Implement `ocean/test_neuro_tile16_hier.ocn` with deterministic PASS/FAIL.
3. Add target to `build.sh` and validate with `./build.sh neuro_tile16_hier`.
