# 0018: Neuro Tile16 Hierarchical Integration

**Status:** In Progress
**Priority:** High
**Created:** 2026-02-05

## Description

Define and implement the next larger integration target beyond current 4-neuron
compute demos: a 16-neuron hierarchical coupled tile that preserves fail-closed
verification and produces reproducible scaling evidence.

Target block:
- `neuro_tile16_hier` (working name)
- built as 4 coupled `neuro_tile4_coupled` quadrants with inter-quadrant links
- single external drive path with measurable propagation depth across all 16 neurons

## Netlist + Verifier Plan

Planned implementation artifacts:
- `netlists/neuro_tile16_hier.scs`
- `ocean/test_neuro_tile16_hier.ocn`

Planned netlist behavior:
1. Preserve existing per-neuron membrane/spike primitive behavior.
2. Keep intra-quadrant coupling equivalent to `neuro_tile4_coupled`.
3. Add explicit inter-quadrant feed-forward links to create a deeper propagation chain.
4. Keep exposed parameters for sweepability (`r_fb`, `rleak`, `r_couple`, `cmem`, `cpost`).

Planned verification checks:
1. All 16 membrane nodes show activity above floor thresholds.
2. Source-channel activity is present and downstream channels propagate.
3. First-spike timestamps are extracted for all channels and ordered by propagation depth.
4. Deterministic PASS/FAIL verdict in `results/neuro_tile16_hier_test.txt`.

## Tasks

- [x] Propose concrete next-scale target with implementation and verifier plan
- [ ] Implement `netlists/neuro_tile16_hier.scs`
- [ ] Implement `ocean/test_neuro_tile16_hier.ocn`
- [ ] Wire target into `build.sh` and include in `./build.sh all`
- [ ] Add first-pass robustness sweep harness for tile16 coupling/leak parameters
- [ ] Publish initial tile16 evidence summary under `competition/analysis/`

## Acceptance Criteria

1. `./build.sh neuro_tile16_hier` passes with strict fail-closed checks.
2. `./build.sh all` passes with tile16 included.
3. A documented tile16 sweep summary exists with explicit pass bands.
4. `my-workspace/docs/STATUS.md` and session logs reflect tile16 milestone progress.
