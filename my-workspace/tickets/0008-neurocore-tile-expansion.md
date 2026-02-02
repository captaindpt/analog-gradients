# 0008: NeuroCore Tile Expansion (Post-Kickoff)

**Status:** Completed
**Priority:** High
**Created:** 2026-02-02

## Description

Expand from single-neuron composition to a small neuromorphic compute tile suitable
for ICTGC demo evidence and concept-paper claims.

## Tasks

- [x] Define target tile architecture (4 channels, staggered presynaptic inputs)
- [x] Implement `netlists/neuro_tile4.scs` (multi-neuron composition)
- [x] Implement `ocean/test_neuro_tile4.ocn` with deterministic PASS/FAIL
- [x] Add build target wiring in `build.sh`
- [x] Verify with `./build.sh neuro_tile4`
- [x] Confirm full-regression compatibility with `./build.sh all`
- [x] Create competition evidence summary in `competition/verification-evidence.md`
- [x] Add metrics rollup script and output (`scripts/collect_competition_metrics.sh`, `competition/metrics-summary.md`)
- [x] Draft screenshot capture checklist in `competition/waveform-capture-checklist.md`
- [x] Add terminal diagram generator (`scripts/generate_competition_diagrams.sh`)
- [x] Add terminal waveform export + plotting pipeline and generate visuals

## Acceptance Criteria

1. `./build.sh neuro_tile4` passes
2. `results/neuro_tile4_test.txt` contains PASS verdict
3. `my-workspace/docs/STATUS.md` updated with new tile-level milestone
4. Competition visuals generated under `competition/diagrams/` and `competition/plots/`
